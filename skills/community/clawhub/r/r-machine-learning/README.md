# 🧬 R Machine Learning Workbench

## 速查

```bash
# 首次使用
bash scripts/launcher.sh install

# 全流程一键
bash scripts/launcher.sh pipeline --data data.csv --target outcome [--type classification/regression]

# 分步执行
bash scripts/launcher.sh split --data data.csv --target outcome
bash scripts/launcher.sh rf --data train.csv --target outcome --tune TRUE
bash scripts/launcher.sh xgboost --data train.csv --target outcome --tune TRUE
bash scripts/launcher.sh compare --data data.csv --target outcome --models rf,xgboost,lasso,svm
bash scripts/launcher.sh roc --preds predictions.csv --truth test.csv --outcome outcome
bash scripts/launcher.sh shap --model output/models/rf_model.rds --data test.csv --target outcome

# 生存分析
bash scripts/launcher.sh survival --data survival.csv --time time --event status --model rfsrc

# 超参调优
bash scripts/launcher.sh tune --data train.csv --target outcome --model xgboost --method bayesian

# 交叉验证
bash scripts/launcher.sh cv --data data.csv --target outcome --model rf --k 10
```

## 文件结构
```
skills/r-machine-learning/
├── SKILL.md                 # 使用文档
├── scripts/
│   ├── launcher.sh          # 入口脚本
│   ├── utils.R              # 工具函数
│   ├── install_packages.R   # 依赖安装
│   ├── data_split.R         # 数据划分
│   ├── data_explore.R       # 探索性分析
│   ├── feature_engineering.R # 特征工程
│   ├── feature_selection.R  # 特征筛选
│   ├── rf_model.R           # 随机森林
│   ├── xgboost_model.R      # XGBoost
│   ├── lasso_model.R        # LASSO/Elastic Net
│   ├── svm_model.R          # SVM
│   ├── hyperparameter_tune.R # 超参调优
│   ├── cross_validation.R   # 交叉验证
│   ├── model_compare.R      # 模型对比
│   ├── roc_analysis.R       # ROC/PR曲线
│   ├── calibration.R        # 校准曲线
│   ├── shap_analysis.R      # SHAP可解释性
│   ├── survival_ml.R        # 生存分析ML
│   ├── pipeline.R           # 全流程管道
│   └── report_generator.R   # 报告生成
└── output/                  # 输出目录
    ├── plots/               # 图表(PDF/PNG)
    ├── models/              # 模型(.rds)
    ├── predictions/         # 预测(.csv)
    ├── reports/             # 报告(.html)
    └── tables/              # 表格(.csv)
```

## 依赖包
安装需要 R >= 4.0，运行 `launcher.sh install` 自动安装全部依赖。

核心包：caret, tidymodels, glmnet, xgboost, ranger, kernlab, Boruta, fastshap, pROC, survival, randomForestSRC, ggplot2, rmarkdown
