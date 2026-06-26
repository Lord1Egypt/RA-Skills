# Synapse Brain

**OpenClaw 持久调度 Agent — 跨会话任务管理 + 多 Agent 编排**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](SKILL.md)

---

## 是什么

Synapse Brain 是基于 OpenClaw Managed Agents 架构的持久调度核心。它解决了一个根本问题：

> AI Agent 每次会话都从零开始，无法追踪长期项目进度。

Brain 通过 `state.json` 持久化会话状态，自动路由用户意图到正确的 Skill（synapse-code 或 synapse-wiki），并协调多个子代理并行工作。

## 架构

```
用户请求 → Synapse Brain
            ├── 意图识别 (task_router.py)
            ├── Session 恢复 (state_manager.py)
            ├── 路由到 Skill (code / wiki)
            ├── 子代理调度 (subagent_dispatch.py)
            └── 状态持久化 (state.json)
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/ankechenlab-node/synapse-brain.git
cd synapse-brain

# 运行安装
./install.sh
```

## 快速开始

```bash
# 初始化项目 session
/synapse-brain init my-project "用户系统开发"

# 查看当前状态
/synapse-brain status my-project

# 通过 Brain 调度开发任务（需要 synapse-code 已安装）
/synapse-brain dispatch "实现登录功能" --skill synapse-code --mode lite

# 保存当前进度
/synapse-brain save
```

## 与 Synapse 生态协作

- **[synapse-code](https://github.com/ankechenlab-node/synapse-code)** — 代码开发工作流引擎，被 Brain 调度执行开发任务
- **[synapse-wiki](https://github.com/ankechenlab-node/synapse-wiki)** — 知识库管理系统，被 Brain 调度管理知识

三者配合形成完整闭环：开发 → 知识沉淀 → 查询复用。

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/state_manager.py` | Session 状态持久化（CRUD） |
| `scripts/task_router.py` | 意图识别 + 任务路由 |
| `scripts/session_init.py` | Session 初始化 / 恢复 |
| `scripts/subagent_dispatch.py` | 子代理并行调度 |

## 配置

安装后自动生成 `config.json`，默认配置：

```json
{
  "brain": {
    "state_dir": "~/.openclaw/brain-state",
    "auto_save": true,
    "auto_save_interval": 300,
    "skills": {
      "code": "synapse-code",
      "wiki": "synapse-wiki"
    }
  }
}
```

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
