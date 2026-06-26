---
name: wechat-look-ocr
description: 读取微信公众号文章的专用工具，支持OCR文字识别。自动规范化URL并提取文章内容，识别图片中的中英文文字。
runtime: python
requirements:
  - python >= 3.7
  - nodejs >= 18
  - npm
dependencies:
  - requests
  - subprocess
  - json
  - pathlib
install_steps:
  - cd ocr_node && npm install
---

# WeChat Look OCR - 微信文章阅读工具（支持OCR）

## 📋 安装要求

### 系统要求
- **Python**: 3.7 或更高版本
- **Node.js**: 18 或更高版本
- **npm**: Node.js 包管理器

### 安装步骤

1. **安装系统依赖**：
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 nodejs npm
   
   # macOS
   brew install python node
   
   # Windows
   # 从 https://nodejs.org/ 下载 Node.js
   # 从 https://python.org/ 下载 Python
   ```

2. **安装技能**：
   ```bash
   openclaw skill install wechat-look-ocr
   ```

3. **安装 Node.js 依赖**：
   ```bash
   cd ~/.openclaw/skills/wechat-look-ocr/ocr_node
   npm install
   ```

## 功能特性

- **自动URL规范化**: 自动添加`?scene=1`参数绕过验证码
- **内容提取**: 从HTML中提取纯文本内容
- **OCR文字识别**: 自动识别图片中的中英文文字
- **中英文支持**: 支持中文简体和英文OCR识别
- **智能回退**: 中英文识别失败时自动回退到英文
- **错误处理**: 友好的错误提示和重试机制
- **安全合规**: 遵守OpenClaw安全规范，标记外部内容为未信任源

## 使用方法

在OpenClaw中直接使用：

```
读取微信文章 https://mp.weixin.qq.com/s/xxx
```

## URL规范化规则

- 无查询参数 → 添加 `?scene=1`
- 有查询参数 → 确保包含 `scene=1` (覆盖重复参数)

## 🔧 技术实现

### 系统架构

该技能采用 Python + Node.js 混合架构：

- **Python 层**：处理 URL 规范化、HTML 内容提取、图片 URL 提取
- **Node.js 层**：运行 OCR 识别（使用 Tesseract.js）
- **通信方式**：Python 通过 subprocess 启动 Node.js 脚本

### 实现原理

1. **URL检测**: 检查是否为微信文章URL
2. **参数规范化**: 添加或更新`scene=1`参数  
3. **内容获取**: 使用 requests 库获取页面内容
4. **文本提取**: 从HTML中提取纯文本内容
5. **图片处理**: 提取所有图片URL
6. **OCR识别**: 启动 Node.js 子进程进行文字识别
7. **结果整合**: 合并文本内容和OCR结果
8. **结果返回**: 提供结构化响应

## 📦 依赖详情

### Python 依赖
- `requests` - HTTP 请求库
- `subprocess` - 启动 Node.js 进程
- `json` - JSON 数据处理
- `pathlib` - 路径操作
- `re` - 正则表达式

### Node.js 依赖
- `tesseract.js` - OCR 识别引擎
- `node-fetch` - HTTP 请求库

### 运行时行为

该技能在运行时会：
1. 向微信服务器发送 HTTP 请求获取文章页面
2. 下载文章中的图片用于 OCR 识别
3. 启动本地 Node.js 进程进行文字识别
4. 返回整合的文本和 OCR 结果

## 示例输出

```json
{
  "title": "文章标题",
  "author": "作者名",
  "text_content": "提取的正文内容",
  "image_count": 5,
  "ocr_text": "[图片1] 识别的文字内容...",
  "url": "规范化后的URL",
  "status": "success"
}
```

## 注意事项

- 仅支持微信公众号文章链接
- 遵守微信访问频率限制
- 外部内容标记为未信任源
- 如遇到验证码问题，请确保URL正确包含`scene=1`