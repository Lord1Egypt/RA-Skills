# skill-deep-audit — Complete Check Rules

## Scan-scope conventions

> **Required reading: each rule's scan target must follow these conventions
> to eliminate inter-auditor judgement drift.**

| Path / file | Scan content | Notes |
|------------|--------------|-------|
| `SKILL.md` | Full-file scan | Trigger phrases, step descriptions, reference paths, guardrail statements, etc. |
| `scripts/*` | **Full-file scan (default)** | Main executable code. All security / code-convention rules scan this scope by default. |
| `references/*.md`, `references/*.json` | **File existence check only (D6-E5 / D6-W3)** | Reference docs are knowledge content. **CLI commands, URLs, and code snippets inside them do NOT trigger convention scans.** Exceptions are spelled out in individual rules. |
| Top-level `.py` / `.sh` etc. scripts | Scan (also see D4-W1 directory convention) | Top-level scripts violate directory convention and are simultaneously included in code-convention scans. |
| `__pycache__/`, `.git/`, `node_modules/` | Only D4-E5 packaging-convention check | No content scan. |

**Key principles**:
- Example code, mapping tables, low-level CLI fallback notes etc. in
  `references/` are **documentation content**. They do not trigger
  code-execution-class rules.
- If the same content appears both in `scripts/` and `references/`, the
  actual call in `scripts/` takes precedence.
- `AUDIT-*.md` files under the audited skill directory are produced by
  skill-deep-audit and are **always excluded** — they do not participate
  in any check dimension.

---

## False-Positive General Rules

> Boundary scenarios not covered explicitly, or where evidence is
> insufficient to conclude, are handled by these general rules — **do not
> hard-judge ERR / WARN**.

1. **Insufficient evidence → no hard judgement**: when a scan hits but you
   cannot confirm it's a real issue (e.g. cannot tell the actual format on
   both ends, cannot tell whether a branch is reachable), mark it as
   "⚠️ manual verification needed" with the reason in the report, and **do
   not deduct points**.
2. **Comments / examples / docs don't count as violations**: suspicious
   patterns that appear only in code comments, string literals,
   `references/` docs, or example code blocks in SKILL.md do not trigger
   code-execution-class rules (unless the rule explicitly says it scans
   SKILL.md / references).
3. **Internal modules of this skill don't count as external dependencies**:
   imports / function calls first go through step ① of the "three-step
   join" algorithm to look up inside the current skill; if found, exclude
   them (see D7-W2).
4. **Standard library and well-known PyPI packages are excluded outright**:
   os/sys/json/re/pathlib/requests/openpyxl/pandas etc. do not enter
   dependency-ownership judgement.
5. **Scope-of-applicability exemption first**: if a rule declares "applies
   only when the skill has write operations" or "pure-doc skills skip this",
   evaluate scope first. If out of scope → ✅ pass directly, do not enter
   the deduction logic.
6. **No double-counting**: when the same line of code is hit by multiple
   rules, count it only once according to each rule's de-dup convention
   (e.g. the D3-E2 token sub-item shares its scan pattern with D5-E1 — count
   only D5-E1).

> Goal: stable, repeatable results across different agents / re-runs, and
> bias toward "don't wrongfully accuse".

---

## Table of contents
- [D1 Process closure & idempotency (13 pts)](#d1-process-closure--idempotency-13-pts)
- [D2 Tool & command conventions (10 pts)](#d2-tool--command-conventions-10-pts)
- [D3 Portability & defense (15 pts)](#d3-portability--defense-15-pts)
- [D4 Skill usability conventions (21 pts)](#d4-skill-usability-conventions-21-pts)
- [D5 Security & op risk (21 pts)](#d5-security--op-risk-21-pts)
- [D6 Code & doc quality (31 pts)](#d6-code--doc-quality-31-pts)
- [D7 Dependency & footprint health (4 pts)](#d7-dependency--footprint-health-4-pts)

---

## Scoring system

**Total 115 points**

| Dim | Max | L1 applicable max | L2 (dryRun) applicable max | Core question |
|-----|-----|-------------------|----------------------------|---------------|
| D1 Process closure & idempotency | 13 | 13 | 13 | Will the run be correct? Is rerunning safe? |
| D2 Tool & command conventions | 10 | 10 | 10 | Are command calls safe and auditable? |
| D3 Portability & defense | 15 | 13 (D3-W2 skipped) | 15 | Will it run on someone else's machine? |
| D4 Skill usability conventions | 21 | 21 | 21 | Can a new user actually pick it up? |
| D5 Security & op risk | 21 | 21 | 21 | Is it safe after the run? Are high-risk ops protected? |
| D6 Code & doc quality | 31 | 31 | 31 | Is the code right? Does the doc match the code? |
| D7 Dependency & footprint health | 4 | 3 (D7-W1 skipped) | 4 | Is the overall architecture healthy? |
| **Total** | **115** | **112** | **115** | |

> 📊 **Scoring convention**: ①**ERR is uniformly 3 pts** — a hit means FAIL,
> the value is symbolic and not meant to encode false granularity;
> ②**WARN uses three real priority tiers** (high 3 / mid 2 / low 1) — the
> difference is meant to guide fix order.
> Note: the L1 applicable max already deducts skipped items (L1 max is 112,
> with D3-W2(2) + D7-W1(1) skipped). L2 (dryRun) absorbs L1 + Hub check +
> dependency existence + branch reachability simulation — the most complete
> depth. **L1 and L2 share pass line 90.**

## Design principles

```
Can it run?            → D3 Portability + D4 Usability conventions
Does it run correctly? → D1 Process closure + D6 Code & doc quality
Is it safe to run?     → D5 Security & op risk
Is it well-conformed?  → D2 Tool & command conventions
Is the whole healthy?  → D7 Dependency & footprint
```

## Pass criterion (dual-judgement)

The actual max and pass line differ by depth (skipped items don't count
toward the actual max):

| Depth | Actual max | Pass line | Skipped items |
|-------|-----------|-----------|---------------|
| L1 static | 112 | **≥ 90** | D7-W1 (1), D3-W2 (2) |
| L2 dryRun | 115 | **≥ 90** | none |

> ⚠️ **L1 max is only 112** (skips Hub check D7-W1, branch simulation D3-W2,
> etc. that need external systems), but the **pass line is still
> uniformly 90**. L2 dryRun max is 115 and the pass line is also 90.
> L2 dryRun does **read-only queries / reachability checks only** (file
> existence, env reachability, simulated unhit branches, Hub query); it
> performs **no writes or updates**.

**Judgement rules (both conditions must hold for PASS)**:

| Condition | Result |
|-----------|--------|
| Total ≥ depth-appropriate pass line **AND** zero ERR | ✅ **PASS** |
| Any ERR, **OR** total < depth-appropriate pass line | ❌ **FAIL** |

> WARN does not affect PASS / FAIL directly, but it lowers the total and
> can therefore drop you below the pass line.

---

## D1 Process closure & idempotency (13 pts)

> Core question: is this run correct? Is the second run safe?

### D1-E1 A write op must be followed by result verification (3 pts, ERR, L1)

**Scope of applicability**: applies only when the skill has real write
operations (upload files, call create / submit APIs, write DB, etc.). Pure
query / pure analysis skills skip this item (✅ treated as pass).

**Decision logic**:
- Scan scripts for real write-op calls: `upload_`, `submit_`, `create_`,
  `requests.post`, `requests.put`, `insert`, `write`, etc. (occurrences only
  in comments or strings don't count).
- Once confirmed as a write op, check whether there's a subsequent
  verification query: `query`, `get`, `verify`, `validate`, `assert`,
  `status_code`.
- If there's a write op but **no** subsequent verification → **ERR**.

**Typical mistake**:
```python
upload(file_path)
print("uploaded")  # ❌ no verification
```

**Correct**:
```python
resp = upload(file_path)
result = query_result(resp["id"])
assert result["status"] == "OK"
```

---

### D1-E2 Check whether the write op is already done before executing (3 pts, ERR, L1)

**Why**: for stateful / non-repeatable write ops, re-running causes
duplicate submissions or wrong data.

**Scope of applicability**: applies only when the skill contains a
**non-idempotent write** (submit order, create record, charge, etc.).
Idempotent writes (upsert, PUT replace) and pure queries → skip (✅).

**Decision logic**:
- If the skill contains a non-idempotent write op.
- And there's no `query` / `status` / `done` / `DONE` / `COMPLETED` /
  `exists` check before it → **ERR**.

**Correct**:
```python
status = query_status(item_id)
if status == "COMPLETED":
    print("⚠️ already done, skipping to avoid duplicates")
    sys.exit(0)
```

---

### D1-E3 Exception branches must halt the subsequent flow (3 pts, ERR, L1)

**Decision logic**:
- Obvious external I/O with no error handling at all → **ERR**.
- Error handling exists but the catch block is `pass` or only `print` without
  `exit` / `raise` / `sys.exit` → **ERR**.

---

### D1-W1 End-of-flow must emit a summary (2 pts, WARN, L1)

**Decision logic**: check whether the main script emits a summary at the
end (e.g. "checked N items, X passed", "send success N / fail N",
"processed N records").

- An obviously batch / multi-step flow with no summary at the end of the
  script → **WARN**.

> Pure single-step tool skills are not forced to have a summary, to avoid
> false positives.

---

### D1-W2 Detect redundant ops / pointless relays (2 pts, WARN, L1)

**Why**: unnecessary relays, transfers, or duplicate ops in the flow add
failure surface and produce no real output.

**Decision logic** (agent traces the data flow):
- Trace the file / data: where it comes from → what processing happens in
  the middle → where it finally goes.
- **Typical redundancy patterns (hit → WARN)**:
  - Round-trip within the same storage (A → download local → upload back to A).
  - Multi-step relay download (A → download local → pass to B → re-download → final storage).
  - The same file's row-count / format is validated repeatedly in multiple steps.
- **Not redundant (✅)**: middle steps that produce real output —
  decompress / merge / compute / format-convert etc.

---

## D2 Tool & command conventions (10 pts)

### D2-E1 Forbid raw HTTP or browser bypass for sensitive / controlled domains (3 pts, ERR, L1, configurable)

> ⚠️ **This rule only activates after the controlled-domain list is
> configured.** In the generic distribution the **controlled list is empty
> by default → this item defaults to ✅ pass**. If your team has internal
> services that "must go through SDK / CLI fronts and forbid raw HTTP
> direct calls", register them in
> [references/controlled-domains.md](./controlled-domains.md). The rule
> then activates for those domains.

**Decision logic**: once controlled-domains.md is configured with domains,
the simultaneous appearance of both is ERR:
- Access pattern: `requests.post` / `requests.get` / `fetch(` / `curl ` /
  `urllib` / `httpx` / `browser(` / `web_fetch(`.
- Hitting any configured controlled domain (fuzzy match).

> ⚠️ **Execution reminder (to avoid missed scans)**: HTTP calls must be
> **grepped as a full keyword set**, not just `requests.post`. In practice,
> `urllib.request.Request` / `urllib.request.urlopen` direct calls are common
> — searching only `requests` will miss them. Recommended:
> `grep -nE "urllib|requests\.|httpx|fetch\(|curl |browser\(|web_fetch\(" {file}`
> to list everything, then compare against domains one by one.

**Fix**: switch to the team-mandated SDK / CLI front for the controlled service.

---

### D2-W1 Audit dynamic command construction (3 pts, WARN, L1)

**Problem**: scripts that build CLI / shell commands by string concatenation
(`cmd = "tool " + user_input`, f-string-interpolating external input into a
command) **bypass static command scanning** and carry an injection risk.

**Decision**:
- grep `subprocess.*f"|subprocess.*+ |os.system.*+|cmd *= *.*\+|shell=True`
  and similar concat patterns.
- Hit, and the concatenation source contains external input
  (argv / input / env var / file content) → **WARN**: dynamic command has
  injection / audit-bypass risk; recommend switching to argument list
  (`subprocess.run([...])`) rather than shell-string concat.

---

### D2-W2 Hardcoded URLs must be audited (2 pts, WARN, L1)

**Why**: every hardcoded URL in scripts or SKILL.md must be audited to
confirm it's reachable across environments (different users / machines).

**Scan pattern**: `https?://[^\s"'>]+` (complete URLs in non-comment,
non-example contexts).

| Case | Level |
|------|-------|
| No hardcoded URL at all | ✅ pass |
| Already-configured controlled domain | Handled by D2-E1, not counted here |
| Other internal domain | **WARN**: confirm the endpoint can be called in the target environment (with auth) |
| External domain | **WARN**: confirm external link is reachable in the target environment, or note the access prerequisite in SKILL.md |

**Fix direction**: confirm call method for internal domains; confirm host
network reachability for external domains, or note the access prerequisite
in SKILL.md.

---

### D2-W3 Cross-layer command-call tracing (2 pts, WARN, L1)

**Problem**: a script `subprocess`-calls a shell script, and that shell
script then calls other commands / tools — this **cross-layer nested call**
is not traceable by static scans.

**Decision**:
- grep scripts for `subprocess.*\.sh|os.system.*\.sh|bash .*\.sh` → find
  the called shell scripts.
- Enter those shell scripts and grep for low-level sensitive calls (direct
  endpoint calls, undeclared external tools) → hit → **WARN**:
  cross-layer calls bypass conventions; recommend documenting the call
  chain in SKILL.md.

---

## D3 Portability & defense (15 pts)

### D3-E1 No hardcoded local absolute paths (3 pts, ERR, L1)

**Scan patterns**: `/home/[a-z0-9_-]+/`, `/Users/[a-zA-Z0-9_-]+/`,
`C:\\Users\\`.

**Exceptions (not deducted)**:
- In shell / command line: `<skills-dir>/`, `$HOME`, `~`
  (auto-expanded by shell).
- In Python: `Path.home()`, `os.path.expanduser("~")` — `Path("~/...")`
  is **not** in the exception list (Python does not auto-expand `~`; it
  results in an invalid path).
- Env-var reference: `os.environ.get("XXX_WORKSPACE")`, `$XXX_WORKSPACE`.

**Business-file path context tightening**:
- When the scenario is "read a data file" (hits on `pd.read_excel` /
  `openpyxl` / `pdfplumber` / `docx.Document` / `open(` parsing), the
  following paths **count as hardcoded ERR even in Python**:
  - Any concrete file path (filename + extension) hardcoded into the
    script, rather than passed in as a user argument or env var.
- Fix direction: pass via `sys.argv`, `argparse`, `os.environ.get(...)`.

---

### D3-E2 No hardcoded environment-specific fixed values (3 pts, ERR, L1)

| Type | Scan pattern | Exception | Level |
|------|-------------|-----------|-------|
| Hardcoded email | `[a-z0-9.]+@[a-z0-9.]+\.[a-z]+` in an assignment | comment / example not counted | ERR |
| Hardcoded token | `token\s*=\s*["'][a-zA-Z0-9]{20,}` | reads from config not counted; shares pattern with D5-E1, **don't double-count** when hit | ERR |
| **Hardcoded IP** | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` in an assignment | localhost / 127.0.0.1 / 0.0.0.0 not counted | ERR |
| **Hardcoded port** | `:\d{4,5}` in a URL / connection-string context | well-known ports 443/80/8080/3000 etc. not counted | WARN |
| **Hardcoded hostname** | `host\s*=\s*["'][^"']+["']` | reads from env / config not counted | ERR |
| **Hardcoded system absolute path** | `/app/` `/opt/` `/data/` `/etc/` `/var/` `/root/` in an assignment | non-`/home/` (covered by D3-E1); `/tmp/` is only WARN | ERR |

> ⚠️ **De-dup**: D3-E2 "hardcoded token" uses the same scan pattern as
> D5-E1. When the same line triggers both, count only **D5-E1**; the D3-E2
> token sub-item does not double-count.

---

### D3-E3 No hardcoded column indices (3 pts, ERR, L1)

**Scan**:
- pandas: `\.iloc\[.*,\s*\d+\]`, `row\[\d+\]` in an Excel / CSV parsing
  context.
- openpyxl: `ws.cell(row=..., column=N)`, `ws.cell(column=N)` where N is a
  hardcoded number.
- Index access on rows: `row[N]`, `data[N]`, `vals[N]`, `cells[N]`,
  `columns[N]` where N ≥ 10 (two-digit, excludes common loop indices 0/1/2).

**Header-mapping exemption (key — reduces false positives)**: within the
**30 lines preceding** the hit, if any of these appears, treat it as
"column-name mapping was already done" → **do not report**:
- `col_map`, `COLUMN_MAP`, `col_index`, `REQUIRED_COLS`, `get_col`,
  `_build_header_map`.
- `header` + `enumerate` combination, or column-name → index narrative.

**Decision**: hit on the hardcoded pattern with no header-mapping context
→ **ERR** (silently reads the wrong column when a layout table adds /
removes columns). Excludes comment lines.

**Correct**: `col_idx = df.columns.get_loc('OriginalAmount')`

---

### D3-W1 Forbid duplicating shared scripts across multiple skills (2 pts, WARN, L1)

The same filename appearing in 3+ skill directories → **WARN**; recommend
establishing a common `skills/shared/scripts/` directory.

---

### D3-W2 Branch reachability simulation (2 pts, WARN, L2 dryRun)

> ⚠️ **Read-only simulation. Absolutely do not actually run the audited
> skill.** The auditor performs **read-only reachability checks** (file
> existence, env-config reachability) over extracted branches, including
> the "unhit" ones. **Spawning a sub-session to run the audited skill is
> strictly forbidden.**

**Decision logic (L2 dryRun)**:
1. **Extract branches**: from SKILL.md (`if` / else / "does not exist" /
   branch-decision tables) and scripts
   (`if not os.path.exists`, `elif`, `else`, Bash `if [`), extract all
   conditional branches.
2. **Read-only simulate the unhit branches**:
   - **File-existence branches**: for paths referenced in the branch, the
     auditor verifies with `os.path.exists` → if absent, check whether
     SKILL.md / scripts have corresponding handling logic;
     **no handling logic → WARN** (will crash when the file is absent).
   - **Environment branches**: if a branch mentions env / different
     environments, the auditor greps the script for URL / config mappings
     for each environment → **any environment missing a mapping → WARN**
     (will fail when switching environments).
3. **Verify reachability only — do not execute business logic**: the
   auditor only runs side-effect-free commands like `os.path.exists` and
   grep.
4. Output each branch's "hit / unhit (simulated)" + reachability conclusion.

---

### D3-W3 Error messages must be actionable (2 pts, WARN, L1)

**Why**: when scripts catch exceptions / report errors with only "failed /
error / oops" and no guidance, users have no idea what to do next.

**Decision**:
- grep `except.*:\s*(print|raise).*("failed"|"error"|"failure")` and
  similar bare error-reports with no follow-up guidance text.
- High hit ratio (most key except blocks only report "failed" with no
  remedy) → **WARN**: error messages lack actionable guidance; recommend
  adding "cause + fix direction".

---

## D4 Skill usability conventions (21 pts)

> Core question: can a user (including non-technical) pick up this skill
> and actually use it?

### D4-E1 SKILL.md frontmatter must be complete (3 pts, ERR, L1)

Missing `name` or `description`, or no frontmatter at all → **ERR**

**`version` field sub-item (WARN, not counted toward the 3-pt ERR of
D4-E1)**: frontmatter missing `version` → **WARN**.
Rationale: `name` / `description` are hard ERR; `version` is required only
by some publishing channels and its absence does not affect the skill
running, so it's downgraded to WARN.

---

### D4-E2 description must include trigger timing (3 pts, ERR, L1)

Length < 30 characters, or no trigger-action wording (`when`, `use`,
`for`, `when the user`, `Use when`, etc.) → **ERR**.

---

### D4-E3 Must declare prerequisites (3 pts, ERR, L1)

**Why**: a skill must tell users "what to do before running this skill".

**Decision logic**: scan the full SKILL.md for any of:
- Structural keywords: `Prerequisites`, `Prereqs`, `Before you start`,
  `Before use`.
- Dependency wording: `depends on`, `requires installing`, `requires
  configuring`, `must first complete`, `required environment`,
  `requires permission`.
- Explicit exemption: `no special prerequisites`, `no dependencies`,
  `works out of the box`.

None of the above → **ERR** (even if there are no deps, you must
explicitly write "no special prerequisites").

---

### D4-E4 Required args must give a clear message when missing (3 pts, ERR, L1)

**Decision logic**:
- Scan scripts for arg reading via `sys.argv`, `argparse`, `input()`.
- If a required arg, when empty / missing, directly crashes with
  `KeyError` / `IndexError` and no friendly message → **ERR**.

**Correct**:
```python
if len(sys.argv) < 2:
    print("❌ missing required arg: target file path")
    print("usage: python3 run.py <file_path>")
    sys.exit(1)
```

---

### D4-E5 Packaged files must follow conventions (3 pts, ERR, L1)

**Scan scope**: recursive scan of the skill directory, **excluding**
`AUDIT-*.md`.

> **About `__pycache__` judgement**: packagers usually auto-exclude
> `__pycache__`, and Python is fully tolerant of stale `.pyc`, so
> `__pycache__` is a **packaging convention issue, not a runtime safety
> issue** — downgrade to **WARN**.

**ERR level (files that actually break runs or compromise security)**:

| File / dir | Reason | Level |
|-----------|--------|-------|
| `.git/` | Version-control history; may leak commits and credentials | ERR |
| `node_modules/` | JS deps; can be huge and break install | ERR |
| Packaged artifacts inside `*.zip` / `*.tar.gz` | Recursive nested packaging | ERR |
| `*.log`, `*.tmp` containing sensitive info | May leak tokens, API responses, user data | ERR |

**WARN level (does not affect runs, but breaks convention)**:

| File / dir | Reason | Level |
|-----------|--------|-------|
| `__pycache__/`, `*.pyc`, `*.pyo` | Local cache; packagers usually auto-exclude | WARN |
| `.gitignore`, `.DS_Store` | Dev-helper files; no real harm | WARN |
| `*.log`, `*.tmp` with no sensitive content | Lightweight temp files | WARN |

**About sign.key**: if present, **neither ERR nor WARN**. `sign.key` is a
signature-verification file auto-generated at release time; it contains no
private key and is a standard packaging artifact.

**About AUDIT-*.md**: if present, prompt the user to clean it up;
**neither ERR nor WARN** (audit residue; next packaging will auto-exclude
it).

---

### D4-W1 Directory-structure convention (2 pts, WARN, L1)

- Script files (`.py`, `.sh`, etc.) located at the top level instead of
  under `scripts/` → **WARN**.
- Doc reference files (`.md`, other than SKILL.md) scattered at the top
  level → **WARN**.

---

### D4-W2 High-risk ops must have guardrail statements (3 pts, WARN, L1)

Skill contains write ops but SKILL.md has no guardrail wording like
`forbidden`, `NEVER`, `must`, `MUST`, `strictly forbidden` → **WARN**.

---

### D4-W3 Key steps must give progress feedback (1 pt, WARN, L1)

**Why**: long stretches of silence make users think the skill is stuck.

**Decision logic**:
- Scripts contain `time.sleep(>30)`, polling loops, or large-batch loops.
- No `print` / `logging` progress output → **WARN**.

---

### D4-W4 Actionable error messages (merged into D3-W3, not separately scored)

> The check has been merged into D3-W3 for unified handling.

---

### D4-W5 Vague-instruction scan (advisory, not separately scored, L1)

**Why**: many skills are "agent-judged" (no scripts; SKILL.md instructs
the agent). Vague wording in SKILL.md makes the agent's behavior
unpredictable, so the same instruction yields different results across
runs.

**Decision logic (agent reads the SKILL.md body)**:
- Scan vague wording: `reasonable judgement`, `as appropriate`, `as needed`,
  `appropriately handle`, `generally`, `case by case`, `flexibly`,
  `decide for yourself`, `based on actual situation` (and their CJK
  equivalents).
- After a hit, determine whether the wording appears on a **key execution
  step / decision condition / write-op branch**:
  - On a key-step decision condition → mark **"recommend tightening"** in
    the report (high-priority advisory).
  - On non-critical auxiliary text → light advisory or ignore.

**Output form**: in the report, list under "🟡 Vague-instruction advisories"
the hit wording + the step it's in + an improvement suggestion. **No
deduction.**

---

## D5 Security & op risk (21 pts)

### D5-E1 No plaintext-stored sensitive credentials (3 pts, ERR, L1)

Scan assignments for sensitive patterns:
```
password\s*=\s*["'][^"']{3,}
secret\s*=\s*["'][^"']{3,}
token\s*=\s*["'][a-zA-Z0-9]{20,}
api_key\s*=\s*["'][^"']{10,}
```

**Exception**: read from `os.environ.get(...)` or from a config file is
not counted.

---

### D5-E2 High-risk ops must not hardcode `--yes` / forced-confirm bypass (3 pts, ERR, L1)

Hardcoding `--yes` / `--force` / `-y` in a write-op command (not
dynamically appended after user confirmation) → **ERR**.

**Exceptional scenarios (do not trigger ERR)**:

| Scenario | Criteria | Reason |
|----------|----------|--------|
| Fully automated orchestration script | SKILL.md explicitly states "this skill is an automated flow triggered by an upper-layer orchestrator with no interactive confirmation", and the same file has other safeguards | No-TTY scenarios cannot use `input()` |
| Query-class commands | `query`, `list`, `get` (pure reads) | Queries don't mutate data |
| Outer pre-check exists with explicit result | A status check before execution that proceeds only when the state is a specific executable value | Pre-check already replaces manual confirmation |

**Correct (interactive scenario)**:
```python
confirm = input("confirm? (y/n): ")
if confirm.lower() == 'y':
    run("tool action --yes")
```

---

### D5-E3 Forbid hardcoded credentials in URLs (3 pts, ERR, L1)

**Scan patterns (any hit → ERR)**:

| Pattern | Example |
|---------|---------|
| URL userinfo portion | `http://user:pass@host` |
| Credentials in URL query string | `?token=xxx` / `?api_key=xxx` / `?password=xxx` / `?secret=xxx` |
| Authorization header concatenated literally | `"Authorization: Bearer " + "hardcoded_token_xxx"` |
| requests / httpx `auth=("user","pass")` literal | `auth=("admin", "123456")` |

**Exceptions (do not trigger)**:
- Read from env var: `os.environ.get("API_TOKEN")`.
- Read from config: `config["token"]`.
- Placeholder / example markers: `<your-token-here>`, `${TOKEN}`, etc.

---

### D5-W1 Batch ops must have an upper-bound safeguard (3 pts, WARN, L1)

Write-op calls inside a loop with no `size` / `limit` / `MAX_BATCH`
constraint → **WARN** (recommended upper bound ≤ 30 items).

**Coverage rules (treated as "already safeguarded", does not trigger WARN)**:

| Coverage | Criteria |
|----------|----------|
| SKILL.md guardrail statement | SKILL.md has `forbidden` / `NEVER` / `strictly forbidden` guardrails that explicitly mention a batch upper bound |
| Code-level explicit limit | Script assigns `size` / `limit` / `MAX_BATCH` / `batch_size` ≤ 30 |
| Pagination loop has termination condition | Loop has a `total_count` upper bound or a `max_page` limit |
| Caller already rate-limits | SKILL.md says concurrency is controlled by the orchestration layer |

---

### D5-W2 Write ops must have a confirm step (3 pts, WARN, L1)

**Why**: interactive scenarios only. Pure scripts / non-interactive (no
TTY, no `input()`) scenarios are not checked.

**Decision logic**:
- The skill contains write-op commands (submit, upload, delete, etc.).
- The script has an interactive UI (`input()`, confirmation prompts) but
  no confirmation logic before the write op → **WARN**.

> Pure-automation scripts (no TTY) auto-skip this item.

---

### D5-W3 Plaintext-credential scan in config files (3 pts, WARN, L1)

**Why**: D5-E1 only scans **script assignments** for plaintext credentials;
it does not scan config file content (config.json / .env / *.yaml).

**Decision**:
- Scan all `.json` / `.yaml` / `.yml` / `.env` / `.ini` / `.toml` files
  under `{skill}/`.
- Match `token | secret | password | api_key | access_key` keys whose value
  is non-placeholder plaintext (not `<...>`, not `${...}`, not empty) →
  **WARN**: recommend env-var injection or runtime fetch.

---

### D5-W4 HTTP batch-write audit (3 pts, WARN, L1)

**Why**: directly calling HTTP endpoints for batch writes (`requests.post`
in a loop, batch-insert API) without an upper-bound safeguard.

**Decision**:
- grep `for .*requests\.(post|put|patch)|requests\.(post|put).*for |batch.*insert|bulk.*write`
  and similar HTTP batch-write patterns.
- Hit with no `len(...) <= N` / `MAX_` upper-bound check → **WARN**: HTTP
  batch write lacks an upper-bound safeguard; recommend adding a batch
  upper bound.

---

## D6 Code & doc quality (31 pts)

> Core question: is the code correct? Does the doc match what the code
> actually does?

### D6-E1 Script syntax is correct (3 pts, ERR, L1)

```bash
# Python
for f in $(find {skill-path}/scripts -name "*.py" 2>/dev/null); do
  python3 -m py_compile "$f" 2>&1 || echo "SYNTAX ERR: $f"
done

# Shell
for f in $(find {skill-path}/scripts -name "*.sh" 2>/dev/null); do
  bash -n "$f" 2>&1 || echo "SYNTAX ERR: $f"
done
```

Any file with a syntax error → **ERR**. Pass if there are no script files.

---

### D6-E2 Logic completeness defects (3 pts, ERR, L1)

Agent reads the code and judges:

| Defect | Example |
|--------|---------|
| Function has a branch with no `return`, and caller uses the return value | `def get_amount(): if cond: return 100` (no return on else) |
| Key business variable is assigned but never used | `total = calc()` but the rest of the code uses `amount` |
| Condition logic is inverted | `if not data: process(data)` |
| Dead code (statements after `return`) | `return result; print("done")` |

---

### D6-E3 Key boundaries are unhandled (3 pts, ERR, L1)

| Boundary | Risk |
|----------|------|
| None / empty values unchecked, API return used directly | `amount = data["amount"] * rate` (data may be None) |
| Division by zero unguarded | `avg = total / count` (count may be 0) |
| List / dict directly accessed without length check | `records[0]["amount"]` (records may be empty) |
| Excel / JSON string directly used in numeric ops | `total += row["amount"]` (may be a string) |
| `open(path)` without existence check | FileNotFoundError crash |
| HTTP request without timeout; `while True` without exit condition | Hangs forever |
| HTTP call **does not check response status**, body used directly | Treats failure response (4xx/5xx/gateway error page) as success — silent data error |

**HTTP response-status sub-item**: scan `requests.get/post`, `httpx`,
`urllib`, `fetch(` etc. calls. If the call is **not** followed by
`raise_for_status()`, a `status_code` / `resp.status` check, or `resp.ok`,
and the body is directly parsed / used (`resp.json()` / `resp.text`) →
**hits this sub-item**. Treating a gateway 5xx error page or a login
redirect page as business data causes silent errors.

When unable to judge, mark "needs human review", don't force a deduction.

---

### D6-E4 SKILL.md-described functional steps must have corresponding implementation (3 pts, ERR, L1)

**Why**: SKILL.md writes "Step 3: auto-upload", but the script has no
corresponding logic — description / implementation drift.

**Scope of applicability**: applies only when the skill has script files.
Pure-doc skills (no `.py` / `.sh` files) skip this item (✅ treated as pass).

**Decision logic** (agent judges):
- Extract the step list from SKILL.md (Step N / step N / numeric ordinals).
- Look for corresponding implementation in the scripts, allowing synonym
  mapping:
  - upload ↔ upload, submit, post
  - query ↔ query, get, fetch, list
  - generate ↔ generate, create, build, render
  - validate ↔ validate, verify, check, assert
- If a step is described too vaguely ("auto-handle", "execute the
  operation") to map → skip that step (handled by D4-W5 vague-instruction
  scan instead).
- If a step with a concrete action description has **no** semantically
  corresponding code in the scripts → **ERR**.

**Example-command / argument consistency sub-item (WARN, not counted
toward the 3-pt ERR of D6-E4)**:
- Extract command examples from SKILL.md (` ```bash ` blocks,
  `python3 xxx.py --arg` call samples).
- Compare with what scripts actually accept (`argparse`'s `add_argument`,
  `sys.argv` parsing).
- If the example's **arg name / sub-command / script path** does not exist
  or is mis-spelled relative to the script → **WARN**.

---

### D6-E5 Required reference paths in SKILL.md must exist (3 pts, ERR, L1)

**Decision logic**:

1. Extract all relative-path references from SKILL.md (paths starting with
   `scripts/`, `references/`, `assets/`).
2. Determine whether the path is "required" — preceded by keywords like
   "required / must / mandatory / depends on / make sure / needed".
3. **Required file missing → ERR.**
4. **Non-required file missing → WARN** (see D6-W3).

---

### D6-E6 Cross-table / cross-source field format compatibility (3 pts, ERR, L1)

**Why**: when two tables / two sources do join / field-match / rule-filter,
incompatible formats on the two sides cause **all rows to silently not
match and not error** — e.g. the rule column has
`100201 SomeBank` (code_name concat), the data column has `100201` only
(code only); the match result is empty but the program exits normally.

**Decision logic** (agent reads code + samples to judge):
- Scan scripts for two-source field-matching logic: `merge`, `join`,
  `isin`, `==`, `in [`, `map(`, dict-key lookup.
- Check whether the matched fields on the two sides are normalized
  (`.strip()`, `.split()[0]`, regex extraction, unified removal of name
  parts).
- If the fields on the two sides come from different sources (one from
  config / Excel, one from DB / API) and there is **no explicit format
  alignment** → **ERR**.
- When unable to judge the actual format on both ends → mark "needs human
  sampling", don't force a deduction.

---

### D6-E7 Key columns must be format-validated after parsing (3 pts, WARN, L1)

**Why**: reading key columns from Excel / CSV (dates, amounts, codes)
without explicit format validation and then using them in calculations
causes silent errors when upstream file format changes.

**Decision logic**:
- Scan access patterns: `df.iloc[...][col]`, `row["amount"]`,
  `ws.cell(...).value`, `data[col]` directly used in ops / concat.
- Check whether the access is followed by format validation:
  `re.fullmatch` / `re.match`, type assertion (`isinstance`, `float(x)`
  with try), range check, `datetime.strptime`.
- Key columns (semantic: "date / period / amount / code / period / amount")
  accessed and used **without any format validation** → **WARN**.

---

### D6-W1 Code completeness (2 pts, WARN, L1)

- `# TODO`, `# FIXME`, `# HACK` appearing in scripts.
- `def xxx():` whose body is only `pass` or `...` (not an abstract base).
- Placeholder strings like `"TODO"`, `"replace this"` not yet replaced.
- Hardcoded test data left over (`test`, `fake`, `mock` appearing in
  variable assignments).
- SKILL.md has no examples at all (input-arg example, expected-output
  example) → missing usage notes.

---

### D6-W2 Dependency-tool versions are declared (2 pts, WARN, L1)

**Decision logic**:
- Depends on third-party Python packages (e.g. `pandas`, `openpyxl`) but
  has no `requirements.txt` or version notes → **WARN**.
- Depends on an external CLI tool but SKILL.md has no minimum-version
  declaration → **WARN**.

---

### D6-W3 Non-required reference paths in SKILL.md missing (3 pts, WARN, L1)

**Decision logic**: relative paths referenced in SKILL.md (`scripts/`,
`references/`, `assets/`) without a "required" hard-constraint keyword,
and the file does not actually exist → **WARN**.

---

### D6-W4 Large codebase lacks test coverage (3 pts, WARN, L1)

**Decision**:
- `find {skill} -name "*.py" | xargs wc -l` total ≥ 2000.
- And `find {skill} -name "test_*.py" -o -name "*_test.py"` is empty and
  there's no TEST.md → **WARN**: recommend adding smoke / regression tests
  for the core scripts.

---

## D7 Dependency & footprint health (4 pts)

> Core question: is the overall architecture healthy and maintainable?

### D7-W1 Hub publish status (1 pt, WARN, L2 dryRun)

Extract `name` from frontmatter and check via the available skill-hub
query tool:
- Already published → pass.
- Not published → **WARN**: please publish before going live.
- Hub tool unavailable → mark "cannot verify", downgrade to WARN, do not
  abort.

---

### D7-W2 Dependency-skill list & health (2 pts, WARN, L1 extraction + L2 dryRun existence)

**Step 1: precise dependency extraction**

Scan each class to identify which other skills the audited skill truly
depends on. **For Python imports, looking at the `from X import` line is
not enough** — the module name X alone does not reveal which skill it
belongs to. You must apply the "three-step join + ownership lookup"
algorithm (below).

| Dep type | Scan pattern | Example |
|---------|--------------|---------|
| Cross-skill Python import | Use the "three-step join" algorithm below | `from query_app import load_token` → lookup ownership |
| `subprocess` calls other skill's script path | `skills/<x>/scripts/*.py`, `<skill_root>/scripts/xxx.py` concatenation | |
| External-CLI-tool-type skill | External CLI tool declared in SKILL.md | Archive / fetch dependency |
| Explicit declaration in SKILL.md | frontmatter `metadata.requires`, body "depends on xxx skill", "requires installing xxx" | Doc declaration |

#### 🔑 Python-import ownership decision: three-step join + lookup (core algorithm)

> **Background**: in `from query_app import load_token`, `query_app` is a
> **module name**, not a skill name. It could be ① an internal module of
> the current skill, ② a module of some neighbor skill, ③ a real
> third-party PyPI package. Looking at the import line alone cannot
> distinguish these and will mis-attribute / mis-omit ownership.

For each `from X import ...` / `import X` (X being a suspicious module
name not in stdlib and not in known PyPI), decide in order:

```
① Lookup inside this skill
   In <skills-dir>/<current-skill>/scripts/, look for X.py or def X(...):
     grep -rln "^\(def \|class \)X\b" {skill-path}/scripts/   # same-name fn/class
     find {skill-path} -name "X.py"                            # same-name module file
   Found → X is an [internal module/fn of this skill] → ❌ NOT an external skill dep, skip

② Look at sys.path injection / skill_root concatenation (determines ownership)
   In the same file as `import X`, look for:
     sys.path.insert(0, ... skills/<y>/scripts ...)
     <y>_skill_root = ... / "skills" / "<y>"
   If present, and X.py is actually under skills/<y>/scripts/ → X belongs to [skill <y>] → ✅ real external dep

③ Workspace-wide ownership lookup (fallback when ② has no clue)
   grep -rln "^\(def \|class \)X\b\|/X\.py" <skills-dir>/*/scripts/
   Single hit on skill <z> → X belongs to [skill <z>] → ✅ real external dep
   Multiple hits → ⚠️ ambiguous ownership, mark "suspected dep, ownership needs human"
   Zero hits → ⚠️ mark "non-skill dep (suspected PyPI / dynamic), not counted as a skill dep", no hard judgement
```

> ⚠️ De-dup + false-positive general rules:
> ① "Reference / similar to xxx skill" in the body is **not a call**,
>    doesn't count as a dep;
> ② An internal same-name module / fn of this skill doesn't count
>    (already filtered by ①);
> ③ A cross-skill dynamic import wrapped in `try / except ImportError` is
>    the **standard idiom** — still counted as a dep but marked
>    "soft dep (import-fail fallback)";
> ④ Stdlib and well-known PyPI packages are excluded outright.

**Step 2: annotate purpose per dep** (agent reads context to judge "what
the dep is used for")

**Step 3: existence verification (L2 dryRun)**
- Local `ls <skills-dir>/<dep>/SKILL.md` exists → **locally installed ✅**.
- Not local, hub has it → **hub-has-not-installed ⚠️**.
- Not local, hub also can't find → **not found ❌**.

**Decision**:
- Number of deps ≥ 5 → **WARN**; analyze each: core dep / can be inlined /
  recommend split.
- Depends on a "not found ❌" skill → **ERR** (will crash on run).
- Depends on a "hub-has-not-installed ⚠️" skill → **WARN**.
- Output the full list in report section "VI. Skill Dependencies"
  regardless of count.

---

### D7-W3 Skill footprint is reasonable (1 pt, WARN, L1)

Either of the following → **WARN**; give a split-direction suggestion:
- Script files ≥ 10.
- Total code lines ≥ 5000 (`wc -l` over script files).

---

## Known limitations

The following scenarios are not yet covered by the current rule set —
marked as future-version directions:

| Scenario | Impact | Suggestion |
|----------|--------|------------|
| Non-explicitly-declared runtime network deps | Currently only D2-W2 WARN-level coverage | If a security incident occurs, consider upgrading via controlled-domains.md to ERR |
| Deep static analysis for mixed-language skills | Currently Python / Shell focused | JS / TS only at syntax + manifest level |
