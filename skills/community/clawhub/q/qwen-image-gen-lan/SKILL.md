---
name: qwen-image-gen
description: 阿里云千问文生图模型（Qwen-Image）技能，支持图像生成。当用户要求AI生成图片、画图、文生图、text-to-image，或提到千问、阿里云生图时使用。支持中英文提示词，可指定画面尺寸、风格参数等。
---

# 千问文生图技能 (qwen-image-gen)

## 快速使用

### 基本文生图（同步接口，推荐）

使用 `qwen-image-2.0-pro` 模型（效果最佳）：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "qwen-image-2.0-pro",
    "input": {
      "messages": [{
        "role": "user",
        "content": [{"text": "你的提示词"}]
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

### 可用模型

| 模型 | 特点 | 推荐场景 |
|------|------|---------|
| `qwen-image-2.0-pro` | 效果最好，文字渲染强 | **首选** |
| `qwen-image-2.0` | 速度快，效果均衡 | 加速场景 |
| `qwen-image-max` | 真实感最强 | 写实摄影 |
| `qwen-image-plus` | 价格优惠 | 常规使用 |

### 常用参数

| 参数 | 说明 | 默认值 |
|------|------|-------|
| `size` | 分辨率，格式 `宽*高` | `2048*2048` |
| `n` | 生成数量（2.0系列1-6张，其他1张） | 1 |
| `prompt_extend` | 智能优化提示词 | `true` |
| `watermark` | 添加水印 | `false` |
| `negative_prompt` | 反向提示词 | - |
| `seed` | 随机种子（0-2147483647） | 随机 |

### 推荐分辨率

**qwen-image-2.0系列：**
- `2048*2048` - 1:1 方图（默认）
- `2688*1536` - 16:9 宽屏
- `1536*2688` - 9:16 竖屏
- `2368*1728` - 4:3
- `1728*2368` - 3:4

**qwen-image-max / plus系列：**
- `1664*928` - 16:9（默认）
- `1328*1328` - 1:1
- `928*1664` - 9:16
- `1472*1104` - 4:3
- `1104*1472` - 3:4

## 执行流程

1. **检查 API Key**：确保 `DASHSCOPE_API_KEY` 环境变量已设置
2. **构建请求**：根据用户提示词和参数构建 JSON 请求
3. **调用 API**：使用 curl 发送同步请求
4. **解析结果**：从响应中提取图像 URL
5. **返回结果**：将图像 URL 返回给用户

## 响应示例

成功时返回：
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
    "height": 2048,
    "image_count": 1,
    "width": 2048
  },
  "request_id": "xxx"
}
```

**注意**：图像 URL 有效期 24 小时，请及时保存！

## 错误处理

常见错误码：
- `InvalidApiKey` - API Key 无效或未设置
- `InvalidParameter` - 参数错误
- `RateLimitExceed` - 请求过于频繁

## 参考资料

详细 API 文档和异步接口说明请参阅 [references/api.md](references/api.md)
