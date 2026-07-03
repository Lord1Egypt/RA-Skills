# OpenClaw Session-Start Template

Use this when your host can run a command before the first assistant reply in a new session.

## Pre-Reply Hook

Run:

```bash
node /absolute/path/to/unified-digest/scripts/startup-hook.js --format json --lang zh --mark-asked
```

If the returned JSON says `shouldPrompt: true`, inject the `message` as the assistant's first reply and stop normal routing until the user answers.

If `shouldPrompt: false`, continue the normal session.

## Answer Routing

Map the user's answer like this:

- `AI` -> run `follow-builders` onboarding
- `医药` -> run `med-builders` onboarding
- `都要` -> collect shared preferences once, then onboard both
- `暂不` -> `node unified-digest/scripts/subscription-state.js snooze 7`
- `不再提示` -> `node unified-digest/scripts/subscription-state.js dismiss`

## Suggested Host Pseudocode

```text
onSessionStart(session):
  result = run(startup-hook.js --format json --lang zh --mark-asked)
  if result.shouldPrompt:
    sendAssistantMessage(result.message)
    session.flags.awaitingDigestSubscription = true

onUserMessage(session, text):
  if session.flags.awaitingDigestSubscription:
    routeDigestAnswer(text)
    session.flags.awaitingDigestSubscription = false
    return
  continueNormalAgentFlow()
```
