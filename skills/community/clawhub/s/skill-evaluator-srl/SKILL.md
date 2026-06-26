---
name: skill-evaluator-srl
description: 对 Skill 进行质量评估打分的 Skill，输出评分报告与改进建议。评估 skill、skill 评分、SRL 评估、skill 质量、检查 skill、skill review、skill score
---

# Skill SRL 评估工具

## 概述

本 Skill 基于 SRL (Skill Reliability Level) 框架，对目标 Skill 进行评估打分。

**核心架构：AI 评审 + 脚本计算**

```
AI 阅读 Skill 全部内容
    → AI 对五维度逐项评分（输出结构化 JSON）
    → Python 脚本加权计算 + 等级映射 + 报告生成
```

- **AI 负责**：阅读理解、语义判断、给出评分和证据
- **脚本负责**：数学加权、修正因子、等级映射、报告格式化

**核心理念**：Skill 的置信度 = 输出中可被外部验证的客观事实占比。可验证的外部事实越多，置信度越高；模型自主推理越多，幻觉累积风险越高。

---

## 阶段 0: 确认评估目标

### 输入获取

- [ ] 确认用户要评估的 Skill 路径
  - 如果用户提供了具体路径，直接使用
  - 如果用户说"评估所有 skill"，逐个评估当前项目 skills 目录下的所有 Skill
  - 如果用户说"评估 xxx skill"，在当前项目 skills 目录下查找匹配的目录

### 验证目标

- [ ] 确认目标路径存在且包含 `SKILL.md`

---

## 阶段 1: 阅读 Skill 全部内容

### 读取文件

- [ ] 读取目标 Skill 的 **SKILL.md** 完整内容（这是最核心的评估对象）
- [ ] 读取 **scripts/** 目录下的所有脚本文件（如有）
- [ ] 读取 **README.md**（如有）
- [ ] 读取 **references/** 目录下的参考文档（如有，仅作为理解上下文的辅助，不作为评分对象）
- [ ] 浏览 `_meta.json` 获取元信息

### 建立全局理解

通过阅读上述文件，形成对 Skill 的完整理解：
- 这个 Skill 做什么？解决什么问题？
- 它的工作流有多少步骤/阶段？
- 它依赖哪些外部系统（CLI/API/DB/网页/AI推理）？
- 它有哪些脚本？脚本做什么？
- 它的错误处理策略是什么？

### 信息充分性检查（"我不知道"机制）

在进入阶段 2 之前，先判断目标 Skill 是否提供了足够信息进行有意义的评估：

**拒绝评估条件**（满足任一则停止）：
- SKILL.md 不存在
- SKILL.md 总行数 < 10 行（排除空行和 frontmatter）
- SKILL.md 中没有任何可识别的工作流/阶段/步骤描述

**触发时的行为**：
```
⚠️ 信息不足，无法进行有意义的 SRL 评估。

原因: [具体原因，如"SKILL.md 仅有 5 行有效内容"]

建议: 
- 补充 SKILL.md 中的工作流描述（阶段划分、步骤说明、错误处理策略等）
- 最低要求: 至少描述 Skill 的目标、工作流步骤、依赖的数据源
```
停止评估，不输出任何评分。

**降级评估条件**（不拒绝但标注不确定性）：
- SKILL.md 有效行数 < 50 行
- 没有 scripts/ 目录（无法评估脚本质量）
- 没有 references/ 目录（缺少上下文辅助）
- **评估目标是 skill-evaluator-srl 自身**（自评场景，存在循环论证风险）

**降级时的行为**：
- 继续评估，但在报告开头添加警告：`⚠️ 目标 Skill 提供的信息有限（有效行数 X 行），以下评估的置信度较低。`
- 如果是自评场景，额外添加警告：`⚠️ 这是自评场景（评估工具评估自身），失败语义清晰度等维度可能因循环论证而偏高。`
- 在阶段 3 的 JSON 输出中添加顶层字段 `"evaluation_confidence": "low"`（正常评估时为 `"normal"`）

---

## 阶段 2: AI 逐维度评审

基于对 Skill 内容的深度理解，逐一评估以下 5 个维度 + 3 个修正因子。

**评分方法：先提取事实，再基于事实打分**

每个维度的评审分两步走：
1. **回答锚定问题**：先回答一组客观事实问题（列出具体行号、命令、数量等），这些答案可被复核
2. **基于答案打分**：根据锚定问题的答案，参照评分公式/参考表给出子项分数

**评分原则**：
- 每个维度 0-100 分
- 每个维度包含 2-4 个子项，子项分数总和应等于维度总分
- 每个维度必须给出至少 2 条具体证据（引用 SKILL.md 中的**具体行号**或脚本中的**具体代码位置**）
- 评分要基于**实际阅读到的内容**，不可脑补 Skill 没写的能力
- evidence 格式示例：`"SKILL.md:47 使用 python3 srl_analyzer.py 执行脚本"`、`"scripts/analyzer.py:135 调用 subprocess.run()"`

**证据分层规则（重要）**：
评分时必须区分以下三个层级，并按层级赋予不同权重：
- **L1 规则声明**：SKILL.md 中写了"应该做 X"→ 可计入评分，但最高只能达到该子项满分的 60%
- **L2 规则实现**：脚本代码中实际实现了该规则（如 try-except、validate_input）→ 可达满分的 80%
- **L3 规则验证**：有测试用例或实际执行记录证明规则生效→ 可达满分的 100%

例如："SKILL.md 说应该拒绝评估" = L1，"脚本代码中有 if lines < 10: exit(1)" = L2，"测试了一个 3 行的 Skill 确实被拒绝" = L3。

**步骤计数规则**（用于幻觉暴露面维度的 Q1/Q2）：
- 步骤 = SKILL.md 中明确标注的阶段（如"阶段 0"、"阶段 1"），不包括阶段内部的子步骤
- 如果 SKILL.md 没有明确的阶段标记，则按顶层 `###` 标题计数
- 必须在 Q1 回答中列出每个步骤的行号和简述，确保计数口径透明

**单维度信息不足声明**：
如果某个维度的锚定问题全部回答为"无"或"未提及"，不要强行给出评分。而是：
- 该维度评分设为 **0**
- evidence 中写明 `"信息不足: SKILL.md 中未找到与此维度相关的任何描述"`
- 在 `improvement_suggestions` 中标注需要补充哪些信息

### 维度 1: 工程锚点密度 (25%)

评估 Skill 工作流中，有多少步骤依赖**可被外部验证的工程化手段**。

#### 锚定问题（先回答，再打分）

**Q1 锚点盘点**: 列出 SKILL.md 和脚本中所有工程锚点（CLI/Shell 命令、API/DB 调用、MCP 工具、文件系统操作），每个标注行号和内容。
**Q2 覆盖率**: 上述锚点覆盖了总共 N 个阶段中的几个？哪些阶段没有任何工程锚点？
**Q3 验证闭环**: 是否存在"执行操作 → 写入文件 → 读取确认"或"调用 API → 校验返回值"的验证闭环？列出所有闭环。
#### 评分公式

| 子项 | 满分 | 计算方式 |
|------|------|---------|
| anchor_coverage | 40 | **先算**: 覆盖率 = 有锚点的阶段数 / 总阶段数（如 3/6=50%）。**再查表**: 覆盖率≥80%→33-40分, 60-79%→22-32分, 40-59%→12-21分, 20-39%→5-11分, <20%→0-4分。**注意**: 严格按算出的百分比查表，不可跨区间。 |
| anchor_intensity | 30 | 密度 = 锚点总数 / 总阶段数。密度≥3→25-30, 2-2.9→18-24, 1-1.9→10-17, 0.5-0.9→4-9, <0.5→0-3 |
| verification_loop | 30 | 有完整的验证闭环（操作→确认）≥2处→22-30, 1处→12-21, 有锚点但无闭环→4-11, 无锚点→0-3 |

> **设计说明**：不再按锚点类型（CLI/API/MCP）分别计分。一个纯 CLI Skill 只要覆盖率高、密度大、有验证闭环，同样可以得满分。

### 维度 2: 幻觉暴露面 (20%)

评估纯 AI 推理且无外部验证的步骤占比。**分数越高 = 暴露面越小 = 越好**。

#### 锚定问题（先回答，再打分）

**Q1 步骤盘点**: 按上述「步骤计数规则」列出 SKILL.md 中所有阶段（行号+编号+简述），标记每步属于哪类：
- `[工程]` = 该步有 CLI/API/DB/文件系统 等外部验证手段
- `[AI]` = 该步纯靠 AI 推理，无外部验证
- `[混合]` = 该步有 AI 推理但结果会被后续工程步骤验证

**Q2 统计**: 工程步骤 X 个，AI 步骤 Y 个，混合步骤 Z 个，总步骤 N 个。纯 AI 占比 = Y / N = ?%

**Q3 输出格式**: 最终输出是什么格式？结构化数据(JSON/表格)？Markdown 报告？自由文本？

#### 评分公式

| 子项 | 满分 | 计算方式 |
|------|------|---------|
| speculative_ratio | 40 | 纯AI占比 <10%→35-40, 10-25%→25-34, 25-40%→15-24, 40-60%→8-14, >60%→0-7 |
| external_validation | 30 | 混合步骤占比（有验证配套的AI步骤）。≥50%→22-30, 20-49%→12-21, <20%→0-11 |
| output_determinism | 30 | 纯结构化输出（所有字段确定性，无自由文本字段）→22-30; 结构化为主但含自由文本字段（如 evidence 为自由文本）→12-21; 自由文本为主→0-11 |

### 维度 3: 失败语义清晰度 (20%)

评估 Skill 遇到错误时，是**停下来报错**还是**脑补继续跑**。

#### 锚定问题（先回答，再打分）

**Q1 错误处理盘点**: 在 SKILL.md 和脚本中，找出所有错误处理相关的描述或代码（行号+内容摘要）。分为：
- `[停止型]` = 检测到错误后停止执行并通知用户（如"如果失败，停止并报告"）
- `[降级型]` = 检测到错误后切换备用方案并标注（如"如果主源失败，用备源并标记低置信度"）
- `[模糊型]` = 提到了错误但处理不明确（如"如果出错，尝试其他方法"）

**Q2 置信度机制**: Skill 中是否有明确的置信度/不确定性标注机制？找出相关描述（行号+内容）。如果没有，写"无"。

**Q3 "我不知道"**: Skill 是否有明确指导在信息不足时拒绝输出？找出相关描述（行号+内容）。如果没有，写"无"。

#### 评分公式

| 子项 | 满分 | 计算方式 |
|------|------|---------|
| error_handling_strategy | 40 | 停止型≥3处→30-40, 停止型1-2处+降级型→20-29, 仅模糊型→10-19, 无→0-9 |
| confidence_degradation | 30 | 有明确的高/中/低分级→22-30, 偶尔标注不确定→10-21, 无→0-9 |
| idk_capability | 30 | 有明确拒绝输出的指导→22-30, 有"待验证"标注→10-21, 无→0-9 |

### 维度 4: 溯源性 (20%)

评估 Skill 输出的信息是否可追溯到可验证的数据来源。

#### 锚定问题（先回答，再打分）

**Q1 数据源盘点**: 列出 Skill 依赖的所有数据来源，每个标注类型：
- `[强溯源]` = 官方 API / CLI 输出 / 数据库查询（有明确契约）
- `[中溯源]` = 第三方聚合 API（有接口但不完全可控）
- `[弱溯源]` = 网页爬取（结构可能变化）
- `[无溯源]` = AI 自主推理（模型"知识"）

**Q2 溯源统计**: 强溯源 A 个，中溯源 B 个，弱溯源 C 个，无溯源 D 个。加权比例 = (A×1.0 + B×0.6 + C×0.3 + D×0) / (A+B+C+D) = ?

**Q3 引用标注**: Skill 是否要求在输出中标注数据来源？找出相关描述（行号+内容）。

**Q4 独立验证**: 用户拿到 Skill 的输出后，能否独立验证其准确性？需要什么信息？

#### 评分公式

| 子项 | 满分 | 计算方式 |
|------|------|---------|
| source_classification | 40 | 加权比例 ≥0.8→35-40, 0.6-0.79→25-34, 0.4-0.59→15-24, 0.2-0.39→5-14, <0.2→0-4 |
| citation_annotation | 30 | 有明确的来源标注要求→20-30（按严格程度）, 偶尔提到→8-19, 无→0-7 |
| independent_verifiability | 30 | 用户可完全独立验证→22-30, 大部分可验证→12-21, 少量可验证→4-11, 无法验证→0-3 |

### 维度 5: 可重现性推断 (15%)

推断 Skill 的**同输入同输出**稳定性。

#### 锚定问题（先回答，再打分）

**Q1 数据源确定性**: 基于维度4的数据源盘点，判断 Skill 属于哪个 Tier：
- Tier 1: 主要强溯源，几乎无弱/无溯源
- Tier 2: 混合，有一定弱溯源
- Tier 3: 主要弱溯源或无溯源

**Q2 状态管理**: Skill 中是否有以下状态持久化机制？逐项回答有/无+行号：
- checkpoint/进度保存？
- 中间结果写入文件？
- 数据库记录？
- 如果全无，状态如何在步骤间传递？（纯上下文？）

**Q3 随机源**: 列出所有可能导致"同输入不同输出"的因素（如：依赖搜索引擎结果、网页内容变化、AI 推理随机性等）。

#### 评分公式

| 子项 | 满分 | 计算方式 |
|------|------|---------|
| tier_determinism | 40 | Tier 1→30-40, Tier 2→15-29, Tier 3→0-14 |
| state_management | 30 | 有完整持久化（checkpoint+文件写入）→22-30, 有部分→10-21, 纯上下文→0-9 |
| step_determinism | 30 | 随机源≤1个→22-30, 2-3个→10-21, ≥4个→0-9 |

### Tier 分类

基于维度 5 Q1 的回答，确定 Skill 的 Tier 分类：

| Tier | 特征 | 典型数据源 |
|------|------|-----------|
| Tier 1 确定性 | 主要使用 CLI/API/DB，几乎无网页爬取 | GitHub API, PostgreSQL, 文件系统 |
| Tier 2 半确定性 | 混合使用 API 和网页，有缓存机制 | 天气API, 电商页面, 第三方聚合 |
| Tier 3 非确定性 | 主要依赖开放互联网搜索或 AI 推理 | 搜索引擎, 用户生成内容, AI 生成 |

### 修正因子（3 个辅助维度）

这三个维度不直接参与加权，但会**修正**上述五维评分。每个修正因子也通过锚定问题评审。

#### 时效性 (Timeliness) — 修正可重现性

**锚定问题**：
- Q1: 列出 Skill 依赖的所有外部系统/接口（包括 AI 模型本身）。每个标注：最近一次已知的 breaking change 是什么时候？（如果不确定写"未知"）
- Q2: 6 个月后这个 Skill 有多大概率还能正常工作？列出最可能失效的环节（包括 AI 模型升级可能导致的评分倾向变化）。
- Q3: Skill 中是否有缓存/版本锁定/刷新机制？找出相关描述（行号+内容）。

**评分**: 0-100。**连续修正**：修正量 = max(0, (50 - 时效性评分) / 50) × 20%，即评分 50 时不修正，0 时扣减 20%，线性插值。

#### 鲁棒性 (Robustness) — 修正幻觉暴露面

**锚定问题**：
- Q1: Skill 或脚本中是否有输入校验？列出所有校验逻辑（行号+校验内容）。
- Q2: 如果某个中间步骤失败，Skill 是否能跳过/回退/降级？找出相关描述。
- Q3: Skill 是否处理了边界条件（空输入、超长输入、格式错误等）？

**评分**: 0-100。**连续修正**：修正量 = max(0, (50 - 鲁棒性评分) / 50) × 10%，即评分 50 时不修正，0 时扣减 10%，线性插值。

#### 级联稳定性 (Cascade Stability) — 修正可重现性

**锚定问题**：
- Q1: Skill 的步骤链路有多长（多少个有依赖关系的步骤）？
- Q2: 是否有步骤的输出是下一步的唯一输入（紧耦合）？列出这样的步骤对。
- Q3: 链路中是否有中间检查点可以独立验证正确性？

**评分**: 0-100。**连续修正**：修正量 = max(0, (50 - 级联稳定性评分) / 50) × 20%，即评分 50 时不修正，0 时扣减 20%，线性插值。

---

## 阶段 3: 输出结构化评分 JSON

- [ ] 将上一阶段的评审结果组织为以下 JSON 格式。

**重要：每个维度必须包含 `anchoring_answers` 字段**，完整记录锚定问题的回答过程，确保评分推导可复核：

```json
{
  "skill_name": "skill 名称",
  "skill_path": "/path/to/skill",
  "description": "skill 简短描述",
  "tier": 2,
  "dimensions": {
    "anchor_density": {
      "score": 70,
      "sub_scores": {
        "anchor_coverage": 30,
        "anchor_intensity": 22,
        "verification_loop": 18
      },
      "anchoring_answers": {
        "Q1_anchor_list": [
          {"type": "CLI", "location": "SKILL.md:47", "content": "python3 srl_analyzer.py"},
          {"type": "文件系统", "location": "SKILL.md:50", "content": "读取 _meta.json"}
        ],
        "Q2_coverage": "2/5 阶段有锚点 = 40%",
        "Q3_verification_loops": [
          "JSON输出 → validate_input() 校验"
        ]
      },
      "evidence": [
        "SKILL.md:47 使用 python3 srl_analyzer.py 执行脚本",
        "scripts/xxx.py:135 调用 subprocess 执行 CLI 命令"
      ]
    },
    "hallucination_exposure": {
      "score": 65,
      "sub_scores": {
        "speculative_ratio": 25,
        "external_validation": 20,
        "output_determinism": 20
      },
      "evidence": ["..."]
    },
    "failure_transparency": {
      "score": 55,
      "sub_scores": {
        "error_handling_strategy": 20,
        "confidence_degradation": 18,
        "idk_capability": 17
      },
      "evidence": ["..."]
    },
    "traceability": {
      "score": 60,
      "sub_scores": {
        "source_classification": 25,
        "citation_annotation": 18,
        "independent_verifiability": 17
      },
      "evidence": ["..."]
    },
    "reproducibility": {
      "score": 50,
      "sub_scores": {
        "tier_determinism": 20,
        "state_management": 15,
        "step_determinism": 15
      },
      "evidence": ["..."]
    }
  },
  "corrections": {
    "timeliness": 70,
    "robustness": 60,
    "cascade_stability": 55
  },
  "improvement_suggestions": [
    "🔧 [失败语义清晰度] 当前 55/100 → 在阶段 X 的 API 调用后添加 HTTP 状态码检查，非 200 时停止执行并报告",
    "🔧 [可重现性] 当前 50/100 → 添加 checkpoint 文件将中间状态写入磁盘，减少对长上下文的依赖"
  ],
  "metadata": {
    "total_files": 8,
    "total_lines": 500,
    "skill_md_lines": 200,
    "total_phases": 5,
    "total_steps": 20,
    "has_scripts": true,
    "has_references": true,
    "script_files": ["scripts/xxx.py"]
  }
}
```

### 评分质量检查

在输出 JSON 前进行自检，并在 JSON 顶层添加 `"quality_checks"` 字段记录检查结果：
- [ ] 每个维度的 `score` 等于其 `sub_scores` 所有子项之和
- [ ] 所有分数在 0-100 范围内
- [ ] 每个维度至少有 2 条 evidence
- [ ] 每个维度包含 anchoring_answers 字段
- [ ] improvement_suggestions 按维度得分从低到高排序，为最低的 3 个维度各给 1-2 条建议
- [ ] 建议必须是具体可执行的（不是"改进错误处理"，而是"在第X步的API调用后添加返回值检查"）

在 JSON 顶层添加：
```json
"quality_checks": {
  "sub_scores_sum_match": true,
  "scores_in_range": true,
  "evidence_count_ok": true,
  "anchoring_answers_present": true,
  "all_passed": true
}
```

**自检失败时的处理**：
如果自检发现 sub_scores 求和不等于 score，或分数超出范围：
1. **优先自行修正**：调整 sub_scores 使其求和等于 score，或将越界分数钳位到 0-100
2. **修正后再输出**：不要输出已知错误的 JSON
3. **如果无法自行修正**（如发现逻辑矛盾无法调和）：直接输出当前 JSON 并在 `improvement_suggestions` 首条添加 `"⚠️ 评分自检未通过: [具体问题]，建议人工复核"`，让脚本的 validate_input() 做最终拦截

---

## 阶段 4: 运行计算脚本

- [ ] 将阶段 3 的 JSON 保存为临时文件或通过 stdin 传递给脚本：

```bash
# 方式一：通过 stdin（路径使用本 Skill 目录的绝对路径）
echo '<JSON数据>' | python3 <本Skill的scripts目录绝对路径>/srl_analyzer.py

# 方式二：通过文件
python3 <本Skill的scripts目录绝对路径>/srl_analyzer.py --input /tmp/srl-eval-input.json

# 查看输入 JSON Schema 说明
python3 <本Skill的scripts目录绝对路径>/srl_analyzer.py --schema

# 示例（假设 Skill 位于项目 .claude/skills/ 下）：
# python3 /absolute/path/to/.claude/skills/skill-evaluator-srl/scripts/srl_analyzer.py --input /tmp/srl-eval-input.json
```

- [ ] 脚本会自动完成：
  - 修正因子应用（时效性/鲁棒性/级联稳定性）
  - 五维加权求和
  - SRL 等级映射
  - Markdown/JSON 报告生成

- [ ] 获取脚本输出的报告

---

## 阶段 5: 输出最终报告

### 报告保存

- [ ] 将脚本输出的 Markdown 报告保存到目标 Skill 目录下的 `.srl-report.md`
- [ ] 将 JSON 报告保存到 `.srl-report.json`

```bash
# 生成 Markdown 报告
echo '<JSON>' | python3 <本Skill的scripts目录绝对路径>/srl_analyzer.py > /path/to/target-skill/.srl-report.md

# 生成 JSON 报告
echo '<JSON>' | python3 <本Skill的scripts目录绝对路径>/srl_analyzer.py --json > /path/to/target-skill/.srl-report.json
```

### 终端展示

- [ ] 在终端直接展示完整评估报告的关键内容（总评 + 五维评分 + 改进清单）

### 批量评估额外输出

如果是批量评估模式：
- [ ] 逐个 Skill 执行阶段 1-4
- [ ] 汇总所有结果，生成排名表
- [ ] 传入 JSON 数组给脚本使用 `--batch` 模式

---

## 参考文档

- [SRL 评估模版](assets/SRL-EVAL-TEMPLATE.md) — 报告输出模版
- [SRL 框架参考](references/srl-framework.md) — 理论六维、落地五维映射、五级标准、三类分档
- [评分规则详细文档](references/scoring-criteria.md) — 每个维度的完整评分标准和子项说明
- [srl_analyzer.py](scripts/srl_analyzer.py) — 加权计算 + 等级映射 + 报告生成脚本
