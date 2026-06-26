# Tooling Reference

CLI tools that extend the LLM's capabilities when working with a second-brain vault.

## Required

### Obsidian Web Clipper

Browser extension that saves web articles as clean markdown files directly into your vault's `raw/` directory.

- **Install:** Chrome Web Store — https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf
- **Setup:** After installing, configure the default vault location to point to your vault's `raw/` directory
- **Why required:** This is the primary way to feed source material into the vault without manual copy-paste

## Optional (Recommended)

### summarize

Summarize turns links, files, and media into sharp summaries with a real extraction pipeline. Use the CLI for automation or the Chrome Side Panel for one-click summaries.

- **Install:** `npm i -g @steipete/summarize`
- **Verify:** `summarize --version`
- **Usage:** `summarize --help` for full feature list
- **When to use:** Summarizing web pages, PDFs, videos, or any media before or during ingestion

### qmd

QMD (Query Markup Documents) is a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device.

- **Install:** `npm i -g @tobilu/qmd`
- **Verify:** `qmd --version`
- **Usage:** `qmd --help` for full feature list
- **When to use:** When the wiki grows beyond what `wiki/index.md` can efficiently navigate (~100+ pages)

### agent-browser

Browser automation CLI for AI agents. Fast native Rust CLI. Use for web research and scraping when native web_search, web_fetch, or computer use tools fail.

- **Install:** `npm i -g agent-browser && agent-browser install`
- **Verify:** `agent-browser --version`
- **Usage:** `agent-browser --help` for full feature list
- **When to use:** Web research tasks where built-in tools fail or return incomplete results
