---
name: synthetic-data-generator
description: "Synthetic Data Generator: Generate synthetic test data: persons, companies, families, e-commerce, auth systems, CRM, financial, technical IDs. 10 locales, edge cases, deterministic seeding. Use when an agent needs synthetic data generator, generate realistic customer data, usage patterns, and transaction history, edge cases to validate ui robustness, generate, data type, count through AgentPMT-hosted remote tool calls. Discovery terms: synthetic data generator, generate realistic customer data."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/synthetic-data-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/synthetic-data-generator"}}
---
# Synthetic Data Generator

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
The Synthetic Data Generator creates production-quality fake data for development, testing, and demonstrations.

Data Types
The tool generates nine data types. Person Profiles include demographics, contact info, and addresses. Company Profiles contain industry classification, revenue, employee counts, and org structures. Family Units provide related household members with shared addresses and relationship mappings. Technical Data covers IPs, UUIDs, MAC addresses, URLs, domains, API keys, and system information. Financial Data generates fake credit cards, bank accounts, transactions, and investment portfolios. Edge Cases produce boundary testing data with unicode, special characters, injection patterns, and null values. E-commerce Datasets create complete online store ecosystems with customers, products, orders, and reviews. Auth System Datasets provide full IAM data with users, roles, permissions, sessions, and audit logs. CRM Datasets generate sales pipeline data with companies, contacts, leads, opportunities, and deals.

Locale Support
Data can be generated in 10 locales: en_US, en_GB, de_DE, fr_FR, es_ES, it_IT, pt_BR, nl_NL, pl_PL, and ja_JP.

Complexity Control
Simple mode requires only data type and count. Detailed mode enables extended fields and relationships. Dataset sizes range from small (100 records) to medium (500) to large (2000+). Advanced options provide granular control over age ranges, industries, family sizes, currencies, and more.

Testing Features
Edge case testing includes unicode, boundary values, special characters, and injection patterns at low, medium, or high severity levels. The generator maintains realistic relationships such as parent-child, customer-order, and user-role mappings. Security testing patterns include SQL injection, XSS attempts, and malformed data.

Scale
Simple types support 1–1000 records per request. Datasets generate hundreds to thousands of related records with preserved relationships and data integrity across entities.

## Product Instructions
### Synthetic Data Generator - Instructions

#### Overview
Generate realistic synthetic data for testing, development, and prototyping. Supports individual records (person, company, family, technical, financial, edge cases) and complete relational datasets (e-commerce, auth system, CRM). Data is locale-aware with support for 10 regions. Use a seed for reproducible results across runs.

#### Actions

##### generate
Generate synthetic data of a specified type.

**Required Fields:**
- `action` (string): `"generate"`
- `data_type` (string): Type of data to generate. One of: `person`, `company`, `family`, `technical`, `financial`, `edge_cases`, `ecommerce_dataset`, `auth_system_dataset`, `crm_dataset`

**Optional Fields:**
- `count` (integer, default: 1): Number of records to generate (1-1000). For dataset types, this is ignored in favor of the `size` parameter.
- `locale` (string, default: `"en_US"`): Region for names, addresses, phone formats. Options: `en_US`, `en_GB`, `de_DE`, `fr_FR`, `es_ES`, `it_IT`, `pt_BR`, `nl_NL`, `pl_PL`, `ja_JP`
- `seed` (integer, default: null): Random seed for reproducible output. Same seed + same parameters = same data every time. Omit for random data.
- `include_details` (boolean, default: true): Include extended fields (addresses, financials, relationships). Set false for minimal records.
- `include_edge_cases` (boolean, default: false): Mix in unicode, special characters, and boundary values for robustness testing.
- `size` (string, default: `"medium"`): Only for dataset types (`ecommerce_dataset`, `auth_system_dataset`, `crm_dataset`). Options: `small` (~100 records), `medium` (~500 records), `large` (~2000+ records). Ignored for non-dataset types.
- `options` (object): Type-specific advanced options (see below).

---

#### Data Types

##### person
Individual profiles with names, emails, addresses, demographics.

**Options:**
- `age_range` (array of 2 integers, 0-120): Filter by age range, e.g. `[25, 65]`

**Example:**
```json
{
  "action": "generate",
  "data_type": "person",
  "count": 5,
  "locale": "fr_FR",
  "options": { "age_range": [25, 45] }
}
```

##### company
Business profiles with industry, size, revenue, and sample employees.

**Options:**
- `industry_filter` (string): Filter to a specific industry. Options: `Technology`, `Healthcare`, `Finance`, `Manufacturing`, `Retail`, `Education`
- `size_category` (string): Company size. Options: `small` (1-50 employees), `medium` (51-500), `large` (501-5000), `enterprise` (5000+)

**Example:**
```json
{
  "action": "generate",
  "data_type": "company",
  "count": 3,
  "options": { "industry_filter": "Technology", "size_category": "medium" }
}
```

##### family
Family units with parents, children, shared addresses, and relationship mappings.

**Options:**
- `family_size_range` (array of 2 integers, 2-10): Min and max family members, e.g. `[3, 5]`

**Example:**
```json
{
  "action": "generate",
  "data_type": "family",
  "count": 2,
  "include_details": true,
  "options": { "family_size_range": [3, 5] }
}
```

##### technical
IPs, UUIDs, URLs, domains, API keys, tokens, and system info.

**Options:**
- `data_types` (array of strings): Which technical types to include. Options: `ip`, `ipv6`, `mac`, `uuid`, `url`, `domain`, `email`, `user_agent`, `api_key`, `token`. Default: `["ip", "uuid", "url", "email", "user_agent"]`

**Example:**
```json
{
  "action": "generate",
  "data_type": "technical",
  "count": 10,
  "options": { "data_types": ["ip", "ipv6", "mac", "uuid", "api_key"] }
}
```

##### financial
Credit cards, bank accounts, balances, and transaction history.

**Options:**
- `currency` (string, default: `"USD"`): ISO 4217 currency code (e.g. `USD`, `EUR`, `GBP`, `JPY`)
- `include_transactions` (boolean, default: false): Include 5-50 detailed transactions per record

**Example:**
```json
{
  "action": "generate",
  "data_type": "financial",
  "count": 3,
  "options": { "currency": "EUR", "include_transactions": true }
}
```

##### edge_cases
Unicode, special characters, boundary values, injection patterns, and malformed data for robustness testing.

**Options:**
- `severity_level` (string, default: `"medium"`): Options: `low`, `medium`, `high`. Higher severity produces more extreme test values.
- `categories` (array of strings): Which edge case types to include. Options: `unicode`, `length`, `null`, `boundary`, `malformed`, `injection`, `special_chars`, `numeric`. Default: `["unicode", "length", "null", "boundary"]`

**Example:**
```json
{
  "action": "generate",
  "data_type": "edge_cases",
  "count": 5,
  "options": { "severity_level": "high", "categories": ["unicode", "injection", "boundary", "malformed"] }
}
```

##### ecommerce_dataset
Complete e-commerce dataset with interlinked customers, products, and orders.

**Example:**
```json
{
  "action": "generate",
  "data_type": "ecommerce_dataset",
  "size": "small",
  "seed": 42
}
```

##### auth_system_dataset
Authentication/authorization dataset with users, roles, permissions, and sessions.

**Example:**
```json
{
  "action": "generate",
  "data_type": "auth_system_dataset",
  "size": "medium",
  "locale": "en_GB"
}
```

##### crm_dataset
CRM dataset with companies, contacts, and deals/opportunities with pipeline stages.

**Example:**
```json
{
  "action": "generate",
  "data_type": "crm_dataset",
  "size": "large",
  "seed": 123
}
```

---

#### Common Workflows

##### Reproducible Test Fixtures
Use `seed` to generate identical data across environments:
```json
{
  "action": "generate",
  "data_type": "person",
  "count": 100,
  "seed": 12345,
  "locale": "en_US"
}
```

##### Security and Validation Testing
Combine edge cases with regular data:
```json
{
  "action": "generate",
  "data_type": "person",
  "count": 50,
  "include_edge_cases": true
}
```

##### Minimal Data for Quick Tests
Disable extended details for lightweight records:
```json
{
  "action": "generate",
  "data_type": "company",
  "count": 20,
  "include_details": false
}
```

---

#### Important Notes
- `count` ranges from 1 to 1000. For dataset types, use `size` instead to control volume.
- Dataset types (`ecommerce_dataset`, `auth_system_dataset`, `crm_dataset`) return multiple interlinked collections with a `record_counts` summary.
- Single-record requests (count=1) return the object directly; multiple records return a list wrapped in a named key.
- All generated data is fake and safe for testing. Financial data (credit cards, accounts) is not real.
- Edge case injection patterns are safe strings for testing input validation -- they do not perform actual attacks.
- The `locale` parameter affects names, addresses, and phone number formats but not all fields (e.g., currency must be set separately via options).

## When To Use
- Use this skill for `Synthetic Data Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: synthetic data generator, generate realistic customer data, usage patterns, and transaction history, edge cases to validate ui robustness, generate, data type, count.
- Supported action names: `generate`.

## Use Cases
- Generate realistic customer data
- usage patterns
- and transaction history
- edge cases to validate UI robustness
- large datasets for stress testing
- valid-format credit card numbers

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `generate` (action slug: `generate`): Generate synthetic data of a specified type. Supports person profiles, company profiles, family units, technical data, financial data, edge cases, and complete relational datasets (e-commerce, auth system, CRM). Price: `10` credits. Parameters: `count`, `data_type`, `include_details`, `include_edge_cases`, `locale`, `options`, `seed`, `size`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "synthetic-data-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "synthetic-data-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "synthetic-data-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "synthetic-data-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "synthetic-data-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "synthetic-data-generator"
  }
}
```

## Call This Tool
Product slug: `synthetic-data-generator`

Marketplace page: https://www.agentpmt.com/marketplace/synthetic-data-generator

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
    "name": "Synthetic-Data-Generator",
    "arguments": {
      "action": "generate",
      "count": 1,
      "data_type": "person",
      "include_details": true,
      "include_edge_cases": false,
      "locale": "en_US",
      "options": {
        "age_range": [
          0
        ],
        "categories": [
          "unicode"
        ],
        "currency": "USD",
        "data_types": [
          "ip"
        ],
        "family_size_range": [
          2
        ],
        "include_transactions": false,
        "industry_filter": "Technology",
        "severity_level": "medium"
      },
      "seed": 1,
      "size": "medium"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "synthetic-data-generator",
  "parameters": {
    "action": "generate",
    "count": 1,
    "data_type": "person",
    "include_details": true,
    "include_edge_cases": false,
    "locale": "en_US",
    "options": {
      "age_range": [
        0
      ],
      "categories": [
        "unicode"
      ],
      "currency": "USD",
      "data_types": [
        "ip"
      ],
      "family_size_range": [
        2
      ],
      "include_transactions": false,
      "industry_filter": "Technology",
      "severity_level": "medium"
    },
    "seed": 1,
    "size": "medium"
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
- Marketplace product: https://www.agentpmt.com/marketplace/synthetic-data-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
