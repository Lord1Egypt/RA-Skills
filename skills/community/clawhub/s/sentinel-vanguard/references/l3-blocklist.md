# L3 Supply Chain Blocklist — Sentinel Vanguard

Extended catalogue of known malicious, compromised, and high-risk packages.
Last updated: 2025. Cross-reference with OSV (https://osv.dev) for live advisories.

## npm — Confirmed Malicious

| Package | Incident | Year | Action |
|---|---|---|---|
| `event-stream` | Injected Bitcoin wallet stealer via `flatmap-stream` | 2018 | BLOCK |
| `node-ipc` | Protestware — wiped files on Russian/Belarusian IPs | 2022 | BLOCK |
| `colors` | Infinite loop sabotage by maintainer | 2022 | BLOCK |
| `faker` | Deliberate breakage by maintainer | 2022 | WARN |
| `ua-parser-js` | Supply chain compromise, cryptominer injected | 2021 | BLOCK |
| `coa` | Account takeover, malicious version pushed | 2021 | BLOCK |
| `rc` | Malicious versions published | 2022 | BLOCK |
| `ctx` | Harvested env vars from CI/CD pipelines | 2022 | BLOCK |
| `discord.js-self` | Unofficial fork, token stealer | ongoing | BLOCK |

## PyPI — Confirmed Malicious

| Package | Incident | Year | Action |
|---|---|---|---|
| `python-binance2` | Credential harvester for Binance API keys | 2022 | BLOCK |
| `setup-tools` | Typosquat for `setuptools` | ongoing | BLOCK |
| `colourama` | Typosquat for `colorama` | 2021 | BLOCK |
| `pytorch-nightly` | Malicious binary distribution | 2022 | BLOCK |
| `loglib-modules` | Data exfiltration to attacker server | 2023 | BLOCK |
| `aioconsole` (fake) | Typosquat with exfil payload | 2023 | BLOCK |
| `requests-darwin` | Requests typosquat, macOS targeting | 2022 | BLOCK |
| `httplib3` | Typosquat for `httplib2` | ongoing | BLOCK |

## High-Risk Typosquat Targets

Popular packages commonly impersonated. Flag any package with edit distance ≤ 2:

**Python**: requests, numpy, flask, django, boto3, pillow, scipy, pandas, tensorflow, anthropic

**Node.js**: express, lodash, axios, react, webpack, typescript, moment, chalk, commander, dotenv

## Unmaintained / Abandoned (WARN)

Flag these as MEDIUM risk — vulnerabilities may not be patched:
- `request` (npm) — deprecated 2020
- `moment` (npm) — feature-frozen, recommends migration
- `node-uuid` — superseded by `uuid`
