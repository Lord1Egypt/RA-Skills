---
name: research-assistant
description: Read Bear notes tagged "待整理", extract topic keywords, search for relevant GIFs via gifgrep, insert them into the note, and remove the tag. Use when the user wants to auto-illustrate or finalize research notes from Bear.
version: 0.1.0
author: ClawdBot
tags: [research, bear, gif, automation]
metadata:
  openclaw:
    requires:
      bins: ["grizzly"]
---

# Research Assistant

Automate the workflow of enriching Bear research notes with topical GIFs.

## Prerequisites

- Bear app running with a valid API token (`~/.config/grizzly/token`)
- `grizzly` CLI installed
- gifgrep skill available (for GIF search)

## Workflow

1. **Fetch notes** — List all notes with the `待整理` tag:
   ```bash
   grizzly open-tag --name "待整理" --enable-callback --json --token-file ~/.config/grizzly/token
   ```

2. **For each note:**
   a. Read the note content via `grizzly open-note --id <ID> --enable-callback --json`.
   b. Extract 2–3 topic keywords from the title and key-findings sections.
   c. Search for a relevant GIF using gifgrep (or `web_search` + `web_fetch` for a GIF URL) with those keywords.
   d. Append the GIF as markdown to the note's "Supporting Media" section:
      ```bash
      echo '![topic](GIF_URL)' | grizzly add-text --id <ID> --mode append --token-file ~/.config/grizzly/token
      ```
   e. Remove the `待整理` tag by replacing tags (exclude `待整理`, keep all others).

3. **Report** — Summarize which notes were processed and how many GIFs were inserted.

## Notes

- If a note already has content in "Supporting Media", insert the GIF on a new line below existing media.
- If no relevant GIF is found, skip insertion and note it in the report.
- Prefer GIFs that visually represent the research topic (e.g., data visualization, concept animation).
- The `待整理` tag signals "needs processing"; removing it marks the note as finalized.
