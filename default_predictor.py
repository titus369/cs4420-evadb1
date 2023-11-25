# -*- coding: utf-8 -*-
"""default_predictor.ipynb

# **Setup**

## **Install and Launch The Postgres Server**
"""

"""
!apt -qq install postgresql
!service postgresql start
"""

"""## **Create Postgres User and Database**"""

"""
!sudo -u postgres psql -c "CREATE USER eva WITH SUPERUSER PASSWORD 'password'"
!sudo -u postgres psql -c "CREATE DATABASE evadb"
"""

"""## **Installing EvaDB and Necessary Packages / Dependencies**"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install fastapi
# %pip install kaleido
# %pip install python-multipart
# %pip install jedi
# %pip install uvicorn
# %pip install --upgrade pip setuptools wheel
# %pip install --upgrade evadb

# %pip install psycopg2

"""## **Setting Up EvaDB**"""

# CS 4420 EvaDB Project 2
# Andrew Titus

# Import the EvaDB package
import evadb
#from evadb import ludwig
import numpy as np
import psycopg2

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

# List all the built-in functions in EvaDB
print(cursor.query("SHOW FUNCTIONS;").df())

"""## **Setting Up PostgreSQL Data Source with EvaDB**"""

# Connects PostgreSQL LoanDefault Database to EvaDB
params = {
    "user": "eva",
    "password": "password", # enter PostgreSQL password here
    "host": "localhost",
    "port": "5432",
    "database": "evadb",
}
query = f"CREATE DATABASE IF NOT EXISTS pg WITH ENGINE = 'postgres', PARAMETERS = {params};"
#print(query)
print(cursor.query(query).df())

"""## **Download CSV from Kaggle Dataset**

Note: You may have to manually upload the CSV into the content folder. The first two lines were originally uncommented.
"""

"""
!mkdir -p content
!wget --header="Authorization: ApiKey 0ad0f3f3a77ada5f751f0bded1e68105" -nc -O /content/Loan_Default.csv https://www.kaggle.com/datasets/yasserh/loan-default-dataset/download/Loan_Default.csv

#!wget -nc -O /content/Loan_Default.csv https://www.kaggle.com/datasets/yasserh/loan-default-dataset/download/Loan_Default.csv
"""

"""# **Data Collection**

The following queries set up the table of data from the imported Kaggle dataset. An example query displays the first 15 rows of the table.
"""

cursor.query("""
  USE pg {
    CREATE TABLE IF NOT EXISTS loan_default (id VARCHAR(20), year VARCHAR(20), loan_limit VARCHAR(20),
    gender VARCHAR(20), approv_in_adv VARCHAR(10), loan_type VARCHAR(10), loan_purpose VARCHAR(10),
    credit_worthiness VARCHAR(10), open_credit VARCHAR(10), business_or_commercial VARCHAR(10),
    loan_amount FLOAT, rate_of_interest FLOAT, interest_rate_spread FLOAT, upfront_charges FLOAT, term FLOAT,
    neg_ammortization VARCHAR(10), interest_only VARCHAR(10), lump_sum_payment VARCHAR(10),
    property_value FLOAT, construction_type VARCHAR(10), occupancy_type VARCHAR(10), secured_by VARCHAR(10),
    total_units VARCHAR(10), income FLOAT, credit_type VARCHAR(10), credit_score INT,
    co_applicant_credit_type VARCHAR(10), age VARCHAR(10), submission_of_application VARCHAR(10), ltv FLOAT,
    region VARCHAR(10), security_type VARCHAR(15), status INTEGER, dtir1 FLOAT)
  }
""").df()

cursor.query("""
  USE pg {
    COPY loan_default (id, year, loan_limit,
    gender, approv_in_adv, loan_type, loan_purpose,
    credit_worthiness, open_credit, business_or_commercial,
    loan_amount, rate_of_interest, interest_rate_spread, upfront_charges, term,
    neg_ammortization, interest_only, lump_sum_payment,
    property_value, construction_type, occupancy_type, secured_by,
    total_units, income, credit_type, credit_score,
    co_applicant_credit_type, age, submission_of_application, ltv,
    region, security_type, status, dtir1)
    FROM '/content/Loan_Default.csv'
    DELIMITER ',' CSV HEADER
  }
""").df()

cursor.query("SELECT * FROM pg.loan_default LIMIT 15;").df()

"""# **ML Model**

First, we need to install a few extra packages from evadb, including ludwig.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --quiet "evadb[document, forecasting, ludwig]"

"""## **Create Training Function**"""

cursor.query("""CREATE OR REPLACE FUNCTION DefaultPredictor FROM
( SELECT * FROM pg.loan_default)
TYPE Ludwig
PREDICT 'status'
TIME_LIMIT 3600;
""").df()

"""## **Manually Entering Data**
This block enters data manually and adds tuples to the prediction table. If you want to upload multiple tuples to the prediction table, comment out the line to clear predictions from the table.
"""

cursor.query("""
  USE pg {
    CREATE TABLE IF NOT EXISTS home_loan_default_predictions (id VARCHAR(20), year VARCHAR(20), loan_limit VARCHAR(20),
    gender VARCHAR(20), approv_in_adv VARCHAR(10), loan_type VARCHAR(10), loan_purpose VARCHAR(10),
    credit_worthiness VARCHAR(10), open_credit VARCHAR(10), business_or_commercial VARCHAR(10),
    loan_amount FLOAT, rate_of_interest FLOAT, interest_rate_spread FLOAT, upfront_charges FLOAT, term FLOAT,
    neg_ammortization VARCHAR(10), interest_only VARCHAR(10), lump_sum_payment VARCHAR(10),
    property_value FLOAT, construction_type VARCHAR(10), occupancy_type VARCHAR(10), secured_by VARCHAR(10),
    total_units VARCHAR(10), income FLOAT, credit_type VARCHAR(10), credit_score INT,
    co_applicant_credit_type VARCHAR(10), age VARCHAR(10), submission_of_application VARCHAR(10), ltv FLOAT,
    region VARCHAR(10), security_type VARCHAR(15), status INTEGER, dtir1 FLOAT)
  }
""").df()

# Clears predictions table if not empty
#cursor.query("USE pg {DELETE FROM home_loan_default_predictions};").df()

# Clears predictions table if not empty
cursor.query("USE pg {DELETE FROM home_loan_default_predictions};").df()

cursor.query("""
  USE pg {
    INSERT INTO home_loan_default_predictions
    (id, year, loan_limit, gender, approv_in_adv, loan_type, loan_purpose,
     credit_worthiness, open_credit, business_or_commercial, loan_amount,
     rate_of_interest, interest_rate_spread, upfront_charges, term,
     neg_ammortization, interest_only, lump_sum_payment, property_value,
     construction_type, occupancy_type, secured_by, total_units, income,
     credit_type, credit_score, co_applicant_credit_type, age,
     submission_of_application, ltv, region, security_type, status, dtir1)
    VALUES (
      '173660', '2019', 'cf', 'Male', 'nopre', 'type2', 'P1', 'l1', 'nopc', 'b/c',
      '206500', NULL, NULL, NULL, '360', 'not_neg', 'not_int', 'lpsm', NULL, 'sb', 'pr',
      'home', '1U', '4980', 'EQUI', '552', 'EXP', '55-64', 'to_inst', NULL, 'North', 'direct', 0, NULL
    )
  }
""").df()

cursor.query("""
  USE pg {
    INSERT INTO home_loan_default_predictions
    (id, year, loan_limit, gender, approv_in_adv, loan_type, loan_purpose,
     credit_worthiness, open_credit, business_or_commercial, loan_amount,
     rate_of_interest, interest_rate_spread, upfront_charges, term,
     neg_ammortization, interest_only, lump_sum_payment, property_value,
     construction_type, occupancy_type, secured_by, total_units, income,
     credit_type, credit_score, co_applicant_credit_type, age,
     submission_of_application, ltv, region, security_type, status, dtir1)
    VALUES (
      '173661', '2019', 'cf', 'MALE', 'nopre', 'type1', 'P4', 'l1', 'nopc', 'nob/c',
      '526500', '3.99', '0.3849', '635.14', 360, 'not_neg', 'not_int', 'not_lpsm', '658000', 'sb', 'pr',
      'home', '1U', '11400', 'CRIF', '579', 'CIB', '<25', 'not_inst', '80.0152', 'south', 'direct', 0, '29'
    )
  }
""").df()

cursor.query("""
  USE pg {
    INSERT INTO home_loan_default_predictions
    (id, year, loan_limit, gender, approv_in_adv, loan_type, loan_purpose,
     credit_worthiness, open_credit, business_or_commercial, loan_amount,
     rate_of_interest, interest_rate_spread, upfront_charges, term,
     neg_ammortization, interest_only, lump_sum_payment, property_value,
     construction_type, occupancy_type, secured_by, total_units, income,
     credit_type, credit_score, co_applicant_credit_type, age,
     submission_of_application, ltv, region, security_type, status, dtir1)
    VALUES (
      '173661', '2019', 'cf', 'MALE', 'nopre', 'type1', 'P4', 'l1', 'nopc', 'nob/c',
      '526500', '3.99', '0.3849', '635.14', 360, 'not_neg', 'not_int', 'lpsm', '658000', 'sb', 'pr',
      'home', '1U', '11400', 'CRIF', '579', 'CIB', '<25', 'not_inst', '80.0152', 'south', 'direct', 0, '29'
    )
  }
""").df()

cursor.query("""
  USE pg {
    INSERT INTO home_loan_default_predictions
    (id, year, loan_limit, gender, approv_in_adv, loan_type, loan_purpose,
     credit_worthiness, open_credit, business_or_commercial, loan_amount,
     rate_of_interest, interest_rate_spread, upfront_charges, term,
     neg_ammortization, interest_only, lump_sum_payment, property_value,
     construction_type, occupancy_type, secured_by, total_units, income,
     credit_type, credit_score, co_applicant_credit_type, age,
     submission_of_application, ltv, region, security_type, status, dtir1)
    VALUES (
      '173661', '2019', 'cf', 'FEMALE', 'nopre', 'type1', 'P4', 'l1', 'nopc', 'nob/c',
      '526500', '3.99', '0.3849', '635.14', 360, 'not_neg', 'not_int', 'not_lpsm', '658000', 'sb', 'pr',
      'home', '1U', '11400', 'CRIF', '579', 'CIB', '<25', 'not_inst', '80.0152', 'south', 'direct', 0, '29'
    )
  }
""").df()

cursor.query("""SELECT * FROM pg.home_loan_default_predictions;""").df()

cursor.query("""SELECT DefaultPredictor(*) FROM pg.home_loan_default_predictions;""").df()

cursor.query("""
  SELECT status, status_predictions FROM pg.home_loan_default_predictions
  JOIN LATERAL DefaultPredictor(*) AS Predicted(status_predictions) LIMIT 15;
""").df()

"""## **Predicting The First 15 Columns Of The Table**

In this attempt to use the Ludwig model, we will predict the status for the first 15 columns of the table and then compare the results with the actual status from the table.


"""

cursor.query("SELECT DefaultPredictor(*) FROM pg.loan_default LIMIT 15;").df()

cursor.query("""
  SELECT status, status_predictions FROM pg.loan_default
  JOIN LATERAL DefaultPredictor(*) AS Predicted(status_predictions) LIMIT 15;
""").df()