# SherpaDesk API Reference Notes

## Canonical external documentation

The authoritative SherpaDesk API documentation currently lives here:

- <https://github.com/sherpadesk/api/wiki>

This URL should be treated as a first-class dependency of this project and kept visible in multiple project surfaces because the API is awkward enough that future work should never rely on hazy memory.

## Working assumptions

SherpaDesk API work should assume:
- inconsistent or under-documented endpoint behavior may exist
- auth/header requirements must be verified empirically
- pagination behavior may vary or be weakly documented
- delta-sync semantics may need endpoint-specific handling
- rate limiting and server-side fragility are real risks

## Current wiki-derived notes

From the public SherpaDesk API wiki, the current documented contract appears to be:
- service endpoint: `https://api.sherpadesk.com/`
- organization discovery: Basic auth with identity `x:{api_token}` against `/organizations/`
- regular API access: Basic auth with identity `{org_key}-{instance_key}:{api_token}`
- many-object endpoints default to 25 records/page
- maximum page size is 250
- page numbering starts at `0`
- stated rate limit: `600 requests/hour`

These notes were initially wiki-derived, but we now have live confirmation that:
- organization discovery works with token-only Basic auth against `/organizations/`
- `GET /tickets?limit=1&page=0` returns a JSON list shape under the org/instance-scoped auth identity
- `status=open` and `status=closed` both work as live filters on `/tickets`
- ticket rows include useful fields for local change detection, including `created_time`, `updated_time`, `closed_time`, `is_new_tech_post`, `is_new_user_post`, and `next_step_date`

We also have negative findings that matter:
- naïve `updated_time=<date>` and `created_time=<date>` query params appear to be ignored by `/tickets`
- the documented `Content-Range` header was not observed in our live ticket-list probes
- page ordering looks recent-ish, but has not yet been proven to be a strict monotonic `updated_time` sort

Account-specific identifiers and secrets should remain local-only and should not be committed to this public repo.
Examples and verification notes in this repository should stay anonymized unless identity is absolutely necessary.

## Project rule

Do not hard-code assumptions about SherpaDesk API behavior without either:
1. a direct citation to the SherpaDesk wiki, or
2. a clearly documented live verification note in this repository.

## Required discipline

Any API integration change should record:
- endpoint used
- auth/header pattern used
- pagination behavior observed
- timestamp / delta fields used
- retry / backoff behavior expected
- any rate-limit or burst-safety assumptions
