# browse — Operational Guides

Read this file when you need the handoff protocol, optimization tips, or help choosing which command to use.

## Handoff Protocol (MANDATORY)

Read this section when you hit CAPTCHA, MFA, OAuth, or any blocker after 2-3 failed attempts. The server auto-suggests handoff after 3 consecutive failures (look for HINT in error messages).

When the browser hits a blocker you can't solve, you MUST follow this exact 3-step protocol. Do NOT skip any step.

### Step 1 — Ask permission (REQUIRED before handoff)

Use `AskUserQuestion` (or your platform's equivalent interactive prompt tool) to ask
the user before opening the browser. Do NOT just print text and proceed — you MUST
wait for an explicit response.

```
AskUserQuestion:
  question: "I'm stuck on a CAPTCHA at [URL]. Can I open a visible browser so you can solve it?"
  options:
    - label: "Yes, open browser"
      description: "Opens a visible Chrome window with your current session"
    - label: "No, try something else"
      description: "I'll try cookie-import, auth login, or a different approach"
```

If your platform does not have `AskUserQuestion`, ask the user via text and wait for
their response before proceeding. Do NOT run handoff without explicit user confirmation.

If the user says no, try `cookie-import`, `auth login`, or a different approach.

### Step 2 — Handoff + wait for user (REQUIRED)

Run the handoff command, then use `AskUserQuestion` (or equivalent) to wait for the
user to finish:

```bash
browse handoff "Stuck on CAPTCHA at login page"
```

Then immediately prompt the user:

```
AskUserQuestion:
  question: "Browser is open. Please solve the CAPTCHA, then click Done."
  options:
    - label: "Done"
      description: "I've solved it, return to headless mode"
    - label: "Cancel"
      description: "Close the browser, try something else"
```

Do NOT proceed or do any other work while waiting. The user is interacting with the
visible browser — wait for their response.

### Step 3 — Resume

After the user responds:

```bash
browse resume
# Returns fresh snapshot — continue working with it
```

If "Done" — continue with the fresh snapshot from resume.
If "Cancel" — resume anyway (closes headed browser), then try alternative approach.

### When to Handoff
- CAPTCHA or bot detection blocking progress
- Multi-factor authentication requiring a physical device
- OAuth popup that redirects to a third-party login
- Any blocker after 2-3 failed attempts at the same step
- The server auto-suggests handoff after 3 consecutive failures (look for HINT in error messages)

### When NOT to Handoff
- Normal navigation/interaction failures — retry or try a different selector
- Pages that just need more time to load — use `wait` commands
- Cookie/auth issues — try `cookie-import` or `auth login` first

### Handoff Rules
- NEVER run `browse handoff` without asking the user first (Step 1)
- NEVER proceed without waiting for the user to finish (Step 2)
- ALWAYS tell the user what they need to do in the visible browser
- ALWAYS run `browse resume` after the user is done

## Speed Rules

Read this section to optimize your command usage and minimize token consumption.

1. **Navigate once, query many times.** `goto` loads the page; then `text`, `js`, `css`, `screenshot` all run against the loaded page instantly.
2. **Use `snapshot -i` for interaction.** Get refs for all interactive elements, then click/fill by ref. No need to guess CSS selectors.
3. **Use `snapshot -C` for SPAs.** Catches cursor:pointer divs and onclick handlers that ARIA misses.
4. **Use `js` for precision.** `js "document.querySelector('.price').textContent"` is faster than parsing full page text.
5. **Use `links` to survey.** Faster than `text` when you just need navigation structure.
6. **Use `chain` for multi-step flows.** Avoids CLI overhead per step.
7. **Use `responsive` for layout checks.** One command = 3 viewport screenshots.
8. **Use `--session` for parallel work.** Multiple agents can browse simultaneously without interference.
9. **Use `value`/`count` instead of `js`.** Purpose-built commands are cleaner than `js "document.querySelector(...).value"`.
10. **Use `frame` for iframes.** Don't try to reach into iframes with CSS — use `frame [id=x]` first.

## When to Use What

Read this section when you're unsure which command to use for a task.

| Task | Commands |
|------|----------|
| Read a page | `goto <url>` then `text` |
| Interact with elements | `snapshot -i` then `click @e3` |
| Find hidden clickables | `snapshot -i -C` then `click @e15` |
| Check if element exists | `count ".thing"` |
| Get input value | `value "[id=email]"` |
| Extract specific data | `js "document.querySelector('.price').textContent"` |
| Visual check | `screenshot` then `Read .browse/sessions/default/screenshot.png` |
| Fill and submit form | `snapshot -i` then `fill @e4 "val"` then `click @e5` |
| Check/uncheck boxes | `check @e7` / `uncheck @e7` |
| Check CSS | `css "selector" "property"` or `css @e3 "property"` |
| Inspect DOM | `html "selector"` or `attrs @e3` |
| Debug console errors | `console` |
| Check network requests | `network` |
| Mock API responses | `route "**/api/*" fulfill 200 '{"data":[]}'` |
| Block ads/trackers | `route "**/*.doubleclick.net/*" block` |
| Test offline behavior | `offline on` then test then `offline off` |
| Interact in iframe | `frame "[id=payment]"` then `fill @e2 "4242..."` then `frame main` |
| Check local dev | `goto http://127.0.0.1:3000` |
| Compare two pages | `diff <url1> <url2>` |
| Mobile layout check | `responsive .browse/sessions/default/resp` |
| Test on mobile device | `emulate iphone` then `goto <url>` then `screenshot` |
| Save/restore session | `state save mysite` / `state load mysite` |
| Auto-login | `auth save gh https://github.com/login user pass` then `auth login gh` |
| Record network | `har start` then browse then `har stop ./out.har` |
| Record video | `video start ./vids` then browse then `video stop` |
| Export automation script | `record start` then browse then `record export replay ./recording.json` |
| Parallel agents | `--session agent-a <cmd>` / `--session agent-b <cmd>` |
| Multi-step flow | `echo '[...]' \| browse chain` |
| Secure browsing | `--allowed-domains example.com goto https://example.com` |
| Scroll through results | `scroll down` then `text` then `scroll down` then `text` |
| Drag and drop | `drag @e1 @e2` |
| Read/write clipboard | `clipboard` / `clipboard write "text"` |
| Find by accessibility | `find role button` / `find text "Submit"` |
| Visual regression | `screenshot-diff baseline.png` |
| Debug with DevTools | `inspect` (set BROWSE_DEBUG_PORT first) |
| Get element position | `box @e3` |
| Check page errors | `errors` |
| Right-click context menu | `rightclick @e3` |
| Test mobile gestures | `emulate iphone` then `tap @e1` / `swipe down` |
| Set dark mode | `set media dark` |
| Test geolocation | `set geo 37.7 -122.4` then verify in page |
| Export/import cookies | `cookie export ./cookies.json` / `cookie import ./cookies.json` |
| Limit output size | `--max-output 5000 text` |
| See the browser | `browse --headed goto <url>` |
| CAPTCHA / MFA blocker | `handoff "reason"` then user solves then `resume` (see Handoff Protocol above) |
| Debug React components | `react-devtools enable` then `tree` then `props @e3` |
| Debug hydration issues | `react-devtools enable` then `hydration` |
| Find suspense blockers | `react-devtools enable` then `suspense` |
| Bypass bot detection | `--runtime rebrowser goto <url>` |
| Persistent login state | `--profile mysite` then browse then close then reopen (still logged in) |
| Cloud browser (CI/CD) | `provider save browserbase <key>` then `--provider browserbase goto <url>` |

## Architecture

Read this section to understand the system design.

- Persistent Chromium daemon on localhost (port 9400-10400)
- Bearer token auth per session
- One server per project directory — `--session` handles agent isolation
- Session multiplexing: multiple agents share one Chromium via isolated BrowserContexts
- For separate servers: set `BROWSE_INSTANCE` env var (e.g., fault isolation between teams)
- `browse instances` — discover all running servers (PID, port, status, session count)
- Project-local state: `.browse/` directory at project root (auto-created, self-gitignored)
  - `sessions/{id}/` — per-session screenshots, logs, PDFs
  - `states/{name}.json` — saved browser state (cookies + localStorage)
  - `browse-server.json` — server PID, port, auth token
- Auto-shutdown when all sessions idle past 30 min
- Chromium crash — server exits — auto-restarts on next command
- AI-friendly error messages: Playwright errors rewritten to actionable hints
- CDP remote connection: `BROWSE_CDP_URL` to connect to existing Chrome
- Policy enforcement: `browse-policy.json` for allow/deny/confirm rules
- Two browser engines: playwright (default) and rebrowser (stealth, bypasses bot detection)
