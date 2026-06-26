---
name: test-case-gen
description: >
  Generate test cases from requirements, user stories, PRDs, or API docs.
  Output structured test cases in markdown tables or export to CSV/JSON.
  Supports equivalence partitioning, boundary value analysis, decision tables,
  state transition, and exploratory testing heuristics.
  Use when: (1) writing test cases from requirements, (2) generating test matrix,
  (3) analyzing edge cases, (4) creating test plans, (5) reviewing test coverage,
  (6) "写测试用例", "生成用例", "测试矩阵", "边界值分析", "等价类划分".
  NOT for: executing tests, automation scripting, or bug tracking.
metadata:
  openclaw:
    emoji: "📝"
---

# Test Case Generator

Generate structured, thorough test cases from various input sources.

## When to Use

✅ **USE this skill when:**
- User provides requirements/PRD/user story and needs test cases
- "帮我写测试用例" / "根据需求生成用例"
- Analyzing boundary values or equivalence classes
- Creating test matrices or decision tables
- Reviewing existing test coverage for gaps

❌ **DON'T use this skill when:**
- Running or executing tests → use `api-tester` or manual execution
- Writing automation scripts → use `api-tester` or coding tools
- Tracking bugs → use project management tools

## Workflow

### Step 1: Analyze Input

Read the provided input (requirements doc, user story, API spec, or verbal description).
Identify:
- **Functional points**: What the system should do
- **Input parameters**: All inputs with data types and constraints
- **Business rules**: Conditional logic, validations, permissions
- **Integration points**: External systems, APIs, databases
- **Non-functional aspects**: Performance, security, usability

### Step 2: Apply Test Design Techniques

Based on the analysis, apply appropriate techniques:

| Technique | When to Apply |
|-----------|---------------|
| **Equivalence Partitioning** | Multiple input values with similar behavior |
| **Boundary Value Analysis** | Numeric ranges, string lengths, date ranges |
| **Decision Table** | Complex business rules with multiple conditions |
| **State Transition** | Workflows with status changes (order, ticket, etc.) |
| **Error Guessing** | Based on common defect patterns |
| **Pairwise/Combinatorial** | Multiple parameters with interactions |

### Step 3: Generate Test Cases

Output format (default markdown table):

```markdown
| ID | Module | Priority | Precondition | Steps | Input Data | Expected Result | Type |
|----|--------|----------|--------------|-------|------------|-----------------|------|
| TC001 | Login | P0 | User registered | 1. Open login page 2. Enter credentials 3. Click login | user: admin, pass: Admin@123 | Login success, redirect to dashboard | Positive |
| TC002 | Login | P0 | User registered | 1. Open login page 2. Enter wrong password 3. Click login | user: admin, pass: wrong | Error: "Invalid credentials" | Negative |
```

**Priority definitions:**
- **P0**: Core functionality, blocks release if failed
- **P1**: Important features, should fix before release
- **P2**: Minor features, can defer
- **P3**: Edge cases, nice to have

**Type categories:**
- Positive / Negative / Boundary / Exception / Security / Performance

### Step 4: Coverage Analysis

After generating, provide a coverage summary:

```
📊 Test Coverage Summary
- Total cases: 25
- By priority: P0(8) P1(10) P2(5) P3(2)
- By type: Positive(10) Negative(8) Boundary(4) Security(2) Performance(1)
- Estimated gaps: [list any uncovered areas]
```

## Export Options

When user requests export:

```bash
# Save as CSV — write to workspace
# ~/.openclaw/workspace/output/test_cases.csv

# Save as JSON (for TestLink/禅道 import)
# ~/.openclaw/workspace/output/test_cases.json
```

### 禅道 CSV Import Format

```csv
所属模块,用例标题,前置条件,步骤,预期,优先级,用例类型,关键词
/登录模块,正常登录验证,用户已注册,1.打开登录页 2.输入正确账号密码 3.点击登录,登录成功跳转首页,1,功能测试,登录;正向
```

### TestLink XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testcases>
  <testcase name="正常登录验证">
    <summary>验证使用正确账号密码能成功登录</summary>
    <preconditions>用户已注册</preconditions>
    <steps>
      <step>
        <step_number>1</step_number>
        <actions>打开登录页，输入正确账号密码，点击登录</actions>
        <expectedresults>登录成功，跳转首页</expectedresults>
      </step>
    </steps>
    <importance>2</importance>
    <execution_type>1</execution_type>
  </testcase>
</testcases>
```

## Tips for Better Test Cases

- Always include at least one boundary value test per numeric input
- For every positive case, create at least one corresponding negative case
- Don't forget null/empty/whitespace inputs
- Consider concurrent access scenarios for multi-user features
- Include data format validation (email, phone, ID card, etc.)
- Test with special characters: `<script>alert(1)</script>`, `' OR 1=1--`, emoji 🔍

## Pairwise / Combinatorial Testing

When multiple input parameters interact, use pairwise to reduce combinations:

```
参数A: [a1, a2, a3]
参数B: [b1, b2]
参数C: [c1, c2, c3]

全组合: 3×2×3 = 18 条
Pairwise: ~9 条（覆盖所有两两组合）
```

示例输出:

| # | 参数A | 参数B | 参数C |
|---|-------|-------|-------|
| 1 | a1 | b1 | c1 |
| 2 | a1 | b2 | c2 |
| 3 | a2 | b1 | c3 |
| 4 | a2 | b2 | c1 |
| 5 | a3 | b1 | c2 |
| 6 | a3 | b2 | c3 |
| ... | | | |

适用场景：浏览器兼容性（浏览器×系统×分辨率）、表单多字段组合、配置项测试。

## State Transition Testing

For workflow/status-driven features, map out state transitions:

```
[草稿] --提交--> [待审核] --通过--> [已发布]
   |                  |--驳回--> [已驳回] --修改--> [草稿]
   |--删除--> [已删除]
```

Generate test cases covering:
- **每个状态**: 至少访问一次
- **每个转换**: 至少触发一次
- **非法转换**: 验证不允许的状态变更（如 已发布→草稿）
- **并发转换**: 两人同时审核同一条记录
