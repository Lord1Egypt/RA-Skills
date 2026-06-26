# Debugging Reference

## Map-Level Trace

### Enable in Design Studio
`Map → Map Properties → Execution → Trace Level`
- `None` — no trace
- `Standard` — rule evaluation + data values
- `Verbose` — full detail including internal parsing steps

Trace output goes to `.mtr` file in map directory.

### Enable via CLI
```bash
dtxcmdsv -MAP mymap.mmc -IN input.dat -OUT output.xml -TRACE trace.mtr
```

### Enable for Adapter (SPE/MQ)
Append trace flags to adapter arguments:
| Flag | Meaning |
|---|---|
| `-T` | Standard trace |
| `-T+` | Verbose trace |
| `-TE` | Errors only |
| `-TE+` | Verbose errors |
| `-TV` | Values trace |
| `-TV+` | Verbose values |

## Environment Variable Debugging

```bash
# Capture input data passed to the map in wtxlogger output
export WTX_DUMP_DATA=true
# WARNING: produces very large log files in production — use only for diagnosis

# Enable verbose ITX runtime logging
export DTX_TRACE=1
```

## Design Studio Debugger

1. Open map in Map Designer
2. Click in the rule bar for the target field → right-click → **Toggle Breakpoint**
3. Click **Debug** (bug icon) instead of Run
4. Debugger halts at breakpoint
5. **Step Over** (F6): evaluate current rule, advance
6. **Step Into** (F5): enter functional map call
7. **Inspect** panel: view data object values at current point
8. **Trace Tab**: full execution log with rule evaluations

### Map Profiler
`Map → Profile Map` — runs map and produces performance report:
- Time spent per rule
- Identifies bottleneck rules
- Useful for optimizing large financial message transformations

## Type Tree Analysis CLI

```bash
# Full analysis with verbose output
tanalyze.exe mytree.mtt -L -S -SAVE -R failures.dbe -LOG analysis.log -APPEND -FAIL -VERBOSE

# Flags
# -L          List all types
# -S          Structure analysis
# -SAVE       Save analysis results
# -R file     Write failures to .dbe file
# -LOG file   Write log to file
# -APPEND     Append to existing log (don't overwrite)
# -FAIL       Show failures only
# -VERBOSE    Full detail
# -NOLOG      Suppress log output (console only)
```

## Log Subsystems (ITX Advanced / ITXA / Sterling B2Bi)

Configure in `customer_overrides.properties`. **Restart host application after changes.**

| Logger | Use Case | Key Properties |
|---|---|---|
| `wtxlogger` | ITX compliance and transform map issues | `wtxlogger.level=TRACE` |
| `spelogger` | SPE adapter issues | `spelogger.level=DEBUG` |
| `systemlogger` | General system issues | `systemlogger.level=INFO` |
| `txlogger` | Sterling B2Bi map invocations | `txlogger.level=TRACE` |

```properties
# customer_overrides.properties
wtxlogger.level=TRACE
wtxlogger.maxFileSize=20MB
wtxlogger.maxBackupIndex=5
WTX_DUMP_DATA=true
```

## Launcher Log Files

Default log location: `$DTX_HOME_DIR/logs/`

| File | Content |
|---|---|
| `launcher.log` | Launcher startup, map system load, errors |
| `mapname.log` | Per-map execution log |
| `dtx.log` | General ITX runtime log |

Control log rotation in `dtx.ini`:
```ini
CircularLogSize=10485760    # 10MB per file
CircularLogFileNum=5        # keep 5 files
```

## Common Errors — Full Reference

| Error / Code | Cause | Resolution |
|---|---|---|
| **Return code 38** | ACE Toolkit overriding map settings | Remove overrides in Toolkit; compile all settings into `.mmc`; apply APAR PI22675 |
| **Memory Error #33056** | Same as return code 38 | Same fix |
| **"Failed to load map"** | Compile/runtime version mismatch — map compiled on newer ITX | Align ITX runtime version; compiled maps are upward-compatible only |
| **Parser error on XML card** | Input card Type set to sub-element instead of root `XSD` | Change card Type to the top-level `XSD` type |
| **0-byte output file** | `OnSuccess` default creates file regardless of content | Set `OnSuccess=CreateOnContent` in `dtx.ini` |
| **`dtxwmqi.lil` load failure (BIP2872E)** | MQ ICU library version mismatch | Run `dtxwmqi_900_64.sh`; set `DTX_HOME_DIR_64`; restart broker |
| **MQ adapter -1003** | Queue could not be opened | Check queue name, permissions, MQ channel status |
| **MQ adapter -1004** | Message put failure | Check MQ channel status; message size vs. `MaxMsgLength` |
| **MQ adapter -1005** | Message get failure | Check queue authorization; message expiry |
| **Choice group input lost** | APAR PI68148 — XSD Choice group parsing bug | Apply fix pack; workaround: restructure type tree to avoid Choice groups |
| **COBOL importer Java exception** | WTX 8.4.1.3 importer bug | Use `Tree → Import → COBOL Copybook (deprecated)` |
| **"undefined type" in type tree** | ODO field not found, or COBOL importer issue | Check ODO field names; re-import with legacy importer |
| **Map not found in subflow** | IIB 9.x subflow/library path resolution bug | Use external map path; upgrade to IIB 10.0+ |
| **`&apos;` apostrophe escaping** | ITX 10.1.0.1+ behavior change for XMLNSC output | Handle downstream; confirmed behavioral change |
| **Functional map not found** | `.mmc` of functional map not co-located with parent map | Place all `.mmc` files in same directory or update path |
| **Exit code 4** | Warnings only — output was produced | Normal; check trace if unexpected; adjust `-EXITON` threshold |
| **Exit code 8** | Errors — partial output may exist | Check `.mtr` trace for which rule failed; check input data |
| **Exit code 16** | Fatal — no output produced | Critical input card failure; check adapter, file existence, permissions |

## Debugging Checklist

### Map Produces Wrong Output
1. Enable trace; inspect `.mtr` for rule evaluation sequence
2. Check WHEN clauses — is a component being skipped?
3. Verify input card Type selection (XSD sub-element vs root)
4. Add `FAIL` or `REJECT` temporarily to catch unexpected values
5. Use `LASTERRORMSG()` in a catch-all output field to surface hidden errors

### Map Crashes / Returns Code 8+
1. Check `.mtr` for last rule evaluated before failure
2. Verify input data matches expected type tree structure
3. Check for null/empty fields that functions don't handle (use `ONERROR` or `IF(VALID(...))`)
4. Check COBOL ODO component rule — count field must precede repeating field in data

### ACE Integration Issues
1. Check broker system log for `dtxwmqi.lil` load status
2. Verify `DTX_HOME_DIR` set in broker service environment
3. Use external map path (not "Use map from project")
4. Remove any map settings overrides from ACE Toolkit properties
5. Confirm `.mmc` compiled for Linux (not Windows) if deploying to Linux ACE

### Type Tree Issues
1. Run `tanalyze` CLI — fix all errors before using in maps
2. Re-analyze after every XSD update
3. Check namespace URI in card properties matches message namespaces exactly
4. For COBOL: verify byte order and code page settings match source system
