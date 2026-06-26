# Seedream API 参考文档

## 平台信息

- **平台**: 火山引擎 方舟大模型服务平台
- **API Endpoint**: `https://ark.cn-beijing.volces.com/api/v3`
- **鉴权方式**: API Key（环境变量 `ARK_API_KEY`）
- **官方文档**: https://www.volcengine.com/docs/82379

---

## 可用模型

| 模型名称 | Model ID | 能力 | 说明 |
|---------|---------|------|------|
| Seedream 3.0 | `doubao-seedream-3-0-t2i-250415` | 文生图 | 推荐，高质量，中英双语 |
| Seedream 4.0 | `doubao-seedream-4-0-250828` | 文生图 + 图生图 | 支持多图融合 |
| Seedream 4.5 | `doubao-seedream-4-5-251128` | 文生图 + 图生图 | 最新，能力最强 |
| Seedream 5.0 Lite | `doubao-seedream-5-0-lite` | 文生图 | 极速，轻量 |

---

## 请求参数

### POST `/images/generations`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | Model ID |
| `prompt` | string | ✅ | 提示词，支持中英文，建议 ≤300 汉字或 600 英文单词 |
| `n` | integer | ❌ | 生成图片数量，默认 1 |
| `size` | string | ❌ | 图片分辨率，如 `1024x1024`、`1792x1024`、`2048x2048`（4.0+支持 4K） |
| `response_format` | string | ❌ | `url`（默认，24h有效）或 `b64_json` |
| `image` | string/array | ❌ | 参考图（URL 或 Base64），3.0 不支持，4.0+ 支持图生图 |
| `watermark` | boolean | ❌ | 是否添加水印，默认 false |

---

## 响应格式

```json
{
  "created": 1700000000,
  "data": [
    {
      "url": "https://...",           // response_format=url 时返回，24h有效
      "b64_json": "...",              // response_format=b64_json 时返回
      "size": "1024x1024"
    }
  ],
  "usage": {
    "total_tokens": 100
  }
}
```

---

## 安装依赖

### 方式一：官方 SDK（推荐）
```bash
pip install 'volcengine-python-sdk[ark]'
```

### 方式二：OpenAI 兼容
```bash
pip install openai
```

---

## 代码示例

### 官方 SDK（Python）
```python
import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.environ.get("ARK_API_KEY"))

resp = client.images.generate(
    model="doubao-seedream-3-0-t2i-250415",
    prompt="一只可爱的橘猫坐在窗边看夕阳",
    n=1,
    response_format="url",
    # size="1024x1024",  # 可选
)

print(resp.data[0].url)
```

### OpenAI 兼容（Python）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

resp = client.images.generate(
    model="doubao-seedream-3-0-t2i-250415",
    prompt="一只可爱的橘猫坐在窗边看夕阳",
)

print(resp.data[0].url)
```

### cURL
```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedream-3-0-t2i-250415",
    "prompt": "一只可爱的橘猫坐在窗边看夕阳",
    "n": 1,
    "response_format": "url"
  }'
```

---

## 提示词建议

- **中英文均支持**，中文描述更直接，英文描述细节控制力更强
- **描述主体**：先描述主要内容，再描述风格、光线、构图
- **字数建议**：≤300 汉字或 600 英文单词，过长反而影响效果
- **风格关键词**：`电影感`、`赛博朋克`、`水彩画`、`写实摄影`、`动漫风格`、`油画`
- **质量关键词**：`高清`、`8K`、`超细节`、`photorealistic`

---

## 获取 API Key

1. 前往 https://console.volcengine.com/ark
2. 注册/登录火山引擎账号
3. 在「API Key」页面创建 Key
4. 在「开通管理」页面开通所需模型
