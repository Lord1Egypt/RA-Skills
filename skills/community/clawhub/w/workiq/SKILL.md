---
name: workiq
description: Query Microsoft 365 data (emails, meetings, documents, Teams messages, people) using WorkIQ CLI
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","homepage":"https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/workiq-overview","requires":{"anyBins":["workiq","npx"]}}}
---

## WorkIQ — Microsoft 365 Data Query

Use this skill to answer questions about Microsoft 365 data: emails, meetings, calendar, documents, Teams messages, and people/org insights. WorkIQ queries data the authenticated user already has permission to access — no extra permissions are granted.

### When to use

Invoke this skill whenever the user asks about:

- **Emails** — "What did Sarah say about the budget?", "Find emails about project X"
- **Calendar / meetings** — "What's on my calendar tomorrow?", "Who attended the standup last Friday?"
- **Documents / files** — "Find my recent PowerPoints", "Summarize the Q4 spec document"
- **Teams messages** — "Summarize today's messages in the Engineering channel"
- **People / org** — "Who is working on Project Alpha?", "Who is my manager?"
- **Meeting notes** — "What issues were raised in yesterday's Contoso meeting?"

### How to query

Use the `exec` tool to run WorkIQ. Prefer the global CLI if available, otherwise fall back to npx.

**If `workiq` is on PATH:**
```bash
workiq ask -q "<natural language question>"
```

**If only `npx` is available (Node.js required):**
```bash
npx -y @microsoft/workiq ask -q "<natural language question>"
```

**With a specific Entra tenant ID:**
```bash
workiq ask -t <tenant-id> -q "<natural language question>"
```

### Query guidelines

- Write questions in **natural language** — WorkIQ understands context
- Be **specific**: include names, dates, project names, or channel names when known
- WorkIQ CLI is **stateless per call** — for follow-ups, include full context in each question
- WorkIQ only returns data the signed-in user has permission to see
- Do **not** pipe or combine WorkIQ output with other shell commands — run it standalone

### Example queries

| User intent | Command |
|---|---|
| Recent emails on a topic | `workiq ask -q "What did John say about the proposal last week?"` |
| Tomorrow's calendar | `workiq ask -q "What meetings do I have tomorrow?"` |
| Find a document | `workiq ask -q "Find my recent documents about Q4 planning"` |
| Teams channel summary | `workiq ask -q "Summarize today's messages in the Engineering channel"` |
| People lookup | `workiq ask -q "Who is working on Project Alpha?"` |
| Meeting notes | `workiq ask -q "What issues were raised in yesterday's Contoso meeting?"` |
| Spec document | `workiq ask -q "Summarize the key requirements in the user portal spec document"` |
| Emails from a person | `workiq ask -q "Summarize emails from Sarah about the budget"` |

### First-time setup

If WorkIQ has never been used, the EULA must be accepted first. Tell the user to run:

```bash
workiq accept-eula
```

If WorkIQ is not installed at all:

```bash
npm install -g @microsoft/workiq
workiq accept-eula
```

### Error handling

| Error | Action |
|---|---|
| Auth / sign-in prompt | Tell the user to run `workiq ask` manually in their terminal to complete the interactive sign-in flow |
| EULA not accepted | Prompt the user to run `workiq accept-eula` |
| No results / empty response | Rephrase the question with more context, a different time range, or more specific names |
| Permission denied | User may lack an M365 Copilot license or admin consent for the WorkIQ app in their Entra tenant |
| `workiq` not found | Prompt the user to install: `npm install -g @microsoft/workiq` |
