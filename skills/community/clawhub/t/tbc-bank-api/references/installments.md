# TBC Bank Online Installments API

Enables merchants to offer installment loans to customers at checkout.

## Flow Overview

1. Merchant creates installment application → gets `sessionId`
2. Redirect customer to TBC Bank installment page
3. Customer applies for and accepts installment loan
4. TBC notifies merchant via callback
5. Merchant polls status or uses callback to fulfill order

## Create Application

```http
POST /v1/online-installments/applications
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
```

**Request Body:**
```json
{
  "merchantKey": "YOUR_MERCHANT_KEY",
  "priceTotal": 1500.00,
  "campaignId": "CAMPAIGN_001",
  "invoiceId": "INV-2023-001",
  "products": [
    {
      "name": "Samsung Galaxy S23",
      "price": 1500.00,
      "quantity": 1
    }
  ],
  "additionalText": "Optional message to customer",
  "callbackUrl": "https://yourshop.com/installment/callback"
}
```

**Response:**
```json
{
  "sessionId": "sess-abc-123",
  "status": "created",
  "redirectUrl": "https://installments.tbcbank.ge/apply?session=sess-abc-123"
}
```

## Redirect Customer

After receiving `redirectUrl`, redirect the customer's browser:

```javascript
window.location.href = response.redirectUrl;
// or
res.redirect(response.redirectUrl);
```

## Check Application Status

```http
GET /v1/online-installments/applications/{sessionId}/status
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

**Response:**
```json
{
  "sessionId": "sess-abc-123",
  "status": "approved",
  "invoiceId": "INV-2023-001",
  "approvedAmount": 1500.00,
  "currency": "GEL"
}
```

**Status values:**
- `created` — Application just initiated
- `pending` — Customer in process of applying
- `approved` — Loan approved, payment complete
- `rejected` — Loan rejected
- `cancelled` — Customer cancelled
- `expired` — Session timed out

## Get Status Changes (Bulk Polling)

```http
GET /v1/online-installments/merchant/applications/status-changes
  ?fromDate=2023-06-01
  &toDate=2023-06-30
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

Use for reconciliation and catching any missed callbacks.

## Callback Handling

TBC Bank POSTs to your `callbackUrl` when status changes:

```json
{
  "sessionId": "sess-abc-123",
  "status": "approved",
  "invoiceId": "INV-2023-001",
  "approvedAmount": 1500.00,
  "currency": "GEL",
  "timestamp": "2023-06-15T10:30:00Z"
}
```

**Callback handler example (Node.js/Express):**
```javascript
app.post('/installment/callback', (req, res) => {
  const { sessionId, status, invoiceId } = req.body;

  if (status === 'approved') {
    // Fulfill the order for invoiceId
    fulfillOrder(invoiceId);
  }

  // Must return 200 to acknowledge
  res.status(200).send('OK');
});
```

## Credentials Setup

1. Register at TBC Bank developer portal: `https://developers.tbcbank.ge`
2. Create an application and get `merchantKey`, `client_id`, `client_secret`
3. Configure callback URL in portal
4. Use sandbox: `https://test-api.tbcbank.ge` for testing
