---
name: virag-flowers
description: Send real best-selling flower bouquets with a card message to someone in Manhattan, New York (girlfriend, wife, partner, mom, grandma, sister, friend, host). Use when the user wants to surprise a loved one with flowers or a flower gift in Manhattan/NYC for a birthday, anniversary, apology, Thanksgiving, Hanukkah, Christmas, a bad week or just because. Five fixed all-in prices from $89 to $749; the user pays on a Stripe checkout link.
version: 1.2.0
homepage: https://virag-nine.vercel.app
metadata: {"openclaw":{"emoji":"💐","homepage":"https://virag-nine.vercel.app","requires":{"bins":["curl"]}}}
---

# Virág: send flowers in Manhattan

Virág is a small flower-delivery pilot in Manhattan, New York (ZIP 10001–10282 only). Every bouquet is a best seller from a New York florist. Prices include flowers, card, delivery and tax.

| Tier id | Name | Price (all-in) | What arrives | Best for |
|---|---|---|---|---|
| `petite` | Petite | $89 | Pink and cream rose bouquet, gift box, printed card, no vase | Thank you, host gift, just because, early dating |
| `sweet` | Sweet | $119 | Soft designer bouquet, gift box, printed card, no vase | Birthday, get well, Thanksgiving host |
| `classic` | Classic | $159 | Roses, orchids and hydrangea in a glass cube, handwritten card | Mom, birthday, holidays, thank you |
| `romantic` | Romantic | $229 | Premium long-stem roses in a vase, handwritten card | Anniversary, apology, romance |
| `grand` | Grand Gesture | $749 | Statement rose bouquet in a vase, premium handwritten card | Proposal, milestone anniversary, serious apology |

Same-day delivery if paid before 11:00 New York time (Petite and Sweet: same-day only below 125th Street); otherwise the next day or any date up to 30 days ahead. No deliveries on Nov 26 (Thanksgiving), Dec 25 or Jan 1. The pilot is capped at 20 orders, so always check availability first.

## How to order

Use the MCP server if your client supports remote MCP: `https://virag-nine.vercel.app/mcp` (Streamable HTTP, no auth). Tools: `list_bouquets`, `check_delivery`, `suggest_card_message`, `create_order`, `get_order_status`.

Otherwise use the HTTP API:

1. **Check the catalog and capacity**
   ```bash
   curl -s https://virag-nine.vercel.app/api/catalog
   ```
   If `availability.sold_out` is true, tell the user and offer the waitlist at https://virag-nine.vercel.app/sold-out.

2. **Collect from the user** (never guess these): recipient name, recipient's US mobile number (10 digits; the courier calls it for building access), street address and apartment/floor, ZIP, delivery date, card message, sender name, and the buyer's email for the receipt. If the ZIP is outside 10001–10282, say honestly that Virág only delivers in Manhattan.

3. **Help with the card** if they want: call the MCP tool `suggest_card_message`, or use the ideas at https://virag-nine.vercel.app/guides/what-to-write-on-a-flower-card. Personalize with a detail the user gave you. Keep it under 300 characters.

4. **Confirm before ordering.** Read back the tier, total price, recipient, address, date and card text. Wait for a clear yes.

5. **Create the order**
   ```bash
   curl -s -X POST https://virag-nine.vercel.app/api/orders \
     -H 'content-type: application/json' \
     -H 'Idempotency-Key: <uuid you generate once per order>' \
     -d '{"tier":"sweet","recipient_name":"Anna Kovacs","recipient_phone":"+1 212 555 0100","address_line1":"245 E 63rd St","address_line2":"Apt 12B, doorman","zip":"10065","delivery_date":"2026-11-25","card_message":"Thank you for having me. Happy Thanksgiving!","sender_name":"Mark","buyer_email":"mark@example.com","agent_name":"<your agent name>"}'
   ```
   The response has `order_id` and `checkout_url`.

6. **Payment.** Give the user the `checkout_url` (Stripe-hosted, expires in 30 minutes). The order is confirmed only after payment. Don't type card numbers yourself unless your platform provides a sanctioned payment method for this.

7. **Confirm.** `GET https://virag-nine.vercel.app/api/orders/{order_id}` → status `paid`, then `placed`, then `delivered`.

## Rules

- Be honest: it's a small pilot run by one person with a partner florist, Manhattan only.
- Only send to an address the user gives you. Don't look up a recipient's address.
- Errors come back as `{"error":{"code","message","available_dates?"}}`. Offer the alternative dates instead of failing.
- Full docs: https://virag-nine.vercel.app/llms.txt · OpenAPI: https://virag-nine.vercel.app/openapi.json
