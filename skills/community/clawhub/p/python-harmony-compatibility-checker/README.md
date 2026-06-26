# Python HarmonyOS Compatibility Checker

🔍 Check if Python libraries are compatible with HarmonyOS (OpenHarmony)

## Features

- **Source Download** - GitHub (preferred) or PyPI
- **Windows Dependency Detection** - Scans for win32api, pythoncom, pywin32
- **Pytest Integration** - Per-test-case reporting
- **Environment Issue Detection** - Distinguishes permission issues from real failures
- **Comprehensive Reports** - Markdown + JSON

## Installation

```bash
clawhub install python-harmony-compatibility-checker
```

## Usage

```bash
# Single package
python scripts/check_compatibility.py requests

# Multiple packages
python scripts/check_compatibility.py requests numpy pandas

# From requirements
python scripts/check_compatibility.py -r requirements.txt

# Keep source
python scripts/check_compatibility.py --keep-source numpy
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-w, --workers N` | Parallel workers | 4 |
| `--sequential` | One at a time | False |
| `-r, --requirements FILE` | Requirements file | - |
| `--keep-source` | Keep downloaded source | False |

## Output

```
📦 numpy v2.2.1
   Status: ✅ Compatible
   Test Pass Rate: 88.9%
   Total: 45 tests | Passed: 40 | Failed: 5
```

Reports: `compatibility_report_*.md` and `compatibility_report_*.json`

## Known Compatible

- `requests`, `numpy` (45 tests, 88.9%), `pandas`, `flask`, `django`, `pytest`, `beautifulsoup4`, `pillow`

## Known Incompatible

- `xlwings` (win32com, pythoncom), `pywin32`, `wmi`

## Requirements

- Python 3.8+
- pytest (optional)
- Network access

## License

MIT
