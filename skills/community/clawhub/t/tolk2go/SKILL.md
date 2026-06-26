# Tolk2Go Interpreter Booking API

Book professional interpreters in the Netherlands, Belgium, Germany, Luxembourg and France via the Tolk2Go public API.

## When to Use

User wants to book an interpreter, find interpreter availability, check pricing, or search interpreting languages and situations.

## Architecture

```
https://api.tolk2go.com/api/v1/    # Base URL
  ├── languages                     # List 108+ interpreting languages
  ├── language-pairs                # List language pair combinations
  ├── situations                    # List situation types (medical, legal, etc.)
  ├── availability                  # Search interpreters with pricing
  ├── register                      # Create user account
  ├── login                         # Get Bearer token (5 min)
  ├── bookings                      # Create booking request
  ├── bookings/{id}                 # Get status / cancel
  ├── bookings/{id}/responses       # Poll interpreter responses
  └── bookings/{id}/book            # Confirm interpreter
```

## OpenAPI Spec

Full specification: `https://api.tolk2go.com/api/v1/spec`

## Booking Flow

Always follow these steps in order:

1. **Find language pair**: `GET /language-pairs` — find the ID for the needed language combination
2. **Find situation**: `GET /situations` — find the ID (medical, legal, notary, etc.)
3. **Search availability**: `GET /availability?language_pair_id=...&situation_id=...&start=...&end=...&type=phone` — returns interpreters with pricing
4. **Register or login**: `POST /register` or `POST /login` — get a Bearer token (valid 5 minutes)
5. **Create booking**: `POST /bookings` — pass `preferred_interpreter_ids` from step 3
6. **Poll responses**: `GET /bookings/{id}/responses` — wait for interpreters to respond
7. **Book interpreter**: `POST /bookings/{id}/book` — confirm a specific interpreter

## Quick Reference

| Endpoint | Auth | Method | Purpose |
|----------|------|--------|---------|
| `/languages` | No | GET | List interpreting languages |
| `/language-pairs` | No | GET | List language pair combinations |
| `/situations` | No | GET | List situation types |
| `/availability` | No | GET | Search interpreters + pricing |
| `/register` | No | POST | Create account |
| `/login` | No | POST | Get Bearer token |
| `/bookings` | Yes | POST | Create booking |
| `/bookings/{id}` | Yes | GET | Check status |
| `/bookings/{id}` | Yes | DELETE | Cancel booking |
| `/bookings/{id}/responses` | Yes | GET | Poll interpreter responses |
| `/bookings/{id}/book` | Yes | POST | Confirm interpreter |

## Example: Search Availability

```bash
curl "https://api.tolk2go.com/api/v1/availability?\
language_pair_id=5a5d02b1d8586dc461fb322a&\
situation_id=6073ec8e9814917b6d136031&\
start=2026-04-01T09:00:00Z&\
end=2026-04-01T10:00:00Z&\
type=phone"
```

## Example: Create Booking

```bash
TOKEN=$(curl -s -X POST https://api.tolk2go.com/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}' | jq -r '.token')

curl -X POST https://api.tolk2go.com/api/v1/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "language_pair_id": "5a5d02b1d8586dc461fb322a",
    "situation_id": "6073ec8e9814917b6d136031",
    "start": "2026-04-01T09:00:00Z",
    "end": "2026-04-01T10:00:00Z",
    "type": "phone",
    "preferred_interpreter_ids": ["id1", "id2"],
    "description": "Medical appointment"
  }'
```

## Core Rules

- **All times in UTC** (ISO-8601). Convert from user's timezone.
- **`preferred_interpreter_ids` is required** for booking — always get IDs from `/availability` first.
- **Tokens expire after 5 minutes**. Re-login if you get 401.
- **For on-site bookings** (`type=address`), `lat`, `lng`, and `address` are required.
- **Present prices clearly**: show both excl. tax and incl. tax in EUR.
- **Never guess IDs** — always look them up via the API.
- **Rate limit**: 5 registrations per IP per 24 hours.

## Coverage

- 🇳🇱 Netherlands, 🇧🇪 Belgium, 🇩🇪 Germany, 🇱🇺 Luxembourg, 🇫🇷 France
- 108+ interpreting languages
- Phone, video, and on-site interpreting
- Healthcare, legal, government, corporate, education sectors

## External Endpoints

All requests go to `https://api.tolk2go.com/api/v1/`.

## Feedback

Website: https://www.tolk2go.com
Support: support@tolk2go.com
