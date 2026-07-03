# Version & Platform Specifics

> Reference for version differences across statistical software.

---

## Platform Support Summary

| Software | Windows | macOS | Linux |
|----------|---------|-------|-------|
| R | ✅ | ✅ | ✅ |
| Stata | ✅ | ✅ | ✅ |
| SAS | ✅ | ✅ | ✅ |
| StatTransfer | ✅ | ✅ | ❌ |
| Gretl | ✅ | ✅ | ✅ |
| Matlab | ✅ | ✅ | ✅ |
| Mathematica | ✅ | ✅ | ✅ |
| Julia | ✅ | ✅ | ✅ |
| Minitab | ✅ | ⚠️ | ⚠️ |
| SPSS Statistics | ✅ | ❌ | ❌ |
| SPSS Modeler | ✅ | ❌ | ❌ |
| JMP | ✅ | ⚠️ | ⚠️ |
| GraphPad Prism | ✅ | ❌ | ❌ |
| EViews | ✅ | ❌ | ❌ |
| Statistica | ✅ | ❌ | ❌ |
| CmdStan | ✅ | ✅ | ✅ |
| Weka | ✅ | ✅ | ✅ |
| KNIME | ✅ | ✅ | ✅ |
| jamovi | ✅ | ✅ | ✅ |
| JASP | ✅ | ✅ | ✅ |
| PSPP | ✅ | ✅ | ✅ |
| Mplus | ✅ | ✅ | ❌ |
| AMOS (IBM) | ✅ | ❌ | ❌ |
| Q / MRKS | ✅ | ❌ | ❌ |
| JAGS | ✅ | ✅ | ✅ |
| SHAZAM | ✅ | ✅ | ✅ |
| OxMetrics | ✅ | ✅ | ✅ |
| TSP | ✅ | ✅ | ✅ |
| Tanagra | ✅ | ✅ | ✅ |
| Orange | ✅ | ✅ | ✅ |
| H2O.ai | ✅ | ✅ | ✅ |
| GenStat | ✅ | ✅ | ✅ |
| Rattle | ✅ | ✅ | ✅ |
| OpenBUGS | ✅ | ✅ | ✅ |
| LIMDEP | ✅ | ❌ | ❌ |
| NLOGIT | ✅ | ❌ | ❌ |
| Microfit | ✅ | ❌ | ❌ |

---

## SPSS Statistics Version Differences

| Version | Bundled Python | f-string Support |
|---------|---------------|-----------------|
| 26 | Python 3.4 | ❌ |
| 27 | Python 3.8 | ✅ |
| 28 | Python 3.9 | ✅ |
| 29 | Python 3.10.4 | ✅ |
| 30 | Python 3.10 | ✅ |

### spss_helper.py Compatibility

- SPSS Statistics 26: Script uses `%s` / `.format()`, no f-string
- SPSS Statistics 27+: Script can use f-string and modern Python

---

## SPSS Modeler Version Differences

| Version | clemb.exe Path | Notes |
|---------|---------------|-------|
| 18.6 | `...\Modeler\18.6\bin\clemb.exe` | Latest, Python scripting |
| 18.5 | `...\Modeler\18.5\bin\clemb.exe` | Performance improvements |
| 18.0 | `...\Modeler\18.0\bin\clemb.exe` | Classic stable |

### clemb.exe Common Arguments

```
-local          Run in local mode (batch recommended)
-stream <file>  Load and execute .str stream file
-script <file>  Load and execute Python script
-project <file> Load project
-execute        Execute loaded stream/script
-log <file>     Redirect log to file
-server         Server mode (requires Modeler Server)
-hostname <h>   Server address
-port <n>       Server port
-username <n>   Username
-password <p>   Password
```

---

## CmdStan Version Differences

| Version | Notes |
|---------|-------|
| 2.30+ | Latest, improved threading, pathfinder |
| 2.28+ | Improved HMC adaptation |
| 2.26+ | Generated quantities redesign |

### CmdStan CLI Usage

```bash
# Compile model
cd $CMDSTAN && make /path/to/model

# Run sampling
./model sample num_samples=2000 num_warmup=1000 data file=init.csv output file=out.csv

# Summary
stansummary out.csv
```

---

## Weka CLI Usage

```bash
# Run filter/from command line
java -cp $WEKA_HOME/weka.jar weka.filters.unsupervised.attribute.StringToWVector \
  -i input.arff -o output.arff

# Classifier
java -cp $WEKA_HOME/weka.jar weka.classifiers.trees.RandomForest \
  -t train.arff -T test.arff -p 0
```

---

## KNIME Batch Usage

```bash
# Headless batch mode
knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION \
  -workflowFile=/path/to/workflow.knwf \
  -workflow.variable=threshold,0.5,double

# CLI only (KNIME Server)
knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION \
  -workflowDir=/path/to/workflow_directory
```

---

## Mplus Version Differences

| Version | Notes |
|---------|-------|
| 8.11 | Latest (2025) |
| 8.10 | BCH method for mixture models |
| 8.8 | Improved multilevel |
| 8.0 | Baseline |

### Mplus CLI Usage

```bash
# Batch mode — create .inp file with DATA/FILEDATA/SAVEDATA/OUTPUT
# Then:
mplus model.inp

# Example .inp file:
TITLE: My analysis
FILEDATA: FILE IS data.dat;
MODEL: y ON x1 x2;
OUTPUT: MODINDICES STANDARDIZED;
SAVEDATA: FILE IS results.dat;
```

---

## Stata Version Differences

| Version | Windows Batch Flag | Mac/Linux Batch Flag |
|---------|-------------------|---------------------|
| ≤ 12 | `/e do "script.do"` | `-e do "script.do"` |
| ≥ 13 | `/b do "script.do"` | `-b do "script.do"` |

---

## R Version Differences

| R Version | Bundled Python | SPSS Equivalent |
|-----------|---------------|-----------------|
| 3.4 | Python 3.4 | SPSS Statistics 26 |
| 3.5+ | Python 3.7+ | SPSS Statistics 27+ |
| 4.0+ | Python 3.9+ | SPSS Statistics 30+ |

---

## SAS Version Differences

| Platform | Batch Mode |
|----------|-----------|
| Windows | `sas -sysin "prog.sas" -log "out.log" -print "out.lst"` |
| Linux | `sas -sysin "prog.sas" -log "out.log" -print "out.lst"` |
| macOS | `sas -sysin "prog.sas" -log "out.log" -print "out.lst"` |

---

## JMP Version Differences

| Version | Extension | Batch Command |
|---------|-----------|--------------|
| 14/15/16 | `.jsl` | `JMP.exe /R "script.jsl"` |
| 16 Pro | `.jsl` | `JMP.exe /S /R "script.jsl"` |
| JMP Live | Web-based | Web API |

---

## jamovi Version Differences

| Version | Notes |
|---------|-------|
| 2.4+ | Latest, Rj module support |
| 2.3+ | Improved syntax export |

### jamovi CLI Usage

```bash
# Rj mode (execute R syntax from command line)
jamovi --Rj "summary(mtcars)"

# Or run Rj script file
jamovi "script.Rj"
```

---

## JASP Version Differences

| Version | Notes | CLI Status |
|---------|-------|-----------|
| 0.18+ | Latest | ⚠️ `jasp --console` (Beta) |
| 0.16+ | Improved modules | ⚠️ Limited CLI |

### JASP CLI Usage

```bash
# Experimental — may not support all features in headless mode
jasp --console data.csv
```

---

## PSPP Version Differences

| Version | Notes |
|---------|-------|
| 2.0+ | Latest, improved compatibility |
| 1.6+ | Added GLM |

### PSPP CLI Usage

```bash
# Run .sps syntax
pspp -o output.txt analysis.sps

# Pipe mode
pspp < analysis.sps
```

---

## AMOS Version Differences

| Version | Notes |
|---------|-------|
| 29.0 | Latest (SPSS Statistics 29 bundle) |
| 28.0 | Improved multi-group |
| 27.0 | Baseline |

### AMOS Batch Usage

> ⚠️ AMOS CLI is limited. Use Python extension to control AMOS:

```python
# Requires IBM SPSS Amos Python extension
import amos
amos.RunAnalysis("model.amw", "output.out")
```

---

## Q (MRKS) Version Differences

| Version | Notes |
|---------|-------|
| 6.0+ | Latest |
| 5.5+ | Improved R integration |

### Q Batch Usage

```batch
REM Run QScript
Q.exe /QScript "c:\scripts\analysis.qs"
```

---

## Mathematica Version Differences

| Version | Notes |
|---------|-------|
| 14.0 | Latest (2024), improved WolframScript |
| 13.0 | Baseline for modern Wolfram Language |
| 12.0 | First version with full WolframScript support |

### Mathematica CLI Usage

```bash
# Run Wolfram Language script
wolframscript -file script.wl

# Execute code directly
wolframscript -code "Table[i^2, {i, 10}]"

# Windows explicit MathKernel call
"C:\Program Files\Wolfram Research\Mathematica\14.0\MathKernel.exe" -noprompt < script.m
```

### Mathematica Common Errors

| Error | Solution |
|-------|----------|
| `wolframscript not found` | Add Mathematica to PATH or use full path |
| License activation required | Run Mathematica GUI once to activate |
| `MathKernel` hangs | Use `-noprompt` flag for batch mode |

---

## Common Errors & Solutions

| Software | Error | Solution |
|----------|-------|----------|
| SPSS Statistics | NullPointerException | Add `<output>` to .spj XML |
| SPSS Statistics | UnicodeDecodeError | Use `cp1252` or `errors='replace'` |
| SPSS Statistics | F-string error (v26) | Use `%s` formatting |
| SPSS Modeler | Stream not found | Verify file path and .str extension |
| CmdStan | `stanc` not found | Set CMDSTAN env var, run setup |
| CmdStan | Compilation fails | Check C++ toolchain |
| Weka | Out of memory | Use `-Xmx` JVM flag with Java |
| KNIME | `-workflowDir` not recognized | Update to KNIME 4.7+ |
| Mplus | License not found | Check license file |
| Mplus | Model not found | Verify .inp file and data path |
| Stata | Confirmation dialog | Loop: v≤12 → `/e`, v≥13 → `/b` |
| R | Package not installed | `install.packages()` |
| SAS | License expired | Update license file |

---

## JAGS Version Differences

| Version | Notes |
|---------|-------|
| 4.3.0 | Latest stable |
| 4.2.0 | Improved parallel chain support |

### JAGS CLI Usage

```bash
# Run JAGS script
jags scriptfile

# Batch execution
jags-script script.txt

# With R interface
Rscript -e "library(rjags); jags.model('script.dat', data)"
```

### JAGS Common Errors

| Error | Solution |
|-------|----------|
| `Cannot find JAGS` | Install JAGS |
| Syntax error in model | Check BUGS syntax |
| MCMC did not converge | Increase burn-in and iterations |

---

## SHAZAM Version Differences

| Version | Notes |
|---------|-------|
| 12.0 | Latest, improved command language |
| 11.0 | Baseline |

### SHAZAM CLI Usage

```bash
# Run SHAZAM command file
shazam commands.txt

# Sample command file content:
# /MODEL TITLE MYMODEL
# / X 1 100
# / PREDICT Y
# /END
```

---

## OxMetrics Version Differences

| Version | Notes |
|---------|-------|
| 8.0 | Latest (Ox 8) |
| 7.0 | Baseline |

### OxMetrics CLI Usage

```bash
# Show CLI options
oxmetrics --help

# Run batch
oxmetrics -b commands.txt
```

---

## TSP Version Differences

| Version | Notes |
|---------|-------|
| 5.0 | Latest |
| 4.5 | Baseline |

### TSP CLI Usage

```bash
# Run TSP command file
tsp commands.txt
```

---

## Tanagra Version Differences

| Version | Notes |
|---------|-------|
| 1.8 | Latest |
| 1.5 | Baseline |

### Tanagra CLI Usage

```bash
# Show CLI options
tanagra --help

# Execute batch script
tanagra -f script.txt
```

---

## Orange Version Differences

| Version | Notes |
|---------|-------|
| 3.36 | Latest |
| 3.30 | Baseline |

### Orange CLI Usage

```bash
# Show CLI options (GUI mode)
orange-canvas --help

# Python module approach (recommended)
python3 -m Orange.canvas
```

### Orange Common Errors

| Error | Solution |
|-------|----------|
| Module not found | `pip install orange3` |
| Conda issues | `conda install -c condaforge orange3` |

---

## H2O.ai Version Differences

| Version | Notes |
|---------|-------|
| 3.44 | Latest |
| 3.40 | AutoML improvements |

### H2O CLI Usage

```bash
# Show CLI options
h2o --help

# Start H2O server
h2o start

# Via Python (recommended)
python3 -c "import h2o; h2o.init()"
```

### H2O Common Errors

| Error | Solution |
|-------|----------|
| Server not starting | Check Java, `java -version` |
| Out of memory | Set `-Xmx` in `h2o.start()` |
| Port conflict | Change port: `h2o.init(port=54322)` |

---

## GenStat Version Differences

| Version | Notes |
|---------|-------|
| 23.0 | Latest |
| 22.0 | Baseline |

### GenStat CLI Usage

```bash
# Show CLI options
genstat --help

# Run GenStat command file
genstat commands.txt
```

---

## Rattle Version Differences

| Version | Notes |
|---------|-------|
| 5.5 | Latest |
| 5.0 | Baseline |

### Rattle CLI Usage

```bash
# Run Rattle in CLI mode
rattle --cli

# Via R package
Rscript -e "library(rattle); rattle()"
```

---

## OpenBUGS Version Differences

| Version | Notes |
|---------|-------|
| 3.2.3 | Latest stable |
| 3.2.2 | Baseline |

### OpenBUGS CLI Usage

```bash
# Show CLI options
openbugs --help

# Batch execution via script
openbugs -b script.txt
```

---

## LIMDEP Version Differences

| Version | Notes |
|---------|-------|
| 11.0 | Latest |
| 10.0 | Baseline |

### LIMDEP CLI Usage

```batch
REM Run LIMDEP command file
limdep commands.txt
```

### LIMDEP Common Errors

| Error | Solution |
|-------|----------|
| License not found | Check license file |
| Data not found | Verify data path in command file |

---

## NLOGIT Version Differences

| Version | Notes |
|---------|-------|
| 6.0 | Latest |
| 5.0 | Discrete choice improvements |

### NLOGIT CLI Usage

```batch
REM Run NLOGIT command file
nlogit commands.txt
```

### NLOGIT Common Errors

| Error | Solution |
|-------|----------|
| Model not converging | Check starting values |
| Sample size mismatch | Verify data dimensions |

---

## Microfit Version Differences

| Version | Notes |
|---------|-------|
| 5.0 | Latest |
| 4.0 | Baseline |

### Microfit CLI Usage

```batch
REM Run Microfit command file
microfit commands.txt
```

---

## NCSS

### Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（/B 参数） | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Version Differences

| Version | Notes |
|---------|-------|
| 2024 | Latest, batch mode support |
| 2023 | Baseline |

### NCSS CLI Usage

```batch
REM Run NCSS batch analysis
"NCSS.exe" /B "analysis.ncss"
```

---

## Origin (OriginLab)

### Platform Support

| 平台 / Platform | 支持 | CLI 支持 | 闪屏 |
|----------------|------|----------|------|
| Windows | ✅ | ✅（-h 参数） | ❌ |
| macOS | ✅ | ⚠️ 有限 / Limited | ⚠️ 可能有 / May have |
| Linux | ❌ | ❌ | — |

### Version Differences

| Version | Notes |
|---------|-------|
| 2025 | Latest, improved LabTalk support |
| 2024 | Baseline |
| 2023 | Older versions may have limited CLI support |

### Origin CLI Usage

```batch
REM Run LabTalk script in batch mode
origin97 -h script.ogs
```
