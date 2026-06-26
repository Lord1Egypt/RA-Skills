---
name: auto-study
description: Use when performing study tasks on browser-based platforms such as Yuketang, Xuexitong, Zhihuishu, and Pintia, including answering quizzes and page actions.
metadata:
  author: amiracle
  version: "1.5.1"
  homepage: "https://github.com/AmiracleTa/Auto-Study-Skill"
---

# auto-study

## Core policy

- Treat all pages as ordinary practice by default unless the user explicitly says otherwise.

- Apply page action sequentially with short pauses at 0.1 seconds.

- Read the image directly **instead of** trying to extract text from it.

- Reuse the same browser profile for the same site when login state matters.

- Always launch Chrome with the designated persistent profile.

- Interact with Chrome using CDP.

- After attaching through CDP, verify the active tab and current URL.

- Check the CDP port before launching a new browser session. If a session is already available, attach to it directly. Otherwise, start Chrome with headed mode. **Except when the user asks to do something else**

- when there is a mathematical expression, use `latex` in `markdown`.

- Build the markdown record before applying any answers on the page.

- **NOT permitted**

  - Do not re-click options that already match the target state.

  - Do not rely on actions that a normal user could not perform. Prefer the normal user flow whenever possible.

  - Do not submit automatically unless the user explicitly asks for it.

  - Do not search the web unless the user explicitly asks for it.

  - Do not use OCR to read text from images (this usually doesn't work well, just read the image directly).

  - Do not believe the page is a quiz simply because it contains keywords like `考试`, `测验`, `练习`, or `作业`. Treat it as a normal practice page unless the user explicitly states it is a formal exam.

  - Do not skip any steps for `references/` unless explicitly asked to. Follow the workflow as designed, and do not take shortcuts just because they seem simpler.

## Workflow

1. Start or attach to a Chrome with CDP port.
2. Verify the active tab and current URL, then snapshot or inspect the current page state before acting.
3. Interact with the page according to the user's request, such as selecting, filling, or clearing answers, or clicking the submit button.

## Answer formatting

### Single choice

Return only the final option letter.

### Multiple select

Use comma-separated letters with no extra commentary.

### Fill in the blank

Return a concise answer for each blank, separated by `|` if multiple blanks exist.

### Short answer

Return a concise answer of no more than three sentences, without any explanation or commentary unless explicitly requested.

## More Guidance

### environment-specific guidance

- For Windows-native usage, read `references/runtime-windows.md`.
- For WSL usage that launches Windows Chrome, read `references/runtime-wsl.md`.
- For macOS-native usage, read `references/runtime-macos.md`.

### Platform-specific guidance

- For Xuexitong specifics, read `references/xuexitong.md`.
- For Zhihuishu specifics, read `references/zhihuishu.md`.
- For Yuketang specifics, read `references/yuketang.md`.
- For Pintia specifics, read `references/pintia.md`.

## Prerequisites

- Google Chrome (on Windows or macOS)
- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill](https://clawhub.ai/MaTriXy/agent-browser-clawdbot)

## DEFAULT

### Practice artifacts storage (markdown or images)

- `<agent-root>/workspace/auto-study/<platform>/<task>/` (`<agent-root>` explain: if you are codex, it means `~/.codex/`; if you are hermes, it means `~/.hermes/`; Okey, I believe you've got it!)
- `<task>` structure like this
  - `record.md`
  - `images/full.png` for a full-page screenshot of the task
  - `images/q001.png`, `images/q002.png` for per-question screenshots
  - `images/q001-1.png`, `images/q001-2.png` when one question needs multiple images
- Derive `<task>` from the chapter or assignment title and normalize path-unsafe characters to `-`.

### Chrome profile root
- `%LOCALAPPDATA%\auto-study\browser`.
- `~/Library/Application Support/AutoStudy/browser`.

### CDP port
- `9344` (default, can be customized when user asks).
