---
paths:
  - "dofiles/**/*.do"
  - "reports/**/*.qmd"
  - "scripts/**/*.py"
  - "scripts/**/*.m"
  - "dofiles/**/*.py"      # Python版pipeline也纳入
---

# Quality Gates & Scoring Rubrics

> 源自 codex-stata-for-economists (陈铸)，适配Python+Stata混合项目

## 阈值

| 分数 | 含义 | 动作 |
|:-----|:-----|:-----|
| < 60 | 质量太差 | 不提交，彻底重写 |
| 60-79 | 有改进空间 | 修正并重评后再提交 |
| **80-89** | **可接受** | ✓ 可以提交 |
| **90+** | **优秀** | ✓ 可以合并PR/发布 |

运行 `python scripts/quality_score.py <file>` 给单个文件打分。

---

## Stata `.do` 文件扣分表

| 严重程度 | 问题 | 扣分 |
|:---------|:-----|:----:|
| Critical | Stata `r(<n>)` 错误（最新日志中） | -100 |
| Critical | 硬编码绝对路径 (`cd "C:\..."`) | -25 |
| Critical | 缺少 `version` 版本锁定 | -15 |
| Critical | 缺少 `log using` / 无日志产出 | -15 |
| Major | 缺少文件头注释块 | -8 |
| Major | 涉及随机过程但缺少 `set seed` | -10 |
| Major | `varabbrev on`（或未设置 `set varabbrev off`） | -5 |
| Major | 循环内包含 `set more off` | -5 |
| Major | 魔数未用macro/local+注释 | -3/个（上限-15） |
| Major | 估计结果未 `est store` | -5 |
| Minor | 分节标注缺失或不一致 | -2 |
| Minor | 注释掉的死代码 | -2/个（上限-8） |
| Minor | 行 > 100字符（`///` 续行除外） | -1/行（上限-10） |
| Minor | 混用 `*` / `//` 注释风格 | -1 |

## Quarto 报告 (`reports/*.qmd`, Stata引擎)

| 严重程度 | 问题 | 扣分 |
|:---------|:-----|:----:|
| Critical | 渲染失败 | -100 |
| Critical | 数值结论无日志引用（违反日志校验协议） | -30/个 |
| Critical | 引用键损坏 | -15 |
| Critical | 缺少必需节（摘要/数据/方法/结果） | -10/节 |
| Major | 表格不是来自 `output/tables/` | -10 |
| Major | 图内联渲染（应当预构建） | -10 |
| Major | 陈旧输出引用（输出文件比do文件旧） | -5 |
| Minor | 叙述中未注释的长代码块 | -2 |

## Python 脚本扣分表

| 严重程度 | 问题 | 扣分 |
|:---------|:-----|:----:|
| Critical | 语法错误 | -100 |
| Critical | 硬编码绝对路径 | -25 |
| Major | 缺少模块docstring | -5 |
| Major | 面向用户的脚本无argparse | -5 |
| Minor | 行 > 100字符 | -1/行 |

## 复现容差阈值

| 量 | 容差 | 理由 |
|:---|:----:|:-----|
| 整数计数（N、样本量） | 精确 | 没有理由不同 |
| 点估计（系数） | < 0.01 绝对 / < 1% 相对 | 论文显示四舍五入 |
| 标准误 | < 0.05 绝对 / < 5% 相对 | 自助法/聚类变异 |
| p值 | 同一显著性星号级别 | 精确值可能不同 |
| 文中百分比 | < 0.1pp | 显示精度 |
| R² | < 0.005 | 显示精度 |

任何偏差记录在 `quality_reports/<project>_replication_report.md`。

## 执行

- **< 80：** 阻止提交，列出问题+文件名行号
- **80-89：** 允许提交，给出改进建议
- **≥ 90：** 可以合并PR/发布
- 用户可在commit message中附加相关说明覆盖评分

## 质量报告

仅在合并时生成（非每次提交）。使用 `templates/quality-report.md` 模板。
保存至 `quality_reports/merges/YYYY-MM-DD_<branch>.md`
