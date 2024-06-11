# Copyright (c) 2024, Amandeep and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today

class EmployeeAttendance(Document):
	def validate(self):
		# check if the selected date is ahead of the current date
		if self.date > today():
			frappe.throw(_("Cannot Mark Attendance for Future Days."))

		# check if the attendance is already marked
		if frappe.db.exists("Employee Attendance",{"employee":self.employee,"date":self.date}):
			frappe.throw(_(f"You have already marked the attendance for {self.date}"))