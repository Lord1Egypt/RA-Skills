# API 调用示例

_同程程心 API 调用参考_

---

本技能**仅**通过 `scripts/` 下各 `*-query.js` 调用程心资源接口;须按 SKILL.md 将用户意图映射到对应脚本并传入结构化参数(及 `--channel` / `--surface`)。

## 📋 通用说明

### 基础调用格式

```bash
node scripts/<脚本名>.js [参数] --channel <渠道> --surface <界面>
```

### 通用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--channel <渠道>` | 通信渠道 | `webchat`、`wechat`、`app` |
| `--surface <界面>` | 交互界面 | `webchat`、`mobile`、`desktop`、`card` |

### 配置方式（优先级：环境变量 > config.json）

- **环境变量**: `CHENGXIN_API_KEY`
- **本地文件**: 创建 `config.json`（见 `config.example.json`）

---

## ✈️ 机票查询 (flight-query.js)

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |
| 航班号 | `--flight-number "CA1234"` | 精确查航班 |
| 出发地 + 特价 | `--departure "北京" --low-price` | 多地低价推荐 |
| 出发地 + 目的地 + 特价 | `--departure "上海" --destination "北京" --low-price` | 指定航线特价 |

### 调用示例

```bash
# 北京到上海，明天的机票
node scripts/flight-query.js \
  --departure "北京" \
  --destination "上海" \
  --extra "明天" \
  --channel webchat \
  --surface webchat

# 查询特定航班
node scripts/flight-query.js \
  --flight-number "CA1234" \
  --channel webchat \
  --surface webchat

# 上海到北京的特价机票
node scripts/flight-query.js \
  --departure "上海" \
  --destination "北京" \
  --low-price \
  --channel webchat \
  --surface webchat

# 从北京出发的特价推荐（未指定目的地）
node scripts/flight-query.js \
  --departure "北京" \
  --low-price \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "flightDataList": [
      {
        "desc": "北京 → 上海 2026-04-21",
        "supplementTrafficType": "pre",
        "supplementTrafficList": [
          {
            "segmentType": "TRAIN",
            "trafficNo": "G1234",
            "depStationName": "苏州北",
            "depStationCode": "OHH",
            "arrStationName": "上海虹桥",
            "arrStationCode": "AOH",
            "depDateTime": "2026-04-21 07:00",
            "arrDateTime": "2026-04-21 07:30",
            "depDate": "2026-04-21",
            "depTime": "07:00",
            "arrDate": "2026-04-21",
            "arrTime": "07:30",
            "runTime": "30分",
            "price": "39.5",
            "ticketList": [
              { "ticketType": "二等座", "ticketPrice": "39.5", "ticketLeft": "21" },
              { "ticketType": "一等座", "ticketPrice": "64.5", "ticketLeft": "15" }
            ],
            "tripType": "DIRECT"
          }
        ],
        "flightList": [
          {
            "flightNo": "MF8561",
            "airlineName": "厦门航空",
            "depAirportName": "北京大兴国际机场",
            "depAirportTerminal": "",
            "arrAirportName": "上海浦东国际机场",
            "arrAirportTerminal": "T2",
            "depDate": "2026-04-21",
            "depTime": "07:50",
            "arrDate": "2026-04-21",
            "arrTime": "09:45",
            "daySpan": "0",
            "runTime": "1时55分",
            "price": "327",
            "discount": null,
            "originPrice": null,
            "pcRedirectUrl": "https://...",
            "clawRedirectUrl": "https://..."
          }
        ]
      }
    ]
  }
}
```

**`supplementTrafficList` 补偿交通字段说明**：

| 字段 | 说明 |
|------|------|
| `supplementTrafficType` | 补偿类型：`"pre"` = 出发地补偿（用户城市→机场城市），`"suffix"` = 目的地补偿（机场城市→用户目的地） |
| `segmentType` | 交通类型：`"TRAIN"` = 火车，`"BUS"` = 汽车 |
| `trafficNo` | 车次号 |
| `depStationName` / `arrStationName` | 出发/到达站名 |
| `depDateTime` / `arrDateTime` | 完整日期时间 |
| `depTime` / `arrTime` | 出发/到达时间 |
| `runTime` | 运行时长 |
| `price` | 最低价格 |
| `ticketList` | 席别票价列表（与火车票结构一致） |
| `tripType` | 行程类型：`"DIRECT"` = 直达 |

---

## 🚂 火车票查询 (train-query.js)

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |
| 车次号 | `--train-number "G1234"` | 精确查车次 |
| 出发站 + 到达站 | `--departure-station "北京南站" --arrival-station "上海虹桥站"` | 精确站点查询 |

### 调用示例

```bash
# 北京到上海，明天的高铁
node scripts/train-query.js \
  --departure "北京" \
  --destination "上海" \
  --extra "明天 高铁" \
  --channel webchat \
  --surface webchat

# 查询特定车次
node scripts/train-query.js \
  --train-number "G1234" \
  --channel webchat \
  --surface webchat

# 站到站精确查询
node scripts/train-query.js \
  --departure-station "北京南站" \
  --arrival-station "上海虹桥站" \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "trainDataList": [
      {
        "desc": "北京 → 上海 2024-04-20",
        "trainList": [
          {
            "trainNo": "G1234",
            "trainType": "GD",
            "depStationName": "北京南站",
            "arrStationName": "上海虹桥站",
            "depTime": "09:00",
            "arrTime": "13:28",
            "runTime": "4小时28分",
            "ticketList": [
              {
                "ticketType": "二等座",
                "ticketPrice": 553
              },
              {
                "ticketType": "一等座",
                "ticketPrice": 933
              }
            ],
            "pcRedirectUrl": "https://...",
            "clawRedirectUrl": "https://..."
          }
        ]
      }
    ]
  }
}
```

---

## 🚌 长途汽车查询 (bus-query.js)

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |
| 出发站 + 到达站 | `--departure-station "北京六里桥客运站" --arrival-station "上海长途汽车客运站"` | 精确站点查询 |

### 调用示例

```bash
# 北京到上海，明天的长途汽车
node scripts/bus-query.js \
  --departure "北京" \
  --destination "上海" \
  --extra "明天" \
  --channel webchat \
  --surface webchat

# 站到站精确查询
node scripts/bus-query.js \
  --departure-station "北京六里桥客运站" \
  --arrival-station "上海长途汽车客运站" \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "busDataList": [
      {
        "desc": "苏州 → 常熟 2026-04-21",
        "busList": [
          {
            "coachNo": "SZ-CSB0001",
            "coachType": "客车",
            "depCityName": "苏州",
            "arrCityName": "常熟",
            "depStationName": "苏州北广场汽车客运站",
            "arrStationName": "常熟南门汽车站",
            "depTime": "06:15",
            "arrTime": "07:45",
            "runTimeMinutes": 90,
            "runTimeDesc": "约1.5小时",
            "price": "14.90",
            "pcRedirectUrl": "https://...",
            "clawRedirectUrl": "https://..."
          }
        ]
      }
    ]
  }
}
```

---

## 🏨 酒店查询 (hotel-query.js)

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 目的地城市 | `--destination "上海"` | 按城市查询 |
| 目的地 + 位置偏好 | `--destination "上海" --extra "外滩附近"` | 指定区域 |
| 目的地 + 入住日期 | `--destination "上海" --extra "明天入住"` | 指定日期 |

### 调用示例

```bash
# 上海酒店，明天入住
node scripts/hotel-query.js \
  --destination "上海" \
  --extra "明天入住" \
  --channel webchat \
  --surface webchat

# 上海外滩附近的酒店
node scripts/hotel-query.js \
  --destination "上海" \
  --extra "外滩附近" \
  --channel webchat \
  --surface webchat

# 简单查询（仅目的地）
node scripts/hotel-query.js \
  --destination "上海" \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "hotelDataList": [
      {
        "desc": "上海酒店推荐",
        "hotelList": [
          {
            "name": "上海虹桥新华联索菲特大酒店",
            "price": "1512",
            "star": "豪华型",
            "score": "4.8",
            "commentNum": "7493",
            "describe": "交通便利，设施齐全，服务优质。",
            "address": "泰虹路666号",
            "pcRedirectUrl": "https://...",
            "clawRedirectUrl": "https://..."
          }
        ]
      }
    ]
  }
}
```

---

## 🏞️ 景点查询 (scenery-query.js)

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 目的地城市 | `--destination "杭州"` | 按城市查询 |
| 目的地 + 特色 | `--destination "杭州" --extra "适合亲子"` | 指定特色 |
| 目的地 + 类型 | `--destination "苏州" --extra "园林 5A 景区"` | 指定类型 |

### 调用示例

```bash
# 杭州景点，适合亲子
node scripts/scenery-query.js \
  --destination "杭州" \
  --extra "适合亲子" \
  --channel webchat \
  --surface webchat

# 苏州园林景点
node scripts/scenery-query.js \
  --destination "苏州" \
  --extra "园林" \
  --channel webchat \
  --surface webchat

# 简单查询（仅目的地）
node scripts/scenery-query.js \
  --destination "杭州" \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "sceneryDataList": [
      {
        "desc": "杭州景区推荐",
        "sceneryList": [
          {
            "name": "杭州宋城",
            "cityName": "杭州",
            "star": "4A",
            "score": "4.8",
            "commentNum": "14186",
            "price": "260",
            "describe": "世界三大名秀之一",
            "address": "杭州市西湖区之江路148号",
            "theme": "演出赛事",
            "pcRedirectUrl": "https://...",
            "clawRedirectUrl": "https://..."
          }
        ]
      }
    ]
  }
}
```

---

## 🧳 旅行度假查询 (travel-query.js)

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 目的地 | `--destination "三亚"` | 按城市/地区查询 |
| 出发地 + 目的地 | `--departure "苏州" --destination "杭州"` | 含往返交通规划 |
| 出发地 + 目的地 + 天数 | `--departure "苏州" --destination "杭州" --extra "3天2晚"` | 含行程规划 ⭐ |
| 目的地 + 天数 + 类型 | `--destination "云南" --extra "6天5晚 自由行"` | 指定行程 |

### 调用示例

```bash
# 经典场景：从某地出发到某地玩几天（推荐）
node scripts/travel-query.js \
  --departure "苏州" \
  --destination "杭州" \
  --extra "3天2晚" \
  --channel webchat \
  --surface webchat

# 仅目的地查询
node scripts/travel-query.js \
  --destination "三亚" \
  --channel webchat \
  --surface webchat

# 带假期条件
node scripts/travel-query.js \
  --destination "三亚" \
  --extra "五一假期" \
  --channel webchat \
  --surface webchat

# 指定天数和类型
node scripts/travel-query.js \
  --destination "云南" \
  --extra "6天5晚 自由行" \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "trainDataList": [
      {
        "desc": "苏州 → 杭州 推荐火车",
        "trainList": [
          { "trainNo": "G7589", "depTime": "09:00", "arrTime": "09:45" }
        ]
      }
    ],
    "hotelDataList": [
      {
        "hotelList": [
          { "hotelName": "杭州西湖大酒店", "price": 580 }
        ]
      }
    ],
    "sceneryDataList": [
      {
        "sceneryList": [
          { "name": "西湖", "price": 0 }
        ]
      }
    ],
    "tripDataList": [
      {
        "desc": "杭州3日游产品",
        "tripList": [
          {
            "name": "3天2晚·宿5钻·杭州+乌镇西栅+西塘古镇+灵隐飞来峰+西湖跟团游",
            "price": "729",
            "score": "0.9296",
            "commentNum": "554",
            "labelList": ["成团保障", "品质游", "古镇古村"],
            "destList": ["杭州", "嘉兴", "桐乡"],
            "pcRedirectUrl": "",
            "clawRedirectUrl": "https://..."
          }
        ]
      }
    ],
    "tripPlanDataList": [
      {
        "totalDays": "3",
        "hotelNights": "2",
        "foods": "杭州市美食有...",
        "sceneryCount": "6",
        "planList": [
          {
            "index": "1",
            "summary": "千岛湖景区",
            "cityNameList": ["杭州"],
            "activitiyList": [
              {
                "name": "千岛湖景区",
                "introduction": "徜徉在星罗密布的岛屿中",
                "price": "45.5",
                "star": "5A级景区",
                "score": "4.6",
                "commentNum": "13614",
                "openTime": "08:00-15:00",
                "playTime": "半天-1天",
                "theme": "海滨岛屿",
                "pcRedirectUrl": "https://...",
                "clawRedirectUrl": "https://..."
              }
            ]
          }
        ]
      }
    ],
    "ugcDataList": [
      {
        "ugcList": [
          {
            "name": "杭州三日游攻略",
            "nickName": "旅行达人",
            "redirectUrl": "https://..."
          }
        ]
      }
    ]
  }
}
```

---

## 🚗 智能交通查询 (traffic-query.js)

> 🚨 **使用场景**: 用户**未明确指定交通方式**时使用！

### 参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |

### 调用示例

```bash
# 北京到上海，智能推荐交通方式
node scripts/traffic-query.js \
  --departure "北京" \
  --destination "上海" \
  --channel webchat \
  --surface webchat

# 明天出发
node scripts/traffic-query.js \
  --departure "北京" \
  --destination "上海" \
  --extra "明天" \
  --channel webchat \
  --surface webchat

# 包含自驾偏好
node scripts/traffic-query.js \
  --departure "苏州" \
  --destination "南京" \
  --extra "自驾" \
  --channel webchat \
  --surface webchat
```

### 响应数据结构

```json
{
  "code": "0",
  "data": {
    "trainDataList": [
      {
        "desc": "北京 → 上海 火车推荐",
        "trainList": [
          { "trainNo": "G123", "depTime": "09:00", "price": 553 }
        ]
      }
    ],
    "flightDataList": [
      {
        "desc": "北京 → 上海 航班推荐",
        "flightList": [
          { "flightNo": "CA1234", "depTime": "08:00", "price": 850 }
        ]
      }
    ],
    "busDataList": [
      {
        "desc": "北京 → 上海 汽车推荐",
        "busList": [
          { "coachNo": "K1234", "depTime": "08:30", "price": 350 }
        ]
      }
    ]
  }
}
```

---

## 📤 响应结构说明

### 成功响应

```json
{
  "code": "0",
  "data": {
    "xxxDataList": [
      {
        "desc": "描述信息",
        "xxxList": [
          {
            "具体资源对象": "..."
          }
        ]
      }
    ]
  }
}
```

**说明**:
- `code`: `"0"` 表示成功
- `data`: 业务数据对象（部分接口可能返回双层嵌套 `{ code, data: { code, data: {...} } }`，代码已做兼容解包）
- `xxxDataList`: 各类资源列表（如 `flightDataList`、`trainDataList` 等）
- `xxxList`: 具体资源列表（如 `flightList`、`trainList` 等）
- `desc`: 描述信息（可选）

### 无结果

```json
{
  "code": "1",
  "message": "无结果"
}
```

### 错误响应

```json
{
  "code": "3",
  "message": "鉴权失败"
}
```

---

## ⚠️ 错误码处理

| Code | 含义 | 处理方式 |
|------|------|---------|
| `0` | 成功 | 正常解析并输出结果 |
| `1` | 无结果 | 告知用户未找到相关资源，建议调整搜索词 |
| `3` | 鉴权失败 | 检查 API Key 是否配置正确 |

详细错误处理指南见 `references/error-handling.md`

---

_同程旅行 · 让旅行更简单，更快乐_
