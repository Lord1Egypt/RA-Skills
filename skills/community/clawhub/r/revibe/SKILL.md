---
name: revibe
description: Analyze any codebase — architecture, patterns, diagrams, agent context. Understand repos in minutes, not hours.
emoji: 🔍
user_invocable: true
homepage: https://www.revibe.codes
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq", "git"], "env": ["REVIBE_API_KEY"], "config": []}, "primaryEnv": "REVIBE_API_KEY"}}
---

## Purpose

Analyze codebases to understand architecture, file roles, design patterns, execution flows, and system design decisions. Returns structured insights inline and saves `agent_context.json` for persistent codebase understanding.

**Revibe** turns any GitHub repository into a complete architecture map — modules, dependencies, call chains, design decisions — in about 2 minutes.

## When to Use

- User asks to "analyze", "understand", or "explain" a codebase or repository
- User clones or forks a new repo and wants to understand it quickly
- User says "what does this project do" or "how is this structured"
- User asks about architecture, patterns, or design decisions of a repo
- Another skill needs codebase context to work effectively (use agent mode)

## Requirements

- **REVIBE_API_KEY** (required): API key for authentication. Free signup at https://app.revibe.codes → Settings → API Keys. Format: `rk_live_xxxxx`. Sent as `X-Revibe-Key` header.

## Privacy Note

This skill sends your repository's GitHub URL to revibe.codes for analysis. Source code is stored securely in Google Cloud Storage to enable features like code exploration and re-analysis. Only you can access your uploaded projects. If you're working with private or sensitive repositories, review revibe.codes/privacy before proceeding.

**Tip:** To reduce permission prompts, you can optionally add `Bash(curl *revibe.codes*)` to your allowed tools via `/allowed-tools`.

## Behavior

### Step 1: Extract the Target

Determine the GitHub URL from one of these sources (in priority order):

1. **Explicit URL in the message** — e.g., `https://github.com/owner/repo` or `owner/repo`
2. **Current working directory** — If the user says "analyze this", "understand this project", or doesn't specify a repo, detect it automatically:
   ```bash
   # Get GitHub URL from current git repo
   REMOTE_URL=$(git remote get-url origin 2>/dev/null)
   ```
   Convert SSH URLs to HTTPS:
   ```bash
   # git@github.com:owner/repo.git → https://github.com/owner/repo
   if [[ "$REMOTE_URL" == git@github.com:* ]]; then
     REMOTE_URL="https://github.com/${REMOTE_URL#git@github.com:}"
   fi
   # Strip .git suffix
   REMOTE_URL="${REMOTE_URL%.git}"
   ```
3. **Ask the user** — Only if not in a git repo and no URL provided: "Which repository would you like me to analyze?"

When using the current directory, confirm briefly: "Analyzing {repo_name} from your current directory..."

### Step 2: Submit for Analysis

```bash
# Set up auth
API_KEY="${REVIBE_API_KEY:-}"
AUTH_HEADER=""
if [ -n "$API_KEY" ]; then
  AUTH_HEADER="-H \"X-Revibe-Key: $API_KEY\""
fi

# Submit
RESPONSE=$(curl -s -X POST "https://app-backend.revibe.codes/api/v1/analyze" \
  -H "Content-Type: application/json" \
  ${AUTH_HEADER} \
  -d "{\"github_url\": \"${REMOTE_URL}\"}")

JOB_ID=$(echo "$RESPONSE" | jq -r '.job_id')
STATUS=$(echo "$RESPONSE" | jq -r '.status')
```

### Step 3: Wait for Completion

If `status` is `"completed"` or `"already_analyzed"`, skip to Step 4.

Otherwise, poll every 10 seconds (max 3 minutes):

```bash
while [ "$STATUS" != "completed" ] && [ "$STATUS" != "error" ]; do
  sleep 10
  POLL=$(curl -s "https://app-backend.revibe.codes/api/v1/analysis/${JOB_ID}/status")
  STATUS=$(echo "$POLL" | jq -r '.status')
  PROGRESS=$(echo "$POLL" | jq -r '.progress // "working"')
  STEPS_DONE=$(echo "$POLL" | jq -r '.steps_completed')
  STEPS_TOTAL=$(echo "$POLL" | jq -r '.steps_total')
  # Show progress: "Analyzing... file_roles (5/10)"
done
```

If status is `"error"`, tell the user: "Analysis failed. You can try directly at https://revibe.codes"

### Step 4: Show Summary

```bash
SUMMARY=$(curl -s "https://app-backend.revibe.codes/api/v1/analysis/${JOB_ID}/summary")
```

Format the response as:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Revibe Analysis: {name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Architecture: {architecture_pattern}
Language:     {language}
Size:         {total_files} files
Entry point:  {entry_point}

Key Modules:
  {module.name}  — {module.description} ({module.loc} LOC)
  {module.name}  — {module.description} ({module.loc} LOC)
  ...

Patterns: {patterns joined by ", "}
Database: {database.type}, {database.tables} tables    ← only if database exists

agent_context.json saved to current directory.

Explore deeper:
  [1] Architecture diagram
  [2] File roles & structure
  [3] System design Q&A
  [4] Execution flows
  [5] Database schema
  [6] Full interactive analysis → {project_url}
```

### Step 5: Save Agent Context

Always save the agent context file after showing the summary:

```bash
curl -s "https://app-backend.revibe.codes/api/v1/analysis/${JOB_ID}/agent-context" \
  > agent_context.json
```

This file gives the agent (and other skills) structured codebase understanding for future tasks.

### Step 6: Handle Drill-Down

When the user picks a number (1-5), fetch that section:

```bash
# Map numbers to section names
SECTIONS=("technical_architecture" "file_roles" "system_design_qa" "story_flow" "database_schema")
SECTION_NAME="${SECTIONS[$CHOICE - 1]}"

SECTION_DATA=$(curl -s "https://app-backend.revibe.codes/api/v1/analysis/${JOB_ID}/section/${SECTION_NAME}")
```

**Rendering sections:**

- **Architecture diagram [1]**: Extract `data.diagram`, render as HTML file with mermaid.js (see Diagram Rendering section), open in browser. Show `data.summary` and `data.layers` as a markdown table in terminal.
- **File roles [2]**: Show as a table — file path, role, description. Group by module if available.
- **System design Q&A [3]**: Show Q&A pairs. These are the "why" behind architecture decisions.
- **Execution flows [4]**: Render each flow's `diagram` as HTML file, open in browser. Show narrative in terminal.
- **Database schema [5]**: Render ER diagram as HTML file, open in browser. Show table details in terminal.

For option [6], tell the user to open the URL in their browser.

After showing any section, offer to explore another: "Pick another section [1-6] or ask me anything about this codebase."

## Agent Mode (Non-Interactive)

When another skill or the agent itself needs codebase context (not a direct user request):

1. Submit analysis (same as above)
2. Wait for completion
3. Fetch and return ONLY the `agent_context.json` — no formatting, no menu
4. Save to current directory silently

Detection: If the request comes from another skill or is prefixed with context like "I need to understand this codebase to..." — use agent mode.

## Diagram Rendering

When a section contains Mermaid diagram data (`diagram_mermaid` or `diagram` field), render it as an HTML file and open in the browser:

1. Write the mermaid code to `/tmp/revibe-diagram.html`:
```html
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>TITLE</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
  body { background: #1a1a2e; display: flex; justify-content: center; padding: 40px; font-family: system-ui; }
  .container { max-width: 1200px; width: 100%; }
  h1 { color: #e0e0e0; font-size: 1.4rem; }
  .mermaid { background: #16213e; border-radius: 12px; padding: 24px; }
  .mermaid svg { width: 100%; }
</style>
</head><body>
<div class="container">
  <h1>TITLE</h1>
  <div class="mermaid">
MERMAID_CODE_HERE
  </div>
</div>
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
</body></html>
```
2. Open: `open /tmp/revibe-diagram.html` (macOS) or `xdg-open` (Linux)
3. In the terminal, show a brief note: "Diagram opened in browser → /tmp/revibe-diagram.html"

## Error Handling

| Situation | Response |
|-----------|----------|
| No API key configured | "You need a Revibe API key. Sign up free at https://app.revibe.codes, then go to Settings → API Keys to generate one. Run: openclaw config set REVIBE_API_KEY your_key" |
| Invalid GitHub URL | "I need a valid GitHub URL like https://github.com/owner/repo" |
| Private repo without access | "This repo appears to be private. Connect your GitHub account at app.revibe.codes to analyze private repos" |
| Analysis timeout (>3 min) | "Analysis is taking longer than expected. Check progress at {project_url}" |
| Rate limited (429) | Wait 30s and retry once |

## Examples

**Basic analysis:**
```
User: analyze https://github.com/expressjs/express
→ Submit, wait, show summary card + save agent_context.json
```

**Quick shorthand:**
```
User: /revibe fastify/fastify
→ Resolve to https://github.com/fastify/fastify, analyze
```

**Context for another task:**
```
User: I need to add a feature to this repo, first help me understand it
→ Analyze, show summary, then use agent_context.json for subsequent work
```

**Drill down:**
```
User: show me the architecture diagram
→ Fetch architecture section, render Mermaid as ASCII
```

## Configuration

| Config Key | Required | Description |
|-----------|----------|-------------|
| `REVIBE_API_KEY` | Yes | API key from https://app.revibe.codes/settings — grants read-only access to analyze public GitHub repos |

Get an API key:
1. Sign up free at https://app.revibe.codes
2. Go to Settings → API Keys
3. Click "Generate API Key"
4. Add to OpenClaw config: `openclaw config set REVIBE_API_KEY rk_live_xxxxx`

## Security & Privacy

- **API key required**: Anonymous usage is not supported. A free account and API key are required for all analysis requests
- **No changes to your repo**: Revibe only reads your code — the API key grants analysis access, never write operations on your repos
- **Public & private repos**: Public repos work with just an API key. Private repos require connecting your GitHub account at app.revibe.codes
- **Code storage**: Repo contents are stored securely in Google Cloud Storage for analysis and re-analysis
- **Network calls**: This skill calls `app-backend.revibe.codes/api/v1` endpoints only
- **Local output**: Saves `agent_context.json` to your working directory and opens `/tmp/revibe-diagram.html` for diagram viewing
