# Command Invocation Examples

> This document contains CLI command invocation examples for each statistical software package.

---

## Table of Contents

1. [R](#r)
2. [SPSS](#spss)
3. [Stata](#stata)
4. [SAS](#sas)
5. [JMP](#jmp)
6. [GraphPad Prism](#graphpad)
7. [Stat/Transfer](#stattranfer)
8. [Other software](#others)
9. [JAGS](#jags)
10. [SHAZAM](#shazam)
11. [OxMetrics](#oxmetrics)
12. [TSP](#tsp)
13. [Tanagra](#tanagra)
14. [Orange](#orange)
15. [H2O.ai](#h2o)
16. [GenStat](#genstat)
17. [Rattle](#rattle)
18. [OpenBUGS](#openbugs)
19. [LIMDEP](#limdep)
20. [NLOGIT](#nlogit)
21. [Microfit](#microfit)

---

## R

### Basic run

```bash
# Run R script
Rscript --vanilla "script.R"

# Use R CMD BATCH (generates .Rout file)
R CMD BATCH "script.R" "output.Rout"
```

### Package installation (requires explicit user confirmation before network download/install)

```bash
# Downloads from CRAN and modifies the local R environment; requires explicit user confirmation before running — do not install without it
Rscript -e "install.packages('pkg', repos='https://cran.r-project.org')"
```

### Batch script template

```r
# script.R
options(warn=-1)
library(dplyr)

data <- read.csv("data.csv", fileEncoding="UTF-8")
result <- lm(y ~ x1 + x2, data=data)
summary(result)

write.csv(result$coefficients, "results.csv", row.names=FALSE)
save(result, file="results.RData")
```

### Common scenarios

```bash
# Read SPSS .sav file
Rscript -e "library(haven); df <- read_sav('data.sav'); print(head(df))"

# Generate HTML report
Rscript -e "rmarkdown::render('report.Rmd', output_file='report.html')"

# Large data processing
Rscript -e "library(arrow); df <- read_parquet('big_data.parquet'); print(dim(df))"
```

---

## SPSS

### 🎯 Usage Recommendation

> **For daily complex syntax runs** → **use Approach 1** (`stats.com` + `.spj`, foolproof)
>
> **Approach 2** (internal Python driver) **can only run pure analysis syntax** and **must not contain** the following commands:
> - ❌ `OUTPUT SAVE`
> - ❌ `OUTPUT EXPORT` / `OUTPUT DISPLAY`
> - ❌ `HOST COMMAND`
> - ❌ `XDATA` / `XSAVE` (when OUTPUT objects are involved)
>
> — When unsure whether a command involves OUTPUT/SAVE, use Approach 1 (`.spj`) for safety.

---

### ⭐ Preferred approach (completely splash-free)

Run directly through the SPSS built-in Python `spss` module:

```bash
# Invoke via spss_helper.py
"C:\Program Files\IBM\SPSS\Statistics\XX\Python3\python.exe" \
  "C:\path\to\statsoft-cli\windows-only\SPSS\spss_helper.py" \
  run-internal "C:\path\to\syntax.sps"
```

**Call chain**:
```
AI Agent (Bash tool)
  → python.exe spss_helper.py run-internal <sps_file>
      → subprocess.run([stats_python_path, helper_script], creationflags=0x08000000)
          → SPSS runs in background (zero window)
```

### Fallback approach

Run the .spj file via `stats.com` (console version, completely splash-free):

```bash
"C:\Program Files\IBM\SPSS\Statistics\XX\stats.com" -production silent -nologo "job.spj"
```

Or use `stats.exe` (GUI version, may show a splash screen):

```bash
"C:\Program Files\IBM\SPSS\Statistics\XX\stats.exe" -production "job.spj" silent -nologo
```

### .spj file XML structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     print="false"
     syntaxErrorHandling="continue"
     syntaxFormat="interactive"
     unicode="true"
     xsi:schemaLocation="http://www.ibm.com/software/analytics/spss/xml/production 
     http://www.ibm.com/software/analytics/spss/xml/production/production-1.4.xsd">
  <locale charset="UTF-8" country="CN" language="zh"/>
  <output outputFormat="viewer" outputPath="output.spv"/>
  <syntax syntaxPath="syntax.sps"/>
</job>
```

**Key**: the `<output>` element must not be omitted, otherwise a NullPointerException is thrown.

### Automated Python script (completely GUI-free)

```python
import sys, os

# 1. Configure paths
spss_python_path = r"C:\Program Files\IBM\SPSS\Statistics\XX\Python3\python.exe"
sps_file = r"project\analysis.sav"
output_sav = r"project\results.sav"

# 2. Generate SPSS syntax
sps_syntax = """
GET FILE='data.sav'.
COMPUTE new_var = var1 + var2.
SAVE OUTFILE='{out}'.
""".format(out=output_sav.replace("\\", "/"))

# 3. Run via SPSS built-in Python (completely GUI-free)
spss_pkg = os.path.join(os.path.dirname(spss_python_path), "Lib", "site-packages")
sys.path.insert(0, spss_pkg)

import spss
spss.StartSPSS()
print("SPSS processor started (no GUI)")

# Submit syntax
spss.Submit(sps_syntax)
print("Syntax executed")

spss.StopSPSS()
print("SPSS processor stopped")

# 4. Read results (using Anaconda Python's pyreadstat)
import pyreadstat
df, meta = pyreadstat.read_sav(output_sav)
print(df.head())
```

---

## SPSS Modeler

### Batch execute .str stream file

```powershell
# Via statsoft-modeler CLI
statsoft-modeler run "C:\path\to\churn_model.str"

# Or call clemb.exe directly
& "C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe" -local -stream "churn_model.str" -log "run.log" -execute
```

### Python script mode (recommended)

```powershell
# Run Python script (within Modeler session)
statsoft-modeler run-script "C:\path\to\train_model.py"

# Equivalent to clemb command
& "C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe" -local `
    -script "train_model.py" -scriptlang python `
    -log "train.log" -execute
```

### Remote Modeler Server mode (not supported)

> ⚠️ This skill does NOT support remote Modeler Server execution. `statsoft-modeler` provides LOCAL (`-local`) mode only — there is no `server-run` subcommand, and the skill never initiates remote connections or handles remote credentials.

### Python script example (run within Modeler)

```python
# train_model.py — SPSS Modeler Python script
import modeler.api

# Get current session
session = modeler.api.GetSession()

# Load stream file
stream = session.LoadStream("churn_model.str")

# Set parameters
stream.SetVariable("data_path", "C:/data/customer.csv")

# Execute stream
stream.Execute()

# Export results
output_node = stream.FindNode("table_output")
output_node.Export("C:/output/results.csv")
```

---

## Stata

### ⚠️ Version and parameter reference table

| Version | Windows silent flag | Mac/Linux silent flag |
|------|-----------------|-------------------|
| **Stata ≤ 12** | `StataMP /e do "script.do"` | `stata-mp -e do "script.do"` |
| **Stata ≥ 13** | `StataMP /b do "script.do"` | `stata-mp -b do "script.do"` |

**Key**: Stata 12 uses `-e`, Stata 13+ uses `-b`. Using the wrong version parameter triggers a confirmation dialog!

### Basic batch example

```bash
# Stata 13+ (Windows)
"C:\Program Files\Stata17\StataMP-64.exe" /b do "script.do"

# Stata 13+ (Mac/Linux)
stata-mp -b do "script.do"

# Stata 12 and earlier (Windows) — /b not supported!
"C:\Program Files\Stata12\StataMP.exe" /e do "script.do"

# Stata 12 and earlier (Mac/Linux) — -b not supported!
stata-mp -e do "script.do"
```

### Version and executable file reference

| Version | MP | SE | BE |
|------|----|----|-----|
| Stata 12 and earlier | `StataMP` | `StataSE` | `Stata` |
| Stata 14/15 | `StataMP` | `StataSE` | `Stata` |
| Stata 16+ | `StataMP-64.exe` | `StataSE-64.exe` | `Stata-64.exe` |

### do-file template

```stata
* script.do — Stata batch script
cd "workdir"
use "data.dta", clear
regress y x1 x2
save "results.dta", replace
log using "results.log", replace
summarize
log close
```

---

## SAS

### Basic batch

```bash
# Windows
"C:\Program Files\SASFoundation\9.4\sas.exe" -sysin "prog.sas" -log "out.log" -print "out.lst"

# Mac/Linux
sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

### SAS program template

```sas
* prog.sas — SAS batch program;
options ls=80 ps=60 nodate nonumber encoding='utf-8';

* Read data;
data work.data;
    infile "data.csv" dlm=',' firstobs=2;
    input var1 var2 var3;
run;

* Analysis;
proc reg data=work.data;
    model y = var1 var2;
run;

* Save results;
proc export data=work.result
    outfile="results.csv"
    dbms=csv replace;
run;
```

---

## JMP

### Basic batch

```powershell
# Batch mode (may show brief splash screen 1-2 seconds)
& "C:\Program Files\JMP\16\JMP.exe" /R "script.jsl"
```

⚠️ JMP script must end with `Exit();`

### JSL script template

```jsl
// script.jsl — JMP batch script
dt = Open("data.jmp");
dt << Fit Y( :Y Column ) X( :X Column );
Save PDF("report.pdf");
Close(dt, "Yes");
Exit();
```

---

## GraphPad Prism

⚠️ **Important limitation (GUI-only, out of scope)**: GraphPad Prism **has no CLI mode**; invocation always pops up the GUI, unavoidable.

**This skill's capability for Prism is limited to**:
- Detecting whether Prism is installed locally;
- Providing **guidance to manually launch the GUI** (you open Prism yourself).

**This skill explicitly does NOT do the following** (even after opt-in):
- Does not call `prism.exe` from the command line or automate/drive the Prism process in any way;
- **Does not create, read, or modify any Prism-related files (including `.pzfx` project/data files)**.

> Note: `.pzfx` is an XML format; third-party pure-Python libraries (e.g., `prismWriter`) can parse/generate it. Such file read/write **is not part of this skill's allowed behavior** — this skill does not wrap, call, or perform such write operations. If you truly need it, use the relevant library manually outside this skill and take responsibility for the file writes yourself.

---

## StatTransfer

### Single-file conversion

```bash
# SPSS → Stata
st in.sav out.dta

# CSV → SPSS
st in.csv out.sav

# SAS → R
st in.sas7bdat out.rda
```

### Batch conversion

```bash
# Batch-convert all .sav in a directory to .dta
st in\*.sav out\*.dta

# Command-file batch processing
st myfile.stcmd
```

---

## Other software

### Gretl

```bash
# Run gretl script in batch mode
gretlcli -b script.inp
```

### Mathematica

```bash
# Run Wolfram Language script
wolframscript -file script.wl

# Execute code directly
wolframscript -code "Table[i^2, {i, 10}]"

# Load data and analyze
wolframscript -code "data = Import[\"data.csv\"]; Mean[data]"

# Symbolic computation
wolframscript -code "D[x^3 + 2x^2 + 5, x]"

# Statistical modeling
wolframscript -code "data = RandomVariate[NormalDistribution[], 1000]; DistributionFitTest[data, Automatic]"

# Generate image
wolframscript -code "p = Plot[Sin[x], {x, 0, 6 Pi}, PlotLabel -> \"Sine Wave\"]; Export[\"sine.png\", p]"

# Windows explicit MathKernel call (alternative to wolframscript)
"C:\Program Files\Wolfram Research\Mathematica\14.0\MathKernel.exe" -noprompt < script.m
```

### Minitab

> ⚠️ **Minitab is GUI-only for automation.** `mtb.exe /run "script.mtb"` launches the full Minitab GUI window (not headless) and may hang. Do **not** drive Minitab from the agent — detect the install and let the user run analyses interactively.

```powershell
# Detection only — verify mtb.exe exists; do NOT call /run headlessly
$mtb = "C:\Program Files\Minitab\Minitab 22\mtb.exe"
if (Test-Path $mtb) { Write-Host "Minitab detected: $mtb" }
```

For actual analysis, open Minitab (GUI) and load your `.mtb` / `.mpj` project, or use the Minitab Web App (https://app.minitab.com/).

### Matlab

```bash
# Completely GUI-free batch
matlab -batch "run('script.m'); exit"
```

### Julia

```bash
julia script.jl
```

### EViews

```powershell
# EViews batch
& "C:\Program Files\QMS\EViews 12\EViews12_x64.exe" /b "program.prg"
```

### Statistica

```powershell
# Statistica Visual Basic script
& "C:\Program Files\StatSoft\Statistica 13\Statistica.exe" /s "script.svb"
```

---

## JAGS

### Basic batch

```bash
# Run JAGS script
jags scriptfile

# Batch execution
jags-script script.txt

# Via R interface
Rscript -e "library(rjags); jags.model('script.dat', data)"
```

---

## SHAZAM

### Basic batch

```bash
# Run SHAZAM command file
shazam commands.txt

# Sample command file:
# /MODEL TITLE MYMODEL
# / X 1 100
# / PREDICT Y
# /END
```

---

## OxMetrics

### Basic batch

```bash
# Show CLI options
oxmetrics --help

# Run batch
oxmetrics -b commands.txt
```

---

## TSP

### Basic batch

```bash
# Run TSP command file
tsp commands.txt
```

---

## Tanagra

### Basic batch

```bash
# Show CLI options
tanagra --help

# Execute batch script
tanagra -f script.txt
```

---

## Orange

### Python module approach (recommended)

```bash
# Via Python module
python3 -m Orange.canvas

# Install (requires network; modifies local Python environment; run only after explicit user confirmation)
# Install (requires network access and modifies the local Python environment; run ONLY after explicit user confirmation)
pip install orange3
# or
conda install -c conda-forge orange3
```

---

## H2O.ai

### Python approach (recommended)

> ⚠️ **Network & download note**: `h2o.init()` / `h2o start` starts a **local web server** on this machine (default port 54321, browser-accessible); the first run **downloads components** over the network; `pip install h2o` also requires network access. Before starting the H2O server, the Agent must explain this network behavior to the user and obtain explicit confirmation, and must never expose the port to the public internet.

```bash
# ⚠️ This starts a local H2O server (JVM, binds a port). Requires explicit per-run opt-in.
# Start H2O server (local HTTP service, default port 54321)
h2o start

# ⚠️ This starts a local H2O server (JVM, binds a port). Requires explicit per-run opt-in.
# Via Python
python3 -c "import h2o; h2o.init()"

# Install (requires network)
pip install h2o
```

---

## GenStat

### Basic batch

```bash
# Run GenStat command file
genstat commands.txt
```

---

## Rattle

### CLI mode

```bash
# CLI mode
rattle --cli

# Via R package
Rscript -e "library(rattle); rattle()"
```

---

## OpenBUGS

### Basic batch

```bash
# Show help
openbugs --help

# Batch execution
openbugs -b script.txt
```

---

## LIMDEP

### Basic batch

```batch
REM Run LIMDEP command file
limdep commands.txt
```

---

## NLOGIT

### Basic batch

```batch
REM Run NLOGIT command file
nlogit commands.txt
```

---

## Microfit

### Basic batch

```batch
REM Run Microfit command file
microfit commands.txt
```

---

## NCSS

### Basic batch

```batch
REM Run NCSS batch analysis
"NCSS.exe" /B "analysis.ncss"

REM Generate NCSS report
"NCSS.exe" /B "report.ncss"
```

### Analysis script template

```
[Analysis]
Procedure = Descriptive Statistics
Variables = Age, Height, Weight

[Output]
Export = "results.html"
```

---

## Origin (OriginLab)

### Run LabTalk script

```batch
REM Run LabTalk batch script
"C:\Program Files\OriginLab\Origin2025\origin97.exe" -h "script.ogs"
```

### LabTalk script template

```labtalk
// script.ogs — Origin LabTalk script
impASC fname:="C:\data\data.csv";
range rr = col(1);
integ1 rr;
type "Mean: $(mean(rr))";
doc -e P "C:\output\result.png";
exit;
```
