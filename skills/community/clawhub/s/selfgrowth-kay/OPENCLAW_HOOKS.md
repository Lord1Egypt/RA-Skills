# Self-Improving Agent Hooks 配置说明

## 安装状态

✅ **技能已安装**: `/root/.openclaw/workspace/skills/self-improving-agent/`

✅ **内存目录已创建**:
- `memory/semantic/` - 存储模式和规则
- `memory/episodic/` - 存储具体经验
- `memory/working/` - 存储当前会话上下文

✅ **Hooks 脚本已就绪**:
- `hooks/pre-tool.sh` - 工具使用前触发
- `hooks/post-bash.sh` - Bash 命令执行后触发
- `hooks/session-end.sh` - 会话结束时触发

## Hooks 配置

### Claude Code (原始设计)

此技能最初是为 Claude Code 设计的，hooks 配置如下：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${SKILLS_DIR}/self-improving-agent/hooks/pre-tool.sh \"$TOOL_NAME\" \"$TOOL_INPUT\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${SKILLS_DIR}/self-improving-agent/hooks/post-bash.sh \"$TOOL_OUTPUT\" \"$EXIT_CODE\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${SKILLS_DIR}/self-improving-agent/hooks/session-end.sh"
          }
        ]
      }
    ]
  }
}
```

### OpenClaw

OpenClaw 的 hooks 系统目前仅支持内部钩子（internal hooks）。self-improving-agent 的 hooks 集成需要 OpenClaw 支持自定义事件钩子。

**当前状态**: OpenClaw 不直接支持 Claude Code 风格的 hooks。

**替代方案**: 技能可以通过手动触发工作：

## 手动触发

无需 hooks，技能可以通过以下命令手动触发：

- "自我进化"
- "self-improve"
- "从经验中学习"
- "分析今天的经验"
- "总结教训"
- "改进 [技能名称]"

## 下一步

如果需要在 OpenClaw 中实现自动 hooks 触发，可能需要：

1. 扩展 OpenClaw 的 hooks 系统以支持自定义钩子
2. 或在 OpenClaw 的会话管理中添加技能事件监听器
3. 或创建一个 OpenClaw 扩展来桥接技能事件

## 参考

- 技能文档：`/root/.openclaw/workspace/skills/self-improving-agent/SKILL.md`
- 安装说明：`/root/.openclaw/workspace/skills/self-improving-agent/README.md`
