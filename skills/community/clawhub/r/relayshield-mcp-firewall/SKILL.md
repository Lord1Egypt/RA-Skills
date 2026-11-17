---
name: relayshield-mcp-firewall
description: Route OpenClaw MCP traffic through the RelayShield Proxy Firewall, screening every tool call and tool result against threat intelligence before it reaches your agent.
auto-activate: false
triggers: [mcp firewall, relayshield, tool screening, mcporter proxy, poisoned tools]
metadata: {"openclaw":{"requires":{"env":["RELAYSHIELD_PROXY_PORT"],"anyBins":["mcporter","python3"]},"primaryEnv":"RELAYSHIELD_PROXY_PORT"}}
---

# RelayShield MCP Proxy Firewall

Screens every MCP tool call and tool result against RelayShield's threat-intelligence corpus (700K+ indicators) before it reaches your agent. Catches poisoned tool definitions, prompt-injected responses, credential exfiltration, and known phishing-kit fingerprints at runtime.

## How it fits

```
OpenClaw -> mcporter -> [RelayShield Proxy :8090] -> Upstream MCP Server
                              |
                    TI screening per tools/call
```

Your agent connects to mcporter as before. mcporter connects to the RelayShield proxy instead of the upstream server directly. The proxy forwards clean calls upstream and blocks or quarantines suspicious ones, returning standard MCP error responses.

## Prerequisites

- Python 3.10+
- mcporter installed: `npm install -g mcporter`
- The RelayShield repo cloned (the proxy ships in it): `git clone https://github.com/nzdsf2-gif/relayshield.git`

## Step 0: Pre-scan (recommended)

Before routing traffic, audit the upstream server's tool definitions offline with the pre-deployment scanner:

```bash
cd relayshield
python3 -m mcp_proxy.tool_scanner --url https://your-mcp-server.example.com/mcp
```

This flags prompt injection, instruction hijacking, exfiltration patterns, credential parameters, and dangerous capabilities in tool definitions. Fix what it finds, then deploy the proxy for runtime protection.

## Step 1: Start the proxy

```bash
cd relayshield
export MCP_PROXY_UPSTREAM="https://your-mcp-server.example.com/mcp"
export MCP_PROXY_PORT="8090"
python3 -m mcp_proxy
```

The proxy listens on port 8090 and forwards screened requests to your upstream server. Point your MCP client at `http://localhost:8090`.

Useful environment variables:

| Variable | Default | Description |
|---|---|---|
| `MCP_PROXY_UPSTREAM` | (required) | Upstream MCP server URL |
| `MCP_PROXY_PORT` | 8090 | Local listen port |
| `MCP_PROXY_SCREENING` | true | Master switch for TI screening |
| `MCP_PROXY_BLOCK_LEVELS` | high,medium | Verdict levels that block |
| `MCP_PROXY_RESULT_SCREENING` | true | Screen tool results, not just calls |
| `MCP_PROXY_BEHAVIOR` | true | Behavioral anomaly detection |
| `RELAYSHIELD_API_KEY` | (optional) | Enables deeper cached checks |

Run one proxy instance per upstream server, each on its own port.

## Step 2: Point mcporter at the proxy

Register the proxy as the server in mcporter instead of the upstream URL. The upstream auth header moves to the proxy's environment only if the upstream needs it; mcporter itself talks to the local proxy with no auth.

```bash
mcporter config add myserver http://127.0.0.1:8090 --scope home
```

If the upstream server needs an Authorization header, the proxy forwards a static header you configure. Set it via the proxy's environment or policy file rather than in mcporter, so the credential never passes through the agent's config.

Verify the tools enumerate through the proxy:

```bash
mcporter list myserver
```

If this prints tool metadata, the chain is live: OpenClaw -> mcporter -> RelayShield proxy -> upstream.

## Step 3: Verify screening

Run a quick check that the proxy is actually screening. The interactive demo runs 14 attack scenarios through the full stack without any network:

```bash
python3 -m mcp_proxy.dashboard --demo
# then open http://127.0.0.1:8091/_rs/dashboard
```

Scenario 2 (poisoned neighbor) and scenario 5 (phishing-kit fingerprint) show BLOCKED verdicts with confidence scores and cause codes explaining which signals fired.

## What gets screened

- **Tool calls:** URLs, domains, and IPs extracted from arguments are checked against the TI corpus. Known-malicious indicators block the call with MCP error -32001.
- **Tool results:** Response content is scanned for prompt injection, secret material, phishing-kit fingerprints, unredacted PII, and credential exfiltration toward non-identity-provider infrastructure.
- **Behavior:** Per-agent baselines flag unusual call sequences, volume spikes, and cross-tool attack chains.
- **Policy:** Optional YAML policy file for declarative allow/deny rules per agent, tool, and server. Every decision is audit-logged.

## Notes

- The proxy never describes a result as safe. Best case is no flags found.
- If TI screening times out, calls fail open (allowed) and the timeout is logged.
- Stdio MCP servers cannot be proxied over HTTP. For stdio servers, run the pre-deployment scanner and rely on OpenClaw's approval hooks.
- More info: https://api.relayshield.net/developers
