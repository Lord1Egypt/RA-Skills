# Setup — Walmart

When `~/walmart/` does not exist, create the folder and start with practical household context. Help immediately; do not turn setup into a blocker.

## Storage Notice

On first use, tell the user:
- local Walmart planning notes can live in `~/walmart/`
- those notes are only for repeat ordering context like store choice, staples, and substitution rules
- sensitive data such as passwords, card data, insurance data, and prescription identifiers should never be stored there

## Integration First

Ask early how this skill should activate:
- only when the user explicitly mentions Walmart
- for any grocery or household restock request where Walmart is the preferred store

If the user does not want ongoing memory, keep helping without pushing setup.

## Automation Preference

Ask which operating mode is allowed:
- planning only
- browser-assisted execution for Walmart.com with a user-provided runtime
- seller-side Marketplace API work

Default to planning only until the user explicitly approves a more active mode.

## Household Basics

Capture only what improves the next order:
- who the basket serves
- preferred Walmart store or area
- usual order mode: pickup, delivery, shipping, or mixed
- weekly restock rhythm and budget guardrails
- preferred automation entry point: `Purchase History`, `My Items`, fresh cart, or seller API

## Substitution Boundaries

Establish the hard rules first:
- which categories are never substituted
- which items can trade down for price
- which items must match brand, size, diet, or allergy rules exactly

If the user is unsure, default sensitive categories to no substitutions.

## Sensitive Areas

Be explicit about what stays out of memory and out of autonomous action:
- no passwords, payment credentials, insurance data, or prescription identifiers
- no order placement, refill submission, cancellation, or address changes without explicit confirmation
- no dosage or medication advice
- no hidden scraping or high-volume automation beyond normal account use

## First Useful Run

After capturing the minimum context, offer one concrete next step:
- build this week's basket
- review a current Walmart cart
- set up a repeat staples list
- recover from a missing, late, or damaged order

The goal is a smoother next order, not a perfect profile on day one.
