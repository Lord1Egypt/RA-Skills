# Testing Strategy

## Layers

### Unit tests
- database schema/bootstrap
- path/layout resolution
- skill-local config loading/writing
- sync state helpers
- data transformation helpers
- query/report helpers
- public artifact generation

### Integration-style tests
- mocked API client behavior
- paging behavior
- retry/backoff logic
- seed and delta sync orchestration

### Live verification notes
Because SherpaDesk is awkward and externally controlled, some truths may only be learnable through live probing.
Those findings should be written down in this repository instead of living only in chat memory.

## Public-fixture rule

Tests and fixtures should stay public-safe.

- use synthetic placeholder names and domains
- avoid real customer/account/user/technician identities in test data
- avoid embedding live sensitive payloads when a reduced synthetic fixture proves the behavior just as well
- prefer `example.com`, placeholder ticket subjects, and obviously fake names in fixtures

## Issue reporting from validation

If testing, live verification, or exploratory use finds a real bug, contract mismatch, or missing capability, check:

- <https://github.com/kklouzal/SherpaMind/issues>

Add supporting detail to an existing issue when it matches; otherwise open a new one.
Keep issue content anonymized and public-safe.

## Rule

Do not assume a green local unit test suite means the SherpaDesk API contract is understood correctly.
