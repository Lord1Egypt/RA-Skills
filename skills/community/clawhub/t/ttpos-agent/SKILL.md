---
name: ttpos-agent
description: >
  通过 ttpos-agent API 查询 TTPOS 餐饮系统营业数据，生成报表。使用前必须访问 GET /api/v1/query/guide 获取数据查询指南。Use when: 今日营业额、订单统计、支付方式、菜品排行、会员分析、班次汇总、时段分析等。NOT for: 与 TTPOS 数据无关的问题。
metadata:
  openclaw:
    emoji: "📊"
    primaryEnv: "LIGHT_BRIDGE_API_KEY"
    requires:
      env: ["LIGHT_BRIDGE_API_KEY"]
    env:
      LIGHT_BRIDGE_URL: "https://claw.doge6.com"
---

# ttpos-agent 数据查询技能

通过 ttpos-agent HTTP API 查询 TTPOS 餐饮系统数据，生成营业报表、订单统计、支付分析等。

## ⚠️ 必须首先执行

**在构造任何 SQL 或调用 API 之前，必须先访问接口获取数据查询指南：**

```
GET {LIGHT_BRIDGE_URL}/api/v1/query/guide
```

请求头需带 `Authorization: Bearer $LIGHT_BRIDGE_API_KEY`。返回的 Markdown 包含：多租户架构、订单/商品/桌台/会员/班次/统计表结构、时间与金额约定、常用查询模式、常见陷阱。**不获取此指南会导致表名错误、字段误用、统计重复。**

---

## Config（必须输入）

| 配置项 | 必填 | 说明 |
|--------|------|------|
| **LIGHT_BRIDGE_API_KEY** | ✅ | 在 [ttpos-agent Web 面板](https://claw.doge6.com/web/dashboard) 创建，在技能面板保存 |

---

## 工作流程

1. **获取指南**：`GET {LIGHT_BRIDGE_URL}/api/v1/query/guide`，理解数据模型与查询规范
2. **获取商户列表**：`GET {LIGHT_BRIDGE_URL}/api/v1/query/companies`，确认可用的 `company_uuid`
3. **构造 SQL**：根据用户问题，按指南中的表结构、统计表、时间筛选规则编写 SQL
4. **执行查询**：`POST {LIGHT_BRIDGE_URL}/api/v1/query/execute`，Body: `{"company_uuid": xxx, "sql": "SELECT ..."}`
5. **呈现结果**：用简洁语言总结，金额使用 ROUND 和当地货币符号；**不展示字段名**，枚举值翻译为中文（如 platform→平台、order_state→订单状态、DELIVERED→已送达）

---

## API 调用示例

### 获取数据查询指南（必须首先调用）

```bash
curl -s -H "Authorization: Bearer $LIGHT_BRIDGE_API_KEY" \
 "$LIGHT_BRIDGE_URL/api/v1/query/guide"
```

### 获取可访问商户

```bash
curl -s -H "Authorization: Bearer $LIGHT_BRIDGE_API_KEY" \
 "$LIGHT_BRIDGE_URL/api/v1/query/companies"
```

### 执行 SQL 查询

```bash
curl -s -X POST "$LIGHT_BRIDGE_URL/api/v1/query/execute" \
 -H "Authorization: Bearer $LIGHT_BRIDGE_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{"company_uuid": 8267304538112000, "sql": "SELECT ..."}'
```

### 获取表结构（可选）

```bash
curl -s -H "Authorization: Bearer $LIGHT_BRIDGE_API_KEY" \
 "$LIGHT_BRIDGE_URL/api/v1/query/schema?company_uuid=8267304538112000"
```

---

## 重要规则

- **只输出最终结论**：工具执行后，仅呈现整理后的表格或总结，不要逐字复述 API 原始返回
- **不展示原始字段名**：禁止直接输出 `platform`、`order_state`、`eater_payment`、`accepted_time` 等数据库字段名；改用「平台」「订单状态」「订单金额」「接单时间」等中文表述
- **枚举值需翻译**：`order_state`(0/10/20/30/40/50/60)、`platform_order_state`(DELIVERED/CANCELLED 等) 必须译为中文（如：已完成、已取消、已送达、骑手已到店）；`platform` 的 grab/lineman 等译为 Grab、LINE MAN
- **先访问 GET /api/v1/query/guide 获取指南**，再写 SQL
- **始终加 `WHERE delete_time = 0`**
- **优先使用 ttpos_statistics_* 统计表**
- **时间用 complete_time 或 finish_time**，不用 create_time
- **金额展示用 ROUND(x, 2)**，指出货币单位
- **单次查询时间范围不宜超过 3 个月**，大数据加 LIMIT

---

## 认证失败时

若 API 返回 401 或缺少 LIGHT_BRIDGE_API_KEY：

**只回复**：「请在技能面板的 API key 输入框中保存你的 ttpos-agent API Key。API Key 在 [ttpos-agent Web 面板](https://claw.doge6.com/web/dashboard)（登录后）创建。」

配置完成后 使用 "/clear" 新建会话 再立即继续用户原来的请求。
