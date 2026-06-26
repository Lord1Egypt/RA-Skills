---
name: tjweather
description: "全球地点天气预报及地理编码分析（TJWeather API）。"
homepage: https://api.tjweather.com
user-invocable: true
metadata: {"openclaw": {"emoji": "🌤️", "requires": {"bins": ["python3"], "env": ["TJWEATHER_API_KEY"]}, "primaryEnv": "TJWEATHER_API_KEY"}}
---

# TJWeather Skill 🌤️

通过 **TJWeather API** 查询全球任意地点的天气预报。本工具不仅提供精准的气象数据，还内置了高可靠性的三级地理编码回退逻辑，确保无论用户输入多么模糊，都能得到妥善的处理。

---

## ⚠️ 核心配置与准则

> [!IMPORTANT]
> **API KEY 获取**：本 Skill 依赖环境变量 `TJWEATHER_API_KEY`。该 Key 已由用户通过 `~/.openclaw/openclaw.json` 完成注入。
> **Agent 禁止行为**：严禁向用户索要或询问 API Key。

> [!TIP]
> **预报限制**：测试版本最长支持 **10 天**。若用户查询请求超过此限制，请在回复中礼貌说明，并展示前 10 天的数据。

---

## 🛠️ 执行流程 (强制逻辑)

作为 Agent，你必须严格按照以下阶段序列执行任务，不得跳步。

### 阶段一：地理编码 (Geocoding - CRITICAL)

你 **必须且仅能** 使用该内部脚本。**禁止** 使用内置 Web 搜索获取坐标。

```bash
# 执行地理编码查询
python3 {baseDir}/scripts/geocoder.py "{location_query}"
```

#### 🔍 响应处理深度指引
- **状态解析**：解析 JSON 输出中的 `lon`, `lat`, `name`, `source`, `tz`。
- **回退感知 (FALLBACK PROTOCOL)**：
    - 若 `source` 为 `Internal (Enhanced Fuzzy)`，意味着精确位置无法匹配，已回退到城市级坐标。**你必须在回复的首行明确告知用户**。
    - **逻辑示例**：用户查“龙旗广场”，若 Source 为 Internal，回复需包含：“未能找到龙旗广场的精确位置，已自动为您查询所属城市（北京市）的天气。”

### 阶段二：气象分析 (Weather Analysis)

结合获取的坐标与你对该地点**夏令时 (DST)** 的最终裁定，调用分析脚本。

```bash
# 执行天气预测、统计及大势分析
python3 {baseDir}/scripts/tjweather.py {lon} {lat} "{matched_name}" "{original_query}" {fcst_days} {tz}
```

> [!CAUTION]
> **时区 (tz) 裁定规则**：
> `geocoder.py` 返回的 `tz` 是物理经度转换的参考值。你必须运用你的通用知识，确认该地点当前是否处于夏令时（例如：伦敦在 3-10 月间需在 tz=0 基础上 +1），以确保回复时间线完全符合当地习惯。

---

## 📝 输出规范 (MANDATORY)

> [!IMPORTANT]
> **回复必须包含以下三个部分，漏掉任何一项均视为任务失败 (FAILED)：**
> 1. **首行自适应提示**：包含查询词、匹配结果及（如果有）回退说明。
> 2. **数据正文**：展示 `tjweather.py` 返回的所有每日统计（气温、风力、降水等）。
> 3. **温润体贴的总结**：在底部追加一段 `📝 总结`。语气需柔和、关怀备至，概括整体趋势并提供生活建议。

---

## 完整示例 (Success with Precision)

**用户：** "北京海淀区上地街道未来3天天气"

**你的逻辑：**
1. 调用 `geocoder.py "北京海淀区上地街道"` -> 返回 `source: Nominatim`, `name: 上地街道, 海淀区, 北京市, 100193, 中国`。
2. 确认由于是首选服务成功，无需回退提示。
3. 调用 `tjweather.py` 获取数据。

**期望输出：**
> 您查询的 北京海淀区上地街道 匹配到 上地街道, 海淀区, 北京市, 100193, 中国，坐标：116.29, 40.04
>
> 📅 2026年4月10日 星期五
> 🌡️ 气温: 7.5°C ~ 26.4°C
> ... (统计数据)
>
> 📝 总结: 上地街道这两天天气晴朗舒适，非常适合户外活动。早晚温差较大，建议您早出晚归时增加一件外套。祝您生活愉快！😊

---

> [!NOTE]
> 遵循本协议将使你的查询表现出卓越的专业度与拟人化的同理心。