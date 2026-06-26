# Channel Context Template

Use this template when creating new channel context files.

```markdown
# Channel Context: #channel-name

## Purpose
[What is this channel for? Be specific and concise.]

## Associated Projects
- [project-name]: [Brief description of the project and its relationship to this channel]
- [another-project]: [Description]

## Rules & Guidelines
- [Rule 1: What behavior is expected in this channel?]
- [Rule 2: Communication style, formatting, etc.]
- [Rule 3: Any special procedures or protocols]

## Recent Activity
- [YYYY-MM-DD]: [Brief update about recent activity]
- [YYYY-MM-DD]: [Another update]

## People to Know
- [@username]: [Role or responsibility in this channel]
- [@another-user]: [Role or responsibility]

## File Naming
- Use `<CHANNEL_ID>.md` (e.g., `C0AK8SDFS4W.md`) for highest priority
- OR `<CHANNEL_NAME>.md` (e.g., `bebops.md`) for medium priority
- Store in: `~/.openclaw/workspace/slack-channel-contexts/`

## Safety Rules

### Question vs. Action Rule
**When the user asks about implementing an idea or feature:**
1. Provide a complete answer and discussion FIRST
2. Do NOT execute any actions (file writes, code changes, API calls, etc.)
3. Wait for explicit confirmation before taking any action
4. Get clear "yes" or "proceed" confirmation before acting

**Why:** This prevents accidental execution of unrefined ideas.

---

```

## Tips for Good Context Files

1. **Be specific**: Clear purpose helps the AI understand the channel's intent
2. **Keep it concise**: Don't write a novel - just the essentials
3. **Update regularly**: Keep the "Recent Activity" section current
4. **Include safety rules**: Help the AI understand your preferences and constraints
5. **Add relevant people**: Who should the AI know about in this channel?

## Example

See [`../examples/EXAMPLE_CHANNEL_CONTEXT.md`](../examples/EXAMPLE_CHANNEL_CONTEXT.md) for a complete working example.

---

*Template version: 1.0.0*
