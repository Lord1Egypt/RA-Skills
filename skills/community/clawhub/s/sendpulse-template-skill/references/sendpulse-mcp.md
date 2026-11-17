# Upload & Manage via the SendPulse MCP Server

> Read this to upload the generated template (and run mailings) **without manual copy-paste**, by
> connecting the user's AI client to the SendPulse MCP server. This is the recommended path: the
> agent calls SendPulse tools directly. Docs: sendpulse.com/features/mcp.

## Table of Contents
1. What the MCP server is
2. Connecting (one-time setup)
3. Available tools
4. Uploading a template you just generated
5. When MCP isn't connected

---

## 1. What the MCP server is

SendPulse runs a hosted MCP server at **`https://mcp.sendpulse.com/mcp`**. Once the user connects
their AI client to it, the assistant can call SendPulse actions as tools — create email templates,
manage address books, send campaigns, run chatbot/push tasks, update contacts, manage automations —
all from chat, no copy-paste. Cloud-hosted, no install, works with Claude, ChatGPT, Cursor, and
other MCP-compatible clients.

## 2. Connecting (one-time setup)

Walk the user through this once (≈10 min):
1. In their AI client, open MCP/connector settings and **add the server URL**
   `https://mcp.sendpulse.com/mcp`.
2. **Authenticate** with their SendPulse account when prompted — a **Single API Key** (Settings →
   API → API keys) is the preferred, simplest credential; account login also works.
3. **Grant** the assistant access and **enable the tools** they want (e.g. email template + campaign).

After that, the SendPulse tools appear in the session and the skill can call them directly.

## 3. Available tools

Tool names follow a `domain_action` pattern. Examples seen in the SendPulse docs:
- `email_template_create` — create an email template (this is the key one for this skill).
- `email_addressbooks_get` — list address books / mailing lists.
- `chatbots_bots_list`, `chatbots_bots_campaigns_t_send` — chatbot audiences & campaigns.
- `push_tasks_send` — web push tasks.
- Plus CRM (deals, contact notes), contact variables, automation flows, pop-up stats.

> The exact tool list depends on which tools the user enabled and the current SendPulse MCP version.
> **Discover them at runtime** (list the available `sendpulse`/`email_*` tools in the session)
> rather than hardcoding — names and parameters may evolve.

## 4. Uploading a template you just generated

1. Generate and save the HTML fragment as usual.
2. Check whether SendPulse MCP tools are present in the session (look for `email_template_create`
   or similar). If yes, offer: *"Want me to upload this straight to your SendPulse account?"*
3. Call the template-create tool with the template **name** and the **HTML body**. (Some tools
   expect raw HTML; the underlying API expects Base64 — the MCP tool usually handles encoding, but
   if it errors, see [sendpulse-api.md](sendpulse-api.md) for the Base64 detail.)
4. Confirm the created template ID / name back to the user and tell them where to find it in
   SendPulse (Email → Templates).
5. If they want to send: use the address-book and campaign tools (or point them to
   [sendpulse-api.md](sendpulse-api.md) §campaigns) — confirm sender, subject, and list first.

> **Sending is an outward-facing action.** Always confirm recipient list, sender, and subject with
> the user before triggering an actual send via MCP. Creating/saving a template is safe; sending is not.

## 5. When MCP isn't connected

If no SendPulse MCP tools are in the session, don't fail — offer two fallbacks:
- **Connect MCP** (walk through §2), or
- **Use the API** directly ([sendpulse-api.md](sendpulse-api.md)) with their client_id/secret, or
- **Manual paste**: deliver the HTML and the paste instructions (SKILL.md Output step).
