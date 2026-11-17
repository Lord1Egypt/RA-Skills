# SendPulse MCP server — what it is and when it fits SMTP work

> Read this when the user's AI client supports MCP (Claude, ChatGPT, Cursor, and
> other MCP-compatible clients) or asks about "SendPulse MCP".
> Docs: sendpulse.com/features/mcp.

## 1. What it is

SendPulse runs a hosted MCP server at **`https://mcp.sendpulse.com/mcp`**.
Cloud-hosted, nothing to install. Once the user connects their AI client to it,
the assistant can call SendPulse actions as tools straight from chat — manage
email templates, address books, campaigns, contacts, and other SendPulse products.

## 2. MCP vs the SMTP API — set expectations correctly

**Transactional email is application runtime territory.** An app that sends order
confirmations or password resets must call the SMTP REST API (or relay) from its
own code — an MCP session is an interactive assistant channel, not your
application's delivery pipeline. So for the core use case of this skill, MCP does
not replace the API integration.

Where MCP genuinely helps SMTP users (when the matching tools are enabled):

- **Interactive account work from chat**: checking verified senders, looking up
  statistics or a specific message's status, managing the unsubscribe list —
  without opening the dashboard or writing one-off scripts.
- **Adjacent tasks**: creating/saving email templates, managing address books and
  campaigns (that's Email Service — see the `sendpulse-email-skill`, which has its
  own MCP guidance).

Tool names follow a `domain_action` pattern (e.g. `email_template_create`,
`email_addressbooks_get`). The available set depends on what the user enabled and
the current MCP version — **discover the available tools at runtime** rather than
hardcoding names.

## 3. Connecting (one-time, ≈10 min)

1. In the AI client, open MCP/connector settings and add the server URL
   `https://mcp.sendpulse.com/mcp`.
2. Authenticate with the SendPulse account — a **Single API Key**
   (*Settings → API → API keys*) is the preferred credential; account login also
   works.
3. Grant access and enable the desired tool groups.

## 4. Safety rule

Reading data (senders, stats, lists) is safe. **Anything that sends email to real
recipients requires explicit user confirmation first** — recipient, sender,
subject. Never trigger a send as a side effect of another request.

## 5. When MCP isn't connected

Proceed with the REST API ([quickstart.md](quickstart.md),
[../examples/](../examples/)) or the SMTP relay ([smtp-relay.md](smtp-relay.md)) —
they cover everything; MCP is a convenience layer for interactive work, not a
prerequisite.
