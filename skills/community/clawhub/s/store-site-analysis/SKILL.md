---
name: store-site-analysis
description: 基于高德开放平台的商铺选址分析 Skill。支持单地址选址分析（竞品搜索、配套评估、交通态势、热力图可视化）和多地址对比分析（雷达图、柱状图、评分排名、聚合地图）。让 AI Agent 一句话完成开店选址评估。
version: "1.0.0"
author: 悟空码字
tags: [amap, lbs, site-analysis, poi, geocode, heatmap, visualization, traffic, compare, radar-chart]
---

# Store Site Analysis Skill

## 单地址分析模式 (Single Address Analysis)

### Trigger Condition
当用户提到以下意图时触发：
- 开店 / 选址 / 评估某个地址适不适合开 XX 店
- "帮我分析在 [地址] 开一家 [类型] 店"
- "查 [地址] 周边有多少家同类竞品"
- 用户明确要求生成地图 / 热力图 / 可视化

### Parameters
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| address | string | ✅ | — | 目标地址 |
| business_keyword | string | ❌ | "奶茶店\|咖啡厅\|小吃快餐\|便利店" | 竞品关键词 |
| business_type | string | ❌ | "" | POI 分类编码（精确匹配） |
| radius | number | ❌ | 1000 | 搜索半径（米），可选 500/1000/1500/2000/3000 |
| output_dir | string | ❌ | "/tmp/store-site-analysis" | 热力图输出目录 |

### Behavior
1. 调用 geocode 将 address → lng,lat（高德地理编码 API）
2. 调用 POI around 搜索同类 business_keyword（最多取 100 条）
3. 调用 POI around 搜索配套设施（types=120000|150500|141200|050000|060100|170000）
4. 调用 regeocode 获取行政区 / 商圈描述（逆地理编码 API）
5. 调用 traffic status 获取区域交通态势（交通态势 API）
6. 生成交互式热力图 HTML（高德 JS API + Handlebars 模板）
7. 返回 JSON + 热力图路径给 Agent，由 LLM 生成选址分析报告

### Output Schema
```json
{
  "address": "string",
  "location": "lng,lat",
  "district": "区名",
  "township": "街道名",
  "city": "城市名",
  "competitor_count": 12,
  "competitors": [{ "name": "店铺名", "address": "地址", "type": "类型", "distance": 120, "location": "lng,lat" }],
  "competitor_type_breakdown": { "咖啡厅": 8, "奶茶店": 4 },
  "facility_count": 32,
  "facilities": [{ "name": "设施名", "type": "类型", "distance": 50, "location": "lng,lat" }],
  "traffic_status": "1",
  "traffic_description": "畅通",
  "heatmap_html": "/tmp/store-site-analysis/xxx_heatmap.html",
  "analysis_summary": "已生成选址分析报告..."
}
```

---

## 多地址对比模式 (Multi-Address Compare)

### Trigger Condition
当用户提到以下意图时触发 compare 模式：
- 对比 / 比较 / 多个地址哪个更适合开 XX 店
- "帮我在 A、B、C 三个地方对比分析开奶茶店"
- "北京国贸、望京、三里屯，哪个更适合开健身房？"
- 用户明确列出 2~5 个地址做选址决策

### Parameters
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| addresses | string[] | ✅ | — | 地址数组（2~5 个） |
| business_keyword | string | ❌ | "奶茶店\|咖啡厅\|小吃快餐\|便利店" | 竞品关键词 |
| radius | number | ❌ | 1000 | 搜索半径（米） |

### Behavior
1. 并行对所有地址执行完整分析（geocode + POI 搜索 + 交通 + 逆地理编码）
2. 5 维度加权评分：
   - 竞品密度 25%（竞品越少分越高 = 100 - 竞品数 × 5）
   - 配套丰富度 20%（设施数 × 3，上限 100）
   - 交通便捷度 20%（地铁站数 × 25 + 畅通加分 20）
   - 商业活跃度 20%（商场 + 写字楼数量 × 15）
   - 居住潜力 15%（住宅小区数量 × 8）
3. 按综合分排序
4. 生成对比可视化 HTML（雷达图 + 柱状图 + 数据表 + 聚合地图）
5. 返回 rankings + compare_html + recommendation

### Output Schema
```json
{
  "summary": "完成 3 个地址的对比分析",
  "rankings": [
    {
      "rank": 1,
      "address": "厦门市思明区中山路",
      "district": "思明区",
      "township": "中华街道",
      "total_score": 78,
      "detail": {
        "competitor_score": 70,
        "facility_score": 85,
        "traffic_score": 90,
        "commercial_score": 80,
        "residence_score": 65
      },
      "competitor_count": 10,
      "facility_count": 32,
      "metro_count": 3,
      "residence_count": 12,
      "commercial_count": 8,
      "traffic_status": "1"
    }
  ],
  "compare_html": "/tmp/store-site-analysis/xxx_compare.html",
  "recommendation": "思明区（中华街道）综合得分最高（78分），最推荐作为选址目标。"
}
```

---

## Examples

### 单地址分析示例
```
User: 帮我在厦门市思明区中山路分析开一家奶茶店的选址情况
Agent: → 调用 store-site-analysis → 返回竞品数、周边配套、交通状态 + 热力图 HTML
```

### 多地址对比示例
```
User: 帮我在厦门中山路、SM城市广场、湖滨南路三个地方对比开奶茶店哪个更好
Agent: → 调用 store-site-analysis.compare → 并行分析 3 个地址 → 返回排名 + 雷达图 + 柱状图 + 对比表 HTML
```

---

## Environment Variables

| 变量名 | 必填 | 说明 |
|---|---|---|
| AMAP_KEY | ✅ | 高德开放平台 Web 服务 API Key |
| AMAP_JS_KEY | ❌ | 高德 JS API Key（用于前端热力图，默认同 AMAP_KEY） |

---

## Dependencies
- axios
- handlebars
- fs-extra