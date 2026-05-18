from fastapi import FastAPI, Form, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import date, datetime, timedelta

app = FastAPI(title="Ledger Bridge Sandbox API")

# --- Auth Credentials ---
API_IDENTIFIER = "WtG58j5XFIRPMJ61vtMhCLeCV6HUmqQT"
API_SECRET = "IGLmLjQNZzZ4NaFGvvHi4B0vqBnfnmT7"

# --- Models ---
# Using Extra.ignore by default in Pydantic v2 to allow extra fields passed in dummy data
class Invoice(BaseModel):
    id: int
    userid: int
    firstname: str
    lastname: str
    companyname: str
    invoicenum: str
    date: str
    duedate: str
    datepaid: Optional[str] = None
    total: float
    subtotal: float
    tax: float
    tax2: float
    status: str
    paymentmethod: str
    currencycode: str

class Client(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    company_name: str
    group_id: int
    status: str

class ClientGroup(BaseModel):
    id: int
    name: str

class Transaction(BaseModel):
    id: int
    userid: int
    currency: int
    gateway: str
    date: str
    description: str
    amountin: float
    amountout: float
    fees: float
    rate: float
    transid: str
    invoiceid: int
    refundid: int

# --- Dummy Data Generation ---

def generate_dummy_data():
    client_groups = [
        ClientGroup(id=1, name="VIP Clients"),
        ClientGroup(id=2, name="Standard Clients"),
    ]

    clients = []
    names = [
        ("Andi", "Lesmana"), ("Bubun", "Badruzaman"), ("Candra", "Wijaya"), 
        ("Diana", "Putri"), ("Eko", "Prasetyo")
    ]
    for i in range(5):
        fname, lname = names[i]
        clients.append(Client(
            id=350 + i,
            email=f"{fname.lower()}@example.com",
            first_name=fname,
            last_name=lname,
            company_name="",
            group_id=1 if i % 2 == 0 else 2,
            status="Active"
        ))

    invoices = []
    transactions = []
    
    base_date = datetime(2026, 4, 25, 10, 0, 0)
    
    # Scaling to 200 records
    for i in range(200):
        inv_id = 14000 + i
        txn_id = 9000 + i
        client = clients[i % 5]
        
        # Determine the base amount (random-ish)
        total = 100000.0 + (i * 7500)
        subtotal = round(total / 1.11, 2)
        tax = round(total - subtotal, 2)
        
        inv_date = (base_date + timedelta(days=i//4)).strftime("%Y-%m-%d")
        paid_datetime = (base_date + timedelta(days=i//4, hours=1, minutes=i%60)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Variety in status
        # 0-179: Paid
        # 180-199: Unpaid
        status = "Paid" if i < 180 else "Unpaid"
        
        # Variety in payment gateways
        gateways = ["duitku_vamandirih2h", "duitku_vacimb", "duitku_vabca", "duitku_permatava", "duitku_alfamart"]
        gateway = gateways[i % len(gateways)]

        invoices.append(Invoice(
            id=inv_id,
            userid=client.id,
            firstname=client.first_name,
            lastname=client.last_name,
            companyname=client.company_name,
            invoicenum=f"INV-2026-{inv_id}",
            date=inv_date,
            duedate=inv_date,
            datepaid=paid_datetime if status == "Paid" else None,
            subtotal=subtotal,
            tax=tax,
            tax2=0.00,
            total=total,
            status=status,
            paymentmethod=gateway,
            currencycode="IDR"
        ))
        
        # Generate WHMCS transaction ONLY for Paid invoices
        # EXCEPT for the "Ghost Payment" case (190-199): 
        # These are Unpaid in WHMCS, but we will NOT create a transaction here 
        # (to simulate them being missing in WHMCS ledger but potentially present in Duitku)
        if status == "Paid":
            transactions.append(Transaction(
                id=txn_id,
                userid=client.id,
                currency=0,
                gateway=gateway,
                date=paid_datetime,
                description=f"Invoice Payment for #{inv_id}",
                amountin=total,
                fees=0.00,
                amountout=0.00,
                rate=1.00000,
                transid=f"D572526{i}ABC{i}XYZ",
                invoiceid=inv_id,
                refundid=0
            ))

    return client_groups, clients, invoices, transactions

CLIENT_GROUPS, CLIENTS, INVOICES, TRANSACTIONS = generate_dummy_data()

# --- Action Handlers ---

ACTION_HANDLERS = {}

def handle_get_clients(form_data=None):
    clients_data = [c.model_dump() for c in CLIENTS]
    return {
        "result": "success",
        "totalresults": len(clients_data),
        "clients": {"client": clients_data}
    }
ACTION_HANDLERS["GetClients"] = handle_get_clients

def handle_get_invoices(form_data=None):
    if form_data is None: form_data = {}
    
    status_filter = form_data.get("status")
    limitstart = int(form_data.get("limitstart", 0))
    limitnum = int(form_data.get("limitnum", 25))  # Default WHMCS limit is typically 25
    orderby = form_data.get("orderby", "id").lower()
    order = form_data.get("order", "asc").lower()

    filtered_invoices = list(INVOICES)
    if status_filter:
        filtered_invoices = [inv for inv in filtered_invoices if inv.status == status_filter]

    # Apply sorting
    reverse_sort = True if order == "desc" else False
    if orderby == "invoicenumber":
        filtered_invoices.sort(key=lambda x: x.invoicenum, reverse=reverse_sort)
    elif orderby == "date":
        filtered_invoices.sort(key=lambda x: x.date, reverse=reverse_sort)
    elif orderby == "duedate":
        filtered_invoices.sort(key=lambda x: x.duedate, reverse=reverse_sort)
    elif orderby == "total":
        filtered_invoices.sort(key=lambda x: x.total, reverse=reverse_sort)
    elif orderby == "status":
        filtered_invoices.sort(key=lambda x: x.status, reverse=reverse_sort)
    else: # default to id
        filtered_invoices.sort(key=lambda x: x.id, reverse=reverse_sort)
        
    total_results = len(filtered_invoices)
    
    # Apply pagination
    if limitnum > 0: # Some users might pass very large limitnum, but if they pass -1 we could return all
        paginated_invoices = filtered_invoices[limitstart : limitstart + limitnum]
    else:
        paginated_invoices = filtered_invoices[limitstart:]

    # Adding extra fields requested by user format, even if not in BaseModel exactly
    # Since we are returning dictionaries via Pydantic model_dump, we can inject
    invoices_data = []
    for i in paginated_invoices:
        d = i.model_dump()
        d.update({
            "last_capture_attempt": "0000-00-00 00:00:00",
            "date_refunded": "0000-00-00 00:00:00",
            "date_cancelled": "0000-00-00 00:00:00",
            "credit": "0.00",
            "taxrate": "11.000",
            "taxrate2": "0.000",
            "paymethodid": "null",
            "notes": "",
            "currencyprefix": "Rp ",
            "currencysuffix": ""
        })
        invoices_data.append(d)
        
    return {
        "result": "success",
        "totalresults": total_results,
        "startnumber": limitstart,
        "numreturned": len(invoices_data),
        "invoices": {"invoice": invoices_data}
    }
ACTION_HANDLERS["GetInvoices"] = handle_get_invoices

def handle_get_client_groups(form_data=None):
    groups_data = [g.model_dump() for g in CLIENT_GROUPS]
    return {
        "result": "success",
        "totalresults": len(groups_data),
        "clientgroups": {"group": groups_data}
    }
ACTION_HANDLERS["GetClientGroups"] = handle_get_client_groups

def handle_get_transactions(form_data=None):
    txn_data = [t.model_dump() for t in TRANSACTIONS]
    return {
        "result": "success",
        "totalresults": len(txn_data),
        "transactions": {"transaction": txn_data}
    }
ACTION_HANDLERS["GetTransactions"] = handle_get_transactions

# --- Single POST Endpoint (WHMCS-style) ---

@app.post("/includes/api.php")
async def api_endpoint(request: Request):
    form_data = await request.form()
    action = form_data.get("action")
    identifier = form_data.get("identifier")
    secret = form_data.get("secret")
    
    if identifier != API_IDENTIFIER or secret != API_SECRET:
        return {
            "result": "error",
            "message": "Authentication Failed"
        }

    handler = ACTION_HANDLERS.get(action)
    if handler is None:
        return {
            "result": "error",
            "message": f"Invalid or missing action: {action}"
        }

    return handler(form_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
