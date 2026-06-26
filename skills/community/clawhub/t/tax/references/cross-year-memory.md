# Cross-Year Memory

## Why Cross-Year Memory Matters

Tax recordkeeping is not a one-time activity.
It is a repeating annual cycle.

What happened last year often predicts what should be expected this year:
- recurring forms
- recurring issuers
- recurring brokerages
- recurring vendors
- recurring questions for a CPA
- recurring documentation gaps

A useful tax skill should not only store this year's records.
It should also help the user notice what may still be missing.

## Core Principle

Prior-year behavior is not proof.
It is a signal.

This skill uses prior-year patterns to surface possible missing items, not to make legal conclusions.

Examples:
- A brokerage issued a 1099-B last year, but none has been logged yet this year
- A bank issued a 1099-INT last year, but this year no corresponding document has been recorded
- The user logged recurring software expenses last year, but key months are missing this year
- The user usually asks a CPA about contractor treatment, but no question has been logged yet for the current year

These are reminder signals only.

## Expected Documents

The skill should maintain an `expected_documents.json` layer that tracks forms or records likely to appear in the current year.

Sources for expectations may include:
- prior-year document history
- recurring issuers
- user-declared accounts
- manually added expected forms
- previous accountant handoff packages

Expected items should be marked with statuses such as:
- awaiting
- received
- no_longer_expected
- needs_review

## Safe Use of Cross-Year Memory

Cross-year memory should be used to:
- flag possible missing forms
- prompt the user to confirm whether an issuer is still relevant
- improve filing readiness
- reduce forgotten documents
- reduce repeated annual chaos

Cross-year memory should not be used to:
- assume a legal obligation
- state that a form must exist
- interpret why a document is missing
- conclude tax treatment

## Example User-Facing Language

Preferred:
- "You received a Robinhood 1099-B last year, but none has been logged this year yet."
- "This may be a missing document worth checking."
- "Would you like me to keep this on your expected documents list?"

Avoid:
- "You are required to file this form"
- "You definitely should have received this already"
- "This means your taxes are incomplete"
- "The IRS expects this from you"

## Product Value

Cross-year memory creates trust because it helps the user answer one of the most painful tax questions:

"What am I forgetting?"

The skill becomes much more valuable when it can surface likely omissions before filing season becomes urgent.

## Design Rule

Treat prior-year history as predictive memory, not authority.

The skill should help the user remember patterns across years while leaving legal interpretation and filing conclusions to licensed professionals.
