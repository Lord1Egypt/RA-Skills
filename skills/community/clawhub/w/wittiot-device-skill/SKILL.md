---
name: wittiot-device-skill
description: WittIoT气象站数据查询，支持WittStation系列气象站，提供实时温湿度、气压、光照、风速风向、降雨量等传感器数据查询，以及24小时/7天/30天历史趋势查询。也支持通过设备短码（shortcode）免登录查询公开气象站数据。
metadata:
  openclaw:
    requires:
      env:
        - WITTIOT_API_KEY
    primaryEnv: WITTIOT_API_KEY
---

# WittIoT 气象站数据查询 Skill

WittIoT 气象站数据查询服务，支持查询绑定在你账户下的 WittStation 气象站的实时与历史传感器数据，以及通过设备短码查询他人公开气象站的实时数据（无需登录）。

## 功能特性

- 实时气象数据查询：温度、湿度、气压、光照、风速、阵风、风向、降雨量
- 历史趋势查询：24小时 / 7天 / 30天历史数据
- 设备列表查询：列出账户下所有绑定的气象站及其在线状态
- 公开短码查询：通过6位短码免登录查询他人公开气象站实时数据（无需 API Key）

## 首次配置

首次使用时需要配置 WittIoT API Key：

1. 访问 https://wittiot.com/index/apikey 创建 API Key（格式：`witt_sk_xxxx`）
2. 设置环境变量：`export WITTIOT_API_KEY=witt_sk_your_key_here`
3. 或运行时自动提示输入并保存到本地 `config.json`

> 短码查询功能（`--action shortcode`）无需 API Key，任何人都可以直接使用。

## 触发条件

当用户表达了以下意图之一时，使用此 Skill：

- 查询自己气象站的实时天气（如"我的气象站现在温度多少"、"家里风速是多少"、"雨量怎么样"）
- 查询气象站历史趋势（如"昨天24小时气温走势"、"上周的降雨量记录"）
- 列出名下设备（如"我绑定了哪些气象站"、"查看我的WittStation设备列表"）
- 查询他人公开气象站（如"查一下短码 ABC123 的天气数据"、"这台气象站现在的数据是什么"）

---

## 执行步骤

### 第一步：判断查询类型

根据用户意图判断操作类型：

| 用户意图 | 操作（--action） | 是否需要 API Key |
|---------|----------------|----------------|
| 查询实时天气 | `realtime` | ✅ 需要 |
| 查询历史数据 | `history` | ✅ 需要 |
| 列出设备 | `devices` | ✅ 需要 |
| 通过短码查询公开数据 | `shortcode` | ❌ 不需要 |

### 第二步：检查 API Key（shortcode 操作跳过此步）

- 如果用户已配置环境变量 `WITTIOT_API_KEY` 或本地 `config.json` 中有 `apiKey`，直接使用
- 如果未配置，**先提示用户提供 API Key**，等待用户回复后继续

**请求 API Key 的回复模板：**

```
🔑 查询 WittIoT 气象站数据需要 API Key，请提供你的 Key。

（在 https://wittiot.com/index/apikey 可以免费创建，格式为 witt_sk_xxxx）
```

### 第三步：运行查询脚本

#### 查询实时数据
```bash
export WITTIOT_API_KEY=witt_sk_your_key_here

# 自动选择唯一设备（账户只有1台时）
python3 scripts/wittiot_query.py --action realtime

# 指定设备名称
python3 scripts/wittiot_query.py --action realtime --device-name "Backyard Station"

# 指定设备 ID
python3 scripts/wittiot_query.py --action realtime --device-id 1
```

#### 查询历史数据
```bash
# 24小时历史（默认）
python3 scripts/wittiot_query.py --action history --device-name "Backyard Station"

# 7天历史
python3 scripts/wittiot_query.py --action history --device-name "Backyard Station" --range 7d

# 30天历史
python3 scripts/wittiot_query.py --action history --device-id 1 --range 30d
```

#### 列出设备
```bash
python3 scripts/wittiot_query.py --action devices
```

#### 通过短码查询公开气象站（无需 API Key）
```bash
python3 scripts/wittiot_query.py --action shortcode --code ABC123
```

### 第四步：处理脚本输出

#### 设备列表输出（--action devices）

```json
{
  "devices": [
    {
      "id": 1,
      "name": "Backyard Station",
      "model": "WS6900",
      "sn": "WS6900-000001",
      "online": true,
      "visibility": "public"
    }
  ]
}
```

以友好的方式列出设备，标注在线/离线状态和公开/私有模式。

#### 实时数据输出（--action realtime）

```json
{
  "device_id": 1,
  "device_name": "Backyard Station",
  "online": true,
  "sensors": {
    "temperature": "23.5 °C",
    "humidity": "68.2 %",
    "pressure": "1013.2 hPa",
    "light": "45.3 Klux",
    "wind_speed": "3.2 m/s",
    "wind_gust": "5.1 m/s",
    "wind_direction": "270° (W)",
    "rainfall": "0.0 mm"
  },
  "_raw": { ... }
}
```

以自然语言向用户汇报数据，例如：
> 🌡 你的「Backyard Station」气象站当前数据（在线）：温度 **23.5°C**，湿度 **68%**，气压 **1013.2 hPa**，西风 **3.2 m/s**，无降雨。

#### 多设备选择输出

当账户有多台设备且用户未指定时，脚本返回：

```json
{"choose_device": [{"id": 1, "name": "Backyard Station"}, {"id": 2, "name": "Rooftop Station"}]}
```

此时应**提示用户选择设备**，然后用 `--device-name` 或 `--device-id` 重新运行。

**提示用户选择设备的回复模板：**

```
📡 你有以下气象站，请告诉我查询哪一台：
1. Backyard Station
2. Rooftop Station
```

#### 历史数据输出（--action history）

```json
{
  "device_id": 1,
  "range": "24h",
  "count": 144,
  "data": [
    {"timestamp": 1743000000, "temperature": 22.1, "humidity": 65.0},
    ...
  ]
}
```

对历史数据进行趋势分析：最高/最低/平均值，并以自然语言描述趋势。

#### 短码查询输出（--action shortcode）

```json
{
  "shortcode": "ABC123",
  "device_name": "Community Weather Station",
  "model": "WS6900",
  "online": true,
  "sensors": {
    "temperature": "21.0 °C",
    "humidity": "72.0 %"
  }
}
```

---

### 错误码与消息处理

当脚本返回错误时，使用以下处理方式：

| 情况 | 处理 |
|------|------|
| `error: Missing API key` | 提示用户提供 API Key（见第二步模板） |
| `error: HTTP 401` | 提示 API Key 无效，请重新获取 |
| `error: No devices found` | 提示用户尚未绑定气象站，引导访问 https://wittiot.com/index/dashboard |
| `error: Device 'xxx' not found` + `available` 列表 | 提示可用设备名称，请用户重新选择 |
| `error: Shortcode not found or device is private` | 提示短码不存在或设备未设为公开 |
| `choose_device` | 列出设备供用户选择（见第四步） |
| 设备 `online: false` | 告知用户设备当前离线，数据可能不是最新 |

**401 固定回复文案：**

```
🔑 API Key 无效或已过期，请访问 https://wittiot.com/index/apikey 重新生成后提供。
```

---

## 配置管理

配置文件位于 `config.json`（参考 `config.example.json`）：

```json
{
  "apiKey": "witt_sk_your_api_key_here"
}
```

设置 Key 的方式（优先级从高到低）：

1. **命令行参数**：`--api-key witt_sk_xxx`
2. **环境变量**：`export WITTIOT_API_KEY=witt_sk_xxx`
3. **配置文件**：`config.json` 中的 `apiKey` 字段

---

## 资源

### scripts/
- `wittiot_query.py` — WittIoT 气象站数据查询脚本（Python 3，无外部依赖）

### references/
- `api-spec.md` — WittIoT API 端点规范与响应结构说明
