# mdfind Query Reference

## Overview

`mdfind` is macOS's command-line interface to Spotlight. It searches indexed metadata (file contents, attributes, and system metadata) using the same index that powers the GUI Spotlight search.

## Basic Usage

```bash
mdfind <query>
```

Searches all indexed volumes for files matching the query.

## Query Syntax

### Simple Text Search

```bash
mdfind "invoice"
mdfind "quarterly report"
```

Searches file **contents** and **metadata** for the given words.

### Attribute Filters

Use `attribute:value` syntax to restrict search to specific metadata.

#### Common Attributes

- `kind:` – File type category
  - `kind:pdf`, `kind:image`, `kind:video`, `kind:application`
  - `kind:folder`, `kind:alias`, `kind:contact`
- `kMDItemFSName` – File system name (supports glob patterns with `==` operator)
- `kMDItemDisplayName` – Display name (includes extension)
- `kMDItemContentType` – Uniform Type Identifier (UTI)
  - `com.apple.application-bundle` (applications)
  - `public.plain-text` (text files)
  - `public.html` (HTML files)
  - `public.jpeg` (JPEG images)
- `kMDItemAuthors` – Author names
- `kMDItemAlbum` – Music album
- `kMDItemPixelHeight`, `kMDItemPixelWidth` – Image dimensions
- `kMDItemDurationSeconds` – Audio/video duration
- `kMDItemEmailAddresses` – Email addresses
- `kMDItemPhoneNumbers` – Phone numbers

#### Comparison Operators

- `==` – Equal (case‑insensitive, diacritic‑insensitive by default)
- `=` – Equal (same as `==`)
- `!=` – Not equal
- `<`, `<=`, `>`, `>=` – Numeric or date comparisons

Use `cd` after an operator for case‑ and diacritic‑insensitive matching (default).  
Use `c` for case‑sensitive, `d` for diacritic‑sensitive.

Examples:

```bash
mdfind 'kMDItemFSName == "*.pdf"cd'
mdfind 'kMDItemPixelHeight >= 1000'
```

#### Boolean Operators

- `AND`, `&&` – Logical AND
- `OR`, `||` – Logical OR
- `NOT`, `!` – Logical NOT (prefix operator)

Parentheses can group sub‑expressions.

Example:

```bash
mdfind '(kind:pdf OR kind:image) AND (kMDItemFSName == "*invoice*")'
```

### Date Filters

Use `kMDItemContentCreationDate`, `kMDItemContentModificationDate`, `kMDItemLastUsedDate`.

Dates can be specified in ISO 8601 format (`YYYY-MM-DD`) or as relative times:

- `$time.today`
- `$time.yesterday`
- `$time.this_week`
- `$time.this_month`
- `$time.this_year`

Examples:

```bash
mdfind 'kind:pdf AND kMDItemContentModificationDate >= $time.today'
mdfind 'kMDItemContentCreationDate >= 2024-01-01'
```

### Searching Specific Directories

Use `-onlyin <directory>` to restrict search to a folder.

```bash
mdfind -onlyin ~/Documents "kind:pdf"
mdfind -onlyin /Applications "kMDItemContentType == com.apple.application-bundle"
```

### Limiting Results

`-limit <N>` returns at most N matches.

```bash
mdfind -limit 10 "kind:image"
```

## Practical Examples

### Find Applications

```bash
# All applications
mdfind 'kMDItemContentType == com.apple.application-bundle'

# Applications whose name contains "chrome"
mdfind 'kMDItemContentType == com.apple.application-bundle && kMDItemFSName == "*chrome*"cd'
```

### Find PDFs Modified Today

```bash
mdfind 'kind:pdf AND kMDItemContentModificationDate >= $time.today'
```

### Find Images Larger Than 2 MB

```bash
mdfind 'kind:image AND kMDItemFSSize > 2000000'
```

### Find Files with "invoice" in Name or Content

```bash
mdfind 'invoice'
```

### Find Contacts

```bash
mdfind 'kind:contact'
```

### Find Recent Documents (Opened in Last 7 Days)

```bash
mdfind 'kMDItemLastUsedDate >= $time.today(-7)'
```

### Find Files with Specific Extension

```bash
mdfind 'kMDItemFSName == "*.md"cd'
```

## Checking Metadata for a File

Use `mdls` to see all Spotlight metadata for a given file:

```bash
mdls /path/to/file
```

Use `grep` to filter:

```bash
mdls -name kMDItemKind /path/to/file
```

## Notes

- Spotlight indexing may exclude certain directories (e.g., `~/Library`, system folders). Use `mdutil -s /` to check indexing status.
- Newly created files may not appear until the index updates (usually within minutes).
- To rebuild the index for a volume: `sudo mdutil -E /`.
- `mdfind` only searches indexed volumes. Use `-a` to search all volumes (including non‑indexed) but performance will be slower.

## Further Reading

- `man mdfind`
- `man mdls`
- Apple's Uniform Type Identifier reference: https://developer.apple.com/documentation/uniformtypeidentifiers
