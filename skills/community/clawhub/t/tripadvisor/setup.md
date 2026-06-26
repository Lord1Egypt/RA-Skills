# Setup — Tripadvisor

Read this when `~/tripadvisor/` does not exist or is empty. Explain local storage behavior in plain language and ask for confirmation before creating files.

## Your Attitude

Be fast, concrete, and compliance-first. The user should get actionable Tripadvisor results without legal or policy ambiguity.

## Priority Order

### 1. First: Integration

Within the first exchanges, confirm activation behavior:
- Should this activate whenever the user mentions Tripadvisor, hotels, attractions, or restaurant comparisons?
- Should API mode be preferred by default when an API key is available?
- Should UI mode be used when users want visual verification before deciding?

Save these preferences in `~/tripadvisor/memory.md` so this skill behaves consistently in future sessions.

### 2. Then: Access readiness

Confirm operational prerequisites:
- Is `TRIPADVISOR_API_KEY` available now?
- Is browser navigation acceptable for UI verification?
- Should outputs focus on hotels, restaurants, attractions, or mixed?

If API key is missing, continue in UI mode and explain tradeoffs.

### 3. Finally: Task context

Capture only what is needed to run the first useful query:
- destination
- user intent (stay, eat, do)
- budget posture and quality threshold
- optional date window

Then execute immediately and iterate from real results.

## What You Are Saving Internally

In `~/tripadvisor/memory.md`, store:
- activation preferences (API/UI/hybrid)
- recurring destination and budget patterns
- accepted/rejected shortlist reasons
- known blockers (consent dialogs, anti-bot interstitials, API errors)

Before the first write in a session, confirm the update explicitly.

## When Done

Once activation behavior and first-query context are known, run the workflow. Refine preferences from actual trip decisions.
