#! /usr/bin/env python
from __future__ import print_function
import os,subprocess
class Bash2Py(object):
  __slots__ = ["val"]
  def __init__(self, value=''):
    self.val = value
  def setValue(self, value=None):
    self.val = value
    return value

def GetVariable(name, local=locals()):
  if name in local:
    return local[name]
  if name in globals():
    return globals()[name]
  return None

def Make(name, local=locals()):
  ret = GetVariable(name, local)
  if ret is None:
    ret = Bash2Py(0)
    globals()[name] = ret
  return ret

_rc0 = subprocess.call(["ST","DETAILS","FOR","OTHER","SERVICES"],shell=True)
TECSIG01=Bash2Py("10.253.48.5")
TECSIG02=Bash2Py("10.253.48.13")
TECAPP01=Bash2Py("10.253.48.6")
TECAPP02=Bash2Py("10.253.48.14")
TECDRA01=Bash2Py("10.253.48.8")
TECDRA02=Bash2Py("10.253.48.10")
PHMSIG01=Bash2Py("10.4.67.229")
PHMSIG02=Bash2Py("10.4.67.237")
PHMAPP01=Bash2Py("10.4.67.230")
PHMAPP02=Bash2Py("10.4.67.238")
PHMDRA01=Bash2Py("10.4.67.232")
PHMDRA02=Bash2Py("10.4.67.234")
#PATH DETAILS
os.environ['SERVICE_EXE_NAME'] = "MMSERVICE"
script_path=Bash2Py("/opt/Roamware/scripts/geomonitor")
pid_file=Bash2Py(str(script_path.val)+"/mmservice.pid")
alert_file=Bash2Py(str(script_path.val)+"/failover_alert.txt")
#Timers
restart_time_threshold=Bash2Py(15)
restart_threshold=Bash2Py(5)
## CHECK IF SCRIPT IS ALREADY Running
if (os.path.exists(str(script_path.val)+"/last_run") ):
    print("Last Instance of script is still running .. Exiting ")
    exit(1)
else:
    subprocess.call(["touch",str(script_path.val)+"/last_run"],shell=True)
##################### Defined functions ##############################
#####Checking if MMS running on both nodes ##############
def check_pid () :
    global localPID
    global SERVICE_EXE_NAME
    global remotePID
    global PHMAPP02

    Make("localPID").setValue(os.popen("ps -eo \"tty pid args\" | grep "+str(SERVICE_EXE_NAME.val)+" | grep -v grep | tr -s \" \" | cut -f2 -d \" \"").read().rstrip("\n"))
    remotePID=Bash2Py(os.popen("ssh "+str(PHMAPP02.val)+" \"ps -eo 'tty pid args' | grep "+str(SERVICE_EXE_NAME.val)+" | grep -v grep | tr -s ' ' | cut -f2 -d ' '\"").read().rstrip("\n"))

def check_app_status () :
    global localPID
    global remotePID

    check_pid()
    if (str(localPID.val) == '' and str(remotePID.val) == '' ):
        print("MMS is not running on both nodes ... wait 3 mins to check again")
        subprocess.call(["sleep","180"],shell=True)
        check_pid()
        if (str(localPID.val) == '' and str(remotePID.val) == '' ):
            print("MMS is not running on both nodes ... for more than 3 minsi ... initiating failover ")
            subprocess.call(["restart_breach_action"],shell=True)
        else:
            print("MMS started after 3 mins")
    elif (str(localPID.val) == '' ):
        print("MMS is not running on local node")
    elif (str(remotePID.val) == '' ):
        print("MMS is not running on remote nodes")
    else:
        print("MMS is running on both nodes ...")
