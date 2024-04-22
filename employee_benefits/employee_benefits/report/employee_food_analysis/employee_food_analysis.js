// Copyright (c) 2024, Samuvelramesh2@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Food Analysis"] = {
	"filters": [
		{
			reqd: 1,
			fieldname: "month",
			label: __("No of Month"),
			fieldtype: "Int",
		},
		{
			reqd: 0,
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Data", // suppose to be link and linked with employee doctype in HRMS
		},
		{
			reqd: 0,
			fieldname: "pen_aplbe",
			label: __("Penality Applicable"),
			fieldtype: "Select",
			options: ["","Yes", "No"]
		},
		{
			reqd: 0,
			fieldname: "is_veg",
			label: __("Is Veg"),
			fieldtype: "Check",
		},
	],
};
