---
name: youraitools-hub
description: One remote MCP server with 45 agent tools we built - read web pages as markdown (WebRead), scan text, pages and tool definitions for prompt injection (InjectScan), check AI agent registrations (AgentGate), domain/email checks, wallet sanctions screening, token and signature safety checks, x402 endpoint checks, FX rates and more. Many tools have a free tier; paid calls via prepaid credits or x402.
version: 1.0.0
homepage: https://youraitools.co
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# YourAITools MCP Hub

We built and run the YourAITools MCP Hub: one remote MCP server (streamable HTTP) that exposes our
agent APIs as 45 tools.

- MCP endpoint: `https://api.youraitools.co/mcp/hub`
- Docs: `https://api.youraitools.co/mcp/hub/README.md`
- Official MCP Registry name: `co.youraitools/hub`

This skill contains instructions only: no code, no keys, and it never pays by itself.

## When to use

- **WebRead** (`read_url`): fetch one public page as clean markdown.
- **InjectScan** (`scan_text`, `scan_url`, `scan_tools`): check untrusted text, a web page (including hidden
  HTML) or MCP tool definitions for prompt injection / tool poisoning before the agent acts on them.
- **AgentGate** (`check_agent`): check whether an AI agent is registered in an on-chain agent registry.
- Safety checks before acting: `check_domain`, `check_email`, `screen_address` / `screen_batch`
  (OFAC sanctions list), `check_signature` (decode a transaction or signature before signing),
  `check_token`, `check_solana_token`, `check_counterparty`, `check_package`, `scan_dependencies`,
  `scan_for_leaks`.
- Agent/dev utilities: `check_x402_endpoint`, `find_paid_api`, `check_mcp_server`, `audit_tools`,
  `route_tools`, `audit_website`, `detect_stack`, `transcribe_audio`, FX rates (`convert_currency`,
  `fx_rates`, `fx_history`), `crypto_price`.
- Trading analytics tools in the hub are read-only and descriptive. They are not financial advice.

## Connect

Add the remote server to any MCP client that supports streamable HTTP, for example:

```json
{ "mcpServers": { "youraitools": { "url": "https://api.youraitools.co/mcp/hub" } } }
```

List tools without any key:

```bash
curl -s -X POST https://api.youraitools.co/mcp/hub \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Pricing and payment

Each tool's description says whether it has a free tier. Paid calls cost the same as the tool's own
paid route, with no hub fee, via prepaid credits (`Authorization: Bearer <key>`, see
https://api.youraitools.co/credits/) or x402 per call. Failed calls are not charged.
**Always ask the user to approve a paid call and its price first.** Never put keys in chat or in this skill.

## Safety

- Inputs you send (URLs, text, addresses) go to api.youraitools.co, which we operate. Don't send secrets.
- Results are signals to help a human or agent decide; double-check anything high-stakes.

## Links

- https://youraitools.co
- Source and docs: https://github.com/Duffey234/youraitools
