# Additional Statistical Software Support

This file contains configuration information for additional statistical software in the `statsoft-cli` skill (core software SPSS Statistics, R, Stata, SAS see SKILL.md).

---

## Table of Contents

0. [Script Routing Tables](#script-routing-tables)
1. [AMOS](#amos)
2. [CmdStan](#cmdstan)
3. [EViews](#eviews)
4. [GenStat](#genstat)
5. [GraphPad Prism](#graphpad-prism)
6. [Gretl](#gretl)
7. [H2O.ai](#h2oai)
8. [JAGS](#jags)
9. [JASP](#jasp)
10. [JMP](#jmp)
11. [Julia](#julia)
12. [KNIME](#knime)
13. [LIMDEP](#limdep)
14. [Matlab](#matlab)
15. [Mathematica](#mathematica)
16. [Microfit](#microfit)
17. [Minitab](#minitab)
18. [Mplus](#mplus)
19. [NCSS](#ncss)
20. [NLOGIT](#nlogit)
21. [OpenBUGS](#openbugs)
22. [Orange](#orange)
23. [OriginLab Origin](#originlab-origin)
24. [OxMetrics](#oxmetrics)
25. [PSPP](#pspp)
26. [Q (MRKS)](#q-mrks)
27. [Rattle](#rattle)
28. [SHAZAM](#shazam)
29. [SPSS Modeler](#spss-modeler)
30. [Stat/Transfer](#stattransfer)
31. [Statistica](#statistica)
32. [Tanagra](#tanagra)
33. [TSP](#tsp)
34. [Weka](#weka)
35. [jamovi](#jamovi)

---

## Script Routing Tables

> **GUI Software Note**: The following software **have no CLI mode** — they launch a GUI and cannot run fully silent. This skill provides detection and manual-launch guidance only (you open the GUI yourself); it never auto-launches GUI applications and offers no batch automation.
> - **AMOS** — GUI only
> - **GraphPad Prism** — GUI only
> - **JASP** — Requires GUI
> - **jamovi** — Requires GUI

### Windows Only

| Software | Configuration Script | CLI Wrapper | Verify |
|----------|----------------------|-------------|--------|
| AMOS | `scripts/windows-only/AMOS/setup_amos.ps1` | — | Check install |
| EViews | `scripts/windows-only/EViews/setup_eviews.ps1` | `scripts/windows-only/EViews/statsoft-eviews.ps1` | `EViews.exe /?` |
| GraphPad | `scripts/windows-only/GraphPad/setup_graphpad.ps1` | — (GUI-only, no CLI wrapper) | No CLI (manual GUI launch to verify) |
| JMP | `scripts/windows-only/JMP/setup_jmp.ps1` | `scripts/windows-only/JMP/statsoft-jmp.ps1` | `JMP.exe /R "Exit();"` |
| LIMDEP | `scripts/windows-only/Limdep/setup_limdep.ps1` | — | `limdep commands.txt` |
| Mathematica | `scripts/windows-only/Mathematica/setup_mathematica.ps1` | `scripts/cross-platform/Mathematica/setup_mathematica.sh` | `wolframscript -code "Print[1]"` |
| Microfit | `scripts/windows-only/Microfit/setup_microfit.ps1` | — | `microfit commands.txt` |
| Minitab | `scripts/windows-only/Minitab/setup_minitab.ps1` | — | No CLI (manual GUI launch; `mtb.exe /run` opens GUI) |
| Mplus | `scripts/windows-only/Mplus/setup_mplus.ps1` | — | `mplus model.inp` |
| NCSS | `scripts/windows-only/NCSS/setup_ncss.ps1` | — | Check install |
| NLOGIT | `scripts/windows-only/NLOGIT/setup_nlogit.ps1` | — | `nlogit commands.txt` |
| Q (MRKS) | `scripts/windows-only/Q_MRKS/setup_q.ps1` | — | Check install |
| SHAZAM | `scripts/windows-only/SHAZAM/setup_shazam.ps1` | — | `shazam commands.txt` |
| SPSS Modeler | `scripts/windows-only/SPSS/setup_modeler.ps1` | — | `clemb -local -stream test.str -execute` |
| Statistica | `scripts/windows-only/Statistica/setup_statistica.ps1` | `scripts/windows-only/Statistica/statsoft-statistica.ps1` | `Statistica.exe /?` |
| Origin | `scripts/windows-only/Origin/setup_origin.ps1` | — | `origin97 -h test.ogs` |

### Cross-Platform

> **Note**: JASP and jamovi require GUI, cannot run in pure CLI silent mode.

| Software | Configuration Script | CLI Wrapper | Verify |
|----------|----------------------|-------------|--------|
| CmdStan | — | `scripts/cross-platform/CmdStan/setup_cmdstan.sh` | Check install |
| GenStat | — | `scripts/cross-platform/GenStat/setup_genstat.sh` | `genstat --help` |
| Gretl | — | `scripts/cross-platform/Gretl/setup_gretl.sh` | `gretlcli -v` |
| H2O.ai | — | `scripts/cross-platform/H2O/setup_h2o.sh` | `h2o --help` |
| JAGS | — | `scripts/cross-platform/JAGS/setup_jags.sh` | `jags scriptfile` |
| JASP | — | `scripts/cross-platform/JASP/setup_jasp.sh` | Check install |
| Julia | — | `scripts/cross-platform/Julia/setup_julia.sh` | `julia -v` |
| KNIME | — | `scripts/cross-platform/KNIME/setup_knime.sh` | Check install |
| Mathematica | — | `scripts/cross-platform/Mathematica/setup_mathematica.sh` | `wolframscript -code "Print[1]"` |
| Matlab | — | `scripts/cross-platform/Matlab/setup_matlab.sh` | `matlab -batch "exit"` |
| Minitab | — | `scripts/cross-platform/Minitab/setup_minitab.sh` | No CLI (manual GUI launch; `mtb.exe /run` opens GUI) |
| Mplus | — | `scripts/cross-platform/Mplus/setup_mplus.sh` | `mplus model.inp` |
| OpenBUGS | — | `scripts/cross-platform/OpenBUGS/setup_openbugs.sh` | `openbugs --help` |
| Orange | — | `scripts/cross-platform/Orange/setup_orange.sh` | `orange-canvas --help` |
| OxMetrics | — | `scripts/cross-platform/OxMetrics/setup_oxmetrics.sh` | `oxmetrics --help` |
| PSPP | — | `scripts/cross-platform/PSPP/setup_pspp.sh` | Check install |
| Rattle | — | `scripts/cross-platform/Rattle/setup_rattle.sh` | `rattle --cli` |
| SHAZAM | — | `scripts/cross-platform/SHAZAM/setup_shazam.sh` | `shazam commands.txt` |
| Stat/Transfer | `scripts/cross-platform/StatTransfer/setup_stattransfer.sh` | `scripts/windows-only/StatTransfer/statsoft-stattransfer.ps1` + `st` (built-in) | `st -v` |
| TSP | — | `scripts/cross-platform/TSP/setup_tsp.sh` | `tsp commands.txt` |
| Tanagra | — | `scripts/cross-platform/Tanagra/setup_tanagra.sh` | `tanagra --help` |
| Weka | — | `scripts/cross-platform/Weka/setup_weka.sh` | Check install |
| jamovi | — | `scripts/cross-platform/jamovi/setup_jamovi.sh` | Check install |

---

## AMOS

### Introduction

AMOS is a Structural Equation Modeling (SEM) software from the SPSS family, Windows-only. After installation, it can be found in the Start Menu, and displays a GUI when running.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ❌ (no CLI) | ⚠️⚠️⚠️ GUI only |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Configuration Completion Notes

- ⚠️⚠️⚠️ No CLI mode — GUI launches when called (unavoidable)
- 💡 Suitable for SEM, path analysis, confirmatory factor analysis

---

## CmdStan

### Introduction

CmdStan is the command-line interface for the Stan statistical platform, pure CLI support, completely splash-free, for Bayesian MCMC sampling.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- ✅ Suitable for Bayesian statistical modeling and MCMC sampling
- 💡 Can also use R `rstan` or Python `cmdstanpy` to call Stan

---

## EViews

### Introduction

EViews is an econometrics time series analysis software (Windows-only), has CLI support (batch mode), may have splash screen.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (batch mode) | ⚠️ May have splash screen |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Batch Command

```powershell
# Run EViews program file
"EViews.exe" "program.prg" /r
```

### Configuration Completion Notes

- ⚠️ EViews batch mode may have splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for time series analysis, regression, forecasting

---

## GenStat

### Introduction

GenStat is an agricultural statistics and data analysis software, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Suitable for agricultural statistics, experimental design, data analysis

---

## GraphPad Prism

### Introduction

GraphPad Prism is scientific graphing and statistical analysis software, **does not have a CLI mode** — calling it will launch the GUI (unavoidable).

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ❌ (no CLI) | ⚠️⚠️⚠️ GUI only |
| macOS | ✅ | ❌ (no CLI) | ⚠️⚠️⚠️ GUI only |
| Linux | ❌ | ❌ | — |

### Installation Paths

**Windows**:
- `C:\Program Files\GraphPad\Prism 8\prism.exe`
- `C:\Program Files\GraphPad\Prism 9\prism.exe`
- `C:\Program Files\GraphPad\Prism 10\prism.exe`

**macOS**:
- `/Applications/GraphPad Prism.app/Contents/MacOS/GraphPad Prism`

### How to Launch (manual GUI launch only, no CLI batch)

> ⚠️ GraphPad Prism **has no CLI mode** and cannot be run silently/batch via command line.
> This skill does **not** provide any `prism.exe` command-line call, and does **not create or modify** any GraphPad Prism project/data files (including `.pzfx`); only the following are supported:
> 1. Manually double-click to open the GUI (or the user launches it themselves);
> 2. The user operates their project/data files within GraphPad Prism themselves.

### ⚠️ Important Limitation

GraphPad Prism **has no CLI mode**, calling it will launch the GUI. This differs from SPSS (Production Facility), R (Rscript), Stata (batch mode).

### Alternatives

- ⚠️ This skill does NOT support any automation that creates or modifies `.pzfx` files in the background (including Python `prismWriter`); such operations are out of scope and must be performed manually by the user in their own GraphPad Prism environment.

### Configuration Completion Notes

- ⚠️⚠️⚠️ No CLI mode — GUI launches when called (unavoidable)
- 💡 This skill provides detection and manual-launch guidance only; it NEVER creates or modifies Prism `.pzfx` project/data files

---

## Gretl

### Introduction

Gretl is a free, cross-platform econometrics software with pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Batch Command

```bash
# Run script
gretlcli -b script.inp
```

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- ✅ Free software, suitable for econometrics analysis

---

## H2O.ai

### Introduction

H2O.ai is an automated machine learning platform, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Suitable for AutoML, deep learning, predictive analytics

---

## JAGS

### Introduction

JAGS (Just Another Gibbs Sampler) is a Bayesian MCMC sampling software, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Batch Command

```bash
jags scriptfile
```

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Suitable for Bayesian modeling, syntax compatible with WinBUGS/OpenBUGS

---

## JASP

### Introduction

JASP is an open-source statistical analysis software offering both classical and Bayesian statistical methods. Requires GUI to run.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ❌ (no pure CLI) | ⚠️⚠️⚠️ Requires GUI |
| macOS | ✅ | ❌ (no pure CLI) | ⚠️⚠️⚠️ Requires GUI |
| Linux | ✅ | ❌ (no pure CLI) | ⚠️⚠️⚠️ Requires GUI |

### Configuration Completion Notes

- ⚠️⚠️⚠️ JASP requires GUI, cannot fully avoid splash screen
- 💡 Suitable for academic research and teaching, user-friendly interface

---

## JMP

### Introduction

JMP is an interactive visualization statistical software by SAS, supports JSL script batch processing (`/R` parameter), may have brief splash screen (1-2 seconds) when running.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (`/R` parameter) | ⚠️ Brief (1-2 sec) |
| macOS | ✅ | ✅ (`/R` parameter) | ⚠️ Brief (1-2 sec) |
| Linux | ❌ | ❌ | — |

### Installation Paths

**Windows**:
- `C:\Program Files\SAS\JMP\JMP.exe`
- `C:\Program Files\JMP\JMP\JMP.exe`

**macOS**:
- `/Applications/JMP.app/Contents/MacOS/JMP`

### Batch Command

```powershell
# Windows
"JMP.exe" /R "script.jsl"

# macOS
JMP -R "script.jsl"
```

### JSL Script Template

```jsl
// script.jsl — JMP script
Clear Log();

// Read data
dt = Open("data.csv");

// Analysis
[AnalysisPlatform](
    Y(:column1),
    X(:column2)
);

// Save results
Save(dt, "results.jmp");
Close(dt, NoSave);

// Exit (batch mode)
Exit();
```

### ⚠️ Splash Screen Issue

JMP is a GUI application; even when using the `/R` batch mode, it may still display a startup splash screen when running. The splash screen lasts only briefly (1-2 seconds), and JMP will auto-close after the script finishes (if the script ends with `Exit();`).

### Notes

- ⚠️ **The script must end with `Exit();`**, otherwise the JMP GUI stays open
- **Compared with GraphPad**: GraphPad has no CLI at all, while JMP has a CLI (`/R` parameter) and supports batch processing

### Configuration Completion Notes

- ⚠️ JMP may show a brief splash screen (1-2 sec) when running, unavoidable
- ⚠️ The script must end with `Exit();`

---

## Julia

### Introduction

Julia is a high-performance scientific computing language, pure CLI support, completely splash-free, suitable for Bayesian statistics and high-performance computing.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Batch Command

```bash
julia script.jl
```

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- ✅ High performance, suitable for big data and complex statistical computing
- 💡 Common packages: Statistics, HypothesisTests, GLM, Turing (Bayesian)

---

## KNIME

### Introduction

KNIME is an open-source data analytics workflow platform, pure CLI support (execute workflows via command line), completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ CLI batch processing supported, completely GUI-free, no splash screen
- 💡 Suitable for visual workflow orchestration and automated data pipelines

---

## LIMDEP

### Introduction

LIMDEP is an econometrics and discrete choice analysis software (Windows-only), has CLI support, suitable for microeconometrics research.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Batch Command

```powershell
limdep commands.txt
```

### Configuration Completion Notes

- ✅ CLI support available, suitable for econometrics analysis
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for discrete choice and limited dependent variable models

---

## Mathematica

### Introduction

Mathematica is a mathematical computing and statistical analysis platform developed by Wolfram Research, pure CLI support (`wolframscript`), completely splash-free. Executes Wolfram Language scripts via command line, supporting symbolic computation, numerical analysis, statistical modeling, and visualization.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (`wolframscript.exe`) | ❌ |
| macOS | ✅ | ✅ (`wolframscript`) | ❌ |
| Linux | ✅ | ✅ (`wolframscript`) | ❌ |

### Batch Command

```bash
# Run Wolfram Language script
wolframscript -file script.wl

# Execute code directly
wolframscript -code "Table[i^2, {i, 10}]"

# Interactive REPL mode
wolframscript

# Windows explicit call (replaces MathKernel)
"C:\Program Files\Wolfram Research\Mathematica\14.0\MathKernel.exe" -noprompt < script.m
```

### Configuration Completion Notes

- ✅ Pure CLI tool (`wolframscript`), completely GUI-free, no splash screen
- ✅ Cross-platform support (Win/Mac/Linux)
- 💡 Suitable for symbolic mathematics, numerical analysis, statistical modeling, and visualization
- ⚠️ WolframScript requires a commercial license with periodic activation

---

## Matlab

### Introduction

Matlab is an engineering computation and statistics software, has CLI support (`-batch` mode), completely splash-free (when using `-batch` parameter).

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (`-batch`) | ❌ (with -batch) |
| macOS | ✅ | ✅ (`-batch`) | ❌ (with -batch) |
| Linux | ✅ | ✅ (`-batch`) | ❌ (with -batch) |

### Batch Command

```bash
# Run script (no GUI)
matlab -batch "run('script.m')"
```

### Configuration Completion Notes

- ✅ Completely GUI-free when using `-batch` parameter
- ⚠️ Requires Statistics and Machine Learning Toolbox
- 💡 Suitable for engineering statistics, signal processing, ML

---

## Microfit

### Introduction

Microfit is an econometrics time series analysis software (Windows-only), has CLI support.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Batch Command

```powershell
microfit commands.txt
```

### Configuration Completion Notes

- ✅ CLI support available, suitable for econometric time series
- ⚠️ Windows-only, no macOS/Linux support

---

## Minitab

### Introduction

Minitab is an industrial statistics and Six Sigma software. **`mtb.exe /run` does NOT run headless** — it launches the full Minitab GUI window (observed window title `Minitab - [Untitled]`), so it is not safe for agent-driven batch automation. Treat Minitab as a **GUI-only** tool: detect the install (path / version) and give a manual launch guide, exactly like AMOS / GraphPad / JASP / jamovi.

### Platform Support

| Platform | Supported | Headless CLI | Notes |
|----------|-----------|--------------|-------|
| Windows | ✅ | ❌ (`mtb.exe /run` opens GUI) | Detect + manual launch only |
| macOS | ⚠️ Limited | ❌ | Minitab Web App / remote desktop |
| Linux | ⚠️ Limited | ❌ | Minitab Web App / remote desktop |

### Configuration Completion Notes

- ⚠️ `mtb.exe /?` is NOT a help flag — it launches the Minitab GUI. Do not use it for detection.
- ⚠️ `mtb.exe /run "script.mtb"` opens the Minitab GUI and may hang waiting on the window; never call it from the agent.
- 💡 Suitable for quality control and Six Sigma projects; run analyses interactively in the Minitab GUI.

---

## Mplus

### Introduction

Mplus is a Structural Equation Modeling (SEM) and latent variable analysis software, has CLI support, suitable for complex statistical modeling.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ❌ | ❌ | — |

### Batch Command

```bash
mplus model.inp
```

### Configuration Completion Notes

- ✅ CLI support available, suitable for SEM and latent variable analysis
- 💡 Suitable for multilevel, growth, mixture models

---

## NCSS

### Introduction

NCSS is a statistical analysis software (Windows-only), has CLI support (batch mode), suitable for medical statistics, sample size calculation, etc.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (batch mode) | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Configuration Completion Notes

- ✅ CLI support available, suitable for statistical analysis
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for medical statistics, sample size calculation, data analysis

---

## NLOGIT

### Introduction

NLOGIT is a discrete choice econometrics software (Windows-only), has CLI support, an extended version of LIMDEP.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Batch Command

```powershell
nlogit commands.txt
```

### Configuration Completion Notes

- ✅ CLI support available, suitable for discrete choice analysis
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for Logit, Probit, Mixed Logit models

---

## OpenBUGS

### Introduction

OpenBUGS is an open-source Bayesian MCMC sampling software, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Suitable for Bayesian modeling, open-source WinBUGS alternative

---

## Orange

### Introduction

Orange is an open-source visual data mining and ML software, has CLI support (Python-based), may display graphical interface when running.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ⚠️ May have |
| macOS | ✅ | ✅ | ⚠️ May have |
| Linux | ✅ | ✅ | ⚠️ May have |

### Configuration Completion Notes

- ⚠️ CLI support available, but some operations may involve GUI
- 💡 Suitable for visual data mining, ML, data exploration

---

## OriginLab Origin

### Introduction

Origin is a professional scientific graphing and data analysis software with over 1 million users worldwide, deeply embedded in Chinese research institutions. Supports LabTalk script batch processing, can execute data analysis tasks via command line.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (LabTalk script) | ❌ |
| macOS | ✅ | ⚠️ Limited | ⚠️ May have |
| Linux | ❌ | ❌ | — |

### Installation Paths

**Windows**:
- `C:\Program Files\OriginLab\Origin2025\Origin95.exe`
- `C:\Program Files\OriginLab\Origin2024\Origin95.exe`

### Batch Command

```powershell
# Windows — run LabTalk script
"origin97" -h "script.ogs"

# Or compile and execute via Origin C
```

### Configuration Completion Notes

- ✅ LabTalk CLI support, completely GUI-free (-h mode)
- ✅ Over 1M users worldwide, widely used in Chinese research institutions
- 💡 Suitable for scientific graphing, data analysis, batch figure generation

---

## OxMetrics

### Introduction

OxMetrics is an econometrics software suite, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Suitable for econometrics, financial time series, predictive modeling

---

## PSPP

### Introduction

PSPP is an open-source alternative to SPSS, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Open-source, SPSS syntax compatible

---

## Q (MRKS)

### Introduction

Q (MRKS) is a market research analysis software (Windows-only), supports CLI mode for market research analytics.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Configuration Completion Notes

- ✅ CLI support available, suitable for market research analysis
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for survey analysis, statistical testing, report generation

---

## Rattle

### Introduction

Rattle is a visual data mining interface for R, has CLI support (`--cli` mode), suitable for data mining tasks.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ CLI support available (`--cli` mode), completely GUI-free
- 💡 Suitable for data exploration, statistical analysis, ML modeling

---

## SHAZAM

### Introduction

SHAZAM is an econometrics software, has CLI support, suitable for economic statistics and econometric analysis.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Batch Command

```bash
shazam commands.txt
```

### Configuration Completion Notes

- ✅ CLI support available, completely GUI-free, no splash screen
- 💡 Suitable for econometrics, statistical analysis, data processing

---

## SPSS Modeler

### Introduction

SPSS Modeler is IBM's data mining and predictive analytics software (Windows-only), executes .str stream files via the `clemb.exe` command-line tool.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (`clemb.exe`) | ❌ |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Installation Paths

**Windows**:
- `C:\Program Files\IBM\SPSS\Modeler\18.0\clemb.exe`

### Batch Command

```powershell
# Execute stream file in local mode
clemb -local -stream "model.str" -execute

# Python script mode
clemb -local -pyscript "script.py" -execute
```

### Configuration Completion Notes

- ✅ Pure CLI execution via `clemb.exe`, completely GUI-free, no splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for data mining, predictive modeling, ML pipelines

---

## Stat/Transfer

### Introduction

Stat/Transfer is a pure CLI data format conversion tool, completely GUI-free, suitable for automation. Supports format conversion between Stata, SPSS, SAS, R, Excel, etc.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Command Line Format

```bash
# Single-file conversion
"[ST_EXE_PATH]" in.sas7bdat out.dta

# Batch conversion
"[ST_EXE_PATH]" in\*.sav out\*.dta

# Command-file batch
"[ST_EXE_PATH]" myfile.stcmd
```

### Supported Formats

| Format | Extension |
|--------|-----------|
| Stata | `.dta` |
| SPSS | `.sav`, `.por` |
| SAS | `.sas7bdat`, `.xpt` |
| R | `.rda`, `.rds` |
| Excel | `.xlsx`, `.xls` |
| CSV | `.csv`, `.tsv` |

### Role in AI Workflow

```
Historical data (.sas7bdat)
      ↓  Stat/Transfer CLI
Intermediate format (.dta / .sav / .csv)
      ↓  R / Stata / SPSS CLI
Analysis results
      ↓  Stat/Transfer CLI
Delivery format (.xlsx / .sas7bdat)
```

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, suitable for automation
- 💡 Role in AI workflow: data format conversion bridge

---

## Statistica

### Introduction

Statistica is a data mining and machine learning software (Windows-only), has CLI support (SVB script batch processing), may have splash screen.

> ⚠️ **Detection-only + manual guidance (SDI-1 safety boundary)**: `setup_statistica.ps1` is detection-only and never writes `config.json`. Executing an SVB script goes through the guarded runner `statsoft-statistica.ps1` with a `Test-UserAuthorizedToRun` gate (same as SPSS/R runners).

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ (SVB script) | ⚠️ May have splash screen |
| macOS | ❌ | ❌ | — |
| Linux | ❌ | ❌ | — |

### Detection & Manual-Guidance Notes

- ⚠️ `setup_statistica.ps1` detection-only, writes no config.json
- ⚠️ Executing an SVB requires the guarded runner + explicit confirmation
- ⚠️ Statistica batch mode may have splash screen
- ⚠️ Windows-only, no macOS/Linux support
- 💡 Suitable for data mining, ML, statistical analysis

---

## Tanagra

### Introduction

Tanagra is an open-source data mining and ML software, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Open-source, suitable for data mining and ML teaching/research

---

## TSP

### Introduction

TSP is a time series and econometrics software, has CLI support, suitable for time series analysis and econometric modeling.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Batch Command

```bash
tsp commands.txt
```

### Configuration Completion Notes

- ✅ CLI support available, completely GUI-free, no splash screen
- 💡 Suitable for time series analysis, econometrics, financial modeling

---

## Weka

### Introduction

Weka is an open-source machine learning and data mining software, pure CLI support, completely splash-free.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ✅ | ❌ |
| macOS | ✅ | ✅ | ❌ |
| Linux | ✅ | ✅ | ❌ |

### Configuration Completion Notes

- ✅ Pure CLI tool, completely GUI-free, no splash screen
- 💡 Open-source, suitable for ML, data mining, predictive analytics

---

## jamovi

### Introduction

jamovi is an open-source statistical analysis software with a spreadsheet-style data analysis interface. Requires GUI to run.

### Platform Support

| Platform | Supported | CLI Support | Splash Screen |
|----------|-----------|-------------|---------------|
| Windows | ✅ | ❌ (no pure CLI) | ⚠️⚠️⚠️ Requires GUI |
| macOS | ✅ | ❌ (no pure CLI) | ⚠️⚠️⚠️ Requires GUI |
| Linux | ✅ | ❌ (no pure CLI) | ⚠️⚠️⚠️ Requires GUI |

### Configuration Completion Notes

- ⚠️⚠️⚠️ jamovi requires GUI, cannot fully avoid splash screen
- 💡 Open-source, user-friendly, suitable for academic research and teaching

---
