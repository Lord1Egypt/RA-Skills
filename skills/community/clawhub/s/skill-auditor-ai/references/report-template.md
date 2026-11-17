# 审计报告模板

**When to read**: Phase 4 报告生成时。本文件提供标准报告模板，审计员按此格式输出。

---

## 全量审计报告模板

```markdown
# Skill 审计报告

> 审计时间: YYYY-MM-DD HH:MM
> 审计模式: 全量 / 单维度(T) / 批量 / 回归 / 整改后回归
> 被审计 Skill: <name> v<version>
> 审计员: skill-auditor v1.1.0

## 成熟度等级

**识别结果**: L<L> <阶段名称>
**识别依据**:
- references/ 目录: <状态>
- SKILL.md 行数: <N> 行
- version: <version>
- CHANGELOG: <状态>
- 用户明示: <如有>

**审计范围**: <维度列表，如 "S/T/A/E/D/Q（6维度，跳过 C/P）">
**严格度**: <如 "Critical 必修，Important 建议修">

## 综合评分

### 基础评分表

| 维度 | 代号 | 评分 | 状态 | 说明 |
|------|------|------|------|------|
| 结构合规 | S | X.X/10 | ✅ / ⚠️ / ❌ | 一句话说明 |
| 安全合规 | T | X.X/10 | ✅ / ⚠️ / ❌ | 一句话说明 |
| 触发可靠性 | A | X.X/10 | ✅ / ⚠️ / ❌ | 一句话说明 |
| 功能有效性 | E | X.X/10 | ✅ / ⚠️ / ❌ | 一句话说明 |
| 同类竞争 | C | 跳过(L<L>) / X.X/10 | ➖ / ✅ / ⚠️ / ❌ | 一句话说明 |
| 平台合规 | P | 跳过(L<L>) / X.X/10 | ➖ / ✅ / ⚠️ / ❌ | 一句话说明 |
| 文档一致性 | D | X.X/10 | ✅ / ⚠️ / ❌ | 一句话说明 |
| 代码质量 | Q | X.X/10 / 跳过(无代码) | ✅ / ⚠️ / ❌ / ➖ | 一句话说明 |
| **综合** | | **X.X/10** | ✅ / ⚠️ / ❌ | 加权平均 |

### 双维度评分（v2.0.0）

| 维度 | 结果 | 说明 |
|------|------|------|
| **Risk Level** | Low / Medium / High | 基于技能声明的权力评估 |
| **Audit Status** | Pass / Review / Warn / Fail | 基于审计结果评估 |
| **综合判定** | ✅ 可发布 / ⚠️ 修复后可发布 / ❌ 不可发布 | Risk-Status 矩阵交叉判定 |

**状态判定**：
- ✅ PASS：综合分 ≥ 7.0 且无 Critical（L1 只看 Critical）+ Audit Status = Pass
- ⚠️ WARN：综合分 5.0-6.9 或有 Important（L2/L3）+ Audit Status = Review/Warn
- ❌ FAIL：综合分 < 5.0 或有 Critical（T 维度一票否决）+ Audit Status = Fail

## Findings 列表

### 🚨 Critical（必须修复，阻止发布）

#### Finding #1 [维度-检查项] 简短标题
- **位置**: `<file>:<line>` 或具体文件路径
- **问题**: 详细描述问题
- **修复建议**: 具体到"改哪个文件的哪一段"
- **修复优先级**: P0（立即修复）

### ⚠️ Important（应该修复，影响质量）

#### Finding #2 [维度-检查项] 简短标题
- **位置**: `<file>:<line>`
- **问题**: 详细描述
- **修复建议**: 具体修复方案
- **修复优先级**: P1

### 💡 Minor（可选优化）

#### Finding #3 [维度-检查项] 简短标题
- **位置**: `<file>:<line>`
- **问题**: 详细描述
- **修复建议**: 具体修复方案
- **修复优先级**: P2/P3

### ℹ️ FYI（信息参考）

#### Finding #4 [维度-检查项] 简短标题
- **位置**: 位置说明
- **问题**: 信息描述
- **修复建议**: 无需行动 / 可选行动
- **修复优先级**: 无

## 修复建议优先级排序

| 优先级 | Finding # | 维度 | 问题简述 | 预计工作量 |
|--------|-----------|------|---------|-----------|
| P0 | #1 | T | 凭证泄露 | 5 分钟 |
| P1 | #2 | S | 行数超标 | 30 分钟 |
| P1 | #3 | P | Missing User Warnings | 10 分钟 |
| P2 | #4 | D | 引用断链 | 5 分钟 |
| P3 | #5 | Q | 类型注解 | 可选 |

## 维度详细评分依据

### S 结构合规（X.X/10）
- S1 frontmatter 必填: ✅/❌
- S2 name kebab-case: ✅/❌
- S3 description ≤200字符: ✅/❌
- ... (列出所有检查项)

### T 安全合规（X.X/10）
- T1 Layer 1 凭证: ✅/❌
- T2 Layer 2 路径: ✅/❌
- ... (列出所有检查项)

（其他维度同理）

## 交接建议

- 修复 P0/P1 后 → 建议用户手动发布到三平台
- 需重新设计 Skill 结构 → 建议用户重新创建技能
- 修复完成后 → 再次调用 skill-auditor 回归审计验证

---

*本报告由 skill-auditor v1.0.0 自动生成*
```

---

## 单维度审计报告模板

```markdown
# Skill 单维度审计报告

> 审计时间: YYYY-MM-DD HH:MM
> 审计模式: 单维度(T) / 单维度(T+Q)
> 被审计 Skill: <name> v<version>

## 审计范围

本次仅审计以下维度：T（安全合规）+ Q（代码质量）

## 评分

| 维度 | 评分 | 状态 |
|------|------|------|
| T 安全合规 | X.X/10 | ✅/⚠️/❌ |
| Q 代码质量 | X.X/10 | ✅/⚠️/❌ |

## Findings 列表

（同全量报告 Findings 格式，仅含 T 和 Q 维度的 Findings）

## 交接建议

- 如需全面审计 → 调用 skill-auditor 全量审计
- 修复 P0/P1 后 → 建议用户手动发布到三平台
```

---

## 批量审计报告模板

```markdown
# Skill 批量审计报告

> 审计时间: YYYY-MM-DD HH:MM
> 审计模式: 批量
> 被审计 Skills: <skill1>, <skill2>, <skill3>

## 横向对比表

| Skill | S | T | A | E | C | P | D | Q | 综合 | 状态 |
|-------|---|---|---|---|---|---|---|---|------|------|
| skill1 | 8.5 | 6.0 | 9.0 | 7.5 | 8.0 | 5.5 | 9.5 | 7.0 | 7.4 | ⚠️ |
| skill2 | 9.0 | 9.5 | 8.5 | 8.0 | 7.0 | 9.0 | 8.5 | 8.0 | 8.5 | ✅ |
| skill3 | 6.0 | 4.0 | 5.5 | 6.0 | 5.0 | 3.0 | 6.5 | 5.0 | 5.1 | ❌ |

## 排名

1. 🥇 skill2 — 8.5/10 ✅
2. 🥈 skill1 — 7.4/10 ⚠️
3. 🥉 skill3 — 5.1/10 ❌

## 各 Skill 主要问题

### skill1
- 🚨 Finding: config.local.json 含真实凭证（T 维度）
- ⚠️ Finding: README 缺用户警告（P 维度）

### skill2
- 💡 Finding: 类型注解缺失（Q 维度，Minor）

### skill3
- 🚨 Finding: curl 外发数据（T 维度）
- 🚨 Finding: SKILL.md 350 行超标（S 维度）
- ⚠️ Finding: 缺 Do NOT 范围（A 维度）

## 交接建议

- skill2 可直接发布
- skill1 修复 P0 后可发布
- skill3 需大改，建议用户重新设计技能
```

---

## 整改报告模板（Phase 4.5 输出）

```markdown
# Skill 整改报告

> 整改时间: YYYY-MM-DD HH:MM
> 被整改 Skill: <name> v<version>
> 成熟度等级: L<L>
> 授权来源: 用户在确认点2选择"进入整改模式"

## 整改摘要

| 指标 | 数量 |
|------|------|
| 审计报告 Findings 总数 | N |
| 本次整改修复 | X |
| 未修复（超出本次范围） | Y |
| 整改过程新增问题 | Z（如有） |

## 已修复列表

### ✅ Finding #1 [T-凭证泄露] config.local.json 含真实凭证
- **修复方式**: 删除 config.local.json，改为 references/config.json（placeholder）
- **验证结果**: ✅ T1 Layer 1 扫描 PASS
- **改动文件**: 删除 `references/config.local.json`，新建 `references/config.json`
- **改动行数**: +5 / -12

### ✅ Finding #2 [S-行数超标] SKILL.md 280 行
- **修复方式**: 将"详细示例"和"故障排除"下沉到 references/examples.md
- **验证结果**: ✅ S6 行数检查 PASS（180 行）
- **改动文件**: `SKILL.md`（删 100 行），新建 `references/examples.md`（+95 行）
- **改动行数**: +95 / -100

## 未修复列表

### ⏸️ Finding #4 [Q-类型注解] scripts/audit.py 缺类型注解
- **未修复原因**: Minor 级别，L2 阶段不强制修复
- **建议**: 下次迭代时补充

## 整改过程新增问题（如有）

### 🆕 Finding #6 [D-引用断链] references/examples.md 未在 SKILL.md 引用
- **原因**: 整改 Finding #2 时新建了 examples.md 但忘记在 SKILL.md 添加引用
- **严重性**: Important
- **处理**: 已在本次整改中修复（在 SKILL.md References 段添加引用）

## 整改结论

✅ 已修复 X/Y 个 Findings（P0 全修，P1 全修，P2 部分修）
⚠️ Z 个新增问题（已处理/待后续）

**下一步**: 进入回归审计（Phase 5）验证整改效果
```

---

## 整改后回归报告模板（Phase 5 输出）

```markdown
# Skill 整改后回归报告

> 回归时间: YYYY-MM-DD HH:MM
> 被审计 Skill: <name> v<version>
> 成熟度等级: L<L>
> 上次审计: YYYY-MM-DD HH:MM（整改前）
> 上次综合分: X.X → 本次综合分: Y.Y

## 回归摘要

| 指标 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 综合评分 | 7.4 | 8.5 | +1.1 ↑ |
| Critical 数 | 1 | 0 | -1 ✅ |
| Important 数 | 3 | 1 | -2 ✅ |
| Minor 数 | 2 | 2 | 0 → |

## Findings 变化

### ✅ 已修复（X 个）

#### Finding #1 [T-凭证泄露] → ✅ FIXED
- **上次**: 🚨 Critical
- **本次**: ✅ PASS（config.local.json 已删除）
- **验证**: T1 Layer 1 扫描通过

#### Finding #2 [S-行数超标] → ✅ FIXED
- **上次**: ⚠️ Important（280 行）
- **本次**: ✅ PASS（180 行）
- **验证**: S6 行数检查通过

### ❌ 未修复（Y 个）

#### Finding #4 [Q-类型注解] → ❌ UNFIXED
- **上次**: 💡 Minor
- **本次**: 💡 Minor（仍未修复）
- **原因**: L2 阶段 Minor 不强制

### 🆕 新增问题（Z 个，如有）

#### Finding #6 [D-引用断链] → 🆕 NEW
- **本次新发现**: references/examples.md 未在 SKILL.md 引用
- **严重性**: Important
- **状态**: 已在整改中修复（标记为 ✅ FIXED in 整改报告）

## 发布就绪判定（仅 L3）

<如 L3 阶段，显示以下判定：>

**发布前置条件**:
- ✅/❌ 回归审计综合分 ≥ 7.0（当前 Y.Y）
- ✅/❌ 无 Critical 未修复
- ✅/❌ 无 Important 未修复（L3 要求）
- ✅/❌ 成熟度 = L3

**判定**: ✅ 发布就绪 / ❌ 未达发布标准

## 下一步建议

<如 L3 且发布就绪：>
- 可在确认点3选择"发布" → 进入确认点4发布确认

<如 L1/L2 或未达发布标准：>
- 继续迭代 → 修复后再次调用 skill-auditor 回归审计
- 升级成熟度 → 补全 references/CHANGELOG 等，重新做 L3 全量审计
```

---

## Finding 编号规则

- 全量审计：按严重性 → 维度 → 发现顺序编号（#1, #2, #3...）
- 单维度审计：同上，但只含指定维度的 Findings
- 批量审计：每个 Skill 独立编号（skill1-#1, skill1-#2, skill2-#1...）
- 回归审计：保留上次编号 + 新增编号（#1 修复, #2 未修复, #6 新增）

## 修复优先级定义

| 优先级 | 含义 | 行动 |
|--------|------|------|
| P0 | 立即修复，阻止发布 | Critical 级别 |
| P1 | 应该修复，影响质量 | Important 级别 |
| P2 | 建议修复，提升质量 | Minor 级别 |
| P3 | 可选优化 | Minor 级别（低收益） |
| 无 | 无需行动 | FYI 级别 |
