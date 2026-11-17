# 腾讯 ima OpenAPI 参考

> 信息来源：ima.qq.com 官方 agent-interface 页面 + 腾讯云开发者社区实测文章。
> 最后核验日期：2026-10-06。如果 ima 改版导致字段变化，以官方文档为准。

## 0. 前置准备

用户必须在 https://ima.qq.com/agent-interface 完成：
1. 登录 ima 网页版
2. 点击「生成 API Key」
3. 拿到 `ClientID` 和 `APIKey`

还需要：
- `knowledge_base_id`：进入目标知识库，URL 中可找到
- `folder_id`：目标文件夹 ID（可选）

**安全提醒**：API Key 等同账号读写权限，任务结束提醒用户轮换。

---

## 1. 认证方式

所有请求加两个 Header：
```
ima-openapi-clientid: <ClientID>
ima-openapi-apikey: <APIKey>
Content-Type: application/json
```

---

## 2. 上传文件三步曲

### Step 1：create_media（申请上传凭证）

```
POST https://ima.qq.com/openapi/wiki/v1/create_media
```

请求体：
```json
{
  "file_name": "20260815-张三-合同v2.docx",
  "file_size": 102400,
  "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "knowledge_base_id": "<你的知识库ID>",
  "file_ext": "docx"
}
```

关键参数：
| 字段 | 说明 |
|---|---|
| file_name | 文件名（带扩展名） |
| file_size | 字节数（整数） |
| content_type | MIME 类型 |
| knowledge_base_id | 目标知识库 |
| file_ext | 不带点的扩展名 |

返回（关键字段）：
- `media_id`：后续 add_knowledge 要用
- 临时 COS 上传凭证（临时密钥 + 上传地址）

### Step 2：上传文件到 COS

用 Step 1 返回的临时凭证，按 COS 规范 PUT 文件到指定地址。
（脚本里用 `cos-python-sdk-v5` 或直接按返回的 POST 表单字段提交。）

### Step 3：add_knowledge（登记到知识库）

```
POST https://ima.qq.com/openapi/wiki/v1/add_knowledge
```

请求体：
```json
{
  "media_type": 11,
  "title": "20260815-张三-合同v2",
  "knowledge_base_id": "<你的知识库ID>",
  "folder_id": "<目标文件夹ID，可选>",
  "media_id": "<Step 1 返回的 media_id>",
  "note_info": {
    "source": "微信归档",
    "contact": "张三",
    "date": "2026-08-15"
  }
}
```

关键字段：
| 字段 | 说明 |
|---|---|
| media_type | 11 = 文件（其他类型见 ima 官方枚举） |
| title | 知识库中显示的标题 |
| media_id | Step 1 返回 |
| note_info | 自定义元数据，会作为附件属性入库 |

---

## 3. 限制与配额

| 项 | 限制 |
|---|---|
| 单文件大小 | ≤ 50 MB |
| PDF 页数 | ≤ 1000 页（超出会上传失败） |
| 调用频率 | 建议 QPS ≤ 1，脚本内置 1 秒间隔 |
| 支持格式 | PDF / Word / PPT / Excel / Markdown / 图片 / 音频 等 19 种 |

---

## 4. 常见错误码

| HTTP | 含义 | 处理 |
|---|---|---|
| 401 | ClientID / APIKey 错或过期 | 让用户去 ima 后台重新生成 |
| 403 | 无权限（知识库 ID 错） | 核对 knowledge_base_id |
| 404 | 接口路径变了 | 查官方文档最新路径 |
| 413 | 文件过大 | 拆小再传 |
| 429 | 限流 | 加大间隔到 2~3 秒 |
| 500/502 | ima 服务端问题 | 退避重试 3 次 |

---

## 5. 调用示例（curl 伪代码）

```bash
# Step 1
curl -X POST "https://ima.qq.com/openapi/wiki/v1/create_media" \
  -H "Content-Type: application/json" \
  -H "ima-openapi-clientid: $CLIENT_ID" \
  -H "ima-openapi-apikey: $API_KEY" \
  -d '{"file_name":"合同.docx","file_size":102400,"content_type":"application/octet-stream","knowledge_base_id":"KB_ID","file_ext":"docx"}'

# （Step 2 走 COS SDK，略）

# Step 3
curl -X POST "https://ima.qq.com/openapi/wiki/v1/add_knowledge" \
  -H "Content-Type: application/json" \
  -H "ima-openapi-clientid: $CLIENT_ID" \
  -H "ima-openapi-apikey: $API_KEY" \
  -d '{"media_type":11,"title":"合同","knowledge_base_id":"KB_ID","media_id":"MEDIA_ID"}'
```
