from flask import Flask, request, jsonify
from database.database import employees,signup,login,reporters
from database_operations import insertDoc,getDoc,insertLogin,getLoginInfo,insertEmployee,getEmployee,updateEmployee,insertReporter,getReporter,updateReporter,getAllEmployees
from validations.validation import EmployeeSchema,LoginSchema,EmployeeInfoSchema,TaskSchema,CommentInfoSchema
from bson import ObjectId
from dataclasses import asdict
import json
employee_schema = EmployeeSchema()
login_schema = LoginSchema()
employeeinfo_schema = EmployeeInfoSchema()
task_schema = TaskSchema()
comment_schema = CommentInfoSchema()

app = Flask(__name__)

#SignUp API :=>
@app.route('/signup', methods=['POST'])
def signup_employee():
    try:
        employee_data = request.json
        print(employee_data)
        if not employee_data:
            resp = jsonify({'Success':False,'message': 'Please provide some data','Status':400})
            resp.status_code = 400
            return resp
    
        employeeInfo = employee_schema.load(employee_data)
       
        insertDoc(asdict(employeeInfo))
        resp = jsonify({'message': 'employee signup successfull','Success':True,'Status':201})
        
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp




#Login API :=>
@app.route('/login', methods=['POST'])
def login_employee():
    try:
        login_data = request.json
        print(login_data)
        if not login_data:
            resp = jsonify({'Success': False, 'message': 'Please provide email and password', 'Status': 400})
            resp.status_code = 400
            return resp

        email = login_data.get('email', None)
        password = login_data.get('password', None)
        
        if not email or not password:
            resp = jsonify({'Success': False, 'message': 'Please provide both email and password', 'Status': 400})
            resp.status_code = 400
            return resp
        
        employee = getDoc({'email': email,'password':password})
        
        if not employee:
            resp = jsonify({'Success': False, 'message': 'Invalid email or password', 'Status': 401})
            resp.status_code = 401
            return resp
        

        loginInfo = login_schema.load(login_data)
        insertLogin(asdict(loginInfo))
        resp = jsonify({'Success': True, 'message': 'Login successful', 'Status': 200})
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp





#Create an Employee :=>
@app.route('/employeeinfo', methods=['POST'])
def create_employee():
    try:
        employee_data = request.json
        print(employee_data)
        if not employee_data:
            resp = jsonify({'Success':False,'message': 'Please provide some data','Status':400})
            resp.status_code = 400
            return resp
        


        email = employee_data.get('email')
        employee = getLoginInfo({'email': email})
        
        if not employee:
            resp = jsonify({'Success': False, 'message': 'please login first', 'Status': 401})
            resp.status_code = 401
            return resp
    
        employeeInfo = employeeinfo_schema.load(employee_data)
       
        insertEmployee(asdict(employeeInfo))
        resp = jsonify({'message': 'employee document saved successfully','Success':True,'Status':201})
        
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp








#Assign a REPORTER from Employees:=>
@app.route('/reporterinfo', methods=['POST'])
def create_reporter():
    try:
        reporter_data = request.json
        print(reporter_data)
        if not reporter_data:
            resp = jsonify({'Success':False,'message': 'Please provide some data','Status':400})
            resp.status_code = 400
            return resp
        

        fullname = reporter_data.get('fullname')
        email = reporter_data.get('email')
        employee = getEmployee({'fullname':fullname,'email': email})
        
        if not employee:
            resp = jsonify({'Success': False, 'message': 'Not present in employee data', 'Status': 401})
            resp.status_code = 401
            return resp
    
        reporterInfo = employeeinfo_schema.load(reporter_data)
       
        insertReporter(asdict(reporterInfo))
        resp = jsonify({'message': 'reporter document saved successfully','Success':True,'Status':201})
        
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp





#Task Assigned By Reporter :=> 
@app.route('/tasks', methods=['POST'])
def assign_task():
    try:
        task_data = request.json

        if not task_data:
            return jsonify({'error': 'Please provide the data'}), 400
        
       
        task_info = task_schema.load(task_data)
        dict1 = asdict(task_info)
        Reporter_id = dict1["Reporter"]
        task_title = dict1["Title"]
        assignee_id = dict1["Assignee"]
        desc = dict1["Description"]
   
        Reporter_doc = getReporter({'_id': ObjectId(Reporter_id)})
        if not Reporter_doc:
            return jsonify({'error': 'Reporter not found'}), 404
            
        Reporter_name = Reporter_doc["fullname"]
        Reporter_task = Reporter_doc["taskassigned"]
        

       #Reporter can assign task to themselves else to all other employees...
        
        if Reporter_id == assignee_id:
            Reporter_task.append(task_title)
            updateReporter({'_id': ObjectId(Reporter_id)}, {'$set': {'taskassigned': Reporter_task}})

        else:

            Assignee_doc = getEmployee({'_id': ObjectId(assignee_id)})
            if not Assignee_doc:
              return jsonify({'error': 'Assignee not found'}), 404
            
            Assignee_name = Assignee_doc["fullname"]
            assignee_task = Assignee_doc["taskassigned"]
            Assignee_email = Assignee_doc["taskemail"]
            assignee_task.append(task_title)
            updateEmployee({'_id': ObjectId(assignee_id)}, {'$set': {'taskassigned': assignee_task}})
 
            Assignee_email.append({"Title": task_title, "Reporter": Reporter_name})
            updateEmployee({'_id': ObjectId(assignee_id)}, {'$set': {'taskemail': Assignee_email}})
 

     
        # Return success response
        resp = jsonify({'message': 'data added successfully'})
        resp.status_code = 201
        return resp

    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp




#ADD Comments :=>
@app.route('/comments/<string:employee_id>', methods=['POST'])
def comment_on_task(employee_id):
    try:
        comment_data = request.json

        if not comment_data:
            return jsonify({'error': 'Please provide the data'}), 400
        
       
        comment_info = comment_schema.load(comment_data)
        dict1 = asdict(comment_info)
        Commenter_id = dict1["commenter"]
        Comments = dict1["comment"]
       
        

        Reporter_doc = reporters.find_one({})
        Reporter_id = Reporter_doc["_id"]
        Reporter_taskemail = Reporter_doc["taskemail"]

        


        Assignee_doc = employees.find_one({'_id': ObjectId(employee_id)})
        if not Assignee_doc:
            return jsonify({'error': 'Assignee not found'}), 404
            
        Assignee_email = Assignee_doc["taskemail"]
        task_commenter = Assignee_doc["commenter"]
        comment_on_task = Assignee_doc["comments"]
        Assignee_name = Assignee_doc["fullname"]
        
     # Comments can be added by employees on their own task, or else comments can be added by other employees or comments can be added by REPORTER too..
        if ObjectId(Commenter_id) == ObjectId(employee_id):
            Reporter_doc = reporters.find_one({})
            Reporter_taskemail = Reporter_doc["taskemail"]
            Reporter_id = Reporter_doc["_id"]   
        
            Reporter_taskemail.append({"Commenter":Assignee_name,"Comments": Comments})
            reporters.update_one({'_id': ObjectId(Reporter_id)}, {'$set': {'taskemail': Reporter_taskemail}})

        elif ObjectId(Commenter_id) != ObjectId(Reporter_id) and ObjectId(Commenter_id) != ObjectId(employee_id):
            commenter_doc = employees.find_one({'_id':ObjectId(Commenter_id)})
            commenter_name = commenter_doc["fullname"]

            Reporter_taskemail.append({"Commenter":commenter_name,"Comments": Comments})
            reporters.update_one({'_id': ObjectId(Reporter_id)}, {'$set': {'taskemail': Reporter_taskemail}})

            
            task_commenter.append(commenter_name)
            reporters.update_one({'_id': ObjectId(employee_id)}, {'$set': {'commenter': task_commenter}})


            
            comment_on_task.append(Comments)
            reporters.update_one({'_id': ObjectId(employee_id)}, {'$set': {'comments': comment_on_task}})



            Assignee_email.append({"Commenter": commenter_name, "Comments": Comments})
            reporters.update_one({'_id': ObjectId(employee_id)}, {'$set': {'taskemail': Assignee_email}})
    

        else:

            Reporter_doc = reporters.find_one({'_id': ObjectId(Commenter_id)})
            if not Reporter_doc:
                return jsonify({'error': 'Reporter not found'}), 404
                
            Reporter_name = Reporter_doc["fullname"]




            task_commenter.append(Reporter_name)
            employees.update_one({'_id': ObjectId(employee_id)}, {'$set': {'commenter': task_commenter}})


            
            comment_on_task.append(Comments)
            employees.update_one({'_id': ObjectId(employee_id)}, {'$set': {'comments': comment_on_task}})



            Assignee_email.append({"Commenter": Reporter_name, "Comments": Comments})
            employees.update_one({'_id': ObjectId(employee_id)}, {'$set': {'taskemail': Assignee_email}})
    

     
        # Return success response
        resp = jsonify({'message': 'comments added successfully'})
        resp.status_code = 201
        return resp

    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp



#Show tasks assigned to a employee by their ids...
@app.route('/employee_tasks/<string:employee_id>', methods=['GET'])
def show_task(employee_id):
    try:
        employee_data = getEmployee({'_id': ObjectId(employee_id)})
        employee_dict = {
            'taskassigned': employee_data['taskassigned']
        }
        resp = jsonify(employee_dict)
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp




#Show all tasks assigned to all employees with their full name...
@app.route('/all-Tasks', methods=['GET'])
def get_all_tasks():
    try:
        all_employees = getAllEmployees({})
        employees_list = []
        for employee_data in all_employees:
            employee_dict = {
                "fullname":employee_data['fullname'],
                'taskassigned': employee_data['taskassigned']
            }
            employees_list.append(employee_dict)
        resp = jsonify(employees_list)
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'Success': False, 'message': 'An error occurred: ' + str(e), 'Status': 500})
        resp.status_code = 500
        return resp   




if __name__ == '__main__':
    app.run(debug=True)
