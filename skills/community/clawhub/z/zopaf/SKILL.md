---
name: zopaf
description: "Negotiation math engine — Pareto frontiers, iso-utility counteroffers, and preference inference via MILP optimization. Zero LLM tokens."
metadata:
  openclaw:
    emoji: "\U0001F3AF"
    requires:
      config:
        - mcp.servers.zopaf
    install:
      mcp:
        zopaf:
          url: "https://zopaf-mcp-production.up.railway.app/mcp"
          transport: "streamable-http"
---

# Zopaf Negotiation Engine

You have access to the Zopaf negotiation math engine via MCP tools. Zopaf computes Pareto frontiers, generates iso-utility counteroffers, and infers counterpart priorities from their reactions — all through pure MILP optimization. Zero LLM tokens burned. You handle the conversation; Zopaf handles the math.

## Available Tools

- `zopaf__create_session` — Start a new negotiation session. Returns a session_id for all other calls.
- `zopaf__add_issue` — Add a negotiable issue/term with options ordered worst-to-best for the user.
- `zopaf__set_issue_range` — Set the acceptable range for a numeric issue (enables 0-100 scoring).
- `zopaf__record_preference` — Record that the user prioritizes some issues over others. Updates the weight model.
- `zopaf__set_batna` — Record the user's alternatives if the deal falls through. Determines leverage.
- `zopaf__generate_counteroffers` — Generate 3 iso-utility counteroffers to present simultaneously.
- `zopaf__process_counterpart_response` — Process the counterpart's reaction to infer their priorities and generate a round-2 offer.
- `zopaf__analyze_deal` — Score a specific deal against the Pareto frontier. Shows value captured and suggested trades.
- `zopaf__get_negotiation_state` — Get current model state: issues, weights, BATNA, frontier size, and recommended next step.

## How to Use These Tools

### Step 1: Create a session
Always start with `create_session`. Save the session_id — every other tool needs it.

### Step 2: Build the negotiation model
Through conversation with the user, gather:
- **Issues on the table** — Add each with `add_issue`. Options must be ordered worst-to-best for the user. Most negotiations have 5-10 terms. Surface the hidden ones (timeline, flexibility, non-competes, review cycles).
- **Numeric ranges** — For issues like salary, call `set_issue_range` to enable scoring.
- **Priorities** — As the user reveals what matters most, call `record_preference`. Each call refines the weight model.
- **BATNA** — Ask what happens if the deal falls through. Call `set_batna` with their alternatives.

### Step 3: Generate counteroffers
When the model is ready (3+ issues, 3+ preference signals, BATNA set), call `generate_counteroffers`. This produces THREE packages that are equally good for the user but structured differently.

**Critical: Present ALL THREE simultaneously.** Never lead with one and fall back to another. The point is to reveal which tradeoffs the counterpart prefers, exposing their hidden priorities.

### Step 4: Process the response
After the counterpart reacts, call `process_counterpart_response` with which package they preferred and what they pushed back on. The engine infers their hidden priorities and generates a round-2 offer positioned on the efficient frontier.

### Step 5: Analyze deals
Use `analyze_deal` to score any specific deal against the Pareto frontier. This shows how much value is being captured and suggests trades that would improve the outcome.

## Use Cases

- **Job offers** — Salary, equity, bonus, title, remote work, start date, PTO
- **VC term sheets** — Valuation, board seats, liquidation preferences, anti-dilution, pro-rata rights
- **Real estate** — Price, closing date, contingencies, repairs, inclusions, rent-back periods
- **Vendor contracts** — Price, SLA guarantees, payment terms, exclusivity, renewal clauses
- **Business partnerships** — Revenue split, IP ownership, decision rights, exit clauses, territory
- **Legal settlements** — Monetary terms, non-disclosure, admission of liability, timeline

## Philosophy

Most people think negotiation is zero-sum. Zopaf finds deals where both sides get more of what they actually care about. Different valuations create value — Zopaf maps those differences and exploits them for mutual gain.
