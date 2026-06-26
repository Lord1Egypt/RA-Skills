---
name: self-evolution-cn
slug: self-evolution-cn
version: 2.1.1
homepage: https://clawhub.ai/skills/self-evolution-cn
description: "多 agent 自我进化系统，自动记录学习、错误和功能需求，支持多 agent 统计和自动提升"
---

# Self-Evolution-CN

多 agent 自我进化系统，自动记录学习、错误和功能需求，支持多 agent 统计和自动提升。

## 快速开始

### 一键配置

```bash
cd ~/.openclaw/skills/self-evolution-cn
./scripts/setup.sh
```

### 手动配置

```bash
# 设置共享目录
export SHARED_LEARNING_DIR="/root/.openclaw/shared-learning"
export SHARED_AGENTS="agent1 agent2"

# 创建目录和软链接
mkdir -p "$SHARED_LEARNING_DIR"
cp .learnings/*.md "$SHARED_LEARNING_DIR/"
ln -s "$SHARED_LEARNING_DIR" ~/.openclaw/workspace-agent1/.learnings
ln -s "$SHARED_LEARNING_DIR" ~/.openclaw/workspace-agent2/.learnings

# 启用 hook 和 cron
openclaw hooks enable self-evolution-cn
crontab -e  # 添加：0 0 * * * ~/.openclaw/skills/self-evolution-cn/scripts/trigger-daily-review.sh >> ~/.openclaw/skills/self-evolution-cn/logs/heartbeat-daily.log 2>&1
```

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `setup.sh` | 一键配置 |
| `daily_review.sh` | 自动统计与提升（每日 00:00 执行） |
| `trigger-daily-review.sh` | Cron 触发脚本 |
| `activator.sh` | 任务完成后提醒 |
| `error-detector.sh` | 命令失败时提醒 |
| `extract-skill.sh` | 提取可重用技能 |

## Hook 集成

自动识别并记录：
- **用户纠正**：检测中文关键词（"不对"、"错了"、"错误"、"不是这样"、"应该是"）和英文关键词（"No, that's wrong"、"Actually"、"should be"）
- **命令失败**：检测工具执行失败（非零退出码）和系统级错误（command not found、Permission denied、fatal）
- **知识缺口**：检测中文关键词（"我不知道"、"查不到"、"不知道"、"无法找到"、"找不到"）和英文关键词（"I don't know"、"can't find"、"not sure"）
- **更好的方法**：检测中文关键词（"更好的方法"、"更简单"、"优化"、"改进"）和英文关键词（"better way"、"simpler"、"optimize"、"improve"）

**自动生成元数据：**
- **Pattern-Key**：根据类别自动生成唯一标识（user.correction、knowledge.gap、better.method）
- **Area**：根据类别自动映射到对应区域（行为准则、工作流、工作流改进）

**记录文件：**
- LEARNINGS.md：学习记录（用户纠正、知识缺口、更好的方法）
- ERRORS.md：错误记录（命令失败、系统错误）
- FEATURE_REQUESTS.md：功能需求记录

启用：
```bash
openclaw hooks enable self-evolution-cn
```

### Hook 事件结构

Hook 监听 OpenClaw 事件并从正确字段读取数据：

| 事件 | 读取字段 | 说明 |
|------|----------|------|
| `message:received` | `event.context.content` | 用户消息内容 |
| `tool:after` | `event.context.output` | 工具执行输出 |
| `agent:bootstrap` | `event.context.bootstrapFiles` | 引导文件注入 |

**兼容性：** 同时支持 `event.message` 和 `event.toolOutput` 旧格式。

## 常见问题

### Q: 如何手动执行检查？

A: 直接运行：
```bash
bash ~/.openclaw/skills/self-evolution-cn/scripts/daily_review.sh
```

### Q: 如何控制是否启用自动提升？

A: 设置环境变量 `AUTO_PROMOTE_ENABLED`：
```bash
# 禁用自动提升（仅统计）
AUTO_PROMOTE_ENABLED=false bash ~/.openclaw/skills/self-evolution-cn/scripts/daily_review.sh

# 启用自动提升（默认）
AUTO_PROMOTE_ENABLED=true bash ~/.openclaw/skills/self-evolution-cn/scripts/daily_review.sh
```

### Q: 如何修改共享目录？

A: 设置环境变量：
```bash
export SHARED_LEARNING_DIR="/your/custom/path"
```

### Q: 执行状态和日志在哪里？

A:
- 状态：`$SHARED_LEARNING_DIR/heartbeat-state.json`
- 日志：`$SHARED_LEARNING_DIR/logs/heartbeat-daily.log`

## 详细文档

- `references/format.md` - 记录格式
- `references/promotion.md` - 提升机制
- `references/multi-agent.md` - 多 agent 支持
- `references/hooks-setup.md` - Hook 配置
- `references/openclaw-integration.md` - OpenClaw 集成
- `hooks/openclaw/HOOK.md` - Hook 说明

## 更新

```bash
clawdhub update self-evolution-cn
```

## 版本

当前版本：2.1.1

### 更新日志

**v2.1.1 (2026-04-18)**
- 改进记录反馈：记录完成后自动告知记录的文件名（LEARNINGS.md、ERRORS.md、FEATURE_REQUESTS.md）
- 修改 recordLearning、recordError、recordFeatureRequest 函数返回文件名
- 更新 HOOK.md 文档：说明自动回复机制

**v2.1.0 (2026-04-18)**
- 添加英文关键词支持：支持 "No, that's wrong"、"Actually"、"should be"、"I don't know"、"can't find"、"not sure"、"better way"、"simpler"、"optimize"、"improve"
- 添加系统级错误检测：支持 command not found、No such file、Permission denied、fatal
- 添加 FEATURE_REQUESTS.md 支持：新增功能需求记录文件
- 实现 Pattern-Key 自动生成：根据类别自动生成唯一标识（user.correction、knowledge.gap、better.method）
- 实现 Area 自动生成：根据类别自动映射到对应区域（行为准则、工作流、工作流改进）
- 统一 handler.js 和 handler.ts 功能：确保两个文件功能完全一致
- 更新 HOOK.md 文档：添加新功能说明
- 改进记录反馈：记录完成后自动告知记录的文件名（LEARNINGS.md、ERRORS.md、FEATURE_REQUESTS.md）

**v2.0.4 (2026-04-16)**
- 修复 detectCorrection 函数：移除 toLowerCase()，中文关键词检测不生效
- 修复 detectKnowledgeGap 函数：移除 toLowerCase()
- 修复 detectBetterMethod 函数：移除 toLowerCase()

**v2.0.2 (2026-04-16)**
- 修复 skills 目录下的 handler.js，确保发布到 clawhub 的版本包含正确的修复
- 从 `event.context.content` 读取消息，而非 `event.message`
- 从 `event.context.output` 读取工具输出，而非 `event.toolOutput`

**v2.0.1 (2026-04-16)**
- 修复 Hook 事件结构读取错误：从 `event.context.content` 读取消息，而非 `event.message`
- 修复 Hook 工具输出读取：从 `event.context.output` 读取，而非 `event.toolOutput`
- 添加事件结构说明文档
- 向后兼容旧格式

**v2.0.0 (2026-04-07)**
- 优化提升格式，去除冗余元数据
- 根据 Area 字段自动映射到对应的二级标题
- 修复 Area 字段提取逻辑
- 更新文档说明
- 精简所有说明文档
- 修复 Pattern-Key 匹配逻辑
- 添加无效 Pattern-Key 过滤

**v1.0.6 (2026-04-06)**
- 初始版本
