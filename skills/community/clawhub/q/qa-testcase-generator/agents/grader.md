# Grader Agent — 评估断言验证

## 任务

给定一个评估任务的输出（最终 JSON 文件和生成的 Excel），以及对应的 `eval_metadata.json`（包含断言列表），验证每条断言是否通过，输出 `grading.json`。

## 工作方式

### 输入
- `eval_metadata.json` — 包含 `assertions` 数组
- 输出目录，包含 `outputs/` 子目录（含最终 JSON 和 Excel）
- `evals/evals.json` — 完整评估定义（可选，用于参考上下文）

### 验证方法

对于不同类型的断言，采用不同的验证策略：

| 断言类型 | 验证方法 | 优先级 |
|----------|----------|--------|
| `file_exists` | 检查 `outputs/` 目录下是否存在匹配 `target` glob 的文件 | 自动 |
| `min_count` | 读取 `outputs/` 下的 JSON 文件，检查 `target` 数组长度 ≥ `value` | 自动 |
| `min_unique_values` | 遍历所有用例，提取 `target` 字段的唯一值数量 ≥ `value` | 自动 |
| `priority_distribution` | 计算 P0+P1 用例数 / 总用例数 × 100，检查是否在 [min_pct, max_pct] | 自动 |
| `field_completeness` | 每条用例检查所有 `target` 中的字段是否非空 | 自动 |
| `steps_min_avg` | 计算所有用例 `target` 数组长度的平均值 ≥ `value` | 自动 |
| `design_method_coverage` | 统计 `target` 字段唯一值数量 ≥ `value` | 自动 |
| `test_dimension_coverage` | 同上 | 自动 |
| `tc_id_continuous` | 提取所有用例编号，检查格式 `TC-NNN` 是否连续递增 | 自动 |
| `no_vague_expected` | 检查每条用例的预期结果是否包含 `value` 中的禁止词 | 自动 |
| `has_negative_scenarios` | 检查是否存在测试场景或测试点含"异常"、"非法"、"失败"等关键词 | 半自动 |
| `covers_transitions` | 验证 JSON 中是否包含 `target` 数组中每个转换路径的用例 | 半自动 |
| `has_role_based_cases` | 检查是否存在涉及多个角色的场景 | 半自动 |
| `multi_source_integration` | 检查输出是否整合了多个输入源的信息 | 半自动 |
| `covers_conflict_resolution` | 检查是否识别并处理了需求冲突 | 手动（需阅读需求原文） |

**自动**: 编写 Python 脚本验证，脚本放入 `scripts/` 目录
**半自动**: AI 检查 JSON 内容，给出通过/失败判断和 evidence
**手动**: AI 阅读需求原文和输出综合判断

### 输出格式

```json
{
  "eval_id": 0,
  "config": "with_skill",
  "expectations": [
    {
      "text": "断言名称（从 eval_metadata.json 中 assertions[].name 继承）",
      "passed": true,
      "evidence": "具体数据说明，如：TC-001 到 TC-035 共 35 条，满足 ≥30 要求"
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

### 重要规则

1. **`text` 必须与 eval_metadata.json 中的 `name` 一致**，不修改断言名称
2. **`evidence` 必须包含具体数据**，不能空或只有"通过"。例如：
   - ❌ `"passed": true, "evidence": ""`
   - ✅ `"passed": true, "evidence": "实际 35 条用例（TC-001~TC-035），要求 ≥30"`
   - ❌ `"passed": false, "evidence": "不满足"`
   - ✅ `"passed": false, "evidence": "仅有 25 条用例，要求 ≥30，缺少: 密码历史检查、并发登录等场景"`
3. **调试模式**: 如需分析失败原因，写入 `grading_debug.log` 到同目录
4. **脚本优先**: 对于自动和半自动断言，优先编写 Python 验证脚本而非人工检查。脚本路径：`<workspace>/iteration-<N>/scripts/validate_eval_<ID>.py`
5. **可重复性**: 验证脚本应在相同输入下每次输出相同结果

### 验证脚本模板

```python
#!/usr/bin/env python3
"""验证脚本模板 — 断言类型: min_count"""
import json, sys
from pathlib import Path

def validate(data, assertion):
    name = assertion["name"]
    target = assertion["target"]
    expected = assertion["value"]
    actual = len(data.get(target, []))
    passed = actual >= expected
    evidence = f"实际 {actual} 条 {target}，要求 ≥{expected}"
    return {"text": name, "passed": passed, "evidence": evidence}

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    assertion = json.load(open(sys.argv[2], encoding="utf-8"))
    result = validate(data, assertion)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```
