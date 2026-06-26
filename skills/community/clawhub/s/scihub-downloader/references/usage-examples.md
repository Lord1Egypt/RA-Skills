# Usage Examples for Paper Downloader v3.0

## 🎯 Basic Examples

### 1. Download by DOI

```bash
# Simple DOI download
scihub-dl "10.1038/nature12373"

# With URL prefix (auto-stripped)
scihub-dl "https://doi.org/10.1016/j.enggeo.2023.107123"

# Output: ~/Downloads/papers/Author_Year.pdf
```

### 2. Download by PMID

```bash
scihub-dl "PMID:36871234"
# or just the number
scihub-dl "36871234"

# Output: ~/Downloads/papers/PMID_36871234.pdf
```

### 3. Download by Title

```bash
scihub-dl "deep learning for slope stability analysis"

# Steps:
# 1. Searches CrossRef for DOI
# 2. Checks OA sources
# 3. Falls back to Sci-Hub if needed
```

### 4. Download arXiv Preprint

```bash
scihub-dl "arXiv:2301.00001"
# or
scihub-dl "2301.00001"

# arXiv papers are always OA
```

## 🔧 Output Control

### Custom Directory

```bash
# Download to specific folder
scihub-dl "10.1038/nature12373" -o ~/papers/

# Download to research workspace
scihub-dl "10.1038/nature12373" \
  -o ~/.openclaw/workspace-research/literature/

# Create project-specific folder
scihub-dl "10.1038/nature12373" \
  -o ~/research/project-alpha/papers/
```

### Custom Filename

```bash
# Specify exact filename
scihub-dl "10.1038/nature12373" -f important-paper.pdf

# Combine with directory
scihub-dl "10.1038/nature12373" \
  -o ~/papers/ -f nature-thermometry.pdf
```

### JSON Output

```bash
# Get metadata as JSON (useful for automation)
scihub-dl "10.1038/nature12373" --json

# Output:
{
  "title": "Nanometre-scale thermometry...",
  "author": "Kucsko",
  "year": "2013",
  "journal": "Nature",
  "doi": "10.1038/nature12373",
  "file": "/home/user/papers/Kucsko_2013.pdf",
  "source": "Unpaywall"
}
```

## 📊 Check & Debug

### Check Availability

```bash
# Check if paper is available (no download)
scihub-dl "10.1038/nature12373" --check

# Output:
# ✓ PDF available at: https://...
# ℹ Source: Unpaywall
```

### Verbose Mode

```bash
# See all attempts and URLs
scihub-dl "10.1038/nature12373" -v

# Output includes:
# - CrossRef metadata fetch
# - Each source checked
# - URLs attempted
# - Error details
```

### Open Access Only

```bash
# Skip Sci-Hub, only use legal OA sources
scihub-dl "10.1038/nature12373" --oa-only

# Useful when:
# - You want to ensure legal access
# - Sci-Hub is blocked
# - Working in restricted environment
```

## 🌐 Sci-Hub Options

### Use Specific Mirror

```bash
# Use sci-hub.st (recommended)
scihub-dl "10.1038/nature12373" -m sci-hub.st

# Try sci-hub.ru
scihub-dl "10.1038/nature12373" -m sci-hub.ru
```

### More Retries

```bash
# Increase retry attempts
scihub-dl "10.1038/nature12373" -r 5

# With verbose
scihub-dl "10.1038/nature12373" -r 5 -v
```

### Browser Required Case

```bash
# When Sci-Hub needs browser, you'll see:
scihub-dl "10.1038/s43017-022-00373-x" -v

# Output:
# → Trying Sci-Hub mirrors...
# ⚠ Sci-Hub requires browser for PDF access
# ℹ Please open in browser: https://sci-hub.st/10.1038/s43017-022-00373-x
```

## 📦 Batch Processing

### From DOI List

```bash
# Create DOI list (dois.txt)
cat > dois.txt << EOF
10.1038/nature12373
10.1016/j.enggeo.2023.107123
10.1029/2023GL010345
EOF

# Batch download with delay
while read doi; do
  echo "Downloading: $doi"
  scihub-dl "$doi" -o ~/papers/
  sleep 3  # Be nice to servers
done < dois.txt
```

### From BibTeX

```bash
# Extract DOIs from BibTeX
grep -oP '(?<=doi=\{)[^}]+' references.bib | while read doi; do
  scihub-dl "$doi" -o ~/papers/
  sleep 3
done
```

### From CSV

```bash
# Assuming CSV with DOI column
cut -d',' -f2 papers.csv | tail -n +2 | while read doi; do
  [ -n "$doi" ] && scihub-dl "$doi" -o ~/papers/
  sleep 3
done
```

### Parallel Downloads (Advanced)

```bash
# Download 5 papers in parallel
cat dois.txt | xargs -P 5 -I {} scihub-dl {} -o ~/papers/
```

## 🔗 Integration Examples

### With Literature Management

```bash
# Download and add to Zotero
doi="10.1038/nature12373"
scihub-dl "$doi" -o /tmp/
# Then: Zotero → File → Import

# Generate BibTeX entry
curl -s "https://api.crossref.org/works/$doi" | \
  jq -r '.message | "@article{\(.DOI), title={(.title[0])} }"'
```

### With Reading Workflow

```bash
# Download and extract text
doi="10.1038/nature12373"
scihub-dl "$doi" -o ~/papers/
pdftotext ~/papers/paper.pdf ~/papers/paper.txt

# Search for keywords
grep -i "slope stability" ~/papers/paper.txt
```

### With Research Workspace

```bash
# Organized project structure
PROJECT="slope-stability-project"
mkdir -p ~/research/$PROJECT/{papers,data,notes}

# Download to project
scihub-dl "10.1038/nature12373" \
  -o ~/research/$PROJECT/papers/
```

## 🐛 Troubleshooting Examples

### Mirror Blocked

```bash
# Try different mirrors
for mirror in sci-hub.st sci-hub.ru sci-hub.wf; do
  echo "Trying $mirror..."
  scihub-dl "10.1038/nature12373" -m $mirror && break
done
```

### VPN Required

```bash
# Check if Sci-Hub is accessible
curl -I https://sci-hub.st

# If blocked, connect VPN and retry
# Or use --oa-only
scihub-dl "10.1038/nature12373" --oa-only
```

### Invalid PDF

```bash
# Check what was downloaded
file ~/papers/paper.pdf

# If HTML, the paper may not be available
# Try alternative sources:
# - Unpaywall extension
# - Open Access Button
# - ResearchGate
```

## 💡 Pro Tips

### 1. Create Alias

```bash
# Add to ~/.bashrc
alias paper='~/.openclaw/skills/scihub-downloader/scripts/scihub-dl.sh'

# Use shorter command
paper "10.1038/nature12373"
```

### 2. Auto-organize by Year

```bash
# Organize papers by publication year
download_organized() {
  local doi="$1"
  local year=$(curl -s "https://api.crossref.org/works/$doi" | \
    grep -o '[0-9]\{4\}' | head -1)
  mkdir -p ~/papers/$year
  scihub-dl "$doi" -o ~/papers/$year/
}
```

### 3. Log Downloads

```bash
# Keep track of downloaded papers
scihub-dl "10.1038/nature12373" -o ~/papers/ --json >> ~/papers/log.json
```

### 4. Smart Batch Script

```bash
#!/bin/bash
# smart-batch.sh - Download with error handling

LOG="download_log.txt"
ERRORS="failed_downloads.txt"

while read doi; do
  echo "$(date): Downloading $doi" >> $LOG
  
  if scihub-dl "$doi" -o ~/papers/ 2>&1 | tee -a $LOG; then
    echo "$(date): SUCCESS: $doi" >> $LOG
  else
    echo "$doi" >> $ERRORS
    echo "$(date): FAILED: $doi" >> $LOG
  fi
  
  sleep 3
done < dois.txt
```

## 📚 Example Workflows

### Literature Review

```bash
# 1. Create project
mkdir -p ~/research/lit-review/{papers,notes}

# 2. Download papers from reading list
cat reading_list.txt | while read doi; do
  scihub-dl "$doi" -o ~/research/lit-review/papers/ -v
  sleep 2
done

# 3. Extract titles for notes
for pdf in ~/research/lit-review/papers/*.pdf; do
  pdftotext "$pdf" - | head -20 > "${pdf%.pdf}_notes.txt"
done
```

### Research Project

```bash
# Setup
PROJECT="landslide-monitoring-2026"
mkdir -p ~/research/$PROJECT/{papers,data,scripts}

# Download core papers
CORE_DOIS=(
  "10.1038/s43017-022-00373-x"  # Casagli et al.
  "10.1007/s12303-017-0034-4"   # Chae et al.
  "10.1016/j.enggeo.2023.107123"
)

for doi in "${CORE_DOIS[@]}"; do
  scihub-dl "$doi" -o ~/research/$PROJECT/papers/ -v
  sleep 3
done
```

---

**Last Updated**: 2026-03-23
**Version**: 3.0