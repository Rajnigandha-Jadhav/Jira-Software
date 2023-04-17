from dataclasses import dataclass,field
from typing import List,Optional
from dataclass_wizard import JSONSerializable



# @dataclass
# class Posts(JSONSerializable):
#     post: str

@dataclass
class Employee(JSONSerializable):
    fullname: str
    email: str
    password: str
    

@dataclass
class Task(JSONSerializable):
    Title: str
    Description: str
    Reporter: str
    Assignee: str


@dataclass
class CommentInfo(JSONSerializable):
    commenter:str
    comment:str

@dataclass
class EmployeeInfo(JSONSerializable):
    fullname: str
    email: str
    taskassigned: Optional[List[Task]] = field(default_factory=list)
    taskemail: Optional[List[Task]] = field(default_factory=list)
    commenter: Optional[List[CommentInfo]] = field(default_factory=list)
    comments: Optional[List[CommentInfo]] = field(default_factory=list)
    
   

@dataclass
class Login(JSONSerializable):
    email: str
    password: str


