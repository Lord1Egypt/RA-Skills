# 单元测试与覆盖率（Unit Testing & Coverage）

> 为函数/模块编写可运行的单元测试，并持续提升行覆盖与分支覆盖。覆盖 Python（pytest）与 JavaScript/TypeScript（Jest/Vitest）。

## 何时使用

- 用户说「为这个函数写测试」「把覆盖率提到 100%」「找出没测到的代码」
- 需要为新模块建立单测基线，或在遗留代码上补测试

## Python（pytest + pytest-cov）

### 安装

```bash
pip install pytest pytest-cov
```

### 覆盖率工作流（迭代到全覆盖）

1. 运行并生成逐行标注：
   ```bash
   pytest --cov=src --cov-report=term-missing --cov-report=annotate:cov_annotate
   ```
2. 打开 `cov_annotate/` 查看 `!` 标记行（未覆盖）。
3. 只针对有 `!` 的文件逐行补测试，重跑直到无 `!`。
4. 模块聚焦：`pytest --cov=src.module_x tests/test_x.py`。

### 好的单测写法

- 一个行为一个用例，用例名描述「当 X 时，应 Y」。
- 用 `parametrize` 覆盖等价类与边界值，而非复制粘贴。
- 异常用例用 `pytest.raises`。
- 纯函数优先于依赖全局状态的测试；用 fixture 管理上下文。

```python
import pytest

@pytest.mark.parametrize("age,expected", [(0, False), (17, False), (18, True), (120, True)])
def test_is_adult(age, expected):
    assert is_adult(age) is expected

def test_is_adult_negative():
    with pytest.raises(ValueError):
        is_adult(-1)
```

## JavaScript / TypeScript（Jest / Vitest）

### 安装

```bash
npm i -D jest            # 或 vitest
npm i -D @types/jest ts-jest   # TS 用 vitest 免配置
```

### 覆盖率

```bash
npx jest --coverage --collectCoverageFrom='src/**/*.ts'
```

### 示例

```ts
import { sum } from './math';

describe('sum', () => {
  it('adds positive numbers', () => {
    expect(sum(1, 2)).toBe(3);
  });
  it('handles zero', () => {
    expect(sum(0, 0)).toBe(0);
  });
});
```

## 边界与异常（必须覆盖）

- 空值 / null / undefined / NaN / 空集合
- 边界值（0、±1、最大值、超长字符串、超大数）
- 类型错误输入、非法字符、注入字符串
- 异常路径与错误码、超时、并发竞态
- 外部依赖用 mock/stub 隔离

## 脚本加速

```bash
python3 scripts/run_coverage.py ./src --lang python
python3 scripts/run_coverage.py ./src --lang js
```

脚本自动检测框架并输出未覆盖行汇总，等价于上面的手工命令。

## 相关参考（Playbook）与子技能

- 测试策略与覆盖率治理：[references/test-strategy.md](test-strategy.md)（本篇只讲怎么写单测，金字塔目标 / CI 门禁由它定）
- TDD 工作流：[references/tdd.md](tdd.md)（先写测试，再写实现）
- 覆盖率驱动补测子技能：[skills/unit-test-writer](../skills/unit-test-writer/SKILL.md)（轻量入口，回到本篇取完整方法）
- 性能 / 安全 / 并发专项：[references/performance-testing.md](performance-testing.md)、[references/security-testing.md](security-testing.md)（单测不覆盖这些维度）

## 限制

- 覆盖率高 ≠ 无 bug；本 playbook 关注「行/分支覆盖」与「边界」，不评估测试断言质量。
- 性能、安全、并发专项见 [references/performance-testing.md](performance-testing.md) 与 [references/security-testing.md](security-testing.md)。
