# TBC Bank Payment Initiation Services (PIS)

Base path: `https://test-api.tbcbank.ge/0.8/v1/`

## Payment Products

| Product | Description |
|---------|-------------|
| `domestic` | Local GEL transfers within Georgia |
| `aspsp` | Bank's own payment product (supports FX) |
| `bulk-payments` | Multiple payments in one request |
| `sepa-credit-transfers` | SEPA transfers |

## Standard Payment Initiation

### Initiate Payment

```http
POST /0.8/v1/payments/{paymentProduct}
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

**Request Body:**
```json
{
  "debtorAccount": {
    "iban": "GE01TB0203040506070809",
    "currency": "GEL"
  },
  "instructedAmount": {
    "currency": "GEL",
    "amount": "100.00"
  },
  "creditorAccount": {
    "iban": "GE99XX0000000000000001"
  },
  "creditorName": "John Smith",
  "remittanceInformationUnstructured": "Invoice #2023-001",
  "ultimateDebtor": "Optional payer name",
  "creditorAgent": "TBCBGE22"
}
```

**Without debtor account (user selects at bank):**
```json
{
  "instructedAmount": { "currency": "GEL", "amount": "100.00" },
  "creditorAccount": { "iban": "GE99XX0000000000000001" },
  "creditorName": "John Smith",
  "remittanceInformationUnstructured": "Payment"
}
```

**Response:**
```json
{
  "paymentId": "7cd2d0e2-60a6-4cc6-1b33-08dae1b181a1",
  "transactionStatus": "ACTC",
  "_links": {
    "scaOAuth": {
      "href": "https://dev-openbanking.tbcbank.ge/openbanking/oauth/.well-known/oauth-authorization-server"
    },
    "self": {
      "href": "/0.8/v1/payments/domestic/7cd2d0e2-..."
    },
    "status": {
      "href": "/0.8/v1/payments/domestic/7cd2d0e2-.../status"
    },
    "scaStatus": {
      "href": "/0.8/v1/payments/domestic/7cd2d0e2-.../authorisations/df93472a-..."
    }
  }
}
```

**FX Payment Response (with currency conversion):**
```json
{
  "paymentId": "1c76b997-3028-4929-...",
  "transactionStatus": "ACTC",
  "estimatedTotalAmount": { "currency": "GEL", "amount": "41.25" },
  "estimatedInterbankSettlementAmount": { "currency": "USD", "amount": "15.00" },
  "_links": { ... }
}
```

### Get Payment Details

```http
GET /0.8/v1/payments/{paymentProduct}/{paymentId}
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

### Get Payment Status

```http
GET /0.8/v1/payments/{paymentProduct}/{paymentId}/status
Authorization: Bearer {token}
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

**Response:**
```json
{ "transactionStatus": "ACSP" }
```

### Start Payment Authorization

```http
POST /0.8/v1/payments/{paymentProduct}/{paymentId}/authorisations
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

## Recurring Payments (v2)

```http
POST /v2/recurring-payments/{paymentProduct}
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
```

**Request Body:**
```json
{
  "debtorAccount": { "iban": "GE01TB0203040506070809" },
  "instructedAmount": { "currency": "GEL", "amount": "50.00" },
  "creditorAccount": { "iban": "GE99XX..." },
  "creditorName": "Subscription Service",
  "remittanceInformationUnstructured": "Monthly subscription",
  "startDate": "2023-07-01",
  "endDate": "2024-06-30",
  "executionRule": "following",
  "frequency": "Monthly"
}
```

## Deferred Payments (v2)

```http
POST /v2/deferred-payments/{paymentProduct}
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
```

Add `"requestedExecutionDate": "2023-07-15"` to the standard payment body.

## Signing Baskets (Bulk Authorization)

Group multiple payments for single user authorization:

```http
POST /0.8/v1/signing-baskets
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}

{
  "paymentIds": ["payment-id-1", "payment-id-2", "payment-id-3"]
}
```

**Response:**
```json
{
  "basketId": "1234-basket-567",
  "transactionStatus": "RCVD",
  "_links": {
    "self": { "href": "/0.8/v1/signing-baskets/1234-basket-567" },
    "status": { "href": "/0.8/v1/signing-baskets/1234-basket-567/status" },
    "startAuthorisation": { "href": "/0.8/v1/signing-baskets/1234-basket-567/authorisations" }
  }
}
```

## Transaction Status Codes

| Code | Meaning |
|------|---------|
| `RCVD` | Received — initial state |
| `ACTC` | Accepted Technical Validation |
| `ACCP` | Accepted Customer Profile |
| `ACFC` | Accepted Funds Checked |
| `ACSP` | Accepted Settlement in Progress |
| `ACCC` | Accepted Credit Completed |
| `RJCT` | Rejected |
| `CANC` | Cancelled |

## Authorization Flows for Payments

After `POST /payments`, follow the `_links` from response:

1. **Redirect** — Use `scaRedirect.href` to redirect user to bank
2. **OAuth2** — Use `scaOAuth.href` to get OAuth config, then initiate authorization code flow
3. **Embedded** — Use `startAuthorisationWithPsuAuthentication.href` to authenticate inline
4. **Decoupled** — User authenticates on mobile app separately
