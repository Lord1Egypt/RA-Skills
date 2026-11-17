---
name: rebind-computer-use
description: Drive THIS computer with a real hardware keyboard and mouse via Rebind — click, type, browse, fill forms, operate any desktop GUI. The OS sees genuine USB input, so it works even in apps that reject synthetic input.
version: 0.2.1
metadata:
  openclaw:
    emoji: "🖱️"
    homepage: https://rebind.gg
    os: ["darwin", "win32"]
    requires:
      env:
        - REBIND_URL
      bins:
        - bun
    primaryEnv: REBIND_URL
---

# Rebind Computer Use

You can drive a real computer through a hardware keyboard and mouse. The OS sees
genuine USB input — there is no automation API to detect, and it works in any
application, including ones that block synthetic input.

## Setup (do this first — the skill does nothing without it)

This skill controls the machine through **Rebind**, a separate app. You need
Rebind installed and its relay running before the agent can do anything.

1. **Install Rebind** on the machine to be controlled — https://rebind.gg/download
   (Windows or macOS). Rebind drives a genuine USB HID device (a Teensy) for
   truly undetectable input, or a software-mode fallback if you have no device.
2. **Start the relay:** in Rebind, load and run the **Remote Access** script.
   The skill talks to it over `ws://127.0.0.1:19561`. This is the #1 reason a
   first attempt fails — no relay, nothing works.
3. **Install this skill + register the MCP server:**
   ```sh
   openclaw skills install @usinput/rebind-computer-use
   openclaw mcp add rebind --no-probe \
     --command bunx --arg @rebind.gg/mcp-server \
     --env REBIND_URL=ws://127.0.0.1:19561
   openclaw config set skills.entries.rebind-computer-use.env.REBIND_URL ws://127.0.0.1:19561
   ```
4. **Confirm the relay is reachable:** `bunx @rebind.gg/mcp-server --selftest`
5. **Start a NEW OpenClaw session** — skills are snapshotted at session start,
   so one installed mid-session stays invisible until you restart.

Full walkthrough (Windows pointer-precision note, auth tokens, troubleshooting)
is in **README.md**. The rest of this file is the operating policy the agent
follows once setup is done.

## Script first, screenshots second

Screenshots are by far the most expensive thing you do: every one you take is
re-sent on every later turn, so a screenshot-per-action loop costs quadratically.
The discipline that keeps tasks fast and cheap:

- **Batch every deterministic sequence into ONE `run_lua` call** — launching
  apps, placing windows, focusing, typing known text, pressing known keys,
  waiting for a window or process. End the script with `return <value>` and use
  that return value as your verification; it costs almost nothing.
- **Verify once, at checkpoints** — after a batch, after a navigation, before
  an irreversible step. Not after every keystroke.
- **Prefer the cheap reads**: `screenshot_window` (one window, monitor-proof)
  over `screenshot` (whole display); `zoom` (small crop) over either when you
  only need to read a value or a label; `run_lua` return values over any image.
- Fall back to full screenshots only for genuinely visual reasoning a script
  cannot resolve.

## Open → place → interact

New windows open wherever the OS pleases — often on a display you are not
looking at. Never guess with screenshots on a multi-monitor machine. Open the
app, wait for its window, move it somewhere known, THEN look:

```lua
System.ExecDetached("cmd", {"/c", "start", "", "https://news.ycombinator.com"})
local h = Window.Wait("Hacker News", 8000)
Window.Move(h, 0, 0, 1600, 1000)  -- pin to the primary display
return Window.Get(h)
```

Then `screenshot_window` that window and continue.

## The visual loop (when scripts can't decide)

1. **`screenshot_window`** (or `screenshot`) — capture. The cursor is a red
   crosshair. ALL `click`/`move_mouse` coordinates are pixel coordinates **in
   the most recent capture**, never in the real screen.
2. **Reason** about what to do next from what you see.
3. **Act** — `click`, `type`, `key`, `scroll`, `focus_window`, or a `run_lua`
   batch.
4. **Verify at the next checkpoint** — cheaply (`zoom`, `screenshot_window`, a
   script return value). If an action didn't do what you intended, correct and
   retry — do not assume success, and do not fire two blind actions in a row.

## Tools

- `run_lua(source)` — run a Luau script on the machine and get its `return`
  value as JSON. Namespaces: System, HID, Input, Screen, Window, Process, File,
  Clipboard, Net, Macro, Env, Log. Your primary tool for anything deterministic.
- `screenshot(display?)` — capture a whole display.
- `screenshot_window(title?)` — capture one window (active if omitted).
  Smaller, cheaper, monitor-proof. Prefer this.
- `zoom(x,y,w,h)` — re-read a region of the last capture at native resolution.
  Read-only: click coordinates still refer to the last full capture.
- `list_displays` — enumerate monitors.
- `click(x,y,button?,double?)` — landing is verified & corrected before pressing.
- `move_mouse(x,y)` — move without clicking.
- `type(text)` — type into the focused element.
- `key(combo)` — press a key/combo. Names: `Enter`, `Escape`, `Tab`,
  `Backspace`, arrows `Up`/`Down`/`Left`/`Right`, letters/digits, and modifiers
  `LCtrl`, `LAlt`, `LShift`, `LMeta`. Join combos with `+`:
  `LCtrl+L` (focus the address bar), `LCtrl+C`, `LAlt+Tab`.
- `scroll(clicks)` — wheel; positive up, negative down.
- `list_windows(filter?)` / `focus_window(handle)` — window management.
- `wait(ms)` — let pages/animations settle (1–10000).
- `get_cursor` / `active_window` — cheap state reads.
- `calibrate` — re-run the mouse scale probe (auto-runs at startup).

## No shortcuts

`System.Exec`/`System.ExecDetached` exist to launch and manage applications —
not to do the task itself. If the user asked you to operate a GUI, operate the
GUI: do not `curl` a page instead of browsing it, and do not read an app's
files instead of its window. Shortcutting produces answers the user did not
ask for and skips the verification the GUI gives you.

## Ergonomics

- **Prefer keyboard shortcuts over mouse** for fiddly widgets: address bars
  (`LCtrl+L`), tabs, dropdowns, menus. Faster and far more reliable than
  pixel-hunting.
- `zoom` before clicking anything with small text.
- If a capture warns the mouse is **not calibrated**, treat every click as
  unverified: verify each one and correct.
- Wait for loads (`wait` 500–1500ms, or `Window.Wait` in a script) before
  capturing after a navigation.
- When you learn something machine-specific (display layout, an app's quirks,
  where a window opens), reuse it for the rest of the session instead of
  rediscovering it.

## Safety — non-negotiable

- **Confirm before irreversible or outbound actions.** Before sending an email,
  submitting a form, making a payment, deleting anything, or posting publicly:
  STOP, summarize exactly what you are about to do (recipient, amount, content),
  and ask the user to confirm in the chat. Only proceed on an explicit "yes".
- **Never enter credentials, payment details, or 2FA codes** unless the user
  supplied them in this conversation for this exact purpose.
- When unsure whether an action is reversible, treat it as irreversible.
- If you get lost (3 failed verifications in a row), stop and report what you
  see — do not flail.
