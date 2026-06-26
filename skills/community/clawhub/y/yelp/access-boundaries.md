# Yelp Access Boundaries

This skill must stay inside official or visible-access behavior.

## Allowed modes

- Official Yelp API requests with a valid `YELP_API_KEY`
- Normal browser navigation of public Yelp pages
- User-approved listing audits, response drafts, and comparison notes

## Hard rules

- No hidden scraping or blocked-content extraction
- No CAPTCHA bypass, anti-detection tricks, or rate-limit evasion
- No owner-side action without explicit user approval
- No claim of account access, verification, or live edit rights without proof

## Practical boundaries

- If the API lacks a field, say so instead of inventing it.
- If the public page conflicts with API data, surface the conflict and mark uncertainty.
- If the task requires an account-only action, stop at a draft or checklist unless the user explicitly wants assisted execution.

## Output policy

- Always disclose whether evidence came from API, public page, or both.
- Mark stale or weak evidence clearly.
- Keep recommendations tied to visible proof, not assumptions.
