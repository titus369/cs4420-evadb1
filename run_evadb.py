# CS 4420 EvaDB Project 1
# Andrew Titus

# Import the EvaDB package
import evadb
#from evadb import ludwig
#import numpy as np
#import psycodb2

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

# List all the built-in functions in EvaDB
print(cursor.query("SHOW FUNCTIONS;").df())

# Connects PostgreSQL LoanDefault Database to EvaDB
# postgres at port 5432 localhost -> ngrok server at tcp://4.tcp.ngrok.io:17588
params = {
    "user": "postgres",
    "password": "", # enter PostgreSQL password here
    "host": "localhost",
    "port": "5432",
    "database": "LoanDefault",
}
query = f"CREATE DATABASE pg WITH ENGINE = 'postgres', PARAMETERS = {params};"
#print(query)
#cursor.query(query).df()
print(cursor.query(query).df())

# Previews Data by providing 5 items from the loan_default_lite table
print(cursor.query("SELECT * FROM pg.loan_default_lite LIMIT 5;").df())

# Attempt to use Ludwig to Create a Prediction function
cursor.query("CREATE OR REPLACE FUNCTION Predict FROM (SELECT * FROM pg.loan_default_lite) TYPE Ludwig PREDICT 'status' TIME_LIMIT 120;").df()

# Attempt to use Sklearn instead of Ludwig
#print(cursor.query("CREATE OR REPLACE FUNCTION Predict FROM (SELECT * FROM pgdb.loan_default_lite) TYPE Sklearn PREDICT 'status';").df())

