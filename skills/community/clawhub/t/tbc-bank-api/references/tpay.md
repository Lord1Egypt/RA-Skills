# TBC Bank TPay Gateway

TPay is TBC Bank's hosted payment gateway for e-commerce.

## Authentication

TPay uses a separate access token from PSD2:

```http
POST /v1/tpay/access-token
Content-Type: application/x-www-form-urlencoded

client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

## Initiate Payment

```http
POST /v1/tpay/payments
Authorization: Bearer {tpay_token}
Content-Type: application/json
X-Request-ID: {uuid}
```

**Request Body:**
```json
{
  "amount": 150.00,
  "currency": "GEL",
  "orderId": "ORDER-2023-001",
  "description": "Purchase at MyShop",
  "callbackUrl": "https://yourshop.com/tpay/callback",
  "preAuth": false,
  "language": "ka",
  "merchantName": "My Shop",
  "cardData": null
}
```

**Response:**
```json
{
  "paymentId": "tpay-payment-abc",
  "status": "created",
  "paymentUrl": "https://tpay.ge/checkout/tpay-payment-abc",
  "expiresAt": "2023-06-15T11:00:00Z"
}
```

## Redirect Customer

```javascript
window.location.href = response.paymentUrl;
```

## Get Payment Status

```http
GET /v1/tpay/payments/{paymentId}
Authorization: Bearer {tpay_token}
X-Request-ID: {uuid}
```

**Response:**
```json
{
  "paymentId": "tpay-payment-abc",
  "status": "success",
  "orderId": "ORDER-2023-001",
  "amount": 150.00,
  "currency": "GEL",
  "paidAt": "2023-06-15T10:45:00Z",
  "cardMask": "4111 **** **** 1111",
  "cardType": "VISA"
}
```

**Status values:**
- `created` — Payment initiated
- `pending` — Customer in payment flow
- `success` — Payment completed
- `failed` — Payment failed
- `expired` — Payment link expired
- `refunded` — Payment refunded

## Callback Handling

TBC posts to your `callbackUrl`:

```json
{
  "paymentId": "tpay-payment-abc",
  "status": "success",
  "orderId": "ORDER-2023-001",
  "amount": 150.00,
  "currency": "GEL",
  "signature": "hmac-sha256-of-payload"
}
```

**Verify callback signature:**
```python
import hmac
import hashlib

def verify_signature(payload: dict, received_sig: str, secret: str) -> bool:
    # Build canonical string from payload fields
    canonical = f"{payload['paymentId']}:{payload['status']}:{payload['amount']}"
    expected = hmac.new(
        secret.encode(),
        canonical.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, received_sig)
```

## Pre-Authorization (Hold & Capture)

For deferred capture (e.g., hotel bookings):

```json
{
  "amount": 200.00,
  "currency": "GEL",
  "orderId": "HOTEL-123",
  "preAuth": true,
  "description": "Hotel reservation hold"
}
```

To capture after service:
```http
POST /v1/tpay/payments/{paymentId}/capture
Authorization: Bearer {token}
Content-Type: application/json

{ "amount": 200.00 }
```

To cancel/void:
```http
POST /v1/tpay/payments/{paymentId}/cancel
Authorization: Bearer {token}
```
