from dotenv import load_dotenv
from process import *
import os
import datetime

def main():

    #Gets users from .env
    load_dotenv('.env')
    # employees_ = os.environ.get('EMPLOYEES')
    # employees_ = employees_.split(',')

    #Connect to EIP
    engine = eng_conn(os.environ['db_conn_str'],os.environ['usr'],os.environ['key'],os.environ['port'],os.environ['db_name'],os.environ['schema'])
    #Uses sql script to pull list of employee emails to be scraped on the outlook calender
    employees_ = engine.execute(pull_employees_script())
    employees_list = employees_.fetchall()
    #Formats it to list to be read by collect calender class
    formatted_employee_list = [row[0] for row in employees_list]
    

    #Gets raw calender data & converts to df
    calenders = CollectCalenders(employees=formatted_employee_list)
    calenders_dict = calenders.get_all_calenders()
    calenders_df = calenders.convert_calenders_to_df(calenders_dict)

    
    #pulls max date 
    result = engine.execute(pull_latest_date_script())
    latest_date = result.fetchone()
    latest_date_formatted = datetime.datetime.strptime(str(latest_date[0]), '%Y-%m-%d')
    #filters df according to the max date and pushes non duplicated rows
    df_filtered_by_date = calenders_df[(calenders_df['Date'] > latest_date_formatted.date())]
    push_df_to_db(df_filtered_by_date,os.environ['table_name'], engine, os.environ['schema'])


if __name__ == '__main__':
    main()

