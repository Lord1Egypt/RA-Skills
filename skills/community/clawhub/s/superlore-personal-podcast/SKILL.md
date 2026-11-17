---
name: "superlore-personal-podcast"
description: "Pair OpenClaw with Superlore to create or upload private podcast episodes and use saved Sources."
homepage: https://superlore.ai/integrations/openclaw
---

# Superlore personal podcast

Use Superlore as the private audio output for agent work.

## Pair once

1. Ask the user to open https://superlore.ai/agents and create a six-digit pairing code.
2. Request the minimum scopes:
   - `episodes:create` for prompt-to-episode generation.
   - Add `sources:read` only when the user wants saved Superlore Sources.
   - Add `episodes:upload` only when uploading finished audio.
3. Run the bundled helper from this skill directory:

```bash
node scripts/superlore.mjs pair --code 123456 --scopes episodes:create,sources:read
```

4. Tell the user the agent has claimed the code and is waiting for approval. The helper polls for approval, stores the one-time credential privately, acknowledges delivery, and performs a side-effect-free connection test.
5. If pairing expires or returns 401, ask for a new code. Never ask the user to paste a raw `slc_` credential.

## Create an episode

Read available feeds and Sources when context matters:

```bash
node scripts/superlore.mjs context
```

Create from a prompt. Add repeated `--source` flags only for Sources the user chose or clearly placed in scope.

```bash
node scripts/superlore.mjs create \
  --prompt "Make a five-minute briefing on today's decisions and tomorrow's priorities." \
  --minutes 5
```

The helper waits for a terminal generation state by default and prints the private listen URL. Use `--no-wait` for detached workflows, then:

```bash
node scripts/superlore.mjs status --generation gen_...
```

For an existing audio file and an explicitly selected feed:

```bash
node scripts/superlore.mjs upload \
  --feed feed_... \
  --audio /absolute/path/briefing.mp3 \
  --title "Daily agent briefing"
```

## Recurring use

When the user explicitly asks for a schedule, use OpenClaw cron to run the same create command at the requested local time. Keep the cron prompt focused on the current briefing window and use Superlore Sources only when granted.

Do not create a test episode during setup. The `test` command verifies credentials without publishing:

```bash
node scripts/superlore.mjs test
```

## Safety

- Never print, paste into chat, or write the agent credential to memory files.
- The helper prefers `SUPERLORE_AGENT_TOKEN`; otherwise it stores the token at `~/.config/superlore/agent.json` with mode `0600`.
- Do not read Sources without the `sources:read` scope.
- Do not upload audio unless the user supplied or authorized the file.
- Reconnect instead of retrying indefinitely after authorization failure.
- Treat returned listen URLs as private.
