import yaml
import pandas as pd
from sqlalchemy import create_engine


# The `DatabaseConnector` class initializes a database connection using provided credentials.
class DatabaseConnector:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.creds_dict = {}
        self.engine = self.init_db_engine()
        

    def read_db_creds(self):

        with open(self.yaml_file, 'r') as file:
            self.creds_dict = yaml.safe_load(file)
        print(self.creds_dict)
        return self.creds_dict

    def init_db_engine(self, database_type="postgresql", dbapi="psycopg2"):

        print(self.read_db_creds())
        self.engine = create_engine(f"{database_type}+{dbapi}://{self.creds_dict['USER']}:{self.creds_dict['PASSWORD']}@{self.creds_dict['HOST']}:{self.creds_dict['PORT']}/{self.creds_dict['DATABASE']}")
        self.engine = self.engine.connect()
        print('Database connected')
        return self.engine

    def upload_to_db(self, cleaned_dataframe: pd.DataFrame, table_name: str, connection):

        print('almost there')
        cleaned_dataframe.to_sql(table_name, con=connection, if_exists='replace')
        print('cleaned dataframe uploaded to postgreSQL')


if __name__ == '__main__':
    db = DatabaseConnector('db_creds.yaml')
   
    