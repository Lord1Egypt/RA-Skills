# Default design

Current version: **0.1.3**

## Purpose
`rolling-suds-workiz-lead-runner` is the read-only orchestration layer for Workiz lead review.

## Scope
Current scope is intentionally narrow:
- leads
- associated client data

No write-back.
No unrelated Workiz objects.

## Current constraint
The user does not currently have permission to create a Workiz developer account or generate an API token.
So the skill must work now from pasted/exported lead data and remain ready for future API integration.

## Skill chain
1. `rolling-suds-customer-quote-intake`
2. `residential-property-rolling-suds-estimator`
3. `rolling-suds-workiz-note-builder`

## Good behavior
- process pasted data cleanly
- separate lead facts from client facts
- estimate only when enough data exists
- preserve manual-review and follow-up flags
- be explicit when API automation is blocked by permissions
- provide a top-level required-missing-data summary when reviewing multiple pasted leads

## Future API target
When credentials exist, support read-only pulls for:
- today's leads
- a specified day's leads
- associated client data for each lead

## Important principle
This skill should be useful even before API access exists.
That means manual-mode quality matters just as much as future automation.
