---
name: quantum-secure-token-generator
description: "Quantum Secure Token Generator: Generate secure random string tokens for API keys, session tokens, and password reset links using quantum entropy. Use when an agent needs quantum secure token generator, api key generation, session tokens, password reset tokens, authentication mechanisms, generate, length, charset through AgentPMT-hosted remote tool calls. Discovery terms: quantum secure token generator, api key generation, session tokens, password reset tokens, authentication mechanisms."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/quantum-secure-token-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/quantum-secure-token-generator"}}
---
# Quantum Secure Token Generator

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
For generating cryptographically secure, random string tokens for authentication and authorization purposes. The tool uses a hardware-based quantum entropy source to ensure true, unpredictable randomness for each character. It allows for customization of the token's length and the selection of a predefined character set, making it ideal for creating highly secure API keys, session tokens, and password reset links.

## Product Instructions
### Quantum Secure Token Generator

#### Overview
Generate cryptographically secure tokens using either quantum-derived true randomness (from the CURBy quantum random number generator at University of Colorado Boulder) or standard cryptographic randomness. Supports multiple character sets and configurable token lengths.

#### Actions

##### generate
Generate a secure random token.

**Required Fields:** None (all fields have defaults)

**Optional Fields:**
- `length` (integer, default: 32) — Token length in characters. Range: 8–256.
- `charset` (string, default: "alphanumeric") — Character set for the token. Options:
  - `"alphanumeric"` — Letters (a-z, A-Z) and digits (0-9)
  - `"hex"` — Hexadecimal characters (0-9, a-f)
  - `"base64"` — URL-safe Base64 characters
  - `"ascii"` — All printable ASCII characters excluding whitespace
- `source` (string, default: "quantum") — Randomness source. Options:
  - `"quantum"` — True randomness from quantum measurements
  - `"standard"` — Cryptographically secure pseudo-random generation

**Example — Generate a default token:**
```json
{
  "action": "generate"
}
```

**Example — Generate a 64-character hex token using quantum randomness:**
```json
{
  "action": "generate",
  "length": 64,
  "charset": "hex",
  "source": "quantum"
}
```

**Example — Generate a short Base64 API key:**
```json
{
  "action": "generate",
  "length": 48,
  "charset": "base64"
}
```

**Example — Generate a strong ASCII password:**
```json
{
  "action": "generate",
  "length": 24,
  "charset": "ascii",
  "source": "quantum"
}
```

**Response includes:**
- `token` — The generated token string
- `length` — Actual length of the generated token
- `charset` — Character set used
- `source` — Randomness source used ("quantum" or "standard")

#### Common Workflows

1. **Generate an API key** — Use `charset: "base64"` with `length: 48` or higher for URL-safe API keys.
2. **Generate a session token** — Use default settings (`charset: "alphanumeric"`, `length: 32`) for session identifiers.
3. **Generate a hex token for cryptographic use** — Use `charset: "hex"` with `length: 64` for 256-bit equivalent tokens.
4. **Generate a strong password** — Use `charset: "ascii"` for maximum character diversity.

#### Important Notes
- The quantum source provides true randomness derived from quantum measurements. If the quantum source is temporarily unavailable, consider using `"standard"` as a fallback.
- The standard source uses cryptographically secure generation suitable for production security applications.
- Token length must be between 8 and 256 characters.
- All generated tokens are returned as strings and are not stored — save them immediately after generation.

## When To Use
- Use this skill for `Quantum Secure Token Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: quantum secure token generator, api key generation, session tokens, password reset tokens, authentication mechanisms, generate, length, charset.
- Supported action names: `generate`.

## Use Cases
- API Key Generation
- Session Tokens
- Password Reset Tokens
- Authentication Mechanisms
- Coupon Codes
- Two-Factor Authentication (2FA) Codes
- Secure URL Generation
- Cryptographic Nonces

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `generate` (action slug: `generate`): Generate a secure random token with configurable length and character set using quantum or standard randomness. Suitable for API keys, session tokens, and password reset links. Price: `5` credits. Parameters: `charset`, `length`, `source`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "quantum-secure-token-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "quantum-secure-token-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "quantum-secure-token-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "quantum-secure-token-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "quantum-secure-token-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "quantum-secure-token-generator"
  }
}
```

## Call This Tool
Product slug: `quantum-secure-token-generator`

Marketplace page: https://www.agentpmt.com/marketplace/quantum-secure-token-generator

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
    "name": "Quantum-Secure-Token-Generator",
    "arguments": {
      "action": "generate",
      "charset": "alphanumeric",
      "length": 32,
      "source": "quantum"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "quantum-secure-token-generator",
  "parameters": {
    "action": "generate",
    "charset": "alphanumeric",
    "length": 32,
    "source": "quantum"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `generate` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/quantum-secure-token-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
