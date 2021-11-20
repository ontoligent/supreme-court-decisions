import pandas as pd
import numpy as np
import seaborn as sns 
import sqlalchemy as sqa
from sqlalchemy import exc
import re

sns.set()

class Db():
    
    tables = []
    db_file = ''
    
    def __init__(self, db_file):
        self.db_file = db_file.replace('./', '')
        self.dbconn = sqa.create_engine(f"sqlite:///{self.db_file}")
        
    def list_tables_in_db(self):
        return sqa.inspect(self.dbconn).get_table_names()
        
    def add_table(self, table_name, df, replace=True):
        if replace and table_name in self.tables:
            self.tables.remove(table_name)
        elif table_name in self.tables:
            print(f"{table_name} already exists.")
            return
        setattr(self, table_name, df)
        self.tables.append(table_name)

    def import_table(self, table_name, table_index=None):
        df = pd.read_sql(table_name, self.dbconn) 
        if table_index:
            df = df.set_index(table_index).sort_index()
        setattr(self, table_name, df)
        
    def save_table(self, table_name, if_exists='replace'):
        print("Saving " + table_name)
        df = getattr(self, table_name) 
        try:
            df.to_sql(table_name, self.dbconn, if_exists=if_exists, index=True)
        except exc.SQLAlchemyError as e:
            print(e)
    
    def save_all_tables(self, if_exists='replace'):
        for table_name in self.tables:
            self.save_table(table_name, if_exists)
            

class lmplot():
    
    x:str = ''
    y:str = ''
    order:int = 1
    aspect:float = 2.5
    context:str = 'talk'
    
    def __init__(self, df):
        self.df = df
        
    def set_x(self, x):
        self.x = x
        return self
        
    def set_y(self, y):
        self.y = y
        return self

    def set_order(self, order):
        self.order = order
        return self
    
    def plot(self):
        with sns.plotting_context(self.context):
            sns.lmplot(data=self.df, x=self.x, y=self.y, order=self.order, aspect=self.aspect)\
                .set(title=f"{self.x} vs {self.y} [order={self.order}]")