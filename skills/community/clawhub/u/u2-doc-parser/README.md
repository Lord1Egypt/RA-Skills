# UniDoc Document Parser Skill

A ClawHub skill for parsing documents using the UniDoc API service. Converts various document formats (PDF, DOC, DOCX, images) to Markdown or JSON with support for both synchronous and asynchronous processing modes.

## Features

- **Multiple Format Support**: Parse PDF, DOC, DOCX, PNG, JPG, and more
- **Output Formats**: Convert to Markdown (`.md`) or JSON (`.json`)
- **Flexible Output**: Print to terminal (default) or save to file
- **Dual Processing Modes**:
  - Synchronous mode for immediate results
  - Asynchronous mode for large files with status polling
- **Cloud-Based**: Leverages UniDoc API for robust parsing
- **Pipeline-Friendly**: Output to stdout for easy integration with other tools

## Installation

### Prerequisites

- Python 3.7+
- `requests` library
- Network connectivity to UniDoc API

### Install Dependencies

```bash
pip install requests
```

## Quick Start

### Basic Usage (Output to Terminal)

```bash
# Parse document and print to terminal
python scripts/unidoc_parse.py path/to/document.pdf

# Specify output format
python scripts/unidoc_parse.py path/to/document.pdf --format md
```

### Save to File

```bash
# Save output to a specific file
python scripts/unidoc_parse.py path/to/document.pdf --output result.md

# Save JSON output
python scripts/unidoc_parse.py path/to/document.docx --format json --output result.json
```

### Asynchronous Mode

```bash
# For large files, use async mode
python scripts/unidoc_parse.py path/to/document.docx --mode async

# Output can still be piped
python scripts/unidoc_parse.py path/to/document.pdf | grep "keyword"
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | `md` | Output format: `md` or `json` |
| `--mode` | `sync` | Processing mode: `sync` or `async` |
| `--func` | `unisound` | Conversion method/algorithm |
| `--output` | `stdout` | Output file path (if not specified, prints to terminal) |
| `--uid` | Auto-generated | Custom user ID |

## Output

- **Default**: Converted content is printed directly to the terminal (stdout)
- **With `--output`**: Content is saved to the specified file path
- **Progress messages**: Sent to stderr to avoid interfering with output
- **Piping**: Can be piped to other commands for further processing

Example:
```bash
# Pipe output to grep
python scripts/unidoc_parse.py document.pdf | grep "important keyword"

# Save to file while also viewing
python scripts/unidoc_parse.py document.pdf | tee result.md
```

## API Endpoints

- **Base URL**: `https://unidoc.uat.hivoice.cn`
- **Sync Upload**: `/syncUploadFile`
- **Async Upload**: `/asyncUploadFile`
- **Export**: `/exportFile`
- **Status**: `/getFileStatus`

## Examples

### Convert PDF to Markdown

```bash
# Output to terminal
python scripts/unidoc_parse.py report.pdf --format md

# Save to file
python scripts/unidoc_parse.py report.pdf --format md --output report.md
```

### Convert DOCX to JSON (Async)

```bash
# Large files work better in async mode
python scripts/unidoc_parse.py document.docx --format json --mode async --output data.json
```

### Parse Image to Markdown

```bash
python scripts/unidoc_parse.py screenshot.png --format md
```

### Pipeline Usage

```bash
# Search for specific content
python scripts/unidoc_parse.py document.pdf | grep "keyword"

# Count lines
python scripts/unidoc_parse.py document.pdf | wc -l

# Convert and post-process
python scripts/unidoc_parse.py document.pdf | sed 's/foo/bar/g' > processed.md
```

## Limitations

- Requires active internet connection
- Dependent on UniDoc API availability
- File size limits determined by API service
- Rate limiting may apply based on API configuration

## ⚠️ Privacy & Security Notice

**This skill uploads your documents to an external API service.**

- **External Service**: Documents are uploaded to `https://unidoc.uat.hivoice.cn`
- **No Authentication**: Current implementation does not require API keys or credentials (UAT environment)
- **Data Transmission**: Your files are transmitted over the internet and processed on third-party servers
- **Recommendation**:
  - ❌ **Do NOT use** with sensitive, confidential, or private documents
  - ✅ **Use ONLY** with non-sensitive test documents
  - ⚠️ Be aware of data privacy implications before using

By using this tool, you acknowledge that your files will be uploaded to external servers for processing.

## License

MIT-0

## Author

云知声智能科技股份有限公司 (Unisound Intelligence Technology Co., Ltd.)

## See Also

- [UniDoc API Documentation](http://unidoc.uat.hivoice.cn)