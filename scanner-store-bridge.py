import serial, pdb, time, re, sys, datetime
from urllib import request, parse

def send_results(base_url, device_name, tag, crossing_data):
    """
    submit crossing data to the specified scanner store URL
    """
    #append appropriate endpoint to the base url
    url = base_url + "/new/result"
    request_dict = {"device_name": device_name,
                    "time": datetime.datetime.now(), 
                    "tag": tag,
                    "raw_results": crossing_data}

    request_data = parse.urlencode(request_dict).encode()
    req = request.Request(url, data=request_data)

    resp = request.urlopen(req)

def create_device(base_url, device_name, device_type, sensor_x, sensor_y):
    """
    Using the REST api on the base_url, create a new scanner device entry with the provided parameters.
    Device name is the device for the new device
    Device type is a decriptor field, classifying the device. Perhaps version/prototype etc.
    Sensor_x/y are the sensor element size
    """

    url = base_url + "/new/device"
    request_dict = {"device_name": device_name,
            "device_type": device_type,
            "sensor_x": sensor_x,
            "sensor_y": sensor_y}

    request_data = parse.urlencode(request_dict).encode()
    req = request.Request(url, data=request_data)

    resp = request.urlopen(req)

store_url = "http://localhost"
device_name = "results"
serial_device = 'COM5'

crossing_data = []
string = ""

print("ready to open")

#open the serial connection

#basic argument parsing, decide if we should display the help, create a new device
#or start listening to a COM port for crossing data to forward
if sys.argv[1] == 'new_device':
    print("creating device")
    print("Name: {}".format(sys.argv[2]))
    print("Type: {}".format(sys.argv[3]))
    print("Sensor x: {}".format(sys.argv[4]))
    print("Sensor y: {}".format(sys.argv[5]))
    create_device(store_url, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    print ("Creation done")
    sys.exit(0)
if "help" in sys.argv[1]:
    print("""
    usage: 
        forward-crossing-to-store.py [help|new_device|tag] <param 1> ...

        if help given, show this message
        if new_device given, then create a new device in the db then exit.
        new_device paramaters:
            name - device name
            type - device type
            sensor_x - x width of device
            sensor_y - y width of device. 

            Example usage:

            forward-crossing-to-store.py new_device test-device arduino-scanner 10 1

        if you give a tag instead of one of the other commands, then that tag will be passed to the scanner, and will be added to any crossing data forwarded to the store.
        allowed characters are anything alphanumeric, comma or colon.
        
        Example usage:

        forward-crossing-to-store.py a:1,b:3,test:true,nodebug
        """)
    sys.exit(0)

#decided to start listening for data
elif len(sys.argv) > 1:
    ser = serial.Serial(serial_device, baudrate=115200, timeout=.2)
    #wait for the device to do start up routine
    time.sleep(3)
    #join the arguments from the command line and set the tag
    tag = ' '.join(sys.argv[1:])
    #inform the user of the tag for the current session
    print("Setting tag: '{}'".format(tag))

try:
    #initialize the string variagle
    string = ""
    while True:
        #if the serial connection has bytes waiting, get them and append them to the string
        if ser.in_waiting > 0:
            time.sleep(0.04)
            string += ser.read_all().decode("ascii") 

        #check the string against the RE
        match = re.search("Total crossings: (\d+)\r?\n\r?\n?\n\r?\n?([\d \n\r]+)+\r?\n?=+", string, re.MULTILINE)

        #string matches the re
        if match:
            #print the crossing details
            crossing_data = match.groups()[1].strip()
            print("===============")
            print("Crossings: {}".format(match.groups()[0]))
            print("Tag: {}".format(tag))
            print("----------------")
            print(crossing_data)
            
            #zero the current string
            string = ""

            #transmit the crossing details to the store
            send_results(store_url, device_name, tag, crossing_data)
            time.sleep(0.2)
            ser.flushInput()
            ser.flushOutput()

        sys.stdout.flush()
        time.sleep(0.5)

except KeyboardInterrupt:
    pdb.set_trace() #enter interative debugging with ctrl + c
    pass
