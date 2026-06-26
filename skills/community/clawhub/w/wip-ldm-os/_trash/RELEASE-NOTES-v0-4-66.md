# Release Notes: wip-ldm-os v0.4.66

Closes #255

## Bridge routes to main session

When CC sends Lesa a message through the bridge, it should appear in the same feed as Parker's iMessage conversations. One feed, all voices. That's how it was originally designed in February when the bridge was first built.

But the bridge was using the OpenAI-compatible endpoint's `user` field for session routing, which created a separate `openai-user:main` session. Parker's iMessage feed lived at `agent:main:main`. CC's bridge messages went to `openai-user:main`. Two feeds, split conversation. Parker couldn't see CC talking to Lesa unless he switched sessions in the TUI.

The fix restores the original `x-openclaw-session-key: agent:main:main` header that was dropped during the bridge absorption into LDM OS on Mar 15. The `user` field is removed since session routing is now handled entirely by the header.
