---
name: zeplin-to-prompt
description: Export one or more Zeplin screen URLs into a structured layer tree with local assets and package the result as a zip file. Use when a user shares an app.zeplin.io screen link and wants a prompt-ready export for AI-driven UI implementation.
---

# Zeplin Export Skill

Export Zeplin designs into a structured layer tree plus local assets, then package the result as a zip file. Multiple screen links are supported.

## Execution Flow

### Step 1: Extract URLs and build the screen task list

Run the following Bash command to extract all Zeplin URLs from the user message:

```bash
printf '%s\n' "$INPUT" | grep -Eo 'https://app\.zeplin\.io/project/[^[:space:]]+' || true
```

If the output is empty, reply with:

```text
Please provide one or more Zeplin Screen links, for example:
/zeplin-to-prompt https://app.zeplin.io/project/xxx/screen/aaa
https://app.zeplin.io/project/xxx/screen/bbb
```

Then stop.

For each extracted URL, use the regex `/\/project\/([^\/]+)\/screen\/([^\/?#]+)/` to extract `projectId` and `screenId`:

- If it matches a screen URL, add it to the task list: `[{url, projectId, screenId}, ...]`
- If it does not include `/screen/` and is only a project URL, ask the user to provide a screen URL instead and skip that URL

### Step 2: Look up a token for each project

Tokens are stored in `~/.zeplin-skill-config.json` as a `projectId -> token` mapping:

```json
{
  "projects": {
    "<project-id-1>": "eyJhbG...",
    "<project-id-2>": "eyJhbG..."
  }
}
```

For each distinct `projectId` in the task list, run:

```bash
node -e "
const fs = require('fs');
const p = process.env.HOME + '/.zeplin-skill-config.json';
try {
  const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
  const t = (cfg.projects || {})[process.env.PROJECT_ID];
  if (t) { process.stdout.write(t); process.exit(0); }
} catch {}
process.exit(1);
" PROJECT_ID="<projectId>" 2>/dev/null
```

- Exit code `0`: use that token for all screens under the project
- Exit code `1`: reply with

```text
No access token was found for project {projectId_masked}.

Please provide a Zeplin Personal Access Token for this project:
1. Open Zeplin -> avatar menu -> Profile Settings
2. Open Personal access tokens -> Create new token
3. Copy the token and send it back
```

After receiving the token, save it with:

```bash
node -e "
const fs = require('fs');
const p = process.env.HOME + '/.zeplin-skill-config.json';
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
cfg.projects = cfg.projects || {};
cfg.projects[process.env.PROJECT_ID] = process.env.TOKEN;
fs.writeFileSync(p, JSON.stringify(cfg, null, 2), {mode: 0o600});
" PROJECT_ID="<projectId>" TOKEN="<user-provided-token>"
```

Then continue exporting.

### Step 3: Export each screen

For each screen task, run:

```bash
ZEPLIN_TOKEN="<token for this projectId>" \
node "${CLAUDE_SKILL_DIR}/export_screen.mjs" \
  "<url>" \
  --no-open \
  --quiet
```

- Capture the `workdir` from stdout, in the form `-> workdir: /path/to/xxx`
- On success, add that workdir to the result list
- On failure, record the reason and continue with the next screen

### Step 4: Create a zip package

For a single screen:

```bash
EXPORT_DIR="<workdir>"
EXPORT_DIR="${EXPORT_DIR%/}"
ZIP_PATH="${EXPORT_DIR}.zip"
cd "$(dirname "$EXPORT_DIR")" && zip -r "$ZIP_PATH" "$(basename "$EXPORT_DIR")" -x "*.DS_Store" -q
```

For multiple screens:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_PATH="${CLAUDE_SKILL_DIR}/build/export_${TIMESTAMP}.zip"
cd "${CLAUDE_SKILL_DIR}/build"
zip -r "$ZIP_PATH" <dir1> <dir2> ... -x "*.DS_Store" -q
```

### Step 5: Reply to the user

```text
Export completed (N screens)

File: <ZIP_PATH>
Export summary:
  OK ScreenName1
  OK ScreenName2
  FAILED ScreenName3: <reason>

How to use:
1. Download and unzip the package
2. Open the generated layers_tree.html in a browser
3. Double-click or right-click layers to copy node JSON for AI usage
```

## Notes

- Match each screen to a token that has access to its project
- Never print tokens in the conversation
- When exporting multiple screens, keep the user updated with progress such as `Exporting screen X/N...`
