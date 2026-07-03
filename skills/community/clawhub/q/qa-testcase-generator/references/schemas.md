# 评估体系 Schema 文档

本文档定义了 qa-testcase-generator 评估体系的全部 JSON 结构。

---

## 1. evals.json — 评估用例集

**路径**: `evals/evals.json`

```json
{
  "skill_name": "qa-testcase-generator",
  "description": "Eval set description",
  "evals": [
    {
      "id": 1,
      "prompt": "用户输入的任务描述（完整自然语言）",
      "expected_output": "期望输出的简要描述",
      "files": ["tests/test_requirements.md"]
    }
  ],
  "assertions": [
    {
      "eval_id": 1,
      "assertions": [
        {
          "name": "断言名称（简短、描述性，在 viewer 中展示）",
          "description": "断言详细说明",
          "type": "断言类型标识符",
          "target": "断言作用的目标字段或文件",
          "value": 30,
          "min_pct": 40,
          "max_pct": 70
        }
      ]
    }
  ]
}
```

### 断言类型一览

| 类型标识符 | 说明 | 必填字段 |
|-----------|------|----------|
| `file_exists` | 检查输出文件存在 | `target` — glob 路径 |
| `min_count` | 测试用例数 ≥ N | `target` — JSON 中数组字段名（如 `测试用例`）, `value` — 下限 |
| `min_unique_values` | 字段唯一值数 ≥ N | `target` — 字段名（如 `业务域`）, `value` — 下限 |
| `min_unique_references` | 需求来源引用数 ≥ N | `target` — 字段名（如 `需求来源`）, `value` — 下限 |
| `priority_distribution` | P0+P1 占比在 [min, max] | `target` — `"P0+P1"`, `min_pct`, `max_pct` |
| `field_completeness` | 每条用例的指定字段非空 | `target` — 字段名数组 |
| `steps_min_avg` | 平均操作步骤数 ≥ N | `target` — `操作步骤`, `value` — 步数下限 |
| `design_method_coverage` | 设计方法种类 ≥ N | `target` — `设计方法`, `value` — 下限 |
| `test_dimension_coverage` | 测试维度种类 ≥ N | `target` — `测试维度`, `value` — 下限 |
| `tc_id_continuous` | 用例编号连续无间断 | `target` — `用例编号` |
| `no_vague_expected` | 预期结果不含模糊用词 | `target` — `预期结果`, `value` — 禁止词数组 |
| `has_negative_scenarios` | 包含异常/反向场景 | `target` — 字段名 |
| `covers_transitions` | 覆盖所有指定状态转换 | `target` — 转换路径数组 |
| `has_negative_transitions` | 包含非法状态转换用例 | `target` — 字段名 |
| `has_role_based_cases` | 包含多角色权限场景 | `target` — 角色名数组 |
| `covers_branches` | 覆盖流程图每个判断分支 | `target` — 分支路径描述 |
| `covers_parameter_validation` | 接口参数校验覆盖 | `target` — 接口数量 |
| `covers_error_codes` | 包含错误码验证场景 | `target` — 字段名 |
| `multi_source_integration` | 多源输入（文本+图片）整合 | `target` — 描述 |
| `covers_conflict_resolution` | 需求冲突识别与处理 | `target` — 描述 |

### 断言类型详细定义

#### 文件类
```json
{"name": "Excel 文件已生成", "type": "file_exists", "target": "output/*.xlsx"}
```

#### 计数类
```json
{"name": "用例数 ≥ 30", "type": "min_count", "target": "测试用例", "value": 30}
```

#### 覆盖类
```json
{"name": "业务域覆盖 ≥ 4", "type": "min_unique_values", "target": "业务域", "value": 4}
```

#### 分布类
```json
{"name": "P0+P1 占比合理", "type": "priority_distribution", "target": "P0+P1", "min_pct": 40, "max_pct": 70}
```

#### 完整性类
```json
{"name": "必填字段完整", "type": "field_completeness", "target": ["用例编号","业务域","优先级","测试维度","测试场景","操作步骤","前置条件","需求来源"]}
```

#### 结构类
```json
{"name": "平均步骤数 ≥ 3", "type": "steps_min_avg", "target": "操作步骤", "value": 3}
```

#### 质量类
```json
{"name": "预期结果不含模糊表述", "type": "no_vague_expected", "target": "预期结果", "value": ["成功","正常"]}
```

---

## 2. eval_metadata.json — 单次评估元数据

**路径**: `<workspace>/iteration-<N>/<eval-name>/eval_metadata.json`

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt（完整原文）",
  "input_files": ["tests/test_requirements.md"],
  "assertions": [
    {
      "name": "断言名称",
      "type": "断言类型",
      "target": "目标",
      "value": 30,
      "min_pct": 40,
      "max_pct": 70,
      "description": "断言详细说明"
    }
  ]
}
```

---

## 3. grading.json — 评分结果

**路径**: `<workspace>/iteration-<N>/<eval-name>/<config>/grading.json`

```json
{
  "eval_id": 0,
  "config": "with_skill | without_skill | old_skill",
  "expectations": [
    {
      "text": "断言名称",
      "passed": true,
      "evidence": "TC-001 到 TC-035 共 35 条用例，满足 ≥30 要求"
    }
  ],
  "summary": {
    "total": 5,
    "passed": 4,
    "failed": 1,
    "pass_rate": 80.0
  }
}
```

**⚠️ 字段名称必须为 `text`, `passed`, `evidence`**（viewer 依赖此命名）。不能用 `name`, `met`, `details` 等变体。

---

## 4. benchmark.json — 聚合基准

**路径**: `<workspace>/iteration-<N>/benchmark.json`

```json
{
  "skill_name": "qa-testcase-generator",
  "iteration": 1,
  "configs": [
    {
      "name": "with_skill",
      "label": "With Skill",
      "eval_groups": [
        {
          "eval_id": 0,
          "eval_name": "用户管理需求生成",
          "assertions_passed": 4,
          "assertions_total": 5,
          "pass_rate": 80.0
        }
      ],
      "summary": {
        "total_assertions": 15,
        "passed_assertions": 13,
        "overall_pass_rate": 86.7,
        "total_time_seconds": 145.3,
        "avg_time_per_eval": 29.1,
        "std_time": 8.2,
        "total_tokens": 485000,
        "avg_tokens_per_eval": 97000,
        "std_tokens": 21000
      }
    }
  ],
  "analysis": [
    "eval-0 和 eval-2 全通过",
    "eval-4 断言 '分支路径覆盖' 失败 — 图片分析的路径识别不完整",
    "所有配置中 'field_completeness' 断言均通过 — 非区分性断言，考虑移除"
  ]
}
```

---

## 5. timing.json — 运行时间

**路径**: `<workspace>/iteration-<N>/<eval-name>/<config>/timing.json`

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

---

## 6. feedback.json — 用户反馈

**路径**: `<workspace>/iteration-<N>/feedback.json`

```json
{
  "reviews": [
    {
      "run_id": "eval-0-with_skill",
      "feedback": "用例步骤数偏少，可以补充更多分支场景",
      "timestamp": "2026-06-29T08:30:00Z"
    }
  ],
  "status": "complete"
}
```

---

## 7. trigger_evals.json — 触发评估集

**路径**: `evals/trigger_evals.json`

```json
[
  {
    "query": "用户的实际输入（包含具体场景细节）",
    "should_trigger": true
  },
  {
    "query": "不应触发此技能的输入（近义词但不相关）",
    "should_trigger": false
  }
]
```

### 设计原则

- **应触发 (true)**: 用户明确需要从需求文档生成测试用例的场景。覆盖不同措辞（正式/口语）、不同输入格式（MD/PDF/Word/图片）。
- **不应触发 (false)**: 近义词场景 — 自动生成脚本、运行测试、整理 bug、CI/CD 配置等。这些场景和目标技能无关但关键词有重叠，是质量最高的负面案例。

---

## 8. assertion 脚本编程接口

对于可编程验证的断言，建议编写断言验证脚本，存放在 `<workspace>/iteration-<N>/scripts/` 下：

```python
# validate_assertions.py
"""
标准断言验证器。
输入：最终 JSON 数据文件路径
输出：grading.json
可复用于不同 iteration。
"""
```

建议遵循以下约定：
1. **脚本随 iteration 保留**，便于跨版本对比
2. **断言函数签名**: `assert_<type>(data, target, value) → (passed: bool, evidence: str)`
3. **失败时 evidence 包含具体差异细节**（如"实际 25 条，需要 ≥30"）
