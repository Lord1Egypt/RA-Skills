# 粘连点（Adhesion Point）机制

> **v1.25.0 新增**。粘连点是调用链中无法由 skill 自动化的缺口标记。

---

## 什么是粘连点

粘连点是调用链中一个特殊类型的步骤（`type: "adhesion"`），标记该位置无法由任何已安装 skill 自动完成。它不会阻断调用链，而是提供三种解决方案供 LLM 选择。

### 什么时候产生粘连点

| 场景 | 触发条件 | 行为 |
|------|---------|------|
| **链修正** | 执行链时发现步骤与真实 skill 不符，修正后仍报错 | 在该步骤位置打粘连点 |
| **链缺口** | 规划链时某步骤无对应 skill 可用 | 在缺失位置插入粘连点 |
| **流程缺口分析** | 规划阶段发现语义/流程/决策缺口 | 在天然断裂处打粘连点（见下方规则） |

### 三个核心原则

1. **链不断** — 粘连点标记不阻断调用链执行，LLM 按方案继续
2. **连接器，非替代品** — 粘连点是两个 skill 步骤之间的连接器，不是 skill 步骤的替代品。**禁止粘连点连粘连点**，连续缺口合并为一个粘连点
3. **不创建 Skill** — 解决方案是步骤描述级别，产生的脚本/产出物归数据目录管理
4. **自愈** — 每次使用含粘连点的链，主动检查是否有新 skill 可填补

---

## 缺口分析规则（规划阶段）

在创建调用链的步骤 3→4 之间插入流程缺口分析，按以下规则判断：

### 三种真实缺口

| 缺口类型 | 判断依据 | 应打粘连点？ | 方案优先级 |
|---------|---------|------------|-----------|
| **语义缺口** | Skill A 输出格式/内容 ≠ Skill B 期望输入 | ✅ 数据转换步骤 | hybrid |
| **流程缺口** | 用户任务中的某个环节无任何 skill 覆盖 | ✅ 补充缺失步骤 | auto / manual |
| **决策缺口** | 需要人工审批、判断、签字的节点 | ✅ 人工审批节点 | manual |
| **自然衔接** | Skill A 输出可直接作为 Skill B 输入 | ❌ 不打 | — |

### 禁止行为

| 禁令 | 说明 |
|------|------|
| ❌ 不要制造缺口 | 自然衔接的 skill 不打粘连点 |
| ❌ 不要粘连点连粘连点 | **连续缺口合并为一个粘连点** |
| ❌ 不要替代 skill | 能用 skill 完成的直接用 skill |
| ❌ 不要过度粘连 | 粘连点数量应远少于 skill 步骤数 |

### 判定示例

```text
用户需求：分析代码 → 生成报告 → 发送邮件

✓ 正确：
  步骤1: code-analysis (skill)        — 分析代码
  步骤2: report-generation (adhesion) — JSON→Markdown 语义缺口
  步骤3: email-send (skill)           — 发送邮件

✓ 连续缺口合并：
  步骤1: code-analysis (skill)
  → 步骤2: data-cleanup (缺失) — 两个连续缺失合并为一个粘连点
  → 步骤3: transform (缺失)    — 🔴 禁止！应为：
  步骤2: data-pipeline (adhesion, hybrid) — 覆盖清洗+转换的完整缺口
  步骤3: email-send (skill)

✗ 过度粘连：
  步骤1: code-analysis (skill)
  步骤2: report-generation (adhesion)  — ❌ 如果有 report skill 就不该打
  步骤3: email-send (skill)

✗ 粘连点连粘连点（禁止）：
  步骤1: code-analysis (skill)
  步骤2: manual-review (adhesion)      — ❌ 连续两个粘连点
  步骤3: data-transform (adhesion)     — ❌ 应合并为一个
  步骤4: email-send (skill)
```

---

## 三种解决方案

### ① 纯手工（manual）

LLM 直接手动执行步骤，不依赖脚本或新 skill。

```json
{"mode": "manual", "description": "人工审核报告", "constraints": "需关注数据准确性"}
```

**适用场景**：一次性、高度灵活的判断任务。

### ② 脚本化（auto）

通过自调用脚本工具执行，产生的脚本入数据目录管理。

```json
{"mode": "auto", "tool_name": "report-verify", "script_path": "scripts/verify.sh"}
```

**适用场景**：可标准化、重复执行的任务。

### ③ 混合（hybrid）

LLM 描述流程步骤 + 约束 + 自调用工具协同执行。

```json
{
  "mode": "hybrid",
  "llm_steps": "LLM 阅读报告并给出审核意见",
  "tool_steps": "脚本验证报告中的数字准确性",
  "integration": "LLM 分析文本，工具验证数字"
}
```

**适用场景**：需要智能判断 + 自动化执行的复合任务。

---

## 执行优先级

AI 执行粘连点步骤时，按以下优先级选择方案：

1. **hybrid** — 最优先，组合 LLM + 工具的最大能力
2. **auto** — 次优先，能脚本化就不手动
3. **manual** — 兜底，LLM 直接执行

---

## 自愈机制

每次加载含粘连点的调用链时，AI 执行自愈检查：

```
1. 扫描 skill 库（skill-sub 所在目录的兄弟目录）
2. 对每个粘连点，用 adhesion.reason 关键词搜索 SKILL.md
3. 找到匹配 → 将 adhesion 步骤升级为 skill 步骤
   - type 改为 "skill"
   - 填充 skill_name / action
   - 原 adhesion.solutions 写入 notes
4. 未找到 → 按原有 3 方案执行
```

也可手动触发：`python chain_manager.py check-gaps`

---

## 与 chain_executor 集成

`chain_executor.py` 在执行计划中渲染粘连点步骤：

```text
### 步骤 3.5: 报告审核
⚠️ 粘连点 — 原因：缺少对应 skill 的自动化能力
  方案1 [混合]：LLM 审核 + 脚本验证
    LLM: 阅读报告并给出审核意见
    工具: 脚本验证报告中的数字准确性
  方案2 [纯手工]：完全由 LLM 手工审核报告
```

---

## 数据目录

粘连点相关的脚本和产出物存放在以下位置，遵循 skill-sub 的数据目录规范：

```
.standardization/skill-sub/data/
├── outputs/        # 脚本化方案产生的输出
└── scripts/        # 自调用工具脚本（auto/hybrid 模式）
```
