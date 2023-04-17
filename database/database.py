from pymongo import MongoClient
import os
from dotenv import load_dotenv

#  load environment variables from .env file
load_dotenv()

# get environment variables
MONGODB_URI= os.environ.get('MONGODB_URL')
print(MONGODB_URI)
DB_NAME = os.environ.get('DATABASE_NAME')
employees = os.environ.get('COLLECTION_NAME_Employee')
signup = os.environ.get('COLLECTION_NAME_EmployeeSignup')
login = os.environ.get('COLLECTION_NAME_EmployeeLogin')
reporters = os.environ.get('COLLECTION_NAME_Reporters')





client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
employees = db.employees
signup = db.signup
login = db.login
reporters = db.reporters
