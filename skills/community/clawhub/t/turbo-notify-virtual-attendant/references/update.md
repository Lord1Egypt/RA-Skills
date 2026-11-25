# Updates

The skill checks its own version on every cycle (`tn_assist version-check --announce`, cached for an hour, or ten minutes after a failed check). When a newer version exists, the administrators get one message with the installed and new versions and the exact command for the harness. A failed check says nothing and never stops service.

## Commands, by harness

| Harness | Update |
|---|---|
| Claude Code | `claude plugin marketplace update turbo-notify`, then `claude plugin update turbo-notify@turbo-notify`, then restart. With auto-update on for the marketplace (`/plugin`, Marketplaces tab, Enable auto-update), it happens by itself when Claude Code starts. |
| Claude Desktop or Cowork | The marketplace syncs from the repository; Claude's documentation describes no manual update button, so if the new version does not show up, remove the `turbo-notify` marketplace on the Plugins page and add it again. A plugin uploaded by hand as a file does not update; install it from the marketplace instead. |
| Codex | `codex plugin marketplace upgrade`, then `codex plugin add turbo-notify@turbo-notify`. |
| Antigravity | `agy plugin install https://github.com/turbo-notify/agent-skills` again, over the installed one. |

Install the moving tag `v1` (for example `turbo-notify/agent-skills#v1`) so that a change that breaks things (`v2`) never arrives by itself. The Antigravity install has no tag: it follows the latest stable version.

## After an update

Run `tn_assist migrate`. If the new version needs a newer workspace layout, it makes a backup in `backup/` first, migrates, and puts everything back if a step fails. Running it again changes nothing. A workspace written by a newer version is left alone, with a message: update the skill instead.

Never edit the files of the installed skill. Local changes are lost on update; the policy and the knowledge in the workspace are yours and are kept.
