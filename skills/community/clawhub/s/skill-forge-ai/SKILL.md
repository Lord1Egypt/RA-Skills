---
name: "skill-forge"
slug: "skill-forge-ai"
displayName: "Skill Forge 技能熔炉"
description: "技能熔炉 — 锻造/评估/改进 Skill。说 技能熔炉 走全流程（含R5改进已有skill）；说 技能评估/skill评估/评估技能 只做同类比对+腾讯9维度。可选能力：搜索SkillHub同类技能（通过TRAE内置工具）、修改已有skill文件（仅R5诊断修复路径，需用户确认）。发布环节请用 skill-publisher。Do NOT use for skill security vetting, skill publishing (use skill-publisher), or general coding tasks."
version: "6.4.0"
license: "MIT-0"
summary: "锻造 → 评估 → 改进，两入口全流程交付可自动触发、稳定输出的 Skill。v6.4.0 修复 ClawHub SkillSpector 审计 findings。发布由 skill-publisher 承接。"
allowed-tools: "Read, Write, Edit, Glob, Grep, LS, AskUserQuestion"
metadata:
  openclaw:
    skillKey: "skill-forge"
    emoji: "⚒️"
    homepage: "https://github.com/EdwardWason/skill-forge"
    os: ["windows", "macos", "linux"]
    requires:
      bins: []
      env: []
    primaryEnv: ""
    envVars: []
    always: false
---

# 技能熔炉 v6.4.0

锻造 → 评估，两入口全流程交付可自动触发、稳定输出的 Skill。发布环节由独立的 skill-publisher 技能承接。

## 入口检测

| 触发词 | 入口 | 执行流程 |
|--------|------|---------|
| 技能熔炉 | Phase -1 | 前置闸门→入口路由→访谈→确认门→同类预检→创建→验证→评估→发布交接提醒 |
| 技能评估 / skill评估 / 评估技能 | Phase 2 | 只做 SkillHub 同类比对 + 腾讯9维度 |

**检测到触发词后，立即跳转到对应 Phase，不执行前面的阶段。**

**发布不在本技能范围内**：当用户说"技能发布/发布技能/更新技能/迭代技能"时，应触发 skill-publisher，不是本技能。

## 撰写原则（5 大原则，必读）

完整 5 大原则详见 [`references/authoring-principles.md`](references/authoring-principles.md) — 创建 Skill 前必读，作为"声明-行为一致性"的硬门控。原三条铁律映射到原则 1/1/4，补充原则 3（最小权限）和原则 5（用户知情）：

| 原则 | 一句话 | 对应原铁律 |
|------|--------|-----------|
| 1. 声明-行为一致性 | name/description/metadata/行为四者对齐 | 铁律1 Description先行（扩展） |
| 2. 权力比例适当 | 副作用强度 ≤ 用户预期 + 披露程度 | （新增） |
| 3. 最小权限 | allowed-tools 只列实际需要的工具 | （新增） |
| 4. 渐进式披露 | SKILL.md ≤200 行，细节下沉 references/ | 铁律3 渐进式披露 |
| 5. 用户知情 | 有副作用必须 README 警告 + 关闭方式 | （新增） |

> 原"铁律2 一Skill一职"已并入原则 1（声明-行为一致性）：description 必须明确单一职责，多功能 Skill 触发混乱本质是声明-行为不一致。

## 权限声明

本技能实际使用的能力类别（用户须知）：

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ✅ | 通过 TRAE 内置工具搜索 SkillHub 同类技能（不直接发起网络请求） |
| 文件读写 | ✅ | 在用户指定目录创建/修改 skill 文件（SKILL.md/references/scripts/assets） |
| 环境变量 | ❌ | 不读取任何环境变量（无凭证需求） |
| subprocess | ❌ | 不调用任何外部命令 |
| 外部 API | ❌ | 不调用任何外部 API（SkillHub 同类搜索由 TRAE 内置工具完成） |

**用户警告**：本技能会在用户指定目录创建/修改 skill 文件（R1-R4 创建新 skill，R5 可修改已有 skill）。R5 修改已有 skill 前需用户确认诊断结果。如不希望写入文件，可在确认门前终止流程。本技能不执行任何发布操作（发布由 skill-publisher 承接）。

## SKILL.md 格式（完整 frontmatter 示例）

```markdown
---
name: "<skill-name>"
slug: "<skill-name>-ai"
displayName: "<Skill Name>"
description: "<做什么 + 何时触发 + Do NOT 范围. 核心关键词放前200字符>"
version: "<MAJOR.MINOR.PATCH>"
license: "MIT-0"
summary: "<一句话摘要>"
allowed-tools: "<工具白名单>"
metadata:
  openclaw:
    skillKey: "<skill-name>"
    emoji: "<emoji>"
    homepage: "<https://github.com/...>"
    os: ["windows", "macos", "linux"]
    requires:
      bins: []
      env: []
    primaryEnv: ""
    envVars: []
    always: false
---

# <技能标题>
## 任务
## 输出格式
## 规则
## 示例
## 故障排除（可选）
```

## 目录结构

```
<skill-name>/
├── SKILL.md          # 主入口（≤200行）
├── references/       # 长文档、方法论、详细案例
├── scripts/          # 可执行脚本（确定性操作）
├── assets/           # 模板、schema、示例文件
├── README.md         # 中英双语说明
├── CHANGELOG.md      # 版本日志
├── LICENSE           # MIT-0
└── .claude-plugin/plugin.json
```

---

## Phase -1: 前置闸门

**【入口：技能熔炉】** — 读取 [`references/pre-gate-and-routing.md`](references/pre-gate-and-routing.md) 获取完整闸门+路由方法论。

**动手前先判断三件事，该劝退就劝退：**

| 检查 | 通过 | 劝退 |
|------|------|------|
| 值不值得做？最近一周≥3次？做法固定？输出可预期？ | ≥2个Yes → 继续 | 一次性任务→"直接问AI更快" |
| 有没有现成的？SkillHub上有同类吗？ | 没有 or 有差距 → 继续 | 有且很好→"建议安装: skillhub install <slug>" |
| 是不是太大了？该拆成几个？ | 单一场景 → 继续 | 多场景→"建议拆开，先做哪个？" |

## Phase 0: 入口路由与需求共创

**【入口：技能熔炉】** — 读取 [`references/pre-gate-and-routing.md`](references/pre-gate-and-routing.md) Part 2-3 + [`references/interview-flow.md`](references/interview-flow.md) 获取完整方法论。

### Step 0.1: 五类入口路由

| 入口 | 信号 | 策略 |
|------|------|------|
| R1 从零想法 | "我想做个skill" | 自适应访谈（Step 0.2） |
| R2 从对话提取 | "把刚才对话变成skill" | 扫描上下文→提取步骤→生成草稿→确认门→Step 0.4 |
| R3 从现成材料 | 给文档/SOP | 分析材料→反推四要素→补缺→确认门→Step 0.4 |
| R4 从草稿完善 | 给半成品SKILL.md | 反推四要素→确认门→Step 0.4 同类预检→补全→验证 |
| R5 改进已有skill | "不触发/跑偏/太啰嗦" | 诊断：症状→检查点→动作→修复→验证 |

### Step 0.2: 自适应访谈（2-5轮，一次一问）

**水平自适应**：从用户措辞判断水平。张口pandas→用术语；说"差不多就行"→换大白话。**全程不问"你几级"**。

**一次一问**：每轮只问1个问题+2-3个选项。一次甩3个问题，用户只会挑最好答的。

**四要素**：做什么 / 何时触发 / 输入输出 / 边界。≥3个明确→进入确认门。

### Step 0.3: 确认门

**理解没对齐，绝不动手写。**

```
我理解是这样——
· 做什么：[一句话]
· 何时触发：[用户会说的话]
· 输入：[格式]；输出：[格式]
· 边界：[不做什么]
这样对吗？没问题我就开始写了。
```

用户确认 → Step 0.4 同类预检。用户纠正 → 修正后重新确认。

### Step 0.4: 同类预检（创建前）

**【入口：技能熔炉】** — 读取 [`references/composition-and-pipeline.md`](references/composition-and-pipeline.md) 获取组合与管线编排方法论。

**适用范围**：所有创建类入口（R1/R2/R3/R4）的确认门通过后必须执行。R5 改进类跳过（走诊断模式）。**即使用户带着成熟的想法、现成仓库、教程材料或半成品草稿调用，也不能跳过此环节**——必须先收敛递归转写为四要素 plan，确认门对齐后再做同类预检。

**确认门通过后，立即搜索 SkillHub，避免重复造轮子：**

| 分支 | 条件 | 动作 |
|------|------|------|
| **a) 有现成的更好** | 找到高质量同类(≥7分) | 建议安装已有Skill，结束流程 |
| **b) 有但不够好** | 有同类但有明显差距 | 提取差异点→作为Phase 1设计输入 |
| **c) 无同类** | 没有同类Skill | 直接进入Phase 1创建 |
| **d) 可组合** | 需求可分解为多个原子操作 | 元技能组合+管线编排建议 |

**分支d详解**：需求分解为原子操作→逐个搜索→评估覆盖率：
- 全组合：所有步骤都有高质量Skill→建议安装+编排管线，无需新建
- 部分组合：部分有高质量→安装已有的+只新建缺失的
- 全新建：无高质量同类→直接Phase 1

---

## Phase 1: 创建

**【入口：技能熔炉】**

### Step 1: Description先行 + 触发优化迭代

**格式**: `"<做什么>. 当用户说<触发词>时触发. Do NOT use for <排除范围>."`

**触发优化迭代**：初版description写完后，用5条真实用户说法测试触发准确率。触发不准→自动迭代用词。最多3轮。

### Step 2: 撰写4+1模块

任务（锁定边界）/ 输出格式（固定结构）/ 规则（3-5条，实习生测试）/ 示例（完整输入输出）/ 故障排除（可选）

### Step 3: 创建目录和文件

有确定性操作→创建 `scripts/`。有模板样式→创建 `assets/`。

### Step 4: 分层验证

**默认轻量验证（小白/日常）：**
- **Step 4a**: Schema检查 — 完整 10 项自检清单见 [`references/authoring-principles.md`](references/authoring-principles.md) §六（含 frontmatter 字段齐全 / description 三要素 / SKILL.md ≤200 行 / allowed-tools 最小权限 / metadata.openclaw 声明 / 无凭证硬编码 / Lethal Trifecta / CHANGELOG 版本一致 / plugin.json 一致）
- **Step 4b**: 安全红线（7条RED FLAG）
- **Step 4c**: 跑给你看 — 拿真实输入跑一遍→看结果→确认/微调

**可选重型验证（老手/严谨场景）：**
- **Step 4d**: 触发测试 — 5条真实用户说法+3条反向
- **Step 4e**: 量化评分（0-10）
- **Step 4f**: 基线对比（有Skill vs 无Skill）

**最多3次迭代。3次后建议"先发布V1再迭代"。**

---

## Phase 2: 质量自评 + 差异化验证

**【入口：技能评估 / skill评估 / 评估技能】** — 读取 [`references/benchmarking-guide.md`](references/benchmarking-guide.md)。

> **角色调整**：同类搜索已前移到 Step 0.4（创建前）。Phase 2 现在聚焦于创建后的质量自评和差异化验证。

### Step 5a: 腾讯9维度自评 — 触发精准度/关键词前置/Do NOT/单一职责/4模块/输出具体性/实习生测试/示例覆盖/体积控制。逐维度自评，标出弱项。

### Step 5b: 差异化验证 — 如果 Step 0.4 发现有同类，验证差异化优势是否落地。如果无同类，跳过。

### Step 5c: 盲区修复 — 列出弱项和盲区，附腾讯手册依据，提出修复方案。

### Step 5d: 用户决策 — 采纳修复 / 保持原样。**用户决策为最终决策。**

---

## 发布交接提醒

**触发条件**：Phase 2 评估完成（Step 5d 用户选择"保持原样"或"采纳修复且修复完成"），且用户未选择"直接安装已有"。

**触发时提示**：

> Skill 已通过锻造与评估。如需发布到 GitHub + ClawHub + SkillHub，请说"技能发布"或"发布技能"调用 **skill-publisher** 技能，它负责：前置条件校验 → 仓库结构生成 → 安全审查 → 版本号查重 → 三平台推送 → 发布后验证 → 本地安装同步。

**不要在本技能内执行任何发布操作。** 发布是独立技能 skill-publisher 的职责，本技能仅负责锻造与评估。

---

## References

- **[authoring-principles.md](references/authoring-principles.md)** — 5 大撰写原则 + frontmatter 规范 + 6 大反模式 + 10 项自检清单（v5.2 新增，从 skill-auditor 反哺）
- **[pre-gate-and-routing.md](references/pre-gate-and-routing.md)** — Phase -1 闸门 + 五类入口路由 + 改进诊断脚本
- **[interview-flow.md](references/interview-flow.md)** — 一次一问 + 水平自适应 + 确认门 + B1-B6规则
- **[composition-and-pipeline.md](references/composition-and-pipeline.md)** — Step 0.4 元技能组合 + 管线编排方法论
- **[interview-methods.md](references/interview-methods.md)** — 行为追问、偏误检测、选项法深度参考
- **[benchmarking-guide.md](references/benchmarking-guide.md)** — 腾讯9维度自评模板 + 差异化验证
- **[meeting-action-extractor-example.md](references/meeting-action-extractor-example.md)** — 完整Skill示例
