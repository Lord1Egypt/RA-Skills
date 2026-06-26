# X to Notebook

Push your X/Twitter bookmarks into Google NotebookLM notebooks as URL sources.

## Requirements

- [twikit](https://github.com/d60/twikit) — X bookmarks fetcher
- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — NotebookLM MCP server

## Setup

1. Install twikit:
   ```bash
   cd ~/.openclaw && uv add twikit
   ```

2. Export X cookies (one-time):
   - Install Cookie-Editor browser extension
   - Go to x.com while logged in
   - Export cookies as JSON to `~/.openclaw/credentials/x-cookies.json`

3. Install Google Chrome (for persistent auth):
   ```bash
   # Download and install
   curl -fsSL -o /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo dpkg -i /tmp/google-chrome.deb && sudo apt -f install -y
   ```

4. Install and auth NotebookLM MCP:
   ```bash
   uv tool install notebooklm-mcp-cli
   nlm login  # Opens Chrome, log in to Google once
   ```

5. Register the MCP server in mcporter:
   ```bash
   mcporter config add notebooklm --command "notebooklm-mcp"
   ```

## Usage

- "push my bookmarks" — auto-routes by folder
- "send my X bookmarks to NotebookLM" — same flow
- "sync bookmarks to notebook" — same flow

Bookmarks are matched to NotebookLM notebooks by folder name (case-insensitive). Unmatched folders prompt you to pick or create a notebook.

## Install

```bash
clawhub install spideystreet/x-to-notebook
```
