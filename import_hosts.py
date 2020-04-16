import requests
import json

class centreonAPI:
    def __init__(self,domaine,secure,username,password):
        self.username=username
        self.password=password
        if secure is False:
            self.dns="http://"
        else:
            self.dns="https://"
        self.dns=self.dns+domaine
        self.token=self.auth()


    def auth(self):
        payload = {'username': self.username,'password': self.password}
        response = requests.request("POST", self.dns+"/centreon/api/index.php?action=authenticate", data=payload)
        if response.status_code == 200:
            return response.json()["authToken"]
        else:
            return ""

    def manageHosts(self,action,values):
        payload = '{\r\n  "action": "'+action+'",\r\n  "object": "host",\r\n  "values": "' + values + '"\r\n}'
        headers = {
            'Content-Type': 'application/json',
            'centreon-auth-token': self.token,
        }
        response = requests.request("POST", self.dns+"/centreon/api/index.php?action=action&object=centreon_clapi", headers=headers, data=payload)
        r = response.text.encode("utf-8")
        if r == '{"result":[]}':
            print "Ok"
        else:
            print r

    def parseForAction(self,f,what,action):
        with open(f) as file:
            data = file.readline()
            while data:
                info = data.split(";")
                values=""
                for i in range(len(info)):
                    values =  values+info[i] + ";"
                values=values[:-1].strip()
                # values = info[0].strip()
                if what == "host":
                    self.manageHosts(action, values)
                data = file.readline()


c =centreonAPI("192.168.1.201",False,"gabriel","uykO3L0E")
c.parseForAction("hostdel.txt","host","del")

