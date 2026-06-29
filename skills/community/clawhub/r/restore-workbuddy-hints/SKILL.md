---
name: restore-workbuddy-hints
description: "Restore WorkBuddy UI hints and tips that were dismissed via the '不再显示' button. Use when the user reports that an in-app tip or prompt bar has disappeared after clicking '不再显示', or when the user wants to bring back hidden WorkBuddy prompts. Triggers: 提示条不见了, 不再显示后怎么恢复, 关闭的提示怎么重新显示, restore dismissed hints."
agent_created: true
---

# Restore WorkBuddy Hints

恢复 WorkBuddy 界面中被「不再显示」关闭的提示条 / 功能引导。

## Overview

WorkBuddy 的提示条（如"批量创建自动化任务太麻烦？"）右上角提供「不再显示」按钮。
点击后，该提示条被记录到 `~/.workbuddy/user-state.json` 的 `tipShowHistory` 字段中，
之后该提示条永久隐藏。此技能通过清除该记录来恢复被关闭的提示条。

## When to Use

- 用户说某个 WorkBuddy 提示条/引导「不见了」「消失了」「点了不再显示之后再也出不来」
- 用户想恢复被关闭的某个特定提示条
- 用户想一次性恢复所有被关闭的提示条
- 用户想查看当前有哪些提示条被关闭了

## Workflow

### Step 1: Confirm User Intent

Ask the user which approach they prefer:

- **全部恢复** — 恢复所有被「不再显示」关闭的提示条
- **指定恢复** — 只恢复某一个提示条（需要先查看列表）
- **仅查看** — 只看当前有哪些提示条被关闭

### Step 2: Run the Restore Script

Run the bundled script from the skill directory. The script path is located under
`~/.workbuddy/skills/restore-workbuddy-hints/scripts/restore_hints.py`.

Use the managed Python runtime:

```
C:/Users/USERNAME/.workbuddy/binaries/python/envs/default/Scripts/python.exe \
  ~/.workbuddy/skills/restore-workbuddy-hints/scripts/restore_hints.py \
  --list | --all | --key HINT_KEY
```

**Options:**

| Flag | 说明 |
|------|------|
| `--list` | 列出所有已被关闭的提示条（查看 key 名称） |
| `--all` | 恢复所有已被关闭的提示条 |
| `--key NAME` | 恢复指定 key 的提示条 |

### Step 3: Restart WorkBuddy

After the script runs successfully, instruct the user:

1. **完全退出 WorkBuddy**（右键系统托盘图标 → 退出）
2. **重新启动 WorkBuddy**
3. 被恢复的提示条将重新出现在界面上

### Important Notes

- 配置文件 `~/.workbuddy/user-state.json` 是本地存储的，不同账号、不同电脑的配置各自独立
- 脚本仅修改 `tipShowHistory` 字段，不会影响其他设置
- **操作前建议先退出 WorkBuddy**，避免客户端运行时覆盖修改

## Manual Recovery (Fallback)

如果 Python 脚本无法运行，也可以手动恢复：

1. 打开文件管理器，地址栏输入 `%USERPROFILE%\.workbuddy` 回车
2. 用记事本打开 `user-state.json`
3. 将 `"tipShowHistory"` 的值改为空对象 `{}`：
   ```json
   "tipShowHistory": {}
   ```
4. 保存文件，重新启动 WorkBuddy

## Resources

### scripts/restore_hints.py

Executable Python script for listing and restoring dismissed hints.
No external dependencies required — uses only Python standard library.

Supports three modes:
- `--list` — List all dismissed hints
- `--all` — Clear entire tipShowHistory
- `--key NAME` — Restore a specific hint by its key name
