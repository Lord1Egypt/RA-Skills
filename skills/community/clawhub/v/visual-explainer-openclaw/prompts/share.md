---
description: Share a generated visual explainer HTML file via Vercel and return a live URL
---
Load the visual-explainer skill, then share a generated HTML page.

**Target file** — determine from `$1`:
- Explicit path: share that file
- No argument: default to the latest diagram (`ls -t ~/.openclaw/workspace/diagrams/*.html | head -1`)

**Workflow:**
1. Validate the file exists and is an `.html` page.
2. Run:
   ```bash
   bash {{skill_dir}}/scripts/share.sh <file>
   ```
3. Parse and report the live URL and claim URL.

**Requirements:**
- `scripts/share.sh` expects a `vercel-deploy` helper script in an OpenClaw skill path (see script output if missing).

**Notes:**
- Deployments are public.
- Keep the local file path in your response so the user can re-share later.

$@
