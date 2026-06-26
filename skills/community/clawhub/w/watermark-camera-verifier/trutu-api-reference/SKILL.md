---
name: trutu-api-reference
version: 1.0.0
description: >
  今日水印相机（Trutu）照片验真 API 完整封装参考手册。
  包含经过真实调试验证的鉴权算法、接口调用、轮询模式和错误处理，
  供封装其他平台插件/Skill 时直接引用。
metadata:
  openclaw:
    always: true
    emoji: "📖"
---

# 今日水印相机 照片验真 API 封装参考手册

> 本手册基于真实调试经验整理，所有细节均已通过实际 API 调用验证。
> 封装任何平台的验真插件时，直接以本文档为准。

---

## 一、API 基本信息

| 项目 | 内容 |
|------|------|
| 服务商 | 今日水印相机（xhey.top） |
| API 域名 | `openapi.xhey.top` |
| 协议 | HTTPS |
| 数据格式 | JSON |
| 凭证申请 | 电话 13141152023 联系官方获取 |

### 端点清单

| 功能 | 方法 | 路径 |
|------|------|------|
| 创建验真任务 | POST | `/v2/truth_build/create` |
| 查询验真结果 | POST | `/v2/truth_build/query` |
| 获取团队照片列表 | POST | `/v2/group/photo` |
| 多维度照片搜索 | POST | `/v2/group/photo/search` |
| 按 ID 获取水印数据 | POST | `/v2/group/watermark/byPhotoId` |
| 按时间获取水印数据 | POST | `/v2/group/watermark/byTime` |

---

## 二、鉴权算法（⚠️ 关键，有坑）

### 三个必须的请求 Header

```
GroupKey:   {groupKey}       ← 账号唯一标识
Timestamp:  {unix秒级时间戳}  ← 注意：秒，不是毫秒
Signature:  {两阶段签名结果}
```

### 两阶段 HMAC-SHA256 签名

> ⚠️ **最重要的坑**：签名结果必须用 **Base64** 编码，不是 hex（文档描述不清晰，实测确认）

```
Stage 1:
  dataSign = Base64( HMAC-SHA256(groupSecret, JSON.stringify(requestBody)) )

Stage 2:
  payload  = `groupKey=${groupKey}&sign=${dataSign}&timestamp=${timestamp}`
  Signature = Base64( HMAC-SHA256(groupSecret, payload) )
```

### Node.js 参考实现（已验证可用）

```javascript
const crypto = require('crypto');

function sign(secret, data) {
  // ⚠️ digest('base64') 而非 digest('hex')
  return crypto.createHmac('sha256', secret).update(data, 'utf8').digest('base64');
}

function buildHeaders(groupKey, groupSecret, requestBody) {
  const bodyStr = JSON.stringify(requestBody);
  const timestamp = Math.floor(Date.now() / 1000).toString(); // ⚠️ 秒级，不是毫秒
  const dataSign = sign(groupSecret, bodyStr);
  const signPayload = `groupKey=${groupKey}&sign=${dataSign}&timestamp=${timestamp}`;
  const signature = sign(groupSecret, signPayload);

  return {
    'Content-Type': 'application/json',
    'GroupKey': groupKey,
    'Timestamp': timestamp,
    'Signature': signature,
  };
}
```

### Python 参考实现（已验证可用）

```python
import hmac, hashlib, base64, time, json

def sign(secret: str, data: str) -> str:
    return base64.b64encode(
        hmac.new(secret.encode(), data.encode(), hashlib.sha256).digest()
    ).decode()

def build_headers(group_key: str, group_secret: str, body: dict) -> dict:
    body_str = json.dumps(body, separators=(',', ':'))
    timestamp = str(int(time.time()))  # 秒级
    data_sign = sign(group_secret, body_str)
    sign_payload = f"groupKey={group_key}&sign={data_sign}&timestamp={timestamp}"
    signature = sign(group_secret, sign_payload)
    return {
        'Content-Type': 'application/json',
        'GroupKey': group_key,
        'Timestamp': timestamp,
        'Signature': signature,
    }
```

---

## 三、创建验真任务

### 请求

```http
POST https://openapi.xhey.top/v2/truth_build/create
Content-Type: application/json
GroupKey: {groupKey}
Timestamp: {timestamp}
Signature: {signature}

{
  "photoUrlList": [
    "https://example.com/photo1.jpg",
    "https://example.com/photo2.jpg"
  ]
}
```

**参数说明：**
- `photoUrlList`：照片 URL 数组，每批最多 10 条，URL 须可公开 GET 访问

### 响应（⚠️ 注意嵌套层级）

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "data": [           // ⚠️ taskID 在 data.data[0]，不是 data 直接下面
      { "taskID": "2036723555890880512" }
    ],
    "status": 0,
    "msg": ""
  },
  "timestamp": 1774427710
}
```

> ⚠️ **坑**：taskID 路径是 `response.data.data[0].taskID`，很多人误以为是 `response.data.taskID`

**取 taskID 的正确写法：**
```javascript
const taskID = res.data?.data?.[0]?.taskID;
```

---

## 四、查询验真结果

### 请求

```http
POST https://openapi.xhey.top/v2/truth_build/query
Content-Type: application/json

{ "taskID": "2036723555890880512" }
```

### 响应（⚠️ 注意字段名）

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskStatus": 5,
    "list": [                // ⚠️ 照片列表字段名是 list，不是 data
      {
        "status": 0,
        "msg": "",
        "photoUrl": "https://...",
        "lat": "40.03479257824713",
        "lng": "116.30887915305028",
        "photoTime": "2026年03月25日 16:52",
        "photoAddress": "北京市海淀区上地街道今日水印相机",
        "antiFakeCode": "..."
      }
    ],
    "status": 0,
    "msg": ""
  },
  "timestamp": 1774427738
}
```

> ⚠️ **坑**：照片列表是 `response.data.list`，不是 `response.data.data`

### taskStatus 含义

| 值 | 含义 | 处理方式 |
|----|------|---------|
| 1 | 待处理 | 继续轮询 |
| 2 | 处理中 | 继续轮询 |
| 5 | **已完成** | 读取 list |
| 6 | 已取消 | 报错退出 |

---

## 五、轮询模式（推荐参数）

API 为异步模式，创建任务后需轮询直到 `taskStatus === 5`。

```javascript
async function pollUntilComplete(taskID, maxRetries = 10, delayMs = 2000) {
  for (let i = 1; i <= maxRetries; i++) {
    const result = await queryTask(taskID);       // result = response.data
    if (result.taskStatus === 5) return result;   // 完成
    if (result.taskStatus === 6) throw new Error('任务已取消');
    if (i < maxRetries) await sleep(delayMs);
  }
  throw new Error(`轮询超时，taskID=${taskID}`);
}
```

**推荐参数：** 最多 10 次 × 2 秒间隔 = 最长等待 20 秒，覆盖绝大多数正常场景。

---

## 六、照片级别错误码

| status | 含义 | 建议处理 |
|--------|------|---------|
| `0` | ✅ 验真通过 | 展示元数据 |
| `-1` | 分辨率过低 | 提示换清晰照片 |
| `-1001` | 网络出错或照片损坏 | 提示检查图片文件 |
| `-1002` | 程序内部错误 | 稍后重试 |
| `-1003` | 未知错误 | 联系技术支持 |
| `-2300` | OCR 启动错误 | 稍后重试 |
| `-2301` | **无防伪码** | 提示非官方水印照片 |
| `-2302` | OCR 识别错误 | 换清晰照片重试 |
| `-2303` | 防伪码长度错误 | 疑似篡改 |
| `-2305` | **非今日水印相机拍摄/无水印** | 最常见的未通过原因 |
| `-2306` | URL 无法访问 | 检查链接有效性 |
| `-2307` | 格式不支持 | 改用 JPG/PNG |
| `-2308` | 分辨率过低 | 换清晰照片 |
| 其他负值 | 验真未通过 | 通用未通过处理 |

---

## 七、HTTP / 业务错误码

| 状态码 | 含义 | 处理方式 |
|--------|------|---------|
| 200 / code=200 | 成功 | 正常处理 |
| 401 / code=401 | 鉴权失败 | 检查签名算法和 Base64 编码 |
| 4007 | 凭证无效或过期 | 联系官方重新获取 Key |
| 400 | 参数错误 | 检查请求体格式 |
| 4009 / 4010 | 参数异常 | 检查 photoUrlList 格式 |
| 500 | 服务端错误 | 照片 URL 不可访问时常见 |

---

## 八、完整调用流程（伪代码）

```
1. 准备凭证
   GROUP_KEY    = env.TRUTU_GROUP_KEY
   GROUP_SECRET = env.TRUTU_GROUP_SECRET

2. 构建签名 Header
   bodyStr   = JSON.stringify({ photoUrlList })
   timestamp = floor(now / 1000)              // 秒
   dataSign  = Base64(HMAC-SHA256(secret, bodyStr))
   payload   = `groupKey=K&sign=D&timestamp=T`
   signature = Base64(HMAC-SHA256(secret, payload))

3. 创建任务
   POST /v2/truth_build/create
   → taskID = response.data.data[0].taskID   // 注意嵌套

4. 轮询查询（最多10次，间隔2s）
   POST /v2/truth_build/query { taskID }
   → 等待 response.data.taskStatus === 5

5. 解析结果
   photos = response.data.list               // 注意字段名 list
   for photo in photos:
     if photo.status === 0  → 通过，取 lat/lng/photoTime/photoAddress
     if photo.status < 0   → 未通过，查错误码表
```

---

## 九、测试用例

| 场景 | URL | 预期 status |
|------|-----|------------|
| 验真**通过** | `https://net-cloud.xhey.top/data/d6aa6870-4bfc-4179-88c1-9914aa0275bd.jpg` | `0`（含完整元数据） |
| 验真**未通过** | `https://net-cloud.xhey.top/data/bdae3a8b-c7ed-49e3-bb31-2800805beb64.png` | `-2301` |

---

## 十、已知限制与注意事项

1. **照片 URL 必须可公开访问**：API 服务器会主动 GET 下载图片，内网/带鉴权的 URL 会返回 500
2. **每批最多 10 张**：超过需分批提交
3. **密钥按月更新**：官方会推送新密钥，需及时更换
4. **无图片上传端点**：API 不接受 base64 或 multipart，只接受 URL
5. **签名时间窗口**：Timestamp 与服务器时间差距过大会导致 401，保持系统时间准确
