# Workspace Context Linter

[中文说明](#中文说明)

Workspace Context Linter audits always-loaded workspace context files such as `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, and `TOOLS.md`.

It is designed to help identify:
- duplicated rules or preferences
- overweight sections in always-loaded context
- content that may belong in a different file role
- likely cleanup priorities before reorganizing context

## What it checks
- file role summaries for core context files
- duplicate themes across core files
- overweight sections that may be better as references
- misplaced content based on expected file roles

## Current scope
This first version focuses on:
- core context files
- text reports
- diagnosis rather than auto-editing
- role-aware duplicate severity

It does **not** automatically rewrite files.

## Usage
```bash
scripts/context_linter.py [--scope core|core+memory|custom] [--paths ...] [--output report.txt]
```

Example:
```bash
scripts/context_linter.py --scope core --output context-report.txt
```

## Output
The report includes:
- summary
- file role summary
- top priorities
- duplicates
- overweight sections
- misplaced content
- suggested moves

---

## 中文说明

Workspace Context Linter 用于体检工作区中**长期常驻上下文文件**，例如：
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `MEMORY.md`
- `TOOLS.md`

它主要帮助发现：
- 重复规则或重复偏好
- 常驻上下文中过重的段落
- 内容可能放错文件的位置
- 在整理上下文前最值得优先处理的项

## 它会检查什么
- core context 文件的角色摘要
- 核心文件之间的重复主题
- 可能更适合外移成 reference 的过重 section
- 基于文件职责推断的误放内容

## 当前范围
这一版主要聚焦：
- core context files
- 文本报告
- 诊断而不是自动改写
- 带角色感知的重复严重度判断

它**不会**自动重写上下文文件。

## 用法
```bash
scripts/context_linter.py [--scope core|core+memory|custom] [--paths ...] [--output report.txt]
```

示例：
```bash
scripts/context_linter.py --scope core --output context-report.txt
```

## 输出内容
报告会包含：
- summary
- file role summary
- top priorities
- duplicates
- overweight sections
- misplaced content
- suggested moves
