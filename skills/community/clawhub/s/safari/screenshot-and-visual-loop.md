# Screenshot and Visual Loop

## Why It Matters

Safari control is brittle if the agent only trusts command output.
Use screenshots to confirm the real visible state whenever the action depends on layout, rendered content, or focus.

## Foreground Capture

Get Safari window bounds, then capture that region:

```bash
BOUNDS=$(osascript -e '
tell application "System Events"
  tell process "Safari"
    set {x, y} to position of front window
    set {w, h} to size of front window
    return (x as text) & "," & (y as text) & "," & (w as text) & "," & (h as text)
  end tell
end tell')

screencapture -x -R "$BOUNDS" /tmp/safari.png
```

If Safari is not frontmost, activate it first and warn the user that the live browser will be brought forward.

## Visual Feedback Loop

1. read the current tab state
2. perform one action
3. capture Safari
4. inspect the image
5. decide the next step

Keep the loop short. One action, one verification.

## Safe Uses

- confirm which tab is active
- verify a click opened the intended menu or page
- check whether typing landed in the right field
- confirm modal, error, or login state before proceeding

## Common Mistakes

- Taking screenshots after several actions in a row -> hard to know what changed.
- Capturing Safari without warning when sensitive tabs may be visible -> privacy failure.
- Treating a screenshot as current after the page changed again -> stale evidence.
