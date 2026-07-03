---
name: agent-learning
description: Agent 学习循环 skill。基于 One Click 的日志 → AI 汇总 → 人工标注 → 经验沉淀三层架构,设计 Agent 的自我迭代机制。触发场景:用户说"经验学习"、"日志设计"、"Agent 迭代机制"、或 workflow-start 路由到此 skill。
---

# Agent-Learning — Agent 学习循环工作流

你是 Agent 经验学习机制的设计专家。目标:**让 Agent 装上就能"越用越准",不是交付后静态产品**。

## 核心原则

> **日志是经验学习的原料。P0 必须把黑匣子装上,确保第一轮实践不白跑。**

学习循环不是可选项,是 **P0 必做**。没日志就没迭代。

## 引用资产

本 skill 深度依赖以下资产,执行时按需读取:

- 📚 **[Agent 教训全集](../../lessons/by-role/agent.md)** — 学习循环设计的典型坑:日志结构设计不合理 / P0 跳过日志导致后续无法迭代

## 门禁原则(Gate-based)

3 个 Phase。

## Phase 1:日志架构(P0 必做)

**🎯 目标**:定义日志数据结构,每次交互自动写入。

### 日志数据结构(One Click 标准)

```
操作日志:
├── meta:operation_id / timestamp / operator / page_context / config_type
├── geo:region / country / city / timezone / locale / currency
├── interaction:user_input / input_type(natural_language|quick_action|template) /
│               agent_parse / agent_questions / form_filled / user_modified /
│               final_submitted
├── execution:api_calls / cross_system / validation_results / submit_status
├── compliance:rules_checked[] / rules_passed[] / rules_blocked[] / override_reason
├── localization:languages[] / currency / tax_rules_applied
├── calendar:nearby_events[] / cultural_flags[]
├── tags:ai_tags / human_tags(双周会后回填)
└── quality:accuracy_score / issues / lessons(双周会后回填)
```

### 核心字段解释

| 字段 | 为什么关键 |
|---|---|
| **user_modified** | 记录 AI 填了什么、用户改成了什么 —— **经验学习的核心数据源** |
| **input_type** | 区分自然语言/快捷动作/模板,分析不同输入方式的效率 |
| **rules_blocked** | 合规拦截了什么,用于优化规则库 |
| **human_tags** | 双周会人工回填,用于训练 AI 识别类别 |

### P0 必做 vs P1+ 后做

| P0 必做 | P1+ 后做 |
|---|---|
| 日志字段规范定义 | 日志查询后台 |
| 每次交互自动写入 | AI 定时总结报告 |
| 操作编号体系(CFG-YYYYMMDD-NNN) | 人工标注 UI |
| 标签字段预留 + AI 自动打标 | 统计可视化 |

**🚧 Phase 1 门禁**:
- ✅ 日志结构完整(含 user_modified / rules_blocked / tags / quality)
- ✅ P0 4 项必做都落地
- ✅ 操作编号体系有(每条日志可唯一追溯)
- ❌ "先不做日志,上线了再补" → 拒绝,补日志 = 重做

## Phase 2:AI 汇总报告机制

**🎯 目标**:让 AI **定期**(如每双周)汇总日志,产出"模式"假设。

### 报告运转节奏

```
日常:Agent 配置 → 自动写入日志
         ↓
定时(每双周):AI 汇总分析 → 生成总结报告 → 推送飞书(双周会前1天)
         ↓
双周会:运营团队过报告 → 人工标注(哪些对、哪些错、哪些是规律)
         ↓
会后:标注结果回喂 AI → AI 结合人工判断做经验沉淀
         ↓
沉淀的经验更新 Agent 知识库 → 反哺日常配置 → 循环
```

### AI 总结报告内容(7 板块)

| 板块 | 内容 |
|---|---|
| 操作概览 | Agent 配置总量、各类型分布、成功率、**各区域/国家分布** |
| 准确率分析 | "AI 填写 vs 用户最终提交"一致率,**按区域拆分对比** |
| 高频修改 TOP 10 | 用户最常修改的字段及模式,**标注是否存在区域差异** |
| 合规拦截统计 | 各市场合规规则触发次数、拦截率、最常见的合规问题 |
| 模板使用率 | 各模板的使用频次和修改率,识别需要更新的模板 |
| AI 发现的模式 | 潜在规律(待人工确认),**按区域标注适用范围** |
| 建议经验条目 | AI 草拟的规则(待人工审核),**标注建议归入 Global / Region / Country 哪一层** |

### 双周会动作

1. 逐条过"高频修改"—— 区分系统性偏差 vs 个例
2. 审核"AI 发现的模式"—— 标注 ✅ 有效 / ❌ 不是规律 / ⚠️ 需更多数据
3. 审核"建议经验条目"—— 修改措辞、补充条件、确认或否决
4. 补充 AI 没发现的隐性经验

**原则**:**AI 先做脏活(汇总、归类、提假设),人类只做判断(确认、否决、补充)**。运营不需要每次操作都打分。

**🚧 Phase 2 门禁**:
- ✅ 报告节奏明确(每双周)
- ✅ 7 板块都覆盖
- ✅ 双周会动作明确
- ❌ "AI 自动更新经验" → 拒绝,必须人工确认(AI 可能误判)

## Phase 3:经验库三层架构

**🎯 目标**:解决"量大了检索慢、命中低、互相矛盾"。

### 三层结构(来自 One Click)

| 层次 | 规则层 Rules | 模式层 Patterns | 原始层 Raw Cases |
|---|---|---|---|
| 数量级 | 几十~几百条 | 几百~几千条 | 全量操作记录 |
| 性质 | 确定性规则,直接影响 Agent 行为 | 统计规律,需人工确认后升级 | 事实记录,不直接参与决策 |
| 产生方式 | 双周会确认后从模式层升级 | AI 定时清洗日志后聚类分析 | Agent 每次交互自动写入 |
| Agent 使用 | 实时加载/检索,直接应用 | 不直接使用 | 不直接使用 |

### 流转关系

```
原始层 ──AI 清洗聚类──→ 模式层 ──双周会确认──→ 规则层 ──→ Agent 决策推荐
```

**关键**:**只有向上流动,没有跳级**。AI 不能从原始日志直接生成规则,必须经过模式层 + 人工确认。

### 地域维度:经验继承链(国际化场景)

```
Global 规则(全球通用,如"促销必须有结束时间")
  └── Region 规则(区域级,如"EU 市场必须展示含税价")
        └── Country 规则(国家级,如"德国折扣不得超过原价标注的 50%")
              └── Cluster 规则(集群/城市级,按需)
```

**继承 vs 覆盖**:
- 细化:下级可以在上级基础上增加约束
- 覆盖:下级可覆盖上级规则,**但需人工确认 + 留审计记录**
- 就近优先:Agent 配置时按 Country → Region → Global 顺序匹配,命中即停

### 落地分级

- **P1(flat 结构 + country 标签)**:经验库只做一层扁平结构,每条规则打 country 标签。此阶段经验条目预计只有几十条,四层继承是过度设计。
- **P2(引入层级继承)**:当经验条目超过 200 条、出现跨市场复用需求时,引入 Global → Region → Country 层级。
- **判断标准**:**如果你发现自己在给 20 个 EU 国家各复制一条一模一样的规则,就是该引入层级的时候了**。

### 生命周期管理

| 机制 | 说明 |
|---|---|
| 规则过期 | 连续 3 个月未命中 → 自动标记"待复核" → 双周会决定保留或废弃 |
| 模式清理 | 已否决保留 3 个月后归档;已升级为规则的标记"已毕业" |
| 原始层归档 | 超 6 个月移到冷存储,仍可查询但不参与 AI 清洗 |

**🚧 Phase 3 门禁**:
- ✅ 三层结构清晰
- ✅ 流转规则明确(只能向上,不能跳级)
- ✅ 生命周期管理(过期 / 归档 / 清理)
- ❌ "AI 直接改规则" → 拒绝,必须经模式层 + 人工确认

## 下一步

学习循环设计完成后:
- 调用 `agent-phasing` 做 P0-P3 分期规划(决定每阶段做多少)

## 常见踩坑

| 坑 | 解决 |
|---|---|
| 日志留空格式不全 | user_modified / rules_blocked / tags 必含 |
| AI 自动沉淀规则 | 错,必须人工确认(AI 会误判个例为规律) |
| 一开始就做地域三层 | 错,P1 用 flat + country 标签够了,200 条后再分层 |
| 规则永远不过期 | 错,3 个月未命中必须复核 |

## 写入日志

```json
{
  "timestamp": "ISO 8601",
  "skill": "agent-learning",
  "log_fields": ["meta", "geo", "interaction", "execution", "compliance",
                 "localization", "calendar", "tags", "quality"],
  "core_field_user_modified": true,
  "report_cadence": "bi-weekly",
  "report_sections": 7,
  "experience_layers": 3,
  "geo_hierarchy_stage": "P1_flat",
  "lifecycle_management": true,
  "outcome": "learning_loop_designed"
}
```
