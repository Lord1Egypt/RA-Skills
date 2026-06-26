# AppleScript Control

## Best Fit

Use AppleScript mode when the user wants the agent to work inside their real Safari session:
- read the current page
- switch or inspect open tabs
- navigate the active tab
- click or type in the live browser

## Read First

### List tabs

```bash
osascript -e '
tell application "Safari"
  set output to ""
  repeat with w from 1 to (count of windows)
    repeat with t from 1 to (count of tabs of window w)
      set output to output & "W" & w & "T" & t & " | " & name of tab t of window w & " | " & URL of tab t of window w & linefeed
    end repeat
  end repeat
  return output
end tell'
```

### Read current tab metadata

```bash
osascript -e '
tell application "Safari"
  return {name of current tab of front window, URL of current tab of front window}
end tell'
```

### Read visible page text

```bash
osascript -e '
tell application "Safari"
  do JavaScript "document.body.innerText" in current tab of front window
end tell'
```

## Navigate Safely

### Reuse current tab

```bash
osascript -e '
tell application "Safari"
  set URL of current tab of front window to "https://example.com"
end tell'
```

### Open a new tab

```bash
osascript -e '
tell application "Safari"
  tell front window
    set newTab to make new tab with properties {URL:"https://example.com"}
    set current tab to newTab
  end tell
end tell'
```

## Click and Fill

### DOM click

```bash
osascript -e '
tell application "Safari"
  do JavaScript "
    const el = document.querySelector(\"button, [role=button]\");
    if (!el) \"not found\";
    else {
      el.dispatchEvent(new MouseEvent(\"click\", {bubbles: true, cancelable: true}));
      \"clicked\";
    }
  " in current tab of front window
end tell'
```

### Set an input value with events

```bash
osascript -e '
tell application "Safari"
  do JavaScript "
    const input = document.querySelector(\"input, textarea\");
    if (!input) \"not found\";
    else {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, \"value\")?.set
        || Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, \"value\")?.set;
      setter.call(input, \"hello world\");
      input.dispatchEvent(new Event(\"input\", {bubbles: true}));
      input.dispatchEvent(new Event(\"change\", {bubbles: true}));
      \"filled\";
    }
  " in current tab of front window
end tell'
```

### Keystrokes only after focus is verified

```bash
osascript -e 'tell application "Safari" to activate'
osascript -e 'tell application "System Events" to keystroke "hello world"'
```

Do not use blind keystrokes until the correct app, tab, and input focus are confirmed.

## Switch Tabs Explicitly

```bash
osascript -e '
tell application "Safari"
  set current tab of front window to tab 2 of front window
end tell'
```

## Wait and Verify

```bash
osascript -e '
tell application "Safari"
  repeat 20 times
    if do JavaScript "document.readyState" in current tab of front window is "complete" then exit repeat
    delay 0.5
  end repeat
end tell'
```

After each meaningful action, re-read the title, URL, text, or screenshot before continuing.

## Common Mistakes

- Guessing selectors without reading the page first -> wrong element clicked.
- Using keystrokes when DOM-based input would work -> focus mistakes become expensive.
- Navigating the current tab without confirming the user is okay replacing it -> disrupts active work.
