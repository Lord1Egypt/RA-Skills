---
name: Invoice Generator
description: Generate, download, and email professional invoices with GST/IGST support and flexible payment terms.
---

# Overview

Invoice Generator is a comprehensive invoice management API that enables businesses to create, customize, and distribute professional invoices programmatically. Built for e-commerce platforms, accounting systems, and billing automation, it supports multi-currency transactions, Indian GST/IGST compliance, and direct email distribution to customers.

The tool provides complete invoice lifecycle management—from generation with line-item details, tax calculations, and payment terms, to secure download and automated email delivery. It integrates seamlessly with SMTP servers for direct email transmission and maintains invoice records for later retrieval.

Ideal users include SaaS billing platforms, freelance management systems, accounting software providers, and e-commerce businesses requiring automated invoice workflows with professional formatting and compliance support.

## Usage

**Generate an invoice for a consulting service with GST:**

```json
{
  "company": {
    "name": "TechCorp Solutions",
    "address": "123 Business Park",
    "city": "Bangalore",
    "state": "Karnataka",
    "pincode": "560001",
    "phone": "+91-80-XXXX-XXXX",
    "email": "billing@techcorp.com",
    "gstin": "18AABCT1234H1Z0",
    "pan": "AAACT1234H",
    "logo_url": "https://example.com/logo.png"
  },
  "customer": {
    "name": "Acme Corporation",
    "address": "456 Client Street",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001",
    "phone": "+91-22-XXXX-XXXX",
    "email": "accounts@acme.com",
    "gstin": "27AABCT5678H1Z1"
  },
  "items": [
    {
      "description": "Consulting Services - Q1 2024",
      "quantity": 1,
      "rate": 50000,
      "tax_percent": 18
    },
    {
      "description": "Development Hours (120 hrs @ 500/hr)",
      "quantity": 120,
      "rate": 500,
      "tax_percent": 18
    }
  ],
  "invoice_number": "INV-2024-001",
  "invoice_date": "2024-01-15",
  "due_date": "2024-02-15",
  "payment_terms": "Net 30",
  "notes": "Thank you for your business. Payment via bank transfer preferred.",
  "bank_name": "HDFC Bank",
  "account_number": "1234567890123456",
  "ifsc_code": "HDFC0000123",
  "upi_id": "techcorp@hdfc",
  "is_igst": false
}
```

**Sample Response:**

```json
{
  "invoice_id": "inv_7f8a9b2c1e5d3k4m",
  "status": "generated",
  "subtotal": 110000,
  "tax_amount": 19800,
  "total_amount": 129800,
  "created_at": "2024-01-15T10:30:45Z",
  "message": "Invoice generated successfully"
}
```

## Endpoints

### GET `/`
**Root endpoint** – Returns API information and health status.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| — | — | — | No parameters |

**Response:** JSON object with service metadata.

---

### GET `/status`
**Status check** – Returns current API health and operational status.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| — | — | — | No parameters |

**Response:** JSON object with status information and service uptime.

---

### POST `/generate`
**Generate Invoice** – Creates a new invoice from company, customer, and line item details.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| company | CompanyDetails | Yes | Company/seller information including name, address, tax IDs, contact details, and optional logo URL |
| customer | CustomerDetails | Yes | Customer/buyer information including name, address, tax IDs, and contact details |
| items | LineItem[] | Yes | Array of line items with description, quantity, rate, and optional tax percentage |
| invoice_number | string | No | Custom invoice number (auto-generated if omitted) |
| invoice_date | string | No | Invoice issuance date in YYYY-MM-DD format |
| due_date | string | No | Payment due date in YYYY-MM-DD format |
| payment_terms | string | No | Payment terms description (default: "Due on Receipt") |
| notes | string | No | Additional notes or payment instructions |
| bank_name | string | No | Bank name for payment details |
| account_number | string | No | Bank account number |
| ifsc_code | string | No | IFSC code for Indian bank transfers |
| upi_id | string | No | UPI ID for digital payments |
| is_igst | boolean | No | Set to true for IGST (Integrated GST), false for SGST+CGST (default: false) |

**Response:** JSON object containing:
- `invoice_id`: Unique identifier for retrieving/downloading the invoice
- `status`: Generation status ("generated")
- `subtotal`: Total amount before tax
- `tax_amount`: Calculated tax amount
- `total_amount`: Final invoice total
- `created_at`: Timestamp of invoice creation

---

### GET `/download/{invoice_id}`
**Download Invoice** – Retrieves and downloads a previously generated invoice as PDF.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| invoice_id | string | Yes | Unique identifier of the invoice to download (path parameter) |

**Response:** PDF file download or JSON error with appropriate HTTP status.

---

### POST `/send-email`
**Send Email** – Sends a generated invoice to a specified email address via SMTP.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| invoice_id | string | Yes | Unique identifier of the invoice to email |
| to_email | string | Yes | Recipient email address (must be valid email format) |
| to_name | string | No | Recipient's display name (default: empty) |
| from_email | string | Yes | Sender email address (must be valid email format) |
| from_name | string | No | Sender's display name (default: empty) |
| subject | string | No | Email subject line (default: empty) |
| message | string | No | Email body/message text (default: empty) |
| smtp_host | string | No | SMTP server hostname (default: "localhost") |
| smtp_port | integer | No | SMTP server port number (default: 587) |
| smtp_user | string | No | SMTP authentication username (default: empty) |
| smtp_pass | string | No | SMTP authentication password (default: empty) |
| use_tls | boolean | No | Enable TLS encryption (default: true) |

**Response:** JSON object containing:
- `status`: Email delivery status ("sent", "pending", or "failed")
- `message`: Status message with delivery details
- `timestamp`: Email send timestamp

---

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

- Kong Route: https://api.toolweb.in/tools/invoicy
- API Docs: https://api.toolweb.in:8165/docs
