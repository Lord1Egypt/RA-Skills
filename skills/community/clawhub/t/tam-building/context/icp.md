---
title: Ideal customer profile
description: Who we sell to, and who we do not. The sourcing filter answers to this file, and so does every skill that later scores, enriches or routes the companies it produces.
---

# Ideal customer profile

PLACEHOLDER. This is a worked example for a company selling GTM automation to
technical revenue teams. Replace every line with yours before deploying, and
keep it in the workspace context repo rather than in a prompt or a model
config: the sourcing filter is derived from this file, and so is every tier a
scoring skill writes later.

## Who buys

B2B software, developer infrastructure, and security companies that already run
a technical go-to-market motion, or are visibly staffing one. The buying signal
is a person: a GTM engineer, a technical RevOps lead, or a growth engineer with
a mandate to automate rather than to report.

## Where this came from

Written from the company's own evidence, not from a brainstorm:

- Website and positioning: who the homepage, pricing page and product pages say
  the product is for
- Customer stories: the named customers on the site, and what their case
  studies say they bought it to fix
- Those customers' LinkedIn company pages: the industry, headcount band,
  headquarters and specialties they share

A line below that no customer supports is a hypothesis. Say so next to it.

## Firmographics

Each line maps to an AI Ark filter group, noted in brackets.

- Industry: software development, IT services and consulting, internet and
  technology, computer and network security [`industry`]
- Headcount: 20 to 500 [`employeeSize`]
- Ownership: privately held or public [`companyType`]
- Persona already employed: GTM engineer, growth engineer, revenue, marketing
  or sales operations [`employeeRole`]
- Countries: United States, United Kingdom, Canada, Ireland, Australia; the
  buying committee operates in English [`companyLocation`]

## Disqualifiers

Any one of these puts a company outside the TAM. Express each as a `_not`
filter where AI Ark has the field, so it is never sourced or paid for.

- Above 500 employees. The 500 to 5,000 band is out of scope, not an exception
- Consumer, marketplace, or services-only businesses with no software product
- Agencies and consultancies with no in-house automation practice
- Already committed to a competing platform on a multi-year contract (no
  filter holds this; it is for whoever works the account)
