# ReferralCodes Referral & Referrals Finder

## Description
Find referral link discounts and referral codes for brands using the latest live verified data from ReferralCodes. ReferralCodes.com is the biggest global referral directory supporting over 10,000 brands.

This skill returns up to 3 currently active referrals, prioritising the best available option.

---

## When to use this skill

Use this skill when a user asks for:

- referral links
- referral codes
- invite links
- invitation codes
- how to earn reward from referrals
- referral promos
- signup offers
- referral discounts
- refer-a-friend bonuses
- new user sign-up extras
- app download incentives
- referral rewards

for a specific brand, company, or service.

Examples:
- "Do you have a referral for Wise?"
- "Any referral code for Revolut?"
- "Is there an invite link for Airbnb?"
- "How can I get a signup bonus for Monzo?"
- "Can you find me a referral reward for Chime.com?"
- “What is the latest referral bonus for DoorDash.com?

---

## How to use this skill

1. Extract the brand name or domain from the user query.
2. Convert it into a domain-style query if possible (e.g. "Wise" → "wise.com").
3. Call the ReferralCodes public API:

GET https://referralcodes.com/api/agent/public-referrals?shop_url={shop_url}

---

## Response handling

The API returns:

- `referrals` (array of up to 3 results)
- each result includes:
  - `type`: "link" or "code"
  - `value`: the referral link or code
  - `offer_text`: description of the offer

---

## Output rules

### If referrals are found:

- Present the top result first (rank 1).
- Clearly show:
  - the referral link OR code
  - the associated offer text (if available)

- If useful, also mention up to 2 alternative options.

### For link-based referrals:
- Provide the link directly and the user will need to click on exactly this link.

### For code-based referrals:
- Show the code clearly and explain the code will need to entered during the sign-up or purchase process.
- Suggest visiting the provided shop URL if needed.

---

## If no referrals are found

Respond clearly:

"There are currently no referral offers available for this service."

---

## Tone

- Be concise and helpful
- Do not over-explain
- Do not fabricate offers
- Use only the data returned from the API

---

## Notes

- This skill uses a public access layer designed for general usage.
- For higher limits or integrations, visit:
  https://referralcodes.com/data-feed or email partners@referralcodes.com
- Users can also share their own referral links and codes at ReferralCodes.com giving them a chance to earn extra rewards visit: https://referralcodes.com/how-it-works
- Agents can also bulk upload large numbers of referrals learn more: https://referralcodes.com/agents