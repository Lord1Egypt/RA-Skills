---
name: verificate
description: "The trust layer for OpenClaw. Verify AI-written code, tool calls and research answers before you trust them — 17 deterministic reality gates + a frontier-model review with veto power. Free to try, no signup."
homepage: https://verificate.ai/mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": {},
        "mcp":
          {
            "verificate":
              {
                "type": "http",
                "url": "https://mcp.verificate.ai/mcp",
              },
          },
      },
  }
---

# verificate

**The trust layer for OpenClaw.** ClawHub skills are powerful but untrusted — Snyk audits keep finding prompt injection, malware and credential theft in community skills, and every AI answer sounds confident whether it's right or wrong. Verificate is the skill that verifies the others.

It connects OpenClaw to the hosted Verificate MCP server (no signup — 25 free validations per machine):

- **`validate_ai_output`** — the merge gate for AI-written code *and* documents: 17 deterministic reality gates (mock/placeholder veto, invented-API checks, false-completion detection) run first and can't be overridden, then a frontier-model review scores what survives. Binary approve/reject with severity-ranked findings.
- **`validate_plan`** — gate a design or plan before any code is written.
- **`analyze_code`** — advisory deep-dive: performance, scalability, failure modes. No verdict, never blocks.
- **`generate_code`** — generate code and gate it in one step.

## Quick start

```
openclaw mcp add verificate --http https://mcp.verificate.ai/mcp
```

Then ask OpenClaw to *"validate this with verificate before you finish."* A real rejection, verbatim from the production gateway: *"`stripe.Inventory` is not a valid Stripe SDK resource"* · *"N+1 synchronous API calls … will trigger Stripe rate limiting"* · *"Stripe API requires integer cents."* Each is an afternoon of production debugging, caught in seconds.

## Guard every interaction (recommended)

Add this to your OpenClaw agent instructions so it self-gates instead of you asking each time:

```text
Before you present any substantive code change, document, or plan as finished,
call validate_ai_output (validate_plan for designs). If REJECTED, fix every
finding and validate again — never present rejected work. Tell me, in one line,
whatever the gate catches.
```

## Trust & privacy

Read-only: your code is analyzed, never executed, never used to train models. The skill's only network call is to `https://mcp.verificate.ai/mcp` — no other egress, nothing to exfiltrate. Open source. Privacy policy: https://verificate.ai/privacy

After the free 25, a 30-day trial (no card, then $30/mo): https://verificate.ai/auth/signup
