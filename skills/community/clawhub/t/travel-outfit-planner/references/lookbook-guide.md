# 视觉灵感板（Lookbook）详细参考

本文档是 `travel-outfit-planner` 技能的 Step 6 补充参考，包含 JSON 数据结构、灵感板模块说明和降级策略。

## JSON 数据结构

灵感板的输入是一个 JSON 文件，结构如下：

```json
{
  "title": "日本7天旅行胶囊衣橱灵感板",
  "summary": {
    "trip": "京都 3天 + 大阪 2天 + 富士山区域 2天",
    "style": "日系清新",
    "traveler": "女生"
  },
  "colors": {
    "swatches": [
      {"name": "奶白", "hex": "#F5F0EB"},
      {"name": "灰绿", "hex": "#8FA68B"}
    ],
    "formulas": [
      "奶白上衣 + 浅米下装 + 灰绿针织外搭"
    ],
    "xhs_search": "京都 春季 日系清新 奶白 灰绿 穿搭配色"
  },
  "items": [
    {
      "id": 1,
      "name": "棉麻衬衫",
      "color_material": "奶白 / 棉麻",
      "scenes": "京都神社、大阪街拍",
      "xhs_search": "奶白棉麻衬衫 女生 春季 京都拍照"
    }
  ],
  "scenes": [
    {
      "name": "Day 1-3 · 京都",
      "description": "神社巡礼 + 樱花拍照 + 和服体验",
      "outfit_hint": "#1 奶白棉麻衬衫 + #4 浅米A字裙 + #2 灰绿针织开衫",
      "keywords_cn": ["京都", "神社", "樱花", "春季"],
      "xhs_search": "京都 神社 樱花 日系清新 女生穿搭"
    }
  ],
  "daily": [
    {
      "day_label": "Day 1 — 4月7日（京都）",
      "scene": "伏见稻荷大社 + 清水寺",
      "outfit": "#1 奶白棉麻衬衫 + #4 浅米A字裙 + #2 灰绿针织开衫",
      "shoes": "#7 白色帆布鞋",
      "accessories": "编织草帽、帆布斜挎包",
      "weather_tip": "最高 18°C / 最低 9°C，早晚需要针织外搭",
      "keywords_cn": ["京都", "神社", "樱花", "春季"],
      "xhs_search": "京都 伏见稻荷 樱花 日系清新 女生穿搭"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 灵感板标题 |
| `summary.trip` | string | 行程概要 |
| `summary.style` | string | 穿搭风格 |
| `summary.traveler` | string | 旅行者类型（女生/男生/情侣等） |
| `colors.swatches` | array | 配色色块，每个包含 `name`（中文色名）和 `hex`（十六进制色值） |
| `colors.formulas` | array | 配色公式文字描述 |
| `colors.xhs_search` | string | 小红书配色搜索词 |
| `items` | array | 胶囊单品列表 |
| `items[].id` | number | 单品编号 |
| `items[].xhs_search` | string | 小红书单品搜索词 |
| `scenes` | array | 场景列表（按目的地分组） |
| `scenes[].keywords_cn` | array | 中文关键词（用于 Pexels 图片搜索） |
| `daily` | array | 每日穿搭日历 |
| `daily[].weather_tip` | string | 天气提示 |

## 灵感板包含的模块

| 模块 | 内容 | 图片来源 |
|------|------|----------|
| 色彩系统 | CSS 色块展示主色/辅助色/点缀色 + 配色公式 | 无需图片（纯 CSS） |
| 场景氛围 | 每个目的地/场景一张氛围图 + 穿搭建议 | Pexels API / CSS 占位符 |
| 胶囊单品 | 每件单品的卡片 + 小红书搜索按钮 | 小红书搜索链接 |
| 每日日历 | 场景图 + 穿搭公式 + 天气提示 + 搜索按钮 | Pexels API / CSS 占位符 |

## 脚本使用方式

```bash
# 无 API Key（降级模式，显示 CSS 占位符）
python3 {baseDir}/scripts/fetch_lookbook_images.py --input wardrobe_data.json --output wardrobe-lookbook.html

# 有 Pexels API Key（推荐，图片质量更高）
python3 {baseDir}/scripts/fetch_lookbook_images.py --input wardrobe_data.json --output wardrobe-lookbook.html --pexels-key YOUR_PEXELS_API_KEY
```

## 降级策略

| 环境 | 处理方式 |
|------|----------|
| 有 Pexels API Key | 调用 Pexels API 获取高质量场景图（200次/小时免费） |
| 无 API Key | 显示精心设计的 CSS 占位符（场景关键词 + 渐变背景）+ 小红书搜索引导按钮 |

> **注意**：Unsplash Source URL 已于 2024 年完全弃用，不再作为降级方案。推荐用户注册免费的 Pexels API Key 以获得最佳体验。
