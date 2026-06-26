# Browser Flow - Uber Eats

Use this flow when Uber Eats is being controlled through the user's real browser session.

## Read First

1. Confirm the active tab is actually Uber Eats.
2. Read the visible title, URL, account state, and active address.
3. If the address is missing, solve that before browsing merchants.
4. If the page is blocked or blank, jump to `access-fallbacks.md`.

## Main Flow

1. Entry:
   - sign in if needed
   - set or verify the delivery address
   - confirm whether the user wants meals, groceries, or convenience items
2. Discovery:
   - browse merchant cards or use search
   - compare ETA, fees, promo state, and ratings
   - open only the most relevant 1-3 merchants
3. Merchant:
   - verify merchant name, ETA, fees, and any promo before adding items
   - read menu sections before touching the cart
   - if the merchant is closed or low-signal, back out early
4. Cart:
   - inspect existing cart state before changing it
   - add or edit only what the user asked for
   - review notes, substitutions, and totals after every major edit
5. Checkout:
   - review order, delivery notes, payment method, tip, and total
   - stop for explicit confirmation before the final live order action

## Verification Loop

- After every navigation, re-read the page or capture a screenshot.
- Never assume a click worked because the tab stayed open.
- If the visible state is ambiguous, refresh the read before the next action.

## Practical Notes

- Official Uber Eats help says ordering starts with sign-in plus a delivery address.
- Official order flow then goes: choose merchant, add items, review order, check payment, add tip, place order, and track.
- Browser state can fail even when the service is up, so keep a fallback ready.
