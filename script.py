import parameters
from os import name
import requests
# import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
from requests.auth import HTTPBasicAuth
import json
import serial
import re


portPath = parameters.PORTPATH
timeout = parameters.TIMEOUT
baubrate = parameters.BAUDRATE

url = parameters.URL
token = parameters.TOKEN
header = parameters.HEADER
headers =json.dumps(header)

check_data = []
list_data_multiple = []

### read data to serial

def read_update():
    serial_listen = serial.Serial(portPath, baubrate,timeout = timeout)
    while serial_listen.is_open:
        data=serial_listen.readline()
        data = data.decode('utf8','ignore').strip()
        data = data.split("<=>")
        # data = max(data)
        for i in range(len(data)):
            key = data[i].find("GP_F")
            if(key != -1):
                data_handle = data[i].replace("O2",'').replace(":",'').replace("GP_F",'').replace("H2",'').split("#")
                data_handle.pop(0)
                data_handle.pop()
                data_handle.pop()
                if len(data_handle)== 5:
                    data_handle.append("-1000")
                check_data.append(data_handle)
                # print(check_data)
                return data_handle
        serial_listen.close()

### auth admin take token 
def auth():
    try:
        auth = parameters.AUTH
        auth = json.dumps(auth)
        data = requests.post(parameters.URL_AUTH, data=auth, headers =  parameters.HEADER_AUTH)
        log = data.json()
        return log["token"]
    except Exception as e:
        print("erro",":",e)

### get infomation for edge 
def map_handle_green(data):
    name = data["nameDevice"].split(" ")
    name = min(name)
    datas = {
       "id":data["_id"],
       "name_house": name,
       "id_user": data["user"]
    }
    return datas

def map_handle_green_id(data):
    datas = {
       "id":data["_id"],
    }
    return datas

def map_handle_users(data):
    datas = {
        "id": data["_id"],
        "username": data["username"]
    }
    return datas


def get_greenhouses():
    try:
        TOKEN = auth()
        role = parameters.ROLE
        # role = json.dumps(role)
        header = {'content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN) 
            }
        data = requests.get(parameters.GET_GREENHOUSES,params=role,headers=header)
        data = data.json()
        lists = data["greenhouses"]
        lists = list(map(map_handle_green,lists))
        # print(lists)
        return lists
    except Exception as e:
        print("erro get green",e)


def get_greenhouses_id():
    try:
        TOKEN = auth()
        role = parameters.ROLE
        # role = json.dumps(role)
        header = {'content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN) 
            }
        data = requests.get(parameters.GET_GREENHOUSES,params=role,headers=header)
        data = data.json()
        lists = data["greenhouses"]
        lists = list(map(map_handle_green_id,lists))
        # print(lists)
        return lists
    except Exception as e:
        print("erro get green",e)

def get_user():
    try:
        TOKEN = auth()
        role = parameters.ROLE
        # role = json.dumps(role)
        header = {'content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN) 
            }
        data = requests.get(parameters.GET_USER,params=role,headers=header)
        data = data.json()
        lists = data["users"]
        lists = list(map(map_handle_users,lists))
        # print(lists)
        return lists
    except Exception as e:
        print("erro get user",e)       

### handle data 

def list_name_handle(data):
    lists_name_enddevice = []
    key = data[0][1]
    lists_name_enddevice.append(key)
    for i in range(len(data)):
        if key != data[i][1]:
            lists_name_enddevice.append(data[i][1])
            key == data[i][1]
            return lists_name_enddevice
        else:
            return lists_name_enddevice

def average(data):
        if data:
            # print("average success")
            data = list(map(float,data)) # ep kieu list float
            SUM = sum(data)
            average = SUM/len(data)
            return average


def handle_data(data):
    try:
        data.sort()
        lists = list_name_handle(data)
        array_request = []
        # print(lists)
        for i in range(len(lists)):
            o =[]
            Temp =[]
            Hum =[]            
            array = list(filter(lambda x: x[1]==lists[i],data))
            if array:
                for j in range(len(array)):
                    o.append(array[j][3])
                    Temp.append(array[j][4])
                    Hum.append(array[j][5])
                data_checked = {
                    "name_id": lists[i],
                    "data":{
                        "Temp": average(Temp),
                        "Hum": average(Hum),
                        "CO2": average(o)
                    }
                }
                array_request.append(data_checked)
                # print(array_request)
        return array_request   
    except Exception as e:
        print(e)

### request data

def data_request_handle():    
    dt_request=handle_data(check_data)
    lists_user = get_user()
    lists_green = get_greenhouses()
    if dt_request:
        for i in range(len(dt_request)):
            name_endevice = dt_request[i]["name_id"].split("-")
            datas = dt_request[i]["data"] 
            name_endevice_green = min(name_endevice)
            name_endevice_user = max(name_endevice)

            for k in range(len(lists_user)):
                check = lists_user[k]
                if check["username"] == name_endevice_user:
                    id_user = check["id"]

            for j in range(len(lists_green)):
                check = lists_green[j]
                if check["name_house"] == name_endevice_green and check["id_user"] == id_user:
                    id_green_house = check["id"]
        
            data_checked = {
                        "greenhouseId": id_green_house,    
                        "role": "admin",   
                        "userId": id_user,

                    }
            data_checked["data"] = datas
            # print(data_checked)
            list_data_multiple.append(data_checked)


def request_data_server():
    try:
        # print(check_data)
        handle_data(check_data)
        data_request_handle()
        if list_data_multiple:
            for i in range(len(list_data_multiple)):
                if list_data_multiple[i]["data"]:
                    greenhouse_to_server = list_data_multiple[i]
                    greenhouse_to_server  = json.dumps(greenhouse_to_server)
                    res = requests.post(url, data = greenhouse_to_server, headers=header)
            print(res.status_code)
            print(greenhouse_to_server)
        list_data_multiple.clear()
    except Exception as e:
        print("erro request")
        print(e)


### Scheduler for edge 
scheduler = BlockingScheduler()
def schedule_data_day():
    scheduler.add_job(read_update,'cron',day_of_week='0-6',hour='0-23',second="*/5") #rm reead_data
    scheduler.add_job(request_data_server,'cron',day_of_week='0-6',hour='0-23', minute="*/5" )

### Run edge  
print("RUN")
schedule_data_day()
scheduler.start()
