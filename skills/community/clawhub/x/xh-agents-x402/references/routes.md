# XH Agents paid routes (generated from live 402 challenges)

Source: `https://xhagents.xyz/openapi.json` + each route's own 402 challenge. Regenerate with `gen_skill_references.py`; do not hand-edit prices.

42 paid routes.

| price | method | path | summary |
|---|---|---|---|
| $0.03 | POST | `/api/daily-drop` | XH Agents Daily Drop - dated demand brief |
| $0.03 | POST | `/api/kb/ask` | Ask the XH Agents knowledge base |
| $0.05 | POST | `/api/company-enrich` | People & company enrichment |
| $0.05 | GET | `/api/document-extract` | Document to text - GET form |
| $0.05 | POST | `/api/document-extract` | Document to text (PDF, scans, images, DOCX, HTML) |
| $0.05 | GET | `/api/domain-audit` | Domain & email audit - GET form |
| $0.05 | POST | `/api/domain-audit` | Domain & email audit - SPF, DMARC, DKIM, MX, TLS, headers |
| $0.05 | POST | `/api/social-data` | Social media data (X/Twitter + LinkedIn) |
| $0.05 | GET | `/api/token-safety` | Token safety score (Base) - GET form |
| $0.05 | POST | `/api/token-safety` | Token safety score (Base) - safe / caution / danger |
| $0.05 | GET | `/api/trust-leaderboard` | x402 seller trust leaderboard - GET form |
| $0.05 | POST | `/api/trust-leaderboard` | x402 seller trust leaderboard - ranked origins |
| $0.05 | GET | `/api/x402-trust` | x402 trust layer - GET form |
| $0.05 | POST | `/api/x402-trust` | x402 trust layer - score an endpoint before you pay it |
| $0.10 | POST | `/api/arkham-intel/counterparties` | Arkham-style intel - counterparty due diligence |
| $0.10 | POST | `/api/arkham-intel/exchange-flow` | Arkham-style intel - pool inflow/outflow |
| $0.10 | POST | `/api/arkham-intel/portfolio` | Arkham-style intel - wallet portfolio snapshot |
| $0.10 | POST | `/api/arkham-intel/trace` | Arkham-style intel - fund trace for investigations |
| $0.10 | POST | `/api/arkham-intel/use-cases` | Arkham-style intel - use-case router |
| $0.10 | POST | `/api/arkham-intel/venue-users` | Arkham-style intel - venue users, VIPs and flagged funders |
| $0.10 | POST | `/api/chat` | Ask the XH Agents AI Trading Assistant |
| $0.10 | POST | `/api/defi-sentiment` | Asset and protocol sentiment from public data |
| $0.10 | POST | `/api/gas-tracker` | Base gas right now |
| $0.10 | GET | `/api/howto/vps-gdrive-connect` | GET - Connect a headless VPS to a user's Google Drive (rclone, no browser on the server) |
| $0.10 | POST | `/api/howto/vps-gdrive-connect` | POST - Connect a headless VPS to a user's Google Drive (rclone, no browser on the server) |
| $0.10 | GET | `/api/howto/youtube-auto-ai` | GET - YouTube Shorts automation with AI: queue -> render -> upload -> notify |
| $0.10 | POST | `/api/howto/youtube-auto-ai` | POST - YouTube Shorts automation with AI: queue -> render -> upload -> notify |
| $0.10 | POST | `/api/payment-verify` | Verify a USDC settlement |
| $0.10 | POST | `/api/token-check` | Check an ERC-20 token on Base |
| $0.10 | POST | `/api/video-license` | XH Animations video licence - one film master |
| $0.10 | POST | `/api/wallet-profile` | Profile an address on Base |
| $0.10 | POST | `/api/whale-watch` | Large recent transfers on Base |
| $0.10 | POST | `/api/x402-check` | Conformance report for any x402 endpoint |
| $0.10 | POST | `/api/x402-directory` | Search the x402 ecosystem |
| $0.15 | GET | `/api/hundred-x-hunter` | XH cycle-wallet hunt - GET form |
| $0.15 | POST | `/api/hundred-x-hunter` | XH cycle-wallet hunt (seven-step 'next 100x' method) |
| $0.25 | POST | `/api/web-search` | Web search + page content retrieval |
| $0.30 | GET | `/api/howto/create-x402-endpoint` | GET - Build an x402 paid endpoint that passes the validator, gets indexed and takes real U |
| $0.30 | POST | `/api/howto/create-x402-endpoint` | POST - Build an x402 paid endpoint that passes the validator, gets indexed and takes real  |
| $0.30 | GET | `/api/howto/x402-register` | GET - Register an x402 endpoint so agents can find and pay it (x402scan + Coinbase Bazaar) |
| $0.30 | POST | `/api/howto/x402-register` | POST - Register an x402 endpoint so agents can find and pay it (x402scan + Coinbase Bazaar |
| $0.91 | POST | `/api/compute/xh-bundle` | XH Agents playbook bundle (13 production playbooks) |

Free, no key: `python3 scripts/xh_pay.py quote <url>` prints the live price, the
network, the asset and the `payTo` address before anything is signed.
