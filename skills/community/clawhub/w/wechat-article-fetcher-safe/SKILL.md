# WeChat Article Fetcher - 微信文章抓取技能

> 使用 Puppeteer + Chrome 本地提取微信公众号文章内容。

---

## 📋 技能信息

| 字段 | 值 |
|------|-----|
| **技能名称** | wechat-article-fetcher-safe |
| **版本** | 2.0.0 |
| **作者** | @Adgai115 |
| **创建时间** | 2026-03-21 |
| **更新时间** | 2026-04-22 |
| **适用场景** | 微信公众号文章内容提取 |
| **技术栈** | Node.js + Puppeteer + Chrome |
| **仓库** | https://github.com/Adgai115/wechat-article-fetcher-safe |

---

## 🎯 功能

### ✅ 支持
- 微信公众号文章全文提取
- 文章元信息获取（标题、作者、时间）
- 文章图片下载保存（原图下载 + Markdown 嵌入链接）
- 移动端 User-Agent 适配
- JavaScript 渲染页面支持
- 输出格式：Markdown / 纯文本 / HTML
- 自动保存为文件
- 错误处理和超时保护

### ❌ 不支持
- 需要登录的文章
- 付费阅读内容
- 图片内文字 OCR 识别（仅下载图片原文件）

---

## 📦 安装

### 1. 确认环境

```bash
node -v  # 需要 v18+
```

### 2. 安装依赖

```bash
cd wechat-article-fetcher-safe
npm install
```

### 3. Chrome 路径

脚本会自动检测 Chrome 路径。如检测失败，修改脚本中的 `chromePath`。

**Windows 标准路径：**
```
C:\Program Files\Google\Chrome\Application\chrome.exe
```

---

## 🚀 使用方法

### 命令行

```bash
node fetch-wechat-article.js https://mp.weixin.qq.com/s/xxx
```

### 作为 OpenClaw Skill 调用

```javascript
const { fetchWechatArticle } = require('./fetch-wechat-article');

const result = await fetchWechatArticle({
  url: 'https://mp.weixin.qq.com/s/xxx',
  saveToFile: true,
  outputDir: './output'
});

console.log(result.title);
console.log(result.content);
```

---

## 📝 输出示例

```
========== 文章信息 ==========

标题：文章标题
作者：公众号名称
时间：发布日期

========== 文章内容 ==========

（正文内容）

========== 文章结束 ==========

内容已保存到：./article-wechat-xxxxx.txt
```

---

## 🔑 核心实现

### 1. Chrome 无头模式

```javascript
const browser = await puppeteer.launch({
  executablePath: chromePath,
  headless: true,
  args: ['--no-sandbox', '--disable-gpu']
});
```

### 2. 移动端 User-Agent

```javascript
await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 ...) MicroMessenger/8.0.0');
await page.setViewport({ width: 375, height: 812 });
```

### 3. 内容提取

```javascript
const articleData = await page.evaluate(() => {
  const title = document.querySelector('#activity-name')?.innerText;
  const content = document.querySelector('#js_content')?.innerText;
  return { title, content };
});
```

---

## ⚠️ 常见问题

### 找不到 Chrome

脚本会自动检测以下路径：
- `C:\Program Files\Google\Chrome\Application\chrome.exe`
- `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- `/usr/bin/google-chrome`
- `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

### 提取内容为空

1. 文章可能需要登录
2. 增加等待时间：`await page.waitForSelector('#js_content', { timeout: 30000 })`

---

## 📁 文件结构

```
wechat-article-fetcher-safe/
├── SKILL.md                    # 技能文档（本文件）
├── fetch-wechat-article.js     # 主脚本
├── package.json                # npm 配置
├── README.md                   # 快速入门
└── README.github.md            # GitHub 展示文档
```

---

## 🔒 隐私说明

- 所有操作在本地完成
- 不发送数据到任何外部服务器
- 不收集用户信息
- 源代码完全公开可审查

---

## 📝 更新日志

### v2.0.0 (2026-04-22)
- 清理冗余文件
- 更新仓库地址
- 移除不必要的 OCR 依赖
- 优化文档

### v1.1.0 (2026-03-25)
- 重命名为安全版 (safe)
- 优化正文提取和失败识别
- 自动探测 Chrome 路径

### v1.0.0 (2026-03-21)
- 初始版本

---

## 📄 许可证

MIT-0 (MIT No Attribution)

---

**仓库**：https://github.com/Adgai115/wechat-article-fetcher-safe
**维护者**：@Adgai115
**最后更新**：2026-04-22
