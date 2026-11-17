# Online Codex CLI test — 2026-10-08

Three independent caller projects installed GitHub commit `7c38728`, then ran real online
Codex sessions from Light through Max. This supersedes the acquisition boundary of the
[earlier snapshot-only smoke test](codex-cli-2026-10-08.md), which remains a separate record.

Codex CLI 0.160.1 used the actual configured `gpt-6.1-sol / high`, no model override,
`web_search="live"`, workspace-write with network enabled and approval policy never.
Each session read the skill, researched public sources, measured local bars, built/resumed
all four tiers and validated them. Installed source fingerprints were unchanged.

| Market | Light | Medium | Heavy | Max | Added Beta | Growth | Bar cutoff |
|---|---:|---:|---:|---:|---:|---:|---|
| CN | 104 | 302 | 457 | 595 | 138 | 30.20% | 2026-09-30 |
| US | 100 | 294 | 370 | 481 | 111 | 30.00% | 2026-10-06 |
| Crypto | 14 | 35 | 50 | 65 | 15 | 30.00% | 2026-10-06 |

References were 42/44/0 per tier respectively. Independent inspection verified all 12 bundles,
zero validation errors, tier nesting, complete Heavy facts/seed retention, Beta-only expansion,
proportional Heavy groups, export limits and local CSV hashes for every selected member.
Wall times were 36.9/32.6/32.1 minutes, including acquisition, research and repair; not guarantees.
The original CN/US/Crypto economic plans and necessary duties were preserved.

## Actual recovery and limits

- CN Light initially needed research. Public alternative histories, per-instrument volume-unit
  checks and remeasurement enabled real resume. Content review then corrected optional Beta
  business assignments and deferred 14 inadequately supported extensions without removing core duties.
- US resolved corporate actions for ET/WBD and repaired a temporary collector's share-class
  filename collisions. Related histories and source identities were reacquired and remeasured.
  WBD's duty was researched through SKYD, not treated as a simple ticker rename. ET has 49 real
  bars and an explicitly disclosed exchange/TradingView namespace discrepancy.
- Crypto kept exact venue/contracts, dated carried evidence, GRAM's short history and STX's
  Monitoring flag. HTTP-200 shells were corrected from "refreshed" to carried/unknown, then all
  tiers were rebuilt. This was not a new complete audit of tokenomics or every protocol fact.
- Default fetch exposed CA failures and large-response truncation. Temporary public acquisition
  helpers completed this test; it did not prove the original adapter recovered without assistance.
- US moved final staging artifacts during delivery. Exact copies restored checkpoint paths.
  Version 0.9.1 now checks saved artifact paths/hashes and documents copy-only delivery.

At this test's completion, worked examples included US's four depths and CN/Crypto/JP/KR Medium.
The current [format-review examples](../../examples/README.md) retain CN Medium and US Light/Medium;
the previous example set is archived locally under `temp/report-format-2026-10-08/previous-examples/`.
Rebuilding examples is offline;
old valid business evidence keeps its original date. Qualification verifies contracts/coverage,
not independent leadership truth, complete regulatory review or investment performance.

## Reproduce and inspect

Use a fresh caller project and an installed reviewed checkout. Start from the dated examples
as candidate benches, refresh listing/market cap and completed bars online, preserve the plan,
measure through the CLI, then build Light → Medium → Heavy → Max with the matching Heavy seed.
A compact CN example needs a newly researched Beta bench for Max.

```bash
codex exec --json --sandbox workspace-write \
  -c 'approval_policy="never"' -c 'web_search="live"' \
  -c 'sandbox_workspace_write.network_access=true' \
  --output-last-message result.md - < request.txt > events.jsonl
```

Retain actual argv/session metadata, raw dated sources, CSVs, failures, materially changed
repair inputs, command receipts and standard bundles. Inspect artifacts/checkpoints separately
from the model's final prose. Full evidence is retained locally under
`temp/codex-online-2026-10-08/`; raw histories and personal session logs are not distributed.
[Sanitized receipts](codex-online-2026-10-08.json) preserve output/CSV hashes and observed checks.
This test exercised actual CLI sessions, not the Codex desktop UI or future-window evaluation.

## 0.9.1 recovery follow-up

Targeted online CLI fetch checks on 2026-10-08 exercised the revised adapter, independently of
the original full sessions above. All three fetched current inventory and usable histories:

| Market | Requested histories | Received | Result |
|---|---:|---:|---|
| CN | 339 | 338 | Partial: SZSE:302132 last quotation 2025-02-14 |
| US | 386 | 385 | Partial: NYSE:VYLR only four effective daily bars |
| Crypto | 3 | 3 | Complete |

Equity `--limit 1` also includes provider-industry representatives and market gauges, so it
requests many more than one history. These are acquisition checks, not new membership decisions.
The missing histories were rejected after checking both Yahoo hosts; no values were fabricated.
CN/US used the same completed-bar cutoffs as above. In this machine's proxy environment, verified
system curl recovered responses that urllib repeatedly truncated, within the same three-attempt
budget. It is optional and is not installed by the skill. Without it, failures remain explicit.
Local manifests, response receipts and logs live under `temp/release-0.9.1/live-fetch/`.

An actual TradingView US Max import and re-export retained all 525 codes (481 entities plus
44 references), identical groups and `AMEX:ET`. CN Max displayed 637 codes after import.
Crypto UI import and further browser checks were waived by the user; no claim is made for them.
Full UI evidence remains local under `temp/release-0.9.1/tradingview/`.
