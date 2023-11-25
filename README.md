# Home Loan Default Predictor

## Introduction

In today’s society, one common way to afford homes and cars is by taking out a loan. An institution that accepts a loan from a customer takes some risk as it is possible that the customer cannot repay the loan. Given a list of factors related to the borrower, a machine learning model can help an institution know whether or not the borrower will be able to repay the loan. The purpose of this project is to take in a set of data and predict whether a user will or will not be able to repay their loan given a specific set of factors. We will use PostgreSQL to collect the home loan default dataset and connect the PostgreSQL database with EvaDB. We will then import EvaDB's Ludwig to create a machine learning prediction model.

The inspiration for this project came from [Ibrahim Ogunbiyi's HashNode blog](https://folksconnect.hashnode.dev/predicting-loan-default-using-mindsdb-postgresql-and-streamlit) which utilized MindsDB to accomplish a similar goal of providing a machine learning prediction model to predict whether a borrower can repay their loan. MindsDB and EvaDB are both systems that provide a SQL interface to accomplish AI tasks from within the database system. MindsDB offers a richer set of integrations, but EvaDB should offer higher performance and GPU utilization.

## Setup

This project is run in a Jupyter notebook. To set up this program, PostgreSQL and EvaDB need to be set up along with a few other packages necessary to get the commands to work. First, to get PostgreSQL set up, we will run the following commands:

```
!apt -qq install postgresql
!service postgresql start
```

Next, we will install various dependencies along before downloading EvaDB. This project uses EvaDB 0.3.9 which requires Python 3.9 or later. However, EvaDB's Ludwig requires a version of Numpy that is not compatible for Python 3.11 or later. Therefore, in this project Python 3.10 is used. Check the Requirements.txt file for specific versions used in this project. Run the following to install EvaDB:

```
%pip install fastapi
%pip install kaleido
%pip install python-multipart
%pip install jedi
%pip install uvicorn
%pip install --upgrade pip setuptools wheel
%pip install --upgrade evadb

%pip install psycopg2
```

## Data Collection

The dataset used for this model is a [Kaggle dataset](https://www.kaggle.com/datasets/yasserh/loan-default-dataset). The dataset is a CSV with 150,000 rows and 34 columns. The columns will be used to help predict whether or not a user will be able to repay a loan, which is defined by the Status column.

* ID: Unique identifier for each loan application.
* Year: The year in which the loan was applied for.
* Loan_limit: The maximum amount of money that the borrower can borrow.
* Gender: The gender of the borrower.
* Approv_in_adv: Whether the loan was approved in advance or not.
* Loan_type: The type of loan applied for (e.g. personal loan, business loan, etc.).
* Loan_purpose: The purpose for which the loan is being taken (e.g. home purchase, debt consolidation, etc.).
* Credit_Worthiness: A measure of the borrower's creditworthiness, based on their credit history and other factors.
* Open_credit: The number of open lines of credit the borrower has.
* Business_or_commercial: Indicates whether the loan is for a business or commercial purpose.
* Loan_amount: The amount of money borrowed.
* Rate_of_interest: The annual interest rate charged on the loan.
* Interest_rate_spread: The difference between the interest rate charged on the loan and a benchmark rate.
* Upfront_charges: Any upfront charges or fees associated with the loan.
* Term: The length of time the borrower has to repay the loan.
* Neg_amortization: Whether the loan has negative amortization, meaning the borrower's monthly payments are not enough to cover the interest owed, resulting in the loan balance increasing over time.
* Interest_only: Whether the borrower is only required to pay the interest on the loan for a certain period of time before starting to pay down the principal.
* Lump_sum_payment: Whether the borrower can make a lump sum payment to pay off the loan early.
* Property_value: The value of the property being purchased or used as collateral for the loan.
* Construction_type: The type of construction being financed by the loan (e.g. new construction, renovation, etc.).
* Occupancy_type: The occupancy status of the property being financed (e.g. owner-occupied, non-owner-occupied, etc.).
* Secured_by: What collateral, if any, is securing the loan.
* Total_units: The total number of units in a multi-unit property being financed.
* Income: The borrower's income.
* Credit_type: The type of credit used by the borrower (e.g. revolving credit, installment credit, etc.).
* Credit_Score: The borrower's credit score.
* Co_applicant_credit_type: The type of credit used by the borrower's co-applicant (if applicable).
* Age: The age of the borrower.
* Submission_of_application: How the borrower applied for the loan (e.g. online, in-person, etc.).
* LTV: The loan-to-value ratio, which is the ratio of the loan amount to the value of the property being financed.
* Region: The region where the property being financed is located.
* Security_Type: The type of security being used to secure the loan.
* Status: Whether the loan is in default or not.
* DTIR1: The borrower's debt-to-income ratio, which is the ratio of the borrower's total debt payments to their income.

### Project 1

In Project 1, the data was originally set up in PostgreSQL manually in pgAdmin 4. Two tables, loan_default and loan_default_lite were created. The first table contained all 150,000 rows and 34 columns from the Kaggle CSV file. The second table consisted of only 5000 rows at random to create a more compact dataset.

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

In Project 2, the data was set up in PostgreSQL using a Jupyter notebook:
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

## Training Our ML Model

The tool that we will use to train the model is EvaDB's Ludwig. We will need to download this extra EvaDB dependency, which we have done as shown below:

```
%pip install --quiet "evadb[document, forecasting, ludwig]"
```

We then create a Prediction function using Ludwig and have the training model run for an hour, or 3600 seconds. This is done using the code below:

```
cursor.query("""CREATE OR REPLACE FUNCTION DefaultPredictor FROM
( SELECT * FROM pg.loan_default)
TYPE Ludwig
PREDICT 'status'
TIME_LIMIT 3600;
""").df()
```

## Results and Analysis

To use this model, we run a few extra queries. The first way that we can do this is by running the model directly on the loan_default table we created during data processing. Using the below command, we can run the prediction function on the first 15 rows of the loan_default table:
```
cursor.query("SELECT DefaultPredictor(*) FROM pg.loan_default LIMIT 15;").df()
```

```
status_predictions
0	True
1	True
2	True
3	True
4	True
5	True
6	True
7	True
8	True
9	True
10	True
11	True
12	True
13	False
14	False
```

We can then compare these True/False values for the predicted status with the actual status found on the table using the following query:
```
cursor.query("""
  SELECT status, status_predictions FROM pg.loan_default
  JOIN LATERAL DefaultPredictor(*) AS Predicted(status_predictions) LIMIT 15;
""").df()
```

```
	status	status_predictions
0	1	True
1	1	True
2	0	False
3	0	False
4	0	False
5	0	False
6	0	False
7	0	False
8	1	True
9	1	True
10	0	False
11	0	False
12	0	False
13	0	False
14	0	False
```

The second way of using this prediction function is to have a user manually enter in a set of data into a new table by adjusting the following query:

```
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
```

Note that when adjusting these queries, the status field should be set to 0 and not to NULL to allow for the prediction function to work. For example, the table created from the following queries will result in the predicted status shown below the table:

```
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
```

```
	status_predictions
0	True
1	False
2	False
3	False
```

## References

* Kakkar, Gaurav T. (2023, August 13). MindsDB vs. Evadb. Evadb Blog. Retrieved from https://medium.com/evadb-blog/mindsdb-vs-evadb-9005c7a9ffd1
* Ogunbiyi, Ibrahim. (2023, April 28). Predicting Loan Default Using MindsDB, PostgreSQL, and Streamlit. FolksConnect. Retrieved from https://folksconnect.hashnode.dev/predicting-loan-default-using-mindsdb-postgresql-and-streamlit
* Yasser H. (2021). Loan Default Dataset. Kaggle. https://www.kaggle.com/datasets/yasserh/loan-default-dataset
* Evadb Documentation. (2023). Evadb. https://evadb.readthedocs.io/en/stable/source/overview/getting-started.html
* Evadb Documentation. (2023). Classification Use Case - Homerental Predict. Evadb. https://evadb.readthedocs.io/en/stable/source/usecases/classification.html#homerental-predict
* Evadb Documentation. (2023). Model Training with Ludwig. Evadb. https://evadb.readthedocs.io/en/stable/source/reference/ai/model-train-ludwig.html#ludwig
