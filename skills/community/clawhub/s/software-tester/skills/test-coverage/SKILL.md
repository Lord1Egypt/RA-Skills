---
name: test-coverage
description: 测试策略设计：覆盖率目标、测试金字塔、CI 集成、测试类型选择
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/test-coverage/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/github/awesome-copilot/pytest-coverage
metadata:
  category: 测试策略
  platform: 通用
  difficulty: 进阶
---

# 测试策略与覆盖率管理

> 制定测试策略：覆盖率目标设定、测试金字塔实践、CI 集成方案、测试类型选择。

## 能力

- **测试金字塔**：单元测试（70%）+ 集成测试（20%）+ E2E 测试（10%）
- **覆盖率目标**：行覆盖率 vs 分支覆盖率、核心模块高标准 vs 非核心适度
- **CI 集成**：覆盖率门槛配置、PR 检查、覆盖率趋势追踪
- **测试类型**：功能测试、回归测试、快照测试、属性测试的选择
- **测试债务管理**：识别长期未更新的测试、误报率高的测试

## 使用方式

```
/test-coverage 为这个项目设计测试策略
/test-coverage 配置 CI 中的覆盖率门槛
/test-coverage 这个模块该写什么类型的测试？
```

## 工作流

1. 分析项目结构和核心模块
2. 设定覆盖率目标（按模块分级）
3. 规划测试金字塔比例
4. 配置 CI 覆盖率检查
5. 定期回顾测试有效性

## 适用场景

- 新项目测试策略制定
- CI 覆盖率门槛配置
- 测试债务清理
- 测试 ROI 评估

## 相关参考（Playbook）

- 测试金字塔、覆盖率目标分级、CI 质量门禁、测试债管理、测试类型选择 → [references/test-strategy.md](../../references/test-strategy.md)（§测试金字塔、§覆盖率目标分级、§CI 质量门禁、§测试债管理、§测试类型选择）
- 测试报告与质量门禁结论（策略的产出）→ [references/reporting.md](../../references/reporting.md)（§质量门禁结论模板、§风险报告格式）

## 限制

- 覆盖率不等于测试质量
- 策略需根据项目类型调整
- 不涉及具体测试框架配置