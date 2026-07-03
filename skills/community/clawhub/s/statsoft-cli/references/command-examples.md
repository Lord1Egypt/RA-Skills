# 命令调用示例 / Command Invocation Examples

> 本文档由 SKILL.md 精简时拆出，包含各统计软件的 CLI 调用命令示例。
> This document contains CLI command invocation examples for each statistical software.package.

---

## 目录 / Table of Contents

1. [R 命令示例](#r)
2. [SPSS 命令示例](#spss)
3. [Stata 命令示例](#stata)
4. [SAS 命令示例](#sas)
5. [JMP 命令示例](#jmp)
6. [GraphPad Prism 命令示例](#graphpad)
7. [Stat/Transfer 命令示例](#stattranfer)
8. [其他软件](#others)
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

### 基本运行

```bash
# 运行 R 脚本
Rscript --vanilla "script.R"

# 使用 R CMD BATCH（生成 .Rout 文件）
R CMD BATCH "script.R" "output.Rout"
```

### 静默安装包

```bash
Rscript -e "install.packages('pkg', repos='https://cran.r-project.org', quiet=TRUE)"
```

### 批处理脚本模板

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

### 常见场景

```bash
# 读取 SPSS .sav 文件
Rscript -e "library(haven); df <- read_sav('data.sav'); print(head(df))"

# 生成 HTML 报告
Rscript -e "rmarkdown::render('report.Rmd', output_file='report.html')"

# 大数据处理
Rscript -e "library(arrow); df <- read_parquet('big_data.parquet'); print(dim(df))"
```

---

## SPSS

### 🎯 使用建议 / Usage Recommendation

> **日常跑复杂语法** → **用方案 1**（`stats.com` + `.spj`，万无一失）
>
> **方案 2**（Python 内部驱动）**只能跑纯分析语法**，**不能包含**以下命令：
> - ❌ `OUTPUT SAVE`
> - ❌ `OUTPUT EXPORT` / `OUTPUT DISPLAY`
> - ❌ `HOST COMMAND`
> - ❌ `XDATA` / `XSAVE`（涉及 OUTPUT 对象时）
>
> —— 遇到不确定是否涉及 OUTPUT/SAVE 的命令时，统一走方案 1（`.spj`）更安全。

---

### ⭐ 首选方式（完全无闪屏）

通过 SPSS 内置 Python 的 `spss` 模块直接运行：

```bash
# 通过 spss_helper.py 调用
"C:\Program Files\IBM\SPSS\Statistics\XX\Python3\python.exe" \
  "C:\path\to\statsoft-cli\windows-only\SPSS\spss_helper.py" \
  run-internal "C:\path\to\syntax.sps"
```

**调用链路**：
```
AI Agent (Bash 工具)
  → python.exe spss_helper.py run-internal <sps_file>
      → subprocess.run([stats_python_path, helper_script], creationflags=0x08000000)
          → SPSS 后台执行（零窗口）
```

### 备用方式

通过 `stats.com`（控制台版）运行 .spj 文件（完全无闪屏）：

```bash
"C:\Program Files\IBM\SPSS\Statistics\XX\stats.com" -production silent -nologo "job.spj"
```

或使用 `stats.exe`（GUI 版，可能有闪屏）：

```bash
"C:\Program Files\IBM\SPSS\Statistics\XX\stats.exe" -production "job.spj" silent -nologo
```

### .spj 文件 XML 结构

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
  <output outputFormat="viewer" outputPath="输出文件.spv"/>
  <syntax syntaxPath="语法文件.sps"/>
</job>
```

**关键**：`<output>` 元素不能缺少，否则会报 NullPointerException

### 自动化 Python 脚本（完全无 GUI）

```python
import sys, os

# 1. 配置路径
spss_python_path = r"C:\Program Files\IBM\SPSS\Statistics\XX\Python3\python.exe"
sps_file = r"项目目录\analysis.sav"
output_sav = r"项目目录\results.sav"

# 2. 生成 SPSS 语法
sps_syntax = """
GET FILE='data.sav'.
COMPUTE new_var = var1 + var2.
SAVE OUTFILE='{out}'.
""".format(out=output_sav.replace("\\", "/"))

# 3. 通过 SPSS 内置 Python 运行（完全无 GUI）
spss_pkg = os.path.join(os.path.dirname(spss_python_path), "Lib", "site-packages")
sys.path.insert(0, spss_pkg)

import spss
spss.StartSPSS()
print("SPSS 处理器已启动（无 GUI）")

# 提交语法
spss.Submit(sps_syntax)
print("语法执行完成")

spss.StopSPSS()
print("SPSS 处理器已停止")

# 4. 读取结果（使用 Anaconda Python 的 pyreadstat）
import pyreadstat
df, meta = pyreadstat.read_sav(output_sav)
print(df.head())
```

---

## SPSS Modeler

### 批处理执行 .str 流文件

```powershell
# 通过 statsoft-modeler CLI
statsoft-modeler run "C:\path\to\churn_model.str"

# 或直接调用 clemb.exe
& "C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe" -local -stream "churn_model.str" -log "run.log" -execute
```

### Python 脚本模式（推荐）

```powershell
# 执行 Python 脚本（在 Modeler 会话中运行）
statsoft-modeler run-script "C:\path\to\train_model.py"

# 等价于 clemb 命令
& "C:\Program Files\IBM\SPSS\Modeler\18.0\bin\clemb.exe" -local `
    -script "train_model.py" -scriptlang python `
    -log "train.log" -execute
```

### 服务器模式（需 Modeler Server）

```powershell
statsoft-modeler server-run "stream.str" -hostname modeler-srv -port 80 `
    -username admin -password secret
```

### Python 脚本示例（在 Modeler 中运行）

```python
# train_model.py — SPSS Modeler Python 脚本
import modeler.api

# 获取当前会话
session = modeler.api.GetSession()

# 加载流文件
stream = session.LoadStream("churn_model.str")

# 设置参数
stream.SetVariable("data_path", "C:/data/customer.csv")

# 执行流
stream.Execute()

# 导出结果
output_node = stream.FindNode("table_output")
output_node.Export("C:/output/results.csv")
```

---

## Stata

### ⚠️ 版本与参数对照表

| 版本 | Windows 静默参数 | Mac/Linux 静默参数 |
|------|-----------------|-------------------|
| **Stata ≤ 12** | `StataMP /e do "script.do"` | `stata-mp -e do "script.do"` |
| **Stata ≥ 13** | `StataMP /b do "script.do"` | `stata-mp -b do "script.do"` |

**关键**：Stata 12 用 `-e`，Stata 13+ 用 `-b`。用错版本参数会弹确认框！

### 基本批处理示例

```bash
# Stata 13+ (Windows)
"C:\Program Files\Stata17\StataMP-64.exe" /b do "script.do"

# Stata 13+ (Mac/Linux)
stata-mp -b do "script.do"

# Stata 12 及更早 (Windows) — 不支持 /b！
"C:\Program Files\Stata12\StataMP.exe" /e do "script.do"

# Stata 12 及更早 (Mac/Linux) — 不支持 -b！
stata-mp -e do "script.do"
```

### 版本与可执行文件对照

| 版本 | MP | SE | BE |
|------|----|----|-----|
| Stata 12 及更早 | `StataMP` | `StataSE` | `Stata` |
| Stata 14/15 | `StataMP` | `StataSE` | `Stata` |
| Stata 16+ | `StataMP-64.exe` | `StataSE-64.exe` | `Stata-64.exe` |

### do-file 模板

```stata
* script.do — Stata 批处理脚本
cd "工作目录"
use "data.dta", clear
regress y x1 x2
save "results.dta", replace
log using "results.log", replace
summarize
log close
```

---

## SAS

### 基本批处理

```bash
# Windows
"C:\Program Files\SASFoundation\9.4\sas.exe" -sysin "prog.sas" -log "out.log" -print "out.lst"

# Mac/Linux
sas -sysin "prog.sas" -log "out.log" -print "out.lst"
```

### SAS 程序模板

```sas
* prog.sas — SAS 批处理程序;
options ls=80 ps=60 nodate nonumber encoding='utf-8';

* 读取数据;
data work.data;
    infile "data.csv" dlm=',' firstobs=2;
    input var1 var2 var3;
run;

* 分析;
proc reg data=work.data;
    model y = var1 var2;
run;

* 保存结果;
proc export data=work.result
    outfile="results.csv"
    dbms=csv replace;
run;
```

---

## JMP

### 基本批处理

```powershell
# 批处理模式（可能有短暂闪屏 1-2秒）
& "C:\Program Files\JMP\16\JMP.exe" /R "script.jsl"
```

⚠️ JMP 脚本末尾必须加 `Exit();`

### JSL 脚本模板

```jsl
// script.jsl — JMP 批处理脚本
dt = Open("data.jmp");
dt << Fit Y( :Y Column ) X( :X Column );
Save PDF("report.pdf");
Close(dt, "Yes");
Exit();
```

---

## GraphPad Prism

⚠️ **重要限制**：GraphPad Prism **没有 CLI 模式**，调用时**会弹出 GUI**，无法避免。

```powershell
# ⚠️ 会弹出 GUI 界面
& "C:\Program Files\GraphPad\Prism 9\prism.exe" "file.pzfx"
```

### 替代方案：Python prismWriter

```python
# 使用 prismWriter 后台操作 .pzfx 文件（无需 GUI）
from prismwriter import Project

p = Project("template.pzfx")
# 写入数据、执行分析...
p.save("output.pzfx")
```

---

## StatTransfer

### 单文件转换

```bash
# SPSS → Stata
st in.sav out.dta

# CSV → SPSS
st in.csv out.sav

# SAS → R
st in.sas7bdat out.rda
```

### 批量转换

```bash
# 批量转换目录下所有 .sav 为 .dta
st in\*.sav out\*.dta

# 命令文件批处理
st myfile.stcmd
```

---

## 其他软件

### Gretl

```bash
# 批处理运行 gretl 脚本
gretlcli -b script.inp
```

### Mathematica

```bash
# 运行 Wolfram Language 脚本
wolframscript -file script.wl

# 直接执行代码
wolframscript -code "Table[i^2, {i, 10}]"

# 加载数据并分析
wolframscript -code "data = Import[\"data.csv\"]; Mean[data]"

# 符号计算
wolframscript -code "D[x^3 + 2x^2 + 5, x]"

# 统计建模
wolframscript -code "data = RandomVariate[NormalDistribution[], 1000]; DistributionFitTest[data, Automatic]"

# 生成图片
wolframscript -code "p = Plot[Sin[x], {x, 0, 6 Pi}, PlotLabel -> \"Sine Wave\"]; Export[\"sine.png\", p]"

# Windows 显式调用 MathKernel（替代 wolframscript）
"C:\Program Files\Wolfram Research\Mathematica\14.0\MathKernel.exe" -noprompt < script.m
```

### Minitab

```powershell
# 基本批处理
& "C:\Program Files\Minitab\Minitab 21\Minitab.exe" /P "macro.mtb"
```

### Matlab

```bash
# 完全无 GUI 批处理
matlab -batch "run('script.m'); exit"
```

### Julia

```bash
julia script.jl
```

### EViews

```powershell
# EViews 批处理
& "C:\Program Files\QMS\EViews 12\EViews12_x64.exe" /b "program.prg"
```

### Statistica

```powershell
# Statistica Visual Basic 脚本
& "C:\Program Files\StatSoft\Statistica 13\Statistica.exe" /s "script.svb"
```

---

## JAGS

### 基本批处理

```bash
# 运行 JAGS 脚本
jags scriptfile

# 批量执行
jags-script script.txt

# 通过 R 接口
Rscript -e "library(rjags); jags.model('script.dat', data)"
```

---

## SHAZAM

### 基本批处理

```bash
# 运行 SHAZAM 命令文件
shazam commands.txt

# 示例命令文件:
# /MODEL TITLE MYMODEL
# / X 1 100
# / PREDICT Y
# /END
```

---

## OxMetrics

### 基本批处理

```bash
# 显示 CLI 选项
oxmetrics --help

# 运行批处理
oxmetrics -b commands.txt
```

---

## TSP

### 基本批处理

```bash
# 运行 TSP 命令文件
tsp commands.txt
```

---

## Tanagra

### 基本批处理

```bash
# 显示 CLI 选项
tanagra --help

# 执行批处理脚本
tanagra -f script.txt
```

---

## Orange

### Python 模块方式（推荐）

```bash
# 通过 Python 模块
python3 -m Orange.canvas

# 安装
pip install orange3
# 或
conda install -c conda-forge orange3
```

---

## H2O.ai

### Python 方式（推荐）

```bash
# 启动 H2O 服务器
h2o start

# 通过 Python
python3 -c "import h2o; h2o.init()"

# 安装
pip install h2o
```

---

## GenStat

### 基本批处理

```bash
# 运行 GenStat 命令文件
genstat commands.txt
```

---

## Rattle

### CLI 模式

```bash
# CLI 模式
rattle --cli

# 通过 R 包
Rscript -e "library(rattle); rattle()"
```

---

## OpenBUGS

### 基本批处理

```bash
# 显示帮助
openbugs --help

# 批处理执行
openbugs -b script.txt
```

---

## LIMDEP

### 基本批处理

```batch
REM 运行 LIMDEP 命令文件
limdep commands.txt
```

---

## NLOGIT

### 基本批处理

```batch
REM 运行 NLOGIT 命令文件
nlogit commands.txt
```

---

## Microfit

### 基本批处理

```batch
REM 运行 Microfit 命令文件
microfit commands.txt
```

---

## NCSS

### 基本批处理

```batch
REM 运行 NCSS 批处理分析
"NCSS.exe" /B "analysis.ncss"

REM 生成 NCSS 报告
"NCSS.exe" /B "report.ncss"
```

### 分析脚本模板

```
[Analysis]
Procedure = Descriptive Statistics
Variables = Age, Height, Weight

[Output]
Export = "results.html"
```

---

## Origin (OriginLab)

### 运行 LabTalk 脚本

```batch
REM 运行 LabTalk 批处理脚本
"C:\Program Files\OriginLab\Origin2025\origin97.exe" -h "script.ogs"
```

### LabTalk 脚本模板

```labtalk
// script.ogs — Origin LabTalk 脚本
impASC fname:="C:\data\data.csv";
range rr = col(1);
integ1 rr;
type "Mean: $(mean(rr))";
doc -e P "C:\output\result.png";
exit;
```
