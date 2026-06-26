---
name: web-reader
description: "智能网页阅读器 - 抓取文章/下载视频并归档，支持分析、摘要、衍生。Triggers: '下载这篇文章', '抓取文章', '保存文章', 'fetch URL', '分析这篇文章', '摘要', '总结文章', '下载视频', '抓取微信文章', '抓取飞书文档', '把这个链接保存下来', '下载B站视频', 'download article', 'analyze article', 'summarize'."
version: 0.2.0
license: MIT
---

# Web Reader

智能网页阅读器：抓取文章（图文）→ 归档到指定目录 → 分析/摘要/衍生。

## 工作流程

### Phase 1: 下载原文（优先执行）

当用户提供 URL 并要求下载/保存/抓取/分析时，**先下载原文**。

**Step 1: 确定归档路径**

检查用户是否配置了归档目录。读取 `~/.claude/web-reader.json`：

```json
{
  "archive_dir": "/Volumes/Keybase (m4)/private/biggerbear/文档/微信摘录",
  "categories": ["AI漫剧短剧", "AI工具与技术", "OpenClaw", "开发技术", "商业与产品", "飞书文档"]
}
```

如果配置文件不存在，使用 `~/Documents/docs/` 作为默认归档目录。

**Step 2: 抓取文章**

```bash
python3 {SKILL_DIR}/fetcher.py "URL" -o "ARCHIVE_DIR" --category "CATEGORY"
```

对于需要 JavaScript 渲染的页面（返回 "JavaScript enabled" 错误），升级为浏览器模式：

```bash
# 先尝试 scrapling fetch（浏览器）
scrapling extract fetch "URL" /tmp/article.md --network-idle

# 如果仍失败，用 camoufox
python3 {SKILL_DIR}/fetcher.py "URL" -o "ARCHIVE_DIR" --method camoufox --category "CATEGORY"
```

**Step 3: 处理微信图片**

对于微信公众号文章（mp.weixin.qq.com），fetcher.py 自动处理 `data-src` 图片。
如果自动处理失败（图片为空 `![]()` 占位符），手动处理：

1. 用 scrapling 获取 HTML：`scrapling extract get "URL" /tmp/wx.html -s "#js_content"`
2. 从 HTML 中提取 `data-src="https://mmbiz.qpic.cn..."` URL
3. 下载图片到 `ARCHIVE_DIR/CATEGORY/SLUG/` 目录
4. 替换 markdown 中的空占位符为本地路径

**Step 4: 自动分类**

根据文章内容判断分类。参考分类关键词：
- **AI漫剧短剧**: 漫剧, 短剧, 动漫, seedance, AI视频创作
- **AI工具与技术**: AI工具, 大模型, scrapling, agent, API, 技术方案
- **OpenClaw**: openclaw, claude code, agent team
- **开发技术**: flutter, 编程, 开发, 逆向, IDE, 部署
- **商业与产品**: 产品分析, 商业模式, 市场, 付费, 创业
- **飞书文档**: feishu.cn 域名

如果不确定分类，**询问用户**选择或创建新分类。

**Step 5: 确认结果**

输出归档信息：
- 文章标题
- 保存路径
- 图片数量
- 分类

### Phase 2: 后续探索（用户触发）

文章下载完成后，等待用户指令：

| 指令 | 动作 |
|------|------|
| **分析** | 阅读文章全文，提取核心观点、论据、方法论，给出结构化分析 |
| **摘要** | 生成 3-5 句话的精炼摘要，保留关键数据和结论 |
| **总结** | 按章节列出要点，适合快速回顾 |
| **衍生** | 基于文章内容，提出可以进一步探索的方向、相关话题、实践建议 |
| **提炼** | 提取可直接复用的方法、工具、配置、代码片段 |
| **对比** | 与之前下载的其他文章进行对比分析（需指定对比目标） |
| **洗稿** | 基于原文重写，保留核心信息但完全改写表述（配合 /wxpub 使用） |

执行分析时，直接读取归档的 markdown 文件，不需要重新抓取。

## 智能路由

| 平台 | 方法 | 说明 |
|------|------|------|
| mp.weixin.qq.com | scrapling | 提取 `data-src` 图片，处理 SVG 占位符 |
| *.feishu.cn | 虚拟滚动 | 滚动采集内容块，浏览器内下载图片 |
| zhuanlan.zhihu.com | scrapling | `.Post-RichText` 选择器 |
| www.zhihu.com | scrapling | `.RichContent` 选择器 |
| www.toutiao.com | scrapling | 处理 toutiaoimg base64 占位符 |
| www.xiaohongshu.com | camoufox | 反爬需要隐身浏览器 |
| www.weibo.com | camoufox | 反爬需要隐身浏览器 |
| bilibili.com / b23.tv | yt-dlp | 视频下载 |
| youtube.com / youtu.be | yt-dlp | 视频下载 |
| douyin.com | yt-dlp | 视频下载 |
| 其他 URL | scrapling | 通用抓取，三级降级策略 |

## 安装依赖

按需安装：

| 依赖 | 用途 | 安装 |
|------|------|------|
| scrapling | 文章抓取 | `pip install scrapling` |
| yt-dlp | 视频下载 | `pip install yt-dlp` |
| camoufox | 反检测浏览器 | `pip install camoufox && python3 -m camoufox fetch` |
| html2text | HTML 转 Markdown | `pip install html2text` |

## CLI 参考

```
python3 {SKILL_DIR}/fetcher.py [URL] [OPTIONS]

参数:
  url                    要抓取的 URL

选项:
  -o, --output DIR       输出目录（默认: 当前目录）
  -q, --quality N        视频质量（默认: 1080）
  --method METHOD        强制方法: scrapling, camoufox, ytdlp, feishu
  --selector CSS         强制 CSS 选择器
  --urls-file FILE       URL 列表文件（每行一个，# 注释）
  --audio-only           仅提取音频
  --no-images            跳过图片下载
  --cookies-browser NAME 浏览器 cookies（如 chrome, firefox）
  --category NAME        归档子目录名
  --json-output          JSON 格式输出（程序化调用）
```

## 配置

创建 `~/.claude/web-reader.json` 配置归档目录：

```json
{
  "archive_dir": "~/Documents/docs/articles",
  "categories": ["技术", "产品", "行业"]
}
```

## 平台特殊处理

### 微信公众号
- 图片使用 `data-src` 属性 + `mmbiz.qpic.cn`
- 可见 `<img>` 是 SVG 懒加载占位符
- 图片下载需要 `Referer: https://mp.weixin.qq.com/` 请求头

### 飞书文档
- 虚拟滚动：滚过的内容会从 DOM 移除
- 注入 JS 采集器在滚动过程中捕获 `[data-block-id]` 内容块
- 图片 401：必须在浏览器上下文内用 `fetch(url, {credentials: 'include'})` 下载

### Bilibili
- 短链 (b23.tv) 自动解析
- 大会员内容用 `--cookies-browser chrome`

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 页面需要 JavaScript | 用 `--method camoufox` 或先 `scrapling extract fetch` |
| 微信图片为空 | 手动从 HTML 提取 `data-src` URL |
| 飞书返回登录页 | 文档可能需要认证 |
| B站 403 | 用 `--cookies-browser chrome` |
| 内容太短 | 尝试 `--method camoufox` |
