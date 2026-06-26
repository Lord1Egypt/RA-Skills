# -*- coding: utf-8 -*-
"""
通达信本地数据读取器
"""
import struct
from pathlib import Path

TDX_PATH = Path(r"D:\new_tdx")

print("=" * 80)
print(" 通达信本地数据分析")
print("=" * 80)

def read_day_file(filepath):
    """读取日线文件 - 每条32字节"""
    records = []
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(32)
            if len(data) < 32: break
            date_int = struct.unpack('<I', data[0:4])[0]
            open_p = struct.unpack('<I', data[4:8])[0] / 100.0
            high_p = struct.unpack('<I', data[8:12])[0] / 100.0
            low_p = struct.unpack('<I', data[12:16])[0] / 100.0
            close_p = struct.unpack('<I', data[16:20])[0] / 100.0
            amount = struct.unpack('<f', data[20:24])[0]
            volume = struct.unpack('<I', data[24:28])[0]
            year = date_int // 10000
            month = (date_int % 10000) // 100
            day = date_int % 100
            records.append({'date': f"{year}-{month:02d}-{day:02d}", 'open': open_p, 'high': high_p, 'low': low_p, 'close': close_p, 'volume': volume})
    return records

# 恒瑞医药
print("\n[1] 恒瑞医药(600276)")
print("-" * 60)
day_file = TDX_PATH / "vipdoc" / "sh" / "lday" / "sh600276.day"
if day_file.exists():
    records = read_day_file(day_file)
    if records:
        print(f"  数据: {records[0]['date']} ~ {records[-1]['date']} ({len(records)}条)")
        for r in records[-5:]:
            print(f"    {r['date']}: {r['close']:.2f}")

# 插件
print("\n[2] 插件")
print("-" * 60)
for folder in ["GNPlugins", "QHPlugins", "TCPlugins", "ZDPlugins"]:
    p = TDX_PATH / folder
    if p.exists():
        dlls = [f.name for f in p.glob("*.dll")]
        if dlls: print(f"  {folder}: {dlls[:2]}")

# 金股猎手
jiangen = TDX_PATH / "GNPlugins" / "TE_Jiangen.dll"
if jiangen.exists():
    print(f"\n  ** 金股猎手: {jiangen.name} ({jiangen.stat().st_size//1024}KB)")

print("\n[3] 功能模块(.sp)")
print("-" * 60)
funcs = list((TDX_PATH / "funcs").glob("*.sp"))
print(f"  共{len(funcs)}个")
for f in funcs[:8]: print(f"    {f.stem}")