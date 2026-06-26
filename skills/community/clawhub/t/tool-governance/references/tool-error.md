# Pattern 2.1: 工具错误重试升级

## 问题

Agent 调用工具失败后会重试，但经常用完全相同的参数重试同一个失败的工具。5 次 `cargo build` 失败（因为容器里没装 cargo）后还在 `cargo build`。

## 原理

通过 PostToolUseFailure hook 追踪连续失败次数，在 PreToolUse hook 中注入逐级升级的干预消息。来自 OMC 的 `post-tool-use-failure.mjs`——OMC 在 5 次失败后注入"ALTERNATIVE APPROACH NEEDED"。

## 三级升级策略

| 连续失败次数 | Hook 行为 | 注入消息 |
|-------------|----------|---------| 
| 1-2 | 记录但不干预 | （无） |
| 3-4 | PreToolUse 注入软提示 | "该工具已失败 3 次。考虑：换一个参数？换一个路径？是否缺少依赖？" |
| 5+ | PreToolUse 注入强制切换 | "MUST use an alternative approach. This tool+args combination has failed 5 times. Previous errors: [error summary]. Do NOT retry the same command." |

## 状态文件

```json
{
  "tool_name": "Bash",
  "input_hash": "a3f2c1...",
  "error": "command not found: cargo",
  "count": 5,
  "first_at": "2026-04-05T10:00:00Z",
  "last_at": "2026-04-05T10:02:30Z"
}
```

`input_hash` 是工具输入的哈希（取前 200 字符），区分"同一个命令反复失败"和"不同命令分别失败"。只有相同 tool_name + input_hash 的连续失败才计数升级。

存储在 `sessions/<session-id>/tool-errors.json`。

## 与 `updatedInput` 的组合

Claude Code 的 PreToolUse hook 支持返回 `updatedInput` 字段，可以在执行前直接修改工具输入。这比在 additionalContext 中"建议"换方案更确定——直接改写命令：

```json
{
  "updatedInput": {
    "command": "pip install cargo-alternative && cargo-alternative build"
  }
}
```

`additionalContext` 是概率性的（LLM 可能忽略建议），`updatedInput` 是确定性的（直接改写输入）。

## 强化：3-Strike Approach Mutation

来源：`OthmanAdi/planning-with-files`

升级版策略——每次重试 MUST 使用不同的方案：
- Attempt 1：诊断并修复
- Attempt 2：换方法/工具/库（NEVER 重复完全相同的失败动作）
- Attempt 3：质疑假设，搜索方案，考虑更新计划
- 3 次后：升级到用户，附带尝试过的方案表

规则：`if action_failed: next_action != same_action`。用结构化表格记录（Error | Attempt | Resolution）。

## 延伸：Error Capture to Auto-Memory

来源：`alirezarezvani/claude-skills` — `self-improving-agent/hooks/error-capture.sh`

Pattern 2.1 处理重试，但不记录解决方案。Error Capture 在 PostToolUse hook 中监控 30+ 错误 pattern（从 `"error:"` 到 `"Traceback"` 到 `"ECONNREFUSED"`），用排除 pattern 过滤误报（`"console.error"`, `"catch (error"`, `"error.log"`）。检测到错误并最终解决后，自动保存解决方案到 auto-memory，供未来 session 复用。

## 实现要点

**PostToolUseFailure hook**：
```bash
# 读取 stdin 获取失败信息
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
ERROR=$(echo "$INPUT" | jq -r '.error // ""')
INPUT_HASH=$(echo "$INPUT" | jq -r '.tool_input' | head -c 200 | md5sum | cut -d' ' -f1)

# 读取或创建错误追踪文件
STATE_FILE="sessions/${SESSION_ID}/tool-errors.json"
# 如果同一 tool+hash，increment count；否则 reset
```

**PreToolUse hook**：
```bash
# 读取错误追踪文件
STATE_FILE="sessions/${SESSION_ID}/tool-errors.json"
COUNT=$(jq -r '.count // 0' "$STATE_FILE")
if [ "$COUNT" -ge 5 ]; then
  echo '{"hookSpecificOutput":{"additionalContext":"MUST use an alternative approach..."}}'
fi
```
