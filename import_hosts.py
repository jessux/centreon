import requests
import config
import logging
import re
import sys


class centreonAPI:
    def __init__(self,file,action):
        self.username=config.USERNAME
        self.password=config.PASSWORD
        self.url=config.URL
        self.token = config.TOKEN
        #logger name
        self.log = logging.getLogger('centreonAPI')
        # setLevel
        self.log.setLevel(config.LOG_LEVEL)
        #log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        if config.LOG_TYPE=="both":
            fh = logging.FileHandler(config.LOG_TYPE)
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            self.log.addHandler(fh)
            self.log.addHandler(ch)
        elif config.LOG_TYPE=="console":
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.log.addHandler(ch)
        elif config.LOG_TYPE=="file":
            fh = logging.FileHandler(config.LOG_FILENAME)
            fh.setFormatter(formatter)
            self.log.addHandler(fh)
        else:
            logging.warning("No logging configuration was found. Please set LOG_TYPE and LOG_FILENAME in the config.py file")
            return
        self.parseForAction(file,action)

    def auth(self):
        self.log = logging.getLogger('centreonAPI.auth')
        payload = {'username': self.username,'password': self.password}
        response = requests.request("POST", self.url+"/centreon/api/index.php?action=authenticate", data=payload)
        self.log.debug("status_code : "+str(response.status_code)+ " Content : "+response.text.encode('utf-8'))
        if response.status_code == 200:
            self.token = response.json()["authToken"]
            fin = open("config.py", "rt")
            data = fin.read()
            data = re.sub('TOKEN="(.*)"','TOKEN="'+self.token+'"',data)
            fin.close()
            fin = open("config.py", "wt")
            fin.write(data)
            fin.close()



    def manageHosts(self,action,values):
        self.log = logging.getLogger('centreonAPI.manageHosts')
        payload = '{\r\n  "action": "'+action+'",\r\n  "object": "host",\r\n  "values": "' + values + '"\r\n}'
        headers = {
            'Content-Type': 'application/json',
            'centreon-auth-token': self.token,
        }
        response = requests.request("POST", self.url+"/centreon/api/index.php?action=action&object=centreon_clapi", headers=headers, data=payload)
        r = response.text.encode("utf-8")
        self.log.debug("status_code : "+str(response.status_code)+ " Content : "+response.text.encode('utf-8'))
        if response.status_code==200:
            return 0,r
        elif response.status_code==403:
            self.auth()
            return self.manageHosts(action, values)
        elif response.status_code==409:
            return 1,r
        else:
            return -1,r


    def parseForAction(self,f,action):
        with open(f) as file:
            data = file.readline()
            while data:
                info = data.split(";")
                values=""
                for i in range(len(info)):
                    values =  values+info[i] + ";"
                values=values[:-1].strip()
                # values = info[0].strip()
                out,result = self.manageHosts(action, values)
                if out == -1:
                    self.log.warning("A problem occured : "+result)
                    return
                elif out == 1:
                    self.log.info(result)
                elif out == 0:
                    self.log.info("Host : "+values.split(';')[0]+" --> Ok")
                data = file.readline()


c=centreonAPI(sys.argv[1],sys.argv[2])

