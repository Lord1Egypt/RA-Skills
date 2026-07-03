# Tool 路由说明

OpenClaw 加载 `tools.json` 后，每个 Tool 由 `handlers/*.js` 发起真实 HTTP 请求。

## API 基址

| 环境 | 基址 | 说明 |
|------|------|------|
| 默认（内网直连，推荐） | `http://10.200.100.32:9302` | OpenClaw 与 user-biz 同网段时直连，少一跳、不依赖 Gateway 路由 |
| 经 Gateway（可选） | `http://10.200.100.32:43000/user-biz` | 仅当 9302 不可达或须走网关负载均衡时使用 |

环境变量：`RY_DRINK_API_BASE` 覆盖默认基址；`RY_DRINK_SAAS_ID` / `RY_DRINK_PLATFORM_TENANT_ID` / `RY_DRINK_FORCED_SHOP_ID` / `RY_DRINK_LINK_PHONE` 由平台按会话动态注入，**勿在 Nacos 写死 saas-id、tenant-id**。

## 查询 vs 写入

| 类型 | Tool | 说明 |
|------|------|------|
| **查询（只读，也必须调 HTTP）** | getShopInfo、getMenu、getTables、listMyAppointments、listOrders、getOrderDetail、getMemberInfo、getTransactions | 禁止凭记忆/知识库回答；查看点餐须 listOrders 且逐单 getOrderDetail |
| **查询+本地生成** | buildPaymentLink | 买单/付款/结账；优先 thirdOrderId 拼链接 |
| **写入** | bookTable、changeAppointment、cancelAppointment、placeOrder、appendOrder、reduceOrder、cancelOrder | 须先完成相关查询 Tool |

## 路由表

| Tool | 方法 | 路径 | 写入表 |
|------|------|------|--------|
| getShopInfo | GET | `/merchant/{tenantId}/info?storeId={shopId}` | — |
| getMenu | GET | `/merchant/{tenantId}/menus?storeId={shopId}` | — |
| getTables | GET | `/aiemployees/appointment/tables?shopId=` | — |
| getMemberInfo | GET | `/member/{memberId}` | — |
| getTransactions | GET | `/transaction/list` | — |
| listMyAppointments | GET | `/aiemployees/appointment/list` | `t_user_appointment_booking`（读） |
| bookTable | POST | `/aiemployees/appointment/booking` | `t_user_appointment_booking`（写） |
| changeAppointment | POST | `/aiemployees/appointment/change` | `t_user_appointment_booking` |
| cancelAppointment | POST | `/aiemployees/appointment/cancel` | `t_user_appointment_booking` |
| placeOrder | POST | `/aiemployees/dining/order` | `t_user_dining_order` |
| appendOrder | POST | `/aiemployees/dining/append` | `t_user_dining_order` |
| reduceOrder | POST | `/aiemployees/dining/reduce` | 减餐记录 |
| cancelOrder | POST | `/aiemployees/dining/cancel` | `t_user_dining_order` |
| listOrders | POST | `/aiemployees/dining/tool/invoke` | 读 |
| getOrderDetail | POST | `/aiemployees/dining/detail` | 读 |
| buildPaymentLink | POST | `/aiemployees/dining/payment/link` | 读 |

## 网关注入 Header（聊天场景）

| Header | 说明 |
|--------|------|
| `X-Saas-Id` | 对应 `saasId` |
| `X-Tenant-Id` | 对应 `tenantId`（平台租客 ID，`t_merchant.id`） |
| `X-Shop-Id` | 对应 `shopId`（门店数字 ID，`t_store_sync.id`）；不能是 OpenClaw slug |
| `X-Mobile` | 对应 `linkPhone` |

Handler 优先使用 OpenClaw 环境变量 `RY_DRINK_FORCED_SHOP_ID`（user-system 按会话 merchantId 写入）；禁止 LLM 改用其他 shopId。

## 部署

将整个 `ry-drink/` 目录同步到 OpenClaw workspace：

```
/home/node/.openclaw/workspace/skills/ry-drink/
├── SKILL.md
├── tools.json
├── skill.json
├── tool-router.md
└── handlers/
    ├── _http.js
    └── *.js
```

安装后在商家端「已安装技能」确认 **ry-drink 已启用**（非「已停用/待部署」）。

## 验证 bookTable

```bash
curl -X POST "http://10.200.100.32:9302/aiemployees/appointment/booking" \
  -H "Content-Type: application/json" \
  -d '{"saasId":"sf8b00e05","tenantId":5,"shopId":"8","linkNickname":"测试","linkPhone":"13800138000","dineDate":"2026-06-23","dineTime":"20:00","tableCode":"HH-A01","personNum":2}'
```

成功后查库：

```sql
SELECT booking_no, link_phone, table_code, dine_date, dine_time, push_status
FROM aiemployees_user.t_user_appointment_booking
ORDER BY create_time DESC LIMIT 5;
```
