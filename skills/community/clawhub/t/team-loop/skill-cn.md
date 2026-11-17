---
name: team-loop
description: >
  目标驱动的自主任务循环引擎。/goal 触发，MA agent团队自主执行
  规划→执行→验证→记忆→再规划完整循环。人只定义目标，不进循环。
  适用于覆盖率提升、代码迁移、批量重构、测试补全等可量化目标。
metadata:
  author: iClaw & iFeel
  version: "2.3"
---

# team-loop — 自主任务循环引擎

## 概述

将 MA agent 团队从人驱瀑布交付升级为目标驱自主循环。

- **输入：** `/goal <可量化目标>`
- **流程：** 初始化 → 拆解 KR → 调度 agent → 对抗验证 → 沉淀记忆 → 下一轮
- **输出：** 增量交付物 + 状态快照 + 审计报告 + token 账单
- **人只介入：** 目标设定、异常终止、预算追认

**接受条件：** 目标必须可量化。"提高代码质量"→拒绝。"分支覆盖率≥50%"→接受。

**核心原则：**
1. 人只定义目标，不进循环
2. 不同 agent / 不同模型 / 不同验证手段
3. 状态在磁盘，每轮 fresh context
4. 基础设施先行——日志、编号、异常捕捉在业务代码之前到位

---

## 触发方式

```
/goal <可量化目标> [预算≤¥N] [max_rounds=N]
```

示例：
```
/goal handler层分支覆盖率 0%→≥50%，预算≤¥20
/goal old-pkg → new-pkg 迁移，全量测试通过
/goal src/handlers/ 补全测试，覆盖率≥80%
```

---

## 角色体系

6 个 agent，复用 MA 现有角色，零新增。

| Agent | 角色 | 职责 | 交付物 | 红线 |
|-------|------|------|--------|------|
| **main** | GoalAgent + PlannerAgent + LoopController + Monitor | 解析目标、拆解KR、调度判决、终止判定、进度聚合、token账单 | StandardGoal, TaskDAG, StateSnapshot, RoundSummary, TokenReport | GoalAgent不读项目文件；PlannerAgent必读rdf/；LoopController/Monitor纯程序化不调LLM |
| **coder** | ExecutorAgent | TDD三步执行KR，产出代码/测试 | TaskResult + commit | 不审查自己代码 |
| **reviewer** | CriticAgent (correctness) | 静态审查代码正确性，不运行代码 | Verdict | 不运行代码 |
| **tester** | CriticAgent (completeness) | 动态执行测试、测量覆盖率、flaky检测 | Verdict + CoverageReport | 不审查代码逻辑 |
| **auditor** | CriticAgent (robustness) | 审计审查者质量，过checklist | Verdict | 永不执行代码、永不修改文件 |
| **publicist** | MemoryAgent | 沉淀经验到RDF记忆库 | MemoryEntry | 只写不执行 |

### 独立性红线

| Agent | 不能做 | 原因 |
|-------|--------|------|
| coder | 审查自己代码 | 自评偏见 |
| reviewer | 运行代码 | 运行=参与=失去独立 |
| tester | 审查代码逻辑 | reviewer职责 |
| auditor | 执行代码、修改文件 | 执行=参与=自己评自己 |

---

## 知识管理：RDF

项目知识存于被管理项目的 `rdf/` 目录。agent 用 `read`/`write` 工具直接读写 Turtle (.ttl) 格式。RDF只存索引，agent 用索引定位后直接 `read` 源码。如项目无 rdf/，PlannerAgent 首次扫描源码生成。

### 目录布局

```
{项目根目录}/
├── src/                          ← 源码 [coder修改]
├── tests/                        ← 测试 [coder修改]
├── rdf/
│   ├── ast/                      ← 源码索引 (自动扫描)
│   │   ├── index.ttl             ← 文件→函数→类→行号
│   │   ├── runtime-ctx.ttl       ← ctx结构、fixture、import
│   │   └── examples.ttl          ← 测试范例
│   └── business/                 ← 业务知识+执行记忆 (agent沉淀)
│       ├── patterns.ttl          ← 已验证的通用模式
│       ├── anti-patterns.ttl     ← 失败模式库
│       └── memory.ttl            ← KR执行结果+经验
├── .team-loop/                   ← 过程状态 (不进git)
│   ├── STATE.md
│   ├── config.json
│   ├── HEARTBEAT
│   ├── CRASH.log
│   ├── adr/                      ← ADR-{N}.md
│   ├── cr/                       ← CR-{N}.json
│   ├── patches/                  ← {interaction_id}.patch
│   ├── state-snapshots/          ← {round}.json
│   └── reports/
├── logs/                         ← 日志 (不进git)
│   └── {loop_id}/R{round}/
│       ├── {agent}.jsonl
│       ├── {agent}.log
│       ├── metrics.json
│       └── round-summary.md
├── docs/ reference/ examples/ scripts/
├── Makefile README.md .gitignore
└── .team-loop/STOP               ← 空文件触发安全停止
```

### 读写规则

| 角色 | 何时 | 读什么 | 何时 | 写什么 |
|------|------|--------|------|--------|
| **PlannerAgent** (main) | seq 2 拆解KR前 | rdf/ast/* + rdf/business/* | — | — |
| **coder** | seq 5 执行KR时 | rdf/ast/* + rdf/business/anti-patterns.ttl | — | 源码、测试 |
| **publicist** | — | — | seq 11 记录记忆 | rdf/business/memory.ttl；新模式/反模式→patterns.ttl/anti-patterns.ttl |

### 谓词汇总

前缀规则：`{项目名}-ast:` / `{项目名}-business:`

| 域 | 谓词 | 说明 |
|----|------|------|
| ast | hasFunction, hasClass, hasImport, hasFixture | 文件→符号 |
| ast | name, signature, source, scope | 符号属性 |
| ast | fields, exampleFile | 运行时上下文 |
| ast | module, function, approach, file | 测试范例 |
| business | memoryOf, round, vetoBy | KR记忆 |
| business | outcome → Passed \| Failed \| Skipped | 执行结果 |
| business | lessons, description, example, solution | 经验说明 |
| business | verifiedIn, seenIn → blank node `{round N}` | 验证/出现轮次 |

**MemoryEntry 示例 (publicist 写作参考):**
```turtle
<kr:K2.1_R3>
    pyov-business:memoryOf "ontology_handler.py 覆盖率测试" ;
    pyov-business:outcome pyov-business:Passed ;
    pyov-business:lessons "handle_tree 的 ctx 必须包含 children 字段" ;
    pyov-business:round 3 .
```

---

## Git 协作（轻量checkout）

不使用 worktree。每轮 coder 在当前分支直接开发、提交。

**提交规范：** coder commit message 格式：
```
[KR-{id}] {简述} | round={N} | interaction_id={id}
```

**auditor 审查：** 审查入口为本轮 commit 的 `git diff HEAD~1`。

**回滚：** KR 失败→`git revert` 本轮 commit。patch 由 main 在 revert 时生成备份到 `.team-loop/patches/{interaction_id}.patch`。

| Agent | Git能力 |
|-------|---------|
| main | init, commit, tag (tag: `R{round}-{passed\|failed}`)，生成patch |
| coder | 在当前分支开发、commit |
| reviewer | 只读diff |
| tester | checkout到目标commit后pytest |
| auditor | `git diff HEAD~1` 审查本轮变更（若coder多commit则`git diff HEAD~N..HEAD`） |
| publicist | 无 |

---

## SOP 主循环 (11步RSF)

### 初始化 (seq 0)

main (LoopController) 在首次启动时执行一次性初始化：
1. 生成 `loop_id`: `manual-{timestamp}-{nonce}-L`
2. 生成根 `interaction_id`: `manual-{timestamp}-{nonce}`
3. 创建目录: `.team-loop/` 及子目录、`logs/{loop_id}/`
4. 写入 `config.json`、`STATE.md`
5. 启动看门狗进程 (独立进程，心跳间隔30s，超时阈值60s)
6. 如项目无 `rdf/`：PlannerAgent 扫描 src/ tests/ 生成 `rdf/ast/` 索引
7. 调用 `/status` 记录基线余额

### RSF

```json
{
  "format": "roles-steps-flows",
  "version": "2.3",
  "description": "单轮KR执行标准流程。每轮1个就绪KR。",
  "roles": {
    "items": [
      {"id": "main", "description": "GoalAgent(LLM)+PlannerAgent(LLM)+LoopController(程序化)+Monitor(程序化)"},
      {"id": "coder", "description": "ExecutorAgent，TDD三步"},
      {"id": "reviewer", "description": "correctness critic，静态审查，不运行代码"},
      {"id": "tester", "description": "completeness critic，动态验证，隔离环境(独立子进程)"},
      {"id": "auditor", "description": "robustness critic，审计审查者，过13项checklist，永不执行永不修改"},
      {"id": "publicist", "description": "memory agent，沉淀RDF记忆"}
    ]
  },
  "steps": {
    "items": [
      {"seq": 1, "description": "解析目标→StandardGoal", "cells": {"main": {"task": "解析目标", "description": "GoalAgent(LLM): 自然语言→StandardGoal。不读项目文件", "in": [], "out": ["StandardGoal"]}}},
      {"seq": 2, "description": "读知识库→拆解三层KR", "cells": {"main": {"task": "规划", "description": "PlannerAgent(LLM): 读rdf/→拆解KR→生成TaskDAG+TokenEstimate。有技术选型→写ADR", "in": ["StandardGoal","MemoryEntry"], "out": ["TaskDAG","TokenEstimate"]}}},
      {"seq": 3, "description": "取就绪KR+预算检查", "cells": {"main": {"task": "下发准备", "description": "LoopController(程序化): 取最高priority就绪KR→装配TaskUnit。调用/status+预算守卫→产出StateSnapshot(t0)", "in": ["TaskDAG","TokenEstimate","retry|next_kr"], "out": ["TaskUnit","StateSnapshot(t0)"]}}},
      {"seq": 4, "description": "下发coder [超时300s]", "cells": {"main": {"task": "下发", "description": "sessions_spawn下发TaskUnit给coder", "in": ["TaskUnit"], "out": ["TaskUnit"]}}},
      {"seq": 5, "description": "coder TDD执行", "cells": {"coder": {"task": "执行KR", "description": "Step1:写测试→验证可运行。Step2:若KR要求实现则写最少代码(补测已有代码则跳过)。Step3:全量回归→产出TaskResult", "in": ["TaskUnit"], "out": ["TaskResult"]}}},
      {"seq": 6, "description": "收集→并行分发critic [超时120s]", "cells": {"main": {"task": "分发", "description": "Monitor(程序化):收TaskResult→sessions_spawn并行分发reviewer+tester", "in": ["TaskResult"], "out": ["TaskResult"]}}},
      {"seq": 7, "description": "并行验证", "cells": {
        "reviewer": {"task": "正确性审查", "description": "静态读diff:spec一致性/逻辑边界/API误用/import幻觉/兼容性/测试死刑→产出Verdict", "in": ["TaskResult"], "out": ["Verdict"]},
        "tester": {"task": "完整性验证", "description": "隔离环境(独立子进程):pytest收集+执行→coverage对比基线→全量回归→flaky检测(新测试连跑3次结果一致)→产出Verdict+CoverageReport", "in": ["TaskResult"], "out": ["Verdict","CoverageReport"]}
      }},
      {"seq": 8, "description": "收集判决→分发auditor [超时120s]", "cells": {"main": {"task": "收集+分发auditor", "description": "Monitor(程序化):收reviewer.Verdict+tester.Verdict+CoverageReport→sessions_spawn分发auditor(附TaskResult+双Verdict+CoverageReport)", "in": ["Verdict","Verdict","CoverageReport","TaskResult"], "out": ["TaskResult","Verdict","Verdict","CoverageReport"]}}},
      {"seq": 9, "description": "auditor审计", "cells": {"auditor": {"task": "健壮性审计", "description": "过13项checklist→产出Verdict。如发现ADR遗漏可中断当前KR通知main", "in": ["TaskResult","Verdict","Verdict","CoverageReport"], "out": ["Verdict"]}}},
      {"seq": 10, "description": "收集auditor→裁决+终止判断", "cells": {"main": {"task": "裁决", "description": "LoopController(程序化):收auditor.Verdict。汇总3票→≥2passed通过；1passed→失败(可重试≤3次则回seq3)；0→跳过。检查终止条件。产出Decision+TokenReport+StateSnapshot(t1)+RoundSummary", "in": ["Verdict"], "out": ["Decision","TokenReport","StateSnapshot(t1)","RoundSummary","TaskResult","retry|next_kr"]}}},
      {"seq": 11, "description": "记忆沉淀", "cells": {"publicist": {"task": "记录记忆", "description": "沉淀结果到rdf/business/:通过→记录成功模式；失败→记录否决原因+改进建议", "in": ["TaskResult","Decision"], "out": ["MemoryEntry"]}}}
    ]
  },
  "flows": {
    "items": [
      {"id":"f1","type":"sync","from":{"role":"main","seq":1},"to":{"role":"main","seq":2},"what":"StandardGoal"},
      {"id":"f2","type":"sync","from":{"role":"main","seq":2},"to":{"role":"main","seq":3},"what":"TaskDAG+TokenEstimate"},
      {"id":"f3","type":"sync","from":{"role":"main","seq":3},"to":{"role":"main","seq":4},"what":"TaskUnit"},
      {"id":"f4","type":"async","from":{"role":"main","seq":4},"to":{"role":"coder","seq":5},"what":"TaskUnit","description":"[超时300s]"},
      {"id":"f5","type":"async","from":{"role":"coder","seq":5},"to":{"role":"main","seq":6},"what":"TaskResult"},
      {"id":"f6","type":"async","from":{"role":"main","seq":6},"to":{"role":"reviewer","seq":7},"what":"TaskResult","description":"[超时120s]"},
      {"id":"f7","type":"async","from":{"role":"main","seq":6},"to":{"role":"tester","seq":7},"what":"TaskResult","description":"[超时120s]"},
      {"id":"f8","type":"async","from":{"role":"reviewer","seq":7},"to":{"role":"main","seq":8},"what":"Verdict"},
      {"id":"f9","type":"async","from":{"role":"tester","seq":7},"to":{"role":"main","seq":8},"what":"Verdict+CoverageReport"},
      {"id":"f10","type":"async","from":{"role":"main","seq":8},"to":{"role":"auditor","seq":9},"what":"TaskResult+Verdict(×2)+CoverageReport","description":"[超时120s]"},
      {"id":"f11","type":"async","from":{"role":"auditor","seq":9},"to":{"role":"main","seq":10},"what":"Verdict"},
      {"id":"f12","type":"async","from":{"role":"main","seq":10},"to":{"role":"publicist","seq":11},"what":"TaskResult+Decision"},
      {"id":"f13","type":"async","from":{"role":"publicist","seq":11},"to":{"role":"main","seq":2},"what":"MemoryEntry","description":"[反馈流，下轮PlannerAgent查询]"},
      {"id":"fR","type":"sync","from":{"role":"main","seq":10},"to":{"role":"main","seq":3},"what":"retry|next_kr","description":"[循环: next_kr或retry→回seq3取下一KR或重试]"}

    ]
  }
}
```

### RSF 语义规则

- **并行:** 同一seq多cell → 并行
- **串行:** 不同seq默认串行；`from.seq > to.seq`=反馈流
- **sync:** 同角色内，阻塞等待
- **async:** 跨角色 (sessions_spawn)，fire-and-forget
- **校验:** flow `(A→B, what=X)` 需满足 `X ∈ A.out ∩ B.in`
- **标注:** `[超时Ns]` `[条件]`

---

## KR 三层递进

| 层 | 目标 | 验证 | 失败处理 |
|----|------|------|---------|
| 🔴 K1 基础层 | 证明test infra可用 | 1个最小可行测试跑通 | 连续3轮失败→FATAL |
| 🟡 K2 覆盖层 | 逐文件提升覆盖率 | pytest+cov增量 | 可重试≤3次→仍失败跳过 |
| 🟢 K3 质量层 | 无回归 | 全量测试100%通过 | 回滚，记录根因 |

**示例：**
```
O: handler层分支覆盖率 0%→≥50%
K1.1: 1个HTTP测试可运行
K2.1-2.3: 逐文件覆盖≥50%
K3.1: 全量回归通过，无flaky
```

### 重试规则

- KR 失败后重试 max 3 次
- 重试时 planner 必须重新读 rdf/ 获取本次失败记忆
- 同一 KR 重试超过 3 次 → 标记 skipped，记录根因到 memory.ttl
- K1 层失败不重试——连续 3 轮失败直接 FATAL
- 重试不改 interaction_id，追加 round 递增

---

## 三视角对抗验证

### reviewer — 正确性审查（不运行代码）

审查项: spec一致性 / 逻辑边界 / API误用 / import幻觉 / 兼容性 / 「测试死刑」检查

### tester — 完整性验证（动态执行，隔离环境）

验证项: pytest收集+执行(独立子进程) / coverage增量 / 断言有效性 / 全量回归 / flaky检测(新测试连跑3次结果一致)

### auditor — 健壮性审计（永不执行代码，永不修改文件）

13项checklist：
1. 错误处理完整性 2. 资源管理 3. 注入安全 4. reviewer审查完整性 5. tester验证完整性 6. 交接物Schema合规(含interaction_id) 7. CR记录完整性 8. 日志可追溯 9. interaction_id一致性 10. 流程合规 11. 模型合规(critic与coder不同模型) 12. 补丁完整性 13. 自检(不执行、不修改)

### 2/3 裁决

| 票数 | 结果 | 后续 |
|------|------|------|
| 3 passed | 通过 | 继续下一KR |
| 2 passed | 通过 | 记录+反对意见 |
| 1 passed | 失败 | 可重试(≤3次)→回seq3，不可→跳过 |
| 0 passed | 失败 | 记录根因，跳过 |

---

## 停止条件（按优先级）

| # | 条件 | 结果 |
|----|------|------|
| 1 | 所有KR completed | SUCCESS |
| 2 | K1层连续3轮失败 | FATAL |
| 3 | agent超时重试耗尽 | FATAL |
| 4 | 所有剩余KR依赖永不可满足 | FATAL |
| 5 | critic spawn连续3次失败 | FATAL |
| 6 | 磁盘满(ENOSPC) | FATAL |
| 7 | 预估下轮消耗 > 剩余预算 | BUDGET |
| 8 | 轮次 ≥ max_rounds | MAX_ROUNDS |
| 9 | 连续3轮覆盖率无提升 | STAGNATION |
| 10 | `.team-loop/STOP`存在 | MANUAL_STOP |
| 11 | 日志逃逸(M < N) | FATAL |
| 12 | 看门狗检测主控崩溃 | FATAL |

---

## 配置与初始化

### config.json

```json
{
  "budget_yuan": 20,
  "token_rate": {"yuan_per_1k_tokens": 0.002},
  "max_rounds": 50,
  "max_retries": 3,
  "timeouts": {"coder": 300, "critic": 120, "auditor": 120},
  "watchdog": {"heartbeat_interval_s": 30, "timeout_s": 60},
  "models": {
    "coder": "deepseek-v4-pro",
    "reviewer": "glm-5.2",
    "tester": "glm-5.2",
    "auditor": "glm-5.2",
    "publicist": "glm-5.2",
    "main_llm": "deepseek-v4-pro"
  },
  "coverage_thresholds": {"line": 0.80, "branch": 0.70}
}
```

### STATE.md

```markdown
# STATE.md
## 状态
running | terminated

## 当前 loop
- loop_id: {id}
- interaction_id: {id}
- 开始时间: {ISO8601}
- round: {N}
- KR状态: [{"kr_id":"K1.1","status":"completed|failed|skipped|pending"}]

## 累计
- 总轮次: {N} | 总耗时: {小时}
- 总token: in={N}/out={N} | 总费用: ¥{N}

## 停止原因 (loop结束时)
{SUCCESS|FATAL|BUDGET|...}
```

### Token ⇔ ¥ 换算

- `token_rate.yuan_per_1k_tokens` 定义换算率
- 每轮 /status 后检查：`预估下轮消耗(tokens) × rate ≤ 剩余预算(¥)`
- TokenReport 含 `cost_yuan` 字段

---

## 交付物模板

### 每轮循环产出清单

| 交付物 | 责任人 | 格式 | 存储位置 |
|--------|--------|------|---------|
| StateSnapshot (t0/t1) | main | JSON | `.team-loop/state-snapshots/{round}.json` |
| TokenReport | main | JSON | `.team-loop/reports/token-R{round}.json` |
| RoundSummary | main | Markdown | `.team-loop/reports/R{round}-summary.md` |
| TaskUnit | main | JSON | sessions_spawn传递 |
| TaskResult | coder | JSON | sessions_spawn返回 |
| Verdict×3 | reviewer,tester,auditor | JSON | sessions_spawn返回 |
| CoverageReport | tester | JSON | `logs/{loop_id}/R{round}/metrics.json` |
| CR | main | JSON | `.team-loop/cr/CR-{N}.json` |
| Patch | main | unified diff | `.team-loop/patches/{interaction_id}.patch` |
| MemoryEntry | publicist | Turtle | `rdf/business/memory.ttl` 追加 |
| ADR | main | Markdown | `.team-loop/adr/ADR-{N}.md` |
| SessionSummary | main | Markdown | `.team-loop/reports/session-summary.md` |

### 交接物模板

**StandardGoal** (main seq1产出):
```json
{"objective": "handler层覆盖率0%→≥50%", "budget_yuan": 20, "max_rounds": 50, "constraints": ["不修改源码"], "accept": "分支覆盖率≥50%"}
```

**TaskDAG** (main seq2产出):
```json
{"krs": [
  {"kr_id":"K1.1","layer":1,"priority":1,"spec":"1个HTTP测试可运行","status":"pending","depends":[],"max_retries":3,"retry_count":0},
  {"kr_id":"K2.1","layer":2,"priority":2,"spec":"ontology_handler.py覆盖≥50%","status":"pending","depends":["K1.1"],"max_retries":3,"retry_count":0}
]}
```

**TokenEstimate** (main seq2产出):
```json
{"per_round": {"coder":50000, "reviewer":15000, "tester":12000, "auditor":10000, "publicist":5000, "main_llm":10000}, "total_rounds_estimate": 8, "total_tokens_estimate": 816000, "cost_yuan_estimate": 1.63}
```

**TaskUnit** (main→coder):
```json
{"kr_id":"K2.1","interaction_id":"{id}","round":3,"priority":2,"retry_count":0,"max_retries":3,"spec":"ontology_handler.py覆盖→≥50%","context":{"target_file":"src/ontology_handler.py"},"type":"test|code|both"}
```

**TaskResult** (coder→main):
```json
{"kr_id":"K2.1","interaction_id":"{id}","round":3,"status":"done|failed","reasoning":"被测:handle_get()，覆盖:4分支，问题:fixture需改","files_changed":["src/...","tests/..."],"commit_sha":"abc1234","token":{"in":25000,"out":8000},"self_test":{"total":257,"passed":257,"failed":0}}
```

**Verdict** (reviewer/tester/auditor→main，必含interaction_id):
```json
// reviewer:
{"interaction_id":"{id}","passed":true,"issues":[],"suggestions":[]}
// tester:
{"interaction_id":"{id}","passed":true,"all_tests":257,"passed_tests":257,"failed_tests":0,"flaky_tests":[]}
// auditor:
{"interaction_id":"{id}","passed":true,"checklist":[{"#":1,"item":"错误处理","result":"✓|✗|N/A"}],"issues":[]}
```

**CoverageReport** (tester→main):
```json
{"interaction_id":"{id}","baseline":{"line":0.12,"branch":0.08},"current":{"line":0.54,"branch":0.51},"target_file":"src/ontology_handler.py","changed_files":["..."],"br_part":["line:42"]}  // br_part=仅部分覆盖的分支行号
```

**Decision** (main seq10产出):
```json
{"kr_id":"K2.1","interaction_id":"{id}","round":3,"result":"passed|failed|skipped","votes":{"reviewer":true,"tester":true,"auditor":true},"retry_count":0,"next_action":"next_kr|retry|skip|terminate","terminate_reason":"null|<停止条件#N>"}
```

### 文档模板

**StateSnapshot**（每轮 t0 和 t1 各一份）:
```json
{
  "loop_id":"manual-20260628T140000-a3f2-L",
  "interaction_id":"manual-20260628T140000-a3f2",
  "kr_id":"K2.1","round":5,"phase":"start|end",
  "timestamp":"2026-06-28T14:35:00Z",
  "intent":"ontology_handler.py→≥50%",
  "result":"passed|failed|skipped|in_progress",
  "confidence":0.85,"debt_flags":[],
  "next_intent":"mapping_handler.py→≥50%|null",
  "coverage":{"baseline_line":0.12,"current_line":0.54,"baseline_branch":0.08,"current_branch":0.51},
  "tokens":{"round_consumed":45000,"total_consumed":234000,"budget_remaining_yuan":15.32}
}
```

**TokenReport**（每轮必须）:
```json
{
  "loop_id":"manual-20260628T140000-a3f2-L",
  "interaction_id":"manual-20260628T140000-a3f2","round":5,
  "consumption":{
    "coder":{"in":25000,"out":8000,"model":"deepseek-v4-pro"},
    "reviewer":{"in":8000,"out":2000,"model":"glm-5.2"},
    "tester":{"in":6000,"out":1500,"model":"glm-5.2"},
    "auditor":{"in":4000,"out":1000,"model":"glm-5.2"},
    "publicist":{"in":3000,"out":500,"model":"glm-5.2"},
    "main_llm":{"in":5000,"out":2000,"model":"deepseek-v4-pro"},
    "main_prog":{"cost":0}
  },
  "round_total":{"in":51000,"out":15000,"cost_yuan":0.13},
  "cumulative":{"in":234000,"out":68000,"cost_yuan":0.60},
  "budget":{"total_yuan":20,"remaining_yuan":19.40,"used_pct":3.0},
  "guard_triggers":[]
}
```

**RoundSummary**（每轮必须）:
```markdown
# Round {N} Summary
- interaction_id: {id} | round: {N} | KR: {kr_id} {描述}
- result: passed/failed | retry: {N}/{max} | duration: {分钟}
- votes: reviewer={✓/✗}, tester={✓/✗}, auditor={✓/✗}
- cost: ¥{金额} ({in}/{out} tokens) | remaining: ¥{金额}
- files: {列表} | coverage: {基线}→{当前}
- notes: {问题/经验/债务}
```

**SessionSummary**（循环结束）:
```markdown
# Session Summary — {loop_id}
- 状态: SUCCESS|FATAL|BUDGET|...
- 总轮次: {N} | KR通过率: {X}/{Y}
- 总耗时: {小时} | 总费用: ¥{金额}
- 覆盖率: {基线}→{最终}
- ADR: {N} | CR: {N}
- 异常聚合: {ERROR按类型+agent分布}
- 恢复率: {recovered/total_failures}
- 健康度: {0-100}
```

**CR（变更记录）**:
```json
{"cr_id":42,"interaction_id":"{id}","round":5,"commit_sha":"abc1234","files_changed":["src/...","tests/..."],"timestamp":"ISO8601","coder":"{agent}","patch_path":".team-loop/patches/{interaction_id}.patch"}
```

### 健康度评分

```
健康度 = 100 - ERROR数×5 - WARNING数×2 - risk_flags数×3 - 连续3轮无提升(-20) - 同KR重试>2(-10)
```
≥80健康 / 50-79警告 / <50触发人工介入。

### 预算守卫

| 消耗% | 动作 |
|--------|------|
| ≥80% | critic模型降级 |
| ≥90% | 失败KR不重试 |
| ≥95% | 暂停等待人工追加（此时停止条件#7尚未触发，给人工决策机会）|
| 预估下轮>剩余 | BUDGET终止(#7) |

### /status 调用时机

| 时机 | 步骤 | 目的 |
|------|------|------|
| seq 0 初始化 | 首次启动 | 记录基线余额 |
| seq 3 每轮开始 | 下发KR前 | 检查剩余、预算守卫判定 |
| seq 10 每轮结束 | 裁决后 | 记录消耗、更新累计 |
| 异常时 | agent超时/spawn失败 | 记录异常、写失败快照 |

### 逃逸检测

每轮应有 7 个 agent 产出确认日志（coder + reviewer + tester + auditor + publicist + main_seq3 + main_seq10）。预期 N=7×round，实际 M=grep interaction_id的日志行数。M<N→触发停止条件#11。

---

## 基础设施

### 交互编号体系

格式: `{source}-{timestamp}-{nonce}` (例: `manual-20260629T143012-a3f2b1`)

来源: `manual`(人工) | `batch`(sessions_spawn) | `test-{N}`(用例)

传递：根ID不可变→下游追加context段→链式trace: `{根ID}/{agent}-R{round}`

**携带载体（缺即逃逸）：**

| 载体 | 携带位置 | 用途 |
|------|---------|------|
| 日志JSONL | `.interaction_id` | 按入口筛选全链路 |
| StateSnapshot | `.interaction_id` | 状态对应入口 |
| TaskUnit/TaskResult | `.interaction_id` | 任务来源 |
| Verdict(×3) | `.interaction_id` | 审查追溯 |
| CR | `.interaction_id` | 变更追溯 |
| ADR | `.interaction_id` | 决策追溯 |
| Patch | 文件名=interaction_id | 补丁关联 |
| STATE.md | interaction_id行 | 运行状态关联 |
| TokenReport | `.interaction_id` | 消费追溯 |

### 日志体系（关注点分离）

**采集侧：** agent调统一Logger（自动注入interaction_id/agent/round/timestamp），提供message+level+tools_used。层级: DEBUG/INFO/WARNING/ERROR。

**加工侧：** 独立分析模块，支持按interaction_id/agent/level筛选、异常聚合、逃逸检测、健康度评分。

**视角侧：** main→state+token / auditor→WARNING+ERROR / developer→DEBUG / human→INFO摘要。

**输出：** `{agent}.log`(人类可读) + `{agent}.jsonl`(结构化，15字段: interaction_id, session_id, round, timestamp, level, agent, intent, message, tools_used, tool_calls, failures, latency_ms, tokens_in, tokens_out, risk_flags)

### 异常捕捉（三层全覆盖）

| 层 | 范围 | 机制 | 逃逸防止 |
|----|------|------|---------|
| L1 工具级 | 单次tool call | failures字段 | 必记录 |
| L2 Session级 | agent超时/spawn失败 | Monitor检测→ERROR | 兜底日志 |
| L3 循环级 | 主控崩溃/磁盘满 | 看门狗独立进程 | 心跳超时60s→写CRASH.log |

**看门狗：** 独立进程，检查 `.team-loop/HEARTBEAT`间隔(30s写入，60s超时)→触发#12。**兜底日志：** 进程退出前刷 `.team-loop/CRASH.log`。

---

## 架构决策记录 (ADR)

**触发：** 技术选型时在seq2写ADR（含interaction_id）。auditor seq9检查遗漏——发现可中断当前KR通知main补充。

**格式：** `.team-loop/adr/ADR-{序号}.md`
```markdown
# ADR-{N}: {标题}
日期: YYYY-MM-DD | 状态: proposed|accepted|deprecated|superseded
interaction_id: {id}
## 上下文
{为什么、约束}
## 决策
{选了什么}
## 后果
{正面+负面}
## 替代方案
{否决方案+原因}
```

---

## Coverage 验证

L1语法(pytest收集成功)→L2功能(通过+行>80%+分支>70%)→L3语义(auditor+human)。每轮迭代: 基线→新增→验证提升→CoverageReport。

---

## TDD 执行规则（coder）

1. **写测试→验证可运行：** 读TaskUnit→AAA模式→pytest验证收集成功、无import错误→失败修复→通过进Step2
2. **写最少代码使通过：** 仅KR要求时执行；补测已有代码→跳过
3. **自检+产出TaskResult：** 全量回归→产出reasoning(被测模块/函数/覆盖分支/问题)+token统计+commit_sha

---

## 验证清单

- [ ] /goal识别+拒绝不可量化目标
- [ ] seq0初始化完成（loop_id/interaction_id/目录/看门狗/config.json）
- [ ] 三层KR正确拆解
- [ ] coder TDD三步，不自审
- [ ] reviewer只读不运行，含"测试死刑"
- [ ] tester隔离子进程+flaky连跑3次结果一致
- [ ] auditor后置审计，13项checklist含自检
- [ ] 2/3裁决正确，重试≤3次
- [ ] 停止条件按优先级命中
- [ ] publicist沉淀到RDF
- [ ] STOP文件安全中断
- [ ] interaction_id全链路携带（9种载体）
- [ ] StateSnapshot(t0/t1)含interaction_id+kr_id
- [ ] TokenReport含cost_yuan+分agent模型
- [ ] RoundSummary+SessionSummary含健康度
- [ ] 预算守卫80/90/95触发，预估超剩余→#7
- [ ] CR编号连续含interaction_id
- [ ] 日志JSONL含15字段
- [ ] 逃逸检测(预期7×round vs 实际)
- [ ] 看门狗心跳30s/超时60s
- [ ] ADR seq2写入含interaction_id
- [ ] commit message含interaction_id
- [ ] 覆盖率L1→L2→L3
- [ ] 崩溃后从StateSnapshot(t1)恢复续跑

---

## 常见问题

**Q: team-loop vs 团队研发模式？**
`/goal`→team-loop自主循环；`团队研发`→12阶段瀑布。同一main。

**Q: 什么目标不合适？**
不可量化("提高质量")、探索性("试试优化")、需频繁人判断。

**Q: 怎么安全停止？**
创建`.team-loop/STOP`→完成当前KR安全退出。

**Q: auditor为什么后置？**
需看到reviewer+tester的Verdict才能评价审查质量。

**Q: 测试死刑是什么？**
重构时错误测试→删+重写，不在错误测试上修补。

**Q: token/cost在哪看？**
TokenReport每轮含cost_yuan，RoundSummary汇总，SessionSummary总账。

**Q: 逃逸检测怎么算？**
预期7条/轮×round；实际按interaction_id统计日志行数；少即逃逸→#11。

**Q: 崩溃后怎么恢复？**
1.看门狗检测→重启主控 2.读STATE.md→找到最后completed KR 3.读对应StateSnapshot(t1)→从下一round seq1续跑 4.in-flight KR如已commit则revert后重试。
