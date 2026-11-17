# Z.ai GLM-4.1V-thinking-flash API 规范文档

## 概述

本文档详细描述 Z.ai GLM-4.1V-thinking-flash 模型的 API 调用规范。所有参数为固定值，**严禁修改**，确保调用一致性和可复现性。

---

## 端点信息

| 项目 | 值 |
|------|-----|
| **Base URL** | `https://open.bigmodel.cn/api/paas/v4` |
| **Endpoint** | `/chat/completions` |
| **Method** | `POST` |
| **Protocol** | HTTPS |
| **Content-Type** | `application/json` |
| **Authentication** | Bearer Token (API Key) |

---

## 请求头

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

| Header | 必需 | 说明 |
|--------|------|------|
| `Authorization` | ✅ | `Bearer ` + API Key |
| `Content-Type` | ✅ | 固定 `application/json` |

---

## 请求体参数（固定，不可修改）

```json
{
  "model": "glm-4.1v-thinking-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "<IMAGE_URL>"
          }
        },
        {
          "type": "text",
          "text": "<PROMPT_TEXT>"
        }
      ]
    }
  ],
  "stream": false,
  "do_sample": true,
  "temperature": 0.8,
  "top_p": 0.6,
  "max_tokens": 4096,
  "tool_choice": "auto"
}
```

### 字段详细说明

| 字段 | 类型 | 固定值 | 说明 |
|------|------|--------|------|
| `model` | string | `"glm-4.1v-thinking-flash"` | **模型名称，严禁修改** |
| `messages` | array | 见结构 | 消息数组，仅支持单轮 user 消息 |
| `messages[0].role` | string | `"user"` | 角色固定为 user |
| `messages[0].content` | array | 见结构 | 多模态内容数组：先 image_url 后 text |
| `messages[0].content[0].type` | string | `"image_url"` | 内容类型：图片 |
| `messages[0].content[0].image_url.url` | string | **动态** | 图片公网访问 URL |
| `messages[0].content[1].type` | string | `"text"` | 内容类型：文本 |
| `messages[0].content[1].text` | string | **动态** | 分析提示词 |
| `stream` | boolean | `false` | **非流式输出，严禁改为 true** |
| `do_sample` | boolean | `true` | 启用采样 |
| `temperature` | number | `0.8` | 采样温度，控制随机性 |
| `top_p` | number | `0.6` | 核采样概率阈值 |
| `max_tokens` | integer | `4096` | 最大输出 token 数 |
| `tool_choice` | string | `"auto"` | 工具选择策略 |

---

## 图片要求

| 限制项 | 规格 |
|--------|------|
| **大小** | ≤ 5 MB |
| **分辨率** | ≤ 6000 × 6000 像素 |
| **格式** | JPG、PNG、JPEG |
| **数量** | 单次请求仅支持 **1 张** |
| **编码** | **支持两种方式**：
  1. **公网 URL**（官方推荐）
  2. **Base64 Data URL**（本 skill 扩展支持，格式：`data:image/xxx;base64,xxx`） |
| **访问性** | 必须为公网可直接访问的 HTTP/HTTPS URL |

### 支持的图片托管方式
- 对象存储（OSS、S3、COS 等）生成的签名 URL
- 图床服务（Imgur、SM.MS、GitHub Raw 等）
- 自建 CDN/静态资源服务器
- **Base64 Data URL**（本 skill 扩展支持，自动将本地文件转换）
- **不支持**：本地文件路径、需要登录/鉴权的私有链接

---

## 响应格式

### 成功响应 (HTTP 200)

```json
{
  "id": "chatcmpl-xxxxxxxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "glm-4.1v-thinking-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "模型生成的分析文本内容...",
        "tool_calls": null
      },
      "finish_reason": "stop",
      "logprobs": null
    }
  ],
  "usage": {
    "prompt_tokens": 1234,
    "completion_tokens": 567,
    "total_tokens": 1801
  }
}
```

### 关键字段提取

| 字段 | 路径 | 说明 |
|------|------|------|
| 分析结果文本 | `choices[0].message.content` | **核心输出**，传递给主模型进一步处理 |
| 总 token 消耗 | `usage.total_tokens` | 计费依据 |
| 输入 token | `usage.prompt_tokens` | 包含图片 token |
| 输出 token | `usage.completion_tokens` | 模型生成的 token |
| 请求 ID | `id` | 用于问题排查 |
| 结束原因 | `choices[0].finish_reason` | `stop`=正常结束、`length`=截断 |

### 错误响应 (非 200)

```json
{
  "error": {
    "message": "错误描述",
    "type": "错误类型",
    "code": "错误码",
    "param": "相关参数名"
  }
}
```

---

## 完整调用示例

### cURL

```bash
curl -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.1v-thinking-flash",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "https://example.com/image.jpg"
            }
          },
          {
            "type": "text",
            "text": "请详细描述这张图片的内容"
          }
        ]
      }
    ],
    "stream": false,
    "do_sample": true,
    "temperature": 0.8,
    "top_p": 0.6,
    "max_tokens": 4096,
    "tool_choice": "auto"
  }'
```

### Python (requests)

```python
import requests
import json

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "YOUR_API_KEY"

payload = {
    "model": "glm-4.1v-thinking-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
                {"type": "text", "text": "请详细描述这张图片的内容"}
            ]
        }
    ],
    "stream": False,
    "do_sample": True,
    "temperature": 0.8,
    "top_p": 0.6,
    "max_tokens": 4096,
    "tool_choice": "auto"
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, timeout=60)
result = response.json()

if response.status_code == 200:
    content = result["choices"][0]["message"]["content"]
    print("分析结果:", content)
    print("Token 使用:", result["usage"])
else:
    print("错误:", result.get("error", "Unknown error"))
```

### Node.js (fetch)

```javascript
const apiKey = "YOUR_API_KEY";
const imageUrl = "https://example.com/image.jpg";
const prompt = "请详细描述这张图片的内容";

const payload = {
  model: "glm-4.1v-thinking-flash",
  messages: [
    {
      role: "user",
      content: [
        { type: "image_url", image_url: { url: imageUrl } },
        { type: "text", text: prompt }
      ]
    }
  ],
  stream: false,
  do_sample: true,
  temperature: 0.8,
  top_p: 0.6,
  max_tokens: 4096,
  tool_choice: "auto"
};

const response = await fetch("https://open.bigmodel.cn/api/paas/v4/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${apiKey}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
});

const result = await response.json();

if (response.ok) {
  console.log("分析结果:", result.choices[0].message.content);
  console.log("Token 使用:", result.usage);
} else {
  console.error("错误:", result.error);
}
```

---

## 参数调整说明（重要）

### ⚠️ 以下参数为固定值，**严禁修改**：

| 参数 | 固定值 | 修改后果 |
|------|--------|----------|
| `model` | `glm-4.1v-thinking-flash` | 模型不存在或调用其他模型 |
| `stream` | `false` | 流式输出格式不兼容，解析失败 |
| `temperature` | `0.8` | 影响输出质量和一致性 |
| `top_p` | `0.6` | 影响采样分布 |
| `max_tokens` | `4096` | 可能截断输出或浪费配额 |
| `tool_choice` | `auto` | 影响工具调用行为 |
| `messages` 结构 | 单轮 user + image_url + text | 多轮/角色变更导致错误 |

### ✅ 允许动态变化的字段：

| 字段 | 来源 | 说明 |
|------|------|------|
| `messages[0].content[0].image_url.url` | 用户提供 | 图片 URL |
| `messages[0].content[1].text` | 根据任务构建 | 分析提示词 |

---

## 计费与配额

### Token 计算
- **图片 Token**：约 256-1024 tokens/张（视分辨率而定）
- **文本 Token**：按字符/词切分计算
- **总消耗** = `prompt_tokens` + `completion_tokens`

### 限制配额（以控制台为准）
- **QPS**（每秒查询数）：根据套餐限制
- **TPM**（每分钟 Token 数）：根据套餐限制
- **并发请求数**：根据套餐限制
- **日/月调用量**：根据套餐限制

### 超限处理
- 返回 `429 Too Many Requests` 或错误码 `RATE_LIMIT_EXCEEDED`
- 响应头包含 `Retry-After`（秒数）
- 客户端应实现指数退避重试和限流队列

---

## 最佳实践

### 1. 图片预处理
- 上传前压缩至 < 5MB
- 长边压缩至 ≤ 2000px 可显著降低 token 消耗
- 确保 URL 稳定、访问速度快（推荐 CDN）

### 2. 提示词工程
- 明确任务类型：描述/提取/分析/推理
- 指定输出格式：自然语言/JSON/Markdown 表格/结构化列表
- 提供示例：few-shot 提示显著提升准确率
- 设置约束：长度限制、必须字段、不确定标注

### 3. 错误处理
- 区分可重试/不可重试错误（见 error-codes.md）
- 记录请求 ID 便于排查
- 实现熔断机制防止级联失败

### 4. 成本控制
- 批量任务使用异步队列，避免并发超限
- 监控 token 消耗趋势
- 缓存相同图片的重复分析结果

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2026-07-29 | 初始版本，基于 GLM-4.1V-thinking-flash 官方文档 |

---

## 相关链接

- [Z.ai 开放平台控制台](https://open.bigmodel.cn/)
- [API 文档中心](https://open.bigmodel.cn/dev/api)
- [错误码完整列表](./error-codes.md)
- [提示词编写指南](./prompt-guide.md)