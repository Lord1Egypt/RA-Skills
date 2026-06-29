# Agent-native routing and pricing structure

Sage Router now mirrors the useful agent-native pieces from BlockRunAI/ClawRouter without adding a mandatory hosted middle layer.

## Agent-native features

- **Agentic auto-detection**: requests with tool definitions or multi-step execution language are marked `agentic` and prefer models with stronger autonomous/tool-use behavior.
- **Tool-aware routing**: forced tool calls remain hard requirements; ordinary tool arrays become a soft preference so casual chat is not over-constrained.
- **Context-aware routing**: document, vision, and long-context signals are folded into requirements before candidate scoring.
- **Session-safe fallback**: each request gets an ordered fallback chain; failed providers are retried sequentially with no mid-stream model handoff.
- **Fusion synthesis**: premium chat requests can call `sage-router/fusion` or attach the `{"type":"sage-router:fusion"}` server tool, which runs a small parallel panel of eligible authorized routes and asks a judge route to synthesize one final answer.
- **Cost/plan telemetry**: route events retain selected model, attempts, elapsed time, auth type, and customer plan.
- **Free/eco fallback policy**: low-cost workflows can select `eco` or `local-first` profiles to avoid paid frontier calls.

Public endpoint:

```bash
curl http://localhost:8790/features/agent-native
```

## Routing profiles

- `sage-router/balanced`: Ollama subscription/local-first route for everyday agent and app traffic, with Codex and cloud fallback providers available for health and 429 resilience.
- `sage-router/agentic`: best-route profile for multi-step agent work, tool preference, and strong model families such as Kimi, Codex, GPT-5, Claude/Sonnet/Opus, and Gemini Pro/3.
- `sage-router/eco`: cost-first/local-first profile that avoids expensive frontier defaults.
- `sage-router/fusion`: Pro/Max/metered multi-model panel plus judge synthesis for prompts where multiple perspectives are worth the extra latency and cost. Gateway-style clients can also request the same route with the `sage-router:fusion` server tool.
- `sage-router/premium`: quality-first paid profile for frontier/large model usage.

## Pricing structure

The public catalog uses the ClawRouter-style plan ladder:

- `free`: $0/month, local/free providers when available.
- `lite`: $6/month or $27/quarter, agent-native routing, API keys, usage analytics, standard fallback chains.
- `pro`: $30/month or $81/quarter, frontier routing, agentic tool-use preference, Fusion synthesis, analytics snapshots, subscription failover.
- `max`: $72/month or $216/quarter, highest-quality routing, frontier/large-model preference, priority fallback and Fusion budget.
- `metered`: usage-based, $0.001 minimum payment and 5% server margin for x402/wallet-style metering.

Public endpoint:

```bash
curl http://localhost:8790/pricing
```

Stripe checkout accepts a plan:

```bash
curl -X POST http://localhost:8790/billing/stripe/checkout \
  -H "Authorization: Bearer $SUPABASE_USER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"plan":"pro"}'
```

Configure plan price IDs with:

```bash
SAGE_ROUTER_STRIPE_PRICE_IDS=lite=price_lite,pro=price_pro,max=price_max
```

`SAGE_ROUTER_STRIPE_PRICE_ID` / `STRIPE_PRICE_ID` remains backward-compatible as the `pro` plan price.
