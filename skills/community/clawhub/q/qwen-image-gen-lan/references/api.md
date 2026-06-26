# 千问文生图 API 详细参考

## 基本信息

- **北京地域 endpoint**: `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **新加坡地域 endpoint**: `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **注意**: 北京和新加坡的 API Key 不可混用

## 环境变量

```bash
export DASHSCOPE_API_KEY="your-api-key-here"
```

获取 API Key: https://help.aliyun.com/zh/model-studio/get-api-key

## 同步接口（推荐）

### 请求头

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Content-Type | string | 是 | 固定值 `application/json` |
| Authorization | string | 是 | 格式 `Bearer $DASHSCOPE_API_KEY` |

### 请求体

```json
{
  "model": "qwen-image-2.0-pro",
  "input": {
    "messages": [{
      "role": "user",
      "content": [{
        "text": "你的提示词（最多800字符）"
      }]
    }]
  },
  "parameters": {
    "negative_prompt": "反向提示词（最多500字符）",
    "prompt_extend": true,
    "watermark": false,
    "size": "2048*2048",
    "n": 1,
    "seed": 12345
  }
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 模型名：`qwen-image-2.0-pro`, `qwen-image-2.0`, `qwen-image-max`, `qwen-image-plus` |
| input.messages[].content[].text | string | 是 | 正向提示词，中英文均可，最多800字符 |
| parameters.negative_prompt | string | 否 | 反向提示词，描述不希望出现的内容 |
| parameters.size | string | 否 | 输出分辨率，默认 `2048*2048` |
| parameters.n | integer | 否 | 生成数量，2.0系列1-6，其他固定1 |
| parameters.prompt_extend | boolean | 否 | 开启智能提示词优化，默认 true |
| parameters.watermark | boolean | 否 | 添加水印，默认 false |
| parameters.seed | integer | 否 | 随机种子，范围 [0, 2147483647] |

## 完整 curl 示例

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "qwen-image-2.0-pro",
    "input": {
      "messages": [{
        "role": "user",
        "content": [{
          "text": "一只橘黄色的猫坐在窗台上，阳光照射进来，温暖舒适"
        }]
      }]
    },
    "parameters": {
      "negative_prompt": "低分辨率，低画质，肢体畸形，手指畸形",
      "prompt_extend": true,
      "watermark": false,
      "size": "2048*2048"
    }
  }'
```

## 响应格式

### 成功响应

```json
{
  "output": {
    "choices": [{
      "finish_reason": "stop",
      "message": {
        "content": [{
          "image": "https://dashscope-result-xxx.png?Expires=xxx"
        }]
      }
    }]
  },
  "usage": {
    "image_count": 1,
    "width": 2048,
    "height": 2048
  },
  "request_id": "d0250a3d-b07f-49e1-bdc8-xxx"
}
```

### 错误响应

```json
{
  "request_id": "a4d78a5f-655f-9639-xxx",
  "code": "InvalidParameter",
  "message": "num_images_per_prompt must be 1"
}
```

## 异步接口（如需使用）

异步接口需两步：
1. 创建任务获取 task_id
2. 轮询查询结果

### 创建任务

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen-image-plus",
    "input": {
      "prompt": "你的提示词"
    },
    "parameters": {
      "size": "1664*928",
      "n": 1,
      "prompt_extend": true,
      "watermark": false
    }
  }'
```

### 查询任务

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| InvalidApiKey | API Key 无效 | 检查 DASHSCOPE_API_KEY 是否正确 |
| InvalidParameter | 参数错误 | 检查请求参数格式和取值范围 |
| RateLimitExceed | 限流 | 降低请求频率 |
| UnsupportedModel | 不支持的模型 | 使用支持的模型名称 |
| InternalError | 内部错误 | 重试或联系支持 |
