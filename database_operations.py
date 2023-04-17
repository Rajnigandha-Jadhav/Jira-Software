from database.database import signup,login,employees,reporters

def insertDoc(request_data):
    signup.insert_one(request_data)

def getDoc(request_data):
    return signup.find_one(request_data)

def insertLogin(request_data):
    login.insert_one(request_data)

def getLoginInfo(request_data):
    return login.find_one(request_data)


def insertEmployee(request_data):
    employees.insert_one(request_data)

def getEmployee(request_data):
    return employees.find_one(request_data)

def getAllEmployees(request_data):
    return employees.find(request_data)

def updateEmployee(query,update_data):
    employees.update_one(query,update_data)

def insertReporter(request_data):
    reporters.insert_one(request_data)

def getReporter(request_data):
    return reporters.find_one(request_data)

def updateReporter(query, update_data):
    reporters.update_one(query,update_data)