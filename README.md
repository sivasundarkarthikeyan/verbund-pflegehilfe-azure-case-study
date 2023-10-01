# Verbung-Pflegehilfe-Azure-Case-Study
Project containing the Azure Data Factory pipeline codes along with Python code for ETL process and SQL queries related to MySQL and Snowflake.

## SQL Queries
Folder `SQL_Queries` contains the DDL and DML queries for `MySQL` and `Snowflake` correspondingly.

## Data for ETL
Folder `Formatted_Data` contains the data in `csv` format. The original data format `xlsx` requires conversion to `csv` format in order to import it in `MySQL`.

## Python Code for ETL
Folder `BIT` contains the python solution which fetches data from Snowflake table `CompanyLeads`, performs necessary transformation and loads it into the Snowflake table `LeadEvents`.

### Prerequisites for Python code
Install the requirements.txt file using the below command to get the required libraries.

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

Change to the Python Code directory and then run the below command to export the required environment variables required for Snowflake connection from the file `snowflake.env`:

```bash
source set_env.sh
```

Run the python code using the command below

```bash
python main.py
```

## Pipeline codes
Folder other than `SQL_Queries` and `BIT` corresponds to the` Azure Data Factory Pipeline`.
