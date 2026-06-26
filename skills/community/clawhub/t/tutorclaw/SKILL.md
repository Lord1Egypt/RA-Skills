---
name: tutorclaw
version: 1.0.1
description: "AI programming tutor for the AI Agent Factory curriculum using PRIMM-Lite pedagogy. Bundles agent brain files, offline shim, and MCP server config."
metadata:
  openclaw:
    requires:
      openclaw: ">=2.0.0"
      python: ">=3.11"
    env:
      - name: STRIPE_SECRET_KEY
        description: "Stripe secret key for payment tier enforcement"
        required: true
      - name: GEMINI_API_KEY
        description: "Gemini API key for the OpenClaw gateway model"
        required: true
---

# TutorClaw

AI programming tutor for the AI Agent Factory curriculum. Teaches Python
using the PRIMM-Lite (Predict-Run-Investigate) methodology.

## What this package installs

| File | Installs to | Purpose |
|---|---|---|
| `tutorclaw/AGENTS.md` | `agents/tutorclaw/AGENTS.md` | Tool orchestration and session flow |
| `SOUL.md` | `agents/tutorclaw/SOUL.md` | Personality and teaching philosophy |
| `IDENTITY.md` | `agents/tutorclaw/IDENTITY.md` | Voice, tone, and boundary definitions |
| `tutorclaw-shim/SKILL.md` | `skills/tutorclaw-shim/SKILL.md` | Offline fallback for Chapters 1-5 |
| `.mcp.json` | merged into OpenClaw config | MCP server connection (streamable-http) |

## Requirements

- **OpenClaw** ≥ 2.0.0
- **Python** ≥ 3.11 (for the MCP server)
- **Stripe account** (for payment tier enforcement)

## Post-install steps

```bash
# Start the TutorClaw MCP server
cd tutorclaw-mcp && python -m uvicorn main:app --port 8000

# Restart the OpenClaw gateway to load the MCP connection
openclaw gateway restart

# Verify the MCP server is connected
openclaw mcp list
```
