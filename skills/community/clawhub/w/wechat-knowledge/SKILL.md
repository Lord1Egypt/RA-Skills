---
name: WeChat Knowledge Base
description: |
  微信最好用的知识库管家 — 发链接就完事！
  📱 支持视频号｜抖音｜小红书｜公众号｜本地文件
  🚀 一站式管理：链接解析 → 自动下载 → 上传腾讯文档 → 智能建索引
  🤖 Agent 自动化，无需手动操作，把散落各处的内容变成你的知识资产
  ☁️ 腾讯文档集成，上传后直接在线播放、预览、分享
  ⚠️ 新用户首次使用需完成腾讯文档授权（详见文档）
  触发词：知识库、保存链接、存到知识库、帮我存这个、下载这个视频/文章
version: 2.2.5
---

# 一键知识库 - 微信内容管家

> 🦅 **微信最好用的知识库管家** — 发链接就完事！
> 
> 链接秒入库 — 支持视频号/抖音/小红书/公众号，自动下载上传到腾讯文档并建索引，告别手动整理。

## ✨ 核心亮点

- 🎯 **一键入库**：发个链接就完事，Agent 自动识别来源、下载、上传、建索引
- 📱 **全平台支持**：视频号、抖音、小红书、微信公众号、本地文件
- 🤖 **智能自动化**：Agent 打通全流程，无需手动操作
- ☁️ **腾讯文档集成**：视频在线播放、文章智能归档、一键分享
- 📊 **智能索引**：自动生成索引表格，内容资产一目了然

## 核心能力

接收链接 → 自动识别来源 → 下载/解析 → 上传腾讯文档 → 写 0 号索引。

| 来源 | 下载方式 | 是否上传视频 |
|------|----------|-------------|
| 视频号 | parsers/sph.py | ✅ 上传 |
| 抖音 | parsers/douyin.py | ✅ 上传 |
| 小红书 | parsers/xiaohongshu.py | ✅ 上传 |
| 公众号 | web_fetch 抓取 | ✅ 上传为 markdown |

## ⚠️ 首次使用必读：腾讯文档授权

**新用户需要完成腾讯文档授权才能使用本技能！**

本技能需要访问你的腾讯文档空间进行文件上传和智能表格操作，首次使用前请完成授权：

### 授权步骤

1. **安装腾讯文档 Skill**
   ```bash
   openclaw skills install tencent-docs
   ```

2. **完成微信扫码授权**
   - 在 Agent 对话中触发任意腾讯文档操作（如「列出我的腾讯文档」）
   - Agent 会弹出授权链接，点击后使用**微信扫码**完成授权
   - 授权成功后自动保存凭证，后续无需重复授权

3. **创建知识库空间**（可选）
   - 如果你还没有知识库空间，Agent 可以帮你创建
   - 或手动在 [docs.qq.com](https://docs.qq.com) 创建知识库空间

### 为什么需要授权？

- 📤 **上传文件**：视频、文档上传到腾讯文档需要访问权限
- 📊 **智能表格**：写入索引记录需要智能表格操作权限
- 🔐 **安全可靠**：通过微信扫码授权，不会存储你的账号密码

---

## 配置

打开 `agent.py`，当前已配置好：

```
TENCENT_SPACE_ID = "DS2RjWGhWZ1VyaWt"
INDEX_FILE_ID    = "ctEJCDugfswG"
INDEX_SHEET_ID   = "t00i2h"
```

**获取 ID 的方法**（如果是新空间）：
1. 打开 [docs.qq.com](https://docs.qq.com)，进入知识库空间，URL 中 `space/` 后面的就是 `space_id`
2. 在空间中新建智能表格 `0号索引`，URL 中拿到 `file_id`
3. 打开智能表格，地址栏 `tab=` 后面就是 `sheet_id`

## 0 号索引字段

| 列名 | 类型 | 字段 ID（固定） |
|------|------|----------------|
| 文件名字 | 文本 | fkfKit |
| 文档大小 | 数字(KB) | f2cnP7 |
| 入库时间 | 日期时间 | fHSMJO |
| 格式 | 单选 | fOVcRT |
| 来源类型 | 单选 | fPoljj |
| 来源 | 文本 | f6drfQ |
| 是否外链 | 复选 | fcP5do |
| 腾讯文档链接 | URL | fBW04a |
| 等级 | 单选 | fWqSI6 |

## 工作流程

### 步骤总览

```
链接/文件 → 识别来源 → 下载到本地 → upload_to_docs.py → 腾讯文档 + 0号索引
```

### 各来源处理

#### 视频号

```
python parsers/sph.py <视频号链接> --output-dir <临时目录>
→ 返回 JSON {title, author, video, size_bytes}

python upload_to_docs.py <video_path> \
  --name "<title>" --format mp4 --source-type 视频号 \
  --source-url "<原始链接>" --author "<author>" --level 一般
```

#### 抖音

```
python parsers/douyin.py <链接> --output-dir <临时目录>
→ 返回 JSON {title, author, video, size_bytes}

python upload_to_docs.py <video_path> \
  --name "<title>" --format mp4 --source-type 抖音 \
  --source-url "<原始链接>" --author "<author>" --level 一般
```

#### 小红书

```
python parsers/xiaohongshu.py <链接> --output-dir <临时目录>
→ 返回 JSON {title, author, file, size_bytes, type}

python upload_to_docs.py <file_path> \
  --name "<title>" --format <type> --source-type 小红书 \
  --source-url "<原始链接>" --author "<author>" --level 一般
```

#### 微信公众号

```
web_fetch 抓取文章内容，转 markdown

python upload_to_docs.py <markdown_file> \
  --name "<标题>" --format 文章 --source-type 微信公众号 \
  --source-url "<原始链接>" --author "<公众号名>" --level 一般
```

#### 本地文件（pdf/pptx/docx/jpg/png）

```
python upload_to_docs.py <文件路径> \
  --name "<文件名>" --format <格式> --source-type 本地上传 \
  --level 一般
```

### upload_to_docs.py 自动完成

该脚本自动执行：
1. `manage.pre_import` — 获取 COS 上传凭证
2. `curl PUT` — 上传到 COS
3. `manage.async_import` — 触发导入
4. `manage.import_progress` — 轮询直到完成
5. `add_to_sheet.py` — 写入 0 号索引

```bash
python upload_to_docs.py <文件路径> \
  --name "标题" \
  --format "mp4|pdf|pptx|docx|jpg|png|文章" \
  --source-type "视频号|抖音|小红书|微信公众号|本地上传" \
  --source-url "原始链接" \
  --author "作者名" \
  --level "机密|高|一般|普通"
```

`--level` 不传默认为 `一般`，`--is-external` 不传默认为 `False`。

## 文件结构

```
knowledge-base/
├── SKILL.md              # 本文件
├── README.md              # 使用说明
├── CHANGELOG.md           # 版本历史
├── DESIGN.md              # 架构设计
├── agent.py               # CLI 辅助
├── add_to_sheet.py        # 智能表格记录添加
├── upload_to_docs.py      # 一键上传
└── parsers/
    ├── sph.py             # 视频号下载
    ├── douyin.py           # 抖音下载
    ├── xiaohongshu.py      # 小红书下载
    └── wechat_article.py   # 公众号文章解析
```

## 注意事项

### ⚠️ 首次使用必看

**新用户必须完成腾讯文档授权才能使用本技能！** 请参阅上方「首次使用必读」章节。

### 其他注意事项

- 视频文件大小限制：腾讯文档单文件 < 100MB
- 小红书 yt-dlp 依赖：需要 yt-dlp + cookies（如需要登录态）
- 公众号文章过长时可能触发 CreateProcess 命令行限制，使用 `upload_to_docs.py` 可绕过
- 索引记录的"入库时间"字段暂不支持 API 设置，需在腾讯文档 UI 上配置自动填入

## 常见问题

**Q：视频上传腾讯文档后能播放吗？**
A：能。腾讯文档支持 mp4 在线播放。

**Q：小红书下载失败？**
A：确认 yt-dlp 已更新到最新版：`yt-dlp -U`。个别小红书链接可能需要浏览器 cookies。

**Q：怎么确认上传成功了？**
A：查看 0 号索引智能表格，新记录出现即表示成功。也可以直接打开腾讯文档链接确认。

---

**让 Agent 帮你管理知识资产，发现好内容，秒速入库！** 🚀