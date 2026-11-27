# QuickBooks access policy

An access policy limits which endpoints QuickBooks connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/quickbooks#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for QuickBooks: its 48 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create quickbooks --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v3/company/{id}/account/{id}"},
    {"method": "GET", "path": "v3/company/{id}/attachable/{id}"},
    {"method": "GET", "path": "v3/company/{id}/bill/{id}"},
    {"method": "GET", "path": "v3/company/{id}/billpayment/{id}"},
    {"method": "GET", "path": "v3/company/{id}/budget/{id}"},
    {"method": "GET", "path": "v3/company/{id}/cdc"},
    {"method": "GET", "path": "v3/company/{id}/class/{id}"},
    {"method": "GET", "path": "v3/company/{id}/companycurrency/{id}"},
    {"method": "GET", "path": "v3/company/{id}/companyinfo/{id}"},
    {"method": "GET", "path": "v3/company/{id}/creditcardpayment/{id}"},
    {"method": "GET", "path": "v3/company/{id}/creditmemo/{id}"},
    {"method": "GET", "path": "v3/company/{id}/creditmemo/{id}/pdf"},
    {"method": "GET", "path": "v3/company/{id}/customer/{id}"},
    {"method": "GET", "path": "v3/company/{id}/customertype/{id}"},
    {"method": "GET", "path": "v3/company/{id}/department/{id}"},
    {"method": "GET", "path": "v3/company/{id}/deposit/{id}"},
    {"method": "GET", "path": "v3/company/{id}/employee/{id}"},
    {"method": "GET", "path": "v3/company/{id}/estimate/{id}"},
    {"method": "GET", "path": "v3/company/{id}/estimate/{id}/pdf"},
    {"method": "GET", "path": "v3/company/{id}/exchangerate"},
    {"method": "GET", "path": "v3/company/{id}/invoice/{id}"},
    {"method": "GET", "path": "v3/company/{id}/invoice/{id}/pdf"},
    {"method": "GET", "path": "v3/company/{id}/item/{id}"},
    {"method": "GET", "path": "v3/company/{id}/journalcode/{id}"},
    {"method": "GET", "path": "v3/company/{id}/journalentry/{id}"},
    {"method": "GET", "path": "v3/company/{id}/payment/{id}"},
    {"method": "GET", "path": "v3/company/{id}/paymentmethod/{id}"},
    {"method": "GET", "path": "v3/company/{id}/preferences"},
    {"method": "GET", "path": "v3/company/{id}/purchase/{id}"},
    {"method": "GET", "path": "v3/company/{id}/purchaseorder/{id}"},
    {"method": "GET", "path": "v3/company/{id}/purchaseorder/{id}/pdf"},
    {"method": "GET", "path": "v3/company/{id}/query"},
    {"method": "POST", "path": "v3/company/{id}/query"},
    {"method": "GET", "path": "v3/company/{id}/recurringtransaction/{id}"},
    {"method": "GET", "path": "v3/company/{id}/refundreceipt/{id}"},
    {"method": "GET", "path": "v3/company/{id}/refundreceipt/{id}/pdf"},
    {"method": "GET", "path": "v3/company/{id}/reports/{id}"},
    {"method": "GET", "path": "v3/company/{id}/salesreceipt/{id}"},
    {"method": "GET", "path": "v3/company/{id}/salesreceipt/{id}/pdf"},
    {"method": "GET", "path": "v3/company/{id}/taxagency/{id}"},
    {"method": "GET", "path": "v3/company/{id}/taxclassification/{id}"},
    {"method": "GET", "path": "v3/company/{id}/taxcode/{id}"},
    {"method": "GET", "path": "v3/company/{id}/taxrate/{id}"},
    {"method": "GET", "path": "v3/company/{id}/term/{id}"},
    {"method": "GET", "path": "v3/company/{id}/timeactivity/{id}"},
    {"method": "GET", "path": "v3/company/{id}/transfer/{id}"},
    {"method": "GET", "path": "v3/company/{id}/vendor/{id}"},
    {"method": "GET", "path": "v3/company/{id}/vendorcredit/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The QuickBooks endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v3/company/{id}/account | write | account | Create, update, sparse-update, void or delete a account (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/account/{id} | read | account | Read a account by Id. |
| POST | v3/company/{id}/attachable | write | attachable | Create, update, sparse-update, void or delete a attachable (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/attachable/{id} | read | attachable | Read a attachable by Id. |
| POST | v3/company/{id}/upload | write | attachable | Upload a file attachment and link it to transactions. |
| POST | v3/company/{id}/batch | write | batch | Run multiple operations in one request; may include creates, updates and deletes. |
| POST | v3/company/{id}/bill | write | bill | Create, update, sparse-update, void or delete a bill (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/bill/{id} | read | bill | Read a bill by Id. |
| POST | v3/company/{id}/billpayment | write | billpayment | Create, update, sparse-update, void or delete a billpayment (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/billpayment/{id} | read | billpayment | Read a billpayment by Id. |
| GET | v3/company/{id}/budget/{id} | read | budget | Read a budget by Id. |
| GET | v3/company/{id}/cdc | read | cdc | Return entities changed since a given timestamp (change data capture). |
| POST | v3/company/{id}/class | write | class | Create, update, sparse-update, void or delete a class (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/class/{id} | read | class | Read a class by Id. |
| POST | v3/company/{id}/companycurrency | write | companycurrency | Create, update, sparse-update, void or delete a companycurrency (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/companycurrency/{id} | read | companycurrency | Read a companycurrency by Id. |
| POST | v3/company/{id}/companyinfo | write | companyinfo | Update company information. |
| GET | v3/company/{id}/companyinfo/{id} | read | companyinfo | Read company information. |
| POST | v3/company/{id}/creditcardpayment | write | creditcardpayment | Create, update, sparse-update, void or delete a creditcardpayment (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/creditcardpayment/{id} | read | creditcardpayment | Read a creditcardpayment by Id. |
| POST | v3/company/{id}/creditmemo | write | creditmemo | Create, update, sparse-update, void or delete a creditmemo (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/creditmemo/{id} | read | creditmemo | Read a creditmemo by Id. |
| GET | v3/company/{id}/creditmemo/{id}/pdf | read | creditmemo | Download a creditmemo as a PDF. |
| POST | v3/company/{id}/creditmemo/{id}/send | write | creditmemo | Email a creditmemo to a recipient. |
| POST | v3/company/{id}/customer | write | customer | Create, update, sparse-update, void or delete a customer (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/customer/{id} | read | customer | Read a customer by Id. |
| POST | v3/company/{id}/customertype | write | customertype | Create, update, sparse-update, void or delete a customertype (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/customertype/{id} | read | customertype | Read a customertype by Id. |
| POST | v3/company/{id}/department | write | department | Create, update, sparse-update, void or delete a department (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/department/{id} | read | department | Read a department by Id. |
| POST | v3/company/{id}/deposit | write | deposit | Create, update, sparse-update, void or delete a deposit (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/deposit/{id} | read | deposit | Read a deposit by Id. |
| POST | v3/company/{id}/employee | write | employee | Create, update, sparse-update, void or delete a employee (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/employee/{id} | read | employee | Read a employee by Id. |
| POST | v3/company/{id}/estimate | write | estimate | Create, update, sparse-update, void or delete a estimate (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/estimate/{id} | read | estimate | Read a estimate by Id. |
| GET | v3/company/{id}/estimate/{id}/pdf | read | estimate | Download a estimate as a PDF. |
| POST | v3/company/{id}/estimate/{id}/send | write | estimate | Email a estimate to a recipient. |
| GET | v3/company/{id}/exchangerate | read | exchangerate | Read the exchange rate for a currency pair and date. |
| POST | v3/company/{id}/exchangerate | write | exchangerate | Update an exchange rate. |
| POST | v3/company/{id}/invoice | write | invoice | Create, update, sparse-update, void or delete a invoice (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/invoice/{id} | read | invoice | Read a invoice by Id. |
| GET | v3/company/{id}/invoice/{id}/pdf | read | invoice | Download a invoice as a PDF. |
| POST | v3/company/{id}/invoice/{id}/send | write | invoice | Email a invoice to a recipient. |
| POST | v3/company/{id}/item | write | item | Create, update, sparse-update, void or delete a item (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/item/{id} | read | item | Read a item by Id. |
| POST | v3/company/{id}/journalcode | write | journalcode | Create, update, sparse-update, void or delete a journalcode (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/journalcode/{id} | read | journalcode | Read a journalcode by Id. |
| POST | v3/company/{id}/journalentry | write | journalentry | Create, update, sparse-update, void or delete a journalentry (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/journalentry/{id} | read | journalentry | Read a journalentry by Id. |
| POST | v3/company/{id}/payment | write | payment | Create, update, sparse-update, void or delete a payment (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/payment/{id} | read | payment | Read a payment by Id. |
| POST | v3/company/{id}/paymentmethod | write | paymentmethod | Create, update, sparse-update, void or delete a paymentmethod (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/paymentmethod/{id} | read | paymentmethod | Read a paymentmethod by Id. |
| GET | v3/company/{id}/preferences | read | preferences | Read company preferences. |
| POST | v3/company/{id}/preferences | write | preferences | Update company preferences. |
| POST | v3/company/{id}/purchase | write | purchase | Create, update, sparse-update, void or delete a purchase (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/purchase/{id} | read | purchase | Read a purchase by Id. |
| POST | v3/company/{id}/purchaseorder | write | purchaseorder | Create, update, sparse-update, void or delete a purchaseorder (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/purchaseorder/{id} | read | purchaseorder | Read a purchaseorder by Id. |
| GET | v3/company/{id}/purchaseorder/{id}/pdf | read | purchaseorder | Download a purchaseorder as a PDF. |
| POST | v3/company/{id}/purchaseorder/{id}/send | write | purchaseorder | Email a purchaseorder to a recipient. |
| GET | v3/company/{id}/query | read | query | Run a SQL-like query for any entity. |
| POST | v3/company/{id}/query | read | query | Run a SQL-like query for any entity, sent in the request body. |
| POST | v3/company/{id}/recurringtransaction | write | recurringtransaction | Create, update, sparse-update, void or delete a recurringtransaction (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/recurringtransaction/{id} | read | recurringtransaction | Read a recurringtransaction by Id. |
| POST | v3/company/{id}/refundreceipt | write | refundreceipt | Create, update, sparse-update, void or delete a refundreceipt (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/refundreceipt/{id} | read | refundreceipt | Read a refundreceipt by Id. |
| GET | v3/company/{id}/refundreceipt/{id}/pdf | read | refundreceipt | Download a refundreceipt as a PDF. |
| POST | v3/company/{id}/refundreceipt/{id}/send | write | refundreceipt | Email a refundreceipt to a recipient. |
| GET | v3/company/{id}/reports/{id} | read | reports | Run a report by name (ProfitAndLoss, BalanceSheet, GeneralLedger, AgedReceivables, etc.). |
| POST | v3/company/{id}/salesreceipt | write | salesreceipt | Create, update, sparse-update, void or delete a salesreceipt (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/salesreceipt/{id} | read | salesreceipt | Read a salesreceipt by Id. |
| GET | v3/company/{id}/salesreceipt/{id}/pdf | read | salesreceipt | Download a salesreceipt as a PDF. |
| POST | v3/company/{id}/salesreceipt/{id}/send | write | salesreceipt | Email a salesreceipt to a recipient. |
| POST | v3/company/{id}/taxagency | write | taxagency | Create, update, sparse-update, void or delete a taxagency (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/taxagency/{id} | read | taxagency | Read a taxagency by Id. |
| GET | v3/company/{id}/taxclassification/{id} | read | taxclassification | Read a tax classification by Id. |
| POST | v3/company/{id}/taxcode | write | taxcode | Create, update, sparse-update, void or delete a taxcode (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/taxcode/{id} | read | taxcode | Read a taxcode by Id. |
| POST | v3/company/{id}/taxrate | write | taxrate | Create, update, sparse-update, void or delete a taxrate (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/taxrate/{id} | read | taxrate | Read a taxrate by Id. |
| POST | v3/company/{id}/taxservice/taxcode | write | taxservice | Create a tax code with its tax rates. |
| POST | v3/company/{id}/term | write | term | Create, update, sparse-update, void or delete a term (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/term/{id} | read | term | Read a term by Id. |
| POST | v3/company/{id}/timeactivity | write | timeactivity | Create, update, sparse-update, void or delete a timeactivity (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/timeactivity/{id} | read | timeactivity | Read a timeactivity by Id. |
| POST | v3/company/{id}/transfer | write | transfer | Create, update, sparse-update, void or delete a transfer (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/transfer/{id} | read | transfer | Read a transfer by Id. |
| POST | v3/company/{id}/vendor | write | vendor | Create, update, sparse-update, void or delete a vendor (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/vendor/{id} | read | vendor | Read a vendor by Id. |
| POST | v3/company/{id}/vendorcredit | write | vendorcredit | Create, update, sparse-update, void or delete a vendorcredit (operation chosen by request body and the operation query parameter). |
| GET | v3/company/{id}/vendorcredit/{id} | read | vendorcredit | Read a vendorcredit by Id. |
