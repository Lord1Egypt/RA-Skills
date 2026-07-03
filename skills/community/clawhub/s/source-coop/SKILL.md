---
name: 地理空间数据访问服务
description: 一个用于发现和访问800TB+地理空间数据的MCP服务器，支持AI客户端通过JSON-RPC协议进行交互，提供智能搜索和高效数据访问功能。
version: 1.0.0
---

# 地理空间数据访问服务

一个用于发现和访问800TB+地理空间数据的MCP服务器，支持AI客户端通过JSON-RPC协议进行交互，提供智能搜索和高效数据访问功能。

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
| Discover all organizations/accounts in Source Cooperative.

Returns:
    List of account IDs (e.g., ['clarkcga', 'harvard-lil', 'youssef-harby'])

Example:
    >>> await list_accounts()
    ['addresscloud', 'clarkcga', 'harvard-lil', ...] | `scripts.tools.list_accounts` |
| List products (datasets) in Source Cooperative with hybrid S3 + API approach.

DEFAULT: Uses S3 direct scan (fast, includes ALL products with file counts).
Set include_unpublished=False for published-only with rich metadata from API.

Args:
    account_id: Filter by specific account. REQUIRED for S3 mode (default).
               If None with include_unpublished=False, lists published from all accounts.
    featured_only: Only return featured/curated products (API mode only).
    include_unpublished: If True (default), scan S3 for ALL products including unpublished.
                       If False, use API for published products with rich metadata.
    include_file_count: Count files in each product (default True, only in S3 mode).

Returns:
    S3 mode (default): Basic info (product_id, s3_prefix, file_count) - fast!
    API mode: Rich metadata (product_id, title, description, dates) - slower

Performance:
    - S3 mode (default): ~240ms, includes unpublished products + file counts
    - API mode (include_unpublished=False): ~500ms, rich metadata, published only

Examples:
    >>> # ALL products with file counts (DEFAULT - fast!)
    >>> await list_products(account_id="youssef-harby")
    [
        {"product_id": "exiobase-3", "source": "s3", "file_count": 1000, ...},
        {"product_id": "egms-copernicus", "source": "s3", "file_count": 53, ...},
        ...
    ]

    >>> # Published products with rich metadata (API mode)
    >>> await list_products(account_id="youssef-harby", include_unpublished=False)
    [{"product_id": "egms-copernicus", "title": "...", "description": "...", ...}]

    >>> # Fast mode without file counts
    >>> await list_products(account_id="youssef-harby", include_file_count=False)
    [{"product_id": "exiobase-3", "source": "s3", ...}]

    >>> # Featured products only (requires API mode)
    >>> await list_products(featured_only=True, include_unpublished=False)
    [{"product_id": "gov-data", "featured": 1, ...}] | `scripts.tools.list_products` |
| Get comprehensive metadata for a specific product.
Always includes README content if found in the product root directory.

Args:
    account_id: Account ID (e.g., "harvard-lil")
    product_id: Product ID (e.g., "gov-data")

Returns:
    Full product metadata including account info, storage config, roles, tags
    Always includes 'readme' field with content and metadata (if README exists)

Example:
    >>> await get_product_details("harvard-lil", "gov-data")
    {
        "title": "Archive of data.gov",
        "description": "...",
        "account": {"name": "Harvard Library Innovation Lab", ...},
        "readme": {
            "found": true,
            "content": "# Archive of data.gov...",
            "size": 5344,
            "path": "harvard-lil/gov-data/README.md"
        },
        ...
    } | `scripts.tools.get_product_details` |
| List all files in a product with full S3 paths ready for analysis.
Optionally show a hierarchical tree visualization (optimized for LLM tokens).

Args:
    account_id: Account ID
    product_id: Product ID
    prefix: Optional prefix to filter files (subdirectory path)
    max_files: Maximum files to return (default 1000)
    show_tree: If True, return tree visualization only (more token-efficient, default True)

Returns:
    Dict with either files list OR tree visualization (not both to save tokens)

Example (List mode - detailed metadata):
    >>> result = await list_product_files("harvard-lil", "gov-data", "metadata/")
    >>> print(result["files"][0])
    {
        "key": "harvard-lil/gov-data/metadata/metadata.jsonl.zip",
        "s3_uri": "s3://us-west-2.opendata.source.coop/harvard-lil/gov-data/metadata/metadata.jsonl.zip",
        "http_url": "https://data.source.coop/harvard-lil/gov-data/metadata/metadata.jsonl.zip",
        "size": 1012127330,
        "last_modified": "2025-02-06T16:20:22+00:00"
    }

Example (Tree mode - token optimized):
    >>> result = await list_product_files("harvard-lil", "gov-data", show_tree=True)
    >>> print(result["tree"])
    s3://us-west-2.opendata.source.coop/harvard-lil/gov-data/
    ├── README.md (5.2 KB) → s3://...README.md
    ├── metadata/
    │   └── metadata.jsonl.zip (965.4 MB) → s3://...metadata.jsonl.zip
    └── data/
        └── datasets.parquet (128.5 MB) → s3://...datasets.parquet

Example (Partitioned data - smart summarization):
    >>> result = await list_product_files("account", "product", show_tree=True)
    >>> print(result["tree"])
    s3://us-west-2.opendata.source.coop/account/product/
    ├── year={1995,1996,...,2007 (13 total)}/ [partitioned]
    │   └── format={ixi,pxp}/ [partitioned]
    │       └── matrix={F_impacts,F_satellite,Y,Z}/ [partitioned]
    │           └── data.parquet (5.1 MB)

    Note: Shows first,second,...,last (total) for >10 values; lists all for ≤10
    Tree mode saves ~70% tokens + smart partition detection saves 96%+ more | `scripts.tools.list_product_files` |
| Get metadata for a specific file without downloading it.
Uses obstore's head operation for efficient metadata retrieval.

Args:
    path: S3 URI (s3://...) or relative path (account_id/product_id/file)

Returns:
    File metadata: size, content-type, last-modified, etag, URLs

Example:
    >>> await get_file_metadata("harvard-lil/gov-data/README.md")
    {
        "key": "harvard-lil/gov-data/README.md",
        "content_type": "binary/octet-stream",
        "content_length": 5344,
        "last_modified": "2025-02-06T16:29:24+00:00",
        ...
    } | `scripts.tools.get_file_metadata` |
| Search for products across ALL accounts with smart fuzzy matching.
Handles typos, partial matches, and incomplete words using 60% similarity threshold.

**Hybrid Search** - Automatically searches across:
- All 94+ organizations
- ALL products (published + unpublished)
- All fields: title, description, product_id

Published products: Full metadata (title, description, product_id)
Unpublished products: product_id only (no title/description available)

Args:
    query: Search keyword (supports typos and partial matches)

Returns:
    **Top 5** matching accounts or products (sorted by relevance score)

Performance:
    ~5-8s (parallel 2-level S3 scan + top 5 API enrichment)

    Performance breakdown:
    - S3 parallel listing: ~2.4s (94 accounts + 354 products)
    - Fuzzy matching: <1s (in-memory processing)
    - API enrichment: ~2-5s (only top 5 results)

    **11x faster** than sequential approach (was ~27s)
    **Uses 2-level delimiter listing** (not full recursive scan)

Examples:
    >>> # Exact match
    >>> results = await search("climate")

    >>> # Fuzzy match (handles typos)
    >>> results = await search("climte")  # Finds "climate"
    >>> results = await search("exiopase")  # Finds "exiobase-3" (includes unpublished!)

    >>> # Partial match
    >>> results = await search("geo")  # Finds "geospatial", "geocoding", etc.

    >>> # Result formats
    >>> print(results[0])  # Account match
    {
        "type": "account",
        "account_id": "harvard-lil",
        "match_string": "harvard-lil",
        "search_score": 9.5,
        "similarity": 0.95,
        "matched_fields": ["account_id"]
    }

    >>> print(results[1])  # Product match
    {
        "type": "product",
        "account_id": "youssef-harby",
        "product_id": "exiobase-3",
        "match_string": "youssef-harby/exiobase-3",
        "title": "",  # Empty for unpublished products
        "description": "",  # Empty for unpublished products
        "search_score": 8.2,
        "similarity": 0.82,
        "matched_fields": ["product_id"]
    } | `scripts.tools.search` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.list_accounts
工具描述：Discover all organizations/accounts in Source Cooperative.

Returns:
    List of account IDs (e.g., ['clarkcga', 'harvard-lil', 'youssef-harby'])

Example:
    >>> await list_accounts()
    ['addresscloud', 'clarkcga', 'harvard-lil', ...]
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.list_products
工具描述：List products (datasets) in Source Cooperative with hybrid S3 + API approach.

DEFAULT: Uses S3 direct scan (fast, includes ALL products with file counts).
Set include_unpublished=False for published-only with rich metadata from API.

Args:
    account_id: Filter by specific account. REQUIRED for S3 mode (default).
               If None with include_unpublished=False, lists published from all accounts.
    featured_only: Only return featured/curated products (API mode only).
    include_unpublished: If True (default), scan S3 for ALL products including unpublished.
                       If False, use API for published products with rich metadata.
    include_file_count: Count files in each product (default True, only in S3 mode).

Returns:
    S3 mode (default): Basic info (product_id, s3_prefix, file_count) - fast!
    API mode: Rich metadata (product_id, title, description, dates) - slower

Performance:
    - S3 mode (default): ~240ms, includes unpublished products + file counts
    - API mode (include_unpublished=False): ~500ms, rich metadata, published only

Examples:
    >>> # ALL products with file counts (DEFAULT - fast!)
    >>> await list_products(account_id="youssef-harby")
    [
        {"product_id": "exiobase-3", "source": "s3", "file_count": 1000, ...},
        {"product_id": "egms-copernicus", "source": "s3", "file_count": 53, ...},
        ...
    ]

    >>> # Published products with rich metadata (API mode)
    >>> await list_products(account_id="youssef-harby", include_unpublished=False)
    [{"product_id": "egms-copernicus", "title": "...", "description": "...", ...}]

    >>> # Fast mode without file counts
    >>> await list_products(account_id="youssef-harby", include_file_count=False)
    [{"product_id": "exiobase-3", "source": "s3", ...}]

    >>> # Featured products only (requires API mode)
    >>> await list_products(featured_only=True, include_unpublished=False)
    [{"product_id": "gov-data", "featured": 1, ...}]
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|account_id|null|false| |null|
|featured_only|boolean|false|false|null|
|include_unpublished|boolean|false|true|null|
|include_file_count|boolean|false|true|null|

---

## scripts.tools.get_product_details
工具描述：Get comprehensive metadata for a specific product.
Always includes README content if found in the product root directory.

Args:
    account_id: Account ID (e.g., "harvard-lil")
    product_id: Product ID (e.g., "gov-data")

Returns:
    Full product metadata including account info, storage config, roles, tags
    Always includes 'readme' field with content and metadata (if README exists)

Example:
    >>> await get_product_details("harvard-lil", "gov-data")
    {
        "title": "Archive of data.gov",
        "description": "...",
        "account": {"name": "Harvard Library Innovation Lab", ...},
        "readme": {
            "found": true,
            "content": "# Archive of data.gov...",
            "size": 5344,
            "path": "harvard-lil/gov-data/README.md"
        },
        ...
    }
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|account_id|string|true| |null|
|product_id|string|true| |null|

---

## scripts.tools.list_product_files
工具描述：List all files in a product with full S3 paths ready for analysis.
Optionally show a hierarchical tree visualization (optimized for LLM tokens).

Args:
    account_id: Account ID
    product_id: Product ID
    prefix: Optional prefix to filter files (subdirectory path)
    max_files: Maximum files to return (default 1000)
    show_tree: If True, return tree visualization only (more token-efficient, default True)

Returns:
    Dict with either files list OR tree visualization (not both to save tokens)

Example (List mode - detailed metadata):
    >>> result = await list_product_files("harvard-lil", "gov-data", "metadata/")
    >>> print(result["files"][0])
    {
        "key": "harvard-lil/gov-data/metadata/metadata.jsonl.zip",
        "s3_uri": "s3://us-west-2.opendata.source.coop/harvard-lil/gov-data/metadata/metadata.jsonl.zip",
        "http_url": "https://data.source.coop/harvard-lil/gov-data/metadata/metadata.jsonl.zip",
        "size": 1012127330,
        "last_modified": "2025-02-06T16:20:22+00:00"
    }

Example (Tree mode - token optimized):
    >>> result = await list_product_files("harvard-lil", "gov-data", show_tree=True)
    >>> print(result["tree"])
    s3://us-west-2.opendata.source.coop/harvard-lil/gov-data/
    ├── README.md (5.2 KB) → s3://...README.md
    ├── metadata/
    │   └── metadata.jsonl.zip (965.4 MB) → s3://...metadata.jsonl.zip
    └── data/
        └── datasets.parquet (128.5 MB) → s3://...datasets.parquet

Example (Partitioned data - smart summarization):
    >>> result = await list_product_files("account", "product", show_tree=True)
    >>> print(result["tree"])
    s3://us-west-2.opendata.source.coop/account/product/
    ├── year={1995,1996,...,2007 (13 total)}/ [partitioned]
    │   └── format={ixi,pxp}/ [partitioned]
    │       └── matrix={F_impacts,F_satellite,Y,Z}/ [partitioned]
    │           └── data.parquet (5.1 MB)

    Note: Shows first,second,...,last (total) for >10 values; lists all for ≤10
    Tree mode saves ~70% tokens + smart partition detection saves 96%+ more
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|account_id|string|true| |null|
|product_id|string|true| |null|
|prefix|string|false|""|null|
|max_files|integer|false|1000.0|null|
|show_tree|boolean|false|true|null|

---

## scripts.tools.get_file_metadata
工具描述：Get metadata for a specific file without downloading it.
Uses obstore's head operation for efficient metadata retrieval.

Args:
    path: S3 URI (s3://...) or relative path (account_id/product_id/file)

Returns:
    File metadata: size, content-type, last-modified, etag, URLs

Example:
    >>> await get_file_metadata("harvard-lil/gov-data/README.md")
    {
        "key": "harvard-lil/gov-data/README.md",
        "content_type": "binary/octet-stream",
        "content_length": 5344,
        "last_modified": "2025-02-06T16:29:24+00:00",
        ...
    }
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|path|string|true| |null|

---

## scripts.tools.search
工具描述：Search for products across ALL accounts with smart fuzzy matching.
Handles typos, partial matches, and incomplete words using 60% similarity threshold.

**Hybrid Search** - Automatically searches across:
- All 94+ organizations
- ALL products (published + unpublished)
- All fields: title, description, product_id

Published products: Full metadata (title, description, product_id)
Unpublished products: product_id only (no title/description available)

Args:
    query: Search keyword (supports typos and partial matches)

Returns:
    **Top 5** matching accounts or products (sorted by relevance score)

Performance:
    ~5-8s (parallel 2-level S3 scan + top 5 API enrichment)

    Performance breakdown:
    - S3 parallel listing: ~2.4s (94 accounts + 354 products)
    - Fuzzy matching: <1s (in-memory processing)
    - API enrichment: ~2-5s (only top 5 results)

    **11x faster** than sequential approach (was ~27s)
    **Uses 2-level delimiter listing** (not full recursive scan)

Examples:
    >>> # Exact match
    >>> results = await search("climate")

    >>> # Fuzzy match (handles typos)
    >>> results = await search("climte")  # Finds "climate"
    >>> results = await search("exiopase")  # Finds "exiobase-3" (includes unpublished!)

    >>> # Partial match
    >>> results = await search("geo")  # Finds "geospatial", "geocoding", etc.

    >>> # Result formats
    >>> print(results[0])  # Account match
    {
        "type": "account",
        "account_id": "harvard-lil",
        "match_string": "harvard-lil",
        "search_score": 9.5,
        "similarity": 0.95,
        "matched_fields": ["account_id"]
    }

    >>> print(results[1])  # Product match
    {
        "type": "product",
        "account_id": "youssef-harby",
        "product_id": "exiobase-3",
        "match_string": "youssef-harby/exiobase-3",
        "title": "",  # Empty for unpublished products
        "description": "",  # Empty for unpublished products
        "search_score": 8.2,
        "similarity": 0.82,
        "matched_fields": ["product_id"]
    }
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|

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