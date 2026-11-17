# Webstudio Verification

Verify everything with DOM measurements and text output - **no images into the
model**. The canvas renders only the selected page; it is an `<iframe>` whose URL
contains `/canvas`. All measurement happens inside that frame.

## Core canvas checks

```js
const frame = page.frames().find(f => f.url().includes('/canvas'))
const out = await frame.evaluate(() => {
  const doc = document, b = doc.body
  return {
    overflowX: doc.documentElement.scrollWidth - doc.documentElement.clientWidth,
    overflowY: doc.documentElement.scrollHeight - doc.documentElement.clientHeight,
    bodyBg: getComputedStyle(b).backgroundColor,
    totalEls: b.querySelectorAll('*').length,
    bodyChildren: [...b.children].map(el => ({ tag: el.tagName, txt: (el.textContent||'').trim().slice(0,24) })),
    inlineStyleCount: document.querySelectorAll('[style]').length,
  }
})
```

- **Overflow** (scrollWidth - clientWidth / scrollHeight - clientHeight) > 0 means
  content is escaping the viewport. Fix before showing.
- **Inline styles** on elements usually mean a manual style leaked in instead of a
  proper style row.
- **Element count + children** confirm the tree built correctly.

## Full-page audit (Playwright pattern)

A reusable Playwright full-page audit pattern (no bundled script - build it from
this). It:
1. Launches Chrome (Playwright), logs in via "Login with Secret".
2. Opens the editor at `http://p-<projectId>.localhost:3000/`.
3. For each target page, switches via the `[aria-label="Toggle pages"]` control and
   measures the canvas DOM (overflow, bg, element counts, inline styles).

Page names come from the native `pages` column of the draft build (see the script);
the project id is resolved from the native `Project` table, so nothing is hardcoded.

## Navigation / switching pages in the canvas

The canvas shows one page at a time. To switch:
- Click the `[aria-label="Toggle pages"]` button.
- Click the target page by exact text (find a leaf node whose trimmed text equals the
  page name, then click its closest `[role="button"]`,`button`,`a`,`[role="menuitem"]`).

Give the canvas time to re-render between switches (wait several seconds after
navigating and after each page change).

## Authenticated browser verification

Prefer an already-authenticated browser session or a dedicated low-privilege automation identity.
Do not search for credentials or read `.env` automatically.

If secret login is required, get explicit approval and use `AUTH_SECRET` only through the
operator's approved secret manager or an ephemeral environment injection. Fill the login form
without printing, logging, persisting, screenshotting, or returning the value. Remove the injected
value after the session. See `security.md`.

An approved Playwright run may consume a task-specific process variable; it must not open or parse
the deployment `.env` file:

```js
const secret = process.env.WEBSTUDIO_LOGIN_SECRET
if (!secret) throw new Error("approved Webstudio login secret was not injected")
try {
  await page.goto(builderUrl)
  await page.getByRole("button", { name: "Login with Secret" }).click()
  await page.getByPlaceholder("Auth secret").fill(secret)
  await page.getByRole("button", { name: /log in|continue/i }).click()
} finally {
  delete process.env.WEBSTUDIO_LOGIN_SECRET
}
```

The operator or secret broker injects `WEBSTUDIO_LOGIN_SECRET` only for that process. Do not echo
the environment, enable shell tracing, record the login form, or preserve the variable in a service
definition. Prefer OAuth or a dedicated automation identity when the deployment supports one.

After login, the editor holds auth cookies (`_csrf`, session). Use the browser's own
`fetch` for any in-page API/tRPC calls so cookies/CSRF are handled automatically.

## Rendering decks / other content for verification

For PowerPoint / other visual work, render to PDF with LibreOffice then OCR the page
for text grounding - still no images into the model:

```bash
/opt/homebrew/bin/soffice --headless --convert-to pdf --outdir _render file.pptx
pdftoppm -f <page> -l <page> -r 200 -png out.pdf pg
tesseract pg-<page>.png stdout
```

## Verification rules

- **Verify before showing.** Never hand over un-verified work.
- **One logical thing per check.** Isolate what you're testing.
- **Text-only evidence.** DOM numbers, computed styles, OCR text. No screenshots into
  the model unless CB asks to see something.
- **Check all breakpoints** on responsive work (Base, tablet, mobile-landscape,
  mobile-portrait).
