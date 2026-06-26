# Architecture: Why Random Thought Works This Way

## The Two-Stage Pipeline

Random Thought uses two stages — **Writer** and **Curator** — instead of one combined job or three separate jobs. Here's why.

### Why not one job?
A single "reflect and curate" job runs in one session context. The Writer's prose, the file contents, and the curation logic all compete for the same context window. On a rich workspace, this hits limits fast. Worse: the curation step is anchored by what the Writer just wrote in the same session, instead of forming an independent judgment across many observations.

### Why not three jobs?
An earlier version included an Observer (annotated each Writer post for actionability). In practice, this was redundant — the Curator performs the same triage, but better, because it has the full day's context rather than a single post. The Observer burned tokens for metadata that the Curator re-evaluated anyway.

### Why cron-driven?
Each cron invocation gets an isolated session — no context bleed between runs. The Writer at 2 PM has zero memory of the Writer at 1 PM. This is a feature: each observation is independent, which gives the Curator genuinely diverse inputs to synthesize.

A skill invocation within a session would carry prior context, defeating this isolation. The hybrid model (crons invoke the skill's stages) gives both distributable logic and session isolation.

## The Freshness Gate

Without a freshness gate, the Writer revisits the same files within days. On a workspace of ~3,000 files with hourly runs, you'd see repeats within a week. The 7-day default cooldown means each file gets at most ~4 visits per month, keeping observations varied.

The history file is a simple TSV (timestamp + path). The `prune` command keeps it from growing indefinitely.

## Action Tags

The Curator classifies every observation using configurable tags. The defaults:

- **you-decide** — needs human judgment (a decision, trade-off, or prioritization)
- **agent-execute** — the agent can act on this autonomously
- **spark** — interesting but no action needed; let it breathe

Users can override these to match their workflow. A development team might use `file-issue`, `tech-debt`, `team-discuss`. A solo developer might simplify to just `act` and `note`.

The key design choice: tags are *output classification*, not *input filtering*. The Writer observes freely. The Curator applies structure after the fact.

## Cost Profile

| Component | Model | Frequency | Est. daily cost |
|-----------|-------|-----------|-----------------|
| Writer | haiku-class | 24×/day | ~$0.07 |
| Curator | sonnet-class | 1×/day | ~$0.07 |
| **Total** | | | **~$0.14/day** |

The system is designed to run on cheap models. The Writer works well with haiku-class models because it's doing creative prose, not complex reasoning. The Curator benefits from a stronger model (sonnet-class) because it's synthesizing across many observations and making classification judgments.

## What This System Is Not

- **Not a code reviewer.** It doesn't find bugs. It notices patterns.
- **Not a task manager.** It doesn't create tickets. It surfaces what might deserve one.
- **Not a summarizer.** It doesn't compress files into briefs. It writes about what strikes it as alive.

The value is in the process of reflection, compounded over time. Individual observations are sparks. The Curator's digest is where patterns emerge.
