---
name: shotlane
description: Screenshot any public web page, read pages as clean Markdown (JavaScript rendered), and render HTML or URLs to PDF using the Shotlane API. Use when the user wants to see what a website looks like, check a deployed page or layout on desktop/mobile, capture a page or element as an image, extract an article or docs page as text for analysis, or produce a PDF (invoices, reports) from HTML.
metadata:
  openclaw:
    primaryEnv: SHOTLANE_API_KEY
    envVars:
      - name: SHOTLANE_API_KEY
        required: false
        description: Shotlane API key, free at https://shotlane.dev/signup.
    requires:
      anyBins: [curl, python3]
    homepage: https://shotlane.dev
---

# Shotlane: screenshots, page reading and PDFs

Shotlane renders pages in a real Chromium browser, so JavaScript-heavy sites (React, Next.js, docs portals) work. Every successful call costs the user 1 credit; failed calls are free.

## Choosing the right operation

| User wants… | Use | Notes |
|---|---|---|
| To *see* a page, check a design/layout, compare desktop vs mobile, spot visual bugs | **screenshot** | Default viewport 1280×800. Add `full_page` for the whole page. |
| The *text/content* of a page (summarize, quote, answer questions, extract data) | **read** (Markdown) | Much cheaper in tokens than a screenshot. Prefer this for anything text-based. |
| A PDF document (invoice, report, printable page) | **pdf** | Pass complete HTML, or a URL. |

If you already have a text fetch or web search tool, keep using it for reading; use Shotlane's screenshot when the question is about how a page looks.

If MCP tools named `screenshot`, `read_page` and `html_to_pdf` are available, call them directly.

## No key yet

- **Try without a key:** fetch `https://shotlane.dev/md/<url>` for Markdown or `https://shotlane.dev/shot/<url>` for a PNG screenshot,
  e.g. `curl https://shotlane.dev/md/https://react.dev/learn`. Limited to 5 requests per IP per day.
- **Get a key without a browser:** ask the user which email address to use (don't invent one), then
  `curl -X POST https://shotlane.dev/v1/signup -H 'content-type: application/json' -d '{"email": "USER_EMAIL"}'`.
  The response has a `claim_token` and a `code`. Tell the user to open the link Shotlane emailed them and type the code.
  Then poll `curl -X POST https://shotlane.dev/v1/signup/claim -H 'content-type: application/json' -d '{"claim_token": "CLAIM_TOKEN"}'`
  every 10 seconds: 202 means still waiting, 200 returns `api_key` once (100 free credits, topped up to 100 every month).
  Still 202 after 15 minutes: stop polling and ask the user to check their inbox and spam. If the address already has an account,
  the email has a login link instead and the key is at https://shotlane.dev/dashboard/keys. A 410 means the signup expired.
  Store the key as `SHOTLANE_API_KEY`.
  With a key, the same `/md/` and `/shot/` URLs work without the daily limit when you send `Authorization: Bearer <key>`.
- **Connect as an MCP server** (sign-in happens in the browser via OAuth):
  - Claude Code: `claude mcp add --transport http shotlane https://shotlane.dev/mcp`
  - Cursor / VS Code / others: add an HTTP MCP server with URL `https://shotlane.dev/mcp`

## Using the bundled script

Needs `SHOTLANE_API_KEY`:

```bash
python scripts/shotlane.py screenshot https://example.com --full-page --out page.png
python scripts/shotlane.py screenshot https://example.com --device iphone --out mobile.png
python scripts/shotlane.py read https://example.com/blog/post > post.md
python scripts/shotlane.py pdf --html invoice.html --paper Letter --out invoice.pdf
```

## Tips that avoid wasted calls

- **Mobile layouts:** use device `iphone` (393 px) or `ipad`; widths ≤ 480 px get a mobile user agent automatically.
- **One element only:** pass a CSS `selector` (e.g. `main`, `#pricing`, `.chart`) instead of a full-page capture.
- **Content loads late** (charts, animations, lazy SPAs): add `delay` (ms, e.g. 1500) or `wait_for_selector`.
- **Cookie banners and ads** are hidden automatically by the MCP tools; with the script use `--clean`.
- **Long pages:** `read` returns the main article by default; use `--whole-page` (`main_content=false`) for navigation-heavy pages like listings or forums.
- **Errors:** `401` = missing/invalid key, `402` = out of credits: when the error message has a top-up link (a Shotlane page that opens Stripe checkout for this account; nothing is charged until the user pays), give the user that link instead of opening it yourself; otherwise, or for other amounts, https://shotlane.dev/pricing, and free credits top up to 100 at the start of every month (UTC), `422` = the page could not be loaded (site down, blocked, or selector not found). Only public URLs work — private/internal addresses are refused.
- Do not loop over many URLs one by one for large batches: use POST https://shotlane.dev/v1/bulk (up to 500 URLs, poll GET /v1/bulk/{id}, download the ZIP) or the bulk page, https://shotlane.dev/bulk.

## API reference

Full docs: https://shotlane.dev/docs · For agents: https://shotlane.dev/llms-full.txt
