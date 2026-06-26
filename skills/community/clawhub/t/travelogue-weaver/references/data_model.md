# 数据模型定义

本文档定义了 Travelogue Weaver 技能使用的核心数据结构。

## 目录
- [旅行记录（Trip）](#旅行记录trip)
- [素材（Moment）](#素材moment)
- [生成的游记（Itinerary）](#生成的游记itinerary)
- [数据存储格式](#数据存储格式)

## 旅行记录（Trip）

旅行记录代表一次完整的旅行，从开始到结束的整个生命周期。

### 数据结构

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| tripId | string | 是 | 唯一标识符（UUID 格式） |
| status | enum | 是 | 状态：`ongoing`（进行中）或 `ended`（已结束） |
| title | string | 是 | 旅行标题（用户指定或自动生成） |
| startTime | datetime | 是 | 开始时间（ISO 8601 格式） |
| startLocation | string | 否 | 起始地点 |
| startEvent | string | 否 | 开始事件描述 |
| endTime | datetime | 否 | 结束时间（仅当状态为 ended 时） |
| endLocation | string | 否 | 结束地点 |
| endEvent | string | 否 | 结束感言 |
| stylePreference | string | 否 | 游记风格偏好（默认：文艺） |
| createdAt | datetime | 是 | 记录创建时间 |

### 示例

```json
{
  "tripId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "ongoing",
  "title": "云南七日漫游",
  "startTime": "2026-04-03T08:30:00",
  "startLocation": "北京",
  "startEvent": "从北京大兴机场出发",
  "endTime": null,
  "endLocation": null,
  "endEvent": null,
  "stylePreference": "文艺",
  "createdAt": "2026-04-03T08:30:00"
}
```

### 状态转换

```
[创建] → ongoing → [结束] → ended
          ↓
       [删除]
```

### 字段约束

- **tripId**: 必须唯一，使用 UUID v4 格式
- **status**: 只能是 `ongoing` 或 `ended`
- **title**: 长度 1-100 字符
- **startTime**: ISO 8601 格式，如 `2026-04-03T08:30:00`
- **stylePreference**: 可选值为 `文艺`、`幽默`、`简洁`、`详细`

## 素材（Moment）

素材是旅行过程中记录的各类内容，包括文字、图片、语音和视频。

### 数据结构

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| momentId | string | 是 | 唯一标识符（UUID 格式） |
| tripId | string | 是 | 所属旅行 ID |
| type | enum | 是 | 类型：`text`、`image`、`audio`、`video` |
| content | string | 是 | 内容（文本/描述/转写文字） |
| rawUrl | string | 否 | 原始文件存储路径 |
| timestamp | datetime | 是 | 时间戳（ISO 8601 格式） |
| location | string | 否 | 地点名称 |
| exif | object | 否 | 图片/视频的 EXIF 元数据 |

### 示例

#### 文字素材
```json
{
  "momentId": "m1n2o3p4-q5r6-7890-stuv-wx1234567890",
  "tripId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "text",
  "content": "洱海的风真大，但蓝得不像话",
  "rawUrl": null,
  "timestamp": "2026-04-03T15:30:00",
  "location": "洱海",
  "exif": null
}
```

#### 图片素材
```json
{
  "momentId": "m1n2o3p4-q5r6-7890-stuv-wx1234567891",
  "tripId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "image",
  "content": "折多山垭口的石碑，海拔4298米",
  "rawUrl": "./travelogue_data/uploads/m1n2o3p4-q5r6-7890-stuv-wx1234567891.jpg",
  "timestamp": "2026-04-03T14:20:00",
  "location": "折多山",
  "exif": {
    "DateTime": "2026:04:03 14:20:15",
    "GPSLatitude": "30.1234",
    "GPSLongitude": "101.5678"
  }
}
```

#### 音频素材
```json
{
  "momentId": "m1n2o3p4-q5r6-7890-stuv-wx1234567892",
  "tripId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "audio",
  "content": "刚刚在古城吃到了烤乳扇，酸酸甜甜，老板说是当地特色",
  "rawUrl": "./travelogue_data/uploads/m1n2o3p4-q5r6-7890-stuv-wx1234567892.mp3",
  "timestamp": "2026-04-03T16:45:00",
  "location": "大理古城",
  "exif": null
}
```

#### 视频素材
```json
{
  "momentId": "m1n2o3p4-q5r6-7890-stuv-wx1234567893",
  "tripId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "video",
  "content": "客栈阳台的风景，远处是苍山",
  "rawUrl": "./travelogue_data/uploads/m1n2o3p4-q5r6-7890-stuv-wx1234567893.mp4",
  "timestamp": "2026-04-03T18:00:00",
  "location": "双廊客栈",
  "exif": null
}
```

### 字段约束

- **momentId**: 必须唯一，使用 UUID v4 格式
- **tripId**: 必须引用有效的 tripId
- **type**: 只能是 `text`、`image`、`audio`、`video`
- **content**: 
  - text 类型：≤5000 字符
  - 其他类型：≤500 字符的描述
- **timestamp**: ISO 8601 格式，默认为当前系统时间
- **location**: 可选，长度 ≤100 字符

## 生成的游记（Itinerary）

游记是根据旅行记录和素材自动生成的最终输出。

### 数据结构

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| itineraryId | string | 是 | 唯一标识符 |
| tripId | string | 是 | 关联的旅行 ID |
| markdownContent | text | 是 | 游记的 Markdown 正文 |
| htmlUrl | string | 否 | 云端 HTML 访问地址 |
| pdfUrl | string | 否 | 云端 PDF 地址 |
| generatedAt | datetime | 是 | 生成时间 |

### 生成规则

1. **标题生成**：使用 trip.title，格式为 `# 【{title}】`
2. **章节划分**：按日期分组素材，每一天为一个章节
3. **时间标注**：每个章节显示日期
4. **地点标注**：提取当天主要地点
5. **内容组织**：按时间顺序排列素材
6. **多媒体处理**：
   - 图片：使用 Markdown 图片语法 `![描述](路径)`
   - 音频：使用特殊标记 `🎵 *语音记录：内容*`
   - 视频：使用特殊标记 `🎬 *视频记录：内容*`
7. **后记**：包含结束时间、地点和感言

## 数据存储格式

### 文件结构

```
./travelogue_data/
├── trips.json          # 旅行记录列表
├── moments.json        # 素材列表
└── uploads/            # 上传文件存储目录
    ├── {momentId}.jpg
    ├── {momentId}.mp3
    └── {momentId}.mp4
```

### trips.json 格式

```json
[
  {
    "tripId": "...",
    "status": "ongoing",
    ...
  },
  {
    "tripId": "...",
    "status": "ended",
    ...
  }
]
```

### moments.json 格式

```json
[
  {
    "momentId": "...",
    "tripId": "...",
    ...
  },
  ...
]
```

### 数据完整性约束

1. **外键约束**：每个 moment 的 tripId 必须在 trips.json 中存在
2. **唯一性约束**：tripId 和 momentId 必须全局唯一
3. **状态一致性**：只能有一个 status 为 ongoing 的旅行记录
4. **时间顺序**：endTime 必须晚于 startTime
5. **文件关联**：rawUrl 字段引用的文件必须存在

### 数据操作规范

1. **创建旅行**：
   - 检查是否已有 ongoing 状态的旅行
   - 生成唯一 tripId
   - 写入 trips.json

2. **添加素材**：
   - 验证 tripId 是否存在且状态为 ongoing
   - 生成唯一 momentId
   - 处理文件上传（如有）
   - 写入 moments.json

3. **结束旅行**：
   - 更新 trip 状态为 ended
   - 设置 endTime、endLocation、endEvent
   - 保存到 trips.json

4. **删除旅行**：
   - 从 trips.json 中移除记录
   - 级联删除所有关联的素材
   - 删除 uploads 目录中的相关文件

## 验证规则

### 旅行记录验证

```python
def validate_trip(trip):
    errors = []
    
    # 必需字段检查
    required = ['tripId', 'status', 'title', 'startTime', 'createdAt']
    for field in required:
        if field not in trip:
            errors.append(f"缺少必需字段: {field}")
    
    # 状态检查
    if trip.get('status') not in ['ongoing', 'ended']:
        errors.append("status 必须是 'ongoing' 或 'ended'")
    
    # 标题长度检查
    if len(trip.get('title', '')) > 100:
        errors.append("title 长度不能超过 100 字符")
    
    # 时间格式检查
    try:
        datetime.fromisoformat(trip['startTime'])
    except:
        errors.append("startTime 格式不正确，应为 ISO 8601 格式")
    
    return errors
```

### 素材验证

```python
def validate_moment(moment):
    errors = []
    
    # 必需字段检查
    required = ['momentId', 'tripId', 'type', 'content', 'timestamp']
    for field in required:
        if field not in moment:
            errors.append(f"缺少必需字段: {field}")
    
    # 类型检查
    if moment.get('type') not in ['text', 'image', 'audio', 'video']:
        errors.append("type 必须是 'text', 'image', 'audio' 或 'video'")
    
    # 内容长度检查
    content = moment.get('content', '')
    if moment.get('type') == 'text' and len(content) > 5000:
        errors.append("text 类型内容不能超过 5000 字符")
    elif len(content) > 500:
        errors.append("非 text 类型内容不能超过 500 字符")
    
    return errors
```

## 错误处理

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| TRIP_NOT_FOUND | 旅行记录不存在 |
| MOMENT_NOT_FOUND | 素材不存在 |
| TRIP_ALREADY_ONGOING | 已有进行中的旅行 |
| TRIP_ALREADY_ENDED | 旅行已结束 |
| NO_ONGOING_TRIP | 没有进行中的旅行 |
| INVALID_STATUS | 无效的状态值 |
| INVALID_TYPE | 无效的素材类型 |
| FILE_NOT_FOUND | 文件不存在 |

### 错误响应格式

```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "ERROR_CODE"
}
```
