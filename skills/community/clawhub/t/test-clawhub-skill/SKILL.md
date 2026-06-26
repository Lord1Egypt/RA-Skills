---
name: test-clawhub-cli
description: 测试 clawhub CLI 发布功能 - 验证 publish 命令的参数处理
version: 1.0.0
tags:
  - test
  - clawhub
  - automation
---

# Test ClawHub CLI Skill

这是一个用于测试 clawhub CLI 发布功能的 skill。

## 功能说明

本 skill 用于验证 clawhub CLI 的 `publish` 命令是否正确处理以下参数：

- `--name` - 显示名称
- `--version` - 版本号（semver 格式）
- `--tags` - 标签（逗号分隔）
- `--changelog` - 变更日志

## 测试目的

确保 skill-manager 项目中 clawhub 发布器的 CLI 调用逻辑与实际 CLI 行为一致。

## 文件结构

```
test-clawhub-skill/
├── SKILL.md           # Skill 元数据定义
├── README.md          # 详细文档
└── test_script.py     # 测试脚本
```

## 开发者说明

本 skill 由 skill-manager 自动测试生成，不建议手动修改。
