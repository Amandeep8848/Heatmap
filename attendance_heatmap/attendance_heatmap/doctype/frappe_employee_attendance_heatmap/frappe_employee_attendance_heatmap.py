# Copyright (c) 2024, Amandeep and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date, timedelta
from frappe.utils import flt,today

class FrappeEmployeeAttendanceHeatmap(Document):
    @frappe.whitelist()
    def get_dates_of_entire_year(self, employee):
        first_day_of_year = date(date.today().year, 1, 1)
        last_day_of_year = date(date.today().year, 12, 31)
        all_dates = {}
        
        add_dates_in_dictionary(all_dates, first_day_of_year, last_day_of_year)
        setAttendence_data(all_dates, employee)
        set_joining_dates(all_dates, employee)
        set_leaves_dates(all_dates, employee)
        
        return all_dates


def set_leaves_dates(all_dates, employee):
    leave_dates =  frappe.db.get_list("Leave Request",fields = ["from_date","to_date","name"])
    for leave in leave_dates:
        if leave['from_date']  != leave['to_date']:
            while True:
                if leave['from_date'] > leave['to_date']:
                    break
                else:
                    all_dates[leave['from_date'].strftime('%Y-%m-%d')] = 0.25
                    leave['from_date'] = leave['from_date'] + timedelta(days=1)
        else:
            all_dates[leave['from_date'].strftime('%Y-%m-%d')] = 0.25


def add_dates_in_dictionary(all_dates, first_day_of_year, last_day_of_year):
   while True:
       all_dates[first_day_of_year.strftime('%Y-%m-%d')] = 0
       if first_day_of_year < last_day_of_year:
           first_day_of_year = first_day_of_year + timedelta(days=1)
       else:
           break

def setAttendence_data(all_dates, employee):
   employee_present_status = frappe.get_list("Employee Attendance",
                                             fields = ["employee","present","date","half_day"],
                                             filters={
                                               "employee": employee
                                           })
   for attendance in employee_present_status:
       if flt(attendance.half_day) == 1:
           all_dates[str(attendance.date)] = 0.75
       else:
        all_dates[str(attendance.date)] = 1

def set_joining_dates(all_dates, employee):
    employee_joining_date = frappe.get_doc("Employee Details", {"name": employee}, "joining_date")
    today_date = datetime.strptime(today(), "%Y-%m-%d").date()
    for mydate in all_dates:
        if datetime.strptime(mydate, "%Y-%m-%d").date() < employee_joining_date.joining_date:
            all_dates[mydate] = 0.5
        elif datetime.strptime(mydate, "%Y-%m-%d").date() > today_date:
            all_dates[mydate] = 0.5