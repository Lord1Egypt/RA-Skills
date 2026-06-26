# Paper Downloader v3.1

📄 **Multi-source academic paper download with direct PDF link extraction.**

## ✨ New in v3.1

- **Direct PDF Extraction**: No browser automation needed!
- **Smart iframe Parsing**: Handles `src = "..."` with spaces
- **Protocol-Relative URLs**: Correctly handles `//pdf.sci-net.xyz/...`
- **Simplified Code**: Removed unnecessary browser dependencies

## 🚀 Features

- ✅ Multiple Open Access sources (Unpaywall, PMC, Semantic Scholar)
- ✅ arXiv preprint support
- ✅ Sci-Hub with direct PDF link extraction
- ✅ Smart filename generation (Author_Year.pdf)
- ✅ JSON output for automation
- ✅ Verbose mode for debugging

## 📦 Installation

```bash
# The skill is already installed in OpenClaw
# Direct usage:
~/.openclaw/skills/scihub-downloader/scripts/scihub-dl.sh "10.1038/nature12373"

# Optional: Create alias
alias scihub-dl='~/.openclaw/skills/scihub-downloader/scripts/scihub-dl.sh'
```

## 📖 Usage

### Basic

```bash
# DOI
scihub-dl "10.1038/nature12373"

# PMID
scihub-dl "PMID:36871234"

# Title
scihub-dl "slope stability analysis machine learning"
```

### Advanced

```bash
# Open Access only
scihub-dl "10.1038/nature12373" --oa-only

# Custom output
scihub-dl "10.1038/nature12373" -o ~/papers/ -f my-paper.pdf

# Check availability
scihub-dl "10.1038/nature12373" --check -v
```

## 🌐 Sci-Hub Access (2026)

### Current Status

| Mirror | Status | Action |
|--------|--------|--------|
| sci-hub.st | ✅ Working | **Primary choice** |
| sci-hub.ru | ✅ Working | Backup |
| sci-hub.se | ❌ Blocked | Avoid |
| sci-hub.wf | ⚠️ Protected | May need VPN |

### Manual Browser Download

If script returns `BROWSER_REQUIRED`:

1. Open browser
2. Go to: `https://sci-hub.st/<DOI>`
3. Wait for PDF to load
4. Download manually

### Why Browser Required?

Sci-Hub now uses JavaScript to:
- Load PDF dynamically
- Bypass simple HTTP requests
- Protect against automated access

## 🔧 Technical Details

### Download Priority

```
1. Unpaywall (Legal OA)     → Success: ~40%
2. PubMed Central (Legal)   → Success: ~15%
3. Semantic Scholar (Legal) → Success: ~10%
4. Sci-Hub (Shadow)         → Success: ~90%+ (may need browser)
```

### File Naming

```
Priority:
1. Author_Year.pdf (if metadata available)
2. paper_<DOI>.pdf (fallback)
3. paper_<timestamp>.pdf (last resort)
```

### Error Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | General error / not found |
| 2 | Network error |
| 3 | Invalid identifier |

## 📚 Integration Examples

### With Zotero

```bash
# Download to Zotero import folder
scihub-dl "10.1038/nature12373" -o ~/Zotero/import/
# Then: File → Import in Zotero
```

### With Python

```python
import subprocess
import json

def download_paper(doi, output_dir):
    result = subprocess.run([
        'scihub-dl', doi, '-o', output_dir, '--json'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None
```

### With Bash Script

```bash
#!/bin/bash
# batch-download.sh

while read doi; do
    echo "Downloading: $doi"
    scihub-dl "$doi" -o ~/papers/
    sleep 3  # Be nice to servers
done < dois.txt
```

## 🐛 Troubleshooting

### "BROWSER_REQUIRED" message

**Cause**: Sci-Hub needs JavaScript

**Solution**:
```bash
# Option 1: Open in browser manually
open "https://sci-hub.st/<DOI>"

# Option 2: Use Open Access sources
scihub-dl "<DOI>" --oa-only

# Option 3: Alternative sources
# - Unpaywall browser extension
# - Open Access Button
# - ResearchGate
```

### "Could not find PDF"

**Causes**:
- Paper very recent (< 1 week)
- Small/local journal
- Embargoed content

**Solutions**:
- Wait a few days
- Contact author via ResearchGate
- Use interlibrary loan

### "Connection failed"

**Causes**:
- Mirror blocked
- Network firewall
- Geographic restriction

**Solutions**:
- Try different mirror
- Use VPN
- Check with `curl -I https://sci-hub.st`

## 📖 API Reference

### Command Line Options

```
Positional:
  <identifier>         DOI, PMID, title, or URL

Options:
  -o, --output DIR     Output directory
  -f, --filename NAME  Custom filename
  -m, --mirror DOMAIN  Sci-Hub mirror
  -r, --retry NUM      Retry attempts (default: 2)
  -t, --timeout SEC    Timeout in seconds (default: 30)
  -c, --check          Check only, don't download
  -v, --verbose        Verbose output
  --oa-only            Open Access sources only
  --no-browser         Disable browser detection
  --json               JSON output
  -h, --help           Show help
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error / Not found |
| 2 | Network error |

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Browser Automation**: Integrate Playwright/Puppeteer
2. **More Sources**: Add Google Scholar, Library Genesis
3. **Better Metadata**: Improve DOI/author detection
4. **Batch Processing**: Parallel downloads

## 📄 License

MIT License

## 🙏 Acknowledgments

- Unpaywall for legal OA access
- Sci-Hub for democratizing research
- Open science advocates worldwide

---

**Version**: 3.0.0
**Updated**: 2026-03-23
**Author**: OpenClaw Team