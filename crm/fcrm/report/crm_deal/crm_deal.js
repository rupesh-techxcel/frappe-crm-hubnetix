frappe.query_reports["CRM Deal"] = {
    "filters": [
        {
            "fieldname": "deal",
            "label": __("Deal"),
            "fieldtype": "Link",
            "options": "CRM Deal",
            "reqd": 0
        },
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "options": "Branches",
            "reqd": 0
        },
        {
            "fieldname": "product_code",
            "label": __("Product Code"),
            "fieldtype": "Link",
            "options": "CRM Product",
            "reqd": 0
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Link",
            "options": "CRM Deal Status",
            "reqd": 0
        },
        {
            "fieldname": "organization",
            "label": __("Organization"),
            "fieldtype": "Link",
            "options": "CRM Organization",
            "reqd": 0
        },
        {
            "fieldname": "executive",
            "label": __("Executive"),
            "fieldtype": "Link",
            "options": "Executive",
            "reqd": 0
        },
        {
            "fieldname": "business_partner",
            "label": __("Business Partner"),
            "fieldtype": "Link",
            "options": "Business Partner",
            "reqd": 0
        },
        {
            "fieldname": "project_name",
            "label": __("Project Name"),
            "fieldtype": "Data",
            "reqd": 0
        }
    ],
    is_tree: true,
    tree_parent_field: "parent_deal"
};
