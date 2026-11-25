# ClawHub review — 2026-11-07

URL-only verification could report any HTTP 200 page as publication. It now requires an API-backed published post and matches the canonical URL. Public fetches are restricted to the explicitly configured site origin, refuse redirects, carry no API credentials and have a bounded timeout. API requests also refuse redirects.

Publish now requires `--status publish` or `--status draft`; draft creation is never presented as public publication. Duplicate checks report failure truthfully. Test fixtures mock every network request; no posts, schedules or live site configuration were changed during this review.

The configured API/site is a trusted operator input. Private WordPress sites remain supported. This CLI is not an internet-facing URL proxy or a sandbox against a malicious local operator. Scanner incomplete-inspection notices are not evidence of concealed behaviour.


## Current scan boundary — 2026-11-22

The helper source is shipped in full and covered by mocked network tests. ClawHub may still report partial static inspection for the referenced JavaScript files; that is a scanner coverage limitation, not hidden runtime code. The skill deliberately omits `allowed-tools`: in Agent Skills metadata that field can preapprove tools rather than cap permissions. Network and environment access remain subject to the host runtime policy and the user-authorized publishing task.
