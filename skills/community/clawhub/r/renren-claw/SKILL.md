---
name: 人人商城龙虾助手
description: |
  人人商城龙虾助手 - 人人商城数据查询与订单管理工具。

  当用户提到以下意图时使用此技能：
  「查待办事项」「查运营数据」「查商品信息」「查会员信息」
  「查订单」「管理订单」「查优惠券」「设置满额包邮」
  「配置商城API」「验证API连通性」

  支持：待办事项查询、运营数据统计、商品/会员/订单全维度查询、优惠券管理、满额包邮规则配置，所有操作需基于用户提供的人人商城合法API凭证执行。
version: 2.0.0
author: likexin
metadata: { "openclaw": { "requires": { "python": [ "requests>=2.31.0" ] }, "primaryEnv": "RR_CLAW_API_KEY", "requiredEnv": [ "RR_CLAW_BASE_URL" ], "optionalEnv": [ ], "baseUrl": "${RR_CLAW_BASE_URL}", "homepage": "https://www.rrsc.cn", "securityNotes": "所有凭证由平台从 ~/.openclaw/openclaw.json 注入，技能代码仅通过参数接收，不直接读取配置文件；运行时仅向用户配置的 RR_CLAW_BASE_URL 发送请求，不会将凭证传输至任何第三方端点" } }
---

# 人人商城龙虾助手

## 一、必读约束

### 首次安装配置

在 `~/.openclaw/openclaw.json` 中添加凭证，平台启动时会自动读取该文件并将凭证注入技能运行上下文（技能代码本身不直接读取此文件）：

```json
{
    "skills": {
        "entries": {
            "renren-claw": {
                "apiKey": "你的RR_CLAW_API_KEY",
                "env": {
                    "RR_CLAW_BASE_URL": "你的人人商城API基础地址"
                }
            }
        }
    }
}
```

**获取凭证**：前往 [人人商城后台 > 插件 > 龙虾助手 > API Key管理] 获取 `API_KEY` 和 `服务器地址`。

### 安全约定

* 你操作的是用户线上的电商系统，任何失误都可能造成用户的经济损失
* 操作类接口提交时一定与用户确认好之后再进行操作
* 技能运行时仅向用户配置的 `RR_CLAW_BASE_URL` 发送请求，不会将 API Key 传输至任何第三方端点
* 严禁在聊天消息中明文输出 API Key

## 二、认证与请求方式

### 请求头

- `Authorization: Bearer $RR_CLAW_API_KEY`（格式：`lh-xxxxxxx-oc`）

### 请求方式

- **GET**：查询类接口
- **POST**：提交数据 / 操作类接口，请求体以 `application/x-www-form-urlencoded` 格式提交

#### 请求接口格式

RR_CLAW_BASE_URL + 接口地址

举例：https://example.com/wap/25/api/apps/openClaw/statistics/overview/to-do

#### 响应数据格式

- 所有接口统一返回 HTTP 200，**禁止以 HTTP 状态码判断成功或失败**
- 响应格式为 JSON：`{"error": 0, "message": "success", ...}`
- **必须检查 `error` 字段**：`0` = 成功，非 `0` = 业务失败（`message` 中包含错误描述）

#### 脚本请求示例

凭证由平台从 `~/.openclaw/openclaw.json` 注入，通过参数传递给客户端：

可自行拼接 cURL 请求，或调用 `scripts/request_client.py` 封装的客户端：

```python
from request_client import get_client

# 首次初始化：传入平台注入的凭证
client = get_client(base_url=RR_CLAW_BASE_URL, api_key=RR_CLAW_API_KEY)

# 后续调用直接复用已初始化的单例
client = get_client()
client.get("/some/path")
```

## 三、快速决策

| 用户意图       | 用户示例问法                | 调用接口                                 | 请求参数                    |
|------------|-----------------------|--------------------------------------|-------------------------|
| **数据统计模块** |                       |                                      |                         |
| 查询待办事项     | "待办事项"、"今天待办"、"待发货多少" | GET /statistics/overview/to-do       | 无                       |
| 查询今日运营数据   | "今日销售额"、"今天运营数据"      | GET /statistics/overview/operational | period=today            |
| 查询昨日运营数据   | "昨天销售额"、"昨日数据"        | GET /statistics/overview/operational | period=yesterday        |
| 查询近7天运营数据  | "近7天运营数据"             | GET /statistics/overview/operational | period=week             |
| 查询近30天运营数据 | "近30天数据"              | GET /statistics/overview/operational | period=month            |
| 新增会员统计     | "今日新增会员"、"近7天新会员"     | GET /statistics/overview/new-member  | period=today            |
| 新增订单统计     | "今日订单数"、"近7天订单趋势"     | GET /statistics/overview/new-order   | period=today            |
| 浏览量分析      | "今日浏览量"、"近7天PV/UV"    | GET /statistics/overview/view-data   | period=today            |
| 商品销量排行     | "销量排行榜"、"什么卖得好"       | GET /statistics/overview/goods-rank  | period=today            |
| 会员消费排行     | "会员消费榜"、"谁消费最多"       | GET /statistics/overview/member-rank | period=today            |
| 商品基础数据统计   | "近30天商品浏览加购数据"        | GET /statistics/goods/basic          | start_time、end_time(可选) |
| **商品模块**   |                       |                                      |                         |
| 查询商品列表     | "搜索iPhone"、"找商品"      | GET /goods/list/get                  | keywords(可选)            |
| 获取商品详情     | "商品ID 184的详情"         | GET /goods/detail/get                | id=184                  |
| 下架商品       | "下架商品ID 184"          | POST /goods/operation/put-store      | id=184                  |
| **会员模块**   |                       |                                      |                         |
| 查询会员列表     | "搜索会员An"、"找会员"        | GET /member/list/get                 | keywords(可选)            |
| 获取会员详情     | "会员ID 317的详情"         | GET /member/list/get                 | id=317                  |
| 通过手机号查会员ID | "手机号15888888888的会员ID" | GET /member/index/get-id-by-mobile   | mobile=15888888888      |
| **订单模块**   |                       |                                      |                         |
| 查询订单列表     | "查订单"、"待发货订单"         | GET /order/list/get                  | status(可选)              |
| 通过订单号查订单ID | "订单号xxx的ID"           | GET /order/index/get-id-by-no        | order_no=xxx            |
| 查询订单状态     | "订单xxx现在什么状态"         | GET /order/index/get-status          | order_no                |
| 查询订单物流     | "订单xxx的物流信息"          | GET /order/index/get-express         | order_no                |
| 关闭待支付订单    | "关闭订单ID 184"          | POST /order/operation/close          | id=184                  |
| **营销活动模块** |                       |                                      |                         |
| 优惠券概览      | "优惠券数据概览"             | GET /sales/coupon/overview           | 无                       |
| 查询优惠券列表    | "搜索优惠券"、"发放中的优惠券"     | GET /sales/coupon/list               | keywords(可选)            |
| 停止发放优惠券    | "停止发放优惠券ID 184"       | POST /sales/coupon/manual-stop       | id=184                  |
| 获取满额包邮设置   | "满额包邮设置"              | GET /sales/full-free/get             | 无                       |
| 关闭满额包邮     | "关闭满额包邮"              | POST /sales/full-free/close          | 无                       |

## 四、功能列表

### 数据统计模块

读取 [数据统计模块](references/statistics.md) 的接口文档。

### 商品查询管理模块

读取 [商品查询管理模块](references/goods.md) 的接口文档。

### 订单查询管理模块

读取 [订单查询管理模块](references/order.md) 的接口文档。

### 会员查询管理模块

读取 [会员查询管理模块](references/member.md) 的接口文档。

### 营销活动查询管理模块

读取 [营销活动查询管理模块](references/sales.md) 的接口文档。

## 五、意图判断指南

### 商城字段名词解释

| 字段名          | 说明   |
|--------------|------|
| goods        | 商品   |
| member       | 会员   |
| order        | 订单   |
| shop         | 店铺   |
| mall         | 综合商城 |
| communityBuy | 社区团购 |
| siteApp      | 智慧轻站 |
| promoter     | 推客带货 |

### 时间段判断

| 用户提到          | period参数值 |
|---------------|-----------|
| 今天、今日         | today     |
| 昨天、昨日         | yesterday |
| 近7天、一周、最近7天   | week      |
| 近30天、一月、最近30天 | month     |

### 功能关键词判断

| 关键词               | 对应功能     |
|-------------------|----------|
| 待办、待发货、待付款、待审核    | 待办事项接口   |
| 销售额、成交金额、运营数据、客单价 | 运营数据接口   |
| 新增会员、新会员          | 新增会员统计接口 |
| 新增订单、订单数          | 新增订单统计接口 |
| 浏览量、PV、UV、访问量     | 浏览量分析接口  |
| 销量、排行、卖得好、商品排行    | 商品销量排行接口 |
| 会员消费、消费榜、谁消费最多    | 会员消费排行接口 |
| 商品、搜索商品、找商品       | 商品列表接口   |
| 会员、搜索会员、找会员       | 会员列表接口   |
| 订单、查订单、订单状态       | 订单列表接口   |
| 物流、快递、物流信息        | 订单物流接口   |
| 优惠券               | 优惠券相关接口  |
| 满额包邮              | 满额包邮相关接口 |

### ⚠️ 危险操作（必须二次确认）

以下接口会直接影响线上业务，**执行前必须向用户明确确认，禁止自动执行**：

- `POST /goods/operation/put-store` — 下架商品（影响前台展示）
- `POST /order/operation/close` — 关闭订单（不可逆）
- `POST /sales/coupon/manual-stop` — 停止发放优惠券（立即生效）
- `POST /sales/full-free/close` — 关闭满额包邮（立即生效）
