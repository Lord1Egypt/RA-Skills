# Web Search / 网络搜索

A lightweight web search and content extraction tool using Jina Reader API and Exa search engine.

一个轻量级的网络搜索和内容提取工具，使用 Jina Reader API 和 Exa 搜索引擎。

## Features / 功能特性

- **URL Content Extraction**: Extract clean, readable content from any web page
  **URL内容提取**: 从任意网页提取干净、可读的内容
- **Keyword Search**: Search the web with specific keywords and get structured results
  **关键词搜索**: 使用特定关键词搜索网络并获取结构化结果
- **No API Keys Required**: Free access to basic search and reading functionality
  **无需API密钥**: 免费访问基础搜索和阅读功能
- **Error Handling**: Comprehensive error handling for network and parameter issues
  **错误处理**: 对网络和参数问题的全面错误处理

## Installation / 安装

### Prerequisites / 前置要求

- Node.js (v22 or higher)
- npm or yarn

### Install Dependencies / 安装依赖

```bash
npm install
```

## Usage / 使用方法

### Read URL Content / 读取URL内容

Extract content from a specific URL:

从特定URL提取内容：

```bash
node search.js <url> [previewLength]
```

**Parameters / 参数**:

- `url`: The URL to read (required)
  要读取的URL（必需）
- `previewLength`: Number of characters to preview (optional, default: 200, use 0 to disable preview)
  预览字符数（可选，默认：200，使用0禁用预览）

**Examples / 示例**:

```bash
# Default preview (200 characters)
# 默认预览（200字符）
node search.js https://www.example.com

# Preview 500 characters
# 预览500字符
node search.js https://www.example.com 500

# No preview (show only metadata)
# 无预览（仅显示元数据）
node search.js https://www.example.com 0
```

**Output / 输出**:

```
Reading: https://www.example.com

=== Read Result ===
Title: Example Domain
URL: https://www.example.com
Platform: web
Content length: 1256 characters

First 200 characters of content:
# Example Domain

This domain is for use in illustrative examples...
```

### Search by Keyword / 关键词搜索

Search for specific keywords:

搜索特定关键词：

```bash
node exasearch.js <keyword> [numResults]
```

**Parameters / 参数**:

- `keyword`: Search query string (required)
  搜索查询字符串（必需）
- `numResults`: Number of results to return (optional, default: 10, max: 100)
  返回结果数量（可选，默认：10，最大：100）

**Examples / 示例**:

```bash
# Basic search with default 10 results
# 默认10个结果的基础搜索
node exasearch.js "artificial intelligence"

# Search with 20 results
# 搜索20个结果
node exasearch.js "machine learning" 20

# Search with 50 results
# 搜索50个结果
node exasearch.js "deep learning" 50
```

## Project Structure / 项目结构

```
websearch/
├── search.js           # URL content extraction script / URL内容提取脚本
├── exasearch.js        # Keyword search script / 关键词搜索脚本
├── ReadResult.js       # ReadResult class definition / ReadResult类定义
├── package.json        # Project dependencies / 项目依赖
├── SKILL.md           # Skill documentation / 技能文档
└── README.md          # This file / 本文件
```

## Dependencies / 依赖项

- **axios**: HTTP client for making web requests
  HTTP客户端，用于发起网络请求
- **mcporter**: Tool integration framework for Exa API
  工具集成框架，用于Exa API

## API Details / API详情

### Jina Reader API

- **Endpoint**: `https://r.jina.ai/`
- **Format**: Markdown
- **Timeout**: 15 seconds
- **Features**: Clean content extraction, ad removal, text formatting
  **功能**: 干净的内容提取、广告移除、文本格式化

### Exa Search API

- **Provider**: Exa (via mcporter)
- **Max Results**: 100 per request
- **Format**: JSON

## Error Handling / 错误处理

The scripts handle various error scenarios:

脚本处理各种错误场景：

- Missing required parameters / 缺少必需参数
- Invalid parameter values (non-integer, negative, too large) / 无效参数值（非整数、负数、过大）
- Network connection errors / 网络连接错误
- HTTP request failures (4xx, 5xx) / HTTP请求失败（4xx、5xx）
- Server timeout errors / 服务器超时错误
- Connection refused / 连接被拒绝

## License / 许可证

MIT License

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。
