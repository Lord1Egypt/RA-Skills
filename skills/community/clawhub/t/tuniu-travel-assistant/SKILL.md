---
name: tuniu-travel-assistant
display_name: "途牛旅行助手"
description: 零配置即装即用，旅行全品类查询预订，酒店/机票/火车票/景点门票/邮轮/度假一站式服务，17个工具覆盖全品类API，含图片渲染和服务间互推荐。
tags:
  - 旅行预订
  - 酒店查询
  - 机票查询
  - 火车票查询
  - 景点门票
  - 邮轮
  - 度假
  - 旅行助手
  - 出行
  - 全品类
tools:
  - name: search_hotel
    description: 搜索酒店
  - name: search_flight
    description: 搜索机票
  - name: search_train
    description: 搜索火车票
  - name: search_scenic
    description: 搜索景点门票
  - name: search_cruise
    description: 搜索邮轮
  - name: search_group
    description: 搜索度假产品
primaryEnv: PROXY_TOKEN

---

# 途牛旅行助手

零配置即装即用的全品类旅行查询预订技能，17个工具覆盖酒店/机票/火车票/景点门票/邮轮/度假全品类API。搜索结果含酒店和邮轮图片，各查询工具自动推荐关联服务。

## 核心功能

### 🏨 酒店（3个工具）
- **hotel_search** — 酒店搜索，按城市+日期查询，支持关键词/商圈筛选和翻页，含酒店图片
- **hotel_detail** — 酒店详情+房型报价，返回preBookParam用于下单，含酒店及房型图片
- **hotel_create_order** — 酒店预订下单

### ✈️ 机票（5个工具）
- **flight_search** — 机票搜索，6种查询模式（默认/时间/价格/周边出发/周边到达/中转）
- **flight_cabin_detail** — 舱位价格详情，返回cabinPriceId用于下单，含退改规则
- **flight_booking_info** — 获取预订必填字段说明
- **flight_save_order** — 机票预订下单
- **flight_cancel_order** — 取消机票订单

### 🚄 火车票（5个工具）
- **train_search** — 火车票搜索，6种排序（出发时间/耗时/票价升降）
- **train_detail** — 车次座位详情+余票，返回resId用于预订
- **train_book** — 火车票预订
- **train_order_detail** — 火车票订单详情
- **train_cancel_order** — 取消火车票订单

### 🎫 门票（2个工具）
- **ticket_query** — 景点门票查询，返回productId+resId
- **ticket_create_order** — 门票预订下单

### 🚢 邮轮（1个工具）
- **cruise_search** — 邮轮搜索，按日期范围和航线搜索邮轮产品，含邮轮图片

### 🏖️ 度假（1个工具）
- **holiday_search** — 度假产品搜索，搜索跟团游/自由行，支持按目的地/天数/价格筛选

## 图片渲染

- **酒店搜索**：每条酒店结果附带 `![酒店图片](firstPic)` Markdown图片
- **酒店详情**：酒店首图 + 各房型图片
- **邮轮搜索**：每条邮轮结果附带 `![邮轮图片](picUrl)` Markdown图片

## 服务间互推荐

每个查询工具的返回结果末尾自动推荐关联服务：

| 当前工具 | 推荐服务 |
|---------|---------|
| 酒店搜索 | 🎫景点门票 · 🚄火车票 · ✈️机票 · 🚢邮轮 |
| 酒店详情 | 🎫景点门票 · 🚄火车票 · ✈️机票 |
| 机票搜索 | 🏨酒店 · 🚄火车票 · 🎫景点门票 · 🚢邮轮 |
| 舱位详情 | 🏨酒店 · 🚄火车票 |
| 火车票搜索 | 🏨酒店 · ✈️机票 · 🎫景点门票 · 🚢邮轮 |
| 车次详情 | 🏨酒店 · ✈️机票 · 🎫景点门票 |
| 门票查询 | 🏨酒店 · 🚄火车票 · ✈️机票 · 🚢邮轮 |
| 邮轮搜索 | 🏨酒店 · 🚄火车票 · ✈️机票 · 🎫景点门票 |
| 度假搜索 | 🏨酒店 · ✈️机票 · 🚄火车票 · 🎫景点门票 · 🚢邮轮 |

## 参数说明

### hotel_search
- **cityName**（首页必填）— 城市名，如：上海、北京
- **checkInDate**（首页必填）— 入住日期，格式：YYYY-MM-DD
- **checkOutDate**（首页必填）— 离店日期，格式：YYYY-MM-DD
- keyword / districtName — 可选筛选
- **queryId** + **pageNum** — 翻页时使用

### hotel_detail
- **hotelId** 或 **hotelName**（必填）— 酒店ID或名称
- **checkInDate** / **checkOutDate**（必填）— 入住离店日期

### flight_search
- **departureCityName**（必填）— 出发城市，如：北京
- **arrivalCityName**（必填）— 到达城市，如：上海
- **departureDate**（必填）— 出发日期，格式：YYYY-MM-DD
- sortType — 排序：0价格1时间2折扣

### train_search
- **departureCityName**（首页必填）— 出发城市
- **arrivalCityName**（首页必填）— 到达城市
- **departureDate**（首页必填）— 出发日期
- sortType — 排序：0出发升/1出发降/2耗时升/3耗时降/4票价升/5票价降

### ticket_query
- **scenic_name**（必填）— 景点名称，如：故宫、迪士尼

### cruise_search
- **departsDateBegin** — 出发日期范围-开始，不填默认明天
- **departsDateEnd** — 出发日期范围-结束，不填默认30天后
- **cruiseLineName** — 邮轮航线名称，如：日本、东南亚
- pageNum / pageSize — 分页

### holiday_search
- **keyWord** — 关键词，如：三亚、日本、亲子
- **tourDay** — 行程天数，如5
- **queryTypeName** — 产品类型：跟团游、自由行
- **highPrice** / **lowPrice** — 价格范围
- **departCityName** — 出发城市
- **departsDateBegin** / **departsDateEnd** — 出发日期范围
- pageNum / pageSize — 分页

## 使用示例

- "查上海6月15到17号的酒店" → `hotel_search(cityName="上海", checkInDate="2026-06-15", checkOutDate="2026-06-17")`
- "北京到上海6月20的机票" → `flight_search(departureCityName="北京", arrivalCityName="上海", departureDate="2026-06-20")`
- "广州到深圳明天的火车票" → `train_search(departureCityName="广州", arrivalCityName="深圳", departureDate="2026-06-23")`
- "故宫门票多少钱" → `ticket_query(scenic_name="故宫")`
- "有什么日本邮轮" → `cruise_search(cruiseLineName="日本")`
- "三亚5天跟团游" → `holiday_search(keyWord="三亚", tourDay=5, queryTypeName="跟团游")`

## 不能做

- 下单类工具需要多步操作（先查询获取ID→再下单），无法一步完成
- 部分小城市火车票/机票数据覆盖可能不完整，建议用大城市名查询

## 数据流向

用户输入（旅行查询需求）→ 本技能脚本 → 代理服务（认证令牌通过环境变量安全读取，代理URL限定为腾讯云SCF端点，防止流量被重定向）→ 旅游平台API → 返回结果给用户。

### 查询类工具（hotel_search / flight_search / train_search / ticket_query / cruise_search / holiday_search）
- 发送参数：城市名、日期、搜索条件等
- **不包含任何个人身份信息**
- 代理仅做请求转发，不存储查询记录

### 下单类工具（hotel_create_order / flight_save_order / train_book / ticket_create_order）
当用户主动发起预订时，需提供以下信息以完成订单：
- 酒店下单：酒店ID、房型ID、入住离店日期、入住人数、联系人姓名、联系电话
- 机票下单：航班信息、舱位价格ID、乘客信息（姓名、证件类型、证件号、联系电话）
- 火车票下单：车次资源、成人乘客列表（姓名、证件类型、证件号）、联系人信息
- 门票下单：产品ID、资源ID、游玩日期、游客信息（姓名、手机号、证件类型、证件号）

**数据处理说明**：
- 上述个人身份信息仅在用户明确下单时由用户主动提供
- 信息直接转发至旅游平台完成订单，本技能不进行本地存储或二次转发
- 本技能不处理支付流程、不存储支付凭证、不记录敏感信息
- 订单完成后相关信息归旅游平台管理，本技能无权访问

## 安全声明

- 认证令牌通过环境变量 `PROXY_TOKEN` 安全读取，源码中无任何硬编码密钥
- 代理服务地址通过环境变量 `PROXY_URL` 配置，代码内置域名校验，仅允许腾讯云SCF端点，防止流量被重定向到未授权服务器
- 所有HTTPS请求使用 ssl.create_default_context() 启用证书验证（verify_mode=CERT_REQUIRED, check_hostname=True）
- 本技能不处理支付流程、不存储支付凭证、不记录用户敏感信息
- 个人身份信息（姓名、证件号、手机号）仅在用户主动发起下单时由用户提供，直接转发至旅游平台，不经本地存储
