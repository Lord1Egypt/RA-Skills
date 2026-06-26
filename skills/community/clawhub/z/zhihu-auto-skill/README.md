<div align="center">

# 🤖 知乎自动化 Skill

**让你的 AI 助手帮你打理知乎 — 发文章、写想法、回答问题、看热榜，全都自动化**

[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/liuboacean/zhihu-automation-skill)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://nodejs.org)
[![Playwright](https://img.shields.io/badge/playwright-powered-orange)](https://playwright.dev)

</div>

---

## ✨ 它能做什么？

| 功能 | 一句话描述 | 效果 |
|:----|-----------|:----:|
| 📝 **发文章** | 把 Markdown 一键发布到知乎专栏 | 不用打开浏览器编辑 |
| 💭 **发想法** | 像发朋友圈一样自动化发想法 | 随手记录灵感 |
| ❓ **答问题** | 搜索并回答知乎上的问题 | 自动涨粉利器 |
| 🙋 **提问** | 在知乎上自动提问 | 获取社区反馈 |
| 👍 **互动** | 点赞、评论、关注一条龙 | 社交自动化 |
| 🔥 **看热榜** | 实时获取知乎热榜 Top 20 | 选题不再愁 |
| 🔍 **搜内容** | 搜索知乎上的文章和回答 | 竞品调研好帮手 |

---

## 🚀 30 秒上手

```bash
# 1. 装依赖（已装好可跳过）
cd zhihu-skill && npm install

# 2. 生成加密密钥
export ZHIHU_COOKIE_KEY="$(openssl rand -hex 32)"

# 3. 登录知乎（只需一次，Cookie 自动加密保存）
node scripts/zhihu-export-cookie.js

# 4. 开玩 🎉
node scripts/zhihu-extract.js --type hot-list --limit 5      # 看热榜
node scripts/zhihu-publish.js thought --content "Hello 知乎"  # 发想法
```

> 💡 **小贴士**：把 `ZHIHU_COOKIE_KEY` 加到 `~/.zshrc` 里，以后每次打开终端就能直接用。

---

## 🏗️ 架构亮点

```
                  ┌──────────────────┐
                  │  AI Agent / 用户  │
                  └────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌────────────┐  ┌────────────┐  ┌──────────────┐
   │ HTTP 读通道 │  │ 浏览器写通道 │  │ Python OpenAPI│
   │ 热榜/搜索   │  │ 文章/想法   │  │ 圈子互动      │
   │ 用户/问答   │  │ 互动/问答   │  │ (可选)        │
   └────────────┘  └────────────┘  └──────────────┘
```

| 特性 | 说明 |
|------|------|
| 🔒 **Cookie 加密** | AES-256-GCM + 随机 IV，权限 0600，支持密钥轮换 |
| 🛡️ **反爬防护** | Playwright Stealth + 贝塞尔鼠标轨迹 + 逐字输入 + TLS 指纹伪装 |
| 🔄 **Plan B 降级** | 签名失效自动降级到浏览器通道，永不中断 |
| ⏱️ **智能限流** | HTTP 200-500ms / 浏览器 5-10s / 限流指数退避（30s → 10min） |
| 💥 **崩溃恢复** | 浏览器崩溃自动重建会话，任务不丢失 |

---

## 📖 详细用法

### 发布文章
```bash
# 从文件读取内容发布
node scripts/zhihu-publish.js article --title "文章标题" --content-file "article.md"

# 或直接传字符串
node scripts/zhihu-publish.js article --title "文章标题" --content "正文内容"

# 存为草稿（不发布）
node scripts/zhihu-publish.js article --title "标题" --content "正文" --draft
```

### 发布想法
```bash
node scripts/zhihu-publish.js thought --content "今天天气真好"
node scripts/zhihu-publish.js thought --content "附张图" --image "photo.jpg"
```

### 数据提取
```bash
node scripts/zhihu-extract.js --type hot-list --limit 10       # 热榜 Top 10
node scripts/zhihu-extract.js --type search --query "AI 编程"   # 搜索
node scripts/zhihu-extract.js --type user --id "excited-vczh"  # 用户信息
node scripts/zhihu-extract.js --type question --id 123456789    # 问题详情
```

### 互动
```bash
node scripts/zhihu-interact.js like --url "https://www.zhihu.com/question/xxx/answer/xxx"
node scripts/zhihu-interact.js comment --url "..." --content "好文章！"
node scripts/zhihu-interact.js follow --user "url_token"
```

### 问答
```bash
node scripts/zhihu-answer.js --question-id 123456789 --content "这是我的回答"
node scripts/zhihu-ask.js --title "如何学习 AI？" --detail "希望得到一些建议"
```

---

## 📂 项目结构

```
zhihu-skill/
├── SKILL.md                    # AI Agent 入口
├── package.json                # 依赖声明
├── config/
│   ├── selectors.json          # 页面选择器（带 fallbacks 自动降级）
│   └── api-endpoints.json      # HTTP API 端点配置
├── scripts/                    # 核心代码 12 模块
│   ├── zhihu-core.js           # Cookie 加密/浏览器管理/日志/重试
│   ├── zhihu-signature.js      # 签名生成（适配器模式）
│   ├── zhihu-http.js           # HTTP 读通道
│   ├── zhihu-browser.js        # 浏览器自动化
│   ├── zhihu-publish.js        # 发布文章+想法
│   ├── zhihu-interact.js       # 点赞+评论+关注
│   ├── zhihu-answer.js         # 回答问题
│   ├── zhihu-ask.js            # 提问
│   ├── zhihu-extract.js        # 数据提取
│   ├── zhihu-bridge.js         # Python 桥接
│   ├── zhihu-export-cookie.js  # Cookie 导出
│   └── python/zhihu_bot.py     # OpenAPI 圈子互动
└── tests/                      # 测试桩
```

---

## 📋 依赖

| 工具 | 版本要求 | 用途 |
|:----|:--------:|------|
| Node.js | >= 18 | 核心运行环境 |
| Playwright | 1.52+ | 浏览器自动化 |
| Python 3 | >= 3.8 | 仅圈子互动（可选） |

---

## ⚠️ 注意事项

- **Cookie 有效期约 30 天**，到期后重新运行 `node scripts/zhihu-export-cookie.js`
- **知乎前端经常改版**，`config/selectors.json` 可能需更新
- **HTTP 签名通道**（热榜/搜索）如果返回 401，系统会自动降级到浏览器通道
- 建议先在小号上测试，熟悉后再用于主账号

---

## 🤝 贡献

提交 Issue 或 PR，一起让知乎自动化更好用！

---

## 📄 License

MIT © liuboacean
