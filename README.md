# Timesheet-Automation
This is an ETL process which extracts data from a shared outlook calender using the win32com.client library, this then consolidates this data into a dictionary which is then converted to a data frame using pandas, this data is then transformed such that non duplicates are uploaded by using the sqlalchemy library by pulling a max date from the table being uploaded to, only records past the max date will be uploaded hence avoiding duplicates. This data frame is then uploaded to a postgres database using the sqlalchemy library as well. 


