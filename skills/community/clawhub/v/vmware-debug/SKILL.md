---
name: vmware-debug
description: >
  Use to diagnose VMware/vSphere/ESXi/NSX incidents: errors, log dumps, slow VMs, disconnected hosts,
  or an unexplained failure. Correlates companion-skill evidence into a timeline, ranks root-cause
  hypotheses, and recommends the next check. Trigger on "diagnose this VMware issue", "why is my VM
  slow", "troubleshoot this vSphere error" or "what does this log mean". Makes no VMware API calls or
  repairs; writes local case records and a separate audit trail. Default stdio is local; optional
  authenticated HTTPS uses caller tokens and TLS files. Route fixes to vmware-aiops (single action) or
  vmware-pilot (gated workflow), and routine inventory/health without an incident to vmware-monitor.
installer:
  kind: uv
  package: vmware-debug
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["vmware-debug","uvx"]},"optional":{"env":["VMWARE_AUDIT_APPROVED_BY","VMWARE_AUDIT_RATIONALE"],"bins":["vmware-policy"]},"homepage":"https://github.com/vmware-skills/VMware-Debug","os":["macos","linux"]}}
---

# VMware Debug

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere"
> are trademarks of Broadcom. Source is publicly auditable under the MIT license.

The diagnostic brain of the VMware skill family. You bring the symptom; this skill
runs the investigation and points at the root cause. It **reads and reasons** — it
never writes to vSphere; it writes local case records and a separate audit trail.
Companion skills do the data collection and the fixing.

## What This Skill Does

| Category | What | Read or Write |
|---|---|---|
| Incident correlation | Merge events from many sources into one timeline, detect spikes | Read |
| Root-cause ranking | Score symptom clusters, surface the most likely cause first | Read |
| Next-check ideas | Suggest exactly what to look at next (which skill/tool) when you're stuck | Read |
| Remediation routing | Hand the fix to vmware-aiops (single) or vmware-pilot (gated, multi-step) | Read (routes only) |
| Investigation ledger | Open a case; record evidence, gaps and hypotheses; grade and close it | Write (local ledger only) |

**No VMware API client and no write to any VMware system.** It correlates data
the agent gathered with companion read tools. Case tools write a local ledger;
every tool is also audited in `~/.vmware/audit.db`. Default stdio has no listener;
optional HTTPS requires caller tokens and TLS files (see `references/setup-guide.md`).

## Quick Install

```bash
uv tool install vmware-debug==2.3.3
vmware-debug categories          # see what it can diagnose
```

## When to Use This Skill

Use it when there is a **problem to solve**: an error message, a stack of logs, an
alarm storm, "my VM won't power on", "storage feels slow", "the host disconnected".

- Need raw inventory/health with no incident? → **vmware-monitor**
- Need to actually run a fix? → **vmware-aiops** (single op) or **vmware-pilot** (gated workflow)
- Need metrics/anomalies? → **vmware-aria**; centralized logs? → **vmware-log-insight**

**Do NOT use when** there is nothing wrong (routine listing → monitor), or when the
user wants the fix executed (→ aiops/pilot). This skill stops at the diagnosis and
a recommended plan.

## Related Skills — Skill Routing

| Symptom touches | Pull signals from | Then |
|---|---|---|
| Storage / datastore / vSAN | vmware-storage, vmware-log-insight | rank → route fix to aiops/pilot |
| Network / firewall / vMotion | vmware-nsx, vmware-nsx-security | run traceflow, check DFW |
| CPU / memory contention | vmware-aria (metrics/anomalies) | rightsizing via pilot |
| HA / DRS / cluster | vmware-monitor, vmware-aiops | cluster remediation via pilot |
| Power / clone / snapshot | vmware-aiops, vmware-monitor | task status, then fix via aiops |
| Auth / cert / login | owning skill's `doctor`, cert, time sync | user fixes config |

## Common Workflows

### 1. "Here's a pile of logs / alarms — what broke?"
1. Collect events with the data-source skills (e.g. MCP tools vmware-monitor `get_events`, vmware-log-insight `search_logs`, vmware-aria `list_alerts`).
2. Pass them all to **`build_incident_timeline`** (envelope below). Read the top hypothesis + `next_checks`.
3. Follow `next_checks` to pull more targeted data; re-run `build_incident_timeline` to confirm.
4. **Failure branch — no events come back:** the affected target may be unreachable. Run the source skill's `doctor`/health first; a 503/timeout is a *signal* (platform not ready), not a dead end.
5. Produce a diagnosis + recommended fix. Route execution to aiops/pilot. **Do not fix here.**

### 2. "I don't even know what to check"
1. Run **`list_symptom_categories`** (or `vmware-debug categories`) to see the catalogue.
2. Describe the symptom; map it to a category; the `suggested_check` tells you which skill/tool to run first.
3. Collect → `build_incident_timeline` → narrow. Loop until one hypothesis dominates.

### 3. Hand off the fix (advisor → executor, like vmware-harden)
1. Debug emits a structured diagnosis + a proposed remediation (steps).
2. **Single, low-risk fix** → call the matching **vmware-aiops** tool (it has its own double-confirm).
3. **Multi-step / needs approval / cross-skill** → submit the plan to **vmware-pilot**, which owns the state machine, approval gate, rollback, and audit.
4. **Failure branch — fix is ambiguous or risky:** stop and present the hypotheses to the user; never guess-execute.

## Usage Mode

- **MCP** (in an agent): the agent calls the other skills' read tools, then `build_incident_timeline` to correlate. This is the primary mode — that's where the cross-skill "联动" happens.
- **CLI** (humans): `vmware-debug triage --events events.json` correlates a JSON array you collected yourself.

## MCP Tools (14 — 7 read, 7 write)

**Correlation** — stateless, for a single look:

| Tool | What |
|---|---|
| `build_incident_timeline` | [READ] Correlate pre-fetched events → timeline + spikes + ranked hypotheses + next-check ideas |
| `list_symptom_categories` | [READ] List recognised symptom categories + what to check for each |

**Investigation ledger** — for an incident you will reason about over time:

| Tool | What |
|---|---|
| `open_case` | [WRITE] Define the event; returns a case id and the grade this environment can reach |
| `get_case_readiness` | [READ] What grade this environment can reach, per symptom category, **before** you start |
| `get_case_knowledge` | [READ] Which knowledge formats are accepted, what is mounted, and which entries apply to a case |
| `plan_case` | [READ] What to fetch next — skill, tool and purpose per step; recomputed from the case's current state |
| `list_cases` | [READ] Cases, newest first |
| `get_case` | [READ] One case: scope, ledger sizes, grade history |
| `record_case_hypothesis` | [WRITE] Register a candidate explanation, or read the ledger of what supports and refutes each |
| `submit_case_evidence` | [WRITE] Record one retrieved fact, with its source, query and time basis |
| `record_case_gap` | [WRITE] Record what could **not** be retrieved, and how to close it |
| `record_case_timeline` | [WRITE] Correlate everything the case has collected into one timeline |
| `grade_case` | [WRITE] Recompute the conclusion grade from the ledger and record it |
| `close_case` | [WRITE] Record the final grade, archive, and name what was left open |

The seven writes go to `$OPS_HOME` (default `~/.vmware/cases/`) and nowhere else.

**List envelope** (output of `list_symptom_categories`): `{items, returned, limit, total, truncated, hint}` — read the rows from `items`. `truncated` is always `false` here, which is the point: it states that the catalogue is complete instead of leaving you to infer it.

**Event envelope** (input to `build_incident_timeline`): `{ts, source, severity, entity, text, fields}`.
See `references/event-envelope.md`. The agent normalises each source's events into this
shape; debug stays source-agnostic and has no dependency on the other packages.
Keep each event's `event_type` in `fields` — the classifier matches it as well as
the message, and on a modern `EventEx` it is the only thing that says what the
event was.

## The Investigation Ledger

Correlating events answers "what happened together". A case answers "what do we
believe, on what evidence, and what is still missing" — and keeps answering it
across sessions and across people.

The case folder is the deliverable, not an implementation detail. Everything in
it but the index is plain text, so a customer can take the folder away and audit
how a conclusion was reached with none of this installed:

```
~/.vmware/cases/<case-id>/
├── scope.json    what is being investigated, and how that was decided
├── evidence/     one file per fact: source skill, exact query, time basis
├── gaps.json     what could NOT be obtained, what it blocks, how to close it
├── conclusion.md the grade, appended — including every time it went down
└── timeline.md · hypotheses.md · plan.jsonl · case.json
```

Hypotheses get ids (H1, H2, …), and those ids are what `record_case_gap(blocks=…)`
and `submit_case_evidence(falsifies=…)` refer to. **An id that was never
registered is refused, not ignored** — a dangling reference blocks nothing and
falsifies nothing, which quietly reports a stronger case than you have.

**You cannot state a conclusion level.** `grade_case` has no parameter for one;
the grade is recomputed from the ledger on every call. To change it, change the
ledger — submit the missing evidence, or record the gap that is blocking it.

- **Candidate** — a hypothesis exists
- **Probable** — ≥2 *independent* sources agree (two calls to one skill are one
  source) and nothing outstanding could overturn it
- **Confirmed** — that, plus a decisive item: a direct hardware diagnostic, a
  version-checked knowledge-base entry, or a vendor SR; and no gap left open
- **Excluded** — an observation that actually rules it out. "We looked and found
  nothing" is a gap, not an exclusion. Exclusion is per hypothesis: two
  independent sources must falsify *that* hypothesis, and the case is Excluded
  only when every registered hypothesis is ruled out. A hypothesis contradicted
  by too few sources holds the case at Candidate. Otherwise `grade_case`
  grades what remains, counting only evidence that falsifies nothing, and lists
  each hypothesis as `open` or `excluded` in `hypotheses`

`plan_case` is not a checklist: submit evidence and the next plan is shorter,
lose a source and it routes around it. Its `unavailable` half is the important
one — a source this install cannot reach is listed there with how to supply it,
so the gap is visible now rather than when the conclusion refuses to firm up.

`get_case_readiness` answers this per symptom category rather than as one number —
"storage reaches Probable, hardware reaches Candidate" can be acted on;
"readiness 78%" cannot. Two classes served by the *same* skill count as one
source, so it agrees with what `grade_case` will actually award.

### Mounting a knowledge library

`get_case_knowledge` answers "what can I add" without anyone reading this file.
Entries go under `$OPS_HOME/knowledge/{kb,runbook,sr,cases}/`:

| Format | How metadata travels |
|---|---|
| `.md` `.markdown` | YAML front-matter between `---` fences, body below — **preferred** |
| `.yaml` `.yml` | the whole file is one entry |
| `.json` | one entry per file |
| `.jsonl` | one JSON object per line — what ticketing systems export |
| `.csv` `.tsv` | one entry per row; use dotted columns (`driver.version`) for nested constraints |
| `.txt` `.log` | a sibling `<name>.yaml` carries the metadata |

PDF, DOCX, PPTX and HTML must be converted to Markdown first — `get_case_knowledge`
names them rather than ignoring them.

**Every entry needs an `applies_to` block to be decisive:**

```yaml
---
id: KB-2026-0417
applies_to:
  product: vsphere
  build: ">=8.0.3, <9.0"
  driver: {name: nvme_pcie, version: ">=1.2.4"}
  firmware: {vendor: dell, version: ">=52.26"}
---
```

`product`, `build`, `driver` and `firmware` are the constraints the checker
evaluates. **Any other key leaves the entry non-decisive** — including a typo —
because an unverified constraint is not a satisfied one, and `get_case_knowledge`
names the key it could not check.

Knowledge evidence must say **which** entry it is
(`submit_case_evidence(source_skill="knowledge-kb", knowledge_entry_id="KB-…")`)
— "some applicable entry is mounted somewhere" is a different claim from "this
one applies", and only the second can carry a conclusion.

Matching is **by version applicability, never by similarity** — an entry written
for the wrong build reads exactly like the right one, and similarity is the only
thing that would let it through. An entry with no `applies_to` can support a
hypothesis but can never make a case Confirmed. A constraint the case scope
cannot answer is not a match either: silence is not a pass.

> **On a stock install the ceiling is Probable.** Confirmed needs a decisive
> source, and there is neither a hardware-diagnostic channel (no Redfish/BMC, no
> SMART/NVMe) nor a knowledge library mounted — `~/.vmware/knowledge/` ships
> empty. Every tool that can reach the ceiling says so in its output rather than
> letting you wonder why a well-supported case never goes higher. Mount a
> knowledge library and the ceiling rises on its own.

Recording a gap is meant to be free: a missing confirmation caps the grade, it
does not demote it. Only a gap that could *overturn* the hypothesis holds a case
at Candidate.

## VMware access and local side effects

vmware-debug does not connect to VMware APIs or require VMware account credentials.
The calling agent fetches with companion read tools and submits results here.
Case tools write the local ledger, and every call writes a separate local audit row.
Default stdio has no listener; opt-in HTTPS opens the configured listener using
caller tokens and TLS certificate/key files. Treat those files as secrets. Running with local or small models? See
[`references/agent-guardrails.md`](references/agent-guardrails.md).

**Never put a secret into a case.** For an auth symptom, record *that* a credential is
missing, expired or rejected (the owning skill's `doctor` says which) — never a password,
token, or the contents of a `.env` file, in any evidence `summary`, `query` or `payload`.
Do not open `.env` files to diagnose; case folders are kept until you delete them.

## CLI Quick Reference

```bash
vmware-debug categories                        # what can it diagnose
vmware-debug triage --events events.json       # correlate a collected event set
cat events.json | vmware-debug triage          # or via stdin
vmware-debug mcp                                # start stdio MCP server (proxy-safe)
```

## Troubleshooting

- **`build_incident_timeline` raises "event[N] could not be normalised"** — event N is missing a timestamp or has an unparseable one. Every event needs `ts` (ISO-8601, epoch seconds, or millis).
- **Most events come back "uncategorized"** — read `classification` in the result: it says how many, what share, and quotes the texts that matched nothing. Do **not** widen the window; a wider window adds baseline, not signal. The spikes still tell you *when*, which is answerable without a category. If the samples name a subsystem the taxonomy does not know, add a signature (see `references/routing.md`).
- **No spikes detected on an obvious burst** — check `binning` for the resolution you were given. The width is chosen from event density so that bins average ≥4 events; a burst shorter than one bin can still be flattened by it. Pass `bin_seconds` to narrow. Below three bins there is no baseline at all and nothing is reported.
- **`record_case_timeline` says zero events after you submitted results** — check `payload_events` in each `submit_case_evidence` reply. Events are read from a bare list, or from `items`/`events`/`rows`; a *summary* of a tool's result carries none. `note` names which items carried nothing and what keys they held instead.
- **`get_case_readiness` says a skill you have is not installed** — both spellings are accepted (`monitor` and `vmware-monitor`). A name it did not recognise comes back in `unrecognised_skills` rather than being read as missing.
- **It won't execute the fix** — by design. Route to vmware-aiops or vmware-pilot.

## Audit & Safety

No VMware API call or remediation is executed. Every tool is audited locally. The seven [WRITE] tools update the local case
ledger under `$OPS_HOME`; nothing here touches a remote VMware estate. Evidence, gaps,
hypotheses and grade history are only ever added to — `timeline.md` is regenerated from
the evidence and `case.json` holds the current grade and state. Remediation is always routed to
aiops/pilot, where the double-confirm / approval gates live.

**What the audit row holds.** Every debug tool call — a failed one included — writes one
row to `~/.vmware/audit.db` through `@vmware_tool`, as do the `categories` and `triage`
CLI commands under their MCP tools' names. The row records the tool, time, OS user,
detected agent, arguments, status (`ok`, `error`, `denied`, `budget_exceeded`,
`interrupted`) and a result. Two arguments are stored as `***`: evidence `payload` and
`build_incident_timeline` `events`. Two results are not stored at all — `build_incident_timeline` and
`record_case_timeline` quote event text (`sample_text`, `unmatched_samples`, `rejected`), which
can carry anything the source logged, so their row says
`[redacted: return value declared sensitive]`. Every other result (ids, counts, grades,
your own summaries and statements) is stored after credential scrubbing. The data itself
is in the case folder, or with you.

**What debug inherits from vmware-policy**, since its tools pass through `guard()`:
- **Runaway guard** — the 26th call to one tool with identical arguments within 120 s is
  refused (`budget_exceeded`; `VMWARE_RUNAWAY_MAX`, `VMWARE_RUNAWAY_WINDOW_SEC`). It
  compares a digest of the arguments the tool received (vmware-policy ≥1.16.0), so
  calls with different `events` are not identical.
- **A malformed `~/.vmware/rules.yaml` fails closed** — every tool is refused with a reason
  naming the file; `categories`/`triage` exit 1 with a traceback ending in that message.
- **A `deny` rule without `operations`** matches every tool, debug's included.
- **Environment-scoped rules never match** — debug registers no resolver (no targets).
- **Maintenance windows** gate only `high`/`critical` risk; every debug tool is `low`.

See `references/setup-guide.md`.

**Case data is sensitive and is kept until you delete it.** Each case lives in
`$OPS_HOME/cases/<case-id>/` (default `~/.vmware/cases/`), created owner-only (`0700`).
It holds whatever evidence was submitted — host names, addresses, log and event text.
Nothing is deleted automatically: `close_case` records the grade and marks the case
closed but keeps its files. Remove a case by deleting its folder.

## License

MIT.
