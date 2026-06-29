---
name: random-password-generator-quantum
description: "Random Password Generator Quantum: Generate high-entropy passwords with configurable length and character requirements (uppercase, lowercase, digits, symbols) using quantum randomness. Use when an agent needs random password generator quantum, root password generation, encryption keys, high security authentication, initial user onboarding, generate, length, uppercase through AgentPMT-hosted remote tool calls. Discovery terms: random password generator quantum, root password generation."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/random-password-generator-quantum
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/random-password-generator-quantum"}}
---
# Random Password Generator Quantum

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
For creating high-entropy, cryptographically strong passwords that adhere to specific security policies. The generator uses a hardware-based quantum source to ensure true randomness for each character. It provides granular control over the password's length and the inclusion of different character types (uppercase, lowercase, digits, symbols), making it ideal for generating credentials for high-security systems.

## Product Instructions
### Random Password Generator Quantum

#### Overview
Generate secure passwords using quantum randomness from the CURBy quantum random number generator or standard cryptographically secure randomness. Customize password length, character types, and ambiguity settings.

#### Actions

##### generate
Generate a secure random password with configurable options.

**Required Fields:**
- `action` (string): Must be `"generate"`

**Optional Fields:**
- `length` (integer): Password length in characters. Range: 8–128. Default: `16`
- `uppercase` (boolean): Include uppercase letters (A-Z). Default: `true`
- `lowercase` (boolean): Include lowercase letters (a-z). Default: `true`
- `digits` (boolean): Include digits (0-9). Default: `true`
- `symbols` (boolean): Include symbols/punctuation characters. Default: `true`
- `exclude_ambiguous` (boolean): Exclude visually ambiguous characters (0, O, 1, l, I). Recommended for passwords that will be manually typed. Default: `true`
- `source` (string): Random source to use. `"quantum"` uses a quantum random number generator; `"standard"` uses cryptographically secure Python randomness. Allowed values: `"quantum"`, `"standard"`. Default: `"quantum"`

**Example — Default 16-character quantum password:**
```json
{
  "action": "generate"
}
```

**Example — Long password with only letters and digits:**
```json
{
  "action": "generate",
  "length": 32,
  "symbols": false,
  "exclude_ambiguous": true
}
```

**Example — Short PIN-style numeric password:**
```json
{
  "action": "generate",
  "length": 8,
  "uppercase": false,
  "lowercase": false,
  "symbols": false,
  "digits": true
}
```

**Example — Standard (non-quantum) source with all character types:**
```json
{
  "action": "generate",
  "length": 24,
  "source": "standard",
  "exclude_ambiguous": false
}
```

**Response includes:**
- `password`: The generated password string
- `length`: Actual character count of the generated password
- `source`: Which random source was used (`"quantum"` or `"standard"`)
- `character_types`: Object showing which character categories were enabled

#### Common Workflows

1. **Quick secure password**: Call `generate` with defaults for a 16-character quantum password with all character types.
2. **Readable password**: Set `exclude_ambiguous` to `true` and `symbols` to `false` for a password that is easy to read and type.
3. **High-entropy password**: Set `length` to 64 or 128 and keep all character types enabled.
4. **Numeric-only code**: Disable `uppercase`, `lowercase`, and `symbols`, keeping only `digits`.

#### Important Notes
- At least one character type (`uppercase`, `lowercase`, `digits`, or `symbols`) must be enabled; otherwise the request will fail.
- The quantum source provides true quantum randomness; the standard source uses cryptographically secure pseudorandomness. Both are suitable for security-sensitive passwords.
- When `exclude_ambiguous` is enabled, the characters `0`, `O`, `1`, `l`, and `I` are removed from the character pool.
- Password length must be between 8 and 128 characters.

## When To Use
- Use this skill for `Random Password Generator Quantum` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: random password generator quantum, root password generation, encryption keys, high security authentication, initial user onboarding, generate, length, uppercase.
- Supported action names: `generate`.

## Use Cases
- Root Password Generation
- Encryption Keys
- High-Security Authentication
- Initial User Onboarding
- Password Rotation Policies
- Secure Credential Generation
- Automated System Accounts

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `generate` (action slug: `generate`): Generate a secure random password with configurable length, character types, and ambiguity settings using quantum or standard randomness. Price: `5` credits. Parameters: `digits`, `exclude_ambiguous`, `length`, `lowercase`, `source`, `symbols`, `uppercase`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "random-password-generator-quantum"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "random-password-generator-quantum"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "random-password-generator-quantum"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "random-password-generator-quantum"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "random-password-generator-quantum"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "random-password-generator-quantum"
  }
}
```

## Call This Tool
Product slug: `random-password-generator-quantum`

Marketplace page: https://www.agentpmt.com/marketplace/random-password-generator-quantum

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
    "name": "Random-Password-Generator-Quantum",
    "arguments": {
      "action": "generate",
      "digits": true,
      "exclude_ambiguous": true,
      "length": 16,
      "lowercase": true,
      "source": "quantum",
      "symbols": true,
      "uppercase": true
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "random-password-generator-quantum",
  "parameters": {
    "action": "generate",
    "digits": true,
    "exclude_ambiguous": true,
    "length": 16,
    "lowercase": true,
    "source": "quantum",
    "symbols": true,
    "uppercase": true
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
- Marketplace product: https://www.agentpmt.com/marketplace/random-password-generator-quantum
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
