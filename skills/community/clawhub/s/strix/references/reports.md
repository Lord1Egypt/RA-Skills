# Reading a Strix run

Artifacts are written under `<checkout>/strix_runs/<run-name>/` while the scan is still `running`. The directory name is `<target-slug>_<4 hex chars>` from `generate_run_name`. The newest `run.json` by mtime is the latest run (`latest_run_dir` in `strix/core/paths.py`).

The short read (executive report first, then finding files) and the headless exit codes are in **penetration-testing-with-strix**. Use the order below when that summary is not enough:

1. `run.json` — did the scan finish, what was in scope, what did it cost.
2. `coverage.json` — what was checked, and which of those claims are the agent's own.
3. `vulnerabilities.csv` — the index. Then each `vulnerabilities/<id>.md`.
4. `penetration_test_report.md` — the root agent's narrative. It does not replace the finding files.
5. `findings.sarif` — only when a code-scanning or ASPM tool will ingest the run.

`strix.log` is the host process log. `.state/` is runtime state used to resume. Neither is a finding.

A person can open the same directory with `uv run --env-file .env strix view <run-name>`. The viewer binds to `127.0.0.1` and prints a tokened URL. Agents read the files.

## Exit code and `status` are different facts

Headless exit codes (`0`, `1`, `2`) are in **penetration-testing-with-strix**. Rules that summary leaves out: severity `none` is below `info` and counts toward exit `2` only when `--fail-on` is omitted; an unrecognized severity always counts. Interactive runs do not use exit `2`. A bare `--resume` picker that cannot run also exits `2`; that is a usage failure, not a finding.

`run.json` `status` is independent of the exit code:

| `status` | How it gets there |
| --- | --- |
| `running` | Run started. A directory you are still polling. |
| `completed` | The root agent called `finish_scan` (`update_scan_final_fields` with `mark_complete=True`). Later cleanup does not downgrade this. |
| `stopped` | Headless process left the loop without `completed`. Budget exhaustion and a persistent rate limit take this path. Resume with `-r <run-name>` after a rate limit. |
| `failed` | Unhandled exception (`exit_reason` `error`). |
| `interrupted` | Keyboard interrupt. |

Exit 0 plus `status: stopped`, or exit 0 plus an empty `vulnerabilities/` directory, is not a clean bill of health. Compare `llm_usage.cost` with the `--max-budget` you set. A wrap-up warning can still end in `completed` if the root calls `finish_scan` before the hard stop, so cost near the cap belongs in the summary either way.

`scan_ended_exit_reason` on the in-memory state (copied into `coverage.json` `completeness.exit_reason`) is `finished_by_tool` when the root finished, `budget_exceeded` on the hard cap, `rate_limited` when the provider kept failing, `interrupted` or `error` otherwise. The final headless beacon may try `agent_stopped` only when no earlier reason was recorded.

## `run.json`

Written by `ReportState`. Fields set for a real scan:

| Field | Read it as |
| --- | --- |
| `run_id`, `run_name` | Identity. `run_name` is the directory name. |
| `start_time`, `end_time` | ISO timestamps. `end_time` is null while `running`. |
| `status` | Table above. |
| `auth_mode` | `subscription` records tokens with `cost` held at 0. |
| `targets_info` | Each entry has `type`, `details`, and `original`. `type` is `local_code`, `repository`, `web_application` (URL or domain), `ip_address`, or `api_spec`. |
| `instruction` | The `--instruction` text, including credentials if the user put them there. Treat the file as sensitive. |
| `scan_mode` | `quick`, `standard`, or `deep`. |
| `scope_mode`, `diff_base`, `diff_scope` | Whether white-box work was limited to a diff. `diff_scope.active` true means changed files, not the whole tree. |
| `non_interactive` | Headless when true. |
| `local_sources` | Host paths mounted into the sandbox. |
| `llm_usage` | `cost` is the number to compare with `--max-budget`. `agents[]` has `agent_id`, `agent_name`, `model`, `cost`, and token counts. `providers` splits usage by upstream name when the gateway reports one. |
| `scan_results` | Present after `finish_scan`: `executive_summary`, `methodology`, `technical_analysis`, `recommendations`, `success`. This object is what `penetration_test_report.md` is rendered from. |
| `mcp_connections`, `mcp_connection_status` | MCP servers the run attached. Status entries are `name`, `provider`, `tool_count`, `dead` — no tokens. |
| `deleted_vulnerability_reports` | Findings removed during the run. Their ids are not reused. |

`STRIX_RUN_RECORD_TIMINGS=true` adds `llm_requests` and `tool_calls`. Leave it off unless you are debugging latency.

## `coverage.json`

Schema version is `schema_version` (currently 1). It answers "what was checked," which a finding list cannot.

Two sources stay separate on purpose:

- `entries[]` with `source: agent_reported` — the coverage ledger the agents wrote. Rich, and self-reported.
- `machine_observed` with `source: runtime` — agents that existed, their statuses, the skills they carried, and how many findings were filed. The runtime recorded this whether or not an agent claimed it.

`entries[]` outcome values:

| `outcome` | `outcome_label` | Meaning |
| --- | --- | --- |
| `reported` | Finding reported | A finding was filed for this surface. |
| `no_issue_found` | No issue identified | The agent says it looked and found nothing. |
| `ruled_out` | Ruled out | A candidate was tested and rejected. |
| `not_applicable` | Not applicable | The class does not apply to this surface. |
| `needs_follow_up` | Requires further review | Left open. Also copied into `gaps`. |

`completeness.complete` is true only when every caveat is absent. Caveats are added when:

- `status` is `failed`, `interrupted`, `stopped`, or `running`
- any agent status is `crashed`, `stopped`, `running`, or `waiting`
- `exit_reason` is set and is not `finished_by_tool` or `completed`

`gaps[]` kinds:

| `kind` | Meaning |
| --- | --- |
| `needs_follow_up` | An agent left this surface open. |
| `unrecorded_risk_class` | An agent carried a vulnerability skill and no ledger row mentions that class. Unexamined, not clean. |
| `agent_recorded_no_coverage` | An agent finished with no ledger rows. The root is exempt when it had children, because its job is delegation. |

`summary.findings_filed` counts reports. It is not a severity breakdown.

A green exit with `completeness.complete: false`, a non-empty `gaps` array, or `diff_scope.active: true` supports only a narrow claim: no validated finding in the work that actually finished.

## Vulnerability files

`vulnerabilities.csv` is an index: `id`, `title`, `severity` (upper case), `timestamp`, `file`. A cell that would look like a spreadsheet formula (`=`, `+`, `-`, `@`, tab, CR) is stored with a leading apostrophe so the spreadsheet treats it as text. Sort order is severity (`critical`, `high`, `medium`, `low`, `info`) then timestamp.

`vulnerabilities.json` is the list of report objects. `vulnerabilities/<id>.md` is the same object rendered for a person. Ids look like `vuln-0001` and are not recycled after a delete.

### Classes

`finding_class`:

- `dynamic` — `create_vulnerability_report`. The PoC is the evidence. Required text: description, impact, target, technical analysis, PoC description, PoC script, remediation, evidence, assumptions. Also required at filing time: counterevidence, confidence, what would change the severity, fix effort, and a CVSS breakdown.
- `dependency_cve` — `create_dependency_report`. A pinned version matched a published advisory. The record keeps package metadata and a contextual CVSS. This is not a live exploit of the application. Say so when you summarize it.

### Severity and CVSS

`severity` is the CVSS v3.1 base severity from `cvss_breakdown`, lowercased, except CVSS `none` is stored as `info`. The score is `cvss`. The breakdown letters:

| Key | Letters |
| --- | --- |
| `attack_vector` | `N` network, `A` adjacent, `L` local, `P` physical |
| `attack_complexity` | `L`, `H` |
| `privileges_required` | `N`, `L`, `H` |
| `user_interaction` | `N`, `R` |
| `scope` | `U` unchanged, `C` changed |
| `confidentiality`, `integrity`, `availability` | `N`, `L`, `H` |

The vector is `CVSS:3.1/AV:…/AC:…/PR:…/UI:…/S:…/C:…/I:…/A:…`. Judge the score against the PoC in the same file. The filing rules tell the agent to score the consequence the PoC demonstrated: `C:H` / `I:H` / `A:H` for broad or directly serious impact, `S:C` only when exploitation crosses a security authority, and `privileges_required` / `attack_complexity` honest about secrets the attacker does not already hold. A finding whose prose claims more than the PoC shows is over-rated; quote the PoC, not the adjective in the title.

`confidence` is `high`, `medium`, or `low`. A proof the agent could not execute is supposed to be at most `medium`, with the gap in `confidence_rationale`. `counterevidence` is the case that the issue is weaker or not exploitable. `severity_change_conditions` is the one piece of evidence that would move the rating. `fix_effort` is `trivial`, `low`, `medium`, or `high`.

`cve` matches `CVE-YYYY-NNNN…`. `cwe` matches `CWE-NNN`.

### Markdown sections

Rendered by `render_vulnerability_md`:

| Section | Use it for |
| --- | --- |
| Header metadata | Id, severity, time, target, endpoint, method, CVE, CWE, CVSS, confidence, fix effort. Dependency reports add package, ecosystem, installed and fixed versions, who introduced it, the dependency chain, advisory CVSS, and the contextual vector. |
| Description | What is wrong. |
| Evidence | Concrete proof. |
| Impact | The security consequence. |
| Counterevidence | Why it might be weaker. |
| Confidence Rationale | Why that confidence. |
| What Would Change This Severity | The missing fact. |
| Technical Analysis | Mechanism. |
| Contextual CVSS | Dependency reports only: why the advisory score was adjusted. |
| Proof of Concept | `poc_description` plus `poc_script_code`. The script is the thing to re-check. |
| Code Analysis | `code_locations[]`: relative `file`, `start_line`, `end_line`, `label`, `snippet`, and a diff from `fix_before` / `fix_after`. Paths are relative and cannot contain `..`. |
| Remediation | `remediation_steps`. |
| Fix Verification | How to show the fix worked. |
| Assumptions | Preconditions for the exploit. |
| Update History | Later edits: who changed which fields. |

`http_exchange_ids` may appear in the JSON. They are proxy capture ids. Finding prose is written to omit them; keep them out of a summary you show the user.

`fix_pr_body` and `agent_name` are JSON fields for follow-up work. The markdown is the deliverable.

## Executive report

`penetration_test_report.md` is a header plus the four blocks from `finish_scan`: Executive Summary, Methodology, Technical Analysis, Recommendations. It is the root agent's close-out. It can be absent when the run stopped before `finish_scan` even though `vulnerabilities/` already has files. Prefer the per-finding PoC over a sentence in the executive summary when they disagree.

## SARIF

`findings.sarif` is SARIF 2.1.0 (`https://json.schemastore.org/sarif-2.1.0.json`).

Strix severities collapse to three SARIF levels. The original label stays in `result.properties.strix.severity`.

| Strix severity | SARIF `level` | `security-severity` when the finding has no CVSS |
| --- | --- | --- |
| `critical` | `error` | `9.5` |
| `high` | `error` | `8.0` |
| `medium` | `warning` | `5.5` |
| `low` | `note` | `3.0` |
| `info` / `informational` | `note` | `1.0` |

When the finding has a CVSS score, GitHub's `rule.properties['security-severity']` uses that score instead of the fallback.

A finding with no safe source location is anchored at `SECURITY.md` and marked `properties.synthetic_location: true`. That anchor is not a real file in the target. Rule tags include a STRIDE leg derived from the CWE (`S`, `T`, `R`, `I`, `D`, `E`); an unmapped CWE gets `T` and `I`.

Coverage rows are appended as non-failing results under rule ids `strix-coverage/<risk-area>`: `no_issue_found` and `ruled_out` as pass, `not_applicable` as not applicable, `needs_follow_up` as open. Reported surfaces are the failing results, not a second coverage row. `run.invocations` carries the completeness caveats when coverage was included.

Repository scans add `versionControlProvenance` when the run recorded a repo URL, commit, and ref. URL and IP scans omit it.

## What to tell the user

Lead with status, cost against budget, and whether coverage is complete. Then counts by severity. Then each `critical` and `high` finding by id, title, affected target, and where the PoC lives (`vulnerabilities/<id>.md`). Quote the assumption and the counterevidence when confidence is not `high`. Call a `dependency_cve` an advisory match. Name every `gaps` kind that is non-empty, and say the diff scope when `diff_scope.active` is true.

A partial scan gets a partial conclusion. Offer `-r <run-name>` when status is `stopped` or `interrupted` and the user wants the same scope continued.
