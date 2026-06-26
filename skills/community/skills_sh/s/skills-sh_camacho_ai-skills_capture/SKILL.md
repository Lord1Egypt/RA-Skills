---
name: capture
description: Creates a draft GitHub Issue with triage label from natural language description.
---

## Inputs
- Free-text description of an idea, bug, or feature request

## Steps

1. **Parse the description** to detect type:
   | Keywords | Type | Labels |
   |----------|------|--------|
   | error, crash, broken, fix, bug, fails, regression | Bug | `triage`, `bug` |
   | add, want, should, new, feature, enhance, improve | Feature | `triage`, `enhancement` |
   | Default | Feature | `triage`, `enhancement` |

2. **Create GitHub Issue**:
   ```bash
   gh issue create \
     --title "<concise title from description>" \
     --body "<full description>" \
     --label "triage" --label "<bug or enhancement>"
   ```

3. **Return** the issue number and URL.

## Fallback

If `gh` is not available or GitHub access fails:
1. Try GitHub MCP tools (if available)
2. If neither works → append to `ai-workspace/scratchpad.md`:
   ```markdown
   ## Captured [date]
   **Type**: [bug/feature]
   **Description**: [text]
   _Failed to create GitHub Issue — saved here as fallback._
   ```
   Inform the user that the capture was saved locally.

## Edge Cases
- No description provided → ask the user to describe the idea/bug
- Offline / no GitHub access → scratchpad fallback (see above)
