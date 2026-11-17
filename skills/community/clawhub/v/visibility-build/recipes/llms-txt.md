---
id: llms-txt
kind: asset
unlocks: [fern-agent-score]
source: https://llmstxt.org/, https://raw.githubusercontent.com/philip/afdocs/main/README.md (loaded 2026-11-08)
---
## Smallest version
A `/llms.txt` at the docs root that lists every existing docs page as a markdown link with a one-line note, plus a `.md` copy of each page at the same URL. Generated from the docs source at build time; no new content.

## Scaffold
No official generator on llmstxt.org. If the docs are already markdown, a build step copies each source file to `<page>.md` next to the HTML and writes llms.txt from the nav/sidebar config.

## Fields the listings check
- llms.txt (llmstxt.org), in order: optional BOM; H1 project/site name (the only required section); blockquote short summary; zero or more non-heading markdown sections; zero or more H2 sections of file lists, each entry `[name](url)` optionally followed by `: notes`. An H2 `Optional` section holds links an agent can skip.
- Location: `/llms.txt` at the site root or any subpath (a file covers pages under its path).
- Markdown mirror: same URL with `.md` appended (`page.html.md`) or extension replaced (`page.md`); for directory URLs `index.html.md` or `index.md`.
- afdocs (powers Fern Agent Score; 0.x, check IDs may change): check IDs `llms-txt-exists`, `llms-txt-size`, `llms-txt-directive-html`; a "Markdown Availability" category ("Your site serves markdown at .md URLs"). README example warns at 65,000 characters and suggests splitting into nested llms.txt files. Content-negotiation and link-resolution checks were seen only in a search summary (unconfirmed).

## Steps
claude: read the docs nav config; write the build step that emits `<page>.md` for every page and `llms.txt` (H1, blockquote, H2 groups mirroring the nav, `Optional` for changelog/legacy)
claude: if llms.txt nears 65k chars, split per section into nested llms.txt files and link them
claude: run afdocs against a preview deploy and fix failures
approve: deploy the docs
human: buildwithfern.com/agent-score -> score the docs URL; optionally request listing

## Verify locally
`npx afdocs@0.23.0 check https://<docs-preview-url> --format scorecard` (Node 22+); `curl -sI https://<docs>/llms.txt` returns 200 and `curl https://<docs>/<page>.md` returns markdown.
