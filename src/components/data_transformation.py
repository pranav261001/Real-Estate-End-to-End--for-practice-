import sys
import os 
from dataclasses import dataclass

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    data_transform_path = os.path.join('artifacts', 'data_transform.pkl')

class DataTransformation(DataTransformationConfig):

    def pipeline_tranformation(self):
        
        try:
            my_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )
            return  my_pipeline
        except Exception as e:
            raise CustomException
    
    def initiate_transformation(self, train_path, test_path):

        train_set = pd.read_csv(train_path)
        test_set = pd.read_csv(test_path)

        pipe_obj = self.pipeline_tranformation()

        target_column = 'MEDV'

        x_train = train_set.drop(columns=target_column, axis=1)
        y_train = train_set[target_column]

        x_test = test_set.drop(columns=target_column, axis=1)
        y_test = test_set[target_column]
        
        x_train_tr = pipe_obj.fit_transform(x_train)
        x_test_tr = pipe_obj.fit_transform(x_test)

        train_arr = np.c_[
            x_train_tr, np.array(y_train)
        ]
        test_arr = np.c_[
            x_test_tr, np.array(y_test)
        ]

        save_object(
            file_path = self.data_transform_path,
            obj = pipe_obj
        )

        return (
            train_arr,
            test_arr,
            self.data_transform_path
        )

        
    
        



