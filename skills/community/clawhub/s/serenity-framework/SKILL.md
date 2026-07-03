---
name: serenity-framework
name_zh: 白毛股神的供应链瓶颈分析框架
description: "Analyze any stock using Serenity's supply-chain bottleneck investment framework. 5-layer pyramid (macro→bottleneck→company→position→execution). Based on 3,704 tweet full analysis. Updated with Grok summary and internet connectivity."
description_zh: "使用白毛股神（Serenity）的供应链瓶颈投资框架分析任意股票、板块或行业。五层金字塔框架（宏观→瓶颈→公司→仓位→执行）。基于 3,704 条推文全量分析训练数据。已整合 Grok 综合总结并新增联网分析功能。"
version: 2.1.0
tags: serenity-framework,bottleneck-analysis,position-sizing,semiconductor,investment-framework,supply-chain,risk-management,stock-analysis,trading-strategy,ai-hardware,five-factor-model,signal-radar,stop-thesis,chinese-kol,day-trading,online-analysis,osint
homepage: https://github.com/kooui/serenity-framework
agent_created: true
---

# 白毛股神的供应链瓶颈分析框架 / Serenity Investment Framework Skill

## English

Analyze any stock, sector, or industry using the supply-chain bottleneck methodology developed by @aleabitoreddit (白毛股神 / Serenity), a professional day trader specializing in semiconductor supply-chain analysis. Based on full analysis of 3,704 tweets (2025-07-02 ~ 2026-06-25) + Grok comprehensive summary.

### Core Framework (5-Layer Pyramid)

```
Layer1: Macro Capex Guidance (demand ceiling)
Layer2: Bottleneck Identification (supply constraint)
Layer3: Company Screening (who captures profit)
Layer4: Position Sizing (Core / Swing / Lottery)
Layer5: Execution (day trading around core positions)
```

### Usage

When user asks to:
- "Analyze $XXX using 白毛股神's framework"
- "What's the supply chain bottleneck for $XXX?"
- "Evaluate my investment thesis for $XXX"
- "Help me size my position in $XXX"
- "Apply stop-thesis to my $XXX holding"
- "Analyze [sector/industry] using Serenity framework"
- "用 Serenity 框架分析 [股票/板块/行业]"

### Output Format

The skill produces a structured analysis report:
1. **Macro Demand** — Hyperscaler Capex, government policy
2. **Bottleneck Map** — supply chain diagram, narrowest link
3. **Company Screening** — Tier1/2/Speculative, SWOT
4. **Position Sizing** — recommended % allocation, stop-thesis level
5. **Risk Factors** — key risks, redemption conditions
6. **Online Data Verification** — real-time data cross-check (NEW in v2.1)

---

## 中文说明

本技能使用白毛股神（Serenity，X.com @aleabitoreddit）开发的供应链瓶颈投资方法论来分析任意股票、板块或行业。
白毛股神是专注于半导体供应链分析的职业日内交易员，其框架在美股半导体板块有显著实战记录。

### 核心框架（五层金字塔）

```
第一层：宏观资本开支指引（需求上限）
第二层：瓶颈识别（供给侧约束）
第三层：公司筛选（谁捕获利润）
第四层：仓位管理（核心仓 / 摆动仓 / 彩票仓）
第五层：执行（围绕核心仓做日内交易）
```

### 使用场景

当用户提出以下需求时触发：
- "用 Serenity 框架分析 $XXX"
- "$XXX 的供应链瓶颈在哪里？"
- "帮我评估 $XXX 的投资逻辑"
- "我应该给 $XXX 分配多少仓位？"
- "对 $XXX 应用 stop-thesis 规则"
- "分析 [板块/行业] 的供应链瓶颈"
- "用白毛股神的方法分析 [股票/板块/行业]"

### 输出格式

本技能生成结构化分析报告，包含：
1. **宏观需求** — 超大规模数据中心资本开支、政府政策
2. **瓶颈地图** — 供应链上下游图、最窄瓶颈环节
3. **公司筛选** — 一线/二线/投机级标的、SWOT 分析
4. **仓位建议** — 推荐仓位比例、stop-thesis 触发条件
5. **风险因素** — 关键风险、逻辑被破坏的赎回条件
6. **联网数据验证** — 实时数据交叉验证（v2.1 新增）

---

## v2.1 核心方法论升级（基于 3,704 条推文全量分析 + Grok 综合总结）

### 一、瓶颈理论的三阶推理框架

| 阶次 | 问题 | 判断标准 |
|------|------|----------|
| 第一阶 | 识别 AI 基础设施的物理瓶颈 | 哪个环节最窄？巨头绕不开哪个？ |
| 第二阶 | 定价权与不可替代性 | TAM 被市场低估多少？有定价权吗？会被替代吗？ |
| 第三阶 | 博弈论视角下的国家供应链安全 | 是否涉及国家安全？CHIPS ACT 是否指向该环节？ |

**第一阶判断依据：**
- "IMO photonics theme + CW laser chokepoint is goated."
- "If I see the entire AI industry bottlenecked by some $600m company worth less than a pre-revenue LLM startup, I'm long."（2025-12-26）

**第二阶判断依据：**
- "TAM for InP substrates was few hundred million previously since it was a niche telecom commodity. Most analysts model this wrong since it's not linear. It's a game theory supply bottleneck."（2026-01-08）

**第三阶判断依据：**
- "The Western AI buildout might be held at choke point by an obscure $700m company like $AXTI and $SMTOY."（2025-12-27）
- "US Chip ACT Funding is one of the largest signals for importance to America National Security."（2026-03-24）

---

### 二、紫苏叶（Shiso Leaf）反推 Checklist

Serenity 将选股逻辑比作找到寿司中那片紫苏叶——不是主角（鱼生），但少了它整道菜就散了。反向推导的 6 步 Checklist：

| 步骤 | 问题 | 验证方法 |
|------|------|----------|
| 1 | 这个 AI 架构里最窄的脖子在哪？ | 技术架构分析 + 供应链图谱 |
| 2 | 这个瓶颈的 TAM 市场认为多少？实际应该是多少？ | 对比分析师预期 vs 实际需求 |
| 3 | 这个瓶颈有定价权吗？ | 检查是否涨价、lead time 是否拉长 |
| 4 | 这个瓶颈会被替代吗？ | 技术路线图分析（替代时间线 > 2 年可接受）|
| 5 | 市场给什么估值？正确估值应该是多少？ | 参考可对标标的（$LITE $3B → $65B+）|
| 6 | 有多少人知道这个逻辑？（信息不对称度） | 机构覆盖数、分析师评级 |

---

### 三、主动避开清单

- **不买 NVDA**：4T+ 市值上涨空间有限，不如买其上游
- **不买无定价权的组装厂**："I personally wouldn't go downstream into assembly and others."（2026-04-02）
- **不买单客户依赖**："this is why I don't like companies with single customer concentration risk"
- **不买低质量上市公司**："As for thesis on Blacksky ($BKSY) honestly, pretty terrible company."（2025-07-03）

---

### 四、信息源层级（优先级排序）← v2.1 更新

| 层级 | 来源 | 权重 | 说明 |
|------|------|------|------|
| 第一层 | 技术架构预判 | 35% | 前 AI 算法 / RISC-V 背景，预判技术演进 |
| 第二层 | OSINT 供应链追踪 | 25% | BOM 分析、产能跟踪、客户映射、foundry 关系 |
| 第三层 | 政策信号 | 15% | CHIPS ACT、国防生产法、出口管制 |
| 第四层 | 公开财报/管理层谈话 | 15% | CEO 关于"massive supply demand imbalance"言论 |
| 第五层 | 行业数据与第三方报告 | 10% | a16z 数据、pitchbook、SMM 价格、Gov publications |

**v2.1 新增：具体数据源清单**

Serenity 使用以下 OSINT 数据源进行供应链映射：

1. **公司财报与 transcript**：10-K、10-Q、季度电话会议记录
2. **a16z / pitchbook 数据**：私募与创投数据，用于评估未上市竞争对手
3. **SMM 价格**：上海金属网价格，追踪原材料成本
4. **政府出版物**：出口管制清单、CHIPS ACT 拨款记录
5. **Hyperscaler 采购记录**：公开合同、产能预订数据
6. **产能数据**：foundry 产能利用率、lead time 追踪
7. **地缘新闻**：出口管制、国家安全指定

---

### 五、研究方法论：Red-team/Blue-team 对抗测试 ← v2.1 新增

Serenity 在发布分析前，会进行内部自我辩论，挑战自身 thesis。这一方法论确保其逻辑经得起反驳。

**Red-team/Blue-team 流程：**

| 步骤 | 内容 | 目的 |
|------|------|------|
| Red Team | 主动寻找反方论据 | 挑战自身 thesis 的弱点 |
| Blue Team | 强化自身 thesis | 确认核心论点的稳健性 |
| 合并 | 综合两方论据 | 形成更平衡的判断 |

**典型表达（inferred from tweet patterns）：**
- "I challenge this view because..."（主动反驳）
- "could be wrong"（承认错误可能性）
- 会接受质疑并公开修正观点

这一方法论解释了为什么 Serenity 的 thesis 往往经得起时间验证——它们在发布前已经过内部压力测试。

---

### 六、仓位管理量化规则（inferred from tweet patterns）← v2.1 更新

| 规则 | 描述 | 备注 |
|------|------|------|
| 分散化重仓 | 同时持有 10+ 只股票，但前 5 持仓占比 >80% | |
| 平均成本法（DCA） | 首次建仓后 2 周内可加码 1-2 次 | |
| 期权运用 | LEAPS 和短线 call 结合，控制资金效率 | |
| 回撤容忍度 | 单票回撤容忍 >50%，组合整体 <20%。基本面未变时 -30% 不动，-50% 加仓 | |
| Margin 使用 | 战略使用 margin（约 1.4x），但警告过度杠杆 | "if you use margin I wouldn't recommend more than 1.4x" |
| 退出条件 | 基本面恶化 / 技术路线被废弃 / 定价权消失 | |

**v2.1 新增：Margin 使用细节**

Serenity 使用 margin 放大收益，但非常谨慎：
- 推荐 margin 上限：~1.4x（根据综合分析与推文模式）
- 警告：不要在波动大时使用过度杠杆
- 经验：多次提到"margin call"风险，强调风险管理
- 实际用法：在 high conviction 标的上使用，且有明确 exit plan

**典型案例：$NBIS**
- 2025-09-09："bought $100k worth of $NBIS"
- 2025-09-19："scaling my $NBIS position to $1M+"
- 跨度 9 个月持续看多，2026-06-12 纳入 Nasdaq 100

---

### 七、Serenity 信号雷达规则 v1（完整版）

#### 信号层次

```
                                  ┌─────────────────────────┐
                                  │    Tier 1: 架构级信号    │ ← 权重 40%
                                  │  (技术架构切换预判)     │
                                  └──────────┬──────────────┘
                                             │
                                  ┌──────────▼──────────────┐
                                  │    Tier 2: 供需失衡信号  │ ← 权重 30%
                                  │  (产能缺口/涨价/Lead    │
                                  │   Time恶化)             │
                                  └──────────┬──────────────┘
                                             │
                    ┌────────────────────────┼──────────────────┐
                    │                        │                  │
          ┌─────────▼──────────┐   ┌─────────▼─────────┐  ┌───▼───────────┐
          │ Tier 3a: 情绪信号 │   │ Tier 3b: 政策信号 │  │ Tier 3c: 关联│ ← 各 10%
          │ (逆向/反WSB)      │   │ (CHIPS/出口管制)  │  │ 信号(对标)  │
          └───────────────────┘   └───────────────────┘  └───────────────┘
```

#### Tier 1：架构级信号（权重 40%）

| 触发条件 | 行动 | 案例 |
|----------|------|------|
| 主流技术被颠覆，新技术路径初步成熟 | 重仓配置新技术上游 | 铜互连→光通信；EML→CPO |
| 技术路线获龙头厂商背书 | 确认后加仓 | $AMD CPO + $GFS 认证（2026-05）|
| CEO 公开表态"massive supply demand imbalance" | 立即进入 | $LITE CEO（2026-05-05）|

#### Tier 2：供需失衡信号（权重 30%）

| 触发条件 | 行动 | 案例 |
|----------|------|------|
| 产业链出现涨价通知 | 对应标的重仓 | VPEC 磊晶圆涨价（2026-06-12）|
| Lead Time 超过 6 个月 | 关注 | 变压器 lead time（2025-12-17）|
| 龙头厂商锁定上游产能 | 加速建仓 | $MTSI 投资 IQE（2026-06-12）|
| 单一供应商全球市占率 >60% | 视为关键节点 | MSSCORP 90% 市占率（2026-05）|

#### Tier 3a：情绪逆向信号（权重 10%）

| 触发条件 | 行动 | 案例 |
|----------|------|------|
| WSB Reddit 开始讨论 | 警惕 | $NBIS 出现在 WSB（2025-10-22）|
| 主流媒体/投行集体唱空 | 考虑做多 | BofA KOSPI 唱空 |
| 分析师升级 | 视为延迟确认 | $XFAB 被 Bernstein 升级 |

#### Tier 3b：政策/地缘信号（权重 10%）

| 触发条件 | 行动 | 案例 |
|----------|------|------|
| CHIPS ACT 拨款给特定公司 | 强力看多 | $SIVE $330M（2026-03-24）|
| 国防生产法引用 | 立刻配置 | 变压器/开关设备（2026-04-24）|
| 中国出口管制涉及新材料 | 寻找替代受益标的 | 钨出口→Foosung（2026-06-15）|

#### 操作规则

```
1. Tier 1 + 任一 Tier 2 = 重仓建仓（仓位 >10%）
2. Tier 2 × 2 = 中型仓位（仓位 5-10%）
3. 单独 Tier 3 = 研究观察仓（仓位 <2%）
4. Tier 1 × 0 + Tier 2 × 0 + 任何 Tier 3 = 暂时放弃
5. 同产业链出现 3+ 个信号 = 全链配置
6. 中文社区热度上升 = 信号延迟确认（不是买入理由）
```

---

### 八、案例研究 ← v2.1 更新

#### $AAOI（成功案例）

$28 → $195（33 条推文，2026年3月→6月）：

```
2026-03-15 @ $28: "Only US optical module company benefiting from CHIPS Act"
2026-04-20 @ $45: "Confirmed in Top-3 hyperscaler sample validation"
2026-05-10 @ $120: "Raised target: 3x revenue in 18 months if 2+ cloud contracts"
2026-06-15 @ $195: "Trimmed 8% → 3%, up 357%, locking profit"
```

关键：不设价格目标，设 **thesis 验证检查点**。

#### $RPI (Raspberry Pi) ← v2.1 新增

小市值、AI/机器人相关需求爆发。Serenity 预测营收增长远超分析师（55% vs 14%），实际 58%。推文后股价单日大涨，后续分析师上调预测。

**关键信息（根据推文与综合分析）：**
- Serenity 预测营收增长：55%
- 分析师一致预期：14%
- 实际营收增长：58%
- 结果：股价单日大涨，分析师上调预测
- 推文提及：多次出现在推文中，作为小市值 AI 受益标的案例

#### $AXTI（成功案例）

InP 衬底供应链映射、分析师数据、高纯铟价格、出口管制等，发现瓶颈。早期推荐时遭质疑，后 Reuters 验证相关短缺，股价从低位大幅上涨。

**关键数据：**
- 早期目标：~$15（2025 年末）
- 2026-05-26：股价达到 $82（从 $12 起）
- 推文确认：精确命中

#### $NBIS（成功案例）

2025-09-19 PT $225，2026-06-12 纳入 Nasdaq 100。趋势验证。

**其他命中记录：**
| 标的 | 时间 | 表现 |
|------|------|------|
| $NBIS | 2025-09-19 PT $225 | 2026-06-12 纳入 Nasdaq 100 |
| $AXTI | 2025 年末 ~$15 → 2026-05 $82 | 精确命中 |
| $LITE | $3B → $65B+ | 对标案例已确认 |

#### 失败案例与风险控制 ← v2.1 新增

**公开讨论的回撤案例：**
- $SIVE 短期被"murdered"（回撤 >50%），仍持百万股等待 volume ramp
- $AAOI 和其他 CPO 相关标的经历大幅回撤
- 应对策略：持有等待验证，不在意短期噪声/5-20% 波动

**风险管理原则：**
- 承认波动与回撤："not doing so well" 但强调长期 conviction
- 避免追高，专注未定价机会
- 常说"could be wrong"，鼓励独立研究
- 未见频繁止损记录，风格偏长期持有 thesis 而非短线交易

---

### 九、Stop-Thesis 规则（核心风险管理）

> "我不使用止损单。我使用 stop-thesis。如果供应链瓶颈 thesis 被破坏，我退出。" — 白毛股神

| Condition | Action |
|-----------|--------|
| Customer demand disappears (e.g., hyperscaler cuts Capex) | Exit full position |
| Valuation extreme (P/E > 2x peer) | Trim 50% |
| Macro reversal (Fed hikes, China export ban) | Trim 30% |
| Technology leapfrogs bottleneck | Exit |

---

### 十、语气与叙事风格指南

#### 英文长线程标准结构

| 步骤 | 内容 | 占比 |
|------|------|------|
| Hook | 短评 + $TICKER + 反直觉断言 | 必选 |
| 论点展开 | 历史对标 + 技术解释 | 必选 |
| 证据链 | BOM 分析、财报引用、政策文件 | 必选 |
| 信念声明 | 个人操作 + 仓位披露 | 必选 |
| 免责（NFA） | 标准化 disclaimer | 可选 |

**风格标签统计（3,704 条推文）：**
- technical_dense: 93.7%
- sarcastic: 4.4%（针对主流媒体/投行）
- self_deprecating: 1.6%（自嘲撇清）
- disclaimer: 0.3%

#### 中文人格 vs 英文人格

| 维度 | 英文 | 中文 |
|------|------|------|
| 语气 | 自信/技术性/偶尔刻薄 | 谦逊/亲昵/感恩 |
| 选题 | 全球 AI 供应链 | A 股 + 全球话题总结 |
| 深度 | thread 全链条逻辑 | 总结性、要点式 |
| 用语 | "I am confident" | "大家喜欢就好"、"拜托我也就是个普通人好吗" |

中文推文使用"啦、哦、嘛"等语气词，接受"白毛股神"称号但自嘲否认。

---

### 十一、方法论演进轨迹

| 阶段 | 时间 | 核心持仓 | 方法论特征 |
|------|------|----------|------------|
| 早期 | 2025Q3 | $UPWK、$ALAB、$GME | 价值修复 + WSB 风格散户策略 |
| 中期 | 2025Q4 | $NBIS、$IREN、$CIFR | Neocloud 聚焦 + 瓶颈理论雏形 |
| 成熟期 | 2026H1 | $SIVE、$AAOI、$AXTI、$LITE | 完整瓶颈理论，全产业链矩阵 |

---

### 十二、高频核心标的 Top 10

| 排名 | Ticker | 提及次数 | 产业链环节 |
|------|--------|----------|------------|
| 1 | $NBIS | 472 | Neocloud / AI Infrastructure |
| 2 | $SIVE | 366 | CW Laser / Photonics Chokepoint |
| 3 | $IREN | 249 | Neocloud / BTC Mining |
| 4 | $LITE | 169 | Photonics / CPO |
| 5 | $AAOI | 160 | Optical Transceiver |
| 6 | $NVDA | 157 | AI Chip（作为参照物，不买）|
| 7 | $AXTI | 151 | InP Substrate |
| 8 | $MRVL | 96 | Semiconductor |
| 9 | $MSFT | 95 | Hyperscaler |
| 10 | $CIFR | 91 | Neocloud |

---

### 十三、适合投资者类型与局限 ← v2.1 新增

#### 适合投资者类型

| 类型 | 匹配度 | 说明 |
|------|--------|------|
| 有较强研究能力的投资者 | ★★★ | 需要能够独立验证供应链逻辑 |
| 耐受高波动的投资者 | ★★★ | Serenity 的标的回撤可达 50%+ |
| 能长期持有的中高级投资者 | ★★ | 等待 thesis 验证需要时间（数月到数年）|
| 对 AI/半导体/供应链感兴趣者 | ★★★ | 核心覆盖领域 |
| 新手投资者 | ✗ | 不适合，波动大、需独立验证 |
| 风险厌恶者 | ✗ | 不适合，小盘、科技/地缘敏感 |
| 追求稳定/短期收益者 | ✗ | 不适合，波动大 |

#### 局限性

| 局限 | 说明 | 风险 |
|------|------|------|
| 依赖个人 OSINT 深度 | Serenity 的分析依赖其个人供应链映射能力 | 普通投资者难以复制 |
| 公开后易被跟风/噪声影响 | 高关注度可能导致标的被过度买入 | 买点变差、波动加剧 |
| 地缘/政策风险高 | 聚焦供应链瓶颈，往往涉及出口管制、国家安全 | 政策突变可能导致 thesis 被破坏 |
| 过去表现不代表未来 | 历史命中率高，但不保证未来同样准确 | 需要持续验证 |
| 小盘股流动性风险 | 偏好小市值公司（10-20 亿美元）| 大资金难以建仓/退出 |

---

### 十四、联网分析功能 ← v2.1 新增

本 skill 支持联网分析任意股票、板块或行业。当用户请求分析未在前 10 大持仓中出现的标的时，自动触发联网数据获取。

#### 联网分析工作流程

```
用户请求 → 判断是否需要联网数据 → 获取实时数据 → 应用 Serenity 框架 → 生成分析报告
```

#### 步骤 1：判断是否需要联网数据

以下情况需要联网获取实时数据：
- 分析的标的不在 Serenity 高频持仓列表中
- 需要最新财报数据（>3 个月前）
- 需要最新政策/新闻（如出口管制更新）
- 用户明确要求"获取最新数据"或"联网分析"

#### 步骤 2：获取实时数据

使用以下工具获取实时数据（按优先级排序）：

**优先级 1：金融数据 API**
- `westock-data`：获取股票行情、财报、研报、新闻（推荐，数据最全）
- `iFinD-Finance-Data`：同花顺金融数据（A 股优选）
- `wb-finance-skill`：综合金融分析

**优先级 2：Web 搜索**
- `web-tools-mcp`：搜索行业报告、新闻、供应链信息
- 搜索关键词模板：
  - "[股票代码] supply chain bottleneck"
  - "[行业] AI capex 2026"
  - "[公司] CHIPS ACT funding"
  - "[原材料] price trend 2026"

**优先级 3：行业特定数据源**
- SMM 价格：https://www.smm.cn/（金属/原材料价格）
- a16z blog：https://a16z.com/（科技/AI 趋势）
- Pitchbook：https://pitchbook.com/（私募/创投数据）

#### 步骤 3：应用 Serenity 框架

将联网获取的数据输入 Serenity 五层金字塔框架：

1. **宏观需求**：使用最新 hyperscaler Capex 数据
2. **瓶颈地图**：使用最新供应链数据（foundry 产能、lead time）
3. **公司筛选**：使用最新财报数据（营收、毛利率、市占率）
4. **仓位建议**：基于实时波动率和流动性
5. **风险因素**：使用最新政策/地缘新闻

#### 步骤 4：生成分析报告

报告包含：
1. **框架分析**（五层金字塔）
2. **实时数据验证**（标注数据来源和时间）
3. **与 Serenity 持仓的对比**（如果适用）
4. **风险提示**（基于最新信息）

#### 联网分析示例

**示例 1：分析 $SMCI（不在 Serenity 高频列表中）**

```
用户："用 Serenity 框架分析 $SMCI"

工作流程：
1. 检测到 $SMCI 不在高频列表 → 触发联网
2. 获取 $SMCI 最新财报（westock-data）
3. 搜索"AI server supply chain bottleneck"（web-tools-mcp）
4. 应用框架：
   - 宏观：Hyperscaler Capex 增长 → 需求强
   - 瓶颈：$SMCI 是 AI 服务器组装厂，无定价权 → 不符合 Serenity 标准
   - 结论：不建议（组装厂，无瓶颈定价权）
```

**示例 2：分析 A 股"绿的谐波（688017）"**

```
用户："用 Serenity 框架分析绿的谐波"

工作流程：
1. 检测到 A 股标的 → 触发联网
2. 获取 688017 最新财报（westock-data 或 iFinD）
3. 搜索"谐波减速器 supply chain"（web-tools-mcp）
4. 应用框架：
   - 宏观：人形机器人需求增长 → 需求强
   - 瓶颈：谐波减速器国产替代瓶颈 → 符合
   - 公司：绿的谐波国内市占率 >60% → 一线
   - 结论：符合 Serenity 框架，推荐研究
```

#### 联网分析注意事项

1. **数据时效性**：标注所有数据的获取时间
2. **来源可靠性**：优先使用官方财报、政府公告
3. **供应链复杂性**：某些行业的供应链难以映射（如消费电子），需要更多研究
4. **地缘敏感性**：出口管制等政策变化快，需要最新信息
5. **A 股特殊性**：A 股供应链数据与美股不同，需要使用 iFinD 或 westock-data 的 A 股模块

---

## 参考资料

- **全量深度分析报告（3,704 条推文）**：`references/serenity_deep_analysis_report.md`
- 原始推文：https://x.com/aleabitoreddit
- 五因子模型 + 六步流程详解：`docs/methodology.md`
- Serenity 背景及人物画像：`docs/serenity_background.md`
- 框架哲学："供给约束创造定价权"
- **v2.1 新增：联网分析模板**：待创建 `references/online_analysis_template.md`

---

*Skill 版本：v2.1.0（2026-07-02）*
*基于 3,704 条推文 + Grok 综合总结 + 联网分析功能*
*更新内容：Red-team/Blue-team 方法论、信息源具体化、$RPI 案例、Margin 细节、投资者类型、局限性、联网分析功能*
