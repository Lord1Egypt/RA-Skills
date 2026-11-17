# Agent guardrails

- MCP and CLI use the same governed functions and audit harness.
- API credentials stay in environment variables; TLS verification is on by default.
- Authentication retries once on HTTP 401 and backs off after rejected login.
- Only documented read routes are exposed; POST is restricted to query-only search where applicable.
- Treat missing, partial and unverified responses as unknown, not healthy or zero.
- No live Symantec Endpoint Detection and Response (on-premises) environment has yet been verified.
