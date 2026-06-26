# Super Lobster

Use this skill when tasks require aggressive web research, browser rendering, local scripting, crawling, extraction, and command execution on this gateway.

## Operating model
- This host is in a China network environment. Do not assume western search engines or API endpoints are reachable or stable.
- Prefer first-party sites, direct URLs, mirrors, and browser rendering over public search APIs.
- Prefer local execution on the gateway for scraping, parsing, coding, and automation.

## Default workflow
1. If a direct URL is known, fetch it with `fetch_url.py`.
2. If only the readable article body matters, use `extract_main_text.py`.
3. If the page is JS-heavy or renders differently in browsers, use `render_url.py` or `chrome_dump_dom.sh`.
4. If you need to discover more pages inside the same site, use `crawl_site.py`.
5. For multi-step processing, write a Python script under `/root/.openclaw/workspace/memory/tmp` and run it.

## Tools
- `/root/.openclaw/workspace/skills/super-lobster/bin/fetch_url.py <url>`
  Returns metadata plus a text and HTML preview.
- `/root/.openclaw/workspace/skills/super-lobster/bin/extract_main_text.py <url>`
  Extracts the readable main content.
- `/root/.openclaw/workspace/skills/super-lobster/bin/chrome_dump_dom.sh <url>`
  Dumps browser-rendered DOM with Chrome headless.
- `/root/.openclaw/workspace/skills/super-lobster/bin/render_url.py <url>`
  Python wrapper around Chrome headless DOM rendering.
- `/root/.openclaw/workspace/skills/super-lobster/bin/crawl_site.py <url> --limit 20`
  Same-site link discovery crawl.

## Browser rules
- Prefer `fetch_url.py` or `extract_main_text.py` first for static pages.
- Use browser rendering only when static fetch is incomplete or JS-dependent.
- Do not depend on OpenClaw's built-in browser RPC in this environment unless explicitly verified working in the current session.

## Coding and execution rules
- You may write and execute Python or shell programs locally on the gateway.
- Prefer Python for scraping, parsing, and data cleanup.
- Keep scratch outputs in `/root/.openclaw/workspace/memory/tmp`.
- Remove clearly temporary files after use unless they are likely to be reused.

## Network rules
- Avoid default reliance on DuckDuckGo, Tavily, Exa, or similar public search providers unless reachability is verified first.
- If provider keys are added later and connectivity is stable, treat them as accelerators, not hard dependencies.
