# Ledger Bridge Sandbox API

Sandbox API yang mensimulasikan endpoint WHMCS untuk kebutuhan pengujian integrasi.

## Endpoint
`POST /includes/api.php`

## Authentication
Request harus menyertakan kredensial berikut dalam form-data:

- **identifier**: `WtG58j5XFIRPMJ61vtMhCLeCV6HUmqQT`
- **secret**: `IGLmLjQNZzZ4NaFGvvHi4B0vqBnfnmT7`

## Request Parameters
| Parameter | Tipe | Wajib | Keterangan |
| :--- | :--- | :--- | :--- |
| `action` | string | Ya | Nama aksi (e.g., `GetClients`, `GetInvoices`) |
| `identifier` | string | Ya | API Identifier |
| `secret` | string | Ya | API Secret |
| `responsetype` | string | Tidak | Format respon (default: `json`) |

## Supported Actions & Full Responses

### 1. GetClients
Mengambil daftar client.
- **Request**: `action=GetClients`
- **Full Response**:
```json
{
    "result": "success",
    "totalresults": 2,
    "clients": {
        "client": [
            {
                "id": 351,
                "email": "",
                "first_name": "Andi",
                "last_name": "Lesmana",
                "company_name": "",
                "group_id": 1,
                "status": "Active"
            },
            {
                "id": 357,
                "email": "",
                "first_name": "Bubun",
                "last_name": "Badruzaman",
                "company_name": "",
                "group_id": 2,
                "status": "Active"
            }
        ]
    }
}
```

### 2. GetInvoices
Mengambil daftar invoice.
- **Request**: `action=GetInvoices`
- **Full Response**:
```json
{
    "result": "success",
    "totalresults": 2,
    "invoices": {
        "invoice": [
            {
                "id": 14346,
                "userid": 351,
                "firstname": "Andi",
                "lastname": "Lesmana",
                "companyname": "",
                "invoicenum": "",
                "date": "2026-04-25",
                "duedate": "2026-04-25",
                "datepaid": "2026-04-25 18:23:28",
                "last_capture_attempt": "0000-00-00 00:00:00",
                "date_refunded": "0000-00-00 00:00:00",
                "date_cancelled": "0000-00-00 00:00:00",
                "subtotal": "363414.00",
                "credit": "0.00",
                "tax": "0.00",
                "tax2": "0.00",
                "total": "363414.00",
                "taxrate": "11.000",
                "taxrate2": "0.000",
                "status": "Paid",
                "paymentmethod": "duitku_vamandirih2h",
                "paymethodid": "null",
                "notes": "",
                "created_at": "2026-04-25 18:22:35",
                "updated_at": "2026-04-25 18:23:29",
                "currencycode": "IDR",
                "currencyprefix": "Rp ",
                "currencysuffix": ""
            },
            {
                "id": 14344,
                "userid": 357,
                "firstname": "Bubun",
                "lastname": "Badruzaman",
                "companyname": "",
                "invoicenum": "",
                "date": "2026-04-25",
                "duedate": "2026-05-26",
                "datepaid": "2026-04-25 00:03:45",
                "last_capture_attempt": "0000-00-00 00:00:00",
                "date_refunded": "0000-00-00 00:00:00",
                "date_cancelled": "0000-00-00 00:00:00",
                "subtotal": "163700.00",
                "credit": "0.00",
                "tax": "18007.00",
                "tax2": "0.00",
                "total": "181707.00",
                "taxrate": "11.000",
                "taxrate2": "0.000",
                "status": "Paid",
                "paymentmethod": "duitku_vacimb",
                "paymethodid": "null",
                "notes": "",
                "created_at": "2026-04-25 00:00:06",
                "updated_at": "2026-04-25 00:03:45",
                "currencycode": "IDR",
                "currencyprefix": "Rp ",
                "currencysuffix": ""
            }
        ]
    }
}
```

### 3. GetTransactions
Mengambil daftar transaksi.
- **Request**: `action=GetTransactions`
- **Full Response**:
```json
{
    "result": "success",
    "totalresults": 2,
    "transactions": {
        "transaction": [
            {
                "id": 9896,
                "userid": 351,
                "currency": 0,
                "gateway": "duitku_vamandirih2h",
                "date": "2026-04-25 18:23:28",
                "description": "Invoice Payment",
                "amountin": "363414.00",
                "fees": "0.00",
                "amountout": "0.00",
                "rate": "1.00000",
                "transid": "D57252613U38DYKNVMZJWR",
                "invoiceid": 14346,
                "refundid": 0
            },
            {
                "id": 9891,
                "userid": 357,
                "currency": 0,
                "gateway": "duitku_vabca",
                "date": "2026-04-25 00:03:45",
                "description": "Invoice Payment",
                "amountin": "181707.00",
                "amountout": "0.00",
                "fees": "0.00",
                "rate": "1.00000",
                "transid": "D572526KLJ3DT0MVU21HTQ",
                "invoiceid": 14247,
                "refundid": 0
            }
        ]
    }
}
```

### 4. GetClientGroups
Mengambil daftar group client.
- **Request**: `action=GetClientGroups`
- **Full Response**:
```json
{
    "result": "success",
    "totalresults": 2,
    "clientgroups": {
        "group": [
            {
                "id": 1,
                "name": "VIP Clients"
            },
            {
                "id": 2,
                "name": "Standard Clients"
            }
        ]
    }
}
```

## Cara Penggunaan (Curl Example)

```bash
curl -X POST "http://localhost:8001/includes/api.php" \
  -d "action=GetTransactions" \
  -d "identifier=WtG58j5XFIRPMJ61vtMhCLeCV6HUmqQT" \
  -d "secret=IGLmLjQNZzZ4NaFGvvHi4B0vqBnfnmT7" \
  -d "responsetype=json"
```

## Error Responses
Jika autentikasi gagal:
```json
{
    "result": "error",
    "message": "Authentication Failed"
}
```
Jika aksi tidak ditemukan:
```json
{
    "result": "error",
    "message": "Invalid or missing action: UnknownAction"
}
```
