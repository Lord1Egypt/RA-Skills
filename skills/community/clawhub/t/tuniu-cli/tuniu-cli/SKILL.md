---
name: tuniu-cli
description: 途牛旅行统一助手（推荐优先使用）- 通过 tuniu CLI 统一调用机票、酒店、门票、火车票、邮轮、度假产品等旅行服务。适用于用户询问航班、酒店、景点门票、火车票、邮轮以及跟团游、自助游、自驾游等度假相关需求的场景。【优先级说明】当同时安装了 tuniu-flight/tuniu-hotel/tuniu-ticket/tuniu-train/tuniu-cruise 等单独服务 skill 时，请优先使用本 skill，它整合了所有服务能力且调用方式更简洁。
version: 1.0.4
minCliVersion: 1.0.7
metadata: {"openclaw": {"emoji": "🧳", "category": "travel", "tags": ["途牛", "旅行", "机票", "酒店", "门票", "火车票", "邮轮", "预订", "度假"], "priority": 100, "requires": {"bins": ["node", "npm", "tuniu"], "node": ">=18.0.0"}, "env": {"TUNIU_API_KEY": {"type": "string", "description": "途牛开放平台 API key，用于 apiKey 请求头", "required": true}}}}
---

# 途牛旅行助手

当用户询问航班、酒店、景点门票、火车票、邮轮、度假产品（跟团/自助/自驾/当地游等）等旅行服务时，使用此 skill 通过 **tuniu CLI** 调用途牛服务。

## 运行环境要求

**运行环境必须安装 Node.js 18+ 与 tuniu-cli**，否则无法调用服务。

### 首次使用前自检

在第一次调用 `tuniu` 前，按顺序检查运行环境：

```bash
node --version
npm --version
tuniu --version
```

- 若 `node` 不存在，或版本低于 18：不要继续安装 `tuniu-cli`；告知用户需先安装或升级 Node.js 18+，否则 `npm install -g tuniu-cli@latest` 会失败。
- 若 `npm` 不存在：告知用户需安装 Node.js/npm 后再继续。
- 若 `tuniu` 不存在，但 Node.js 版本满足要求，自动执行 `npm install -g tuniu-cli@latest`安装 CLI。
- 若 `tuniu` 已存在：检查版本是否满足本 skill 头部的 `minCliVersion`。低于该版本时，先更新 CLI，再继续业务调用。

### 安装 tuniu-cli

```bash
# npm 全局安装（推荐）
npm install -g tuniu-cli@latest

# 或使用 npx 临时调用
npx tuniu-cli --version
```

## 配置要求

### 必需配置

- **TUNIU_API_KEY**：途牛开放平台 API key，用于认证

用户需在 [途牛开放平台](https://open.tuniu.com/mcp/login) 注册并获取上述密钥。

```bash
export TUNIU_API_KEY=your_api_key
```

### API Key 检查与缺失时的安全处理

`TUNIU_API_KEY` 是敏感凭证：

- 如果已配置：直接调用 `tuniu`，不要要求用户重复提供 API Key，也不要改写用户环境变量或配置文件。
- 如果未配置：提示用户前往途牛开放平台获取 API Key。只有当用户在对话中主动提供 API Key，并明确希望 Agent 帮助配置时，才执行下面的安全处理规则。

用户提供 API Key 后，Agent 必须按以下规则处理：

1. **不要明文复述密钥**：API Key 只能用脱敏形式确认，例如 `tn_****abcd`，不得在回复、业务参数、日志摘要、调试输出中明文展示完整密钥。
2. **优先持久化到环境变量**：如果 Agent 有权限修改用户 shell 配置，征得用户同意后，将 `export TUNIU_API_KEY=...` 写入用户当前 shell 的启动文件（如 `~/.zshrc`、`~/.bashrc`、`~/.profile`），并提醒用户重新打开终端或执行 `source <文件>`。写入时不得把完整密钥打印到终端输出；若当前 Agent 会记录完整 shell 命令，不要代替用户执行包含真实密钥的命令；应提示用户在本地终端自行设置环境变量。
3. **无持久化权限时使用临时环境变量**：只能在当前会话中设置 `TUNIU_API_KEY`，并明确说明重启终端或 Agent 后可能需要重新配置。
4. **配置文件仅作兜底**：若无法设置环境变量，且用户明确同意把密钥写入本地文件，可初始化 `~/.tuniu-mcp/config.json` 并把各服务 `headers.apiKey` 从 `${TUNIU_API_KEY}` 改为实际密钥，同时将文件权限设为仅当前用户可读写（例如 `chmod 600 ~/.tuniu-mcp/config.json`）。
5. **优先使用宿主 Agent 的密钥/Secret 能力**：如果运行环境提供 Secret 管理、凭证输入框或受保护环境变量，应优先使用该能力，避免把密钥写入聊天记录或 shell 历史。

## 速查表

### 意图识别（用户说什么 → 用什么工具）

| 用户意图关键词 | server | 首选工具 | 必填参数 |
|---------------|--------|----------|----------|
| 航班/机票/飞机 | `flight` | `searchLowestPriceFlight` | `departureCityName`, `arrivalCityName`, `departureDate` |
| 酒店/住宿/民宿 | `hotel` | `tuniuHotelSearch` | `cityName` |
| 门票/景点门票 | `ticket` | `query_cheapest_tickets` | `scenic_name` |
| 火车票/高铁/动车 | `train` | `searchLowestPriceTrain` | `departureCityName`, `arrivalCityName`, `departureDate` |
| 邮轮/游轮 | `cruise` | `searchCruiseList` | `departsDateBegin`, `departsDateEnd` |
| 度假/跟团/自助游/自驾游/旅游线路 | `holiday` | `searchHolidayList` | 无单一必填（建议 `keyWord` 和/或结构化条件；若传出游日期则 `departsDateBegin` 与 `departsDateEnd` 需成对） |

### 基本命令格式

```bash
tuniu call <server> <tool> -a '<JSON参数>'
```

| 参数 | 说明 |
|------|------|
| `server` | 服务名称：`ticket`、`hotel`、`flight`、`train`、`cruise`、`holiday`、`traveler` |
| `tool` | 工具名称，如 `query_cheapest_tickets`、`searchLowestPriceFlight` 等 |
| `--args` 或 `-a` | 工具输入参数，必须是合法的 JSON 字符串 |

**重要**：`--args` 的值必须是 JSON 格式，且用引号包裹。中文可直接写入，无需转义。无参数时用空对象：`-a '{}'`

### 服务工具链路

| 服务 | 完整流程（搜索→详情→下单） |
|------|---------------------------|
| `flight` | `searchLowestPriceFlight` → `multiCabinDetails` → `saveOrder` → `cancelOrder` |
| `hotel` | `tuniuHotelSearch` → `tuniuHotelDetail` → `tuniuHotelCreateOrder` |
| `ticket` | `query_cheapest_tickets` → `create_ticket_order` |
| `train` | `searchLowestPriceTrain` → `queryTrainDetail` → `bookTrain` → `cancelOrder` |
| `cruise` | `searchCruiseList` → `getCruiseProductDetail` → `getCruiseCabinAndRoom` → `saveCruiseOrder` |
| `holiday` | `searchHolidayList` → `getHolidayProductDetail` → `getHolidayBookingRequiredInfo`（可选，预订说明）→ `saveHolidayOrder` |

### 常用辅助命令

| 命令 | 用途 |
|------|------|
| `tuniu list` / `tuniu list <server>` | 列出服务/工具 |
| `tuniu help <server> <tool>` | 查看参数说明 |
| `tuniu schema --output json` | 获取完整 Schema |
| `tuniu discovery refresh && tuniu discovery list` | 检查新服务 |
| `tuniu call ... -d` | 调试模式 |
| `tuniu skill version` | 查看已安装 skill 版本 |
| `tuniu skill install [--agent/--dir]` | 安装/更新 skill 到指定 Agent 或目录 |

---

## 服务发现触发条件

当遇到以下情况时，**必须**先执行 `tuniu discovery refresh && tuniu discovery list`：

1. **用户需求不在已知服务列表中**（如签证、租车、度假套餐等）
2. **tuniu list 返回的服务不包含用户需要的功能**
3. **工具调用返回"工具不存在"错误（退出码 102）**
4. **首次使用 tuniu-cli 时**（确保获取最新服务列表）

```bash
tuniu discovery refresh && tuniu discovery list
```

执行后重新检查服务列表，再决定下一步调用。若仍无法满足用户需求，才告知用户当前平台暂不支持该功能。

---

## Skill 版本与更新说明

`tuniu-cli` 提供 **skill** 子命令，用于维护本助手在各 AI Agent 目录下的安装与版本查看，与业务调用（`tuniu call`）相互独立。

### CLI 与 Skill 兼容性

本 skill 依赖 `tuniu-cli` 版本不低于头部声明的 `minCliVersion`。Agent 在使用本 skill 时必须遵循：

1. 若 `tuniu --version` 低于 `minCliVersion`，先执行 `npm install -g tuniu-cli@latest` 更新 CLI。
2. 更新 CLI 后执行 `tuniu --version` 确认版本，再执行 `tuniu skill install` 更新本地 skill。
3. 若全局 npm 安装无权限，先尝试提示用户授权或使用当前环境可用的安装方式；不要继续调用低版本 CLI 中不存在的命令。
4. 若更新失败，明确告知用户当前 CLI 版本与 skill 不兼容，部分操作可能失效。

**使用场景简述**

- **`tuniu skill version`**：在已配置多台 Agent（如 Cursor、Claude 等）时，检查各目录下已安装的 skill 版本、来源与安装时间；便于确认是否与文档站最新包一致。
- **`tuniu skill install`**：需要**安装或更新**本 skill 时使用。默认仅写入 `~/.agents/skills/tuniu-cli/`；通过 `--agent` 可指定单个、多个（逗号分隔）或 `all`（全部内置支持的 Agent）；`--dir` 可额外指定自定义 skills 根目录。
- **`npm install` / `npm ci`**：安装 `tuniu-cli` 时若启用脚本，**postinstall** 可能已根据本机存在的 Agent 父目录自动复制内置 skill；若需与线上一致或显式更新，仍建议执行 `tuniu skill install`。

更完整的参数与示例见：`tuniu skill install --help`。

---

## 隐私与个人信息（PII）说明

预订功能会将用户提供的**个人信息**（联系人姓名、手机号、乘客姓名、证件号等）通过 tuniu CLI 发送至途牛远端服务，以完成订单创建。使用本 skill 即表示用户知晓并同意上述 PII 被发送到外部服务。请勿在日志或回复中暴露用户个人信息。

## 适用场景

- 机票搜索、舱位查询、机票预订
- 酒店搜索、详情查询、酒店预订
- 景点门票查询、门票预订
- 火车票车次查询、车次详情、火车票预订
- 邮轮产品搜索、团期查询、邮轮预订（兼容"游轮"说法）
- 度假产品搜索、团期价格日历、度假预订（兼容跟团、自助游、自驾游、当地游等表述）
- **动态服务发现**：当用户旅行需求超出上述服务范围时，通过 discovery 功能检查是否有新服务上线

## 动态服务发现

途牛 CLI 支持动态发现新服务。**触发条件见上方 服务发现触发条件 章节**，满足条件时执行：

```bash
tuniu discovery refresh && tuniu discovery list
```

**服务发现默认开启**。如不确定，可先执行 `tuniu discovery status` 确认；若返回 `启用: 否`，手动开启：

```bash
export TUNIU_DISCOVERY_ENABLED=true
```

| 命令 | 用途 |
|------|------|
| `tuniu discovery status` | 查看启用状态、缓存状态、服务数量 |
| `tuniu discovery list` | 获取当前可用服务列表（失败时回退静态配置/缓存） |
| `tuniu discovery refresh` | 强制刷新缓存，获取最新服务列表 |

> 工具调用返回退出码 102 时，先执行 `tuniu discovery refresh && tuniu schema --output json`，再重试调用。

### 最佳实践

1. **初始化时**：执行 `tuniu discovery status` 确认服务发现状态（默认开启）
2. **遇到新需求时**：先执行 `tuniu discovery refresh` 刷新缓存，再 `tuniu discovery list` 查看最新服务
3. **获取新服务能力**：执行 `tuniu schema --output json` 获取最新工具定义
4. **降级处理**：如果 discovery 服务不可用，会自动回退到静态配置

## 各服务详细说明

### 1. 机票服务 (flight)

**触发词**：航班、机票、飞机、某地到某地航班、查机票、机票价格

#### 1.1 航班搜索 (searchLowestPriceFlight)

**支持 6 种查询模式**：
- **默认低价查询**：不传 searchType
- **TIME 时间范围查询**：searchType="TIME"，按出发/到达时间筛选
- **PRICE 价格区间查询**：searchType="PRICE"，按价格区间筛选
- **NEAR_GO 周边出发**：searchType="NEAR_GO"，查询出发地周边机场
- **NEAR_BACK 周边到达**：searchType="NEAR_BACK"，查询目的地周边机场
- **TRANSFER 中转查询**：searchType="TRANSFER"，查询中转航班

**必填参数**：`departureCityName`、`arrivalCityName`、`departureDate`（YYYY-MM-DD）

**翻页**：传相同城市日期参数 + `pageNum`（2=第二页，3=第三页…）

```bash
# 默认低价查询
tuniu call flight searchLowestPriceFlight -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15"}'

# TIME 模式：早班机
tuniu call flight searchLowestPriceFlight -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15","searchType":"TIME","departureTime":"06:00-10:00"}'

# 翻页查询
tuniu call flight searchLowestPriceFlight -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15","pageNum":2}'
```

#### 1.2 舱位详情查询 (multiCabinDetails)

**必填参数**：`departureCityName`、`arrivalCityName`、`departureDate`（YYYY-MM-DD）、`flightNo`

**返回**：`cabinPriceId`（下单必需）

```bash
tuniu call flight multiCabinDetails -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15","flightNo":"MU5101"}'
```

#### 1.3 创建订单 (saveOrder)

**前置条件**：必须先调用 `searchLowestPriceFlight` 和 `multiCabinDetails` 获取 `cabinPriceId`

**必填参数**：`departureCityName`、`arrivalCityName`、`departureDate`、`flightNo`、`cabinPriceId`、`tourists`、`contactTourist`

```bash
tuniu call flight saveOrder -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15","flightNo":"MU5101","cabinPriceId":"xxx","tourists":[{"name":"张三","idType":"身份证","idNumber":"310101199001011234","mobile":"13800138000"}],"contactTourist":{"name":"张三","mobile":"13800138000"}}'
```

#### 1.4 取消订单 (cancelOrder)

```bash
tuniu call flight cancelOrder -a '{"orderId":"订单号"}'
```

---

### 2. 酒店服务 (hotel)

**触发词**：酒店、住宿、民宿、某地酒店、入住、查酒店

#### 2.1 酒店搜索 (tuniuHotelSearch)

**必填参数**：`cityName`
**可选参数**：`checkIn`、`checkOut`（YYYY-MM-DD）、`keyword`、`prices`

**翻页**：传 `queryId`（首次搜索返回）和 `pageNum`

```bash
# 第一页
tuniu call hotel tuniuHotelSearch -a '{"cityName":"北京","checkIn":"2026-03-01","checkOut":"2026-03-03"}'

# 翻页（使用 queryId）
tuniu call hotel tuniuHotelSearch -a '{"queryId":"xxx","pageNum":2}'
```

#### 2.2 酒店详情 (tuniuHotelDetail)

**必填参数**：`hotelId` 或 `hotelName` 二选一

```bash
tuniu call hotel tuniuHotelDetail -a '{"hotelId":12345,"checkIn":"2026-03-01","checkOut":"2026-03-03"}'
```

#### 2.3 创建订单 (tuniuHotelCreateOrder)

**前置条件**：必须先调用 `tuniuHotelDetail` 获取 `preBookParam`

**必填参数**：`hotelId`、`roomId`、`preBookParam`、`checkInDate`、`checkOutDate`、`roomCount`、`roomGuests`、`contactName`、`contactPhone`

```bash
tuniu call hotel tuniuHotelCreateOrder -a '{"hotelId":"xxx","roomId":"xxx","preBookParam":"xxx","checkInDate":"2026-03-01","checkOutDate":"2026-03-03","roomCount":1,"roomGuests":[{"guests":[{"firstName":"三","lastName":"张"}]}],"contactName":"张三","contactPhone":"13800138000"}'
```

---

### 3. 门票服务 (ticket)

**触发词**：门票、景点门票、某景点门票、门票价格、门票多少钱

#### 3.1 门票查询 (query_cheapest_tickets)

**必填参数**：`scenic_name`（景点名称）

**返回**：`productId`、`resId`（下单必需）

```bash
tuniu call ticket query_cheapest_tickets -a '{"scenic_name":"中山陵"}'
```

#### 3.2 创建订单 (create_ticket_order)

**前置条件**：必须先调用 `query_cheapest_tickets` 获取 `productId` 和 `resId`

**必填参数**：`product_id`、`resource_id`、`depart_date`、`adult_num`、`contact_name`、`contact_mobile`、`tourist_1_name`、`tourist_1_mobile`、`tourist_1_cert_type`、`tourist_1_cert_no`

```bash
tuniu call ticket create_ticket_order -a '{"product_id":12345,"resource_id":"res001","depart_date":"2026-04-01","adult_num":1,"contact_name":"张三","contact_mobile":"13800138000","tourist_1_name":"张三","tourist_1_mobile":"13800138000","tourist_1_cert_type":"身份证","tourist_1_cert_no":"310101199001011234"}'
```

---

### 4. 火车票服务 (train)

**触发词**：火车票、火车、车次、某站到某站火车、高铁、动车

#### 4.1 查询车次列表 (searchLowestPriceTrain)

**必填参数**：`departureCityName`、`arrivalCityName`、`departureDate`（yyyy-MM-dd）
**可选参数**：`departureTime`、`arrivalTime`（时间范围，如"08:00-12:00"）、`searchType`（查询模式，默认值 `5`）

**searchType 取值说明**：
- `1`：按出发时间升序
- `2`：按出发时间降序
- `3`：按行程耗时升序
- `4`：按行程耗时降序
- `5`：按票价升序（默认）
- `6`：按票价降序

**翻页**：传首次查询返回的 `queryId` 和 `pageNum`

```bash
# 首次查询
tuniu call train searchLowestPriceTrain -a '{"departureCityName":"南京","arrivalCityName":"上海","departureDate":"2026-03-20","searchType":"5"}'

# 翻页
tuniu call train searchLowestPriceTrain -a '{"queryId":"xxx","pageNum":2}'
```

#### 4.2 查询车次详情 (queryTrainDetail)

**必填参数**：`departureStationName`、`arrivalStationName`、`departureDate`、`trainNum`

**返回**：`resId`、`price`、`departsDate`（下单必需）

```bash
tuniu call train queryTrainDetail -a '{"departureStationName":"南京南","arrivalStationName":"上海虹桥","departureDate":"2026-03-20","trainNum":"G203"}'
```

#### 4.3 预订下单 (bookTrain)

**前置条件**：必须先调用 `searchLowestPriceTrain` 和 `queryTrainDetail`

**必填参数**：`resources`、`adultTourists`、`contact`、`acceptStandingTicket`

```bash
tuniu call train bookTrain -a '{"acceptStandingTicket":false,"adultTourists":[{"name":"张三","psptId":"310101199001011234","psptType":1,"isStuDisabledArmyPolice":0,"tel":"13800138000"}],"contact":{"tel":"13800138000"},"resources":[{"resourceId":2121337089,"adultPrice":141.0,"departsDate":"2026-03-20"}]}'
```

#### 4.4 取消订单 (cancelOrder)

```bash
tuniu call train cancelOrder -a '{"orderId":"订单号"}'
```

---

### 5. 邮轮服务 (cruise)

**触发词**：邮轮、游轮、邮轮产品、游轮搜索、邮轮预订（兼容"游轮"说法）

#### 5.1 邮轮列表搜索 (searchCruiseList)

**必填参数**：`departsDateBegin`、`departsDateEnd`（YYYY-MM-DD）
**可选参数**：`cruiseLineName`（航线）、`cruiseBrand`（品牌）、`tourDay`（天数）、`pageNum`

**日期约束**：起始日期不得早于当天，结束日期不得早于起始日期

**筛选说明**：接口支持仅按日期查询；用户只给日期范围时直接查，不要为了补齐可选筛选而额外追问航线/品牌/天数。

**翻页说明**：用户说“还有吗/翻页/下一页”时，保持相同筛选条件，仅更新 `pageNum`（2/3/4...）。

**列表展示要求**：当前页 `data.rows` 需逐条展示，不应无说明地只列少量样例。

```bash
tuniu call cruise searchCruiseList -a '{"departsDateBegin":"2026-03-17","departsDateEnd":"2026-03-30"}'

# 按航线筛选
tuniu call cruise searchCruiseList -a '{"departsDateBegin":"2026-03-17","departsDateEnd":"2026-03-30","cruiseLineName":"长江三峡","cruiseBrand":"世纪邮轮"}'
```

#### 5.2 产品详情 (getCruiseProductDetail)

**所有参数必须从 searchCruiseList 返回结果中获取，且来自同一条 rows 记录**

**必填参数**：`productId`、`departsDateBegin`、`departsDateEnd`、`departCityCode`（数组格式，必须原样传递）、`classBrandParentId`、`proMode`

**团期规则**：必须展示 `productPriceCalendar` 中全部可售团期；若 `count=0` 或 `rows` 为空，明确告知无可售团期并停止后续下单链路。

```bash
tuniu call cruise getCruiseProductDetail -a '{"productId":"321648365","departsDateBegin":"2026-02-10","departsDateEnd":"2026-02-14","departCityCode":[1602],"classBrandParentId":12,"proMode":1}'
```

#### 5.3 邮轮基础信息（可选） (getCruiseBaseInfo)

**用途**：查询船只参数、餐饮娱乐、涵盖舱等说明；不替代可售房型查询。

```bash
tuniu call cruise getCruiseBaseInfo -a '{"productId":"321648365","traceId":"<可选traceId>"}'
```

#### 5.4 行程详情（可选） (getJourneyDetail)

**用途**：按天展开行程详情；与预订主链路解耦。

```bash
tuniu call cruise getJourneyDetail -a '{"productId":"321648365","traceId":"<可选traceId>"}'
```
#### 5.5 查询舱位房型 (getCruiseCabinAndRoom)

**必填参数**：`productId`、`departDate`（用户从团期列表选择的日期）

**参数来源约束**：`departDate` 必须来自 `getCruiseProductDetail.data.productPriceCalendar.rows[].departDate`。

**下单映射约束（关键）**：
- `journeyId` 必须来自本次返回的 `cabinList[].journeyId`
- `resourceId` 必须取用户所选房型 `priceRes` 中 `roomTypeResType=0` 条目的 `resId`
- `subResourceId`（可选）取同一 `priceRes` 中 `roomTypeResType=1` 条目的 `resId`
- 严禁把 `priceRes` 数组下标（0/1/2...）当作 `resourceId/subResourceId`
- 严禁复用历史对话中的 ID，必须以“最近一次”舱位查询结果为准

```bash
tuniu call cruise getCruiseCabinAndRoom -a '{"productId":"321648365","departDate":"2026-05-01"}'
```

#### 5.6 获取预订信息 (getCruiseBookingRequiredInfo)

**说明**：无参数，返回预订必填字段与合规提示文本。

```bash
tuniu call cruise getCruiseBookingRequiredInfo -a '{}'
```

#### 5.7 创建订单 (saveCruiseOrder)

**前置条件**：必须先调用 `getCruiseProductDetail`、`getCruiseCabinAndRoom`、`getCruiseBookingRequiredInfo`

**必填参数**：`productId`、`departureDate`、`departureCityName`、`duration`、`night`、`vendorId`、`selectRes`、`tourists`

**来源与校验要点**：
- `departureDate` 必须取 `getCruiseCabinAndRoom.data.base.beginDate`
- `selectRes[].journeyId/resourceId/subResourceId` 必须逐项回溯到最近一次 `getCruiseCabinAndRoom` 原始返回
- `resourceId/subResourceId` 必须是 `priceRes[].resId` 的真实值，不能是索引或推断值
- 建议透传 `getCruiseProductDetail` 的 `traceId` 到后续调用，便于排障

```bash
tuniu call cruise saveCruiseOrder -a '{"productId":"321648365","departureDate":"2026-05-01","departureCityName":"上海","duration":5,"night":4,"vendorId":73197,"selectRes":[{"journeyId":91808486,"resourceId":2121750804}],"tourists":[{"name":"张三","idType":"身份证","idNumber":"310101199001011234","mobile":"13800138000"}]}'
```

---

### 6. 度假产品服务 (holiday)

**触发词**：度假、跟团、自助游、自驾游、旅游产品、当地游、线路、目的地度假（与门票/酒店等区分时优先用列表搜索）

#### 6.1 度假列表搜索 (searchHolidayList)

**参数规则**：无单一必填参数。建议至少提供 `keyWord` 和/或结构化条件（日期、出发城市、产品类型等）。
**可选参数**：`keyWord`、`departsDateBegin`、`departsDateEnd`（成对出现，yyyy-MM-dd）、`departCityName`、`tourDay`、`queryTypeName`（`自驾游` / `自助游` / `跟团`）、`brandTypeName`、`conditions`、`lowPrice`、`highPrice`、`pageNum`

**keyWord 实操要点**：
- `keyWord` 用于承接目的地/主题等检索语义，不要混入“第2页/下一页”等翻页词
- 避免将“推荐/热门/受欢迎”等排序词写入 `keyWord`
- 翻页时保持筛选条件不变，仅更新 `pageNum`

**列表价格展示**：`searchHolidayList` 返回的 `price`、`starPrice` 等价为**起步价**。向用户展示时必须标注「起」（如 `¥38起`），不得写成确定价，避免误导。

```bash
tuniu call holiday searchHolidayList -a '{"keyWord":"三亚","departsDateBegin":"2026-04-10","departsDateEnd":"2026-04-15"}'

# 指定上海出发、跟团
tuniu call holiday searchHolidayList -a '{"keyWord":"云南","departsDateBegin":"2026-04-10","departsDateEnd":"2026-04-20","departCityName":"上海","queryTypeName":"跟团"}'
```

#### 6.2 产品详情 (getHolidayProductDetail)

**前置条件**：必须先调用 `searchHolidayList`，**所有入参须从列表 `data.rows[]` 对应行原样取得**（含 `departCityCode` 数组、`classBrandId`→`classBrandParentId`、`proMode` 等）。

**必填参数**：`productId`、`departCityCode`（数组）、`classBrandParentId`、`proMode`；若列表行含 `departsDateBegin`/`departsDateEnd` 则需成对传入且与列表一致。

**展示约束**：
- 团期需展示 `productPriceCalendar.rows` 中全部可选日期与价格
- 若 `count=0` 或 `rows` 为空，明确告知暂无可售团期并停止下单链路
- 若返回 `journeySummary`，按天（第N天+标题+模块）组织展示

```bash
tuniu call holiday getHolidayProductDetail -a '{"productId":"321619424","departCityCode":[1602],"classBrandParentId":12,"proMode":1}'
```

#### 6.3 预订说明 (getHolidayBookingRequiredInfo)

无参数，返回预订需填信息的中文说明（纯文本，直接展示，不做 JSON.parse）。

```bash
tuniu call holiday getHolidayBookingRequiredInfo -a '{}'
```

#### 6.4 创建订单 (saveHolidayOrder)

**前置条件**：必须先调用 `getHolidayProductDetail`；`departDate` 须来自详情中 `productPriceCalendar.rows[].departDate`；建议传入详情返回的 `traceId`。

**必填参数**：`productId`、`departDate`、`departCityName`、`duration`、`tourists`；`night` 可选（半日游可能为 0 或空）。

**参数来源约束**：`departCityName` 必须取 `getHolidayProductDetail.data.departureCityName`。

```bash
tuniu call holiday saveHolidayOrder -a '{"productId":"321619424","departDate":"2026-05-01","departCityName":"南京","duration":5,"night":4,"traceId":"<详情返回的traceId>","tourists":[{"name":"张三","idType":"身份证","idNumber":"310101199001011234","mobile":"13800138000"}]}'
```

---

## 响应处理

### 成功响应

stdout 输出 JSON 格式：

```json
{
  "success": true,
  "result": {...},
  "metadata": {...}
}
```

### 业务字段解析补充

- 通常 `tuniu call` 的 stdout 为统一 JSON 包装，业务结果在 `result` 内。
- 对于多数查询/下单工具，业务字段可按 JSON 对象读取。
- 对于 `getHolidayBookingRequiredInfo`、`getCruiseBookingRequiredInfo`，返回内容为预订说明文本，应按纯文本展示，不要强行按业务 JSON 结构解析。

### 错误响应

```json
{
  "success": false,
  "error": {
    "type": "ToolNotFoundError",
    "message": "工具不存在",
    "code": 102
  }
}
```

### 退出码含义

| 退出码 | 含义 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | 解析 stdout JSON |
| 101 | 连接失败 | 重试或检查网络 |
| 102 | 工具不存在 | 优先读取 `available_tools` 改用真实工具名；否则运行 `tuniu list <server> -o json` 校验 |
| 103 | 参数错误 | 运行 `tuniu help <server> <tool>` |
| 104 | 认证失败 | 检查 TUNIU_API_KEY |
| 105 | 超时 | 使用 `-t 60` 增加超时 |
| 108 | 未配置 API Key | 告知用户前往 [途牛开放平台](https://open.tuniu.com/mcp/login) 注册获取 API Key，并执行 `export TUNIU_API_KEY=your_api_key` |
| 199 | 未知错误 | 使用 `-d` 调试模式 |

---

## 使用示例

以下示例中，所有参数均从**用户表述或上一轮结果**中解析并填入。

### 机票场景

**用户**：3月15号北京到上海的航班

**AI 执行**：
```bash
tuniu call flight searchLowestPriceFlight -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15"}'
```

**用户**：看一下 MU5101 这个航班的舱位

**AI 执行**：
```bash
tuniu call flight multiCabinDetails -a '{"departureCityName":"北京","arrivalCityName":"上海","departureDate":"2026-03-15","flightNo":"MU5101"}'
```

### 酒店场景

**用户**：北京3月1号入住一晚，有什么酒店？

**AI 执行**：
```bash
tuniu call hotel tuniuHotelSearch -a '{"cityName":"北京","checkIn":"2026-03-01","checkOut":"2026-03-02"}'
```

### 门票场景

**用户**：中山陵门票多少钱？

**AI 执行**：
```bash
tuniu call ticket query_cheapest_tickets -a '{"scenic_name":"中山陵"}'
```

### 火车票场景

**用户**：3月20号南京到上海的火车票

**AI 执行**：
```bash
tuniu call train searchLowestPriceTrain -a '{"departureCityName":"南京","arrivalCityName":"上海","departureDate":"2026-03-20"}'

# 如果用户要求特定排序，例如“先看最便宜的”
tuniu call train searchLowestPriceTrain -a '{"departureCityName":"南京","arrivalCityName":"上海","departureDate":"2026-03-20","searchType":"5"}'
```

### 邮轮场景

**用户**：查一下3月17到3月30的邮轮

**AI 执行**：
```bash
tuniu call cruise searchCruiseList -a '{"departsDateBegin":"2026-03-17","departsDateEnd":"2026-03-30"}'
```

### 度假场景

**用户**：4月中旬想去三亚有什么度假线路？

**AI 执行**：
```bash
tuniu call holiday searchHolidayList -a '{"keyWord":"三亚","departsDateBegin":"2026-04-10","departsDateEnd":"2026-04-20"}'
```

---

## 注意事项

1. **密钥安全**：不要在回复或日志中暴露 TUNIU_API_KEY
2. **PII 安全**：联系人姓名、手机号、乘客姓名、证件号仅在预订时发送至 MCP 服务，勿在日志或回复中暴露
3. **认证**：若遇认证错误（退出码 104、108），必须告知用户前往 [途牛开放平台](https://open.tuniu.com/mcp/login) 注册获取 API Key，并提示设置 `TUNIU_API_KEY`
4. **日期格式**：所有日期均为 YYYY-MM-dd 或 yyyy-MM-dd
5. **参数验证**：下单前必须先调用搜索/详情接口获取必需参数（如 cabinPriceId、productId、resId 等）
6. **翻页**：各服务翻页参数不同，注意区分
7. **支付提醒**：下单成功后必须提示用户点击支付链接完成支付
8. **调试模式**：遇到问题时使用 `-d` 参数查看详细请求/响应
9. **游轮兼容**：用户说"游轮"时等同于"邮轮"
10. **度假详情参数**：`getHolidayProductDetail` 的 `departCityCode` 等字段必须与 `searchHolidayList` 列表行一致，勿拆数组或自行拼参；`saveHolidayOrder` 的 `departDate` 必须来自详情团期日历中的可选日期
11. **邮轮下单 ID 映射**：`saveCruiseOrder.selectRes` 的 `journeyId/resourceId/subResourceId` 只能来自最近一次 `getCruiseCabinAndRoom` 返回（`resourceId/subResourceId` 必须取 `priceRes[].resId`，不能用数组下标或历史 ID）
12. **团期价格展示口径**：成人/儿童价格均需基于可售团期原始字段展示；儿童价为 0 时不展示儿童价，双 0 团期不展示
13. **订单结果提示**：下单成功后应明确展示 `orderId` 与 `orderDetailUrl`，并提醒用户在途牛 App/小程序跟进订单与出行通知
14. **102 处理规则**：若错误 JSON 含 `error.details.available_tools`，优先从中选择符合当前意图的真实工具名并重试；否则执行 `tuniu list <server> -o json` 获取工具名，再用 `tuniu help <server> <tool>` 或 `tuniu schema <server> -o json` 确认参数。禁止继续用错误工具名重试。
