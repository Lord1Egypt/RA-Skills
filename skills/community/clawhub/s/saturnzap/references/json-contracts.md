# SaturnZap JSON Output Contracts

Every `sz` command writes JSON to stdout on success and stderr on error.
No `--json` flag is needed — JSON is the default output format.

## Envelope Format

### Success

```json
{ "status": "ok", ...fields }
```

### Error

```json
{ "status": "error", "code": "ERROR_CODE", "message": "Human-readable detail" }
```

Error codes: `ALREADY_INITIALIZED`, `CONNECTION_FAILED`, `INSUFFICIENT_FUNDS`,
`INVALID_PUBKEY`, `INVALID_ADDRESS`, `INVALID_INVOICE`, `INVALID_CHANNEL_ID`,
`INVALID_NETWORK`, `PAYMENT_FAILED`, `CHANNEL_CREATION_FAILED`,
`SPENDING_CAP_EXCEEDED`, `EXCEEDS_MAX_SATS`, `INVALID_PEER_ADDRESS`, `INVALID_ARGS`,
`INVALID_HEADER`, `L402_PARSE_FAILED`, `L402_NO_CHALLENGE`,
`LDK_ERROR`, `INTERNAL_ERROR`, `NO_SEED`, `UNKNOWN_REGION`, `UNKNOWN_LSP`.

---

## Node Management

### `sz init`

```json
{
  "status": "ok",
  "mnemonic": "twelve word seed phrase here ...",
  "pubkey": "0234b0c302e8c201e0ffd31580bf9106b625505b1fe3cc2550d7437afe5df59e50",
  "seed_path": "/root/.config/saturnzap/seed.enc",
  "message": "Wallet initialized. WRITE DOWN YOUR MNEMONIC AND STORE IT SAFELY."
}
```

### `sz start`

```json
{
  "status": "ok",
  "pubkey": "0234b0c302e8c201e0ffd31580bf9106b625505b1fe3cc2550d7437afe5df59e50",
  "message": "Node started."
}
```

### `sz stop`

```json
{
  "status": "ok",
  "message": "Node stopped."
}
```

With `--close-all`:

```json
{
  "status": "ok",
  "message": "Closed 2 channel(s) and stopped node.",
  "closed_channels": ["abc123...", "def456..."]
}
```

With open channels (no `--close-all`):

```json
{
  "status": "ok",
  "message": "Node stopped.",
  "warning": "2 channel(s) still open. Use --close-all to close first."
}
```

### `sz status`

```json
{
  "status": "ok",
  "pubkey": "0234b0c302e8c201e0ffd31580bf9106b625505b1fe3cc2550d7437afe5df59e50",
  "is_running": true,
  "network": "signet",
  "block_height": 204512,
  "block_hash": "00000023...",
  "latest_wallet_sync": 1711700000,
  "latest_lightning_sync": 1711700000,
  "peer_count": 2,
  "channel_count": 1,
  "usable_channel_count": 1,
  "sync_lag_seconds": 3
}
```

### `sz setup`

```json
{
  "status": "ok",
  "pubkey": "0234b0c302e8c201e0ffd31580bf9106b625505b1fe3cc2550d7437afe5df59e50",
  "steps": [
    { "step": "init", "skipped": true, "reason": "already initialized" },
    { "step": "address", "address": "tb1qxxxx...", "network": "signet" }
  ],
  "message": "Setup complete. Fund your wallet: send signet sats to tb1qxxxx..."
}
```

With `--auto` (includes inbound request):

```json
{
  "status": "ok",
  "pubkey": "0234b0c302e8c201e0ffd31580bf9106b625505b1fe3cc2550d7437afe5df59e50",
  "steps": [
    { "step": "init", "skipped": false, "mnemonic": "twelve words ...", "seed_path": "/root/..." },
    { "step": "address", "address": "tb1qxxxx...", "network": "signet" },
    { "step": "inbound", "skipped": false, "user_channel_id": "1", "lqwd_node": "LQWD-Canada", "..." : "..." }
  ],
  "message": "Setup complete."
}
```

---

## Wallet

### `sz address`

```json
{
  "status": "ok",
  "address": "tb1qxxxx...",
  "network": "signet"
}
```

### `sz send <address> --amount 50000`

```json
{
  "status": "ok",
  "txid": "a1b2c3d4...",
  "amount_sats": 50000,
  "send_all": false
}
```

### `sz send <address>` (send all)

```json
{
  "status": "ok",
  "txid": "a1b2c3d4...",
  "amount_sats": null,
  "send_all": true
}
```

### `sz balance`

```json
{
  "status": "ok",
  "onchain_sats": 50000,
  "spendable_onchain_sats": 49000,
  "lightning_sats": 99000,
  "anchor_reserve_sats": 1000,
  "channels": [
    {
      "channel_id": "abc123...",
      "counterparty_node_id": "03992d76...",
      "channel_value_sats": 100000,
      "outbound_capacity_msat": 99000000,
      "inbound_capacity_msat": 1000000,
      "is_channel_ready": true,
      "is_usable": true,
      "is_outbound": true,
      "is_announced": false,
      "confirmations": 6,
      "funding_txo": "e23d2889...:0",
      "status_reason": "ready"
    }
  ]
}
```

`status_reason` values: `"ready"`, `"awaiting_confirmation"`, `"peer_offline"`.

---

## Payments

### `sz invoice --amount-sats 1000 --memo "test"`

```json
{
  "status": "ok",
  "invoice": "lnbc1000n1pjxyz...",
  "amount_sats": 1000,
  "memo": "test",
  "expiry_secs": 3600,
  "payment_hash": "def456..."
}
```

### `sz invoice --amount-sats 0` (variable-amount)

```json
{
  "status": "ok",
  "invoice": "lnbc1pjxyz...",
  "amount_sats": null,
  "memo": "",
  "expiry_secs": 3600,
  "payment_hash": "def456..."
}
```

### `sz invoice --amount-sats 1000 --wait`

Paid:

```json
{
  "status": "ok",
  "invoice": "lnbc1000n1pjxyz...",
  "amount_sats": 1000,
  "payment_hash": "def456...",
  "expiry_secs": 3600,
  "paid": true,
  "received_sats": 1000,
  "waited_seconds": 12
}
```

Not paid (timed out):

```json
{
  "status": "ok",
  "invoice": "lnbc1000n1pjxyz...",
  "amount_sats": 1000,
  "payment_hash": "def456...",
  "expiry_secs": 3600,
  "paid": false,
  "waited_seconds": 3600,
  "message": "Invoice not paid within 3600s."
}
```

### `sz pay --invoice "lnbc..."`

```json
{
  "status": "ok",
  "payment_hash": "def456...",
  "amount_sats": 1000,
  "fee_sats": 1,
  "duration_ms": 342,
  "message": "Payment sent."
}
```

### `sz keysend --pubkey "03abc..." --amount-sats 500`

```json
{
  "status": "ok",
  "payment_hash": "abc789...",
  "amount_sats": 500,
  "duration_ms": 280,
  "message": "Keysend sent."
}
```

### `sz transactions --limit 5`

```json
{
  "status": "ok",
  "transactions": [
    {
      "payment_hash": "def456...",
      "direction": "outbound",
      "amount_sats": 1000,
      "fee_sats": 1,
      "status": "succeeded",
      "timestamp": 1711700000
    }
  ],
  "count": 1
}
```

---

## L402 (HTTP 402 Auto-Pay)

### `sz fetch "https://api.example.com/data" --max-sats 100`

Success (no 402):

```json
{
  "status": "ok",
  "url": "https://api.example.com/data",
  "http_status": 200,
  "duration_ms": 150,
  "body": { "result": "data here" }
}
```

Success (402 auto-paid):

```json
{
  "status": "ok",
  "url": "https://api.example.com/data",
  "http_status": 200,
  "payment_hash": "abc123...",
  "amount_sats": 50,
  "fee_sats": 0,
  "duration_ms": 1200,
  "body": { "result": "premium data" }
}
```

The `body` field is parsed as JSON when possible, otherwise a raw string.

---

## Peers

### `sz peers list`

```json
{
  "status": "ok",
  "peers": [
    {
      "node_id": "03992d76...",
      "address": "198.51.100.10:9735",
      "is_connected": true
    }
  ]
}
```

### `sz peers add "03abc...@1.2.3.4:9735"`

```json
{
  "status": "ok",
  "node_id": "03abc...",
  "address": "1.2.3.4:9735",
  "message": "Peer added."
}
```

### `sz peers remove "03abc..."`

```json
{
  "status": "ok",
  "node_id": "03abc...",
  "message": "Peer removed."
}
```

---

## Channels

### `sz channels list`

```json
{
  "status": "ok",
  "channels": [
    {
      "channel_id": "abc123...",
      "counterparty_node_id": "03992d76...",
      "channel_value_sats": 100000,
      "outbound_capacity_msat": 99000000,
      "inbound_capacity_msat": 1000000,
      "is_channel_ready": true,
      "is_usable": true,
      "is_outbound": true,
      "is_announced": false,
      "confirmations": 6,
      "funding_txo": "e23d2889...:0",
      "status_reason": "ready"
    }
  ]
}
```

### `sz channels open --peer "03abc...@1.2.3.4:9735" --amount-sats 100000`

```json
{
  "status": "ok",
  "user_channel_id": 1,
  "counterparty": "03abc...",
  "amount_sats": 100000,
  "message": "Channel open initiated."
}
```

### `sz channels close --channel-id "abc123" --counterparty "03abc..."`

```json
{
  "status": "ok",
  "channel_id": "abc123",
  "message": "Cooperative close initiated."
}
```

### `sz channels close --channel-id "abc123" --counterparty "03abc..." --force`

```json
{
  "status": "ok",
  "channel_id": "abc123",
  "message": "Force-close initiated."
}
```

### `sz channels wait --channel-id "abc123" --timeout 300`

Success (ready before timeout):

```json
{
  "status": "ok",
  "status": "ready",
  "channel": {
    "channel_id": "abc123...",
    "counterparty_node_id": "03992d76...",
    "is_usable": true,
    "status_reason": "ready",
    "...": "..."
  },
  "waited_seconds": 45
}
```

Timeout:

```json
{
  "status": "ok",
  "status": "timeout",
  "channel": { "channel_id": "abc123...", "is_usable": false, "status_reason": "awaiting_confirmation", "...": "..." },
  "waited_seconds": 300,
  "message": "Channel not ready after 300s."
}
```

---

## Liquidity

### `sz liquidity status`

```json
{
  "status": "ok",
  "channel_count": 1,
  "total_capacity_sats": 100000,
  "total_outbound_msat": 99000000,
  "total_inbound_msat": 1000000,
  "average_health_score": 2,
  "channels": [
    {
      "channel_id": "abc123...",
      "counterparty_node_id": "03992d76...",
      "channel_value_sats": 100000,
      "outbound_capacity_msat": 99000000,
      "inbound_capacity_msat": 1000000,
      "health_score": 2,
      "health_label": "critical"
    }
  ],
  "recommendations": [
    "Channel abc123... has low inbound capacity (critical). Request inbound liquidity."
  ],
  "stale_channels": [
    {
      "channel_id": "def456...",
      "counterparty_node_id": "03bbb...",
      "recommendation": "Peer offline — channel unusable. Consider force-closing if persistent."
    }
  ]
}
```

`stale_channels` lists channels where the peer is connected but the channel is not usable (typically peer offline).

### `sz liquidity request-inbound --amount-sats 100000`

```json
{
  "status": "ok",
  "region": "CA",
  "node_id": "03abc...",
  "amount_sats": 100000,
  "message": "Inbound liquidity request initiated."
}
```

---

## Service Management

### `sz service install`

```json
{
  "status": "ok",
  "unit_path": "/etc/systemd/system/saturnzap.service",
  "unit_name": "saturnzap.service",
  "message": "Service installed and started. Check: systemctl status saturnzap.service"
}
```

### `sz service status`

```json
{
  "status": "ok",
  "unit_name": "saturnzap.service",
  "is_active": true,
  "is_enabled": true,
  "installed": true
}
```

### `sz service uninstall`

```json
{
  "status": "ok",
  "unit_name": "saturnzap.service",
  "message": "Service removed."
}
```
