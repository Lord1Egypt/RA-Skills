# 测试用例模板

## 一、测试用例分类

### 1. 正常场景用例
测试 Agent 在理想条件下的核心功能。

```markdown
### TC-001：{功能名}_正常输入

**分类**：正常场景
**前置条件**：{需要的环境/数据准备}
**输入**：
{具体的用户输入}

**期望输出**：
- 格式：{期望的输出格式}
- 内容：{必须包含的信息}
- 质量：{质量标准}

**评分标准**：
- 5分：输出完全正确，格式规范，信息完整
- 4分：内容正确，有小瑕疵（格式/措辞）
- 3分：核心内容正确，缺少部分次要信息
- 2分：部分正确，有明显错误
- 1分：完全错误或无关输出

**优先级**：P0
```

### 2. 边界场景用例
测试 Agent 在极端条件下的表现。

```markdown
### TC-101：{功能名}_空输入

**分类**：边界场景
**输入**：空字符串 / null

**期望输出**：
- 友好的错误提示
- 引导用户提供有效输入

**评分标准**：
- 5分：给出清晰的引导信息
- 3分：提示不够友好但能理解
- 1分：报错或无响应

**优先级**：P1
```

常见边界场景：
- 空输入
- 超长输入（>10000 字）
- 多语言混合输入
- 包含特殊字符
- 重复/冗余输入

### 3. 异常场景用例
测试 Agent 在错误条件下的容错能力。

```markdown
### TC-201：{功能名}_工具调用失败

**分类**：异常场景
**模拟条件**：{模拟工具超时/失败}
**输入**：{需要调用工具的输入}

**期望输出**：
- 优雅降级，而非崩溃
- 告知用户当前情况
- 提供替代方案

**评分标准**：
- 5分：优雅降级 + 替代方案
- 3分：告知用户问题，无替代方案
- 1分：崩溃或无响应

**优先级**：P1
```

常见异常场景：
- 工具/API 调用超时
- 工具返回错误数据
- LLM 返回格式错误
- 权限不足
- 数据不存在

---

## 二、测试用例数量建议

| Agent 复杂度 | 正常场景 | 边界场景 | 异常场景 | 总计 |
|-------------|---------|---------|---------|------|
| 简单（单能力） | 5-10 | 3-5 | 2-3 | 10-18 |
| 中等（2-3能力） | 10-20 | 5-10 | 5-8 | 20-38 |
| 复杂（多能力协作） | 20-40 | 10-20 | 8-15 | 38-75 |

---

## 三、批量测试输入模板

用于快速批量测试的 JSON 格式：

```json
{
  "test_suite": "{Agent 名称} 评测集",
  "version": "1.0",
  "cases": [
    {
      "id": "TC-001",
      "category": "normal",
      "capability": "{能力名}",
      "input": "{输入内容}",
      "expected_contains": ["{必须包含的内容1}", "{必须包含的内容2}"],
      "expected_not_contains": ["{不应出现的内容}"],
      "max_length": 1000,
      "min_length": 100,
      "priority": "P0"
    }
  ]
}
```

---

## 四、评测自动化脚本模板

```python
"""
Agent 评测自动化脚本
"""
import json
from typing import Dict, List

class AgentEvaluator:
    def __init__(self, agent):
        self.agent = agent
        self.results = []

    def load_cases(self, path: str) -> List[Dict]:
        """加载测试用例"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['cases']

    def run_case(self, case: Dict) -> Dict:
        """运行单个测试用例"""
        output = self.agent.run(case['input'])

        result = {
            'id': case['id'],
            'input': case['input'],
            'output': output,
            'checks': {}
        }

        # 内容包含检查
        if 'expected_contains' in case:
            result['checks']['contains'] = all(
                exp in output for exp in case['expected_contains']
            )

        # 内容排除检查
        if 'expected_not_contains' in case:
            result['checks']['not_contains'] = all(
                exp not in output for exp in case['expected_not_contains']
            )

        # 长度检查
        if 'max_length' in case:
            result['checks']['max_length'] = len(output) <= case['max_length']
        if 'min_length' in case:
            result['checks']['min_length'] = len(output) >= case['min_length']

        # 综合评分
        passed = sum(1 for v in result['checks'].values() if v)
        total = len(result['checks'])
        result['score'] = (passed / total * 5) if total > 0 else 5

        return result

    def run_all(self, cases: List[Dict]) -> Dict:
        """运行所有测试用例"""
        self.results = [self.run_case(c) for c in cases]

        return {
            'total': len(self.results),
            'avg_score': sum(r['score'] for r in self.results) / len(self.results),
            'pass_rate': sum(1 for r in self.results if r['score'] >= 3) / len(self.results),
            'results': self.results
        }
```
