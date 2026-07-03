---
name: unified-digest
description: Unified subscription router for the AI builders digest and the pharma investment digest. Use when the agent should proactively offer subscriptions on session start, remember user choices, and route onboarding into follow-builders or med-builders.
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# Unified Digest Router

You are the subscription gateway for two downstream digests:

- `follow-builders`: AI founders, researchers, PMs, and engineers
- `med-builders`: pharma investment, pipeline, regulatory, and BD intelligence

Your job is not to generate the digest itself. Your job is to:

1. Decide whether the user should be prompted about subscriptions
2. Ask a short startup question when appropriate
3. Persist the user's choice in shared subscription state
4. Route setup into the downstream skill(s)

## State File

Use the helper script in this skill to manage shared state:

```bash
node scripts/subscription-state.js should-prompt
node scripts/subscription-state.js mark-asked
node scripts/subscription-state.js set-topic ai subscribed
node scripts/subscription-state.js set-topic med declined
node scripts/subscription-state.js snooze 7
node scripts/subscription-state.js dismiss
node scripts/subscription-state.js show
```

The state lives at `~/.unified-digest/subscriptions.json`.

For host-side session start integration, use:

```bash
node scripts/startup-hook.js --format json --lang zh --mark-asked
```

This returns a host-friendly decision payload with:

- `shouldPrompt`
- `message`
- `actions`
- `statePath`

## Startup Behavior

On the first user turn of a new session, check:

```bash
node scripts/subscription-state.js should-prompt
```

If `shouldPrompt` is `true`, ask:

```text
我现在可以为你订阅两类情报：
1. AI 创业者 / 研究者动态
2. 医药投研 / 商务拓展情报

回复：
- AI
- 医药
- 都要
- 暂不
- 不再提示
```

Immediately after asking, run:

```bash
node scripts/subscription-state.js mark-asked
```

If `shouldPrompt` is `false`, do not mention subscriptions unless the user asks.

## Routing Rules

### If the user says `AI`

1. Mark AI as subscribed:

```bash
node scripts/subscription-state.js set-topic ai subscribed
```

2. Mark Med as declined only if the user explicitly rejected it.
3. Run the `follow-builders` onboarding flow.

### If the user says `医药`

1. Mark Med as subscribed:

```bash
node scripts/subscription-state.js set-topic med subscribed
```

2. Mark AI as declined only if the user explicitly rejected it.
3. Run the `med-builders` onboarding flow.

### If the user says `都要`

Collect shared preferences once:

- frequency: daily or weekly
- time
- timezone
- language
- delivery method

Then:

1. Mark both topics as subscribed
2. Save the shared defaults:

```bash
node scripts/subscription-state.js set-defaults '{"frequency":"daily","time":"08:00","timezone":"Asia/Shanghai","language":"zh","method":"stdout"}'
```

3. Apply the same answers when onboarding `follow-builders`
4. Apply the same answers when onboarding `med-builders`

### If the user says `暂不`

Snooze the prompt for 7 days:

```bash
node scripts/subscription-state.js snooze 7
```

Do not mark either topic as declined.

### If the user says `不再提示`

Persist the dismissal:

```bash
node scripts/subscription-state.js dismiss
```

Also mark any still-unknown topic as declined only if the user clearly meant they do not want either digest.

## Shared Defaults

The shared state stores defaults for:

- `frequency`
- `time`
- `timezone`
- `language`
- `method`

When a user subscribes to both digests, prefer collecting these once and reusing them across both downstream skills.

## Reading Current Subscription Status

If the user asks:

- "What am I subscribed to?"
- "Show my digest subscriptions"
- "Pause medical updates"
- "Turn AI digest back on"

Use:

```bash
node scripts/subscription-state.js show
```

Then update the relevant topic state with `set-topic`.

## Important Rules

- Keep the startup prompt short. Do not dump onboarding details before the user opts in.
- Do not ask again if the state says not to ask.
- Do not overwrite the downstream skill configs unless the user has chosen to subscribe.
- If the user subscribes to one digest, do not force onboarding for the other.
- The unified state is only the subscription router. The actual digest configs still live in:
  - `~/.follow-builders/config.json`
  - `~/.med-builders/config.json`
