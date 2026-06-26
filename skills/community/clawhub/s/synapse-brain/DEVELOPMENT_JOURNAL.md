# Synapse Brain 开发日记

## 项目起源

Synapse Brain 始于 2026-04-10，是 Synapse Skills v2.0.0 架构升级的核心组件。

基于 OpenClaw Managed Agents 架构，解决了一个根本问题：AI Agent 每次会话从零开始，无法追踪长期项目进度。Brain 通过 `state.json` 持久化会话状态，自动路由用户意图到正确的 Skill，并协调多个子代理并行工作。

---

## 开发阶段

### Phase 1: 架构设计
- 设计 Brain/Hands 架构
- 定义 state.json 持久化格式
- 确定 4 种运行模式（standalone/lite/full/parallel）

### Phase 2: 核心脚本开发
- state_manager.py — Session 状态持久化（CRUD + archive + list）
- task_router.py — 意图识别 + 任务路由（6 种意图分类）
- session_init.py — Session 初始化 / 恢复
- subagent_dispatch.py — 子代理并行调度

### Phase 3: Agent 定义
- SOUL.md — Brain Agent 角色定义、决策逻辑、输出格式
- SKILL.md — 技能接口文档、命令速查、架构说明

### Phase 4: 发布准备
- 审计并修复 YAML frontmatter 格式
- 添加 LICENSE (MIT)、README.md、.gitignore
- 修正安装指引（避免 bootstrap 问题）
- 清理 __pycache__ 等构建产物
- 模拟测试验证：意图分类 8/8, CRUD 全部通过

---

## 关键决策

### 1. Brain 定位
Brain 不是执行者，是指挥者。不直接写代码或管理知识，而是调度 synapse-code 和 synapse-wiki 完成工作。

### 2. 状态存储
选择 JSON 文件而非数据库，理由：
- 轻量，无需额外依赖
- 人类可读，便于调试
- 项目级隔离，每个 project 独立 state.json

### 3. 意图路由
基于关键词匹配 + 优先级 + anti-keywords 机制，而非 ML 模型。理由：
- 零依赖，立即可用
- 可解释，易调试
- v2.1.0 可升级为 ML 增强

### 4. 个人路径清除
所有硬编码的 `/Users/leo/` 路径统一替换为 `~/` 或相对路径，确保公开发布安全。

---

## 测试报告

| 模块 | 测试项 | 结果 |
|------|--------|------|
| task_router | 8 种意图分类 | 8/8 通过 |
| state_manager | CRUD + list + archive | 全部通过 |
| session_init | new / resume / auto | 全部通过 |
| subagent_dispatch | dispatch / complete / report | 全部通过 |
| Python 语法 | 4 个脚本 | 全部通过 |
| Shell 语法 | install.sh | 通过 |

---

## 经验教训

### 有效做法
- 审计流程自动化（三个 skills 并行检查）
- 模拟测试先于推送
- 统一 GitHub org 命名

### 踩过的坑
1. **YAML frontmatter 格式** — JSON 流语法在某些解析器下不支持，改为纯 YAML
2. **SOUL.md log.md 引用** — 文档引用了不存在的文件，改为 state.json 内部 log 字段
3. **远程 URL 混乱** — 三个 repo 的 remote origin 曾互相指向错误地址，需逐个确认

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v2.0.0 | 2026-04-10 | 初始发布 |

---

## 未来规划

### v2.0.1
- task_router ML 增强 — 基于历史路由改进分类准确率
- 子代理自动重试 — 失败任务智能重试
- 进度通知 — Telegram/飞书推送任务状态

### v2.0.2
- synapse-design — 设计创作 Skill
- synapse-analytics — 数据分析 Skill
- Brain Skill Marketplace
- 跨项目知识图谱
