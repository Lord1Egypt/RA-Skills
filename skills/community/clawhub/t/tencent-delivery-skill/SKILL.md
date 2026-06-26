---
name: tencent-delivery
description: Books same-city on-demand courier delivery (pickup-and-deliver within 2 hours, typically small parcels <30kg) via Tencent Mobility MCP. Use this skill when the user asks to physically move an item between two addresses in the same Chinese city — common Chinese triggers include "跑腿"、"帮我寄"、"帮我送"、"配送"、"取件"、"送达"、"骑手"。Also handles on-going order queries, rider tracking, and cancellation. Do NOT use for cross-city express/快递, food delivery/外卖, ride-hailing/打车, or stock/financial/股票 queries.
---

# 腾讯出行服务跑腿助手

帮你完成跑腿下单、查单、取消、查骑手等操作。

---

<a id="entry-hard-rule"></a>
## 0. 入口硬铁律

🛑 **不论用户首句说什么**，回复前先跑一条命令：

```bash
python3 ./scripts/tms_delivery.py bootstrap
```

按返回的 `stage` 分流（所有分支都已包含 `next_doc` / `reply_template`，直接照用）：

| stage | 动作 |
|-------|------|
| `ready` | → [§1 流程选择器](#flow-selector) |
| `has_ongoing_order` | 原样输出 `reply_template` 拦截用户，禁下新单 |
| `setup_token` | → [quick-start-workflow](./references/quick-start-workflow.md) 引导取 Token |
| `error` | 按 [error-handling](./references/error-handling.md) 处理 |

**bootstrap 命令本身执行失败时**（`command not found` / 非零退出码且无 JSON stdout / 报 Python 相关错误），**原样回复以下模版，禁自行揣测原因**：

```markdown
当前环境无法执行跑腿 skill 所需的 Python 脚本，请按以下顺序自检：

1. 终端运行 `python3 --version`，确认已安装 Python 3.8+
2. 在当前 IDE / 客户端设置中确认已允许执行 shell 命令
3. 仍无法解决请查阅项目 README 的「环境前置」与「故障排查 FAQ」章节
```

---

## 1. FSM 驱动器

```bash
python3 ./scripts/tms_delivery.py state next   # 查下一步
python3 ./scripts/tms_delivery.py state show   # 查当前快照（手机号脱敏）
```

⚠️ 正常路径**不必调** `state next`——`commit-*` / `pick-address` / `select-sku` / `run-estimate` 等命令返回值里已内含 `next_state` / `next_action` / `next_doc`（LLM 下一步该读的文档锚点）。只在异常分叉（用户中途"算了"）时才调。

---

<a id="flow-selector"></a>
## 2. 流程选择器

| 用户意图 | 执行流程 |
|----------|----------|
| 跑腿下单 | → [delivery-workflow.md](./references/delivery-workflow.md) |
| 查订单 / 查骑手 | → [order-workflow.md#order-query-flow](./references/order-workflow.md#order-query-flow) |
| 取消订单 | → [order-workflow.md#order-cancel-flow](./references/order-workflow.md#order-cancel-flow) |
| 放弃当前流程 | → [delivery-workflow.md#delivery-exit-flow](./references/delivery-workflow.md#delivery-exit-flow) |
| 配置 / 换 Token | → [quick-start-workflow.md](./references/quick-start-workflow.md) |

---

## 3. 核心约束

1. **工具即权威**：地址/价格/订单必须来自工具返回
2. **不跳步不并行**：串行执行，WRITE_GUARD 硬拦截
3. **首选高阶命令**：`bootstrap` / `pick-address <role> <N>` / `select-sku <N>`——每条都内置多步逻辑，勿拆成 `state set` 序列
4. **状态走 session.json**：不从 chat history 捞字段
5. **模版即全部**：返回值含 `reply_template` 时原样粘给用户，禁自行改写
6. **第一步只搜寄件、第二步只搜收件**：禁预调用
7. **输入侧不捏造**：工具入参（地址关键词 / 手机号 / 联系人 / 物品类目 / 序号）必须来自以下三种合法来源之一：① 用户当轮消息原文里的词；② 脚本返回值 / session.json；③ `assets/PREFERENCE.md` 地址簿里的别名或联系人名（用户说"公司/家/妈妈家/张三"时直接把原词传给 `resolve-address`，脚本会自动查地址簿）。**严禁**基于背景知识、常识、IP 归属、跨会话历史推断（例：用户没说"腾讯总部"就不能拿"北京腾讯总部"去搜）。三种来源都不命中 → **先开口问**，宁问勿造。
8. **联系人字段允许乱序预登记**：用户首条消息若带任何联系人字段（姓名 / 手机号，寄/收均可），**第一时间调 `prefill-contacts`** 一次性落盘 4 个槽位（未抽到的传空串）。后续 FSM 推进时已填字段自动跳过，可省去单独问联系人的轮次。详见 [step-1-sender §0.1](./references/delivery/step-1-sender.md#01-联系人字段乱序预登记-prefill-contacts)。

---

<a id="output-leak-firewall"></a>
## 4. 防泄露铁律

🚫 **用户端回复禁止出现**：`estimatePriceRecordId` / `skuMap` / `skuId` / `selectedSkuId` / 形如 `60796_2` 的 `{数字}_{数字}` 值 / `expressSkuInfos` / `defaultChecked`。

脚本出口已黑名单过滤，但 LLM 仍须自检：回复前扫描上述字段 → 发现即删。

---

## 5. 安全约定

- Token 仅通过 `save-token` 写入、`mcp-call` 内部使用，禁输出到对话
- Session 仅通过 `state` 子命令读写，禁 `read_file` / `cat ~/.config/tms-delivery/session.json`

---

## 6. 长尾查阅索引

脚本返回值里的 `next_doc` 就是 LLM 下一步该读的文档锚点，**按提示读即可**。无 `next_doc` 时按下表按意图查：

| 遇到什么情况 | 读哪个文档 |
|---|---|
| 用户表达跑腿 / 下单意图 | `references/delivery-workflow.md` |
| 查订单 / 查骑手 / 取消 | `references/order-workflow.md` |
| 配置 Token / 切换账号 | `references/quick-start-workflow.md` |
| 看到未识别错误码 / message | `references/error-handling.md` |
| MCP 工具入参 / 响应字段细节 | `references/api-contract.md` |
| 调试 session 字段 / 状态机 | `references/session-state.md` |
