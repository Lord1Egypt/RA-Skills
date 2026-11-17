# GTFS Feed Check reference

Load this reference before calling either bundled tool or interpreting its report.

## App identity

- App: GTFS Feed Check
- App id: `gtfs-feed-check`
- App version: `0.2.1`
- MCP server: `powmcp-gtfs-feed-check`
- App page: https://powmcp.com/apps/gtfs-feed-check/

## What the checks measure

Both tools fetch directly hosted public GTFS Schedule ZIP bytes and run the pinned Canonical GTFS Validator 8.0.1 engine in a no-network sandbox.
The measured criterion is conformance with the engine's GTFS specification and Best Practices profile. The evidence is granular to severity, notice code, affected file and field, returned message, and example row or field locations.
A check can also report structural inventory, service-date span, and SHA-256 of the exact downloaded bytes. These fields bind the report to the artifact that was fetched.

## One-feed check

Use `powmcp-gtfs-feed-check:gtfs_feed_check` for one-feed readiness and diagnosis.
The input requiring judgment is `url`. It must be a direct public HTTP(S) URL to a GTFS Schedule ZIP containing `.txt` tables.
Do not supply a ChatGPT file id, local path, GBFS feed, GTFS-Realtime feed, feed-portal page, cloud-drive share, or authenticated URL requiring a login.
`maxNotices` is optional. Its default is 400, its minimum is 1, and its maximum is 1000. It limits distinct notice codes returned, ordered most severe first.
Tell the user before the call that the live download and validation can take up to 90 seconds.

Read these returned fields first:

- `pass`
- engine version and profile date
- most severe notice
- ERROR, WARNING, and INFO counts
- whether the notice list was truncated

Then quote the returned structural evidence:

- present required and optional tables
- agency, route, trip, stop, and shape counts
- `feed_info` presence
- service-date span
- SHA-256 of the exact bytes

For each notice, quote its severity, code, file, field, message, and example location as returned. Codes such as `foreign_key_violation` and `stop_too_far_from_shape` name validator rules; they do not support a broader diagnosis than the returned message.
A pass means the pinned profile produced no ERROR notice. WARNING and INFO notices may remain.

## Feed comparison

Use `powmcp-gtfs-feed-check:gtfs_feed_compare` only for exactly two GTFS Schedule feeds from the same agency.
The input requiring judgment is `urls`. Supply exactly two distinct direct public HTTP(S) GTFS Schedule URLs, baseline first and revised second.
`maxNotices` is optional. Its default is 300, its minimum is 1, and its maximum is 600. It caps notice codes collected per feed for the comparison.
Tell the user before the call that downloading and validating the two feeds can take up to 115 seconds.

Read these returned fields:

- each feed's SHA-256
- each feed's pass verdict
- each feed's ERROR, WARNING, and INFO counts
- each feed's service-date span
- notice codes that appear or worsen in the revised feed
- notice codes removed or reduced in the revised feed
- ranking by pass state and then fewer ERROR notices

The regressions and resolved lists compare automated notice codes. The ranking measures automated conformance only. A pass and ERROR-count tie provides no evidenced winner.

## What a pass does and does not prove

A pass proves only that the fetched bytes had no ERROR notice under the pinned automated specification and Best Practices profile at the time of the run.

It does not establish that:

- the timetable matches real service
- a distributor will accept the feed under additional rules
- GTFS-Realtime is valid
- a feed omitted from a comparison is acceptable
- an unreturned notice is absent when findings were truncated

Human review of the underlying schedule remains necessary.

## Structurally unassessable cases

The tools cannot assess a portal page, local path, authenticated resource, GBFS feed, or GTFS-Realtime feed because the input contract requires directly hosted public GTFS Schedule ZIP bytes.
The tools do not judge whether scheduled service occurs in the real world. That requires human schedule review.
The comparison cannot support a same-agency regression claim when the inputs belong to different agencies or when fewer or more than two URLs are supplied.
Distributor-specific acceptance remains outside the measured profile and must be reviewed against the applicable distributor's rules.

## Failure handling and user lines

If an invalid-arguments response names a field, correct that field and call again. Say:
> The check rejected the named field argument. I will correct that field and rerun the same check.

This response is not evidence that the tool is missing.
The comparison contract supplies this strict failure message:
> Feed compare failed: the two URLs must be distinct feeds

Resolve it by supplying separate baseline and revised URLs for the same agency.
If the tool is absent, say:
> The exact feed could not be checked, so notice-level evidence is unavailable.

Then offer connection and rerun, or use the non-PowMCP path below. Do not invent a transport or validator failure code that the call did not return.

## Non-PowMCP path

Download the exact public GTFS Schedule ZIP and run the Canonical GTFS Schedule Validator through its web interface, desktop application, CLI, or GitHub Action.
Preserve the validator version and report. Triage ERROR before WARNING and INFO notices, correct the upstream scheduling data, rerun, publish at a stable URL, refresh applicable registrations, and conduct separate human schedule review.
This path does not provide the PowMCP return contract. Record the version, artifact identity, findings, and truncation behavior that the chosen interface actually reports rather than assuming fields are equivalent.

## Source of truth

- GTFS validation guidance: https://gtfs.org/getting-started/validate/
- Canonical validator rules: https://gtfs-validator.mobilitydata.org/rules.html
- Canonical validator releases: https://github.com/MobilityData/gtfs-validator/releases
- GTFS Feed Check app: https://powmcp.com/apps/gtfs-feed-check/
