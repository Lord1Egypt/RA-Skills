---
slug: statdata-transfer
name: statdata-transfer
displayName: 统计数据格式转换器 / Statistical Data Format Converter
cn_name: 统计数据格式转换器
version: 2.2.1
summary: 读入/转存 50+ 统计软件格式，对统计二进制格式完整保留变量标签/值标签/特殊缺失值等元数据。副作用声明（完整）：运行环境检查（scripts/check_env.py）；可应要求 pip 安装缺失包；写入主输出文件的同时，可能生成 sidecar 元数据文件（CSV/TSV 旁生成 <名>_metadata.json，Parquet/Arrow 内嵌元数据）及覆盖 .hyper 时的 .bak/.bak.1 备份；处理 .rda/.rds/.RData/.mtw/.mpj/.rec 文件时可调用本地 R 解释器，但该回退默认禁用，需 allow_r_exec=True 显式开启。
license: MIT
description: "读入/转存 50+ 统计软件格式，对统计二进制格式完整保留变量标签/值标签/特殊缺失值等元数据。副作用声明（完整）：运行环境检查（scripts/check_env.py）；可应要求 pip 安装缺失包；写入主输出文件的同时可能生成 sidecar 元数据（CSV/TSV 旁 <名>_metadata.json、Parquet/Arrow 内嵌）及覆盖 .hyper 时的 .bak/.bak.1 备份；处理 .rda/.rds/.RData/.mtw/.mpj/.rec 时可调用本地 R 解释器，但该回退默认禁用，需 allow_r_exec=True 显式开启。 / Read/convert 50+ statistical software formats, preserving variable/value labels and missing-value metadata for binary stats formats. FULL side effects: runs environment checks (scripts/check_env.py); may optionally pip-install missing packages on request; writes the main output file AND may emit sidecar metadata (e.g. <name>_metadata.json beside CSV/TSV, embedded in Parquet/Arrow schema) and .bak/.bak.1 backups when overwriting .hyper; can invoke the local R interpreter for .rda/.rds/.RData/.mtw/.mpj/.rec files via a fallback DISABLED by default and opted in only with allow_r_exec=True."
triggers:
  - "statdata-transfer"
  - "统计数据格式转换"
  - "spss stata sas 格式"
  - ".sav .dta .sas7bdat 读入"
  - "sav转dta 格式转换"
  - "variable labels 变量标签"
  - "metadata-preserved conversion"
required_commands: [python]
invocable: true
metadata:
  openclaw: { emoji: "🛠️", icon: "assets/logo.svg" }
  authors: ["medstatstar", "phoe-zip"]
  license: "MIT"
  tags: ["data-conversion", "statistics", "spss", "stata", "sas", "clinical-trials", "metadata", "pandas", "bidirectional"]
  homepage: "https://github.com/medstatstar/statdata-transfer"
permissions:
  scope: "user-space-only"
  network: "off"
  network_note: "Offline by default; the only network touchpoint is the optional `python scripts/check_env.py --install`, which pip-installs missing packages and runs ONLY on explicit user request."
  filesystem: "read-only to its own files; reads the input data file you specify; writes the converted output file to a path you specify, and may additionally create sidecar metadata files (e.g. <name>_metadata.json beside CSV/TSV, or metadata embedded in Parquet/Arrow schema) and .bak/.bak.1 backups when overwriting .hyper"
  data: "no external data transmission"
---

# Statistical Data Format Converter

> **Safe by default — preview, not execute**: the skill shows what it will read/convert and only writes a file when you explicitly ask. Every R-invoking path is opt-in and disabled by default.

## Language

- **English guide** → [README.md](https://github.com/medstatstar/statdata-transfer/blob/main/README.md)
- **中文指南** → [README_zh-CN.md](https://github.com/medstatstar/statdata-transfer/blob/main/README_zh-CN.md)

This skill responds in the user's input language and auto-switches; runtime prompts switch by locale. SKILL.md body is English-only (agent-facing); bilingual walkthroughs live in the two READMEs.

## Purpose

Read 50+ statistical-software and clinical-trial data formats into a pandas DataFrame, and inter-convert between most formats (SPSS ↔ Stata ↔ R ↔ SAS XPT ↔ Excel ↔ Parquet ↔ HDF5 ↔ JSON …). For statistical binary formats it preserves full variable/value labels and special-missing-value metadata; text/JSON formats preserve only a retainable subset.

## Features

| Capability | Description | Typical Scenario |
|:---|:---|:---|
| **Read** | Extract data + all metadata from 50+ formats into a pandas DataFrame; clearly report what is preserved vs lost | `read data.sav and show metadata` |
| **Convert** | Inter-convert most stats formats; export to universal formats (Parquet/Feather/HDF5/JSON/CSV/Excel) with labels embedded | `convert data.sav to .dta keeping variable labels` |
| **Embed metadata** | Labels embedded in Arrow `schema.metadata` / sidecar JSON for lossless round-trips | `save to parquet but keep value labels` |
| **Warn** | Auto-detect and report metadata loss per conversion path | audit before exporting to CSV |

## Supported Formats

*50+ formats, sorted alphabetically.*

| Format | Extension | Meta Preserve |
|--------|-----------|---------------|
| CDISC ODM | `.odm` | ⚠️ Clinical data only |
| dBASE / FoxPro | `.dbf` | ⚠️ Read+Write, uppercase names |
| EpiData | `.rec` | ⚠️ Via R (opt-in) |
| EpiInfo | `.prj` `.xml` | ✅ XML structure |
| Excel | `.xlsx` `.xls` `.xlsm` | ⚠️ Extra sheet for labels; merged-cell fill |
| EViews | `.wf1` `.wf2` | ⚠️ JSON structure |
| Feather | `.feather` `.arrow` | ✅ Via schema |
| FST | `.fst` | ✗ Detect-only (proprietary) |
| GraphPad Prism | `.pzfx` `.pz` | ⚠️ Multi-table |
| Gretl | `.gdt` `.gdtb` | ✅ String-tables |
| HDF5 | `.h5` `.hdf5` | ⚠️ Hierarchy + attribute labels |
| HTML | `.html` | ⚠️ Tables only |
| jamovi | `.omv` | ✅ JSON analysis |
| JMP | `.jmp` | ⚠️ Multi-table |
| JSON | `.json` | ✅ stat-full-meta |
| MATLAB | `.mat` | ⚠️ v7.3+ via h5py fallback |
| Mathematica | `.wdx` | ⚠️ Best-effort XML |
| Minitab | `.mtw` `.mpj` | ⚠️ Via R (opt-in) |
| MS Access | `.mdb` `.accdb` | ⚠️ Multi-table; needs system driver |
| ODS | `.ods` | ⚠️ Data only |
| ORC | `.orc` | ✅ Via schema |
| Origin | `.opju` `.oggu` | ⚠️ Best-effort |
| Parquet | `.parquet` | ✅ Via schema; partitioned datasets |
| R | `.rda` `.rds` `.rdata` | ✅ pyreadr; R fallback opt-in (allow_r_exec) |
| SAS | `.sas7bdat` `.xpt` `.sas7bcat` | ✅ |
| SPSS | `.sav` `.zsav` `.por` | ✅ |
| Stata | `.dta` | ✅ |
| Weka ARFF | `.arff` | ✅ Nominal mapping |
| XML | `.xml` | ⚠️ Structure preserved |

> ✅=Full · ⚠️=Partial/conditional · ✗=Not preserved
>
> 12 detect-only formats (SAS CPORT `.cpt`, Statistica `.sta`, OxMetrics `.in7`, SYSTAT `.sys`/`.syd`, Paradox `.db`/`.px`, LIMDEP `.lpw`, NCSS `.ncss`, FST) give clear export guidance — see README.

## Return Structure

```python
{
    "dataframe": pd.DataFrame,
    "metadata": {
        "file_format": "spss_sav",
        "row_count": 100, "column_count": 10,
        "variable_labels": {"q1": "Question 1"},
        "value_labels": {"q1": {1: "Yes", 2: "No"}},
        "special_missing": {...},
    },
    "warnings": [],
    "column_report": {"q1": {"source_type": "int", "pandas_dtype": "int64"}},
}
```

## Quick Start

```bash
# Check environment (optional install on request)
python scripts/check_env.py --install
```

In WorkBuddy (bilingual, auto-detects your language):

```
> convert data.sav to .dta
> read data.sav and show metadata
> 把 data.sav 转成 .dta 并保留变量标签
```

> For complete code examples, see `references/usage_examples.py`.

## Dependencies

```yaml
requires:
  bins: [python3]
  packages:
    core: [pyreadstat>=1.3.5,<2, pyreadr>=0.4,<0.5, pandas>=2.0,<3]
    extended: [openpyxl, xlrd, scipy, h5py, pyarrow, lxml, odfpy, tableauhyperapi, dbfread, dbf, pyodbc]
```

> Full list: `requirements.txt`

## ⚠️ Safety

- All R-invoking paths are **opt-in and disabled by default**; they only run when you pass `allow_r_exec=True` on a trusted file.
- Pure-Python parsers (`pyreadr`, `mtbpy`) are tried first and never execute code.
- No silent R fallback — if the pure-Python parser fails and `allow_r_exec` is not set, the skill raises a clear error.
- Writing an existing `.hyper` backs up to `.bak` before overwrite; on failure the original is untouched.
- Output for reference only; validate before regulatory submissions.

### Security model (transparent disclosure)

| Behavior | Description |
|:---|:---|
| **R invocation (opt-in)** | Reading `.rda/.rds/.RData` (`readRDS()/load()`), Minitab `.mtw/.mpj`, EpiData `.rec`, and writing R formats run **only** with `allow_r_exec=True` on a trusted file. Pure-Python parsers tried first. |
| **No silent fallback** | On pure-Python parser failure without `allow_r_exec`, raises a clear error instead of launching R — avoids executing embedded code from untrusted files. |
| **Static R templates** | When the opt-in R path runs, all R scripts are static templates; user input passes only as CLI args (`commandArgs(trailingOnly=TRUE)` via `jsonlite`) — never concatenated into executable R code. |
| **Temp CSV bridge** | Opt-in R writes data to a temp CSV then reads back; deleted after use, but on crash could briefly persist — avoid highly sensitive data through R-backed formats. |
| **No destructive writes** | `.hyper` write → temp file → rotate existing to `.bak` (prior `.bak` → `.bak.1`, never silently deleted) → atomic swap. Original untouched on failure. |
| **Sidecar metadata files** | Writing CSV/TSV also emits `<name>_metadata.json` (full 17-field metadata) next to the data file; Parquet/Arrow embed metadata inside the file schema. No writes occur outside the output path you specify. |
| **Pinned dependencies** | Core deps carry upper-bound pins (`pandas`, `pyreadstat`, `pyreadr`) — see `requirements.txt`. |
| **Optional install** | `python scripts/check_env.py --install` only on explicit request. |
| **Permissions** | Read the input file; write the output file to a path you specify. No network unless you explicitly request package install. |

## License

MIT. See [LICENSE](./LICENSE).
