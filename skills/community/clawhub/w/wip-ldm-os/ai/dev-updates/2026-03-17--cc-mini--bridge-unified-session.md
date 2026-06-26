# Bridge unified session fix

Bridge now sends `user: "main"` instead of `user: "claude-code"` when calling the OpenClaw chatCompletions endpoint. This routes CC messages to the main session instead of creating a separate `agent:main:openai-user:claude-code` session.

**Before:** CC messages went to an isolated session. Parker couldn't see them in the TUI.
**After:** CC messages appear in the same session as iMessage. Parker sees everything in one place.

Requires the companion OpenClaw gateway dist patch (local only, not upstream) that treats `user: "main"` as the default session key.

Closes #76
