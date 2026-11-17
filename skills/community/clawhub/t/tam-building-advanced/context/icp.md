---
title: Ideal customer profile
description: Who we sell to, and who we do not. Every source filter in the TAM answers to this file, and so does the category list every company is classified into.
---

# Ideal customer profile

PLACEHOLDER. This is a worked example for a company selling GTM automation to
B2B software companies. Replace every line with yours before deploying, and
keep it in the workspace context repo rather than in a prompt or a model
config: four source filters and the classifier are derived from this file,
and they only agree with each other because they agree with it.

## Who buys

B2B software companies with 51 to 1,000 people, headquartered in North
America or Western Europe, that sell to other businesses: SaaS, AI software,
developer tools, data and cloud infrastructure, security, fintech software.

## Where this came from

- Website and positioning: who the homepage and pricing page say the product
  is for
- Customer stories: the named customers on the site
- Those customers' LinkedIn company pages: industry, headcount, headquarters

A line below that no customer supports is a hypothesis. Say so next to it.

## Firmographics

Each line maps to every source. The paths are in `references/configure.md`.

- Industries: B2B software of the kinds above
- Headcount: 51 to 1,000 employees on LinkedIn
- Countries: United States, Canada, United Kingdom, Ireland, France, Germany,
  Netherlands, Spain

## Categories

The values every company is classified into, from its own description. Use the
values of the industry field in your CRM, so the TAM, the CRM and the reports
use the same words. Mirrored in `infra/settings.ts`.

- B2B SaaS
- AI software
- Developer tools
- Data infrastructure
- Cloud software
- Cybersecurity
- Fintech software

## Disqualifiers

A company that matches one stays in the TAM model, flagged `out_of_scope` with
the reason, so you can see what each source returned that was not your market.

- IT services, consultancies and agencies, whatever their LinkedIn industry
- Consumer products, financial institutions, hardware
- Subsidiaries, country pages and acquired brands of a larger company
- Outside the headcount band or the countries above
