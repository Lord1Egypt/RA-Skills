# 更新日志 (Changelog)

## [1.0.1] - 2026-04-10

### 🎯 版本概述
本次更新重点优化了 Skill 套件的一致性和联动性，提升了整体质量和可用性。

### ✨ 新增功能

#### 1. 标准化输出格式
- 为所有 7 个核心 Skill 定义了标准包格式
- 新增 `modeling_package.yaml` 完整定义
- 统一包字段结构：`metadata` + `content` + `downstream_specs`

#### 2. 联动命令增强
- 新增 `--from-{skill}` 自动化命令模式
- 所有 downstream 连接添加 `auto_trigger` 和 `command` 配置
- 新增 3 个工作流：
  - `requirement_to_architecture`: 需求到架构
  - `test_driven_deployment`: 测试驱动部署
  - `model_to_development`: 建模到开发

#### 3. 文档体系完善
- 新增 `skill-template.md` Skill 开发模板
- 新增 `CLAUDE.md` Claude Code 指导文件
- 主 SKILL.md 新增示例快速索引表
- 所有 Skill 添加"上游输入"和"下游联动"章节

### 🔧 优化改进

#### modeling-assistant 全面重构
- 简化架构图，与其他 Skill 保持一致
- 添加标准包格式定义
- 添加上游输入说明（从 requirement/architecture 接收）
- 添加下游联动说明（到 sql/etl/dq/test）
- 综合评分从 75 提升至 87

#### 架构图统一
- 所有 Skill 采用统一简洁风格
- 移除复杂 ASCII 框图，改用简洁流程图

#### 参考资料导航统一
- 添加"何时读取"和"场景"列
- 7 个 Skill 格式完全一致

#### skill-connections.yaml 增强
- 添加 `auto_trigger` 标记
- 添加 `command` 命令提示
- 添加 `condition` 部署条件
- 完善标准包字段定义

### 📊 质量提升

| Skill | v1.0.0 | v1.0.1 | 提升 |
|-------|--------|--------|------|
| requirement-analyst | 90 | 92 | +2 |
| architecture-designer | 88 | 90 | +2 |
| modeling-assistant | 75 | 87 | +12 |
| sql-assistant | 82 | 85 | +3 |
| etl-assistant | 84 | 86 | +2 |
| dq-assistant | 84 | 86 | +2 |
| test-engineer | 83 | 85 | +2 |
| **套件整体** | **84** | **88** | **+4** |

### 🐛 修复问题
- 修复 `etl-assistant` 缺少 YAML frontmatter 的问题
- 修复 `test-engineer` 缺少标准包定义的问题
- 修复 `architecture-designer` 联动说明不完整的问题
- 修复 `modeling-assistant` 上游输入路径错误

### 📦 文件变更
- 新增：`CLAUDE.md`, `skill-template.md`, `CHANGELOG.md`
- 更新：所有 `SKILL.md`, `skill-connections.yaml`, `package.json`, `_meta.json`

---

## [1.0.0] - 2026-01-01

### 🎉 初始发布

#### 核心功能
- 7 个数据开发核心模块：
  - requirement-analyst: 需求分析助手
  - architecture-designer: 架构设计助手
  - modeling-assistant: 数据建模助手
  - sql-assistant: SQL 智能开发助手
  - etl-assistant: ETL Pipeline 开发助手
  - dq-assistant: 数据质量检查助手
  - test-engineer: 测试工程师

#### 特色能力
- 端到端数据开发生命周期覆盖
- 模块间智能联动
- 标准化 YAML 包格式
- 企业级最佳实践

#### SkillHub 上架
- 已收录于 SkillHub 平台
- 触发词：数据开发、数据仓库、ETL、SQL 优化等
- 兼容 Claude >=3.5, OpenClaw >=0.8.0
