from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_accounts(
) -> Dict[str, Any]:
    """
    Discover all organizations/accounts in Source Cooperative.

Returns:
    List of account IDs (e.g., ['clarkcga', 'harvard-lil', 'youssef-harby'])

Example:
    >>> await list_accounts()
    ['addresscloud', 'clarkcga', 'harvard-lil', ...]
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072576515", "list_accounts", arguments)

def list_products(
    account_id: Optional[null] = None,
    featured_only: Optional[bool] = False,
    include_unpublished: Optional[bool] = True,
    include_file_count: Optional[bool] = True
) -> Dict[str, Any]:
    """
    List products (datasets) in Source Cooperative with hybrid S3 + API approach.

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
    
    Args:
        account_id: null
        featured_only: null
        include_unpublished: null
        include_file_count: null
    
    Returns:
        null
    """
    arguments = {
        "account_id": account_id,
        "featured_only": featured_only,
        "include_unpublished": include_unpublished,
        "include_file_count": include_file_count
    }
    
    return call_api("1777419072576515", "list_products", arguments)

def get_product_details(
    account_id: str,
    product_id: str
) -> Dict[str, Any]:
    """
    Get comprehensive metadata for a specific product.
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
    
    Args:
        account_id: null
        product_id: null
    
    Returns:
        null
    """
    arguments = {
        "account_id": account_id,
        "product_id": product_id
    }
    
    return call_api("1777419072576515", "get_product_details", arguments)

def list_product_files(
    account_id: str,
    product_id: str,
    prefix: Optional[str] = "",
    max_files: Optional[int] = 1000.0,
    show_tree: Optional[bool] = True
) -> Dict[str, Any]:
    """
    List all files in a product with full S3 paths ready for analysis.
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
    
    Args:
        account_id: null
        product_id: null
        prefix: null
        max_files: null
        show_tree: null
    
    Returns:
        null
    """
    arguments = {
        "account_id": account_id,
        "product_id": product_id,
        "prefix": prefix,
        "max_files": max_files,
        "show_tree": show_tree
    }
    
    return call_api("1777419072576515", "list_product_files", arguments)

def get_file_metadata(
    path: str
) -> Dict[str, Any]:
    """
    Get metadata for a specific file without downloading it.
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
    
    Args:
        path: null
    
    Returns:
        null
    """
    arguments = {
        "path": path
    }
    
    return call_api("1777419072576515", "get_file_metadata", arguments)

def search(
    query: str
) -> Dict[str, Any]:
    """
    Search for products across ALL accounts with smart fuzzy matching.
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
    
    Args:
        query: null
    
    Returns:
        null
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777419072576515", "search", arguments)

