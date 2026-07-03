# Multi-Software Workflow Example / 多软件工作流示例

> This file demonstrates how to combine multiple statistical software in a single AI Agent workflow.
> 本文件演示如何在单个 AI Agent 工作流中组合使用多款统计软件。

---

## Scenario / 场景

**Research Question**: Analyze customer churn factors using historical code assets from R, SPSS, Stata, and SAS.

**研究问题**: 使用 R、SPSS、Stata、SAS 的历史代码资产分析客户流失因素。

---

## Workflow / 工作流

### Step 1: Data Preparation with R / 数据准备（R）

**Purpose**: Clean and prepare raw data using existing R scripts.
**目的**: 使用现有 R 脚本清理和准备原始数据。

```r
# test_r_cleaning.R (historical code asset)
library(dplyr)
library(tidyr)

data <- read.csv("raw_customer_data.csv", fileEncoding="UTF-8")

# Clean data
data_clean <- data %>%
  filter(!is.na(customer_id)) %>%
  mutate(churn = ifelse(churn_flag == 1, "Yes", "No")) %>%
  select(customer_id, age, tenure, monthly_charges, churn)

# Export for SPSS
write.csv(data_clean, "data_clean.csv", row.names=FALSE, fileEncoding="UTF-8")
```

**AI Agent command**:
```
Run R script test_r_cleaning.R to clean customer data
```

---

### Step 2: Descriptive Statistics with SPSS / 描述统计（SPSS）

**Purpose**: Generate descriptive statistics and visualizations using existing SPSS syntax.
**目的**: 使用现有 SPSS 语法生成描述性统计和可视化。

```spss
* test_spss_descriptive.sps (historical code asset)
GET FILE="data_clean.csv".

* Descriptive statistics
SUMMARY
  /VARIABLES=age tenure monthly_charges
  /FORMAT=LIST.

* Churn distribution
CROSSTABS
  /TABLES=churn BY contract_type
  /FORMAT=AVALUE.

* Export results
OUTPUT EXPORT
  /CONTENTS EXPORT=ALL
  /TYPE=HTML
  /FILE="desc_stats.html".
```

**AI Agent command**:
```
Run SPSS syntax test_spss_descriptive.sps
```

---

### Step 3: Regression Analysis with Stata / 回归分析（Stata）

**Purpose**: Run logistic regression using existing Stata do-files.
**目的**: 使用现有 Stata do-file 运行逻辑回归。

```stata
* test_stata_regression.do (historical code asset)
import delimited "data_clean.csv"

* Encode categorical variables
encode contract_type, gen(contract_num)
encode payment_method, gen(payment_num)

* Logistic regression
logit churn age tenure monthly_charges contract_num payment_num

* Odds ratios
logit, or

* Export results
outreg2 using "regression_results.doc", replace ctitle(Churn Model)
```

**AI Agent command**:
```
Run Stata do-file test_stata_regression.do
```

---

### Step 4: Report Generation with SAS / 报告生成（SAS）

**Purpose**: Generate final report with tables and charts using existing SAS macros.
**目的**: 使用现有 SAS 宏程序生成包含表格和图表的终期报告。

```sas
* test_sas_report.sas (historical code asset);
proc import datafile="data_clean.csv"
    out=customer_data
    dbms=csv
    replace;
run;

* Generate summary table;
proc means data=customer_data mean std min max;
    var age tenure monthly_charges;
    class churn;
    output out=summary_table;
run;

* Export to Excel;
proc export data=summary_table
    outfile="final_report.xlsx"
    dbms=xlsx
    replace;
run;

* Print completion message;
%put NOTE: ✅ Final report generated: final_report.xlsx;
```

**AI Agent command**:
```
Run SAS program test_sas_report.sas
```

---

## Complete Workflow Command / 完整工作流命令

In AI Agent conversation, you can trigger the entire workflow with natural language:

在 AI Agent 对话中，您可以用自然语言触发整个工作流：

```
Analyze customer churn factors:
1. Clean data with R (use test_r_cleaning.R)
2. Generate descriptive stats with SPSS (use test_spss_descriptive.sps)
3. Run regression with Stata (use test_stata_regression.do)
4. Generate final report with SAS (use test_sas_report.sas)
```

The AI Agent will execute these steps sequentially, passing data between software as needed.

AI Agent 将按顺序执行这些步骤，根据需要在不同软件之间传递数据。

---

## Key Benefits / 核心优势

| Benefit / 优势 | Description / 说明 |
|----------------|-------------------|
| 🔄 **Code Reuse / 代码复用** | Leverage historical assets without rewriting |
| 🔗 **Seamless Integration / 无缝集成** | AI Agent handles data passing between software |
| ⚡ **Efficiency / 高效** | Execute entire workflow in a single conversation |
| 📊 **Best Tool for Each Task / 任务最优工具** | Use R for cleaning, SPSS for stats, Stata for regression, SAS for reporting |

---

## Test These Scripts / 测试这些脚本

Use the test scripts in this directory to verify your software configuration:

使用本目录中的测试脚本验证您的软件配置：

| Script / 脚本 | Software | Command |
|--------|----------|---------|
| `test-syntax.sps` | SPSS Statistics | `stats.exe -syntax "test-syntax.sps"` |
| `test_r.r` | R | `Rscript --vanilla "test_r.r"` |
| `test_do.do` | Stata | `stata-mp -b do "test_do.do"` |
| `test_sas.sas` | SAS | `sas -sysin "test_sas.sas"` |

---

**📚 More Examples**: See [`ADDITIONAL_SOFTWARE.md`](./ADDITIONAL_SOFTWARE.md) for detailed use cases of all 31 supported software packages.
