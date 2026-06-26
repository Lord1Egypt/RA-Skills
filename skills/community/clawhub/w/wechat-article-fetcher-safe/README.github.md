# 🛡️ 微信文章抓取器 - 安全版

> 本地运行的微信公众号文章内容提取工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-green.svg)](https://nodejs.org/)
[![Puppeteer](https://img.shields.io/badge/puppeteer-core-blue.svg)](https://pptr.dev/)

---

## ✨ 特性

- ✅ **本地运行** — 数据不外传，保护隐私
- ✅ **完整源代码** — 可审查，无后门
- ✅ **全文提取** — 支持长文内容完整获取
- ✅ **元信息获取** — 标题、作者、发布时间
- ✅ **JavaScript 渲染** — 完整获取动态内容
- ✅ **自动保存** — 提取结果保存为文本文件

---

## 🚀 快速开始

### 安装

```bash
npm install
```

### 运行

```bash
node fetch-wechat-article.js https://mp.weixin.qq.com/s/YOUR_ARTICLE_ID
```

### 输出示例

```
========== 文章信息 ==========

标题：文章标题
作者：公众号名称

========== 文章内容 ==========

（正文内容）

========== 文章结束 ==========

内容已保存到：./article-wechat-xxxxx.txt
```

---

## 📦 文件结构

```
wechat-article-fetcher-safe/
├── fetch-wechat-article.js     # 主脚本
├── package.json                # npm 配置
├── README.md                   # 快速入门
├── README.github.md            # 本文件（GitHub 展示）
└── SKILL.md                    # 完整技能文档
```

---

## ⚙️ 技术实现

1. **Puppeteer + Chrome** — 无头浏览器渲染页面
2. **移动端 User-Agent** — 获取移动端友好页面
3. **多选择器回退** — `#js_content` → `.rich_media_content` → `article`
4. **超时保护** — 默认 60 秒超时

---

## ❓ 常见问题

**Q: 找不到 Chrome？**
→ 脚本会自动检测 Chrome 路径。如果检测失败，修改脚本中的 `chromePath`。

**Q: 提取内容为空？**
→ 增加 `waitForSelector` 超时时间，或检查文章是否需要登录。

---

## 🔒 隐私说明

- 所有操作在本地完成
- 不发送数据到任何外部服务器
- 不收集用户信息
- 源代码完全公开可审查

---

## 📄 许可证

MIT-0 (MIT No Attribution)

---

**仓库**：https://github.com/Adgai115/wechat-article-fetcher-safe
**维护者**：@Adgai115
**最后更新**：2026-04-22
