# 📄 `rebrand.py`

**Path:** `/run/media/axioma/Merlin/axiom-rebrand/axiom_rebrand/rebrand.py`  
**Size:** 16,385 bytes / 431 lines  
**Hash:** `6f82ab1a18a4ec16`  
**Generated:** 2026-06-15T01:00:47.156159+00:00

## 📝 Module Docstring

```
rebrand — Generic rebrand pipeline.

Transforms an internal source directory into a public destination directory
suitable for publication (marketplace, open-source, multi-tenant).

Operations (in order):
  1. Copy .py, .md, LICENSE, *.json, *.yaml from source → destination
  2. Strip jargon (configurable patterns)
  3. Fix hardcoded sys.path inserts in test files
  4. Regenerate MANIFEST.txt with SHA-256 hashes
  5. Validate via custom validator (if provided)
  6. Return byte-to-byte audit report

Idempotent: running twice produces identical output (modulo timestamps).
Pure Python stdlib, zero dependencies.
```

## 📦 Imports (17)

```python
import __future__.annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import pathlib.Path
import typing.Dict
import typing.List
import typing.Optional
import typing.Tuple
import yaml
import yaml
```

## ⚡ Functions (11)

### `def sha256_file(path):`
> Compute SHA-256 of a file (byte-to-byte).

### `def load_jargon_from_config(config_path):`
> Load jargon patterns from a config file.

Supports 3 formats, auto-detected by extension then content:
- `.yaml` / `.yml` → YAML structured (requires PyYAML)
- `.json` → JSON structured
- other / no e

### `def strip_jargon(text, patterns):`
> Remove jargon from a string. Returns (cleaned, n_stripped).

### `def fix_sys_path(text):`
> Replace hardcoded sys.path.insert with Path(__file__).parent.
Returns (fixed, n_fixed).

### `def remove_blank_lines_excess(text):`
> Remove runs of 3+ blank lines down to 2 (clean docstring format).

### `def rebrand_file(src, dst, patterns):`
> Copy a file from src to dst, stripping jargon and fixing paths.
Returns audit info.

### `def regenerate_manifest(dst_dir, project_name):`
> Regenerate MANIFEST.txt with SHA-256 of all files in dst_dir.

Akasha-style: NO timestamp, NO random, NO env-dependent content.
Same input → same output, byte-to-byte, forever.

### `def validate(dst_dir, validator):`
> Run a custom validator on dst_dir. Returns True if it passes.

### `def run_tests(dst_dir):`
> Run all test_*.py in dst_dir. Returns True if all OK.

### `def rebrand_project(src_root, dst_root, project_name):`
> Rebrand an entire project directory.

Returns an audit report with byte-to-byte info.

### `def main(argv):`
