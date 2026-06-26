# 音色推荐与BGM推荐

## 音色推荐

根据剧情内容（cut_story）推荐合适的配音音色。

### 接口

#### 提交音色推荐

```
POST /api/hook/submit/voice.recommend
```

#### 查询音色推荐结果

```
POST /api/hook/query/voice.recommend.result
```

> ⚠️ **轮询必须用 POST + body 传参**，不能用 GET + query string！

**轮询参数**：body 传 `{"task_id": server_task_id}`

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id |
| `cut_story` | string | ✅ | 剧情主线（来自AI剪辑结果） |

### 异步轮询

- **建议超时**：120秒
- **轮询间隔**：2-3秒

### 轮询响应（state=2 成功）

```json
{
  "err_code": -1,
  "state": 2,
  "data": {
    "state": 2,
    "result": {
      "recommended_voices": [
        {
          "voice_id": 1001,
          "voice_name": "磁性男声",
          "gender": "male",
          "scene": "悬疑/剧情"
        },
        {
          "voice_id": 1002,
          "voice_name": "温柔女声",
          "gender": "female",
          "scene": "情感/爱情"
        }
      ]
    }
  }
}
```

---

## BGM推荐

根据剧情内容（cut_story）推荐背景音乐。

### 接口

#### 提交BGM推荐

```
POST /api/hook/submit/bgm.recommend
```

#### 查询BGM推荐结果

```
POST /api/hook/query/bgm.recommend.result
```

> ⚠️ **轮询必须用 POST + body 传参**，不能用 GET + query string！

**轮询参数**：body 传 `{"task_id": server_task_id}`

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id |
| `cut_story` | string | ✅ | 剧情主线（来自AI剪辑结果） |

### 异步轮询

- **建议超时**：120秒
- **轮询间隔**：2-3秒

### 轮询响应（state=2 成功）

```json
{
  "err_code": -1,
  "state": 2,
  "data": {
    "state": 2,
    "result": {
      "recommended_bgm": [
        {
          "bgm_id": 2001,
          "bgm_name": "悬疑紧张",
          "style": "紧张刺激",
          "duration": "3:20"
        },
        {
          "bgm_id": 2002,
          "bgm_name": "高潮迭起",
          "style": "动感",
          "duration": "4:05"
        }
      ]
    }
  }
}
```

---

## BGM配置列表

获取可用的BGM曲目列表（分页）。

### 接口

```
POST /api/hook/bgm.config.list
```

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | int | ✅ | 页码（从1开始） |
| `page_size` | int | ✅ | 每页数量（建议 10-20） |

### 响应示例

```json
{
  "err_code": -1,
  "data": {
    "list": [
      {
        "bgm_id": 2001,
        "bgm_name": "悬疑紧张",
        "url": "https://cdn.example.com/bgm/xxx.mp3",
        "duration": 200,
        "style": "紧张"
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 10
  }
}
```

## 注意事项

- 音色推荐和BGM推荐可以并行调用，互不依赖
- 推荐结果中的 `voice_id` / `bgm_id` 可用于后续视频合成时指定音色/BGM
- BGM配置列表接口**不需要**传 `task_id`，是独立接口
- BGM列表支持分页，适合做 BGM 选择器 UI
