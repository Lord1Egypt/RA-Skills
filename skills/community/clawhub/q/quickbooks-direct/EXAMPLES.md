# QuickBooks API Examples

This document provides practical examples for common QuickBooks operations using the skill.

## Table of Contents
- [Setup & Authentication](#setup--authentication)
- [Customer Management](#customer-management)
- [Invoice Workflows](#invoice-workflows)
- [Inventory Management](#inventory-management)
- [Payment Processing](#payment-processing)
- [Financial Reporting](#financial-reporting)
- [Vendor & Bill Management](#vendor--bill-management)
- [Advanced Queries](#advanced-queries)

## Setup & Authentication

### Initial Authentication

```javascript
// Step 1: Authenticate with QuickBooks
{
  "tool": "qb_authenticate",
  "arguments": {
    "client_id": "ABxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

This will:
1. Open a browser window
2. Redirect to QuickBooks authorization
3. Capture the auth code automatically
4. Save tokens to config.json

## Customer Management

### Create a Basic Customer

```json
{
  "tool": "qb_create_customer",
  "arguments": {
    "DisplayName": "Acme Corporation",
    "CompanyName": "Acme Corp",
    "PrimaryEmailAddr": {
      "Address": "billing@acme.com"
    }
  }
}
```

### Create a Customer with Full Details

```json
{
  "tool": "qb_create_customer",
  "arguments": {
    "DisplayName": "John Smith",
    "GivenName": "John",
    "FamilyName": "Smith",
    "CompanyName": "Smith Consulting",
    "PrimaryEmailAddr": {
      "Address": "john@smithconsulting.com"
    },
    "PrimaryPhone": {
      "FreeFormNumber": "(555) 123-4567"
    },
    "Mobile": {
      "FreeFormNumber": "(555) 987-6543"
    },
    "BillAddr": {
      "Line1": "123 Main Street",
      "Line2": "Suite 100",
      "City": "San Francisco",
      "CountrySubDivisionCode": "CA",
      "PostalCode": "94102",
      "Country": "USA"
    },
    "ShipAddr": {
      "Line1": "456 Oak Avenue",
      "City": "San Francisco",
      "CountrySubDivisionCode": "CA",
      "PostalCode": "94103",
      "Country": "USA"
    },
    "Notes": "Preferred customer - Net 30 terms",
    "WebAddr": {
      "URI": "https://smithconsulting.com"
    }
  }
}
```

### Find Customers by Name

```json
{
  "tool": "qb_query_customers",
  "arguments": {
    "query": "SELECT * FROM Customer WHERE DisplayName LIKE '%Smith%'"
  }
}
```

### Get All Active Customers

```json
{
  "tool": "qb_query_customers",
  "arguments": {
    "query": "SELECT * FROM Customer WHERE Active = true ORDER BY DisplayName"
  }
}
```

### Get Customer by ID

```json
{
  "tool": "qb_get_customer",
  "arguments": {
    "customer_id": "123"
  }
}
```

## Invoice Workflows

### Create a Simple Invoice

```json
{
  "tool": "qb_create_invoice",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "Line": [
      {
        "Amount": 500.00,
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "ItemRef": {
            "value": "1"
          },
          "Qty": 10,
          "UnitPrice": 50.00
        }
      }
    ],
    "TxnDate": "2026-02-21",
    "DueDate": "2026-03-21"
  }
}
```

### Create an Invoice with Multiple Line Items

```json
{
  "tool": "qb_create_invoice",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "Line": [
      {
        "Amount": 1000.00,
        "DetailType": "SalesItemLineDetail",
        "Description": "Consulting Services - February 2026",
        "SalesItemLineDetail": {
          "ItemRef": {
            "value": "1"
          },
          "Qty": 20,
          "UnitPrice": 50.00
        }
      },
      {
        "Amount": 150.00,
        "DetailType": "SalesItemLineDetail",
        "Description": "Travel Expenses",
        "SalesItemLineDetail": {
          "ItemRef": {
            "value": "2"
          },
          "Qty": 1,
          "UnitPrice": 150.00
        }
      }
    ],
    "TxnDate": "2026-02-21",
    "DueDate": "2026-03-21",
    "CustomerMemo": {
      "value": "Thank you for your business!"
    },
    "BillEmail": {
      "Address": "billing@customer.com"
    }
  }
}
```

### Send an Invoice via Email

```json
{
  "tool": "qb_send_invoice",
  "arguments": {
    "invoice_id": "456",
    "email": "customer@example.com"
  }
}
```

### Query Unpaid Invoices

```json
{
  "tool": "qb_query_invoices",
  "arguments": {
    "query": "SELECT * FROM Invoice WHERE Balance > 0 ORDER BY DueDate"
  }
}
```

### Query Invoices by Date Range

```json
{
  "tool": "qb_query_invoices",
  "arguments": {
    "query": "SELECT * FROM Invoice WHERE TxnDate >= '2026-01-01' AND TxnDate <= '2026-01-31'"
  }
}
```

### Query Overdue Invoices

```json
{
  "tool": "qb_query_invoices",
  "arguments": {
    "query": "SELECT * FROM Invoice WHERE Balance > 0 AND DueDate < '2026-02-21' ORDER BY DueDate"
  }
}
```

## Inventory Management

### Create a Service Item

```json
{
  "tool": "qb_create_item",
  "arguments": {
    "Name": "Consulting Services",
    "Type": "Service",
    "Description": "Hourly consulting services",
    "UnitPrice": 150.00,
    "IncomeAccountRef": {
      "value": "79"
    }
  }
}
```

### Create an Inventory Item

```json
{
  "tool": "qb_create_item",
  "arguments": {
    "Name": "Widget Pro 3000",
    "Type": "Inventory",
    "Description": "Professional grade widget",
    "UnitPrice": 299.99,
    "QtyOnHand": 50,
    "InvStartDate": "2026-01-01",
    "IncomeAccountRef": {
      "value": "79"
    },
    "ExpenseAccountRef": {
      "value": "80"
    },
    "AssetAccountRef": {
      "value": "81"
    },
    "TrackQtyOnHand": true
  }
}
```

### Create a Non-Inventory Item

```json
{
  "tool": "qb_create_item",
  "arguments": {
    "Name": "Shipping & Handling",
    "Type": "NonInventory",
    "Description": "Standard shipping fee",
    "UnitPrice": 15.00,
    "IncomeAccountRef": {
      "value": "79"
    }
  }
}
```

### Query All Items

```json
{
  "tool": "qb_query_items",
  "arguments": {
    "query": "SELECT * FROM Item WHERE Active = true ORDER BY Name"
  }
}
```

### Query Low Stock Items

```json
{
  "tool": "qb_query_items",
  "arguments": {
    "query": "SELECT * FROM Item WHERE Type = 'Inventory' AND QtyOnHand < 10"
  }
}
```

## Payment Processing

### Record a Full Payment Against an Invoice

```json
{
  "tool": "qb_create_payment",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "TotalAmt": 500.00,
    "TxnDate": "2026-02-21",
    "Line": [
      {
        "Amount": 500.00,
        "LinkedTxn": [
          {
            "TxnId": "456",
            "TxnType": "Invoice"
          }
        ]
      }
    ],
    "PaymentMethodRef": {
      "value": "1"
    }
  }
}
```

### Record a Partial Payment

```json
{
  "tool": "qb_create_payment",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "TotalAmt": 250.00,
    "TxnDate": "2026-02-21",
    "Line": [
      {
        "Amount": 250.00,
        "LinkedTxn": [
          {
            "TxnId": "456",
            "TxnType": "Invoice"
          }
        ]
      }
    ],
    "PrivateNote": "Partial payment - balance due next month"
  }
}
```

### Record a Payment for Multiple Invoices

```json
{
  "tool": "qb_create_payment",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "TotalAmt": 1500.00,
    "TxnDate": "2026-02-21",
    "Line": [
      {
        "Amount": 1000.00,
        "LinkedTxn": [
          {
            "TxnId": "456",
            "TxnType": "Invoice"
          }
        ]
      },
      {
        "Amount": 500.00,
        "LinkedTxn": [
          {
            "TxnId": "457",
            "TxnType": "Invoice"
          }
        ]
      }
    ]
  }
}
```

### Query Recent Payments

```json
{
  "tool": "qb_query_payments",
  "arguments": {
    "query": "SELECT * FROM Payment WHERE TxnDate >= '2026-02-01' ORDER BY TxnDate DESC"
  }
}
```

## Financial Reporting

### Get Profit & Loss Report for Last Month

```json
{
  "tool": "qb_get_profit_loss",
  "arguments": {
    "start_date": "2026-01-01",
    "end_date": "2026-01-31"
  }
}
```

### Get Year-to-Date Profit & Loss

```json
{
  "tool": "qb_get_profit_loss",
  "arguments": {
    "start_date": "2026-01-01",
    "end_date": "2026-02-21"
  }
}
```

### Get Current Balance Sheet

```json
{
  "tool": "qb_get_balance_sheet",
  "arguments": {
    "date": "2026-02-21"
  }
}
```

### Get Cash Flow Report

```json
{
  "tool": "qb_get_cash_flow",
  "arguments": {
    "start_date": "2026-01-01",
    "end_date": "2026-02-21"
  }
}
```

### Get Aged Receivables (Who Owes You Money)

```json
{
  "tool": "qb_get_aged_receivables",
  "arguments": {}
}
```

### Get Aged Payables (Who You Owe Money)

```json
{
  "tool": "qb_get_aged_payables",
  "arguments": {}
}
```

## Vendor & Bill Management

### Create a Vendor

```json
{
  "tool": "qb_create_vendor",
  "arguments": {
    "DisplayName": "Office Supplies Inc",
    "CompanyName": "Office Supplies Inc",
    "PrimaryEmailAddr": {
      "Address": "billing@officesupplies.com"
    },
    "PrimaryPhone": {
      "FreeFormNumber": "(555) 555-5555"
    },
    "BillAddr": {
      "Line1": "789 Commercial Blvd",
      "City": "New York",
      "CountrySubDivisionCode": "NY",
      "PostalCode": "10001"
    }
  }
}
```

### Create a Bill

```json
{
  "tool": "qb_create_bill",
  "arguments": {
    "VendorRef": {
      "value": "789"
    },
    "Line": [
      {
        "Amount": 350.00,
        "DetailType": "AccountBasedExpenseLineDetail",
        "AccountBasedExpenseLineDetail": {
          "AccountRef": {
            "value": "7"
          }
        },
        "Description": "Office supplies - February"
      }
    ],
    "TxnDate": "2026-02-21",
    "DueDate": "2026-03-21"
  }
}
```

### Query Unpaid Bills

```json
{
  "tool": "qb_query",
  "arguments": {
    "query": "SELECT * FROM Bill WHERE Balance > 0 ORDER BY DueDate"
  }
}
```

## Advanced Queries

### Get Company Information

```json
{
  "tool": "qb_get_company_info",
  "arguments": {}
}
```

### Query Chart of Accounts

```json
{
  "tool": "qb_query_accounts",
  "arguments": {
    "query": "SELECT * FROM Account WHERE Active = true ORDER BY Name"
  }
}
```

### Get Income Accounts

```json
{
  "tool": "qb_query_accounts",
  "arguments": {
    "query": "SELECT * FROM Account WHERE AccountType = 'Income' AND Active = true"
  }
}
```

### Get Expense Accounts

```json
{
  "tool": "qb_query_accounts",
  "arguments": {
    "query": "SELECT * FROM Account WHERE AccountType = 'Expense' AND Active = true"
  }
}
```

### Complex Join Query (Invoices with Customer Names)

```json
{
  "tool": "qb_query",
  "arguments": {
    "query": "SELECT Invoice.Id, Invoice.TxnDate, Invoice.TotalAmt, Customer.DisplayName FROM Invoice INNER JOIN Customer ON Invoice.CustomerRef = Customer.Id WHERE Invoice.TxnDate >= '2026-01-01'"
  }
}
```

### Create a Sales Receipt (Cash Sale)

```json
{
  "tool": "qb_create_sales_receipt",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "Line": [
      {
        "Amount": 100.00,
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "ItemRef": {
            "value": "1"
          },
          "Qty": 2,
          "UnitPrice": 50.00
        }
      }
    ],
    "TxnDate": "2026-02-21",
    "PaymentMethodRef": {
      "value": "1"
    }
  }
}
```

### Create an Estimate/Quote

```json
{
  "tool": "qb_create_estimate",
  "arguments": {
    "CustomerRef": {
      "value": "123"
    },
    "Line": [
      {
        "Amount": 5000.00,
        "DetailType": "SalesItemLineDetail",
        "Description": "Website Development Project",
        "SalesItemLineDetail": {
          "ItemRef": {
            "value": "1"
          },
          "Qty": 100,
          "UnitPrice": 50.00
        }
      }
    ],
    "TxnDate": "2026-02-21",
    "ExpirationDate": "2026-03-21",
    "CustomerMemo": {
      "value": "Estimate valid for 30 days"
    }
  }
}
```

### Batch Operations (Multiple Requests in One Call)

```json
{
  "tool": "qb_batch",
  "arguments": {
    "operations": [
      {
        "bId": "bid1",
        "operation": "create",
        "Customer": {
          "DisplayName": "Batch Customer 1"
        }
      },
      {
        "bId": "bid2",
        "operation": "create",
        "Customer": {
          "DisplayName": "Batch Customer 2"
        }
      },
      {
        "bId": "bid3",
        "operation": "query",
        "Query": "SELECT * FROM Invoice WHERE Balance > 0"
      }
    ]
  }
}
```

## Tips & Best Practices

### Date Formats
Always use ISO 8601 format: `YYYY-MM-DD` (e.g., `2026-02-21`)

### Reference IDs
Most entities require reference IDs in the format:
```json
{
  "value": "123"
}
```

### Line Item Details
For invoices and sales receipts, use `SalesItemLineDetail`.
For bills and expenses, use `AccountBasedExpenseLineDetail` or `ItemBasedExpenseLineDetail`.

### Query Operators
- `=` Equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `LIKE` Pattern matching (use `%` as wildcard)
- `IN` Match any in list
- `AND`, `OR` Logical operators

### Common Pitfalls
1. Always include required references (CustomerRef, ItemRef, etc.)
2. Make sure referenced entities exist before creating dependent entities
3. Use the correct entity type in queries (e.g., `FROM Customer` not `FROM Customers`)
4. Include SyncToken when updating entities
5. Check that dates are not in the future (QuickBooks may reject them)

### Performance Tips
1. Use specific queries instead of `SELECT *` when possible
2. Use batch operations for multiple creates/updates
3. Cache frequently used reference IDs (accounts, items, etc.)
4. Use pagination for large result sets

## Need Help?

- Review the [README.md](README.md) for setup instructions
- Check [QuickBooks API Documentation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- Visit the [QuickBooks Developer Forum](https://help.developer.intuit.com/s/)
