# Solana mainnet balances

The packaged command reads the fixed protected config and returns only public addresses and public on-chain balances. It uses `https://api.mainnet-beta.solana.com`; no RPC API key is required.

Check SOL and canonical Solana USDC:

```bash
"$HOME/.local/share/swimmer-stock-trading/venv/bin/python" \
  "<SKILL_DIR>/scripts/solana_sign_send.py" balance
```

Check those balances plus one allowlisted stock ticker:

```bash
"$HOME/.local/share/swimmer-stock-trading/venv/bin/python" \
  "<SKILL_DIR>/scripts/solana_sign_send.py" balance --stock AAPL
```

The signer resolves the stock mint from protected `trusted_stock_mints`; it does not accept an arbitrary mint on the command line. A missing associated token account is reported as zero. Before BUY, require sufficient USDC and SOL. Before SELL, require sufficient trusted stock tokens and SOL. Balance reads do not reserve funds, so simulation remains mandatory.
