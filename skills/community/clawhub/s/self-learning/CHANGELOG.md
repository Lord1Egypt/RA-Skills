# 更新日志

所有重要的项目变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [3.0.0] - 2026-03-05

### 🚀 重大更新：双引擎学习系统

#### 新增
- ✨ **学习记录系统** (.learnings/ 目录)
  - `LEARNINGS.md` - 纠正、知识缺口、最佳实践
  - `ERRORS.md` - 命令失败、异常
  - `FEATURE_REQUESTS.md` - 功能请求
- ✨ **条目 ID 系统**
  - `LRN-YYYYMMDD-XXX` (学习)
  - `ERR-YYYYMMDD-XXX` (错误)
  - `FEAT-YYYYMMDD-XXX` (功能)
- ✨ **优先级和状态管理**
  - Priority: low/medium/high/critical
  - Status: pending/in_progress/resolved/promoted/wont_fix
- ✨ **Pattern-Key 追踪** - 检测重复模式 (Recurrence-Count >= 3 自动提升)
- ✨ **提升规则** - 自动将学习内容提升到 SOUL.md/AGENTS.md/TOOLS.md
- ✨ **Hook 集成** (OpenClaw)
  - onSessionStart: 检查待处理高优先级条目
  - onPromptSubmit: 检测用户纠正信号
- ✨ **CLI 命令** (learning_manager.py)
  - `add-learning` - 添加学习记录
  - `add-error` - 添加错误记录
  - `add-feature` - 添加功能请求
  - `list-pending` - 查看待处理条目
  - `check-recurring` - 检查重复模式

#### 改进
- 🚀 重构主脚本，模块化设计 (LearningManager 类)
- 🚀 增强 AI 分析 prompt，支持学习记录判断
- 🚀 代码结构优化，易于扩展

## [2.0.0] - 2026-03-05

### 新增
- ✨ 支持多平台部署 (不再局限于 OpenClaw)
- ✨ 配置文件支持 (config.yaml)
- ✨ 完整的日志系统
- ✨ 执行历史记录
- ✨ 文件验证机制
- ✨ 回滚功能
- ✨ 预览模式 (--dry-run)

### 改进
- 🚀 重构代码为面向对象架构
- 🚀 工作目录自动检测优化
- 🚀 错误处理增强
- 🚀 配置灵活性提升

### 修复
- 🐛 修复多 Agent 工作目录冲突问题
- 🐛 修复备份清理逻辑

### 变更
- ⚠️ 配置文件结构变更
- ⚠️ 命令行参数调整

## [1.1.0] - 2026-03-05

### 新增
- ✨ 支持多 Agent 工作目录自动检测
- ✨ 命令行参数 --workspace
- ✨ 环境变量支持

### 改进
- 🚀 启动信息优化
- 🚀 备份目录隔离

## [1.0.0] - 2026-03-05

### 新增
- ✨ 初始版本
- ✨ 基础自我学习功能
- ✨ 8 个核心配置文件支持
- ✨ 自动备份机制
