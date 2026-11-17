# order-system CLI 使用说明（注册表条目示例）

> 沉淀日期：2026-09-20 ｜ 最近更新：2026-09-20 ｜ 状态：活跃（demo 示例）
> 代码位置：`demo/cli/order-system/` ｜ 守卫客户端：`<工作区>/cli/_guard/`（共享）

> ⚠️ 本条目是**示例**：展示「一个系统的 CLI 做完后，注册表条目应该长什么样」。真实系统的条目按 `registry/_template.md` 写。

## 1. 系统档案

| 项 | 值 |
|----|----|
| 系统名 | 订单管理系统（示例） |
| 入口 URL | https://order.example.com |
| 认证方式 | 环境变量 ORDER_TOKEN > 缓存 ~/.config/order-cli/token.json > 浏览器登录态 |
| token 有效期/刷新 | 以服务端 401 为准自动重取 |
| 是否内网 | 否 |

## 2. 命令索引

```bash
python3 order_cli.py list --status open        # 查开放订单（agent 接「看看有哪些待处理订单」）
python3 order_cli.py detail 27127              # 查单笔订单详情含流程日志（接「看看这笔订单怎么回事」）
python3 order_cli.py apply 27127 --status done --note 复核通过 --dry-run   # 写操作预演（不审批不执行）
python3 order_cli.py apply 27127 --status done --note 复核通过             # 正式变更（飞书审批后执行）
```

## 3. 状态机/枚举表

| 状态码 | 英文 | 中文 | 说明 |
|--------|------|------|------|
| 1 | open | 进行中 | 中间态，可变更 |
| 2 | done | 已完成 | 终态，变更需审批并写明复核依据 |
| 3 | cancelled | 已取消 | 终态，不可逆（守卫文案需标明） |

## 4. 写操作清单（守卫拦截范围）

| 命令 | 副作用 | 不可逆 | 审批文案要点 |
|------|--------|--------|--------------|
| apply | 修改订单状态 | 置为终态时是 | 目标订单 + 变更后状态 + note |

## 5. 已知坑

- 2026-09-20：卡片刷新 token 只能成功用一次（第二次报 300040）——刷新已统一归守护进程，CLI 不要自己碰 card-update。（若未来平台放开频控，先看 write-guard-hitl.md §3 再动）

## 6. 实战记录

- 2026-09-20：demo 演示批次：list 2 条 → detail 1 条 → apply dry-run → 审批执行 → 结果上卡片，全链路通过。

## 7. 关联文件

- CLI：`demo/cli/order-system/order_cli.py`（stub，真实部署替换 api() 函数）
- 守卫客户端：`demo/cli/order-system/_guard_client.py`（部署时移至 `cli/_guard/` 全局共享）
- 守护进程：`demo/guard/feishu_guard_daemon.py`（全局单例）
