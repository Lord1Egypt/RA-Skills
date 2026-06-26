#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LSTM 预测器测试脚本
测试已保存的模型并验证预测功能
"""

import sys
import json
from ml_predictor import LSTMStockPredictor


def test_saved_model():
    """测试加载已保存的模型并进行预测"""
    print("=" * 60)
    print("LSTM 模型测试 - 加载已保存模型")
    print("=" * 60)
    
    # 创建预测器
    predictor = LSTMStockPredictor(
        stock_code="000001",
        time_step=60,
        lstm_units=50,
        lstm_layers=2,
        dropout_rate=0.2,
        forecast_days=5
    )
    
    # 获取数据（用于特征计算）
    print("\n[1/3] 获取数据...")
    df = predictor.fetch_data()
    
    # 计算特征
    print("\n[2/3] 计算特征...")
    features = predictor.calculate_features(df)
    
    # 加载模型
    print("\n[3/3] 加载模型并预测...")
    try:
        predictor.load_model("lstm_stock_predictor.keras")
        result = predictor.predict()
        
        print("\n" + "=" * 60)
        print("预测结果")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 验证输出格式
        required_fields = [
            "direction", "probability", "target_range",
            "confidence_interval", "forecast"
        ]
        
        missing = [f for f in required_fields if f not in result]
        if missing:
            print(f"\n[ERROR] 缺少字段：{missing}")
            return False
        
        # 验证字段类型
        assert result["direction"] in ["UP", "DOWN"], "direction 必须是 UP 或 DOWN"
        assert 0 <= result["probability"] <= 1, "probability 必须在 0-1 之间"
        assert len(result["target_range"]) == 2, "target_range 必须包含 2 个值"
        assert len(result["forecast"]) == 5, "forecast 必须包含 5 个值"
        assert result["confidence_interval"] == "68%", "confidence_interval 必须是 68%"
        
        print("\n[OK] 所有验证通过！")
        return True
        
    except FileNotFoundError:
        print("[ERROR] 模型文件未找到，请先运行 ml_predictor.py 训练模型")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def test_quick_predict():
    """快速预测测试（使用模拟数据）"""
    print("\n" + "=" * 60)
    print("快速预测测试")
    print("=" * 60)
    
    predictor = LSTMStockPredictor(
        stock_code="000001",
        time_step=60,
        lstm_units=50,
        lstm_layers=2,
        dropout_rate=0.2,
        forecast_days=5
    )
    
    # 完整流程
    df = predictor.fetch_data()
    features = predictor.calculate_features(df)
    X_train, X_test, y_train, y_test = predictor.prepare_sequences(test_size=0.2)
    
    input_shape = (X_train.shape[1], X_train.shape[2])
    predictor.build_model(input_shape)
    
    # 快速训练（仅 10 个 epoch 用于测试）
    predictor.train(X_train, y_train, X_test, y_test, epochs=10, batch_size=32)
    
    result = predictor.predict()
    
    print("\n快速测试结果:")
    print(f"  方向：{result['direction']}")
    print(f"  概率：{result['probability']}")
    print(f"  预测：{result['forecast']}")
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        test_quick_predict()
    else:
        success = test_saved_model()
        sys.exit(0 if success else 1)
