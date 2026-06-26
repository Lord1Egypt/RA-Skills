---
name: values-elicit
description: Run a Moral Graph Elicitation interview when the user expresses a strong feeling, a goal, a norm, or a difficult choice in a way that suggests an underlying source of meaning worth capturing. Produces a values card stored in the configured values store. Also runnable as the /values slash command.
user-invocable: true
metadata: {"openclaw": {"emoji": "🪺", "requires": {"bins": ["node"]}}}
---

# Values Elicitation

Help the user articulate a "source of meaning" — a way of living they find
intrinsically meaningful — and write it as a values card in their values
store.

## When to run

Run when:
- The user invokes the skill.
- The user shares a story, strong feeling, role model, difficult choice,
  norm, something they want more of in their life, or a topic they have
  strong feelings about — AND signals openness to going deeper. When in
  doubt, ask once.

Don't run when:
- The user is in flow on another task.

## How to run

The interview has four stages. Read `references/conversation.md` for the
flow, brevity rules, and how to handle goals/feelings/norms.

1. **Surface** the source of meaning (1-3 exchanges).
2. **Draft and refine** 3-6 attention policies.
3. **Ask once** what gets in the way of living this.
4. **Write** the card. Don't ask for confirmation on title or
   situations — generate them, save, and tell the user where the file
   is and that they can edit it.

Read `references/cards.md` before drafting policies or writing the card.
It covers what a source of meaning is, how to write attention policies,
and the exact card format.

## Setup

Values store path:
- Preferred: `$AGENT_VALUES_DIR`
- Fallback: `~/.openclaw/values`

Silently ensure these exist on every run (no chatter):
- `$AGENT_VALUES_DIR/` (or `~/.openclaw/values/`)
- `cards/`
- `transcripts/`
- `VALUES.md` (create an empty file if missing)
- `build.mjs` (copy from `scripts/build-values.mjs` if missing)

**First run only.** Detect first run by whether `VALUES.md` existed before
this turn. If it did not, after the silent bootstrap:

1. Tell the user in **one line** where the values store landed (e.g.
   "Set up your values store at `~/.openclaw/values/`.").
2. Check for `USER.md` at `$OPENCLAW_USER_MD_PATH`, then
   `~/.openclaw/workspace/USER.md`, then `~/.openclaw/USER.md`. If one
   exists and doesn't already mention `VALUES.md`, ask **once** whether
   to append the contents of `references/USER_MD_SNIPPET.md` so other
   agents will consult their values. Append if they say yes; otherwise
   move on. If no `USER.md` is found, mention briefly that they may
   want to add the snippet to their user profile later.
3. Proceed straight into the elicitation. Do not repeat any of this on
   subsequent runs.

## Output

After Stage 3 (the blocker question), without asking for confirmation:

1. **Pick a slug.** Kebab-cased title. "Tending the Quiet" → `tending-the-quiet`.
2. **Write the card** to `cards/<slug>.md` using the format in `references/cards.md`.
3. **Write the transcript** to `transcripts/<YYYY-MM-DD>-<slug>.md` — plain
   markdown dump with `**Me:**` / `**Agent:**` turn markers.
4. **Rebuild VALUES.md** by running `node "$AGENT_VALUES_DIR/build.mjs"`
   (or `node ~/.openclaw/values/build.mjs` if unset). The Setup step
   already ensures the helper exists.
5. **Tell the user** the file path and that they can edit it if anything
   needs changing.

## What the user sees vs. what goes in the file

Don't show the explication ("What this is" prose) in chat — write it
directly into the card. The user can read it there if they want to.
Don't re-render the whole card after small refinements — show only what
changed. See `references/conversation.md` for brevity rules.
