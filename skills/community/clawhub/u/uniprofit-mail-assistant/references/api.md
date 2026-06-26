# API Reference

## Environment

- `UNIPROFIT_API_BASE_URL`
  - Example: `https://your-domain`
- `UNIPROFIT_MAIL_SEND_KEY`
  - User-created `mail_send` OpenClaw API key

Important:

- The environment variable alone does not authenticate the request.
- Every runtime request must include:

```http
X-UniProfit-Key: {UNIPROFIT_MAIL_SEND_KEY}
```

Protocol:

- Use only `GET /openclaw/credential/me` for credential validation.
- Use `GET /openclaw/mail/account/list` to fetch selectable sender accounts.
- Use only `POST /openclaw/mail/send` for runtime delivery.
- Do not translate this skill into generic mail or SMTP endpoints.

## Credential Check

```http
GET {UNIPROFIT_API_BASE_URL}/openclaw/credential/me
X-UniProfit-Key: {UNIPROFIT_MAIL_SEND_KEY}
```

Expected:

- `skill_code = mail_send`
- `configured = true`

If this request returns `401` with a message like `Invalid OpenClaw credential`, first check whether the caller actually sent `X-UniProfit-Key`. Do not assume the endpoint needs platform login auth.

## List Sender Accounts

```http
GET {UNIPROFIT_API_BASE_URL}/openclaw/mail/account/list
X-UniProfit-Key: {UNIPROFIT_MAIL_SEND_KEY}
```

Typical response:

```json
{
  "code": 0,
  "msg": "Query succeeded",
  "data": [
    {
      "account_id": 12,
      "email": "sales@your-domain.com",
      "name": "Sales",
      "smtp_verified": true
    }
  ],
  "success": true
}
```

Use this list for sender selection. Then pass the corresponding `account_id` to the send API.

## Send Mail Request

```http
POST {UNIPROFIT_API_BASE_URL}/openclaw/mail/send
X-UniProfit-Key: {UNIPROFIT_MAIL_SEND_KEY}
Content-Type: application/json
```

Body:

```json
{
  "account_id": 12,
  "to_email": "buyer@example.com",
  "to_name": "Alice",
  "subject": "Product Introduction",
  "body": "<p>Hello Alice</p>",
  "reply_to": "sales@example.com"
}
```

## Send Mail Response

```json
{
  "code": 0,
  "msg": "Send completed",
  "data": {
    "to_email": "buyer@example.com",
    "status": "SENT",
    "record_id": 10086,
    "message_id": "4e6f4f5c-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  },
  "success": true
}
```
