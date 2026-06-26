---
name: wechat-saver
version: "1.1.0"
description: 微信公众号文章抓取工具。将微信文章转换为 Obsidian 兼容的 Markdown 格式，支持图片下载、智能格式识别（代码块/列表/引用）。
author: kuiilabs
tags: [wechat, markdown, obsidian, crawler, knowledge-base]
tech_stack: [Python, requests, BeautifulSoup, readability-lxml]
category: Content-Tools
complexity: Intermediate
---

# WeChat Saver - 微信公众号文章保存工具

将微信公众号文章转换为 Markdown 格式，保存到本地 Obsidian 知识库。

## 触发场景

当用户提供：
- 微信公众号文章链接
- 多条微信文章链接（批量处理）
- "把这篇文章保存到 Obsidian"
- "微信文章转 Markdown"

## 核心功能

### 1. 文章抓取
- 自动提取文章标题和正文
- 移除广告和无关元素
- 保留文章原始结构（标题、段落、列表等）
- 微信文章专属优化（`#js_content`、`.rich_media_content` 容器识别）

### 2. 图片处理
- 自动下载文章中的所有图片
- 保存到文章同级的 `images/` 目录
- Markdown 中使用相对路径引用（Obsidian 兼容）
- 支持微信图片多源识别（`data-src`、`data-original`、`src`）

### 3. Markdown 转换
- HTML → Markdown 格式转换
- 添加 YAML Frontmatter（标题、来源、日期、标签）
- 附加原文链接和抓取时间
- **智能格式识别**：
  - 代码块：自动识别命令行、curl、pip/npm 命令
  - 列表：识别中文序号（第一，、第二，）、数字列表、符号列表
  - 引用：识别"打个比方"、"例如"、"比如"等引用标记
  - URL：短文本中的 URL 自动转为 Markdown 链接
- 自动清理多余空行（3 个以上合并为 1 个）

### 4. 批量处理
- 支持一次处理多篇文章
- 输出处理报告

## 使用方法

### 安装依赖

**方法 1: 使用虚拟环境（推荐）**

```bash
# 创建虚拟环境
python3 -m venv ~/.claude/skills/wechat-saver/.venv

# 激活并安装
source ~/.claude/skills/wechat-saver/.venv/bin/activate
pip install requests readability-lxml beautifulsoup4 lxml
```

**方法 2: 使用 --break-system-packages**

```bash
pip3 install --break-system-packages requests readability-lxml beautifulsoup4 lxml
```

**方法 3: 使用国内镜像**

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple \
  --break-system-packages \
  requests readability-lxml beautifulsoup4 lxml
```

### 处理单篇文章

```bash
# 默认输出到 ~/Documents/Obsidian Vault/00-Inbox
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py \
  https://mp.weixin.qq.com/s/A1aYj3Dh-T32NqQdlYh27Q
```

### 指定输出目录

```bash
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py \
  -o ~/Documents/Obsidian\ Vault/01-Learning/Articles \
  https://mp.weixin.qq.com/s/xxx
```

### 不下载图片

```bash
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py \
  --no-images \
  https://mp.weixin.qq.com/s/xxx
```

### 批量处理

```bash
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py \
  url1 \
  url2 \
  url3
```

## 输出结构

```
00-Inbox/
├── 文章标题/
│   ├── images/
│   │   ├── image_001.jpg
│   │   ├── image_002.png
│   │   └── ...
│   └── 文章标题.md
```

## Markdown 输出格式

```markdown
---
title: 文章标题
source: https://mp.weixin.qq.com/s/xxx
created: 2026-04-05 12:00:00
tags: [wechat, article]
---

文章内容...

![image](images/image_001.jpg)

---
📌 原文链接：https://mp.weixin.qq.com/s/xxx
📅 抓取时间：2026-04-05 12:00:00
```

## 注意事项

1. **依赖安装**: 首次使用前需要安装 Python 依赖
2. **网络环境**: 需要能访问微信服务器
3. **图片反爬**: 部分图片可能有防盗链，下载可能失败
4. **付费文章**: 不支持需要登录/付费的文章

## 故障排查

| 问题 | 错误信息 | 解决方案 |
|------|---------|---------|
| 依赖缺失 | `ModuleNotFoundError` | 运行 `pip install requests readability-lxml beautifulsoup4 lxml` |
| 图片下载失败 | `403 Forbidden` | 微信防盗链，跳过该图片 |
| 提取失败 | 内容为空 | 文章可能需要登录或已被删除 |
| 输出目录不存在 | `FileNotFoundError` | 检查路径是否正确，注意空格转义 |

## 相关命令

```bash
# 安装依赖
pip install requests readability-lxml beautifulsoup4 lxml

# 测试单篇
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py <url>

# 查看帮助
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py --help
```

## 技术实现

- **正文提取**: `readability-lxml` (Mozilla Readability 算法)
- **HTML 解析**: `BeautifulSoup4` + `lxml`
- **图片下载**: `requests` 会话复用
- **路径处理**: Obsidian 相对路径兼容

## 改进方向

- [x] 智能格式识别（代码块、列表、引用自动格式化）
- [x] 连续空行自动清理
- [x] URL 自动转 Markdown 链接
- [ ] 支持微信登录 cookie（访问付费文章）
- [ ] 支持公众号主页抓取（批量获取文章列表）
- [ ] 添加文章元数据（作者、发布时间、阅读量等）

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.1.0 | 2026-04-05 | 新增智能格式识别：代码块、中文序号列表、X 层：列表、引用、URL 自动转链接；空行自动清理 |
| 1.0.0 | 2026-04-05 | 初始版本：基础抓取、图片下载、Markdown 转换 |
