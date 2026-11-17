# WhatsApp setup

WhatsApp Business Platform **Cloud API only**. This package never uses whatsapp-web.js,
Baileys or anything that automates a personal WhatsApp account. Each user brings their
own Meta app and WhatsApp Business Account (WABA). Generated from
`docs/platforms/whatsapp-setup.md`; edit it there. Facts checked 2026-10-24.

## 1. Meta app and WhatsApp product

1. Create an app at https://developers.facebook.com/apps with the use case
   "Connect with customers through WhatsApp", and pick (or create) a business portfolio.
2. The WhatsApp > API Setup page gives you a test business number, its
   **Phone number ID** and your **WhatsApp Business Account ID**.
3. The temporary token on that page expires quickly. Do not use it for real work.

## 2. Permanent token (System User)

1. Business Settings > Users > System users > Add (role: Admin or Employee).
2. Assign assets: your app (Manage app) and your WABA (Manage WhatsApp Business accounts).
3. Generate token with `business_management`, `whatsapp_business_management` and
   `whatsapp_business_messaging`. Choose the expiry you want.
4. Store it outside any repository, for example in `~/.config/social-skills/env.sh`
   (mode 600):
   ```sh
   export WA_ACCESS_TOKEN="..."
   export WA_PHONE_NUMBER_ID="..."
   export WA_WABA_ID="..."
   export WA_APP_SECRET="..."    # App settings > Basic > App secret (support bot)
   export WA_VERIFY_TOKEN="..."  # any long random string you choose (support bot)
   ```

## 3. Real phone number

You must own it; it needs a country and area code and must receive SMS or a voice call.
A number registered with the Cloud API can no longer be used with the WhatsApp app.
New business portfolios can register 2 numbers (20 after business verification).

## 4. Limits that affect these skills

- **Opt-in:** you may only message people who gave you their number and opted in to
  receive messages from your business, by name. Honour every opt-out, on or off WhatsApp.
- **24-hour customer service window:** opened each time a customer messages you. Inside
  it you may send free-form replies; outside it only approved templates.
- **Messaging limit:** unique customers you can start conversations with per rolling
  24 hours, per business portfolio: 250, then 2,000 (business verification or quality
  history), 10,000, 100,000, unlimited.
- **Throughput:** 80 messages per second per number by default.
- **Templates:** 250 per WABA until the portfolio is verified; review takes up to 24 hours.
- **Marketing templates are not delivered to US numbers** (+1 US area codes).
- **AI assistants:** since 2026-01-15, Meta's WhatsApp Business terms (section 4.7)
  prohibit general-purpose AI assistants as the primary functionality. The support bot
  in this package answers only from your approved knowledge base and has no AI model.

## 5. Pricing (from 2025-07-01 per message; changes on 2026-10-01)

- Charged per delivered template message by category (marketing, utility,
  authentication) and recipient country.
- From 2026-10-01: utility templates inside the service window are no longer free, and
  service (free-form) replies are charged after 1,000 free per month per number.
- There is no pricing API. Copy the rates you need from the rate card into `rates.json`;
  see the socialkit-whatsapp-broadcast skill's references/pricing.md.
- Rate card: https://business.whatsapp.com/products/platform-pricing

## 6. Webhooks (support bot only)

Meta delivers incoming messages to a public HTTPS URL with a valid certificate
(self-signed is rejected). Run the bot locally and expose it with a tunnel, for example
`cloudflared tunnel --url http://127.0.0.1:8787`, then in the App Dashboard >
WhatsApp > Configuration set the callback URL and your `WA_VERIFY_TOKEN`, and subscribe
to the `messages` field. Every request is checked against `X-Hub-Signature-256` with
your app secret.

## 7. Sources

- Get started: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
- Templates: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview
- Messaging limits: https://developers.facebook.com/docs/whatsapp/messaging-limits
- Pricing: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Opt-in: https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in
- Terms (section 4.7): https://www.facebook.com/legal/Meta-Terms-for-WhatsApp-Business-Platform
- Error codes: https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes
