# Address books & subscribers

The address book (mailing list) is the unit everything else operates on: campaigns
target books (or segments of them), variables live on subscribers within books,
statistics aggregate per book.

## Books

| Method | Path | Purpose |
|---|---|---|
| POST | `/addressbooks` | Create: `{"bookName": "..."}` → `{"id": N}` |
| PUT | `/addressbooks/{id}` | Rename |
| GET | `/addressbooks` | List (`limit`, `offset` — default page 100) |
| GET | `/addressbooks/{id}` | Info: name, counts, creation date, status |
| DELETE | `/addressbooks/{id}` | Delete the book |
| GET | `/addressbooks/{id}/cost` | Campaign cost for this book — check before sending |
| GET | `/addressbooks/{id}/variables` | Variables defined in the book |
| GET | `/addressbooks/{id}/campaigns` | Campaigns sent to this book |

Book statuses: 0 Active · 1 Deleted · 3 Awaiting clarification · 4 Blocked by
service · 5 Temporarily blocked. A non-zero status usually means the service has
questions about the list origin — resolve it in the dashboard before sending.

**Structure advice:** fewer, well-maintained books + segments beat dozens of
overlapping books. Duplicates across books each count toward plan limits; a
campaign to multiple books deduplicates recipients, but management gets messy.

## Subscribers

| Method | Path | Purpose |
|---|---|---|
| POST | `/addressbooks/{id}/emails` | Add subscribers (single or double opt-in — below) |
| GET | `/addressbooks/{id}/emails` | List (`limit`, `offset`, filters `active`/`not_active`) |
| GET | `/addressbooks/{id}/emails/total` | Count |
| GET | `/addressbooks/{id}/emails/{email}` | One subscriber's info in this book |
| DELETE | `/addressbooks/{id}/emails` | Remove: `{"emails": [...]}` — **max 100 per call** |
| POST | `/addressbooks/{id}/emails/unsubscribe` | Unsubscribe from this book |
| GET | `/emails/{email}` | Subscriber across ALL books |
| DELETE | `/emails/{email}` | Remove from all books |
| GET | `/emails/{email}/campaigns` | Which campaigns this address received, opens/clicks |

### Adding — single opt-in

```json
POST /addressbooks/{id}/emails
{
  "emails": [
    {"email": "jane@example.com", "variables": {"name": "Jane", "signup_date": "2026-07-01"}}
  ]
}
```

Plain form `{"emails": ["a@b.c", "d@e.f"]}` works when there are no variables.
Re-adding an existing address **updates** its variables (upsert) — safe to sync.

### Adding — double opt-in (recommended for new signups)

```json
{
  "emails": [{"email": "jane@example.com", "variables": {"name": "Jane"}}],
  "confirmation": "force",
  "sender_email": "news@myshop.com",
  "template_id": "<confirmation-template id>",
  "message_lang": "en"
}
```

The subscriber gets a confirmation email and becomes active only after clicking.
Requires an activated sender. Double opt-in gives smaller but far healthier lists —
recommend it by default; see [list-building.md](list-building.md).

### Subscriber statuses (returned in subscriber info)

0 New · 1 Active · 2 Confirmation requested · 3 Activation requested ·
4 Unsubscribed (this book) · 5 Rejected · 6 Unsubscribed from all ·
7+ various delivery-error/blocked states.

Campaigns automatically skip everything that isn't sendable. **Never re-import
unsubscribed addresses to force delivery** — it violates consent, and the service
tracks it.

## Variables (personalization + segmentation fuel)

- Types: `string` (default), `number`, `date` (**format `YYYY-MM-DD` only**).
- Set on add (upsert) or individually:
  `POST /addressbooks/{id}/emails/variable` with `{"email": "...", "variables": [{"name": "...", "type": "...", "value": "..."}]}`.
- Used in emails as `{{variable_name}}` (the template side of this — fallbacks, system
  variables like `{{unsubscribe_url}}` — is `sendpulse-template-skill` territory).
- Used in segments as conditions (`number` and `date` types enable range conditions —
  prefer them over strings for anything you'll filter on).
- Keep a consistent naming scheme (`name`, `city`, `last_order_date`) — variables are
  per-book, and a messy schema makes segmentation painful later.
- `GET /addressbooks/{id}/variables` shows what exists; there is a per-book cap on
  the number of variables, so don't create one-off junk variables.

## Tags (Pro plan and above)

Cross-book labels on contacts:

| Method | Path |
|---|---|
| GET/POST | `/tags` (create: `{"name","color"}`) |
| PUT/DELETE | `/tags/{id}` |
| POST | `/tags/pin/email` / `/tags/unpin/email` — `{"email": "...", "tags": [ids]}` |

Use tags for facts that span books (VIP, source=webinar); use variables for per-book
data you'll template or segment on.

## Account-wide blacklist

Suppression across ALL books and campaigns:

| Method | Path | Notes |
|---|---|---|
| GET | `/blacklist` | Current list |
| POST | `/blacklist` | `{"emails": "<Base64 of comma-separated addresses>", "comment": "..."}` |
| DELETE | `/blacklist` | `{"emails": "<Base64 of comma-separated addresses>"}` |

⚠️ Note the format difference: blacklist `emails` is a **Base64-encoded
comma-separated string**, not a JSON array. Wire your app's global opt-outs and
complaint handling here.

## Import hygiene rules (enforce in any integration you build)

1. Import only opt-in addresses; keep the consent source recorded (a `source`
   variable is a good habit).
2. Validate doubtful/old lists with SendPulse **Email Verifier** before importing —
   bounces from a dirty list damage the account's reputation and can block sends.
3. Deduplicate on your side when syncing regularly (the upsert behavior helps).
4. Batch big imports; respect the 100-address cap on DELETE calls.
5. Mirror your app's unsubscribes to SendPulse immediately (book-level unsubscribe
   or account-level blacklist).
