# SkillQA Pro

[![Selftest CI](https://github.com/vnbochkarev-netizen/ViBo-SkillQA/actions/workflows/selftest-ci.yml/badge.svg)](https://github.com/vnbochkarev-netizen/ViBo-SkillQA/actions/workflows/selftest-ci.yml)

**Certify your skills. Sell with confidence.**

SkillQA Pro is an autonomous QA and certification tool for AI agent skills (OpenClaw / ClawHub): it runs your skill through seven deep checks and produces a shareable quality certificate buyers can trust.

> **v0.2.0** · Python 3.10+ · pip-free · OpenClaw-ready · ClawHub-ready

---

## Why SkillQA Pro exists

The AI agent skill market is growing fast. OpenClaw, ClawHub and dozens of agent frameworks now let anyone publish skills — and thousands of authors are shipping them every month. But the ecosystem has a hole:

- **Authors have no QA tool.** There is no standard way to check whether a skill is well-structured, crashes, leaks secrets, duplicates an existing one, degrades under load, or breaks on another Python version.
- **Buyers have no proof of quality.** Marketplace listings are a description and a star rating. Nobody knows what's actually inside.
- **Bad skills hurt everyone.** One skill that hardcodes your `~/.openclaw` path or prints your API key into a log erodes trust in the whole marketplace.

**The niche is wide open — SkillQA Pro fills it.**

SkillQA Pro is the missing quality gate for the skill economy: an autonomous tester that runs any skill folder (`SKILL.md` + scripts) through **7 verification modules**, grades it **A/B/C/D**, and issues a **certification report** that the author can show to buyers, and that CI can consume as JSON.

---

## Features

### Seven verification modules

| Module | What it checks |
|---|---|
| 🛡️ **Static scan** | Structure: `SKILL.md` exists, valid YAML frontmatter (`name`, `description`, `version`), referenced files exist, no empty/broken files, no magic absolute paths, sane sizes, consistent versioning. |
| 🧪 **Sandbox run** | Behaviour: auto-discovers `*.py` / `*.sh` / `*.js`, runs each in an isolated sandbox with fake env and tokens, checks exit codes, `--help` handling, no-args behaviour, crashes and hangs. |
| 📜 **Log audit** | Logging hygiene: does the skill log, where, is there rotation, are errors readable (`file:line`), and — critically — **no secret leaks**: hardcoded secrets in code/logs (Bearer tokens, `sk-…`, `token=…`, AWS keys, private keys, long hex/base64) **and production secrets in `.env*` files** (`.env`, `.env.production`, `.env.local`, `*env*.prod`). Env values are classified `severe` / `dev` / `unknown` and **always masked** in reports (`first4***last3`) — full values never leave the tester. |
| 🔍 **Novelty** | Originality: compares against your local skill library (`~/.openclaw/skills`, workspace, ClawHub cache) for name collisions and description overlap; verifies the skill isn't an empty shell and includes usage examples. |
| ⚡ **Load test** | Performance: runs the main script N times (default 20, `--load N`), reports min/avg/max/median timings and peak RSS, flags progressive degradation and memory leaks, kills hangs. |
| 🔀 **Parallel test** | Concurrency: launches 5–10 simultaneous instances, detects deadlocks, races, shared temp-file conflicts and runaway processes. |
| 🔧 **Compat check** | Compatibility: detects required Python version from code features (match/walrus/type unions), parses `requirements.txt`/`pyproject.toml`, verifies imports, and test-runs the skill on every installed Python (3.10/3.11/3.12). |

### Core capabilities

- ✅ **Self-testing (`selftest`)** — SkillQA Pro tests *itself*: it runs its own code through static + sandbox checks, hunts down every intentionally planted bug in a reference "bad" skill, verifies a clean reference skill passes, and confirms 3 consecutive runs produce identical results. If the tool is broken, it tells you before you trust it.
- 🔒 **100% sandboxed execution** — every script runs in a temporary copy of the skill with fake tokens, no network, no real home directory, and a hard timeout-kill. Your machine and the author's skill never touch each other for real.
- 📄 **Certification reports** — a polished Markdown certificate (grade, per-module verdicts, check-by-check details) ready to show to buyers, plus machine-readable JSON for CI pipelines (Pro edition).

---

## Quick start

**Requirements:** Python 3.10 or newer. That's it — no `pip install`, no dependencies, no build step. Download the package, unzip, run.

```bash
# Test any skill folder (OpenClaw skill, ClawHub package, your own):
python3 skillqa.py test ~/.openclaw/skills/my-skill

# English output:
python3 skillqa.py test ~/.openclaw/skills/my-skill --lang en

# Verify SkillQA Pro itself is working correctly:
python3 skillqa.py selftest

# Show version / help:
python3 skillqa.py --version
python3 skillqa.py -h
```

### Options

| Option | Description |
|---|---|
| `--lang ru\|en` | Report and console language (default: `ru`). |
| `--skip static,load` | Skip specific modules (also reads `.qaignore` in the skill folder). |
| `--load N` | Number of load-test runs (default: 20). |
| `--parallel [N]` | Enable the parallel test with N instances (default 5, range 5–10). |
| `--timeout S` | Per-run timeout in seconds (default: 15). |
| `--demo` | Force free demo mode (static scan + teaser report only). |
| `--pro` | Force Pro mode (requires a valid license; exit code 3 otherwise). |

License management:

```bash
python3 skillqa.py license --status      # show license state
python3 skillqa.py license --machine-id  # print this machine's ID
python3 skillqa.py license --install license.key   # activate Pro
```

**Exit codes:** `0` — no failures · `1` — failures found · `2` — usage error · `3` — license missing/invalid for `--pro`.

Reports land in `./qa_reports/<skill_name>/` automatically.

---

## The certification report

Every Pro run produces a **certificate-quality Markdown report** you can attach to your marketplace listing or send to a buyer:

- 🏅 **Overall grade — A, B, C or D** — computed from per-module scores (`pass` = 2, `warn` = 1, `fail` = 0) with a hard rule: crashes or secret leaks cap the grade at **B**, no matter the score.
- 📋 **Per-module verdicts** — a table of all 7 modules with status, execution time and check counts, followed by a detailed section for each module: every check with its icon, name and localized explanation.
- ⚙️ **Environment summary** — skipped modules, total runtime, Python and OS versions.
- ✍️ **Signature** — *"Certified by SkillQA Pro"* with the owner's machine ID and license term.

The same run produces a **JSON report** (Pro) with the full machine-readable structure — `grade`, `score_pct`, `fail_count`, per-module results — ready for CI gates, marketplaces and automated listing filters.

Demo mode gives a **teaser report**: the static-scan result plus a preview of what the full Pro certificate includes.

---

## How it works

SkillQA Pro takes safety seriously — for both sides:

- **Everything runs in a sandbox.** The skill is copied into an isolated temp directory (`skillqa_*`) and executed only from the copy. The original folder is read-only and never modified.
- **Fake environment.** Scripts get scrubbed env vars — `HOME`, `TMPDIR` and working directories all point inside the sandbox — and **fake tokens** replace every real credential (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `AWS_*`, `HF_TOKEN`, `DATABASE_URL`, …). Any variable whose name hints at a secret is overwritten.
- **No network.** When possible, scripts run in a network namespace with connectivity removed; otherwise proxies are stripped and `NO_PROXY=*` is set.
- **Timeout-kill.** Every execution is wrapped in a hard `timeout --kill-after=2 --signal=KILL`; a hung script is killed, marked `timed_out`, and reported as a failure — never allowed to run forever.
- **`rm -rf` is impossible outside the sandbox.** Isolation is enforced by environment and paths; the only directory the tool ever deletes is its own `skillqa_*` temp root.

**Sandbox limitations (honest):** the sandbox isolates tested scripts via scrubbed environment, network-disabled namespaces (when possible), path confinement and hard timeout-kills. It is **not** a VM/container security boundary (no cgroups/seccomp). For untrusted or potentially malicious skills, run SkillQA inside a disposable VM or container.

**Access scope (disclosed):**
- **Reads:** the selected skill folder (including `.env`-like files, for secret checks); novelty *metadata* (names/descriptions) of local skill libraries under `~/.openclaw/skills`, `~/.openclaw/workspace/skills`, `~/.claude/skills` and `$OPENCLAW_SKILLS_DIR`; license state at `~/.config/skillqa/skillqa_license.dat`.
- **Writes:** QA reports to `./qa_reports/<skill>/` (absolute skill path + content hash included for certification); license file to `~/.config/skillqa/` (Pro / selftest).
- **Does not access:** the network; real secret values (found secrets are reported as findings with masked fragments only, never echoed in full); any other files outside the paths listed above.
- **Fixtures** under `fixtures/bad_skill/` are *intentionally bad examples* (fake secrets like `sk-abc…`, leaky scripts) used to verify detectors — they run only inside the sandbox, never against real data. The marketplace package ships WITHOUT `fixtures/` (they live in the GitHub source repo for selftest).

---

## License & pricing

| | **Demo** (free) | **Pro** |
|---|---|---|
| Static scan | ✅ | ✅ |
| Sandbox run, Log audit, Novelty, Load, Parallel, Compat | — | ✅ |
| Full certificate report (Markdown) | teaser only | ✅ |
| JSON report for CI | — | ✅ |
| Price | **Free** | **$X** (one-time, placeholder) |

The demo edition is free forever — run the static scan on any skill and see the teaser report. Upgrade to Pro to unlock all 7 modules, the full certificate and CI-ready JSON.

**Payment methods:**
- 💵 USDT (TRC20): `T...` *(wallet placeholder — to be set before release)*
- ⭐ Telegram Stars: `@...` *(handle placeholder — to be set before release)*

After payment you receive a license key bound to your machine ID. Install it with `skillqa.py license --install license.key` and run `--pro` — or just run the tool and let it pick up Pro automatically when a valid license is present.

---

## Roadmap

- [x] **v0.1.0** — 7 verification modules, sandbox, reports (MD+JSON), selftest, demo/Pro licensing.
- [ ] **v0.2** — HTML certificate export, batch testing of a whole skill library, ClawHub API integration.
- [ ] **v0.3** — Plugins for more agent frameworks (n8n, Claude, custom), online license validation, marketplace manifest generator.
- [ ] **v1.0** — SkillQA Pro badge API for marketplaces ("verified by SkillQA").

---

*SkillQA Pro is an independent tool and is not affiliated with OpenClaw or ClawHub.*

© 2026 SkillQA Pro by Viacheslav Bochkarev

## 🤖 GitHub CI (optional, 1 file)

Add `.github/workflows/skillqa-ci.yml` (from this repo) to YOUR skill repository —
every pull request gets an automatic SkillQA report in a comment:

- triggers on PRs and pushes touching `SKILL.md` / `skills/**` / `scripts/**`
- runs `skillqa test` (static + sandbox + log + novelty + compat, `--skip load,parallel`)
- posts the grade (A–D) and per-module verdicts as a PR comment
- no secrets, no network access for the skill itself (sandboxed)

Your buyers see quality checks running — not just promises.

## How grades work (A · B · C · D)

Grades are **calculated, not awarded**:

| Grade | Requirement |
|---|---|
| **A** | 0 fails + score ≥ 85/100 |
| **B** | ≤ 1 fail + score ≥ 65/100 (crashes or secret leaks cap at B) |
| **C** | score ≥ 45/100 |
| **D** | below |

Score = `(2 × pass + 1 × warn + 0 × fail) / (2 × modules)`. Every check
carries a concrete detail (`file:line`, script output, exit code) — the
grade is reproducible by anyone running the same version of the tool.

## Certificate integrity

Each certificate is **bound to the SHA-256 of the tested skill content**.
Change the skill → the old certificate no longer matches → run the test
again and get a fresh certificate. No cherry-picking after edits.

## Next grade roadmap

Every report includes a **Next grade roadmap** section: the exact checks
that hold the grade back and what to fix to move up (D → C → B → A). After
fixes, re-run — the new certificate reflects the new content.

## GitHub CI (one file)

Add `.github/workflows/skillqa-ci.yml` to a skill repository: every PR that
touches `SKILL.md`/scripts is tested automatically and the bot posts the
certificate summary as a pull-request comment.

```yaml
# copy from this repository: .github/workflows/skillqa-ci.yml
```

## Licensing

- **demo** (free): static scan + teaser report
- **pro** ($5/month, 250⭐ or 5 USDT): all 7 modules, full certificate,
  JSON report, `Next grade roadmap`, CI support

License key: `vibo skillqa license --install <key>` (bound to machine-id).

---

© 2026 Viacheslav Bochkarev · wwwvibo.com
