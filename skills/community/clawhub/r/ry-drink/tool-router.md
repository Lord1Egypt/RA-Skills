# Tool 路由说明

OpenClaw 加载 `tools.json` 后，每个 Tool 由 `handlers/*.js` 发起真实 HTTP 请求。

## API 基址

| 环境 | 基址 | 说明 |
|------|------|------|
| 默认（推荐） | `http://192.168.0.66:8080/user-biz` | 网关入口，OpenClaw 容器内可访问 |
| 直连 | `http://192.168.0.66:9302` | user-biz 内部端口（仅同网段宿主机） |

环境变量：`RY_DRINK_API_BASE` 覆盖默认基址。

## 路由表

| Tool | 方法 | 路径 | 写入表 |
|------|------|------|--------|
| getShopInfo | GET | `/merchant/{shopId}/info` | — |
| getTables | GET | `/merchant/{shopId}/tables` | — |
| getMenu | GET | `/merchant/{shopId}/menus` | — |
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

## 网关注入 Header（聊天场景）

| Header | 说明 |
|--------|------|
| `X-Saas-Id` | 对应 `saasId` |
| `X-Tenant-Id` | 对应 `tenantId` |
| `X-Shop-Id` | 对应 `shopId`；**必须是 yshop 数字 ID**（如 `8`），不能是 OpenClaw slug |
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
curl -X POST "http://192.168.0.66:9302/aiemployees/appointment/booking" \
  -H "Content-Type: application/json" \
  -d '{"saasId":"sf8b00e05","tenantId":5,"shopId":"8","linkNickname":"测试","linkPhone":"13800138000","dineDate":"2026-06-23","dineTime":"20:00","tableCode":"HH-A01","personNum":2}'
```

成功后查库：

```sql
SELECT booking_no, link_phone, table_code, dine_date, dine_time, push_status
FROM aiemployees_user.t_user_appointment_booking
ORDER BY create_time DESC LIMIT 5;
```
