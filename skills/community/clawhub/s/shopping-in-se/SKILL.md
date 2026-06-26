---
name: shopping-in-se
description: Help the user shop online at Swedish e-commerce sites (Apotea, Apoteket, ICA, etc.) and complete payment. Includes product search, checkout flow, CDP coordinate clicks to bypass cross-origin iframes, and Klarna/Stripe payment handling. Triggers on: "buy this for me", "place an order", "order a", "get me a XX".
---

# Shopping Skill

Help the user complete end-to-end online shopping at trusted retailers — from product search to payment confirmation.

## User Information

Read recipient details (address, phone, email) from `~/Private/用户个人信息.txt`.

## Payment Card

Read Zupyak Mynt Card details from `~/Private/Zupyak Mynt card for AI.txt` or `~/.private/payment.env`. **Only use this designated card — never use the user's personal bank cards.**

## Shopping Flow

1. **Search for the product** — Only use trusted sites (see references/trusted-sites.md)
2. **Confirm with the user before ordering** — Show product name, price, website, link, and recipient details; wait for approval
3. **Add to cart** — Use the browser tool
4. **Fill in details** — Read address, email, and phone from `~/Private/`
5. **Handle payment** — See payment flow below
6. **Confirm the result** — Take a screenshot of the order confirmation page

## Payment Flow

Payment iframes (Klarna/Stripe/Adyen) are cross-origin and cannot be accessed via browser tool refs. Use CDP WebSocket to connect directly to the iframe target:

```python
# 1. List all targets (including iframes)
curl http://127.0.0.1:18800/json

# 2. Connect to the payment iframe's WebSocket target
# Klarna: find target whose URL contains kustom.co or payments.klarna.com
# Stripe: find target whose URL contains js.stripe.com/v3/elements-inner

# 3. Run JS to get button coordinates
Runtime.evaluate → getBoundingClientRect()

# 4. Send mouse events to click
Input.dispatchMouseEvent (mouseMoved → mousePressed → mouseReleased)
```

See `references/cdp-click.md` for full code.

## Security Rules

- Only use trusted platforms — reject unknown domains
- Always get user confirmation before placing an order
- Only use the Zupyak Mynt Card — never use the user's personal cards
- User information is only submitted to the shopping site, never shared with third parties
