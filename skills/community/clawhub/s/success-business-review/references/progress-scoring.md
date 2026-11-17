# Progress Scoring（progress-scoring）

> 配套 SKILL.md 主线第二步「核进展证据判红黄绿」。采用 delivered-vs-promised + 5 可信度规则 + 证据 6 维元数据 + 健康度五维。

## 一、承诺逐条四态（层 1，不软化）

上轮 QBR 的每条承诺逐条标：

| 状态 | 含义 | 标注要求 |
|---|---|---|
| delivered | 兑现 | 标证据 source+as-of |
| partial | 部分兑现 | **标缺口量+缺口原因** |
| not delivered | 未兑现 | **我方原因认我方原因**（不全推客户依赖）；标补救计划 |
| descoped by agreement | 双方同意调范围 | 标调整时间+双方确认证据 |

**铁律**：
- 坏季度就写坏季度（客户 lived it，读了「delivered」会失去所有信任，续约烧、转介绍烧）。
- 不软化 not delivered 为 partial（partial 必须有明确缺口量，不是模糊「基本达成」）。
- 我方原因不认、全推客户依赖 → 客户反感甩锅，关系破裂。

## 二、Success Definition 三档（层 2，整体判定）

| 档 | 信号 | 判定 | 后续 |
|---|---|---|---|
| on_track（绿） | 关键价值指标达 baseline→target 进度 ≥70% | 绿 | 正常埋续约/增购/转介绍钩子 |
| at_risk（黄） | 进度 30-70% 或有阻塞 | 黄 | 救计划优先，**不埋 expansion**，记原因 |
| not_measurable_yet | 早期无法量度 | 早期诚实 | **第 3 次复盘仍是 = 测量问题，升红** |

**not_measurable_yet 规则**：早期（前 2 次复盘）诚实标注 not_measurable_yet 可接受；第 3 次复盘仍是 = success definition 形同虚设，升红，需重新定义指标或补建基线。

## 三、5 可信度规则（防被决策层戳穿）

1. **坏季度就写坏季度**：客户 lived it，读了「delivered」会失去所有信任。
2. **不编造结果**（Proof Gate）：无 source 无 number，每数字可溯源到 proof record 或客户侧系统。
3. **outputs ≠ outcomes**：「shipped 14 deliverables」「培训 200 人」是 activity/outputs；success definition 是 outcome（审批时长降 X%、合规事件降 Y%）。outcome 未量度时用 not_measurable_yet，不拿 activity 替代。
4. **我方原因就认我方原因**：不全推客户依赖，透明+负责。
5. **not_measurable_yet 早期诚实晚期 evasive**：第 3 次 = 测量问题升红。

## 四、证据 6 维元数据（每条证据必带）

证据 reconcile 法：

| 维 | 含义 | 例 |
|---|---|---|
| source | 数据来源 | 业务侧手动统计 / 私有化后台 / 微信截图 / 客户系统 |
| as-of | 数据截止日 | 2026-08-15 |
| baseline | 上线前快照值 | 5.2 小时 |
| current | 当前值 | 3.0 小时 |
| confidence | 5 级可信度 | customer-confirmed / customer-validated / data-derived / estimated / assumed（禁用） |
| attribution | 归因状态 + alternative explanations + 客户是否接受 | 产品+客户配合；无替代解释；客户分管副总微信认可 |

**证据 5 级可信度**（沿用首价值证明五级法）：
- customer-confirmed（最高）：客户原话「这工具帮我们每周省 10 小时」。
- customer-validated：我方估算+客户点头。
- data-derived：基于使用量×单次节省推算。
- estimated：基于行业基准估算。
- assumed（禁用）：「我们觉得有价值」。

**估算必须标 estimated，不准当 confirmed 报。**

## 五、健康度五维 Green/Yellow/Red（内部用）

健康度指标五维。**内部用，客户面用「目标达成度」红黄绿，不打分给客户看**：

| 维 | Green | Yellow | Red |
|---|---|---|---|
| 决策层出席率 | 决策层出席 | 委派代表 | 缺席/改期 2 次以上 |
| 客户会前准备 | 提供本季数据/问题 | 基本准备 | 无准备 |
| 会上参与度 | 主动讨论 | 礼貌听讲 | 走神/早退 |
| 会后跟进响应率 | 当日响应 | 一周内 | 无响应 |
| 上轮 action 完成率 | ≥80% | 50-80% | <50% |

**综合健康度**：5 维任一 Red → 整体至少 Yellow；2 维以上 Red → 整体 Red。

**客户面表述**：用「目标达成度」红黄绿（绿=on_track / 黄=at_risk / 红=not_measurable_yet 第 3 次），不说「health score」。

## 六、无 Telemetry 替代证据（中国私有化/国产化）

私有化部署无完整 telemetry 时：

| 证据类型 | 海外做法 | 中国替代 |
|---|---|---|
| 使用数据 | 后台 telemetry 自动 | 业务侧手动统计（审批时长/工单数/人天/合规事件数）+ 私有化后台部分活跃数据 |
| 业务结果 | BI 自动拉 | 客户侧业务负责人提供报表+我方推算+客户确认 |
| 客户原话 | email/NPS | 微信/企微群聊截图 + 朋友圈 + 客户领导微信群认可截图 |

**客户确认的基线/数据比我方估算可信 10×**。优先拉客户侧业务负责人提供数据。
