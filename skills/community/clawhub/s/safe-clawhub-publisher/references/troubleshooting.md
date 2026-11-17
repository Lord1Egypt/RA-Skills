# Troubleshooting

## Network unavailable before publication

Apply this section only when DNS resolution, TLS connection setup, or another network operation fails before any publish command has been attempted.

1. Treat restricted sandbox networking or a missing network permission as the first hypothesis. Do not describe a single sandboxed DNS failure as a confirmed ClawHub outage.
2. When the execution environment supports approval or escalation, request it and retry the same failed read-only ClawHub command once with network access. If the CLI error is not diagnostic enough, use one narrowly scoped DNS or HTTPS check instead. This approval covers only the displayed read-only check; it does not authorize login, publication, broader network access, or persistent configuration changes.
3. If the retry succeeds, continue with account and remote inspection. If escalation is unavailable, denied, or the approved retry still fails, complete all package inspection and local validation that do not require the network, then report which remote evidence remains unavailable.
4. Distinguish the outcome precisely: `network permission unavailable`, `DNS failed even with approved network access`, or `ClawHub returned an HTTP/CLI error`. Do not collapse these into a generic DNS or service outage.

Never repeat the network retry automatically. If a publish command may already have reached ClawHub, skip this section and use **Publish response is unclear** below; another publish command is not a connectivity test.

## Authentication or ownership failure

Stop and report the account/owner evidence available without exposing credentials. Do not switch accounts, create a namespace, or republish under a different owner unless the user authorizes that target.

For missing authentication, prefer the installed CLI's device flow with browser opening disabled so the verification URL and one-time code can be relayed safely. Keep the interactive process alive while polling in bounded intervals. If persistent sessions are unavailable, ask the user to complete the same command in their terminal. Never ask them to paste an API token into chat. After success, run `clawhub whoami`, then repeat remote inspection and dry-run.

## Command error reporting

Every release-critical command must preserve and report its result, with special priority for the final publish command. When the publish command, dry-run, account check, or remote verification exits non-zero, writes an error to stderr, returns empty output, or emits a rate-limit/reset message, show the sanitized message, phase, exit status, and next safe action to the user. Do not replace an actionable server error with `publish failed`, and do not suppress a release-critical error with `|| true` except for an explicitly expected absence check whose exit status and interpretation are reported separately. Failures from ordinary local helper commands only need escalation when they affect the release decision.

Classify the outcome before deciding what happens next:

- **Rejected:** ClawHub returned a definitive validation or authorization error, such as a reserved topic or too many topics. Do not retry the same command. Explain the exact correction, rerun local preflight and dry-run, and obtain fresh confirmation for the corrected command.
- **Unavailable:** The command could not reach ClawHub or the server returned a temporary limit. Report the retry delay or network condition and perform only the bounded read-only check allowed by this workflow.
- **Unknown:** Publication may have reached the server but the response is incomplete, empty, or timed out. Do not publish again until bounded remote verification establishes failure.

Never expose tokens, cookies, device secrets, or other credentials while relaying command errors.

## Duplicate or rejected version

Inspect the remote package first. Never overwrite or reuse an immutable version. Re-evaluate the diff and propose the next appropriate version; do not mechanically increment until the server accepts it.

## Ambiguous package type

Show the detected markers and conflicting files. Ask the user to identify the intended artifact or fix the manifests. Do not try both publish commands.

## Manifest rejected

Use the installed CLI's error and `--help`, then consult current official schema documentation. Patch only the fields implicated by evidence, rerun local validation, and repeat the dry-run. A manifest edit invalidates any earlier publish confirmation.

## Publish response is unclear

Treat timeouts, dropped connections, empty output, and interrupted output as unknown state. A missing version in CLI/API output can reflect indexing delay, stale cache, publication processing, or rate limiting; absence alone is not proof that publication failed.

Apply this fixed budget so the workflow cannot loop:

1. Make one immediate non-mutating inspection of the exact version, artifact, and tags.
2. If the result is absent, stale, rate-limited, or pending, wait only for the server's `Retry-After` value and inspect once more. Cap this wait at two minutes.
3. After the second inspection, stop automated polling and show the canonical package page. Do not schedule another check or issue another publish command.

Construct and show the canonical package page from the already-confirmed target:

```text
https://clawhub.ai/<owner>/skills/<slug>
```

Ask the user to open it and verify the intended immutable version, current/latest tag, changelog, and file list. Do not invent a version-specific URL unless the installed CLI or canonical page exposes one.

- If the user confirms the intended version is visible, record `user-confirmed in ClawHub UI`; the release is terminal for retry decisions. Do not publish again. Optional later verification must be a new user request, not continued polling from this run.
- If the page is also unavailable or inconclusive, report the state as unknown and stop rather than risk a duplicate publication.
- A second publication attempt is allowed only when authoritative evidence establishes that the first attempt was rejected or failed, the exact version is not pending or published, and the user gives fresh confirmation for the exact retry command. Any added flag such as `--json` changes the command and requires new confirmation.
- Permit at most one such confirmed retry. If it also fails or returns an ambiguous outcome, stop for manual resolution even when later inspections remain empty.

## Integrity gate mismatch

If the validator and CLI fingerprints differ, or a repeated pre-publication check no longer matches the confirmed plan, stop. Compare the exact included files, ignore rules, generated-card behavior, CLI version, account, and remote baseline. Refresh the plan and obtain a new confirmation; never waive the mismatch because the semantic diff appears small.

## Security scan pending or failed

Report pending as pending. For a failure, capture the finding without reproducing secrets, correct the release source, choose a new version if the original was accepted, and dry-run again. Never weaken ignore rules merely to clear the scan.

## CLI behavior differs from this skill

Record the installed CLI version and relevant `--help`. Prefer that help for syntax, but retain this skill's safety boundaries. If the newer CLI requires a destructive or broader action, stop and ask before proceeding.
