# curl examples

Set once (Single API Key from *Settings → API → API keys*):

```bash
export SENDPULSE_API_KEY="your_api_key"
AUTH="Authorization: Bearer $SENDPULSE_API_KEY"
API="https://api.sendpulse.com"
```

(Using OAuth instead? `POST /oauth/access_token` with client_id/client_secret and
use the returned token the same way — it expires in 1 h.)

## Address book + subscribers

```bash
# Create a book
curl -s -X POST $API/addressbooks -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"bookName": "Newsletter"}'
# -> {"id": 12345}

# Add subscribers with variables (upsert — re-adding updates variables)
curl -s -X POST $API/addressbooks/12345/emails -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {"email": "jane@example.com", "variables": {"name": "Jane", "city": "Berlin", "signup_date": "2026-07-01"}},
      {"email": "john@example.com", "variables": {"name": "John", "city": "Kyiv",  "signup_date": "2026-07-02"}}
    ]
  }'

# Add with double opt-in (confirmation email)
curl -s -X POST $API/addressbooks/12345/emails -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "emails": [{"email": "jane@example.com", "variables": {"name": "Jane"}}],
    "confirmation": "force",
    "sender_email": "news@myshop.com",
    "template_id": "your-confirmation-template-id",
    "message_lang": "en"
  }'

# Count / list / one subscriber
curl -s $API/addressbooks/12345/emails/total -H "$AUTH"
curl -s "$API/addressbooks/12345/emails?limit=100&offset=0" -H "$AUTH"
curl -s $API/emails/jane@example.com -H "$AUTH"
```

## Pre-flight: senders, cost, balance

```bash
curl -s $API/senders -H "$AUTH"                    # sender_email must be here & active
curl -s $API/addressbooks/12345/cost -H "$AUTH"    # what this send will cost
curl -s $API/balance -H "$AUTH"
```

## Create a campaign

```bash
BODY_B64=$(printf '<h1>Hello {{name}}!</h1><p>Our July digest...</p>' | base64 | tr -d '\n')

curl -s -X POST $API/campaigns -H "$AUTH" -H "Content-Type: application/json" \
  -d "{
    \"name\": \"July digest\",
    \"sender_name\": \"My Shop\",
    \"sender_email\": \"news@myshop.com\",
    \"subject\": \"Your July digest is here\",
    \"body\": \"$BODY_B64\",
    \"list_id\": 12345,
    \"send_date\": \"2026-07-10 10:00:00\",
    \"stats\": {\"opens\": true, \"clicks\": true, \"utm_campaign\": \"july_digest\"}
  }"
# -> {"id": 987654, ...}   (omit send_date to send ASAP; use "template_id" instead of "body" for stored templates)
```

## Watch and manage

```bash
curl -s $API/campaigns/987654 -H "$AUTH"                       # status + stats after sending
curl -s "$API/campaigns?limit=20&offset=0" -H "$AUTH"          # recent campaigns
curl -s -X PATCH $API/campaigns/987654 -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"send_date": "2026-07-11 09:00:00"}'                    # reschedule (while still scheduled)
curl -s -X DELETE $API/campaigns/987654 -H "$AUTH"             # cancel before sending
```

## Analytics

```bash
curl -s $API/campaigns/987654/countries -H "$AUTH"             # by recipient country
curl -s $API/campaigns/987654/referrals -H "$AUTH"             # clicks per link
curl -s $API/campaigns/987654/email/jane@example.com -H "$AUTH" # one recipient's result
curl -s $API/emails/jane@example.com/campaigns -H "$AUTH"      # one address across campaigns
```

## Suppression (account-wide blacklist — note the Base64 format!)

```bash
EMAILS_B64=$(printf 'optout@example.com,complained@example.com' | base64 | tr -d '\n')

curl -s -X POST $API/blacklist -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"emails\": \"$EMAILS_B64\", \"comment\": \"complained via app\"}"
curl -s $API/blacklist -H "$AUTH"
```

## Webhooks

```bash
curl -s -X POST $API/v2/email-service/webhook/ -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"url": "https://your.app/hooks/sendpulse/SECRET", "actions": ["delivered", "open", "redirect", "unsubscribe", "spam", "hard_bounces", "task_status_update"]}'
curl -s $API/v2/email-service/webhook -H "$AUTH"
```
