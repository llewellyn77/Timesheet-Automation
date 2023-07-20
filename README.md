# Timesheet-Automation
This uses the win32com.client library to access the shared calendars of employees within a company then extracts all their calendar information and uploads this into a postgres database, this also includes functionality to upload non duplicate values by using the sqlalchemy library to pull the max date of the information within the table 
