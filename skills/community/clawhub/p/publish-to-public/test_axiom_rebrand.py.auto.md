# 📄 `test_axiom_rebrand.py`

**Path:** `/run/media/axioma/Merlin/axiom-rebrand/test_axiom_rebrand.py`  
**Size:** 11,503 bytes / 299 lines  
**Hash:** `5352e0213f67aed2`  
**Generated:** 2026-06-15T01:00:47.154170+00:00

## 📝 Module Docstring

```
Tests for axiom-rebrand — Generic rebrand pipeline.

Verifies:
- strip_jargon() catches all major patterns
- fix_sys_path() rewrites hardcoded paths
- rebrand_file() is deterministic
- rebrand_project() is idempotent byte-to-byte
- Custom config patterns work
- Excludes work
```

## 📦 Imports (17)

```python
import os
import sys
import tempfile
import unittest
import pathlib.Path
import axiom_rebrand.rebrand_project
import axiom_rebrand.rebrand_file
import axiom_rebrand.strip_jargon
import axiom_rebrand.fix_sys_path
import axiom_rebrand.sha256_file
import axiom_rebrand.rebrand.DEFAULT_JARGON_PATTERNS
import axiom_rebrand.rebrand.DEFAULT_EXCLUDE_PATTERNS
import axiom_rebrand.rebrand.load_jargon_from_config
import axiom_rebrand.rebrand.load_jargon_from_config
import axiom_rebrand.rebrand.load_jargon_from_config
import shutil
import shutil
```

## 🏛️ Classes (6)

### `TestStripJargon`
> Verify strip_jargon() catches all known patterns.
**Methods:** `test_auteur_line, test_author_line, test_premier_jet, test_premier_jet_uppercase, test_first_draft_replaced, test_in_altum, test_cluster_axioma_stellaris_NOT_in_defaults, test_cluster_patterns_via_config, test_emoji_merlin_souleymane_via_config, test_path_removed`
_(+1 more)_

### `TestFixSysPath`
> Verify fix_sys_path() rewrites hardcoded paths.
**Methods:** `test_double_quote, test_single_quote, test_no_op_when_already_fixed`

### `TestSHA256`
**Methods:** `test_basic`

### `TestConfigLoading`
**Methods:** `test_json_config, test_yaml_config_by_extension, test_yml_config_by_extension, test_text_fallback_config`

### `TestIdempotence`
> Verify rebrand_project is idempotent byte-to-byte.
**Methods:** `setUp, tearDown, test_byte_to_byte_identical`

### `TestExcludes`
**Methods:** `setUp, tearDown, test_excluded_files_not_copied`
