# 小红书矩阵系统 API 文档

## 基础信息

- **API 域名**: `http://redapi.cn`
- **完整 URL**: `http://redapi.cn/api/external-api/{endpoint}`
- **认证方式**: 请求头 `X-API-Key: YOUR_API_KEY` 或查询参数 `?api_key=YOUR_API_KEY`
- **响应格式**: JSON

## 通用响应格式

```json
{
  "code": 200,
  "message": "成功",
  "data": {...}
}
```

## 错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 429 | 请求频率过高 |
| 500 | 服务器内部错误 |

---

## 接口列表

### GET /external-api/accounts（消耗 1 次）

获取账号列表

```python
import requests

url = "http://redapi.cn/api/external-api/accounts"
headers = {"X-API-Key": "YOUR_API_KEY"}
response = requests.get(url, headers=headers)
data = response.json()

if data["code"] == 200:
    accounts = data["data"]["accounts"]
    for account in accounts:
        print(f"账号ID: {account['id']}, 昵称: {account['nickname']}")
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "accounts": [
      {"id": 123, "nickname": "小红薯用户", "red_id": "5f8a9b2c...", "status": "active"}
    ]
  }
}
```

---

### POST /external-api/search（消耗 2 次）

搜索笔记

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| keyword | string | 是 | 搜索关键词 |
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页数量，默认20 |
| sort | string | 否 | GENERAL/MOST_POPULAR/LATEST |

```python
import requests

url = "http://redapi.cn/api/external-api/search"
headers = {"X-API-Key": "YOUR_API_KEY", "Content-Type": "application/json"}
data = {"keyword": "美食推荐", "page": 1, "page_size": 20, "sort": "MOST_POPULAR"}
response = requests.post(url, headers=headers, json=data)
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "keyword": "美食推荐",
    "total": 1000,
    "has_more": true,
    "items": [
      {
        "id": "67685c7f...",
        "title": "超好吃的蛋糕制作教程",
        "desc": "分享一个简单易学的蛋糕...",
        "author": {"nickname": "美食达人小王", "user_id": "5f8a9b2c..."},
        "like_count": 2580,
        "images": ["https://example.com/image1.jpg"]
      }
    ]
  }
}
```

---

### POST /external-api/note-detail（消耗 2 次）

获取笔记详情

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| note_id | string | 是 | 笔记ID |
| xsec_token | string | 是 | 笔记安全令牌 |

```python
import requests

url = "http://redapi.cn/api/external-api/note-detail"
headers = {"X-API-Key": "YOUR_API_KEY", "Content-Type": "application/json"}
data = {"note_id": "67685c7f000000001e00f5b9", "xsec_token": ""}
response = requests.post(url, headers=headers, json=data)
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "note_id": "67685c7f...",
    "title": "超好吃的蛋糕制作教程",
    "desc": "今天分享一个简单易学的蛋糕...",
    "type": "normal",
    "images": [{"url": "https://sns-img-qc.xhscdn.com/...", "width": 1024, "height": 768}],
    "interact_info": {"liked_count": 2580, "collected_count": 456, "comment_count": 128, "share_count": 89},
    "author": {"user_id": "5f8a9b2c...", "nickname": "美食达人小王", "avatar": "..."},
    "tags": ["美食", "烘焙", "蛋糕"],
    "publish_time": 1699123456000,
    "ip_location": "上海"
  }
}
```

---

### POST /external-api/publish（消耗 5 次）

发布图文笔记

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| account_id | integer | 是 | 小红书账号ID |
| title | string | 是 | 笔记标题（最大100字符） |
| content | string | 是 | 笔记内容（最大1000字符） |
| image_urls | array | 是 | 图片URL列表（1-9张） |
| topics | array | 否 | 话题标签列表 |
| scheduled_at | string | 否 | 定时发布时间 YYYY-MM-DD HH:MM:SS |

```python
import requests

url = "http://redapi.cn/api/external-api/publish"
headers = {"X-API-Key": "YOUR_API_KEY", "Content-Type": "application/json"}
data = {
    "account_id": 123,
    "title": "分享一道超好吃的家常菜",
    "content": "今天给大家分享一道简单易做的家常菜...",
    "image_urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    "topics": ["美食", "家常菜"]
}
response = requests.post(url, headers=headers, json=data)
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "task_id": "task_123456789",
    "status": "scheduled",
    "scheduled_at": "2024-01-15 18:00:00"
  }
}
```

---

### GET /external-api/usage（消耗 1 次）

获取使用统计

```python
import requests

url = "http://redapi.cn/api/external-api/usage"
headers = {"X-API-Key": "YOUR_API_KEY"}
params = {"page": 1, "per_page": 10}
response = requests.get(url, headers=headers, params=params)
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "total_requests": 1000,
    "remaining_requests": 750,
    "today_usage": 25,
    "records": [{"endpoint": "/external-api/search", "cost": 2, "created_at": "2024-01-15 14:30:00"}]
  }
}
```
