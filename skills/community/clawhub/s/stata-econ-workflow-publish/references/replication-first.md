---
paths:
  - "dofiles/**/*.do"
  - "templates/replication-targets.md"
  - "quality_reports/**"
---

# Replication-First Protocol

> 源自 codex-stata-for-economists (陈铸)

**核心原则：** 在扩展之前，先将原始结果精确复现到逐点。如果基线不对，任何扩展都没有意义。

---

## Phase 1: 清点与基线

在写任何do文件之前：

- [ ] 阅读论文的复现README
- [ ] 清点复现包：语言（Stata / R / Matlab等）、数据文件、脚本、输出
- [ ] 将黄金标准数字记录在 `templates/replication-targets.md` → 保存到 `quality_reports/<paper>_replication_targets.md`：

```markdown
## 复现目标: [论文作者 (年份)]

| 目标 | 表/图 | 值 | SE/CI | 备注 |
|:-----|:------|:--:|:-----:|:-----|
| 主ATT | Table 2, Col 3 | -1.632 | (0.584) | 主规范，州层面聚类 |
| 一阶段F | Table 3, Panel A | 28.4 | — | 弱工具变量检验 |
| 样本量 | Table 1 | 12,453 | — | 所有限制后 |
```

- [ ] 标记每个目标为 MUST / SHOULD / MAY

---

## Phase 2: 翻译与执行

- [ ] 所有do文件遵循 `stata-coding-convention.md`
- [ ] 初始阶段**逐行翻译**——不要在复现时"改进"
- [ ] 精确匹配原始规范：协变量、样本限制、聚类、标准误方法、权重
- [ ] 所有中间结果作为 `.dta` 保存在 `data/derived/`（gitignored）

### 常见翻译陷阱

#### Stata → Stata (不同包版本)

| Stata | 陷阱 |
|:------|:-----|
| `xtreg ... fe` vs `reghdfe` | `xtreg` 使用不同于 `reghdfe` 默认的小样本调整 |
| `cluster()` 新旧版本 | df调整有变化；锁定命令版本 |
| `bootstrap` vs `boottest` | 两阶段wild-cluster与pairs bootstrap在小聚类数量下SE不同 |
| `areg` vs `reghdfe` | 去均值方法略有差异；检查 `reghdfe` 的 `dofadjustments()` 选项 |

#### Stata ↔ R

| Stata | R等价 | 陷阱 |
|:------|:------|:-----|
| `reg y x, cluster(id)` | `feols(y ~ x, cluster = ~id)` (`fixest`) | Stata的df调整不同于 `lmtest::coeftest` |
| `areg y x, absorb(id)` | `feols(y ~ x \| id)` | 检查去均值方法 |
| `probit` for PS | `glm(family = binomial(link = "probit"))` | R某些命令的默认链接是logit |
| `bootstrap, reps(999)` | `boot::boot()` | 精确匹配种子、次数和类型 |

#### Stata ↔ Python

| Stata | Python等价 | 陷阱 |
|:------|:-----------|:-----|
| `reg y x, robust` | `statsmodels.OLS(...).fit(cov_type="HC1")` | Stata用HC1；`linearmodels` 默认HC0 |
| `xtreg ... fe` | `linearmodels.PanelOLS(entity_effects=True)` | df调整差异 |

---

## Phase 3: 验证匹配

使用 `quality-gates.md` 中的容差。超出容差：

**不要进行扩展。** 定位差异来源：

1. 样本量——检查 `keep`/`drop` 顺序和缺失值处理
2. 标准误计算——检查聚类层级、df调整、权重
3. 默认选项——许多命令在Stata各版本间默认值发生变化
4. 变量定义——对数零值处理、winsorization、顶编码

将调查结果记录在复现报告中 **即使未解决**。一个未复现的结果是有信息量的；一个掩盖的差异是欺诈。

### 复现报告

保存到 `quality_reports/<paper>_replication_report.md`：

```markdown
# 复现报告: [论文作者 (年份)]
**日期:** [YYYY-MM-DD]
**原始语言:** [Stata 15 / R 4.x / 等]
**我们的实现:** dofiles/<path>

## 摘要
- **已检查/通过/失败的目标:** N / M / K
- **总体评估:** [已复现 / 部分复现 / 失败]

## 结果对比
| 目标 | 论文 | 我们的 | 差异 | 状态 |

## 差异（如有）
- **目标:** X
  - **调查:** ...
  - **解决方案:** [已解决 / 未解决（有假设）]

## 环境
- Stata版本+类型（来自 `logs/00_master_environment.log`）
- 关键用户命令及其版本
- 数据来源+版本
```

---

## Phase 4: 然后扩展

复现验证通过后（所有 MUST 目标 PASS）：

- [ ] 提交复现：`Replicate <Paper> Tables 2–4: all targets within tolerance`
- [ ] 用项目特定修改扩展（替代估计量、新结果、稳健性检验）
- [ ] 每个扩展建立在已验证的基线上
- [ ] 如果扩展的结果在精神上与复现基线相悖，那就是一个值得理解的研究发现——而不是要压制的bug
