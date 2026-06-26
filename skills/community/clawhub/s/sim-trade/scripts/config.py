#!/usr/bin/env python3
"""
Sim Trade 统一配置
"""
import os

# ===========================================
# 💰 资金配置
# ===========================================

# 初始资金（元）
INITIAL_CAPITAL = 100000.0

# 手续费（万分之三）
FEE_RATE = 0.0003

# 印花税（卖出，千分之一）
STAMP_TAX_SELL = 0.001

# 滑点（元/股）
SLIPPAGE = 0.01

# ===========================================
# 📁 数据存储配置
# ===========================================

# 主数据目录
DATA_DIR = os.path.expanduser("~/.openclaw/sim_trade")

# 账户文件
ACCOUNT_FILE = os.path.join(DATA_DIR, "account.json")

# 持仓文件
POSITIONS_FILE = os.path.join(DATA_DIR, "positions.json")

# 交易记录文件
TRADES_FILE = os.path.join(DATA_DIR, "trades.txt")

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# ===========================================
# 🔌 行情数据源
# ===========================================

DATA_SOURCES_PRIORITY = ["xueqiu", "tencent"]

# 请求间隔（秒）
REQUEST_DELAY = 1.0

# 超时时间（秒）
REQUEST_TIMEOUT = 10
