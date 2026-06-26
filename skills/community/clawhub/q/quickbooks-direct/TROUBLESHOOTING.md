# QuickBooks API Skill - Troubleshooting Guide

## Quick Diagnostics Checklist

- [ ] Node.js version 18+ installed (`node --version`)
- [ ] Dependencies installed (`npm install`)
- [ ] config.json file exists with credentials
- [ ] QuickBooks Developer app created
- [ ] Redirect URI matches in app and config
- [ ] Successfully completed OAuth flow
- [ ] Access token not expired

## Common Issues & Solutions

### 1. Authentication Issues

#### Problem: "Not authenticated. Please run qb_authenticate first."

**Cause:** No valid config.json file found or missing credentials.

**Solution:**
```bash
# 1. Copy template
cp config.json.template config.json

# 2. Edit config.json with your credentials
# Add your client_id and client_secret from QuickBooks Developer Portal

# 3. Run authentication
# Use qb_authenticate tool through OpenClaw
```

---

#### Problem: "Token refresh failed: 401 Unauthorized"

**Cause:** Refresh token has expired (they last 100 days) or invalid credentials.

**Solution:**
```bash
# 1. Delete existing config
rm config.json

# 2. Copy template again
cp config.json.template config.json

# 3. Add credentials and re-authenticate
# Use qb_authenticate tool
```

---

#### Problem: Browser doesn't open during authentication

**Cause:** System cannot open default browser or display server issue.

**Solution:**
1. Copy the authorization URL from the console output
2. Manually paste it into your browser
3. Complete the authorization
4. You'll be redirected to localhost:3000/callback
5. The process should complete automatically

---

#### Problem: "Invalid redirect URI"

**Cause:** Redirect URI in config.json doesn't match QuickBooks app settings.

**Solution:**
1. Go to [Intuit Developer Portal](https://developer.intuit.com)
2. Open your app
3. Go to "Keys & credentials"
4. Check "Redirect URIs"
5. Ensure `http://localhost:3000/callback` is listed
6. Update config.json to match exactly

---

### 2. API Errors

#### Problem: "QuickBooks API Error: 400 - Validation error"

**Cause:** Missing required fields or invalid data format.

**Solution:**
```javascript
// Check your request has all required fields:
// For Customer: DisplayName is required
// For Invoice: CustomerRef and Line are required
// For Item: Name and Type are required

// Example of correct invoice structure:
{
  "CustomerRef": { "value": "123" },  // Note: nested "value"
  "Line": [{
    "Amount": 100.00,
    "DetailType": "SalesItemLineDetail",
    "SalesItemLineDetail": {
      "ItemRef": { "value": "1" }
    }
  }]
}
```

**Common validation errors:**
- Missing `value` in reference objects (should be `{"value": "123"}` not `"123"`)
- Wrong `DetailType` (use "SalesItemLineDetail" for invoices, not "ExpenseLineDetail")
- Dates in wrong format (must be "YYYY-MM-DD")
- Missing required nested objects

---

#### Problem: "QuickBooks API Error: 404 - Not Found"

**Cause:** Referenced entity doesn't exist (customer, item, account, etc.).

**Solution:**
```javascript
// 1. First verify the entity exists:
// Query to check if customer exists:
{
  "tool": "qb_query",
  "arguments": {
    "query": "SELECT * FROM Customer WHERE Id = '123'"
  }
}

// 2. If it doesn't exist, create it first
// 3. Then use the Id from the creation response
```

---

#### Problem: "QuickBooks API Error: 429 - Too Many Requests"

**Cause:** Hit rate limit (500 requests/minute in sandbox).

**Solution:**
- Implement exponential backoff in your code
- Use batch operations for multiple requests
- Cache frequently used data (items, accounts)
- Spread requests over time
- Consider upgrading production plan for higher limits

---

#### Problem: "Stale object error" when updating

**Cause:** Missing or incorrect `SyncToken` in update request.

**Solution:**
```javascript
// Always get the latest version first
{
  "tool": "qb_get_customer",
  "arguments": { "customer_id": "123" }
}

// Use the SyncToken from the response in your update
{
  "tool": "qb_update_customer",  // Note: Not yet implemented, use create with Id
  "arguments": {
    "Id": "123",
    "SyncToken": "5",  // From the get response
    "DisplayName": "Updated Name"
  }
}
```

---

### 3. Query Issues

#### Problem: "No results returned" from query

**Cause:** Incorrect SQL syntax or entity name.

**Solution:**
```sql
-- ❌ WRONG: Entity names must be singular
SELECT * FROM Customers

-- ✅ CORRECT: Entity is singular
SELECT * FROM Customer

-- ❌ WRONG: Missing quotes around string values
SELECT * FROM Customer WHERE DisplayName = John

-- ✅ CORRECT: Use single quotes
SELECT * FROM Customer WHERE DisplayName = 'John'

-- ❌ WRONG: Date comparison without quotes
SELECT * FROM Invoice WHERE TxnDate > 2026-01-01

-- ✅ CORRECT: Dates must be quoted
SELECT * FROM Invoice WHERE TxnDate > '2026-01-01'
```

---

#### Problem: "Invalid query error"

**Cause:** Using unsupported SQL features.

**Solution:**
```sql
-- QuickBooks SQL is limited. These are NOT supported:
-- ❌ Joins between entities (use separate queries)
-- ❌ Subqueries
-- ❌ GROUP BY
-- ❌ COUNT, SUM, AVG (use reports instead)
-- ❌ HAVING
-- ❌ LIMIT (use MAXRESULTS instead)

-- ✅ Supported:
SELECT * FROM Customer WHERE Active = true ORDER BY DisplayName
SELECT *, MAXRESULTS 10 FROM Invoice ORDER BY TxnDate DESC
SELECT Id, DisplayName FROM Customer WHERE Balance > 0
```

---

### 4. Connection Issues

#### Problem: "ECONNREFUSED" or "Network error"

**Cause:** Cannot connect to QuickBooks API servers.

**Solution:**
1. Check your internet connection
2. Verify you can reach https://quickbooks.api.intuit.com
3. Check firewall settings
4. Verify no proxy is blocking the connection
5. Try from a different network

---

#### Problem: Port 3000 already in use

**Cause:** Another application is using port 3000.

**Solution:**

**Option 1 - Use different port:**
```javascript
// In your QuickBooks app settings at developer.intuit.com:
// Change redirect URI to: http://localhost:3001/callback

// In config.json:
{
  "redirect_uri": "http://localhost:3001/callback"
}

// Then modify the code in run.js at line "app.listen(3000"
// Change to: app.listen(3001
```

**Option 2 - Kill process using port 3000:**
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process

# Or find and kill manually:
netstat -ano | findstr :3000
taskkill /PID [PID_NUMBER] /F
```

---

### 5. Data Issues

#### Problem: Invoice shows $0.00 total

**Cause:** Line items not properly structured or Amount calculation incorrect.

**Solution:**
```javascript
{
  "Line": [
    {
      // Amount must match Qty * UnitPrice
      "Amount": 100.00,  // This should be 2 * 50.00
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "ItemRef": { "value": "1" },
        "Qty": 2,
        "UnitPrice": 50.00
      }
    }
  ]
}
```

---

#### Problem: Cannot link payment to invoice

**Cause:** Incorrect LinkedTxn structure or invoice already paid.

**Solution:**
```javascript
// 1. First check invoice balance
{
  "tool": "qb_get_invoice",
  "arguments": { "invoice_id": "456" }
}

// 2. If balance > 0, create payment with correct structure:
{
  "tool": "qb_create_payment",
  "arguments": {
    "CustomerRef": { "value": "123" },
    "TotalAmt": 500.00,
    "Line": [{
      "Amount": 500.00,
      "LinkedTxn": [{
        "TxnId": "456",        // Invoice ID
        "TxnType": "Invoice"   // Must be exact
      }]
    }]
  }
}
```

---

### 6. OpenClaw Integration Issues

#### Problem: Skill not showing up in OpenClaw

**Cause:** Configuration file not updated or OpenClaw not restarted.

**Solution:**
1. Check your OpenClaw configuration file and ensure the path to run.js is correct.
2. Restart OpenClaw completely to load the skill.

---

#### Problem: "Cannot find module '@modelcontextprotocol/sdk'"

**Cause:** Dependencies not installed.

**Solution:**
```bash
cd "c:\Users\Shaun\Desktop\Quickbooks skill"
npm install
```

---

#### Problem: Tool calls timing out

**Cause:** Large queries or slow API responses.

**Solution:**
- Use more specific queries (avoid `SELECT *`)
- Add MAXRESULTS to limit rows: `SELECT *, MAXRESULTS 50 FROM Customer`
- Break large batch operations into smaller chunks
- Increase timeout in OpenClaw configuration if available

---

### 7. Environment Issues

#### Problem: Different results in sandbox vs production

**Cause:** Using sandbox credentials with production data or vice versa.

**Solution:**
1. Verify you're using the correct credentials:
   - Sandbox: Keys from "Development" tab
   - Production: Keys from "Production" tab

2. Ensure realm_id matches the environment:
   - Sandbox companies have different realm IDs than production

3. Check company info to verify:
```javascript
{
  "tool": "qb_get_company_info",
  "arguments": {}
}
```

---

### 8. Report Issues

#### Problem: Report returns no data

**Cause:** Date range has no transactions or wrong date format.

**Solution:**
```javascript
// ✅ Correct date format:
{
  "tool": "qb_get_profit_loss",
  "arguments": {
    "start_date": "2026-01-01",  // YYYY-MM-DD
    "end_date": "2026-01-31"
  }
}

// Also check if company has data in that date range:
{
  "tool": "qb_query",
  "arguments": {
    "query": "SELECT COUNT(*) FROM Invoice WHERE TxnDate >= '2026-01-01' AND TxnDate <= '2026-01-31'"
  }
}
```

---

### 9. Permission Issues

#### Problem: "Insufficient permissions" error

**Cause:** App doesn't have correct scopes or company hasn't granted permission.

**Solution:**
1. Check app scopes at developer.intuit.com:
   - Should have "com.intuit.quickbooks.accounting" scope
   
2. Re-authenticate to grant new permissions:
```bash
# Delete config and re-authenticate
rm config.json
cp config.json.template config.json
# Add credentials and use qb_authenticate tool
```

3. Check if specific features are enabled in QuickBooks subscription:
   - Some features require QuickBooks Online Plus or Advanced

---

### 10. Windows-Specific Issues

#### Problem: "EPERM: operation not permitted" when saving config

**Cause:** File permissions or antivirus blocking file writes.

**Solution:**
```powershell
# Check file permissions
icacls config.json

# Grant full control to current user
icacls config.json /grant:r "%USERNAME%:F"

# Or run PowerShell as Administrator
```

---

#### Problem: Path issues with backslashes

**Cause:** Windows uses backslashes, but JSON needs forward slashes or escaped backslashes.

**Solution:**
```json
// ❌ WRONG:
"args": ["c:\Users\Shaun\Desktop\Quickbooks skill\run.js"]

// ✅ CORRECT (option 1 - forward slashes):
"args": ["c:/Users/Shaun/Desktop/Quickbooks skill/run.js"]

// ✅ CORRECT (option 2 - escaped backslashes):
"args": ["c:\\Users\\Shaun\\Desktop\\Quickbooks skill\\run.js"]
```

---

## Debugging Tips

### Enable Verbose Logging

Add this to run.js after the imports:
```javascript
// Add after require statements
axios.interceptors.request.use(request => {
  console.error('Request:', request.method, request.url);
  return request;
});

axios.interceptors.response.use(response => {
  console.error('Response:', response.status);
  return response;
});
```

### Check Token Status

Manually inspect your config.json:
```javascript
// Check if token is expired
const config = require('./config.json');
const expiryDate = new Date(config.token_expiry);
const now = new Date();

console.log('Token expires:', expiryDate);
console.log('Current time:', now);
console.log('Token expired:', now > expiryDate);
```

### Test API Connectivity

```bash
# Test if you can reach QuickBooks API
curl https://quickbooks.api.intuit.com

# Should return HTML or error page (not connection error)
```

### Validate JSON Syntax

```bash
# Check if your config.json is valid
node -e "console.log(JSON.parse(require('fs').readFileSync('config.json')))"
```

## Getting Help

### Before Asking for Help

Collect this information:
1. Node.js version: `node --version`
2. npm version: `npm --version`
3. Operating System: Windows/Mac/Linux
4. Environment: Sandbox or Production
5. Error message (full text)
6. Steps to reproduce
7. What you tried already

### Where to Get Help

1. **QuickBooks Developer Forum**
   - https://help.developer.intuit.com/s/
   - Search existing issues first
   - Tag questions with "QuickBooks API"

2. **API Documentation**
   - https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account
   - Check for entity-specific requirements

3. **Stack Overflow**
   - Tag: `quickbooks`, `intuit-partner-platform`
   - Search before posting

4. **Intuit Developer Support**
   - For production app issues
   - https://help.developer.intuit.com/s/contactsupport

### Reporting Bugs

When reporting issues with this skill:
1. Include Node.js and OS version
2. Provide error messages
3. Share sanitized request/response (remove credentials!)
4. Describe expected vs actual behavior
5. List reproduction steps

## Additional Resources

- [QuickBooks API Status](https://status.developer.intuit.com/) - Check for outages
- [Release Notes](https://developer.intuit.com/app/developer/qbo/docs/release-notes) - API changes
- [Known Issues](https://help.developer.intuit.com/s/bug-tracker-page) - Current bugs
- [Sample Apps](https://developer.intuit.com/app/developer/qbo/docs/get-started/start-developing-your-app) - Working examples

## Emergency Fixes

### Reset Everything

If nothing works, start fresh:
```bash
# 1. Delete node_modules and config
rm -rf node_modules
rm config.json

# 2. Reinstall
npm install

# 3. Copy template
cp config.json.template config.json

# 4. Add credentials
# Edit config.json with your client_id and client_secret

# 5. Re-authenticate
# Use qb_authenticate tool
```

### Check QuickBooks API Status

```bash
# Quick status check
curl https://status.developer.intuit.com/
```

If API is down, wait and retry later.

---

**Still stuck? Check the QuickBooks Developer Forum or contact Intuit Support.**
