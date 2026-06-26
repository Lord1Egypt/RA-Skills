# QuickBooks API Skill for OpenClaw

A comprehensive QuickBooks Online API integration skill for OpenClaw, providing full access to QuickBooks accounting features.

## Features

### 🔐 Authentication
- OAuth2 authentication flow with automatic token refresh
- Secure credential storage
- Automatic browser-based authorization

### 📊 Customer Management
- Create, read, and query customers
- Manage customer details and contact information
- Search customers with SQL-like queries

### 🧾 Invoice Operations
- Create and manage invoices
- Send invoices via email
- Query invoice history
- Track invoice status

### 📦 Inventory & Items
- Create and manage products/services
- Track inventory items
- Manage pricing and descriptions
- Support for Service, Inventory, and Non-Inventory items

### 💰 Payment Processing
- Record customer payments
- Link payments to invoices
- Query payment history

### 📈 Financial Reports
- Profit & Loss statements
- Balance Sheet reports
- Cash Flow reports
- Aged Receivables (A/R Aging)
- Aged Payables (A/P Aging)

### 🏢 Vendor Management
- Create and manage vendors
- Create bills for vendors
- Track vendor payments

### 📝 Estimates & Quotes
- Create estimates/quotes
- Convert estimates to invoices
- Track estimate status

### 🛒 Purchase Orders
- Create purchase orders
- Track PO status

### 💵 Sales Receipts
- Create cash sale receipts
- Record immediate payments

### 🔍 Advanced Features
- Generic SQL-like queries for any entity
- Batch operations for multiple requests
- Complete Chart of Accounts access
- Tax code and rate management
- Company information retrieval

## Prerequisites

1. **Node.js** (v18 or higher)
2. **QuickBooks Developer Account**
   - Sign up at [https://developer.intuit.com](https://developer.intuit.com)
3. **QuickBooks App**
   - Create an app in the Intuit Developer Portal
   - Enable QuickBooks Online API scope

## Setup Instructions

### Step 1: Create QuickBooks Developer App

1. Go to [Intuit Developer Portal](https://developer.intuit.com)
2. Sign in and navigate to "My Apps"
3. Click "Create an app" and select "QuickBooks Online and Payments"
4. Fill in your app details:
   - **App name**: Choose a name for your app
   - **Redirect URI**: `http://localhost:3001/callback` (must match exactly)
5. After creating the app, note your:
   - **Client ID**
   - **Client Secret**
6. Under "Keys & credentials", make sure you're in the right environment:
   - **Sandbox**: For testing (recommended to start)
   - **Production**: For live data

### Step 2: Install Dependencies

```bash
cd "c:\Users\Shaun\Desktop\Quickbooks skill"
npm install
```

### Step 3: Configure Authentication

Create a `config.json` file from the template:

```bash
cp config.json.template config.json
```

Edit `config.json` and add your credentials:

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

### Step 4: Authenticate with QuickBooks

The skill uses OAuth2 for authentication. The first time you run any QuickBooks operation, you'll need to authenticate:

1. The authentication process will:
   - Start a local web server on port 3001
   - Open your default browser
   - Redirect to QuickBooks authorization page
   - Capture the auth code and exchange it for tokens
   - Save tokens to `config.json`

2. After successful authentication, all subsequent API calls will use the saved tokens
3. Tokens are automatically refreshed when they expire

## OpenClaw Integration

### Add to OpenClaw Configuration

Add this skill to your OpenClaw configuration file (typically `~/.config/openclaw/config.json` or similar):

```json
{
  "mcpServers": {
    "quickbooks": {
      "command": "node",
      "args": ["c:/Users/Shaun/Desktop/Quickbooks skill/run.js"],
      "env": {}
    }
  }
}
```

## Usage with OpenClaw

Once installed and configured, the skill will be automatically available in OpenClaw. All QuickBooks tools will appear in your available skill set.

Restart OpenClaw after installation to load the skill.

## Usage Examples

### Authentication

First, authenticate with QuickBooks:

```
Use the qb_authenticate tool with your client_id and client_secret
```

The tool will open a browser for you to authorize the app. After authorization, tokens are saved automatically.

### Create a Customer

```
Use qb_create_customer with:
{
  "DisplayName": "John Doe",
  "PrimaryEmailAddr": {
    "Address": "john@example.com"
  },
  "PrimaryPhone": {
    "FreeFormNumber": "555-1234"
  }
}
```

### Create an Invoice

```
Use qb_create_invoice with:
{
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
  "DueDate": "2026-03-15",
  "TxnDate": "2026-02-21"
}
```

### Query Customers

```
Use qb_query_customers with:
{
  "query": "SELECT * FROM Customer WHERE DisplayName LIKE '%John%'"
}
```

### Get Profit & Loss Report

```
Use qb_get_profit_loss with:
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-31"
}
```

### Send an Invoice

```
Use qb_send_invoice with:
{
  "invoice_id": "123",
  "email": "customer@example.com"
}
```

## Available Tools

### Authentication
- `qb_authenticate` - Initiate OAuth2 flow
- `qb_exchange_token` - Exchange auth code for tokens (handled automatically)

### Customers
- `qb_create_customer` - Create a new customer
- `qb_get_customer` - Get customer by ID
- `qb_query_customers` - Query customers with SQL

### Invoices
- `qb_create_invoice` - Create a new invoice
- `qb_get_invoice` - Get invoice by ID
- `qb_send_invoice` - Email an invoice
- `qb_query_invoices` - Query invoices with SQL

### Items
- `qb_create_item` - Create product/service item
- `qb_get_item` - Get item by ID
- `qb_query_items` - Query items with SQL

### Payments
- `qb_create_payment` - Record a payment
- `qb_query_payments` - Query payments with SQL

### Estimates
- `qb_create_estimate` - Create an estimate/quote
- `qb_query_estimates` - Query estimates with SQL

### Vendors & Bills
- `qb_create_vendor` - Create a vendor
- `qb_create_bill` - Create a bill
- `qb_query_vendors` - Query vendors with SQL

### Reports
- `qb_get_profit_loss` - Profit & Loss report
- `qb_get_balance_sheet` - Balance Sheet report
- `qb_get_cash_flow` - Cash Flow report
- `qb_get_aged_receivables` - A/R Aging report
- `qb_get_aged_payables` - A/P Aging report

### Accounts
- `qb_query_accounts` - Query chart of accounts

### Purchase Orders
- `qb_create_purchase_order` - Create a PO

### Sales Receipts
- `qb_create_sales_receipt` - Create a cash sale receipt

### Other
- `qb_get_company_info` - Get company information
- `qb_query` - Execute any SQL query
- `qb_batch` - Execute multiple operations in one request

## SQL Query Syntax

QuickBooks uses a SQL-like query language. Examples:

```sql
-- Get all active customers
SELECT * FROM Customer WHERE Active = true

-- Get invoices for a specific customer
SELECT * FROM Invoice WHERE CustomerRef = '123'

-- Get items with price greater than 50
SELECT * FROM Item WHERE UnitPrice > 50

-- Get recent transactions
SELECT * FROM Invoice WHERE TxnDate > '2026-01-01' ORDER BY TxnDate DESC

-- Get customers with email
SELECT * FROM Customer WHERE PrimaryEmailAddr IS NOT NULL
```

Supported entities for queries:
- Account
- Bill
- Customer
- Estimate
- Invoice
- Item
- Payment
- Purchase
- PurchaseOrder
- SalesReceipt
- Vendor
- And many more...

## Error Handling

The skill includes comprehensive error handling:

- **Authentication Errors**: Clear messages when tokens are invalid or expired
- **API Errors**: Detailed QuickBooks API error messages
- **Validation Errors**: Client-side validation of required fields
- **Rate Limiting**: Automatic retry with exponential backoff (if needed)

## API Environment Configuration

The skill supports both Sandbox and Production environments:

### Sandbox (Default)
For testing and development. Configured automatically when you authenticate.

```json
{
  "api_environment": "sandbox"
}
```

### Production
For live company data. Requires Intuit app verification.

```json
{
  "api_environment": "production"
}
```

**Switching Environments:**
1. Update `api_environment` in `config.json`
2. Re-authenticate with `qb_authenticate` using production credentials
3. Verify you're using production Client ID and Secret from QuickBooks Developer Portal

## Security Best Practices

⚠️ **Important Security Considerations**

This skill stores sensitive credentials in plaintext in `config.json`. Before using in production:

1. **File Permissions** - Restrict `config.json` to owner read/write only:
   - Windows: Right-click → Properties → Security → Advanced
   - Linux/Mac: `chmod 600 config.json`

2. **Never Commit Credentials** - Ensure `config.json` is in `.gitignore`

3. **Secure Storage Location** - Store the skill in a protected directory

4. **Regular Credential Rotation** - Rotate client secrets monthly in QuickBooks Developer Portal

5. **Audit Access** - Monitor who has access to the machine and skill directory

6. **Use Sandbox First** - Always test with sandbox before production

7. **Disable AutoStart** - Don't enable autoStart in OpenClaw until thoroughly tested

8. **HTTPS in Production** - Use HTTPS redirect URIs for production deployments

9. **Monitor Token Usage** - Refresh tokens expire after 100 days of inactivity

10. **Principle of Least Privilege** - Only grant QuickBooks scopes you actually need

## Troubleshooting

### "Not authenticated" Error
- Run the authentication flow first using `qb_authenticate`
- Make sure config.json exists and has valid credentials

### Token Refresh Failures
- Your refresh token may have expired (they last 100 days)
- Re-authenticate using `qb_authenticate`

### API Permission Errors
- Make sure your app has the correct scopes enabled
- Check that you're using the right environment (sandbox vs production)

### Browser Doesn't Open
- Manually visit the authorization URL provided in the output
- Make sure port 3001 is available

### Port 3001 Already in Use
- Kill the process using port 3001
- Or change to a different port in:
  - Your QuickBooks app settings (redirect URI)
  - Your `config.json` (redirect_uri)
  - The `run.js` code (server port)

### Wrong API Environment
- Check `api_environment` in `config.json` matches your intent (sandbox vs production)
- Production requires verified app - use sandbox for development
- After changing environment, re-authenticate with matching credentials

## Development

### Testing

```bash
# Install dependencies
npm install

# Run the skill
node run.js
```

### Debugging

Enable debug logging by setting:

```bash
export DEBUG=quickbooks:*
node run.js
```

## API Rate Limits

QuickBooks has API rate limits:
- **Sandbox**: 500 requests per app per minute
- **Production**: Varies by subscription level

The skill handles rate limiting gracefully with automatic retries.

## References

- [QuickBooks API Documentation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [QuickBooks Workflows](https://developer.intuit.com/app/developer/qbo/docs/workflows)
- [OAuth2 Guide](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0)
- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)

## License

MIT

## Support

For issues and questions:
1. Check the [QuickBooks Developer Forum](https://help.developer.intuit.com/s/)
2. Review the API documentation
3. Open an issue in this repository

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Changelog

### Version 1.0.1 - 2026-02-21
**Security & Configuration Update**

- ✅ Fixed port mismatch: Standardized all documentation to port 3001
- ✅ Made API environment configurable: Added `api_environment` setting (sandbox/production)
- ✅ Removed unused dependency: Cleaned up @modelcontextprotocol/sdk reference
- ✅ Enhanced security documentation: Added credential storage warnings and best practices
- ✅ Updated configuration template with api_environment field
- ✅ Fixed run.js to dynamically select API endpoint based on configuration

### Version 1.0.0 - 2026-02-21
- Initial release
- Full OAuth2 authentication
- Complete CRUD operations for all major entities
- Financial reporting
- Batch operations
- SQL query support
