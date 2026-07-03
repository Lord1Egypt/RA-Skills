# Unified Digest

This skill adds a shared subscription layer in front of:

- `follow-builders`
- `med-builders`

It is meant to be used as the agent's startup router. On the first user turn of a session, the agent checks shared subscription state and decides whether to ask:

```text
I can subscribe you to:
1. AI builders / researcher updates
2. Pharma investment / BD intelligence
```

The shared state is stored in `~/.unified-digest/subscriptions.json`.

## What This Solves

- One startup prompt instead of two separate onboarding flows
- Shared "don't ask again" and "ask me later" behavior
- Shared defaults for delivery cadence, language, and timezone
- Clean coexistence between `follow-builders` and `med-builders`

## Files

- `SKILL.md`: agent workflow
- `config/subscription-schema.json`: state schema
- `scripts/subscription-state.js`: deterministic state helper
- `scripts/state-lib.js`: shared state library for host hooks
- `scripts/startup-hook.js`: host-facing session-start hook
- `templates/`: host integration templates

## Typical Flow

1. Agent runs `node scripts/subscription-state.js should-prompt`
2. If needed, agent asks the user whether they want `AI`, `医药`, `都要`, `暂不`, or `不再提示`
3. Agent records the answer in shared state
4. Agent routes onboarding into `follow-builders`, `med-builders`, or both

## Host Integration

If your runtime supports a session-start hook, call:

```bash
node /absolute/path/to/unified-digest/scripts/startup-hook.js --format json --lang zh --mark-asked
```

The returned JSON tells the host:

- whether to prompt now
- what exact prompt text to show
- whether normal session routing should continue
