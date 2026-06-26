---
name: remote-claws
description: "Full remote desktop control of a machine via Remote Claws MCP. Use when asked to: take a screenshot of the remote desktop; click, type, or drag with the mouse/keyboard on the remote machine; run commands or scripts; automate a Chromium browser on the remote machine; read or write files on the remote machine."
homepage: https://github.com/wentbackward/remote-claws
---

# Remote Claws — Remote Desktop Control

Controls a remote machine over MCP/SSE. All 39 tools are provided by the remote-claws MCP server registered in openclaw.json.

## When to Use This Skill

Use Remote Claws tools whenever you need to interact with the remote desktop machine — taking screenshots, clicking buttons, typing text, running commands, automating a browser, or transferring files. If the user asks you to do something "on the remote machine" or "on Windows," these are your tools.

## Strategy

1. **Screenshot first.** Before clicking or typing, take a `desktop_screenshot` to see what's on screen. Use the coordinates from the screenshot to target actions.
2. **Prefer browser tools for web tasks.** `browser_*` tools use CSS selectors and are resolution-independent. Only use `desktop_*` tools for web tasks if the browser tools can't reach something (e.g. browser dialogs, file pickers).
3. **Prefer element names over coordinates.** `desktop_click_element` and `desktop_get_element_text` target UI controls by name — more reliable than coordinate clicking, which breaks when windows move.
4. **Exec is async.** `exec_run` starts a command and returns immediately. Use `exec_get_output` with `wait=true` if you need to block until it finishes.
5. **Re-screenshot after actions.** Windows may move, dialogs may appear. Take a fresh screenshot to verify the result before proceeding.

## Tool Groups

### Desktop (mouse, keyboard, screenshots)
- `desktop_screenshot` — capture full screen or region [x, y, width, height]
- `desktop_mouse_click` — left/right/middle click at x, y
- `desktop_mouse_move` — move cursor to x, y
- `desktop_mouse_drag` — drag from start to end coordinates
- `desktop_type_text` — type ASCII text at current focus (ASCII only)
- `desktop_press_key` — press key or combo: "enter", "ctrl+c", "alt+f4"
- `desktop_scroll` — scroll at x,y; direction "up" or "down"
- `desktop_find_window` — find windows by title or class_name substring
- `desktop_focus_window` — bring window to foreground by title
- `desktop_list_elements` — list UI controls (buttons, fields) inside a window
- `desktop_click_element` — click a named UI element (more reliable than coords)
- `desktop_get_element_text` — read the value of a named UI element

### Browser (Chromium via Playwright — CSS selectors)
- `browser_navigate` — go to a URL
- `browser_click` — click element by CSS selector
- `browser_fill` — set input value (handles Unicode, triggers change events)
- `browser_type` — type keystroke-by-keystroke (appends, does not clear)
- `browser_press_key` — key press e.g. "Enter", "Control+a"
- `browser_get_text` — extract visible text from element (default: body)
- `browser_get_html` — get HTML markup of element
- `browser_eval_js` — run JavaScript in page context
- `browser_screenshot` — screenshot page or element
- `browser_wait_for` — wait for element state: visible/hidden/attached/detached
- `browser_select_option` — select a dropdown option by value or label
- `browser_go_back` / `browser_go_forward`
- `browser_tabs_list` / `browser_tab_new` / `browser_tab_close`

### Exec (run commands, async)
- `exec_run` — start command; returns process_id immediately
- `exec_get_output` — read stdout/stderr; set wait=true to block
- `exec_send_input` — send a line to stdin of a running process
- `exec_kill` — terminate a process
- `exec_list` — list all tracked processes

### Files (base64 encoded)
- `file_write` — write base64 content to a path
- `file_read` — read file as base64 (use offset/limit for large files)
- `file_list` — list directory; supports glob patterns, recursive
- `file_delete` — delete file or empty directory
- `file_move` — move or rename file/directory
- `file_info` — get size, created, modified timestamps

## Authentication & Security

The remote-claws MCP server requires a bearer token, configured in `openclaw.json` when registering the server. The server will reject unauthenticated connections with 401.

The server also supports IP allowlisting (`allowed_ips`), host header validation (`allowed_hosts`), and per-tool permission policies (`permissions.json`) to restrict which tools are available. See the [setup guide](https://github.com/wentbackward/remote-claws/blob/master/remote-claws-openclaw-setup-guide.md) and [README](https://github.com/wentbackward/remote-claws#security) for configuration details.

## Important Notes

- Screenshots are JPEG, max 1280x960. Coordinates are absolute pixels.
- `desktop_type_text` is ASCII only. For Unicode, use `browser_fill` or clipboard: `exec_run powershell Set-Clipboard`, then `desktop_press_key ctrl+v`.
- File content is base64 encoded. Decode after reading.
- The browser launches on first use and stays open across calls. Sessions persist (cookies, local storage).
