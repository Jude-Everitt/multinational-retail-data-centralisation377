import yaml
import pandas as pd
from sqlalchemy import create_engine


# The `DatabaseConnector` class initializes a database connection using provided credentials.
# The `DatabaseConnector` class is a Python class that connects to a database using credentials from a
# YAML file and provides methods to read the credentials, initialize the database engine, and upload a
# cleaned dataframe to the database.
class DatabaseConnector:
    def __init__(self, yaml_file):
        """
        The function initializes the class instance with a YAML file, an empty dictionary, and a database
        engine.
        
        :param yaml_file: The `yaml_file` parameter is a string that represents the path or name of a
        YAML file
        """
        self.yaml_file = yaml_file
        #self.creds_dict = {}
        #self.engine = self.init_db_engine()
        

    def read_db_creds(self):
        """
        The function reads a YAML file containing database credentials and returns them as a dictionary.
        :return: the `creds_dict` variable, which is a dictionary containing the credentials read from
        the YAML file.
        """

        with open(self.yaml_file, 'r') as file:
            creds_dict = yaml.safe_load(file)
        return creds_dict

    def init_db_engine(self, database_type="postgresql", dbapi="psycopg2"):
        """
        The function initializes a database engine using the specified database type and DBAPI, and
        connects to the database using the provided credentials.
        
        :param database_type: The database type, such as "postgresql" or "mysql", defaults to postgresql
        (optional)
        :param dbapi: The `dbapi` parameter is the Python Database API (DBAPI) module that will be used
        to connect to the database. In this case, the `psycopg2` module is being used, which is a DBAPI
        for connecting to PostgreSQL databases, defaults to psycopg2 (optional)
        :return: the database engine object.
        """
        creds_dict = self.read_db_creds()
        engine = create_engine(f"{database_type}+{dbapi}://{creds_dict['USER']}:{creds_dict['PASSWORD']}@{creds_dict['HOST']}:{creds_dict['PORT']}/{creds_dict['DATABASE']}")
        engine = engine.connect()
        print('Database connected')
        return engine

    def upload_to_db(self, cleaned_dataframe: pd.DataFrame, table_name: str, connection):
        """
        The function uploads a cleaned dataframe to a PostgreSQL database table.
        
        :param cleaned_dataframe: The cleaned_dataframe parameter is a pandas DataFrame that contains
        the data you want to upload to the database
        :type cleaned_dataframe: pd.DataFrame
        :param table_name: The table name is a string that specifies the name of the table in the
        database where the cleaned dataframe will be uploaded
        :type table_name: str
        :param connection: The "connection" parameter is the connection object that is used to connect
        to the PostgreSQL database. It is typically created using the psycopg2 library, like this:
        """

        print('almost there')
        cleaned_dataframe.to_sql(table_name, con=connection, if_exists='replace')
        print('cleaned dataframe uploaded to postgreSQL')


if __name__ == '__main__':
 db = DatabaseConnector("db_creds.yaml")
   
    