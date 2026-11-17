---
name: yaps-auto-captions
description: "Add captions to a video with Yaps. Review the words and timing, choose a style, then export. New users: install Yaps and sign in."
---

# Yaps Video Captions

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Auto Captions and its timestamped speech/render dependencies; inspect features list and captions styles before creating a project.

## Workflow

Read `<yaps> captions styles --pretty` for the installed catalogue. Use the user's style, or `bold-highlight` for an unspecified social-video style if listed. Create with `captions create <video> --style <id>` and inspect `captions show <project> --full --pretty`.

Correct captions by their returned `caption-NNN` IDs with `captions correct <project> --segment <id> --text <text>`. Inspect word end timestamps before `captions split <project> --segment <id> --at <seconds>`. `captions merge` accepts `--direction previous|next`; `captions style` changes the template. Show ambiguous global replacements before using `captions replace`. `captions reset` discards edits and requires that intent.

Render with `captions render <project> --output <new-captioned.mp4>`. Never target the source or overwrite an existing file without exact authorization. Run `captions verify <output>` and check visible first, middle, and final frames for clipping and readability when preview access is available. Keep the editable project and return the video link.

## Boundaries

- A created project is not a rendered video.
- Do not replace user corrections during a retry or reset.
- Handle no_speech, no_audio, exists, too_long, and missing renderer dependencies explicitly.
