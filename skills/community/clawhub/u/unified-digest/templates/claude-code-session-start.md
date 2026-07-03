# Claude Code Session-Start Template

Claude Code itself does not expose a universal built-in "window opened" hook, so the practical integration point is:

- intercept the first user turn in a fresh session
- call `startup-hook.js`
- optionally short-circuit the normal tool/task workflow with the subscription prompt

## Wrapper Flow

Before dispatching the first user message to the agent:

```bash
node /absolute/path/to/unified-digest/scripts/startup-hook.js --format json --lang zh --mark-asked
```

If `shouldPrompt` is `true`:

1. prepend or replace the first assistant response with the returned `message`
2. store a session flag such as `awaiting_digest_subscription=true`
3. on the next user reply, route into the unified-digest answer mapping

If `shouldPrompt` is `false`, proceed as normal.

## Minimal Routing

- `AI` -> `node unified-digest/scripts/subscription-state.js set-topic ai subscribed`
- `医药` -> `node unified-digest/scripts/subscription-state.js set-topic med subscribed`
- `都要` -> mark both subscribed, then collect shared defaults
- `暂不` -> `node unified-digest/scripts/subscription-state.js snooze 7`
- `不再提示` -> `node unified-digest/scripts/subscription-state.js dismiss`

## Why This Shape

This keeps the startup decision deterministic and host-side. The LLM only sees:

- whether it should prompt
- the exact text to show
- the user's answer

That reduces repeated prompting and avoids burying subscription logic in the general system prompt.
