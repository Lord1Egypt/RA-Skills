# 迁移方案报告：mcp-server-google-flights + OpenSky Network

## 执行摘要

本报告评估将 variflight-aviation-skill 项目从 AviationStack（免费套餐，每月约100次请求）迁移至两个替代数据源的可行性：mcp-server-google-flights 负责机票搜索与价格查询，OpenSky Network 负责实时飞机位置追踪。核心结论是：**两者的组合可以覆盖原有部分功能，但均存在明显局限——前者不支持按航班号查询且无实时状态，后者在中国境内覆盖极为稀疏**，对于以中国国内航班为主的场景，该迁移方案价值有限。

## 背景

当前项目使用 AviationStack MCP（aviationstack-mcp，通过 uvx 启动）作为底层数据源，实现了六个命令：info（航班详情）、search（航线搜索）、track（实时追踪）、comfort（舒适度评分）、transfer（中转方案）、weather（机场天气）。免费套餐的主要限制是每月约100次API请求、无历史航班访问权限、MCP 工具每次随机返回约20条数据。

## mcp-server-google-flights 详细分析

### 项目现状

目前没有一个统一的"官方"mcp-server-google-flights，而是有多个社区实现，其中最完整的是 HaroldLeo/google-flights-mcp（PyPI 包名 `mcp-server-google-flights`），同时还有 tistaharahap/google-flights-mcp（PyPI 包名 `google-flights-mcp`）、random-robbie/Flight-Search-MCP-Server 以及 modellers/mcp-google-travels（npm 包 `@taskingagency/mcp-google-travels`）。

### 核心能力（以 HaroldLeo 版本为准）

该 MCP 服务器提供9个工具，均以"出发机场 + 目的地机场 + 日期"为核心参数，包括：

- `search_one_way_flights` / `search_round_trip_flights`：单程和往返搜索
- `search_round_trips_in_date_range`：灵活日期区间搜索
- `get_multi_city_flights`：多城市行程
- `search_direct_flights`：仅直飞
- `search_flights_by_airline`：按航司或联盟筛选（如"CA"或"STAR_ALLIANCE"）
- `search_flights_with_max_stops`：按最大中转次数筛选
- `get_travel_dates`：计算旅行日期（辅助工具）
- `generate_google_flights_url`：生成可分享的 Google Flights 链接

### 安装方式

```bash
# Python 版（推荐，无需 API Key 即可使用 fast-flights 爬取）
uvx mcp-server-google-flights

# 配置（带 SerpAPI Key 可选，更稳定）
# claude_desktop_config.json 或 .cline/cline_mcp_settings.json：
{
  "mcpServers": {
    "google-flights": {
      "command": "uvx",
      "args": ["mcp-server-google-flights"],
      "env": {
        "SERPAPI_API_KEY": "your_serpapi_key_here"  // 可选
      }
    }
  }
}

# Node.js 版（需要 SerpAPI Key）
npx -y @taskingagency/mcp-google-travels
```

### 数据来源与免费配额

该工具有两种数据来源，优先使用 fast-flights（无需 API Key，基于 Google Flights Protobuf 接口逆向），失败时回退到 SerpAPI。SerpAPI 免费套餐每月250次搜索，付费套餐从 $50/月（5000次）起。fast-flights 无配额限制，但受 Google 反爬机制影响，高频访问可能被封锁。

SerpAPI 模式返回字段包括 `flight_number`、`airline`、`departure_airport`（含 IATA 代码和时间）、`arrival_airport`、`duration`、`price`、`carbon_emissions`、`booking_token` 等完整信息；fast-flights 模式字段较少，不含航班号。

### 与现有命令的适配性评估

| 现有命令 | 适配情况 | 说明 |
|---------|---------|------|
| `search <dep> <arr> <date>` | ✅ 可迁移 | `search_one_way_flights(origin, destination, date)` 直接对应 |
| `info <fnum>` | ❌ 无法迁移 | 所有工具均不支持按航班号（如 CA1234）查询；不返回延误/实际起降时间 |
| `track <fnum>` | ❌ 无法迁移 | 无实时飞行状态，无法追踪具体航班当前位置和飞行阶段 |
| `comfort <fnum>` | ❌ 无法迁移 | 需要机型数据，Google Flights 仅部分返回 `airplane` 字段 |
| `transfer <dep> <arr>` | ⚠️ 间接支持 | 可用 `search_flights_with_max_stops(max_stops=1)` 搜索中转方案，但无法定制中转点 |
| `weather <airport>` | ❌ 不相关 | 纯天气功能，与本工具无关 |

### 关键局限性

Google Flights 系列 MCP 工具本质上是"机票预订辅助工具"，聚焦价格和时刻表，**完全不提供实时飞行状态、延误信息、航班追踪**。对于中国国内航班，Google Flights 数据覆盖不如携程、去哪儿等国内平台完整。

## OpenSky Network API 详细分析

### 项目概述

OpenSky Network 是一个非营利学术项目，依托全球5000+志愿者贡献的 ADS-B 接收器，提供实时和历史飞机位置数据。API 版本 1.4.0，Base URL 为 `https://opensky-network.org/api`。

### 认证方式（重要变更）

自2026年3月18日起，Basic Auth（用户名/密码）已完全废弃，**现在必须使用 OAuth2 客户端凭证流**：

```bash
# Step 1: 在 opensky-network.org 注册账号，创建 API 客户端，下载 credentials.json
# Step 2: 获取 Access Token（有效期30分钟）
curl -X POST \
  "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
# Step 3: 携带 Bearer Token 调用 API
curl -H "Authorization: Bearer YOUR_TOKEN" "https://opensky-network.org/api/states/all"
```

### 核心 API 端点

`GET /api/states/all` 是最核心的端点，返回当前所有可见飞机的状态向量数组。每条状态向量按索引顺序包含：`icao24`（唯一标识）、`callsign`（呼号，如 `CCA1234`）、`origin_country`、`time_position`、`last_contact`、`longitude`、`latitude`、`baro_altitude`（气压高度，米）、`on_ground`（是否在地）、`velocity`（对地速度，米/秒）、`true_track`（真实航向，度）、`vertical_rate`（垂直速率，米/秒）、`geo_altitude`、`squawk`（应答机代码）及 `position_source`（0=ADS-B，1=ASTERIX，2=MLAT）。

其他重要端点：`GET /api/flights/aircraft?icao24=xxx&begin=ts&end=ts`（历史航班，仅前一天起，时间区间≤30天）；`GET /api/flights/arrival?airport=ZBAA&begin=ts&end=ts`（机场到达，区间≤2天）；`GET /api/flights/departure`（出发，同限制）；`GET /api/tracks?icao24=xxx&time=0`（实时轨迹，实验性功能）。

### 使用限制

| 用户类型 | 每日 API 积分 | 时间分辨率 | 历史数据 |
|---------|-------------|-----------|---------|
| 匿名用户 | 400 credits | 10秒 | 仅当前时刻 |
| 注册用户 | 4,000 credits | 5秒 | 过去1小时 |
| 活跃贡献者 | 8,000 credits | 5秒 | 过去1小时 |

`/states/all` 按查询区域消耗积分：小区域（<500×500km）消耗1 credit，全球查询消耗4 credits。超限返回 HTTP 429，响应头 `X-Rate-Limit-Retry-After-Seconds` 给出等待时间。注意：OpenSky **明确禁止商业用途**，违反需联系 contact@opensky-network.org 另行协商。

### callsign 与航班号的对应关系

ADS-B 中广播的 `callsign` 使用**航司 ICAO 三字母代码**而非 IATA 二字母代码，例如国航 CA1234 的呼号是 `CCA1234`，东方航空 MU5735 的呼号是 `CES5735`，南方航空 CZ3101 的呼号是 `CSN3101`。callsign 最多8字符，可能有尾随空格，比较时需要 `trim()`。查找特定航班可通过 `/states/all` 获取全量数据后过滤 `callsign` 字段（索引1）。

### 中国境内覆盖情况（核心局限）

这是最关键的问题。OpenSky 依赖志愿者贡献的 ADS-B 地面接收器，**中国境内接收器数量极为稀少**，原因包括：接收器贡献者集中在欧美；中国对 ADS-B 数据的开放有一定政策限制；来自 AWS 等云服务商 IP 可能被封锁。实际效果是，在中国大城市机场附近（北京 ZBAA 周边）可能有零散数据点，广大内陆和西部地区基本无覆盖，与欧洲（几乎无死角）和美国大陆（90%+）相比差距悬殊。这意味着 OpenSky 对于追踪中国国内航班实时位置**基本不可用**。

### Node.js 集成示例

```javascript
// opensky-client.js（核心工具类）
class OpenSkyClient {
  constructor(clientId, clientSecret) {
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.baseUrl = 'https://opensky-network.org/api';
    this.tokenUrl = 'https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token';
    this.accessToken = null;
    this.tokenExpiry = 0;
  }

  async getToken() {
    const now = Date.now();
    if (this.accessToken && now < this.tokenExpiry - 60000) return this.accessToken;
    const params = new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: this.clientId,
      client_secret: this.clientSecret,
    });
    const res = await fetch(this.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    const data = await res.json();
    this.accessToken = data.access_token;
    this.tokenExpiry = now + data.expires_in * 1000;
    return this.accessToken;
  }

  async request(path, params = {}) {
    const token = await this.getToken();
    const url = new URL(this.baseUrl + path);
    Object.entries(params).forEach(([k, v]) => {
      if (Array.isArray(v)) v.forEach(val => url.searchParams.append(k, val));
      else if (v != null) url.searchParams.set(k, v);
    });
    const res = await fetch(url.toString(), {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (res.status === 429) throw new Error('Rate limit exceeded');
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  }

  // 通过 callsign 在全量数据中查找飞机（需 ICAO 三字母代码）
  // 例：CA1234 → findByCallsign('CCA1234')
  async findByCallsign(callsign) {
    const data = await this.request('/states/all');
    if (!data?.states) return [];
    const normalized = callsign.trim().toUpperCase();
    return data.states.filter(sv => sv[1]?.trim().toUpperCase() === normalized)
      .map(sv => ({
        icao24: sv[0], callsign: sv[1]?.trim(),
        latitude: sv[6], longitude: sv[5],
        altitude: sv[7], velocity: sv[9],
        trueTrack: sv[10], verticalRate: sv[11],
        onGround: sv[8], positionSource: sv[16],
      }));
  }

  // 查询特定区域飞机（如中国上空）
  async getStatesInBoundingBox(lamin, lomin, lamax, lomax) {
    const data = await this.request('/states/all', { lamin, lamax, lomin, lomax });
    return data?.states?.map(sv => ({
      icao24: sv[0], callsign: sv[1]?.trim(),
      latitude: sv[6], longitude: sv[5], altitude: sv[7],
    })) || [];
  }
}
```

### 与现有命令的适配性评估

| 现有命令 | 适配情况 | 说明 |
|---------|---------|------|
| `track <fnum>` | ⚠️ 理论可行，实践困难 | 可通过 callsign 过滤全量数据；但中国境内 ADS-B 覆盖稀少，国内航班追踪基本不可用 |
| `info <fnum>` | ⚠️ 部分补充 | 可获取飞机当前位置/高度/速度，但无延误时间、登机口、行李转盘等调度信息 |
| `search` / `comfort` / `transfer` / `weather` | ❌ 无关 | OpenSky 仅提供位置数据，不含时刻表/票价/天气 |

## 两方案联合分析

将两个数据源组合，理论上可以满足：机票价格和时刻表搜索（Google Flights MCP）+ 国际航班实时位置追踪（OpenSky，主要在欧美亚航线上空）。然而对于当前项目最核心的场景——**中国国内航班的实时追踪和详细状态**，两者均无法可靠覆盖。

具体来看，`search` 命令可以迁移到 Google Flights MCP 的 `search_one_way_flights`，体验实际上会有提升（价格信息、直飞/中转筛选），只是无法精确到某特定日期的实际运营状态。`track` 命令可以尝试接入 OpenSky，用来追踪跨境航班（如 PEK-FRA、PVG-LHR 等），但国内段会丢失信号。`info` 命令由于完全依赖按航班号查询实时状态，两个替代数据源均无法满足，仍需依赖 AviationStack 或类似的专业实时航班 API。

## 迁移成本与工作量

若决定迁移，需要重写 `aviationstack-client.js` 底层，新增 `opensky-client.js`（Node.js，处理 OAuth2 Token 刷新）和与 Google Flights MCP 通信的调用逻辑；改造 `search.js` 对接 `search_one_way_flights`；改造 `track.js` 对接 OpenSky `/states/all`（含 IATA→ICAO 呼号映射表）；保持 `info.js`、`comfort.js` 等命令的现有 AviationStack 接口（这些命令需要延误/舱位信息，Google Flights 和 OpenSky 均无法替代）。IATA↔ICAO 航司代码映射需要维护一个本地表（OpenTravelData 的 airlines.csv 可作为数据源）。

## 结论与建议

综合评估，mcp-server-google-flights + OpenSky Network 作为"次推荐方案"的适用场景确实存在，但有明确的边界条件。**如果项目的核心场景是国际长途航班的价格比较和欧美境内飞机追踪**，该组合是合理的免费方案；**如果核心场景是中国国内航班的实时动态**，则该迁移基本没有实用价值。

具体建议如下：第一，可以将 Google Flights MCP 作为 `search` 命令的补充或替换，提供价格信息（这是 AviationStack 免费套餐缺失的能力）；第二，可以将 OpenSky 作为国际航班追踪的辅助数据源，与 AviationStack 并联使用——OpenSky 数据充足时优先展示位置，否则回退到 AviationStack 的状态字段；第三，`info`、`comfort`、`transfer` 命令建议保留 AviationStack 接口，或者考虑升级到付费套餐（$9.99/月起）以获得完整功能；第四，如果完全放弃 AviationStack，可以考虑 **FlightAware AeroAPI**（$0-30/月，按量计费，国内外覆盖完整，支持按航班号查询实时状态）作为功能更完整的替代方案。

## 参考资料

1. [HaroldLeo/google-flights-mcp - GitHub](https://github.com/HaroldLeo/google-flights-mcp)
2. [tistaharahap/google-flights-mcp - PyPI](https://pypi.org/project/google-flights-mcp/)
3. [modellers/mcp-google-travels - GitHub](https://github.com/modellers/mcp-google-travels)
4. [random-robbie/Flight-Search-MCP-Server - GitHub](https://github.com/random-robbie/Flight-Search-MCP-Server)
5. [SerpAPI Google Flights API 文档](https://serpapi.com/google-flights-api)
6. [OpenSky Network REST API 官方文档 v1.4.0](https://openskynetwork.github.io/opensky-api/rest.html)
7. [OpenSky REST API - DeepWiki](https://deepwiki.com/openskynetwork/opensky-api/2-opensky-rest-api)
8. [openskynetwork/opensky-api - GitHub](https://github.com/openskynetwork/opensky-api)
9. [如何获取 OpenSky API 密钥（幂简集成）](https://explinks.com/blog/wa-how-to-get-opensky-air-traffic-data-api-key-step-by-step-guide/)
10. [OpenTravelData - airlines.csv（IATA/ICAO 映射）](https://github.com/opentraveldata/opentraveldata)
11. [google-flights-mcp MCP 市场介绍](http://mcpmarket.cn/server/690cb4fa944e98de23c703d3)
