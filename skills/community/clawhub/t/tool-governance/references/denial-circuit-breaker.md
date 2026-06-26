# Pattern 2.2: 权限否决追踪（Denial Circuit Breaker）

## 问题

Agent 尝试执行被用户/策略拒绝的操作后，可能换一种表述再试——"我用 `rm` 删不了，试试 `unlink`"。

## 原理

追踪被拒绝的工具调用模式。连续多次否决后，从"允许但提醒"降级到"会话级禁止"。来自 Claude Code 内部的 `DenialTrackingState`——3 次连续否决或 20 次总否决后，系统从 auto 模式退回 default 模式（`shouldFallbackToPrompting`）。

## 三级降级

| 连续否决次数 | 行为 |
|-------------|------|
| 1-2 | 记录，不干预 |
| 3+ | 注入 additionalContext："该操作已被拒绝 3 次。MUST 使用完全不同的方案，不要变换表述重试相同操作。" |
| 5+ | 标记 tool_name + input_pattern 为 session 级禁止。PreToolUse hook 直接 `{"decision":"block"}` |

## 与工具错误升级 (Pattern 2.1) 的区别

| | 工具错误升级 | 权限否决追踪 |
|---|---|---|
| 触发 | 工具执行失败（exit code != 0） | 用户/策略拒绝（permission denied） |
| 原因 | 技术问题（依赖缺失、路径错误） | 策略问题（不允许该操作） |
| 解决方向 | 换参数/换工具 | 换完全不同的方案 |

## 状态文件

存储在 `sessions/<session-id>/denials.json`：

```json
{
  "denials": [
    {
      "tool_name": "Bash",
      "input_pattern": "rm -rf",
      "count": 3,
      "last_at": "2026-04-05T10:05:00Z"
    }
  ],
  "total_denials": 5,
  "session_banned": ["Bash:rm -rf", "Bash:unlink"]
}
```

## Claude Code 内部的实现参考

Claude Code 的 `DenialTrackingState` 使用两个阈值：
- 3 次连续否决同一操作 → `shouldFallbackToPrompting` 返回 true
- 20 次总否决（不限操作类型）→ 从 auto 模式退回 default 模式

这是一个 circuit breaker 模式——防止 agent 在被拒绝的操作上无限消耗 token。
