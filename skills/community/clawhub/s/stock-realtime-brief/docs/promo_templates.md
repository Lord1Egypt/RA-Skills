# 推广文案模板

## 1. Reddit r/algotrading（英文）

**Title**: [Open-source] A-share (China) realtime analyzer with three-tier hard stop-loss and announcement detection — feedback welcome

**Body**:

I've been frustrated with how most A-share analysis tools output things like "consider careful trading" or "watch sentiment" — meaningless without trigger conditions or specific actions.

After 3 weeks of dogfooding on my own portfolio, I've open-sourced **stock-realtime-brief** — a CLI/Python lib that produces *actually executable* recommendations.

**Three modes:**
- 📦 **Portfolio**: full pre-market briefing with margin coverage check + 14-day announcement scanner
- 🔍 **Single**: deep-dive analysis with 5 operational levels
- 📊 **Multi**: side-by-side comparison with composite scoring

**Key opinionated design:**
- Three-tier hard stop loss (Warning / Risk / Cut) instead of one-size-fits-all
- "Profit lock level" for positions up >30% (not the usual cost-15% which becomes meaningless)
- Risk-based ranking (loss × margin × MA20 break × heavy weight)
- All recommendations come with trigger conditions you can directly set as conditional orders
- Battle-tested data source fallback: Tencent → Sina → AKShare (avoid the AKShare timeout pit)

GitHub: https://github.com/Michaelliugh/stock-realtime-brief

Honest disclaimer: This is for A-share market only. The methodology should generalize to other markets but the data sources and announcement detection are A-share specific.

Looking for feedback on:
1. The three-tier stop loss algorithm — is the "profit lock" too aggressive?
2. Multi-mode composite scoring — what indicators would you add?
3. Anyone interested in extending to HK/US markets?

Cheers!

---

## 2. V2EX /go/stock 节点（中文）

**标题**：[开源] 一个开箱即用的 A 股盘前简报工具 — 给有持仓的散户用

**正文**：

各位 V 友好

写了个 CLI 工具叫 stock-realtime-brief，自己用了 3 周觉得还行，开源出来分享。

它解决一个具体问题：**散户在开盘前的 5 分钟，怎么把所有该做的决策一次想清楚？**

不是"分析师推荐股票"那种工具，而是"按你的实际持仓 + 实时行情，给出今天上午每只票该挂什么条件单"的清单生成器。

**核心特点**：

1. 三档硬止损（预警/风控/清仓），不是一刀切
2. 盈利 30%+ 自动给"利润保护位"（避免 cost*0.85 这种笑话）
3. 融资融券自动算担保比例 + 五档预警
4. 自动拉近 14 天减持/立案/业绩预减公告
5. 重仓股容错率自动收紧 5%
6. 输出全部是"触发位 + 动作 + 数量"，可直接抄进券商 APP

**数据源策略**：
- 腾讯财经（实时，最稳）
- 新浪批量（多只行情）
- AKShare（历史 K 线）

避开了 AKShare 主源 `82.push2.eastmoney.com` 在交易日早盘频繁超时的坑（实测最久卡过 50 分钟）。

**用法**：

```bash
pip install -e .

# 单股
stock-brief --code 300750

# 多股对比
stock-brief --codes 600519,300750,600036

# 持仓简报
stock-brief --portfolio my_portfolio.json
```

GitHub: https://github.com/Michaelliugh/stock-realtime-brief

MIT 协议，欢迎 PR。

也欢迎拍砖 — 尤其是对三档止损算法、综合评分公式的意见，这两个我打磨过几次但肯定还有优化空间。

不构成投资建议，使用风险自负（详见仓库 DISCLAIMER.md）。

---

## 3. 雪球（中文）

**标题**：开源了一个我自己用的 A 股盘前简报工具

**正文**：

各位球友

利用最近大盘震荡的几周，我把自己的"盘前看盘流程"沉淀成了一个工具。

简单说，我每天早上 8:50 跑一遍，10 秒后拿到一份长这样的清单：

[贴 portfolio sample 截图]

包含：
- 持仓实时态势 + 浮盈
- 关键均线 + 三档硬止损位
- 融资担保比例评估（如果有融资）
- 近 14 天重要公告告警（减持/立案/业绩预减）
- 今早可执行的条件单清单（按 P0/P1/P2 优先级）

不是教你怎么炒股，是帮你**把已经想好的规则自动化**。

5 月 6 日早盘我用它发现了天岳先进的减持公告（5/1 公告，8 月 26 日才开窗减持），借早盘 +6% 强势卖了 8000 股，落袋 14.62 万。如果当时只看技术面（多头排列、站上 MA5）我可能会扛着等更高点。

GitHub 已开源，MIT 协议，欢迎拿去自己改：
https://github.com/Michaelliugh/stock-realtime-brief

不构成投资建议。仅供参考。

---

## 4. 微信公众号 / 知乎专栏

**标题**：我把 3 周的盘前看盘经验做成了一个开源工具，免费给所有人用

**摘要**：
散户的最大敌人不是市场，是开盘前 5 分钟的情绪混乱。这个工具用来对抗这个混乱。

**关键钩子段**：
- 数据：实测某 AKShare 主源 50 分钟无响应（如何避坑）
- 故事：5/6 天岳减持公告 → 借强势减仓 14.62 万实战
- 设计哲学：为什么"亏 15% 止损"对盈利股是个笑话
- 反思：为什么"建议关注"是无效输出

**Call to action**：
- ⭐ Star 支持
- 提 Issue 反馈
- 二次开发欢迎

---

## 5. Twitter/X 简短版（英文）

> Just open-sourced **stock-realtime-brief** — A-share CLI analyzer that outputs **actually executable** recommendations (specific price + specific action + specific quantity).
>
> Three modes (portfolio/single/multi), three-tier hard stop loss, profit lock for >30% gains, auto announcement scanner, margin risk check.
>
> https://github.com/Michaelliugh/stock-realtime-brief 🇨🇳📊

---

## 6. 微博 / 朋友圈（中文，最简）

> 开源了一个 A 股盘前分析工具，写给有持仓的散户。
> 三种模式（持仓/单股/多股）+ 三档硬止损 + 自动公告检测 + 融资风险体检。
> 输出可直接抄进券商条件单。
> MIT 协议，自己用得不错才开源。
>
> 链接：[github 链接]
> 不构成投资建议。

---

## 发布顺序建议

1. **Day 1**: V2EX + 雪球（中文社区先行，验证早期反馈）
2. **Day 2-3**: 修早期 issue / typo
3. **Day 4**: 微博 + 公众号 / 知乎（个人渠道引流）
4. **Day 7**: Reddit r/algotrading（英文社区，流量大）
5. **Day 10**: Twitter/X（如有英文受众）
6. **持续**: 在你回答的金融/投资话题里自然提及

## 数据追踪

发完每个渠道，记录：
- 1 小时内 stars
- 24 小时内 stars + issues + PRs
- 7 天后 stars + 真实用户使用反馈

调整下一波渠道侧重。
