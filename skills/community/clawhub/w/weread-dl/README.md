# 微信读书 AI 阅读助手 (weread-dl-skill)

基于 [Playwright](https://playwright.dev) 浏览器自动化的微信读书 AI 阅读助手。扫码登录后，可获取阅读进度、解码章节内容、存档聊天记录。

## 功能

- **扫码登录** — 通过微信扫码登录 weread.qq.com，cookies 持久化
- **书架列表** — 列出所有书籍及阅读进度
- **章节解码** — 拦截 `/web/book/chapter/e_X` API，解码 base64 HTML 章节内容
- **本地解码器** — `scripts/decode.js` 独立解码脚本，无需外部服务
- **阅读存档** — 每本书一个文件夹，保存 metadata / 章节加密数据 / 截图 / 聊天记录
- **标注笔记拉取** — 自动获取划线/高亮和笔记，保存到 notes.md，帮助理解阅读关注点
- **AI 对话** — 基于当前章节内容、标注和笔记与用户深度讨论书中观点

## 快速开始

### 环境要求

- Node.js >= 18
- Chromium / Chrome（Playwright 自动管理）

### 安装

```bash
git clone https://github.com/ColorlessBoy/weread-dl-skill.git
cd weread-dl-skill
export NODE_PATH=$(npm root -g)
```

### 1. 扫码登录

```bash
node scripts/login.js
```

脚本会打开 headless Chromium → 弹出微信二维码 → 截图二维码路径 → 等待扫码 → 保存 cookies。

### 2. 打开书籍（自动拉取标注+笔记）

```bash
node scripts/read-chapter.js <bookId>
```

bookId 从书架列表或阅读 URL（`/web/reader/{bookId}`）获取。

### 3. 单独拉取标注+笔记（不读章节）

```bash
node scripts/get-notes.js <bookId>
```

结果保存在 `books/<书名>/notes.md`。

### 3. 解码章节内容

```bash
node scripts/decode.js books/<书名>/chapters
```

解码结果保存在 `books/<书名>/chapters/` 下。

## 文件结构

```
weread-dl-skill/
├── SKILL.md                          # 完整文档
├── package.json
├── .gitignore
├── scripts/
│   ├── login.js                      # 扫码登录
│   ├── read-chapter.js               # 打开书籍 + API 拦截 + 存档 + 标注笔记
│   ├── get-notes.js                  # 单独拉取标注+笔记
│   ├── decode.js                     # 本地章节解码器
│   └── list-books.js                 # 书架列表
└── books/
    └── <书名>/
        ├── metadata.json             # 书籍信息 + 目录 + 阅读进度 + 标注/笔记统计
        ├── current-chapter.md        # 当前章节标记
        ├── chapters/
        │   ├── chapter_e0.enc        # 加密章节数据
        │   ├── chapter_e1.enc
        │   ├── chapter_e2.enc        # CSS 样式
        │   ├── chapter_e3.enc
        │   └── toc.json              # 目录结构数据
        ├── screenshots/
        │   └── YYYY-MM-DD.png        # 阅读页面截图
        ├── notes.md                  # 标注（划线）+ 笔记全文
        └── chat.md                   # 聊天记录
```

## 解码算法

微信读书章节 API 数据格式并非 AES 加密，而是：

```
32位hex校验码 + 1位分隔符 + base64(UTF-8 HTML)
```

| 端点 | 内容 |
|------|------|
| `chapter_e_0` | 完整 HTML 文档（含 `<body>`） |
| `chapter_e_1` | 续文片段 |
| `chapter_e_3` | 续文片段 |
| `chapter_e_2` | CSS 样式 |

解码即：去除前 33 个字符 → base64 decode → UTF-8 解码。
运行 `node scripts/decode.js books/<书名>/chapters` 即可获取纯文本。

## 技术实现

- **浏览器**: Playwright + Chromium (headless)
- **登录**: 微信开放平台 OAuth 扫码
- **数据**: API 响应拦截 + base64 解码
- **持久化**: cookies 保存到 `profile/weread-cookies.json`

## 注意事项

- ⚠️ 使用第三方工具有封号风险，建议使用小号
- VIP 专享内容需要 VIP 权益才能缓存导出

## License

MIT
