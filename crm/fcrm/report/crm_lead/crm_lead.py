import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Organization", "fieldname": "organization", "fieldtype": "Link", "options": "CRM Organization", "width": 180},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branches", "width": 150},
        {"label": "Executive", "fieldname": "executive", "fieldtype": "Data", "width": 160},
        {"label": "Status", "fieldname": "status", "fieldtype": "Link", "options": "CRM Lead Status", "width": 120}
    ]

def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("branch"):
        conditions += " AND cl.branch = %(branch)s"
        values["branch"] = filters.get("branch")

    if filters.get("status"):
        conditions += " AND cl.status = %(status)s"
        values["status"] = filters.get("status")

    if filters.get("organization"):
        conditions += " AND cl.organization = %(organization)s"
        values["organization"] = filters.get("organization")

    query = f"""
        SELECT
            cl.organization,
            cl.branch,
            cl.executive,
            cl.status
        FROM `tabCRM Lead` cl
        WHERE cl.docstatus < 2
        {conditions}
    """
    return frappe.db.sql(query, values, as_dict=1)
