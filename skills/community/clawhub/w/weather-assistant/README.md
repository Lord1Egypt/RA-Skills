# 天气助手 Weather Assistant — Skill README

## 一、功能概述

天气助手是一个集天气查询、定时推送、城市配置于一体的完整天气服务系统：

1. **随时查询天气** — 通过 skill 触发，查询任意城市天气
2. **每日定时推送** — 每天早上 8:00 自动推送天气到微信，附带名人名言
3. **可视化配置城市** — 三个字段均可编辑（显示名、wttr.in 查询名、简称）
4. **穿衣建议** — 根据天气自动给出简短穿衣建议

---

## 二、系统架构

```
定时触发 (cron 08:00)          用户对话触发
    │                              │
    ▼                              ▼
isolated agent session        skill: weather-assistant
    │                              │
    │  读取 config.json            │  读取 config.json
    │  curl wttr.in → 查天气       │  curl wttr.in → 查天气
    │  cat 名人名言.md → 随机名言    │  cat 名人名言.md → 随机名言
    │                              │
    ▼                              ▼
delivery (announce) → 微信     直接输出天气信息
```

**关键点**：定时推送不依赖任何 Python 脚本，完全由 cron agent 的 LLM 直接调用 `exec` 工具完成。agent 读取 cron payload 中的提示词，执行 curl 命令获取天气，格式化后输出，由 delivery 机制自动推送到微信。

---

## 三、文件结构

```
~/.qclaw/skills/weather-assistant/
├── SKILL.md          # Skill 定义文件
├── README.md         # 本文件
└── config.json       # 城市配置文件（可视化编辑）

依赖的外部文件：
~/workspace/名人名言.md         # 名人名言数据源（定时推送用）
~/.qclaw/scripts/get-token.sh  # Gateway API token 获取脚本（调试用）
```

---

## 四、配置文件格式

**文件路径：** `~/.qclaw/skills/weather-assistant/config.json`

```json
{
  "cities": [
    {
      "name": "上海（示例）",
      "query": "Shanghai",
      "alias": "上海"
    },
    {
      "name": "北京（示例）",
      "query": "Beijing",
      "alias": "北京"
    }
  ]
}
```

### 字段说明

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `name` | ✅ | 显示名称，完整地名 | "北京"、"东京" |
| `query` | ✅ | wttr.in 查询名，英文 | "Beijing"、"Tokyo"、"New+York" |
| `alias` | ✅ | 简称，推送时显示 | "北京"、"东京" |

### wttr.in 支持的查询名

支持城市英文名、有空格时用 `+` 连接：
- 北京 → `Beijing`
- 上海 → `Shanghai`
- 东京 → `Tokyo`
- 纽约 → `New+York`
- 伦敦 → `London`
- 巴黎 → `Paris`

---

## 五、定时推送 Cron 配置

### Cron 任务详情

| 字段 | 值 |
|------|------|
| 表达式 | `0 8 * * *`（每天早上 8:00） |
| 时区 | Asia/Shanghai |
| sessionTarget | isolated |
| wakeMode | now |
| delivery.mode | `announce` |
| delivery.channel | `openclaw-weixin` |

### 完整 Cron Payload 提示词

cron job 中 `payload.message` 的完整内容，agent 靠这段提示词完成所有工作：

```
你是一个贴心的天气播报助手。请完成以下任务：

1. 读取 ~/.qclaw/skills/weather-assistant/config.json 获取城市列表，对每个城市查询天气：
```bash
curl -s "wttr.in/{query}?format=j1"
```

2. 从天气数据中提取当天（index=0）的：
   - 最低温/最高温（mintempC / maxtempC，格式：13~16°C）
   - 天气状况（weatherDesc[0]['value']，对应：Sunny=☀️ 阴=☁️ 多云=⛅ 雨=🌧 雾=🌫 雪=❄️）
   - 湿度（humidity）
   - 风向（winddir16Point）和风速（windspeedKmph）

3. 从文件 ~/workspace/名人名言.md 中读取所有句子，随机选择1条作为每日名言：
```bash
cat ~/workspace/名人名言.md
```
随机选一条（不要按天气匹配，随机即可）。

4. 输出格式（控制在6-8句，不回复HEARTBEAT_OK，不调用message工具，直接输出内容）：

🌤 早安！X月X日天气播报

☁️ 【城市alias】
气温 XX~XX°C，【天气】
湿度 XX%，【风向】风 XXkm/h
穿衣建议：【简短建议】

☀️ 【城市alias】
气温 XX~XX°C，【天气】
湿度 XX%，【风向】风 XXkm/h
穿衣建议：【简短建议】

💡「【从名人名言.md随机选的句子】」

要求：(1)不回复HEARTBEAT_OK (2)不调用message工具 (3)直接输出内容 (4)温暖简洁有活力 (5)气温格式为低温~高温
```

### 手动触发

```bash
openclaw cron run YOUR_CRON_JOB_ID
```

---

## 六、微信推送配置

| 参数 | 值 | 说明 |
|------|------|------|
| channel | `openclaw-weixin` | 微信公众号通道 |
| target | `YOUR_WECHAT_OPENID` | 用户 OpenID |
| accountId | `YOUR_WECHAT_ACCOUNT_ID` | 微信 bot 账号 |
| delivery.mode | `announce` | cron 运行结果自动推送 |
| delivery.bestEffort | `true` | 推送失败不阻塞 |

### Gateway API（手动调试用）

- Base URL: `http://localhost:{GATEWAY_PORT}/api/v1`
- Token 获取: `bash ~/.qclaw/scripts/get-token.sh`

手动推送示例：
```bash
TOKEN=$(bash ~/.qclaw/scripts/get-token.sh)
curl -X POST "http://localhost:{GATEWAY_PORT}/api/v1/messages/send" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "openclaw-weixin",
    "target": "YOUR_WECHAT_OPENID",
    "accountId": "YOUR_WECHAT_ACCOUNT_ID",
    "message": "🌤 早安！..."
  }'
```

---

## 七、wttr.in API 详解

### 查询接口
```
curl -s "wttr.in/{城市}?format=j1"
```

### 关键字段提取

```json
{
  "weather": [{
    "mintempC": "13",
    "maxtempC": "16",
    "hourly": [{
      "weatherDesc": [{"value": "Sunny"}],
      "humidity": "65",
      "winddir16Point": "NE",
      "windspeedKmph": "15"
    }]
  }]
}
```

提取逻辑：
- 气温：`weather[0].mintempC` / `weather[0].maxtempC`
- 天气描述：`weather[0].hourly[4].weatherDesc[0].value`（取中午时段）
- 湿度/风：同理从 hourly 取

### 天气 emoji 映射

| 原文 | Emoji |
|------|------|
| Sunny/Clear | ☀️ |
| Overcast/Cloudy | ☁️ |
| Partly cloudy | ⛅ |
| Rain/Drizzle/Mist | 🌧 |
| Fog | 🌫 |
| Snow | ❄️ |

---

## 八、Skill 触发方式

**触发关键词：**
- "天气"、"查天气"、"今天天气"
- "天气推送"、"每日天气"、"天气播报"
- "城市配置"、"改城市"、"加城市"
- "weather"

---

## 九、重建指南

### 从零重建此 Skill

```bash
# 1. 创建目录和配置文件
mkdir -p ~/.qclaw/skills/weather-assistant
cat > ~/.qclaw/skills/weather-assistant/config.json << 'EOF'
{
  "cities": [
    {"name": "上海（示例）", "query": "Shanghai", "alias": "上海"},
    {"name": "北京（示例）", "query": "Beijing", "alias": "北京"}
  ]
}
EOF

# 2. 创建定时推送 cron
openclaw cron add \
  --name "每日早8点天气推送" \
  --schedule '{"kind":"cron","expr":"0 8 * * *","tz":"Asia/Shanghai"}' \
  --payload '{"kind":"agentTurn","message":"<上面的完整提示词>"}' \
  --delivery '{"mode":"announce","channel":"openclaw-weixin","to":"YOUR_WECHAT_OPENID","accountId":"YOUR_WECHAT_ACCOUNT_ID"}'

# 3. 准备名言文件
确保 ~/workspace/名人名言.md 存在

# 4. 测试
openclaw cron run <job-id>
```

---

## 十、已知限制

1. **wttr.in 偶发超时**：服务有时响应慢，curl 建议加 `-m 15` 超时
2. **微信推送偶发丢失**：风控原因，无法根治；delivery 设了 bestEffort
3. **wttr.in 不支持区县级**：城市用对应英文名查询
4. **名言文件格式**：每条以数字编号开头（如 `1. 我们必须习惯...`），agent 会自动去掉编号
