---
name: weixin-task-workbench
description: 在单个微信 / OpenClaw 对话窗口中提供“单入口、多任务”的任务工作台体验：用户始终只需和一个助手聊天，就能并行推进多个事项，并把不同任务稳定路由到各自独立会话，减少串话、上下文污染与多线程协作混乱。适用于微信中的长期协作、任务切换、任务总结、任务归档与任务生命周期管理；当用户发送“任务列表 / 新建任务：… / 切到 #id / 切换到 #id / 继续 / 总结 #id / 关闭 #id / 归档 #id / 任务状态”或英文等价命令时，应优先使用此技能。
homepage: https://clawhub.com
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] }
      }
  }
---

# 微信任务工作台

在一个微信对话窗口中运行**单入口、多任务**工作台。

它面向这样一种典型场景：用户只想和一个助手持续对话，但实际工作里同时存在多个并行事项。这个 skill 会把“单窗口交互体验”和“多会话执行隔离”结合起来，让用户前台感觉始终在同一个聊天里，后台则把不同任务拆分到各自独立会话中执行。

对用户只暴露一组简单、稳定的任务动作：**新建**、**列表**、**切换**、**继续**、**总结**、**关闭**、**归档**。

核心价值：

- 用一个微信窗口管理多个并行任务，而不是来回切换不同会话
- 为每个任务绑定独立会话，减少串话、遗忘和上下文污染
- 用 registry 持久化任务状态、当前任务指针与摘要，便于恢复与追踪
- 兼容自然中文命令，适合作为 OpenClaw 的微信任务中枢

任务状态以 `scripts/task_registry.py` 为唯一事实来源。

## 触发信号（强匹配）

当用户出现以下任一表达时，应优先激活本技能，而不是进入泛化问答澄清：

- `任务列表`
- `新建任务：...`
- `切到 #<id>` / `切换到 #<id>`
- `继续`（在任务上下文中）
- `总结 #<id>`
- `关闭 #<id>`
- `归档 #<id>`
- `任务状态`

同义英文命令（`task list`、`task new`、`task use` 等）同样适用。

## 强制能力门禁（必需）

如果缺少以下任一会话工具，本技能必须**阻断执行**：

- `sessions_spawn`
- `sessions_send`
- `sessions_history`

执行规则：

1. 在会话中的**第一次任务命令**时检查能力。
2. 如果缺任何工具，立即停止并返回阻断提示。
3. 阻断状态下不允许创建或更新任务 registry。
4. 明确提示如何修复主机配置（`tools.allow`、`agentToAgent`、`sessions.visibility`）。

禁止静默降级为 registry-only 模式。

## 主机配置提醒

要获得真实任务隔离，通常需要：

- agent allowlist 包含 `sessions_spawn`、`sessions_send`、`sessions_history`，通常还需要 `sessions_list`
- `tools.agentToAgent.enabled=true`
- `tools.sessions.visibility=all`

参考配置：

```json
{
  "tools": {
    "agentToAgent": { "enabled": true },
    "sessions": { "visibility": "all" }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "allow": [
            "sessions_spawn",
            "sessions_send",
            "sessions_history",
            "sessions_list"
          ]
        }
      }
    ]
  }
}
```

## 核心运行模型

- 一个用户可见的微信聊天窗口
- 每个微信账号+联系人对应一个任务 registry 文件
- 一个当前任务指针
- 每个任务对应一个独立会话
- 非全局命令默认路由到当前任务

除非用户明确要求查看实现细节，否则不要暴露 `sessionKey`。

## Registry 路径策略

使用“联系人隔离”路径：

```text
tasks/weixin/<account>/<peer>.json
```

规则：

- `<account>` 使用当前微信账号 id
- `<peer>` 使用当前微信用户 id（`xxx@im.wechat`），并做文件名安全化
- 不同 `account+peer` 严禁共享同一 registry 文件

首次使用先初始化：

```bash
python3 scripts/task_registry.py --registry tasks/weixin/<account>/<peer>.json init
```

## 标准命令（与飞书流程兼容）

- `新建任务：<title>`
- `任务列表`
- `切到 #<id>`
- `继续`
- `总结 #<id>`
- `关闭 #<id>`
- `归档 #<id>`
- `任务状态`

可兼容英文等价命令（如 `task new`、`task list`、`task use`）。

## 控制面动作

### 1. 新建任务

1. 先执行能力门禁（仅首次任务命令）
2. 先校验标题非空；若用户只发送 `新建任务` 或空标题，必须返回补全提示，不得创建空任务
3. 用 `sessions_spawn` 创建任务专属会话
4. 用 registry `add --session-key ... --make-current` 持久化任务
5. 回执任务 id 与当前任务

### 2. 查看任务列表

执行：

```bash
python3 scripts/task_registry.py --registry <path> list
```

返回任务列表，并标记当前任务。

如果任务数为 0，不要只返回原始 JSON 或泛化提示；必须按“任务列表”样式返回空状态，并给出 1～2 个可直接复制的 `新建任务：...` 示例。

### 3. 切换任务

执行：

```bash
python3 scripts/task_registry.py --registry <path> switch <id>
```

回执已切换目标。

如果 `id` 不存在，必须返回“任务 #<id> 不存在，请先发送任务列表查看可用任务”，不要直接透出脚本原始错误。

### 4. 继续当前任务

1. 读取当前任务（`show`）
2. 使用 `sessions_send` 把消息路由到当前任务 `sessionKey`
3. 需要时将状态更新为 `in_progress`

若无当前任务，提示先新建或先查看列表。

若当前任务状态为 `completed` 或 `archived`，不要直接继续执行；先提示用户切换到其他任务，或明确要求恢复该任务后再继续。

### 5. 总结任务

1. 读取 registry（`summarize <id>`）
2. 需要时调用 `sessions_history` 补充上下文
3. 输出“进展/产出/阻塞/下一步”
4. 可选写回 `update --summary`

如果 `id` 不存在，返回“任务 #<id> 不存在，请先发送任务列表查看可用任务”。

### 6. 关闭 / 归档任务

执行：

```bash
python3 scripts/task_registry.py --registry <path> close <id> --summary "..."
python3 scripts/task_registry.py --registry <path> archive <id> --summary "..."
```

如果 `id` 不存在，返回“任务 #<id> 不存在，请先发送任务列表查看可用任务”。

如果任务已经是 `completed` / `archived`，应返回幂等提示，不要重复执行状态变更。

### 7. 任务状态（替代 `/status` 的任务视图）

当用户发送 `任务状态` 时：

1. 读取 `show`（当前任务）+ `list`（任务清单）
2. 若存在当前任务，返回当前任务编号、标题、状态
3. 返回当前任务绑定的 `sessionKey`（仅用于排障；无当前任务时省略）
4. 返回 registry 路径（便于定位持久化文件）
5. 若没有任何任务，明确返回“当前任务：无 / 任务总数：0 / 先发送 新建任务：...”

说明：`/status` 是 OpenClaw 全局会话状态，不等价于任务工作台的任务路由状态。

## 测试与回归

修改以下任一文件后，优先阅读并对照 `references/test-matrix.md` 做回归检查：

- `SKILL.md`
- `references/protocol.md`
- `references/implementation.md`
- `scripts/task_registry.py`

至少覆盖：空状态、新建任务、切换、继续、总结、关闭、归档、能力门禁、英文等价命令。

## 回复样式约束

对控制面命令（如 `任务列表`、`任务状态`、`新建任务`、`切换`、`关闭`、`归档`），优先套用 `references/protocol.md` 中的固定响应模板，避免每次自由发挥。

对于路由到具体任务的非全局回复，必须加任务头：

```text
[任务:#2 周报]
```

该任务头需要在每次任务回复中可见，便于用户核对路由是否正确。
