# Shopping Price Comparison (Safe Mode)

通过搜索引擎查找各电商平台上的商品价格信息，生成对比报告和购买建议。

⚠️ **重要提示**: 本技能仅使用公开可访问的搜索引擎数据，不涉及任何自动化爬取行为。

---

## ⚖️ Legal Disclaimer / 法律免责声明

### 🇺🇸 English Version

This skill is designed for **personal, non-commercial use only**.

**Compliance Statement:**
- ✅ We do NOT perform automated web scraping or crawling
- ✅ All data is obtained from publicly available search engine results only
- ✅ No attempts are made to bypass anti-bot measures or authentication
- ✅ Respects `robots.txt` and website Terms of Service
- ⚠️ Users are responsible for their own compliance with local laws

**Prohibited Uses:**
- ❌ Commercial exploitation of any collected data
- ❌ Mass data collection beyond reasonable personal use
- ❌ Circumventing access controls or rate limiting
- ❌ Redistributing platform-specific pricing data
- ❌ Any activities that could damage platform services

**Recommendations:**
1. Use sparingly - only when comparing a few items personally
2. Accept that search results may not show all available prices
3. For critical purchases, verify prices directly on the platform
4. Consider using official affiliate APIs for commercial needs

---

### 🇨🇳 中文版

本技能仅供**个人非商业用途**。

**合规声明:**
- ✅ 不进行任何自动化网页爬取或抓取行为
- ✅ 所有数据均来自公开可访问的搜索引擎结果
- ✅ 不尝试绕过反爬虫机制或身份验证
- ✅ 尊重 `robots.txt` 和各网站服务条款
- ⚠️ 用户需自行承担遵守当地法律的责任

**禁止用途:**
- ❌ 商业性利用任何收集的数据
- ❌ 超出合理个人使用范围的大规模数据收集
- ❌ 规避访问控制或速率限制
- ❌ 重新分发特定平台的价格数据
- ❌ 任何可能损害平台服务的活动

**建议做法:**
1. 节制使用 - 仅在个人比较少量商品时使用
2. 理解搜索可能无法显示所有可用价格
3. 重要购买请直接在平台上核实价格
4. 商业需求请使用官方联盟 API

---

### ⚠️ Disclaimers / 免责条款

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

本软件按"原样"提供，不提供任何形式的保证，包括但不限于对适销性、
特定用途适用性和非侵权的保证。在任何情况下，作者或版权持有人均不对
任何索赔、损害或其他责任负责，无论是因合同纠纷、侵权行为还是其他方
面，因软件或软件的使用或其他交易而引起。

---

## Quick Start

当需要购物时，直接告诉我你想买的商品，例如：

```
"帮我看看 iPhone 15 Pro Max 哪个平台最便宜"
"比较一下索尼 WH-1000XM5 在不同电商的价格"
"买华为 MateBook 14，预算 6000 以内"
```

OpenClaw 会：

1. 🔍 使用搜索引擎查询各平台的价格信息
2. 📊 从公开页面提取可见数据
3. 📝 生成对比表格和购买建议

---

## Supported Platforms / 支持的平台

| 平台 | URL | 特色 | 适合场景 |
|------|-----|------|----------|
| 🟦 京东 | `https://item.jd.com` | 正品保障、快速配送 | 高价值物品、急用商品 |
| 🔴 淘宝 | `https://s.taobao.com` | 品类最全、价格多样 | 非标品、特色商品 |
| 🟧 天猫 | `https://search.tmall.com` | 品牌官方旗舰店 | 品牌正品保障 |
| 🟢 拼多多 | `https://mobile.yangkeduo.com` | 低价团购、百亿补贴 | 追求性价比 |
| ⚪ 1688 | `https://s.1688.com` | 批发价、厂家直供 | 多件采购 |
| 🟣 苏宁 | `https://list.m.suning.com` | 家电专长 | 大家电、电子产品 |
| 🟡 义乌购 | `https://www.yiwugou.com` | 小商品源头 | 小物件批发 |
| 🔴 唯品会 | `https://www.vipshop.com` | 品牌特卖 | 服装鞋包折扣 |

---

## How It Works / 工作原理

### Safe Data Collection Method

```python
# Step 1: Search each platform via search engine
web_search(
    query="商品名称 site:jd.com OR site:tmall.com OR site:pdd.com",
    count=10,
    safeSearch="moderate"
)

# Step 2: Extract visible data from search snippets
# Only reads what's already indexed and publicly shown

# Step 3: Generate comparison report
# Combines data with context analysis
```

**Key Safety Features:**
- ✅ No direct HTTP requests to target sites
- ✅ No JavaScript execution or DOM parsing
- ✅ No cookies or session manipulation
- ✅ Rate-limited to prevent overloading search engines
- ✅ Only uses public search results

---

## Output Format / 输出格式

### Standard Comparison Report

When you ask for price comparison, you'll receive:

```markdown
# 🛒 [商品名称] 比价报告

## 💡 核心结论
💡 **推荐渠道**: [平台] - ¥[价格] ([推荐理由])

---

## 📊 价格对比表

| 排名 | 平台 | 价格 | 运费 | 到手价 | 销量 | 备注 |
|------|------|------|------|--------|------|------|
| 🥇 | 拼多多 | ¥7,299 | 包邮 | **¥7,299** | 10 万 + | 百亿补贴 |
| 🥈 | 京东 | ¥7,599 | 包邮 | **¥7,599** | 5 万+ | 自营 |
| 3 | 天猫 | ¥7,699 | 包邮 | **¥7,659** | 3 万+ | 旗舰店 |

---

## 🔍 详细分析

### 🥇 [平台名] - 首选推荐
- **价格优势**: 最低价，比次低贵 X%
- **信任度**: {销量} 销量，{好评率}% 好评
- **注意事项**: {特定平台的购买建议}

### 🥈 [平台名] - 备选方案
- **优势**: {相比首选的优势点}
- **适用场景**: {什么时候选这个更合适}

---

## ✅ 购买建议

💰 **差价分析**: 最高价与最低价相差 XX 元  
⚠️ **风险提示**: {可能的风险点}  
📅 **时机判断**: 当前价格是否值得入手

> ⚠️ **温馨提示**: 以上价格来自搜索引擎索引，实际购买请以各平台页面为准。
```

---

## Limitations / 局限性

Understand these constraints when using this skill:

### What Search Results CAN Provide
- ✅ List prices displayed in search snippets
- ✅ Product titles and basic specifications
- ✅ Sales volume indicators (if indexed)
- ✅ Basic platform reputation signals

### What Search Results CANNOT Provide
- ❌ Member-only prices (requires login)
- ❌ Real-time coupon calculations
- ❌ Shipping costs to your specific location
- ❌ Current stock availability
- ❌ Live promotional discounts
- ❌ Bundle deals requiring page interaction

### Workarounds
For most accurate pricing:

1. **Manual Verification (Recommended)**
   ```
   1. OpenClaw provides links to each platform
   2. You manually open these pages
   3. Tell me the actual prices you see
   4. I'll generate final comparison
   ```

2. **Accept Approximate Data**
   - Use search-based estimates for initial research
   - Verify final decision on-platform
   - Factor in potential ±10-20% price variance

---

## Usage Best Practices / 最佳实践

### DO ✅
- Use for personal shopping decisions
- Compare a few items occasionally
- Verify important purchases on-platform
- Respect rate limits (ask questions spaced out)
- Accept data limitations gracefully

### DON'T ❌
- Use for commercial price monitoring
- Request hundreds of comparisons at once
- Try to get around login requirements
- Distribute collected data to others
- Treat search snippets as authoritative prices

---

## Examples / 使用示例

### Basic Comparison
```
User: 帮我比价华为 MateBook 14 2024 款
Agent: (Uses web_search → generates markdown report)
```

### With Budget Constraint
```
User: 找 MacBook Air M2，不要超过 7000 元，包邮
Agent: (Filters by price constraint → shows matching options)
```

### Platform-Specific
```
User: 只查京东自营和天猫旗舰店的价格
Agent: (Limits search to specified platforms only)
```

---

## Related Files / 相关文件

- `QUICKSTART.md` - More detailed usage guide
- `scripts/price_checker.py` - Implementation code
- `references/platform_info.md` - Platform characteristics

---

## Version History / 版本历史

- **v1.0 (2026-03-27)**: Initial release with safe-mode only
  - Removed all scraping/crawling functionality
  - Added comprehensive legal disclaimers
  - Implemented search-engine-based data collection

---

_This skill is designed for safe, compliant price research. Always verify prices on official platforms before purchasing._
