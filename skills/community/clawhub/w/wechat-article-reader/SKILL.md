---
name: WeChat-article-reader
description: "将微信公众号文章导出为 Markdown 格式。当用户提供微信公众号链接 (mp.weixin.qq.com) 或要求下载/导出/保存微信文章时触发。默认保存到工作空间的 source 目录。"
---

# 微信公众号文章导出技能 (WeChat-Article-Reader)

## 触发条件

当以下情况时触发此技能：

- 用户提供微信公众号文章链接 (mp.weixin.qq.com)
- 用户要求"下载"、"导出"或"保存"微信文章
- 用户要求将微信文章转换为 Markdown
- 用户提到"公众号文章"、"微信文章"、"下载微信"、"导出公众号"

**触发示例：**
- "下载这篇文章 https://mp.weixin.qq.com/s/xxx"
- "把这篇公众号文章导出为 markdown"
- "保存微信文章到本地"
- "帮我保存这篇微信文章"

## 工作原理

此技能使用 Python 脚本执行以下操作：
1. 获取微信文章 HTML 页面
2. 从 Open Graph 元标签提取元数据（标题、作者、发布时间）
3. 从 `#js_content` div 提取正文内容
4. 使用 markdownify 将 HTML 转换为 Markdown
5. 保存为带 YAML Front Matter 的 Markdown 文件

## 脚本目录

**基础目录**：`~/.npm-global/lib/node_modules/openclaw/skills/WeChat-article-reader`

**脚本位置**：`scripts/export.py`

## 安装设置

### 首次安装

1. **检查 Python 依赖**：
```bash
python3 -c "import requests, bs4, markdownify" 2>/dev/null || echo "需要安装依赖"
```

2. **如需安装依赖**：
```bash
pip3 install requests beautifulsoup4 lxml markdownify
```

### 无需配置

此技能开箱即用，无需 API Key 或额外配置。使用带浏览器头部的 HTTP 请求来获取微信文章。

## 执行步骤

当此技能被触发时，按以下步骤执行：

### 步骤 1：提取 URL

从用户请求中识别微信文章 URL。有效 URL 以以下开头：
- `https://mp.weixin.qq.com/s/`
- `https://mp.weixin.qq.com/...`

### 步骤 2：确定输出目录

默认输出目录：`~/.openclaw/workspace-qiming/source`

用户可以指定自定义输出目录。

### 步骤 3：运行导出脚本

```bash
# 如需要则创建输出目录
mkdir -p "$OUTPUT_DIR"

# 运行导出脚本
python3 ~/.npm-global/lib/node_modules/openclaw/skills/WeChat-article-reader/scripts/export.py "$URL" "$OUTPUT_DIR"
```

### 步骤 4：报告结果

告知用户：
- 成功或失败状态
- 输出文件路径
- 文章标题和元数据
- 任何错误或警告

## 命令示例

```bash
# 基本导出
python3 ~/.npm-global/lib/node_modules/openclaw/skills/WeChat-article-reader/scripts/export.py "https://mp.weixin.qq.com/s/xxx" ~/.openclaw/workspace-qiming/source

# 指定自定义输出目录
python3 ~/.npm-global/lib/node_modules/openclaw/skills/WeChat-article-reader/scripts/export.py "$URL" "/path/to/output"
```

## 输出格式

导出的 Markdown 文件包含：

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

标题中的特殊字符会被清理以确保文件系统兼容性。

## 常见问题与限制

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| "无法找到文章正文内容" | 文章需要登录或已被删除 | 尝试在浏览器中打开，或使用浏览器工具 |
| 连接超时 | 网络问题或限流 | 等待后重试，检查网络连接 |
| 编码问题 | 特殊字符 | 脚本自动处理 UTF-8 |

### 已知限制

- **需要登录的文章**：部分文章需要微信登录才能查看
- **反爬虫**：微信有反机器人措施，可能阻止频繁请求
- **图片**：不下载文章图片，仅保存 Markdown 文本
- **复杂格式**：可能无法完全保留所有格式

## 依赖项

| 包名 | 版本 | 用途 |
|------|------|------|
| requests | >=2.31.0 | HTTP 请求 |
| beautifulsoup4 | >=4.12.0 | HTML 解析 |
| lxml | >=4.9.0 | XML/HTML 解析器 |
| markdownify | >=0.11.6 | HTML 转 Markdown |

## 错误处理

脚本会：
- 打印清晰的中文错误信息
- 使用正确的状态码退出
- 优雅处理缺失的依赖
- 处理前验证 URL 格式

## 来源

基于 wechat-article-export 项目：
- GitHub: https://github.com/wechat-article/wechat-article-exporter
- 本 Skill 由 启明 创建

## 开源协议

MIT License
