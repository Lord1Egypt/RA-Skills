---
name: scripting-utils
description: Universal scripting utilities supporting 8+ languages (Bash, PowerShell, Python, Perl/Raku, JavaScript, Tcl), IRC bot frameworks (pbot, Limnoria), system management (systemd, Ubuntu/CentOS), and WebSearch integration. Provides syntax validation, code generation, best-practice linting, and cross-platform compatibility checks. Use when (1) Writing or validating scripts in any supported language, (2) Needing IRC bot command syntax, (3) Managing systemd services across Ubuntu/CentOS, (4) Validating JSON/API responses from web searches, (5) Converting between shell dialects, or (6) Batch-processing script validation.
---

# Scripting Utils

Universal scripting utilities with WebSearch integration for 8+ languages and IRC bot frameworks.

## Supported Languages

| Language | Command | Validation | Linting | WebSearch Docs |
|----------|---------|------------|---------|----------------|
| Bash | `bash` | ✅ shellcheck | ✅ | ✅ |
| sh (POSIX) | `sh` | ✅ shellcheck | ✅ | ✅ |
| Python | `python3` | ✅ pylint/mypy | ✅ | ✅ |
| Perl 5 | `perl` | ✅ perlcritic | ✅ | ✅ |
| Raku | `raku` | ✅ | ✅ | ✅ |
| PowerShell | `pwsh` | ✅ PSScriptAnalyzer | ✅ | ✅ |
| JavaScript | `node` | ✅ eslint | ✅ | ✅ |
| Tcl | `tclsh` | ✅ | ✅ | ✅ |

## IRC Bot Frameworks

| Framework | Language | Docs Source | Status |
|-----------|----------|-------------|--------|
| pbot | Perl 5 | https://github.com/pragma-/pbot | ✅ |
| Limnoria | Python | https://docs.limnoria.net/ | ✅ |
| Eggdrop | Tcl | https://docs.eggheads.org/ | ✅ |

## System Management

| System | Ubuntu | CentOS 8 | Command Matrix |
|--------|--------|----------|----------------|
| systemd | ✅ | ✅ | ✅ |
| packages (apt/yum) | ✅ | ✅ | ✅ |
| services | ✅ | ✅ | ✅ |
| networking | ✅ | ✅ | ✅ |

## WebSearch Integration

All modules support automatic documentation lookup:

```python
from scripting_utils import LanguageValidator

validator = LanguageValidator("powershell")
# Auto-fetches syntax from Microsoft docs if needed
result = validator.validate("$var = Get-Process")
```

## Modules

| Module | Purpose |
|--------|---------|
| `language_validator.py` | Multi-language syntax validation |
| `irc_bot_syntax.py` | pbot, Limnoria, Eggdrop command syntax |
| `system_manager.py` | systemd, Ubuntu/CentOS abstraction |
| `json_websearch.py` | JSON-Utils + WebSearch combination |
| `script_converter.py` | Cross-language script conversion |
| `batch_validator.py` | Batch validation of script directories |

## Quick Start

### Validate a script:
```bash
python scripts/language_validator.py script.ps1 --lang powershell
python scripts/language_validator.py script.pl --lang perl
```

### Get IRC bot command syntax:
```bash
python scripts/irc_bot_syntax.py --bot pbot --command "keyword add"
python scripts/irc_bot_syntax.py --bot limnoria --command "config channel"
```

### System command (Ubuntu vs CentOS):
```bash
python scripts/system_manager.py --action install --package nginx --os ubuntu
python scripts/system_manager.py --action install --package nginx --os centos
```

### JSON from WebSearch + Validate:
```python
from json_websearch import validate_search_result
from scripting_utils import WebSearchJSON

# Search API docs, validate response
result = WebSearchJSON.search_and_validate(
    query="github api repos endpoint",
    schema="github_api_schema.json"
)
```

## Integration with json-utils

The `json_websearch.py` module extends `json-utils` with WebSearch capabilities:

- Fetch API schemas from documentation
- Validate real API responses
- Batch-validate multiple endpoints
- Auto-repair common API response errors

See: `../json-utils/` for core JSON functionality.
