---
name: youdo-business
description: Work with the YouDo Business API. Use when asked to interact with YouDo Business to manage employees, projects, tasks, payments, webhooks, or generate signed API requests.
---

# YouDo Business API Skill

This skill provides the knowledge and guidelines for interacting with the YouDo Business API.

## Base URLs
- **Production**: `https://business-api.youdo.com/api/v1`
- **Sandbox/Test**: `https://business-api.public-test.youdo.sg/api/v1`
- **Swagger**: `https://business-api.youdo.com/api/doc/index.html`

## Authentication

All requests use **JSON Web Token (JWT)** signed with the **RS256** asymmetric algorithm.
- The JWT must be sent in the header: `Authorization: Bearer <JWT_TOKEN>`
- **Header**: `{"alg": "RS256", "typ": "JWT", "kid": "<Key ID>"}`
- **Payload**: `{"iss": "<Issuer ID>", "cid": "<Company ID>"}`

## Request Signing

Certain methods (like `/api/v1/Task/{taskId}/pay`) require request signing. You must include the following headers:
- `Date`: Current time, RFC 7231 (e.g., `Tue, 19 Feb 2019 08:43:02 GMT`)
- `Content-SHA256`: SHA256 hex hash of the request body (empty string for GET).
- `Signature`: RS256 signed hex string of the request string.

**String to Sign format**:
```
Uppercase(RequestMethod) + "\n"
RequestPath + "\n"
RequestQuery + "\n"  // Alphabetically sorted, URLEncoded
SignedRequestHeaders + "\n" // Alphabetically sorted, lowercased keys
SHA256Hex(RequestPayload)
```

## Key Endpoints

### Employees (Исполнители)
- **Create**: `POST /Employee`
  - Body: `phone`, `firstName`, `lastName`, `inn`, `projectId`
- **Get Info**: `GET /Employee/{id}`
- **Search**: `POST /Employe/search` (Body: `projectIds`, `employeeName`, `inns`, `phones`, `itemsPerPage`, `page`)
- **Find by Phone**: `GET /Employe/byPhone/{phone}`
- **Add to Project**: `POST /Employee/addToProject`
- **Remove from Project**: `DELETE /Employee/{id}/deleteFromProject/{projectId}`
- **Restart Binding**: `PUT /Employee/{id}/binding/restart`

### Projects (Проекты)
- **Get Projects**: `GET /Project/Projects`

### Tasks & Payments (Задания и выплаты)
- **Create Internal Task**: `POST /Task/internal`
- **Create External Task**: `POST /Task/external`
- **Get Task**: `GET /Task/{taskId}`
- **Update Task**: `PUT /Task/{taskId}`
- **Pay Task**: `POST /Task/{taskId}/pay` (Requires request signing)
- **Resend Offer**: `PUT /Task/{taskId}/resendOffer`

### Documents (Документы)
- **Download Doc**: `GET /Documents/{documentId}`
- **Download Cert**: `GET /Documents/{documentId}/certificate`

### Payments Report (Отчет агента)
- **List Payments**: `POST /Payments` (Body: `from`, `to`, `inn`, `taskIds`, `ids`)

### Framework Agreements (Рамочные соглашения)
- **Get Agreements**: `GET /FrameworkAgreements/employees/{employeeId}/projects/{projectId}`
- **Create**: `POST /FrameworkAgreements`
- **Stop**: `POST /FrameworkAgreements/{agreementId}/stop`

### Prepayment Invoices (Счета на предоплату)
- **Create**: `POST /prepaymentInvoices` (Body: `companyId`, `amount`)
- **Get**: `GET /prepaymentInvoices/{id}`

### Balance (Баланс)
- **By Company**: `GET /Balance/byCompany?companyId={id}`
- **By Project**: `GET /Balance/byProject?projectId={id}`

### Webhooks
- **Subscribe**: `POST /WebHook/subscribe` (Body: `type`, `url`, `headers`)
- **Unsubscribe**: `DELETE /WebHook/{type}/unsubscribe`
