---
name: 网络研究助手
description: 一个提供网络研究和发现功能的综合模型上下文协议（MCP）服务器，包含13种工具用于搜索、爬取和分析网络内容。
version: 1.0.0
---

# 网络研究助手

一个提供网络研究和发现功能的综合模型上下文协议（MCP）服务器，包含13种工具用于搜索、爬取和分析网络内容。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Use this first to gather fresh web search results via the local SearXNG instance. | `scripts.tools.web_search` |
| Fetch a URL with crawl4ai when you need the actual page text for quoting or analysis. | `scripts.tools.crawl_url` |
| 
Look up package information from npm, PyPI, crates.io, or Go modules.

Returns version, downloads, license, dependencies, security status, and repository links.
Use this to quickly evaluate libraries before adding them to your project.

Examples:
- package_info("express", reasoning="Need web framework", registry="npm")
- package_info("requests", reasoning="HTTP client for API", registry="pypi")
- package_info("serde", reasoning="JSON serialization", registry="crates")
 | `scripts.tools.package_info` |
| 
Search for code examples, tutorials, and technical articles.

Optimized for finding practical examples and learning resources. Can optionally filter by
time range for the most recent content. Perfect for learning new APIs, finding usage patterns,
or discovering how others solve specific technical problems.

Content Types:
- 'code': GitHub repos, code snippets, gists, Stack Overflow code examples
- 'articles': Blog posts, tutorials, documentation, technical articles
- 'both': Mix of code and written content (default)

Time Ranges:
- 'all': Search all available content (default, recommended for best results)
- 'year', 'month', 'week', 'day': Filter to recent content only

Examples:
- search_examples("FastAPI dependency injection examples", content_type="code")
- search_examples("React hooks tutorial", content_type="articles", time_range="year")
- search_examples("Rust lifetime examples", content_type="both")
 | `scripts.tools.search_examples` |
| 
Search for high-quality stock images using Pixabay.

Returns royalty-free images that are safe to use. Perfect for finding photos,
illustrations, and vector graphics for projects, presentations, or design work.

Image Types:
- 'photo': Real photographs
- 'illustration': Digital illustrations and artwork
- 'vector': Vector graphics (SVG format available)
- 'all': All types (default)

Examples:
- search_images("mountain landscape", image_type="photo")
- search_images("business icons", image_type="vector")
- search_images("technology background", orientation="horizontal")
 | `scripts.tools.search_images` |
| 
Search for packages by keywords or description across registries.

Use this to find packages that solve a specific problem or provide certain functionality.
Perfect for discovering libraries when you know what you need but not the package name.

Examples:
- package_search("web framework", reasoning="Need backend framework", registry="npm")
- package_search("json parsing", reasoning="Data processing", registry="pypi")
 | `scripts.tools.package_search` |
| 
Fetch GitHub repository information and health metrics.

Returns stars, forks, issues, recent activity, language, license, and description.
Use this to evaluate open source projects before using them.

Examples:
- github_repo("microsoft/vscode", reasoning="Evaluate editor project")
- github_repo("https://github.com/facebook/react", reasoning="Research UI framework")
 | `scripts.tools.github_repo` |
| 
Find solutions for error messages and stack traces from Stack Overflow and GitHub.

Takes an error message or stack trace and finds relevant solutions with code examples.
Automatically detects language and framework, extracts key error information, and
searches for the best solutions ranked by votes and relevance.

Perfect for:
- Debugging production errors
- Understanding cryptic error messages
- Finding working code fixes
- Learning from similar issues

Examples:
- translate_error("TypeError: Cannot read property 'map' of undefined", reasoning="Debugging React app crash")
- translate_error("CORS policy: No 'Access-Control-Allow-Origin' header", reasoning="Fixing API integration", framework="FastAPI")
- translate_error("error[E0382]: borrow of moved value", reasoning="Learning Rust ownership", language="rust")
 | `scripts.tools.translate_error` |
| 
Search and fetch official API documentation with examples and explanations.

Documentation-first approach: fetches human-written docs with context, examples,
and best practices. Much more useful than OpenAPI specs alone.

Discovery strategy:
1. Try common URL patterns (docs.{api}.com, {api}.com/docs, etc.)
2. If patterns fail, search for "{api} API official documentation"
3. Crawl discovered docs and extract relevant content

No hardcoded URLs - works for ANY API by discovering docs dynamically.

Examples:
- api_docs("stripe", "create customer", reasoning="Setting up payments")
- api_docs("github", "create repository", reasoning="Automating repo creation")
- api_docs("spartan", "button component", reasoning="Learning UI library")
 | `scripts.tools.api_docs` |
| 
Extract structured data from web pages.

Extracts tables, lists, or specific fields from HTML pages and returns
structured data. Much more efficient than parsing full page text.

Extract Types:
- "table": Extract HTML tables as list of dicts
- "list": Extract lists (ul/ol/dl) as structured list
- "fields": Extract specific elements using CSS selectors
- "json-ld": Extract JSON-LD structured data
- "auto": Automatically detect and extract structured content

Examples:
- extract_data("https://pypi.org/project/fastapi/", reasoning="Get package info")
- extract_data("https://github.com/user/repo/releases", reasoning="Get releases", extract_type="list")
- extract_data(
    "https://example.com/product",
    reasoning="Extract product details",
    extract_type="fields",
    selectors={"price": ".price", "title": "h1.product-name"}
  )
 | `scripts.tools.extract_data` |
| 
Compare multiple technologies, frameworks, or libraries side-by-side.

Automatically gathers information about each technology and presents
a structured comparison to help make informed decisions.

Categories:
- "framework": Web frameworks (React, Vue, Angular, etc.)
- "library": JavaScript/Python/etc. libraries
- "database": Databases (PostgreSQL, MongoDB, etc.)
- "language": Programming languages (Python, Go, Rust, etc.)
- "tool": Build tools, CLIs, etc. (Webpack, Vite, etc.)
- "auto": Auto-detect category

Examples:
- compare_tech(["React", "Vue", "Svelte"], reasoning="Choose framework for new project")
- compare_tech(["PostgreSQL", "MongoDB"], category="database", reasoning="Database for user data")
- compare_tech(["FastAPI", "Flask"], aspects=["performance", "learning_curve"], reasoning="Python web framework")
 | `scripts.tools.compare_tech` |
| Get changelog and release notes for a package. | `scripts.tools.get_changelog` |
| Check if an API service or platform is experiencing issues. | `scripts.tools.check_service_status` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.web_search
工具描述：Use this first to gather fresh web search results via the local SearXNG instance.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|reasoning|string|true| |null|
|category|string|false|"general"|null|
|max_results|integer|false|5.0|null|

---

## scripts.tools.crawl_url
工具描述：Fetch a URL with crawl4ai when you need the actual page text for quoting or analysis.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|url|string|true| |null|
|reasoning|string|true| |null|
|max_chars|integer|false|8000.0|null|

---

## scripts.tools.package_info
工具描述：
Look up package information from npm, PyPI, crates.io, or Go modules.

Returns version, downloads, license, dependencies, security status, and repository links.
Use this to quickly evaluate libraries before adding them to your project.

Examples:
- package_info("express", reasoning="Need web framework", registry="npm")
- package_info("requests", reasoning="HTTP client for API", registry="pypi")
- package_info("serde", reasoning="JSON serialization", registry="crates")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|name|string|true| |null|
|reasoning|string|true| |null|
|registry|string|false|"npm"|null|

---

## scripts.tools.search_examples
工具描述：
Search for code examples, tutorials, and technical articles.

Optimized for finding practical examples and learning resources. Can optionally filter by
time range for the most recent content. Perfect for learning new APIs, finding usage patterns,
or discovering how others solve specific technical problems.

Content Types:
- 'code': GitHub repos, code snippets, gists, Stack Overflow code examples
- 'articles': Blog posts, tutorials, documentation, technical articles
- 'both': Mix of code and written content (default)

Time Ranges:
- 'all': Search all available content (default, recommended for best results)
- 'year', 'month', 'week', 'day': Filter to recent content only

Examples:
- search_examples("FastAPI dependency injection examples", content_type="code")
- search_examples("React hooks tutorial", content_type="articles", time_range="year")
- search_examples("Rust lifetime examples", content_type="both")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|reasoning|string|true| |null|
|content_type|string|false|"both"|null|
|time_range|string|false|"all"|null|
|max_results|integer|false|5.0|null|

---

## scripts.tools.search_images
工具描述：
Search for high-quality stock images using Pixabay.

Returns royalty-free images that are safe to use. Perfect for finding photos,
illustrations, and vector graphics for projects, presentations, or design work.

Image Types:
- 'photo': Real photographs
- 'illustration': Digital illustrations and artwork
- 'vector': Vector graphics (SVG format available)
- 'all': All types (default)

Examples:
- search_images("mountain landscape", image_type="photo")
- search_images("business icons", image_type="vector")
- search_images("technology background", orientation="horizontal")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|reasoning|string|true| |null|
|image_type|string|false|"all"|null|
|orientation|string|false|"all"|null|
|max_results|integer|false|10.0|null|

---

## scripts.tools.package_search
工具描述：
Search for packages by keywords or description across registries.

Use this to find packages that solve a specific problem or provide certain functionality.
Perfect for discovering libraries when you know what you need but not the package name.

Examples:
- package_search("web framework", reasoning="Need backend framework", registry="npm")
- package_search("json parsing", reasoning="Data processing", registry="pypi")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|reasoning|string|true| |null|
|registry|string|false|"npm"|null|
|max_results|integer|false|5.0|null|

---

## scripts.tools.github_repo
工具描述：
Fetch GitHub repository information and health metrics.

Returns stars, forks, issues, recent activity, language, license, and description.
Use this to evaluate open source projects before using them.

Examples:
- github_repo("microsoft/vscode", reasoning="Evaluate editor project")
- github_repo("https://github.com/facebook/react", reasoning="Research UI framework")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|repo|string|true| |null|
|reasoning|string|true| |null|
|include_commits|boolean|false|true|null|

---

## scripts.tools.translate_error
工具描述：
Find solutions for error messages and stack traces from Stack Overflow and GitHub.

Takes an error message or stack trace and finds relevant solutions with code examples.
Automatically detects language and framework, extracts key error information, and
searches for the best solutions ranked by votes and relevance.

Perfect for:
- Debugging production errors
- Understanding cryptic error messages
- Finding working code fixes
- Learning from similar issues

Examples:
- translate_error("TypeError: Cannot read property 'map' of undefined", reasoning="Debugging React app crash")
- translate_error("CORS policy: No 'Access-Control-Allow-Origin' header", reasoning="Fixing API integration", framework="FastAPI")
- translate_error("error[E0382]: borrow of moved value", reasoning="Learning Rust ownership", language="rust")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|error_message|string|true| |null|
|reasoning|string|true| |null|
|language|null|false| |null|
|framework|null|false| |null|
|max_results|integer|false|5.0|null|

---

## scripts.tools.api_docs
工具描述：
Search and fetch official API documentation with examples and explanations.

Documentation-first approach: fetches human-written docs with context, examples,
and best practices. Much more useful than OpenAPI specs alone.

Discovery strategy:
1. Try common URL patterns (docs.{api}.com, {api}.com/docs, etc.)
2. If patterns fail, search for "{api} API official documentation"
3. Crawl discovered docs and extract relevant content

No hardcoded URLs - works for ANY API by discovering docs dynamically.

Examples:
- api_docs("stripe", "create customer", reasoning="Setting up payments")
- api_docs("github", "create repository", reasoning="Automating repo creation")
- api_docs("spartan", "button component", reasoning="Learning UI library")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|api_name|string|true| |null|
|reasoning|string|true| |null|
|topic|string|true| |null|
|max_results|integer|false|2.0|null|

---

## scripts.tools.extract_data
工具描述：
Extract structured data from web pages.

Extracts tables, lists, or specific fields from HTML pages and returns
structured data. Much more efficient than parsing full page text.

Extract Types:
- "table": Extract HTML tables as list of dicts
- "list": Extract lists (ul/ol/dl) as structured list
- "fields": Extract specific elements using CSS selectors
- "json-ld": Extract JSON-LD structured data
- "auto": Automatically detect and extract structured content

Examples:
- extract_data("https://pypi.org/project/fastapi/", reasoning="Get package info")
- extract_data("https://github.com/user/repo/releases", reasoning="Get releases", extract_type="list")
- extract_data(
    "https://example.com/product",
    reasoning="Extract product details",
    extract_type="fields",
    selectors={"price": ".price", "title": "h1.product-name"}
  )

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|url|string|true| |null|
|reasoning|string|true| |null|
|extract_type|string|false|"auto"|null|
|selectors|null|false| |null|
|max_items|integer|false|100.0|null|

---

## scripts.tools.compare_tech
工具描述：
Compare multiple technologies, frameworks, or libraries side-by-side.

Automatically gathers information about each technology and presents
a structured comparison to help make informed decisions.

Categories:
- "framework": Web frameworks (React, Vue, Angular, etc.)
- "library": JavaScript/Python/etc. libraries
- "database": Databases (PostgreSQL, MongoDB, etc.)
- "language": Programming languages (Python, Go, Rust, etc.)
- "tool": Build tools, CLIs, etc. (Webpack, Vite, etc.)
- "auto": Auto-detect category

Examples:
- compare_tech(["React", "Vue", "Svelte"], reasoning="Choose framework for new project")
- compare_tech(["PostgreSQL", "MongoDB"], category="database", reasoning="Database for user data")
- compare_tech(["FastAPI", "Flask"], aspects=["performance", "learning_curve"], reasoning="Python web framework")

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|technologies|array|true| |null|
|reasoning|string|true| |null|
|category|string|false|"auto"|null|
|aspects|null|false| |null|
|max_results_per_tech|integer|false|3.0|null|

---

## scripts.tools.get_changelog
工具描述：Get changelog and release notes for a package.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|package|string|true| |null|
|reasoning|string|true| |null|
|registry|string|false|"auto"|null|
|max_releases|integer|false|5.0|null|

---

## scripts.tools.check_service_status
工具描述：Check if an API service or platform is experiencing issues.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|service|string|true| |null|
|reasoning|string|true| |null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据