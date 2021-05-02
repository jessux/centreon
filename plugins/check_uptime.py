#!/usr/bin/python

import plac
import getopt
import sys
import re
from subprocess import Popen, PIPE
import datetime

SNMPGET_BIN = '/usr/bin/snmpget'
SNMP_ENGINE_OID = '.1.3.6.1.6.3.10.2.1.3.0'
SNMP_UPTIME_OID = '.1.3.6.1.2.1.1.3.0'

host=""
community=""
warning=0
critical=0

def get_uptime(host,community,warning,critical):
    # first search the SNMP engine time OID
    port = 161

    status= 3
    perfdata=""
    message=""
    method=""
    mycode, stdout = snmpget(host, port, community, SNMP_ENGINE_OID)
    match = re.search('INTEGER:\W*(\d+)\W*seconds',str(stdout))
    if match:
        uptime_sec = int(match.group(1))
        method = 'engine'
    else:
        # no match, continue on to using the SysUpTime OID
        mycode, stdout = snmpget(host, port, community, SNMP_UPTIME_OID)
        #print stdout
        match = re.search('Timeticks:\W*\((\d+)\)\W*', stdout)
        if match:
            uptime_sec = int(match.group(1)) / 100
            method = 'sysUptime'
        else:
            message= 'CRITICAL: Unable to determine uptime'
            status = 2
    if method != "":
        if uptime_sec < critical:
            message = "CRITICAL: Uptime less than "+str(datetime.timedelta(seconds=critical))+" : is currently "+str(datetime.timedelta(seconds=uptime_sec))+" (SNMP method: "+method+")"
            status = 2
        elif uptime_sec < int(warning):
            message = 'WARNING: Uptime less than '+str(datetime.timedelta(seconds=warning))+': is currently '+str(datetime.timedelta(seconds=uptime_sec))+' (method: '+method+')'
            status = 1
        else:
            message = 'UPTIME OK: '+str(datetime.timedelta(seconds=uptime_sec))+' (method: '+method+')'
            status = 0
        perfdata = "'uptime_sec'="+str(datetime.timedelta(seconds=uptime_sec))+" seconds"
        #print(message,perfdata,status)
    return message,perfdata,status

def snmpget(host, port, community, oid):
        snmpe = Popen([SNMPGET_BIN,'-v','2c','-c',community,host + ':' + str(port),oid], stdout=PIPE)
        sout, serr = snmpe.communicate()
        return (snmpe.returncode, sout)

def main(argv):
    opts,args= getopt.getopt(argv,"hH:C:w:c:",["help","host","community","warning","critical"])
    global host,community,warning,critical
    for option,value in opts:
        if option in ("-h","--help"):
            sys.exit(0)
        elif option in ("-H","--host"):
            host=value
        elif option in ("-C","--community"):
            community=value
        elif option in ("-w","--warning"):
            warning=int(value)
        elif option in ("-c","--critical"):
            critical=int(value)

if __name__ == '__main__':
    argv = sys.argv[1:]
    main(argv)
    message,perfdata,status = get_uptime(host,community,warning,critical)
    print(message + "|" + perfdata)
    sys.exit(status)

# snmp engine
# .1.3.6.1.6.3.10.2.1.3.0

# sysUptime
# .1.3.6.1.2.1.1.3.0