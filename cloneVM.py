# Create multiple clones for a VM with REST
# Author: Aditya Gawade
from requests.auth import HTTPBasicAuth
from pprint import pprint
import requests
import sys
import json

# Clone name list
nameList = ["test-xyzAB", "test-xyzCD", "test-xyzEF", "test-xyzGH"]

peVIP = "10.1.1.1:9440"
baseUrl = "https://" + peVIP + ":9440/PrismGateway/services/rest/v2.0/"
headers = {'ContentType':'application/json'}
user = "admin"
passw = "Nutanix/4u"

def enterCloneName(cloneName):
    cloneData = {
    "spec_list":
       [
         {
          "name":cloneName,
          "memory_mb":4096,
          "num_vcpus":4,
          "num_cores_per_vcpu":1,
          "vm_nics":
           [
            {
             "network_uuid":"ebaf058d-b73e-43b0-a4d2-a6b4b62b27d7"
            }
           ],
          "override_network_config":True,
          "clone_affinity":False
          }
       ]
    }
    return cloneData

# standard get Request
def getRequest(baseUrl, user, passw, obj):
    comUrl = baseUrl + obj + "/"
    r = requests.get(comUrl, auth=(user, passw), verify=False)
    return r.json()

# standard post Request
def postRequest(baseUrl, user, passw, obj, data):
    comUrl = baseUrl + obj + "/"
    print("URL: ", comUrl)
    dumpData = json.dumps(cloneData, separators=(',', ':'))
    print("type", type(dumpData))
    print(dumpData)
    r = requests.post(comUrl, auth=(user, passw), data=dumpData, verify=False)
    return r.status_code

# Obtain VM UUID from Name
def getVmUuid(vmName):
    nameDict = {}
    vmJson = getRequest(baseUrl, user, passw, "vms")
    for field in vmJson["entities"]:
        dictKey = field["name"]
        nameDict[dictKey] = field["uuid"]
    try:
        vmUuid = nameDict[vmName]
        print("uuid ", vmUuid)
    except:
        print("No such vm exists")
        sys.exit(1)
    return vmUuid

# create clone for the VM
def cloneVM(vmUuid, cloneName):
    postObj = "vms/" + vmUuid + "/clone"
    value = postRequest(baseUrl, user, passw, postObj, cloneData)
    return value


if __name__ == "__main__":
    vmUuid = getVmUuid("test-xyz1")
    for cloneName in nameList:
        cloneData = enterCloneName(cloneName)
        status = cloneVM(vmUuid, cloneName)
        statString = "status for creating clone" + cloneName + " " + str(status)
        print(statString)
