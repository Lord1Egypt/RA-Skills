<a id="quick-start-main"></a>
## ⚡ Quick Start

<a id="entry-checklist"></a>
### 1.0 入口自检清单（首轮回复前必过）

> 本节承载了原 SKILL.md §0 的详细自检清单，供 LLM 在不确定时快速核对。核心三动作见 [SKILL.md §0](../SKILL.md#entry-hard-rule)。

#### 首轮回复前逐条默念

- [ ] 执行过 `preflight`？—— 没有就**立刻执行**，不允许先问用户任何问题
- [ ] 执行过 `runerrand_query_going_order`？—— 没有就**立刻执行**（该接口唯一合法调用时机）
- [ ] 执行过 `state reconcile`？—— 没有就**立刻执行**，传入上一步完整 JSON
- [ ] 正打算说"请提供寄件地址""从哪里寄""告诉我所在城市"？—— **停！** 先做上面三动作
- [ ] 用户话里信息看起来很完整（"从 A 寄到 B 给 XX 电话 138..."），想"高效"直接下单？—— **停！** [入口硬铁律](../SKILL.md#entry-hard-rule) 要求先跑 `bootstrap` 查进行中订单，**信息完整度不是豁免条件**

#### 常见误判模式

| 错误思路 | 为什么错 | 正确做法 |
|----------|----------|----------|
| "用户只说'帮我叫个跑腿'，信息不够，先问地址" | 跳过了 preflight + query_going_order | 先执行三动作，再按结果分流 |
| "意图很明确是下单，直接按下单流程第一步" | §1.1 流程选择器是在三动作**通过之后**才用 | 先走 §0，通过后进选择器 |
| "上次 session 已经查过了" | 本轮对话首次进入必查；模型不应假设"上次" | 每轮对话首次进入都必查 |
| "只是闲聊/寒暄，不用查吧" | 用户话里含"跑腿/寄/送"等关键词就已触发 skill | 触发即校验 |

> 💡 这是 skill 最脆弱的入口——模型看到具体需求时有强烈冲动直接响应业务语义，而忘记环境校验。本清单是"先查再做"的最后防线。

---

### 1. 检查环境（每次入口都要执行）

先运行 `python3 ./scripts/tms_delivery.py preflight` 判断 token 是否存在（来源：`~/.config/tms-delivery/env.json` 的 `token`），决定是引导取 token 还是直接继续。

`preflight` 返回码规则：
- `0`：环境已就绪（`next_actions` 仅为 `ready`）
- `1`：环境未就绪（按 `next_actions` 补齐）

<a id="qs-get-token"></a>

#### 1.1 获取 Token

如果 `preflight` 返回 `setup_token`，使用以下模版回复用户：

**回复模版**：

```markdown
请使用微信扫描下方二维码，获取跑腿 TOKEN 后回复我：
![引导图](https://static.img.tai.qq.com/mp/ops/cdnImg/2026/15/mplaunch_skillToken_1775811974.png)

如果图片无法正常展示，请前往：
「微信」-「我」-「服务」-「出行服务」-「我的」-「头像/昵称」-「Token信息」中获取跑腿 token
```

**❌ 禁止回复模版以外的内容**

用户提供 TOKEN 后，执行：

```bash
python3 ./scripts/tms_delivery.py save-token <用户提供的token>
```

#### 1.2 再次确认

执行 `python3 ./scripts/tms_delivery.py preflight`，直到返回码为 `0`。

<a id="qs-check-ongoing"></a>

#### 1.3 Token 有效性 + 进行中订单校验（关键）

> 本步骤一举两得：① 用一次真实 MCP 调用验证 token；② 同时拿到是否有进行中订单。

**🛑 调用时机：仅在进入 skill 时调用一次，全局唯一调用点**（详见 [入口硬铁律](../SKILL.md#entry-hard-rule)）

**以下场景均不调用 `runerrand_query_going_order`**：
- 下新单 / 进入下单流程
- 支付确认（第七步）—— 已有 orderCode，直接查订单详情
- 查订单 / 查骑手 —— 直接走 [订单查询流程](./order-workflow.md#order-query-flow)
- 取消订单 —— 直接走 [取消流程](./order-workflow.md#order-cancel-flow)

执行：

```bash
python3 ./scripts/tms_delivery.py mcp-call runerrand_query_going_order '{}'
```

判断分支：

| 返回情况 | 含义 | 处理 |
|----------|------|------|
| `code == 0` 且 `orderCode` 不为空 | Token 有效，**有**进行中订单 | 进入 [§1.3.1 拦截](#qs-block-on-ongoing) |
| `code == 0` 且 `orderCode` 为空 | Token 有效，无进行中订单 | 通过，进入用户意图对应流程 |
| 鉴权错误（401 / token 无效）| Token 失效 | `delete-token` 后回 [§1.1](#qs-get-token) |
| `code == 10000` 或网络错误 | 服务不可用 | 提示"服务暂时不可用，请稍后重试"，终止 |

<a id="qs-block-on-ongoing"></a>

##### 1.3.1 进行中订单的分流

**分流规则**（v1.0.8+ 放宽：询价不再拦截）：

```
IF runerrand_query_going_order 返回 orderCode 不为空:
    IF 用户意图 == 「下单」:
        → ❌ 严禁 runerrand_book_order
        → ✅ 按下方拦截模版回复
    ELSE IF 用户意图 == 「询价」:
        → ✅ 允许进入询价流程（只读，不产生新订单）
        → 询价结束后若用户说"下单" → 再按拦截模版提示
    ELSE IF 用户意图 == 「查询」/「取消」/「查骑手」:
        → ✅ 不拦截，直接进入对应流程，以此 orderCode 为目标
```

**拦截模版**（用户意图为下单时使用）：

```markdown
🚴 检测到您还有一笔进行中的跑腿订单，无法新建下单：

🧾 订单号：{orderCode}
📋 当前状态：{orderStatusText}

是否查询该订单的详细状态？
- 回复「查跑腿」查看详情
- 回复「骑手到哪了」查看骑手位置
- 回复「取消跑腿」取消该订单
```

**❌ 禁止回复模版以外的内容**

约束：
- 用户回复"查跑腿"等 → 用 `orderCode` 调 `runerrand_query_order_detail`，走 [订单查询](./order-workflow.md#order-query-flow)
- 用户意图为查询/取消/查骑手 → 不拦截
- 用户意图为下单 → 拦截，**不执行 `runerrand_book_order`**
- 用户意图为询价 → 允许询价（只读），但询价后若要下单需走拦截流程

---

<a id="token-management"></a>
## 🔐 Token 管理

### 注销
用户表达"注销"时：

```bash
python3 ./scripts/tms_delivery.py delete-token
```

执行后再运行 `preflight`，确认包含 `setup_token`。提示用户：已注销，下次使用需重新获取 Token。

### 换 Token
用户表达"换 token"时：

```bash
python3 ./scripts/tms_delivery.py delete-token
# 引导用户获取新 token（展示 §1.1 的二维码模版）
python3 ./scripts/tms_delivery.py save-token <新token>
python3 ./scripts/tms_delivery.py preflight
```

