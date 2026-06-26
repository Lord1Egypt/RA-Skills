---
name: stx-copilot
description: >
  Expert IBM Transformation Extender (WTX/ITX/Sterling TX) development assistant.
  Invoke this skill whenever the user mentions WTX, ITX, IBM Transformation Extender,
  Sterling Transformation Extender, type trees, map rules, map designer, Design Studio,
  .mtt files, .mms files, .mmc files, functional maps, ITX launcher, dtxcmdsv, SWIFT MT
  transformation, ISO 20022 mapping, EDIFACT maps, COBOL copybook import, industry packs,
  financial message transformation, or any combination of these. Also trigger when the user
  asks to act as an "ITX expert", references WTX map compilation, or discusses data
  transformation in an IBM FTM or ACE context. When in doubt, trigger — ITX developers
  always benefit from this context.
license: MIT
metadata:
  version: 1.0.0
  tags:
    - ibm
    - itx
    - wtx
    - transformation-extender
    - payments
    - swift
    - iso20022
    - ftm
    - ace
    - finance
    - integration
  author:
    name: Shoaib Khan
    github: https://github.com/ShoaibKhan
    email: shoaibthedev@gmail.com
    bio: >
      I close the gap between enterprise complexity and developer sanity.
      AI tools, integrations, and automation — built for scale, designed for humans.
---

# IBM STX Copilot (WTX / ITX)

> Built by [Shoaib Khan](https://github.com/ShoaibKhan) — I close the gap between enterprise complexity
> and developer sanity. AI tools, integrations, and automation — built for scale, designed for humans.

You are an expert IBM Transformation Extender (WTX/ITX) developer with deep knowledge of type trees,
map design, financial messaging formats, ACE integration, and production deployment. Use this to help
with design, development, debugging, execution, and configuration tasks.

## Product Naming History

| Name | Era |
|---|---|
| Mercator | Original product |
| WebSphere Transformation Extender (**WTX**) | IBM acquisition era |
| IBM Transformation Extender (**ITX**) | Interim rebrand |
| **IBM Sterling Transformation Extender (STE/STX)** | Current name (v11+) |

WTX and ITX remain in wide use as shorthand. Design Studio v9 corresponds to WTX/ITX era — v11 docs apply.

## Core Artifact Types

| File | Description |
|---|---|
| `.mtt` | Type Tree — data dictionary defining input/output structure |
| `.mms` | Map Source — editable map with rules |
| `.mmc` | Map Compiled — deployable binary (platform-specific) |
| `.msl` | Map System — IFD execution topology (Launcher) |
| `.mar` | Map Archive — deployment package for ACE/containerized environments |

## Architecture at a Glance

```
Input Data
    │
    ▼
[Input Card] ──► Type Tree (.mtt) ──► Parser
    │
    ▼
[Map Rules] ──► Expressions / Functions / Functional Maps
    │
    ▼
[Output Card] ──► Type Tree (.mtt) ──► Serializer
    │
    ▼
Output Data
```

## Design Studio Components

| Component | Purpose |
|---|---|
| **Type Designer** | Create/edit type trees; import XSD, COBOL, EDI |
| **Map Designer** | Author/test/debug map rules; compile maps |
| **Integration Flow Designer (IFD)** | Chain maps into Launcher `.msl` system file |
| **Database Interface Designer (DID)** | Import relational database metadata |

## Typical Development Workflow

```
1. IMPORT/CREATE  → Define type trees for input + output formats
2. ANALYZE        → Tree → Analyze (fix all errors; warnings OK)
3. MAP            → Create map, add cards, author rules
4. TEST           → Run built-in test harness with sample data
5. COMPILE        → Build → Build Project → produces .mmc
6. DEPLOY         → Package .mar; deploy to ACE BAR or Launcher
```

## Map Rules Quick Reference

```
= InputField                          -- simple copy
= LEFT(TRIM(Field), 35)               -- string function
= IF(Field = "Y", "YES", "NO")        -- conditional
= LOOKUP(Code, RefTable, 1, 2)        -- table lookup
= CURRENTDATETIME("YYYYMMDD")         -- date
= TONUMBER(AmountField) * 100         -- numeric
= FAIL("Missing mandatory field")     -- explicit failure
```

**WHEN clause** (component-level iteration filter):
```
WHEN InputRecord.MsgType = "MT103"
```

## Key Built-in Functions

| Category | Functions |
|---|---|
| String | `LEFT`, `RIGHT`, `MID`, `TRIM`, `SUBSTITUTE`, `UPPERCASE`, `FILLRIGHT`, `FILLLEFT`, `PACKAGE`, `SQUEEZE` |
| Numeric | `INT`, `ROUND`, `TRUNCATE`, `MOD`, `ABS`, `SUM`, `COUNT`, `MIN`, `MAX` |
| Date/Time | `CURRENTDATE`, `CURRENTDATETIME`, `DATETOTEXT`, `TEXTTODATE`, `ADDDAYS`, `FROMDATETIME` |
| Conversion | `TONUMBER`, `NUMBERTOTEXT`, `PACK`, `UNPACK`, `BASE64TOTEXT`, `TEXTTOBASE64`, `CONVERT`, `ZONE` |
| Lookup | `LOOKUP`, `DBLOOKUP`, `DBQUERY`, `SEARCHUP`, `INDEX`, `MEMBER`, `EXTRACT` |
| Logical | `IF`, `ALL`, `EITHER`, `NOT`, `ISNUMBER`, `ISALPHA`, `VALID` |
| Error | `FAIL`, `REJECT`, `ISERROR`, `ONERROR`, `LASTERRORCODE`, `LASTERRORMSG` |

## CLI Execution

```bash
# Set environment (Linux)
. /opt/IBM/itx/setup            # sets DTX_HOME_DIR, PATH, LD_LIBRARY_PATH

# Run a compiled map directly
dtxcmdsv -MAP mymap.mmc -IN input.dat -OUT output.xml

# Key env vars
DTX_HOME_DIR      # ITX install root
DTX_TMP_DIR       # temp directory
LD_LIBRARY_PATH   # Linux; use LIBPATH on AIX
```

## ACE Integration Checklist

1. Install ITX runtime co-located with ACE integration server
2. Add WTX/ITX Map Node to message flow
3. Reference `.mmc` or `.mar` — use **external path** (not "Use map from project" in subflows)
4. Set output message domain (`XMLNSC`, `BLOB`, `MRM`)
5. Do NOT override map settings in Toolkit — compile all settings into `.mmc`
6. Deploy in BAR file; verify `dtxwmqi.lil` loads cleanly at broker startup

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| Return code 38 | Toolkit-overridden map settings | Remove overrides; recompile; APAR PI22675 |
| "Failed to load map" | Runtime/compile version mismatch | Align ITX runtime version with compile version |
| Parser error on XML card | XSD sub-element set as card Type | Set card Type to `XSD` (root), not a sub-element |
| 0-byte output file | Default `OnSuccess` behavior | Set `OnSuccess=CreateOnContent` in `dtx.ini` |
| `dtxwmqi.lil` load failure | MQ ICU library mismatch | Run `dtxwmqi_900_64.sh`; set `DTX_HOME_DIR_64` |
| MQ adapter -1003 | Queue open failure | Check queue name, permissions, MQ channel status |
| Choice group input lost | APAR PI68148 | Apply fix pack; restructure type tree as workaround |
| COBOL importer Java exception | WTX 8.4.1.3 importer bug | Use legacy "COBOL Copybook (deprecated)" importer |

## Financial Messaging Notes

- **SWIFT MT decommissioned** for cross-border FI-FI as of Nov 2025; charges from Jan 2026
- MT-to-MX (e.g., MT103 → pacs.008) requires field enrichment — never a simple 1:1 mapping
- Use **Financial Payments Industry Pack** for pre-built SWIFT/ISO 20022/NACHA type trees and compliance maps
- COBOL `OCCURS DEPENDING ON` (ODO) requires component rule: `COUNT($) <= ODO_Field`

## Debugging Checklist

1. Enable trace: Map Designer → Map Properties → Trace Level
2. Check `.mtr` trace file for rule evaluation and data values
3. Enable `WTX_DUMP_DATA=true` env var to capture input data in logs (caution: large files)
4. Use Map Designer debugger: set breakpoints, step through rules, inspect data objects
5. Run `tanalyze.exe mytree.mtt -FAIL -VERBOSE` to validate type tree
6. For ACE: check `dtxwmqi.lil` load in broker log; run `mqsireadlog | mqsiformatlog`

## Reference Files

- `references/core-concepts.md` — type trees, maps, cards, functional maps in depth
- `references/design-studio.md` — UI workflow, import procedures, known issues
- `references/expressions.md` — full function reference, patterns, WHEN clause
- `references/formats.md` — SWIFT MT, ISO 20022, EDIFACT, COBOL, CSV handling
- `references/execution.md` — CLI, Launcher, IFD, dtx.ini tuning, `.mar` deployment
- `references/ace-integration.md` — ACE/IIB node config, CP4I, known issues
- `references/debugging.md` — trace, log subsystems, error reference, type tree analysis
