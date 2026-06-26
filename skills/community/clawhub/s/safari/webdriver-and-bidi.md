# WebDriver and BiDi

## Best Fit

Use `safaridriver` when the user wants Safari-specific automation but not direct control over their currently open tabs.
This is the cleaner mode for repeatable flows, tests, and isolated repros.

## Driver Lifecycle

Enable Safari WebDriver once:

```bash
safaridriver --enable
```

Run a local driver instance:

```bash
safaridriver -p 0
```

Enable diagnostic logging when a session is unstable:

```bash
safaridriver --diagnose -p 0
```

Enable WebDriver BiDi on a local port when the client supports it:

```bash
safaridriver --bidi 0 -p 0
```

## Quick Client Example

Python with Selenium:

```python
from selenium import webdriver

driver = webdriver.Safari()
driver.get("https://example.com")
print(driver.title)
driver.quit()
```

## Session Rules

- Treat WebDriver mode as isolated until proven otherwise.
- Do not promise that cookies, tabs, or logins from the user's visible Safari windows are automatically shared.
- Use WebDriver mode for clean repros, form workflows, and deterministic browser-state checks.

## Verification Rule

After starting WebDriver:
- confirm the session actually launches
- confirm the target page loads
- confirm the browser state matches the intended test path

If the task depends on the exact tabs the user already has open, switch back to AppleScript mode instead of forcing WebDriver to pretend it is the same session.

## When to Hand Off

- If the user needs a richer browser automation framework or cross-browser parity, move to `playwright`.
- If the blocker is Safari permissions or app focus rather than WebDriver itself, move to `macos`.

## Common Mistakes

- Starting `safaridriver` and assuming the real Safari session is now under control -> wrong mental model.
- Using WebDriver for a task that explicitly depends on the user's existing logged-in tabs -> session mismatch.
- Leaving diagnostics on by default -> noisy logs and unclear intent.
