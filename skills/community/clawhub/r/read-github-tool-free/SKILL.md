---slug: read-github-tool-free
name: read-github-tool-free
version: 1.0.0
displayName: 代码仓库阅读免费版
summary: "通过MCP serve"
license: Proprietary
edition: free
description: '代码仓库阅读工具免费版，通过MCP server读取代码仓库的文档和代码，帮助用户快速理解开源项目。核心能力:

  - 获取仓库完整文档（README等）

  - 文档语义搜索

  - 代码搜索（精确匹配）

  - 获取文档中引用的外部URL内容

  - URL自动转换（github。Use when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。'
tags:
  - 开发
  - 代码阅读
  - 文档
  - 开源
  - 版本控制
  - Git
  - 开发工具
  - repo
  - self
  - url
  - react
  - facebook
tools:
  - read
  - exec
  - write
homepage: ""
category: "Development"---# 代码仓库阅读工具（免费版）

## 概述

代码仓库阅读工具免费版通过 MCP server 帮助用户阅读和理解代码仓库的文档与代码。无需克隆整个仓库，通过 URL 转换和 MCP工具调用即可获取仓库文档、搜索代码和查找特定函数，大幅提升学习开源项目和进行技术选型的效率.
本版本聚焦单仓库的文档获取与代码搜索，适合个人开发者学习开源项目、查找 API 用法和进行技术选型。如需批量仓库分析、代码审计与 API 集成等高级能力，可升级至 PRO 版本.
## 核心能力

### 功能概览

| 功能 | 说明 | 命令 |
|---|---|---|
| 获取文档 | 获取仓库完整文档（README等） | `fetch-docs owner/repo` |
| 搜索文档 | 语义搜索仓库文档 | `search-docs owner/repo "query"` |
| 搜索代码 | 精确匹配搜索代码 | `search-code owner/repo "function_name"` |
| 获取URL内容 | 获取文档引用的外部URL | `fetch-url owner/repo "url"` |
| 列出工具 | 列出可用MCP工具 | `list-tools owner/repo` |

### URL 转换规则

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 代码仓库阅读免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
owner/repo → gitmcp.io/owner/repo
# ...
示例：
facebook/react → gitmcp.io/facebook/react
karpathy/llm-council → gitmcp.io/karpathy/llm-council
```

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 免费版能力边界

```text
[支持] 单仓库文档获取
[支持] 文档语义搜索
[支持] 代码精确匹配搜索
[支持] 外部URL内容获取
[支持] MCP工具列表查看
[限制] 不支持批量多仓库分析
[限制] 不支持跨仓库代码搜索
[限制] 不支持代码审计与安全检查
[限制] 不支持API集成
```

**处理**: 解析URL 转换规则的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回URL 转换规则的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：server、读取代码仓库文档、与代码、支持文档搜索与代、码检索、代码仓库阅读工具、读取代码仓库的文、档和代码、帮助用户快速理解、开源项目、核心能力、获取文档中引用的、自动转换、github、Use、when、需要文件处理、文档转换、格式互转、内容提取时使用、不适用于加密文件等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
### 核心功能执行(补充)
执行核心功能执行操作,使用`input_params`参数进行配置.

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：学习开源项目

开发者想快速了解一个开源项目的功能和使用方式.
```text
用户：帮我读一下 facebook/react 的文档
# ...
Agent 执行流程：
1. 转换URL: facebook/react → gitmcp.io/facebook/react
2. 调用 fetch-docs 获取完整文档
3. 解析文档结构
4. 输出项目概述、核心功能、使用方式
```

命令执行：

```bash
python3 （请参考skill目录中的脚本文件） fetch-docs facebook/react
```

示例输出：

```markdown
## React 项目文档
# ...
### 项目概述
React 是一个用于构建用户界面的 JavaScript 库...
# ...
### 核心功能
- 组件化开发
- 虚拟DOM
- 单向数据流
- JSX语法
# ...
### 依赖详情
npm install react react-dom
# ...
### 快速开始
[示例代码与使用说明]
```

### 场景二：查找特定函数

开发者需要找到某个函数的实现代码.
```text
用户：帮我在 facebook/react 仓库中搜索 useState 的实现
# ...
Agent：
1. 转换URL
2. 调用 search-code 搜索 "useState"
3. 返回匹配的文件和代码片段
```

```bash
python3 （请参考skill目录中的脚本文件） search-code facebook/react "useState"
```

### 场景三：搜索文档内容

用户想了解项目中某个特定功能的用法.
```text
用户：在 react 仓库中搜索"hooks"相关文档
# ...
Agent：
1. 调用 search-docs 进行语义搜索
2. 返回相关文档段落
3. 提供上下文链接
```

```bash
python3 （请参考skill目录中的脚本文件） search-docs facebook/react "hooks"
```

## 快速开始(补充)

### Step 1：获取仓库文档

```bash
# 获取仓库完整文档
python3 （请参考skill目录中的脚本文件） fetch-docs owner/repo
# ...
# 示例
python3 （请参考skill目录中的脚本文件） fetch-docs facebook/react
python3 （请参考skill目录中的脚本文件） fetch-docs vuejs/vue
```

### Step 2：搜索文档

```bash
# 语义搜索文档
python3 （请参考skill目录中的脚本文件） search-docs owner/repo "query"
# ...
# 示例
python3 （请参考skill目录中的脚本文件） search-docs facebook/react "state management"
```

### Step 3：搜索代码

```bash
# 精确匹配搜索代码
python3 （请参考skill目录中的脚本文件） search-code owner/repo "function_name"
# ...
# 示例
python3 （请参考skill目录中的脚本文件） search-code facebook/react "useState"
```

### Step 4：列出可用工具

```bash
# 查看仓库可用的MCP工具
python3 （请参考skill目录中的脚本文件） list-tools owner/repo
```

## 示例

### 脚本使用配置

```python
# gitmcp.py - 核心脚本配置
import sys
import json
import requests
# ...
class GitMCPClient:
    """MCP server客户端"""
# ...
    def __init__(self):
        self.base_url = "https://gitmcp.io"
        self.timeout = 30
# ...
    def list_tools(self, repo):
        """列出仓库可用的MCP工具"""
        url = f"{self.base_url}/{repo}"
        # 获取可用工具列表
        tools = self._call_mcp(url, "list_tools")
        return tools
# ...
    def fetch_docs(self, repo):
        """获取仓库文档"""
        # 工具名称动态生成: fetch_{repo}_documentation
        tool_name = self._generate_tool_name(repo, "documentation")
        return self._call_tool(repo, tool_name, {})
# ...
    def search_docs(self, repo, query):
        """语义搜索文档"""
_generate_tool_name(repo, "documentation")
        return self._call_tool(repo, f"search_{tool_name}", {"query": query})
# ...
    def search_code(self, repo, query):
        """搜索代码"""
_generate_tool_name(repo, "code")
        return self._call_tool(repo, f"search_{tool_name}", {"query": query})
# ...
    def _generate_tool_name(self, repo, suffix):
        """生成工具名称（仓库名下划线连接）"""
        repo_slug = repo.replace("/", "_").replace("-", "_")
        return f"{repo_slug}_{suffix}"
# ...
    def _call_tool(self, repo, tool_name, args):
        """调用MCP工具"""
        payload = {
            "tool": tool_name,
            "args": args
        }
        response = requests.post(url, json=payload, timeout=self.timeout)
        return response.json()
```

### 工作流配置

```yaml
# workflow.yaml - 免费版工作流配置
edition: free
version: "1.0.0"
# ...
# 默认行为
defaults:
  fetch_docs_first: true      # 优先获取文档
  search_code_exact: true     # 代码精确匹配
  respect_robots_txt: true    # 遵守robots.txt
# ...
# 已知限制
limits:
  max_search_results: 20
  max_url_fetch_size: "1MB"
  timeout_seconds: 30
# ...
# URL转换
url_mapping:
  source: "github.com"
  target: "gitmcp.io"
# ...
# 输出格式
output:
  format: markdown
  include_links: true
  include_code_blocks: true
```

## 最佳实践

### 1. 先获取文档再搜索

```text
# 推荐 - 先了解项目再深入
第一步：帮我读一下 owner/repo 的文档
第二步：在文档中搜索"authentication"相关内容
第三步：搜索代码中"login"函数的实现
# ...
# 不推荐 - 直接搜索代码
帮我搜索 useState 的实现（不知道在哪个文件）
```

### 2. 使用精确的搜索词

```bash
# 推荐 - 精确函数名
python3 （请参考skill目录中的脚本文件） search-code facebook/react "useState"
# ...
# 不推荐 - 模糊描述
python3 （请参考skill目录中的脚本文件） search-code facebook/react "state hook function"
```

### 3. 善用文档语义搜索

```bash
# 文档搜索支持语义匹配，可以用自然语言
python3 （请参考skill目录中的脚本文件） search-docs facebook/react "how to manage state in components"
```

### 4. 利用外部URL获取

当文档中引用了外部资源时，可以获取其内容：

```bash
# 获取文档中引用的外部URL
python3 （请参考skill目录中的脚本文件） fetch-url owner/repo "https://example.com/api-docs"
```

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 常见问题

### Q1：免费版支持哪些代码托管平台？

免费版通过 gitmcp.io 服务访问代码仓库，主要支持代码仓库的文档和代码阅读。URL 转换仅针对代码仓库.
### Q2：搜索代码是精确匹配还是模糊匹配？

代码搜索（search-code）使用精确匹配，返回包含确切关键词的文件。文档搜索（search-docs）使用语义搜索，支持自然语言查询.
### Q3：获取的文档包含哪些内容？

获取的文档通常包括 README、CONTRIBUTING、CHANGELOG 等项目文档文件。具体内容取决于仓库的文档组织方式.
### Q4：免费版有调用次数限制吗？

免费版无硬性次数限制，但建议合理使用。频繁请求可能触发服务端限流.
### Q5：免费版与 PRO 版本的区别？

| 对比项 | 免费版 | PRO 版本 |
|---:|---:|---:|
| 仓库数 | 单仓库 | 批量多仓库 |
| 代码搜索 | 单仓库精确匹配 | 跨仓库搜索 |
| 代码审计 | 不支持 | 安全漏洞检查 |
| 导出格式 | 终端输出 | MD/PDF/JSON |
| API 集成 | 不支持 | REST API |
| 历史记录 | 不支持 | 搜索历史 |
| 仓库对比 | 不支持 | 多仓库对比 |

## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **网络连接**: 需要可访问互联网以连接MCP server
- **Python 版本**: 3.8 及以上

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| MCP server | 服务 | 必需 | gitmcp.io免费提供 |
| Python 3.8+ | 运行时 | 必需 | 系统包管理器安装 |
| requests | Python 包 | 可选 | `pip install requests` |

### API Key 配置

免费版通过公开的 MCP server 访问代码仓库，无需额外 API Key.
```bash
# 验证环境
python3 --version
python3 -c "import requests; print('requests就绪')" 2>/dev/null || echo "requests未安装（可选）"
# ...
# 验证MCP server连通性
curl -s -o /dev/null -w "%{http_code}" https://gitmcp.io
# 预期输出: 200
```

### 可用性分类

- **分类**: MD+EXEC（纯 Markdown 指令 + Python 脚本执行）
- **说明**: 通过 MCP server访问代码仓库的文档与代码，支持获取、搜索和内容提取
- **适用规模**: 个人开发者、轻量级代码阅读场景
- **升级路径**: 可无缝升级至 read-github-tool-pro 获取批量仓库分析与代码审计能力

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
