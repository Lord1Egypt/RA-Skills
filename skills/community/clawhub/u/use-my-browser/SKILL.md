---
name: use-my-browser
description: |
  Control the user's REAL Chrome browser via Tampermonkey injection.
  Trigger when user says "use my browser", "open in my browser", "check this page for me", or needs to access login-required content.
  Reuses all login sessions. Does NOT steal the mouse cursor.
  Requires: openclaw-tmwd plugin + Tampermonkey userscript in Chrome.
---

# Use My Browser

Operate the user's real Chrome browser through Tampermonkey script injection. The agent runs JavaScript directly in the page context — sharing all cookies, sessions, and login state.

## Setup

```bash
openclaw plugins install openclaw-tmwd --registry https://registry.npmjs.org
```

Then install the [Tampermonkey userscript](https://raw.githubusercontent.com/lsdefine/pc-agent-loop/main/assets/ljq_web_driver.user.js) in Chrome. Green indicator at bottom-right = connected.

## Tools

| Tool | Purpose |
|------|---------|
| `tmwd_status` | Check connection, list connected tabs |
| `tmwd_switch` | Switch to tab matching URL pattern |
| `tmwd_navigate` | Navigate current tab to URL |
| `tmwd_newtab` | Open new tab |
| `tmwd_text` | Get visible text of current page |
| `tmwd_elements` | List interactive elements (buttons, links, inputs) |
| `tmwd_scan` | Get simplified HTML |
| `tmwd_exec` | Execute JavaScript in page context |

## Workflow

### Read a page

```
tmwd_status()                          # Verify connection
tmwd_switch(pattern="github.com")      # Switch to target tab
tmwd_text(max_chars=5000)              # Get page content
```

### Navigate to URL

```
tmwd_navigate(url="https://example.com")
tmwd_text()
```

### Click / fill / interact

```
tmwd_exec(code="document.querySelector('#submit').click()")

tmwd_exec(code="var e=document.querySelector('#email'); e.value='user@example.com'; e.dispatchEvent(new Event('input',{bubbles:true}))")
```

### Extract data

```
tmwd_exec(code="return document.querySelector('.content').innerText")

tmwd_exec(code="return Array.from(document.querySelectorAll('h2')).map(e=>e.textContent)")
```

### Read table data

```
tmwd_exec(code="var rows=document.querySelectorAll('table tr'); var d=[]; rows.forEach(function(r){var c=[]; r.querySelectorAll('td,th').forEach(function(e){c.push(e.innerText.trim())}); if(c.length) d.push(c)}); return d")
```

### Click by text match

```
tmwd_exec(code="var btns=document.querySelectorAll('button'); for(var i=0;i<btns.length;i++){if(btns[i].innerText.includes('Submit')){btns[i].click();break}}")
```

### Fill form with multiple fields

```
tmwd_exec(code="var f={'#username':'admin','#email':'a@b.com'}; Object.keys(f).forEach(function(s){var e=document.querySelector(s); e.value=f[s]; e.dispatchEvent(new Event('input',{bubbles:true}))})")
```

## JS Patterns Quick Reference

| Action | Code |
|--------|------|
| Click button | `document.querySelector('button.submit').click()` |
| Fill input | `var e=document.querySelector('#input'); e.value='x'; e.dispatchEvent(new Event('input',{bubbles:true}))` |
| Select dropdown | `var s=document.querySelector('select'); s.value='opt1'; s.dispatchEvent(new Event('change',{bubbles:true}))` |
| Check checkbox | `var c=document.querySelector('[type=checkbox]'); c.checked=true; c.dispatchEvent(new Event('change',{bubbles:true}))` |
| Scroll to bottom | `window.scrollTo(0, document.body.scrollHeight)` |
| Scroll to element | `document.querySelector('#target').scrollIntoView()` |
| Wait for element | `return !!document.querySelector('.loaded')` |
| Get current URL | `return location.href` |
| Go back | `history.back()` |

## CSP Fallback

Some sites (X/Twitter, banking sites) block `eval()` via Content Security Policy. When `tmwd_exec` returns `csp_blocked: true`, fall back to the built-in `browser` tool:

```
1. browser(action="open", profile="openclaw", url="<same-url>")
2. browser(action="snapshot", targetId=<targetId>)
```

Built-in browser uses CDP which bypasses CSP, but runs in a separate instance (no user login state — login once, profile is persisted).

**Rule: always try tmwd first, fall back only on failure.**

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No connected tabs" | Check green indicator in Chrome bottom-right |
| Red indicator | Refresh the page, userscript auto-reconnects |
| `el.click()` no effect | Try `el.dispatchEvent(new MouseEvent('click',{bubbles:true}))` |
| CSP blocks eval | Use `tmwd_text` (no eval needed) or fall back to built-in browser |

## Notes

- All JS runs in page context — shares cookies, localStorage, login state
- `el.click()` is DOM-level, does not move the mouse cursor
- Cross-origin iframes cannot be accessed (same-origin policy)
- If page refreshes, the userscript auto-reconnects with the same sessionId
- Use `return` in JS to send values back; without `return` there is no output
- For React/Vue apps, always use `dispatchEvent` after setting values — direct `.value=` alone won't trigger framework reactivity
