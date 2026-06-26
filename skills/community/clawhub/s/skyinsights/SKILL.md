---
name: skyinsights
description: >-
  Query the CertiK SkyInsights blockchain risk intelligence API. Use this skill
  when the user wants to check whether a wallet address or transaction hash is
  risky, look up labels or entity details, or run AML screening. Subcommands:
  kya, labels, screen, kyt.
license: MIT
metadata: {"url": "https://skyinsights.certik.com/", "script": "./scripts/skyinsights.py", "primary-commands": "kya labels screen kyt", "openclaw": {"requires": {"env": ["SKYINSIGHTS_API_KEY", "SKYINSIGHTS_API_SECRET"], "bins": ["python3"]}, "primaryEnv": "SKYINSIGHTS_API_KEY"}}
---

# SkyInsights Risk Intelligence

Use `{skillDir}/scripts/skyinsights.py` for all API calls. The script handles credentials, request formatting, error handling, screening polling, and terminal-friendly output.

## Running Commands

```bash
python {skillDir}/scripts/skyinsights.py <subcommand> [args...]
```

## Subcommands

- `kya <address> [chain=eth]` — `GET /v4/kya/risk`
- `labels <address> [chain=eth]` — `GET /v4/kya/labels`
- `screen <address> [chain=eth] [rule_set_id=standard-mode-rule-set]` — `GET /v4/kya/screening_v2` + poll (⚠️ 5–15s)
- `kyt <txn_hash> <chain>` — `GET /v4/kyt/risk`
- `help` — show usage

`rule_set_id` options: `standard-mode-rule-set` (default), `fast-mode-rule-set`

## Supported Chains

Per-endpoint chain support. Use the **API Value** when specifying the `chain` parameter.

| Chain | API Value | kya/labels | kya/risk | kya/screening_v2 | kyt/risk |
|---|---|:---:|:---:|:---:|:---:|
| Bitcoin | `btc` | ✓ | ✓ | ✓ | ✓ |
| Bitcoin Cash | `bch` | ✓ | ✓ | | |
| Litecoin | `ltc` | ✓ | ✓ | | |
| Solana | `sol` | ✓ | ✓ | | |
| Ethereum | `eth` | ✓ | ✓ | ✓ | ✓ |
| Polygon | `polygon` | ✓ | ✓ | ✓ | ✓ |
| Optimism | `op` | ✓ | ✓ | ✓ | ✓ |
| Arbitrum | `arb` | ✓ | ✓ | ✓ | ✓ |
| Avalanche | `avax` | ✓ | ✓ | ✓ | ✓ |
| Binance Smart Chain | `bsc` | ✓ | ✓ | ✓ | ✓ |
| Fantom | `ftm` | ✓ | ✓ | | |
| Tron | `tron` | ✓ | ✓ | ✓ | ✓ |
| Wemix | `wemix` | ✓ | ✓ | ✓ | ✓ |
| Base | `base` | ✓ | ✓ | ✓ | ✓ |
| Blast | `blast` | ✓ | ✓ | | |
| Linea | `linea` | ✓ | ✓ | | |
| Sonic | `sonic` | ✓ | ✓ | | |
| Unichain | `unichain` | ✓ | ✓ | | |
| Polygon zkEVM | `polygon_zkevm` | ✓ | ✓ | | |

> `kya/screening_v2` supports: `btc` `eth` `polygon` `op` `arb` `avax` `bsc` `tron` `wemix` `base`
> `multi-chain` is supported by `kya/risk` only.

## Default Workflow

Route user requests as follows:

- User mentions a **transaction hash / tx / txn** → run `kyt`
- User asks about **labels / entity / institution / exchange** for an address → run `labels`
- User asks if an **address is risky / safe / suspicious** (no subcommand specified):
  1. Run `kya` first — fast, checks the address's own labels and risk score.
  2. If `kya` returns `None` or `Low`, automatically follow with `screen` — a clean address can still have counterparty exposure to sanctioned or hacked funds. Tell the user: "该地址自身风险较低，正在进行合规筛查以检查对手方暴露情况，请稍候（约 5–15 秒）…"
  3. If `kya` returns `Medium`, `High`, or `Unknown`, present the result directly without running `screen`.

## Output Expectations

Printed shapes per subcommand:

```
# kya
Risk: {None|Low|Medium|High|Unknown} (score={0-5})
Reasons: {reason1}, {reason2}     ← omitted if empty

# labels
Entity: {name}  Type: {type}
Labels: {label1}, {label2}        ← omitted if none

# screen
Screening: {Pass|Fail|Pending}
Flagged counterparties: {count}
{counterparty_address}  {risk_level}  {reason}  ← one line per flagged party

# kyt
Tx Risk: {None|Low|Medium|High|Unknown} (score={0-5})
Transfers: {count}
{from} → {to}  {amount} {token}   ← one line per transfer
```

Risk level emojis: ✅ None / 🟡 Low / 🟠 Medium / 🔴 High / ⚪ Unknown

After running the script, summarize the key findings in plain language — especially the risk level and notable risk factors. Don't just repeat the raw output.

## Error Handling

| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad Request — invalid parameters (e.g., unsupported chain, malformed address) |
| 401 | Unauthorized — missing, invalid, or expired `X-API-Key` / `X-API-Secret` |
| 402 | Payment Required — account quota exceeded |
| 403 | Forbidden — access denied |
| 429 | Too Many Requests — rate limit reached |
| 500 | Internal Server Error |

- Missing credentials: tell the user to set `SKYINSIGHTS_API_KEY` and `SKYINSIGHTS_API_SECRET`.
- Unsupported chain: ask the user to retry with one of the supported chain identifiers.
- `risk_level` is `Unknown`: the address or transaction is not indexed on that chain, or has no available risk history.

## Risk Factors Reference

| Risk Factor | Default Level | Description |
|---|---|---|
| Sanctioned | High | Associated with international sanctions lists or restricted entities |
| TerroristFinancing | High | Involved in terrorist financing or support activities |
| ChildAbuse | High | Related to child exploitation or illegal content payments |
| Hack | High | Funds linked to hacking or security breach incidents |
| Scam | High | Fraud-related activities (e.g., phishing, rug pulls) |
| Ransomware | High | Connected to ransomware attacks or extortion |
| Darkweb | High | Associated with dark web markets or illicit transactions |
| Laundering | High | Associated with on-chain money laundering activities |
| Blocked | High | Officially frozen by stablecoin issuers (e.g., USDT, USDC) |
| Blacklisted | High | Listed in blacklists by users or partners |
| Mixing | Medium | Related to mixing services or fund obfuscation behavior |
| Gambling | Medium | Connected to gambling or betting platforms |

### Risk Score & Level Mapping

| Score | Level | Description |
|---|---|---|
| 0 | None | No known risk — no history of malicious behavior or suspicious associations |
| 1 | Low | Low likelihood of illicit involvement, no unusual behavior detected |
| 2–3 | Medium | Moderate risk due to indirect exposure or uncertain behavior |
| 4–5 | High | Strong indications of potential involvement in malicious or high-risk activity |

### Risk Reasons Format

The `risk_reasons` field explains why a risk was assigned. Each entry is prefixed by type:

- `label: Scam/Rugpull` — risk comes from a specific label
- `label: Sanction/OFAC`
- `entity: huione` — risk linked to a known entity without a direct label
- `entity: blender_io`

---

## Usage (for users)

When a user asks how to use this skill, show them these commands:

```
/skyinsights kya <address> [chain]       Address risk assessment / 地址风险评分
/skyinsights labels <address> [chain]    Address labels & entity info / 地址标签和实体信息
/skyinsights screen <address> [chain]    Compliance screening (AML) / 合规筛查，需 5–15 秒
/skyinsights kyt <txn_hash> <chain>      Transaction risk / 交易风险分析
/skyinsights help                        Show help / 显示帮助
```

**Prerequisites / 前提条件：** Set credentials in environment or `.env` file / 在环境变量或 `.env` 文件中设置凭证：
```
SKYINSIGHTS_API_KEY=your_key
SKYINSIGHTS_API_SECRET=your_secret
```
