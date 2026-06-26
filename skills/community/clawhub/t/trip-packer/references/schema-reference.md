# trip-packer JSON Schema 完整字段参考

## 根结构：ItineraryData

```json
{
  "metadata": { ... },
  "locations": { ... },
  "days": [ ... ]
}
```

---

## metadata

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `title` | `string` | 是 | 行程主标题 | `"京都古刹二日游"` |
| `subtitle` | `string` | 是 | 副标题 | `"京都站附近1晚 · 2日慢游"` |
| `startDate` | `string` | 否 | 开始日期（ISO格式） | `"2026-11-15"` |
| `endDate` | `string` | 否 | 结束日期 | `"2026-11-16"` |
| `mapCenter` | `object` | 否 | 地图默认中心 | `{ "lat": 35.01, "lng": 135.77 }` |
| `mapZoom` | `number` | 否 | 默认缩放级别（推荐 12-14） | `13` |
| `cityLabel` | `string` | 否 | 城市本地名称 | `"京都"` |
| `seasonLabel` | `string` | 否 | 季节标签 | `"AUTUMN"` |
| `flag` | `string` | 否 | Emoji 国旗 | `"🇯🇵"` |
| `country` | `string` | 否 | **ISO 国家代码**。`"CN"` 用高德瓦片，其他用 CARTO | `"JP"` |

---

## locations

`locations` 是一个以 `id` 为键的字典，每个值只能是以下两种类型之一：

### 类型 A：LocationGroup（商圈/酒店组）

用于 `type: "group"` 或 `"hotel_group"`。

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `id` | `string` | 是 | 唯一标识 | `"kyoto_station_hotel"` |
| `name` | `string` | 是 | 显示名称 | `"京都格兰比亚大酒店"` |
| `lat` | `number` | 是 | 纬度 | `34.985` |
| `lng` | `number` | 是 | 经度 | `135.758` |
| `color` | `string` | 是 | 标记颜色（hex） | `"#3b82f6"` |
| `type` | `string` | 是 | 固定为 `"group"` 或 `"hotel_group"` | `"hotel_group"` |
| `description` | `string` | 否 | 简短描述 | `"JR京都站上盖 · 交通便利"` |
| `address` | `string` | 否 | 详细地址 | `"京都府京都市下京区..."` |
| `children` | `string[]` | 是 | 子地点 `id` 列表 | `[]` |

### 类型 B：Location（具体地点）

用于 `type: "spot"`（景点、餐厅、店铺等）。

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `id` | `string` | 是 | 唯一标识 | `"kiyomizudera"` |
| `name` | `string` | 是 | 显示名称 | `"清水寺"` |
| `lat` | `number` | 是 | 纬度 | `34.9949` |
| `lng` | `number` | 是 | 经度 | `135.785` |
| `color` | `string` | 是 | 标记颜色（hex） | `"#ef4444"` |
| `type` | `string` | 是 | 固定为 `"spot"` | `"spot"` |
| `description` | `string` | 否 | 简短描述 | `"世界遗产 · 清水舞台"` |
| `parentId` | `string` | 是 | 所属 `LocationGroup` 的 `id` | `"kyoto_station_hotel"` |
| `address` | `string` | 否 | 详细地址 | `"京都府京都市东山区..."` |

> **注意**：Schema 不识别 `"food"`，餐厅也必须用 `"spot"`。

---

## days

`days` 是一个数组，每个元素代表一天的行程。

### DayPlan

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `day` | `number` | 是 | 第几天（从 1 开始） | `1` |
| `date` | `string` | 否 | 具体日期 | `"2026-11-15"` |
| `title` | `string` | 是 | 当日标题 | `"东山古刹巡礼"` |
| `note` | `string` | 是 | 当日说明/备忘 | `"上午清水寺参拜..."` |
| `baseHotelId` | `string` | 是 | 当日住宿酒店的 `id` | `"kyoto_station_hotel"` |
| `path` | `PathPoint[]` | 是 | 当日完整路径 | 见下文 |

### PathPoint

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `locationId` | `string` | 是 | 对应 `locations` 中的 `id` | `"kiyomizudera"` |
| `label` | `string` | 是 | 路径线上显示的文字 | `"公交206路 · 约20分钟"` |
| `transit` | `TransitDetail` | 否 | 从**上一个点**到本点的交通详情 | 见下文 |
| `isHotel` | `boolean` | 否 | 标记是否为酒店（首/尾常用） | `true` |
| `notes` | `NoteItem[]` | 否 | 本地点的备注列表 | 见下文 |

#### TransitDetail

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `distance` | `string` | 是 | 总距离 | `"约4公里"` |
| `duration` | `string` | 是 | 总时长 | `"约20分钟"` |
| `fare` | `string` | 否 | 票价 | `"230日元"` |
| `steps` | `TransitStep[]` | 是 | 分段详情 | 见下文 |
| `startName` | `string` | 是 | 起点名称 | `"京都站"` |
| `endName` | `string` | 是 | 终点名称 | `"清水寺"` |

#### TransitStep

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `mode` | `string` | 是 | 交通方式。可选值：`walk`, `subway`, `bus`, `train`, `taxi`, `airport` | `"bus"` |
| `line` | `string` | 否 | 线路名称 | `"市营巴士206路"` |
| `from` | `string` | 是 | 出发地 | `"京都站"` |
| `to` | `string` | 是 | 目的地 | `"五条坂站"` |
| `duration` | `string` | 是 | 本段时间 | `"约15分钟"` |
| `distance` | `string` | 否 | 本段距离 | `"约4公里"` |
| `instruction` | `string` | 是 | 导航说明 | `"乘坐市营巴士206路至五条坂"` |

#### NoteItem

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `category` | `string` | 是 | 分类。可选：`food`, `shopping`, `tips`, `other` | `"food"` |
| `content` | `string` | 是 | 内容 | `"推荐尝试抹茶冰淇淋"` |

---

## 常见规则与建议

### `path` 顺序
- `path[0]` 通常应该是 `baseHotelId` 对应的酒店，并设置 `isHotel: true`。
- 最后回到酒店时，最后一个 `PathPoint` 也建议设置 `isHotel: true`。
- 搬家日（换酒店）时，`path[0]` 可以是旧酒店，`path[1]` 为新酒店。

### `mode` 使用场景
- `walk`：步行
- `subway`：地铁
- `bus`：公交/巴士
- `train`：火车/JR/高铁
- `taxi`：出租车
- `airport`：机场专线/机场铁路

### `label` 写法建议
- 有交通时：`"公交206路 · 约20分钟"`、`"步行 · 约5分钟"`
- 无交通时（起点/酒店）：`"起点"`、`"入住"`

### `country` 与瓦片
- `"CN"`：国内使用**高德地图**瓦片
- 其他如 `"JP"`、`"KR"`、`"US"`：使用 **CARTO CDN** 瓦片

---

## 完整最小示例

参见 `sample-itinerary.json`（京都 2 日游示例）。
