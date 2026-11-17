---
name: vibe-ledger
description: Explain an AI-built ("vibe-coded") app to the person who made it and check it at the same time. Draws the project's files as an interactive flowchart — click a file to read what it does, what calls it, its main functions, its risks and how it came to be — and, from the Claude Code and Codex conversations that built it, checks every requirement the user gave against the code (done, partly, not done, done differently, superseded) and keeps a ledger of what was asked for, claimed and put off, each checked against verified code evidence. Renders one offline HTML page (flowchart, a requirements tab, and an overview with app map, who-can-see matrix, conversation timeline and call paths). Use when someone wants to understand or sanity-check an app an AI wrote — "explain my app", "how do my files connect", "what did the AI actually build", "did it do what I asked", "is my vibe-coded app safe", "AI 有没有按我的要求做", "帮我看懂这个 AI 写的项目", "这些文件之间怎么调用的", "检查一下 AI 写的代码有没有问题". Runs locally and sends nothing anywhere.
---

# vibe-ledger

Draws the project's files as a flowchart the user can click through, checks every requirement the user typed against the code (the 需求对照 / Your asks tab), and turns *what was asked, claimed and put off* about safety into a ledger of promises checked against the code. **Every conclusion carries evidence a script verifies. Anything that fails verification shows as ❓ or "unverified" — it is never shown as fact.**

## Rules

1. **Never invent evidence.** Copy quotes character for character from a reading pack, and code snippets from the file. `check` rejects anything else, and the report shows the rejection.
2. **The ledger takes only the five questions** (references/five-questions.md): where data lives, what costs money, who can see it, where it is most likely to break, what was put off. Leave cosmetic and feature requests out of the ledger — they belong in `requirements.json`, which takes every request about the project.
3. **A status other than `unknown` needs code or probe evidence.** When unsure, write `unknown`.
4. **Two voices.** Plain text is for someone who cannot read code (an analogy only if it is accurate); dev text names the file and the mechanism. Write both in the run's language (`lang` in `run.json`).
5. **Explanations name only what exists.** Function names are copied from their definitions; a name goes in backticks only if it is in the project. Describe what a file does, not what it should do.
6. **Ask before `retention --set`.** It edits the user's Claude Code settings.
7. **Transcripts are private.** Quote only what a promise or a file's history needs. The digest is already masked; never unmask or repeat a secret.

## Steps

Run everything as `python3 <this skill's folder>/scripts/vl.py …`. Each step prints the exact next command — run it as printed.

1. **Start** — `vl.py start --project <app folder>`. It finds the conversations, writes reading packs, runs the probes, builds the file graph and writes `explain_pack.md`. Read its summary: conversations, candidates, probes, file graph, files to explain, warnings. If it prints a retention line, ask the user (rule 6).
2. **Ledger** — follow references/extraction-guide.md.
   - One reading pack: read it, `probes.json`, `candidates.json` and the code it points at; write `<run>/ledger.json`, including `map`, `access` and `paths`.
   - Several packs: give each pack to its own subagent (or work through them one by one) → `<run>/parts/part_NN.json` with evidence, promises and compromises only.
3. **Requirements** — follow references/requirements-guide.md. Skip it when `start` says there are no user messages.
   - One request pack: read `requests_01.md` and the code each request is about; write `<run>/requirements.json`. Account for every message: a requirement's source, or `skipped`.
   - Several packs: give each `requests_NN.md` to its own subagent → `<run>/parts/req_NN.json`.
4. **Explanations** — follow references/explain-guide.md.
   - One group (8 files or fewer): read `explain_pack.md` and every file it lists; write `<run>/explain.json`, including 2–4 `journeys` — what the user does and the files it passes through, in order — and the function map: `areas` (the project's 2–10 parts), `items` and `flows` (what data each part reads and writes, one code line each; guide section 4).
   - Several groups: give each group to its own subagent → `<run>/parts/explain_NN.json`.
5. **Merge** (only if step 2, 3 or 4 wrote parts) — `vl.py merge --project <app folder>`. It merges all three kinds of part. Then add `map`, `access` and `paths` to `<run>/ledger.json`, and the `journeys`, `areas`, `items` and `flows` to `<run>/explain.json`, yourself.
6. **Check** — `vl.py check --project <app folder>`. It verifies `ledger.json`, `explain.json` and `requirements.json`; it stops if one is missing or malformed. It lists user messages you left unaccounted — add them as requirements or `skipped`. Fix a failed quote, snippet or function line only by copying the real text. Downgrades to ❓, dropped function names and "unverified" purposes are the honest result, not something to work around.
7. **Render** — `vl.py render --project <app folder>`. It compares with the previous finished run of this project by itself and prints what changed (`--compare <run folder>` picks another run, `--no-compare` skips it).
8. **Look** — `vl.py shot --project <app folder>`. It must print `Layout check: … none overlap`. Then open every screenshot: the flowchart reads left to right with no overlapping cards; the selected file's panel explains it; the overview diagrams say what the ledger says; the requirements tab groups the asks by area with the counts check printed; at phone width the panel's text stays inside the screen. (On a phone the flowchart itself is wider than the screen on purpose — it keeps cards readable and pans with a finger — so a graph cut at the right edge is expected.) Fix and re-render if not. If no browser is available, open the HTML and read it.
9. **Tell the user**, in the language they wrote to you in (the run's `lang`) — the report path; how to read it (start on the flowchart, open a route under “点一下会发生什么” — “What happens when you…” on English pages, click a file, red cards have problems; the flowchart opens on the 功能图 — the project's parts, each opening into its files — and 数据流 shows what each part reads and writes; a route's 时序图 gives the order of calls; “对比上次” shows what changed; “导出” saves a PNG or SVG; the 需求对照 / Your asks tab checks each thing they asked for); if render printed a comparison, say what changed since last time; the counts (✅ ❌ ⚠️ ⏳ ❓) and the requirement counts (✅ ⚠️ ❌ 🔀 ↩️ ❓); the three most important problems (requirements not done or done differently come first) in plain words, each with the fix it suggests; and what the report could not see (the overview's last section).

## When there are no conversations

`start` says so. Leave `promises` empty, still record `map`, `access` and `paths` from the code, write `explain.json` without `history`, skip `requirements.json`, and tell the user the report checked the code only.

## Reference

- references/extraction-guide.md — how to write the ledger, with a worked example
- references/explain-guide.md — how to write the file explanations, with a worked example
- references/requirements-guide.md — how to write requirements.json, with a worked example
- references/ledger-schema.md — every ledger field
- references/five-questions.md — what belongs under each question
- references/probes.md — what each probe checks and where it is blind
- references/candidates.md — how candidates are found
