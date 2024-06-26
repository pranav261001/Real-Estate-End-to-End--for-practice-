import os
import sys

from src.exception import CustomException
from src.logger import logging

import pandas as pd
import pymysql
from sklearn.model_selection import train_test_split

from dataclasses import dataclass
from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation


@dataclass # directly define class variabele
class DataIngestionConfig:
    train_data_path: str= os.path.join('artifacts', 'train.csv')
    test_data_path: str= os.path.join('artifacts', 'test.csv')
    raw_data_path: str= os.path.join('artifacts', 'data.csv')

    
class DataIngestion(DataIngestionConfig):
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion")

        try:
            logging.info("Reading the data ")

            df_connection = pymysql.connect(host="localhost", user="root", password="Panu2610@sql", database="Project")
            df = pd.read_sql_query("SELECT * FROM real_estate", df_connection)

            os.makedirs(os.path.dirname(self.train_data_path), exist_ok=True) # creates folder 
            ''' os.path.dirname(self.train_data_path) returns 'artifacts'

                     os.makedirs('artifacts', exist_ok=True)'''
            
            df.to_csv(self.raw_data_path, index=False, header = True) # create file
            '''df.to_csv('artifacts/data.csv', index=False, header=True)'''

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.train_data_path, index=False, header = True)
            test_set.to_csv(self.test_data_path, index=False, header = True)

            logging.info("Train test split completed!")

            return(
                self.train_data_path,
                self.test_data_path)
        except Exception as e:
            raise CustomException(e, sys)
        

# TESTING 
if __name__ == '__main__':
    obj = DataIngestion()
    obj.initiate_data_ingestion()
    train_p, test_p = obj.initiate_data_ingestion()

    data_transformation_obj = DataTransformation()
    data_transformation_obj.initiate_transformation(train_p, test_p)
    
    


