# Channel Context: #bebops

> **This is an example context file** - use it as a template for your own channels.
> See [`references/context-template.md`](references/context-template.md) for the basic template.


## Purpose
All things Bebop - announcements, updates, and kudos. This channel is for sharing Bebop-related news, celebrating wins, and keeping everyone informed.

## Associated Projects
- **bebops-project**: Main Bebops project repository
- **announcements**: Company announcement templates
- **slack-channel-context**: Channel context management skill

## Rules & Guidelines
- Keep messages positive and supportive
- Use ⭐ emoji for kudos and celebrations
- Tag relevant team members for updates
- Be concise - focus on what matters
- Always read context files before making changes

## Safety Rules

### Question vs. Action Rule
**When the user asks about implementing an idea or feature:**
1. Provide a complete answer and discussion FIRST
2. Do NOT execute any actions (file writes, code changes, API calls, etc.)
3. Wait for explicit confirmation before taking any action
4. Get clear "yes" or "proceed" confirmation before acting

**Why:** This prevents accidental execution of unrefined ideas and ensures we discuss the approach first.

## Recent Activity
- 2026-03-15: Released v2.0 with new features
- 2026-03-14: Celebrated 1000+ successful deployments
- 2026-03-13: Added new voice storytelling capabilities

## People to Know
- **@Brian** (U0AKPRNJWL9): User, primary stakeholder
- **@Bebop** (U0AKELP85GU): AI assistant, creator
- **@Team**: Development team members

## File Naming Convention

Context files are stored in `~/.openclaw/workspace/slack-channel-contexts/` with simple names:
- `<CHANNEL_ID>.md` (e.g., `C0AK8SDFS4W.md`) - highest priority
- `<CHANNEL_NAME>.md` (e.g., `bebops.md`) - medium priority
- No default file - channels without context files return None

## How to Update This File

**When you edit this file, always follow these steps:**

1. **Read the file first** - Use the `read` tool to see current contents
2. **Make your edits** - Use the `edit` tool for precise changes
3. **Force reload cache** - Call `load_channel_context()` with `force_reload=True`

**Important:** Never overwrite a file without reading it first! Always preserve existing content.

## Update History
- 2026-03-15: Added force_reload workflow documentation
- 2026-03-14: Updated recent activity section
- 2026-03-13: Created channel context file

---

