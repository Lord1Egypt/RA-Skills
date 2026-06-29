---
name: zeecu-device-skill
description: 极酷电动车车辆信息查询，支持查询用户绑定的车辆列表、车辆实时状态、历史骑行轨迹
metadata:
  openclaw:
    requires:
      env:
        - API_KEY
    primaryEnv: API_KEY
---

# 极酷电动车车辆信息查询服务 Skill

极酷电动车车辆信息查询服务向开发者提供完整的车辆信息查询服务，包括车辆列表、实时状态、位置、历史骑行轨迹等信息的查询功能。

## 功能特性

- 查询用户绑定的车辆列表（车型、颜色、车架号、条码号等）
- 查询车辆实时数据（位置、在线状态、速度、电源状态、电量、续航里程、信号强度、里程等）
- 查询车辆历史骑行轨迹（行程列表、里程、时长、速度、起止地址等）
- 轨迹查询默认最近 7 天，按天并发请求，最大支持 30 天
- 支持多设备查询和选择

## 首次配置

首次使用时需要配置 API Key:

1. 在品牌 App 中点击"获取 AI 助手接入密钥"，获取以 `sk_live_` 开头的 API Key
2. 设置环境变量：`export API_KEY=your_key`
3. 或编辑 `config.json` 写入 Key

当用户想要查询极酷电动车车辆信息（如车辆列表、实时位置、在线状态、电量、里程、骑行记录等）时，使用此 skill。

## 触发条件

用户表达了以下意图之一：
- 查询绑定的车辆列表（如"我绑定了哪些车"、"查看我的车辆"）
- 查询车辆实时状态（如"我的车在线吗"、"车辆位置在哪"、"电量多少"）
- 查询车辆详细信息（如"我的车型是什么"、"车架号是多少"）
- 查询骑行历史记录（如"我最近骑了多少次"、"这周骑行记录"、"上周的骑行数据"）
- 查询某段时间的行程（如"最近7天的骑行数据"、"5月1日到5月7日的骑行记录"）

## 执行步骤

#### 第一步：检查 API Key
- 如果用户已经配置好了环境变量 `API_KEY` 或在本地 `config.json` 中提供了 Key，直接使用该 Key 进行后续 API 调用
- 如果用户之前未提供过 Key，**先提示用户提供 API Key**，等待用户回复后再继续
- 如果用户已提供 Key，直接使用

**请求 Key 的回复模板：**

```
🔑 查询车辆信息需要 API Key，请在品牌 App 中点击"获取 AI 助手接入密钥"获取。
```

#### 第二步：获取 API Key
优先读取环境变量 `API_KEY`，其次从本地 `config.json` 读取。也支持在命令行显式传入 `--api-key`。
API Key 以 `sk_live_` 开头，通过请求体参数传递。
参考 `config.example.json` 作为配置样例。

**config.json 示例：**
```json
{
  "apiKey": "sk_live_your_key_here"
}
```

### 第三步：运行查询脚本

#### 查询车辆实时信息

```bash
export API_KEY=sk_live_your_key_here
python3 scripts/query.py \
  --device-name "我的小电驴"
```

#### 查询骑行轨迹

默认查询最近 7 天的骑行轨迹（按天并发查询）：

```bash
export API_KEY=sk_live_your_key_here
python3 scripts/query.py \
  --device-tuid T123456789
```

指定查询最近 N 天（最大 30 天）：

```bash
export API_KEY=sk_live_your_key_here
python3 scripts/query.py \
  --device-tuid T123456789 \
  --days 14
```

仅查询车辆实时数据，不查询轨迹：

```bash
export API_KEY=sk_live_your_key_here
python3 scripts/query.py \
  --device-tuid T123456789 \
  --no-trips
```

显式指定时间范围（秒级 Unix 时间戳）：

```bash
export API_KEY=sk_live_your_key_here
python3 scripts/query.py \
  --device-tuid T123456789 \
  --start-time 1713849600 \
  --end-time 1714454400
```

如果脚本执行返回 API_KEY_INVALID 错误，说明 API Key 无效或已撤销，**提示用户提供有效的 API Key**，等待用户回复后再继续。

如果账户有多个设备且未提供选择，脚本会返回一个列表供用户选择：

```json
{"choose_device": [{"tuid":"T123456789","model":"XX-200"},{"tuid":"T987654321","model":"YY-100"}]}
```

然后使用 `--device-name` 或 `--device-tuid` 重新运行脚本。

**提供无效 key 的回复模版**
```
🔑 提供的 API Key 无效或已撤销，请检查后重新提供。
```

### 第四步：解析输出

#### 车辆实时信息输出：
```json
{
  "tuid": "T123456789",
  "model": "XX-200",
  "color": "珍珠白",
  "frameNo": "VIN123456789012345",
  "barCode": "1234567890123",
  "location": "120.123456,30.123456",
  "locationAddress": "浙江省杭州市西湖区xxx路xxx号",
  "runningStatus": "在线",
  "speed": "0",
  "powerStatus": "OFF",
  "rsrp": "-75",
  "locss": "12",
  "totalMileage": 1234.5,
  "batteryLevel": "85",
  "enduranceMileage": "45.2",
  "lastLocationTime": "1713849600000"
}
```

#### 骑行轨迹输出：
```json
{
  "tuid": "T123456789",
  "model": "XX-200",
  "trips": [
    {
      "tripId": "trip_7cb1cc64f0d949d8bcb969370884fe6e",
      "startTime": 1782208290452,
      "endTime": 1782208298492,
      "mileage": "50.0",
      "durationValue": "0.1",
      "durationUnit": "min",
      "avgSpeed": "30.0",
      "maxSpeed": "30.0",
      "firstAddress": "上海市黄浦区南京东路街道延安高架路凯迪拉克·上海音乐厅",
      "lastAddress": "上海市黄浦区外滩街道河南中路南京商务楼"
    }
  ],
  "tripCount": 1
}
```

## 配置管理

配置文件位于 `config.json`，包含以下内容：

```json
{
  "apiKey": "sk_live_your_key_here"
}
```

设置 Key 的方式：

1. **环境变量**：`export API_KEY=sk_live_your_key`
2. **手动编辑**：直接编辑 `config.json` 文件
3. **命令行参数**：`--api-key sk_live_your_key`

## 资源

### scripts/
- `query.py` — 查询电动车信息脚本

### references/
- `api-spec.md` — API 规范文档