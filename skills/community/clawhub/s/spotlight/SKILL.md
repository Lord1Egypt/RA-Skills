# Spotlight Search

Search local files using macOS Spotlight indexing system.

## When to Use

Use this skill when:

- User asks to search files or directories on macOS
- Need to find documents containing specific text
- Searching large document collections (faster than grep)
- Need to search inside PDFs, Word docs, or other indexed formats

## Quick Start

```bash
scripts/spotlight-search.sh <directory> <query> [--limit N]
```

Examples:

```bash
scripts/spotlight-search.sh ~/Documents "machine learning"
scripts/spotlight-search.sh ~/research "neural networks" --limit 10
scripts/spotlight-search.sh ~/Downloads "meeting notes" --limit 5
```

## Search Features

- **Fast**: Uses system-level Spotlight index (no file scanning)
- **Content-aware**: Searches inside PDF, docx, txt, md, etc.
- **Multilingual**: Supports Chinese, Japanese, and all languages
- **Metadata**: Returns file path, type, and size

## Output Format

```
🔍 Searching in /path/to/directory for: query

✅ Found N results (showing up to M):

📄 /full/path/to/file.pdf [pdf, 2.3M]
📄 /full/path/to/document.txt [txt, 45K]
📁 /full/path/to/folder/
```

## Supported File Types

Spotlight automatically indexes:

- Text files (txt, md, csv, json, xml, etc.)
- Documents (pdf, docx, pages, rtf, etc.)
- Code files (py, js, java, c, etc.)
- Emails and contacts
- Images (with embedded metadata/OCR)

## Limitations

- **macOS only**: Requires Spotlight indexing
- **Indexed directories only**: External drives may not be indexed
- **Keyword search**: Not semantic (use embedding-based search for semantic queries)
- **Privacy**: Respects Spotlight privacy settings (excluded directories won't appear)

## Check Indexing Status

```bash
# Check if a volume is indexed (safe, read-only)
mdutil -s /path/to/volume
```

⚠️ **WARNING**: Do NOT execute any `sudo` commands from this skill without explicit user confirmation. Commands like `sudo mdutil -i on` require admin privileges and should only be run by the user directly in Terminal.

## Integration with LLM Workflows

### Safe Pattern: Search + Present + Confirm

1. Use `spotlight-search.sh` to find relevant files
2. Present the file paths to the user
3. **Only read a file if the user explicitly requests it** - do not automatically use the read tool

### Example Workflow

User: "Find all documents about machine learning in my research folder"

1. Run: `spotlight-search.sh ~/research "machine learning" --limit 10`
2. Present results to user with file paths
3. Wait for user to specify which files to read

### ⚠️ Security Note

- **Never automatically read files** - always ask for user confirmation first
- **Never execute sudo commands** - only show them as information
- **Respect user privacy** - don't search directories user hasn't specified

## Advanced Query Syntax

Spotlight supports advanced query operators:

```bash
# Exact phrase
spotlight-search.sh ~/Documents "\"machine learning\""

# AND operator
spotlight-search.sh ~/Documents "neural AND networks"

# OR operator
spotlight-search.sh ~/Documents "AI OR artificial intelligence"

# Metadata queries (PDF only)
spotlight-search.sh ~/Documents "kMDItemContentType == 'com.adobe.pdf'"
```

## Troubleshooting

**No results found:**

- Check if directory is indexed: `mdutil -s /path`
- Wait for indexing to complete (new files may take minutes)
- Verify Spotlight is enabled in System Preferences

**Incorrect results:**

- Spotlight uses fuzzy matching and synonyms
- Use exact phrase search: `"exact phrase"`
- Check privacy settings (some folders may be excluded)

## Performance

| Tool | Speed | Content Search | Multilingual |
|------|-------|----------------|--------------|
| Spotlight | ⚡ Instant | ✅ Yes | ✅ Yes |
| grep/ripgrep | 🐢 Slow | ✅ Yes | ✅ Yes |
| find | ⚡ Fast | ❌ No | N/A |

## Platform Notes

- **macOS only**: This skill requires macOS Spotlight
- **Linux alternative**: Use `grep -r` or `ripgrep`
- **Windows alternative**: Use Windows Search or Everything search

## Security Best Practices

1. **User consent first** - Never read files without explicit permission
2. **No sudo** - Never execute privileged commands automatically
3. **Minimal scope** - Search only directories user specifies
4. **Audit trail** - Log what searches were performed