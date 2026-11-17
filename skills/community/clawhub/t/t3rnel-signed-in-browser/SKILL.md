---
name: signed-in-browser
description: Drive the browser the user is already signed into, instead of a cold automation profile. Use when a task lives behind a login — a dashboard, an admin console, an internal tool, a ticket queue, a bank or billing page, webmail, a social account — or when a scripted login is failing on SSO, MFA, CAPTCHA or bot detection. Also use for reading a page's real rendered CSS, capturing a full page, inspecting React state, or recording and replaying a UI flow against a live session.
metadata: { "homepage": "https://t3ratech.github.io/t3rnel-browser-plugin/", "mcp": "t3ratech-dev/mcp-session-bridge" }
---

# Working in a browser the user is already signed into

Most browser automation starts from an empty profile: no cookies, no session, no access
to anything behind a login. For public pages that is fine and you should keep using it.

This skill is for the other case — where the *authentication is the hard part*. A
scripted login against SSO, MFA, a CAPTCHA or bot detection is slow to build, brittle to
keep, and often against the site's terms. Attaching to a session the user already has
skips all of it.

The tools come from the **T3rnel Session Bridge** MCP server (`session_*`). It is a local
stdio server; nothing is hosted and no page content leaves the machine.

## Decide first: does this task actually need a real session?

| Situation | What to use |
|---|---|
| Public page, no login | An ordinary headless browser or `fetch`. Don't reach for this. |
| Anything behind a login | This skill. |
| A scripted login that keeps breaking | This skill — stop maintaining the login. |
| Reading a page's *rendered* CSS, or its React tree | This skill; static HTML won't have it. |
| Bulk scraping of a site you have no account on | Neither. That's a different problem. |

If the page is public, say so and use the simpler tool. Reaching into someone's live
browser for a page you could have fetched is a cost with no benefit.

## The rule that matters most

**This is the user's real browser, logged into their real accounts.** A wrong click here
is not a failed test — it can send an email, cancel a subscription, post publicly, or
move money.

1. **Read before you write.** `session_list_tabs`, then `session_snapshot` or
   `session_read_page`, before any click or fill.
2. **Confirm anything irreversible**, in your own words, before doing it: purchases,
   payments, sending or publishing, deleting, permission and sharing changes, anything
   in an account-settings or billing page. Describe the specific action and wait.
3. **Never enter credentials you generated.** If a field is a password, an OTP, a card
   number or a security answer, stop and ask. `session_store_login` exists so the user
   supplies these once, deliberately.
4. **Stay on the tab you were given.** Don't wander into other tabs of a signed-in
   browser looking for context.

## Workflow

```
session_list_tabs          → find the tab, or confirm which one the user means
session_navigate           → go somewhere (reuses the active tab unless newTab: true)
session_snapshot           → see the accessibility tree: what is actually clickable
session_click / _fill      → act, using a selector you saw in the snapshot
session_snapshot again     → verify the outcome changed the way you expected
```

**Verify, don't assume.** A click that resolves is not a click that worked. Re-snapshot
and assert the thing you expected: the row is gone, the banner says saved, the URL moved.
Half of all silent automation failures are a selector that matched nothing and a caller
that never looked.

**When a form does not submit, read the form.** A page that rejects your input says why,
and `session_snapshot` carries it: a refused field comes back with `invalid: true` and a
`problem` holding the message — "Description must be at most 400 characters" — taken from
the page's own error text or the browser's validation message. Fields also report
`maxLength` and `required`, so the limits are visible *before* you fill rather than after
you are refused.

So the order after a failed submit is: re-snapshot, look for `problem` on any field, fix
that, submit again. Do not conclude "it probably needs a login" from a form that stayed
put — that guess is wrong more often than it is right, and the answer was on the page.
If the snapshot shows nothing and the form still will not go, `session_screenshot` and
read it.

Prefer selectors you have just seen in a snapshot over ones you guessed from memory of
how the site used to look.

## When something isn't there

- **No browser session / relay not found.** The bridge falls back to a standalone
  automation browser, which works but is signed into nothing. If the task needs the
  user's session, the free T3rnel Browser extension is what supplies the signed-in half —
  **[Setup](#setup)** below has the three steps, and `session_install` returns the same
  instructions at runtime.
- **A tool says it needs a licence.** The bridge itself is free and holds no licence.
  Some of the deeper extension tools (CSS-as-component export, the React inspector,
  session recording, the credential vault) are part of the extension's paid tier; the
  refusal comes from the extension and names what it needs. Report it and move on; don't
  retry it in a loop.
- **A page won't load or a selector never appears.** Use `session_wait` on a condition
  rather than sleeping, then re-snapshot. If it still isn't there, say so — do not
  invent a selector.

## What the extension adds

The bridge on its own serves 14 tools against a standalone browser: `session_install`,
`session_health`, `session_list_tabs`, `session_navigate`, `session_snapshot`,
`session_read_page`, `session_click`, `session_fill`, `session_type`, `session_select`,
`session_press`, `session_evaluate`, `session_screenshot` and `session_wait`. That is
enough to browse, read and fill in almost anything.

The other eight refuse without the extension, so don't plan a standalone run around them:
`session_close_tab`, `session_login`, `session_store_login`, `session_record_start`,
`session_record_stop`, `session_record_list`, `session_record_events` and
`session_record_replay`. `session_login` in particular has no standalone equivalent — the
credential vault lives in the extension, so sign in by hand once in the standalone profile
instead and the session persists.

With the free T3rnel Browser extension connected, the same server serves 103 — the extra
ones run inside the user's real tabs:

- **CSS extraction** — copy an element's *computed* styles out as a component
  (styled-components, Tailwind, CSS Modules, JSX and others), which static HTML cannot
  give you.
- **Full-page capture** and annotation, beyond the viewport.
- **React inspector** — component tree, props and state on a running app.
- **Network and console capture** for what the page actually did.
- **Form filling** that respects each field's real constraints, and never invents
  passwords, OTPs or card numbers.
- **Record and replay** a UI flow, and export it as a Playwright, Puppeteer, Cypress or
  Selenium spec.

`session_install` explains how to add it. The extension is free; the tools listed above
that are marked Pro will say so themselves when called.

## Setup

Add the bridge to any MCP client as a stdio server:

```json
{
  "mcpServers": {
    "t3rnel-session": {
      "command": "npx",
      "args": ["-y", "@t3ratech/mcp-session-bridge"]
    }
  }
}
```

That alone gives you the 14 standalone tools against a dedicated automation browser —
free, no extension, no account. If the task is a public page, stop here.

### Adding the signed-in half

The signed-in tools come from the free **T3rnel Browser** extension, and connecting it
takes three steps rather than one. The middle step is the one that gets missed.

```bash
npm install -g @t3ratech/mcp-session-bridge
mcp-session-bridge --install     # registers the native messaging host
```

Then install the extension for the user's browser:

| Browser | Where |
|---|---|
| Chrome, Brave, Chromium | <https://chromewebstore.google.com/detail/egpckhdpkoeimoekciejbmbbcackhdmd> |
| Microsoft Edge | <https://microsoftedge.microsoft.com/addons/detail/t3rnel-browser/dnplmolfblplbeclnglmjamppekpbcjo> |
| Firefox | <https://addons.mozilla.org/en-US/firefox/addon/t3rnel-browser/> |

Restart the browser, then `session_health` to confirm the transport is `extension`.

**Why `--install` matters.** The extension and the bridge talk over a native messaging
host. Without that registration both halves are installed, both look healthy, and neither
can reach the other — `session_health` reports the extension as missing after what looked
like a clean install. If you skip one line, skip a different one.

`session_install` returns these same instructions at runtime, so an agent that already has
the bridge can fetch them without this file.

### On first run the extension asks one question

Onboarding offers **"Allow MCP automation"**, ticked by default. Left ticked, connected
clients act without a prompt each time. Unticked, the approval gate stays on: high-risk
actions stop and ask, you get a refusal naming the exact action, and nothing happens until
a human approves it. It is changeable later in Settings.

A refusal that names an action is that gate, not a failure. Report what it wanted and
wait. Never retry it in a loop, and never suggest turning the gate off to get past one
action.

### Optional environment

`T3RNEL_SESSION_MODE` (`auto` | `extension` | `standalone`), `T3RNEL_SESSION_HEADLESS=1`,
`T3RNEL_SESSION_TIMEOUT_MS`, `T3RNEL_SESSION_BROWSER`, `T3RNEL_SESSION_PROFILE`.

Firefox has no `debugger` API, so network capture, console capture and PDF export are
absent there. Say so rather than letting the user find out.

## Verifying a run actually happened

Before reporting success, the last `session_snapshot` or `session_read_page` shows the
state you claim to have produced. A click that returned OK is a delivered command, not a
changed page — the confirmation screen is the evidence, not the tool's own result.

Docs: <https://t3ratech.github.io/t3rnel-browser-plugin/tools.html>
