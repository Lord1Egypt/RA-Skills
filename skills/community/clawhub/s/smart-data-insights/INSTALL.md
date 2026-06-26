# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip3
- OpenClaw installed

## Quick Install

### Option 1: One-Command Install (Recommended)

```bash
# Clone and install
git clone https://github.com/yourusername/data-analyst-skill.git
cd data-analyst-skill
./install.sh
```

### Option 2: Manual Install

```bash
# 1. Install Python dependencies
pip3 install pandas openpyxl matplotlib seaborn

# 2. Copy skill to OpenClaw
cp -r ~/.openclaw/skills/data-analyst ~/.openclaw/skills/

# 3. Verify installation
~/.openclaw/skills/data-analyst/test.sh
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >=1.3.0 | Data manipulation |
| openpyxl | >=3.0.0 | Excel file support |
| matplotlib | >=3.4.0 | Visualization |
| seaborn | >=0.11.0 | Statistical graphics |

## Installation Verification

### Test 1: Check Dependencies

```bash
python3 -c "import pandas, matplotlib, openpyxl; print('✅ All dependencies OK')"
```

### Test 2: Run Test Suite

```bash
bash ~/.openclaw/skills/data-analyst/test.sh
```

### Test 3: Quick Analysis

```bash
# Create test file
echo "name,age,city
Alice,25,NYC
Bob,30,LA
Charlie,35,Chicago" > /tmp/test.csv

# Run analysis
python3 ~/.openclaw/skills/data-analyst/tools/analyze.py /tmp/test.csv

# Cleanup
rm /tmp/test.csv
```

## Troubleshooting

### Issue: "Module not found"

```bash
# Solution: Install missing module
pip3 install pandas
pip3 install openpyxl
pip3 install matplotlib
```

### Issue: "Permission denied"

```bash
# Solution: Fix permissions
chmod +x ~/.openclaw/skills/data-analyst/tools/*.py
chmod +x ~/.openclaw/skills/data-analyst/test.sh
```

### Issue: "Command not found: python3"

```bash
# Solution: Use python instead
# Or install Python 3
sudo apt-get install python3  # Ubuntu/Debian
brew install python3          # macOS
```

### Issue: "pip3 install fails"

```bash
# Solution: Upgrade pip
pip3 install --upgrade pip

# Or use --user flag
pip3 install --user pandas openpyxl matplotlib
```

### Issue: "Charts not generating"

```bash
# Solution: Install matplotlib backend
pip3 install matplotlib[backends]

# For headless servers
export MPLBACKEND=Agg
```

## Environment Setup

### For Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### For Production

```bash
# System-wide install
sudo pip3 install pandas openpyxl matplotlib seaborn

# Or user install
pip3 install --user pandas openpyxl matplotlib seaborn
```

## Configuration

### Default Settings

Edit `~/.openclaw/skills/data-analyst/config.json`:

```json
{
  "default_encoding": "utf-8",
  "chart_style": "professional",
  "chart_dpi": 150,
  "max_rows_sample": 100000,
  "outlier_threshold": 3.0
}
```

### Custom Templates

Place custom report templates in:
```
~/.openclaw/skills/data-analyst/templates/
```

## Updating

```bash
# Pull latest version
cd ~/.openclaw/skills/data-analyst
git pull

# Update dependencies
pip3 install --upgrade pandas openpyxl matplotlib seaborn

# Re-run tests
./test.sh
```

## Uninstalling

```bash
# Remove skill
rm -rf ~/.openclaw/skills/data-analyst

# Remove dependencies (optional)
pip3 uninstall pandas openpyxl matplotlib seaborn
```

## Support

Having issues? Check:
1. [Troubleshooting Guide](references/troubleshooting.md)
2. [FAQ](FAQ.md)
3. [GitHub Issues](https://github.com/yourusername/data-analyst-skill/issues)

## Next Steps

After installation:
1. Read the [README](README.md)
2. Try the [Quick Start](README.md#quick-start)
3. Explore [Examples](README.md#examples)
4. Check [Command Reference](README.md#command-reference)
