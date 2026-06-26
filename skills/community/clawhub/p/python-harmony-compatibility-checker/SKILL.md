---
name: python-harmony-compatibility-checker
description: Check Python library compatibility with HarmonyOS. Downloads source from GitHub/PyPI, detects Windows-specific dependencies, runs pytest with per-test-case reporting, and generates detailed compatibility reports.
---

# Python HarmonyOS Compatibility Checker

## When to Use

- Check if a Python package works on HarmonyOS
- Validate multiple packages before deployment
- Migrate a Python project to HarmonyOS
- Detect Windows-specific API dependencies (win32api, pythoncom, pywin32, etc.)

## Usage

```bash
# Single package
python scripts/check_compatibility.py requests

# Multiple packages (parallel, 4 workers default)
python scripts/check_compatibility.py requests numpy pandas flask

# Specify workers
python scripts/check_compatibility.py --workers 8 requests numpy pandas

# From requirements file
python scripts/check_compatibility.py -r requirements.txt
python scripts/check_compatibility.py -w 8 -r requirements.txt

# Sequential mode (debugging)
python scripts/check_compatibility.py --sequential requests numpy

# Keep downloaded source for verification
python scripts/check_compatibility.py --keep-source numpy
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-w, --workers N` | Number of parallel workers | 4 |
| `--sequential` | Run checks one at a time | False |
| `-r, --requirements FILE` | Check packages from requirements file | - |
| `--keep-source` | Keep downloaded source code for verification | False |

## Output

Reports saved to current directory:
- `compatibility_report_*.md` - Markdown with summary and details
- `compatibility_report_*.json` - Machine-readable with per-test-case results

Timestamps use **东八区时间 (UTC+8/北京时间)**.

### Example (numpy)

```
📦 numpy v2.2.1
   Status: ✅ Compatible
   Test Pass Rate: 88.9%
   Total: 45 tests | Passed: 40 | Failed: 5
```

### Metrics

| Metric | Description |
|--------|-------------|
| **Total Tests** | Individual test functions run |
| **Passed** | Successfully completed |
| **Failed** | Failed due to code issues |
| **Environment Issues** | Permission/temp dir failures (not counted) |
| **Pass Rate** | `passed / total` |
| **Valid Pass Rate** | `passed / (passed + failed)` - excludes environment issues |

## Test Workflow

1. **Download Source** - GitHub (preferred) or PyPI
2. **Windows Check** - Scan for Windows-specific imports (win32api, pythoncom, pywin32, ctypes.windll)
   - Found → **Incompatible** (no further testing)
3. **Find Tests** - From installed package (preferred) or source
4. **Run Tests** - pytest with verbose output, per-function reporting
5. **Analyze** - Categorize: environment issues vs code issues
6. **Report** - Markdown + JSON with detailed results

### Status

| Status | Criteria |
|--------|----------|
| **✅ Compatible** | Installs + valid pass rate ≥ 80% + no Windows deps |
| **⚠️ Partial** | Installs + valid pass rate 50-79% |
| **❌ Incompatible** | Cannot install OR valid pass rate < 50% OR Windows deps detected |

### Error Classification

| Type | Description | Counts Against |
|------|-------------|----------------|
| **Environment** | Permission errors, temp dir issues | ❌ No |
| **Code** | Import errors, API incompatibilities | ✅ Yes |
| **Platform** | Windows/macOS/X11 dependencies | ✅ Yes |

## Known Issues

### Platform Dependencies

| Platform | Problematic Packages | Alternative |
|----------|---------------------|-------------|
| Windows | pywin32, wmi, pythoncom, **xlwings** | Cross-platform libs |
| macOS | applescript, quartz, cocoa | - |
| X11 | python-xlib, xcb | pynput |

### Windows Module Detection

Scans for: `win32api`, `win32con`, `win32gui`, `win32com`, `pythoncom`, `pywintypes`, `ctypes.windll`, `winsound`, `msvcrt`

**Detection includes:**
- Direct imports: `import win32api`, `from win32com import ...`
- Dynamic imports: `importlib.import_module('pythoncom')`
- ctypes Windows DLL: `ctypes.windll`, `ctypes.WinDLL`
- References in setup.py, pyproject.toml

### Compatible Packages

- `requests`, `numpy` (45 tests, 88.9%), `pandas`, `flask`, `django`, `pytest`, `beautifulsoup4`, `pillow`

## Scripts

### check_compatibility.py

**Features:**
- Source download from GitHub/PyPI
- Windows dependency detection
- Test discovery from installed package or source
- pytest integration with per-test-case reporting
- Environment issue detection
- Source code retention (`--keep-source`)

**pytest Integration:**
- Uses `pytest -v --tb=short --import-mode=importlib`
- Runs from `/tmp` to avoid source import conflicts
- Parses output for individual test function results
- Limits to 15 test files, shows progress every 5 files

## Troubleshooting

### Permission Errors

```bash
# Clean up pytest temp directories
rm -rf pytest-of-*
```

### Source Verification

```bash
# Keep source for inspection
python scripts/check_compatibility.py --keep-source xlwings

# Check Windows imports
grep -r "import win32" /path/to/source/
```

### False Positives

Some failures may be due to:
- Missing optional system libraries
- Network-dependent tests
- pytest configuration issues

Review detailed reports to distinguish real incompatibilities from environment issues.

## Integration

### CI/CD

```yaml
- name: HarmonyOS Compatibility
  run: python scripts/check_compatibility.py -r requirements.txt --keep-source
```

### Programmatic

```python
from scripts.check_compatibility import check_package
result = check_package("requests")
print(f"Compatible: {result.compatible}, Issues: {result.issues}")
```

## Limitations

- Binary dependencies may fail to compile
- Some packages require system-level dependencies
- Pure HarmonyOS (NEXT) has stricter security policies
- Not all packages have unit tests
- Network required for source download

## Related

- `references/python-env-setup.md` - Python setup on HarmonyOS
- `references/compatibility-database.md` - Known package status

## Best Practices

### For Users

1. Review error classifications (environment vs code)
2. Use `--keep-source` to verify tested code
3. Run multiple times for transient failures
4. Check Windows dependencies first

### For Authors

1. Include tests in your package
2. Use pytest
3. Avoid platform-specific tests (or use `@pytest.mark.skipif`)
4. Document system dependencies
5. Use conditional imports: `if sys.platform == 'win32'`
