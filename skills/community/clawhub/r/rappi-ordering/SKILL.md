---
name: rappi-ordering
description: Assisted Rappi ordering through the local openclaw-rappi HTTP service. Use when the user asks to order food, groceries, pharmacy, convenience items, lunch, snacks, household basics, or anything “por Rappi”. The skill structures the request, creates a cart draft in visible Chrome, summarizes cart/checkout, prepares review handoff, sends a native approval button when available, and submits the final purchase only after exact explicit approval in the current chat.
---

# OpenClaw Rappi

Use the local service at `http://127.0.0.1:4777` unless configured otherwise.

## Setup check

1. Call `GET /health` before the first order in a session.
2. If unavailable, bootstrap the local service from GitHub automatically before asking the user for help. Run this once, then re-check `GET /health`:

```bash
set -euo pipefail
INSTALL_DIR="${OPENCLAW_RAPPI_DIR:-$HOME/.openclaw/tools/openclaw-rappi}"
mkdir -p "$(dirname "$INSTALL_DIR")"
if [ -d "$INSTALL_DIR/.git" ]; then
  git -C "$INSTALL_DIR" pull --ff-only
else
  git clone https://github.com/zarruk/openclaw-rappi.git "$INSTALL_DIR"
fi
cd "$INSTALL_DIR"
npm install
npm run build
if [ "$(uname -s)" = "Darwin" ]; then
  ./scripts/install-launchd.sh
else
  mkdir -p logs
  nohup npm start > logs/service.out.log 2> logs/service.err.log &
fi
```

3. Do not use `npm install -g openclaw-rappi`; the public distribution is GitHub + ClawHub, not npm.
4. If the bootstrap command fails, report the exact blocker and the last relevant stderr lines. Do not continue to cart creation until the service is healthy.
5. If Chrome CDP is unavailable, ask the user to open a dedicated visible Chrome profile and log in to Rappi:

```bash
mkdir -p "$HOME/.openclaw/rappi-chrome-profile"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.openclaw/rappi-chrome-profile" \
  --no-first-run --no-default-browser-check \
  https://www.rappi.com.co/
```

## Hard safety rules

- Never click or cause the service to click final purchase actions (`Pedir`, `Pagar`, `Confirmar compra`, `Realizar pedido`, `Place order`, or equivalents) unless the user has explicitly approved that exact order in the current chat after receiving the checkout summary.
- Approval is per-order and single-use. Do not infer approval from “sí”, standing instructions, previous orders, or vague confirmations.
- The required approval phrase is exactly: `APRUEBO COMPRA RAPPI <draftId>`.
- In Telegram direct chats, send the approval request with native top-level `buttons`, never only as a plain assistant reply. Button label: `Aprobar compra`; `callback_data`: `APRUEBO COMPRA RAPPI <draftId>`.
- Include the exact phrase in the approval message body as fallback, on its own short line.
- Treat a button callback/value that exactly equals `APRUEBO COMPRA RAPPI <draftId>` as explicit approval for that draft.
- After approval, call `POST /drafts/:id/confirm-purchase` with the exact approval text. Do not manually click final purchase buttons through browser automation unless the service endpoint is unavailable and the user explicitly approves that fallback in the same chat.
- Stop if the visible total, address, items, payment method, delivery estimate, or checkout state differs materially from the summary the user approved.
- Stop and ask for manual intervention if Rappi shows login, captcha, 2FA, age verification, alcohol, tobacco, prescription medication, identity validation, payment changes, address changes, or other sensitive screens.
- Do not modify saved addresses, payment methods, phone, ID, or personal data unless the user explicitly asked for that exact change.
- If the user gave a budget and the visible total/subtotal exceeds it, stop and ask.
- If there is important ambiguity before touching the cart, ask one concise question first.
- Do not use Rappi private/internal APIs or attempt to bypass anti-fraud, captchas, validation, or limits.

## Workflow

1. Parse the request into:
   - `category`: `restaurant`, `grocery`, `pharmacy`, `convenience`, or `unknown`.
   - `items`: names, quantities, notes.
   - `preferences`: budget, dietary preferences, preferred store, address hint, substitution policy.
   - If the user explicitly asks to “dejar listo para pagar”, “llevar hasta checkout”, “hasta el final”, or equivalent, set `handoffTarget: "checkout"`. Otherwise use `handoffTarget: "cart"`.
   - `safety`: always `{ "requireHumanFinalCheckout": true, "restrictedItemsAllowed": false }`.
2. Create draft with `POST /drafts`.
3. Poll `GET /drafts/:id` occasionally until status is `cart_ready`, `checkout_ready`, `needs_user_input`, `blocked`, or `failed`.
4. Summarize:
   - store/restaurant
   - products and quantities
   - missing items
   - substitutions
   - visible subtotal/shipping/total
   - visible delivery address
   - payment method label/last digits when visible
   - delivery estimate
   - warnings
5. If `handoffTarget` is `cart`, ask whether to prepare checkout for review.
6. If the user wants checkout prepared, call `POST /drafts/:id/prepare-checkout`, then poll again.
7. If the user wants the purchase completed, show the checkout summary and request approval.
8. In Telegram, use:

```json
{
  "action": "send",
  "channel": "telegram",
  "target": "telegram:<chat-id>",
  "message": "<checkout summary>\n\nAPRUEBO COMPRA RAPPI <draftId>",
  "buttons": [[{"text":"Aprobar compra","callback_data":"APRUEBO COMPRA RAPPI <draftId>","style":"success"}]]
}
```

If using `message action=send` for the user-visible approval request, reply with `NO_REPLY` in the main assistant response to avoid duplicate messages.

9. Only after the exact approval phrase appears in the current chat or button callback, call:

```bash
curl -X POST http://127.0.0.1:4777/drafts/<draftId>/confirm-purchase \
  -H 'Content-Type: application/json' \
  -d '{"approvalText":"APRUEBO COMPRA RAPPI <draftId>","approvedBy":"user"}'
```

10. Report success/blocker immediately. Never fabricate order confirmation; if Rappi status is unclear, say so.

## API reference

- `GET /health`
- `GET /capabilities`
- `POST /drafts`
- `POST /drafts/adopt-checkout` — advanced recovery endpoint for adopting a currently visible checkout screen into a new draft; use only when the service lost draft state but Rappi is already at checkout.
- `GET /drafts/:id`
- `POST /drafts/:id/prepare-checkout`
- `POST /drafts/:id/confirm-purchase`
- `POST /drafts/:id/cancel`

Example `POST /drafts` body:

```json
{
  "requestText": "Quiero algo saludable por menos de 80 mil",
  "category": "restaurant",
  "items": [
    { "name": "algo saludable", "quantity": 1, "notes": "máximo 80000 COP" }
  ],
  "preferences": {
    "budgetMax": 80000,
    "dietary": [],
    "allowSubstitutions": false,
    "handoffTarget": "cart"
  },
  "safety": {
    "requireHumanFinalCheckout": true,
    "restrictedItemsAllowed": false
  }
}
```
