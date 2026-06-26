---
name: rolling-suds-workiz-lead-runner
description: Read-only Rolling Suds workflow for processing Workiz leads and associated client data. Use when the user wants to review current-day or specific-day leads, pasted/exported Workiz lead data, or future Workiz API lead results, then run them through rolling-suds-customer-quote-intake, residential-property-rolling-suds-estimator, and rolling-suds-workiz-note-builder.
homepage: https://github.com/mwdearing/rolling-suds-workiz-lead-runner
metadata:
  {
    "openclaw":
      {
        "emoji": "📋"
      },
  }
---

# Rolling Suds Workiz lead runner

Current skill version: **0.1.6**

Process Workiz lead data in a read-only way.

## Purpose

This skill is for reviewing Workiz **lead** data and associated **client** data, then running that information through the existing Rolling Suds skills.

In manual mode, the primary key is the **Workiz Lead #**.

For now, this skill is **read-only**.
It should not create, update, or delete anything in Workiz.

## Current operating modes

### Mode 1: Manual / pasted Workiz data
Use when the user provides:
- pasted Workiz lead text
- copied lead details
- exported daily lead content
- lead + client data copied from Workiz screens

Require the **Lead #** when possible for manual processing, since that is the correct lead-stage identifier for estimates before conversion into a job.

### Mode 2: Future API mode
Design the workflow so it can later use the Workiz API when proper credentials/permissions exist.

Do not pretend API access exists if token access is blocked.

## Allowed data scope

This skill is only for:
- **leads** data
- associated **client** data connected to a given lead

Do not expand scope into unrelated Workiz objects unless the user later asks for it.

## Downstream skill chain

When enough data exists, process each lead through:
1. `rolling-suds-customer-quote-intake`
2. `residential-property-rolling-suds-estimator`
3. `rolling-suds-workiz-note-builder`

## Read-only rule

- Never modify Workiz.
- Never write notes back to Workiz from this skill.
- Never claim that data was synced or updated in Workiz.
- Focus on analysis and note generation only.

## Output goals

For each lead, produce:
1. lead summary
2. client summary
3. cleaned intake
4. estimate if possible
5. Workiz-ready note
6. manual-review flags

Always preserve the **Lead #** in outputs when it is provided.

## Required data gate

Do not move forward into estimating if the address is missing.
Address is required.

If one or more pasted leads are missing required data such as address:
- stop estimate generation for those leads
- return a clear missing-required-data section
- add a top-level `Required Missing Data Summary` block when processing multiple leads
- group affected leads by missing field when useful
- ask for the missing data before proceeding

## Recommended output structure

For multiple pasted leads, prefer this structure:

```text
Required Missing Data Summary
Lead Summary
Client Summary
Intake Summary
Estimator Output
Workiz Note
Manual Review Flags
```

Use `Required Missing Data Summary` as a top-level triage block when one or more leads are missing required fields such as address.

If estimate quality is too weak, say so clearly and preserve the note/follow-up path.

## Manual mode workflow

1. Read the provided Workiz lead/client data.
2. Extract and preserve the Workiz Lead # as the primary manual-mode identifier.
3. Separate lead details from client details.
4. If customer/contact fields are absent, distinguish between "not included in pasted lead description" and truly unknown data.
5. Validate required data before continuing.
6. If address is missing, stop estimate generation for that lead and report the missing required field.
7. Normalize valid leads through `rolling-suds-customer-quote-intake`.
8. If enough estimate inputs exist, run `residential-property-rolling-suds-estimator`.
9. Build the final Workiz-ready note with `rolling-suds-workiz-note-builder`.
10. Mark anything unresolved as follow-up or manual review.

## Future API workflow

When API access exists later, this skill should support read-only API pulls for:
- current day leads
- specified day leads
- associated client records for those leads

Future API mode should use the lead record plus client fields attached to the lead so estimate context can be associated correctly before a lead becomes a job.

Until then, keep API usage conceptual and clearly blocked by permissions.

## API readiness notes

The user reported that Workiz has API documentation at `https://developer.workiz.com`, but their current account permission level does not allow developer-account/token creation.

Therefore:
- build the skill to be API-ready
- but keep the current implementation read-only and manual-input compatible
- do not invent token flows or pretend auth is available

## Interaction style

- Be practical.
- Keep lead-by-lead output clean.
- Favor operational usefulness over perfect formatting.
- Be explicit when something is blocked by missing permissions.

## Missing-data interpretation rule

When a pasted Workiz lead description blob does not include phone, email, or full address details, do not automatically claim the customer data is missing from Workiz.
Prefer wording like:
- not included in pasted lead description
- not present in provided blob

However, if the address is not present in the provided input, treat that as a hard blocker for estimate flow until the address is supplied.

Read `references/default-design.md` before major edits or iteration.
