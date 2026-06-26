# Zopaf Social Posts

## X/Twitter

### Main launch post

I built a negotiation math engine that any AI agent can use.

One URL. 9 tools. Zero LLM tokens.

It computes Pareto frontiers, generates iso-utility counteroffers, and infers what the other side really cares about — pure MILP optimization, no language model needed.

The trick: generate 3 offers that are equally good for you but structured differently. Present all 3 simultaneously. Whichever one they pick reveals their hidden priorities. Then you exploit that on round 2.

Works with Claude, GPT, Llama — any MCP-compatible agent.

Job offers. VC term sheets. Real estate. Vendor contracts. Anything with multiple terms to trade.

Your agent brings the brain. Zopaf brings the calculator.

https://smithery.ai/servers/zopaf/negotiation-engine

### Thread follow-up (reply to main post)

How the 3-offer strategy works:

Say you're negotiating a job. You care about salary and equity. They care about start date and remote policy.

Zopaf generates 3 packages that score identically for you:
A: $180K, 0.25% equity, on-site, start in 2 weeks
B: $170K, 0.5% equity, hybrid, start in 1 month
C: $160K, 0.75% equity, remote, start in 2 months

They pick B and push back on equity.

Now Zopaf knows: they weight equity at 57%. Round 2 concedes there (cheap for you) and captures value on salary (expensive for them).

Both sides improve. You just improve more.

### Short version (if you want punchy)

Built a negotiation engine for AI agents.

Agents bring the conversation. Zopaf brings the math.

- Pareto frontiers
- Iso-utility counteroffers
- Counterpart priority inference
- BATNA-weighted value splitting

9 MCP tools. Zero tokens. One URL.

https://smithery.ai/servers/zopaf/negotiation-engine

---

## LinkedIn

Most people negotiate 1-2 issues. There are usually 5-10. The terms you haven't thought about are where the most value is hiding.

I built Zopaf — a negotiation math engine that any AI agent can plug into. It's now live as an MCP server that Claude, GPT, or any agent can connect to with a single URL.

What it does:
- Maps the entire deal space using MILP optimization
- Computes the Pareto-efficient frontier (the set of deals where neither side can improve without the other losing)
- Generates 3 counteroffers that are equally good for you but structured differently
- When the counterpart picks one, the engine infers what they actually care about
- Round 2 exploits that information, weighted by your leverage

What it doesn't do:
- Burn LLM tokens. It's pure math — the calling agent handles conversation, Zopaf handles optimization.
- Cost you anything. Zero token cost for any agent that connects.

It works with any multi-issue negotiation: job offers, VC term sheets, real estate, vendor contracts, salary reviews, partnership agreements.

The insight behind the 3-offer strategy: presenting multiple equally-valued packages is not about giving options. It's an information extraction mechanism. The counterpart's preference is a signal about their hidden utility function. Once you have that signal, you can move toward the efficient frontier while capturing more of the surplus.

Live now on Smithery: https://smithery.ai/servers/zopaf/negotiation-engine

If you negotiate deals — or build agents that do — try it.

#AI #MCP #negotiation #agents

---

## Hacker News

### Title
Show HN: Zopaf – Negotiation math engine as MCP tools (zero LLM tokens)

### Text
I built a negotiation math engine exposed as MCP tools. Any AI agent (Claude, GPT, Llama) can connect to it with a single URL and get quantitative negotiation coaching — Pareto frontier analysis, iso-utility counteroffer generation, counterpart priority inference — without burning any LLM tokens.

The core idea: most negotiations have 5-10 terms, but people fixate on 1-2. The hidden terms are where the real value lives. Zopaf models the full deal space using MILP optimization (PuLP solver) and generates 3 equally-good counteroffers structured differently. When you present all 3 simultaneously, the counterpart's preference reveals their priorities. Round 2 exploits that signal.

The math engine runs on a hosted server. Agents call 9 tools via MCP's Streamable HTTP transport:

- create_session, add_issue, set_issue_range — model the deal
- record_preference — learn user priorities via tradeoff questions
- set_batna — record alternatives, determines anchoring strategy
- generate_counteroffers — 3 iso-utility packages
- process_counterpart_response — infer counterpart weights, generate round-2 offer
- analyze_deal — score any deal against the Pareto frontier
- get_negotiation_state — full model state + next step

The calling agent's LLM handles the conversation. Zopaf handles the optimization. Token cost: $0.

Works with any negotiation: job offers, VC term sheets, real estate, vendor contracts, salary, partnerships.

Server: https://zopaf-mcp-production.up.railway.app/mcp
Smithery: https://smithery.ai/servers/zopaf/negotiation-engine
GitHub (docs): https://github.com/rjandino/zopaf
