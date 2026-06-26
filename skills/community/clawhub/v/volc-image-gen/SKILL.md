# volc-image-gen - 火山引擎图像生成技能

⚡ 基于火山引擎方舟平台的 AI 图像生成技能，支持文生图、图生图、批量生成和变体生成。

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/node/openclaw-skills/volc-image-gen
npm install
```

### 2. 配置环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export VOLC_API_KEY="your_volc_api_key"
export VOLC_API_BASE="https://ark.cn-beijing.volces.com/api/v3"
export VOLC_IMAGE_MODEL="doubao-image-x"

# 使配置生效
source ~/.bashrc
```

### 3. 获取 API Key

访问 [火山引擎方舟控制台](https://console.volcengine.com/ark) 获取 API Key。

---

## 📋 命令列表

### 文生图

```json
{
  "command": "generate",
  "params": {
    "prompt": "一只可爱的猫咪，高清，写实风格",
    "size": "1024x1024",
    "n": 1,
    "style": "realistic",
    "negative_prompt": ""
  }
}
```

**参数说明：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | ✅ | 图片描述 |
| size | string | ❌ | 尺寸，默认 1024x1024 |
| n | number | ❌ | 生成数量，默认 1 |
| style | string | ❌ | 风格（见下方风格列表） |
| negative_prompt | string | ❌ | 负面提示词 |

### 图生图

```json
{
  "command": "edit",
  "params": {
    "image": "/path/to/image.png",
    "prompt": "将猫咪换成狗狗",
    "strength": 0.7,
    "size": "1024x1024"
  }
}
```

**参数说明：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | string | ✅ | 输入图片（URL 或本地路径） |
| prompt | string | ✅ | 编辑描述 |
| strength | number | ❌ | 重绘强度 0-1，默认 0.7 |
| size | string | ❌ | 输出尺寸 |

### 批量生成

```json
{
  "command": "batch",
  "params": {
    "prompts": ["一只猫咪", "一只狗狗", "一只兔子"],
    "concurrent": 3,
    "size": "1024x1024",
    "style": "realistic"
  }
}
```

### 生成变体

```json
{
  "command": "variations",
  "params": {
    "image": "/path/to/image.png",
    "n": 5,
    "strength": 0.5,
    "size": "1024x1024"
  }
}
```

---

## 🎨 可用风格

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| `realistic` | 写实风格，高清，高质量 | 产品摄影、人像、风景 |
| `anime` | 动漫风格，二次元，精美 | 动漫角色、插画 |
| `oil` | 油画风格，艺术感，厚重 | 艺术作品、装饰画 |
| `watercolor` | 水彩风格，清新，透明感 | 清新插画、背景 |
| `sketch` | 素描风格，线条感，黑白 | 草图、线稿 |
| `cyberpunk` | 赛博朋克风格，霓虹灯，未来感 | 科幻场景、未来城市 |
| `fantasy` | 奇幻风格，魔法，梦幻 | 奇幻场景、魔法效果 |

---

## 📐 支持尺寸

- 512x512
- 512x768
- 768x512
- 768x768
- 1024x1024
- 1024x1536
- 1536x1024

---

## 💡 使用示例

### 示例 1：生成写实风格猫咪

```javascript
const { execute } = require('./src/index');

const result = await execute({
  command: 'generate',
  params: {
    prompt: '一只可爱的猫咪在阳光下玩耍',
    style: 'realistic',
    size: '1024x1024'
  }
});

console.log(result);
```

### 示例 2：生成动漫风格头像

```javascript
const result = await execute({
  command: 'generate',
  params: {
    prompt: '一个可爱的女孩，大眼睛，长发',
    style: 'anime',
    n: 4
  }
});
```

### 示例 3：批量生成产品图

```javascript
const result = await execute({
  command: 'batch',
  params: {
    prompts: [
      '白色 T 恤，简约设计',
      '蓝色牛仔裤，休闲风格',
      '黑色运动鞋，时尚款式'
    ],
    concurrent: 3,
    style: 'realistic'
  }
});

console.log(`成功：${result.successful}, 失败：${result.failed}`);
```

### 示例 4：图片编辑

```javascript
const result = await execute({
  command: 'edit',
  params: {
    image: 'https://example.com/input.png',
    prompt: '将背景换成海滩',
    strength: 0.6
  }
});
```

---

## 📊 返回结果格式

### 成功响应

```json
{
  "success": true,
  "images": [
    {
      "url": "https://xxx.volces.com/xxx.png",
      "local_path": "/tmp/openclaw/volc_1712000000_abc123.png",
      "prompt": "一只可爱的猫咪",
      "size": "1024x1024",
      "style": "realistic",
      "index": 1
    }
  ],
  "usage": {
    "tokens": 100,
    "cost": 0.12,
    "model": "doubao-image-x"
  }
}
```

### 错误响应

```json
{
  "success": false,
  "error": "鉴权失败 (401) - 请检查 VOLC_API_KEY 是否正确",
  "code": 401
}
```

---

## ⚙️ 高级配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VOLC_API_KEY` | 火山引擎 API Key（必填） | - |
| `VOLC_API_BASE` | API 基础 URL | `https://ark.cn-beijing.volces.com/api/v3` |
| `VOLC_IMAGE_MODEL` | 图像模型 | `doubao-image-x` |

### 缓存机制

- 内置 1 小时缓存，相同参数不会重复调用 API
- 缓存键基于 prompt + 参数生成
- 可通过 `useCache: false` 禁用缓存

### 重试策略

- 默认最大重试 3 次
- 指数退避：1s → 2s → 4s
- 401/400 错误不重试，429/5xx 错误重试

---

## 🧪 测试

```bash
# 运行单元测试
npm test

# 或手动测试
node tests/image-gen.test.js
```

---

## ⚠️ 常见问题

### 1. 鉴权失败 (401)

**原因：** API Key 配置错误  
**解决：** 检查 `VOLC_API_KEY` 环境变量是否正确设置

### 2. 参数错误 (400)

**原因：** prompt 或 size 参数不合法  
**解决：** 检查参数格式和取值范围

### 3. API 限流 (429)

**原因：** 请求频率过高  
**解决：** 降低并发数或稍后重试

### 4. 图片下载失败

**原因：** 网络问题或 URL 失效  
**解决：** 检查网络连接，重试请求

---

## 📝 更新日志

### v1.0.0 (2026-04-01)

- ✨ 初始版本发布
- 🎨 支持文生图、图生图、批量生成、变体生成
- 🎭 7 种预定义风格
- 🔄 智能重试机制（指数退避）
- 💾 自动缓存（1 小时）
- ⚡ 并发控制（p-limit）
- 🧪 完整单元测试

---

## 🔗 相关链接

- [火山引擎方舟文档](https://www.volcengine.com/docs/82379)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/rfdiosuao/openclaw-skills)

---

**版本：** 1.0.0  
**许可：** MIT  
**作者：** OpenClaw Skill Master
