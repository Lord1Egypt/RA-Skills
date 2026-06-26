# TBC Bank Consent Management & SCA

Consents authorize a TPP to access specific account data. Required for all AIS operations.

## Create Consent

```http
POST /0.8/v1/consents
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

**Request Body (Account + Transaction access):**
```json
{
  "access": {
    "accounts": [
      {
        "iban": "GE01TB0203040506070809",
        "currency": "GEL"
      }
    ],
    "balances": [
      { "iban": "GE01TB0203040506070809" }
    ],
    "transactions": [
      { "iban": "GE01TB0203040506070809" }
    ]
  },
  "recurringIndicator": true,
  "validTo": "2024-12-31",
  "frequencyPerDay": 4,
  "combinedServiceIndicator": false
}
```

**Loan account access:**
```json
{
  "access": {
    "loans": [
      {
        "account": { "iban": "GE78TB1121245063622479" },
        "rights": ["accountDetails", "balances", "transactions", "ownerName"]
      }
    ]
  },
  "consentType": "V2Consent",
  "recurringIndicator": true,
  "validTo": "2023-07-01",
  "frequencyPerDay": 4
}
```

**Response:**
```json
{
  "consentId": "consent-abc-123",
  "consentStatus": "received",
  "_links": {
    "scaRedirect": { "href": "https://..." },
    "scaOAuth": { "href": "https://..." },
    "self": { "href": "/0.8/v1/consents/consent-abc-123" },
    "status": { "href": "/0.8/v1/consents/consent-abc-123/status" },
    "startAuthorisation": { "href": "/0.8/v1/consents/consent-abc-123/authorisations" }
  }
}
```

## Get Consent Details

```http
GET /0.8/v1/consents/{consentId}
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

**Response:**
```json
{
  "access": {
    "loans": [
      {
        "account": { "iban": "GE78TB1121245063622479" },
        "rights": ["accountDetails", "balances", "transactions", "ownerName"]
      }
    ]
  },
  "consentType": "V2Consent",
  "recurringIndicator": true,
  "validTo": "2023-07-01",
  "frequencyPerDay": 4,
  "consentStatus": "valid"
}
```

## Get Consent Status

```http
GET /0.8/v1/consents/{consentId}/status
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

**Response:**
```json
{ "consentStatus": "valid" }
```

**Consent statuses:**
- `received` — Created, not yet authorized
- `partiallyAuthorised` — Some accounts authorized
- `valid` — Fully authorized and active
- `revokedByPsu` — User revoked
- `expired` — Past `validTo` date
- `terminatedByTpp` — TPP revoked it

## Start Consent Authorization

```http
POST /0.8/v1/consents/{consentId}/authorisations
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

**Response:**
```json
{
  "authorisationId": "auth-xyz-789",
  "scaStatus": "scaMethodSelected",
  "_links": {
    "scaRedirect": { "href": "https://openbanking.tbcbank.ge/authorize?..." },
    "scaStatus": { "href": "/0.8/v1/consents/{consentId}/authorisations/auth-xyz-789" }
  }
}
```

## Get SCA Status

```http
GET /0.8/v1/consents/{consentId}/authorisations/{authorisationId}
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

**Response:**
```json
{ "scaStatus": "finalised" }
```

## SCA Status Flow

```
received
  → psuIdentified       (user identified)
  → psuAuthenticated    (credentials validated)
  → scaMethodSelected   (SCA method chosen)
  → finalised           (authorization complete)
  → failed              (authorization failed)
```

## Delete Consent

```http
DELETE /0.8/v1/consents/{consentId}
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

## Using Consent-ID in AIS Requests

After consent is `valid`, include the `consentId` in every AIS call:

```http
GET /0.8/v1/accounts
Authorization: Bearer {token}
Consent-ID: {consentId}
X-Request-ID: {uuid}
PSU-IP-Address: {ip}
```

## Access Rights

| Right | Description |
|-------|-------------|
| `accountDetails` | IBAN, owner name, product type |
| `balances` | Current balance information |
| `transactions` | Transaction history |
| `ownerName` | Account holder name only |
