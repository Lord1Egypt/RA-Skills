---
name: remote-claws
description: "Full control of a remote machine via Remote Claws MCP: screenshots, mouse/keyboard, browser automation, run commands, read/write files on the remote host."
homepage: https://github.com/wentbackward/remote-claws
---

# Remote Claws — Remote Machine Control

Provide permission-based access to a remote desktop machine via the
remote-claws MCP server (https://github.com/wentbackward/remote-claws) allowing
your agent to run in a sandbox.

Four tools, each taking an `action` parameter: `remote_browser`, `remote_desktop`,
`remote_exec`, `remote_files`. Read each tool's description for its action
list — an unknown action returns the valid list.

## CRITICAL: Remote vs Local

The `remote_*` tools act on the REMOTE machine. OpenClaw's built-in `browser`,
`exec`, `read`/`write`/`edit` act on the LOCAL gateway machine. Never
substitute one for the other. Take care not to confuse remote-claws with remote
SSH commands.

## Strategy

1. **Screenshot first.** `remote_desktop(action="screenshot")` before clicking
   or typing; use the returned coordinates to target actions. Re-screenshot
   after actions — windows move, dialogs appear.
2. **Prefer remote_browser for web tasks.** CSS selectors are
   resolution-independent. Only fall back to `remote_desktop` for things the
   browser can't reach (native dialogs, file pickers).
3. **Prefer element names over coordinates.** `remote_desktop(action=
   "click_element", ...)` targets controls by name — survives window moves.
4. **Exec is async.** `remote_exec(action="run", ...)` returns a process_id;
   poll with `action="get_output"` (wait=true blocks), `action="send_input"`
   for stdin, `action="kill"` when done.
5. **Denied actions are final.** A "permission denied" result means server
   policy — do not retry unless the user requests it.

## Common actions

- Desktop: screenshot, mouse_click, mouse_move, mouse_drag, scroll,
  type_text (ASCII only), press_key, find_window, focus_window,
  list_elements, click_element, get_element_text
- Browser: navigate, click, fill (clears first, Unicode-safe), type
  (appends), press_key, get_text, get_html, eval_js, screenshot, wait_for,
  select_option, go_back, go_forward, tabs_list, tab_new, tab_close
- Exec: run, get_output, send_input, kill, list
- Files: read (base64, offset/limit for chunks), write (base64), list,
  delete, move, info

## Authentication & Security

The remote-claws MCP server requires a bearer token, configured in
`openclaw.json` when registering the server. Unauthenticated connections get
401. The server also supports IP allowlisting (`allowed_ips`), host header
validation (`allowed_hosts`), and per-action permission policies
(`permissions.json`). See the [setup guide](https://github.com/wentbackward/remote-claws/blob/master/remote-claws-openclaw-setup-guide.md)
and [README](https://github.com/wentbackward/remote-claws#security).

## Important Notes

- Screenshots are JPEG, max 1280x960. Coordinates are absolute pixels. If your main
  LLM supports images, openclaw media handling should just work. Otherwise use
  `remote_desktop(action="screenshot", save_to_disk=true)` and download the binary.
- **Reading Remote Files**: `remote_files(action="read", ...)` returns base64
  only up to a threshold. Bigger reads fail with `"inline read would return N bytes"`
  to avoid context token explosion. Re-issue the same read with `as_url=true` and use
  the returned URL to download — do NOT retry the plain read. Small chunks via
  offset/limit will work.
- `type_text` is ASCII only. For Unicode, use browser `fill`, or clipboard:
  `remote_exec(action="run", command="powershell", args=["Set-Clipboard", ...])`
  then `remote_desktop(action="press_key", keys="ctrl+v")`.
- The browser launches on first use and stays open across calls. Sessions
  persist (cookies, local storage).
