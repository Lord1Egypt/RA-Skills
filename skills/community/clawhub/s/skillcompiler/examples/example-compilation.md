# Example: Compiling a Code Review Prompt

**Type:** normal — 演示完整编译流程

---

## Source Prompt

```
你是一个 Python 代码审查专家。用户会给你一段 Python 代码，你需要：
1. 检查代码风格（PEP 8）
2. 检查常见 bug（空指针、类型错误、资源泄漏）
3. 检查安全问题（SQL 注入、XSS、硬编码密码）
4. 给出改进建议
5. 按严重程度分级：Critical / Warning / Info

输出格式：
## 代码审查报告
### Critical Issues
- [行号] 问题描述 + 修复建议
### Warnings
- [行号] 问题描述 + 修复建议
### Info
- [行号] 问题描述 + 修复建议
### Summary
总体评价
```

---

## Pass 0 — Triage

```json
{
  "decision": "compile",
  "reason": "可复用的代码审查能力，有明确的输入输出契约"
}
```

---

## Pass 1 — Analyze (IR)

```json
{
  "prompt_summary": "Python 代码审查专家，按风格/Bug/安全三维度检查并分级报告",
  "prompt_goal": {
    "stated": "审查 Python 代码",
    "actual": "可复用的、标准化的 Python 代码质量审计能力"
  },
  "input_spec": {
    "type": "string",
    "description": "Python 源代码",
    "inferred": false
  },
  "output_spec": {
    "type": "report",
    "description": "分级的代码审查报告（Critical/Warning/Info + Summary）",
    "inferred": false
  },
  "capability_hints": ["Review", "Analysis", "Classification"],
  "boundary": {
    "in_scope": ["Python 代码审查", "风格/Bug/安全三维度"],
    "out_of_scope": ["非 Python 语言", "性能优化", "架构重构"]
  },
  "hidden_assumptions": ["需要 PEP 8 规则知识", "需要安全漏洞模式知识"],
  "unknowns": []
}
```

---

## Pass 2 — Extract (IR)

```json
{
  "capability_graph": {
    "primary": ["Review", "Analysis"],
    "secondary": ["Classification", "Ranking"],
    "graph": {
      "Review": ["Style Check", "Bug Detection", "Security Scan"],
      "Analysis": ["Code Understanding", "Pattern Matching"]
    }
  },
  "knowledge_inventory": {
    "rules": [
      { "content": "按 PEP 8 检查风格", "source": "from source prompt", "target_file": "references/pep8-rules.md" },
      { "content": "检查空指针、类型错误、资源泄漏", "source": "from source prompt", "target_file": "references/bug-patterns.md" },
      { "content": "检查 SQL 注入、XSS、硬编码密码", "source": "from source prompt", "target_file": "references/security-checks.md" },
      { "content": "分级：Critical / Warning / Info", "source": "from source prompt", "target_file": "rubrics/severity-rubric.md" }
    ],
    "templates": [
      { "name": "Review Report", "structure": "Critical / Warning / Info / Summary", "target_file": "templates/review-report.md" }
    ],
    "domain_knowledge": [
      { "content": "PEP 8 规范", "domain": "Python", "target_file": "references/pep8-rules.md" },
      { "content": "常见 Python bug 模式", "domain": "Python", "target_file": "references/bug-patterns.md" },
      { "content": "Python 安全漏洞模式", "domain": "Security", "target_file": "references/security-checks.md" }
    ],
    "standards": [
      { "type": "scoring", "content": "严重程度分级标准", "target_file": "rubrics/severity-rubric.md" }
    ]
  },
  "role_matrix": {
    "existing": [
      {
        "name": "Python 代码审查专家",
        "responsibility": "审查代码 + 分级报告",
        "capabilities": ["Review", "Analysis"],
        "should_split": false,
        "split_reason": ""
      }
    ],
    "to_add": []
  }
}
```

---

## Pass 3 — Design (IR)

```json
{
  "architecture_type": "single-prompt",
  "workflow_pattern": null,
  "single_skill_pattern": "reviewer",
  "module_decomposition": {
    "core_prompt": "路由到三维度检查 + 分级报告生成",
    "references": [
      "references/pep8-rules.md",
      "references/bug-patterns.md",
      "references/security-checks.md"
    ],
    "templates": ["templates/review-report.md"],
    "rubrics": ["rubrics/severity-rubric.md"],
    "configs": []
  },
  "folder_structure": "code-reviewer/\n  SKILL.md\n  references/\n    pep8-rules.md\n    bug-patterns.md\n    security-checks.md\n  templates/\n    review-report.md\n  rubrics/\n    severity-rubric.md"
}
```

**设计决策：**
- single-prompt：一次 LLM 调用即可完成，无需多步骤
- reviewer pattern：分离"检查什么"（references）与"怎么查"（SKILL.md 逻辑）
- 三维度知识外置：PEP 8 / Bug / Security 各独立文件，按需加载

---

## Pass 4 — Generate (输出文件列表)

```
code-reviewer/
  SKILL.md                              ← 路由 + 三步检查流程
  references/
    pep8-rules.md                       ← PEP 8 规则
    bug-patterns.md                     ← 常见 bug 模式
    security-checks.md                  ← 安全检查项
  templates/
    review-report.md                    ← 报告模板
  rubrics/
    severity-rubric.md                  ← 严重度分级标准
```

---

## Pass 5 — Optimize

**触发：** 否（Prompt < 500 字，无重复，single-prompt）

跳过。

---

## Pass 6 — Validate

```json
{
  "review_summary": "结构清晰，三维度知识外置合理，reviewer pattern 适用。SKILL.md 预计 80 行，远低于上限。",
  "issues": [],
  "optimization_opportunities": [
    {
      "type": "future-expansion",
      "description": "未来可扩展为 multi-agent（风格/Bug/安全分别由独立 agent 检查后合并）",
      "priority": "low"
    }
  ],
  "verdict": "pass"
}
```

---

## Compilation Report

| 字段 | 值 |
|------|-----|
| Skill Name | code-reviewer |
| Architecture | single-prompt / reviewer |
| Passes Executed | 0, 1, 2, 3, 4, 6（跳过 5） |
| Files Generated | 6 |
| SKILL.md Lines | ~80 |
| Validation | pass |
