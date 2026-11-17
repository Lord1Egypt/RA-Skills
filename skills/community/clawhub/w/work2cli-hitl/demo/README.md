# demo/ — 参考形态骨架

> 这个目录展示 work2cli-hitl 的**目标形态**：cli 按系统组织 + 全局守卫单例 + 守卫客户端共享 + 注册表自进化。代码是**参考骨架**（Python 示意，外部 API 用 stub 标注了替换点），照着组织结构抄，不是拿来直接跑的成品。

## 目录结构

```
demo/
├── README.md                          # 本文件
├── guard/
│   └── feishu_guard_daemon.py         # 全局守卫单例守护进程（参考实现骨架）
├── cli/
│   └── order-system/                  # 示例系统目录（真实部署时在 <工作区>/cli/<system>/）
│       ├── order_cli.py               # 示例 CLI：读命令 + 写命令（dry-run + 守卫接入）
│       └── _guard_client.py           # 守卫客户端（真实部署时放 <工作区>/cli/_guard/ 共享）
└── registry/
    └── order-system.md                # 注册表条目示例（做完 CLI 回写的使用说明长这样）
```

## 数据流（写命令从发起到结果上卡片）

```
order_cli apply 27127
  → _guard_client.request_approval("order-system", "apply", "订单 27127", params)
      → 算 hash8 → 查 inflight 复用/发新卡片 → 确保全局守护进程在跑
      → 轮询 spool/decisions/order-system/<hash8>.json（5s 间隔，倒计时）
  ← approved
  → CLI 执行真实写操作（stub）
  → _guard_client.report_result(...)  # 写 results/<hash8>.json
      → 守护进程读到 → 持 token 原位刷卡片成「执行结果」（预算 1 次）
```

## 部署检查单（把 demo 变成真实部署时）

- [ ] `feishu_guard_daemon.py` 复制到固定位置，配置 lark-cli profile，先手动跑通一次 `event consume`
- [ ] `_guard_client.py` 放到 `<工作区>/cli/_guard/`，所有 CLI 共享这一份
- [ ] 每个新系统：复制 `order-system/` 目录结构 → 替换 stub 为真实 API → 跑守卫离线测试
- [ ] 自检三问：守护进程在跑吗 / 杀掉后能自动拉起吗 / **两个不同 CLI** 连续审批都能收到吗
- [ ] 验收通过后回写 `registry/<system>.md`（对照 `registry/_template.md`）
