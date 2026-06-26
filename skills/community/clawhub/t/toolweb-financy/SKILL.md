---
name: Financy - Personal Finance Tracker
description: Professional personal finance management API with analytics, multi-currency support, and transaction tracking.
---

# Overview

Financy is a comprehensive personal finance tracking API designed for users who need professional-grade financial management capabilities. The platform enables seamless tracking of income and expenses across multiple currencies, providing actionable insights through integrated analytics and dashboard summaries. Whether you're managing personal budgets, tracking investments, or analyzing spending patterns, Financy offers a secure, scalable foundation for financial data management.

Key capabilities include real-time transaction management, multi-currency support, category-based expense organization, comprehensive dashboard analytics, and data export functionality. The API is built with security best practices and is ideal for fintech applications, budgeting tools, personal finance platforms, and financial advisory services.

Financy serves developers, financial advisors, and organizations building consumer finance solutions who require reliable transaction management with advanced reporting and analytics capabilities.

## Usage

### Create a Transaction

**Request:**
```json
{
  "userId": 1001,
  "transaction": {
    "type": "expense",
    "amount": 45.99,
    "category": "Groceries",
    "date": "2024-01-15",
    "description": "Weekly grocery shopping",
    "notes": "Bought at Whole Foods",
    "currency": "USD"
  }
}
```

**Response:**
```json
{
  "success": true,
  "transaction_id": 5432,
  "message": "Transaction saved successfully",
  "data": {
    "id": 5432,
    "type": "expense",
    "amount": 45.99,
    "category": "Groceries",
    "date": "2024-01-15",
    "description": "Weekly grocery shopping",
    "notes": "Bought at Whole Foods",
    "currency": "USD"
  }
}
```

### Get Dashboard Summary

**Request:**
```json
{
  "userId": 1001,
  "currency": "USD"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": 1001,
  "summary": {
    "total_income": 5000.00,
    "total_expenses": 1245.50,
    "net_balance": 3754.50,
    "currency": "USD"
  },
  "recent_transactions": [
    {
      "id": 5432,
      "type": "expense",
      "amount": 45.99,
      "category": "Groceries",
      "date": "2024-01-15",
      "description": "Weekly grocery shopping"
    }
  ],
  "analytics": {
    "expense_by_category": {
      "Groceries": 245.50,
      "Transportation": 300.00,
      "Entertainment": 150.00
    },
    "monthly_trend": "spending decreased by 12%"
  }
}
```

## Endpoints

### GET /
**Health Check Endpoint**

Returns a simple health status to verify API availability.

**Parameters:** None

**Response:**
```json
{
  "status": "ok",
  "service": "Financy API",
  "version": "1.0.0"
}
```

---

### POST /api/financy/dashboard
**Get Dashboard with Summary and Analytics**

Retrieves user dashboard containing account summary, recent transactions, and spending analytics.

**Parameters:**
- `userId` (integer, required): Unique identifier for the user
- `currency` (string, optional, default: "USD"): Three-letter currency code (e.g., USD, EUR, GBP)

**Response:**
```json
{
  "success": true,
  "user_id": 1001,
  "summary": {
    "total_income": 5000.00,
    "total_expenses": 1245.50,
    "net_balance": 3754.50
  },
  "recent_transactions": [],
  "analytics": {}
}
```

---

### POST /api/financy/transaction
**Create or Update Transaction**

Saves a new transaction or updates an existing one for the specified user.

**Parameters:**
- `userId` (integer, required): Unique identifier for the user
- `transaction` (object, required): Transaction details containing:
  - `type` (string, required): "income" or "expense"
  - `amount` (number, required): Transaction amount
  - `category` (string, required): Expense or income category
  - `date` (string, required): Transaction date in YYYY-MM-DD format
  - `description` (string, required): Brief description of the transaction
  - `notes` (string, optional): Additional notes or comments
  - `currency` (string, optional, default: "USD"): Three-letter currency code
  - `id` (integer, optional): Provide to update existing transaction

**Response:**
```json
{
  "success": true,
  "transaction_id": 5432,
  "message": "Transaction saved successfully"
}
```

---

### DELETE /api/financy/transaction/{transaction_id}
**Delete Transaction**

Removes a specific transaction from the user's account.

**Parameters:**
- `transaction_id` (integer, required, path): ID of the transaction to delete
- `userId` (integer, required, body): Unique identifier for the user

**Response:**
```json
{
  "success": true,
  "message": "Transaction deleted successfully",
  "transaction_id": 5432
}
```

---

### POST /api/financy/export
**Export Transaction Data as CSV**

Exports user's transaction data in CSV format for external analysis or record-keeping.

**Parameters:**
- `userId` (integer, required): Unique identifier for the user
- `currency` (string, optional, default: "USD"): Three-letter currency code for exported data

**Response:**
```json
{
  "success": true,
  "export_id": "exp_12345",
  "format": "csv",
  "download_url": "https://api.toolweb.in/tools/financy/exports/exp_12345.csv",
  "record_count": 42,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/financy/categories
**Get All Available Categories**

Retrieves the complete list of predefined transaction categories for income and expense classification.

**Parameters:** None

**Response:**
```json
{
  "success": true,
  "expense_categories": [
    "Groceries",
    "Transportation",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Education",
    "Shopping",
    "Dining",
    "Insurance",
    "Housing",
    "Personal Care"
  ],
  "income_categories": [
    "Salary",
    "Bonus",
    "Investment Returns",
    "Freelance",
    "Gift",
    "Refund",
    "Other Income"
  ]
}
```

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.toolweb.in/tools/financy
- **API Docs:** https://api.toolweb.in:8170/docs
