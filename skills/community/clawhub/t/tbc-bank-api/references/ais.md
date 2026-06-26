# TBC Bank Account Information Services (AIS)

Base path: `https://test-api.tbcbank.ge/0.8/v1/`

Requires a valid consent with AIS scope. See `consent.md` first.

## Endpoints

### List Accounts
```http
GET /0.8/v1/accounts
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

**Response:**
```json
{
  "accounts": [
    {
      "resourceId": "761a7d98-3251-4e98-50fe-08dd818830c7",
      "iban": "GE01TB0203040506070809",
      "currency": "GEL",
      "ownerName": "John Doe",
      "product": "Current Account",
      "status": "enabled",
      "bic": "TBCBGE22",
      "balances": [
        {
          "balanceType": "interimBooked",
          "balanceAmount": { "currency": "GEL", "amount": "30.00" }
        }
      ],
      "_links": {
        "balances": { "href": "/0.8/v1/accounts/761a7d98.../balances" },
        "transactions": { "href": "/0.8/v1/accounts/761a7d98.../transactions" }
      }
    }
  ]
}
```

### Get Account Details
```http
GET /0.8/v1/accounts/{accountId}
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
```

**Response:**
```json
{
  "account": {
    "resourceId": "c5503035-7f59-4f66-ff96-08dd6cfe8f7c",
    "iban": "GE01TB2123003210034512",
    "msisdn": "558112233",
    "currency": "USD",
    "ownerName": "მოქი მოქიაშვილი",
    "ownerIdentification": {
      "privateId": {
        "others": [{ "identification": "PNOGE-00000000001" }]
      }
    },
    "name": "მოქი მოქიაშვილი",
    "displayName": "My Card",
    "cashAccountType": "CARD",
    "status": "enabled",
    "bic": "TBCBGE22",
    "usage": "PRIV",
    "balances": [],
    "_links": {
      "balances": { "href": "/0.8/v1/accounts/{id}/balances" },
      "transactions": { "href": "/0.8/v1/accounts/{id}/transactions" },
      "account": { "href": "/0.8/v1/accounts/{id}" }
    }
  }
}
```

### Get Account Balances
```http
GET /0.8/v1/accounts/{accountId}/balances
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
```

**Response:**
```json
{
  "account": { "iban": "GE01TB0203040506070809", "currency": "XXX" },
  "balances": [
    {
      "balanceType": "interimAvailable",
      "balanceAmount": { "currency": "GEL", "amount": "30.00" },
      "creditLimitIncluded": false
    },
    {
      "balanceType": "interimBooked",
      "balanceAmount": { "currency": "GEL", "amount": "30.00" },
      "creditLimitIncluded": false,
      "referenceDate": "2025-03-26",
      "lastChangeDateTime": "2025-03-26T00:00:00"
    }
  ]
}
```

**Balance types:**
- `interimAvailable` — Available now (real-time)
- `interimBooked` — Booked balance (last settlement)
- `closingBooked` — Closing balance (end of day)

### Get Account Transactions
```http
GET /0.8/v1/accounts/{accountId}/transactions
  ?dateFrom=2023-01-01
  &dateTo=2023-12-31
  &bookingStatus=booked
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
```

**Query params:**
- `dateFrom` — ISO 8601 date (required)
- `dateTo` — ISO 8601 date (optional, defaults to today)
- `bookingStatus` — `booked`, `pending`, `both`
- `withBalance` — `true/false` — include balance snapshots
- `pageKey` — cursor for pagination

**Response:**
```json
{
  "account": { "iban": "GE01TB0203040506070809" },
  "transactions": {
    "booked": [
      {
        "transactionId": "abc123",
        "creditorName": "Merchant Name",
        "creditorAccount": { "iban": "GE99XX..." },
        "transactionAmount": { "currency": "GEL", "amount": "-50.00" },
        "bookingDate": "2023-06-15",
        "valueDate": "2023-06-15",
        "remittanceInformationUnstructured": "Payment for invoice #123"
      }
    ],
    "pending": [],
    "_links": {
      "next": { "href": "/0.8/v1/accounts/{id}/transactions?pageKey=..." }
    }
  }
}
```

## Card Accounts

### List Card Accounts
```http
GET /0.8/v1/card-accounts
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
```

### Get Card Account Balances
```http
GET /0.8/v1/card-accounts/{cardAccountId}/balances
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
```

## Exchange Rates

```http
GET /v1/exchange-rates/extended
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

```http
GET /v1/exchange-rates/commercial
Authorization: Bearer {token}
X-Request-ID: {uuid}
```
