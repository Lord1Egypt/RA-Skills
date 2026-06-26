---
name: webup-buddy-reroll
description: Reroll Claude Code /buddy companion to a target species and rarity, or rename/customize companion name and personality. Triggers on "reroll buddy", "change buddy", "legendary buddy", "new companion", "buddy hack", "rename buddy", "buddy name", "buddy personality", "换宠物", "重新抽", "传说宠物", "改名", "宠物名字", "バディ変更", "伝説バディ", "バディ名前", or similar.
---

# Buddy Reroll

Brute-force a new `/buddy` companion by finding a userID that hashes to the desired species and rarity.

## How It Works

Claude Code generates companions deterministically: `hash(userID + SALT)` → `mulberry32` PRNG → rarity, species, eyes, hat, shiny. Same userID = same companion, always.

To reroll: replace `userID` in `~/.claude.json`, clear `companion` field, restart.

**Critical**: Claude Code is Bun-bundled, so `Bun.hash()` (xxHash64) is the correct hash function. Node.js FNV-1a produces wrong results — the script MUST run under Bun.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.mjs`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/reroll.mjs` | Brute-force target species+rarity, optionally apply to config |
| `scripts/oauth-setup.mjs` | OAuth config helper for Pro/Max subscribers (--check/--prepare/--verify/--restore) |
| `scripts/rename.mjs` | Change companion name and/or personality (--name/--desc) |

## Prerequisites

- **Claude Code >= 2.1.89** — the `/buddy` system was introduced in this version. The script auto-checks and exits if the version is too old.
- **Bun** — required for correct hashing. Use `npx -y bun` if not installed globally.
- **API users**: Works directly — `userID` in `~/.claude.json` can be freely replaced.
- **Pro/Max subscribers**: Requires OAuth setup first (automated by this skill). Pro/Max accounts have `accountUuid` which `/buddy` uses instead of `userID`. The OAuth method bypasses this — see workflow below.

## Usage

```bash
# Direct (if bun is installed globally)
bun ${SKILL_DIR}/scripts/reroll.mjs --species dragon --rarity legendary --apply

# Via npx (works even without global bun install)
npx -y bun ${SKILL_DIR}/scripts/reroll.mjs --species dragon --rarity legendary --apply
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--species <name>` | `dragon` | Target species (see list below) |
| `--rarity <level>` | `legendary` | Minimum rarity: common / uncommon / rare / epic / legendary |
| `--max <n>` | `1000000` | Max brute-force iterations |
| `--apply` | off | Auto-write result to `~/.claude.json` and clear companion |

### Species (18)

| | | | | | |
|---|---|---|---|---|---|
| duck | goose | blob | cat | dragon | octopus |
| owl | penguin | turtle | snail | ghost | axolotl |
| capybara | cactus | robot | rabbit | mushroom | chonk |

### Rarity Tiers

| Rarity | Stars | Chance | ~Iterations to find |
|--------|-------|--------|---------------------|
| common | ★ | 60% | ~30 |
| uncommon | ★★ | 25% | ~72 |
| rare | ★★★ | 10% | ~180 |
| epic | ★★★★ | 4% | ~450 |
| legendary | ★★★★★ | 1% | ~1800 |

## Invocation

This skill can be invoked with or without arguments:

- **No args** (`/webup-buddy-reroll`): Prompts the user interactively via `AskUserQuestion` before running.
- **Reroll only** (`/webup-buddy-reroll dragon legendary`): Skips the prompt and locks to the given species and rarity.
- **Reroll + rename** (`/webup-buddy-reroll dragon legendary 沧海九粟 爱打盹的小龙`): Reroll, then immediately apply the given name and personality.
- **Rename only** (`/webup-buddy-reroll 改名叫沧海九粟，个性是爱打盹的小龙`): Skip reroll, only change name and/or personality.

### Arg parsing (natural language)

The args string is free-form text. Use NLP to extract these fields:

1. **species** — match against the 18 known species names (duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk). Also recognize Chinese/Japanese equivalents (龙=dragon, 猫=cat, etc.).
2. **rarity** — match against the 5 tiers (common, uncommon, rare, epic, legendary) or equivalents (传说=legendary, 史诗=epic, etc.).
3. **name** — a short proper name for the companion (e.g. "沧海九粟", "Nimbus", "小火"). Look for patterns like "叫X", "名字X", "named X", "name X", or a standalone proper noun that isn't a species/rarity keyword.
4. **personality** — a description of the companion's vibe or character (e.g. "爱打盹的小龙", "sarcastic robot"). Look for patterns like "个性X", "性格X", "personality X", or descriptive phrases that aren't species/rarity/name.

All four fields are optional. Any combination is valid.

**Detect intent**:
- If species or rarity found → **Reroll Workflow** (+ post-reroll rename if name/personality also found)
- If only name and/or personality found (no species/rarity) → **Rename Workflow**
- If no args at all → prompt interactively, detect from user's message whether they want reroll or rename

## Reroll Workflow

0. **Detect account type**: Run the check script to see if `accountUuid` exists in `~/.claude.json`:
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/oauth-setup.mjs --check
   ```
   - **Exit 0** (no `accountUuid`): API user or OAuth already set up. Skip to step 1.
   - **Exit 1** (`accountUuid` found): Pro/Max subscriber. Run **OAuth Setup** below, then continue to step 1.

### OAuth Setup (Pro/Max only)

**Principle**: When logging in via `CLAUDE_CODE_OAUTH_TOKEN` env var, Claude Code does NOT write `accountUuid` to `~/.claude.json`. This makes `/buddy` fall back to `userID`, which can be freely replaced.

   a. Tell user to open a **separate terminal** and run `claude setup-token` to get their OAuth token. Ask them to paste the token back here.

   b. Once token is received, prepare the config (backup + reset):
      ```bash
      npx -y bun ${SKILL_DIR}/scripts/oauth-setup.mjs --prepare
      ```

   c. Tell user to run in a **separate terminal** (replace `<TOKEN>` with actual token):
      ```bash
      CLAUDE_CODE_OAUTH_TOKEN=<TOKEN> claude
      ```
      Wait for Claude to fully load, then **exit immediately** — do NOT use `/buddy`.

   d. After user confirms they've done this, verify the config:
      ```bash
      npx -y bun ${SKILL_DIR}/scripts/oauth-setup.mjs --verify
      ```
      If verification fails, run `--restore` to restore backup and retry from step (a).

   e. Continue to step 1.

---

1. **If no args provided**: Use `AskUserQuestion` to ask the user to pick a species AND a rarity in a single prompt (two questions):
   - **Species question**: Present 4 popular options (dragon, cat, axolotl, capybara) as choices. Each option's `description` should list the remaining species so the user knows what's available via "Other", e.g. the first option's description: "Or type any of: duck, goose, blob, octopus, owl, penguin, turtle, snail, ghost, cactus, robot, rabbit, mushroom, chonk".
   - **Rarity question**: Present all 5 tiers (legendary as first/recommended, then epic, rare, uncommon, common).
   - Do NOT skip this step. Always ask even if the user mentioned a species — confirm their choice.

   **If species/rarity parsed from args**: Skip the prompt and proceed directly.
2. Run the script with `--apply`:
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/reroll.mjs --species <choice> --rarity <choice> --apply
   ```
3. **If name or personality was parsed from args**: Run the rename script immediately after reroll (no restart needed between):
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/rename.mjs --name "<parsed name>" --desc "<parsed personality>"
   ```
   Omit `--name` or `--desc` if only one was parsed.
4. Tell user to restart Claude Code and run `/buddy` to hatch the new companion.
   - **If OAuth was used**: Remind user to start Claude with `CLAUDE_CODE_OAUTH_TOKEN=<TOKEN> claude` (not plain `claude`) to prevent `accountUuid` from being written back.

## Manual Apply

If `--apply` was not used:
1. Copy the output userID
2. Edit `~/.claude.json`: replace `"userID"` value, set `"companion": null`
3. Restart Claude Code → `/buddy`

## Rename / Customize Companion

Change the companion's name and/or personality description without rerolling species or rarity.

### Rename Workflow

**If name and/or personality were parsed from args**: Skip steps 1–3, go directly to step 4 with the parsed values. When personality is provided directly via args, use it as-is — skip the AI generation step.

1. Use `AskUserQuestion` to ask what the user wants to change (one question, multiSelect):
   - **Name**: "Change companion name"
   - **Personality**: "Change companion personality/description"
2. For **name**: ask the user for the exact name. Pass it directly.
3. For **personality**: ask the user for a brief tip or vibe (e.g. "lazy cat that loves keyboards", "sarcastic robot"). Then **you** (Claude Code) generate a fun, creative personality description (1–2 sentences, matching the companion's species and the user's tip). Show the generated text to the user for confirmation before applying.
4. Run the rename script:
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/rename.mjs --name "<name>" --desc "<personality>"
   ```
   Omit `--name` or `--desc` if only one is being changed.
5. Tell user to restart Claude Code for changes to take effect.

## Notes

- `userID` only affects telemetry bucketing and buddy seed — no impact on conversations, API keys, or local config
- SALT is `friend-2026-401` (Claude Code 2.1.89). Update the script if a future version changes it
- 1M iterations finds legendary in seconds on modern hardware
