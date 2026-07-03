# Configuration & Memory Templates

## SPSS Statistics Memory Template

```markdown
### SPSS Statistics 环境配置 / SPSS Statistics Environment

- **版本 / Version**：IBM SPSS Statistics [26/27/28/29/30/31]
- **主程序 / Main Executable**：`C:\Program Files\IBM\SPSS\Statistics\[版本]\stats.exe`
- **调用优先级 / Invocation Priority**：
  1. **方案 1（首选）**：`stats.com` 控制台版 + `.spj` 文件 → 完全无闪屏，**万无一失**
     ```bash
     "C:\Program Files\IBM\SPSS\Statistics\[版本]\stats.com" -production silent -nologo "作业文件.spj"
     ```
  2. **方案 2（备用）**：Python 内部驱动 `spss.Submit()` → 无闪屏，**但只能跑纯分析语法**
     - ❌ 不能包含 `OUTPUT SAVE`、`OUTPUT EXPORT`、`HOST COMMAND`、`XDATA` 等
  3. **方案 3（最后备选）**：`stats.exe` GUI 版 + `.spj` → 可能有闪屏
     ```bash
     "C:\Program Files\IBM\SPSS\Statistics\[版本]\stats.exe" -production silent -nologo "作业文件.spj"
     ```
- **内置 Python 路径**：`C:\Program Files\IBM\SPSS\Statistics\[版本]\Python3\python.exe`
- **.spj 文件 XML 结构模板**：
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       print="false" syntaxErrorHandling="continue"
       syntaxFormat="interactive" unicode="true">
    <locale charset="UTF-8" country="CN" language="zh"/>
    <output outputFormat="viewer" outputPath="输出.spv"/>
    <syntax syntaxPath="语法.sps"/>
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
### SPSS Modeler 环境配置 / SPSS Modeler Environment

- **版本 / Version**：IBM SPSS Modeler [18.0/18.1/18.2/18.3/18.4/18.5/18.6]
- **主程序 / Main Executable**：`C:\Program Files\IBM\SPSS\Modeler\[版本]\bin\clemb.exe`
- **modelerclient.exe**：`C:\Program Files\IBM\SPSS\Modeler\[版本]\bin\modelerclient.exe`
- **Batch Mode 命令行格式**：
  ```powershell
  # 执行流文件
  clemb.exe -local -stream "作业文件.str" -log "输出.log" -execute

  # 执行 Python 脚本（推荐）
  clemb.exe -local -script "train_model.py" -scriptlang python -log "train.log" -execute
  ```
- **配置字段 / Config Field**：`config.json > "SPSS Modeler"`
- **与 Statistics 的区别**：Statistics 是统计分析工具，Modeler 是数据挖掘/建模工具
```

## SPSSModeler Version Differences

| Version | clemb.exe Path | Notes |
|---------|---------------|-------|
| 18.6 | `C:\Program Files\IBM\SPSS\Modeler\18.6\bin\clemb.exe` | Latest, Python scripting |
| 18.5 | `C:\Program Files\IBM\SPSS\Modeler\18.5\bin\clemb.exe` | Performance improvements |
| 18.0 | `C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe` | Classic stable |

## Stata Memory Template

```markdown
### Stata 环境配置

- **版本**：Stata [VERSION] [EDITION]（MP/SE/BE）
- **主程序路径**：`[STATA_EXE_PATH]`（如 `StataMP-64.exe`）
- **批处理命令行格式**：
  ```bash
  # Windows — 新版本 MP/SE (Stata 14+)
  "[STATA_EXE_PATH]" /b do "script.do"
  # Windows — 老旧 SE (如 Stata 12 SE) 用 /e 避免弹窗
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
### R 环境配置 / R Environment

- **版本 / Version**：R [VERSION]
- **Rscript 路径 / Rscript Path**：`[RSCRIPT_EXE_PATH]`
- **批处理命令行格式 / Batch Command Format**：
  ```bash
  Rscript --vanilla "script.R"
  ```
```

## SAS Memory Template

```markdown
### SAS 环境配置 / SAS Environment

- **版本 / Version**：SAS [VERSION]（如 9.4）
- **主程序路径 / Executable Path**：`[SAS_EXE_PATH]`

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

## SPSS Modeler Memory Template

```markdown
### SPSS Modeler 环境配置 / SPSS Modeler Environment

- **版本 / Version**：IBM SPSS Modeler [18.0/18.1/18.2/18.3/18.4/18.5/18.6]
- **主程序 / Main Executable**：`C:\Program Files\IBM\SPSS\Modeler\[版本]\bin\clemb.exe`
- **modelerclient.exe**：`C:\Program Files\IBM\SPSS\Modeler\[版本]\bin\modelerclient.exe`
- **Batch Mode 命令行格式**：
  ```powershell
  clemb.exe -local -stream "作业文件.str" -log "输出.log" -execute
  ```
- **配置字段 / Config Field**：`config.json > "SPSS Modeler"`
- **与 Statistics 的区别**：
  - Statistics 用 `.spj` + `stats.com -production silent -nologo`
  - Modeler 用 `.str` + `clemb.exe -local -execute`
```

## SPSSModeler Version Differences

| Version | clemb.exe Path | Notes |
|---------|---------------|-------|
| 18.6 | `C:\Program Files\IBM\SPSS\Modeler\18.6\bin\clemb.exe` | Latest, Python scripting |
| 18.5 | `C:\Program Files\IBM\SPSS\Modeler\18.5\bin\clemb.exe` | Performance improvements |
| 18.0 | `C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe` | Classic stable |

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
✅ SPSS [version] 配置完成！

📋 Configuration:
  - Version: IBM SPSS Statistics [version]
  - Path: [install_path]
  - Bundled Python: [python_path] (Python [ver])
  - f-string: [✅/❌]

✅ Internal Python test passed (no splash screen).
```

### Stata

```
✅ Stata [version] 配置完成！

⚠️ Notes:
  1. New MP/SE (14+) use `/b`; old SE (e.g., Stata 12) must use `/e`
  2. Wrap paths with spaces in quotes
  3. License match: MP→StataMP-64.exe / SE→StataSE-64.exe / BE→Stata-64.exe

📋 Invocation:
  "StataMP-64.exe" /b do "script.do"
```

### R

```
✅ R [version] 配置完成！

⚠️ Notes:
  1. Use Rscript --vanilla, not GUI
  2. Use fileEncoding="UTF-8" for Chinese encoding
  3. Use data.table/arrow for large memory data

📋 Invocation:
  "[Rpath]\Rscript.exe" --vanilla "script.R"
```

### SAS

```
✅ SAS [version] 配置完成！

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
| JMP | `statsoft-jmp run script.jsl` |
| GraphPad | `statsoft-graphpad run file.pzfx` |
