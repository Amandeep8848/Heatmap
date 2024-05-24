# Copyright (c) 2024, Amandeep and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date, timedelta

class FrappeEmployeeAttendanceHeatmap(Document):
    @frappe.whitelist()
    def get_dates_of_entire_year(self, employee):
        # Calculate first and last day of the year
        first_day_of_year = date(date.today().year, 1, 1)
        last_day_of_year = date(date.today().year, 12, 31)
        
        # Initialize all_dates dictionary
        all_dates = {}
        
        # Call the function to add dates in dictionary and other necessary functions
        add_dates_in_dictionary(all_dates, first_day_of_year, last_day_of_year)
        setAttendence_data(all_dates, employee)
        set_joining_dates(all_dates, employee)
        
        return all_dates


def set_leaves_data(all_dates, employee_leaves):
   for leave in employee_leaves:
       leave_from = leave.leave_from
       if leave.leave_from < leave.to:           
           while True:
               if leave_from > leave.to:
                   break
               else:
                   all_dates[leave_from.strftime('%Y-%m-%d')] = 0.25
                   leave_from = leave_from + timedelta(days=1)
       else:
           all_dates[leave_from.strftime('%Y-%m-%d')] = 0.25

def add_dates_in_dictionary(all_dates, first_day_of_year, last_day_of_year):
   while True:
       all_dates[first_day_of_year.strftime('%Y-%m-%d')] = 0
       if first_day_of_year < last_day_of_year:
           first_day_of_year = first_day_of_year + timedelta(days=1)
       else:
           break

def setAttendence_data(all_dates, employee):
   employee_present_status = frappe.get_list("Employee Attendance",
                                             fields = ["employee","present","date"],
                                             filters={
                                               "employee": employee
                                           })
   for attendance in employee_present_status:
    #    if int(attendance.half_day) == 1:
    #        all_dates[str(attendance.date)] = 0.75
    #    else:
        all_dates[str(attendance.date)] = 1

def set_joining_dates(all_dates, employee):
   employee_joining_date = frappe.get_doc("Employee Details", {"name": employee}, "joining_date")
   for mydate in all_dates:
       if datetime.strptime(mydate, "%Y-%m-%d").date() < employee_joining_date.joining_date:
           all_dates[mydate] = 0.5
