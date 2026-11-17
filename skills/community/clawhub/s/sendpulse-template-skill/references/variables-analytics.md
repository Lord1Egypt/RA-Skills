# Variables, UTM, Analytics, A/B Testing & Unsubscribe

> Read this for SendPulse personalization variables, UTM tagging, click/open analytics, A/B tests,
> and the legally required unsubscribe. These turn a static template into a trackable, personalized,
> optimizable campaign.

## Table of Contents
1. SendPulse variables (standard + custom)
2. UTM tagging
3. Analytics / tracking settings
4. A/B testing
5. Unsubscribe & legal footer

---

## 1. SendPulse variables

**Standard service variables** (auto-filled by SendPulse):

| Variable | Use |
|---|---|
| `{{unsubscribe_url}}` | Unsubscribe link — **required** in footer |
| `{{webversion}}` | "View in browser" link (preheader) |
| `{{current_year}}` | Copyright year |
| `{{ec_es_email_sender_company}}` | Sender company name |
| `{{ec_es_email_sender_address}}` | Sender physical address (legally required) |
| `{{name}}` | Subscriber first name |
| `{{email}}` | Subscriber email |

**Custom variables** — defined per mailing list (e.g. `{{city}}`, `{{plan}}`, `{{order_id}}`).
- Reference docs: SendPulse KB → "standard SendPulse service variables list", "how to create a
  custom variable", and "custom variable in a template".
- **Always provide a fallback** for personalization so empty values don't break copy. Pattern:
  `{{name | "there"}}` style fallback (confirm exact SendPulse fallback syntax in the KB) or write
  copy that reads fine if the variable is blank ("Hi {{name}}," → ensure it degrades to "Hi,").
- Offer personalization where it adds value (greeting, order details, recommendations) — don't
  over-personalize for its own sake.

> ⚠️ **Variables do NOT resolve in test sends / previews.** In a test email, SendPulse shows stub
> placeholders instead of real values — e.g. `{{webversion}}` renders as
> `https://s<id>.sendpul.se/stubs/en/webversion/`, and `{{unsubscribe_url}}`, `{{name}}`, etc. are
> likewise stubbed. This is expected and does NOT mean the template is broken. To verify real
> substitution, send an actual campaign to a mailing list that includes your own address. Tell the
> user this proactively when they test a template, so a stubbed link isn't mistaken for a bug.

## 2. UTM tagging

Tag in-email links so clicks attribute correctly in analytics.

**Convention (recommend the user fix one and reuse it):**
- `utm_source=sendpulse`
- `utm_medium=email`
- `utm_campaign=<campaign-slug>` (e.g. `spring_sale_2026`)
- `utm_content=<which link/block>` (e.g. `hero_cta`, `product_1`, `footer_link`) — distinguishes
  multiple links to the same URL.
- `utm_term=<optional, segment/variant>`

**Rules:**
- lowercase, no spaces (use `_` or `-`), consistent across campaigns.
- Add UTM to **content links and CTAs**, **never** to `{{unsubscribe_url}}` or `{{webversion}}`.
- SendPulse can auto-append UTM (Google Analytics tracking option) — if enabled, avoid double-tagging.
- Keep a shared UTM naming sheet so reports stay clean (a brand-profile.md can hold the convention).

## 3. Analytics / tracking settings

Remind the user to enable in the SendPulse campaign settings:
- **Open tracking** (tracking pixel) and **click tracking** (link wrapping) — on by default in most
  setups; confirm before sending.
- **Google Analytics / UTM** option if they use GA.
- After send, review open rate, CTR, click map, and unsubscribes to inform the next A/B test.

## 4. A/B testing

Run an A/B test when the list is **large enough** for the result to be meaningful.

- **Change ONE variable per test** — subject line, OR preheader, OR hero image, OR CTA label/color,
  OR send time. Changing several at once makes the result uninterpretable.
- Highest-leverage first: usually **subject line** (drives opens), then **CTA** (drives clicks).
- Send variants to comparable random splits; let SendPulse pick the winner by your metric (opens for
  subject tests, clicks/conversions for content tests).
- Wait for adequate sample / significance before declaring a winner; don't call it on 20 opens.
- Use the multiple subject lines from content-copywriting.md as ready A/B candidates.

## 5. Unsubscribe & legal footer

- `{{unsubscribe_url}}` is **mandatory** (CAN-SPAM / GDPR / local law). Never hide or fake it.
- Include the sender's **physical postal address** (`{{ec_es_email_sender_address}}`).
- For reactivation, also offer a **preference/frequency update** link — softer than a full opt-out.
- Make unsubscribe visible and one-click; it lowers spam complaints and protects deliverability.
