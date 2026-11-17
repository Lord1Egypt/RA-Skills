---
name: scam-wallet-screener
description: Screens Ethereum and other EVM wallet addresses (Base, Polygon, BSC, Arbitrum, etc.) against the ScamSniffer community-maintained blocklist of known phishing, wallet drainer, and scam addresses, with no API key required. Use this when the user asks to check if a crypto address is a scam, verify a wallet before sending funds or signing a transaction, screen for wallet drainer addresses, check if an address is blacklisted or flagged for phishing, do a quick on-chain safety check before an airdrop claim or NFT mint, or wants a fast keyless scam address lookup tool. Pulls a public, actively updated JSON feed (~2,500+ known bad addresses) and caches it locally for 6 hours. Complements, but does not replace, deeper on-chain forensics or paid threat-intel services — a clean result means the address is not on this particular list, not that it is verified safe.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Scam / Drainer Wallet Screener

Checks one or more EVM addresses against the ScamSniffer community
blocklist — a public, actively maintained list of addresses tied to
phishing sites, wallet drainers, and fraudulent contracts. No API key
required; the data is a public GitHub JSON feed.

## When to use this

- Before sending funds to an address the user isn't fully sure about.
- Before approving/signing a transaction from an unfamiliar contract.
- Quick pre-check before claiming an airdrop or minting an NFT from a link
  that was shared in DMs, Discord, or a suspicious-looking site.
- Batch-screening a list of addresses (e.g. from a CSV of transaction
  counterparties).

## How to run it

```bash
python3 scripts/screen_address.py 0xAddressHere
python3 scripts/screen_address.py 0xAddr1 0xAddr2 0xAddr3
python3 scripts/screen_address.py --json 0xAddressHere
python3 scripts/screen_address.py --refresh 0xAddressHere   # bypass the 6h cache
```

Output for each address is either `FLAGGED` (found in the blocklist) or
`not found in blocklist`.

## Important limitations (be upfront with the user about these)

- **Absence ≠ safety.** This only checks one community list. A "not found"
  result means the address hasn't been reported to this specific feed —
  it does not mean the address is trustworthy. New scam addresses appear
  constantly and this list won't have same-day coverage of everything.
- **EVM addresses only.** The blocklist covers Ethereum-style `0x...`
  addresses; it does not cover Solana, Bitcoin, or other non-EVM chains.
- **Community-sourced, not authoritative.** Entries come from crowd
  reports and automated detection, not a regulator or exchange. Treat a
  flag as a strong warning sign, not a legal determination.
- Data is cached locally for 6 hours (`~/.cache/scam-wallet-screener/`) to
  avoid hammering the source on every call — use `--refresh` if you need
  the absolute latest list.
- For anything involving real money movement, this should be one signal
  among several (contract verification, transaction simulation, reading
  the actual contract code) — not a sole gate.

See `README.md` for a plain-language overview of the data source.
