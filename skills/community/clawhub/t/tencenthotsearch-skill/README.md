# TencentHotSearch Skill

> ⚠️ **Security Notice**: This skill requires Tencent Cloud API credentials. Please read [Security Considerations](#security-considerations) and [SECURITY.md](SECURITY.md) before installation.

A trending news and article search tool based on Tencent Cloud Online Search API (SearchPro). Supports web-wide search or site-specific search to retrieve popular articles and news related to keywords.

**API Information:**
- **Endpoint Domain**: wsa.tencentcloudapi.com
- **API Version**: 2025-05-08
- **API Name**: SearchPro

## Source & Repository

- **GitHub**: https://github.com/neuhanli/skills
- **Package**: TencentHotSearch-skill
- **Documentation**: [SECURITY.md](SECURITY.md), [CONFIG.md](CONFIG.md)

### Verification

To verify the integrity of this skill:

```bash
# Clone the official repository
git clone https://github.com/neuhanli/skills.git
cd skills/TencentHotSearch-skill

# Review the code
cat scripts/tencent_hotsearch.py
cat requirements.txt

# Check configuration
cat config.example.json
```

## Features

- **Multi-keyword Search**: Supports 1-5 keywords for combined search
- **Site-specific Search**: Choose between web-wide search or specific sites (e.g., qq.com, news.qq.com)
- **Multiple Search Modes**:
  - Natural search results (Mode=0, default)
  - Multimodal VR results (Mode=1)
  - Mixed results (Mode=2)
- **Time Filtering**: Filter results by start time and end time
- **Industry Filtering**: Filter by industry (gov/news/acad/finance, Premium version)
- **Structured Results**: Returns complete information including title, summary, dynamic summary, source platform, publish time, original link, relevance score, image list, etc.
- **Multi-format Output**: Supports JSON, CSV, TXT, MD format output (default: MD)
- **Custom Output Path**: Supports setting default output directory in configuration file

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/neuhanli/skills.git
cd skills/TencentHotSearch-skill
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Copy the configuration template and fill in your API credentials:

```bash
cp config.example.json config.json
```

Edit `config.json` and fill in your Tencent Cloud API credentials:

```json
{
  "secret_id": "YOUR_TENCENT_CLOUD_SECRET_ID",
  "secret_key": "YOUR_TENCENT_CLOUD_SECRET_KEY",
  "output_dir": "./output"
}
```

For detailed configuration steps, refer to [CONFIG.md](CONFIG.md)

### 4. Run Search

#### Command Line Usage

```bash
# Web-wide search (default mode, MD format output)
python scripts/tencent_hotsearch.py "AI" "machine learning" -l 10

# Site-specific search (Tencent.com)
python scripts/tencent_hotsearch.py "AI" "machine learning" -s qq.com -l 10

# Site-specific search (News channel)
python scripts/tencent_hotsearch.py "technology" "innovation" -s news.qq.com -l 15

# Multimodal VR mode search
python scripts/tencent_hotsearch.py "AI" -m 1 -l 10

# Mixed mode search
python scripts/tencent_hotsearch.py "AI" -m 2 -l 20

# Search by time range
python scripts/tencent_hotsearch.py "AI" --from-time 1704067200 --to-time 1706745600

# Filter by industry (Premium)
python scripts/tencent_hotsearch.py "AI" --industry news -l 20

# Save results to specified file
python scripts/tencent_hotsearch.py "AI" "machine learning" -o results.md

# Save results to JSON file
python scripts/tencent_hotsearch.py "AI" "machine learning" -o results.json -f json

# Save results to CSV file
python scripts/tencent_hotsearch.py "AI" "machine learning" -o results.csv -f csv

# Save results to TXT file
python scripts/tencent_hotsearch.py "AI" "machine learning" -o results.txt -f txt

# Print results to console
python scripts/tencent_hotsearch.py "AI" "machine learning" --print

# Custom storage path (relative path)
python scripts/tencent_hotsearch.py "AI" -o output/ai_results.txt -f txt

# Custom storage path (absolute path)
python scripts/tencent_hotsearch.py "technology" -o /path/to/your/output/tech_news.md -f md
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `keywords` | Search keywords (1-5) | - |
| `-s, --site` | Specify search site (e.g., qq.com) | Web-wide search |
| `-m, --mode` | Search mode (0/1/2) | 0 |
| `-l, --limit` | Number of results (10/20/30/40/50) | 10 |
| `--from-time` | Start time (Unix timestamp) | - |
| `--to-time` | End time (Unix timestamp) | - |
| `--industry` | Industry filter (gov/news/acad/finance) | - |
| `-c, --config` | Configuration file path | config.json |
| `-o, --output` | Output file path | - |
| `-f, --format` | Output format (json/csv/txt/md) | md |
| `--print` | Print results to console | False |

## Usage Examples

### Example 1: Web-wide search for AI-related news

```bash
python scripts/tencent_hotsearch.py "AI" "machine learning" -l 15 -o ai_news.md
```

### Example 2: Search technology news on Tencent.com

```bash
python scripts/tencent_hotsearch.py "technology" "innovation" -s qq.com -l 20 -f json
```

### Example 3: Search financial news on news channel

```bash
python scripts/tencent_hotsearch.py "finance" "stock market" -s news.qq.com --print
```

### Example 4: Multi-keyword search

```bash
python scripts/tencent_hotsearch.py "blockchain" "Web3" "cryptocurrency" -l 10 -f csv
```

### Example 5: Search by time range

```bash
python scripts/tencent_hotsearch.py "AI" --from-time 1704067200 --to-time 1706745600 -l 30
```

### Example 6: Mixed mode search

```bash
python scripts/tencent_hotsearch.py "AI" -m 2 -l 20 -o results.md
```

## Output Formats

### Markdown Format (Default)

Suitable for viewing in Markdown editors, includes formatted titles, links, and metadata.

```markdown
# Search Results

**Total results:** 10
**Timestamp:** 2024-01-15T10:30:00

---

## 1. Article Title

**Summary:** Content summary...

**Dynamic Summary:** Dynamic summary content...

**Source:** Source Platform

**Time:** 2024-01-15 10:30:00

**Link:** [https://example.com/article](https://example.com/article)

**Relevance:** 0.8978

---
```

### JSON Format

Structured data, suitable for program processing and data analysis.

```json
{
  "results": [
    {
      "title": "Article Title",
      "summary": "Standard summary...",
      "dynamic_summary": "Dynamic summary (Premium version)...",
      "source": "Source Platform",
      "publishTime": "2024-01-15 10:30:00",
      "url": "https://example.com/article",
      "score": 0.8978,
      "images": ["https://example.com/image1.jpg"],
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "total": 10,
  "timestamp": "2024-01-15T10:30:00"
}
```

### CSV Format

Table format, suitable for opening in Excel and other tools for data analysis.

### TXT Format

Plain text format, suitable for quick reading and copy-paste.

## Search Modes

### Mode 0: Natural Search Results (Default)

- Returns traditional web search results
- Supports filtering parameters such as Site, FromTime, ToTime, Industry
- Suitable for regular search needs

### Mode 1: Multimodal VR Results

- Returns multimodal VR search results
- **Note**: Site, FromTime, ToTime, Industry parameters are invalid in this mode
- Suitable for scenarios requiring rich media content

### Mode 2: Mixed Results

- Returns a mix of multimodal VR results and natural search results
- Site, FromTime, ToTime, Industry parameters only apply to natural results
- Suitable for scenarios requiring comprehensive search results

## Industry Filters (Premium Version)

| Value | Description |
|-------|-------------|
| gov | Government and party organs |
| news | Authoritative media |
| acad | Academic (English) |
| finance | Finance |

## API Response Fields

| Field | Type | Description |
|-------|------|-------------|
| title | string | Result title |
| summary | string | Standard summary |
| dynamic_summary | string | Dynamic summary (Premium version) |
| source | string | Website name |
| publishTime | string | Content publish time |
| url | string | Content source URL |
| score | float | Relevance score (0~1) |
| images | array | Image list |
| favicon | string | Website icon link |

## Configuration File

### config.json Structure

```json
{
  "secret_id": "YOUR_TENCENT_CLOUD_SECRET_ID",
  "secret_key": "YOUR_TENCENT_CLOUD_SECRET_KEY",
  "output_dir": "./output"
}
```

### Configuration Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| secret_id | string | Yes | Tencent Cloud API Key ID |
| secret_key | string | Yes | Tencent Cloud API Key |
| output_dir | string | No | Default output directory, defaults to ./output |

## Dependencies

- Python 3.7+
- No external dependencies (core functionality uses only Python standard library)
- Optional: pandas>=2.0.0 (only when CSV export functionality is needed)

## Security Considerations

> For comprehensive security guidelines, see [SECURITY.md](SECURITY.md)

### Before Installation

⚠️ **Important**: This skill requires Tencent Cloud API credentials. Please ensure you:

1. **Review the source code** in `scripts/tencent_hotsearch.py`
2. **Use temporary/least-privileged API keys** for testing
3. **Run in isolated environment** (container/VM)
4. **Never commit config.json** to version control
5. **Read [SECURITY.md](SECURITY.md)** for complete security checklist

### 1. API Credentials Protection

- ⚠️ **DO NOT** commit `config.json` to version control (Git)
- ⚠️ Use `.gitignore` to ignore `config.json` (already configured)
- ⚠️ Rotate API keys regularly
- ⚠️ Use different keys for different environments
- ⚠️ Follow least privilege principle when configuring API keys

### 2. Output Directory Safety

- ⚠️ Do not set output directory to sensitive system paths
- ⚠️ Recommended to use dedicated temporary directory or sandbox environment
- ⚠️ Program will automatically create output directory but prevents directory traversal attacks

### 3. Runtime Environment

- ⚠️ Recommended to run in isolated environment (container or sandbox)
- ⚠️ Use temporary API keys with minimal permissions for testing
- ⚠️ Rotate/delete keys after testing

### 4. Network Security

- ✅ All API requests are encrypted via HTTPS
- ✅ Only accesses official Tencent Cloud API endpoint (wsa.tencentcloudapi.com)
- ✅ Request timeout set to 30 seconds to avoid long blocking

## Notes

- Keyword limit: 1-5 keywords
- Result limit: 10/20/30/40/50 (Premium version supports up to 50)
- Timestamp format: Unix timestamp (seconds)
- Industry filtering only supported in Premium version
- Dynamic summary only supported in Premium version
- In Mode 1, Site, FromTime, ToTime, Industry parameters are invalid
- Output path must be within the configured output_dir directory to prevent directory traversal attacks

## Error Handling

- **Configuration file not found**: Prompt to create config.json file, refer to CONFIG.md
- **API authentication failed**: Check if SecretId and SecretKey are correct (error messages do not expose credentials)
- **Network error**: Check network connection and API service status
- **Parameter error**: Check keyword count, timestamp format, etc.
- **Path security error**: Output paths containing directory traversal attempts (..) will be rejected

## License

MIT License

## Installation Verification Checklist

> ⚠️ **Important**: Due to registry metadata inconsistencies, please complete this verification before providing API credentials.

Before installing and providing credentials:

- [ ] **Review Source Code**: Examine `scripts/tencent_hotsearch.py` for API calls and signing logic
- [ ] **Verify Repository**: Confirm the official GitHub repository: https://github.com/neuhanli/skills
- [ ] **Use Temporary Keys**: Create dedicated, least-privileged Tencent API keys
- [ ] **Isolated Environment**: Run in container/VM with non-sensitive output directory
- [ ] **File Protection**: Ensure `config.json` is never committed and set `chmod 600`
- [ ] **Monitor Network**: Watch for unexpected network connections

### Code Integrity Verification

```bash
# Clone and inspect the code
git clone https://github.com/neuhanli/skills.git
cd skills/TencentHotSearch-skill

# Review the main script
cat scripts/tencent_hotsearch.py

# Check for expected functionality
grep -n "wsa.tencentcloudapi.com" scripts/tencent_hotsearch.py
grep -n "HMAC" scripts/tencent_hotsearch.py
grep -n "config.json" scripts/tencent_hotsearch.py

# Verify no unexpected dependencies
grep -n "import" scripts/tencent_hotsearch.py | grep -v "from datetime\|from pathlib\|from typing\|import json\|import os\|import sys\|import hashlib\|import hmac\|import time\|import urllib"
```

### Expected Code Patterns

When reviewing the code, look for these legitimate patterns:

- ✅ **Tencent API Endpoint**: `wsa.tencentcloudapi.com`
- ✅ **HMAC-SHA256 Signing**: Manual implementation using `hashlib` and `hmac`
- ✅ **Configuration File**: Reads `config.json` for credentials
- ✅ **Standard Library Only**: Uses `urllib` instead of external HTTP libraries
- ✅ **Path Validation**: Prevents directory traversal attacks
- ✅ **Secret Masking**: API keys are masked in error messages

### Registry Metadata Notice

The registry metadata incorrectly states "no credentials/config required" while the actual code requires Tencent API credentials. This inconsistency has been addressed in SKILL.md but users should be aware of this discrepancy.

## Author

Created for Agent Skills platform
