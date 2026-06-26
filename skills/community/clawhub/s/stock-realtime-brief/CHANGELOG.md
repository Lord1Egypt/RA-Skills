# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [4.2.0] - 2026-05-29 (失败复盘驱动的纪律升级)

### 🚨 重要升级 - 基于真实失误的反思 + 修正

**触发事件**：2026-05-29 "卖中天买通富" 换仓决策当日就被市场打脸
- 中天反弹 +6.79% (卖飞 ¥3,500)
- 通富立刻浮亏 -1.85% (¥9,300)
- 同板块同跌（罗博/华工/通富 -2 到 -6%）
- 集中度风险上升

### 复盘洞察（5 大问题）

1. ❌ 误用主线锁定铁律（主线/支线 = 新建仓 选择，≠ 减仓决策）
2. ❌ 忽视同板块同涨跌风险
3. ❌ 没考虑已浮盈 +40% 仓位的特殊性
4. ❌ 一天内反复改建议（违反 v3.2 入场计划冻结）
5. ❌ 没有"不操作"作为默认选项

### Added - 7 条新铁律（4-10）

- **铁律 4**: "不操作" 为默认选项
- **铁律 5**: 已浮盈 +30% 小仓位特殊保护（Let winners run）
- **铁律 6**: 同板块集中度上限（60-80%）
- **铁律 7**: 主线/支线分类的适用边界（仅用于新建仓）
- **铁律 8**: 操作频次限制（24h 1 次 / 7 天 2 次）
- **铁律 9**: 卖飞防御机制（24h 禁言）
- **铁律 10**: 用户阶段识别（建仓/持有/收割）

### Added - 5 大新检查模块（disciplines.py）

- `check_action_necessity()` - 操作必要性检查
- `check_sector_concentration()` - 同板块集中度检查
- `detect_user_phase()` - 用户阶段识别
- `winning_position_protection()` - winner 仓位保护
- `post_action_review()` - 卖飞反思 + 24h 禁言
- `comprehensive_v42_check()` - 综合纪律检查

### Lessons Learned (案例 4)

> 主线/支线评分 30 分 ≠ 应该减仓
> 已浮盈 +40% 的小仓位 = winner，应 let it run
> 加仓前必须检查 同板块集中度
> 一天内同票最多 1 次操作建议
> 已落袋 ¥100 万+ = 进入"收割期" → 减少操作

### Philosophical Shift

```
v4.1: 主动推荐操作 → 锁定主线 → 替换支线
v4.2: 默认"不操作" → 保护胜利果实 → Let winners run
```

### 文档增量

- `docs/principles/trading-discipline.md` (新增铁律 4-10)
- `docs/principles/data-freshness.md` (新增案例 4)
- `docs/principles/reflection-case-zhongtian-tongfu.md` (完整复盘报告 8500 字)

## [4.1.0] - 2026-05-29 (金融博士铁律集成)

### 🎉 5 大新能力 - 金融博士级投研体系

基于上海金融女博士「牛市五条核心铁律」全面优化：

### Added - 4 个新模块
- **main_line_tracker.py** 主线赛道识别引擎
  - 三大标准评分：板块持续性 + 批量大涨股 + 龙头梯队
  - 自动识别 主线 / 次主线 / 支线
  - 输出 一/二/三线龙头梯队

- **market_phase.py** 牛熊阶段判断器
  - 监控 4 大指数（上证 / 深成 / 创业板 / 科创 50）
  - 自动判定 5 大阶段
  - 自动给出 阶段化仓位建议（牛市初/主升/末期）

- **end_wave_detector.py** 鱼尾行情预警
  - 检测主线龙头长上影线（高位滞涨）
  - 检测垃圾股普涨（全民炒股）
  - 综合评分 + 4 级风险预警

- **shake_vs_break.py** 洗盘 vs 破位智能区分
  - MA20/MA30 跌破判定
  - 3 日主力资金净流出
  - 5 日跌幅范围
  - 长上影线 + 收阴
  - 综合 4 维评分 → 洗盘/破位判定

### New Commands (主入口)
- `python3 run_brief.py mainline` - 主线赛道识别
- `python3 run_brief.py phase` - 市场阶段判断
- `python3 run_brief.py endwave` - 鱼尾预警
- `python3 run_brief.py shake CODE` - 洗盘破位判定

### Improved
- 12 维评分系统 升级为 金融博士标准
- 仓位策略 从 单股 50% 升级为 阶段化（20-70%）
- 主线优先 + 支线规避 自动判断
- 龙头梯队 一/二/三线 自动分类

### Lessons Implemented (来自 5 月 ¥103 万 实战)
- 5/27 反思"保守了" → 入场计划冻结
- 5/28 罗博临停 → 鱼尾预警识别
- 5/22 新莱止损 → 破位判定

### Inspiration
- 上海金融女博士《牛市五条核心铁律》
- 五条铁律：主线锁定 / 主升突破 / 仓位分级 / 鱼尾撤退 / 趋势持仓

## [4.0.0] - 2026-05-28 (All-in-One 重大升级)

### 🎉 重大整合
- **All-in-One**: 整合 4 个独立 skill 进入 stock-realtime-brief
- 新增 **smart_picker** 模块（89 只候选股 / 5 大策略 / 12 维评分）
- 新增 **price_watcher** 模块（盯盘 Agent / QQ 自动推送）
- 新增 **disciplines** 模块（4 大纪律守护）

### Added
- **风险收益比量化器**: 3 档上涨 + 3 档下跌 + 风险收益比
- **情绪化拦截器**: FOMO / 反思补偿 / 报复交易 / 抄底 心态拦截
- **入场计划冻结**: 入场后不得新增止盈条件
- **杠杆使用门禁**: 3 道关卡（体系性 + 正期望 + 压力测试）
- **板块强度排名**: 15 板块平均涨跌 + 平均分 + 龙头
- **主力资金流追踪**: 3/5/10 日累计净流入
- **MACD/RSI/MA 完整技术指标**

### v4.0 命令
- `pick` - 智能选股
- `sectors` - 板块强度排名
- `push` - QQ 推送简报
- `watch` - 盯盘 Agent
- `rr` - 风险收益比量化
- `check` - 纪律综合检查

### Migration
- 旧 `stock-smart-picker` skill 已合并
- 旧 `price-watcher` project 已合并
- 旧 `v3.2 决策模板` 已合并

## [3.1.0] - 2026-05-26

### Added（重要！基于实战教训）
- **第一重要原则：数据与消息时效性检查**
  - 来源：2026-05-26 用户经过实战教训后明确要求
  - 强制流程：任何搜索结果使用前 100% 核查时效性
  - 自检清单：数据日期 / 消息发布日 / 是否已 price-in / 当时股价反应

### Lessons Learned (重要案例)

> **教训案例 1：新莱应材 (2026-05-26)**
> 误判 2025-01 已了结的"实控人立案"为新利空
> 差点让用户 ¥84 万持仓在几乎平本时清仓
> 实际今天主力净流入 ¥4461 万（散户恐慌出逃）
> 
> **教训案例 2：罗博特科 5/22 (2026)**
> 误判"5/25 解禁 5.72%"为致命利空
> 实际解禁日罗博暴涨 +13%
>
> **教训案例 3：天岳先进 5/6 (2026)**
> 误判"减持公告"为有效利空
> 实际从 ¥110 涨到 ¥180 (+64%)

### Rules
- 1 年以上的"利空" → 通常已被 price-in
- 超过 3 个月的消息 → 慎用
- 找不到日期的信息 → 不能作为决策依据
- 任何"立案/处罚/减持/解禁"必须查发生日期

## [3.0.0] - 2026-05-22

### Major Architecture Change（重大架构升级）

**用户指导**：盘中实时分析 ≠ 周期分析，重点落在量价关系

之前的混淆：把"盘中即时分析"和"盘后单股长期评估"混在一起 → 给盘中场景输出周期共振结论，不可执行。

### Added
- **盘中实时分析模块** (`realtime_analyzer.py`)
  - 维度：量价 + 资金 + 技术 + 板块
  - 不谈月线/周线（盘后用）
  - 输出：当下状态 + 趋势预判 + 立即可做的策略

- **量价配合判断**（核心信号）
  - 量价齐升 (健康)
  - 价升量缩 (滞涨警惕)
  - 价升主动卖 (顶部信号) 
  - 量价齐跌 (杀跌中)
  - 价跌量缩 (恐慌减弱)
  - 放量震荡 (多空分歧)

- **资金动向分析**
  - 内外盘比（主动买卖）
  - 五档盘口厚度（买卖压力）

- **盘中形态识别**
  - 冲高回落 / 强势上攻 / 弱势杀跌 / 横盘震荡 / 高位回落

### Changed
- SKILL.md 加入"双模式触发关键词"
  - 盘中模式：实时 / 现在怎么样 / 盘中
  - 盘后模式：深度分析 / 多周期 / 单股研究

### Lessons Learned

> 罗博 5/22 盘中：滞涨 + 内外盘均衡 + 冲高回落 = 盘中减仓信号
> 罗博 5/22 盘后：月/周/日三周期共振 + 高盛 ¥688 = 长期持有
> 
> 两个结论看似矛盾，实际是不同时间维度的合理结合。
> 之前 skill 只有一套逻辑 → 错位给建议。
> v3.0 后正确区分两个场景。

## [2.9.0] - 2026-05-22

### Added (重大升级)
- **多周期共振分析模块** (`multi_timeframe.py`)
  - 核心原则：月 K 定趋势 / 周 K 定波段 / 日 K 定买卖点
  - 源于专业操盘手多年实战经验
  - 补齐之前 “只看日 K” 的重大缺陷
- **三周期独立分析**
  - 趋势 7 档（强多/多/弱多/震荡/弱空/空/强空）
  - 阶段识别（新高附近/高位回调/中位调整/深度调整/底部区域）
  - 5 条均线（MA5/10/20/30/60）
  - KDJ + MACD 多周期
- **共振决策矩阵**
  - 🚀🚀 三周期共振做多（重仓）
  - ✅ 趋势内调整买入
  - 🚨 月线已破/日线反弹 = **逃命反弹**
  - ⛔ 中长期空头（清仓）
  - 10+ 场景识别
- **评分权重**：月×3 / 周×2 / 日×1（月线为王）

### Data Source
- 腾讯 K 线 API（https://web.ifzq.gtimg.cn/）
  - 日 K 200 条
  - 周 K 200 条
  - 月 K 100 条（约 7-8 年历史）

### Why this matters
> 之前仅看日线是重大缺陷。
> 例：“日 K 跳破 MA20” 你以为是顶，实际可能是月线主升中的中继。
> 同样，日 K 反弹看似很好，月线已破则是逃命反弹。
> 这是职业操盘手 vs 散户的核心差异。

### Example Output

```
📊 多周期共振分析 · 罗博特科

月线：🚀 强多头 / 新高附近
周线：🚀 强多头 / 中位调整 11.2%
日线：⚠️ 跌破 MA20 / MACD 绿柱↓

🎯 综合: 🚀🚀 三周期共振做多
💡 建议：不需慌，月线趋势未破。
```

## [2.8.0] - 2026-05-21

### Added
- **机构研报扰索模块** (`research_reports.py`)
  - 目标价提取（均值 / 最高 / 最低）
  - 评级分布（买入/增持/中性/减持/卖出计数）
  - 券商覆盖识别（30+ 主流券商库）
  - 综合评级推断
  - 上涨空间计算
  - 评级升降级信号（升位/降位检测）
  - 近期研报清单

### Why this matters
> 研报是上下技术面外的重要补充信息。
> 例：罗博特科高盛给 ¥688 买入目标价、未上涨 +26.5% 空间——这类信息之前需要手动查询，现在自动扣入分析。

### Use Cases

```python
from stock_realtime_brief.research_reports import fetch_research_reports, format_report_summary

result = fetch_research_reports('300757', '罗博特科')
print(format_report_summary(result, current_price=544))
```

## [2.7.0] - 2026-05-21

### Added
- **回撤分析模块** (`calc_drawdown` in `indicators.py`)
  - 当前回撤（现价距全局高点）
  - 区间最大回撤（高质量回调反手）
  - 全局高点价位 + 距高点交易日数
  - 6 级风险分级：新高附近 / 健康回调 / 中度 / 深度 / 重度 / 腰斩级
- 持仓 + 单股模式输出均包含回撤信息
- 可以用于“是否高位”、“是否抢反弹”、“跟踪回调质量”

### Why this matters
> 之前仅看“40 日涨幅”和“区间高低”，不够直观。
> 回撤分析是估值高低 + 仓位控制的重要参考。
> 例：罗博 11% 回撤（中度调整） vs 深度下跌是两种完全不同的估价场景。

## [2.6.0] - 2026-05-21

### Added
- **七维多维分析模块** (`multi_dim_analysis.py`)
  - 基本面 / 估值面 / 情绪面 / 资金面 / 题材面 / 风险事件 / 技术面
  - 加权综合评分模型（基本面×2、资金面×2、风险×1.5）
  - 评分越高 = 越看多，越低 = 越看空
- **业绩质量深挖模块** (`business_quality.py`)
  - 区分 “结构性亏损” vs “战略性亏损”
  - 重点识别在手订单 + 顽级客户（英伟达/台积电/英特尔/博通等）
  - 切换期公司（旧业务衰退+新业务上升）有独立判断逻辑
- **解禁等未来事件检测**（v2.4 遗哪的重要修复）
  - “解禁”升级为 HIGH 级关键词
  - HIGH 级支持双向时间窗口（过去 14 天 + 未来 30 天）
  - 从仅 4 个查询词扩充到 6 个（含 “限售股 上市”、“可流通”）
  - 新增 `_is_within_days_v26` 函数

### Improved
- SKILL.md 加入七维分析说明、评分逻辑、实战教训
- 智能参考理论与实际结合：单一维度看空≠减仓，需多维度一致才行动

### Lessons Learned (重要)

> **实战教训 1: 太岳先进 5/6 减持 case**
> - 原版本仅看“减持公告”单一信息→减仓建议
> - 实际股价从 110 涨到 180（+60%）
> - **原因**：未识别资金面重仓与题材主升共振
>
> **实战教训 2: 罗博特科 5/25 解禁漏报**
> - 原版本“解禁”仅 MED 级 + 仅看过去 14 天
> - 5/25 未来解禁事件被漏报
> - **修复**：解禁升 HIGH + 双向时间窗口
>
> **实战教训 3: 罗博业绩亏损 case**
> - 原版本看到亏损→看空
> - 实际：战略性转型 + 11 亿在手订单 + AI 头部客户→优质切换期公司
> - **修复**：业绩深挖区分亏损原因 + 订单与客户质量快速加分

### Backwards Compatibility
- 完全兼容 v2.4 的接口
- 新增函数不影响原有调用者
- 20/20 tests pass

## [2.4.0] - 2026-05-11

### Added
- **TinyFish Search 集成**：公告检测主源升级到 TinyFish Web Search API
  - 中文源准确率大幅提升（雪球/知乎/东财/新浪财经都可达）
  - 能跨 Cloudflare/反爬护栏（雪球这些站点以前 gsk 抓不到）
  - gsk web_search 作为兜底仍可用
- 环境变量 `TINYFISH_API_KEY` （或 `~/.openclaw/secrets/tinyfish.env`）

### Fixed
- **严格时效过滤（重要）**
  - 之前：TinyFish 不返回原生日期 → HIGH 级公告被默认当作“近期”接受
  - 后果：2-4 月的旧减持公告被错误报警 (如罗博特科多条减持)
  - 修复：从 snippet/URL/title 提取真实日期
    - `公告日期：XXXX-XX-XX`
    - 东财公告号 `AN20260414XXXXX` （前 8 位是日期）
    - `X月Y日` （按当前年推断）
  - 无日期一律跳过、防止老公告混入
- 实测效果：同一持仓 24 条 → 3 条（准确率大幅提升）

### Why this matters
> 之前版本会报警罗博特科 6 条减持公告，
> 但都是 2-4 月的旧公告（早被市场完全 price-in）
> v2.4 修复后：只保留真正在 14 天内的新公告。
> 这避免了“看到 6 条减持”就错误减仓的决策错误。

## [2.3.0] - 2026-05-08

### Added
- 🔮 **“好公司 ≠ 好股票” 核心心智**（SKILL.md § 8）
  - 4 象限分类（多头股/机会成本贼/炒作股/远离股）
  - “机会成本贼” 检查清单（5 个诊断信号）
  - EV (Expected Value) 评估公式
  - 词语表达规范 + 反模式补充
- 📝 实战案例：特变电工 600089（2026-05-08）

### Why
“好公司” 不等于 “好股票”，推荐出手时要换位思考：
- 业绩 × 趋势 是两个独立质量轴
- 亲机会成本，不要只看价格质量

### Added (docs & marketing)
- Three-mode output screenshots in `docs/images/`
- Demo GIF showing single + multi mode usage
- `docs/blog_post.md` — open-source story for cross-posting
- `docs/promo_templates.md` — pre-written templates for Reddit/V2EX/雪球/Twitter
- Codecov badge & GitHub Actions integration
- Visible badges row in README (License/Python/Market/OpenClaw/Tests/Codecov)

### Planned
- Sector comparison mode (auto-detect CPO / Semiconductor / New Energy sectors)
- Historical backtest module (validate stop-loss rules)
- HK & US market support
- Web Dashboard

## [2.2.0] - 2026-05-06

### Added
- 🆕 **Announcement detection module** (`announcements.py`)
  - Auto-pulls recent 14-day announcements via gsk web_search
  - Recognizes HIGH (减持/立案/业绩预减) and MED (解禁/收购/重组) severity
  - Pinned at top of portfolio briefing output
- 🆕 **Profit lock level** in stop-loss algorithm — prevents risk line from being stuck at irrelevant levels for profitable positions
- 🆕 **Risk-based ranking** for portfolio holdings (loss × margin × MA20 break × heavy weight)
- 🆕 **Margin coverage ratio** auto-calculation with 5-level alerting
- 🆕 **Operation priority labels** (P0/P1/P2) on action lists

### Fixed
- Profit % display bug (template variable misalignment)
- Multi-account holdings of same symbol now correctly merged (weighted average cost)
- Stop-loss line for profitable heavy positions (was using cost-15%, now uses MA20)
- Default portfolio path resolution (now: arg > env > cwd)

### Changed
- Default data source priority: Tencent → Sina → AKShare (was AKShare-first)
- AKShare timeout reduced to 15s (was unlimited)

## [2.0.0] - 2026-04-29

### Added
- 🆕 **Three-mode architecture**: Portfolio (P) / Single (S) / Multi (M)
- 🆕 Auto mode detection based on input
- 🆕 Tencent daily-K backup data source
- 🆕 Multi-stock comparison with composite scoring
- 🆕 Single-stock deep-dive with 5 operational levels

### Changed
- Renamed from `premarket-position-brief` to `stock-realtime-brief`
- Expanded scope from "portfolio only" to "any A-share input"

## [1.0.0] - 2026-04-21

### Added
- Initial release as `premarket-position-brief`
- Portfolio-only mode
- 7-step methodology
- Three-tier hard stop loss (Warning / Risk / Cut)
- Position adjustment factors (heavy / margin / loss)
- Tencent + Sina + AKShare data fetcher

[Unreleased]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.2.0...HEAD
[2.9.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.8.0...v2.9.0
[2.8.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.7.0...v2.8.0
[2.7.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.6.0...v2.7.0
[2.6.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.4.0...v2.6.0
[2.4.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.0.0...v2.2.0
[2.0.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Michaelliugh/stock-realtime-brief/releases/tag/v1.0.0
