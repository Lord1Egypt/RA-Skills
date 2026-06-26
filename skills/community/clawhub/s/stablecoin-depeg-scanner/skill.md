---
name: stablecoin-depeg-scanner
description: Evaluate stablecoin depeg events for crisis arbitrage opportunities. Use when a user mentions a stablecoin crash, depeg, exploit, hack, or asks whether to buy a depegged stablecoin. Triggers on keywords like "depeg", "depegged", "stablecoin crash", "脱锚", "稳定币暴跌", "稳定币脱钩", "能不能抄底", "mint exploit", "USR", "UST", "should I buy", "black swan", "黑天鹅".
---

# Stablecoin Depeg Scanner 🔍

3-minute crisis arbitrage evaluator. When a stablecoin loses its peg, run the assessment to decide: buy, watch, or avoid.

## Philosophy

Depeg = panic pricing. The question is NOT "is it safe" but "is the discount bigger than the real damage?" Small position, high odds, asymmetric payoff.

## Quick Start

When user mentions a stablecoin depeg event:

### Step 1: Run the automated evaluator (60 seconds)

```bash
cd SKILL_DIR && python scripts/depeg_eval.py <COIN> --capital <USER_CAPITAL>
```

- `<COIN>`: CoinGecko ID or symbol (e.g., `resolv-usr`, `USR`, `DAI`)
- `--capital`: User's total available capital in USD (default: 5000)
- `--peg`: Target peg price if not $1.00 (default: 1.0)

The script auto-fetches: current price, market cap, TVL from DefiLlama, and calculates odds + position size.

Replace `SKILL_DIR` with the resolved absolute path of this SKILL.md's parent directory.

### Step 2: Complete exploit analysis (60 seconds)

The script outputs a checklist. Use `web_search` to answer these questions:

1. **Was collateral stolen or was it a mint/logic exploit?**
   - Search: `"<coin_name> exploit PeckShield"` or `"<coin_name> hack SlowMist"`
   - Mint/logic exploit (collateral intact) → bullish
   - Collateral drained → bearish

2. **Has the team responded?**
   - Check their Twitter for pause announcement
   - Response within 1h → good sign
   - Silent >6h → red flag

3. **Is the bug fixable?**
   - Smart contract bug with clear fix → recovery likely
   - Fundamental design flaw → avoid

### Step 3: Adjust and deliver recommendation (60 seconds)

Based on exploit analysis, adjust the script's score:

- Collateral confirmed intact → score +10
- Team responded fast with plan → score +10  
- Collateral partially stolen → score -10
- No team response → score -20
- Algorithmic stablecoin / no real backing → score -50 (AVOID regardless)

Deliver final recommendation with:
- Action: BUY / WATCH / AVOID
- Position size in USD
- Entry price range
- Exit target
- Stop condition

## Decision Framework

For detailed scoring logic, exploit type analysis, historical benchmarks, and red/green flags, read `references/decision-framework.md`.

## Output Format (to user)

```
🔍 稳定币脱锚评估: <SYMBOL>

📊 价格:
• 当前: $X.XX | 锚定: $1.00 | 偏离: XX%
• 赔率: X.Xx

🏦 抵押物:
• TVL: $XXM (较昨日 -X%)
• 状态: 完整/部分损失/已掏空

🔐 攻击分析:
• 类型: 铸造漏洞/预言机/抵押物被盗
• 团队响应: 已暂停/未回应
• 可修复性: 高/中/低

📋 结论:
• 操作: 🟢买入 / 🟡观望 / 🔴回避
• 仓位: $XXX (总资金X%)
• 目标: $X.XX
• 止损条件: XXX
```

## Key Rules

1. **Speed over perfection** — 3 minutes, not 30 minutes. First-mover advantage is everything.
2. **TVL is truth** — DefiLlama TVL > official statements. Contracts don't lie.
3. **Small positions only** — Never >6% of capital on a single depeg bet.
4. **Algorithmic = death** — No real collateral = no recovery. Luna/UST is the permanent lesson.
5. **Exit plan before entry** — Know your sell condition before buying.
