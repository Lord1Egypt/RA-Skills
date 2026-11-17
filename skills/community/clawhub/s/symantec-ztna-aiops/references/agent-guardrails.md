# Agent guardrails

| Enforced in code | Location |
|---|---|
| MCP and CLI use the same governed read functions. | `symantec_ztna_aiops/mcp_server/tools/ztna.py`, `symantec_ztna_aiops/cli/__init__.py` |
| API client credentials stay in environment variables; TLS verification defaults on. | `symantec_ztna_aiops/connection.py:_settings` |
| Expired tokens refresh once; rejected login backs off. | `symantec_ztna_aiops/connection.py:ZtnaConnection` |
| POST is restricted to documented query-only audit search. | `symantec_ztna_aiops/connection.py:ZtnaConnection._request` |
| Page metadata is validated and incomplete health probes remain visible. | `symantec_ztna_aiops/ops.py:_paged`, `health_sample` |

No live tenant has been verified. A resolved application and site status reflect configuration and reported health, not proof of end-user connectivity. Do not infer full fleet health from `health-sample`.
