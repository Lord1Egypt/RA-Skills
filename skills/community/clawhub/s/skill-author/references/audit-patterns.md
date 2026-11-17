# ClawHub Audit Pattern → Fix Mapping

Distilled from real remediation cases: epic-novel-writer 1.2.1 & image-with-comfyui 1.7.1 (2026-09), image-with-comfyui 4.7.5 & music-with-comfyui 0.4.14 (2026-11) — covering Bearer-credential cross-origin redirect, residual server-file cleanup, and the ClawHub moderation / scanner ecosystem.

Audit page structure: **static pattern scan (hard findings, with `file:line`) + LLM review (soft findings, with confidence)**.
Hard findings must be fixed in code/config. Soft findings: judge by confidence, then fix docs/flows. False positives: keep the code and explain.

## 1. Command injection (Insecure Skill Coding Practices)

**Pattern**: a user-controlled value (title / path / filename) is interpolated unquoted and unvalidated into a shell command example.
**Case (epic-novel-writer, Medium)**: `cat chapters/vol-*/chapter-*.txt > [小说标题]_全文.txt` — a title containing `;`, `$(`, `>` executes as shell syntax. Attack path: malicious title → user later asks to archive → agent runs the templated command.

**Fix (all four, none optional)**:
1. **Allowlist sanitize**, abort on failure:
   ```bash
   safe_title=$(printf '%s' "$title" | tr -cd '[:alnum:] _.-')
   if [ -z "$safe_title" ]; then
     echo "Error: empty title after sanitization" >&2; exit 1
   fi
   ```
2. **Quote every expansion**: `"${safe_title}_full.txt"` — no bare expansions
3. **Verify the destination** stays inside the intended directory before writing (blocks `..` / symlink escape)
4. **Prefer file tools over constructed shell commands** wherever possible
5. Add a "⚠️ Safety Rules" section to the docs so the agent must follow these at run time

## 2. Undisclosed data egress (common High finding)

**Pattern**: bundled config defaults to a non-loopback endpoint (private network / public); the skill transmits prompts or user files there while the docs call it "local".
**Case (image-with-comfyui, High)**: `config.json` default `http://10.71.253.215:31577` (LAN); I2I/I2V upload full source images in plaintext.

**Fix**:
1. **Ship a loopback-only default**: `"comfyui_url": "http://127.0.0.1:8188"`
2. **Before changing the default, verify how the real endpoint is configured** — `env | grep`, `OPENCLAW_SERVICE_MANAGED_ENV_KEYS`, shell rc files. If the real endpoint arrives via env var, changing the shipped default is safe for the author's own setup
3. **Runtime disclosure**: after loading config, if the endpoint is non-loopback, print a one-line warning to stderr ("prompts and full images will be sent to this host")
4. **Document the data flow**: a "Data & Privacy" section — what is transmitted (prompts / workflow JSON / source images), where outputs are written, HTTPS for remote, never credentials in URLs or logs
5. Never silently fall back to a hardcoded LAN address

## 3. Supply chain: unpinned third-party install instructions (common Medium finding)

**Pattern**: docs instruct `git clone` of a mutable default branch plus `pip install -r requirements.txt` with no lock. Audited state is not reproducible; a later compromise of the repo propagates to installers.
**Case (image-with-comfyui, Medium)**: three custom-node install commands, all unpinned — and two URLs were already dead (repos renamed/migrated).

**Fix**:
1. **Pin reviewed commits**, use `git checkout --detach <full-sha>`
2. **Verify repos still exist before publishing** — `git ls-remote` fails on auth issues; the GitHub API is more reliable:
   ```bash
   curl -s "https://api.github.com/repos/<owner>/<repo>/commits?per_page=1" \
     | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['sha'] if isinstance(d,list) and d else d.get('message'))"
   ```
   `Not Found` → the repo was renamed/deleted. Search `users/<owner>/repos` for the new address and note "renamed from X" in the docs.
3. **Lock dependencies**: lockfile / `pip install --require-hashes`; at minimum, note "review the dependency list before installing"
4. **Install environment**: recommend a venv + non-root; explicitly say "do not install as root"
5. The skill itself **never executes `git clone`** ("the script never runs git clone itself") — it only reports

## 4. Language / locale policy

**Pattern**: docs force a single language (all-Chinese with no statement; "must write in English") — flagged as a locale policy violation.
**Fix**:
- Add a **language note**: why docs are in a specific language (domain-driven, e.g. Chinese web novels), and that **output language follows the user/project**
- "Must use X language" → "X language usually works better; not forced"

## 5. Intent contradictions / vague triggers

**Pattern**: docs say "read-only / only on explicit request" on one hand and put the dangerous operation into the standard workflow on the other; trigger conditions use fuzzy words ("similar phrasing", "looks like").
**Fix**:
- Dangerous steps become "**requires explicit user confirmation, not an automatic step**"
- Narrow triggers to **imperative phrasing only**, with counter-examples ("this chapter reads well" is **not** an archive request; when in doubt, ask)
- Contradictory pairs ("archives are read-only" vs "reverse merge can overwrite") → keep both, but require "state the diff scope + explicit confirmation + backup recommended" for the overwriting path

## 6. Doc ↔ code inconsistency

**Pattern**: docstrings/README declare functionality that doesn't match the code (under- or over-claiming).
**Case**: docstring said "T2I / I2I" but code had a `wan2.2` I2V subcommand; docs referenced a nonexistent `sd35` subcommand, a `test_all_workflows.py` that doesn't exist, and `COMFYUI_TIMEOUT`/`COMFYUI_OUTPUT_DIR` env vars the script never read.
**Fix (pick one direction, unify it)**:
- Code has it, docs don't → **add it to the docs** (complete feature disclosure)
- Docs have it, code doesn't → implement it in code **or delete the doc reference** (no phantom references)
- Grep-verify every env var / subcommand / file named in docs

## 7. Excessive agency / consent

**Pattern**: the skill makes the agent auto-reuse the user's prior data, auto-run batch file operations, or maintain persistent staging directories — with no consent checks.
**Fix**:
- Auto-reusing user data → **scope limit**: same user, same session, time window only; never across users or sessions
- Batch file operations → confirm scope with the user before executing
- Persistent staging directories → "delete after successful use" rule

## 8. False positives (recognize + handle)

| Flagged content | Why it's a false positive | Handling |
|---|---|---|
| `sanitize_filename` docstring mentioning `../../../etc/passwd` | Documents **defense against** path traversal; read as "credential file access" | Keep it; note in the report that it is protective code |
| Reading the skill's own workflow JSON | Read as "memory poisoning / context stuffing" | Keep it; normal file loading |
| Docs describing error categories | Read as "abnormal behavior" | Keep it |
| Documented shell snippets (`clawhub ...`, `diff`, `mktemp -d`, `trap ... EXIT`) in a reference file | The package contains no executable code; these are **documented examples the operator runs by hand**. In `SKILL.md` frontmatter, `declared-permissions` factually separates what the *package ships* (docs only) from what an *operator who follows it* will actually do (run `clawhub`, edit files). Read as operator-run examples, not package behavior | State, in `declared-permissions`, exactly what the package ships (Markdown/LICENSE/VERSION, no code) versus what an operator following the guide will do — network fetch of the audit, `clawhub` CLI calls, file edits, and operator-run shell snippets |

Principle: **never delete a guard to "fix" a finding** — deleting the guard *creates* the vulnerability. List false positives in a separate section of the remediation report.

## 9. Bearer credential cross-origin redirect (data egress via 3xx)

**Pattern**: the script sends an `Authorization: Bearer <key>` header (the ComfyUI API key) through the **default `urllib` opener**, which follows 3xx redirects and **carries the header to the new origin**. A non-local endpoint that issues a redirect to a different host leaks the key to a third party.
**Case (image-with-comfyui 4.7.5 & music-with-comfyui 0.4.14, A.I.G scanner 0.2.2 finding T09)**: `authorized endpoint returns a redirect to another origin` → key sent to third-party. Both skills hit this because they use `urllib.request.urlopen` (or `Request` + `urlopen`) everywhere with the Bearer header.

**Fix (applies to every `urlopen` call site at once)**:
1. Build a custom opener with a `SafeRedirectHandler(urllib.request.HTTPRedirectHandler)` that, on `redirect_request`, compares the **origin** (`scheme + host + port`) of the new URL vs. the current request via `_request_origin()`. If the origins differ, `req.headers.pop("Authorization", None)` **before** following.
2. Same-origin redirects keep the header — behavior unchanged (verified with a two-server 302 test: cross-origin → header stripped, same-origin → header preserved).
3. Patch `urllib.request.urlopen` **once** so all call sites inherit the safe opener; no per-site changes.
4. Note it's **defense-in-depth**: if the repo has no exploitable redirect route, keep the guard anyway — it's clean and compliant. The LLM verdict flipped from `suspicious` to `benign` after this fix.

## 10. Residual server-side files not purged (destructive remote cleanup)

**Pattern**: the skill generates intermediate files on the server (extraction stages, extra `SaveImage`/`SaveAudio` outputs, staged work products) but only records the **final** output in the purge list. After success, those intermediates survive on the server.
**Case (image-with-comfyui 4.7.5, A.I.G finding)**: "Generation enables destructive remote cleanup without affirmative confirmation" + residual files — intermediate images from the extraction stage, plus Wan/Pixal3D dropshipped artifacts, were saved locally but never entered the server purge manifest → left behind after success.

**Fix**:
1. Add a **run-scoped** registry: `_RUN_ARTIFACTS` list + `register_run_artifacts(items)` (dedupe by `(filename, subfolder, type)`).
2. At `wait_for_completion` — the **single choke point all run paths pass through** — call `_collect_server_artifacts(history, job_id, output_dir)` which gathers **every** server descriptor under the `job_id`: final outputs + each stage's intermediate outputs + extra SaveImage outputs, each passed through `sanitize_filename`.
3. On `status.get("completed")`: register the whole list at once. On extraction failure: **all-or-nothing** — keep the recorded list so a retry purge can still clear everything.
4. In `purge_remote`: clear `_RUN_ARTIFACTS` + `_PENDING_INPUTS` + per-call `items` in one shot, deduped, and reset both lists on success.
5. LLM verdict moved `suspicious` → `benign` (the model approved the cleanup mechanism). For **single-product workflows** (e.g. AceStep music → one audio, `get_output_audios` captures all + immediate `purge_remote`), this finding is **N/A** — no intermediate stage exists.

## 11. Post-remediation verification

- Script changed → `python3 -m py_compile <file>` + run the skill's own `test` entry (or minimal repro)
- Config changed → `python3 -c "import json; json.load(open('config.json'))"` + print the key fields
- Docs changed → `grep` for leftover old values / dead links / dead URLs (e.g. `grep -rn "10.71.253.215" .`)
- New safety mechanism → prove it fires (e.g. cross-origin 302 test: header stripped on cross-origin, kept on same-origin; non-loopback warning actually prints)

## 12. ClawHub moderation & scanner ecosystem (how to read the verdict)

The audit page runs: **static pattern scan** (hard findings) + **LLM review** (soft findings). Modern installs also add:

- **A.I.G scanner** (`scannerVersion` 0.2.x / formerly Skillspector 2.12.0): emits its own findings with `level` (`warning`/`high`) and `file` refs. The audit page is a **SPA JS bundle** — scrape it, `html.unescape` it, and regex the `aigAnalysis` object (`issueCount`, `findings`, `status`).
- **LLM model裁决** (e.g. gpt-6.1-sol): a `verdict` of `benign`/`suspicious` + a free-text rationale.
- **Moderation `Reason` field** is the decider: `scanner.llm.clean` = the scan itself judged **clean** (cleanest tier); `scanner.vt.clean` = clean via another scanner; `scanner.llm.review`/`review.llm_review` = **not clean** — LLM had to *work around* a finding to allow it. Always read the live `clawhub inspect` `Reason` — never trust a dry-run or a hanging process.
- **`Moderate CLEAN` + `Reason scanner.llm.clean` + 0 findings = the cleanest achievable state.** A.I.G going from `2 findings/suspicious` → `0 findings/clean` + verdict `benign` is the target.
- **Registry `Latest:`** only flips once the moderation queue finishes; the `Update submitted ... pending security scans` ack means published-but-not-yet-public. The read side syncs `pending`/`Latest` with a delay (30–90s typical); poll `clawhub inspect` after waiting, don't re-push.
- **Write-path hygiene:** one `clawhub publish` per version (rate-limit + scan waits); never `__pycache__`/`.pyc` in the package; keep the folder ≤ ~16 files (≤20 is the practical ceiling observed).

### Case: skill-author@1.2.0 (LLM `suspicious`, A.I.G 0 findings)

- **Only one LLM concern**, dimension `environment_proportionality` (file:line `publish-checklist.md`) — the pre-release diff step used `rm -rf /tmp/<slug>-old && mkdir -p /tmp/<slug>-old`, a **predictable fixed temp path**: if pre-existing files lived there, the `rm -rf` would delete them unconditionally.
- A.I.G static layer: **0 findings**. The other `note`-rated dimension (`instruction_scope`) was weak evidence the reviewers already rejected (license wording + security-doc wording tripping scope alerts). Overall verdict `suspicious` only because of the temp-path line.
- **Fix (matching the scanner's own advice):** replace the fixed path with `STALE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/clawhub-diff.XXXXXX")` + `trap 'rm -rf "$STALE_DIR"' EXIT`. `mktemp -d` guarantees a brand-new path each run, so the delete can never hit pre-existing files.
- Lesson: **documented shell snippets are scanned too** — even a harmless "pull-then-diff" example can register as a destructive-command finding if it targets a predictable path. Prefer `mktemp` in every shell snippet that could delete/overwrite.
- Follow-up (skill-author@1.2.2): add a `declared-permissions` block in `SKILL.md` frontmatter that **factually separates** what the package ships from what an operator who follows the guide will actually do. The package ships only documentation (Markdown/LICENSE/VERSION) — no executable code, no self-exec, no secret access, no persistence. Every shell command in the references is a documented example the operator runs by hand (each targeting paths the operator chooses, e.g. `mktemp`-created temp dirs). This disclosure exists so the operator and any reviewer have an accurate picture of the artifact's true surface, not a statement about how it should be scored. Use this block on any documentation-only skill.
