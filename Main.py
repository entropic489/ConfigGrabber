import sys
sys.path.append('/usr/lib/python3.5')
import netmiko
from Tkinter import *

root = Tk()
devices = []

#Gets values from textboxes, checks for duplicate entries, and calls the add_device function
def grab_values():
    output_text.delete(1.0, END)

    is_duplicate = False

    name = name_text.get("1.0", 'end-1c')
    ip = ip_text.get("1.0", 'end-1c')
    username = username_text.get("1.0", 'end-1c')
    password = password_text.get("1.0", 'end-1c')
    enable_secret = enable_secret_text.get("1.0", 'end-1c')

    for device in devices:
        device_ip = device.get('ip')
        if device_ip == ip:
            is_duplicate = True
    
    if is_duplicate:
        output_text.insert(END, "Device Already Exists")
    elif is_duplicate == FALSE or len(devices) == 0:
        add_device(name, ip, username, password, enable_secret)
    else:
        output_text.insert(END, "Failure")

#adds the device to the devices list
def add_device(name, ip, username, password, enable_secret):
    name = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    devices.append(name)

#iterates through device list, establishes ssh connection, pulls running config, and outputs to file
def get_configs():
    for device in devices:
        connection = netmiko.ConnectHandler(**device)
        connection.enable()
        config_output = connection.send_command("show run")
        new_output = ">>>>>>>>Device {0}<<<<<<<<<".format(device['ip']) + "\n" + config_output + "\n>>>>>>>>>END<<<<<<<<"
        output_text.insert(END, ">>>>>>>>Device {0}<<<<<<<<<".format(device['ip']))
        output_text.insert(END, config_output)
        output_text.insert(END, ">>>>>>>>>END<<<<<<<<")
        f = open('/home/*****/Desktop/ConfigOutput.txt', 'w')
        f.write(new_output)
        f.close()

#saves current devices to txt file
def save_devices():
    f = open('/home/*****/Desktop/DeviceList.txt', 'w')
    for device in devices:
        f.write('cisco_ios\n' + str(device.get('ip')) + "\n" + str(device.get('username')) + "\n" + str(device.get('password')) + "\n" + str(device.get('secret')) + "\n")
    f.close()

#loads saved devices from txt file
def open_devices():
    f = open('/home/*****/Desktop/DeviceList.txt', 'r')
    device_count = sum(1 for line in open('/home/*****/Desktop/DeviceList.txt'))
    device_count /= 5
    for i in range(1, device_count):
        add_device(f.readline(1 + i), f.readline(2 + i), f.readline(3 + i), f.readline(4 + i), f.readline(5 + i))
    f.close()

    output_text.insert(END, device_count)


#gui generation
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Devices", command=open_devices)
filemenu.add_command(label="Save Devices", command=save_devices)
menubar.add_cascade(label="File", menu = filemenu)
root.config(menu=menubar)
name_text = Text(root, height=8)
name_text.pack()
ip_text = Text(root, height=8)
ip_text.pack()
username_text = Text(root, height=8)
username_text.pack()
password_text = Text(root, height=8)
password_text.pack()
enable_secret_text = Text(root, height=8)
enable_secret_text.pack()
add_button = Button(root, text="Add Device", command=grab_values)
add_button.pack()
config_button = Button(root, text="Get Running Configs", command=get_configs)
config_button.pack()
output_text = Text(root, height=8)
output_text.pack()

#deprecated, resets text boxes to default labels
def set_text():
    name_text.delete(1.0,END)
    name_text.insert(END, "Device Name Here")
    ip_text.delete(1.0,END)
    ip_text.insert(END, "Device IP Here")
    username_text.delete(1.0,END)
    username_text.insert(END, "Username Here")
    password_text.delete(1.0,END)
    password_text.insert(END, "User Pass Here")
    enable_secret_text.delete(1.0,END)
    enable_secret_text.insert(END, "Enable Secret Here")

set_text()

root.mainloop()



