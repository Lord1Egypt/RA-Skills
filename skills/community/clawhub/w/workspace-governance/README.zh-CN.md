# workspace-governance

[English](README.md)

一个方法论优先的 AI Agent 工作区治理技能。  
目标是让智能体在“可执行、可回滚、可追溯”的前提下整理工作区，而不是强制固定目录模板。

## 文档元信息

- 作者: Mars
- GitHub: Mars2003
- 日期: 2026-04-28

## 核心原则（简版）

- 先边界，后结构
- 先方案，后执行
- 可逆优先
- 删除和批量移动必须确认
- 默认不触碰敏感文件和版本控制元数据

## 快速开始

### 1) 安装技能

```bash
# Claude Code（全局）
mkdir -p ~/.claude/skills/workspace-governance
cp SKILL.md ~/.claude/skills/workspace-governance/

# Cursor（项目级）
mkdir -p .cursor/skills/workspace-governance
cp SKILL.md .cursor/skills/workspace-governance/
```

### 2) 项目级适配（可选但推荐）

仓库已提供 `SKILL_ADAPT.yaml`，用于声明边界、保护规则、执行批次和日志策略。  
没有它也能用，但有它更稳定、更一致、更可审计。

### 3) 推荐触发语句

- “整理工作区”
- “先审计再清理”
- “归档项目 xxx”
- “创建项目 yyy 并设置治理边界”

### 4) 一键校验（推荐）

```bash
make check
```

## 目录建议

除 `SKILL.md` 外，建议按需扩展以下目录：

- `references/`：详细手册、流程说明、策略示例
- `assets/`：图示、截图、可视化素材
- `scripts/`：辅助脚本（检查、批处理、导出等）
- `tools/`：工具配置、扩展工具说明

## 详细文档

- 中文治理手册（详细版）：`references/治理手册.zh-CN.md`
- 最小运行示例：`examples/minimal-governance-run.md`

## 项目信息

- 版本日志：`CHANGELOG.md`
- 贡献指南：`CONTRIBUTING.md`

## 许可

MIT
