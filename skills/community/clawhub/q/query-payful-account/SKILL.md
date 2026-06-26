---
name: payful-query
description: Query Payful account information including balance, transactions, and account details. Use when the user needs to check their Payful account status, view balance, or retrieve account information. Requires PAYFUL_TOKEN and PAYFUL_USER_ID environment variables to be set.
metadata: {"env": [{"name": "PAYFUL_TOKEN", "description": "Authentication token sourced from the BF-INTERNATIONAL-MEMBER-TOKEN browser cookie on global.payful.com", "required": true, "credential": true}, {"name": "PAYFUL_USER_ID", "description": "User ID sourced from the AGL_USER_ID browser cookie on global.payful.com", "required": true, "credential": true}], "primaryCredential": "PAYFUL_TOKEN"}
---

# Payful Query Skill

This skill queries Payful account information via the Payful API.

> **Security notice**: `PAYFUL_TOKEN` and `PAYFUL_USER_ID` are sensitive browser session cookies extracted from global.payful.com. They grant full access to your Payful account. Only set these values in a trusted environment and never share them.

## Prerequisites

Set the following environment variables:
- `PAYFUL_TOKEN` - Authentication token (from BF-INTERNATIONAL-MEMBER-TOKEN cookie)
- `PAYFUL_USER_ID` - User ID (from AGL_USER_ID cookie)

## Usage

### Query Account Balance

```python
python scripts/query_balance.py
```

### Query with Custom API URL

If using a different Payful environment:

```python
python scripts/query_balance.py --api-url https://other.payful.com
```

## API Reference

The skill uses the following Payful API endpoints:

### Get Account Balance
- **URL**: `https://global.payful.com/api/user/account/queryUserAccBalByHomePage`
- **Method**: GET
- **Headers**:
  - `Accept: application/json, text/plain, */*`
  - `Accept-Language: zh-CN`
  - `request-system-name: member-exchange-client`
  - `Cookie`: Contains authentication tokens

## Response Format

```json
{
  "code": "0000",
  "data": {
    "totalBalance": "1234.56",
    "currency": "USD",
    "availableBalance": "1200.00",
    "frozenBalance": "34.56"
  },
  "message": "success"
}
```
