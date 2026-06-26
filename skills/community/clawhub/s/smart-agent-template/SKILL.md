---
name: smart-agent-template
description: Smart Agent 工作流模板：三重判断机制 + 自动更新 + Context 优化。包含完整的任务执行规范、WBS 拆分、流程豁免阈值、记忆管理等最佳实践。
metadata:
  openclaw:
    emoji: 🤖
---

# Smart Agent Template

Agent 工作流模板，实现高效的任务管理和协作机制。

## 核心特性

### 1. 三重判断机制
- **会话独立性判断**：自动识别任务是否可以在新会话执行，避免 context 膨胀
- **执行者判断**：根据任务类型自动分配给合适的 agent
- **WBS 拆分判断**：复杂任务自动拆分，确保每个子任务可控

### 2. 自动更新
- 启动时自动检查 GitHub/Gitee 更新
- 可配置开关（config/auto_update.yaml）
- 支持静默更新

### 3. Context 优化
- spawn subagent = 新空白 context
- Task Brief 最小化传递（≤ 100 字背景）
- 触发条件：对话 ≥ 15 轮 / context > 80K / 连续同类任务 > 3 次

### 4. 流程豁免阈值
满足所有 5 条可跳过三重判断：
- 单文件操作
- ≤ 3 步
- 无依赖
- 耗时 < 2 分钟
- 纯操作类

## 快速开始

1. 克隆模板
```bash
git clone https://github.com/whhaijun/agent-workflow.git
cd agent-workflow
```

2. 配置身份
编辑 `IDENTITY.md` 定义 agent 角色

3. 启动
按 `AGENTS.md` 启动流程执行

## 文件结构

```
├── AGENTS.md           # 工作规范（核心）
├── IDENTITY.md         # Agent 身份定义
├── config/
│   └── auto_update.yaml  # 自动更新配置
├── scripts/
│   └── auto_update.sh    # 更新脚本
├── memory/
│   └── hot.md           # HOT 层记忆
└── docs/               # 详细文档
```

## 使用场景

- 多 Agent 协作项目
- 需要长期记忆的 Agent
- 复杂任务自动拆分
- 需要版本管理的 Agent 工作流

## 更多文档

- [任务执行规范](docs/TASK_EXECUTION.md)
- [记忆管理](docs/MEMORY_MANAGEMENT.md)
- [多 Agent 协作](docs/MULTI_AGENT_COLLABORATION.md)

## License

MIT
