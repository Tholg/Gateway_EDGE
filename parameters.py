PORTPATH ="/dev/ttyUSB0"
# PORTPATH ="/dev/ttyAMA0"
TIMEOUT = 5
BAUDRATE = 115200

####### request server ###########33
URL = 'http://localhost:5000/greenhouse/add'

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2MjI5Nzk1MTlhYWE0NjI1YjBhMDVhZmYiLCJpYXQiOjE2NTE4MDk5NzJ9.KkkZEG33O8eb5BzXAr_4cfL5ugWXtCg__GEjasxkM8M"
HEADER = {'content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN) 

}


URL_AUTH = 'http://127.0.0.1:5000/auth/login'
AUTH = {
    "username":"admin",
    "password":"123"
}
HEADER_AUTH = {'content-Type': 'application/json'}

ROLE = {
    "role": "admin"
}
GET_GREENHOUSES = "http://localhost:5000/greenhouse/all"
GET_USER = "http://localhost:5000/user"