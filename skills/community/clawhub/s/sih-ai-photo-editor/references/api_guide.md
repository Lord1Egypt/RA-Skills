# Sih.Ai API 完整指南

## 📡 API Endpoints

### 图片编辑接口

**Endpoint:** `POST https://api.vwu.ai/v1/images/generations/`

**认证方式:** Bearer Token

```http
Authorization: Bearer sk-xxxxx
Content-Type: application/json
```

---

## 📥 请求格式

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | string/array | ✅ | 图片URL或Base64编码 |
| `prompt` | string | ✅ | 编辑指令（自然语言描述） |
| `model` | string | ❌ | 模型名称，默认 `sihai-image-27` |

### 请求示例

```bash
curl --location 'https://api.vwu.ai/v1/images/generations/' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer sk-w4YfLvoXwIEM0I3uNcOOOclfHkBDiR19Md9ixabWv1XMNPhn' \
  --data '{
    "image": ["https://s3.amazonaws.com/sihai2/v2/590789f030495b874f05755d799cf215.JPG"],
    "prompt": "背景改为在海边",
    "model": "sihai-image-27"
  }'
```

---

## 📤 响应格式

### 成功响应

```json
{
  "model": "sihai-image-27",
  "created": 1773386658,
  "data": [
    {
      "url": "https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021773386641671e645a7ebc8dd03740e8d979685c0f6a0d07cb2_0.jpeg?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260313%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260313T072418Z&X-Tos-Expires=86400&X-Tos-Signature=d3d0c33965f7d2eecc3c1f5bdbb83c590c35eca4c73f383d7135f4b8411dd2a2&X-Tos-SignedHeaders=host",
      "size": "2048x2048"
    }
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 16384,
    "total_tokens": 16384
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `model` | string | 使用的模型名称 |
| `created` | int | 生成时间戳 |
| `data[].url` | string | 生成图片的URL |
| `data[].size` | string | 图片尺寸 |
| `usage.generated_images` | int | 生成的图片数量 |
| `usage.output_tokens` | int | 输出token数 |

---

## 🖼️ 图片格式支持

### URL格式

确保图片URL可被公网访问：

```json
{
  "image": ["https://example.com/photo.jpg"]
}
```

### Base64格式

遵循标准格式：`data:image/<格式>;base64,<Base64编码>`

```json
{
  "image": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAA..."]
}
```

**注意事项：**
- `<格式>` 必须小写（`jpeg`、`png`、`webp`）
- Base64编码需完整且正确
- 大图片的Base64可能很长，注意请求体大小限制

---

## 🎯 Prompt 最佳实践

### ✅ 推荐写法

```
"把衣服换成红色连衣裙"
"背景换成海边沙滩，有夕阳"
"转换成日系动漫风格"
"脸换成Angelababy，保持原姿势"
"去掉背景，只保留人物"
```

### ❌ 避免写法

```
"P一下"              # 太模糊
"好看一点"            # 不够具体
"修一修"              # 需要明确修改内容
"弄得漂亮点"          # 主观描述
```

### 💡 技巧

1. **具体描述** - "红色连衣裙" 比 "好看的裙子" 更好
2. **组合操作** - 可同时要求换装+换背景+换风格
3. **保留元素** - "保持原姿势"、"保持面部表情"
4. **风格明确** - "日系动漫"、"美式漫画"、"3D渲染"

---

## 🔐 错误处理

### HTTP状态码

| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常处理响应 |
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 未授权 | 检查API Key |
| 403 | 禁止访问 | 检查权限 |
| 429 | 请求过于频繁 | 降低请求频率 |
| 500 | 服务器错误 | 稍后重试 |

### 错误响应示例

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

---

## ⚙️ 高级参数（待实现）

以下参数可能在API中存在，需要确认：

### 尺寸控制
```json
{
  "size": "1024x1024"  // 输出尺寸
}
```

### 质量控制
```json
{
  "quality": "high"  // 生成质量
}
```

### 批量处理
```json
{
  "image": [
    "https://example.com/1.jpg",
    "https://example.com/2.jpg"
  ],
  "prompt": "统一换成动漫风格"
}
```

---

## 🧪 测试用例

### 测试1：换装
```bash
curl -X POST 'https://api.vwu.ai/v1/images/generations/' \
  -H 'Authorization: Bearer sk-xxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
    "image": ["https://example.com/person.jpg"],
    "prompt": "把衣服换成白色婚纱"
  }'
```

### 测试2：换背景
```bash
curl -X POST 'https://api.vwu.ai/v1/images/generations/' \
  -H 'Authorization: Bearer sk-xxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
    "image": ["https://example.com/person.jpg"],
    "prompt": "背景换成咖啡厅"
  }'
```

### 测试3：风格转换
```bash
curl -X POST 'https://api.vwu.ai/v1/images/generations/' \
  -H 'Authorization: Bearer sk-xxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
    "image": ["https://example.com/person.jpg"],
    "prompt": "转换成动漫风格"
  }'
```

---

## 💡 常见问题

### Q1: 图片URL无法访问
**A:** 确保图片URL可公网访问，不要使用本地URL或需要授权的URL

### Q2: Base64格式错误
**A:** 检查格式是否为 `data:image/jpeg;base64,<编码>`，注意格式名小写

### Q3: 处理时间过长
**A:** 复杂操作（换脸、风格转换）可能需要30-60秒，设置合理的超时时间

### Q4: 生成结果不符合预期
**A:** 优化prompt描述，使用更具体、清晰的语言

### Q5: 如何获取API Key
**A:** 访问 https://sih.ai 注册账号并获取API Key

---

## 📞 技术支持

- **官网:** https://sih.ai
- **文档:** https://docs.sih.ai
- **邮箱:** support@sih.ai
- **微信群:** [加入技术交流群]

---

**最后更新:** 2026-03-13
