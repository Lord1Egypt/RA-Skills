---
name: research-assistant
description: Auto-enrich Bear research notes tagged 「待整理」 with topic-matched GIFs. Reads notes via grizzly, searches GIFs via gifgrep, appends media, and removes the tag. Use when the user wants to batch-process or tidy up research notes in Bear.
version: 0.1.0
author: ClawdBot
tags: [research, bear, gif, productivity]
metadata:
  openclaw:
    requires:
      bins: [grizzly]
      skills: [bear-notes, gifgrep]
    install:
      - id: go
        kind: go
        module: github.com/tylerwince/grizzly/cmd/grizzly@latest
        bins: [grizzly]
        label: Install grizzly (go)
---

# Research Assistant

Batch-process Bear notes tagged 「待整理」: find a relevant GIF for each note, append it, then remove the tag.

## Prerequisites

- Bear running + grizzly installed + token at `~/.config/grizzly/token`
- gifgrep skill available

## Workflow

1. **Fetch tagged notes**
   ```bash
   grizzly open-tag --name "待整理" --enable-callback --json --token-file ~/.config/grizzly/token
   ```
   Parse the JSON to get note IDs and titles/summaries.

2. **For each note:**
   a. **Read full content**
      ```bash
      grizzly open-note --id "$NOTE_ID" --enable-callback --json
      ```
   b. **Derive a GIF search query** — extract 2–3 keywords from the note title or key findings. Prefer concrete nouns and verbs over abstract terms.
   c. **Search for a GIF** using the gifgrep skill (or `web_search` + `web_fetch` as fallback) with the derived query.
   d. **Append the GIF** to the note under a `## Supporting Media` heading:
      ```bash
      printf '\n## Supporting Media\n\n![%s](%s)\n' "$ALT_TEXT" "$GIF_URL" \
        | grizzly add-text --id "$NOTE_ID" --mode append --token-file ~/.config/grizzly/token
      ```
   e. **Remove the 「待整理」 tag** — replace note content with the tag removed, or use Bear's tag API:
      ```bash
      grizzly create --title "$TITLE" --tag "$OTHER_TAGS" < /dev/null
      # Then delete the old note if needed, or strip the tag from content
      ```
      Simplest approach: append a line that re-tags the note (Bear removes a tag when it's deleted from the note body). Use `sed` on the note content to strip `#待整理` and re-write via `grizzly add-text --mode replace`.

3. **Report** — list processed notes and any failures.

## Script

For batch runs, use `scripts/process_tagged.sh`:

```bash
bash scripts/process_tagged.sh
```

The script reads all notes tagged 「待整理」, extracts keywords, and calls the gifgrep search endpoint. It appends the top GIF result and strips the tag.

## Notes

- If no GIF matches, skip the note and log it — don't force irrelevant results.
- Rate-limit Bear API calls (1–2 req/s) to avoid callback timeouts.
- The script is a convenience wrapper; the agent can also drive the workflow step-by-step for more control.
