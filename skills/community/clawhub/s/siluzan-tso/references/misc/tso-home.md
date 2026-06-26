# TSO 首页看板

## 引导用户打开首页

```bash
siluzan-tso config show   # 取 webUrl
```

首页地址：`https://www.siluzan.com/v3/foreign_trade/tso/home`

---

## CLI 能做什么 / 不能做什么

| 用户需求                                                       | Agent 做法                                                              |
| -------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 与首页**完全一致**的昨日汇总、全账户余额一览、图表级多账户联动 | **无对应 CLI**；引导打开首页（上表 URL）                                |
| 单账户余额                                                     | `balance -m <媒体> -a <mediaCustomerId>`                                |
| 单账户消耗/点击/转化                                           | `stats -m <媒体> -a <mediaCustomerId>`                                  |
| 开户进度                                                       | `account-history`、`open-account`                                       |
| 充值                                                           | **无 CLI**；见 `references/accounts/finance.md`，用 `webUrl` 引导充值页 |
| AI / 建站 / 内容等非 TSO 模块                                  | 说明超出本 Skill；用 `webUrl` 拼接路径，**勿**用 siluzan-tso 冒充       |

---

## 推荐话术

1. **「和首页一样的总览」** → 打开 `https://www.siluzan.com/v3/foreign_trade/tso/home`。
2. **「某个 Google 账户昨天花了多少」** → `list-accounts -m Google` + `stats -m Google -a <id>`。
3. **「有待充值账户」** → 说明聚合数据在首页；CLI 可 `list-accounts` + `balance` 逐户排查，或引导充值页。

多账户巡检见 **`references/core/workflows.md`** 流程十。
