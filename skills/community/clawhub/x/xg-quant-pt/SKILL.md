---
name: xg-quant-platform
description: |
  小果量化交易平台助手（XG Quant Platform）技能。小果量化是一个专业的量化交易系统，提供完整的回测、模拟交易、社区策略分享等功能。
  
  【核心功能】
  - 📊 历史行情数据获取（股票、ETF、可转债）
  - 📈 多维度因子数据提取（技术指标、Alpha因子、动量因子等）
  - 💰 财务数据分析（资产负债表、利润表、现金流量表等）
  - 🔄 多种策略回测（定投、动量、资产配置、网格、海龟、均值方差等）
  - 🤖 模拟交易和社区策略管理
  - 📉 多标的量化分析（相关性矩阵、协方差矩阵、投资组合优化）
  - 📊 股票组合收益分析（绩效指标、夏普比率、最大回撤等）
  - ⏰ 分钟级K线数据（1/5/15/30/60分钟）
  
  【触发关键词】
  小果量化、xg_quant、量化数据、回测系统、定投回测、动量回测、资产配置、
  网格策略、海龟策略、综合动量、条件因子、排序多因子、均值方差、
  因子数据、财务数据、历史行情、ETF数据、可转债数据、K线数据、
  相关性矩阵、协方差矩阵、投资组合优化、股票分析、绩效分析、
  模拟交易、社区策略、数据API、量化分析、策略生成
  
  【作者】
  小果，微信：xg_quant
  
version: 2.0.0
metadata:
  openclaw:
    emoji: "📈"
  author:
    name: "小果"
    wechat: "xg_quant"
---

# 小果量化平台（XG Quant Platform）

## 一、平台简介

小果量化数据API是一个基于量化数据接口，提供股票历史数据、因子数据、财务数据以及多种量化策略回测功能。

### 主要功能

| 功能模块 | 说明 |
|---------|------|
| 📊 历史行情数据 | 获取股票、ETF、可转债的日线历史数据 |
| 📈 因子数据提取 | 数百种技术指标、Alpha因子、动量因子 |
| 💰 财务数据查询 | 资产负债表、利润表、现金流量表、估值数据 |
| 🔄 策略回测 | 定投、动量、资产配置、网格、海龟等9种策略 |
| 🤖 模拟交易 | 个人策略模拟交易和社区策略分享 |
| 📉 量化分析 | 相关性矩阵、协方差矩阵、投资组合优化 |
| 📊 组合分析 | 完整绩效指标（50+项） |

## 二、快速开始

### 1. 安装客户端

使用教程https://gitcode.com/qq_50882340/xg_quant_backtrader_data

# 一、介绍
小果量化数据API是一个基于量化数据接口，提供股票历史数据、因子数据、财务数据以及多种量化策略回测功能。

主要功能
📊 历史行情数据获取

📈 因子数据提取

💰 财务数据查询

🔄 多种策略回测（定投、动量、资产配置、网格、海龟等）

🤖 模拟交易和社区策略

# 用户操作
## 1获取用户信息
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例49：获取用户信息
# ============================================================
"""
参数说明：
    user: str = '小果'     - 用户名称

返回数据：
    username         - 用户名
    expiry           - 账户到期时间
    days_until_expiry - 剩余天数
    expiry_warning   - 是否即将到期
"""

print("\n" + "=" * 60)
print("📊 获取用户信息")
print("=" * 60)

result = client.get_user_info()
print("用户信息：")
print(result)
```
## 2检查授权码有效性
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例50：检查授权码有效性
# ============================================================
"""
参数说明：
    user: str = '小果'     - 用户名称

返回数据：
    status           - 状态（success/failed）
    message          - 消息
    user_info        - 用户信息
"""

print("\n" + "=" * 60)
print("📊 检查授权码有效性")
print("=" * 60)

result = client.check_password_is_av_user()
print("授权码检查结果：")
print(result)
```
## 3读取个人全部模拟策略
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例71：读取个人全部模拟策略
# ============================================================
"""
参数说明：
    user: str = '小果'           - 用户名称

返回数据：
    strategies       - 策略列表（包含策略类型、名称、建立时间等）
    total            - 策略总数
"""

print("\n" + "=" * 60)
print("📊 读取个人全部模拟策略")
print("=" * 60)

result = client.get_all_moni_trader_data(
    user='小果'
)
print("模拟策略列表：")
print(f"策略总数: {result.get('total', 0)}")
strategies = result.get('strategies', [])
for i, s in enumerate(strategies, 1):
    print(f"  {i}. {s.get('策略类型')} - {s.get('策略名称')} (建立时间: {s.get('建立时间')})")
```
## 4读取个人全部社区策略
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例72：读取个人全部社区策略
# ============================================================
"""
参数说明：
    user: str = '小果'           - 用户名称

返回数据：
    strategies       - 策略列表（包含策略类型、名称、建立时间等）
    total            - 策略总数
"""

print("\n" + "=" * 60)
print("📊 读取个人全部社区策略")
print("=" * 60)

result = client.get_all_moni_trader_data_sq(
    user='小果'
)
print("社区策略列表：")
print(f"策略总数: {result.get('total', 0)}")
strategies = result.get('strategies', [])
for i, s in enumerate(strategies, 1):
    print(f"  {i}. {s.get('策略类型')} - {s.get('策略名称')} (建立时间: {s.get('建立时间')})")
```
## 5删除单个模拟策略
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例67：删除单个模拟策略
# ============================================================
"""
参数说明：
    user: str = '小果'           - 用户名称
    st_type: str = '定投策略'     - 策略类型
    st_name: str = '小果定投模拟策略公开' - 策略名称
    open_show: str = '是'        - 是否公开策略

策略类型可选值：
    '定投策略'、'动量策略'、'资产配置策略'、
    '资产配置平衡策略'、'网格策略'、'海龟策略'、
    '综合动量策略'、'条件因子策略'、'排序多因子策略'、
    '均值方差策略'
"""

print("\n" + "=" * 60)
print("📊 删除单个模拟策略")
print("=" * 60)

result = client.del_moni_trader_data(
    user='小果',
    st_type='定投策略',
    st_name='小果定投模拟策略公开',
    open_show='是'
)
print("删除结果：")
print(result)
```
## 6删除单个社区策略
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例68：删除单个社区策略
# ============================================================
"""
参数说明：
    user: str = '小果'           - 用户名称
    st_type: str = '定投策略'     - 策略类型
    st_name: str = '小果定投模拟策略公开' - 策略名称
    open_show: str = '是'        - 是否公开策略
"""

print("\n" + "=" * 60)
print("📊 删除单个社区策略")
print("=" * 60)

result = client.del_moni_trader_data_sq(
    user='小果',
    st_type='定投策略',
    st_name='小果定投模拟策略公开',
    open_show='是'
)
print("删除结果：")
print(result)
```
## 7删除个人全部模拟策略
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例69：删除全部模拟策略
# ============================================================
"""
参数说明：
    user: str = '小果'           - 用户名称
    confirm: str = '是'          - 确认删除（必须为'是'才能执行）

⚠️ 警告：此操作将删除该用户的所有模拟策略，不可恢复！
"""

print("\n" + "=" * 60)
print("📊 删除全部模拟策略")
print("=" * 60)

result = client.del_all_moni_trader_data(
    user='小果',
    confirm='是'
)
print("删除结果：")
print(result)
```
## 8删除全部社区策略
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例70：删除全部社区策略
# ============================================================
"""
参数说明：
    user: str = '小果'           - 用户名称
    confirm: str = '是'          - 确认删除（必须为'是'才能执行）

⚠️ 警告：此操作将删除该用户的所有社区策略，不可恢复！
"""

print("\n" + "=" * 60)
print("📊 删除全部社区策略")
print("=" * 60)

result = client.del_all_moni_trader_data_sq(
    user='小果',
    confirm='是'
)
print("删除结果：")
print(result)
```
# 二、使用教程

## 1. 安装依赖并初始化
```python
# ============================================================
# 完整示例1：初始化客户端
# ============================================================
"""
参数说明：
    url: str = "数据库服务器"     - 服务器地址
    port: int = 数据库端口                 - 服务器端口
    user: str = "小果"              - 用户名
    password: str = "小果"          - 密码
    auth_code: str = "小果"         - 授权码
"""

import requests
import json
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

print("✅ 客户端初始化成功！")
print(f"📡 服务器地址: http://数据库服务器:数据库端口")
```

## 2. 获取股票历史行情数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例2：获取历史行情数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码，格式：代码.市场（SH/SZ）
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD

返回字段：
    date        - 交易日期
    open        - 开盘价
    high        - 最高价
    low         - 最低价
    close       - 收盘价
    volume      - 成交量
    amount      - 成交金额
    zdf         - 涨跌幅
    pct_chg     - 百分比变化
"""

print("\n" + "=" * 60)
print("📊 获取历史行情数据")
print("=" * 60)

# 获取单只股票历史数据
result = client.get_stock_hist_data(
    stock='513100.SH',      # 平安银行
    start_date='20240101',
    end_date='20500101'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
print(f"\n数据列: {df.columns.tolist()}")
```
## 3读取ETF基金历史行情数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例2：获取历史行情数据
# ============================================================
"""
参数说明：
    stock: str = '513100.SH'        - 股票代码，格式：代码.市场（SH/SZ）
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD

返回字段：
    date        - 交易日期
    open        - 开盘价
    high        - 最高价
    low         - 最低价
    close       - 收盘价
    volume      - 成交量
    amount      - 成交金额
    zdf         - 涨跌幅
    pct_chg     - 百分比变化
"""

print("\n" + "=" * 60)
print("📊 获取历史行情数据")
print("=" * 60)

# 获取单只股票历史数据
result = client.get_stock_hist_data(
    stock='513100.SH',      # 平安银行
    start_date='20240101',
    end_date='20500101'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
print(f"\n数据列: {df.columns.tolist()}")

```
## 4读取可转债历史行情数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例2：获取历史行情数据
# ============================================================
"""
参数说明：
    stock: str = '513100.SH'        - 股票代码，格式：代码.市场（SH/SZ）
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD

返回字段：
    date        - 交易日期
    open        - 开盘价
    high        - 最高价
    low         - 最低价
    close       - 收盘价
    volume      - 成交量
    amount      - 成交金额
    zdf         - 涨跌幅
    pct_chg     - 百分比变化
"""

print("\n" + "=" * 60)
print("📊 获取历史行情数据")
print("=" * 60)

# 获取单只股票历史数据
result = client.get_stock_hist_data(
    stock='128136.SZ',     
    start_date='20240101',
    end_date='20500101'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
print(f"\n数据列: {df.columns.tolist()}")

```
## 5. 获取股票因子数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例3：获取因子数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD
    columns: str = 'date,close,open,high,low,volume,amount'  - 选择字段，逗号分隔

【基础因子字段】
    date                - 交易日期
    证券代码            - 股票代码
    close               - 收盘价
    open                - 开盘价
    high                - 最高价
    low                 - 最低价
    volume              - 成交量
    amount              - 成交金额
    zdf                 - 涨跌幅

【涨跌幅因子】
    5日涨跌幅           - 5日涨跌幅
    10日涨跌幅          - 10日涨跌幅
    20日涨跌幅          - 20日涨跌幅
    30日涨跌幅          - 30日涨跌幅
    60日涨跌幅          - 60日涨跌幅
    120日涨跌幅         - 120日涨跌幅
    250日涨跌幅         - 250日涨跌幅

【价格距离均线涨跌幅】
    价格距离5日均线涨跌幅   - 价格距离5日均线涨跌幅
    价格距离10日均线涨跌幅  - 价格距离10日均线涨跌幅
    价格距离20日均线涨跌幅  - 价格距离20日均线涨跌幅
    价格距离30日均线涨跌幅  - 价格距离30日均线涨跌幅
    价格距离60日均线涨跌幅  - 价格距离60日均线涨跌幅
    价格距离120日均线涨跌幅 - 价格距离120日均线涨跌幅

【均线距离涨跌幅】
    5日均线距离10日均线涨跌幅  - 5日均线距离10日均线涨跌幅
    10日均线距离20日均线涨跌幅 - 10日均线距离20日均线涨跌幅
    20日均线距离30日均线涨跌幅 - 20日均线距离30日均线涨跌幅
    30日均线距离60日均线涨跌幅 - 30日均线距离60日均线涨跌幅
    60日均线距离120日均线涨跌幅 - 60日均线距离120日均线涨跌幅

【移动平均线】
    5日均线             - 5日均线
    10日均线            - 10日均线
    20日均线            - 20日均线
    30日均线            - 30日均线
    60日均线            - 60日均线
    120日均线           - 120日均线

【均线交叉信号】
    5日10日金叉         - 5日10日均线金叉
    10日20日金叉        - 10日20日均线金叉
    20日30日金叉        - 20日30日均线金叉
    30日60日金叉        - 30日60日均线金叉
    60日120日金叉       - 60日120日均线金叉
    5日10日死叉         - 5日10日均线死叉
    10日20日死叉        - 10日20日均线死叉
    20日30日死叉        - 20日30日均线死叉
    30日60日死叉        - 30日60日均线死叉
    60日120日死叉       - 60日120日均线死叉

【价格位置判断】
    价格在5均线上        - 价格是否在5日均线上
    价格在10均线上       - 价格是否在10日均线上
    价格在20均线上       - 价格是否在20日均线上
    价格在30均线上       - 价格是否在30日均线上
    价格在60均线上       - 价格是否在60日均线上
    价格在120均线上      - 价格是否在120日均线上
    5均线在10均线上      - 5日均线是否在10日均线上
    10均线在20均线上     - 10日均线是否在20日均线上
    20均线在30均线上     - 20日均线是否在30日均线上
    30均线在60均线上     - 30日均线是否在60日均线上
    60均线在120均线上    - 60日均线是否在120日均线上

【技术指标 - KDJ】
    KDJ_K               - KDJ指标K值
    KDJ_D               - KDJ指标D值
    KDJ_J               - KDJ指标J值
    KDJ_KD金叉          - KDJ金叉信号
    KDJ_KD死叉          - KDJ死叉信号

【技术指标 - MACD】
    MACD_DIF            - MACD平滑异同平均线DIF
    MACD_DEA            - MACD平滑异同平均线DEA
    MACD_MACD           - MACD平滑异同平均线MACD
    MACD_金叉           - MACD金叉信号
    MACD_死叉           - MACD死叉信号

【技术指标 - RSI】
    RSI1                - RSI相对强弱RSI1
    RSI2                - RSI相对强弱RSI2
    RSI3                - RSI相对强弱RSI3
    RSI_金叉            - RSI金叉信号
    RSI_死叉            - RSI死叉信号

【技术指标 - BOLL布林线】
    BOLL_BOLL           - BOLL布林线中轨
    BOLL_UB             - BOLL布林线上轨
    BOLL_LB             - BOLL布林线下轨

【技术指标 - CCI】
    CCI                 - CCI商品路径指标

【技术指标 - MFI】
    MFI                 - MFI资金流量指标

【技术指标 - MTM】
    MTM_MTM             - MTM动量线MTM值
    MTM_MTMMA           - MTM动量线MTMMA值

【技术指标 - SKDJ】
    SKDJ_K              - SKDJ慢速随机K值
    SKDJ_D              - SKDJ慢速随机D值

【技术指标 - WR】
    WR1                 - WR威廉指标WR1
    WR2                 - WR威廉指标WR2
    WR_金叉             - WR金叉信号
    WR_死叉             - WR死叉信号

【技术指标 - PSY】
    PSY_PSY             - PSY心理线PSY
    PSY_PSYMA           - PSY心理线PSYMA
    PSY_金叉            - PSY金叉信号
    PSY_死叉            - PSY死叉信号

【技术指标 - BIAS乖离率】
    BIAS1               - BIAS乖离率BIAS1
    BIAS2               - BIAS乖离率BIAS2
    BIAS3               - BIAS乖离率BIAS3
    BIAS_QL_BIAS        - BIAS_QL乖离率传统版BIAS值
    BIAS_QL_BIASMA      - BIAS_QL乖离率传统版BIASMA值
    BIAS36_BIAS36       - BIAS36三六乖离BIAS36
    BIAS36_BIAS612      - BIAS36三六乖离BIAS612
    BIAS36_MABIAS       - BIAS36三六乖离MABIAS

【技术指标 - DMI】
    DMI_PDI             - DMI趋向指标PDI
    DMI_MDI             - DMI趋向指标MDI
    DMI_ADX             - DMI趋向指标ADX
    DMI_ADXR            - DMI趋向指标ADXR

【技术指标 - DMA】
    DMA_XT_DIF          - DMA_XT平均差DIF
    DMA_XT_DIFMA        - DMA_XT平均差DIFMA

【技术指标 - DPO】
    DPO_DPO             - DPO区间震荡线DPO
    DPO_MADPO           - DPO区间震荡线MADPO

【技术指标 - EMV】
    EMV_EMV             - EMV简易波动指标EMV
    EMV_MAEMV           - EMV简易波动指标MAEMV

【技术指标 - TRIX】
    TRIX_TRIX           - TRIX三重指数平均线TRIX
    TRIX_MATRIX         - TRIX三重指数平均线MATRIX

【技术指标 - UOS】
    UOS_UOS             - UOS终极指标UOS
    UOS_MAUOS           - UOS终极指标MAUOS

【技术指标 - VPT】
    VTP_VPT             - VPT量价曲线VPT
    VTP_MAVP            - VPT量价曲线MAVP

【技术指标 - WVAD】
    WVAD_WVAD           - WVAD威廉变异离散量WVAD
    WVAD_MAWVAD         - WVAD威廉变异离散量MAWVAD

【技术指标 - BRAR】
    BRAR_BR             - BRAR情绪指标BR
    BRAR_AR             - BRAR情绪指标AR

【技术指标 - CR】
    CR_CR               - CR带状能量线CR
    CR_MA1              - CR带状能量线MA1
    CR_MA2              - CR带状能量线MA2
    CR_MA3              - CR带状能量线MA3
    CR_MA4              - CR带状能量线MA4

【技术指标 - MASS】
    MASS_MASS           - MASS梅斯线MASS
    MASS_MAMASS         - MASS梅斯线MAMASS

【技术指标 - VR】
    VR_VR               - VR成交量变异率VR
    VR_MAVR             - VR成交量变异率MAVR

【技术指标 - OBV】
    OBV_OBV             - OBV累积能量线OBV
    OBV_MAOBV           - OBV累积能量线MAOBV

【技术指标 - VOL成交量】
    VOL_XT_MAVOL1       - VOL成交量MAVOL1
    VOL_XT_MAVOL2       - VOL成交量MAVOL2

【技术指标 - VRSI】
    VRSI1               - VRSI相对强弱量RSI1
    VRSI2               - VRSI相对强弱量RSI2
    VRSI3               - VRSI相对强弱量RSI3

【技术指标 - HSL换手线】
    HSL_HSL             - HSL换手线HSL
    HSL_MAHSL           - HSL换手线MAHSL

【技术指标 - ACD】
    ACD_ACD             - ACD升降线ACD
    ACD_MAACD           - ACD升降线MAACD

【技术指标 - BBI】
    BBI                 - BBI多空均线

【技术指标 - EXPMA】
    EXPMA_EXP1          - EXPMA指数平均线EXP1
    EXPMA_EXP2          - EXPMA指数平均线EXP2

【技术指标 - SAR】
    SAR                 - SAR抛物线指标

【技术指标 - AMO成交金额】
    AMO_AMOW            - AMO成交金额AMOW
    AMO_AMO1            - AMO成交金额AMO1
    AMO_AMO2            - AMO成交金额AMO2

【技术指标 - MIKE】
    MIKE_STOR           - MIKE麦克支撑压力STOR
    MIKE_MIDR           - MIKE麦克支撑压力MIDR
    MIKE_WEKR           - MIKE麦克支撑压力WEKR
    MIKE_WEKS           - MIKE麦克支撑压力WEKS
    MIKE_MIDS           - MIKE麦克支撑压力MIDS
    MIKE_STOS           - MIKE麦克支撑压力STOS

【技术指标 - ENE】
    ENE_UPPER           - ENE轨道线上轨
    ENE_LOWER           - ENE轨道线下轨
    ENE_ENE             - ENE轨道线ENE

【技术指标 - PBX瀑布线】
    PBX_PBX1            - PBX瀑布线PBX1
    PBX_PBX2            - PBX瀑布线PBX2
    PBX_PBX3            - PBX瀑布线PBX3
    PBX_PBX4            - PBX瀑布线PBX4
    PBX_PBX5            - PBX瀑布线PBX5
    PBX_PBX6            - PBX瀑布线PBX6

【技术指标 - XS薛斯通道】
    XS_SUP              - XS薛斯通道SUP
    XS_SDN              - XS薛斯通道SDN
    XS_LUP              - XS薛斯通道LUP
    XS_LDN              - XS薛斯通道LDN

【技术指标 - TQN唐奇安通道】
    TQN_周期高点        - TQN唐奇安通道周期高点
    TQN_周期低点        - TQN唐奇安通道周期低点
    TQN_平空开多        - TQN唐奇安通道平空开多信号
    TQN_平多开空        - TQN唐奇安通道平多开空信号

【技术指标 - ALLIGAT鳄鱼线】
    ALLIGAT_上唇        - ALLIGAT鳄鱼线上唇
    ALLIGAT_牙齿        - ALLIGAT鳄鱼线牙齿
    ALLIGAT_下颚        - ALLIGAT鳄鱼线下颚

【技术指标 - GMMA顾比均线】
    GMMA_MA3            - GMMA顾比均线MA3
    GMMA_MA5            - GMMA顾比均线MA5
    GMMA_MA8            - GMMA顾比均线MA8
    GMMA_MA10           - GMMA顾比均线MA10
    GMMA_MA12           - GMMA顾比均线MA12
    GMMA_MA15           - GMMA顾比均线MA15
    GMMA_MA30           - GMMA顾比均线MA30
    GMMA_MA35           - GMMA顾比均线MA35
    GMMA_MA40           - GMMA顾比均线MA40
    GMMA_MA45           - GMMA顾比均线MA45
    GMMA_MA50           - GMMA顾比均线MA50
    GMMA_MA60           - GMMA顾比均线MA60

【技术指标 - VMACD】
    VMACD_DIF           - VMACD量平滑异同平均线DIF
    VMACD_DEA           - VMACD量平滑异同平均线DEA
    VMACD_MACD          - VMACD量平滑异同平均线MACD

【技术指标 - SMACD】
    SMACD_DEA           - SMACD单线平滑异同平均线DEA
    SMACD_MACD          - SMACD单线平滑异同平均线MACD

【技术指标 - QACD】
    QACD_DIF            - QACD快速异同平均线DIF
    QACD_MACD           - QACD快速异同平均线MACD
    QACD_DDIF           - QACD快速异同平均线DDIF

【技术指标 - 成交量相关】
    连续上涨天数        - 连续上涨天数
    连续下跌天数        - 连续下跌天数

【技术指标 - 偏度峰度】
    5日偏度             - 5日偏度
    10日偏度            - 10日偏度
    20日偏度            - 20日偏度
    30日偏度            - 30日偏度
    60日偏度            - 60日偏度
    120日偏度           - 120日偏度
    5日峰度             - 5日峰度
    10日峰度            - 10日峰度
    20日峰度            - 20日峰度
    30日峰度            - 30日峰度
    60日峰度            - 60日峰度
    120日峰度           - 120日峰度

【Alpha因子 - 世界金融实验室101因子】
    Alpha001 至 Alpha191 - 世界金融实验室101因子（共191个）

【交易信号因子】
    六脉神剑            - 六脉神剑交易信号
    小波段交易          - 小波段交易信号
    大波段交易          - 大波段交易信号
    波段超级买卖        - 波段超级买卖信号

【回归分析因子】
    3日回归动量         - 3日回归动量
    5日回归动量         - 5日回归动量
    7日回归动量         - 7日回归动量
    9日回归动量         - 9日回归动量
    12日回归动量        - 12日回归动量
    15日回归动量        - 15日回归动量
    18日回归动量        - 18日回归动量
    20日回归动量        - 20日回归动量
    23日回归动量        - 23日回归动量
    25日回归动量        - 25日回归动量
    28日回归动量        - 28日回归动量
    30日回归动量        - 30日回归动量
    35日回归动量        - 35日回归动量
    40日回归动量        - 40日回归动量
    45日回归动量        - 45日回归动量
    50日回归动量        - 50日回归动量
    60日回归动量        - 60日回归动量

【回归斜率】
    5日回归斜率         - 5日回归斜率
    10日回归斜率        - 10日回归斜率
    20日回归斜率        - 20日回归斜率
    30日回归斜率        - 30日回归斜率
    60日回归斜率        - 60日回归斜率
    120日回归斜率       - 120日回归斜率

【标准差】
    5日标准差           - 5日标准差
    10日标准差          - 10日标准差
    20日标准差          - 20日标准差
    30日标准差          - 30日标准差
    60日标准差          - 60日标准差
    120日标准差         - 120日标准差

【最高最低值周期】
    5日最高值到当前周期   - 5日最高值到当前周期
    10日最高值到当前周期  - 10日最高值到当前周期
    20日最高值到当前周期  - 20日最高值到当前周期
    30日最高值到当前周期  - 30日最高值到当前周期
    60日最高值到当前周期  - 60日最高值到当前周期
    120日最高值到当前周期 - 120日最高值到当前周期
    5日最低值到当前周期   - 5日最低值到当前周期
    10日最低值到当前周期  - 10日最低值到当前周期
    20日最低值到当前周期  - 20日最低值到当前周期
    30日最低值到当前周期  - 30日最低值到当前周期
    60日最低值到当前周期  - 60日最低值到当前周期
    120日最低值到当前周期 - 120日最低值到当前周期

【Alpha系数】
    5日Alpha            - 5日Alpha
    10日Alpha           - 10日Alpha
    20日Alpha           - 20日Alpha
    30日Alpha           - 30日Alpha
    60日Alpha           - 60日Alpha
    120日Alpha          - 120日Alpha

【Beta系数】
    5日Beta             - 5日Beta
    10日Beta            - 10日Beta
    20日Beta            - 20日Beta
    30日Beta            - 30日Beta
    60日Beta            - 60日Beta
    120日Beta           - 120日Beta

【夏普比率】
    5日夏普比率         - 5日夏普比率
    10日夏普比率        - 10日夏普比率
    20日夏普比率        - 20日夏普比率
    30日夏普比率        - 30日夏普比率
    60日夏普比率        - 60日夏普比率
    120日夏普比率       - 120日夏普比率

【年化波动率】
    5日年化波动率       - 5日年化波动率
    10日年化波动率      - 10日年化波动率
    20日年化波动率      - 20日年化波动率
    30日年化波动率      - 30日年化波动率
    60日年化波动率      - 60日年化波动率
    120日年化波动率     - 120日年化波动率

【最大回撤】
    5日最大回撤         - 5日最大回撤
    10日最大回撤        - 10日最大回撤
    20日最大回撤        - 20日最大回撤
    30日最大回撤        - 30日最大回撤
    60日最大回撤        - 60日最大回撤
    120日最大回撤       - 120日最大回撤

【上涨/下跌捕获率】
    5日上涨捕获率       - 5日上涨捕获率
    10日上涨捕获率      - 10日上涨捕获率
    20日上涨捕获率      - 20日上涨捕获率
    30日上涨捕获率      - 30日上涨捕获率
    60日上涨捕获率      - 60日上涨捕获率
    120日上涨捕获率     - 120日上涨捕获率
    5日下跌捕获率       - 5日下跌捕获率
    10日下跌捕获率      - 10日下跌捕获率
    20日下跌捕获率      - 20日下跌捕获率
    30日下跌捕获率      - 30日下跌捕获率
    60日下跌捕获率      - 60日下跌捕获率
    120日下跌捕获率     - 120日下跌捕获率

【庄家/主力指标】
    ZJTJ_无庄控盘       - ZJTJ庄家抬轿无庄控盘
    ZJTJ_开始控盘       - ZJTJ庄家抬轿开始控盘
    ZJTJ_有庄控盘       - ZJTJ庄家抬轿有庄控盘
    ZJTJ_主力出货       - ZJTJ庄家抬轿主力出货
    CYW                 - CYW主力控盘
    ZLJC_JCS            - ZLJC主力进出JCS
    ZLJC_JCM            - ZLJC主力进出JCM
    ZLJC_JCL            - ZLJC主力进出JCL
    ZLMM_MMS            - ZLMM主力买卖MMS
    ZLMM_MMM            - ZLMM主力买卖MMM
    ZLMM_MML            - ZLMM主力买卖MML
    LHXJ_主力弃盘       - LHXJ猎狐先觉主力弃盘
    LHXJ_主力控盘       - LHXJ猎狐先觉主力控盘
    LYJH_机构做空能量线  - LYJH猎鹰歼狐机构做空能量线
    LYJH_机构做多能量线  - LYJH猎鹰歼狐机构做多能量线

【智能交易信号】
    BDZX_AK             - BDZX波段之星AK
    BDZX_AD1            - BDZX波段之星AD1
    BDZX_AJ             - BDZX波段之星AJ
    BDZX_买进           - BDZX波段之星买进信号
    BDZX_卖出           - BDZX波段之星卖出信号
    CYHT_SK             - CYHT财运亨通SK
    CYHT_SD             - CYHT财运亨通SD
    CYHT_卖出           - CYHT财运亨通卖出信号
    CYHT_买进           - CYHT财运亨通买进信号
    BSQJ_B买            - BSQJ买卖区间B买信号
    BSQJ_持仓           - BSQJ买卖区间持仓信号
    BSQJ_S卖            - BSQJ买卖区间S卖信号
    BSQJ_空仓           - BSQJ买卖区间空仓信号
    JFZX_多头力量       - JFZX飓风智能中线多头力量
    JFZX_空头力量       - JFZX飓风智能中线空头力量
    XJDX_J              - XJDX超级短线J
    XJDX_D              - XJDX超级短线D
    XJDX_K              - XJDX超级短线K

【其他特色指标】
    CYS                 - CYS市场盈亏
    CYR_CYR             - CYR市场强弱CYR
    CYR_MACYR           - CYR市场强弱MACYR
    CYE_CYEL            - CYE市场趋势CYEL
    CYE_CYES            - CYE市场趋势CYES
    CYS                 - CYS市场盈亏
    RAD_RADER1          - RAD威力雷达RADER1
    RAD_RADERMA         - RAD威力雷达RADERMA
    SG_XDT_QR           - SG_XDT心电图QR
    SG_XDT_MQR1         - SG_XDT心电图MQR1
    SG_XDT_MQR2         - SG_XDT心电图MQR2
    SG_NDB_DK           - SG_NDB脑电波DK
    SG_NDB_MDK1         - SG_NDB脑电波MDK1
    SG_NDB_MDK2         - SG_NDB脑电波MDK2
    SG_SMX_ZY1          - SG_SMX生命线ZY1
    SG_SMX_ZY2          - SG_SMX生命线ZY2
    SG_SMX_ZY3          - SG_SMX生命线ZY3
    SG_LB_量比          - SG_LB量比
    SG_LB_MA5           - SG_LB量比MA5
    SG_LB_MA10          - SG_LB量比MA10
    SG_PF               - SG_PF强势股评分
    SLZT_白龙           - SLZT神龙在天白龙
    SLZT_黄龙           - SLZT神龙在天黄龙
    SLZT_紫龙           - SLZT神龙在天紫龙
    SLZT_青龙           - SLZT神龙在天青龙
    SLZT_红龙           - SLZT神龙在天红龙
    SLZT_蓝龙           - SLZT神龙在天蓝龙
    ADVOL_ADVOL         - ADVOL龙系离散量ADVOL
    ADVOL_MA1           - ADVOL龙系离散量MA1
    ADVOL_MA2           - ADVOL龙系离散量MA2
    JAX_J               - JAX济安线J
    JAX_A               - JAX济安线A
    JAX_X               - JAX济安线X
    LON_LON             - LON龙系长线LON
    LON_LONMA           - LON龙系长线LONMA
    LON_LONT            - LON龙系长线LONT
    SHT_SHT             - SHT龙系短线SHT
    SHT_SHTMA           - SHT龙系短线SHTMA
    CDP_STD_CDP         - CDP_STD逆势操作CDP
    CDP_STD_AH          - CDP_STD逆势操作AH
    CDP_STD_NH          - CDP_STD逆势操作NH
    CDP_STD_NL          - CDP_STD逆势操作NL
    CDP_STD_AL          - CDP_STD逆势操作AL
"""

print("\n" + "=" * 60)
print("📈 获取因子数据")
print("=" * 60)

# 获取基础因子数据
result = client.get_stock_factor_data(
    stock='513100.SH',      # 纳指ETF
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,high,low,volume,amount'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取涨跌幅因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='159915.SZ',      # 创业板ETF
    start_date='20220101',
    end_date='20241231',
    columns='date,证券代码,5日涨跌幅,10日涨跌幅,20日涨跌幅,60日涨跌幅'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取技术指标因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,MACD_DIF,MACD_DEA,MACD_MACD,KDJ_K,KDJ_D,KDJ_J,RSI1,RSI2,RSI3,BOLL_BOLL,BOLL_UB,BOLL_LB'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（技术指标）")
print(df.head())

# 获取均线系统因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,5日均线,10日均线,20日均线,30日均线,60日均线,120日均线'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（均线系统）")
print(df.head())

# 获取Alpha因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,Alpha001,Alpha002,Alpha003,Alpha004,Alpha005'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（Alpha因子）")
print(df.head())

# 获取动量因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,3日回归动量,5日回归动量,10日回归动量,20日回归动量,30日回归动量,60日回归动量'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（动量因子）")
print(df.head())
```
## 6读取ETF基金因子数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例3：获取因子数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD
    columns: str = 'date,close,open,high,low,volume,amount'  - 选择字段，逗号分隔

【基础因子字段】
    date                - 交易日期
    证券代码            - 股票代码
    close               - 收盘价
    open                - 开盘价
    high                - 最高价
    low                 - 最低价
    volume              - 成交量
    amount              - 成交金额
    zdf                 - 涨跌幅

【涨跌幅因子】
    5日涨跌幅           - 5日涨跌幅
    10日涨跌幅          - 10日涨跌幅
    20日涨跌幅          - 20日涨跌幅
    30日涨跌幅          - 30日涨跌幅
    60日涨跌幅          - 60日涨跌幅
    120日涨跌幅         - 120日涨跌幅
    250日涨跌幅         - 250日涨跌幅

【价格距离均线涨跌幅】
    价格距离5日均线涨跌幅   - 价格距离5日均线涨跌幅
    价格距离10日均线涨跌幅  - 价格距离10日均线涨跌幅
    价格距离20日均线涨跌幅  - 价格距离20日均线涨跌幅
    价格距离30日均线涨跌幅  - 价格距离30日均线涨跌幅
    价格距离60日均线涨跌幅  - 价格距离60日均线涨跌幅
    价格距离120日均线涨跌幅 - 价格距离120日均线涨跌幅

【均线距离涨跌幅】
    5日均线距离10日均线涨跌幅  - 5日均线距离10日均线涨跌幅
    10日均线距离20日均线涨跌幅 - 10日均线距离20日均线涨跌幅
    20日均线距离30日均线涨跌幅 - 20日均线距离30日均线涨跌幅
    30日均线距离60日均线涨跌幅 - 30日均线距离60日均线涨跌幅
    60日均线距离120日均线涨跌幅 - 60日均线距离120日均线涨跌幅

【移动平均线】
    5日均线             - 5日均线
    10日均线            - 10日均线
    20日均线            - 20日均线
    30日均线            - 30日均线
    60日均线            - 60日均线
    120日均线           - 120日均线

【均线交叉信号】
    5日10日金叉         - 5日10日均线金叉
    10日20日金叉        - 10日20日均线金叉
    20日30日金叉        - 20日30日均线金叉
    30日60日金叉        - 30日60日均线金叉
    60日120日金叉       - 60日120日均线金叉
    5日10日死叉         - 5日10日均线死叉
    10日20日死叉        - 10日20日均线死叉
    20日30日死叉        - 20日30日均线死叉
    30日60日死叉        - 30日60日均线死叉
    60日120日死叉       - 60日120日均线死叉

【价格位置判断】
    价格在5均线上        - 价格是否在5日均线上
    价格在10均线上       - 价格是否在10日均线上
    价格在20均线上       - 价格是否在20日均线上
    价格在30均线上       - 价格是否在30日均线上
    价格在60均线上       - 价格是否在60日均线上
    价格在120均线上      - 价格是否在120日均线上
    5均线在10均线上      - 5日均线是否在10日均线上
    10均线在20均线上     - 10日均线是否在20日均线上
    20均线在30均线上     - 20日均线是否在30日均线上
    30均线在60均线上     - 30日均线是否在60日均线上
    60均线在120均线上    - 60日均线是否在120日均线上

【技术指标 - KDJ】
    KDJ_K               - KDJ指标K值
    KDJ_D               - KDJ指标D值
    KDJ_J               - KDJ指标J值
    KDJ_KD金叉          - KDJ金叉信号
    KDJ_KD死叉          - KDJ死叉信号

【技术指标 - MACD】
    MACD_DIF            - MACD平滑异同平均线DIF
    MACD_DEA            - MACD平滑异同平均线DEA
    MACD_MACD           - MACD平滑异同平均线MACD
    MACD_金叉           - MACD金叉信号
    MACD_死叉           - MACD死叉信号

【技术指标 - RSI】
    RSI1                - RSI相对强弱RSI1
    RSI2                - RSI相对强弱RSI2
    RSI3                - RSI相对强弱RSI3
    RSI_金叉            - RSI金叉信号
    RSI_死叉            - RSI死叉信号

【技术指标 - BOLL布林线】
    BOLL_BOLL           - BOLL布林线中轨
    BOLL_UB             - BOLL布林线上轨
    BOLL_LB             - BOLL布林线下轨

【技术指标 - CCI】
    CCI                 - CCI商品路径指标

【技术指标 - MFI】
    MFI                 - MFI资金流量指标

【技术指标 - MTM】
    MTM_MTM             - MTM动量线MTM值
    MTM_MTMMA           - MTM动量线MTMMA值

【技术指标 - SKDJ】
    SKDJ_K              - SKDJ慢速随机K值
    SKDJ_D              - SKDJ慢速随机D值

【技术指标 - WR】
    WR1                 - WR威廉指标WR1
    WR2                 - WR威廉指标WR2
    WR_金叉             - WR金叉信号
    WR_死叉             - WR死叉信号

【技术指标 - PSY】
    PSY_PSY             - PSY心理线PSY
    PSY_PSYMA           - PSY心理线PSYMA
    PSY_金叉            - PSY金叉信号
    PSY_死叉            - PSY死叉信号

【技术指标 - BIAS乖离率】
    BIAS1               - BIAS乖离率BIAS1
    BIAS2               - BIAS乖离率BIAS2
    BIAS3               - BIAS乖离率BIAS3
    BIAS_QL_BIAS        - BIAS_QL乖离率传统版BIAS值
    BIAS_QL_BIASMA      - BIAS_QL乖离率传统版BIASMA值
    BIAS36_BIAS36       - BIAS36三六乖离BIAS36
    BIAS36_BIAS612      - BIAS36三六乖离BIAS612
    BIAS36_MABIAS       - BIAS36三六乖离MABIAS

【技术指标 - DMI】
    DMI_PDI             - DMI趋向指标PDI
    DMI_MDI             - DMI趋向指标MDI
    DMI_ADX             - DMI趋向指标ADX
    DMI_ADXR            - DMI趋向指标ADXR

【技术指标 - DMA】
    DMA_XT_DIF          - DMA_XT平均差DIF
    DMA_XT_DIFMA        - DMA_XT平均差DIFMA

【技术指标 - DPO】
    DPO_DPO             - DPO区间震荡线DPO
    DPO_MADPO           - DPO区间震荡线MADPO

【技术指标 - EMV】
    EMV_EMV             - EMV简易波动指标EMV
    EMV_MAEMV           - EMV简易波动指标MAEMV

【技术指标 - TRIX】
    TRIX_TRIX           - TRIX三重指数平均线TRIX
    TRIX_MATRIX         - TRIX三重指数平均线MATRIX

【技术指标 - UOS】
    UOS_UOS             - UOS终极指标UOS
    UOS_MAUOS           - UOS终极指标MAUOS

【技术指标 - VPT】
    VTP_VPT             - VPT量价曲线VPT
    VTP_MAVP            - VPT量价曲线MAVP

【技术指标 - WVAD】
    WVAD_WVAD           - WVAD威廉变异离散量WVAD
    WVAD_MAWVAD         - WVAD威廉变异离散量MAWVAD

【技术指标 - BRAR】
    BRAR_BR             - BRAR情绪指标BR
    BRAR_AR             - BRAR情绪指标AR

【技术指标 - CR】
    CR_CR               - CR带状能量线CR
    CR_MA1              - CR带状能量线MA1
    CR_MA2              - CR带状能量线MA2
    CR_MA3              - CR带状能量线MA3
    CR_MA4              - CR带状能量线MA4

【技术指标 - MASS】
    MASS_MASS           - MASS梅斯线MASS
    MASS_MAMASS         - MASS梅斯线MAMASS

【技术指标 - VR】
    VR_VR               - VR成交量变异率VR
    VR_MAVR             - VR成交量变异率MAVR

【技术指标 - OBV】
    OBV_OBV             - OBV累积能量线OBV
    OBV_MAOBV           - OBV累积能量线MAOBV

【技术指标 - VOL成交量】
    VOL_XT_MAVOL1       - VOL成交量MAVOL1
    VOL_XT_MAVOL2       - VOL成交量MAVOL2

【技术指标 - VRSI】
    VRSI1               - VRSI相对强弱量RSI1
    VRSI2               - VRSI相对强弱量RSI2
    VRSI3               - VRSI相对强弱量RSI3

【技术指标 - HSL换手线】
    HSL_HSL             - HSL换手线HSL
    HSL_MAHSL           - HSL换手线MAHSL

【技术指标 - ACD】
    ACD_ACD             - ACD升降线ACD
    ACD_MAACD           - ACD升降线MAACD

【技术指标 - BBI】
    BBI                 - BBI多空均线

【技术指标 - EXPMA】
    EXPMA_EXP1          - EXPMA指数平均线EXP1
    EXPMA_EXP2          - EXPMA指数平均线EXP2

【技术指标 - SAR】
    SAR                 - SAR抛物线指标

【技术指标 - AMO成交金额】
    AMO_AMOW            - AMO成交金额AMOW
    AMO_AMO1            - AMO成交金额AMO1
    AMO_AMO2            - AMO成交金额AMO2

【技术指标 - MIKE】
    MIKE_STOR           - MIKE麦克支撑压力STOR
    MIKE_MIDR           - MIKE麦克支撑压力MIDR
    MIKE_WEKR           - MIKE麦克支撑压力WEKR
    MIKE_WEKS           - MIKE麦克支撑压力WEKS
    MIKE_MIDS           - MIKE麦克支撑压力MIDS
    MIKE_STOS           - MIKE麦克支撑压力STOS

【技术指标 - ENE】
    ENE_UPPER           - ENE轨道线上轨
    ENE_LOWER           - ENE轨道线下轨
    ENE_ENE             - ENE轨道线ENE

【技术指标 - PBX瀑布线】
    PBX_PBX1            - PBX瀑布线PBX1
    PBX_PBX2            - PBX瀑布线PBX2
    PBX_PBX3            - PBX瀑布线PBX3
    PBX_PBX4            - PBX瀑布线PBX4
    PBX_PBX5            - PBX瀑布线PBX5
    PBX_PBX6            - PBX瀑布线PBX6

【技术指标 - XS薛斯通道】
    XS_SUP              - XS薛斯通道SUP
    XS_SDN              - XS薛斯通道SDN
    XS_LUP              - XS薛斯通道LUP
    XS_LDN              - XS薛斯通道LDN

【技术指标 - TQN唐奇安通道】
    TQN_周期高点        - TQN唐奇安通道周期高点
    TQN_周期低点        - TQN唐奇安通道周期低点
    TQN_平空开多        - TQN唐奇安通道平空开多信号
    TQN_平多开空        - TQN唐奇安通道平多开空信号

【技术指标 - ALLIGAT鳄鱼线】
    ALLIGAT_上唇        - ALLIGAT鳄鱼线上唇
    ALLIGAT_牙齿        - ALLIGAT鳄鱼线牙齿
    ALLIGAT_下颚        - ALLIGAT鳄鱼线下颚

【技术指标 - GMMA顾比均线】
    GMMA_MA3            - GMMA顾比均线MA3
    GMMA_MA5            - GMMA顾比均线MA5
    GMMA_MA8            - GMMA顾比均线MA8
    GMMA_MA10           - GMMA顾比均线MA10
    GMMA_MA12           - GMMA顾比均线MA12
    GMMA_MA15           - GMMA顾比均线MA15
    GMMA_MA30           - GMMA顾比均线MA30
    GMMA_MA35           - GMMA顾比均线MA35
    GMMA_MA40           - GMMA顾比均线MA40
    GMMA_MA45           - GMMA顾比均线MA45
    GMMA_MA50           - GMMA顾比均线MA50
    GMMA_MA60           - GMMA顾比均线MA60

【技术指标 - VMACD】
    VMACD_DIF           - VMACD量平滑异同平均线DIF
    VMACD_DEA           - VMACD量平滑异同平均线DEA
    VMACD_MACD          - VMACD量平滑异同平均线MACD

【技术指标 - SMACD】
    SMACD_DEA           - SMACD单线平滑异同平均线DEA
    SMACD_MACD          - SMACD单线平滑异同平均线MACD

【技术指标 - QACD】
    QACD_DIF            - QACD快速异同平均线DIF
    QACD_MACD           - QACD快速异同平均线MACD
    QACD_DDIF           - QACD快速异同平均线DDIF

【技术指标 - 成交量相关】
    连续上涨天数        - 连续上涨天数
    连续下跌天数        - 连续下跌天数

【技术指标 - 偏度峰度】
    5日偏度             - 5日偏度
    10日偏度            - 10日偏度
    20日偏度            - 20日偏度
    30日偏度            - 30日偏度
    60日偏度            - 60日偏度
    120日偏度           - 120日偏度
    5日峰度             - 5日峰度
    10日峰度            - 10日峰度
    20日峰度            - 20日峰度
    30日峰度            - 30日峰度
    60日峰度            - 60日峰度
    120日峰度           - 120日峰度

【Alpha因子 - 世界金融实验室101因子】
    Alpha001 至 Alpha191 - 世界金融实验室101因子（共191个）

【交易信号因子】
    六脉神剑            - 六脉神剑交易信号
    小波段交易          - 小波段交易信号
    大波段交易          - 大波段交易信号
    波段超级买卖        - 波段超级买卖信号

【回归分析因子】
    3日回归动量         - 3日回归动量
    5日回归动量         - 5日回归动量
    7日回归动量         - 7日回归动量
    9日回归动量         - 9日回归动量
    12日回归动量        - 12日回归动量
    15日回归动量        - 15日回归动量
    18日回归动量        - 18日回归动量
    20日回归动量        - 20日回归动量
    23日回归动量        - 23日回归动量
    25日回归动量        - 25日回归动量
    28日回归动量        - 28日回归动量
    30日回归动量        - 30日回归动量
    35日回归动量        - 35日回归动量
    40日回归动量        - 40日回归动量
    45日回归动量        - 45日回归动量
    50日回归动量        - 50日回归动量
    60日回归动量        - 60日回归动量

【回归斜率】
    5日回归斜率         - 5日回归斜率
    10日回归斜率        - 10日回归斜率
    20日回归斜率        - 20日回归斜率
    30日回归斜率        - 30日回归斜率
    60日回归斜率        - 60日回归斜率
    120日回归斜率       - 120日回归斜率

【标准差】
    5日标准差           - 5日标准差
    10日标准差          - 10日标准差
    20日标准差          - 20日标准差
    30日标准差          - 30日标准差
    60日标准差          - 60日标准差
    120日标准差         - 120日标准差

【最高最低值周期】
    5日最高值到当前周期   - 5日最高值到当前周期
    10日最高值到当前周期  - 10日最高值到当前周期
    20日最高值到当前周期  - 20日最高值到当前周期
    30日最高值到当前周期  - 30日最高值到当前周期
    60日最高值到当前周期  - 60日最高值到当前周期
    120日最高值到当前周期 - 120日最高值到当前周期
    5日最低值到当前周期   - 5日最低值到当前周期
    10日最低值到当前周期  - 10日最低值到当前周期
    20日最低值到当前周期  - 20日最低值到当前周期
    30日最低值到当前周期  - 30日最低值到当前周期
    60日最低值到当前周期  - 60日最低值到当前周期
    120日最低值到当前周期 - 120日最低值到当前周期

【Alpha系数】
    5日Alpha            - 5日Alpha
    10日Alpha           - 10日Alpha
    20日Alpha           - 20日Alpha
    30日Alpha           - 30日Alpha
    60日Alpha           - 60日Alpha
    120日Alpha          - 120日Alpha

【Beta系数】
    5日Beta             - 5日Beta
    10日Beta            - 10日Beta
    20日Beta            - 20日Beta
    30日Beta            - 30日Beta
    60日Beta            - 60日Beta
    120日Beta           - 120日Beta

【夏普比率】
    5日夏普比率         - 5日夏普比率
    10日夏普比率        - 10日夏普比率
    20日夏普比率        - 20日夏普比率
    30日夏普比率        - 30日夏普比率
    60日夏普比率        - 60日夏普比率
    120日夏普比率       - 120日夏普比率

【年化波动率】
    5日年化波动率       - 5日年化波动率
    10日年化波动率      - 10日年化波动率
    20日年化波动率      - 20日年化波动率
    30日年化波动率      - 30日年化波动率
    60日年化波动率      - 60日年化波动率
    120日年化波动率     - 120日年化波动率

【最大回撤】
    5日最大回撤         - 5日最大回撤
    10日最大回撤        - 10日最大回撤
    20日最大回撤        - 20日最大回撤
    30日最大回撤        - 30日最大回撤
    60日最大回撤        - 60日最大回撤
    120日最大回撤       - 120日最大回撤

【上涨/下跌捕获率】
    5日上涨捕获率       - 5日上涨捕获率
    10日上涨捕获率      - 10日上涨捕获率
    20日上涨捕获率      - 20日上涨捕获率
    30日上涨捕获率      - 30日上涨捕获率
    60日上涨捕获率      - 60日上涨捕获率
    120日上涨捕获率     - 120日上涨捕获率
    5日下跌捕获率       - 5日下跌捕获率
    10日下跌捕获率      - 10日下跌捕获率
    20日下跌捕获率      - 20日下跌捕获率
    30日下跌捕获率      - 30日下跌捕获率
    60日下跌捕获率      - 60日下跌捕获率
    120日下跌捕获率     - 120日下跌捕获率

【庄家/主力指标】
    ZJTJ_无庄控盘       - ZJTJ庄家抬轿无庄控盘
    ZJTJ_开始控盘       - ZJTJ庄家抬轿开始控盘
    ZJTJ_有庄控盘       - ZJTJ庄家抬轿有庄控盘
    ZJTJ_主力出货       - ZJTJ庄家抬轿主力出货
    CYW                 - CYW主力控盘
    ZLJC_JCS            - ZLJC主力进出JCS
    ZLJC_JCM            - ZLJC主力进出JCM
    ZLJC_JCL            - ZLJC主力进出JCL
    ZLMM_MMS            - ZLMM主力买卖MMS
    ZLMM_MMM            - ZLMM主力买卖MMM
    ZLMM_MML            - ZLMM主力买卖MML
    LHXJ_主力弃盘       - LHXJ猎狐先觉主力弃盘
    LHXJ_主力控盘       - LHXJ猎狐先觉主力控盘
    LYJH_机构做空能量线  - LYJH猎鹰歼狐机构做空能量线
    LYJH_机构做多能量线  - LYJH猎鹰歼狐机构做多能量线

【智能交易信号】
    BDZX_AK             - BDZX波段之星AK
    BDZX_AD1            - BDZX波段之星AD1
    BDZX_AJ             - BDZX波段之星AJ
    BDZX_买进           - BDZX波段之星买进信号
    BDZX_卖出           - BDZX波段之星卖出信号
    CYHT_SK             - CYHT财运亨通SK
    CYHT_SD             - CYHT财运亨通SD
    CYHT_卖出           - CYHT财运亨通卖出信号
    CYHT_买进           - CYHT财运亨通买进信号
    BSQJ_B买            - BSQJ买卖区间B买信号
    BSQJ_持仓           - BSQJ买卖区间持仓信号
    BSQJ_S卖            - BSQJ买卖区间S卖信号
    BSQJ_空仓           - BSQJ买卖区间空仓信号
    JFZX_多头力量       - JFZX飓风智能中线多头力量
    JFZX_空头力量       - JFZX飓风智能中线空头力量
    XJDX_J              - XJDX超级短线J
    XJDX_D              - XJDX超级短线D
    XJDX_K              - XJDX超级短线K

【其他特色指标】
    CYS                 - CYS市场盈亏
    CYR_CYR             - CYR市场强弱CYR
    CYR_MACYR           - CYR市场强弱MACYR
    CYE_CYEL            - CYE市场趋势CYEL
    CYE_CYES            - CYE市场趋势CYES
    CYS                 - CYS市场盈亏
    RAD_RADER1          - RAD威力雷达RADER1
    RAD_RADERMA         - RAD威力雷达RADERMA
    SG_XDT_QR           - SG_XDT心电图QR
    SG_XDT_MQR1         - SG_XDT心电图MQR1
    SG_XDT_MQR2         - SG_XDT心电图MQR2
    SG_NDB_DK           - SG_NDB脑电波DK
    SG_NDB_MDK1         - SG_NDB脑电波MDK1
    SG_NDB_MDK2         - SG_NDB脑电波MDK2
    SG_SMX_ZY1          - SG_SMX生命线ZY1
    SG_SMX_ZY2          - SG_SMX生命线ZY2
    SG_SMX_ZY3          - SG_SMX生命线ZY3
    SG_LB_量比          - SG_LB量比
    SG_LB_MA5           - SG_LB量比MA5
    SG_LB_MA10          - SG_LB量比MA10
    SG_PF               - SG_PF强势股评分
    SLZT_白龙           - SLZT神龙在天白龙
    SLZT_黄龙           - SLZT神龙在天黄龙
    SLZT_紫龙           - SLZT神龙在天紫龙
    SLZT_青龙           - SLZT神龙在天青龙
    SLZT_红龙           - SLZT神龙在天红龙
    SLZT_蓝龙           - SLZT神龙在天蓝龙
    ADVOL_ADVOL         - ADVOL龙系离散量ADVOL
    ADVOL_MA1           - ADVOL龙系离散量MA1
    ADVOL_MA2           - ADVOL龙系离散量MA2
    JAX_J               - JAX济安线J
    JAX_A               - JAX济安线A
    JAX_X               - JAX济安线X
    LON_LON             - LON龙系长线LON
    LON_LONMA           - LON龙系长线LONMA
    LON_LONT            - LON龙系长线LONT
    SHT_SHT             - SHT龙系短线SHT
    SHT_SHTMA           - SHT龙系短线SHTMA
    CDP_STD_CDP         - CDP_STD逆势操作CDP
    CDP_STD_AH          - CDP_STD逆势操作AH
    CDP_STD_NH          - CDP_STD逆势操作NH
    CDP_STD_NL          - CDP_STD逆势操作NL
    CDP_STD_AL          - CDP_STD逆势操作AL
"""

print("\n" + "=" * 60)
print("📈 获取因子数据")
print("=" * 60)

# 获取基础因子数据
result = client.get_stock_factor_data(
    stock='513100.SH',      # 纳指ETF
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,high,low,volume,amount'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取涨跌幅因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='159915.SZ',      # 创业板ETF
    start_date='20220101',
    end_date='20241231',
    columns='date,证券代码,5日涨跌幅,10日涨跌幅,20日涨跌幅,60日涨跌幅'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取技术指标因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,MACD_DIF,MACD_DEA,MACD_MACD,KDJ_K,KDJ_D,KDJ_J,RSI1,RSI2,RSI3,BOLL_BOLL,BOLL_UB,BOLL_LB'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（技术指标）")
print(df.head())

# 获取均线系统因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,5日均线,10日均线,20日均线,30日均线,60日均线,120日均线'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（均线系统）")
print(df.head())

# 获取Alpha因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,Alpha001,Alpha002,Alpha003,Alpha004,Alpha005'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（Alpha因子）")
print(df.head())

# 获取动量因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,3日回归动量,5日回归动量,10日回归动量,20日回归动量,30日回归动量,60日回归动量'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（动量因子）")
print(df.head())
```
## 7读取可转债因子数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例3：获取因子数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD
    columns: str = 'date,close,open,high,low,volume,amount'  - 选择字段，逗号分隔

【基础因子字段】
    date                - 交易日期
    证券代码            - 股票代码
    close               - 收盘价
    open                - 开盘价
    high                - 最高价
    low                 - 最低价
    volume              - 成交量
    amount              - 成交金额
    zdf                 - 涨跌幅

【涨跌幅因子】
    5日涨跌幅           - 5日涨跌幅
    10日涨跌幅          - 10日涨跌幅
    20日涨跌幅          - 20日涨跌幅
    30日涨跌幅          - 30日涨跌幅
    60日涨跌幅          - 60日涨跌幅
    120日涨跌幅         - 120日涨跌幅
    250日涨跌幅         - 250日涨跌幅

【价格距离均线涨跌幅】
    价格距离5日均线涨跌幅   - 价格距离5日均线涨跌幅
    价格距离10日均线涨跌幅  - 价格距离10日均线涨跌幅
    价格距离20日均线涨跌幅  - 价格距离20日均线涨跌幅
    价格距离30日均线涨跌幅  - 价格距离30日均线涨跌幅
    价格距离60日均线涨跌幅  - 价格距离60日均线涨跌幅
    价格距离120日均线涨跌幅 - 价格距离120日均线涨跌幅

【均线距离涨跌幅】
    5日均线距离10日均线涨跌幅  - 5日均线距离10日均线涨跌幅
    10日均线距离20日均线涨跌幅 - 10日均线距离20日均线涨跌幅
    20日均线距离30日均线涨跌幅 - 20日均线距离30日均线涨跌幅
    30日均线距离60日均线涨跌幅 - 30日均线距离60日均线涨跌幅
    60日均线距离120日均线涨跌幅 - 60日均线距离120日均线涨跌幅

【移动平均线】
    5日均线             - 5日均线
    10日均线            - 10日均线
    20日均线            - 20日均线
    30日均线            - 30日均线
    60日均线            - 60日均线
    120日均线           - 120日均线

【均线交叉信号】
    5日10日金叉         - 5日10日均线金叉
    10日20日金叉        - 10日20日均线金叉
    20日30日金叉        - 20日30日均线金叉
    30日60日金叉        - 30日60日均线金叉
    60日120日金叉       - 60日120日均线金叉
    5日10日死叉         - 5日10日均线死叉
    10日20日死叉        - 10日20日均线死叉
    20日30日死叉        - 20日30日均线死叉
    30日60日死叉        - 30日60日均线死叉
    60日120日死叉       - 60日120日均线死叉

【价格位置判断】
    价格在5均线上        - 价格是否在5日均线上
    价格在10均线上       - 价格是否在10日均线上
    价格在20均线上       - 价格是否在20日均线上
    价格在30均线上       - 价格是否在30日均线上
    价格在60均线上       - 价格是否在60日均线上
    价格在120均线上      - 价格是否在120日均线上
    5均线在10均线上      - 5日均线是否在10日均线上
    10均线在20均线上     - 10日均线是否在20日均线上
    20均线在30均线上     - 20日均线是否在30日均线上
    30均线在60均线上     - 30日均线是否在60日均线上
    60均线在120均线上    - 60日均线是否在120日均线上

【技术指标 - KDJ】
    KDJ_K               - KDJ指标K值
    KDJ_D               - KDJ指标D值
    KDJ_J               - KDJ指标J值
    KDJ_KD金叉          - KDJ金叉信号
    KDJ_KD死叉          - KDJ死叉信号

【技术指标 - MACD】
    MACD_DIF            - MACD平滑异同平均线DIF
    MACD_DEA            - MACD平滑异同平均线DEA
    MACD_MACD           - MACD平滑异同平均线MACD
    MACD_金叉           - MACD金叉信号
    MACD_死叉           - MACD死叉信号

【技术指标 - RSI】
    RSI1                - RSI相对强弱RSI1
    RSI2                - RSI相对强弱RSI2
    RSI3                - RSI相对强弱RSI3
    RSI_金叉            - RSI金叉信号
    RSI_死叉            - RSI死叉信号

【技术指标 - BOLL布林线】
    BOLL_BOLL           - BOLL布林线中轨
    BOLL_UB             - BOLL布林线上轨
    BOLL_LB             - BOLL布林线下轨

【技术指标 - CCI】
    CCI                 - CCI商品路径指标

【技术指标 - MFI】
    MFI                 - MFI资金流量指标

【技术指标 - MTM】
    MTM_MTM             - MTM动量线MTM值
    MTM_MTMMA           - MTM动量线MTMMA值

【技术指标 - SKDJ】
    SKDJ_K              - SKDJ慢速随机K值
    SKDJ_D              - SKDJ慢速随机D值

【技术指标 - WR】
    WR1                 - WR威廉指标WR1
    WR2                 - WR威廉指标WR2
    WR_金叉             - WR金叉信号
    WR_死叉             - WR死叉信号

【技术指标 - PSY】
    PSY_PSY             - PSY心理线PSY
    PSY_PSYMA           - PSY心理线PSYMA
    PSY_金叉            - PSY金叉信号
    PSY_死叉            - PSY死叉信号

【技术指标 - BIAS乖离率】
    BIAS1               - BIAS乖离率BIAS1
    BIAS2               - BIAS乖离率BIAS2
    BIAS3               - BIAS乖离率BIAS3
    BIAS_QL_BIAS        - BIAS_QL乖离率传统版BIAS值
    BIAS_QL_BIASMA      - BIAS_QL乖离率传统版BIASMA值
    BIAS36_BIAS36       - BIAS36三六乖离BIAS36
    BIAS36_BIAS612      - BIAS36三六乖离BIAS612
    BIAS36_MABIAS       - BIAS36三六乖离MABIAS

【技术指标 - DMI】
    DMI_PDI             - DMI趋向指标PDI
    DMI_MDI             - DMI趋向指标MDI
    DMI_ADX             - DMI趋向指标ADX
    DMI_ADXR            - DMI趋向指标ADXR

【技术指标 - DMA】
    DMA_XT_DIF          - DMA_XT平均差DIF
    DMA_XT_DIFMA        - DMA_XT平均差DIFMA

【技术指标 - DPO】
    DPO_DPO             - DPO区间震荡线DPO
    DPO_MADPO           - DPO区间震荡线MADPO

【技术指标 - EMV】
    EMV_EMV             - EMV简易波动指标EMV
    EMV_MAEMV           - EMV简易波动指标MAEMV

【技术指标 - TRIX】
    TRIX_TRIX           - TRIX三重指数平均线TRIX
    TRIX_MATRIX         - TRIX三重指数平均线MATRIX

【技术指标 - UOS】
    UOS_UOS             - UOS终极指标UOS
    UOS_MAUOS           - UOS终极指标MAUOS

【技术指标 - VPT】
    VTP_VPT             - VPT量价曲线VPT
    VTP_MAVP            - VPT量价曲线MAVP

【技术指标 - WVAD】
    WVAD_WVAD           - WVAD威廉变异离散量WVAD
    WVAD_MAWVAD         - WVAD威廉变异离散量MAWVAD

【技术指标 - BRAR】
    BRAR_BR             - BRAR情绪指标BR
    BRAR_AR             - BRAR情绪指标AR

【技术指标 - CR】
    CR_CR               - CR带状能量线CR
    CR_MA1              - CR带状能量线MA1
    CR_MA2              - CR带状能量线MA2
    CR_MA3              - CR带状能量线MA3
    CR_MA4              - CR带状能量线MA4

【技术指标 - MASS】
    MASS_MASS           - MASS梅斯线MASS
    MASS_MAMASS         - MASS梅斯线MAMASS

【技术指标 - VR】
    VR_VR               - VR成交量变异率VR
    VR_MAVR             - VR成交量变异率MAVR

【技术指标 - OBV】
    OBV_OBV             - OBV累积能量线OBV
    OBV_MAOBV           - OBV累积能量线MAOBV

【技术指标 - VOL成交量】
    VOL_XT_MAVOL1       - VOL成交量MAVOL1
    VOL_XT_MAVOL2       - VOL成交量MAVOL2

【技术指标 - VRSI】
    VRSI1               - VRSI相对强弱量RSI1
    VRSI2               - VRSI相对强弱量RSI2
    VRSI3               - VRSI相对强弱量RSI3

【技术指标 - HSL换手线】
    HSL_HSL             - HSL换手线HSL
    HSL_MAHSL           - HSL换手线MAHSL

【技术指标 - ACD】
    ACD_ACD             - ACD升降线ACD
    ACD_MAACD           - ACD升降线MAACD

【技术指标 - BBI】
    BBI                 - BBI多空均线

【技术指标 - EXPMA】
    EXPMA_EXP1          - EXPMA指数平均线EXP1
    EXPMA_EXP2          - EXPMA指数平均线EXP2

【技术指标 - SAR】
    SAR                 - SAR抛物线指标

【技术指标 - AMO成交金额】
    AMO_AMOW            - AMO成交金额AMOW
    AMO_AMO1            - AMO成交金额AMO1
    AMO_AMO2            - AMO成交金额AMO2

【技术指标 - MIKE】
    MIKE_STOR           - MIKE麦克支撑压力STOR
    MIKE_MIDR           - MIKE麦克支撑压力MIDR
    MIKE_WEKR           - MIKE麦克支撑压力WEKR
    MIKE_WEKS           - MIKE麦克支撑压力WEKS
    MIKE_MIDS           - MIKE麦克支撑压力MIDS
    MIKE_STOS           - MIKE麦克支撑压力STOS

【技术指标 - ENE】
    ENE_UPPER           - ENE轨道线上轨
    ENE_LOWER           - ENE轨道线下轨
    ENE_ENE             - ENE轨道线ENE

【技术指标 - PBX瀑布线】
    PBX_PBX1            - PBX瀑布线PBX1
    PBX_PBX2            - PBX瀑布线PBX2
    PBX_PBX3            - PBX瀑布线PBX3
    PBX_PBX4            - PBX瀑布线PBX4
    PBX_PBX5            - PBX瀑布线PBX5
    PBX_PBX6            - PBX瀑布线PBX6

【技术指标 - XS薛斯通道】
    XS_SUP              - XS薛斯通道SUP
    XS_SDN              - XS薛斯通道SDN
    XS_LUP              - XS薛斯通道LUP
    XS_LDN              - XS薛斯通道LDN

【技术指标 - TQN唐奇安通道】
    TQN_周期高点        - TQN唐奇安通道周期高点
    TQN_周期低点        - TQN唐奇安通道周期低点
    TQN_平空开多        - TQN唐奇安通道平空开多信号
    TQN_平多开空        - TQN唐奇安通道平多开空信号

【技术指标 - ALLIGAT鳄鱼线】
    ALLIGAT_上唇        - ALLIGAT鳄鱼线上唇
    ALLIGAT_牙齿        - ALLIGAT鳄鱼线牙齿
    ALLIGAT_下颚        - ALLIGAT鳄鱼线下颚

【技术指标 - GMMA顾比均线】
    GMMA_MA3            - GMMA顾比均线MA3
    GMMA_MA5            - GMMA顾比均线MA5
    GMMA_MA8            - GMMA顾比均线MA8
    GMMA_MA10           - GMMA顾比均线MA10
    GMMA_MA12           - GMMA顾比均线MA12
    GMMA_MA15           - GMMA顾比均线MA15
    GMMA_MA30           - GMMA顾比均线MA30
    GMMA_MA35           - GMMA顾比均线MA35
    GMMA_MA40           - GMMA顾比均线MA40
    GMMA_MA45           - GMMA顾比均线MA45
    GMMA_MA50           - GMMA顾比均线MA50
    GMMA_MA60           - GMMA顾比均线MA60

【技术指标 - VMACD】
    VMACD_DIF           - VMACD量平滑异同平均线DIF
    VMACD_DEA           - VMACD量平滑异同平均线DEA
    VMACD_MACD          - VMACD量平滑异同平均线MACD

【技术指标 - SMACD】
    SMACD_DEA           - SMACD单线平滑异同平均线DEA
    SMACD_MACD          - SMACD单线平滑异同平均线MACD

【技术指标 - QACD】
    QACD_DIF            - QACD快速异同平均线DIF
    QACD_MACD           - QACD快速异同平均线MACD
    QACD_DDIF           - QACD快速异同平均线DDIF

【技术指标 - 成交量相关】
    连续上涨天数        - 连续上涨天数
    连续下跌天数        - 连续下跌天数

【技术指标 - 偏度峰度】
    5日偏度             - 5日偏度
    10日偏度            - 10日偏度
    20日偏度            - 20日偏度
    30日偏度            - 30日偏度
    60日偏度            - 60日偏度
    120日偏度           - 120日偏度
    5日峰度             - 5日峰度
    10日峰度            - 10日峰度
    20日峰度            - 20日峰度
    30日峰度            - 30日峰度
    60日峰度            - 60日峰度
    120日峰度           - 120日峰度

【Alpha因子 - 世界金融实验室101因子】
    Alpha001 至 Alpha191 - 世界金融实验室101因子（共191个）

【交易信号因子】
    六脉神剑            - 六脉神剑交易信号
    小波段交易          - 小波段交易信号
    大波段交易          - 大波段交易信号
    波段超级买卖        - 波段超级买卖信号

【回归分析因子】
    3日回归动量         - 3日回归动量
    5日回归动量         - 5日回归动量
    7日回归动量         - 7日回归动量
    9日回归动量         - 9日回归动量
    12日回归动量        - 12日回归动量
    15日回归动量        - 15日回归动量
    18日回归动量        - 18日回归动量
    20日回归动量        - 20日回归动量
    23日回归动量        - 23日回归动量
    25日回归动量        - 25日回归动量
    28日回归动量        - 28日回归动量
    30日回归动量        - 30日回归动量
    35日回归动量        - 35日回归动量
    40日回归动量        - 40日回归动量
    45日回归动量        - 45日回归动量
    50日回归动量        - 50日回归动量
    60日回归动量        - 60日回归动量

【回归斜率】
    5日回归斜率         - 5日回归斜率
    10日回归斜率        - 10日回归斜率
    20日回归斜率        - 20日回归斜率
    30日回归斜率        - 30日回归斜率
    60日回归斜率        - 60日回归斜率
    120日回归斜率       - 120日回归斜率

【标准差】
    5日标准差           - 5日标准差
    10日标准差          - 10日标准差
    20日标准差          - 20日标准差
    30日标准差          - 30日标准差
    60日标准差          - 60日标准差
    120日标准差         - 120日标准差

【最高最低值周期】
    5日最高值到当前周期   - 5日最高值到当前周期
    10日最高值到当前周期  - 10日最高值到当前周期
    20日最高值到当前周期  - 20日最高值到当前周期
    30日最高值到当前周期  - 30日最高值到当前周期
    60日最高值到当前周期  - 60日最高值到当前周期
    120日最高值到当前周期 - 120日最高值到当前周期
    5日最低值到当前周期   - 5日最低值到当前周期
    10日最低值到当前周期  - 10日最低值到当前周期
    20日最低值到当前周期  - 20日最低值到当前周期
    30日最低值到当前周期  - 30日最低值到当前周期
    60日最低值到当前周期  - 60日最低值到当前周期
    120日最低值到当前周期 - 120日最低值到当前周期

【Alpha系数】
    5日Alpha            - 5日Alpha
    10日Alpha           - 10日Alpha
    20日Alpha           - 20日Alpha
    30日Alpha           - 30日Alpha
    60日Alpha           - 60日Alpha
    120日Alpha          - 120日Alpha

【Beta系数】
    5日Beta             - 5日Beta
    10日Beta            - 10日Beta
    20日Beta            - 20日Beta
    30日Beta            - 30日Beta
    60日Beta            - 60日Beta
    120日Beta           - 120日Beta

【夏普比率】
    5日夏普比率         - 5日夏普比率
    10日夏普比率        - 10日夏普比率
    20日夏普比率        - 20日夏普比率
    30日夏普比率        - 30日夏普比率
    60日夏普比率        - 60日夏普比率
    120日夏普比率       - 120日夏普比率

【年化波动率】
    5日年化波动率       - 5日年化波动率
    10日年化波动率      - 10日年化波动率
    20日年化波动率      - 20日年化波动率
    30日年化波动率      - 30日年化波动率
    60日年化波动率      - 60日年化波动率
    120日年化波动率     - 120日年化波动率

【最大回撤】
    5日最大回撤         - 5日最大回撤
    10日最大回撤        - 10日最大回撤
    20日最大回撤        - 20日最大回撤
    30日最大回撤        - 30日最大回撤
    60日最大回撤        - 60日最大回撤
    120日最大回撤       - 120日最大回撤

【上涨/下跌捕获率】
    5日上涨捕获率       - 5日上涨捕获率
    10日上涨捕获率      - 10日上涨捕获率
    20日上涨捕获率      - 20日上涨捕获率
    30日上涨捕获率      - 30日上涨捕获率
    60日上涨捕获率      - 60日上涨捕获率
    120日上涨捕获率     - 120日上涨捕获率
    5日下跌捕获率       - 5日下跌捕获率
    10日下跌捕获率      - 10日下跌捕获率
    20日下跌捕获率      - 20日下跌捕获率
    30日下跌捕获率      - 30日下跌捕获率
    60日下跌捕获率      - 60日下跌捕获率
    120日下跌捕获率     - 120日下跌捕获率

【庄家/主力指标】
    ZJTJ_无庄控盘       - ZJTJ庄家抬轿无庄控盘
    ZJTJ_开始控盘       - ZJTJ庄家抬轿开始控盘
    ZJTJ_有庄控盘       - ZJTJ庄家抬轿有庄控盘
    ZJTJ_主力出货       - ZJTJ庄家抬轿主力出货
    CYW                 - CYW主力控盘
    ZLJC_JCS            - ZLJC主力进出JCS
    ZLJC_JCM            - ZLJC主力进出JCM
    ZLJC_JCL            - ZLJC主力进出JCL
    ZLMM_MMS            - ZLMM主力买卖MMS
    ZLMM_MMM            - ZLMM主力买卖MMM
    ZLMM_MML            - ZLMM主力买卖MML
    LHXJ_主力弃盘       - LHXJ猎狐先觉主力弃盘
    LHXJ_主力控盘       - LHXJ猎狐先觉主力控盘
    LYJH_机构做空能量线  - LYJH猎鹰歼狐机构做空能量线
    LYJH_机构做多能量线  - LYJH猎鹰歼狐机构做多能量线

【智能交易信号】
    BDZX_AK             - BDZX波段之星AK
    BDZX_AD1            - BDZX波段之星AD1
    BDZX_AJ             - BDZX波段之星AJ
    BDZX_买进           - BDZX波段之星买进信号
    BDZX_卖出           - BDZX波段之星卖出信号
    CYHT_SK             - CYHT财运亨通SK
    CYHT_SD             - CYHT财运亨通SD
    CYHT_卖出           - CYHT财运亨通卖出信号
    CYHT_买进           - CYHT财运亨通买进信号
    BSQJ_B买            - BSQJ买卖区间B买信号
    BSQJ_持仓           - BSQJ买卖区间持仓信号
    BSQJ_S卖            - BSQJ买卖区间S卖信号
    BSQJ_空仓           - BSQJ买卖区间空仓信号
    JFZX_多头力量       - JFZX飓风智能中线多头力量
    JFZX_空头力量       - JFZX飓风智能中线空头力量
    XJDX_J              - XJDX超级短线J
    XJDX_D              - XJDX超级短线D
    XJDX_K              - XJDX超级短线K

【其他特色指标】
    CYS                 - CYS市场盈亏
    CYR_CYR             - CYR市场强弱CYR
    CYR_MACYR           - CYR市场强弱MACYR
    CYE_CYEL            - CYE市场趋势CYEL
    CYE_CYES            - CYE市场趋势CYES
    CYS                 - CYS市场盈亏
    RAD_RADER1          - RAD威力雷达RADER1
    RAD_RADERMA         - RAD威力雷达RADERMA
    SG_XDT_QR           - SG_XDT心电图QR
    SG_XDT_MQR1         - SG_XDT心电图MQR1
    SG_XDT_MQR2         - SG_XDT心电图MQR2
    SG_NDB_DK           - SG_NDB脑电波DK
    SG_NDB_MDK1         - SG_NDB脑电波MDK1
    SG_NDB_MDK2         - SG_NDB脑电波MDK2
    SG_SMX_ZY1          - SG_SMX生命线ZY1
    SG_SMX_ZY2          - SG_SMX生命线ZY2
    SG_SMX_ZY3          - SG_SMX生命线ZY3
    SG_LB_量比          - SG_LB量比
    SG_LB_MA5           - SG_LB量比MA5
    SG_LB_MA10          - SG_LB量比MA10
    SG_PF               - SG_PF强势股评分
    SLZT_白龙           - SLZT神龙在天白龙
    SLZT_黄龙           - SLZT神龙在天黄龙
    SLZT_紫龙           - SLZT神龙在天紫龙
    SLZT_青龙           - SLZT神龙在天青龙
    SLZT_红龙           - SLZT神龙在天红龙
    SLZT_蓝龙           - SLZT神龙在天蓝龙
    ADVOL_ADVOL         - ADVOL龙系离散量ADVOL
    ADVOL_MA1           - ADVOL龙系离散量MA1
    ADVOL_MA2           - ADVOL龙系离散量MA2
    JAX_J               - JAX济安线J
    JAX_A               - JAX济安线A
    JAX_X               - JAX济安线X
    LON_LON             - LON龙系长线LON
    LON_LONMA           - LON龙系长线LONMA
    LON_LONT            - LON龙系长线LONT
    SHT_SHT             - SHT龙系短线SHT
    SHT_SHTMA           - SHT龙系短线SHTMA
    CDP_STD_CDP         - CDP_STD逆势操作CDP
    CDP_STD_AH          - CDP_STD逆势操作AH
    CDP_STD_NH          - CDP_STD逆势操作NH
    CDP_STD_NL          - CDP_STD逆势操作NL
    CDP_STD_AL          - CDP_STD逆势操作AL
"""

print("\n" + "=" * 60)
print("📈 获取因子数据")
print("=" * 60)

# 获取基础因子数据
result = client.get_stock_factor_data(
    stock='513100.SH',      # 纳指ETF
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,high,low,volume,amount'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取涨跌幅因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='159915.SZ',      # 创业板ETF
    start_date='20220101',
    end_date='20241231',
    columns='date,证券代码,5日涨跌幅,10日涨跌幅,20日涨跌幅,60日涨跌幅'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取技术指标因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,MACD_DIF,MACD_DEA,MACD_MACD,KDJ_K,KDJ_D,KDJ_J,RSI1,RSI2,RSI3,BOLL_BOLL,BOLL_UB,BOLL_LB'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（技术指标）")
print(df.head())

# 获取均线系统因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,5日均线,10日均线,20日均线,30日均线,60日均线,120日均线'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（均线系统）")
print(df.head())

# 获取Alpha因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='128137.SZ',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,Alpha001,Alpha002,Alpha003,Alpha004,Alpha005'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（Alpha因子）")
print(df.head())

# 获取动量因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,3日回归动量,5日回归动量,10日回归动量,20日回归动量,30日回归动量,60日回归动量'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（动量因子）")
print(df.head())
```
## 8. 获取财务数据 获取资产负债表
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例4：获取资产负债表（全部字段）
# ============================================================
"""
参数说明：
    table: str = '资产负债表'       - 财务表类型
    date: str = '2026-06-30'        - 报告日期，格式YYYY-MM-DD
    columns: str = 'secu_code,end_date,total_assets'  - 选择字段，逗号分隔

财务表类型：
    '资产负债表'     - 资产负债表
    '利润表'         - 利润表
    '现金流量表'     - 现金流量表
    '估值数据'       - 估值数据
    '成长能力'       - 成长能力指标
    '盈利能力'       - 盈利能力指标
    '每股指标'       - 每股指标
    '营运能力'       - 营运能力指标
    '偿债能力'       - 偿债能力指标

【资产负债表 - balance_statement 全部字段】
    secu_code                       - 股票代码
    secu_abbr                       - 股票简称
    company_type                    - 公司类型
    end_date                        - 截止日期
    publ_date                       - 公告日期
    settlement_provi                - 结算备付金
    client_provi                    - 客户备付金
    deposit_in_interbank            - 存放同业款项
    r_metal                         - 贵金属
    lend_capital                    - 拆出资金
    derivative_assets               - 衍生金融资产
    bought_sellback_assets          - 买入返售金融资产
    loan_and_advance                - 发放贷款和垫款
    insurance_receivables           - 应收保费
    receivable_subrogation_fee      - 应收代位追偿款
    reinsurance_receivables         - 应收分保账款
    receivable_unearned_r           - 应收分保未到期责任准备金
    receivable_claims_r             - 应收分保未决赔款准备金
    receivable_life_r               - 应收分保寿险责任准备金
    receivable_lt_health_r          - 应收分保长期健康险责任准备金
    insurer_impawn_loan             - 保户质押贷款
    fixed_deposit                   - 定期存款
    refundable_capital_deposit      - 存出资本保证金
    refundable_deposit              - 存出保证金
    independence_account_assets     - 独立账户资产
    other_assets                    - 其他资产
    borrowing_from_centralbank      - 向中央银行借款
    deposit_of_interbank            - 同业及其他金融机构存放款项
    borrowing_capital               - 拆入资金
    derivative_liability            - 衍生金融负债
    sold_buyback_secu_proceeds      - 卖出回购金融资产款
    deposit                         - 吸收存款
    proxy_secu_proceeds             - 代理买卖证券款
    sub_issue_secu_proceeds         - 代理承销证券款
    deposits_received               - 存入保证金
    advance_insurance               - 预收保费
    commission_payable              - 应付手续费及佣金
    reinsurance_payables            - 应付分保账款
    compensation_payable            - 应付赔付款
    policy_dividend_payable         - 应付保单红利
    insurer_deposit_investment      - 保户储金及投资款
    unearned_premium_reserve        - 未到期责任准备金
    outstanding_claim_reserve       - 未决赔款准备金
    life_insurance_reserve          - 寿险责任准备金
    lt_health_insurance_lr          - 长期健康险责任准备金
    independence_liability          - 独立账户负债
    other_liability                 - 其他负债
    cash_equivalents                - 货币资金
    client_deposit                  - 客户资金存款
    trading_assets                  - 交易性金融资产
    bill_receivable                 - 应收票据
    dividend_receivable             - 应收股利
    interest_receivable             - 应收利息
    account_receivable              - 应收账款
    other_receivable                - 其他应收款
    advance_payment                 - 预付款项
    inventories                     - 存货
    non_current_asset_in_one_year   - 一年内到期的非流动资产
    other_current_assets            - 其他流动资产
    total_current_assets            - 流动资产合计
    shortterm_loan                  - 短期借款
    impawned_loan                   - 质押借款
    trading_liability               - 交易性金融负债
    notes_payable                   - 应付票据
    accounts_payable                - 应付账款
    advance_receipts                - 预收款项
    salaries_payable                - 应付职工薪酬
    dividend_payable                - 应付股利
    taxs_payable                    - 应交税费
    interest_payable                - 应付利息
    other_payable                   - 其他应付款
    non_current_liability_in_one_year - 一年内到期的非流动负债
    other_current_liability         - 其他流动负债
    total_current_liability         - 流动负债合计
    hold_for_sale_assets            - 可供出售金融资产
    hold_to_maturity_investments    - 持有至到期投资
    investment_property             - 投资性房地产
    longterm_equity_invest          - 长期股权投资
    longterm_receivable_account     - 长期应收款
    fixed_assets                    - 固定资产
    construction_materials          - 工程物资
    constru_in_process              - 在建工程
    fixed_assets_liquidation        - 固定资产清理
    biological_assets               - 生产性生物资产
    oil_gas_assets                  - 油气资产
    intangible_assets               - 无形资产
    seat_costs                      - 交易席位费
    development_expenditure         - 开发支出
    good_will                       - 商誉
    long_deferred_expense           - 长期待摊费用
    deferred_tax_assets             - 递延所得税资产
    other_non_current_assets        - 其他非流动资产
    total_non_current_assets        - 非流动资产合计
    longterm_loan                   - 长期借款
    bonds_payable                   - 应付债券
    longterm_account_payable        - 长期应付款
    long_salaries_pay               - 长期应付职工薪酬
    specific_account_payable        - 专项应付款
    estimate_liability              - 预计负债
    deferred_tax_liability          - 递延所得税负债
    long_defer_income               - 长期递延收益
    other_non_current_liability     - 其他非流动负债
    total_non_current_liability     - 非流动负债合计
    paidin_capital                  - 实收资本（或股本）
    other_equityinstruments         - 其他权益工具
    capital_reserve_fund            - 资本公积
    surplus_reserve_fund            - 盈余公积
    retained_profit                 - 未分配利润
    treasury_stock                  - 减：库存股
    other_composite_income          - 其他综合收益
    ordinary_risk_reserve_fund      - 一般风险准备
    foreign_currency_report_conv_diff - 外币报表折算差额
    specific_reserves               - 专项储备
    se_without_mi                   - 归属母公司股东权益合计
    minority_interests              - 少数股东权益
    total_shareholder_equity        - 所有者权益合计
    total_liability_and_equity      - 负债和权益总计
    total_assets                    - 资产总计
    total_liability                 - 负债总计
    contract_liability              - 合同负债
    total_fixed_asset               - 固定资产合计
    t_constru_in_process            - 在建工程合计
"""

print("\n" + "=" * 60)
print("💰 获取资产负债表")
print("=" * 60)

result = client.get_stock_finance_data(
    table='资产负债表',
    date='2024-06-30',
    columns='secu_code,secu_abbr,end_date,total_assets,total_liability,total_shareholder_equity'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 9. 获取利润表
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例5：获取利润表（全部字段）
# ============================================================
"""
【利润表 - income_statement 全部字段】
    secu_code                       - 股票代码
    secu_abbr                       - 股票简称
    company_type                    - 公司类型
    end_date                        - 截止日期
    publ_date                       - 公告日期
    basic_eps                       - 基本每股收益
    diluted_eps                     - 稀释每股收益
    net_profit                      - 净利润
    np_parent_company_owners        - 归属于母公司所有者的净利润
    minority_profit                 - 少数股东损益
    total_operating_cost            - 营业总成本
    operating_payout                - 营业支出
    refunded_premiums               - 退保金
    compensation_expense            - 赔付支出
    amortization_expense            - 减:摊回赔付支出
    premium_reserve                 - 提取保险责任准备金
    amortization_premium_reserve    - 减:摊回保险责任准备金
    policy_dividend_payout          - 保单红利支出
    reinsurance_cost                - 分保费用
    amortization_reinsurance_cost   - 减:摊回分保费用
    insurance_commission_expense    - 保险手续费及佣金支出
    other_operating_cost            - 其他营业成本
    operating_cost                  - 营业成本
    operating_tax_surcharges        - 营业税金及附加
    operating_expense               - 销售费用
    administration_expense          - 管理费用
    financial_expense               - 财务费用
    asset_impairment_loss           - 资产减值损失
    operating_profit                - 营业利润
    non_operating_income            - 加：营业收入
    non_operating_expense           - 减：营业外支出
    non_current_assetss_deal_loss   - 其中：非流动资产处置净损失
    total_operating_revenue         - 营业总收入
    operating_revenue               - 营业收入
    net_interest_income             - 利息净收入
    interest_income                 - 其中：利息收入
    interest_expense                - 其中:利息支出
    net_commission_income           - 手续费及佣金净收入
    commission_income               - 其中：手续费及佣金收入
    commission_expense              - 其中：手续费及佣金支出
    net_proxy_secu_income           - 其中：代理买卖证券业务净收入
    net_subissue_secu_income        - 其中：证券承销业务净收入
    net_trust_income                - 其中:受托客户资产管理业务净收入
    premiums_earned                 - 已赚保费
    premiums_income                 - 保险业务收入
    reinsurance_income              - 其中：分保费收入
    reinsurance                     - 减：分出保费
    unearned_premium_reserve        - 提取未到期责任准备金
    other_operating_revenue         - 其他营业收入
    other_net_revenue               - 非营业性收入
    fair_value_change_income        - 公允价值变动净收益
    invest_income                   - 投资净收益
    invest_income_associates        - 其中:对联营合营企业的投资收益
    exchange_income                 - 汇兑收益
    total_profit                    - 利润总额
    income_tax_cost                 - 减：所得税费用
    total_composite_income          - 综合收益总额
    ci_parent_company_owners        - 归属于母公司所有者的综合收益总额
    ci_minority_owners              - 归属于少数股东的综合收益总额
    r_and_d                         - 研发费用
"""

print("\n" + "=" * 60)
print("💰 获取利润表")
print("=" * 60)

result = client.get_stock_finance_data(
    table='利润表',
    date='2024-06-30',
    columns='secu_code,secu_abbr,total_operating_revenue,operating_cost,net_profit,basic_eps'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 10. 现金流量表
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例6：获取现金流量表（全部字段）
# ============================================================
"""
【现金流量表 - cashflow_statement 全部字段】
    secu_code                       - 股票代码
    secu_abbr                       - 股票简称
    company_type                    - 公司类型
    end_date                        - 截止日期
    publ_date                       - 公告日期
    goods_sale_service_render_cash  - 销售商品、提供劳务收到的现金
    tax_levy_refund                 - 收到的税费返还
    net_deposit_increase            - 客户存款和同业存放款项净增加额
    net_borrowing_from_central_bank - 向中央银行借款净增加额
    net_borrowing_from_finance_co   - 向其他金融机构拆入资金净增加额
    interest_and_commission_cashin  - 收取利息、手续费及佣金的现金
    net_deal_trading_assets         - 处置交易性金融资产净增加额
    net_buyback                     - 回购业务资金净增加额
    net_original_insurance_cash     - 收到原保险合同保费取得的现金
    net_reinsurance_cash            - 收到再保业务现金净额
    net_insurer_deposit_investment  - 保户储金及投资款净增加额
    other_cashin_related_operate    - 收到其他与经营活动有关的现金
    subtotal_operate_cash_inflow    - 经营活动现金流入小计
    goods_and_services_cash_paid    - 购买商品、接受劳务支付的现金
    staff_behalf_paid               - 支付给职工以及为职工支付的现金
    all_taxes_paid                  - 支付的各项税费
    net_loan_and_advance_increase   - 客户贷款及垫款净增加额
    net_deposit_in_cb_and_ib        - 存放中央银行和同业款项净增加额
    net_lend_capital                - 拆出资金净增加额
    commission_cash_paid            - 支付手续费及佣金的现金
    original_compensation_paid      - 支付原保险合同赔付款项的现金
    net_cash_for_reinsurance        - 支付再保业务现金净额
    policy_dividend_cash_paid       - 支付保单红利的现金
    other_operate_cash_paid         - 支付其他与经营活动有关的现金
    subtotal_operate_cash_outflow   - 经营活动现金流出小计
    net_operate_cash_flow           - 经营活动产生的现金流量净额
    invest_withdrawal_cash          - 收回投资收到的现金
    invest_proceeds                 - 取得投资收益收到的现金
    fix_intan_other_asset_dispo_cash - 处置固定资产、无形资产和其他长期资产收回的现金净额
    net_cash_deal_sub_company       - 处置子公司及其他营业单位收到的现金净额
    other_cash_from_invest_act      - 收到其他与投资活动有关的现金
    subtotal_invest_cash_inflow     - 投资活动现金流入小计
    fix_intan_other_asset_acqui_cash - 购建固定资产、无形资产和其他长期资产支付的现金
    invest_cash_paid                - 投资支付的现金
    net_cash_from_sub_company       - 取得子公司及其他营业单位支付的现金净额
    impawned_loan_net_increase      - 质押贷款净增加额
    other_cash_to_invest_act        - 支付其他与投资活动有关的现金
    subtotal_invest_cash_outflow    - 投资活动现金流出小计
    net_invest_cash_flow            - 投资活动产生的现金流量净额
    cash_from_invest                - 吸收投资收到的现金
    cash_from_bonds_issue           - 发行债券收到的现金
    cash_from_borrowing             - 取得借款收到的现金
    other_finance_act_cash          - 收到其他与筹资活动有关的现金
    subtotal_finance_cash_inflow    - 筹资活动现金流入小计
    borrowing_repayment             - 偿还债务支付的现金
    dividend_interest_payment       - 分配股利、利润或偿付利息支付的现金
    other_finance_act_payment       - 支付其他与筹资活动有关的现金
    subtotal_finance_cash_outflow   - 筹资活动现金流出小计
    net_finance_cash_flow           - 筹资活动产生的现金流量净额
    exchan_rate_change_effect       - 汇率变动对现金及现金等价物的影响
    cash_equivalent_increase        - 现金及现金等价物净增加额
    begin_period_cash               - 加：期初现金及现金等价物余额
    end_period_cash_equivalent      - 期末现金及现金等价物余额
    net_profit                      - 净利润
    minority_profit                 - 加:少数股东损益
    assets_depreciation_reserves    - 加:资产减值准备
    fixed_asset_depreciation        - 固定资产折旧
    intangible_asset_amortization   - 收无形资产摊销
    deferred_expense_amort          - 长期待摊费用摊销
    deferred_expense_decreased      - 待摊费用减少(减:增加)
    accrued_expense_added           - 预提费用增加(减:减少)
    fix_intanther_asset_dispo_loss  - 处置固定资产、无形资产和其他长期资产的损失
    fixed_asset_scrap_loss          - 固定资产报废损失
    loss_from_fair_value_changes    - 公允价值变动损失
    financial_expense               - 财务费用
    invest_loss                     - 投资损失
    defered_tax_asset_decrease      - 递延所得税资产减少
    defered_tax_liability_increase  - 递延所得税负债增加
    inventory_decrease              - 存货的减少
    operate_receivable_decrease     - 经营性应收项目的减少
    operate_payable_increase        - 经营性应付项目的增加
    others                          - 其他
    net_operate_cash_flow_notes     - 经营活动产生的现金流量净额
    debt_to_captical                - 债务转为资本
    cbs_expiring_within_one_year    - 一年内到期的可转换公司债券
    fixed_assets_finance_leases     - 融资租入固定资产
    cash_at_end_of_year             - 现金的期末余额
    cash_at_beginning_of_year       - 减:现金的期初余额
    cash_equivalents_at_end_of_year - 加:现金等价物的期末余额
    cash_equivalents_at_beginning   - 减:现金等价物的期初余额
    net_incr_in_cash_and_equivalents - 现金及现金等价物净增加额
"""

print("\n" + "=" * 60)
print("💰 获取现金流量表")
print("=" * 60)

result = client.get_stock_finance_data(
    table='现金流量表',
    date='2024-06-30',
    columns='secu_code,secu_abbr,net_operate_cash_flow,net_invest_cash_flow,net_finance_cash_flow'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 11. 获取估值数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例7：获取估值数据（全部字段）
# ============================================================
"""
【估值数据 - valuation 全部字段】
    trading_day                     - 交易日期（固定返回）
    total_value                     - A股总市值(元)（固定返回）
    float_value                     - A股流通市值(元)（自选返回）
    naps                            - 每股净资产/(元/股)（自选返回）
    pcf                             - 市现率（自选返回）
    secu_abbr                       - 证券简称（自选返回）
    secu_code                       - 证券代码（固定返回）
    ps                              - 市销率PS（自选返回）
    ps_ttm                          - 市销率PS(TTM)（自选返回）
    pe_ttm                          - 市盈率PE(TTM)（自选返回）
    a_shares                        - A股股本（自选返回）
    a_floats                        - 可流通A股（自选返回）
    pe_dynamic                      - 动态市盈率（自选返回）
    pe_static                       - 静态市盈率（自选返回）
    b_floats                        - 可流通B股（自选返回）
    b_shares                        - B股股本（自选返回）
    h_shares                        - H股股本（自选返回）
    total_shares                    - 总股本（自选返回）
    turnover_rate                   - 换手率（自选返回）
    dividend_ratio                  - 滚动股息率（自选返回）
    pb                              - 市净率（自选返回）
    roe                             - 净资产收益率（自选返回）
"""

print("\n" + "=" * 60)
print("💰 获取估值数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='估值数据',
    date='2024-06-30',
    columns='secu_code,secu_abbr,pe_ttm,pb,total_value,roe,turnover_rate'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 12. 获取成长能力数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例8：获取成长能力数据（全部字段）
# ============================================================
"""
【成长能力 - growth_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    basic_eps_yoy                   - 基本每股收益同比增长（%）
    diluted_eps_yoy                 - 稀释每股收益同比增长（%）
    operating_revenue_grow_rate     - 营业收入同比增长（%）
    np_parent_company_yoy           - 归属母公司股东的净利润同比增长（%）
    net_operate_cash_flow_yoy       - 经营活动产生的现金流量净额同比增长（%）
    oper_profit_grow_rate           - 营业利润同比增长（%）
    total_profit_grow_rate          - 利润总额同比增长（%）
    eps_grow_rate_ytd               - 每股净资产相对年初增长率（%）
    se_without_mi_grow_rate_ytd     - 归属母公司股东的权益相对年初增长率（%）
    ta_grow_rate_ytd                - 资产总计相对年初增长率（%)
    np_parent_company_cut_yoy       - 归属母公司股东的净利润(扣除)同比增长（%）
    avg_np_yoy_past_five_year       - 过去五年同期归属母公司净利润平均增幅（%）
    oper_cash_ps_grow_rate          - 每股经营活动产生的现金流量净额同比增长（%）
    naor_yoy                        - 净资产收益率(摊薄)同比增（%）
    net_asset_grow_rate             - 净资产同比增长（%）
    total_asset_grow_rate           - 总资产同比增长（%）
    sustainable_grow_rate           - 可持续增长率（%）
    net_profit_grow_rate            - 净利润同比增长（%）
"""

print("\n" + "=" * 60)
print("📈 获取成长能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='成长能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,operating_revenue_grow_rate,np_parent_company_yoy,oper_profit_grow_rate'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 13. 盈利能力
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例9：获取盈利能力数据（全部字段）
# ============================================================
"""
【盈利能力 - profit_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    roe_avg                         - 净资产收益率%平均计算值（%）
    roe_weighted                    - 净资产收益率%加权公布值（%）
    roe                             - 净资产收益率%摊薄公布值（%）
    roe_cut                         - 净资产收益率%扣除摊薄（%）
    roe_cut_weighted                - 净资产收益率%扣除加权（%）
    roe_ttm                         - 净资产收益率_TTM（%）
    roa_ebit                        - 总资产报酬率（%）
    roa_ebit_ttm                    - 总资产报酬率_TTM（%）
    roa                             - 总资产净利率（%）
    roa_ttm                         - 总资产净利率_TTM（%）
    roic                            - 投入资本回报率（%）
    net_profit_ratio                - 销售净利率（%）
    net_profit_ratio_ttm            - 销售净利率_TTM（%）
    gross_income_ratio              - 销售毛利率（%）
    gross_income_ratio_ttm          - 销售毛利率_TTM（%）
    sales_cost_ratio                - 销售成本率（%）
    period_costs_rate               - 销售期间费用率（%）
    period_costs_rate_ttm           - 销售期间的费用率_TTM（%）
    np_to_tor                       - 净利润／营业总收入（%）
    np_to_tor_ttm                   - 净利润／营业总收入_TTM（%）
    operating_profit_to_tor         - 营业利润／营业总收入（%）
    operating_profit_to_tor_ttm     - 营业利润／营业总收入_TTM（%）
    ebit_to_tor                     - 息税前利润／营业总收入（%）
    ebit_to_tor_ttm                 - 息税前利润／营业总收入_TTM（%）
    t_operating_cost_to_tor         - 营业总成本／营业总收入（%）
    t_operating_cost_to_tor_ttm     - 营业总成本／营业总收入_TTM（%）
    operating_expense_rate          - 销售费用／营业总收入（%）
    operating_expense_rate_ttm      - 销售费用／营业总收入_TTM（%）
    admini_expense_rate             - 管理费用／营业总收入（%）
    admini_expense_rate_ttm         - 管理费用／营业总收入_TTM（%）
    financial_expense_rate          - 财务费用／营业总收入（%）
    financial_expense_rate_ttm      - 财务费用／营业总收入_TTM（%）
    asset_impa_loss_to_tor          - 资产减值损失／营业总收入（%）
    asset_impa_loss_to_tor_ttm      - 资产减值损失／营业总收入_TTM（%）
    net_profit                      - 归属母公司净利润（元）
    net_profit_cut                  - 扣除非经常性损益后的净利润（元）
    ebit                            - 息税前利润（元）
    ebitda                          - 息税折旧摊销前利润（元）
    operating_profit_ratio          - 营业利润率（%）
    total_profit_cost_ratio         - 成本费用利润率
"""

print("\n" + "=" * 60)
print("📈 获取盈利能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='盈利能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,roe,gross_income_ratio,net_profit_ratio'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 14. 每股指标
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例10：获取每股指标数据（全部字段）
# ============================================================
"""
【每股指标 - eps 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    basic_eps                       - 基本每股收益（元/股）
    diluted_eps                     - 稀释每股收益（元/股）
    eps                             - 每股收益_期末股本摊薄（元/股）
    eps_ttm                         - 每股收益_TTM（元/股）
    naps                            - 每股净资产（元/股）
    total_operating_revenue_ps      - 每股营业总收入（元/股）
    main_income_ps                  - 每股营业收入（元/股）
    operating_revenue_ps_ttm        - 每股营业收入_TTM（元/股）
    oper_profit_ps                  - 每股营业利润（元/股）
    ebitps                          - 每股息税前利润（元/股）
    capital_surplus_fund_ps         - 每股资本公积金（元/股）
    surplus_reserve_fund_ps         - 每股盈余公积（元/股）
    accumulation_fund_ps            - 每股公积金（元/股）
    undivided_profit                - 每股未分配利润（元/股）
    retained_earnings_ps            - 每股留存收益（元/股）
    net_operate_cash_flow_ps        - 每股经营活动产生的现金流量净额（元/股）
    net_operate_cash_flow_ps_ttm    - 每股经营活动产生的现金流量净额_TTM（元/股）
    cash_flow_ps                    - 每股现金流量净额（元/股）
    cash_flow_ps_ttm                - 每股现金流量净额_TTM（元/股）
    enterprise_fcf_ps               - 每股企业自由现金流量（元/股）
    shareholder_fcf_ps              - 每股股东自由现金流量（元/股）
"""

print("\n" + "=" * 60)
print("📈 获取每股指标数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='每股指标',
    date='2024-06-30',
    columns='secu_code,secu_abbr,basic_eps,diluted_eps,naps'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 15. 获取营运能力数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例11：获取营运能力数据（全部字段）
# ============================================================
"""
【营运能力 - operating_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    oper_cycle                      - 营业周期（天/次）
    inventory_turnover_rate         - 存货周转率（次）
    inventory_turnover_days         - 存货周转天数（天/次）
    accounts_receivables_turnover_rate - 应收账款周转率（次）
    accounts_receivables_turnover_days - 应收账款周转天数（天/次）
    accounts_payables_turnover_rate - 应付账款周转率（次）
    accounts_payables_turnover_days - 应付账款周转天数（天/次）
    current_assets_turnover_rate    - 流动资产周转率（次）
    fixed_asset_turnover_rate       - 固定资产周转率（次）
    equity_turnover_rate            - 股东权益周转率（次）
    total_asset_turnover_rate       - 总资产周转率（次）
"""

print("\n" + "=" * 60)
print("📈 获取营运能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='营运能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,inventory_turnover_rate,accounts_receivables_turnover_rate,total_asset_turnover_rate'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 16. 获取偿债能力数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例12：获取偿债能力数据（全部字段）
# ============================================================
"""
【偿债能力 - debt_paying_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    current_ratio                   - 流动比率
    quick_ratio                     - 速动比率
    super_quick_ratio               - 超速动比率
    debt_equity_ratio               - 产权比率（%）
    sewmi_to_total_liability        - 归属母公司股东的权益／负债合计（%）
    sewmi_to_interest_bear_debt     - 归属母公司股东的权益／带息债务（%）
    debt_tangible_equity_ratio      - 有形净值债务率（%）
    tangible_a_to_interest_bear_debt - 有形净值／带息债务（%）
    tangible_a_to_net_debt          - 有形净值／净债务（%）
    ebitda_to_t_liability           - 息税折旧摊销前利润／负债合计
    nocf_to_t_liability             - 经营活动产生现金流量净额/负债合计
    nocf_to_interest_bear_debt      - 经营活动产生现金流量净额/带息债务
    nocf_to_current_liability       - 经营活动产生现金流量净额/流动负债
    nocf_to_net_debt                - 经营活动产生现金流量净额/净债务
    interest_cover                  - 利息保障倍数（倍）
    long_debt_to_working_capital    - 长期负债与营运资金比率
    opercashinto_current_debt       - 现金流动负债比
"""

print("\n" + "=" * 60)
print("📈 获取偿债能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='偿债能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,current_ratio,quick_ratio,debt_equity_ratio'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 17. 读取模拟交易统计数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例13：读取模拟交易统计数据
# ============================================================
"""
参数说明：
    st_type: str = '动量策略'        - 策略类型
        可选值：'定投策略'、'动量策略'、'资产配置策略'、
               '资产配置平衡策略'、'网格策略'、'海龟策略'、
               '综合动量策略'、'条件因子策略'、'排序多因子策略'
    st_name: str = '小果动量模拟策略'  - 策略名称
"""

print("\n" + "=" * 60)
print("📊 读取模拟交易统计数据")
print("=" * 60)

result = client.get_moni_trader_data(
    st_type='动量策略',
    st_name='小果动量模拟策略'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 18. 读取社区交易统计数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例14：读取社区交易统计数据
# ============================================================
"""
参数说明：
    st_type: str = '动量策略'        - 策略类型
        可选值：'定投策略'、'动量策略'、'资产配置策略'、
               '资产配置平衡策略'、'网格策略'、'海龟策略'、
               '综合动量策略'、'条件因子策略'、'排序多因子策略'
    st_name: str = '小果动量模拟策略'  - 策略名称
"""

print("\n" + "=" * 60)
print("📊 读取社区交易统计数据")
print("=" * 60)

result = client.get_moni_trader_data_sq(
    st_type='动量策略',
    st_name='小果动量模拟策略'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
# 三、回测接口
## 1. 定投回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例15：定投回测
# ============================================================
"""
参数说明：
    start_date: str = '20260701'     - 回测开始日期，格式YYYYMMDD
    end_date: str = '20500101'       - 回测结束日期，格式YYYYMMDD
    stock_list: str = '513100.SH,513500.SH'  - 股票列表，逗号分隔
    index_stock: str = '000300.SH'   - 基准指数代码
    cash: float = 100000             - 初始资金
    dt_interval: int = 20            - 定投间隔（交易日）
    dt_type: str = '金额'            - 定投类型：'金额'、'份额'、'百分比'
    dt_value: float = 1000           - 定投金额/份额/百分比值
    sell_zdf: float = 0.03           - 止盈涨幅阈值（如0.03表示3%）
    buy_zdf: float = -0.03           - 补仓跌幅阈值（如-0.03表示-3%）
    trade_value: float = 1000        - 每次交易金额
    comm: float = 0.0001             - 佣金费率（如0.0001表示万分之一）
"""

print("\n" + "=" * 60)
print("📊 定投回测")
print("=" * 60)

result = client.xg_dt_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    dt_interval=20,
    dt_type='金额',
    dt_value=1000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("定投回测结果：")
print(result)
```
## 2. 动量回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例16：动量回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    mom_type: str = '百分比'         - 动量类型：'百分比'或'金额'
    mom_value: float = 1             - 动量值（百分比或金额）
    mom_daily: int = 25              - 动量计算周期（交易日）
    min_mom: float = 0               - 最小动量阈值，低于此值不买入
    max_mom: float = 5               - 最大动量阈值，高于此值不买入
    buy_rank: int = 1                - 买入排名，1表示买排名第1的股票
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_amount: float = 1000        - 卖出金额
"""

print("\n" + "=" * 60)
print("📊 动量回测")
print("=" * 60)

result = client.xg_mom_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    mom_type='百分比',
    mom_value=1,
    mom_daily=25,
    min_mom=0,
    max_mom=5,
    buy_rank=1,
    sell_zdf=0.03,
    sell_amount=1000
)
print("动量回测结果：")
print(result)
```
## 3. 资产配置回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例17：资产配置回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    dt_type: str = '百分比'          - 配置类型：'百分比'、'金额'
    weight_list: str = '0.4,0.4,0.2' - 权重配置，与股票列表一一对应
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
    comm: float = 0.0001             - 佣金费率
"""

print("\n" + "=" * 60)
print("📊 资产配置回测")
print("=" * 60)

result = client.xg_pz_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.4,0.4,0.2',
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置回测结果：")
print(result)
```
## 4. 资产配置平衡回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例18：资产配置平衡回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    dt_type: str = '百分比'          - 配置类型
    weight_list: str = '0.35,0.35,0.3'  - 目标权重
    deviation_list: str = '0.1,0.1,0.05'  - 偏离容忍度，与股票一一对应
    interval: int = 20               - 再平衡间隔（交易日）
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
    comm: float = 0.0001             - 佣金费率
"""

print("\n" + "=" * 60)
print("📊 资产配置平衡回测")
print("=" * 60)

result = client.xg_zcph_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.35,0.35,0.3',
    deviation_list='0.1,0.1,0.05',
    interval=20,
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置平衡回测结果：")
print(result)
```
## 5. 网格策略回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例19：网格策略回测
# ============================================================
"""
参数说明：
    start_date: str = '20250701'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '513100.SH,513500.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    gd_interval: int = 1             - 网格间隔
    gd_bc_type_list: str = '百分比,百分比'  - 网格类型
    gd_buy_bc_list: str = '0.03,0.02'  - 买入阈值
    gd_sell_bc_list: str = '-0.02,-0.015'  - 卖出阈值
    gd_atr_ratio_list: str = '2.0,2.0'  - ATR比例
    gd_type_list: str = '金额,金额'  - 交易类型
    gd_value_list: str = '1000,1500'  - 交易金额
    init_position_ratio_list: str = '0.1,0.15'  - 初始仓位
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
    comm: float = 0.0001             - 佣金费率
"""

print("\n" + "=" * 60)
print("📊 网格策略回测")
print("=" * 60)

result = client.xg_gd_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    gd_interval=1,
    gd_bc_type_list='百分比,百分比',
    gd_buy_bc_list='0.03,0.02',
    gd_sell_bc_list='-0.02,-0.015',
    gd_atr_ratio_list='2.0,2.0',
    gd_type_list='金额,金额',
    gd_value_list='1000,1500',
    init_position_ratio_list='0.1,0.15',
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("网格策略回测结果：")
print(result)
```
## 6. 海龟策略回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例20：海龟策略回测
# ============================================================
"""
参数说明：
    start_date: str = '20240101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '513100.SH,513500.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    max_workers: int = 4             - 最大进程数
    entry_period: int = 20           - 入场周期
    exit_period: int = 10            - 离场周期
    n_period: int = 20               - N值计算周期
    risk_per_trade: float = 0.01     - 单笔风险
    risk_per_unit: float = 0.02      - 单位风险
    max_units: int = 4               - 最大单位
    add_unit_threshold: float = 0.5  - 加仓阈值
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
"""

print("\n" + "=" * 60)
print("📊 海龟策略回测")
print("=" * 60)

result = client.xg_hg_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    entry_period=20,
    exit_period=10,
    n_period=20,
    risk_per_trade=0.01,
    risk_per_unit=0.02,
    max_units=4,
    add_unit_threshold=0.5,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000
)
print("海龟策略回测结果：")
print(result)
```
## 7. 综合动量回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例21：综合动量回测
# ============================================================
"""
参数说明：
    start_date: str = '20250101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    max_workers: int = 4             - 最大进程数
    enable_index_timing: bool = False  - 启用指数择时
    index_mean_line: int = 20        - 指数均线周期
    index_not_trader: str = '513100.SH,518880.SH'  - 不参与择时的标的
    index_condition_type: str = '大于均线'  - 指数条件类型
    index_offset: float = 0.0        - 指数偏移
    mom_type: str = '百分比'         - 动量类型
    mom_value: float = 0.1           - 动量值
    mom_models: str = '动量1'        - 动量模型
    mom_daily: int = 25              - 动量计算天数
    period: int = 20                 - 周期
    short_ma: int = 3                - 短期均线
    long_ma: int = 20                - 长期均线
    enable_mom_filter: bool = False  - 启用动量过滤
    max_value: float = 5             - 最大值
    mini_value: float = 0            - 最小值
    max_rank: int = 1                - 最大排名
    min_rank: int = 2                - 最小排名
    enable_buy_condition: bool = False  - 启用买入条件
    enable_sell_condition: bool = False  - 启用卖出条件
    buy_condition_type: str = '涨幅'  - 买入条件类型
    buy_period: int = 20             - 买入周期
    buy_period_ratio: float = 0.1    - 买入周期比例
    buy_offset: float = 0.0          - 买入偏移
    sell_condition_type: str = '跌幅'  - 卖出条件类型
    sell_period: int = 20            - 卖出周期
    sell_period_ratio: float = -0.1  - 卖出周期比例
    sell_offset: float = 0.0         - 卖出偏移
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_amount: float = 1000        - 卖出金额
    interval: int = 1                - 间隔
"""

print("\n" + "=" * 60)
print("📊 综合动量回测")
print("=" * 60)

result = client.xg_more_mom_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    enable_index_timing=False,
    index_mean_line=20,
    index_not_trader='513100.SH,518880.SH',
    index_condition_type='大于均线',
    index_offset=0.0,
    mom_type='百分比',
    mom_value=0.1,
    mom_models='动量1',
    mom_daily=25,
    period=20,
    short_ma=3,
    long_ma=20,
    enable_mom_filter=False,
    max_value=5,
    mini_value=0,
    max_rank=1,
    min_rank=2,
    enable_buy_condition=False,
    enable_sell_condition=False,
    buy_condition_type='涨幅',
    buy_period=20,
    buy_period_ratio=0.1,
    buy_offset=0.0,
    sell_condition_type='跌幅',
    sell_period=20,
    sell_period_ratio=-0.1,
    sell_offset=0.0,
    sell_zdf=0.03,
    sell_amount=1000,
    interval=1
)
print("综合动量回测结果：")
print(result)
```
## 8. 条件因子回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例22：条件因子回测
# ============================================================
"""
参数说明：
    start_date: str = '20250101'     - 回测开始日期
    end_date: str = '20261201'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    min_commission: float = 0        - 最低佣金
    trader_type: str = '百分比'      - 交易类型
    trader_value: float = 0.5        - 交易值
    hold_stock_limit: int = 2        - 持股上限
    is_open_user_factor: bool = True - 启用自定义因子
    user_factor_list: str = 'close,high,low,open,amount,volume,zdf'  - 因子列表
    user_factor_cacal: str = '{"因子名": "计算公式"}'  - 因子计算
    buy_condi_factor: str = '{"因子名": {"选择类型": "and", "选择方向": "大于", "值": 0}}'  - 买入条件
    rank_factor: str = '{"因子名": "降序"}'  - 排序因子
    sell_condi_factor: str = '{"因子名": {"选择类型": "or", "选择方向": "等于", "值": false}}'  - 卖出条件
    sell_type: str = '金额'          - 卖出类型
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_value: float = 1000         - 卖出金额
    max_workers: int = 4             - 最大进程数
    interval: int = 1                - 间隔
    min_hold_days: int = 1           - 最少持有天数
    risk_free_rate: float = 0.02     - 无风险利率
    slippage: float = 0              - 滑点
    enable_limit_up_down_filter: bool = True  - 启用涨跌停过滤
    max_single_position_ratio: float = 1.0  - 最大单仓位比例
"""

print("\n" + "=" * 60)
print("📊 条件因子回测")
print("=" * 60)

result = client.xg_condi_factor_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),True,False)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    buy_condi_factor='{"收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true}, "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}}',
    rank_factor='{"均线评分": "降序"}',
    sell_condi_factor='{"收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false}, "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}}',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("条件因子回测结果：")
print(result)
```
## 9. 排序多因子回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例23：排序多因子回测
# ============================================================
"""
参数说明：
    start_date: str = '20250101'     - 回测开始日期
    end_date: str = '20261201'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    min_commission: float = 0        - 最低佣金
    trader_type: str = '百分比'      - 交易类型
    trader_value: float = 0.5        - 交易值
    hold_stock_limit: int = 2        - 持股上限
    is_open_user_factor: bool = True - 启用自定义因子
    user_factor_list: str = 'close,high,low,open,amount,volume,zdf'  - 因子列表
    user_factor_cacal: str = '{"因子名": "计算公式"}'  - 因子计算
    is_open_buy_condi: bool = True   - 启用买入条件
    buy_condi_factor: str = '{"因子名": {"选择类型": "and", "选择方向": "大于", "值": 0}}'  - 买入条件
    rank_factor: str = '{"因子名": {"相关性": "正相关", "权重": 1}}'  - 排序因子
    total_factor_rank: str = '降序'  - 总因子排序
    sell_type: str = '金额'          - 卖出类型
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_value: float = 1000         - 卖出金额
    max_workers: int = 4             - 最大进程数
    interval: int = 1                - 间隔
    min_hold_days: int = 1           - 最少持有天数
    risk_free_rate: float = 0.02     - 无风险利率
    slippage: float = 0              - 滑点
    enable_limit_up_down_filter: bool = True  - 启用涨跌停过滤
    max_single_position_ratio: float = 1.0  - 最大单仓位比例
"""

print("\n" + "=" * 60)
print("📊 排序多因子回测")
print("=" * 60)

result = client.xg_rank_factor_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),0,1)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    is_open_buy_condi=True,
    buy_condi_factor='{"25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0}, "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}}',
    rank_factor='{"25日回归动量": {"相关性": "正相关", "权重": 1}}',
    total_factor_rank='降序',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("排序多因子回测结果：")
print(result)
```
## 10均值方差最优资产组合回测
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例42：均值方差最优资产组合回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    max_workers: int = 4             - 最大进程数
    lookback_days: int = 60          - 计算协方差矩阵使用的历史数据天数
    max_weight: float = 0.6          - 最大单只权重
    min_weight: float = 0.05         - 最小单只权重
    lambda_risk: float = 2.0         - 风险厌恶系数
    interval: int = 5                - 调仓间隔（交易日）
"""

print("\n" + "=" * 60)
print("📊 均值方差最优资产组合回测")
print("=" * 60)

result = client.xg_mean_var_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    lookback_days=60,
    max_weight=0.6,
    min_weight=0.05,
    lambda_risk=2.0,
    interval=5
)
print("均值方差最优资产组合回测结果：")
print(result)
```
# 四、个人策略模拟交易
## 1. 定投策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例24：定投策略模拟交易
# ============================================================
"""
参数说明：与 xg_dt_backtrader 完全相同
    新增参数：
    st_name: str = '小果测试'       - 策略名称
    open_show: str = '是'           - 是否显示
"""

result = client.xg_dt_backtrader_moni(
    st_name='我的定投策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    dt_interval=20,
    dt_type='金额',
    dt_value=1000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("定投策略模拟交易结果：")
print(result)
```
## 2. 动量策略模拟交易

```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例25：动量策略模拟交易
# ============================================================
"""
参数说明：与 xg_mom_backtrader 完全相同
"""

result = client.xg_mom_backtrader_moni(
    st_name='我的动量策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    mom_type='百分比',
    mom_value=1,
    mom_daily=25,
    min_mom=0,
    max_mom=5,
    buy_rank=1,
    sell_zdf=0.03,
    sell_amount=1000
)
print("动量策略模拟交易结果：")
print(result)
```
## 3. 资产配置策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例26：资产配置策略模拟交易
# ============================================================
"""
参数说明：与 xg_pz_backtrader 完全相同
"""

result = client.xg_pz_backtrader_moni(
    st_name='我的资产配置策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.4,0.4,0.2',
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置策略模拟交易结果：")
print(result)
```
## 4. 资产配置平衡策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例27：资产配置平衡策略模拟交易
# ============================================================
"""
参数说明：与 xg_zcph_backtrader 完全相同
"""

result = client.xg_zcph_backtrader_moni(
    st_name='我的资产配置平衡策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.35,0.35,0.3',
    deviation_list='0.1,0.1,0.05',
    interval=20,
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置平衡策略模拟交易结果：")
print(result)
```
## 5. 网格策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例28：网格策略模拟交易
# ============================================================
"""
参数说明：与 xg_gd_backtrader 完全相同
"""

result = client.xg_gd_backtrader_moni(
    st_name='我的网格策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    gd_interval=1,
    gd_bc_type_list='百分比,百分比',
    gd_buy_bc_list='0.03,0.02',
    gd_sell_bc_list='-0.02,-0.015',
    gd_atr_ratio_list='2.0,2.0',
    gd_type_list='金额,金额',
    gd_value_list='1000,1500',
    init_position_ratio_list='0.1,0.15',
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("网格策略模拟交易结果：")
print(result)
```
## 6. 海龟策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例29：海龟策略模拟交易
# ============================================================
"""
参数说明：与 xg_hg_backtrader 完全相同
"""

result = client.xg_hg_backtrader_moni(
    st_name='我的海龟策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    entry_period=20,
    exit_period=10,
    n_period=20,
    risk_per_trade=0.01,
    risk_per_unit=0.02,
    max_units=4,
    add_unit_threshold=0.5,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000
)
print("海龟策略模拟交易结果：")
print(result)
```
## 7. 综合动量策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例30：综合动量策略模拟交易
# ============================================================
"""
参数说明：与 xg_more_mom_backtrader 完全相同
"""

result = client.xg_more_mom_backtrader_moni(
    st_name='我的综合动量策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    enable_index_timing=False,
    index_mean_line=20,
    index_not_trader='513100.SH,518880.SH',
    index_condition_type='大于均线',
    index_offset=0.0,
    mom_type='百分比',
    mom_value=0.1,
    mom_models='动量1',
    mom_daily=25,
    period=20,
    short_ma=3,
    long_ma=20,
    enable_mom_filter=False,
    max_value=5,
    mini_value=0,
    max_rank=1,
    min_rank=2,
    enable_buy_condition=False,
    enable_sell_condition=False,
    buy_condition_type='涨幅',
    buy_period=20,
    buy_period_ratio=0.1,
    buy_offset=0.0,
    sell_condition_type='跌幅',
    sell_period=20,
    sell_period_ratio=-0.1,
    sell_offset=0.0,
    sell_zdf=0.03,
    sell_amount=1000,
    interval=1
)
print("综合动量策略模拟交易结果：")
print(result)
```
## 8. 条件因子策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例31：条件因子策略模拟交易
# ============================================================
"""
参数说明：与 xg_condi_factor_backtrader 完全相同
"""

result = client.xg_condi_factor_backtrader_moni(
    st_name='我的条件因子策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),True,False)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    buy_condi_factor='{"收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true}, "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}}',
    rank_factor='{"均线评分": "降序"}',
    sell_condi_factor='{"收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false}, "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}}',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("条件因子策略模拟交易结果：")
print(result)
```
## 9. 排序多因子策略模拟交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例32：排序多因子策略模拟交易
# ============================================================
"""
参数说明：与 xg_rank_factor_backtrader 完全相同
"""

result = client.xg_rank_factor_backtrader_moni(
    st_name='我的排序多因子策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),0,1)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    is_open_buy_condi=True,
    buy_condi_factor='{"25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0}, "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}}',
    rank_factor='{"25日回归动量": {"相关性": "正相关", "权重": 1}}',
    total_factor_rank='降序',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("排序多因子策略模拟交易结果：")
print(result)
```
## 10均值方差策略模拟交易
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例43：均值方差策略模拟交易
# ============================================================
"""
参数说明：与 xg_mean_var_backtrader 完全相同
    新增参数：
    st_name: str = '小果均值方差策略'   - 策略名称
    open_show: str = '是'           - 是否公开策略
"""

result = client.xg_mean_var_backtrader_moni(
    st_name='我的均值方差策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    lookback_days=60,
    max_weight=0.6,
    min_weight=0.05,
    lambda_risk=2.0,
    interval=5
)
print("均值方差策略模拟交易结果：")
print(result)
```
# 五、社区模拟策略接口
## 1. 定投策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例33：定投策略社区交易
# ============================================================
"""
参数说明：与 xg_dt_backtrader_moni 完全相同
"""

result = client.xg_dt_backtrader_moni_sq(
    st_name='社区定投策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    dt_interval=20,
    dt_type='金额',
    dt_value=1000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("定投策略社区交易结果：")
print(result)
```
## 2. 动量策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例34：动量策略社区交易
# ============================================================
"""
参数说明：与 xg_mom_backtrader_moni 完全相同
"""

result = client.xg_mom_backtrader_moni_sq(
    st_name='社区动量策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    mom_type='百分比',
    mom_value=1,
    mom_daily=25,
    min_mom=0,
    max_mom=5,
    buy_rank=1,
    sell_zdf=0.03,
    sell_amount=1000
)
print("动量策略社区交易结果：")
print(result)
```
## 3. 资产配置策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例35：资产配置策略社区交易
# ============================================================
"""
参数说明：与 xg_pz_backtrader_moni 完全相同
"""

result = client.xg_pz_backtrader_moni_sq(
    st_name='社区资产配置策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.4,0.4,0.2',
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置策略社区交易结果：")
print(result) 
```
## 4. 资产配置平衡策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例36：资产配置平衡策略社区交易
# ============================================================
"""
参数说明：与 xg_zcph_backtrader_moni 完全相同
"""

result = client.xg_zcph_backtrader_moni_sq(
    st_name='社区资产配置平衡策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.35,0.35,0.3',
    deviation_list='0.1,0.1,0.05',
    interval=20,
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置平衡策略社区交易结果：")
print(result)
```
## 5. 网格策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例37：网格策略社区交易
# ============================================================
"""
参数说明：与 xg_gd_backtrader_moni 完全相同
"""

result = client.xg_gd_backtrader_moni_sq(
    st_name='社区网格策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    gd_interval=1,
    gd_bc_type_list='百分比,百分比',
    gd_buy_bc_list='0.03,0.02',
    gd_sell_bc_list='-0.02,-0.015',
    gd_atr_ratio_list='2.0,2.0',
    gd_type_list='金额,金额',
    gd_value_list='1000,1500',
    init_position_ratio_list='0.1,0.15',
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("网格策略社区交易结果：")
print(result)
```
## 6. 海龟策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例38：海龟策略社区交易
# ============================================================
"""
参数说明：与 xg_hg_backtrader_moni 完全相同
"""

result = client.xg_hg_backtrader_moni_sq(
    st_name='社区海龟策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    entry_period=20,
    exit_period=10,
    n_period=20,
    risk_per_trade=0.01,
    risk_per_unit=0.02,
    max_units=4,
    add_unit_threshold=0.5,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000
)
print("海龟策略社区交易结果：")
print(result)
```
## 7. 综合动量策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例39：综合动量策略社区交易
# ============================================================
"""
参数说明：与 xg_more_mom_backtrader_moni 完全相同
"""

result = client.xg_more_mom_backtrader_moni_sq(
    st_name='社区综合动量策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    enable_index_timing=False,
    index_mean_line=20,
    index_not_trader='513100.SH,518880.SH',
    index_condition_type='大于均线',
    index_offset=0.0,
    mom_type='百分比',
    mom_value=0.1,
    mom_models='动量1',
    mom_daily=25,
    period=20,
    short_ma=3,
    long_ma=20,
    enable_mom_filter=False,
    max_value=5,
    mini_value=0,
    max_rank=1,
    min_rank=2,
    enable_buy_condition=False,
    enable_sell_condition=False,
    buy_condition_type='涨幅',
    buy_period=20,
    buy_period_ratio=0.1,
    buy_offset=0.0,
    sell_condition_type='跌幅',
    sell_period=20,
    sell_period_ratio=-0.1,
    sell_offset=0.0,
    sell_zdf=0.03,
    sell_amount=1000,
    interval=1
)
print("综合动量策略社区交易结果：")
print(result)
```
## 8. 条件因子策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例40：条件因子策略社区交易
# ============================================================
"""
参数说明：与 xg_condi_factor_backtrader_moni 完全相同
"""

result = client.xg_condi_factor_backtrader_moni_sq(
    st_name='社区条件因子策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),True,False)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    buy_condi_factor='{"收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true}, "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}}',
    rank_factor='{"均线评分": "降序"}',
    sell_condi_factor='{"收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false}, "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}}',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("条件因子策略社区交易结果：")
print(result)
```
## 9. 排序多因子策略社区交易
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例41：排序多因子策略社区交易
# ============================================================
"""
参数说明：与 xg_rank_factor_backtrader_moni 完全相同
"""

result = client.xg_rank_factor_backtrader_moni_sq(
    st_name='社区排序多因子策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),0,1)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    is_open_buy_condi=True,
    buy_condi_factor='{"25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0}, "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}}',
    rank_factor='{"25日回归动量": {"相关性": "正相关", "权重": 1}}',
    total_factor_rank='降序',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("排序多因子策略社区交易结果：")
print(result)
```
## 10均值方差策略社区交易
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例44：均值方差策略社区交易
# ============================================================
"""
参数说明：与 xg_mean_var_backtrader_moni 完全相同
"""

result = client.xg_mean_var_backtrader_moni_sq(
    st_name='社区均值方差策略',
    open_show='是',
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    lookback_days=60,
    max_weight=0.6,
    min_weight=0.05,
    lambda_risk=2.0,
    interval=5
)
print("均值方差策略社区交易结果：")
print(result)
```









# 六、多标的量化分析接口
## 1相关性矩阵
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例45：计算多标的收益率相关性矩阵
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 开始日期
    end_date: str = '20500101'       - 结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    max_workers: int = 4             - 最大进程数
    method: str = 'pearson'          - 相关性计算方法：pearson/spearman/kendall
    risk_free_rate: float = 0.03     - 无风险利率

返回数据：
    correlation_matrix   - 相关性矩阵
    correlation_matrix_index - 矩阵索引（股票代码列表）
    covariance_matrix    - 协方差矩阵
    stock_list           - 股票列表
    method               - 使用的计算方法
"""

print("\n" + "=" * 60)
print("📊 多标的收益率相关性矩阵")
print("=" * 60)

result = client.xg_stock_cov_correlation(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03
)
print(result)
```
## 2 协方差矩阵
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例46：计算多标的收益率协方差矩阵
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 开始日期
    end_date: str = '20500101'       - 结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    max_workers: int = 4             - 最大进程数
    method: str = 'pearson'          - 相关性计算方法
    risk_free_rate: float = 0.03     - 无风险利率
    annualized: bool = True          - 是否年化协方差矩阵

返回数据：
    covariance_matrix    - 协方差矩阵
    covariance_matrix_index - 矩阵索引
    standard_deviations  - 标准差（年化）
    stock_list           - 股票列表
    annualized           - 是否年化
"""

print("\n" + "=" * 60)
print("📊 多标的收益率协方差矩阵")
print("=" * 60)

result = client.xg_stock_cov_covariance(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03,
    annualized=True
)
print(result)
```
## 3投资组合优化
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例47：多标的投资组合优化
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 开始日期
    end_date: str = '20500101'       - 结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    max_workers: int = 4             - 最大进程数
    method: str = 'pearson'          - 相关性计算方法
    risk_free_rate: float = 0.03     - 无风险利率
    target_return: float = None      - 目标收益率（年化），可选

返回组合：
    min_variance         - 最小方差组合
    max_sharpe           - 最大夏普比率组合
    risk_parity          - 风险平价组合
    equal_weight         - 等权重组合（基准）
    target_return_portfolio - 目标收益组合（如果指定target_return）

每个组合包含：
    weights              - 各标的权重
    expected_return      - 预期收益率（年化）
    volatility           - 波动率（年化）
    sharpe_ratio         - 夏普比率
"""

print("\n" + "=" * 60)
print("📊 多标的投资组合优化")
print("=" * 60)

# 不指定目标收益率
result = client.xg_stock_cov_portfolio(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03,
    target_return=None
)
print("投资组合优化结果：")
print(result)

# 指定目标收益率
print("\n" + "-" * 40)
print("指定目标收益率 15%")
result = client.xg_stock_cov_portfolio(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03,
    target_return=0.15
)
print(result)
```
## 4股票组合分析接口
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例48：小果股票分析系统 - 组合收益分析
# ============================================================
"""
参数说明：
    start_date: str = '20240101'     - 开始日期
    end_date: str = '20261231'       - 结束日期
    stock_list: str = '159915.SZ,518880.SH,510300.SH'  - 股票列表
    stock_weight: str = '0.4,0.3,0.3'  - 股票权重（自动归一化）
    index_stock: str = '000300.SH'   - 基准指数
    max_workers: int = 4             - 最大进程数
    risk_free_rate: float = 0.03     - 无风险利率

返回数据结构：
    summary              - 基本摘要信息（日期范围、股票数量等）
    performance_metrics  - 完整绩效指标（50+项）
    annual_performance   - 年度绩效
    rolling_metrics      - 滚动指标（60日窗口）
    period_returns       - 周期收益（日/周/月/年）
    equity_curve         - 权益曲线（每日净值）
    weight_info          - 个股权重信息
    raw_data             - 原始日度数据

绩效指标包括：
    total_return         - 总收益率
    annual_return        - 年化收益率
    annual_std           - 年化波动率
    sharpe_ratio         - 夏普比率
    max_drawdown         - 最大回撤
    max_drawdown_duration - 最大回撤持续天数
    win_rate             - 胜率
    positive_ratio       - 正收益比例
    beta                 - Beta系数
    alpha                - Alpha系数
    information_ratio    - 信息比率
    tracking_error       - 跟踪误差
    calmar_ratio         - 卡玛比率
    sortino_ratio        - 索提诺比率
"""

print("\n" + "=" * 60)
print("📊 小果股票分析系统 - 组合收益分析")
print("=" * 60)

result = client.xg_stock_analysis(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,518880.SH,510300.SH',
    stock_weight='0.4,0.3,0.3',
    index_stock='000300.SH',
    max_workers=4,
    risk_free_rate=0.03
)

print("股票组合分析结果：")
print(f"状态: {result.get('status')}")
print(f"消息: {result.get('message')}")

# 提取绩效指标
metrics = result.get('performance_metrics', {})
print(f"\n📈 绩效指标:")
print(f"  总收益率: {metrics.get('total_return', 0)*100:.2f}%")
print(f"  年化收益率: {metrics.get('annual_return', 0)*100:.2f}%")
print(f"  年化波动率: {metrics.get('annual_std', 0)*100:.2f}%")
print(f"  夏普比率: {metrics.get('sharpe_ratio', 0):.4f}")
print(f"  最大回撤: {metrics.get('max_drawdown', 0)*100:.2f}%")
print(f"  胜率: {metrics.get('positive_ratio', 0)*100:.2f}%")
if 'beta' in metrics:
    print(f"  Beta: {metrics.get('beta', 0):.4f}")
if 'alpha' in metrics:
    print(f"  Alpha: {metrics.get('alpha', 0)*100:.2f}%")
```
# 七股票分钟数据
## 获取5分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例57：获取5分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '5'           - 频率（5/15/30/60）
    adjustflag: str = '2'          - 复权类型（1-不复权 2-前复权 3-后复权）
"""

print("\n" + "=" * 60)
print("📊 获取5分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_5(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='5',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条5分钟数据（mini）")
print(df.head())
```
## 2获取5分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例57：获取5分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '5'           - 频率（5/15/30/60）
    adjustflag: str = '2'          - 复权类型（1-不复权 2-前复权 3-后复权）
"""

print("\n" + "=" * 60)
print("📊 获取5分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_5(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='5',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条5分钟数据（mini）")
print(df.head())
```
## 3获取15分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例58：获取15分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '15'          - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取15分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_15(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='15',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条15分钟数据（mini）")
print(df.head()
```
## 4 获取30分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例59：获取30分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '30'          - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取30分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_30(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='30',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条30分钟数据（mini）")
print(df.head())
```
## 5获取60分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例60：获取60分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '60'          - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取60分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_60(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='60',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条60分钟数据（mini）")
print(df.head())
```
## 6 获取日线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例61：获取日线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'd'           - 频率（d/w/m）
    adjustflag: str = '2'          - 复权类型（1-不复权 2-前复权 3-后复权）

返回字段：
    date, open, high, low, close, volume, amount
"""

print("\n" + "=" * 60)
print("📊 获取日线数据")
print("=" * 60)

result = client.query_history_k_data_plus_d(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='d',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条日线数据")
print(df.head())
```
## 7 获取周线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例62：获取周线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'w'           - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取周线数据")
print("=" * 60)

result = client.query_history_k_data_plus_w(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='w',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条周线数据")
print(df.head())
```
## 8获取月线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例63：获取月线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'm'           - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取月线数据")
print("=" * 60)

result = client.query_history_k_data_plus_m(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='m',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条月线数据")
print(df.head())
```
# 八指数K线数据接口
## 1获取指数日线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例64：获取指数日线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.000001'     - 指数代码（sh.000001 上证指数，sz.399001 深证成指）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'd'           - 频率（d/w/m）
"""

print("\n" + "=" * 60)
print("📊 获取指数日线数据")
print("=" * 60)

result = client.query_history_k_data_plus_index_d(
    stock='sh.000001',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='d'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条指数日线数据")
print(df.head())
```
## 2获取指数周线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例65：获取指数周线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.000001'     - 指数代码
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'w'           - 频率
"""

print("\n" + "=" * 60)
print("📊 获取指数周线数据")
print("=" * 60)

result = client.query_history_k_data_plus_index_w(
    stock='sh.000001',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='w'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条指数周线数据")
print(df.head())
```
## 3获取指数月线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例66：获取指数月线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.000001'     - 指数代码
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'm'           - 频率
"""

print("\n" + "=" * 60)
print("📊 获取指数月线数据")
print("=" * 60)

result = client.query_history_k_data_plus_index_m(
    stock='sh.000001',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='m'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条指数月线数据")
print(df.head())
```
# 九 财务数据
## 1获取盈利能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例1：获取盈利能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码，格式：sh.600031 或 sz.000001
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【盈利能力 - query_profit_data 返回字段】
    code            - 证券代码
    pubDate         - 公司发布财报的日期
    statDate        - 财报统计的季度的最后一天，如2017-03-31, 2017-06-30
    roeAvg          - 净资产收益率(平均)(%)，归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
    npMargin        - 销售净利率(%)，净利润/营业收入*100%
    gpMargin        - 销售毛利率(%)，毛利/营业收入100%=(营业收入-营业成本)/营业收入100%
    netProfit       - 净利润(元)
    epsTTM          - 每股收益，归属母公司股东的净利润TTM/最新总股本
    MBRevenue       - 主营营业收入(元)
    totalShare      - 总股本
    liqaShare       - 流通股本
"""

print("\n" + "=" * 60)
print("📊 获取盈利能力数据")
print("=" * 60)

result = client.query_profit_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条盈利能力数据")
print(df.head())

# 打印关键指标
if not df.empty:
    print("\n📈 关键盈利能力指标：")
    print(f"  净资产收益率(平均): {df['roeAvg'].iloc[0] if 'roeAvg' in df.columns else 'N/A'}")
    print(f"  销售净利率: {df['npMargin'].iloc[0] if 'npMargin' in df.columns else 'N/A'}")
    print(f"  销售毛利率: {df['gpMargin'].iloc[0] if 'gpMargin' in df.columns else 'N/A'}")
    print(f"  净利润: {df['netProfit'].iloc[0] if 'netProfit' in df.columns else 'N/A'}")
```
## 2获取营运能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例2：获取营运能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【营运能力 - query_operation_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    NRTurnRatio         - 应收账款周转率(次)，营业收入/[(期初应收票据及应收账款净额+期末应收票据及应收账款净额)/2]
    NRTurnDays          - 应收账款周转天数(天)，季报天数/应收账款周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    INVTurnRatio        - 存货周转率(次)，营业成本/[(期初存货净额+期末存货净额)/2]
    INVTurnDays         - 存货周转天数(天)，季报天数/存货周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    CATurnRatio         - 流动资产周转率(次)，营业总收入/[(期初流动资产+期末流动资产)/2]
    AssetTurnRatio      - 总资产周转率，营业总收入/[(期初资产总额+期末资产总额)/2]
"""

print("\n" + "=" * 60)
print("📊 获取营运能力数据")
print("=" * 60)

result = client.query_operation_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条营运能力数据")
print(df.head())

if not df.empty:
    print("\n📈 关键营运能力指标：")
    print(f"  应收账款周转率: {df['NRTurnRatio'].iloc[0] if 'NRTurnRatio' in df.columns else 'N/A'}")
    print(f"  存货周转率: {df['INVTurnRatio'].iloc[0] if 'INVTurnRatio' in df.columns else 'N/A'}")
    print(f"  总资产周转率: {df['AssetTurnRatio'].iloc[0] if 'AssetTurnRatio' in df.columns else 'N/A'}")
```
## 3获取成长能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例3：获取成长能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【成长能力 - query_growth_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    YOYEquity           - 净资产同比增长率，(本期净资产-上年同期净资产)/上年同期净资产的绝对值*100%
    YOYAsset            - 总资产同比增长率，(本期总资产-上年同期总资产)/上年同期总资产的绝对值*100%
    YOYNI               - 净利润同比增长率，(本期净利润-上年同期净利润)/上年同期净利润的绝对值*100%
    YOYEPSBasic         - 基本每股收益同比增长率，(本期基本每股收益-上年同期基本每股收益)/上年同期基本每股收益的绝对值*100%
    YOYPNI              - 归属母公司股东净利润同比增长率，(本期归属母公司股东净利润-上年同期归属母公司股东净利润)/上年同期归属母公司股东净利润的绝对值*100%
"""

print("\n" + "=" * 60)
print("📊 获取成长能力数据")
print("=" * 60)

result = client.query_growth_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条成长能力数据")
print(df.head())

if not df.empty:
    print("\n📈 关键成长能力指标：")
    print(f"  净资产同比增长率: {df['YOYEquity'].iloc[0] if 'YOYEquity' in df.columns else 'N/A'}")
    print(f"  总资产同比增长率: {df['YOYAsset'].iloc[0] if 'YOYAsset' in df.columns else 'N/A'}")
    print(f"  净利润同比增长率: {df['YOYNI'].iloc[0] if 'YOYNI' in df.columns else 'N/A'}")
    print(f"  归属母公司股东净利润同比增长率: {df['YOYPNI'].iloc[0] if 'YOYPNI' in df.columns else 'N/A'}")
```
## 4 获取偿债能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例4：获取偿债能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【偿债能力 - query_balance_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    currentRatio        - 流动比率，流动资产/流动负债
    quickRatio          - 速动比率，(流动资产-存货净额)/流动负债
    cashRatio           - 现金比率，(货币资金+交易性金融资产)/流动负债
    YOYLiability        - 总负债同比增长率，(本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%
    liabilityToAsset    - 资产负债率，负债总额/资产总额
    assetToEquity       - 权益乘数，资产总额/股东权益总额=1/(1-资产负债率)
"""

print("\n" + "=" * 60)
print("📊 获取偿债能力数据")
print("=" * 60)

result = client.query_balance_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条偿债能力数据")
print(df.head())

if not df.empty:
    print("\n📈 关键偿债能力指标：")
    print(f"  流动比率: {df['currentRatio'].iloc[0] if 'currentRatio' in df.columns else 'N/A'}")
    print(f"  速动比率: {df['quickRatio'].iloc[0] if 'quickRatio' in df.columns else 'N/A'}")
    print(f"  资产负债率: {df['liabilityToAsset'].iloc[0] if 'liabilityToAsset' in df.columns else 'N/A'}")
```
## 5获取现金流量数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例5：获取现金流量数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【现金流量 - query_cash_flow_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    CAToAsset           - 流动资产除以总资产
    NCAToAsset          - 非流动资产除以总资产
    tangibleAssetToAsset - 有形资产除以总资产
    ebitToInterest      - 已获利息倍数，息税前利润/利息费用
    CFOToOR             - 经营活动产生的现金流量净额除以营业收入
    CFOToNP             - 经营性现金净流量除以净利润
    CFOToGr             - 经营性现金净流量除以营业总收入
"""

print("\n" + "=" * 60)
print("📊 获取现金流量数据")
print("=" * 60)

result = client.query_cash_flow_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条现金流量数据")
print(df.head())

if not df.empty:
    print("\n📈 关键现金流量指标：")
    print(f"  已获利息倍数: {df['ebitToInterest'].iloc[0] if 'ebitToInterest' in df.columns else 'N/A'}")
    print(f"  经营性现金净流量/营业收入: {df['CFOToOR'].iloc[0] if 'CFOToOR' in df.columns else 'N/A'}")
```
## 6 获取杜邦指数数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="数据库服务器",
    port=数据库端口,
    user="自己名称",
    password="自己密码",
    auth_code="自己的token"
)

# ============================================================
# 完整示例6：获取杜邦指数数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【杜邦指数 - query_dupont_data 返回字段】
    code                    - 证券代码
    pubDate                 - 公司发布财报的日期
    statDate                - 财报统计的季度的最后一天
    dupontROE               - 净资产收益率，归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
    dupontAssetStoEquity    - 权益乘数，反映企业财务杠杆效应强弱和财务风险，平均总资产/平均归属于母公司的股东权益
    dupontAssetTurn         - 总资产周转率，反映企业资产管理效率的指标，营业总收入/[(期初资产总额+期末资产总额)/2]
    dupontPnitoni           - 归属母公司股东的净利润/净利润，反映母公司控股子公司百分比
    dupontNitogr            - 净利润/营业总收入，反映企业销售获利率
    dupontTaxBurden         - 净利润/利润总额，反映企业税负水平，该比值高则税负较低
    dupontIntburden         - 利润总额/息税前利润，反映企业利息负担，该比值高则税负较低
    dupontEbittogr          - 息税前利润/营业总收入，反映企业经营利润率
"""

print("\n" + "=" * 60)
print("📊 获取杜邦指数数据")
print("=" * 60)

result = client.query_dupont_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条杜邦指数数据")
print(df.head())

if not df.empty:
    print("\n📈 关键杜邦指数指标：")
    print(f"  净资产收益率(ROE): {df['dupontROE'].iloc[0] if 'dupontROE' in df.columns else 'N/A'}")
    print(f"  权益乘数: {df['dupontAssetStoEquity'].iloc[0] if 'dupontAssetStoEquity' in df.columns else 'N/A'}")
    print(f"  总资产周转率: {df['dupontAssetTurn'].iloc[0] if 'dupontAssetTurn' in df.columns else 'N/A'}")
    print(f"  销售净利率: {df['dupontNitogr'].iloc[0] if 'dupontNitogr' in df.columns else 'N/A'}")
```
# 十全部代码
```
'''
作者:小果
微信:xg_quant
'''
import requests
import json
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
import urllib.parse
class xg_quant_backtrader_data:
    """
    小果量化回测系统数据api
    小果量化数据 - API对接框架
    """
    
    def __init__(
        self,
        url: str = "数据库服务器",
        port: int = 数据库端口,  # 修复：port应该是int类型
        user: str = "小果",
        password: str = "小果",
        auth_code: str = "小果"
    ):
        """
        初始化小果量化数据客户端
        
        Args:
            url: 服务器地址
            port: 服务器端口
            user: 用户名称
            password: 用户密码
            auth_code: 授权码
        """
        self.url = url
        self.port = port
        self.user = user
        self.password = password
        self.auth_code = auth_code
        self.base_url = f"http://{url}:{port}"
        self.session = requests.Session()
        self.timeout = 120
        
        # 设置默认请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        })
    
    def _get_params(self, **kwargs) -> Dict[str, Any]:
        """构建请求参数，自动添加用户认证信息"""
        params = {
            'user': self.user,
            'password': self.password,
            'auth_code': self.auth_code,
        }
        params.update(kwargs)
        return params
    
    def _request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        method: str = 'GET',
        timeout: Optional[int] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            endpoint: API端点路径
            params: 请求参数
            method: 请求方法
            timeout: 超时时间
            verbose: 是否打印详细信息
        
        Returns:
            响应数据字典
        """
        if timeout is None:
            timeout = self.timeout
        
        url = f"{self.base_url}{endpoint}"
        
        # 清理参数中的None值
        clean_params = {k: v for k, v in params.items() if v is not None}
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=clean_params, timeout=timeout)
            else:
                response = self.session.post(url, params=clean_params, timeout=timeout)
            
            if verbose:
                print(f"📤 请求URL: {response.url[:100]}...")
                print(f"📤 状态码: {response.status_code}")
            
            response.raise_for_status()
            
            # 尝试解析JSON
            try:
                result = response.json()
                if verbose and result.get('status') == 'failed':
                    print(f"❌ 接口返回失败: {result.get('message', result.get('error', '未知错误'))}")
                    if 'info' in result:
                        print(f"📄 详细信息: {result.get('info')}")
                return result
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"📄 响应内容: {response.text[:500]}")
                return {"status": "failed", "error": "Invalid JSON response", "raw": response.text[:500]}
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            # 尝试获取更多错误信息
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"📄 错误详情: {error_detail}")
                    return {"status": "failed", "error": str(e), "detail": error_detail}
                except:
                    print(f"📄 响应内容: {e.response.text[:500]}")
                    return {"status": "failed", "error": str(e), "raw": e.response.text[:500]}
            return {"status": "failed", "error": str(e)}
    
    def _to_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        将API返回的数据转换为DataFrame
        处理NaN和Infinity值
        """
        if data.get('status') == 'failed':
            print(f"⚠️ 数据获取失败: {data.get('message', data.get('error', '未知错误'))}")
            return pd.DataFrame()
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            # 清理数据：将NaN、Infinity替换为None
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.where(pd.notnull(df), None)
            return df
        
        return pd.DataFrame()
    
    def _to_dataframe_with_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """将API返回的数据转换为包含元信息的DataFrame"""
        if data.get('status') == 'failed':
            return {
                'status': 'failed', 
                'data': pd.DataFrame(), 
                'info': data.get('message', data.get('error', '未知错误'))
            }
        
        df = pd.DataFrame(data.get('data', []))
        # 清理数据
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.where(pd.notnull(df), None)
        
        result = {
            'status': data.get('status', 'success'),
            'data': df,
            'total': data.get('total', len(df)),
            'message': data.get('message', ''),
            'available_columns': data.get('available_columns', []),
            'selected_columns': data.get('selected_columns', []),
        }
        for key in ['stock', 'start_date', 'end_date', 'table', 'report_date']:
            if key in data:
                result[key] = data[key]
        return result

    # ============================================================
    # 一、回测接口（类方法名不带数字，但请求路径带 _1）
    # ============================================================
    
    def xg_dt_backtrader(
        self,
        start_date: str = '20260701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        dt_interval: int = 20,
        dt_type: str = '金额',
        dt_value: float = 1000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """定投回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, dt_interval=dt_interval,
            dt_type=dt_type, dt_value=dt_value, sell_zdf=sell_zdf,
            buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_dt_backtrader_1', params)
    
    def xg_mom_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        mom_type: str = '百分比',
        mom_value: float = 1,
        mom_daily: int = 25,
        min_mom: float = 0,
        max_mom: float = 5,
        buy_rank: int = 1,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000
    ) -> Dict[str, Any]:
        """动量回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            mom_type=mom_type, mom_value=mom_value, mom_daily=mom_daily,
            min_mom=min_mom, max_mom=max_mom, buy_rank=buy_rank,
            sell_zdf=sell_zdf, sell_amount=sell_amount
        )
        return self._request('/xg_mom_backtrader_1', params)
    
    def xg_pz_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.4,0.4,0.2',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, index_stock=index_stock,
            cash=cash, sell_zdf=sell_zdf, buy_zdf=buy_zdf,
            trade_value=trade_value, comm=comm
        )
        return self._request('/xg_pz_backtrader_1', params)
    
    def xg_zcph_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.35,0.35,0.3',
        deviation_list: str = '0.1,0.1,0.05',
        interval: int = 20,
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置平衡策略回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, deviation_list=deviation_list,
            interval=interval, index_stock=index_stock, cash=cash,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_zcph_backtrader_1', params)
    
    def xg_gd_backtrader(
        self,
        start_date: str = '20250701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        gd_interval: int = 1,
        gd_bc_type_list: str = '百分比,百分比',
        gd_buy_bc_list: str = '0.03,0.02',
        gd_sell_bc_list: str = '-0.02,-0.015',
        gd_atr_ratio_list: str = '2.0,2.0',
        gd_atr_period_list: str = '14,14',
        gd_type_list: str = '金额,金额',
        gd_value_list: str = '1000,1500',
        init_position_ratio_list: str = '0.1,0.15',
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """网格策略回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, gd_interval=gd_interval,
            gd_bc_type_list=gd_bc_type_list, gd_buy_bc_list=gd_buy_bc_list,
            gd_sell_bc_list=gd_sell_bc_list, gd_atr_ratio_list=gd_atr_ratio_list,
            gd_atr_period_list=gd_atr_period_list, gd_type_list=gd_type_list,
            gd_value_list=gd_value_list, init_position_ratio_list=init_position_ratio_list,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value,
            comm=comm, max_workers=max_workers
        )
        return self._request('/xg_gd_backtrader_1', params)
    
    def xg_hg_backtrader(
        self,
        start_date: str = '20240101',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        entry_period: int = 20,
        exit_period: int = 10,
        n_period: int = 20,
        risk_per_trade: float = 0.01,
        risk_per_unit: float = 0.02,
        max_units: int = 4,
        add_unit_threshold: float = 0.5,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000
    ) -> Dict[str, Any]:
        """海龟策略回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, entry_period=entry_period,
            exit_period=exit_period, n_period=n_period,
            risk_per_trade=risk_per_trade, risk_per_unit=risk_per_unit,
            max_units=max_units, add_unit_threshold=add_unit_threshold,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value
        )
        return self._request('/xg_hg_backtrader_1', params)
    
    def xg_more_mom_backtrader(
        self,
        start_date: str = '20250101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        enable_index_timing: bool = False,
        index_mean_line: int = 20,
        index_not_trader: str = '513100.SH,518880.SH',
        index_condition_type: str = '大于均线',
        index_offset: float = 0.0,
        mom_type: str = '百分比',
        mom_value: float = 0.1,
        mom_models: str = '动量1',
        mom_daily: int = 25,
        period: int = 20,
        short_ma: int = 3,
        long_ma: int = 20,
        enable_mom_filter: bool = False,
        max_value: float = 5,
        mini_value: float = 0,
        max_rank: int = 1,
        min_rank: int = 2,
        enable_buy_condition: bool = False,
        enable_sell_condition: bool = False,
        buy_condition_type: str = '涨幅',
        buy_period: int = 20,
        buy_period_ratio: float = 0.1,
        buy_offset: float = 0.0,
        sell_condition_type: str = '跌幅',
        sell_period: int = 20,
        sell_period_ratio: float = -0.1,
        sell_offset: float = 0.0,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000,
        interval: int = 1
    ) -> Dict[str, Any]:
        """综合动量回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, enable_index_timing=enable_index_timing,
            index_mean_line=index_mean_line, index_not_trader=index_not_trader,
            index_condition_type=index_condition_type, index_offset=index_offset,
            mom_type=mom_type, mom_value=mom_value, mom_models=mom_models,
            mom_daily=mom_daily, period=period, short_ma=short_ma,
            long_ma=long_ma, enable_mom_filter=enable_mom_filter,
            max_value=max_value, mini_value=mini_value,
            max_rank=max_rank, min_rank=min_rank,
            enable_buy_condition=enable_buy_condition,
            enable_sell_condition=enable_sell_condition,
            buy_condition_type=buy_condition_type, buy_period=buy_period,
            buy_period_ratio=buy_period_ratio, buy_offset=buy_offset,
            sell_condition_type=sell_condition_type, sell_period=sell_period,
            sell_period_ratio=sell_period_ratio, sell_offset=sell_offset,
            sell_zdf=sell_zdf, sell_amount=sell_amount, interval=interval
        )
        return self._request('/xg_more_mom_backtrader_1', params)
    
    def xg_condi_factor_backtrader(
        self,
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),True,False)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        buy_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true},
            "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}
        }''',
        rank_factor: str = '''{
            "均线评分": "降序"
        }''',
        sell_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false},
            "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}
        }''',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """条件因子回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            sell_condi_factor=sell_condi_factor,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_condi_factor_backtrader_1', params)
    
    def xg_rank_factor_backtrader(
        self,
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),0,1)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        is_open_buy_condi: bool = True,
        buy_condi_factor: str = '''{
            "25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0},
            "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}
        }''',
        rank_factor: str = '''{
            "25日回归动量": {"相关性": "正相关", "权重": 1}
        }''',
        total_factor_rank: str = '降序',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """排序多因子回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            is_open_buy_condi=is_open_buy_condi,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            total_factor_rank=total_factor_rank,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_rank_factor_backtrader_1', params)

    # ============================================================
    # 二、策略模拟交易接口（moni，不带 _1）
    # ============================================================
    
    def xg_dt_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        dt_interval: int = 20,
        dt_type: str = '金额',
        dt_value: float = 1000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """定投策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, dt_interval=dt_interval,
            dt_type=dt_type, dt_value=dt_value, sell_zdf=sell_zdf,
            buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_dt_backtrader_moni', params)
    
    def xg_mom_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        mom_type: str = '百分比',
        mom_value: float = 1,
        mom_daily: int = 25,
        min_mom: float = 0,
        max_mom: float = 5,
        buy_rank: int = 1,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000
    ) -> Dict[str, Any]:
        """动量策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            mom_type=mom_type, mom_value=mom_value, mom_daily=mom_daily,
            min_mom=min_mom, max_mom=max_mom, buy_rank=buy_rank,
            sell_zdf=sell_zdf, sell_amount=sell_amount
        )
        return self._request('/xg_mom_backtrader_moni', params)
    
    def xg_pz_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.4,0.4,0.2',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, index_stock=index_stock,
            cash=cash, sell_zdf=sell_zdf, buy_zdf=buy_zdf,
            trade_value=trade_value, comm=comm
        )
        return self._request('/xg_pz_backtrader_moni', params)
    
    def xg_zcph_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.35,0.35,0.3',
        deviation_list: str = '0.1,0.1,0.05',
        interval: int = 20,
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置平衡策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, deviation_list=deviation_list,
            interval=interval, index_stock=index_stock, cash=cash,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_zcph_backtrader_moni', params)
    
    def xg_gd_backtrader_moni(
        self,
        st_name: str = '小果网格测试策略',
        open_show: str = '是',
        start_date: str = '20250701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        gd_interval: int = 1,
        gd_bc_type_list: str = '百分比,百分比',
        gd_buy_bc_list: str = '0.03,0.02',
        gd_sell_bc_list: str = '-0.02,-0.015',
        gd_atr_ratio_list: str = '2.0,2.0',
        gd_atr_period_list: str = '14,14',
        gd_type_list: str = '金额,金额',
        gd_value_list: str = '1000,1500',
        init_position_ratio_list: str = '0.1,0.15',
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """网格策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, gd_interval=gd_interval,
            gd_bc_type_list=gd_bc_type_list, gd_buy_bc_list=gd_buy_bc_list,
            gd_sell_bc_list=gd_sell_bc_list, gd_atr_ratio_list=gd_atr_ratio_list,
            gd_atr_period_list=gd_atr_period_list, gd_type_list=gd_type_list,
            gd_value_list=gd_value_list,
            init_position_ratio_list=init_position_ratio_list,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value,
            comm=comm, max_workers=max_workers
        )
        return self._request('/xg_gd_backtrader_moni', params)
    
    def xg_hg_backtrader_moni(
        self,
        st_name: str = '小果海龟测试策略',
        open_show: str = '是',
        start_date: str = '20240101',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        entry_period: int = 20,
        exit_period: int = 10,
        n_period: int = 20,
        risk_per_trade: float = 0.01,
        risk_per_unit: float = 0.02,
        max_units: int = 4,
        add_unit_threshold: float = 0.5,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000
    ) -> Dict[str, Any]:
        """海龟策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, entry_period=entry_period,
            exit_period=exit_period, n_period=n_period,
            risk_per_trade=risk_per_trade, risk_per_unit=risk_per_unit,
            max_units=max_units, add_unit_threshold=add_unit_threshold,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value
        )
        return self._request('/xg_hg_backtrader_moni', params)
    
    def xg_more_mom_backtrader_moni(
        self,
        st_name: str = '小果综合动量测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        enable_index_timing: bool = False,
        index_mean_line: int = 20,
        index_not_trader: str = '513100.SH,518880.SH',
        index_condition_type: str = '大于均线',
        index_offset: float = 0.0,
        mom_type: str = '百分比',
        mom_value: float = 0.1,
        mom_models: str = '动量1',
        mom_daily: int = 25,
        period: int = 20,
        short_ma: int = 3,
        long_ma: int = 20,
        enable_mom_filter: bool = False,
        max_value: float = 5,
        mini_value: float = 0,
        max_rank: int = 1,
        min_rank: int = 2,
        enable_buy_condition: bool = False,
        enable_sell_condition: bool = False,
        buy_condition_type: str = '涨幅',
        buy_period: int = 20,
        buy_period_ratio: float = 0.1,
        buy_offset: float = 0.0,
        sell_condition_type: str = '跌幅',
        sell_period: int = 20,
        sell_period_ratio: float = -0.1,
        sell_offset: float = 0.0,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000,
        interval: int = 1
    ) -> Dict[str, Any]:
        """综合动量策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, enable_index_timing=enable_index_timing,
            index_mean_line=index_mean_line, index_not_trader=index_not_trader,
            index_condition_type=index_condition_type, index_offset=index_offset,
            mom_type=mom_type, mom_value=mom_value, mom_models=mom_models,
            mom_daily=mom_daily, period=period, short_ma=short_ma,
            long_ma=long_ma, enable_mom_filter=enable_mom_filter,
            max_value=max_value, mini_value=mini_value,
            max_rank=max_rank, min_rank=min_rank,
            enable_buy_condition=enable_buy_condition,
            enable_sell_condition=enable_sell_condition,
            buy_condition_type=buy_condition_type, buy_period=buy_period,
            buy_period_ratio=buy_period_ratio, buy_offset=buy_offset,
            sell_condition_type=sell_condition_type, sell_period=sell_period,
            sell_period_ratio=sell_period_ratio, sell_offset=sell_offset,
            sell_zdf=sell_zdf, sell_amount=sell_amount, interval=interval
        )
        return self._request('/xg_more_mom_backtrader_moni', params)
    
    def xg_condi_factor_backtrader_moni(
        self,
        st_name: str = '小果条件因子测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),True,False)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        buy_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true},
            "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}
        }''',
        rank_factor: str = '''{
            "均线评分": "降序"
        }''',
        sell_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false},
            "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}
        }''',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """条件多因子策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            sell_condi_factor=sell_condi_factor,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_condi_factor_backtrader_moni', params)
    
    def xg_rank_factor_backtrader_moni(
        self,
        st_name: str = '小果排序多因子模拟策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),0,1)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        is_open_buy_condi: bool = True,
        buy_condi_factor: str = '''{
            "25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0},
            "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}
        }''',
        rank_factor: str = '''{
            "25日回归动量": {"相关性": "正相关", "权重": 1}
        }''',
        total_factor_rank: str = '降序',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """排序多因子策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            is_open_buy_condi=is_open_buy_condi,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            total_factor_rank=total_factor_rank,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_rank_factor_backtrader_moni', params)

    # ============================================================
    # 三、社区策略接口（moni_sq，不带 _1）
    # ============================================================
    
    def xg_dt_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        dt_interval: int = 20,
        dt_type: str = '金额',
        dt_value: float = 1000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """定投策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, dt_interval=dt_interval,
            dt_type=dt_type, dt_value=dt_value, sell_zdf=sell_zdf,
            buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_dt_backtrader_moni_sq', params)
    
    def xg_mom_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        mom_type: str = '百分比',
        mom_value: float = 1,
        mom_daily: int = 25,
        min_mom: float = 0,
        max_mom: float = 5,
        buy_rank: int = 1,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000
    ) -> Dict[str, Any]:
        """动量策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            mom_type=mom_type, mom_value=mom_value, mom_daily=mom_daily,
            min_mom=min_mom, max_mom=max_mom, buy_rank=buy_rank,
            sell_zdf=sell_zdf, sell_amount=sell_amount
        )
        return self._request('/xg_mom_backtrader_moni_sq', params)
    
    def xg_pz_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.4,0.4,0.2',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, index_stock=index_stock,
            cash=cash, sell_zdf=sell_zdf, buy_zdf=buy_zdf,
            trade_value=trade_value, comm=comm
        )
        return self._request('/xg_pz_backtrader_moni_sq', params)
    
    def xg_zcph_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.35,0.35,0.3',
        deviation_list: str = '0.1,0.1,0.05',
        interval: int = 20,
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置平衡策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, deviation_list=deviation_list,
            interval=interval, index_stock=index_stock, cash=cash,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_zcph_backtrader_moni_sq', params)
    
    def xg_gd_backtrader_moni_sq(
        self,
        st_name: str = '小果网格测试策略',
        open_show: str = '是',
        start_date: str = '20250701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        gd_interval: int = 1,
        gd_bc_type_list: str = '百分比,百分比',
        gd_buy_bc_list: str = '0.03,0.02',
        gd_sell_bc_list: str = '-0.02,-0.015',
        gd_atr_ratio_list: str = '2.0,2.0',
        gd_atr_period_list: str = '14,14',
        gd_type_list: str = '金额,金额',
        gd_value_list: str = '1000,1500',
        init_position_ratio_list: str = '0.1,0.15',
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """网格策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, gd_interval=gd_interval,
            gd_bc_type_list=gd_bc_type_list, gd_buy_bc_list=gd_buy_bc_list,
            gd_sell_bc_list=gd_sell_bc_list, gd_atr_ratio_list=gd_atr_ratio_list,
            gd_atr_period_list=gd_atr_period_list, gd_type_list=gd_type_list,
            gd_value_list=gd_value_list,
            init_position_ratio_list=init_position_ratio_list,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value,
            comm=comm, max_workers=max_workers
        )
        return self._request('/xg_gd_backtrader_moni_sq', params)
    
    def xg_hg_backtrader_moni_sq(
        self,
        st_name: str = '小果海龟测试策略',
        open_show: str = '是',
        start_date: str = '20240101',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        entry_period: int = 20,
        exit_period: int = 10,
        n_period: int = 20,
        risk_per_trade: float = 0.01,
        risk_per_unit: float = 0.02,
        max_units: int = 4,
        add_unit_threshold: float = 0.5,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000
    ) -> Dict[str, Any]:
        """海龟策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, entry_period=entry_period,
            exit_period=exit_period, n_period=n_period,
            risk_per_trade=risk_per_trade, risk_per_unit=risk_per_unit,
            max_units=max_units, add_unit_threshold=add_unit_threshold,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value
        )
        return self._request('/xg_hg_backtrader_moni_sq', params)
    
    def xg_more_mom_backtrader_moni_sq(
        self,
        st_name: str = '小果综合动量测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        enable_index_timing: bool = False,
        index_mean_line: int = 20,
        index_not_trader: str = '513100.SH,518880.SH',
        index_condition_type: str = '大于均线',
        index_offset: float = 0.0,
        mom_type: str = '百分比',
        mom_value: float = 0.1,
        mom_models: str = '动量1',
        mom_daily: int = 25,
        period: int = 20,
        short_ma: int = 3,
        long_ma: int = 20,
        enable_mom_filter: bool = False,
        max_value: float = 5,
        mini_value: float = 0,
        max_rank: int = 1,
        min_rank: int = 2,
        enable_buy_condition: bool = False,
        enable_sell_condition: bool = False,
        buy_condition_type: str = '涨幅',
        buy_period: int = 20,
        buy_period_ratio: float = 0.1,
        buy_offset: float = 0.0,
        sell_condition_type: str = '跌幅',
        sell_period: int = 20,
        sell_period_ratio: float = -0.1,
        sell_offset: float = 0.0,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000,
        interval: int = 1
    ) -> Dict[str, Any]:
        """综合动量策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, enable_index_timing=enable_index_timing,
            index_mean_line=index_mean_line, index_not_trader=index_not_trader,
            index_condition_type=index_condition_type, index_offset=index_offset,
            mom_type=mom_type, mom_value=mom_value, mom_models=mom_models,
            mom_daily=mom_daily, period=period, short_ma=short_ma,
            long_ma=long_ma, enable_mom_filter=enable_mom_filter,
            max_value=max_value, mini_value=mini_value,
            max_rank=max_rank, min_rank=min_rank,
            enable_buy_condition=enable_buy_condition,
            enable_sell_condition=enable_sell_condition,
            buy_condition_type=buy_condition_type, buy_period=buy_period,
            buy_period_ratio=buy_period_ratio, buy_offset=buy_offset,
            sell_condition_type=sell_condition_type, sell_period=sell_period,
            sell_period_ratio=sell_period_ratio, sell_offset=sell_offset,
            sell_zdf=sell_zdf, sell_amount=sell_amount, interval=interval
        )
        return self._request('/xg_more_mom_backtrader_moni_sq', params)
    
    def xg_condi_factor_backtrader_moni_sq(
        self,
        st_name: str = '小果条件因子测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),True,False)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        buy_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true},
            "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}
        }''',
        rank_factor: str = '''{
            "均线评分": "降序"
        }''',
        sell_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false},
            "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}
        }''',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """条件多因子策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            sell_condi_factor=sell_condi_factor,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_condi_factor_backtrader_moni_sq', params)
    
    def xg_rank_factor_backtrader_moni_sq(
        self,
        st_name: str = '小果排序多因子社区策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),0,1)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        is_open_buy_condi: bool = True,
        buy_condi_factor: str = '''{
            "25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0},
            "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}
        }''',
        rank_factor: str = '''{
            "25日回归动量": {"相关性": "正相关", "权重": 1}
        }''',
        total_factor_rank: str = '降序',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """排序多因子策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            is_open_buy_condi=is_open_buy_condi,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            total_factor_rank=total_factor_rank,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_rank_factor_backtrader_moni_sq', params)

    # ============================================================
    # 四、数据读取接口
    # ============================================================
    
    def get_moni_trader_data(
        self,
        user: str = '小果',
        st_type: str = '动量策略',
        st_name: str = '小果动量模拟策略'
    ) -> Dict[str, Any]:
        """读取模拟交易的统计数据"""
        params = self._get_params(user=user,st_type=st_type, st_name=st_name)
        return self._request('/get_moni_trader_data', params)
    
    def get_moni_trader_data_sq(
        self,
        user: str = '小果',
        st_type: str = '动量策略',
        st_name: str = '小果动量模拟策略'
    ) -> Dict[str, Any]:
        """读取社区交易的统计数据"""
        params = self._get_params(user=user,st_type=st_type, st_name=st_name)
        return self._request('/get_moni_trader_data_sq', params)
    
    
    
    def get_stock_hist_data(
        self,
        stock: str = '513100.SH',
        start_date: str = '20200101',
        end_date: str = '20261231'
    ) -> Dict[str, Any]:
        """读取标的历史行情数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date
        )
        return self._request('/get_stock_hist_data', params)
    
    def get_stock_factor_data(
        self,
        stock: str = '513100.SH',
        start_date: str = '20200101',
        end_date: str = '20261231',
        columns: str = 'date,close,open,high,low,volume,amount'
    ) -> Dict[str, Any]:
        """读取标的因子数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            columns=columns
        )
        return self._request('/get_stock_factor_data', params)
    
    def get_stock_finance_data(
        self,
        table: str = '资产负债表',
        date: str = '2026-06-30',
        columns: str = 'secu_code,end_date,total_assets'
    ) -> Dict[str, Any]:
        """读取股票财务数据"""
        params = self._get_params(
            table=table,
            date=date,
            columns=columns
        )
        return self._request('/get_stock_finance_data', params)
        # ============================================================
    # 四、策略删除接口（单个）
    # ============================================================
    
    def del_moni_trader_data(
        self,
        user: str = '小果',
        st_type: str = '定投策略',
        st_name: str = '小果定投模拟策略公开',
        open_show: str = '是'
    ) -> Dict[str, Any]:
        """删除模拟策略数据"""
        params = self._get_params(
            user=user,
            st_type=st_type,
            st_name=st_name,
            open_show=open_show
        )
        return self._request('/del_moni_trader_data', params)
    
    def del_moni_trader_data_sq(
        self,
        user: str = '小果',
        st_type: str = '定投策略',
        st_name: str = '小果定投模拟策略公开',
        open_show: str = '是'
    ) -> Dict[str, Any]:
        """删除社区策略数据"""
        params = self._get_params(
            user=user,
            st_type=st_type,
            st_name=st_name,
            open_show=open_show
        )
        return self._request('/del_moni_trader_data_sq', params)

    # ============================================================
    # 五、批量策略管理接口
    # ============================================================
    
    def del_all_moni_trader_data(
        self,
        user: str = '小果',
        confirm: str = '是'
    ) -> Dict[str, Any]:
        """删除全部模拟策略数据"""
        params = self._get_params(
            user=user,
            confirm=confirm
        )
        return self._request('/del_all_moni_trader_data', params)
    
    def del_all_moni_trader_data_sq(
        self,
        user: str = '小果',
        confirm: str = '是'
    ) -> Dict[str, Any]:
        """删除全部社区策略数据"""
        params = self._get_params(
            user=user,
            confirm=confirm
        )
        return self._request('/del_all_moni_trader_data_sq', params)
    
    def get_all_moni_trader_data(
        self,
        user: str = '小果'
    ) -> Dict[str, Any]:
        """读取个人模拟全部策略"""
        params = self._get_params(user=user)
        return self._request('/get_all_moni_trader_data', params)
    
    def get_all_moni_trader_data_sq(
        self,
        user: str = '小果'
    ) -> Dict[str, Any]:
        """读取个人社区全部策略"""
        params = self._get_params(user=user)
        return self._request('/get_all_moni_trader_data_sq', params)

    # ============================================================
    # 六、策略执行接口
    # ============================================================
    
    def xg_condi_factor_backtrader_run(
        self,
        st_name: str = '小果条件因子测试策略',
        force_rerun: bool = False,
        save_data: bool = True
    ) -> Dict[str, Any]:
        """条件多因子策略回测执行接口"""
        params = self._get_params(
            st_name=st_name,
            force_rerun=force_rerun,
            save_data=save_data
        )
        return self._request('/xg_condi_factor_backtrader_run', params)
    ############################新添加模型**************************
    # ============================================================
    # 七、均值方差策略接口
    # ============================================================
    
    def xg_mean_var_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        lookback_days: int = 60,
        max_weight: float = 0.6,
        min_weight: float = 0.05,
        lambda_risk: float = 2.0,
        interval: int = 5
    ) -> Dict[str, Any]:
        """均值方差最优资产组合权重再平衡策略回测"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, lookback_days=lookback_days,
            max_weight=max_weight, min_weight=min_weight,
            lambda_risk=lambda_risk, interval=interval
        )
        return self._request('/xg_mean_var_backtrader_1', params)
    
    def xg_mean_var_backtrader_moni(
        self,
        st_name: str = '小果均值方差策略',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        lookback_days: int = 60,
        max_weight: float = 0.6,
        min_weight: float = 0.05,
        lambda_risk: float = 2.0,
        interval: int = 5
    ) -> Dict[str, Any]:
        """均值方差最优资产组合策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, lookback_days=lookback_days,
            max_weight=max_weight, min_weight=min_weight,
            lambda_risk=lambda_risk, interval=interval
        )
        return self._request('/xg_mean_var_backtrader_moni', params)
    
    def xg_mean_var_backtrader_moni_sq(
        self,
        st_name: str = '小果均值方差社区策略',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        lookback_days: int = 60,
        max_weight: float = 0.6,
        min_weight: float = 0.05,
        lambda_risk: float = 2.0,
        interval: int = 5
    ) -> Dict[str, Any]:
        """均值方差最优资产组合策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, lookback_days=lookback_days,
            max_weight=max_weight, min_weight=min_weight,
            lambda_risk=lambda_risk, interval=interval
        )
        return self._request('/xg_mean_var_backtrader_moni_sq', params)

    # ============================================================
    # 八、多标的量化分析接口
    # ============================================================
    
    def xg_stock_cov_correlation(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        max_workers: int = 4,
        method: str = 'pearson',
        risk_free_rate: float = 0.03
    ) -> Dict[str, Any]:
        """多标的收益率相关性矩阵"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            max_workers=max_workers, method=method,
            risk_free_rate=risk_free_rate
        )
        return self._request('/xg_stock_cov_correlation', params)
    
    def xg_stock_cov_covariance(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        max_workers: int = 4,
        method: str = 'pearson',
        risk_free_rate: float = 0.03,
        annualized: bool = True
    ) -> Dict[str, Any]:
        """多标的收益率协方差矩阵"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            max_workers=max_workers, method=method,
            risk_free_rate=risk_free_rate, annualized=annualized
        )
        return self._request('/xg_stock_cov_covariance', params)
    
    def xg_stock_cov_portfolio(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        max_workers: int = 4,
        method: str = 'pearson',
        risk_free_rate: float = 0.03,
        target_return: Optional[float] = None
    ) -> Dict[str, Any]:
        """多标的投资组合优化"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            max_workers=max_workers, method=method,
            risk_free_rate=risk_free_rate, target_return=target_return
        )
        return self._request('/xg_stock_cov_portfolio', params)

    # ============================================================
    # 九、股票组合分析接口
    # ============================================================
    
    def xg_stock_analysis(
        self,
        start_date: str = '20240101',
        end_date: str = '20261231',
        stock_list: str = '159915.SZ,518880.SH,510300.SH',
        stock_weight: str = '0.4,0.3,0.3',
        index_stock: str = '000300.SH',
        max_workers: int = 4,
        risk_free_rate: float = 0.03
    ) -> Dict[str, Any]:
        """小果股票分析系统 - 组合收益分析"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            stock_weight=stock_weight, index_stock=index_stock,
            max_workers=max_workers, risk_free_rate=risk_free_rate
        )
        return self._request('/xg_stock_analysis', params)

    # ============================================================
    # 十、用户认证接口
    # ============================================================
    
    def get_user_info(
        self,
        user: str = '小果'
    ) -> Dict[str, Any]:
        """获取用户信息"""
        params = self._get_params(user=user)
        return self._request('/get_user_info', params)
    
    def check_password_is_av_user(
        self,
        user: str = '小果'
    ) -> Dict[str, Any]:
        """检查授权码有效性"""
        params = self._get_params(user=user)
        return self._request('/check_password_is_av_user', params)

    # ============================================================
    # 十一、数据查询接口（AKShare/数据库API）
    # ============================================================
    
    def get_wencai_data(
        self,
        query: str = '今日涨停'
    ) -> Dict[str, Any]:
        """获取问财数据"""
        params = self._get_params(query=query)
        return self._request('/get_wencai_data', params)
    
    def get_user_def_data(
        self,
        name: str = 'df',
        func: str = '''
import akshare as ak
df = ak.stock_info_a_code_name()
print(df)
'''
    ) -> Dict[str, Any]:
        """获取自定义数据"""
        params = self._get_params(name=name, func=func)
        return self._request('/get_user_def_data', params)
    
    def get_user_base_data(
        self,
        file_path: str = '/xg_data/全市场股票/',
        file_name: str = '全市场股票'
    ) -> Dict[str, Any]:
        """获取数据库的数据"""
        params = self._get_params(file_path=file_path, file_name=file_name)
        return self._request('/get_user_base_data', params)

    # ============================================================
    # 十二、Tick/分钟数据接口
    # ============================================================
    
    
    
    def get_mini_data_5(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '5',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取5分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_5', params)
    
    def get_mini_data_15(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '15',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取15分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_15', params)
    
    def get_mini_data_30(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '30',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取30分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_30', params)
    
    def get_mini_data_60(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '60',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取60分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_60', params)

    # ============================================================
    # 十三、K线数据接口
    # ============================================================
    
    def query_history_k_data_plus_d(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'd',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """日线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/query_history_k_data_plus_d', params)
    
    def query_history_k_data_plus_w(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'w',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """周线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/query_history_k_data_plus_w', params)
    
    def query_history_k_data_plus_m(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'm',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """月线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/query_history_k_data_plus_m', params)

    # ============================================================
    # 十四、指数K线数据接口
    # ============================================================
    
    def query_history_k_data_plus_index_d(
        self,
        stock: str = 'sh.000001',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'd'
    ) -> Dict[str, Any]:
        """指数日线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        return self._request('/query_history_k_data_plus_index_d', params)
    
    def query_history_k_data_plus_index_w(
        self,
        stock: str = 'sh.000001',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'w'
    ) -> Dict[str, Any]:
        """指数周线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        return self._request('/query_history_k_data_plus_index_w', params)
    
    def query_history_k_data_plus_index_m(
        self,
        stock: str = 'sh.000001',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'm'
    ) -> Dict[str, Any]:
        """指数月线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        return self._request('/query_history_k_data_plus_index_m', params)

    # ============================================================
    # 十五、财务数据接口
    # ============================================================
    
    def query_profit_data(
        self,
        code: str = 'sh.600031',
        year: str = '2025',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """盈利能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_profit_data', params)
    
    def query_operation_data(
        self,
        code: str = 'sh.600031',
        year: str = '2025',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """营运能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_operation_data', params)
    
    def query_growth_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频成长能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_growth_data', params)
    
    def query_balance_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频偿债能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_balance_data', params)
    
    def query_cash_flow_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频现金流量"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_cash_flow_data', params)
    
    def query_dupont_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频杜邦指数"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_dupont_data', params)

    # ============================================================
    # 五、系统接口
    # ============================================================
    
    def root(self) -> Dict[str, Any]:
        """根路径"""
        return self._request('/', {})
    
    def health(self) -> Dict[str, Any]:
        """健康检查"""
        return self._request('/health', {})


# ============================================================
# 测试代码
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 小果量化数据API测试")
    print("=" * 60)
    
    # 初始化客户端（使用您提供的服务器地址）
    client = xg_quant_backtrader_data(
        url="数据库服务器",
        port=数据库端口,
        user="自己名称",
        password="自己密码",
        auth_code="自己的token"
    )
    
    print("\n" + "=" * 60)
    print("📋 一、系统接口测试")
    print("=" * 60)
    #因子数据
    df=client.get_stock_factor_data(columns='date,证券代码,5日涨跌幅')
    df=client._to_dataframe(df)
    print(df)
    #股票数据
    df=client.get_stock_hist_data()
    df=client._to_dataframe(df)
    print(df)
    #财务数据
    df=client.get_stock_finance_data()
    df=client._to_dataframe(df)
    print(df)

```
# 全部的因子
{
    "5日涨跌幅": "cacal_zdf(n=5)",
    "10日涨跌幅": "cacal_zdf(n=10)",
    "20日涨跌幅": "cacal_zdf(n=20)",
    "30日涨跌幅": "cacal_zdf(n=30)",
    "60日涨跌幅": "cacal_zdf(n=60)",
    "120日涨跌幅": "cacal_zdf(n=120)",
    "六脉神剑":"six_pulse_excalibur_hist()",
    "小波段交易":"small_fruit_band_trading_1()",
    "大波段交易":"small_fruit_band_trading_2()",
    "波段超级买卖":"band_supe_buy_sell()",
    "价格距离5日均线涨跌幅":"cacal_price_line_zdf(n=5)",
    "价格距离10日均线涨跌幅":"cacal_price_line_zdf(n=10)",
    "价格距离20日均线涨跌幅":"cacal_price_line_zdf(n=20)",
    "价格距离30日均线涨跌幅":"cacal_price_line_zdf(n=30)",
    "价格距离60日均线涨跌幅":"cacal_price_line_zdf(n=60)",
    "价格距离120日均线涨跌幅":"cacal_price_line_zdf(n=120)",
    "5日均线距离10日均线涨跌幅":"cacal_line_line_zdf(n1=5,n2=10)",
    "10日均线距离20日均线涨跌幅":"cacal_line_line_zdf(n1=10,n2=20)",
    "20日均线距离30日均线涨跌幅":"cacal_line_line_zdf(n1=20,n2=30)",
    "30日均线距离60日均线涨跌幅":"cacal_line_line_zdf(n1=30,n2=60)",
    "60日均线距离120日均线涨跌幅":"cacal_line_line_zdf(n1=60,n2=120)",
    "5日偏度":"cacal_skew(n=5)",
    "10日偏度":"cacal_skew(n=10)",
    "20日偏度":"cacal_skew(n=20)",
    "30日偏度":"cacal_skew(n=30)",
    "60日偏度":"cacal_skew(n=60)",
    "120日偏度":"cacal_skew(n=120)",
    "5日峰度":"cacal_kurt(n=5)",
    "10日峰度":"cacal_kurt(n=10)",
    "20日峰度":"cacal_kurt(n=20)",
    "30日峰度":"cacal_kurt(n=30)",
    "60日峰度":"cacal_kurt(n=60)",
    "120日峰度":"cacal_kurt(n=120)",
    "KDJ_KD金叉": "KDJ_KD金叉()",
    "KDJ_KD死叉": "KDJ_KD死叉()",
    "RSI_金叉": "RSI_金叉()",
    "RSI_死叉": "RSI_死叉()",
    "WR_金叉": "WR_金叉()",
    "MACD_金叉": "MACD_金叉()",
    "MACD_死叉": "MACD_死叉()",
    "PSY_金叉": "PSY_金叉()",
    "PSY_死叉": "PSY_死叉()",
    "5日均线": "SMA(period=5)",
    "10日均线": "SMA(period=10)",
    "20日均线": "SMA(period=20)",
    "30日均线": "SMA(period=30)",
    "60日均线": "SMA(period=60)",
    "120日均线": "SMA(period=120)",
    "5日10日金叉": "CROSS_UP(n1=5,n2=10)",
    "10日20日金叉": "CROSS_UP(n1=10,n2=20)",
    "20日30日金叉": "CROSS_UP(n1=20,n2=30)",
    "30日60日金叉": "CROSS_UP(n1=30,n2=60)",
    "60日120日金叉": "CROSS_UP(n1=60,n2=120)",
    "5日10日死叉": "CROSS_DOWN(n1=10,n2=5)",
    "10日20日死叉": "CROSS_DOWN(n1=20,n2=10)",
    "20日30日死叉": "CROSS_DOWN(n1=30,n2=20)",
    "30日60日死叉": "CROSS_DOWN(n1=60,n2=30)",
    "60日120日死叉": "CROSS_DOWN(n1=120,n2=60)",
    "连续上涨天数": "BARSLASTCOUNT_UP()",
    "连续下跌天数": "BARSLASTCOUNT_DOWN()",
    "价格在5均线上": "PRICE_MA_LINE_ANAL(n=5)",
    "价格在10均线上": "PRICE_MA_LINE_ANAL(n=10)",
    "价格在20均线上": "PRICE_MA_LINE_ANAL(n=20)",
    "价格在30均线上": "PRICE_MA_LINE_ANAL(n=30)",
    "价格在60均线上": "PRICE_MA_LINE_ANAL(n=60)",
    "价格在120均线上": "PRICE_MA_LINE_ANAL(n=120)",
    "5均线在10均线上": "MA_LINE_ANAL(n1=5,n2=10)",
    "10均线在20均线上": "MA_LINE_ANAL(n1=10,n2=20)",
    "20均线在30均线上": "MA_LINE_ANAL(n1=20,n2=30)",
    "30均线在60均线上": "MA_LINE_ANAL(n1=30,n2=60)",
    "60均线在120均线上": "MA_LINE_ANAL(n1=60,n2=120)",
    "5日Alpha": "roll_alpha(n=5)",
    "10日Alpha": "roll_alpha(n=10)",
    "20日Alpha": "roll_alpha(n=20)",
    "30日Alpha": "roll_alpha(n=30)",
    "60日Alpha": "roll_alpha(n=60)",
    "120日Alpha": "roll_alpha(n=120)",
    "5日Beta": "roll_beta(n=5)",
    "10日Beta": "roll_beta(n=10)",
    "20日Beta": "roll_beta(n=20)",
    "30日Beta": "roll_beta(n=30)",
    "60日Beta": "roll_beta(n=60)",
    "120日Beta": "roll_beta(n=120)",
    "5日夏普比率": "roll_sharpe_ratio(n=5)",
    "10日夏普比率": "roll_sharpe_ratio(n=10)",
    "20日夏普比率": "roll_sharpe_ratio(n=20)",
    "30日夏普比率": "roll_sharpe_ratio(n=30)",
    "60日夏普比率": "roll_sharpe_ratio(n=60)",
    "120日夏普比率": "roll_sharpe_ratio(n=120)",
    "5日年化波动率": "roll_annual_volatility(n=5)",
    "10日年化波动率": "roll_annual_volatility(n=10)",
    "20日年化波动率": "roll_annual_volatility(n=20)",
    "30日年化波动率": "roll_annual_volatility(n=30)",
    "60日年化波动率": "roll_annual_volatility(n=60)",
    "120日年化波动率": "roll_annual_volatility(n=120)",
    "5日最大回撤": "roll_max_drawdown(n=5)",
    "10日最大回撤": "roll_max_drawdown(n=10)",
    "20日最大回撤": "roll_max_drawdown(n=20)",
    "30日最大回撤": "roll_max_drawdown(n=30)",
    "60日最大回撤": "roll_max_drawdown(n=60)",
    "120日最大回撤": "roll_max_drawdown(n=120)",
    "5日上涨捕获率": "roll_up_capture(n=5)",
    "10日上涨捕获率": "roll_up_capture(n=10)",
    "20日上涨捕获率": "roll_up_capture(n=20)",
    "30日上涨捕获率": "roll_up_capture(n=30)",
    "60日上涨捕获率": "roll_up_capture(n=60)",
    "120日上涨捕获率": "roll_up_capture(n=120)",
    "5日下跌捕获率": "roll_down_capture(n=5)",
    "10日下跌捕获率": "roll_down_capture(n=10)",
    "20日下跌捕获率": "roll_down_capture(n=20)",
    "30日下跌捕获率": "roll_down_capture(n=30)",
    "60日下跌捕获率": "roll_down_capture(n=60)",
    "120日下跌捕获率": "roll_down_capture(n=120)",
    "3日回归动量": "calculate_momentum_score(n=3)",
    "5日回归动量": "calculate_momentum_score(n=5)",
    "7日回归动量": "calculate_momentum_score(n=7)",
    "9日回归动量": "calculate_momentum_score(n=9)",
    "12日回归动量": "calculate_momentum_score(n=12)",
    "15日回归动量": "calculate_momentum_score(n=15)",
    "18日回归动量": "calculate_momentum_score(n=18)",
    "20日回归动量": "calculate_momentum_score(n=20)",
    "23日回归动量": "calculate_momentum_score(n=23)",
    "25日回归动量": "calculate_momentum_score(n=25)",
    "28日回归动量": "calculate_momentum_score(n=28)",
    "30日回归动量": "calculate_momentum_score(n=30)",
    "35日回归动量": "calculate_momentum_score(n=35)",
    "40日回归动量": "calculate_momentum_score(n=40)",
    "45日回归动量": "calculate_momentum_score(n=45)",
    "50日回归动量": "calculate_momentum_score(n=50)",
    "60日回归动量": "calculate_momentum_score(n=60)",
    "5日最高值到当前周期": "HHVBARS(n=5)",
    "10日最高值到当前周期": "HHVBARS(n=10)",
    "20日最高值到当前周期": "HHVBARS(n=20)",
    "30日最高值到当前周期": "HHVBARS(n=30)",
    "60日最高值到当前周期": "HHVBARS(n=60)",
    "120日最高值到当前周期": "HHVBARS(n=120)",
    "5日最低值到当前周期": "LLVBARS(n=5)",
    "10日最低值到当前周期": "LLVBARS(n=10)",
    "20日最低值到当前周期": "LLVBARS(n=20)",
    "30日最低值到当前周期": "LLVBARS(n=30)",
    "60日最低值到当前周期": "LLVBARS(n=60)",
    "120日最低值到当前周期": "LLVBARS(n=120)",
    "5日回归斜率": "SLOPE(n=5)",
    "10日回归斜率": "SLOPE(n=10)",
    "20日回归斜率": "SLOPE(n=20)",
    "30日回归斜率": "SLOPE(n=30)",
    "60日回归斜率": "SLOPE(n=60)",
    "120日回归斜率": "SLOPE(n=120)",
    "5日标准差": "STD(n=5)",
    "10日标准差": "STD(n=10)",
    "20日标准差": "STD(n=20)",
    "30日标准差": "STD(n=30)",
    "60日标准差": "STD(n=60)",
    "120日标准差": "STD(n=120)",
    "CCI商品路径指标": "CCI()",
    "MFI最近流量指标": "MFI()",
    "MTM动量线_MTM值": "MTM_MTM()",
    "MTM动量线_MTMMA值": "MTM_MTMMA()",
    "RSI相对强弱_RSI1": "RSI1()",
    "RSI相对强弱_RSI2": "RSI2()",
    "RSI相对强弱_RSI3": "RSI3()",
    "KDJ指标_K值": "KDJ_K()",
    "KDJ指标_D值": "KDJ_D()",
    "KDJ指标_J值": "KDJ_J()",
    "SKDJ慢速随机_K值": "SKDJ_K()",
    "SKDJ慢速随机_D值": "SKDJ_D()",
    "UDL引力线_UDL值": "UDL_UDL()",
    "UDL引力线_MAUDL值": "UDL_MAUDL()",
    "WR威廉指标_WR1": "WR1()",
    "WR威廉指标_WR2": "WR2()",
    "LWR指标_LWR1": "LWR1()",
    "LWR指标_LWR2": "LWR2()",
    "MARSI相对强弱平均线_RSI1": "MARSI1()",
    "MARSI相对强弱平均线_RSI2": "MARSI2()",
    "BIAS乖离率_BIAS1": "BIAS1()",
    "BIAS乖离率_BIAS2": "BIAS2()",
    "BIAS乖离率_BIAS3": "BIAS3()",
    "BIAS_QL乖离率传统版_BIAS值": "BIAS_QL_BIAS()",
    "BIAS_QL乖离率传统版_BIASMA值": "BIAS_QL_BIASMA()",
    "BIAS36三六乖离_BIAS36": "BIAS36_BIAS36()",
    "BIAS36三六乖离_BIAS612": "BIAS36_BIAS612()",
    "BIAS36三六乖离_MABIAS": "BIAS36_MABIAS()",
    "ACCER幅度涨速": "ACCER()",
    "ASI振动升降指标_ASI": "ASI_ASI()",
    "ASI振动升降指标_ASIT": "ASI_ASIT()",
    "CHO佳庆指标_CHO": "CHO_CHO()",
    "CHO佳庆指标_MACHO": "CHO_MACHO()",
    "DMA_XT平均差_DIF": "DMA_XT_DIF()",
    "DMA_XT平均差_DIFMA": "DMA_XT_DIFMA()",
    "DMI趋向指标_PDI": "DMI_PDI()",
    "DMI趋向指标_MDI": "DMI_MDI()",
    "DMI趋向指标_ADX": "DMI_ADX()",
    "DMI趋向指标_ADXR": "DMI_ADXR()",
    "DPO区间震荡线_DPO": "DPO_DPO()",
    "DPO区间震荡线_MADPO": "DPO_MADPO()",
    "EMV简易波动指标_EMV": "EMV_EMV()",
    "EMV简易波动指标_MAEMV": "EMV_MAEMV()",
    "MACD平滑异同平均线_DIF": "MACD_DIF()",
    "MACD平滑异同平均线_DEA": "MACD_DEA()",
    "MACD平滑异同平均线_MACD": "MACD_MACD()",
    "VMACD量平滑异同平均线_DIF": "VMACD_DIF()",
    "VMACD量平滑异同平均线_DEA": "VMACD_DEA()",
    "VMACD量平滑异同平均线_MACD": "VMACD_MACD()",
    "SMACD单线平滑异同平均线_DEA": "SMACD_DEA()",
    "SMACD单线平滑异同平均线_MACD": "SMACD_MACD()",
    "QACD快速异同平均线_DIF": "QACD_DIF()",
    "QACD快速异同平均线_MACD": "QACD_MACD()",
    "QACD快速异同平均线_DDIF": "QACD_DDIF()",
    "TRIX三重指数平均线_TRIX": "TRIX_TRIX()",
    "TRIX三重指数平均线_MATRIX": "TRIX_MATRIX()",
    "UOS终极指标_UOS": "UOS_UOS()",
    "UOS终极指标_MAUOS": "UOS_MAUOS()",
    "VTP量价曲线_VPT": "VTP_VPT()",
    "VTP量价曲线_MAVP": "VTP_MAVP()",
    "WVAD威廉变异离散量_WVAD": "WVAD_WVAD()",
    "WVAD威廉变异离散量_MAWVAD": "WVAD_MAWVAD()",
    "JS加数线_JS": "JS_JS()",
    "JS加数线_MAJS1": "JS_MAJS1()",
    "JS加数线_MAJS2": "JS_MAJS2()",
    "JS加数线_MAJS3": "JS_MAJS3()",
    "CYE市场趋势_CYEL": "CYE_CYEL()",
    "CYE市场趋势_CYES": "CYE_CYES()",
    "GDX轨道线_轨道": "GDX_轨道()",
    "GDX轨道线_压力线": "GDX_压力线()",
    "GDX轨道线_支撑线": "GDX_支撑线()",
    "JLHB绝路航标_B": "JLHB_B()",
    "JLHB绝路航标_VAR2": "JLHB_VAR2()",
    "JLHB绝路航标_绝路航标": "JLHB_绝路航标()",
    "BRAR情绪指标_BR": "BRAR_BR()",
    "BRAR情绪指标_AR": "BRAR_AR()",
    "CR带状能量线_CR": "CR_CR()",
    "CR带状能量线_MA1": "CR_MA1()",
    "CR带状能量线_MA2": "CR_MA2()",
    "CR带状能量线_MA3": "CR_MA3()",
    "CR带状能量线_MA4": "CR_MA4()",
    "MASS梅斯线_MASS": "MASS_MASS()",
    "MASS梅斯线_MAMASS": "MASS_MAMASS()",
    "PSY心理线_PSY": "PSY_PSY()",
    "PSY心理线_PSYMA": "PSY_PSYMA()",
    "VR成交量变异率_VR": "VR_VR()",
    "VR成交量变异率_MAVR": "VR_MAVR()",
    "WAD威廉多空力度线_WAD": "WAD_WAD()",
    "WAD威廉多空力度线_MAWAD": "WAD_MAWAD()",
    "PCNT幅度比_PCNT": "PCNT_PCNT()",
    "PCNT幅度比_MAPCNT": "PCNT_MAPCNT()",
    "CYR市场强弱_CYR": "CYR_CYR()",
    "CYR市场强弱_MACYR": "CYR_MACYR()",
    "AMO成交金额_AMOW": "AMO_AMOW()",
    "AMO成交金额_AMO1": "AMO_AMO1()",
    "AMO成交金额_AMO2": "AMO_AMO2()",
    "OBV累积能量线_OBV": "OBV_OBV()",
    "OBV累积能量线_MAOBV": "OBV_MAOBV()",
    "VOL成交量_MAVOL1": "VOL_XT_MAVOL1()",
    "VOL成交量_MAVOL2": "VOL_XT_MAVOL2()",
    "VRSI相对强弱量_RSI1": "VRSI1()",
    "VRSI相对强弱量_RSI2": "VRSI2()",
    "VRSI相对强弱量_RSI3": "VRSI3()",
    "HSL换手线_HSL": "HSL_HSL()",
    "HSL换手线_MAHSL": "HSL_MAHSL()",
    "MA均线_MA1": "MA_XT_MA1()",
    "MA均线_MA2": "MA_XT_MA2()",
    "MA均线_MA3": "MA_XT_MA3()",
    "MA均线_MA4": "MA_XT_MA4()",
    "ACD升降线_ACD": "ACD_ACD()",
    "ACD升降线_MAACD": "ACD_MAACD()",
    "BBI多空均线": "BBI()",
    "EXPMA指数平均线_EXP1": "EXPMA_EXP1()",
    "EXPMA指数平均线_EXP2": "EXPMA_EXP2()",
    "HMA高价平均线_HMA1": "HMA_HMA1()",
    "HMA高价平均线_HMA2": "HMA_HMA2()",
    "HMA高价平均线_HMA3": "HMA_HMA3()",
    "HMA高价平均线_HMA4": "HMA_HMA4()",
    "HMA高价平均线_HMA5": "HMA_HMA5()",
    "LMA低价平均线_LMA1": "LMA_LMA1()",
    "LMA低价平均线_LMA2": "LMA_LMA2()",
    "LMA低价平均线_LMA3": "LMA_LMA3()",
    "LMA低价平均线_LMA4": "LMA_LMA4()",
    "LMA低价平均线_LMA5": "LMA_LMA5()",
    "VMA变异平均线_VMA1": "VMA_VMA1()",
    "VMA变异平均线_VMA2": "VMA_VMA2()",
    "VMA变异平均线_VMA3": "VMA_VMA3()",
    "VMA变异平均线_VMA4": "VMA_VMA4()",
    "VMA变异平均线_VMA5": "VMA_VMA5()",
    "AMV成本均线_AMV1": "AMV_AMV1()",
    "AMV成本均线_AMV2": "AMV_AMV2()",
    "AMV成本均线_AMV3": "AMV_AMV3()",
    "AMV成本均线_AMV4": "AMV_AMV4()",
    "BBIBOLL多空布林线_BBIBOLL": "BBIBOLL_BBIBOLL()",
    "BBIBOLL多空布林线_UPR": "BBIBOLL_UPR()",
    "BBIBOLL多空布林线_DWN": "BBIBOLL_DWN()",
    "ALLIGAT鳄鱼线_上唇": "ALLIGAT_上唇()",
    "ALLIGAT鳄鱼线_牙齿": "ALLIGAT_牙齿()",
    "ALLIGAT鳄鱼线_下颚": "ALLIGAT_下颚()",
    "GMMA顾比均线_MA3": "GMMA_MA3()",
    "GMMA顾比均线_MA5": "GMMA_MA5()",
    "GMMA顾比均线_MA8": "GMMA_MA8()",
    "GMMA顾比均线_MA10": "GMMA_MA10()",
    "GMMA顾比均线_MA12": "GMMA_MA12()",
    "GMMA顾比均线_MA15": "GMMA_MA15()",
    "GMMA顾比均线_MA30": "GMMA_MA30()",
    "GMMA顾比均线_MA35": "GMMA_MA35()",
    "GMMA顾比均线_MA40": "GMMA_MA40()",
    "GMMA顾比均线_MA45": "GMMA_MA45()",
    "GMMA顾比均线_MA50": "GMMA_MA50()",
    "GMMA顾比均线_MA60": "GMMA_MA60()",
    "BOLL布林线_BOLL": "BOLL_BOLL()",
    "BOLL布林线_UB": "BOLL_UB()",
    "BOLL布林线_LB": "BOLL_LB()",
    "PBX瀑布线_PBX1": "PBX_PBX1()",
    "PBX瀑布线_PBX2": "PBX_PBX2()",
    "PBX瀑布线_PBX3": "PBX_PBX3()",
    "PBX瀑布线_PBX4": "PBX_PBX4()",
    "PBX瀑布线_PBX5": "PBX_PBX5()",
    "PBX瀑布线_PBX6": "PBX_PBX6()",
    "ENE轨道线_UPPER": "ENE_UPPER()",
    "ENE轨道线_LOWER": "ENE_LOWER()",
    "ENE轨道线_ENE": "ENE_ENE()",
    "MIKE麦克支撑压力_STOR": "MIKE_STOR()",
    "MIKE麦克支撑压力_MIDR": "MIKE_MIDR()",
    "MIKE麦克支撑压力_WEKR": "MIKE_WEKR()",
    "MIKE麦克支撑压力_WEKS": "MIKE_WEKS()",
    "MIKE麦克支撑压力_MIDS": "MIKE_MIDS()",
    "MIKE麦克支撑压力_STOS": "MIKE_STOS()",
    "XS薛斯通道_SUP": "XS_SUP()",
    "XS薛斯通道_SDN": "XS_SDN()",
    "XS薛斯通道_LUP": "XS_LUP()",
    "XS薛斯通道_LDN": "XS_LDN()",
    "TQN唐奇安通道_周期高点": "TQN_周期高点()",
    "TQN唐奇安通道_周期低点": "TQN_周期低点()",
    "TQN唐奇安通道_平空开多": "TQN_平空开多()",
    "TQN唐奇安通道_平多开空": "TQN_平多开空()",
    "SAR抛物线指标": "SAR()",
    "MA交易_MA1": "MA_交易_MA1()",
    "MA交易_MA2": "MA_交易_MA2()",
    "MA交易_平空开多": "MA_交易_平空开多()",
    "MA交易_平多开空": "MA_交易_平多开空()",
    "MACD交易_DIFF": "MACD_交易_DIFF()",
    "MACD交易_DEA": "MACD_交易_DEA()",
    "MACD交易_MACD": "MACD_交易_MACD()",
    "MACD交易_平空开多": "MACD_交易_平空开多()",
    "MACD交易_平多开空": "MACD_交易_平多开空()",
    "KDJ交易_K": "KDJ_交易_K()",
    "KDJ交易_D": "KDJ_交易_D()",
    "KDJ交易_J": "KDJ_交易_J()",
    "KDJ交易_平空开多": "KDJ_交易_平空开多()",
    "KDJ交易_平多开空": "KDJ_交易_平多开空()",
    "SG_XDT心电图_QR": "SG_XDT_QR()",
    "SG_XDT心电图_MQR1": "SG_XDT_MQR1()",
    "SG_XDT心电图_MQR2": "SG_XDT_MQR2()",
    "SG_NDB脑电波_DK": "SG_NDB_DK()",
    "SG_NDB脑电波_MDK1": "SG_NDB_MDK1()",
    "SG_NDB脑电波_MDK2": "SG_NDB_MDK2()",
    "SG_SMX生命线_ZY1": "SG_SMX_ZY1()",
    "SG_SMX生命线_ZY2": "SG_SMX_ZY2()",
    "SG_SMX生命线_ZY3": "SG_SMX_ZY3()",
    "SG_LB量比_量比": "SG_LB_量比()",
    "SG_LB量比_MA5": "SG_LB_MA5()",
    "SG_LB量比_MA10": "SG_LB_MA10()",
    "SG_PF强势股评分": "SG_PF()",
    "RAD威力雷达_RADER1": "RAD_RADER1()",
    "RAD威力雷达_RADERMA": "RAD_RADERMA()",
    "LON龙系长线_LON": "LON_LON()",
    "LON龙系长线_LONMA": "LON_LONMA()",
    "LON龙系长线_LONT": "LON_LONT()",
    "SHT龙系短线_SHT": "SHT_SHT()",
    "SHT龙系短线_SHTMA": "SHT_SHTMA()",
    "ZLJC主力进出_JCS": "ZLJC_JCS()",
    "ZLJC主力进出_JCM": "ZLJC_JCM()",
    "ZLJC主力进出_JCL": "ZLJC_JCL()",
    "ZLMM主力买卖_MMS": "ZLMM_MMS()",
    "ZLMM主力买卖_MMM": "ZLMM_MMM()",
    "ZLMM主力买卖_MML": "ZLMM_MML()",
    "SLZT神龙在天_白龙": "SLZT_白龙()",
    "SLZT神龙在天_黄龙": "SLZT_黄龙()",
    "SLZT神龙在天_紫龙": "SLZT_紫龙()",
    "SLZT神龙在天_青龙": "SLZT_青龙()",
    "SLZT神龙在天_红龙": "SLZT_红龙()",
    "SLZT神龙在天_蓝龙": "SLZT_蓝龙()",
    "ADVOL龙系离散量_ADVOL": "ADVOL_ADVOL()",
    "ADVOL龙系离散量_MA1": "ADVOL_MA1()",
    "ADVOL龙系离散量_MA2": "ADVOL_MA2()",
    "CYS市场盈亏": "CYS()",
    "CYW主力控盘": "CYW()",
    "JAX济安线_J": "JAX_J()",
    "JAX济安线_A": "JAX_A()",
    "JAX济安线_X": "JAX_X()",
    "XJDX超级短线_J": "XJDX_J()",
    "XJDX超级短线_D": "XJDX_D()",
    "XJDX超级短线_K": "XJDX_K()",
    "ZJTJ庄家抬轿_无庄控盘": "ZJTJ_无庄控盘()",
    "ZJTJ庄家抬轿_开始控盘": "ZJTJ_开始控盘()",
    "ZJTJ庄家抬轿_有庄控盘": "ZJTJ_有庄控盘()",
    "ZJTJ庄家抬轿_主力出货": "ZJTJ_主力出货()",
    "BDZX波段之星_AK": "BDZX_AK()",
    "BDZX波段之星_AD1": "BDZX_AD1()",
    "BDZX波段之星_AJ": "BDZX_AJ()",
    "BDZX波段之星_买进": "BDZX_买进()",
    "BDZX波段之星_卖出": "BDZX_卖出()",
    "LHXJ猎狐先觉_主力弃盘": "LHXJ_主力弃盘()",
    "LHXJ猎狐先觉_主力控盘": "LHXJ_主力控盘()",
    "LYJH猎鹰歼狐_机构做空能量线": "LYJH_机构做空能量线()",
    "LYJH猎鹰歼狐_机构做多能量线": "LYJH_机构做多能量线()",
    "JFZX飓风智能中线_多头力量": "JFZX_多头力量()",
    "JFZX飓风智能中线_空头力量": "JFZX_空头力量()",
    "CYHT财运亨通_SK": "CYHT_SK()",
    "CYHT财运亨通_SD": "CYHT_SD()",
    "CYHT财运亨通_卖出": "CYHT_卖出()",
    "CYHT财运亨通_买进": "CYHT_买进()",
    "BSQJ买卖区间_B买": "BSQJ_B买()",
    "BSQJ买卖区间_持仓": "BSQJ_持仓()",
    "BSQJ买卖区间_S卖": "BSQJ_S卖()",
    "BSQJ买卖区间_空仓": "BSQJ_空仓()",
    "CDP_STD逆势操作_CDP": "CDP_STD_CDP()",
    "CDP_STD逆势操作_AH": "CDP_STD_AH()",
    "CDP_STD逆势操作_NH": "CDP_STD_NH()",
    "CDP_STD逆势操作_NL": "CDP_STD_NL()",
    "CDP_STD逆势操作_AL": "CDP_STD_AL()",
    "Alpha001": "alpha001()",
    "Alpha002": "alpha002()",
    "Alpha003": "alpha003()",
    "Alpha004": "alpha004()",
    "Alpha005": "alpha005()",
    "Alpha006": "alpha006()",
    "Alpha007": "alpha007()",
    "Alpha008": "alpha008()",
    "Alpha009": "alpha009()",
    "Alpha010": "alpha010()",
    "Alpha011": "alpha011()",
    "Alpha012": "alpha012()",
    "Alpha013": "alpha013()",
    "Alpha014": "alpha014()",
    "Alpha015": "alpha015()",
    "Alpha016": "alpha016()",
    "Alpha017": "alpha017()",
    "Alpha018": "alpha018()",
    "Alpha019": "alpha019()",
    "Alpha020": "alpha020()",
    "Alpha021": "alpha021()",
    "Alpha022": "alpha022()",
    "Alpha023": "alpha023()",
    "Alpha024": "alpha024()",
    "Alpha025": "alpha025()",
    "Alpha026": "alpha026()",
    "Alpha027": "alpha027()",
    "Alpha028": "alpha028()",
    "Alpha029": "alpha029()",
    "Alpha030": "alpha030()",
    "Alpha031": "alpha031()",
    "Alpha032": "alpha032()",
    "Alpha033": "alpha033()",
    "Alpha034": "alpha034()",
    "Alpha035": "alpha035()",
    "Alpha036": "alpha036()",
    "Alpha037": "alpha037()",
    "Alpha038": "alpha038()",
    "Alpha039": "alpha039()",
    "Alpha040": "alpha040()",
    "Alpha041": "alpha041()",
    "Alpha042": "alpha042()",
    "Alpha043": "alpha043()",
    "Alpha044": "alpha044()",
    "Alpha045": "alpha045()",
    "Alpha046": "alpha046()",
    "Alpha047": "alpha047()",
    "Alpha048": "alpha048()",
    "Alpha049": "alpha049()",
    "Alpha050": "alpha050()",
    "Alpha051": "alpha051()",
    "Alpha052": "alpha052()",
    "Alpha053": "alpha053()",
    "Alpha054": "alpha054()",
    "Alpha055": "alpha055()",
    "Alpha056": "alpha056()",
    "Alpha057": "alpha057()",
    "Alpha058": "alpha058()",
    "Alpha059": "alpha059()",
    "Alpha060": "alpha060()",
    "Alpha061": "alpha061()",
    "Alpha062": "alpha062()",
    "Alpha063": "alpha063()",
    "Alpha064": "alpha064()",
    "Alpha065": "alpha065()",
    "Alpha066": "alpha066()",
    "Alpha067": "alpha067()",
    "Alpha068": "alpha068()",
    "Alpha069": "alpha069()",
    "Alpha070": "alpha070()",
    "Alpha071": "alpha071()",
    "Alpha072": "alpha072()",
    "Alpha073": "alpha073()",
    "Alpha074": "alpha074()",
    "Alpha075": "alpha075()",
    "Alpha076": "alpha076()",
    "Alpha077": "alpha077()",
    "Alpha078": "alpha078()",
    "Alpha079": "alpha079()",
    "Alpha080": "alpha080()",
    "Alpha081": "alpha081()",
    "Alpha082": "alpha082()",
    "Alpha083": "alpha083()",
    "Alpha084": "alpha084()",
    "Alpha085": "alpha085()",
    "Alpha086": "alpha086()",
    "Alpha087": "alpha087()",
    "Alpha088": "alpha088()",
    "Alpha089": "alpha089()",
    "Alpha090": "alpha090()",
    "Alpha091": "alpha091()",
    "Alpha092": "alpha092()",
    "Alpha093": "alpha093()",
    "Alpha094": "alpha094()",
    "Alpha095": "alpha095()",
    "Alpha096": "alpha096()",
    "Alpha097": "alpha097()",
    "Alpha098": "alpha098()",
    "Alpha099": "alpha099()",
    "Alpha100": "alpha100()",
    "Alpha101": "alpha101()",
    "Alpha102": "alpha102()",
    "Alpha103": "alpha103()",
    "Alpha104": "alpha104()",
    "Alpha105": "alpha105()",
    "Alpha106": "alpha106()",
    "Alpha107": "alpha107()",
    "Alpha108": "alpha108()",
    "Alpha109": "alpha109()",
    "Alpha110": "alpha110()",
    "Alpha111": "alpha111()",
    "Alpha112": "alpha112()",
    "Alpha113": "alpha113()",
    "Alpha114": "alpha114()",
    "Alpha115": "alpha115()",
    "Alpha116": "alpha116()",
    "Alpha117": "alpha117()",
    "Alpha118": "alpha118()",
    "Alpha119": "alpha119()",
    "Alpha120": "alpha120()",
    "Alpha121": "alpha121()",
    "Alpha122": "alpha122()",
    "Alpha123": "alpha123()",
    "Alpha124": "alpha124()",
    "Alpha125": "alpha125()",
    "Alpha126": "alpha126()",
    "Alpha127": "alpha127()",
    "Alpha128": "alpha128()",
    "Alpha129": "alpha129()",
    "Alpha130": "alpha130()",
    "Alpha131": "alpha131()",
    "Alpha132": "alpha132()",
    "Alpha133": "alpha133()",
    "Alpha134": "alpha134()",
    "Alpha135": "alpha135()",
    "Alpha136": "alpha136()",
    "Alpha137": "alpha137()",
    "Alpha138": "alpha138()",
    "Alpha139": "alpha139()",
    "Alpha140": "alpha140()",
    "Alpha141": "alpha141()",
    "Alpha142": "alpha142()",
    "Alpha143": "alpha143()",
    "Alpha144": "alpha144()",
    "Alpha145": "alpha145()",
    "Alpha146": "alpha146()",
    "Alpha147": "alpha147()",
    "Alpha148": "alpha148()",
    "Alpha149": "alpha149()",
    "Alpha150": "alpha150()",
    "Alpha151": "alpha151()",
    "Alpha152": "alpha152()",
    "Alpha153": "alpha153()",
    "Alpha154": "alpha154()",
    "Alpha155": "alpha155()",
    "Alpha156": "alpha156()",
    "Alpha157": "alpha157()",
    "Alpha158": "alpha158()",
    "Alpha159": "alpha159()",
    "Alpha160": "alpha160()",
    "Alpha161": "alpha161()",
    "Alpha162": "alpha162()",
    "Alpha163": "alpha163()",
    "Alpha164": "alpha164()",
    "Alpha165": "alpha165()",
    "Alpha166": "alpha166()",
    "Alpha167": "alpha167()",
    "Alpha168": "alpha168()",
    "Alpha169": "alpha169()",
    "Alpha170": "alpha170()",
    "Alpha171": "alpha171()",
    "Alpha172": "alpha172()",
    "Alpha173": "alpha173()",
    "Alpha174": "alpha174()",
    "Alpha175": "alpha175()",
    "Alpha176": "alpha176()",
    "Alpha177": "alpha177()",
    "Alpha178": "alpha178()",
    "Alpha179": "alpha179()",
    "Alpha180": "alpha180()",
    "Alpha181": "alpha181()",
    "Alpha182": "alpha182()",
    "Alpha183": "alpha183()",
    "Alpha184": "alpha184()",
    "Alpha185": "alpha185()",
    "Alpha186": "alpha186()",
    "Alpha187": "alpha187()",
    "Alpha188": "alpha188()",
    "Alpha189": "alpha189()",
    "Alpha190": "alpha190()",
    "Alpha191": "alpha191()"
}
#全部因子的计算公式
from xg_tdx_func.xg_tdx_func import *
import empyrical as ep
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from scipy import stats
import statsmodels.api as sm
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")

class xg_factor:
    '''
    小果因子库计算系统
    '''
    def __init__(self,
                df='',
                index_df='',):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.df = df.copy() if df is not None and not isinstance(df, str) and hasattr(df, 'copy') else df
        self.index_df = index_df.copy() if index_df is not None and not isinstance(index_df, str) and hasattr(index_df, 'copy') else index_df
        
        # 数据重命名（一次性完成）
        if isinstance(self.df, pd.DataFrame) and not self.df.empty:
            rename_dict = {
                "close": "closePrice",
                "open": "openPrice",
                "low": "lowestPrice",
                "high": "highestPrice",
                "volume": "turnoverVol",
                "amount": "turnoverValue"
            }
            # 只重命名存在的列
            self.df.rename(columns={k: v for k, v in rename_dict.items() if k in self.df.columns}, inplace=True)
            
            # 提取核心数据列（使用重命名后的列名）
            self.closePrice = self.df['closePrice'] if 'closePrice' in self.df.columns else pd.Series()
            self.openPrice = self.df['openPrice'] if 'openPrice' in self.df.columns else pd.Series()
            self.lowestPrice = self.df['lowestPrice'] if 'lowestPrice' in self.df.columns else pd.Series()
            self.highestPrice = self.df['highestPrice'] if 'highestPrice' in self.df.columns else pd.Series()
            self.turnoverVol = self.df['turnoverVol'] if 'turnoverVol' in self.df.columns else pd.Series()
            self.turnoverValue = self.df['turnoverValue'] if 'turnoverValue' in self.df.columns else pd.Series()
            
            # 统一简写命名（方便调用）
            self.C = self.closePrice
            self.H = self.highestPrice
            self.L = self.lowestPrice
            self.O = self.openPrice
            self.V = self.turnoverVol
            self.AMOUNT = self.turnoverValue
            
            # 保留原始简写（兼容旧代码）
            self.close = self.closePrice
            self.high = self.highestPrice
            self.low = self.lowestPrice
            self.open = self.openPrice
            self.volume = self.turnoverVol
            self.amount = self.turnoverValue
        else:
            # 空数据时的默认值
            self.closePrice = pd.Series()
            self.openPrice = pd.Series()
            self.lowestPrice = pd.Series()
            self.highestPrice = pd.Series()
            self.turnoverVol = pd.Series()
            self.turnoverValue = pd.Series()
            self.C = pd.Series()
            self.H = pd.Series()
            self.L = pd.Series()
            self.O = pd.Series()
            self.V = pd.Series()
            self.AMOUNT = pd.Series()
            self.close = pd.Series()
            self.high = pd.Series()
            self.low = pd.Series()
            self.open = pd.Series()
            self.volume = pd.Series()
            self.amount = pd.Series()

    # ========== 辅助函数 ==========
    def _sma(self, series, n, m):
        """SMA: 移动平均，alpha = m/n"""
        return series.ewm(adjust=False, alpha=m/n, min_periods=0, ignore_na=False).mean()
    
    def _tsrank(self, series, n):
        """TSRANK: 时间序列排名"""
        def rank_last(x):
            return stats.rankdata(x)[-1] / len(x) if len(x) > 0 else np.nan
        return series.rolling(window=n, min_periods=n).apply(rank_last)
    
    def _tsrank_fixed(self, series, n):
        """改进的TSRANK函数"""
        result = pd.Series(index=series.index, dtype=float)
        for i in range(len(series)):
            start = max(0, i - n + 1)
            window_data = series.iloc[start:i+1]
            valid_data = window_data.dropna()
            if len(valid_data) >= max(2, n // 2):
                current_val = series.iloc[i]
                rank = (valid_data < current_val).sum() + 1
                result.iloc[i] = rank / len(valid_data)
            else:
                result.iloc[i] = np.nan
        return result.fillna(method='ffill').fillna(method='bfill')
    
    def _decaylinear(self, series, n):
        """DECAYLINEAR: 线性衰减加权和"""
        w = np.arange(1, n + 1)
        return series.rolling(window=n, min_periods=n).apply(lambda x: np.dot(x, w))
    
    def _regbeta(self, y, x):
        """REGBETA: 回归beta"""
        y_vals = y.values
        x_vals = x.values if isinstance(x, pd.Series) else np.array(x)
        x_vals = sm.add_constant(x_vals)
        try:
            result = sm.OLS(y_vals, x_vals).fit()
            return result.params[1]
        except:
            return np.nan
    def six_pulse_excalibur_hist(self):
        '''
        六脉神剑
        '''
        
        markers=0
        signal=0
        #df=self.data.get_hist_data_em(stock=stock)
        CLOSE=self.C
        LOW=self.L
        HIGH=self.H
        DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
        DEA=EMA(DIFF,5)
        #如果满足DIFF>DEA 在1的位置标记1的图标
        #DRAWICON(DIFF>DEA,1,1);
        markers+=IF(DIFF>DEA,1,0)
        #如果满足DIFF<DEA 在1的位置标记2的图标
        #DRAWICON(DIFF<DEA,1,2);
        markers+=IF(DIFF<DEA,1,0)
        #DRAWTEXT(ISLASTBAR=1,1,'. MACD'),COLORFFFFFF;{微信公众号:尊重市场}
        ABC1=DIFF>DEA
        signal+=IF(ABC1,1,0)
        尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
        K=SMA(尊重市场1,3,1)
        D=SMA(K,3,1)
        #如果满足k>d 在2的位置标记1的图标
        markers+=IF(K>D,1,0)
        #DRAWICON(K>D,2,1);
        markers+=IF(K<D,1,0)
        #DRAWICON(K<D,2,2);
        #DRAWTEXT(ISLASTBAR=1,2,'. KDJ'),COLORFFFFFF;
        ABC2=K>D
        signal+=IF(ABC2,1,0)
        指标营地=REF(CLOSE,1)
        RSI1=(SMA(MAX(CLOSE-指标营地,0),5,1))/(SMA(ABS(CLOSE-指标营地),5,1))*100
        RSI2=(SMA(MAX(CLOSE-指标营地,0),13,1))/(SMA(ABS(CLOSE-指标营地),13,1))*100
        markers+=IF(RSI1>RSI2,1,0)
        #DRAWICON(RSI1>RSI2,3,1);
        markers+=IF(RSI1<RSI2,1,0)
        #DRAWICON(RSI1<RSI2,3,2);
        #DRAWTEXT(ISLASTBAR=1,3,'. RSI'),COLORFFFFFF;
        ABC3=RSI1>RSI2
        signal+=IF(ABC3,1,0)
        尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
        LWR1=SMA(尊重市场,3,1)
        LWR2=SMA(LWR1,3,1)
        #DRAWICON(LWR1>LWR2,4,1);
        markers+=IF(LWR1>LWR2,1,0)
        #DRAWICON(LWR1<LWR2,4,2);
        markers+=IF(LWR1<LWR2,1,0)
        #DRAWTEXT(ISLASTBAR=1,4,'. LWR'),COLORFFFFFF;
        ABC4=LWR1>LWR2
        signal+=IF(ABC4,1,0)
        BBI=(MA(CLOSE,3)+MA(CLOSE,5)+MA(CLOSE,8)+MA(CLOSE,13))/4
        #DRAWICON(CLOSE>BBI,5,1);
        markers+=IF(CLOSE>BBI,1,0)
        #DRAWICON(CLOSE<BBI,5,2);
        markers+=IF(CLOSE<BBI,1,0)
        #DRAWTEXT(ISLASTBAR=1,5,'. BBI'),COLORFFFFFF;
        ABC10=7
        ABC5=CLOSE>BBI
        signal+=IF(ABC5,1,0)
        MTM=CLOSE-REF(CLOSE,1)
        MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
        MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
        markers+=IF(MMS>MMM,1,0)
        #DRAWICON(MMS>MMM,6,1);
        markers+=IF(MMS<MMM,1,0)
        #DRAWICON(MMS<MMM,6,2);
        #DRAWTEXT(ISLASTBAR=1,6,'. ZLMM'),COLORFFFFFF;
        ABC6=MMS>MMM
        signal+=IF(ABC6,1,0)
        return signal
    def small_fruit_band_trading_1(self):
        '''
        小波段交易
        '''
        df=self.df
        CLOSE=self.C
        C=self.C
        LOW=self.L
        L=self.L
        HIGH=self.H
        H=self.H
        OPEN=self.O
        O=self.O
        volume=self.V
        V=self.V
        N1=7
        N2=5
        N3=3
        ABC1=(((HIGH + LOW)+(CLOSE*2)) / 4)
        ABC3=EMA(ABC1,N1)
        ABC4=STD(ABC1,N1)
        ABC5=((ABC1 - ABC3)*100) / ABC4
        ABC6=EMA(ABC5,N2)
        RK7=EMA(ABC6,N1)
        UP=(EMA(ABC6,10)+(100 / 2)) - 5
        DOWN=EMA(UP,N3)
        ACB1=EMA(DOWN,N3)
        ACB2=EMA(ACB1,N3)
        ACB3=EMA(ACB2,N3)
        ACB4=EMA(ACB3,N3)
        #STICKLINE(UP < REF(UP,1),UP,MA(UP,3),5,0),COLORBLUE;
        #STICKLINE(UP > REF(UP,1),UP,EMA(UP,3),5,0),COLORMAGENTA;
        df['柱子']=IF(UP > REF(UP,1),'红色','蓝色')
        df['买']=IF(AND(UP > REF(UP,1),REF(UP,1) < REF(UP,2)),'买',None)
        df['卖']=IF(AND(UP < REF(UP,1),REF(UP,1) > REF(UP,2)),'卖',None)
        #DRAWTEXT(UP > REF(UP,1)  AND  REF(UP,1) < REF(UP,2) ,UP,'买'),COLORRED;
        #DRAWTEXT(UP < REF(UP,1)  AND  REF(UP,1) > REF(UP,2) ,UP,'卖'),COLORGREEN;
        stats_list=[]
        for buy,sell in zip(df['买'].tolist(),df['卖'].tolist()):
            if buy=='买':
                stats_list.append(True)
            elif sell=='卖':
                stats_list.append(False)
            else:
                stats_list.append(None)
        df['stats']=stats_list
        df['stats']=df['stats'].fillna(method='ffill')
        return df['stats']
    def small_fruit_band_trading_2(self):
        '''
        大波段交易
        '''
        df=self.df
        CLOSE=self.C
        C=self.C
        LOW=self.L
        L=self.L
        HIGH=self.H
        H=self.H
        OPEN=self.O
        O=self.O
        volume=self.V
        V=self.V
        N1=18
        N2=15
        N3=12
        ABC1=(((HIGH + LOW)+(CLOSE*2)) / 4)
        ABC3=EMA(ABC1,N1)
        ABC4=STD(ABC1,N1)
        ABC5=((ABC1 - ABC3)*100) / ABC4
        ABC6=EMA(ABC5,N2)
        RK7=EMA(ABC6,N1)
        UP=(EMA(ABC6,10)+(100 / 2)) - 5
        DOWN=EMA(UP,N3)
        ACB1=EMA(DOWN,N3)
        ACB2=EMA(ACB1,N3)
        ACB3=EMA(ACB2,N3)
        ACB4=EMA(ACB3,N3)
        #STICKLINE(UP < REF(UP,1),UP,MA(UP,3),5,0),COLORBLUE;
        #STICKLINE(UP > REF(UP,1),UP,EMA(UP,3),5,0),COLORMAGENTA;
        df['柱子']=IF(UP > REF(UP,1),'红色','蓝色')
        df['买']=IF(AND(UP > REF(UP,1),REF(UP,1) < REF(UP,2)),'买',None)
        df['卖']=IF(AND(UP < REF(UP,1),REF(UP,1) > REF(UP,2)),'卖',None)
        #DRAWTEXT(UP > REF(UP,1)  AND  REF(UP,1) < REF(UP,2) ,UP,'买'),COLORRED;
        #DRAWTEXT(UP < REF(UP,1)  AND  REF(UP,1) > REF(UP,2) ,UP,'卖'),COLORGREEN;
        stats_list=[]
        for buy,sell in zip(df['买'].tolist(),df['卖'].tolist()):
            if buy=='买':
                stats_list.append(True)
            elif sell=='卖':
                stats_list.append(False)
            else:
                stats_list.append(None)
        df['stats']=stats_list
        df['stats']=df['stats'].fillna(method='ffill')
        return df['stats']
    def band_supe_buy_sell(self):
        '''
        波段超级买卖
        尊重市场1赋值:收盘价的6.5日[1日权重]移动平均
        尊重市场2赋值:收盘价的13.5日[1日权重]移动平均
        尊重市场11赋值:收盘价的3日[1日权重]移动平均
        尊重市场21赋值:收盘价的8日[1日权重]移动平均
        当满足条件尊重市场1>尊重市场2时,在尊重市场1和尊重市场2位置之间画柱状线,宽度为2.5,0不为0则画空心柱.,画红色,线宽为2
        当满足条件尊重市场2>尊重市场1时,在尊重市场1和尊重市场2位置之间画柱状线,宽度为2.5,0不为0则画空心柱.,画蓝色,线宽为2
        当满足条件尊重市场1上穿尊重市场2时,在最低价*0.98位置画5号图标
        当满足条件尊重市场21上穿尊重市场11时,在最高价*1.02位置书写文字,画黄色
        BBI赋值:(收盘价的3日简单移动平均+收盘价的6日简单移动平均+收盘价的12日简单移动平均+收盘价的24日简单移动平均)/4
        UPR赋值:BBI+3*BBI的13日估算标准差,线宽为2
        DWN赋值:BBI-3*BBI的13日估算标准差
        安全赋值:收盘价的60日简单移动平均,线宽为2
        LC赋值:1日前的收盘价
        RSI赋值:收盘价-LC和0的较大值的6日[1日权重]移动平均/收盘价-LC的绝对值的6日[1日权重]移动平均*100
        A7赋值:(2*收盘价+最高价+最低价)/4
        输出操作线:A7的5日简单移动平均,线宽为1
        操作线1赋值:A7的5日简单移动平均*1.03,线宽为2
        操作线2赋值:A7的5日简单移动平均*0.97,线宽为2
        输出ABC1:21日内A7的最低值
        输出ABC2:21日内A7的最高值
        SK赋值:(A7-ABC1)/(ABC2-ABC1)*100的7日指数移动平均
        SD赋值:0.667*1日前的SK+0.333*SK的5日指数移动平均
        当满足条件如果统计8日中满足收盘价<1日前的收盘价的天数/8>6/10ANDVOL>=1.5*成交量(手)的5日简单移动平均ANDCOUNT(SK>=SD,3)ANDREF(最低价,1)=120日内最低价的最低值,返回1,否则返回0时,在最低价*0.98位置画9号图标
        当满足条件如果统计13日中满足收盘价<1日前的收盘价的天数/13>6/10ANDCOUNT(SK>SD,6)ANDREF(最低价,5)=120日内最低价的最低值ANDREF(收盘价>=开盘价,4)ANDREF(收阳线,3)ANDREF(收阳线,2)ANDREF(开盘价>CLOS,返回?,否则返回?时,在,1)ANDOPEN>1日前的收盘价,1,0)位置书写文字 ,画黄色
        当满足条件如果统计13日中满足收盘价<1日前的收盘价的天数/13>6/10ANDCOUNT(SK>SD,6)ANDREF(最低价,5)=120日内最低价的最低值ANDREF(收盘价>=开盘价,4)ANDREF(收阳线,3)ANDREF(收阳线,2)ANDREF(开盘价>CLOS,返回?,否则返回?时,在,1)ANDOPEN>1日前的收盘价,1,0)位置画最低价*0.98号图标
        '''
        df=self.df
        CLOSE=self.C
        C=self.C
        LOW=self.L
        L=self.L
        HIGH=self.H
        H=self.H
        OPEN=self.O
        O=self.O
        volume=self.V
        V=self.V
        尊重市场1=SMA(C,6.5,1)
        尊重市场2=SMA(C,13.5,1)
        尊重市场11=SMA(C,3,1)
        尊重市场21=SMA(C,8,1)
        '''
        STICKLINE(尊重市场1>尊重市场2 , 尊重市场1,尊重市场2 ,2.5, 0),COLORRED,LINETHICK2;
        STICKLINE(尊重市场2>尊重市场1,尊重市场1,尊重市场2,2.5,0),COLORBLUE,LINETHICK2;
        '''
        df['柱子']=IF(尊重市场1>尊重市场2,'红色','蓝色')
        #DRAWICON( CROSS(尊重市场1,尊重市场2),L*0.98,5);
        df['笑脸']=CROSS(尊重市场1,尊重市场2)
        #DRAWTEXT(CROSS(尊重市场21,尊重市场11),H*1.02,''),COLORYELLOW;
        df['标记文字']=CROSS(尊重市场21,尊重市场11)
        BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
        UPR=BBI+3*STD(BBI,13)
        DWN=BBI-3*STD(BBI,13)
        安全=MA(CLOSE,60)
        LC=REF(CLOSE,1)
        RSI=SMA(MAX(CLOSE-LC,0),6,1)/SMA(ABS(CLOSE-LC),6,1)*100
        A7=(2*C+H+L)/4
        操作线=MA(A7,5)
        df['操作线']=操作线
        操作线1=MA(A7,5)*1.03
        df['操作线1']=操作线1
        操作线2=MA(A7,5)*0.97
        df['操作线2']=操作线2
        ABC1=LLV(A7,21)
        ABC2=HHV(A7,21)
        SK=EMA((A7-ABC1)/(ABC2-ABC1)*100,7)
        SD=EMA(0.667*REF(SK,1)+0.333*SK,5)
        '''
        DRAWICON(IF(COUNT(CLOSE<REF(CLOSE,1),8)/8>6/10 AND VOL>=1.5*MA(VOL,5) AND
        COUNT(SK>=SD,3) AND REF(LOW,1)=LLV(LOW,120),1,0),L*0.98,9);
        {DRAWTEXT(IF(COUNT(CLOSE<REF(CLOSE,1),8)/8>6/10 AND VOL>=1.5*MA(VOL,5) AND
        COUNT(SK>=SD,3) AND REF(LOW,1)=LLV(LOW,120),1,0),LOW*0.98,'底买') ,COLOR0099FF;}
        DRAWTEXT(IF(COUNT(CLOSE<REF(CLOSE,1),13)/13>6/10 AND
        COUNT(SK>SD,6) AND REF(LOW,5)=LLV(LOW,120) AND REF(CLOSE>=OPEN,4) AND
        REF(CLOSE>OPEN,3) AND REF(CLOSE>OPEN,2) AND REF(OPEN>CLOSE,1) AND
        OPEN>REF(CLOSE,1),1,0),LOW*0.98,'底买') ,COLORYELLOW;
        DRAWICON(IF(COUNT(CLOSE<REF(CLOSE,1),13)/13>6/10 AND
        COUNT(SK>SD,6) AND REF(LOW,5)=LLV(LOW,120) AND REF(CLOSE>=OPEN,4) AND
        REF(CLOSE>OPEN,3) AND REF(CLOSE>OPEN,2) AND REF(OPEN>CLOSE,1) AND
        OPEN>REF(CLOSE,1),1,0),L*0.98,9);
        '''
        趋势=CLOSE>=操作线
        df['趋势']=CLOSE>=操作线
        df['stats']=IF(AND(趋势,尊重市场1>尊重市场2),True,False)
        return df['stats']
    def KDJ_KD金叉(self):
        '''
        KDJ_KD金叉 的 Docstring
        '''
        K,D,J=KDJ(CLOSE=self.C,HIGH=self.H,LOW=self.L)
        result=CROSS(K,D)
        #result=IF(result==True,0,1)
        return result
    def KDJ_KD死叉(self):
        '''
        KDJ_KD金叉 的 Docstring
        '''
        K,D,J=KDJ(CLOSE=self.C,HIGH=self.H,LOW=self.L)
        result=CROSS(D,K)
        #result=IF(result==True,0,1)
        return result
    def RSI_金叉(self):
        '''
        RSI_金叉 的 Docstring
        '''
        RSI1,RSI2,RSI3=RSI(CLOSE=self.C)
        result=CROSS(RSI1,RSI2)
        #result=IF(result==True,0,1)
        return result
    def RSI_死叉(self):
        '''
        RSI_金叉 的 Docstring
        '''
        RSI1,RSI2,RSI3=RSI(CLOSE=self.C)
        result=CROSS(RSI2,RSI1)
        #result=IF(result==True,0,1)
        return result

    def WR_金叉(self):
        '''
        WR_金叉 的 Docstring
        '''
        WR1,WR2=WR(CLOSE=self.C,LOW=self.L,HIGH=self.H)
        result=CROSS(WR1,WR2)
        #result=IF(result==True,0,1)
        return result
    def WR_金叉(self):
        '''
        WR_金叉 的 Docstring
        '''
        WR1,WR2=WR(CLOSE=self.C,LOW=self.L,HIGH=self.H)
        result=CROSS(WR1,WR2)
        #result=IF(result==True,0,1)
        return result
    def MACD_金叉(self):
        '''
        MACD_金叉 的 Docstring
        '''
        DIF,DEA,MACD_1=MACD(CLOSE=self.C)
        result=CROSS(DIF,DEA)
        #result=IF(result==True,0,1)
        return result
    def MACD_死叉(self):
        '''
        MACD_金叉 的 Docstring
        '''
        DIF,DEA,MACD_1=MACD(CLOSE=self.C)
        result=CROSS(DEA,DIF)
        #result=IF(result==True,0,1)
        return result
    def PSY_金叉(self):
        '''
        PSY_金叉 的 Docstring
        '''
        PSY_1,PSYMA=PSY(CLOSE=self.C)
        result=CROSS(PSY_1,PSYMA)
        #result=IF(result==True,0,1)
        return result
    def PSY_死叉(self):
        '''
        PSY_金叉 的 Docstring
        '''
        PSY_1,PSYMA=PSY(CLOSE=self.C)
        result=CROSS(PSYMA,PSY_1)
        #result=IF(result==True,0,1)  
        return result
    def roll_alpha(self,n=5):
        '''
        5日alpha
        '''
        result=ep.roll_alpha(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    def roll_beta(self,n=5):
        '''
        5日beta
        '''
        result=ep.roll_beta(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    def roll_sharpe_ratio(self,n=5):
        '''
        5日夏普
        '''
        result=ep.roll_sharpe_ratio(self.C.pct_change(),window=n)
        return result
    def roll_annual_volatility(self,n=5):
        '''
        5日年华波动率
        '''
        result=ep.roll_annual_volatility(self.C.pct_change(),window=n)
        return result
    def roll_max_drawdown(self,n=5):
        '''
        5日最大回撤
        '''
        result=ep.roll_max_drawdown(self.C.pct_change(),window=n)
        return result
    def roll_up_capture(self,n=5):
        '''
        5日上涨捕获率
        '''
    
        result=ep.roll_up_capture(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    def roll_down_capture(self,n=5):
        '''
        5日下跌捕获率
        '''
        result=ep.roll_down_capture(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    
    
    




    






    # ========== 因子方法 ==========
    def SMA(self, period=5):
        """
        SMA
        """
        return MA(self.C, N=period)
    
    def CROSS_UP(self, n1=5, n2=10):
        """
        金叉判断
        """
        result = CROSS(MA(self.C, n1), MA(self.C, n2))
        return result
    
    def CROSS_DOWN(self, n1=10, n2=5):
        """
        死叉判断
        """
        result = CROSS(MA(self.C, n1), MA(self.C, n2))
        return result
    
    def BARSLASTCOUNT_UP(self):
        """
        连续上涨
        """
        return BARSLASTCOUNT(self.C > self.O)
    
    def BARSLASTCOUNT_DOWN(self):
        """
        连续下跌
        """
        return BARSLASTCOUNT(self.C < self.O)
    
    def PRICE_MA_LINE_ANAL(self, n=5):
        """
        价格在5均线上
        """
        #IF(self.C >= MA(self.C, n), 0, 1)
        return self.C >= MA(self.C, n)
    
    def MA_LINE_ANAL(self, n1=5, n2=10):
        """
        5均线在10均线上
        """
        #IF(MA(self.C, n1) >= MA(self.C, n2), 0, 1)
        return MA(self.C, n1) >= MA(self.C, n2)
    
    def HHVBARS(self, n=5):
        """
        5日最高值到当前周期
        """
        return HHVBARS(self.C, n)
    
    def LLVBARS(self, n=5):
        """
        5日最低值到当前周期
        """
        return LLVBARS(self.C, n)
    
    def cacal_zdf(self, n=5):
        """
        5日涨跌幅
        """
        return (self.C / REF(self.C, n) - 1) * 100
    def cacal_price_line_zdf(self, n=5):
        """
        价格距离5日均线涨跌幅
        """
        result=((self.C-MA(self.C,n))/MA(self.C,n))*100
        return result
    def cacal_line_line_zdf(self, n1=5,n2=10):
        """
        5日均线距离10日均线涨跌幅
        """
        result=((MA(self.C,n1)-MA(self.C,n2))/MA(self.C,n2))*100
        return result
    def cacal_skew(self,n=5):
        '''
        5日偏度
        '''
        result=self.C.rolling(window=n).skew()
        return result
    def cacal_kurt(self,n=5):
        '''
        5日峰度
        '''
        result=self.C.rolling(window=n).kurt()
        return result
    
    def calculate_momentum_score(self, n=3):
        """
        n日回归动量 - 返回时间序列
        """
        df = self.df.copy()
        mom_daily = n
        
        # 创建与df相同索引的Series，初始全部为NaN
        result = pd.Series(index=df.index, dtype=float)
        
        # 从 n-1 开始，因为需要至少 n 个数据点来计算
        for i in range(mom_daily - 1, len(df)):
            # 获取从 i-n+1 到 i 的窗口数据 (共 n 个数据点)
            start_idx = i - mom_daily + 1
            df_sub = df.iloc[start_idx:i+1].copy()
            
            # 检查数据是否足够
            if len(df_sub) < mom_daily:
                continue
            
            # 检查价格数据是否有效
            close_data = df_sub['closePrice'].values
            if np.any(np.isnan(close_data)) or np.any(np.isinf(close_data)) or np.any(close_data <= 0):
                continue
            
            try:
                y = np.log(close_data)
                y_len = len(y)
                weights = np.linspace(1, 2, y_len)
                x = np.arange(y_len)
                slope, intercept = np.polyfit(x, y, 1, w=weights)
                annualized_returns = math.pow(math.exp(slope), 250) - 1
                residuals = y - (slope * x + intercept)
                weighted_residuals = weights * residuals**2
                y_mean = np.mean(y)
                r_squared = 1 - (np.sum(weighted_residuals) / np.sum(weights * (y - y_mean)**2))
                score = annualized_returns * r_squared
                result.iloc[i] = score
            except Exception as e:
                continue
        
        return result
    
    def SLOPE(self, n=5):
        '''
        5日回归斜率
        '''
        result = SLOPE(self.close, N=n)
        return result
    
    def STD(self, n=5):
        '''
        5日标准差
        '''
        result = STD(self.close, N=n)
        return result

    # ===== 超卖超买类 =====

    def CCI(self):
        '''
        CCI商品路径指标
        '''
        TYP = (self.H + self.L + self.C) / 3
        result = (TYP - MA(TYP, 14)) * 1000 / (15 * AVEDEV(TYP, 14))
        return result

    def MFI(self):
        '''
        最近流量指标
        '''
        return MFI(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=14)

    def MTM_MTM(self):
        '''动量线 - MTM值'''
        mtm_val, mtmma_val = MTM(CLOSE=self.C, N=12, M=6)
        return mtm_val

    def MTM_MTMMA(self):
        '''动量线 - MTMMA值'''
        mtm_val, mtmma_val = MTM(CLOSE=self.C, N=12, M=6)
        return mtmma_val


    def RSI1(self):
        '''相对强弱指标 - RSI1'''
        rsi1_val, rsi2_val, rsi3_val = RSI(CLOSE=self.C, N1=6, N2=12, N3=24)
        return rsi1_val

    def RSI2(self):
        '''相对强弱指标 - RSI2'''
        rsi1_val, rsi2_val, rsi3_val = RSI(CLOSE=self.C, N1=6, N2=12, N3=24)
        return rsi2_val

    def RSI3(self):
        '''相对强弱指标 - RSI3'''
        rsi1_val, rsi2_val, rsi3_val = RSI(CLOSE=self.C, N1=6, N2=12, N3=24)
        return rsi3_val

    def KDJ_K(self):
        '''KDJ指标 - K值'''
        k_val, d_val, j_val = KDJ(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3, M2=3)
        return k_val

    def KDJ_D(self):
        '''KDJ指标 - D值'''
        k_val, d_val, j_val = KDJ(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3, M2=3)
        return d_val

    def KDJ_J(self):
        '''KDJ指标 - J值'''
        k_val, d_val, j_val = KDJ(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3, M2=3)
        return j_val

    def SKDJ_K(self):
        '''慢速随机指标 - K值'''
        k_val, d_val = SKDJ(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M=3)
        return k_val

    def SKDJ_D(self):
        '''慢速随机指标 - D值'''
        k_val, d_val = SKDJ(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M=3)
        return d_val

    def UDL_UDL(self):
        '''引力线 - UDL值'''
        udl_val, maudl_val = UDL(CLOSE=self.C, N1=3, N2=5, N3=10, N4=20, M=6)
        return udl_val

    def UDL_MAUDL(self):
        '''引力线 - MAUDL值'''
        udl_val, maudl_val = UDL(CLOSE=self.C, N1=3, N2=5, N3=10, N4=20, M=6)
        return maudl_val

    def WR1(self):
        '''威廉指标 - WR1'''
        wr1_val, wr2_val = WR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=10, N1=6)
        return wr1_val

    def WR2(self):
        '''威廉指标 - WR2'''
        wr1_val, wr2_val = WR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=10, N1=6)
        return wr2_val

    def LWR1(self):
        '''LWR指标 - LWR1'''
        lwr1_val, lwr2_val = LWR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M1=3, M2=3)
        return lwr1_val

    def LWR2(self):
        '''LWR指标 - LWR2'''
        lwr1_val, lwr2_val = LWR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M1=3, M2=3)
        return lwr2_val

    def MARSI1(self):
        '''相对强弱平均线 - RSI1'''
        rsi1_val, rsi2_val = MARSI(CLOSE=self.C, M1=10, M2=6)
        return rsi1_val

    def MARSI2(self):
        '''相对强弱平均线 - RSI2'''
        rsi1_val, rsi2_val = MARSI(CLOSE=self.C, M1=10, M2=6)
        return rsi2_val

    def BIAS1(self):
        '''乖离率 - BIAS1(6日)'''
        bias1_val, bias2_val, bias3_val = BIAS(CLOSE=self.C, N1=6, N2=12, N3=24)
        return bias1_val

    def BIAS2(self):
        '''乖离率 - BIAS2(12日)'''
        bias1_val, bias2_val, bias3_val = BIAS(CLOSE=self.C, N1=6, N2=12, N3=24)
        return bias2_val

    def BIAS3(self):
        '''乖离率 - BIAS3(24日)'''
        bias1_val, bias2_val, bias3_val = BIAS(CLOSE=self.C, N1=6, N2=12, N3=24)
        return bias3_val

    def BIAS_QL_BIAS(self):
        '''乖离率-传统版 - BIAS值'''
        bias_val, biasma_val = BIAS_QL(CLOSE=self.C, N=6, M=6)
        return bias_val

    def BIAS_QL_BIASMA(self):
        '''乖离率-传统版 - BIASMA值'''
        bias_val, biasma_val = BIAS_QL(CLOSE=self.C, N=6, M=6)
        return biasma_val

    def BIAS36_BIAS36(self):
        '''三六乖离 - BIAS36'''
        bias36_val, bias612_val, mabias_val = BIAS36(CLOSE=self.C, M=6)
        return bias36_val

    def BIAS36_BIAS612(self):
        '''三六乖离 - BIAS612'''
        bias36_val, bias612_val, mabias_val = BIAS36(CLOSE=self.C, M=6)
        return bias612_val

    def BIAS36_MABIAS(self):
        '''三六乖离 - MABIAS'''
        bias36_val, bias612_val, mabias_val = BIAS36(CLOSE=self.C, M=6)
        return mabias_val

    def ACCER(self):
        '''幅度涨速'''
        return ACCER(CLOSE=self.C, N=8)

    # ===== 趋势类型 =====

    def ASI_ASI(self):
        '''振动升降指标 - ASI'''
        asi_val, asit_val = ASI(OPEN=self.O, CLOSE=self.C, HIGH=self.H, LOW=self.L, M1=26, M2=10)
        return asi_val

    def ASI_ASIT(self):
        '''振动升降指标 - ASIT'''
        asi_val, asit_val = ASI(OPEN=self.O, CLOSE=self.C, HIGH=self.H, LOW=self.L, M1=26, M2=10)
        return asit_val

    def CHO_CHO(self):
        '''佳庆指标 - CHO'''
        cho_val, macho_val = CHO(CLOSE=self.C, OPEN=self.O, LOW=self.L, HIGH=self.H, VOL=self.V, N1=10, N2=20, M=6)
        return cho_val

    def CHO_MACHO(self):
        '''佳庆指标 - MACHO'''
        cho_val, macho_val = CHO(CLOSE=self.C, OPEN=self.O, LOW=self.L, HIGH=self.H, VOL=self.V, N1=10, N2=20, M=6)
        return macho_val

    def DMA_XT_DIF(self):
        '''平均差 - DIF'''
        dif_val, difma_val = DMA_XT(CLOSE=self.C, N1=10, N2=50, M=10)
        return dif_val

    def DMA_XT_DIFMA(self):
        '''平均差 - DIFMA'''
        dif_val, difma_val = DMA_XT(CLOSE=self.C, N1=10, N2=50, M=10)
        return difma_val

    def DMI_PDI(self):
        '''趋向指标 - PDI'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return pdi_val

    def DMI_MDI(self):
        '''趋向指标 - MDI'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return mdi_val

    def DMI_ADX(self):
        '''趋向指标 - ADX'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return adx_val

    def DMI_ADXR(self):
        '''趋向指标 - ADXR'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return adxr_val

    def DPO_DPO(self):
        '''区间震荡线 - DPO'''
        dpo_val, madpo_val = DPO(CLOSE=self.C, N=21, M=6)
        return dpo_val

    def DPO_MADPO(self):
        '''区间震荡线 - MADPO'''
        dpo_val, madpo_val = DPO(CLOSE=self.C, N=21, M=6)
        return madpo_val

    def EMV_EMV(self):
        '''简易波动指标 - EMV'''
        emv_val, maemv_val = EMV(HIGH=self.H, LOW=self.L, VOL=self.V, N=14, M=9)
        return emv_val

    def EMV_MAEMV(self):
        '''简易波动指标 - MAEMV'''
        emv_val, maemv_val = EMV(HIGH=self.H, LOW=self.L, VOL=self.V, N=14, M=9)
        return maemv_val

    def MACD_DIF(self):
        '''平滑异同平均线 - DIF'''
        dif_val, dea_val, macd_val = MACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dif_val

    def MACD_DEA(self):
        '''平滑异同平均线 - DEA'''
        dif_val, dea_val, macd_val = MACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dea_val

    def MACD_MACD(self):
        '''平滑异同平均线 - MACD'''
        dif_val, dea_val, macd_val = MACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return macd_val

    def VMACD_DIF(self):
        '''量平滑异同平均线 - DIF'''
        dif_val, dea_val, macd_val = VMACD(VOL=self.V, SHORT=12, LONG=26, MID=9)
        return dif_val

    def VMACD_DEA(self):
        '''量平滑异同平均线 - DEA'''
        dif_val, dea_val, macd_val = VMACD(VOL=self.V, SHORT=12, LONG=26, MID=9)
        return dea_val

    def VMACD_MACD(self):
        '''量平滑异同平均线 - MACD'''
        dif_val, dea_val, macd_val = VMACD(VOL=self.V, SHORT=12, LONG=26, MID=9)
        return macd_val

    def SMACD_DEA(self):
        '''单线平滑异同平均线 - DEA'''
        dea_val, macd_val = SMACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dea_val

    def SMACD_MACD(self):
        '''单线平滑异同平均线 - MACD'''
        dea_val, macd_val = SMACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return macd_val

    def QACD_DIF(self):
        '''快速异同平均线 - DIF'''
        dif_val, macd_val, ddif_val = QACD(CLOSE=self.C, N1=12, N2=12, M=9)
        return dif_val

    def QACD_MACD(self):
        '''快速异同平均线 - MACD'''
        dif_val, macd_val, ddif_val = QACD(CLOSE=self.C, N1=12, N2=12, M=9)
        return macd_val

    def QACD_DDIF(self):
        '''快速异同平均线 - DDIF'''
        dif_val, macd_val, ddif_val = QACD(CLOSE=self.C, N1=12, N2=12, M=9)
        return ddif_val

    def TRIX_TRIX(self):
        '''三重指数平均线 - TRIX'''
        trix_val, matrix_val = TRIX(CLOSE=self.C, N=12, M=9)
        return trix_val

    def TRIX_MATRIX(self):
        '''三重指数平均线 - MATRIX'''
        trix_val, matrix_val = TRIX(CLOSE=self.C, N=12, M=9)
        return matrix_val

    def UOS_UOS(self):
        '''终极指标 - UOS'''
        uos_val, mauos_val = UOS(CLOSE=self.C, HIGH=self.H, LOW=self.L, N1=7, N2=14, N3=28, M=6)
        return uos_val

    def UOS_MAUOS(self):
        '''终极指标 - MAUOS'''
        uos_val, mauos_val = UOS(CLOSE=self.C, HIGH=self.H, LOW=self.L, N1=7, N2=14, N3=28, M=6)
        return mauos_val

    def VTP_VPT(self):
        '''量价曲线 - VPT'''
        vpt_val, mavp_val = VTP(CLOSE=self.C, VOL=self.V, N=51, M=6)
        return vpt_val

    def VTP_MAVP(self):
        '''量价曲线 - MAVP'''
        vpt_val, mavp_val = VTP(CLOSE=self.C, VOL=self.V, N=51, M=6)
        return mavp_val

    def WVAD_WVAD(self):
        '''威廉变异离散量 - WVAD'''
        wvad_val, mawvad_val = WVAD(CLOSE=self.C, OPEN=self.O, HIGH=self.H, LOW=self.L, VOL=self.V, N=24, M=6)
        return wvad_val

    def WVAD_MAWVAD(self):
        '''威廉变异离散量 - MAWVAD'''
        wvad_val, mawvad_val = WVAD(CLOSE=self.C, OPEN=self.O, HIGH=self.H, LOW=self.L, VOL=self.V, N=24, M=6)
        return mawvad_val

    def JS_JS(self):
        '''加数线 - JS'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return js_val

    def JS_MAJS1(self):
        '''加数线 - MAJS1'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return majs1_val

    def JS_MAJS2(self):
        '''加数线 - MAJS2'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return majs2_val

    def JS_MAJS3(self):
        '''加数线 - MAJS3'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return majs3_val

    def CYE_CYEL(self):
        '''市场趋势 - CYEL'''
        cyel_val, cyes_val = CYE(CLOSE=self.C)
        return cyel_val

    def CYE_CYES(self):
        '''市场趋势 - CYES'''
        cyel_val, cyes_val = CYE(CLOSE=self.C)
        return cyes_val

    def GDX_轨道(self):
        '''轨道线 - 轨道'''
        轨道_val, 压力线_val, 支撑线_val = GDX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30, M=9)
        return 轨道_val

    def GDX_压力线(self):
        '''轨道线 - 压力线'''
        轨道_val, 压力线_val, 支撑线_val = GDX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30, M=9)
        return 压力线_val

    def GDX_支撑线(self):
        '''轨道线 - 支撑线'''
        轨道_val, 压力线_val, 支撑线_val = GDX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30, M=9)
        return 支撑线_val

    def JLHB_B(self):
        '''绝路航标 - B'''
        b_val, var2_val, 绝路航标_val = JLHB(CLOSE=self.C, LOW=self.L,HIGH=self.H, N=7, M=5)
        return b_val

    def JLHB_VAR2(self):
        '''绝路航标 - VAR2'''
        b_val, var2_val, 绝路航标_val = JLHB(CLOSE=self.C, LOW=self.L,HIGH=self.H, N=7, M=5)
        return var2_val

    def JLHB_绝路航标(self):
        '''绝路航标 - 绝路航标'''
        b_val, var2_val, 绝路航标_val = JLHB(CLOSE=self.C, LOW=self.L,HIGH=self.H, N=7, M=5)
        return 绝路航标_val

    # ===== 能量类型 =====

    def BRAR_BR(self):
        '''情绪指标 - BR'''
        br_val, ar_val = BRAR(OPEN=self.O, HIGH=self.H, LOW=self.L,CLOSE=self.C, N=26)
        return br_val

    def BRAR_AR(self):
        '''情绪指标 - AR'''
        br_val, ar_val = BRAR(OPEN=self.O, HIGH=self.H, LOW=self.L,CLOSE=self.C, N=26)
        return ar_val

    def CR_CR(self):
        '''带状能量线 - CR'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return cr_val

    def CR_MA1(self):
        '''带状能量线 - MA1'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma1_val

    def CR_MA2(self):
        '''带状能量线 - MA2'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma2_val

    def CR_MA3(self):
        '''带状能量线 - MA3'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma3_val

    def CR_MA4(self):
        '''带状能量线 - MA4'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma4_val

    def MASS_MASS(self):
        '''梅斯线 - MASS'''
        mass_val, mamass_val = MASS(HIGH=self.H, LOW=self.L, N1=9, N2=25, M=6)
        return mass_val

    def MASS_MAMASS(self):
        '''梅斯线 - MAMASS'''
        mass_val, mamass_val = MASS(HIGH=self.H, LOW=self.L, N1=9, N2=25, M=6)
        return mamass_val

    def PSY_PSY(self):
        '''心理线 - PSY'''
        psy_val, psyma_val = PSY(CLOSE=self.C, N=12, M=6)
        return psy_val

    def PSY_PSYMA(self):
        '''心理线 - PSYMA'''
        psy_val, psyma_val = PSY(CLOSE=self.C, N=12, M=6)
        return psyma_val

    def VR_VR(self):
        '''成交量变异率 - VR'''
        vr_val, mavr_val = VR(CLOSE=self.C,VOL=self.V, N=26, M=6)
        return vr_val

    def VR_MAVR(self):
        '''成交量变异率 - MAVR'''
        vr_val, mavr_val = VR(CLOSE=self.C,VOL=self.V, N=26, M=6)
        return mavr_val

    def WAD_WAD(self):
        '''威廉多空力度线 - WAD'''
        wad_val, mawad_val = WAD(CLOSE=self.C, LOW=self.L,HIGH=self.H, M=30)
        return wad_val

    def WAD_MAWAD(self):
        '''威廉多空力度线 - MAWAD'''
        wad_val, mawad_val = WAD(CLOSE=self.C, LOW=self.L,HIGH=self.H, M=30)
        return mawad_val

    def PCNT_PCNT(self):
        '''幅度比 - PCNT'''
        pcnt_val, mapcnt_val = PCNT(CLOSE=self.C, M=5)
        return pcnt_val

    def PCNT_MAPCNT(self):
        '''幅度比 - MAPCNT'''
        pcnt_val, mapcnt_val = PCNT(CLOSE=self.C, M=5)
        return mapcnt_val

    def CYR_CYR(self):
        '''市场强弱 - CYR'''
        cyr_val, macyr_val = CYR(AMOUNT=self.AMOUNT,VOL=self.V, N=13, M=5)
        return cyr_val

    def CYR_MACYR(self):
        '''市场强弱 - MACYR'''
        cyr_val, macyr_val = CYR(AMOUNT=self.AMOUNT,VOL=self.V, N=13, M=5)
        return macyr_val

    # ===== 能量型 =====

    def AMO_AMOW(self):
        '''成交金额 - AMOW'''
        amow_val, amo1_val, amo2_val = AMO(AMOUNT=self.AMOUNT, M1=5, M2=10)
        return amow_val

    def AMO_AMO1(self):
        '''成交金额 - AMO1'''
        amow_val, amo1_val, amo2_val = AMO(AMOUNT=self.AMOUNT, M1=5, M2=10)
        return amo1_val

    def AMO_AMO2(self):
        '''成交金额 - AMO2'''
        amow_val, amo1_val, amo2_val = AMO(AMOUNT=self.AMOUNT, M1=5, M2=10)
        return amo2_val

    def OBV_OBV(self):
        '''累积能量线 - OBV'''
        obv_val, maobv_val = OBV(VOL=self.V, CLOSE=self.C, M=30)
        return obv_val

    def OBV_MAOBV(self):
        '''累积能量线 - MAOBV'''
        obv_val, maobv_val = OBV(VOL=self.V, CLOSE=self.C, M=30)
        return maobv_val

    def VOL_XT_MAVOL1(self):
        '''成交量 - MAVOL1'''
        mavol1_val, mavol2_val = VOL_XT(VOL=self.V, M1=5, M2=10)
        return mavol1_val

    def VOL_XT_MAVOL2(self):
        '''成交量 - MAVOL2'''
        mavol1_val, mavol2_val = VOL_XT(VOL=self.V, M1=5, M2=10)
        return mavol2_val

    def VRSI1(self):
        '''相对强弱量 - RSI1'''
        rsi1_val, rsi2_val, rsi3_val = VRSI(VOL=self.V, N1=6, N2=12, N3=24)
        return rsi1_val

    def VRSI2(self):
        '''相对强弱量 - RSI2'''
        rsi1_val, rsi2_val, rsi3_val = VRSI(VOL=self.V, N1=6, N2=12, N3=24)
        return rsi2_val

    def VRSI3(self):
        '''相对强弱量 - RSI3'''
        rsi1_val, rsi2_val, rsi3_val = VRSI(VOL=self.V, N1=6, N2=12, N3=24)
        return rsi3_val

    def HSL_HSL(self):
        '''换手线 - HSL'''
        hsl_val, mahsl_val = HSL(HSL=self.V, N=5)
        return hsl_val

    def HSL_MAHSL(self):
        '''换手线 - MAHSL'''
        hsl_val, mahsl_val = HSL(HSL=self.V, N=5)
        return mahsl_val

    # ===== 均线系统 =====

    def MA_XT_MA1(self):
        '''均线 - MA1(5日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma1_val

    def MA_XT_MA2(self):
        '''均线 - MA2(10日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma2_val

    def MA_XT_MA3(self):
        '''均线 - MA3(20日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma3_val

    def MA_XT_MA4(self):
        '''均线 - MA4(60日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma4_val

    def ACD_ACD(self):
        '''升降线 - ACD'''
        acd_val, maacd_val = ACD(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=20)
        return acd_val

    def ACD_MAACD(self):
        '''升降线 - MAACD'''
        acd_val, maacd_val = ACD(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=20)
        return maacd_val

    def BBI(self):
        '''多空均线'''
        return BBI(CLOSE=self.C, M1=3, M2=6, M3=12, M4=24)

    def EXPMA_EXP1(self):
        '''指数平均线 - EXP1(12日)'''
        exp1_val, exp2_val = EXPMA(CLOSE=self.C, M1=12, M2=50)
        return exp1_val

    def EXPMA_EXP2(self):
        '''指数平均线 - EXP2(50日)'''
        exp1_val, exp2_val = EXPMA(CLOSE=self.C, M1=12, M2=50)
        return exp2_val

    def HMA_HMA1(self):
        '''高价平均线 - HMA1'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma1_val

    def HMA_HMA2(self):
        '''高价平均线 - HMA2'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma2_val

    def HMA_HMA3(self):
        '''高价平均线 - HMA3'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma3_val

    def HMA_HMA4(self):
        '''高价平均线 - HMA4'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma4_val

    def HMA_HMA5(self):
        '''高价平均线 - HMA5'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma5_val

    def LMA_LMA1(self):
        '''低价平均线 - LMA1'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma1_val

    def LMA_LMA2(self):
        '''低价平均线 - LMA2'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma2_val

    def LMA_LMA3(self):
        '''低价平均线 - LMA3'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma3_val

    def LMA_LMA4(self):
        '''低价平均线 - LMA4'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma4_val

    def LMA_LMA5(self):
        '''低价平均线 - LMA5'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma5_val

    def VMA_VMA1(self):
        '''变异平均线 - VMA1'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma1_val

    def VMA_VMA2(self):
        '''变异平均线 - VMA2'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma2_val

    def VMA_VMA3(self):
        '''变异平均线 - VMA3'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma3_val

    def VMA_VMA4(self):
        '''变异平均线 - VMA4'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma4_val

    def VMA_VMA5(self):
        '''变异平均线 - VMA5'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma5_val

    def AMV_AMV1(self):
        '''成本均线 - AMV1(5日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv1_val

    def AMV_AMV2(self):
        '''成本均线 - AMV2(13日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv2_val

    def AMV_AMV3(self):
        '''成本均线 - AMV3(34日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv3_val

    def AMV_AMV4(self):
        '''成本均线 - AMV4(60日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv4_val

    def BBIBOLL_BBIBOLL(self):
        '''多空布林线 - BBIBOLL'''
        bbiboll_val, upr_val, dwn_val = BBIBOLL(CLOSE=self.C, N=11, M=6)
        return bbiboll_val

    def BBIBOLL_UPR(self):
        '''多空布林线 - UPR'''
        bbiboll_val, upr_val, dwn_val = BBIBOLL(CLOSE=self.C, N=11, M=6)
        return upr_val

    def BBIBOLL_DWN(self):
        '''多空布林线 - DWN'''
        bbiboll_val, upr_val, dwn_val = BBIBOLL(CLOSE=self.C, N=11, M=6)
        return dwn_val

    def ALLIGAT_上唇(self):
        '''鳄鱼线 - 上唇'''
        上唇_val, 牙齿_val, 下颚_val = ALLIGAT(HIGH=self.H, LOW=self.L)
        return 上唇_val

    def ALLIGAT_牙齿(self):
        '''鳄鱼线 - 牙齿'''
        上唇_val, 牙齿_val, 下颚_val = ALLIGAT(HIGH=self.H, LOW=self.L)
        return 牙齿_val

    def ALLIGAT_下颚(self):
        '''鳄鱼线 - 下颚'''
        上唇_val, 牙齿_val, 下颚_val = ALLIGAT(HIGH=self.H, LOW=self.L)
        return 下颚_val

    def GMMA_MA3(self):
        '''顾比均线 - MA3'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma3_val

    def GMMA_MA5(self):
        '''顾比均线 - MA5'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma5_val

    def GMMA_MA8(self):
        '''顾比均线 - MA8'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma8_val

    def GMMA_MA10(self):
        '''顾比均线 - MA10'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma10_val

    def GMMA_MA12(self):
        '''顾比均线 - MA12'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma12_val

    def GMMA_MA15(self):
        '''顾比均线 - MA15'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma15_val

    def GMMA_MA30(self):
        '''顾比均线 - MA30'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma30_val

    def GMMA_MA35(self):
        '''顾比均线 - MA35'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma35_val

    def GMMA_MA40(self):
        '''顾比均线 - MA40'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma40_val

    def GMMA_MA45(self):
        '''顾比均线 - MA45'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma45_val

    def GMMA_MA50(self):
        '''顾比均线 - MA50'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma50_val

    def GMMA_MA60(self):
        '''顾比均线 - MA60'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma60_val

    # ===== 路径类 =====

    def BOLL_BOLL(self):
        '''布林线 - BOLL'''
        boll_val, ub_val, lb_val = BOLL(CLOSE=self.C, M=20)
        return boll_val

    def BOLL_UB(self):
        '''布林线 - UB'''
        boll_val, ub_val, lb_val = BOLL(CLOSE=self.C, M=20)
        return ub_val

    def BOLL_LB(self):
        '''布林线 - LB'''
        boll_val, ub_val, lb_val = BOLL(CLOSE=self.C, M=20)
        return lb_val

    def PBX_PBX1(self):
        '''瀑布线 - PBX1'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx1_val

    def PBX_PBX2(self):
        '''瀑布线 - PBX2'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx2_val

    def PBX_PBX3(self):
        '''瀑布线 - PBX3'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx3_val

    def PBX_PBX4(self):
        '''瀑布线 - PBX4'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx4_val

    def PBX_PBX5(self):
        '''瀑布线 - PBX5'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx5_val

    def PBX_PBX6(self):
        '''瀑布线 - PBX6'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx6_val

    def ENE_UPPER(self):
        '''轨道线 - UPPER'''
        upper_val, lower_val, ene_val = ENE(CLOSE=self.C, N=25, M1=6, M2=6)
        return upper_val

    def ENE_LOWER(self):
        '''轨道线 - LOWER'''
        upper_val, lower_val, ene_val = ENE(CLOSE=self.C, N=25, M1=6, M2=6)
        return lower_val

    def ENE_ENE(self):
        '''轨道线 - ENE'''
        upper_val, lower_val, ene_val = ENE(CLOSE=self.C, N=25, M1=6, M2=6)
        return ene_val

    def MIKE_STOR(self):
        '''麦克支撑压力 - STOR'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return stor_val

    def MIKE_MIDR(self):
        '''麦克支撑压力 - MIDR'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return midr_val

    def MIKE_WEKR(self):
        '''麦克支撑压力 - WEKR'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return wekr_val

    def MIKE_WEKS(self):
        '''麦克支撑压力 - WEKS'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return weks_val

    def MIKE_MIDS(self):
        '''麦克支撑压力 - MIDS'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return mids_val

    def MIKE_STOS(self):
        '''麦克支撑压力 - STOS'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return stos_val

    def XS_SUP(self):
        '''薛斯通道 - SUP'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return sup_val

    def XS_SDN(self):
        '''薛斯通道 - SDN'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return sdn_val

    def XS_LUP(self):
        '''薛斯通道 - LUP'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return lup_val

    def XS_LDN(self):
        '''薛斯通道 - LDN'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return ldn_val

    def TQN_周期高点(self):
        '''唐奇安通道 - 周期高点'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 周期高点_val

    def TQN_周期低点(self):
        '''唐奇安通道 - 周期低点'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 周期低点_val

    def TQN_平空开多(self):
        '''唐奇安通道 - 平空开多信号'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 平空开多_val

    def TQN_平多开空(self):
        '''唐奇安通道 - 平多开空信号'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 平多开空_val

    # ===== 停损 =====

    def SAR(self):
        '''抛物线指标'''
        return SAR(HIGH=self.H, LOW=self.L, M=10, af=2, amax=20)

    # ===== 交易类型 =====

    def MA_交易_MA1(self):
        '''MA交易 - MA1(短期均线)'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return ma1_val

    def MA_交易_MA2(self):
        '''MA交易 - MA2(长期均线)'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return ma2_val

    def MA_交易_平空开多(self):
        '''MA交易 - 平空开多信号'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return 平空开多_val

    def MA_交易_平多开空(self):
        '''MA交易 - 平多开空信号'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return 平多开空_val

    def MACD_交易_DIFF(self):
        '''MACD交易 - DIFF'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return diff_val

    def MACD_交易_DEA(self):
        '''MACD交易 - DEA'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dea_val

    def MACD_交易_MACD(self):
        '''MACD交易 - MACD'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return macd_val

    def MACD_交易_平空开多(self):
        '''MACD交易 - 平空开多信号'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return 平空开多_val

    def MACD_交易_平多开空(self):
        '''MACD交易 - 平多开空信号'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return 平多开空_val

    def KDJ_交易_K(self):
        '''KDJ交易 - K值'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return k_val

    def KDJ_交易_D(self):
        '''KDJ交易 - D值'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return d_val

    def KDJ_交易_J(self):
        '''KDJ交易 - J值'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return j_val

    def KDJ_交易_平空开多(self):
        '''KDJ交易 - 平空开多信号'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return 平空开多_val

    def KDJ_交易_平多开空(self):
        '''KDJ交易 - 平多开空信号'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return 平多开空_val

    # ===== 神系 =====

    def SG_XDT_QR(self):
        '''心电图 - QR强弱指标'''
        qr_val, mqr1_val, mqr2_val = SG_XDT(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return qr_val

    def SG_XDT_MQR1(self):
        '''心电图 - MQR1(5日均线)'''
        qr_val, mqr1_val, mqr2_val = SG_XDT(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return mqr1_val

    def SG_XDT_MQR2(self):
        '''心电图 - MQR2(10日均线)'''
        qr_val, mqr1_val, mqr2_val = SG_XDT(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return mqr2_val

    def SG_NDB_DK(self):
        '''脑电波 - DK'''
        dk_val, mdk1_val, mdk2_val = SG_NDB(CLOSE=self.C, HIGH=self.H, LOW=self.L, P1=5, P2=10)
        return dk_val

    def SG_NDB_MDK1(self):
        '''脑电波 - MDK1'''
        dk_val, mdk1_val, mdk2_val = SG_NDB(CLOSE=self.C, HIGH=self.H, LOW=self.L, P1=5, P2=10)
        return mdk1_val

    def SG_NDB_MDK2(self):
        '''脑电波 - MDK2'''
        dk_val, mdk1_val, mdk2_val = SG_NDB(CLOSE=self.C, HIGH=self.H, LOW=self.L, P1=5, P2=10)
        return mdk2_val

    def SG_SMX_ZY1(self):
        '''生命线 - ZY1(3日EMA)'''
        zy1_val, zy2_val, zy3_val = SG_SMX(CLOSE=self.C, HIGH=self.H, LOW=self.L, 
                                INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                N=50)
        return zy1_val

    def SG_SMX_ZY2(self):
        '''生命线 - ZY2(17日EMA)'''
        zy1_val, zy2_val, zy3_val = SG_SMX(CLOSE=self.C, HIGH=self.H, LOW=self.L, 
                                INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                N=50)
        return zy2_val

    def SG_SMX_ZY3(self):
        '''生命线 - ZY3(34日EMA)'''
        zy1_val, zy2_val, zy3_val = SG_SMX(CLOSE=self.C, HIGH=self.H, LOW=self.L, 
                                INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                N=50)
        return zy3_val

    def SG_LB_量比(self):
        '''量比'''
        量比_val, ma5_val, ma10_val = SG_LB(VOL=self.V, INDEXV=self.index_df['volume'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return 量比_val

    def SG_LB_MA5(self):
        '''量比 - MA5'''
        量比_val, ma5_val, ma10_val = SG_LB(VOL=self.V, INDEXV=self.index_df['volume'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return ma5_val

    def SG_LB_MA10(self):
        '''量比 - MA10'''
        量比_val, ma5_val, ma10_val = SG_LB(VOL=self.V, INDEXV=self.index_df['volume'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return ma10_val

    def SG_PF(self):
        '''强势股评分'''
        return SG_PF(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())

    # ===== 龙系 =====

    def RAD_RADER1(self):
        '''威力雷达 - RADER1'''
        rader1_val, rader_ma_val = RAD(OPEN=self.O, HIGH=self.H, CLOSE=self.C, LOW=self.L,
                            INDEXO=self.index_df['open'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            D=3, S=30, M=30)
        return rader1_val

    def RAD_RADERMA(self):
        '''威力雷达 - RADERMA'''
        rader1_val, rader_ma_val = RAD(OPEN=self.O, HIGH=self.H, CLOSE=self.C, LOW=self.L,
                            INDEXO=self.index_df['open'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            D=3, S=30, M=30)
        return rader_ma_val

    def LON_LON(self):
        '''龙系长线 - LON'''
        lon_val, lonma_val, lont_val = LON(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=10)
        return lon_val

    def LON_LONMA(self):
        '''龙系长线 - LONMA'''
        lon_val, lonma_val, lont_val = LON(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=10)
        return lonma_val

    def LON_LONT(self):
        '''龙系长线 - LONT'''
        lon_val, lonma_val, lont_val = LON(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=10)
        return lont_val

    def SHT_SHT(self):
        '''龙系短线 - SHT'''
        sht_val, shtma_val = SHT(CLOSE=self.C, VOL=self.V, N=5)
        return sht_val

    def SHT_SHTMA(self):
        '''龙系短线 - SHTMA'''
        sht_val, shtma_val = SHT(CLOSE=self.C, VOL=self.V, N=5)
        return shtma_val

    def ZLJC_JCS(self):
        '''主力进出 - JCS'''
        jcs_val, jcm_val, jcl_val = ZLJC(CLOSE=self.C, LOW=self.L, HIGH=self.H,VOL=self.V)
        return jcs_val

    def ZLJC_JCM(self):
        '''主力进出 - JCM'''
        jcs_val, jcm_val, jcl_val = ZLJC(CLOSE=self.C, LOW=self.L, HIGH=self.H,VOL=self.V)
        return jcm_val

    def ZLJC_JCL(self):
        '''主力进出 - JCL'''
        jcs_val, jcm_val, jcl_val = ZLJC(CLOSE=self.C, LOW=self.L, HIGH=self.H,VOL=self.V)
        return jcl_val

    def ZLMM_MMS(self):
        '''主力买卖 - MMS'''
        mms_val, mmm_val, mml_val = ZLMM(CLOSE=self.C)
        return mms_val

    def ZLMM_MMM(self):
        '''主力买卖 - MMM'''
        mms_val, mmm_val, mml_val = ZLMM(CLOSE=self.C)
        return mmm_val

    def ZLMM_MML(self):
        '''主力买卖 - MML'''
        mms_val, mmm_val, mml_val = ZLMM(CLOSE=self.C)
        return mml_val

    def SLZT_白龙(self):
        '''神龙在天 - 白龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 白龙_val

    def SLZT_黄龙(self):
        '''神龙在天 - 黄龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 黄龙_val

    def SLZT_紫龙(self):
        '''神龙在天 - 紫龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 紫龙_val

    def SLZT_青龙(self):
        '''神龙在天 - 青龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 青龙_val

    def SLZT_红龙(self):
        '''神龙在天 - 红龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 红龙_val

    def SLZT_蓝龙(self):
        '''神龙在天 - 蓝龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 蓝龙_val

    def ADVOL_ADVOL(self):
        '''龙系离散量 - ADVOL'''
        advol_val, ma1_val, ma2_val = ADVOL(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)
        return advol_val

    def ADVOL_MA1(self):
        '''龙系离散量 - MA1'''
        advol_val, ma1_val, ma2_val = ADVOL(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)
        return ma1_val

    def ADVOL_MA2(self):
        '''龙系离散量 - MA2'''
        advol_val, ma1_val, ma2_val = ADVOL(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)
        return ma2_val

    # ===== 鬼系 =====

    def CYS(self):
        '''市场盈亏'''
        return CYS(CLOSE=self.C, AMOUNT=self.AMOUNT, VOL=self.V)

    

    def CYW(self):
        '''主力控盘'''
        return CYW(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)

    # ===== 其他系 =====

    def JAX_J(self):
        '''济安线 - J'''
        j_val, a_val, x_val = JAX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30)
        return j_val

    def JAX_A(self):
        '''济安线 - A'''
        j_val, a_val, x_val = JAX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30)
        return a_val

    def JAX_X(self):
        '''济安线 - X'''
        j_val, a_val, x_val = JAX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30)
        return x_val

    def XJDX_J(self):
        '''超级短线 - J'''
        j_val, d_val, k_val = XJDX(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return j_val

    def XJDX_D(self):
        '''超级短线 - D'''
        j_val, d_val, k_val = XJDX(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return d_val

    def XJDX_K(self):
        '''超级短线 - K'''
        j_val, d_val, k_val = XJDX(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return k_val

    def ZJTJ_无庄控盘(self):
        '''庄家抬轿 - 无庄控盘'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 无庄控盘_val

    def ZJTJ_开始控盘(self):
        '''庄家抬轿 - 开始控盘'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 开始控盘_val

    def ZJTJ_有庄控盘(self):
        '''庄家抬轿 - 有庄控盘'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 有庄控盘_val

    def ZJTJ_主力出货(self):
        '''庄家抬轿 - 主力出货'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 主力出货_val

    
    def BDZX_AK(self):
        '''波段之星 - AK'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return ak_val

    def BDZX_AD1(self):
        '''波段之星 - AD1'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return ad1_val

    def BDZX_AJ(self):
        '''波段之星 - AJ'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return aj_val

    def BDZX_买进(self):
        '''波段之星 - 买进信号'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 买进_val

    def BDZX_卖出(self):
        '''波段之星 - 卖出信号'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 卖出_val

    def LHXJ_主力弃盘(self):
        '''猎狐先觉 - 主力弃盘'''
        主力弃盘_val, 主力控盘_val = LHXJ(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 主力弃盘_val

    def LHXJ_主力控盘(self):
        '''猎狐先觉 - 主力控盘'''
        主力弃盘_val, 主力控盘_val = LHXJ(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 主力控盘_val

    def LYJH_机构做空能量线(self):
        '''猎鹰歼狐 - 机构做空能量线'''
        机构做空能量线_val, 机构做多能量线_val, lh_val, lh1_val = LYJH(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=80, M1=50)
        return 机构做空能量线_val

    def LYJH_机构做多能量线(self):
        '''猎鹰歼狐 - 机构做多能量线'''
        机构做空能量线_val, 机构做多能量线_val, lh_val, lh1_val = LYJH(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=80, M1=50)
        return 机构做多能量线_val

    def JFZX_多头力量(self):
        '''飓风智能中线 - 多头力量'''
        多头力量_val, 空头力量_val, 多空平衡_val = JFZX(OPEN=self.O, CLOSE=self.C, VOL=self.V, N=30)
        return 多头力量_val

    def JFZX_空头力量(self):
        '''飓风智能中线 - 空头力量'''
        多头力量_val, 空头力量_val, 多空平衡_val = JFZX(OPEN=self.O, CLOSE=self.C, VOL=self.V, N=30)
        return 空头力量_val

    def CYHT_SK(self):
        '''财运亨通 - SK'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return sk_val

    def CYHT_SD(self):
        '''财运亨通 - SD'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return sd_val

    def CYHT_卖出(self):
        '''财运亨通 - 卖出信号'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return 卖出_val

    def CYHT_买进(self):
        '''财运亨通 - 买进信号'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return 买进_val

    def BSQJ_B买(self):
        '''买卖区间 - B买信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return b买_val

    def BSQJ_持仓(self):
        '''买卖区间 - 持仓信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return 持仓_val

    def BSQJ_S卖(self):
        '''买卖区间 - S卖信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return s卖_val

    def BSQJ_空仓(self):
        '''买卖区间 - 空仓信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return 空仓_val

    def CDP_STD_CDP(self):
        '''逆势操作 - CDP'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return cdp_val

    def CDP_STD_AH(self):
        '''逆势操作 - AH'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return ah_val

    def CDP_STD_NH(self):
        '''逆势操作 - NH'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return nh_val

    def CDP_STD_NL(self):
        '''逆势操作 - NL'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return nl_val

    def CDP_STD_AL(self):
        '''逆势操作 - AL'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return al_val








































    # ===== Alpha因子 =====

    def alpha001(self, max_window=6):
        """
        (-1 * CORR(RANK(DELTA(LOG(VOLUME),1)), RANK((CLOSE-OPEN)/OPEN), 6))
        """
        rank_sizenl = np.log(self.V).diff(1).rank(axis=0, pct=True)
        rank_ret = ((self.C - self.O) / self.O).rank(axis=0, pct=True)
        return -1 * rank_sizenl.rolling(window=max_window, min_periods=max_window).corr(rank_ret)
    
    def alpha002(self, max_window=2):
        """
        -1*delta(((close-low)-(high-close))/(high-low),1)
        """
        win_ratio = (max_window * self.C - self.L - self.H) / (self.H - self.L)
        return -1 * win_ratio.diff(1)
    
    def alpha003(self):
        """
        -1*SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),6)
        """
        alpha = self.C.copy()
        condition2 = self.C.diff(periods=1) > 0.0
        condition3 = self.C.diff(periods=1) < 0.0
        alpha[condition2] = self.C[condition2] - np.minimum(self.C[condition2].shift(1).replace(np.NaN, 10000), self.L[condition2])
        alpha[condition3] = self.C[condition3] - np.maximum(self.C[condition3].shift(1).replace(np.NaN, 0), self.H[condition3])
        return -1 * alpha.sum(axis=0)

    def alpha004(self, max_window=20):
        """
        (((SUM(CLOSE,8)/8)+STD(CLOSE,8))<(SUM(CLOSE,2)/2))
        ?-1:(SUM(CLOSE,2)/2<(SUM(CLOSE,8)/8-STD(CLOSE,8))
            ?1:(1<=(VOLUME/MEAN(VOLUME,20))
                ?1:-1))
        """
        ma8 = self.C.rolling(window=8, min_periods=8).mean()
        std8 = self.C.rolling(window=8, min_periods=8).std()
        ma2 = self.C.rolling(window=2, min_periods=2).mean()
        ma20_vol = self.V.rolling(window=max_window, min_periods=max_window).mean()
        
        result = np.where(
            (ma8 + std8) < ma2,
            -1,
            np.where(
                ma2 < (ma8 - std8),
                1,
                np.where(1 <= (self.V / ma20_vol), 1, -1)
            )
        )
        return pd.Series(result, index=self.df.index, name='alpha004')

    # ... 继续 alpha005 到 alpha191（保持原有代码不变）
    def alpha005(self):
        """
        -1*TSMAX(CORR(TSRANK(VOLUME,5),TSRANK(HIGH,5),5),3)
        """
        ts_volume = self.V.rolling(window=5, min_periods=5).apply(lambda x: stats.rankdata(x)[-1] / 5.0)
        ts_high = self.H.rolling(window=5, min_periods=5).apply(lambda x: stats.rankdata(x)[-1] / 5.0)
        corr_ts = ts_volume.rolling(window=5, min_periods=5).corr(ts_high)
        return -1 * corr_ts.rolling(window=3, min_periods=3).max()
    
    def alpha006(self):
        """
        -1*RANK(SIGN(DELTA(OPEN*0.85+HIGH*0.15,4)))
        """
        weighted_price = self.O * 0.85 + self.H * 0.15
        delta = weighted_price.diff(periods=4)
        sign_val = np.sign(delta)
        rank_val = sign_val.rank(axis=0, pct=True)
        return -1 * rank_val
    
    def alpha007(self):
        """
        (RANK(MAX(VWAP-CLOSE,3))+RANK(MIN(VWAP-CLOSE,3)))*RANK(DELTA(VOLUME,3))
        """
        vwap = self.AMOUNT / self.V
        part1 = (vwap - self.C).rolling(window=3, min_periods=3).max().rank(axis=0, pct=True)
        part2 = (vwap - self.C).rolling(window=3, min_periods=3).min().rank(axis=0, pct=True)
        part3 = self.V.diff(3).rank(axis=0, pct=True)
        return (part1 + part2) * part3
    
    def alpha008(self):
        """
        -1*RANK(DELTA((HIGH+LOW)/10+VWAP*0.8,4))
        """
        vwap = self.AMOUNT / self.V
        ma_price = (self.H + self.L) / 10 + vwap * 0.8
        return -1 * ma_price.diff(4).rank(axis=0, pct=True)
    
    def alpha009(self):
        """
        SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,7,2)
        """
        part1 = (self.H + self.L) * 0.5 - (self.H.shift(1) + self.L.shift(1)) * 0.5
        part2 = part1 * (self.H - self.L) / self.V
        return part2.ewm(adjust=False, alpha=float(2) / 7, min_periods=7).mean()
    
    def alpha010(self):
        """
        RANK(MAX(((RET<0)?STD(RET,20):CLOSE)^2,5))
        """
        ret = self.C.pct_change(periods=1)
        std_ret = ret.rolling(window=20, min_periods=20).std()
        part1 = np.where(ret < 0, std_ret, self.C)
        part1 = pd.Series(part1, index=self.df.index)
        return (part1 ** 2).rolling(window=5, min_periods=5).max().rank(axis=0, pct=True)
    
    def alpha011(self):
        """
        SUM(((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-LOW)*VOLUME,6)
        """
        raw = ((2 * self.C - self.L - self.H) / (self.H - self.L)) * self.V
        return raw.rolling(window=6, min_periods=6).sum()
    
    def alpha012(self):
        """
        RANK(OPEN-MA(VWAP,10))*RANK(ABS(CLOSE-VWAP))*(-1)
        """
        vwap = self.AMOUNT / self.V
        part1 = (self.O - vwap.rolling(window=10, min_periods=10).mean()).rank(axis=0, pct=True)
        part2 = abs(self.C - vwap).rank(axis=0, pct=True)
        return -1 * part1 * part2
    
    def alpha013(self):
        """
        ((HIGH*LOW)^0.5)-VWAP
        """
        vwap = self.AMOUNT / self.V
        return np.sqrt(self.H * self.L) - vwap
    
    def alpha014(self):
        """
        CLOSE-DELAY(CLOSE,5)
        """
        return self.C.diff(5)
    
    def alpha015(self):
        """
        OPEN/DELAY(CLOSE,1)-1
        """
        return self.O / self.C.shift(1) - 1.0
    
    def alpha016(self):
        """
        (-1*TSMAX(RANK(CORR(RANK(VOLUME),RANK(VWAP),5)),5))
        """
        vwap = self.AMOUNT / self.V
        rank_vol = self.V.rank(axis=0, pct=True)
        rank_vwap = vwap.rank(axis=0, pct=True)
        corr_vol_vwap = rank_vol.rolling(window=5, min_periods=5).corr(rank_vwap)
        rank_corr = corr_vol_vwap.rank(axis=0, pct=True)
        return -1 * rank_corr.rolling(window=5, min_periods=5).max()
    
    def alpha017(self):
        """
        RANK(VWAP-MAX(VWAP,15))^DELTA(CLOSE,5)
        """
        vwap = self.AMOUNT / self.V
        delta_price = self.C.diff(5)
        base = (vwap - vwap.rolling(window=15, min_periods=15).max()).rank(axis=0, pct=True)
        return base ** delta_price
    
    def alpha018(self):
        """
        CLOSE/DELAY(CLOSE,5)
        """
        return self.C / self.C.shift(5)
    
    def alpha019(self):
        """
        (CLOSE<DELAY(CLOSE,5)?(CLOSE/DELAY(CLOSE,5)-1):(CLOSE=DELAY(CLOSE,5)?0:(1-DELAY(CLOSE,5)/CLOSE)))
        """
        condition1 = self.C <= self.C.shift(5)
        alpha = self.C.copy()
        alpha[condition1] = self.C.pct_change(periods=5)[condition1]
        alpha[~condition1] = -self.C.pct_change(periods=5)[~condition1]
        return alpha
    
    def alpha020(self):
        """
        (CLOSE/DELAY(CLOSE,6)-1)*100
        """
        return self.C.pct_change(periods=6) * 100.0
    
    def alpha021(self):
        """
        REGBETA(MEAN(CLOSE,6),SEQUENCE(6))
        """
        close_ma = self.C.rolling(window=6, min_periods=6).mean()
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(6, len(self.df)):
            y = close_ma.iloc[i-6:i]
            x = np.arange(1, 7)
            result.iloc[i] = self._regbeta(y, x)
        return result.fillna(0)
    
    def alpha022(self):
        """
        SMEAN((CLOSE/MEAN(CLOSE,6)-1-DELAY(CLOSE/MEAN(CLOSE,6)-1,3)),12,1)
        """
        ratio = self.C / self.C.rolling(window=6, min_periods=6).mean() - 1.0
        alpha = ratio.diff(3)
        return self._sma(alpha, 12, 1)
    
    def alpha023(self):
        """
        SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1) / 
        (SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)+SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1))*100
        """
        prc_std = self.C.rolling(window=20, min_periods=20).std()
        condition1 = self.C > self.C.shift(1)
        part1 = prc_std.copy()
        part2 = prc_std.copy()
        part1[~condition1] = 0.0
        part2[condition1] = 0.0
        sma1 = self._sma(part1, 20, 1)
        sma2 = self._sma(part2, 20, 1)
        return sma1 / (sma1 + sma2) * 100
    
    def alpha024(self):
        """
        SMA(CLOSE-DELAY(CLOSE,5),5,1)
        """
        return self._sma(self.C.diff(5), 5, 1)
    
    def alpha025(self):
        """
        (-1*RANK(DELTA(CLOSE,7)*(1-RANK(DECAYLINEAR(VOLUME/MEAN(VOLUME,20),9)))))*(1+RANK(SUM(RET,250)))
        """
        n_rows = len(self.df)
        if n_rows < 50:
            return pd.Series(index=self.df.index, dtype=float)
        
        if n_rows < 260:
            ret_window = min(250, n_rows - 10)
        else:
            ret_window = 250
        
        w = np.arange(1, 10)
        ret = self.C.pct_change().fillna(0)
        
        part1 = self.C.diff(7).fillna(0)
        vol_ma = self.V.rolling(window=20, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        volume_ratio = (self.V / vol_ma).fillna(method='ffill').fillna(method='bfill')
        
        decay_linear = volume_ratio.rolling(window=9, min_periods=4).apply(
            lambda x: np.dot(x, w[:len(x)]) if len(x) >= 4 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        
        rank_decay = decay_linear.rank(method='min', pct=True).fillna(method='ffill').fillna(method='bfill')
        part2 = 1.0 - rank_decay
        
        sum_ret = ret.rolling(window=ret_window, min_periods=max(10, ret_window//5)).sum().fillna(method='ffill').fillna(method='bfill')
        rank_sum_ret = sum_ret.rank(method='min', pct=True).fillna(method='ffill').fillna(method='bfill')
        part3 = 1.0 + rank_sum_ret
        
        part1_part2 = (part1 * part2).fillna(method='ffill').fillna(method='bfill')
        rank_part1_part2 = part1_part2.rank(method='min', pct=True).fillna(method='ffill').fillna(method='bfill')
        
        alpha = -1.0 * rank_part1_part2 * part3
        return alpha.fillna(method='ffill').fillna(method='bfill')
    
    def alpha026(self):
        """
        (SUM(CLOSE,7)/7-CLOSE+CORR(VWAP,DELAY(CLOSE,5),230))
        """
        n_rows = len(self.df)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        part1 = (self.C.rolling(window=7, min_periods=3).mean() - self.C).fillna(method='ffill').fillna(method='bfill')
        
        if n_rows < 230:
            corr_window = max(30, n_rows // 2)
        else:
            corr_window = 230
        
        close_lag5 = self.C.shift(5)
        part2 = vwap.rolling(window=corr_window, min_periods=max(10, corr_window//5)).corr(close_lag5).fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 + part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha027(self):
        """
        WMA((CLOSE-DELTA(CLOSE,3))/DELAY(CLOSE,3)*100+(CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*100,12)
        """
        part1 = self.C.pct_change(periods=3) * 100.0 + self.C.pct_change(periods=6) * 100.0
        w = np.arange(1, 13)
        return part1.rolling(window=12, min_periods=12).apply(lambda x: np.dot(x, w))
    
    def alpha028(self):
        """
        3*SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
        -2*SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)
        """
        part1 = self.C - self.C.rolling(window=9, min_periods=9).min()
        part2 = self.H.rolling(window=9, min_periods=9).max() - self.L.rolling(window=9, min_periods=9).min()
        rsv = part1 / part2 * 100
        sma1 = self._sma(rsv, 3, 1)
        sma2 = self._sma(sma1, 3, 1)
        return 3 * sma1 - 2 * sma2
    
    def alpha029(self):
        """
        (CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*VOLUME
        """
        return self.C.pct_change(periods=6) * self.V
    
    def alpha030(self):
        """
        WMA((REGRESI(RET,MKT,SMB,HML,60))^2,20)
        单只股票版本：使用市场指数作为基准
        """
        ret = self.C.pct_change().fillna(0.0)
        if 'index_close' in self.df.columns:
            mkt_ret = self.df['index_close'].pct_change().fillna(0.0)
        else:
            mkt_ret = ret.rolling(window=20, min_periods=20).mean().fillna(0.0)
        
        smb_ret = pd.Series(0, index=ret.index)
        hml_ret = pd.Series(0, index=ret.index)
        
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(60, len(self.df)):
            y = ret.iloc[i-60:i]
            X = pd.DataFrame({
                'const': 1,
                'mkt': mkt_ret.iloc[i-60:i],
                'smb': smb_ret.iloc[i-60:i],
                'hml': hml_ret.iloc[i-60:i]
            }).dropna()
            y = y.loc[X.index]
            if len(y) >= 20:
                try:
                    result.iloc[i] = sm.OLS(y, X).fit().resid.iloc[-1]
                except:
                    result.iloc[i] = np.nan
            else:
                result.iloc[i] = np.nan
        
        w = np.arange(1, 21) / np.arange(1, 21).sum()
        return (result ** 2).rolling(window=20, min_periods=20).apply(lambda x: np.dot(x, w))
    
    def alpha031(self):
        """
        (CLOSE-MEAN(CLOSE,12))/MEAN(CLOSE,12)*100
        """
        ma = self.C.rolling(window=12, min_periods=12).mean()
        return (self.C / ma - 1.0) * 100
    
    def alpha032(self):
        """
        (-1*SUM(RANK(CORR(RANK(HIGH),RANK(VOLUME),3)),3))
        """
        part1 = self.H.rank(pct=True).rolling(window=3, min_periods=3).corr(self.V.rank(pct=True))
        return -1 * part1.rank(pct=True).rolling(window=3, min_periods=3).sum()
    
    def alpha033(self):
        """
        (-1*TSMIN(LOW,5)+DELAY(TSMIN(LOW,5),5))*RANK((SUM(RET,240)-SUM(RET,20))/220)*TSRANK(VOLUME,5)
        """
        n_rows = len(self.df)
        if n_rows < 10:
            return pd.Series(0, index=self.df.index)
        
        self.V = self.V.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill')
        
        low_min5 = self.L.rolling(window=5, min_periods=3).min().fillna(method='ffill').fillna(method='bfill')
        part1 = -1 * low_min5.diff(5).fillna(0)
        
        if n_rows < 240:
            sum_window1 = min(240, n_rows - 5)
            sum_window2 = min(20, n_rows // 3)
        else:
            sum_window1 = 240
            sum_window2 = 20
        
        ret = self.C.pct_change().fillna(0)
        sum_ret1 = ret.rolling(window=sum_window1, min_periods=max(5, sum_window1//10)).sum().fillna(method='ffill').fillna(method='bfill')
        sum_ret2 = ret.rolling(window=sum_window2, min_periods=max(3, sum_window2//5)).sum().fillna(method='ffill').fillna(method='bfill')
        
        part2_series = ((sum_ret1 - sum_ret2) / 220).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_series.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        part3 = self._tsrank_fixed(self.V, 5).fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 * part2 * part3).fillna(0)
        return alpha
    
    def alpha034(self):
        """
        MEAN(CLOSE,12)/CLOSE
        """
        return self.C.rolling(window=12, min_periods=12).mean() / self.C
    
    def alpha035(self):
        """
        (MIN(RANK(DECAYLINEAR(DELTA(OPEN,1),15)),RANK(DECAYLINEAR(CORR(VOLUME,OPEN*0.65+CLOSE*0.35,17),7)))*-1)
        """
        w7 = np.arange(1, 8)
        w15 = np.arange(1, 16)
        part1 = self.O.diff().rolling(window=15, min_periods=15).apply(lambda x: np.dot(x, w15)).rank(pct=True)
        part2 = (self.O * 0.65 + self.C * 0.35).rolling(window=17, min_periods=17).corr(self.V)
        part2 = part2.rolling(window=7, min_periods=7).apply(lambda x: np.dot(x, w7)).rank(pct=True)
        return np.minimum(part1, part2) * (-1)
    
    def alpha036(self):
        """
        RANK(SUM(CORR(RANK(VOLUME),RANK(VWAP),6),2))
        """
        self.V = self.V.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill')
        vol_rank = self.V.rank(pct=True, method='min')
        vwap_rank = vwap.rank(pct=True, method='min')
        part1 = vol_rank.rolling(window=6, min_periods=3).corr(vwap_rank)
        return part1.rolling(window=2, min_periods=1).sum().rank(pct=True, method='min')
    
    def alpha037(self):
        """
        (-1*RANK(SUM(OPEN,5)*SUM(RET,5)-DELAY(SUM(OPEN,5)*SUM(RET,5),10)))
        """
        part1 = self.O.rolling(window=5, min_periods=5).sum() * self.C.pct_change().rolling(window=5, min_periods=5).sum()
        return -1 * part1.diff(10)
    
    def alpha038(self):
        """
        ((SUM(HIGH,20)/20)<HIGH)?(-1*DELTA(HIGH,2)):0
        """
        condition = self.H.rolling(window=20, min_periods=20).mean() < self.H
        alpha = -1 * self.H.diff(2)
        alpha[~condition] = 0.0
        return alpha
    
    def alpha039(self):
        """
        (RANK(DECAYLINEAR(DELTA(CLOSE,2),8))-RANK(DECAYLINEAR(CORR(VWAP*0.3+OPEN*0.7,SUM(MEAN(VOLUME,180),37),14),12)))*-1
        使用填充版本
        """
        n_rows = len(self.df)
        if n_rows < 200:
            return self._alpha039_small_data()
        
        w8 = np.arange(1, 9)
        w12 = np.arange(1, 13)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        parta = vwap * 0.3 + self.O * 0.7
        V_filled = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(180, n_rows // 2)
        vol_min_periods = min(vol_window, max(10, vol_window // 10))
        vol_ma = V_filled.rolling(window=vol_window, min_periods=vol_min_periods).mean().fillna(method='ffill').fillna(method='bfill')
        
        sum_window = min(37, n_rows // 4)
        sum_min_periods = min(sum_window, max(5, sum_window // 4))
        partb = vol_ma.rolling(window=sum_window, min_periods=sum_min_periods).sum().fillna(method='ffill').fillna(method='bfill')
        
        part1 = self.C.diff(2).fillna(0)
        decay_window1 = 8
        decay_min_periods1 = min(decay_window1, max(3, decay_window1 // 2))
        part1_decay = part1.rolling(window=decay_window1, min_periods=decay_min_periods1).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= decay_min_periods1 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        corr_window = min(14, n_rows // 8)
        corr_min_periods = min(corr_window, max(3, corr_window // 2))
        part2_corr = parta.rolling(window=corr_window, min_periods=corr_min_periods).corr(partb).fillna(0)
        
        decay_window2 = min(12, n_rows // 8)
        decay_min_periods2 = min(decay_window2, max(3, decay_window2 // 2))
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=decay_min_periods2).apply(
            lambda x: np.dot(x, w12[:len(x)]) if len(x) >= decay_min_periods2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def _alpha039_small_data(self):
        """
        小数据量版本
        """
        n_rows = len(self.df)
        w8 = np.arange(1, 9)
        w12 = np.arange(1, 13)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        parta = vwap * 0.3 + self.O * 0.7
        V_filled = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(30, n_rows // 2)
        vol_min_periods = min(vol_window, max(3, vol_window // 3))
        vol_ma = V_filled.rolling(window=vol_window, min_periods=vol_min_periods).mean().fillna(method='ffill').fillna(method='bfill')
        
        sum_window = min(10, n_rows // 3)
        sum_min_periods = min(sum_window, max(3, sum_window // 2))
        partb = vol_ma.rolling(window=sum_window, min_periods=sum_min_periods).sum().fillna(method='ffill').fillna(method='bfill')
        
        part1 = self.C.diff(2).fillna(0)
        decay_window1 = min(8, n_rows // 3)
        decay_min_periods1 = min(decay_window1, max(2, decay_window1 // 2))
        part1_decay = part1.rolling(window=decay_window1, min_periods=decay_min_periods1).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= decay_min_periods1 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        corr_window = min(8, n_rows // 4)
        corr_min_periods = min(corr_window, max(2, corr_window // 2))
        part2_corr = parta.rolling(window=corr_window, min_periods=corr_min_periods).corr(partb).fillna(0)
        
        decay_window2 = min(8, n_rows // 4)
        decay_min_periods2 = min(decay_window2, max(2, decay_window2 // 2))
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=decay_min_periods2).apply(
            lambda x: np.dot(x, w12[:len(x)]) if len(x) >= decay_min_periods2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha040(self):
        """
        SUM(CLOSE>DELAY(CLOSE,1)?VOLUME:0,26)/SUM(CLOSE<=DELAY(CLOSE,1)?VOLUME:0,26)*100
        """
        diff = self.C.diff()
        part1 = ((diff > 0) * self.V).rolling(window=26, min_periods=26).sum()
        part2 = ((diff <= 0) * self.V).rolling(window=26, min_periods=26).sum()
        return part1 / part2 * 100
    
    def alpha041(self):
        """
        RANK(MAX(DELTA(VWAP,3),5))*-1
        """
        self.V = self.V.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        vwap_diff = vwap.diff(3)
        vwap_max = vwap_diff.rolling(window=5, min_periods=3).max()
        return -1 * vwap_max.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
    
    def alpha042(self):
        """
        (-1*RANK(STD(HIGH,10)))*CORR(HIGH,VOLUME,10)
        """
        part1 = -1 * self.H.rolling(window=10, min_periods=10).std().rank(pct=True)
        part2 = self.H.rolling(window=10, min_periods=10).corr(self.V)
        return part1 * part2
    
    def alpha043(self):
        """
        (SUM(CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0),6))
        """
        diff = self.C.diff()
        part1 = ((diff > 0) * self.V).rolling(window=6, min_periods=6).sum()
        part2 = ((diff < 0) * -self.V).rolling(window=6, min_periods=6).sum()
        return part1 + part2
    
    def alpha044(self):
        """
        (TSRANK(DECAYLINEAR(CORR(LOW,MEAN(VOLUME,10),7),6),4)+TSRANK(DECAYLINEAR(DELTA(VWAP,3),10),15))
        """
        w6 = np.arange(1, 7)
        w10 = np.arange(1, 11)
        self.V = self.V.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        vol_ma = self.V.rolling(window=10, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_ma.rolling(window=7, min_periods=4).corr(self.L).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=6, min_periods=3).apply(
            lambda x: np.dot(x, w6[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = self._tsrank_fixed(part1_decay, 4)
        
        vwap_diff = vwap.diff(3).fillna(0)
        part2_decay = vwap_diff.rolling(window=10, min_periods=5).apply(
            lambda x: np.dot(x, w10[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, 15)
        
        return part1 + part2
    
    def alpha045(self):
        """
        (RANK(DELTA(CLOSE*0.6+OPEN*0.4,1))*RANK(CORR(VWAP,MEAN(VOLUME,150),15)))
        调整版本：根据数据量动态调整窗口
        """
        n_rows = len(self.df)
        vol_window = max(20, n_rows // 3) if n_rows < 150 else 150
        
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        weighted_price = self.C * 0.6 + self.O * 0.4
        part1 = weighted_price.diff().fillna(0).rank(pct=True, method='min')
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vwap.rolling(window=15, min_periods=5).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        return (part1 * part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha046(self):
        """
        (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/(4*CLOSE)
        """
        ma3 = self.C.rolling(window=3, min_periods=3).mean()
        ma6 = self.C.rolling(window=6, min_periods=6).mean()
        ma12 = self.C.rolling(window=12, min_periods=12).mean()
        ma24 = self.C.rolling(window=24, min_periods=24).mean()
        return (ma3 + ma6 + ma12 + ma24) / (4 * self.C)
    
    def alpha047(self):
        """
        SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,9,1)
        """
        high_max = self.H.rolling(window=6, min_periods=6).max()
        low_min = self.L.rolling(window=6, min_periods=6).min()
        part1 = (high_max - self.C) / (high_max - low_min) * 100
        return self._sma(part1, 9, 1)
    
    def alpha048(self):
        """
        -1*RANK(SIGN(CLOSE-DELAY(CLOSE,1))+SIGN(DELAY(CLOSE,1)-DELAY(CLOSE,2))+SIGN(DELAY(CLOSE,2)-DELAY(CLOSE,3)))*SUM(VOLUME,5)/SUM(VOLUME,20)
        """
        diff1 = self.C.diff()
        part1 = (np.sign(diff1) + np.sign(diff1.shift(1)) + np.sign(diff1.shift(2))).rank(pct=True)
        part2 = self.V.rolling(window=5, min_periods=5).sum() / self.V.rolling(window=20, min_periods=20).sum()
        return -1 * part1 * part2
    
    def alpha049(self):
        """
        SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
        (SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)+
        SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
        """
        hl_sum = self.H + self.L
        condition1 = hl_sum >= hl_sum.shift(1)
        condition2 = hl_sum <= hl_sum.shift(1)
        max_abs = np.maximum(abs(self.H.diff()), abs(self.L.diff()))
        
        part1 = max_abs.copy()
        part2 = max_abs.copy()
        part1[condition1] = 0.0
        part2[condition2] = 0.0
        
        sum1 = part1.rolling(window=12, min_periods=12).sum()
        sum2 = part2.rolling(window=12, min_periods=12).sum()
        return sum1 / (sum1 + sum2)
    
    def alpha050(self):
        """
        SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
        (SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)
        +SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
        -SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
        (SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)
        +SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
        """
        hl_sum = self.H + self.L
        condition1 = hl_sum >= hl_sum.shift(1)
        condition2 = hl_sum <= hl_sum.shift(1)
        max_abs = np.maximum(abs(self.H.diff()), abs(self.L.diff()))
        
        part1 = max_abs.copy()
        part2 = max_abs.copy()
        part1[condition2] = 0.0
        part2[condition1] = 0.0
        
        sum1 = part1.rolling(window=12, min_periods=12).sum()
        sum2 = part2.rolling(window=12, min_periods=12).sum()
        return sum1 / (sum1 + sum2) - sum2 / (sum1 + sum2)
    
    def alpha051(self):
        """
        SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)/
        (SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)
        +SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12))
        """
        hl_sum = self.H + self.L
        condition1 = hl_sum <= hl_sum.shift(1)
        condition2 = hl_sum >= hl_sum.shift(1)
        max_abs = np.maximum(abs(self.H.diff()), abs(self.L.diff()))
        
        part1 = max_abs.copy()
        part2 = max_abs.copy()
        part1[condition1] = 0.0
        part2[condition2] = 0.0
        
        sum1 = part1.rolling(window=12, min_periods=12).sum()
        sum2 = part2.rolling(window=12, min_periods=12).sum()
        return sum1 / (sum1 + sum2)
    
    def alpha052(self):
        """
        SUM(MAX(0,HIGH-DELAY((HIGH+LOW+CLOSE)/3,1)),26)/SUM(MAX(0,DELAY((HIGH+LOW+CLOSE)/3,1)-L),26)*100
        """
        ma = (self.H + self.L + self.C) / 3.0
        part1 = np.maximum(0.0, self.H - ma.shift(1)).rolling(window=26, min_periods=26).sum()
        part2 = np.maximum(0.0, ma.shift(1) - self.L).rolling(window=26, min_periods=26).sum()
        return part1 / part2 * 100.0
    
    def alpha053(self):
        """
        COUNT(CLOSE>DELAY(CLOSE,1),12)/12*100
        """
        return (self.C.diff() > 0.0).rolling(window=12, min_periods=12).sum() / 12.0 * 100
    
    def alpha054(self):
        """
        (-1*RANK(STD(ABS(CLOSE-OPEN))+CLOSE-OPEN+CORR(CLOSE,OPEN,10)))
        """
        part1 = abs(self.C - self.O).rolling(window=10, min_periods=10).std() + self.C - self.O + self.C.rolling(window=10, min_periods=10).corr(self.O)
        return -1 * part1.rank(pct=True)
    
    def alpha055(self):
        """
        SUM(16*(CLOSE+(CLOSE-OPEN)/2-DELAY(OPEN,1))/
        ((ABS(HIGH-DELAY(CLOSE,1))>ABS(LOW-DELAY(CLOSE,1)) & ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) ? 
        ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
        (ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) & ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1)) ?
        ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
        ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4)))
        *MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1))),20)
        """
        part1 = self.C * 1.5 - self.O * 0.5 - self.O.shift(1)
        part2 = abs(self.H - self.C.shift(1)) + abs(self.L - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        
        condition1 = np.logical_and(
            abs(self.H - self.C.shift(1)) > abs(self.L - self.C.shift(1)),
            abs(self.H - self.C.shift(1)) > abs(self.H - self.L.shift(1))
        )
        condition2 = np.logical_and(
            abs(self.L - self.C.shift(1)) > abs(self.H - self.L.shift(1)),
            abs(self.L - self.C.shift(1)) > abs(self.H - self.C.shift(1))
        )
        
        part2[~condition1 & condition2] = abs(self.L - self.C.shift(1)) + abs(self.H - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        part2[~condition1 & ~condition2] = abs(self.H - self.L.shift(1)) + abs(self.C - self.O).shift(1) / 4.0
        
        part3 = np.maximum(abs(self.H - self.C.shift(1)), abs(self.L - self.C.shift(1)))
        alpha = (part1 / part2 * part3 * 16.0).rolling(window=20, min_periods=20).sum()
        return alpha
    
    def alpha056(self):
        """
        RANK(OPEN-TSMIN(OPEN,12))<RANK(RANK(CORR(SUM((HIGH +LOW)/2,19),SUM(MEAN(VOLUME,40),19),13))^5)
        """
        part1 = (self.O - self.O.rolling(window=12, min_periods=12).min()).rank(pct=True)
        t1 = (self.H * 0.5 + self.L * 0.5).rolling(window=19, min_periods=19).sum()
        t2 = self.V.rolling(window=40, min_periods=40).mean().rolling(window=19, min_periods=19).sum()
        part2 = (t1.rolling(window=13, min_periods=13).corr(t2).rank(pct=True) ** 5).rank(pct=True)
        return part2 - part1
    
    def alpha057(self):
        """
        SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
        """
        part1 = self.C - self.C.rolling(window=9, min_periods=9).min()
        part2 = self.H.rolling(window=9, min_periods=9).max() - self.L.rolling(window=9, min_periods=9).min()
        rsv = part1 / part2 * 100
        return self._sma(rsv, 3, 1)
    
    def alpha058(self):
        """
        COUNT(CLOSE>DELAY(CLOSE,1),20)/20*100
        """
        return (self.C.diff() > 0.0).rolling(window=20, min_periods=20).sum() / 20.0 * 100
    
    def alpha059(self):
        """
        SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),20)
        """
        alpha = self.C.copy()
        diff = self.C.diff()
        condition1 = diff > 0.0
        condition2 = diff < 0.0
        
        alpha[condition1] = self.C[condition1] - np.minimum(self.L[condition1], self.C.shift(1)[condition1])
        alpha[condition2] = self.C[condition2] - np.maximum(self.H[condition2], self.C.shift(1)[condition2])
        alpha[diff == 0] = 0.0
        
        return alpha.rolling(window=20, min_periods=20).sum()
    
    def alpha060(self):
        """
        SUM((2*CLOSE-LOW-HIGH)/(HIGH-LOW)*VOLUME,20)
        """
        price_range = (self.H - self.L).replace(0, 1e-10)
        numerator = 2 * self.C - self.L - self.H
        ratio = numerator / price_range
        part1 = (ratio * self.V).fillna(method='ffill').fillna(method='bfill')
        alpha = part1.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha061(self):
        """
        MAX(RANK(DECAYLINEAR(DELTA(VWAP,1),12)),RANK(DECAYLINEAR(RANK(CORR(LOW,MEAN(VOLUME,80),8)),17)))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        w12 = np.arange(1, 13)
        vwap_diff = vwap.diff().fillna(0)
        part1_decay = vwap_diff.rolling(window=12, min_periods=6).apply(
            lambda x: np.dot(x, w12[:len(x)]) if len(x) >= 6 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(80, len(self.df) // 2)
        turnover_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = turnover_ma.rolling(window=8, min_periods=4).corr(self.L).fillna(method='ffill').fillna(method='bfill')
        part2_rank = part2_corr.rank(pct=True, method='min')
        
        w17 = np.arange(1, 18)
        part2_decay = part2_rank.rolling(window=17, min_periods=8).apply(
            lambda x: np.dot(x, w17[:len(x)]) if len(x) >= 8 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha062(self):
        """
        -1*CORR(HIGH,RANK(VOLUME),5)
        """
        return -1 * self.V.rank(pct=True).rolling(window=5, min_periods=5).corr(self.H)
    
    def alpha063(self):
        """
        SMA(MAX(CLOSE-DELAY(CLOSE,1),0),6,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),6,1)*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 6, 1)
        sma2 = self._sma(part2, 6, 1)
        return sma1 / sma2 * 100.0
    
    def alpha064(self):
        """
        (MAX(RANK(DECAYLINEAR(CORR(RANK(VWAP),RANK(VOLUME),4),4)),RANK(DECAYLINEAR(MAX(CORR(RANK(CLOSE),RANK(MEAN(VOLUME,60)),4),13),14)))*-1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w4 = np.arange(1, 5)
        w14 = np.arange(1, 15)
        
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        
        part1_corr = vwap_rank.rolling(window=4, min_periods=3).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=4, min_periods=3).apply(
            lambda x: np.dot(x, w4[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(60, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        vol_ma_rank = vol_ma.rank(pct=True, method='min')
        close_rank = self.C.rank(pct=True, method='min')
        
        part2_corr = close_rank.rolling(window=4, min_periods=3).corr(vol_ma_rank).fillna(method='ffill').fillna(method='bfill')
        part2_max = part2_corr.rolling(window=13, min_periods=7).max().fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_max.rolling(window=14, min_periods=7).apply(
            lambda x: np.dot(x, w14[:len(x)]) if len(x) >= 7 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha065(self):
        """
        MEAN(CLOSE,6)/CLOSE
        """
        return self.C.rolling(window=6, min_periods=6).mean() / self.C
    
    def alpha066(self):
        """
        (CLOSE-MEAN(CLOSE,6))/MEAN(CLOSE,6)*100
        """
        ma = self.C.rolling(window=6, min_periods=6).mean()
        return (self.C - ma) / ma * 100
    
    def alpha067(self):
        """
        SMA(MAX(CLOSE-DELAY(CLOSE,1),0),24,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),24,1)*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 24, 1)
        sma2 = self._sma(part2, 24, 1)
        return sma1 / sma2 * 100
    
    def alpha068(self):
        """
        SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,15,2)
        """
        part1 = (self.H.diff() * 0.5 + self.L.diff() * 0.5) * (self.H - self.L) / self.V
        return self._sma(part1, 15, 2)
    
    def alpha069(self):
        """
        (SUM(DTM,20)>SUM(DBM,20)?(SUM(DTM,20)-SUM(DBM,20))/SUM(DTM,20):
        (SUM(DTM,20)=SUM(DBM,20)?0:(SUM(DTM,20)-SUM(DBM,20))/SUM(DBM,20)))
        """
        dtm = (self.O.diff() <= 0) * np.maximum(self.H - self.O, self.O.diff())
        dbm = (self.O.diff() >= 0) * np.maximum(self.O - self.L, self.O.diff())
        
        dtm_sum = dtm.rolling(window=20, min_periods=20).sum()
        dbm_sum = dbm.rolling(window=20, min_periods=20).sum()
        
        result = pd.Series(index=self.df.index, dtype=float)
        mask_gt = dtm_sum > dbm_sum
        mask_eq = dtm_sum == dbm_sum
        mask_lt = dtm_sum < dbm_sum
        
        result[mask_gt] = (dtm_sum[mask_gt] - dbm_sum[mask_gt]) / dtm_sum[mask_gt]
        result[mask_eq] = 0.0
        result[mask_lt] = (dtm_sum[mask_lt] - dbm_sum[mask_lt]) / dbm_sum[mask_lt]
        
        return result
    
    def alpha070(self):
        """
        STD(AMOUNT,6)
        """
        return self.AMOUNT.rolling(window=6, min_periods=6).std()
    
    def alpha071(self):
        """
        (CLOSE-MEAN(CLOSE,24))/MEAN(CLOSE,24)*100
        """
        ma = self.C.rolling(window=24, min_periods=24).mean()
        return (self.C - ma) / ma * 100
    
    def alpha072(self):
        """
        SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,15,1)
        """
        high_max = self.H.rolling(window=6, min_periods=6).max()
        low_min = self.L.rolling(window=6, min_periods=6).min()
        part1 = (high_max - self.C) / (high_max - low_min) * 100.0
        return self._sma(part1, 15, 1)
    
    def alpha073(self):
        """
        ((TSRANK(DECAYLINEAR(DECAYLINEAR(CORR(CLOSE,VOLUME,10),16),4),5)-RANK(DECAYLINEAR(CORR(VWAP,MEAN(VOLUME,30),4),3)))*-1)
        ETF专用版本
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        def normalize(series):
            return (series - series.min()) / (series.max() - series.min() + 1e-10)
        
        part1_corr = self.C.rolling(window=10, min_periods=5).corr(self.V).fillna(method='ffill').fillna(method='bfill')
        part1_ema1 = part1_corr.ewm(span=16, adjust=False, min_periods=5).mean()
        part1_ema2 = part1_ema1.ewm(span=4, adjust=False, min_periods=3).mean()
        part1 = normalize(part1_ema2)
        
        vol_window = min(30, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vwap.rolling(window=4, min_periods=3).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        
        w3 = np.arange(1, 4) / np.arange(1, 4).sum()
        part2 = part2_corr.rolling(window=3, min_periods=2).apply(
            lambda x: np.sum(x * w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = normalize(part2)
        
        return -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha074(self):
        """
        RANK(CORR(SUM(LOW*0.35+VWAP*0.65,20),SUM(MEAN(VOLUME,40),20),7))+RANK(CORR(RANK(VWAP),RANK(VOLUME),6))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        weighted_price = self.L * 0.35 + vwap * 0.65
        sum1 = weighted_price.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(40, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//8)).mean().fillna(method='ffill').fillna(method='bfill')
        sum2 = vol_ma.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        
        part1_corr = sum1.rolling(window=7, min_periods=4).corr(sum2).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min')
        
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        part2_corr = vwap_rank.rolling(window=6, min_periods=4).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        return (part1 + part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha075(self):
        """
        COUNT(CLOSE>OPEN & BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN,50)/COUNT(BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN,50)
        使用指数数据
        """
        n_rows = len(self.df)
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'open' in index_data.columns:
                index_open = index_data['open']
            else:
                index_open = index_close.shift(1).fillna(index_close)
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                close_map = dict(zip(index_data['date'], index_close))
                open_map = dict(zip(index_data['date'], index_open))
                bm_close = self.df['date'].map(close_map).fillna(method='ffill').fillna(method='bfill')
                bm_open = self.df['date'].map(open_map).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
                bm_open = index_open.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
            bm_open = self.O.rolling(window=20, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        
        bm_down = bm_close < bm_open
        stock_up = self.C > self.O
        condition = stock_up & bm_down
        
        if condition.sum() == 0:
            bm_ret = bm_close.pct_change().fillna(0)
            bm_down_ret = bm_ret < 0
            condition = stock_up & bm_down_ret
            bm_down = bm_down_ret
        
        window = min(50, n_rows // 2)
        min_periods = max(5, window // 3)
        
        numerator = condition.rolling(window=window, min_periods=min_periods).sum()
        denominator = bm_down.rolling(window=window, min_periods=min_periods).sum().replace(0, np.nan)
        alpha = (numerator / denominator).fillna(method='ffill').fillna(method='bfill').fillna(0)
        
        return alpha
    
    def alpha076(self):
        """
        STD(ABS(CLOSE/DELAY(CLOSE,1)-1)/VOLUME,20)/MEAN(ABS(CLOSE/DELAY(CLOSE,1)-1)/VOLUME,20)
        """
        self.V = self.V.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill')
        ret = self.C.pct_change().fillna(0).replace([np.inf, -np.inf], 0)
        ret_vol = (abs(ret) / self.V).fillna(method='ffill').fillna(method='bfill')
        std = ret_vol.rolling(window=20, min_periods=10).std()
        mean = ret_vol.rolling(window=20, min_periods=10).mean().replace(0, np.nan)
        alpha = (std / mean).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha077(self):
        """
        MIN(RANK(DECAYLINEAR(HIGH*0.5+LOW*0.5-VWAP,20)),RANK(DECAYLINEAR(CORR(HIGH*0.5+LOW*0.5,MEAN(VOLUME,40),3),6)))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w6 = np.arange(1, 7)
        w20 = np.arange(1, 21)
        
        hl_avg = self.H * 0.5 + self.L * 0.5
        part1_series = hl_avg - vwap
        part1_decay = part1_series.rolling(window=20, min_periods=10).apply(
            lambda x: np.dot(x, w20[:len(x)]) if len(x) >= 10 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(40, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//8)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = hl_avg.rolling(window=3, min_periods=2).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_corr.rolling(window=6, min_periods=3).apply(
            lambda x: np.dot(x, w6[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return np.minimum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha078(self):
        """
        ((HIGH+LOW+CLOSE)/3-MA((HIGH+LOW+CLOSE)/3,12))/(0.015*MEAN(ABS(CLOSE-MEAN((HIGH+LOW+CLOSE)/3,12)),12))
        """
        tp = (self.H + self.L + self.C) / 3
        tp_ma = tp.rolling(window=12, min_periods=12).mean()
        part1 = tp - tp_ma
        part2 = abs(self.C - tp_ma).rolling(window=12, min_periods=12).mean() * 0.015
        return part1 / part2
    
    def alpha079(self):
        """
        SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 12, 1)
        sma2 = self._sma(part2, 12, 1)
        return sma1 / sma2 * 100
    
    def alpha080(self):
        """
        (VOLUME-DELAY(VOLUME,5))/DELAY(VOLUME,5)*100
        """
        return self.V.pct_change(periods=5) * 100.0
    
    def alpha081(self):
        """
        SMA(VOLUME,21,2)
        """
        return self._sma(self.V, 21, 2)
    
    def alpha082(self):
        """
        SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,20,1)
        """
        high_max = self.H.rolling(window=6, min_periods=6).max()
        low_min = self.L.rolling(window=6, min_periods=6).min()
        part1 = (high_max - self.C) / (high_max - low_min) * 100
        return self._sma(part1, 20, 1)
    
    def alpha083(self):
        """
        (-1*RANK(COVIANCE(RANK(HIGH),RANK(VOLUME),5)))
        """
        alpha = self.H.rank(pct=True).rolling(window=5, min_periods=5).cov(self.V.rank(pct=True))
        return -1 * alpha.rank(pct=True)
    
    def alpha084(self):
        """
        SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),20)
        """
        part1 = np.sign(self.C.diff()) * self.V
        return part1.rolling(window=20, min_periods=20).sum()
    
    def alpha085(self):
        """
        TSRANK(VOLUME/MEAN(VOLUME,20),20)*TSRANK(-1*DELTA(CLOSE,7),8)
        """
        part1 = self.V / self.V.rolling(window=20, min_periods=20).mean()
        part1 = self._tsrank(part1, 20)
        part2 = -1 * self.C.diff(7)
        part2 = self._tsrank(part2, 8)
        return part1 * part2
    
    def alpha086(self):
        """
        ((0.25<((DELAY(CLOSE,20)-DELAY(CLOSE,10))/10-(DELAY(CLOSE,10)-CLOSE)/10))?-1:((((DELAY(CLOSE,20)-DELAY(CLOSE,10))/10-(DELAY(CLOSE,10)-CLOSE)/10)<0)?1:(DELAY(CLOSE,1)-CLOSE)))
        """
        part = (self.C.shift(20) - self.C.shift(10)) / 10 - (self.C.shift(10) - self.C) / 10
        condition1 = part > 0.25
        condition2 = part < 0.0
        
        alpha = pd.Series(index=self.df.index, dtype=float)
        alpha[condition1] = -1.0
        alpha[~condition1 & condition2] = 1.0
        alpha[~condition1 & ~condition2] = self.C.shift(1) - self.C
        
        return alpha
    
    def alpha087(self):
        """
        (RANK(DECAYLINEAR(DELTA(VWAP,4),7))+TSRANK(DECAYLINEAR((LOW-VWAP)/(OPEN-(HIGH+LOW)/2),11),7))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w7 = np.arange(1, 8)
        w11 = np.arange(1, 12)
        
        vwap_diff = vwap.diff(4).fillna(0)
        part1_decay = vwap_diff.rolling(window=7, min_periods=4).apply(
            lambda x: np.dot(x, w7[:len(x)]) if len(x) >= 4 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        hl_avg = (self.H + self.L) / 2
        denominator = self.O - hl_avg
        denominator = denominator.replace(0, 1e-10)
        mask_small = abs(denominator) < 1e-8
        denominator[mask_small] = 1e-10 * np.sign(denominator[mask_small])
        
        part2_series = (self.L - vwap) / denominator
        part2_series = part2_series.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        
        part2_decay = part2_series.rolling(window=11, min_periods=6).apply(
            lambda x: np.dot(x, w11[:len(x)]) if len(x) >= 6 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, 7)
        
        return -1 * (part1 + part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha088(self):
        """
        (CLOSE-DELAY(CLOSE,20))/DELAY(CLOSE,20)*100
        """
        return self.C.pct_change(periods=20) * 100
    
    def alpha089(self):
        """
        2*(SMA(CLOSE,13,2)-SMA(CLOSE,27,2)-SMA(SMA(CLOSE,13,2)-SMA(CLOSE,27,2),10,2))
        """
        sma13 = self._sma(self.C, 13, 2)
        sma27 = self._sma(self.C, 27, 2)
        part = sma13 - sma27
        return 2.0 * (part - self._sma(part, 10, 2))
    
    def alpha090(self):
        """
        (RANK(CORR(RANK(VWAP),RANK(VOLUME),5))*-1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        corr = vwap_rank.rolling(window=5, min_periods=3).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        alpha = -1 * corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        return alpha
    
    def alpha091(self):
        """
        ((RANK(CLOSE-MAX(CLOSE,5))*RANK(CORR(MEAN(VOLUME,40),LOW,5)))*-1)
        """
        part1 = (self.C - self.C.rolling(window=5, min_periods=5).max()).rank(pct=True)
        part2 = self.V.rolling(window=40, min_periods=40).mean().rolling(window=5, min_periods=5).corr(self.L).rank(pct=True)
        return -1 * part1 * part2
    
    def alpha092(self):
        """
        (MAX(RANK(DECAYLINEAR(DELTA(CLOSE*0.35+VWAP*0.65,2),3)),TSRANK(DECAYLINEAR(ABS(CORR((MEAN(VOLUME,180)),CLOSE,13)),5),15))*-1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w3 = np.arange(1, 4)
        w5 = np.arange(1, 6)
        
        weighted_price = self.C * 0.35 + vwap * 0.65
        weighted_diff = weighted_price.diff(2).fillna(0)
        part1_decay = weighted_diff.rolling(window=3, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(180, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vol_ma.rolling(window=13, min_periods=7).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part2_abs = abs(part2_corr)
        part2_decay = part2_abs.rolling(window=5, min_periods=3).apply(
            lambda x: np.dot(x, w5[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, 15)
        
        return -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha093(self):
        """
        SUM(OPEN>=DELAY(OPEN,1)?0:MAX(OPEN-LOW,OPEN-DELAY(OPEN,1)),20)
        """
        condition = self.O.diff() >= 0.0
        alpha = np.maximum(self.O - self.L, self.O.diff())
        alpha[condition] = 0.0
        return alpha.rolling(window=20, min_periods=20).sum()
    
    def alpha094(self):
        """
        SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),30)
        """
        part1 = np.sign(self.C.diff()) * self.V
        return part1.rolling(window=30, min_periods=30).sum()
    
    def alpha095(self):
        """
        STD(AMOUNT,20)
        """
        return self.AMOUNT.rolling(window=20, min_periods=20).std()
    
    def alpha096(self):
        """
        SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)
        """
        part1 = self.C - self.C.rolling(window=9, min_periods=9).min()
        part2 = self.H.rolling(window=9, min_periods=9).max() - self.L.rolling(window=9, min_periods=9).min()
        rsv = part1 / part2 * 100
        sma1 = self._sma(rsv, 3, 1)
        return self._sma(sma1, 3, 1)
    
    def alpha097(self):
        """
        STD(VOLUME,10)
        """
        return self.V.rolling(window=10, min_periods=10).std()
    
    def alpha098(self):
        """
        (DELTA(SUM(CLOSE,100)/100,100)/DELAY(CLOSE,100)<=0.05)?(-1*(CLOSE-TSMIN(CLOSE,100))):(-1*DELTA(CLOSE,3))
        """
        condition1 = self.C.rolling(window=100, min_periods=100).mean().diff(100) / self.C.shift(100) <= 0.05
        alpha = pd.Series(index=self.df.index, dtype=float)
        alpha[condition1] = -1 * (self.C - self.C.rolling(window=100, min_periods=100).min())
        alpha[~condition1] = -1 * self.C.diff(3)
        return alpha
    
    def alpha099(self):
        """
        (-1*RANK(COVIANCE(RANK(CLOSE),RANK(VOLUME),5)))
        """
        alpha = self.C.rank(pct=True).rolling(window=5, min_periods=5).cov(self.V.rank(pct=True))
        return -1 * alpha.rank(pct=True)
    
    def alpha100(self):
        """
        STD(VOLUME,20)
        """
        return self.V.rolling(window=20, min_periods=20).std()
    
    def alpha101(self):
        """
        (RANK(CORR(CLOSE,SUM(MEAN(VOLUME,30),37),15)) < RANK(CORR(RANK(HIGH*0.1+VWAP*0.9),RANK(VOLUME),11)))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(30, len(self.df) // 3)
        sum_window = min(37, len(self.df) // 3)
        corr_window = min(15, len(self.df) // 4)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        vol_sum = vol_ma.rolling(window=sum_window, min_periods=max(5, sum_window//6)).sum().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_sum.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min')
        
        weighted_price = self.H * 0.1 + vwap * 0.9
        weighted_rank = weighted_price.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        corr_window2 = min(11, len(self.df) // 4)
        part2_corr = weighted_rank.rolling(window=corr_window2, min_periods=max(4, corr_window2//3)).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        return -1 * (part2 - part1).fillna(method='ffill').fillna(method='bfill')
    
    def alpha102(self):
        """
        SMA(MAX(VOLUME-DELAY(VOLUME,1),0),6,1)/SMA(ABS(VOLUME-DELAY(VOLUME,1)),6,1)*100
        """
        diff = self.V.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 6, 1)
        sma2 = self._sma(part2, 6, 1)
        return sma1 / sma2 * 100
    
    def alpha103(self):
        """
        ((20-LOWDAY(LOW,20))/20)*100
        """
        def lowday(x):
            return 19 - x.argmin() if len(x) == 20 else np.nan
        return (20 - self.L.rolling(window=20, min_periods=20).apply(lowday)) / 20 * 100
    
    def alpha104(self):
        """
        -1*(DELTA(CORR(HIGH,VOLUME,5),5)*RANK(STD(CLOSE,20)))
        """
        part1 = self.H.rolling(window=5, min_periods=5).corr(self.V).diff(5)
        part2 = self.C.rolling(window=20, min_periods=20).std().rank(pct=True)
        return -1 * part1 * part2
    
    def alpha105(self):
        """
        -1*CORR(RANK(OPEN),RANK(VOLUME),10)
        """
        return -1 * self.O.rank(pct=True).rolling(window=10, min_periods=10).corr(self.V.rank(pct=True))
    
    def alpha106(self):
        """
        CLOSE-DELAY(CLOSE,20)
        """
        return self.C.diff(20)
    
    def alpha107(self):
        """
        (-1*RANK(OPEN-DELAY(HIGH,1)))*RANK(OPEN-DELAY(CLOSE,1))*RANK(OPEN-DELAY(LOW,1))
        """
        part1 = -1 * (self.O - self.H.shift(1)).rank(pct=True)
        part2 = (self.O - self.C.shift(1)).rank(pct=True)
        part3 = (self.O - self.L.shift(1)).rank(pct=True)
        return part1 * part2 * part3
    
    def alpha108(self):
        """
        (RANK(HIGH-MIN(HIGH,2))^RANK(CORR(VWAP,MEAN(VOLUME,120),6)))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        high_min = self.H.rolling(window=2, min_periods=1).min()
        part1 = (self.H - high_min).rank(pct=True, method='min')
        
        vol_window = min(120, len(self.df) // 2)
        corr_window = min(6, len(self.df) // 6)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vwap.rolling(window=corr_window, min_periods=max(3, corr_window//2)).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        alpha = pd.Series(index=self.df.index, dtype=float)
        for i in range(len(self.df)):
            p1 = part1.iloc[i]
            p2 = part2.iloc[i]
            if pd.notna(p1) and pd.notna(p2):
                p1 = max(0.001, min(p1, 0.999))
                try:
                    alpha.iloc[i] = -(p1 ** p2)
                except:
                    alpha.iloc[i] = np.nan
            else:
                alpha.iloc[i] = np.nan
        
        return alpha.fillna(method='ffill').fillna(method='bfill')
    
    def alpha109(self):
        """
        SMA(HIGH-LOW,10,2)/SMA(SMA(HIGH-LOW,10,2),10,2)
        """
        hl = self.H - self.L
        sma = self._sma(hl, 10, 2)
        return sma / self._sma(sma, 10, 2)
    
    def alpha110(self):
        """
        SUM(MAX(0,HIGH-DELAY(CLOSE,1)),20)/SUM(MAX(0,DELAY(CLOSE,1)-LOW),20)*100
        """
        part1 = np.maximum(self.H - self.C.shift(1), 0.0).rolling(window=20, min_periods=20).sum()
        part2 = np.maximum(self.C.shift(1) - self.L, 0.0).rolling(window=20, min_periods=20).sum()
        return part1 / part2 * 100.0
    
    def alpha111(self):
        """
        SMA(VOL*(2*CLOSE-LOW-HIGH)/(HIGH-LOW),11,2)-SMA(VOL*(2*CLOSE-LOW-HIGH)/(HIGH-LOW),4,2)
        """
        win_vol = self.V * (2 * self.C - self.L - self.H) / (self.H - self.L)
        return self._sma(win_vol, 11, 2) - self._sma(win_vol, 4, 2)
    
    def alpha112(self):
        """
        (SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)-SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))
        /(SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)+SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0).rolling(window=12, min_periods=12).sum()
        part2 = abs(np.minimum(diff, 0.0)).rolling(window=12, min_periods=12).sum()
        return (part1 - part2) / (part1 + part2) * 100
    
    def alpha113(self):
        """
        -1*RANK(SUM(DELAY(CLOSE,5),20)/20)*CORR(CLOSE,VOLUME,2)*RANK(CORR(SUM(CLOSE,5),SUM(CLOSE,20),2))
        """
        self.V = self.V.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill')
        
        part1_series = self.C.shift(5).rolling(window=20, min_periods=10).mean().fillna(method='ffill').fillna(method='bfill')
        part1 = part1_series.rank(pct=True, method='min')
        
        part2 = self.C.rolling(window=2, min_periods=2).corr(self.V).fillna(method='ffill').fillna(method='bfill').clip(-1, 1)
        
        sum5 = self.C.rolling(window=5, min_periods=3).sum().fillna(method='ffill').fillna(method='bfill')
        sum20 = self.C.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        part3_corr = sum5.rolling(window=2, min_periods=2).corr(sum20).fillna(method='ffill').fillna(method='bfill').clip(-1, 1)
        part3 = part3_corr.rank(pct=True, method='min')
        
        return -1 * part1 * part2 * part3
    
    def alpha114(self):
        """
        RANK(DELAY((HIGH-LOW)/(SUM(CLOSE,5)/5),2))*RANK(RANK(VOLUME))/((HIGH-LOW)/(SUM(CLOSE,5)/5)/(VWAP-CLOSE))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        hl = self.H - self.L
        close_ma5 = self.C.rolling(window=5, min_periods=3).mean().fillna(method='ffill').fillna(method='bfill')
        hl_ma = (hl / close_ma5).fillna(method='ffill').fillna(method='bfill')
        
        part1 = hl_ma.shift(2).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        vol_rank1 = self.V.rank(pct=True, method='min')
        part2 = vol_rank1.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        vwap_close_diff = vwap - self.C
        threshold = 0.0001
        mask_small = abs(vwap_close_diff) < threshold
        vwap_close_diff[mask_small] = threshold * np.sign(vwap_close_diff[mask_small])
        vwap_close_diff = vwap_close_diff.replace(0, threshold)
        part3 = (hl_ma / vwap_close_diff).fillna(method='ffill').fillna(method='bfill')
        part3 = part3.clip(lower=part3.quantile(0.01), upper=part3.quantile(0.99))
        
        alpha = (part1 * part2 / part3).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha115(self):
        """
        (RANK(CORR(HIGH*0.9+CLOSE*0.1,MEAN(VOLUME,30),10))^RANK(CORR(TSRANK((HIGH+LOW)/2,4),TSRANK(VOLUME,10),7)))
        """
        part1 = (self.H * 0.9 + self.C * 0.1).rolling(window=10, min_periods=10).corr(
            self.V.rolling(window=30, min_periods=30).mean()
        ).rank(pct=True)
        part2 = self._tsrank((self.H + self.L) / 2, 4)
        part2 = part2.rolling(window=7, min_periods=7).corr(self._tsrank(self.V, 10)).rank(pct=True)
        return part1 ** part2
    
    def alpha116(self):
        """
        REGBETA(CLOSE,SEQUENCE,20)
        """
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(20, len(self.df)):
            y = self.C.iloc[i-20:i]
            x = np.arange(1, 21)
            result.iloc[i] = self._regbeta(y, x)
        return result.fillna(0)
    
    def alpha117(self):
        """
        TSRANK(VOLUME,32)*(1-TSRANK(CLOSE+HIGH-LOW,16))*(1-TSRANK(RET,32))
        """
        part1 = self._tsrank(self.V, 32)
        part2 = 1.0 - self._tsrank(self.C + self.H - self.L, 16)
        part3 = 1.0 - self._tsrank(self.C.pct_change(), 32)
        return part1 * part2 * part3
    
    def alpha118(self):
        """
        SUM(HIGH-OPEN,20)/SUM(OPEN-LOW,20)*100
        """
        part1 = (self.H - self.O).rolling(window=20, min_periods=20).sum()
        part2 = (self.O - self.L).rolling(window=20, min_periods=20).sum()
        return part1 / part2 * 100.0
    
    def alpha119(self):
        """
        RANK(DECAYLINEAR(CORR(VWAP,SUM(MEAN(VOLUME,5),26),5),7))-RANK(DECAYLINEAR(TSRANK(MIN(CORR(RANK(OPEN),RANK(MEAN(VOLUME,15)),21),9),7),8))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w7 = np.arange(1, 8)
        w8 = np.arange(1, 9)
        
        vol_ma5 = self.V.rolling(window=5, min_periods=3).mean().fillna(method='ffill').fillna(method='bfill')
        sum_window = min(26, len(self.df) // 3)
        corr_window1 = min(5, len(self.df) // 10)
        decay_window1 = min(7, len(self.df) // 10)
        
        vol_sum = vol_ma5.rolling(window=sum_window, min_periods=max(5, sum_window//5)).sum().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_sum.rolling(window=corr_window1, min_periods=max(3, corr_window1//2)).corr(vwap).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=decay_window1, min_periods=max(3, decay_window1//2)).apply(
            lambda x: np.dot(x, w7[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(15, len(self.df) // 3)
        corr_window2 = min(21, len(self.df) // 3)
        min_window = min(9, len(self.df) // 5)
        decay_window2 = min(8, len(self.df) // 5)
        
        vol_ma15 = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//3)).mean().fillna(method='ffill').fillna(method='bfill')
        vol_ma15_rank = vol_ma15.rank(pct=True, method='min')
        open_rank = self.O.rank(pct=True, method='min')
        part2_corr = vol_ma15_rank.rolling(window=corr_window2, min_periods=max(5, corr_window2//4)).corr(open_rank).fillna(method='ffill').fillna(method='bfill')
        part2_min = part2_corr.rolling(window=min_window, min_periods=max(3, min_window//3)).min().fillna(method='ffill').fillna(method='bfill')
        part2_tsrank = self._tsrank_fixed(part2_min, 7)
        part2_decay = part2_tsrank.rolling(window=decay_window2, min_periods=max(3, decay_window2//2)).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha120(self):
        """
        RANK(VWAP-CLOSE)/RANK(VWAP+CLOSE)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        denominator = vwap + self.C
        denominator = denominator.replace(0, 1e-10)
        alpha = ((vwap - self.C) / denominator).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha121(self):
        """
        (RANK(VWAP-MIN(VWAP,12))^TSRANK(CORR(TSRANK(VWAP,20),TSRANK(MEAN(VOLUME,60),2),18),3))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_min = vwap.rolling(window=12, min_periods=6).min().fillna(method='ffill').fillna(method='bfill')
        part1 = (vwap - vwap_min).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        vol_window = min(60, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        tsrank_vwap = self._tsrank_fixed(vwap, 20)
        tsrank_vol = self._tsrank_fixed(vol_ma, 2)
        corr_window = min(18, len(self.df) // 3)
        part2_corr = tsrank_vwap.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(tsrank_vol).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_corr, 3).fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        alpha = pd.Series(index=self.df.index, dtype=float)
        for i in range(len(self.df)):
            p1 = part1.iloc[i]
            p2 = part2.iloc[i]
            if pd.notna(p1) and pd.notna(p2):
                try:
                    alpha.iloc[i] = -(p1 ** p2)
                except:
                    alpha.iloc[i] = np.nan
            else:
                alpha.iloc[i] = np.nan
        
        return alpha.fillna(method='ffill').fillna(method='bfill')
    
    def alpha122(self):
        """
        (SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)-DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1))/DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1)
        """
        part1 = np.log(self.C)
        part1 = self._sma(part1, 13, 2)
        part1 = self._sma(part1, 13, 2)
        part1 = self._sma(part1, 13, 2)
        return part1.pct_change()
    
    def alpha123(self):
        """
        (RANK(CORR(SUM((HIGH+LOW)/2,20),SUM(MEAN(VOLUME,60),20),9)) < RANK(CORR(LOW,VOLUME,6)))*-1
        """
        part1 = (self.H * 0.5 + self.L * 0.5).rolling(window=20, min_periods=20).sum()
        part1 = self.V.rolling(window=60, min_periods=60).mean().rolling(window=20, min_periods=20).sum().rolling(window=9, min_periods=9).corr(part1).rank(pct=True)
        part2 = self.L.rolling(window=6, min_periods=6).corr(self.V).rank(pct=True)
        return -1 * (part2 - part1)
    
    def alpha124(self):
        """
        (CLOSE-VWAP)/DECAYLINEAR(RANK(TSMAX(CLOSE,30)),2)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        part1 = self.C - vwap
        close_max = self.C.rolling(window=30, min_periods=15).max().fillna(method='ffill').fillna(method='bfill')
        part2_rank = close_max.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        w2 = np.arange(1, 3)
        part2 = part2_rank.rolling(window=2, min_periods=1).apply(
            lambda x: np.dot(x, w2[:len(x)]) if len(x) >= 1 else np.nan
        ).fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill')
        alpha = alpha.clip(lower=alpha.quantile(0.01), upper=alpha.quantile(0.99))
        return alpha
    
    def alpha125(self):
        """
        RANK(DECAYLINEAR(CORR(VWAP,MEAN(VOLUME,80),17),20))/RANK(DECAYLINEAR(DELTA(CLOSE*0.5+VWAP*0.5,3),16))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w20 = np.arange(1, 21)
        w16 = np.arange(1, 17)
        
        vol_window = min(80, len(self.df) // 2)
        corr_window = min(17, len(self.df) // 3)
        decay_window1 = min(20, len(self.df) // 3)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//8)).mean().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_ma.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(vwap).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=decay_window1, min_periods=max(5, decay_window1//4)).apply(
            lambda x: np.dot(x, w20[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        decay_window2 = min(16, len(self.df) // 3)
        weighted_price = self.C * 0.5 + vwap * 0.5
        part2_diff = weighted_price.diff(3).fillna(0)
        part2_decay = part2_diff.rolling(window=decay_window2, min_periods=max(5, decay_window2//3)).apply(
            lambda x: np.dot(x, w16[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill')
        alpha = alpha.clip(lower=alpha.quantile(0.01), upper=alpha.quantile(0.99))
        return alpha
    
    def alpha126(self):
        """
        (CLOSE+HIGH+LOW)/3
        """
        return (self.C + self.H + self.L) / 3.0
    
    def alpha127(self):
        """
        MEAN((100*(CLOSE-MAX(CLOSE,12))/MAX(CLOSE,12))^2)^(1/2)
        """
        close_max = self.C.rolling(window=12, min_periods=12).max()
        alpha = (self.C - close_max) / close_max * 100
        return (alpha ** 2).rolling(window=12, min_periods=12).mean() ** 0.5
    
    def alpha128(self):
        """
        100-(100/(1+SUM(((HIGH+LOW+CLOSE)/3>DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),14)/
        SUM(((HIGH+LOW+CLOSE)/3<DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),14)))
        """
        tp = (self.H + self.L + self.C) / 3.0
        condition1 = tp.diff() > 0.0
        condition2 = tp.diff() < 0.0
        
        part1 = tp * self.V
        part1[~condition1] = 0.0
        part1 = part1.rolling(window=14, min_periods=14).sum()
        
        part2 = tp * self.V
        part2[~condition2] = 0.0
        part2 = part2.rolling(window=14, min_periods=14).sum()
        
        return 100.0 - 100.0 / (1 + part1 / part2)
    
    def alpha129(self):
        """
        SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12)
        """
        return abs(np.minimum(self.C.diff(), 0.0)).rolling(window=12, min_periods=12).sum()
    
    def alpha130(self):
        """
        (RANK(DECAYLINEAR(CORR((HIGH+LOW)/2,MEAN(VOLUME,40),9),10))/RANK(DECAYLINEAR(CORR(RANK(VWAP),RANK(VOLUME),7),3)))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w10 = np.arange(1, 11)
        w3 = np.arange(1, 4)
        
        vol_window = min(40, len(self.df) // 2)
        corr_window1 = min(9, len(self.df) // 4)
        decay_window1 = min(10, len(self.df) // 4)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//4)).mean().fillna(method='ffill').fillna(method='bfill')
        hl_avg = self.H * 0.5 + self.L * 0.5
        part1_corr = vol_ma.rolling(window=corr_window1, min_periods=max(5, corr_window1//2)).corr(hl_avg).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=decay_window1, min_periods=max(5, decay_window1//2)).apply(
            lambda x: np.dot(x, w10[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        corr_window2 = min(7, len(self.df) // 5)
        decay_window2 = min(3, len(self.df) // 10)
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        part2_corr = vwap_rank.rolling(window=corr_window2, min_periods=max(4, corr_window2//2)).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill')
        alpha = alpha.clip(lower=alpha.quantile(0.01), upper=alpha.quantile(0.99))
        return alpha
    
    def alpha131(self):
        """
        (RANK(DELTA(VWAP,1))^TSRANK(CORR(CLOSE,MEAN(VOLUME,50),18),18))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_diff = vwap.diff().fillna(0)
        part1 = vwap_diff.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        vol_window = min(50, len(self.df) // 2)
        corr_window = min(18, len(self.df) // 3)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//5)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vol_ma.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_corr, 18).fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        alpha = np.exp(np.log(part1 + 1e-10) * part2)
        alpha = alpha.fillna(method='ffill').fillna(method='bfill').clip(0, 100)
        return alpha
    
    def alpha132(self):
        """
        MEAN(AMOUNT,20)
        """
        return self.AMOUNT.rolling(window=20, min_periods=20).mean()
    
    def alpha133(self):
        """
        ((20-HIGHDAY(HIGH,20))/20)*100-((20-LOWDAY(LOW,20))/20)*100
        """
        def highday(x):
            return 19 - x.argmax() if len(x) == 20 else np.nan
        def lowday(x):
            return 19 - x.argmin() if len(x) == 20 else np.nan
        
        part1 = (20 - self.H.rolling(window=20, min_periods=20).apply(highday)) / 20 * 100
        part2 = (20 - self.L.rolling(window=20, min_periods=20).apply(lowday)) / 20 * 100
        return part1 - part2
    
    def alpha134(self):
        """
        (CLOSE-DELAY(CLOSE,12))/DELAY(CLOSE,12)*VOLUME
        """
        return self.C.pct_change(periods=12) * self.V
    
    def alpha135(self):
        """
        SMA(DELAY(CLOSE/DELAY(CLOSE,20),1),20,1)
        """
        alpha = (self.C / self.C.shift(20)).shift(1)
        return self._sma(alpha, 20, 1)
    
    def alpha136(self):
        """
        -1*RANK(DELTA(RET,3))*CORR(OPEN,VOLUME,10)
        """
        ret = self.C.pct_change()
        part1 = ret.diff(3).rank(pct=True)
        part2 = self.O.rolling(window=10, min_periods=10).corr(self.V)
        return -1 * part1 * part2
    
    def alpha137(self):
        """
        16*(CLOSE+(CLOSE-OPEN)/2-DELAY(OPEN,1))/
        ((ABS(HIGH-DELAY(CLOSE,1))>ABS(LOW-DELAY(CLOSE,1))&ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1))?ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
        (ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) & ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1))?ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4)))
        *MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1)))
        """
        part1 = self.C * 1.5 - self.O * 0.5 - self.O.shift(1)
        part2 = abs(self.H - self.C.shift(1)) + abs(self.L - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        
        condition1 = np.logical_and(
            abs(self.H - self.C.shift(1)) > abs(self.L - self.C.shift(1)),
            abs(self.H - self.C.shift(1)) > abs(self.H - self.L.shift(1))
        )
        condition2 = np.logical_and(
            abs(self.L - self.C.shift(1)) > abs(self.H - self.L.shift(1)),
            abs(self.L - self.C.shift(1)) > abs(self.H - self.C.shift(1))
        )
        
        part2[~condition1 & condition2] = abs(self.L - self.C.shift(1)) + abs(self.H - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        part2[~condition1 & ~condition2] = abs(self.H - self.L.shift(1)) + abs(self.C - self.O).shift(1) / 4.0
        
        part3 = np.maximum(abs(self.H - self.C.shift(1)), abs(self.L - self.C.shift(1)))
        alpha = part1 / part2 * part3 * 16.0
        return alpha
    
    def alpha138(self):
        """
        ((RANK(DECAYLINEAR(DELTA(LOW*0.7+VWAP*0.3,3),20))
        -TSRANK(DECAYLINEAR(TSRANK(
            CORR(TSRANK(LOW,8),TSRANK(MEAN(VOLUME,60),17),5)
            ,19),16),7))* -1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w20 = np.arange(1, 21)
        w16 = np.arange(1, 17)
        
        decay_window1 = min(20, len(self.df) // 3)
        weighted_price = self.L * 0.7 + vwap * 0.3
        part1_diff = weighted_price.diff(3).fillna(0)
        part1_decay = part1_diff.rolling(window=decay_window1, min_periods=max(5, decay_window1//4)).apply(
            lambda x: np.dot(x, w20[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(60, len(self.df) // 2)
        tsrank_window1 = min(17, len(self.df) // 3)
        corr_window = min(5, len(self.df) // 6)
        tsrank_window2 = min(19, len(self.df) // 3)
        decay_window2 = min(16, len(self.df) // 3)
        tsrank_window3 = min(7, len(self.df) // 5)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        tsrank_vol = self._tsrank_fixed(vol_ma, tsrank_window1).fillna(method='ffill').fillna(method='bfill')
        tsrank_low = self._tsrank_fixed(self.L, 8).fillna(method='ffill').fillna(method='bfill')
        part2_corr = tsrank_low.rolling(window=corr_window, min_periods=max(3, corr_window//2)).corr(tsrank_vol).fillna(method='ffill').fillna(method='bfill')
        part2_tsrank = self._tsrank_fixed(part2_corr, tsrank_window2).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_tsrank.rolling(window=decay_window2, min_periods=max(5, decay_window2//3)).apply(
            lambda x: np.dot(x, w16[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, tsrank_window3).fillna(method='ffill').fillna(method='bfill')
        
        alpha = -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha139(self):
        """
        (-1*CORR(OPEN,VOLUME,10))
        """
        return -1 * self.O.rolling(window=10, min_periods=10).corr(self.V)
    
    def alpha140(self):
        """
        MIN(RANK(DECAYLINEAR(RANK(OPEN)+RANK(LOW)-RANK(HIGH)-RANK(CLOSE),8)),TSRANK(DECAYLINEAR(CORR(TSRANK(CLOSE,8),TSRANK(MEAN(VOLUME,60),20),8),7),3))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w8 = np.arange(1, 9)
        w7 = np.arange(1, 8)
        
        decay_window1 = min(8, len(self.df) // 4)
        open_rank = self.O.rank(pct=True, method='min')
        low_rank = self.L.rank(pct=True, method='min')
        high_rank = self.H.rank(pct=True, method='min')
        close_rank = self.C.rank(pct=True, method='min')
        
        part1_series = open_rank + low_rank - high_rank - close_rank
        part1_series = part1_series.fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_series.rolling(window=decay_window1, min_periods=max(4, decay_window1//2)).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= 4 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(60, len(self.df) // 2)
        tsrank_window1 = min(20, len(self.df) // 3)
        corr_window = min(8, len(self.df) // 4)
        decay_window2 = min(7, len(self.df) // 5)
        tsrank_window2 = min(3, len(self.df) // 10)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        tsrank_vol = self._tsrank_fixed(vol_ma, tsrank_window1).fillna(method='ffill').fillna(method='bfill')
        tsrank_close = self._tsrank_fixed(self.C, 8).fillna(method='ffill').fillna(method='bfill')
        part2_corr = tsrank_close.rolling(window=corr_window, min_periods=max(4, corr_window//2)).corr(tsrank_vol).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=max(3, decay_window2//2)).apply(
            lambda x: np.dot(x, w7[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, tsrank_window2).fillna(method='ffill').fillna(method='bfill')
        
        alpha = np.minimum(part1, part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha141(self):
        """
        (RANK(CORR(RANK(HIGH),RANK(MEAN(VOLUME,15)),9))*-1)
        """
        alpha = self.V.rolling(window=15, min_periods=15).mean().rank(pct=True)
        alpha = alpha.rolling(window=9, min_periods=9).corr(self.H.rank(pct=True)).rank(pct=True)
        return -1 * alpha
    
    def alpha142(self):
        """
        -1*RANK(TSRANK(CLOSE,10))*RANK(DELTA(DELTA(CLOSE,1),1))*RANK(TSRANK(VOLUME/MEAN(VOLUME,20),5))
        """
        part1 = self._tsrank(self.C, 10).rank(pct=True)
        part2 = self.C.diff().diff().rank(pct=True)
        part3 = self._tsrank(self.V / self.V.rolling(window=20, min_periods=20).mean(), 5).rank(pct=True)
        return -1 * part1 * part2 * part3
    
    def alpha143(self):
        """
        CLOSE>DELAY(CLOSE,1)?(CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*SELF:SELF
        """
        condition = self.C > self.C.shift(1)
        alpha = self.C.pct_change()
        alpha[~condition] = alpha.shift(1)[~condition]
        return alpha
    
    def alpha144(self):
        """
        SUMIF(ABS(CLOSE/DELAY(CLOSE,1)-1)/AMOUNT,20,CLOSE<DELAY(CLOSE,1))/COUNT(CLOSE<DELAY(CLOSE,1),20)
        """
        part1 = abs(self.C.pct_change()) / self.AMOUNT
        part1[self.C.diff() >= 0] = 0.0
        part1 = part1.rolling(window=20, min_periods=20).sum()
        part2 = (self.C.diff() < 0.0).rolling(window=20, min_periods=20).sum()
        return part1 / part2
    
    def alpha145(self):
        """
        (MEAN(VOLUME,9)-MEAN(VOLUME,26))/MEAN(VOLUME,12)*100
        """
        ma9 = self.V.rolling(window=9, min_periods=9).mean()
        ma26 = self.V.rolling(window=26, min_periods=26).mean()
        ma12 = self.V.rolling(window=12, min_periods=12).mean()
        return (ma9 - ma26) / ma12 * 100.0
    
    def alpha146(self):
        """
        MEAN(RET-SMA(RET,61,2),20)*(RET-SMA(RET,61,2))/SMA(SMA(RET,61,2)^2,60)
        """
        ret = self.C.pct_change()
        sma = self._sma(ret, 61, 2)
        ret_excess = ret - sma
        part1 = ret_excess.rolling(window=20, min_periods=20).mean() * ret_excess
        part2 = self._sma(sma ** 2, 60, 1)
        return part1 / part2
    
    def alpha147(self):
        """
        REGBETA(MEAN(CLOSE,12),SEQUENCE(12))
        """
        ma_price = self.C.rolling(window=12, min_periods=12).mean()
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(12, len(self.df)):
            y = ma_price.iloc[i-12:i]
            x = np.arange(1, 13)
            result.iloc[i] = self._regbeta(y, x)
        return result.fillna(0)
    
    def alpha148(self):
        """
        (RANK(CORR(OPEN,SUM(MEAN(VOLUME,60),9),6))<RANK(OPEN-TSMIN(OPEN,14)))*-1
        """
        part1 = self.V.rolling(window=60, min_periods=60).mean().rolling(window=9, min_periods=9).sum()
        part1 = part1.rolling(window=6, min_periods=6).corr(self.O).rank(pct=True)
        part2 = (self.O - self.O.rolling(window=14, min_periods=14).min()).rank(pct=True)
        return -1 * (part2 - part1)
    
    def alpha149(self):
        """
        REGBETA(FILTER(RET,BANCHMARK_INDEX_CLOSE<DELAY(BANCHMARK_INDEX_CLOSE,1)),
        FILTER(BANCHMARK_INDEX_CLOSE/DELAY(BANCHMARK_INDEX_CLOSE,1)-1,BANCHMARK_INDEX_CLOSE<DELAY(BANCHMARK_INDEX_CLOSE,1)),252)
        调整窗口期以适应数据量
        """
        n_rows = len(self.df)
        if n_rows < 252:
            window = max(60, n_rows // 2)
        else:
            window = 252
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            elif 'closePrice' in index_data.columns:
                index_close = index_data['closePrice']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                date_to_index = dict(zip(index_data['date'], index_close))
                bm_close = self.df['date'].map(date_to_index).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=5).mean()
        
        bm_ret = bm_close.pct_change().fillna(0)
        bm_down = bm_ret < 0.0
        stock_ret = self.C.pct_change().fillna(0)
        
        result = pd.Series(index=self.df.index, dtype=float)
        if n_rows < window:
            return pd.Series(0, index=self.df.index)
        
        for i in range(window, n_rows):
            start_idx = i - window
            bm_down_window = bm_down.iloc[start_idx:i]
            valid_indices = bm_down_window[bm_down_window].index
            if len(valid_indices) < 5:
                result.iloc[i] = np.nan
                continue
            y = stock_ret.loc[valid_indices]
            x = bm_ret.loc[valid_indices]
            valid_mask = ~(y.isna() | x.isna())
            y_clean = y[valid_mask]
            x_clean = x[valid_mask]
            if len(y_clean) > 3:
                try:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
                    result.iloc[i] = slope
                except:
                    result.iloc[i] = np.nan
            else:
                result.iloc[i] = np.nan
        
        result = result.fillna(method='ffill').fillna(method='bfill').fillna(0)
        return result
    
    def alpha150(self):
        """
        (CLOSE+HIGH+LOW)/3*VOLUME
        """
        return (self.C + self.H + self.L) / 3.0 * self.V
    
    def alpha151(self):
        """
        SMA(CLOSE-DELAY(CLOSE,20),20,1)
        """
        return self._sma(self.C.diff(20), 20, 1)
    
    def alpha152(self):
        """
        A=DELAY(SMA(DELAY(CLOSE/DELAY(CLOSE,9),1),9,1),1)
        SMA(MEAN(A,12)-MEAN(A,26),9,1)
        """
        a = (self.C / self.C.shift(9)).shift(1)
        a = self._sma(a, 9, 1).shift(1)
        alpha = (a.rolling(window=12, min_periods=12).mean() - a.rolling(window=26, min_periods=26).mean())
        alpha = self._sma(alpha, 9, 1)
        return alpha
    
    def alpha153(self):
        """
        (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/4
        """
        ma3 = self.C.rolling(window=3, min_periods=3).mean()
        ma6 = self.C.rolling(window=6, min_periods=6).mean()
        ma12 = self.C.rolling(window=12, min_periods=12).mean()
        ma24 = self.C.rolling(window=24, min_periods=24).mean()
        return (ma3 + ma6 + ma12 + ma24) / 4
    
    def alpha154(self):
        """
        VWAP-MIN(VWAP,16)<CORR(VWAP,MEAN(VOLUME,180),18)
        """
        n_rows = len(self.df)
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_min = vwap.rolling(window=16, min_periods=8).min().fillna(method='ffill').fillna(method='bfill')
        part1 = vwap - vwap_min
        
        if n_rows < 180:
            vol_window = max(60, n_rows // 2)
            corr_window = max(10, min(18, n_rows // 5))
        else:
            vol_window = 180
            corr_window = 18
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vol_ma.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(vwap).fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part2_corr - part1).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha155(self):
        """
        SMA(VOLUME,13,2)-SMA(VOLUME,27,2)-SMA(SMA(VOLUME,13,2)-SMA(VOLUME,27,2),10,2)
        """
        sma13 = self._sma(self.V, 13, 2)
        sma27 = self._sma(self.V, 27, 2)
        diff = sma13 - sma27
        return sma13 - sma27 - self._sma(diff, 10, 2)
    
    def alpha156(self):
        """
        MAX(RANK(DECAYLINEAR(DELTA(VWAP,5),3)),RANK(DECAYLINEAR((DELTA(OPEN*0.15+LOW*0.85,2)/(OPEN*0.15+LOW*0.85)) * -1,3))) * -1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        w3 = np.arange(1, 4)
        den = self.O * 0.15 + self.L * 0.85
        
        vwap_diff = vwap.diff(5).fillna(0)
        part1_decay = vwap_diff.rolling(window=3, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        den = den.replace(0, 1e-10)
        den_diff = den.diff(2).fillna(0)
        den_ratio = (den_diff / den) * (-1)
        den_ratio = den_ratio.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        part2_decay = den_ratio.rolling(window=3, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha157(self):
        """
        MIN(PROD(RANK(LOG(SUM(TSMIN(RANK(-1*RANK(DELTA(CLOSE-1,5))),2),1))),1),5)+TSRANK(DELAY(-1*RET,6),5)
        """
        part1 = (self.C - 1.0).diff(5).rank(pct=True) * (-1)
        part1 = part1.rank(pct=True).rolling(window=2, min_periods=2).min()
        part1 = np.log(part1.rolling(window=1, min_periods=1).sum()).rank(pct=True)
        part1 = part1.rolling(window=5, min_periods=5).min()
        
        part2 = self._tsrank((-1 * self.C.pct_change()).shift(6), 5)
        
        return part1 + part2
    
    def alpha158(self):
        """
        (HIGH-LOW)/CLOSE
        """
        return (self.H - self.L) / self.C
    
    def alpha159(self):
        """
        ((CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),6))/SUM(MAX(HIGH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),6)*12*24
        +(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),12))/SUM(MAX(HIGH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),12)*6*24
        +(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),24))/SUM(MAX(HIGH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),24)*6*12)*100/(6*12+6*24+12*24)
        """
        min_low_close = np.minimum(self.L, self.C.shift(1))
        max_high_close = np.maximum(self.H, self.C.shift(1))
        diff = max_high_close - min_low_close
        
        part1 = (self.C - min_low_close.rolling(window=6, min_periods=6).sum()) / diff.rolling(window=6, min_periods=6).sum() * 12 * 24
        part2 = (self.C - min_low_close.rolling(window=12, min_periods=12).sum()) / diff.rolling(window=12, min_periods=12).sum() * 6 * 24
        part3 = (self.C - min_low_close.rolling(window=24, min_periods=24).sum()) / diff.rolling(window=24, min_periods=24).sum() * 6 * 12
        
        return (part1 + part2 + part3) * 100.0 / (12 * 6 + 6 * 24 + 12 * 24)
    
    def alpha160(self):
        """
        SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)
        """
        part1 = self.C.rolling(window=20, min_periods=20).std()
        part1[self.C.diff() > 0] = 0.0
        return self._sma(part1, 20, 1)
    
    def alpha161(self):
        """
        MEAN(MAX(MAX(HIGH-LOW,ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),12)
        """
        part1 = np.maximum(self.H - self.L, abs(self.C.shift(1) - self.H))
        part1 = np.maximum(part1, abs(self.C.shift(1) - self.L))
        return part1.rolling(window=12, min_periods=12).mean()
    
    def alpha162(self):
        """
        (SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100
        -MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))
        /(MAX(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12)
        -MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))
        """
        diff = self.C.diff()
        den = np.maximum(diff, 0.0).ewm(adjust=False, alpha=1/12, min_periods=0).mean() / abs(diff).ewm(adjust=False, alpha=1/12, min_periods=0).mean() * 100.0
        
        alpha = (den - den.rolling(window=12, min_periods=12).min()) / (den.rolling(window=12, min_periods=12).max() - den.rolling(window=12, min_periods=12).min())
        return alpha
    
    def alpha163(self):
        """
        RANK((-1*RET)*MEAN(VOLUME,20)*VWAP*(HIGH-CLOSE))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        ret = self.C.pct_change().fillna(0)
        vol_ma = self.V.rolling(window=20, min_periods=10).mean().fillna(method='ffill').fillna(method='bfill')
        high_minus_close = self.H - self.C
        
        alpha = (-1 * ret) * vol_ma * vwap * high_minus_close
        alpha = alpha.fillna(method='ffill').fillna(method='bfill')
        alpha_rank = alpha.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        return alpha_rank
    
    def alpha164(self):
        """
        SMA(((CLOSE>DELAY(CLOSE,1)?1/(CLOSE-DELAY(CLOSE,1)):1)-MIN(CLOSE>DELAY(CLOSE,1)?1/(CLOSE-DELAY(CLOSE,1)):1,12))/(HIGH-LOW)*100,13,2)
        """
        diff = self.C.diff()
        part1 = 1.0 / diff
        part1[diff <= 0] = 1.0
        part2 = part1.rolling(window=12, min_periods=12).min()
        alpha = (part1 - part2) / (self.H - self.L) * 100.0
        return self._sma(alpha, 13, 2)
    
    def alpha165(self):
        """
        MAX(SUMAC(CLOSE-MEAN(CLOSE,48)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,48)))/STD(CLOSE,48)
        """
        part = self.C - self.C.rolling(window=48, min_periods=48).mean()
        part = part.rolling(window=48, min_periods=48).sum()
        
        part1 = part.rolling(window=48, min_periods=48).max()
        part2 = part.rolling(window=48, min_periods=48).min()
        part3 = self.C.rolling(window=48, min_periods=48).std()
        
        return part1 - part2 / part3
    
    def alpha166(self):
        """
        -20*(20-1)^1.5*SUM(CLOSE/DELAY(CLOSE,1)-1-MEAN(CLOSE/DELAY(CLOSE,1)-1,20),20)/((20-1)*(20-2)*(SUM((CLOSE/DELAY(CLOSE,1))^2,20))^1.5)
        """
        ret = self.C.pct_change()
        ret_mean = ret.rolling(window=20, min_periods=20).mean()
        part1 = (ret - ret_mean).rolling(window=20, min_periods=20).sum() * (-20 * 19 ** 1.5)
        part2 = ((self.C / self.C.shift(1)) ** 2).rolling(window=20, min_periods=20).sum() ** 1.5 * 19 * 18
        return part1 / part2
    
    def alpha167(self):
        """
        SUM(CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0,12)
        """
        return np.maximum(self.C.diff(), 0.0).rolling(window=12, min_periods=12).sum()
    
    def alpha168(self):
        """
        -1*VOLUME/MEAN(VOLUME,20)
        """
        return -1 * self.V / self.V.rolling(window=20, min_periods=20).mean()
    
    def alpha169(self):
        """
        SMA(MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),12)-MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),26),10,1)
        """
        part1 = self._sma(self.C.diff(), 9, 1).shift(1)
        part2 = part1.rolling(window=12, min_periods=12).mean() - part1.rolling(window=26, min_periods=26).mean()
        return self._sma(part2, 10, 1)
    
    def alpha170(self):
        """
        ((RANK(1/CLOSE)*VOLUME)/MEAN(VOLUME,20))*(HIGH*RANK(HIGH-CLOSE)/(SUM(HIGH,5)/5))-RANK(VWAP-DELAY(VWAP,5))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        inv_close_rank = (1.0 / self.C).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        vol_ma = self.V.rolling(window=20, min_periods=10).mean().fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        part1 = (inv_close_rank * self.V) / vol_ma
        
        high_minus_close_rank = (self.H - self.C).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        high_ma5 = self.H.rolling(window=5, min_periods=3).sum() / 5.0
        high_ma5 = high_ma5.fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        part2 = (self.H * high_minus_close_rank) / high_ma5
        
        vwap_diff = vwap.diff(5).fillna(0)
        part3 = vwap_diff.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 * part2 - part3).fillna(method='ffill').fillna(method='bfill').clip(-10, 10)
        return alpha
    
    def alpha171(self):
        """
        (-1*(LOW-CLOSE)*(OPEN^5))/((CLOSE-HIGH)*(CLOSE^5))
        """
        self.C = self.C.clip(lower=1e-10)
        self.O = self.O.clip(lower=1e-10)
        self.H = self.H.clip(lower=1e-10)
        self.L = self.L.clip(lower=1e-10)
        
        part1 = (self.C - self.L) * (self.O ** 5)
        part2 = (self.C - self.H) * (self.C ** 5)
        part2 = part2.replace(0, 1e-10)
        mask_small = abs(part2) < 1e-10
        part2[mask_small] = 1e-10 * np.sign(part2[mask_small])
        
        alpha = part1 / part2
        alpha = alpha.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        return alpha
    
    def alpha172(self):
        """
        ADX指标
        """
        hd = self.H.diff()
        ld = -self.L.diff()
        tr = np.maximum(
            np.maximum(self.H - self.L, abs(self.H - self.C.shift(1))),
            abs(self.L - self.C.shift(1))
        )
        
        plus_dm = ((hd > 0) & (hd > ld)) * hd
        minus_dm = ((ld > 0) & (ld > hd)) * ld
        
        plus_di = plus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        minus_di = minus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
        return dx.rolling(window=6, min_periods=6).mean()
    
    def alpha173(self):
        """
        3*SMA(CLOSE,13,2)-2*SMA(SMA(CLOSE,13,2),13,2)+SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)
        """
        sma = self._sma(self.C, 13, 2)
        sma2 = self._sma(sma, 13, 2)
        log_sma = self._sma(np.log(self.C), 13, 2)
        log_sma2 = self._sma(log_sma, 13, 2)
        log_sma3 = self._sma(log_sma2, 13, 2)
        
        return 3 * sma - 2 * sma2 + log_sma3
    
    def alpha174(self):
        """
        SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)
        """
        part1 = self.C.rolling(window=20, min_periods=20).std()
        part1[self.C.diff() <= 0] = 0.0
        return self._sma(part1, 20, 1)
    
    def alpha175(self):
        """
        MEAN(MAX(MAX(HIGH-LOW,ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),6)
        """
        part1 = np.maximum(self.H - self.L, abs(self.C.shift(1) - self.H))
        part1 = np.maximum(part1, abs(self.C.shift(1) - self.L))
        return part1.rolling(window=6, min_periods=6).mean()
    
    def alpha176(self):
        """
        CORR(RANK((CLOSE-TSMIN(LOW,12))/(TSMAX(HIGH,12)-TSMIN(LOW,12))),RANK(VOLUME),6)
        """
        high_max = self.H.rolling(window=12, min_periods=12).max()
        low_min = self.L.rolling(window=12, min_periods=12).min()
        part1 = (self.C - low_min) / (high_max - low_min)
        part1 = part1.rank(pct=True)
        part2 = self.V.rank(pct=True)
        return part1.rolling(window=6, min_periods=6).corr(part2)
    
    def alpha177(self):
        """
        ((20-HIGHDAY(HIGH,20))/20)*100
        """
        def highday(x):
            return 19 - x.argmax() if len(x) == 20 else np.nan
        return (20 - self.H.rolling(window=20, min_periods=20).apply(highday)) / 20 * 100
    
    def alpha178(self):
        """
        (CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*VOLUME
        """
        return self.C.pct_change() * self.V
    
    def alpha179(self):
        """
        RANK(CORR(VWAP,VOLUME,4))*RANK(CORR(RANK(LOW),RANK(MEAN(VOLUME,50)),12))
        """
        n_rows = len(self.df)
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        part1_corr = vwap.rolling(window=4, min_periods=3).corr(self.V).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        if n_rows < 50:
            vol_window = max(20, n_rows // 2)
            corr_window = max(5, min(12, n_rows // 4))
        else:
            vol_window = 50
            corr_window = 12
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//5)).mean().fillna(method='ffill').fillna(method='bfill')
        low_rank = self.L.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        vol_ma_rank = vol_ma.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        part2_corr = low_rank.rolling(window=corr_window, min_periods=max(3, corr_window//2)).corr(vol_ma_rank).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 * part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha180(self):
        """
        (MEAN(VOLUME,20)<VOLUME)?((-1*TSRANK(ABS(DELTA(CLOSE,7)),60))*SIGN(DELTA(CLOSE,7)):(-1*VOLUME))
        """
        condition = self.V.rolling(window=20, min_periods=20).mean() < self.V
        alpha = pd.Series(index=self.df.index, dtype=float)
        alpha[condition] = self._tsrank(abs(self.C.diff(7)), 60) * np.sign(self.C.diff(7)) * (-1)
        alpha[~condition] = -1 * self.V
        return alpha
    
    def alpha181(self):
        """
        SUM(RET-MEAN(RET,20)-(BANCHMARK_INDEX_CLOSE-MEAN(BANCHMARK_INDEX_CLOSE,20))^2,20)/SUM((BANCHMARK_INDEX_CLOSE-MEAN(BANCHMARK_INDEX_CLOSE,20))^3)
        """
        n_rows = len(self.df)
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            elif 'closePrice' in index_data.columns:
                index_close = index_data['closePrice']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                date_to_index = dict(zip(index_data['date'], index_close))
                bm_close = self.df['date'].map(date_to_index).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=10).mean()
        
        bm_mean = bm_close - bm_close.rolling(window=20, min_periods=10).mean().fillna(0)
        ret = self.C.pct_change().fillna(0)
        ret_mean = ret.rolling(window=20, min_periods=10).mean().fillna(0)
        
        part1 = (ret - ret_mean - bm_mean ** 2).rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        part2 = (bm_mean ** 3).rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        return alpha
    
    def alpha182(self):
        """
        COUNT((CLOSE>OPEN & BANCHMARK_INDEX_CLOSE>BANCHMARK_INDEX_OPEN) OR (CLOSE<OPEN &BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN),20)/20
        """
        n_rows = len(self.df)
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            elif 'closePrice' in index_data.columns:
                index_close = index_data['closePrice']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'open' in index_data.columns:
                index_open = index_data['open']
            elif 'openPrice' in index_data.columns:
                index_open = index_data['openPrice']
            else:
                index_open = index_close.shift(1).fillna(index_close)
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                date_to_close = dict(zip(index_data['date'], index_close))
                date_to_open = dict(zip(index_data['date'], index_open))
                bm_close = self.df['date'].map(date_to_close).fillna(method='ffill').fillna(method='bfill')
                bm_open = self.df['date'].map(date_to_open).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
                bm_open = index_open.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=5).mean()
            bm_open = self.O.rolling(window=20, min_periods=5).mean()
        
        bm_up = bm_close > bm_open
        stock_up = self.C > self.O
        stock_down = self.C < self.O
        
        condition1 = stock_up & bm_up
        condition2 = stock_down & ~bm_up
        condition = condition1 | condition2
        
        min_periods = max(5, min(10, n_rows // 4))
        alpha = condition.rolling(window=20, min_periods=min_periods).mean().fillna(method='ffill').fillna(method='bfill')
        
        return alpha
    
    def alpha183(self):
        """
        MAX(SUMAC(CLOSE-MEAN(CLOSE,24)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,24)))/STD(CLOSE,24)
        """
        part = self.C - self.C.rolling(window=24, min_periods=24).mean()
        part = part.rolling(window=24, min_periods=24).sum()
        
        part1 = part.rolling(window=24, min_periods=24).max()
        part2 = part.rolling(window=24, min_periods=24).min()
        part3 = self.C.rolling(window=24, min_periods=24).std()
        
        return part1 - part2 / part3
    
    def alpha184(self):
        """
        RANK(CORR(DELAY(OPEN-CLOSE,1),CLOSE,200))+RANK(OPEN-CLOSE)
        """
        n_rows = len(self.df)
        if n_rows < 200:
            window = max(20, int(n_rows * 0.6))
        else:
            window = 200
        
        oc = self.O - self.C
        min_periods = max(10, min(50, window // 4))
        part1_corr = oc.shift(1).rolling(window=window, min_periods=min_periods).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        part2 = oc.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = ((part1 + part2) / 2.0).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha185(self):
        """
        RANK(-1*(1-OPEN/CLOSE)^2)
        """
        return -1 * (1.0 - self.O / self.C) ** 2
    
    def alpha186(self):
        """
        ADXR指标
        """
        hd = self.H.diff()
        ld = -self.L.diff()
        tr = np.maximum(
            np.maximum(self.H - self.L, abs(self.H - self.C.shift(1))),
            abs(self.L - self.C.shift(1))
        )
        
        plus_dm = ((hd > 0) & (hd > ld)) * hd
        minus_dm = ((ld > 0) & (ld > hd)) * ld
        
        plus_di = plus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        minus_di = minus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
        adx = dx.rolling(window=6, min_periods=6).mean()
        adxr = (adx + adx.shift(6)) / 2
        
        return adxr
    
    def alpha187(self):
        """
        SUM(OPEN<=DELAY(OPEN,1)?0:MAX(HIGH-OPEN,OPEN-DELAY(OPEN,1)),20)
        """
        part1 = np.maximum(self.H - self.O, self.O.diff())
        part1[self.O.diff() <= 0] = 0.0
        return part1.rolling(window=20, min_periods=20).sum()
    
    def alpha188(self):
        """
        ((HIGH-LOW-SMA(HIGH-LOW,11,2))/SMA(HIGH-LOW,11,2))*100
        """
        hl = self.H - self.L
        sma = self._sma(hl, 11, 2)
        return (hl - sma) / sma * 100
    
    def alpha189(self):
        """
        MEAN(ABS(CLOSE-MEAN(CLOSE,6)),6)
        """
        ma = self.C.rolling(window=6, min_periods=6).mean()
        return abs(self.C - ma).rolling(window=6, min_periods=6).mean()
    
    def alpha190(self):
        """
        LOG((COUNT(RET>((CLOSE/DELAY(CLOSE,19))^(1/20)-1),20)-1)
        *SUMIF((RET-(CLOSE/DELAY(CLOSE,19))^(1/20)-1)^2,20,RET<(CLOSE/DELAY(CLOSE,19))^(1/20)-1)
        /(COUNT(RET<(CLOSE/DELAY(CLOSE,19))^(1/20)-1,20)
        *SUMIF((RET-((CLOSE/DELAY(CLOSE,19))^(1/20)-1))^2,20,RET>(CLOSE/DELAY(CLOSE,19))^(1/20)-1)))
        """
        ret = self.C.pct_change()
        ret_19 = (self.C / self.C.shift(19)) ** 0.05 - 1.0
        
        part1 = (ret > ret_19).rolling(window=20, min_periods=20).sum() - 1.0
        part2 = (np.minimum(ret - ret_19, 0.0) ** 2).rolling(window=20, min_periods=20).sum()
        part3 = (ret < ret_19).rolling(window=20, min_periods=20).sum()
        part4 = (np.maximum(ret - ret_19, 0.0) ** 2).rolling(window=20, min_periods=20).sum()
        
        return np.log(part1 * part2 / part3 / part4)
    
    def alpha191(self):
        """
        CORR(MEAN(VOLUME,20),LOW,5)+(HIGH+LOW)/2-CLOSE
        """
        part1 = self.V.rolling(window=20, min_periods=20).mean().rolling(window=5, min_periods=5).corr(self.L)
        return part1 + (self.H + self.L) / 2 - self.C


if __name__ == '__main__':
    api = xg_factor()
    result = api.CROSS_DOWN()
    # print(result)
# 全部因子的底层函数
'''
小果
微信:xg_quant
'''
import pandas as pd
import numpy as np
#------------------ 0级：核心工具函数 -------------------------------------------
import numpy as np
import pandas as pd

def RD(N, D=3):
    """四舍五入取3位小数"""
    return np.round(N, D)

def RET(S, N=1):
    """返回序列倒数第N个值，默认返回最后一个"""
    return np.array(S)[-N]

def ABS(S):
    """返回N的绝对值"""
    return np.abs(S)

def MAX(S1, S2):
    """序列max"""
    return np.maximum(S1, S2)

def MIN(S1, S2):
    """序列min"""
    return np.minimum(S1, S2)

def IF(S, A, B):
    """序列布尔判断 return=A if S==True else B"""
    return np.where(S, A, B)

def REF(S, N=1):
    """对序列整体下移动N，返回序列(shift后会产生NAN)"""
    return pd.Series(S).shift(N).values

def DIFF(S, N=1):
    """前一个值减后一个值，前面会产生nan；np.diff(S)直接删除nan，会少一行"""
    return pd.Series(S).diff(N).values

def STD(S, N):
    """求序列的N日标准差，返回序列"""
    return pd.Series(S).rolling(N).std(ddof=0).values

def SUM(S, N):
    """对序列求N天累计和，返回序列；N=0对序列所有依次求和"""
    return pd.Series(S).rolling(N).sum().values if N > 0 else pd.Series(S).cumsum().values

def CONST(S):
    """返回序列S最后的值组成常量序列"""
    return np.full(len(S), S[-1])

def AND(S1, S2):
    """逻辑与运算"""
    return np.logical_and(S1, S2)

def OR(S1, S2):
    """逻辑或运算"""
    return np.logical_or(S1, S2)

def NOT(S1):
    """逻辑非运算"""
    return np.logical_not(S1)

def RANGE(A, B, C):
    """期间函数：B <= A <= C"""
    df = pd.DataFrame()
    df['select'] = A.tolist()
    df['select'] = df['select'].apply(lambda x: True if (x >= B and x <= C) else False)
    return df['select']

def HHV(S, N):
    """HHV(C, 5) 最近5天收盘最高价"""
    return pd.Series(S).rolling(N).max().values

def LLV(S, N):
    """LLV(C, 5) 最近5天收盘最低价"""
    return pd.Series(S).rolling(N).min().values

def HHVBARS(S, N):
    """求N周期内S最高值到当前周期数，返回序列"""
    return pd.Series(S).rolling(N).apply(lambda x: np.argmax(x[::-1]), raw=True).values

def LLVBARS(S, N):
    """求N周期内S最低值到当前周期数，返回序列"""
    return pd.Series(S).rolling(N).apply(lambda x: np.argmin(x[::-1]), raw=True).values

def MA(S, N):
    """求序列的N日简单移动平均值，返回序列"""
    return pd.Series(S).rolling(N).mean().values

def EMA(S, N):
    """指数移动平均，为了精度 S>4*N，EMA至少需要120周期；alpha=2/(span+1)"""
    return pd.Series(S).ewm(span=N, adjust=False).mean().values

def SMA(S, N, M=1):
    """中国式的SMA，至少需要120周期才精确(雪球180周期)；alpha=1/(1+com)"""
    return pd.Series(S).ewm(alpha=M/N, adjust=False).mean().values  # com=N-M/M

def DMA(S, A):
    """求S的动态移动平均，A作平滑因子，必须 0<A<1 (此为核心函数，非指标)"""
    return pd.Series(S).ewm(alpha=A, adjust=True).mean().values

def WMA(S, N):
    """通达信S序列的N日加权移动平均 Yn = (1*X1+2*X2+3*X3+...+n*Xn)/(1+2+3+...+Xn)"""
    return pd.Series(S).rolling(N).apply(lambda x: x[::-1].cumsum().sum() * 2 / N / (N + 1), raw=True).values

def AVEDEV(S, N):
    """平均绝对偏差 (序列与其平均值的绝对差的平均值)"""
    return pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values

def SLOPE(S, N):
    """返回S序列N周期回线性回归斜率"""
    return pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N), x, deg=1)[0], raw=True).values

def FORCAST(S, N):
    """返回S序列N周期回线性回归后的预测值"""
    return pd.Series(S).rolling(N).apply(lambda x: np.polyval(np.polyfit(range(N), x, deg=1), N-1), raw=True).values

def LAST(S, A, B):
    """从前A日到前B日一直满足S_BOOL条件，要求A>B & A>0 & B>=0"""
    return np.array(pd.Series(S).rolling(A+1).apply(lambda x: np.all(x[::-1][B:]), raw=True), dtype=bool)


#------------------ 1级：应用层函数(通过0级核心函数实现）--------------------------
def COUNT(S, N):
    """COUNT(CLOSE>O, N): 最近N天满足S_BOO的天数，True的天数"""
    return SUM(S, N)

def EVERY(S, N):
    """EVERY(CLOSE>O, 5) 最近N天是否都是True"""
    return IF(SUM(S, N) == N, True, False)

def EXIST(S, N):
    """EXIST(CLOSE>3010, N=5) n日内是否存在一天大于3000点"""
    return IF(SUM(S, N) > 0, True, False)

def FILTER(S, N):
    """
    FILTER函数，S满足条件后，将其后N周期内的数据置为0
    例：FILTER(C==H,5) 涨停后，后5天不再发出信号
    """
    for i in range(len(S)):
        if S[i]:
            S[i+1:i+1+N] = 0
    return S

def BARSLAST(S):
    """上一次条件成立到当前的周期，BARSLAST(C/REF(C,1)>=1.1) 上一次涨停到今天的天数"""
    M = np.concatenate(([0], np.where(S, 1, 0)))
    for i in range(1, len(M)):
        M[i] = 0 if M[i] else M[i-1] + 1
    return M[1:]

def BARSLASTCOUNT(S):
    """统计连续满足S条件的周期数；BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数"""
    rt = np.zeros(len(S) + 1)
    for i in range(len(S)):
        rt[i+1] = rt[i] + 1 if S[i] else rt[i+1]
    return rt[1:]

def BARSSINCEN(S, N):
    """N周期内第一次S条件成立到现在的周期数，N为常量"""
    return pd.Series(S).rolling(N).apply(
        lambda x: N-1-np.argmax(x) if np.argmax(x) or x[0] else 0,
        raw=True
    ).fillna(0).values.astype(int)

def CROSS(S1, S2):
    """判断向上金叉穿越 CROSS(MA(C,5), MA(C,10))；判断向下死叉穿越 CROSS(MA(C,10), MA(C,5))"""
    return np.concatenate(([False], np.logical_not((S1 > S2)[:-1]) & (S1 > S2)[1:]))

def CROSS_UP(S1, S2):
    """判断向上金叉穿越 CROSS(MA(C,5), MA(C,10))"""
    return np.concatenate(([False], np.logical_not((S1 > S2)[:-1]) & (S1 > S2)[1:]))

def CROSS_DOWN(S1, S2):
    """判断向下死叉穿越 CROSS(MA(C,5), MA(C,10))"""
    return np.concatenate(([False], np.logical_not((S1 < S2)[:-1]) & (S1 < S2)[1:]))

def LONGCROSS(S1, S2, N):
    """两条线维持一定周期后交叉，S1在N周期内都小于S2，本周期从S1下方向上穿过S2时返回1，否则返回0；N=1时等同于CROSS(S1, S2)"""
    return np.array(np.logical_and(LAST(S1 < S2, N, 1), (S1 > S2)), dtype=bool)

def VALUEWHEN(S, X):
    """当S条件成立时，取X的当前值，否则取VALUEWHEN的上个成立时的X值"""
    return pd.Series(np.where(S, X, np.nan)).ffill().values


#------------------ 扩展函数（来自第二个文件）-------------------------------------
def BACKSET(X, N):
    """
    属于未来函数，将当前位置到若干周期前的数据设为1。
    用法：BACKSET(X,N)，若X非0，则将当前位置到N周期前的数值设为1。
    例如：BACKSET(CLOSE>OPEN,2) 若收阳则将该周期及前一周期数值设为1，否则为0
    """
    result = np.zeros_like(X)
    for i in range(len(X)):
        if X[i] != 0:
            start_index = max(0, i - N + 1)
            result[start_index:i+1] = 1
    return result

def ALIGNRIGHT(X):
    """
    有效数据右对齐。
    用法：ALIGNRIGHT(X) 有效数据向右移动，左边空出来的周期填充无效值
    例如：TC:=IF(CURRBARSCOUNT=2 || CURRBARSCOUNT=5, DRAWNULL, C); XC:=ALIGNRIGHT(TC);
         删除了两天的收盘价，并将剩余数据右移
    """
    valid_indices = np.where(X != np.nan)[0]
    invalid_count = len(X) - len(valid_indices)
    result = np.empty_like(X)
    result[:] = np.nan
    result[invalid_count:len(valid_indices)+invalid_count] = X[valid_indices]
    return result

def BARSCOUNT(X):
    """
    有效数据周期数。
    用法：BARSCOUNT(X) 第一个有效数据到当前的间隔周期数
    注意：判断范围为指标或条件选股计算时公式使用的数据，
          如果给画线指标的数据少(比如没有按下箭头取更多K线)或给条件选股给的数据少，这个有效值也可能少
    """
    valid_indices = np.where(~np.isnan(X))[0]
    if len(valid_indices) == 0:
        return 0
    first_valid_index = valid_indices[0]
    current_index = len(X) - 1
    bars_count = current_index - first_valid_index + 1
    return bars_count

def BARSLASTS(X, N):
    """
    倒数第N次成立时距今的周期数。
    用法：BARSLASTS(X,N): X倒数第N满足到现在的周期数，N支持变量
    """
    valid_indices = np.where(~np.isnan(X))[0]
    if len(valid_indices) == 0:
        return -1
    last_n_indices = valid_indices[-N:]
    if len(last_n_indices) < N:
        return -1
    current_index = len(X) - 1
    bars_since_last_n = current_index - last_n_indices[-1] + 1
    return bars_since_last_n

def ZIG(CLOSE, X=0.05):
    """
    未来函数，计算之字转向。
    用法：ZIG(CLOSE, 0.05) 5%之字转向
    """
    ZIG_STATE_START = 0
    ZIG_STATE_RISE = 1
    ZIG_STATE_FALL = 2
    x = X
    k = CLOSE
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i] * (1 - x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i] * (1 + x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i + 1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value) / (peer_end_i - peer_start_i)
        for j in range(peer_end_i - peer_start_i + 1):
            z[j + peer_start_i] = start_value + a * j
    return pd.Series(z)
def calculate_zigzag(data, percent):
    """
    计算ZigZag指标。
    
    参数:
    data : pandas.DataFrame
        包含价格数据的DataFrame，必须包含'High'和'Low'列。
    percent : float
        百分比阈值，用于确定局部高点和低点。
        
    返回:
    zigzag : pandas.Series
        ZigZag指标值。
    """
    # 初始化ZigZag序列
    zigzag = pd.Series(index=data.index)
    
    # 初始方向为向上
    direction = 'up'
    
    # 遍历数据
    for i in range(1, len(data)):
        if direction == 'up':
            if data['high'][i] >= data['high'][i-1] * (1 + percent / 100):
                zigzag[i] = data['high'][i]
                direction = 'down'
            elif data['low'][i] <= data['low'][i-1] * (1 - percent / 100):
                zigzag[i] = data['low'][i]
                direction = 'down'
            else:
                zigzag[i] = zigzag[i-1]
        else:
            if data['low'][i] <= data['low'][i-1] * (1 - percent / 100):
                zigzag[i] = data['low'][i]
                direction = 'up'
            elif data['high'][i] >= data['high'][i-1] * (1 + percent / 100):
                zigzag[i] = data['high'][i]
                direction = 'up'
            else:
                zigzag[i] = zigzag[i-1]
    
    return zigzag

def TROUGHBARS(data, K, N, M):
    """
    计算前M个ZIG转向波谷到当前的周期数。
    
    参数:
    data : pandas.DataFrame
        包含价格数据的DataFrame，必须包含'High'和'Low'列。
    K : int
        百分比阈值，用于计算ZigZag指标。
    N : int
        未使用的参数，保留以符合函数签名。
    M : int
        前M个波谷的数量。
        
    返回:
    result : pandas.Series
        每个周期的前M个波谷到当前的周期数。
    """
    # 计算ZigZag指标
    zigzag = calculate_zigzag(data, K)
    
    # 找到波谷的位置
    valleys = zigzag[zigzag.notna() & (zigzag.shift(1) > zigzag)].index
    
    # 计算每个周期的前M个波谷到当前的周期数
    result = pd.Series(index=data.index)
    for i in range(len(data)):
        if i < len(valleys):
            result[i] = np.nan
        else:
            distances = [i - v for v in valleys[-M:]]
            result[i] = min(distances)
    
    return result
#df,DATE,CLOSE,OPEN,LOW,HIGH,VOL,CAPITAL,HSL,AMOUNT=set_start_data()
def params_data(test='test.txt',to_path='result.txt'):
    '''
    解析通达信公式
    test原来通达信公式文件
    to_path结果文件，python可以直接运行的文件
    '''
    test=open(r'{}'.format(test),'r',encoding='utf-8')
    result=test.readlines()
    columns=[]
    #挑选需要返回的数据
    for i in result:
        if ':' in i and ':=' not in i:
            name_list=i.split(':')
            columns.append(name_list[0])
    text=''.join(result)
    text1=text.replace(':=','=')
    text2=text1.replace(':','=')
    text4=text2.replace('&&',' and ')
    text5=text4.replace('||','or')
    text6=text5.replace('AND','and')
    text7=text6.replace('OR','or')
    text8=text7.replace('NOT','not')
    text9=text8.replace('DRAWNULL','None')
    text10=text9.replace(',NODRAW','')
    text11=text10.replace('MF0>MF1 and MF0>MF2','np.logical_and(MF0>MF1,MF0>MF2)')
    text12=text11.replace('MF0<MF1 and MF0<MF2','np.logical_and(MF0<MF1,MF0<MF2)')
    text3=text12.split(';')
    del text3[-1]
    fill=open(r'{}'.format(to_path),'w+',encoding='utf-8')
    fill.truncate()
    for i in text3:
        try:
            m=i.split('=')
            var=m[0]
            result=m[1]
            fill.write(var +'='+result)
        except:
           fill.write(var +'='+result)
    fill.write('\n')
    fill.write('return {}'.format(','.join(columns)))
    fill.close()
    print('公式分析成功')
def data_to_pandas(func=''):
    '''
    将函数的计算结果数据变成pandas数据,需要自动补充列名称
    func计算公式，例子data_to_pandas(CCI(CLOSE,HIGH,LOW)),CCI函数，也可以计算在返回
    print(data_to_pandas(CCI(CLOSE,HIGH,LOW)))
                   0       
    300          NaN       
    301          NaN       
    302          NaN       
    303          NaN       
    304          NaN       
    ...          ...       
    4634   10.314220       
    4635   68.462799       
    4636  106.677513       
    4637  116.201078       
    4638   85.026126  
    '''
    df=pd.DataFrame(func)
    #自己补充列明，列名称就是返回的参数
    columns=[]
    #df.columns=columns
    df1=df.T
    return df1
def CCI(CLOSE,HIGH,LOW,N=14):
    '''
    超卖超买类
    CCI商品路劲指标
    TYP赋值:(最高价+最低价+收盘价)/3
    输出CCI:(TYP-TYP的N日简单移动平均)*1000/(15*TYP的N日平均绝对偏差)
    '''
    TYP=(HIGH+LOW+CLOSE)/3
    result=(TYP-MA(TYP,N))*1000/(15*AVEDEV(TYP,N))
    return result
def KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3):
    '''
    超卖超买类
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出K:RSV的M1日[1日权重]移动平均
    输出D:K的M2日[1日权重]移动平均
    输出J:3*K-2*D
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M2,1)
    J=3*K-2*D
    return K,D,J
def MFI(CLOSE,HIGH,LOW,VOL,N=14):
    '''
    最近流量指标
    超卖超买类
    赋值: (最高价 + 最低价 + 收盘价)/3
    V1赋值:如果TYP>1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和/如果TYP<1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和
    输出资金流量指标:100-(100/(1+V1))
    '''
    TYP = (HIGH + LOW + CLOSE)/3
    V1=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N)  
    return 100-(100/(1+V1))  
def MTM(CLOSE,N=12,M=6):
    '''
    动量线指标
    超卖超买类
    输出动量线:收盘价-收盘价的有效数据周期数和N的较小值日前的收盘价
    输出MTMMA:MTM的M日简单移动平均
    '''
    MTM=CLOSE-REF(CLOSE,N)
    MTMMA=MA(MTM,M)
    return MTM,MTMMA
def EXPMEMA(data,N=20):
    '''
    data pandas.Series数据
    超卖超买类
    指数平滑移动平均
    '''
    result=data.ewm(com=N).mean()
    return result

def BARSCOUNT(CLOSE):
    df=pd.DataFrame()
    df['数据']=range(len(CLOSE))
    return df['数据']

def RSI(CLOSE, N1=6,N2=12,N3=24):
    '''
    相对强弱指标
    LC赋值:1日前的收盘价
    输出RSI1:收盘价-LC和0的较大值的N1日[1日权重]移动平均/收盘价-LC的绝对值的N1日[1日权重]移动平均*100
    输出RSI2:收盘价-LC和0的较大值的N2日[1日权重]移动平均/收盘价-LC的绝对值的N2日[1日权重]移动平均*100
    输出RSI3:收盘价-LC和0的较大值的N3日[1日权重]移动平均/收盘价-LC的绝对值的N3日[1日权重]移动平均*100
    '''
    LC=REF(CLOSE,1)
    RSI1=SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100
    RSI2=SMA(MAX(CLOSE-LC,0),N2,1)/SMA(ABS(CLOSE-LC),N2,1)*100
    RSI3=SMA(MAX(CLOSE-LC,0),N3,1)/SMA(ABS(CLOSE-LC),N3,1)*100
    return RSI1,RSI2,RSI3
def KD(CLOSE,LOW,HIGH,N=9,M1=3,M2=3):
    '''
    相对强弱指标
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出K:RSV的M1日[1日权重]移动平均
    输出D:K的M2日[1日权重]移动平均
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M2,1)
    return K,D
def SKDJ(CLOSE,LOW,HIGH,N=9,M=3):
    '''
    慢速随机指标
    LOWV赋值:N日内最低价的最低值
    HIGHV赋值:N日内最高价的最高值
    RSV赋值:(收盘价-LOWV)/(HIGHV-LOWV)*100的M日指数移动平均
    输出K:RSV的M日指数移动平均
    输出D:K的M日简单移动平均
    '''
    LOWV=LLV(LOW,N)
    HIGHV=HHV(HIGH,N)
    RSV=EMA((CLOSE-LOWV)/(HIGHV-LOWV)*100,M)
    K=EMA(RSV,M)
    D=MA(K,M)
    return K,D
def UDL(CLOSE,N1=3,N2=5,N3=10,N4=20,M=6):
    '''
    引力线
    输出引力线:(收盘价的N1日简单移动平均+收盘价的N2日简单移动平均+收盘价的N3日简单移动平均+收盘价的N4日简单移动平均)/4
    输出MAUDL:UDL的M日简单移动平均
    '''
    UDL=(MA(CLOSE,N1)+MA(CLOSE,N2)+MA(CLOSE,N3)+MA(CLOSE,N4))/4
    MAUDL=MA(UDL,M)
    return UDL,MAUDL
def WR(CLOSE,LOW,HIGH,N=10,N1=6):
    '''
    威廉指标
    输出WR1:100*(N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)
    输出WR2:100*(N1日内最高价的最高值-收盘价)/(N1日内最高价的最高值-N1日内最低价的最低值)
    '''
    WR1=100*(HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))
    WR2=100*(HHV(HIGH,N1)-CLOSE)/(HHV(HIGH,N1)-LLV(LOW,N1))
    return WR1,WR2
def LWR(CLOSE,LOW,HIGH,N=9,M1=3,M2=3):
    '''
    LWR指标
    RSV赋值: (N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出LWR1:RSV的M1日[1日权重]移动平均
    输出LWR2:LWR1的M2日[1日权重]移动平均
    '''
    RSV= (HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))*100
    LWR1=SMA(RSV,M1,1)
    LWR2=SMA(LWR1,M2,1)
    return LWR1,LWR2
def MEMA(S,N,M=1):
    '''
    平滑移动平均
    '''
    return SMA(S,N,M)
def MARSI(CLOSE,M1=10,M2=6):
    '''
    相对强弱平均线
    DIF赋值:收盘价-1日前的收盘价
    VU赋值:如果DIF>=0,返回DIF,否则返回0
    VD赋值:如果DIF<0,返回-DIF,否则返回0
    MAU1赋值:VU的M1日平滑移动平均
    MAD1赋值:VD的M1日平滑移动平均
    MAU2赋值:VU的M2日平滑移动平均
    '''
    DIF=CLOSE-REF(CLOSE,1)
    VU=IF(DIF>=0,DIF,0)
    VD=IF(DIF<0,-DIF,0)
    MAU1=MEMA(VU,M1)
    MAD1=MEMA(VD,M1)
    MAU2=MEMA(VU,M2)
    MAD2=MEMA(VD,M2)
    RSI1=MA(100*MAU1/(MAU1+MAD1),M1)
    RSI2=MA(100*MAU2/(MAU2+MAD2),M2)
    return RSI1,RSI2
def BIAS_QL(CLOSE,N=6,M=6):
    '''
    乖离率-传统版
    输出乖离率 :(收盘价-收盘价的N日简单移动平均)/收盘价的N日简单移动平均*100
    输出BIASMA :乖离率的M日简单移动平均
    '''
    BIAS=(CLOSE-MA(CLOSE,N))/MA(CLOSE,N)*100
    BIASMA=MA(BIAS,M)
    return BIAS,BIASMA
def BIAS(CLOSE,N1=6,N2=12,N3=24):
    '''
    乖离率
    输出BIAS1 :(收盘价-收盘价的N1日简单移动平均)/收盘价的N1日简单移动平均*100
    输出BIAS2 :(收盘价-收盘价的N2日简单移动平均)/收盘价的N2日简单移动平均*100
    输出BIAS3 :(收盘价-收盘价的N3日简单移动平均)/收盘价的N3日简单移动平均*100
    '''
    BIAS1=(CLOSE-MA(CLOSE,N1))/MA(CLOSE,N1)*100
    BIAS2=(CLOSE-MA(CLOSE,N2))/MA(CLOSE,N2)*100
    BIAS3=(CLOSE-MA(CLOSE,N3))/MA(CLOSE,N3)*100
    return BIAS1,BIAS2,BIAS3
def BIAS36(CLOSE,M=6):
    '''
    三六乖离
    输出三六乖离:收盘价的3日简单移动平均-收盘价的6日简单移动平均
    输出BIAS612:收盘价的6日简单移动平均-收盘价的12日简单移动平均
    输出MABIAS:BIAS36的M日简单移动平均
    '''
    BIAS36=MA(CLOSE,3)-MA(CLOSE,6)
    BIAS612=MA(CLOSE,6)-MA(CLOSE,12)
    MABIAS=MA(BIAS36,M)
    return BIAS36,BIAS612,MABIAS
def ACCER(CLOSE,N=8):
    '''
    幅度涨速
    输出幅度涨速:收盘价的N日线性回归斜率/收盘价
    '''
    ACCER=SLOPE(CLOSE,N)/CLOSE
    return ACCER
#需要编写活力函数
def CYD(CLOSE,CAPITAL,N=21):
    '''
    承接因子
    输出CYDS:以收盘价计算的获利盘比例/(成交量(手)/当前流通股本(手))
    输出CYDN:以收盘价计算的获利盘比例/成交量(手)/当前流通股本(手)的N日简单移动平均
    '''
    CYDS=WINNER(CLOSE)/(VOL/CAPITAL)
    CYDN=WINNER(CLOSE)/MA(VOL/CAPITAL,N);   
    return CYDS,CYDN
def CYF(HSL,N=21):
    '''
    市场能量
    输出市场能量:100-100/(1+换手线的N日指数移动平均)
    '''
    CYF=100-100/(1+EMA(HSL,N))
    return CYF
def SFL(CLOSE,VOL):
    '''
    分水岭
    输出SWL:(收盘价的5日指数移动平均*7+收盘价的10日指数移动平均*3)/10
    输出SWS:以1和100*(成交量(手)的5日累和/(3*当前流通股本(手)))的较大值为权重收盘价的12日指数移动平均的动态移动平均
    '''
    SWL=(EMA(CLOSE,5)*7+EMA(CLOSE,10)*3)/10
    IF(100*(SUM(VOL,5)/(3*CAPITAL)>1),100*(SUM(VOL,5)/(3*CAPITAL)),1)
    SWS=DMA(EMA(CLOSE,12),MAX(1,1))
    return SWL,SWS
def ATR(CLOSE,HIGH,LOW,N=14):
    '''
    真实波幅
    输出MTR:(最高价-最低价)和1日前的收盘价-最高价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值
    输出真实波幅:MTR的N日简单移动平均
    '''
    MTR=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW))
    ATR=MA(MTR,N)
    return MTR,ATR
def DKX(CLOSE,LOW,OPEN,HIGH,M=10):
    '''
    多空线
    MID赋值:(3*收盘价+最低价+开盘价+最高价)/6
    输出多空线:(20*MID+19*1日前的MID+18*2日前的MID+17*3日前的MID+16*4日前的MID+15*5日前的MID+14*6日前的MID+13*7日前的MID+12*8日前的MID+11*9日前的MID+10*10日前的MID+9*11日前的MID+8*12日前的MID+7*13日前的MID+6*14日前的MID+5*15日前的MID+4*16日前的MID+3*17日前的MID+2*18日前的MID+20日前的MID)/210
    输出MADKX:DKX的M日简单移动平均
    '''
    MID=(3*CLOSE+LOW+OPEN+HIGH)/6
    DKX=(20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
    16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
    13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
    10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
    7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
    4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210
    MADKX=MA(DKX,M)
    return DKX,MADKX
#*******************************************
#******************************************
#趋势类型
def ASI(OPEN,CLOSE,HIGH,LOW,M1=26,M2=10):   
    '''
    振动升降指标
    '''        
    LC=REF(CLOSE,1)
    AA=ABS(HIGH-LC)   
    BB=ABS(LOW-LC)
    CC=ABS(HIGH-REF(LOW,1))  
    DD=ABS(LC-REF(OPEN,1))
    R=IF( (AA>BB) & (AA>CC),AA+BB/2+DD/4,IF( (BB>CC) & (BB>AA),BB+AA/2+DD/4,CC+DD/4))
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1))
    SI=16*X/R*MAX(AA,BB)
    ASI=SUM(SI,M1)
    ASIT=MA(ASI,M2)
    return ASI,ASIT  
def CHO(CLOSE,OPEN,LOW,HIGH,VOL,N1=10,N2=20,M=6):
    '''
    佳庆指标
    MID赋值:成交量(手)*(2*收盘价-最高价-最低价)/(最高价+最低价)的历史累和
    输出佳庆指标:MID的N1日简单移动平均-MID的N2日简单移动平均
    输出MACHO:CHO的M日简单移动平均
    '''
    MID=SUM(VOL*(2*CLOSE-HIGH-LOW)/(HIGH+LOW),0)
    CHO=MA(MID,N1)-MA(MID,N2)
    MACHO=MA(CHO,M)
    return CHO,MACHO
def DMA_XT(CLOSE,N1=10,N2=50,M=10):
    '''
    平均差
    输出DIF:收盘价的N1日简单移动平均-收盘价的N2日简单移动平均
    输出DIFMA:DIF的M日简单移动平均
    '''
    DIF=MA(CLOSE,N1)-MA(CLOSE,N2)
    DIFMA=MA(DIF,M)
    return DIF,DIFMA
def DMI(CLOSE,HIGH,LOW,N=14,M=6):
    '''
    趋向指标
    MTR赋值:最高价-最低价和最高价-1日前的收盘价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值的N日累和
    赋值:最高价-1日前的最高价
    赋值:1日前的最低价-最低价
    DMP赋值:如果HD>0并且HD>LD,返回HD,否则返回0的N日累和
    DMM赋值:如果LD>0并且LD>HD,返回LD,否则返回0的N日累和
    输出PDI: DMP*100/MTR
    输出MDI: DMM*100/MTR
    输出ADX: MDI-PDI的绝对值/(MDI+PDI)*100的M日简单移动平均
    输出ADXR:(ADX+M日前的ADX)/2
    '''
    MTR=SUM(MAX(MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1))),ABS(REF(CLOSE,1)-LOW)),N)
    HD =HIGH-REF(HIGH,1)
    LD =REF(LOW,1)-LOW
    list_A=[]
    list_B=[]
    for m,n in zip(LD>0,LD>HD):
        if m==n and m==True:
            list_A.append(True)
        else:
            list_A.append(False)
    for i,j in zip(LD>0,LD>HD):
        if i==j and i==True:
            list_B.append(True)
        else:
            list_B.append(False)
    DMP=SUM(IF(list_A,HD,0),N)
    DMM=SUM(IF(list_B,LD,0),N)
    PDI= DMP*100/MTR
    MDI=DMM*100/MTR
    ADX=MA(ABS(MDI-PDI)/(MDI+PDI)*100,M)
    ADXR=(ADX+REF(ADX,M))/2
    return PDI,MDI,ADX,ADXR
def DPO(CLOSE,N=21,M=6):
    '''
    区间震荡线
    输出区间震荡线:收盘价-N/2+1日前的收盘价的N日简单移动平均
    输出MADPO:DPO的M日简单移动平均
    '''
    #print(REF(MA(CLOSE,N),N/2))
    DPO=CLOSE-REF(MA(CLOSE,7),6)
    MADPO=MA(DPO,M)
    return DPO,MADPO
def EMV(HIGH,LOW,VOL,N=14,M=9):
    '''
    简易波动指标
    VOLUME赋值:成交量(手)的N日简单移动平均/成交量(手)
    MID赋值:100*(最高价+最低价-1日前的最高价+最低价)/(最高价+最低价)
    输出EMV:MID*VOLUME*(最高价-最低价)/最高价-最低价的N日简单移动平均的N日简单移动平均
    输出MAEMV:EMV的M日简单移动平均
    '''
    VOLUME=MA(VOL,N)/VOL
    MID=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW)
    EMV=MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N)
    MAEMV=MA(EMV,M)
    return EMV,MAEMV
def MACD(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    平滑异同平均线
    输出DIF:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:(DIF-DEA)*2,COLORSTICK
    '''
    DIF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIF,MID)
    MACD=(DIF-DEA)*2
    return DIF,DEA,MACD

def VMACD(VOL,SHORT=12,LONG=26,MID=9):
    '''
    量平滑异同平均线
    输出DIF:成交量(手)的SHORT日指数移动平均-成交量(手)的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:DIF-DEA,COLORSTICK
    '''
    DIF=EMA(VOL,SHORT)-EMA(VOL,LONG)
    DEA=EMA(DIF,MID)
    MACD=DIF-DEA
    return DIF,DEA,MACD
def SMACD(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    单线平滑异同平均线
    DIF赋值:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:DIF,COLORSTICK
    '''
    DIF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIF,MID)
    MACD=DIF
    return DEA,MACD
def QACD(CLOSE,N1=12,N2=12,M=9):
    '''
    快速异同平均线
    输出DIF:收盘价的N1日指数移动平均-收盘价的N2日指数移动平均
    输出平滑异同平均线:DIF的M日指数移动平均
    输出DDIF:DIF-MACD
    '''
    DIF=EMA(CLOSE,N1)-EMA(CLOSE,N2)
    MACD=EMA(DIF,M)
    DDIF=DIF-MACD
    return DIF,MACD,DDIF
def TRIX(CLOSE,N=12,M=9):
    '''
    三重指数平均线
    MTR赋值:收盘价的N日指数移动平均的N日指数移动平均的N日指数移动平均
    输出三重指数平均线:(MTR-1日前的MTR)/1日前的MTR*100
    输出MATRIX:TRIX的M日简单移动平均 
    '''
    MTR=EMA(EMA(EMA(CLOSE,N),N),N)
    TRIX=(MTR-REF(MTR,1))/REF(MTR,1)*100
    MATRIX=MA(TRIX,M) 
    return TRIX,MATRIX
def UOS(CLOSE,HIGH,LOW,N1=7,N2=14,N3=28,M=6):
    '''
    终极指标
    TH赋值:最高价和1日前的收盘价的较大值
    TL赋值:最低价和1日前的收盘价的较小值
    ACC1赋值:收盘价-TL的N1日累和/TH-TL的N1日累和
    ACC2赋值:收盘价-TL的N2日累和/TH-TL的N2日累和
    ACC3赋值:收盘价-TL的N3日累和/TH-TL的N3日累和
    输出终极指标:(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3)
    输出MAUOS:UOS的M日指数平滑移动平均
    '''
    TH=MAX(HIGH,REF(CLOSE,1))
    TL=MIN(LOW,REF(CLOSE,1))
    ACC1=SUM(CLOSE-TL,N1)/SUM(TH-TL,N1)
    ACC2=SUM(CLOSE-TL,N2)/SUM(TH-TL,N2)
    ACC3=SUM(CLOSE-TL,N3)/SUM(TH-TL,N3)
    UOS=(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3)
    MAUOS=EXPMEMA(pd.Series(UOS),M)
    return UOS,np.array(MAUOS)
def VTP(CLOSE,VOL,N=51,M=6):
    '''
    量价曲线
    输出量价曲线:成交量(手)*(收盘价-1日前的收盘价)/1日前的收盘价的N日累和
    输出MAVPT:VPT的M日简单移动平均
    '''
    VPT=SUM(VOL*(CLOSE-REF(CLOSE,1))/REF(CLOSE,1),N)
    MAVP=MA(VPT,M)
    return VPT,MAVP
def WVAD(CLOSE,OPEN,HIGH,LOW,VOL,N=24,M=6):
    '''
    威廉变异离散量
    输出WVAD:(收盘价-开盘价)/(最高价-最低价)*成交量(手)的N日累和/10000
    输出MAWVAD:WVAD的M日简单移动平均
    '''
    WVAD=SUM((CLOSE-OPEN)/(HIGH-LOW)*VOL,N)/10000
    MAWVAD=MA(WVAD,M)
    return WVAD,MAWVAD
def DBQR(CLOSE,INDEXC,N=5,M1=10,M2=20,M3=60):
    '''
    对比强弱(需下载日线)
    输出ZS:(大盘的收盘价-N日前的大盘的收盘价)/N日前的大盘的收盘价
    输出GG:(收盘价-N日前的收盘价)/N日前的收盘价
    输出MADBQR1:GG的M1日简单移动平均
    输出MADBQR2:GG的M2日简单移动平均
    输出MADBQR3:GG的M3日简单移动平均
    '''
    ZS=(INDEXC-REF(INDEXC,N))/REF(INDEXC,N)
    GG=(CLOSE-REF(CLOSE,N))/REF(CLOSE,N)
    MADBQR1=MA(GG,M1)
    MADBQR2=MA(GG,M2)
    MADBQR3=MA(GG,M3)
    return ZS,GG,MADBQR1,MADBQR2,MADBQR3
def JS(CLOSE,N=5,M1=5,M2=10,M3=20):
    '''
    加数线
    输出加速线:100*(收盘价-N日前的收盘价)/(N*N日前的收盘价)
    输出MAJS1:JS的M1日简单移动平均
    输出MAJS2:JS的M2日简单移动平均
    输出MAJS3:JS的M3日简单移动平均
    '''
    JS=100*(CLOSE-REF(CLOSE,N))/(N*REF(CLOSE,N))
    MAJS1=MA(JS,M1)
    MAJS2=MA(JS,M2)
    MAJS3=MA(JS,M3)
    return JS,MAJS1,MAJS2,MAJS3
def CYE(CLOSE):
    '''
    市场趋势
    MAL赋值:收盘价的5日简单移动平均
    MAS赋值:收盘价的20日简单移动平均的5日简单移动平均
    输出CYEL:(MAL-1日前的MAL)/1日前的MAL*100
    输出CYES:(MAS-1日前的MAS)/1日前的MAS*100
    '''
    MAL=MA(CLOSE,5)
    MAS=MA(MA(CLOSE,20),5)
    CYEL=(MAL-REF(MAL,1))/REF(MAL,1)*100
    CYES=(MAS-REF(MAS,1))/REF(MAS,1)*100
    return CYEL,CYES
def QR(CLOSE,INDEXC,N=21):
    '''
    强弱指标(需下载日线)
    NN赋值:收盘价的有效数据周期数和N的较小值
    输出 个股: (收盘价-NN日前的收盘价)/NN日前的收盘价*100
    输出 大盘: (大盘的收盘价-NN日前的大盘的收盘价)/NN日前的大盘的收盘价*100
    输出 强弱值:个股-大盘的2日指数移动平均,COLORSTICK
    '''
    NN=MIN(BARSCOUNT(CLOSE),N)
    GG=(CLOSE-REF(CLOSE,NN))/REF(CLOSE,NN)*100
    DP=(INDEXC-REF(INDEXC,NN))/REF(INDEXC,NN)*100
    value=EMA(GG-DP,2)
    return GG,DP,value
def GDX(CLOSE,HIGH,LOW,N=30,M=9):
    '''
    轨道线
    AA赋值:(2*收盘价+最高价+最低价)/4-收盘价的N日简单移动平均的绝对值/收盘价的N日简单移动平均
    输出 轨道:以AA为权重收盘价的动态移动平均
    输出压力线:(1+M/100)*轨道
    输出 支撑线:(1-M/100)*轨道
    '''
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N)
    轨道 =DMA(AA,0.5)
    压力线=(1+M/100)*轨道 
    支撑线=(1-M/100)*轨道
    return 轨道,压力线,支撑线
def JLHB(CLOSE,LOW,HIGH,N=7,M=5):
    '''
    绝路航标
    VAR1赋值:(收盘价-60日内最低价的最低值)/(60日内最高价的最高值-60日内最低价的最低值)*80
    输出 B:VAR1的N日[1日权重]移动平均
    输出 VAR2:B的M日[1日权重]移动平均
    输出 绝路航标:如果B上穿VAR2ANDB<40,返回50,否则返回0
    '''
    VAR1=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80
    B=SMA(VAR1,N,1)
    VAR2=SMA(B,M,1)
    绝路航标=IF(np.logical_and(B,VAR2),50,0)
    return B,VAR2,绝路航标
#********************************************
#********************************************
#能量类型
def BRAR(OPEN,HIGH,LOW,CLOSE,N=26):
    '''
    情绪指标
    输出BR:0和最高价-1日前的收盘价的较大值的N日累和/0和1日前的收盘价-最低价的较大值的N日累和*100
    输出AR:最高价-开盘价的N日累和/开盘价-最低价的N日累和*100
    '''
    BR=SUM(MAX(0,HIGH-REF(CLOSE,1)),N)/SUM(MAX(0,REF(CLOSE,1)-LOW),N)*100
    AR=SUM(HIGH-OPEN,N)/SUM(OPEN-LOW,N)*100
    return BR,AR
def CR(HIGH,LOW,N=26,M1=10,M2=20,M3=40,M4=60):
    '''
    带状能量线
    MID赋值:1日前的最高价+最低价/2
    输出带状能量线:0和最高价-MID的较大值的N日累和/0和MID-最低价的较大值的N日累和*100
    输出MA1:M1/2.5+1日前的CR的M1日简单移动平均
    输出均线:M2/2.5+1日前的CR的M2日简单移动平均
    输出MA3:M3/2.5+1日前的CR的M3日简单移动平均
    输出MA4:M4/2.5+1日前的CR的M4日简单移动平均
    '''
    MID=REF(HIGH+LOW,1)/2
    CR=SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100
    MA1=pd.DataFrame(CR).shift(11).mean()
    MA2=pd.DataFrame(CR).shift(5).mean()
    MA3=pd.DataFrame(CR).shift(17).mean()
    MA4=pd.DataFrame(CR).shift(25).mean()
    return CR,MA1,MA2,MA3,MA4
def MASS(HIGH,LOW,N1=9,N2=25,M=6):
    '''
    梅斯线
    输出梅斯线:最高价-最低价的N1日简单移动平均/最高价-最低价的N1日简单移动平均的N1日简单移动平均的N2日累和
    输出MAMASS:MASS的M日简单移动平均
    '''
    MASS=SUM(MA(HIGH-LOW,N1)/MA(MA(HIGH-LOW,N1),N1),N2)
    MAMASS=MA(MASS,M)
    return MASS,MAMASS
def PSY(CLOSE,N=12,M=6):
    '''
    心理线
    输出PSY:统计N日中满足收盘价>1日前的收盘价的天数/N*100
    输出PSYMA:PSY的M日简单移动平均
    '''
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return PSY,PSYMA
def VR(CLOSE,VOL,N=26,M=6):
    '''
    成交量变异率
    TH赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回0的N日累和
    TL赋值:如果收盘价<1日前的收盘价,返回成交量(手),否则返回0的N日累和
    TQ赋值:如果收盘价=1日前的收盘价,返回成交量(手),否则返回0的N日累和
    输出VR:100*(TH*2+TQ)/(TL*2+TQ)
    输出MAVR:VR的M日简单移动平均
    '''
    TH=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N)
    TL=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N)
    TQ=SUM(IF(CLOSE==REF(CLOSE,1),VOL,0),N)
    VR=100*(TH*2+TQ)/(TL*2+TQ)
    MAVR=MA(VR,M)
    return VR,MAVR
def WAD(CLOSE,LOW,HIGH,M=30):
    '''
    威廉多空力度线
    MIDA赋值:收盘价-1日前的收盘价和最低价的较小值
    MIDB赋值:如果收盘价<1日前的收盘价,返回收盘价-1日前的收盘价和最高价的较大值,否则返回0
    输出威廉多空力度线:如果收盘价>1日前的收盘价,返回MIDA,否则返回MIDB的历史累和
    输出MAWAD:WAD的M日简单移动平均
    '''
    MIDA=CLOSE-MIN(REF(CLOSE,1),LOW)
    MIDB=IF(CLOSE<REF(CLOSE,1),CLOSE-MAX(REF(CLOSE,1),HIGH),0)
    WAD=SUM(IF(CLOSE>REF(CLOSE,1),MIDA,MIDB),0)
    MAWAD=MA(WAD,M)
    return WAD,MAWAD
def EXPMEMA(CLOSE,M=5):
    '''
    指数平滑
    '''
    return pd.Series(CLOSE).ewm(span=M, adjust=False).mean().values
def PCNT(CLOSE,M=5):
    '''
    输出幅度比:(收盘价-1日前的收盘价)/收盘价*100
    输出MAPCNT:PCNT的M日指数平滑移动平均
    '''
    PCNT=(CLOSE-REF(CLOSE,1))/CLOSE*100
    MAPCNT=EXPMEMA(PCNT,M)
    return PCNT,MAPCNT
def CYR(AMOUNT,VOL,N=13,M=5):
    '''
    市场强弱
    AMOUNT成交量=price*volume
    DIVE赋值:0.01*成交额(元)的N日指数移动平均/成交量(手)的N日指数移动平均
    输出市场强弱:(DIVE/1日前的DIVE-1)*100
    输出MACYR:CYR的M日简单移动平均
    '''
    DIVE=0.01*EMA(AMOUNT,N)/EMA(VOL,N)
    CYR=(DIVE/REF(DIVE,1)-1)*100
    MACYR=MA(CYR,M)
    return CYR,MACYR
#*********************************************
#*********************************************
#能量型
def AMO(AMOUNT,M1=5,M2=10):
    '''
    成交金额
    输出AMOW:成交额(元)/10000.0,VOLSTICK
    输出AMO1:AMOW的M1日简单移动平均
    输出AMO2:AMOW的M2日简单移动平均
    '''
    AMOW=AMOUNT/10000.0
    AMO1=MA(AMOW,M1)
    AMO2=MA(AMOW,M2)
    return AMOW,AMO1,AMO2
def OBV(VOL,CLOSE,M=30):
    '''
    累积能量线
    VA赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回-成交量(手)
    输出OBV:如果收盘价=1日前的收盘价,返回0,否则返回VA的历史累和
    输出MAOBV:OBV的M日简单移动平均
    '''
    VA=IF(CLOSE>REF(CLOSE,1),VOL,-VOL)
    OBV=SUM(IF(CLOSE==REF(CLOSE,1),0,VA),0)
    MAOBV=MA(OBV,M)
    return OBV,MAOBV
def VOL_XT(VOL,M1=5,M2=10):
    '''
    成交量
    输出VOLUME:成交量(手),VOLSTICK
    输出MAVOL1:VOLUME的M1日简单移动平均
    输出MAVOL2:VOLUME的M2日简单移动平均
    '''
    VOLUME=VOL
    MAVOL1=MA(VOLUME,M1)
    MAVOL2=MA(VOLUME,M2)
    return MAVOL1,MAVOL2
def VRSI(VOL,N1=6,N2=12,N3=24):
    '''
    相对强弱量
    LC赋值:1日前的成交量(手)
    输出RSI1:成交量(手)-LC和0的较大值的N1日[1日权重]移动平均/成交量(手)-LC的绝对值的N1日[1日权重]移动平均*100
    输出RSI2:成交量(手)-LC和0的较大值的N2日[1日权重]移动平均/成交量(手)-LC的绝对值的N2日[1日权重]移动平均*100
    输出RSI3:成交量(手)-LC和0的较大值的N3日[1日权重]移动平均/成交量(手)-LC的绝对值的N3日[1日权重]移动平均*100
    '''
    LC=REF(VOL,1)
    RSI1=SMA(MAX(VOL-LC,0),N1,1)/SMA(ABS(VOL-LC),N1,1)*100
    RSI2=SMA(MAX(VOL-LC,0),N2,1)/SMA(ABS(VOL-LC),N2,1)*100
    RSI3=SMA(MAX(VOL-LC,0),N3,1)/SMA(ABS(VOL-LC),N3,1)*100
    return RSI1,RSI2,RSI3
def HSL(HSL,N=5):
    '''
    换手线
    '''
    HSL=HSL
    MAHSL=MA(HSL,N)
    return HSL,MAHSL
#******************************************
#******************************************
#均线系统
def MA_XT(CLOSE,M1=5,M2=10,M3=20,M4=60):
    '''
    均线
    输出MA1:收盘价的M1日简单移动平均
    输出均线:收盘价的M2日简单移动平均
    输出MA3:收盘价的M3日简单移动平均
    输出MA4:收盘价的M4日简单移动平均
    输出MA5:收盘价的M5日简单移动平均
    输出MA6:收盘价的M6日简单移动平均
    输出MA7:收盘价的M7日简单移动平均
    输出MA8:收盘价的M8日简单移动平均
    '''
    MA1=MA(CLOSE,M1)
    MA2=MA(CLOSE,M2)
    MA3=MA(CLOSE,M3)
    MA4=MA(CLOSE,M4)
    return MA1,MA2,MA3,MA4
def MA2(CLOSE,M1=5,M2=10,M3=20,M4=60,M5=120,M6=240,M7=360,M8=420,M9=680,M10=720):
    '''
    均线2
    输出MA1:收盘价的M1日简单移动平均
    输出均线:收盘价的M2日简单移动平均
    输出MA3:收盘价的M3日简单移动平均
    输出MA4:收盘价的M4日简单移动平均
    输出MA5:收盘价的M5日简单移动平均
    输出MA6:收盘价的M6日简单移动平均
    输出MA7:收盘价的M7日简单移动平均
    输出MA8:收盘价的M8日简单移动平均
    输出MA9:收盘价的M9日简单移动平均
    输出MA10:收盘价的M10日简单移动平均
    '''
    MA1=MA(CLOSE,M1)
    MA2=MA(CLOSE,M2)
    MA3=MA(CLOSE,M3)
    MA4=MA(CLOSE,M4)
    MA5=MA(CLOSE,M5)
    MA6=MA(CLOSE,M6)
    MA7=MA(CLOSE,M7)
    MA8=MA(CLOSE,M8)
    MA9=MA(CLOSE,M9)
    MA10=MA(CLOSE,M10)
    return MA1,MA2,MA3,MA4,MA5,MA6,MA7,MA8,MA8,MA9,MA10
def ACD(CLOSE,HIGH,LOW,M=20):
    '''
    升降线
    LC赋值:1日前的收盘价
    DIF赋值:收盘价-如果收盘价>LC,返回最低价和LC的较小值,否则返回最高价和LC的较大值
    输出升降线:如果收盘价=LC,返回0,否则返回DIF的历史累和
    输出MAACD:ACD的M日指数平滑移动平均
    '''
    LC=REF(CLOSE,1)
    DIF=CLOSE-IF(CLOSE>LC,MIN(LOW,LC),MAX(HIGH,LC))
    ACD=SUM(IF(CLOSE==LC,0,DIF),0)
    MAACD=EXPMEMA(ACD,M)
    return ACD,MAACD
def BBI(CLOSE,M1=3,M2=6,M3=12,M4=24):
    '''
    多空均线
    输出多空均线:(收盘价的M1日简单移动平均+收盘价的M2日简单移动平均+收盘价的M3日简单移动平均+收盘价的M4日简单移动平均)/4
    '''
    BBI=(MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4
    return BBI
def EXPMA(CLOSE,M1=12,M2=50):
    '''
    指数平均线
    输出EXP1:收盘价的M1日指数移动平均
    输出EXP2:收盘价的M2日指数移动平均
    '''
    EXP1=EMA(CLOSE,M1)
    EXP2=EMA(CLOSE,M2)
    return EXP1,EXP2
def HMA(HIGH,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    高价平均线
    输出HMA1:最高价的M1日简单移动平均
    输出HMA2:最高价的M2日简单移动平均
    输出HMA3:最高价的M3日简单移动平均
    输出HMA4:最高价的M4日简单移动平均
    输出HMA5:最高价的M5日简单移动平均
    '''
    HMA1=MA(HIGH,M1)
    HMA2=MA(HIGH,M2)
    HMA3=MA(HIGH,M3)
    HMA4=MA(HIGH,M4)
    HMA5=MA(HIGH,M5)
    return HMA1,HMA2,HMA3,HMA4,HMA5
def LMA(LOW,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    低价平均线
    输出LMA1:最低价的M1日简单移动平均
    输出LMA2:最低价的M2日简单移动平均
    输出LMA3:最低价的M3日简单移动平均
    输出LMA4:最低价的M4日简单移动平均
    输出LMA5:最低价的M5日简单移动平均
    '''
    LMA1=MA(LOW,M1)
    LMA2=MA(LOW,M2)
    LMA3=MA(LOW,M3)
    LMA4=MA(LOW,M4)
    LMA5=MA(LOW,M5)
    return LMA1,LMA2,LMA3,LMA4,LMA5
def VMA(HIGH,OPEN,LOW,CLOSE,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    变异平均线
    VV赋值:(最高价+开盘价+最低价+收盘价)/4
    输出VMA1:VV的M1日简单移动平均
    输出VMA2:VV的M2日简单移动平均
    输出VMA3:VV的M3日简单移动平均
    输出VMA4:VV的M4日简单移动平均
    输出VMA5:VV的M5日简单移动平均
    '''
    VV=(HIGH+OPEN+LOW+CLOSE)/4
    VMA1=MA(VV,M1)
    VMA2=MA(VV,M2)
    VMA3=MA(VV,M3)
    VMA4=MA(VV,M4)
    VMA5=MA(VV,M5)
    return VMA1,VMA2,VMA3,VMA4,VMA5
def AMV(OPEN,CLOSE,VOL,M1=5,M2=13,M3=34,M4=60):
    '''
    成本均线
    AMOV赋值:成交量(手)*(开盘价+收盘价)/2
    输出AMV1:AMOV的M1日累和/成交量(手)的M1日累和
    输出AMV2:AMOV的M2日累和/成交量(手)的M2日累和
    输出AMV3:AMOV的M3日累和/成交量(手)的M3日累和
    输出AMV4:AMOV的M4日累和/成交量(手)的M4日累和
    '''
    AMOV=VOL*(OPEN+CLOSE)/2
    AMV1=SUM(AMOV,M1)/SUM(VOL,M1)
    AMV2=SUM(AMOV,M2)/SUM(VOL,M2)
    AMV3=SUM(AMOV,M3)/SUM(VOL,M3)
    AMV4=SUM(AMOV,M4)/SUM(VOL,M4)
    return AMV1,AMV2,AMV3,AMV4
def BBIBOLL(CLOSE,N=11,M=6):
    '''
    多空布林线
    CV赋值:收盘价
    输出多空布林线:(CV的3日简单移动平均+CV的6日简单移动平均+CV的12日简单移动平均+CV的24日简单移动平均)/4
    输出UPR:BBIBOLL+M*BBIBOLL的N日估算标准差
    输出DWN:BBIBOLL-M*BBIBOLL的N日估算标准差
    '''
    CV=CLOSE
    BBIBOLL=(MA(CV,3)+MA(CV,6)+MA(CV,12)+MA(CV,24))/4
    UPR=BBIBOLL+M*STD(BBIBOLL,N)
    DWN=BBIBOLL-M*STD(BBIBOLL,N)
    return BBIBOLL,UPR,DWN
def ALLIGAT(HIGH,LOW):
    '''
    鳄鱼线
    NN赋值:(最高价+最低价)/2
    输出上唇:3日前的NN的5日简单移动平均,COLOR40FF40
    输出牙齿:5日前的NN的8日简单移动平均,COLOR0000C0
    输出下颚:8日前的NN的13日简单移动平均,COLORFF4040
    '''
    H=HIGH
    L=LOW
    NN=(H+L)/2
    上唇=REF(MA(NN,5),3)
    牙齿=REF(MA(NN,8),5)
    下颚=REF(MA(NN,13),8)
    return 上唇,牙齿,下颚
def GMMA(CLOSE):
    '''
    顾比均线
    '''
    MA3=EMA(CLOSE,3)
    MA5=EMA(CLOSE,5)
    MA8=EMA(CLOSE,8)
    MA10=EMA(CLOSE,10)
    MA12=EMA(CLOSE,12)
    MA15=EMA(CLOSE,15)
    MA30=EMA(CLOSE,30)
    MA35=EMA(CLOSE,35)
    MA40=EMA(CLOSE,40)
    MA45=EMA(CLOSE,45)
    MA50=EMA(CLOSE,50)
    MA60=EMA(CLOSE,60)
    return MA3,MA5,MA8,MA10,MA12,MA15,MA30,MA35,MA40,MA45,MA50,MA60
#*******************************************
#*******************************************
#路径类
def BOLL(CLOSE,M=20):
    '''
    布林线
    输出BOLL:收盘价的M日简单移动平均
    输出UB:BOLL+2*收盘价的M日估算标准差
    输出LB:BOLL-2*收盘价的M日估算标准差
    '''
    BOLL=MA(CLOSE,M)
    UB=BOLL+2*STD(CLOSE,M)
    LB=BOLL-2*STD(CLOSE,M)
    return BOLL,UB,LB
def PBX(CLOSE,M1=4,M2=6,M3=9,M4=13,M5=18,M6=24):
    '''
    瀑布线
    输出PBX1:(收盘价的M1日指数移动平均+收盘价的M1*2日简单移动平均+收盘价的M1*4日简单移动平均)/3
    输出PBX2:(收盘价的M2日指数移动平均+收盘价的M2*2日简单移动平均+收盘价的M2*4日简单移动平均)/3
    输出PBX3:(收盘价的M3日指数移动平均+收盘价的M3*2日简单移动平均+收盘价的M3*4日简单移动平均)/3
    输出PBX4:(收盘价的M4日指数移动平均+收盘价的M4*2日简单移动平均+收盘价的M4*4日简单移动平均)/3
    输出PBX5:(收盘价的M5日指数移动平均+收盘价的M5*2日简单移动平均+收盘价的M5*4日简单移动平均)/3
    输出PBX6:(收盘价的M6日指数移动平均+收盘价的M6*2日简单移动平均+收盘价的M6*4日简单移动平均)/3
    '''
    PBX1=(EMA(CLOSE,M1)+MA(CLOSE,M1*2)+MA(CLOSE,M1*4))/3
    PBX2=(EMA(CLOSE,M2)+MA(CLOSE,M2*2)+MA(CLOSE,M2*4))/3
    PBX3=(EMA(CLOSE,M3)+MA(CLOSE,M3*2)+MA(CLOSE,M3*4))/3
    PBX4=(EMA(CLOSE,M4)+MA(CLOSE,M4*2)+MA(CLOSE,M4*4))/3
    PBX5=(EMA(CLOSE,M5)+MA(CLOSE,M5*2)+MA(CLOSE,M5*4))/3
    PBX6=(EMA(CLOSE,M6)+MA(CLOSE,M6*2)+MA(CLOSE,M6*4))/3
    return PBX1,PBX2,PBX3,PBX4,PBX5,PBX6
def ENE(CLOSE,N=25,M1=6,M2=6):
    '''
    轨道线
    输出UPPER:(1+M1/100)*收盘价的N日简单移动平均
    输出LOWER:(1-M2/100)*收盘价的N日简单移动平均
    输出轨道线:(UPPER+LOWER)/2
    '''
    UPPER=(1+M1/100)*MA(CLOSE,N)
    LOWER=(1-M2/100)*MA(CLOSE,N)
    ENE=(UPPER+LOWER)/2
    return UPPER,LOWER,ENE
def MIKE(HIGH,LOW,CLOSE,N=10):
    '''
    麦克支撑压力
    HLC赋值:1日前的(最高价+最低价+收盘价)/3的N日简单移动平均
    HV赋值:N日内最高价的最高值的3日指数移动平均
    LV赋值:N日内最低价的最低值的3日指数移动平均
    输出STOR:2*HV-LV的3日指数移动平均
    输出MIDR:HLC+HV-LV的3日指数移动平均
    输出WEKR:HLC*2-LV的3日指数移动平均
    '''
    HLC=REF(MA((HIGH+LOW+CLOSE)/3,N),1)
    HV=EMA(HHV(HIGH,N),3)
    LV=EMA(LLV(LOW,N),3)
    STOR=EMA(2*HV-LV,3)
    MIDR=EMA(HLC+HV-LV,3)
    WEKR=EMA(HLC*2-LV,3)
    WEKS=EMA(HLC*2-HV,3)
    MIDS=EMA(HLC-HV+LV,3)
    STOS=EMA(2*LV-HV,3)
    return STOR,MIDR,WEKR,WEKS,MIDS,STOS
def XS(CLOSE,VOL,N=13):
    '''
    薛斯通道
    VAR2赋值:收盘价*成交量(手)
    VAR3赋值:(VAR2的3日指数移动平均/成交量(手)的3日指数移动平均+VAR2的6日指数移动平均/成交量(手)的6日指数移动平均+VAR2的12日指数移动平均/成交量(手)的12日指数移动平均+VAR2的24日指数移动平均/成交量(手)的24日指数移动平均)/4的N日指数移动平均
    输出SUP:1.06*VAR3
    输出SDN:VAR3*0.94
    VAR4赋值:收盘价的9日指数移动平均
    输出LUP:VAR4*1.14的5日指数移动平均
    输出LDN:VAR4*0.86的5日指数移动平均
    '''
    VAR2=CLOSE*VOL
    VAR3=EMA((EMA(VAR2,3)/EMA(VOL,3)+EMA(VAR2,6)/EMA(VOL,6)+EMA(VAR2,12)/EMA(VOL,12)+EMA(VAR2,24)/EMA(VOL,24))/4,N)
    SUP=1.06*VAR3
    SDN=VAR3*0.94
    VAR4=EMA(CLOSE,9)
    LUP=EMA(VAR4*1.14,5)
    LDN=EMA(VAR4*0.86,5)
    return SUP,SDN,LUP,LDN
def XS2(CLOSE,HIGH,LOW,N=102,M=7):
    '''
    薛斯通道II
    AA赋值:(2*收盘价+最高价+最低价)/4的5日简单移动平均
    输出 通道1:AA*N/100
    输出 通道2:AA*(200-N)/100
    CC赋值:(2*收盘价+最高价+最低价)/4-收盘价的20日简单移动平均的绝对值/收盘价的20日简单移动平均
    DD赋值:以CC为权重收盘价的动态移动平均
    输出 通道3:(1+M/100)*DD
    '''
    AA=MA((2*CLOSE+HIGH+LOW)/4,5)
    通道1=AA*N/100
    通道2=AA*(200-N)/100
    CC=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,20))/MA(CLOSE,20)
    DD=DMA(CLOSE,0.5)
    通道3=(1+M/100)*DD
    通道4=(1-M/100)*DD
    return 通道1,通道2,通道3,通道4
def TQN(HIGH, LOW, X1=20, X2=20):
    '''
    唐奇安通道
    输出周期高点:1日前的X1日内最高价的最高值
    输出周期低点:1日前的X2日内最低价的最低值
    平空开多赋值:最高价>=周期高点
    平多开空赋值:最低价<=周期低点
    先平空仓再开多仓
    先平多仓再开空仓
    自动过滤交易信号
    '''
    # 计算周期高点：X1日内最高价的最高值，然后取1日前的值
    周期高点 = REF(HHV(HIGH, X1), 1)
    
    # 计算周期低点：X2日内最低价的最低值，然后取1日前的值
    周期低点 = REF(LLV(LOW, X2), 1)
    
    # 平空开多信号：最高价 >= 周期高点
    平空开多 = HIGH >= 周期高点
    
    # 平多开空信号：最低价 <= 周期低点
    平多开空 = LOW <= 周期低点
    
    return 周期高点, 周期低点, 平空开多, 平多开空
#*******************************************
#*******************************************
def SAR(HIGH, LOW, M=10, af=2, amax=20):
    '''
    抛物线指标
    '''
    af = af / 100
    amax = amax / 100
    
    # 转换为numpy数组，处理NaN
    high = np.array(HIGH, dtype=float)
    low = np.array(LOW, dtype=float)
    
    # 检查数据有效性
    if len(high) == 0 or np.isnan(high).all() or np.isnan(low).all():
        return pd.Series([np.nan] * len(HIGH))
    
    # 替换NaN为有效值（用前向填充或均值）
    high_clean = pd.Series(high).fillna(method='ffill').fillna(method='bfill').values
    low_clean = pd.Series(low).fillna(method='ffill').fillna(method='bfill').values
    
    n = len(high_clean)
    
    # 初始化结果数组
    sar = np.full(n, np.nan)
    
    # 需要至少 M+1 个数据点
    if n < M + 1:
        return pd.Series(sar, index=HIGH.index if hasattr(HIGH, 'index') else None)
    
    # 计算标准差，处理0值
    hl_std = np.std(high_clean - low_clean)
    if hl_std == 0 or np.isnan(hl_std):
        hl_std = 0.001  # 设置一个极小值避免除零
    
    # 起始值
    sig0 = True
    xpt0 = high_clean[M - 1] if M > 0 else high_clean[0]
    af0 = af
    
    # 第一个SAR值
    sar[0] = low_clean[0] - hl_std
    
    for i in range(1, n):
        sig1 = sig0
        xpt1 = xpt0
        af1 = af0
        
        if i < M:
            # 前M个数据点使用简单方式
            if i > 0:
                sar[i] = sar[i-1] + (xpt1 - sar[i-1]) * af1
            continue
        
        # 获取当前和前一个的高低点
        lmin = min(low_clean[i-1], low_clean[i])
        lmax = max(high_clean[i-1], high_clean[i])
        
        # 判断趋势方向
        if sig1:
            sig0 = low_clean[i] > sar[i-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high_clean[i] >= sar[i-1]
            xpt0 = min(lmin, xpt1)
        
        # 计算SAR值
        if sig0 == sig1:
            sari = sar[i-1] + (xpt1 - sar[i-1]) * af1
            af0 = min(amax, af1 + af)
            
            if sig0:
                af0 = af0 if xpt0 > xpt1 else af1
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 < xpt1 else af1
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0
        
        sar[i] = sari
    
    # 转换为pandas Series，保持索引一致
    if hasattr(HIGH, 'index'):
        return pd.Series(sar, index=HIGH.index)
    else:
        return pd.Series(sar)
#*******************************
#******************************
#交易类型
def MA_交易(CLOSE,SHORT=5,LONG=20):
    '''
    MA_交易
    MA1赋值:收盘价的SHORT日简单移动平均
    MA2赋值:收盘价的LONG日简单移动平均
    平空开多赋值:MA1上穿MA2
    平多开空赋值:MA2上穿MA1
    先平空仓再开多仓
    先平多仓再开空仓
    '''
    MA1=MA(CLOSE,SHORT)
    MA2=MA(CLOSE,LONG)
    平空开多=CROSS(MA1,MA2)
    平多开空=CROSS(MA2,MA1)
    return MA1,MA2,平空开多,平多开空
def MACD_交易(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    MACD交易
    DIFF赋值:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    DEA赋值:DIFF的MID日指数移动平均
    MACD赋值:2*(DIFF-DEA)
    平空开多赋值:MACD上穿0
    平多开空赋值:0上穿MACD
    先平空仓再开多仓
    '''
    DIFF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIFF,MID)
    MACD=2*(DIFF-DEA)
    平空开多=CROSS(MACD,0)
    平空开多=CROSS(0,MACD)
    return DIFF,DEA,MACD,平空开多,平空开多
def KDJ_交易(CLOSE,HIGH,LOW,N=9,M1=3):
    '''
    KDJ交易
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    K赋值:RSV的M1日[1日权重]移动平均
    D赋值:K的M1日[1日权重]移动平均
    J赋值:3*K-2*D
    平空开多赋值:J上穿0
    平多开空赋值:100上穿J
    先平空仓再开多仓
    先平多仓再开空仓
    自动过滤交易信号
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M1,1)
    J=3*K-2*D
    平空开多=CROSS(J,0)
    平多开空=CROSS(100,J)
    return K,D,J,平空开多,平多开空
#*****************************************
#*****************************************
#神系
def SG_XDT(CLOSE,INDEXC,P1=5,P2=10):
    '''
    心电图(需下载日线)
    输出强弱指标(需下载日线):收盘价/大盘的收盘价*1000
    输出MQR1:QR的5日简单移动平均
    输出MQR2:QR的10日简单移动平均
    ''' 
    QR=CLOSE/INDEXC*1000
    MQR1=MA(QR,5)
    MQR2=MA(QR,10)
    return QR,MQR1,MQR2
def SG_NDB(CLOSE,HIGH,LOW,P1=5,P2=10):
    '''
    脑电波(神系)
    HH赋值:如果收盘价/1日前的收盘价>1.093ANDL>1日前的最高价,返回2*收盘价-1日前的收盘价-最高价,否则返回2*收盘价-最高价-最低价
    V1赋值:收盘价的有效数据周期数
    V2赋值:2*V1日前的收盘价-V1日前的最高价-V1日前的最低价
    输出DK:HH的历史累和+V2
    输出MDK1:DK的P1日简单移动平均
    输出MDK2:DK的P2日简单移动平均
    '''
    C=CLOSE
    H=HIGH
    L=LOW
    HH=IF(np.logical_or(C/REF(C,1)>1.093 ,L>REF(H,1)),2*C-REF(C,1)-H,2*C-H-L)
    V1=1
    V2=2*REF(C,V1)-REF(H,V1)-REF(L,V1)
    DK=SUM(HH,0)+V2
    MDK1=MA(DK,P1)
    MDK2=MA(DK,P2)
    return DK,MDK1,MDK2
def SG_SMX(CLOSE,HIGH,LOW,INDEXH,INDEXL,INDEXC,N=50):
    '''
    生命线(需下载日线)
    INDEXH,INDEXL,INDEXC指数的高，低收盘价,可以通过akshare.stock_zh_a_daily(sybol='sh000001')获取
    H1赋值:N日内最高价的最高值
    L1赋值:N日内最低价的最低值
    H2赋值:N日内大盘的最高价的最高值
    L2赋值:N日内大盘的最低价的最低值
    ZY赋值:收盘价/大盘的收盘价*2000
    输出ZY1:ZY的3日指数移动平均
    输出ZY2:ZY的17日指数移动平均
    输出ZY3:ZY的34日指数移动平均
    '''
    H1=HHV(HIGH,N)
    L1=LLV(LOW,N)
    H2=HHV(INDEXH,N)
    L2=LLV(INDEXL,N)
    ZY=CLOSE/INDEXC*2000
    ZY1=EMA(ZY,3)
    ZY2=EMA(ZY,17)
    ZY3=EMA(ZY,34)
    return ZY1,ZY2,ZY3
def SG_LB(VOL,INDEXV):
    '''
    量比(需下载日线)
    VOl个股成交量，INDXEXV大盘成交量，可以通过ak.stock_zh_a_daily()获取
    ZY2赋值:成交量(手)/大盘的成交量*1000
    输出量比:ZY2
    输出MA5:ZY2的5日简单移动平均
    输出MA10:ZY2的10日简单移动平均
    '''
    ZY2=VOL/INDEXV*1000
    量比=ZY2
    MA5=MA(ZY2,5)
    MA10=MA(ZY2,10)
    return 量比,MA5,MA10
def SG_PF(CLOSE,INDEXC):
    '''
    强势股评分(需下载日线)
    ZY1赋值:收盘价/大盘的收盘价*1000
    A1赋值:如果ZY1>3日内ZY1的最高值,返回10,否则返回0
    A2赋值:如果ZY1>5日内ZY1的最高值,返回15,否则返回0
    A3赋值:如果ZY1>10日内ZY1的最高值,返回20,否则返回0
    A4赋值:如果ZY1>2日内ZY1的最高值,返回10,否则返回0
    A5赋值:统计9日中满足ZY1>1日前的ZY1的天数*5
    输出强势股评分:A1+A2+A3+A4+A5
    '''
    ZY1=CLOSE/INDEXC*1000
    A1=IF(ZY1>HHV(ZY1,3),10,0)
    A2=IF(ZY1>HHV(ZY1,5),15,0)
    A3=IF(ZY1>HHV(ZY1,10),20,0)
    A4=IF(ZY1>HHV(ZY1,2),10,0)
    A5=COUNT(ZY1>REF(ZY1,1) ,9)*5
    强势股评分=A1+A2+A3+A4+A5
    return 强势股评分
#*************************************************
#*************************************************
#龙系
def RAD(OPEN,HIGH,CLOSE,LOW,INDEXO,INDEXH,INDEXL,INDEXC,D=3,S=30,M=30):
    '''
    威力雷达(需下载日线)
    OPEN+HIGH+CLOSE+LOW个股
    INDEXO+INDEXH+INDEXL+INDEXC大盘数据，可以通过akshare获取
    SM赋值:(开盘价+最高价+收盘价+最低价)/4
    SMID赋值:SM的D日简单移动平均
    IM赋值:(大盘的开盘价+大盘的最高价+大盘的最低价+大盘的收盘价)/4
    IMID赋值:IM的D日简单移动平均
    SI1赋值:(SMID-1日前的SMID)/SMID
    II赋值:(IMID-1日前的IMID)/IMID
    输出RADER1:(SI1-II)*2的S日累和*1000
    输出RADERMA:RADER1的M日[1日权重]移动平均
    '''
    SM=(OPEN+HIGH+CLOSE+LOW)/4
    SMID=MA(SM,D)
    IM=(INDEXO+INDEXH+INDEXL+INDEXC)/4
    IMID=MA(IM,D)
    SI1=(SMID-REF(SMID,1))/SMID
    II=(IMID-REF(IMID,1))/IMID
    RADER1=SUM((SI1-II)*2,S)*1000
    RADERMA=SMA(RADER1,M,1)
    return RADER1,RADERMA
    return 
def LON(CLOSE,HIGH,LOW,VOL,N=10):
    '''
    龙系长线
    赋值: 1日前的收盘价
    赋值: 成交量(手)的2日累和/(((2日内最高价的最高值-2日内最低价的最低值))*100)
    赋值: (收盘价-LC)*VID
    赋值: RC的历史累和
    赋值: LONG的10日[1日权重]移动平均
    赋值: LONG的20日[1日权重]移动平均
    输出龙系长线 : DIFF-DEA
    输出LONMA : 龙系长线的N日简单移动平均
    输出LONT : 龙系长线, COLORSTICK
    '''
    LC = REF(CLOSE,1)
    VID = SUM(VOL,2)/(((HHV(HIGH,2)-LLV(LOW,2)))*100)
    RC = (CLOSE-LC)*VID
    LONG = SUM(RC,0)
    DIFF = SMA(LONG,10,1)
    DEA = SMA(LONG,20,1)
    LON = DIFF-DEA
    LONMA = MA(LON,N)
    LONT = LON
    return LON,LONMA,LONT
def SHT(CLOSE,VOL,N=5):
    '''
    龙系短线
    VAR1赋值:(成交量(手)-1日前的成交量(手))/1日前的成交量(手)的5日简单移动平均
    VAR2赋值:(收盘价-收盘价的24日简单移动平均)/收盘价的24日简单移动平均*100
    输出MY: VAR2*(1+VAR1)
    输出龙系短线: MY, COLORSTICK
    输出SHTMA: SHT的N日简单移动平均
    '''
    VAR1=MA((VOL-REF(VOL,1))/REF(VOL,1),5)
    VAR2=(CLOSE-MA(CLOSE,24))/MA(CLOSE,24)*100
    MY= VAR2*(1+VAR1)
    SHT= MY#COLORSTICK
    SHTMA= MA(SHT,N)
    return SHT,SHTMA
def ZLJC(CLOSE,LOW,HIGH,VOL):
    '''
    主力进出
    VAR1赋值:(收盘价+最低价+最高价)/3
    VAR2赋值:((VAR1-1日前的最低价)-(最高价-VAR1))*成交量(手)/100000/(最高价-最低价)的历史累和
    VAR3赋值:VAR2的1日指数移动平均
    输出 JCS:VAR3
    输出 JCM:VAR3的12日简单移动平均
    输出 JCL:VAR3的26日简单移动平均
    '''
    VAR1=(CLOSE+LOW+HIGH)/3
    VAR2=SUM(((VAR1-REF(LOW,1))-(HIGH-VAR1))*VOL/100000/(HIGH-LOW),0)
    VAR3=EMA(VAR2,1)
    JCS=VAR3
    JCM=MA(VAR3,12)
    JCL=MA(VAR3,26)
    return JCS,JCM,JCL
def ZLMM(CLOSE):
    '''
    赋值:1日前的收盘价
    RSI2赋值:收盘价-LC和0的较大值的12日[1日权重]移动平均/收盘价-LC的绝对值的12日[1日权重]移动平均*100
    RSI3赋值:收盘价-LC和0的较大值的18日[1日权重]移动平均/收盘价-LC的绝对值的18日[1日权重]移动平均*100
    输出MMS:3*RSI2-2*收盘价-LC和0的较大值的16日[1日权重]移动平均/收盘价-LC的绝对值的16日[1日权重]移动平均*100的3日简单移动平均
    输出MMM:MMS的8日指数移动平均
    输出MML:3*RSI3-2*收盘价-LC和0的较大值的12日[1日权重]移动平均/收盘价-LC的绝对值的12日[1日权重]移动平均*100的5日简单移动平均
    '''
    LC =REF(CLOSE,1)
    RSI2=SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100
    RSI3=SMA(MAX(CLOSE-LC,0),18,1)/SMA(ABS(CLOSE-LC),18,1)*100
    MMS=MA(3*RSI2-2*SMA(MAX(CLOSE-LC,0),16,1)/SMA(ABS(CLOSE-LC),16,1)*100,3)
    MMM=EMA(MMS,8)
    MML=MA(3*RSI3-2*SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100,5)
    return MMS,MMM,MML
def SLZT(CLOSE,LOW,HIGH):
    '''
    神龙在天
    输出白龙: 收盘价的125日简单移动平均
    输出黄龙: 白龙+2*收盘价的170日估算标准差
    输出紫龙: 白龙-2*收盘价的145日估算标准差
    输出青龙: 步长为1极限值为7的125日抛物转向, LINESTICK
    VAR2赋值:70日内最高价的最高值
    VAR3赋值:20日内最高价的最高值
    输出红龙: VAR2*0.83
    输出蓝龙: VAR3*0.91
    '''
    白龙=MA(CLOSE,125)
    黄龙=白龙+2*STD(CLOSE,170)
    紫龙=白龙-2*STD(CLOSE,145)
    青龙=SAR(HIGH,LOW,125,1,7)# LINESTICK;
    VAR2=HHV(HIGH,70)
    VAR3=HHV(HIGH,20)
    红龙= VAR2*0.83
    蓝龙=VAR3*0.91
    return 白龙,黄龙,紫龙,青龙,红龙,蓝龙
def ADVOL(CLOSE,HIGH,LOW,VOL):
    '''
    龙系离散量
    A赋值:((收盘价-最低价)-(最高价-收盘价))*成交量(手)/10000/(最高价-最低价)的历史累和
    输出龙系离散量:A
    输出MA1:A的30日简单移动平均
    输出均线:MA1的100日简单移动平均
    '''
    A=SUM(((CLOSE-LOW)-(HIGH-CLOSE))*VOL/10000/(HIGH-LOW),0)
    ADVOL=A
    MA1=MA(A,30)
    MA2=MA(MA1,100)
    return ADVOL,MA1,MA2
#*********************************************
#*********************************************
#鬼系
def CYC(code='sh600031',start_date='20210101',end_date='20221022',P1=5,P2=13,P3=34):
    '''
    成本均线
    JJJ赋值:如果总量>0.01,简单理解流通股,返回0.01*总金额/总量,否则返回昨收盘价
    DDD赋值:(最高价<0.01 或者 最低价<0.01)
    JJJT赋值:如果DDD,返回1,否则返回(JJJ<(最高价+0.01)并且JJJ>(最低价-0.01))
    输出CYC1:如果JJJT,返回0.01*成交额(元)的P1日指数移动平均/成交量(手)的P1日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P1日指数移动平均
    输出CYC2:如果JJJT,返回0.01*成交额(元)的P2日指数移动平均/成交量(手)的P2日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P2日指数移动平均
    输出CYC3:如果JJJT,返回0.01*成交额(元)的P3日指数移动平均/成交量(手)的P3日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P3日指数移动平均
    输出CYC∞:如果JJJT,返回以100*成交量(手)/流通股本(股)为权重成交额(元)/(100*成交量(手))的动态移动平均,否则返回(最高价+最低价+收盘价)/3的120日指数移动平均
    '''
    pass
    def DYNAINFO_10(M=10):
        '''
        总金额=price*volume
        '''
        result=df['close']*df['volume']
        return result
    def DYNAINFO_3(M=3):
        '''
        昨日收盘价
        '''
        return df['close'].shift(1)
    def DYNAINFO_5(M=5):
        '''
        最高价
        '''
        return df['high']
    def DYNAINFO_6(M=6):
        '''
        最低价
        '''
        return df['low']
    AMOUNT=AMOUNT=df['close']*df['volume']
    VOL=df['volume']
    HIGH=df['high']
    LOW=df['low']
    CLOSE=df['close']
    def FINANCE_7(M=7):
        '''
        100*成交量
        '''
        return 100*df['volume']
    JJJ=IF(DYNAINFO_8(8)>0.01,0.01*DYNAINFO_10(10)/DYNAINFO_8(8),DYNAINFO_3(3))
    DDD=np.logical_or(DYNAINFO_5(5)<0.01,DYNAINFO_6(6)<0.01)
    JJJT=IF(DDD,False,np.logical_and(JJJ<(DYNAINFO_5(5)+0.01),JJJ>(DYNAINFO_6(6)-0.01)))
    CYC1=IF(JJJT,0.01*EMA(AMOUNT,P1)/EMA(VOL,P1),EMA((HIGH+LOW+CLOSE)/3,P1))
    CYC2=IF(JJJT,0.01*EMA(AMOUNT,P2)/EMA(VOL,P2),EMA((HIGH+LOW+CLOSE)/3,P2))
    CYC3=IF(JJJT,0.01*EMA(AMOUNT,P3)/EMA(VOL,P3),EMA((HIGH+LOW+CLOSE)/3,P3))
    #CYC_a=IF(JJJT,DMA(AMOUNT/(100*VOL),100*VOL/FINANCE_7(7)),EMA((HIGH+LOW+CLOSE)/3,120))
    return CYC1,CYC2,CYC3
def CYS(CLOSE,AMOUNT,VOL):
    '''
    市场盈亏
    AMOUNT成交额，VOL成交量
    CYC13赋值:0.01*成交额(元)的13日指数移动平均/成交量(手)的13日指数移动平均
    输出市场盈亏:(收盘价-CYC13)/CYC13*100
    '''
    CYC13=0.01*EMA(AMOUNT,13)/EMA(VOL,13)
    CYS=(CLOSE-CYC13)/CYC13*100
    return CYS
def CYQKL(CLOSE,OPEN):
    '''
    博弈K线长度
    输出KL:100*(以收盘价计算的获利盘比例-以开盘价计算的获利盘比例)
    '''
    KL=100*(WINNER(CLOSE)-WINNER(OPEN))
    return KL
def CYW(CLOSE,HIGH,LOW,VOL):
    '''
    主力控盘
    VAR1赋值:收盘价-最低价
    VAR2赋值:最高价-最低价
    VAR3赋值:收盘价-最高价
    VAR4赋值:如果最高价>最低价,返回(VAR1/VAR2+VAR3/VAR2)*成交量(手),否则返回0
    输出主力控盘: VAR4的10日累和/10000, COLORSTICK
    '''
    VAR1=CLOSE-LOW
    VAR2=HIGH-LOW
    VAR3=CLOSE-HIGH
    VAR4=IF(HIGH>LOW,(VAR1/VAR2+VAR3/VAR2)*VOL,0)
    CYW=SUM(VAR4,10)/10000 #COLORSTICK
    return CYW
#***************************************************
#***************************************************
#其他系
def PEAK(CLOSE,N,n=1):
    '''
    计算倾效
    np.polyfit(range(N),x,deg=1)
    '''
    pass
def TROUGH(CLOSE,N,n=1):
    '''
    箱底
    '''
    pass
def XT(CLOSE):
    '''
    箱体
    '''
    箱顶=PEAK(CLOSE,N,1)*0.98
    箱底=TROUGH(CLOSE,N,1)*1.02
    箱高=100*(箱顶-箱底)/箱底,#NODRAW
def  MOD(M,N):
    '''
    计算模
    M/N的余数
    '''
    return M//N
def SQJZ(CLSOE):
    '''
    N赋值:到最后交易的周期
    B赋值:收盘价<4日前的收盘价
    T1赋值: 条件连续成立次数
    A_B1赋值:(T1>9) AND T1关于9的模=1
    A_B2赋值:(T1>9) AND T1关于9的模=2
    A_B8赋值:(T1>9) AND T1关于9的模=8
    A_B9赋值:(T1>9) AND T1关于9的模=0
    B1赋值:(N=6 AND 5日后的(平滑处理)统计6日中满足B的天数=6) OR (N=7 AND 6日后的(平滑处理)统计7日中满足B的天数=7) OR (N=8 AND 7日后的(平滑处理)统计8日中满足B的天数=8) OR (N>=9 AND 8日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B1AND(1日前的B=0ORA_B1)时,在最低价位置书写数字,画洋红色
    B2赋值:(N=5 AND 4日后的(平滑处理)统计6日中满足B的天数=6) OR (N=6 AND 5日后的(平滑处理)统计7日中满足B的天数=7) OR (N=7 AND 6日后的(平滑处理)统计8日中满足B的天数=8) OR (N>=8 AND 7日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B2AND(2日前的B=0ORA_B2)时,在最低价位置书写数字,画洋红色
    B8赋值:(N=1 AND 统计8日中满足B的天数=8) OR (N>=2 AND 1日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B8AND(8日前的B=0ORA_B8)时,在最低价位置书写数字,画洋红色
    B9赋值:(N>=1 AND 统计9日中满足B的天数=9)
    当满足条件B9AND(9日前的B=0ORA_B9)时,在最低价位置书写数字,画红色
    S赋值:收盘价>4日前的收盘价
    T2赋值: 条件连续成立次数
    A_S1赋值:(T2>9) AND T2关于9的模=1
    A_S2赋值:(T2>9) AND T2关于9的模=2
    A_S8赋值:(T2>9) AND T2关于9的模=8
    A_S9赋值:(T2>9) AND T2关于9的模=0
    S1赋值:(N=6 AND 5日后的(平滑处理)统计6日中满足S的天数=6) OR (N=7 AND 6日后的(平滑处理)统计7日中满足S的天数=7) OR (N=8 AND 7日后的(平滑处理)统计8日中满足S的天数=8) OR (N>=9 AND 8日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S1AND(1日前的S=0ORA_S1)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S2赋值:(N=5 AND 4日后的(平滑处理)统计6日中满足S的天数=6) OR (N=6 AND 5日后的(平滑处理)统计7日中满足S的天数=7) OR (N=7 AND 6日后的(平滑处理)统计8日中满足S的天数=8) OR (N>=8 AND 7日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S2AND(2日前的S=0ORA_S2)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S8赋值:(N=1 AND 统计8日中满足S的天数=8) OR (N>=2 AND 1日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S8AND(8日前的S=0ORA_S8)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S9赋值:(N>=1 AND 统计9日中满足S的天数=9)
    当满足条件S9AND(9日前的S=0ORA_S9)时,在最高价位置书写数字,画绿色,显示在位置之上
    C=CLOSE
    N=CURRBARSCOUNT()
    B=C<REF(C,4)
    T1= BARSLASTCOUNT(B)
    A_B1=IF(T1>=9,1,None)
    A_B2=IF(T1>9,2,None)
    A_B8=IF(T1>9,8,None)
    A_B9=IF(T1>9,0,None)
    B1:=(N=6 AND REFXV(COUNT(B,6),5)=6) OR (N=7 AND REFXV(COUNT(B,7),6)=7) OR (N=8 AND REFXV(COUNT(B,8),7)=8) OR (N>=9 AND REFXV(COUNT(B,9),8)=9);
    DRAWNUMBER(B1 AND (REF(B,1)=0 OR A_B1),L,1),COLORMAGENTA;
    B2:=(N=5 AND REFXV(COUNT(B,6),4)=6) OR (N=6 AND REFXV(COUNT(B,7),5)=7) OR (N=7 AND REFXV(COUNT(B,8),6)=8) OR (N>=8 AND REFXV(COUNT(B,9),7)=9);
    DRAWNUMBER(B2 AND(REF(B,2)=0 OR A_B2),L,2),COLORMAGENTA;
    B8:=(N=1 AND COUNT(B,8)=8) OR (N>=2 AND REFXV(COUNT(B,9),1)=9);
    DRAWNUMBER(B8 AND (REF(B,8)=0 OR A_B8),L,8),COLORMAGENTA;
    B9:=(N>=1 AND COUNT(B,9)=9);
    DRAWNUMBER(B9 AND (REF(B,9)=0 OR A_B9),L,9),COLORRED;
    S:=C>REF(C,4);
    T2:= BARSLASTCOUNT(S);
    A_S1:=(T2>9) AND MOD(T2,9)=1;
    A_S2:=(T2>9) AND MOD(T2,9)=2;
    A_S8:=(T2>9) AND MOD(T2,9)=8;
    A_S9:=(T2>9) AND MOD(T2,9)=0;
    S1:=(N=6 AND REFXV(COUNT(S,6),5)=6) OR (N=7 AND REFXV(COUNT(S,7),6)=7) OR (N=8 AND REFXV(COUNT(S,8),7)=8) OR (N>=9 AND REFXV(COUNT(S,9),8)=9);
    DRAWNUMBER(S1 AND (REF(S,1)=0 OR A_S1),H,1),COLORMAGENTA,DRAWABOVE;
    S2:=(N=5 AND REFXV(COUNT(S,6),4)=6) OR (N=6 AND REFXV(COUNT(S,7),5)=7) OR (N=7 AND REFXV(COUNT(S,8),6)=8) OR (N>=8 AND REFXV(COUNT(S,9),7)=9);
    DRAWNUMBER(S2 AND (REF(S,2)=0 OR A_S2),H,2),COLORMAGENTA,DRAWABOVE;
    S8:=(N=1 AND COUNT(S,8)=8) OR (N>=2 AND REFXV(COUNT(S,9),1)=9);
    DRAWNUMBER(S8 AND (REF(S,8)=0 OR A_S8),H,8),COLORMAGENTA,DRAWABOVE;
    S9:=(N>=1 AND COUNT(S,9)=9);
    DRAWNUMBER(S9 AND (REF(S,9)=0 OR A_S9),H,9),COLORGREEN,DRAWABOVE;
    '''
    pass
def JAX(CLOSE,HIGH,LOW,N=30):
    '''
    济安线
    AA赋值:(2*收盘价+最高价+最低价)/4-收盘价的N日简单移动平均的绝对值/收盘价的N日简单移动平均
    输出济安线:以AA为权重(2*收盘价+最低价+最高价)/4的动态移动平均,线宽为3,画洋红色
    CC赋值:(收盘价/济安线)
    MA1赋值:CC*(2*收盘价+最高价+最低价)/4的3日简单移动平均
    MAAA赋值:((MA1-济安线)/济安线)/3
    TMP赋值:MA1-MAAA*MA1
    输出J:如果TMP<=济安线,返回济安线,否则返回无效数,线宽为3,画青色
    输出A:TMP,线宽为2,画棕色
    输出X:如果TMP<=济安线,返回TMP,否则返回无效数,线宽为2,画绿色
    '''
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N)
    data=pd.DataFrame()
    data['数据']=(2*CLOSE+LOW+HIGH)/4
    #alpha中值0.5
    济安线=data['数据'].ewm(alpha=0.5, adjust=True).mean()#LINETHICK3,COLORMAGENTA
    CC=(CLOSE/济安线)
    MA1=MA(CC*(2*CLOSE+HIGH+LOW)/4,3)
    MAAA=((MA1-济安线)/济安线)/3
    TMP=MA1-MAAA*MA1
    J=IF(TMP<=济安线,济安线,None)#LINETHICK3,COLORCYAN
    A=TMP#LINETHICK2,COLORBROWN
    X=IF(TMP<=济安线,TMP,None)#LINETHICK2,COLORGREEN
    return J,A,X
def XJDX(CLOSE,HIGH,LOW):
    '''
    超级短线
    VAR1赋值:(2*收盘价+最高价+最低价)/4
    VAR2赋值:VAR1的4日指数移动平均的4日指数移动平均的4日指数移动平均
    输出J: (VAR2-1日前的VAR2)/1日前的VAR2*100, COLORSTICK
    输出D: J的3日简单移动平均
    输出K: J的1日简单移动平均
    '''
    VAR1=(2*CLOSE+HIGH+LOW)/4
    VAR2=EMA(EMA(EMA(VAR1,4),4),4)
    J=(VAR2-REF(VAR2,1))/REF(VAR2,1)*100# COLORSTICK
    D=MA(J,3)
    K= MA(J,1)
    return J,D,K
def ZJTJ(CLOSE):
    '''
    庄家抬轿
    获利盘，和成本函数需要写
    VAR1赋值:收盘价的9日指数移动平均的9日指数移动平均
    控盘赋值:(VAR1-1日前的VAR1)/1日前的VAR1*1000
    当满足条件控盘<0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,画白色
    A10赋值:控盘上穿0
    输出无庄控盘:如果控盘<0,返回控盘,否则返回0,画白色,NODRAW
    输出开始控盘:如果A10,返回5,否则返回0,线宽为1,画棕色
    当满足条件控盘>1日前的控盘AND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,画红色
    输出有庄控盘:如果控盘>1日前的控盘AND控盘>0,返回控盘,否则返回0,画红色,NODRAW
    VAR2赋值:100*以收盘价*0.95计算的获利盘比例
    当满足条件VAR2>50ANDCOST(85)<CLOSEAND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,COLORFF00FF
    输出高度控盘:如果VAR2>50ANDCOST(85)<CLOSEAND控盘>0,返回控盘,否则返回0,COLORFF00FF,NODRAW
    当满足条件控盘<1日前的控盘AND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,COLOR00FF00
    输出主力出货:如果控盘<1日前的控盘AND控盘>0,返回控盘,否则返回0,COLOR00FF00,NODRAW
    '''
    VAR1=EMA(EMA(CLOSE,9),9)
    控盘=(VAR1-REF(VAR1,1))/REF(VAR1,1)*1000
    #STICKLINE(控盘<0,控盘,0,1,0),COLORWHITE;
    A10=CROSS(控盘,0)
    无庄控盘=IF(控盘<0,控盘,0)#COLORWHITE,NODRAW;
    开始控盘=IF(A10,1,0)#LINETHICK1,COLORBROWN;
    #STICKLINE(控盘>REF(控盘,1) AND 控盘>0,控盘,0,1,0),COLORRED;
    有庄控盘=IF(np.logical_and(控盘>REF(控盘,1),控盘>0),控盘,0)#COLORRED,NODRAW;
    #VAR2=100*WINNER(CLOSE*0.95)
    #STICKLINE(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0,1,0),COLORFF00FF;
    #高度控盘:IF(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0),COLORFF00FF,NODRAW;
    #STICKLINE(控盘<REF(控盘,1) AND 控盘>0,控盘,0,1,0),COLOR00FF00;
    主力出货=IF(np.logical_and(控盘<REF(控盘,1),控盘>0),控盘,0)#COLOR00FF00,NODRAW;
    return 无庄控盘,开始控盘,有庄控盘,主力出货
def ZBCD(HIGH,LOW,OPEN,AMOUNT,VOL,CLOSE,N=10):
    '''
    准备抄底
    VAR1赋值:成交额(元)/成交量(手)/7
    VAR2赋值:(3*最高价+最低价+开盘价+2*收盘价)/7
    VAR3赋值:成交额(元)的N日累和/VAR1/7
    VAR4赋值:以成交量(手)/VAR3为权重VAR2的动态移动平均
    输出抄底:(收盘价-VAR4)/VAR4*100,画淡洋红色
    当满足条件-7.0上穿抄底时,在抄底位置画1号图标
    '''
    VAR1=AMOUNT/VOL/7
    VAR2=(3*HIGH+LOW+OPEN+2*CLOSE)/7
    VAR3=SUM(AMOUNT,N)/VAR1/7
    VAR4=DMA(VAR2,VOL/VAR3)
    抄底=(CLOSE-VAR4)/VAR4*100#COLORLIMAGENTA
    #DRAWICON(CROSS(-7.0,抄底),抄底,1)
    return 抄底
def BDZX(HIGH,LOW,CLOSE):
    '''
    波段之星
    VAR2赋值:(最高价+最低价+收盘价*2)/4
    VAR3赋值:VAR2的21日指数移动平均
    VAR4赋值:VAR2的21日估算标准差
    VAR5赋值:((VAR2-VAR3)/VAR4*100+200)/4
    VAR6赋值:(VAR5的5日指数移动平均-25)*1.56
    输出AK: VAR6的2日指数移动平均*1.22
    输出AD1: AK的2日指数移动平均
    输出AJ: 3*AK-2*AD1
    输出AA:100
    输出布林极限:0
    输出CC:80
    输出买进: 如果AK上穿AD1,返回58,否则返回20
    输出卖出: 如果AD1上穿AK,返回58,否则返回20
    '''
    VAR2=(HIGH+LOW+CLOSE*2)/4
    VAR3=EMA(VAR2,21)
    VAR4=STD(VAR2,21)
    VAR5=((VAR2-VAR3)/VAR4*100+200)/4
    VAR6=(EMA(VAR5,5)-25)*1.56
    AK= EMA(VAR6,2)*1.22
    AD1= EMA(AK,2)
    AJ= 3*AK-2*AD1
    AA=100
    BB=0
    CC=80
    买进= IF(CROSS(AK,AD1),58,20)
    卖出= IF(CROSS(AD1,AK),58,20)
    return AK,AD1,AJ,AA,BB,CC,买进,卖出
def LHXJ(HIGH,LOW,CLOSE):
    '''
    猎狐先觉
    VAR1赋值:(收盘价*2+最高价+最低价)/4
    VAR2赋值:VAR1的13日指数移动平均-VAR1的34日指数移动平均
    VAR3赋值:VAR2的5日指数移动平均
    输出主力弃盘: (-2)*(VAR2-VAR3)*3.8
    输出主力控盘: 2*(VAR2-VAR3)*3.8
    '''
    VAR1=(CLOSE*2+HIGH+LOW)/4
    VAR2=EMA(VAR1,13)-EMA(VAR1,34)
    VAR3=EMA(VAR2,5)
    主力弃盘=(-2)*(VAR2-VAR3)*3.8
    主力控盘=2*(VAR2-VAR3)*3.8
    return 主力弃盘,主力控盘
def LYJH(CLOSE,HIGH,LOW,M=80,M1=50):
    '''
    猎鹰歼狐
    VAR1赋值:(36日内最高价的最高值-收盘价)/(36日内最高价的最高值-36日内最低价的最低值)*100
    输出机构做空能量线: VAR1的2日[1日权重]移动平均
    VAR2赋值:(收盘价-9日内最低价的最低值)/(9日内最高价的最高值-9日内最低价的最低值)*100
    输出机构做多能量线: VAR2的5日[1日权重]移动平均-8
    输出LH: M
    输出LH1: M1
    '''
    VAR1=(HHV(HIGH,36)-CLOSE)/(HHV(HIGH,36)-LLV(LOW,36))*100
    机构做空能量线=SMA(VAR1,2,1)
    VAR2=(CLOSE-LLV(LOW,9))/(HHV(HIGH,9)-LLV(LOW,9))*100
    机构做多能量线=SMA(VAR2,5,1)-8
    LH=M
    LH1=M1
    return 机构做空能量线,机构做多能量线,LH,LH1
def JFZX(OPEN,CLOSE,VOL,N=30):
    '''
    飓风智能中线
    VAR2赋值:如果收阳线,返回成交量(手),否则返回0的N日累和/成交量(手)的N日累和*100
    VAR3赋值:100-如果收阳线,返回成交量(手),否则返回0的N日累和/成交量(手)的N日累和*100
    输出多头力量: VAR2
    输出空头力量: VAR3
    输出多空平衡: 50
    '''
    VAR2=SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100
    VAR3=100-SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100
    多头力量= VAR2
    空头力量= VAR3
    多空平衡= 50
    return 多头力量,空头力量,多空平衡
def CYHT(CLOSE,HIGH,LOW,OPEN):
    '''
    财运亨通
    VAR1赋值:(2*收盘价+最高价+最低价+开盘价)/5
    输出高抛: 80
    VAR2赋值:34日内最低价的最低值
    VAR3赋值:34日内最高价的最高值
    输出SK: (VAR1-VAR2)/(VAR3-VAR2)*100的13日指数移动平均
    输出SD: SK的3日指数移动平均
    输出低吸: 20
    输出强弱分界: 50
    VAR4赋值:如果SK上穿SD,返回40,否则返回22
    VAR5赋值:如果SD上穿SK,返回60,否则返回78
    输出卖出: VAR5
    输出买进: VAR4
    '''
    VAR1=(2*CLOSE+HIGH+LOW+OPEN)/5
    高抛= 80
    VAR2=LLV(LOW,34)
    VAR3=HHV(HIGH,34)
    SK= EMA((VAR1-VAR2)/(VAR3-VAR2)*100,13)
    SD= EMA(SK,3)
    低吸= 20
    强弱分界= 50
    VAR4=IF(CROSS(SK,SD),40,22)
    VAR5=IF(CROSS(SD,SK),60,78)
    卖出= VAR5
    买进= VAR4
    return 高抛,SK,SD,低吸,强弱分界,卖出,买进
def BSQJ(CLOSE):
    '''
    买卖区间
    买线赋值:收盘价的2日指数移动平均
    卖线赋值:收盘价的21日线性回归斜率*20+收盘价的42日指数移动平均
    当满足条件买线>=卖线时,在日期日0日内最高价的最高值和日期日0日内最低价的最低值位置之间画柱状线,宽度为6,0不为0则画空心柱.,COLOR001050
    当满足条件买线<卖线时,在日期日0日内最高价的最高值和日期日0日内最低价的最低值位置之间画柱状线,宽度为6,0不为0则画空心柱.,COLOR404050
    K线
    指导赋值:(收盘价的4日指数移动平均+收盘价的6日指数移动平均+收盘价的12日指数移动平均+收盘价的24日指数移动平均)/4的2日指数移动平均
    界赋值:收盘价的27日简单移动平均
    输出B买:如果指导上穿界ORCROSS(买线,卖线),返回收盘价,否则返回无效数,画洋红色,NODRAW
    输出持仓:如果买线>=卖线,返回收盘价,否则返回无效数,画红色,NODRAW
    输出S卖:如果界上穿指导ORCROSS(卖线,买线),返回收盘价,否则返回无效数,画淡灰色,NODRAW
    输出空仓:如果买线<卖线,返回收盘价,否则返回无效数,画绿色,NODRAW
    当满足条件买线上穿卖线时,在最低价位置画1号图标
    当满足条件卖线上穿买线时,在最高价位置画2号图标
    '''
    C=CLOSE
    买线=EMA(C,2)
    卖线=EMA(SLOPE(C,21)*20+C,42)
    #STICKLINE(买线>=卖线,REFDATE(HHV(H,0),DATE),REFDATE(LLV(L,0),DATE),6,0),COLOR001050
    #STICKLINE(买线<卖线,REFDATE(HHV(H,0),DATE),REFDATE(LLV(L,0),DATE),6,0),COLOR404050;
    #DRAWKLINE(H,O,L,C);
    指导=EMA((EMA(CLOSE,4)+EMA(CLOSE,6)+EMA(CLOSE,12)+EMA(CLOSE,24))/4,2)
    界=MA(CLOSE,27)
    B买=IF(np.logical_or(CROSS(指导,界),CROSS(买线,卖线)),C,None)#COLORMAGENTA,NODRAW;
    持仓=IF(买线>=卖线,C,None)#COLORRED,NODRAW
    S卖=IF(np.logical_or(CROSS(界,指导),CROSS(卖线,买线)),C,None)#COLORLIGRAY,NODRAW
    空仓=IF(买线<卖线,C,None)#COLORGREEN,NODRAW
    #DRAWICON(CROSS(买线,卖线),L,1);
    #DRAWICON(CROSS(卖线,买线),H,2);
    return B买,持仓,S卖,空仓
def CDP_STD(CLOSE, HIGH, LOW):
    '''
    逆势操作
    CH赋值:1日前的最高价
    CL赋值:1日前的最低价
    CC赋值:1日前的收盘价
    输出CDP:(CH+CL+CC)/3
    输出AH:2*CDP+CH-2*CL
    输出NH:CDP+CDP-CL
    输出NL:CDP+CDP-CH
    输出AL:2*CDP-2*CH+CL
    '''
    CH = REF(HIGH, 1)
    CL = REF(LOW, 1)
    CC = REF(CLOSE, 1)
    CDP = (CH + CL + CC) / 3
    AH = 2 * CDP + CH - 2 * CL
    NH = CDP + CDP - CL
    NL = CDP + CDP - CH
    AL = 2 * CDP - 2 * CH + CL
    return CDP, AH, NH, NL, AL
def TBP_STD(HIGH,LOW,CLOSE):
    '''
    趋势平衡点
    APX赋值:(最高价+最低价+收盘价)/3
    TR0赋值:最高价-最低价和最高价-1日前的收盘价的绝对值和最低价-1日前的收盘价的绝对值的较大值的较大值
    MF0赋值:收盘价-2日前的收盘价
    MF1赋值:1日前的MF0
    MF2赋值:2日前的MF0
    DIRECT1赋值:上次MF0>MF1ANDMF0>MF2距今天数
    DIRECT2赋值:上次MF0<MF1ANDMF0<MF2距今天数
    DIRECT0赋值:如果DIRECT1<DIRECT2,返回100,否则返回-100
    输出TBP:1日前的1日前的收盘价+如果DIRECT0>50,返回MF0和MF1的较小值,否则返回MF0和MF1的较大值
    输出多头获利:1日前的如果DIRECT0>50,返回APX*2-最低价,否则返回无效数,NODRAW
    输出多头停损:1日前的如果DIRECT0>50,返回APX-TR0,否则返回无效数,NODRAW
    输出空头回补:1日前的如果DIRECT0<-50,返回APX*2-最高价,否则返回无效数,NODRAW
    输出空头停损:1日前的如果DIRECT0<-50,返回APX+TR0,否则返回无效数,NODRAW
    '''
    H=HIGH
    L=LOW
    C=CLOSE
    APX=(H+L+C)/3
    TR0=MAX(H-L,MAX(ABS(H-REF(C,1)),ABS(L-REF(C,1))))
    MF0=C-REF(C,2)
    MF1=REF(MF0,1)
    MF2=REF(MF0,2)
    DIRECT1=BARSLAST(np.logical_and(MF0>MF1,MF0>MF2))
    DIRECT2=BARSLAST(np.logical_and(MF0<MF1,MF0<MF2))
    DIRECT0=IF(DIRECT1<DIRECT2,100,-100)
    TBP=REF(REF(C,1)+IF(DIRECT0>50,MIN(MF0,MF1),MAX(MF0,MF1)),1)
    多头获利=REF(IF(DIRECT0>50,APX*2-L,None),1)
    多头停损=REF(IF(DIRECT0>50,APX-TR0,None),1)
    空头回补=REF(IF(DIRECT0<-50,APX*2-H,None),1)
    空头停损=REF(IF(DIRECT0<-50,APX+TR0,None),1)
    return TBP,多头获利,多头停损,空头回补,空头停损
#***********************************************
#***********************************************
#****************有空写****************************

