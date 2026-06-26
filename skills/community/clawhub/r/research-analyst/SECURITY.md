# Security Policy - Research Analyst v1.4.0 (Minimal)

## Overview

This is a **bundled code** skill with minimal dependencies and zero external downloads.

**Security Model**:
- ✅ All Python code bundled in skill package
- ✅ Code reviewed by ClawHub during submission
- ✅ No runtime downloads (scripts don't fetch external code, no git operations)
- ✅ Only public APIs (read-only GET requests)
- ✅ No credentials required
- ✅ No subprocess calls
- ✅ No system modifications

## What's Included

### Python Scripts (5 files, 139KB)

All scripts bundled with this skill:

1. `scripts/stock_analyzer.py` (99KB) - Main analysis engine
2. `scripts/portfolio_manager.py` (20KB) - Portfolio tracking
3. `scripts/dividend_analyzer.py` (14KB) - Dividend analysis
4. `scripts/cn_stock_quotes.py` (3KB) - China market quotes
5. `scripts/cn_market_rankings.py` (3KB) - China market rankings

**Source**: https://github.com/ZhenRobotics/openclaw-research-analyst

### Dependencies (requirements.txt)

All from PyPI:

```
yfinance==0.2.40
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
pandas==2.2.0
numpy==1.26.3
+ transitive dependencies
```

**Installation**: `pip install -r requirements.txt`

## Data Flow

### What Gets Fetched (Read-Only)

- Stock quotes from `query1.finance.yahoo.com`
- Crypto data from `api.coingecko.com`
- News from `news.google.com`
- China market data from `sina.com.cn`, `eastmoney.com`

All requests are **HTTP GET** - read-only, no data upload.

### What Gets Sent

- API queries only (ticker symbols, date ranges)
- No authentication headers
- No personal data
- No analytics or tracking

### What Stays Local

- All analysis results (computed locally)
- Portfolio data (`~/.clawdbot/skills/research-analyst/portfolios.json`)
- Cached API responses (optional, local only)

**No data leaves your machine** except for public API queries.

## Trust Model

### Bundled Code (This Skill)

**Trust decision**: You trust ClawHub's review process.

- ✅ Code reviewed by ClawHub during skill submission
- ✅ Source available for inspection on GitHub
- ✅ MIT-0 license (public domain)
- ✅ No obfuscation, fully readable Python

**Verification**:
```bash
# View main script
cat scripts/stock_analyzer.py

# Check for network calls (should only see GET)
grep -r "requests\." scripts/

# Check for POST (should be empty)
grep -ri "method.*post\|requests\.post" scripts/

# Check for subprocess (should be empty)
grep -r "subprocess\|os\.system" scripts/
```

### PyPI Dependencies

**Trust decision**: You trust the PyPI ecosystem.

Standard, widely-used packages:
- `yfinance` - ~50M downloads
- `requests` - ~500M downloads
- `beautifulsoup4` - ~100M downloads
- `pandas` - ~100M downloads

**Mitigation**:
- Install in virtual environment
- Install in isolated environment for safety
- Review `requirements.txt` for full dependency list

## Installation Security

### Recommended Installation

```bash
# 1. Create isolated environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test
python3 scripts/stock_analyzer.py AAPL
```

### Optional: Container Isolation

For maximum security, run in container:

```bash
docker run -it -v $(pwd):/app python:3.10 bash
cd /app && pip install -r requirements.txt
python3 scripts/stock_analyzer.py AAPL
```

### Advanced: Supply Chain Verification

For additional supply chain security:

```bash
# 1. Review package metadata on PyPI before installing
# Visit: https://pypi.org/project/yfinance/
# Check: recent updates, maintainers, download stats

# 2. Download packages for inspection (optional)
pip download -r requirements.txt -d ./packages
ls -lh ./packages/  # Review downloaded files

# 3. Install from downloaded packages
pip install --no-index --find-links=./packages -r requirements.txt

# 4. Verify no unexpected network calls during import
python3 -c "import yfinance; import requests; import pandas"
# Should complete without network activity
```

## Verification

### Automated Verification

```bash
bash verify_install.sh
```

**Checks**:
1. ✅ Python environment (version 3.10+)
2. ✅ requirements.txt exists
3. ✅ Key files present
4. ✅ No suspicious patterns (eval, exec, subprocess)

**Results**:
- `Exit code 0`: All checks passed
- `Exit code 1`: Critical errors detected

### Manual Verification

```bash
# 1. Check file integrity
ls -lh scripts/*.py

# Expected: 5 files
# stock_analyzer.py, portfolio_manager.py, dividend_analyzer.py,
# cn_stock_quotes.py, cn_market_rankings.py

# 2. Scan for suspicious patterns
grep -r "eval(\|exec(\|compile(" scripts/
# Should be empty

# 3. Check network behavior
grep -r "requests\." scripts/
# Should only see requests.get(), not requests.post()

# 4. Check subprocess usage
grep -r "subprocess\|os\.system" scripts/
# Should be empty
```

## What This Skill Does NOT Do

- ❌ Download external code (all bundled)
- ❌ Execute subprocess calls
- ❌ Modify system files or cron
- ❌ Require credentials or API keys
- ❌ Upload data to external servers
- ❌ Use eval/exec for dynamic code execution
- ❌ Install additional packages at runtime

## Risk Assessment

### Low Risk

- ✅ Bundled code (reviewed by ClawHub)
- ✅ Read-only API calls (public data sources)
- ✅ Local storage only
- ✅ No credentials required
- ✅ No system modifications

### Low Risk (with standard mitigations)

- ℹ️ PyPI dependencies (mainstream packages with millions of downloads)
  - `requests` (~500M downloads/month)
  - `pandas` (~100M downloads/month)
  - `yfinance` (~50M downloads/month)
  - All pinned to specific versions
- ℹ️ Network requests to public APIs (read-only, rate-limited)

**Mitigations in place**:
- Pinned versions prevent unexpected updates
- All packages are widely-used, established projects
- Virtual environment isolation recommended
- No elevated privileges required
- Local execution only (no cloud dependencies)

### Not Applicable

- ❌ External code execution (not used)
- ❌ Credential theft (no credentials)
- ❌ System compromise (no privilege escalation)

## Known Limitations

1. **API Rate Limits**
   - Yahoo Finance: ~2000 requests/hour
   - CoinGecko: 50 calls/minute (free tier)

2. **Data Lag**
   - Yahoo Finance data may lag 15-20 minutes
   - Short interest lags ~2 weeks

3. **Geographic Restrictions**
   - China market data may require VPN outside China

## Reporting Security Issues

**Found a security issue?**

- **Email**: security@zhenrobotics.com
- **GitHub**: https://github.com/ZhenRobotics/openclaw-research-analyst/security/advisories/new

**Please include**:
- Description of the issue
- Steps to reproduce
- Affected files/functions
- Suggested fix (if any)

**Response time**: Within 48 hours for critical issues.

## Security Changelog

### v1.4.0-minimal (2026-03-28)

**Bundled code architecture** - Major security improvement:

- ✅ Removed all external downloads (no git clone)
- ✅ Removed all subprocess calls
- ✅ Removed external tool dependencies
- ✅ Minimal feature set (5 core scripts only)
- ✅ ClawHub reviewed all bundled code

**Removed features** (security-motivated):
- Watchlist manager (used subprocess)
- Twitter integration (external CLI + credentials)
- News ML training (model downloads)
- Scheduling (cron modification)
- Feishu notifications (webhook credentials)

### v1.3.3 (2026-03-27)

- Added GPG signature verification
- Added `verify_install.sh` script
- Pinned dependency versions
- Download model (external git clone)

## License

MIT-0 (Public Domain) - See LICENSE

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE**

This tool is for informational purposes only. Not investment advice. Always do your own research.

---

**Questions?** https://github.com/ZhenRobotics/openclaw-research-analyst/issues
