# Signing in, the Zoom app and MCP

The core rules in [SKILL.md](../SKILL.md) apply.

## Sign in

- To log in, run `zm personal session start` in the background, read the URL after
  `Open this URL to approve Zoom login:` and give it to the person as a link; their browser must be on this computer.
  `--no-input` cannot approve it. The owner can also sign in from WireCat Desktop (Tools → Zoom → Manage).
- Tokens stay in the keyring.
- Missing scopes require changes to the Zoom app and a new login. `meetings show` from Zoom needs the optional
  `meeting:read:past_meeting` scope.
- `session status` is cached locally; `--check` verifies it remotely.

## The Zoom app and its client id

WireCat has no Zoom app: the person brings their own Public Client ID
([how](https://github.com/WireCatLabs/zoom-cli/blob/main/docs/zoom-app.md)). zm takes, first match wins,
`session start --client-id <id>` (saved as `zoom.client_id` on success), `ZM_ZOOM_CLIENT_ID`, then `zoom.client_id`;
`zm doctor --json` names the source under `oauth_client`.

## MCP

- `zm personal mcp serve` is for clients that cannot run commands (chat apps, remote agents); prefer the commands
  when you can run them. It serves them as `zm_tools_search`, `zm_read` and `zm_write`, with the same permissions as
  the command line; a call answers as the command does.
- Over MCP a change at level `ask` runs without a question.
- `zm mcp serve --profiles a,b` or `--profiles all` serves several profiles from one server; each tool then needs
  `profile` — ask which if the owner named none.
- The server captures source selections at startup; restart it after changing or revoking configuration.
- MCP serving and `watch` are foreground lifetimes; `--timeout` bounds finite commands.
