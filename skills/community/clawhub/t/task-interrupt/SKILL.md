# Task Interrupt Skill - 任务打断机制

## 概述

任务打断机制是一个用于控制和管理OpenClaw Agent任务执行的技能。它解决了Agent执行任务时卡住、运行时间过长或用户想中途终止的问题。

## 问题场景

- Agent执行长时间任务时用户无法中断
- 任务卡住或陷入死循环时无停止机制
- 用户需要中途放弃当前任务
- 需要优雅的资源清理和状态保存

## 核心架构

### 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              飞书群聊                                    │
│                   用户发送: /stop  或  "中断"                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ Webhook/消息事件
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        主 Agent (maojingli)                             │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────────────┐ │
│  │  消息监听器  │───▶│  中断指令识别器   │───▶│  Subagent 管理器      │ │
│  │              │    │  /stop, 中断      │    │  sessions_*           │ │
│  │              │    │  cancel, abort    │    │                       │ │
│  └──────────────┘    └──────────────────┘    └───────────┬───────────┘ │
│                                                            │             │
│                          ┌─────────────────────────────────┘             │
│                          │                                                │
│                          ▼                                                │
│              ┌───────────────────────┐                                   │
│              │  中断信号发射器        │                                   │
│              │  1. 写入中断标志文件  │                                   │
│              │  2. process.kill()    │                                   │
│              └───────────────────────┘                                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ 中断信号 (信号量/标志文件)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Subagent (maoxiami 等)                               │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────────────┐ │
│  │ 心跳/轮询器  │───▶│  中断检测器       │───▶│  任务执行器 (可中断)   │ │
│  │ (每5秒检查)  │    │  检查标志文件    │    │  exec/tool calls      │ │
│  └──────────────┘    └──────────────────┘    └───────────┬───────────┘ │
│        ▲                                               │               │
│        │                                               ▼               │
│        │                                    ┌───────────────────────┐   │
│        │                                    │  安全停止处理器        │   │
│        │                                    │  1. 保存检查点        │   │
│        │                                    │  2. 清理临时文件      │   │
│        │                                    │  3. 释放资源          │   │
│        └────────────────────────────────────┴───────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## 组件说明

### 1. 中断指令识别器（主Agent）

识别来自用户的打断指令：
- `/stop`、`/中断`、`/cancel`、`/abort`
- `停止`、`中断`等关键词

### 2. 中断信号发射器（主Agent）

将中断信号传递给运行中的subagent：
- 写入中断标志文件到 `/tmp/agent-stop-{sessionId}.flag`
- 可选：发送 SIGINT 信号到子进程
- 调用 `sessions_kill` 作为最终手段

### 3. 中断检测器（Subagent）

轮询检查中断标志：
- 默认每5秒检查一次
- 发现标志后触发安全停止流程
- 自动清理过期标志（60秒）

### 4. 安全停止处理器（Subagent）

优雅停止并清理资源：
- 保存当前检查点状态
- 清理临时文件和连接
- 取消定时任务
- 清除中断标志
- 通知主Agent

## 使用说明

### 1. 在主Agent中集成中断功能

在主Agent的消息处理流程中添加中断指令识别和发射逻辑。参考设计文档中的代码示例。

### 2. 在Subagent中启用中断检测

Subagent需要在启动时调用 `startInterruptPolling()`，并在任务关键点保存检查点 `saveCheckpoint()`。

#### 基本用法：

```javascript
const interruptible = new InterruptibleAgent(sessionId);

// 启动中断轮询
await interruptible.startInterruptPolling();

try {
  // 保存检查点
  await interruptible.saveCheckpoint('task_start', { step: 1 });

  // 执行任务...
  await doLongRunningTask();

  // 保存检查点
  await interruptible.saveCheckpoint('task_complete', { success: true });

} catch (error) {
  if (error.message === 'INTERRUPTED') {
    // 处理被中断的情况
    console.log('任务被用户中断');
  }
} finally {
  // 停止轮询
  await interruptible.stopInterruptPolling();
}
```

### 3. 命令行工具

技能提供了三个Shell脚本用于手动测试和管理：

#### create-stop-flag.sh - 创建停止标志

```bash
./scripts/create-stop-flag.sh <sessionId> [reason]
```

示例：
```bash
./scripts/create-stop-flag.sh abc123 "User requested stop"
```

#### check-stop-flag.sh - 检查停止标志

```bash
./scripts/check-stop-flag.sh <sessionId> [maxAgeSeconds]
```

返回码：
- 0: 标志存在且在有效期内
- 1: 标志不存在或已过期

示例：
```bash
if ./scripts/check-stop-flag.sh abc123 60; then
  echo "检测到中断请求"
fi
```

#### clear-stop-flag.sh - 清除停止标志

```bash
./scripts/clear-stop-flag.sh <sessionId>
```

示例：
```bash
./scripts/clear-stop-flag.sh abc123
```

## API 参考

### InterruptibleAgent 类

#### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| sessionId | string | 当前会话ID |
| interruptCheckInterval | number | 轮询间隔（毫秒，默认5000） |
| isInterrupted | boolean | 是否已中断 |
| checkpoints | Array | 已保存的检查点列表 |

#### 方法

##### startInterruptPolling()

启动中断检测轮询。

```javascript
await agent.startInterruptPolling();
```

##### stopInterruptPolling()

停止中断检测轮询。

```javascript
await agent.stopInterruptPolling();
```

##### checkForInterrupt()

手动检查中断标志（通常自动调用）。

```javascript
const flag = await agent.checkForInterrupt();
// 返回 null 或 { sessionId, reason, timestamp, signal }
```

##### saveCheckpoint(name, data)

保存任务检查点。

```javascript
await agent.saveCheckpoint('step1', { processed: 100, total: 200 });
```

##### getLastCheckpoint()

获取最后一个检查点。

```javascript
const checkpoint = agent.getLastCheckpoint();
```

##### handleInterrupt(flag)

处理中断（内部调用）。

```javascript
await agent.handleInterrupt(flag);
```

### SafeStopHandler 类

提供安全停止和资源清理功能。

#### 方法

##### stop(reason)

执行完整的安全停止流程。

```javascript
const handler = new SafeStopHandler(agent);
const result = await handler.stop('user_stop');
// 返回 { success: boolean, checkpoint?: object, reason?: string, error?: string }
```

##### saveState()

保存Agent状态到 `/tmp/agent-state/{sessionId}.json`。

```javascript
const statePath = await handler.saveState();
```

##### cleanupTempFiles()

清理临时文件模式：
- `/tmp/agent-work/{sessionId}/*`
- `/tmp/agent-downloads/{sessionId}/*`

```javascript
await handler.cleanupTempFiles();
```

##### closeConnections()

关闭数据库连接和文件句柄。

```javascript
await handler.closeConnections();
```

##### cancelScheduledTasks()

取消所有定时任务。

```javascript
await handler.cancelScheduledTasks();
```

## 文件结构

```
task-interrupt/
├── SKILL.md                 # 本文档
├── instructions.md          # Agent指令说明
├── claw.json                # 技能元数据
└── scripts/
    ├── create-stop-flag.sh  # 创建停止标志
    ├── check-stop-flag.sh   # 检查停止标志
    └── clear-stop-flag.sh   # 清除停止标志
```

## 文件路径规范

中断标志文件：`/tmp/agent-stop-{sessionId}.flag`

状态保存文件：`/tmp/agent-state/{sessionId}.json`

标志文件格式：

```json
{
  "sessionId": "abc123",
  "timestamp": 1742345678901,
  "reason": "user_request",
  "signal": "SIGINT"
}
```

## 配置选项

可通过环境变量调整行为：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| INTERRUPT_CHECK_INTERVAL | 5000 | 轮询间隔（毫秒） |
| INTERRUPT_FLAG_DIR | /tmp/agent-stop | 标志文件目录 |
| INTERRUPT_FLAG_MAX_AGE | 60 | 标志最大有效期（秒） |
| AGENT_STATE_DIR | /tmp/agent-state | 状态保存目录 |

## 安全考虑

- 中断标志文件应具有适当权限（0600）
- 只允许删除自己session的标志文件
- 状态文件可能包含敏感数据，应定期清理
- 清理资源时应确保连接正确关闭

## 故障排除

### 中断没有生效

1. 检查Subagent是否已启动轮询：`startInterruptPolling()`
2. 确认标志文件路径是否正确：`/tmp/agent-stop-{sessionId}.flag`
3. 检查轮询间隔是否过短或过长

### 中断后资源未释放

1. 检查 `safeStopHandler.stop()` 是否完整执行
2. 确认数据库连接和文件句柄是否全部关闭
3. 查看临时文件是否已清理

### 标志文件未自动清除

1. 检查文件权限
2. 确认 `clear-stop-flag.sh` 是否执行成功
3. 标志文件60秒后自动过期

## 示例：完整集成

```javascript
// interruptible-agent.js
const path = require('path');
const { exec } = require('child_process');

class InterruptibleAgent {
  constructor(sessionId, options = {}) {
    this.sessionId = sessionId;
    this.interruptCheckInterval = options.interval || 5000;
    this.isInterrupted = false;
    this.checkpoints = [];
    this.pollingTimer = null;
  }

  startInterruptPolling() {
    this.pollingTimer = setInterval(async () => {
      await this.checkForInterrupt();
    }, this.interruptCheckInterval);
  }

  stopInterruptPolling() {
    if (this.pollingTimer) {
      clearInterval(this.pollingTimer);
      this.pollingTimer = null;
    }
  }

  async checkForInterrupt() {
    try {
      const flagPath = `/tmp/agent-stop-${this.sessionId}.flag`;
      if (await fs.pathExists(flagPath)) {
        const content = await fs.readFile(flagPath, 'utf8');
        const flag = JSON.parse(content);

        console.log(`[中断] 检测到中断信号: ${flag.reason}`);
        this.isInterrupted = true;
        await this.handleInterrupt(flag);
      }
    } catch (error) {
      console.error(`[中断] 检查失败: ${error.message}`);
    }
  }

  saveCheckpoint(name, data) {
    const checkpoint = {
      name,
      data,
      timestamp: Date.now()
    };
    this.checkpoints.push(checkpoint);
    console.log(`[检查点] 已保存: ${name}`);
  }

  getLastCheckpoint() {
    return this.checkpoints[this.checkpoints.length - 1] || null;
  }

  async handleInterrupt(flag) {
    console.log('[中断] 开始安全停止流程...');

    this.stopInterruptPolling();
    await this.saveState();
    await this.cleanup();
    await this.clearFlag(flag);

    // 通知主Agent
    await this.notifyMainAgent({
      interrupted: true,
      checkpoint: this.getLastCheckpoint(),
      reason: flag.reason
    });
  }

  async clearFlag(flag) {
    const flagPath = `/tmp/agent-stop-${flag.sessionId}.flag`;
    if (await fs.pathExists(flagPath)) {
      await fs.remove(flagPath);
    }
  }

  async saveState() {
    const state = {
      sessionId: this.sessionId,
      checkpoints: this.checkpoints,
      timestamp: Date.now()
    };
    const stateDir = '/tmp/agent-state';
    await fs.ensureDir(stateDir);
    await fs.writeJson(path.join(stateDir, `${this.sessionId}.json`), state);
    console.log(`[状态] 已保存`);
  }

  async cleanup() {
    // 清理临时文件
    const tempDir = `/tmp/agent-work/${this.sessionId}`;
    if (await fs.pathExists(tempDir)) {
      await fs.remove(tempDir);
    }

    // 关闭连接
    if (this.db) await this.db.end();
    if (this.fileHandles) {
      for (const fh of this.fileHandles) {
        await fh.close();
      }
    }

    // 取消定时任务
    if (this.schedules) {
      for (const s of this.schedules) {
        clearTimeout(s.timer);
        clearInterval(s.interval);
      }
    }

    console.log('[清理] 完成');
  }

  async notifyMainAgent(result) {
    // 实现通知逻辑
    console.log('[通知]', result);
  }
}

module.exports = InterruptibleAgent;
```

## 性能影响

- 轮询间隔建议5-10秒
- 检查点保存频率根据任务重要性调整
- 状态保存使用异步IO，避免阻塞任务执行

## 测试

提供测试脚本验证功能：

```bash
# 测试1: 创建标志
./scripts/create-stop-flag.sh test-session "test reason"

# 测试2: 检查标志
./scripts/check-stop-flag.sh test-session 60

# 测试3: 清除标志
./scripts/clear-stop-flag.sh test-session
```

## 版本历史

- **1.0.0** - 初始版本
  - 基础中断标志文件机制
  - 轮询检测（5秒间隔）
  - 安全停止流程
  - Shell命令行工具

## 相关链接

- [OpenClaw 官方文档](https://openclaw.org/docs)
- [AgentSkill 规范](https://clawhub.com/specs/agent-skill)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT
