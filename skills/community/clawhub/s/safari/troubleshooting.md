# Troubleshooting

## Failure Ladder

Use this order:

1. confirm control mode: AppleScript or WebDriver
2. confirm Safari is running and the target surface exists
3. run the smallest read probe
4. resolve permissions
5. retry one action
6. verify visually or by re-read

## Common Failures

### Safari does not respond to AppleScript

- Check Automation permission for the terminal app.
- Run the simplest probe again before trying a more complex script.
- If Safari is not running, launch it explicitly and retry.

### `do JavaScript` fails

- Verify the current tab is a normal web page, not a browser-internal surface.
- Confirm Safari allows the JavaScript automation path required for the session.
- Fall back to read-only tab metadata if JavaScript execution is blocked.

### `safaridriver` fails to start

- Re-run `safaridriver --enable`.
- Start with `safaridriver -p 0` before adding more flags.
- Add `--diagnose` only after the simple start path still fails.

### Typing lands in the wrong place

- Stop using blind keystrokes immediately.
- Re-activate Safari and verify the exact tab and focused element.
- Prefer DOM-based input with read-back verification.

### Screenshot does not match the expected page

- Confirm the front window changed after the last action.
- Re-capture immediately after bringing Safari forward.
- Check whether another app stole focus between actions.

## Recovery Principles

- One variable at a time
- One action, one verification
- Prefer read-first fallbacks over repeated forced clicks
- Switch control mode if the task assumptions were wrong
