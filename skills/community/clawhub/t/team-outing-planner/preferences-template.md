# 团队偏好收集模板

## JSON 批量输入格式

当团队人数较多时，可使用以下 JSON 格式批量输入所有成员的偏好：

```json
{
  "teamInfo": {
    "teamSize": 15,
    "departureCity": "杭州",
    "plannedDate": "2026-05-01",
    "duration": "2天1晚",
    "budgetPerPerson": 800
  },
  "members": [
    {
      "name": "张三",
      "preferences": ["自然风光", "温泉度假"],
      "intensity": "轻松休闲",
      "specialNeeds": []
    },
    {
      "name": "李四",
      "preferences": ["户外运动", "主题乐园"],
      "intensity": "适度活动",
      "specialNeeds": ["晕车"]
    },
    {
      "name": "王五",
      "preferences": ["历史古迹", "城市观光"],
      "intensity": "轻松休闲",
      "specialNeeds": []
    }
  ]
}
```

## 字段说明

### teamInfo 团队信息

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| teamSize | number | 参与人数 | 15 |
| departureCity | string | 出发城市 | "杭州" |
| plannedDate | string | 计划日期 | "2026-05-01" |
| duration | string | 活动时长 | "2天1晚" |
| budgetPerPerson | number | 人均预算(元) | 800 |

### members 成员偏好

| 字段 | 类型 | 说明 | 可选值 |
|------|------|------|--------|
| name | string | 成员姓名 | - |
| preferences | array | 活动类型偏好(可多选) | 见下方选项 |
| intensity | string | 运动强度偏好 | 见下方选项 |
| specialNeeds | array | 特殊需求(可多选) | 见下方选项 |

### 活动类型选项 (preferences)

- `自然风光` - 山水、湖泊、森林等自然景观
- `历史古迹` - 古镇、博物馆、文化遗址
- `主题乐园` - 游乐园、水上乐园
- `温泉度假` - 温泉酒店、度假村
- `户外运动` - 徒步、漂流、滑雪、露营
- `城市观光` - 城市地标、美食购物

### 运动强度选项 (intensity)

- `轻松休闲` - 步行少，以观光和休息为主
- `适度活动` - 有一定步行量，节奏适中
- `挑战型` - 大量户外活动，对体力有要求

### 特殊需求选项 (specialNeeds)

- `行动不便` - 需要无障碍设施
- `恐高` - 避免高空项目
- `晕车` - 优先短途或高铁可达
- `饮食限制` - 素食/清真/过敏等
- 留空 `[]` 表示无特殊需求

## 简化版本

如果不需要详细偏好，可使用简化版本：

```json
{
  "teamInfo": {
    "teamSize": 10,
    "departureCity": "上海",
    "plannedDate": "2026-04-15",
    "budgetPerPerson": 500
  },
  "summary": {
    "preferenceVotes": {
      "自然风光": 4,
      "温泉度假": 3,
      "历史古迹": 2,
      "主题乐园": 1
    },
    "intensityVotes": {
      "轻松休闲": 6,
      "适度活动": 4
    },
    "specialNeeds": ["有1人晕车", "有1人恐高"]
  }
}
```
