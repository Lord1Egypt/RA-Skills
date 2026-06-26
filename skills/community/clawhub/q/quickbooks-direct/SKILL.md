---
name: quickbooks-openclaw
version: 1.0.1
description: Comprehensive QuickBooks Online API integration for accounting, invoicing, payments, and financial reporting
author: Armysarge
license: MIT
tags:
  - accounting
  - quickbooks
  - invoicing
  - payments
  - financial
  - erp
  - bookkeeping
category: Business & Finance
---

# QuickBooks API Skill for OpenClaw

A complete QuickBooks Online direct API integration skill for OpenClaw providing full access to accounting, invoicing, customer management, inventory, payments, and financial reporting through the Intuit QuickBooks API.

## Overview

This skill enables OpenClaw to interact with QuickBooks Online for:
- **Customer & Vendor Management**: Create and manage business relationships
- **Invoicing**: Generate, send, and track invoices
- **Payments**: Record and reconcile payments
- **Inventory**: Manage products, services, and stock levels
- **Financial Reports**: Generate P&L, Balance Sheets, Cash Flow, and aging reports
- **Estimates**: Create quotes and proposals
- **Bills**: Track accounts payable
- **Purchase Orders**: Manage procurement

## Prerequisites

1. **QuickBooks Developer Account**
   - Sign up at [https://developer.intuit.com](https://developer.intuit.com)
   - Create a new app in the Developer Portal
   - Enable "QuickBooks Online API" scope

2. **App Credentials**
   - Client ID from your QuickBooks app
   - Client Secret from your QuickBooks app
   - Redirect URI: `http://localhost:3001/callback`

3. **Node.js**
   - Version 18.0.0 or higher
   - npm or yarn package manager

## Installation

### 1. Install Dependencies

```bash
cd "c:\Users\Shaun\Desktop\Quickbooks skill"
npm install
```

Required packages:
- `axios` - HTTP client for API requests
- `express` - OAuth callback server
- `open` - Browser automation for OAuth

### 2. Configure Credentials

Create `config.json` from template:

```bash
cp config.json.template config.json
```

Edit `config.json` with your QuickBooks app credentials:

```json
{
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "redirect_uri": "http://localhost:3001/callback",
  "api_environment": "sandbox",
  "access_token": "",
  "refresh_token": "",
  "realm_id": "",
  "token_expiry": 0
}
```

### 3. Add to Configuration

**For OpenClaw:**

Add to your OpenClaw configuration:
```json
{
  "skills": {
    "quickbooks": {
      "path": "~/.openclaw/workspace/skills/Quickbooks-openclaw",
      "enabled": true,
      "autoStart": true
    }
  }
}
```

## Authentication

### First-Time Setup

1. Use the `qb_authenticate` tool with your credentials:
```
Use qb_authenticate with client_id and client_secret
```

2. A browser window will open automatically
3. Log in to your QuickBooks account
4. Authorize the application
5. You'll be redirected to localhost (handled automatically)
6. Tokens are saved to `config.json`

### Token Management

- **Access tokens** expire after 1 hour (refreshed automatically)
- **Refresh tokens** last 100 days (renewed on refresh)
- The skill automatically refreshes tokens before they expire
- Re-authenticate if you see "Not authenticated" errors

## Available Tools

### 🔐 Authentication

#### `qb_authenticate`
Initiate OAuth2 authentication flow.

**Parameters:**
- `client_id` (required): Your QuickBooks app Client ID
- `client_secret` (required): Your QuickBooks app Client Secret
- `redirect_uri` (optional): OAuth redirect URI (default: http://localhost:3001/callback)

**Example:**
```json
{
  "client_id": "ABxxxxxxxxxxxxxxxxxxxx",
  "client_secret": "xxxxxxxxxxxxxxxxxx"
}
```

---

### 👥 Customer Management

#### `qb_create_customer`
Create a new customer.

**Parameters:**
- `DisplayName` (required): Customer display name
- `CompanyName`: Company name
- `GivenName`: First name
- `FamilyName`: Last name
- `PrimaryEmailAddr`: Email address object
- `PrimaryPhone`: Phone number object
- `BillAddr`: Billing address object
- `ShipAddr`: Shipping address object

**Example:**
```json
{
  "DisplayName": "Acme Corporation",
  "PrimaryEmailAddr": {
    "Address": "billing@acme.com"
  }
}
```

#### `qb_get_customer`
Get customer details by ID.

**Parameters:**
- `customer_id` (required): Customer ID

#### `qb_query_customers`
Query customers using SQL syntax.

**Parameters:**
- `query`: SQL query string (default: "SELECT * FROM Customer")

**Example:**
```json
{
  "query": "SELECT * FROM Customer WHERE Active = true"
}
```

---

### 🧾 Invoice Management

#### `qb_create_invoice`
Create a new invoice.

**Parameters:**
- `CustomerRef` (required): Customer reference object
- `Line` (required): Array of line items
- `TxnDate`: Transaction date (YYYY-MM-DD)
- `DueDate`: Due date (YYYY-MM-DD)
- `CustomerMemo`: Message to customer
- `BillEmail`: Email address for invoice

**Example:**
```json
{
  "CustomerRef": { "value": "123" },
  "Line": [{
    "Amount": 500.00,
    "DetailType": "SalesItemLineDetail",
    "SalesItemLineDetail": {
      "ItemRef": { "value": "1" },
      "Qty": 10,
      "UnitPrice": 50.00
    }
  }],
  "DueDate": "2026-03-15"
}
```

#### `qb_get_invoice`
Get invoice by ID.

**Parameters:**
- `invoice_id` (required): Invoice ID

#### `qb_send_invoice`
Send invoice via email.

**Parameters:**
- `invoice_id` (required): Invoice ID
- `email` (required): Recipient email address

#### `qb_query_invoices`
Query invoices using SQL syntax.

**Parameters:**
- `query`: SQL query string

**Example:**
```json
{
  "query": "SELECT * FROM Invoice WHERE Balance > 0"
}
```

---

### 📦 Item/Product Management

#### `qb_create_item`
Create a new product or service item.

**Parameters:**
- `Name` (required): Item name
- `Type` (required): Item type (Service, Inventory, NonInventory)
- `Description`: Item description
- `UnitPrice`: Sales price
- `IncomeAccountRef`: Income account reference
- `ExpenseAccountRef`: Expense account reference (for inventory)
- `QtyOnHand`: Quantity on hand (for inventory)

**Example:**
```json
{
  "Name": "Consulting Services",
  "Type": "Service",
  "UnitPrice": 150.00,
  "IncomeAccountRef": { "value": "79" }
}
```

#### `qb_get_item`
Get item by ID.

**Parameters:**
- `item_id` (required): Item ID

#### `qb_query_items`
Query items using SQL syntax.

**Parameters:**
- `query`: SQL query string

---

### 💰 Payment Processing

#### `qb_create_payment`
Record a payment received.

**Parameters:**
- `CustomerRef` (required): Customer reference
- `TotalAmt` (required): Total payment amount
- `TxnDate`: Transaction date
- `Line`: Array of payment line items linking to invoices
- `PaymentMethodRef`: Payment method reference

**Example:**
```json
{
  "CustomerRef": { "value": "123" },
  "TotalAmt": 500.00,
  "Line": [{
    "Amount": 500.00,
    "LinkedTxn": [{
      "TxnId": "456",
      "TxnType": "Invoice"
    }]
  }]
}
```

#### `qb_query_payments`
Query payments using SQL syntax.

---

### 📊 Financial Reports

#### `qb_get_profit_loss`
Generate Profit & Loss report.

**Parameters:**
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)

**Example:**
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-31"
}
```

#### `qb_get_balance_sheet`
Generate Balance Sheet report.

**Parameters:**
- `date` (required): Report date (YYYY-MM-DD)

#### `qb_get_cash_flow`
Generate Cash Flow report.

**Parameters:**
- `start_date` (required): Start date
- `end_date` (required): End date

#### `qb_get_aged_receivables`
Generate Aged Receivables (A/R Aging) report.

**Parameters:** None

#### `qb_get_aged_payables`
Generate Aged Payables (A/P Aging) report.

**Parameters:** None

---

### 💼 Vendor & Bill Management

#### `qb_create_vendor`
Create a new vendor.

**Parameters:**
- `DisplayName` (required): Vendor display name
- `CompanyName`: Company name
- `PrimaryEmailAddr`: Email address object
- `PrimaryPhone`: Phone number object

#### `qb_create_bill`
Create a bill for a vendor.

**Parameters:**
- `VendorRef` (required): Vendor reference
- `Line` (required): Array of bill line items
- `TxnDate`: Transaction date
- `DueDate`: Due date

#### `qb_query_vendors`
Query vendors using SQL syntax.

---

### 📝 Estimates & Quotes

#### `qb_create_estimate`
Create a new estimate/quote.

**Parameters:**
- `CustomerRef` (required): Customer reference
- `Line` (required): Array of line items
- `TxnDate`: Transaction date
- `ExpirationDate`: Expiration date

#### `qb_query_estimates`
Query estimates using SQL syntax.

---

### 🛒 Purchase Orders

#### `qb_create_purchase_order`
Create a purchase order.

**Parameters:**
- `VendorRef` (required): Vendor reference
- `Line` (required): Array of PO line items

---

### 💵 Sales Receipts

#### `qb_create_sales_receipt`
Create a sales receipt (cash sale).

**Parameters:**
- `CustomerRef` (required): Customer reference
- `Line` (required): Array of line items
- `TxnDate`: Transaction date

---

### 🏦 Chart of Accounts

#### `qb_query_accounts`
Query chart of accounts.

**Parameters:**
- `query`: SQL query string

**Example:**
```json
{
  "query": "SELECT * FROM Account WHERE AccountType = 'Income'"
}
```

---

### 🏢 Company Information

#### `qb_get_company_info`
Get company information.

**Parameters:** None

---

### 🔍 Generic Query

#### `qb_query`
Execute any SQL query against QuickBooks entities.

**Parameters:**
- `query` (required): SQL query string

**Example:**
```json
{
  "query": "SELECT * FROM Customer WHERE Balance > 100 ORDER BY DisplayName"
}
```

**Supported Entities:**
Account, Bill, BillPayment, Class, CreditMemo, Customer, Department, Deposit, Employee, Estimate, Invoice, Item, JournalEntry, Payment, PaymentMethod, Purchase, PurchaseOrder, RefundReceipt, SalesReceipt, TaxCode, TaxRate, Term, TimeActivity, Transfer, Vendor, VendorCredit

---

### ⚡ Batch Operations

#### `qb_batch`
Execute multiple operations in a single batch request.

**Parameters:**
- `operations` (required): Array of batch operations

**Example:**
```json
{
  "operations": [
    {
      "bId": "bid1",
      "operation": "create",
      "entity": "Customer",
      "data": { "DisplayName": "Customer 1" }
    },
    {
      "bId": "bid2",
      "operation": "query",
      "query": "SELECT * FROM Invoice WHERE Balance > 0"
    }
  ]
}
```

## Usage Examples

### Create and Send an Invoice Workflow

```
1. First, create or find a customer:
   "Find customer with name 'Acme Corp' using qb_query_customers"

2. Create an invoice:
   "Create an invoice for customer ID 123 with consulting services 
    for 10 hours at $150/hour, due in 30 days"

3. Send the invoice:
   "Send invoice 456 to billing@acme.com"
```

### Financial Reporting Workflow

```
1. Get month-end reports:
   "Show me the profit and loss for January 2026"

2. Check cash flow:
   "What's the cash flow for last quarter?"

3. Review outstanding receivables:
   "Show me the aged receivables report"
```

### Inventory Management Workflow

```
1. Check low stock items:
   "Query items where quantity on hand is less than 10"

2. Create reorder purchase order:
   "Create a purchase order for vendor 789 to reorder low stock items"

3. Update item prices:
   "Update the price of item 'Widget Pro' to $299.99"
```

## SQL Query Syntax

QuickBooks uses a SQL-like query language:

### Basic Query
```sql
SELECT * FROM Customer WHERE Active = true
```

### With Conditions
```sql
SELECT * FROM Invoice WHERE Balance > 0 AND DueDate < '2026-03-01'
```

### Pattern Matching
```sql
SELECT * FROM Customer WHERE DisplayName LIKE '%Corp%'
```

### Ordering Results
```sql
SELECT * FROM Invoice ORDER BY TxnDate DESC
```

### Limiting Results
```sql
SELECT *, MAXRESULTS 50 FROM Customer
```

### Multiple Conditions
```sql
SELECT * FROM Item WHERE Type = 'Inventory' AND QtyOnHand < 10
```

## Error Handling

The skill provides detailed error messages:

- **Authentication Errors**: "Not authenticated. Please run qb_authenticate first."
- **API Errors**: Full QuickBooks error details with status codes
- **Validation Errors**: Missing required fields or invalid data
- **Rate Limit Errors**: "Too Many Requests - retry after delay"

## Configuration

All configuration is stored in `config.json`. This file contains both your app credentials (Client ID and Secret) and the OAuth tokens that are saved after authentication.

### API Environment

The skill supports both Sandbox and Production environments via the `api_environment` setting in `config.json`:

- **sandbox** (default): QuickBooks Sandbox API for development and testing
- **production**: QuickBooks Production API for live company data (requires app verification)

To switch environments, update `config.json`:
```json
{
  "api_environment": "sandbox"  // or "production"
}
```

**Important**: Production mode requires your app to be verified by Intuit. Start with sandbox for development.

### Security Considerations

⚠️ **Credential Storage**: This skill stores OAuth tokens and client secrets in plaintext in `config.json` on your local filesystem. To enhance security:

- Set restrictive file permissions on `config.json` (read/write for owner only)
- Never commit `config.json` to version control (included in `.gitignore`)
- Store the skill directory in a secure location
- Regularly rotate your client secrets in the QuickBooks Developer Portal
- Consider encrypting your disk or using a secure secret management solution
- Do not enable `autoStart` until you've verified the skill behaves as expected

## Rate Limits

- **Sandbox**: 500 requests/minute per app
- **Production**: Varies by subscription (500-1000/minute)

The skill automatically handles rate limiting with proper error messages.

## Security

- OAuth2 authentication (no password storage)
- Tokens stored in `config.json` (excluded from git)
- Automatic token refresh
- Secure HTTPS API communication
- No credentials in code

## Troubleshooting

### "Not authenticated" Error
Run `qb_authenticate` with your credentials.

### "Token refresh failed"
Delete `config.json` and re-authenticate.

### "Invalid redirect URI"
Ensure redirect URI in config matches your QuickBooks app settings.

### Port 3000 Already in Use
Change port in code or kill the process using port 3000.

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Documentation

- [README.md](README.md) - Complete setup guide
- [EXAMPLES.md](EXAMPLES.md) - 50+ practical examples
- [API_REFERENCE.md](API_REFERENCE.md) - Full API documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [CHANGELOG.md](CHANGELOG.md) - Version history

## Support

- [QuickBooks Developer Portal](https://developer.intuit.com)
- [QuickBooks Developer Forum](https://help.developer.intuit.com/s/)
- [API Documentation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [API Status](https://status.developer.intuit.com/)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly in sandbox
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Version

**Current Version**: 1.0.1  
**Last Updated**: February 21, 2026  
**Node.js Required**: 18.0.0+

## Tags

`accounting` `quickbooks` `invoicing` `payments` `financial-reporting` `bookkeeping` `erp` `business` `intuit` `api-integration` `mcp-skill` `openclaw`

---

**Ready to use!** Run `npm install` and authenticate to get started.
