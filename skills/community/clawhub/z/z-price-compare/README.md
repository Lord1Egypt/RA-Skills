# 🛒 Shopping Price Comparison Skill (Safe & Legal Version)

**Last Updated**: 2026-03-27  
**Version**: 1.0 - Safe Mode Only

---

## ⚠️ Important Legal Notice / 重要法律提示

This skill is designed for **PERSONAL, NON-COMMERCIAL USE ONLY**.

本技能仅供**个人非商业用途**。

### Compliance Statement / 合规声明

✅ What We Do / 我们做的:
- Use search engine APIs (`web_search`) to retrieve publicly indexed data
- Extract only what's visible in search result snippets
- Respect `robots.txt` and website Terms of Service
- No direct HTTP requests to target shopping platforms
- No JavaScript execution or DOM parsing
- No cookie manipulation or login attempts

❌ What We Don't Do / 我们不做的:
- Perform automated web scraping or crawling
- Bypass anti-bot measures or authentication
- Access member-only prices without login
- Collect data beyond reasonable personal use
- Redistribute platform-specific pricing data

---

## Quick Start / 快速开始

### Basic Usage / 基本用法

Just tell OpenClaw what you want to compare:

```
"帮我比价华为 MateBook 14 2024 款"
"看看 iPhone 15 Pro Max 哪个平台最便宜"
"索尼 WH-1000XM5 在京东和拼多多的价格对比"
```

OpenClaw will:
1. 🔍 Use `web_search()` API to find product info across platforms
2. 📊 Extract public price data from search snippets
3. 📝 Generate a markdown comparison report
4. 💡 Provide purchase recommendations

---

## How It Works / 工作原理

```
User Request → web_search API → Public Search Results → 
Parse Snippets → Generate Report
     ↓
   NO DIRECT PLATFORM ACCESS
```

**Key Difference from Scraping Tools:**

| Aspect | Traditional Scraper | This Skill |
|--------|---------------------|------------|
| Target | Direct site access | Search engine only |
| Data Source | HTML parsing | Search snippets |
| Rate Limits | Risk throttling | API rate limits apply |
| Login Required | Often tries to bypass | Not needed |
| Legal Risk | Medium-High | Very Low |

---

## Supported Platforms / 支持平台

| Platform | Code | Best For |
|----------|------|----------|
| 🟦 京东 | `jd` | Electronics, urgent items |
| 🔴 淘宝 | `taobao` | General merchandise |
| 🟧 天猫 | `tmall` | Brand name products |
| 🟢 拼多多 | `pdd` | Budget-friendly deals |
| ⚪ 1688 | `1688` | Wholesale/bulk |
| 🟣 苏宁 | `suning` | Home appliances |
| 🟡 义乌购 | `yiwugou` | Small commodities |
| 🔴 唯品会 | `vipshop` | Fashion discounts |

---

## Output Example / 输出示例

```markdown
# 🛒 iPhone 15 Pro Max 比价报告

## 💡 核心结论
💡 推荐渠道：**拼多多** - ¥7,299 (百亿补贴最划算)

---

## 📊 价格对比表

| 排名 | 平台 | 价格 | 到手价 | 销量 | 备注 |
|------|------|------|--------|------|------|
| 🥇 | 拼多多 | ¥7,299 | ¥7,299 | 10 万 + | 百亿补贴 |
| 🥈 | 京东 | ¥7,599 | ¥7,599 | 5 万+ | 自营 |
| 3 | 天猫 | ¥7,699 | ¥7,659 | 3 万+ | 旗舰店 |

---

## ✅ 购买建议

⚠️ **温馨提示**: 以上价格来自搜索引擎索引，实际购买请以各平台页面为准。
```

---

## File Structure / 文件结构

```
shopping-price-compare/
├── SKILL.md                    # Main skill definition (with full disclaimer)
├── QUICKSTART.md               # User guide with examples
├── README.md                   # This file - overview and compliance notice
├── scripts/
│   └── price_checker.py        # Core logic (web_search based, compliant)
└── references/
    └── platform_info.md        # Platform characteristics (public info only)
```

---

## Limitations / 局限性

### What You CAN Get / 你能得到的:
- List prices shown in search snippets
- Product titles and basic specs
- Sales volume indicators (if indexed)
- General price ranges per platform

### What You CANNOT Get / 你不能得到的:
- Member-exclusive prices (requires login)
- Real-time coupon calculations
- Current stock levels
- Location-specific shipping costs
- Live promotional deals requiring interaction

### Workaround / 解决方案:
For most accurate pricing:
1. Use this skill for initial research
2. Click provided links to visit actual platforms
3. Check final prices after login
4. Share the actual prices with OpenClaw for final comparison

---

## Legal Disclaimer / 完整免责声明

See [`SKILL.md`](./SKILL.md) section "**Legal Disclaimer / 法律免责声明**" for full details.

TL;DR:
- Personal non-commercial use only ✅
- No warranty provided ✅  
- Users responsible for their compliance ✅
- No liability for any consequences ✅

---

## Version History / 版本历史

### v1.0 (2026-03-27) - Initial Safe Release
- ✅ Removed all scraping/crawling functionality
- ✅ Replaced with `web_search` API usage
- ✅ Added comprehensive legal disclaimers
- ✅ Created safe-mode documentation
- ❌ Deprecated browser automation scripts
- ❌ Removed MCP configuration guides

### Planned Future Versions
- v1.1: Better search query optimization
- v1.2: Support for more platforms
- v2.0: Optional integration with official affiliate APIs

---

## Contributing / 贡献

If you find issues or have suggestions:
1. Check if it's related to search limitations (expected behavior)
2. Verify you're using it for personal, non-commercial purposes
3. Contact me with specific feedback

**Commercial Use?** Contact us for licensing or use official APIs instead.

---

_Happy safe shopping! Remember to verify prices on official platforms before purchasing! 🛍️_

**Important**: Always confirm final prices on the actual platform pages before making purchases.