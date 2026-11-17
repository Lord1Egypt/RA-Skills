# Audit report template and launch-readiness checklist

Use this to turn the data from `workflows.md` playbook 1 into one report the owner can act on. It was shaped by a
live pre-opening audit of an apparel store. Write plainly: the reader is a business owner, not a developer.

## Report skeleton

```
# <Store> pre-opening audit, <date>
Verdict: READY / NOT READY / READY WITH CONDITIONS  (one sentence why)
Method: what was read (API, public pages, admin screens), what scopes were used, "nothing was changed".

## Fix first (ordered)
1. <action> - why it blocks opening - where to click in Shopify admin
...

## The Ugly (blocks opening)
- <finding> [API|Screen|Public|Inferred]

## The Bad (fix soon)
## The Good (working, keep)

## What was not covered
<each item the audit could not check, and why>

## How this report was checked
<queries run, counts reconciled, anything re-verified>
```

Rules for the report:
- Tag every finding with its evidence: `[API]` read from Shopify, `[Screen]` seen in the admin UI, `[Public]` seen
  on the public storefront, `[Inferred]` reasoned but not seen. Do not state an `[Inferred]` item as fact.
- Order "Fix first" by what stops sales or money, then legal text, then polish.
- Give counts, not adjectives ("3 of 18 products are active", not "few products are live").
- Never claim a payment, tax or checkout setting is correct unless someone looked at that screen.
- Keep customer data out of the report. Counts and consent states only.

## Launch-readiness checklist

Blockers (stops opening):
- Payment provider is in live mode, not test mode, and a real checkout has been completed by the owner.
- Every product meant to sell is ACTIVE, priced above zero, and published on the sales channel.
- Every ACTIVE product's delivery profile can ship to the countries the store says it serves (a zone for each
  target country or a Rest-of-World zone).
- Policy pages (refund, shipping, privacy, terms, cancellations) have no template placeholders such as `[Your Email]`.
- Store password is removed only when the owner decides to open.

Should fix before launch:
- SEO title and description, image alt text, category and barcode on active products.
- Unit costs set so margin can be reported.
- Menus link to the shop and to the policies; redirects point to pages that exist.
- Test gift cards removed or disabled; discount codes have end dates.
- Analytics and ad pixels you intend to use are installed and firing (this needs a browser check, not the API).

Cannot be checked from the API (say so in the report):
- Whether a payment provider is in live or test mode on the provider side, tax settings, checkout settings,
  staff 2FA, notification sender address, order routing, a rendered storefront behind a password, confirmation
  emails, vendor order flow.

## After the report
Offer the owner a short "next 3 actions" list. If they want the changes made for them, point to `shopify-admin-pro`,
which can apply them with preview and confirmation. This skill itself cannot change the store.
