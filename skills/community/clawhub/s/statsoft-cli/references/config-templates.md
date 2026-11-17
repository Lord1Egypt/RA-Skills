# Configuration & Memory Templates

## SPSS Statistics Memory Template

```markdown
### SPSS Statistics Environment

- **Version**: IBM SPSS Statistics [26/27/28/29/30/31]
- **Main Executable**: `C:\Program Files\IBM\SPSS\Statistics\[version]\stats.exe`
- **Invocation Priority**:
  1. **Approach 1 (preferred)**: `stats.com` console version + `.spj` file → completely splash-free, **foolproof**
     ```bash
     "C:\Program Files\IBM\SPSS\Statistics\[version]\stats.com" -production silent -nologo "job.spj"
     ```
  2. **Approach 2 (fallback)**: internal Python driver `spss.Submit()` → splash-free, **but can only run pure analysis syntax**
     - ❌ Must not contain `OUTPUT SAVE`, `OUTPUT EXPORT`, `HOST COMMAND`, `XDATA`, etc.
  3. **Approach 3 (last resort)**: `stats.exe` GUI version + `.spj` → may show a splash screen
     ```bash
     "C:\Program Files\IBM\SPSS\Statistics\[version]\stats.exe" -production silent -nologo "job.spj"
     ```
- **Built-in Python path**: `C:\Program Files\IBM\SPSS\Statistics\[version]\Python3\python.exe`
- **.spj file XML structure template**:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       print="false" syntaxErrorHandling="continue"
       syntaxFormat="interactive" unicode="true">
    <!-- locale auto-detect: in Chinese environments inject country="CN" language="zh" automatically; in other environments omit this element so SPSS inherits the system locale (avoids hardcoding locale that changes parsing/encoding/reproducibility, SQP-3) -->
    <output outputFormat="viewer" outputPath="output.spv"/>
    <syntax syntaxPath="syntax.sps"/>
  </job>
  ```
```

## SPSS Statistics Version Differences

### Python Version Comparison

| SPSS Statistics Version | Bundled Python | f-string Support |
|-------------------------|---------------|-----------------|
| 26 | Python 3.4 | ❌ |
| 27 | Python 3.8 | ✅ |
| 28 | Python 3.9 | ✅ |
| 29 | Python 3.10.4 | ✅ |
| 30 | Python 3.10 | ✅ |

### spss_helper.py Compatibility

- SPSS Statistics 26: Script uses `%s` / `.format()`, no f-string
- SPSS Statistics 27+: Script can use f-string and modern Python

## SPSS Modeler Memory Template

```markdown
### SPSS Modeler Environment

- **Version**: IBM SPSS Modeler [18.0/18.1/18.2/18.3/18.4/18.5/18.6]
- **Main Executable**: `C:\Program Files\IBM\SPSS\Modeler\[version]\bin\clemb.exe`
- **modelerclient.exe**: `C:\Program Files\IBM\SPSS\Modeler\[version]\bin\modelerclient.exe`
- **Batch Mode command format**:
  ```powershell
  # Run stream file
  clemb.exe -local -stream "job.str" -log "output.log" -execute

  # Run Python script (recommended)
  clemb.exe -local -script "train_model.py" -scriptlang python -log "train.log" -execute
  ```
- **Config Field**: `config.json > "SPSS Modeler"`
- **Difference from Statistics**: Statistics is a statistical analysis tool, Modeler is a data mining/modeling tool
```

## SPSSModeler Version Differences

| Version | clemb.exe Path | Notes |
|---------|---------------|-------|
| 18.6 | `C:\Program Files\IBM\SPSS\Modeler\18.6\bin\clemb.exe` | Latest, Python scripting |
| 18.5 | `C:\Program Files\IBM\SPSS\Modeler\18.5\bin\clemb.exe` | Performance improvements |
| 18.0 | `C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe` | Classic stable |

## Stata Memory Template

```markdown
### Stata Environment

- **Version**: Stata [VERSION] [EDITION] (MP/SE/BE)
- **Main Executable Path**: `[STATA_EXE_PATH]` (e.g., `StataMP-64.exe`)
- **Batch Command Format**:
  ```bash
  # Windows — new MP/SE (Stata 14+)
  "[STATA_EXE_PATH]" /b do "script.do"
  # Windows — old SE (e.g., Stata 12 SE) use /e to avoid popup
  "[STATA_EXE_PATH]" /e do "script.do"
  ```
```

## Stata Version Differences

| Edition | License Match | Notes |
|---------|--------------|-------|
| MP (Multiprocessing) | ✅ Multi-core | Best for large data |
| SE (Special Edition) | ✅ Single-core | Mid-size data |
| BE (Basic Edition) | ✅ Limited | No parallelism |

## R Memory Template

```markdown
### R Environment

- **Version**: R [VERSION]
- **Rscript Path**: `[RSCRIPT_EXE_PATH]`
- **Batch Command Format**:
  ```bash
  Rscript --vanilla "script.R"
  ```
```

## SAS Memory Template

```markdown
### SAS Environment

- **Version**: SAS [VERSION] (e.g., 9.4)
- **Executable Path**: `[SAS_EXE_PATH]`
```

## Minitab Memory Template

```markdown
### Minitab Environment

- **Version**: Minitab [22/21/20/19/18]
- **Main Executable**: `C:\Program Files\Minitab\Minitab [VERSION]\mtb.exe`
- **Automation**: ❌ **GUI-only** — `mtb.exe /run "script.mtb"` opens the Minitab GUI window and is not headless-safe; never call it from the agent. Detect the install and let the user run analyses interactively (or via Minitab Web App).
- **Config Field**: `config.json > "Minitab"`
- **macOS / Linux**: No native CLI; use Minitab Web App (https://app.minitab.com/) or remote desktop to a Windows host
```

## R — Alternative when R is not available

| R Package | Anaconda Python Alternative |
|-----------|---------------------------|
| dplyr / tidyr | pandas |
| ggplot2 | matplotlib / seaborn |
| caret / xgboost | scikit-learn |
| survival | lifelines |
| lme4 / nlme | statsmodels |

## Configuration File (config.json)

```json
{
  "platform": "windows",
  "R": { "installed": true, "path": "C:\\Program Files\\R\\R-4.5.1\\bin\\Rscript.exe", "version": "4.5.1", "mode": "simple" },
  "Stata": { "installed": true, "path": "C:\\Program Files\\Stata17\\StataMP-64.exe", "edition": "MP", "version": "17", "mode": "simple" },
  "SAS": { "installed": true, "path": "C:\\Program Files\\SASFoundation\\9.4\\sas.exe", "version": "9.4", "mode": "simple" },
  "SPSS": { "installed": true, "version": "28", "path": "C:\\Program Files\\IBM\\SPSS\\Statistics\\28\\stats.exe", "mode": "simple" }
}
```

## Common Errors & Solutions

| Software | Error | Cause | Solution |
|----------|-------|-------|----------|
| SPSS | NullPointerException | .spj missing `<output>` | Add complete XML |
| SPSS | UnicodeDecodeError | Non-UTF-8 output | Use `cp1252` or `errors='replace'` |
| SPSS | K=1 result | High variable dimensionality | Reduce noise variables |
| SPSS | F-string error | Python 3.4 limitation | Use `%s` formatting |
| Stata | Confirmation dialog | Wrong batch flag | Stata ≤12: `/e` (Win) or `-e` (Mac/Linux); Stata ≥13: `/b` (Win) or `-b` (Mac/Linux) |
| Stata | File not found | Spaces in path | Wrap path in quotes |
| R | Package not found | Package not installed | `install.packages()` |
| R | Encoding issue | Non-UTF-8 file | Use `fileEncoding="UTF-8"` |
| SAS | License expired | Expired license | Update license file |
| SAS | Encoding issue | Encoding mismatch | `options encoding='utf-8';` |

## Completion Prompt Templates

### SPSS (preferred success)

```
✅ SPSS [version] configuration complete!

📋 Configuration:
  - Version: IBM SPSS Statistics [version]
  - Path: [install_path]
  - Bundled Python: [python_path] (Python [ver])
  - f-string: [✅/❌]

✅ Internal Python test passed (no splash screen).
```

### Stata

```
✅ Stata [version] configuration complete!

⚠️ Notes:
  1. New MP/SE (14+) use `/b`; old SE (e.g., Stata 12) must use `/e`
  2. Wrap paths with spaces in quotes
  3. License match: MP→StataMP-64.exe / SE→StataSE-64.exe / BE→Stata-64.exe

📋 Invocation:
  "StataMP-64.exe" /b do "script.do"
```

### R

```
✅ R [version] configuration complete!

⚠️ Notes:
  1. Use Rscript --vanilla, not GUI
  2. Use fileEncoding="UTF-8" for Chinese encoding
  3. Use data.table/arrow for large memory data

📋 Invocation:
  "[Rpath]\Rscript.exe" --vanilla "script.R"
```

### SAS

```
✅ SAS [version] configuration complete!

⚠️ Notes:
  1. Batch mode generates .log and .lst files
  2. Use options encoding='utf-8'; for Chinese
  3. Ensure license is not expired

📋 Invocation:
  sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

## Platform-Specific Paths

### R
- Windows: `C:\Program Files\R\`
- Mac: `/Library/Frameworks/R.framework/`
- Linux: `/usr/lib/R/`

### Stata
- Windows: `C:\Program Files\Stata17\`; `C:\Program Files\Stata18\`
- Mac: `/Applications/Stata/`
- Linux: `/usr/local/stata/`

### SPSS (Windows only)
`C:\Program Files\IBM\SPSS\Statistics\26\` → `31`

### JMP (Windows only)
`C:\Program Files\JMP\16\`; `\17\`

### GraphPad (Windows only)
`C:\Program Files\GraphPad\Prism 9\`; `\10\`

## Advanced Mode Scripts

| Software | Windows Command |
|----------|-----------------|
| R | `statsoft-r run script.R` |
| SAS | `statsoft-sas run program.sas` |
| SPSS | `statsoft-spss run syntax.sps` |
| SPSS (batch) | `statsoft-spss run-batch s1.sps s2.sps s3.sps` |
| JMP (Windows, CLI) | `statsoft-jmp run script.jsl` — only executes user-provided JSL scripts, requires explicit user confirmation |
