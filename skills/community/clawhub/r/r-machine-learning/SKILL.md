---
name: r-machine-learning
metadata:
  openclaw:
    emoji: "🧬"
    requires:
      bins:
        - Rscript
    description: >
      全流程R机器学习工作台。覆盖caret/tidymodels建模、随机森林、XGBoost、LASSO、SVM、
      数据集划分、特征工程、特征筛选(Boruta/RFE/LASSO)、交叉验证(5折/10折)、超参调优
      (网格/随机/贝叶斯)、结果分析(ROC/校准曲线/SHAP可解释性)、生信专项(生存分析ML/
      差异表达分类/多组学)。输出可发表级图表和专业报告。
      Use when: user asks for R machine learning, R ML pipeline, caret, tidymodels,
      random forest in R, XGBoost in R, LASSO in R, SVM in R, cross-validation R,
      hyperparameter tuning R, SHAP R, ROC curve R, calibration curve R, feature selection R,
      Boruta R, RFE R, survival random forest R, survival ML R, compare models R.
---

# 🧬 R Machine Learning Workbench

## 概述

专业级 R 语言机器学习技能，专为生物医学/生信研究者设计。所有脚本由 R 原生执行，
输出结果为可直接用于论文的图表和报告。

## 触发词

R机器学习, R ML, caret建模, tidymodels, 随机森林R, XGBoost R, LASSO R, SVM R,
交叉验证R, 超参调优R, SHAP R, ROC曲线R, 校准曲线R, 特征筛选R, Boruta R,
生存分析ML, 差异表达分类, r machine learning, caret, random forest R, xgboost R

## 能力清单

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `install` | 安装所有依赖包 | 首次使用 |
| `split` | 数据划分(训练/验证/测试) | 任何建模前 |
| `explore` | 数据探索性分析 | 理解数据特点 |
| `feature_engineer` | 自动特征工程 | 数据预处理 |
| `feature_select` | 特征筛选(Boruta/RFE/LASSO) | 高维数据降维 |
| `rf` | 随机森林(回归/分类/生存) | 基线模型/复杂关系 |
| `xgboost` | XGBoost(回归/分类/生存) | 强预测/竞赛级 |
| `lasso` | LASSO回归(glmnet) | 高维稀疏/特征选择 |
| `svm` | SVM分类/回归 | 小样本/高维数据 |
| `tune` | 超参调优(网格/随机/贝叶斯) | 模型优化 |
| `cv` | 交叉验证(3/5/10折) | 模型评估 |
| `compare` | 多模型对比+统计检验 | 选最优模型 |
| `roc` | ROC曲线+PR曲线 | 二分类评价 |
| `calibration` | 校准曲线+HL检验 | 概率校准评价 |
| `shap` | SHAP可解释性分析 | 模型解释/特征重要性 |
| `survival` | 生存分析ML(RF-Survival/XGB-Cox) | 生存数据建模 |
| `pipeline` | 一键全流程 | 快速出结果 |
| `report` | 生成完整分析报告(HTML) | 可交付产出 |

## 依赖包

```r
# 核心建模
caret, tidymodels, glmnet, xgboost, randomForest, ranger, kernlab

# 特征选择
Boruta, FSelectorRFE

# 模型解释
fastshap, DALEX, DALEXtra, ingredients

# 评价
pROC, PRROC, rms, ResourceSelection

# 生存分析
survival, survminer, randomForestSRC, xgboost.surv

# 可视化
ggplot2, ggpubr, corrplot, pheatmap

# 报告
rmarkdown, knitr, DT, kableExtra

# 数据处理
dplyr, tidyr, recipes, rsample, workflows
```

## 脚本架构

```
scripts/
├── utils.R              # 通用工具函数
├── install_packages.R   # 依赖安装
├── data_split.R         # 数据划分
├── data_explore.R       # 探索性分析
├── feature_engineering.R # 特征工程
├── feature_selection.R  # 特征筛选
├── rf_model.R           # 随机森林
├── xgboost_model.R      # XGBoost
├── lasso_model.R        # LASSO
├── svm_model.R          # SVM
├── hyperparameter_tune.R # 超参调优
├── cross_validation.R   # 交叉验证
├── model_compare.R      # 模型对比
├── roc_analysis.R       # ROC分析
├── calibration.R        # 校准曲线
├── shap_analysis.R      # SHAP解释
├── survival_ml.R        # 生存ML
├── pipeline.R           # 全流程
└── report_generator.R   # 报告生成
```

## 使用示例

### 快速入门：一键全流程
#### Windows (PowerShell)
```powershell
# 1. 先安装依赖（仅首次）
.\scripts\launcher.ps1 install

# 2. 一键全流程
.\scripts\launcher.ps1 pipeline --data data.csv --target outcome --type classification --cv 5

# 3. 指定建模+调优
.\scripts\launcher.ps1 tune --data data.csv --target outcome --model xgboost --method bayesian
```

#### Linux/macOS (Bash)
```bash
bash scripts/launcher.sh install
bash scripts/launcher.sh pipeline --data data.csv --target outcome --type classification --cv 5
bash scripts/launcher.sh tune --data data.csv --target outcome --model xgboost --method bayesian
```

### 自定义步骤
#### Windows
```powershell
.\scripts\launcher.ps1 split --data data.csv --target outcome --ratio 0.7
.\scripts\launcher.ps1 feature_select --data train.csv --target outcome --method boruta
.\scripts\launcher.ps1 rf --data train.csv --target outcome --cv 5 --tune TRUE
.\scripts\launcher.ps1 shap --model model.rds --data test.csv
.\scripts\launcher.ps1 roc --preds predictions.csv --truth test.csv --outcome outcome
.\scripts\launcher.ps1 survival --data survival_data.csv --time time --event status --model rfsrc
.\scripts\launcher.ps1 report --data data.csv --target outcome
```

#### Linux/macOS
```bash
bash scripts/launcher.sh split --data data.csv --target outcome --ratio 0.7
bash scripts/launcher.sh feature_select --data train.csv --target outcome --method boruta
bash scripts/launcher.sh rf --data train.csv --target outcome --cv 5 --tune TRUE
bash scripts/launcher.sh shap --model model.rds --data test.csv
bash scripts/launcher.sh roc --preds predictions.csv --truth test.csv --outcome outcome
bash scripts/launcher.sh survival --data survival_data.csv --time time --event status --model rfsrc
bash scripts/launcher.sh report --data data.csv --target outcome
```

## 输出

所有输出保存到 `output/` 目录：
- `output/plots/` - 发表级图表(PDF/PNG/SVG)
- `output/models/` - 模型对象(.rds)
- `output/predictions/` - 预测结果(.csv)
- `output/reports/` - 分析报告(.html/.pdf)
- `output/tables/` - 结果表格(.csv/.tex)

## 数据要求

- 输入: CSV格式，行为样本，列为变量
- 分类目标: 二分类(factor, 0/1)，多分类(factor)
- 回归目标: 连续数值(numeric)
- 生存目标: time(数值) + event(0/1) 两列
- 无特殊字符列名，缺失值用NA表示

## 注意事项

⚠️ 需要R >= 4.0 已安装
⚠️ 首次使用需运行 install 命令安装依赖包（Windows: `.\scripts\launcher.ps1 install`）
⚠️ Windows 需要在 PATH 中加入 R：`C:\Program Files\R\R-4.6.0\bin\x64`（或其他R安装路径）
⚠️ 高维数据(p>>n)建议先用 LASSO 或 Boruta 筛选
⚠️ 大文件(>100MB)会明显增加处理时间
