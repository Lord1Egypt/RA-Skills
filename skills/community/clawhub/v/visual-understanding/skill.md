---
name: glm-4.6v-vision-connector
description: "智谱 GLM-4.6V 多模态视觉模型集成插件。支持本地图像解析（Base64）及公网链接读取。优先提供 zai SDK 接入，并包含 cURL 原生降级方案。"
version: "1.1.0"
homepage: "https://github.com/zai-org/GLM-V"
repository: "https://github.com/zai-org/GLM-V.git"
authors: ["IsabellaZhangYM"]
license: "MIT"

requirements:
  environment_variables:
    - ZHIPUAI_API_KEY
  dependencies:
    python:
      - "zai"
  install_command: "pip install zai"

credentials:
  ZHIPUAI_API_KEY:
    description: "智谱 AI 开放平台 (bigmodel.cn) API Key"
    required: true
    source: "environment_variable"
---

# 👁️ GLM-4.6V 图像理解集成指南

本 Skill 为开发者提供接入智谱 GLM-4.6V 视觉大模型的能力，支持精准的图像内容描述、多图对比及信息提取。

## 🛡️ 安全与数据合规

1. **凭据安全**：禁止硬编码 API Key，必须通过环境变量 `ZHIPUAI_API_KEY` 读取。
2. **隐私提醒**：使用 Base64 上传本地图片时，请确保已脱敏处理图片中的个人隐私信息（PII）或机密数据。

---

## 🚀 方式一：Python SDK 请求（⭐️ 推荐）

**适用场景**：已安装 Python 环境，且需要处理**本地图片**（通过 Base64 编码上传）。此方式最稳定且支持高级应用封装。

### 1. 安装依赖
```bash
pip install zai
```



## 2. 调用代码示例

```python
import os
import base64
from zai import ZhipuAiClient

# 安全规范：通过环境变量读取凭据
client = ZhipuAiClient(api_key=os.environ.get("ZHIPUAI_API_KEY"))

def encode_image(image_path):
    """将本地图像编码为 base64 格式"""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================
# 场景 A：使用公网图像 URL
# ==========================================
response_url = client.chat.completions.create(
    model="glm-4.6v",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这张图片里有什么？请详细描述。"},
            {"type": "image_url", "image_url": {"url": "[https://example.com/image.jpg](https://example.com/image.jpg)"}}
        ]
    }]
)
print("URL 解析结果:", response_url.choices[0].message.content)

# ==========================================
# 场景 B：使用本地图片 (Base64)
# ==========================================
local_image_path = 'path/to/your/image.jpg'
if os.path.exists(local_image_path):
    base64_image = encode_image(local_image_path)
    response_base64 = client.chat.completions.create(
        model="glm-4.6v",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "分析这张图片中的内容"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }]
    )
    print("本地图片解析结果:", response_base64.choices[0].message.content)
```

------

## ⚡ 方式二：cURL 原生请求（降级方案）

**适用场景**：受限环境（如 CI/CD 管道、轻量级容器），**无法安装 `zai` SDK**。

- **注意**：此方式不支持直接上传本地文件，图片必须具备可公开访问的**公网下载地址 (URL)**。

## 调用示例（支持多图对比）

请在终端中执行，系统将自动读取已配置的 `$ZHIPUAI_API_KEY` 环境变量：



```bash
curl --request POST \
  --url [https://open.bigmodel.cn/api/paas/v4/chat/completions](https://open.bigmodel.cn/api/paas/v4/chat/completions) \
  --header "Authorization: Bearer $ZHIPUAI_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "glm-4.6v",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "[https://cdn.bigmodel.cn/static/logo/register.png](https://cdn.bigmodel.cn/static/logo/register.png)"
            }
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "[https://cdn.bigmodel.cn/static/logo/api-key.png](https://cdn.bigmodel.cn/static/logo/api-key.png)"
            }
          },
          {
            "type": "text",
            "text": "What are the pics talk about?"
          }
        ]
      }
    ]
  }'
```

------

## 💡 最佳实践与避坑指南

| **请求方式** | **优点**                                     | **局限性**                                   |
| ------------ | -------------------------------------------- | -------------------------------------------- |
| **zai SDK**  | 支持本地图片、易于与 RAG 或 Agent 工作流集成 | 需要 Python 环境及 `pip install` 权限        |
| **cURL**     | 零依赖，随处可用，非常适合自动化 Shell 脚本  | 只能读取公网图床，本地图片需自行搭建图床中转 |

