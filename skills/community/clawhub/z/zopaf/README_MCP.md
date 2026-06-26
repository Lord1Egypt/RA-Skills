# Zopaf Negotiation Engine -- MCP Server

A negotiation math engine exposed as MCP tools that any AI agent can call. Zopaf computes Pareto frontiers, generates iso-utility counteroffers, and infers counterpart priorities from their reactions -- all through pure MILP optimization. Zero LLM tokens burned. The calling agent handles the conversation; Zopaf handles the math.

## Quick Start

### Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "zopaf": {
      "type": "streamable-http",
      "url": "https://zopaf-mcp-production.up.railway.app/mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add zopaf --transport streamable-http https://zopaf-mcp-production.up.railway.app/mcp
```

### OpenClaw

```bash
openclaw mcp set zopaf '{"url":"https://zopaf-mcp-production.up.railway.app/mcp","transport":"streamable-http"}'
```

Or install from ClawHub:

```bash
openclaw skills install zopaf
```

### NemoClaw (NVIDIA)

Zopaf runs on [NemoClaw](https://www.nvidia.com/en-us/ai/nemoclaw/) — NVIDIA's enterprise agent platform built on OpenClaw. Same MCP setup, but agents run locally on RTX hardware with Nemotron models. No deal terms leave your network.

```bash
openclaw mcp set zopaf '{"url":"https://zopaf-mcp-production.up.railway.app/mcp","transport":"streamable-http"}'
```

For fully on-prem deployments (e.g., enterprise procurement), run the Zopaf MCP server locally:

```bash
git clone https://github.com/rjandino/zopaf.git
cd zopaf && pip install -r requirements.txt
openclaw mcp set zopaf '{"command":"python3","args":["zopaf_mcp_server.py"],"cwd":"/path/to/zopaf"}'
```

This keeps all negotiation data — deal terms, counterpart priorities, BATNA analysis — entirely on-prem. Ideal for procurement, M&A, and any negotiation where terms are confidential.

### Generic MCP Client

Connect to the Streamable HTTP endpoint:

```
URL: https://zopaf-mcp-production.up.railway.app/mcp
Transport: Streamable HTTP
```

## Tools Reference

| Tool | Description |
|------|-------------|
| `create_session` | Create a new negotiation session. Returns a session_id used by all other tools. |
| `add_issue` | Add a negotiable issue/term with options ordered worst to best for the user. |
| `set_issue_range` | Set the acceptable range for a numeric issue, enabling 0-100 scoring. |
| `record_preference` | Record that the user prioritizes some issues over others. Updates the weight model. |
| `set_batna` | Record the user's alternatives if the deal falls through. Determines leverage. |
| `generate_counteroffers` | Generate 3 iso-utility counteroffers to present simultaneously. |
| `process_counterpart_response` | Process the counterpart's reaction to infer their priorities and generate a round-2 offer. |
| `analyze_deal` | Score a specific deal against the Pareto frontier. Shows value captured and suggested trades. |
| `get_negotiation_state` | Get current model state: issues, weights, BATNA, frontier size, and recommended next step. |

## How It Works

1. **Create session** -- Initialize a new negotiation model with `create_session`.

2. **Add issues** -- Define the terms on the table with `add_issue`. Each issue includes options ordered worst to best for the user (e.g., Salary: `['$150K', '$160K', '$170K', '$180K']`).

3. **Set ranges** -- For numeric issues, call `set_issue_range` to map values onto a 0-100 scoring scale.

4. **Record preferences** -- Call `record_preference` as you learn what the user cares about. Each call updates the internal weight model.

5. **Set BATNA** -- Use `set_batna` to record alternatives. The number and quality determines leverage strength and anchoring strategy.

6. **Generate 3 counteroffers** -- Call `generate_counteroffers` to produce three packages that are equally good for the user but structured differently. Present ALL THREE simultaneously. Never lead with one and fall back to another.

7. **Process counterpart response** -- Call `process_counterpart_response` with which package they preferred and what they pushed back on. The engine infers their hidden priorities.

8. **Get round-2 offer** -- Returns a refined offer on the efficient frontier, with value split weighted by leverage.

## Example: Job Offer Negotiation

```
create_session
-> {"session_id": "a1b2c3d4"}

add_issue(session_id="a1b2c3d4", issue_name="Salary", options=["$150K", "$160K", "$170K", "$180K"])
add_issue(session_id="a1b2c3d4", issue_name="Equity", options=["0.1%", "0.25%", "0.5%", "0.75%"])
add_issue(session_id="a1b2c3d4", issue_name="Signing Bonus", options=["$0", "$10K", "$20K", "$30K"])
add_issue(session_id="a1b2c3d4", issue_name="Remote Work", options=["On-site", "Hybrid", "Fully Remote"])

set_issue_range(issue_name="Salary", worst_acceptable=150000, best_hoped=180000,
    option_values={"$150K": 150000, "$160K": 160000, "$170K": 170000, "$180K": 180000})
-> {"scores": {"$150K": 0.0, "$160K": 33.3, "$170K": 66.7, "$180K": 100.0}}

record_preference(preferred_issues=["Salary", "Equity"], over_issues=["Signing Bonus", "Remote Work"])
-> {"learned_weights": {"Salary": 0.345, "Equity": 0.345, "Signing Bonus": 0.155, "Remote Work": 0.155}}

set_batna(alternatives=["Competing offer from Company B at $165K", "Stay in current role"])
-> {"leverage_strength": "strong"}

generate_counteroffers(target_satisfaction="ambitious")
-> {
  "counteroffers": [
    {"label": "A", "terms": {"Salary": "$180K", "Equity": "0.25%", "Signing Bonus": "$10K", "Remote Work": "On-site"}},
    {"label": "B", "terms": {"Salary": "$170K", "Equity": "0.5%", "Signing Bonus": "$0", "Remote Work": "Hybrid"}},
    {"label": "C", "terms": {"Salary": "$160K", "Equity": "0.75%", "Signing Bonus": "$20K", "Remote Work": "On-site"}}
  ]
}

process_counterpart_response(preferred_package="B", pushback_issues=["Equity"])
-> {
  "counterpart_priorities_inferred": {"Equity": 0.571, "Salary": 0.143, ...},
  "round_2_offer": {"Salary": "$180K", "Equity": "0.25%", "Signing Bonus": "$20K", "Remote Work": "Hybrid"},
  "value_split": "User gets 75% of surplus"
}
```

The engine inferred that the counterpart cares most about equity (57% of their weight). The round-2 offer concedes on equity -- where it costs the user less -- and captures value on salary and signing bonus. Both sides improve. The user captures 75% of the surplus based on their strong BATNA.

## Use Cases

- **Job offers** -- Salary, equity, bonus, title, remote work, start date, PTO
- **VC term sheets** -- Valuation, board seats, liquidation preferences, anti-dilution, pro-rata rights
- **Real estate** -- Price, closing date, contingencies, repairs, inclusions, rent-back periods
- **Vendor contracts** -- Price, SLA guarantees, payment terms, exclusivity, renewal clauses
- **Salary negotiations** -- Base pay, bonus structure, review timeline, scope of role
- **Business partnerships** -- Revenue split, IP ownership, decision rights, exit clauses, territory
- **Legal settlements** -- Monetary terms, non-disclosure terms, admission of liability, timeline

## Enterprise: Procurement & High-Stakes Negotiations

Zopaf on NemoClaw is built for enterprise teams that negotiate repeatedly at scale:

- **Procurement** — Vendor contracts, SLA terms, payment schedules, volume discounts, exclusivity clauses. Run Zopaf on-prem so no supplier terms or internal pricing models leave your network.
- **M&A** — Model complex multi-party deal structures with dozens of interdependent terms. Pareto frontier analysis shows where both sides can gain.
- **Real estate portfolios** — Standardize negotiation strategy across property managers. Each deal feeds back into the model.
- **Licensing & partnerships** — Revenue splits, IP rights, territory, renewal terms. Generate iso-utility packages that reveal what the counterpart actually values.

The on-prem NemoClaw deployment means your negotiation intelligence — learned counterpart priorities, BATNA assessments, historical deal patterns — stays inside your firewall.

## Why Zero Tokens?

Zopaf is a math engine, not a language model. It runs MILP optimization and combinatorial scoring -- operations that are computationally cheap but tedious for an LLM to attempt in-context.

Your agent's LLM handles the conversation with the user, asks the right questions, and explains the strategy. Zopaf handles the optimization -- computing Pareto frontiers, generating iso-utility packages, solving preference weights from revealed choices, and positioning offers on the efficient frontier.

You bring the brain. Zopaf brings the calculator.
