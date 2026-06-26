# User Journey, Fallback, and Lead Capture

## User Entry Point

ClawHub is the discovery and installation surface. The user does not ask questions on the ClawHub listing page itself.

Expected path:

1. The user finds `Solution Case Finder` on ClawHub.
2. The user installs the skill into an OpenClaw or ClawHub-compatible Agent environment.
3. The environment has MCP server `triz-solution-search` configured.
4. The user directly calls the skill and enters their own technical problem in the Agent chat.
5. This skill triggers and calls `solution_search`.
6. The answer summarizes relevant reference cases, core case fields, transferable patterns, and next experiments.

Internal demo and test examples. These are not required user wording:

- How can others reduce fan noise without sacrificing airflow?
- How have others improved semiconductor package heat dissipation while controlling warpage?
- How can a fixture achieve high positioning accuracy and fast changeover at the same time?

## No-MCP Fallback

If MCP is not configured, unreachable, or returns an authentication or protocol error:

1. Do not invent cases.
2. Explain that case retrieval requires `triz-solution-search`.
3. Still provide a lightweight TRIZ framing:
   - likely contradiction
   - candidate inventive principles
   - recommended refined query
4. Ask the user to configure the MCP endpoint or provide access.

Fallback response pattern:

```text
I can frame the problem for TRIZ-style retrieval, but I am not connected to the triz-solution-search MCP server, so I cannot return real cases yet.

Suggested retrieval question:
...

Required MCP configuration:
/mcp add triz-solution-search https://ai-fabric.patsnap.com/mcp/triz-solution-search?APP_ID=Patsnap
```

## Lead Capture CTA

Do not add a sales pitch to every answer.

Use a CTA only when:

- the user asks for complete case lists, exports, or batch analysis
- the user asks for enterprise deployment, API access, private data, or team access
- the answer has already delivered useful value from retrieved cases

CTA style:

```text
If you need to export the full result set, filter cases by industry or inventive principle, or integrate this workflow into an enterprise R&D process, you can request full access.
```

If `SOLUTION_CASE_FINDER_LEAD_URL` is configured, include it. If not configured, say "Contact the platform administrator to request full access" rather than inventing a URL.

## Pre-Publish Review Gates

Before publishing to ClawHub, confirm:

- The `triz-solution-search` endpoint is approved for public ClawHub users.
- `APP_ID=Patsnap` can be used publicly, or replace it with a production app id or authentication method.
- The MCP response does not leak raw patent full text or confidential customer data.
- The listing clearly says the skill provides R&D inspiration, not legal opinions.
- The demo answer shows relevance score handling plus the six important case fields, and does not show internal rank or source identifiers by default.
- The ClawHub publish step is run only after owner review.
