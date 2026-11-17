---
name: xiaoguo-qmt-assistant
description: |
  小果全能大QMT量化交易助手 - 专业级QMT策略开发全能助手
  本助手是专为「迅投QMT极速策略交易系统」打造的量化交易策略开发专家。由小果（微信：xg_quant）精心打造，深度封装了QMT平台的全部API接口、运行机制、数据结构和实战经验，能够根据用户的自然语言描述，自动生成从基础到高级、从回测到实盘的完整量化交易策略代码。

  【核心功能矩阵】
  ✅ 策略开发：根据需求描述自动生成QMT策略代码，支持股票/期货/期权/ETF/可转债/两融等多品种
  ✅ 策略回测：生成完整的回测模型代码，包含历史数据获取、撮合规则、绩效分析
  ✅ 实盘交易：生成实盘模型代码，支持逐K线生效和立即下单两种模式
  ✅ 代码检查：自动检测QMT策略常见错误（ContextInfo回滚、全局变量、白名单、阻塞操作等）
  ✅ 策略模板：提供双均线、MACD、RSI、布林带、网格交易、多因子选股等多种内置模板
  ✅ 函数查询：详细解释QMT全部API函数的用法、参数和示例
  ✅ 问题诊断：针对QMT运行报错提供解决方案和修复建议
  ✅ 数据管理：提供历史数据下载、财务数据获取、实时行情订阅的完整方案

  版本：2.0.0
  作者：小果
  微信：xg_quant
  更新日期：2026-08-31
---

# 小果大QMT量化交易系统助手
## 完整策略开发手册 v2.0 - 全函数库终极完整版

---

## 📖 第一部分：系统概述与核心规范

### 1.1 QMT系统简介
QMT（极速策略交易系统）是迅投科技推出的专业量化交易平台，内置Python 3.6运行环境，提供行情数据获取与交易下单两大核心功能。

### 1.2 QMT运行机制对比

| 机制类型 | 函数/方法 | 触发方式 | 适用场景 |
|:---|:---|:---|:---|
| **逐K线驱动** | `handlebar` | 历史K线逐根回放；盘中每个tick触发 | 传统趋势策略，需要回测验证 |
| **事件驱动** | `subscribe_quote` | 订阅品种新分笔到达时触发 | 盘中实时监控，高频交易 |
| **定时任务** | `run_time`/`schedule_run` | 固定时间间隔触发 | 轮询监控，固定频率执行 |

### 1.3 强制编码规范
```python
#coding:gbk  # 【必须】代码第一行，否则中文报错
# 【必须】缩进统一使用4个空格或Tab
# 【必须】必须定义 init 和 handlebar 函数
# 【禁止】使用 time.sleep()、死循环等阻塞操作
# 【禁止】在 ContextInfo 对象上存储状态
# 【推荐】使用全局类实例 g = G() 存储状态
1.4 回测与实盘核心差异
维度	回测模式	实盘模式
数据来源	本地历史数据 (subscribe=False)	实时订阅数据 (subscribe=True)
撮合规则	价格在K线高低点内按指定价，否则按收盘价	交易所实际规则：价格笼子、T+1、数量限制
成交确认	立即按规则撮合	等待交易所回报，异步处理
状态保存	每次handlebar调用自动保存	K线结束时的信号才生效，需用全局变量
策略模板
#coding:gbk
"""
策略名称: {策略名称}
策略描述: {策略描述}
作者: 小果
微信: xg_quant
创建日期: {日期}
运行模式: 回测/实盘
"""

# ==================== 导入依赖库 ====================
import pandas as pd
import numpy as np
import talib
import datetime
import time
import json
import os
import math
import random
from collections import defaultdict

# ==================== 全局变量定义 ====================
class G():
    """
    全局状态存储类
    注意：QMT的ContextInfo对象有逐K线回滚机制，不能直接在上面存属性
    所有策略状态必须使用全局类实例存储
    """
    pass

g = G()  # 实例化全局变量

# ==================== 必须函数1: init ====================
def init(ContextInfo):
    """
    【必须定义】策略初始化函数，策略启动时仅执行一次

    参数：
        ContextInfo: QMT上下文对象，包含K线信息和系统接口

    功能说明：
        1. 初始化策略参数和变量
        2. 设置交易标的和资金账号
        3. 订阅行情数据（如需）
        4. 注册定时任务（如需）
        5. 设置回测起止时间（回测模式）
        6. 设置回测初始资金（回测模式）
        7. 设置股票池和板块
        8. 初始化状态变量

    注意事项：
        - init执行完成前部分接口无法使用（如get_trading_dates）
        - 非VIP用户订阅数量有限制（通常300个）
        - 可使用ContextInfo.start/end设置回测区间
        - 可使用ContextInfo.capital设置初始资金
    """

    # -------- 1. 设置交易标的 --------
    g.stock = ContextInfo.stockcode + '.' + ContextInfo.market
    g.stock_name = ContextInfo.get_stock_name(g.stock)

    # -------- 2. 设置策略参数 --------
    g.fast_line = 10      # 快线周期
    g.slow_line = 20      # 慢线周期
    g.trade_amount = 10000 # 每次交易金额
    g.stop_loss = -0.05   # 止损比例
    g.take_profit = 0.10  # 止盈比例

    # -------- 3. 设置资金账号 --------
    if ContextInfo.do_back_test:
        g.accountid = "testS"  # 回测账号
    else:
        g.accountid = account   # 实盘账号（模型交易界面自动传入）
        g.account_type = accountType

    # -------- 4. 设置回测参数 --------
    if ContextInfo.do_back_test:
        ContextInfo.start = "2020-01-01 00:00:00"
        ContextInfo.end = "2023-12-31 00:00:00"
        ContextInfo.capital = 1000000

    # -------- 5. 初始化状态变量 --------
    g.position = 0        # 当前持仓数量
    g.avg_price = 0       # 持仓均价
    g.trade_count = 0     # 交易次数
    g.waiting_list = []   # 待确认委托列表
    g.order_ref = {}      # 委托记录

    print(f"策略初始化完成，交易标的: {g.stock} {g.stock_name}")

# ==================== 必须函数2: handlebar ====================
def handlebar(ContextInfo):
    """
    【必须定义】核心行情处理函数

    调用时机：
        - 回测模式：历史K线从左向右逐根调用
        - 实盘模式：每个新tick（约3秒）触发调用

    功能说明：
        1. 获取行情数据
        2. 计算技术指标
        3. 判断交易信号
        4. 执行下单操作
        5. 更新策略状态
    """

    # -------- 1. 跳过实盘历史K线 --------
    if not ContextInfo.do_back_test and not ContextInfo.is_last_bar():
        return

    # -------- 2. 获取当前K线信息 --------
    bar_date = timetag_to_datetime(
        ContextInfo.get_bar_timetag(ContextInfo.barpos),
        '%Y%m%d%H%M%S'
    )

    # -------- 3. 获取行情数据 --------
    data = ContextInfo.get_market_data_ex(
        fields=['open', 'high', 'low', 'close'],
        stock_list=[g.stock],
        period=ContextInfo.period,
        count=max(g.fast_line, g.slow_line) + 10,
        dividend_type='front_ratio',
        fill_data=True,
        subscribe=not ContextInfo.do_back_test
    )

    if g.stock not in data or len(data[g.stock]) < max(g.fast_line, g.slow_line):
        return

    close_prices = data[g.stock]['close'].values
    current_price = close_prices[-1]

    # -------- 4. 计算技术指标 --------
    fast_ma = np.mean(close_prices[-g.fast_line:])
    slow_ma = np.mean(close_prices[-g.slow_line:])

    # -------- 5. 获取账户与持仓信息 --------
    account_info = get_trade_detail_data(g.accountid, 'stock', 'account')
    if not account_info:
        return
    available_cash = account_info[0].m_dAvailable

    positions = get_trade_detail_data(g.accountid, 'stock', 'position')
    pos_dict = {p.m_strInstrumentID + '.' + p.m_strExchangeID: p.m_nVolume for p in positions}
    g.position = pos_dict.get(g.stock, 0)

    # -------- 6. 交易信号判断 --------
    signal = None

    if g.position == 0 and fast_ma > slow_ma:
        signal = 'buy'
    elif g.position > 0 and fast_ma < slow_ma:
        signal = 'sell'

    # -------- 7. 执行交易 --------
    if signal == 'buy':
        vol = int(g.trade_amount / current_price / 100) * 100
        if vol > 0 and available_cash > g.trade_amount:
            msg = f"{bar_date} 买入 {vol}股"
            passorder(23, 1101, g.accountid, g.stock, 5, current_price, vol,
                     '小果策略', 2 if not ContextInfo.do_back_test else 0, msg, ContextInfo)
            g.waiting_list.append(msg)
            g.trade_count += 1

    elif signal == 'sell' and g.position > 0:
        msg = f"{bar_date} 卖出 {g.position}股"
        passorder(24, 1101, g.accountid, g.stock, 5, current_price, g.position,
                 '小果策略', 2 if not ContextInfo.do_back_test else 0, msg, ContextInfo)
        g.waiting_list.append(msg)
        g.trade_count += 1

# ==================== 可选函数1: after_init ====================
def after_init(ContextInfo):
    """
    【可选定义】后初始化函数，在init完成后、handlebar前执行一次
    用于执行一次性操作、立即下单（需quickTrade=2）
    """
    # 可在此执行立即下单
    # passorder(23, 1101, g.accountid, g.stock, 5, -1, 100, '开盘买入', 2, '', ContextInfo)
    pass

# ==================== 可选函数2: stop ====================
def stop(ContextInfo):
    """
    【可选定义】策略停止函数，策略被停止时调用
    注意：stop被调用时交易连接已断开，不能下单
    """
    print(f"策略停止，共交易{g.trade_count}次")
############################
函数名	必须	调用时机	功能说明	参数	注意事项
init(ContextInfo)	✅	策略启动时执行一次	初始化策略参数、订阅行情、注册定时器、设置回测参数	ContextInfo	部分接口在init中不可用
handlebar(ContextInfo)	✅	历史K线逐根调用；实盘每个tick调用	核心策略逻辑：获取数据→计算指标→判断信号→执行下单	ContextInfo	实盘中只有K线结束的信号才生效
after_init(ContextInfo)	❌	init完成后、handlebar前执行一次	执行一次性操作、立即下单、调用init中不支持的函数	ContextInfo	可调用get_trading_dates等函数
stop(ContextInfo)	❌	策略被停止时调用	清理资源、反订阅行情、输出日志	ContextInfo	此时交易连接已断开，不能下单
##########################################
ContextInfo核心属性
属性名	类型	功能说明	使用场景
ContextInfo.start	str	回测开始时间，格式'%Y-%m-%d %H:%M:%S'	设置回测起始日期
ContextInfo.end	str	回测结束时间	设置回测截止日期
ContextInfo.capital	float	回测初始资金，默认1000000	设置回测资金
ContextInfo.period	str	当前K线周期，如'1d','1m','5m'等	获取策略运行周期
ContextInfo.barpos	int	当前K线索引号，从0开始	获取当前处理到哪根K线
ContextInfo.stockcode	str	当前主图代码	获取主图品种代码
ContextInfo.market	str	当前主图市场	获取主图市场代码
ContextInfo.dividend_type	str	当前复权方式	获取复权设置
ContextInfo.benchmark	str	回测基准标的代码	获取回测基准
ContextInfo.do_back_test	bool	是否为回测模式	判断运行模式
ContextInfo.time_tick_size	int	当前图K线数量	获取K线总数
3.3 行情数据函数（Data Functions）
📊 核心行情获取函数
函数名	功能	参数详解	返回值	使用场景
get_market_data_ex(fields, stock_list, period, start_time, end_time, count, dividend_type, fill_data, subscribe)	最核心行情函数，获取K线、Tick、Level2等数据	fields: ['open','high','low','close']；stock_list: ['000001.SZ']；period: 'tick','1m','5m','15m','30m','1h','1d','1w','1mon'；start_time/end_time: '20230101'或'20230101093000'；count: 数据条数；dividend_type: 'none','front','back','front_ratio','back_ratio'；fill_data: True/False；subscribe: True实时/False本地	dict{stock_code: DataFrame}	几乎所有行情获取场景
get_full_tick(stock_code)	获取最新分笔快照（含盘口买卖盘）	stock_code: ['000001.SZ']	dict{stock_code: {time,lastPrice,open,high,low,lastClose,amount,volume,openInt,askPrice,askVol,bidPrice,bidVol}}	获取最新价、买卖盘、涨跌幅
get_local_data(stock_code, start_time, end_time, period, divid_type, count)	仅取本地历史数据（不订阅不更新）	同get_market_data_ex	dict{timestamp: {open,high,low,close,volume,amount}}	回测或离线分析
get_history_data(len, period, field, dividend_type, skip_paused)	⚠️已弃用	使用get_market_data_ex替代	-	旧版兼容
get_market_data(fields, stock_code, start_time, end_time, skip_paused, period, dividend_type, count)	⚠️已弃用	使用get_market_data_ex替代	-	旧版兼容
📊 Level2行情数据
函数名	功能	period参数	返回数据
get_market_data_ex	Level2逐笔成交	period='l2transaction'	time,price,volume,amount,tradeIndex,buyNo,sellNo,tradeType,tradeFlag
get_market_data_ex	Level2逐笔委托	period='l2order'	time,price,volume,entrustNo,entrustType,entrustDirection
get_market_data_ex	Level2十档快照	period='l2quote'	time,lastPrice,open,high,low,askPrice(10档),askVol(10档),bidPrice(10档),bidVol(10档)
get_market_data_ex	Level2大单统计	period='l2transactioncount'	bidNumber,offNumber,ddx,ddy,ddz等
get_market_data_ex	Level2委买委卖队列	period='l2orderqueue'	委买委卖队列数据
3.4 行情订阅函数（Subscribe Functions）
函数名	功能	参数详解	返回值	使用场景
subscribe_quote(stock_code, period, dividend_type, result_type, callback)	订阅指定品种行情，触发回调函数	stock_code: '000001.SZ'；period: 'tick','1m','5m','1d'；dividend_type: 复权方式；result_type: 'DataFrame','dict','list'；callback: 自定义回调函数	int: 订阅号	事件驱动策略、盘中实时监控
subscribe_whole_quote(code_list, callback)	订阅全推数据（全市场分笔）	code_list: ['SH','SZ']；callback: 数据推送回调	int: 订阅号	VIP用户实时全市场监控
unsubscribe_quote(subId)	反订阅行情释放资源	subId: subscribe_quote返回的订阅号	bool: 是否成功	策略停止时清理订阅
3.5 财务数据函数（Financial Data Functions）
函数名	功能	参数详解	返回值	使用场景
get_financial_data(fieldList, stockList, startDate, endDate, report_type)	获取财务数据（资产负债表、利润表、现金流等）	fieldList: ['ASHAREBALANCESHEET.fix_assets','利润表.净利润']；stockList: ['600000.SH']；report_type: 'announce_time'或'report_time'	Series/DataFrame/Panel	基本面分析、因子选股
get_raw_financial_data(fieldList, stockList, startDate, endDate, report_type)	获取原始财务数据（不填充交易日）	同get_financial_data	Series/DataFrame/Panel	获取未经处理的财报数据
get_last_volume(stockcode)	获取最新流通股本	stockcode: '000001.SZ'	int: 流通股本	计算市值、换手率
get_total_share(stockcode)	获取总股本	stockcode: '000001.SZ'	int: 总股本	计算每股指标
get_turnover_rate(stock_list, startTime, endTime)	获取换手率	stock_list: ['000001.SZ']	DataFrame	计算换手率指标
3.6 合约信息函数（Contract Info Functions）
函数名	功能	参数详解	返回值	使用场景
get_instrument_detail(stockcode)	获取合约详细信息	stockcode: '000001.SZ'	dict: ExchangeID,InstrumentID,InstrumentName,ProductID,ProductName,OpenDate,ExpireDate,PreClose,UpStopPrice,DownStopPrice,FloatVolume,TotalVolume,PriceTick,VolumeMultiple,MainContract,IsTrading等	获取涨停跌停价、合约乘数、上市日期
get_stock_list_in_sector(sectorname)	获取板块成份股	sectorname: '沪深300'	list: 成份股代码列表	构建股票池
get_stock_name(stockcode)	获取股票名称	stockcode: '000001.SZ'	str: 股票名称	获取名称
get_open_date(stockcode)	获取股票上市日期	stockcode: '000001.SZ'	number: 上市日期	判断次新股
get_main_contract(codemarket)	获取期货主力合约	codemarket: 'IF00.IF'	str: 主力合约代码	期货交易
get_contract_multiplier(contractcode)	获取合约乘数	contractcode: 'rb2401.SF'	int: 合约乘数	期货价值计算
get_contract_expire_date(codemarket)	获取期货合约到期日	codemarket: 'IF2311.IF'	str: 到期日	期货移仓换月
get_his_contract_list(market)	获取已退市合约列表	market: 'SH'	list: 退市合约代码	获取历史数据
3.7 期权函数（Option Functions）
函数名	功能	参数详解	返回值
get_option_detail_data(optioncode)	获取期权品种详细信息	optioncode: '10002235.SHO'	dict: ExchangeID,InstrumentID,ExpireDate,OptExercisePrice,OptUndlCode等
get_option_list(undl_code, dedate, opttype, isavailable)	获取期权列表	undl_code: '510300.SH'；dedate: '202101'或'20210104'；opttype: 'CALL'/'PUT'；isavailable: True/False	list: 期权合约列表
get_option_undl_data(undl_code_ref)	获取期权标的对应期权品种	undl_code_ref: '510300.SH'	list或dict
bsm_price(optionType,objectPrices,strikePrice,riskFree,sigma,days,dividend)	BS模型计算期权理论价格	optionType: 'C'/'P'	float或list
bsm_iv(optionType,objectPrices,strikePrice,optionPrice,riskFree,days,dividend)	BS模型计算隐含波动率	optionType: 'C'/'P'	double
3.8 板块操作函数（Sector Functions）
函数名	功能	参数详解	返回值
create_sector(parent_node, sector_name, overwrite)	创建板块	parent_node: ''；sector_name: '我的板块'	str: 实际创建的板块名
create_sector_folder(parent_node, folder_name, overwrite)	创建板块目录节点	parent_node: ''；folder_name: '新建分类'	str: 实际创建的节点名
get_sector_list(node)	获取板块目录信息	node: '我的'	list: [[板块列表],[目录列表]]
reset_sector_stock_list(sector, stock_list)	设置板块成分股	sector: '我的自选'；stock_list: ['000001.SZ']	bool: 成功/失败
remove_stock_from_sector(sector, stock_code)	移除板块成分股	sector: '我的自选'；stock_code: '000001.SZ'	bool: 成功/失败
add_stock_to_sector(sector, stock_code)	添加板块成分股	sector: '我的自选'；stock_code: '000001.SZ'	bool: 成功/失败
3.9 数据下载函数（Data Download Functions）
函数名	功能	参数详解	使用场景
download_history_data(stockcode, period, startTime, endTime)	下载指定合约历史行情数据	stockcode: '000001.SZ'；period: '1d','1m','5m','tick'；startTime: '20230101'	回测前下载历史数据
download_history_data(stockcode, period, startTime, endTime, incrementally=True)	增量下载历史数据	同上，增加增量下载参数	每日更新数据
3.10 交易下单函数（Trade Order Functions）
函数名	功能	参数详解	返回值	使用场景
passorder(opType, orderType, accountid, orderCode, prType, price, volume, strategyName, quickTrade, userOrderId, ContextInfo)	核心综合下单函数	opType: 23买入/24卖出/27融资买入/33担保品买入；orderType: 1101单股/1102金额/1113比例；prType: 5最新价/11指定价/14对手价；quickTrade: 0逐K生效/1最新K立即/2立即下单	无	所有交易场景
algo_passorder(opType, orderType, accountid, orderCode, prType, price, volume, strategyName, quickTrade, userOrderId, userOrderParam, ContextInfo)	算法交易（拆单）函数	同passorder，增加userOrderParam拆单参数	无	大额交易拆单
smart_algo_passorder(opType, orderType, accountid, orderCode, prType, price, volume, strategyName, quickTrade, userOrderId, smartAlgoType, limitOverRate, minAmountPerOrder, targetPriceLevel, startTime, endTime, limitControl, ContextInfo)	智能算法交易（VWAP/TWAP）	smartAlgoType: 'VWAP','TWAP'；limitOverRate: 量比；targetPriceLevel: 目标价格	无	智能算法交易
cancel(orderId, accountId, accountType, ContextInfo)	撤销委托	orderId: 委托号；accountType: 'STOCK'/'FUTURE'/'CREDIT'	bool: 是否成功	撤单
cancel_task(taskId, accountId, accountType, ContextInfo)	撤销任务	taskId: 任务号	bool: 是否成功	撤销算法交易任务
pause_task(taskId, accountId, accountType, ContextInfo)	暂停任务	taskId: 任务号	bool: 是否成功	暂停算法交易
resume_task(taskId, accountId, accountType, ContextInfo)	继续任务	taskId: 任务号	bool: 是否成功	恢复算法交易
3.11 交易查询函数（Trade Query Functions）
函数名	功能	参数详解	返回值	使用场景
get_trade_detail_data(accountID, strAccountType, strDatatype, strategyName)	核心交易查询函数	accountID: 资金账号；strAccountType: 'STOCK','FUTURE','CREDIT'；strDatatype: 'account','position','order','deal','task'；strategyName: 可选，按策略名筛选	list: 对应对象列表	获取资金、持仓、委托、成交信息
get_last_order_id(accountID, strAccountType, strDatatype, strategyName)	获取最新委托号	同get_trade_detail_data	str: 委托号	获取最新委托ID
get_value_by_order_id(orderId, accountID, strAccountType, strDatatype)	根据委托号获取委托信息	orderId: 委托号	Order或Deal对象	查询特定委托状态
get_history_trade_detail_data(accountID, strAccountType, strDatatype, strStartDate, strEndDate)	查询历史交易明细	增加strStartDate和strEndDate	list: 历史交易数据	查询历史交易记录
3.12 两融函数（Credit Functions）
函数名	功能	参数详解	返回值
get_assure_contract(accId)	获取两融担保标的明细	accId: 信用账户	list: StkSubjects对象列表
get_enable_short_contract(accId)	获取可融券明细	accId: 信用账户	list: CreditSloEnableAmount对象列表
query_credit_account(accountId, seq, ContextInfo)	查询信用账户明细	accountId: 两融账号；seq: 查询序列号	需配合credit_account_callback
query_credit_opvolume(accountId, stockCode, opType, prType, price, seq, ContextInfo)	查询两融最大可下单量	stockCode: 股票代码或列表	需配合credit_opvolume_callback
get_unclosed_compacts(accountID, accountType)	获取未了结负债合约	accountType: 'CREDIT'	list: 负债合约列表
get_closed_compacts(accountID, accountType)	获取已了结负债合约	accountType: 'CREDIT'	list: 负债合约列表
3.13 期权持仓函数（Option Position Functions）
函数名	功能	参数详解	返回值
get_option_subject_position(accountID)	取期权标的持仓	accountID: 账号	list: CLockPosition对象列表
get_comb_option(accountID)	取期权组合持仓	accountID: 账号	list: CStkOptCombPositionDetail对象列表
3.14 辅助工具函数（Utility Functions）
函数名	功能	参数详解	返回值
timetag_to_datetime(timetag, format)	QMT时间戳转日期时间	timetag: QMT时间戳；format: '%Y%m%d%H%M%S'	str: 日期时间字符串
get_trading_calendar(market, start_time, end_time)	获取交易日历	market: 'SH'；start_time: '20170101'	list: 交易日列表
get_trading_dates(stockcode, start_date, end_date, count, period)	获取K线交易日信息	同get_market_data_ex	list: 交易日列表
get_ipo_data(type)	获取当日新股新债信息	type: 'STOCK'/'BOND'/空	dict: 新股新债数据
get_new_purchase_limit(accid)	获取新股申购额度	accid: 资金账号	dict: 申购额度
get_st_status(stockcode)	获取历史ST状态	stockcode: '000004.SZ'	dict: ST历史
get_his_st_data(stockcode)	获取股票ST历史	stockcode: '000004.SZ'	dict: ST历史
3.15 画图函数（Plotting Functions）
函数名	功能	参数详解	使用场景
ContextInfo.paint(name, value, index, line_style, color, limit)	在副图上画指标线	name: 指标名；value: 数值；line_style: 0曲线/42柱状线；color: 颜色；limit: 'noaxis'/'nodraw'	回测可视化
ContextInfo.draw_text(condition, position, text)	在图形上显示文字	condition: 条件；position: 位置；text: 文字	标记买卖信号
ContextInfo.draw_number(cond, height, number, precision)	在图形上显示数字	precision: 小数位数	显示数值
ContextInfo.draw_vertline(cond, number1, number2, color, limit)	绘制垂直线	同上	标记区间
ContextInfo.draw_icon(cond, height, type)	绘制小图标	type: 0矩形/1椭圆	标记信号
ContextInfo.set_output_index_property(index_name, draw_style, color, noaxis, nodraw, noshow)	设定指标绘制属性	index_name: 指标名称	控制指标显示
3.16 ETF函数（ETF Functions）
函数名	功能	参数详解	返回值
get_etf_info(stockcode)	获取ETF申赎清单	stockcode: '510050.SH'	dict: 成份股信息
get_etf_iopv(stockcode)	获取ETF基金份额参考净值	stockcode: '510050.SH'	float: IOPV
#######################################################
北向资金函数（Northbound Fund Functions）
函数名	功能	参数详解	返回值
get_north_finance_change(period)	获取北向资金数据	period: '1d'/'1m'	dict: 北向资金数据
get_hkt_details(stockcode)	获取北向持股明细	stockcode: '600000.SH'	dict: 持股明细
get_hkt_statistics(stockcode)	获取北向持股统计	stockcode: '600000.SH'	dict: 持股统计
get_hkt_exchange_rate(accountID, accountType)	获取沪深港通汇率	accountType: 'HUGANGTONG'/'SHENGANGTONG'	dict: 汇率数据
3.18 扩展数据函数（Extended Data Functions）
函数名	功能	参数详解	返回值
ext_data(extdataname, stockcode, deviation, ContextInfo)	获取扩展数据	extdataname: 扩展数据名称	number
ext_data_rank(extdataname, stockcode, deviation, ContextInfo)	获取扩展数据排名	同上	number
ext_data_range(extdataname, stockcode, begintime, endtime, ContextInfo)	获取区间扩展数据	增加时间区间	dict
ext_data_rank_range(extdataname, stockcode, begintime, endtime, ContextInfo)	获取区间扩展数据排名	同上	dict
get_factor_value(factorname, stockcode, deviation, ContextInfo)	获取因子数据	factorname: 因子名称	number
get_factor_rank(factorname, stockcode, deviation, ContextInfo)	获取因子排名	同上	number
3.19 篮子交易函数（Basket Trade Functions）
函数名	功能	参数详解	返回值
get_basket(basketName)	获取股票篮子	basketName: 篮子名称	dict: 篮子信息
set_basket(basketDict)	设置股票篮子	basketDict: {'name':'篮子名','stocks':[...]}	无
3.20 定时器函数（Timer Functions）
函数名	功能	参数详解	返回值	使用场景
run_time(funcName, period, startTime)	注册定时器（旧版）	funcName: 回调函数名；period: '5nSecond'/'5nDay'；startTime: '2019-10-14 13:20:00'	无	固定间隔执行
schedule_run(func, time_point, repeat_times, interval, name)	注册定时器（新版）	func: 回调函数；time_point: '20231231235959'；repeat_times: -1无限；interval: timedelta；name: 任务组名	int: 任务号	高级定时任务
cancel_schedule_run(key)	取消定时任务	key: 任务号或任务组名	bool: 是否成功	取消定时任务
3.21 实时回调函数（Real-time Callback Functions）
函数名	功能	参数详解	使用场景
account_callback(ContextInfo, accountInfo)	资金账号状态变化回调	accountInfo: 账号对象	监控账号状态
order_callback(ContextInfo, orderInfo)	委托状态变化回调	orderInfo: 委托对象	监控委托状态
deal_callback(ContextInfo, dealInfo)	成交状态变化回调	dealInfo: 成交对象	监控成交状态
position_callback(ContextInfo, positionInfo)	持仓状态变化回调	positionInfo: 持仓对象	监控持仓变化
task_callback(ContextInfo, taskInfo)	任务状态变化回调	taskInfo: 任务对象	监控算法交易任务
orderError_callback(ContextInfo, orderArgs, errMsg)	下单异常回调	orderArgs: 下单参数；errMsg: 错误信息	处理下单异常
credit_account_callback(ContextInfo, seq, result)	信用账户查询回调	seq: 序列号；result: 查询结果	两融账户查询
credit_opvolume_callback(ContextInfo, accid, seq, ret, result)	两融可下单量查询回调	accid: 账号；seq: 序列号；ret: 状态码	两融可下单量查询
📋 第四部分：参数枚举值大全
4.1 opType - 操作类型（股票/ETF/可转债）
数值	描述
23	股票/ETF/可转债买入
24	股票/ETF/可转债卖出
25	组合买入
26	组合卖出
27	融资买入
28	融券卖出
29	买券还券
30	直接还券
31	卖券还款
32	直接还款
33	担保品买入
34	担保品卖出
35	普通账号一键买卖
36	信用账号一键买卖
4.2 opType - 操作类型（期货）
数值	描述
0	开多
1	平昨多
2	平今多
3	开空
4	平昨空
5	平今空
6	平多，优先平今
7	平多，优先平昨
8	平空，优先平今
9	平空，优先平昨
4.3 opType - 操作类型（期权）
数值	描述
50	买入开仓
51	卖出平仓
52	卖出开仓
53	买入平仓
54	备兑开仓
55	备兑平仓
56	认购行权
57	认沽行权
58	证券锁定
59	证券解锁
60	ETF申购
61	ETF赎回
4.4 orderType - 下单方式
数值	描述
1101	单股、单账号、普通、股/手方式下单
1102	单股、单账号、普通、金额（元）方式下单
1113	单股、单账号、总资产、比例方式下单
1123	单股、单账号、可用、比例方式下单
1201	单股、账号组、普通、股/手方式下单
2101	组合、单账号、按组合股票数量下单
2102	组合、单账号、按组合股票权重下单
2103	组合、单账号、按账号可用方式下单
4.5 prType - 下单选价类型
数值	描述
0	卖5价
1	卖4价
2	卖3价
3	卖2价
4	卖1价
5	最新价
6	买1价
7-10	买2-5价
11	指定价
12	涨跌停价
13	挂单价
14	对手价
42	最优五档即时成交剩余撤销
43	最优五档即时成交剩转限价
44	对手方最优价格委托
45	本方最优价格委托
46	即时成交剩余撤销委托
47	最优五档即时成交剩余撤销委托
48	全额成交或撤销委托
49	盘后定价
4.6 quickTrade - 快速下单
数值	描述
0	逐K线生效（K线结束才发单）
1	最新K线立即下单
2	任何情况下立即下单
📝 第五部分：策略模板大全
5.1 双均线策略模板
python
#coding:gbk
import pandas as pd
import numpy as np

class G(): pass
g = G()

def init(ContextInfo):
    g.stock = ContextInfo.stockcode + '.' + ContextInfo.market
    g.fast = 5
    g.slow = 20
    g.accountid = "testS" if ContextInfo.do_back_test else account
    if ContextInfo.do_back_test:
        ContextInfo.capital = 1000000

def handlebar(ContextInfo):
    if not ContextInfo.do_back_test and not ContextInfo.is_last_bar():
        return

    data = ContextInfo.get_market_data_ex(
        ['close'], [g.stock],
        period=ContextInfo.period,
        count=g.slow + 10,
        subscribe=not ContextInfo.do_back_test
    )
    if g.stock not in data or len(data[g.stock]) < g.slow:
        return

    close = data[g.stock]['close'].values
    fast_ma = np.mean(close[-g.fast:])
    slow_ma = np.mean(close[-g.slow:])

    positions = get_trade_detail_data(g.accountid, 'stock', 'position')
    pos_dict = {p.m_strInstrumentID + '.' + p.m_strExchangeID: p.m_nVolume for p in positions}
    holding = pos_dict.get(g.stock, 0)

    account_info = get_trade_detail_data(g.accountid, 'stock', 'account')
    if not account_info:
        return
    cash = account_info[0].m_dAvailable

    if holding == 0 and fast_ma > slow_ma:
        vol = int(10000 / close[-1] / 100) * 100
        if vol > 0 and cash > 10000:
            passorder(23, 1101, g.accountid, g.stock, 5, close[-1], vol,
                     '双均线策略', 2 if not ContextInfo.do_back_test else 0, '', ContextInfo)
    elif holding > 0 and fast_ma < slow_ma:
        passorder(24, 1101, g.accountid, g.stock, 5, close[-1], holding,
                 '双均线策略', 2 if not ContextInfo.do_back_test else 0, '', ContextInfo)
5.2 MACD策略模板
python
#coding:gbk
import pandas as pd
import numpy as np
import talib

class G(): pass
g = G()

def init(ContextInfo):
    g.stock = ContextInfo.stockcode + '.' + ContextInfo.market
    g.accountid = "testS" if ContextInfo.do_back_test else account
    g.fast = 12
    g.slow = 26
    g.signal = 9

def handlebar(ContextInfo):
    if not ContextInfo.do_back_test and not ContextInfo.is_last_bar():
        return

    data = ContextInfo.get_market_data_ex(
        ['close'], [g.stock],
        period=ContextInfo.period,
        count=100,
        subscribe=not ContextInfo.do_back_test
    )
    if g.stock not in data or len(data[g.stock]) < 50:
        return

    close = data[g.stock]['close'].values
    macd, signal, hist = talib.MACD(close, g.fast, g.slow, g.signal)

    if len(macd) < 2:
        return

    positions = get_trade_detail_data(g.accountid, 'stock', 'position')
    pos_dict = {p.m_strInstrumentID + '.' + p.m_strExchangeID: p.m_nVolume for p in positions}
    holding = pos_dict.get(g.stock, 0)

    account_info = get_trade_detail_data(g.accountid, 'stock', 'account')
    if not account_info:
        return
    cash = account_info[0].m_dAvailable

    # MACD金叉（MACD上穿信号线）
    if holding == 0 and macd[-2] < signal[-2] and macd[-1] > signal[-1]:
        vol = int(10000 / close[-1] / 100) * 100
        if vol > 0 and cash > 10000:
            passorder(23, 1101, g.accountid, g.stock, 5, close[-1], vol,
                     'MACD策略', 2 if not ContextInfo.do_back_test else 0, '', ContextInfo)
    # MACD死叉（MACD下穿信号线）
    elif holding > 0 and macd[-2] > signal[-2] and macd[-1] < signal[-1]:
        passorder(24, 1101, g.accountid, g.stock, 5, close[-1], holding,
                 'MACD策略', 2 if not ContextInfo.do_back_test else 0, '', ContextInfo)
5.3 RSI策略模板
python
#coding:gbk
import pandas as pd
import numpy as np
import talib

class G(): pass
g = G()

def init(ContextInfo):
    g.stock = ContextInfo.stockcode + '.' + ContextInfo.market
    g.accountid = "testS" if ContextInfo.do_back_test else account
    g.rsi_period = 14
    g.rsi_buy = 30
    g.rsi_sell = 70

def handlebar(ContextInfo):
    if not ContextInfo.do_back_test and not ContextInfo.is_last_bar():
        return

    data = ContextInfo.get_market_data_ex(
        ['close'], [g.stock],
        period=ContextInfo.period,
        count=100,
        subscribe=not ContextInfo.do_back_test
    )
    if g.stock not in data or len(data[g.stock]) < g.rsi_period + 1:
        return

    close = data[g.stock]['close'].values
    rsi = talib.RSI(close, g.rsi_period)

    if len(rsi) < 2:
        return

    positions = get_trade_detail_data(g.accountid, 'stock', 'position')
    pos_dict = {p.m_strInstrumentID + '.' + p.m_strExchangeID: p.m_nVolume for p in positions}
    holding = pos_dict.get(g.stock, 0)

    account_info = get_trade_detail_data(g.accountid, 'stock', 'account')
    if not account_info:
        return
    cash = account_info[0].m_dAvailable

    # RSI超卖买入
    if holding == 0 and rsi[-1] < g.rsi_buy:
        vol = int(10000 / close[-1] / 100) * 100
        if vol > 0 and cash > 10000:
            passorder(23, 1101, g.accountid, g.stock, 5, close[-1], vol,
                     'RSI策略', 2 if not ContextInfo.do_back_test else 0, '', ContextInfo)
    # RSI超买卖出
    elif holding > 0 and rsi[-1] > g.rsi_sell:
        passorder(24, 1101, g.accountid, g.stock, 5, close[-1], holding,
                 'RSI策略', 2 if not ContextInfo.do_back_test else 0, '', ContextInfo)
🛠️ 第六部分：常见问题与解决方案
6.1 ContextInfo回滚机制
问题：在ContextInfo上存储的属性值在下一个tick丢失
解决：使用全局类实例 g = G() 存储状态

6.2 第三方库白名单报错
问题：ImportError: Forbidden: Module xxx not in whitelist!
解决：联系券商开通对应库的白名单权限

6.3 实盘下单失败
检查项：

是否在模型交易界面运行（非编辑器）

quickTrade参数是否正确（定时器/回调中用2）

账号是否登录、有足够资金

6.4 订阅数量超限
解决：使用 unsubscribe_quote() 释放不需要的订阅

6.5 数据获取失败
检查项：

回测前是否 download_history_data 下载数据

subscribe参数是否正确（回测False，实盘True）

📌 第七部分：快速参考
7.1 常用代码片段
获取行情数据：

python
data = ContextInfo.get_market_data_ex(['close'], ['000001.SZ'], period='1d', count=20, subscribe=False)
获取账户信息：

python
account = get_trade_detail_data('test', 'stock', 'account')[0]
cash = account.m_dAvailable
获取持仓信息：

python
positions = get_trade_detail_data('test', 'stock', 'position')
pos_dict = {p.m_strInstrumentID + '.' + p.m_strExchangeID: p.m_nVolume for p in positions}
holding = pos_dict.get('000001.SZ', 0)
下单买入：

python
passorder(23, 1101, 'test', '000001.SZ', 5, -1, 100, '策略名', 2, '备注', ContextInfo)
下单卖出：

python
passorder(24, 1101, 'test', '000001.SZ', 5, -1, 100, '策略名', 2, '备注', ContextInfo)
撤单：

python
cancel(orderId, accountId, 'stock', ContextInfo)
################################详细接口例子训练*******************
'''
1变量约定
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
函数命名规则
函数名以 get_ 开头的，表示数据来源于客户端内存
函数名以 query_ 开头的，表示数据是向服务查询
账号类型说明
'FUTURE' - 期货账号
'STOCK' - 股票账号
'CREDIT' - 信用账号
'FUTURE_OPTION' - 期货期权
'STOCK_OPTION' - 股票期权
'HUGANGTONG' - 沪港通
'SHENGANGTONG' - 深港通
symbol_code - 代码表示
迅投代码(symbol_code)是迅投平台统一用于表示交易标的的代码 其格式为:交易标的代码.交易所代码,例如深圳证券交易所的平安银行,迅投代码为000001.SZ(不区分大小写)。代码表示可以在迅投研终端的行情列表或者按键精灵中查询。

迅投研终端示例

交易所代码
目前迅投研支持国内12个交易所,12个交易所的代码缩写如下:

交易所名称	迅投简称	显示后缀
上海证券交易所	SH	SH
深圳证券交易所	SZ	SZ
北京证券交易所	BJ	BJ
香港证券交易所	HK	HK
沪港通	HGT	HGT
深港通	SGT	SGT
中国金融期货交易所	IF	CFFEX
上海期货交易所	SF	SHFE
大连商品交易所	DF	DCE
郑州商品交易所	ZF	CZCE
上海国际能源交易中心	INE	INE
广州期货交易所	GF	GFEX
迅投研系统目前支持一站式获取全球多市场数据，详情链接：全球市场数据

全球行情展示

交易标的代码
交易标的代码是指交易所给出的交易标的代码, 包括股票（如 600000）, 期货（如 rb2011）, 期权（如 10002498）, 指数（如 000001）, 基金（如 510300）等代码。

注意

对于期货合约代码来说，我们仅对market做了简化处理，symbol仍遵守交易所标准命名规则，且严格区分大小写，例如AP401.ZF不能写成ap401.ZF,rb2401.SF不能写成RB2401.SF

symbol示例
市场中文名	市场代码	示例代码	显示后缀	证券简称
上交所	SH	600000.SH	SH	浦发银行
深交所	SZ	000001.SZ	SZ	平安银行
北交所	BJ	830779.BJ	BJ	武汉蓝电
中金所	IF	IC2311.IF	CFFEX	中证 500 指数 2023 年 11 月期货合约
上期所	SF	rb2311.SF	SHFE	螺纹钢 2023 年 11 月期货合约
大商所	DF	m2311.DF	DCE	豆粕 2023 年 11 月期货合约
郑商所	ZF	FG305.ZF	CZCE	玻璃 2023 年 5 月期货合约
上海国际能源交易中心	INE	sc2311.INE	INE	原油 2023 年 11 月期货合约
广期所	GF	lc2405.GF	GFEX	碳酸锂 2024 年 05 月期货合约
上证期权	SHO	10005334.SHO	SH	50ETF购12月2650
深证期权	SZO	90002114.SZO	SZ	深证100ETF沽12月2700
板块指数	BKZS	290001.BKZS	BKZS	工业品期货板块指数
期货主力连续合约
仅支持回测模式下交易，期货主力连续合约为量价数据的简单拼接，未做平滑处理，如rb00.SF螺纹钢主连合约，其他[主连合约代码请参考](期货数据 | 迅投知识库 (thinktrader.net))

期货加权连续合约
仅支持回测模式下交易，期货加权连续合约为迅投按照一定规则加权合成的连续合约，相比主力连续合约更加平滑,如rbJQ00.SF,其他[加权合约代码参考](期货数据 | 迅投知识库 (thinktrader.net))

mode - 模式选择
迅投研终端中，策略可以以四种模式运行，分别为调试运行模式，回测模式,模拟信号模式,实盘交易模式，模式需要在运行策略时手动选择

调试运行模式
调试运行模式需要在策略编辑界面点击编辑栏上方的运行，该模式下策略会以实时行情进行运算，但迅投研终端不会记录交易信号迅投研终端示例

回测模式
回测模式需要在策略编辑界面点击编辑栏上方的回测，该模式下策略会以右侧栏设定的回测周期推进行情进行运算，回测模式下，发生的交易会被记录在回测结果页面迅投研终端示例

模拟信号模式
模拟信号模式需要在策略交易界面，在左侧策略文件栏中选择要进行计算运行的策略，点击右侧圆形按钮选择模拟，点击三角形运行按钮后策略会以实时行情进行运算，该模式下调用的下单函数(passorder)不会产生实际交易，仅会记录交易信号在下方的策略信号栏中迅投研终端示例

实盘交易模式
实盘交易模式需要在策略交易界面，在左侧策略文件栏中选择要进行计算运行的策略，点击右侧圆形按钮选择实盘，点击三角形运行按钮后策略会以实时行情进行运算，该模式下调用的下单函数(passorder)会对账户实际下单，同时交易信号会记录在下方的策略信号栏中迅投研终端示例

ContextInfo - 上下文对象
ContextInfo.start/ContextInfo.end - 回测开始/结束时间
注意

一、此属性只在回测模式生效；

二、仅在init中设置生效，应在init中设置完毕；

三、缺省值为策略编辑界面设定的回测时间范围；

四、回测起止时间也可在策略编辑器的回测参数面板中设置，若两处同时设置，则以代码中设置的值为准；

五、结束时间小于等于开始时间则计算范围为空。

释义

可通过此属性设定回测开始/结束的时间,以%Y-%m-%d %H:%M:%S格式传入

原型

内置python

ContextInfo.start # 回测开始时间属性
ContextInfo.end # 回测结束时间属性
返回值none

示例

内置python输出值

# coding:gbk
def init(ContextInfo):
	ContextInfo.start = "2017-01-01 00:00:00"# 回测开始时间为 2017-01-01
	ContextInfo.end = "2020-01-01 00:00:00"# 回测结束时间为 2020-01-01
def handlebar(ContextInfo):
	# 打印输出当前回测时间
	print(timetag_to_datetime(ContextInfo.get_bar_timetag(ContextInfo.barpos), "%Y-%m-%d %H%M%S"))
ContextInfo.capital - 设定回测初始资金
注意

此函数只支持回测模式。回测初始资金也可在策略编辑器的回测参数面板中设置，若两处同时设置，则以代码中设置的值为准。

释义 设定回测初始资金，支持读写，默认为 1000000

原型

内置python

ContextInfo.capital = 10000000 # 设定ContextInfo.capital 值为10000000
返回值float类型的数值，代表当前策略设定的回测金额

示例

内置python输出值

# coding:gbk
def init(ContextInfo):
    ContextInfo.capital = 10000000
def handlebar(ContextInfo):
    print(ContextInfo.capital)
ContextInfo.period - 获取当前周期
释义 获取当前周期，即基本信息中设置的默认周期，只读

原型

内置python

ContextInfo.period
返回string,返回值含义:

值	含义
'1d'	日线
'1m'	1分钟线
'3m'	3分钟线
'5m'	5分钟线
'15m'	15分钟线
'30m'	30分钟线
'1h'	小时线
'1w'	周线
'1mon'	月线
'1q'	季线
'1hy'	半年线
'1y'	年线
示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.period)
ContextInfo.barpos - 获取当前运行到 K 线索引号
释义

获取主图当前运行到的 K 线索引号，只读，索引号从0开始

原型

内置python

ContextInfo.barpos
返回值int类型值,代表着当前K线的索引号

示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.barpos)
ContextInfo.time_tick_size - 获取当前图 K 线数目
释义

获取当前图 K 线bar的数量，只读

原型

内置python

ContextInfo.time_tick_size
返回值int

示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.time_tick_size)
ContextInfo.stockcode - 获取当前图代码
释义

获取当前主图代码，只读

原型

内置python

ContextInfo.stockcode
返回值string：对应主图代码

示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.stockcode)
ContextInfo.market - 获取当前主图市场
释义

获取当前主图市场，只读

原型

内置python

ContextInfo.market
返回值string：对应主图市场

示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.market)
ContextInfo.dividend_type - 获取当前主图复权处理方式
释义

获取当前主图复权处理方式

原型

内置python

ContextInfo.dividend_type
返回值string，返回值含义：

值	含义
'none'	不复权
'front'	向前复权
'back'	向后复权
'front_ratio'	等比向前复权
'back_ratio'	等比向后复权
示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.dividend_type)
ContextInfo.benchmark - 获取回测基准标的
注意

该属性只在回测模式可用

释义 获取回测基准的代码，只读

原型

内置python

ContextInfo.benchmark
返回值string

示例

内置python返回值

# coding:gbk
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    print(ContextInfo.benchmark)
ContextInfo.do_back_test - 表示当前是否为回测模式
释义

表示当前是否为回测模式，只读，默认值为 False

原型

内置python

ContextInfo.do_back_test
返回值bool
###################################################
'''
2数据结果
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
数据类
Tick - Tick 对象
行情快照数据

get_market_data_ex/get_full_tick返回对象：
字段名	数据类型	含义
time	int	时间戳
stime	string	时间戳字符串形式
lastPrice	float	最新价
open	float	开盘价
high	float	最高价
low	float	最低价
lastClose	float	前收盘价
amount	float	成交总额
volume	int	成交总量（手）
pvolume	int	原始成交总量(未经过股手转换的成交总量)【不推荐使用】
stockStatus	int	证券状态
openInt	int	若是股票，则openInt含义为股票状态，非股票则是持仓量openInt字段说明
transactionNum	float	成交笔数(期货没有，单独计算)
lastSettlementPrice	float	前结算(股票为0)
settlementPrice	float	今结算(股票为0)
askPrice	list[float]	多档委卖价
askVol	list[int]	多档委卖量
bidPrice	list[float]	多档委买价
bidVol	list[int]	多档委买量
get_market_data返回对象：
字段	数据类型	含义
timetag	string	时间戳，格式为: %Y%m%d %H:%M:%S
lastPrice	float	最新价
open	float	开盘价
high	float	最高价
low	float	最低价
lastClose	float	前收盘价
amount	float	成交额
volume	float	成交量（手）
pvolume	float	原始成交量（股）【不推荐使用】
stockStatus	int	作废 参考openInt
openInt	float	若是股票，则openInt含义为股票状态，非股票则是持仓量openInt字段说明
lastSettlementPrice	float	昨结算价
pe	float	对于股票是市盈率,对于ETF是iopv值
askPrice	list	委卖价
bidPrice	list	委买价
askVol	list	委卖量
bidVol	list	委买量
settlementPrice	float	今结算价
subscribe_quote/subscribe_whole_quote回调对象：
同 get_full_tick 返回结构

Bar - Bar对象
bar数据是指各种频率的行情数据

字段	数据类型	含义
time	int	时间
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
volume	float	成交量
amount	float	成交额
settelementPrice	float	今结算
openInterest	float	持仓量
preClose	float	前收盘价
suspendFlag	int	停牌 1停牌，0 不停牌
l2quote - Level2行情快照
字段名	数据类型	解释
time	int	时间戳
stime	string	时间戳字符串形式
lastPrice	float	最新价
open	float	开盘价
high	float	最高价
low	float	最低价
amount	float	成交额
volume	int	成交总量
pvolume	int	原始成交总量(未经过股手转换的成交总量)
stockStatus	int	证券状态
openInt	int	持仓量
transactionNum	int	成交笔数(期货没有，单独计算)
lastClose	float	前收盘价
lastSettlementPrice	float	前结算(股票为0)
settlementPrice	float	今结算(股票为0)
askPrice	list[float]	多档委卖价
askVol	list[int]	多档委卖量
bidPrice	list[float]	多档委买价
bidVol	list[int]	多档委买量
l2quoteaux - Level2行情快照补充
字段名	数据类型	解释
time	int	时间戳
stime	string	时间戳字符串形式
avgBidPrice	float	委买均价
totalBidQuantity	int	委买总量
avgOffPrice	float	委卖均价
totalOffQuantity	int	委卖总量
withdrawBidQuantity	int	买入撤单总量
withdrawBidAmount	float	买入撤单总额
withdrawOffQuantity	int	卖出撤单总量
withdrawOffAmount	float	卖出撤单总额
l2order - Level2逐笔委托
字段名	数据类型	解释
time	int	时间戳
stime	float	时间戳浮点数形式
price	float	委托价
volume	int	委托量
entrustNo	int	委托号
entrustType	int	委托类型
entrustDirection	int	委托方向
提示

注：上交所的撤单信息在逐笔委托的委托方向，区分撤买撤卖

0 - 未知
1 - 买入
2 - 卖出
3 - 撤买（上交所）
4 - 撤卖（上交所）
l2transaction - Level2逐笔成交
字段名	数据类型	解释
time	int	时间戳
stime	string	时间戳字符串形式
price	float	成交价
volume	int	成交量
amount	float	成交额
tradeIndex	int	成交记录号
buyNo	int	买方委托号
sellNo	int	卖方委托号
tradeType	int	成交类型
tradeFlag	int	成交标志
提示

深交所逐笔成交的撤单标志，没有方向

0 - 未知
1 - 外盘，主买
2 - 内盘，主卖
3 - 撤单
l2transactioncount - Level2逐笔成交统计
字段名	数据类型	解释
time	int	时间戳
bidNumber	int	主买单总单数
offNumber	int	主卖单总单数
ddx	float	大单动向
ddy	float	涨跌动因
ddz	float	大单差分
netOrder	int	净挂单量
netWithdraw	int	净撤单量
withdrawBid	int	总撤买量
withdrawOff	int	总撤卖量
bidNumberDx	int	主买单总单数增量
offNumberDx	int	主卖单总单数增量
transactionNumber	int	成交笔数增量
bidMostAmount	float	主买特大单成交额
bidBigAmount	float	主买大单成交额
bidMediumAmount	float	主买中单成交额
bidSmallAmount	float	主买小单成交额
bidTotalAmount	float	主买累计成交额
offMostAmount	float	主卖特大单成交额
offBigAmount	float	主卖大单成交额
offMediumAmount	float	主卖中单成交额
offSmallAmount	float	主卖小单成交额
offTotalAmount	float	主卖累计成交额
unactiveBidMostAmount	float	被动买特大单成交额
unactiveBidBigAmount	float	被动买大单成交额
unactiveBidMediumAmount	float	被动买中单成交额
unactiveBidSmallAmount	float	被动买小单成交额
unactiveBidTotalAmount	float	被动买累计成交额
unactiveOffMostAmount	float	被动卖特大单成交额
unactiveOffBigAmount	float	被动卖大单成交额
unactiveOffMediumAmount	float	被动卖中单成交额
unactiveOffSmallAmount	float	被动卖小单成交额
unactiveOffTotalAmount	float	被动卖累计成交额
netInflowMostAmount	float	净流入超大单成交额（lv1数据不支持计算，返回为 0，如有需求可咨询高频资金流数据）
netInflowBigAmount	float	净流入大单成交额（lv1数据不支持计算，返回为 0，如有需求可咨询高频资金流数据）
netInflowMediumAmount	float	净流入中单成交额（lv1数据不支持计算，返回为 0，如有需求可咨询高频资金流数据）
netInflowSmallAmount	float	净流入小单成交额（lv1数据不支持计算，返回为 0，如有需求可咨询高频资金流数据）
bidMostVolume	int	主买特大单成交量
bidBigVolume	int	主买大单成交量
bidMediumVolume	int	主买中单成交量
bidSmallVolume	int	主买小单成交量
bidTotalVolume	int	主买累计成交量
offMostVolume	int	主卖特大单成交量
offBigVolume	int	主卖大单成交量
offMediumVolume	int	主卖中单成交量
offSmallVolume	int	主卖小单成交量
offTotalVolume	int	主卖累计成交量
unactiveBidMostVolume	int	被动买特大单成交量
unactiveBidBigVolume	int	被动买大单成交量
unactiveBidMediumVolume	int	被动买中单成交量
unactiveBidSmallVolume	int	被动买小单成交量
unactiveBidTotalVolume	int	被动买累计成交量
unactiveOffMostVolume	int	被动卖特大单成交量
unactiveOffBigVolume	int	被动卖大单成交量
unactiveOffMediumVolume	int	被动卖中单成交量
unactiveOffSmallVolume	int	被动卖小单成交量
unactiveOffTotalVolume	int	被动卖累计成交量
netInflowMostVolume	int	净流入超大单成交量
netInflowBigVolume	int	净流入大单成交量
netInflowMediumVolume	int	净流入中单成交量
netInflowSmallVolume	int	净流入小单成交量
bidMostAmountDx	float	主买特大单成交额增量
bidBigAmountDx	float	主买大单成交额增量
bidMediumAmountDx	float	主买中单成交额增量
bidSmallAmountDx	float	主买小单成交额增量
bidTotalAmountDx	float	主买累计成交额增量
offMostAmountDx	float	主卖特大单成交额增量
offBigAmountDx	float	主卖大单成交额增量
offMediumAmountDx	float	主卖中单成交额增量
offSmallAmountDx	float	主卖小单成交额增量
offTotalAmountDx	float	主卖累计成交额增量
unactiveBidMostAmountDx	float	被动买特大单成交额增量
unactiveBidBigAmountDx	float	被动买大单成交额增量
unactiveBidMediumAmountDx	float	被动买中单成交额增量
unactiveBidSmallAmountDx	float	被动买小单成交额增量
unactiveBidTotalAmountDx	float	被动买累计成交额增量
unactiveOffMostAmountDx	float	被动卖特大单成交额增量
unactiveOffBigAmountDx	float	被动卖大单成交额增量
unactiveOffMediumAmountDx	float	被动卖中单成交额增量
unactiveOffSmallAmountDx	float	被动卖小单成交额增量
unactiveOffTotalAmountDx	float	被动卖累计成交额增量
netInflowMostAmountDx	float	净流入超大单成交额增量
netInflowBigAmountDx	float	净流入大单成交额增量
netInflowMediumAmountDx	float	净流入中单成交额增量
netInflowSmallAmountDx	float	净流入小单成交额增量
bidMostVolumeDx	int	主买特大单成交量增量
bidBigVolumeDx	int	主买大单成交量增量
bidMediumVolumeDx	int	主买中单成交量增量
bidSmallVolumeDx	int	主买小单成交量增量
bidTotalVolumeDx	int	主买累计成交量增量
offMostVolumeDx	int	主卖特大单成交量增量
offBigVolumeDx	int	主卖大单成交量增量
offMediumVolumeDx	int	主卖中单成交量增量
offSmallVolumeDx	int	主卖小单成交量增量
offTotalVolumeDx	int	主卖累计成交量增量
unactiveBidMostVolumeDx	int	被动买特大单成交量增量
unactiveBidBigVolumeDx	int	被动买大单成交量增量
unactiveBidMediumVolumeDx	int	被动买中单成交量增量
unactiveBidSmallVolumeDx	int	被动买小单成交量增量
unactiveBidTotalVolumeDx	int	被动买累计成交量增量
unactiveOffMostVolumeDx	int	被动卖特大单成交量增量
unactiveOffBigVolumeDx	int	被动卖大单成交量增量
unactiveOffMediumVolumeDx	int	被动卖中单成交量增量
unactiveOffSmallVolumeDx	int	被动卖小单成交量增量
unactiveOffTotalVolumeDx	int	被动卖累计成交量增量
netInflowMostVolumeDx	int	净流入超大单成交量增量
netInflowBigVolumeDx	int	净流入大单成交量增量
netInflowMediumVolumeDx	int	净流入中单成交量增量
netInflowSmallVolumeDx	int	净流入小单成交量增量
l2orderqueue - Level2委买委卖队列
交易类
Account - 账户对象
字段名	数据类型	解释
m_strAccountID	str	资金账号，用于识别不同的资金账户
m_nBrokerType	int	账号类型，表示账号的具体种类
m_dMaxMarginRate	float	保证金比率，通常用于期货账号
m_dFrozenMargin	float	冻结保证金，指投资者在交易中被冻结的保证金金额
m_dFrozenCash	float	冻结金额，指投资者在交易中被冻结的资金金额
m_dFrozenCommission	float	冻结手续费，指投资者在交易中被冻结的手续费金额
m_dRisk	float	风险度，指投资者账户的风险程度
m_dNav	float	单位净值，用于表示基金的净值
m_dPreBalance	float	期初权益，指期初时账户的资金金额
m_dBalance	float	总资产，表示账户的总资金金额
m_dAvailable	float	可用金额，指账户中可用于交易和提取的资金金额
m_dCommission	float	手续费 (旧版本为 m_dComission)
m_dPositionProfit	float	持仓盈亏，指当前持有的证券或期货合约的盈亏金额
m_dCloseProfit	float	平仓盈亏，在期货交易中表示已经平仓的交易的盈亏金额
m_dCashIn	float	出入金净值，表示账户中出入金的净额
m_dCurrMargin	float	当前使用的保证金金额
m_dInitBalance	float	初始权益，指账户初始时的权益金额
m_strStatus	str	状态，表示账户的当前状态
m_dInitCloseMoney	float	期初平仓盈亏，指账户初始时的平仓盈亏金额
m_dInstrumentValue	float	总市值，表示持有的证券或期货合约的总市值
m_dDeposit	float	入金，指账户中的入金金额
m_dWithdraw	float	出金，指账户中的出金金额
m_dPreCredit	float	上次信用额度，用于表示上次的信用额度
m_dPreMortgage	float	上次质押，指上次的质押金额
m_dMortgage	float	质押，指当前的质押金额
m_dCredit	float	信用额度，表示账户的信用额度
m_dAssetBalance	float	证券初始资金，表示股票账户的初始资金
m_strOpenDate	str	起始日期，表示账户的起始日期
m_dFetchBalance	float	可取金额，指账户中可取出的金额
m_strTradingDate	str	交易日，表示当前的交易日期
m_dStockValue	float	股票总市值，表示股票账户中持有的股票的总市值
m_dLoanValue	float	债券总市值，表示账户中持有的债券的总市值
m_dFundValue	float	基金总市值，包括ETF和封闭式基金在内的基金的总市值
m_dRepurchaseValue	float	回购总市值，表示账户中持有的所有回购交易的总市值
m_dLongValue	float	多单总市值，指现货账户中多单持仓的总市值
m_dShortValue	float	空单总市值，指现货账户中空单持仓的总市值
m_dNetValue	float	净持仓总市值，指现货账户中多单总市值减去空单总市值的差额
m_dAssureAsset	float	净资产，表示账户的净资产金额
m_dTotalDebit	float	总负债，表示账户的总负债金额
m_dEntrustAsset	float	可信资产，用于校对账户资金的准确性
m_dInstrumentValueRMB	float	总市值（人民币），指沪港通账户中的持仓证券的总市值
m_dSubscribeFee	float	申购费，指申购基金时支付的费用
m_dGoldValue	float	库存市值，表示黄金现货账户中黄金库存的市值
m_dGoldFrozen	float	现货冻结，表示黄金现货账户中被冻结的黄金金额
m_dMargin	float	占用保证金，用于维持保证金
m_strMoneyType	str	币种，表示账户的资金所使用的货币种类
m_dPurchasingPower	float	购买力，指账户可用于购买投资品的金额
m_dRawMargin	float	原始保证金，指期货账户中的原始保证金金额
m_dBuyWaitMoney	float	买入待交收金额（元），指账户中买入股票但尚未交收的金额
m_dSellWaitMoney	float	卖出待交收金额（元），指账户中卖出股票但尚未交收的金额
m_dReceiveInterestTotal	float	本期间应计利息，指账户本期间内应计的利息金额
m_dRoyalty	float	权利金收支，指期货期权交易中的权利金收支金额
m_dFrozenRoyalty	float	冻结权利金，指期货期权交易中被冻结的权利金金额
m_dRealUsedMargin	float	实时占用保证金，用于股票期权交易中表示实时占用的保证金金额
m_dRealRiskDegree	float	实时风险度，用于股票期权交易中表示实时的风险度
Order - 委托对象
字段	数据类型	解释
m_strAccountID	str	资金账号，账号，账号，资金账号
m_strExchangeID	str	证券市场
m_strExchangeName	str	交易市场
m_strProductID	str	品种代码
m_strProductName	str	品种名称
m_strInstrumentID	str	证券代码
m_strInstrumentName	str	证券名称，合约名称
m_nRef	int	订单编号
m_strOrderRef	str	内部委托号，下单引用等于股票的内部委托号
m_nOrderPriceType	int	EBrokerPriceType 类型，例如市价单、限价单
m_nDirection	int	EEntrustBS 类型，操作，多空，期货多空，股票买卖永远是 48，其他的 dir 同理
m_nOffsetFlag	int	EOffset_Flag_Type类型，买卖/开平，用此字段区分股票买卖，期货开、平仓，期权买卖等
m_nHedgeFlag	int	EHedge_Flag_Type 类型，投保
m_dLimitPrice	float	委托价格，限价单的限价，即报价
m_nVolumeTotalOriginal	int	委托数量，最初的委托数量
m_nOrderSubmitStatus	int	EEntrustSubmitStatus 类型，报单状态，提交状态，股票中不需要报单状态
m_strOrderSysID	str	合同编号，委托号
m_nOrderStatus	int	EEntrustStatus，委托状态
m_nVolumeTraded	int	成交数量，已成交量
m_nVolumeTotal	int	委托剩余量，当前总委托量，股票中表示总委托量减去成交量
m_nErrorID	int	状态ID
m_strErrorMsg	str	状态信息
m_nTaskId	int	任务号
m_dFrozenMargin	float	冻结金额，冻结保证金
m_dFrozenCommission	float	冻结手续费
m_strInsertDate	str	委托日期，报单日期
m_strInsertTime	str	委托时间
m_dTradedPrice	float	成交均价（股票）
m_dCancelAmount	float	已撤数量
m_strOptName	str	买卖标记，展示委托属性的中文
m_dTradeAmount	float	成交金额，期货的计算方式为均价乘以数量乘以合约乘数
m_eEntrustType	int	EEntrustTypes，委托类别
m_strCancelInfo	str	废单原因
m_strUnderCode	str	标的证券代码
m_eCoveredFlag	int	备兑标记，'0’表示非备兑，'1’表示备兑
m_dOrderPriceRMB	float	委托价格（人民币），目前用于港股通
m_dTradeAmountRMB	float	成交金额（人民币），目前用于港股通
m_dReferenceRate	float	汇率，目前用于港股通
m_strCompactNo	str	合约编号
m_eCashgroupProp	int	EXTCompactBrushSource类型，头寸来源
m_dShortOccupedMargin	float	预估在途占用保证金，用于期权
m_strXTTrade	str	是否是迅投交易
m_strAccountKey	str	账号key，唯一区别不同账号的key
m_strRemark	str	投资备注
Deal - 成交对象
字段	数据类型	解释
m_strAccountID	str	资金账号
m_strExchangeID	str	证券市场
m_strExchangeName	str	交易市场
m_strProductID	str	品种代码
m_strProductName	str	品种名称
m_strInstrumentID	str	证券代码
m_strInstrumentName	str	证券名称
m_strTradeID	str	成交编号
m_strOrderRef	str	下单引用，等于股票的内部委托号
m_strOrderSysID	str	合同编号，报单编号，委托号
m_nDirection	int	EEntrustBS，买卖方向 对于股票该值始终是48
m_nOffsetFlag	int	EOffset_Flag_Type，买卖/开平，用此字段区分股票买卖，期货开、平仓，期权买卖等
m_nHedgeFlag	int	EHedge_Flag_Type 类型，投保
m_dPrice	float	成交均价
m_nVolume	int	成交量，期货单位手，股票做到股
m_strTradeDate	str	成交日期
m_strTradeTime	str	成交时间
m_dCommission	float	手续费 (旧版本为 m_dComission)
m_dTradeAmount	float	成交额，期货 = 均价 * 量 * 合约乘数
m_nTaskId	int	任务号
m_nOrderPriceType	int	EBrokerPriceType 类型，例如市价单、限价单
m_strOptName	str	买卖标记，展示委托属性的中文
m_eEntrustType	int	EEntrustTypes，委托类别
m_eFutureTradeType	int	EFutureTradeType 类型，成交类型
m_nRealOffsetFlag	int	EOffset_Flag_Type 类型，实际开平，主要是区分平今和平昨
m_eCoveredFlag	int	ECoveredFlag类型，备兑标记 '0' - 非备兑，'1' - 备兑
m_nCloseTodayVolume	int	平今量，不显示
m_dOrderPriceRMB	float	委托价格（人民币），目前用于港股通
m_dPriceRMB	float	成交价格（人民币），目前用于港股通
m_dTradeAmountRMB	float	成交金额（人民币），目前用于港股通
m_dReferenceRate	float	汇率，目前用于港股通
m_strXTTrade	str	是否是迅投交易
m_strCompactNo	str	合约编号
m_dCloseProfit	float	平仓盈亏，目前用于外盘
m_strRemark	str	投资备注
m_strAccountKey	str	账号key，唯一区别不同账号的key
m_nRef	int	订单编号
Position - 持仓对象
字段名	数据类型	含义
m_strAccountID	string	资金账号
m_strExchangeID	string	证券市场
m_strExchangeName	string	市场名称
m_strProductID	string	品种代码
m_strProductName	string	品种名称
m_strInstrumentID	string	证券代码
m_strInstrumentName	string	证券名称
m_nHedgeFlag	int	EHedge_Flag_Type 类型，投保 ，股票不适用
m_nDirection	int	EEntrustBS，买卖方向 对于股票该值始终是48
m_strOpenDate	string	开仓日期 股票此字段无效
m_strTradeID	string	成交号，最初开仓位的成交
m_nVolume	int	当前拥股/持仓量
m_dOpenPrice	float	持仓成本 ；持仓成本 = (总买入金额 - 总卖出金额) / 剩余数量
m_strTradingDay	string	在实盘运行中是当前交易日，在回测中是股票最后交易过的日期
m_dMargin	float	使用的保证金，历史的直接用ctp的，新的自己用成本价存量系数算，股票不适用
m_dOpenCost	float	开仓成本，等于成本价*第一次建仓的量，后续减持会影响，不算手续费，股票不适用
m_dSettlementPrice	float	最新结算价/当前价
m_nCloseVolume	int	平仓量（对于股票不适用）
m_dCloseAmount	float	平仓额（对于股票不适用）
m_dFloatProfit	float	浮动盈亏
m_dCloseProfit	float	平仓盈亏（对于股票不适用）
m_dMarketValue	float	市值/合约价值
m_dPositionCost	float	持仓成本（对于股票不适用）
m_dPositionProfit	float	持仓盈亏（对于股票不适用）
m_dLastSettlementPrice	float	最新结算价（对于股票不适用）
m_dInstrumentValue	float	合约价值（对于股票不适用）
m_bIsToday	bool	是否今仓
m_strStockHolder	string	股东账号
m_nFrozenVolume	int	冻结数量
m_nCanUseVolume	int	可用数量
m_nOnRoadVolume	int	在途股份
m_nYesterdayVolume	int	昨夜拥股
m_dLastPrice	float	最新价/当前价
m_dAvgOpenPrice	float	开仓均价（对于股票不适用）
m_dProfitRate	float	盈亏比例
m_eFutureTradeType	int	EFutureTradeType 类型，成交类型
m_strExpireDate	string	到期日（针对逆回购）
m_strComTradeID	string	组合成交号
m_nLegId	int	组合序号
m_dTotalCost	float	累计成本（自定义，股票信用用到）
m_dSingleCost	float	单股成本（自定义，股票信用用
m_nCoveredVolume	int	备兑数量，用于个股期权
m_eSideFlag	int	持仓类型 ，用于个股期权，标记 '0' - 权利，'1' - 义务，'2' - '备兑'
m_dReferenceRate	float	汇率，目前用于港股通
m_dStructFundVol	float	分级基金可用（可分拆或可合并）
m_dRedemptionVolume	float	分级基金可赎回量
m_nPREnableVolume	int	申赎可用量（记录当日申购赎回的股票或基金数量）
m_dRealUsedMargin	float	实时占用保证金，用于期权
m_dRoyalty	float	权利金
m_dStockLastPrice	float	标的证券最新价，用于期权
m_dStaticHoldMargin	float	静态持仓占用保证金，用于期权
m_nOptCombUsedVolume	int	期权组合占用数量
m_nEnableExerciseVolume	int	能够行使的数量，用于个股期权
m_strAccountKey	string	账号key，唯一区别不同账号的key
PositionStatistics - 持仓统计对象
字段名	数据类型	描述
m_strAccountID	string	账号
m_strExchangeID	string	市场代码
m_strExchangeName	string	市场名称
m_strProductID	string	品种代码
m_strInstrumentID	string	合约代码
m_strInstrumentName	string	合约名称
m_nDirection	int	多空
m_nHedgeFlag	int	投保
m_nPosition	int	持仓
m_nYestodayPosition	int	昨仓
m_nTodayPosition	int	今仓
m_nCanCloseVol	int	可平
m_dPositionCost	float	持仓成本
m_dAvgPrice	float	持仓均价
m_dPositionProfit	float	持仓盈亏
m_dFloatProfit	float	浮动盈亏
m_dOpenPrice	float	开仓均价
m_dUsedMargin	float	已使用保证金
m_dUsedCommission	float	已使用的手续费
m_dFrozenMargin	float	冻结保证金
m_dFrozenCommission	float	冻结手续费
m_dInstrumentValue	float	市值，合约价值
m_nOpenTimes	int	开仓次数
m_nOpenVolume	int	总开仓量 中间平仓不减
m_nCancelTimes	int	撤单次数
m_dLastPrice	float	最新价
m_dRiseRatio	float	当日涨幅
m_strProductName	string	产品名称
m_dRoyalty	float	权利金市值
m_strExpireDate	string	到期日
m_dAssestWeight	float	资产占比
m_dIncreaseBySettlement	float	当日涨幅（结）
m_dMarginRatio	float	保证金占比
m_dFloatProfitDivideByUsedMargin	float	浮盈比例（保证金）
m_dFloatProfitDivideByBalance	float	浮盈比例（动态权益）
m_dTodayProfitLoss	float	当日盈亏（结）
m_nYestodayInitPosition	int	昨日持仓
m_dFrozenRoyalty	float	冻结权利金
m_dTodayCloseProfitLoss	float	当日盈亏（收）
m_dCloseProfit	float	平仓盈亏
m_strFtProductName	string	品种名称
m_dOpenCost	float	开仓成本
CCreditAccountDetail - 信用账号对象(非查柜台)
字段名	数据类型	解释
m_strAccountID	str	资金账号
m_nBrokerType	int	账号类型，1-期货账号，2-股票账号，3-信用账号，5-期货期权账号，6-股票期权账号，7-沪港通账号，11-深港通账号
m_strAccountKey	str	唯一区别不同账号的key
m_dMaxMarginRate	float	保证金比率，股票的保证金率等于1
m_dFrozenMargin	float	冻结保证金，外源性，股票的保证金就是冻结资金，股票不适用
m_dFrozenCash	float	冻结金额，内外源冻结保证金和手续费四个的和
m_dFrozenCommission	float	冻结手续费，外源性冻结资金源
m_dRisk	float	风险度，冻结资金/可用资金
m_dNav	float	单位净值
m_dPreBalance	float	期初权益，也叫静态权益，股票不适用
m_dBalance	float	总资产，动态权益，即市值
m_dAvailable	float	可用金额
m_dCommission	float	手续费(旧版本为 m_dComission)
m_dPositionProfit	float	持仓盈亏
m_dCloseProfit	float	平仓盈亏，股票不适用
m_dCashIn	float	出入金净值
m_dCurrMargin	float	当前使用的保证金，股票不适用
m_dInitBalance	float	初始权益
m_strStatus	str	状态
m_dInitCloseMoney	float	期初平仓盈亏，初始平仓盈亏
m_dInstrumentValue	float	总市值，合约价值，合约价值
m_dDeposit	float	入金
m_dWithdraw	float	出金
m_dPreCredit	float	上次信用额度，股票不适用
m_dPreMortgage	float	上次质押，股票不适用
m_dMortgage	float	质押，股票不适用
m_dCredit	float	信用额度，股票不适用
m_dAssetBalance	float	证券初始资金，股票不适用
m_strOpenDate	str	起始日期股票不适用
m_dFetchBalance	float	可取金额
m_strTradingDate	str	交易日
m_dStockValue	float	股票总市值，期货没有
m_dLoanValue	float	债券总市值，期货没有
m_dFundValue	float	基金总市值，包括 ETF 和封闭式基金，期货没有
m_dRepurchaseValue	float	回购总市值，所有回购，期货没有
m_dLongValue	float	多单总市值，现货没有
m_dShortValue	float	单总市值，现货没有
m_dNetValue	float	净持仓总市值，净持仓市值 = 多 - 空
m_dAssureAsset	float	净资产
m_dEntrustAsset	float	可信资产，用于校对
m_dInstrumentValueRMB	float	总市值（人民币），沪港通
m_dSubscribeFee	float	申购费，申购费
m_dGoldValue	float	库存市值，黄金现货库存市值
m_dGoldFrozen	float	现货冻结，黄金现货冻结
m_dMargin	float	占用保证金，维持保证金
m_strMoneyType	str	币种
m_dPurchasingPower	float	购买力，盈透购买力
m_dRawMargin	float	原始保证金
m_dBuyWaitMoney	float	买入待交收金额（元），买入待交收
m_dSellWaitMoney	float	卖出待交收金额（元），卖出待交收
m_dReceiveInterestTotal	float	本期间应计利息
m_dRoyalty	float	权利金收支，期货期权用
m_dFrozenRoyalty	float	冻结权利金，期货期权用
m_dRealUsedMargin	float	实时占用保证金，用于股票期权
m_dRealRiskDegree	float	实时风险度
m_dPerAssurescaleValue	float	个人维持担保比例
m_dEnableBailBalance	float	可用保证金
m_dUsedBailBalance	float	已用保证金
m_dAssureEnbuyBalance	float	可买担保品资金
m_dFinEnbuyBalance	float	可买标的券资金
m_dSloEnrepaidBalance	float	可还券资金
m_dFinEnrepaidBalance	float	可还款资金
m_dFinMaxQuota	float	融资授信额度
m_dFinEnableQuota	float	融资可用额度
m_dFinUsedQuota	float	融资已用额度
m_dFinUsedBail	float	融资已用保证金额
m_dFinCompactBalance	float	融资合约金额
m_dFinCompactFare	float	融资合约费用
m_dFinCompactInterest	float	融资合约利息
m_dFinMarketValue	float	融资市值
m_dFinIncome	float	融资合约盈亏
m_dSloMaxQuota	float	融券授信额度
m_dSloEnableQuota	float	融券可用额度
m_dSloUsedQuota	float	融券已用额度
m_dSloUsedBail	float	融券已用保证金额
m_dSloCompactBalance	float	融券合约金额
m_dSloCompactFare	float	融券合约费用
m_dSloCompactInterest	float	融券合约利息
m_dSloMarketValue	float	融券市值
m_dSloIncome	float	融券合约盈亏
m_dOtherFare	float	其它费用
m_dUnderlyMarketValue	float	标的证券市值
m_dFinEnableBalance	float	可融资金额
m_dDiffEnableBailBalance	float	可用保证金调整值
m_dBuySecuRepayFrozenMargin	float	买券还券冻结资金
m_dBuySecuRepayFrozenCommission	float	买券还券冻结手续费
m_dSpecialEnableBalance	float	专项可融金额
m_dEncumberedAssets	float	担保资产
m_dSloSellBalance	float	融券卖出资金
m_dDiffAssureEnbuyBalance	float	可买担保品资金调整值
m_dDiffFinEnbuyBalance	float	可买标的券资金调整值
m_dDiffFinEnrepaidBalance	float	可还款资金调整值
m_dOtherRealCompactBalance	float	其他负债合约金额
m_dOtherFinCompactInterest	float	其他负债合约利息金额
m_dUsedSloSellBalance	float	已用融券卖出资金
m_dFetchAssetBalance	float	可提出资产总额
m_dTotalEnableQuota	float	可用总信用额度
m_dTotalUsedQuota	float	已用总信用额度
m_dDebtProfit	float	负债总浮盈
m_dDebtLoss	float	负债总浮亏
m_nContractEndDate	int	合同到期日期
m_dFinDebt	float	融资负债
m_dFinProfitAmortized	float	融资浮盈折算
m_dSloProfit	float	融券浮盈
m_dSloProfitAmortized	float	融券浮盈折算
m_dFinLoss	float	融资浮亏
m_dSloLoss	float	融券浮亏
CCreditDetail - 两融资金信息(查柜台)
字段名	数据类型	解释
m_dPerAssurescaleValue	float	维持担保比例
m_dBalance	float	总资产
m_dTotalDebt	float	总负债
m_dAssureAsset	float	净资产
m_dMarketValue	float	总市值
m_dEnableBailBalance	float	可用保证金
m_dAvailable	float	可用资金
m_dFinDebt	float	融资负债
m_dFinDealAvl	float	融资本金
m_dFinFee	float	融资息费
m_dSloDebt	float	融券负债
m_dSloMarketValue	float	融券市值
m_dSloFee	float	融券息费
m_dOtherFare	float	其它费用
m_dFinMaxQuota	float	融资授信额度
m_dFinEnableQuota	float	融资可用额度
m_dFinUsedQuota	float	融资冻结额度
m_dSloMaxQuota	float	融券授信额度
m_dSloEnableQuota	float	融券可用额度
m_dSloUsedQuota	float	融券冻结额度
m_dSloSellBalance	float	融券卖出资金
m_dUsedSloSellBalance	float	已用融券卖出资金
m_dSurplusSloSellBalance	float	剩余融券卖出资金
m_dStockValue	float	股票市值
m_dFundValue	float	基金市值
error	string	错误信息
CreditSloEnableAmount - 可融券明细对象
提示

由于字段m_dSloRatio、m_dSloStatus提供来源和取担保品明细get_assure_contract重复，字段在2021年9月移除，后续用担保品明细接口获取,具体见 担保标的对象字段说明

字段名	数据类型	解释
m_nPlatformID	int	平台号
m_strBrokerID	string	经纪公司编号
m_strBrokerName	string	经纪公司
m_strAccountID	string	资金账号
m_strExchangeID	string	交易所
m_strInstrumentID	string	证券代码
m_nEnableAmount	int	融券可融数量
m_eQuerySloType	enum	EXTSloTypeQueryMode，查询类型
StkCompacts - 负债合约对象
字段名	数据类型	解释
m_strAccountID	string	资金账号，账号，账号，资金账号
m_strExchangeID	string	交易所
m_strInstrumentID	string	证券代码
m_strExchangeName	string	交易所名称
m_strInstrumentName	string	股票名称
m_nOpenDate	int	合约开仓日期
m_strCompactId	string	合约编号
m_dCrdtRatio	float	融资融券保证金比例
m_strEntrustNo	string	委托编号
m_dEntrustPrice	float	委托价格
m_nEntrustVol	int	委托数量
m_nBusinessVol	int	合约开仓数量
m_dBusinessBalance	float	合约开仓金额
m_dBusinessFare	float	合约开仓费用
m_eCompactType	enum	EXTCompactType，合约类型
m_eCompactStatus	enum	EXTCompactStatus，合约状态
m_dRealCompactBalance	float	未还合约金额
m_nRealCompactVol	int	未还合约数量
m_dRealCompactFare	float	未还合约费用
m_dRealCompactInterest	float	未还合约利息
m_dRepaidInterest	float	已还利息
m_nRepaidVol	int	已还数量
m_dRepaidBalance	float	已还金额
m_dCompactInterest	float	合约总利息
m_dUsedBailBalance	float	占用保证金
m_dYearRate	float	合约年利率
m_nRetEndDate	int	归还截止日
m_strDateClear	string	了结日期
m_strPositionStr	string	定位串
m_dPrice	float	最新价
m_nOpenTime	int	合约开仓时间
m_nCancelVol	int	合约撤单数量
m_eCashgroupProp	enum	EXTCompactBrushSource，头寸来源
m_dUnRepayBalance	float	负债金额
m_nRepayPriority	int	偿还优先级
m_dRealDefaultInterest	float	未还罚息
m_dOtherRealCompactBalance	float	其他负债合约金额
m_dOtherRealCompactInterest	float	其他负债合约利息金额
StkSubjects - 担保标的对象
字段名	数据类型	解释
m_nPlatformID	int	平台号//目前主要用于区别不同的行情，根据此来选择对应行情
m_strBrokerID	string	经纪公司编号
m_strBrokerName	string	经纪公司名称
m_strExchangeID	string	交易所
m_strInstrumentID	string	证券代码
m_dSloRatio	float	融券保证金比例
m_eSloStatus	enum	EXTSubjectsStatus，融券状态
m_dFinRatio	float	融资保证金比例
m_eFinStatus	enum	EXTSubjectsStatus，融资状态
m_strAccountID	string	资金账号
m_eCreditFundCtl	enum	EXTCreditFundCtl，融资交易控制
m_eCreditStkCtl	enum	EXTCreditStkCtl，融券交易控制
m_eAssureStatus	enum	EXTSubjectsStatus，是否可做担保
m_dAssureRatio	float	担保品折算比例
PassorderArguments - 下单函数参数对象
字段名	数据类型	解释
opType	int	passorder的opType参数
orderType	int	passorder的orderType参数
accountID	string	资金账号
orderCode	string	交易代码
prType	int	passorder的prType，价格类型
modelPrice	float	下单价格
modelVolume	int	下单量（手数或股数）
strategyName	string	策略名 _ &&& _ 投资备注
CTaskDetail - 任务对象
字段名	数据类型	解释
m_nTaskId	int	任务号
m_eStatus	enum	任务状态 ETaskStatus类型,见ETaskStatus说明
m_strMsg	string	任务状态消息
m_startTime	int	任务开始时间, 时间戳类型
m_endTime	int	任务结束时间, 时间戳类型
m_cancelTime	int	任务取消时间
m_nBusinessNum	int	已成交量
m_nGroupId	int	组合Id
m_stockCode	string	下单代码(不针对组合下单)
m_strAccountID	string	下单用户(单用户下单)
m_eOperationType	enum	下单操作：开平、多空……EOperationType类型, 见EOperationType说明
m_eOrderType	enum	算法交易、普通交易 EOrderType类型, 见EOrderType说明
m_ePriceType	enum	报价方式：对手、最新…… EPriceType类型见EPriceType说明
m_dFixPrice	float	委托价
m_nNum	int	委托量
m_strRemark	string	投资备注
CLockPosition - 期权标的持仓
字段名	数据类型	解释
m_strAccountID	string	账号名
m_strExchangeID	string	交易所
m_strExchangeName	string	交易所名
m_strInstrumentID	string	标的代码
m_strInstrumentName	string	标的名称
m_totalVol	int	总持仓量
m_lockVol	int	可用锁定量
m_unlockVol	int	未锁定量
m_coveredVol	int	备兑量
m_nOnRoadcoveredVol	int	在途备兑量
CStkOptCombPositionDetail - 期权组合持仓
字段名	数据类型	解释
m_strAccountID	string	账号名
m_strExchangeID	string	交易所
m_strExchangeName	string	交易所名
m_strContractAccount	string	合约账号
m_strCombID	string	组合编号
m_strCombCode	string	组合策略编码
m_strCombCodeName	string	组合策略名称
m_nVolume	int	持仓量
m_nFrozenVolume	int	冻结数量
m_nCanUseVolume	int	可用数量
m_strFirstCode	string	合约一
m_eFirstCodeType	enum	合约一类型 认购:48,认沽:49
m_strFirstCodeName	string	合约一名称
m_eFirstCodePosType	enum	合约一持仓类型 认购:48,义务:49,备兑:50
m_nFirstCodeAmt	int	合约一数量
m_strSecondCode	string	合约二
m_eSecondCodeType	enum	合约二类型 认购:48,认沽:49
m_strSecondCodeName	string	合约二名称
m_eSecondCodePosType	enum	合约二持仓类型 权利:48,义务:49,备兑:50
m_nSecondCodeAmt	int	合约二数量
m_dCombBailBalance	float	占用保证金
entrustType - 委托类型
0 - 未知
1 - 正常交易业务
2 - 即时成交剩余撤销
3 - ETF基金申报
4 - 最优五档即时成交剩余撤销
5 - 全额成交或撤销
6 - 本方最优价格
7 - 对手方最优价格
openInt - 证券状态（股票）
编码	状态
0,10	默认为未知
1	停牌
11	开盘前S
12	集合竞价时段C
13	连续交易T
14	休市B
15	闭市E
16	波动性中断V,例如(10006742.SHO)50ETF沽9月2300在2024/08/28 10:15:34 - 2024/08/28 10:18:34 触发熔断临时停牌，此时的openInt值为16
17	临时停牌P
18	收盘集合竞价U
19	盘中集合竞价M
20	暂停交易至闭市N
21	获取字段异常
22	盘后固定价格行情
23	盘后固定价格行情完毕
openInt - 证券状态（期货）
编码	状态
0	默认为未知
1	开盘前S
2	集合竞价时段C
3	连续交易T
4	休市B
5	闭市E
##################################################
'''
3系统函数
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
ContextInfo 对象
ContextInfo 是策略运行环境对象，是 init, after_init, handlebar 等基本方法的入参，里面包括了终端自带的属性和方法。一般情况下不建议对ContextInfo添加自定义属性，ContextInfo会随着bar的切换而重置到上一根bar的结束状态，建议用自建的全局变量来存储。详细说明请看这里

init - 初始化函数
初始化函数，只在整个策略开始时调用运行到一次。用于初始订阅行情，订阅账号信息使用。init函数执行完成前部分接口无法使用，如交易日获取函数get_trading_dates。

系统函数 不可被手动调用

参数：

名称	类型	描述
ContextInfo	object	策略运行环境对象，可以用于存储自定义的全局变量
返回： 无

示例：

python

def init(ContextInfo):
    ContextInfo.initProfit = 0
在init函数中订阅行情示例：

python

#coding:gbk

def init(C):
	#init函数入参为ContextInfo对象 定义时可以选择更简短的形参名 如C
	#在init函数中 可以进行 订阅行情的操作
    #如需在行情回调函数中下单 下单函数需要传入ContextInfo对象 可以通过在init中定义回调函数 来使用外层的ContextInfo
	def my_callback_function(data):
		#自定义行情回调函数 入参为指数据字典
		print(data)
	stock = '600000.SH'
	C.subscribe_quote(stock, period = '5m', callback = my_callback_function)
	#init函数执行完成后 
	print('init函数执行完成')
after_init - 初始化后函数
后初始化函数，在初始化函数执行完成后被调用一次。可以用于放置一次性触发的下单，取数据操作代码。

系统会在init函数执行完后和执行handlebar之前调用after_init, 有些init里不支持的函数比如ContextInfo.get_trading_dates可以在after_init里调用。

系统函数 不可被手动调用

参数：

名称	类型	描述
ContextInfo	object	策略运行环境对象，可以用于存储自定义的全局变量
返回： 无

示例：

python

#coding:gbk
def init(ContextInfo):
    print('init')  


def after_init(ContextInfo):
    print('系统会在init函数执行完后和执行handlebar之前调用after_init')


def handlebar(ContextInfo):
    if ContextInfo.is_last_bar():
        print('handlebar')

after_init函数中立刻下单示例：

python

#coding:gbk

def after_init(C):
	#after_init 函数 可以用于执行运行开始时 需要执行一次的代码 例如下一笔委托
	#account变量是模型交易界面 添加策略时选择的资金账号 不需要手动填写 交易模型需要在模型交易界面运行 才有效
	#快速交易参数(quickTrade )填2 passorder函数执行后立刻下单 不会等待k线走完再委托。 可以在after_init函数 run_time函数注册的回调函数里进行委托 
	msg = f"投资备注字符串 用来区分不同委托"
	passorder(23, 1101, account, '600000.SH', 5, -1, 100, '测试下单', 2, msg, C)
handlebar - 行情事件函数
系统函数 不可被手动调用

释义： 行情事件函数，每根 K 线运行一次；实时行情获取状态下，先每根历史 K 线运行一次，再在每个 tick 数据来后驱动运行一次

历史k线上，按时间顺序每根K线触发一次调用；盘中，每个新到达的TICK数据驱动运行一次。可以作为行情驱动的函数，实现指标计算，回测，实盘下单的效果。

参数：

名称	类型	描述
ContextInfo	object	策略运行环境对象，可以用于存储自定义的全局变量
返回： 无

示例：


def handlebar(ContextInfo):
    # 输出当前运行到的 K 线的位置
    print(ContextInfo.barpos)
ContextInfo.schedule_run - 设置定时器
说明

该函数是新版设置定时器函数，相比旧版run_time，新版schedule_run新增了任务分组,任务取消等多种功能
原型:

python

ContextInfo.schedule_run(
    func:Callable, # 回调函数，到达定时器预定时间时触发调用，参数为ContextInfo类型，无需返回值
    time_point:Union[dt.datetime,str], # 表示预定的第一次触发时间，如果设置定时器时已经过了预定时间，会立即执行func以及后续逻辑；当使用str类型时，格式为'yyyymmddHHMMSS'如'20231231235959'，需要满足转换dt.datetime.strptime('20231231235959','%Y%m%d%H%M%S')
    repeat_times:int=0, # 表示在预定时间触发后按interval间隔再触发多少次
    interval:datetime.timedelta=None, # 表示预定时间触发后的后续重复执行的时间间隔
    name:str='' # 定时器任务组名，可用于定时器分组，多次设置同名定时任务不会互相覆盖，会计入同一个任务组，按任务组名取消时会全部取消
    )
参数：

名称	类型	描述
func	Callable	回调函数，到达定时器预定时间时触发调用，参数为ContextInfo类型，无需返回值，定义示例如下：
def on_timer(C:ContextInfo): pass
time_point	Union[datetime.datetime,str]	表示预定的第一次触发时间，如果设置定时器时已经过了预定时间，会立即执行func以及后续逻辑；
当使用str类型时，格式为'yyyymmddHHMMSS'如'20231231235959'，需要满足转换datetime.datetime.strptime('20231231235959','%Y%m%d%H%M%S')
repeat_times	int	表示在预定时间触发后按interval间隔再触发多少次，传-1表示不限制次数
interval	datetime.timedelta	表示预定时间触发后的后续重复执行的时间间隔
name	str	定时器任务组名，可用于定时器分组，多次设置同名定时任务不会互相覆盖，会计入同一个任务组，按任务组名取消时会全部取消
回调函数参数： ContextInfo：策略模型全局对象

返回值：

int类型，表示本次调用后生成的定时任务号，可用于取消本次定时任务，全局唯一不重复

示例：

python

import datetime as dt
def on_timer(C:ContextInfo):
    print('hello world')
def init(ContextInfo):
    tid=ContextInfo.schedule_run(on_timer,'20231231235959',-1,dt.timedelta(minutes=1),'my_timer')
def handlebar(ContextInfo):
    pass
#此例为自2023-12-31 23:59:59后每60s运行一次on_timer
ContextInfo.cancel_schedule_run - 取消由schedule_run产生的定时任务
原型：

python

ContextInfo.cancel_schedule_run(
    key:Union[seq:int,name:str] # 定时任务号或定时任务组名称
    )
参数：

名称	类型	描述
key:	Union[seq:int,name:str]	类型为int时，表示按任务号取消;类型为str时，表示按任务组取消，会取消组内所有定时任务
返回值：

bool类型，表示是否取消成功，即是否能按key找到目标定时任务

示例：

示例


ContextInfo.cancel_schedule_run('my_timer') #取消my_timer任务组所有定时任务
ContextInfo.cancel_schedule_run(1) #取消任务号为1的定时任务

ContextInfo.run_time - 设置定时器
设置定时器函数，可以指定时间间隔，定时触发用户定义的回调函数。适用与在盘中，持续判断交易信号的模型。

用法： ContextInfo.run_time(funcName,period,startTime) 定时触发指定的 funcName函数, funcName函数由用户定义, 入参为ContextInfo对象。

参数：

funcName：回调函数名
period：重复调用的时间间隔,'5nSecond'表示每5秒运行1次回调函数,'5nDay'表示每5天运行一次回调函数,'500nMilliSecond'表示每500毫秒运行1次回调函数
startTime：表示定时器第一次启动的时间,如果要定时器立刻启动,可以设置历史的时间
回调函数参数： ContextInfo：策略模型全局对象

示例：

python

import time
def init(ContextInfo):
    ContextInfo.run_time("f","5nSecond","2019-10-14 13:20:00")
def f(ContextInfo):
    print('hello world')

#此例为自2019-10-14 13:20:00后每5s运行一次函数f
注意

模型回测时无效
定时器没有结束方法，会随着策略的结束而结束。
period有nMilliSecond、nSecond和Day三个周期单元，部分周期下定时器函数在第一次运行之前会先等待一个period
stop - 停止处理函数
系统函数 不可被手动调用

释义： PY策略模型关闭停止前运行到的函数，复杂策略模型，如中间有起线程可通过在该函数内实现停止线程操作。注意, 当前版本stop函数被调用时交易连接已断开, 不能在stop函数中做报单 / 撤单操作.

参数：

名称	类型	描述
ContextInfo	object	策略运行环境对象，可以用于存储自定义的全局变量
示例：

python

def stop(ContextInfo):
    print( 'strategy is stop !')
ContextInfo.is_last_bar - 是否为最后一根K线
用法： ContextInfo.is_last_bar()

释义： 判定是否为最后一根 K 线

参数： 无

返回： bool，返回值含义：True 是右侧最新k线 False不是最新k线

True：是

False：否

示例：

pythonresult

def handlebar(ContextInfo):
    print(ContextInfo.is_last_bar())
ContextInfo.is_new_bar - 判定是否为新的 K 线
用法： ContextInfo.is_new_bar()

释义： 某根 K 线的第一个 tick 数据到来时，判定该 K 线为新的 K 线，其后的tick不会认为是新的 K 线

参数： 无

返回： bool，返回值含义：

True：是

False：否

示例：

pythonresult

def handlebar(ContextInfo):
    print(ContextInfo.is_new_bar()) #历史k线每根都是新k线 盘中 每根新k线第一个分笔返回True 其他分笔返回False
ContextInfo.get_stock_name - 根据代码获取名称
注意

我们计划后续版本抛弃这个函数，不建议继续使用，可以用ContextInfo.get_instrument_detail("stockcode")["InstrumentName"]来实现同样功能

用法： ContextInfo.get_stock_name('stockcode')

释义： 根据代码获取名称

参数： stockcode：股票代码，如'000001.SZ'，缺省值 ' ' 默认为当前图代码

返回： string（GBK编码）

示例：

示例返回值

def handlebar(ContextInfo):
    print(ContextInfo.get_stock_name('000001.SZ'))
ContextInfo.get_open_date - 根据代码返回对应股票的上市时间
用法： ContextInfo.get_open_date('stockcode')

释义： 根据代码返回对应股票的上市时间

参数： stockcode：股票代码，如'000001.SZ'，缺省值 ' ' 默认为当前图代码

返回： number

示例：

pythonresult

def init(ContextInfo):
    print(ContextInfo.get_open_date('000001.SZ'))
ContextInfo.set_output_index_property - 设定指标绘制的属性
用法： ContextInfo.set_output_index_property(index_name,draw_style=0,color='white',noaxis=False,nodraw=False,noshow=False)

释义： 设定指标绘制的属性，会最终覆盖掉指标对应的属性字段

参数：

index_name:string,指标名称，不可缺省
draw_style,同paint函数的drawstyle，可缺省默认为0
color,同paint函数的color，可缺省默认为'white'
noaxis:bool,是否无坐标，可缺省默认为False
nodraw:bool,是否不画线，可缺省默认为False
noshow:bool,是否不展示，可缺省默认为False
返回： 无

示例：

pythonpythonresult

def init(ContextInfo):
    ContextInfo.set_output_index_property('单位净值', nodraw = True)#使回测指标'单位净值'不画线
create_sector - 创建板块
用法： create_sector(parent_node,sector_name,overwrite)

释义： 创建板块

参数：

parent_node：str，父节点，''为'我的'（默认目录）
sector_name：str，要创建的板块名
overwrite：bool，是否覆盖。如果目标节点已存在，为True时跳过，为False时在sector_name后增加数字编号，编号为从1开始自增的第一个不重复的值。
返回： sector_name2：实际创建的板块名

示例：

create_sector_folder - 创建板块目录节点
用法： create_sector_folder(parent_node,folder_name,overwrite)

释义： 创建板块目录节点

参数：

parent_node：str，父节点，''为'我的'（默认目录）
sector_name：str，要创建的节点名
overwrite：bool，是否覆盖。如果目标节点已存在，为True时跳过，为False时在folder_name后增加数字编号，编号为从1开始自增的第一个不重复的值。
返回： sector_name2：实际创建的节点名

示例：

pythonresult

folder=create_sector_folder('我的','新建分类',False)
get_sector_list - 获取板块目录信息
用法： get_sector_list(node)

释义： 获取板块目录信息

参数：

node：str，板块节点名，''为顶层目录
返回： info_list：[[s1,s2,...],[f1,f2,...]]s为板块名，f为目录节点名，例如[['我的自选'],['新建分类1']]

示例：

pythonresult

get_sector_list('我的')
reset_sector_stock_list - 设置板块成分股
用法： reset_sector_stock_list(sector,stock_list)

释义： 设置板块成分股

参数：

sector：板块名
stock_list：list，品种代码列表，例如['000001.SZ','600000.SH']
返回： result：bool，操作成功为True，失败为False

示例：

pythonresult

reset_sector_stock_list('我的自选',['000001.SZ','600000.SH'])
remove_stock_from_sector - 移除板块成分股
用法： remove_stock_from_sector(sector,stock_code)

释义： 移除板块成分股

参数：

sector：板块名
stock_code：品种代码，例如'000001.SZ'
返回： result：bool，操作成功为True，失败为False

示例：

pythonresult

remove_stock_from_sector('我的自选','000001.SZ')
add_stock_to_sector - 添加板块成分股
用法： add_stock_to_sector(sector,stock_code)

释义： 添加板块成分股

参数：

sector：板块名
stock_code：品种代码，例如'000001.SZ'
返回： result：bool，操作成功为True，失败为False

示例：

pythonresult

add_stock_to_sector('我的自选','000001.SZ')
##############################################
'''
4行情函数
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
获取行情数据
该目录下的函数用于获取实时行情,历史行情

ContextInfo.get_market_data_ex - 获取行情数据
注意

该函数不建议在init中运行,在init中运行时仅能取到本地数据
关于获取行情函数之间的区别与注意事项可在 - 常见问题-行情相关 查看
除实时行情外，该函数还可用于获取特色数据，如资金流向数据,订单流数据等，获取方式见数据字典
原型

内置python

ContextInfo.get_market_data_ex(
    fields=[], 
    stock_code=[], 
    period='follow', 
    start_time='', 
    end_time='', 
    count=-1, 
    dividend_type='follow', 
    fill_data=True, 
    subscribe=True)
释义

获取实时行情与历史行情数据

参数

名称	类型	描述
field	list	数据字段，详情见下方field字段表
stock_list	list	合约代码列表
period	str	数据周期，可选字段为:
"tick"
"1m"：1分钟线
"5m"：5分钟线；"15m"：15分钟线；"30m"：30分钟线
"1h"小时线
"1d"：日线
"1w"：周线
"1mon"：月线
"1q"：季线
"1hy"：半年线
"1y"：年线
'l2quote'：Level2行情快照
'l2quoteaux'：Level2行情快照补充
'l2order'：Level2逐笔委托
'l2transaction'：Level2逐笔成交
'l2transactioncount'：Level2大单统计
'l2orderqueue'：Level2委买委卖队列
start_time	str	数据起始时间，格式为 %Y%m%d 或 %Y%m%d%H%M%S，填""为获取历史最早一天
end_time	str	数据结束时间，格式为 %Y%m%d 或 %Y%m%d%H%M%S ，填""为截止到最新一天
count	int	数据个数
dividend_type	str	除权方式,可选值为
'none'：不复权
'front':前复权
'back':后复权
'front_ratio': 等比前复权
'back_ratio': 等比后复权
fill_data	bool	是否填充数据
subscribe	bool	订阅数据开关，默认为True，设置为False时不做数据订阅，只读取本地已有数据。
field字段可选：
field	数据类型	含义
time	int	时间
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
volume	float	成交量
amount	float	成交额
settle	float	今结算
openInterest	float	持仓量
preClose	float	前收盘价
suspendFlag	int	停牌 1停牌，0 不停牌
period周期为tick时，field字段可选:
field	数据类型	含义
time	int	时间
lastPrice	float	最新价
lastClose	float	前收盘价
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
volume	float	成交量
amount	float	成交额
settle	float	今结算
openInterest	float	持仓量
stockStatus	int	停牌 1停牌，0 不停牌
period周期为Level2数据时，字段参考数据结构
返回值

返回dict { stock_code1 : value1, stock_code2 : value2, ... }
value1, value2, ... ：pd.DataFrame 数据集，index为time_list，columns为fields,可参考Bar字段
各标的对应的DataFrame维度相同、索引相同
示例

示例data1返回值data2返回值data3返回值data4返回值历史tick期货五档盘口

# coding:gbk
import pandas as pd
import numpy as np

def init(C):	
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]# 指定获取的标的
	C.start_time = "20230901"# 指定获取数据的开始时间
	C.end_time = "20231101"# 指定获取数据的结束时间
	
def handlebar(C):
	# 获取多只股票，多个字段，一条数据
	data1 = C.get_market_data_ex([],C.stock_list, period = "1d",count = 1)
	# 获取多只股票，多个字段，指定时间数据
	data2 = C.get_market_data_ex([],C.stock_list, period = "1d", start_time = C.start_time, end_time = C.end_time)
	# 获取多只股票，多个字段，指定时间15m数据
	data3 = C.get_market_data_ex([],C.stock_list, period = "15m", start_time = C.start_time, end_time = C.end_time)
	# 获取多只股票，指定字段，指定时间15m数据
	data4 = C.get_market_data_ex(["close","open"],C.stock_list, period = "15m", start_time = C.start_time, end_time = C.end_time)
	# 获取多只股票，历史tick
	tick = C.get_market_data_ex([],C.stock_list, period = "tick", start_time = C.start_time, end_time = C.end_time)
	# 获取期货5档盘口tick
	future_lv2_quote = C.get_market_data_ex([],["rb2405.SF","ec2404.INE"], period = "l2quote", count = 1)
	print(data1)
	print(data2["000001.SZ"].tail())
	print(data3)
	print(data4["000001.SZ"])
	print(data4["000001.SZ"].to_csv("your_path")) # 导出文件为csv格式，路径填本机路径
	print(tick["000001.SZ"])
	print(future_lv2_quote)

ContextInfo.get_full_tick - 获取全推数据
提示

不能用于回测 只能取最新的分笔，不能取历史分笔

原型

内置python

ContextInfo.get_full_tick(stock_code=[])
释义

获取最新分笔数据

参数

名称	类型	描述
stock_code	list[str]	合约代码列表，如['600000.SH','600036.SH']，不指定时为当前主图合约。
返回值 根据stock_code返回一个dict，该字典的key值是股票代码，其值仍然是一个dict，在该dict中存放股票代码对应的最新的数据。该字典数据key值参考tick字段

示例

示例返回值

# coding:gbk
import pandas as pd
import numpy as np

def init(C):
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]
	
def handlebar(C):
	tick = C.get_full_tick(C.stock_list)
	print(tick["510050.SH"])
ContextInfo.subscribe_quote - 订阅行情数据
提示

该函数属于订阅函数，非VIP用户限制订阅数量

VIP用户支持全推市场指定周期K线

VIP用户权限请参考vip-行情用户优势对比

原型

内置python

ContextInfo.subscribe_quote(
    stock_code,
    period='follow',
    dividend_type='follow',
    result_type='',
    callback=None)
释义

订阅行情数据,关于订阅机制请参考运行机制对比

参数

字段名	数据类型	解释
stockcode	string	股票代码，'stkcode.market'，如'600000.SH'
period	string	K线周期类型
dividend_type	string	除权方式,可选值为
'none'：不复权
'front':前复权
'back':后复权
'front_ratio': 等比前复权
'back_ratio': 等比后复权
注意：分笔周期返回数据均为不复权
result_type	string	返回数据格式,可选范围：<br>'DataFrame'或''（默认）：返回{code:data}，data为pd.DataFrame数据集，index为字符串格式的时间序列，columns为数据字段<br>'dict'：返回{code:{k1:v1,k2:v2,...}}，k为数据字段名，v为字段值<br>'list'：返回{code:{k1:[v1],k2:[v2],...}}，k为数据字段名，v为字段值
callback	function	指定推送行情的回调函数
返回值

int：订阅号，用于反订阅

示例

示例返回值

# conding = gbk
def call_back(data):
	print(data)
	
def init(C):
	C.subID = C.subscribe_quote("000001.SZ","1d", callback = call_back)
def handlebar(C):
	print("============================")
	print("C.subID: ",C.subID)
	
ContextInfo.subscribe_whole_quote - 订阅全推数据
提示

内置python

ContextInfo.subscribe_whole_quote(code_list,callback=None)
释义

订阅全推数据，全推数据只有分笔周期，每次增量推送数据有变化的品种

参数

字段名	数据类型	解释
code_list	list[str,...]	市场代码列表/品种代码列表,如 ['SH','SZ'] 或 ['600000.SH', '000001.SZ']
callback	function	数据推送回调
返回值int，订阅号，可用ContextInfo.unsubscribe_quote做反订阅

示例返回值

# conding = gbk
def call_back(data):
	print(data)
	
def init(C):
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]
	C.subID = C.subscribe_whole_quote(C.stock_list,callback=call_back)
def handlebar(C):
	print("============================")
	print("C.subID: ",C.subID)
ContextInfo.unsubscribe_quote - 反订阅行情数据
原型

内置python

ContextInfo.unsubscribe_quote(subId)
释义

反订阅行情数据，配合ContextInfo.subscribe_quote()或ContextInfo.subscribe_whole_quote()使用

参数

字段名	数据类型	解释
subId	int	行情订阅返回的订阅号
示例

示例

# conding = gbk
def call_back(data):
	print(data)
def init(C):
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]
	C.subID = C.subscribe_whole_quote(C.stock_list,callback=call_back)

def handlebar(C):
	print("============================")
	print("C.subID: ",C.subID)
	if C.subID > 0:
		C.unsubscribe_quote(C.subID) # 取消行情订阅
subscribe_formula - 订阅模型
原型

内置python

subscribe_formula(
   formula_name,stock_code,period
   ,start_time="",end_time="",count=-1
   ,dividend_type="none"
   ,extend_param={}
   ,callback=None)
释义 订阅vba模型运行结果，使用前要注意补充本地K线数据或分笔数据

参数

字段名	类型	描述
formula_name	str	模型名称名
stock_code	str	模型主图代码形式如'stkcode.market'，如'000300.SH'
period	str	K线周期类型，可选范围：'tick':分笔线，'1d':日线，'1m':分钟线，'3m':三分钟线，'5m':5分钟线，'15m':15分钟线，'30m':30分钟线，'1h':小时线，'1w':周线，'1mon':月线，'1q':季线，'1hy':半年线，'1y':年线
start_time	str	模型运行起始时间，形如:'20200101'，默认为空视为最早
end_time	str	模型运行截止时间，形如:'20200101'，默认为空视为最新
count	int	模型运行范围为向前 count 根 bar，默认为 -1 运行所有 bar
dividend_type	str	复权方式，默认为主图除权方式，可选范围：'none':不复权，'front':向前复权，'back':向后复权，'front_ratio':等比向前复权，'back_ratio':等比向后复权
extend_param	dict	模型的入参，形如 {'a': 1, '__basket': {}}
__basket	dict	可选参数，组合模型的股票池权重，形如 {'600000.SH': 0.06, '000001.SZ': 0.01}
返回值 分两块，

subscribe_formula返回模型的订阅号,可用于后续反订阅，失败返回 -1

callback:

timelist： 数据时间戳
outputs：模型的输出值，结构为{变量名:值}
示例

示例

#encoding=gbk
def callback(data):
    print(data)

def init(ContextInfo):
    basket={
       '600000.SH':0.06,
       '000001.SZ':0.01
      }
    argsDict={'a':100,'__basket':basket}
    subID=subscribe_formula(
      '单股模型示范','000300.SH','1d',
      '20240101','20240201',-1,
      "none",
      argsDict,
      callback
   )

unsubscribe_formula - 反订阅模型
原型

内置python

unsubscribe_formula(subID)
释义 反订阅模型

参数

字段名	类型	描述
subID	int	模型订阅号
返回值

bool:反订阅成功为True，失败为False
示例

示例

#encoding=gbk
def callback(data):
    print(data)

def init(ContextInfo):
    basket={
       '600000.SH':0.06,
       '000001.SZ':0.01
      }
    argsDict={'a':100,'__basket':basket}
    subID=subscribe_formula(
      '单股模型示范','000300.SH','1d',
      '20240101','20240201',-1,
      "none",
      argsDict,
      callback
   )

	unsubscribe_formula(subID)
call_formula - 调用模型
原型

内置python

call_formula(formula_name,stock_code,period,start_time="",end_time="",count=-1,dividend_type="none",extend_param={})
释义 获取vba模型运行结果，使用前要注意补充本地K线数据或分笔数据

参数

字段名	类型	描述
formula_name	str	模型名称名
stock_code	str	模型主图代码形式如'stkcode.market'，如'000300.SH'
period	str	K线周期类型，可选范围：'tick':分笔线，'1d':日线，'1m':分钟线，'3m':三分钟线，'5m':5分钟线，'15m':15分钟线，'30m':30分钟线，'1h':小时线，'1w':周线，'1mon':月线，'1q':季线，'1hy':半年线，'1y':年线
start_time	str	模型运行起始时间，形如:'20200101'，默认为空视为最早
end_time	str	模型运行截止时间，形如:'20200101'，默认为空视为最新
count	int	模型运行范围为向前 count 根 bar，默认为 -1 运行所有 bar
dividend_type	str	复权方式，默认为主图除权方式，可选范围：'none':不复权，'front':向前复权，'back':向后复权，'front_ratio':等比向前复权，'back_ratio':等比向后复权
extend_param	dict	模型的入参,{"模型名:参数名":参数值},例如在跑模型MA时，{'MA:n1':1};入参可以添加__basket:dict,组合模型的股票池权重,形如{'__basket':{'600000.SH':0.06,'000001.SZ':0.01}}，如果在跑一个模型1的时候，模型1调用了模型2，如果只想修改模型2的参数可以传{'模型2:参数':参数值}
返回值 返回：dict{ 'dbt':0,#返回数据类型，0:全部历史数据 'timelist':[...],#返回数据时间范围list, 'outputs':{'var1':[...],'var2':[...]}#输出变量名：变量值list }

示例

示例

def handlebar(ContextInfo):
    basket={'600000.SH':0.06,'000001.SZ':0.01}
    argsDict={'a':100,'__basket':basket}
    modelRet=call_formula('单股模型示范','000300.SH','1d','20240101','20240201',-1,"none",argsDict)
    print(modelRet)

call_formula_batch - 批量调用模型
原型

内置python

call_formula_batch(formula_names,stock_codes,period,start_time="",end_time="",count=-1,dividend_type="none",extend_params=[])

释义 批量获取vba模型运行结果，使用前要注意补充本地K线数据或分笔数据

参数

字段名	类型	描述
formula_names	list	包含要批量运行的模型名
stock_codes	list	包含要批量运行的模型主图代码形式'stkcode.market'，如'000300.SH'
period	str	K线周期类型，可选范围：'tick':分笔线，'1d':日线，'1m':分钟线，'3m':三分钟线，'5m':5分钟线，'15m':15分钟线，'30m':30分钟线，'1h':小时线，'1w':周线，'1mon':月线，'1q':季线，'1hy':半年线，'1y':年线
start_time	str	模型运行起始时间，形如:'20200101'，默认为空视为最早
end_time	str	模型运行截止时间，形如:'20200101'，默认为空视为最新
count	int	模型运行范围为向前 count 根 bar，默认为 -1 运行所有 bar
dividend_type	str	复权方式，默认为主图除权方式，可选范围：'none':不复权，'front':向前复权，'back':向后复权，'front_ratio':等比向前复权，'back_ratio':等比向后复权
extend_params	list	包含每个模型的入参,[{"模型名:参数名":参数值}],例如在跑模型MA时，{'MA:n1':1};入参可以添加__basket:dict,组合模型的股票池权重,形如{'__basket':{'600000.SH':0.06,'000001.SZ':0.01}}，如果在跑一个模型1的时候，模型1调用了模型2，如果只想修改模型2的参数可以传{'模型2:参数':参数值}
返回值

list[dict]
dict说明:
formula:模型名
stock:品种代码
argument:参数
result:dict参考call_formula返回结果
示例

示例


def handlebar(ContextInfo):
    formulas=['testModel1','testModel2']
    codes=['600000.SH','000001.SZ']
    basket={'600000.SH':0.06,'000001.SZ':0.01}
    args=[{'a':100,'__basket':basket},{'a':200,'__basket':basket}]
    modelRet=call_formula_batch(formulas,codes,'1d',extend_params=args);
    print(modelRet)

ContextInfo.get_svol - 根据代码获取对应股票的内盘成交量
原型

内置python

ContextInfo.get_svol(stockcode)
释义

根据代码获取对应股票的内盘成交量

参数

字段名	数据类型	解释
stockcode	string	股票代码，如 '000001.SZ'，缺省值''，默认为当前图代码
返回值int:内盘成交量

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_svol('000001.SZ')
	print(data)
ContextInfo.get_bvol - 根据代码获取对应股票的外盘成交量
原型

内置python

ContextInfo.get_bvol(stockcode)
释义

根据代码获取对应股票的外盘成交量

参数

字段名	数据类型	解释
stockcode	string	股票代码，如 '000001.SZ'，缺省值''，默认为当前图代码
返回值

int:外盘成交量

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_bvol('000001.SZ')
	print(data)
ContextInfo.get_turnover_rate - 获取换手率
提示

使用之前需要下载财务数据(在财务数据下载中)以及日线数据

如果不补充股本数据,将使用最新流通股本计算历史换手率,可能会造成历史换手率不正确

原型

内置python

ContextInfo.get_turnover_rate(stock_list,startTime,endTime)
释义

获取换手率

参数

字段名	数据类型	解释
stock_list	list	股票列表，如['600000.SH','000001.SZ']
startTime	string	起始时间，如'20170101'
endTime	string	结束时间，如'20180101'
返回值

pandas.Dataframe

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_turnover_rate(['000002.SZ'],'20170101','20170301')
	print(data)
ContextInfo.get_longhubang - 获取龙虎榜数据
原型

内置python

ContextInfo.get_longhubang(stock_list, startTime, endTime)
释义

获取龙虎榜数据

参数

参数名称	类型	描述
stock_list	list	股票列表，如 ['600000.SH', '600036.SH']
startTime	str	起始时间，如 '20170101'
endTime	str	结束时间，如 '20180101'
返回值

格式为pandas.DataFrame:
参数名称	数据类型	描述
stockCode	str	股票代码
stockName	str	股票名称
date	datetime	上榜日期
reason	str	上榜原因
close	float	收盘价
SpreadRate	float	涨跌幅
TurnoverVolume	float	成交量
Turnover_Amount	float	成交金额
buyTraderBooth	pandas.DataFrame	买方席位
sellTraderBooth	pandas.DataFrame	卖方席位
buyTraderBooth 或 sellTraderBooth 包含字段：
参数名称	数据类型	描述
traderName	str	交易营业部名称
buyAmount	float	买入金额
buyPercent	float	买入金额占总成交占比
sellAmount	float	卖出金额
sellPercent	float	卖出金额占总成交占比
totalAmount	float	该席位总成交金额
rank	int	席位排行
direction	int	买卖方向
示例

示例返回值

# coding:gbk

def init(C):
    return

def handlebar(C):
    print(C.get_longhubang(['000002.SZ'],'20100101','20180101'))
ContextInfo.get_north_finance_change - 获取对应周期的北向数据
原型

内置python

ContextInfo.get_north_finance_change(period)
释义

获取对应周期的北向数据

参数

字段名	数据类型	描述
period	str	数据周期
返回值

根据period返回一个dict，该字典的key值是北向数据的时间戳，其值仍然是一个dict，其值的key值是北向数据的字段类型，其值是对应字段的值。该字典数据key值有：
字段名	数据类型	描述
hgtNorthBuyMoney	int	HGT北向买入资金
hgtNorthSellMoney	int	HGT北向卖出资金
hgtSouthBuyMoney	int	HGT南向买入资金
hgtSouthSellMoney	int	HGT南向卖出资金
sgtNorthBuyMoney	int	SGT北向买入资金
sgtNorthSellMoney	int	SGT北向卖出资金
sgtSouthBuyMoney	int	SGT南向买入资金
sgtSouthSellMoney	int	SGT南向卖出资金
hgtNorthNetInFlow	int	HGT北向资金净流入
hgtNorthBalanceByDay	int	HGT北向当日资金余额
hgtSouthNetInFlow	int	HGT南向资金净流入
hgtSouthBalanceByDay	int	HGT南向当日资金余额
sgtNorthNetInFlow	int	SGT北向资金净流入
sgtNorthBalanceByDay	int	SGT北向当日资金余额
sgtSouthNetInFlow	int	SGT南向资金净流入
sgtSouthBalanceByDay	int	SGT南向当日资金余额
示例：

示例返回值

# coding = gbk
def init(C):
    return
# 获取市场北向数据
def handlebar(C):
    print(C.get_north_finance_change('1d'))
ContextInfo.get_hkt_details - 获取指定品种的持股明细
原型

内置python

ContextInfo.get_hkt_details(stockcode)
释义

获取指定品种的持股明细

参数

参数名称	数据类型	描述
stockcode	string	必须是'stock.market'形式
返回值

根据stockcode返回一个dict，该字典的key值是北向持股明细数据的时间戳，其值仍然是一个dict，其值的key值是北向持股明细数据的字段类型，其值是对应字段的值，该字典数据key值有：
参数名称	数据类型/单位	描述
stockCode	str	股票代码
ownSharesCompany	str	机构名称
ownSharesAmount	int	持股数量
ownSharesMarketValue	float	持股市值
ownSharesRatio	float	持股数量占比
ownSharesNetBuy	float	净买入金额（当日持股-前一日持股）
示例：

示例返回值

# coding = gbk
def init(C):
    return
def handlebar(C):
    data = C.get_hkt_details('600000.SH')
    print(data)
ContextInfo.get_hkt_statistics - 获取指定品种的持股统计
原型

内置python

ContextInfo.get_hkt_statistics(stockcode)
释义

获取指定品种的持股统计

参数

字段名	数据类型	解释
stockcode	string	必须是'stock.market'形式
返回值

根据stockcode返回一个dict，该字典的key值是北向持股统计数据的时间戳，其值仍然是一个dict，其值的key值是北向持股统计数据的字段类型，其值是对应字段的值，该字典数据key值有：

字段名	数据类型	解释
stockCode	string	股票代码
ownSharesAmount	float	持股数量，单位：股
ownSharesMarketValue	float	持股市值，单位：元
ownSharesRatio	float	持股数量占比，单位：%
ownSharesNetBuy	float	净买入，单位：元，浮点数（当日持股-前一日持股）
示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):

	print(C.get_hkt_statistics('600000.SH'))
get_etf_info - 根据ETF基金代码获取ETF申赎清单及对应成分股数据
原型

内置python

get_etf_info(stockcode)
释义

根据ETF基金代码获取ETF申赎清单及对应成分股数据,每日盘前更新

参数

字段名	数据类型	解释
stockcode	string	ETF基金代码如"510050.SH"
返回值

一个多层嵌套的dict

示例

示例返回值

# coding:gbk
def init(C):
    pass
    
def handlebar(C):
    d = get_etf_info("510050.SH")
    print(d)
get_etf_iopv - 根据ETF基金代码获取ETF的基金份额参考净值
原型

内置python

get_etf_iopv(stockcode)
释义

根据ETF基金代码获取ETF的基金份额参考净值

参数

字段名	数据类型	解释
stockcode	string	ETF基金代码如"510050.SH"
返回值

float类型值,IOPV，基金份额参考净值

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	print(get_etf_iopv("510050.SH"))
ContextInfo.get_local_data - 获取本地行情数据【不推荐】
注意

本函数用于仅用于获取本地历史行情数据，使用前请确保已通过download_history_data下载过历史行情数据

原型

内置python

ContextInfo.get_local_data(
    stock_code,
    start_time='',
    end_time='',
    period='1d',
    divid_type='none',
    count=-1)
释义

获取本地行情数据

参数

字段名	数据类型	解释
stock_code	string	默认参数，合约代码格式为 code.market，不指定时为当前图合约
start_time	string	默认参数，开始时间，格式为 '20171209' 或 '20171209010101'
end_time	string	默认参数，结束时间，格式同 start_time
period	string	默认参数，K线类型，可选值包括：
'tick'：分笔线（只用于获取'quoter'字段数据）、'realtime': 实时线、'1d'：日线
'md'：多日线、'1m'：1分钟线、'3m'：3分钟线
'5m'：5分钟线、'15m'：15分钟线、'30m'：30分钟线
'mm'：多分钟线、'1h'：小时线、'mh'：多小时线
'1w'：周线、'1mon'：月线、'1q'：季线
'1hy'：半年线、'1y'：年线
dividend_type	string	除复权种类，可选值：
'none'：不复权
'front'：向前复权
'back'：向后复权
'front_ratio'：等比向前复权
'back_ratio'：等比向后复权
count	int	当 count 大于等于0时：
如果指定了 start_time 和 end_time，则以 end_time 为基准向前取 count 条数据；
如果 start_time 和 end_time 缺省，则默认取本地数据最新的 count 条数据；
如果 start_time、end_time 和 count 都缺省时，则默认取本地全部数据。
返回值

返回一个dict，键值为timetag，value为另一个dict(valuedict)

period='tick'时函数获取分笔数据，valuedict字典数据key值有：
字段	数据类型	含义
lastPrice	float	最新价
open	float	开盘价
high	float	最高价
low	float	最低价
lastClose	float	前收盘价
amount	float	成交额
volume	float	成交量
pvolume	float	原始成交量
stockStatus	int	作废 参考openInt
openInt	float	若是股票，则openInt含义为股票状态，非股票则是持仓量openInt字段说明
lastSettlementPrice	float	昨结算价
askPrice	list	委卖价
bidPrice	list	委买价
askVol	list	委卖量
bidVol	list	委买量
settlementPrice	float	今结算价
period为其他值时，valuedict字典数据key值有：
字段名	数据类型	解释
amount	float	成交额
volume	float	成交量
open	float	开盘价
high	float	最高价
low	float	最低价
close	float	收盘价
示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_local_data(stock_code='600000.SH',start_time='20220101',end_time='20220131',period='1d',divid_type='none')
	print(data)
ContextInfo.get_history_data - 获取历史行情数据【不推荐】
警告

此函数已不推荐使用，推荐使用ContextInfo.get_market_data_ex()
此函数使用前需要先通过ContextInfo.set_universe()设定股票池
原型

内置python

ContextInfo.get_history_data(
    len, 
    period, 
    field, 
    dividend_type = 0,
    skip_paused = True)
释义

获取历史行情数据

参数

名称	类型	描述
len	int	需获取的历史数据长度
period	string	需获取的历史数据周期，可选值包括：
'tick'：分笔线、 '1d'：日线、 '1m'：1分钟线
'3m'：3分钟线、 '5m'：5分钟线、 '15m'：15分钟线
'30m'：30分钟线、 '1h'：小时线、 '1w'：周线
'1mon'：月线、 '1q'：季线、 '1hy'：半年线
'1y'：年线
field	string	需获取的历史数据的类型，可选值包括：
'open'：开盘价
'high'：最高价
'low'：最低价
'close'：收盘价
'quoter'：详细报价（结构见 get_market_data 方法）
dividend_type	int	默认参数，除复权，默认不复权，可选值包括：
0：不复权
1：向前复权
2：向后复权
3：等比向前复权
4：等比向后复权
skip_paused	bool	默认参数，是否停牌填充，默认填充
返回值 一个字典dict结构，key 为 stockcode.market, value 为行情数据 list，list 中第 0 位为最早的价格，第 1 位为次早价格，依次下去。

示例

示例返回值

# coding = gbk
def init(C):
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]
	C.set_universe(C.stock_list)

def handlebar(C):
	data = C.get_history_data(2, '1d', 'close')
	print(data)

ContextInfo.get_market_data() - 获取行情数据【不推荐】
提示

推荐使用ContextInfo.get_market_data_ex()

原型

内置python

ContextInfo.get_market_data(
    fields, 
    stock_code = [], 
    start_time = '', 
    end_time = '',
    skip_paused = True, 
    period = 'follow', 
    dividend_type = 'follow', 
    count = -1)
释义

获取行情数据

参数

字段名	数据类型	解释
fields	字段列表	可选值包括：
'open': 开
'high': 高
'low': 低
'close': 收
'volume': 成交量
'amount': 成交额
'settle': 结算价
'quoter': 分笔数据（包括历史）
stock_code	默认参数，合约代码列表	合约格式为 code.market，例如 '600000.SH'，不指定时为当前图合约
start_time	默认参数，时间戳	开始时间，格式为 '20171209' 或 '20171209010101'
end_time	默认参数，时间戳	结束时间，格式为 '20171209' 或 '20171209010101'
skip_paused	默认参数，布尔值	如何处理停牌数据：
true：如果是停牌股，会自动填充未停牌前的价格作为停牌日的价格
false：停牌数据为 NaN
period	string	需获取的历史数据周期，可选值包括：
'tick'：分笔线、 '1d'：日线、 '1m'：1分钟线
'3m'：3分钟线、 '5m'：5分钟线、 '15m'：15分钟线
'30m'：30分钟线、 '1h'：小时线、 '1w'：周线
'1mon'：月线、 '1q'：季线、 '1hy'：半年线
'1y'：年线
dividend_type	默认参数，字符串	缺省值为 'none'，除复权，可选值包括：
'none'：不复权
'front'：向前复权
'back'：向后复权
'front_ratio'：等比向前复权
'back_ratio'：等比向后复权
count	默认参数，整数	缺省值为 -1。当大于等于 0 时，效果与 get_history_data 保持一致
count参数设置的几种情况
count 取值	时间设置是否生效	开始时间和结束时间设置效果
count >= 0	生效	返回数量取决于开始时间与结束时间和count与结束时间的交集
count = -1	生效	同时设置开始时间和结束时间，在所设置的时间段内取值
count = -1	生效	开始时间结束时间都不设置，取当前最新bar的值
count = -1	生效	只设置开始时间，取所设开始时间到当前时间的值
count = -1	生效	只设置结束时间，取股票上市第一根 bar 到所设结束时间的值
返回值

返回值根据传入的参数情况，会返回不同类型的结果
count	字段数量	股票数量	时间点	返回类型
=-1	=1	=1	=1	float
=-1	>1	=1	默认值	pandas.Series
>=-1	>=1	=1	>=1	pandas.DataFrame(字段数量和时间点不同时为1)
=-1	>=1	>1	默认值	pandas.DataFrame
>1	=1	=1	=1	pandas.DataFrame
>=-1	>=1	>1	>=1	pandas.Panel
示例

示例data1返回值data2返回值data3返回值data4返回值

# coding = gbk
def init(C):
    C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]
	
def handlebar(C):
    data1 = C.get_market_data(["close"],["000001.SZ"],start_time = "20231106",end_time = "20231106", count = -1) # 返回float值
    data2 = C.get_market_data(["close","open"],["000001.SZ"], count = -1) # 返回pandas.Series
    data3 = C.get_market_data(["close","open"],C.stock_list, count = -1) # 返回pandas.DataFrame
    data4 = C.get_market_data(["open","high", "low", "close"],C.stock_list,count = 20) # 返回pandas.Panel

    print(data1)
    print(data2)
    print(data3)
    print(data4)



#############################
'''
5获取财务数据
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
获取财务数据
获取财务数据前，请先通过界面端数据管理 - 财务数据下载

财务数据下载

提示

财务数据接口通过读取下载本地的数据取数，使用前需要补充本地数据。除公告日期和报表截止日期为时间戳毫秒格式其他单位为元或 %，数据主要包括资产负债表(ASHAREBALANCESHEET)、利润表（ASHAREINCOME）、现金流量表（ASHARECASHFLOW）、股本表（CAPITALSTRUCTURE）的主要字段数据以及经过计算的主要财务指标数据（PERSHAREINDEX）。建议使用本文档对照表中的英文表名和迅投英文字段，表名不区分大小写。

ContextInfo.get_financial_data - 获取财务数据
财务数据接口有两种用法，入参和返回值不同，具体如下

用法1
原型

内置python

ContextInfo.get_financial_data(fieldList, stockList, startDate, enDate, report_type = 'announce_time')
释义

获取财务数据，方法1

参数

字段名	类型	释义与用例
fieldList	List（必须）	财报字段列表：['ASHAREBALANCESHEET.fix_assets', '利润表.净利润']
stockList	List（必须）	股票列表：['600000.SH', '000001.SZ']
startDate	Str（必须）	开始时间：'20171209'
endDate	Str（必须）	结束时间：'20171212'
report_type	Str（可选）	报表时间类型，可缺省，默认是按照数据的公告期为区分取数据，设置为 'report_time' 为按照报告期取数据，' announce_time' 为按照公告日期取数据
提示

选择按照公告期取数和按照报告期取数的区别：

报告日期是指财务报告所覆盖的会计时间段，而公告日期是指公司向外界公布该报告的具体时间点

若指定report_type为report_time，则不会考虑财报的公告日期，可能会取到未来数据

若指定report_type为announce_time，则会按财报实际发布日期返回数据，不会取到未来数据

例：

返回值

函数根据stockList代码列表,startDate,endDate时间范围，返回不同的的数据类型。如下：

代码数量	时间范围	返回类型
=1	=1	pandas.Series (index = 字段)
=1	>1	pandas.DataFrame (index = 时间, columns = 字段)
>1	=1	pandas.DataFrame (index = 代码, columns = 字段)
>1	>1	pandas.Panel (items = 代码, major_axis = 时间, minor_axis = 字段)
示例

示例返回值

# coding:gbk
def init(C):
  pass

def handlebar(C):

  #取总股本和净利润
  fieldList = ['CAPITALSTRUCTURE.total_capital', '利润表.净利润']   
  stockList = ["000001.SZ","000002.SZ","430017.BJ"]
  startDate = '20171209'
  endDate = '20231204'
  data = C.get_financial_data(fieldList, stockList, startDate, endDate, report_type = 'report_time')
  print(data)
用法2
原型

内置python

ContextInfo.get_financial_data(tabname, colname, market, code, report_type = 'report_time', barpos)
与用法 1 可同时使用

释义

获取财务数据，方法2

参数

字段名	类型	释义与用例
tabname	Str（必须）	表名：'ASHAREBALANCESHEET'
colname	Str（必须）	字段名：'fix_assets'
market	Str（必须）	市场：'SH'
code	Str（必须）	代码：'600000'
report_type	Str（可选）	报表时间类型，可缺省，默认是按照数据的公告期为区分取数据，设置为 'report_time' 为按照报告期取数据，' announce_time ' 为按照公告日期取数据
barpos	number	当前 bar 的索引
返回值

float ：所取字段的数值

示例

示例返回值

# coding:gbk
def init(C):
  pass
	
def handlebar(C):
  index = C.barpos
  data = C.get_financial_data('ASHAREBALANCESHEET', 'fix_assets', 'SH', '600000', index)
  print(data)
ContextInfo.get_raw_financial_data - 获取原始财务数据
提示

取原始财务数据,与get_financial_data相比不填充每个交易日的数据

原型

内置python

ContextInfo.get_raw_financial_data(fieldList,stockList,startDate,endDate,report_type='announce_time')

释义

取原始财务数据,与get_financial_data相比不填充每个交易日的数据

参数

字段名	类型	释义与用例
fieldList	List（必须）	字段列表：例如 ['资产负债表.固定资产','利润表.净利润']
stockList	List（必须）	股票列表：例如['600000.SH','000001.SZ']
startDate	Str（必须）	开始时间：例如 '20171209'
endDate	Str（必须）	结束时间：例如 '20171212'
report_type	Str（可选）	时间类型，可缺省，默认是按照数据的公告期为区分取数据，设置为 'report_time' 为按照报告期取数据，可选值:'announce_time','report_time'
返回值

函数根据stockList代码列表,startDate,endDate时间范围，返回不同的的数据类型。如下：

代码数量	时间范围	返回类型
=1	=1	pandas.Series (index = 字段)
=1	>1	pandas.DataFrame (index = 时间, columns = 字段)
>1	=1	pandas.DataFrame (index = 代码, columns = 字段)
>1	>1	pandas.Panel (items = 代码, major_axis = 时间, minor_axis = 字段)
示例

示例返回值

#encoding:gbk
'''
获取财务数据
'''
import pandas as pd
import numpy as np
import talib

def to_zw(a):
	'''0.中文价格字符串'''
	import numpy as np
	try:
		header = '' if a > 0 else '-'
		if np.isnan(a):
			return '问题数据'
		if abs(a) < 1000:
			return header + str(int(a)) + "元"
		if abs(a) < 10000:
			return header + str(int(a))[0] + "千"
		if abs(a) < 100000000:
			return header + str(int(a))[:-4] + "万" + str(int(a))[-4] + '千'
		else:
			return header + str(int(a))[:-8] + "亿" + str(int(a))[-8:-4] + '万'
	except:
		print(f"问题数据{a}")
		return '问题数据'


def after_init(C):
	fieldList = ['ASHAREINCOME.net_profit_excl_min_int_inc','ASHAREINCOME.revenue'] # 字段表
	stockList = ['000001.SZ'] # 标的
	a=C.get_raw_financial_data(fieldList,stockList,'20150101','20300101',report_type = 'report_time') # 获取原始财务数据
	# print(a)
	for stock in a:
		for key in a[stock]:
			for t in a[stock][key]:
				print(key, timetag_to_datetime(int(t),'%Y%m%d'), to_zw(a[stock][key][t]))
			print('-' *22)
		print('-' *22)

ContextInfo.get_last_volume - 获取最新流通股本
原型

内置python

ContextInfo.get_last_volume(stockcode)
释义

获取最新流通股本

参数

字段名	数据类型	解释
stockcode	string	标的名称，必须是 'stock.market' 形式
返回值

int类型值,代表流通股本数量

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_last_volume("000001.SZ")
	print(data)
ContextInfo.get_total_share - 获取总股数
原型

内置python

ContextInfo.get_total_share(stockcode)
释义

获取总股数

参数

字段名	数据类型	解释
stockcode	string	股票代码，缺省值 ''，默认为当前图代码, 如：'600000.SH'
返回值

int:总股数

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_total_share('600000.SH')
	print(data)
财务数据字段表
资产负债表 (ASHAREBALANCESHEET)
中文字段	迅投字段
应收利息	int_rcv
可供出售金融资产	fin_assets_avail_for_sale
持有至到期投资	held_to_mty_invest
长期股权投资	long_term_eqy_invest
固定资产	fix_assets
无形资产	intang_assets
递延所得税资产	deferred_tax_assets
资产总计	tot_assets
交易性金融负债	tradable_fin_liab
应付职工薪酬	empl_ben_payable
应交税费	taxes_surcharges_payable
应付利息	int_payable
应付债券	bonds_payable
递延所得税负债	deferred_tax_liab
负债合计	tot_liab
实收资本(或股本)	cap_stk
资本公积金	cap_rsrv
盈余公积金	surplus_rsrv
未分配利润	undistributed_profit
归属于母公司股东权益合计	tot_shrhldr_eqy_excl_min_int
少数股东权益	minority_int
负债和股东权益总计	tot_liab_shrhldr_eqy
所有者权益合计	total_equity
货币资金	cash_equivalents
应收票据	bill_receivable
应收账款	account_receivable
预付账款	advance_payment
其他应收款	other_receivable
其他流动资产	other_current_assets
流动资产合计	total_current_assets
存货	inventories
在建工程	constru_in_process
工程物资	construction_materials
长期待摊费用	long_deferred_expense
非流动资产合计	total_non_current_assets
短期借款	shortterm_loan
应付股利	dividend_payable
其他应付款	other_payable
一年内到期的非流动负债	non_current_liability_in_one_year
其他流动负债	other_current_liability
长期应付款	longterm_account_payable
应付账款	accounts_payable
预收账款	advance_peceipts
流动负债合计	total_current_liability
应付票据	notes_payable
长期借款	long_term_loans
专项应付款	grants_received
其他非流动负债	other_non_current_liabilities
非流动负债合计	non_current_liabilities
专项储备	specific_reserves
商誉	goodwill
报告截止日	m_timetag
公告日	m_anntime
利润表 (ASHAREINCOME)
中文字段	迅投字段
投资收益	plus_net_invest_inc
联营企业和合营企业的投资收益	incl_inc_invest_assoc_jv_entp
营业税金及附加	less_taxes_surcharges_ops
营业总收入	revenue
营业总成本	total_operating_cost
营业收入	revenue_inc
营业成本	total_expense
资产减值损失	less_impair_loss_assets
营业利润	oper_profit
营业外收入	plus_non_oper_rev
营业外支出	less_non_oper_exp
利润总额	tot_profit
所得税	inc_tax
净利润	net_profit_incl_min_int_inc
归母净利润	net_profit_excl_min_int_inc
管理费用	less_gerl_admin_exp
销售费用	sale_expense
财务费用	financial_expense
综合收益总额	total_income
归属于少数股东的综合收益总额	total_income_minority
公允价值变动收益	change_income_fair_value
已赚保费	earned_premium
报告截止日	m_timetag
公告日	m_anntime
现金流量表 (ASHARECASHFLOW)
中文字段	迅投字段
收到其他与经营活动有关的现金	other_cash_recp_ral_oper_act
经营活动现金流入小计	stot_cash_inflows_oper_act
支付给职工以及为职工支付的现金	cash_pay_beh_empl
支付的各项税费	pay_all_typ_tax
支付其他与经营活动有关的现金	other_cash_pay_ral_oper_act
经营活动现金流出小计	stot_cash_outflows_oper_act
经营活动产生的现金流量净额	net_cash_flows_oper_act
取得投资收益所收到的现金	cash_recp_return_invest
处置固定资产、无形资产和其他长期投资收到的现金	net_cash_recp_disp_fiolta
投资活动现金流入小计	stot_cash_inflows_inv_act
投资支付的现金	cash_paid_invest
购建固定资产、无形资产和其他长期投资支付的现金	cash_pay_acq_const_fiolta
支付其他与投资的现金	other_cash_pay_ral_inv_act
投资活动产生的现金流出小计	stot_cash_outflows_inv_act
投资活动产生的现金流量净额	net_cash_flows_inv_act
吸收投资收到的现金	cash_recp_cap_contrib
取得借款收到的现金	cash_recp_borrow
收到其他与筹资活动有关的现金	other_cash_recp_ral_fnc_act
筹资活动现金流入小计	stot_cash_inflows_fnc_act
偿还债务支付现金	cash_prepay_amt_borr
分配股利、利润或偿付利息支付的现金	cash_pay_dist_dpcp_int_exp
支付其他与筹资的现金	other_cash_pay_ral_fnc_act
筹资活动现金流出小计	stot_cash_outflows_fnc_act
筹资活动产生的现金流量净额	net_cash_flows_fnc_act
汇率变动对现金的影响	eff_fx_flu_cash
现金及现金等价物净增加额	net_incr_cash_cash_equ
销售商品、提供劳务收到的现金	goods_sale_and_service_render_cash
收到的税费与返还	tax_levy_refund
购买商品、接受劳务支付的现金	goods_and_services_cash_paid
处置子公司及其他收到的现金	net_cash_deal_subcompany
其中子公司吸收现金	cash_from_mino_s_invest_sub
处置固定资产、无形资产和其他长期资产支付的现金净额	fix_intan_other_asset_dispo_cash_payment
报告截止日	m_timetag
公告日	m_anntime
股本表 (CAPITALSTRUCTURE)
中文字段	迅投字段
总股本	total_capital
已上市流通A股	circulating_capital
自由流通股本	free_float_capital（旧版本为freeFloatCapital）
限售流通股份	restrict_circulating_capital
变动日期	m_timetag
公告日	m_anntime
主要指标 (PERSHAREINDEX)
中文字段	迅投字段
每股经营活动现金流量	s_fa_ocfps
每股净资产	s_fa_bps
基本每股收益	s_fa_eps_basic
稀释每股收益	s_fa_eps_diluted
每股未分配利润	s_fa_undistributedps
每股资本公积金	s_fa_surpluscapitalps
扣非每股收益	adjusted_earnings_per_share
净资产收益率	du_return_on_equity
销售毛利率	sales_gross_profit
主营收入同比增长	inc_revenue_rate
净利润同比增长	du_profit_rate
归属于母公司所有者的净利润同比增长	inc_net_profit_rate
扣非净利润同比增长	adjusted_net_profit_rate
营业总收入滚动环比增长	inc_total_revenue_annual
归属净利润滚动环比增长	inc_net_profit_to_shareholders_annual
扣非净利润滚动环比增长	adjusted_profit_to_profit_annual
加权净资产收益率	equity_roe
摊薄净资产收益率	net_roe
摊薄总资产收益率	total_roe
毛利率	gross_profit
净利率	net_profit
实际税率	actual_tax_rate
预收款营业收入	pre_pay_operate_income
销售现金流营业收入	sales_cash_flow
资产负债比率	gear_ratio
存货周转率	inventory_turnover
十大股东/十大流通股东 (TOP10HOLDER/TOP10FLOWHOLDER)
提示

对于公告内披露的十大股东数量大于10条的，我们会保留原始数据，以保持和公司公告信息一致

中文字段	迅投字段
公告日期	declareDate
截止日期	endDate
股东名称	name
股东类型	type
持股数量	quantity
变动原因	reason
持股比例	ratio
股份性质	nature
持股排名	rank
股东数 (SHAREHOLDER)
中文字段	迅投字段
公告日期	declareDate
截止日期	endDate
股东总数	shareholder
A股东户数	shareholderA
B股东户数	shareholderB
H股东户数	shareholderH
已流通股东户数	shareholderFloat
未流通股东户数	shareholderOther
#########################################
'''
6获取合约信息
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
获取合约信息
ContextInfo.get_instrument_detail - 根据代码获取合约详细信息
提示

旧版本客户端中，函数名为ContextInfo.get_instrumentdetail；不支持iscomplete参数

原型

内置python


ContextInfo.get_instrument_detail(stockcode,iscomplete = Fasle)

释义

根据代码获取合约详细信息

参数

字段名	数据类型	解释
stockcode	string	标的名称，必须是 'stock.market' 形式
iscomplete	bool	是否获取全部字段，默认为False
返回值

根据stockcode返回一个dict。该字典数据key值有：

名称	类型	描述
ExchangeID	string	合约市场代码
InstrumentID	string	合约代码
InstrumentName	string	合约名称
ProductID	string	合约的品种ID(期货)
ProductName	string	合约的品种名称(期货)
ProductType	int	合约的类型, 默认-1,枚举值可参考下方说明
ExchangeCode	string	交易所代码
UniCode	string	统一规则代码
CreateDate	str	创建日期
OpenDate	str	上市日期（特殊值情况见表末）
ExpireDate	int	退市日或者到期日（特殊值情况见表末）
PreClose	float	前收盘价格
SettlementPrice	float	前结算价格
UpStopPrice	float	当日涨停价
DownStopPrice	float	当日跌停价
FloatVolume	float	流通股本（单位：股。注意，部分低等级客户端中此字段为FloatVolumn）
TotalVolume	float	总股本（单位：股。注意，部分低等级客户端中此字段为FloatVolumn）
LongMarginRatio	float	多头保证金率
ShortMarginRatio	float	空头保证金率
PriceTick	float	最小价格变动单位
VolumeMultiple	int	合约乘数(对期货以外的品种，默认是1)
MainContract	int	主力合约标记，1、2、3分别表示第一主力合约，第二主力合约，第三主力合约
LastVolume	int	昨日持仓量
InstrumentStatus	int	合约停牌状态(<=0:正常交易（-1:复牌）;>=1停牌天数;)
IsTrading	bool	合约是否可交易
IsRecent	bool	是否是近月合约
ChargeType	int	期货和期权手续费方式
ChargeOpen	float	开仓手续费(率)
ChargeClose	float	平仓手续费(率)
ChargeTodayOpen	float	开今仓(日内开仓)手续费(率)
ChargeTodayClose	float	平今仓(日内平仓)手续费(率)
OptionType	int	期权类型
OpenInterestMultiple	int	交割月持仓倍数
提示

字段OpenDate有以下几种特殊值： 19700101=新股, 19700102=老股东增发, 19700103=新债, 19700104=可转债, 19700105=配股， 19700106=配号 字段ExpireDate为0 或 99999999 时，表示该标的暂无退市日或到期日

字段ProductType 对于股票以外的品种，有以下几种值

国内期货市场： 1-期货 2-期权(DF SF ZF INE GF) 3-组合套利 4-即期 5-期转现 6-期权(IF) 7-结算价交易(tas)

**沪深股票期权市场：**0-认购 1-认沽

外盘： 1-100：期货， 101-200：现货, 201-300:股票相关 1：股指期货 2：能源期货 3：农业期货 4：金属期货 5：利率期货 6：汇率期货 7：数字货币期货 99：自定义合约期货 107：数字货币现货 201：股票 202：GDR 203：ETF 204：ETN 300：其他

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_instrumentdetail("000001.SZ")
	print(data)
get_st_status - 获取历史st状态
提示

本函数需要下载历史ST数据(过期合约K线),可通过界面端数据管理 - 过期合约数据下载

原型

内置python

get_st_status(stockcode)
释义

获取历史st状态

参数

字段名	数据类型	解释
stockcode	string	股票代码，如000004.SZ（可为空，为空时取主图代码）
返回值

st范围字典 格式 {'ST': [['20210520', '20380119']], '*ST': [['20070427', '20080618'], ['20200611', '20210520']]}

示例：

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	print(get_st_status('600599.SH'))
ContextInfo.get_his_st_data - 获取某只股票ST的历史
提示

本函数需要下载历史ST数据(过期合约K线),可通过界面端数据管理 - 过期合约数据下载

原型

内置python

ContextInfo.get_his_st_data(stockcode)
释义

获取某只股票ST的历史

参数

字段名	数据类型	解释
stockcode	string	股票代码，'stkcode.market'，如'000004.SZ'
返回值

dict,st历史，key为ST,*ST,PT,历史未ST会返回{}

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	print(C.get_his_st_data('000004.SZ'))
ContextInfo.get_main_contract - 获取期货主力合约
提示

该函数支持实盘/回测两种模式
若要使用该函数获取历史主力合约，必须要先下载历史主力合约数据
历史主力合约数据目前通过界面端数据管理 - 过期合约数据 - 历史主力合约下载
原型

内置python

ContextInfo.get_main_contract(codemarket)
ContextInfo.get_main_contract(codemarket,date="")
ContextInfo.get_main_contract(codemarket,startDate="",endDate="")
释义

获取当前期货主力合约

参数

字段名	数据类型	解释
codemarket	string	合约和市场，合约格式为品种名加00，如IF00.IF，zn00.SF
startDate	string	开始日期(可以不写),如20180608
endDate	string	结束日期(可以不写),如20190608
返回值

str，合约代码

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	symbol1 = C.get_main_contract('IF00.IF')# 获取当前主力合约

	symbol2 = C.get_main_contract('IF00.IF',"20190101")# 获取指定日期主力合约

	symbol3 = C.get_main_contract('IF00.IF',"20181101","20190101") # 获取时间段内全部主力合约

	print(symbol1, symbol2)
	print("="*10)
	print(symbol3)
ContextInfo.get_contract_multiplier - 获取合约乘数
原型

内置python

ContextInfo.get_contract_multiplier(contractcode)
释义

获取合约乘数

参数

字段名	数据类型	解释
contractcode	string	合约代码，格式为 'code.market'，例如 'IF1707.IF'
返回值int,表示合约乘数

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	multiplier = C.get_contract_multiplier("rb2401.SF")
	print(multiplier)
ContextInfo.get_contract_expire_date - 获取期货合约到期日
原型

内置python

ContextInfo.get_contract_expire_date(codemarket)
释义

获取期货合约到期日

参数

字段名	数据类型	解释
Codemarket	string	合约和市场,如IF00.IF,zn00.SF
返回值str，合约到期日

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_contract_expire_date("IF2311.IF")
	# print(type(data))
	print(data)
ContextInfo.get_his_contract_list - 获取市场已退市合约
原型

内置python

ContextInfo.get_his_contract_list(market)
释义

获取市场已退市合约，需要手动补充过期合约列表

参数

字段名	数据类型	解释
market	string	市场,SH,SZ,SHO,SZO,IF等
返回值

list,合约代码列表

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):

	print(C.get_his_contract_list('SHO')[:30])

##############################
'''
7获取期权信息
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
获取期权信息
ContextInfo.get_option_detail_data - 获取指定期权品种的详细信息
原型

内置python

ContextInfo.get_option_detail_data(optioncode)
释义

获取指定期权品种的详细信息

参数

字段名	数据类型	解释
optioncode	string	期权代码,如'10001506.SHO',当填写空字符串时候默认为当前主图的期权品种
返回值dict,字段如下：

字段	类型	说明
ExchangeID	str	期权市场代码
InstrumentID	str	期权代码
ProductID	str	期权标的的产品ID
OpenDate	int	发行日期
ExpireDate	int	到期日
PreClose	float	前收价格
SettlementPrice	float	前结算价格
UpStopPrice	float	当日涨停价
DownStopPrice	float	当日跌停价
LongMarginRatio	float	多头保证金率
ShortMarginRatio	float	空头保证金率
PriceTick	float	最小变价单位
VolumeMultiple	int	合约乘数
MaxMarketOrderVolume	int	涨跌停价最大下单量
MinMarketOrderVolume	int	涨跌停价最小下单量
MaxLimitOrderVolume	int	限价单最大下单量
MinLimitOrderVolume	int	限价单最小下单量
OptUnit	int	期权合约单位
MarginUnit	float	期权单位保证金
OptUndlCode	str	期权标的证券代码
OptUndlMarket	str	期权标的证券市场
OptExercisePrice	float	期权行权价
NeeqExeType	str	全国股转转让类型
OptUndlRiskFreeRate	float	期权标的无风险利率
OptUndlHistoryRate	float	期权标的历史波动率
EndDelivDate	int	期权行权终止日
optType	str	期权类型
示例

示例返回值

#encoding:gbk
def init(ContextInfo):
  pass

def after_init(ContextInfo):
  print(ContextInfo.get_option_detail_data('10002235.SHO'))
ContextInfo.get_option_list - 获取指定期权列表
原型

内置python

ContextInfo.get_option_list(undl_code,dedate,opttype,isavailable)
释义

获取指定期权列表。如获取历史期权，需先下载过期合约列表

参数

字段名	数据类型	解释
undl_code	string	期权标的代码,如'510300.SH'
dedate	string	期权到期月或当前交易日期，"YYYYMM"格式为期权到期月，"YYYYMMDD"格式为获取当前日期交易的期权
opttype	string	期权类型，默认值为空，"CALL"，"PUT"，为空时认购认沽都取
isavailable	bool	是否可交易，当dedate的格式为"YYYYMMDD"格式为获取当前日期交易的期权时，isavailable为True时返回当前可用，为False时返回当前和历史可用
返回值

list，期权合约列表

示例

示例data1返回值data2返回值data3返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	# 获取到期月份为202101的上交所510300ETF认购合约
	data1=C.get_option_list('510300.SH','202101',"CALL")

	# 获取20210104当天上交所510300ETF可交易的认购合约
	data2=C.get_option_list('510300.SH','20210104',"CALL",True)

	# 获取20210104当天上交所510300ETF已经上市的认购合约(包括退市)
	data3=C.get_option_list('510300.SH','20210104',"CALL",False)
ContextInfo.get_option_undl_data - 获取指定期权标的对应的期权品种列表
原型

内置python

ContextInfo.get_option_undl_data(undl_code_ref)
释义

获取指定期权标的对应的期权品种列表

参数

字段名	数据类型	解释
undl_code_ref	string	期权标的代码,如'510300.SH'，传空字符串时获取全部标的数据
返回值

指定期权标的代码时返回对应该标的的期权合约列表list

期权标的代码为空字符串时返回全部标的对应的品种列表的字典dict

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):

	print(C.get_option_undl_data('510300.SH')[:30])
ContextInfo.bsm_price - 基于BS模型计算欧式期权理论价格
原型

内置python

ContextInfo.bsm_price(optionType,objectPrices,strikePrice,riskFree,sigma,days,dividend)
释义

基于Black-Scholes-Merton模型，输入期权标的价格、期权行权价、无风险利率、期权标的年化波动率、剩余天数、标的分红率、计算期权的理论价格

参数

字段	类型	说明
optionType	str	期权类型，认购：'C'，认沽：'P'
objectPrices	float	期权标的价格，可以是价格列表或者单个价格
strikePrice	float	期权行权价
riskFree	float	无风险收益率
sigma	float	标的波动率
days	int	剩余天数
dividend	float	分红率
返回

提示

objectPrices为float时，返回float
objectPrices为list时，返回list
计算结果最小值0.0001，结果保留4位小数,输入非法参数返回nan
示例返回值

#encoding:gbk
import numpy as np


def init(ContextInfo):
  pass

def after_init(ContextInfo):
  object_prices=list(np.arange(3,4,0.01));
  #计算剩余15天的行权价3.5的认购期权,在无风险利率3%,分红率为0,标的年化波动率为23%时标的价格从3元到4元变动过程中期权理论价格序列
  prices=ContextInfo.bsm_price('C',object_prices,3.5,0.03,0.23,15,0)
  print(prices)
  #计算剩余15天的行权价3.5的认购期权,在无风险利率3%,分红率为0,标的年化波动率为23%时标的价格为3.51元的平值期权的理论价格
  price=ContextInfo.bsm_price('C',3.51,3.5,0.03,0.23,15,0)
  print(price)

ContextInfo.bsm_iv - 基于BS模型计算欧式期权隐含波动率
原型

内置python

ContextInfo.bsm_iv(optionType,objectPrices,strikePrice,optionPrice,riskFree,days,dividend)

释义 基于Black-Scholes-Merton模型,输入期权标的价格、期权行权价、期权现价、无风险利率、剩余天数、标的分红率,计算期权的隐含波动率

参数

字段	类型	说明
optionType	str	期权类型，认购：'C'，认沽：'P'
objectPrices	float	期权标的价格，可以是价格列表或者单个价格
strikePrice	float	期权行权价
riskFree	float	无风险收益率
sigma	float	标的波动率
days	int	剩余天数
dividend	float	分红率
返回

double

示例返回值

#encoding:gbk
import numpy as np

def init(ContextInfo):
    pass

def after_init(ContextInfo):
    # 计算剩余15天的行权价3.5的认购期权,在无风险利率3%,分红率为0时,标的现价3.51元,期权价格0.0725元时的隐含波动率
    iv=ContextInfo.bsm_iv('C',3.51,3.5,0.0725,0.03,15)
    print(iv)
##############################
'''
8其他信息函数
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
获取除复权信息
ContextInfo.get_divid_factors - 获取除权除息日和复权因子
原型

内置python

ContextInfo.get_divid_factors(stock.market)
释义

获取除权除息日和复权因子

参数

字段名	数据类型	解释
stock.market	string	股票代码.市场代码，如 '600000.SH'
返回值

dict

key:时间戳，

value:list[每股红利,每股送转,每股转赠,配股,配股价,是否股改,复权系数]

输入除权除息日非法时候返回空dict，合法时返回输入日期的对应的dict，不输入时返回查询股票的所有除权除息日及对应dict

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	Result = C.get_divid_factors('600000.SH')
	print(Result)
获取指数权重
ContextInfo.get_weight_in_index - 获取某只股票在某指数中的绝对权重
原型

内置python

ContextInfo.get_weight_in_index(indexcode, stockcode)
释义

获取某只股票在某指数中的绝对权重

参数

字段名	数据类型	解释
indexcode	string	指数代码，格式为 'stockcode.market'，例如 '000300.SH'
stockcode	string	股票代码，格式为 'stockcode.market'，例如 '600004.SH'
返回值

float：返回的数值单位是 %，如 1.6134 表示权重是 1.6134%

示例

示例返回值

# coding:gbk
def init(C):
	pass
	
def handlebar(C):
	data = C.get_weight_in_index('000300.SH', '000002.SZ')
	print(data)
获取成分股信息
ContextInfo.get_stock_list_in_sector - 获取板块成份股
原型

内置python

ContextInfo.get_stock_list_in_sector(sectorname, realtime)
释义

获取板块成份股，支持客户端左侧板块列表中任意的板块，包括自定义板块

参数

字段名	数据类型	解释
sectorname	string	板块名，如 '沪深300'，'中证500'，'上证50'，'我的自选'等
realtime	毫秒级时间戳	实时数据的毫秒级时间戳
返回值

list：内含成份股代码，代码形式为 'stockcode.market'，如 '000002.SZ'

示例

示例返回值

# coding:gbk
def init(C):
	pass
def handlebar(C):
	print(C.get_stock_list_in_sector('上证50'))
获取交易日信息
注意

该函数只能在after_init;handlebar运行
ContextInfo.get_trading_dates - 获取交易日信息
原型

内置python

ContextInfo.get_trading_dates(stockcode,start_date,end_date,count,period='1d')
释义

ContextInfo.get_trading_dates(stockcode,start_date,end_date,count,period='1d')

参数

字段名	数据类型	解释
stockcode	string	股票代码,缺省值''默认为当前图代码，如:'600000.SH'
start_date	string	开始时间，缺省值''为空时不使用，如:'20170101','20170101000000'
end_date	string	结束时间，缺省值''默认为当前bar的时间，如:'20170102','20170102000000'
count	int	K线个数，必须大于0，取包括end_date往前的count个K线，但最早不会早于start_date
period	string	k线类型,'1d':日线,'1m':分钟线,'3m':三分钟线,'5m':5分钟线,'15m':15分钟线,'30m':30分钟线,'1h':小时线,'1w':周线,'1mon':月线,'1q':季线,'1hy':半年线,'1y':年线
返回值

list:K线周期（交易日）列表 period为日线时返回如['20170101','20170102',...]样式 其它返回如['20170101010000','20170102020000',...]样式

示例

示例返回值

# coding:gbk
def init(C):
	pass
def after_init(C):
    print(C.get_trading_dates('600000.SH','','',30,'1d'))
def handlebar(C):
	pass
###############################
'''
9交易下单函数
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
交易下单函数
passorder - 综合下单函数
综合下单函数，用于股票、期货、期权等下单和新股、新债申购、融资融券等交易操作推荐使用

提示

推荐使用
可覆盖多品种下单
注意参数的变化
调用方法：

python示例

passorder(
    opType, orderType, accountid
    , orderCode, prType, price, volume
    , strategyName, quickTrade, userOrderId
    , ContextInfo
)
'''
passorder(
    2 #opType 操作号
    , 1101 #orderType 组合方式
    , '1000044' #accountid 资金账号
    , 'cu2403.SF' #orderCode 品种代码
    , 14 #prType 报价类型
    , 0.0 #price 价格
    , 2 #volume 下单量
    , '示例下单' #strategyName 策略名称
    , 1 #quickTrade 快速下单标记
    , '投资备注' #userOrderId 投资备注
    , C #ContextInfo 策略上下文
)
'''
参数：

参数名	类型	说明	提示
opType	int	交易类型	可选买、买，期货开仓、平仓等

可选值参考opType-操作类型
orderType	int	

下单方式	可选值参考orderType-下单方式

可选按股票数量买卖或按照金额等方式买卖

一、期货不支持 1102 和 1202;

二、对所有账号组的操作相当于对账号组里的每个账号做一样的操作，如 passorder (23, 1202, 'testS', '000001. SZ', 5, -1, 50000, ContextInfo)，意思就是对账号组 testS 里的所有账号都以最新价开仓买入 50000 元市值的 000001.SZ 平安银行；passorder (60,1101,"test",'510050. SH', 5,-1,1, ContextInfo)意思就是账号test申购 1 个单位 (900000股)的华夏上证50ETF (只申购不买入成分股)。

accountID	string	资金账号	下单的账号ID（可多个）或账号组名或套利组名（一个篮子一个套利账号，如 accountID = '股票账户名, 期货账号'）
orderCode	string	下单代码	1. 如果是单股或单期货、港股，则该参数填合约代码；
2. 如果是组合交易, 则该参数填篮子名称，参考组合交易；
3. 如果是组合套利，则填一个篮子名和一个期货合约名（如orderCode = '篮子名, 期货合约名'），请参考组合套利交易

prType	int	下单选价类型	可选值参考prType-下单选价类型

特别的对于套利，这个 prType 只对篮子起作用，期货的采用默认的方式）
price	float	下单价格	一、单股下单时，prType 是模型价/科创板盘后定价时 price 有效；其它情况无效；

1.1 即单股时， prType 参数为 11，49 时被使用。

1.2 prType 参数不为 11，49 时也需填写，填写的内容可为 -1，0，2，100 等任意数字；

二、组合下单时，是组合套利时，price 作套利比例有效，其它情况无效。
volume	int	下单数量（股 / 手 / 元 / %）	根据 orderType 值最后一位确定 volume 的单位，可选值参考volume - 下单
strategyName	string	自定义策略名	

一、用来区分 order 委托和deal 成交来自不同的策略。

根据该策略名，get_trade_detail_data，get_last_order_id 函数可以获取相应策略名对应的委托或成交集合。

strategyName 只对同账号本地客户端有效，即 strategyName 只对当前客户端下的单进行策略区分，且该策略区分只能当前客户端使用。

quickTrade	int	设定是否立即触发下单	

可选值参考quicktrade - 快速下单

passorder是对最后一根K线完全走完后生成的模型信号在下一根K线的第一个tick数据来时触发下单交易；

采用quickTrade参数设置为1时，非历史bar上执行时（ContextInfo.is_last_bar()为True），只要策略模型中调用到就触发下单交易。

quickTrade参数设置为2时，不判断bar状态，只要策略模型中调用到就触发下单交易，历史bar上也能触发下单，请谨慎使用。
userOrderId	string	用户自设委托 ID	如果传入该参数，
则 strategyName 和 quickTrade 参数也填写。
对应 order 委托对象和 deal 成交对象中的 m_strRemark 属性，通过 get_trade_detail_data 函数或委托主推函数 order_callback 和成交主推函数 deal_callback 可拿到这两个对象信息。
ContextInfo	class	系统参数	含有k线信息和接口的上下文对象
返回：

无

更多示例：

股票
基金
两融
期货
期权
新股申购
债券
ETF
组合交易
组合套利交易
algo_passorder - 算法下单（拆单）函数
用于按固定时间间隔和固定规则把目标交易数量拆分成多次下单的交易函数

调用用法：

python

algo_passorder(opType,orderType,accountid,orderCode,prType,price,volume,[strategyName,quickTrade,userOrderId,userOrderParam],ContextInfo)`
提示

算法交易下单，此时使用交易面板-程序交易-函数交易-函数交易参数中设置的下单类型(普通交易,算法交易,随机量交易) 如果函数交易参数使用未修改的默认值,此函数和passorder函数一致， 设置了函数交易参数后，将会使用函数交易参数的超价等拆单参数，algo_passorder内的prType若赋值,则优先使用该参数，若algo_passorder内的prType=-1,将会使用userOrderParam内的opType，若userOrderParam未赋值，则使用界面上的函数交易参数的报价方式

参数：
其他参数同passorder，详细解释可参考passorder的说明
userOrderParam dict[str:value] 是用户自定义交易参数,主要用于修改算法交易的参数 其中Key Value定义如下

注：所有参数均为非必选

Key	Value类型	Value
OrderType	int	普通交易:0
算法交易:1
随机量交易:2
PriceType	int	报价方式:数值同passorde prType
MaxOrderCount	int	最大下单次数
SinglePriceRange	int	波动区间是否单向:
否:0，
是:1
PriceRangeType	int	波动区间类型按比例:0,按数值1
PriceRangeValue	float	波动区间(按数值)
PriceRangeRate	float	波动区间(按比例)[0-1]
SuperPriceType	int	单笔超价类型:
按比例:0
按数值1
SuperPriceRate	float	单笔超价(按比例)[0-1]
SuperPriceValue	float	单笔超价(按数值)
VolumeType	int	单笔基准量类型卖1+2+3+4+5量:0
卖1+2+3+4量:1
...
卖1量:4
买1量:5
...
买1+2+3+4+5量:9
目标量:10
目标剩余量:11
持仓数量:12
VolumeRate	float	单笔下单比率[0-1]
SingleNumMin	float	单笔下单量最小值
SingleNumMax	float	单笔下单量最大值
ValidTimeType	int	有效时间类型:
0:按持续时间
1 按时间区间，默认为0
ValidTimeElapse	int	有效持续时间,ValidTimeType设置为0时生效
ValidTimeStart	int	有效开始时间偏移,ValidTimeType设置为1时生效
ValidTimeEnd	int	有效结束时间偏移,ValidTimeType设置为1时生效
UndealtEntrustRule	int	未成委托处理数值同prType
PlaceOrderInterval	int	下撤单时间间隔
UseTrigger	int	是否触价:
否:0
是:1
TriggerType	int	触价类型:
最新价大于:1
最新价小于:2
TriggerPrice	float	触价价格
SuperPriceEnable	int	超价启用笔数
返回
无
示例

python

#coding:gbk
userparam = {
    "OrderType": 1,
    "MaxOrderCount": 20,
    "SuperPriceType": 1,
    "SuperPriceValue": 1.12}
accid = '918800000818'  #资金账号
algo_passorder(23,1101,accid,'000001.SZ',5,15,1000,'',1,'strReMark',userparam,ContextInfo)
#表示修改算法交易的最大委托次数为20,单笔下单基准类型为按价格类型超价,单笔超价1.12元,其他参数同函数交易参数中设置
smart_algo_passorder - 智能算法（VWAP 等）函数
提示

调用该函数需要有【智能算法】使用权限
用于使用主动算法或被动算法交易的函数如VWAP TWAP等

调用方法一：

python

smart_algo_passorder(opType,orderType,accountid,orderCode,prType,price,volume,strageName,quickTrade,userOrderId,smartAlgoType,limitOverRate,minAmountPerOrder,[targetPriceLevel,startTime,endTime,limitControl],ContextInfo)
提示

可选参数可缺省

参数：
其他参数同passorder，详细解释可参考passorder的说明

参数名	类型	说明	提示
prType	int	可选值：
11:限价（只对单股情况支持,对组合交易不支持）
12:市价
特别的对于套利：这个prType只对篮子起作用，期货的采用默认的方式	
smartAlgoType	str	智能算法类型 [enum_constants#smartAlgoType智能算法类型]	
limitOverRate	int	量比 数据范围0-100	网格算法无此项
若在algoParam中填写量比，则填写范围0-1的小数。
minAmountPerOrder	int	智能算法最小委托金额，数据范围0-100000	
targetPriceLevel	int	智能算法目标价格,可选值：
1：己方盘口 1
2：己方盘口2
3：己方盘口3
4：己方盘口4
5：己方盘口5
6：最新价
7：对方盘口	一、输入无效值则targetPriceLevel为1
二、本项只针对冰山算法,其他算法可缺省。
startTime	str	智能算法开始时间	格式"HH:MM:SS"，如"10:30:00"。如果缺省值，则默认为"09:30:00"
endTime	str	智能算法截止时间	格式"HH:MM:SS"，如"14:30:00"。如果缺省值，则默认为"15:30:00"
limitControl	int	涨跌停控制	默认值为1
1：涨停不卖跌停不买
0：无限制
返回
无

示例：

python

#coding:gbk


def init(ContextInfo):
    pass


def after_init(ContextInfo):
    # # 使用smart_algo_passorder 下单
    smart_algo_passorder(
        23,                # 买入
        1101,              # 表示volume的单位是股
        account,           # 资金账号
        '000001.SZ',
        12,                #  11限价，12市价
        0,                 # 限价时，价格填任意数量占位
        50000,             # 5000股
        '',
        2,                 # quickTrade
        '',
        'VWAP',
        25,                 # 量比25%
        0,                  # 智能算法最小委托金额
        1,                  # 智能算法目标价格 本项只针对冰山算法,其他算法可缺省。
        "10:25:00",         # 开始时间
        "14:50:00",         # 结束时间
        1,                  # 涨跌停控制 1为涨停不卖跌停不卖 0 为无限制
        ContextInfo
        )
调用方法二：
当时用algoParam时，函数声明为：smart_algo_passorder(opType,orderType,accountid,orderCode,prType,modelprice,volume,strageName,quickTrade,userid,smartAlgoType,startTime,endTime,algoParam,ContextInfo)参数均不可缺省
smartAlgoType,startTime,endTime 含义同上，algoParam请使用下面的方法获取：

获取algoParam具体字段
释义

获取智能算法参数配置信息

用法

python

get_smart_algo_param(algoList)
参数

参数	类型	说明
algoList	list	需要查询参数配置信息的算法名称列表, 若传空则查询全部有权限的算法参数配置信息
返回

返回一个字典，键为算法名称，值为参数字典列表。

字段	类型	说明
key	string	参数名称key值,即smart_algo_order中algoList字典需要传的键值
name	string	参数名称
dataType	string	参数类型
valueRange	string	参数范围
defaultValue	string	参数默认值
enumName	string	参数枚举值的名称
enumValue	string	参数实际的枚举值
unit	string	参数的单位, 当单位为%时, 值要填写小数而非参数范围所示的百分数值
valueRangeByName	string	不同算法参数范围
defaultValueByName	string	不同算法参数默认值
示例

python

#coding:gbk


def init(ContextInfo):
    pass

    # 方法2 使用algoParam 和smart_algo_passorder
    # 该方法部分旧版本客户端可能会不支持
    # algoParam
    # 先获取所有需要传入的参数
    #
    print(get_smart_algo_param(['VWAP']))
    '''
    输出：[2024-01-30 11:21:10][智能算法1][SH000300][日线] 
    {'VWAP': [
        {'key': 'm_dLimitOverRate', 'name': '量比比例', 'dataType': '浮点数', 'valueRange': '0.00-100.00', 'defaultValue': '20.00', 'enumName': '', 'enumValue': '', 'unit': '%', 'valueRangByName': '', 'defaultValueByName': ''}, 
        {'key': 'm_dMinAmountPerOrder', 'name': '委托最小金额', 'dataType': '整数', 'valueRange': '0-100000', 'defaultValue': '0', 'enumName': '', 'enumValue': '', 'unit': '', 'valueRangByName': '', 'defaultValueByName': ''},
        {'key': 'm_dMaxAmountPerOrder', 'name': '委托最大金额', 'dataType': '浮点数', 'valueRange': '0.00-100000000.00', 'defaultValue': '0', 'enumName': '', 'enumValue': '', 'unit': '', 'valueRangByName': '', 'defaultValueByName': ''}, 
        {'key': 'm_nStopTradeForOwnHiLow', 'name': '涨跌停控制', 'dataType': '整数', 'valueRange': '', 'defaultValue': '涨停不卖跌停不买', 'enumName': '无,涨停不卖跌停不买', 'enumValue': '0,1', 'unit': '', 'valueRangByName': '', 'defaultValueByName': ''}, 
        {'key': 'm_dMulitAccountRate', 'name': '多账号总量比', 'dataType': '浮点数', 'valueRange': '0.00-100.00', 'defaultValue': '0', 'enumName': '', 'enumValue': '', 'unit': '%', 'valueRangByName': '', 'defaultValueByName': ''}, 
        {'key': 'm_strCmdRemark', 'name': '投资备注', 'dataType': '字符串', 'valueRange': '', 'defaultValue': '', 'enumName': '', 'enumValue': '', 'unit': '', 'valueRangByName': '', 'defaultValueByName': ''}]}
    '''
    algoParam={
    'm_dLimitOverRate': 0.25,      # 量比 25%
    'm_dMinAmountPerOrder':0,      # 委托最小金额
    'm_dMaxAmountPerOrder':10000,  # 委托最大金额
    'm_nStopTradeForOwnHiLow': 1,  # 涨跌停控制
    'm_dMulitAccountRate':0.30,    # 多账号总量比
    'm_strCmdRemark':  '投资备注1'  # 投资备注
    }
    smart_algo_passorder(
        23,
        1101,
        account,
        '600000.SH',
        12,
        0,
        10000,
        '',
        2,               # quickTrade
        '投资备注',
        'VWAP',
        "10:25:00",      # 开始时间
        "14:50:00",      # 结束时间
        algoParam,       # 算法参数
        ContextInfo
        ) 
    
cancel-撤销委托
调用方法cancel(orderId, accountId, accountType, ContextInfo)

参数

参数名	类型	含义	说明
orderId	string	委托号	必填
accountID	string	资金账号	必填
AccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
ContextInfo	class	含有k线信息和接口的上下文对象	必填
返回 bool，是否发出了取消委托信号，返回值含义：

True：是
False：否

示例

python返回值

#coding:gbk
'''
（1）下单前,根据 get_trade_detail_data 函数返回账号的信息，判定资金是否充足，账号是否在登录状态，统计持仓情况等等。
（2）满足一定的模型条件，用 passorder 下单。
（3）下单后，时刻根据 get_last_order_id 函数获取委托和成交的最新id，注意如果委托生成了，就有了委托号（这个id需要自己保存做一个全局控制）。
（4）用该委托号根据 get_value_by_order_id 函数查看委托的状态，各种情况等。
当一个委托的状态变成“已成'后，那么对应的成交 deal 信息就有一条成交数据；用该委托号可查看成交情况。
*注：委托列表和成交列表中的委托号是一样的,都是这个 m_strOrderSysID 属性值。
可用 get_last_order_id 获取最新的 order 的委托号,然后根据这个委托号获取 deal 的信息，当获取成功后，也说明这笔交易是成了，可再根据 position 持仓信息再进一步验证。
（5）根据委托号获取委托信息，根据委托状态，或模型设定，用 cancel 取消委托。
'''


def init(ContextInfo):
    ContextInfo.accid = '6000000248'

def handlebar(ContextInfo):
    if ContextInfo.is_last_bar():
        orderid = get_last_order_id(ContextInfo.accid, 'stock', 'order')
        print(cancel(orderid, ContextInfo.accid, 'stock', ContextInfo))
cancel_task - 撤销任务
调用方法cancel_task(taskId,accountId,accountType,ContextInfo)

参数

参数名	类型	含义	说明
taskId	string	委托号	必填
accountID	string	资金账号	必填
AccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
ContextInfo	class	含有k线信息和接口的上下文对象	必填
返回 bool，是否发出了撤销任务信号，返回值含义：

True：是

False：否

示例

python

#coding:gbk
'''
（1）根据get_trade_detail_data函数返回任务的信息,获取任务编号（m_nTaskId），任务状态等等；
（2）根据任务编号，用cancel_task取消委托。
'''

def init(ContextInfo):
    ContextInfo.accid = '6000000248'

def handlebar(ContextInfo):
    # 获取当前客户端所有的任务
    if ContextInfo.is_last_bar():
        objlist = get_trade_detail_data(ContextInfo.accid,'stock','task')
        for obj in objlist:
            cancel_task(str(obj.m_nTaskId),ContextInfo.accid,'stock',ContextInfo)
pause_task - 暂停任务
暂停智能算法任务

调用方法 pause_task(taskId,accountId,accountType,ContextInfo)

参数

参数名	类型	含义	说明
taskId	string	委托号	必填
accountID	string	资金账号	必填
AccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
ContextInfo	class	含有k线信息和接口的上下文对象	必填
返回 bool，是否发出了暂停任务信号，返回值含义：

True：是

False：否

示例

python

#coding:gbk
'''
（1）根据get_trade_detail_data函数返回任务的信息,获取任务编号（m_nTaskId），任务状态等等；
（2）根据任务编号，用pause_task暂停智能算法任务。
'''

def init(ContextInfo):
    ContextInfo.accid = '6000000248'    

def handlebar(ContextInfo):
    
    if ContextInfo.is_last_bar():
        # 获取当前客户端所有的任务
        objlist = get_trade_detail_data(ContextInfo.accid,'stock','task')
        for obj in objlist:
            pause_task(obj.m_nTaskId,ContextInfo.accid,'stock',ContextInfo)
resume_task - 继续任务
继续智能算法任务

调用方法resume_task(taskId,accountId,accountType,ContextInfo)

参数

参数名	类型	含义	说明
taskId	string	委托号	必填
accountID	string	资金账号	必填
AccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
ContextInfo	class	含有k线信息和接口的上下文对象	必填
返回 bool，是否发出了重启任务信号，返回值含义：

True：是

False：否

示例

python

#coding:gbk
'''
（1）根据get_trade_detail_data函数返回任务的信息,获取任务编号（m_nTaskId），任务状态等等；
（2）根据任务编号，用resume_task启动已暂停智能算法任务。
'''

def init(ContextInfo):
    ContextInfo.accid = '6000000248'    
def handlebar(ContextInfo):
    if ContextInfo.is_last_bar():
        # 获取当前客户端所有的任务
        objlist = get_trade_detail_data(ContextInfo.accid,'stock','task')
        for obj in objlist:
            resume_task(obj.m_nTaskId,ContextInfo.accid,'stock',ContextInfo)
get_basket-获取股票篮子
用法： get_basket(basketName)

释义： 获取股票篮子

参数：

basketName：股票篮子名称
示例：


print( get_basket('basket1') )
set_basket-设置股票篮子
用法： set_basket(basketDict)

释义： 设置passorder的股票篮子,仅用于passorder进行篮子交易,设置成功后,用get_basket可以取出后即可进行passorder组合交易下单

参数：

basketDict：股票篮子 {'name':股票篮子名称,'stocks':[{'stock':股票名称,'weight',权重,'quantity':数量,'optType':交易类型}]} 。
示例：


table=[
    {'stock':'600000.SH','weight':0.11,'quantity':100,'optType':23},
    {'stock':'600028.SH','weight':0.11,'quantity':200,'optType':24},
]
basket={'name':'basket1','stocks':table}
set_basket(basket)
#一键买卖2份(2101代表用篮子里quantity字段)basket1里面的股票组合，即600000.SH买入200股，600028.SH卖出400股
table=[
    {'stock':'600000.SH','weight':0.11,'quantity':100,'optType':23},
    {'stock':'600028.SH','weight':0.11,'quantity':200,'optType':24},
]
basket={'name':'basket1','stocks':table}
set_basket(basket)
#一键买卖2份(2101代表用篮子里quantity字段)basket1里面的股票组合，即600000.SH买入200股，600028.SH卖出400股
passorder(35,2101,ContextInfo.accid,'basket1',5,-1,2,'basketOrder',2,'basketOrder',ContextInfo)
##################################
'''
10交易查询函数
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''交易查询函数
get_trade_detail_data-查询账号资金信息、委托记录等
调用方法 get_trade_detail_data(accountID, strAccountType, strDatatype, strategyName)
或不区分策略
get_trade_detail_data(accountID, strAccountType, strDatatype)

参数

参数名	类型	说明	备注
accountID	string	资金账号	必填
strAccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
strDatatype	string	要查询数据类型 可选：
ACCOUNT：账号对象或信用账号对象
POSITION：持仓
POSITION_STATISTICS：持仓统计
ORDER：委托
DEAL ：成交
TASK：任务	必填
strategyName	string	策略 当用passorder下单时指定了strategyName 参数时，当查询成交和委托时传入同样的strageName，则可以只返回包含strategyName的委托子集或成交子集	strategyName参数只对成交和委托有效,选填
返回 list，list 中放的是对应strDatatype的 Python对象，通过 dir(pythonobj) 可返回某个对象的属性列表。

有五种交易相关信息，包括：

ACCOUNT：账号对象或信用账号对象

POSITION：持仓明细

POSITION_STATISTICS: 持仓统计

ORDER：委托

DEAL：成交

TASK：任务

示例：

python返回值


#coding:gbk

account = '800174' # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值；编译器环境里执行的下单函数不会产生实际委托

def init(ContextInfo):
    pass

def handlebar(ContextInfo):
    if not ContextInfo.is_last_bar():
        return
    
    orders = get_trade_detail_data(account, 'stock', 'order')
    print('查询委托结果：')
    for o in orders:
        print(f'股票代码: {o.m_strInstrumentID}, 市场类型: {o.m_strExchangeID}, 证券名称: {o.m_strInstrumentName}, 买卖方向: {o.m_nOffsetFlag}',
        f'委托数量: {o.m_nVolumeTotalOriginal}, 成交均价: {o.m_dTradedPrice}, 成交数量: {o.m_nVolumeTraded}, 成交金额:{o.m_dTradeAmount}')


    deals = get_trade_detail_data(account, 'stock', 'deal')
    print('查询成交结果：')
    for dt in deals:
        print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 买卖方向: {dt.m_nOffsetFlag}', 
        f'成交价格: {dt.m_dPrice}, 成交数量: {dt.m_nVolume}, 成交金额: {dt.m_dTradeAmount}')

    positions = get_trade_detail_data(account, 'stock', 'position')
    print('查询持仓结果：')
    for dt in positions:
        print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 持仓量: {dt.m_nVolume}, 可用数量: {dt.m_nCanUseVolume}',
        f'成本价: {dt.m_dOpenPrice:.2f}, 市值: {dt.m_dInstrumentValue:.2f}, 持仓成本: {dt.m_dPositionCost:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')


    accounts = get_trade_detail_data(account, 'stock', 'account')
    print('查询账号结果：')
    for dt in accounts:
        print(f'总资产: {dt.m_dBalance:.2f}, 净资产: {dt.m_dAssureAsset:.2f}, 总市值: {dt.m_dInstrumentValue:.2f}', 
        f'总负债: {dt.m_dTotalDebit:.2f}, 可用金额: {dt.m_dAvailable:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')
    
    position_statistics = get_trade_detail_data(account,"FUTURE",'POSITION_STATISTICS')
    for obj in position_statistics:
        if obj.m_nDirection == 49:
			continue
		PositionInfo_dict[obj.m_strInstrumentID+"."+obj.m_strExchangeID]={
		"持仓":obj.m_nPosition,
		"成本":obj.m_dPositionCost,
		"浮动盈亏":obj.m_dFloatProfit,
		"保证金占用":obj.m_dUsedMargin
		}
	print(PositionInfo_dict)

	
get_history_trade_detail_data - 查询历史交易明细
用法： get_history_trade_detail_data(accountID,strAccountType,strDatatype,strStratDate,strEndDate);

释义： 获取历史成交明细数据，返回结果为一个([timetag,obj...])的元组

参数：

accountID：string,账号； strAccountType：string,账号类型,有"FUTURE","STOCK","CREDIT","HUGANGTONG","SHENGANGTONG","STOCK_OPTION"； strDatatype：string,交易明细数据类型,有：持仓"POSITION"、委托"ORDER"、成交"DEAL"； strStratDate：string,开始时间,如'20240513'； strEndDate：string,结束时间,如'20240514'；

**返回：**list,list中放的是PythonObj,通过dir(pythonobj)可返回某个对象的属性列表 示例：

示例

def handlebar(ContextInfo):
    obj_list = get_history_trade_detail_data('6000000248','stock','position','20240513','20240514')
    for time,data in obj_list:
        for obj in data:
            print(obj.m_strInstrumentID)
            print(dir(obj))#查看有哪些属性字段
get_ipo_data-获取当日新股新债信息
用法： get_ipo_data([,type])

释义： 获取当日新股新债信息，返回结果为一个字典,包括新股申购代码,申购名称,最大申购数量,最小申购数量等数据

参数：

type：为空时返回新股新债信息，type="STOCK"时只返回新股申购信息，type="BOND"时只返回新债申购信息
示例：


#coding:gbk
def init(ContextInfo):
    ipoData=get_ipo_data()# 返回新股新债信息
    ipoStock=get_ipo_data("STOCK")# 返回新股信息
    ipoCB=get_ipo_data("BOND")# 返回新债申购信息
get_new_purchase_limit-获取账户新股申购额度
用法： get_new_purchase_limit(accid)

释义： 获取账户新股申购额度，返回结果为一个字典,包括上海主板,深圳市场,上海科创版的申购额度

参数：

accid：资金账号，必须时股票账号或者信用账号
示例：


def init(ContextInfo):
    ContextInfo.accid="10000001"# 返回新股新债信息
    purchase_limit=get_new_purchase_limit(ContextInfo.accid)
get_value_by_order_id-根据委托号获取委托或成交信息
调用方法get_value_by_order_id(orderId, accountID, strAccountType, strDatatype)

参数

参数名	类型	含义	说明
orderId	string	委托号	必填
accountID	string	资金账号	必填
strAccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
strDatatype	string	要查询数据类型 可选：
'ORDER'：委托
'DEAL' ：成交	必填
返回

委托对象 或 成交对象

示例

python返回值

def init(ContextInfo):
    ContextInfo.accid = '6000000248'

def handlebar(ContextInfo):
    orderid = get_last_order_id(ContextInfo.accid, 'stock', 'order')
    print(orderid)
    obj = get_value_by_order_id(orderid,ContextInfo.accid, 'stock', 'order')
    print(obj.m_strInstrumentID)
调用方法

python

# 区分策略，添加策略名称参数 strategyName
get_last_order_id(accountID, strAccountType, strDatatype, strategyName)

# 不区分策略
get_last_order_id(accountID, strAccountType, strDatatype)
参数

参数名	类型	含义	说明
accountID	string	资金账号	必填
strAccountType	string	账号类型 可选：
'FUTURE'：期货
'STOCK'：股票
'CREDIT'：信用
'HUGANGTONG'：沪港通
'SHENGANGTONG'：深港通
'STOCK_OPTION'：期权
必填
strDatatype	string	要查询数据类型 可选：
'ORDER'：委托
'DEAL' ：成交	必填
strategyName	string	策略 当用passorder下单时指定了strategyName 参数时，当查询成交和委托时传入同样的strageName，则可以只返回包含strategyName的委托子集或成交子集	选填
返回

String，委托号，如果没找到返回 '-1'。

示例


def init(ContextInfo):
    ContextInfo.accid = '6000000248'

def handlebar(ContextInfo):
    orderid = get_last_order_id(ContextInfo.accid, 'stock', 'order')
    print(orderid)
    obj = get_value_by_order_id(orderid,ContextInfo.accid, 'stock', 'order')
    print(obj.m_strInstrumentID)
get_assure_contract-获取两融担保标的明细
用法： get_assure_contract(accId)

释义： 获取信用账户担保合约明细

参数：

accId：信用账户
返回： list，list 中放的是 StkSubjects，通过 dir(pythonobj) 可返回某个对象的属性列表。

示例：

python


def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def handlebar(ContextInfo): 
    obj = get_assure_contract('6000000248')
    for i in obj[:3]:
		print(show_data(i))


"""
{'m_dAssureRatio': 0.0, # 担保品折算比例
'm_dFinRatio': 0.8, # 融资保证金比例
'm_dSloRatio': 1.0,  # 融券保证金比例
'm_eAssureStatus': 50,  # 是否可做担保
'm_eCreditFundCtl': 50, # 融资交易控制
'm_eCreditStkCtl': 50, # 融券交易控制
'm_eFinStatus': 48, # 融资状态
'm_eSloStatus': 48, # 融券状态
'm_nPlatformID': 10064,  # 平台号
'm_strAccountID': '95000857',  # 资金账号
'm_strBrokerID': '003', # 经纪公司编号
'm_strBrokerName': '光大证券信用',  # 证券公司
'm_strExchangeID': 'SH', # 交易所
'm_strInstrumentID':'510150' # 证券代码
"""
        
get_enable_short_contract-获取可融券明细
提示

注:由于字段m_dSloRatio、m_dSloStatus提供来源和取担保品明细(get_assure_contract)重复，字段在2021年9月移除，后续用担保品明细接口获取,具体见 担保标的对象字段说明

用法： get_enable_short_contract(accId)

释义： 获取信用账户当前可融券的明细

参数：

accId：信用账户
返回： list，list 中放的是 CreditSloEnableAmount，通过 dir(pythonobj) 可返回某个对象的属性列表。

示例：

python


def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def handlebar(ContextInfo):
    obj = get_enable_short_contract('6000000248')
    for i in obj[:3]:
		print(show_data(i))

"""
Rerutn:

{'m_eQuerySloType': 48, # 查询类型
'm_nEnableAmount': 0,  # 融券可融数量
'm_nPlatformID': 10064,  # 平台号
'm_strAccountID': '95000857',  # 资金账号
'm_strBrokerID': '003',  # 经纪公司编号
'm_strBrokerName': '光大证券信用',  # 证券公司
'm_strExchangeID': 'SH', # 标的市场
'm_strInstrumentID': '688321' # 证券代码
}

"""

query_credit_account - 查询信用账户明细
注意

本函数一次最多查询200只股票的两融最大下单量，且同时只能有一个查询,如果前面的查询正在进行中,后面的查询将会提前返回。本函数从服务器查询数据,建议平均查询时间间隔180s一次,不可频繁调用。
该函数必须配合credit_account_callback回调才能使用，关于此回调的说明请看credit_account_callback
callback返回的对象是CCreditAccountDetail
调用query_credit_account，该接口的查询结果将会推送给credit_account_callback，所以程序里需要按照函数参数实现函数credit_account_callback,callback返回的对象是CCreditAccountDetail

用法： query_credit_account(accountId,seq,ContextInfo)
释义： 查询信用账户明细。本函数只能有一个查询，如果前面的查询正在进行中，后面的查询将会提前返回。

参数：

accountId：string，查询的两融账号

seq：int，查询序列号，建议输入唯一值以便对应结果回调

示例：

python返回值

#coding:gbk


import time

def init(ContextInfo):
	ContextInfo.accid='200133'
	
def handlebar(ContextInfo):
	if ContextInfo.is_last_bar():
		query_credit_account(ContextInfo.accid,int(time.time()),ContextInfo)
# 该函数必须配合credit_account_callback回调才能使用
def credit_account_callback(ContextInfo,seq,result):
	print(seq)
	print(f":维持担保比例:{result.m_dPerAssurescaleValue:.2f},总负债:{result.m_dTotalDebt:.2f}")

回调示例 见query_credit_account

query_credit_opvolume - 查询两融最大可下单量
注意

本函数一次最多查询200只股票的两融最大下单量，且同时只能有一个查询,如果前面的查询正在进行中,后面的查询将会提前返回。本函数从服务器查询数据,建议平均查询时间间隔180s一次,不可频繁调用。
该函数必须配合credit_opvolume_callback回调才能使用,关于此回调的说明请看credit_account_callback
调用query_credit_opvolume，该接口的查询结果将会推送给credit_opvolume_callback，所以必须配合credit_opvolume_callback回调才能使用

用法： query_credit_opvolume(accountId,stockCode,opType,prType,price,seq,ContextInfo)

释义： 查询两融最大可下单量。

参数：

accountId:查询的两融账号
stockCode:需要查询的股票代码,stockCode为List的类型,可以查询多只股票
opType:两融下单类型,同passorder的下单类型
prType:报单价格类型,同passorder的报价类型
seq:查询序列号,int型，建议输入唯一值以便对应结果回调
price:报价(非限价单可以填任意值),如果stockCode为List类型,报价也需要为长度相同的List
ContextInfo:ContextInfo类
示例：

python返回值

#coding:gbk

import time

def init(ContextInfo):
	ContextInfo.accid='200133'
	
def handlebar(ContextInfo):
	if ContextInfo.is_last_bar():
        #查询accid账号担保品买入600000,SH限价10元的最大可下单量
		query_credit_opvolume(ContextInfo.accid,'600000.SH',33,11,10,int(time.time()),C) # 查询两融最大可下单量。
		time.sleep(0.5)
        #查询accid账号担保品买入600000,SH限价10元,000001.SZ担保品买入限价20元的最大可下单量
		query_credit_opvolume(ContextInfo.accid,["600000.SH","000001.SZ"],33,11,[10,20],int(time.time()),C) # 查询两融最大可下单量。

# 该函数必须配合credit_opvolume_callback回调才能使用
def credit_opvolume_callback(ContextInfo,accid,seq,ret,result):
	print(seq)
	print(f'查询结果:{ret}') # 正常返回:1,正在查询中-1,输入账号非法:-2,输入查询参数非法:-3,超时等服务器返回报错:-4
	print(result)


get_option_subject_position-取期权标的持仓
用法： get_option_subject_position(accountID)

释义： 取期权标的持仓

参数：

accountID：string,账号
返回： list,list中放的是CLockPosition,通过dir(pythonobj)可返回某个对象的属性列表

示例：


data=get_option_subject_position('880399990383')
print(len(data));
forobjindata:
    print(obj.m_strInstrumentName,obj.m_lockVol,obj.m_coveredVol);
get_comb_option-取期权组合持仓
用法： get_comb_option(accountID)

释义： 取期权组合持仓

参数：

accountID：string,账号
返回： list,list中放的是CStkOptCombPositionDetail ,通过dir(pythonobj)可返回某个对象的属性列表

示例：


obj_list=get_comb_option('880399990383')
print(len(obj_list));
forobjinobj_list:
    print(obj.m_strCombCodeName,obj.m_strCombID,obj.m_nVolume,obj.m_nFrozenVolume)
get_unclosed_compacts-获取未了结负债合约明细
用法： get_unclosed_compacts(accountID,accountType)

释义： 获取未了结负债合约明细

参数：

accountID：str，资金账号
accountType：str，账号类型，这里应该填'CREDIT'
返回：

list([ CStkUnclosedCompacts, ... ]) 负债列表，CStkUnclosedCompacts属性如下：

字段名称	类型	说明
m_strAccountID	string	账号ID
m_nBrokerType	int	账号类型
1-期货账号
2-股票账号
3-信用账号
5-期货期权账号
6-股票期权账号
7-沪港通账号
11-深港通账号
m_strExchangeID	string	市场
m_strInstrumentID	string	证券代码
m_eCompactType	int	合约类型
32-不限制
48-融资
49-融券
m_eCashgroupProp	int	头寸来源
32-不限制
48-普通头寸
49-专项头寸
m_nOpenDate	int	开仓日期(如'20201231')
m_nBusinessVol	int	合约证券数量
m_nRealCompactVol	int	未还合约数量
m_nRetEndDate	int	到期日(如'20201231')
m_dBusinessBalance	float	合约金额
m_dBusinessFare	float	合约息费
m_dRealCompactBalance	float	未还合约金额
m_dRealCompactFare	float	未还合约息费
m_dRepaidFare	float	已还息费
m_dRepaidBalance	float	已还金额
m_strCompactId	string	合约编号
m_strEntrustNo	string	委托编号
m_nRepayPriority	int	偿还优先级
m_strPositionStr	string	定位串
m_eCompactRenewalStatus	int	合约展期状态
48-可申请
49-已申请
50-审批通过
51-审批不通过
52-不可申请
53-已执行
54-已取消
m_nDeferTimes	int	展期次数
示例：


get_unclosed_compacts('6000000248', 'CREDIT')
get_closed_compacts-获取已了结负债合约明细
用法： get_closed_compacts(accountID,accountType)

释义： 获取已了结负债合约明细

参数：

accountID：str，资金账号
accountType：str，账号类型，这里应该填'CREDIT'
返回：

list([ CStkUnclosedCompacts, ... ]) 负债列表，CStkUnclosedCompacts属性如下：

字段名	类型	描述
m_strAccountID	string	账号ID
m_nBrokerType	int	账号类型
1-期货账号
2-股票账号
3-信用账号
5-期货期权账号
6-股票期权账号
7-沪港通账号
11-深港通账号
m_strExchangeID	string	市场
m_strInstrumentID	string	证券代码
m_eCompactType	int	合约类型
32-不限制
48-融资
49-融券
m_eCashgroupProp	int	头寸来源
32-不限制
48-普通头寸
49-专项头寸
m_nOpenDate	int	开仓日期(如'20201231')
m_nBusinessVol	int	合约证券数量
m_nRetEndDate	int	到期日(如'20201231')
m_nDateClear	int	了结日期(如'20201231')
m_nEntrustVol	int	委托数量
m_dEntrustBalance	float	委托金额
m_dBusinessBalance	float	合约金额
m_dBusinessFare	float	合约息费
m_dRepaidFare	float	已还息费
m_dRepaidBalance	float	已还金额
m_strCompactId	string	合约编号
m_strEntrustNo	string	委托编号
m_strPositionStr	string	定位串
示例：


get_closed_compacts('6000000248', 'CREDIT')
################################
'''
11其他交易函数仅回测可用
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
其他交易函数（仅回测可用）
警告

以下函数仅回测生效，实盘和模拟盘交易均不可用

order_lots-指定手数交易
用法： order_lots(stockcode, lots[, style, price], ContextInfo[, accId])

释义： 指定手数交易，指定手数发送买/卖单。如有需要落单类型当做一个参量传入，如果忽略掉落单类型，那么默认以最新价下单。

参数：

stockcode：代码，string，如 '000002.SZ'

lots：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定 选此参数时必须指定有效的price参数，其他style值可不用传入price参数

'HANG'：挂单 用己方盘口挂单，即买入时用盘口买一价下单，卖出时用卖一价挂单，

'COMPETE'：对手

'MARKET'：市价

'SALE5', 'SALE4', 'SALE3', 'SALE2', 'SALE1'：卖5-1价

'BUY1', 'BUY2', 'BUY3', 'BUY4', 'BUY5'：买1-5价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下 1 手买入
    order_lots('000002.SZ', 1, ContextInfo, '600000248')

    # 用对手价下 1 手卖出
    order_lots('000002.SZ', -1, 'COMPETE', ContextInfo, '600000248')

    # 用指定价 37.5 下 2 手卖出
    order_lots('000002.SZ', -2, 'fix', 37.5, ContextInfo, '600000248')
order_value-指定价值交易
用法： order_value(stockcode, value[, style, price], ContextInfo[, accId])

释义： 指定价值交易，使用想要花费的金钱买入 / 卖出股票，而不是买入 / 卖出想要的股数，正数代表买入，负数代表卖出。股票的股数总是会被调整成对应的 100 的倍数（在中国 A 股市场 1 手是 100 股）。当您提交一个卖单时，该方法代表的意义是您希望通过卖出该股票套现的金额，如果金额超出了您所持有股票的价值，那么您将卖出所有股票。需要注意，如果资金不足，该 API 将不会创建发送订单。

参数：

stockcode：代码，string，如 '000002.SZ'

value：金额（元），double

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE5', 'SALE4', 'SALE3', 'SALE2', 'SALE1'：卖5-1价

'BUY1', 'BUY2', 'BUY3', 'BUY4', 'BUY5'：买1-5价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下 10000 元买入
    order_value('000002.SZ', 10000, ContextInfo, '600000248')

    # 用对手价下 10000 元卖出
    order_value('000002.SZ', -10000, 'COMPETE', ContextInfo, '600000248')

    # 用指定价 37.5 下 20000 元卖出
    order_value('000002.SZ', -20000, 'fix', 37.5, ContextInfo, '600000248')
order_percent-指定比例交易
用法： order_percent(stockcode, percent[, style, price], ContextInfo[, accId])

释义： 指定比例交易，发送一个等于目前投资组合价值（市场价值和目前现金的总和）一定百分比的买 / 卖单，正数代表买，负数代表卖。股票的股数总是会被调整成对应的一手的股票数的倍数（1 手是 100 股）。百分比是一个小数，并且小于或等于1（小于等于100%），0.5 表示的是 50%。需要注意，如果资金不足，该 API 将不会创建发送订单。

参数：

stockcode：代码，string，如 '000002.SZ'

percent：比例，double

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE5', 'SALE4', 'SALE3', 'SALE2', 'SALE1'：卖5-1价

'BUY1', 'BUY2', 'BUY3', 'BUY4', 'BUY5'：买1-5价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下 5.1% 价值买入
    order_percent('000002.SZ', 0.051, ContextInfo, '600000248')

    # 用对手价下 5.1% 价值卖出
    order_percent('000002.SZ', -0.051, 'COMPETE', ContextInfo, '600000248')

    # 用指定价 37.5 下 10.2% 价值卖出
    order_percent('000002.SZ', -0.102, 'fix', 37.5, ContextInfo, '600000248')
order_target_value-指定目标价值交易
用法： order_target_value(stockcode, tar_value[, style, price], ContextInfo[, accId])

释义： 指定目标价值交易，买入 / 卖出并且自动调整该证券的仓位到一个目标价值。如果还没有任何该证券的仓位，那么会买入全部目标价值的证券；如果已经有了该证券的仓位，则会买入 / 卖出调整该证券的现在仓位和目标仓位的价值差值的数目的证券。需要注意，如果资金不足，该API将不会创建发送订单。

参数：

stockcode：代码，string，如 '000002.SZ'

tar_value：目标金额（元），double，非负数

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE5', 'SALE4', 'SALE3', 'SALE2', 'SALE1'：卖5-1价

'BUY1', 'BUY2', 'BUY3', 'BUY4', 'BUY5'：买1-5价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下调仓到 10000 元持仓   
    order_target_value('000002.SZ', 10000, ContextInfo, '600000248')

    # 用对手价调仓到 10000 元持仓   
    order_target_value('000002.SZ', 10000, 'COMPETE', ContextInfo, '600000248')

    # 用指定价 37.5 下调仓到 20000 元持仓
    order_target_value('000002.SZ', 20000, 'fix', 37.5, ContextInfo, '600000248')
order_target_percent-指定目标比例交易
用法： order_target_percent(stockcode, tar_percent[, style, price], ContextInfo[, accId])

释义： 指定目标比例交易，买入 / 卖出证券以自动调整该证券的仓位到占有一个指定的投资组合的目标百分比。投资组合价值等于所有已有仓位的价值和剩余现金的总和。买 / 卖单会被下舍入一手股数（A 股是 100 的倍数）的倍数。目标百分比应该是一个小数，并且最大值应该小于等于1，比如 0.5 表示 50%，需要注意，如果资金不足，该API将不会创建发送订单。

参数：

stockcode：代码，string，如 '000002.SZ'

tar_percent：目标百分比 [0 ~ 1]，double

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE5', 'SALE4', 'SALE3', 'SALE2', 'SALE1'：卖5-1价

'BUY1', 'BUY2', 'BUY3', 'BUY4', 'BUY5'：买1-5价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下买入调仓到 5.1% 持仓
    order_target_percent('000002.SZ', 0.051, ContextInfo, '600000248')

    # 用对手价调仓到 5.1% 持仓   
    order_target_percent('000002.SZ', 0.051, 'COMPETE', ContextInfo, '600000248')

    # 用指定价 37.5 调仓到 10.2% 持仓
    order_target_percent('000002.SZ', 0.102, 'fix', 37.5, ContextInfo, '600000248')
order_shares-指定股数交易
用法： order_shares(stockcode, shares[, style, price], ContextInfo[, accId])

释义： 指定股数交易，指定股数的买 / 卖单,最常见的落单方式之一。如有需要落单类型当做一个参量传入，如果忽略掉落单类型，那么默认以最新价下单。

参数：

stockcode：代码，string，如 '000002.SZ'

shares：股数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE5', 'SALE4', 'SALE3', 'SALE2', 'SALE1'：卖5-1价

'BUY1', 'BUY2', 'BUY3', 'BUY4', 'BUY5'：买1-5价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下 100 股买入 
    order_shares('000002.SZ', 100, ContextInfo, '600000248')

    # 用对手价下 100 股卖出   
    order_shares('000002.SZ', -100, 'COMPETE', ContextInfo, '600000248')

    # 用指定价 37.5 下 200 股卖出
    order_shares('000002.SZ', -200, 'fix', 37.5, ContextInfo, '600000248')
buy_open-期货买入开仓
用法： buy_open(stockcode, amount[, style, price], ContextInfo[, accId])

释义： 期货买入开仓

参数：

stockcode：代码，string，如 'IF1805.IF'

amount：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE1'：卖一价

'BUY1'：买一价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价 1 手买入开仓 
    buy_open('IF1805.IF', 1, ContextInfo, '110476')

    # 用对手价 1 手买入开仓   
    buy_open('IF1805.IF', 1, 'COMPETE', ContextInfo, '110476')

    # 用指定价 3750 元 2 手买入开仓
    buy_open('IF1805.IF', 2, 'fix', 3750, ContextInfo, '110476')
buy_close_tdayfirst-期货买入平仓（平今优先）
用法： buy_close_tdayfirst(stockcode, amount[, style, price], ContextInfo[, accId])

释义： 期货买入平仓，平今优先

参数：

stockcode：代码，string，如 'IF1805.IF'

amount：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE1'：卖一价

'BUY1'：买一价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价 1 手买入平仓，平今优先  
    buy_close_tdayfirst('IF1805.IF', 1, ContextInfo, '110476')

    # 用对手价 1 手买入平仓，平今优先   
    buy_close_tdayfirst('IF1805.IF', 1, 'COMPETE', ContextInfo, '110476')

    # 用指定价 3750 元 2 手买入平仓，平今优先
    buy_close_tdayfirst('IF1805.IF', 2, 'fix', 3750, ContextInfo, '110476')
buy_close_ydayfirst-期货买入平仓（平昨优先）
用法： buy_close_ydayfirst(stockcode, amount[, style, price], ContextInfo[, accId])

释义： 期货买入开仓，平昨优先

参数：

stockcode：代码，string，如 'IF1805.IF'

amount：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE1'：卖一价

'BUY1'：买一价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价 1 手买入平仓，平昨优先
    buy_close_ydayfirst('IF1805.IF', 1, ContextInfo, '110476')

    # 用对手价 1 手买入平仓，平昨优先   
    buy_close_ydayfirst('IF1805.IF', 1, 'COMPETE', ContextInfo, '110476')

    # 用指定价 3750 元 2 手买入平仓，平昨优先
    buy_close_ydayfirst('IF1805.IF', 2, 'fix', 3750, ContextInfo, '110476')
sell_open-期货卖出开仓
用法： sell_open(stockcode, amount[, style, price], ContextInfo[, accId])

释义： 期货卖出开仓

参数：

stockcode：代码，string，如 'IF1805.IF'

amount：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE1'：卖一价

'BUY1'：买一价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价 1 手卖出开仓
    sell_open('IF1805.IF', 1, ContextInfo, '110476')
    
    # 用对手价 1 手卖出开仓   
    sell_open('IF1805.IF', 1, 'COMPETE', ContextInfo, '110476')

    # 用指定价 3750 元 2 手卖出开仓
    sell_open('IF1805.IF', 2, 'fix',3750, ContextInfo, '110476')
sell_close_tdayfirst-期货卖出平仓（平今优先）
用法： sell_close_tdayfirst(stockcode, amount[, style, price], ContextInfo[, accId])

释义： 期货卖出平仓，平今优先

参数：

stockcode：代码，string，如 'IF1805.IF'

amount：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE1'：卖一价

'BUY1'：买一价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo):
    # 按最新价下 1 手卖出平仓，平今优先
    sell_close_tdayfirst('IF1805.IF', 1, ContextInfo, '110476')
    
    # 用对手价 1 手卖出平仓，平今优先
    sell_close_tdayfirst('IF1805.IF', 1, 'COMPETE', ContextInfo, '110476')
    
    # 用指定价 3750 元 2 手卖出平仓，平今优先
    sell_close_tdayfirst('IF1805.IF', 1, 'fix', 3750, ContextInfo, '110476')
sell_close_ydayfirst-期货卖出平仓（平昨优先）
用法： sell_close_ydayfirst(stockcode, amount[, style, price], ContextInfo[, accId])

释义： 期货卖出平仓，平昨优先

参数：

stockcode：代码，string，如 'IF1805.IF'

amount：手数，int

style：下单选价类型，string，默认为最新价 'LATEST'，可选值：

'LATEST'：最新

'FIX'：指定

'HANG'：挂单

'COMPETE'：对手

'MARKET'：市价

'SALE1'：卖一价

'BUY1'：买一价

price：价格，double

ContextInfo：PythonObj，Python 对象，这里必须是 ContextInfo

accId：账号，string

返回： 无

示例：


def handlebar(ContextInfo): 
    # 按最新价 1 手卖出平仓，平昨优先 
    sell_close_ydayfirst('IF1805.IF', 1, ContextInfo, '110476')

    # 用对手价 1 手卖出平仓，平昨优先   
    sell_close_ydayfirst('IF1805.IF', 1, 'COMPETE', ContextInfo, '110476')

    # 用指定价 3750 元 2 手卖出平仓，平昨优先
    sell_close_ydayfirst('IF1805.IF', 2, 'fix', 3750, ContextInfo, '110476')
[已弃用] get_debt_contract-获取两融负债合约明细
用法： get_debt_contract(accId)

释义： 获取信用账户负债合约明细

此接口已弃用，替代接口为get_unclosed_compacts（获取未了结负债）和get_closed_compacts（获取已了结负债）

参数：

accId：信用账户
返回： list，list 中放的是 PythonObj，通过 dir(pythonobj) 可返回某个对象的属性列表。

示例：


def handlebar(ContextInfo):
    obj_list = get_debt_contract('6000000248')
    for obj in obj_list:
        # 输出负债合约名
        print(obj.m_strInstrumentName)
get_hkt_exchange_rate-获取沪深港通汇率数据
用法： get_hkt_exchange_rate(accountID,accountType)

释义： 获取沪深港通汇率数据

参数：

accountID：string,账号；
accountType:string,账号类型,必须填HUGANGTONG或者SHENGANGTONG
返回：

dict,字段释义：

bidReferenceRate:买入参考汇率

askReferenceRate:卖出参考汇率

dayBuyRiseRate:日间买入参考汇率浮动比例

daySaleRiseRate:日间卖出参考汇率浮动比例

示例：


def init(ContextInfo):
      data=get_hkt_exchange_rate('6000000248','HUGANGTONG')
      print(data)
#########################################
'''
12实时主推函数
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
account_callback - 资金账号状态变化主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。
用法： account_callback(ContextInfo, accountInfo)

释义： 当资金账号状态有变化时，这个函数被客户端调用

参数：

ContextInfo：特定对象
accountInfo：账号对象或信用账号对象
返回： 无

示例：

示例返回值

#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def account_callback(ContextInfo, accountInfo):
    print(show_data(accountInfo)) 

task_callback - 账号任务状态变化主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。
用法： task_callback(ContextInfo, taskInfo)

释义： 当账号任务状态有变化时，这个函数被客户端调用

参数：

ContextInfo：特定对象
taskInfo 任务对象
返回： 无

示例：

示例返回值

#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def task_callback(ContextInfo, taskInfo):
    print(show_data(taskInfo))
order_callback - 账号委托状态变化主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。
用法： order_callback(ContextInfo, orderInfo)

释义： 当账号委托状态有变化时，这个函数被客户端调用

参数：

ContextInfo：特定对象
orderInfo：委托
返回： 无

示例：

示例返回值

#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def order_callback(ContextInfo, orderInfo):
    print(show_data(orderInfo))
deal_callback - 账号成交状态变化主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。
用法： deal_callback(ContextInfo, dealInfo)

释义： 当账号成交状态有变化时，这个函数被客户端调用

参数：

ContextInfo：特定对象
dealInfo：成交
返回： 无

示例：

示例返回值

#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def deal_callback(ContextInfo, dealInfo):
    print(show_data(dealInfo))
position_callback - 账号持仓状态变化主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。
用法： position_callback(ContextInfo, positonInfo)

释义： 当账号持仓状态有变化时，这个函数被客户端调用

参数：

ContextInfo：特定对象
positonInfo：持仓
返回： 无

示例：

示例返回值

#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def position_callback(ContextInfo, positionInfo):
    print(show_data(positionInfo))

orderError_callback - 账号异常下单主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。
用法： orderError_callback(ContextInfo,orderArgs,errMsg)

释义： 当账号下单异常时，这个函数被客户端调用

参数：

ContextInfo：特定对象
orderArgs：下单参数
errMsg：错误信息
返回： 无

示例：

示例返回值

#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 11, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def orderError_callback(ContextInfo,orderArgs,errMsg):
    print(show_data(orderArgs))
    print(errMsg)

其他主推函数
credit_account_callback - 查询信用账户明细回调
用法： credit_account_callback(ContextInfo,seq,result)

释义： 查询信用账户明细回调

参数：

ContextInfo：策略模型全局对象
seq:query_credit_account时输入查询seq
result: 信用账户明细
credit_opvolume_callback - 查询两融最大可下单量的回调
用法： credit_opvolume_callback(ContextInfo,accid,seq,ret,result)

释义： 查询两融最大可下单量的回调。

参数：

ContextInfo：策略模型全局对象
accid:查询的账号
seq:query_credit_opvolume时输入查询seq
ret:查询结果状态。正常返回:1,正在查询中-1,输入账号非法:-2,输入查询参数非法:-3,超时等服务器返回报错:-4
result:查询到的结果
示例 见query_credit_opvolume
##########################################
'''
15枚举常量
，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是小果量化，，欢迎联系微信：xg_quant。，只做学习使用，不做投资参考，注意风险
'''
opType - 操作类型
期货/股指期权/商品期权 - 六键
数值	描述
0	开多
1	平昨多
2	平今多
3	开空
4	平昨空
5	平今空
期货/股指期权/商品期权 - 四键
数值	描述
6	平多, 优先平今
7	平多, 优先平昨
8	平空, 优先平今
9	平空, 优先平昨
期货/股指期权/商品期权 - 两键
数值	描述
10	卖出, 如有多仓, 优先平仓, 优先平今, 如有余量, 再开空
11	卖出, 如有多仓, 优先平仓, 优先平昨, 如有余量, 再开空
12	买入, 如有空仓, 优先平仓, 优先平今, 如有余量, 再开多
13	买入, 如有空仓, 优先平仓, 优先平昨, 如有余量, 再开多
14	买入, 不优先平仓
15	卖出, 不优先平仓
股票/ETF/可转债买卖
数值	描述
23	股票/ETF/可转债买入，或沪港通、深港通股票买入
24	股票/ETF/可转债卖出，或沪港通、深港通股票卖出
融资融券
数值	描述
27	融资买入
28	融券卖出
29	买券还券
30	直接还券
31	卖券还款
32	直接还款
33	担保品买入
34	担保品卖出
组合交易
数值	描述
25	组合买入，或沪港通、深港通的组合买入
26	组合卖出，或沪港通、深港通的组合卖出
27	融资买入
28	融券卖出
29	买券还券
31	卖券还款
33	担保品买入
34	担保品卖出
35	普通账号一键买卖
36	信用账号一键买卖
40	期货组合开多
43	期货组合开空
46	期货组合平多, 优先平今
47	期货组合平多, 优先平昨
48	期货组合平空, 优先平今
49	期货组合平空, 优先平昨
ETF期权交易
数值	描述
50	买入开仓
51	卖出平仓
52	卖出开仓
53	买入平仓
54	备兑开仓
55	备兑平仓
56	认购行权
57	认沽行权
58	证券锁定
59	证券解锁
ETF申赎交易
数值	描述
60	申购
61	赎回
专项两融
数值	描述
70	专项融资买入
71	专项融券卖出
72	专项买券还券
73	专项直接还券
74	专项卖券还款
75	专项直接还款
可转债转股/回售
数值	描述
80	普通账户转股
81	普通账户回售
82	信用账户转股
83	信用账户回售
orderType - 下单方式
提示

注意

一、期货不支持 1102 和 1202

二、对所有账号组的操作相当于对账号组里的每个账号做一样的操作，如：

passorder(23, 1202, 'testS', '000001.SZ', 5, -1, 50000, ContextInfo)，意思就是对账号组testS 里的所有账号都以最新价开仓买入 50000 元市值的 000001.SZ平安银行；
passorder (60,1101,"test",'510050. SH', 5,-1,1, ContextInfo)意思就是账号test申购1个单位 (900000股)的华夏上证50ETF (只申购不买入成分股)。
单股交易
数值	描述
1101	单股、单账号、普通、股/手方式下单
1102	单股、单账号、普通、金额（元）方式下单（只支持股票）
1113	单股、单账号、总资产、比例 [0 ~ 1] 方式下单
1123	单股、单账号、可用、比例[0 ~ 1]方式下单
单股交易（账号组）
数值	描述
1201	单股、账号组（无权重）、普通、股/手方式下单
1202	单股、账号组（无权重）、普通、金额（元）方式下单（只支持股票）
1213	单股、账号组（无权重）、总资产、比例 [0 ~ 1] 方式下单
1223	单股、账号组（无权重）、可用、比例 [0 ~ 1] 方式下单
组合交易（单账号）
数值	描述
2101	组合、单账号、普通、按组合股票数量（篮子中股票设定的数量）方式下单 > 对应 volume 的单位为篮子的份
2102	组合、单账号、普通、按组合股票权重（篮子中股票设定的权重）方式下单 > 对应 volume 的单位为元
2103	组合、单账号、普通、按账号可用方式下单 > （底层篮子股票怎么分配？答：按可用资金比例后按篮子中股票权重分配，如用户没填权重则按相等权重分配）只对股票篮子支持
组合交易（账号组）
数值	描述
2201	组合、账号组（无权重）、普通、按组合股票数量方式下单
2202	组合、账号组（无权重）、普通、按组合股票权重方式下单
2203	组合、账号组（无权重）、普通、按账号可用方式下单只对股票篮子支持
prType - 下单选价类型
关于使用市价指令的说明

对于上交所（42,43,44,45）

当prType选择市价类型时时，price为保护限价，范围为（0 - 9999）表示投资者能够接受的最高买入价或最低卖出价，即买入申报的成交价格和转限价的价格不高于保护限价，卖出申报的成交价格和转限价的价格不低于保护限价，当price指定为 0 时，保护限价为对应的涨跌停价
融券卖出不允许使用市价指令
集合竞价阶段不允许使用市价指令
对于深交所（44,45,46,47,48）

市价申报只适用于有价格涨跌幅限制证券。
集合竞价阶段不允许使用市价指令
对于北交所(42,43,44,45)

当prType选择市价类型时时，price为保护限价，范围为（0 - 9999）表示投资者能够接受的最高买入价或最低卖出价，即买入申报的成交价格和转限价的价格不高于保护限价，卖出申报的成交价格和转限价的价格不低于保护限价，当price指定为 0 时，保护限价为对应的涨跌停价
融券卖出不允许使用市价指令
集合竞价阶段不允许使用市价指令
数值	描述
-1	无效(只对于algo_passorder起作用)
0	卖5价
1	卖4价
2	卖3价
3	卖2价
4	卖1价
5	最新价
6	买1价
7	买2价(组合不支持)
8	买3价(组合不支持)
9	买4价(组合不支持)
10	买5价(组合不支持)
11	指定价（只对单股情况支持,对组合交易不支持）
12	涨跌停价(对手方最远端价格)
13	挂单价(本方一档价格)
14	对手价(对方一档价格)
18	市价最优价[郑商所][期货] (不支持模拟交易中使用)
19	市价即成剩撤[大商所][期货] (不支持模拟交易中使用)
20	市价全额成交或撤[大商所][期货] (不支持模拟交易中使用)
21	市价最优一档即成剩撤[中金所][期货] (不支持模拟交易中使用)
22	市价最优五档即成剩撤[中金所][期货] (不支持模拟交易中使用)
23	市价最优一档即成剩转[中金所][期货] (不支持模拟交易中使用)
24	市价最优五档即成剩转[中金所][期货] (不支持模拟交易中使用)
26	限价即时全部成交否则撤单[上交所[期权]] [深交所[期权]] (不支持模拟交易中使用)
27	市价即成剩撤[上交所][期权] (不支持模拟交易中使用)
28	市价即全成否则撤[上交所][期权] (不支持模拟交易中使用)
29	市价剩转限价[上交所][期权] (不支持模拟交易中使用)
42	最优五档即时成交剩余撤销申报[上交所[股票]][北交所[股票]] (不支持模拟交易中使用)
43	最优五档即时成交剩转限价申报[上交所[股票]][北交所[股票]] (不支持模拟交易中使用)
44	对手方最优价格委托[上交所[股票]][深交所[股票][北交所[股票]][期权]] (不支持模拟交易中使用)
45	本方最优价格委托[上交所[股票]][深交所[股票][北交所[股票]][期权]] (不支持模拟交易中使用)
46	即时成交剩余撤销委托[深交所][股票][期权] (不支持模拟交易中使用)
47	最优五档即时成交剩余撤销委托[深交所][股票][期权] (不支持模拟交易中使用)
48	全额成交或撤销委托[深交所][股票][期权] (不支持模拟交易中使用)
49	盘后定价
volume - 下单数量
提示

根据 orderType 值最后一位确定 volume 的单位

单股下单时
数值	描述
1	股 / 手 （股票: 股，股票期权: 张，期货: 手，可转债: 张，基金：份）
2	金额（元）
3	比例（%）
组合下单时
数值	描述
1	按组合股票数量（份）
2	按组合股票权重（元）
3	按账号可用（%）
quicktrade - 快速下单
数值	描述
0	否
1	是
2	是
提示

passorder是对最后一根K线完全走完后生成的模型信号在下一根K线的第一个 tick 数据来时触发下单交易；

采用quickTrade参数设置为1时，非历史 bar 上执行时（ContextInfo.is_last_bar()为True），只要策略模型中调用到就触发下单交易。

quickTrade参数设置为2时，不判断 bar 状态，只要策略模型中调用到就触发下单交易，历史 bar 上也能触发下单，请谨慎使用。

enum_ - 对象属性状态字段释义
enum_EEntrustBS - 买卖方向
变量	数值	描述
ENTRUST_BUY	48	买入，多
ENTRUST_SELL	49	卖出，空
ENTRUST_PLEDGE_IN	81	质押入库
ENTRUST_PLEDGE_OUT	66	质押出库
EEntrustSubmitStatus - 报单状态
数值	描述
48	已经提交
49	撤单已经提交
50	修改已经提交
51	已经接受
52	报单已经被拒绝
53	撤单已经被拒绝
54	改单已经被拒绝
enum_EEntrustTypes - 委托类型
变量名称	数值	描述
ENTRUST_BUY_SELL	48	买卖
ENTRUST_QUERY	49	查询
ENTRUST_CANCE	50	撤单
ENTRUST_APPEND	51	补单
ENTRUST_COMFIRM	52	确认
ENTRUST_BIG	53	大宗
ENTRUST_FIN	54	融资委托
ENTRUST_SLO	55	融券委托
ENTRUST_CLOSE	56	信用平仓
ENTRUST_CREDIT_NORMAL	57	信用普通委托
ENTRUST_CANCEL_OPEN	58	撤单补单
ENTRUST_TYPE_OPTION_EXERCISE	59	行权
ENTRUST_TYPE_OPTION_SECU_LOCK	60	锁定
ENTRUST_TYPE_OPTION_SECU_UNLOCK	61	解锁
ENTRUST_QUOTATION_REPURCHASE	62	报价回购
ENTRUST_TYPE_OPTION_ABANDON	63	放弃行权
ENTRUST_AGREEMENT_REPURCHASE	64	协议回购
ENTRUST_TYPE_OPTION_COMB_EXERCISE	65	组合行权
ENTRUST_TYPE_OPTION_BUILD_COMB_STRATEGY	66	构建组合策略持仓
ENTRUST_TYPE_OPTION_RELEASE_COMB_STRATEGY	67	解除组合策略持仓
ENTRUST_TYPE_LMT_LOAN	68	转融通出借
ENTRUST_TYPE_LMT_LOAN_DEFER	69	转融通出借展期
ENTRUST_TYPE_LMT_LOAN_FINISH_AHEAD	70	转融通出借提前了结
ENTRUST_CROSS_MARKET_IN	71	跨市场场内
ENTRUST_CROSS_MARKET_OUT	72	跨市场场外
enum_EEntrustStatus - 委托状态
变量名称	数值	描述
ENTRUST_STATUS_WAIT_REPORTING	49	待报
ENTRUST_STATUS_REPORTED	50	已报（已报出到柜台，待成交）
ENTRUST_STATUS_REPORTED_CANCEL	51	已报待撤（对已报状态的委托撤单吗，等待柜台处理撤单请求）
ENTRUST_STATUS_PARTSUCC_CANCEL	52	部成待撤（已报到柜台，已有部分成交，已发出对剩余部分的撤单，待柜台处理撤单请求）
ENTRUST_STATUS_PART_CANCEL	53	部撤（已报到柜台，已有部分成交，剩余部分已撤）
ENTRUST_STATUS_CANCELED	54	已撤
ENTRUST_STATUS_PART_SUCC	55	部成（已报到柜台，已有部分成交）
ENTRUST_STATUS_SUCCEEDED	56	已成
ENTRUST_STATUS_JUNK	57	废单（不符合报单条件，委托被打回，相关信息再委托的废单原因字段查看）
委托状态流程

enum_EHedge_Flag_Type - 投保类型
变量名称	数值	描述
HEDGE_FLAG_SPECULATION	49	投机
HEDGE_FLAG_ARBITRAGE	50	套利
HEDGE_FLAG_HEDGE	51	套保
enum_EFutureTradeType - 成交类型
变量名称	数值	描述
FUTRUE_TRADE_TYPE_COMMON	48	普通成交
FUTURE_TRADE_TYPE_OPTIONSEXECUTION	49	期权成交
FUTURE_TRADE_TYPE_OTC	50	OTC 成交
FUTURE_TRADE_TYPE_EFPDIRVED	51	期转现衍生成交
FUTURE_TRADE_TYPE_COMBINATION_DERIVED	52	组合衍生成交
enum_EBrokerPriceType - 价格类型
变量名称	数值	描述
BROKER_PRICE_ANY	49	市价
BROKER_PRICE_LIMIT	50	限价
BROKER_PRICE_BEST	51	最优价
BROKER_PRICE_PROP_ALLOTMENT	52	配股
BROKER_PRICE_PROP_REFER	53	转托
BROKER_PRICE_PROP_SUBSCRIBE	54	申购
BROKER_PRICE_PROP_BUYBACK	55	回购
BROKER_PRICE_PROP_PLACING	56	配售
BROKER_PRICE_PROP_DECIDE	57	指定
BROKER_PRICE_PROP_EQUITY	58	转股
BROKER_PRICE_PROP_SELLBACK	59	回售
BROKER_PRICE_PROP_DIVIDEND	60	股息
BROKER_PRICE_PROP_SHENZHEN_PLACING	68	深圳配售确认
BROKER_PRICE_PROP_CANCEL_PLACING	69	配售放弃
BROKER_PRICE_PROP_WDZY	70	无冻质押
BROKER_PRICE_PROP_DJZY	71	冻结质押
BROKER_PRICE_PROP_WDJY	72	无冻解押
BROKER_PRICE_PROP_JDJY	73	解冻解押
BROKER_PRICE_PROP_ETF	81	ETF申购
BROKER_PRICE_PROP_VOTE	75	投票
BROKER_PRICE_PROP_YYSGYS	92	要约收购预售
BROKER_PRICE_PROP_YSYYJC	77	预售要约解除
BROKER_PRICE_PROP_FUND_DEVIDEND	78	基金设红
BROKER_PRICE_PROP_FUND_ENTRUST	79	基金申赎
BROKER_PRICE_PROP_CROSS_MARKET	80	跨市转托
BROKER_PRICE_PROP_EXERCIS	83	权证行权
BROKER_PRICE_PROP_PEER_PRICE_FIRST	84	对手方最优价格
BROKER_PRICE_PROP_L5_FIRST_LIMITPX	85	最优五档即时成交剩余转限价
BROKER_PRICE_PROP_MIME_PRICE_FIRST	86	本方最优价格
BROKER_PRICE_PROP_INSTBUSI_RESTCANCEL	87	即时成交剩余撤销
BROKER_PRICE_PROP_L5_FIRST_CANCEL	88	最优五档即时成交剩余撤销
BROKER_PRICE_PROP_FULL_REAL_CANCEL	89	全额成交并撤单
BROKER_PRICE_PROP_DIRECT_SECU_REPAY	101	直接还券
BROKER_PRICE_PROP_FUND_CHAIHE	90	基金拆合
BROKER_PRICE_PROP_DEBT_CONVERSION	91	债转股
BROKER_PRICE_BID_LIMIT	92	港股通竞价限价
BROKER_PRICE_ENHANCED_LIMIT	93	港股通增强限价
BROKER_PRICE_RETAIL_LIMIT	94	港股通零股限价
BROKER_PRICE_PROP_INCREASE_SHARE	'j'	增发
BROKER_PRICE_PROP_COLLATERAL_TRANSFER	107	担保品划转
BROKER_PRICE_PROP_NEEQ_PRICING	'w'	定价（全国股转 - 挂牌公司交易 - 协议转让）
BROKER_PRICE_PROP_NEEQ_MATCH_CONFIRM	'x'	成交确认（全国股转 - 挂牌公司交易 - 协议转让）
BROKER_PRICE_PROP_NEEQ_MUTUAL_MATCH_CONFIRM	'y'	互报成交确认（全国股转 - 挂牌公司交易 - 协议转让）
BROKER_PRICE_PROP_NEEQ_LIMIT	'z'	限价（用于挂牌公司交易 - 做市转让 - 限价买卖和两网及退市交易-限价买卖）
enum_EOffset_Flag_Type - 操作类型
变量名称	数值	描述
EOFF_THOST_FTDC_OF_INVALID	-1	无效操作
EOFF_THOST_FTDC_OF_Open	48	买入，开仓
EOFF_THOST_FTDC_OF_Close	49	卖出，平仓
EOFF_THOST_FTDC_OF_ForceClose	50	强平
EOFF_THOST_FTDC_OF_CloseToday	51	平今
EOFF_THOST_FTDC_OF_CloseYesterday	52	平昨
EOFF_THOST_FTDC_OF_ForceOff	53	强减
EOFF_THOST_FTDC_OF_LocalForceClose	54	本地强平
EOFF_THOST_FTDC_OF_PLEDGE_IN	81	质押入库
EOFF_THOST_FTDC_OF_PLEDGE_OUT	66	质押出库
EOFF_THOST_FTDC_OF_ALLOTMENT	67	股票配股
enum_EXTSubjectsStatus - 融资融券状态
变量名称	数值	描述
SUBJECTS_STATUS_NORMAL	48	正常
SUBJECTS_STATUS_PAUSE	49	暂停
SUBJECTS_STATUS_NOT	50	作废
enum_EXTCreditFundCtl - 融资交易控制
变量名称	数值	描述
FUND_CTL_ONLY_FIN_BUY	48	只允许融资买入
FUND_CTL_ONLY_SELL_CASH_REPAY	49	只允许卖券还款
FUND_CTL_ALL	50	既允许融资买入又允许卖券还款
FUND_CTL_NONE	51	既不允许融资买入又不允许卖券还款
enum_EXTCreditStkCtl - 融券交易控制
变量名称	数值	描述
STK_CTL_ONLY_SLO_SELL	48	只允许融券卖出
STK_CTL_ONLY_BUY_SECU_REPAY	49	只允许买券还券
STK_CTL_ALL	50	既允许融券卖出又允许买券还券
STK_CTL_NONE	51	既不允许融券卖出又不允许买券还券
enum_EXTSloTypeQueryMode - 查询类型
变量名称	数值	描述
XT_SLOTYPE_QUERYMODE_NOMARL	48	普通
XT_SLOTYPE_QUERYMODE_SPECIAL	49	专项
enum_EXTCompactType - 合约类型
变量名称	数值	描述
COMPACT_TYPE_ALL	32	不限制
COMPACT_TYPE_FIN	48	融资
COMPACT_TYPE_SLO	49	融券
enum_EXTCompactStatus - 合约状态
变量名称	数值	描述
COMPACT_STATUS_ALL	32	不限制
COMPACT_STATUS_UNDONE	48	未归还
COMPACT_STATUS_PART_DONE	49	部分归还
COMPACT_STATUS_DONE	50	已归还
COMPACT_STATUS_DONE_BY_SELF	51	自行了结
COMPACT_STATUS_DONE_BY_HAND	52	手工了结
COMPACT_STATUS_NOT_DEBT	53	未形成负债
COMPACT_STATUS_EXPIRY	54	合约已过期
enum_EXTCompactBrushSource - 头寸来源
变量名称	数值	描述
XT_COMPACT_BRUSH_SOURCE_ALL	32	不限制
XT_COMPACT_BRUSH_SOURCE_NORMAL	48	普通头寸
XT_COMPACT_BRUSH_SOURCE_SPECIAL	49	专项头寸
enum_EXTSpecialAssure - 是否可以用融券资金买入
变量名称	数值	描述
ASSURE_USE_SLO_CASH_DISABLE	48	担保品买入不允许使用融券资金
ASSURE_USE_SLO_CASH_ENABLE	49	担保品买入允许使用融券资金
enum_EOperationType - 下单操作类型/主要交易类型
变量名称	数值	描述
OPT_OPEN_LONG	0	开多
OPT_CLOSE_LONG_HISTORY	1	平昨多
OPT_CLOSE_LONG_TODAY	2	平今多
OPT_OPEN_SHORT	3	开空
OPT_CLOSE_SHORT_HISTORY	4	平昨空
OPT_CLOSE_SHORT_TODAY	5	平今空
OPT_CLOSE_LONG_TODAY_FIRST	6	优先平今多
OPT_CLOSE_LONG_HISTORY_FIRST	7	优先平昨多
OPT_CLOSE_SHORT_TODAY_FIRST	8	平空优先平今
OPT_CLOSE_SHORT_HISTORY_FIRST	9	平空优先平昨
OPT_CLOSE_LONG_TODAY_HISTORY_THEN_OPEN_SHORT	10	卖出优先平今
OPT_CLOSE_LONG_HISTORY_TODAY_THEN_OPEN_SHORT	11	卖出优先平昨
OPT_CLOSE_SHORT_TODAY_HISTORY_THEN_OPEN_LONG	12	买入优先平今
OPT_CLOSE_SHORT_HISTORY_TODAY_THEN_OPEN_LONG	13	买入优先平昨
OPT_CLOSE_LONG	14	平多
OPT_CLOSE_SHORT	15	平空
OPT_OPEN	16	开仓
OPT_CLOSE	17	平仓
OPT_BUY	18	买入
OPT_SELL	19	卖出
OPT_FIN_BUY	20	融资买入
OPT_SLO_SELL	21	融券卖出
OPT_BUY_SECU_REPAY	22	买券还券
OPT_DIRECT_SECU_REPAY	23	直接还券
OPT_SELL_CASH_REPAY	24	卖券还款
OPT_DIRECT_CASH_REPAY	25	直接还款
OPT_FUND_SUBSCRIBE	26	基金申购
OPT_FUND_REDEMPTION	27	基金赎回
OPT_FUND_MERGE	28	基金合并
OPT_FUND_SPLIT	29	基金分拆
OPT_PLEDGE_IN	30	质押入库
OPT_PLEDGE_OUT	31	质押出库
OPT_OPTION_BUY_OPEN	32	买入开仓（个股期权交易）
OPT_OPTION_SELL_CLOSE	33	卖出平仓（个股期权交易）
OPT_OPTION_SELL_OPEN	34	卖出开仓（个股期权交易）
OPT_OPTION_BUY_CLOSE	35	买入平仓（个股期权交易）
OPT_OPTION_COVERED_OPEN	36	备兑开仓（个股期权交易）
OPT_OPTION_COVERED_CLOSE	37	备兑平仓（个股期权交易）
OPT_OPTION_CALL_EXERCISE	38	认购行权（个股期权交易）
OPT_OPTION_PUT_EXERCISE	39	认沽行权（个股期权交易）
OPT_OPTION_SECU_LOCK	40	证券锁定（个股期权交易）
OPT_OPTION_SECU_UNLOCK	41	证券解锁（个股期权交易）
OPT_N3B_PRICE_BUY	42	协议转让-定价买入
OPT_N3B_PRICE_SELL	43	协议转让-定价卖出
OPT_N3B_CONFIRM_BUY	44	协议转让-成交确认买入
OPT_N3B_CONFIRM_SELL	45	协议转让-成交确认卖出
OPT_N3B_REPORT_CONFIRM_BUY	46	协议转让-互报成交确认买入
OPT_N3B_REPORT_CONFIRM_SELL	47	协议转让-互报成交确认卖出
OPT_N3B_LIMIT_PRICE_BUY	48	全国股转-限价买入
OPT_N3B_LIMIT_PRICE_SELL	49	全国股转-限价卖出
OPT_FUTURE_OPTION_EXERCISE	50	期货期权行权
OPT_CONVERT_BONDS	51	可转债转股
OPT_SELL_BACK_BONDS	52	可转债回售
OPT_STK_ALLOTMENT	53	股票配股
OPT_STK_INCREASE_SHARE	54	股票增发
OPT_COLLATERAL_TRANSFER_IN	55	担保品划入
OPT_COLLATERAL_TRANSFER_OUT	56	担保品划出
OPT_BLOCK_INTENTION_BUY	57	意向申报买入
OPT_BLOCK_INTENTION_SELL	58	意向申报卖出
OPT_BLOCK_PRICE_BUY	59	定价申报买入
OPT_BLOCK_PRICE_SELL	60	定价申报卖出
OPT_BLOCK_CONFIRM_BUY	61	成交申报买入
OPT_BLOCK_CONFIRM_SELL	62	成交申报卖出
OPT_BLOCK_CLOSE_PRICE_BUY	63	盘后定价买入
OPT_BLOCK_CLOSE_PRICE_SELL	64	盘后定价卖出
OPT_GOLD_PRICE_DELIVERY_BUY	65	黄金交割买
OPT_GOLD_PRICE_DELIVERY_SELL	66	黄金交割卖
OPT_GOLD_PRICE_MIDDLE_BUY	67	黄金中立仓买
OPT_GOLD_PRICE_MIDDLE_SELL	68	黄金中立仓卖
OPT_COMPOSE_ONEKEY_BUYSELL	69	组合交易一键买卖
OPT_COMPOSE_GGT_BUY	70	组合交易港股通买入
OPT_COMPOSE_GGT_SELL	71	组合交易港股通卖出
OPT_ODD_SELL	72	零股卖出
OPT_ETF_STOCK_BUY	73	成份股买入
OPT_ETF_STOCK_SELL	74	成份股卖出
OPT_OTC_FUND_SUBSCRIBE	200	场外基金认购
OPT_OTC_FUND_PURCHASE	201	场外基金申购
OPT_OTC_FUND_REDEMPTION	202	场外基金赎回
OPT_OTC_FUND_CONVERT	203	场外基金转换
OPT_OTC_FUND_BONUS_TYPE_UPDATE	204	场外基金分红方式变更
OPT_OTC_CONTRACTUAL_DEPOSIT	205	场外协议存款
OPT_OTC_NON_CONTRACTUAL_DEPOSIT	206	场外非协议存款
OPT_OTC_CONTRACTUAL_DEPOSIT_ASK	207	场外协议存款询价
OPT_OTC_NON_CONTRACTUAL_DEPOSIT_ASK	208	场外非协议存款询价
OPT_OTC_NON_CONTRACTUAL_DEPOSIT_CUR	209	场外非协议活期存款
OPT_OTC_DRAW_DEPOSIT	210	场外存单支取
OPT_OTC_STOCK_INQUIRY	230	网下询价
OPT_OTC_STOCK_PURCHASE	231	网下申购
OPT_OPTION_NS_DEPOSIT	1001	场外转账入金
OPT_OPTION_NS_WITHDRAW	1002	场外转账出金
OPT_OPTION_NS_INOUT	1003	场外互转
OPT_ETF_PURCHASE	1004	ETF申购
OPT_ETF_REDEMPTION	1005	ETF赎回
OPT_OUTER_BUY	1006	外盘买入
OPT_OUTER_SELL	1007	外盘卖出
OPT_OUTER_CAN_CLOSE_BUY	1008	外盘可平买仓
OPT_OUTER_CAN_CLOSE_SELL	1009	外盘可平卖仓
OPT_SLO_SELL_SPECIAL	1010	专项融券卖出
OPT_BUY_SECU_REPAY_SPECIAL	1011	专项买券还券
OPT_DIRECT_SECU_REPAY_SPECIAL	1012	专项直接还券
OPT_NEEQ_O3B_LIMIT_PRICE_BUY	1013	全国股转-两网及退市交易-限价买入
OPT_NEEQ_O3B_LIMIT_PRICE_SELL	1014	全国股转-两网及退市交易-限价卖出
OPT_IBANK_BOND_BUY	1015	投行债券买入
OPT_IBANK_BOND_SELL	1016	投行债券卖出
OPT_IBANK_FUND_REPURCHASE	1017	质押式融资回购
OPT_IBANK_BOND_REPURCHASE	1018	质押式融券回购
OPT_IBANK_BOND_REPAY	1019	质押式融资购回
OPT_IBANK_FUND_RETRIEVE	1020	质押式融券购回
OPT_INTEREST_FEE	1021	融券息费
OPT_FIN_BUY_SPECIAL	1022	专项融资买入
OPT_SELL_CASH_REPAY_SPECIAL	1023	专项卖券还款
OPT_DIRECT_CASH_REPAY_SPECIAL	1024	专项直接还款
OPT_FUND_PRICE_BUY	1025	货币基金申购
OPT_FUND_PRICE_SELL	1026	货币基金赎回
OPT_N3B_CALL_AUCTION_BUY	1027	协议转让-集合竞价买入
OPT_N3B_CALL_AUCTION_SELL	1028	协议转让-集合竞价卖出
OPT_N3B_AFTER_HOURS_BUY	1029	全国股转-盘后协议买入
OPT_N3B_AFTER_HOURS_SELL	1030	全国股转-盘后协议卖出
OPT_ETF_HEDGE	1031	ETF套利
OPT_QUOTATION_REPURCHASE_BUY	1032	报价回购买入
OPT_QUOTATION_REPURCHASE_STOP	1033	报价回购终止续做
OPT_QUOTATION_REPURCHASE_BEFORE	1034	报价回购提前购回
OPT_QUOTATION_REPURCHASE_RESERVATION	1035	报价回购购回预约
OPT_QUOTATION_REPURCHASE_CANCEL	1036	报价回购取消预约
OPT_BLOCK_CONFIRM_MATCH_BUY	1037	成交申报配对买入
OPT_BLOCK_CONFIRM_MATCH_SELL	1038	成交申报配对卖出
OPT_FUTURE_OPTION_ABANDON	1039	期货期权放弃行权
OPT_ONEKEY_TRANSFER	1040	一键划转
OPT_ONEKEY_TRANSFER_IN	1041	一键划入
OPT_ONEKEY_TRANSFER_OUT	1042	一键划出
OPT_AFTER_FIX_BUY	1043	盘后定价买入
OPT_AFTER_FIX_SELL	1044	盘后定价卖
OPT_AGREEMENT_REPURCHASE_TRANSACTION_DEC_FORWARD	1045	成交申报正回购
OPT_AGREEMENT_REPURCHASE_TRANSACTION_DEC_REVERSE	1046	成交申报逆回购
OPT_AGREEMENT_REPURCHASE_EXPIRE_CONFIRM	1047	到期确认
OPT_AGREEMENT_REPURCHASE_ADVANCE_REPURCHASE	1048	提前购回正回购
OPT_AGREEMENT_REPURCHASE_ADVANCE_REVERSE	1049	提前购回逆回购
OPT_AGREEMENT_REPURCHASE_EXPIRE_RENEW	1050	到期续做正回购
OPT_AGREEMENT_REPURCHASE_EXPIRE_REVERSE	1051	到期续做逆回购
OPT_TRANSACTION_IN_CASH_BUY	1052	现券买入
OPT_TRANSACTION_IN_CASH_SELL	1053	现券卖出
OPT_OUTRIGHT_REPO_FUND_REPURCHASE	1054	买断式融资回购
OPT_OUTRIGHT_REPO_BOND_REPURCHASE	1055	买断式融券回购
OPT_OUTRIGHT_REPO_BOND_REPAY	1056	买断式融资购回
OPT_OUTRIGHT_REPO_FUND_RETRIEVE	1057	买断式融券购回
OPT_DISTRIBUTION_BUYING	1058	分销买入
OPT_FIXRATE_TO_FLOATINGRATE	1059	固定利率换浮动利率
OPT_FLOATINGRATE_TO_FIXRATE	1060	浮动利率换固定利率
OPT_IBANK_TRANSFER_OUT	1061	银行间转出托管
OPT_IBANK_TRANSFER_IN	1062	银行间转入托管
OPT_AGREEMENT_REPURCHASE_INTENTION_BUY	1063	意向申报正回购买入
OPT_AGREEMENT_REPURCHASE_INTENTION_SELL	1064	意向申报正回购卖出
OPT_AGREEMENT_REPURCHASE_BIZ_APPLY_CONFIRM	1065	协议回购成交申报确认
OPT_AGREEMENT_REPURCHASE_BIZ_APPLY_REJECT	1066	协议回购成交申报拒绝
OPT_AGREEMENT_REPURCHASE_CONTINUE_CONFIRM	1067	协议回购到期续做申报确认
OPT_AGREEMENT_REPURCHASE_CONTINUE_REJECT	1068	协议回购到期续做申报拒绝
OPT_AGREEMENT_REPURCHASE_INTENTION_CHANGE_BONDS	1069	协议回购换券申报
OPT_AGREEMENT_REPURCHASE_INTENTION_CHANGE_BONDS_CONFIRM	1070	协议回购换券申报确认
OPT_AGREEMENT_REPURCHASE_INTENTION_CHANGE_BONDS_REJECT	1071	协议回购换券申报拒绝
OPT_AGREEMENT_REPURCHASE_STOP_AHEAD_CONFIRM	1072	协议回购正回购提前终止申报确认
OPT_AGREEMENT_REPURCHASE_STOP_AHEAD_REJECT	1073	协议回购正回购提前终止申报拒绝
OPT_AGREEMENT_REPURCHASE_RELEASE_PLEDGE	1074	协议回购正回购方解除质押申报
OPT_AGREEMENT_REPURCHASE_RELEASE_PLEDGE_CONFIRM	1075	协议回购正回购解除质押申报确认
OPT_AGREEMENT_REPURCHASE_RELEASE_PLEDGE_REJECT	1076	协议回购正回购解除质押申报拒绝
OPT_AGREEMENT_REPURCHASE_EXPIRE_CONFIRM_SELL	1077	深圳到期确认卖出
OPT_LOAN_DISTRIBUTION_BUY	1078	债券分销
OPT_PREFERENCE_SHARES_BIDDING_BUY	1079	优先股竞价买入
OPT_PREFERENCE_SHARES_BIDDING_SELL	1080	优先股竞价卖出
OPT_TOC_BOND	1081	债券转托管
OPT_TOC_FUND	1082	基金转托管
OPT_IBANK_BORROW	1083	同业拆入
OPT_IBANK_LOAN	1084	同业拆出
OPT_IBANK_BORROW_REPAY	1085	拆入还款
OPT_IBANK_LOAN_REPAY	1086	拆出还款
OPT_FINANCIAL_PRODUCT_BUY	1087	理财产品申购
OPT_FINANCIAL_PRODUCT_SELL	1088	理财产品赎回
OPT_OPTION_COMB_EXERCISE	1089	组合行权
OPT_OPTION_BUILD_COMB_STRATEGY	1090	构建组合策略
OPT_OPTION_RELEASE_COMB_STRATEGY	1091	解除组合策略
OPT_AGREEMENT_REPURCHASE_REVERSE_STOP_AHEAD_CONFIRM	1092	协议回购逆回购提前终止申报确认
OPT_AGREEMENT_REPURCHASE_REVERSE_STOP_AHEAD_REJECT	1093	协议回购逆回购提前终止申报拒绝
OPT_AGREEMENT_REPURCHASE_REVERSE_RELEASE_PLEDGE	1094	协议回购逆回购方解除质押申报
OPT_AGREEMENT_REPURCHASE_REVERSE_RELEASE_PLEDGE_CONFIRM	1095	协议回购逆回购解除质押申报确认
OPT_AGREEMENT_REPURCHASE_REVERSE_RELEASE_PLEDGE_REJECT	1096	协议回购逆回购解除质押申报拒绝
OPT_BOND_TENDER	1097	债券投标
OPT_FINANCIAL_PRODUCT_CALL	1098	理财产品认购
OPT_NEEQ_O3B_CONTINUOUS_AUCTION_BUY	1099	全国股转-北交所买入
OPT_NEEQ_O3B_CONTINUOUS_AUCTION_SELL	1100	全国股转-北交所卖出
OPT_NEEQ_O3B_ASK_PRICE	1101	全国股转-申购-询价申报
OPT_NEEQ_O3B_PRICE_CONFIRM	1102	全国股转-申购-申购申报
OPT_NEEQ_O3B_BLOCKTRADING_BUY	1103	全国股转-大宗交易买入
OPT_NEEQ_O3B_BLOCKTRADING_SELL	1104	全国股转-大宗交易卖出
OPT_LMT_LOAN_SET	1105	转融通非约定出借申报
OPT_LMT_LOAN_CONVENTION	1106	转融通约定出借申报
OPT_LMT_LOAN_RENEWAL	1107	转融通出借展期
OPT_LMT_LOAN_SETTLE_EARLY	1108	转融通出借提前了结
OPT_CROSS_MARKET_IN_ETF_PURCHASE	1109	跨市场ETF场内申购
OPT_CROSS_MARKET_IN_ETF_REDEMPTION	1110	跨市场ETF场内赎回
OPT_CROSS_MARKET_OUT_ETF_PURCHASE	1111	跨市场ETF场外申购
OPT_CROSS_MARKET_OUT_ETF_REDEMPTION	1112	跨市场ETF场外赎回
OPT_CREDIT_APPOINTMENT	1113	券源预约
OPT_OFF_IPO_PUB_PRICE	1114	网下申购-公开发行询价
OPT_OFF_IPO_PUB_PURCHASE	1115	网下申购-公开发行申购
OPT_OFF_IPO_NON_PUB_PRICE	1116	网下申购-非公开发行询价
OPT_OFF_IPO_NON_PUB_PURCHASE	1117	网下申购-非公开发行申购
OPT_IBANK_PUT	1118	债券回售
OPT_IBANK_BOND_BORROW	1119	债券借贷融入
OPT_IBANK_BOND_LEND	1120	债券借贷融出
OPT_IBANK_BOND_BORROW_REPAY	1121	债券借贷融入购回
OPT_IBANK_BOND_LEND_RETRIEVE	1122	债券借贷融出购回
OPT_IBANK_BOND_DISPLACE	1123	债券借贷-质押券置换
OPT_LENDING_INTEGRATE_INTO	1124	融券通-预约融券融入
OPT_LENDING_MELT_OUT	1125	融券通-预约融券融出
OPT_FICC_MANUAL_DECLARE_BUY	1126	固收业务-点击成交-报价申报买入
OPT_FICC_MANUAL_DECLARE_SELL	1127	固收业务-点击成交-报价申报卖出
OPT_FICC_MANUAL_CONFIRM_BUY_CONFIRM	1128	固收业务-点击成交-报价确认-买入-确认
OPT_FICC_MANUAL_CONFIRM_BUY_REJECT	1129	固收业务-点击成交-报价确认-买入-拒绝
OPT_FICC_MANUAL_CONFIRM_SELL_CONFIRM	1130	固收业务-点击成交-报价确认-卖出-确认
OPT_FICC_MANUAL_CONFIRM_SELL_REJECT	1131	固收业务-点击成交-报价确认-卖出-拒绝
OPT_FICC_CONSULT_DECLARE_BUY	1132	固收业务-协商成交-协商申报买入
OPT_FICC_CONSULT_DECLARE_SELL	1133	固收业务-协商成交-协商申报卖出
OPT_FICC_CONSULT_CONFIRM_BUY_CONFIRM	1134	固收业务-协商成交-协商确认-买入-确认
OPT_FICC_CONSULT_CONFIRM_BUY_REJECT	1135	固收业务-协商成交-协商确认-买入-拒绝
OPT_FICC_CONSULT_CONFIRM_SELL_CONFIRM	1136	固收业务-协商成交-协商确认-卖出-确认
OPT_FICC_CONSULT_CONFIRM_SELL_REJECT	1137	固收业务-协商成交-协商确认-卖出-拒绝
OPT_FICC_ENQUIRY_DECLARE_BUY	1138	固收业务-询价成交-询价申报买入
OPT_FICC_ENQUIRY_DECLARE_SELL	1139	固收业务-询价成交-询价申报卖出
OPT_FICC_ENQUIRY_REPLAY_BUY_CONFIRM	1140	固收业务-询价成交-报价回复-买入-确认
OPT_FICC_ENQUIRY_REPLAY_BUY_REJECT	1141	固收业务-询价成交-报价回复-买入-拒绝--预留字段
OPT_FICC_ENQUIRY_REPLAY_SELL_CONFIRM	1142	固收业务-询价成交-报价回复-卖出-确认
OPT_FICC_ENQUIRY_REPLAY_SELL_REJECT	1143	固收业务-询价成交-报价回复-卖出-拒绝--预留字段
OPT_FICC_ENQUIRY_INQUIRY_BUY_CONFIRM	1144	固收业务-询价成交-询价成交-买入-确认
OPT_FICC_ENQUIRY_INQUIRY_BUY_REJECT	1145	固收业务-询价成交-询价成交-买入-拒绝--预留字段
OPT_FICC_ENQUIRY_INQUIRY_SELL_CONFIRM	1146	固收业务-竞买成交-询价成交-卖出-确认
OPT_FICC_ENQUIRY_INQUIRY_SELL_REJECT	1147	固收业务-竞买成交-询价成交-卖出-拒绝--预留字段
OPT_FICC_BINDDING_RESERVE_BUY	1148	固收业务-竞买成交-竞买预约买入
OPT_FICC_BINDDING_RESERVE_SELL	1149	固收业务-竞买成交-竞买预约卖出
OPT_FICC_BINDDING_DECLARE_BUY	1150	固收业务-竞买成交-竞买申报买入
OPT_FICC_BINDDING_DECLARE_SELL	1151	固收业务-竞买成交-竞买申报卖出
OPT_FICC_BINDDING_PRICE_DECLARE_BUY	1152	固收业务-竞买成交-应价申报买入
OPT_FICC_BINDDING_PRICE_DECLARE_SELL	1153	固收业务-竞买成交-应价申报卖出
OPT_OPTION_BUY_CLOSE_THEN_OPEN	1154	买入优先平仓，个股期权交易业务补充类型
OPT_OPTION_SELL_CLOSE_THEN_OPEN	1155	卖出优先平仓
OPT_FUND_TRANSFER_IN	1156	资金划入
OPT_FUND_TRANSFER_OUT	1157	资金划出
enum_EOrderType - 算法交易、普通交易类型
变量名称	数值	描述
OTP_ORDINARY	0	常规
OTP_ALGORITHM	1	算法交易
OTP_RANDVOLUME	2	随机量交易
OTP_ALGORITHM3	3	算法交易3
OTP_ZXJT	4	中信建投算法
OTP_ZSGS	5	隔时交易
OTP_ORDINARY_BASKET_TRIGGER_SINGLE_ORDER	6	普通交易的触价单笔委托方式
OTP_ALGORITHM_BASKET_TRIGGER_SINGLE_ORDER	7	算法交易的触价单笔委托方式
OTP_ZXZQ	8	中信证券算法
OTP_GENUS	9	金纳算法
OTP_JAZZ	10	爵士算法
OTP_VWAP	11	智能VWAP
OTP_TWAP	12	智能TWAP
OTP_XTALGO	13	智能算法
OTP_HUACHUANG	14	华创算法
OTP_HUARUN	15	华润算法
OTP_CUSTOM	16	回转算法
OPT_EXTERN	17	主动算法
OTP_GUANGFA	18	广发算法
enum_EPriceType - 价格类型
变量名称	数值	描述
PRTP_SALE5	0	卖5
PRTP_SALE4	1	卖4
PRTP_SALE3	2	卖3
PRTP_SALE2	3	卖2
PRTP_SALE1	4	卖1
PRTP_LATEST	5	最新价
PRTP_BUY1	6	买1
PRTP_BUY2	7	买2
PRTP_BUY3	8	买3
PRTP_BUY4	9	买4
PRTP_BUY5	10	买5
PRTP_FIX	11	指定价
PRTP_MARKET	12	市价_涨跌停价
PRTP_HANG	13	挂单价
PRTP_COMPETE	14	对手价
PRTP_AUTO	15	自动盘口
PRTP_CLOSE	16	昨收价
PRTP_AVERAGE	17	大宗加权平均价
PRTP_MARKET_BEST	18	市价_最优价
PRTP_MARKET_CANCEL	19	市价_即成剩撤
PRTP_MARKET_CANCEL_ALL	20	市价_全额成交或撤
PRTP_MARKET_CANCEL_1	21	市价_最优1档即成剩撤
PRTP_MARKET_CANCEL_5	22	市价_最优5档即成剩撤
PRTP_MARKET_CONVERT_1	23	市价_最优1档即成剩转
PRTP_MARKET_CONVERT_5	24	市价_最优5档即成剩转
PRTP_STK_OPTION_ASK	25	询价
PRTP_STK_OPTION_FIX_CANCEL_ALL	26	限价即时全部成交否则撤单
PRTP_STK_OPTION_MARKET_CACEL_LEFT	27	市价即时成交剩余撤单
PRTP_STK_OPTION_MARKET_CANCEL_ALL	28	市价即时全部成交否则撤单
PRTP_STK_OPTION_MARKET_CONVERT_FIX	29	市价剩余转限价
PRTP_SALE6	30	卖6
PRTP_SALE7	31	卖7
PRTP_SALE8	32	卖8
PRTP_SALE9	33	卖9
PRTP_SALE10	34	卖10
PRTP_BUY6	35	买6
PRTP_BUY7	36	买7
PRTP_BUY8	37	买8
PRTP_BUY9	38	买9
PRTP_BUY10	39	买10
PRTP_UPPER_LIMIT_PRICE	40	涨停价
PRTP_LOWER_LIMIT_PRICE	41	跌停价
PRTP_MARKET_SH_CONVERT_5_CANCEL	42	最优五档即时成交剩余撤销
PRTP_MARKET_SH_CONVERT_5_LIMIT	43	最优五档即时成交剩转限价
PRTP_MARKET_PEER_PRICE_FIRST	44	对手方最优价格委托
PRTP_MARKET_MINE_PRICE_FIRST	45	本方最优价格委托
PRTP_MARKET_SZ_INSTBUSI_RESTCANCEL	46	即时成交剩余撤销委托
PRTP_MARKET_SZ_CONVERT_5_CANCEL	47	最优五档即时成交剩余撤销委托
PRTP_MARKET_SZ_FULL_REAL_CANCEL	48	全额成交或撤销委托
PRTP_AFTER_FIX_PRICE	49	盘后定价申报
enum_ETaskStatus - 任务状态
变量名称	数值	描述
TASK_STATUS_UNKNOWN	0	未知
TASK_STATUS_WAITING	1	等待
TASK_STATUS_COMMITING	2	提交中
TASK_STATUS_RUNNING	3	执行中
TASK_STATUS_PAUSE	4	暂停
TASK_STATUS_CANCELING_DEPRECATED	5	撤销中（已弃用）
TASK_STATUS_EXCEPTION_CANCELING_DEPRECATED	6	异常撤销中（已弃用）
TASK_STATUS_COMPLETED	7	完成
TASK_STATUS_CANCELED	8	已撤
TASK_STATUS_REJECTED	9	打回
TASK_STATUS_EXCEPTION_CANCELED	10	异常终止
TASK_STATUS_DROPPED	11	放弃（用于组合交易中，放弃补单）
TASK_STATUS_FORCE_CANCELED_DEPRECATED	12	强制终止（已弃用）
