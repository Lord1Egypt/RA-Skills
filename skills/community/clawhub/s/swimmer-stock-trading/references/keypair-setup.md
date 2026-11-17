# Dedicated wallet and policy setup

Perform setup in a trusted local terminal and editor outside the agent conversation. Anyone who obtains the config can spend the dedicated wallet’s funds.

## Install dependencies

```bash
python3 -m venv "$HOME/.local/share/swimmer-stock-trading/venv"
"$HOME/.local/share/swimmer-stock-trading/venv/bin/pip" install \
  -r "<SKILL_DIR>/scripts/requirements.txt"
```

## Create the fixed protected config

```bash
install -d -m 700 "$HOME/.config/swimmer-stock-trading"
install -m 600 "<SKILL_DIR>/config.example.json" \
  "$HOME/.config/swimmer-stock-trading/config.json"
```

In a trusted editor, configure:

- `private_key`: a new dedicated base58-encoded 64-byte Solana keypair, never a seed phrase or primary wallet.
- `rpc_url`: leave exactly `https://api.mainnet-beta.solana.com`.
- `accepted_custodial_recipient`: after following [custody-and-settlement.md](custody-and-settlement.md), enter the full independently verified fixed recipient.
- `trusted_stock_mints`: uppercase tickers mapped to mints independently verified from an official source. API discovery alone is insufficient.
- `max_offer_raw_by_mint`: each token mint the wallet may send mapped to a conservative maximum raw amount per transaction. Add canonical USDC for BUY and each trusted stock mint for SELL.

Example structure with deliberately invalid placeholders:

```json
{
  "private_key": "REPLACE_LOCALLY",
  "rpc_url": "https://api.mainnet-beta.solana.com",
  "accepted_custodial_recipient": "REPLACE_AFTER_INDEPENDENT_VERIFICATION",
  "trusted_stock_mints": {"AAPL": "REPLACE_WITH_VERIFIED_MINT"},
  "max_offer_raw_by_mint": {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "25000000"
  }
}
```

The CLI deliberately has no `--config` option. It atomically opens only the fixed path, refuses symlinks, requires the current owner, exact directory mode `0700`, and exact file mode `0600`.

Verify only the public address:

```bash
"$HOME/.local/share/swimmer-stock-trading/venv/bin/python" \
  "<SKILL_DIR>/scripts/solana_sign_send.py" address
```

Deposit only the intended USDC trading balance and a small SOL fee balance. If the host or config may be compromised, stop and move funds from a separate trusted device.
