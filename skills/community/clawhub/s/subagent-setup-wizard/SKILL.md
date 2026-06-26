---
name: subagent-setup-wizard
description: |
  Subagent 启用配置向导。解决 Subagent 版本查询、启用配置、并发场景最佳实践、资源监控等问题。

  **当以下情况时使用此 Skill**：
  (1) 查询 Subagent 是哪个版本引入的
  (2) 需要启用 Subagent 配置向导
  (3) 并发场景最佳实践咨询
  (4) 资源占用监控与优化
  (5) 用户提到"subagent"、"并发"、"多 agent"
---

# 🤖 Subagent 配置向导

## 版本信息

- **版本**: v1.0.0
- **作者**: 郑宇航
- **适用场景**: Subagent 启用、配置、并发优化

---

## 🚨 常见问题快速索引

| 问题 | 解决方案 | 难度 |
|------|----------|------|
| Subagent 版本查询 | [版本历史](#版本历史) | ⭐ |
| 启用 Subagent | [启用向导](#启用-subagent) | ⭐⭐ |
| 并发配置 | [最佳实践](#并发最佳实践) | ⭐⭐⭐ |
| 资源监控 | [监控方案](#资源监控) | ⭐⭐ |

---

## 📋 Subagent 是什么？

**Subagent** 是 OpenClaw 的子代理系统，允许主 Agent 创建和管理多个子 Agent 并行执行任务。

**核心能力**:
- ✅ 任务拆分与并行执行
- ✅ 独立的上下文和工具集
- ✅ 持久化会话支持
- ✅ 资源隔离与监控

---

## 📊 版本历史

| OpenClaw 版本 | Subagent 支持 | 说明 |
|---------------|---------------|------|
| **2026.3.0** | ✅ 基础支持 | 引入 `sessions_spawn` 和 `subagents` 工具 |
| **2026.3.5** | ✅ ACP 模式 | 增加 ACP 编码模式支持 |
| **2026.3.7** | ✅ 持久化 | Session History 持久化、Persistent Channel Bindings |
| **2026.4.0+** | ✅ 完整支持 | 默认启用，支持 steer 引导 |

**为什么不被默认使用？**:
- Subagent 会消耗更多 API 配额
- 需要合理的任务拆分策略
- 适合大型项目，简单任务不需要

---

## 🛠️ 启用 Subagent

### 步骤 1: 检查版本

```bash
openclaw -v
# 需要 >= 2026.3.0
```

### 步骤 2: 查看可用 Agents

```bash
openclaw agents list
# 或
agents_list
```

### 步骤 3: 创建子 Agent

**交互式向导**:

```
用户：创建子 Agent

机器人：
🤖 Subagent 配置向导

请选择运行时类型：
1. ACP 模式 - 编码任务（专业编码环境）
2. Subagent 模式 - 通用任务（继承主代理能力）

请输入序号 (1-2):
```

**配置参数**:

```json
{
  "runtime": "acp",
  "mode": "session",
  "thread": true,
  "timeout": 3600,
  "model": "qwen3.5-plus"
}
```

**使用工具**: `sessions_spawn`, `subagents`

---

## 💡 并发最佳实践

### 场景 1: 单会话串行（推荐默认）

**适用**: 简单任务、对话式交互

**配置**:
```json
{
  "concurrency": 1,
  "mode": "session",
  "thread_bound": true
}
```

**优势**:
- ✅ 资源消耗低
- ✅ 上下文连贯
- ✅ 易于调试

---

### 场景 2: 多 Agent 并行

**适用**: 大型项目、多任务处理

**配置**:
```json
{
  "concurrency": 3,
  "max_subagents": 5,
  "mode": "session",
  "timeout": 7200
}
```

**示例**:
```
用户：开发一个博客系统

机器人创建 3 个子 Agent:
1. 前端 Agent - React + TypeScript
2. 后端 Agent - Node.js + Express
3. 数据库 Agent - PostgreSQL Schema

并行执行，最后整合结果
```

**使用工具**: `sessions_spawn`, `subagents`

---

### 场景 3: 研究分析任务

**适用**: 资料搜集、文档整理

**配置**:
```json
{
  "runtime": "subagent",
  "mode": "run",
  "concurrency": 2
}
```

**示例**:
```
用户：研究 OpenClaw 架构

机器人创建 2 个子 Agent:
1. 文档搜集 Agent - 抓取官方文档
2. 代码分析 Agent - 分析 GitHub 源码

输出整合报告
```

---

## 📊 资源配置建议

### 推荐配置表

| 任务类型 | 并发数 | 超时 (秒) | 模式 | 说明 |
|----------|--------|-----------|------|------|
| 简单对话 | 1 | 300 | session | 默认配置 |
| 文档处理 | 2 | 600 | run | 并行处理 |
| 代码生成 | 3 | 3600 | session | ACP 模式 |
| 大型项目 | 5 | 7200 | session | 多 Agent 并行 |
| 研究分析 | 2 | 1800 | run | subagent 模式 |

### 资源限制

```json
{
  "limits": {
    "max_subagents": 10,
    "max_concurrent": 5,
    "max_timeout": 7200,
    "api_quota_per_subagent": 100
  }
}
```

---

## 🔍 资源监控

### 监控命令

```bash
# 查看所有子 Agent 状态
subagents list

# 查看特定子 Agent 详情
subagents describe <id>

# 查看资源占用
openclaw resources
```

### 监控指标

| 指标 | 阈值 | 告警 |
|------|------|------|
| CPU 使用率 | > 80% | ⚠️ 警告 |
| 内存占用 | > 2GB | ⚠️ 警告 |
| API 调用/分钟 | > 100 | ⚠️ 限流风险 |
| 子 Agent 数量 | > 10 | ❌ 超限 |

### 优化建议

**CPU 过高**:
- 减少并发数
- 增加任务间隔
- 使用更轻量模型

**内存过高**:
- 限制上下文长度
- 定期清理会话
- 使用 run 模式而非 session

**API 限流**:
- 降低并发数
- 增加延迟
- 使用缓存

---

## 🛠️ 配置模板

### 模板 1: 开发环境

```json
{
  "subagents": {
    "enabled": true,
    "max_concurrent": 3,
    "default_runtime": "acp",
    "default_mode": "session",
    "timeout": 3600,
    "model": "qwen3.5-plus"
  }
}
```

### 模板 2: 生产环境

```json
{
  "subagents": {
    "enabled": true,
    "max_concurrent": 2,
    "default_runtime": "subagent",
    "default_mode": "run",
    "timeout": 1800,
    "model": "qwen3.5-plus",
    "quota_limit": 1000
  }
}
```

### 模板 3: 高性能模式

```json
{
  "subagents": {
    "enabled": true,
    "max_concurrent": 5,
    "default_runtime": "acp",
    "default_mode": "session",
    "timeout": 7200,
    "model": "qwen3.5-plus",
    "auto_cleanup": true
  }
}
```

---

## 🔧 一键配置脚本

### 脚本 1: 启用 Subagent

```bash
#!/bin/bash
# enable-subagent.sh

echo "🤖 启用 Subagent..."

# 1. 检查版本
VERSION=$(openclaw -v | grep -oP '\d+\.\d+\.\d+')
if [[ "$VERSION" < "2026.3.0" ]]; then
  echo "❌ OpenClaw 版本过低，需要 >= 2026.3.0"
  exit 1
fi

# 2. 配置 Subagent
openclaw config set subagents.enabled true
openclaw config set subagents.max_concurrent 3
openclaw config set subagents.default_mode session

# 3. 验证配置
openclaw config get subagents

echo "✅ Subagent 已启用！"
```

### 脚本 2: 并发优化

```bash
#!/bin/bash
# optimize-concurrency.sh

echo "⚙️ 优化并发配置..."

# 根据系统资源自动配置
CPU_CORES=$(nproc)
MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')

if [ $MEMORY_GB -gt 8 ]; then
  CONCURRENCY=5
elif [ $MEMORY_GB -gt 4 ]; then
  CONCURRENCY=3
else
  CONCURRENCY=2
fi

openclaw config set subagents.max_concurrent $CONCURRENCY

echo "✅ 并发数设置为 $CONCURRENCY"
```

---

## 📝 使用示例

### 示例 1: 创建编码子 Agent

```
用户：创建一个 Next.js 博客系统

机器人：
🤖 正在创建子 Agent...

运行时：ACP 模式
模式：Session
超时：3600 秒
模型：qwen3.5-plus

✅ 子 Agent sess_abc123 已创建
📋 任务：使用 Next.js 14 创建博客系统
⏱️ 预计耗时：15-20 分钟

使用 /steer sess_abc123 可以引导方向
使用 /status 查看进度
```

### 示例 2: 多 Agent 并行

```
用户：分析这 10 篇文档

机器人：
🤖 创建 3 个子 Agent 并行处理...

Agent 1: 分析文档 1-3
Agent 2: 分析文档 4-6
Agent 3: 分析文档 7-10

✅ 3 个子 Agent 已创建
📊 预计耗时：5-8 分钟（串行需要 15 分钟）
```

---

## 🆘 故障排查

### 问题 1: 子 Agent 无法创建

**原因**: 版本过低或配置错误

**解决**:
```bash
# 检查版本
openclaw -v

# 重置配置
openclaw config reset subagents

# 重启
openclaw gateway restart
```

### 问题 2: 子 Agent 卡住

**原因**: 超时设置过短或任务复杂

**解决**:
```bash
# 增加超时
openclaw config set subagents.timeout 7200

# 终止卡住的子 Agent
subagents kill <id>
```

### 问题 3: API 限流

**原因**: 并发过高

**解决**:
```bash
# 降低并发
openclaw config set subagents.max_concurrent 2

# 增加延迟
openclaw config set subagents.delay 1000
```

---

## 📚 相关资源

- [OpenClaw 子代理文档](https://my.feishu.cn/docx/IgkrdJvgxowAuMxAAkAcDaCOntf)
- [并发最佳实践](https://docs.openclaw.ai)
- [资源监控指南](https://docs.openclaw.ai/monitoring)

---

## 📊 版本历史

### v1.0.0 (2026-04-09)
- ✅ Subagent 版本历史说明
- ✅ 启用配置向导
- ✅ 并发最佳实践
- ✅ 资源监控方案
- ✅ 一键配置脚本

---

**最后更新**: 2026-04-09  
**作者**: 郑宇航
