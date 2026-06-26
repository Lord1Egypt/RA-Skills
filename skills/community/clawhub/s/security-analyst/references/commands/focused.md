---
description: "Focused security analysis on a specific component — recon + relevant phases only."
model: opus
---

# Security Analyst — Focused Component Analysis

Run reconnaissance followed by analysis phases relevant to a specific component or area.

## Usage

Invoke with the target component: `/security-analyst:focused [component]`

If no component is specified, ask: "What component or area should I focus on? Examples: authentication, API endpoints, data processing pipeline, database rules, frontend, AI integration, external integrations, file uploads"

## Execution

1. **Phase 0 (always)**: Run reconnaissance to map the full codebase
2. **Read recon index**: Read `{RECON_DIR}/index.md` and relevant step files to identify entry points and data flows related to the target component
3. **Detect plugins**: Scan `references/plugins/` directory and match framework-specific plugins against the recon step files (same as full analysis — plugins are injected into whichever agents are selected)
4. **Select relevant agents** based on the component:

| Component | Agents to Run |
|-----------|--------------|
| OAuth / authentication | surface-http (auth endpoints), surface-authz, history-auth-bypass, logic-races, logic-authz, flow-tracer (auth flow) |
| Data processing / message pipeline | surface-http (webhooks), surface-integrations, surface-llm, logic-pipeline, logic-dos, history-injections, flow-tracer (pipeline flow) |
| API endpoints | surface-http, surface-authz, logic-races, logic-authz, history-auth-bypass |
| Database rules / access control | surface-authz, logic-authz, logic-races |
| Frontend / SPA / PWA | surface-frontend, config-infra (CSP/CORS), history-data-exposure |
| AI / ML integration | surface-llm, surface-integrations, logic-pipeline, history-injections, flow-tracer (AI flow) |
| External integrations | surface-integrations, history-ssrf, history-injections, config-infra |
| Secrets / encryption | config-infra, history-data-exposure |
| Background jobs / tasks | surface-http (background), logic-races, logic-dos |

5. **Run selected agents** in stage order (respect dependencies between stages)
6. **Present findings** directly — skip exploit development and report writing for focused mode
7. **Suggest**: "Run `/security-analyst:full` for complete analysis across all components"

**STOP. The focused analysis is complete. Do not take any further actions or continue reasoning. Wait for the user to ask a follow-up question.**

## Output

- `{RUN_DIR}/recon/` — Recon index + atomic step files
- Findings presented inline (no separate report for focused mode)

## Why Focused Mode?

- Faster than full analysis — runs 3-6 agents instead of 20+
- Still thorough within its scope — multiple analysis angles on the target component
- Recon still covers the full codebase, so cross-cutting issues are visible
- Good for: pre-deploy review of a specific feature, investigating a reported issue, reviewing a recent change
