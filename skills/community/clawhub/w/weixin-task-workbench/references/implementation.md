# 微信任务工作台实现说明

## 与飞书版本的差异

本微信版本沿用飞书版命令语义，但运行策略有三点差异：

- 会话工具缺失时强制阻断（不降级到 registry-only）
- registry 按 `account + peer` 隔离
- 所有任务路由回复都必须带任务头

## 目录结构

```text
skills/public/weixin-task-workbench/
  SKILL.md
  scripts/task_registry.py
  references/protocol.md
  references/implementation.md

tasks/weixin/<account>/<peer>.json
```

## 启动检查

在会话内第一次任务命令时执行：

1. 检查 `sessions_spawn`、`sessions_send`、`sessions_history`
2. 如缺任一能力，返回阻断提示并停止
3. 能力齐全后才进入正常任务流程

## Registry 路径构造

- `account` = 当前微信账号 id
- `peer` = 当前微信用户 id（`xxx@im.wechat`），做文件名安全化
- 最终路径 = `tasks/weixin/<account>/<peer>.json`

## 标准命令流程

## 异常与幂等处理

实现时不要把 `task_registry.py` 的原始错误直接转发给用户。对常见异常统一转成任务工作台话术：

- 空标题创建任务 → 返回补全提示
- 不存在的任务 id → 返回“任务 #<id> 不存在，请先发送任务列表查看可用任务”
- 无当前任务时继续 → 返回“当前没有可继续的任务”
- 已完成任务重复关闭 / 已归档任务重复归档 → 返回幂等提示，不重复写状态
- 当前任务为 `completed` / `archived` 时收到 `继续` → 先提示切换或恢复，不直接路由

优先使用 `references/protocol.md` 中的固定响应模板。除任务总结、任务头内正文等确需生成内容的场景外，不要自由改写这些控制面回复。

### 新建任务

1. `sessions_spawn` 创建任务会话
2. `task_registry.py add ... --session-key <sessionKey> --make-current`
3. 回执任务创建成功与当前任务

### 继续任务

1. `task_registry.py show`
2. 通过 `sessions_send` 将用户消息发送到任务 `sessionKey`
3. 需要时更新任务状态

### 总结任务

1. `task_registry.py summarize <id>`
2. 需要更多上下文时调用 `sessions_history`
3. 输出简明阶段总结
4. 可选写回 `update --summary`

### 任务状态

1. `task_registry.py show` 获取当前任务
2. `task_registry.py list` 获取任务列表
3. 返回任务态摘要（当前任务、状态、sessionKey、registry 路径）
4. 用于排障时优先使用 `任务状态`，不要用 `/status` 判断任务是否隔离

## 验收标准

满足以下条件才可认为运行有效：

1. `新建任务` 能写入 registry 并获得真实 `sessionKey`
2. 后续消息能通过 `sessions_send` 持续进入同一任务会话
3. `总结 #id` 可通过 `sessions_history` 获取近期上下文
4. 切换任务后默认路由目标同步变化
5. 非全局任务回复均包含 `[任务:#id 标题]` 任务头
