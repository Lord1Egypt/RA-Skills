# Scam / Drainer Wallet Screener

A keyless Python tool that checks EVM crypto addresses against the
[ScamSniffer](https://github.com/scamsniffer/scam-database) community
blocklist — a public, actively updated feed of addresses tied to
phishing sites, wallet drainers, and fraudulent contracts.

## Why this exists

There was no simple, no-API-key skill on ClawHub that answers "has this
specific wallet address been reported as a scam/drainer?" before sending
funds or signing a transaction. This fills that gap using a real,
community-maintained dataset (2,500+ addresses at time of writing).

## Quick start

```bash
cd scripts
python3 screen_address.py 0xYourAddressHere
```

```
Checked against 2530 known scam/drainer addresses.

  0x101ce0cedd142f199c9ef61739ae59b6611a0fc0  ->  FLAGGED — known scam/drainer address
  0x0000000000000000000000000000000000dead  ->  not found in blocklist
```

## How it works

1. Downloads (and caches for 6 hours) the ScamSniffer blocklist JSON from
   GitHub.
2. Normalizes and lowercases both the blocklist and the input address(es).
3. Reports a flag if there's a match, otherwise reports "not found."

## Limitations

- Covers EVM addresses only (Ethereum, Base, Polygon, BSC, Arbitrum, etc.),
  not Solana/Bitcoin/other non-EVM chains.
- A clean result is not a safety guarantee — it just means this specific
  list hasn't seen a report for that address yet.
- Community-sourced data, not a regulatory or exchange-grade determination.

Use this as one fast pre-check, not a substitute for reading contract
code or using a transaction simulator before approving anything of value.
