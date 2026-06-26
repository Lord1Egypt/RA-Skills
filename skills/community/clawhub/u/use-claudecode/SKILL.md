---
name: claude_cli_skill
description: A universal MCP-compatible tool/skill that empowers ANY AI Agent to natively call the local Anthropic Claude Code CLI. Ideal for code refactoring, large scale code generation, terminal execution, bash shell commands, running tests, local environment modification, and bypassing token limits.
author: BigHit1
version: 1.0.0
---

# Claude CLI Wrapper Skill

## 🎯 技能介绍 (Skill Overview)
让 OpenClaw 能够以“人类程序员”的视角，直接在命令行中调用本地安装的 Anthropic `claude-code` 工具。
通过这项技能，你可以将枯燥的代码编写、大规模重构、Bug修复委托给底层的 Claude CLI，并通过阅读它的终端返回结果（包括变更的文件、编译报错、它的思考过程）来决定下一步操作。

## 🔍 何时使用此技能 (When to Use)
**当你（OpenClaw）收到以下类型的用户请求时，必须触发使用此技能：**
1. **涉及大规模代码生成或重构**：用户要求创建一个完整的应用、模块或进行项目结构级的改动。
2. **需要修改特定工作区中的文件**：用户明确提示在某个 `project_path` 下增删改代码，而你自己没有直接访问该目录写文件的工具权限时，可以将其委派给本技能。
3. **疑难 Bug 排查**：用户发来极其复杂的项目报错，你需要一个“本地开发小助手”去项目里实地跑一遍代码和测试。
*(简而言之：不要自己尝试在对话框里猜代码，只要涉及文件工程，就立刻调用 `talk_to_claude` 让底层小弟去干活。)*

## 💡 核心设计理念: 工具即终端交互
你不应该试图用脚本把 Claude “锁”在一个死循环里。相反，你应该像一个坐在屏幕前的人类：
1. 发送一条指令。
2. 仔细阅读返回的终端输出日志。
3. 若任务完成，则验收关闭。
4. 若任务未完成（由于 Tokens 限制或遭遇阻碍），手动发送继续或排障指令。

---

## 🛠️ 可用工具 (Available Tools)

### `talk_to_claude` 工具
**作用**: 向指定工作目录中的 Claude CLI 发送一条消息，并获取它的原生终端回显。

**参数列表**:
- `message` (string, 必填): 你想要发送给 Claude 的指令。
- `project_path` (string, 必填): 目标项目所在的**绝对路径**。
- `is_new_session` (bool, 选填): 
  - `True`: 清空过去的对话上下文，开启一个全新的独立会话。当你开始在当前目录做一个完全不相干的新任务时使用。
  - `False` (默认): 在当前目录追加 `--continue` 参数，也就是接着上一条命令继续聊。当你需要它修 Bug、继续输出被打断的代码、或者补充说明时，务必保持为 `False`。

---

## 🚀 最佳实践指南 (Best Practices for OpenClaw)

### 场景 1: 分配一个新任务
当需要让 Claude 实现一个全新的需求：
```json
{
  "name": "talk_to_claude",
  "arguments": {
    "message": "请用 Pygame 写一个贪吃蛇游戏的核心逻辑类，并存到 src/snake.py 中。",
    "project_path": "/Users/my_projects/snake_game",
    "is_new_session": true
  }
}
```

### 场景 2: 任务被掐断需要继续
如果观察到刚才的输出代码截断了，或者是 Claude 主动停下来了：
```json
{
  "name": "talk_to_claude",
  "arguments": {
    "message": "代码好像还没写完，请继续完成剩下的部分。",
    "project_path": "/Users/my_projects/snake_game",
    "is_new_session": false
  }
}
```

### 场景 3: 指导排障
如果发现刚才执行后终端报错了：
```json
{
  "name": "talk_to_claude",
  "arguments": {
    "message": "刚刚你写的蛇移动逻辑在边缘碰撞时会抛出 IndexOutOfBound 错误，请检查一下 move 方法的边界判断。",
    "project_path": "/Users/my_projects/snake_game",
    "is_new_session": false
  }
}
```

---

## 🚫 注意事项
- 你必须总是确保 `project_path` 是正确存在的本机绝对路径。
- 该工具封装内部已自动带有 `--permission-mode bypassPermissions`，你无需担心命令行会因为卡在 `(Y/n)` 确认等待处而崩溃。
- 由于是文本传输，工具执行可能有长达数分钟的延时（等待 Claude 输出完毕），请耐心等待工具返回结果。
