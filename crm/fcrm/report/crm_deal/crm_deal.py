import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Deal", "fieldname": "deal", "fieldtype": "Data", "width": 220, "align": "left"},
        {"label": "Organization", "fieldname": "organization", "fieldtype": "Link", "options": "CRM Organization", "width": 180, "align": "left"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Link", "options": "CRM Deal Status", "width": 120, "align": "left"},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branches", "width": 150, "align": "left"},
        {"label": "Executive", "fieldname": "executive", "fieldtype": "Link", "options": "Executive", "width": 140, "align": "left"},
        {"label": "Business Partner", "fieldname": "business_partner", "fieldtype": "Link", "options": "Business Partner", "width": 140, "align": "left"},
        {"label": "Project", "fieldname": "project_name", "fieldtype": "Data", "width": 160, "align": "left"},
        {"label": "Product Code", "fieldname": "product_code", "fieldtype": "Link", "options": "CRM Products", "width": 160, "align": "left"},
        {"label": "Product Name", "fieldname": "product_name", "fieldtype": "Data", "width": 200, "align": "left"},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 120, "align": "left"},
        {"label": "Discount %", "fieldname": "discount_percentage", "fieldtype": "Percent", "width": 120, "align": "left"},
        {"label": "Discount Amount", "fieldname": "discount_amount", "fieldtype": "Currency", "width": 120, "align": "left"},
    ]

def get_data(filters):
    conditions = ""
    values = {}

    join_products = False

    if filters.get("deal"):
        conditions += " AND cd.name = %(deal)s"
        values["deal"] = filters.get("deal")

    if filters.get("branch"):
        conditions += " AND cd.branch = %(branch)s"
        values["branch"] = filters.get("branch")

    if filters.get("status"):
        conditions += " AND cd.status = %(status)s"
        values["status"] = filters.get("status")

    if filters.get("organization"):
        conditions += " AND cd.organization = %(organization)s"
        values["organization"] = filters.get("organization")

    if filters.get("executive"):
        conditions += " AND cd.executive = %(executive)s"
        values["executive"] = filters.get("executive")

    if filters.get("business_partner"):
        conditions += " AND cd.business_partner = %(business_partner)s"
        values["business_partner"] = filters.get("business_partner")

    if filters.get("project_name"):
        conditions += " AND cd.project_name LIKE %(project_name)s"
        values["project_name"] = f"%{filters.get('project_name')}%"

    # Check if product_code filter exists, then we join tabCRM Products
    if filters.get("product_code"):
        join_products = True
        conditions += " AND cp.product_code = %(product_code)s"
        values["product_code"] = filters.get("product_code")

    # Build the deals query
    deals_query = f"""
        SELECT
            cd.name AS deal,
            cd.organization,
            cd.status,
            cd.branch,
            cd.executive,
            cd.business_partner,
            cd.project_name
        FROM `tabCRM Deal` cd
    """

    if join_products:
        deals_query += """
            INNER JOIN `tabCRM Products` cp ON cp.parent = cd.name
        """

    deals_query += f"""
        WHERE cd.docstatus < 2
        {conditions}
        ORDER BY cd.name
    """

    deals = frappe.db.sql(deals_query, values, as_dict=1)

    # Early return if no deals found
    if not deals:
        return []

    deal_names = [d['deal'] for d in deals]
    placeholders = ', '.join(['%s'] * len(deal_names))

    products_query = f"""
        SELECT
            cp.parent AS deal,
            cp.product_code,
            cp.product_name,
            cp.rate,
            cp.discount_percentage,
            cp.discount_amount
        FROM `tabCRM Products` cp
        WHERE cp.parent IN ({placeholders})
        ORDER BY cp.idx
    """
    products = frappe.db.sql(products_query, tuple(deal_names), as_dict=1)

    products_by_deal = {}
    for p in products:
        products_by_deal.setdefault(p['deal'], []).append(p)

    data = []
    for deal in deals:
        deal_name = deal["deal"]
        data.append({
            "deal": deal_name,
            "organization": deal.get("organization"),
            "status": deal.get("status"),
            "branch": deal.get("branch"),
            "executive": deal.get("executive"),
            "business_partner": deal.get("business_partner"),
            "project_name": deal.get("project_name"),
            "product_code": None,
            "product_name": None,
            "rate": None,
            "discount_percentage": None,
            "discount_amount": None,
            "parent_deal": None,
            "indent": 0,
            "expandable": True,
        })
        for prod in products_by_deal.get(deal_name, []):
            data.append({
                "deal": None,
                "organization": None,
                "status": None,
                "branch": None,
                "executive": None,
                "business_partner": None,
                "project_name": None,
                "product_code": prod.get("product_code"),
                "product_name": prod.get("product_name"),
                "rate": prod.get("rate"),
                "discount_percentage": prod.get("discount_percentage"),
                "discount_amount": prod.get("discount_amount"),
                "parent_deal": deal_name,
                "indent": 1,
                "expandable": False,
            })

    return data
