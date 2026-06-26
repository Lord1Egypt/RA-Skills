# Send a Basic Email

Simplest possible email send: plain text to one recipient.

## User Prompt

> "Send an email to alice@example.com saying the deployment completed successfully."

## Agent Action

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: deploy-complete-2026-03-11-001" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "alice@example.com",
    "from": "notifications@yourapp.com",
    "subject": "Deployment completed successfully",
    "html": "<p>The deployment to production completed successfully at 2026-03-11 14:30 UTC.</p>",
    "text": "The deployment to production completed successfully at 2026-03-11 14:30 UTC."
  }'
```

## Expected Response

```json
{
  "status": "sent",
  "message_id": "cm1abc2def3ghi",
  "provider_message_id": "0100018e-abcd-1234-5678-example"
}
```

## Agent Reply

> Sent email to alice@example.com with subject "Deployment completed successfully". Message ID: `cm1abc2def3ghi`.
