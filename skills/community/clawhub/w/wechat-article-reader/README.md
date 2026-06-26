# 微信公众号文章导出技能

> 一个可以将微信公众号文章导出为 Markdown 格式的 SKILL 技能，支持 Claude Code / OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 功能特性

- 一键导出微信公众号文章为 Markdown
- 自动提取元数据（标题、作者、发布时间）
- 输出带 YAML Front Matter 的规范格式
- 无需配置 API Key，开箱即用
- 支持中英文双语

## 安装

### 作为 Claude Code / OpenClaw 技能使用

1. 将此仓库克隆到你的 skills 目录：

```bash
# Claude Code
git clone https://github.com/启明/WeChat-article-reader.git ~/.claude/skills/WeChat-article-reader

# OpenClaw
git clone https://github.com/启明/WeChat-article-reader.git ~/.openclaw/workspace/skills/WeChat-article-reader
```

2. 安装 Python 依赖：

```bash
pip3 install -r requirements.txt
```

### 独立命令行使用

```bash
# 安装依赖
pip3 install -r requirements.txt

# 导出文章
python3 scripts/export.py "https://mp.weixin.qq.com/s/xxx" ./output
```

## 使用方法

### 在 Claude Code 中使用

直接提供微信公众号文章链接：

```
下载这篇文章：https://mp.weixin.qq.com/s/xxx
```

技能会自动：
1. 抓取文章内容
2. 提取元数据和正文
3. 保存为 Markdown 文件
4. 报告输出位置

### 命令行使用

```bash
python3 scripts/export.py <文章URL> [输出目录]
```

## 输出格式

导出的 Markdown 文件包含完整的 YAML Front Matter：

```yaml
---
title: 文章标题
author: 作者名称
publish_time: 发布时间
source_url: 原文链接
exported_at: 导出时间戳
description: 文章描述
---

# 文章标题

> 原文链接: URL

**作者**: XXX
**发布时间**: XXX

-----

文章正文内容...
```

## 文件命名

生成的文件遵循格式：`YYYYMMDD_HHMMSS_文章标题.md`

特殊字符会被自动清理以确保文件系统兼容性。

## 使用限制

- 部分文章需要微信登录才能查看
- 微信有反爬虫机制，频繁请求可能被限制
- 仅导出文本内容，不下载图片
- 复杂排版可能无法完全还原

## 技术实现

- **HTTP 请求**：`requests` - 获取文章页面
- **HTML 解析**：`BeautifulSoup` + `lxml` - 提取内容
- **格式转换**：`markdownify` - HTML 转 Markdown

## 项目结构

```
WeChat-article-reader/
├── SKILL.md          # 技能文档（Claude Code 使用）
├── README.md         # 项目说明
├── LICENSE           # MIT 开源协议
├── requirements.txt  # Python 依赖
├── .gitignore        # Git 忽略规则
└── scripts/
    └── export.py     # 导出脚本
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) - 项目灵感来源
- [markdownify](https://github.com/matthewwithanm/python-markdownify) - HTML 转 Markdown 工具

## 开源协议

[MIT License](LICENSE)

## 作者

Created by [Leefee](https://github.com/启明)

---

如果这个项目对你有帮助，请给个 ⭐ Star！
