---
name: stock-research-team
description: 股票分析技能（v4 简化版）。主 agent 单 agent 快速模式：westock-data 采集数据 + minimax__web_search 实时资讯（含🛡️ 监管/处罚/政策 hard rule）+ 综合建议。覆盖 A 股 / 港股 / 美股。Fork of `stock-research-team` (charonling, 1.0.0) 并大幅简化——不再支持多 agent 流水线。
---

# Stock Research Team（v4 简化版）

> 这是 `stock-research-team` (clawhub charonling 1.0.0 多 agent 流水线版本) 的**简化重写 fork**。本版本**只保留默认模式**，不再支持 5-subagent 多视角流水线。理由记录在 `references/changelog.md`。

## 默认模式：主 agent 单跑（simple mode）

**触发本 skill 后，默认由主 agent 自己跑完**，不 spawn subagent、不分多视角、不做多空辩论。流程只有三步：

1. 调 `westock-data` skill 采集：行情 + 技术指标 + 财报 + 资金流向 + 公司简况
2. 调 `minimax__web_search` 抓最近 1 周的关键新闻 / 舆情 / 业绩快报
3. **🛡️ 强制检索：监管 / 处罚 / 政策（hard rule）**——不能跳过，详见下文
4. 主 agent 自己综合输出：**结论 + 关键位（支撑/压力）+ 风险清单 + 操作建议**

输出直接给用户，**不长篇大论**，抓住决策点即可。

## 🛡️ 强制检索：监管 / 处罚 / 政策（hard rule）

**无论标的复杂与否，第 2 步 web search 必跑这一轮专项检索，不能跳过。**

执行步骤（3 次并行搜索）：

```
1. <标的中文名或简称> 罚款 处罚 立案 调查
2. <标的中文名> 反垄断 监管 政策（适用：平台 / 互联网 / 金融）
3. <公司英文名> fine penalty regulatory enforcement investigation
```

**判定规则**：

| 检索结果 | 后续动作 |
|---|---|
| 无负面新闻 | 标记「✅ 监管/处罚：近 30 天无重大事件」，参与下一步评级 |
| 罚款 / 处罚 ≤ 净利润 5% | 列入「风险」段，**评级不下调** |
| 罚款 / 处罚 占净利润 5-15% | 列入「风险」顶部 + 评级降一档 + 一次性计提提示 |
| 罚款 / 处罚 > 净利润 15% 或首例效应 | 列入「风险」顶部 + **评级降至「持有」或以下** + 等中报定调 |
| 立案调查尚未落地 | 列入「风险」顶部 + 评级保守一档 + 注明可能罚款区间 |

**真实反例（real example，2026-07-27）**：

> 携程 09961.HK 复盘时主 agent 默认只跑业绩 + 新闻，漏掉 7/25 国家市监总局反垄断罚单 51.79 亿（占净利润 15%）。给出「买入 8-12%」评级后被用户指出「结合罚款消息」，重新下调至「谨慎买入 5-8%」。**如果一开始就走这条 hard rule，评级会一步到位给到「谨慎买入」，无需返工。**

**写入位置**：强制检索结果必须出现在输出的「风险」段**最顶部**（在「核心论点」之后立即出现）。

## 默认模式输出模板

```markdown
## <标的> <代码>.<市场> 复盘

**当前价 / 涨跌：** ...
**评级：** 强烈买入 / 买入 / 持有 / 卖出 / 强烈卖出
**操作建议：** <仓位> <入场区间> <止损> <目标价>
**关键位：** 支撑 ... / 压力 ...
**核心论点（3 条以内）：**
- ...
- ...
- ...
**风险：**
🛡️ **监管事件（近 30 天）：** ✅ 无重大事件 / <存在 X 事件>（说明 + 财务影响 + 评级反应）
- 其他风险 1：...
- 其他风险 2：...
```

## 评级体系

详见 `references/rating-criteria.md`（五级评级门槛 + 操作建议规范）。

货币单位 / 市场专属规则详见 `references/market-rules.md`。

## 三市场差异化提示

- **A 股**：人民币（¥），交易时间 09:30-11:30 / 13:00-15:00，关注龙虎榜 / 融资融券 / 业绩预告
- **港股**：港元（HK$），交易时间 09:30-12:00 / 13:00-16:00，**禁止使用人民币符号**
- **美股**：美元（$），盘前 / 盘中 / 盘后，关注卖空数据 / SEC 文件

## 安装 / 使用

```bash
# clawhub
clawhub install tanteng-stock-research
# or
openclaw skills install tanteng-stock-research
```

## Resources

### references/

- `market-rules.md` — 三市场货币单位 / 交易时间 / 数据源
- `rating-criteria.md` — 五级评级判定门槛与操作建议规范
- `changelog.md` — 版本演进记录（v1 → v4 + 与原版差异）

## 版本

- **v4.0.0 (2026-07-27)**：移除多 agent 5-subagent 流水线，只保留默认模式。继承自 `stock-research-team` (charonling, clawhub 1.0.0)。
- v3.x：默认 + 多 agent opt-in（已废弃分支）
- v1-v2：纯多 agent 流水线（v3.x 已废弃）
