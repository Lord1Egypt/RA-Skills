---
name: unit-test-writer
description: Pytest 测试覆盖率：运行测试、发现未覆盖行、持续增加覆盖率到 100%
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/unit-test-writer/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/github/awesome-copilot/pytest-coverage
metadata:
  category: 单元测试
  platform: Python
  difficulty: 入门
---

# Pytest 测试覆盖率

> 运行 pytest 测试并生成覆盖率报告，发现未覆盖代码行，持续补充测试直到 100% 覆盖。

## 能力

- **覆盖率报告**：`pytest --cov --cov-report=annotate:cov_annotate` 生成逐行标注
- **未覆盖定位**：`!` 标记精确指出未测试代码行
- **迭代补充**：逐文件检查、补充测试、重新运行、直到全覆盖
- **模块聚焦**：`pytest --cov=module_name` 只检查特定模块
- **测试选择**：`pytest tests/test_x.py --cov=x` 精准运行相关测试

## 使用方式

```
/unit-test-writer 为这个模块生成 100% 覆盖率的测试
/unit-test-writer 找出所有未覆盖的代码行
```

## 工作流

1. 运行 `pytest --cov --cov-report=annotate:cov_annotate`
2. 打开 `cov_annotate/` 目录，查看标注后的源码
3. 100% 覆盖的文件跳过，只关注有 `!` 标记的文件
4. 逐行分析未覆盖的代码，补充测试
5. 重复运行直到所有行覆盖

## 适用场景

- Python 项目测试覆盖率提升
- CI 中设置覆盖率门槛
- 遗留代码补充测试

## 相关参考（Playbook）

- 单测写法与覆盖率工作流（pytest / Jest / Vitest）→ [references/unit-testing.md](../../references/unit-testing.md)（§Python pytest、§覆盖率工作流、§好的单测写法、§JS/TS Jest/Vitest）
- TDD 节奏（Red-Green-Refactor，覆盖率驱动）→ [references/tdd.md](../../references/tdd.md)（§工作流、§与覆盖率关系）

## 限制

- 仅支持 Python/pytest
- 100% 覆盖率不等于无 bug
- 不涉及测试质量评估（仅行覆盖）