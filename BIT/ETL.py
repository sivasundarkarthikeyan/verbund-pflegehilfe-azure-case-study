import os
import uuid
import pandas as pd
import snowflake.connector
import snowflake.connector.errors as sce
from snowflake.connector.pandas_tools import write_pandas

class ETL:

    def __init__(self) -> None:
        """Constructor definition for ETL class
        """
        self.dataframe = None
        self.connection = None

    def transform_leads(self) -> pd.DataFrame:
        """Function which performs required transformations

        Returns:
            pd.DataFrame: Transformed data as a pandas dataframe
        """
        transformed_dataframe = None
        rows_to_insert = []
        for _, row in self.dataframe.iterrows():
            state = row['STATE']
            current_state = 0
            if current_state == 0 and current_state <= state:
                _id = str(uuid.uuid4()).upper()
                event_type = "LeadSold"
                event_employee = row['SOLD_EMPLOYEE']
                event_date = row['CREATED_DATE_UTC']
                lead_id = row['ID']
                updated_date_utc = row['UPDATED_DATE_UTC']
                rows_to_insert.append([_id, event_type, event_employee, event_date, lead_id, updated_date_utc])

            current_state += 1
            if current_state == 1 and current_state <= state:
                _id = str(uuid.uuid4()).upper()
                event_type = "LeadRequestedCancellation"
                event_employee = "Unknown"
                event_date = row['CANCELLATION_REQUEST_DATE_UTC']
                lead_id = row['ID']
                updated_date_utc = row['UPDATED_DATE_UTC']
                rows_to_insert.append([_id, event_type, event_employee, event_date, lead_id, updated_date_utc])
            
            current_state += 1
            if state >= current_state:
                if current_state == state:
                    _id = str(uuid.uuid4()).upper()
                    event_type = "LeadCancelled"
                    event_employee = row['CANCELED_EMPLOYEE']
                    event_date = row['CANCELLATION_DATE_UTC']
                    lead_id = row['ID']
                    updated_date_utc = row['UPDATED_DATE_UTC']
                    rows_to_insert.append([_id, event_type, event_employee, event_date, lead_id, updated_date_utc])
            
                current_state += 1
                if current_state == state:
                    _id = str(uuid.uuid4()).upper()
                    event_type = "LeadCancellationRejected"
                    event_employee = "Unknown"
                    event_date = row['CANCELLATION_REJECTION_DATE_UTC']
                    lead_id = row['ID']
                    updated_date_utc = row['UPDATED_DATE_UTC']
                    rows_to_insert.append([_id, event_type, event_employee, event_date, lead_id, updated_date_utc])

        transformed_dataframe = pd.DataFrame(rows_to_insert, columns = ['ID', 'EVENT_TYPE', 'EVENT_EMPLOYEE', 'EVENT_DATE', 'LEAD_ID', 'UPDATED_DATE_UTC'])
        return transformed_dataframe


    def connect_with_snowflake(self) -> None:
        """Function to establish the Snowflake DB connection
        """
        username = str(os.environ['SNOWFLAKE_USER']).strip()
        passkey = str(os.environ['SNOWFLAKE_PASS']).strip()
        account_id = str(os.environ['SNOWFLAKE_ID']).strip()
        database_name = str(os.environ['SNOWFLAKE_DB']).strip()
        warehouse_name = str(os.environ['SNOWFLAKE_WH']).strip()
        schema_name = str(os.environ['SNOWFLAKE_SH']).strip()
        try:
            self.connection = snowflake.connector.connect(user=username, password=passkey,
                        account = account_id, database = database_name,
                        warehouse = warehouse_name, schema = schema_name)
        except Exception as error:
            raise sce.DatabaseError("Could not establish connection with Snowflake", error)

    def extract_from_snowflake(self) -> None:
        """Function to extract the data to be transformed from Snowflake table
        """
        con_cursor = self.connection.cursor()
        try:
            table_name = str(os.environ['SOURCE_TABLE_NAME']).strip()
            con_cursor.execute(f"SELECT * from {table_name}")
            self.dataframe = con_cursor.fetch_pandas_all()
        except Exception as error:
            self.connection.rollback()
            raise sce.DatabaseError("Error in transaction, reverting all changes using rollback ") from error        
        finally:
            con_cursor.close()
        
    def transform_and_load_into_snowflake(self) -> None:
        """Function to load the transformed data into a Snowflake table
        """
        try:
            table_name = str(os.environ['DESTINATION_TABLE_NAME']).strip()
            transformed_company_leads_df = self.transform_leads()
            write_pandas(self.connection, transformed_company_leads_df, table_name)
        except Exception as error:
            self.connection.rollback()
            raise sce.DatabaseError("Error in transaction, reverting all changes using rollback ") from error
        finally:
            self.connection.close()

    def run(self) -> None:
        """Funtion that consolidates the entire process and 
        runs them sequentially
        """
        self.connect_with_snowflake()
        print("Established connection with Snowflake")
        self.extract_from_snowflake()
        print("Extracted data from Snowflake")
        self.transform_and_load_into_snowflake()
        print("Transformed the data and then loaded into Snowflake")
