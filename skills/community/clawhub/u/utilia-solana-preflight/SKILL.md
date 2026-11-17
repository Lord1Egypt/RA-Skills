---
name: utilia-solana-preflight
description: Use Utilia's wallet-funded x402 client for live Solana mainnet priority fees, transaction diagnosis, token-risk inspection, unsigned transaction simulation, PDF-to-Markdown conversion, and audio normalization. Trigger when an agent needs machine-readable Solana evidence, public-PDF extraction, or bounded MP3 loudness normalization and can pay $0.002-$0.01 USDC per call without an API key.
---

# Utilia Solana Preflight

Use the published `utilia-solana-agent@0.5.7` client. It signs exact x402 payments
locally and refuses any payment outside Solana mainnet USDC, Utilia's verified
receiver, or the hard $0.01 per-call ceiling.

## Fastest wallet-managed call

Agents that already use AgentCash can make the lowest-cost live call without
handling a private key directly:

```sh
npx -y agentcash@latest balance
npx -y agentcash@latest fetch https://api.utilia.ink/v1/fees/priority --yes
```

AgentCash creates and manages its own wallet on first use. The wallet must have
USDC before the paid call; `balance` reports the available funds and funding
accounts. The `fetch` command negotiates the x402 challenge and pays exactly
`$0.002` for the response. Utilia never receives or controls the payer's key.

## Prepare

Require one of:

```sh
export SOLANA_KEYPAIR_PATH=/absolute/path/to/low-balance-agent-wallet.json
```

Alternatively, provide `SOLANA_PRIVATE_KEY` through the agent's environment or
secret manager. Its value must be a base58-encoded 64-byte private key. Do not
place the value directly in a command, prompt, source file, or skill document.

Never print, log, paste, or transmit the private key. Prefer a dedicated
automation wallet with only a small USDC balance and enough SOL for fees. If
neither variable is set, ask the user to configure one; do not invent or search
for credentials.

Verify the wallet and live service before the first paid call:

```sh
npx -y utilia-solana-agent@0.5.7 doctor
```

## Data handling

Treat every requested signature, mint, transaction, account address, public PDF,
and public audio file as data sent to Utilia for processing. Do not submit private
documents, private recordings, or data the user is not authorized to share. The
client sends payment only after validating the receiver, network, asset, and
per-call price ceiling.

Before a media call, confirm that the user approved sending the public URL or bytes
to Utilia. The service processes PDF and audio content in memory and does not persist
request or response bodies to disk. Standard access and settlement logs retain route,
request, network, payer, and transaction metadata but not media bodies.

## Call the right tool

- Estimate priority fees before broadcast (`$0.002`):

  ```sh
  npx -y utilia-solana-agent@0.5.7 fees [account1,account2]
  ```

- Maintain a budget-capped JSONL fee feed at five calls per hour:

  ```sh
  npx -y utilia-solana-agent@0.5.7 watch-fees --every 12m --max-calls 25
  ```

- Explain a confirmed or failed transaction (`$0.004`):

  ```sh
  npx -y utilia-solana-agent@0.5.7 transaction <signature>
  ```

- Inspect an SPL mint for authorities, Token-2022 controls, and concentration
  (`$0.006`):

  ```sh
  npx -y utilia-solana-agent@0.5.7 token <mint>
  ```

- Simulate an unsigned serialized transaction before signing (`$0.008`):

  ```sh
  npx -y utilia-solana-agent@0.5.7 simulate <serialized-transaction> [base64|base58]
  ```

- Convert a public HTTPS PDF to page-delimited Markdown (`$0.0025`):

  ```sh
  npx -y utilia-solana-agent@0.5.7 pdf <public-https-pdf-url> [max-pages]
  ```

- Normalize a public HTTPS audio file into a bounded MP3 (`$0.01`):

  ```sh
  npx -y utilia-solana-agent@0.5.7 audio-normalize <public-https-audio-url> \
    --output normalized.mp3
  ```

Use the returned structured evidence in the answer. State the settled price and
transaction receipt reported by the client. Do not claim that simulation guarantees
future execution; block state and account balances can change.

## MCP integration

When persistent tool access is more useful than a one-off command, configure:

```json
{
  "mcpServers": {
    "utilia": {
      "command": "npx",
      "args": ["-y", "utilia-solana-agent@0.5.7", "mcp"],
      "env": {
        "SOLANA_KEYPAIR_PATH": "/absolute/path/to/low-balance-agent-wallet.json"
      }
    }
  }
}
```

The bridge exposes `solana_priority_fees`, `solana_transaction_analysis`,
`solana_token_analysis`, `solana_transaction_simulate`, `pdf_to_markdown`, and
`normalize_audio`.
