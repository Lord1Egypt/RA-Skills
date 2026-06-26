---
name: "SiYuan Note"
description: SiYuan Note (思源笔记) API client - Complete notebook, document and block management
homepage: https://github.com/siyuan-note/siyuan
api_docs: https://www.siyuan-note.club/apis
version: "1.0.3"
author: "weiwei"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"] },
        "install": [{ "kind": "none", "label": "No external deps required" }],
      },
  }
---

# SiYuan Note (思源笔记)

A clean API client for SiYuan Note, providing access to your notes via the local HTTP API.

**ClawHub**: https://clawhub.ai/weiwei2027/siyuan  
**Install**: `clawhub install siyuan`  
**Version**: 1.0.1

## Prerequisites

- SiYuan running with API enabled (Settings → About → API)
- API token from SiYuan settings

## Configuration

1. Get your API token from SiYuan: **Settings → About → API → Copy Token**

2. Create/edit `~/.openclaw/workspace/skills/siyuan/config.yaml`:

```yaml
siyuan:
  base_url: "http://127.0.0.1:6806"  # Check SiYuan settings for actual port
  token: "your-api-token-here"       # Paste your token here
  timeout: 30
  retry: 3
```

**Note**: SiYuan may use different ports on restart (default 6806, but could be 34669, etc.). Check the current port in SiYuan settings.

## Python Client API

### Initialize Client

```python
from siyuan_client import SiYuanClient

# Use config.yaml settings
client = SiYuanClient()

# Or explicit configuration
client = SiYuanClient(
    base_url="http://127.0.0.1:6806",
    token="your-token"
)
```

### System Operations

```python
# Get system version
version = client.system_version()
print(f"SiYuan v{version}")

# Get current time
timestamp = client.current_time()
```

### Notebook Operations

```python
# List all notebooks
notebooks = client.list_notebooks()
for nb in notebooks:
    print(f"{nb['name']}: {nb['id']}")

# Create new notebook
new_nb = client.create_notebook("我的新项目")

# Open/close notebook (load/unload from memory)
client.open_notebook("notebook-id")
client.close_notebook("notebook-id")

# Rename notebook
client.rename_notebook("notebook-id", "新名称")

# Get/set notebook configuration
conf = client.get_notebook_conf("notebook-id")
client.set_notebook_conf("notebook-id", {"dailyNoteSavePath": "/daily"})

# Remove notebook
client.remove_notebook("notebook-id")
```

### Document Operations

```python
# Export document as Markdown
result = client.export_md_content("doc-id")
print(result['hPath'])      # Human-readable path
print(result['content'])    # Markdown content

# Create new document
new_doc = client.create_doc_with_md(
    notebook_id="notebook-id",
    path="folder/document-name",  # Supports nested paths
    markdown="# Title\n\nContent here"
)

# Rename document
client.rename_doc("notebook-id", "/old-path", "新标题")
client.rename_doc_by_id("doc-id", "新标题")

# Get document paths
hpath = client.get_hpath_by_id("doc-id")  # Human-readable path
path_info = client.get_path_by_id("doc-id")  # Storage path
ids = client.get_ids_by_hpath("notebook-id", "/人类可读路径")

# Move documents by ID
client.move_docs_by_id(
    doc_ids=["doc-id-1", "doc-id-2"],
    to_id="target-notebook-or-doc-id"
)

# Move documents by path
client.move_docs(
    from_paths=["/path/to/doc1.sy", "/path/to/doc2.sy"],
    to_notebook="target-notebook-id",
    to_path="/subfolder"
)

# Remove document by notebook and path
client.remove_doc("notebook-id", "/path/to/doc.sy")

# Remove document by ID
client.remove_doc_by_id("doc-id")
```

### Block Operations

```python
# Insert blocks at specific position
blocks = client.insert_block(
    data_type="markdown",
    data="## New Section\n\nSome content",
    parent_id="doc-id",      # Optional: parent block/document
    previous_id="block-id",  # Optional: insert after this block
    next_id="block-id"       # Optional: insert before this block
)

# Prepend to beginning of document
blocks = client.prepend_block(
    data_type="markdown",
    data="# Title\n",
    parent_id="doc-id"
)

# Append to end of document
blocks = client.append_block(
    data_type="markdown",
    data="\n---\nFooter here",
    parent_id="doc-id"
)

# Update block content
client.update_block(
    data_type="markdown",
    data="Updated content",
    block_id="block-id"
)

# Delete block
client.delete_block("block-id")

# Move block
client.move_block(
    block_id="block-id",
    previous_id="target-block-id",  # Optional: insert after this block
    parent_id="parent-block-id"     # Optional: set parent (at least one required)
)

# Fold/unfold (collapse/expand) blocks
client.fold_block("block-id")
client.unfold_block("block-id")

# Transfer block references
client.transfer_block_ref(
    from_id="source-block-id",
    to_id="target-block-id",
    ref_ids=["ref-1", "ref-2"]  # Optional: specific refs to transfer
)

# Get block in Kramdown format
kramdown = client.get_block_kramdown("block-id")

# Get child blocks
children = client.get_child_blocks("container-block-id")
for child in children:
    print(f"{child['type']}: {child['content'][:50]}")
```

### Block Attributes

```python
# Set custom attributes on a block
client.set_block_attrs("block-id", {
    "custom-key": "value",
    "custom-priority": "high",
    "custom-status": "done"
})

# Get all attributes of a block
attrs = client.get_block_attrs("block-id")
print(attrs.get("custom-key"))
```

### Assets

```python
# Upload asset files
result = client.upload_asset(
    file_paths=["/path/to/image.png", "/path/to/doc.pdf"],
    assets_dir_path="/assets/"
)
print(result['succMap'])  # Successfully uploaded files
print(result['errFiles'])  # Failed uploads
```

### SQL Operations

```python
# Execute SQL query
results = client.query_sql("""
    SELECT * FROM blocks 
    WHERE type = 'd' 
    ORDER BY updated DESC 
    LIMIT 10
""")

# Flush SQLite transaction to disk
client.flush_transaction()
```

### Templates

```python
# Render a template file
result = client.render_template(
    doc_id="doc-id",
    template_path="/data/templates/daily.md"
)
print(result['content'])

# Render Sprig template string
output = client.render_sprig('/daily note/{{now | date "2006/01"}}/{{now | date "2006-01-02"}}')
```

### File Operations

```python
# Read file content
content = client.get_file("/data/20210808180117-6v0mkxr/20200923234011-ieuun1p.sy")

# Create directory
client.put_file("/data/new-folder", is_dir=True)

# Upload file
with open("local-file.txt", "rb") as f:
    client.put_file("/data/new-folder/file.txt", file_content=f.read())

# List directory
files = client.read_dir("/data/20210808180117-6v0mkxr")
for f in files:
    print(f"{'[DIR]' if f['isDir'] else '[FILE]'} {f['name']}")

# Rename/move file
client.rename_file("/data/old-name.sy", "/data/new-name.sy")

# Remove file
client.remove_file("/data/unwanted-file.sy")
```

### Export

```python
# Export document as Markdown
result = client.export_md_content("doc-id")
print(result['hPath'])      # Human-readable path
print(result['content'])    # Markdown content

# Export multiple files/folders as zip
zip_path = client.export_resources(
    paths=["/conf/appearance/boot", "/conf/appearance/langs"],
    name="my-export"
)
print(f"Exported to: {zip_path}")
```

### Conversion

```python
# Run Pandoc conversion
# 1. Put input file
client.put_file("/temp/convert/pandoc/mydir/input.epub", file_content=epub_bytes)

# 2. Run conversion
work_dir = client.pandoc("mydir", ["--to", "markdown_strict", "input.epub", "-o", "output.md"])

# 3. Get output file
output = client.get_file("/temp/convert/pandoc/mydir/output.md")
```

### Notifications

```python
# Push message to SiYuan UI
msg_id = client.push_msg("Hello from API!")

# Push error message
err_id = client.push_err_msg("Something went wrong!", timeout=10000)
```

### Network

```python
# Forward HTTP request through SiYuan proxy
response = client.forward_proxy(
    url="https://api.example.com/data",
    method="GET",
    headers=[{"Authorization": "Bearer token"}]
)
print(response['body'])
print(response['status'])
```

### System

```python
# Get boot progress
progress = client.boot_progress()
print(f"Boot: {progress['progress']}% - {progress['details']}")

# Get system version
version = client.system_version()
print(f"SiYuan v{version}")

# Get current time (milliseconds)
timestamp = client.current_time()
```

### SQL Query

```python
# Execute SQL query (read-only recommended)
results = client.query_sql("""
    SELECT * FROM blocks 
    WHERE content LIKE '%关键词%'
    ORDER BY updated DESC 
    LIMIT 10
""")
for block in results:
    print(f"{block['content'][:100]}...")
```

## CLI Tools

All tools are located in `tools/` directory and depend on `siyuan_client.py`.

### List

```bash
# List all notebooks
python3 tools/list.py --notebooks

# List documents in a notebook
python3 tools/list.py --docs "notebook-id"

# Output as JSON
python3 tools/list.py -n -j
```

### Read

```bash
# Read document content
python3 tools/read.py 20240602141622-l7ou7t7

# Save to file
python3 tools/read.py 20240602141622-l7ou7t7 -o ~/doc.md

# Show document metadata
python3 tools/read.py 20240602141622-l7ou7t7 --info
```

### Search

```bash
# Search by keyword
python3 tools/search.py "keyword"

# Limit results
python3 tools/search.py "keyword" -l 50

# Raw SQL query
python3 tools/search.py "SELECT * FROM blocks WHERE type='d' LIMIT 10" --sql
```

### Export

```bash
# Export all notebooks
python3 tools/export.py -o ~/backup/

# Export specific notebook
python3 tools/export.py -n "工作" -o ~/backup/

# Export single document
python3 tools/export.py -d 20240602141622-l7ou7t7 -o ~/doc.md
```

### Create

```bash
# Create notebook
python3 tools/create.py --notebook "New Project"

# Create document
python3 tools/create.py --doc notebook-id /readme "# Hello\n\nWorld"

# Create with nested path
python3 tools/create.py --doc notebook-id /folder/doc "## Title\nContent"
```

### Delete

```bash
# Delete notebook
python3 tools/delete.py --notebook notebook-id

# Delete document
python3 tools/delete.py --doc doc-id

# Delete block
python3 tools/delete.py --block block-id

# Skip confirmation
python3 tools/delete.py --doc doc-id --yes
```

### Move

```bash
# Move single document
python3 tools/move.py --doc doc-id --to-notebook target-nb-id

# Move multiple documents
python3 tools/move.py --docs id1 id2 id3 --to-notebook target-nb-id

# Move by path
python3 tools/move.py --from-paths /doc1.sy /doc2.sy --to-nb target-nb --to-path /folder/
```

### Update

```bash
# Update a block
python3 tools/update.py --block block-id --markdown "New content"

# Append to document
python3 tools/update.py --append doc-id --markdown "\n\nFooter"

# Prepend to document
python3 tools/update.py --prepend doc-id --markdown "# Header\n"

# Insert block
python3 tools/update.py --insert "New paragraph" --parent doc-id
```

## Safety Features

- ✅ All write operations are logged
- ✅ Automatic retry with exponential backoff
- ✅ Connection health checks
- ✅ Comprehensive error handling
- ✅ Read-only by default for queries

## Troubleshooting

### Connection Refused

1. Check if SiYuan is running
2. Verify API is enabled in Settings → About → API
3. Check the correct port in config.yaml

### Authentication Failed

1. Get fresh token from SiYuan: Settings → About → API
2. Update config.yaml with new token

### Port Changes

SiYuan may use different ports on restart. Check current port:
```bash
ss -tlnp | grep SiYuan
```

Then update config.yaml accordingly.

## API Reference

- **Local API Documentation**: See [`API.md`](./API.md) in this directory (downloaded from [official repo](https://github.com/siyuan-note/siyuan/blob/master/API.md))
- **Online API Docs**: https://www.siyuan-note.club/apis
- **Official Repository**: https://github.com/siyuan-note/siyuan

## Changelog

### v1.0.0 (2026-03-20)
- Added complete API client with automatic retry
- Added 8 CLI tools for all common operations
- Added bilingual documentation (Chinese/English)
- Added configuration file support
- Production-ready with comprehensive error handling

### v0.5.0 (2026-03-18)
- Initial release
