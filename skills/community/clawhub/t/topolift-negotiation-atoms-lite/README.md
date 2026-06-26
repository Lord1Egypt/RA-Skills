# TopoLift: Negotiation Skill (v1.2)

The public dialect skill for **TopoLift atom-grounded negotiation reasoning**.

The atom corpus stays on TopoLift's GPU. What this skill ships — and teaches
your agent — is the public **dialect**: the closed vocabulary in which
TopoLift speaks, plus the three ways to call the live reasoning API.

## What you get

When an MCP-aware agent loads this skill, it learns to read TopoLift's
**bilingual** API responses:

- A typed `topology` object (`regime`, `load_bearing_strategies[]`,
  `bridge_pivots[]`, `topology_signals{}`) drawn from a closed vocabulary
- Prose with inline `[Cluster_X#strategy1,strategy2]` citation tokens
  anchoring every claim to the cluster + load-bearing atoms that drove it

## Live dialect endpoint

```bash
curl https://api.topolift.ai/v1/dialect
```

No auth. No rate limit. Returns the canonical vocabulary your agent needs.

## Three install paths

### MCP (Claude Code / Cursor / Agents SDK)

```bash
pip install topolift-mcp
claude mcp add topolift-negotiation \
  -e TOPOLIFT_API_KEY=tl-... \
  -- topolift-mcp
```

### Bearer key (Stripe-provisioned)

```bash
curl -X POST https://api.topolift.ai/v1/negotiate \
  -H "Authorization: Bearer tl-..." \
  -H "Content-Type: application/json" \
  -d '{...}'
```

Plans: $50 one-time / $49 mo / $99 mo unlimited. Buy at <https://topolift.ai>.

### x402 pay-per-call (autonomous agents)

`$0.10 USDC` per call on Base mainnet. No API key. No signup. Standard x402
protocol via the Coinbase facilitator. POST without auth to get a 402
challenge with `PaymentRequirements`.

## Status of the downloadable atoms

The atom corpus remains paused for download — TopoLift evolves the atoms
continuously, and we don't want stale copies fragmenting the dialect across
agents in the wild. The reasoning is served as a managed API instead.

Pre-pause Lite bundles remain under their original Apache-2.0 license. The
dialect itself (the vocabulary published at `/v1/dialect`) is open and stable.

## Links

- **Site**: <https://topolift.ai>
- **API**: <https://api.topolift.ai>
- **Live dialect**: <https://api.topolift.ai/v1/dialect>
- **MCP server**: <https://github.com/TopoLift/topolift-mcp>
- **PyPI**: <https://pypi.org/project/topolift-mcp/>
- **Official MCP registry**: <https://registry.modelcontextprotocol.io/v0/servers?search=topolift>
- **Contact**: atoms@topolift.ai

— TopoLift
