# statdata-transfer / Statistical Data Format Converter

[🇨🇳 Chinese](./README_zh-CN.md)

<div align="center">
<img src="assets/icon.svg" width="240" height="240" />
</div>

---

> Read 50+ statistical-software and clinical-trial data formats, and **inter-convert between most of them** while keeping variable/value labels and missing-value metadata. No statistical software required — format conversion only.

## How to use it in a conversation

Just talk to the agent in natural language. A few real examples (copy-paste ready):

**① Most common — convert a file**
- **You say**: `convert C:/Users/Name/Desktop/data.sav to .dta`
- **Agent replies** (sketch): reads `data.sav` with pyreadstat, preserves all variable/value labels, and writes `data.dta` in the same folder.
- **Trigger the real conversion**: by default the agent previews the plan; say `please write the file` to execute.

**② Show what's inside**
- **You say**: `read data.sav and show metadata`
- **Agent replies**: prints the DataFrame shape, variable labels, value labels, and a list of which metadata will be preserved.

**③ Check before you lose data**
- **You say**: `will converting .sav to .xlsx lose any metadata?`
- **Agent replies**: warns that Excel keeps labels only in a side sheet; suggests Parquet/Stata to keep them losslessly.

**④ Ask for reproducible code**
- **You say**: `show me the Python code to convert .sav to .parquet`
- **Agent replies**: prints the `read_stat_file` / `write_stat_file` snippet (code is always English).

**⑤ Switch language**
- **You say**: `reply in Chinese` / `switch to English` — all user-facing messages follow your OS language or this prompt.

## What can it do? (scenario index)

| Capability | Typical use | Try saying |
|:---|:---|:---|
| **Read 50+ formats** | Open SPSS/Stata/SAS/R/Excel/Parquet/HDF5/JSON… into pandas | `read data.sav and show metadata` |
| **Convert between stats formats** | SPSS ↔ Stata ↔ R ↔ SAS XPT, keeping all labels | `convert data.sav to .dta keeping variable labels` |
| **Export universal formats** | Parquet / Feather / HDF5 / JSON / CSV / Excel with labels embedded | `save to parquet but keep value labels` |
| **Metadata-safe round-trip** | Labels survive a convert-and-convert-back | `convert to parquet then back to sav, keep labels` |
| **Metadata-loss warning** | Know what will be dropped before exporting | `will .sav to .xlsx lose metadata?` |
| **Batch / folder** | Convert a whole folder or a zip archive | `convert all .dta in this zip to .sav` |

Full format list and per-format limits: see **Advanced reference** below.

## First-use FAQ

- **Do I need SPSS/Stata/R installed?** No. The skill is pure Python; it only *optionally* calls a local R interpreter for a few formats (Minitab/EpiData/R write), and only when you pass `allow_r_exec=True`.
- **How do I get the actual converted file, not just code?** Say `please write the file`. By default it previews; execution is explicit.
- **Will my labels survive?** For binary stats formats (SPSS/Stata/SAS/R) — yes, fully. For text/JSON — only a retainable subset. The skill always tells you what is preserved vs lost.
- **Can I get reproducible code?** Yes — ask `show me the Python code` and it prints the `read_stat_file` / `write_stat_file` calls.
- **Is the output in Chinese on a Chinese system?** User-facing messages auto-switch to Chinese on a `zh-*` OS, or you can force it with `reply in Chinese`. Code stays English.
- **My data file is huge / can't be uploaded directly?** Use the absolute file path in your prompt, or compress it into a `.zip` and upload the zip.

## Safety (in plain words)

The skill runs **locally** and follows a **safe-preview** model: it shows what it will read/convert and only writes a file when you explicitly ask. Every path that would call the local R interpreter is **opt-in and off by default** — it runs only when you pass `allow_r_exec=True` on a file you trust. Your data is never sent over the network unless you explicitly request a package install. Treat the output as reference and validate before regulatory submissions.

---

## Advanced reference

> The following is developer/reference material, kept out of the quick-start above.

### Supported Formats & Capability Matrix

*Sorted alphabetically.*

| Format | Extension | Dependency | Var Label | Val Label | Special Missing | Formula | Meta Preserve |
|--------|-----------|------------|-----------|-----------|-----------------|---------|---------------|
| CDISC ODM | `.odm` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Clinical data only |
| dBASE / FoxPro | `.dbf` | dbfread / dbf | ✗ | ✗ | ✗ | ✗ | ⚠️ Read+Write; uppercase names |
| EpiData | `.rec` | R foreign | ✗ | ✗ | ✗ | ✗ | ⚠️ Via R |
| EpiInfo | `.prj` `.xml` | xml/etree | ✅ | ✅(codes) | ✗ | ✗ | ✅ XML structure |
| Excel | `.xlsx` `.xls` `.xlsm` | openpyxl / xlrd | ✗ | ✗ | ✗ | ⚠️ result only | ⚠️ Extra sheet for labels; merged-cell fill |
| EViews | `.wf1` `.wf2` | built-in | ✗ | ✗ | ✗ | ✗ | ⚠️ JSON structure |
| Feather | `.feather` `.arrow` | pyarrow | ✅(schema) | ✅(schema) | ✗ | ✗ | ⚠️ Version diff |
| FST | `.fst` | — | ✗ | ✗ | ✗ | ✗ | ✗ Detect-only (proprietary format) |
| GraphPad Prism | `.pzfx` `.pz` | pzfx | ✗ | ✗ | ✗ | ✗ | ⚠️ Multi-table |
| Gretl | `.gdt` `.gdtb` | built-in | ✅ | ✅(tables) | ✗ | ✗ | ✅ string-tables |
| HDF5 | `.h5` `.hdf5` | h5py | ✗ | ✗ | ✗ | ✗ | ⚠️ Hierarchy + attribute labels |
| HTML | `.html` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Tables only |
| jamovi | `.omv` | ZIP built-in | ✅ | ✅ | ✗ | ✗ | ✅ JSON analysis |
| JMP | `.jmp` | jmpio-python | ⚠️ | ⚠️ | ✗ | ✗ | ⚠️ Multi-table |
| JSON | `.json` | built-in | ✅ | ✅ | ✗ | ✗ | ✅ stat-full-meta on write |
| MATLAB | `.mat` | scipy | ✗ | ✗ | ✗ | ✗ | ⚠️ v7.3+ via h5py fallback |
| Mathematica | `.wdx` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Best-effort XML |
| Minitab | `.mtw` `.mpj` | mtbpy / R | ✗ | ✗ | ✗ | ✗ | ⚠️ Via R |
| MS Access | `.mdb` `.accdb` | pyodbc + Access Driver | ✗ | ✗ | ✗ | ✗ | ⚠️ Multi-table; needs system driver |
| ODS | `.ods` | odfpy | ✗ | ✗ | ✗ | ✗ | ⚠️ Data only |
| ORC | `.orc` | pyarrow | ✅(schema) | ✅(schema) | ✗ | ✗ | ⚠️ Version diff |
| Origin | `.opju` `.oggu` | zipfile + lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Best-effort |
| Parquet | `.parquet` | pyarrow | ✅(schema) | ✅(schema) | ✗ | ✗ | ⚠️ Nested types; partitioned datasets |
| R | `.rda` `.rds` `.rdata` | pyreadr + R | ✅ | ✅ | ✅ | ✗ | ✅ statdata_meta + R bridge |
| SAS | `.sas7bdat` `.xpt` `.sas7bcat` | pyreadstat | ✅ | ✅(need catalog) | ⚠️ | ✗ | ✅ |
| SPSS | `.sav` `.zsav` `.por` | pyreadstat | ✅ | ✅ | ✅ | ✗ | ✅ |
| Stata | `.dta` | pyreadstat | ✅ | ✅ | ⚠️ | ✗ | ✅ |
| Weka ARFF | `.arff` | built-in | ✅ | ✅(nominal) | ✗ | ✗ | ✅ nominal mapping |
| XML | `.xml` | lxml | ✗ | ✗ | ✗ | ✗ | ⚠️ Structure preserved |

> ✅=Full preservation · ⚠️=Partial/conditional · ✗=Not preserved

### Detect-Only Formats

Formats with no parser available. The skill detects the extension and provides clear export guidance (no data parsing).

| Format | Extension | Guidance |
|--------|-----------|----------|
| FST (R fst package) | `.fst` | R: `fst::read_fst("in.fst", "out.csv")` then read CSV |
| LIMDEP / NLOGIT | `.lpw` | Export to CSV from original software |
| NCSS | `.ncss` | Export to CSV |
| OxMetrics | `.in7` | Export to CSV / `.dta` |
| Paradox | `.db` `.px` | Export to `.dbf` / CSV |
| SAS CPORT | `.cpt` | SAS: `proc export` to XPORT(`.xpt`) / `.sas7bdat` |
| Statistica | `.sta` | Export to `.sav` / `.csv` |
| SYSTAT | `.sys` `.syd` | Export to CSV / `.sav` |

### Return Structure

```python
{
    "dataframe": pd.DataFrame,
    "metadata": {
        "file_format": "spss_sav",
        "row_count": 100, "column_count": 10,
        "variable_labels": {"q1": "Question 1"},
        "value_labels": {"q1": {1: "Yes", 2: "No"}},
    },
    "warnings": [],
    "column_report": {"q1": {"source_type": "int", "pandas_dtype": "int64"}},
}
```

### Metadata Preservation Tiers

1. **Statistical binary formats** (SPSS/Stata/SAS/R): 100% metadata preserved
2. **Arrow ecosystem** (Parquet/Feather/ORC): only restores labels from `write_stat_file`
3. **Non-stats formats** (CSV/Excel/XML/HTML/ODS): data only; use `apply_value_labels()` to attach manually
4. **R formats**: embeds all metadata via `statdata_meta` attribute

### Recommended Read Strategies

| Use Case | Recommendation |
|----------|---------------|
| Data warehousing / ETL | SPSS `.sav` or Stata `.dta` → Parquet / HDF5 |
| Scientific computing | `.mat` or `.hdf5` → NumPy / pandas |
| Statistical analysis (Python) | `.sav` / `.dta` → pandas → scipy.stats |
| Report output | pandas → JSON / HTML / Excel |
| Cross-software sharing | Stata ↔ SPSS ↔ R direct interconversion |

### File Size Limits

| Format | Memory Behavior |
|--------|----------------|
| pyreadstat (SPSS/Stata/SAS) | Loads entire file into RAM |
| HDF5 | Chunked reading; not limited by RAM |
| Parquet | pyarrow memory-mapped (mmap); handles files >RAM |

### Encoding Notes

- **Chinese files**: old Stata/SAS may use GBK/gb2312. Use `encoding='gbk'`.
- **European files**: some SAS files use Latin-1. Try `encoding='latin1'` if UTF-8 fails.
- **Auto-detection**: `_auto_detect_encoding` is enabled by default for SPSS/Stata/SAS.

### Providing Input Files

AI agents can only directly upload a limited set of file types. When your data file cannot be uploaded directly:

1. **Use the absolute file path** in your prompt (e.g. `convert C:/Users/Name/Desktop/data.sav to .dta`)
2. **Compress the file as a `.zip` archive** and upload the zip instead

The skill automatically extracts and processes zip archives containing a single data file.

### CLI (advanced)

```bash
# Check environment (optional install on request)
python scripts/check_env.py --install
```

Complete code examples: [`references/usage_examples.py`](./references/usage_examples.py)

### Extending

To add a new format: edit `scripts/reader_*.py` to add a reader function, register it in `format_map` in `scripts/reader_core.py`, and add a TypedDict in `scripts/reader_core.py`.

### Format Limitations

*Alphabetically ordered. ✅ = fixed, 🔄 = new capability; rest are inherent format limits.*

- **CDISC ODM (.odm)**: ❌ XML structure dependency; ❌ no statistical metadata in ODM spec, only clinical structure preserved
- **dBASE / FoxPro (.dbf)**: ❌ field names forced to uppercase; ✅ Read + Write supported
- **EpiData (.rec)**: ❌ requires R + `foreign` package; ❌ statistical metadata lost in R-to-CSV bridge
- **EpiInfo (.prj)**: ❌ project file contains no data, auto-associates same-name CSV; ❌ Access not supported, export to CSV first; ✅ variable labels/codes reconstructed in XML
- **Excel (.xlsx/.xls/.xlsm)**: ✅ merged cells filled with anchor value (`fill_merged_cells=True`, default); ❌ formulas lost; ❌ charts/shapes not extracted; labels in separate metadata worksheet on write
- **HDF5 (.h5/.hdf5)**: ✅ multi-dataset fallback via h5py; ✅ attribute labels scanned; ❌ hierarchy flattened
- **JMP (.jmp)**: ❌ requires `jmpio-python`; ❌ multi-table returns first only; write single-table only
- **MATLAB (.mat)**: ✅ v7.3+ (HDF5) via h5py; ❌ complex structures flattened; ❌ object/datetime lose fidelity
- **Parquet (.parquet)**: ❌ deeply nested types (>2 levels) opaque; ✅ partitioned datasets via `pyarrow.dataset`
- **R (.rda/.rds/.rdata)**: ✅ ASCII XDR read via R bridge needs `allow_r_exec=True`; ❌ factor order may not be Categorical unless embedded; write via `statdata_meta`
- **SAS (.sas7bdat/.xpt/.sas7bcat)**: ✅ value labels need co-located `.sas7bcat`; ❌ Viya CAS `.sashdat` not supported; date origin 1960-01-01
- **SPSS (.sav/.zsav/.por)**: ❌ MR Sets as raw dict; ❌ formulas lost; ⚠️ special missing (`.A`–`.Z`) flagged in `special_missing`; `.zsav` needs pyreadstat 1.2+, else fallback to `.sav`
- **Stata (.dta)**: ⚠️ special missing (`.a`–`.z`) preserved when `user_missing=True` (default), NaN when `False` (irreversible); ✅ pre-v13 Latin-1 auto-detected; ❌ Stata 117–119 not supported, auto-downgrade to v15 on write

### Security

- **R execution is opt-in and sandboxed by default.** Reading `.rda/.rds/.RData`, Minitab `.mtw/.mpj`, EpiData `.rec`, and writing R formats is disabled by default; runs only with `allow_r_exec=True` on a trusted file. Pure-Python parsers tried first.
- **No silent R fallback.** On pure-Python failure without `allow_r_exec`, raises a clear error instead of launching R.
- **R scripts are static templates.** User input passes only as CLI args — never concatenated into executable R code.
- **Temp CSV exposure (R bridge).** Opt-in R writes a temp CSV; deleted after use but could briefly persist on crash. Avoid highly sensitive data through R-backed formats.
- **No destructive writes.** Existing `.hyper` is rotated to `.bak` before overwrite; original untouched on failure.
- **Pinned dependencies.** Core deps carry upper-bound pins — see `requirements.txt`.

## Contact the author

For feature requests, bug reports, or other feedback, please contact the author directly at medstatstar@gmail.com (Wintone Zhang).

## License

MIT License. See [LICENSE](LICENSE) for details.
