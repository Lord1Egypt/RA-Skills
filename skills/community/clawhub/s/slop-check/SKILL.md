---
name: slop-check
description: Grade how vibe-coded a codebase is. Produces a Slop Percentage (0-100% AI slop), a tier ranking from Senior Engineer down to "GPT-3.5, Unsupervised", and an HTML report card served at a local URL with specific file:line findings and copy-paste fix-it prompts. Use whenever the user wants to slop-check or grade a repo, asks how vibe-coded / AI-generated / sloppy / well-architected a codebase is, wants a code quality score, roast, audit, or report card, or mentions AI slop, vibe coding, or code smells — even if they don't name the skill.
---

# slop-check

Grade a codebase's slop level. Fun on the surface, real code review underneath: every point
of slop must cite a real file and line. The roast is the headline; the receipts are the product.

This skill is agent-agnostic — nothing in it depends on a specific coding agent. The only
requirement is Node 18+ on the machine.

## Process

### 1. Resolve the target

The target repo is the argument if given, otherwise the current working directory.
If the target has fewer than 5 code files, tell the user there isn't enough to grade and stop.

**Always double-quote every path in the shell commands below.** Project paths often contain
spaces (e.g. `~/Documents/My Project/`), and an unquoted path silently writes the report to
the wrong place. Write `"$ROOT/.slop-check/metrics.json"`, never
`$ROOT/.slop-check/metrics.json`. The scripts themselves handle spaces fine; the only risk
is an unquoted path in the command you run.

If a file you just wrote then "isn't there," do NOT conclude that a watcher, dev server, or
cleanup hook is deleting it, and do not alarm the user with that theory — this skill never
deletes anything, and that misdiagnosis has happened before. The real cause is almost always
an unquoted path that wrote the file somewhere other than where you looked. Re-run the
command with the path fully quoted and `ls` the exact quoted path before assuming anything
external is at fault.

### 2. Run the deterministic scanner

```bash
node <this-skill's-directory>/scripts/slop-scan.mjs <target-root> --out <target-root>/.slop-check/metrics.json
```

This is dependency-free (Node 18+, no installs). It produces `metrics.json` containing:

- File inventory, language breakdown, line counts
- Import graph metrics: circular dependencies, god files, possibly-dead orphan files
- Cross-file duplication estimate (hashed line windows)
- AI-tell counts from regex (narrating comments, "in a real app", placeholder TODOs, leftover debug logging, commented-out code)
- Utils-folder sprawl, giant files
- **Pre-computed subscores** for the four script-owned categories (Coupling, Duplication, Dead Weight, AI Tells)
- `sampleSuggestions`: the files most worth reading by hand in step 3

The scanner also writes `.slop-check/slop-map.json` — the full per-file import graph
(every file's `importedBy` / `imports` lists plus flags). Do NOT read it whole (it can be
large); it exists so step 5's fix-it prompts and any future fixing agent can pull exact
context without re-exploring the repo. Pull individual entries from it when you need a
specific file's blast radius.

Read the whole `metrics.json` before continuing. Treat orphan files as *suspects*, not
convictions — dynamic loading, workers, and cross-package imports can hide real users.
If `truncated` is true (the repo exceeded the 50,000-code-file walk cap), say so in the
verdict — never let a partial scan read as full coverage.

Each run is self-contained — a fresh snapshot of the code as it is right now. If a
previous run left anything in `.slop-check/` (or an old `slop-report.html`), ignore its
contents entirely and overwrite it. Do not read old reports, compare against them, or
carry findings forward; code changes too much between runs for that to mean anything.
The grade reflects the current state, nothing else.

### 3. The taste pass (judgment)

The files in `sampleSuggestions` (plus any the metrics make you suspicious about) get
judged against `references/HEURISTICS.md` — read it now if you haven't. The categories
being scored here:

- **Architecture & Modularity** — deletion test, shallow modules, pass-through layers, horizontal slicing, layering violations
- **Naming & Domain Language** — generic names, no consistent domain vocabulary
- **Consistency** — mixed paradigms, styles, and conventions that show nobody was steering

Scale the effort to the repo — a slop-check takes minutes, not hours:

- **Small repo (under ~40 code files):** read the sample yourself. No subagents.
- **Bigger repo, and your environment supports parallel subagents:** spawn reviewers in
  **one parallel batch — at most 6, with no second wave.** There are three lenses; start
  with one reviewer per lens, and when a lens's file list exceeds ~40 files, split that
  list across two reviewers with the same lens (this is how you reach 4-6 — more files
  per reviewer just means skimming, which is worse than sampling):
  1. *Architecture* — the god files, largest files, and most-imported files; hunts
     shallow modules, pass-through layers, layering violations.
  2. *Naming & consistency* — the spread sample (files from different corners of the
     repo); hunts generic naming, vocabulary drift, mixed conventions.
  3. *AI tells & local quality* — the highest-tell files; confirms or refutes the
     regex counts and hunts the tells regexes can't catch.

  Tell each reviewer to read `references/HEURISTICS.md`, read only its assigned files,
  and return JSON with two things: `findings` (`{category, file, line, severity,
  description}` with the severity scale below) and `observations` — one line per file
  read (`{file, observation}`) capturing what the file *is* and how it relates to its
  neighbors, even when there's nothing wrong with it. The observations are not for
  scoring; they're the knowledge that makes step 5's fix-it prompts context-rich, so the
  tokens spent reading don't evaporate. Then merge everything yourself, dedupe anything
  two reviewers both caught, and own the final category scores — reviewers report,
  you grade.
- **No subagent support:** do the three lenses yourself, sequentially, over the same sample.

If you ever feel the urge to spawn a seventh agent or a second wave, stop — you are
rebuilding the hours-long pipeline this skill exists to be the cheap alternative to.

You may also adjust the script's AI Tells subscore by up to ±15 points based on what was
actually read (regexes can't catch tone; readers can).

Every finding kept must have: category, `file:line`, a one-line description, and a
severity (minor 1-3 pts / moderate 4-7 pts / major 8-12 pts within its category).
No vibes-only deductions — if you can't cite a line, it isn't a finding.

### 3.5 Verify the receipts

Before scoring, re-open the cited location of every **major** finding (and anything
secondhand from a reviewer that sounds too good to roast with) and confirm the code
actually shows what the description claims. A wrong receipt is the one unforgivable
failure in a report that roasts people's code — drop or downgrade anything that doesn't
hold up exactly as described.

### 4. Compute the Slop Percentage

Follow `references/SCORING.md` exactly: seven weighted categories combine into one Slop
Percentage, which maps to a tier. Higher % = more slop = lower tier.

### 5. Generate the report and serve it

You never read or write HTML — a script does the injection, so the only thing you author
is a small JSON payload:

1. Write the payload to `<target-root>/.slop-check/report-data.json`, following
   `references/REPORT-SCHEMA.md` (read it now).
2. Build the report (this validates the payload and fails loudly if something's missing):

```bash
node <this-skill's-directory>/scripts/build-report.mjs \
  --data <target-root>/.slop-check/report-data.json \
  --out <target-root>/slop-report.html
```

   `build-report.mjs` prints `verified the live report renders this payload` on success.
   If it instead prints a validation or verification error, fix what it names and rerun —
   do **not** serve an unverified file. (A serve of the raw template renders only blank
   defaults; the build step is what makes the report real.)

3. Serve it at a local URL (run in the background so you can keep working):

```bash
node <this-skill's-directory>/scripts/serve-report.mjs <target-root>/slop-report.html
```

   Before handing over the URL, sanity-check that the served page carries the real data,
   not template defaults: `curl -s <url> | grep -c '"name": "example-project"'` must
   print `0`. If it prints `1`, the build didn't land — stop and fix it, don't give the
   user a blank report.

It prints `Slop report live at: http://localhost:<port>` — give the user that URL.
If running a server isn't possible in the environment, fall back to opening the file
directly (`open` / `xdg-open`) or just tell the user the file path; the report is fully
self-contained either way.

The report includes **Fix-It Prompts**: for each of the top 3-6 findings, write a
ready-to-paste prompt the user can give to any coding agent to fix that exact issue.
These prompts are the genuinely-useful payoff; don't phone them in. Each prompt has
three parts:

1. **The task** — the files, the problem, the desired end state, and how to verify
   nothing broke.
2. **Pre-paid context** — a short "Context from the slop-check map:" block embedding
   what this run already learned, so the fixing agent starts warm instead of re-exploring:
   the target file's `importedBy` list from `slop-map.json` (the blast radius), what it
   imports, relevant reviewer observations about it and its neighbors, and any related
   findings. This is the whole point — the tokens were spent during the check, so the
   fix prompt should hand the knowledge over rather than make the next agent buy it again.
3. **The map pointer** — end with: "A machine-readable import map of this repo is at
   `.slop-check/slop-map.json` — check a file's `importedBy` entry before moving or
   renaming anything."

### 6. Deliver the verdict in the chat

End with a short verdict, in this shape:

```
🍝 Slop Check: 61% slop — "Somehow, It Works"
Scanned: <N> files · <N> lines · <cycles> cycles · <dup>% duplication · <tells> AI tells
Worst offenders: <top 3 findings, one line each, with file:line>
Most valuable fix: <the single highest-impact action, in plain terms>
Report: http://localhost:<port>  (also saved to slop-report.html)
```

## Tone rules

- Straight-talking, deadpan, funny in the verdict copy — never mean about the *person*, only the code.
- Brutal honesty cuts both ways: if the codebase is genuinely good, say so plainly and grade it high. A rigged roast is worthless.
- Small hand-written hobby projects get judged on the same scale — but say what the scale is measuring so a 200-line script isn't confused about why "no layers" cost it nothing.

## Bundled resources

- `references/HEURISTICS.md` — the smell catalog for the taste pass (read during step 3)
- `references/SCORING.md` — category weights, formulas, tier bands, easter egg rule (read during step 4)
- `references/REPORT-SCHEMA.md` — the report payload format (read during step 5)
- `scripts/slop-scan.mjs` — deterministic metrics scanner (execute, don't read)
- `scripts/build-report.mjs` — injects your payload into the template (execute, don't read)
- `scripts/serve-report.mjs` — single-file report server (execute, don't read)
- `assets/report-template.html` — the report card template (never read this; build-report.mjs handles it)
