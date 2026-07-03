---
name: quantum-distribution-generator
description: "Quantum Distribution Generator: Sample from probability distributions (exponential, Poisson, binomial, beta, gamma) with Monte Carlo and. Use when an agent needs quantum distribution generator, monte carlo simulations for risk analysis and option pricing, queuing theory modeling with poisson and exponential distributions, a/b testing and conversion rate analysis using binomial and beta distributions, stochastic process simulation, beta, source, count through AgentPMT-hosted remote tool calls."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/quantum-distribution-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/quantum-distribution-generator"}}
---
# Quantum Distribution Generator

## Freshness
Last updated: `2026-06-29`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Statistical distribution sampling and stochastic simulation powered by quantum or pseudo-random sources. Generate samples from common probability distributions including exponential, Poisson, binomial, beta, and gamma, with support for Monte Carlo sampling and multi-dimensional random walks. Configurable parameters for distribution shapes, sample counts, and dimensionality enable flexible statistical modeling and simulation workflows.

## Product Instructions
### Quantum Distribution Generator

Generate statistical distribution samples, Monte Carlo samples, and random walks. Use the product action name in `action`; the backend also accepts legacy `operation` for compatibility.

#### Actions

##### exponential
Required: `action:"exponential"`.
Optional: `source:"quantum"|"standard"` default `quantum`, `count` 1-10000 default 1, `rate` > 0 default 1.0.
Example: `{"action":"exponential","count":5,"rate":2.5}`

##### poisson
Required: `action:"poisson"`.
Optional: `source`, `count` default 1, `lambda_param` > 0 default 1.0. Quantum source max count: 200.
Example: `{"action":"poisson","count":10,"lambda_param":4.5}`

##### binomial
Required: `action:"binomial"`.
Optional: `source`, `count`, `n_trials` default 10, `p_success` 0-1 default 0.5. Quantum source max count 200 and max n_trials 50.
Example: `{"action":"binomial","count":20,"n_trials":10,"p_success":0.3}`

##### beta
Required: `action:"beta"`.
Optional: `source`, `count`, `alpha` > 0 default 1.0, `beta_param` > 0 default 1.0.
Example: `{"action":"beta","count":10,"alpha":2.0,"beta_param":5.0}`

##### gamma
Required: `action:"gamma"`.
Optional: `source`, `count`, `shape` > 0 default 1.0, `scale` > 0 default 1.0.
Example: `{"action":"gamma","count":15,"shape":2.0,"scale":1.5}`

##### montecarlo_sample
Required: `action:"montecarlo_sample"`.
Optional: `source`, `samples` 1-1000000 default 1000, `dimensions` 1-100 default 1, `distribution_type:"uniform"|"normal"` default `uniform`.
Example: `{"action":"montecarlo_sample","samples":500,"dimensions":3,"distribution_type":"normal"}`

##### randomwalk
Required: `action:"randomwalk"`.
Optional: `source`, `steps` 1-10000 default 100, `dimensions` 1-100 default 1, `step_size` > 0 default 1.0. Quantum source max steps: 80.
Example: `{"action":"randomwalk","steps":50,"dimensions":2,"step_size":0.5}`

## When To Use
- Use this skill for `Quantum Distribution Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: quantum distribution generator, monte carlo simulations for risk analysis and option pricing, queuing theory modeling with poisson and exponential distributions, a/b testing and conversion rate analysis using binomial and beta distributions, stochastic process simulation, beta, source, count.
- Supported action names: `beta`, `binomial`, `exponential`, `gamma`, `montecarlo_sample`, `poisson`, `randomwalk`.

## Use Cases
- Monte Carlo simulations for risk analysis and option pricing
- queuing theory modeling with Poisson and exponential distributions
- A/B testing and conversion rate analysis using binomial and beta distributions
- stochastic process simulation
- particle diffusion and Brownian motion modeling
- Bayesian inference and prior distribution sampling
- financial market random walk simulations
- statistical hypothesis testing
- reliability engineering and failure time analysis.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `7`.
x402 availability: not enabled for this product.

- `beta` (action slug: `beta`): Generate values from a beta distribution, useful for modeling probabilities and proportions. Price: `5` credits. Parameters: `alpha`, `beta_param`, `count`, `source`.
- `binomial` (action slug: `binomial`): Generate values from a binomial distribution, modeling the number of successes in a fixed number of trials. Price: `5` credits. Parameters: `count`, `n_trials`, `p_success`, `source`.
- `exponential` (action slug: `exponential`): Generate values from an exponential distribution, commonly used for modeling wait times and decay processes. Price: `5` credits. Parameters: `count`, `rate`, `source`.
- `gamma` (action slug: `gamma`): Generate values from a gamma distribution, used for modeling wait times and skewed data. Price: `5` credits. Parameters: `count`, `scale`, `shape`, `source`.
- `montecarlo_sample` (action slug: `montecarlo-sample`): Generate multi-dimensional Monte Carlo samples from uniform or normal distributions for simulation and analysis. Price: `5` credits. Parameters: `dimensions`, `distribution_type`, `samples`, `source`.
- `poisson` (action slug: `poisson`): Generate values from a Poisson distribution, used for modeling count-based events (e.g., arrivals per hour). Price: `5` credits. Parameters: `count`, `lambda_param`, `source`.
- `randomwalk` (action slug: `randomwalk`): Simulate a random walk in one or more dimensions starting from the origin. Quantum max 80 steps. Price: `5` credits. Parameters: `dimensions`, `source`, `step_size`, `steps`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "quantum-distribution-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "quantum-distribution-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "quantum-distribution-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "quantum-distribution-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "quantum-distribution-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "quantum-distribution-generator"
  }
}
```

## Call This Tool
Product slug: `quantum-distribution-generator`

Marketplace page: https://www.agentpmt.com/marketplace/quantum-distribution-generator

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
    "name": "Quantum-Distribution-Generator",
    "arguments": {
      "action": "beta",
      "alpha": 1,
      "beta_param": 1,
      "count": 1,
      "source": "quantum"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "quantum-distribution-generator",
  "parameters": {
    "action": "beta",
    "alpha": 1,
    "beta_param": 1,
    "count": 1,
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
- If `beta` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/quantum-distribution-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
