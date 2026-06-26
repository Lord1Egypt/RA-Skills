# volc-image-gen

🎨 火山引擎图像生成技能 - 基于火山引擎方舟平台的 AI 图像生成工具

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/rfdiosuao/openclaw-skills/tree/main/volc-image-gen)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

---

## 📖 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [API 参考](#-api-参考)
- [配置说明](#-配置说明)
- [示例代码](#-示例代码)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)

---

## ✨ 功能特性

### 核心功能

- 🎨 **文生图** - 根据文本描述生成高质量图片
- 🖼️ **图生图** - 基于现有图片进行编辑和重绘
- 📦 **批量生成** - 支持并发批量生成多张图片
- 🔄 **变体生成** - 为图片生成多个相似变体

### 技术特性

- 🎭 **7 种风格** - 写实/动漫/油画/水彩/素描/赛博朋克/奇幻
- 💾 **智能缓存** - 1 小时缓存机制，节省 API 调用
- 🔄 **智能重试** - 失败自动重试，指数退避策略
- ⚡ **并发控制** - 批量生成时控制并发数，避免限流
- 📐 **多尺寸支持** - 7 种尺寸可选，最高 1536x1536
- 🛡️ **完整错误处理** - 详细的错误信息和错误码

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/node/openclaw-skills/volc-image-gen
npm install
```

### 2. 配置环境变量

**Linux/macOS:**

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export VOLC_API_KEY="your_api_key_here"' >> ~/.bashrc
echo 'export VOLC_API_BASE="https://ark.cn-beijing.volces.com/api/v3"' >> ~/.bashrc
source ~/.bashrc
```

**Windows PowerShell:**

```powershell
[System.Environment]::SetEnvironmentVariable("VOLC_API_KEY", "your_api_key_here", "User")
[System.Environment]::SetEnvironmentVariable("VOLC_API_BASE", "https://ark.cn-beijing.volces.com/api/v3", "User")
```

### 3. 获取 API Key

1. 访问 [火山引擎方舟控制台](https://console.volcengine.com/ark)
2. 登录/注册账号
3. 创建或选择应用
4. 获取 API Key

### 4. 测试安装

```bash
node tests/image-gen.test.js
```

---

## 📋 使用指南

### 通过 OpenClaw 调用

```javascript
const { execute } = require('./src/index');

// 文生图
const result = await execute({
  command: 'generate',
  params: {
    prompt: '一只可爱的猫咪在阳光下玩耍',
    style: 'realistic',
    size: '1024x1024',
    n: 1
  }
});

console.log(result);
```

### 命令别名

| 功能 | 命令别名 |
|------|----------|
| 文生图 | `generate`, `文生图`, `生成图片`, `img`, `image` |
| 图生图 | `edit`, `图生图`, `编辑图片`, `img2img` |
| 批量生成 | `batch`, `批量生成`, `batch_generate` |
| 变体生成 | `variations`, `生成变体`, `变体` |
| 帮助 | `help`, `帮助`, `usage` |

---

## 🔧 API 参考

### generateImage - 文生图

```javascript
async function generateImage(options)
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | string | - | 【必填】图片描述 |
| size | string | '1024x1024' | 图片尺寸 |
| n | number | 1 | 生成数量 |
| style | string | 'realistic' | 风格 |
| negative_prompt | string | '' | 负面提示词 |
| maxRetries | number | 3 | 最大重试次数 |
| useCache | boolean | true | 是否使用缓存 |

**返回：**

```json
{
  "success": true,
  "images": [...],
  "usage": {
    "tokens": 100,
    "cost": 0.12,
    "model": "doubao-image-x"
  }
}
```

### editImage - 图生图

```javascript
async function editImage(options)
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| image | string | - | 【必填】输入图片（URL 或本地路径） |
| prompt | string | - | 【必填】编辑描述 |
| strength | number | 0.7 | 重绘强度（0-1） |
| size | string | '1024x1024' | 输出尺寸 |
| maxRetries | number | 3 | 最大重试次数 |

### batchGenerate - 批量生成

```javascript
async function batchGenerate(prompts, options)
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompts | string[] | - | 【必填】提示词数组 |
| concurrent | number | 3 | 并发数 |
| size | string | '1024x1024' | 尺寸 |
| style | string | 'realistic' | 风格 |

### createVariations - 变体生成

```javascript
async function createVariations(image, options)
```

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| image | string | - | 【必填】输入图片 |
| n | number | 3 | 变体数量 |
| strength | number | 0.5 | 变体强度 |
| size | string | '1024x1024' | 尺寸 |

---

## 🎨 风格列表

| 风格 Key | 说明 | 适用场景 |
|----------|------|----------|
| `realistic` | 写实风格，高清，高质量，专业摄影 | 产品摄影、人像、风景 |
| `anime` | 动漫风格，二次元，精美，日系动画 | 动漫角色、插画 |
| `oil` | 油画风格，艺术感，厚重，古典绘画 | 艺术作品、装饰画 |
| `watercolor` | 水彩风格，清新，透明感，淡雅 | 清新插画、背景 |
| `sketch` | 素描风格，线条感，黑白，手绘 | 草图、线稿 |
| `cyberpunk` | 赛博朋克风格，霓虹灯，未来感，科技 | 科幻场景、未来城市 |
| `fantasy` | 奇幻风格，魔法，梦幻，神秘 | 奇幻场景、魔法效果 |

---

## 📐 支持尺寸

- `512x512` - 小尺寸，快速生成
- `512x768` - 竖向构图
- `768x512` - 横向构图
- `768x768` - 中等尺寸
- `1024x1024` - 标准尺寸（默认）
- `1024x1536` - 高清竖向
- `1536x1024` - 高清横向

---

## ⚙️ 配置说明

### 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `VOLC_API_KEY` | ✅ | - | 火山引擎 API Key |
| `VOLC_API_BASE` | ❌ | `https://ark.cn-beijing.volces.com/api/v3` | API 基础 URL |
| `VOLC_IMAGE_MODEL` | ❌ | `doubao-image-x` | 图像模型名称 |

### 缓存配置

缓存默认启用，TTL 为 1 小时。缓存键基于：
- prompt 内容
- size 参数
- style 参数
- n 参数

相同参数的请求会直接返回缓存结果，不会产生 API 调用。

### 重试策略

- **触发条件：** 429（限流）或 5xx（服务器错误）
- **不重试：** 401（鉴权失败）、400（参数错误）
- **退避算法：** `delay = 1000ms * 2^(attempt-1)`
- **最大重试：** 3 次（可配置）

---

## 💡 示例代码

### 示例 1：基础文生图

```javascript
const { execute } = require('./src/index');

const result = await execute({
  command: 'generate',
  params: {
    prompt: '一只可爱的猫咪在阳光下玩耍',
    style: 'realistic'
  }
});

if (result.success) {
  console.log('生成成功！');
  console.log('本地路径:', result.images[0].local_path);
} else {
  console.error('生成失败:', result.error);
}
```

### 示例 2：动漫风格头像

```javascript
const result = await execute({
  command: 'generate',
  params: {
    prompt: '一个可爱的女孩，大眼睛，长发，微笑',
    style: 'anime',
    size: '1024x1024',
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
      '白色 T 恤，简约设计，纯白背景',
      '蓝色牛仔裤，休闲风格，展示细节',
      '黑色运动鞋，时尚款式，侧面视角'
    ],
    concurrent: 3,
    style: 'realistic'
  }
});

console.log(`成功：${result.successful}, 失败：${result.failed}`);
console.log(`总成本：¥${result.usage.total_cost.toFixed(2)}`);
```

### 示例 4：图片编辑

```javascript
const result = await execute({
  command: 'edit',
  params: {
    image: 'https://example.com/input.png',
    prompt: '将背景换成海滩日落',
    strength: 0.6
  }
});
```

### 示例 5：生成变体

```javascript
const result = await execute({
  command: 'variations',
  params: {
    image: '/path/to/image.png',
    n: 5,
    strength: 0.5
  }
});

console.log(`生成了 ${result.variations.length} 个变体`);
```

---

## ⚠️ 常见问题

### 1. 鉴权失败 (401)

**错误信息：** `鉴权失败 (401) - 请检查 VOLC_API_KEY 是否正确`

**解决方案：**
```bash
# 检查环境变量
echo $VOLC_API_KEY

# 重新配置
export VOLC_API_KEY="your_correct_api_key"
```

### 2. 参数错误 (400)

**错误信息：** `参数错误 (400): ...`

**解决方案：**
- 检查 prompt 是否为空
- 检查 size 是否在支持列表中
- 检查 strength 是否在 0-1 范围内

### 3. API 限流 (429)

**错误信息：** `API 限流，请稍后重试`

**解决方案：**
- 降低批量生成的并发数（concurrent: 1-2）
- 添加请求间隔
- 联系火山引擎申请提高配额

### 4. 图片下载失败

**错误信息：** `下载图片失败：...`

**解决方案：**
- 检查网络连接
- 检查 /tmp/openclaw 目录权限
- 重试请求

### 5. 超时错误

**错误信息：** `timeout of 120000ms exceeded`

**解决方案：**
- 图片生成可能需要较长时间，特别是高分辨率
- 检查火山引擎服务状态
- 稍后重试

---

## 📊 更新日志

### v1.0.0 (2026-04-01)

**✨ 初始版本发布**

- 🎨 文生图功能（7 种风格）
- 🖼️ 图生图功能（图片编辑）
- 📦 批量生成功能（并发控制）
- 🔄 变体生成功能
- 💾 1 小时智能缓存
- 🔄 指数退避重试策略
- 🧪 完整单元测试
- 📚 详细文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [火山引擎方舟文档](https://www.volcengine.com/docs/82379)
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/rfdiosuao/openclaw-skills)
- [ClawHub Skill 市场](https://clawhub.ai)

---

## 👨‍💻 作者

**OpenClaw Skill Master**

如有问题或建议，欢迎提交 Issue 或 Pull Request！
