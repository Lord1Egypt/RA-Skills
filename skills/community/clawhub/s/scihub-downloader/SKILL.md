---
name: scihub-downloader
description: Download academic papers from multiple sources (Unpaywall, PMC, Semantic Scholar, arXiv, Sci-Hub). Direct PDF link extraction from Sci-Hub without browser automation.
homepage: https://github.com/openclaw/skills/scihub-downloader
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["curl"] },
        "category": "research",
        "tags": ["paper", "download", "open-access", "unpaywall", "pmc", "scihub", "doi"],
        "version": "3.1.0"
      },
  }

Download academic papers from multiple sources with direct PDF link extraction.

## ⚡ Quick Start

```bash
# Download by DOI
scihub-dl "10.1038/nature12373"

# Download by title
scihub-dl "slope stability analysis machine learning"

# Open Access only
scihub-dl "10.1038/nature12373" --oa-only
```

## 📋 When to Use

| Trigger | Action |
|---------|--------|
| "Download paper DOI..." | Download by DOI |
| "Get paper PMID..." | Download by PubMed ID |
| "Find paper [title]" | Search and download |
| "Fetch article..." | Download paper |

## 🔄 Download Strategy

| Priority | Source | Type | Success Rate |
|----------|--------|------|--------------|
| 1 | **Unpaywall** | Legal OA | ~40% |
| 2 | **PubMed Central** | Legal OA | ~15% |
| 3 | **Semantic Scholar** | Legal OA | ~10% |
| 4 | **arXiv** | Legal OA | Preprints |
| 5 | **Sci-Hub** | Shadow | ~90%+ |

## 🛠️ Commands

### Basic Usage

```bash
# DOI
scihub-dl "10.1038/nature12373"

# PMID
scihub-dl "PMID:36871234"

# arXiv
scihub-dl "arXiv:2301.00001"

# Title search
scihub-dl "deep learning for image recognition"
```

### Output Options

```bash
# Custom directory
scihub-dl "10.1038/nature12373" -o ~/papers/

# Custom filename
scihub-dl "10.1038/nature12373" -f my-paper.pdf

# JSON output
scihub-dl "10.1038/nature12373" --json
```

### Check & Verbose

```bash
# Check availability
scihub-dl "10.1038/nature12373" --check

# Verbose mode
scihub-dl "10.1038/nature12373" -v

# Open Access only
scihub-dl "10.1038/nature12373" --oa-only
```

## 🌐 Sci-Hub Mirrors (2026)

| Mirror | Status | Notes |
|--------|--------|-------|
| `sci-hub.st` | ⚠️ Protected | DDoS-Guard |
| `sci-hub.ru` | ✅ Working | Redirects to sci-net.xyz |
| `sci-hub.se` | ❌ Blocked | Connection closed |
| `sci-hub.wf` | ⚠️ Protected | DDoS-Guard |

**推荐**: 使用 `sci-hub.ru` 或直接访问 `sci-net.xyz`

## 📊 Example Output

```bash
$ scihub-dl "10.1038/s43017-022-00373-x" -v

[Paper-DL] Detected type: doi
[Paper-DL] DOI: 10.1038/s43017-022-00373-x
ℹ Title: Landslide detection, monitoring and prediction...
ℹ Author: Casagli et al.
ℹ Year: 2023
→ Checking Unpaywall...
→ Trying Sci-Hub mirrors...
✓ Found via Sci-Hub (sci-hub.ru)
→ Downloading from Sci-Hub (sci-hub.ru)...
✓ Downloaded: ~/papers/Casagli_2023.pdf (3.0M)

✨ Download complete!
  📄 File: ~/papers/Casagli_2023.pdf
  📊 Size: 3.0M
  🌐 Source: Sci-Hub (sci-hub.ru)
```

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "Could not find PDF" | Paper may not be in any source |
| "DDoS-Guard protection" | Try `-m sci-hub.ru` |
| "Connection closed" | Mirror blocked, try another |
| Invalid PDF | Retry or use alternative source |

## 📝 Files

```
scihub-downloader/
├── SKILL.md              # This file
├── README.md             # Documentation
├── scripts/
│   └── scihub-dl.sh      # Main script v3.1
└── references/
    ├── mirrors.md        # Sci-Hub mirrors (2026)
    ├── doi-formats.md    # DOI format reference
    └── usage-examples.md # More examples
```

## 🔄 Changelog

### v3.1.0 (2026-03-23)
- ✨ **Direct PDF extraction** - No browser needed!
- ✨ Fixed iframe src parsing (handles `src = "..."`)
- ✨ Added protocol-relative URL handling
- 🐛 Removed unnecessary browser automation code
- 📝 Simplified codebase

### v3.0.0
- Initial multi-source implementation

## ⚖️ Disclaimer

**For educational and research purposes only.**

Users are responsible for understanding copyright laws in their jurisdiction.

## 📜 License

MIT