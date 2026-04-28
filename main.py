from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

app = FastAPI(title="Ledger Bridge Sandbox API")

# --- Auth Credentials ---
API_IDENTIFIER = "WtG58j5XFIRPMJ61vtMhCLeCV6HUmqQT"
API_SECRET = "IGLmLjQNZzZ4NaFGvvHi4B0vqBnfnmT7"

# --- Models ---

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

    clients = [
        Client(
            id=351,
            email="",
            first_name="Andi",
            last_name="Lesmana",
            company_name="",
            group_id=1,
            status="Active"
        ),
        Client(
            id=357,
            email="",
            first_name="Bubun",
            last_name="Badruzaman",
            company_name="",
            group_id=2,
            status="Active"
        ),
    ]

    invoices = [
        Invoice(
            id= 14346,
            userid= 351,
            firstname= "Andi",
            lastname= "Lesmana",
            companyname= "",
            invoicenum= "",
            date= "2026-04-25",
            duedate= "2026-04-25",
            datepaid= "2026-04-25 18:23:28",
            last_capture_attempt= "0000-00-00 00:00:00",
            date_refunded= "0000-00-00 00:00:00",
            date_cancelled= "0000-00-00 00:00:00",
            subtotal= "363414.00",
            credit= "0.00",
            tax= "0.00",
            tax2= "0.00",
            total= "363414.00",
            taxrate= "11.000",
            taxrate2= "0.000",
            status= "Paid",
            paymentmethod= "duitku_vamandirih2h",
            paymethodid= "null",
            notes= "",
            created_at= "2026-04-25 18:22:35",
            updated_at= "2026-04-25 18:23:29",
            currencycode= "IDR",
            currencyprefix= "Rp ",
            currencysuffix= ""
        ),
        Invoice(
            id=14247,
            userid=357,
            firstname="Bubun",
            lastname="Badruzaman",
            companyname="",
            invoicenum="",
            date="2026-04-25",
            duedate="2026-05-26",
            datepaid="2026-04-25 00:03:45",
            last_capture_attempt="0000-00-00 00:00:00",
            date_refunded="0000-00-00 00:00:00",
            date_cancelled="0000-00-00 00:00:00",
            subtotal="163700.00",
            credit="0.00",
            tax="18007.00",
            tax2="0.00",
            total="181707.00",
            taxrate="11.000",
            taxrate2="0.000",
            status="Paid",
            paymentmethod="duitku_vacimb",
            paymethodid="null",
            notes="",
            created_at="2026-04-25 00:00:06",
            updated_at="2026-04-25 00:03:45",
            currencycode="IDR",
            currencyprefix="Rp ",
            currencysuffix=""
        ),
    ]

    transactions = [
        Transaction(
            id= 9896,
            userid= 351,
            currency= 0,
            gateway= "duitku_vamandirih2h",
            date= "2026-04-25 18:23:28",
            description= "Invoice Payment",
            amountin= "363414.00",
            fees= "0.00",
            amountout= "0.00",
            rate= "1.00000",
            transid= "D57252613U38DYKNVMZJWR",
            invoiceid= 14346,
            refundid= 0
        ),
        Transaction(
            id=9891,
            userid=357,
            currency=0,
            gateway="duitku_vabca",
            date="2026-04-25 00:03:45",
            description="Invoice Payment",
            amountin=181707.00,
            amountout=0.00,
            fees=0.00,
            rate=1.00,
            transid="D572526KLJ3DT0MVU21HTQ",
            invoiceid=14247,
            refundid=0
        ),
    ]

    return client_groups, clients, invoices, transactions

CLIENT_GROUPS, CLIENTS, INVOICES, TRANSACTIONS = generate_dummy_data()

# --- Action Handlers ---

ACTION_HANDLERS = {}

def handle_get_clients():
    clients_data = [c.model_dump() for c in CLIENTS]
    return {
        "result": "success",
        "totalresults": len(clients_data),
        "clients": {"client": clients_data}
    }
ACTION_HANDLERS["GetClients"] = handle_get_clients

def handle_get_invoices():
    invoices_data = [i.model_dump() for i in INVOICES]
    return {
        "result": "success",
        "totalresults": len(invoices_data),
        "invoices": {"invoice": invoices_data}
    }
ACTION_HANDLERS["GetInvoices"] = handle_get_invoices

def handle_get_client_groups():
    groups_data = [g.model_dump() for g in CLIENT_GROUPS]
    return {
        "result": "success",
        "totalresults": len(groups_data),
        "clientgroups": {"group": groups_data}
    }
ACTION_HANDLERS["GetClientGroups"] = handle_get_client_groups

def handle_get_transactions():
    txn_data = [t.model_dump() for t in TRANSACTIONS]
    return {
        "result": "success",
        "totalresults": len(txn_data),
        "transactions": {"transaction": txn_data}
    }
ACTION_HANDLERS["GetTransactions"] = handle_get_transactions

# --- Single POST Endpoint (WHMCS-style) ---

@app.post("/includes/api.php")
async def api_endpoint(
    action: str = Form(...),
    identifier: str = Form(...),
    secret: str = Form(...),
    responsetype: str = Form("json"),
):
    """
    WHMCS-compatible API endpoint.
    Accepts POST form data with action, identifier, secret, and responsetype.

    Example:
        curl -X POST "http://localhost:8001/includes/api.php" \\
             -d "action=GetClients" \\
             -d "identifier=WtG58j5XFIRPMJ61vtMhCLeCV6HUmqQT" \\
             -d "secret=IGLmLjQNZzZ4NaFGvvHi4B0vqBnfnmT7" \\
             -d "responsetype=json"
    """
    # Validate credentials
    if identifier != API_IDENTIFIER or secret != API_SECRET:
        return {
            "result": "error",
            "message": "Authentication Failed"
        }

    # Route to the correct action handler
    handler = ACTION_HANDLERS.get(action)
    if handler is None:
        return {
            "result": "error",
            "message": f"Invalid or missing action: {action}"
        }

    return handler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
