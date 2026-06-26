---
name: spec-engine
description: |
  项目规格自动生成与验证工具 — 从想法到任务清单的全流程自动化。
  支持：(1) 智能生成 spec (2) 可配置验证评分 (3) 自动拆解子任务 (4) Web 仪表盘 (5) 版本对比 (6) 历史分析
version: 3.0.0
tags: spec, project, validation, generator, tasks, dashboard
---

# spec-engine v3.0

> 项目规格自动生成与验证工具 — 从想法到任务清单的全流程自动化

## 功能一览

| 命令 | 说明 |
|------|------|
| `generate` | 输入项目描述 → 智能提取 → 生成完整 spec |
| `validate` | 验证 spec 完整性，100分制评分 + A/B/C/D 等级 |
| `decompose` | 从 spec 中提取功能 → 自动拆解子任务 + 工时 + 依赖 + 负责人 |
| `analyze` | 扫描目录，分析历史 spec 数据统计 |
| `dashboard` | 生成 Web 仪表盘，可视化所有 spec 状态 |
| `compare` | 对比两个 spec 版本的差异 |

## 快速开始

### generate — 智能生成 spec
```bash
python scripts/generate.py -i <项目描述文件> [-o spec.md] [--format brief|detailed]
```
自动识别技术栈、推断文件结构、估算时间、识别风险。

### validate — 可配置验证
```bash
python scripts/validate.py <spec文件> [--rules rules.json] [--strict] [--json]
```
支持自定义规则、4维检查、100分评分制。

### decompose — 任务拆解（v3.0 新增）
```bash
python scripts/decompose.py -i <spec文件> [-o tasks.md] [--format table|list] [--json]
```
从 spec 中提取功能需求，自动拆解为子任务清单，含工时估算、依赖关系、负责人建议、关键路径分析。

### analyze — 历史分析
```bash
python scripts/analyze.py [--dir <目录>] [--output report.md] [--json]
```

### dashboard — Web 仪表盘（v3.0 新增）
```bash
python scripts/dashboard.py [-d <目录>] [-o dashboard.html]
```
生成深色主题 HTML 仪表盘，展示所有 spec 的评分、技术栈分布、完整性状态。

### compare — 版本对比
```bash
python scripts/compare.py <旧spec> <新spec> [--json]
```

## 文件结构
```
spec-engine/
├── SKILL.md
├── scripts/
│   ├── generate.py      # 智能 spec 生成
│   ├── validate.py      # 可配置验证
│   ├── decompose.py     # 任务拆解（v3.0）
│   ├── analyze.py       # 历史分析
│   ├── dashboard.py     # Web 仪表盘（v3.0）
│   └── compare.py       # 版本对比
└── templates/
    ├── spec-template.md # spec 模板
    └── rules.json       # 验证规则配置
```

## 特点
- 纯 Python 标准库，零外部依赖
- UTF-8 编码，跨平台兼容
- 完全向后兼容 v1/v2

## 适用场景
- Agent 团队写项目 spec → generate
- 提交前检查 → validate
- spec 确认后拆任务 → decompose
- 团队复盘 → analyze + dashboard
