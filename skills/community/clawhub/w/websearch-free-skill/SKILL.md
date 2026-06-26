---
name: websearch
description: "Perform web searches using various search engines and APIs. "
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["node","npm"] } } }
---

# Web Search Skill / 网络搜索技能

Perform web searches using various search engines and APIs. This skill provides access to search functionality without requiring API keys for basic usage.

使用各种搜索引擎和API进行网络搜索。此技能提供搜索功能访问，无需API密钥即可进行基本操作。

## Features / 功能特性

- **URL Content Extraction**: Read and extract content from any web page URL
  **URL内容提取**: 从任意网页URL读取和提取内容
- **Keyword Search**: Search for specific keywords and return specified number of results
  **关键词搜索**: 搜索特定关键词并返回指定数量的结果
- **Dependency Management**: Automatic dependency installation via npm
  **依赖管理**: 通过npm自动安装依赖项

## Basic Usage / 基础用法

Read content from a specific URL:

从特定URL读取内容：

```bash
node ./search.js <url> [previewLength]
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
node ./search.js https://www.example.com

# Preview 500 characters
# 预览500字符
node ./search.js https://www.example.com 500

# No preview (show only metadata)
# 无预览（仅显示元数据）
node ./search.js https://www.example.com 0
```

**Output Format / 输出格式**:
- Title / 标题
- URL
- Platform / 平台
- Content length / 内容长度
- Content preview / 内容预览（可选）

## Advanced Usage / 高级用法

Search with specific keyword and result limit:

使用特定关键词和结果限制进行搜索：

```bash
node ./exasearch.js <keyword> [numResults]
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
node ./exasearch.js "artificial intelligence"

# Search with 20 results
# 搜索20个结果
node ./exasearch.js "machine learning" 20

# Search with 50 results
# 搜索50个结果
node ./exasearch.js "deep learning" 50
```

## Setup / 安装设置

First-time setup requires installing dependencies:

首次使用需要安装依赖：

**Prerequisites / 前置要求**:
- Node.js v22 or higher / Node.js v22 或更高版本
- npm or yarn

```bash
npm install
```

**Dependencies / 依赖项**:
- `axios`: HTTP client for web requests
  HTTP客户端，用于网络请求
- `mcporter`: Tool integration framework
  工具集成框架

## Error Handling / 错误处理

The scripts include comprehensive error handling for:

脚本包含全面的错误处理：

- Missing required parameters / 缺少必需参数
- Invalid parameter values / 无效参数值
- Network connection errors / 网络连接错误
- HTTP request failures / HTTP请求失败
- Server timeout errors / 服务器超时错误

## Technical Details / 技术细节

- **Backend / 后端**: Jina Reader API (https://r.jina.ai)
- **Timeout / 超时**: 15 seconds for web requests / 网络请求15秒
- **Output Format / 输出格式**: JSON / Markdown
- **Search Provider / 搜索提供商**: Exa API (via mcporter)

## Logic Examples / 逻辑示例

### ReadResult.js - Result Object Class

```javascript
export class ReadResult {
  constructor(title, content, url, platform = "web") {
    this.title = title;
    this.content = content;
    this.url = url;
    this.platform = platform;
  }

  toDict() {
    return {
      title: this.title,
      content: this.content,
      url: this.url,
      platform: this.platform
    };
  }
}
```

### search.js - URL Content Extraction

```javascript
import axios from 'axios';
import { ReadResult } from './ReadResult.js';

class WebChannel {
  constructor() {
    this.JINA_URL = "https://r.jina.ai/";
  }

  async read(url) {
    try {
      const response = await axios.get(`${this.JINA_URL}${url}`, {
        headers: {
          'Accept': 'text/markdown'
        },
        timeout: 15000
      });

      const text = response.data;
      let title = url;
      const lines = text.split('\n');
      
      for (const line of lines) {
        const trimmedLine = line.trim();
        if (trimmedLine.startsWith('# ')) {
          title = trimmedLine.substring(2).trim();
          break;
        }
        if (trimmedLine.startsWith('Title:')) {
          title = trimmedLine.substring(6).trim();
          break;
        }
      }

      return new ReadResult(title, text, url, "web");

    } catch (error) {
      if (error.response) {
        throw new Error(`HTTP ${error.response.status}: ${error.response.statusText}`);
      } else if (error.request) {
        throw new Error('Network error: No response received');
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
  }
}

async function main() {
  const url = process.argv[2];
  const previewLength = process.argv[3] ? parseInt(process.argv[3], 10) : 200;
  
  if (!url) {
    console.error('Usage: node search.js <url> [previewLength]');
    console.error('  url: The URL to read');
    console.error('  previewLength: Number of characters to preview (optional, default: 200)');
    process.exit(1);
  }

  if (isNaN(previewLength) || previewLength < 0) {
    console.error('Error: previewLength must be a non-negative integer');
    process.exit(1);
  }

  const webChannel = new WebChannel();
  
  try {
    console.log(`Reading: ${url}`);
    const result = await webChannel.read(url);
    
    console.log('\n=== Read Result ===');
    console.log(`Title: ${result.title}`);
    console.log(`URL: ${result.url}`);
    console.log(`Platform: ${result.platform}`);
    console.log(`Content length: ${result.content.length} characters`);
    
    if (previewLength > 0) {
      console.log(`\nFirst ${previewLength} characters of content:`);
      const preview = result.content.substring(0, previewLength);
      console.log(preview + (result.content.length > previewLength ? '...' : ''));
    }
    
  } catch (error) {
    console.error('Error reading web page:', error.message);
    process.exit(1);
  }
}

main();
```

### exasearch.js - Keyword Search

```javascript
import { callOnce } from "mcporter";

async function main() {
  const keyword = process.argv[2];
  const num = process.argv[3];

  if (!keyword) {
    console.error('Error: Search keyword is required');
    console.error('Usage: node exasearch.js <keyword> [numResults]');
    process.exit(1);
  }

  const numResults = num ? parseInt(num, 10) : 10;

  if (isNaN(numResults) || numResults < 1) {
    console.error('Error: numResults must be a positive integer');
    process.exit(1);
  }

  if (numResults > 100) {
    console.error('Error: numResults cannot exceed 100');
    process.exit(1);
  }

  try {
    console.log(`Searching for: ${keyword}`);
    console.log(`Number of results: ${numResults}`);
    
    const result = await callOnce({
      server: "exa",
      toolName: "web_search_exa",
      args: { query: keyword, numResults: numResults },
    });

    console.log('\n=== Search Results ===');
    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error('Error during search:', error.message);
    
    if (error.response) {
      console.error(`HTTP ${error.response.status}: ${error.response.statusText}`);
    } else if (error.request) {
      console.error('Network error: No response received from server');
    } else if (error.code === 'ECONNREFUSED') {
      console.error('Connection refused: Unable to reach the search server');
    } else if (error.code === 'ETIMEDOUT') {
      console.error('Request timeout: Server took too long to respond');
    }
    
    process.exit(1);
  }
}

main();
```
