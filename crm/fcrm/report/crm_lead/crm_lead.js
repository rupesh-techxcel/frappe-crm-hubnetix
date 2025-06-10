// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["CRM Lead"] = {
	"filters": [

	]
};
frappe.query_reports["CRM Lead"] = {
    filters: [
        {
            fieldname: "branch",
            label: __("Branch"),
            fieldtype: "Link",
            options: "Branches",
            reqd: 0
        },
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Link",
            options: "CRM Lead Status",
            reqd: 0
        },
        {
            fieldname: "organization",
            label: __("Organization"),
            fieldtype: "Link",
            options: "CRM Organization",
            reqd: 0
        }
    ]
};
