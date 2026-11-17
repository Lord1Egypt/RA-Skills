---
paths:
  - "dofiles/**/*.do"
  - "data/**"
---

# Stata Coding Conventions

> 源自 codex-stata-for-economists (陈铸)

## Do File 标准结构

每个do文件应当按以下顺序组织：

```stata
* ===== File Header =====
* Analyis: 主回归分析 — Table 2, Columns 1-3
* Author:   [你的名字]
* Date:     2025-12-01
* Input:    data/derived/analysis_sample.dta
* Output:   output/tables/table2_main.tex
*           logs/03_analysis_main_regression.log

version 18
clear all
set more off
set varabbrev off
set seed 20251201

cap log close
log using "logs/03_analysis_main_regression.log", replace text

* ===== 1. Load data =====
use "data/derived/analysis_sample.dta", clear
```

## 文件名命名

- 使用有意义的名称，如 `01_clean_taxdata.do`, `02_construct_vars.do`
- 以数字前缀控制执行顺序：`01_`, `02_`, 等
- do文件不含空格或特殊字符

## 路径

- **始终使用相对路径**。以项目根目录为参考。
- 不写 `cd "C:\Users\..."`。用 `use "data/derived/sample.dta"` 替代。
- 数据写入和读取路径一致。

## 变量命名

- 英文名 lower_snake_case：`tax_revenue`, `evasion_rate`
- 避免Stata保留字：`_merge`, `_n`, `id`
- 标签中文：`label variable tax_revenue "应纳税额"`

## 日志规则

- 每个do文件开日志、关日志
- 使用 `text` 格式
- 日志放在项目根目录的 `logs/` 下
- 路径：`logs/<stage>_<name>.log`

## 结果保存

- 所有回归结果用 `estimates store` 或 `est store` 保存
- 表格用 `esttab` 导出 `.tex` 和 `.csv` 两种格式
- 图形用 `graph export` 输出 `.pdf` 和 `.png`

```stata
* 回归结果保存
reghdfe y treated $controls, absorb(id year) cluster(state_id)
est store m1

* 表格导出
esttab m1 m2 m3 using "output/tables/table2_main.tex", replace ///
    se star(* 0.1 ** 0.05 *** 0.01) ///
    label title("Main Results") ///
    stats(N r2, fmt(0 3))

* CSV版本（供log-validator和Python读取）
esttab m1 m2 m3 using "output/tables/table2_main.csv", replace ///
    se plain wide
```

## 注释

- 使用中文注释以方便理解
- 分节用 `=====` 标注
- 复杂计算步骤必须注释

## 参考

完整Stata语法参考见 `stata-skill` 技能或 `.claude/skills/stata/` 目录中的对应文件。
