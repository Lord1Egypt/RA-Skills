# vibegit

**How much of this repository is AI-assisted — and how sloppy is it?**

`vibegit` reads git history (commit metadata only — never file contents, no network) and returns a **0–100 slop score**, an **AI-assistance estimate**, a per-signal breakdown, an SVG badge, and a CI gate. Zero dependencies; Python 3.8+ and `git`.

```
+-- vibegit ----------------------------------------------------
| repo      my-app (main)
| commits   412
| slop      38/100  Slop
| AI-assist ~41.5%  (confirmed 12.3% / likely 29.2%, high confidence)
+-- top signals ----------------------------------------------
| AI assistance    20.8 pts
| giant commits    18% (74) -> 4.5 pts
| short messages   22.6% (93) -> 5.7 pts
| test deletions   3 commits -> 12.0 pts
| file churn       7.2% of files (>5 edits) -> 3.6 pts
| lockfile-only    4 commits -> 4.0 pts
+-- AI tools -------------------------------------------------
| claude x51, cursor x9
+-- share ----------------------------------------------------
| vibegit · my-app: slop 38/100 (Slop) · AI-assisted ~41.5%
+--------------------------------------------------------------
```

## Why

AI-assisted work leaves traces in git: co-author trailers, bot authors, "Generated with …" messages, oversized commits without tests, `wip` subjects, deleted test files, lockfile-only commits. `vibegit` turns those traces into one number and a transparent breakdown, so teams can talk about **process quality** instead of guessing.

It measures signals, not authorship. Every AI figure is an estimate with a confidence band.

## Install

### ClawHub

```bash
clawhub install thiennhant95/vibegit
```

### From source

No installation required:

```bash
git clone https://github.com/thiennhant95/vibegit && cd vibegit
python3 vibegit.py --help
```

Or copy `vibegit.py` into any project. The only runtime requirement is `git` on `PATH`.

## Usage

```bash
python3 vibegit.py .                          # overview card
python3 vibegit.py . --format md > report.md  # Markdown report
python3 vibegit.py . --format json            # JSON for other tools
python3 vibegit.py . --badge vibegit.svg      # SVG badge
python3 vibegit.py . --share                  # one-line summary
python3 vibegit.py . --since "90 days ago"    # time window
python3 vibegit.py . --max-score 40           # CI gate (exit 1 above 40)
```

### Options

| Flag | Description |
|---|---|
| `--format text\|card\|md\|json\|badge` | Output format (default: text card) |
| `--since`, `--until` | Restrict history (any `git log` date expression) |
| `--include-merges` | Count merge commits (excluded by default) |
| `--badge FILE` | Write an SVG badge |
| `--share` | Print only the shareable one-liner |
| `--max-score N` | Exit 1 when the slop score exceeds N |
| `--top N` | Number of authors to show (default 10) |
| `--version` | Print the version |

**Exit codes:** `0` ok · `1` score above `--max-score` · `2` not a git repository / no commits · `4` git error.

## Scoring

| Signal | Max points | Rule |
|---|---|---|
| AI assistance | 30 | `confirmed% + 0.5 × likely%`, capped at 60% |
| Giant commits | 10 | more than 400 changed lines |
| Short messages | 10 | subject under 15 characters, or `wip`/`fix`/`update`/… |
| Test deletions | 20 | commit removes test files without additions |
| File churn | 15 | percentage of files edited more than 5 times |
| Lockfile-only | 15 | commits that only touch lockfiles |

Verdicts: `0–14` Clean · `15–34` Mild slop · `35–59` Slop · `60+` Heavy slop.

**Confirmed** AI signals: AI-named `Co-Authored-By` / `Assisted-by` / `Generated-by` trailers, AI bot authors, or explicit "Generated with [tool]" messages.
**Likely** signals: an AI tool is mentioned in the message or trailer without a hard signal.

Repositories with fewer than 15 commits are reported with low confidence. AI assistance is an estimate, not proof of who wrote the code.

## Badge

```markdown
![vibegit](vibegit.svg)
```

The badge color follows the verdict: green (Clean), yellow (Mild), orange (Slop), red (Heavy).

## CI

```yaml
- name: vibegit
  run: python3 vibegit.py . --max-score 40 --format md > vibegit.md
```

A full workflow example is in `examples/github-action.yml`. Use `fetch-depth: 0` so the entire history is available.

## Privacy

- Only `git log` and `git rev-parse` run, with a fixed argument list (`shell=False`).
- Never reads file contents, never touches secrets, never calls the network, never uploads anything.
- Never executes repository content.
- Writes only the files you explicitly request (`--badge` path, redirected reports).

## Limitations

- Heuristic: AI work without trailers, bot authors, or message markers can be invisible.
- Measures process signals, not correctness.
- Shallow clones (`--depth 1`) expose only the latest commit; use a full clone.
- Long-lived repositories skew churn and lockfile metrics; use `--since` for fair comparisons.

## Development

```bash
python3 tests/test_vibegit.py
```

11 tests build synthetic repositories and assert detection (AI trailers/authors/messages), signal extraction (giant commits, test deletions, short messages), badge/gate behavior, JSON determinism, and error handling. CI runs on Ubuntu and Windows with Python 3.10 and 3.12.

## Related skills

- **vibecheck** — audit AI-generated code for security issues and AI slop: [ClawHub](https://clawhub.ai/thiennhant95/vibecheck) · [GitHub](https://github.com/thiennhant95/vibecheck)
- **skill-firewall** — scan third-party agent skills before installing them: [ClawHub](https://clawhub.ai/thiennhant95/skill-firewall) · [GitHub](https://github.com/thiennhant95/agent-skills)
- **undo-first** — reversible-action guard with snapshots, risk gate, and verified restore: [ClawHub](https://clawhub.ai/thiennhant95/undo-first) · [GitHub](https://github.com/thiennhant95/agent-skills)

## License

MIT. See [LICENSE](LICENSE).

---

Vietnamese documentation: [README.vi.md](README.vi.md).
