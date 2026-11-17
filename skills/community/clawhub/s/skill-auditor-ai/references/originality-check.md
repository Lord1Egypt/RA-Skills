# 原创度审计与嫁接清洗

**When to read**: 执行 D-O 系列检查（嫁接痕迹识别+清洗）时，或用户主动触发"原创度审计"/"嫁接清洗"时。本文件定义 7 类嫁接痕迹的识别模式、清洗策略和验证清单。

---

## 背景与原则

### 为什么需要嫁接清洗

开发者从已有技能 fork/继承/扩展时，源文件的措辞会残留对父技能的引用（"继承自 skill-xxx"、"与 skill-xxx 分工"、"交接 skill-xxx 发布"等）。这些痕迹：

1. **降低原创感**：用户阅读时立刻识别为"派生物"，对技能的专业度评价下降
2. **暴露内部工具链**：父技能名可能是私有/未发布的，残留等于泄露内部信息
3. **影响平台合规**：Do NOT 指向具体技能名可能触发 ClawHub SkillSpector 的 MCP Tool Poisoning 检测
4. **阻碍独立演化**：清洗后技能可独立演化，不绑定父技能的迭代节奏

### 核心判断铁律

> **能否用「场景描述」替代「具体技能名」？能则替代，不能则保留。**

| 原措辞（点名） | 清洗后（场景化） | 判断 |
|---------------|----------------|------|
| "Do NOT use for skill-forge" | "Do NOT use for creating skills" | ✅ 场景化 |
| "交接 skill-publisher 发布" | "建议用户手动发布到三平台" | ✅ 场景化 |
| "继承自 skill-forge benchmarking.md" | "定义 C 维度同类竞争审计方法论" | ✅ 场景化 |
| "本技能读取 references/security-scan.md" | 保留（自引用，不是嫁接） | ✅ 保留 |
| "触发词：技能审计" | 保留（自身触发词，不是嫁接） | ✅ 保留 |

---

## 7 类嫁接痕迹识别清单

### D-O1：直接继承声明

**识别模式**（Grep）：
```
继承自|based on|forked from|derived from|extended from|扩展自|源自
```

**典型场景**：
- references/*.md 文件头："继承自 skill-xxx 的 references/yyy.md，扩展为审计用途"
- SKILL.md 设计原则段："本技能基于 skill-xxx 派生"
- README.md 介绍段："forked from skill-xxx"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "继承自 skill-xxx 的 yyy.md，扩展为审计用途" | "定义 X 维度的完整方法论" |
| "based on skill-xxx" | 删除整段，改为独立介绍 |
| "扩展自 skill-xxx" | 删除，描述本技能自身职责 |

**保留例外**：自引用（"本技能的 references/yyy.md"）不是嫁接，保留。

---

### D-O2：Do NOT 指向具体技能名

**识别模式**（正则）：
```
Do NOT use for [a-z][a-z0-9-]+
```
（匹配 Do NOT 后紧跟 kebab-case 单词，点名具体技能名）

**典型场景**：
- SKILL.md frontmatter description："Do NOT use for skill-forge or skill-publisher"
- README.md 边界声明："不要用于 skill-xxx 的场景"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "Do NOT use for skill-forge or skill-publisher" | "Do NOT use for creating skills or publishing to platforms" |
| "Do NOT use for skill-xxx" | "Do NOT use for <场景词>" |

**场景词替换表**：
- skill-forge / 技能熔炉 / 技能创建 → "creating skills"
- skill-publisher / 技能发布 → "publishing to platforms"
- skill-auditor / 技能审计 → "auditing existing skills"
- skill-creator / 技能生成 → "generating new skills"

---

### D-O3：三角分工定位

**识别模式**：
```
三角分工|分工|XX 负责.*本技能负责|与.*的分工|本技能与.*互补
```

**典型场景**：
- README.md 定位段："与 skill-forge / skill-publisher 三角分工：skill-forge 负责创建，skill-publisher 负责发布，本技能负责审计"
- SKILL.md 任务段："在三角工作流中负责审计环节"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "与 skill-forge / skill-publisher 三角分工" | "专注深度审计+整改+回归，不负责创建或发布" |
| "在三角工作流中负责审计环节" | "独立审计定位：专注审计，不创建不发布" |
| "本技能与 skill-xxx 互补" | 删除整段，改为自身能力边界声明 |

---

### D-O4：发布/交接措辞

**识别模式**：
```
交接|调用.*发布|交给.*处理|移交|转交|交付给
```

**典型场景**：
- SKILL.md Phase 段："Phase N: 交接 skill-publisher 发布"
- SKILL.md 示例段："完成后调用 skill-publisher 推送到三平台"
- references/report-template.md："交接建议：调用 skill-publisher 发布"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "Phase N: 交接 skill-publisher 发布" | "Phase N: 发布建议（建议用户手动发布）" |
| "完成后调用 skill-publisher 推送" | "完成后建议用户手动发布到三平台" |
| "交接建议：调用 skill-xxx 发布" | "交接建议：建议用户手动发布" |

**关键约束**：清洗后必须保持"不自动发布"的语义不变，只是把"交接 X"改为"建议用户手动"。

---

### D-O5：示例点名其他技能

**识别方法**：审查 SKILL.md 示例段，检查是否含具体技能名（非自身）。

**典型场景**：
- 示例 1："用户调用 skill-publisher 发布"
- 示例 2："流程：skill-forge 创建 → skill-auditor 审计 → skill-publisher 发布"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "用户调用 skill-publisher 发布" | "用户手动发布到三平台" |
| "skill-forge 创建 → skill-auditor 审计 → skill-publisher 发布" | "创建 → 审计 → 发布（三阶段，由用户手动衔接）" |

---

### D-O6：CHANGELOG 历史痕迹

**识别方法**：审查 CHANGELOG.md 历史条目，检查是否含"XX 创建"/"继承自"/"forked from"。

**典型场景**：
- v1.0.0 条目："Initial version created by skill-forge"
- v1.1.0 条目："继承自 skill-xxx 的 yyy.md"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "Initial version created by skill-forge" | "Initial version: 8 维度审计矩阵" |
| "继承自 skill-xxx" | "新增 references/yyy.md" |
| "forked from skill-xxx" | 删除，改为功能描述 |

**关键约束**：CHANGELOG 历史条目不能删除（破坏版本可追溯性），只能重新措辞。

---

### D-O7：场景描述点名

**识别方法**：审查 SKILL.md 触发条件段、对比段，检查是否点名具体技能作为对比。

**典型场景**：
- 触发条件段："技能创建/技能熔炉 = skill-forge"
- 对比段："本技能 vs skill-xxx 的区别"

**清洗策略**：
| 原措辞 | 清洗后 |
|--------|--------|
| "技能创建/技能熔炉 = skill-forge" | "技能创建/技能熔炉 = 从 0 创建新技能" |
| "本技能 vs skill-xxx" | "本技能 vs 同类审计工具" |

---

## 清洗执行流程

### Phase O-1: 全量扫描

对 skill 目录下所有文件执行 7 类 Grep 扫描：

```
1. D-O1 Grep: 继承自|based on|forked from|derived from|extended from|扩展自|源自
2. D-O2 正则: Do NOT use for [a-z][a-z0-9-]+
3. D-O3 Grep: 三角分工|分工|XX 负责.*本技能负责|与.*的分工
4. D-O4 Grep: 交接|调用.*发布|交给.*处理|移交|转交|交付给
5. D-O5 审查: SKILL.md 示例段
6. D-O6 审查: CHANGELOG.md 历史条目
7. D-O7 审查: SKILL.md 触发条件段/对比段
```

### Phase O-2: 分类标记

每条命中标记：
- **类别**：D-O1 ~ D-O7
- **位置**：file:line
- **原措辞**：命中片段
- **建议清洗后**：按清洗策略表
- **保留例外**：如是自引用/自身触发词，标记 PASS

### Phase O-3: 用户确认（确认点 O）

展示清洗清单，用户选择：
- A. 全部清洗（按建议替换）
- B. 选择性清洗（用户指定哪些清洗）
- C. 只要清单，自己改
- D. 取消

### Phase O-4: 执行清洗（需用户在确认点 O 授权）

**前置条件**：用户必须在确认点 O 明确选择 A/B/C 之一后才执行 Edit 操作。未授权 = 只输出清单，不修改任何文件。

按用户选择执行 Edit 操作：
- 每个清洗点单独 Edit，最小化改动
- 不"顺便优化"周边代码
- 不重构（即使发现相邻问题）
- **绝不跳过确认点 O 自动清洗**：任何触发词都不能绕过用户授权

### Phase O-5: 验证清单

清洗后必须验证：

| # | 验证项 | 方法 | PASS 标准 |
|---|--------|------|-----------|
| 1 | 7 类痕迹零残留 | 重新跑 Phase O-1 扫描 | 全部 PASS |
| 2 | 管线完整性 | 检查 4 模块/规则/示例仍齐全 | 无缺失 |
| 3 | 功能不退化 | description/触发词/Do NOT 语义不变 | 语义保留 |
| 4 | 引用不断链 | Grep references/*.md 引用 | 所有引用存在 |
| 5 | CHANGELOG 可追溯 | 历史条目仍在，只是重新措辞 | 版本号连续 |
| 6 | 自引用保留 | references 自引用未被误删 | 保留 |
| 7 | 自身触发词保留 | 触发词段未被误改 | 保留 |

### Phase O-6: 回归报告

输出清洗报告：
- 清洗点数 / 已清洗数 / 保留例外数
- 每类的清洗前后对比（前 3 条样本）
- 验证清单全部 PASS
- 综合原创度评分（清洗后）：X.X/10

---

## 主动触发模式

用户可通过以下触发词单独启动原创度审计：

| 触发词 | 行为 |
|--------|------|
| "原创度审计" / "原创性检查" | Phase O-1~O-6 全流程（含确认点 O） |
| "嫁接清洗" / "清洗嫁接痕迹" | Phase O-1~O-2 + **确认点 O**（用户授权后才清洗）+ Phase O-4~O-6 |
| "技能审计" + "原创度" | 全量审计 + D 维度重点查 D-O 系列 |
| "D-O 检查" | 仅执行 Phase O-1~O-2（扫描+清单，只读不修改） |

**安全约束**：所有触发词都**不能跳过确认点 O**。即使用户说"嫁接清洗"，也必须展示清洗清单并等待用户明确选择 A/B/C/D 后才能修改文件。"嫁接清洗"触发词与"原创度审计"的区别仅在入口，不在授权——两者都需用户授权才执行 Edit。

**与其他审计的关系**：
- 全量审计时 D 维度自动包含 D-O1~O7 检查
- 单维度 D 审计时 D-O1~O7 也包含
- 主动触发"原创度审计"只跑 D-O 系列，不跑 D1~D7

---

## 评分影响

- **D 维度评分**：D-O Finding 按 Important/Minor 计入 D 维度扣分
- **不新增权重**：D 维度权重仍 0.5（嫁接痕迹不是安全红线）
- **原创度评分**：清洗后单独输出"原创度评分"（0-10），不计入综合分，仅作参考
  - 10.0：无任何嫁接痕迹
  - 8.0-9.9：仅 Minor 痕迹（D-O2/O5/O6/O7）
  - 5.0-7.9：有 Important 痕迹（D-O1/O3/O4）
  - <5.0：大量 Important 痕迹

---

## 清洗边界（什么不能删）

清洗时**绝对不能删除**的内容：

| 类别 | 原因 |
|------|------|
| 自身触发词 | 删除会导致技能无法触发 |
| 自身 Do NOT 范围 | 删除会导致误触发 |
| 功能描述 | 删除会改变技能行为 |
| 规则条款 | 删除会降低可执行性 |
| references 自引用 | 删除会断链 |
| CHANGELOG 版本号 | 删除会破坏可追溯性 |
| 示例的语义结构 | 删除会降低示例有效性 |

**清洗只改"措辞"，不改"语义"**。

---

## 常见误区

### 误区1：过度清洗

**错误**：把所有提及"skill-xxx"的地方都删除，包括 SKILL.md 中"本技能不创建技能（参考 skill-creator 的设计）"这类**对比性引用**。

**正确**：对比性引用可以保留，只要不是"继承自"/"分工"这类**派生关系声明**。

### 误区2：清洗后破坏管线

**错误**：清洗"交接 skill-publisher"时，把整个 Phase N 段落删除。

**正确**：保留 Phase N 段落，只把"交接 skill-publisher 发布"改为"建议用户手动发布"。

### 误区3：CHANGELOG 删除历史

**错误**：删除 CHANGELOG 中含"skill-forge 创建"的历史条目。

**正确**：保留条目，重新措辞为"Initial version: 8 维度审计矩阵"。

### 误区4：误判自引用

**错误**：把 SKILL.md 中"读取 references/security-scan.md"误判为嫁接痕迹。

**正确**：这是自引用（references 是本技能自己的目录），不是嫁接。

---

## 清洗策略速查表

| 痕迹类型 | 优先策略 | 替代策略 | 不可用时 |
|---------|---------|---------|---------|
| D-O1 直接继承 | 删除声明，改为自身职责描述 | 用"独立设计"替代"继承自" | 保留功能描述 |
| D-O2 Do NOT 点名 | 用场景词替代（creating/publishing） | 用动词替代（to create/to publish） | 保留 Do NOT 本身 |
| D-O3 三角分工 | 改为"独立定位：专注 X，不负责 Y" | 删除分工段，改为能力边界 | 保留能力边界声明 |
| D-O4 交接措辞 | 改为"建议用户手动 X" | 改为"用户可选择 X" | 保留 Phase 结构 |
| D-O5 示例点名 | 用场景描述替代 | 用"用户手动 X"替代 | 保留示例语义 |
| D-O6 CHANGELOG | 重新措辞为功能描述 | 删除派生关系，保留版本号 | 保留版本条目 |
| D-O7 场景点名 | 用场景词替代（"技能创建"） | 用动词替代（"to create"） | 保留对比结构 |
