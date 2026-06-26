# Session Continuity for OpenClaw

跨会话记忆接续器——保存进度，随时从断点继续。

---

## 功能一览

```
/checkpoint save <name>      保存当前任务状态到命名断点
/checkpoint list              列出所有可用断点
/checkpoint resume <name>     从断点恢复会话
/checkpoint delete <name>     删除已完成的断点
```

断点保存在文件中，会话结束后、上下文压缩后、甚至崩溃后都能恢复。可以跨天、跨周继续工作。

---

## 安装方式

**方式一：通过 ClawHub（推荐）**
```bash
openclaw skills install session-continuity
```

**方式二：手动安装**
```bash
# 复制到 OpenClaw 工作空间
cp -r session-continuity ~/.openclaw/workspace/skills/

# 创建断点目录
mkdir -p ~/.openclaw/workspace/memory/checkpoints
```

**验证安装：**
```bash
openclaw skills check
# 确认 session-continuity 出现在列表中
```

---

## 快速上手

### 保存工作进度

会话即将结束但任务还没完成：

```
/checkpoint save my-task
```

技能会写入一个断点文件，包含：
- 任务摘要
- 已完成的内容（文件路径 + 行号）
- 精确的下一步操作（哪个文件、哪个命令）
- 当前阻碍
- 会话中做的关键决策

### 在新会话中恢复

```
/checkpoint list                    # 查看所有断点
/checkpoint resume my-task          # 从断点恢复
```

技能展示结构化简报：
- 任务摘要 + 保存时间
- 已完成内容
- 下一步操作
- 陈旧警告（如文件已不存在）

---

## 工作原理

### 断点文件

```
memory/checkpoints/<name>.md
```

每个断点包含：
- **Task**：一行任务描述
- **Progress**：已完成的具体内容（文件路径、行号）
- **Next Action**：精确的下一步（文件 + 命令）
- **Blockers**：当前阻碍
- **Key Decisions**：推理过程而非仅事实
- **Relevant Context**：偏好设置、文件路径等必要上下文

### 架构

```
~/.openclaw/workspace/
├── SESSION-STATE.md              ← WAL：每条消息的决策记录（proactive-agent）
├── memory/
│   ├── working-buffer.md         ← WAL：危险区交换记录
│   └── checkpoints/
│       ├── <name>.md             ← 命名断点（手动创建）
│       └── autosave.md           ← 自动创建（关闭信号 / 高上下文时）
```

技能基于 [proactive-agent](https://github.com/hal-lobster/proactive-agent) 的 WAL 协议：
- WAL 记录每条消息的决策和修正
- 断点记录任务级别的恢复状态

两者配合使用，不是替代关系。

---

## 自动断点（自动保存）

技能在检测到以下信号时自动保存到 `autosave.md`：

| 信号 | 例子 |
|------|------|
| 上下文 >70% | tokens 快用完了 |
| 关闭信号 | "晚安"、"exit"、"logout" |
| 空闲但有工作 | 10分钟以上未操作且有活跃任务 |
| 长时间操作 | 即将执行 >30 秒的命令 |

自动保存不会覆盖命名断点。命名断点永久保存直到手动删除。

---

## 环境要求

- OpenClaw（任意近期版本）
- Python 3.8+（用于 checkpoint 脚本）
- `OPENCLAW_WORKSPACE` 环境变量（OpenClaw 自动设置）

无需外部 Python 包，纯标准库实现。

---

## 运行测试

```bash
cd session-continuity
python3 tests/test_checkpoint.py
```

预期输出：
```
✅ All tests passed
```

---

## 许可

MIT — 可自由使用、修改、分发。无担保。

---

## 致谢

使用 [MiniMax Skill Factory](https://github.com/MiniMax-AI/skills) 工作流构建。
灵感来自 [proactive-agent](https://github.com/hal-lobster/proactive-agent) 的 WAL 协议。
