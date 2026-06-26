# Privacy Model

## Principle
This skill is **local-first**.

The user may use a WeRead cookie locally to export their own reading records, but:
- the cookie must stay on the local machine
- the cookie must not be embedded in skill files
- the cookie must not be written into exported JSON
- the cookie must not be sent to third-party sync services by default

## Allowed local cookie sources
- environment variable
- local cookie file
- direct one-off CLI argument

## Not the default path
- CookieCloud
- remote cookie sync
- shared cloud storage of cookie

## Output hygiene
The exporter should write only reading-record data that is necessary for downstream recommendation work.

## Recommended workflow
1. User sets local cookie
2. Export raw JSON locally
3. Normalize locally
4. Skill reads normalized JSON
5. Recommendation happens from the normalized file, not from a live cookie session unless the user explicitly requests a refresh
