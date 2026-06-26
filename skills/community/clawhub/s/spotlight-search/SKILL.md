---
name: spotlight-search
description: Search files, apps, and metadata on macOS using Spotlight CLI tools (`mdfind`, `mdls`, `mdutil`) with a fallback script for cases where indexing is incomplete. Use when the task is to find documents, PDFs, apps, file paths, or metadata on a Mac, especially for prompts like "spotlight search", "find this file on mac", "search my computer", "find PDFs", "locate an app", or "check file metadata".
metadata:
  {
    "openclaw":
      {
        "emoji": "🔦",
        "os": ["darwin"],
        "requires": { "bins": ["mdfind", "mdls", "mdutil", "find"] },
      },
  }
---

# Spotlight Search

## Overview

Use `mdfind` first for indexed search, `mdls` for metadata inspection, and `mdutil` only when diagnosing indexing issues. If Spotlight misses a known file, use the bundled fallback script instead of hand-rolling a `find` command every time.

## Quick Start

Preferred flow:
1. Use `mdfind` for normal search.
2. Use `mdls` when the task is about metadata, not discovery.
3. Use `./scripts/spotlight_search.sh` when Spotlight indexing is incomplete or results are unexpectedly empty.
4. Treat the fallback script as a filename/path matcher, not a general shell helper.
5. Use `mdutil` only to inspect indexing, and only suggest re-indexing when the user explicitly wants that system-level change.


```bash
# Find files containing "invoice" in name or content
mdfind "invoice"

# Find PDFs modified today
mdfind 'kind:pdf AND kMDItemContentModificationDate >= $time.today'

# Find applications whose name contains "chrome"
mdfind 'kMDItemContentType == com.apple.application-bundle && kMDItemFSName == "*chrome*"cd'

# Search only within ~/Documents
mdfind -onlyin ~/Documents "kind:pdf"

# View metadata for a file
mdls /path/to/file
```

For a hybrid search that tries Spotlight first and falls back to `find`, use the bundled script:

```bash
./scripts/spotlight_search.sh "query"
./scripts/spotlight_search.sh -t pdf "report"
./scripts/spotlight_search.sh -d ~/Documents "meeting"
```

## Core Capabilities

### 1. File Search

Spotlight indexes file contents and metadata, making it ideal for locating documents when you remember words inside them.

**Common patterns:**

- **Simple keyword**: `mdfind "quarterly report"`
- **By file type**: `mdfind "kind:pdf invoice"`
- **By extension**: `mdfind 'kMDItemFSName == "*.md"cd'`
- **By date**: `mdfind 'kMDItemContentModificationDate >= $time.yesterday'`
- **By size**: `mdfind 'kMDItemFSSize > 1000000'` (files >1 MB)

**When to use:** You recall words from the file's content, need to filter by type/date, or want to search across all indexed volumes quickly.

### 2. Application Search

Spotlight knows about installed applications (`.app` bundles) and can find them by name or bundle identifier.

**Examples:**

```bash
# All applications
mdfind 'kMDItemContentType == com.apple.application-bundle'

# Applications containing "visual" in name
mdfind 'kMDItemContentType == com.apple.application-bundle && kMDItemFSName == "*visual*"cd'
```

**When to use:** You need to locate an installed app, verify its presence, or get its bundle path.

### 3. Metadata Inspection

Use `mdls` to view the rich metadata Spotlight stores for any file.

```bash
# All metadata
mdls /path/to/file

# Specific attribute
mdls -name kMDItemKind /path/to/file
```

**Common attributes:** `kMDItemKind`, `kMDItemContentType`, `kMDItemAuthors`, `kMDItemContentCreationDate`, `kMDItemPixelHeight`, `kMDItemDurationSeconds`.

**When to use:** You need to check file properties (creation date, dimensions, author) without opening the file.

### 4. Hybrid Search (Fallback)

Spotlight indexing may be incomplete (excluded directories, recent files not yet indexed). The bundled script `scripts/spotlight_search.sh` provides a hybrid approach:

1. Attempts Spotlight search via `mdfind`
2. If no results, falls back to `find` with name‑based matching
3. Uses shell argument arrays instead of `eval`, so the query is passed as data rather than executable shell text
4. Supports filtering by kind (`pdf`, `image`, `application`, etc.)

**Usage:**

```bash
./scripts/spotlight_search.sh "query"
./scripts/spotlight_search.sh -t pdf "report"
./scripts/spotlight_search.sh -d ~/Documents -l 10 "draft"
```

**When to use:** You want maximum recall, or Spotlight is returning empty results for known files.

## Reference Materials

For detailed query syntax, operator reference, and advanced examples, see:

- **[mdfind Query Reference](references/mdfind-queries.md)** – Comprehensive guide to `mdfind` syntax, attribute filters, date comparisons, and practical examples.

Load this reference when you need to construct complex queries or understand Spotlight's capabilities.

## Workflow Guidance

### Choosing the Right Tool

| Scenario | Recommended Tool | Example |
|----------|-----------------|---------|
| "Find files containing 'budget'" | `mdfind "budget"` | Content‑aware search |
| "Find all PDFs modified this week" | `mdfind 'kind:pdf AND kMDItemContentModificationDate >= $time.this_week'` | Metadata‑filtered search |
| "Find the Chrome app" | `mdfind 'kMDItemContentType == com.apple.application-bundle && kMDItemFSName == "*chrome*"cd'` | Application search |
| "Search only in Downloads folder" | `mdfind -onlyin ~/Downloads "kind:image"` | Scoped search |
| "Check when a file was created" | `mdls -name kMDItemContentCreationDate /path/to/file` | Metadata inspection |
| "Spotlight returns nothing but I know the file exists" | `./scripts/spotlight_search.sh "filename"` | Hybrid fallback |

### Troubleshooting

**No results for known files?**

1. Check indexing status: `mdutil -s /`
2. Ensure the directory is indexed (Spotlight excludes some system and Library folders)
3. Re-index only with explicit user approval because it is a privileged, system-wide action: `sudo mdutil -E /`

**Query syntax errors?**

- Enclose queries containing spaces or special characters in single quotes.
- Use `cd` after `==` for case‑ and diacritic‑insensitive matching: `kMDItemFSName == "*.pdf"cd`
- Combine filters with `AND`/`OR` and parentheses.

**Slow performance?**

- Limit results with `-limit N`
- Restrict search scope with `-onlyin`

## Notes

- Spotlight indexing is not real‑time; newly created files may take minutes to appear.
- Some directories (e.g., `~/Library`, system folders) may be excluded from indexing.
- `mdfind` searches all indexed volumes by default; use `-onlyin` to constrain.
- The hybrid script requires `find` (always present) and optionally `fd` (faster).

## See Also

- `man mdfind`
- `man mdls`
- `man mdutil`
- Apple's Uniform Type Identifier reference: https://developer.apple.com/documentation/uniformtypeidentifiers
