# QuickBooks API Skill - Complete API Reference

## Entity Relationships

```
┌─────────────┐
│  Customer   │────┐
└─────────────┘    │
                   ├──► Invoice ──► Payment
┌─────────────┐    │      │
│    Item     │────┤      │
└─────────────┘    │      └──► SalesReceipt
                   │
┌─────────────┐    └──► Estimate
│   Account   │
└─────────────┘

┌─────────────┐
│   Vendor    │────► Bill ──► BillPayment
└─────────────┘    │
                   └──► PurchaseOrder
```

## Core Entities

### Customer

**Fields:**
- `DisplayName` (required) - Customer name
- `Title` - Title (Mr., Mrs., etc.)
- `GivenName` - First name
- `MiddleName` - Middle name
- `FamilyName` - Last name
- `Suffix` - Name suffix (Jr., Sr., etc.)
- `CompanyName` - Company name
- `PrimaryEmailAddr.Address` - Email address
- `PrimaryPhone.FreeFormNumber` - Phone number
- `Mobile.FreeFormNumber` - Mobile number
- `Fax.FreeFormNumber` - Fax number
- `WebAddr.URI` - Website URL
- `BillAddr` - Billing address object
  - `Line1`, `Line2`, `Line3`, `Line4`, `Line5`
  - `City`
  - `CountrySubDivisionCode` (State/Province)
  - `PostalCode`
  - `Country`
- `ShipAddr` - Shipping address (same structure as BillAddr)
- `Notes` - Customer notes
- `Active` - Boolean, customer status
- `Balance` - Current balance (read-only)
- `BalanceWithJobs` - Balance including jobs (read-only)
- `PreferredDeliveryMethod` - Email, Print, or None
- `ResaleNum` - Resale number
- `PaymentMethodRef` - Default payment method
- `TermRef` - Payment terms reference

**Query Examples:**
```sql
SELECT * FROM Customer WHERE Active = true
SELECT * FROM Customer WHERE Balance > 0
SELECT * FROM Customer WHERE DisplayName LIKE '%ACME%'
SELECT Id, DisplayName, Balance FROM Customer ORDER BY Balance DESC
```

### Invoice

**Fields:**
- `CustomerRef.value` (required) - Customer ID
- `Line` (required) - Array of line items
  - `Amount` (required)
  - `DetailType` - Usually "SalesItemLineDetail"
  - `Description`
  - `SalesItemLineDetail`
    - `ItemRef.value` (required) - Item ID
    - `Qty` - Quantity
    - `UnitPrice` - Price per unit
    - `TaxCodeRef.value` - Tax code
    - `DiscountAmt` - Discount amount
- `TxnDate` - Transaction date (YYYY-MM-DD)
- `DueDate` - Due date (YYYY-MM-DD)
- `DocNumber` - Invoice number (auto-generated if omitted)
- `PrivateNote` - Internal note
- `CustomerMemo.value` - Message to customer
- `BillEmail.Address` - Email for sending invoice
- `BillEmailCc.Address` - CC email address
- `BillEmailBcc.Address` - BCC email address
- `ShipAddr` - Shipping address
- `BillAddr` - Billing address
- `TxnTaxDetail` - Tax details
- `SalesTermRef` - Payment terms
- `ShipMethodRef` - Shipping method
- `ShipDate` - Ship date
- `TrackingNum` - Tracking number
- `TotalAmt` (read-only) - Total amount
- `Balance` (read-only) - Remaining balance
- `EmailStatus` - Email status (read-only)
- `PrintStatus` - Print status

**Query Examples:**
```sql
SELECT * FROM Invoice WHERE Balance > 0
SELECT * FROM Invoice WHERE DueDate < '2026-02-21' AND Balance > 0
SELECT * FROM Invoice WHERE CustomerRef = '123'
SELECT Id, DocNumber, TotalAmt, Balance FROM Invoice ORDER BY TxnDate DESC
SELECT * FROM Invoice WHERE TxnDate >= '2026-01-01' AND TxnDate <= '2026-01-31'
```

### Item

**Types:** Service, Inventory, NonInventory, Category, Group

**Common Fields:**
- `Name` (required) - Item name
- `Type` (required) - Item type
- `Description` - Item description
- `Active` - Boolean, item status
- `UnitPrice` - Sales price
- `PurchaseCost` - Purchase cost
- `QtyOnHand` - Quantity (Inventory only)
- `InvStartDate` - Inventory start date (required for Inventory)
- `IncomeAccountRef.value` - Income account
- `ExpenseAccountRef.value` - Expense account (Inventory/NonInventory)
- `AssetAccountRef.value` - Asset account (Inventory only)
- `TrackQtyOnHand` - Boolean, track inventory (Inventory only)
- `Taxable` - Boolean, item is taxable
- `SalesTaxCodeRef.value` - Sales tax code

**Query Examples:**
```sql
SELECT * FROM Item WHERE Active = true ORDER BY Name
SELECT * FROM Item WHERE Type = 'Inventory'
SELECT * FROM Item WHERE QtyOnHand < 10
SELECT Name, UnitPrice, QtyOnHand FROM Item WHERE Type = 'Inventory'
```

### Payment

**Fields:**
- `CustomerRef.value` (required) - Customer ID
- `TotalAmt` (required) - Total payment amount
- `TxnDate` - Transaction date
- `Line` - Array of line items
  - `Amount` - Amount applied
  - `LinkedTxn` - Array of linked transactions
    - `TxnId` - Transaction ID (usually Invoice)
    - `TxnType` - Transaction type (usually "Invoice")
- `PaymentMethodRef.value` - Payment method
- `PaymentRefNum` - Check number or reference
- `DepositToAccountRef.value` - Deposit account
- `PrivateNote` - Internal note
- `UnappliedAmt` (read-only) - Unapplied amount
- `ProcessPayment` - Boolean, process payment (for credit cards)

**Query Examples:**
```sql
SELECT * FROM Payment WHERE TxnDate >= '2026-01-01'
SELECT * FROM Payment WHERE CustomerRef = '123'
SELECT Id, TxnDate, TotalAmt, UnappliedAmt FROM Payment ORDER BY TxnDate DESC
```

### Estimate

**Fields:**
Similar to Invoice, but represents a quote/estimate rather than an actual sale.

- `CustomerRef.value` (required)
- `Line` (required) - Same structure as Invoice
- `TxnDate` - Estimate date
- `ExpirationDate` - Expiration date
- `AcceptedBy` - Name of person who accepted
- `AcceptedDate` - Date accepted
- `TxnStatus` - Accepted, Closed, Pending, Rejected
- `CustomerMemo.value` - Message to customer
- `EmailStatus` (read-only)
- `TotalAmt` (read-only)

**Query Examples:**
```sql
SELECT * FROM Estimate WHERE TxnStatus = 'Pending'
SELECT * FROM Estimate WHERE CustomerRef = '123'
SELECT * FROM Estimate WHERE ExpirationDate < '2026-02-21' AND TxnStatus = 'Pending'
```

### Vendor

**Fields:**
- `DisplayName` (required) - Vendor name
- `CompanyName` - Company name
- `Title`, `GivenName`, `MiddleName`, `FamilyName`, `Suffix`
- `PrimaryEmailAddr.Address` - Email
- `PrimaryPhone.FreeFormNumber` - Phone
- `Mobile.FreeFormNumber` - Mobile
- `Fax.FreeFormNumber` - Fax
- `WebAddr.URI` - Website
- `BillAddr` - Address object (same structure as Customer)
- `Active` - Boolean, vendor status
- `Balance` - Current balance (read-only)
- `AcctNum` - Account number
- `Vendor1099` - Boolean, if vendor receives 1099
- `TaxIdentifier` - Tax ID/SSN
- `TermRef` - Payment terms

**Query Examples:**
```sql
SELECT * FROM Vendor WHERE Active = true ORDER BY DisplayName
SELECT * FROM Vendor WHERE Balance > 0
SELECT * FROM Vendor WHERE Vendor1099 = true
```

### Bill

**Fields:**
- `VendorRef.value` (required) - Vendor ID
- `Line` (required) - Array of line items
  - `Amount` (required)
  - `DetailType` - Usually "AccountBasedExpenseLineDetail" or "ItemBasedExpenseLineDetail"
  - `Description`
  - `AccountBasedExpenseLineDetail`
    - `AccountRef.value` - Expense account ID
    - `TaxCodeRef.value` - Tax code
  - `ItemBasedExpenseLineDetail`
    - `ItemRef.value` - Item ID
    - `Qty` - Quantity
    - `UnitPrice` - Price per unit
- `TxnDate` - Transaction date
- `DueDate` - Due date
- `DocNumber` - Bill number
- `PrivateNote` - Internal note
- `APAccountRef.value` - Accounts Payable account
- `TotalAmt` (read-only)
- `Balance` (read-only)

**Query Examples:**
```sql
SELECT * FROM Bill WHERE Balance > 0
SELECT * FROM Bill WHERE DueDate < '2026-02-21' AND Balance > 0
SELECT * FROM Bill WHERE VendorRef = '789'
```

### Account

**Types:** Bank, Accounts Receivable, Other Current Asset, Fixed Asset, Other Asset, Accounts Payable, Credit Card, Other Current Liability, Long Term Liability, Equity, Income, Cost of Goods Sold, Expense, Other Income, Other Expense

**Fields:**
- `Name` (required) - Account name
- `AccountType` (required) - Account type from list above
- `AccountSubType` - Specific subtype
- `Description` - Account description
- `Active` - Boolean, account status
- `CurrentBalance` (read-only) - Current balance
- `CurrentBalanceWithSubAccounts` (read-only)
- `AcctNum` - Account number
- `SubAccount` - Boolean, is sub-account
- `ParentRef.value` - Parent account ID (if sub-account)

**Query Examples:**
```sql
SELECT * FROM Account WHERE Active = true ORDER BY Name
SELECT * FROM Account WHERE AccountType = 'Income'
SELECT * FROM Account WHERE AccountType = 'Expense'
SELECT * FROM Account WHERE AccountType = 'Bank'
SELECT Name, AccountType, CurrentBalance FROM Account WHERE CurrentBalance != 0
```

### SalesReceipt

**Fields:**
Similar to Invoice, but represents an immediate cash sale.

- `CustomerRef.value` (required)
- `Line` (required) - Same structure as Invoice
- `TxnDate` - Transaction date
- `PaymentMethodRef.value` - Payment method
- `PaymentRefNum` - Check/reference number
- `DepositToAccountRef.value` - Deposit account
- `CustomerMemo.value` - Message to customer
- `PrivateNote` - Internal note
- `TotalAmt` (read-only)

**Query Examples:**
```sql
SELECT * FROM SalesReceipt WHERE TxnDate >= '2026-01-01'
SELECT * FROM SalesReceipt WHERE CustomerRef = '123'
SELECT * FROM SalesReceipt WHERE PaymentMethodRef = '1'
```

### PurchaseOrder

**Fields:**
- `VendorRef.value` (required) - Vendor ID
- `Line` (required) - Array of line items
  - `Amount` (required)
  - `DetailType` - Usually "ItemBasedExpenseLineDetail"
  - `Description`
  - `ItemBasedExpenseLineDetail`
    - `ItemRef.value` - Item ID
    - `Qty` - Quantity
    - `UnitPrice` - Price per unit
- `TxnDate` - Transaction date
- `DueDate` - Expected delivery date
- `DocNumber` - PO number
- `ShipAddr` - Shipping address
- `ShipMethodRef` - Shipping method
- `POStatus` - Open, Closed
- `POEmail.Address` - Email to send PO
- `TotalAmt` (read-only)

**Query Examples:**
```sql
SELECT * FROM PurchaseOrder WHERE POStatus = 'Open'
SELECT * FROM PurchaseOrder WHERE VendorRef = '789'
SELECT * FROM PurchaseOrder WHERE TxnDate >= '2026-01-01'
```

## Report Types

### ProfitAndLoss
**Parameters:**
- `start_date` (required) - Start date (YYYY-MM-DD)
- `end_date` (required) - End date (YYYY-MM-DD)
- `accounting_method` - Cash or Accrual
- `summarize_column_by` - Total, Month, Quarter, Year

### BalanceSheet
**Parameters:**
- `date` (required) - Report date (YYYY-MM-DD)
- `accounting_method` - Cash or Accrual

### CashFlow
**Parameters:**
- `start_date` (required) - Start date
- `end_date` (required) - End date
- `accounting_method` - Cash or Accrual

### AgedReceivables
**Parameters:**
- `report_date` - As of date
- `aging_method` - Report Basis, Current
- `num_periods` - Number of aging periods (default: 4)
- `aging_period` - Number of days in each period (default: 30)

### AgedPayables
**Parameters:**
Same as AgedReceivables

## Query Language (SQL-like)

### Syntax
```sql
SELECT [fields] FROM [Entity] WHERE [conditions] ORDER BY [field] [ASC|DESC]
```

### Operators
- `=` Equal
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `<>` or `!=` Not equal
- `LIKE` Pattern matching (use `%` wildcard)
- `IN` Match any value in list
- `AND` Logical AND
- `OR` Logical OR

### Examples

**Select specific fields:**
```sql
SELECT Id, DisplayName, Balance FROM Customer
```

**Where clause:**
```sql
SELECT * FROM Invoice WHERE Balance > 0 AND DueDate < '2026-02-21'
```

**Pattern matching:**
```sql
SELECT * FROM Customer WHERE DisplayName LIKE '%Corp%'
```

**In clause:**
```sql
SELECT * FROM Item WHERE Type IN ('Service', 'Inventory')
```

**Order by:**
```sql
SELECT * FROM Customer ORDER BY Balance DESC
```

**Complex conditions:**
```sql
SELECT * FROM Invoice 
WHERE (Balance > 0 AND DueDate < '2026-02-21') 
   OR (TotalAmt > 1000 AND EmailStatus = 'NotSent')
ORDER BY DueDate ASC
```

### Queryable Entities

Full list of entities you can query:

- Account
- Bill
- BillPayment
- Class
- CreditMemo
- Customer
- Department
- Deposit
- Employee
- Estimate
- Invoice
- Item
- JournalEntry
- Payment
- PaymentMethod
- Purchase
- PurchaseOrder
- RefundReceipt
- SalesReceipt
- TaxCode
- TaxRate
- Term
- TimeActivity
- Transfer
- Vendor
- VendorCredit

## Error Codes

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid/expired token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (entity doesn't exist)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable

### QuickBooks Error Types

**ValidationFault:**
- Missing required fields
- Invalid field values
- Invalid references

**AuthenticationFault:**
- Invalid or expired access token
- Invalid company/realm ID

**AuthorizationFault:**
- Insufficient permissions
- Feature not enabled for account

**ServiceException:**
- Internal QuickBooks error
- Try again later

## Rate Limits

### Sandbox
- 500 requests per minute per app
- 100 requests per minute per user (across all apps)

### Production
Varies by subscription:
- **QuickBooks Online Plus**: 500 requests/minute
- **QuickBooks Online Advanced**: 1000 requests/minute

**Rate Limit Headers:**
```
intuit_tid: [transaction ID]
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 499
X-RateLimit-Reset: 1234567890
```

## Authentication Flow

### 1. Authorization URL
```
https://appcenter.intuit.com/connect/oauth2?
  client_id=[CLIENT_ID]&
  redirect_uri=[REDIRECT_URI]&
  response_type=code&
  scope=com.intuit.quickbooks.accounting&
  state=[RANDOM_STATE]
```

### 2. Exchange Code for Token
```
POST https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
Authorization: Basic [BASE64(client_id:client_secret)]
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=[AUTH_CODE]&
redirect_uri=[REDIRECT_URI]
```

### 3. Refresh Token
```
POST https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
Authorization: Basic [BASE64(client_id:client_secret)]
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=[REFRESH_TOKEN]
```

### Token Lifetimes
- **Access Token**: 1 hour
- **Refresh Token**: 100 days (renewable)

## Best Practices

### 1. Error Handling
Always wrap API calls in try-catch and handle specific error types.

### 2. Token Management
- Refresh tokens proactively (don't wait for expiration)
- Store tokens securely
- Implement token refresh logic

### 3. Data Validation
- Validate input before sending to API
- Check for required references
- Ensure dates are in correct format

### 4. Performance
- Use batch operations when possible
- Cache reference data (accounts, items)
- Use specific queries instead of SELECT *
- Implement pagination for large result sets

### 5. Idempotency
- Store transaction IDs to prevent duplicates
- Use unique DocNumbers for invoices
- Implement retry logic with exponential backoff

### 6. Testing
- Always test in Sandbox first
- Create test data for different scenarios
- Test error conditions

### 7. Webhooks
Consider using webhooks for:
- Real-time updates
- Change notifications
- Event-driven architecture

## Environment Differences

### Sandbox
- Test environment with sample data
- No real financial impact
- Can create unlimited test companies
- Same API as production

### Production
- Real customer data
- Real financial transactions
- Requires approval and review
- Company limit based on subscription

## Additional Resources

- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account)
- [Webhooks Documentation](https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks)
- [Sample Apps](https://developer.intuit.com/app/developer/qbo/docs/get-started/start-developing-your-app)
- [Developer Forum](https://help.developer.intuit.com/s/)
