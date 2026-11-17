# Configuration Completion Prompts

> This document was extracted when SKILL.md was streamlined; it contains completion-prompt templates for each statistical software configuration.
> After software detection completes, the AI should output completion notices to the user following the templates below.

---

## SPSS

> ⚠️ **Important — daily usage recommendation**:
> - **For complex syntax runs → use Approach 1** (`stats.com` + `.spj`, foolproof)
> - **Approach 2** (internal Python driver) **can only run pure analysis syntax** and must not contain:
>   - `OUTPUT SAVE`, `OUTPUT EXPORT`, `OUTPUT DISPLAY`
>   - `HOST COMMAND`, `XDATA`, `XSAVE` (when OUTPUT objects are involved)
> - When unsure whether a command involves OUTPUT/SAVE → use Approach 1 (`.spj`) uniformly
>
> See SKILL.md core permissions section (Core Permissions) for SPSS invocation details.

---

## SPSS Modeler

- ✅ SPSS Modeler supports pure CLI execution via `clemb.exe`, completely GUI-free, no splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for data mining, predictive modeling, ML pipelines

---

## Stata

```
✅ Stata association configuration complete!

⚠️ Important notes:
  1. **⚠️⚠️ Stata version and batch parameters (important)**:
     - **Stata 12 and earlier** → Windows: `/e do "script.do"`, Mac/Linux: `-e do "script.do"`
     - **Stata 13 and later** → Windows: `/b do "script.do"`, Mac/Linux: `-b do "script.do"`
     - ❌ **Wrong version parameter triggers a confirmation dialog!**
  2. Paths containing spaces must be wrapped in double quotes, otherwise a file not found error occurs
  3. **License match**: when invoking Stata you must use the executable matching the license
     - MP license → use StataMP-64.exe (Windows) or stata-mp (Mac/Linux)
     - SE license → use StataSE-64.exe (Windows) or stata-se (Mac/Linux)
     - BE license → use Stata-64.exe (Windows) or stata (Mac/Linux)
     - ❌ If the wrong edition is used (e.g., MP binary without an MP license), Stata fails to start or errors out
  4. **Edition feature differences**:
     - MP (Multiprocessing): multi-core parallelism, good for large data
     - SE (Special Edition): single-core, good for medium data
     - BE (Basic Edition): limited features, no parallelism
  5. **Version-specific changes**:
     - Stata 14/15: executables named StataMP, StataSE (no -64 suffix)
     - Stata 16+: executables named StataMP-64, StataSE-64 (added -64 suffix)
     - Stata 16+: supports Python integration (call Python from Stata)
     - Stata 17+: introduced PyStata (call Stata from Python)
     - Stata 19+: introduced StataNow rapid-update mechanism
  6. **Windows install path differences**:
     - Stata 14-18: `C:\Program Files\StataNN` (NN is the version number)
     - Stata 19: `C:\Program Files\Stata19` or `C:\Program Files\StataNow19`

📋 Recommended usage:
  # Windows (choose correct edition by license)
  "StataMP-64.exe" /b do "script.do"   # MP edition (Stata 16+)
  "StataSE-64.exe" /b do "script.do"   # SE edition (Stata 16+)
  "Stata-64.exe" /b do "script.do"     # BE edition (Stata 16+)
  "StataMP" /b do "script.do"          # MP edition (Stata 14/15)

  # Mac/Linux (choose correct edition by license)
  stata-mp -b do "script.do"   # MP edition
  stata-se -b do "script.do"   # SE edition
  stata -b do "script.do"      # BE edition
```

---

## R

```
✅ R connection configuration complete!

⚠️ Important notes:
  1. Use Rscript command for batch mode, not R GUI
  2. Installing R packages requires EXPLICIT user confirmation (downloads from CRAN, modifies local environment) before proceeding — do not install without it
  3. Chinese encoding issues: use fileEncoding="UTF-8" parameter
  4. Insufficient memory: use data.table or arrow packages for large data

📋 Recommended usage:
  Rscript --vanilla "script.R"

  # Package installation (requires explicit user confirmation before network download)
  Rscript -e "cat('Installing package from CRAN (requires network access)...\n'); install.packages('[PKG]', repos='https://cran.r-project.org')"

  # Read SPSS .sav file
  Rscript -e "library(haven); df <- read_sav('data.sav'); print(head(df))"

💡 Alternatives without R:
  If R is not installed, consider using Anaconda Python environment:
  - dplyr / tidyr → pandas
  - ggplot2 → matplotlib / seaborn
  - caret / xgboost → scikit-learn
  - survival → lifelines
  - lme4 / nlme → statsmodels
  - metafor → PyMC
```

---

## SAS

```
✅ SAS connection configuration complete!

⚠️ Important notes:
  1. Batch mode generates .log (log) and .lst (output listing) files, ensure write permissions
  2. Chinese encoding: add options encoding='utf-8'; at beginning of program
  3. SAS license expiration will cause ERROR: License expired

📋 Recommended usage:
  # Windows
  "sas.exe" -sysin "prog.sas" -log "out.log" -print "out.lst"

  # Mac/Linux
  sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

---

## JMP

- ⚠️ JMP may display a brief splash screen (1-2 seconds), cannot be fully avoided
- ⚠️ Script must end with `Exit();` or JMP GUI will remain open

> See [ADDITIONAL_SOFTWARE.md → JMP](../ADDITIONAL_SOFTWARE.md#jmp) for details

---

## GraphPad Prism

- ⚠️⚠️⚠️ GraphPad Prism **has no CLI mode**; invocation pops up the GUI (unavoidable)
- ⚠️ When used, the following occurs: GUI pops up on invocation, user must operate manually
- 🖱️ This skill only provides **detection + manual GUI-launch guidance**; it does not drive batch processing via CLI/headless

**Parsing-only alternative**:
| Approach | Description |
|------|------|
| Python `prismWriter` library | Can **parse** .pzfx structure (read/validate) without launching the GUI; the library itself also has the ability to **generate** .pzfx, but this skill **never calls or wraps any of its write operations** (consistent with command-examples.md: .pzfx read/write is outside this skill's allowed scope; if needed, do it manually outside this skill and take responsibility) |

> See [ADDITIONAL_SOFTWARE.md → GraphPad Prism](../ADDITIONAL_SOFTWARE.md#graphpad-prism) for details

---

## Stat/Transfer

- ✅ Stat/Transfer is a pure CLI tool, completely GUI-free, suitable for automation
- ⚠️ Before conversion, confirm the target format supports the required data types

> See [ADDITIONAL_SOFTWARE.md → Stat/Transfer](../ADDITIONAL_SOFTWARE.md#stattransfer)

---

## Gretl

- ✅ Gretl is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Free software, suitable for econometric analysis
- 💡 Supports reading Stata .dta, SAS .sas7bdat, Excel .xlsx, etc.

> See [ADDITIONAL_SOFTWARE.md → Gretl](../ADDITIONAL_SOFTWARE.md#gretl)

---

## Minitab

- ⚠️ Minitab batch mode may show a brief splash screen
- ⚠️ Ensure the license is valid
- 💡 Suitable for quality control and Six Sigma projects

> See [ADDITIONAL_SOFTWARE.md → Minitab](../ADDITIONAL_SOFTWARE.md#minitab)

---

## Matlab

- ✅ Completely GUI-free when using `-batch` parameter
- ⚠️ Requires Statistics and Machine Learning Toolbox
- 💡 Suitable for engineering statistics, signal processing, and ML

> See [ADDITIONAL_SOFTWARE.md → Matlab](../ADDITIONAL_SOFTWARE.md#matlab) for details

---

## Mathematica

- ✅ Mathematica is a pure CLI tool (`wolframscript`), completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- 💡 Suitable for symbolic mathematics, numerical analysis, statistical modeling, and visualization
- ⚠️ WolframScript requires a commercial license with periodic activation

> See [ADDITIONAL_SOFTWARE.md → Mathematica](../ADDITIONAL_SOFTWARE.md#mathematica) for details

---

## Julia

- ✅ Julia is a pure CLI tool, completely GUI-free, no splash screen
- ✅ High performance, suitable for big data and complex statistical computing
- 💡 Common packages: Statistics, HypothesisTests, GLM, Turing (Bayesian)

> See [ADDITIONAL_SOFTWARE.md → Julia](../ADDITIONAL_SOFTWARE.md#julia) for details

---

## EViews

- ⚠️ EViews batch mode may show a splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for time-series analysis, regression, and forecasting

> See [ADDITIONAL_SOFTWARE.md → EViews](../ADDITIONAL_SOFTWARE.md#eviews)

---

## Statistica

- ⚠️ Statistica batch mode may show a splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for data mining, machine learning, and statistical analysis

> See [ADDITIONAL_SOFTWARE.md → Statistica](../ADDITIONAL_SOFTWARE.md#statistica)

---

## JAGS

- ✅ JAGS is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ⚠️ If invoked via the `rjags` R package, R and the rjags package must be installed first
- 💡 Suitable for Bayesian hierarchical models, MCMC simulation

📋 Recommended usage:
  jags scriptfile

💡 Via R interface:
  Rscript -e "library(rjags); jags.model('script.dat', data)"

---

## SHAZAM

- ✅ SHAZAM is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ⚠️ Windows version requires a valid license file
- 💡 Suitable for econometrics, time series, hypothesis testing

📋 Recommended usage:
  shazam commands.txt

---

## OxMetrics

- ✅ OxMetrics is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ⚠️ License file required
- 💡 Suitable for econometrics, time series, forecasting

📋 Recommended usage:
  oxmetrics --help          # view options
  oxmetrics -b commands.txt # batch

---

## TSP

- ✅ TSP is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ⚠️ License file required
- 💡 Suitable for time-series analysis, econometrics, hypothesis testing

📋 Recommended usage:
  tsp commands.txt

---

## Tanagra

- ✅ Tanagra is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- 💡 Suitable for clustering, classification, association rules, feature selection

📋 Recommended usage:
  tanagra --help          # view options
  tanagra -f script.txt   # batch script

---

## Orange

- ⚠️ Orange **has no pure CLI mode**; invocation pops up the GUI (unavoidable)
- ✅ Recommended to call in the background via the Python module (no GUI needed)
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free

**Pure CLI alternative (Python)**:
```python
# Run Orange analysis script in background, no GUI needed
from Orange.data import Table
from Orange.classification import RandomForestLearner

data = Table("data.csv")
learner = RandomForestLearner()
model = learner(data)
predictions = model(data)
```

📋 Recommended usage:
  python3 -m Orange.canvas          # GUI mode
  python3 script.py                 # Python script mode (recommended, no GUI)

---

## H2O.ai

- ✅ H2O can run in the background via Python, no GUI popup
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free (AutoML fully free)
- ⚠️ Requires Java (JVM)
- ⚠️ First start downloads components
- 💡 Suitable for large-scale ML, AutoML, deep learning

📋 Recommended usage (Python):

> ⚠️ **Security note**: `h2o.init()` launches a local H2O server (a JVM process) and may open a listening port (default 54321); `h2o.import_file("data.csv")` transfers your dataset contents into that service. Require explicit user confirmation before running — never auto-execute.

```python
import h2o
h2o.init()                          # launches local H2O server (JVM)
h2o.import_file("data.csv")         # uploads dataset into the H2O service
# ... AutoML training ...
h2o.shutdown()                      # shut down the server
```

⚠️ Notes:
  - If default port 54321 is occupied, use `h2o.init(port=54322)`
  - If memory is insufficient, set `h2o.init(max_mem_size="4G")`

---

## GenStat

- ✅ GenStat is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ⚠️ License file required
- 💡 Suitable for mixed models, experimental design, REML, spatial analysis, Meta analysis

📋 Recommended usage:
  genstat commands.txt

---

## Rattle

- ⚠️ Rattle **has no pure CLI mode**; invocation pops up the GUI (unavoidable)
- ✅ Recommended to call Rattle functions via R script in the background (no GUI needed)
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- 💡 Suitable for data mining, decision trees, clustering, association rules

**Pure CLI alternative (R script)**:
```r
library(rattle)
# Load data
audit <- read.csv("audit.csv")
# Build model
model <- Target ~ Age + Employment + ... 
# Output results
summary(model)
```

📋 Recommended usage:
  rattle --cli    # try CLI mode (may still pop up, not guaranteed)
  Rscript script.R  # R script calling Rattle functions (recommended, no GUI)

---

## OpenBUGS

- ⚠️ OpenBUGS **has no pure CLI mode**; invocation pops up the GUI (unavoidable)
- ✅ Can be called in the background via R packages `R2OpenBUGS` or `BRugs` (no GUI needed)
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- 💡 Suitable for Bayesian analysis, MCMC, hierarchical models

**Pure CLI alternative (R script)**:
```r
library(BRugs)
# Define model
modelCheck("model.txt")
modelData("data.txt")
modelCompile()
modelUpdate(1000)
# Extract results
samplesStats("*")
```

📋 Recommended usage:
  openbugs --help            # GUI mode
  Rscript openbugs_script.R  # R script call (recommended, no GUI)

---

## LIMDEP

- ✅ LIMDEP is a pure CLI tool, completely GUI-free, no splash screen
- 🔴 Windows only
- ⚠️ License file required
- 💡 Suitable for Logit, Probit, Tobit, sample selection, Count models, Frontier analysis

📋 Recommended usage (Windows):
  limdep commands.txt

**English Memory Template**:
```
- **Version**: LIMDEP 11.0
- **Path**: `[LIMDEP_install_PATH]\limdep.exe`
- **Batch Command Format**:
  ```batch
  limdep commands.txt
  ```
- **Notes**: Windows only, license required
```

---

## NLOGIT

- ✅ NLOGIT is a pure CLI tool, completely GUI-free, no splash screen
- 🔴 Windows only
- ⚠️ License file required (included in LIMDEP license)
- 💡 Suitable for Multinomial Logit, Nested Logit, Mixed Logit, Probit models

📋 Recommended usage (Windows):
  nlogit commands.txt

---

## Microfit

- ✅ Microfit is a pure CLI tool, completely GUI-free, no splash screen
- 🔴 Windows only
- ⚠️ License file required
- 💡 Suitable for time series, econometrics, unit-root tests, ARDL, panel data

📋 Recommended usage (Windows):
  microfit commands.txt

---

## CmdStan

- ✅ CmdStan is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- ⚠️ First use requires compiling the model (time-consuming)
- ⚠️ Requires a C++ compiler (Windows: Rtools or Visual Studio)
- 💡 Suitable for Bayesian statistics, hierarchical models, consumer behavior modeling

📋 Recommended usage:
  # Compile model
  stanc model.stan
  # Run sampling
  sample num_samples=1000 num_warmup=500 data file=data.json
  # View results
  stansummary output.csv

💡 Via cmdstanr/cmdstanpy (recommended):
  Rscript -e "library(cmdstanr); model <- cmdstan_model('model.stan'); fit <- model\$sample(data_file='data.json')"

---

## Weka

- ✅ Weka is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- ⚠️ Requires Java environment (JVM)
- ⚠️ Increase JVM memory for large data: `java -Xmx4g -jar weka.jar ...`
- 💡 Suitable for clustering, classification, association rules, feature selection, market basket analysis

📋 Recommended usage:
  # Command line classification
  java -cp weka.jar weka.classifiers.trees.RandomForest -t data.arff -T test.arff
  # Clustering
  java -cp weka.jar weka.clusterers.SimpleKMeans -t data.arff -N 3
  # Association rules
  java -cp weka.jar weka.associations.Apriori -t data.arff

---

## KNIME

- ✅ KNIME supports headless mode, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- ⚠️ Headless mode requires installing the KNIME headless extension
- ⚠️ Workflows must be designed in the GUI beforehand
- 💡 Suitable for automated workflows, ETL, data mining, visual analytics

📋 Recommended usage:
  # Headless workflow execution
  knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="/path/to/workflow"
  # Execute with parameters
  knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="/path/to/workflow" -workflow.variable=myVar,value,String

---

## jamovi

- ⚠️ jamovi **has no pure CLI mode**; invocation pops up the GUI (unavoidable)
- ✅ Can call jamovi analysis modules in the background via the `jmv` R package (no GUI needed)
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- 💡 Suitable for descriptive statistics, Bayesian analysis, frequency analysis

**Pure CLI alternative (R script)**:
```r
library(jmv)
# Descriptive statistics
descriptives <- jmv::descriptives(data = mydata, vars = c("var1", "var2"))
# Chi-square test
chisq <- jmv::contTables(data = mydata, rows = "group", cols = "outcome")
```

📋 Recommended approach:
  Rscript jmv_script.R              # R script calling jmv package (recommended, no GUI)

---

## JASP

- ⚠️ JASP **has no pure CLI mode**; invocation pops up the GUI (unavoidable)
- ✅ Can call JASP analysis modules in the background via the `jaspTools` R package (no GUI needed)
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free
- 💡 Suitable for descriptive statistics, Bayesian analysis, exploratory analysis

**Pure CLI alternative (R script)**:
```r
library(jaspTools)
# Load JASP data
data <- jaspTools::readOSR("data.csv")
# Descriptive statistics
desc <- jaspTools::descriptives(data, variables = c("var1", "var2"))
```

📋 Recommended approach:
  Rscript jasp_script.R             # R script calling jaspTools package (recommended, no GUI)

---

## PSPP

- ✅ PSPP is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- ✅ Open source and free (SPSS alternative)
- ⚠️ Syntax compatible with SPSS, but some advanced features unsupported
- 💡 Suitable for descriptive statistics, regression, contingency tables, data cleaning

📋 Recommended usage:
  # Run .sps syntax
  pspp -o output.txt analysis.sps
  # Pipe mode
  pspp < analysis.sps
  # Output directly to file
  pspp analysis.sps -o output.html

---

## Mplus

- ✅ Mplus is a pure CLI tool, completely GUI-free, no splash screen
- ✅ Supports Windows and Mac
- ⚠️ License file required
- ⚠️ Syntax is distinctive, steep learning curve
- 💡 Suitable for SEM, latent class analysis (LCA/LPA), multilevel models, survival analysis

📋 Recommended usage:
  mplus model.inp
  # With output file
  mplus model.inp output.out

---

## AMOS

- ⚠️ AMOS **has no pure CLI mode**; invocation pops up the GUI (unavoidable)
- ✅ Can be called in the background via the IBM SPSS Amos Python extension (no GUI needed)
- 🔴 Windows only
- ⚠️ Requires SPSS Statistics license
- 💡 Suitable for SEM, path analysis, confirmatory factor analysis

**Background automation (write your own, outside this skill's automation scope)**:
- For background automation, use the official IBM SPSS Amos Python extension on your own (this skill does not drive it)
- This skill only provides **detection + manual GUI-launch guidance** (GUI-only, no automation)

📋 Recommended approach:
  # Manually launch GUI to open file (pops up, no automation)
  amos.exe model.amw

---

## Q (MRKS)

- ✅ Q (MRKS) supports QScript batch mode, completely GUI-free, no splash screen
- 🔴 Windows only
- ⚠️ Requires Q (MRKS) license
- 💡 Suitable for market-research questionnaire analysis, cross-tabs, statistical tests

📋 Recommended usage (Windows):
  REM Run QScript
  Q.exe /QScript "c:\scripts\analysis.qs"
  REM With log
  Q.exe /QScript "c:\scripts\analysis.qs" /Log "c:\logs\output.log"

---

## NCSS

```
✅ NCSS connection configuration complete!

📊 Configuration Information:
  - NCSS Version: [2024]
  - NCSS Executable: [NCSS.exe path]
  - Platform: Windows

⚠️ Important notes:
  1. NCSS supports batch mode via /B parameter
  2. Windows-only, no macOS/Linux support
  3. Suitable for medical statistics, sample size calculation, clinical data analysis

📋 Recommended usage:
  "NCSS.exe" /B "analysis.ncss"
```

---

## Origin (OriginLab)

```
✅ Origin connection configuration complete!

📊 Configuration Information:
  - Origin Version: [2025/2024/2023]
  - Origin Executable: [Origin95.exe or Origin97.exe path]
  - Platform: Windows

⚠️ Important notes:
  1. Origin supports LabTalk script batch processing via -h parameter
  2. Scientific graphing and data analysis software, over 1M users worldwide
  3. macOS CLI support is limited, Windows environment recommended
  4. Suitable for batch data processing, scientific figure generation, statistical analysis

📋 Recommended usage:
  "origin97.exe" -h "script.ogs"
```

---

## Generic Memory Template Format

If the software is not listed in this document, use the following generic template:

**English Memory Template**:
```
### [Software] Environment

- **Version**: [version]
- **Executable Path**: `[path]`
- **Batch Command Format**:
  ```bash
  [command]
  ```
- **Script Template**:
  ```[language]
  [code]
  ```
- **Common Errors & Solutions**:
  | Error | Cause | Solution |
  |-------|-------|---------|
  | [error1] | [cause] | [solution] |
- **Configuration Completion Notes**:
  - ✅ [benefit1]
  - ⚠️ [caution1]
```
