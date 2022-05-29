import Ice
import sys
import SmartHome_ice

SmartHome = Ice.openModule("SmartHome")
communicator = Ice.initialize(sys.argv)

objects = {}

address1 = "tcp -h 127.0.0.2 -p 10001 -z : udp -h 127.0.0.2 -p 10001 -z"
address2 = "tcp -h 127.0.0.2 -p 10002 -z : udp -h 127.0.0.2 -p 10002 -z"


class ObjProxy:
    def __init__(self, name, category, address):
        self.name = name
        self.category = category
        self.address = address;


def castObject(category, name, address, obj):
    return obj.checkedCast(communicator.stringToProxy(
        category + "/" + name + ":" + address))


def getObjectProxy(category, name, address):
    if category == "MD":
        return castObject(category, name, address, SmartHome.MultimediaDevicePrx)
    elif category == "TVS":
        return castObject(category, name, address, SmartHome.TvSmartPrx)
    elif category == "MP":
        return castObject(category, name, address, SmartHome.MusicPlayerPrx)
    elif category == "F":
        return castObject(category, name, address, SmartHome.FridgePrx)
    elif category == "BF":
        return castObject(category, name, address, SmartHome.BigFridgePrx)
    elif category == "T":
        return castObject(category, name, address, SmartHome.ThermometerPrx)
    elif category == "Util":
        return castObject(category, name, address, SmartHome.DevicesUtilPrx)


def updateDevices(devicesList):
    objects.clear()
    for objectProxy in devicesList:
        try:
            objects[objectProxy.name] = getObjectProxy(objectProxy.category, objectProxy.name, objectProxy.address)
        except:
            print("Device " + objectProxy.name + " is not available")


def update():
    aDList = [ObjProxy("util1", "Util", address1), ObjProxy("util2", "Util", address2)]
    try:
        adList1 = objects["util1"].getAvailableDevices()
        if adList1:
            aDList += adList1
    except:
        print("Server 1 is not available")

    try:
        adList2 = objects["util2"].getAvailableDevices()
        if adList2:
            aDList += adList2
    except:
        print("Server 2 is not available")

    updateDevices(aDList)
    print(aDList)


objectsProxyList = [ObjProxy("util1", "Util", address1), ObjProxy("util2", "Util", address2)]
updateDevices(objectsProxyList)

while True:
    print()
    deviceId = input("Enter Device ID or 'update' devices list: \n")
    if deviceId == "update":
        update()
        continue
    try:
        device = objects[deviceId]

        method = input("Device functionality: \n")
        if method == "turn on":
            print(device.turnOn())
        elif method == "turn off":
            print(device.turnOff())
        elif method == "get state":
            print(device.getState())
        elif method == "get song":
            print(device.currentlyPlaying())

        elif method == "play song":
            songName = input("Enter song name: ")
            print(device.playSong(songName))

        elif method == "get songs":
            print(device.getAvailableSongs())

        elif method == "get app":
            print(device.openedApp())

        elif method == "get apps":
            print(device.getApplicationsList())

        elif method == "open app":
            appName = input("Enter app name: ")
            print(device.openApp(appName))

        elif method == "produce ice":
            print(device.produceIce())

        elif method == "get fridge temperature":
            print(device.currentTemperature())

        elif method == "change temperature":
            temp = input("Enter new temperature: ")
            print(device.changeTemperature(int(temp)))

        elif method == "get air temperature":
            print(device.getCurrentTemperature())

        elif method == "get last week temperature":
            print(device.getLastWeekTemperature())

        elif method == "":
            continue
        else:
            print("There is no entered method")
    except SmartHome.ContainerFull:
        print("Ice container is full")
    except SmartHome.TemperatureOutOfRange as e:
        print(e.text)
    except SmartHome.DeviceTurnedOff:
        print("Device is turned off. Type command 'turn on'")
    except SmartHome.NotFound:
        print("App/Song not found")
    except KeyError:
        print("There is no entered device")
    except:
        print("There is no such method in device")
