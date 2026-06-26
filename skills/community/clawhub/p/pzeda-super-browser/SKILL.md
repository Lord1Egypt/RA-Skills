---
name: super-browser
description: Browser automation through the published `@pzeda/super-browser` package and its `super-browser` CLI against a real local Chrome session. Use when the task needs to open a webpage, inspect rendered content, click through a real site flow, reuse an existing Chrome login session, upload files, take screenshots, inspect network requests, or drive browser decisions and crawls.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
---

# super-browser Skill

Use the published `@pzeda/super-browser` package. Do not rely on repository-only scripts or `src/` paths when performing browser work through this skill.

## Setup

Require:

- Node.js 22+
- Chrome or Chromium installed locally
- A Chrome session that can expose CDP on port `9222`

Install the package:

```bash
npm install -g @pzeda/super-browser
```

This installs the executable as:

```bash
super-browser
```

Check that the CLI is available:

```bash
super-browser --version
```

If a global install is not appropriate, use:

```bash
npx -y @pzeda/super-browser --help
```

## When To Use

Use this skill when the task needs a real browser session at all, especially for:

- opening a website or visiting a URL
- clicking, searching, paginating, or filling a browser flow
- inspecting what a page actually renders in Chrome
- reusing the user's logged-in Chrome session
- uploading files or taking screenshots in a browser
- inspecting browser-side network requests
- collecting structured page state for a decision-making workflow

## Standard Rule

Do not lead with daemon management in the normal path.

For ordinary browser tasks, run the browser command you need directly, for example:

```bash
super-browser new --url https://example.com
```

The CLI auto-starts and reuses the daemon in the background.

Only switch into explicit connection diagnosis when browser commands fail or when `browserConnected` is reported as `false`.

Preferred diagnosis entrypoint:

```bash
super-browser doctor
```

Use `super-browser daemon status` only as an advanced status check.

## Core Workflow

When the task needs to use the browser, follow this order:

1. Ensure `super-browser` is available.
2. Run the actual browser command you need. Let the CLI auto-start the daemon.
3. If browser connection fails, run `super-browser doctor`.
4. Create and use a dedicated task tab.
5. Reuse the returned `pageId` for later commands.
6. Prefer structured commands over ad hoc browser scripts.

Create a task tab:

```bash
super-browser new --url https://example.com
```

Navigate:

```bash
super-browser navigate --page <pageId> --url https://example.com/search?q=phone
```

Inspect page state:

```bash
super-browser page-state --page <pageId>
```

List managed tabs:

```bash
super-browser pages
```

Close the task tab:

```bash
super-browser close --page <pageId>
```

## Common Commands

Basic page operations:

```bash
super-browser info --page <pageId>
super-browser click --page <pageId> "button.search"
super-browser click-real --page <pageId> "input[type=file]"
super-browser scroll --page <pageId> --direction down --distance 3000
super-browser screenshot --page <pageId> --file D:\\temp\\shot.png
super-browser upload --page <pageId> --selector "input[type=file]" --files D:\\tmp\\a.pdf D:\\tmp\\b.pdf
```

Network inspection:

```bash
super-browser network start --page <pageId>
super-browser network requests --page <pageId> --business
super-browser network patterns --page <pageId>
super-browser network stop --page <pageId>
```

Decision workflow:

```bash
super-browser decision candidates --page <pageId> --intent search --target "iphone"
super-browser decision propose --page <pageId> --intent search --target "iphone"
super-browser decision context --page <pageId> --intent search --target "iphone"
super-browser decision render --page <pageId> --intent search --target "iphone"
super-browser decision execute --page <pageId> --intent search --target "iphone"
```
