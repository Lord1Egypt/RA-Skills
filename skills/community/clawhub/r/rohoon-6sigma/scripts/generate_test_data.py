#!/usr/bin/env python3
"""
生成三组模拟 SPC 测试数据（Excel 格式）
- 一组正态分布数据
- 两组非正态分布数据（偏态、混合分布）
每组 600 条测量值，包含完整业务信息
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

try:
    sys.path.insert(0, '/Library/Python/3.9/site-packages')
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
except ImportError:
    print("请安装 openpyxl: pip3 install openpyxl")
    sys.exit(1)

np.random.seed(42)

# 输出目录
output_dir = os.path.join(os.path.dirname(__file__), 'tmp', 'test_data')
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("生成 SPC 测试数据（三组，每组 600 条）")
print("=" * 80)

# ==================== 公共参数 ====================
n_samples = 600
subgroup_size = 5
n_subgroups = n_samples // subgroup_size

# 规格限
usl = 30.140
lsl = 29.860
target = 30.000

# 业务信息
part_name = "AIAG-VDA-Example-Part"
characteristic_name = "Bore Diameter"
machine_name = "CNC-Machining-Center-01"
process_name = "Engine Block Boring"
operator = "John Smith"
department = "Quality Control"

# 生成检测时间（从 2026-03-31 08:00 开始，每小时 25 个样本）
start_time = datetime(2026, 3, 31, 8, 0)
time_intervals = [start_time + timedelta(minutes=i*12) for i in range(n_samples)]

# ==================== 第一组：正态分布数据 ====================
print("\n[1/3] 生成正态分布数据...")

mu_normal = 30.000
sigma_normal = 0.020
data_normal = np.random.normal(mu_normal, sigma_normal, n_samples)

# 生成批次信息
batch_normal = [f"BATCH-{(i // 50) + 1:03d}" for i in range(n_samples)]

df_normal = pd.DataFrame({
    'Sample_ID': [f"S{i+1:04d}" for i in range(n_samples)],
    'Measurement_Value': data_normal,
    'USL': usl,
    'LSL': lsl,
    'Target': target,
    'Part_Name': part_name,
    'Characteristic': characteristic_name,
    'Machine': machine_name,
    'Process': process_name,
    'Operator': operator,
    'Department': department,
    'Batch': batch_normal,
    'Measurement_Time': time_intervals,
    'Subgroup_ID': [(i // subgroup_size) + 1 for i in range(n_samples)],
})

# 保存 Excel
excel_normal_path = os.path.join(output_dir, '01_Normal_Distribution_Data.xlsx')
df_normal.to_excel(excel_normal_path, index=False, sheet_name='SPC_Data')
print(f"      ✓ {excel_normal_path}")
print(f"        样本数：{n_samples}, 均值：{np.mean(data_normal):.4f}, 标准差：{np.std(data_normal, ddof=1):.4f}")

# ==================== 第二组：非正态数据（偏态分布 - Weibull） ====================
print("\n[2/3] 生成非正态分布数据（偏态/Weibull）...")

# Weibull 分布（右偏）
shape = 2.0  # 形状参数
scale = 0.025  # 尺度参数
data_weibull_raw = np.random.weibull(shape, n_samples) * scale + (lsl + 0.1)
# 调整到规格范围内
data_weibull = np.clip(data_weibull_raw, lsl + 0.001, usl - 0.001)

batch_weibull = [f"BATCH-{(i // 50) + 1:03d}" for i in range(n_samples)]

df_weibull = pd.DataFrame({
    'Sample_ID': [f"S{i+1:04d}" for i in range(n_samples)],
    'Measurement_Value': data_weibull,
    'USL': usl,
    'LSL': lsl,
    'Target': target,
    'Part_Name': part_name,
    'Characteristic': characteristic_name,
    'Machine': machine_name,
    'Process': process_name,
    'Operator': operator,
    'Department': department,
    'Batch': batch_weibull,
    'Measurement_Time': time_intervals,
    'Subgroup_ID': [(i // subgroup_size) + 1 for i in range(n_samples)],
})

excel_weibull_path = os.path.join(output_dir, '02_NonNormal_Weibull_Data.xlsx')
df_weibull.to_excel(excel_weibull_path, index=False, sheet_name='SPC_Data')
print(f"      ✓ {excel_weibull_path}")
print(f"        样本数：{n_samples}, 均值：{np.mean(data_weibull):.4f}, 标准差：{np.std(data_weibull, ddof=1):.4f}")

# ==================== 第三组：非正态数据（混合分布/双峰） ====================
print("\n[3/3] 生成非正态分布数据（混合分布/双峰）...")

# 混合两个正态分布（双峰）
n1 = n_samples // 2
n2 = n_samples - n1
mu1 = 29.950
mu2 = 30.050
sigma_mix = 0.015

data_mix1 = np.random.normal(mu1, sigma_mix, n1)
data_mix2 = np.random.normal(mu2, sigma_mix, n2)
data_mixed = np.concatenate([data_mix1, data_mix2])
np.random.shuffle(data_mixed)
data_mixed = np.clip(data_mixed, lsl + 0.001, usl - 0.001)

batch_mixed = [f"BATCH-{(i // 50) + 1:03d}" for i in range(n_samples)]

df_mixed = pd.DataFrame({
    'Sample_ID': [f"S{i+1:04d}" for i in range(n_samples)],
    'Measurement_Value': data_mixed,
    'USL': usl,
    'LSL': lsl,
    'Target': target,
    'Part_Name': part_name,
    'Characteristic': characteristic_name,
    'Machine': machine_name,
    'Process': process_name,
    'Operator': operator,
    'Department': department,
    'Batch': batch_mixed,
    'Measurement_Time': time_intervals,
    'Subgroup_ID': [(i // subgroup_size) + 1 for i in range(n_samples)],
})

excel_mixed_path = os.path.join(output_dir, '03_NonNormal_Mixed_Data.xlsx')
df_mixed.to_excel(excel_mixed_path, index=False, sheet_name='SPC_Data')
print(f"      ✓ {excel_mixed_path}")
print(f"        样本数：{n_samples}, 均值：{np.mean(data_mixed):.4f}, 标准差：{np.std(data_mixed, ddof=1):.4f}")

# ==================== 统计摘要 ====================
print("\n" + "=" * 80)
print("数据生成完成！统计摘要")
print("=" * 80)

for name, df, data in [
    ('正态分布', df_normal, data_normal),
    ('Weibull 偏态', df_weibull, data_weibull),
    ('混合双峰', df_mixed, data_mixed),
]:
    mu = np.mean(data)
    sigma = np.std(data, ddof=1)
    cp = (usl - lsl) / (6 * sigma)
    cpk = min((usl - mu) / (3 * sigma), (mu - lsl) / (3 * sigma))
    
    print(f"\n{name}:")
    print(f"  文件：0{'123'[['正态分布','Weibull 偏态','混合双峰'].index(name)]}_{name.replace('正态分布','Normal').replace('Weibull 偏态','NonNormal_Weibull').replace('混合双峰','NonNormal_Mixed')}_Data.xlsx")
    print(f"  均值 (μ): {mu:.4f}")
    print(f"  标准差 (σ): {sigma:.4f}")
    print(f"  Cp: {cp:.4f}")
    print(f"  Cpk: {cpk:.4f}")
    print(f"  能力判定：{'✅ 达标 (≥1.67)' if cpk >= 1.67 else '⚠️ 边缘 (1.33-1.67)' if cpk >= 1.33 else '❌ 不达标 (<1.33)'}")

print("\n" + "=" * 80)
print(f"输出目录：{output_dir}")
print("=" * 80)
