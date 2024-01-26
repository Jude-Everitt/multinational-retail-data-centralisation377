# Multinational Retail Data Centralisation
The MRDC project is a project where a company's sales data is spread across different data sources and each data source is extracted, cleaned and stored in a database I created for easier and more accesable analysis. 

## Table Of Contents

1. Project Description
2. Instilation Instructions
3. Usage Instructions
4. File Structure
5. License Information

## Project Description
### Database Utils

Within Database Utils a DatabaseConnector class is created. The historical data of users is currently stored in an AWS RDS database in the cloud. Within the class there are three methods. 
-"read_db_creds" reads the inputted database credentials from a yaml file and returns a dictionary.
-"init_db_engine" The function initializes a database engine using the specified database type and DBAPI, and connects to the database using the provided credentials. 
-"upload_to_db" uploads a cleaned dataframe to a PostgreSQL database table. 

### Database Extractor

Databasee Extraction contains a class called DatabaseExtractor which consists of methods each used to extract data from different data sources. 

-"read_api_creds" is a method which reads the credentials off of a yaml file and returns it a dictionary which is to be used in further methods. 
-"list_db_tables" retrieves a list of table names from a data sqlalchemy engine. The engine parameter is an instance of a database which is used to connect to the database and perrform operations on it. Returning a list of table names in the database. 
-"read_rds_table" reads and conevrts a table to a pandas dataframe object from a provided tablename and engine. 
-"retrieve_pdf_data" retrieves data from a PDF file and converts it into a pandas dataframe. The filepath/url parameter is a string that represents the file path of the PDF file that you want to retrieve data from. 
-"list_number_of_stores" function retrieves the number of stores from a specified endpoint using an API key and returns the number of stores. The endpoint parameter is a string that represents the URL of the API endpoint you want to make a request to. The headers parameter is a dictionary (created from "read_api_creds") that contains the headers to be included in the HTTP request. The function returns the number of stores from the response JSON. 
-"retrieve_stroes_data" returns a pandas DataFrame containing the store details retrieved from the specified endpoint and api key. 
-"extract_from_s3" extracts data from a csv file stored in an S3 bucket and returns it as a pandas DataFrame. The bucket parameter is the name of the S3 bucket from which you want to extract the file. It is a string that represents the name of the bucket. The file_from_s3 parameter is the name or key of the file that you want to extract from the S3 bucket. It is the specific file that you want to download and read as a pandas DataFrame. 
-"extract_from_s3_json" function extracts data from a JSON file stored in an S3 bucket and returns it as a pandas DataFrame. It contains the same parameters as the csv extraaction. 

### Data Cleaning

The Data Cleaning file contains a class called DataCleaning and is used for cleaning and preprocessing data. 

The DataCleaning class also contains statistic methods which are methods within a class that have no access to anything else in the class. They cannot change or look at any object attributes or call other methods within the class.
- "datatime_transform" takes a list of column names and a DataFrame, and converts the values in those columns to datetime format.
- "month_year_transform" converts columns in a DataFrame to datetime format using the specified format.
- "column_value_set" takes a column name and a DataFrame as input, and prints the unique values in that column.
- "kg_cov" removes the "kg" suffix from a given string if it exists.
- "grams_and_ml" converts a value from grams to kilograms or from milliliters to liters.
- "multiply_values" The function takes a string value, checks if it contains 'x', replaces ' x ' with a space, splits the string into two numbers, multiplies them, and returns the result divided by 1000.
- "oz_conversion" converts a value from ounces to grams.

Each method within the DataCleaning class is created to clean its corresponding data extracted froma  specific pipeline called within the "main.py" file. Each method is specific to clean the provided dataframe.
- "clean_orders_table" removes specific columns from the orders table and returns the cleaned table.
- "clean_user_data" cleans and processes user data by removing duplicates, formatting phone numbers, replacing country codes, filtering by country codes, filtering by user UUID length, and dropping null values.
- "clean_card_data" cleans and transforms the data in the `cards_table` by removing duplicates, null values, and non-numeric card numbers, and converting date columns to the correct datetime format.
- "clean_store_data" cleans the store dataframe by removing unnecessary columns, setting a new index, dropping duplicates, filtering by specific country codes, removing newline characters in the address column, removing letters from the staff_numbers column, converting datetime values, correcting misspelled continents, and setting column value sets.
- "convert_product_weights" cleans and converts the weights of products in a table.
- "clean_datetime_table" cleans a datetime table by removing rows where the 'month' column is not a digit, dropping any rows with missing values, and removing duplicate rows.

### Main

The main script contains different functions each used to access each pipeline of source data extract and convert to a pandas dataframe, clean the data then upload each dataframe to a local database. Each method used to upload thee clean eextracteed data is described belowe. 

#### orders_run 
- The orders_run is used to specify the table or data structure that stores information about orders. This could include details such as order ID, customer ID, product ID, quantity, price, and any other relevant information related to orders.

#### users_run
- A table or data structure that stores information about users. It could be a database table, a list, a dictionary, or any other data structure that allows storing and retrieving user information.
#### cards_run 
- The cards_run is used to store information about credit cards or payment methods associated with users. It could include fields such as card number, cardholder name, expiration date, and billing address.
#### stores_run 
- The stores_run is used to specify the table or data structure that stores information about stores. This could include details such as store names, addresses, contact information, and any other relevant information about the stores.
#### products_run 
- The products_run is used to specify the table or data structure that stores information about products. This table typically contains details such as product names, descriptions, prices, and other relevant information.

#### datetimes_run 
- The datetimes_run is used to specify the table or data structure that stores datetime information. It could be a database table, a list, a dictionary, or any other data structure that can store datetime values. This parameter allows you to pass an existing table or create a new one specifically. 

## Instilation Instructions

To run this code:
- Clone repository
  1. Go to GitHub.com and navigate to the main page of the repository.
  2. Click <>code.
  3. Copy the URL for the repository.
  4. Open terminal
  5. Change the current working directory to the location where you want the cloned directory.
  6. Type: git clone pasted_URL_here
  7. Press Enter to create local clone.
- Open file within on VSCode within repository
- When making changes and updating them
  1. git add .
  2. git commit -m "comment"
  3. git push
     This updates any changes to the code to the Git repository, where changes can be tracked.

## Usage Instructions

## File Structure 

## License Infornation

MIT License

Copyright (c) 2023 Jude Everitt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "hangman milestones"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
