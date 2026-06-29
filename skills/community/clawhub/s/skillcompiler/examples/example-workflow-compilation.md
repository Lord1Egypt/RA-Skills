# Example: Compiling a Workflow Prompt (API Doc Generator)

**Type:** normal — 演示 workflow 架构的完整编译流程

---

## Source Prompt

```
你是一个 API 文档专家。用户给你一段 API 代码（REST/GraphQL），你需要：
1. 提取所有 endpoint 和参数
2. 为每个 endpoint 生成文档（描述、参数表、请求示例、响应示例）
3. 检查文档是否缺少必要字段（描述、示例、错误码）
4. 生成最终的 API 文档（Markdown 格式）

如果发现 endpoint 缺少描述，先标记为 TODO，继续处理其他 endpoint，最后汇总所有 TODO。
```

---

## Pass 0 — Triage

```json
{
  "decision": "compile",
  "reason": "多步骤可复用工作流，有明确的输入输出契约，步骤间有顺序依赖"
}
```

---

## Pass 1 — Analyze (IR)

```json
{
  "prompt_summary": "API 代码 → 提取 endpoint → 逐个生成文档 → 完整性检查 → 汇总输出",
  "prompt_goal": {
    "stated": "为 API 代码生成文档",
    "actual": "可复用的、标准化的 API 文档自动化生成工作流，支持增量处理"
  },
  "input_spec": {
    "type": "file",
    "description": "API 源代码文件（REST 路由定义 / GraphQL schema）",
    "inferred": false
  },
  "output_spec": {
    "type": "report",
    "description": "Markdown 格式的完整 API 文档 + TODO 汇总清单",
    "inferred": false
  },
  "capability_hints": ["Analysis", "Writing", "Review", "Planning"],
  "boundary": {
    "in_scope": ["REST API 文档生成", "GraphQL schema 文档生成", "完整性检查"],
    "out_of_scope": ["OpenAPI/Swagger 规范转换", "API 性能分析", "代码逻辑审查"]
  },
  "hidden_assumptions": ["需要 HTTP 方法语义知识", "需要常见 API 参数模式知识"],
  "unknowns": []
}
```

---

## Pass 2 — Extract (IR)

```json
{
  "capability_graph": {
    "primary": ["Analysis", "Writing"],
    "secondary": ["Review", "Planning"],
    "graph": {
      "Analysis": ["Endpoint Extraction", "Parameter Parsing"],
      "Writing": ["Doc Generation", "Example Synthesis"],
      "Review": ["Completeness Check"],
      "Planning": ["Batch Orchestration"]
    }
  },
  "knowledge_inventory": {
    "rules": [
      { "content": "每个 endpoint 文档必须含：描述、参数表、请求示例、响应示例", "source": "from source prompt", "target_file": "rubrics/completeness-rubric.md" },
      { "content": "缺少描述时标记 TODO，不阻塞后续处理", "source": "from source prompt", "target_file": "references/rules.md" },
      { "content": "最后汇总所有 TODO", "source": "from source prompt", "target_file": "references/rules.md" }
    ],
    "templates": [
      { "name": "Endpoint Doc", "structure": "描述 + 参数表 + 请求示例 + 响应示例", "target_file": "templates/endpoint-doc.md" }
    ],
    "domain_knowledge": [
      { "content": "HTTP 方法语义（GET/POST/PUT/DELETE/PATCH）", "domain": "API", "target_file": "references/http-semantics.md" },
      { "content": "常见 API 参数模式（path/query/header/body）", "domain": "API", "target_file": "references/api-patterns.md" }
    ],
    "standards": [
      { "type": "quality", "content": "完整性检查清单（描述/示例/错误码）", "target_file": "rubrics/completeness-rubric.md" }
    ]
  },
  "role_matrix": {
    "existing": [
      {
        "name": "API 文档专家",
        "responsibility": "提取 + 生成 + 检查 + 汇总",
        "capabilities": ["Analysis", "Writing", "Review"],
        "should_split": true,
        "split_reason": "同时负责'生成文档'和'检查文档完整性'——干验分离原则（AP-04）"
      }
    ],
    "to_add": [
      {
        "name": "Completeness Checker",
        "reason": "独立于生成者，检查文档完整性",
        "responsibility": "验证每个 endpoint 文档是否含全部必填字段"
      }
    ]
  }
}
```

---

## Pass 3 — Design (IR)

```json
{
  "architecture_type": "workflow",
  "workflow_pattern": "pipeline",
  "single_skill_pattern": "pipeline",
  "module_decomposition": {
    "core_prompt": "四步流水线：提取 → 生成 → 检查 → 汇总",
    "references": [
      "references/http-semantics.md",
      "references/api-patterns.md",
      "references/rules.md"
    ],
    "templates": ["templates/endpoint-doc.md"],
    "rubrics": ["rubrics/completeness-rubric.md"]
  },
  "workflow_steps": [
    {
      "id": "extract",
      "purpose": "从 API 代码中提取所有 endpoint 和参数",
      "input": "API 源代码",
      "output": "endpoint 列表（JSON）",
      "decision_gate": "endpoint 列表非空",
      "exit_criteria": "所有 endpoint 已解析出路径、方法、参数",
      "retry_strategy": "解析失败时重试（最多 3 次）",
      "rollback_strategy": "返回错误，提示用户检查代码格式"
    },
    {
      "id": "generate",
      "purpose": "为每个 endpoint 生成文档",
      "input": "endpoint 列表",
      "output": "endpoint 文档列表",
      "decision_gate": "文档列表数量 = endpoint 列表数量",
      "exit_criteria": "每个 endpoint 有对应文档（含 TODO 标记）",
      "retry_strategy": "生成失败的单个 endpoint 跳过并标记，不阻塞整体",
      "rollback_strategy": "已生成的文档保留，缺失项记入 TODO"
    },
    {
      "id": "check",
      "purpose": "独立检查文档完整性",
      "input": "endpoint 文档列表",
      "output": "检查报告（缺失字段清单）",
      "decision_gate": "无",
      "exit_criteria": "每个文档已检查全部必填字段",
      "retry_strategy": "无（检查是只读操作）",
      "rollback_strategy": "无"
    },
    {
      "id": "assemble",
      "purpose": "汇总为最终 Markdown 文档 + TODO 清单",
      "input": "endpoint 文档列表 + 检查报告",
      "output": "完整 API 文档（Markdown）",
      "decision_gate": "文档非空",
      "exit_criteria": "Markdown 输出包含所有 endpoint 文档 + TODO 汇总",
      "retry_strategy": "无",
      "rollback_strategy": "无"
    }
  ],
  "folder_structure": "api-doc-generator/\n  SKILL.md\n  references/\n    http-semantics.md\n    api-patterns.md\n    rules.md\n  templates/\n    endpoint-doc.md\n  rubrics/\n    completeness-rubric.md"
}
```

**设计决策：**
- workflow：四步顺序执行，步骤间有数据依赖（extract → generate → check → assemble）
- pipeline pattern：强制顺序，每步有 decision_gate 门控
- generate 步骤支持增量处理：单个 endpoint 失败不阻塞整体（对应"标记 TODO 继续"的需求）
- check 步骤独立于 generate（干验分离，避免 AP-04）

### IR 校验（Pass 3→4 门控）

| # | 校验项 | 结果 |
|---|--------|------|
| 1 | meta + pass_1 + pass_2 + pass_3 四个顶层字段齐全 | ✅ |
| 2 | capability_graph.primary 非空（Analysis, Writing） | ✅ |
| 3 | architecture_type = workflow | ✅ |
| 4 | single_skill_pattern = pipeline | ✅ |
| 5 | folder_structure 非空 | ✅ |

全部 PASS → 进入 Pass 4。

---

## Pass 4 — Generate (输出文件列表)

```
api-doc-generator/
  SKILL.md                              ← 路由 + 四步流水线概览
  references/
    http-semantics.md                   ← HTTP 方法语义
    api-patterns.md                     ← API 参数模式
    rules.md                            ← 处理规则（TODO 标记、汇总）
  templates/
    endpoint-doc.md                     ← 单个 endpoint 文档模板
  rubrics/
    completeness-rubric.md              ← 完整性检查清单
```

---

## Pass 5 — Optimize

**触发：** 是（architecture_type = workflow，且步骤间有数据依赖需要精简契约）

```json
{
  "optimizations_applied": [
    {
      "check": "O2",
      "issue": "generate 步骤输出完整文档给 check 步骤，但 check 只需要文档的字段清单",
      "action": "精简 generate→check 数据契约：check 只接收文档 ID + 字段存在性矩阵",
      "impact": "inter-agent 数据传输量减少 ~60%"
    }
  ],
  "optimizations_skipped": [
    { "check": "O8", "reason": "不涉及外部能力" }
  ]
}
```

---

## Pass 6 — Validate

```json
{
  "review_summary": "四步流水线设计合理，generate 步骤的增量处理满足'标记 TODO 继续'的需求。check 步骤独立于 generate（AP-04 合规）。workflow 步骤均有 exit_criteria 和 retry_strategy。",
  "issues": [
    {
      "id": "ISS-001",
      "severity": "medium",
      "role": "Workflow Designer",
      "title": "generate 步骤无 max_iterations",
      "detail": "generate 步骤的 retry_strategy 说'失败时重试最多 3 次'，但未在 workflow 定义中显式声明 max_iterations",
      "fix": "在 workflow 定义中增加 max_iterations: 3",
      "fix_difficulty": "easy"
    }
  ],
  "verdict": "conditional-pass",
  "verdict_reason": "1 个 Medium issue，有明确修复方案"
}
```

---

## Execution Trace（产出）

```json
{
  "skill_name": "skill-compiler",
  "invocation_id": "compile-api-doc-20260626",
  "passes": [
    { "pass_id": "triage", "status": "executed", "trigger_reason": "总是执行" },
    { "pass_id": "analyze", "status": "executed", "ir_fields_written": ["pass_1_analyze"] },
    { "pass_id": "extract", "status": "executed", "ir_fields_written": ["pass_2_extract"] },
    { "pass_id": "design", "status": "executed", "ir_fields_written": ["pass_3_design"] },
    { "pass_id": "generate", "status": "executed", "ir_fields_written": ["files_generated"] },
    { "pass_id": "optimize", "status": "executed", "trigger_reason": "architecture_type=workflow" },
    { "pass_id": "validate", "status": "executed" }
  ],
  "outcome": "success",
  "validation_verdict": "conditional-pass"
}
```

---

## Compilation Report

| 字段 | 值 |
|------|-----|
| Skill Name | api-doc-generator |
| Architecture | workflow / pipeline |
| Passes Executed | 0, 1, 2, 3, 4, 5, 6（全部执行） |
| Files Generated | 6 |
| SKILL.md Lines | ~120 |
| Validation | conditional-pass（1 Medium issue） |
| Trace | ✅ 产出 |
