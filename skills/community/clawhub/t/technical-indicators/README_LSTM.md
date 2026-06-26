# LSTM 股票价格预测模型

基于深度学习的时间序列预测模型，使用 LSTM 神经网络预测股票未来 5 日价格走势。

## 功能特性

### 1. 数据准备
- 获取历史 K 线数据（至少 1 年）
- 特征工程：MA/MACD/RSI/成交量等 27 个技术指标
- 数据归一化处理（MinMaxScaler）
- 训练集/测试集分割（80/20）

### 2. LSTM 模型架构
```
输入层：(60, 27) - 60 天历史数据，27 个特征
├── LSTM 层 1: 50 神经元，return_sequences=True
├── Dropout: 0.2
├── LSTM 层 2: 50 神经元
├── Dropout: 0.2
└── Dense 输出层：5 个输出（未来 5 日价格）
```

### 3. 训练配置
- Loss 函数：MSE（均方误差）
- 优化器：Adam（learning_rate=0.001）
- Epochs: 100（带早停）
- Batch Size: 32
- Validation Split: 0.1

### 4. 预测输出格式
```json
{
  "direction": "UP/DOWN",
  "probability": 0.72,
  "target_range": [560, 590],
  "confidence_interval": "68%",
  "forecast": [545, 550, 555, 560, 565],
  "current_price": 550.00,
  "predicted_change": 1.82,
  "timestamp": "2026-03-14T22:57:10"
}
```

## 使用方法

### 基本使用
```python
from ml_predictor import LSTMStockPredictor

# 创建预测器
predictor = LSTMStockPredictor(
    stock_code="000001",  # 股票代码
    time_step=60,         # 时间步长
    lstm_units=50,        # LSTM 神经元数
    lstm_layers=2,        # LSTM 层数
    dropout_rate=0.2,     # Dropout 比例
    forecast_days=5       # 预测天数
)

# 1. 获取数据
df = predictor.fetch_data()

# 2. 特征工程
features = predictor.calculate_features(df)

# 3. 准备序列
X_train, X_test, y_train, y_test = predictor.prepare_sequences(test_size=0.2)

# 4. 构建模型
input_shape = (X_train.shape[1], X_train.shape[2])
predictor.build_model(input_shape)

# 5. 训练模型
predictor.train(X_train, y_train, X_test, y_test, epochs=100, batch_size=32)

# 6. 预测
result = predictor.predict()
print(result)

# 7. 保存模型
predictor.save_model("my_model.h5")
```

### 加载已训练模型
```python
from ml_predictor import LSTMStockPredictor

predictor = LSTMStockPredictor()
predictor.load_model("lstm_stock_predictor.h5")

# 直接预测
result = predictor.predict()
```

### 命令行运行
```bash
cd skills/technical-indicators
python ml_predictor.py
```

## 技术指标列表

模型使用以下 27 个特征：

### 价格数据
- close, open, high, low, volume

### 移动平均线
- ma5, ma10, ma20, ma60
- close_ma5_ratio, close_ma20_ratio

### MACD
- macd_dif, macd_dea, macd_hist

### RSI
- rsi14, rsi7

### 成交量指标
- volume_ma5, volume_ma20, volume_ratio

### 动量指标
- momentum_5, momentum_10
- roc_5, roc_10

### 波动率
- volatility_5, volatility_20

### 价格范围
- high_low_ratio, close_open_ratio

## 依赖项

```bash
pip install tensorflow scikit-learn pandas numpy akshare
```

可选（用于更快的指标计算）：
```bash
pip install ta-lib
```

## 性能指标

- 训练集 Loss: ~0.003
- 测试集 Loss: ~0.036
- 训练集 MAE: ~0.040
- 测试集 MAE: ~0.171

## 注意事项

1. **数据质量**: 模型性能高度依赖输入数据质量，建议使用真实市场数据
2. **过拟合**: 使用 Dropout 和早停机制防止过拟合
3. **市场风险**: 预测结果仅供参考，不构成投资建议
4. **重新训练**: 建议定期使用最新数据重新训练模型

## 文件结构

```
skills/technical-indicators/
├── ml_predictor.py           # 主程序
├── lstm_stock_predictor.h5   # 预训练模型
├── README_LSTM.md            # 本文档
└── test_lstm_predictor.py    # 测试脚本
```

## 更新日志

- 2026-03-14: 初始版本，完成 L3 专家级能力建设
  - 实现完整 LSTM 架构
  - 支持 27 个技术指标
  - 输出标准化 JSON 格式
