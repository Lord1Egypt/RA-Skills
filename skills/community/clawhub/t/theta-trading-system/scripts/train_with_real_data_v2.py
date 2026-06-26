#!/usr/bin/env python3
"""
基于真实数据的Theta模型 - 优化版
不按股票分组，直接使用所有数据
增加更多通用特征
"""

import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
import joblib
import json
import os
from datetime import datetime

print("=" * 80)
print("🚀 基于真实数据的Theta模型 - 优化版")
print("🎯 使用所有数据，增加通用特征")
print("=" * 80)

# 加载真实数据
print("\n📊 步骤1: 加载真实涨停股数据...")
DB_PATH = "/root/.openclaw/workspace/data/real_stock_data.db"
conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("""
    SELECT date, code, name, close, change_pct, turnover_rate, amount
    FROM limit_up_stocks
    ORDER BY date, code
""", conn)

conn.close()

print(f"✅ 加载真实数据: {len(df)}条")
print(f"日期范围: {df['date'].min()} ~ {df['date'].max()}")

# 特征工程（不按股票分组）
print("\n📊 步骤2: 特征工程（全局特征）...")

# 添加日期特征
df['date_obj'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date_obj'].dt.dayofweek
df['is_monday'] = (df['day_of_week'] == 0).astype(int)
df['is_friday'] = (df['day_of_week'] == 4).astype(int)

# 全局统计特征
df['market_avg_change'] = df.groupby('date')['change_pct'].transform('mean')
df['market_std_change'] = df.groupby('date')['change_pct'].transform('std')
df['market_avg_turnover'] = df.groupby('date')['turnover_rate'].transform('mean')

# 相对市场表现
df['relative_to_market'] = df['change_pct'] - df['market_avg_change']

# 成交额排名
df['amount_rank'] = df.groupby('date')['amount'].rank(pct=True)

# 换手率排名
df['turnover_rank'] = df.groupby('date')['turnover_rate'].rank(pct=True)

# 涨幅排名
df['change_rank'] = df.groupby('date')['change_pct'].rank(pct=True)

# 组合特征
df['momentum_score'] = df['change_rank'] * df['amount_rank']
df['strength_score'] = df['change_pct'] * df['turnover_rate']

# 方案A: 目标变量 - 次日/3日涨幅（基于日期全局排序）
# 按日期和涨幅排序，预测下一个交易日的表现
df = df.sort_values(['date', 'change_pct'], ascending=[True, False])
df['next_day_change'] = df.groupby('code')['change_pct'].shift(-1)
df['next_3day_change'] = df.groupby('code')['change_pct'].rolling(3, min_periods=1).sum().shift(-3).values

# 删除无目标值的数据
df_clean = df.dropna(subset=['next_day_change', 'next_3day_change'])

print(f"✅ 特征工程完成: {len(df_clean)}条有效数据")

# 准备训练数据
print("\n📊 步骤3: 准备训练数据...")

feature_cols = [
    'change_pct', 'turnover_rate', 
    'day_of_week', 'is_monday', 'is_friday',
    'market_avg_change', 'market_std_change', 'market_avg_turnover',
    'relative_to_market',
    'amount_rank', 'turnover_rank', 'change_rank',
    'momentum_score', 'strength_score'
]

X = df_clean[feature_cols].fillna(0).values
y_1d = df_clean['next_day_change'].values
y_3d = df_clean['next_3day_change'].values

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 特征筛选（选最重要的10个）
print(f"\n📊 步骤4: 特征筛选（从{len(feature_cols)}个中选10个）...")
selector = SelectKBest(score_func=f_regression, k=10)
X_selected = selector.fit_transform(X_scaled, y_1d)

# 获取选中的特征
selected_mask = selector.get_support()
selected_features = [feature_cols[i] for i in range(len(feature_cols)) if selected_mask[i]]

print(f"✅ 选中的特征: {selected_features}")

# 数据分割
X_train, X_test, y_1d_train, y_1d_test, y_3d_train, y_3d_test = train_test_split(
    X_selected, y_1d, y_3d, test_size=0.2, random_state=42
)

X_train, X_val, y_1d_train, y_1d_val, y_3d_train, y_3d_val = train_test_split(
    X_train, y_1d_train, y_3d_train, test_size=0.2, random_state=42
)

print(f"训练集: {len(X_train)}, 验证集: {len(X_val)}, 测试集: {len(X_test)}")

# 训练次日涨幅模型
print("\n📊 步骤5: 训练次日涨幅模型...")
model_1d = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model_1d.fit(X_train, y_1d_train)

# 评估
y_1d_pred = model_1d.predict(X_test)
r2_1d = r2_score(y_1d_test, y_1d_pred)
mae_1d = mean_absolute_error(y_1d_test, y_1d_pred)
acc_1d = np.mean((y_1d_pred > 0) == (y_1d_test > 0))
cv_1d = cross_val_score(model_1d, X_selected, y_1d, cv=3, scoring='r2').mean()

print(f"  ✅ 次日模型: R²={r2_1d:.4f}, MAE={mae_1d:.2f}%, 准确率={acc_1d*100:.2f}%, CV R²={cv_1d:.4f}")

# 训练3日涨幅模型
print("\n📊 步骤6: 训练3日涨幅模型...")
model_3d = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model_3d.fit(X_train, y_3d_train)

# 评估
y_3d_pred = model_3d.predict(X_test)
r2_3d = r2_score(y_3d_test, y_3d_pred)
mae_3d = mean_absolute_error(y_3d_test, y_3d_pred)
acc_3d = np.mean((y_3d_pred > 0) == (y_3d_test > 0))
cv_3d = cross_val_score(model_3d, X_selected, y_3d, cv=3, scoring='r2').mean()

print(f"  ✅ 3日模型: R²={r2_3d:.4f}, MAE={mae_3d:.2f}%, 准确率={acc_3d*100:.2f}%, CV R²={cv_3d:.4f}")

# 保存模型
print("\n💾 步骤7: 保存模型...")
MODEL_DIR = "/root/.openclaw/workspace/models/real_data_optimized"
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model_1d, os.path.join(MODEL_DIR, 'model_1d.pkl'))
joblib.dump(model_3d, os.path.join(MODEL_DIR, 'model_3d.pkl'))
joblib.dump(scaler, os.path.join(MODEL_DIR, 'scaler.pkl'))
joblib.dump(selector, os.path.join(MODEL_DIR, 'selector.pkl'))

results = {
    'timestamp': datetime.now().isoformat(),
    'data_source': 'AkShare真实涨停股数据（优化版）',
    'n_samples': len(df_clean),
    'n_features': len(selected_features),
    'selected_features': selected_features,
    '1d_model': {
        'test_r2': float(r2_1d),
        'test_mae': float(mae_1d),
        'test_accuracy': float(acc_1d),
        'cv_r2': float(cv_1d)
    },
    '3d_model': {
        'test_r2': float(r2_3d),
        'test_mae': float(mae_3d),
        'test_accuracy': float(acc_3d),
        'cv_r2': float(cv_3d)
    }
}

with open(os.path.join(MODEL_DIR, 'results.json'), 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"✅ 模型已保存")

# 最终报告
print("\n" + "=" * 80)
print("📊 基于真实数据的优化模型训练完成报告")
print("=" * 80)

print(f"\n✅ 数据源:")
print(f"  - 来源: AkShare真实涨停股数据")
print(f"  - 有效样本: {len(df_clean)}条")
print(f"  - 特征数: {len(selected_features)}个")

print(f"\n📊 次日涨幅模型:")
print(f"  - 测试集 R²: {r2_1d:.4f}")
print(f"  - 测试集 MAE: {mae_1d:.2f}%")
print(f"  - 方向准确率: {acc_1d*100:.2f}%")
print(f"  - 交叉验证 R²: {cv_1d:.4f}")

print(f"\n📊 3日累计涨幅模型:")
print(f"  - 测试集 R²: {r2_3d:.4f}")
print(f"  - 测试集 MAE: {mae_3d:.2f}%")
print(f"  - 方向准确率: {acc_3d*100:.2f}%")
print(f"  - 交叉验证 R²: {cv_3d:.4f}")

print(f"\n🎯 效果对比:")
print(f"  模拟数据模型 R²: 0.0009")
print(f"  真实数据次日模型 R²: {r2_1d:.4f}")
print(f"  真实数据3日模型 R²: {r2_3d:.4f}")

print(f"\n✅ 推荐使用:")
best_r2 = max(r2_1d, r2_3d)
if best_r2 > 0.1:
    if r2_1d > r2_3d:
        print(f"  🏆 次日涨幅模型（R²={r2_1d:.4f}）")
    else:
        print(f"  🏆 3日涨幅模型（R²={r2_3d:.4f}）")
elif best_r2 > 0:
    print(f"  ⚠️ 模型效果一般，建议继续优化")
else:
    print(f"  ⚠️ 模型效果不佳，需要根本性改进")

print(f"\n📌 改进建议:")
print(f"  1. 获取更多历史数据（目前只有16天）")
print(f"  2. 增加技术指标特征（均线、MACD、RSI等）")
print(f"  3. 添加资金流向数据（主力/散户）")
print(f"  4. 引入板块联动分析")

print("\n" + "=" * 80)
print("✅ 优化模型训练完成！")
print("=" * 80)
