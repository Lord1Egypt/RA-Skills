# US SaaS pricing mechanics

Reference for the SaaS Pricing Tiers skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Cost before price

- Support cost per account per month, from the support log.
- Onboarding and setup cost per account.
- Infrastructure and third-party cost per user or per API call.
- Payment processing cost, including the fixed fee.
- Churn: a tier priced below its serve cost loses money on every renewal.

## Structure that works

- A no-cost tier with a hard cap and no human support.
- An entry tier priced at a multiple of its serve cost.
- A growth tier that counts the unit the buyer already tracks.
- An enterprise tier priced by contract rather than by list.
- Annual prepay pricing and monthly pricing shown side by side.

## US details that bite

- Sales tax in most states, collected on the state's taxable base.
- Processing fees are commonly kept on a refunded sale, so refunds reduce net margin.
- Legacy pricing needs its own line in the model.
- Confirm the economic nexus position before you quote tax-inclusive pricing.
