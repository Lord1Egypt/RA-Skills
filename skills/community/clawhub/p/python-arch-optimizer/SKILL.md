---
name: python-arch-optimizer
description: Python 项目架构优化技能。用于分析和重构 Python 项目结构，使其符合最佳实践。使用场景：(1) 评估现有项目架构，(2) 重构目录结构，(3) 优化依赖管理，(4) 改进代码组织，(5) 建立测试架构，(6) 配置 CI/CD
---

# Python 架构优化器

本技能帮助优化 Python 项目的整体架构，使其更符合现代 Python 工程最佳实践。

## 核心能力

### 1. 目录结构优化
- 按功能/模块划分项目
- 分离配置、业务逻辑、测试
- 符合 PEP 8 和 Python 社区惯例

### 2. 依赖管理
- `requirements.txt` / `pyproject.toml` / `poetry` 配置
- 依赖分类（生产/开发/可选）
- 版本锁定策略

### 3. 代码组织
- 包/模块设计
- 导入结构优化
- 关注点分离

### 4. 测试架构
- pytest 配置
- 测试目录结构
- 覆盖率配置

### 5. 工程化配置
- pre-commit 钩子
- linting 配置（ruff/black/mypy）
- CI/CD 模板

## 工作流程

### 步骤 1: 分析现有架构
```bash
# 使用分析脚本
python scripts/analyze_project.py <project-path>
```

读取项目结构，识别问题：
- 循环依赖
- 过深的嵌套
- 缺失的 `__init__.py`
- 测试覆盖率低
- 配置硬编码

### 步骤 2: 生成优化建议
参考 `references/best-practices.md` 生成具体建议。

### 步骤 3: 执行重构（需用户确认）

**⚠️ 安全警告：** 重构操作会移动/创建文件，可能影响现有项目。

**必须获得用户明确确认后**才能执行迁移脚本：
```bash
# 用户确认后执行（支持：yes / y / 确认 / 是）
python scripts/migrate_project.py <project-path>
```

**回滚策略：**
- 迁移前自动备份到 `<project-path>.backup.<timestamp>/`
- 提供 `--dry-run` 预览变更
- 失败时自动恢复备份

### 步骤 4: 验证
运行测试和 lint 检查确保重构后功能正常。

## 参考文档

- **最佳实践**: `references/best-practices.md` - Python 项目架构详细指南

## 脚本工具

- `scripts/analyze_project.py` - 项目结构分析
- `scripts/generate_structure.py` - 生成推荐结构
- `scripts/migrate_project.py` - 执行迁移（支持 --dry-run 预览、自动备份、回滚）

### 迁移脚本安全机制

```bash
# 1. 预览模式（不会修改任何文件）
python scripts/migrate_project.py ./my-project --dry-run

# 2. 保存计划供审查
python scripts/migrate_project.py ./my-project --plan migration-plan.json

# 3. 用户确认后执行（自动备份）
python scripts/migrate_project.py ./my-project

# 4. 失败时自动回滚到备份
```

## 触发条件

当用户提到：
- "优化 Python 项目结构"
- "重构 Python 代码架构"
- "Python 项目目录怎么组织"
- "改进 Python 工程化"
- "Python 最佳实践"
