import win32com.client, datetime
from datetime import date as date_function
from dateutil.parser import *
import calendar
import pandas as pd
import datetime

class CollectCalenders:

  def __init__(self,employees:list):
    self.employees = employees

    
  def  get_all_calenders(self):

   appt_dict = {}
   item = 0
   
   for i in self.employees:

    Outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = Outlook.GetNamespace("MAPI")

    recipient = namespace.createRecipient(i)
    resolved = recipient.Resolve()

    appts = namespace.GetSharedDefaultFolder(recipient,9).Items

  #Step 1 sort events by occurence and include recurring events
    appts.Sort("[Start]")
    appts.IncludeRecurrences = "True"

  #Step 2 filter to the range: from = (today - 10), to = (today)
    end = date_function.today().strftime('%Y-%m-%d') 
    begin = date_function.today() - datetime.timedelta(days=15)
    begin = begin.strftime('%Y-%m-%d')
    appts = appts.Restrict("[Start] >= '" +begin+ "' AND [END] <= '" +end+ "'")

  # Step 3 create list of excluded meeting subjects
    excluded_subjects=('<first excluded subject>')

  # Step 3 populate dictionary of meetings/appointments and return a dictionary of those meetings
          
    for indx, a in enumerate(appts):
      subject = str(a.Subject)
      if subject in (excluded_subjects):
        continue
      else:
        organizer = str(a.Organizer)
        meetingDate = str(a.Start)
        #date = parse(meetingDate).date()
        date = datetime.datetime.strptime(meetingDate, '%Y-%m-%d %H:%M:%S%z')
        subject = str(a.Subject) 
        duration = str(a.duration)
        start_time = str(a.start)
        end_time = str(a.end)
        format_start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S%z')
        format_end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S%z')
        appt_dict[item] = {"Employee":i,"Duration": duration, "Organizer": organizer, "Subject": subject, "Date": date.date(),"Start_Time": format_start_time.time(),"End_Time":format_end_time.time()}
        item = item + 1

   return appt_dict

  def  convert_calenders_to_df(self,appt_dict):
    """
    creates a dataframe from the calender data extracted from the dictionary

    """
    apt_df = pd.DataFrame.from_dict(appt_dict, orient='index', columns = ['Employee','Duration', 'Organizer', 'Subject', 'Date','Start_Time','End_Time'])


    return apt_df
