PORTPATH ="/dev/ttyUSB0"
# PORTPATH ="/dev/ttyAMA0"
TIMEOUT = 5
BAUDRATE = 115200

####### request server ###########33
URL = 'https://greenhouseserver.herokuapp.com/greenhouse/add'

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2MjI5Nzk1MTlhYWE0NjI1YjBhMDVhZmYiLCJpYXQiOjE2NTE4MDk5NzJ9.KkkZEG33O8eb5BzXAr_4cfL5ugWXtCg__GEjasxkM8M"
HEADER = {'content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN) 

}


URL_AUTH = 'https://greenhouseserver.herokuapp.com/auth/login'
AUTH = {
    "username":"admin",
    "password":"123"
}
HEADER_AUTH = {'content-Type': 'application/json'}

ROLE = {
    "role": "admin"
}
GET_GREENHOUSES = "https://greenhouseserver.herokuapp.com/greenhouse/all"
GET_USER = "https://greenhouseserver.herokuapp.com/user"