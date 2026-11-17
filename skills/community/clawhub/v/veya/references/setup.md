# Setup

## 1. Connect the MCP server

Endpoint: **`https://mcp.veyanet.tech/mcp`** (MCP Streamable HTTP). No install, no clone.

### Cursor

Add to `.cursor/mcp.json` in the project, or `~/.cursor/mcp.json` for all projects
(or Settings → MCP → Add custom MCP server):

```json
{
  "mcpServers": {
    "veya": { "url": "https://mcp.veyanet.tech/mcp" }
  }
}
```

### Claude Code

```bash
claude mcp add veya --transport http https://mcp.veyanet.tech/mcp
```

### Claude Desktop / claude.ai

Settings → Connectors → Add custom connector → URL `https://mcp.veyanet.tech/mcp`.

### Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.veya]
url = "https://mcp.veyanet.tech/mcp"
```

### Any MCP client

Use Streamable HTTP transport with the URL above. Requests must accept
`application/json, text/event-stream`. Ready configs: [../assets/mcp.json](../assets/mcp.json)
and [../assets/mcp.self-hosted.json](../assets/mcp.self-hosted.json).

## 2. Confirm it works

Ask the agent: *"Call veya_describe and veya_ping_chain and summarize the network."*
The answer should name Robinhood Chain Mainnet (or Testnet when selected), and
the `Veya.sol` contract. Details: [service-and-chain.md](service-and-chain.md).

From a terminal:

```bash
curl -s https://mcp.veyanet.tech/health
```

## 3. Product API key (scoped and write tools)

1. Open https://app.veyanet.tech and connect your wallet.
2. Open **System → API Keys** and create a Dev or Live key. It starts with `veya_dev_` or `veya_live_` and is shown once.
3. Give it to the agent when a tool needs `apiKey`. Check it with `veya_account`.
4. Keys travel as tool arguments (`apiKey`, and `payerPrivateKey` for writes). Do not put them in `mcp.json`; the hosted config has no key.

The key owns your environments, agents, memory and tool rules. See
[auth-and-limits.md](auth-and-limits.md).

## 4. Fund the wallet (on-chain writes)

Writes are sent from the wallet bound to your API key and need ETH for gas on the selected network.

| Network | RPC | Explorer |
|---|---|---|
| Mainnet (default) | `https://rpc.mainnet.chain.robinhood.com` | https://robinhoodchain.blockscout.com |
| Testnet (optional) | `https://rpc.testnet.chain.robinhood.com` | https://explorer.testnet.chain.robinhood.com |

Testnet faucet: https://faucet.testnet.chain.robinhood.com/

## 5. Self-hosting (optional)

```bash
npx -y @veyanet/mcp          # Streamable HTTP on PORT (default <mcp-port>)
# local URL: <your-mcp-host>/mcp
```

| Variable | Purpose | Default |
|---|---|---|
| `ROBINHOOD_NETWORK` | `testnet` selects Testnet | Mainnet |
| `VEYA_MAINNET_CONTRACT_ADDRESS` | Mainnet contract | `0x87dC582eEA544A434a5C1e30Ca3d12c1e548a674` |
| `ROBINHOOD_MAINNET_RPC_URL` | Mainnet RPC | `https://rpc.mainnet.chain.robinhood.com` |
| `VEYA_API_URL` | Product API | `https://api.veyanet.tech` |
| `VEYA_PAYER_PRIVATE_KEY` | Wallet for product write tools on this host | unset |
| `MCP_API_KEY` | Require `Authorization: Bearer <key>` on `/mcp` | unset |
| `VEYA_CAPACITY_PER_MINUTE` | Per-key limit for consensus/sealed/seal-decision | `30` |
| `VEYA_SEAL_DECISION_RELAYER` | `1` lets the host relayer pay for `veya_seal_decision` | off |
| `VEYA_SEAL_DECISION_ENVIRONMENT_ID` | Environment for `veya_seal_decision` receipts, registered on the active network (needed on mainnet unless each call passes `environmentId`) | unset |
| `VEYA_SEAL_DECISION_DAILY_CAP` | Relayer seals per key per UTC day | `20` |
| `VEYA_SEAL_DECISION_GLOBAL_DAILY_CAP` | Relayer seals per host per UTC day | `100` |
| `CORS_ORIGIN` | Browser Origin allowlist | empty |

Full operator docs: https://github.com/veyanet/veya-mcp/tree/main/docs
