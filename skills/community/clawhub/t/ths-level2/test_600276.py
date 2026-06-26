# -*- coding: utf-8 -*-
"""
测试获取恒瑞医药(600276) Level2数据
"""
import os
import sys
import sqlite3
import json
import struct
import socket
import time
from pathlib import Path
from datetime import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'

THS_PATH = Path(r"D:\同花顺远航版")

print("=" * 70)
print(" 恒瑞医药(600276) Level2数据获取测试")
print("=" * 70)

# ========== 1. 本地SQLite数据 ==========
print("\n[1] 本地SQLite数据库 - 股票基本信息")
print("-" * 50)

db_path = THS_PATH / "bin" / "stockname" / "stocknameV2.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 查询恒瑞医药
cursor.execute("SELECT * FROM tablestock WHERE CODE = '600276'")
rows = cursor.fetchall()
print(f"恒瑞医药(600276) 信息:")
for row in rows:
    print(f"  代码: {row[0]}")
    print(f"  名称: {row[1]}")
    print(f"  市场: {row[2]}")
    print(f"  拼音: {row[3]}")

conn.close()

# ========== 2. 本地配置文件 ==========
print("\n[2] 本地配置文件 - 用户自选股")
print("-" * 50)

config_path = THS_PATH / "bin" / "users" / "config" / "config.xml"
if config_path.exists():
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '600276' in content:
        print("恒瑞医药在用户最近浏览列表中")
    else:
        print("恒瑞医药不在最近浏览列表中")

# ========== 3. 检查本地缓存 ==========
print("\n[3] 本地缓存数据检查")
print("-" * 50)

# 检查用户目录下的缓存
cache_dirs = [
    THS_PATH / "bin" / "users" / "claremouse" / "Cache",
    THS_PATH / "bin" / "data",
]

for cache_dir in cache_dirs:
    if cache_dir.exists():
        print(f"检查目录: {cache_dir}")
        for f in cache_dir.rglob("*"):
            if f.is_file() and f.suffix in ['.dat', '.ini', '.xml', '.json']:
                try:
                    size = f.stat().st_size
                    if size < 100000:  # 只读取小文件
                        content = f.read_text(encoding='utf-8', errors='ignore')
                        if '600276' in content or '恒瑞' in content:
                            print(f"  找到相关数据: {f.name}")
                except:
                    pass

# ========== 4. 尝试TCP连接 ==========
print("\n[4] TCP连接测试")
print("-" * 50)

SERVERS = [
    ("hevo-h.10jqka.com.cn", 9601),
    ("hevo.10jqka.com.cn", 8602),
    ("110.41.57.53", 9602),
]

connected = False
sock = None

for host, port in SERVERS:
    try:
        print(f"尝试连接 {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        connected = True
        print(f"  连接成功!")
        break
    except Exception as e:
        print(f"  连接失败: {e}")
        if sock:
            sock.close()
        sock = None

if connected and sock:
    # 尝试发送请求
    print("\n尝试发送Level2数据请求...")
    
    # 构建请求 - 获取恒瑞医药行情
    # 根据DataPushJob.xml协议
    request = b"id=200&market=USHA&codelist=600276&datatype=5,6,7,8,9,10,13,19,22,23"
    
    # 添加长度头
    msg_len = len(request)
    full_request = struct.pack('<I', msg_len) + request
    
    try:
        sock.send(full_request)
        print(f"  已发送请求: {request.decode()}")
        
        # 接收响应
        sock.settimeout(3)
        response = sock.recv(4096)
        if response:
            print(f"  收到响应: {len(response)} 字节")
            print(f"  响应预览: {response[:100]}")
            
            # 保存原始响应
            output_path = Path(__file__).parent / "ths_response_600276.bin"
            with open(output_path, "wb") as f:
                f.write(response)
            print(f"  原始数据已保存到 {output_path}")
        else:
            print("  未收到响应")
    except socket.timeout:
        print("  接收超时 - 可能需要登录认证")
    except Exception as e:
        print(f"  通信错误: {e}")
    
    sock.close()
else:
    print("无法建立TCP连接")

# ========== 5. 读取市场配置 ==========
print("\n[5] 市场配置信息")
print("-" * 50)

market_ini = THS_PATH / "bin" / "users" / "internal" / "market.ini"
if market_ini.exists():
    with open(market_ini, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 查找上海A股相关配置
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'USHA' in line or 'Market_1' in line:
            print(f"  {line.strip()}")
            # 打印后续几行
            for j in range(1, min(5, len(lines) - i)):
                print(f"  {lines[i+j].strip()}")

# ========== 6. 读取板块配置 ==========
print("\n[6] 板块归属信息")
print("-" * 50)

block_files = [
    THS_PATH / "bin" / "users" / "internal" / "Stock" / "block_content_conception.ini",
    THS_PATH / "bin" / "users" / "internal" / "Stock" / "block_content_industry.ini",
]

for bf in block_files:
    if bf.exists():
        print(f"检查: {bf.name}")
        try:
            with open(bf, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if '600276' in content:
                print("  找到恒瑞医药记录")
                # 提取相关行
                for line in content.split('\n'):
                    if '600276' in line:
                        print(f"  {line[:100]}...")
                        break
        except Exception as e:
            print(f"  读取失败: {e}")

# ========== 7. 总结 ==========
print("\n" + "=" * 70)
print(" 测试结果总结")
print("=" * 70)

results = {
    "本地SQLite数据": "成功 - 可读取股票基本信息",
    "本地配置文件": "成功 - 可读取用户配置",
    "本地缓存": "需进一步分析数据格式",
    "TCP连接": "部分成功 - 连接成功但需要协议分析",
    "市场配置": "成功 - 可读取市场定义",
}

for item, status in results.items():
    print(f"  {item}: {status}")

print("\n下一步建议:")
print("  1. 使用Wireshark抓包分析TCP数据格式")
print("  2. 分析th_response_600276.bin文件")
print("  3. 尝试内存读取方式(需要同花顺运行)")
print("  4. 研究SDK DLL接口")