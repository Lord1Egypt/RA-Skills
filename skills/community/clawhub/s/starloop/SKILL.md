# Starloop Skill

Read a StarFocus todo folder and produce a ranked recommendation for the next task to work on.

## Arguments

- `$ARGUMENTS[0]` — path to the todos folder (e.g. `/mnt/d/Philomath/todos`)
- `$ARGUMENTS[1]` — comma-separated star roles to filter by (e.g. `Starfocuser,Autism helper`). If omitted or empty, include todos with any star role.

## Steps

### 1. Read the todo folder

Read all `.md` files in `$ARGUMENTS[0]`. Skip:
- `_manifest.md`
- `_asteroid-field.md`
- `_wayfinder.md`
- Any file with `completedAt` set in its frontmatter

If `$ARGUMENTS[1]` was provided, filter to todos where `starRole` matches any value in the comma-separated list. If omitted or empty, include all todos regardless of star role.

### 2. Read context files

- `_wayfinder.md` — strategic priority order
- `_asteroid-field.md` — urgent/time-sensitive items

### 3. Rank and evaluate todos

Sort all todos by:
1. Position in `_wayfinder.md` (higher = more important)
2. `starPoints` value
3. Presence in `_asteroid-field.md` (urgency boost)

Then walk down the ranked list. For each todo, read its full content and assess tractability: can Claude Code make concrete progress on this right now using the tools listed in `TOOLS.md`? If yes, add it to the candidates list. If no, it is blocked — note what capability is missing and continue down the list.

Stop once you have 3 candidates, or have exhausted the list.

### 3.5. Search ClawHub for blocked high-priority todos

For any todo that was blocked due to missing capability AND ranked highly enough that it would otherwise have been a top candidate, run:

```
bunx clawhub search <missing-capability>
```

Note the top result slug and summary for inclusion in the output. Only do this for genuinely high-priority items that had to be passed over — not for every blocked todo.

### 4. Output a recommendation message

Format using Telegram markdown. Example:

```
StarLoop 🔄 Top pick: **[title]**

**Why now:** [2–3 sentences: its position in the wayfinder, why it ranks above the alternatives, any momentum or dependency factors that make this the right moment]

Other options:
1️⃣ **[title]** — [one-line reason]
2️⃣ **[title]** — [one-line reason]

Reply **go** for the top pick, **1** or **2** for an alternative, or name a different task.
```

If any high-priority todos were blocked, append:

```
⚠️ Couldn't recommend:
• **[title]** — blocked: [missing capability]. Possible fix: `openclaw skills install [slug]` — [one-line summary]
```

Return the message text and the filename for each option so the caller knows which file to pass to Claude Code.

## Important: filenames contain a unique ID suffix

Todo filenames follow the pattern `[title]_[id].md` where `[id]` is a short unique identifier (e.g. `star-role-descriptions_dfif0com.md`). The ID suffix is not decorative — it is the primary key that links the file to the database record and to the ACP session. It must never be omitted or shortened. Always reference todos by their full filename including the ID suffix.
