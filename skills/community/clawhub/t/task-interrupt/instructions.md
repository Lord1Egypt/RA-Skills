# Task Interrupt - 任务打断机制

## 你的角色

你是一个具备任务中断能力的助手。当用户要求停止当前任务时，你需要：
1. 检测中断信号
2. 保存当前状态到检查点
3. 优雅地清理资源
4. 通知主Agent任务已中断

## 启动规则

每次收到可中断的长任务时：

1. **初始化中断检测**
   ```javascript
   const InterruptibleAgent = require('task-interrupt');
   const agent = new InterruptibleAgent(sessionId, { interval: 5000 });
   await agent.startInterruptPolling();
   ```

2. **任务执行中定期保存检查点**
   ```javascript
   await agent.saveCheckpoint('milestone_name', { data: '...' });
   ```

3. **任务结束时清理**
   ```javascript
   await agent.stopInterruptPolling();
   ```

## 中断检测

轮询机制每5秒检查一次标志文件：
- 标志文件：`/tmp/agent-stop-{sessionId}.flag`
- 如果文件存在且未过期（60秒内），触发中断流程
- 中断后自动清除标志文件

## 检查点使用

在长任务的关键节点保存检查点：

```javascript
// 开始
await agent.saveCheckpoint('start', { step: 'initialization' });

// 中期
await agent.saveCheckpoint('processing', { completed: 50, total: 100 });

// 完成前
await agent.saveCheckpoint('finalizing', { ready: true });
```

检查点可用于：
- 中断后恢复任务（如果支持）
- 提供进度反馈给用户
- 调试和日志记录

## 中断处理

当检测到中断时：

1. 自动停止轮询
2. 保存当前状态
3. 清理临时文件
4. 关闭所有连接
5. 取消定时任务
6. 通知主Agent
7. 清除中断标志

**重要**：不要抛出未处理的异常，使用回调或Promise返回状态。

## 工具脚本

提供命令行工具用于测试和管理：

```bash
# 手动创建中断标志（主Agent用）
./scripts/create-stop-flag.sh <sessionId> [reason]

# 检查中断标志（Subagent用）
./scripts/check-stop-flag.sh <sessionId> [maxAgeSeconds]

# 清除中断标志
./scripts/clear-stop-flag.sh <sessionId>
```

## 集成到主Agent

主Agent需要：

1. 监听飞书消息，识别 `/stop` 等关键词
2. 获取当前运行中session的ID
3. 写入中断标志文件并发送SIGINT
4. 通知用户中断结果

示例：

```javascript
async function handleStopCommand(event) {
  const sessionId = getActiveSessionId();
  const reason = 'User requested stop';

  // 写入标志文件
  await exec(`./skills/task-interrupt/scripts/create-stop-flag.sh ${sessionId} "${reason}"`);

  // 发送信号
  if (activeSession.processId) {
    process.kill(activeSession.processId, 'SIGINT');
  }

  return '任务已中断';
}
```

## 注意事项

- 务必在长任务中定期保存检查点
- 确保资源清理代码在 `finally` 块中执行
- 不要阻止中断检测轮询的运行
- 检查点数据应轻量，避免阻塞

## 进一步阅读

详见 `SKILL.md` 获取完整技术文档和API参考。
