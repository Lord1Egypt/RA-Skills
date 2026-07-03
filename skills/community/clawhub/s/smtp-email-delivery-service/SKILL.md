---
name: smtp-email-delivery-service
description: "SMTP Email Delivery Service: Send emails via SMTP with HTML/text body, attachments, CC/BCC, and priority levels. Supports SMTPS encryption. Use when an agent needs smtp email delivery service, smtp email sending, automated email delivery, transactional email, notification email, send, smtp url, to through AgentPMT-hosted remote tool calls. Search keywords: smtp email delivery service, smtp email sending, automated email delivery, transactional email, notification email, send, smtp url, to."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/smtp-email-delivery-service
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/smtp-email-delivery-service"}}
---
# SMTP Email Delivery Service

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
SMTP Mailer is a streamlined email sending service designed for AI agents and automation workflows to deliver messages through any standard SMTP server. It accepts connection credentials via an intuitive URL format supporting both plain SMTP and encrypted SMTPS connections, making configuration straightforward without complex parameter handling. Recipients can be specified as a single address, an array, or a comma-separated string, with support for CC and BCC fields for flexible distribution. The tool sends both plain text and HTML formatted emails, enabling rich content delivery including formatted newsletters, styled notifications, and branded communications. File attachments are supported through base64-encoded content with configurable MIME types for documents, images, and other media. Email priority levels allow marking messages as low, normal, or high importance for recipient mail client handling. The sender address can be explicitly set or automatically derived from the SMTP username, simplifying configuration for common use cases. This tool is optimized specifically for email delivery. For workflows requiring additional protocols such as FTP file transfers, SSH command execution, or MQTT messaging alongside email, use the Protocol Bridge tool which provides a unified interface across multiple network protocols.

## Product Instructions
### SMTP Email Delivery Service

Send emails through any SMTP server with support for HTML content, attachments, CC/BCC, and priority settings.

#### Actions

##### send

Send an email via an SMTP server.

**Required Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Must be `"send"` |
| `smtp_url` | string | SMTP server URL with credentials. Format: `smtp://username:password@hostname:port` for STARTTLS (port 587) or `smtps://username:password@hostname:port` for SSL/TLS (port 465). |
| `to` | array or string | Recipient email address(es). Accepts an array of strings, a single string, or a comma-separated string. |
| `subject` | string | Email subject line. |
| `body` | string | Email body content, plain text or HTML depending on `body_type`. |

**Optional Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `from_email` | string | Username from `smtp_url` | Sender email address. Useful when sending from a different address than the one used for authentication. |
| `body_type` | string | `"plain"` | Body format: `"plain"` for plain text, `"html"` for HTML content. |
| `cc` | array | — | CC recipients. Array of email addresses. Visible to all recipients. |
| `bcc` | array | — | BCC recipients. Array of email addresses. Hidden from other recipients. |
| `attachments` | array | — | File attachments (max 25MB total). Each object requires `filename` (string) and `content` (base64-encoded string). Optional `content_type` (MIME type, defaults to `application/octet-stream`). |
| `priority` | string | `"normal"` | Email priority: `"low"`, `"normal"`, or `"high"`. Sets the X-Priority header. |

**Example — Send a plain text email:**

```json
{
  "action": "send",
  "smtp_url": "smtp://user:app-password@smtp.gmail.com:587",
  "to": ["recipient@example.com"],
  "subject": "Monthly Status Update",
  "body": "Hello,\n\nHere is the monthly status update.\n\nBest regards,\nThe Team"
}
```

**Example — Send an HTML email:**

```json
{
  "action": "send",
  "smtp_url": "smtps://user:pass@smtp.example.com:465",
  "to": ["recipient@example.com"],
  "subject": "Welcome!",
  "body": "<html><body><h1>Welcome!</h1><p>Thank you for signing up.</p></body></html>",
  "body_type": "html"
}
```

**Example — Send with CC, BCC, attachment, and high priority:**

```json
{
  "action": "send",
  "smtp_url": "smtp://user:pass@mail.example.com:587",
  "to": ["recipient@example.com"],
  "cc": ["manager@example.com"],
  "bcc": ["archive@example.com"],
  "subject": "Q1 Report",
  "body": "Please find the quarterly report attached.",
  "priority": "high",
  "attachments": [
    {
      "filename": "report.pdf",
      "content": "JVBERi0xLjQK...",
      "content_type": "application/pdf"
    }
  ]
}
```

**Example — Multiple recipients with a custom sender:**

```json
{
  "action": "send",
  "smtp_url": "smtp://auth-user:pass@mail.company.com:587",
  "to": ["alice@example.com", "bob@example.com"],
  "from_email": "noreply@company.com",
  "subject": "Team Announcement",
  "body": "<html><body><p>Please review the updated policy.</p></body></html>",
  "body_type": "html"
}
```

#### Common Workflows

1. **Send a notification email** — Use the `send` action with plain text body to deliver a quick notification to one or more recipients.
2. **Send a formatted newsletter** — Set `body_type` to `"html"` and provide styled HTML content with images and links.
3. **Distribute a report with attachments** — Attach base64-encoded files (PDF, CSV, Excel) and send to recipients with CC for visibility.
4. **Confidential distribution** — Use `bcc` to send to multiple recipients without revealing other addresses.
5. **Urgent communication** — Set `priority` to `"high"` to flag the email as important in recipient email clients.

#### Important Notes

- **Gmail users**: You must use an App Password, not your regular account password. Generate one at https://myaccount.google.com/apppasswords.
- **SMTP URL schemes**: Use `smtp://` for STARTTLS (port 587, recommended) or `smtps://` for direct SSL/TLS (port 465).
- **Attachment size limit**: Total attachment size must not exceed 25MB.
- **From address**: Some providers (like Gmail) enforce that the sender address matches the authenticated account. Use `from_email` only when your provider allows sending from an alias.
- **Priority**: Use `"high"` priority sparingly to avoid emails being flagged as spam.
- **Common MIME types for attachments**: `application/pdf`, `text/csv`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (Excel), `image/png`, `image/jpeg`, `text/plain`.

## When To Use
- Use this skill for `SMTP Email Delivery Service` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: smtp email delivery service, smtp email sending, automated email delivery, transactional email, notification email, send, smtp url, to.
- Supported action names: `send`.

## Use Cases
- SMTP email sending
- automated email delivery
- transactional email
- notification email
- alert email sending
- AI agent email
- LLM email integration
- workflow email automation
- HTML email sending
- rich text email
- formatted email delivery
- email with attachments
- document email delivery
- PDF email attachment
- image email attachment
- bulk email sending

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `send` (action slug: `send`): Send an email via an SMTP server. Supports plain text and HTML body formats, CC/BCC recipients, file attachments (base64-encoded), and priority levels. Price: `5` credits. Parameters: `attachments`, `bcc`, `body`, `body_type`, `cc`, `from_email`, `priority`, `smtp_url`, plus 2 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "smtp-email-delivery-service"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "smtp-email-delivery-service"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "smtp-email-delivery-service"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "smtp-email-delivery-service"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "smtp-email-delivery-service"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "smtp-email-delivery-service"
  }
}
```

## Call This Tool
Product slug: `smtp-email-delivery-service`

Marketplace page: https://www.agentpmt.com/marketplace/smtp-email-delivery-service

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "SMTP-Email-Delivery-Service",
    "arguments": {
      "action": "send",
      "attachments": [
        {
          "content": "Draft marketing copy to check for banned phrases.",
          "content_type": "Draft marketing copy to check for banned phrases.",
          "filename": "example filename"
        }
      ],
      "bcc": [
        "example bcc"
      ],
      "body": "example body",
      "body_type": "plain",
      "cc": [
        "example cc"
      ],
      "from_email": "user@example.com",
      "priority": "normal",
      "smtp_url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "smtp-email-delivery-service",
  "parameters": {
    "action": "send",
    "attachments": [
      {
        "content": "Draft marketing copy to check for banned phrases.",
        "content_type": "Draft marketing copy to check for banned phrases.",
        "filename": "example filename"
      }
    ],
    "bcc": [
      "example bcc"
    ],
    "body": "example body",
    "body_type": "plain",
    "cc": [
      "example cc"
    ],
    "from_email": "user@example.com",
    "priority": "normal",
    "smtp_url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `send` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/smtp-email-delivery-service
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
