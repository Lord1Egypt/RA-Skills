---
name: yaps-translation
description: "Translate text or subtitle files with Yaps. Keep the original and preserve subtitle timing. New users: install Yaps and sign in."
---

# Yaps Translation

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Translation Standard or Extended. Query translate --list-languages for each engine's installed languages and reduced-quality flags; use current reported download sizes.

## Workflow

Run `<yaps> translate --list-languages --pretty` before promising a language. Respect `installed`, language codes, and any `reduced_quality` warning. If the required language needs a missing engine, explain the reported model/download and get authorization before `features translation standard|extended --enable`.

Translate a file with `translate <input.md|txt|srt> --to <code> --output <new-file> --pretty`, or supplied short text with `translate --text <text> --to <code>`. Use `--from` if source detection is wrong or uncertain. Leave `--engine auto` unless the user requests `gemmax2` (Standard) or `translategemma` (Extended).

Default file naming is `<stem>.<language>.<extension>`; check collisions and preserve the source. For SRT, compare every cue index and timestamp line before/after; only spoken text should change. For Markdown, inspect headings, links, code, and list structure. Return the file and stated language/engine. Local translation inference does not mean agent usage is free or that text shown to the agent stays outside its context.

## Boundaries

- No silent hosted translation fallback.
- Do not promise a language outside the installed catalogue or suppress quality limitations.
- Do not reinterpret a request to translate as permission to rewrite the meaning or publish the result.
