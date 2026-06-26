# 星露谷 Mod 制作参考

## Event 触发条件

### 常用条件

| 条件 | 代码 | 示例 |
|------|------|------|
| 结婚 | `Spouse NPC名` | `Spouse mizuki` |
| 约会 | `Dating NPC名` | `Dating mizuki` |
| 好感度 | `Friendship NPC名 数字` | `Friendship mizuki 2500` (10心) |
| 时间 | `Time 开始 结束` | `Time 600 1800` |
| 天气 | `Weather rainy/sunny` | `Weather rainy` |
| 季节 | `Season spring/summer/fall/winter` | `Season summer` |
| 日期 | `DayOfMonth 数字` | `DayOfMonth 25` |
| 星期 | `DayOfWeek Mon/Tue/Wed` | `DayOfWeek Sat` |

### NPC 内部名（结婚可触发）

原版可结婚 NPC：
- abigail, alex, elliott, emily, haley, harvey
- leah, maru, penny, sam, sebastian, shane, krobus

### 爱心对应

| 爱心 | 分数 |
|------|------|
| 1心 | 250 |
| 2心 | 500 |
| ... | ... |
| 10心 | 2500 |

## 对话格式

### 婚后对话 Key

- `Rainy_Day_0` - 雨天白天
- `Rainy_Night_0` - 雨天夜晚
- `Indoor_Day_0` - 室内白天
- `Indoor_Night_0` - 室内夜晚
- `Outdoor_0` - 室外
- `Good_0` - 高好感
- `Neutral_0` - 中好感
- `Bad_0` - 低好感

### 对话表情代码

- `$1` - 开心
- `$3` - 悲伤
- `$4` - 恋爱
- `$7` - 失落
- `$9` - 感动

## CP 常用 Action

| Action | 用途 |
|--------|------|
| `Load` | 加载文件 |
| `EditData` | 编辑数据 |
| `EditImage` | 编辑图片 |
| `EditMap` | 编辑地图 |
| `Include` | 包含其他 JSON |

## Target 路径

| 路径 | 用途 |
|------|------|
| `Data/NPCs` | NPC 数据 |
| `Characters/Dialogue/XXX` | 对话 |
| `Data/NPCGiftTastes` | 礼物喜好 |
| `Data/Events/地点` | 事件 |
| `Characters/schedules/XXX` | 行程 |
