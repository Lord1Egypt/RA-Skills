# TJWeather Skill (tjweather) 🌤️

这是一个为 OpenClaw 开发的全球天气查询插件，核心调用 **TJWeather API**。它不仅支持精准的全球天气预测，还内置了三级地理编码回退机制，确保在各种网络环境下都能稳定获取位置坐标。

---

## 🌐 官方资源
- **气象官网**: [https://www.tjweather.com/](https://www.tjweather.com/)
- **API Key 申请**: [https://www.tjweather.com/Apply](https://www.tjweather.com/Apply)
- **试用 Key**: 我们提供了 3 个试用 Key，欢迎大家使用和反馈意见：
  - `aok356vvxetuz8ijnudw76gb`
  - `aok32r59lwskymrt80yvcv46`
  - `AOK202508111438522A2949E198FB80E6D3ACAC2003A65C`

## 🛠️ 环境配置要求
- **运行环境**: Python 3.8+ 
- **依赖库**: 仅需 Python 标准库 (`sys`, `json`, `urllib`, `difflib`)。
- **网络能力**: 
  - **方案一/二 (首选)**: 需要具备**国际网络访问能力**（以连接 OpenStreetMap 等国际地理编码服务）。
  - **方案三 (离线模式)**: 内置中国行政区划数据库，可在无国际网络时作为大陆地区的兜底方案。

---

## ⚙️ 技能配置 (Skills Config)

本 Skill 需要在 `~/.openclaw/openclaw.json` 中配置你的 API Key。

### 1. 基础配置
在 `skills.entries` 下添加 `tjweather` 项。

> [!TIP]
> **apiKey** 字段可以接受明文字符串，也可以接受 `SecretRef` 对象以增强安全性。

#### 方案 A：明文配置 (简单快捷)
```json
{
  "skills": {
    "entries": {
      "tjweather": {
        "enabled": true,
        "apiKey": "您的_TJWEATHER_API_KEY"
      }
    }
  }
}
```

#### 方案 B：引用环境变量 (推荐)
如果您已经在系统环境变量中设置了 `TJWEATHER_API_KEY`，可以使用 `SecretRef`：
```json
{
  "skills": {
    "entries": {
      "tjweather": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "TJWEATHER_API_KEY" }
      }
    }
  }
}
```

### 2. 智能体可见性控制 (Agent Visibility)
您可以精确控制哪些 Agent 可以调用此技能。

- **默认开放**: 
  ```json
  "agents": { "defaults": { "skills": ["tjweather"] } }
  ```
- **特定 Agent 专属**:
  ```json
  "agents": {
    "list": [
      { "id": "weather-expert", "skills": ["tjweather"] }
    ]
  }
  ```

> [!IMPORTANT]
> **配置生效**: `tjweather` 的 `apiKey` 会被 OpenClaw 自动注入到运行时的环境变量 `TJWEATHER_API_KEY` 中，Agent 将直接透明使用。

---

## 📍 地理编码查询 (3级回退机制)

为了保证全球范围内搜索的准确性与稳定性，本工具按优先级依次尝试：

1. **方案一 (Nominatim)**: 调用 OpenStreetMap (OSM) 数据。全球精度最高，**必须具备国际网络访问能力**。
2. **方案二 (Photon)**: 基于 Komoot 的搜索引擎，作为首选方案失效后的快速补充。
3. **方案三 (中国内部库)**: **中国大陆兜底方案**。内置全量行政区划坐标，确保在网络受限时国内城市查询依然秒开。

---

## 📝 使用规范

### 1. 预测天数
目前版本建议预测天数在 **10 天** 以内（受 API 版本限制）。

### 2. 输出语言
- **主要语向**: 输出以 **中文** 为主。
- **动态适配**: 智能体会根据全局配置自动将数据标签（如温度、风级）翻译为用户所需语言。

---

> [!NOTE]
> 更多详情请参考 [SKILL.md](./SKILL.md) 了解 Agent 的内部执行逻辑。
