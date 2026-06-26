# SuperpowersOpen

Superpowers 方法论在 OpenClaw 平台上的完整移植。为 OpenClaw 用户提供经过验证的 AI 辅助开发工作流。

## 安装

### 方式一：ClawHub 安装
```bash
clawhub install superpowers-open
```

### 方式二：手动安装
将整个 `superpowers-open/` 目录复制到 `~/.openclaw/skills/`：

```bash
cp -r superpowers-open ~/.openclaw/skills/
```

重启 OpenClaw Gateway 后生效。

## 技能列表

### 入口层
| 技能 | 说明 |
|------|------|
| `using-superpowers-open` | 工具映射表、触发协调、指令优先级（始终激活） |

### 流程层
| 技能 | 说明 |
|------|------|
| `brainstorming` | 设计先行——编码前必须完成设计并获批准 |
| `writing-plans` | 将设计拆解为可执行的分步实现计划 |
| `executing-plans` | 加载计划、逐任务执行、验证完成 |
| `finishing-a-development-branch` | 完成后提供 merge/PR/保留/丢弃 4 选项 |

### 实践层
| 技能 | 说明 |
|------|------|
| `test-driven-development` | RED-GREEN-REFACTOR：先写测试，看它失败，写最小代码 |
| `systematic-debugging` | 4 阶段系统化调试：根因→模式→假设→修复 |
| `verification-before-completion` | 声称完成前必须运行验证命令并出示证据 |
| `receiving-code-review` | 收到审查反馈时：验证后实现，禁止表演性同意 |
| `requesting-code-review` | 5 维度自检清单替代 subagent 审查 |
| `writing-skills` | TDD 方法论应用于技能文档编写 |
| `using-git-worktrees` | 创建隔离的 git worktree 工作空间 |

## 工作流

```
using-superpowers-open（始终激活）
         ↓
   brainstorming（设计先行）
         ↓
   writing-plans（编写计划）
         ↓
   executing-plans（执行计划）
         ↓
   finishing-a-development-branch（完成集成）
```

辅助技能（按需触发）：TDD、调试、验证、审查、worktree 隔离

## 兼容性

- 平台：OpenClaw
- 格式：SKILL.md（YAML frontmatter + Markdown）
- 无需额外依赖

## 许可

MIT-0

## 致谢

基于 [obra/superpowers](https://github.com/obra/superpowers) 方法论移植适配。
