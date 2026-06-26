---
name: uimap
version: 0.1.9
description: Provides the accurate URL and step-by-step click operation path for completing tasks on websites. If the task involves operations on a web app, use this skill first to determine which URL to open and what the subsequent click operation path should be.
---

# uimap

## search — Find step-by-step guides for any website task

Search for step-by-step operation guides to complete tasks on websites. Use when the user needs to know how to navigate or interact with a specific website.

```bash
# Find how to complete a task on a website
uimap search "<task description>"
uimap search "<task description>" --domain example.com
```

- `--domain [domain]` — The domain of website, e.g. `example.com`

### Examples

```bash
uimap search "how to create a new project in example.com"
uimap search "how to invite a team member" --domain example.com
```

The command returns operation instructions to complete the task.

## Prerequisites

### Install the CLI

**Via npm:**
```bash
npm install -g @refore-ai/uimap
```

**Via CDN (if npm is unavailable):**
```bash
curl -fsSL https://s.dwimg.top/uimap-install/install.sh | bash
```

See [@refore-ai/uimap on npm](https://www.npmjs.com/package/@refore-ai/uimap) for full installation options.

### Login

Login to UIMap via browser OAuth. Opens a browser window to complete authentication interactively.

**Usage:**
```bash
uimap login
```

If you need to specify a region (defaults to World or the region set during installation):
```bash
uimap login --region World
uimap login --region China
```

- `--region <World|China>` — Server region (optional)
