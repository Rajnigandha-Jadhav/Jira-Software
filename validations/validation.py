from models.model import Employee,Login,EmployeeInfo,Task,CommentInfo
from marshmallow import Schema, fields, post_load, validate




class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    

    @post_load
    def login_employee(self, data, **kwargs):
        return Login(**data)



class EmployeeSchema(Schema):
    fullname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    

    @post_load
    def make_employee(self, data, **kwargs):
        return Employee(**data)





class TaskSchema(Schema):
    Title = fields.Str(required=True)
    Description = fields.Str(required=True)
    Reporter = fields.Str(required=True)
    Assignee = fields.Str(required=True)


    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)




class CommentInfoSchema(Schema):
    commenter = fields.Str(required=True)
    comment = fields.Str(required=True)
    

    @post_load
    def make_comment(self, data, **kwargs):
        return CommentInfo(**data)
    



class EmployeeInfoSchema(Schema):
    fullname = fields.Str(required=True)
    email = fields.Email(required=True)
    taskassigned : fields.List(fields.Nested(TaskSchema))
    taskemail : fields.List(fields.Nested(TaskSchema))
    commenter : fields.List(fields.Str())
    comments : fields.List(fields.Str())

    

    @post_load
    def make_employeeinfo(self, data, **kwargs):
        return EmployeeInfo(**data)




