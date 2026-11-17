# Quickstart — first campaign in 10 minutes

Prerequisites: a SendPulse account, a **verified sender** on your own (corporate)
domain, and an API key from *Settings → API → API keys* (or OAuth `ID`/`Secret`).

Throughout: `Authorization: Bearer $SENDPULSE_API_KEY` on every request to
`https://api.sendpulse.com`.

## 0. (OAuth only) Get a token

Skip this if you use a Single API Key. Otherwise:

```bash
curl -s -X POST https://api.sendpulse.com/oauth/access_token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"YOUR_ID","client_secret":"YOUR_SECRET"}'
# -> {"access_token":"...","token_type":"Bearer","expires_in":3600}
```

## 1. Create an address book

```bash
curl -s -X POST https://api.sendpulse.com/addressbooks \
  -H "Authorization: Bearer $SENDPULSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"bookName": "Newsletter subscribers"}'
# -> {"id": 12345}
```

## 2. Add subscribers (with variables)

```bash
curl -s -X POST https://api.sendpulse.com/addressbooks/12345/emails \
  -H "Authorization: Bearer $SENDPULSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {"email": "jane@example.com", "variables": {"name": "Jane", "city": "Berlin"}},
      {"email": "john@example.com", "variables": {"name": "John", "city": "Kyiv"}}
    ]
  }'
```

Only add people who **opted in**. For double opt-in (confirmation email), add
`"confirmation": "force"` plus `sender_email`, `template_id`, `message_lang` — see
[address-books.md](address-books.md).

## 3. Check the sender and the cost

```bash
# Verified senders — sender_email below must be one of these
curl -s https://api.sendpulse.com/senders -H "Authorization: Bearer $SENDPULSE_API_KEY"

# What will this campaign cost for this book?
curl -s https://api.sendpulse.com/addressbooks/12345/cost \
  -H "Authorization: Bearer $SENDPULSE_API_KEY"
```

## 4. Create the campaign

The HTML `body` must be **Base64-encoded**. (Need the HTML itself? Build it with the
`sendpulse-template-skill` — this skill doesn't code emails.)

```bash
BODY_B64=$(printf '<h1>Hello {{name}}!</h1><p>Our July digest...</p>' | base64 | tr -d '\n')

curl -s -X POST https://api.sendpulse.com/campaigns \
  -H "Authorization: Bearer $SENDPULSE_API_KEY" \
  -H "Content-Type: application/json" \
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
# -> {"id": 987654, "status": 0, ...}
```

Alternatively pass `"template_id": <id>` instead of `body` to use a template stored
in SendPulse. Omit `send_date` to send as soon as possible.

## 5. Watch the status

```bash
curl -s https://api.sendpulse.com/campaigns/987654 \
  -H "Authorization: Bearer $SENDPULSE_API_KEY"
```

**Don't panic if the campaign sits in review** — first campaigns from a new account
are routinely checked by SendPulse's anti-abuse system before sending. It's normal
and usually resolves within hours. Status meanings: [errors.md](errors.md).

## 6. Read the results

After it's sent, the same `GET /campaigns/{id}` returns the statistics (sent,
delivered, opened, clicked, unsubscribed...). What to do with the numbers:
[analytics.md](analytics.md).

## The pre-flight checklist (use it for every real campaign)

- [ ] Sender verified (`GET /senders`), on your own domain
- [ ] List is opt-in; segment chosen (not "everyone") — [segmentation.md](segmentation.md)
- [ ] Test email sent to yourself and checked on desktop + phone
- [ ] Cost checked (`/addressbooks/{id}/cost`), balance sufficient
- [ ] Tracking on (`stats.opens/clicks`) + UTM tags set
- [ ] Unsubscribe link present in the template footer
- [ ] Scheduled at a sensible time (consider `send_at_the_optimum_time` /
      timezone sending — [campaigns.md](campaigns.md))
