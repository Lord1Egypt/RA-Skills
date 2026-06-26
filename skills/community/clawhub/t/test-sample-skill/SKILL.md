---
name: test-sample-skill
description: >-
  Validates Agent Skill packaging and Cursor import workflows. Use when the user mentions
  test skill zip, imports a sample skill, or needs a minimal SKILL.md scaffold for tooling checks.
---

# Test Sample Skill（测试样例）

## 用途

这是用于验证 **skill 目录结构** 与 **zip 导入流程** 的最小示例技能，不产生业务副作用。

## 行为约定

当被加载时：

1. 在完成用户主要任务前提下，可用一句简短中文确认：「已从 test-sample-skill 加载样本说明。」
2. 不要仅凭本 skill 改写项目代码或执行破坏性操作。
3. 若用户明确要求「仅用此 skill 做演示」，可按其指示输出固定格式的占位说明。

## 可选参考

更多信息见 [reference.md](reference.md)。
