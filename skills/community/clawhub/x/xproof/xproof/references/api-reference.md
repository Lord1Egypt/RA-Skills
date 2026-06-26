# xProof API Reference (Quick Index)

Complete OpenAPI 3.1 spec is available at: `GET https://xproof.app/api/acp/openapi.json`

## Onboarding (No Account)

| Method | Path | Auth | Purpose |
|:---|:---|:---|:---|
| `POST` | `/api/agent/register` | None | Get a `pm_` key + 10 free proofs |
| `GET`  | `/api/agent/status` | Bearer | Credits remaining, last proof, agent metadata |

## Certification

| Method | Path | Auth | Purpose |
|:---|:---|:---|:---|
| `POST` | `/api/proof` | Bearer or x402 | Anchor a single file hash on MultiversX |
| `POST` | `/api/batch` | Bearer or x402 | Anchor up to 50 files in one call |
| `POST` | `/api/audit` | Bearer | Anchor an agent decision (audit log standard) |

## Verification (Public)

| Method | Path | Purpose |
|:---|:---|:---|
| `GET` | `/api/proof/:id` | JSON document for a proof UUID |
| `GET` | `/api/proof/hash/:hash` | JSON document for a file hash |
| `GET` | `/proof/:id` | Human-readable proof page (HTML) |
| `GET` | `/proof/:id.json` | Same data as `/api/proof/:id` |
| `GET` | `/api/certificates/:id.pdf` | Downloadable PDF certificate with QR |
| `GET` | `/badge/:id` | SVG status badge (shields.io style) |
| `GET` | `/audit/:id` | Human-readable audit log page |

## Trust & Standards

| Method | Path | Purpose |
|:---|:---|:---|
| `GET` | `/api/standard` | Agent Proof Standard specification |
| `POST` | `/api/standard/validate` | Validate a proof document against the standard |
| `GET` | `/api/artifact/trust/:hash` | Aggregate trust score for an artifact |
| `GET` | `/api/v1/skills/xproof/file?path=...` | Read a published Clawhub skill file |

## MCP

| Method | Path | Purpose |
|:---|:---|:---|
| `POST` | `/mcp` | JSON-RPC 2.0 endpoint (requires `Accept: application/json, text/event-stream`) |
| `GET`  | `/mcp` | MCP capability discovery |

## Discovery

| Method | Path | Purpose |
|:---|:---|:---|
| `GET` | `/api/acp/openapi.json` | OpenAPI 3.1 spec (full REST surface) |
| `GET` | `/api/acp/health` | Health check |
| `GET` | `/.well-known/agent.json` | Agent Protocol manifest |
| `GET` | `/.well-known/mcp.json` | MCP server manifest |
| `GET` | `/.well-known/agent-audit-schema.json` | Audit log canonical schema |
| `GET` | `/ai-plugin.json` | OpenAI ChatGPT plugin manifest |
| `GET` | `/llms.txt` | LLM-friendly summary |
| `GET` | `/llms-full.txt` | Complete LLM reference |
