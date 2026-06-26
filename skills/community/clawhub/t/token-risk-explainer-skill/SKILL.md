---
name: token-risk-explainer-skill
description: Explain crypto token risk in plain Chinese and English from Binance Web3 token audit and market metadata. Use this skill when users want a contract-level risk score, factor-by-factor explanation, comparison between tokens, watchlist triage, and ready-to-send community or Binance Square risk copy.
---

# Skill: token-risk-explainer-skill

## Purpose / 用途
Use this skill to turn raw token audit signals into a readable risk explanation for users, community managers, and content operators.
用这个 skill 可以把原始风控字段转成用户看得懂的风险解释，适合新手教育、社群预警、内容科普和快速筛查。

## Commands / 命令
Run from the skill root:
在 skill 根目录执行：

```bash
python3 scripts/token_risk_explainer.py explain --chain bsc --contract 0x1234 --lang zh
python3 scripts/token_risk_explainer.py compare --chain bsc --contracts 0xaaa,0xbbb --lang zh
python3 scripts/token_risk_explainer.py watchlist --chain bsc --input ./contracts.txt --lang zh
python3 scripts/token_risk_explainer.py health
```

## Output Contract / 输出结构
`explain` returns:
- `token`
- `contract_address`
- `chain`
- `risk_score`
- `risk_level`
- `risk_summary_zh`
- `risk_summary_en`
- `risk_factors[]`
- `continue_research`
- `community_alert_draft`
- `square_post_draft`

## Billing Hook (SkillPay) / 计费预留
- Bill only `explain`, `compare`, and `watchlist`.
- Read API key from `SKILLPAY_APIKEY`.
- Default price comes from `SKILLPAY_PRICE_USDT`.
- Keep secrets in environment variables only.

## Notes / 说明
- This skill is read-only. It does not place orders.
- Output must remain neutral. Never promise safety or returns.
- `LOW` risk does not mean safe. It only means fewer visible red flags in the current snapshot.
