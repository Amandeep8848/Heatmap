# Copyright (c) 2024, Amandeep and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class LeaveRequest(Document):
	def validate(self):
		if self.from_date > self.to_date:
			frappe.throw(_("Please Enter Valid dates"))
