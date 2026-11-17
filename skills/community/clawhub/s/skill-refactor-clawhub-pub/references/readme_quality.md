# README.md quality (the `readme` mode)

Load-on-demand home for the skill's README optimization capability (mirrors design
doc §7). The body only keeps "five questions + fixed order + a routing pointer";
all field rules live here. The fill-in skeleton lives in `assets/readme_template.md`.

Source consensus: 8 mainstream README guides (devhexlab / markcallen / shiftquality
/ devtoolkit / markdowneditoronline / vibe-coding-tools / csdn / wikiplus) — this is
the intersection, not one blog's opinion.

## 1. The five questions (a README must answer)

1. **What is this?** — what it does + for whom + the differentiator (1–3 sentences,
   written for someone who has never heard of it).
2. **How do I install / run it?** — the smallest path to working, < 10 minutes.
3. **How do I use it?** — a real example, most-common case first, copy-runnable.
4. **How do I contribute?** — fork/branch/PR path + contribution entry.
5. **What else should I know?** — license (missing = "all rights reserved", blocks
   adoption), status (production / beta / experimental).

**Fixed order (decreasing urgency — do not reorder):** name one-liner → badges →
what/why → quick start → install → usage → configuration → architecture →
contributing → license. Readers scan top-to-bottom; the first question sits at the
top.

## 2. Field rules (do these to pass)

| Field | Rule |
|---|---|
| one-liner | verb first: "Converts CSV to Markdown tables", not "This is a CSV project"; say what + for whom |
| badges | 3–5 max, each carrying a **changing** value (CI / version / license / downloads); 20 badges is noise; fill `{org}/{repo}` from the real git remote, never invent |
| TOC | only when >5 sections; anchor `#installation` (GitHub auto-builds H2 anchors) |
| install | prerequisites (runtime/version) **before** the command; the full clean-checkout command; don't assume the reader knows the ecosystem |
| usage examples | most-common case first; each self-contained and copy-runnable; library → common API, CLI → common flags, API → full request/response |
| configuration | a **table** (Option/Type/Default/Description), not prose; env rows must match `.env.example` keys exactly (two files must not drift) |
| images / GIF | store in `docs/images/` via relative path (most reliable); always write alt text; GIF < 5MB / < 10s; architecture: prefer ```mermaid (GitHub renders natively, won't go stale) over external images |
| collapsible | long config tables behind `<details>` to keep the body scannable |
| multilingual | internationalized projects offer a switch: `[English](./README.md) · [中文](./README.zh-CN.md)` |

## 3. What stays OUT of a README (avoid bloat / drift)

| Don't put in | Put in | Why |
|---|---|---|
| architecture detail | `docs/architecture.md` | a README is a start guide, not an architecture doc |
| full API reference | generated API docs / a reference file | ditto |
| changelog | `CHANGELOG.md` / GitHub Releases | first-time readers don't care about project history |
| origin story | a blog post | noise |
| every badge | — | keep the 3–5 that change |

**Stale is worse than no README** — outdated instructions send people down a dead
end and erode trust. Rule: a PR that changes install / config / public API **must**
update the README in the *same* PR (not a follow-up); pin a `Last updated: <date>`
line at the top of docs that evolve.

## 4. Failure modes (self-check while writing)

- value proposition buried under a TOC or a badge wall (no "what is this" in the first seconds)
- a wall of text with no visuals / no sectioning
- an install command that only works on **your** machine (mentally test a clean checkout)
- describing a feature instead of showing a runnable example
- referencing an API/commands two releases old
- an invented badge org; env rows not matching `.env.example`

## 5. `readme` mode — five steps (single-turn closed loop)

1. **Resolve:** target = the repo's `README.md` (missing → start from the
   `assets/readme_template.md` skeleton; present → polish). Pick host + language
   (i18n_policy §3 three-state).
2. **Read + screen:** read the README + nearby `.env.example` / `package.json` /
   `LICENSE` / git remote. `check_skillmd.py` does not lint READMEs, so cross-check
   the §2 table by hand.
3. **Plan changes against the five questions + §2 + §4:** tag each old→new + reason
   + assumed? + P0.
4. **Emit:** refactor (back up first, H2) or audit-only report
   `readme_audit_<name>.md` (H1, don't touch the original); preview with `present_files`.
5. **Close:** summary + assumptions + "does `.env.example` need syncing? add an
   i18n switch link?"; state the boundary — this skill does not fix called code.

## 6. Where this sits in the main file

- the 5-step flow Step 1 now lists `readme` as a third mode; the routing table
  points here.
- §2/§3/§4 sink into this file; the body keeps only "five questions + fixed order +
  routing pointer" (still within the 8000 / first-3000 token budget).
- README language follows i18n_policy §3 — do not duplicate.
