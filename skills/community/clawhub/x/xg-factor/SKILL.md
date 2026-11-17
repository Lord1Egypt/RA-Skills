---
name: 小果量化因子库
description: |
   小果量化因子库是一个集成了数百个技术指标、Alpha因子和交易信号的Python量化因子计算系统。
   支持股票、ETF、可转债等多品种的历史因子批量计算，提供单只股票因子分析和全市场因子数据生成。
   触发关键词：小果因子、量化因子、因子计算、xg_factor、技术指标、Alpha因子、因子选股、因子库。
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
---

# 小果量化因子库 Skill

## 1. 概述

小果量化因子库是一套完整的 Python 量化因子计算系统，基于 `xg_factor` 核心类实现，提供了从传统技术指标到高级 Alpha 因子的全面覆盖。该系统支持单只股票的因子分析和全市场股票的批量因子计算，是量化投研和策略开发的得力工具。

**作者**：小果（微信：xg_quant）

## 2. 主要作用

1. **因子计算引擎**：提供 300+ 个量化因子计算函数，涵盖技术指标、交易信号、风险收益指标、WorldQuant Alpha 因子等。
2. **批量数据处理**：支持多进程/多线程并行计算全市场股票的因子数据，大幅提升计算效率。
3. **策略信号生成**：内置多种交易信号函数（如金叉死叉、波段买卖点），可直接用于构建量化策略。
4. **数据标准化输出**：统一的因子计算结果以 Pandas DataFrame 或 Parquet 格式输出，便于后续分析和回测。

## 3. 核心功能模块

### 3.1 基础技术指标（超卖超买类）
| 函数名 | 说明 |
|--------|------|
| `CCI()` | 商品路径指标 |
| `RSI1()` / `RSI2()` / `RSI3()` | 相对强弱指标（6/12/24日） |
| `KDJ_K()` / `KDJ_D()` / `KDJ_J()` | KDJ随机指标 |
| `WR1()` / `WR2()` | 威廉指标 |
| `MFI()` | 资金流量指标 |
| `BIAS1()` / `BIAS2()` / `BIAS3()` | 乖离率（6/12/24日） |
| `PSY()` / `PSYMA()` | 心理线指标 |
| `SKDJ_K()` / `SKDJ_D()` | 慢速随机指标 |
| `LWR1()` / `LWR2()` | LWR指标 |
| `MARSI1()` / `MARSI2()` | 相对强弱平均线 |
| `BIAS_QL_BIAS()` / `BIAS_QL_BIASMA()` | 传统版乖离率 |
| `BIAS36_BIAS36()` / `BIAS36_BIAS612()` / `BIAS36_MABIAS()` | 三六乖离 |
| `ACCER()` | 幅度涨速 |
| `MTM_MTM()` / `MTM_MTMMA()` | 动量线指标 |
| `UDL_UDL()` / `UDL_MAUDL()` | 引力线 |

### 3.2 趋势类指标
| 函数名 | 说明 |
|--------|------|
| `MACD_DIF()` / `MACD_DEA()` / `MACD_MACD()` | 平滑异同平均线 |
| `MACD_金叉()` / `MACD_死叉()` | MACD金叉/死叉信号 |
| `DMI_PDI()` / `DMI_MDI()` / `DMI_ADX()` / `DMI_ADXR()` | 趋向指标 |
| `BOLL_BOLL()` / `BOLL_UB()` / `BOLL_LB()` | 布林线（中/上/下轨） |
| `SAR()` | 抛物线转向指标 |
| `TRIX_TRIX()` / `TRIX_MATRIX()` | 三重指数平均线 |
| `UOS_UOS()` / `UOS_MAUOS()` | 终极指标 |
| `ASI_ASI()` / `ASI_ASIT()` | 振动升降指标 |
| `CHO_CHO()` / `CHO_MACHO()` | 佳庆指标 |
| `DMA_XT_DIF()` / `DMA_XT_DIFMA()` | 平均差 |
| `DPO_DPO()` / `DPO_MADPO()` | 区间震荡线 |
| `EMV_EMV()` / `EMV_MAEMV()` | 简易波动指标 |
| `VMACD_DIF()` / `VMACD_DEA()` / `VMACD_MACD()` | 量平滑异同平均线 |
| `SMACD_DEA()` / `SMACD_MACD()` | 单线平滑异同平均线 |
| `QACD_DIF()` / `QACD_MACD()` / `QACD_DDIF()` | 快速异同平均线 |
| `VTP_VPT()` / `VTP_MAVP()` | 量价曲线 |
| `WVAD_WVAD()` / `WVAD_MAWVAD()` | 威廉变异离散量 |
| `JS_JS()` / `JS_MAJS1()` / `JS_MAJS2()` / `JS_MAJS3()` | 加数线 |
| `CYE_CYEL()` / `CYE_CYES()` | 市场趋势 |
| `GDX_轨道()` / `GDX_压力线()` / `GDX_支撑线()` | 轨道线 |
| `JLHB_B()` / `JLHB_VAR2()` / `JLHB_绝路航标()` | 绝路航标 |

### 3.3 能量类指标
| 函数名 | 说明 |
|--------|------|
| `OBV_OBV()` / `OBV_MAOBV()` | 累积能量线 |
| `VR_VR()` / `VR_MAVR()` | 成交量变异率 |
| `BRAR_BR()` / `BRAR_AR()` | 情绪指标 |
| `CR_CR()` / `CR_MA1()` / `CR_MA2()` / `CR_MA3()` / `CR_MA4()` | 带状能量线 |
| `MASS_MASS()` / `MASS_MAMASS()` | 梅斯线 |
| `WAD_WAD()` / `WAD_MAWAD()` | 威廉多空力度线 |
| `PCNT_PCNT()` / `PCNT_MAPCNT()` | 幅度比 |
| `CYR_CYR()` / `CYR_MACYR()` | 市场强弱 |
| `AMO_AMOW()` / `AMO_AMO1()` / `AMO_AMO2()` | 成交金额 |
| `VOL_XT_MAVOL1()` / `VOL_XT_MAVOL2()` | 成交量均线 |
| `VRSI1()` / `VRSI2()` / `VRSI3()` | 相对强弱量 |
| `HSL_HSL()` / `HSL_MAHSL()` | 换手线 |

### 3.4 均线系统
| 函数名 | 说明 |
|--------|------|
| `SMA(period)` | N日简单移动平均线（5/10/20/30/60/120日） |
| `MA_XT_MA1()` / `MA_XT_MA2()` / `MA_XT_MA3()` / `MA_XT_MA4()` | 均线（5/10/20/60日） |
| `EXPMA_EXP1()` / `EXPMA_EXP2()` | 指数平均线（12/50日） |
| `BBI()` | 多空均线 |
| `ACD_ACD()` / `ACD_MAACD()` | 升降线 |
| `HMA_HMA1()` ~ `HMA_HMA5()` | 高价平均线（6/12/30/70/90日） |
| `LMA_LMA1()` ~ `LMA_LMA5()` | 低价平均线（6/12/30/70/90日） |
| `VMA_VMA1()` ~ `VMA_VMA5()` | 变异平均线 |
| `AMV_AMV1()` / `AMV_AMV2()` / `AMV_AMV3()` / `AMV_AMV4()` | 成本均线（5/13/34/60日） |
| `BBIBOLL_BBIBOLL()` / `BBIBOLL_UPR()` / `BBIBOLL_DWN()` | 多空布林线 |
| `ALLIGAT_上唇()` / `ALLIGAT_牙齿()` / `ALLIGAT_下颚()` | 鳄鱼线 |
| `GMMA_MA3()` ~ `GMMA_MA60()` | 顾比均线（12条均线） |
| `CROSS_UP(n1,n2)` | N1上穿N2金叉判断 |
| `CROSS_DOWN(n1,n2)` | N1下穿N2死叉判断 |
| `PRICE_MA_LINE_ANAL(n)` | 价格在N均线上方判断 |
| `MA_LINE_ANAL(n1,n2)` | N1均线在N2均线上方判断 |

### 3.5 路径类指标
| 函数名 | 说明 |
|--------|------|
| `PBX_PBX1()` ~ `PBX_PBX6()` | 瀑布线（6条） |
| `ENE_UPPER()` / `ENE_LOWER()` / `ENE_ENE()` | 轨道线 |
| `MIKE_STOR()` / `MIKE_MIDR()` / `MIKE_WEKR()` / `MIKE_WEKS()` / `MIKE_MIDS()` / `MIKE_STOS()` | 麦克支撑压力 |
| `XS_SUP()` / `XS_SDN()` / `XS_LUP()` / `XS_LDN()` | 薛斯通道 |
| `TQN_周期高点()` / `TQN_周期低点()` / `TQN_平空开多()` / `TQN_平多开空()` | 唐奇安通道 |

### 3.6 WorldQuant Alpha 因子（101-191）
| 函数名 | 说明 |
|--------|------|
| `alpha001()` ~ `alpha191()` | 完整的 WorldQuant Formula 101 系列因子 |
| 涵盖类型 | 动量、反转、波动率、相关性、排名、衰减、成交量、价格等 |

### 3.7 交易信号类
| 函数名 | 说明 |
|--------|------|
| `six_pulse_excalibur_hist()` | 六脉神剑（多指标综合买卖信号） |
| `small_fruit_band_trading_1()` | 小波段交易买卖点识别 |
| `small_fruit_band_trading_2()` | 大波段交易买卖点识别 |
| `band_supe_buy_sell()` | 波段超级买卖信号 |
| `KDJ_KD金叉()` / `KDJ_KD死叉()` | KDJ金叉/死叉信号 |
| `RSI_金叉()` / `RSI_死叉()` | RSI金叉/死叉信号 |
| `WR_金叉()` | WR金叉信号 |
| `PSY_金叉()` / `PSY_死叉()` | PSY金叉/死叉信号 |
| `BARSLASTCOUNT_UP()` | 连续上涨天数 |
| `BARSLASTCOUNT_DOWN()` | 连续下跌天数 |
| `HHVBARS(n)` | N日最高值到当前周期数 |
| `LLVBARS(n)` | N日最低值到当前周期数 |

### 3.8 风险收益指标（需指数基准）
| 函数名 | 说明 |
|--------|------|
| `roll_alpha(n)` | N日Alpha（5/10/20/30/60/120日） |
| `roll_beta(n)` | N日Beta |
| `roll_sharpe_ratio(n)` | N日夏普比率 |
| `roll_annual_volatility(n)` | N日年化波动率 |
| `roll_max_drawdown(n)` | N日最大回撤 |
| `roll_up_capture(n)` | N日上涨捕获率 |
| `roll_down_capture(n)` | N日下跌捕获率 |
| `calculate_momentum_score(n)` | N日回归动量评分 |

### 3.9 价格与统计类因子
| 函数名 | 说明 |
|--------|------|
| `cacal_zdf(n)` | N日涨跌幅（5/10/20/30/60/120日） |
| `cacal_price_line_zdf(n)` | 价格距离N日均线涨跌幅 |
| `cacal_line_line_zdf(n1,n2)` | N1均线距离N2均线涨跌幅 |
| `cacal_skew(n)` | N日偏度 |
| `cacal_kurt(n)` | N日峰度 |
| `SLOPE(n)` | N日回归斜率 |
| `STD(n)` | N日标准差 |

### 3.10 神系指标
| 函数名 | 说明 |
|--------|------|
| `SG_XDT_QR()` / `SG_XDT_MQR1()` / `SG_XDT_MQR2()` | 心电图（需指数数据） |
| `SG_NDB_DK()` / `SG_NDB_MDK1()` / `SG_NDB_MDK2()` | 脑电波 |
| `SG_SMX_ZY1()` / `SG_SMX_ZY2()` / `SG_SMX_ZY3()` | 生命线（需指数数据） |
| `SG_LB_量比()` / `SG_LB_MA5()` / `SG_LB_MA10()` | 量比（需指数数据） |
| `SG_PF()` | 强势股评分（需指数数据） |

### 3.11 龙系指标
| 函数名 | 说明 |
|--------|------|
| `RAD_RADER1()` / `RAD_RADERMA()` | 威力雷达（需指数数据） |
| `LON_LON()` / `LON_LONMA()` / `LON_LONT()` | 龙系长线 |
| `SHT_SHT()` / `SHT_SHTMA()` | 龙系短线 |
| `ZLJC_JCS()` / `ZLJC_JCM()` / `ZLJC_JCL()` | 主力进出 |
| `ZLMM_MMS()` / `ZLMM_MMM()` / `ZLMM_MML()` | 主力买卖 |
| `SLZT_白龙()` / `SLZT_黄龙()` / `SLZT_紫龙()` / `SLZT_青龙()` / `SLZT_红龙()` / `SLZT_蓝龙()` | 神龙在天 |
| `ADVOL_ADVOL()` / `ADVOL_MA1()` / `ADVOL_MA2()` | 龙系离散量 |

### 3.12 鬼系及其他指标
| 函数名 | 说明 |
|--------|------|
| `CYS()` | 市场盈亏 |
| `CYW()` | 主力控盘 |
| `JAX_J()` / `JAX_A()` / `JAX_X()` | 济安线 |
| `XJDX_J()` / `XJDX_D()` / `XJDX_K()` | 超级短线 |
| `ZJTJ_无庄控盘()` / `ZJTJ_开始控盘()` / `ZJTJ_有庄控盘()` / `ZJTJ_主力出货()` | 庄家抬轿 |
| `BDZX_AK()` / `BDZX_AD1()` / `BDZX_AJ()` / `BDZX_买进()` / `BDZX_卖出()` | 波段之星 |
| `LHXJ_主力弃盘()` / `LHXJ_主力控盘()` | 猎狐先觉 |
| `LYJH_机构做空能量线()` / `LYJH_机构做多能量线()` | 猎鹰歼狐 |
| `JFZX_多头力量()` / `JFZX_空头力量()` | 飓风智能中线 |
| `CYHT_SK()` / `CYHT_SD()` / `CYHT_卖出()` / `CYHT_买进()` | 财运亨通 |
| `BSQJ_B买()` / `BSQJ_持仓()` / `BSQJ_S卖()` / `BSQJ_空仓()` | 买卖区间 |
| `CDP_STD_CDP()` / `CDP_STD_AH()` / `CDP_STD_NH()` / `CDP_STD_NL()` / `CDP_STD_AL()` | 逆势操作 |

### 3.13 交易策略类（含买卖信号）
| 函数名 | 说明 |
|--------|------|
| `MA_交易_MA1()` / `MA_交易_MA2()` / `MA_交易_平空开多()` / `MA_交易_平多开空()` | MA均线交易系统 |
| `MACD_交易_DIFF()` / `MACD_交易_DEA()` / `MACD_交易_MACD()` / `MACD_交易_平空开多()` / `MACD_交易_平多开空()` | MACD交易系统 |
| `KDJ_交易_K()` / `KDJ_交易_D()` / `KDJ_交易_J()` / `KDJ_交易_平空开多()` / `KDJ_交易_平多开空()` | KDJ交易系统 |

## 4. 系统架构

### 4.1 核心类：`xg_factor`
```python
class xg_factor:
    """
    小果因子库核心计算类
    
    功能：提供所有因子计算方法的统一入口
    """
    def __init__(self, df='', index_df=''):
        """
        初始化因子计算实例
        
        参数:
            df: pandas.DataFrame，股票OHLCV数据
                必须包含列: date, open, high, low, close, volume, amount
            index_df: pandas.DataFrame，指数数据（可选）
                用于计算Alpha、Beta等相对指标
                必须包含列: date, close
        """
据列名自动映射
系统自动将标准列名映射为内部简写，便于快速调用：

原始列名	重命名后	简写别名
close	closePrice	C / close
open	openPrice	O / open
high	highestPrice	H / high
low	lowestPrice	L / low
volume	turnoverVol	V / volume
amount	turnoverValue	AMOUNT / amount
4.3 底层技术指标函数库（xg_tdx_func）
系统内置了通达信风格的底层技术指标计算函数：

函数名	说明	函数名	说明
MA(S,N)	简单移动平均	EMA(S,N)	指数移动平均
SMA(S,N,M)	中国式移动平均	WMA(S,N)	加权移动平均
HHV(S,N)	N日最高值	LLV(S,N)	N日最低值
HHVBARS(S,N)	最高值位置	LLVBARS(S,N)	最低值位置
REF(S,N)	引用N日前数据	DIFF(S,N)	差分
STD(S,N)	N日标准差	SUM(S,N)	N日累和
MAX(S1,S2)	最大值	MIN(S1,S2)	最小值
IF(S,A,B)	条件判断	CROSS(S1,S2)	金叉判断
COUNT(S,N)	N日条件计数	BARSLAST(S)	上次条件成立至今
SLOPE(S,N)	N日回归斜率	AVEDEV(S,N)	平均绝对偏差
FORCAST(S,N)	N日预测值	BACKSET(X,N)	未来函数（向后赋值）
ZIG(CLOSE,X)	之字转向	PEAK() / TROUGH()	波峰/波谷

# 例子单只股票因子计算
'''
from xg_factor_trader import xg_factor_trader

# 1. 初始化批量计算器（增量模式）
api = xg_factor_trader(
    max_workers=4,              # 使用4个进程
    start_date='20240101',      # 数据起始日期
    end_date='20241231',        # 数据截止日期
    verbose=True,               # 显示详细信息
    use_multiprocess=True,      # 使用多进程
    chunk_size=50,              # 每批50只
    stage_size=200,             # 每阶段200只
    use_async_io=True,          # 使用异步IO
    force_recalc=False          # 增量计算，跳过已计算
)

# 2. 生成因子列表
api.get_all_factor_table()
# 输出: data/全部因子/全部因子.xlsx 和 全部因子.json

# 3. 执行批量计算
api.cacal_all_stock_factor()

# 4. 查看结果
# 每个股票生成一个因子文件: data/全部因子数据/{stock_code}.parquet
df_513100 = api.get_factor_data('513100.SH')
print(df_513100.shape)  # (交易日数, 因子数+基础列)
print(df_513100.columns.tolist())

# 5. 获取所有股票因子数据（合并）
all_factors = api.get_all_factor_data()
print(f"全部数据: {all_factors.shape}")

# 6. 查看失败列表
# data/全部因子数据/失败列表.xlsx
'''
# 例子2批量计算全市场因子
'''
from xg_factor_trader import xg_factor_trader

# 1. 初始化批量计算器（增量模式）
api = xg_factor_trader(
    max_workers=4,              # 使用4个进程
    start_date='20240101',      # 数据起始日期
    end_date='20241231',        # 数据截止日期
    verbose=True,               # 显示详细信息
    use_multiprocess=True,      # 使用多进程
    chunk_size=50,              # 每批50只
    stage_size=200,             # 每阶段200只
    use_async_io=True,          # 使用异步IO
    force_recalc=False          # 增量计算，跳过已计算
)

# 2. 生成因子列表
api.get_all_factor_table()
# 输出: data/全部因子/全部因子.xlsx 和 全部因子.json

# 3. 执行批量计算
api.cacal_all_stock_factor()

# 4. 查看结果
# 每个股票生成一个因子文件: data/全部因子数据/{stock_code}.parquet
df_513100 = api.get_factor_data('513100.SH')
print(df_513100.shape)  # (交易日数, 因子数+基础列)
print(df_513100.columns.tolist())

# 5. 获取所有股票因子数据（合并）
all_factors = api.get_all_factor_data()
print(f"全部数据: {all_factors.shape}")

# 6. 查看失败列表
# data/全部因子数据/失败列表.xlsx
'''
# 3完整例子
'''
# ============================================================
# 小果量化因子库 - 快速开始示例
# ============================================================

from xg_factor import xg_factor
from xg_factor_trader import xg_factor_trader
import pandas as pd
import numpy as np

print("=" * 60)
print("小果量化因子库 - 快速开始")
print("=" * 60)

# ============================================================
# 第一部分：单只股票因子计算
# ============================================================
print("\n[1] 单只股票因子计算")

# 1.1 加载数据
stock = '513100.SH'
df = pd.read_parquet(f'data/历史数据/{stock}.parquet')
df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
df = df.sort_values('date').reset_index(drop=True)

# 1.2 加载指数数据
index_df = pd.read_parquet('data/指数数据/000300.SH.parquet')
index_df['date'] = pd.to_datetime(index_df['date'].astype(str), format='%Y%m%d')
index_df = index_df.sort_values('date').reset_index(drop=True)

# 1.3 初始化因子计算器
models = xg_factor(df=df, index_df=index_df)

# 1.4 计算因子
df['5日涨跌幅'] = models.cacal_zdf(5)
df['10日涨跌幅'] = models.cacal_zdf(10)
df['MACD金叉'] = models.MACD_金叉()
df['KDJ金叉'] = models.KDJ_KD金叉()
df['RSI'] = models.RSI1()
df['CCI'] = models.CCI()
df['BBI'] = models.BBI()
df['SAR'] = models.SAR()
df['Alpha001'] = models.alpha001()
df['Alpha005'] = models.alpha005()

# 1.5 查看最新数据
latest = df.iloc[-1]
print(f"\n最新因子数据 ({latest['date']}):")
print(f"  收盘价: {latest['close']:.4f}")
print(f"  5日涨跌幅: {latest['5日涨跌幅']:.2f}%")
print(f"  10日涨跌幅: {latest['10日涨跌幅']:.2f}%")
print(f"  MACD金叉: {latest['MACD金叉']}")
print(f"  KDJ金叉: {latest['KDJ金叉']}")
print(f"  RSI: {latest['RSI']:.2f}")
print(f"  CCI: {latest['CCI']:.2f}")
print(f"  Alpha001: {latest['Alpha001']:.6f}")

# ============================================================
# 第二部分：批量计算全市场因子
# ============================================================
print("\n[2] 批量计算全市场因子（增量模式）")

# 2.1 初始化批量计算器
api = xg_factor_trader(
    max_workers=4,
    start_date='20240101',
    end_date='20241231',
    verbose=True,
    use_multiprocess=True,
    force_recalc=False        # 增量模式
)

# 2.2 生成因子列表
api.get_all_factor_table()

# 2.3 执行批量计算
# api.cacal_all_stock_factor()  # 取消注释以执行

# 2.4 获取结果
df_result = api.get_factor_data('513100.SH')
print(f"\n因子数据形状: {df_result.shape}")
print(f"因子列数: {len(df_result.columns)}")

# ============================================================
# 第三部分：因子数据导出
# ============================================================
print("\n[3] 因子数据导出")

# 3.1 导出最新日期的因子数据
latest_date = df['date'].max()
df_latest = df[df['date'] == latest_date].copy()
df_latest['date'] = df_latest['date'].dt.strftime('%Y-%m-%d')

# 3.2 选择关键因子列
key_columns = ['date', '证券代码', '证券名称', 'close', '5日涨跌幅', '10日涨跌幅',
               'MACD金叉', 'KDJ金叉', 'RSI', 'CCI', 'BBI', 'Alpha001']
df_export = df_latest[key_columns]

# 3.3 保存
df_export.to_excel('因子结果_最新.xlsx', index=False)
print(f"最新因子数据已保存: 因子结果_最新.xlsx")
print(f"共 {len(df_export)} 条记录")

print("\n" + "=" * 60)
print("小果量化因子库 - 运行完成")
print("=" * 60)
'''
# 全部的因子库计算
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
# 底层的支持函数框架
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
# 因子计算例子
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from xg_factor import xg_factor
from tqdm import tqdm
class xg_factor_trader:
    def __init__(self,
            index_stock='000300.SH',
            start_date='20260101',
            end_date='20500101'):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.index_stock=index_stock
        self.start_date=start_date
        self.end_date=end_date
        self.adj_type = 'none'
    def adjust_price(self, df):
        '''
        根据复权方式调整价格
        '''
        if self.adj_type == 'none':
            return df
        
        if 'preClose' in df.columns:
            try:
                df['adj_factor'] = 1.0
                for i in range(1, len(df)):
                    if df.loc[i, 'preClose'] > 0:
                        actual_return = df.loc[i, 'close'] / df.loc[i, 'preClose']
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor'] * actual_return
                    else:
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor']
                
                if self.adj_type in ['front', 'front_ratio']:
                    last_factor = df['adj_factor'].iloc[-1]
                    df['adj_factor'] = df['adj_factor'] / last_factor
                
                price_cols = ['open', 'high', 'low', 'close']
                for col in price_cols:
                    if col in df.columns:
                        df[col] = df[col] * df['adj_factor']
                
                df = df.drop(columns=['adj_factor'])
            except Exception as e:
                print(f"  复权计算出错: {e}")
                return df
        else:
            print(f"  警告: 没有preClose列，使用原始价格")
        
        return df
    def _convert_to_serializable(self, obj):
        '''
        递归转换不可序列化的对象为JSON可序列化格式
        '''
        if isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj) if not np.isnan(obj) else None
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif pd.isna(obj):
            return None
        else:
            return obj
    
    def get_stock_data(self, stock_code):
        '''读取单个股票历史数据'''
        try:
            df = pd.read_parquet(r'{}/data/历史数据/{}.parquet'.format(self.path, stock_code),
                engine='pyarrow',use_threads=True)
            
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            df = df[(df['date'] >= pd.to_datetime(self.start_date)) & 
                    (df['date'] <= pd.to_datetime(self.end_date))]
            df = df.sort_values('date').reset_index(drop=True)
            
            # 删除无效数据行
            df = df[df['close'] > 0]
            df = df[df['open'] > 0]
            
            # 应用复权
            df = self.adjust_price(df)
            
            # 计算涨跌幅
            df['zdf'] = df['close'].pct_change()
            
            return df
        except Exception as e:
            print(f"加载股票数据出错 {stock_code}: {e}")
            return pd.DataFrame()
    
    def _load_single_stock(self, stock):
        '''单个股票加载函数（用于多线程）'''
        try:
            df = self.get_stock_data(stock)
            if not df.empty:
                return (stock, df, True, f"数据加载成功: {len(df)} 行")
            else:
                return (stock, None, False, "数据加载失败")
        except Exception as e:
            return (stock, None, False, f"加载异常: {e}")
    
    def adjust_price(self, df):
        '''
        根据复权方式调整价格
        '''
        if self.adj_type == 'none':
            return df
        
        if 'preClose' in df.columns:
            try:
                df['adj_factor'] = 1.0
                for i in range(1, len(df)):
                    if df.loc[i, 'preClose'] > 0:
                        actual_return = df.loc[i, 'close'] / df.loc[i, 'preClose']
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor'] * actual_return
                    else:
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor']
                
                if self.adj_type in ['front', 'front_ratio']:
                    last_factor = df['adj_factor'].iloc[-1]
                    df['adj_factor'] = df['adj_factor'] / last_factor
                
                price_cols = ['open', 'high', 'low', 'close']
                for col in price_cols:
                    if col in df.columns:
                        df[col] = df[col] * df['adj_factor']
                
                df = df.drop(columns=['adj_factor'])
            except Exception as e:
                print(f"  复权计算出错: {e}")
                return df
        else:
            print(f"  警告: 没有preClose列，使用原始价格")
        
        return df
    def get_index_data(self):
        '''读取指数历史数据'''
        try:
        
            file_path = r'{}/data/指数数据/{}.parquet'.format(self.path, self.index_stock)
            if not os.path.exists(file_path):
                print(f"指数文件不存在: {file_path}")
                return pd.DataFrame()
            
            df = pd.read_parquet(file_path,engine='pyarrow',use_threads=True)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            df = df[(df['date'] >= pd.to_datetime(self.start_date)) & 
                    (df['date'] <= pd.to_datetime(self.end_date))]
            df = df.sort_values('date').reset_index(drop=True)
            df = df[df['close'] > 0]
            df = df[df['open'] > 0]
            
            print(f"指数数据加载成功: {len(df)} 行")
            return df
        except Exception as e:
            print(f"加载指数数据出错: {e}")
            return pd.DataFrame()
if __name__=='__main__':
    stock='513100.SH'
    api=xg_factor_trader()
    df=api.get_stock_data(stock)
    index_df=api.get_index_data()
    models=xg_factor(df=df,index_df=index_df)
    result=models.MACD_金叉()
    df['因子']=result
    df=df[['date','证券代码','证券名称','因子']]
    print(df)
# 全部因子计算系统
import pandas as pd
import numpy as np
import os
from datetime import datetime
import json
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from tqdm import tqdm
import multiprocessing
import gc
import shutil
import pickle
from functools import lru_cache
import re

warnings.filterwarnings("ignore")


# ========== 模块级函数（用于多进程） ==========
def _call_factor_function_worker(models, func_str):
    """因子函数调用工作函数（修复版 - 正确解析参数）"""
    if not func_str:
        return None
    
    # 提取函数名
    func_name = func_str.split('(')[0].strip() if '(' in func_str else func_str.strip()
    
    if not hasattr(models, func_name):
        return None
    
    method = getattr(models, func_name)
    if not callable(method):
        return None
    
    # 如果没有参数，直接调用
    if '(' not in func_str or func_str.endswith('()'):
        try:
            return method()
        except Exception as e:
            return None
    
    # 解析参数
    try:
        start = func_str.index('(') + 1
        end = func_str.rindex(')')
        params_str = func_str[start:end].strip()
        
        if not params_str:
            return method()
        
        # 解析参数 - 处理带括号的复杂参数
        args = {}
        # 按逗号分割，但跳过括号内的逗号
        params = re.split(r',(?![^()]*\))', params_str)
        
        for param in params:
            param = param.strip()
            if not param:
                continue
                
            if '=' in param:
                key, value = param.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 尝试转换为数值
                try:
                    if value.lower() == 'true':
                        args[key] = True
                    elif value.lower() == 'false':
                        args[key] = False
                    elif value.lower() == 'none':
                        args[key] = None
                    elif '.' in value:
                        args[key] = float(value)
                    else:
                        args[key] = int(value)
                except:
                    # 尝试去除引号
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        args[key] = value[1:-1]
                    else:
                        args[key] = value
            else:
                # 位置参数 - 尝试转换为数值
                try:
                    if '.' in param:
                        args['arg'] = float(param)
                    else:
                        args['arg'] = int(param)
                except:
                    args['arg'] = param
        
        # 调用方法
        try:
            return method(**args)
        except TypeError as e:
            # 如果参数不匹配，尝试不带参数调用
            try:
                return method()
            except:
                return None
    except Exception as e:
        return None


def calculate_single_stock_worker_optimized(stock_code, path, index_stock, start_date, end_date, text, adj_type='none'):
    """多进程工作函数：计算单只股票的所有因子（优化版 - 修复数据对齐）"""
    try:
        from xg_factor import xg_factor
        
        file_path = r'{}/data/历史数据/{}.parquet'.format(path, stock_code)
        if not os.path.exists(file_path):
            return (stock_code, False, "数据文件不存在")
        
        # 只读取需要的列，减少内存
        use_cols = ['date','证券代码','证券名称' ,'open', 'high', 'low', 'close', 'volume', 'amount']
        if adj_type != 'none':
            use_cols.append('preClose')
        
        df = pd.read_parquet(file_path, columns=use_cols, engine='pyarrow', use_threads=True)
        df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
        
        # 使用query过滤，速度更快
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
        df = df.sort_values('date').reset_index(drop=True)
        
        # 过滤无效数据
        df = df[(df['close'] > 0) & (df['open'] > 0)]
        
        if df.empty:
            return (stock_code, False, "无有效数据")
        
        # 获取指数数据
        index_file = r'{}/data/指数数据/{}.parquet'.format(path, index_stock)
        index_df = pd.DataFrame()
        if os.path.exists(index_file):
            try:
                index_df = pd.read_parquet(index_file, columns=['date', 'open', 'close'], 
                                          engine='pyarrow', use_threads=True)
                index_df['date'] = pd.to_datetime(index_df['date'].astype(str), format='%Y%m%d')
                index_df = index_df[(index_df['date'] >= start_dt) & (index_df['date'] <= end_dt)]
                index_df = index_df.sort_values('date').reset_index(drop=True)
            except:
                index_df = pd.DataFrame()
        
        # 创建因子计算实例
        models = xg_factor(df=df, index_df=index_df)
        
        # 预分配结果列
        for name in text.keys():
            df[name] = np.nan
        
        # 批量计算因子
        for name, func_str in text.items():
            try:
                result = _call_factor_function_worker(models, func_str)
                
                if result is None:
                    continue
                elif isinstance(result, pd.Series):
                    # 对齐长度 - 确保与df长度一致
                    if len(result) == len(df):
                        df[name] = result.values
                    elif len(result) < len(df):
                        # 前面填充NaN
                        temp = pd.Series([np.nan] * (len(df) - len(result)) + list(result))
                        df[name] = temp.values
                    else:
                        # 截取前len(df)个
                        df[name] = result.iloc[:len(df)].values
                elif isinstance(result, (int, float, np.number)):
                    # 标量值，整列赋值
                    df[name] = result
                elif isinstance(result, (list, tuple, np.ndarray)):
                    if len(result) == len(df):
                        df[name] = result
                    elif len(result) < len(df):
                        temp = [np.nan] * (len(df) - len(result)) + list(result)
                        df[name] = temp
                    else:
                        df[name] = result[:len(df)]
                else:
                    try:
                        if hasattr(result, '__len__') and len(result) == len(df):
                            df[name] = result
                    except:
                        pass
            except Exception as e:
                continue
        
        if df.shape[0] > 0:
            save_path = r'{}/data/全部因子数据/{}.parquet'.format(path, stock_code)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_parquet(save_path, compression='zstd')
            return (stock_code, True, "成功")
        else:
            return (stock_code, False, "数据为空")
            
    except Exception as e:
        return (stock_code, False, str(e))


class xg_factor_trader:
    def __init__(self,
            index_stock='000300.SH',
            start_date='20200101',
            end_date='20500101',
            max_workers=None,
            verbose=False,
            use_multiprocess=True,
            chunk_size=30,
            stage_size=200,
            use_async_io=True,
            force_recalc=False):
        """
        初始化因子计算器（超级优化版）
        
        Args:
            index_stock: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            max_workers: 最大进程数
            verbose: 是否显示详细信息
            use_multiprocess: 是否使用多进程
            chunk_size: 批次处理大小
            stage_size: 阶段大小
            use_async_io: 是否使用异步IO
            force_recalc: 是否强制重新计算所有股票（True=覆盖计算全部，False=跳过已计算的）
        """
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.index_stock = index_stock
        self.start_date = start_date
        self.end_date = end_date
        self.chunk_size = chunk_size
        self.stage_size = stage_size
        self.use_async_io = use_async_io
        self.force_recalc = force_recalc
        
        if max_workers is None:
            self.max_workers = max(1, multiprocessing.cpu_count() - 1)
        else:
            self.max_workers = max_workers
        
        self.verbose = verbose
        self.use_multiprocess = use_multiprocess
        
        # 缓存指数数据
        self.index_df = self.get_index_data()
        self.adj_type = 'none'
        
        # 加载因子表
        try:
            with open(r'因子表.json', 'r+', encoding='utf-8') as f:
                com = f.read()
            self.text = json.loads(com)
        except:
            self.text = {}
            print("警告: 因子表.json 不存在，请先创建")
        
        # 统计
        self.success_count = 0
        self.fail_count = 0
        self.fail_list = []
        self.stage_results = []
        
        # 创建目录
        os.makedirs(r'{}/data/全部因子数据'.format(self.path), exist_ok=True)
        
        self.stock_list = None
        self._processed_cache = set()  # 缓存已处理的股票
        
        # 如果强制重算，清空已计算的缓存
        if self.force_recalc:
            print("⚠️  强制重算模式已开启，将重新计算所有股票并覆盖已有数据")
            # 清理已处理缓存，但保留目录
            self._processed_cache = set()

    def get_all_factor_table(self):
        """生成因子列表"""
        data = pd.DataFrame()
        text_copy = self.text.copy()
        text_copy['close'] = '默认'
        text_copy['high'] = '默认'
        text_copy['low'] = '默认'
        text_copy['open'] = '默认'
        text_copy['amount'] = '默认'
        text_copy['volume'] = '默认'
        text_copy['zdf'] = '默认'

        for name, func in text_copy.items():
            data = pd.concat([data, pd.DataFrame({'因子名称': [name], '因子函数': [func]})], ignore_index=True)
        
        os.makedirs(r'{}/data/全部因子'.format(self.path), exist_ok=True)
        data.to_excel(r'{}/data/全部因子/全部因子.xlsx'.format(self.path))
        data.to_json(r'{}/data/全部因子/全部因子.json'.format(self.path), orient='records', force_ascii=False)
        print(f"因子列表已生成，共 {len(data)} 个因子")

    @lru_cache(maxsize=128)
    def _get_stock_data_cached(self, stock_code):
        """缓存股票数据"""
        return self.get_stock_data(stock_code)

    def get_stock_data(self, stock_code):
        """获取单只股票数据（优化版）"""
        try:
            file_path = r'{}/data/历史数据/{}.parquet'.format(self.path, stock_code)
            if not os.path.exists(file_path):
                return pd.DataFrame()
            
            # 只读需要的列
            use_cols = ['date','证券代码','证券名称', 'open', 'high', 'low', 'close', 'volume', 'amount']
            if self.adj_type != 'none':
                use_cols.append('preClose')
            
            df = pd.read_parquet(file_path, columns=use_cols, engine='pyarrow', use_threads=True)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            
            start_dt = pd.to_datetime(self.start_date)
            end_dt = pd.to_datetime(self.end_date)
            df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
            df = df.sort_values('date').reset_index(drop=True)
            df = df[(df['close'] > 0) & (df['open'] > 0)]
            
            if df.empty:
                return df
            
            df = self.adjust_price(df)
            df['zdf'] = df['close'].pct_change() * 100
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def adjust_price(self, df):
        """价格复权（优化版）"""
        if self.adj_type == 'none' or 'preClose' not in df.columns:
            return df
        
        try:
            # 使用向量化操作
            df['adj_factor'] = 1.0
            pre_close = df['preClose'].values
            close = df['close'].values
            
            # 批量计算复权因子
            for i in range(1, len(df)):
                if pre_close[i] > 0:
                    df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor'] * (close[i] / pre_close[i])
                else:
                    df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor']
            
            if self.adj_type in ['front', 'front_ratio']:
                df['adj_factor'] = df['adj_factor'] / df['adj_factor'].iloc[-1]
            
            price_cols = ['open', 'high', 'low', 'close']
            for col in price_cols:
                if col in df.columns:
                    df[col] = df[col] * df['adj_factor']
            df = df.drop(columns=['adj_factor'])
        except Exception as e:
            pass
        return df
    
    def get_index_data(self):
        """获取指数数据"""
        try:
            file_path = r'{}/data/指数数据/{}.parquet'.format(self.path, self.index_stock)
            if not os.path.exists(file_path):
                return pd.DataFrame()
            df = pd.read_parquet(file_path, columns=['date', 'open', 'close'], 
                                engine='pyarrow', use_threads=True)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            
            start_dt = pd.to_datetime(self.start_date)
            end_dt = pd.to_datetime(self.end_date)
            df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
            df = df.sort_values('date').reset_index(drop=True)
            df = df[(df['close'] > 0) & (df['open'] > 0)]
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def _call_factor_function(self, models, func_str):
        """调用因子函数（单线程版本 - 修复参数解析）"""
        if not func_str:
            return None
        
        func_name = func_str.split('(')[0].strip() if '(' in func_str else func_str.strip()
        
        if not hasattr(models, func_name):
            return None
        
        method = getattr(models, func_name)
        if not callable(method):
            return None
        
        if '(' not in func_str or func_str.endswith('()'):
            try:
                return method()
            except:
                return None
        
        try:
            start = func_str.index('(') + 1
            end = func_str.rindex(')')
            params_str = func_str[start:end].strip()
            
            if not params_str:
                return method()
            
            # 解析参数 - 处理带括号的复杂参数
            args = {}
            params = re.split(r',(?![^()]*\))', params_str)
            
            for param in params:
                param = param.strip()
                if not param:
                    continue
                    
                if '=' in param:
                    key, value = param.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    try:
                        if value.lower() == 'true':
                            args[key] = True
                        elif value.lower() == 'false':
                            args[key] = False
                        elif value.lower() == 'none':
                            args[key] = None
                        elif '.' in value:
                            args[key] = float(value)
                        else:
                            args[key] = int(value)
                    except:
                        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                            args[key] = value[1:-1]
                        else:
                            args[key] = value
                else:
                    try:
                        if '.' in param:
                            args['arg'] = float(param)
                        else:
                            args['arg'] = int(param)
                    except:
                        args['arg'] = param
            
            try:
                return method(**args)
            except TypeError as e:
                try:
                    return method()
                except:
                    return None
        except:
            return None
    
    def cacal_stock_factor(self, stock='513100.SH'):
        """单只股票因子计算（修复版）"""
        try:
            from xg_factor import xg_factor
            df = self.get_stock_data(stock_code=stock)
            if df.empty:
                print(f"股票 {stock} 无数据")
                return False
            
            print(f"股票 {stock} 数据加载成功: {len(df)} 行")
            print(f"因子数量: {len(self.text)} 个")
            
            models = xg_factor(df=df, index_df=self.index_df)
            factor_items = list(self.text.items())
            
            for name, func_str in tqdm(factor_items, desc=f"计算 {stock}", unit="个", leave=False, disable=not self.verbose):
                try:
                    result = self._call_factor_function(models, func_str)
                    if result is None:
                        df[name] = np.nan
                        continue
                    
                    # 处理不同类型的返回值
                    if isinstance(result, pd.Series):
                        # 对齐长度
                        if len(result) < df.shape[0]:
                            # 结果长度小于df，在前面填充NaN
                            result = pd.concat([pd.Series([np.nan] * (df.shape[0] - len(result))), result], ignore_index=True)
                        elif len(result) > df.shape[0]:
                            # 结果长度大于df，截取前df.shape[0]个
                            result = result.iloc[:df.shape[0]]
                        df[name] = result.values
                        
                    elif isinstance(result, (list, tuple, np.ndarray)):
                        # 列表、元组、数组
                        if len(result) < df.shape[0]:
                            # 前面填充NaN
                            result = [np.nan] * (df.shape[0] - len(result)) + list(result)
                        elif len(result) > df.shape[0]:
                            # 截取前df.shape[0]个
                            result = result[:df.shape[0]]
                        df[name] = result
                        
                    elif isinstance(result, (int, float, np.number)):
                        # 标量值，直接赋值（整列都是同一个值）
                        df[name] = result
                        
                    else:
                        # 其他类型尝试转换
                        try:
                            if hasattr(result, '__len__') and len(result) == df.shape[0]:
                                df[name] = result
                            else:
                                df[name] = np.nan
                        except:
                            df[name] = np.nan
                            
                except Exception as e:
                    df[name] = np.nan
            
            if df.shape[0] > 0:
                save_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                df.to_parquet(save_path, compression='zstd')
                print(f"股票 {stock} 因子计算完成，共 {df.shape[0]} 行数据")
                return True
            return False
        except Exception as e:
            print(f"股票 {stock} 计算失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _calculate_single_stock_sync(self, stock):
        """同步单线程计算单只股票（修复版）"""
        try:
            from xg_factor import xg_factor
            df = self.get_stock_data(stock_code=stock)
            if df.empty:
                return False
            
            models = xg_factor(df=df, index_df=self.index_df)
            df_len = len(df)
            
            for name, func_str in self.text.items():
                try:
                    result = self._call_factor_function(models, func_str)
                    
                    if result is None:
                        df[name] = np.nan
                    elif isinstance(result, pd.Series):
                        if len(result) == df_len:
                            df[name] = result.values
                        elif len(result) < df_len:
                            temp = pd.Series([np.nan] * (df_len - len(result)) + list(result))
                            df[name] = temp.values
                        else:
                            df[name] = result.iloc[:df_len].values
                    elif isinstance(result, (int, float, np.number)):
                        df[name] = result
                    elif isinstance(result, (list, tuple, np.ndarray)):
                        if len(result) == df_len:
                            df[name] = result
                        elif len(result) < df_len:
                            df[name] = [np.nan] * (df_len - len(result)) + list(result)
                        else:
                            df[name] = result[:df_len]
                    else:
                        try:
                            if hasattr(result, '__len__') and len(result) == df_len:
                                df[name] = result
                            else:
                                df[name] = np.nan
                        except:
                            df[name] = np.nan
                except Exception as e:
                    df[name] = np.nan
            
            if df.shape[0] > 0:
                save_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                df.to_parquet(save_path, compression='zstd')
                return True
            return False
        except Exception as e:
            if self.verbose:
                print(f"计算 {stock} 时出错: {e}")
            return False
    def get_bond_stock(self):
        '''
        可转债代码
        '''
        df_bond = pd.read_excel(r'{}/data/可转债代码/可转债代码.xlsx'.format(self.path))
        df_bond['代码'] = df_bond['代码'].apply(lambda x: str(x)[2:] + '.' + str(x)[:2])
        df_bond.columns = ['证券代码', '证券名称']
        return df_bond
    def _get_stock_list(self):
        """获取股票列表（带缓存）- 支持强制重算模式"""
        if self.stock_list is not None:
            return self.stock_list
        
        # 如果不强制重算，加载已处理缓存
        if not self.force_recalc:
            try:
                factor_path = r'{}/data/全部因子数据'.format(self.path)
                if os.path.exists(factor_path):
                    processed = [f.replace('.parquet', '') for f in os.listdir(factor_path) 
                                if f.endswith('.parquet') and f != '失败列表.xlsx']
                    self._processed_cache = set(processed)
            except:
                self._processed_cache = set()
        else:
            # 强制重算模式：清空缓存，但保留已计算文件（后续会覆盖）
            self._processed_cache = set()
            print("🔄 强制重算模式：将重新计算所有股票并覆盖已有数据文件")
        
        try:
            # 尝试从Excel读取
            excel_path = r'{}/data/基金代码/基金代码.xlsx'.format(self.path)
            if os.path.exists(excel_path):
                df_fund = pd.read_excel(excel_path)
                df_fund=df_fund[['基金代码','基金名称']]
                df_fund.columns = ['证券代码', '证券名称']
                df_bond=self.get_bond_stock()
                df=pd.concat([df_fund,df_bond],ignore_index=True)
                if '证券代码' in df.columns:
                    self.stock_list = df['证券代码'].tolist()
                    # 如果不强制重算，过滤已处理的股票
                    if not self.force_recalc and self._processed_cache:
                        original_count = len(self.stock_list)
                        self.stock_list = [s for s in self.stock_list if s not in self._processed_cache]
                        skipped_count = original_count - len(self.stock_list)
                        if skipped_count > 0:
                            print(f"⏭️  跳过已计算的股票: {skipped_count} 只")
                    
                    print(f"📊 本次需要计算的股票数: {len(self.stock_list)} 只")
                    return self.stock_list
            
            # 尝试从parquet目录获取
            hist_path = r'{}/data/历史数据'.format(self.path)
            if os.path.exists(hist_path):
                files = [f.replace('.parquet', '') for f in os.listdir(hist_path) if f.endswith('.parquet')]
                if files:
                    self.stock_list = files
                    # 如果不强制重算，过滤已处理的
                    if not self.force_recalc and self._processed_cache:
                        original_count = len(self.stock_list)
                        self.stock_list = [s for s in self.stock_list if s not in self._processed_cache]
                        skipped_count = original_count - len(self.stock_list)
                        if skipped_count > 0:
                            print(f"⏭️  跳过已计算的股票: {skipped_count} 只")
                    
                    print(f"📊 本次需要计算的股票数: {len(self.stock_list)} 只")
                    return self.stock_list
            
            self.stock_list = []
            return self.stock_list
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            self.stock_list = []
            return self.stock_list
    
    def _clear_cache(self):
        """清理缓存释放内存"""
        gc.collect()
    
    def _save_stage_checkpoint(self, stage_num, total_stages):
        """保存阶段检查点"""
        checkpoint_path = r'{}/data/全部因子数据/checkpoint.json'.format(self.path)
        checkpoint_data = {
            'stage': stage_num,
            'total_stages': total_stages,
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'force_recalc': self.force_recalc,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def cacal_all_stock_factor_single(self):
        """单线程分阶段计算所有股票因子"""
        stock_list = self._get_stock_list()
        if not stock_list:
            print("没有找到需要计算的股票数据")
            return
        
        total = len(stock_list)
        self.success_count = 0
        self.fail_count = 0
        self.fail_list = []
        self.stage_results = []
        
        total_stages = max(1, (total + self.stage_size - 1) // self.stage_size)
        
        print(f"\n{'='*60}")
        print(f"单线程分阶段计算模式")
        print(f"需要计算股票数: {total}")
        print(f"因子数量: {len(self.text)} 个")
        print(f"阶段大小: {self.stage_size} 只/阶段")
        print(f"总阶段数: {total_stages}")
        if self.force_recalc:
            print("模式: 🔄 强制重算（覆盖已有数据）")
        else:
            print("模式: 📝 增量计算（跳过已计算）")
        print(f"{'='*60}\n")
        
        start_time = datetime.now()
        
        for stage_idx in range(total_stages):
            stage_start = stage_idx * self.stage_size
            stage_end = min(stage_start + self.stage_size, total)
            stage_stocks = stock_list[stage_start:stage_end]
            
            stage_success = 0
            stage_fail = 0
            stage_start_time = datetime.now()
            
            print(f"\n阶段 {stage_idx + 1}/{total_stages} (股票 {stage_start+1}-{stage_end}/{total})")
            
            # 使用线程池进行并行IO
            if self.use_async_io and len(stage_stocks) > 10:
                with ThreadPoolExecutor(max_workers=min(8, len(stage_stocks))) as io_executor:
                    # 预加载数据
                    futures = {io_executor.submit(self.get_stock_data, stock): stock for stock in stage_stocks}
                    for future in as_completed(futures):
                        stock = futures[future]
                        try:
                            df = future.result()
                            if not df.empty:
                                self.success_count += 1
                                stage_success += 1
                                # 保存数据
                                save_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
                                df.to_parquet(save_path, compression='zstd')
                            else:
                                self.fail_count += 1
                                stage_fail += 1
                                self.fail_list.append(stock)
                        except:
                            self.fail_count += 1
                            stage_fail += 1
                            self.fail_list.append(stock)
            else:
                # 传统顺序处理
                for idx, stock in enumerate(tqdm(stage_stocks, desc=f"阶段{stage_idx+1}进度", unit="只")):
                    try:
                        success = self._calculate_single_stock_sync(stock)
                        if success:
                            self.success_count += 1
                            stage_success += 1
                        else:
                            self.fail_count += 1
                            stage_fail += 1
                            self.fail_list.append(stock)
                    except Exception as e:
                        self.fail_count += 1
                        stage_fail += 1
                        self.fail_list.append(stock)
            
            stage_elapsed = (datetime.now() - stage_start_time).total_seconds()
            self.stage_results.append({
                'stage': stage_idx + 1,
                'stocks': len(stage_stocks),
                'success': stage_success,
                'fail': stage_fail,
                'time': stage_elapsed
            })
            
            self._clear_cache()
            self._save_stage_checkpoint(stage_idx + 1, total_stages)
            
            total_elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n阶段 {stage_idx+1} 完成! 成功:{stage_success} 失败:{stage_fail} 耗时:{stage_elapsed:.1f}s")
            
            if stage_idx + 1 < total_stages:
                avg_time = total_elapsed / (stage_idx + 1)
                remaining = avg_time * (total_stages - stage_idx - 1)
                print(f"  预计剩余: {remaining:.1f}s ({remaining/60:.1f}分钟)")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        self._print_summary(total, elapsed)
    
    def cacal_all_stock_factor_multiprocess(self):
        """多进程分阶段计算所有股票因子（优化版）"""
        stock_list = self._get_stock_list()
        if not stock_list:
            print("没有找到需要计算的股票数据")
            return
        
        total = len(stock_list)
        self.success_count = 0
        self.fail_count = 0
        self.fail_list = []
        self.stage_results = []
        
        total_stages = max(1, (total + self.stage_size - 1) // self.stage_size)
        
        print(f"\n{'='*60}")
        print(f"多进程分阶段计算模式（优化版）")
        print(f"需要计算股票数: {total}")
        print(f"因子数量: {len(self.text)} 个")
        print(f"进程数: {self.max_workers}")
        print(f"批次大小: {self.chunk_size}")
        print(f"阶段大小: {self.stage_size} 只/阶段")
        print(f"总阶段数: {total_stages}")
        if self.force_recalc:
            print("模式: 🔄 强制重算（覆盖已有数据）")
        else:
            print("模式: 📝 增量计算（跳过已计算）")
        print(f"{'='*60}\n")
        
        start_time = datetime.now()
        
        for stage_idx in range(total_stages):
            stage_start = stage_idx * self.stage_size
            stage_end = min(stage_start + self.stage_size, total)
            stage_stocks = stock_list[stage_start:stage_end]
            
            stage_success = 0
            stage_fail = 0
            stage_start_time = datetime.now()
            
            print(f"\n阶段 {stage_idx + 1}/{total_stages} (股票 {stage_start+1}-{stage_end}/{total})")
            
            # 批量提交任务
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                for stock in stage_stocks:
                    future = executor.submit(
                        calculate_single_stock_worker_optimized,
                        stock,
                        self.path,
                        self.index_stock,
                        self.start_date,
                        self.end_date,
                        self.text,
                        self.adj_type
                    )
                    futures[future] = stock
                
                with tqdm(total=len(futures), desc=f"阶段{stage_idx+1}进度", unit="只") as pbar:
                    for future in as_completed(futures):
                        try:
                            stock, success, msg = future.result(timeout=600)
                            if success:
                                self.success_count += 1
                                stage_success += 1
                            else:
                                self.fail_count += 1
                                stage_fail += 1
                                self.fail_list.append(stock)
                            pbar.set_postfix_str(f"成功:{self.success_count} 失败:{self.fail_count}")
                        except Exception as e:
                            self.fail_count += 1
                            stage_fail += 1
                            stock = futures[future]
                            self.fail_list.append(stock)
                            if self.verbose:
                                print(f"股票 {stock} 计算异常: {e}")
                        pbar.update(1)
            
            stage_elapsed = (datetime.now() - stage_start_time).total_seconds()
            self.stage_results.append({
                'stage': stage_idx + 1,
                'stocks': len(stage_stocks),
                'success': stage_success,
                'fail': stage_fail,
                'time': stage_elapsed
            })
            
            self._clear_cache()
            self._save_stage_checkpoint(stage_idx + 1, total_stages)
            
            total_elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n阶段 {stage_idx+1} 完成!")
            
            if stage_idx + 1 < total_stages:
                avg_time = total_elapsed / (stage_idx + 1)
                remaining = avg_time * (total_stages - stage_idx - 1)
                print(f"  预计剩余: {remaining:.1f}s ({remaining/60:.1f}分钟)")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        self._print_summary(total, elapsed)
    
    def _print_summary(self, total, elapsed):
        """打印计算摘要"""
        print(f"\n{'='*60}")
        print(f"计算完成!")
        print(f"{'='*60}")
        print(f"总股票数: {total}")
        print(f"成功: {self.success_count} 只")
        print(f"失败: {self.fail_count} 只")
        if self.fail_list:
            print(f"失败列表: {self.fail_list[:10]}{'...' if len(self.fail_list) > 10 else ''}")
        print(f"总耗时: {elapsed:.1f} 秒 ({elapsed/60:.1f} 分钟)")
        if total > 0:
            print(f"平均每只: {elapsed/total:.2f} 秒")
        print(f"{'='*60}")
        
        if self.stage_results:
            print(f"\n阶段统计:")
            print(f"{'阶段':<8} {'股票数':<8} {'成功':<8} {'失败':<8} {'耗时(s)':<10}")
            print("-" * 50)
            for r in self.stage_results:
                print(f"{r['stage']:<8} {r['stocks']:<8} {r['success']:<8} {r['fail']:<8} {r['time']:<10.1f}")
        
        if self.fail_list:
            fail_df = pd.DataFrame({'失败股票': self.fail_list})
            fail_path = r'{}/data/全部因子数据/失败列表.xlsx'.format(self.path)
            fail_df.to_excel(fail_path, index=False)
            print(f"\n失败列表已保存至: {fail_path}")
    
    def cacal_all_stock_factor(self):
        """计算所有股票因子"""
        if not self.text:
            print("因子表为空，请检查因子表.json")
            return
        
        if self.use_multiprocess and self.max_workers > 1:
            self.cacal_all_stock_factor_multiprocess()
        else:
            self.cacal_all_stock_factor_single()
    
    def get_factor_data(self, stock='513100.SH'):
        """获取已计算的因子数据"""
        try:
            file_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
            if not os.path.exists(file_path):
                return pd.DataFrame()
            return pd.read_parquet(file_path, engine='pyarrow', use_threads=True)
        except:
            return pd.DataFrame()
    
    def get_all_factor_data(self):
        """获取所有已计算的因子数据"""
        data_path = r'{}/data/全部因子数据'.format(self.path)
        if not os.path.exists(data_path):
            return pd.DataFrame()
        
        all_data = []
        for file in os.listdir(data_path):
            if file.endswith('.parquet') and file != '失败列表.xlsx':
                try:
                    stock = file.replace('.parquet', '')
                    df = self.get_factor_data(stock)
                    if not df.empty:
                        df['stock'] = stock
                        all_data.append(df)
                except:
                    continue
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()
    
    def run_all_func(self):
        """运行完整流程"""
        print("="*60)
        print("小果因子计算系统 (超级优化版)")
        print("="*60)
        
        print("\n[1/2] 生成因子列表...")
        self.get_all_factor_table()
        
        print("\n[2/2] 计算所有股票因子...")
        self.cacal_all_stock_factor()
        
        print("\n全部完成!")
        #下载一个因子的例子
        df=self.get_factor_data('513100.SH')[-10:]
        df['date']=pd.to_datetime(df['date'])
        df['date']=df['date'].apply(lambda x:str(x)[:10])
        df.to_json(r'{}/data/因子例子参考/因子例子参考.json'.format(self.path),orient='records',force_ascii=False)
        df.to_excel(r'{}/data/因子例子参考/因子例子参考.xlsx'.format(self.path))

if __name__ == '__main__':
    # ========== 强制重新计算所有股票（覆盖最新） ==========
    api = xg_factor_trader(
        max_workers=4,          # 进程数
        verbose=False,          # 是否显示详细信息
        use_multiprocess=True,  # 多进程模式
        chunk_size=100,         # 每批处理100只
        stage_size=100,         # 每阶段处理100只后清理缓存
        use_async_io=True,      # 使用异步IO
        start_date='20240101',
        force_recalc=True       # 🔥 强制重算模式：覆盖计算全部股票
    )
    api.run_all_func()
   
    df=api.get_factor_data('513100.SH')[-10:]
    df['date']=pd.to_datetime(df['date'])
    df['date']=df['date'].apply(lambda x:str(x)[:10])
    df.to_json(r'data/因子例子参考/因子例子参考.json',orient='records',force_ascii=False)
    df.to_excel(r'data/因子例子参考/因子例子参考.xlsx')
    


    
    
# 全部因子表
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
# 因子的数据参考
[{"date":"2026-08-12","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.211,"high":2.231,"low":2.203,"close":2.226,"volume":1365827,"amount":303278765.0,"5日涨跌幅":-1.8085575651,"10日涨跌幅":7.3288331726,"20日涨跌幅":1.7367458867,"30日涨跌幅":0.769578995,"60日涨跌幅":8.7445041524,"120日涨跌幅":20.715835141,"六脉神剑":3,"小波段交易":true,"大波段交易":true,"波段超级买卖":false,"价格距离5日均线涨跌幅":-0.7313592579,"价格距离10日均线涨跌幅":1.4076807435,"价格距离20日均线涨跌幅":3.3522146903,"价格距离30日均线涨跌幅":3.1383208748,"价格距离60日均线涨跌幅":1.9285218227,"价格距离120日均线涨跌幅":10.3117902127,"5日均线距离10日均线涨跌幅":2.1547993258,"10日均线距离20日均线涨跌幅":1.9175410902,"20日均线距离30日均线涨跌幅":-0.2069561994,"30日均线距离60日均线涨跌幅":-1.1729869575,"60日均线距离120日均线涨跌幅":8.22465414,"5日偏度":-0.2130310453,"10日偏度":-1.0221057336,"20日偏度":0.3810247202,"30日偏度":0.2017338127,"60日偏度":0.2998040577,"120日偏度":-0.2485685917,"5日峰度":-2.2484308094,"10日峰度":0.037361987,"20日峰度":-1.1104291952,"30日峰度":-0.2884371674,"60日峰度":-0.0182365693,"120日峰度":-1.3905473607,"KDJ_KD金叉":false,"KDJ_KD死叉":true,"RSI_金叉":true,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.2424,"10日均线":2.1951,"20日均线":2.1538,"30日均线":2.1582666667,"60日均线":2.1838833333,"120日均线":2.0179166667,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":1.0,"连续下跌天数":0.0,"价格在5均线上":false,"价格在10均线上":true,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":true,"10均线在20均线上":true,"20均线在30均线上":false,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":-0.7870401156,"10日Alpha":1.5279211226,"20日Alpha":0.558122868,"30日Alpha":0.4721503394,"60日Alpha":0.6217769524,"120日Alpha":0.534733555,"5日Beta":1.783108246,"10日Beta":1.8058127872,"20日Beta":0.8406653199,"30日Beta":0.6747796035,"60日Beta":0.7477430717,"120日Beta":0.8656100515,"5日夏普比率":-4.7339151452,"10日夏普比率":5.6783911399,"20日夏普比率":0.8943193136,"30日夏普比率":0.3785819377,"60日夏普比率":1.2913231069,"120日夏普比率":1.5466301384,"5日年化波动率":0.1908613939,"10日年化波动率":0.3231912345,"20日年化波动率":0.2858363993,"30日年化波动率":0.2488261973,"60日年化波动率":0.3090598995,"120日年化波动率":0.2809662064,"5日最大回撤":-0.0229378033,"10日最大回撤":-0.0229378033,"20日最大回撤":-0.0671846435,"30日最大回撤":-0.0760525124,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":0.6096493156,"10日上涨捕获率":14.2486836524,"20日上涨捕获率":1.4592948064,"30日上涨捕获率":0.6775266829,"60日上涨捕获率":0.4881101519,"120日上涨捕获率":0.814182379,"5日下跌捕获率":1.3929087211,"10日下跌捕获率":1.0750162743,"20日下跌捕获率":0.980760663,"30日下跌捕获率":0.9172752098,"60日下跌捕获率":0.8318726995,"120日下跌捕获率":0.8577392569,"3日回归动量":-0.2829123116,"5日回归动量":-0.3208832801,"7日回归动量":0.0029174585,"9日回归动量":0.6046065815,"12日回归动量":4.2175617161,"15日回归动量":2.7437958874,"18日回归动量":1.6029448369,"20日回归动量":0.9929720615,"23日回归动量":0.3310707002,"25日回归动量":0.1741267729,"28日回归动量":0.0816717032,"30日回归动量":0.0501476075,"35日回归动量":0.0034646786,"40日回归动量":-0.000626963,"45日回归动量":-0.0000311048,"50日回归动量":-0.0014016675,"60日回归动量":-0.0046687401,"5日最高值到当前周期":3.0,"10日最高值到当前周期":5.0,"20日最高值到当前周期":5.0,"30日最高值到当前周期":5.0,"60日最高值到当前周期":51.0,"120日最高值到当前周期":51.0,"5日最低值到当前周期":1.0,"10日最低值到当前周期":9.0,"20日最低值到当前周期":9.0,"30日最低值到当前周期":9.0,"60日最低值到当前周期":9.0,"120日最低值到当前周期":91.0,"5日回归斜率":-0.0087,"10日回归斜率":0.0197272727,"20日回归斜率":0.0078481203,"30日回归斜率":0.001796218,"60日回归斜率":-0.0009806891,"120日回归斜率":0.0046584832,"5日标准差":0.0196224361,"10日标准差":0.0731989754,"20日标准差":0.0690967438,"30日标准差":0.0571436397,"60日标准差":0.0678920937,"120日标准差":0.1926236219,"CCI商品路径指标":50.8311461067,"MFI最近流量指标":54.5403536554,"MTM动量线_MTM值":0.108,"MTM动量线_MTMMA值":0.1283333333,"RSI相对强弱_RSI1":58.3435226351,"RSI相对强弱_RSI2":57.5115630898,"RSI相对强弱_RSI3":55.3318713166,"KDJ指标_K值":75.4933875058,"KDJ指标_D值":76.8569515941,"KDJ指标_J值":72.7662593292,"SKDJ慢速随机_K值":78.4629088913,"SKDJ慢速随机_D值":84.0344680332,"UDL引力线_UDL值":2.206325,"UDL引力线_MAUDL值":2.18949375,"WR威廉指标_WR1":25.6809338521,"WR威廉指标_WR2":74.1573033708,"LWR指标_LWR1":24.5066124942,"LWR指标_LWR2":23.1430484059,"MARSI相对强弱平均线_RSI1":57.4236832096,"MARSI相对强弱平均线_RSI2":68.6858285517,"BIAS乖离率_BIAS1":-0.9125306032,"BIAS乖离率_BIAS2":2.3722837543,"BIAS乖离率_BIAS3":3.1829419036,"BIAS_QL乖离率传统版_BIAS值":-0.9125306032,"BIAS_QL乖离率传统版_BIASMA值":2.0499356551,"BIAS36三六乖离_BIAS36":-0.0125,"BIAS36三六乖离_BIAS612":0.0720833333,"BIAS36三六乖离_MABIAS":0.0354722222,"ACCER幅度涨速":0.0043426176,"ASI振动升降指标_ASI":-0.1564894329,"ASI振动升降指标_ASIT":-1.3107365544,"CHO佳庆指标_CHO":4184.5905204515,"CHO佳庆指标_MACHO":1142.7974403891,"DMA_XT平均差_DIF":0.01726,"DMA_XT平均差_DIFMA":-0.045046,"DMI趋向指标_PDI":-31.8104906937,"DMI趋向指标_MDI":28.5956006768,"DMI趋向指标_ADX":-7084.5467836264,"DMI趋向指标_ADXR":-5875.387454643,"DPO区间震荡线_DPO":0.1214285714,"DPO区间震荡线_MADPO":0.1459761905,"EMV简易波动指标_EMV":-0.1190448216,"EMV简易波动指标_MAEMV":-0.141039147,"MACD平滑异同平均线_DIF":0.0225298257,"MACD平滑异同平均线_DEA":0.0081187101,"MACD平滑异同平均线_MACD":0.0288222311,"VMACD量平滑异同平均线_DIF":-308785.7393637362,"VMACD量平滑异同平均线_DEA":-406459.89052896,"VMACD量平滑异同平均线_MACD":97674.1511652238,"SMACD单线平滑异同平均线_DEA":0.0081187101,"SMACD单线平滑异同平均线_MACD":0.0225298257,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.1097065676,"TRIX三重指数平均线_MATRIX":-0.0640896938,"UOS终极指标_UOS":60.7766999834,"UOS终极指标_MAUOS":61.5877280418,"VTP量价曲线_VPT":-354677.7628514307,"VTP量价曲线_MAVP":10498.5363889925,"WVAD威廉变异离散量_WVAD":-17.3425361354,"WVAD威廉变异离散量_MAWVAD":31.2808161602,"JS加数线_JS":-0.361711513,"JS加数线_MAJS1":0.9111374804,"JS加数线_MAJS2":0.6932409207,"JS加数线_MAJS3":0.1751721031,"CYE市场趋势_CYEL":-0.3643472852,"CYE市场趋势_CYES":0.1613286769,"GDX轨道线_轨道":0.0340470664,"GDX轨道线_压力线":0.0371113024,"GDX轨道线_支撑线":0.0309828304,"JLHB绝路航标_B":26.8744484067,"JLHB绝路航标_VAR2":25.3118455162,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":118.202764977,"BRAR情绪指标_AR":87.8048780488,"CR带状能量线_CR":104.5501551189,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":23.1002855604,"MASS梅斯线_MAMASS":22.3410970655,"PSY心理线_PSY":58.3333333333,"PSY心理线_PSYMA":61.1111111111,"VR成交量变异率_VR":132.8159126535,"VR成交量变异率_MAVR":139.7487445795,"WAD威廉多空力度线_WAD":0.905,"WAD威廉多空力度线_MAWAD":0.8299,"PCNT幅度比_PCNT":0.4941599281,"PCNT幅度比_MAPCNT":-0.033835521,"CYR市场强弱_CYR":0.1058513323,"CYR市场强弱_MACYR":0.4417613438,"AMO成交金额_AMOW":30327.8765,"AMO成交金额_AMO1":40886.68482,"AMO成交金额_AMO2":37401.33608,"OBV累积能量线_OBV":235539263,"OBV累积能量线_MAOBV":231874215.1999999881,"VOL成交量_MAVOL1":1821840.2,"VOL成交量_MAVOL2":1695639.6000000001,"VRSI相对强弱量_RSI1":38.7734190153,"VRSI相对强弱量_RSI2":43.4941115267,"VRSI相对强弱量_RSI3":45.4245755267,"HSL换手线_HSL":1365827,"HSL换手线_MAHSL":1821840.2,"MA均线_MA1":2.2424,"MA均线_MA2":2.1951,"MA均线_MA3":2.1538,"MA均线_MA4":2.1838833333,"ACD升降线_ACD":0.905,"ACD升降线_MAACD":0.8589231862,"BBI多空均线":2.2030625,"EXPMA指数平均线_EXP1":2.1982271655,"EXPMA指数平均线_EXP2":2.1523850555,"HMA高价平均线_HMA1":2.2593333333,"HMA高价平均线_HMA2":2.186,"HMA高价平均线_HMA3":2.1705333333,"HMA高价平均线_HMA4":2.1905714286,"HMA高价平均线_HMA5":2.1198333333,"LMA低价平均线_LMA1":2.2328333333,"LMA低价平均线_LMA2":2.1615,"LMA低价平均线_LMA3":2.1459666667,"LMA低价平均线_LMA4":2.1456571429,"LMA低价平均线_LMA5":2.0800444444,"VMA变异平均线_VMA1":2.246,"VMA变异平均线_VMA2":2.1738958333,"VMA变异平均线_VMA3":2.1585583333,"VMA变异平均线_VMA4":2.1692678571,"VMA变异平均线_VMA5":2.1009166667,"AMV成本均线_AMV1":2.2440883738,"AMV成本均线_AMV2":2.1837928567,"AMV成本均线_AMV3":2.1689018028,"AMV成本均线_AMV4":2.198343106,"BBIBOLL多空布林线_BBIBOLL":2.2030625,"BBIBOLL多空布林线_UPR":2.4467707646,"BBIBOLL多空布林线_DWN":1.9593542354,"ALLIGAT鳄鱼线_上唇":2.2115,"ALLIGAT鳄鱼线_牙齿":2.1225625,"ALLIGAT鳄鱼线_下颚":2.1148461538,"GMMA顾比均线_MA3":2.2301331171,"GMMA顾比均线_MA5":2.2273638288,"GMMA顾比均线_MA8":2.2141079277,"GMMA顾比均线_MA10":2.2054433994,"GMMA顾比均线_MA12":2.1982271655,"GMMA顾比均线_MA15":2.1900973264,"GMMA顾比均线_MA30":2.172434441,"GMMA顾比均线_MA35":2.1682181759,"GMMA顾比均线_MA40":2.1634912218,"GMMA顾比均线_MA45":2.1581869323,"GMMA顾比均线_MA50":2.1523850555,"GMMA顾比均线_MA60":2.1397852552,"BOLL布林线_BOLL":2.1538,"BOLL布林线_UB":2.2919934875,"BOLL布林线_LB":2.0156065125,"PBX瀑布线_PBX1":2.2052431354,"PBX瀑布线_PBX2":2.1850374613,"PBX瀑布线_PBX3":2.176316841,"PBX瀑布线_PBX4":2.1789455636,"PBX瀑布线_PBX5":2.1701341214,"PBX瀑布线_PBX6":2.142380694,"ENE轨道线_UPPER":2.2871408,"ENE轨道线_LOWER":2.0282192,"ENE轨道线_ENE":2.15768,"MIKE麦克支撑压力_STOR":2.5234972816,"MIKE麦克支撑压力_MIDR":2.4089822865,"MIKE麦克支撑压力_WEKR":2.2944672915,"MIKE麦克支撑压力_WEKS":2.0503201079,"MIKE麦克支撑压力_MIDS":1.9206879194,"MIKE麦克支撑压力_STOS":1.791055731,"XS薛斯通道_SUP":2.3092492824,"XS薛斯通道_SDN":2.0478248353,"XS薛斯通道_LUP":2.4987324277,"XS薛斯通道_LDN":1.8850086735,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1011462526,"MA交易_MA1":2.2424,"MA交易_MA2":2.1538,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0225298257,"MACD交易_DEA":0.0081187101,"MACD交易_MACD":0.0288222311,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":75.4933875058,"KDJ交易_D":76.8569515941,"KDJ交易_J":72.7662593292,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4745341848,"SG_XDT心电图_MQR1":0.4790940767,"SG_XDT心电图_MQR2":0.4735654119,"SG_NDB脑电波_DK":3.236,"SG_NDB脑电波_MDK1":3.2702,"SG_NDB脑电波_MDK2":3.2186,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":25.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":20265.0003337464,"LON龙系长线_LONMA":18712.9743401545,"LON龙系长线_LONT":20265.0003337464,"SHT龙系短线_SHT":2.9059964489,"SHT龙系短线_SHTMA":4.6752333608,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":62.6621367061,"ZLMM主力买卖_MMM":60.8500027654,"ZLMM主力买卖_MML":52.1947107395,"SLZT神龙在天_白龙":2.010776,"SLZT神龙在天_黄龙":2.3527495292,"SLZT神龙在天_紫龙":1.6446841664,"SLZT神龙在天_青龙":2.0451772,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":29849.315222474,"ADVOL龙系离散量_MA1":29611.0830611894,"ADVOL龙系离散量_MA2":28391.3848606991,"CYS市场盈亏":1.1058971362,"CYW主力控盘":324.6395665901,"JAX济安线_J":null,"JAX济安线_A":2.2300305232,"JAX济安线_X":null,"XJDX超级短线_J":0.5024481383,"XJDX超级短线_D":0.7494571209,"XJDX超级短线_K":0.5024481383,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":4.0134009598,"BDZX波段之星_AK":97.1324341257,"BDZX波段之星_AD1":99.4382488111,"BDZX波段之星_AJ":92.520804755,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":58,"LHXJ猎狐先觉_主力弃盘":-0.062165747,"LHXJ猎狐先觉_主力控盘":0.062165747,"LYJH猎鹰歼狐_机构做空能量线":26.1647773602,"LYJH猎鹰歼狐_机构做多能量线":64.3326110395,"JFZX飓风智能中线_多头力量":55.480316838,"JFZX飓风智能中线_空头力量":44.519683162,"CYHT财运亨通_SK":56.1309112953,"CYHT财运亨通_SD":52.2088301912,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":2.226,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":null,"CDP_STD逆势操作_CDP":2.224,"CDP_STD逆势操作_AH":2.269,"CDP_STD逆势操作_NH":2.236,"CDP_STD逆势操作_NL":2.203,"CDP_STD逆势操作_AL":2.17,"Alpha001":0.0731309203,"Alpha002":-1.461038961,"Alpha003":-21.998,"Alpha004":-1,"Alpha005":-0.8607533668,"Alpha006":-0.2064364207,"Alpha007":0.6901065046,"Alpha008":-0.2590266876,"Alpha009":-0.0000000001,"Alpha010":0.965210356,"Alpha011":1884595.2703823685,"Alpha012":-0.0488951204,"Alpha013":-219.8307596178,"Alpha014":-0.041,"Alpha015":-0.0018058691,"Alpha016":-0.9921507064,"Alpha017":1.0549686726,"Alpha018":0.9819144243,"Alpha019":-0.0180855757,"Alpha020":1.5510948905,"Alpha021":0.0286285714,"Alpha022":-0.0027697855,"Alpha023":53.7118280567,"Alpha024":0.0589143403,"Alpha025":-1.6992024455,"Alpha026":0.9375550996,"Alpha027":507.2355475392,"Alpha028":70.8334217389,"Alpha029":21185.2728102187,"Alpha030":0.0003506157,"Alpha031":2.3722837543,"Alpha032":-2.082942097,"Alpha033":-0.029249298,"Alpha034":0.9768268943,"Alpha035":-0.8162939297,"Alpha036":0.9327073552,"Alpha037":-0.0750026688,"Alpha038":0.061,"Alpha039":-0.2605304212,"Alpha040":123.1919629475,"Alpha041":-0.9544025157,"Alpha042":-0.754936306,"Alpha043":-140170.0,"Alpha044":1.6666666667,"Alpha045":0.0753502839,"Alpha046":0.9896956424,"Alpha047":42.0463136061,"Alpha048":-0.0680222064,"Alpha049":0.3755555556,"Alpha050":0.2488888889,"Alpha051":0.6244444444,"Alpha052":110.0651701665,"Alpha053":58.3333333333,"Alpha054":-0.9825949367,"Alpha055":0.1918481656,"Alpha056":-0.4636752137,"Alpha057":72.7765373248,"Alpha058":50.0,"Alpha059":0.036,"Alpha060":-245708.4587304331,"Alpha061":-0.8658346334,"Alpha062":-0.6832722298,"Alpha063":58.3435226351,"Alpha064":-0.8627145086,"Alpha065":1.0092093441,"Alpha066":-0.9125306032,"Alpha067":55.3318713166,"Alpha068":-0.0,"Alpha069":-0.6463022508,"Alpha070":67322444.0968458652,"Alpha071":3.1829419036,"Alpha072":45.9911184756,"Alpha073":-0.3097472421,"Alpha074":1.0031201248,"Alpha075":0.375,"Alpha076":0.801239871,"Alpha077":0.0608424337,"Alpha078":41.8579683602,"Alpha079":57.5115630898,"Alpha080":-39.4149206328,"Alpha081":1910662.3912005352,"Alpha082":47.2058734352,"Alpha083":-0.5337519623,"Alpha084":835886.0,"Alpha085":0.4125,"Alpha086":-0.011,"Alpha087":-1.5059059505,"Alpha088":1.7367458867,"Alpha089":0.0288222311,"Alpha090":-0.8658346334,"Alpha091":-0.1290880643,"Alpha092":-0.8666666667,"Alpha093":0.16,"Alpha094":6784490.0,"Alpha095":116367020.5474933237,"Alpha096":73.7480951178,"Alpha097":405378.522116738,"Alpha098":0.04,"Alpha099":-0.5400313972,"Alpha100":526926.7677797917,"Alpha101":-0.848673947,"Alpha102":38.7734190153,"Alpha103":55.0,"Alpha104":0.1924425457,"Alpha105":-0.8007247395,"Alpha106":0.038,"Alpha107":-0.0085941086,"Alpha108":-0.0120796215,"Alpha109":1.103573236,"Alpha110":119.6675900277,"Alpha111":165542.2933471237,"Alpha112":25.5924170616,"Alpha113":0.2531535895,"Alpha114":342.3359736886,"Alpha115":0.0419277531,"Alpha116":0.0062195489,"Alpha117":0.009765625,"Alpha118":102.510460251,"Alpha119":-0.1419656786,"Alpha120":0.9801492565,"Alpha121":-0.9703880123,"Alpha122":0.0013985943,"Alpha123":-0.6747322794,"Alpha124":-80.4256390297,"Alpha125":0.5804311774,"Alpha126":2.22,"Alpha127":3.1421106912,"Alpha128":54.5403536554,"Alpha129":0.157,"Alpha130":0.1258064516,"Alpha131":0.9349481331,"Alpha132":380859522.4499999881,"Alpha133":35.0,"Alpha134":69645.5694050992,"Alpha135":1.0043193694,"Alpha136":-0.3067593261,"Alpha137":-0.016,"Alpha138":-0.7775796746,"Alpha139":-0.7975742477,"Alpha140":0.3333333333,"Alpha141":-0.0953150242,"Alpha142":-0.0486700105,"Alpha143":0.00496614,"Alpha144":0.0,"Alpha145":-7.7384988214,"Alpha146":0.2080342686,"Alpha147":0.0028627622,"Alpha148":-0.2664384942,"Alpha149":0.8150987734,"Alpha150":3032135.9400000004,"Alpha151":0.0064054733,"Alpha152":-0.0060930527,"Alpha153":2.2030625,"Alpha154":-18.6726363898,"Alpha155":97674.1511652238,"Alpha156":-0.8736349454,"Alpha157":0.4023622047,"Alpha158":0.0125786164,"Alpha159":-4540.8269061622,"Alpha160":0.0243987487,"Alpha161":0.04475,"Alpha162":0.7271251064,"Alpha163":0.3088923557,"Alpha164":193576.0131370541,"Alpha165":-23.1229760457,"Alpha166":-0.0018869312,"Alpha167":0.265,"Alpha168":-0.774653551,"Alpha169":-0.0001182342,"Alpha170":-0.1394672068,"Alpha171":-4.4470882164,"Alpha172":31.5577478963,"Alpha173":3.0341860347,"Alpha174":0.0283117984,"Alpha175":0.0423333333,"Alpha176":0.7518667051,"Alpha177":90.0,"Alpha178":6782.8880361171,"Alpha179":0.0708891382,"Alpha180":-1365827.0,"Alpha181":0.004963636,"Alpha182":0.65,"Alpha183":16.485603634,"Alpha184":0.4547581903,"Alpha185":-0.000045408,"Alpha186":29.0179953215,"Alpha187":0.344,"Alpha188":6.336464265,"Alpha189":0.0595833333,"Alpha190":-0.5421235052,"Alpha191":0.829023019},{"date":"2026-08-13","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.235,"high":2.244,"low":2.224,"close":2.226,"volume":1300873,"amount":290744504.0,"5日涨跌幅":-0.8021390374,"10日涨跌幅":9.0641842234,"20日涨跌幅":2.7226580526,"30日涨跌幅":3.1510658017,"60日涨跌幅":8.1632653061,"120日涨跌幅":20.9125475285,"六脉神剑":2,"小波段交易":true,"大波段交易":true,"波段超级买卖":false,"价格距离5日均线涨跌幅":-0.571734858,"价格距离10日均线涨跌幅":0.5601734731,"价格距离20日均线涨跌幅":3.2108496581,"价格距离30日均线涨跌幅":3.0301160207,"价格距离60日均线涨跌幅":1.7980045884,"价格距离120日均线涨跌幅":10.1366813037,"5日均线距离10日均线涨跌幅":1.1384170582,"10日均线距离20日均线涨跌幅":2.6359105135,"20日均线距离30日均线涨跌幅":-0.1751110837,"30日均线距离60日均线涨跌幅":-1.1958750314,"60日均线距离120日均线涨跌幅":8.1913950564,"5日偏度":0.4550308081,"10日偏度":-1.0550917172,"20日偏度":0.2752640693,"30日偏度":0.1208218411,"60日偏度":0.3172445872,"120日偏度":-0.2811011908,"5日峰度":-2.8497713639,"10日峰度":0.0191304268,"20日峰度":-1.3386854093,"30日峰度":-0.507039159,"60日峰度":0.0353602538,"120日峰度":-1.3755166262,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.2388,"10日均线":2.2136,"20日均线":2.15675,"30日均线":2.1605333333,"60日均线":2.1866833333,"120日均线":2.021125,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":0.0,"连续下跌天数":1.0,"价格在5均线上":false,"价格在10均线上":true,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":true,"10均线在20均线上":true,"20均线在30均线上":false,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":-0.4389750473,"10日Alpha":2.1275971094,"20日Alpha":0.5382414897,"30日Alpha":0.5536264627,"60日Alpha":0.6120045835,"120日Alpha":0.5498733745,"5日Beta":1.3003590165,"10日Beta":1.7250747573,"20日Beta":0.8535067606,"30日Beta":0.6538173741,"60日Beta":0.7468204626,"120日Beta":0.8645441842,"5日夏普比率":-2.1514317608,"10日夏普比率":7.4470382537,"20日夏普比率":1.3300051616,"30日夏普比率":1.2070948145,"60日夏普比率":1.2186326304,"120日夏普比率":1.5589630511,"5日年化波动率":0.1822902694,"10日年化波动率":0.3002764973,"20日年化波动率":0.2831277514,"30日年化波动率":0.2387012248,"60日年化波动率":0.3089746378,"120日年化波动率":0.2809350024,"5日最大回撤":-0.0225066196,"10日最大回撤":-0.0229378033,"20日最大回撤":-0.0581449008,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":0.6096493156,"10日上涨捕获率":14.2486836524,"20日上涨捕获率":1.4592948064,"30日上涨捕获率":0.6775266829,"60日上涨捕获率":0.4881101519,"120日上涨捕获率":0.814182379,"5日下跌捕获率":1.118306755,"10日下跌捕获率":0.9731358637,"20日下跌捕获率":0.9773785799,"30日下跌捕获率":0.8794158145,"60日下跌捕获率":0.8395662517,"120日下跌捕获率":0.8551653234,"3日回归动量":0.4139271413,"5日回归动量":-0.355756323,"7日回归动量":-0.3271204901,"9日回归动量":0.026086817,"12日回归动量":1.9256288042,"15日回归动量":2.4727392269,"18日回归动量":1.4899941576,"20日回归动量":1.2761095447,"23日回归动量":0.4757373874,"25日回归动量":0.2640678919,"28日回归动量":0.1366002553,"30日回归动量":0.0825288244,"35日回归动量":0.0161305822,"40日回归动量":-0.0014602598,"45日回归动量":-0.0000822071,"50日回归动量":-0.0000171153,"60日回归动量":-0.0051988804,"5日最高值到当前周期":4.0,"10日最高值到当前周期":6.0,"20日最高值到当前周期":6.0,"30日最高值到当前周期":6.0,"60日最高值到当前周期":52.0,"120日最高值到当前周期":52.0,"5日最低值到当前周期":2.0,"10日最低值到当前周期":9.0,"20日最低值到当前周期":10.0,"30日最低值到当前周期":10.0,"60日最低值到当前周期":10.0,"120日最低值到当前周期":92.0,"5日回归斜率":-0.0115,"10日回归斜率":0.0111393939,"20日回归斜率":0.0090879699,"30日回归斜率":0.0022313682,"60日回归斜率":-0.0011250069,"120日回归斜率":0.0046701333,"5日标准差":0.0206242576,"10日标准差":0.0523129047,"20日标准差":0.0708349314,"30日标准差":0.0584224462,"60日标准差":0.0660829004,"120日标准差":0.192856318,"CCI商品路径指标":53.5239361702,"MFI最近流量指标":60.6033097928,"MTM动量线_MTM值":0.158,"MTM动量线_MTMMA值":0.1261666667,"RSI相对强弱_RSI1":58.3435226351,"RSI相对强弱_RSI2":57.5115630898,"RSI相对强弱_RSI3":55.3318713166,"KDJ指标_K值":71.2328798061,"KDJ指标_D值":74.9822609981,"KDJ指标_J值":63.7341174222,"SKDJ慢速随机_K值":72.9824846706,"SKDJ慢速随机_D值":78.6929849506,"UDL引力线_UDL值":2.2078708333,"UDL引力线_MAUDL值":2.1990125,"WR威廉指标_WR1":35.6756756757,"WR威廉指标_WR2":74.1573033708,"LWR指标_LWR1":28.7671201939,"LWR指标_LWR2":25.0177390019,"MARSI相对强弱平均线_RSI1":60.2954748267,"MARSI相对强弱平均线_RSI2":65.1375143934,"BIAS乖离率_BIAS1":-0.6102098527,"BIAS乖离率_BIAS2":1.7561235762,"BIAS乖离率_BIAS3":3.0794165316,"BIAS_QL乖离率传统版_BIAS值":-0.6102098527,"BIAS_QL乖离率传统版_BIASMA值":0.9219326004,"BIAS36三六乖离_BIAS36":-0.0173333333,"BIAS36三六乖离_BIAS612":0.0520833333,"BIAS36三六乖离_MABIAS":0.0226111111,"ACCER幅度涨速":-0.000315535,"ASI振动升降指标_ASI":0.4330859861,"ASI振动升降指标_ASIT":-0.7944306307,"CHO佳庆指标_CHO":5608.5271257344,"CHO佳庆指标_MACHO":2349.5061564782,"DMA_XT平均差_DIF":0.03722,"DMA_XT平均差_DIFMA":-0.033184,"DMI趋向指标_PDI":-26.0869565217,"DMI趋向指标_MDI":24.6956521739,"DMI趋向指标_ADX":-2009.5467836258,"DMI趋向指标_ADXR":-6274.446594428,"DPO区间震荡线_DPO":0.1001428571,"DPO区间震荡线_MADPO":0.1366666667,"EMV简易波动指标_EMV":0.0446939319,"EMV简易波动指标_MAEMV":-0.0723024412,"MACD平滑异同平均线_DIF":0.0230764465,"MACD平滑异同平均线_DEA":0.0111102574,"MACD平滑异同平均线_MACD":0.0239323781,"VMACD量平滑异同平均线_DIF":-322623.6138674989,"VMACD量平滑异同平均线_DEA":-389692.6351966679,"VMACD量平滑异同平均线_MACD":67069.0213291689,"SMACD单线平滑异同平均线_DEA":0.0111102574,"SMACD单线平滑异同平均线_MACD":0.0230764465,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.1365059069,"TRIX三重指数平均线_MATRIX":-0.0273071856,"UOS终极指标_UOS":53.6406606806,"UOS终极指标_MAUOS":59.3171373672,"VTP量价曲线_VPT":-299849.7349444533,"VTP量价曲线_MAVP":-54535.5941092949,"WVAD威廉变异离散量_WVAD":-4.2353822465,"WVAD威廉变异离散量_MAWVAD":3.757906014,"JS加数线_JS":-0.1604278075,"JS加数线_MAJS1":0.4812077249,"JS加数线_MAJS2":0.7616655261,"JS加数线_MAJS3":0.1666890322,"CYE市场趋势_CYEL":-0.1605422761,"CYE市场趋势_CYES":0.1522240067,"GDX轨道线_轨道":0.0330998107,"GDX轨道线_压力线":0.0360787936,"GDX轨道线_支撑线":0.0301208277,"JLHB绝路航标_B":27.0626531942,"JLHB绝路航标_VAR2":25.6620070518,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":130.4668304668,"BRAR情绪指标_AR":92.4528301887,"CR带状能量线_CR":116.2663755459,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":23.5482694759,"MASS梅斯线_MAMASS":22.6390188652,"PSY心理线_PSY":58.3333333333,"PSY心理线_PSYMA":59.7222222222,"VR成交量变异率_VR":144.5320532972,"VR成交量变异率_MAVR":137.3852135931,"WAD威廉多空力度线_WAD":0.905,"WAD威廉多空力度线_MAWAD":0.8339666667,"PCNT幅度比_PCNT":0.0,"PCNT幅度比_MAPCNT":-0.022557014,"CYR市场强弱_CYR":0.1650252221,"CYR市场强弱_MACYR":0.3531028554,"AMO成交金额_AMOW":29074.4504,"AMO成交金额_AMO1":38158.33432,"AMO成交金额_AMO2":38074.69067,"OBV累积能量线_OBV":235539263,"OBV累积能量线_MAOBV":232214360.5333333313,"VOL成交量_MAVOL1":1700507.3999999999,"VOL成交量_MAVOL2":1716237.3,"VRSI相对强弱量_RSI1":37.36095685,"VRSI相对强弱量_RSI2":42.9114581864,"VRSI相对强弱量_RSI3":45.1995950329,"HSL换手线_HSL":1300873,"HSL换手线_MAHSL":1700507.3999999999,"MA均线_MA1":2.2388,"MA均线_MA2":2.2136,"MA均线_MA3":2.15675,"MA均线_MA4":2.1866833333,"ACD升降线_ACD":0.905,"ACD升降线_MAACD":0.8633114542,"BBI多空均线":2.2022708333,"EXPMA指数平均线_EXP1":2.2024999093,"EXPMA指数平均线_EXP2":2.155271916,"HMA高价平均线_HMA1":2.2553333333,"HMA高价平均线_HMA2":2.1983333333,"HMA高价平均线_HMA3":2.1721333333,"HMA高价平均线_HMA4":2.1936428571,"HMA高价平均线_HMA5":2.1253777778,"LMA低价平均线_LMA1":2.2285,"LMA低价平均线_LMA2":2.1751666667,"LMA低价平均线_LMA3":2.1482666667,"LMA低价平均线_LMA4":2.1488142857,"LMA低价平均线_LMA5":2.0857222222,"VMA变异平均线_VMA1":2.2412083333,"VMA变异平均线_VMA2":2.1867083333,"VMA变异平均线_VMA3":2.16045,"VMA变异平均线_VMA4":2.1723642857,"VMA变异平均线_VMA5":2.1064861111,"AMV成本均线_AMV1":2.242141378,"AMV成本均线_AMV2":2.1917365799,"AMV成本均线_AMV3":2.1694777534,"AMV成本均线_AMV4":2.2024882768,"BBIBOLL多空布林线_BBIBOLL":2.2022708333,"BBIBOLL多空布林线_UPR":2.4509142898,"BBIBOLL多空布林线_DWN":1.9536273769,"ALLIGAT鳄鱼线_上唇":2.242,"ALLIGAT鳄鱼线_牙齿":2.1384375,"ALLIGAT鳄鱼线_下颚":2.1101923077,"GMMA顾比均线_MA3":2.2280665586,"GMMA顾比均线_MA5":2.2269092192,"GMMA顾比均线_MA8":2.2167506105,"GMMA顾比均线_MA10":2.2091809631,"GMMA顾比均线_MA12":2.2024999093,"GMMA顾比均线_MA15":2.1945851606,"GMMA顾比均线_MA30":2.1758902835,"GMMA顾比均线_MA35":2.1714282772,"GMMA顾比均线_MA40":2.1665404305,"GMMA顾比均线_MA45":2.1611353265,"GMMA顾比均线_MA50":2.155271916,"GMMA顾比均线_MA60":2.1426119682,"BOLL布林线_BOLL":2.15675,"BOLL布林线_UB":2.2984198627,"BOLL布林线_LB":2.0150801373,"PBX瀑布线_PBX1":2.2108375479,"PBX瀑布线_PBX2":2.1903997739,"PBX瀑布线_PBX3":2.1801775469,"PBX瀑布线_PBX4":2.1806117652,"PBX瀑布线_PBX5":2.1731745843,"PBX瀑布线_PBX6":2.145529683,"ENE轨道线_UPPER":2.2896848,"ENE轨道线_LOWER":2.0304752,"ENE轨道线_ENE":2.16008,"MIKE麦克支撑压力_STOR":2.516201752,"MIKE麦克支撑压力_MIDR":2.4110469916,"MIKE麦克支撑压力_WEKR":2.3058922313,"MIKE麦克支撑压力_WEKS":2.0743461245,"MIKE麦克支撑压力_MIDS":1.947954778,"MIKE麦克支撑压力_STOS":1.8215634315,"XS薛斯通道_SUP":2.3144356681,"XS薛斯通道_SDN":2.0524240831,"XS薛斯通道_LUP":2.5067212441,"XS薛斯通道_LDN":1.8910353245,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1164145524,"MA交易_MA1":2.2388,"MA交易_MA2":2.15675,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0230764465,"MACD交易_DEA":0.0111102574,"MACD交易_MACD":0.0239323781,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":71.2328798061,"KDJ交易_D":74.9822609981,"KDJ交易_J":63.7341174222,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4772776392,"SG_XDT心电图_MQR1":0.4780606584,"SG_XDT心电图_MQR2":0.4764332724,"SG_NDB脑电波_DK":3.265,"SG_NDB脑电波_MDK1":3.2636,"SG_NDB脑电波_MDK2":3.2378,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":25.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":20014.5204629591,"LON龙系长线_LONMA":18938.7410825607,"LON龙系长线_LONT":20014.5204629591,"SHT龙系短线_SHT":2.8769483951,"SHT龙系短线_SHTMA":4.1301377488,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":59.1886819679,"ZLMM主力买卖_MMM":60.4808203659,"ZLMM主力买卖_MML":52.4832703927,"SLZT神龙在天_白龙":2.01376,"SLZT神龙在天_黄龙":2.3576397506,"SLZT神龙在天_紫龙":1.6458886633,"SLZT神龙在天_青龙":2.050113656,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":29745.2453824739,"ADVOL龙系离散量_MA1":29627.0235416494,"ADVOL龙系离散量_MA2":28415.2325783114,"CYS市场盈亏":0.9393217962,"CYW主力控盘":264.3655665901,"JAX济安线_J":2.2300079674,"JAX济安线_A":2.219272168,"JAX济安线_X":2.219272168,"XJDX超级短线_J":0.3322758599,"XJDX超级短线_D":0.5289343915,"XJDX超级短线_K":0.3322758599,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":3.4992012239,"BDZX波段之星_AK":91.4904505728,"BDZX波段之星_AD1":94.1397166522,"BDZX波段之星_AJ":86.191918414,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":-0.0491411669,"LHXJ猎狐先觉_主力控盘":0.0491411669,"LYJH猎鹰歼狐_机构做空能量线":25.9228556062,"LYJH猎鹰歼狐_机构做多能量线":62.4084617129,"JFZX飓风智能中线_多头力量":57.5098986083,"JFZX飓风智能中线_空头力量":42.4901013917,"CYHT财运亨通_SK":59.0071513159,"CYHT财运亨通_SD":55.6079907535,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":2.226,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":null,"CDP_STD逆势操作_CDP":2.22,"CDP_STD逆势操作_AH":2.265,"CDP_STD逆势操作_NH":2.237,"CDP_STD逆势操作_NL":2.209,"CDP_STD逆势操作_AL":2.181,"Alpha001":0.3633053436,"Alpha002":1.4428571429,"Alpha003":-21.998,"Alpha004":-1,"Alpha005":-0.8607533668,"Alpha006":-0.2064364207,"Alpha007":0.6782737526,"Alpha008":-0.2700156986,"Alpha009":0.0,"Alpha010":0.965210356,"Alpha011":-1160009.796284352,"Alpha012":-0.0338869251,"Alpha013":-221.2655523125,"Alpha014":-0.018,"Alpha015":0.0040431267,"Alpha016":-0.9921507064,"Alpha017":1.0176661885,"Alpha018":0.9919786096,"Alpha019":-0.0080213904,"Alpha020":-1.8085575651,"Alpha021":0.0231666667,"Alpha022":-0.0043514138,"Alpha023":50.0778661956,"Alpha024":0.0435314723,"Alpha025":-1.4151007226,"Alpha026":0.9426543187,"Alpha027":412.8609937538,"Alpha028":58.3799783181,"Alpha029":-23527.0370533745,"Alpha030":0.0003242894,"Alpha031":1.7561235762,"Alpha032":-2.0672926448,"Alpha033":-0.0157553822,"Alpha034":0.9827418389,"Alpha035":-0.8913738019,"Alpha036":0.9186228482,"Alpha037":-0.3570896467,"Alpha038":0.001,"Alpha039":-0.1934477379,"Alpha040":126.7006570576,"Alpha041":-0.8883647799,"Alpha042":-0.5324592165,"Alpha043":-2394565.0,"Alpha044":1.35,"Alpha045":0.1050547482,"Alpha046":0.989339997,"Alpha047":45.6142013577,"Alpha048":-0.1080406203,"Alpha049":0.2927400468,"Alpha050":0.4145199063,"Alpha051":0.7072599532,"Alpha052":122.3674096849,"Alpha053":58.3333333333,"Alpha054":-0.6772151899,"Alpha055":0.5176304811,"Alpha056":-0.5510545011,"Alpha057":67.1617593465,"Alpha058":50.0,"Alpha059":0.057,"Alpha060":-145023.8587304844,"Alpha061":-0.895475819,"Alpha062":-0.7342119504,"Alpha063":58.3435226351,"Alpha064":-0.8751950078,"Alpha065":1.0061395627,"Alpha066":-0.6102098527,"Alpha067":55.3318713166,"Alpha068":0.0,"Alpha069":-0.7044776119,"Alpha070":71950750.5276385695,"Alpha071":3.0794165316,"Alpha072":47.8688641353,"Alpha073":-0.2152839633,"Alpha074":0.9625585023,"Alpha075":0.36,"Alpha076":0.8560930117,"Alpha077":0.0546021841,"Alpha078":41.4757029091,"Alpha079":57.5115630898,"Alpha080":-31.8035246498,"Alpha081":1852587.2110861987,"Alpha082":48.553444932,"Alpha083":-0.5714285714,"Alpha084":2738191.0,"Alpha085":0.5,"Alpha086":0.0,"Alpha087":-1.0844662358,"Alpha088":2.7226580526,"Alpha089":0.0239323781,"Alpha090":-0.848673947,"Alpha091":-0.1305450402,"Alpha092":-1.0,"Alpha093":0.156,"Alpha094":10204360.0,"Alpha095":117788804.5084904134,"Alpha096":71.5526498607,"Alpha097":375601.8664643688,"Alpha098":0.035,"Alpha099":-0.5604395604,"Alpha100":535656.466355734,"Alpha101":-0.8143525741,"Alpha102":37.36095685,"Alpha103":50.0,"Alpha104":0.0706424227,"Alpha105":-0.5789221771,"Alpha106":0.059,"Alpha107":-0.4527662201,"Alpha108":-0.8392171497,"Alpha109":1.0386237511,"Alpha110":132.7433628319,"Alpha111":458653.2580251503,"Alpha112":42.4731182796,"Alpha113":-0.2092698373,"Alpha114":390.4086223837,"Alpha115":0.2073891623,"Alpha116":0.0078481203,"Alpha117":0.0256347656,"Alpha118":98.7804878049,"Alpha119":0.0436817473,"Alpha120":0.9802769319,"Alpha121":-0.9853858938,"Alpha122":0.0017490829,"Alpha123":-0.6285483597,"Alpha124":-80.9568108937,"Alpha125":0.5595854922,"Alpha126":2.2313333333,"Alpha127":2.7638422305,"Alpha128":60.6033097928,"Alpha129":0.107,"Alpha130":0.0947712418,"Alpha131":0.9850754382,"Alpha132":374737019.5500000119,"Alpha133":35.0,"Alpha134":99389.7166344294,"Alpha135":1.0049717739,"Alpha136":-0.3210578086,"Alpha137":0.067575419,"Alpha138":-0.747938489,"Alpha139":-0.5876834025,"Alpha140":0.3333333333,"Alpha141":-0.2051696284,"Alpha142":-0.0170196989,"Alpha143":0.00496614,"Alpha144":0.0,"Alpha145":-8.9086258321,"Alpha146":-0.2305872982,"Alpha147":0.005083042,"Alpha148":-0.3297549618,"Alpha149":0.8150987734,"Alpha150":2902681.2873333339,"Alpha151":0.0090351997,"Alpha152":-0.0052015605,"Alpha153":2.2022708333,"Alpha154":-20.1482014343,"Alpha155":67069.0213291689,"Alpha156":-0.7784711388,"Alpha157":0.4023622047,"Alpha158":0.008984726,"Alpha159":-5365.5598707726,"Alpha160":0.0268125666,"Alpha161":0.0415833333,"Alpha162":0.7271251064,"Alpha163":0.4836193448,"Alpha164":163795.0880390458,"Alpha165":-20.1211361993,"Alpha166":-0.0021893926,"Alpha167":0.265,"Alpha168":-0.7506159575,"Alpha169":0.0002549298,"Alpha170":-0.3798449707,"Alpha171":-0.1133755294,"Alpha172":33.6249313588,"Alpha173":3.0361073015,"Alpha174":0.0268962085,"Alpha175":0.033,"Alpha176":0.642977617,"Alpha177":85.0,"Alpha178":0.0,"Alpha179":0.0781077733,"Alpha180":-1300873.0,"Alpha181":0.0048940686,"Alpha182":0.65,"Alpha183":16.2094926024,"Alpha184":0.8291731669,"Alpha185":-0.0000163469,"Alpha186":28.9010362572,"Alpha187":0.368,"Alpha188":-20.5729198755,"Alpha189":0.0399444444,"Alpha190":-0.5662877474,"Alpha191":0.6737679224},{"date":"2026-08-14","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.257,"high":2.265,"low":2.247,"close":2.264,"volume":1630904,"amount":368068849.0,"5日涨跌幅":-0.0882612533,"10日涨跌幅":7.196969697,"20日涨跌幅":7.4513526341,"30日涨跌幅":4.4762344255,"60日涨跌幅":7.6557299097,"120日涨跌幅":23.311546841,"六脉神剑":5,"小波段交易":true,"大波段交易":true,"波段超级买卖":true,"价格距离5日均线涨跌幅":1.1436740529,"价格距离10日均线涨跌幅":1.5793251974,"价格距离20日均线涨跌幅":4.5920724383,"价格距离30日均线涨跌幅":4.6323540739,"价格距离60日均线涨跌幅":3.4089005953,"价格距离120日均线涨跌幅":11.8194951495,"5日均线距离10日均线涨跌幅":0.4307250538,"10日均线距离20日均线涨跌幅":2.9659059411,"20日均线距离30日均线涨跌幅":0.0385130867,"30日均线距离60日均线涨跌幅":-1.1692879219,"60日均线距离120日均线涨跌幅":8.1333371748,"5日偏度":0.4289797715,"10日偏度":-1.5192442715,"20日偏度":0.0826642655,"30日偏度":0.1065132939,"60日偏度":0.2571520868,"120日偏度":-0.3108401283,"5日峰度":-2.9208548891,"10日峰度":2.5321315534,"20日峰度":-1.4949460633,"30日峰度":-0.7264116528,"60日峰度":0.003101523,"120日峰度":-1.3572389331,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.2384,"10日均线":2.2288,"20日均线":2.1646,"30日均线":2.1637666667,"60日均线":2.1893666667,"120日均线":2.0246916667,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":true,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":1.0,"连续下跌天数":0.0,"价格在5均线上":true,"价格在10均线上":true,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":true,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":0.5532030963,"10日Alpha":2.0939253348,"20日Alpha":0.8185933051,"30日Alpha":0.7895093848,"60日Alpha":0.5140636591,"120日Alpha":0.6178796074,"5日Beta":1.5345859098,"10日Beta":1.5257997669,"20日Beta":0.8640049279,"30日Beta":0.6589326538,"60日Beta":0.7780421546,"120日Beta":0.86518193,"5日夏普比率":-0.1204940472,"10日夏普比率":6.6530022593,"20日夏普比率":3.535812908,"30日夏普比率":1.6316007502,"60日夏普比率":1.1579373385,"120日夏普比率":1.702036886,"5日年化波动率":0.2151588769,"10日年化波动率":0.2690109019,"20日年化波动率":0.2659996837,"30日年化波动率":0.2430121459,"60日年化波动率":0.3077782728,"120日年化波动率":0.2817328879,"5日最大回撤":-0.0225066196,"10日最大回撤":-0.0229378033,"20日最大回撤":-0.0422336931,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":4.5365869772,"10日上涨捕获率":10.1198827517,"20日上涨捕获率":2.0510815989,"30日上涨捕获率":0.9658668137,"60日上涨捕获率":0.577165377,"120日上涨捕获率":0.8957104814,"5日下跌捕获率":1.118306755,"10日下跌捕获率":0.9731358637,"20日下跌捕获率":0.9737190432,"30日下跌捕获率":0.8794158145,"60日下跌捕获率":0.8829387563,"120日下跌捕获率":0.8551653234,"3日回归动量":10.2021035879,"5日回归动量":0.0713567732,"7日回归动量":-0.0000375883,"9日回归动量":0.0007520887,"12日回归动量":1.2438906666,"15日回归动量":2.4410010516,"18日回归动量":1.8152040651,"20日回归动量":1.4942326198,"23日回归动量":0.7502320002,"25日回归动量":0.4488474297,"28日回归动量":0.242015627,"30日回归动量":0.1537940682,"35日回归动量":0.0378066351,"40日回归动量":0.0044719364,"45日回归动量":-0.0008487979,"50日回归动量":-0.0003433926,"60日回归动量":-0.0033486895,"5日最高值到当前周期":0.0,"10日最高值到当前周期":7.0,"20日最高值到当前周期":7.0,"30日最高值到当前周期":7.0,"60日最高值到当前周期":53.0,"120日最高值到当前周期":53.0,"5日最低值到当前周期":3.0,"10日最低值到当前周期":9.0,"20日最低值到当前周期":11.0,"30日最低值到当前周期":11.0,"60日最低值到当前周期":11.0,"120日最低值到当前周期":93.0,"5日回归斜率":0.0017,"10日回归斜率":0.0071151515,"20日回归斜率":0.0098345865,"30日回归斜率":0.0029434928,"60日回归斜率":-0.0011400945,"120日回归斜率":0.0046927113,"5日标准差":0.0201057206,"10日标准差":0.0415615207,"20日标准差":0.0735346177,"30日标准差":0.0613039875,"60日标准差":0.0658989041,"120日标准差":0.1933566996,"CCI商品路径指标":70.3685866564,"MFI最近流量指标":61.0892060821,"MTM动量线_MTM值":0.19,"MTM动量线_MTMMA值":0.1388333333,"RSI相对强弱_RSI1":68.2594517831,"RSI相对强弱_RSI2":62.4260981009,"RSI相对强弱_RSI3":57.8736166833,"KDJ指标_K值":73.4728385059,"KDJ指标_D值":74.4791201674,"KDJ指标_J值":71.460275183,"SKDJ慢速随机_K值":72.8549464241,"SKDJ慢速随机_D值":74.7667799953,"UDL引力线_UDL值":2.2176166667,"UDL引力线_MAUDL值":2.2062055556,"WR威廉指标_WR1":15.8192090395,"WR威廉指标_WR2":31.4606741573,"LWR指标_LWR1":26.5271614941,"LWR指标_LWR2":25.5208798326,"MARSI相对强弱平均线_RSI1":61.9020855116,"MARSI相对强弱平均线_RSI2":64.5847990554,"BIAS乖离率_BIAS1":0.936246099,"BIAS乖离率_BIAS2":2.7495177943,"BIAS乖离率_BIAS3":4.6452507511,"BIAS_QL乖离率传统版_BIAS值":0.936246099,"BIAS_QL乖离率传统版_BIASMA值":0.460499484,"BIAS36三六乖离_BIAS36":-0.0043333333,"BIAS36三六乖离_BIAS612":0.0395833333,"BIAS36三六乖离_MABIAS":0.0101388889,"ACCER幅度涨速":-0.0014565455,"ASI振动升降指标_ASI":0.7768112496,"ASI振动升降指标_ASIT":-0.3003756425,"CHO佳庆指标_CHO":6504.8839916836,"CHO佳庆指标_MACHO":3497.5620241337,"DMA_XT平均差_DIF":0.05194,"DMA_XT平均差_DIFMA":-0.019882,"DMI趋向指标_PDI":-25.1677852349,"DMI趋向指标_MDI":23.8255033557,"DMI趋向指标_ADX":-2427.6023391814,"DMI趋向指标_ADXR":-6759.4956140358,"DPO区间震荡线_DPO":0.113,"DPO区间震荡线_MADPO":0.1328095238,"EMV简易波动指标_EMV":0.0565082761,"EMV简易波动指标_MAEMV":-0.0144416061,"MACD平滑异同平均线_DIF":0.0262730702,"MACD平滑异同平均线_DEA":0.01414282,"MACD平滑异同平均线_MACD":0.0242605005,"VMACD量平滑异同平均线_DIF":-303461.3717964583,"VMACD量平滑异同平均线_DEA":-372446.382516626,"VMACD量平滑异同平均线_MACD":68985.0107201677,"SMACD单线平滑异同平均线_DEA":0.01414282,"SMACD单线平滑异同平均线_MACD":0.0262730702,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.162743594,"TRIX三重指数平均线_MATRIX":0.0121870254,"UOS终极指标_UOS":50.1148370285,"UOS终极指标_MAUOS":56.687908699,"VTP量价曲线_VPT":-177228.2684347031,"VTP量价曲线_MAVP":-112077.8181982554,"WVAD威廉变异离散量_WVAD":186.5225269038,"WVAD威廉变异离散量_MAWVAD":36.0530033517,"JS加数线_JS":-0.0176522507,"JS加数线_MAJS1":0.1860106081,"JS加数线_MAJS2":0.7522957383,"JS加数线_MAJS3":0.1966251869,"CYE市场趋势_CYEL":-0.0178667143,"CYE市场趋势_CYES":0.1822052412,"GDX轨道线_轨道":0.0387873616,"GDX轨道线_压力线":0.0422782242,"GDX轨道线_支撑线":0.0352964991,"JLHB绝路航标_B":28.0252367389,"JLHB绝路航标_VAR2":26.1346529892,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":133.1695331695,"BRAR情绪指标_AR":91.1949685535,"CR带状能量线_CR":120.6401766004,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":23.9572790241,"MASS梅斯线_MAMASS":22.9851601765,"PSY心理线_PSY":58.3333333333,"PSY心理线_PSYMA":59.7222222222,"VR成交量变异率_VR":141.4844031212,"VR成交量变异率_MAVR":138.9803877647,"WAD威廉多空力度线_WAD":0.943,"WAD威廉多空力度线_MAWAD":0.8385333333,"PCNT幅度比_PCNT":1.6784452297,"PCNT幅度比_MAPCNT":0.5444437339,"CYR市场强弱_CYR":0.3213692741,"CYR市场强弱_MACYR":0.293050558,"AMO成交金额_AMOW":36806.8849,"AMO成交金额_AMO1":36547.82868,"AMO成交金额_AMO2":38191.00998,"OBV累积能量线_OBV":237170167,"OBV累积能量线_MAOBV":232496998.0666666627,"VOL成交量_MAVOL1":1628390.0,"VOL成交量_MAVOL2":1710547.3,"VRSI相对强弱量_RSI1":48.7452683272,"VRSI相对强弱量_RSI2":46.8574786046,"VRSI相对强弱量_RSI3":46.6018042296,"HSL换手线_HSL":1630904,"HSL换手线_MAHSL":1628390.0,"MA均线_MA1":2.2384,"MA均线_MA2":2.2288,"MA均线_MA3":2.1646,"MA均线_MA4":2.1893666667,"ACD升降线_ACD":0.943,"ACD升降线_MAACD":0.8709008395,"BBI多空均线":2.2121458333,"EXPMA指数平均线_EXP1":2.2119614617,"EXPMA指数平均线_EXP2":2.1595357625,"HMA高价平均线_HMA1":2.2585,"HMA高价平均线_HMA2":2.2136666667,"HMA高价平均线_HMA3":2.1751333333,"HMA高价平均线_HMA4":2.1966,"HMA高价平均线_HMA5":2.1312111111,"LMA低价平均线_LMA1":2.2306666667,"LMA低价平均线_LMA2":2.1908333333,"LMA低价平均线_LMA3":2.1517,"LMA低价平均线_LMA4":2.1519142857,"LMA低价平均线_LMA5":2.0914888889,"VMA变异平均线_VMA1":2.2439583333,"VMA变异平均线_VMA2":2.2021875,"VMA变异平均线_VMA3":2.1637583333,"VMA变异平均线_VMA4":2.1754392857,"VMA变异平均线_VMA5":2.1123111111,"AMV成本均线_AMV1":2.2426735994,"AMV成本均线_AMV2":2.203568329,"AMV成本均线_AMV3":2.1716296833,"AMV成本均线_AMV4":2.2064009054,"BBIBOLL多空布林线_BBIBOLL":2.2121458333,"BBIBOLL多空布林线_UPR":2.4507286899,"BBIBOLL多空布林线_DWN":1.9735629768,"ALLIGAT鳄鱼线_上唇":2.2519,"ALLIGAT鳄鱼线_牙齿":2.1606875,"ALLIGAT鳄鱼线_下颚":2.1107692308,"GMMA顾比均线_MA3":2.2460332793,"GMMA顾比均线_MA5":2.2392728128,"GMMA顾比均线_MA8":2.2272504748,"GMMA顾比均线_MA10":2.2191480607,"GMMA顾比均线_MA12":2.2119614617,"GMMA顾比均线_MA15":2.2032620155,"GMMA顾比均线_MA30":2.1815747813,"GMMA顾比均线_MA35":2.1765711507,"GMMA顾比均线_MA40":2.1712945559,"GMMA顾比均线_MA45":2.1656077036,"GMMA顾比均线_MA50":2.1595357625,"GMMA顾比均线_MA60":2.1465919036,"BOLL布林线_BOLL":2.1646,"BOLL布林线_UB":2.3116692354,"BOLL布林线_LB":2.0175307646,"PBX瀑布线_PBX1":2.2213566954,"PBX瀑布线_PBX2":2.2008093623,"PBX瀑布线_PBX3":2.1865846301,"PBX瀑布线_PBX4":2.184429132,"PBX瀑布线_PBX5":2.1777422206,"PBX瀑布线_PBX6":2.1506786972,"ENE轨道线_UPPER":2.2935008,"ENE轨道线_LOWER":2.0338592,"ENE轨道线_ENE":2.16368,"MIKE麦克支撑压力_STOR":2.5025774316,"MIKE麦克支撑压力_MIDR":2.41097642,"MIKE麦克支撑压力_WEKR":2.3193754084,"MIKE麦克支撑压力_WEKS":2.1046160975,"MIKE麦克支撑压力_MIDS":1.9814577981,"MIKE麦克支撑压力_STOS":1.8582994988,"XS薛斯通道_SUP":2.3204907939,"XS薛斯通道_SDN":2.0577937229,"XS薛斯通道_LUP":2.5159311966,"XS薛斯通道_LDN":1.8979831834,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1304613882,"MA交易_MA1":2.2384,"MA交易_MA2":2.1646,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0262730702,"MACD交易_DEA":0.01414282,"MACD交易_MACD":0.0242605005,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":73.4728385059,"KDJ交易_D":74.4791201674,"KDJ交易_J":71.460275183,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4852245482,"SG_XDT心电图_MQR1":0.4785657494,"SG_XDT心电图_MQR2":0.4789245738,"SG_NDB脑电波_DK":3.268,"SG_NDB脑电波_MDK1":3.2552,"SG_NDB脑电波_MDK2":3.2525,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":25.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":21058.9159369743,"LON龙系长线_LONMA":19399.2611615413,"LON龙系长线_LONT":21058.9159369743,"SHT龙系短线_SHT":4.5346413721,"SHT龙系短线_SHTMA":3.826351554,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":62.2716337498,"ZLMM主力买卖_MMM":60.8787788957,"ZLMM主力买卖_MML":52.6992395203,"SLZT神龙在天_白龙":2.017152,"SLZT神龙在天_黄龙":2.3635716949,"SLZT神龙在天_紫龙":1.6469942768,"SLZT神龙在天_青龙":2.0549513829,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":29890.2146269184,"ADVOL龙系离散量_MA1":29642.3832044512,"ADVOL龙系离散量_MA2":28439.4133446531,"CYS市场盈亏":2.3335861697,"CYW主力控盘":437.4648777012,"JAX济安线_J":2.2450039837,"JAX济安线_A":2.2422464261,"JAX济安线_X":2.2422464261,"XJDX超级短线_J":0.3045001206,"XJDX超级短线_D":0.379741373,"XJDX超级短线_K":0.3045001206,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":3.7262750017,"ZJTJ庄家抬轿_主力出货":0.0,"BDZX波段之星_AK":90.5210889968,"BDZX波段之星_AD1":91.7272982153,"BDZX波段之星_AJ":88.1086705598,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":-0.0508775882,"LHXJ猎狐先觉_主力控盘":0.0508775882,"LYJH猎鹰歼狐_机构做空能量线":18.4088986202,"LYJH猎鹰歼狐_机构做多能量线":63.9173205514,"JFZX飓风智能中线_多头力量":56.2055169241,"JFZX飓风智能中线_空头力量":43.7944830759,"CYHT财运亨通_SK":63.0511547133,"CYHT财运亨通_SD":59.3295727334,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":2.264,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":null,"CDP_STD逆势操作_CDP":2.2313333333,"CDP_STD逆势操作_AH":2.2586666667,"CDP_STD逆势操作_NH":2.2386666667,"CDP_STD逆势操作_NL":2.2186666667,"CDP_STD逆势操作_AL":2.1986666667,"Alpha001":0.0722335126,"Alpha002":-1.6888888889,"Alpha003":-21.998,"Alpha004":-1,"Alpha005":-0.8607533668,"Alpha006":-0.2064364207,"Alpha007":0.8795090291,"Alpha008":-0.273155416,"Alpha009":0.0000000001,"Alpha010":0.9627831715,"Alpha011":-982008.6851731525,"Alpha012":-0.0202487213,"Alpha013":-223.4279631752,"Alpha014":-0.002,"Alpha015":0.0139263252,"Alpha016":-0.8649921507,"Alpha017":1.0010826841,"Alpha018":0.9991173875,"Alpha019":-0.0008826125,"Alpha020":0.8912655971,"Alpha021":0.0151238095,"Alpha022":-0.0022478868,"Alpha023":53.5146137442,"Alpha024":0.0344251778,"Alpha025":-0.7172076587,"Alpha026":0.9046746507,"Alpha027":395.0707535047,"Alpha028":53.1648029137,"Alpha029":14535.68627451,"Alpha030":0.0002976026,"Alpha031":2.7495177943,"Alpha032":-2.2660406886,"Alpha033":-0.0380555382,"Alpha034":0.9732405771,"Alpha035":-0.9313099042,"Alpha036":0.8794992175,"Alpha037":0.0560918779,"Alpha038":-0.034,"Alpha039":-0.3229329173,"Alpha040":123.8752430145,"Alpha041":-0.4811320755,"Alpha042":-0.6017252755,"Alpha043":1143876.0,"Alpha044":1.0333333333,"Alpha045":0.1026428577,"Alpha046":0.9770962161,"Alpha047":44.0415872244,"Alpha048":-0.2107310953,"Alpha049":0.2528735632,"Alpha050":0.4942528736,"Alpha051":0.7471264368,"Alpha052":125.7517347726,"Alpha053":58.3333333333,"Alpha054":-0.6756329114,"Alpha055":1.9371614987,"Alpha056":-0.637973138,"Alpha057":63.6721440263,"Alpha058":55.0,"Alpha059":0.155,"Alpha060":3679602.0857139779,"Alpha061":-0.9157566303,"Alpha062":-0.6686839958,"Alpha063":68.2594517831,"Alpha064":-0.8237129485,"Alpha065":0.9907243816,"Alpha066":0.936246099,"Alpha067":57.8736166833,"Alpha068":0.0000000001,"Alpha069":-0.7254901961,"Alpha070":69721694.3320248872,"Alpha071":4.6452507511,"Alpha072":46.7749848034,"Alpha073":-0.5516993881,"Alpha074":0.9875195008,"Alpha075":0.3846153846,"Alpha076":0.8500055851,"Alpha077":0.0468018721,"Alpha078":51.7544422349,"Alpha079":62.4260981009,"Alpha080":-18.1063836091,"Alpha081":1831474.5243160846,"Alpha082":47.6988063933,"Alpha083":-0.5306122449,"Alpha084":7535673.0,"Alpha085":0.7,"Alpha086":-0.038,"Alpha087":-0.6748384221,"Alpha088":7.4513526341,"Alpha089":0.0242605005,"Alpha090":-0.8237129485,"Alpha091":-0.489213128,"Alpha092":-1.0,"Alpha093":0.125,"Alpha094":8479126.0,"Alpha095":95002252.2293613553,"Alpha096":68.9258145826,"Alpha097":376510.3536076262,"Alpha098":-0.049,"Alpha099":-0.5227629513,"Alpha100":416073.0836736145,"Alpha101":-0.7737909516,"Alpha102":48.7452683272,"Alpha103":45.0,"Alpha104":0.2701191834,"Alpha105":-0.641584701,"Alpha106":0.157,"Alpha107":-0.7041407471,"Alpha108":-0.892927531,"Alpha109":0.9829355034,"Alpha110":177.8181818182,"Alpha111":-255530.5485684633,"Alpha112":47.0297029703,"Alpha113":-0.0014481078,"Alpha114":1244.8345855426,"Alpha115":0.3923926025,"Alpha116":0.0090879699,"Alpha117":0.0054931641,"Alpha118":111.1111111111,"Alpha119":0.4836193448,"Alpha120":0.9801358157,"Alpha121":-0.9958224056,"Alpha122":0.0020893865,"Alpha123":-0.6029661737,"Alpha124":-81.7421146621,"Alpha125":0.5102739726,"Alpha126":2.2586666667,"Alpha127":2.3190663024,"Alpha128":61.0892060821,"Alpha129":0.107,"Alpha130":0.1269035533,"Alpha131":0.9910269634,"Alpha132":359605637.6499999762,"Alpha133":35.0,"Alpha134":149407.7917068464,"Alpha135":1.0060845142,"Alpha136":-0.6464799508,"Alpha137":0.4689017341,"Alpha138":-0.7588589258,"Alpha139":-0.6717907482,"Alpha140":0.3333333333,"Alpha141":-0.4701130856,"Alpha142":-0.2687210774,"Alpha143":0.0170709793,"Alpha144":0.0,"Alpha145":-3.3144311188,"Alpha146":8.9013909901,"Alpha147":0.007169289,"Alpha148":-0.4169092049,"Alpha149":0.8211172204,"Alpha150":3683668.5013333331,"Alpha151":0.0164334397,"Alpha152":-0.0041362334,"Alpha153":2.2121458333,"Alpha154":-22.3760345904,"Alpha155":68985.0107201677,"Alpha156":-0.3697347894,"Alpha157":1.0220472441,"Alpha158":0.00795053,"Alpha159":-5201.7408698071,"Alpha160":0.0254719382,"Alpha161":0.043,"Alpha162":0.8689374377,"Alpha163":0.352574103,"Alpha164":160233.2706259316,"Alpha165":-19.2313173017,"Alpha166":-0.0041814447,"Alpha167":0.297,"Alpha168":-0.9846727956,"Alpha169":0.0006605999,"Alpha170":-0.4592388851,"Alpha171":-16.7388109409,"Alpha172":33.5662161277,"Alpha173":3.0528291708,"Alpha174":0.0293236444,"Alpha175":0.034,"Alpha176":0.5802106163,"Alpha177":80.0,"Alpha178":27841.1284815813,"Alpha179":0.0870568364,"Alpha180":-1630904.0,"Alpha181":0.0066765186,"Alpha182":0.6,"Alpha183":15.5548358039,"Alpha184":0.5062402496,"Alpha185":-0.0000095597,"Alpha186":28.6798775601,"Alpha187":0.39,"Alpha188":-24.6067442014,"Alpha189":0.0300833333,"Alpha190":-0.772880177,"Alpha191":0.0859011962},{"date":"2026-08-17","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.264,"high":2.274,"low":2.262,"close":2.274,"volume":1535357,"amount":348272377.9999999404,"5日涨跌幅":0.5749668288,"10日涨跌幅":6.9111424542,"20日涨跌幅":8.4923664122,"30日涨跌幅":4.744357439,"60日涨跌幅":5.9645852749,"120日涨跌幅":24.262295082,"六脉神剑":6,"小波段交易":true,"大波段交易":true,"波段超级买卖":true,"价格距离5日均线涨跌幅":1.4725568942,"价格距离10日均线涨跌幅":1.3594829507,"价格距离20日均线涨跌幅":4.6238785369,"价格距离30日均线涨跌幅":4.9280177187,"价格距离60日均线涨跌幅":3.7645448323,"价格距离120日均线涨跌幅":12.108526049,"5日均线距离10日均线涨跌幅":-0.1114330287,"10日均线距离20日均线涨跌幅":3.2206119163,"20日均线距离30日均线涨跌幅":0.2906976744,"30日均线距离60日均线涨跌幅":-1.1088295688,"60日均线距离120日均线涨跌幅":8.04126422,"5日偏度":0.5514141512,"10日偏度":-0.6949372634,"20日偏度":-0.1026650165,"30日偏度":0.0991094726,"60日偏度":0.1911271172,"120日偏度":-0.3399981715,"5日峰度":-2.6238705811,"10日峰度":-0.6690107676,"20日峰度":-1.5008808747,"30日峰度":-0.9000811373,"60日峰度":-0.1035433675,"120日峰度":-1.3350511601,"KDJ_KD金叉":true,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":true,"PSY_死叉":false,"5日均线":2.241,"10日均线":2.2435,"20日均线":2.1735,"30日均线":2.1672,"60日均线":2.1915,"120日均线":2.0283916667,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":true,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":2.0,"连续下跌天数":0.0,"价格在5均线上":true,"价格在10均线上":true,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":0.0123298054,"10日Alpha":0.1544823707,"20日Alpha":1.0060719525,"30日Alpha":0.6675376336,"60日Alpha":0.3993625896,"120日Alpha":0.5613607089,"5日Beta":0.6924900923,"10日Beta":1.4552676999,"20日Beta":0.8983994254,"30日Beta":0.6390704104,"60日Beta":0.7579658711,"120日Beta":0.8598873511,"5日夏普比率":1.4240412407,"10日夏普比率":6.393430803,"20日夏普比率":4.024267844,"30日夏普比率":1.719488174,"60日夏普比率":0.9468512769,"120日夏普比率":1.7598102987,"5日年化波动率":0.2162147047,"10日年化波动率":0.2693483888,"20日年化波动率":0.2638888855,"30日年化波动率":0.2431514055,"60日年化波动率":0.3052875143,"120日年化波动率":0.2816542959,"5日最大回撤":-0.0203449801,"10日最大回撤":-0.0229378033,"20日最大回撤":-0.0422336931,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":1.4840579626,"10日上涨捕获率":4.5960316175,"20日上涨捕获率":2.4853657955,"30日上涨捕获率":0.7877293545,"60日上涨捕获率":0.4871037306,"120日上涨捕获率":0.8512490405,"5日下跌捕获率":1.118306755,"10日下跌捕获率":1.2738513165,"20日下跌捕获率":0.9737190432,"30日下跌捕获率":0.8954189662,"60日下跌捕获率":0.8829387563,"120日下跌捕获率":0.8586607574,"3日回归动量":7.737404262,"5日回归动量":4.9187864175,"7日回归动量":0.048134924,"9日回归动量":-0.0035068732,"12日回归动量":0.6519287498,"15日回归动量":2.4026280134,"18日回归动量":2.0944522401,"20日回归动量":1.6329640568,"23日回归动量":1.1463370084,"25日回归动量":0.673926685,"28日回归动量":0.3497025385,"30日回归动量":0.2556372999,"35日回归动量":0.0782033232,"40日回归动量":0.0257275153,"45日回归动量":-0.0019711343,"50日回归动量":-0.0003661206,"60日回归动量":-0.0013335689,"5日最高值到当前周期":0.0,"10日最高值到当前周期":0.0,"20日最高值到当前周期":0.0,"30日最高值到当前周期":0.0,"60日最高值到当前周期":54.0,"120日最高值到当前周期":54.0,"5日最低值到当前周期":4.0,"10日最低值到当前周期":9.0,"20日最低值到当前周期":12.0,"30日最低值到当前周期":12.0,"60日最低值到当前周期":12.0,"120日最低值到当前周期":94.0,"5日回归斜率":0.0156,"10日回归斜率":0.0027939394,"20日回归斜率":0.0103142857,"30日回归斜率":0.0037045606,"60日回归斜率":-0.0010748541,"120日回归斜率":0.0047139281,"5日标准差":0.0234264807,"10日标准差":0.0260624251,"20日标准差":0.0754403738,"30日标准差":0.0644181134,"60日标准差":0.0665293168,"120日标准差":0.1938432483,"CCI商品路径指标":73.823113578,"MFI最近流量指标":66.8967225571,"MTM动量线_MTM值":0.233,"MTM动量线_MTMMA值":0.155,"RSI相对强弱_RSI1":70.4785960194,"RSI相对强弱_RSI2":63.6336783977,"RSI相对强弱_RSI3":58.5217355548,"KDJ指标_K值":75.5736526369,"KDJ指标_D值":74.8439643239,"KDJ指标_J值":77.033029263,"SKDJ慢速随机_K值":74.5531454812,"SKDJ慢速随机_D值":73.4635255253,"UDL引力线_UDL值":2.2281666667,"UDL引力线_MAUDL值":2.2119791667,"WR威廉指标_WR1":14.1732283465,"WR威廉指标_WR2":20.2247191011,"LWR指标_LWR1":24.4263473631,"LWR指标_LWR2":25.1560356761,"MARSI相对强弱平均线_RSI1":63.3479090519,"MARSI相对强弱平均线_RSI2":63.9089849571,"BIAS乖离率_BIAS1":1.3218476162,"BIAS乖离率_BIAS2":2.3018669866,"BIAS乖离率_BIAS3":4.8973629584,"BIAS_QL乖离率传统版_BIAS值":1.3218476162,"BIAS_QL乖离率传统版_BIASMA值":0.1912051588,"BIAS36三六乖离_BIAS36":0.0103333333,"BIAS36三六乖离_BIAS612":0.0215,"BIAS36三六乖离_MABIAS":0.00225,"ACCER幅度涨速":0.0005549273,"ASI振动升降指标_ASI":0.7869748457,"ASI振动升降指标_ASIT":0.0577236082,"CHO佳庆指标_CHO":7027.4959072466,"CHO佳庆指标_MACHO":4510.3806172611,"DMA_XT平均差_DIF":0.06526,"DMA_XT平均差_DIFMA":-0.005596,"DMI趋向指标_PDI":-22.5454545455,"DMI趋向指标_MDI":17.8181818182,"DMI趋向指标_ADX":-2311.5766981557,"DMI趋向指标_ADXR":-7063.4272379674,"DPO区间震荡线_DPO":0.0955714286,"DPO区间震荡线_MADPO":0.1202619048,"EMV简易波动指标_EMV":0.3807189727,"EMV简易波动指标_MAEMV":0.0615581785,"MACD平滑异同平均线_DIF":0.0292758601,"MACD平滑异同平均线_DEA":0.017169428,"MACD平滑异同平均线_MACD":0.0242128642,"VMACD量平滑异同平均线_DIF":-292611.9528314385,"VMACD量平滑异同平均线_DEA":-356479.4965795885,"VMACD量平滑异同平均线_MACD":63867.54374815,"SMACD单线平滑异同平均线_DEA":0.017169428,"SMACD单线平滑异同平均线_MACD":0.0292758601,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.1879983738,"TRIX三重指数平均线_MATRIX":0.0522961295,"UOS终极指标_UOS":55.0449450935,"UOS终极指标_MAUOS":56.218490526,"VTP量价曲线_VPT":-37086.1255783841,"VTP量价曲线_MAVP":-135496.8597537601,"WVAD威廉变异离散量_WVAD":208.1836921419,"WVAD威廉变异离散量_MAWVAD":55.3263045518,"JS加数线_JS":0.1149933658,"JS加数线_MAJS1":-0.0429888382,"JS加数线_MAJS2":0.7552964913,"JS加数线_MAJS3":0.2355851873,"CYE市场趋势_CYEL":0.116154396,"CYE市场趋势_CYES":0.2213107909,"GDX轨道线_轨道":0.0433416321,"GDX轨道线_压力线":0.047242379,"GDX轨道线_支撑线":0.0394408852,"JLHB绝路航标_B":29.0611676002,"JLHB绝路航标_VAR2":26.7199559114,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":129.3398533007,"BRAR情绪指标_AR":94.1935483871,"CR带状能量线_CR":117.770419426,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":24.2188354025,"MASS梅斯线_MAMASS":23.3323592538,"PSY心理线_PSY":66.6666666667,"PSY心理线_PSYMA":59.7222222222,"VR成交量变异率_VR":139.9364879798,"VR成交量变异率_MAVR":134.721009896,"WAD威廉多空力度线_WAD":0.955,"WAD威廉多空力度线_MAWAD":0.8427,"PCNT幅度比_PCNT":0.4397537379,"PCNT幅度比_MAPCNT":0.5095470686,"CYR市场强弱_CYR":0.3318968345,"CYR市场强弱_MACYR":0.230697753,"AMO成交金额_AMOW":34827.2378,"AMO成交金额_AMO1":34747.06856,"AMO成交金额_AMO2":39500.19988,"OBV累积能量线_OBV":238705524,"OBV累积能量线_MAOBV":232762648.8333333433,"VOL成交量_MAVOL1":1549863.3999999999,"VOL成交量_MAVOL2":1761855.3999999999,"VRSI相对强弱量_RSI1":45.8502775162,"VRSI相对强弱量_RSI2":45.8564157082,"VRSI相对强弱量_RSI3":46.2443393751,"HSL换手线_HSL":1535357,"HSL换手线_MAHSL":1549863.3999999999,"MA均线_MA1":2.241,"MA均线_MA2":2.2435,"MA均线_MA3":2.1735,"MA均线_MA4":2.1915,"ACD升降线_ACD":0.955,"ACD升降线_MAACD":0.8789102834,"BBI多空均线":2.2224166667,"EXPMA指数平均线_EXP1":2.2215058522,"EXPMA指数平均线_EXP2":2.1640245561,"HMA高价平均线_HMA1":2.2585,"HMA高价平均线_HMA2":2.2319166667,"HMA高价平均线_HMA3":2.1784333333,"HMA高价平均线_HMA4":2.1995714286,"HMA高价平均线_HMA5":2.1371222222,"LMA低价平均线_LMA1":2.2346666667,"LMA低价平均线_LMA2":2.20975,"LMA低价平均线_LMA3":2.1555333333,"LMA低价平均线_LMA4":2.1550857143,"LMA低价平均线_LMA5":2.0974111111,"VMA变异平均线_VMA1":2.246125,"VMA变异平均线_VMA2":2.2207916667,"VMA变异平均线_VMA3":2.1672,"VMA变异平均线_VMA4":2.1784892857,"VMA变异平均线_VMA5":2.1182555556,"AMV成本均线_AMV1":2.2409665331,"AMV成本均线_AMV2":2.2165547951,"AMV成本均线_AMV3":2.172303891,"AMV成本均线_AMV4":2.2094542117,"BBIBOLL多空布林线_BBIBOLL":2.2224166667,"BBIBOLL多空布林线_UPR":2.4406082445,"BBIBOLL多空布林线_DWN":2.0042250888,"ALLIGAT鳄鱼线_上唇":2.2435,"ALLIGAT鳄鱼线_牙齿":2.1864375,"ALLIGAT鳄鱼线_下颚":2.1215384615,"GMMA顾比均线_MA3":2.2600166396,"GMMA顾比均线_MA5":2.2508485419,"GMMA顾比均线_MA8":2.2376392582,"GMMA顾比均线_MA10":2.2291211406,"GMMA顾比均线_MA12":2.2215058522,"GMMA顾比均线_MA15":2.2121042636,"GMMA顾比均线_MA30":2.1875376987,"GMMA顾比均线_MA35":2.1819838646,"GMMA顾比均线_MA40":2.1763045775,"GMMA顾比均线_MA45":2.1703204122,"GMMA顾比均线_MA50":2.1640245561,"GMMA顾比均线_MA60":2.1507692183,"BOLL布林线_BOLL":2.1735,"BOLL布林线_UB":2.3243807476,"BOLL布林线_LB":2.0226192524,"PBX瀑布线_PBX1":2.2293723506,"PBX瀑布线_PBX2":2.212391608,"PBX瀑布线_PBX3":2.1937177041,"PBX瀑布线_PBX4":2.188656289,"PBX瀑布线_PBX5":2.1827488874,"PBX瀑布线_PBX6":2.1554527348,"ENE轨道线_UPPER":2.2979952,"ENE轨道线_LOWER":2.0378448,"ENE轨道线_ENE":2.16792,"MIKE麦克支撑压力_STOR":2.4782769936,"MIKE麦克支撑压力_MIDR":2.4004980054,"MIKE麦克支撑压力_WEKR":2.3227190173,"MIKE麦克支撑压力_WEKS":2.134096233,"MIKE麦克支撑压力_MIDS":2.023252437,"MIKE麦克支撑压力_STOS":1.9124086409,"XS薛斯通道_SUP":2.3270694053,"XS薛斯通道_SDN":2.0636275858,"XS薛斯通道_LUP":2.5259384248,"XS薛斯通道_LDN":1.9055324959,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1433844771,"MA交易_MA1":2.241,"MA交易_MA2":2.1735,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0292758601,"MACD交易_DEA":0.017169428,"MACD交易_MACD":0.0242128642,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":75.5736526369,"KDJ交易_D":74.8439643239,"KDJ交易_J":77.033029263,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.47963573,"SG_XDT心电图_MQR1":0.478321565,"SG_XDT心电图_MQR2":0.4800706987,"SG_NDB脑电波_DK":3.312,"SG_NDB脑电波_MDK1":3.2592,"SG_NDB脑电波_MDK2":3.2703,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":20.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":22432.9241172024,"LON龙系长线_LONMA":20035.5248058611,"LON龙系长线_LONT":22432.9241172024,"SHT龙系短线_SHT":4.7545993882,"SHT龙系短线_SHTMA":3.5855150712,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":65.2535581383,"ZLMM主力买卖_MMM":61.8509520607,"ZLMM主力买卖_MML":52.9203071038,"SLZT神龙在天_白龙":2.02084,"SLZT神龙在天_黄龙":2.3699906166,"SLZT神龙在天_紫龙":1.6482501019,"SLZT神龙在天_青龙":2.0596923552,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30043.7503269184,"ADVOL龙系离散量_MA1":29657.9917715386,"ADVOL龙系离散量_MA2":28464.0316578919,"CYS市场盈亏":2.4455760183,"CYW主力控盘":548.9068600541,"JAX济安线_J":null,"JAX济安线_A":2.2620407982,"JAX济安线_X":null,"XJDX超级短线_J":0.3288217578,"XJDX超级短线_D":0.3218659128,"XJDX超级短线_K":0.3288217578,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":3.8991111698,"ZJTJ庄家抬轿_主力出货":0.0,"BDZX波段之星_AK":90.9810406032,"BDZX波段之星_AD1":91.2297931406,"BDZX波段之星_AJ":90.4835355285,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":-0.0520565183,"LHXJ猎狐先觉_主力控盘":0.0520565183,"LYJH猎鹰歼狐_机构做空能量线":12.7063948354,"LYJH猎鹰歼狐_机构做多能量线":65.4889126209,"JFZX飓风智能中线_多头力量":55.8047643263,"JFZX飓风智能中线_空头力量":44.1952356737,"CYHT财运亨通_SK":67.084424996,"CYHT财运亨通_SD":63.2069988647,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":2.274,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":null,"CDP_STD逆势操作_CDP":2.2586666667,"CDP_STD逆势操作_AH":2.2883333333,"CDP_STD逆势操作_NH":2.2703333333,"CDP_STD逆势操作_NL":2.2523333333,"CDP_STD逆势操作_AL":2.2343333333,"Alpha001":0.2393733443,"Alpha002":-0.1111111111,"Alpha003":-21.998,"Alpha004":-1,"Alpha005":-0.8607533668,"Alpha006":-0.7080062794,"Alpha007":1.0791499257,"Alpha008":-0.8053375196,"Alpha009":0.0000000001,"Alpha010":0.9805825243,"Alpha011":-553035.5740620415,"Alpha012":-0.0109895535,"Alpha013":-224.5667948949,"Alpha014":0.013,"Alpha015":0.0,"Alpha016":-0.8649921507,"Alpha017":0.9958117538,"Alpha018":1.0057496683,"Alpha019":-0.0057496683,"Alpha020":0.3530450132,"Alpha021":0.0072714286,"Alpha022":-0.000198581,"Alpha023":56.7313553106,"Alpha024":0.0301401422,"Alpha025":-1.4076581784,"Alpha026":0.8993716645,"Alpha027":362.9931829273,"Alpha028":58.7050205775,"Alpha029":5420.5013239187,"Alpha030":0.0002837134,"Alpha031":2.3018669866,"Alpha032":-2.2926447574,"Alpha033":-0.0163619345,"Alpha034":0.9774992671,"Alpha035":-0.9217252396,"Alpha036":0.8450704225,"Alpha037":-0.0133835341,"Alpha038":-0.03,"Alpha039":-0.5288611544,"Alpha040":122.4402025979,"Alpha041":-0.7232704403,"Alpha042":-0.1792579253,"Alpha043":687742.0,"Alpha044":1.2166666667,"Alpha045":0.0295754732,"Alpha046":0.9773160364,"Alpha047":41.395268544,"Alpha048":-0.2016927265,"Alpha049":0.1981132075,"Alpha050":0.6037735849,"Alpha051":0.8018867925,"Alpha052":122.7447956823,"Alpha053":66.6666666667,"Alpha054":-0.292721519,"Alpha055":2.4755962813,"Alpha056":-0.7116272616,"Alpha057":64.5454742947,"Alpha058":60.0,"Alpha059":0.189,"Alpha060":6648234.9190473426,"Alpha061":-0.9079563183,"Alpha062":-0.3029467315,"Alpha063":70.4785960194,"Alpha064":-0.8845553822,"Alpha065":0.9869539724,"Alpha066":1.3218476162,"Alpha067":58.5217355548,"Alpha068":0.0000000001,"Alpha069":-0.760989011,"Alpha070":61311347.1060150638,"Alpha071":4.8973629584,"Alpha072":45.00496709,"Alpha073":-0.831632596,"Alpha074":0.992199688,"Alpha075":0.36,"Alpha076":0.8516649601,"Alpha077":0.0327613105,"Alpha078":45.9020703253,"Alpha079":63.6336783977,"Alpha080":-20.3648877847,"Alpha081":1803272.8553336004,"Alpha082":46.3251020286,"Alpha083":-0.4740973312,"Alpha084":10790961.0,"Alpha085":0.525,"Alpha086":-0.01,"Alpha087":-1.1065299755,"Alpha088":8.4923664122,"Alpha089":0.0242128642,"Alpha090":-0.6224648986,"Alpha091":-0.0449851152,"Alpha092":-0.8845553822,"Alpha093":0.112,"Alpha094":7969523.0,"Alpha095":95032556.4645449668,"Alpha096":67.4657011533,"Alpha097":299349.1949988178,"Alpha098":-0.048,"Alpha099":-0.5039246468,"Alpha100":416633.8007407733,"Alpha101":-0.7987519501,"Alpha102":45.8502775162,"Alpha103":40.0,"Alpha104":0.2897326674,"Alpha105":-0.3296228168,"Alpha106":0.178,"Alpha107":-0.19332407,"Alpha108":-0.8460979647,"Alpha109":0.9061215754,"Alpha110":184.8484848485,"Alpha111":-551723.5054363888,"Alpha112":61.154855643,"Alpha113":0.7177698652,"Alpha114":1237.8326826981,"Alpha115":0.5860103487,"Alpha116":0.0098345865,"Alpha117":0.0134277344,"Alpha118":116.3551401869,"Alpha119":0.3463338534,"Alpha120":0.9801491682,"Alpha121":-0.9798353287,"Alpha122":0.0024140234,"Alpha123":-0.5673975863,"Alpha124":-81.3239912092,"Alpha125":0.445561139,"Alpha126":2.27,"Alpha127":1.2714512359,"Alpha128":66.8967225571,"Alpha129":0.074,"Alpha130":0.1932624113,"Alpha131":0.9818538051,"Alpha132":358890648.5500000119,"Alpha133":35.0,"Alpha134":175275.933855953,"Alpha135":1.0095059648,"Alpha136":-0.1214217701,"Alpha137":0.1224347826,"Alpha138":-0.7838199242,"Alpha139":-0.2503096038,"Alpha140":0.3333333333,"Alpha141":-0.6978998384,"Alpha142":-0.0810088772,"Alpha143":0.0044169611,"Alpha144":0.0,"Alpha145":-4.2015581795,"Alpha146":1.5555693362,"Alpha147":0.009115676,"Alpha148":-0.4814402293,"Alpha149":0.8584512947,"Alpha150":3485260.3900000001,"Alpha151":0.0245117677,"Alpha152":-0.0028747895,"Alpha153":2.2224166667,"Alpha154":-23.5954069895,"Alpha155":63867.54374815,"Alpha156":-0.4071762871,"Alpha157":0.6354330709,"Alpha158":0.0052770449,"Alpha159":-5728.2086346797,"Alpha160":0.0241983413,"Alpha161":0.04075,"Alpha162":0.8305265597,"Alpha163":0.4836193448,"Alpha164":262505.075145016,"Alpha165":-16.8789862953,"Alpha166":-0.0042810811,"Alpha167":0.307,"Alpha168":-0.9321794643,"Alpha169":0.0011118416,"Alpha170":-0.3946820412,"Alpha171":100.0,"Alpha172":34.9705065567,"Alpha173":3.0691560607,"Alpha174":0.0317274717,"Alpha175":0.03,"Alpha176":0.2222808387,"Alpha177":75.0,"Alpha178":6781.6121908128,"Alpha179":0.160537966,"Alpha180":-1535357.0,"Alpha181":0.0085790289,"Alpha182":0.65,"Alpha183":14.9294175435,"Alpha184":0.4664586583,"Alpha185":-0.0000193383,"Alpha186":28.5731524139,"Alpha187":0.4,"Alpha188":-44.7405871937,"Alpha189":0.02425,"Alpha190":-0.5614859313,"Alpha191":-0.8661461376},{"date":"2026-08-18","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.243,"high":2.247,"low":2.234,"close":2.239,"volume":1115509,"amount":249761026.0,"5日涨跌幅":1.0835214447,"10日涨跌幅":2.1441605839,"20日涨跌幅":5.117370892,"30日涨跌幅":3.2272936837,"60日涨跌幅":0.3585835948,"120日涨跌幅":22.8195282501,"六脉神剑":1,"小波段交易":true,"大波段交易":true,"波段超级买卖":false,"价格距离5日均线涨跌幅":-0.3027874254,"价格距离10日均线涨跌幅":-0.4092162619,"价格距离20日均线涨跌幅":2.755914546,"价格距离30日均线涨跌幅":3.201917463,"价格距离60日均线涨跌幅":2.1612496008,"价格距离120日均线涨跌幅":10.1946904107,"5日均线距离10日均线涨跌幅":-0.1067520683,"10日均线距离20日均线涨跌幅":3.1781362583,"20日均线距离30日均线涨跌幅":0.4340411148,"30日均线距离60日均线涨跌幅":-1.0083803556,"60日均线距离120日均线涨跌幅":7.8634911391,"5日偏度":0.4857921266,"10日偏度":-0.3613883939,"20日偏度":-0.2887897752,"30日偏度":0.0269850165,"60日偏度":0.1868536043,"120日偏度":-0.3733925875,"5日峰度":-2.5069873954,"10日峰度":-1.5306856577,"20日峰度":-1.4756062037,"30日峰度":-1.0410458266,"60日峰度":-0.1186370983,"120日峰度":-1.3089526051,"KDJ_KD金叉":false,"KDJ_KD死叉":true,"RSI_金叉":false,"RSI_死叉":true,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":true,"5日均线":2.2458,"10日均线":2.2482,"20日均线":2.17895,"30日均线":2.1695333333,"60日均线":2.1916333333,"120日均线":2.0318583333,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":0.0,"连续下跌天数":1.0,"价格在5均线上":false,"价格在10均线上":false,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":0.3139254065,"10日Alpha":-0.3114131496,"20日Alpha":0.984620567,"30日Alpha":0.4236541623,"60日Alpha":0.1753578953,"120日Alpha":0.5606132207,"5日Beta":0.4217624765,"10日Beta":1.3717797311,"20日Beta":1.100375718,"30日Beta":0.6504037668,"60日Beta":0.7287986733,"120日Beta":0.8691638846,"5日夏普比率":3.0007359865,"10日夏普比率":2.2176110386,"20日夏普比率":2.470484928,"30日夏普比率":1.195496912,"60日夏普比率":0.1959108427,"120日夏普比率":1.6676483368,"5日年化波动率":0.1858077692,"10日年化波动率":0.2543722721,"20日年化波动率":0.2686269555,"30日年化波动率":0.2480531181,"60日年化波动率":0.2963698243,"120日年化波动率":0.2826549263,"5日最大回撤":-0.0153913808,"10日最大回撤":-0.0229378033,"20日最大回撤":-0.0422336931,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":1.4840579626,"10日上涨捕获率":2.7927353412,"20日上涨捕获率":3.9203007691,"30日上涨捕获率":0.7877293545,"60日上涨捕获率":0.379695167,"120日上涨捕获率":0.9055729543,"5日下跌捕获率":1.2660047975,"10日下跌捕获率":1.3691746833,"20日下跌捕获率":1.0052825156,"30日下跌捕获率":0.9302909944,"60日下跌捕获率":0.8959606856,"120日下跌捕获率":0.8692348913,"3日回归动量":-0.486726769,"5日回归动量":0.0758369094,"7日回归动量":0.0700530206,"9日回归动量":0.0013486698,"12日回归动量":0.1398089422,"15日回归动量":1.2916755895,"18日回归动量":1.7960507349,"20日回归动量":1.5218847702,"23日回归动量":1.2862250949,"25日回归动量":0.7992152975,"28日回归动量":0.4316503881,"30日回归动量":0.3257875679,"35日回归动量":0.1247554369,"40日回归动量":0.0407420044,"45日回归动量":-0.0009880942,"50日回归动量":-0.0004856153,"60日回归动量":-0.0002988375,"5日最高值到当前周期":1.0,"10日最高值到当前周期":1.0,"20日最高值到当前周期":1.0,"30日最高值到当前周期":1.0,"60日最高值到当前周期":55.0,"120日最高值到当前周期":55.0,"5日最低值到当前周期":3.0,"10日最低值到当前周期":5.0,"20日最低值到当前周期":13.0,"30日最低值到当前周期":13.0,"60日最低值到当前周期":13.0,"120日最低值到当前周期":95.0,"5日回归斜率":0.0074,"10日回归斜率":-0.0008848485,"20日回归斜率":0.0105631579,"30日回归斜率":0.0041802002,"60日回归斜率":-0.0009300361,"120日回归斜率":0.0047146573,"5日标准差":0.0197828208,"10日标准差":0.0198484256,"20日标准差":0.0760358304,"30日标准差":0.0656961355,"60日标准差":0.066616306,"120日标准差":0.1938588961,"CCI商品路径指标":37.0722032325,"MFI最近流量指标":67.3851514067,"MTM动量线_MTM值":0.127,"MTM动量线_MTMMA值":0.1545,"RSI相对强弱_RSI1":54.4806941092,"RSI相对强弱_RSI2":56.6785513436,"RSI相对强弱_RSI3":55.4083890041,"KDJ指标_K值":63.8655811587,"KDJ指标_D值":71.1845032688,"KDJ指标_J值":49.2277369384,"SKDJ慢速随机_K值":66.4517684257,"SKDJ慢速随机_D值":71.2866201103,"UDL引力线_UDL值":2.2329875,"UDL引力线_MAUDL值":2.2167333333,"WR威廉指标_WR1":59.5505617978,"WR威廉指标_WR2":49.2957746479,"LWR指标_LWR1":36.1344188413,"LWR指标_LWR2":28.8154967312,"MARSI相对强弱平均线_RSI1":62.8612255267,"MARSI相对强弱平均线_RSI2":60.9096578776,"BIAS乖离率_BIAS1":-0.0743826242,"BIAS乖离率_BIAS2":0.249990672,"BIAS乖离率_BIAS3":3.1817047178,"BIAS_QL乖离率传统版_BIAS值":-0.0743826242,"BIAS_QL乖离率传统版_BIASMA值":-0.0819790481,"BIAS36三六乖离_BIAS36":0.0183333333,"BIAS36三六乖离_BIAS612":0.00725,"BIAS36三六乖离_MABIAS":0.0001666667,"ACCER幅度涨速":0.000122291,"ASI振动升降指标_ASI":0.6969880325,"ASI振动升降指标_ASIT":0.2804643533,"CHO佳庆指标_CHO":7329.669398139,"CHO佳庆指标_MACHO":5533.3252397667,"DMA_XT平均差_DIF":0.06746,"DMA_XT平均差_DIFMA":0.008212,"DMI趋向指标_PDI":-23.9436619718,"DMI趋向指标_MDI":22.0070422535,"DMI趋向指标_ADX":-2448.697910277,"DMI趋向指标_ADXR":-7469.4878440281,"DPO区间震荡线_DPO":0.0291428571,"DPO区间震荡线_MADPO":0.097047619,"EMV简易波动指标_EMV":0.3405286754,"EMV简易波动指标_MAEMV":0.1127413398,"MACD平滑异同平均线_DIF":0.0285028224,"MACD平滑异同平均线_DEA":0.0194361069,"MACD平滑异同平均线_MACD":0.0181334311,"VMACD量平滑异同平均线_DIF":-314269.2348066347,"VMACD量平滑异同平均线_DEA":-348037.4442249978,"VMACD量平滑异同平均线_MACD":33768.2094183631,"SMACD单线平滑异同平均线_DEA":0.0194361069,"SMACD单线平滑异同平均线_MACD":0.0285028224,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.2043899432,"TRIX三重指数平均线_MATRIX":0.0894790907,"UOS终极指标_UOS":47.0747160284,"UOS终极指标_MAUOS":53.6059835267,"VTP量价曲线_VPT":22564.4318369635,"VTP量价曲线_MAVP":-150767.3704343574,"WVAD威廉变异离散量_WVAD":136.0559257957,"WVAD威廉变异离散量_MAWVAD":85.0194743072,"JS加数线_JS":0.2167042889,"JS加数线_MAJS1":-0.0416187833,"JS加数线_MAJS2":0.6570442896,"JS加数线_MAJS3":0.2648535815,"CYE市场趋势_CYEL":0.2141900937,"CYE市场趋势_CYES":0.2504502086,"GDX轨道线_轨道":0.0378532516,"GDX轨道线_压力线":0.0412600442,"GDX轨道线_支撑线":0.0344464589,"JLHB绝路航标_B":29.2111009583,"JLHB绝路航标_VAR2":27.2181849208,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":119.9084668192,"BRAR情绪指标_AR":98.0132450331,"CR带状能量线_CR":113.7526652452,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":24.3683766508,"MASS梅斯线_MAMASS":23.6581533493,"PSY心理线_PSY":58.3333333333,"PSY心理线_PSYMA":59.7222222222,"VR成交量变异率_VR":146.2211132104,"VR成交量变异率_MAVR":136.6333887382,"WAD威廉多空力度线_WAD":0.92,"WAD威廉多空力度线_MAWAD":0.8459333333,"PCNT幅度比_PCNT":-1.5631978562,"PCNT幅度比_MAPCNT":-0.1813679064,"CYR市场强弱_CYR":0.0868785525,"CYR市场强弱_MACYR":0.2022042431,"AMO成交金额_AMOW":24976.1026,"AMO成交金额_AMO1":31202.51044,"AMO成交金额_AMO2":38104.73411,"OBV累积能量线_OBV":237590015,"OBV累积能量线_MAOBV":233061719.9666666687,"VOL成交量_MAVOL1":1389694.0,"VOL成交量_MAVOL2":1694623.8999999999,"VRSI相对强弱量_RSI1":34.9158965434,"VRSI相对强弱量_RSI2":41.5964837391,"VRSI相对强弱量_RSI3":44.6731251873,"HSL换手线_HSL":1115509,"HSL换手线_MAHSL":1389694.0,"MA均线_MA1":2.2458,"MA均线_MA2":2.2482,"MA均线_MA3":2.17895,"MA均线_MA4":2.1916333333,"ACD升降线_ACD":0.92,"ACD升降线_MAACD":0.8828235897,"BBI多空均线":2.2257604167,"EXPMA指数平均线_EXP1":2.2241972596,"EXPMA指数平均线_EXP2":2.1669647696,"HMA高价平均线_HMA1":2.251,"HMA高价平均线_HMA2":2.2425833333,"HMA高价平均线_HMA3":2.1808,"HMA高价平均线_HMA4":2.2015285714,"HMA高价平均线_HMA5":2.1416333333,"LMA低价平均线_LMA1":2.2303333333,"LMA低价平均线_LMA2":2.2203333333,"LMA低价平均线_LMA3":2.1581666667,"LMA低价平均线_LMA4":2.157,"LMA低价平均线_LMA5":2.1023666667,"VMA变异平均线_VMA1":2.2407083333,"VMA变异平均线_VMA2":2.2315,"VMA变异平均线_VMA3":2.1696666667,"VMA变异平均线_VMA4":2.1804214286,"VMA变异平均线_VMA5":2.1230111111,"AMV成本均线_AMV1":2.2453754021,"AMV成本均线_AMV2":2.2265601405,"AMV成本均线_AMV3":2.1713277241,"AMV成本均线_AMV4":2.209145082,"BBIBOLL多空布林线_BBIBOLL":2.2257604167,"BBIBOLL多空布林线_UPR":2.40613311,"BBIBOLL多空布林线_DWN":2.0453877233,"ALLIGAT鳄鱼线_上唇":2.2423,"ALLIGAT鳄鱼线_牙齿":2.209375,"ALLIGAT鳄鱼线_下颚":2.1318461538,"GMMA顾比均线_MA3":2.2495083198,"GMMA顾比均线_MA5":2.2468990279,"GMMA顾比均线_MA8":2.2379416452,"GMMA顾比均线_MA10":2.2309172968,"GMMA顾比均线_MA12":2.2241972596,"GMMA顾比均线_MA15":2.2154662306,"GMMA顾比均线_MA30":2.1908578472,"GMMA顾比均线_MA35":2.1851514276,"GMMA顾比均线_MA40":2.1793628908,"GMMA顾比均线_MA45":2.1733064812,"GMMA顾比均线_MA50":2.1669647696,"GMMA顾比均线_MA60":2.1536620308,"BOLL布林线_BOLL":2.17895,"BOLL布林线_UB":2.3310216607,"BOLL布林线_LB":2.0268783393,"PBX瀑布线_PBX1":2.229527577,"PBX瀑布线_PBX2":2.2159126565,"PBX瀑布线_PBX3":2.1966630521,"PBX瀑布线_PBX4":2.1905552074,"PBX瀑布线_PBX5":2.1853671819,"PBX瀑布线_PBX6":2.1592279049,"ENE轨道线_UPPER":2.3009208,"ENE轨道线_LOWER":2.0404392,"ENE轨道线_ENE":2.17068,"MIKE麦克支撑压力_STOR":2.4478826357,"MIKE麦克支撑压力_MIDR":2.3841539004,"MIKE麦克支撑压力_WEKR":2.3204251652,"MIKE麦克支撑压力_WEKS":2.1632422087,"MIKE麦克支撑压力_MIDS":2.0697879874,"MIKE麦克支撑压力_STOS":1.9763337662,"XS薛斯通道_SUP":2.3324273405,"XS薛斯通道_SDN":2.0683789623,"XS薛斯通道_LUP":2.5330437182,"XS薛斯通道_LDN":1.9108926295,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.155273719,"MA交易_MA1":2.2458,"MA交易_MA2":2.17895,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0285028224,"MACD交易_DEA":0.0194361069,"MACD交易_MACD":0.0181334311,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":63.8655811587,"KDJ交易_D":71.1845032688,"KDJ交易_J":49.2277369384,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4737808132,"SG_XDT心电图_MQR1":0.4780905831,"SG_XDT心电图_MQR2":0.4798062486,"SG_NDB脑电波_DK":3.305,"SG_NDB脑电波_MDK1":3.2772,"SG_NDB脑电波_MDK2":3.2801,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":15.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":22335.7826157114,"LON龙系长线_LONMA":20585.8049928243,"LON龙系长线_LONT":22335.7826157114,"SHT龙系短线_SHT":2.9187849909,"SHT龙系短线_SHTMA":3.598194119,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":64.5810263557,"ZLMM主力买卖_MMM":62.4576352374,"ZLMM主力买卖_MML":53.212535293,"SLZT神龙在天_白龙":2.023976,"SLZT神龙在天_黄龙":2.3751779153,"SLZT神龙在天_紫龙":1.6497684664,"SLZT神龙在天_青龙":2.0643385081,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30018.0078115338,"ADVOL龙系离散量_MA1":29670.3887881132,"ADVOL龙系离散量_MA2":28488.8993077292,"CYS市场盈亏":0.7812398615,"CYW主力控盘":357.1521160981,"JAX济安线_J":null,"JAX济安线_A":2.2598354433,"JAX济安线_X":null,"XJDX超级短线_J":0.2445661259,"XJDX超级短线_D":0.2926293348,"XJDX超级短线_K":0.2445661259,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":3.210996733,"BDZX波段之星_AK":86.7140292765,"BDZX波段之星_AD1":88.2192838978,"BDZX波段之星_AJ":83.7035200338,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":-0.0343630606,"LHXJ猎狐先觉_主力控盘":0.0343630606,"LYJH猎鹰歼狐_机构做空能量线":16.6644814644,"LYJH猎鹰歼狐_机构做多能量线":58.8810177372,"JFZX飓风智能中线_多头力量":52.9547045539,"JFZX飓风智能中线_空头力量":47.0452954461,"CYHT财运亨通_SK":68.9183898521,"CYHT财运亨通_SD":66.0626943584,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":2.239,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":null,"CDP_STD逆势操作_CDP":2.27,"CDP_STD逆势操作_AH":2.29,"CDP_STD逆势操作_NH":2.278,"CDP_STD逆势操作_NL":2.266,"CDP_STD逆势操作_AL":2.254,"Alpha001":0.0678457298,"Alpha002":1.2307692308,"Alpha003":-21.998,"Alpha004":-1,"Alpha005":-0.8660254038,"Alpha006":-0.7080062794,"Alpha007":0.947321687,"Alpha008":-0.6279434851,"Alpha009":-0.0,"Alpha010":0.9805825243,"Alpha011":997029.8970918062,"Alpha012":-0.0061711329,"Alpha013":-221.658219345,"Alpha014":0.024,"Alpha015":-0.0136323659,"Alpha016":-0.8838304553,"Alpha017":0.9789138024,"Alpha018":1.0108352144,"Alpha019":-0.0108352144,"Alpha020":-0.9730207873,"Alpha021":0.0025857143,"Alpha022":0.0002644901,"Alpha023":52.8512305767,"Alpha024":0.0289121138,"Alpha025":-0.2867253536,"Alpha026":0.9307506807,"Alpha027":285.8116100212,"Alpha028":31.4235856922,"Alpha029":-10854.1344537816,"Alpha030":0.0002577132,"Alpha031":0.249990672,"Alpha032":-2.323943662,"Alpha033":0.0015135725,"Alpha034":0.9975063272,"Alpha035":-0.8178913738,"Alpha036":0.7198748044,"Alpha037":0.5014009997,"Alpha038":0.018,"Alpha039":-0.3400936037,"Alpha040":127.5214400609,"Alpha041":-0.7232704403,"Alpha042":-0.1988343233,"Alpha043":1500223.0,"Alpha044":1.3333333333,"Alpha045":0.003034942,"Alpha046":0.9940868319,"Alpha047":42.2731025555,"Alpha048":-0.1439423107,"Alpha049":0.2947368421,"Alpha050":0.4105263158,"Alpha051":0.7052631579,"Alpha052":117.0965364775,"Alpha053":58.3333333333,"Alpha054":-0.0996835443,"Alpha055":1.6636476073,"Alpha056":-0.7750915751,"Alpha057":52.0190802414,"Alpha058":55.0,"Alpha059":0.12,"Alpha060":4124164.6742921076,"Alpha061":-0.6021840874,"Alpha062":-0.7939203982,"Alpha063":54.4806941092,"Alpha064":-0.9407176287,"Alpha065":1.0007443799,"Alpha066":-0.0743826242,"Alpha067":55.4083890041,"Alpha068":0.0,"Alpha069":-0.8269230769,"Alpha070":63047355.8492230251,"Alpha071":3.1817047178,"Alpha072":45.2910209271,"Alpha073":-0.7900207901,"Alpha074":0.887675507,"Alpha075":0.3461538462,"Alpha076":0.8248912459,"Alpha077":0.0249609984,"Alpha078":7.4389365464,"Alpha079":56.6785513436,"Alpha080":-41.7900953685,"Alpha081":1737771.5357780196,"Alpha082":46.4736356596,"Alpha083":-0.4850863422,"Alpha084":6905108.0,"Alpha085":0.45,"Alpha086":1.0,"Alpha087":-0.8083351906,"Alpha088":5.117370892,"Alpha089":0.0181334311,"Alpha090":-0.8845553822,"Alpha091":-0.0616340182,"Alpha092":-0.5850234009,"Alpha093":0.116,"Alpha094":8972134.0,"Alpha095":81322401.8086434007,"Alpha096":62.316827516,"Alpha097":361843.7384658459,"Alpha098":-0.013,"Alpha099":-0.546310832,"Alpha100":338879.8597104504,"Alpha101":-0.5741029641,"Alpha102":34.9158965434,"Alpha103":35.0,"Alpha104":-0.4315296104,"Alpha105":-0.4950604178,"Alpha106":0.109,"Alpha107":-0.0003981667,"Alpha108":-0.0637628154,"Alpha109":0.8632029923,"Alpha110":148.3552631579,"Alpha111":-52305.9838007248,"Alpha112":36.8115942029,"Alpha113":-0.4846512737,"Alpha114":264.757850846,"Alpha115":0.6814312185,"Alpha116":0.0103142857,"Alpha117":0.0346069336,"Alpha118":103.2110091743,"Alpha119":0.2839313573,"Alpha120":0.9801979068,"Alpha121":-0.9519680378,"Alpha122":0.0026251056,"Alpha123":-0.4320159782,"Alpha124":-79.8672704083,"Alpha125":0.406462585,"Alpha126":2.24,"Alpha127":1.1301253708,"Alpha128":67.3851514067,"Alpha129":0.109,"Alpha130":0.2740740741,"Alpha131":0.8606205071,"Alpha132":342015632.8500000238,"Alpha133":35.0,"Alpha134":67078.4294507575,"Alpha135":1.0132768498,"Alpha136":-0.0771613594,"Alpha137":-0.3085714286,"Alpha138":-0.7728994874,"Alpha139":-0.4130402181,"Alpha140":0.3333333333,"Alpha141":-0.6962843296,"Alpha142":-0.0030190153,"Alpha143":0.0044169611,"Alpha144":0.0,"Alpha145":-10.0181962889,"Alpha146":-5.6885493538,"Alpha147":0.0107619464,"Alpha148":-0.6510122239,"Alpha149":0.867939238,"Alpha150":2498740.1599999997,"Alpha151":0.0287361793,"Alpha152":-0.0013923681,"Alpha153":2.2257604167,"Alpha154":-20.6674882794,"Alpha155":33768.2094183631,"Alpha156":-0.4789391576,"Alpha157":1.2307086614,"Alpha158":0.0058061635,"Alpha159":-5699.4375680026,"Alpha160":0.0268889801,"Alpha161":0.0375833333,"Alpha162":0.3988776955,"Alpha163":0.8221528861,"Alpha164":222119.6789688597,"Alpha165":-15.5852300868,"Alpha166":-0.0024113432,"Alpha167":0.236,"Alpha168":-0.7130952152,"Alpha169":0.0016334869,"Alpha170":-0.5127303863,"Alpha171":-0.6306028328,"Alpha172":34.7129144958,"Alpha173":3.0664413047,"Alpha174":0.0301410981,"Alpha175":0.0313333333,"Alpha176":0.2214664508,"Alpha177":70.0,"Alpha178":-17169.2238346527,"Alpha179":0.2704140615,"Alpha180":-1115509.0,"Alpha181":0.0089126903,"Alpha182":0.65,"Alpha183":14.7389256928,"Alpha184":0.7269890796,"Alpha185":-0.0000031916,"Alpha186":30.1647398686,"Alpha187":0.4,"Alpha188":-35.4232174999,"Alpha189":0.0187222222,"Alpha190":-0.4803529679,"Alpha191":-0.6161860274},{"date":"2026-08-19","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.197,"high":2.2,"low":2.185,"close":2.2,"volume":1618804,"amount":354981207.0,"5日涨跌幅":-1.1680143756,"10日涨跌幅":-2.9554477283,"20日涨跌幅":3.2863849765,"30日涨跌幅":2.7557216254,"60日涨跌幅":0.6864988558,"120日涨跌幅":20.5479452055,"六脉神剑":0,"小波段交易":false,"大波段交易":true,"波段超级买卖":false,"价格距离5日均线涨跌幅":-1.8120146389,"价格距离10日均线涨跌幅":-1.8514387687,"价格距离20日均线涨跌幅":0.8041421338,"价格距离30日均线涨跌幅":1.3124568271,"价格距离60日均线涨跌幅":0.3703055972,"价格距离120日均线涨跌幅":8.1089935217,"5日均线距离10日均线涨跌幅":-0.0401516841,"10日均线距离20日均线涨跌幅":2.705674815,"20日均线距离30日均线涨跌幅":0.5042597283,"30日均线距离60日均线涨跌幅":-0.929946089,"60日均线距离120日均线涨跌幅":7.7101368562,"5日偏度":-0.3177220123,"10日偏度":-0.2759354352,"20日偏度":-0.4322744353,"30日偏度":-0.0612691202,"60日偏度":0.1753320941,"120日偏度":-0.4085714023,"5日峰度":-1.0764695978,"10日峰度":-1.1069888804,"20日峰度":-1.3262453435,"30日峰度":-1.0386662249,"60日峰度":-0.1220273652,"120日峰度":-1.277430503,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.2406,"10日均线":2.2415,"20日均线":2.18245,"30日均线":2.1715,"60日均线":2.1918833333,"120日均线":2.0349833333,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":1.0,"连续下跌天数":0.0,"价格在5均线上":false,"价格在10均线上":false,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":0.0300026198,"10日Alpha":-0.3895131028,"20日Alpha":1.1612163378,"30日Alpha":0.5368351143,"60日Alpha":0.3252388306,"120日Alpha":0.5997026422,"5日Beta":0.5551152781,"10日Beta":0.6749639299,"20日Beta":0.9996990609,"30日Beta":0.6423415414,"60日Beta":0.7341975551,"120日Beta":0.8627394878,"5日夏普比率":-2.5020661594,"10日夏普比率":-3.7119612219,"20日夏普比率":1.5985866075,"30日夏普比率":1.0321581021,"60日夏普比率":0.2419874595,"120日夏普比率":1.5226654411,"5日年化波动率":0.2280616394,"10日年化波动率":0.1985671274,"20日年化波动率":0.2778491098,"30日年化波动率":0.2506093637,"60日年化波动率":0.2954795289,"120日年化波动率":0.2840323827,"5日最大回撤":-0.0325417766,"10日最大回撤":-0.0325417766,"20日最大回撤":-0.0422336931,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":1.985498162,"10日上涨捕获率":1.0498024795,"20日上涨捕获率":3.9203007691,"30日上涨捕获率":0.7877293545,"60日上涨捕获率":0.4769190206,"120日上涨捕获率":0.9252728094,"5日下跌捕获率":0.9765768577,"10日下跌捕获率":1.0533303658,"20日下跌捕获率":0.9936173606,"30日下跌捕获率":0.9268579924,"60日下跌捕获率":0.9023156096,"120日下跌捕获率":0.8731660404,"3日回归动量":-0.9837271116,"5日回归动量":-0.2282325225,"7日回归动量":0.007651555,"9日回归动量":-0.0292781417,"12日回归动量":-0.0005976624,"15日回归动量":0.3304568338,"18日回归动量":0.9778335903,"20日回归动量":1.0492402093,"23日回归动量":0.9703245113,"25日回归动量":0.7918548809,"28日回归动量":0.4330370894,"30日回归动量":0.3042857934,"35日回归动量":0.1535068729,"40日回归动量":0.0494237213,"45日回归动量":0.0028753412,"50日回归动量":0.0000403615,"60日回归动量":-0.0001707581,"5日最高值到当前周期":2.0,"10日最高值到当前周期":2.0,"20日最高值到当前周期":2.0,"30日最高值到当前周期":2.0,"60日最高值到当前周期":56.0,"120日最高值到当前周期":56.0,"5日最低值到当前周期":0.0,"10日最低值到当前周期":0.0,"20日最低值到当前周期":14.0,"30日最低值到当前周期":14.0,"60日最低值到当前周期":14.0,"120日最低值到当前周期":96.0,"5日回归斜率":-0.0077,"10日回归斜率":-0.0022606061,"20日回归斜率":0.0100909774,"30日回归斜率":0.0041799778,"60日回归斜率":-0.0009275632,"120日回归斜率":0.004697222,"5日标准差":0.0265601205,"10日标准差":0.0233677128,"20日标准差":0.0753096773,"30日标准差":0.0656956366,"60日标准差":0.0666190893,"120日标准差":0.193521359,"CCI商品路径指标":-44.9853943525,"MFI最近流量指标":65.6573175349,"MTM动量线_MTM值":0.073,"MTM动量线_MTMMA值":0.1481666667,"RSI相对强弱_RSI1":41.7951414228,"RSI相对强弱_RSI2":50.0312614948,"RSI相对强弱_RSI3":52.1806408261,"KDJ指标_K值":47.2499513021,"KDJ指标_D值":63.2063192799,"KDJ指标_J值":15.3372153464,"SKDJ慢速随机_K值":51.3181549526,"SKDJ慢速随机_D值":64.1076896198,"UDL引力线_UDL值":2.2255541667,"UDL引力线_MAUDL值":2.2197534722,"WR威廉指标_WR1":85.9813084112,"WR威廉指标_WR2":83.1460674157,"LWR指标_LWR1":52.7500486979,"LWR指标_LWR2":36.7936807201,"MARSI相对强弱平均线_RSI1":60.7393499495,"MARSI相对强弱平均线_RSI2":58.6168214341,"BIAS乖离率_BIAS1":-1.7052647256,"BIAS乖离率_BIAS2":-1.7637865595,"BIAS乖离率_BIAS3":1.3202333436,"BIAS_QL乖离率传统版_BIAS值":-1.7052647256,"BIAS_QL乖离率传统版_BIASMA值":-0.1740490151,"BIAS36三六乖离_BIAS36":-0.0005,"BIAS36三六乖离_BIAS612":-0.0013333333,"BIAS36三六乖离_MABIAS":-0.001,"ACCER幅度涨速":-0.0006764069,"ASI振动升降指标_ASI":0.2510097868,"ASI振动升降指标_ASIT":0.3773454353,"CHO佳庆指标_CHO":6706.5239449616,"CHO佳庆指标_MACHO":6226.9484813695,"DMA_XT平均差_DIF":0.06076,"DMA_XT平均差_DIFMA":0.020144,"DMI趋向指标_PDI":-26.9296740995,"DMI趋向指标_MDI":25.7289879931,"DMI趋向指标_ADX":-2798.5391801183,"DMI趋向指标_ADXR":-6309.9640345041,"DPO区间震荡线_DPO":-0.0245714286,"DPO区间震荡线_MADPO":0.072452381,"EMV简易波动指标_EMV":0.3562461941,"EMV简易波动指标_MAEMV":0.1480167651,"MACD平滑异同平均线_DIF":0.0244612365,"MACD平滑异同平均线_DEA":0.0204411328,"MACD平滑异同平均线_MACD":0.0080402074,"VMACD量平滑异同平均线_DIF":-287506.8860999462,"VMACD量平滑异同平均线_DEA":-335931.3325999875,"VMACD量平滑异同平均线_MACD":48424.4465000413,"SMACD单线平滑异同平均线_DEA":0.0204411328,"SMACD单线平滑异同平均线_MACD":0.0244612365,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.2070390313,"TRIX三重指数平均线_MATRIX":0.1213304967,"UOS终极指标_UOS":48.2530661262,"UOS终极指标_MAUOS":52.0765785551,"VTP量价曲线_VPT":288582.9797488015,"VTP量价曲线_MAVP":-92949.080037201,"WVAD威廉变异离散量_WVAD":181.1140391291,"WVAD威廉变异离散量_MAWVAD":115.0497109314,"JS加数线_JS":-0.2336028751,"JS加数线_MAJS1":-0.0159970557,"JS加数线_MAJS2":0.4475702124,"JS加数线_MAJS3":0.2796816644,"CYE市场趋势_CYEL":-0.2315433253,"CYE市场趋势_CYES":0.2646015738,"GDX轨道线_轨道":0.0246254515,"GDX轨道线_压力线":0.0268417421,"GDX轨道线_支撑线":0.0224091609,"JLHB绝路航标_B":28.5172641846,"JLHB绝路航标_VAR2":27.4780007735,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":113.5076252723,"BRAR情绪指标_AR":97.2696245734,"CR带状能量线_CR":108.7755102041,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":24.5552433106,"MASS梅斯线_MAMASS":23.9580482374,"PSY心理线_PSY":50.0,"PSY心理线_PSYMA":58.3333333333,"VR成交量变异率_VR":120.837616765,"VR成交量变异率_MAVR":137.6379311712,"WAD威廉多空力度线_WAD":0.881,"WAD威廉多空力度线_MAWAD":0.8488,"PCNT幅度比_PCNT":-1.7727272727,"PCNT幅度比_MAPCNT":-0.7118210285,"CYR市场强弱_CYR":-0.1876899275,"CYR市场强弱_MACYR":0.1434959911,"AMO成交金额_AMOW":35498.1207,"AMO成交金额_AMO1":32236.55928,"AMO成交金额_AMO2":36561.62205,"OBV累积能量线_OBV":235971211,"OBV累积能量线_MAOBV":233370502.3666666746,"VOL成交量_MAVOL1":1440289.3999999999,"VOL成交量_MAVOL2":1631064.8,"VRSI相对强弱量_RSI1":51.5402617224,"VRSI相对强弱量_RSI2":47.9230386437,"VRSI相对强弱量_RSI3":46.9286662971,"HSL换手线_HSL":1618804,"HSL换手线_MAHSL":1440289.3999999999,"MA均线_MA1":2.2406,"MA均线_MA2":2.2415,"MA均线_MA3":2.18245,"MA均线_MA4":2.1918833333,"ACD升降线_ACD":0.881,"ACD升降线_MAACD":0.8826499145,"BBI多空均线":2.2216666667,"EXPMA指数平均线_EXP1":2.2204746042,"EXPMA指数平均线_EXP2":2.1682602688,"HMA高价平均线_HMA1":2.2435,"HMA高价平均线_HMA2":2.24825,"HMA高价平均线_HMA3":2.182,"HMA高价平均线_HMA4":2.2029285714,"HMA高价平均线_HMA5":2.1457111111,"LMA低价平均线_LMA1":2.2258333333,"LMA低价平均线_LMA2":2.2261666667,"LMA低价平均线_LMA3":2.1596666667,"LMA低价平均线_LMA4":2.1585,"LMA低价平均线_LMA5":2.1068666667,"VMA变异平均线_VMA1":2.2355,"VMA变异平均线_VMA2":2.2376041667,"VMA变异平均线_VMA3":2.1711333333,"VMA变异平均线_VMA4":2.181925,"VMA变异平均线_VMA5":2.1272638889,"AMV成本均线_AMV1":2.2399355316,"AMV成本均线_AMV2":2.2335203324,"AMV成本均线_AMV3":2.1717933392,"AMV成本均线_AMV4":2.2090805876,"BBIBOLL多空布林线_BBIBOLL":2.2216666667,"BBIBOLL多空布林线_UPR":2.3557810846,"BBIBOLL多空布林线_DWN":2.0875522487,"ALLIGAT鳄鱼线_上唇":2.2423,"ALLIGAT鳄鱼线_牙齿":2.222375,"ALLIGAT鳄鱼线_下颚":2.1425769231,"GMMA顾比均线_MA3":2.2247541599,"GMMA顾比均线_MA5":2.2312660186,"GMMA顾比均线_MA8":2.2295101685,"GMMA顾比均线_MA10":2.2252959701,"GMMA顾比均线_MA12":2.2204746042,"GMMA顾比均线_MA15":2.2135329518,"GMMA顾比均线_MA30":2.1914476635,"GMMA顾比均线_MA35":2.1859763483,"GMMA顾比均线_MA40":2.1803695791,"GMMA顾比均线_MA45":2.174467069,"GMMA顾比均线_MA50":2.1682602688,"GMMA顾比均线_MA60":2.1551813085,"BOLL布林线_BOLL":2.18245,"BOLL布林线_UB":2.3330693547,"BOLL布林线_LB":2.0318306453,"PBX瀑布线_PBX1":2.2230332129,"PBX瀑布线_PBX2":2.2141737229,"PBX瀑布线_PBX3":2.1961082195,"PBX瀑布线_PBX4":2.1899035478,"PBX瀑布线_PBX5":2.1856577222,"PBX瀑布线_PBX6":2.1615841169,"ENE轨道线_UPPER":2.3014296,"ENE轨道线_LOWER":2.0408904,"ENE轨道线_ENE":2.17116,"MIKE麦克支撑压力_STOR":2.4280633873,"MIKE麦克支撑压力_MIDR":2.3741293991,"MIKE麦克支撑压力_WEKR":2.3201954108,"MIKE麦克支撑压力_WEKS":2.1834181504,"MIKE麦克支撑压力_MIDS":2.1005748782,"MIKE麦克支撑压力_STOS":2.017731606,"XS薛斯通道_SUP":2.3352588805,"XS薛斯通道_SDN":2.0708899506,"XS薛斯通道_LUP":2.5351636268,"XS薛斯通道_LDN":1.9124918588,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1662118215,"MA交易_MA1":2.2406,"MA交易_MA2":2.18245,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0244612365,"MACD交易_DEA":0.0204411328,"MACD交易_MACD":0.0080402074,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":47.2499513021,"KDJ交易_D":63.2063192799,"KDJ交易_J":15.3372153464,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4794390389,"SG_XDT心电图_MQR1":0.4790715539,"SG_XDT心电图_MQR2":0.4790828153,"SG_NDB脑电波_DK":3.305,"SG_NDB脑电波_MDK1":3.291,"SG_NDB脑电波_MDK2":3.2806,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":20.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":21281.0621785354,"LON龙系长线_LONMA":20826.6512013048,"LON龙系长线_LONT":21281.0621785354,"SHT龙系短线_SHT":1.4061236234,"SHT龙系短线_SHTMA":3.2982195539,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":58.1459101614,"ZLMM主力买卖_MMM":61.4994741094,"ZLMM主力买卖_MML":53.5305337106,"SLZT神龙在天_白龙":2.026824,"SLZT神龙在天_黄龙":2.3794428059,"SLZT神龙在天_紫龙":1.6515128274,"SLZT神龙在天_青龙":2.068891738,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30179.8882115338,"ADVOL龙系离散量_MA1":29694.0183630211,"ADVOL龙系离散量_MA2":28514.1360240668,"CYS市场盈亏":-0.7880062782,"CYW主力控盘":318.6418494314,"JAX济安线_J":null,"JAX济安线_A":2.2277249334,"JAX济安线_X":null,"XJDX超级短线_J":0.0267283447,"XJDX超级短线_D":0.2000387428,"XJDX超级短线_K":0.0267283447,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":1.9362659419,"BDZX波段之星_AK":76.2303986841,"BDZX波段之星_AD1":80.2266937554,"BDZX波段之星_AJ":68.2378085417,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":-0.0023158269,"LHXJ猎狐先觉_主力控盘":0.0023158269,"LYJH猎鹰歼狐_机构做空能量线":26.231073417,"LYJH猎鹰歼狐_机构做多能量线":48.3085525075,"JFZX飓风智能中线_多头力量":56.2142983505,"JFZX飓风智能中线_空头力量":43.7857016495,"CYHT财运亨通_SK":68.0445565047,"CYHT财运亨通_SD":67.0536254315,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":null,"BSQJ买卖区间_S卖":2.2,"BSQJ买卖区间_空仓":2.2,"CDP_STD逆势操作_CDP":2.24,"CDP_STD逆势操作_AH":2.259,"CDP_STD逆势操作_NH":2.246,"CDP_STD逆势操作_NL":2.233,"CDP_STD逆势操作_AL":2.22,"Alpha001":-0.0834906414,"Alpha002":-1.2307692308,"Alpha003":-21.998,"Alpha004":1,"Alpha005":-0.8660254038,"Alpha006":-0.2064364207,"Alpha007":0.9829450405,"Alpha008":-0.1177394035,"Alpha009":-0.0000000002,"Alpha010":0.9805825243,"Alpha011":4183761.5334554287,"Alpha012":-0.0090345386,"Alpha013":-217.0936073767,"Alpha014":-0.026,"Alpha015":-0.0187583743,"Alpha016":-0.8838304553,"Alpha017":1.0478185658,"Alpha018":0.9883198562,"Alpha019":-0.0116801438,"Alpha020":-0.6772009029,"Alpha021":-0.0001142857,"Alpha022":-0.0019588098,"Alpha023":49.333418565,"Alpha024":0.017929691,"Alpha025":-0.1094404463,"Alpha026":0.9608928729,"Alpha027":172.8746009757,"Alpha028":-2.1705340902,"Alpha029":-10962.5553047404,"Alpha030":0.0002604489,"Alpha031":-1.7637865595,"Alpha032":-1.8435054773,"Alpha033":0.0119288612,"Alpha034":1.0179545455,"Alpha035":-0.3610223642,"Alpha036":0.613458529,"Alpha037":1.0982675756,"Alpha038":0.074,"Alpha039":0.0343213729,"Alpha040":105.2910354733,"Alpha041":-0.7232704403,"Alpha042":-0.2062981189,"Alpha043":1797775.0,"Alpha044":1.2666666667,"Alpha045":0.0060844867,"Alpha046":1.0098484848,"Alpha047":46.8145430956,"Alpha048":-0.0610013681,"Alpha049":0.3870192308,"Alpha050":0.2259615385,"Alpha051":0.6129807692,"Alpha052":111.5411681914,"Alpha053":50.0,"Alpha054":-0.2088607595,"Alpha055":1.0550341221,"Alpha056":-0.2405372405,"Alpha057":34.6793868276,"Alpha058":55.0,"Alpha059":0.081,"Alpha060":7022948.0076254429,"Alpha061":-0.3900156006,"Alpha062":0.0641578235,"Alpha063":41.7951414228,"Alpha064":-0.7691107644,"Alpha065":1.0173484848,"Alpha066":-1.7052647256,"Alpha067":52.1806408261,"Alpha068":-0.0000000001,"Alpha069":-0.8,"Alpha070":45604019.5078074038,"Alpha071":1.3202333436,"Alpha072":47.8146906931,"Alpha073":-0.3884605417,"Alpha074":0.7488299532,"Alpha075":0.3703703704,"Alpha076":0.7436194008,"Alpha077":0.0202808112,"Alpha078":-39.798051259,"Alpha079":50.0312614948,"Alpha080":18.5218918648,"Alpha081":1726441.2942753511,"Alpha082":48.3072572474,"Alpha083":-0.4332810047,"Alpha084":5286304.0,"Alpha085":0.9,"Alpha086":1.0,"Alpha087":-0.4798306218,"Alpha088":3.2863849765,"Alpha089":0.0080402074,"Alpha090":-0.4992199688,"Alpha091":-0.0365425306,"Alpha092":-0.4,"Alpha093":0.128,"Alpha094":9263472.0,"Alpha095":80623760.7715218365,"Alpha096":53.1043472865,"Alpha097":303751.616459375,"Alpha098":0.064,"Alpha099":-0.5086342229,"Alpha100":333884.4466828952,"Alpha101":-0.5678627145,"Alpha102":51.5402617224,"Alpha103":30.0,"Alpha104":0.6784102142,"Alpha105":-0.3377492412,"Alpha106":0.07,"Alpha107":-0.0000259552,"Alpha108":-0.0223441903,"Alpha109":0.8519485742,"Alpha110":120.9039548023,"Alpha111":-440225.72991894,"Alpha112":19.783197832,"Alpha113":0.1927565402,"Alpha114":575.7050787494,"Alpha115":0.8673025591,"Alpha116":0.0105631579,"Alpha117":0.2255859375,"Alpha118":98.6175115207,"Alpha119":0.3884555382,"Alpha120":0.980134193,"Alpha121":-0.6134811579,"Alpha122":0.0026610811,"Alpha123":-0.425463199,"Alpha124":-78.2193291769,"Alpha125":0.3865384615,"Alpha126":2.195,"Alpha127":1.4685775206,"Alpha128":65.6573175349,"Alpha129":0.148,"Alpha130":0.5298165138,"Alpha131":0.4463616407,"Alpha132":340287933.0,"Alpha133":35.0,"Alpha134":55558.3883403854,"Alpha135":1.0151716928,"Alpha136":-0.0129486404,"Alpha137":-0.4812885906,"Alpha138":-0.6980164921,"Alpha139":-0.2844235833,"Alpha140":0.3333333333,"Alpha141":-0.633279483,"Alpha142":-0.0225673078,"Alpha143":-0.0153913808,"Alpha144":0.0,"Alpha145":-8.7979848433,"Alpha146":-2.8170141281,"Alpha147":0.0117581585,"Alpha148":-0.1929704029,"Alpha149":0.8556020201,"Alpha150":3553274.7800000003,"Alpha151":0.0307993704,"Alpha152":0.0002984291,"Alpha153":2.2216666667,"Alpha154":-15.9615513927,"Alpha155":48424.4465000413,"Alpha156":-0.8923556942,"Alpha157":1.4307086614,"Alpha158":0.0068181818,"Alpha159":-5490.0080535697,"Alpha160":0.029407836,"Alpha161":0.0404166667,"Alpha162":0.0,"Alpha163":0.4836193448,"Alpha164":187947.4206659582,"Alpha165":-14.3155394103,"Alpha166":-0.0013177524,"Alpha167":0.221,"Alpha168":-1.0414908724,"Alpha169":0.002119904,"Alpha170":-0.2136565462,"Alpha171":100.0,"Alpha172":36.2180174016,"Alpha173":3.0476335872,"Alpha174":0.0286340432,"Alpha175":0.0321666667,"Alpha176":-0.0375561601,"Alpha177":65.0,"Alpha178":-28197.1219294326,"Alpha179":0.2655756776,"Alpha180":0.5333333333,"Alpha181":0.0089068203,"Alpha182":0.65,"Alpha183":14.7467785191,"Alpha184":0.5343213729,"Alpha185":-0.0000018595,"Alpha186":32.0241843581,"Alpha187":0.366,"Alpha188":-21.8674781855,"Alpha189":0.0207777778,"Alpha190":-0.4913546732,"Alpha191":0.4029718584},{"date":"2026-08-20","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.217,"high":2.223,"low":2.21,"close":2.212,"volume":861635,"amount":190993874.0,"5日涨跌幅":-0.6289308176,"10日涨跌幅":-1.4260249554,"20日涨跌幅":3.8010323792,"30日涨跌幅":2.1237303786,"60日涨跌幅":-0.4948268106,"120日涨跌幅":20.7423580786,"六脉神剑":0,"小波段交易":false,"大波段交易":true,"波段超级买卖":false,"价格距离5日均线涨跌幅":-1.1529180445,"价格距离10日均线涨跌幅":-1.1749988831,"价格距离20日均线涨跌幅":1.1662474274,"价格距离30日均线涨跌幅":1.7931923118,"价格距离60日均线涨跌幅":0.9262216544,"价格距离120日均线涨跌幅":8.5297941761,"5日均线距离10日均线涨跌幅":-0.0223383818,"10日均线距离20日均线涨跌幅":2.3690830094,"20日均线距离30日均线涨跌幅":0.6197174457,"30日均线距离60日均线涨跌幅":-0.851698073,"60日均线距离120日均线涨跌幅":7.5337929004,"5日偏度":-0.0733189361,"10日偏度":0.035764288,"20日偏度":-0.5999885498,"30日偏度":-0.1254287267,"60日偏度":0.1830947803,"120日偏度":-0.4436078776,"5日峰度":-2.4204978891,"10日峰度":-1.6517183385,"20日峰度":-1.1212404973,"30日峰度":-1.0774783551,"60日峰度":-0.107710322,"120日峰度":-1.2447279704,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.2378,"10日均线":2.2383,"20日均线":2.1865,"30日均线":2.1730333333,"60日均线":2.1917,"120日均线":2.03815,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":0.0,"连续下跌天数":1.0,"价格在5均线上":false,"价格在10均线上":false,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":0.1478651851,"10日Alpha":-0.1281570594,"20日Alpha":1.3469897303,"30日Alpha":0.6848264296,"60日Alpha":0.2299089876,"120日Alpha":0.597098745,"5日Beta":0.5805613201,"10日Beta":0.6842444725,"20日Beta":1.0064121311,"30日Beta":0.6679511192,"60日Beta":0.7456908794,"120日Beta":0.8631720316,"5日夏普比率":-1.2601609581,"10日夏普比率":-1.7360257571,"20日夏普比率":1.8229736349,"30日夏普比率":0.8290723596,"60日夏普比率":0.0727955145,"120日夏普比率":1.5344444982,"5日年化波动率":0.2346654349,"10日年化波动率":0.1981253135,"20日年化波动率":0.2781047602,"30日年化波动率":0.2489549405,"60日年化波动率":0.293533926,"120日年化波动率":0.284067651,"5日最大回撤":-0.0325417766,"10日最大回撤":-0.0325417766,"20日最大回撤":-0.0422336931,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":2.5906011098,"10日上涨捕获率":1.3311735646,"20日上涨捕获率":4.5790471839,"30日上涨捕获率":1.0872044483,"60日上涨捕获率":0.5078759992,"120日上涨捕获率":0.9460196229,"5日下跌捕获率":1.0008344479,"10日下跌捕获率":1.0200693867,"20日下跌捕获率":0.9936173606,"30日下跌捕获率":0.9268579924,"60日下跌捕获率":0.9265579973,"120日下跌捕获率":0.8794390853,"3日回归动量":-0.1768054864,"5日回归动量":-0.6608426744,"7日回归动量":-0.1140078779,"9日回归动量":-0.0447927469,"12日回归动量":-0.0829467812,"15日回归动量":0.0302536399,"18日回归动量":0.5636367756,"20日回归动量":0.7541794843,"23日回归动量":0.7341184545,"25日回归动量":0.7678175363,"28日回归动量":0.4447043176,"30日回归动量":0.3193035182,"35日回归动量":0.1651968742,"40日回归动量":0.0677539707,"45日回归动量":0.0113772328,"50日回归动量":0.000058503,"60日回归动量":-0.0000096512,"5日最高值到当前周期":3.0,"10日最高值到当前周期":3.0,"20日最高值到当前周期":3.0,"30日最高值到当前周期":3.0,"60日最高值到当前周期":57.0,"120日最高值到当前周期":57.0,"5日最低值到当前周期":1.0,"10日最低值到当前周期":1.0,"20日最低值到当前周期":15.0,"30日最低值到当前周期":15.0,"60日最低值到当前周期":15.0,"120日最低值到当前周期":97.0,"5日回归斜率":-0.0178,"10日回归斜率":-0.0037030303,"20日回归斜率":0.0097007519,"30日回归斜率":0.004403337,"60日回归斜率":-0.000841845,"120日回归斜率":0.0046850823,"5日标准差":0.0286104876,"10日标准差":0.0249441376,"20日标准差":0.0746086456,"30日标准差":0.0660850378,"60日标准差":0.0665483033,"120日标准差":0.1932828519,"CCI商品路径指标":-29.7826752372,"MFI最近流量指标":64.5110933601,"MTM动量线_MTM值":0.02,"MTM动量线_MTMMA值":0.1335,"RSI相对强弱_RSI1":46.4030584885,"RSI相对强弱_RSI2":51.9238691111,"RSI相对强弱_RSI3":53.0586116746,"KDJ指标_K值":39.911182488,"KDJ指标_D值":55.4412736826,"KDJ指标_J值":8.8510000987,"SKDJ慢速随机_K值":41.0136240611,"SKDJ慢速随机_D值":52.9278491465,"UDL引力线_UDL值":2.2199,"UDL引力线_MAUDL值":2.2220159722,"WR威廉指标_WR1":74.7663551402,"WR威廉指标_WR2":69.6629213483,"LWR指标_LWR1":60.088817512,"LWR指标_LWR2":44.5587263174,"MARSI相对强弱平均线_RSI1":59.3372977042,"MARSI相对强弱平均线_RSI2":56.6267440763,"BIAS乖离率_BIAS1":-1.0659709281,"BIAS乖离率_BIAS2":-1.301405518,"BIAS乖离率_BIAS3":1.6680391443,"BIAS_QL乖离率传统版_BIAS值":-1.0659709281,"BIAS_QL乖离率传统版_BIASMA值":-0.1996224026,"BIAS36三六乖离_BIAS36":-0.0188333333,"BIAS36三六乖离_BIAS612":-0.0053333333,"BIAS36三六乖离_MABIAS":-0.0020555556,"ACCER幅度涨速":-0.0005489538,"ASI振动升降指标_ASI":0.1796097595,"ASI振动升降指标_ASIT":0.4693114068,"CHO佳庆指标_CHO":5521.9030369131,"CHO佳庆指标_MACHO":6449.8339007797,"DMA_XT平均差_DIF":0.05618,"DMA_XT平均差_DIFMA":0.03053,"DMI趋向指标_PDI":-29.7348484848,"DMI趋向指标_MDI":28.4090909091,"DMI趋向指标_ADX":-3216.3336663338,"DMI趋向指标_ADXR":-5150.4402249801,"DPO区间震荡线_DPO":-0.0267142857,"DPO区间震荡线_MADPO":0.0477619048,"EMV简易波动指标_EMV":0.3110149954,"EMV简易波动指标_MAEMV":0.1641402379,"MACD平滑异同平均线_DIF":0.0219732563,"MACD平滑异同平均线_DEA":0.0207475575,"MACD平滑异同平均线_MACD":0.0024513975,"VMACD量平滑异同平均线_DIF":-323663.7480978405,"VMACD量平滑异同平均线_DEA":-333477.8156995581,"VMACD量平滑异同平均线_MACD":9814.0676017177,"SMACD单线平滑异同平均线_DEA":0.0207475575,"SMACD单线平滑异同平均线_MACD":0.0219732563,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.2024890865,"TRIX三重指数平均线_MATRIX":0.14642694,"UOS终极指标_UOS":52.1201555884,"UOS终极指标_MAUOS":52.0890291361,"VTP量价曲线_VPT":10716.8297272986,"VTP量价曲线_MAVP":-32049.9812740795,"WVAD威廉变异离散量_WVAD":415.1542501868,"WVAD威廉变异离散量_MAWVAD":187.1325086518,"JS加数线_JS":-0.1257861635,"JS加数线_MAJS1":-0.0090687269,"JS加数线_MAJS2":0.236069499,"JS加数线_MAJS3":0.2900051851,"CYE市场趋势_CYEL":-0.1249665268,"CYE市场趋势_CYES":0.2740356937,"GDX轨道线_轨道":0.0217963968,"GDX轨道线_压力线":0.0237580725,"GDX轨道线_支撑线":0.0198347211,"JLHB绝路航标_B":28.1755780517,"JLHB绝路航标_VAR2":27.6175162292,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":113.7254901961,"BRAR情绪指标_AR":98.275862069,"CR带状能量线_CR":107.1428571429,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":24.6528183452,"MASS梅斯线_MAMASS":24.2168037015,"PSY心理线_PSY":50.0,"PSY心理线_PSYMA":56.9444444444,"VR成交量变异率_VR":110.3381001189,"VR成交量变异率_MAVR":133.8916290821,"WAD威廉多空力度线_WAD":0.893,"WAD威廉多空力度线_MAWAD":0.8512333333,"PCNT幅度比_PCNT":0.5424954792,"PCNT幅度比_MAPCNT":-0.2937155259,"CYR市场强弱_CYR":-0.003085767,"CYR市场强弱_MACYR":0.1098737933,"AMO成交金额_AMOW":19099.3874,"AMO成交金额_AMO1":30241.54668,"AMO成交金额_AMO2":34199.9405,"OBV累积能量线_OBV":236832846,"OBV累积能量线_MAOBV":233633495.6333333254,"VOL成交量_MAVOL1":1352441.8,"VOL成交量_MAVOL2":1526474.6000000001,"VRSI相对强弱量_RSI1":35.2742934223,"VRSI相对强弱量_RSI2":40.6892369129,"VRSI相对强弱量_RSI3":44.1059611646,"HSL换手线_HSL":861635,"HSL换手线_MAHSL":1352441.8,"MA均线_MA1":2.2378,"MA均线_MA2":2.2383,"MA均线_MA3":2.1865,"MA均线_MA4":2.1917,"ACD升降线_ACD":0.893,"ACD升降线_MAACD":0.8836356369,"BBI多空均线":2.2174270833,"EXPMA指数平均线_EXP1":2.219170819,"EXPMA指数平均线_EXP2":2.1699755524,"HMA高价平均线_HMA1":2.2421666667,"HMA高价平均线_HMA2":2.25075,"HMA高价平均线_HMA3":2.1838,"HMA高价平均线_HMA4":2.2047142857,"HMA高价平均线_HMA5":2.1499666667,"LMA低价平均线_LMA1":2.227,"LMA低价平均线_LMA2":2.2299166667,"LMA低价平均线_LMA3":2.1617666667,"LMA低价平均线_LMA4":2.1605,"LMA低价平均线_LMA5":2.1114111111,"VMA变异平均线_VMA1":2.235125,"VMA变异平均线_VMA2":2.2405625,"VMA变异平均线_VMA3":2.1729916667,"VMA变异平均线_VMA4":2.1838,"VMA变异平均线_VMA5":2.131675,"AMV成本均线_AMV1":2.2385097082,"AMV成本均线_AMV2":2.2381698995,"AMV成本均线_AMV3":2.1731207646,"AMV成本均线_AMV4":2.2088395296,"BBIBOLL多空布林线_BBIBOLL":2.2174270833,"BBIBOLL多空布林线_UPR":2.3140791669,"BBIBOLL多空布林线_DWN":2.1207749998,"ALLIGAT鳄鱼线_上唇":2.2407,"ALLIGAT鳄鱼线_牙齿":2.2361875,"ALLIGAT鳄鱼线_下颚":2.1530769231,"GMMA顾比均线_MA3":2.21837708,"GMMA顾比均线_MA5":2.2248440124,"GMMA顾比均线_MA8":2.22561902,"GMMA顾比均线_MA10":2.222878521,"GMMA顾比均线_MA12":2.219170819,"GMMA顾比均线_MA15":2.2133413328,"GMMA顾比均线_MA30":2.1927736207,"GMMA顾比均线_MA35":2.1874221067,"GMMA顾比均线_MA40":2.1819125264,"GMMA顾比均线_MA45":2.1760989356,"GMMA顾比均线_MA50":2.1699755524,"GMMA顾比均线_MA60":2.1570442164,"BOLL布林线_BOLL":2.1865,"BOLL布林线_UB":2.3357172912,"BOLL布林线_LB":2.0372827088,"PBX瀑布线_PBX1":2.2215699277,"PBX瀑布线_PBX2":2.2143125799,"PBX瀑布线_PBX3":2.1968402793,"PBX瀑布线_PBX4":2.1905501105,"PBX瀑布线_PBX5":2.1863219191,"PBX瀑布线_PBX6":2.1638887765,"ENE轨道线_UPPER":2.3033376,"ENE轨道线_LOWER":2.0425824,"ENE轨道线_ENE":2.17296,"MIKE麦克支撑压力_STOR":2.4158427284,"MIKE麦克支撑压力_MIDR":2.363440924,"MIKE麦克支撑压力_WEKR":2.3110391196,"MIKE麦克支撑压力_WEKS":2.1868075982,"MIKE麦克支撑压力_MIDS":2.1149778813,"MIKE麦克支撑压力_STOS":2.0431481644,"XS薛斯通道_SUP":2.3373737889,"XS薛斯通道_SDN":2.0727654354,"XS薛斯通道_LUP":2.5353953363,"XS薛斯通道_LDN":1.9126666572,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1762748757,"MA交易_MA1":2.2378,"MA交易_MA2":2.1865,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0219732563,"MACD交易_DEA":0.0207475575,"MACD交易_MACD":0.0024513975,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":39.911182488,"KDJ交易_D":55.4412736826,"KDJ交易_J":8.8510000987,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4816286539,"SG_XDT心电图_MQR1":0.4799417568,"SG_XDT心电图_MQR2":0.4790012076,"SG_NDB脑电波_DK":3.324,"SG_NDB脑电波_MDK1":3.3028,"SG_NDB脑电波_MDK2":3.2832,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":20.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":20664.5191570148,"LON龙系长线_LONMA":20981.6631828678,"LON龙系长线_LONT":20664.5191570148,"SHT龙系短线_SHT":1.6363822355,"SHT龙系短线_SHTMA":3.050106322,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":52.1114781051,"ZLMM主力买卖_MMM":59.4132527751,"ZLMM主力买卖_MML":53.8131282879,"SLZT神龙在天_白龙":2.029792,"SLZT神龙在天_黄龙":2.3839420671,"SLZT神龙在天_紫龙":1.6532894442,"SLZT神龙在天_青龙":2.0733539032,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30120.2365576876,"ADVOL龙系离散量_MA1":29710.2406185584,"ADVOL龙系离散量_MA2":28539.7653121343,"CYS市场盈亏":-0.2437717041,"CYW主力控盘":131.8210622519,"JAX济安线_J":2.218406499,"JAX济安线_A":2.2087091833,"JAX济安线_X":2.2087091833,"XJDX超级短线_J":-0.093207773,"XJDX超级短线_D":0.0593622326,"XJDX超级短线_K":-0.093207773,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":1.2646862772,"BDZX波段之星_AK":69.133887613,"BDZX波段之星_AD1":72.8314896604,"BDZX波段之星_AJ":61.7386835181,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":0.0085389143,"LHXJ猎狐先觉_主力控盘":-0.0085389143,"LYJH猎鹰歼狐_机构做空能量线":28.6797390431,"LYJH猎鹰歼狐_机构做多能量线":42.093570978,"JFZX飓风智能中线_多头力量":53.4548680713,"JFZX飓风智能中线_空头力量":46.5451319287,"CYHT财运亨通_SK":68.3183469317,"CYHT财运亨通_SD":67.6859861816,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":null,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":2.212,"CDP_STD逆势操作_CDP":2.195,"CDP_STD逆势操作_AH":2.22,"CDP_STD逆势操作_NH":2.205,"CDP_STD逆势操作_NL":2.19,"CDP_STD逆势操作_AL":2.175,"Alpha001":-0.6162852286,"Alpha002":1.6923076923,"Alpha003":-21.998,"Alpha004":1,"Alpha005":-0.8660254038,"Alpha006":-0.2064364207,"Alpha007":0.6469625836,"Alpha008":-0.1302982732,"Alpha009":-0.0,"Alpha010":0.9805825243,"Alpha011":2709213.3521367093,"Alpha012":-0.0121842848,"Alpha013":-219.4479892699,"Alpha014":-0.014,"Alpha015":0.0077272727,"Alpha016":-0.8838304553,"Alpha017":1.0190397362,"Alpha018":0.9937106918,"Alpha019":-0.0062893082,"Alpha020":-0.6289308176,"Alpha021":-0.0010666667,"Alpha022":-0.0037854244,"Alpha023":52.6220029076,"Alpha024":0.0115437528,"Alpha025":-0.6442838681,"Alpha026":0.9484960628,"Alpha027":68.874076667,"Alpha028":-8.1373421061,"Alpha029":-5419.0880503146,"Alpha030":0.0002680907,"Alpha031":-1.301405518,"Alpha032":-1.3317683881,"Alpha033":0.0030889236,"Alpha034":1.013185654,"Alpha035":-0.4696485623,"Alpha036":0.6087636933,"Alpha037":1.1174429053,"Alpha038":0.024,"Alpha039":0.127925117,"Alpha040":95.5306664029,"Alpha041":-0.7232704403,"Alpha042":-0.3143501641,"Alpha043":1293583.0,"Alpha044":1.1333333333,"Alpha045":0.2684670257,"Alpha046":1.0024534735,"Alpha047":49.3532517903,"Alpha048":-0.0583356747,"Alpha049":0.4236842105,"Alpha050":0.1526315789,"Alpha051":0.5763157895,"Alpha052":110.4855735398,"Alpha053":50.0,"Alpha054":-0.2183544304,"Alpha055":1.3400118408,"Alpha056":-0.2177156177,"Alpha057":26.8579089754,"Alpha058":55.0,"Alpha059":0.084,"Alpha060":6864527.1614715727,"Alpha061":-0.4102964119,"Alpha062":-0.1825510015,"Alpha063":46.4030584885,"Alpha064":-0.6770670827,"Alpha065":1.010774563,"Alpha066":-1.0659709281,"Alpha067":53.0586116746,"Alpha068":0.0,"Alpha069":-0.7993920973,"Alpha070":69967350.8104682565,"Alpha071":1.6680391443,"Alpha072":49.2712394034,"Alpha073":-0.1681577722,"Alpha074":0.7831513261,"Alpha075":0.3703703704,"Alpha076":0.6879942942,"Alpha077":0.0140405616,"Alpha078":-25.2775873886,"Alpha079":51.9238691111,"Alpha080":-33.7648640567,"Alpha081":1644078.790058651,"Alpha082":49.3750404525,"Alpha083":-0.4678178964,"Alpha084":4724128.0,"Alpha085":0.15,"Alpha086":1.0,"Alpha087":-0.3784265656,"Alpha088":3.8010323792,"Alpha089":0.0024513975,"Alpha090":-0.6427457098,"Alpha091":-0.07054126,"Alpha092":-0.2,"Alpha093":0.128,"Alpha094":7889798.0,"Alpha095":87003669.109637931,"Alpha096":44.3555345161,"Alpha097":370672.0084911756,"Alpha098":0.062,"Alpha099":-0.5274725275,"Alpha100":367428.3955257654,"Alpha101":-0.4976599064,"Alpha102":35.2742934223,"Alpha103":25.0,"Alpha104":0.4669756428,"Alpha105":-0.4130984639,"Alpha106":0.081,"Alpha107":-0.6344674873,"Alpha108":-0.9088093851,"Alpha109":0.8327040316,"Alpha110":125.1445086705,"Alpha111":145975.0661721919,"Alpha112":6.3291139241,"Alpha113":0.1479795853,"Alpha114":20.5666892014,"Alpha115":0.8411850464,"Alpha116":0.0100909774,"Alpha117":0.0061035156,"Alpha118":105.9113300493,"Alpha119":0.5288611544,"Alpha120":0.9802391033,"Alpha121":-0.299893295,"Alpha122":0.0026051435,"Alpha123":-0.4959204488,"Alpha124":-79.0719727447,"Alpha125":0.4447300771,"Alpha126":2.215,"Alpha127":1.6661906449,"Alpha128":64.5110933601,"Alpha129":0.148,"Alpha130":0.7524038462,"Alpha131":0.941725745,"Alpha132":334648907.1000000238,"Alpha133":35.0,"Alpha134":7861.6332116786,"Alpha135":1.0160563006,"Alpha136":-0.2069692151,"Alpha137":0.1187096774,"Alpha138":-0.5560508135,"Alpha139":-0.4019493598,"Alpha140":0.3333333333,"Alpha141":-0.6122778675,"Alpha142":-0.0161478615,"Alpha143":0.0054545455,"Alpha144":0.0,"Alpha145":-11.8339290024,"Alpha146":0.8901461514,"Alpha147":0.0119493007,"Alpha148":-0.1072210158,"Alpha149":0.8422423057,"Alpha150":1908521.5249999999,"Alpha151":0.0333094018,"Alpha152":0.0021105433,"Alpha153":2.2174270833,"Alpha154":-18.2748469929,"Alpha155":9814.0676017177,"Alpha156":-0.9188767551,"Alpha157":0.8307086614,"Alpha158":0.0058770344,"Alpha159":-5752.9679595156,"Alpha160":0.0279374442,"Alpha161":0.0368333333,"Alpha162":0.1117450505,"Alpha163":0.2121684867,"Alpha164":256468.3303070971,"Alpha165":-12.6467168412,"Alpha166":-0.001385107,"Alpha167":0.168,"Alpha168":-0.5645603326,"Alpha169":0.0025402552,"Alpha170":-0.2565301057,"Alpha171":-0.1838823998,"Alpha172":36.855597583,"Alpha173":3.0379371381,"Alpha174":0.0310296838,"Alpha175":0.0313333333,"Alpha176":0.3529415235,"Alpha177":60.0,"Alpha178":4699.827272727,"Alpha179":0.3872654126,"Alpha180":-861635.0,"Alpha181":0.0088916355,"Alpha182":0.65,"Alpha183":15.0350296252,"Alpha184":0.748049922,"Alpha185":-0.0000051094,"Alpha186":34.2066727396,"Alpha187":0.381,"Alpha188":-28.0623907726,"Alpha189":0.0213333333,"Alpha190":-0.4934307661,"Alpha191":0.8076416181},{"date":"2026-08-21","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.195,"high":2.2,"low":2.187,"close":2.195,"volume":1367074,"amount":299752862.0,"5日涨跌幅":-3.0477031802,"10日涨跌幅":-3.1332744925,"20日涨跌幅":4.325095057,"30日涨跌幅":0.9659613615,"60日涨跌幅":-0.8581752484,"120日涨跌幅":20.6706981858,"六脉神剑":0,"小波段交易":false,"大波段交易":true,"波段超级买卖":false,"价格距离5日均线涨跌幅":-1.3039568345,"价格距离10日均线涨跌幅":-1.6224453209,"价格距离20日均线涨跌幅":0.1802788617,"价格距离30日均线涨跌幅":0.9783475434,"价格距离60日均线涨跌幅":0.1650403474,"价格距离120日均线涨跌幅":7.5303934616,"5日均线距离10日均线涨跌幅":-0.3226963069,"10日均线距离20日均线涨跌幅":1.8324547591,"20日均线距离30日均线涨跌幅":0.7966325216,"30日均线距离60日均线涨跌幅":-0.8054273176,"60日均线距离120日均线涨跌幅":7.3532173388,"5日偏度":1.0505573473,"10日偏度":0.3405356473,"20日偏度":-0.7869136385,"30日偏度":-0.1568951095,"60日偏度":0.1976196075,"120日偏度":-0.4797256833,"5日峰度":0.013608861,"10日峰度":-1.2366509328,"20日峰度":-0.6815425294,"30日峰度":-1.0863255838,"60日峰度":-0.0927528815,"120日峰度":-1.204689119,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":true,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.224,"10日均线":2.2312,"20日均线":2.19105,"30日均线":2.1737333333,"60日均线":2.1913833333,"120日均线":2.0412833333,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":0.0,"连续下跌天数":0.0,"价格在5均线上":false,"价格在10均线上":false,"价格在20均线上":true,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":-0.7331989938,"10日Alpha":-0.4260784576,"20日Alpha":0.8797368899,"30日Alpha":0.338479639,"60日Alpha":0.1930946893,"120日Alpha":0.5688634137,"5日Beta":0.4692073687,"10日Beta":0.5860814091,"20日Beta":0.9764970127,"30日Beta":0.6945879165,"60日Beta":0.7406313299,"120日Beta":0.8583371848,"5日夏普比率":-9.0560410503,"10日夏普比率":-4.1343103107,"20日夏普比率":2.0707295142,"30日夏普比率":0.4432870745,"60日夏普比率":0.0207370448,"120日夏普比率":1.5298724605,"5日年化波动率":0.1704315762,"10日年化波动率":0.1897971603,"20日年化波动率":0.2751617527,"30日年化波动率":0.249995485,"60日年化波动率":0.2938471123,"120日年化波动率":0.2841077029,"5日最大回撤":-0.0347405453,"10日最大回撤":-0.0347405453,"20日最大回撤":-0.0363550519,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":0.0347223763,"10日上涨捕获率":0.5803905213,"20日上涨捕获率":3.035749671,"30日上涨捕获率":0.8596670306,"60日上涨捕获率":0.4715700446,"120日上涨捕获率":0.8906071821,"5日下跌捕获率":1.0008344479,"10日下跌捕获率":1.0200693867,"20日下跌捕获率":0.9985096195,"30日下跌捕获率":0.9505917253,"60日下跌捕获率":0.9265579973,"120日下跌捕获率":0.8771660564,"3日回归动量":-0.0816494696,"5日回归动量":-0.6401956076,"7日回归动量":-0.4118127418,"9日回归动量":-0.096112081,"12日回归动量":-0.1370355699,"15日回归动量":0.0021275164,"18日回归动量":0.1753373841,"20日回归动量":0.3949643366,"23日回归动量":0.5186273667,"25日回归动量":0.562295301,"28日回归动量":0.4107567773,"30日回归动量":0.3075113013,"35日回归动量":0.1644015228,"40日回归动量":0.0676737459,"45日回归动量":0.0215433479,"50日回归动量":-0.0003637988,"60日回归动量":-0.000001355,"5日最高值到当前周期":4.0,"10日最高值到当前周期":4.0,"20日最高值到当前周期":4.0,"30日最高值到当前周期":4.0,"60日最高值到当前周期":58.0,"120日最高值到当前周期":58.0,"5日最低值到当前周期":0.0,"10日最低值到当前周期":0.0,"20日最低值到当前周期":16.0,"30日最低值到当前周期":16.0,"60日最低值到当前周期":16.0,"120日最低值到当前周期":98.0,"5日回归斜率":-0.0185,"10日回归斜率":-0.0042181818,"20日回归斜率":0.0085195489,"30日回归斜率":0.0045517241,"60日回归斜率":-0.0007986385,"120日回归斜率":0.0046578165,"5日标准差":0.0292779781,"10日标准差":0.0261258493,"20日标准差":0.0721737314,"30日标准差":0.0662026854,"60日标准差":0.0664866131,"120日标准差":0.1927517481,"CCI商品路径指标":-107.7930582842,"MFI最近流量指标":59.1511864804,"MTM动量线_MTM值":-0.072,"MTM动量线_MTMMA值":0.0951666667,"RSI相对强弱_RSI1":40.8987320617,"RSI相对强弱_RSI2":49.0525589832,"RSI相对强弱_RSI3":51.6565949301,"KDJ指标_K值":30.352773344,"KDJ指标_D值":47.0784402364,"KDJ指标_J值":-3.0985604407,"SKDJ慢速随机_K值":30.993074087,"SKDJ慢速随机_D值":41.1082843669,"UDL引力线_UDL值":2.2121458333,"UDL引力线_MAUDL值":2.2227284722,"WR威廉指标_WR1":90.6542056075,"WR威廉指标_WR2":88.7640449438,"LWR指标_LWR1":69.647226656,"LWR指标_LWR2":52.9215597636,"MARSI相对强弱平均线_RSI1":57.3522889478,"MARSI相对强弱平均线_RSI2":53.7192789808,"BIAS乖离率_BIAS1":-1.5989240885,"BIAS乖离率_BIAS2":-1.7970322869,"BIAS乖离率_BIAS3":0.695771848,"BIAS_QL乖离率传统版_BIAS值":-1.5989240885,"BIAS_QL乖离率传统版_BIASMA值":-0.3644081085,"BIAS36三六乖离_BIAS36":-0.0283333333,"BIAS36三六乖离_BIAS612":-0.0045,"BIAS36三六乖离_MABIAS":-0.0038888889,"ACCER幅度涨速":-0.002787721,"ASI振动升降指标_ASI":0.164948439,"ASI振动升降指标_ASIT":0.4042862008,"CHO佳庆指标_CHO":3552.3130907828,"CHO佳庆指标_MACHO":6107.1315616211,"DMA_XT平均差_DIF":0.04778,"DMA_XT平均差_DIFMA":0.03856,"DMI趋向指标_PDI":-33.7711069418,"DMI趋向指标_MDI":32.4577861163,"DMI趋向指标_ADX":-3448.4765234767,"DMI趋向指标_ADXR":-2729.0116535512,"DPO区间震荡线_DPO":-0.0485714286,"DPO区间震荡线_MADPO":0.0229761905,"EMV简易波动指标_EMV":0.2085797972,"EMV简易波动指标_MAEMV":0.1652574707,"MACD平滑异同平均线_DIF":0.0184174512,"MACD平滑异同平均线_DEA":0.0202815362,"MACD平滑异同平均线_MACD":-0.0037281701,"VMACD量平滑异同平均线_DIF":-307983.3778899475,"VMACD量平滑异同平均线_DEA":-328378.928137636,"VMACD量平滑异同平均线_MACD":20395.5502476885,"SMACD单线平滑异同平均线_DEA":0.0202815362,"SMACD单线平滑异同平均线_MACD":0.0184174512,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.1903022251,"TRIX三重指数平均线_MATRIX":0.1640276501,"UOS终极指标_UOS":47.6754606624,"UOS终极指标_MAUOS":50.8280095722,"VTP量价曲线_VPT":108045.5489768464,"VTP量价曲线_MAVP":35932.5660461371,"WVAD威廉变异离散量_WVAD":493.9844210201,"WVAD威廉变异离散量_MAWVAD":270.1691425295,"JS加数线_JS":-0.609540636,"JS加数线_MAJS1":-0.127446404,"JS加数线_MAJS2":0.0292821021,"JS加数线_MAJS3":0.2609519786,"CYE市场趋势_CYEL":-0.6166770936,"CYE市场趋势_CYES":0.2429726254,"GDX轨道线_轨道":0.0156174219,"GDX轨道线_压力线":0.0170229898,"GDX轨道线_支撑线":0.0142118539,"JLHB绝路航标_B":27.5242434961,"JLHB绝路航标_VAR2":27.5988616826,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":113.4782608696,"BRAR情绪指标_AR":94.8979591837,"CR带状能量线_CR":105.1051051051,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":24.6147295968,"MASS梅斯线_MAMASS":24.394547055,"PSY心理线_PSY":41.6666666667,"PSY心理线_PSYMA":54.1666666667,"VR成交量变异率_VR":113.2816419094,"VR成交量变异率_MAVR":128.6832271841,"WAD威廉多空力度线_WAD":0.876,"WAD威廉多空力度线_MAWAD":0.8528333333,"PCNT幅度比_PCNT":-0.7744874715,"PCNT幅度比_MAPCNT":-0.4539728411,"CYR市场强弱_CYR":-0.1478990844,"CYR市场强弱_MACYR":0.0160201216,"AMO成交金额_AMOW":29975.2862,"AMO成交金额_AMO1":28875.22694,"AMO成交金额_AMO2":32711.52781,"OBV累积能量线_OBV":235465772,"OBV累积能量线_MAOBV":233789508.5333333313,"VOL成交量_MAVOL1":1299675.8,"VOL成交量_MAVOL2":1464032.8999999999,"VRSI相对强弱量_RSI1":48.3354857156,"VRSI相对强弱量_RSI2":46.5631508808,"VRSI相对强弱量_RSI3":46.3536034147,"HSL换手线_HSL":1367074,"HSL换手线_MAHSL":1299675.8,"MA均线_MA1":2.224,"MA均线_MA2":2.2312,"MA均线_MA3":2.19105,"MA均线_MA4":2.1913833333,"ACD升降线_ACD":0.876,"ACD升降线_MAACD":0.8829084334,"BBI多空均线":2.212,"EXPMA指数平均线_EXP1":2.2154522314,"EXPMA指数平均线_EXP2":2.1709569033,"HMA高价平均线_HMA1":2.2348333333,"HMA高价平均线_HMA2":2.2450833333,"HMA高价平均线_HMA3":2.1841666667,"HMA高价平均线_HMA4":2.2059,"HMA高价平均线_HMA5":2.1543777778,"LMA低价平均线_LMA1":2.2208333333,"LMA低价平均线_LMA2":2.2246666667,"LMA低价平均线_LMA3":2.1623,"LMA低价平均线_LMA4":2.1618428571,"LMA低价平均线_LMA5":2.1158444444,"VMA变异平均线_VMA1":2.2287916667,"VMA变异平均线_VMA2":2.235,"VMA变异平均线_VMA3":2.1735083333,"VMA变异平均线_VMA4":2.1850357143,"VMA变异平均线_VMA5":2.1360861111,"AMV成本均线_AMV1":2.2238375806,"AMV成本均线_AMV2":2.2402471231,"AMV成本均线_AMV3":2.1737359858,"AMV成本均线_AMV4":2.2084994428,"BBIBOLL多空布林线_BBIBOLL":2.212,"BBIBOLL多空布林线_UPR":2.279366679,"BBIBOLL多空布林线_DWN":2.144633321,"ALLIGAT鳄鱼线_上唇":2.2431,"ALLIGAT鳄鱼线_牙齿":2.2458125,"ALLIGAT鳄鱼线_下颚":2.1602692308,"GMMA顾比均线_MA3":2.20668854,"GMMA顾比均线_MA5":2.2148960083,"GMMA顾比均线_MA8":2.2188147933,"GMMA顾比均线_MA10":2.217809699,"GMMA顾比均线_MA12":2.2154522314,"GMMA顾比均线_MA15":2.2110486662,"GMMA顾比均线_MA30":2.192917258,"GMMA顾比均线_MA35":2.1878431008,"GMMA顾比均线_MA40":2.1825509398,"GMMA顾比均线_MA45":2.176920721,"GMMA顾比均线_MA50":2.1709569033,"GMMA顾比均线_MA60":2.1582886683,"BOLL布林线_BOLL":2.19105,"BOLL布林线_UB":2.3353974627,"BOLL布林线_LB":2.0467025373,"PBX瀑布线_PBX1":2.22030029,"PBX瀑布线_PBX2":2.2107292237,"PBX瀑布线_PBX3":2.1975722234,"PBX瀑布线_PBX4":2.1898195087,"PBX瀑布线_PBX5":2.1867344267,"PBX瀑布线_PBX6":2.1649751744,"ENE轨道线_UPPER":2.3070688,"ENE轨道线_LOWER":2.0458912,"ENE轨道线_ENE":2.17648,"MIKE麦克支撑压力_STOR":2.4085768816,"MIKE麦克支撑压力_MIDR":2.3556085742,"MIKE麦克支撑压力_WEKR":2.3026402668,"MIKE麦克支撑压力_WEKS":2.1858530606,"MIKE麦克支撑压力_MIDS":2.1220341618,"MIKE麦克支撑压力_STOS":2.0582152629,"XS薛斯通道_SUP":2.3381728075,"XS薛斯通道_SDN":2.0734739991,"XS薛斯通道_LUP":2.5333125589,"XS薛斯通道_LDN":1.9110954392,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.1855328857,"MA交易_MA1":2.224,"MA交易_MA2":2.19105,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0184174512,"MACD交易_DEA":0.0202815362,"MACD交易_MACD":-0.0037281701,"MACD交易_平空开多":true,"MACD交易_平多开空":true,"KDJ交易_K":30.352773344,"KDJ交易_D":47.0784402364,"KDJ交易_J":-3.0985604407,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4752218875,"SG_XDT心电图_MQR1":0.4779412247,"SG_XDT心电图_MQR2":0.4782534871,"SG_NDB脑电波_DK":3.303,"SG_NDB脑电波_MDK1":3.3098,"SG_NDB脑电波_MDK2":3.2825,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":20.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":19507.8293194966,"LON龙系长线_LONMA":20902.6662746752,"LON龙系长线_LONT":19507.8293194966,"SHT龙系短线_SHT":0.7288923026,"SHT龙系短线_SHTMA":2.2889565081,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":48.2841225727,"ZLMM主力买卖_MMM":56.9401127301,"ZLMM主力买卖_MML":54.0562071287,"SLZT神龙在天_白龙":2.032664,"SLZT神龙在天_黄龙":2.3879900523,"SLZT神龙在天_紫龙":1.655321825,"SLZT神龙在天_青龙":2.0777268251,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30151.7844192261,"ADVOL龙系离散量_MA1":29731.6085517026,"ADVOL龙系离散量_MA2":28565.8181740426,"CYS市场盈亏":-0.8638119804,"CYW主力控盘":52.7305349015,"JAX济安线_J":2.2063282495,"JAX济安线_A":2.1942364291,"JAX济安线_X":2.1942364291,"XJDX超级短线_J":-0.2013700795,"XJDX超级短线_D":-0.0892831693,"XJDX超级短线_K":-0.2013700795,"ZJTJ庄家抬轿_无庄控盘":0.0,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":0.4784492537,"BDZX波段之星_AK":61.5783998735,"BDZX波段之星_AD1":65.3294298025,"BDZX波段之星_AJ":54.0763400155,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":0.0237020954,"LHXJ猎狐先觉_主力控盘":-0.0237020954,"LYJH猎鹰歼狐_机构做空能量线":33.2114648523,"LYJH猎鹰歼狐_机构做多能量线":34.3220477936,"JFZX飓风智能中线_多头力量":53.9383438401,"JFZX飓风智能中线_空头力量":46.0616561599,"CYHT财运亨通_SK":67.4190611277,"CYHT财运亨通_SD":67.5525236547,"CYHT财运亨通_卖出":60,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":null,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":2.195,"CDP_STD逆势操作_CDP":2.215,"CDP_STD逆势操作_AH":2.233,"CDP_STD逆势操作_NH":2.22,"CDP_STD逆势操作_NL":2.207,"CDP_STD逆势操作_AL":2.194,"Alpha001":-0.5818436489,"Alpha002":-0.9230769231,"Alpha003":-21.998,"Alpha004":-1,"Alpha005":-8.177564889e-16,"Alpha006":-0.2064364207,"Alpha007":1.083739287,"Alpha008":-0.0455259027,"Alpha009":-0.0000000001,"Alpha010":0.9805825243,"Alpha011":4065390.3675213675,"Alpha012":-0.0150328798,"Alpha013":-217.0725201027,"Alpha014":-0.069,"Alpha015":-0.0076853526,"Alpha016":-0.8838304553,"Alpha017":1.1334909278,"Alpha018":0.9695229682,"Alpha019":-0.0304770318,"Alpha020":-1.3926325247,"Alpha021":-0.0010666667,"Alpha022":-0.0047404236,"Alpha023":49.3596858537,"Alpha024":-0.0045649977,"Alpha025":-0.2159189644,"Alpha026":0.9605934894,"Alpha027":-20.9075459804,"Alpha028":-17.3617431709,"Alpha029":-19038.3171608267,"Alpha030":0.0002426805,"Alpha031":-1.7970322869,"Alpha032":-0.8294209703,"Alpha033":0.0081210608,"Alpha034":1.0182991648,"Alpha035":-0.2060702875,"Alpha036":0.6713615023,"Alpha037":1.1295205625,"Alpha038":0.0,"Alpha039":0.1856474259,"Alpha040":97.8953311917,"Alpha041":-0.7232704403,"Alpha042":-0.2956623791,"Alpha043":-73491.0,"Alpha044":1.0666666667,"Alpha045":0.067026706,"Alpha046":1.0077448747,"Alpha047":53.7322288074,"Alpha048":-0.0561770693,"Alpha049":0.5786163522,"Alpha050":-0.1572327044,"Alpha051":0.4213836478,"Alpha052":108.9521165857,"Alpha053":41.6666666667,"Alpha054":-0.4367088608,"Alpha055":1.4976890783,"Alpha056":-0.0239149739,"Alpha057":17.9052726503,"Alpha058":55.0,"Alpha059":0.094,"Alpha060":6893834.9768562363,"Alpha061":-0.4617784711,"Alpha062":-0.0228740265,"Alpha063":40.8987320617,"Alpha064":-0.5959438378,"Alpha065":1.0162490509,"Alpha066":-1.5989240885,"Alpha067":51.6565949301,"Alpha068":-0.0,"Alpha069":-0.8145896657,"Alpha070":69813393.1375309974,"Alpha071":0.695771848,"Alpha072":51.9040931061,"Alpha073":-0.1347977965,"Alpha074":0.8517940718,"Alpha075":0.3461538462,"Alpha076":0.7057549881,"Alpha077":0.0109204368,"Alpha078":-46.3672442925,"Alpha079":49.0525589832,"Alpha080":-16.1769178321,"Alpha081":1617697.3814816365,"Alpha082":51.344490677,"Alpha083":-0.4458398744,"Alpha084":4787908.0,"Alpha085":0.48125,"Alpha086":1.0,"Alpha087":-0.2676621351,"Alpha088":4.325095057,"Alpha089":-0.0037281701,"Alpha090":-0.5585023401,"Alpha091":-0.0342743735,"Alpha092":-0.2666666667,"Alpha093":0.131,"Alpha094":4680387.0,"Alpha095":87029903.6344664395,"Alpha096":35.5387805609,"Alpha097":334457.8167941584,"Alpha098":0.044,"Alpha099":-0.5133437991,"Alpha100":368574.5231450292,"Alpha101":-0.4024960998,"Alpha102":48.3354857156,"Alpha103":20.0,"Alpha104":0.6296425217,"Alpha105":-0.4243544264,"Alpha106":0.091,"Alpha107":-0.0016430483,"Alpha108":-0.0065966115,"Alpha109":0.8235908891,"Alpha110":129.2537313433,"Alpha111":82333.74597003,"Alpha112":-27.9069767442,"Alpha113":0.1858348281,"Alpha114":388.766780008,"Alpha115":0.867746011,"Alpha116":0.0097007519,"Alpha117":0.1396484375,"Alpha118":101.9417475728,"Alpha119":0.6614664587,"Alpha120":0.9801770976,"Alpha121":-0.1159793464,"Alpha122":0.0024517068,"Alpha123":-0.4617202108,"Alpha124":-78.2138941611,"Alpha125":0.608,"Alpha126":2.194,"Alpha127":1.9447225607,"Alpha128":59.1511864804,"Alpha129":0.165,"Alpha130":0.8920863309,"Alpha131":0.2731540154,"Alpha132":334585551.8499999642,"Alpha133":35.0,"Alpha134":-43418.3184825761,"Alpha135":1.0171540018,"Alpha136":-0.2828753685,"Alpha137":-0.2728682171,"Alpha138":-0.3828838868,"Alpha139":-0.4076733252,"Alpha140":0.3333333333,"Alpha141":-0.5783521809,"Alpha142":-0.0046825029,"Alpha143":0.0054545455,"Alpha144":0.0,"Alpha145":-15.101913134,"Alpha146":-2.110191595,"Alpha147":0.0115731352,"Alpha148":0.6197052041,"Alpha149":0.8422423057,"Alpha150":2999360.3559999992,"Alpha151":0.0361939317,"Alpha152":0.0039783448,"Alpha153":2.212,"Alpha154":-8.5998730776,"Alpha155":20395.5502476885,"Alpha156":-0.7987519501,"Alpha157":1.0307086614,"Alpha158":0.0059225513,"Alpha159":-5867.4562427604,"Alpha160":0.0302430063,"Alpha161":0.0325833333,"Alpha162":0.0,"Alpha163":0.6973478939,"Alpha164":217011.6641060052,"Alpha165":-9.6634305897,"Alpha166":-0.001465772,"Alpha167":0.093,"Alpha168":-0.8976095365,"Alpha169":0.0028565733,"Alpha170":-0.0571692956,"Alpha171":-1.6,"Alpha172":34.2691631676,"Alpha173":3.0232268339,"Alpha174":0.0294781996,"Alpha175":0.0321666667,"Alpha176":0.4346291644,"Alpha177":55.0,"Alpha178":-10506.4457504521,"Alpha179":0.1647192253,"Alpha180":-1367074.0,"Alpha181":0.0090398579,"Alpha182":0.65,"Alpha183":15.5233074009,"Alpha184":0.6076443058,"Alpha185":0.0,"Alpha186":33.9470472632,"Alpha187":0.381,"Alpha188":-24.1946079846,"Alpha189":0.025,"Alpha190":-0.5086850605,"Alpha191":0.8415678681},{"date":"2026-08-24","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.19,"high":2.191,"low":2.164,"close":2.166,"volume":1444993,"amount":314261067.9999999404,"5日涨跌幅":-4.7493403694,"10日涨跌幅":-4.2016806723,"20日涨跌幅":2.2662889518,"30日涨跌幅":-0.0922509225,"60日涨跌幅":-4.7074351078,"120日涨跌幅":20.1997780244,"六脉神剑":0,"小波段交易":false,"大波段交易":false,"波段超级买卖":false,"价格距离5日均线涨跌幅":-1.6527424628,"价格距离10日均线涨跌幅":-2.507089166,"价格距离20日均线涨跌幅":-1.2514531902,"价格距离30日均线涨跌幅":-0.3527066401,"价格距离60日均线涨跌幅":-1.0778224333,"价格距离120日均线涨跌幅":5.952274191,"5日均线距离10日均线涨跌幅":-0.8687041455,"10日均线距离20日均线涨跌幅":1.2879254143,"20日均线距离30日均线涨跌幅":0.9101364821,"30日均线距离60日均线涨跌幅":-0.7276823773,"60日均线距离120日均线涨跌幅":7.1066941684,"5日偏度":0.0282004789,"10日偏度":0.087185436,"20日偏度":-0.8977322393,"30日偏度":-0.153698219,"60日偏度":0.2545591757,"120日偏度":-0.5160645627,"5日峰度":0.9747705264,"10日峰度":-0.0053428538,"20日峰度":-0.3333518279,"30日峰度":-1.0879438109,"60日峰度":0.0376936544,"120日峰度":-1.1556466716,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.2024,"10日均线":2.2217,"20日均线":2.19345,"30日均线":2.1736666667,"60日均线":2.1896,"120日均线":2.0443166667,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":0.0,"连续下跌天数":1.0,"价格在5均线上":false,"价格在10均线上":false,"价格在20均线上":false,"价格在30均线上":false,"价格在60均线上":false,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":-0.8067440872,"10日Alpha":-0.4557266397,"20日Alpha":0.9866139232,"30日Alpha":0.1933903107,"60日Alpha":0.0362696225,"120日Alpha":0.6018007372,"5日Beta":0.4172306923,"10日Beta":0.616202178,"20日Beta":1.0218035261,"30日Beta":0.7263896462,"60日Beta":0.7515360292,"120日Beta":0.8635922189,"5日夏普比率":-16.6654710637,"10日夏普比率":-5.4114047335,"20日夏普比率":1.1411920036,"30日夏普比率":0.0910101663,"60日夏普比率":-0.5567617818,"120日夏普比率":1.4993225617,"5日年化波动率":0.1459260992,"10日年化波动率":0.1962548204,"20日年化波动率":0.2799493941,"30日年化波动率":0.2529754855,"60日年化波动率":0.2897475244,"120日年化波动率":0.2844817085,"5日最大回撤":-0.0474934037,"10日最大回撤":-0.0474934037,"20日最大回撤":-0.0474934037,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":-0.1939229465,"10日上涨捕获率":0.7217204527,"20日上涨捕获率":3.7915339021,"30日上涨捕获率":0.8596670306,"60日上涨捕获率":0.4715700446,"120日上涨捕获率":0.9452514803,"5日下跌捕获率":1.0029174509,"10日下跌捕获率":1.0184580894,"20日下跌捕获率":1.0002558084,"30日下跌捕获率":0.9678605641,"60日下跌捕获率":0.9550752479,"120日下跌捕获率":0.8820216517,"3日回归动量":-0.9185906599,"5日回归动量":-0.6851822872,"7日回归动量":-0.7679084469,"9日回归动量":-0.4042270946,"12日回归动量":-0.2882888999,"15日回归动量":-0.1228376166,"18日回归动量":0.0084416729,"20日回归动量":0.1258325157,"23日回归动量":0.2696578384,"25日回归动量":0.3076671585,"28日回归动量":0.331295863,"30日回归动量":0.2410487172,"35日回归动量":0.138727427,"40日回归动量":0.0599634423,"45日回归动量":0.0271322504,"50日回归动量":-0.0005858995,"60日回归动量":-0.0000199548,"5日最高值到当前周期":4.0,"10日最高值到当前周期":5.0,"20日最高值到当前周期":5.0,"30日最高值到当前周期":5.0,"60日最高值到当前周期":59.0,"120日最高值到当前周期":59.0,"5日最低值到当前周期":0.0,"10日最低值到当前周期":0.0,"20日最低值到当前周期":17.0,"30日最低值到当前周期":17.0,"60日最低值到当前周期":17.0,"120日最低值到当前周期":99.0,"5日回归斜率":-0.0151,"10日回归斜率":-0.0057878788,"20日回归斜率":0.0070082707,"30日回归斜率":0.0044622914,"60日回归斜率":-0.0007019172,"120日回归斜率":0.0046088131,"5日标准差":0.0237368911,"10日标准差":0.0304731029,"20日标准差":0.0704829589,"30日标准差":0.066209432,"60日标准差":0.0657039319,"120日标准差":0.1918241809,"CCI商品路径指标":-157.3384272525,"MFI最近流量指标":52.2073064654,"MTM动量线_MTM值":-0.078,"MTM动量线_MTMMA值":0.0505,"RSI相对强弱_RSI1":32.9079582883,"RSI相对强弱_RSI2":44.4756431052,"RSI相对强弱_RSI3":49.336028594,"KDJ指标_K值":20.8412428354,"KDJ指标_D值":38.3327077694,"KDJ指标_J值":-14.1416870326,"SKDJ慢速随机_K值":21.1942135263,"SKDJ慢速随机_D值":31.0669705582,"UDL引力线_UDL值":2.2021375,"UDL引力线_MAUDL值":2.2201486111,"WR威廉指标_WR1":98.1818181818,"WR威廉指标_WR2":98.1818181818,"LWR指标_LWR1":79.1587571646,"LWR指标_LWR2":61.6672922306,"MARSI相对强弱平均线_RSI1":54.9425900358,"MARSI相对强弱平均线_RSI2":47.8273633983,"BIAS乖离率_BIAS1":-2.1827487581,"BIAS乖离率_BIAS2":-2.8118456476,"BIAS乖离率_BIAS3":-0.7029339853,"BIAS_QL乖离率传统版_BIAS值":-2.1827487581,"BIAS_QL乖离率传统版_BIASMA值":-0.8842405847,"BIAS36三六乖离_BIAS36":-0.0233333333,"BIAS36三六乖离_BIAS612":-0.0143333333,"BIAS36三六乖离_MABIAS":-0.0070555556,"ACCER幅度涨速":-0.0054412347,"ASI振动升降指标_ASI":0.4993352983,"ASI振动升降指标_ASIT":0.3508994616,"CHO佳庆指标_CHO":2643.778250858,"CHO佳庆指标_MACHO":5463.6139381502,"DMA_XT平均差_DIF":0.0382,"DMA_XT平均差_DIFMA":0.044178,"DMI趋向指标_PDI":-37.9518072289,"DMI趋向指标_MDI":39.3574297189,"DMI趋向指标_ADX":-1923.4765234767,"DMI趋向指标_ADXR":-2175.5394313291,"DPO区间震荡线_DPO":-0.0771428571,"DPO区间震荡线_MADPO":-0.0087142857,"EMV简易波动指标_EMV":-0.0761532429,"EMV简易波动指标_MAEMV":0.1670103087,"MACD平滑异同平均线_DIF":0.0131082882,"MACD平滑异同平均线_DEA":0.0188468866,"MACD平滑异同平均线_MACD":-0.0114771969,"VMACD量平滑异同平均线_DIF":-285972.6447881514,"VMACD量平滑异同平均线_DEA":-319897.6714677391,"VMACD量平滑异同平均线_MACD":33925.0266795877,"SMACD单线平滑异同平均线_DEA":0.0188468866,"SMACD单线平滑异同平均线_MACD":0.0131082882,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.1687596927,"TRIX三重指数平均线_MATRIX":0.1744371579,"UOS终极指标_UOS":43.6860859295,"UOS终极指标_MAUOS":48.78745996,"VTP量价曲线_VPT":118436.3778298061,"VTP量价曲线_MAVP":85210.007090222,"WVAD威廉变异离散量_WVAD":155.6660533433,"WVAD威廉变异离散量_MAWVAD":265.0263969361,"JS加数线_JS":-0.9498680739,"JS加数线_MAJS1":-0.3404186919,"JS加数线_MAJS2":-0.191703765,"JS加数线_MAJS3":0.2029623917,"CYE市场趋势_CYEL":-0.9712230216,"CYE市场趋势_CYES":0.1828187071,"GDX轨道线_轨道":0.0082495942,"GDX轨道线_压力线":0.0089920577,"GDX轨道线_支撑线":0.0075071307,"JLHB绝路航标_B":26.3544649049,"JLHB绝路航标_VAR2":27.349982327,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":122.2482435597,"BRAR情绪指标_AR":96.5397923875,"CR带状能量线_CR":114.006514658,"CR带状能量线_MA1":null,"CR带状能量线_MA2":null,"CR带状能量线_MA3":null,"CR带状能量线_MA4":null,"MASS梅斯线_MASS":24.5172450982,"MASS梅斯线_MAMASS":24.487874734,"PSY心理线_PSY":41.6666666667,"PSY心理线_PSYMA":51.3888888889,"VR成交量变异率_VR":123.9146078255,"VR成交量变异率_MAVR":125.7549279682,"WAD威廉多空力度线_WAD":0.847,"WAD威廉多空力度线_MAWAD":0.8538333333,"PCNT幅度比_PCNT":-1.3388734995,"PCNT幅度比_MAPCNT":-0.7489397273,"CYR市场强弱_CYR":-0.2493264043,"CYR市场强弱_MACYR":-0.1002245262,"AMO成交金额_AMOW":31426.1068,"AMO成交金额_AMO1":28195.00074,"AMO成交金额_AMO2":31471.03465,"OBV累积能量线_OBV":234020779,"OBV累积能量线_MAOBV":233962951.2333333194,"VOL成交量_MAVOL1":1281603.0,"VOL成交量_MAVOL2":1415733.2,"VRSI相对强弱量_RSI1":50.1947330292,"VRSI相对强弱量_RSI2":47.4385866476,"VRSI相对强弱量_RSI3":46.6983976424,"HSL换手线_HSL":1444993,"HSL换手线_MAHSL":1281603.0,"MA均线_MA1":2.2024,"MA均线_MA2":2.2217,"MA均线_MA3":2.19345,"MA均线_MA4":2.1896,"ACD升降线_ACD":0.847,"ACD升降线_MAACD":0.8794885826,"BBI多空均线":2.2038333333,"EXPMA指数平均线_EXP1":2.2078441958,"EXPMA指数平均线_EXP2":2.1707625149,"HMA高价平均线_HMA1":2.2225,"HMA高价平均线_HMA2":2.2405,"HMA高价平均线_HMA3":2.1845666667,"HMA高价平均线_HMA4":2.2068285714,"HMA高价平均线_HMA5":2.1583555556,"LMA低价平均线_LMA1":2.207,"LMA低价平均线_LMA2":2.2188333333,"LMA低价平均线_LMA3":2.1623666667,"LMA低价平均线_LMA4":2.1629857143,"LMA低价平均线_LMA5":2.1196222222,"VMA变异平均线_VMA1":2.215375,"VMA变异平均线_VMA2":2.2296666667,"VMA变异平均线_VMA3":2.1737,"VMA变异平均线_VMA4":2.1860857143,"VMA变异平均线_VMA5":2.1399638889,"AMV成本均线_AMV1":2.2026804173,"AMV成本均线_AMV2":2.2331795613,"AMV成本均线_AMV3":2.1740412725,"AMV成本均线_AMV4":2.2069337452,"BBIBOLL多空布林线_BBIBOLL":2.2038333333,"BBIBOLL多空布林线_UPR":2.2596011154,"BBIBOLL多空布林线_DWN":2.1480655512,"ALLIGAT鳄鱼线_上唇":2.2382,"ALLIGAT鳄鱼线_牙齿":2.2469375,"ALLIGAT鳄鱼线_下颚":2.1690769231,"GMMA顾比均线_MA3":2.18634427,"GMMA顾比均线_MA5":2.1985973388,"GMMA顾比均线_MA8":2.2070781726,"GMMA顾比均线_MA10":2.2083897537,"GMMA顾比均线_MA12":2.2078441958,"GMMA顾比均线_MA15":2.2054175829,"GMMA顾比均线_MA30":2.1911806607,"GMMA顾比均线_MA35":2.1866295952,"GMMA顾比均线_MA40":2.1817435769,"GMMA顾比均线_MA45":2.176445907,"GMMA顾比均线_MA50":2.1707625149,"GMMA顾比均线_MA60":2.1585414988,"BOLL布林线_BOLL":2.19345,"BOLL布林线_UB":2.3344159179,"BOLL布林线_LB":2.0524840821,"PBX瀑布线_PBX1":2.2128718406,"PBX瀑布线_PBX2":2.2041875407,"PBX瀑布线_PBX3":2.1957633343,"PBX瀑布线_PBX4":2.1884359525,"PBX瀑布线_PBX5":2.1856359198,"PBX瀑布线_PBX6":2.1648084104,"ENE轨道线_UPPER":2.3100368,"ENE轨道线_LOWER":2.0485232,"ENE轨道线_ENE":2.17928,"MIKE麦克支撑压力_STOR":2.4006161995,"MIKE麦克支撑压力_MIDR":2.3485900099,"MIKE麦克支撑压力_WEKR":2.2965638203,"MIKE麦克支撑压力_WEKS":2.1833344944,"MIKE麦克支撑压力_MIDS":2.1221313581,"MIKE麦克支撑压力_STOS":2.0609282218,"XS薛斯通道_SUP":2.3370649413,"XS薛斯通道_SDN":2.0724915517,"XS薛斯通道_LUP":2.5279302404,"XS薛斯通道_LDN":1.9070350936,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.292,"MA交易_MA1":2.2024,"MA交易_MA2":2.19345,"MA交易_平空开多":false,"MA交易_平多开空":false,"MACD交易_DIFF":0.0131082882,"MACD交易_DEA":0.0188468866,"MACD交易_MACD":-0.0114771969,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":20.8412428354,"KDJ交易_D":38.3327077694,"KDJ交易_J":-14.1416870326,"KDJ交易_平空开多":false,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4746745981,"SG_XDT心电图_MQR1":0.4769489983,"SG_XDT心电图_MQR2":0.4776352817,"SG_NDB脑电波_DK":3.292,"SG_NDB脑电波_MDK1":3.3058,"SG_NDB脑电波_MDK2":3.2825,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":20.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":17288.6822645986,"LON龙系长线_LONMA":20528.8686859305,"LON龙系长线_LONT":17288.6822645986,"SHT龙系短线_SHT":-0.7526447087,"SHT龙系短线_SHTMA":1.1875076887,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":45.5536152755,"ZLMM主力买卖_MMM":54.4097799624,"ZLMM主力买卖_MML":54.2502036879,"SLZT神龙在天_白龙":2.035352,"SLZT神龙在天_黄龙":2.3915364855,"SLZT神龙在天_紫龙":1.6575484313,"SLZT神龙在天_青龙":2.0820122886,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30028.6924229298,"ADVOL龙系离散量_MA1":29750.8027192839,"ADVOL龙系离散量_MA2":28592.2194460718,"CYS市场盈亏":-1.9290672101,"CYW主力控盘":110.3876011052,"JAX济安线_J":2.1890391247,"JAX济安线_A":2.1829408216,"JAX济安线_X":2.1829408216,"XJDX超级短线_J":-0.3210241062,"XJDX超级短线_D":-0.2052006529,"XJDX超级短线_K":-0.3210241062,"ZJTJ庄家抬轿_无庄控盘":-0.5667017818,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":0.0,"BDZX波段之星_AK":52.5801731509,"BDZX波段之星_AD1":56.8299253681,"BDZX波段之星_AJ":44.0806687164,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":0.0411556382,"LHXJ猎狐先觉_主力控盘":-0.0411556382,"LYJH猎鹰歼狐_机构做空能量线":41.1193511032,"LYJH猎鹰歼狐_机构做多能量线":26.2212745985,"JFZX飓风智能中线_多头力量":54.4804795638,"JFZX飓风智能中线_空头力量":45.5195204362,"CYHT财运亨通_SK":65.592102423,"CYHT财运亨通_SD":66.5723130388,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":null,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":2.166,"CDP_STD逆势操作_CDP":2.194,"CDP_STD逆势操作_AH":2.214,"CDP_STD逆势操作_NH":2.201,"CDP_STD逆势操作_NL":2.188,"CDP_STD逆势操作_AL":2.175,"Alpha001":-0.2830347746,"Alpha002":1.0826210826,"Alpha003":-21.998,"Alpha004":1,"Alpha005":-8.177564889e-16,"Alpha006":-0.2064364207,"Alpha007":0.9224174724,"Alpha008":-0.0659340659,"Alpha009":-0.0000000001,"Alpha010":0.9522653722,"Alpha011":1384777.9601139179,"Alpha012":-0.0208386816,"Alpha013":-215.305303357,"Alpha014":-0.108,"Alpha015":-0.0022779043,"Alpha016":-0.8838304553,"Alpha017":1.2671683181,"Alpha018":0.9525065963,"Alpha019":-0.0474934037,"Alpha020":-4.3286219081,"Alpha021":-0.0025619048,"Alpha022":-0.0047432917,"Alpha023":46.4024813387,"Alpha024":-0.0252519982,"Alpha025":-0.0832187422,"Alpha026":0.9801376992,"Alpha027":-120.5649048639,"Alpha028":-19.5323944029,"Alpha029":-62548.2835689046,"Alpha030":0.0002247467,"Alpha031":-2.8118456476,"Alpha032":-0.4804381847,"Alpha033":0.0250184087,"Alpha034":1.0289319791,"Alpha035":-0.1685303514,"Alpha036":0.5868544601,"Alpha037":1.2294936614,"Alpha038":0.0,"Alpha039":0.399375975,"Alpha040":106.3638622963,"Alpha041":-0.0974842767,"Alpha042":-0.1003231903,"Alpha043":-3149388.0,"Alpha044":1.0666666667,"Alpha045":0.0909436065,"Alpha046":1.0174669129,"Alpha047":58.6710720712,"Alpha048":-0.0554115422,"Alpha049":0.5799373041,"Alpha050":-0.1598746082,"Alpha051":0.4200626959,"Alpha052":118.045112782,"Alpha053":41.6666666667,"Alpha054":-0.3813291139,"Alpha055":0.6294466541,"Alpha056":-0.0344044844,"Alpha057":11.9368484335,"Alpha058":50.0,"Alpha059":0.051,"Alpha060":4855361.6805599239,"Alpha061":-0.5304212168,"Alpha062":0.6956869346,"Alpha063":32.9079582883,"Alpha064":-0.6146645866,"Alpha065":1.0223145583,"Alpha066":-2.1827487581,"Alpha067":49.336028594,"Alpha068":-0.0000000001,"Alpha069":-0.8086419753,"Alpha070":62720329.2067588344,"Alpha071":-0.7029339853,"Alpha072":54.9892747778,"Alpha073":-0.1873054262,"Alpha074":0.6583463339,"Alpha075":0.3461538462,"Alpha076":0.6790590813,"Alpha077":0.0171606864,"Alpha078":-67.5088428499,"Alpha079":44.4756431052,"Alpha080":-5.8855367188,"Alpha081":1601249.3451500521,"Alpha082":53.6863570523,"Alpha083":-0.3799058085,"Alpha084":1889319.0,"Alpha085":0.56875,"Alpha086":1.0,"Alpha087":-0.2146200134,"Alpha088":2.2662889518,"Alpha089":-0.0114771969,"Alpha090":-0.1918876755,"Alpha091":-0.0447632874,"Alpha092":-0.4666666667,"Alpha093":0.157,"Alpha094":5203281.0,"Alpha095":86924720.2717819363,"Alpha096":27.6714698517,"Alpha097":292220.616407674,"Alpha098":0.034,"Alpha099":-0.4222919937,"Alpha100":368664.8142954717,"Alpha101":-0.1700468019,"Alpha102":50.1947330292,"Alpha103":15.0,"Alpha104":0.8651095886,"Alpha105":-0.1843267436,"Alpha106":0.048,"Alpha107":-0.0463688612,"Alpha108":-0.0054465602,"Alpha109":0.9389372766,"Alpha110":113.3879781421,"Alpha111":540849.6857279302,"Alpha112":-29.5454545455,"Alpha113":0.2494152808,"Alpha114":242.2701083375,"Alpha115":0.8766376609,"Alpha116":0.0085195489,"Alpha117":0.2563476562,"Alpha118":83.9826839827,"Alpha119":0.7566302652,"Alpha120":0.9802776033,"Alpha121":-0.1159793464,"Alpha122":0.0021783749,"Alpha123":-0.2650773415,"Alpha124":-77.5818123253,"Alpha125":0.9,"Alpha126":2.1736666667,"Alpha127":2.3613248177,"Alpha128":52.2073064654,"Alpha129":0.171,"Alpha130":1.0142857143,"Alpha131":0.2780864852,"Alpha132":334946036.7499999404,"Alpha133":35.0,"Alpha134":-50227.0294117646,"Alpha135":1.0184588492,"Alpha136":-0.0860921407,"Alpha137":-0.6162424242,"Alpha138":-0.2892801426,"Alpha139":-0.1428143062,"Alpha140":0.3333333333,"Alpha141":-0.4894991922,"Alpha142":-0.0129345903,"Alpha143":-0.0076853526,"Alpha144":0.0,"Alpha145":-14.5695145346,"Alpha146":-0.4825886378,"Alpha147":0.0106984266,"Alpha148":0.8319545968,"Alpha149":0.8422423057,"Alpha150":3140933.1176666673,"Alpha151":0.0367842352,"Alpha152":0.00583054,"Alpha153":2.2038333333,"Alpha154":-5.1939260303,"Alpha155":33925.0266795877,"Alpha156":-0.8315132605,"Alpha157":0.6307086614,"Alpha158":0.012465374,"Alpha159":-6012.4692228034,"Alpha160":0.0323465555,"Alpha161":0.0324166667,"Alpha162":0.0,"Alpha163":0.8923556942,"Alpha164":183625.2542435429,"Alpha165":-6.1548744945,"Alpha166":-0.0002586196,"Alpha167":0.093,"Alpha168":-0.9490385503,"Alpha169":0.0029992555,"Alpha170":0.0383126612,"Alpha171":-0.0845314463,"Alpha172":28.8753674632,"Alpha173":2.9998206918,"Alpha174":0.0280042896,"Alpha175":0.0308333333,"Alpha176":0.110546318,"Alpha177":50.0,"Alpha178":-19091.0236902049,"Alpha179":0.1203365451,"Alpha180":-1444993.0,"Alpha181":0.0090476206,"Alpha182":0.65,"Alpha183":15.7054324106,"Alpha184":0.8377535101,"Alpha185":-0.0001227738,"Alpha186":31.2207917954,"Alpha187":0.364,"Alpha188":42.5536709262,"Alpha189":0.0295555556,"Alpha190":-0.5820932845,"Alpha191":0.6185781038},{"date":"2026-08-25","证券代码":"513100.SH","证券名称":"纳指ETF国泰","open":2.159,"high":2.209,"low":2.154,"close":2.195,"volume":2536518,"amount":553824482.0,"5日涨跌幅":-1.9651630192,"10日涨跌幅":-0.9029345372,"20日涨跌幅":6.1411992263,"30日涨跌幅":1.1520737327,"60日涨跌幅":-7.1881606765,"120日涨跌幅":22.9003359462,"六脉神剑":0,"小波段交易":false,"大波段交易":false,"波段超级买卖":true,"价格距离5日均线涨跌幅":0.0638220277,"价格距离10日均线涨跌幅":-1.112762986,"价格距离20日均线涨跌幅":-0.2182016547,"价格距离30日均线涨跌幅":0.9427454587,"价格距离60日均线涨跌幅":0.3765071719,"价格距离120日均线涨跌幅":7.1921278492,"5日均线距离10日均线涨跌幅":-1.1758345722,"10日均线距离20日均线涨跌幅":0.9046276934,"20日均线距离30日均线涨跌幅":1.1634858588,"30日均线距离60日均线涨跌幅":-0.5609499566,"60日均线距离120日均线涨跌幅":6.7900556308,"5日偏度":-1.2495275231,"10日偏度":0.2341453243,"20日偏度":-1.1001495855,"30日偏度":-0.1915031297,"60日偏度":0.0558949739,"120日偏度":-0.5533115521,"5日峰度":2.6228834802,"10日峰度":-0.4001037885,"20日峰度":0.5800241632,"30日峰度":-1.092107235,"60日峰度":-0.2204248202,"120日峰度":-1.1025882825,"KDJ_KD金叉":false,"KDJ_KD死叉":false,"RSI_金叉":false,"RSI_死叉":false,"WR_金叉":false,"MACD_金叉":false,"MACD_死叉":false,"PSY_金叉":false,"PSY_死叉":false,"5日均线":2.1936,"10日均线":2.2197,"20日均线":2.1998,"30日均线":2.1745,"60日均线":2.1867666667,"120日均线":2.047725,"5日10日金叉":false,"10日20日金叉":false,"20日30日金叉":false,"30日60日金叉":false,"60日120日金叉":false,"5日10日死叉":false,"10日20日死叉":false,"20日30日死叉":false,"30日60日死叉":false,"60日120日死叉":false,"连续上涨天数":1.0,"连续下跌天数":0.0,"价格在5均线上":true,"价格在10均线上":false,"价格在20均线上":false,"价格在30均线上":true,"价格在60均线上":true,"价格在120均线上":true,"5均线在10均线上":false,"10均线在20均线上":true,"20均线在30均线上":true,"30均线在60均线上":false,"60均线在120均线上":true,"5日Alpha":0.1377569775,"10日Alpha":0.1269457602,"20日Alpha":1.2710982591,"30日Alpha":0.5693862876,"60日Alpha":-0.090502889,"120日Alpha":0.6394382601,"5日Beta":0.5964151714,"10日Beta":0.5581784862,"20日Beta":1.0408765598,"30日Beta":0.7827275814,"60日Beta":0.7796429277,"120日Beta":0.8639245798,"5日夏普比率":-4.7761590934,"10日夏普比率":-1.105929696,"20日夏普比率":2.9441312971,"30日夏普比率":0.4991883371,"60日夏普比率":-0.9879898891,"120日夏普比率":1.663244777,"5日年化波动率":0.2054808744,"10日年化波动率":0.1916257827,"20日年化波动率":0.2668442459,"30日年化波动率":0.2558946754,"60日年化波动率":0.2784272031,"120日年化波动率":0.2845595206,"5日最大回撤":-0.032603841,"10日最大回撤":-0.0474934037,"20日最大回撤":-0.0474934037,"30日最大回撤":-0.0671846435,"60日最大回撤":-0.1369978858,"120日最大回撤":-0.1369978858,"5日上涨捕获率":-0.1939229465,"10日上涨捕获率":0.7217204527,"20日上涨捕获率":3.7915339021,"30日上涨捕获率":1.2386123408,"60日上涨捕获率":0.4715700446,"120日上涨捕获率":0.9452514803,"5日下跌捕获率":0.7910545231,"10日下跌捕获率":0.871481572,"20日下跌捕获率":0.9624902379,"30日下跌捕获率":0.9410338735,"60日下跌捕获率":0.9724568533,"120日下跌捕获率":0.8671528024,"3日回归动量":-0.0102246604,"5日回归动量":-0.0889587906,"7日回归动量":-0.4862092361,"9日回归动量":-0.4525542164,"12日回归动量":-0.2638818733,"15日回归动量":-0.2716088227,"18日回归动量":0.0029789066,"20日回归动量":0.0277941333,"23日回归动量":0.1695642683,"25日回归动量":0.2185772157,"28日回归动量":0.2976547917,"30日回归动量":0.2256864861,"35日回归动量":0.1372640618,"40日回归动量":0.0701256706,"45日回归动量":0.029338963,"50日回归动量":0.0006220847,"60日回归动量":-0.0002519468,"5日最高值到当前周期":3.0,"10日最高值到当前周期":6.0,"20日最高值到当前周期":6.0,"30日最高值到当前周期":6.0,"60日最高值到当前周期":59.0,"120日最高值到当前周期":60.0,"5日最低值到当前周期":1.0,"10日最低值到当前周期":1.0,"20日最低值到当前周期":18.0,"30日最低值到当前周期":18.0,"60日最低值到当前周期":18.0,"120日最低值到当前周期":100.0,"5日回归斜率":-0.0056,"10日回归斜率":-0.0076909091,"20日回归斜率":0.0050496241,"30日回归斜率":0.0045746385,"60日回归斜率":-0.0003957766,"120日回归斜率":0.0045625425,"5日标准差":0.0151340675,"10日标准差":0.0314866638,"20日标准差":0.0643487374,"30日标准差":0.0663152823,"60日标准差":0.0616174669,"120日标准差":0.1908351366,"CCI商品路径指标":-105.3724053724,"MFI最近流量指标":52.6323493007,"MTM动量线_MTM值":-0.071,"MTM动量线_MTMMA值":-0.0001666667,"RSI相对强弱_RSI1":45.6504934991,"RSI相对强弱_RSI2":49.6052610763,"RSI相对强弱_RSI3":51.6046162077,"KDJ指标_K值":25.2830507792,"KDJ指标_D值":33.982822106,"KDJ指标_J值":7.8835081255,"SKDJ慢速随机_K值":21.9876116712,"SKDJ慢速随机_D值":24.7249664282,"UDL引力线_UDL值":2.1996083333,"UDL引力线_MAUDL值":2.2153888889,"WR威廉指标_WR1":65.8333333333,"WR威廉指标_WR2":55.9139784946,"LWR指标_LWR1":74.7169492208,"LWR指标_LWR2":66.017177894,"MARSI相对强弱平均线_RSI1":54.1613723251,"MARSI相对强弱平均线_RSI2":43.6893463116,"BIAS乖离率_BIAS1":-0.2801544635,"BIAS乖离率_BIAS2":-1.2484534923,"BIAS乖离率_BIAS3":0.5017456169,"BIAS_QL乖离率传统版_BIAS值":-0.2801544635,"BIAS_QL乖离率传统版_BIASMA值":-1.1512409313,"BIAS36三六乖离_BIAS36":-0.0158333333,"BIAS36三六乖离_BIAS612":-0.0215833333,"BIAS36三六乖离_MABIAS":-0.0114166667,"ACCER幅度涨速":-0.0061991539,"ASI振动升降指标_ASI":1.2256098081,"ASI振动升降指标_ASIT":0.4857883773,"CHO佳庆指标_CHO":3383.2118156566,"CHO佳庆指标_MACHO":4856.2332562185,"DMA_XT平均差_DIF":0.03746,"DMA_XT平均差_DIFMA":0.047952,"DMI趋向指标_PDI":-39.6226415094,"DMI趋向指标_MDI":41.0901467505,"DMI趋向指标_ADX":-864.5021645024,"DMI趋向指标_ADXR":-1588.0394313291,"DPO区间震荡线_DPO":-0.0524285714,"DPO区间震荡线_MADPO":-0.0333809524,"EMV简易波动指标_EMV":-0.2059260472,"EMV简易波动指标_MAEMV":0.1573568392,"MACD平滑异同平均线_DIF":0.0111126956,"MACD平滑异同平均线_DEA":0.0173000484,"MACD平滑异同平均线_MACD":-0.0123747056,"VMACD量平滑异同平均线_DIF":-178395.6015341729,"VMACD量平滑异同平均线_DEA":-291597.2574810259,"VMACD量平滑异同平均线_MACD":113201.655946853,"SMACD单线平滑异同平均线_DEA":0.0173000484,"SMACD单线平滑异同平均线_MACD":0.0111126956,"QACD快速异同平均线_DIF":0.0,"QACD快速异同平均线_MACD":0.0,"QACD快速异同平均线_DDIF":0.0,"TRIX三重指数平均线_TRIX":0.147204134,"TRIX三重指数平均线_MATRIX":0.1786035542,"UOS终极指标_UOS":41.7014109721,"UOS终极指标_MAUOS":46.7628745349,"VTP量价曲线_VPT":80344.1122789755,"VTP量价曲线_MAVP":104781.7133997819,"WVAD威廉变异离散量_WVAD":382.3232860706,"WVAD威廉变异离散量_MAWVAD":294.0496625909,"JS加数线_JS":-0.3930326038,"JS加数线_MAJS1":-0.4623660705,"JS加数线_MAJS2":-0.2519924269,"JS加数线_MAJS3":0.2124187427,"CYE市场趋势_CYEL":-0.3995641119,"CYE市场趋势_CYES":0.1907175003,"GDX轨道线_轨道":0.0072864435,"GDX轨道线_压力线":0.0079422234,"GDX轨道线_支撑线":0.0066306636,"JLHB绝路航标_B":25.9632893703,"JLHB绝路航标_VAR2":27.0726437357,"JLHB绝路航标_绝路航标":50,"BRAR情绪指标_BR":130.0469483568,"BRAR情绪指标_AR":113.1672597865,"CR带状能量线_CR":121.2418300654,"CR带状能量线_MA1":136.8271696104,"CR带状能量线_MA2":136.6036527339,"CR带状能量线_MA3":137.188611716,"CR带状能量线_MA4":138.2253463744,"MASS梅斯线_MASS":24.4927966562,"MASS梅斯线_MAMASS":24.533534943,"PSY心理线_PSY":41.6666666667,"PSY心理线_PSYMA":47.2222222222,"VR成交量变异率_VR":151.9972682395,"VR成交量变异率_MAVR":127.7650580114,"WAD威廉多空力度线_WAD":0.888,"WAD威廉多空力度线_MAWAD":0.8550666667,"PCNT幅度比_PCNT":1.3211845103,"PCNT幅度比_MAPCNT":-0.0588983148,"CYR市场强弱_CYR":-0.2549212726,"CYR市场强弱_MACYR":-0.1685844912,"AMO成交金额_AMOW":55382.4482,"AMO成交金额_AMO1":34276.26986,"AMO成交金额_AMO2":32739.39015,"OBV累积能量线_OBV":236557297,"OBV累积能量线_MAOBV":234125560.3333333433,"VOL成交量_MAVOL1":1565804.8,"VOL成交量_MAVOL2":1477749.3999999999,"VRSI相对强弱量_RSI1":68.9676306154,"VRSI相对强弱量_RSI2":57.9629251803,"VRSI相对强弱量_RSI3":51.2759809571,"HSL换手线_HSL":2536518,"HSL换手线_MAHSL":1565804.8,"MA均线_MA1":2.1936,"MA均线_MA2":2.2197,"MA均线_MA3":2.1998,"MA均线_MA4":2.1867666667,"ACD升降线_ACD":0.888,"ACD升降线_MAACD":0.8802991938,"BBI多空均线":2.1983229167,"EXPMA指数平均线_EXP1":2.2058681657,"EXPMA指数平均线_EXP2":2.1717130045,"HMA高价平均线_HMA1":2.2116666667,"HMA高价平均线_HMA2":2.2350833333,"HMA高价平均线_HMA3":2.1858333333,"HMA高价平均线_HMA4":2.2085285714,"HMA高价平均线_HMA5":2.1620777778,"LMA低价平均线_LMA1":2.189,"LMA低价平均线_LMA2":2.2118333333,"LMA低价平均线_LMA3":2.1629666667,"LMA低价平均线_LMA4":2.1643285714,"LMA低价平均线_LMA5":2.1229333333,"VMA变异平均线_VMA1":2.2005,"VMA变异平均线_VMA2":2.2233125,"VMA变异平均线_VMA3":2.1743916667,"VMA变异平均线_VMA4":2.1876428571,"VMA变异平均线_VMA5":2.1434833333,"AMV成本均线_AMV1":2.1889003242,"AMV成本均线_AMV2":2.2253114934,"AMV成本均线_AMV3":2.1748913035,"AMV成本均线_AMV4":2.2015120071,"BBIBOLL多空布林线_BBIBOLL":2.1983229167,"BBIBOLL多空布林线_UPR":2.2536702282,"BBIBOLL多空布林线_DWN":2.1429756051,"ALLIGAT鳄鱼线_上唇":2.2347,"ALLIGAT鳄鱼线_牙齿":2.247,"ALLIGAT鳄鱼线_下颚":2.1783846154,"GMMA顾比均线_MA3":2.190672135,"GMMA顾比均线_MA5":2.1973982259,"GMMA顾比均线_MA8":2.2043941342,"GMMA顾比均线_MA10":2.2059552531,"GMMA顾比均线_MA12":2.2058681657,"GMMA顾比均线_MA15":2.2041153851,"GMMA顾比均线_MA30":2.1914270697,"GMMA顾比均线_MA35":2.1870946177,"GMMA顾比均线_MA40":2.1823902316,"GMMA顾比均线_MA45":2.1772526067,"GMMA顾比均线_MA50":2.1717130045,"GMMA顾比均线_MA60":2.1597368595,"BOLL布林线_BOLL":2.1998,"BOLL布林线_UB":2.3284974747,"BOLL布林线_LB":2.0711025253,"PBX瀑布线_PBX1":2.2132314377,"PBX瀑布线_PBX2":2.2023978466,"PBX瀑布线_PBX3":2.1979680749,"PBX瀑布线_PBX4":2.1895421717,"PBX瀑布线_PBX5":2.1860153746,"PBX瀑布线_PBX6":2.1657913765,"ENE轨道线_UPPER":2.3127928,"ENE轨道线_LOWER":2.0509672,"ENE轨道线_ENE":2.18188,"MIKE麦克支撑压力_STOR":2.3969719791,"MIKE麦克支撑压力_MIDR":2.3427961997,"MIKE麦克支撑压力_WEKR":2.2886204202,"MIKE麦克支撑压力_WEKS":2.1745878959,"MIKE麦克支撑压力_MIDS":2.114731151,"MIKE麦克支撑压力_STOS":2.0548744061,"XS薛斯通道_SUP":2.3361048521,"XS薛斯通道_SDN":2.0716401519,"XS薛斯通道_LUP":2.5233509878,"XS薛斯通道_LDN":1.9035805698,"TQN唐奇安通道_周期高点":2.292,"TQN唐奇安通道_周期低点":2.035,"TQN唐奇安通道_平空开多":false,"TQN唐奇安通道_平多开空":false,"SAR抛物线指标":2.292,"MA交易_MA1":2.1936,"MA交易_MA2":2.1998,"MA交易_平空开多":false,"MA交易_平多开空":true,"MACD交易_DIFF":0.0111126956,"MACD交易_DEA":0.0173000484,"MACD交易_MACD":-0.0123747056,"MACD交易_平空开多":false,"MACD交易_平多开空":false,"KDJ交易_K":25.2830507792,"KDJ交易_D":33.982822106,"KDJ交易_J":7.8835081255,"KDJ交易_平空开多":true,"KDJ交易_平多开空":false,"SG_XDT心电图_QR":0.4822021281,"SG_XDT心电图_MQR1":0.4786332613,"SG_XDT心电图_MQR2":0.4783619222,"SG_NDB脑电波_DK":3.293,"SG_NDB脑电波_MDK1":3.3034,"SG_NDB脑电波_MDK2":3.2903,"SG_SMX生命线_ZY1":null,"SG_SMX生命线_ZY2":null,"SG_SMX生命线_ZY3":null,"SG_LB量比_量比":null,"SG_LB量比_MA5":null,"SG_LB量比_MA10":null,"SG_PF强势股评分":25.0,"RAD威力雷达_RADER1":null,"RAD威力雷达_RADERMA":null,"LON龙系长线_LON":16354.5392031558,"LON龙系长线_LONMA":20120.3775589395,"LON龙系长线_LONT":16354.5392031558,"SHT龙系短线_SHT":0.6404714395,"SHT龙系短线_SHTMA":0.7318449785,"ZLJC主力进出_JCS":5671.4612723812,"ZLJC主力进出_JCM":5671.4612723812,"ZLJC主力进出_JCL":5671.4612723812,"ZLMM主力买卖_MMS":44.5512079147,"ZLMM主力买卖_MMM":52.218986174,"ZLMM主力买卖_MML":54.0977288892,"SLZT神龙在天_白龙":2.038328,"SLZT神龙在天_黄龙":2.3955812912,"SLZT神龙在天_紫龙":1.6598921569,"SLZT神龙在天_青龙":2.0862120429,"SLZT神龙在天_红龙":2.13891,"SLZT神龙在天_蓝龙":2.08572,"ADVOL龙系离散量_ADVOL":30153.2123974752,"ADVOL龙系离散量_MA1":29765.1541852549,"ADVOL龙系离散量_MA2":28618.9879940326,"CYS市场盈亏":-0.3620230815,"CYW主力控盘":391.700339287,"JAX济安线_J":2.1886445624,"JAX济安线_A":2.1798509356,"JAX济安线_X":2.1798509356,"XJDX超级短线_J":-0.3338324002,"XJDX超级短线_D":-0.285408862,"XJDX超级短线_K":-0.3338324002,"ZJTJ庄家抬轿_无庄控盘":-0.689310363,"ZJTJ庄家抬轿_开始控盘":0,"ZJTJ庄家抬轿_有庄控盘":0.0,"ZJTJ庄家抬轿_主力出货":0.0,"BDZX波段之星_AK":47.86555766,"BDZX波段之星_AD1":50.8536802294,"BDZX波段之星_AJ":41.8893125213,"BDZX波段之星_买进":20,"BDZX波段之星_卖出":20,"LHXJ猎狐先觉_主力弃盘":0.0415829785,"LHXJ猎狐先觉_主力控盘":-0.0415829785,"LYJH猎鹰歼狐_机构做空能量线":39.4312708823,"LYJH猎鹰歼狐_机构做多能量线":26.2103530122,"JFZX飓风智能中线_多头力量":54.194318753,"JFZX飓风智能中线_空头力量":45.805681247,"CYHT财运亨通_SK":64.4152428773,"CYHT财运亨通_SD":65.493777958,"CYHT财运亨通_卖出":78,"CYHT财运亨通_买进":22,"BSQJ买卖区间_B买":null,"BSQJ买卖区间_持仓":null,"BSQJ买卖区间_S卖":null,"BSQJ买卖区间_空仓":2.195,"CDP_STD逆势操作_CDP":2.1736666667,"CDP_STD逆势操作_AH":2.2103333333,"CDP_STD逆势操作_NH":2.1833333333,"CDP_STD逆势操作_NL":2.1563333333,"CDP_STD逆势操作_AL":2.1293333333,"Alpha001":-0.6069781311,"Alpha002":-1.3427609428,"Alpha003":-21.998,"Alpha004":1,"Alpha005":-0.3034330425,"Alpha006":-0.2064364207,"Alpha007":1.5588436576,"Alpha008":-0.328100471,"Alpha009":-0.0000000001,"Alpha010":0.9522653722,"Alpha011":1094620.7055684456,"Alpha012":-0.0269703193,"Alpha013":-216.1591235156,"Alpha014":-0.044,"Alpha015":-0.0032317636,"Alpha016":-0.6405023548,"Alpha017":1.0896991484,"Alpha018":0.9803483698,"Alpha019":-0.0196516302,"Alpha020":-3.4740545295,"Alpha021":-0.0052095238,"Alpha022":-0.0036931703,"Alpha023":49.32040805,"Alpha024":-0.0290015986,"Alpha025":-0.1452245297,"Alpha026":0.9409067808,"Alpha027":-181.0729208208,"Alpha028":0.4694340572,"Alpha029":-88120.0184696573,"Alpha030":0.000214053,"Alpha031":-1.2484534923,"Alpha032":-0.9827856025,"Alpha033":0.0327176287,"Alpha034":1.012642369,"Alpha035":-0.054313099,"Alpha036":0.3599374022,"Alpha037":0.3408776197,"Alpha038":0.0,"Alpha039":0.4586583463,"Alpha040":130.3768667899,"Alpha041":-0.0172955975,"Alpha042":0.1064162412,"Alpha043":-2148227.0,"Alpha044":1.0666666667,"Alpha045":0.5607462988,"Alpha046":1.0015138573,"Alpha047":58.3647283405,"Alpha048":-0.0649297622,"Alpha049":0.5987055016,"Alpha050":-0.1974110032,"Alpha051":0.4012944984,"Alpha052":125.7164404223,"Alpha053":41.6666666667,"Alpha054":-0.4746835443,"Alpha055":1.5562471154,"Alpha056":-0.0413974914,"Alpha057":16.0134545112,"Alpha058":55.0,"Alpha059":0.142,"Alpha060":6788120.8704588963,"Alpha061":-0.6099843994,"Alpha062":0.0231394828,"Alpha063":45.6504934991,"Alpha064":-0.6209048362,"Alpha065":1.0028094153,"Alpha066":-0.2801544635,"Alpha067":51.6046162077,"Alpha068":-0.0,"Alpha069":-0.6728395062,"Alpha070":124579366.4509005696,"Alpha071":0.5017456169,"Alpha072":55.0509216923,"Alpha073":-0.0542315417,"Alpha074":0.3057722309,"Alpha075":0.3461538462,"Alpha076":0.683405361,"Alpha077":0.0187207488,"Alpha078":-52.652259332,"Alpha079":49.6052610763,"Alpha080":127.3866010942,"Alpha081":1690322.5503738564,"Alpha082":53.7977381244,"Alpha083":-0.4615384615,"Alpha084":5663444.0,"Alpha085":1.0,"Alpha086":1.0,"Alpha087":-0.658792066,"Alpha088":6.1411992263,"Alpha089":-0.0123747056,"Alpha090":-0.3104524181,"Alpha091":-0.3036495277,"Alpha092":-0.4666666667,"Alpha093":0.132,"Alpha094":4878273.0,"Alpha095":97555161.7027771175,"Alpha096":23.7854647382,"Alpha097":439142.002759666,"Alpha098":0.017,"Alpha099":-0.4960753532,"Alpha100":425802.4759521912,"Alpha101":0.4555382215,"Alpha102":68.9676306154,"Alpha103":10.0,"Alpha104":0.7545366264,"Alpha105":0.5358939256,"Alpha106":0.127,"Alpha107":-0.0055999146,"Alpha108":-0.8664035525,"Alpha109":1.2272429005,"Alpha110":143.125,"Alpha111":-108600.0357519501,"Alpha112":-26.1992619926,"Alpha113":-0.1419632448,"Alpha114":568.8475195204,"Alpha115":0.9008931045,"Alpha116":0.0070082707,"Alpha117":0.068359375,"Alpha118":115.5339805825,"Alpha119":0.8439937598,"Alpha120":0.9800939033,"Alpha121":-0.5672518802,"Alpha122":0.001904939,"Alpha123":0.1253187149,"Alpha124":-77.8804011034,"Alpha125":1.6886792453,"Alpha126":2.186,"Alpha127":2.5654331638,"Alpha128":52.6323493007,"Alpha129":0.171,"Alpha130":1.6045751634,"Alpha131":0.7370380285,"Alpha132":349831763.0999999642,"Alpha133":35.0,"Alpha134":-79476.0714916155,"Alpha135":1.0186690512,"Alpha136":0.3432467935,"Alpha137":0.3102745098,"Alpha138":-0.1738355248,"Alpha139":0.4902426176,"Alpha140":0.3333333333,"Alpha141":-0.4491114701,"Alpha142":-0.1733960261,"Alpha143":0.013388735,"Alpha144":0.0,"Alpha145":-7.7847778297,"Alpha146":5.4700193863,"Alpha147":0.0092316434,"Alpha148":0.8301971276,"Alpha149":0.8413638515,"Alpha150":5544828.3480000002,"Alpha151":0.0412950234,"Alpha152":0.0075657084,"Alpha153":2.1983229167,"Alpha154":-0.9059917726,"Alpha155":113201.655946853,"Alpha156":-0.8673946958,"Alpha157":1.0307086614,"Alpha158":0.0250569476,"Alpha159":-5217.5538866432,"Alpha160":0.0307292277,"Alpha161":0.034,"Alpha162":0.2600309043,"Alpha163":0.0764430577,"Alpha164":164741.0217363376,"Alpha165":-3.2148973808,"Alpha166":-0.0019070097,"Alpha167":0.1,"Alpha168":-1.5977746587,"Alpha169":0.0029826404,"Alpha170":-0.0437367768,"Alpha171":-2.6961646472,"Alpha172":23.749600592,"Alpha173":2.9940593336,"Alpha174":0.0299050957,"Alpha175":0.038,"Alpha176":-0.0706402424,"Alpha177":45.0,"Alpha178":33960.7673130194,"Alpha179":0.2196256337,"Alpha180":0.65,"Alpha181":0.0108056177,"Alpha182":0.65,"Alpha183":15.9306897762,"Alpha184":0.3775351014,"Alpha185":-0.0002689899,"Alpha186":29.3600535744,"Alpha187":0.364,"Alpha188":115.7154108814,"Alpha189":0.0256388889,"Alpha190":-0.6106721507,"Alpha191":-0.5870215453}]