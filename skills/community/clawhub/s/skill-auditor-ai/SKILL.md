---
name: "skill-auditor"
slug: "skill-auditor-ai"
displayName: "Skill Auditor"
description: "对已存在 Skill 做 8 维度全面体检（结构/安全/触发/有效性/竞争/平台/文档/代码质量）。说 技能审计/审计技能/技能体检 时触发。支持成熟度分级+4确认点+整改+回归审计。绝不自动发布。Do NOT use for creating skills or publishing to platforms."
version: "2.0.1"
license: "MIT"
summary: "对已存在 Skill 做 8 维度全面体检，支持三级成熟度分级+4确认点+整改模式+回归审计。绝不自动发布。"
allowed-tools: "Read, Write, Edit, Glob, Grep, LS, WebFetch, AskUserQuestion"
metadata:
  openclaw:
    skillKey: "skill-auditor"
    emoji: "🔍"
    homepage: "https://github.com/EdwardWason/skill-auditor"
    os: ["windows", "macos", "linux"]
    requires:
      bins: []
      env: []
    primaryEnv: ""
    envVars: []
    always: false
---

# 技能审计师

对已存在 Skill 做 8 维度体检，按成熟度分级执行不同深度审计，4 个用户确认点全程可控。**只审计+可选整改，绝不自动发布**。

## 何时触发

**触发词**：「技能审计」/「审计技能」/「skill审计」/「技能体检」/「原创度审计」/「嫁接清洗」/「清洗嫁接痕迹」

**与相似场景区分**：
- 「技能创建/技能熔炉」= 从 0 创建新技能；「技能发布」= 推送到外部平台
- 「技能审计」= 8 维度体检 + 成熟度分级 + 整改 + 回归（本技能）
- 「原创度审计」/「嫁接清洗」= 仅执行 D-O 系列检查 + 清洗（本技能的专项子模式）

**前置条件**：用户给出目标 Skill 路径或名称 + 目录下有 SKILL.md

## 任务

只做 Skill 的**深度审计 + 可选整改 + 回归验证**：8 维度扫描 → 标准化报告 → 用户确认 → 可选整改 → 可选回归 → 可选发布交接。**不自动发布，发布需用户在确认点4明确授权**。

## 权限声明

**本技能的行为范围（用户须知）**：
- 读取被审计 Skill 目录的文件（Read/Glob/Grep/LS）
- 可选网络访问：WebFetch 调用 SkillHub API 做 C 维度比对（不可达时跳过）
- 整改模式（用户授权后）：Edit/Write 修改被审计 Skill 文件
- 输出审计报告到被审计 Skill 目录（.audit-report.md）
- 绝不自动发布，不自动执行发布操作（除非用户明确授权后建议手动发布）

## 输出格式

**审计报告**（同时输出到对话和 `<skill-dir>/.audit-report.md`）：
1. **成熟度等级**：L1原型 / L2迭代 / L3发布
2. **审计范围**：本次执行的维度（按成熟度确定）
3. **综合评分表**：各维度 0-10 分 + 加权综合分 + 状态
4. **Findings 列表**：按严重性分级，每条含位置(file:line) + 问题 + 修复建议 + 优先级(P0-P3)
5. **整改报告**（如进入整改模式）：已修复/未修复/验证结果
6. **回归报告**（如进入回归）：已修复✅/未修复❌/新增🆕

## 三级成熟度模型

| 等级 | 名称 | 审计范围 | 严格度 |
|------|------|---------|--------|
| **L1** | 原型阶段 | S(精简) + A(精简) + D1 | 只报 Critical，Important 以下为"建议" |
| **L2** | 迭代阶段 | S/T/A/E/D/Q（6维度，跳过 C/P） | Critical 必修，Important 建议修 |
| **L3** | 发布阶段 | 全量 8 维度 | Critical/Important 必修，Minor 建议修 |

**识别信号**：references/ 目录 + SKILL.md 行数 + version + CHANGELOG + scripts/ + 用户明示

**详细判定规则**：读取 [`references/maturity-model.md`](references/maturity-model.md)

## 8 大审计维度

| 代号 | 维度 | 核心检查 |
|------|------|---------|
| S | 结构合规 | frontmatter / 4模块 / ≤200行 / 渐进式披露 |
| T | 安全合规 | 凭证/路径/危险命令/YARA/SSD3/MCP + **AST10 对齐** + **Lethal Trifecta** |
| A | 触发可靠性 | 正例/反例/触发词冲突/关键词前置 |
| E | 功能有效性 | 声明一致性/输出格式/增量价值 |
| C | 同类竞争 | SkillHub API + 腾讯9维度 + 差异化 |
| P | 平台合规 | TRACE五维度 + SkillSpector9项 + 文件限制 + **Coherence 审计** |
| D | 文档一致性 | 引用一致/版本号同步/中英文同步 + **声明-行为一致性(D-M)** + 嫁接清洗(D-O) |
| Q | 代码质量 | 错误处理/资源管理/命名/复杂度 |

**详细检查项**：读取 [`references/audit-dimensions.md`](references/audit-dimensions.md)

## 执行流程（5 Phase + 4 确认点）

### Phase 0: 入口识别 + 成熟度判定 + 【确认点1】

1. 检测触发词 → 确定入口模式（全量/单维度/批量/回归）
2. 全量审计模式 → 自动识别成熟度（L1/L2/L3）
3. **【确认点1】** 展示识别结果 + 建议审计范围，用户确认或调整等级

### Phase 1-3: 按成熟度执行审计

- **Phase 1 静态扫描**（S/T/D/Q）：LS + Grep + 读取文件
- **Phase 2 动态测试**（A/E）：触发逻辑验证 + 声明一致性
- **Phase 3 外部比对**（C/P，仅 L3）：SkillHub API + 平台规则

### Phase 4: 报告生成 + 【确认点2】

生成报告 → **【确认点2】** 用户选择：
- A. 进入整改模式（授权修改被审计 Skill）
- B. 只要报告，自己改
- C. 重新审计（调整成熟度/维度）
- D. 结束

### Phase 4.5: 整改模式（仅用户选 A）

用户选 A 后，追加选择整改子模式：

- **A1. 标准整改**：按 P0→P1→P2 顺序修复所有 Finding（含 D-O 类）
- **A2. 原创度优化**：仅集中清洗 D-O1~O7 嫁接痕迹（适合已审计过、只想清洗派生痕迹的场景）
- **A3. 两者都做**：先标准整改，再原创度优化

**A2 子模式**：扫描 7 类痕迹 → 分类标记 → 【确认点 O】用户选择 → 执行清洗 → 7 项验证 → 回归报告。详细流程见 [`references/originality-check.md`](references/originality-check.md)。

**约束**：最小化改动 / 只改措辞不改语义 / 不自动发布 / 清洗边界（不删功能描述/触发词/规则/references 自引用/CHANGELOG 版本号）

### Phase 5: 回归验证 + 【确认点3】

整改后自动回归 / 独立回归触发 → 对比前后报告 → **【确认点3】** 用户选择：
- A. 再做一轮回归
- B. 发布（仅 L3 可选）
- C. 结束

### Phase 6: 发布建议 + 【确认点4】（仅 L3 + 用户选 B）

**【确认点4】** 发布确认 → 用户**必须明确选"是，发布"**才建议用户手动发布
**发布前置条件**：回归分≥7.0 + 无 Critical + 无 Important(L3) + L3 等级

**绝不自动发布**：即使所有条件满足，也必须用户明确授权后，仅提供发布建议，不自动执行发布。

## 严重性分级

| 级别 | 标签 | 含义 |
|------|------|------|
| Critical | 🚨 | 必须修复，阻止发布 |
| Important | ⚠️ | 应该修复，影响质量 |
| Minor | 💡 | 可选优化 |
| FYI | ℹ️ | 信息参考 |

## 评分标准

每维度 0-10 分，综合分加权（T×2.0, P×1.5, S/A/E×1.0, C/D/Q×0.5）
T 维度有 Critical → 综合状态 = ❌ FAIL（一票否决）

**双维度评分（v2.0.0）**：
- **Risk Level**：Low（只读）/ Medium（改本地文件）/ High（外部推送/网络外发）— 评估权力大小
- **Audit Status**：Pass / Review / Warn / Fail — 评估权力是否合理披露
- High Risk + Pass = 合理（权力大但已披露且比例适当）

## 规则

1. **绝不自动发布**：任何阶段都不自动执行发布操作，必须用户在确认点4明确选"是，发布"后才提供发布建议
2. **整改需授权**：默认只读审计，用户在确认点2选 A 才授权修改被审计 Skill
3. **成熟度可覆盖**：用户可强制指定等级（如"对原型做全量审计"），覆盖自动识别
4. **整改最小化**：每个修复只改 Finding 涉及的行，不做"顺便优化"，不重构
5. **Pre-Scan 必做**：LS 列出所有文件（含 .gitignore 中的），Grep 会跳过 .gitignore 文件
6. **网络降级**：SkillHub API 不可达时 C 维度跳过并标注；回归模式需存在上次 `.audit-report.md`，不存在则降级为首次全量审计
7. **L1/L2 不显示发布选项**：确认点3 的 B 选项（发布）仅 L3 阶段显示
8. **模糊回答追问**：确认点4 的发布确认，模糊回答（如"好吧"）→ 追问"请明确确认"
9. **Finding 必含位置**：每个 Finding 必须标注 `file:line` 或具体文件路径

## 示例

### 示例1：L2 迭代阶段全量审计 + 整改 + 回归

**用户**："技能审计 wx-peitu"
**Phase 0**：识别 L2（references/存在 + version 7.1.0 + CHANGELOG 有更新）
**【确认点1】**："识别为 L2，建议 S/T/A/E/D/Q 6维度。确认？" → 用户选 A
**Phase 1-3**：6 维度审计完成 → 报告 综合分 7.4 ⚠️，1 Critical + 2 Important
**【确认点2】**："进入整改？" → 用户选 A → 修复 P0(凭证泄露) + P1(行数超标) → 验证通过
**Phase 5**：回归审计 综合分 7.4→8.5 ↑
**【确认点3】**："L2 不显示发布选项。再做回归/结束？" → 用户选 C 结束

### 示例2：L3 发布阶段 + 发布交接

**用户**："技能审计 web-to-fim，准备发布"
**Phase 0**：识别 L3（用户明示"准备发布" + version 3.3.0 + references 5文件）
**【确认点1】**："识别为 L3，全量 8 维度。确认？" → 用户选 A
**Phase 1-3**：8 维度审计完成，综合分 8.0 ✅
**【确认点2】**："进入整改？" → 用户选 A（修复 1 个 Minor）→ 验证通过
**Phase 5**：回归审计 综合分 8.0→8.5 ↑
**【确认点3】**："L3 阶段。再做回归/发布/结束？" → 用户选 B
**【确认点4】**："⚠️ 即将发布 web-to-fim v3.3.0 到三平台。是否发布？"
用户明确选 A "是，发布" → 提供发布建议（建议用户手动发布）

### 示例3：用户拒绝自动发布

**【确认点4】**：展示发布确认 → 用户选 B "暂不发布"
**输出**："建议用户手动发布到三平台。审计报告已保存到 .audit-report.md"
**不自动执行发布操作**

### 示例4：原创度审计 + 嫁接清洗（A2 子模式）

**用户**："原创度审计 skill-xxx"

**Phase O-1**：扫描 7 类嫁接痕迹，命中 D-O1(继承声明 3处) + D-O4(交接措辞 2处) + D-O6(CHANGELOG 1处)
**【确认点 O】**："6 处嫁接痕迹，全部清洗？" → 用户选 A
**Phase O-4**：执行清洗（"继承自 skill-yyy" → "定义 X 维度方法论"；"交接 skill-zzz" → "建议用户手动发布"）
**Phase O-5**：7 项验证全部 PASS（零残留/管线完整/功能不退化/引用不断链/CHANGELOG 可追溯/自引用保留/触发词保留）
**Phase O-6**：原创度评分 7.2 → 10.0 ↑

## References

- **[`references/maturity-model.md`](references/maturity-model.md)** — 三级成熟度详细模型（识别信号 + 判定规则 + 各等级审计范围）
- **[`references/audit-dimensions.md`](references/audit-dimensions.md)** — 8 维度详细检查项（含 AST10 + Lethal Trifecta + D-M + D-O + P-C）
- **[`references/security-scan.md`](references/security-scan.md)** — 安全扫描详细模式（5层 + SkillSpector 9项）
- **[`references/benchmarking.md`](references/benchmarking.md)** — 同类比对方法论（SkillHub + 腾讯9维度）
- **[`references/report-template.md`](references/report-template.md)** — 审计报告模板（含双维度评分 + 整改/回归模板）
- **[`references/regression.md`](references/regression.md)** — 回归审计方法论（差异对比规则）
- **[`references/originality-check.md`](references/originality-check.md)** — 原创度审计 + 嫁接清洗（D-O 系列）
- **[`references/skill-authoring-guide.md`](references/skill-authoring-guide.md)** — 高质量 Skill 撰写指南（5大原则 + frontmatter 规范 + 反模式 + 自检清单）
