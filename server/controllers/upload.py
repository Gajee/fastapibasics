
from typing import List

# from config.db import SessionLocal
# from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd    
import json as js

from functools import reduce
import operator
import pprint
import os

engine = create_engine('mysql+pymysql://root:active36@localhost:3306/test', echo=False)


class upload_files:

    def upload(thisdict, file):
        df1 = pd.read_csv(file.file)
        file_location = f"static/uploads/{file.filename}"
        df1.to_csv(file_location, index=False)
        
        df = pd.read_csv(file_location, nrows=1)
        
        temp = df.columns.tolist()
        res = js.dumps(temp)
        
        
        # for id in range(len(aa)):#df.values:
        #     # print(len(aa[id]))
        #     for i in range(len(aa[id])):
        #         header["color"] = "red"
        #         print(aa[id][i])
        #     print()
        
        return {
            "status" : True,
            "data" : res,
            "saved_at" : file_location
        }
    

    def cli_import(lists, filename, email, db):
        
        df = pd.read_csv(filename, usecols = lists)
        csv_val = df.values.tolist()
        
        aa = pd.read_csv(filename, usecols = [email])
        ids = aa.values.tolist()
        res = pd.read_sql("SELECT name,business_area,email_id,company_info FROM clients where email_id in %s" % repr(ids).replace('[','(').replace(']',')'), engine)
        result = res.values.tolist()
        
        first_set = set(map(tuple, csv_val))
        secnd_set = set(map(tuple, result))
        
        insert = first_set.symmetric_difference(secnd_set)
        
        duplicates = first_set.intersection(secnd_set)
        df = pd.DataFrame(list(insert),columns=lists)
        df.to_sql('clients', con=engine, index=False, if_exists = 'append')
        
        return {
            "status" : True,
            "duplicates" : duplicates,
            "inserted" : insert
        }
        

    


