# 6 pipes lines, each pipeline will look like a function with a bunch of method calls from other python files
# user data create instancee of connector class and feed dbcredsyaml file the create instanc of cleaning class then extractor class
#first user data pipeline, when extract data from RDS us db_creds, push to postgres use pgadmin4_creds


from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning



if __name__ == '__main__':
 
 db_local = DatabaseConnector('pgadmin4_connection_creds.yaml')
 local_engine = db_local.init_db_engine()
 
 def orders_run():
      
       db2 = DatabaseConnector('db_creds.yaml')
       de2 = DataExtractor()
       table_list = de2.list_db_tables(engine=db2.engine)
       orders_raw = de2.read_rds_table(engine=db2.engine, table_name=table_list[2])
       orders_cleaned_init = DataCleaning(orders_table=orders_raw)
       cleaned_orders = orders_cleaned_init.clean_orders_table()
       db2.upload_to_db(cleaned_dataframe=cleaned_orders, table_name='orders_table', connection=local_engine)
 
 print("starting orders run")
 orders_run()
 print("finished orders run")

 db = DatabaseConnector('db_creds.yaml')
 de = DataExtractor()
 eng = db.init_db_engine()
 db_local = DatabaseConnector('pgadmin4_connection_creds.yaml')
 local_engine = db_local.init_db_engine()
 pdf_file = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
 headers = {'x-api-key': 'ayFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMXi_key'}
 num_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
 retrieve_store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
 s3_url = "s3://data-handling-public/products.csv"
 s3_bucket = "data-handling-public"
 s3_object_key = "products.csv"
 s3_json_url = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
 s3_json_bucket = "data-handling-public"
 s3_json_object_key = "date_details.json"   
 
 def users_run():

       table_list = de.list_db_tables(engine=eng)
       users_raw = de.read_rds_table(engine=eng, table_name=table_list[1])
       user_clean_init = DataCleaning(users_table=users_raw)
       cleaned_res = user_clean_init.clean_user_data()
       print(cleaned_res.head())
       db.upload_to_db(cleaned_dataframe=cleaned_res, table_name='dim_users', connection=local_engine)

 print("starting users run")
 users_run()
 print("finished users run")

 def cards_run():
   
      card_raw = de.retrieve_pdf_data(filepath=pdf_file)
      card_cleaned_init = DataCleaning(cards_table=card_raw)
      cleaned_cards = card_cleaned_init.clean_card_data()
      print("cards data cleaned")
      db.upload_to_db(cleaned_dataframe=cleaned_cards, table_name='dim_card_details', connection=local_engine)
      print("cards data uploaded to pgadmin4")
    
 print("starting cards run")
 cards_run()
 print("finished cards run")

 def stores_run():

     stores_raw = de.retrieve_stores_data(endpoint=retrieve_store_endpoint, headers=headers)
     stores_clean_init = DataCleaning(stores_table=stores_raw)
     cleaned_stores = stores_clean_init.clean_store_data()
     db.upload_to_db(cleaned_dataframe=cleaned_stores, table_name='dim_store_details', connection=local_engine)

 print("starting stores run")
 stores_run()
 print("finished stores run")

 def products_run():
  
    products_raw = de.extract_from_s3(bucket=s3_bucket, file_from_s3=s3_object_key)
    product_clean_init = DataCleaning(products_table=products_raw)
    cleaned_products = product_clean_init.convert_product_weights()
    db.upload_to_db(cleaned_dataframe=cleaned_products, table_name='dim_products', connection=local_engine)
    
 print("starting products run")
 products_run()
 print("finished products run")

 def datetime_run():
      
    datetime_raw = de.extract_from_s3_json(bucket=s3_json_bucket, file_from_s3=s3_json_object_key)
    datetime_clean_init = DataCleaning(datetimes_table=datetime_raw)
    cleaned_datetime = datetime_clean_init.clean_datetime_table()
    db.upload_to_db(cleaned_dataframe=cleaned_datetime, table_name='dim_date_times', connection=local_engine)
    
 print("starting datetime run")
 datetime_run()
 print("finished datetime run")

 print('All Cleaning Done') 

