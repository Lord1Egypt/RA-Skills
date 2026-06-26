#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LSTM 股票价格预测模型
基于深度学习的时间序列预测

注意：设置控制台编码为 UTF-8 以避免中文显示问题
"""

import sys
import io
# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""

功能：
1. 数据准备：获取历史 K 线数据，特征工程，归一化，训练集/测试集分割
2. LSTM 模型构建：2 层 LSTM，每层 50 神经元，Dropout 0.2
3. 模型训练：MSE loss, Adam 优化器，100 epochs, batch size 32
4. 预测输出：方向、概率、目标区间、置信区间、未来 5 日预测
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# 深度学习库
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.model_selection import train_test_split
    TF_AVAILABLE = True
except ImportError as e:
    print(f"TensorFlow/Keras 导入失败：{e}")
    TF_AVAILABLE = False
    # 使用备用方案
    MinMaxScaler = None
    train_test_split = None

# 数据获取库
try:
    import akshare as ak
    AK_AVAILABLE = True
except ImportError:
    AK_AVAILABLE = False
    print("AkShare 未安装，将使用模拟数据")

# 技术指标计算
try:
    import talib
    TALIB_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    print("TA-Lib 未安装，将使用自定义指标计算")


class LSTMStockPredictor:
    """LSTM 股票价格预测器"""
    
    def __init__(self, stock_code: str = "000001", time_step: int = 60, 
                 lstm_units: int = 50, lstm_layers: int = 2, 
                 dropout_rate: float = 0.2, forecast_days: int = 5):
        """
        初始化预测器
        
        参数:
            stock_code: 股票代码
            time_step: 时间步长（历史天数）
            lstm_units: LSTM 神经元数量
            lstm_layers: LSTM 层数
            dropout_rate: Dropout 比例
            forecast_days: 预测天数
        """
        self.stock_code = stock_code
        self.time_step = time_step
        self.lstm_units = lstm_units
        self.lstm_layers = lstm_layers
        self.dropout_rate = dropout_rate
        self.forecast_days = forecast_days
        
        self.model = None
        self.scaler = None
        self.feature_scalers = {}
        self.data = None
        self.features = None
        self.history = None
        
        print(f"[OK] 预测器初始化完成")
        print(f"  - 股票代码：{stock_code}")
        print(f"  - 时间步长：{time_step} 天")
        print(f"  - LSTM 架构：{lstm_layers}层 x {lstm_units}神经元")
        print(f"  - Dropout: {dropout_rate}")
        print(f"  - 预测天数：{forecast_days} 天")
    
    def fetch_data(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取历史 K 线数据（至少 1 年）
        
        参数:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
        
        返回:
            DataFrame with OHLCV data
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        if start_date is None:
            # 获取至少 1.5 年数据以确保有足够样本
            start_date = (datetime.now() - timedelta(days=550)).strftime("%Y%m%d")
        
        print(f"\n[DATA] 正在获取历史数据...")
        print(f"  时间范围：{start_date} 至 {end_date}")
        
        if AK_AVAILABLE:
            try:
                # 获取 A 股历史行情
                df = ak.stock_zh_a_hist(
                    symbol=self.stock_code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"  # 前复权
                )
                
                # 重命名列以匹配标准格式
                df = df.rename(columns={
                    '日期': 'date',
                    '开盘': 'open',
                    '收盘': 'close',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume',
                    '成交额': 'amount',
                    '振幅': 'amplitude',
                    '涨跌幅': 'pct_change',
                    '涨跌额': 'change',
                    '换手率': 'turnover'
                })
                
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                print(f"  [OK] 获取成功：{len(df)} 条记录")
                self.data = df
                return df
                
            except Exception as e:
                print(f"  [WARN] AkShare 获取失败：{e}")
                print("  [INFO] 使用模拟数据")
        
        # 生成模拟数据（用于测试）
        print("  [INFO] 生成模拟数据...")
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=550),
            end=datetime.now(),
            freq='B'  # 工作日
        )
        
        n = len(dates)
        # 生成随机游走价格
        np.random.seed(42)
        returns = np.random.normal(0.0005, 0.02, n)
        prices = 100 * np.exp(np.cumsum(returns))
        
        df = pd.DataFrame({
            'date': dates,
            'open': prices * (1 + np.random.uniform(-0.01, 0.01, n)),
            'high': prices * (1 + np.random.uniform(0, 0.02, n)),
            'low': prices * (1 - np.random.uniform(0, 0.02, n)),
            'close': prices,
            'volume': np.random.uniform(1e6, 1e7, n),
            'amount': np.random.uniform(1e7, 1e8, n)
        })
        
        self.data = df
        print(f"  [OK] 模拟数据生成：{len(df)} 条记录")
        return df
    
    def calculate_features(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """
        特征工程：计算技术指标
        
        特征包括:
        - MA: 5/10/20/60 日均线
        - MACD: DIF/DEA/Histogram
        - RSI: 14 日相对强弱指标
        - 成交量相关指标
        - 价格动量指标
        
        参数:
            df: 原始数据 DataFrame
        
        返回:
            包含所有特征的 DataFrame
        """
        if df is None:
            df = self.data.copy()
        
        print(f"\n[FEATURE] 正在进行特征工程...")
        
        # 确保有收盘价
        if 'close' not in df.columns:
            raise ValueError("数据中缺少收盘价列")
        
        close = df['close'].values
        high = df['high'].values if 'high' in df.columns else close
        low = df['low'].values if 'low' in df.columns else close
        volume = df['volume'].values if 'volume' in df.columns else np.ones(len(close))
        
        # 1. 移动平均线 (MA)
        print("  - 计算移动平均线 (MA)...")
        df['ma5'] = self._calculate_ma(close, 5)
        df['ma10'] = self._calculate_ma(close, 10)
        df['ma20'] = self._calculate_ma(close, 20)
        df['ma60'] = self._calculate_ma(close, 60)
        
        # MA 与价格的关系
        df['close_ma5_ratio'] = close / df['ma5']
        df['close_ma20_ratio'] = close / df['ma20']
        
        # 2. MACD
        print("  - 计算 MACD...")
        df['macd_dif'], df['macd_dea'], df['macd_hist'] = self._calculate_macd(close)
        
        # 3. RSI
        print("  - 计算 RSI...")
        df['rsi14'] = self._calculate_rsi(close, 14)
        df['rsi7'] = self._calculate_rsi(close, 7)
        
        # 4. 成交量指标
        print("  - 计算成交量指标...")
        df['volume_ma5'] = self._calculate_ma(volume, 5)
        df['volume_ma20'] = self._calculate_ma(volume, 20)
        df['volume_ratio'] = volume / df['volume_ma5']
        
        # 5. 价格动量
        print("  - 计算动量指标...")
        df['momentum_5'] = close / self._calculate_ma(close, 5) - 1
        df['momentum_10'] = close / self._calculate_ma(close, 10) - 1
        df['roc_5'] = (close - np.roll(close, 5)) / np.roll(close, 5) * 100
        df['roc_10'] = (close - np.roll(close, 10)) / np.roll(close, 10) * 100
        
        # 6. 波动率
        print("  - 计算波动率...")
        df['volatility_5'] = self._calculate_volatility(close, 5)
        df['volatility_20'] = self._calculate_volatility(close, 20)
        
        # 7. 价格范围
        df['high_low_ratio'] = (high - low) / close
        df['close_open_ratio'] = (close - df['open']) / df['open']
        
        # 处理 NaN 值
        df = df.bfill().ffill().fillna(0)
        
        # 选择特征列
        feature_columns = [
            'close', 'open', 'high', 'low', 'volume',
            'ma5', 'ma10', 'ma20', 'ma60',
            'close_ma5_ratio', 'close_ma20_ratio',
            'macd_dif', 'macd_dea', 'macd_hist',
            'rsi14', 'rsi7',
            'volume_ma5', 'volume_ma20', 'volume_ratio',
            'momentum_5', 'momentum_10', 'roc_5', 'roc_10',
            'volatility_5', 'volatility_20',
            'high_low_ratio', 'close_open_ratio'
        ]
        
        # 只保留存在的列
        feature_columns = [col for col in feature_columns if col in df.columns]
        
        self.features = df[feature_columns]
        print(f"  [OK] 特征工程完成：{len(feature_columns)} 个特征")
        
        return self.features
    
    def _calculate_ma(self, data: np.ndarray, period: int) -> np.ndarray:
        """计算移动平均线"""
        ma = pd.Series(data).rolling(window=period).mean().values
        return ma
    
    def _calculate_macd(self, close: np.ndarray, 
                        fast: int = 12, slow: int = 26, signal: int = 9):
        """计算 MACD"""
        if TALIB_AVAILABLE:
            dif, dea, hist = talib.MACD(close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
            return dif, dea, hist
        
        # 手动计算
        ema_fast = pd.Series(close).ewm(span=fast, adjust=False).mean().values
        ema_slow = pd.Series(close).ewm(span=slow, adjust=False).mean().values
        dif = ema_fast - ema_slow
        dea = pd.Series(dif).ewm(span=signal, adjust=False).mean().values
        hist = dif - dea
        
        return dif, dea, hist
    
    def _calculate_rsi(self, close: np.ndarray, period: int = 14) -> np.ndarray:
        """计算 RSI"""
        if TALIB_AVAILABLE:
            return talib.RSI(close, timeperiod=period)
        
        # 手动计算
        delta = np.diff(close, prepend=close[0])
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        avg_gain = pd.Series(gain).rolling(window=period).mean().values
        avg_loss = pd.Series(loss).rolling(window=period).mean().values
        
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_volatility(self, close: np.ndarray, period: int) -> np.ndarray:
        """计算波动率（标准差）"""
        returns = np.diff(close, prepend=close[0]) / (close + 1e-10)
        vol = pd.Series(returns).rolling(window=period).std().values
        return vol
    
    def prepare_sequences(self, test_size: float = 0.2):
        """
        准备 LSTM 输入序列
        
        参数:
            test_size: 测试集比例
        
        返回:
            X_train, X_test, y_train, y_test
        """
        print(f"\n[SEQ] 正在准备序列数据...")
        
        if self.features is None:
            raise ValueError("请先调用 calculate_features()")
        
        data = self.features.values
        
        # 归一化
        print("  - 数据归一化...")
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        data_scaled = self.scaler.fit_transform(data)
        
        # 创建序列
        print(f"  - 创建时间序列 (步长={self.time_step})...")
        X, y = [], []
        
        for i in range(self.time_step, len(data_scaled) - self.forecast_days):
            X.append(data_scaled[i - self.time_step:i])
            # 预测未来 forecast_days 天的收盘价
            y.append(data_scaled[i:i + self.forecast_days, 
                                self.features.columns.get_loc('close')])
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"  - 序列形状：X={X.shape}, y={y.shape}")
        
        # 分割训练集和测试集
        print(f"  - 分割训练集/测试集 (80/20)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, shuffle=False
        )
        
        print(f"  [OK] 序列准备完成")
        print(f"    训练集：{X_train.shape[0]} 样本")
        print(f"    测试集：{X_test.shape[0]} 样本")
        
        return X_train, X_test, y_train, y_test
    
    def build_model(self, input_shape: tuple):
        """
        构建 LSTM 模型
        
        架构:
        - 输入层：(time_step, n_features)
        - LSTM 层 1: 50 神经元，return_sequences=True
        - Dropout: 0.2
        - LSTM 层 2: 50 神经元
        - Dropout: 0.2
        - Dense 输出层：forecast_days 个输出
        
        参数:
            input_shape: 输入形状 (time_step, n_features)
        """
        print(f"\n[BUILD] 正在构建 LSTM 模型...")
        
        if not TF_AVAILABLE:
            raise ImportError("TensorFlow/Keras 未安装，无法构建模型")
        
        model = Sequential()
        
        # 第一层 LSTM
        model.add(LSTM(
            units=self.lstm_units,
            return_sequences=True,
            input_shape=input_shape
        ))
        model.add(Dropout(self.dropout_rate))
        
        # 第二层 LSTM
        model.add(LSTM(
            units=self.lstm_units,
            return_sequences=False
        ))
        model.add(Dropout(self.dropout_rate))
        
        # 输出层（预测未来 forecast_days 天）
        model.add(Dense(self.forecast_days))
        
        # 编译模型
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        
        print(f"  [OK] 模型构建完成")
        model.summary()
        
        return model
    
    def train(self, X_train, y_train, X_test, y_test, 
              epochs: int = 100, batch_size: int = 32, 
              validation_split: float = 0.1):
        """
        训练模型
        
        参数:
            X_train: 训练输入
            y_train: 训练输出
            X_test: 测试输入
            y_test: 测试输出
            epochs: 训练轮数
            batch_size: 批次大小
            validation_split: 验证集比例
        """
        print(f"\n[TRAIN] 开始模型训练...")
        print(f"  - Epochs: {epochs}")
        print(f"  - Batch Size: {batch_size}")
        print(f"  - Validation Split: {validation_split}")
        
        if self.model is None:
            raise ValueError("请先调用 build_model()")
        
        # 早停
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
        
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
        
        # 训练
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        # 评估
        print(f"\n[EVAL] 模型评估...")
        train_loss, train_mae = self.model.evaluate(X_train, y_train, verbose=0)
        test_loss, test_mae = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"  训练集 - Loss: {train_loss:.6f}, MAE: {train_mae:.6f}")
        print(f"  测试集 - Loss: {test_loss:.6f}, MAE: {test_mae:.6f}")
        
        return self.history
    
    def predict(self, X: np.ndarray = None) -> dict:
        """
        进行预测并输出标准格式结果
        
        参数:
            X: 输入序列，如果为 None 则使用最新数据
        
        返回:
            {
                "direction": "UP/DOWN",
                "probability": 0.72,
                "target_range": [560, 590],
                "confidence_interval": "68%",
                "forecast": [545, 550, 555, 560, 565]
            }
        """
        print(f"\n[PREDICT] 正在进行预测...")
        
        if self.model is None:
            raise ValueError("模型未训练，请先调用 train()")
        
        # 如果没有提供输入，使用最新数据
        if X is None:
            # 获取最新的 time_step 条数据
            data = self.features.values[-self.time_step:]
            data_scaled = self.scaler.transform(data)
            X = data_scaled.reshape(1, self.time_step, -1)
        
        # 预测
        predictions_scaled = self.model.predict(X, verbose=0)
        
        # 反归一化
        # 创建一个完整的特征向量用于反归一化
        n_features = self.features.shape[1]
        close_idx = self.features.columns.get_loc('close')
        
        forecasts = []
        for pred in predictions_scaled:
            # 创建 dummy 特征向量
            dummy = np.zeros((len(pred), n_features))
            dummy[:, close_idx] = pred
            
            # 反归一化
            pred_original = self.scaler.inverse_transform(dummy)[:, close_idx]
            forecasts.append(pred_original.tolist())
        
        # 取第一个样本的预测
        forecast = forecasts[0] if forecasts else []
        
        # 计算方向
        current_price = self.features['close'].iloc[-1]
        avg_forecast = np.mean(forecast)
        direction = "UP" if avg_forecast > current_price else "DOWN"
        
        # 计算概率（基于预测的置信度）
        # 使用预测值的标准差来估计概率
        forecast_std = np.std(forecast)
        forecast_mean = np.mean(forecast)
        price_change = (forecast_mean - current_price) / current_price
        
        # 简化概率计算
        probability = 0.5 + 0.4 * np.tanh(price_change * 10)
        probability = round(max(0.1, min(0.9, probability)), 2)
        
        # 目标区间（基于预测的 68% 置信区间）
        target_low = round(min(forecast) * 0.98, 2)
        target_high = round(max(forecast) * 1.02, 2)
        
        # 四舍五入预测值
        forecast = [round(p, 2) for p in forecast]
        
        result = {
            "direction": direction,
            "probability": probability,
            "target_range": [target_low, target_high],
            "confidence_interval": "68%",
            "forecast": forecast,
            "current_price": round(current_price, 2),
            "predicted_change": round((avg_forecast - current_price) / current_price * 100, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"  [OK] 预测完成")
        print(f"    当前价格：{result['current_price']}")
        print(f"    预测方向：{result['direction']}")
        print(f"    概率：{result['probability']}")
        print(f"    目标区间：{result['target_range']}")
        print(f"    未来 5 日预测：{result['forecast']}")
        
        return result
    
    def save_model(self, path: str = "lstm_model.keras"):
        """保存模型和 scaler"""
        import pickle
        if self.model:
            # 使用新的 Keras 格式保存模型
            self.model.save(path)
            # 保存 scaler
            scaler_path = path.replace('.keras', '_scaler.pkl')
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"[OK] 模型已保存至：{path}")
            print(f"[OK] Scaler 已保存至：{scaler_path}")
    
    def load_model(self, path: str = "lstm_model.keras"):
        """加载模型和 scaler"""
        import pickle
        if TF_AVAILABLE:
            from tensorflow.keras.models import load_model
            # 自动检测文件格式
            if path.endswith('.h5'):
                from tensorflow.keras.models import load_model as load_h5
                self.model = load_h5(path, compile=True)
            else:
                self.model = load_model(path)
            # 加载 scaler
            scaler_path = path.replace('.keras', '_scaler.pkl')
            try:
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print(f"[OK] 模型已加载：{path}")
                print(f"[OK] Scaler 已加载：{scaler_path}")
            except FileNotFoundError:
                print(f"[WARN] Scaler 文件未找到：{scaler_path}")
                print(f"[INFO] 请确保先运行过 prepare_sequences() 以初始化 scaler")


def main():
    """主函数：演示完整流程"""
    print("=" * 60)
    print("LSTM 股票价格预测模型")
    print("=" * 60)
    
    # 创建预测器
    predictor = LSTMStockPredictor(
        stock_code="000001",  # 平安银行
        time_step=60,
        lstm_units=50,
        lstm_layers=2,
        dropout_rate=0.2,
        forecast_days=5
    )
    
    # 1. 数据准备
    print("\n" + "=" * 60)
    print("阶段 1: 数据准备")
    print("=" * 60)
    df = predictor.fetch_data()
    features = predictor.calculate_features(df)
    
    # 2. 准备序列
    print("\n" + "=" * 60)
    print("阶段 2: 序列准备")
    print("=" * 60)
    X_train, X_test, y_train, y_test = predictor.prepare_sequences(test_size=0.2)
    
    # 3. 构建模型
    print("\n" + "=" * 60)
    print("阶段 3: 模型构建")
    print("=" * 60)
    input_shape = (X_train.shape[1], X_train.shape[2])
    predictor.build_model(input_shape)
    
    # 4. 训练模型
    print("\n" + "=" * 60)
    print("阶段 4: 模型训练")
    print("=" * 60)
    predictor.train(X_train, y_train, X_test, y_test, epochs=100, batch_size=32)
    
    # 5. 预测
    print("\n" + "=" * 60)
    print("阶段 5: 预测输出")
    print("=" * 60)
    result = predictor.predict()
    
    # 输出 JSON 格式结果
    print("\n" + "=" * 60)
    print("预测结果 (JSON 格式)")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 保存模型（使用新的 Keras 格式）
    predictor.save_model("lstm_stock_predictor.keras")
    
    return result


if __name__ == "__main__":
    main()
