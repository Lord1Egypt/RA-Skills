# Preflight and Permissions

## Start With the Lowest-Risk Probe

Run one safe read command before any click, type, or screenshot:

```bash
osascript -e 'tell application "Safari" to get name of front window'
```

If this fails, do not continue with live-session control until the permission path is clear.

## Permission Ladder

### Apple Events / Automation

Safari control through AppleScript requires the terminal app to be allowed to control Safari.

Use this probe:

```bash
osascript -e 'tell application "Safari" to get URL of current tab of front window'
```

If macOS prompts for Automation permission, approve it for the terminal app in use.

### `safaridriver`

Enable WebDriver access once:

```bash
safaridriver --enable
```

Start a local driver instance when needed:

```bash
safaridriver -p 0
```

Use `--diagnose` when setup is flaky or the session dies unexpectedly:

```bash
safaridriver --diagnose -p 0
```

### Screen Recording

If the workflow needs screenshots of the live Safari window, the terminal app may need Screen Recording permission.
Do not assume this is granted just because `screencapture` exists.

## JavaScript Preflight

If the plan uses `do JavaScript` in Safari, verify a simple read script first:

```bash
osascript -e 'tell application "Safari" to do JavaScript "document.title" in current tab of front window'
```

If Safari blocks this path, stop and resolve the browser-side permission or menu setting before writing more automation around it.

## Safe Preflight Checklist

1. Safari is installed and running
2. The correct terminal app has Automation permission
3. The target is the expected window or tab
4. `safaridriver --enable` has been run if WebDriver mode is required
5. Screen Recording is approved if screenshots are required

## Common Mistakes

- Starting with a click command before a read probe -> hard to tell whether failure is permissions or selector logic.
- Forgetting that each terminal app has separate macOS permissions -> Terminal and iTerm do not share approval.
- Leaving `safaridriver` running without deciding whether the session should be real-state or isolated-state -> later assumptions become muddy.
