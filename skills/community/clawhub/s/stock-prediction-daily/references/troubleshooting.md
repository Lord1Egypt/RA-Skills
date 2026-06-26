# 问题排查指南

## API相关

### Tencent日线无volume列
**症状**：Tencent返回的列名有`amount`但无`volume`
**解决**：`df["volume"] = df["amount"]`

## 模型相关

### xgboost save_model/load_model 报错
**症状**：`TypeError` 或 JSON序列化错误
**原因**：sklearn包装器与xgboost原生方法不兼容
**解决**：必须用 `joblib.dump(model, path)` / `joblib.load(path)`

### 预测日线不足
**症状**：预测时报 `Insufficient data`
**原因**：目标股票可用日线历史不足，无法计算长周期特征
**解决**：确保 `scripts/data/` 下已有训练阶段缓存，或重新运行训练补齐日线历史

### 特征缺失 (NaN/0填充)
**症状**：预测时部分特征全为0
**原因**：数据行数不足以计算长周期特征（如ma_ratio_100需100+天）
**解决**：确保获取足够历史（Tencent日线 lookback_days≥400）

### 次日评估返回数据不足
**症状**：`evaluate.py` 的 `一天后价格` 为 `N/A`
**原因**：预测日期之后还没有新的交易日收盘数据
**解决**：等待下一个交易日数据可用后重新执行 `python3 evaluate.py`

## Flask相关

### app.py 报 "can't open file"
**症状**：`python3 app.py` 报文件不存在
**原因**：cwd不正确，Flask使用相对路径加载模板
**解决**：进入 `.github/skills/stock-prediction-daily/scripts` 后执行 `python3 app.py`

### 端口5000被占用
**解决**：`lsof -ti:5000 | xargs kill -9`

### 表格文字换行
**解决**：给 `tbody td` 加 `white-space: nowrap`，容器 `max-width` 调大
