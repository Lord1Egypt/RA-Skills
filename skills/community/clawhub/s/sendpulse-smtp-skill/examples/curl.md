# curl examples

Set once:

```bash
export SENDPULSE_API_ID="your_id"
export SENDPULSE_API_SECRET="your_secret"
```

## Get a token

```bash
TOKEN=$(curl -s -X POST https://api.sendpulse.com/oauth/access_token \
  -H "Content-Type: application/json" \
  -d "{\"grant_type\":\"client_credentials\",\"client_id\":\"$SENDPULSE_API_ID\",\"client_secret\":\"$SENDPULSE_API_SECRET\"}" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
```

## Send a simple HTML email

```bash
HTML_B64=$(printf '<h1>Hello!</h1><p>Your order #1234 is confirmed.</p>' | base64 | tr -d '\n')

curl -s -X POST https://api.sendpulse.com/smtp/emails \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": {
      \"subject\": \"Order confirmed\",
      \"from\": {\"name\": \"My Shop\", \"email\": \"noreply@myshop.com\"},
      \"to\": [{\"name\": \"Jane\", \"email\": \"jane@example.com\"}],
      \"html\": \"$HTML_B64\",
      \"text\": \"Hello! Your order #1234 is confirmed.\"
    }
  }"
# -> {"result":true,"id":"..."}
```

## Send using a stored template with variables

```bash
curl -s -X POST https://api.sendpulse.com/smtp/emails \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": {
      "subject": "Order confirmed",
      "from": {"name": "My Shop", "email": "noreply@myshop.com"},
      "to": [{"email": "jane@example.com"}],
      "template": {"id": 12345, "variables": {"name": "Jane", "order_id": "1234"}}
    }
  }'
```

## Send with a PDF attachment

```bash
PDF_B64=$(base64 < invoice.pdf | tr -d '\n')

curl -s -X POST https://api.sendpulse.com/smtp/emails \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": {
      \"subject\": \"Your invoice\",
      \"from\": {\"name\": \"My Shop\", \"email\": \"billing@myshop.com\"},
      \"to\": [{\"email\": \"jane@example.com\"}],
      \"html\": \"$(printf '<p>Invoice attached.</p>' | base64 | tr -d '\n')\",
      \"text\": \"Invoice attached.\",
      \"attachments_binary\": {\"invoice.pdf\": \"$PDF_B64\"}
    }
  }"
```

## Check delivery status

```bash
curl -s https://api.sendpulse.com/smtp/emails/MESSAGE_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Hygiene: check blocklist, pull bounces, unsubscribe

```bash
# Is this address unsubscribed?
curl -s "https://api.sendpulse.com/smtp/unsubscribe/search?email=jane@example.com" \
  -H "Authorization: Bearer $TOKEN"

# Bounces for the last 24 h
curl -s https://api.sendpulse.com/smtp/bounces/day \
  -H "Authorization: Bearer $TOKEN"

# Add an address to the blocklist (user opted out in your app)
curl -s -X POST https://api.sendpulse.com/smtp/unsubscribe \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"emails": [{"email": "jane@example.com", "comment": "opted out in app"}]}'
```

## List verified senders

```bash
curl -s https://api.sendpulse.com/smtp/senders -H "Authorization: Bearer $TOKEN"
```
