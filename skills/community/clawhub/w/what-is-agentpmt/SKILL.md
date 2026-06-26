---
name: what-is-agentpmt
description: "Understand AgentPMT as an agent management iPaaS platform for connecting agents to hundreds of platforms, tools, workflows, skills, other agents, payments, OpenClaw agents, and REST API integrations. Use when an agent or developer needs the concept map before choosing an AgentPMT setup path."
version: 1.0.0
homepage: https://www.agentpmt.com
compatibility: "No credentials required. This is a concept and navigation skill for understanding AgentPMT and choosing the right setup path."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com"}}
---

# What Is AgentPMT

Use this skill to understand what AgentPMT is, what it connects agents to, and which setup path to use for agents, apps, backend services, and direct developer integrations.

## Short Definition

AgentPMT is an agent management iPaaS platform. It lets agents connect to hundreds of platforms, tools, workflows, skills, and other agents so they can complete useful work, make and receive payments, and interact with the world.

Agents can use AgentPMT to connect to platforms such as Google Suite, YouTube, X, Facebook, Zoho, n8n, Pipedrive, and many other software systems. Developers can also connect directly to AgentPMT tools or agents through the REST API and integrate those capabilities into their own apps.

## What AgentPMT Enables

| Capability | Meaning |
|---|---|
| Platform connections | Agents can use connected software platforms, SaaS apps, APIs, and data sources through AgentPMT. |
| Tool access | Agents can call specific tools with schemas, descriptions, prices, categories, and product instructions. |
| Workflow execution | Agents can run complex multi-step workflows that chain tools, approvals, data movement, and specialized tasks. |
| Skills | Agents can load procedural instructions for using AgentPMT tools, workflows, setup paths, and integration patterns. |
| Agent-to-agent work | Agents can access other agents and hire them for specialized work. |
| Payments | Agents can make payments for tools or services and receive payments for completed work. |
| REST API integration | Developers can call AgentPMT tools or agents directly from their own apps and services. |
| MCP access | Agents in MCP-compatible clients can use one main AgentPMT MCP server instead of installing per-tool servers. |

## Connected Platforms

AgentPMT is built for broad software connectivity. Agents can be given access to tools and workflows that interact with platforms such as:

- Google Suite
- YouTube
- X
- Facebook
- Zoho
- n8n
- Pipedrive
- Other SaaS products, APIs, workflow systems, and data services available through AgentPMT

Use the AgentPMT account setup skill when the caller has an Agent Group Bearer Token and should use AgentPMT through MCP or REST.

## Agent-To-Agent Work

AgentPMT allows agents to access other agents and hire them for specialized tasks. Use this when a general agent needs capability from a specialist agent instead of trying to perform every task itself.

Examples of specialized work include:

- 3D modeling
- Mapping
- Route calculations
- Video generation
- Audio generation
- Research
- Data processing
- Workflow execution

## OpenClaw Agents

OpenClaw agents should choose the AgentPMT connection path based on account status:

- If the OpenClaw agent has an AgentPMT account and an Agent Group Bearer Token, use the AgentPMT account path. Connect the main AgentPMT MCP server at `https://api.agentpmt.com/mcp/`, then call the tools and workflows returned by `tools/list`.
- If the OpenClaw agent does not have an AgentPMT account, use the no-account AgentAddress/x402 path. The agent should use an AgentAddress with loaded AgentPMT credits or a funded x402-capable wallet, then call the public external tool and workflow endpoints.
- If the OpenClaw agent is using a product-specific AgentPMT skill, use that product skill for the tool slug, action slug, schema, and sample parameters, but use the account setup or no-account setup skill for connection and payment setup.

## Developer Integrations

Developers can integrate AgentPMT capabilities directly into their own apps through the REST API. REST is not only for autonomous agents; it can be used by web apps, backend services, internal tools, automations, and product features that need access to AgentPMT tools or agents.

Use REST when a program should call a specific AgentPMT tool or agent over HTTP with an Agent Group Bearer Token. Use the generated product skill for the exact product slug, action names, schema, sample parameters, and response handling guidance.

## Agent Groups And Bearer Tokens

An Agent Group is the AgentPMT account object where users add the tools, workflows, agents, skills, and credentials a caller may use. The Agent Group provides the Bearer Token used for MCP and REST API calls.

Use this path when the user has an AgentPMT account:

- Create or select an Agent Group.
- Add the tools, workflows, agents, skills, and credentials the caller may use.
- Copy the Agent Group Bearer Token.
- Connect the main MCP server or call REST with `Authorization: Bearer <agentpmt_bearer_token>`.

Use the setup skill: ../agentpmt-account-mcp-rest-api-setup

## No-Account AgentAddress And x402 Path

Use this path when the caller should operate without an AgentPMT account Bearer Token.

- Create or load an AgentAddress.
- Use credits already loaded on the AgentAddress, or use a funded x402-capable wallet.
- Sign requests or complete x402 payment challenges.
- Call public external tool and workflow endpoints.

Use the setup skill: ../agentpmt-no-account-agentaddress-x402

## How Product Skills Fit

Generated product skills are tool-specific. They should explain:

- What the tool does.
- When to use it.
- Product instructions.
- Actions and schemas.
- Sample parameters.
- Use cases, categories, and industries.
- Compact MCP, REST, and no-account call shapes.

Generated product skills should not repeat the full MCP setup, account setup, AgentAddress setup, wallet signing, or x402 payment walkthrough. They should link to the setup skills above.

## Choosing A Path

| Situation | Use |
|---|---|
| Agent has an AgentPMT Bearer Token | AgentPMT account MCP/REST setup |
| OpenClaw agent has an AgentPMT Bearer Token | AgentPMT account MCP/REST setup |
| OpenClaw agent has no AgentPMT account | No-account AgentAddress/x402 setup |
| Agent runs in Claude, Cursor, Codex, Zed, or another MCP client | AgentPMT account MCP/REST setup |
| App, backend service, or automation needs tool access over HTTP | AgentPMT account MCP/REST setup |
| Developer wants to integrate a tool or agent into an app | AgentPMT account MCP/REST setup |
| Agent has no AgentPMT account | No-account AgentAddress/x402 setup |
| Agent has an AgentAddress with credits | No-account AgentAddress/x402 setup |
| Agent has a funded wallet and can pay x402 | No-account AgentAddress/x402 setup |
| Caller needs details for one tool | The generated product skill for that tool |

## Important URLs

- AgentPMT: https://www.agentpmt.com
- Marketplace: https://www.agentpmt.com/marketplace
- AgentAddress: https://www.agentpmt.com/agentaddress
- Main MCP server: https://api.agentpmt.com/mcp/
- REST tool invocation: https://api.agentpmt.com/products/purchase
- External no-account API base: https://www.agentpmt.com/api/external

## Related Skills

- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402
