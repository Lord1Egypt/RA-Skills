# Zopaf Negotiation Engine -- MCP Directory Submissions

## Table of Contents

1. [Smithery.ai](#1-smitheryai)
2. [mcp.run](#2-mcprun)
3. [Glama.ai MCP](#3-glamaai-mcp)
4. [awesome-mcp-servers GitHub](#4-awesome-mcp-servers-github)

---

## 1. Smithery.ai

Smithery requires a `smithery.yaml` config file in your repo root and a listing submitted via their web UI or CLI. Below is the config file content and the listing metadata.

### smithery.yaml (place in repo root)

```yaml
# smithery.yaml
startCommand:
  type: http
  configSchema:
    type: object
    properties: {}
  url: https://zopaf-mcp-production.up.railway.app/mcp
```

### Listing Metadata

- **Name:** Zopaf Negotiation Engine
- **Slug:** zopaf-negotiation-engine
- **Repository:** https://github.com/rjandino/negotiation-coach
- **Server URL:** https://zopaf-mcp-production.up.railway.app/mcp
- **Transport:** Streamable HTTP

### Short Description (for card/preview)

Pure-math negotiation coach. MILP optimization and Pareto frontier analysis with zero LLM token cost -- the calling agent brings its own LLM, Zopaf does the math.

### Full Description

Zopaf Negotiation Engine turns any LLM agent into a quantitative negotiation coach. It handles the hard math -- MILP optimization, Pareto frontier computation, preference weight solving, and iso-utility counteroffer generation -- while your agent handles the conversation.

**Zero LLM token cost.** Zopaf is a pure computation engine. No internal LLM calls, no API keys needed. The calling agent (Claude, GPT, Llama, or any MCP client) provides the language layer.

**Works with any negotiation:** job offers, VC term sheets, real estate, vendor contracts, salary reviews, partnership agreements, and more.

**9 tools for a complete negotiation workflow:**

| Tool | Purpose |
|------|---------|
| `create_session` | Start a new negotiation session |
| `add_issue` | Add a negotiable term (options ordered worst to best) |
| `set_issue_range` | Set numeric range for proper 0-100 scoring |
| `set_batna` | Record alternatives; determines leverage strategy |
| `record_preference` | Learn user priorities from tradeoff choices |
| `analyze_deal` | Score a deal against the Pareto frontier |
| `generate_counteroffers` | Generate 3 iso-utility packages (present all simultaneously) |
| `process_counterpart_response` | Infer counterpart priorities from their reaction |
| `get_negotiation_state` | Full model state + next-step guidance |

**Key capabilities:**

- Computes the Pareto-efficient frontier across all negotiable issues
- Generates 3 equally-good counteroffers structured differently -- presenting all three simultaneously reveals the counterpart's true priorities
- BATNA-weighted value splitting: users with stronger alternatives capture more surplus
- Learns user priorities incrementally through pairwise tradeoff questions
- Infers counterpart priorities from their reactions to the triple-offer strategy

### Tags

`negotiation`, `optimization`, `pareto`, `milp`, `game-theory`, `decision-support`, `math`, `zero-token`, `hosted`

---

## 2. mcp.run

mcp.run focuses on hosted/runnable MCP servers. Submit via their web interface at https://mcp.run.

### Listing Information

- **Name:** Zopaf Negotiation Engine
- **Author:** rjandino
- **Source:** https://github.com/rjandino/negotiation-coach
- **Endpoint:** https://zopaf-mcp-production.up.railway.app/mcp
- **Transport:** Streamable HTTP
- **Auth Required:** No
- **Runtime:** Python (FastMCP)

### Short Description

Quantitative negotiation coach -- MILP optimization and Pareto frontier analysis with zero LLM token cost. Turns any agent into a deal-making strategist.

### Full Description

Zopaf Negotiation Engine is a hosted MCP server that provides pure-math negotiation intelligence to any LLM agent. No internal LLM calls, no API keys, no token costs -- just optimization math.

**What it does:**

Your agent conducts the negotiation conversation with the user. When it needs analytical firepower, it calls Zopaf's tools to:

- Model the negotiation as a multi-issue optimization problem
- Compute the Pareto-efficient frontier (the set of deals where neither side can improve without the other losing)
- Generate 3 iso-utility counteroffers -- equally good for your user but structured differently. Presenting all three at once forces the counterpart to reveal their real priorities.
- Score any proposed deal against the frontier to quantify how much value is being left on the table
- Adjust strategy based on BATNA strength (alternatives determine how aggressively to anchor)

**9 tools covering the full negotiation lifecycle:** session management, issue modeling, preference elicitation, deal analysis, counteroffer generation, counterpart inference, and state tracking.

**Works with any negotiation type:** salary, equity, start dates, real estate terms, vendor contracts, VC term sheets, partnership agreements -- anything with multiple issues to trade.

**Model-agnostic:** Claude, GPT-4, Llama, Mistral, or any MCP-compatible agent. Zopaf provides the math; your model provides the language.

### Category

Productivity / Decision Support

### Tags

`negotiation`, `optimization`, `pareto`, `math`, `zero-cost`, `hosted`

---

## 3. Glama.ai MCP

Glama's MCP directory accepts submissions via their web form or GitHub integration. Below is the listing content.

### Listing Information

- **Name:** Zopaf Negotiation Engine
- **Server URL:** https://zopaf-mcp-production.up.railway.app/mcp
- **GitHub Repository:** https://github.com/rjandino/negotiation-coach
- **Transport:** Streamable HTTP
- **Category:** Productivity & Decision Making

### Short Description

Pure-math negotiation engine with zero LLM token cost. MILP optimization, Pareto frontier analysis, and iso-utility counteroffer generation for any multi-issue negotiation.

### Full Description

Zopaf Negotiation Engine is a hosted MCP server that gives any LLM agent rigorous negotiation analytics -- without burning a single LLM token internally. All computation is pure math: mixed-integer linear programming, Pareto frontier enumeration, and preference weight solving.

**The problem it solves:** LLMs are good conversationalists but poor negotiators. They lack the mathematical framework to identify efficient tradeoffs, quantify leverage, or generate strategically structured counteroffers. Zopaf fills that gap.

**How it works:**

1. The agent gathers negotiation context through conversation and feeds it to Zopaf via `add_issue`, `set_issue_range`, and `record_preference`
2. Zopaf builds a multi-dimensional utility model and computes the Pareto frontier
3. When it is time to make a move, `generate_counteroffers` produces 3 iso-utility packages -- deals that are equally good for the user but emphasize different issues
4. Presenting all 3 simultaneously is a deliberate strategy: the counterpart's preference reveals their hidden priorities
5. `process_counterpart_response` ingests that signal and generates a refined round-2 offer positioned on the efficient frontier, weighted by BATNA strength

**9 tools:**

- `create_session` -- Initialize a negotiation session
- `add_issue` -- Define negotiable terms with options ordered worst-to-best
- `set_issue_range` -- Map numeric values to 0-100 satisfaction scores
- `set_batna` -- Record walk-away alternatives; drives anchoring strategy
- `record_preference` -- Capture priority tradeoffs to build the weight model
- `analyze_deal` -- Score any deal against the Pareto frontier
- `generate_counteroffers` -- 3 equally-valued packages structured to reveal counterpart priorities
- `process_counterpart_response` -- Infer counterpart weights and generate BATNA-weighted round-2 offer
- `get_negotiation_state` -- Full model dump with next-step recommendations

**Use cases:** Job offer negotiations, VC term sheets, real estate deals, vendor/supplier contracts, salary reviews, partnership agreements, freelance rate negotiations.

**Zero dependencies on any specific LLM.** Works with Claude, GPT, Llama, Gemini, or any MCP-compatible client.

### Tags

`negotiation`, `optimization`, `pareto-frontier`, `milp`, `game-theory`, `decision-support`, `productivity`, `zero-token-cost`, `hosted`, `model-agnostic`

---

## 4. awesome-mcp-servers GitHub

Repository: https://github.com/punkpeye/awesome-mcp-servers

Submit as a pull request adding an entry to the README. The list is organized by category with entries in the format: `- [Name](url) - Description`.

### PR Title

Add Zopaf Negotiation Engine (MILP optimization + Pareto frontier analysis)

### PR Body

```
Adds Zopaf Negotiation Engine to the Knowledge & Memory section (or Productivity, depending on current categories).

Zopaf is a hosted MCP server that provides pure-math negotiation coaching -- MILP optimization, Pareto frontier analysis, and iso-utility counteroffer generation -- with zero internal LLM token cost.

- Server URL: https://zopaf-mcp-production.up.railway.app/mcp
- GitHub: https://github.com/rjandino/negotiation-coach
- 9 tools covering the full negotiation lifecycle
- Works with any MCP-compatible agent (Claude, GPT, Llama, etc.)
```

### Entry to Add (under "Productivity" or most relevant category)

```markdown
- [Zopaf Negotiation Engine](https://github.com/rjandino/negotiation-coach) - Pure-math negotiation coach with zero LLM token cost. MILP optimization, Pareto frontier analysis, and iso-utility counteroffer generation for any multi-issue negotiation (job offers, term sheets, real estate, vendor contracts). Generates 3 equally-good counteroffers that reveal counterpart priorities when presented simultaneously.
```

### Alternative shorter entry (if the list prefers brevity)

```markdown
- [Zopaf Negotiation Engine](https://github.com/rjandino/negotiation-coach) - Quantitative negotiation coach using MILP optimization and Pareto frontier analysis. Zero LLM token cost -- pure math engine for any multi-issue negotiation.
```

---

## Quick Reference: Connection Details for All Directories

| Field | Value |
|-------|-------|
| Server Name | Zopaf Negotiation Engine |
| Endpoint URL | `https://zopaf-mcp-production.up.railway.app/mcp` |
| Transport | Streamable HTTP |
| GitHub Repo | `https://github.com/rjandino/negotiation-coach` |
| Auth Required | No |
| Tool Count | 9 |
| LLM Token Cost | Zero (pure math engine) |
| Runtime | Python 3, FastMCP, PuLP (MILP), NumPy, SciPy |

## MCP Client Configuration (for documentation/README)

```json
{
  "mcpServers": {
    "zopaf": {
      "url": "https://zopaf-mcp-production.up.railway.app/mcp"
    }
  }
}
```
