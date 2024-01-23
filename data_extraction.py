import tabula
import requests
import pandas as pd
from database_utils import DatabaseConnector
from sqlalchemy import inspect
import json
import numpy as np
import boto3
from io import StringIO

headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
num_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
retrieve_store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
s3_url = "s3://data-handling-public/products.csv"
s3_bucket = "data-handling-public"
s3_object_key = "products.csv"


class DataExtractor:
      
    def __init__(self) -> None:
        pass

    def list_db_tables(self, engine):

        inspector = inspect(engine)
        self.table_list = inspector.get_table_names()
        print(self.table_list)
        # for column in inspector.get_columns(self.table_list):
        #     print("Column: %s" % column['name'])
        return self.table_list

    def read_rds_table(self, engine, table_name: pd.DataFrame):

        con = engine
        db_tables = self.list_db_tables(engine)
        if table_name in db_tables:
            pd_users = pd.read_sql_table(table_name, con=con)
            return pd_users
        else:
            print('Invalid Table')

    def retrieve_pdf_data(self, filepath: str):
        
        cc_df = tabula.read_pdf(filepath, stream=False, pages='all')
        cc_df = pd.concat(cc_df)
        print("PDF converted to pandas dataframe")
        return cc_df

    def list_number_of_stores(self, endpoint: str, headers: dict):
        num_stores_endpoint = endpoint
        num_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
        api = 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'
        true_header = {'x-api-key': api}
        response = requests.get(num_stores_endpoint, headers=true_header)
        print(f"Status Code: {response.status_code}")
        stores_list = response.json()
        return stores_list['number_stores']
    
    def retrieve_stores_data(self, endpoint: str, headers: dict):

       curr_stores = []
       no_of_stores = self.list_number_of_stores(endpoint='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', headers={'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'})
       retrieve_store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
       for store in range(0, no_of_stores):
            response = requests.get(f"{'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'}{store}", headers={'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}).json()
            curr_stores.append(pd.DataFrame(response,index=[np.NaN]))
       curr_stores_df = pd.concat(curr_stores)
       print(f'stores loaded into dataframe with {len(curr_stores_df)} rows :')
       return curr_stores_df
    
    def extract_from_s3(self, bucket: str, file_from_s3: str):

        s3 = boto3.client('s3')
        s3_object = s3.get_object(Bucket=bucket, Key=file_from_s3)
        s3_data = s3_object['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(s3_data))
        print('S3 file Downloaded')
        print(df)
        return df
    
    def extract_from_s3_json(self, bucket: str, file_from_s3: str):
     
        s3 = boto3.client('s3')
        s3_object = s3.get_object(Bucket=bucket, Key=file_from_s3)
        s3_data = s3_object['Body'].read().decode('utf-8')
        df = pd.read_json(StringIO(s3_data))
        print(df.head())
        print('S3 file Downloaded')
        return df

if __name__ == '__main__':
    db = DatabaseConnector('db_creds.yaml')
    de = DataExtractor()
    table_list = de.list_db_tables(engine=db.engine)
    print(table_list)
