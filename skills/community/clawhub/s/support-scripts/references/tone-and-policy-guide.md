# Tone & Policy Guide

How to set the voice that every script inherits, the guardrails that keep replies compliant, the empathy pattern that defuses upset customers, and the cautions that keep localized scripts from breaking.

## Defining Brand Voice

Pick a position on each slider and write it into the library header so every script is consistent.

- **Register (casual ↔ formal):** Most DTC brands land warm-professional. Match your product and audience — a streetwear brand on TikTok Shop sits casual; a skincare or supplement brand sits a notch more measured.
- **Warmth (transactional ↔ personal):** Higher warmth means using the customer's name, acknowledging feelings, and writing like a person. Even efficient brands should clear a warmth floor — never cold.
- **Formality (slang/emoji ↔ plain prose):** Decide an emoji rule (e.g. "one max, never on a complaint or refund") and a contraction rule (contractions read friendlier). Be stricter on serious tickets.
- **Energy (calm ↔ upbeat):** Upbeat suits pre-sale and promo replies; dial energy down for complaints, refunds, and anything involving money or safety.

Write 3-5 voice rules and 2-3 "we don't sound like this" examples. Concrete anti-examples ("not 'Dear valued customer'", "not 'lol no worries'") guide agents faster than adjectives.

### Channel adaptation

- **TikTok Shop chat:** short, fast, scannable; one idea per message; light emoji allowed in friendly contexts; lead with the answer.
- **Shopee chat:** concise and polite; SEA markets skew more formal and courteous; quick replies expected.
- **Shopify email:** fuller, complete sentences, clear structure, an explicit next step and sign-off.

The same scenario should exist in a short chat variant and a fuller email variant — do not reuse one length everywhere.

## Platform Policy Guardrails

Keep these general and accurate; always defer to each platform's current seller policies and your own store policy, which override anything here.

- **Refunds:** Only promise refunds you're authorized to issue. On Shopify you control refunds directly, so you can confirm and state the bank window (typically several business days). On Shopee and TikTok Shop, buyer-protection and dispute systems often govern outcomes — phrase as "I'll process/request this" rather than guaranteeing a result you don't fully control. Never invent a faster timeline than the payment processor allows.
- **Shipping & delivery dates:** Give estimated windows, not guarantees. Carrier delays are common and a hard promise you miss becomes a worse ticket. Use "expected by `{{eta_date}}`" and explain customs/peak-season variability for cross-border orders.
- **Returns & exchanges:** State your published window and condition rules; apply goodwill exceptions as clearly limited one-offs, not new policy. On marketplaces, return eligibility and who pays return shipping may be set by platform rules — reflect that, don't contradict it.
- **Compensation:** Pre-define a tiered, capped ladder (reship → partial credit → coupon → full refund) so agents don't improvise. Lead with fixing the problem, not paying it off.
- **Off-platform steering:** Marketplaces (TikTok Shop, Shopee) restrict pushing buyers to contact or pay off-platform. Keep transactional conversation on-platform; don't share external payment links or ask buyers to cancel-and-reorder elsewhere.
- **Sensitive claims:** For injury, illness, allergic reaction, or safety claims, do not admit fault, diagnose, or promise outcomes — acknowledge, gather facts, and escalate immediately per your do-not-say rules.

## Empathy Pattern: Acknowledge → Align → Act

A reliable three-beat structure for any complaint or upset customer:

1. **Acknowledge** — name the specific problem and the feeling. "A melted candle is not the welcome we wanted to send." Avoid the non-apology ("sorry you feel that way").
2. **Align** — show you're on their side and take ownership where it's yours. "That's on us." Don't make excuses or blame the carrier/customer.
3. **Act** — state the concrete fix and exactly what happens next, with a timeframe. "I've shipped a free replacement today; tracking by `{{eta_date}}`."

Close by inviting a reply and, where appropriate, a relationship repair (not a reflex discount). For public negative reviews, do beats 1-2 publicly and beat 3 privately, then invite an updated review only after the issue is resolved.

## Localization & Translation Cautions

- **Localize voice, not just words.** Word-for-word translation breaks tone. Politeness levels and directness differ — SEA markets on Shopee generally expect more formal courtesy than a casual US TikTok Shop tone.
- **Use native review.** Have a native speaker check each localized set for register, idioms, and accidental rudeness; machine translation alone is a risk on refunds and complaints.
- **Watch placeholders in translation.** Don't let `{{ }}` tokens get translated or word order break them; verify variables still render correctly after localization.
- **Adapt formats, not just language.** Date formats, currency symbols, name order, and honorifics vary by market; bake the right format into each locale's scripts.
- **Keep one source of truth.** Maintain a master scenario list and derive localized versions from it so a policy change updates every language, not just English.
