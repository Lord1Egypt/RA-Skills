---
name: spm-v4
description: "Super Project Manager v4 — production-grade AI coding project management engine. WBS ledger, 6-phase state machine, SHA-256 attestation, 3-domain event store, YAML security gate, sub-agent orchestration."
metadata: {"openclaw": {"emoji": "🚀", "requires": {"anyBins": ["node", "npm"]}}}
---

# SPM V4 — Super Project Manager

> **SPM V4 的唯一目标：在结构化任务台账 + 完整性验证的约束下，最大化 AI agent 的项目交付质量。**
>
> Maximize project delivery quality under structured task ledger + integrity verification constraint.

## When to Use

- **启动新项目** — 需要一个可追踪的工作分解结构
- **跨会话开发** — 需要断点恢复、进度可见
- **子代理编排** — 多 agent 协作，需统一的任务管理
- **审计要求高** — 需要完整的 job dispatch + quality gate 记录

**When NOT to use:**
- 单文件修改、修 typo
- 一次性查询/搜索
- 不需要追踪的临时任务

---

## Overview

SPM V4 管理项目开发的完整生命周期：

```
Context Init → Requirement → Planning → Execution → Quality → Delivery
     ↑                                                          |
     └────────────────── 迭代循环 ──────────────────────────────┘
```

核心机制：
- **WBS 台账** — `docs/spm/ledger.md`，单数据源，每任务有 Context Brief + Exit Criteria + Evidence
- **哈希认证** — 每次台账变更后 SHA-256 锁定，防篡改，Merkle 树增量验证
- **事件审计** — 子代理调度、质量门禁、哈希变更全部记入三域 Event Store
- **安全门** — 命令三级分类（safe/risky/dangerous），YAML 策略可配置
- **子代理 Prompt** — 4 种角色 prompt（implementer / spec-reviewer / quality-reviewer / plan-reviewer）

---

## Agent Instructions

### Step 0: 判断是否使用 SPM

用户提到以下关键词 → 启动 SPM：
- "项目"、"工程"、"开发"、"实现"
- 需要多步骤、多文件的任务
- 明确要求追踪、管理、计划

其他情况 → 不用 SPM，直接回答。

---

### Step 1: 初始化项目

用户说"开始项目 X"或"用 SPM 管理项目 X"时：

1. 创建项目目录结构：

```
mkdir -p docs/spm
mkdir -p src tests .spm
```

2. 在 `docs/spm/ledger.md` 创建 WBS 台账模板：

```markdown
# SPM WBS Ledger — [项目名称]

## WB-001: [任务描述]
- **Status**: todo
- **Dependencies**: none
- **Context**: [一句话上下文 + 涉及文件 + 约束]
- **Exit Criteria**: [可验证的完成条件]
- **Evidence**:
```

3. 哈希认证：

```bash
# 用 SHA-256 锁定初始台账
# 在目录下创建 .spm/wbs-attestation 文件
# 内容格式：<sha256_hash> <timestamp>
echo "$(shasum -a 256 docs/spm/ledger.md | awk '{print $1}') $(date -u +%s)" > .spm/wbs-attestation
```

4. 回复："✅ SPM V4 已初始化。WBS 台账已创建并认证。"

---

### Step 2: 任务分解

帮助用户把需求分解为可执行的 WBS 任务：

**任务粒度规则**：每个任务 2-5 分钟，不超过 30 分钟（5 个文件修改）。

**Context Brief 模板**：

```
Context Brief: [任务标题]

目标: [一句话]
前置产物: [依赖任务完成了什么]
涉及文件:
- 新建: [文件路径]
- 修改: [文件路径]
关键约束: [技术约束、算法选择、风格要求]
验收要点: [具体可验证的标准]
```

**Exit Criteria 必须可验证**：
- ✅ `curl 测试返回 200`
- ✅ `npm test 5 passed`
- ❌ "代码写好了"

---

### Step 3: 开发循环

这是最核心的步骤，每次做一个任务：

```
为每个任务：

  1. 选择 WBS 中的一个 todo 任务
  2. 更新 WBS: Status: doing
  3. 哈希认证
  4. 执行任务（写代码/配置/测试）
  5. 验证输出（运行命令确认）
  6. 更新 WBS: Status: done。Evidence 填入验证命令输出
  7. 哈希认证
  8. 进入下一个任务
```

**每次台账变更后必须认证**：

```bash
hash=$(shasum -a 256 docs/spm/ledger.md | awk '{print $1}')
echo "$hash $(date -u +%s)" > .spm/wbs-attestation
```

**每次任务前验证完整性**：

```bash
stored=$(cat .spm/wbs-attestation | awk '{print $1}')
actual=$(shasum -a 256 docs/spm/ledger.md | awk '{print $1}')
if [ "$stored" != "$actual" ]; then
  echo "⚠️ WBS 已被篡改！检查 docs/spm/ledger.md"
fi
```

---

### Step 4: 子代理调度

当任务可独立执行时，使用 `sessions_spawn` 调度子代理：

```markdown
[Subagent prompt — implementer.md 模板]

你是一个实现者，负责完成以下任务。

WBS 上下文:
- 任务 ID: WB-003
- 上下文: {从 WBS 读取 Context Brief}
- 前置产物: {依赖任务的文件/结果}

你的输出:
1. 修改的文件列表
2. 关键代码说明
3. 验证命令及输出
```

子代理返回后：
1. 检查输出是否满足 Exit Criteria
2. 更新 WBS Status: done + Evidence
3. 哈希认证

**4 种子代理角色：**

| Prompt | 协作模式 |
|--------|----------|
| `implementer` | 接收任务描述，返回实现代码 + 验证结果 |
| `spec-reviewer` | 审查设计文档，确认符合需求 |
| `quality-reviewer` | 审查代码质量，检查测试覆盖 |
| `plan-reviewer` | 审查 WBS 计划完整性 |

---

### Step 5: 质量门禁

完成所有任务后，执行 Quality Gate：

```markdown
检查清单（5 项）：
□ 所有 done 任务有 Evidence
□ Evidence 匹配 Exit Criteria
□ 无循环依赖
□ 所有依赖任务已 done（或 skipped）
□ 哈希认证匹配
```

**任何一项不通过 → 先修复再继续。**

---

### Step 6: 交付

```markdown
最终检查：
□ quality-check 通过
□ WBS attestation 匹配
□ 所有任务 done
□ 验证命令输出作为证据存档
```

交付后更新 WBS 台账添加总结行：

```markdown
## Delivery Summary
- 项目: [名称]
- 任务数: [N]
- 完成时间: [日期]
```

---

## WBS 台账格式标准

```
# SPM WBS Ledger — <项目名称>

## <WB-NNN>: <任务描述>
- **Status**: todo | doing | done | blocked | skipped
- **Dependencies**: <WB-XXX, WB-YYY> 或 none
- **Context**: <冷启动上下文，必须自包含>
- **Exit Criteria**: <可验证的完成条件>
- **Evidence**: <验证命令输出>
```

**铁律**：
- `done` 必须填写 `Evidence`
- `blocked` 必须写明原因
- `skipped` 保留原行（不删除）
- 不允许修改已完成任务的 Evidence

---

## 安全门（可选配置）

在项目目录创建 `config/security-policy.yaml`：

```yaml
rules:
  - pattern: "^rm -rf /"
    level: dangerous
    action: block
  - pattern: "^git push --force"
    level: risky
    action: warn
  - pattern: "^curl .*\\| sh$"
    level: risky
    action: warn
```

执行危险命令前检查：

```bash
# 对每条待执行命令匹配规则
# dangerous → 阻止并提示用户
# risky → 警告并确认
# safe → 放行
```

---

## 事件审计（可选）

使用 `docs/spm/events/` 目录记录结构化事件：

```
events/
├── audit.jsonl      # 子代理调度记录
├── integrity.jsonl   # 哈希认证记录
└── quality.jsonl     # 质量门禁记录
```

每行一个 JSON 事件：

```json
{"type":"subagent_dispatch","timestamp":"...","task":"WB-003","model":"sensenova/deepseek-v4-flash","result":"DONE"}
{"type":"wbs_attestation","timestamp":"...","hash":"a3f8c2..."}
{"type":"quality_gate","timestamp":"...","tasks":3,"passed":true}
```

---

## Examples

```
帮我用 SPM 管理一个 REST API 项目
用 SPM 实现用户认证模块
SPM 初始化：消息队列
启动一个新项目，用 SPM 追踪进度
```

## Related

- MoA（Mixture of Agents）Skill — 多模型并行分析，为 SPM 的复杂决策提供参考
- OpenClaw SPM Shell v3 — 上一代 Shell 版本