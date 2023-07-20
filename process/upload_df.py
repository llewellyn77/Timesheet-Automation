from sqlalchemy import create_engine, true
import time
from sqlalchemy import exc


def eng_conn (db_conn_str,usr,key,port,db_name,schema):
        engine = create_engine('postgresql://'+usr+':'+key+db_conn_str+':'+port+'/'+db_name)
        engine.execute('SET search_path TO '+schema)
    
        return engine


def push_df_to_db(df,table_name,engine,schema_,dataTypes=None):
        print(f"{table_name}    |  { schema_}")
        start_time = time.time()
        try:
            print("Pushing df....")
            df.to_sql(table_name, con = engine,schema=schema_,dtype=dataTypes,if_exists='append',index=False)
            print(f"table successfully created   !! {time.time() - start_time }")
        except Exception as e:
            print(f" SQL error : {e}")
            pass


# def append_non_duplicates_to_eip(df,table_name,engine,schema):
#     num_rows = len(df)
#     print(f"{table_name}    |  { schema}")
#     for i in range(num_rows):
        
#      try:
#         #Try inserting the row
#         df.iloc[i:i+1].to_sql(table_name,con = engine,schema=schema,if_exists = 'append',index=False)
#      except exc.IntegrityError:
#         #Ignore duplicates
#         pass

def pull_latest_date_script():
    #based on the table youre uploading to thats where your from statement will point to, to pull the max date so the dataframe can be filtered to the max date
    script = '''

    SELECT 
	
	MAX("Date")
	
    FROM TIMESHEET_AUTOMATION.TIMESHEET_AUTOMATION_RAW_DATA;

    '''

    return script


def pull_employees_script():

    script = '''

    SELECT "Employee Email"
    FROM TIMESHEET_AUTOMATION.EMPLOYEE_LIST;

    '''

    return script


