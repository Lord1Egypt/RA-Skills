---
name: "TencentHotSearch-skill"
description: "Fetches trending news and articles using Tencent Cloud Online Search API (SearchPro). Supports searching across the entire web or within specific sites, with multiple output formats (JSON, CSV, TXT, MD). Invoke when user wants to get hot news, trending topics, or search for articles on specific keywords using Tencent Cloud services."
required_credentials:
  - name: "secret_id"
    description: "Tencent Cloud API Secret ID (starts with AKID)"
    required: true
    warning: "Sensitive credential - use temporary/least-privileged keys only"
  - name: "secret_key"
    description: "Tencent Cloud API Secret Key"
    required: true
    warning: "Sensitive credential - rotate regularly and never commit to version control"
permissions:
  - name: "network_access"
    description: "Access to Tencent Cloud API endpoint (wsa.tencentcloudapi.com)"
    required: true
  - name: "file_write"
    description: "Write search results to specified output directory"
    required: true
source:
  homepage: "https://github.com/neuhanli/skills"
  repository: "https://github.com/neuhanli/skills/tree/main/TencentHotSearch-skill"
---

> ⚠️ **BEFORE INSTALLING - Security Notice**
> 
> This skill requires Tencent Cloud API credentials (SecretId/SecretKey). 
> Please read [Security Considerations](#security-considerations) before providing credentials.
> 
> **Verify Source**: Check the [GitHub repository](https://github.com/neuhanli/skills) for code audit.  
> **Use Temporary Keys**: Only use temporary/least-privileged API keys for testing.  
> **Run in Isolation**: Execute in container/VM with non-sensitive output directory.

# TencentHotSearch Skill

## Overview

TencentHotSearch-skill is a trending news and article search tool based on Tencent Cloud Online Search API (SearchPro). It supports web-wide search or site-specific search to retrieve popular articles and news related to keywords.

**API Information:**
- **Endpoint Domain**: wsa.tencentcloudapi.com
- **API Version**: 2025-05-08
- **API Name**: SearchPro

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
- **Compliance & Security**: All data is obtained through Tencent's official API compliantly

## Security Considerations

Before installing and using this skill, please carefully read the following security guidelines:

### ⚠️ Important Notice

**Registry Metadata Inconsistency**: The registry metadata claims 'no credentials/config required', but both SKILL.md and the code require a `config.json` file containing your Tencent SecretId and SecretKey. This is a documentation mismatch that users should be aware of.

### Pre-Installation Checklist

1. **Verify Source and Provenance**
   - Review the skill source code yourself
   - Check the publisher's credibility
   - Note: Source/homepage links may be missing - verify from trusted sources

2. **Inspect the Code**
   - Review `scripts/tencent_hotsearch.py` to understand the signing and HTTPS calls
   - The code performs legitimate Tencent Cloud API calls
   - No hidden exfiltration mechanisms detected, but always review yourself

3. **Use Minimal/Temporary Credentials**
   - Use temporary or least-privileged API keys
   - Create dedicated API keys for this skill
   - Safely rotate/delete keys after testing
   - Follow the principle of least privilege

4. **Run in Isolated Environment**
   - Use container/VM for execution
   - Do not point `output_dir` to sensitive system paths
   - Use dedicated temporary directory or sandbox environment

5. **Protect Configuration Files**
   - Do NOT commit `config.json` to version control
   - Follow the provided `.gitignore` configuration (already set up)
   - Set file permissions: `chmod 600 config.json` (Linux/macOS)
   - Regularly rotate API keys

### For Higher Confidence

If you need higher assurance before installation:

- Ask the publisher to correct registry metadata to explicitly declare required credentials
- Request a verified homepage or repository URL
- Ask for signed releases or upstream repository URL for auditing
- Review the full source code in `scripts/tencent_hotsearch.py`

### Security Features Implemented

✅ **Path Traversal Prevention**: Validates output paths to prevent directory traversal attacks  
✅ **Secret Masking**: Masks API keys in error messages and logs  
✅ **HTTPS Only**: All API requests use encrypted HTTPS connections  
✅ **Official Endpoint**: Only accesses official Tencent Cloud API (wsa.tencentcloudapi.com)  
✅ **Git Protection**: `.gitignore` configured to exclude `config.json`  
✅ **Error Handling**: Comprehensive error handling with secure credential management  

For detailed security recommendations, see [CONFIG.md](CONFIG.md#security-recommendations)

## When to Use

Invoke this skill when users have the following needs:
- Want to get trending news or trending topics in a specific field
- Need to search for the latest articles related to specific keywords
- Want to track hot events or plan content topics
- Need to quickly grasp dynamics in a specific field
- Need to search content within specific sites (e.g., Tencent.com, news channels)
- Need to filter search results by time range or industry

## Usage

### Quick Start (Command Line)

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Configure Tencent Cloud API
Edit the `config.json` file and fill in your Tencent Cloud API credentials:
```json
{
  "secret_id": "YOUR_TENCENT_CLOUD_SECRET_ID",
  "secret_key": "YOUR_TENCENT_CLOUD_SECRET_KEY",
  "output_dir": "./output"
}
```

For detailed configuration instructions, refer to [CONFIG.md](CONFIG.md)

#### 3. Run Search
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

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| keywords | array[string] | Yes | 1-5 search keywords |
| site | string | No | Specify search site (e.g., qq.com, news.qq.com), web-wide search if not specified |
| mode | integer | No | Search mode: 0-natural search (default), 1-multimodal VR, 2-mixed results |
| limit | integer | No | Number of results to return, default 10, options: 10/20/30/40/50 |
| from_time | integer | No | Start time filter (Unix timestamp, seconds) |
| to_time | integer | No | End time filter (Unix timestamp, seconds) |
| industry | string | No | Industry filter: gov/news/acad/finance (Premium version) |

### Command Line Arguments

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

### Example

```json
{
  "keywords": ["artificial intelligence", "machine learning"],
  "site": "qq.com",
  "mode": 0,
  "limit": 10,
  "from_time": 1704067200,
  "to_time": 1706745600,
  "industry": "news"
}
```

### Response Format

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
  "query": {
    "keywords": ["artificial intelligence", "machine learning"],
    "site": "qq.com",
    "mode": 0
  }
}
```

## API Configuration

### Tencent Cloud Online Search API

#### Setup Steps

1. Visit [Tencent Cloud Console](https://console.cloud.tencent.com/)
2. Log in to your Tencent Cloud account
3. Navigate to "Products" -> "Artificial Intelligence" -> "Online Search"
4. Activate the service and obtain API credentials (SecretId and SecretKey)
5. Select appropriate region (e.g., ap-guangzhou)

#### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| secret_id | Tencent Cloud API Key ID | AKIDxxxxxxxxxxxxxxxx |
| secret_key | Tencent Cloud API Key | xxxxxxxxxxxxxxxx |
| output_dir | Default output directory | ./output |

## Output Formats

### 1. Markdown Format (Default)

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

### 2. JSON Format

Structured data, suitable for program processing and data analysis.

```json
{
  "results": [...],
  "total": 10,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 3. CSV Format

Table format, suitable for opening in Excel and other tools for data analysis.

### 4. TXT Format

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

## Dependencies

- Python 3.7+
- No external dependencies (core functionality uses only Python standard library)
- Optional: pandas>=2.0.0 (only when CSV export functionality is needed)

## Security Considerations

### API Credentials Protection

- ⚠️ **DO NOT** commit `config.json` to version control (Git)
- ⚠️ Use `.gitignore` to ignore `config.json` (already configured)
- ⚠️ Rotate API keys regularly
- ⚠️ Use different keys for different environments
- ⚠️ Follow least privilege principle when configuring API keys

### Output Directory Safety

- ⚠️ Do not set output directory to sensitive system paths
- ⚠️ Recommended to use dedicated temporary directory or sandbox environment
- ⚠️ Program will automatically create output directory but prevents directory traversal attacks

### Runtime Environment

- ⚠️ Recommended to run in isolated environment (container or sandbox)
- ⚠️ Use temporary API keys with minimal permissions for testing
- ⚠️ Rotate/delete keys after testing

### Network Security

- ✅ All API requests are encrypted via HTTPS
- ✅ Only accesses official Tencent Cloud API endpoint (wsa.tencentcloudapi.com)
- ✅ Request timeout set to 30 seconds to avoid long blocking

## Installation

```bash
# Clone repository
git clone https://github.com/neuhanli/skills.git
cd skills/TencentHotSearch-skill

# Install dependencies
pip install -r requirements.txt

# Configure API credentials
cp config.example.json config.json
# Edit config.json and fill in your API credentials
```

## Error Handling

- **Configuration file not found**: Prompt to create config.json file
- **API authentication failed**: Check if SecretId and SecretKey are correct
- **Network error**: Check network connection and API service status
- **Parameter error**: Check keyword count, timestamp format, etc.

## Notes

- Keyword limit: 1-5 keywords
- Result limit: 10/20/30/40/50 (Premium version supports up to 50)
- Timestamp format: Unix timestamp (seconds)
- Industry filtering only supported in Premium version
- Dynamic summary only supported in Premium version

## License

MIT License

## Author

Created for Agent Skills platform
