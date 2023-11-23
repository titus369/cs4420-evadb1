# Home Loan Default Predictor

## Introduction

In today’s society, one common way to afford homes and cars is by taking out a loan. An institution that accepts a loan from a customer takes some risk as it is possible that the customer cannot repay the loan. Given a list of factors related to the borrower, a machine learning model can help an institution know whether or not the borrower will be able to repay the loan. The goal of this project is to form a machine learning model that takes in a dataset of borrowers and outputs whether a user with certain factors will be able to repay the loan.

## Data Collection

### Project 1

The dataset used for this model is a [Kaggle dataset](https://www.kaggle.com/datasets/yasserh/loan-default-dataset). In Project 1, the data was originally set up in PostgreSQL manually in pgAdmin 4. Two tables, loan_default and loan_default_lite were created. The first table contained all 150,000 rows and 34 columns from the Kaggle CSV file. The second table consisted of only 5000 rows at random to create a more compact dataset.

To connect the PostgreSQL database with EvaDB, we originally used the following block fo code:
```
params = {
    "user": "postgres",
    "password": "", # enter PostgreSQL password here
    "host": "localhost",
    "port": "5432",
    "database": "Home Loan",
}
query = f"CREATE DATABASE IF NOT EXISTS pg WITH ENGINE = 'postgres', PARAMETERS = {params};"
#print(query)
#cursor.query(query).df()
print(cursor.query(query).df())
```

### Project 2

In Project 2, the data was set up in PostgreSQL through the following Jupyter notebook commands:
```
!sudo -u postgres psql -c "CREATE USER eva WITH SUPERUSER PASSWORD 'password'"
!sudo -u postgres psql -c "CREATE DATABASE evadb"

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
```

We then upload the CSV to the PostgreSQL database using the following queries in EvaDB:
```
cursor.query("""
  USE pg {
    CREATE TABLE IF NOT EXISTS loan_default (id VARCHAR(20), year INT, loan_limit VARCHAR(20),
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
```
