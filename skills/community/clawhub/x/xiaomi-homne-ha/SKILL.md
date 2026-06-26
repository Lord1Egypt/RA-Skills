````skill
---
name: xiaomi-home-ha
description: "Control Xiaomi/Mi Home smart devices via Home Assistant REST API (curl+jq). Use for lights, switches, sensors, AC, fans, media players, scenes — query state or call any HA service. 通过 HA REST API 控制小米智能家居设备。"
homepage: https://www.home-assistant.io/integrations/rest/
metadata: { "openclaw": { "emoji": "🏠", "requires": { "bins": ["curl", "jq"], "env": ["HA_URL", "HA_TOKEN"] }, "primaryEnv": "HA_TOKEN" } }
---

# 小米智能家居 (Xiao Mi Home for HA)

通过 Home Assistant REST API，用自然语言控制任意小米/米家智能设备。  
Control any Xiaomi/Mi Home smart device via Home Assistant REST API using natural language.

---

## 适用场景 / When to Use

✅ **适用 / USE when:**

- 控制灯光（开关、调光、色温、RGB）/ Control lights (on/off, brightness, color temp, RGB)
- 控制开关、插座、风扇 / Control switches, smart plugs, fans
- 控制空调、温控器 / Control air conditioners, thermostats
- 控制小米音箱、媒体播放器 / Control Xiaomi speakers, media players
- 查询任意设备状态 / Query any device state
- 读取温湿度、空气质量等传感器值 / Read temperature, humidity, air quality sensors
- 调用任意 HA 服务（脚本、场景、自动化）/ Call any HA service (scripts, scenes, automations)

❌ **不适用 / DON'T use when:**

- 未接入 Home Assistant 的设备 / Devices not connected to Home Assistant
- 纯云端米家 App（无本地 HA 实例）/ Cloud-only Mi Home App without local HA
- 非智能家居相关的任务 / Non-smart-home tasks

---

## 前置配置 / Setup

### 1. 配置项 / Required Config

| 变量 | 说明 | 是否必填 |
|------|------|----------|
| `HA_URL` | HA 地址，如 `http://192.168.31.202:8123` | ✅ 必填 |
| `HA_TOKEN` | 长期访问令牌 (Long-Lived Access Token) | ✅ 必填 |
| `HA_DEFAULT_ENTITY` | 未指定实体时的默认值，如 `light.bed_lamp` | 可选 |

### 2. 安装依赖 / Install Dependencies

本 skill 需要 `curl` 和 `jq`。`curl` 通常已预装；`jq` 按系统安装：

```bash
# Ubuntu / Debian
sudo apt-get install -y jq

# macOS
brew install jq

# 无 sudo 备用（需要 Node.js）
npm i -g node-jq   # 安装后 jq 命令即可用
```

验证: `jq --version`

### 3. 获取 Token / How to Get Token

> HA Web → 右下角头像 → **安全** → **长期访问令牌** → **创建令牌** → 复制  
> HA UI → Profile → Security → Long-Lived Access Tokens → Create Token

### 4. 写入配置（三种方式）/ Configure (3 ways)

**方式 A — 飞书/客户端（最简，无需开终端）**

在飞书对话中直接发给 AI：

> 帮我配置小米智能家居 skill，HA 地址 http://192.168.31.202:8123，token 是 eyJhbGc...

AI 会自动运行 `openclaw config set` 完成写入。

**方式 B — 命令行 / CLI**

```bash
openclaw config set 'skills."xiaomi-home-ha".env.HA_URL' "http://192.168.31.202:8123"
openclaw config set 'skills."xiaomi-home-ha".env.HA_TOKEN' "eyJhbGc..."
# 可选 / optional
openclaw config set 'skills."xiaomi-home-ha".env.HA_DEFAULT_ENTITY' "light.bed_lamp"
```

**方式 C — 直接编辑 `~/.openclaw/openclaw.json`**

```json5
{
  "skills": {
    "entries": {
      "xiaomi-home-ha": {
        "env": {
          "HA_URL": "http://192.168.31.202:8123",
          "HA_TOKEN": "eyJhbGc...",
          "HA_DEFAULT_ENTITY": "light.bed_lamp"
        }
      }
    }
  }
}
```

> 配置写入后重新开启一个会话即生效（OpenClaw 每次会话启动时注入 env）。  
> Changes take effect on the next new session.

### 5. 验证连接 / Verify Connection

```bash
curl -sf "${HA_URL}/api/" \
  -H "Authorization: Bearer ${HA_TOKEN}"
```

预期输出 / Expected output:
```json
{ "message": "API running." }
```

---

## 核心 API 模型 / Core API Pattern

所有操作基于两个通用端点，AI 根据意图自动填充变量：  
All operations use two universal endpoints; the AI fills in variables based on intent:

### 查询状态 / Query State

```bash
# 查询所有实体 / Query all entities
GET ${HA_URL}/api/states

# 查询单个实体 / Query single entity
GET ${HA_URL}/api/states/${ENTITY_ID}
```

### 执行操作 / Execute Action

```bash
# 通用操作模板 / Universal action template
POST ${HA_URL}/api/services/${DOMAIN}/${SERVICE}
Body: { "entity_id": "${ENTITY_ID}", ...service_data }
```

**AI 工作流 / AI Workflow:**
1. 从 `entity_id` 拆出 `domain`（如 `light.bed_lamp` → `domain=light`）
2. 根据用户意图选择 `service`（如 "开" → `turn_on`，"暂停" → `media_pause`）
3. 构造 `service_data`（可选附加参数，如亮度、温度等）

---

## 查询设备 / Query Entities

### 列出所有设备 / List All Entities

```bash
# 查询所有受控实体（含状态）/ All entities with state
curl -sf "${HA_URL}/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  | jq '[.[] | {entity_id, state, name: .attributes.friendly_name}]'
```

### 按前缀过滤域 / Filter by Domain Prefix

```bash
# 变量：DOMAIN_PREFIX = light / switch / sensor / media_player / climate / fan 等
# Variable: DOMAIN_PREFIX = light / switch / sensor / media_player / climate / fan etc.
DOMAIN_PREFIX="light"

curl -sf "${HA_URL}/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  | jq --arg prefix "${DOMAIN_PREFIX}." \
    '[.[] | select(.entity_id | startswith($prefix))
      | {entity_id, state,
         name: .attributes.friendly_name,
         extra: .attributes}]'
```

### 按区域过滤 / Filter by Area

```bash
AREA_KEYWORD="bedroom"   # 中文也可以 / Chinese also works, e.g. "卧室"

curl -sf "${HA_URL}/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  | jq --arg area "${AREA_KEYWORD}" \
    '[.[] | select(
        (.attributes.friendly_name // "" | ascii_downcase | contains($area)) or
        (.attributes.area_id // "" | ascii_downcase | contains($area))
      ) | {entity_id, state, name: .attributes.friendly_name}]'
```

### 查询单个实体完整状态 / Full State for One Entity

```bash
ENTITY_ID="light.bed_lamp"

curl -sf "${HA_URL}/api/states/${ENTITY_ID}" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  | jq '{
      entity_id,
      state,
      name: .attributes.friendly_name,
      attributes: .attributes,
      last_updated
    }'
```

---

## 控制设备 / Control Devices

所有控制操作共用一套模板，只需替换 `DOMAIN`、`SERVICE`、`ENTITY_ID`、`SERVICE_DATA`。  
All control operations share one template — just swap `DOMAIN`, `SERVICE`, `ENTITY_ID`, `SERVICE_DATA`.

### 通用操作模板 / Universal Control Template

```bash
# 必填变量 / Required variables
ENTITY_ID="light.bed_lamp"          # 实体 ID / entity ID
DOMAIN="${ENTITY_ID%%.*}"           # 自动从 entity_id 拆出 / auto-extracted from entity_id
SERVICE="turn_on"                   # HA 服务名 / HA service name
SERVICE_DATA='{"transition": 0.5}'  # 附加参数（可为空对象）/ extra params (can be {})

curl -sf -X POST "${HA_URL}/api/services/${DOMAIN}/${SERVICE}" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
        --arg eid "${ENTITY_ID}" \
        --argjson extra "${SERVICE_DATA}" \
        '{entity_id: $eid} + $extra')"
```

### 开 / 关 / 切换 — Turn On / Off / Toggle

```bash
# 任意实体均适用 / Works for any entity
ENTITY_ID="switch.fan"
curl -sf -X POST "${HA_URL}/api/services/${ENTITY_ID%%.*}/turn_on" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"entity_id\": \"${ENTITY_ID}\"}"

# 关闭 / Turn off
curl -sf -X POST "${HA_URL}/api/services/${ENTITY_ID%%.*}/turn_off" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"entity_id\": \"${ENTITY_ID}\"}"

# 切换 / Toggle
curl -sf -X POST "${HA_URL}/api/services/${ENTITY_ID%%.*}/toggle" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"entity_id\": \"${ENTITY_ID}\"}"
```

### 带附加参数的服务调用 / Service Call with Extra Parameters

```bash
# 示例 1：调节灯光亮度至 40% + 色温 3000K / Light: brightness 40% + color temp 3000K
ENTITY_ID="light.ceiling"
curl -sf -X POST "${HA_URL}/api/services/light/turn_on" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
        \"entity_id\": \"${ENTITY_ID}\",
        \"brightness_pct\": 40,
        \"color_temp_kelvin\": 3000,
        \"transition\": 0.5
      }"

# 示例 2：空调设置温度 / Climate: set temperature
ENTITY_ID="climate.bedroom_ac"
curl -sf -X POST "${HA_URL}/api/services/climate/set_temperature" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
        \"entity_id\": \"${ENTITY_ID}\",
        \"temperature\": 26,
        \"hvac_mode\": \"cool\"
      }"

# 示例 3：媒体播放器音量 / Media player: set volume
ENTITY_ID="media_player.xiaomi_speaker"
curl -sf -X POST "${HA_URL}/api/services/media_player/volume_set" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
        \"entity_id\": \"${ENTITY_ID}\",
        \"volume_level\": 0.5
      }"

# 示例 4：执行场景 / Activate a scene
ENTITY_ID="scene.bedtime_mode"
curl -sf -X POST "${HA_URL}/api/services/scene/turn_on" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"entity_id\": \"${ENTITY_ID}\"}"
```

### 操作后读取最新状态 / Read State After Action

```bash
# 建议操作后等待 600ms 再查询（HA 状态有短暂延迟）
# Wait 600ms after action before querying (HA state has brief delay)
sleep 0.6
curl -sf "${HA_URL}/api/states/${ENTITY_ID}" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  | jq '{state, name: .attributes.friendly_name, attributes: .attributes}'
```

---

## 常用 service_data 参数速查 / Common service_data Parameters

以下参数按**参数类型**而非设备类型分组，可组合使用：  
Parameters grouped by **type** (not device), combinable as needed:

| 参数 / Parameter | 适用域 / Domain | 说明 / Description | 示例值 / Example |
|---|---|---|---|
| `brightness_pct` | `light` | 亮度百分比 / Brightness % | `0` – `100` |
| `color_temp_kelvin` | `light` | 色温 Kelvin / Color temp K | `2700` (暖) ~ `6500` (冷) |
| `rgb_color` | `light` | RGB 颜色 / RGB color | `[255, 100, 0]` |
| `transition` | `light` | 过渡秒数 / Fade seconds | `0.5` |
| `temperature` | `climate` | 目标温度℃ / Target temp °C | `26` |
| `hvac_mode` | `climate` | 运行模式 / HVAC mode | `"cool"` `"heat"` `"auto"` `"off"` |
| `volume_level` | `media_player` | 音量 0-1 / Volume 0-1 | `0.5` |
| `percentage` | `fan` | 风速百分比 / Fan speed % | `0` – `100` |
| `media_content_id` | `media_player` | 播放内容 ID / Content ID | `"spotify:..."` |
| `media_content_type` | `media_player` | 内容类型 / Content type | `"music"` |

---

## 快捷场景 / Quick Recipes

### 睡前场景 / Bedtime Mode

```bash
# 所有灯调至 10% 暖黄 / All lights dim warm
for entity in light.bedroom light.corridor; do
  curl -sf -X POST "${HA_URL}/api/services/light/turn_on" \
    -H "Authorization: Bearer ${HA_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"entity_id\": \"${entity}\", \"brightness_pct\": 10, \"color_temp_kelvin\": 2700}" &
done
wait
```

### 读取室内环境 / Read Indoor Environment

```bash
# 一次性读取温湿度等所有 sensor 值
curl -sf "${HA_URL}/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  | jq '[.[] | select(.entity_id | startswith("sensor."))
          | select(.attributes.device_class // "" | IN("temperature","humidity","pm25","co2"))
          | {
              entity_id,
              name: .attributes.friendly_name,
              value: .state,
              unit: .attributes.unit_of_measurement,
              type: .attributes.device_class
            }]'
```

### 批量关闭所有设备 / Turn Off All Devices

```bash
# 关闭所有灯和开关 / Turn off all lights and switches
for domain in light switch; do
  curl -sf "${HA_URL}/api/states" \
    -H "Authorization: Bearer ${HA_TOKEN}" \
    | jq -r --arg d "${domain}." '[.[] | select(.entity_id | startswith($d)) | .entity_id] | .[]' \
    | while read -r eid; do
        curl -sf -X POST "${HA_URL}/api/services/${domain}/turn_off" \
          -H "Authorization: Bearer ${HA_TOKEN}" \
          -H "Content-Type: application/json" \
          -d "{\"entity_id\": \"${eid}\"}" > /dev/null
        echo "✓ off: ${eid}"
      done
done
```

---

## 注意事项 / Notes

- **状态延迟**：操作后建议 `sleep 0.6` 再查询，HA 需时同步设备状态  
  **State latency**: Wait `sleep 0.6` after actions before re-querying; HA needs time to sync

- **Token 安全**：`HA_TOKEN` 应存在 shell profile 而非明文传入命令  
  **Token security**: Keep `HA_TOKEN` in shell profile, not hardcoded in commands

- **过渡动画**：`"transition": 0.5` 使灯光平滑变化；开关类设备忽略此参数  
  **Transitions**: `"transition": 0.5` enables smooth changes for lights; ignored by switches

- **entity_id 发现**：不确定实体 ID 时先用"查询设备"命令列出所有实体  
  **Discovering entities**: Use the query commands to list entities when unsure of entity_id

- **401 错误**：Token 错误或已过期，重新在 HA 创建  
  **401 error**: Token invalid or expired — recreate in HA Profile → Security

- **404 错误**：entity_id 不存在，先列出所有实体后再操作  
  **404 error**: entity_id does not exist — list all entities first

---

## 发布信息 / Publishing

```bash
# 校验格式 / Validate format
clawhub validate ./skills/xiaomi-home-ha

# 发布到 ClawHub / Publish to ClawHub
clawhub publish ./skills/xiaomi-home-ha \
  --slug xiaomi-home-ha \
  --name "小米智能家居 (Xiao Mi Home for HA)" \
  --version 1.0.0 \
  --changelog "Initial release: full Xiaomi/HA device control via curl + jq"

# 安装验证 / Verify installation
clawhub install xiaomi-home-ha
clawhub list | grep xiaomi-home-ha
```

````
