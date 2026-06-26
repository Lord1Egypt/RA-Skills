# Setup — Yelp

Read this when `~/yelp/` does not exist or is empty.

## Your Attitude

Be fast, local-intent-aware, and evidence-first. The user should get usable Yelp output in the first pass, not a long setup ritual.

## Priority Order

### 1. First: Integration

Confirm how this should activate in future sessions:
- activate for Yelp-specific business search, review analysis, and local comparison requests
- prefer API mode when `YELP_API_KEY` exists, or public-page mode by default
- stay read-only unless the user explicitly asks for owner-side drafts or listing audits

Store the activation preference and rationale in `~/yelp/memory.md`.

### 2. Then: Access and scope

Clarify only the minimum needed to run the first useful Yelp task:
- market or city
- business type or category
- decision type: discover, compare, review, or audit
- whether live API access is available now

If API access is missing, continue with public-page research and explain what structured fields may be unavailable.

### 3. Finally: First useful task

Capture only the filters that change the result:
- location or neighborhood
- price posture
- quality floor
- optional service flags such as delivery, takeout, or open now

Then run the first search or audit immediately and refine from real evidence.

## What You Are Saving Internally

In `~/yelp/memory.md`, store:
- activation preferences
- recurring cities, categories, and price filters
- accepted and rejected business patterns
- API availability, unsupported endpoints, and repeated blockers

Before the first write in a workspace, confirm that local files will be created under `~/yelp/`.

## When Done

Once activation behavior and the first decision context are known, execute the Yelp workflow. Learn from accepted and rejected options rather than guessing long preference lists up front.
