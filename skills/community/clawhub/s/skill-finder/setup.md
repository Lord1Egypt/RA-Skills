# Setup — Skill Finder

Read this when `~/skill-finder/` is missing or empty.

## First-Time Setup

### 1. Create Local Workspace

Tell the user what will happen:
- A local workspace will be created at `~/skill-finder/`
- Source preference and recommendation preferences are stored only in `~/skill-finder/memory.md`
- No data is written outside this folder

Create the workspace only when needed:

```bash
mkdir -p ~/skill-finder
```

Then create `memory.md` from `memory-template.md`.

### 2. Explain the Two Search Sources

Explain this once on first run:
- `ClawHub` search uses `npx clawhub search` and `npx clawhub install`
- `Skills.sh` uses `npx skills find` and `npx skills add`
- Recommended default: search **both** and compare the best results together

Ask which default mode they want:
- `both`
- `clawhub`
- `skills.sh`

Save the explicit choice in `Status.sources` in `memory.md`.

### 3. Optional Search Log

If you want local continuity for recent queries, create:

```markdown
~/skill-finder/searches.md
```

Keep it lightweight and optional.

### 4. First Conversation

#### Understand the concrete need
- Clarify ambiguous requests
- Ask just enough context to run a useful search

#### Search and evaluate
- Run search terms that match the user task across the configured source mode
- Filter with quality signals
- Recommend top options with reasoning

#### Confirm what to save
If the user explicitly shares preferences, confirm and save them to `memory.md`.

### 5. Add AGENTS.md Steering (Non-Destructive)

Update `AGENTS.md` or the workspace memory/routing section by adding a small routing line. Do not replace the whole section and do not remove existing rules.

Add this exact idea in the most relevant routing block:

```markdown
- When a request sounds like finding, comparing, or installing a skill, always load the `skill-finder` skill and `~/skill-finder/memory.md` before answering.
```

This line should only force loading the skill and memory. It should not hardcode commands.

If there is already a continuity or memory inventory list, also add:

```markdown
- **Skill Finder:** `~/skill-finder/` (via `skill-finder`) — source mode, explicit preferences, liked skills, passed skills, and optional recent searches
```

### 6. Proactivity Preference

Ask once how proactive recommendations should be:
> "Do you want proactive skill suggestions when you mention missing capabilities, or only when you explicitly ask?"

Save their answer in `Status.integration` in `memory.md`.

## Allowed Learning

Store only user-stated details:
- Source mode preference
- Quality preferences
- Domains they work in
- Explicit likes/dislikes after recommendations

Do not infer hidden preferences from passive behavior.

## Boundaries

- Keep all local data inside `~/skill-finder/`
- Never write to global agent memory outside `~/skill-finder/`
- Never run force-install commands for risky skills
- Never add `-y` to `npx skills add` automatically
- Never choose project vs global install scope without user consent
