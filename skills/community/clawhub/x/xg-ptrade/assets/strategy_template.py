
"""
策略名称：
三因子日线交易策略
运行周期:
日线
策略流程：
盘前将中小板成分股中st、停牌、退市的股票过滤得到股票池
盘中：
1、获取市场风险溢价、市值因子、账面市值比因子三因子数据，
2、分组差值做线性回归处理，最终得到得分，选择得分高的标的调仓买入
3、每15天换仓一次
注意事项：
策略中调用的order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
# 导入函数库
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
from decimal import Decimal


# 初始化此策略
def initialize(context):
    g.factor_params_info = {
        'total_shareholder_equity': ['balance_statement', 'total_shareholder_equity'],
        'roe': ['profit_ability', 'roe']
    }
    set_params()  # 设置策参数
    set_variables()  # 设置中间变量
    if not is_trade():
        set_backtest()  # 设置回测条件


# 设置策参数
def set_params():
    g.tc = 15  # 调仓频率
    g.yb = 63  # 样本长度
    g.N = 10  # 持仓数目
    g.NoF = 3  # 三因子模型


# 设置中间变量
def set_variables():
    g.t = 0  # 记录连续回测天数
    g.rf = 0.04  # 无风险利率
    g.if_trade = False  # 当天是否交易


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')


# 每天盘前处理
def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # 2005-06-01前回测由于数据不足，不执行。
    if g.current_date < '20050601':
        g.trade_flag = False
    else:
        g.trade_flag = True

    g.rf = 0.04
    g.all_stocks = get_index_stocks('000300.XBHS', g.current_date)

    if g.t % g.tc == 0:
        # 每隔g.tc天，交易一次
        g.if_trade = True
        # 将ST、停牌、退市三种状态的股票剔除当日的股票池
        g.all_stocks = filter_stock_by_status(g.all_stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
    g.t += 1


# 每天交易时要做的事情
def handle_data(context, data):
    if not g.trade_flag:
        return

    if g.if_trade:
        df_scores = get_scores(g.all_stocks, str(get_trading_day(-63)), str(get_trading_day(-1)), g.rf)
        # 为每个持仓股票分配资金
        # 依打分排序，当前需要持仓的股票
        if df_scores.empty:
            stock_sort = list()
        else:
            stock_sort = df_scores.sort_values('score')['code'].tolist()
        # 把涨停状态的股票剔除
        up_limit_stock = get_limit_stock(stock_sort)['up_limit']
        # stock_sort = list(set(stock_sort)-set(up_limit_stock))
        stock_sort = [stock for stock in stock_sort if stock not in up_limit_stock]
        position_list = get_position_list(context)
        # 持仓中跌停的股票不做卖出
        limit_info = get_limit_stock(position_list)
        hold_down_limit_stock = limit_info['down_limit']
        log.info('持仓跌停股：%s' % hold_down_limit_stock)
        position_list = get_position_list(context)
        # 持仓中除了不处于前g.N且跌停不能卖的股票进行卖出
        sell_stocks = list(set(position_list) - set(stock_sort[:g.N]) - set(hold_down_limit_stock))
        # 对不在换仓列表中且飞跌停股的股票进行卖出操作
        order_stock_sell(sell_stocks)
        # 获取仍在持仓中的股票
        position_list = get_position_list(context)
        # 获取调仓买入的股票
        buy_stocks = [stock for stock in stock_sort if stock not in position_list][:(g.N - len(position_list))]
        # 仓位动态平衡的股票
        balance_stocks = list(set(buy_stocks + position_list) - set(hold_down_limit_stock))
        every_stock = context.portfolio.portfolio_value / g.N
        order_stock_balance(balance_stocks, every_stock)
        order_stock_balance(balance_stocks, every_stock)
    g.if_trade = False


# 不在换仓目标中且没有跌停的股票进行清仓操作
def order_stock_sell(sell_stocks):
    # 对于不需要持仓的股票，全仓卖出
    for stock in sell_stocks:
        order_target_value(stock, 0)


# 非跌停的换仓目标股进行仓位再平衡
def order_stock_balance(balance_stocks, every_stock):
    for stock in balance_stocks:
        order_target_value(stock, every_stock)


# 获取综合得分
def get_scores(stocks, begin, end, rf):
    try:
        length = len(stocks)
        market_cap_df = get_fundamentals(stocks, 'valuation', fields='total_value', date=begin)
        market_cap_df.dropna(inplace=True)
        if market_cap_df.empty:
            print('获取市值数据失败，股票因子评分失败')
            return pd.DataFrame()
        total_shareholder_equity_df = get_factor_values(stocks, 'total_shareholder_equity', begin, g.factor_params_info)
        total_shareholder_equity_df.dropna(inplace=True)
        if total_shareholder_equity_df.empty:
            print('获取total_shareholder_equity财务数据失败，股票因子评分失败')
            return pd.DataFrame()
        roe_df = get_factor_values(stocks, 'roe', begin, g.factor_params_info)
        roe_df.dropna(inplace=True)
        if roe_df.empty:
            print('获取roe财务数据失败，股票因子评分失败')
            return pd.DataFrame()
        df_all = pd.concat([market_cap_df, total_shareholder_equity_df, roe_df], axis=1)
        df_all.dropna(inplace=True)
        df_all['BTM'] = df_all['total_shareholder_equity'] / df_all['total_value']
        df_all = df_all.reset_index()
        S = df_all.sort_values('total_value')['index'][:int(length / 3)]
        B = df_all.sort_values('total_value')['index'][length - int(length / 3):]
        L = df_all.sort_values('BTM')['index'][:int(length / 3)]
        H = df_all.sort_values('BTM')['index'][length - int(length / 3):]
        W = df_all.sort_values('roe')['index'][:int(length / 3)]
        R = df_all.sort_values('roe')['index'][length - int(length / 3):]

        close_data = get_price(stocks, begin, end, fields='close', frequency='1d', is_dict=True)

        close_df = pd.DataFrame()
        for stock_code, stock_data in close_data.items():
            date_info = pd.to_datetime(stock_data['datetime'], format='%Y%m%d')
            close_info = stock_data['close']
            close_df[stock_code] = pd.Series(close_info, index=date_info)
        close_df.sort_index(inplace=True)
        df = np.diff(np.log(close_df), axis=0) + 0 * close_df[1:]
        SMB = df[S].T.sum() / len(S) - df[B].T.sum() / len(B)
        HML = df[H].T.sum() / len(H) - df[L].T.sum() / len(L)
        RMW = df[R].T.sum() / len(R) - df[W].T.sum() / len(W)
        dp = get_price('000300.XSHG', begin, end, '1d')['close']
        if len(dp)-len(df)>1:
            log.info('历史行情数据缺失，股票因子评分失败')
            return pd.DataFrame()
        RM = np.diff(np.log(dp)) - rf / 252
        X = pd.DataFrame({"RM": RM, "SMB": SMB, "HML": HML, "RMW": RMW})
        factor_flag = ["RM", "SMB", "HML", "RMW"][:g.NoF]
        X = X[factor_flag]
        t_scores = [0.0] * length
        for i in range(length):
            t_stock = stocks[i]
            t_r = linreg(X, df[t_stock] - rf / 252, len(factor_flag))
            t_scores[i] = t_r[0]
        scores = pd.DataFrame({'code': stocks, 'score': t_scores})
        df_scores = scores.sort_values(by='score')
        return df_scores
    except:
        print('股票因子评分失败，请检查数据')
        return pd.DataFrame()


# 获取因子值
def get_factor_values(stock_list, factor, date, factor_params_info):
    """
    获取因子值方法
    入参：
    1、股票池：stock_list
    2、因子名称：factor
    3、计算日期：date
    4、因子数据获取需要维护的信息（因子名称、表名、字段名）
    """
    data = get_fundamentals(stock_list, table=factor_params_info[factor][0], fields=factor_params_info[factor][1],
                            date=date, is_dataframe=True)
    factor_info = {}
    for stock in stock_list.copy():
        if stock not in data.index:
            continue
        factor_info[stock] = data.loc[stock, factor_params_info[factor][1]]
    if factor_info == {}:
        return pd.DataFrame()
    factor_df = pd.DataFrame.from_dict(factor_info, orient='index')
    factor_df.columns = [factor_params_info[factor][1]]
    return factor_df


# 线性回归
def linreg(x, y, columns=3):
    x = sm.add_constant(np.array(x))
    y = np.array(y)
    if len(y) > 1:
        results = regression.linear_model.OLS(y, x).fit()
        return results.params
    else:
        return [float("nan")] * (columns + 1)


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 生成昨日持仓股票列表
def get_position_list(context):
    return [
        position.sid
        for position in context.portfolio.positions.values()
        if position.amount != 0
    ]


# 日级别回测获取持仓中不能卖出的股票(涨停就不卖出)
def get_limit_stock(stock_list):
    out_info = {'up_limit': [], 'down_limit': []}
    for stock in stock_list:
        limit_status = check_limit(stock)[stock]
        if limit_status == 1:
            out_info['up_limit'].append(stock)
        elif limit_status == -1:
            out_info['down_limit'].append(stock)
    return out_info
################################
"""
策略名称：
指数增强日线交易策略
策略流程：
盘前：
1、将沪深300成分股中st、停牌、退市的股票过滤得到股票池
2、示例用roe作为单因子选出排名第一档的股票作为目标股票池
盘中：
1、财报调仓日或者固定间隔调仓日通过线性规划的方法进行调仓，以图实现增强效果
注意事项：
策略中调用的order_target、order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
from decimal import Decimal
import datetime
from datetime import date as justdate
from scipy.optimize import minimize


# 初始化
def initialize(context):
    g.factor = 'roe'
    g.factor_params_info = {'roe': ['profit_ability', 'roe', False],  # 净资产收益率,最后布尔值为排序方式
                            'operating_revenue_grow': ['growth_ability', 'operating_revenue_grow_rate', False],  # 营收增速
                            'net_profit_grow': ['growth_ability', 'np_parent_company_cut_yoy', False],  # 扣非净利润增速
                            }
    set_params()  # 设置策参数
    set_variables()  # 设置中间变量
    is_trade_flag = is_trade()
    if is_trade_flag:
        pass
    else:
        set_backtest()  # 设置回测条件


# 设置策参数
def set_params():
    g.percent = 0.10
    g.est_interval = 80  # 记录优化区间，使用二次规划根据这个区间最优化权重
    g.lamda = 0
    g.hold_days = 60
    g.max_hold_num = 20  # 最大持仓的股票
    g.run_days = 0
    g.benchmark = '000300.SS'
    # 财报季度调仓所依据的指定日期
    g.finance_update_date_list = ['0401', '0801', '1001']


# 设置中间变量
def set_variables():
    g.init_screen = True
    g.is_update_stocks = False


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')  # 回测撮合不限制成交量


# 盘前处理
def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime('%Y%m%d')
    # 2008-01-01前回测由于数据不足，不执行。
    if g.current_date < '20080101':
        g.trade_flag = False
    else:
        g.trade_flag = True
    if not g.trade_flag:
        return
    g.everyStock = 0
    if is_pub_date(g.current_date):  # 财报调仓日
        g.stocks = create_stocks()
        g.is_update_stocks = True
    elif g.init_screen:
        '''初始化一个组合，这一小段代码只会用一次'''
        g.stocks = create_stocks()
        g.is_update_stocks = True
        g.init_screen = False  # 将Flag置为False，保证下次不再运行


# 每天交易时要做的事情
def handle_data(context, data):
    if not g.trade_flag:
        return
    # 如果到公告日更新了调仓
    if g.is_update_stocks:
        stock_sort = g.stocks
        log.info('初始日或调仓日股票池')
        log.info(stock_sort)
        if not stock_sort:
            return
        previous_date = get_trading_day(-1)
        # 通过二次规划确定权重
        weight = get_weights(stock_sort, previous_date)
        stock_weight = dict(zip(stock_sort, weight))
        stocks = stock_sort
        current_hold_set = set(context.portfolio.positions.keys())
        if set(stocks) != current_hold_set:
            need_buy = set(stocks).difference(current_hold_set)
            need_sell = current_hold_set.difference(stocks)
            current_stocks = set(stocks).difference(need_buy)
            try:
                for stock in need_sell:
                    order_target(stock, 0)
                for stock in need_buy:
                    order_value(stock, context.portfolio.portfolio_value * stock_weight[stock])
                for stock in current_stocks:
                    order_target_value(stock, context.portfolio.portfolio_value * stock_weight[stock])
            except:
                pass
        g.is_update_stocks = False
        g.run_days = 0

    elif g.run_days % g.hold_days == 0:
        stocks = g.stocks
        log.info('非调仓日股票池')
        log.info(stocks)
        if not stocks:
            return
        '''这里的权重通过二次规划确定'''
        weight = get_weights(stocks, context.previous_date)
        stock_weight = dict(zip(stocks, weight))
        try:
            for stock in stocks:
                order_target_value(stock, context.portfolio.portfolio_value * stock_weight[stock])
        except:
            pass
    if context.portfolio.cash > 0:
        # 如果可用资金大于0，说明没有全仓，就是撮合单的时候出问题，所以需要重新买入，这时候重新全仓买入几个ETF
        log.info('尝试把剩余资金用完，买入ETF')
        cash = context.portfolio.cash
        order_value('510300.SS', cash / 10 * 4)
        order_value('510330.SS', cash / 10 * 3)
        order_value('510500.SS', cash / 10 * 3)
    g.run_days += 1


# 建立股票池
def create_stocks():
    g.all_stocks = get_index_stocks('000300.XBHS', g.current_date)
    for stock in g.all_stocks.copy():
        if stock[:3] == '688':
            g.all_stocks.remove(stock)
    # 将ST、停牌、退市三种状态的股票剔除当日的股票池
    g.all_stocks = filter_stock_by_status(g.all_stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
    return get_stocks(g.all_stocks, str(get_trading_day(-1)), g.factor)


# 获取拟持仓股票池
def get_stocks(stocks, date, factor):
    sort_type = g.factor_params_info[factor][-1]
    df = get_factor_values(stocks, factor, date, g.factor_params_info)
    df.dropna(inplace=True)
    if df.empty:
        print('%s数据获取失败，选股失败' % factor)
        return list()
    # 3倍标准差去极值
    df = winsorize(df, factor, std=3, have_negative=True)
    # z标准化
    df = standardize(df, factor, ty=2)
    # 市值中性化
    market_cap_df = get_fundamentals(stocks, 'valuation', fields='total_value', date=date)
    market_cap_df = market_cap_df[['total_value']]
    market_cap_df.dropna(inplace=True)
    if market_cap_df.empty:
        print('市值数据获取失败，选股失败')
        return list()
    df = neutralization(df, factor, market_cap_df)
    df = df.sort_values(by=factor, ascending=sort_type)
    return list(df.head(int(len(df) * g.percent)).index)


# 获取因子值
def get_factor_values(stock_list, factor, date, factor_params_info):
    """
    获取因子值方法
    入参：
    1、股票池：stock_list
    2、因子名称：factor
    3、计算日期：date
    4、因子数据获取需要维护的信息（因子名称、表名、字段名）
    """
    data = get_fundamentals(stock_list, table=factor_params_info[factor][0], fields=factor_params_info[factor][1],
                            date=date, is_dataframe=True)
    factor_info = {}
    for stock in stock_list.copy():
        if stock not in data.index:
            continue
        factor_info[stock] = data.loc[stock, factor_params_info[factor][1]]
    if factor_info == {}:
        return pd.DataFrame()
    factor_df = pd.DataFrame.from_dict(factor_info, orient='index')
    factor_df.columns = [factor_params_info[factor][1]]
    return factor_df


# 使用二次规划确定权重  
def get_weights(stocks, date):
    date = date.strftime('%Y-%m-%d')
    start_date = get_trading_day(-(g.est_interval + 1)).strftime('%Y-%m-%d')
    price_data = get_price(stocks, start_date=start_date, end_date=date, frequency='daily',
                           fields=['close'], is_dict=True)
    
    close_df = pd.DataFrame()
    for stock_code, stock_data in price_data.items():
        date_info = pd.to_datetime(stock_data['datetime'], format='%Y%m%d')
        close_info = stock_data['close']
        close_df[stock_code] = pd.Series(close_info, index=date_info)
    close_df.sort_index(inplace=True)    

    code_list = list(close_df.columns)
    df_list = []
    for stock in code_list:
        df = close_df[[stock]]
        df['change'] = 0 
        df['change'] = df[stock] / df[stock].shift(1) - 1
        df[stock] = df['change']
        df = df[[stock]]
        df.fillna(0, inplace=True)
        df_list.append(df)

    result = pd.concat(df_list, axis=1)
    index_price = get_price(g.benchmark, start_date=start_date, end_date=date, frequency='daily',
                            fields=['close'], is_dict=False)
    index_r = index_price.pct_change()
    index_r.fillna(0, inplace=True)
    weight = calculate_weight(np.array(result), np.array(index_r))
    return weight


def calculate_weight(train_returns, target_returns):
    length = len(train_returns.T)

    # 定义二次线性规划目标函数
    def objective(weights):
        return np.sum((np.dot(train_returns, weights) - target_returns) ** 2)

    # 定义约束条件
    constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                   {'type': 'ineq', 'fun': lambda weights: 0.2 - np.max(weights)}
                   ]
    # 定义权重的取值范围（可以设置最小权重和最大权重区间）
    min_weight = (1 / length) * 0.2  # 最小权重
    max_weight = (1 / length) * 5  # 最大权重
    bounds = [(min_weight, max_weight)] * train_returns.shape[1]
    # 初始化权重
    initial_weights = np.ones(train_returns.shape[1]) / train_returns.shape[1]
    # 最小化目标函数，求解权重
    result = minimize(objective, initial_weights, constraints=constraints, bounds=bounds)
    # 输出结果
    test_weights = result.x
    # print("测试集投资权重：", test_weights)
    return test_weights


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 去极值函数（3倍标准差去极值）
def winsorize(factor_data, factor, std=3, have_negative=True):
    """
    去极值函数
    factor:以股票code为index，因子值为value的Series
    std为几倍的标准差，have_negative 为布尔值，是否包括负值
    输出Series
    """
    r = factor_data[factor]
    if not have_negative:
        r = r[r >= 0]
    # 取极值
    edge_up = r.mean() + std * r.std()
    edge_low = r.mean() - std * r.std()
    r[r > edge_up] = edge_up
    r[r < edge_low] = edge_low
    r = pd.DataFrame(r)
    return r


# z－score标准化函数：
def standardize(factor_data, factor, ty=2):
    """
    s为Series数据
    ty为标准化类型:1 MinMax,2 Standard,3 maxabs
    """
    temp = factor_data[factor]
    re = 0
    if int(ty) == 1:
        re = (temp - temp.min()) / (temp.max() - temp.min())
    elif ty == 2:
        re = (temp - temp.mean()) / temp.std()
    elif ty == 3:
        re = temp / 10 ** np.ceil(np.log10(temp.abs().max()))
    return pd.DataFrame(re)


# 市值中性化函数
def neutralization(data_factor, factor, data_market_cap):
    data_market_cap['total_value2'] = 0
    data_market_cap['total_value2'] = data_market_cap['total_value'].apply(lambda a: math.log(a))
    df = pd.concat([data_factor, data_market_cap], axis=1, join='inner')
    y = df[factor]
    x = df['total_value2']
    result = sm.OLS(y, x).fit()
    result = pd.DataFrame(result.resid)
    result.columns = [factor]
    return result


# 判断当天时间是不是出财报的下一天时间
def is_pub_date(current_date):
    cur_year = current_date[:4]
    trade_dates = []
    # 按季度选股，在4.30、8.31、10.31三个时间日重新根据财务报表选择股票
    for date in g.finance_update_date_list:
        trade_dates.append(get_trading_day_by_date(cur_year+date, day=0))
    if current_date in trade_dates:
        return True
    return False
######################################
"""
策略名称：
AROON指标策略
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import talib as ta


# 初始化
def initialize(context):
    g.stock = "000333.SZ"
    g.period = 20


# 每个交易日处理
def before_trading_start(context, data):
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    # 2013-10-01前回测由于数据不足，不执行。
    if current_date < '2013-10-01':
        g.trade_flag = False
    else:
        g.trade_flag = True


def handle_data(context, data):
    if not g.trade_flag:
        return
    log.info(g.stock + '当前持仓' + str(get_position(g.stock).amount))
    high = get_history(g.period * 2, frequency='1d', field='high', security_list=g.stock, fq='pre', is_dict=True)
    low = get_history(g.period * 2, frequency='1d', field='low', security_list=g.stock, fq='pre', is_dict=True)
    # 通过talib库计算AROON指标值   
    aroon_down, aroon_up = ta.AROON(high[g.stock]['high'], low[g.stock]['low'], g.period)
    aroon = aroon_up - aroon_down
    signal = 0
    if aroon_up[-2] < 70 <= aroon_up[-1] and aroon[-1] > 0:
        signal += 1
    if aroon_down[-2] < 70 <= aroon_down[-1] and aroon[-1] < 0:
        signal += -1
    if aroon_up[-2] > 50 >= aroon_up[-1] and aroon[-1] < 0:
        signal += -1
    if aroon_down[-2] > 50 >= aroon_down[-1] and aroon[-1] > 0:
        signal += 1
    if signal > 0 and get_position(g.stock).amount == 0:
        order_value(g.stock, context.portfolio.cash)
    if signal < 0 < get_position(g.stock).amount:
        order_target(g.stock, 0)
########################################
"""
策略名称：
单因子日线交易策略
策略流程：
盘前将中小板成分股中st、停牌、退市的股票过滤得到股票池
盘中：
1、通过极值处理、标准化处理、市值中性化处理
2、因子排序获得股票池
3、动态平衡仓位
注意事项：
策略中调用的order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
from decimal import Decimal


# 初始化处理
def initialize(context):
    g.factor = 'roe'
    g.factor_params_info = {
        'roe': ['profit_ability', 'roe', False],  # 净资产收益率,最后布尔值为排序方式
        'operating_revenue_grow_rate': ['growth_ability', 'operating_revenue_grow_rate', False],
        # 营收增速
        'np_parent_company_cut_yoy': ['growth_ability', 'np_parent_company_cut_yoy', False],
        # 扣非净利润增速
    }
    # 初始化此策略
    set_params()  # 设置策参数
    set_variables()  # 设置中间变量
    if not is_trade():
        set_backtest()  # 设置回测条件


# 设置策参数
def set_params():
    g.tc = 15  # 调仓频率
    g.yb = 63  # 样本长度
    g.N = 20  # 持仓数目
    g.NoF = 3  # 三因子模型
    g.percent = 0.10


# 设置中间变量
def set_variables():
    g.days = 0  # 记录连续回测天数
    g.rf = 0.04  # 无风险利率
    g.is_trade = False  # 当天是否交易
    g.every_stock = 0


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')


# 盘前处理
def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # g.all_stocks = get_index_stocks('000906.XBHS', g.current_date)
    g.all_stocks = get_index_stocks('000300.XBHS', g.current_date)
    if g.days % g.tc == 0:
        # 每g.tc天，交易一次行
        g.is_trade = True
        # 将ST、停牌、退市三种状态的股票剔除当日的股票池
        g.all_stocks = filter_stock_by_status(g.all_stocks, filter_type=["ST", "HALT", "DELISTING"], query_date=None)
    g.days += 1


# 每天交易时要做的事情
def handle_data(context, data):
    if g.is_trade:
        stock_sort = get_stocks(g.all_stocks, str(get_trading_day(-1)), g.factor)
        # 把涨停状态的股票剔除
        up_limit_stock = get_limit_stock(context, stock_sort)['up_limit']
        stock_sort = [stock for stock in stock_sort if stock not in up_limit_stock]
        position_list = get_position_list(context)
        # 持仓中跌停的股票不做卖出
        limit_info = get_limit_stock(context, position_list)
        hold_down_limit_stock = limit_info['down_limit']
        log.info('持仓跌停股：%s' % hold_down_limit_stock)
        # 持仓中除了不处于前g.N且跌停不能卖的股票进行卖出
        sell_stocks = list(set(position_list) - set(stock_sort[:g.N]) - set(hold_down_limit_stock))
        # 对不在换仓列表中且飞跌停股的股票进行卖出操作
        order_stock_sell(context, data, sell_stocks)
        # 获取仍在持仓中的股票
        position_list = get_position_list(context)
        # 获取调仓买入的股票
        buy_stocks = [stock for stock in stock_sort if stock not in position_list][:(g.N - len(position_list))]
        # 仓位动态平衡的股票
        balance_stocks = list(set(buy_stocks + position_list) - set(hold_down_limit_stock))
        log.info('balance_stocks%s' % len(balance_stocks))
        g.every_stock = context.portfolio.portfolio_value / g.N
        log.info('g.every_stock%s' % g.every_stock)
        order_stock_balance(context, data, balance_stocks)
        order_stock_balance(context, data, balance_stocks)
    g.is_trade = False


# 不在换仓目标中且没有跌停的股票进行清仓操作
def order_stock_sell(context, data, sell_stocks):
    # 对于不需要持仓的股票，全仓卖出
    for stock in sell_stocks:
        stock_sell = stock
        order_target_value(stock_sell, 0)


# 非跌停的换仓目标股进行仓位再平衡
def order_stock_balance(context, data, balance_stocks):
    for stock in balance_stocks:
        order_target_value(stock, g.every_stock)


# 获取拟持仓股票池
def get_stocks(stocks, date, factor):
    sort_type = g.factor_params_info[factor][-1]
    df = get_factor_values(stocks, factor, date, g.factor_params_info)
    df.dropna(inplace=True)
    if df.empty:
        print('%s数据获取失败，选股失败' % factor)
        return list()
    # 3倍标准差去极值
    df = winsorize(df, factor, std=3, have_negative=True)
    # z标准化
    df = standardize(df, factor, ty=2)
    # 市值中性化
    market_cap_df = get_fundamentals(stocks, 'valuation', fields='total_value', date=date)
    market_cap_df.dropna(inplace=True)
    if market_cap_df.empty:
        print('市值数据获取失败，选股失败')
        return list()
    market_cap_df = market_cap_df[['total_value']]
    # 中性化处理
    df = neutralization(df, factor, market_cap_df)
    df = df.sort_values(by=factor, ascending=sort_type)
    return list(df.head(int(len(df) * g.percent)).index)


# 获取因子值
def get_factor_values(stock_list, factor, date, factor_params_info):
    """
    获取因子值方法
    入参：
    1、股票池：stock_list
    2、因子名称：factor
    3、计算日期：date
    4、因子数据获取需要维护的信息（因子名称、表名、字段名）
    """
    data = get_fundamentals(stock_list, table=factor_params_info[factor][0], fields=factor_params_info[factor][1],
                            date=date, is_dataframe=True)
    factor_info = {}
    for stock in stock_list.copy():
        if stock not in data.index:
            continue
        factor_info[stock] = data.loc[stock, factor_params_info[factor][1]]
    if factor_info == {}:
        return pd.DataFrame()
    factor_df = pd.DataFrame.from_dict(factor_info, orient='index')
    factor_df.columns = [factor_params_info[factor][1]]
    return factor_df


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 生成昨日持仓股票列表
def get_position_list(context):
    position_last_list = [
        position.sid
        for position in context.portfolio.positions.values()
        if position.amount != 0
    ]
    return position_last_list


# 日级别回测获取持仓中不能卖出的股票(涨停就不卖出)
def get_limit_stock(context, stock_list):
    out_info = {'up_limit': [], 'down_limit': []}
    for stock in stock_list:
        limit_status = check_limit(stock)[stock]
        if limit_status == 1:
            out_info['up_limit'].append(stock)
        elif limit_status == -1:
            out_info['down_limit'].append(stock)
    return out_info


# 去极值函数（3倍标准差去极值）
def winsorize(factor_data, factor, std=3, have_negative=True):
    """
    去极值函数
    factor:以股票code为index，因子值为value的Series
    std为几倍的标准差，have_negative 为布尔值，是否包括负值
    输出Series
    """
    r = factor_data[factor]
    if not have_negative:
        r = r[r >= 0]
    # 取极值
    edge_up = r.mean() + std * r.std()
    edge_low = r.mean() - std * r.std()
    r[r > edge_up] = edge_up
    r[r < edge_low] = edge_low
    r = pd.DataFrame(r)
    return r


# z－score标准化函数：
def standardize(factor_data, factor, ty=2):
    """
    s为Series数据
    ty为标准化类型:1 MinMax,2 Standard,3 maxabs
    """
    temp = factor_data[factor]
    re = 0
    if int(ty) == 1:
        re = (temp - temp.min()) / (temp.max() - temp.min())
    elif ty == 2:
        re = (temp - temp.mean()) / temp.std()
    elif ty == 3:
        re = temp / 10 ** np.ceil(np.log10(temp.abs().max()))
    return pd.DataFrame(re)


# 市值中性化函数
def neutralization(data_factor, factor, data_market_cap):
    data_market_cap['total_value2'] = 0
    data_market_cap['total_value2'] = data_market_cap['total_value'].apply(lambda a: math.log(a))
    df = pd.concat([data_factor, data_market_cap], axis=1, join='inner')
    y = df[factor]
    x = df['total_value2']
    result = sm.OLS(y, x).fit()
    result = pd.DataFrame(result.resid)
    result.columns = [g.factor]
    return result
##########################################
"""
策略名称：
二八轮动策略
运行周期:
日线
策略流程：
策略通过计算沪深300、中证500的阶段动量数据，来决定持有沪深300ETF还是中证500ETF还是货币基金
持有至少10天
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""


# 初始化
def initialize(context):
    set_params()
    g.signal = 0
    g.open_date = get_trading_day(-40)
    # 基金池: 沪深300，中证500，货币基金
    g.fund_list = ['000300.SS', '510300.SS',
                   '000905.SS', '510500.SS',
                   '511880.SS', '511880.SS']

    if not is_trade():
        set_backtest()  # 设置回测条件


# 设置策略参数
def set_params():
    g.N = 20  # N日涨幅
    g.holding_days = 10  # 至少持有天数（交易日）
    g.rise_threshold = 0  # 涨幅阈值


# 设置回测条件
def set_backtest():
    set_limit_mode('UNLIMITED')
    set_commission(commission_ratio=0.00015, min_commission=5.0)


def before_trading_start(context, data):
    current_date = context.blotter.current_dt.strftime('%Y%m%d')
    # 2005-05-01前回测由于数据不足，不执行。
    if current_date < '20050501':
        g.trade_flag = False
    else:
        g.trade_flag = True


# 盘中处理
def handle_data(context, data):
    if not g.trade_flag:
        return
    # 产生信号并交易
    g.signal = create_signal(g.fund_list, g.N, g.rise_threshold)
    trade(context, g.signal, g.fund_list, g.holding_days)
    return


# 交易函数
def trade(context, signal, security_round_list, holding_days):
    security_round_num = int(len(security_round_list) / 2)  # 轮动组数
    pre_trading_date = get_trading_day(-holding_days - 1)
    days = (g.open_date - pre_trading_date).days
    if days > 0:
        return
    hold = set(context.portfolio.positions.keys())
    if signal == 0:  # 买货币基金
        to_buy = {security_round_list[(security_round_num - 1) * 2 + 1]}
    else:
        to_buy = {security_round_list[(signal - 1) * 2 + 1]}
    sell = hold - to_buy
    buy = to_buy - hold
    if sell:
        order_target(list(sell)[0], 0)
    if buy:
        target_value = context.portfolio.cash
        order_value(list(buy)[0], target_value)
        g.open_date = context.current_dt.date()
    return


# 产生信号，返回signal
def create_signal(fund_list, num, rise_threshold):
    price_rise = [0, 0, 0, 0]
    max_rise_index = 0  # 涨幅最大的指数
    price_rise_max = -999999  # 价格涨幅
    security_round_num = int(len(fund_list) / 2)  # 轮动组数
    # 货币基金不参与计算信号
    for i in range(security_round_num - 1):
        stock = fund_list[i * 2]
        his_data = get_history(num + 1, frequency='1d', field='close', security_list=stock, fq=None,
                               include=False, is_dict=True)
        price_rise[i] = his_data[stock]['close'][-1] / his_data[stock]['close'][-num - 1] - 1  # N日涨幅
        if price_rise[i] > price_rise_max:
            max_rise_index = i
            price_rise_max = price_rise[i]
    if price_rise[max_rise_index] > rise_threshold:
        signal = max_rise_index + 1
    else:
        signal = security_round_num
    return signal
###########################################
"""
策略名称：
阳线策略
注意事项：
策略中调用的order_target、order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import numpy as np
from decimal import Decimal


def initialize(context):
    if is_trade():
        log.info('-----trade-------')
    else:
        set_fixed_slippage(0.0)
        set_slippage(slippage=0.01)
        set_limit_mode('UNLIMITED')
    g.before_start = False
    # 持仓数量
    g.hold_num = 10


def before_trading_start(context, data):
    g.current_date = context.blotter.current_dt.strftime("%Y%m%d")
    # 持仓股昨日最低价容器
    g.holds_pre_low_price = {}
    # 今日开盘价容器
    g.open_price_info = {}
    # 昨日持仓股
    g.position_list = []
    # 获取全市场股票，选最近10个交易日K线，判断个股形态：最近的一个阴K线之后没有阳线结构，符合形态且当天没有停牌的就加入股票池
    g.stock_list = get_Ashares()

    his_data_info = get_history(10, frequency='1d', field=['open', 'close', 'volume'],
                                security_list=g.stock_list, fq=None, include=False, is_dict=True)
    halt_status = get_stock_status(g.stock_list, 'HALT')
    g.buy_stocks = []
    for stock in g.stock_list.copy():
        # 停牌的过滤
        if halt_status[stock]:
            continue
        his_data = his_data_info[stock]
        his_data = np.array(list(filter(volume_filter, his_data)))
        if len(his_data) < 2:
            continue
        yinx_flag = False
        yangx_flag = False
        is_true = False
        for stock_data in reversed(his_data):
            if stock_data['close'] < stock_data['open']:
                yinx_flag = True
            if stock_data['close'] > stock_data['open']:
                yangx_flag = True
            if yinx_flag and not yangx_flag:
                is_true = True
                break
            if not yinx_flag and yangx_flag:
                is_true = False
                break
        if is_true:
            g.buy_stocks.append(stock)
    g.before_start = True
    g.first_handledata = False
    total_value = context.portfolio.portfolio_value
    g.cash = total_value / g.hold_num

    # 对持仓进行数据载入
    g.position_list = position_last_close_init(context)
    log.info(('盘前查询持仓股:', g.position_list))
    log.info(len(g.position_list))
    # 判断持仓股是否停牌，停牌的标的当日不做交易判断
    halt_status = get_stock_status(g.position_list, 'HALT')
    pre_low_data = get_history(1, '1d', 'low', security_list=g.position_list, fq='dypre', is_dict=True)
    for stock in g.position_list.copy():
        # 停牌的过滤
        if halt_status[stock]:
            g.position_list.remove(stock)
            continue
        # 非停牌持仓股获取昨日最低价
        g.holds_pre_low_price[stock] = pre_low_data[stock]['low'][0]


def handle_data(context, data):
    # 确保盘前处理已完成
    if not g.before_start:
        return
    g.K_num = get_current_kline_count()
    # 第一分钟处理
    if not g.first_handledata:
        # 回测场景持仓股及拟买股票池赋值开盘价
        if not is_trade():
            for stock in g.buy_stocks:
                g.open_price_info[stock] = data[stock].open
            for stock in g.position_list:
                g.open_price_info[stock] = data[stock].open
        g.first_handledata = True

    # 14:45之前持仓股如果符合最新价小于昨日最低价条件清仓
    if g.K_num < 225:
        if is_trade():
            for stock in g.position_list.copy():
                snapshot = get_snapshot(stock)
                if snapshot[stock]['last_px'] < g.holds_pre_low_price[stock]:
                    order_target(stock, 0)
                    g.position_list.remove(stock)
        else:
            for stock in g.position_list.copy():
                if data[stock].close < g.holds_pre_low_price[stock]:
                    order_target(stock, 0)
                    g.position_list.remove(stock)

    # 14:45分对非涨停状态的个股进行清仓
    if g.K_num == 225:
        for stock in g.position_list.copy():
            stock_flag = check_limit(stock)[stock]
            if stock_flag != 1:
                order_target(stock, 0)
                g.position_list.remove(stock)

    # 14:50分进行买入,校验当日实体阳线K线
    if g.K_num == 230:
        hold_list = position_last_close_init(context)
        if is_trade():
            count = 0
            for stock in g.buy_stocks:
                if count + len(hold_list) < g.hold_num and stock not in hold_list:
                    snapshot = get_snapshot(stock)
                    if snapshot[stock]['last_px'] > g.open_price_info[stock]:
                        order_target_value(stock, g.cash)
                        count += 1
        else:
            count = 0
            for stock in g.buy_stocks:
                if count + len(hold_list) < g.hold_num and stock not in hold_list:
                    if data[stock].close > g.open_price_info[stock]:
                        order_target_value(stock, g.cash)
                        count += 1


# 生成持仓股票列表
def position_last_close_init(context):
    position_last_list = []
    for stock in context.portfolio.positions:
        if context.portfolio.positions[stock].amount != 0:
            position_last_list.append(stock)
    return position_last_list


# 保留小数点两位
def replace(x):
    x = Decimal(x)
    x = float(str(round(x, 2)))
    return x


# 按成交量筛选停牌的数据
def volume_filter(data):
    if data['volume'] > 0:
        return data
#####################################################
"""
策略名称：
猛犸策略
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import random


def initialize(context):
    # 交易标的列表（该股票池中的代码仅作为demo演示，非投资建议）
    context.universe = [
        '002131.SZ',
        '002736.SZ',
        '600804.SS',
        '000001.SZ',
        '600376.SS',
        '600104.SS',
        '000630.SZ',
        '002065.SZ',
        '601166.SS',
        '600875.SS',
        '000555.SZ',
        '601939.SS',
        '600999.SS',
    ]
    g.daycount = 0
    g.holdstocks = []


def handle_data(context, data):
    # 最大持仓股票支数
    maxhold = 5
    totalsize = len(context.universe)
    # 取得当前的现金
    cash = context.portfolio.cash
    g.daycount = g.daycount + 1

    if len(g.holdstocks) == 0:  # 初始状态
        count = maxhold
        singlemoney = cash / maxhold

        while count > 0:
            buystock = context.universe[random.randint(0, totalsize - 1)]
            if buystock not in g.holdstocks:
                g.holdstocks.append(buystock)
                # 用所有 singlemoney 买入股票
                log.info('buystock=' + buystock)
                log.info('singlemoney=' + str(singlemoney))
                order_value(buystock, singlemoney)
                # 记录这次买入
                # log.info("Buying %s" % (buystock))
                log.info("Buying %s" % buystock)
                count = count - 1
                log.info('count=' + str(count))

    elif g.daycount % 5 == 1:  # 5 days change

        log.info('g.daycount=' + str(g.daycount))
        # 选择过去7天表现最差的股票卖出
        weakstock = ''
        weak_returns = 10000
        his_data_info = get_history(7, '1d', field=['price', 'volume'], security_list=context.universe,
                                    fq='pre', include=False, is_dict=True)
        halt_status = get_stock_status(context.universe, 'HALT')
        for stock in g.holdstocks:
            his_data = his_data_info[stock]
            # 当日停牌跳过
            if halt_status[stock]:
                continue
            if his_data.size == 0:
                continue
            startprice = his_data['price'][0]
            endprice = his_data['price'][-1]

            cur_returns = endprice / startprice - 1
            # 遍历记录涨幅最小的股票
            if cur_returns < weak_returns:
                weak_returns = cur_returns
                weakstock = stock
        if weakstock == '':
            weakstock = g.holdstocks[0]
        sellstock = weakstock
        log.info('weakstock=' + weakstock)
        g.holdstocks.remove(weakstock)
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(sellstock, 0)
        # 记录这次卖出
        log.info("selling %s" % sellstock)

        while True:
            buystock = context.universe[random.randint(0, totalsize - 1)]
            if buystock not in g.holdstocks and buystock != sellstock:
                g.holdstocks.append(buystock)
                # 用所有 cash 买入股票
                log.info('buystock=' + buystock)
                log.info('cash=' + str(cash))
                order_value(buystock, cash)
                # 记录这次买入
                log.info("Buying %s" % buystock)
                break
#############################################
"""
策略名称：
协整配对策略
注意事项：
策略中调用的order_target、order_target_value接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import numpy as np


# 初始化函数，设定基准等等
def initialize(context):
    set_params()
    set_variables()
    set_backtest()


# ---代码块1. 设置参数
def set_params():
    # 股票1
    g.security1 = '601398.SS'
    # 股票2
    g.security2 = '601988.SS'
    # 基准
    g.benchmark = '601988.SS'
    # 回归系数
    g.regression_ratio = 0.9938
    # 股票1默认仓位
    g.p = 0.5
    # 股票2默认仓位
    g.q = 0.5
    # 算z-score天数
    g.test_days = 120
    # 
    g.days_count = 0
    # 
    g.benchmarkStart = 0
    #
    g.portfolioStart = 0


# ---代码块2. 设置变量
def set_variables():
    # 现在状态
    g.state = 'empty'


# ---代码块3. 设置回测
def set_backtest():
    # 设置基准
    set_benchmark(g.benchmark)


def before_trading_start(context, data):
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    # 2006-11-01前回测由于数据不足，不执行。
    if current_date < '2006-11-01':
        g.trade_flag = False
    else:
        g.trade_flag = True


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    if not g.trade_flag:
        return
    g.days_count += 1
    log.info('day:' + str(g.days_count))
    # z值检验流程
    # 获取两支股票历史价格
    prices1 = get_history(g.test_days, '1d', 'close', g.security1, is_dict=True)[g.security1]['close']
    prices2 = get_history(g.test_days, '1d', 'close', g.security2, is_dict=True)[g.security2]['close']

    # 根据回归比例算它们的平稳序列 a.X-Y,
    stable_series = g.regression_ratio * prices1 - prices2
    # 算均值
    series_mean = np.mean(stable_series)
    # 算标准差
    sigma = np.std(stable_series)
    # 算序列现值离均值差距多少
    diff = stable_series[-1] - series_mean
    # 返回z值
    z_score = diff / sigma
    # log.info('z_score='+str(z_score))
    new_state = get_signal(z_score)
    # log.info(new_state)
    # 调仓
    change_positions(new_state, context)


# ---代码块5.获取信号
# 返回新的状态，是一个string
def get_signal(z_score):
    if z_score > 1:
        # 状态为全仓第二支
        return 'buy2'
    # 如果小于负标准差
    if z_score < -1:
        # 状态为全仓第一支
        return 'buy1'
    # 如果在正负标准差之间
    if -1 <= z_score <= 1:
        # 如果差大于0
        if z_score >= 0:
            # 在均值上面
            return 'side1'
        # 反之
        else:
            # 在均值下面
            return 'side2'


# ---代码块6.根据信号调换仓位
# 输入是目标状态，输入为一个string
def change_positions(new_state, context):
    # 总值产价值
    total_value = context.portfolio.portfolio_value
    # 如果新状态是全仓股票1
    if new_state == 'buy1':
        # 全卖股票2
        order_target(g.security2, 0)
        # 全买股票1
        order_value(g.security1, total_value)
        # 旧状态更改
        g.state = 'buy1'
    # 如果新状态是全仓股票2
    if new_state == 'buy2':
        # 全卖股票1
        order_target(g.security1, 0)
        # 全买股票2
        order_value(g.security2, total_value)
        # 旧状态更改
        g.state = 'buy2'
    # 如果处于全仓一股票状态，但是z-score交叉0点
    if (g.state == 'buy1' and new_state == 'side1') or (g.state == 'buy2' and new_state == 'side2'):
        # 按照p,q值将股票仓位调整为默认值
        order_target_value(g.security1, g.p * total_value)
        order_target_value(g.security2, g.q * total_value)
        # 代码里重复两遍因为要先卖后买，而我们没有特地确定哪个先哪个后
        order_target_value(g.security1, g.p * total_value)
        order_target_value(g.security2, g.q * total_value)
        # 状态改为‘平’
        g.state = 'even'
################################################
"""
策略名称：
双均线策略
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
import numpy as np


def initialize(context):
    # 初始化此策略
    g.security = '600570.SS'


def before_trading_start(context, data):
    h = get_history(20, '1d', field=['close', 'volume'], security_list=g.security,
                    fq='dypre', include=False, is_dict=True)
    g.close_data = h[g.security]['close']


# 当五日均线高于十日均线时买入，当五日均线低于十日均线时卖出
def handle_data(context, data):
    # 获取历史日K线数据
    current_price = data[g.security].close
    # 合成最新K线序列
    close_data = np.concatenate((g.close_data, np.array(list([current_price]))), axis=0)
    # 获取5日、10日均线
    ma5 = get_ma(close_data, 5)
    ma10 = get_ma(close_data, 10)
    # 得到当前资金余额
    cash = context.portfolio.cash
    # 如果当前有余额，并且五日均线大于十日均线
    if ma5 > ma10 and get_position(g.security).amount == 0:
        # 用所有 cash 买入股票
        order_value(g.security, cash)
        # 记录这次买入
        log.info("Buying %s" % g.security)

    # 如果五日均线小于十日均线，并且目前有头寸
    elif ma5 < ma10 and get_position(g.security).enable_amount > 0:
        # 全部卖出
        order_target(g.security, 0)
        # 记录这次卖出
        log.info("Selling %s" % g.security)


# 获取MA函数
def get_ma(close_array, num):
    ma = close_array[-num:].mean()
    return round(ma, 2)
####################################################
"""
策略名称：
单标的日内交易策略
运行周期:
分钟
策略流程：
盘中10点后每隔5分钟进行一次RSI短周期与长周期多空共振的判断，决定做正T还是反T；
盘中再按照盈利比例进行头寸恢复或者收盘前清算头寸恢复
注意事项：
策略中调用的order_target接口的使用有场景限制，回测可以正常使用，交易谨慎使用。
回测场景下撮合是引擎计算的，因此成交之后持仓信息的更新是瞬时的，但交易场景下信息的更新依赖于柜台数据
的返回，无法做到瞬时同步，可能造成重复下单。详细原因请看帮助文档。
"""
# 导入函数库

import numpy as np


# 初始化此策略
def initialize(context):
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.ini_buy_flag = False  # 买底仓开关
    g.amount = 100  # 1份标准交易头寸
    g.rate = 1  # 做T涨跌幅，1就是1%
    g.L = 50  # 长周期RSI阈值
    g.S = 80  # 短周期RSI阈值
    g.security = '510500.SS'
    if not is_trade():
        set_limit_mode('UNLIMITED')


# 盘前处理
def before_trading_start(context, data):
    g.B_T_flag = False  # 做正T开关（先买后卖）
    g.S_T_flag = False  # 做反T开关（先卖后买）
    g.first_buy_flag = False
    g.second_buy_flag = False
    g.handle_data_flag = True
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    # 2013-04-01前510500.SS回测由于数据不足，不执行。可按照标的更改允许回测时间
    if current_date < '2013-04-01':
        g.trade_flag = False
    else:
        g.trade_flag = True


# 盘中处理
def handle_data(context, data):
    if not g.trade_flag:
        return
    # 盘中交易开关（一天只做一次T）
    if not g.handle_data_flag:
        return
    k_num = get_current_kline_count()
    if not g.ini_buy_flag:
        order(g.security, g.amount)
        g.ini_buy_flag = True
        g.handle_data_flag = False
    if k_num <= 30:
        return
    # 每个5分钟整点进行做T判断
    if k_num % 5 == 0:
        # 获取5分钟K线数据
        h = get_history(100, '5m', field=['close', 'volume'], security_list=g.security,
                        fq='dypre', include=True, is_dict=True)
        close_array_5m = h[g.security]['close']
        # 合成15分钟K线数据
        h = get_history(100, '15m', field=['close', 'volume'], security_list=g.security,
                        fq='dypre', include=False, is_dict=True)
        close_array_15m = h[g.security]['close']
        current_price = data[g.security].close
        close_array_15m = np.concatenate((close_array_15m, np.array(list([current_price]))), axis=0)
        if close_array_5m.ndim != 0 and close_array_15m.ndim != 0:
            # 获取5分钟、15分钟RSI
            rsi_5m = get_rsi(close_array_5m, 11)[-1]
            rsi_15m = get_rsi(close_array_15m, 11)[-1]
            # 做T条件判断
            if rsi_15m > g.L and rsi_5m > g.S:
                if get_position(g.security).enable_amount == g.amount and not g.B_T_flag:
                    order_id = order(g.security, g.amount)
                    if order_id is not None:
                        log.info('日内看多做正T')
                        g.B_T_flag = True
                        g.B_T_cost = data[g.security].price
            if rsi_15m < 100 - g.L and rsi_5m < 100 - g.S:
                if get_position(g.security).enable_amount == g.amount and not g.S_T_flag:
                    order_id = order(g.security, -g.amount)
                    if order_id is not None:
                        log.info('日内看空做反T')
                        g.S_T_flag = True
                        g.S_T_cost = data[g.security].price
    if g.B_T_flag:
        if data[g.security].price >= g.B_T_cost * (1 + g.rate / 100):
            order_id = order(g.security, -g.amount)
            if order_id is not None:
                log.info('做正T后恢复头寸')
                g.B_T_flag = False
    if g.S_T_flag:
        if data[g.security].price <= g.S_T_cost * (1 - g.rate / 100):
            order_id = order(g.security, g.amount)
            if order_id is not None:
                log.info('做反T后恢复头寸')
                g.S_T_flag = False
    # 收盘前多次尝试将持仓恢复到开盘持有量
    if k_num >= 238:
        log.info('收盘前多次尝试将持仓恢复到开盘持有量')
        order_id = order_target(g.security, g.amount)
        if order_id is not None:
            log.info('收盘清算')


# 获取RSI数据
def get_rsi(array_list, periods=14):
    length = len(array_list)
    rsi_values = [np.nan] * length
    if length <= periods:
        return rsi_values
    up_avg = 0
    down_avg = 0

    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsi_values[periods] = 100 - 100 / (1 + rs)

    for j in range(periods + 1, length):
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        rs = up_avg / down_avg
        rsi_values[j] = 100 - 100 / (1 + rs)
    return rsi_values
##############################################
# ============================================================
# 双动量ETF轮动策略 — PTrade 版本
# 策略逻辑：
#   1. 绝对动量过滤：只选过去N日收益 > 0 的ETF
#   2. 相对动量排序：N日动量加权得分排名
#   3. 波动率加权：根据近期波动率调整仓位
#   4. ATR跟踪止损 + 冷却期风控
#   5. 防御模式：全部过滤时切换防御型ETF或空仓
# ============================================================
# 【回测设置】
#   频率：分钟级别
#   起始时间：自定义
#   基准：510300.SS (沪深300ETF)
#   成交比例：建议 ≥ 0.5（回测撮合设置）
# ============================================================

import numpy as np
import math
import pandas as pd
from datetime import datetime, date, timedelta

# ==================== 策略参数 ====================
class Params:
    # ── 基础配置 ──
    CAPITAL_RATIO = 1.00              # 资金隔离比例（总资产×10%）
    HOLDINGS_NUM = 2                   # 持仓ETF数量
    MOMENTUM_LOOKBACK = 20             # 动量回看天数
    SHORT_LOOKBACK = 5                 # 短期动量回看天数
    VOL_LOOKBACK = 20                  # 波动率计算回看天数

    # ── 绝对动量门槛 ──
    ABS_MOM_MIN_RETURN = -0.05          # 过去N日收益率阈值（-0.05=允许轻微回撤，只排除暴跌ETF）

    #     ── 排名加权 ──
    # 综合得分 = 年化收益 × R²（与七星高照相同的加权对数回归动量评分）
    VOL_PENALTY_WEIGHT = 0.0           # 波动惩罚权重（0=关闭，匹配七星高照纯动量评分）

    # ── 风控 ──
    MIN_MONEY = 5000                   # 最小交易金额
    USE_TRAILING_STOP = True           # 启用跟踪止损
    TRAILING_STOP_ATR_MULT = 3.0       # 止损线 = 最高价 - N倍ATR
    ATR_PERIOD = 14                    # ATR计算周期
    COOLDOWN_DAYS = 3                  # 止损后冷却天数

    # ── 成交量过滤 ──
    ENABLE_VOLUME_FILTER = True        # 启用成交量过滤
    VOLUME_RATIO_THRESHOLD = 4.0       # 当日量/均值量 < 阈值（放宽，只排除极端放量）

    # ── 防御模式 ──
    DEFENSIVE_ETF = "511880.SS"        # 银华日利（货币ETF）
    SAFE_HAVEN_ETF = "511010.SS"       # 国债ETF

    # ── 基准 ──
    BENCHMARK = "510300.SS"            # 沪深300ETF


# ==================== 候选ETF池 ====================
ETF_POOL = [
    # ── A股宽基 ──
    "510300.SS",   # 沪深300ETF
    "510500.SS",   # 中证500ETF
    "510050.SS",   # 上证50ETF
    "159915.SZ",   # 创业板ETF
    "588080.SS",   # 科创板50ETF
    "512100.SS",   # 中证1000ETF
    "563300.SS",   # 中证2000ETF

    # ── 行业/风格ETF ──
    "512890.SS",   # 红利低波ETF
    "512040.SS",   # 国信价值ETF

    # ── 跨境ETF ──
    "513100.SS",   # 纳指ETF
    "159509.SZ",   # 纳指科技ETF
    "513500.SS",   # 标普500ETF
    "513030.SS",   # 德国ETF
    "513520.SS",   # 日经ETF
    "513310.SS",   # 中韩芯片ETF

    # ── 港股ETF ──
    "513130.SS",   # 恒生科技ETF
    "159920.SZ",   # 恒生ETF
    "513690.SS",   # 恒生高股息ETF

    # ── 商品ETF ──
    "518880.SS",   # 黄金ETF
    "159985.SZ",   # 豆粕ETF
    "159981.SZ",   # 能源化工ETF

    # ── 债券/防御ETF ──
    "511010.SS",   # 国债ETF
    "511220.SS",   # 城投债ETF
    "511380.SS",   # 可转债ETF
    "511880.SS",   # 银华日利
]


# ==================== 初始化函数 ====================
def initialize(context):
    """策略初始化"""
    # ── 资金隔离 ──
    g.capital_allocation_ratio = Params.CAPITAL_RATIO
    g.my_positions = {}                       # 自有持仓账本 {code: {amount, total_cost, cost_basis, entry_date}}
    g.etf_name_memory = {}                    # ETF名称缓存
    g.__initialized = False                   # 防止重复初始化

    # ── 回测专用 ──
    if not is_trade():
        set_slippage(slippage=0.0001)
        set_commission(commission_ratio=0.0001, min_commission=5.0, type="ETF")

    set_benchmark(Params.BENCHMARK)

    # ── 状态变量 ──
    g.target_etfs = []                        # 今日目标ETF列表
    g.cooldown_end_date = None                # 冷却期结束日
    g.position_highs = {}                     # 持仓最高价（ATR跟踪用）
    g.atr_cache = {}                          # ATR日缓存
    g.last_ranked_date = None                 # 上次排名日期

    # ── 设置股票池 ──
    all_etfs = list(set(ETF_POOL))
    set_universe(all_etfs)

    # ── 定时任务 ──
    run_daily(context, check_positions, time='09:10')           # 盘前同步+日志
    run_daily(context, etf_sell_trade, time='10:30')            # 卖出（早盘稳定后）

    # 分钟级风控（10:00~14:30 每隔一段时间检查）
    for t in ['10:00', '11:00', '13:15', '14:00', '14:30']:
        run_daily(context, trailing_stop_check, time=t)

    log.info("=" * 60)
    log.info("双动量ETF轮动策略 初始化完成")
    log.info(f"持仓数量: {Params.HOLDINGS_NUM}只, 动量回看: {Params.MOMENTUM_LOOKBACK}天")
    log.info(f"资金比例: {Params.CAPITAL_RATIO*100:.0f}%, 止损: {'开启' if Params.USE_TRAILING_STOP else '关闭'}")
    log.info(f"防御ETF: {Params.DEFENSIVE_ETF}, 避险ETF: {Params.SAFE_HAVEN_ETF}")
    log.info("=" * 60)


# ==================== 行情工具函数 ====================
def get_etf_name(security):
    """获取ETF名称（带缓存）"""
    try:
        if security in g.etf_name_memory:
            return g.etf_name_memory[security]
        names = get_stock_name(security)
        name = names.get(security, security) if isinstance(names, dict) else security
        g.etf_name_memory[security] = name
        return name
    except:
        return security


def get_current_price(context, security):
    """获取当前价格（回测用get_history，实盘用get_snapshot）"""
    try:
        if is_trade():
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                price = snapshot[security].get('last_px', 0)
                if price and price > 0:
                    return float(price), True
            return 0, False
        else:
            hist = get_history(1, '1d', 'close', security_list=security, fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                price = hist['close'].values[-1]
                if price > 0:
                    return float(price), True
            return 0, False
    except Exception as e:
        log.warning(f"获取{security}当前价格失败: {e}")
        return 0, False


def is_paused(context, security):
    """判断是否停牌"""
    try:
        # 优先用成交量判断（回测/实盘均兼容）
        hist = get_history(1, '1d', 'volume', security_list=security, fq='pre', include=True)
        if hist is not None and len(hist) > 0:
            vol = hist['volume'].values[-1]
            if vol == 0 or str(vol) == 'nan':
                return True
        # 实盘用快照辅助
        if is_trade():
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                status = snapshot[security].get('trade_status', 'TRADE')
                return status in ['HALT', 'SUSP', 'STOPT']
        return False
    except:
        return False


def get_extreme_limits(context, security):
    """获取涨跌停价"""
    try:
        if is_trade():
            ss = get_snapshot(security)
            if ss and security in ss:
                return ss[security].get('up_px', 0), ss[security].get('down_px', 0), True
        else:
            hist = get_history(1, '1d', ['high_limit', 'low_limit'], security_list=security,
                               fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                return (hist['high_limit'].values[-1] if 'high_limit' in hist.columns else 0,
                        hist['low_limit'].values[-1] if 'low_limit' in hist.columns else 0, True)
        return 0, 0, False
    except:
        return 0, 0, False


# ==================== 动量计算引擎 ====================
def calc_momentum_score(price_series):
    """
    计算动量综合得分：
    score = 年化收益 × R² × (1 - vol_penalty)
    用加权对数回归拟合趋势线，R²衡量趋势可信度
    """
    n = len(price_series)
    if n < 5:
        return 0, 0, 0, 0

    log_prices = np.log(price_series)
    x = np.arange(n)
    weights = np.linspace(0.5, 1.5, n)  # 近期权重更高

    # 加权线性回归
    w_sum = np.sum(weights)
    wx_mean = np.sum(weights * x) / w_sum
    wy_mean = np.sum(weights * log_prices) / w_sum
    numerator = np.sum(weights * (x - wx_mean) * (log_prices - wy_mean))
    denominator = np.sum(weights * (x - wx_mean) ** 2)
    slope = numerator / denominator if denominator != 0 else 0
    intercept = wy_mean - slope * wx_mean

    # 年化收益
    ann_return = math.exp(slope * 250) - 1

    # R²
    y_pred = slope * x + intercept
    ss_res = np.sum(weights * (log_prices - y_pred) ** 2)
    ss_tot = np.sum(weights * (log_prices - np.average(log_prices, weights=weights)) ** 2)
    r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # 波动率
    daily_returns = np.diff(log_prices)
    annual_vol = np.std(daily_returns) * math.sqrt(250) if len(daily_returns) > 1 else 1

    # 综合得分
    vol_penalty = 1.0 / (1.0 + Params.VOL_PENALTY_WEIGHT * annual_vol)
    score = ann_return * max(r_sq, 0) * vol_penalty

    return score, ann_return, r_sq, annual_vol


def get_atr(security, period, context):
    """计算ATR（Average True Range）"""
    try:
        hist = get_history(period + 1, '1d', ['high', 'low', 'close'],
                           security_list=security, fq='pre', include=False)
        if hist is None or len(hist) < period + 1:
            return 0, False

        h = hist['high'].values
        l = hist['low'].values
        c = hist['close'].values

        tr = np.zeros(len(h))
        for i in range(1, len(h)):
            tr[i] = max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1]))

        atr = np.mean(tr[-period:])
        return float(atr), True
    except Exception as e:
        log.debug(f"ATR计算失败 {security}: {e}")
        return 0, False


def get_today_volume(context, security):
    """获取今日成交量"""
    try:
        if is_trade():
            kv = get_history(240, '1m', 'volume', security_list=security, fq='pre', include=False)
            return kv['volume'].sum() if kv is not None and not kv.empty else 0
        else:
            kv = get_history(1, '1d', 'volume', security_list=security, fq='pre', include=True)
            return kv['volume'].values[-1] if kv is not None and not kv.empty else 0
    except:
        return 0


# ==================== ETF排名与筛选 ====================
def rank_etfs(context):
    """对ETF池进行双动量排名"""
    pool = list(ETF_POOL)
    today = context.current_dt.date()

    # 停牌过滤
    active = [e for e in pool if not is_paused(context, e)]
    if not active:
        log.info("今日无可交易ETF")
        return []

    # 批量获取历史数据
    lookback = max(Params.MOMENTUM_LOOKBACK, Params.VOL_LOOKBACK, Params.ATR_PERIOD) + 10
    try:
        bulk_hist = get_history(lookback, '1d',
                                ['close', 'high', 'low', 'volume'],
                                security_list=active, fq='pre', include=False)
    except Exception as e:
        log.warning(f"批量获取历史数据失败: {e}")
        return []

    if bulk_hist is None or bulk_hist.empty:
        return []

    # 逐个计算排名分
    ranked = []
    for etf in active:
        try:
            name = get_etf_name(etf)
            price, ok = get_current_price(context, etf)
            if not ok or price <= 0:
                log.debug(f"{etf} {name} 无有效价格，跳过")
                continue

            # 提取该ETF的历史数据
            if 'code' in bulk_hist.columns:
                phist = bulk_hist[bulk_hist['code'] == etf]
            else:
                phist = bulk_hist

            if phist is None or len(phist) < Params.MOMENTUM_LOOKBACK:
                log.debug(f"{etf} {name} 数据不足{Params.MOMENTUM_LOOKBACK}天，跳过")
                continue

            close_arr = np.array(phist['close'].values[-Params.MOMENTUM_LOOKBACK-1:])
            close_arr = np.append(close_arr, price)

            # ── 绝对动量过滤 ──
            abs_return = close_arr[-1] / close_arr[-Params.MOMENTUM_LOOKBACK-1] - 1
            if abs_return <= Params.ABS_MOM_MIN_RETURN:
                log.debug(f"{etf} {name} 绝对动量 {abs_return*100:.1f}% ≤ {Params.ABS_MOM_MIN_RETURN*100:.0f}%，过滤")
                continue

            # ── 短期动量 ──
            if len(close_arr) >= Params.SHORT_LOOKBACK + 1:
                short_ret = close_arr[-1] / close_arr[-(Params.SHORT_LOOKBACK+1)] - 1
            else:
                short_ret = 0

            # ── 成交量过滤 ──
            if Params.ENABLE_VOLUME_FILTER:
                avg_vol = np.mean(phist['volume'].values[-20:]) if len(phist) >= 20 else 0
                today_vol = get_today_volume(context, etf)
                if avg_vol > 0 and today_vol > 0:
                    vol_ratio = today_vol / avg_vol
                    if vol_ratio > Params.VOLUME_RATIO_THRESHOLD:
                        log.debug(f"{etf} {name} 放量{vol_ratio:.1f}倍>{Params.VOLUME_RATIO_THRESHOLD}，过滤")
                        continue

            # ── 综合得分 ──
            score, ann_ret, r_sq, vol = calc_momentum_score(close_arr)

            ranked.append({
                'etf': etf,
                'name': name,
                'score': score,
                'ann_ret': ann_ret,
                'r_squared': r_sq,
                'volatility': vol,
                'short_ret': short_ret,
                'price': price,
            })
        except Exception as e:
            log.debug(f"计算{etf}排名出错: {e}")
            continue

    # 按得分降序排序
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked


# ==================== 风控模块 ====================
def is_in_cooldown(context):
    """是否处于冷却期"""
    if g.cooldown_end_date is None:
        return False
    return context.current_dt.date() < g.cooldown_end_date


def enter_cooldown(context, reason):
    """进入冷却期"""
    g.cooldown_end_date = context.current_dt.date() + timedelta(days=Params.COOLDOWN_DAYS)
    log.info(f"⛔ 进入冷却期（{reason}），持续到 {g.cooldown_end_date}")


def exit_cooldown_if_ended(context):
    """如果冷却期结束则退出"""
    if g.cooldown_end_date and context.current_dt.date() >= g.cooldown_end_date:
        g.cooldown_end_date = None
        g.position_highs = {}
        log.info("✅ 冷却期结束，恢复交易")


def trailing_stop_check(context):
    """ATR跟踪止损检查（分钟级）"""
    if not Params.USE_TRAILING_STOP:
        return
    if is_in_cooldown(context):
        return

    for sec in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(sec, None)
        if not pos or pos.amount <= 0:
            continue
        # 防御ETF不止损
        if sec in [Params.DEFENSIVE_ETF, Params.SAFE_HAVEN_ETF]:
            continue

        current_price, ok = get_current_price(context, sec)
        if not ok or current_price <= 0:
            continue

        # 计算ATR
        atr, ok_atr = get_atr(sec, Params.ATR_PERIOD, context)
        if not ok_atr or atr <= 0:
            continue

        # 更新最高价
        if sec not in g.position_highs:
            g.position_highs[sec] = current_price
        else:
            g.position_highs[sec] = max(g.position_highs[sec], current_price)

        # 止损线
        stop_price = g.position_highs[sec] - Params.TRAILING_STOP_ATR_MULT * atr

        if current_price <= stop_price:
            name = get_etf_name(sec)
            log.info(f"🛑 ATR跟踪止损: {sec} {name}, "
                     f"当前价{current_price:.3f} ≤ 止损价{stop_price:.3f}, "
                     f"最高{g.position_highs[sec]:.3f}, ATR={atr:.4f}")
            if smart_order(sec, 0, context):
                g.position_highs.pop(sec, None)
                enter_cooldown(context, f"{name} ATR跟踪止损")


# ==================== 资金隔离工具 ====================
def get_my_capital(context):
    """本策略可用资金 = 总资产 × 分配比例"""
    return context.portfolio.portfolio_value * g.capital_allocation_ratio


def sync_my_ledger(context):
    """每日同步账本与真实持仓，修正前日回测/撮合偏差"""
    ledger = g.my_positions
    pool_set = set(ETF_POOL)

    # 以真实持仓覆盖账本
    for sec in context.portfolio.positions:
        pos = context.portfolio.positions[sec]
        if sec not in pool_set or pos.amount <= 0:
            continue
        cost = getattr(pos, 'cost_basis', 0) or getattr(pos, 'avg_cost', 0) or 0
        if cost <= 0:
            p, ok = get_current_price(context, sec)
            if ok and p > 0:
                cost = p
        if cost <= 0:
            cost = 0.0001
        ledger[sec] = {
            'amount': int(pos.amount),
            'total_cost': round(int(pos.amount) * cost, 2),
            'cost_basis': round(cost, 4),
            'entry_date': context.current_dt.strftime('%Y-%m-%d'),
        }

    # 删除真实持仓中已不存在的
    for sec in list(ledger.keys()):
        if sec not in pool_set:
            continue
        pos = context.portfolio.positions.get(sec, None)
        if pos is None or pos.amount <= 0:
            del ledger[sec]


def update_my_ledger(context, code, amount, price):
    """更新自有账本"""
    ledger = g.my_positions
    if amount > 0:  # 买入
        if code in ledger:
            old = ledger[code]
            new_amt = old['amount'] + amount
            new_cost = old['total_cost'] + amount * price
            old['amount'] = new_amt
            old['total_cost'] = new_cost
            old['cost_basis'] = round(new_cost / new_amt, 4)
        else:
            ledger[code] = {
                'amount': amount,
                'total_cost': round(amount * price, 2),
                'cost_basis': round(price, 4),
                'entry_date': context.current_dt.strftime('%Y-%m-%d'),
            }
    else:  # 卖出
        sell_amt = abs(amount)
        if code in ledger:
            entry = ledger[code]
            entry['total_cost'] -= sell_amt * entry['cost_basis']
            entry['amount'] -= sell_amt
            if entry['amount'] <= 0:
                del ledger[code]


# ==================== 智能下单函数 ====================
def smart_order(security, target_value, context):
    """
    智能下单：停牌/涨跌停/最小金额/T+1保护，使用限价单
    返回 True 如果下单成功
    """
    try:
        name = get_etf_name(security)

        if is_paused(context, security):
            log.debug(f"{security} {name} 停牌，跳过")
            return False

        price, ok = get_current_price(context, security)
        if not ok or price <= 0:
            return False

        high_lim, low_lim, _ = get_extreme_limits(context, security)

        target_amount = int(target_value / price)
        target_amount = (target_amount // 100) * 100
        if target_amount <= 0 and target_value > 0:
            target_amount = 100  # 至少买1手

        # 使用自有账本判断当前持仓量，避免回测实际持仓延迟导致 diff 计算错误
        ledger_amt = g.my_positions.get(security, {}).get('amount', 0)
        cur_pos = context.portfolio.positions.get(security, None)
        cur_amount = ledger_amt
        diff = target_amount - cur_amount

        # 涨停不买 / 跌停不卖
        if diff > 0 and high_lim > 0 and price >= high_lim:
            log.debug(f"{security} {name} 涨停，跳过买入")
            return False
        if diff < 0 and low_lim > 0 and price <= low_lim:
            log.debug(f"{security} {name} 跌停，跳过卖出")
            return False

        # 最小金额检查（仅买入）
        trade_val = abs(diff) * price
        if diff > 0 and 0 < trade_val < Params.MIN_MONEY:
            log.debug(f"{security} {name} 买入金额{trade_val:.0f}<{Params.MIN_MONEY}，跳过")
            return False

        # T+1 可卖数量限制
        if diff < 0 and cur_pos:
            closeable = int(cur_pos.enable_amount)
            if closeable == 0:
                log.debug(f"{security} {name} 今日买入不可卖")
                return False
            diff = -min(abs(diff), closeable)

        if diff == 0:
            return False

        limit_price = round(price, 3)

        # 记录下单前持仓
        before_amt = int(cur_pos.amount) if cur_pos else 0

        order_id = order(security, diff, limit_price=limit_price)
        if not order_id:
            log.warning(f"下单失败: {security} {name} 数量{diff}")
            return False

        # 获取实际成交数量
        actual_filled = None
        try:
            order_info = get_order(order_id)
            if order_info and len(order_info) > 0:
                o = order_info[0]
                actual_filled = int(o.filled if hasattr(o, 'filled') else o.get('filled', 0))
        except:
            pass

        # get_order失败时用持仓变化估算
        if actual_filled is None or actual_filled <= 0:
            try:
                after_pos = context.portfolio.positions.get(security, None)
                after_amt = int(after_pos.amount) if after_pos else 0
                actual_filled = abs(after_amt - before_amt)
            except:
                pass

        # 回测撮合延迟：get_order 和持仓变化都返回0时，乐观假设订单将被撮合
        # 避免账本因撮合延迟而持续失真（盘前 sync_my_ledger 会修正残留偏差）
        optimistic = False
        if actual_filled is None or actual_filled <= 0:
            actual_filled = abs(diff)
            optimistic = True

        # 更新账本
        actual_amount = actual_filled if diff > 0 else -actual_filled
        if actual_filled > 0:
            update_my_ledger(context, security, actual_amount, price)
            if diff > 0:
                tag = "预估成交" if optimistic else "成交"
                log.info(f"📥 买入 {security} {name} 委托{diff} {tag}{actual_filled} 价格{price:.3f}")
                g.position_highs[security] = price
            else:
                tag = "预估成交" if optimistic else "成交"
                log.info(f"📤 卖出 {security} {name} 委托{-diff} {tag}{actual_filled} 价格{price:.3f}")
        else:
            log.info(f"⚠️ {security} {name} 订单未成交")

        return True

    except Exception as e:
        log.warning(f"智能下单 {security} 出错: {e}")
        return False


# ==================== 交易逻辑 ====================
def check_positions(context):
    """盘前：同步账本 + 日志"""
    sync_my_ledger(context)

    for sec in context.portfolio.positions:
        pos = context.portfolio.positions[sec]
        if pos.amount > 0:
            name = get_etf_name(sec)
            cp, _ = get_current_price(context, sec)
            pnl_pct = (cp / pos.cost_basis - 1) * 100 if pos.cost_basis > 0 else 0
            log.info(f"📊 {sec} {name}: 持仓{pos.amount}股, "
                     f"成本{pos.cost_basis:.3f}, 现价{cp:.3f}, 盈亏{pnl_pct:+.2f}%")


def etf_sell_trade(context):
    """卖出不在目标名单的持仓"""
    log.info("=" * 40)
    log.info("【卖出阶段】")

    exit_cooldown_if_ended(context)

    if is_in_cooldown(context):
        log.info(f"冷却期中，跳过卖出，冷却至 {g.cooldown_end_date}")
        # 冷却期也清仓（只留防御ETF）
        for sec in list(context.portfolio.positions.keys()):
            if sec not in [Params.DEFENSIVE_ETF, Params.SAFE_HAVEN_ETF]:
                smart_order(sec, 0, context)
        log.info("=" * 40)
        return

    # 获取排名
    ranked = rank_etfs(context)

    # 确定目标ETF
    target_list = []
    for r in ranked[:Params.HOLDINGS_NUM]:
        target_list.append(r['etf'])

    # 无目标时切防御
    if not target_list:
        log.info("无符合条件的ETF，切换防御模式")
        target_list = [Params.DEFENSIVE_ETF]

    g.target_etfs = target_list
    target_set = set(target_list)

    log.info(f"今日目标ETF: {[f'{e} {get_etf_name(e)}' for e in target_list]}")

    # 卖出不在目标中的持仓
    for sec in list(context.portfolio.positions.keys()):
        if sec not in target_set:
            pos = context.portfolio.positions.get(sec, None)
            if pos and pos.amount > 0:
                if smart_order(sec, 0, context):
                    log.info(f"📤 清仓(不在目标): {sec} {get_etf_name(sec)}")

    log.info("=" * 40)

    # 同时进行买入（卖和买同一时间，等待下一分钟买入执行）
    # 这里采用 sell -> buy_next_minute 模式（需要两个 run_daily）
    # 为简化，直接在卖出后立即买入
    etf_buy_execute(context)


def etf_buy_execute(context):
    """买入执行逻辑"""
    log.info("【买入阶段】")

    if is_in_cooldown(context):
        log.info("冷却期中，不买入")
        log.info("=" * 40)
        return

    target_etfs = getattr(g, 'target_etfs', [])
    if not target_etfs:
        log.info("无目标ETF")
        log.info("=" * 40)
        return

    # 资金隔离
    my_cap = get_my_capital(context)

    # 计算账本已持仓市值
    held_val = 0.0
    for code, entry in list(g.my_positions.items()):
        if entry['amount'] > 0:
            p, ok = get_current_price(context, code)
            if ok:
                held_val += entry['amount'] * p

    remaining = my_cap - held_val
    if remaining < Params.MIN_MONEY:
        log.info(f"剩余配额 {remaining:.0f} < {Params.MIN_MONEY}，不买入")
        log.info("=" * 40)
        return

    # 等权分配
    need_buy = [e for e in target_etfs if e not in g.my_positions or g.my_positions[e]['amount'] == 0]
    if not need_buy:
        # 都在目标中，只调仓
        need_buy = target_etfs

    per_etf = remaining / max(len(need_buy), 1)

    log.info(f"资金配额: 总{my_cap:.0f}, 已持仓{held_val:.0f}, 剩余{remaining:.0f}, 每只{per_etf:.0f}")

    for etf in need_buy:
        # 计算当前持仓市值
        cur_val = 0
        if etf in g.my_positions and g.my_positions[etf]['amount'] > 0:
            cp, ok = get_current_price(context, etf)
            if ok:
                cur_val = g.my_positions[etf]['amount'] * cp

        target_val = per_etf + cur_val
        if abs(target_val - cur_val) < Params.MIN_MONEY:
            continue

        if smart_order(etf, target_val, context):
            log.info(f"📦 调仓: {etf} {get_etf_name(etf)} 目标市值{target_val:.0f}")

    log.info("=" * 40)


# ==================== 必需的 handle_data ====================
def handle_data(context, data):
    """PTrade必需函数，策略使用run_daily调度，此函数保持为空"""
    pass
##############################################################
# 七星高照ETF轮动策略-PTrade版本
# 原始策略来源：聚宽
# 转换说明：已适配PTrade平台API，支持回测和交易

import numpy as np
import math

def initialize(context):
    """
    初始化函数
    """
    # ==================== 实盘交易设置 ====================
    
    # 回测专用设置（仅在回测环境执行）
    if not is_trade():
        # 设置滑点（PTrade使用set_slippage）
        set_slippage(slippage=0.0002)
        
        # 设置交易成本：ETF交易成本较低
        set_commission(commission_ratio=0.0002, min_commission=5.0, type="ETF")
    
    log.info("增强版策略初始化完成！")
    
    # 设置参考基准（代码尾缀转换：XSHE改为SZ）
    set_benchmark("161226.SZ")
    
    # ==================== ETF池设置 ====================
    g.etf_pool = [
        # 大宗商品ETF（代码尾缀转换：XSHG改为SS，XSHE改为SZ）
        "518880.SS",  # 黄金ETF
        "159985.SZ",  # 豆粕ETF（跟踪豆粕期货价格）
        "501018.SS",  # 南方原油（投资原油相关资产）
        "161226.SZ",  # 白银LOF
        # 国际ETF
        "511010.SS",  # 国债
        "513100.SS",  # 纳指ETF
        # 中国ETF
        "159915.SZ",  # 创业板ETF
        # 债券ETF
        "511220.SS",  # 城投债ETF
    ]
    
    # 大ETF池（备用）
    g.etf_pool_bak = [
        # 大宗商品ETF
        "518880.SS",  # 黄金ETF
        "159980.SZ",  # 有色ETF（跟踪有色金属板块）
        "159985.SZ",  # 豆粕ETF（跟踪豆粕期货价格）
        "501018.SS",  # 南方原油（投资原油相关资产）
        "161226.SZ",  # 白银LOF
        "159981.SZ",  # 能源化工ETF
        # 国际ETF
        "513100.SS",  # 纳指ETF
        "159509.SZ",  # 纳指科技ETF
        "513290.SS",  # 纳指生物ETF
        "513500.SS",  # 标普500ETF
        "159529.SZ",  # 标普消费
        "513400.SS",  # 道琼斯ETF
        "513520.SS",  # 日经225ETF
        "513030.SS",  # 德国30ETF
        "513080.SS",  # 法国ETF
        "513310.SS",  # 中韩半导体ETF
        "513730.SS",  # 东南亚ETF
        # 香港ETF
        "159792.SZ",  # 港股互联ETF
        "513130.SS",  # 恒生科技
        "513050.SS",  # 中概互联网ETF
        "159920.SZ",  # 恒生ETF
        "513690.SS",  # 港股红利
        # 指数ETF
        "510300.SS",  # 沪深300ETF
        "510500.SS",  # 中证500ETF
        "510050.SS",  # 上证50ETF
        "510210.SS",  # 上证ETF
        "159915.SZ",  # 创业板ETF
        "588080.SS",  # 科创50
        "512100.SS",  # 中证1000ETF
        "563360.SS",  # A500-ETF
        "563300.SS",  # 中证2000ETF
        # 风格ETF
        "512890.SS",  # 红利低波ETF
        "159967.SZ",  # 创业板成长ETF
        "512040.SS",  # 价值ETF
        "159201.SZ",  # 自由现金流ETF
        # 债券ETF
        "511380.SS",  # 可转债ETF
        "511010.SS",  # 国债ETF
        "511220.SS",  # 城投债ETF
    ]
    
    # g.etf_pool = g.etf_pool_bak  # 启用完整大池
    
    # ==================== 核心策略参数 ====================
    # 动量计算参数
    g.lookback_days = 25  # 长期动量计算周期
    g.holdings_num = 1    # 持仓ETF数量
    g.defensive_etf = "511010.SS"  # 防御性ETF（货币ETF）
    g.min_money = 5000  # 最小交易金额
    g.max_order_amount = 1000000  # 单笔最大委托数量（券商限制，通常为100万股）
    
    # 风险控制参数
    g.stop_loss = 0.95    # 固定百分比止损线（下跌5%止损）
    g.loss = 0.97   # 近3日跌幅止损线
    
    # 得分阈值
    g.min_score_threshold = 0  # 最低得分阈值
    g.max_score_threshold = 500.0  # 最高得分阈值
    
    # ==================== 成交量过滤参数 ====================
    g.enable_volume_check = True  # 是否启用成交量过滤
    g.volume_lookback = 5  # 成交量历史参考天数
    g.volume_threshold = 2  # 放量阈值（大于设定值视为放量）
    g.volume_return_limit = 1  # 年化收益率过滤：当高于该值，则启用成交量过滤
    
    # ==================== 新增：均线过滤参数 ====================
    g.enable_ma_filter = False  # 是否启用均线过滤
    g.ma_filter_days = 20  # 均线过滤天数
    
    # ==================== 原有：短期动量过滤参数 ====================
    g.use_short_momentum_filter = True  # 是否启用短期动量过滤
    g.short_lookback_days = 10  # 短期动量计算周期
    g.short_momentum_threshold = 0.0  # 短期动量阈值
    
    # ==================== 原有：ATR动态止损参数 ====================
    g.use_atr_stop_loss = True  # 是否启用ATR动态止损
    g.atr_period = 14  # ATR计算周期
    g.atr_multiplier = 2  # ATR倍数
    g.atr_trailing_stop = False  # 是否使用跟踪止损
    g.atr_exclude_defensive = True  # 防御ETF是否豁免ATR止损
    
    # ==================== 原有：RSI过滤参数 ====================
    g.use_rsi_filter = True  # 是否启用RSI过滤
    g.rsi_period = 6  # RSI计算周期
    g.rsi_lookback_days = 1  # 检查RSI的历史天数
    g.rsi_threshold = 98  # RSI阈值
    
    # ==================== 持仓管理 ====================
    g.positions = {}  # 记录持仓
    g.position_highs = {}  # 记录持仓期间的最高价
    g.position_stop_prices = {}  # 记录持仓的ATR止损价
    
    # 设置股票池（将所有可能交易的ETF加入）
    all_etfs = list(set(g.etf_pool + [g.defensive_etf]))
    set_universe(all_etfs)
    
    # ==================== 交易调度 ====================
    # 每天开盘后检查持仓
    run_daily(context, check_positions, time='09:10')
    # 每天开盘后检查ATR动态止损
    run_daily(context, check_atr_stop_loss, time='10:31')
    # 执行卖出操作
    run_daily(context, etf_sell_trade, time='10:45')
    # 执行买入操作
    run_daily(context, etf_buy_trade, time='14:00')
    
    log.info("策略参数初始化完成:")
    log.info("- ETF池大小: %s 只ETF" % len(g.etf_pool))
    log.info("- 动量周期: %s 天" % g.lookback_days)
    log.info("- 持仓数量: %s 只" % g.holdings_num)
    log.info("- 成交量过滤: %s" % ("启用" if g.enable_volume_check else "禁用"))
    log.info("- 均线过滤: %s" % ("启用" if g.enable_ma_filter else "禁用"))
    log.info("- RSI过滤: %s" % ("启用" if g.use_rsi_filter else "禁用"))
    log.info("- ATR止损: %s" % ("启用" if g.use_atr_stop_loss else "禁用"))
    log.info("- 防御ETF: %s" % g.defensive_etf)

# ==================== 统一的价格获取函数 ====================
def get_current_price(context, security):
    """
    统一的价格获取函数，自动适配回测和交易环境
    返回：(当前价格, 是否成功)
    """
    try:
        if is_trade():
            # 交易环境使用get_snapshot
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                current_price = snapshot[security].get('last_px', 0)
                if current_price > 0:
                    return current_price, True
            return 0, False
        else:
            # 回测环境使用get_history，include=True包含当前周期
            hist = get_history(1, '1d', 'close', security_list=security, 
                            fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                current_price = hist['close'].values[-1]
                if current_price > 0:
                    return current_price, True
            return 0, False
    except Exception as e:
        log.warning("获取%s当前价格失败: %s" % (security, str(e)))
        return 0, False

def get_current_prices_batch(context, securities):
    """
    批量获取多个标的的当前价格
    返回：字典 {security: price}
    """
    result = {}
    try:
        if is_trade():
            # 交易环境批量获取快照
            snapshot = get_snapshot(securities)
            if snapshot:
                for security in securities:
                    if security in snapshot:
                        price = snapshot[security].get('last_px', 0)
                        if price > 0:
                            result[security] = price
        else:
            # 回测环境批量获取历史数据
            hist = get_history(1, '1d', 'close', security_list=securities,
                            fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                for security in securities:
                    try:
                        price_data = hist.query('code in ["%s"]' % security)['close']
                        if len(price_data) > 0:
                            price = price_data.values[-1]
                            if price > 0:
                                result[security] = price
                    except:
                        continue
        
        return result
    except Exception as e:
        log.warning("批量获取价格失败: %s" % str(e))
        return result

def get_trade_status(context, security):
    """
    获取标的交易状态
    返回：(状态字符串, 涨停价, 跌停价)
    """
    try:
        if is_trade():
            # 交易环境使用get_snapshot
            snapshot = get_snapshot(security)
            if snapshot and security in snapshot:
                info = snapshot[security]
                status = info.get('trade_status', 'TRADE')
                high_limit = info.get('up_px', 0)
                low_limit = info.get('down_px', 0)
                return status, high_limit, low_limit
            return 'UNKNOWN', 0, 0
        else:
            # 回测环境使用get_history获取涨跌停价
            hist = get_history(1, '1d', ['close', 'high_limit', 'low_limit'], 
                            security_list=security, fq='pre', include=True)
            if hist is not None and len(hist) > 0:
                close_price = hist['close'].values[-1]
                high_limit = hist['high_limit'].values[-1] if 'high_limit' in hist.columns else 0
                low_limit = hist['low_limit'].values[-1] if 'low_limit' in hist.columns else 0
                
                # 回测中默认认为可交易
                status = 'TRADE'
                
                # 检查是否停牌（成交量为0）
                vol_hist = get_history(1, '1d', 'volume', security_list=security,
                                    fq='pre', include=True)
                if vol_hist is not None and len(vol_hist) > 0:
                    volume = vol_hist['volume'].values[-1]
                    if volume == 0:
                        status = 'HALT'
                
                return status, high_limit, low_limit
            return 'UNKNOWN', 0, 0
    except Exception as e:
        log.warning("获取%s交易状态失败: %s" % (security, str(e)))
        return 'UNKNOWN', 0, 0

# ============ 持仓检查 ===============
def check_positions(context):
    """每日开盘后检查持仓状态"""
    try:
        positions = context.portfolio.positions
        if not positions:
            log.info("当前无持仓")
            return
        
        # 获取持仓列表
        position_list = list(positions.keys())
        
        for security in positions:
            position = positions[security]
            if position.amount > 0:
                security_name = get_stock_name(security).get(security, security)
                current_price = position.last_sale_price
                
                # 检查停牌状态
                trade_status, high_limit, low_limit = get_trade_status(context, security)
                if trade_status in ['HALT', 'SUSP', 'STOPT']:
                    log.info("警告 %s %s 今日停牌" % (security, security_name))
                
                log.info("持仓检查: %s %s, 数量: %s, 成本: %.3f, 当前价: %.3f" % 
                        (security, security_name, position.amount, position.cost_basis, current_price))
    except Exception as e:
        log.warning("检查持仓时出错: %s" % str(e))

# ==================== 卖出函数 ====================
def etf_sell_trade(context):
    """
    卖出函数
    功能：卖出不符合条件的持仓
    """
    log.info("========== 卖出操作开始 ==========")
    
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 如果没有持仓，直接返回
    if not current_positions:
        log.info("当前无持仓，无需卖出")
        return
    
    # 获取符合条件的ETF排名
    ranked_etfs = get_ranked_etfs(context)
    
    # ========== 构建目标ETF列表（最多g.holdings_num只） ==========
    target_etfs = []
    for metrics in ranked_etfs:
        if len(target_etfs) >= g.holdings_num:
            break
        if metrics['score'] >= g.min_score_threshold:
            target_etfs.append(metrics['etf'])
        else:
            break
    
    # ========== 如果无合格标的，尝试使用防御ETF ==========
    if not target_etfs:
        defensive_etf_available = check_defensive_etf_available(context)
        if defensive_etf_available:
            target_etfs = [g.defensive_etf]
    
    target_etfs_set = set(target_etfs)
    
    # ========== 卖出不在目标列表中的持仓 ==========
    for security in current_positions:
        # 只处理ETF池中的标的或防御ETF
        if (security in g.etf_pool or security == g.defensive_etf) and security not in target_etfs_set:
            position = context.portfolio.positions[security]
            if position.amount > 0:
                success = smart_order_target_value(security, 0, context)
                if success:
                    security_name = get_stock_name(security).get(security, security)
                    log.info("卖出不在目标列表的持仓: %s %s" % (security, security_name))
                    
                    # 清除相关记录
                    if security in g.position_highs:
                        del g.position_highs[security]
                    if security in g.position_stop_prices:
                        del g.position_stop_prices[security]
    
    # ========== 检查并执行固定止损 ==========
    for security in list(context.portfolio.positions.keys()):
        if security in g.etf_pool:
            position = context.portfolio.positions[security]
            if position.amount > 0:
                current_price = position.last_sale_price
                cost_price = position.cost_basis
                
                if current_price <= cost_price * g.stop_loss:
                    success = smart_order_target_value(security, 0, context)
                    if success:
                        security_name = get_stock_name(security).get(security, security)
                        loss_percent = (current_price / cost_price - 1) * 100
                        log.info("固定百分比止损卖出: %s %s，亏损: %.2f%%" % 
                                (security, security_name, loss_percent))
                        
                        # 清除记录
                        if security in g.position_highs:
                            del g.position_highs[security]
                        if security in g.position_stop_prices:
                            del g.position_stop_prices[security]
    
    log.info("========== 卖出操作完成 ==========")

# ==================== 获取ETF排名函数 ====================
def get_ranked_etfs(context):
    """
    获取符合条件的ETF排名
    返回结果：应用所有过滤条件，返回满足条件的ETF列表，按得分降序
    """
    etf_metrics = []
    
    # 可选：先进行均线过滤（减少计算量）
    filtered_pool = g.etf_pool
    
    for etf in filtered_pool:
        # ========== 停牌过滤 ==========
        trade_status, high_limit, low_limit = get_trade_status(context, etf)
        if trade_status in ['HALT', 'SUSP', 'STOPT']:
            log.info("%s: 今日停牌，跳过计算" % etf)
            continue
        
        metrics = calculate_momentum_metrics(context, etf)
        if metrics is not None:
            # 过滤掉得分异常的ETF
            if 0 < metrics['score'] < g.max_score_threshold:
                etf_metrics.append(metrics)
            else:
                log.info("警告 %s 得分不满足要求！" % etf)
    
    # 按得分降序排序
    etf_metrics.sort(key=lambda x: x['score'], reverse=True)
    return etf_metrics

# ==================== 动量指标计算函数 ====================
def calculate_momentum_metrics(context, etf):
    """
    计算ETF的动量指标，整合所有过滤条件
    返回包含各项指标和过滤结果的字典
    """
    try:
        # 获取历史价格数据
        lookback = max(g.lookback_days, g.short_lookback_days, 
                    g.rsi_period + g.rsi_lookback_days) + 20
        
        # PTrade使用get_history获取历史数据
        prices_df = get_history(lookback, '1d', ['close', 'high', 'low', 'volume'], 
                            security_list=etf, fq='pre', include=True)
        
        if prices_df is None or len(prices_df) < g.lookback_days:
            log.info("%s: 历史数据不足，跳过计算" % etf)
            return None
        
        # 提取收盘价、最高价、最低价和成交量
        close_prices = prices_df['close'].values
        high_prices = prices_df['high'].values
        low_prices = prices_df['low'].values
        volumes = prices_df['volume'].values
        
        # 最后一个数据点是当前价格
        current_price = close_prices[-1]
        if current_price == 0:
            log.info("%s: 当前价格为0，跳过计算" % etf)
            return None
        
        # 使用包含当前价格的完整序列
        price_series = close_prices
        
        # ========== 成交量过滤检查 ==========
        if g.enable_volume_check and len(price_series) > g.lookback_days and len(volumes) > g.volume_lookback:
            volume_ratio = check_volume_surge(volumes, g.volume_lookback, g.volume_threshold)
            if volume_ratio is not None:
                volume_annualized = get_annualized_returns(price_series, g.lookback_days)
                if volume_annualized > g.volume_return_limit:
                    log.info("%s: 成交量放大%.2f倍且折合年化收益%.2f超过设置值%s，属于'高位放量'，过滤掉" % 
                            (etf, volume_ratio, volume_annualized, g.volume_return_limit))
                    return None
        
        # ========== RSI过滤检查 ==========
        rsi_filter_pass = True
        current_rsi = 0
        max_rsi = 0
        
        if g.use_rsi_filter and len(price_series) >= g.rsi_period + g.rsi_lookback_days:
            rsi_values = calculate_rsi(price_series, g.rsi_period)
            
            if len(rsi_values) >= g.rsi_lookback_days:
                recent_rsi = rsi_values[-g.rsi_lookback_days:]
                rsi_ever_above_threshold = np.any(recent_rsi > g.rsi_threshold)
                
                # 检查当前价格是否在MA5之下
                if len(price_series) >= 5:
                    ma5 = np.mean(price_series[-5:])
                    current_below_ma5 = current_price < ma5
                else:
                    current_below_ma5 = True
                
                if rsi_ever_above_threshold and current_below_ma5:
                    rsi_filter_pass = False
                    max_rsi = np.max(recent_rsi)
                    current_rsi = recent_rsi[-1] if len(recent_rsi) > 0 else 0
                    log.info("RSI过滤: %s 近%s日RSI曾达%.1f，当前价%.3f<MA5，当前RSI=%.1f" % 
                            (etf, g.rsi_lookback_days, max_rsi, current_price, current_rsi))
                else:
                    max_rsi = np.max(recent_rsi) if len(recent_rsi) > 0 else 0
                    current_rsi = recent_rsi[-1] if len(recent_rsi) > 0 else 0
        
        if not rsi_filter_pass:
            return None
        
        # ========== 短期动量计算 ==========
        if len(price_series) >= g.short_lookback_days + 1:
            short_return = price_series[-1] / price_series[-(g.short_lookback_days + 1)] - 1
            short_annualized = (1 + short_return) ** (250.0 / g.short_lookback_days) - 1
        else:
            short_return = 0
            short_annualized = 0
        
        # ========== 短期动量过滤 ==========
        if g.use_short_momentum_filter and short_annualized < g.short_momentum_threshold:
            log.info("%s: 短期动量%.4f < 阈值%.4f，过滤掉" % 
                    (etf, short_annualized, g.short_momentum_threshold))
            return None
        
        # ========== 长期动量计算（加权回归） ==========
        recent_price_series = price_series[-(g.lookback_days + 1):]
        y = np.log(recent_price_series)
        x = np.arange(len(y))
        weights = np.linspace(1, 2, len(y))
        
        # 计算年化收益率
        slope, intercept = np.polyfit(x, y, 1, w=weights)
        annualized_returns = math.exp(slope * 250) - 1
        
        # 计算R²（拟合优度）
        ss_res = np.sum(weights * (y - (slope * x + intercept)) ** 2)
        ss_tot = np.sum(weights * (y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0
        
        # 综合得分 = 年化收益率 * 趋势稳定性
        score = annualized_returns * r_squared
        
        # ========== 短期风控过滤 ==========
        if len(price_series) >= 4:
            day1_ratio = price_series[-1] / price_series[-2]
            day2_ratio = price_series[-2] / price_series[-3]
            day3_ratio = price_series[-3] / price_series[-4]
            
            if min(day1_ratio, day2_ratio, day3_ratio) < g.loss:
                score = 0
                log.info("警告 %s 近3日有单日跌幅超设定值，已排除" % etf)
        
        return {
            'etf': etf,
            'annualized_returns': annualized_returns,
            'r_squared': r_squared,
            'score': score,
            'slope': slope,
            'current_price': current_price,
            'short_return': short_return,
            'short_annualized': short_annualized,
            'short_momentum_pass': short_return >= g.short_momentum_threshold,
            'rsi_filter_pass': rsi_filter_pass,
            'current_rsi': current_rsi,
            'max_recent_rsi': max_rsi,
        }
        
    except Exception as e:
        log.warning("计算%s动量指标时出错: %s" % (etf, str(e)))
        return None

# ==================== 成交量检查函数 ====================
def check_volume_surge(volumes, lookback_days, threshold):
    """
    检查成交量是否放量
    volumes: 成交量数组（已包含当日数据）
    lookback_days: 历史参考天数
    threshold: 放量阈值
    返回：如果放量返回比值，否则返回None
    """
    if len(volumes) < lookback_days + 1:
        return None
    
    # 当日成交量
    current_volume = volumes[-1]
    
    # 历史平均成交量（不包括当日）
    historical_volumes = volumes[-(lookback_days + 1):-1]
    avg_volume = np.mean(historical_volumes)
    
    if avg_volume == 0:
        return None
    
    volume_ratio = current_volume / avg_volume
    
    if volume_ratio > threshold:
        return volume_ratio
    else:
        return None

# ==================== 均线过滤函数 ====================
def filter_below_ma(context, stocks, days=None):
    """
    过滤掉当前价格小于N日均价的股票/ETF
    返回过滤后的标的列表（仅保留当前价 >= N日均价的标的）
    """
    if days is None:
        days = g.ma_filter_days
    
    if not stocks:
        return []
    
    filtered = []
    
    for stock in stocks:
        try:
            # 获取N日历史收盘价数据（包含当前价格）
            hist = get_history(days, "1d", "close", 
                            security_list=stock, fq='pre', include=True)
            
            if hist is None or len(hist) < days:
                log.info("%s: 历史数据不足%s天，跳过过滤" % (stock, days))
                continue
            
            close_prices = hist['close'].values
            
            # 计算N日均价（包含当前价格）
            ma_n = np.mean(close_prices)
            
            # 获取当前价格（数组最后一个元素）
            current_price = close_prices[-1]
            
            # 保留当前价 >= N日均价的标的
            if current_price >= ma_n:
                filtered.append(stock)
                log.info("%s: 通过%s日均线过滤，当前价 %.2f >= 均线 %.2f" % 
                        (stock, days, current_price, ma_n))
            else:
                log.info("%s: 未通过%s日均线过滤，当前价 %.2f < 均线 %.2f" % 
                        (stock, days, current_price, ma_n))
                
        except Exception as e:
            log.warning("计算%s %s日均价失败: %s" % (stock, days, str(e)))
            continue
    
    return filtered

# ==================== ATR计算函数 ====================
def calculate_atr(security, period=14):
    """
    计算ATR（平均真实波幅）指标
    """
    try:
        needed_days = period + 20
        hist_data = get_history(needed_days, '1d', ['high', 'low', 'close'],
                            security_list=security, fq='pre', include=True)
        
        if hist_data is None or len(hist_data) < period + 1:
            return 0, [], False, "数据不足%s天" % (period + 1)
        
        high_prices = hist_data['high'].values
        low_prices = hist_data['low'].values
        close_prices = hist_data['close'].values
        
        tr_values = np.zeros(len(high_prices))
        for i in range(1, len(high_prices)):
            tr1 = high_prices[i] - low_prices[i]
            tr2 = abs(high_prices[i] - close_prices[i-1])
            tr3 = abs(low_prices[i] - close_prices[i-1])
            tr_values[i] = max(tr1, tr2, tr3)
        
        atr_values = np.zeros(len(tr_values))
        for i in range(period, len(tr_values)):
            atr_values[i] = np.mean(tr_values[i-period+1:i+1])
        
        current_atr = atr_values[-1] if len(atr_values) > 0 else 0
        valid_atr = atr_values[period:] if len(atr_values) > period else atr_values
        
        return current_atr, valid_atr, True, "计算成功"
    
    except Exception as e:
        log.warning("计算%s ATR时出错: %s" % (security, str(e)))
        return 0, [], False, "计算出错:%s" % str(e)

# ==================== RSI计算函数 ====================
def calculate_rsi(prices, period=6):
    """
    计算RSI指标
    """
    if len(prices) < period + 1:
        return []
    
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gains = np.zeros_like(prices)
    avg_losses = np.zeros_like(prices)
    avg_gains[period] = np.mean(gains[:period])
    avg_losses[period] = np.mean(losses[:period])
    
    rsi_values = np.zeros(len(prices))
    rsi_values[:period] = 50
    
    for i in range(period + 1, len(prices)):
        avg_gains[i] = (avg_gains[i-1] * (period - 1) + gains[i-1]) / period
        avg_losses[i] = (avg_losses[i-1] * (period - 1) + losses[i-1]) / period
        
        if avg_losses[i] == 0:
            rsi_values[i] = 100
        else:
            rs = avg_gains[i] / avg_losses[i]
            rsi_values[i] = 100 - (100 / (1 + rs))
    
    return rsi_values[period:]

# ==================== 计算年化收益 ====================
def get_annualized_returns(price_series, lookback_days):
    """
    计算年化收益率
    """
    # 使用最后lookback_days+1天的数据
    recent_price_series = price_series[-(lookback_days + 1):]
    y = np.log(recent_price_series)
    x = np.arange(len(y))
    weights = np.linspace(1, 2, len(y))  # 加权回归，近期权重更高
    
    # 计算年化收益率
    slope, intercept = np.polyfit(x, y, 1, w=weights)
    annualized_returns = math.exp(slope * 250) - 1
    return annualized_returns

# ==================== 买入函数 ====================
def etf_buy_trade(context):
    """
    买入函数
    功能：买入符合条件的ETF
    """
    log.info("========== 买入操作开始 ==========")
    
    # 获取符合条件的ETF排名
    ranked_etfs = get_ranked_etfs(context)
    
    # 记录所有ETF的指标（用于调试）
    if ranked_etfs:
        log.info("=== 符合条件的ETF指标 ===")
        for i, metrics in enumerate(ranked_etfs[:5]):  # 只显示前5名
            if i >= 5:
                break
            etf_name = get_stock_name(metrics['etf']).get(metrics['etf'], metrics['etf'])
            log.info("%s %s: 得分=%.4f, 年化=%.4f, R²=%.4f, 短期动量=%.4f, RSI=%.1f" % 
                    (metrics['etf'], etf_name, metrics['score'], metrics['annualized_returns'], 
                    metrics['r_squared'], metrics['short_return'], metrics['current_rsi']))
    
    # ========== 选择前g.holdings_num只合格ETF ==========
    target_etfs = []
    for metrics in ranked_etfs:
        if len(target_etfs) >= g.holdings_num:
            break
        if metrics['score'] >= g.min_score_threshold:
            target_etfs.append(metrics['etf'])
        else:
            break
    
    # 如果没有合格标的，尝试使用防御ETF
    if not target_etfs:
        if check_defensive_etf_available(context):
            target_etfs = [g.defensive_etf]
            log.info("进入防御模式，选择防御ETF: %s %s" % 
                    (g.defensive_etf, get_stock_name(g.defensive_etf).get(g.defensive_etf, g.defensive_etf)))
        else:
            log.info("进入空仓模式，无符合条件的ETF且防御ETF不可用")
            return
    else:
        # 显示选中的ETF
        selected_info = []
        for etf in target_etfs:
            etf_name = get_stock_name(etf).get(etf, etf)
            selected_info.append("%s %s" % (etf, etf_name))
        log.info("选择前%s名ETF: %s" % (len(target_etfs), ', '.join(selected_info)))
    
    # ========== 检查是否有其他非目标持仓未清空 ==========
    current_positions = list(context.portfolio.positions.keys())
    current_etf_positions = [pos for pos in current_positions if pos in g.etf_pool or pos == g.defensive_etf]
    other_positions = [pos for pos in current_etf_positions if pos not in target_etfs]
    
    if other_positions:
        for pos in other_positions:
            position = context.portfolio.positions[pos]
            if position.amount > 0:
                pos_name = get_stock_name(pos).get(pos, pos)
                log.info("警告 尚有其他持仓 %s 未卖出，等待卖出完成后再买入新标的" % pos_name)
                return
    
    # ========== 等权重分配资金 ==========
    # 交易环境使用可用资金，回测环境使用总资产
    if is_trade():
        # 实盘：使用可用资金 + 现有持仓市值
        available_cash = context.portfolio.cash
        current_positions_value = 0
        
        # 计算目标ETF中已有持仓的市值
        for etf in target_etfs:
            if etf in context.portfolio.positions:
                pos = context.portfolio.positions[etf]
                current_positions_value += pos.amount * pos.last_sale_price
        
        total_available = available_cash + current_positions_value
        target_value_per_etf = total_available / len(target_etfs)
        
        log.info("实盘资金分配 - 可用资金: %.2f, 目标持仓市值: %.2f, 总可用: %.2f, 单ETF目标: %.2f" % 
                (available_cash, current_positions_value, total_available, target_value_per_etf))
    else:
        # 回测：使用总资产
        total_value = context.portfolio.portfolio_value
        target_value_per_etf = total_value / len(target_etfs)
        log.info("回测资金分配 - 总资产: %.2f, 单ETF目标: %.2f" % 
                (total_value, target_value_per_etf))
    
    # 对每个目标ETF下单
    for etf in target_etfs:
        success = smart_order_target_value(etf, target_value_per_etf, context)
        if success:
            etf_name = get_stock_name(etf).get(etf, etf)
            # 判断是买入还是调仓
            current_pos = context.portfolio.positions.get(etf)
            current_val = 0
            if current_pos:
                current_val = current_pos.amount * current_pos.last_sale_price
            action = "调仓" if current_val > 0 else "买入"
            log.info("%s: %s %s，目标金额: %.2f" % (action, etf, etf_name, target_value_per_etf))
    
    log.info("========== 买入操作完成 ==========")

# ==================== 辅助函数 ====================
def check_defensive_etf_available(context):
    """检查防御ETF是否可交易"""
    defensive_etf = g.defensive_etf
    
    try:
        if is_trade():
            # 交易环境使用get_snapshot
            snapshot = get_snapshot(defensive_etf)
            
            if not snapshot or defensive_etf not in snapshot:
                log.info("防御性ETF %s 无行情数据" % defensive_etf)
                return False
            
            etf_info = snapshot[defensive_etf]
            trade_status = etf_info.get('trade_status', 'TRADE')
            
            if trade_status in ['HALT', 'SUSP', 'STOPT']:
                log.info("防御性ETF %s 今日停牌" % defensive_etf)
                return False
            
            last_px = etf_info.get('last_px', 0)
            high_limit = etf_info.get('up_px', 0)
            low_limit = etf_info.get('down_px', 0)
            
            if last_px >= high_limit and high_limit > 0:
                log.info("防御性ETF %s 当前涨停" % defensive_etf)
                return False
            
            if last_px <= low_limit and low_limit > 0:
                log.info("防御性ETF %s 当前跌停" % defensive_etf)
                return False
        else:
            # 回测环境简单检查数据可用性
            hist = get_history(1, '1d', ['close', 'volume'], 
                            security_list=defensive_etf, fq='pre', include=True)
            if hist is None or len(hist) == 0:
                log.info("防御性ETF %s 无历史数据" % defensive_etf)
                return False
            
            volume = hist['volume'].values[-1]
            if volume == 0:
                log.info("防御性ETF %s 停牌" % defensive_etf)
                return False
        
        return True
        
    except Exception as e:
        log.warning("检查防御ETF可用性时出错: %s" % str(e))
        return False

def smart_order_target_value(security, target_value, context):
    """
    智能下单函数，兼容回测和交易环境
    """
    try:
        # 获取交易状态和限价信息
        trade_status, high_limit, low_limit = get_trade_status(context, security)
        
        # 检查标的是否停牌
        if trade_status in ['HALT', 'SUSP', 'STOPT']:
            security_name = get_stock_name(security).get(security, security)
            log.info("%s %s: 今日停牌，跳过交易" % (security, security_name))
            return False
        
        # 获取当前价格
        current_price, price_success = get_current_price(context, security)
        if not price_success or current_price == 0:
            security_name = get_stock_name(security).get(security, security)
            log.info("%s %s: 无法获取当前价格，跳过交易" % (security, security_name))
            return False
        
        # 检查涨停（买入时）
        if target_value > 0 and high_limit > 0:
            if current_price >= high_limit:
                security_name = get_stock_name(security).get(security, security)
                log.info("%s %s: 当前涨停，跳过买入" % (security, security_name))
                return False
        
        # 检查跌停（卖出时）
        if target_value == 0 and low_limit > 0:
            if current_price <= low_limit:
                security_name = get_stock_name(security).get(security, security)
                log.info("%s %s: 当前跌停，跳过卖出" % (security, security_name))
                return False
        
        # 计算目标数量
        target_amount = int(target_value / current_price)
        
        # 对于ETF，按100股整数倍调整
        target_amount = (target_amount // 100) * 100
        if target_amount <= 0 and target_value > 0:
            target_amount = 100
        
        # 限制单笔最大委托数量（避免超过券商限制）
        if target_amount > g.max_order_amount:
            log.warning("%s: 计算的目标数量%s超过单笔最大限额%s，调整为最大限额" % 
                    (security, target_amount, g.max_order_amount))
            target_amount = g.max_order_amount
        
        # 获取当前持仓
        current_position = context.portfolio.positions.get(security, None)
        current_amount = current_position.amount if current_position else 0
        
        # 计算需要调整的数量
        amount_diff = target_amount - current_amount
        
        # 限制单次调整数量（避免超过券商限制）
        if abs(amount_diff) > g.max_order_amount:
            if amount_diff > 0:
                log.warning("%s: 需买入数量%s超过单笔限额%s，本次先买入%s股" % 
                        (security, amount_diff, g.max_order_amount, g.max_order_amount))
                amount_diff = g.max_order_amount
            else:
                log.warning("%s: 需卖出数量%s超过单笔限额%s，本次先卖出%s股" % 
                        (security, abs(amount_diff), g.max_order_amount, g.max_order_amount))
                amount_diff = -g.max_order_amount
        
        # 检查最小交易金额
        trade_value = abs(amount_diff) * current_price
        if 0 < trade_value < g.min_money:
            security_name = get_stock_name(security).get(security, security)
            log.info("%s %s: 交易金额%.2f小于最小交易额%s，跳过交易" % 
                    (security, security_name, trade_value, g.min_money))
            return False
        
        # 检查T+1限制（卖出操作）
        if amount_diff < 0:
            closeable_amount = current_position.enable_amount if current_position else 0
            if closeable_amount == 0:
                security_name = get_stock_name(security).get(security, security)
                log.info("%s %s: 当天买入不可卖出(T+1)" % (security, security_name))
                return False
            amount_diff = -min(abs(amount_diff), closeable_amount)
        
        # 执行下单
        if amount_diff != 0:
            # 使用限价单，价格设置为当前价格的小数精度（ETF为3位小数）
            limit_price = round(current_price, 3)
            order_result = order(security, amount_diff, limit_price=limit_price)
            
            if order_result:
                # 更新持仓记录
                g.positions[security] = target_amount
                
                # 如果买入操作，初始化最高价记录和ATR止损价
                if amount_diff > 0 and security in g.etf_pool:
                    g.position_highs[security] = current_price
                    
                    # 计算ATR止损价
                    if g.use_atr_stop_loss and not (g.atr_exclude_defensive and security == g.defensive_etf):
                        current_atr, atr_list, success, msg = calculate_atr(security, g.atr_period)
                        if success:
                            if g.atr_trailing_stop:
                                g.position_stop_prices[security] = current_price - g.atr_multiplier * current_atr
                            else:
                                g.position_stop_prices[security] = current_price - g.atr_multiplier * current_atr
                
                security_name = get_stock_name(security).get(security, security)
                if amount_diff > 0:
                    log.info("买入 %s %s，数量: %s，价格: %.3f" % 
                            (security, security_name, amount_diff, current_price))
                else:
                    log.info("卖出 %s %s，数量: %s，价格: %.3f" % 
                            (security, security_name, abs(amount_diff), current_price))
                return True
            else:
                security_name = get_stock_name(security).get(security, security)
                log.warning("下单失败: %s %s，数量: %s" % (security, security_name, amount_diff))
                return False
        
        return False
        
    except Exception as e:
        log.warning("智能下单%s时出错: %s" % (security, str(e)))
        return False

def check_atr_stop_loss(context):
    """
    检查并执行ATR动态止损
    """
    if not g.use_atr_stop_loss:
        return
    
    try:
        positions_list = list(context.portfolio.positions.keys())
        if not positions_list:
            return
        
        # 批量获取当前价格
        current_prices = get_current_prices_batch(context, positions_list)
        
        for security in positions_list:
            if security not in g.etf_pool:
                continue
            
            position = context.portfolio.positions[security]
            if position.amount <= 0:
                continue
            
            # 防御ETF豁免检查
            if g.atr_exclude_defensive and security == g.defensive_etf:
                continue
            
            try:
                # 获取当前价格
                if security not in current_prices:
                    continue
                
                current_price = current_prices[security]
                if current_price == 0:
                    continue
                
                cost_price = position.cost_basis
                
                # 计算当前ATR值
                current_atr, atr_values, success, atr_info = calculate_atr(security, g.atr_period)
                
                if not success:
                    continue
                
                # 更新持仓期间的最高价
                if security not in g.position_highs:
                    g.position_highs[security] = current_price
                else:
                    g.position_highs[security] = max(g.position_highs[security], current_price)
                
                position_high = g.position_highs[security]
                
                # 计算ATR止损价
                if g.atr_trailing_stop:
                    atr_stop_price = position_high - g.atr_multiplier * current_atr
                else:
                    atr_stop_price = cost_price - g.atr_multiplier * current_atr
                
                g.position_stop_prices[security] = atr_stop_price
                
                # 检查是否触发ATR止损
                if current_price <= atr_stop_price:
                    success = smart_order_target_value(security, 0, context)
                    if success:
                        security_name = get_stock_name(security).get(security, security)
                        loss_percent = (current_price / cost_price - 1) * 100
                        atr_stop_type = "跟踪" if g.atr_trailing_stop else "固定"
                        log.info("ATR动态止损(%s)卖出: %s %s，亏损: %.2f%%" % 
                                (atr_stop_type, security, security_name, loss_percent))
                        
                        # 清除记录
                        if security in g.position_highs:
                            del g.position_highs[security]
                        if security in g.position_stop_prices:
                            del g.position_stop_prices[security]
            
            except Exception as e:
                log.warning("检查%s ATR止损时出错: %s" % (security, str(e)))
                
    except Exception as e:
        log.warning("ATR止损检查整体出错: %s" % str(e))

# ==================== 必需的handle_data函数 ====================
def handle_data(context, data):
    """
    PTrade必需的handle_data函数
    由于策略使用run_daily定时执行，这里保持为空即可
    """
    pass
#############################################################
def initialize(context):
    # 长白山股票代码
    g.security = '603099.SS'
    set_universe(g.security)
    # 用于标记是否已在当年4-5月买入
    g.bought_this_year = False
    # 记录当前年份，用于判断新一年的开始
    g.current_year = None
    log.info('=== 策略初始化完成 ===')
    log.info('标的股票: %s (长白山)' % g.security)
    log.info('策略逻辑: 4-5月底价买入，价格突破60元卖出')

def before_trading_start(context, data):
    # 获取当前日期
    current_date = context.blotter.current_dt
    current_month = current_date.month
    current_year = current_date.year
    
    # 如果跨年了，重置买入标记
    if g.current_year != current_year:
        g.current_year = current_year
        g.bought_this_year = False
        log.info('=== 新年份 %d 开始，重置买入标记 ===' % current_year)
    
    # 每日盘前信息
    position = get_position(g.security)
    log.info('【盘前状态】日期: %s, 当前持仓: %d股, 今年是否已买入: %s, 当前月份: %d月' 
            % (current_date.strftime('%Y-%m-%d'), position.amount, g.bought_this_year, current_month))

def handle_data(context, data):
    security = g.security
    current_date = context.blotter.current_dt
    current_month = current_date.month
    
    # 获取当前持仓
    position = get_position(security)
    current_amount = position.amount
    
    # 获取当前价格（收盘价和最高价）
    current_price = data[security].close
    high_price = data[security].high
    
    # 获取账户信息
    cash = context.portfolio.cash
    portfolio_value = context.portfolio.portfolio_value
    
    # 输出每日基本运行状态（确认策略在运行）
    log.info('--- 策略运行 %s ---' % current_date.strftime('%Y-%m-%d'))
    
    # 卖出逻辑：盘中最高价 > 60元，立刻全部卖出（最高优先级）
    if current_amount > 0 and high_price > 60:
        order_target(security, 0)
        log.info('>>> 【卖出信号】盘中最高价突破60元，立刻卖出全部持仓 | 最高价: %.2f元, 收盘价: %.2f元, 持仓: %d股' 
                % (high_price, current_price, current_amount))
        return
    
    # 持仓监控：显示当前持仓状态
    if current_amount > 0:
        cost_basis = position.cost_basis
        pnl_ratio = (current_price - cost_basis) / cost_basis * 100 if cost_basis > 0 else 0
        log.info('【持仓中】收盘价: %.2f元, 成本: %.2f元, 盈亏: %.2f%%, 持仓: %d股, 等待突破60元' 
                % (current_price, cost_basis, pnl_ratio, current_amount))
    
    # 买入逻辑：仅在4-5月执行
    if current_month in [4, 5] and not g.bought_this_year and current_amount == 0:
        # 获取过去30天的历史价格，找到底价区域
        try:
            history = get_history(30, '1d', 'close', security, fq='pre', include=False)
            if len(history) > 0:
                # 计算30天最低价和平均价
                min_price = history['close'].min()
                avg_price = history['close'].mean()
                
                # 底价买入策略：当前价格接近最低价（在最低价上浮5%范围内）
                threshold_price = min_price * 1.05
                
                log.info('【4-5月买入窗口】当前价格: %.2f元, 30日最低: %.2f元, 买入阈值: %.2f元, 30日均价: %.2f元' 
                        % (current_price, min_price, threshold_price, avg_price))
                
                if current_price <= threshold_price:
                    # 使用80%的可用资金买入
                    buy_value = cash * 1.0
                    if buy_value > 0:
                        order_value(security, buy_value)
                        g.bought_this_year = True
                        expected_shares = int(buy_value / current_price / 100) * 100
                        log.info('>>> 【买入信号】底价区域买入 | 价格: %.2f元, 预计买入: %d股, 金额: %.2f元' 
                                % (current_price, expected_shares, buy_value))
                    else:
                        log.info('资金不足，无法买入')
                else:
                    price_diff_ratio = (current_price - threshold_price) / threshold_price * 100
                    log.info('价格高于买入阈值 %.2f%%，等待价格回落' % price_diff_ratio)
        except Exception as e:
            log.error('获取历史数据失败: %s' % str(e))
    elif current_month not in [4, 5] and current_amount == 0:
        # 非4-5月且无持仓，显示等待状态
        if current_month in [1, 2, 3]:
            log.info('【等待买入窗口】当前%d月，等待进入4-5月买入窗口，价格: %.2f元' % (current_month, current_price))
        elif current_month in [6, 7, 8, 9, 10, 11, 12]:
            log.info('【非交易窗口】当前%d月，价格: %.2f元，等待明年4-5月' % (current_month, current_price))
    elif g.bought_this_year and current_amount == 0:
        # 今年已经买入过但现在没有持仓（已卖出），不再买入
        log.info('【本年已完成交易】今年已买入并卖出，等待下一年，当前价格: %.2f元' % current_price)
    
    # 最后输出账户总览
    log.info('账户总资产: %.2f元, 可用资金: %.2f元, 持仓市值: %.2f元' 
            % (portfolio_value, cash, position.amount * current_price if position.amount > 0 else 0))
###################################################
'''
#策略名称：PTRADE股票双低三因子策略（版权所有不得转卖或转赠）
#升级说明：在A级策略“股票双低轮动策略”的基础上增加了回调因子，寻找调整过后的双低个股。同时加入了
时序因子，在历史数据小微盘股表现不佳的月份选择空仓。经过优化后策略收益率有较大提升，最大回撤也有所减小。

# 特别注意：本策略日频调仓，实盘和回测时请在周期频率选项处选择 "每日"！！！每天调仓时间为14：50左右（根据券商不同有细微差别）
# 再次重申：本策略日频调仓，实盘和回测时请在周期频率选项处选择 "每日"！！！
#——————————————————
'''

#v2：前后3因子一致版

import pandas as pd
import numpy as np

# 初始化
def initialize(context):
    set_universe([])
    g.enable_market_sentiment = True  # 情绪监控开关 （默认True开启）
    g.use_index_stocks = False        # 股票池开关设置True=使用指数成分股，False=使用全市场A股  
    g.enable_financial_filter = True  # 是否开启财务指标筛选（True打开）
    g.enable_688 = True               # 是否允许科创板标的（True允许）
    g.clear_period = False            # 空仓期初始化 
    g.index = "399303.SZ"             # 成分股指数 (默认国证2000）
    g.buy_stock_count = 10             # 最大持有股票数量
    g.pervalue = 20000                # 单次买入金额
    g.screen_stock_count = 70         # 盘前筛选股票数量（情绪监控池）
    g.fall_days = 30                  # 回调因子计算周期（天）
    g.price_line = 2.2             # 股价下限
    g.turnover_threshold = 1     # 换手率下限%
    g.float_line = 6 * 100000000   # 市值下限
    g.market_cap_weight = 1      # 市值因子权重系数
    g.fallback_weight = 1        # 回调因子权重系数
    if not is_trade():
        set_backtest()  # 设置回测条件
    
    # 情绪监控设置
    g.down_ratio_threshold = 0.51   # 下跌家数超过时清仓
    g.hi_ratio = 0.95              # 极端情绪阈值，默认下跌家数超95%时恢复买入
    g.holdings = set()
    g.pause_buy = False      # 暂停买入标志
    
# 设置回测条件
def set_backtest():
    set_limit_mode("UNLIMITED")
    set_commission(commission_ratio=0.00015, min_commission=5.0, type="stock")


# 盘前处理
def before_trading_start(context, data):
    g.pre_position_list = list(g.holdings)
    g.pause_buy = False
    
    # ===== 空仓期检查 =====
    current_date = context.current_dt.date()
    g.clear_period = False
    
    # 检查是否在空仓期
    if (current_date.month == 12 and current_date.day >= 15) or \
       (current_date.month in (1, 2) and (current_date.month == 1 or current_date.day <= 5)):
        g.clear_period = True
 #       log.info("当前日期 %s 处于空仓期 ，停止选股并准备清仓" % current_date)
        g.trade_stocks = []
        set_universe([])
        return  # 直接返回，跳过后续选股逻辑    
        
    if g.use_index_stocks:
        g.stock_list = get_index_stocks(g.index)
    else:
        g.stock_list = get_Ashares() 
    
    stock_list_tmp = filter_stock_by_status(g.stock_list, filter_type=["ST", "HALT", "DELISTING","DELISTING_SORTING"], query_date=None)
    if not g.enable_688:
        stock_list_tmp = [s for s in stock_list_tmp if not s.startswith('688')]
    
    
    if g.enable_financial_filter:
        log.info("开始财务筛选，当前候选数量：%d" % len(stock_list_tmp))
        current_year = context.previous_date.year
        years_needed = [current_year - 1, current_year - 2]
        df_income = get_fundamentals(stock_list_tmp, 'income_statement', fields=['net_profit'],
                                     start_year=str(years_needed[1]), end_year=str(years_needed[0]),
                                     report_types='4', date_type='end')
        valid_stocks = []
        if not df_income.empty:
            grouped = df_income.groupby('secu_code')['net_profit'].agg(
                lambda x: x.count() >= 2 and not (x < 0).all()
            )
            valid_stocks = grouped[grouped].index.tolist()
        stock_list_tmp = [stock for stock in stock_list_tmp if stock in valid_stocks]
        log.info("净利润筛选后数量：%d" % len(stock_list_tmp))
    else:
        log.info("已关闭财务筛选，跳过净利润及ROE检查")

    # 获取估值数据
    fields = ["total_value", "a_floats", "float_value", "turnover_rate"]
    df = get_fundamentals(stock_list_tmp, "valuation", fields=fields, date=context.previous_date)
    
    df['turnover_rate'] = df['turnover_rate'].astype(float)
    df['price'] = df['float_value'] / df['a_floats']
    df = df[
        (df['price'] > g.price_line) & 
        (df['float_value'] > g.float_line) &
        (df['turnover_rate'] >= g.turnover_threshold)
    ].sort_values(by='float_value').head(400)
    
    stock_list_tmp = df.index.tolist()
    set_universe(stock_list_tmp)
    
    # === 新增：计算回调幅度 ===
    # 获取历史收盘价数据
    close_data = get_history(g.fall_days+1, '1d', ['close'], stock_list_tmp, fq='pre', is_dict=True)
      
    # 计算每只股票的回调幅度
    fallback_pct = {}
    for stock in stock_list_tmp:
        if stock in close_data:
            closes = close_data[stock]['close']
            if len(closes) >= 2:  # 确保有足够数据
                start_price = closes[0]   # g.fall_days天前的收盘价
                end_price = closes[-1]    # 最近交易日收盘价
                fallback = (start_price - end_price) / start_price
                fallback_pct[stock] = fallback
            else:
                fallback_pct[stock] = 0  # 数据不足设为0
        else:
            fallback_pct[stock] = 0
    
    # 将回调幅度加入DataFrame
    df['fallback'] = pd.Series(fallback_pct)
    
    # === 修改：三因子排序 ===
    df['市值排名'] = df['float_value'].rank()
    df['股价排名'] = df['price'].rank()
    df['回调排名'] = df['fallback'].rank(ascending=False)  # 回调幅度越大排名越小
    df['综合排名'] = (
        df['市值排名'] * g.market_cap_weight + 
        df['股价排名'] * 1 +  # 保持原股价权重为1
        df['回调排名'] * g.fallback_weight
    )
    df = df.sort_values(by='综合排名').head(g.screen_stock_count)
    
    g.trade_stocks = df.index.tolist()
    g.df = df
    
    # === 修改：日志增加回调幅度信息 ===
    if not df.empty:
        min_price = df['price'].min()
        max_price = df['price'].max()
        avg_price = df['price'].mean()
        min_float_value = df['float_value'].min()
        max_float_value = df['float_value'].max()
        avg_float_value = df['float_value'].mean()
        min_fallback = df['fallback'].min() * 100  # 转换为百分比
        max_fallback = df['fallback'].max() * 100
        avg_fallback = df['fallback'].mean() * 100
        stock_count = len(df)
        
        log.info(f"[盘前筛选] 共筛选股票 {stock_count} 只 | "
                f"股价范围 {min_price:.2f}-{max_price:.2f} 元 | "
                f"流通市值 {min_float_value/100000000:.2f}-{max_float_value/100000000:.2f} 亿 | "
                f"回调幅度 {min_fallback:.2f}%-{max_fallback:.2f}%")
    else:
        log.warning("[盘前筛选] 未筛选出符合条件的股票，请检查筛选参数！")


# 盘中处理
def handle_data(context, data):
    # 空仓期处理
    if g.clear_period:
        # 清空所有持仓
        for stock in list(context.portfolio.positions):
            order_target_value(stock, 0)
        return  # 跳过后续交易逻辑    
    
    if g.enable_market_sentiment:
        # 获取实时涨跌家数
        down_ratio, decline_count, valid_count = get_realtime_down_ratio(context, data, g.trade_stocks)
        log.info("[情绪监控] 当前下跌比例：{:.2%} (下跌家数：{}，统计家数：{})".format(down_ratio, decline_count, valid_count))

        # 风控判断
        if g.hi_ratio > down_ratio > g.down_ratio_threshold:
            log.warning("[情绪监控] 触发下跌家数阈值，执行清仓")
            clear_all_positions(context)
            return  # 终止后续交易
    else:
        log.info("[情绪监控] 当前市场情绪监控已关闭")   
    buy_stocks = get_trade_stocks(context, data)
    log.info("buy_stocks:%s" % buy_stocks)
    trade(context, buy_stocks)

def get_realtime_down_ratio(context, data, stock_list):
    """通过data对象计算下跌比例"""
    if not stock_list:
        return 0.0
    
    decline_count = 0
    valid_count = 0
    
    for stock in stock_list:
        # 确保股票在数据中且价格有效
        if stock in data and data[stock].price > 0 and data[stock].preclose > 0:
            if data[stock].price < data[stock].preclose:
                decline_count += 1
            valid_count += 1
    
    down_ratio = decline_count / valid_count if valid_count > 0 else 0.0
    return down_ratio, decline_count, valid_count

def clear_all_positions(context):
    """清空所有持仓"""
    for stock in list(g.holdings):
        order_target(stock, 0)
        log.info("清仓: %s" % stock)
    g.holdings.clear()

# 交易函数
def trade(context, buy_stocks):
    # 卖出不在买入列表中的持仓
    for stock in list(g.holdings):
        if stock not in buy_stocks:
            order_target_value(stock, 0)
            g.holdings.remove(stock)
            log.info("sell:%s" % stock)
    
    # 买入新标的，使用固定金额
    for stock in buy_stocks:
        if stock not in g.holdings and len(g.holdings) < g.buy_stock_count:
            order_value(stock, g.pervalue)
            g.holdings.add(stock)
            log.info("buy:%s" % stock)


# 获取买入股票池（涨停股不参与换仓）
def get_trade_stocks(context, data):
    hold_up_limit_stock = [stock.replace("XSHG", "SS").replace("XSHE", "SZ") 
                          for stock in g.pre_position_list 
                          if check_limit(stock)[stock] == 1] # 获取持仓中涨停的标的
    df = g.df
    if df.empty:
        return hold_up_limit_stock
    df["code"] = df.index
    # 计算当前流通市值和实时股价
    df["curr_float_value"] = df.apply(lambda x: x["a_floats"] * data[x["code"]].price, axis=1)
    df["curr_price"] = df.apply(lambda x: data[x["code"]].price, axis=1)
    
    # 过滤无效数据
    df = df[(df["curr_float_value"] > 0) & (df["curr_price"] > g.price_line)]
    
    # 三因子排序（与盘前逻辑一致）
    df['市值排名'] = df['curr_float_value'].rank()
    df['股价排名'] = df['curr_price'].rank()
    # 使用盘前计算好的回调幅度（因为盘中无法重新计算）
    df['回调排名'] = df['fallback'].rank(ascending=False)
    df['综合排名'] = (
        df['市值排名'] * g.market_cap_weight + 
        df['股价排名'] * 1 + 
        df['回调排名'] * g.fallback_weight
    )
    
    # 按综合排名排序
    stocks = df.sort_values(by="综合排名").index.tolist()
    
    # 计算本次可买入数量
    count = g.buy_stock_count - len(hold_up_limit_stock)
    check_out_lists = stocks[:count]
    check_out_lists = check_out_lists + hold_up_limit_stock
    return check_out_lists
####################################################
# 导入必要的库
import pandas as pd

# 初始化函数
def initialize(context):
    # 全局变量设置
    g.index = '399101.XBHS'  # 中小板综指数
    g.buy_stock_count = 3    # 持仓股票数量
    g.screen_stock_count = 15 # 筛选股票数量
    
    # 财务数据筛选阈值
    g.roe_threshold = 0.15   # ROE > 15%
    g.roa_threshold = 0.10   # ROA > 10%
    g.revenue_threshold = 1e8 # 营业收入 > 1亿元
    g.profit_threshold = 0    # 净利润 > 0
    g.market_cap_min = 5      # 市值下限（亿元）
    g.market_cap_max = 50     # 市值上限（亿元）
    
    # 风控参数
    g.stoploss_limit = 0.88   # 个股止损阈值
    g.HV_ratio = 0.9          # 异常放量检测比例
    
    # 设置股票池
    g.security = get_index_stocks(g.index)
    set_universe(g.security)
    
    # 设置定时任务 - 修正：run_daily需要3个参数
    run_daily(context, before_trading_start, time='9:00')
    run_daily(context, handle_data, time='10:00')
    
    # 如果需要更多定时任务，可以添加
    run_daily(context, check_stoploss_daily, time='14:30')
    run_daily(context, print_position_info, time='15:00')

# 盘前处理函数
def before_trading_start(context, data):
    """
    盘前处理函数，接受2个参数
    """
    log.info(f"盘前处理开始: {context.blotter.current_dt}")
    
    # 获取指数成分股
    stocks = get_index_stocks(g.index)
    
    # 过滤ST、停牌、退市股票
    stocks = filter_stock_by_status(stocks, filter_type=["ST", "HALT", "DELISTING"])
    
    # 获取财务数据并进行筛选
    g.target_list = filter_by_fundamentals(context, stocks)
    
    # 按流通市值排序，选择小市值股票
    if g.target_list:
        # 获取流通市值数据
        df = get_fundamentals(g.target_list, "valuation", 
                              fields=["float_value"], 
                              date=context.previous_date,
                              is_dataframe=True)
        
        if df is not None and not df.empty:
            df = df.sort_values(by="float_value", ascending=True)
            g.target_list = df.index.tolist()[:g.screen_stock_count]
    
    log.info(f"今日目标股票列表: {g.target_list}")

# 财务数据筛选函数
def filter_by_fundamentals(context, stocks):
    """
    基于财务数据筛选股票
    """
    if not stocks:
        return []
    
    try:
        # 获取当前日期
        current_date = context.blotter.current_dt.strftime('%Y%m%d')
        
        # 获取盈利能力数据
        df_profit = get_fundamentals(stocks, "profit_ability",
                                     fields=["roe", "roa"],
                                     date=current_date,
                                     is_dataframe=True)
        
        # 获取利润表数据
        df_income = get_fundamentals(stocks, "income_statement",
                                     fields=["net_profit", "operating_revenue"],
                                     date=current_date,
                                     is_dataframe=True)
        
        # 获取估值数据
        df_val = get_fundamentals(stocks, "valuation",
                                  fields=["total_value"],
                                  date=current_date,
                                  is_dataframe=True)
        
        if df_profit is None or df_income is None or df_val is None:
            return []
        
        # 合并数据
        df = df_profit.merge(df_income, left_index=True, right_index=True, how='inner')
        df = df.merge(df_val, left_index=True, right_index=True, how='inner')
        
        # 转换为数值类型
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 市值转为亿元
        df['total_value'] = df['total_value'] / 1e8
        
        # 应用筛选条件
        mask = (
            (df['roe'] > g.roe_threshold) &
            (df['roa'] > g.roa_threshold) &
            (df['net_profit'] > g.profit_threshold) &
            (df['operating_revenue'] > g.revenue_threshold) &
            (df['total_value'] >= g.market_cap_min) &
            (df['total_value'] <= g.market_cap_max)
        )
        
        filtered_stocks = df[mask].index.tolist()
        log.info(f"财务数据筛选后股票数量: {len(filtered_stocks)}")
        return filtered_stocks
        
    except Exception as e:
        log.error(f"财务数据筛选异常: {e}")
        return []

# 盘中交易处理函数
def handle_data(context, data):
    """
    盘中交易处理函数
    """
    log.info(f"盘中交易处理: {context.blotter.current_dt}")
    
    # 检查持仓股票的止损条件
    check_stoploss(context, data)
    
    # 检查异常放量
    check_high_volume(context, data)
    
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 卖出不在目标列表中的股票（涨停股除外）
    for stock in current_positions:
        if stock not in g.target_list:
            # 检查是否涨停
            if not is_limit_up(stock, data):
                order_target_value(stock, 0)
                log.info(f"卖出不在目标列表的股票: {stock}")
    
    # 买入目标股票
    if g.target_list:
        # 计算可用资金
        available_cash = context.portfolio.cash
        
        # 计算每只股票分配的资金
        buy_count = min(g.buy_stock_count - len(current_positions), len(g.target_list))
        if buy_count > 0 and available_cash > 0:
            value_per_stock = available_cash / buy_count
            
            for stock in g.target_list[:buy_count]:
                if stock not in current_positions:
                    order_target_value(stock, value_per_stock)
                    log.info(f"买入财务数据良好的小市值股票: {stock}")

# 止损检查函数
def check_stoploss(context, data):
    for stock, position in context.portfolio.positions.items():
        avg_cost = position.cost_basis
        if avg_cost <= 0:
            continue
            
        # 获取当前价格
        current_price = data[stock].price if stock in data else position.last_sale_price
        
        if current_price < avg_cost * g.stoploss_limit:
            order_target_value(stock, 0)
            log.info(f"触发止损，卖出股票: {stock} (成本: {avg_cost:.2f}, 现价: {current_price:.2f})")

# 每日止损检查函数（独立定时任务）
def check_stoploss_daily(context):
    """
    每日固定时间检查止损
    """
    log.info("执行每日止损检查")
    
    # 获取当前持仓
    positions = get_positions()
    
    for stock, position in positions.items():
        avg_cost = position.cost_basis
        if avg_cost <= 0:
            continue
            
        # 获取当前价格
        snapshot = get_snapshot(stock)
        if snapshot and stock in snapshot:
            current_price = snapshot[stock].get("last_px", 0)
            
            if current_price > 0 and current_price < avg_cost * g.stoploss_limit:
                order_target_value(stock, 0)
                log.info(f"每日止损检查：卖出股票: {stock}")

# 异常放量检查函数
def check_high_volume(context, data):
    for stock in context.portfolio.positions.keys():
        try:
            # 获取历史成交量
            hist_data = get_history(120, '1d', 'volume', 
                                    security_list=[stock], 
                                    fq='pre')
            
            if hist_data is not None and not hist_data.empty:
                # 获取当日成交量
                if stock in data:
                    cur_volume = data[stock].volume
                    hist_max = hist_data.max().values
                    
                    # 检查是否异常放量
                    if cur_volume > g.HV_ratio * hist_max:
                        order_target_value(stock, 0)
                        log.info(f"检测到异常放量，卖出股票: {stock}")
        except Exception as e:
            log.error(f"检查异常放量时出错: {e}")

# 涨停检查函数
def is_limit_up(stock, data):
    """
    检查股票是否涨停
    """
    if stock not in data:
        return False
    
    try:
        # 获取最新价格和涨停价
        current_data = data[stock]
        last_close = current_data.pre_close
        current_price = current_data.price
        
        if last_close <= 0:
            return False
        
        # 计算涨停价（考虑不同板块的涨跌幅限制）
        if stock.startswith('68') or stock.startswith('3'):
            limit_rate = 0.2  # 科创板和创业板
        else:
            limit_rate = 0.1  # 主板
        
        limit_price = last_close * (1 + limit_rate)
        
        # 考虑价格精度
        if stock.endswith('.SS') or stock.endswith('.SZ'):
            # 股票价格精度为小数点后2位
            limit_price = round(limit_price, 2)
        
        return current_price >= limit_price * 0.999  # 考虑微小误差
        
    except Exception as e:
        log.error(f"检查涨停时出错: {e}")
        return False

# 持仓信息打印函数
def print_position_info(context):
    """
    打印持仓信息
    """
    log.info("=" * 50)
    log.info(f"持仓信息 - {context.blotter.current_dt}")
    log.info(f"总资产: {context.portfolio.portfolio_value:.2f}")
    log.info(f"可用资金: {context.portfolio.cash:.2f}")
    
    positions = get_positions()
    if positions:
        for stock, position in positions.items():
            log.info(f"股票: {stock}, 持仓: {position.amount}, 市值: {position.market_value:.2f}, "
                    f"成本: {position.cost_basis:.2f}, 盈亏: {position.pnl:.2f}")
    else:
        log.info("当前无持仓")
    log.info("=" * 50)
#####################################################
"""
MACD金叉plus流通小市值选股策略（PTrade国金版）
适配实盘+增强风控
核心优化：连续回撤保护、双止盈、市价买入、大盘过滤
"""

def initialize(context):
    """初始化函数，回测/实盘仅执行1次"""
    # ========== 基础配置 ==========
    # 设置基准指数为沪深300
    set_benchmark('000300.SS')  # PTrade使用.SS后缀
    
    # 设置滑点（回测专用，实盘无效）
    if not is_trade():
        set_slippage(slippage=0.001)  # 0.1%滑点
        # 设置交易成本（回测专用）
        set_commission(commission_ratio=0.0003, min_commission=5.0)
    
    # ========== 原策略核心参数 ==========
    g.stop_loss = -0.07  # 止损阈值：亏损7%
    g.max_stocks = 3  # 最多持有3只
    g.stock_list = []  # 选股结果存储
    
    # MACD参数（经典12,26,9）
    g.macd_short = 12
    g.macd_long = 26
    g.macd_signal = 9

    # ========== 实盘优化新增参数 ==========
    g.take_profit_base = 0.15  # 保底止盈：盈利15%
    g.take_profit_target = 0.3  # 目标止盈：盈利30%
    g.max_loss_streak = 2  # 最大连续亏损轮数
    g.loss_streak = 0  # 连续亏损轮数计数
    g.strategy_pause = False  # 策略暂停标记
    g.last_batch_profit = 0  # 上一轮调仓盈亏
    g.index_filter = '000300.SS'  # 大盘过滤标的：沪深300
    g.index_ma_period = 20  # 大盘过滤周期：20日线
    g.take_profit_half_done = {}  # 记录是否已执行过半止盈
    
    # 初始化周几标记（用于模拟run_weekly）
    g.last_select_weekday = -1  # 上次选股的星期几
    g.last_trade_weekday = -1  # 上次交易的星期几
    
    # 设置股票池（初始为空，后续动态更新）
    set_universe([])
    
    log.info("策略初始化完成")


def before_trading_start(context, data):
    """每日盘前运行：执行选股逻辑（周二盘前执行，使用周一收盘数据）"""
    # 获取当前是星期几（1=周一, 2=周二, ..., 5=周五）
    current_weekday = context.blotter.current_dt.isoweekday()
    current_date = context.blotter.current_dt.strftime('%Y-%m-%d')
    
    # 周二盘前执行选股（相当于周一收盘后选股）
    if current_weekday == 2 and g.last_select_weekday != 2:
        log.info(f"========== {current_date} 周二盘前选股 ==========")
        get_stock_list(context)
        g.last_select_weekday = 2


def handle_data(context, data):
    """盘中运行：执行交易逻辑（周二开盘交易）+ 止盈止损检查"""
    # 获取当前是星期几
    current_weekday = context.blotter.current_dt.isoweekday()
    current_time = context.blotter.current_dt
    current_date = current_time.strftime('%Y-%m-%d')
    current_hour = current_time.hour
    current_minute = current_time.minute
    
    # ========== 周二开盘交易（仅执行一次）==========
    # 判断是否为周二且是开盘后第一分钟
    is_opening_time = False
    if not is_trade():  # 回测场景：9:31分
        is_opening_time = (current_hour == 9 and current_minute == 31)
    else:  # 实盘场景：9:30分
        is_opening_time = (current_hour == 9 and current_minute == 30)
    
    if current_weekday == 2 and is_opening_time and g.last_trade_weekday != 2:
        log.info(f"========== {current_date} 周二开盘交易 ==========")
        trade(context)
        g.last_trade_weekday = 2
        # 重置半止盈状态（新调仓周期开始）
        g.take_profit_half_done = {}
    
    # 每日重置周几标记（避免一周内重复执行）
    if current_weekday != 2:
        g.last_trade_weekday = -1
        g.last_select_weekday = -1
    
    # ========== 盘中止盈止损检查（每分钟执行）==========
    check_stop_loss_and_take_profit(context, data)


def get_stock_list(context):
    """选股函数：MACD金叉+小市值+大盘过滤+连续亏损保护"""
    # 1. 策略暂停判断
    if g.strategy_pause:
        log.info("策略暂停：连续亏损达标/大盘破位，本周不选股")
        g.strategy_pause = False  # 暂停一周后自动恢复
        g.stock_list = []
        set_universe([])
        return
    
    # 2. 大盘过滤：沪深300跌破20日线，暂停选股
    try:
        current_date = context.blotter.current_dt.strftime('%Y%m%d')
        # 获取沪深300最近21天数据（计算20日均线需要20+1天）
        index_data = get_history(
            count=g.index_ma_period + 1,
            frequency='1d',
            field='close',
            security_list=g.index_filter,
            fq=None,
            include=False
        )
        
        if len(index_data) >= g.index_ma_period:
            # 计算20日均线
            close_values = index_data['close'].values
            ma20 = close_values[-g.index_ma_period:].mean()
            current_close = close_values[-1]
            
            if current_close < ma20:
                log.info(f"沪深300跌破20日线，本周不选股（收盘价：{current_close:.2f}, 20日线：{ma20:.2f}）")
                g.stock_list = []
                set_universe([])
                return
    except Exception as e:
        log.error(f"大盘过滤出错：{e}")
    
    # 3. 获取所有A股
    current_date = context.blotter.current_dt.strftime('%Y%m%d')
    all_stocks = get_Ashares(date=current_date)
    
    # 过滤科创板(688开头)、北交所(8/4开头)
    all_stocks = [stock for stock in all_stocks 
                if not (stock.startswith('688') or stock.startswith('8') or stock.startswith('4'))]
    
    # 过滤次新股（上市不满1年）
    all_stocks = filter_new_stock(context, all_stocks)
    
    # 过滤ST股票
    all_stocks = filter_st_stock(all_stocks)
    
    # 过滤停牌股票
    all_stocks = paused_filter(context, all_stocks)
    
    log.info(f"过滤后剩余股票数量：{len(all_stocks)}")
    
    # 4. MACD金叉筛选
    candidates = []  # 技术面达标池
    for stock in all_stocks:
        try:
            # 获取过去30天日线数据（确保MACD计算准确）
            df = get_history(
                count=30,
                frequency='1d',
                field=['close', 'high', 'low'],
                security_list=stock,
                fq='pre',  # 前复权
                include=False
            )
            
            if len(df) < 30:  # 数据不足跳过
                continue
            
            # 获取收盘价数组
            close_array = df['close'].values
            
            # 过滤过度炒作：过去10天涨停≤3次
            if len(close_array) >= 10:
                last_10_close = close_array[-10:]
                last_10_pre = close_array[-11:-1]
                limit_up_count = ((last_10_close / last_10_pre - 1) >= 0.099).sum()
                if limit_up_count > 3:
                    continue
            
            # 计算MACD
            # EMA短周期
            ema_short = calculate_ema(close_array, g.macd_short)
            # EMA长周期
            ema_long = calculate_ema(close_array, g.macd_long)
            # DIF
            dif = ema_short - ema_long
            # DEA（DIF的EMA）
            dea = calculate_ema(dif, g.macd_signal)
            
            # 判断MACD金叉：昨日DIF<DEA，今日DIF>DEA
            if len(dif) >= 2 and len(dea) >= 2:
                if dif[-2] < dea[-2] and dif[-1] > dea[-1]:
                    candidates.append(stock)
                    
        except Exception as e:
            # 出错则跳过该股票
            pass
    
    log.info(f"技术面筛选：MACD金叉股票数量 = {len(candidates)}")
    
    if not candidates:  # 无金叉标的
        g.stock_list = []
        set_universe([])
        return
    
    # 5. 基本面筛选：流通市值从小到大选3只
    # 【修复点】字段名改为 float_value（A股流通市值）
    try:
        final_stocks_data = get_fundamentals(
            candidates,
            'valuation',
            fields=['float_value'],  # 修正：使用正确的字段名
            date=current_date
        )
        
        if final_stocks_data is not None and not final_stocks_data.empty:
            # 按流通市值升序排序，取前3只
            final_stocks_data_sorted = final_stocks_data.sort_values('float_value')
            final_stocks = final_stocks_data_sorted.index.tolist()[:g.max_stocks]
            
            log.info(f"基本面筛选：市值最小的{g.max_stocks}只股票")
            log.info(final_stocks)
            g.stock_list = final_stocks
            set_universe(final_stocks)
        else:
            log.info("获取估值数据失败，本周不选股")
            g.stock_list = []
            set_universe([])
    except Exception as e:
        log.error(f"基本面筛选出错：{e}")
        g.stock_list = []
        set_universe([])


def trade(context):
    """每周二开盘交易：调仓+批次盈亏统计"""
    final_stocks = g.stock_list
    
    if not final_stocks:
        log.info("无选股结果，本周不调仓")
        # 但要清仓旧持仓
        for stock in list(context.portfolio.positions.keys()):
            log.info(f"清仓旧持仓: {stock}")
            order_target(stock, 0)
        return
    
    # 记录调仓前总资产（用于计算本批次盈亏）
    pre_total_asset = context.portfolio.portfolio_value
    
    # 执行调仓
    adjust_positions(context, final_stocks)
    
    # 记录调仓后总资产
    post_total_asset = context.portfolio.portfolio_value
    g.last_batch_profit = post_total_asset - pre_total_asset
    log.info(f"调仓完成，调仓前资产：{pre_total_asset:.2f}，调仓后资产：{post_total_asset:.2f}")


def adjust_positions(context, final_stocks):
    """调仓核心：等权分配，市价单买入"""
    if not final_stocks:
        # 无选股结果，清仓所有持仓
        for stock in list(context.portfolio.positions.keys()):
            log.info(f"无新选股，清仓旧持仓: {stock}")
            order_target(stock, 0)
        return
    
    # 1. 计算每只股票的目标持仓金额
    total_value = context.portfolio.portfolio_value
    # 等权分配，预留2%现金应对手续费和价格波动
    target_value_per_stock = total_value * 0.98 / len(final_stocks)
    log.info(f"开始调仓，总资产: {total_value:.2f}, 每只股票目标金额: {target_value_per_stock:.2f}")
    
    # 2. 卖旧：清仓不在新选股列表中的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in final_stocks:
            log.info(f"卖出旧持仓: {stock}")
            order_target(stock, 0)
    
    # 3. 买新：为新选股列表中的每只股票设置目标金额
    for stock in final_stocks:
        try:
            # PTrade使用order_target_value进行等金额买入
            # 实盘场景：不传limit_price时，系统会用最新价报单
            # 回测场景：自动按回测价格成交
            log.info(f"为 {stock} 设置目标金额 {target_value_per_stock:.2f}，市价买入")
            order_target_value(stock, target_value_per_stock)
        except Exception as e:
            log.error(f"买入 {stock} 失败：{e}")


def check_stop_loss_and_take_profit(context, data):
    """盘中止盈止损：止损7% + 保底止盈15% + 目标止盈30% + 连续亏损统计"""
    # 无持仓，不检查
    positions = context.portfolio.positions
    if not positions:
        return
    
    # 遍历持仓个股
    current_profit = 0  # 本批次当前总盈亏
    
    for stock in list(positions.keys()):
        try:
            position = positions[stock]
            
            # 获取当前价格
            if is_trade():
                # 实盘：使用get_snapshot获取最新价
                snapshot = get_snapshot(stock)
                if snapshot and stock in snapshot:
                    current_price = snapshot[stock].get('last_px', 0)
                else:
                    continue
            else:
                # 回测：使用data对象
                current_price = data[stock].price
            
            # 计算盈亏比
            cost_price = position.cost_basis
            if cost_price <= 0:
                continue
            
            profit_loss = (current_price - cost_price) / cost_price
            single_profit = (current_price - cost_price) * position.amount
            current_profit += single_profit
            
            # 1. 止损：亏损7%清仓
            if profit_loss <= g.stop_loss:
                log.info(f"触发止损: {stock}, 盈亏比: {profit_loss * 100:.2f}%, 清仓")
                order_target(stock, 0)
                # 重置半止盈状态
                if stock in g.take_profit_half_done:
                    del g.take_profit_half_done[stock]
                continue
            
            # 2. 目标止盈：盈利30%，全部清仓
            if profit_loss >= g.take_profit_target:
                log.info(f"触发目标止盈（30%）：{stock}, 盈亏比 {profit_loss * 100:.2f}%, 全部清仓")
                order_target(stock, 0)
                # 重置半止盈状态
                if stock in g.take_profit_half_done:
                    del g.take_profit_half_done[stock]
                continue
            
            # 3. 保底止盈：盈利15%，且尚未执行过半止盈，则清仓一半
            if profit_loss >= g.take_profit_base and stock not in g.take_profit_half_done:
                log.info(f"触发保底止盈（15%）：{stock}, 盈亏比 {profit_loss * 100:.2f}%, 清仓一半")
                target_amount = int(position.amount / 2)
                order_target(stock, target_amount)
                # 标记为已执行过半止盈
                g.take_profit_half_done[stock] = True
                
        except Exception as e:
            log.error(f"处理 {stock} 止盈止损时出错：{e}")
    
    # 4. 批次盈亏统计+连续亏损判断（持仓全部清空时触发）
    if not context.portfolio.positions:
        g.last_batch_profit = current_profit
        
        if g.last_batch_profit < 0:  # 本批次亏损
            g.loss_streak += 1
            log.info(f"本批次亏损 {abs(g.last_batch_profit):.2f} 元，连续亏损 {g.loss_streak} 轮")
            
            if g.loss_streak >= g.max_loss_streak:
                log.info(f"连续亏损 {g.max_loss_streak} 轮，触发策略暂停1周")
                g.strategy_pause = True
                g.loss_streak = 0
        else:  # 本批次盈利
            if g.last_batch_profit > 0:
                log.info(f"本批次盈利 {g.last_batch_profit:.2f} 元，连续亏损计数重置为0")
            g.loss_streak = 0
        
        # 重置半止盈状态
        g.take_profit_half_done = {}


def after_trading_end(context, data):
    """盘后运行：输出持仓情况"""
    # 输出当日持仓情况
    if context.portfolio.positions:
        log.info(f"========== 盘后持仓情况 ==========")
        for stock, position in context.portfolio.positions.items():
            profit_loss = (position.last_sale_price - position.cost_basis) / position.cost_basis
            log.info(f"{stock}: 持仓 {position.amount} 股, 成本 {position.cost_basis:.2f}, "
                    f"现价 {position.last_sale_price:.2f}, 盈亏比 {profit_loss * 100:.2f}%")
    else:
        log.info("当前无持仓")


# ========== 辅助函数 ==========

def calculate_ema(data, period):
    """计算EMA指数移动平均"""
    import numpy as np
    ema = np.zeros(len(data))
    # EMA的平滑系数
    multiplier = 2.0 / (period + 1)
    
    # 第一个EMA值用SMA
    ema[0] = data[0]
    
    # 后续EMA递推计算
    for i in range(1, len(data)):
        ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1]
    
    return ema


def paused_filter(context, security_list):
    """过滤停牌股票"""
    # 回测场景：使用get_stock_status
    if not is_trade():
        try:
            halt_status = get_stock_status(security_list, 'HALT')
            if halt_status:
                return [stock for stock in security_list if halt_status.get(stock) is not True]
            return security_list
        except:
            return security_list
    
    # 实盘场景：使用get_snapshot判断交易状态
    try:
        snapshot = get_snapshot(security_list)
        if snapshot:
            return [stock for stock in security_list 
                    if stock in snapshot and snapshot[stock].get('trade_status') not in ['HALT', 'SUSP', 'STOPT', 'DELISTED']]
        return security_list
    except:
        return security_list


def filter_st_stock(stock_list):
    """过滤ST/*ST/退市股"""
    try:
        # 使用PTrade的get_stock_status判断ST状态
        st_status = get_stock_status(stock_list, 'ST')
        if st_status:
            # 过滤掉ST股票
            filtered = [stock for stock in stock_list if st_status.get(stock) is not True]
            return filtered
        return stock_list
    except Exception as e:
        log.error(f"过滤ST股票出错：{e}")
        return stock_list


def filter_new_stock(context, stock_list):
    """过滤上市不满1年次新股"""
    try:
        import datetime
        current_date = context.blotter.current_dt.date()
        filtered = []
        
        for stock in stock_list:
            # 获取股票基础信息
            stock_info = get_stock_info(stock, field=['listed_date'])
            if stock_info and stock in stock_info:
                listed_date_str = stock_info[stock].get('listed_date')
                if listed_date_str:
                    # 转换上市日期字符串为日期对象
                    listed_date = datetime.datetime.strptime(listed_date_str, '%Y-%m-%d').date()
                    # 判断是否上市超过375天（约1年）
                    if (current_date - listed_date).days > 375:
                        filtered.append(stock)
        
        return filtered
    except Exception as e:
        log.error(f"过滤次新股出错：{e}")
        return stock_list
#################################
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime, timedelta
import pandas as pd

# --- 全局参数设置 ---
g = {
    'take_profit': 0.3,          # 止盈比例：30%
    'stop_loss': -0.07,          # 止损比例：-7%
    'max_stocks': 3,             # 最大持仓数量
    'benchmark': '000300.SH'     # 基准指数：沪深300
}

# --- 策略初始化 ---
def initialize(context):
    """
    策略初始化函数，在回测或实时交易开始时运行一次。
    """
    # 设置基准
    set_benchmark('000300.SS')
    
    # 定义定时任务
    # 每日10:30执行选股和交易逻辑
    # context 参数必须在第一个位置
    run_daily(context, select_and_trade, time='10:30') 
    
    # 每日收盘后执行止盈止损检查
    # 在 initialize 函数中
    run_daily(context, check_stop_loss_and_take_profit, time='15:00')
    
    log.info("策略初始化完成")


# --- 核心逻辑函数 ---

def select_and_trade(context):
    """
    选股并执行交易的核心函数。
    """
    log.info("开始执行选股逻辑...")
    
    # 1. 获取初始股票池
    # 在 select_and_trade 函数中
    
    # 在 select_and_trade 函数中
    # 在 select_and_trade 函数中

    # 1. 分别获取上交所和深交所的股票列表
    all_stocks = get_index_stocks('000985.SS')
    
    
    # 2. 应用一系列过滤器
    filtered_stocks = all_stocks
    filtered_stocks = filter_kcb_bse_stock(filtered_stocks)
    filtered_stocks = filter_st_stock(context, filtered_stocks)
    filtered_stocks = filter_new_stock(context, filtered_stocks)
    filtered_stocks = filter_paused_stock(context, filtered_stocks)
    
    log.info(f"基础过滤后剩余股票: {len(filtered_stocks)} 只")
    
    # 3. 技术指标筛选
    candidates = []
    for stock in filtered_stocks:
        try:
            # 获取过去20天的日线数据以计算指标
            hist_data = attribute_history(stock, 20, '1d', ['open', 'close', 'high', 'low', 'pre_close'], df=True)
            if len(hist_data) < 20:
                continue
            
            # 检查过去10天涨停次数
            limit_up_count = ((hist_data['close'] / hist_data['pre_close'] - 1) >= 0.099).sum()
            if limit_up_count > 3:
                continue
            
            # 计算布林带指标
            ma20 = hist_data['close'].mean()
            std20 = hist_data['close'].std()
            up_band = ma20 + 2 * std20
            down_band = ma20 - 2 * std20
            
            # 获取昨天和今天的价格
            t1_close = hist_data['close'][-2]
            current_price = get_ticks(stock, end_dt=context.current_dt, fields=['time', 'price'], count=1)[0]['price']
            
            # 布林带条件：今日股价跌破下轨，昨日收盘价在中下轨之间
            boll_condition = (current_price < down_band) and (t1_close > down_band)
            
            # 计算MACD指标
            ema_short = hist_data['close'].ewm(span=12, adjust=False).mean()
            ema_long = hist_data['close'].ewm(span=26, adjust=False).mean()
            dif = ema_short - ema_long
            dea = dif.ewm(span=9, adjust=False).mean()
            
            # MACD金叉条件
            macd_gold_cross = (dif.iloc[-2] < dea.iloc[-2]) and (dif.iloc[-1] > dea.iloc[-1])
            
            if boll_condition and macd_gold_cross:
                candidates.append(stock)
        except Exception as e:
            log.warn(f"处理股票 {stock} 时出错: {e}")
    
    log.info(f"技术指标筛选后剩余股票: {len(candidates)} 只")
    
    # 4. 按流通市值排序，选择市值最小的N只
    if not candidates:
        log.warn("未选出任何符合条件的股票，清仓所有持仓。")
        adjust_positions(context, [])
        return
        
    # 获取候选股票的最新基本面数据
    q = query(
        fundamentals.valuation.code,
        fundamentals.valuation.circulating_market_cap
    ).filter(
        fundamentals.valuation.code.in_(candidates)
    ).order_by(
        fundamentals.valuation.circulating_market_cap.asc()
    ).limit(g['max_stocks'])
    
    fund_data = get_fundamentals(q)
    final_stocks = fund_data['code'].tolist()
    
    log.info(f"最终选定股票: {final_stocks}")
    
    # 5. 调整持仓
    adjust_positions(context, final_stocks)


def adjust_positions(context, final_stocks):
    """
    根据选股结果调整持仓。
    """
    current_positions = list(context.portfolio.positions.keys())
    
    # 卖出持仓中不在最终列表的股票
    for stock in current_positions:
        if stock not in final_stocks:
            log.info(f"卖出股票: {stock}")
            order_target(stock, 0)
    
    # 买入新选出的股票，等权分配资金
    if not final_stocks:
        return
        
    # 计算每只股票的目标权重
    target_weight = 1.0 / len(final_stocks)
    
    # 获取当前可用资金
    available_cash = context.portfolio.cash
    
    # 获取当前总资产
    total_value = context.portfolio.total_value
    
    for stock in final_stocks:
        # 计算目标持仓价值
        target_value = total_value * target_weight
        # 计算当前持仓价值
        current_value = context.portfolio.positions.get(stock, 0).total_amount
        
        if target_value > current_value:
            # 需要买入
            order_value(stock, target_value - current_value)
            log.info(f"买入股票: {stock}, 目标价值: {target_value:.2f}")
        # 如果目标价值小于等于当前价值，不执行操作，以避免频繁交易


def check_stop_loss_and_take_profit(context):
    """
    检查持仓股票是否达到止盈止损条件。
    """
    log.info("开始执行止盈止损检查...")
    for stock in context.portfolio.positions:
        position = context.portfolio.positions[stock]
        # 获取持仓成本价
        cost_price = position.avg_cost
        # 获取当前最新价
        current_price = get_ticks(stock, end_dt=context.current_dt, fields=['price'], count=1)[0]['price']
        
        # 计算盈亏比例
        profit_loss_ratio = (current_price - cost_price) / cost_price
        
        # 检查止盈条件
        if profit_loss_ratio >= g['take_profit']:
            log.info(f"触发止盈: {stock}, 盈亏比: {profit_loss_ratio:.2%}, 清仓。")
            order_target(stock, 0)
        # 检查止损条件
        elif profit_loss_ratio <= g['stop_loss']:
            log.info(f"触发止损: {stock}, 盈亏比: {profit_loss_ratio:.2%}, 清仓。")
            order_target(stock, 0)


# --- 辅助过滤函数 ---

def filter_kcb_bse_stock(stock_list):
    """过滤科创板和北交所股票"""
    return [stock for stock in stock_list if not (stock.startswith('688') or stock.startswith('8') or stock.startswith('4'))]

def filter_st_stock(context, stock_list):
    """过滤ST、*ST及退市股票"""
    current_data = get_current_data()
    return [stock for stock in stock_list if not (
        current_data[stock].is_st or 
        'ST' in current_data[stock].name or 
        '*' in current_data[stock].name or 
        '退' in current_data[stock].name
    )]

def filter_new_stock(context, stock_list):
    """过滤上市不满一年的次新股"""
    # 获取上一个交易日
    yesterday = context.previous_date
    return [stock for stock in stock_list if (yesterday - get_security_info(stock).start_date) >= timedelta(days=365)]

def filter_paused_stock(context, stock_list):
    """过滤停牌股票"""
    current_data = get_current_data()
    return [stock for stock in stock_list if not current_data[stock].paused]
##########################################
"""
MACD+布林策略 (适配Ptrade平台)
策略逻辑：MACD金叉 + 布林带下轨反转 + 小市值选股
"""

# 1. [修改] 导入Ptrade的API库，替换聚宽的 jqdata
from ptrade import *
import pandas as pd
import numpy as np

def initialize(context):
    """
    初始化函数
    """
    # [修改] 设置基准指数，Ptrade使用 '000300.SS'
    set_benchmark('000300.SS')
    
    # [修改] 日志级别设置，Ptrade使用 log.setLevel()
    # 可选级别: log.DEBUG, log.INFO, log.WARN, log.ERROR, log.CRITICAL
    log.setLevel(log.INFO)
    
    # [修改] 定时任务，Ptrade的时间格式为 'HH:MM'
    run_daily(select_and_trade, time='10:30')
    
    # [修改] 定时任务，Ptrade中没有 'every_bar'，使用 '1m' 模拟，实现分钟级监控
    run_daily(check_stop_loss_and_take_profit, time='1m')

    # 全局变量定义
    g.take_profit = 0.3      # 止盈：盈利30%
    g.stop_loss = -0.07      # 止损：跌幅7%
    g.max_stocks = 3         # 最多持有股票数
    # 布林带参数
    g.boll_window = 20
    g.boll_std = 2

def select_and_trade(context):
    """
    每日10:30选股并调整持仓
    """
    # [修改] 获取所有A股，Ptrade使用 get_instruments()
    all_stocks = get_instruments('stock', date=context.now)
    # 过滤科创板(688)和北交所(8,4)
    all_stocks = [stock for stock in all_stocks if not (stock.startswith('688') or stock.startswith('8') or stock.startswith('4'))]
    
    # 应用过滤函数
    all_stocks = filter_new_stock(context, all_stocks)
    all_stocks = filter_st_stock(context, all_stocks) # [修改] 函数签名增加context
    all_stocks = paused_filter(context, all_stocks)
    
    candidates = []
    # [修改] Ptrade的get_price一次性获取所有股票数据，效率更高
    # 计算技术指标需要至少21天数据
    price_df = get_price(all_stocks, count=21, end_date=context.now, frequency='daily', fields=['open', 'close', 'high', 'low', 'pre_close'])

    for stock in all_stocks:
        try:
            # 从DataFrame中提取单只股票的数据
            df = price_df[price_df['code'] == stock]
            if len(df) < 21:
                continue
            
            # 检查过去10天涨停次数
            limit_up_count = ((df['close'] / df['pre_close'] - 1) >= 0.099).sum()
            if limit_up_count > 3:
                continue
            
            # 计算布林带
            df['ma20'] = df['close'].rolling(window=g.boll_window).mean()
            df['std'] = df['close'].rolling(window=g.boll_window).std()
            df['up'] = df['ma20'] + g.boll_std * df['std']
            df['down'] = df['ma20'] - g.boll_std * df['std']
            
            # 获取昨天和今天的数据点
            t1_data = df.iloc[-2] # T-1 天
            current_price = get_ticks(stock, count=1, fields='last_price')[stock]['last_price']
            
            # 布林带反转条件：昨收在中轨上，今开在中轨下
            boli_true = current_price < t1_data['down'] and t1_data['close'] > t1_data['down']
            if not boli_true:
                continue

            # 计算MACD
            short_window = 12
            long_window = 26
            signal_window = 9
            df['ema_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
            df['ema_long'] = df['close'].ewm(span=long_window, adjust=False).mean()
            df['dif'] = df['ema_short'] - df['ema_long']
            df['dea'] = df['dif'].ewm(span=signal_window, adjust=False).mean()

            # 判断MACD金叉 (T-1日死叉，T日金叉)
            if df['dif'].iloc[-2] < df['dea'].iloc[-2] and df['dif'].iloc[-1] > df['dea'].iloc[-1]:
                candidates.append(stock)
        except Exception as e:
            log.error(f"处理股票 {stock} 时出错: {e}")
            
    log.info(f"------------金叉选股 全股----------- {candidates}")
    
    if not candidates:
        log.info("没有选出符合条件的股票，清空所有持仓。")
        for stock in context.portfolio.positions:
            order_target(stock, 0)
        return

    # [修改] 获取基本面数据，Ptrade的 get_fundamentals 用法不同
    q = query(
        fundamentals.valuation.code,
        fundamentals.valuation.circulating_market_cap
    ).filter(
        fundamentals.valuation.code.in_(candidates)
    ).order_by(
        fundamentals.valuation.circulating_market_cap.asc()
    ).limit(g.max_stocks)
    
    final_stocks_df = get_fundamentals(q, date=context.now)
    final_stocks = final_stocks_df['code'].tolist()
    
    log.info(f"------------选3只市值最小----------- {final_stocks}")

    # 调整持仓
    adjust_positions(context, final_stocks)

def adjust_positions(context, final_stocks):
    """
    调整持仓到选定股票
    """
    # [修改] 获取当前持仓，Ptrade的结构略有不同
    current_positions = [position.sid for position in context.portfolio.positions.values() if position.total_amount > 0]

    # 卖出不在选股列表中的股票
    for stock in current_positions:
        if stock not in final_stocks:
            order_target(stock, 0)

    # 平均分配资金到新选定的股票
    # [修改] 计算可用资金时，需要考虑已下单但未成交的部分
    available_cash = context.portfolio.cash
    if final_stocks:
        # 计算需要买入的新股票数量
        new_stocks_to_buy = [stock for stock in final_stocks if stock not in current_positions]
        if new_stocks_to_buy:
            weight = 1.0 / len(final_stocks)
            total_value_to_allocate = context.portfolio.total_value * weight
            
            for stock in new_stocks_to_buy:
                # 计算目标市值，避免超买
                current_value = context.portfolio.positions.get(stock, 0)
                if current_value:
                    current_value = current_value.total_amount * current_value.last_price
                target_value = total_value_to_allocate - current_value
                if target_value > 0:
                    order_target_value(stock, total_value_to_allocate)

def check_stop_loss_and_take_profit(context):
    """
    检查持仓股票是否达到止盈止损条件
    """
    # [修改] 遍历持仓的方式
    positions = context.portfolio.positions
    for stock, position in positions.items():
        if position.total_amount <= 0:
            continue
            
        # [修改] 获取当前价格，Ptrade使用 get_ticks 或 get_price
        current_price = get_ticks(stock, count=1, fields='last_price')[stock]['last_price']
        cost_price = position.avg_cost
        profit_loss = (current_price - cost_price) / cost_price

        # 止盈条件
        if profit_loss >= g.take_profit:
            log.info(f"止盈触发: {stock}, 收益率: {profit_loss:.2%}")
            order_target(stock, 0)

        # 止损条件
        if profit_loss <= g.stop_loss:
            log.info(f"止损触发: {stock}, 收益率: {profit_loss:.2%}")
            order_target(stock, 0)

## [修改] 过滤函数的适配
def paused_filter(context, security_list):
    """过滤停牌股票"""
    # [修改] Ptrade没有直接获取停牌状态的函数，用get_price判断
    # 这是一个常用的替代方法
    current_prices = get_price(security_list, count=1, end_date=context.now, frequency='daily', fields='close')
    return [stock for stock in security_list if not current_prices[current_prices['code'] == stock]['close'].isna().any()]
    
def filter_st_stock(context, stock_list):
    """过滤ST及退市风险股票"""
    # [修改] Ptrade通过 get_instruments 获取详细信息
    instruments_info = get_instruments(stock_list, date=context.now, fields=['listed_date', 'name'])
    return [info['code'] for info in instruments_info if 
            'ST' not in info['name'] and 
            '*' not in info['name'] and 
            '退' not in info['name']]

def filter_new_stock(context, stock_list):
    """过滤次新股（上市不足375天）"""
    # [修改] Ptrade通过 get_instruments 获取上市日期
    instruments_info = get_instruments(stock_list, date=context.now, fields=['listed_date'])
    yesterday = context.now.date() - datetime.timedelta(days=1)
    return [info['code'] for info in instruments_info if 
            (yesterday - pd.to_datetime(info['listed_date']).date()).days >= 375]
###################################################
#导入函数库 3.11版本  #0406
import numpy as np
import pandas as pd
import time
import pickle
import ast
from datetime import datetime
from datetime import timedelta
import json

NOTEBOOK_PATH=''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

def initialize(context):
    # 设定基准为沪深300指数
    set_benchmark('000300.SS')
    NOTEBOOK_PATH = get_research_path()#+'xsz/'#'/home/fly/notebook/'
    #g.risk_idx = "399101.XBHS"         #'000985.XBHS'中证全指、'399101.XBHS'中小综指
    g.risk_idx = "000985.XBHS"
    #g.risk_idx = "399006.XBHS"         #"399006.XBHS" 创业板指
    #g.risk_idx= '516860.XBHS'
    
    # 策略基础配置和状态变量
    g.no_trading_today_signal = True  # 当天是否执行空仓（资金再平衡）操作
    g.pass_april = True               # 是否在04月或01月期间执行空仓策略
    g.run_stoploss = True              # 是否启用止损策略
    # 持仓和调仓记录
    g.hold_list = []                 # 当前持仓股票代码列表
    g.yesterday_HL_list = []         # 昨日涨停的股票列表（收盘价等于涨停价）
    g.target_list = []               # 本次调仓候选股票列表
    g.not_buy_again = []             # 当天已买入的股票列表，避免重复下单
    # 策略交易及风控的参数
    g.stock_num =10               # 每次调仓目标持仓股票数量
    g.up_price = 40                # 股票价格上限过滤条件（排除股价超过此值的股票）
    g.reason_to_sell = ''            # 记录卖出原因（例如：'limitup' 涨停破板 或 'stoploss' 止损）
    g.stoploss_strategy = 3          # 止损策略：1-个股止损；2-大盘止损；3-联合止损策略
    g.stoploss_limit = 0.88          # 个股止损阀值（成本价 × 0.92） 0.88
    g.stoploss_market = 0.97         # 大盘止损参数（若整体跌幅过大则触发卖出）
    g.totalcash = 50000             #策略使用总资金
    
    g.HV_control = False             # 是否启用成交量异常检测
    g.HV_duration = 120              # 检查成交量时参考的历史天数
    g.HV_ratio = 0.9                 # 当天成交量超过历史最高成交量的比例（如0.9即90%）
    
    # 僵尸因子：市值排名rolling过滤参数
    g.enable_rank_filter = False      # 是否启用市值排名rolling过滤
    g.rank_threshold = 2            # 市值排名rolling均值阈值
    g.rank_rolling_days = 30         # rolling窗口天数，只算交易日
    
    # 周线MACD因子
    g.enable_macd_filter = False       # 是否启用周线MACD因子
    
    # 5日/10日量比因子
    g.enable_volume_ratio_filter = True   # 是否启用量比因子
    g.volume_ratio_threshold = 1.0        # 量比阈值
    g.volume_ratio_boost_positions = 8     # 量比优秀股票往前提升的位置数
    
    #代码转换需要加的全局变量
    g.trading_signal = True  # 是否为可交易日
    g.count = 1 #记录交易日
    g.trade_count = 0 #记录交易日
    g.up_tardeday = ''
    
    g.get_finiance = True
    g.start_year = ""
    g.end_year = ""
    
    g.zt = {}
    #清空财务数据表
    #df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    #df.to_csv('\\finance_data\\output.csv', index=False)
    #持久化，尝试启动pickle文件
    
    if not is_trade():# 如果是回测，则强制初始化count=1和firstcount=0的文件
        with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
            pickle.dump(1,f,-1)
        with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
            pickle.dump(0,f,-1)
    try:# 从文件中读取count和firstcount的值
        with open(NOTEBOOK_PATH+'count.pkl','rb') as f:
            g.count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略当前交易日: %s" % (g.count)) 
        with open(NOTEBOOK_PATH+'firstcount.pkl','rb') as f:
            g.trade_count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略运行第%s个交易日" % (g.trade_count)) 
    except Exception as e:
        log.error("读取count和firstcount文件失败: %s" % (e))
    
    # 设置交易运行时间
    run_daily(context, update_counters, time='9:00')
    run_daily(context, print_position_info, time='9:00')
    # run_daily(context, save_data_local, time='9:00')
    # run_daily(context, prepare, time='9:05')#gai0:这里改到before_trading_start
    
    # 上午交易任务
    run_daily(context, sell_stocks, time='10:00')
    run_daily(context, weekly_adjustment, time='10:30')
    # 下午交易任务
    run_daily(context, trade_afternoon, time='14:30')
    run_daily(context, close_account, time='14:50')
    # 策略维护
    run_daily(context, record_counters, time='14:55')
    # run_daily(context, print_position_info_weekend, time='15:10')
    # if is_trade():#实盘模式增加
    #     run_daily(context, save_data_local, time='15:00')
    if not is_trade():
        set_limit_mode('UNLIMITED')
          
# 1、开盘前准备工作
#@维护周内计数(g.count)和总计数(g.trade_count)
def update_counters(context):
    """
    更新维护周内计数(g.count)和总计数(g.trade_count)
    如果经过假期，或者策略中断，重置g.count为1，否则g.count++
    g.trade_count++
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1 #weekday()返回0-6，所以要+1
    current_date = str(get_trading_day()) #返回格式'2025-06-06'
    date_time = datetime.strptime(current_date, "%Y-%m-%d")
    days = 0
    if g.up_tardeday !='':
        date_time_pre = datetime.strptime(g.up_tardeday, "%Y-%m-%d")
        days = (date_time-date_time_pre).days
    else:#策略首次启动或中断后重启，需要重置count计数
        g.count = 1

    if days >1 or weekdays == 1:#距离上次执行超过1天（说明跨周末或假期），或者今天是周一
        g.count = 1
    else:
        if days != 0:
            g.count += 1
    g.up_tardeday = current_date
    g.trade_count += 1

#@打印每只持仓股票的数据。
def print_position_info(context):
    """
    打印每只持仓股票的数据。
    """
    positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    log.info(f"{'='*50}")
    log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 持仓总结")
    log.info(f"{'='*50}")
    if len(positions)==0:
        log.info(f"                    空")
    else:
        for stock in positions:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            ret = 100 * (price / avg_cost - 1)
            value = position.amount
            amount = position.amount * price
            print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
    log.info(f"{'='*50}")
    return
def before_trading_start(context, data):
    prepare(context)
#@ 初始化g.zt={}, g.hold_list持仓股票列表, g.yesterday_HL_list昨日涨停持仓, g.no_trading_today_signal空仓日
def prepare(context):
    """
    1、初始化涨停板追踪字典g.zt={}
    2、更新持仓列表g.hold_list：刷新当前实际持仓股票清单
    3、识别涨停股票g.yesterday_HL_list：找出昨日收盘时处于涨停状态的持仓股票
    4、判断交易状态g.no_trading_today_signal：确定当日是否为资金再平衡的空仓日
    """
    g.zt = {}
    # 从当前持仓中提取股票代码，更新持仓列表
    g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    if g.hold_list != []:
        # 获取持仓股票昨日数据（包括收盘价、涨停价、跌停价）
        p = get_history(1, frequency="1d", field=['low','open','close','high_limit','volume'], security_list=g.hold_list, fq='dypre', include=False)#gai0：这里pre改成dypre，不影响结果，因为只是判断涨停与否
        up_limit_list = list(p[p['close'] == p['high_limit']]['code'])
        g.yesterday_HL_list = up_limit_list
    else:
        g.yesterday_HL_list = []
    # 根据当前日期判断是否为空仓日（例如04月或01月时资金再平衡）
    g.no_trading_today_signal = today_is_between(context)


# 2、上午交易任务
#@止盈与止损操作
def sell_stocks(context):
    """
    止盈与止损操作：
    根据策略（1: 个股止损；2: 大盘止损；3: 联合策略）判断是否执行卖出操作。
    """
    if g.run_stoploss:
        current_positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if g.stoploss_strategy == 1:# 个股止盈或止损判断
            for stock in current_positions:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if price >= avg_cost * 2:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止盈。")
                elif price < avg_cost * g.stoploss_limit and price > 0 :
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止损。")
                    g.reason_to_sell = 'stoploss'
        elif g.stoploss_strategy == 2:# 大盘止损判断，若整体市场跌幅过大则平仓所有股票
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks(g.risk_idx,last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'], count=1)
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，大盘止损。")
                
        elif g.stoploss_strategy == 3:# 联合止损策略：结合大盘和个股判断
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks(g.risk_idx,last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'],count=1)#gai:fq从None改成dypre，不影响结果
            # #gai：当天跌幅过大就清仓，不要算昨天的。效果有提升，但是回测太慢
            # stock_list = get_index_stocks('399101.XBHS',last_trade_day)
            # stock_df = get_history(1,'1d',['open'],stock_list,include=True)
            # latest_close = get_history(1, '1m', 'close', stock_list, include=True)
            # stock_df = stock_df.merge(latest_close[['code', 'close']], on='code', how='left')
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    close_position(context,stock)
                    log.critical(f"股票{stock}清仓，大盘止损，持仓收益率{price/avg_cost-1:.2%}。")
            else:
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    if price < avg_cost * g.stoploss_limit and price > 0:
                        close_position(context,stock)
                        log.critical(f"股票{stock}清仓，个股止损，持仓收益率{price/avg_cost-1:.2%}。")
                        g.reason_to_sell = 'stoploss'
#@每周调仓策略
def weekly_adjustment(context):
    """
    每周调仓策略：
    如果非空仓日，先选股得到目标股票列表，再卖出当前持仓中不在目标列表且昨日未涨停的股票，
    最后买入目标股票，同时记录当天买入情况避免重复下单。

    时机控制：只在策略启动日或每周第2天执行调仓
    智能卖出：保护昨日涨停股票，避免错失涨停后续收益
    资金管理：先卖后买，确保资金合理分配
    实盘适配：为实盘交易增加延时处理
    """
    if not g.no_trading_today_signal:
        log.info(f"当前第{g.trade_count}个交易日，周{g.count}")
        if g.trade_count == 1 or g.count == 2:#策略首次运行，或者每周第2天
            log.info(f"每周调仓，开始...")
            g.not_buy_again = []  # 重置当天已买入记录
            g.target_list = get_stock_list(context)
            # 取目标持仓数以内的股票作为调仓目标
            target_list = g.target_list[:g.stock_num]
            log.info(f"每周调仓目标股票: {target_list}")
            log.info(f"每周调仓，先卖出不在目标中的股票...")
            # 遍历当前持仓，若股票不在目标列表且非昨日涨停，则执行卖出操作
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if stock not in target_list and stock not in g.yesterday_HL_list:
                    log.critical(f"股票{stock}不在调仓目标中，清仓，持仓收益率{price/avg_cost-1:.2%}。")
                    close_position(context,stock)
                else:
                    log.info(f"股票{stock}仍在调仓目标中，继续持有，持仓收益率{price/avg_cost-1:.2%}。")
            if is_trade():
                time.sleep(30)
            log.info(f"每周调仓，买入目标中还未持仓的股票...")
            buy_security(context, target_list)# 对目标股票执行买入操作
            if is_trade():
                time.sleep(30)
            # 更新当天已买入记录，防止重复买入
            check_hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
            for stock in check_hold_list:
                if stock not in g.not_buy_again:
                    g.not_buy_again.append(stock)
##@获取市值最小的2*g.stock_num只股票
def get_stock_list(context):
    '''
    股票池：g.risk_idx
    进行过滤
    先选出市值最小的50只股票，再根据市值排名rolling均值进行二次筛选，最后选出市值最小的2 * g.stock_num作为候选池
    '''
    final_list = []
    MKT_index = g.risk_idx #'399101.XBHS'#中小综指
    current_time = context.blotter.current_dt - timedelta(days=1)
    cur_formatted_time = current_time.strftime("%Y%m%d")
    initial_list = filter_stocks(context, get_index_stocks(MKT_index,cur_formatted_time))

    circulating_market_cap_df = get_float_value(context,initial_list)
    if not circulating_market_cap_df.empty:
        sort_df = circulating_market_cap_df.sort_values(by='total_value', ascending=True)#排序
        initial_list = list(sort_df.index)
        final_list = initial_list[:50]  # 限制数据规模，防止一次处理数据过大
        
        # 僵尸因子：按市值排名rolling均值过滤
        if g.enable_rank_filter:
            final_list = filter_by_market_cap_rank_rolling(context, final_list, 
                                                         threshold=g.rank_threshold, 
                                                         rolling_days=g.rank_rolling_days)
        
        # 5日/10日量比因子：筛选量比>=阈值的股票
        if g.enable_volume_ratio_filter:
            final_list = filter_by_volume_ratio(context, final_list, g.volume_ratio_threshold)
        
        # 周线MACD因子：筛选上周MACD>0的股票
        if g.enable_macd_filter:
            final_list = filter_by_weekly_macd(context, final_list)
        
        #hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        # 取前2倍目标持仓股票数作为候选池
        final_list = final_list[:2 * g.stock_num]
        log.info(f"初选候选股票: {final_list}")
    return final_list
##@ 过滤股票
def filter_stocks(context, stock_list):
    """
    过滤以下股票：
    1、过滤停牌、退市、ST等有风险的股票
    2、只保留主板
    3、过滤未持仓的涨跌停股票
    4、过滤上市时间不足375天的次新股
    5、过滤名称中包含退市标识的股票
    """
    today = context.blotter.current_dt
    today_str = str(today.strftime("%Y%m%d"))
    yesterday = context.blotter.current_dt - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    filtered_stocks = []
    halt_status_today = get_stock_status(stock_list, 'HALT',today_str)
    halt_status_yesterday = get_stock_status(stock_list, 'HALT',yesterday_str)
    delisting_status = get_stock_status(stock_list, 'DELISTING',today_str)
    st_status = get_stock_status(stock_list, 'ST',today_str)
    #获取股票信息
    stock_infos = get_stock_info(stock_list, ['stock_name','listed_date','de_listed_date'])
    last_trade_day = get_trading_day(-1)
    for stock in stock_list:
        if is_trade():#gai0：这里改为is_trade()，回测有未来函数
            if '退' in stock_infos[stock]['stock_name'] or 'ST' in stock_infos[stock]['stock_name']: #gai0:这里加上名字st
                continue
        if halt_status_yesterday[stock]:
            continue
        if halt_status_today[stock]:  # 停牌
            continue
        if st_status[stock]:  # ST
            continue
        if delisting_status[stock]:  # 退市
            continue
        # if not (stock.startswith('00') or stock.startswith('60')):  # 非主板
        #     continue
        # if stock.startswith('00') or stock.startswith('60'):  # 主板剔除
        #     continue
        if not (stock in position_list or check_limit(stock)[stock]==0):  # 涨跌停 #gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
            continue
        if 'listed_date' in stock_infos[stock]:# 过滤上市天数少于375天的股票
            listed_date_str = stock_infos[stock]['listed_date']
            listed_date = datetime.strptime(listed_date_str, '%Y-%m-%d')
            if (last_trade_day-listed_date.date()).days<375:
                continue
        else:
            continue
        filtered_stocks.append(stock)
    return filtered_stocks
##@ 僵尸因子：按市值排名rolling均值过滤股票
def filter_by_market_cap_rank_rolling(context, stock_list, threshold, rolling_days):
    """
    根据市值排名rolling均值过滤股票
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 市值排名rolling均值阈值，小于此值的股票将被剔除
        rolling_days: rolling窗口天数，默认20个交易日（约一个月）
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    
    filtered_stocks = []
    
    try:
        trading_days = []
        for i in range(rolling_days, 0, -1):# 获取过去rolling_days个交易日的日期
            trade_day = get_trading_day(-i)
            trading_days.append(str(trade_day).replace('-',''))
        
        # # 获取昨日指数成分股作为排名基准池
        # yesterday = context.blotter.current_dt - timedelta(days=1)
        # yesterday_formatted_time = yesterday.strftime("%Y%m%d")
        # index_stocks = get_index_stocks(MKT_index, yesterday_formatted_time)
        
        # 创建DataFrame存储每只股票每天的排名：行是股票，列是交易日
        stock_rankings_df = pd.DataFrame(index=stock_list)
        
        for trade_day in trading_days:
            try:
                daily_market_cap = get_total_value_bydate(context,stock_list,trade_day)# 获取该日期的市值数据
                if not daily_market_cap.empty:
                    # 直接计算市值排名（市值越小，排名数字越小）
                    daily_market_cap['rank'] = daily_market_cap['total_value'].rank(method='min', na_option='keep')
                    # stock_rankings_df有但daily_market_cap没有的填NaN，反之舍弃
                    stock_rankings_df[trade_day] = daily_market_cap['rank'].reindex(stock_rankings_df.index)
                else:
                    log.error(f"获取{trade_day}日市值数据为空")
            except Exception as e:
                log.error(f"计算{trade_day}日市值排名失败: {e}")
        
        # 检查是否有有效的交易日数据
        total_trading_days = len(stock_rankings_df.columns)
        if total_trading_days == 0:
            log.error("没有获取到任何有效的交易日数据，返回原股票列表")
            return stock_list
            
        valid_days_count = stock_rankings_df.count(axis=1)  # 每行非NaN值的数量
        avg_ranks = stock_rankings_df.mean(axis=1)  # 每行的平均值（自动忽略NaN）
        # 数据充足的股票（有效数据>=一半交易日）
        min_required_days = max(1, total_trading_days // 2)  # 至少需要1天数据
        sufficient_data_mask = valid_days_count >= min_required_days
        sufficient_data_stocks = stock_rankings_df.index[sufficient_data_mask]
        # 在数据充足的股票中，筛选平均排名>=阈值的股票
        qualified_mask = avg_ranks[sufficient_data_mask] >= threshold
        qualified_stocks = sufficient_data_stocks[qualified_mask]
        # 数据不足的股票（保守保留）
        insufficient_data_stocks = stock_rankings_df.index[~sufficient_data_mask]
        # 合并结果
        filtered_stocks = list(qualified_stocks) + list(insufficient_data_stocks)
        
        # 日志输出
        for stock in sufficient_data_stocks:
            avg_rank = avg_ranks[stock]
            log.debug(f"股票{stock}排名: {stock_rankings_df.loc[stock]}")
            if avg_rank >= threshold:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，通过筛选（排名≥{threshold}）")
            else:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，被剔除（排名<{threshold}，市值排名过于靠前）")
        for stock in insufficient_data_stocks:
            valid_days = valid_days_count[stock]
            log.info(f"股票{stock}数据不足（有效数据{valid_days}天），保留")
        log.info(f"市值排名rolling过滤：原有{len(stock_list)}只股票，过滤后{len(filtered_stocks)}只股票")
    
    except Exception as e:
        log.error(f"市值排名rolling过滤失败: {e}，返回原股票列表")
        return stock_list
    
    return filtered_stocks
##@ 5日/10日量比因子：筛选量比>=阈值的股票
def filter_by_volume_ratio(context, stock_list, threshold):
    """
    根据5日/10日量比调整股票排序，量比>=阈值的股票在原顺序基础上往前提升指定位置
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 量比阈值，大于等于此值的股票将往前提升位置
    返回:
        调整排序后的股票代码列表
    """
    if not stock_list:
        return stock_list
    volume_boost_stocks = set()# 记录量比>=阈值的股票
    try:
        volume_data = get_history(20, '1d', 'volume', security_list=stock_list, fq='dypre', include=False, fill='pre')
        for stock in stock_list:
            try:
                stock_volume_data = volume_data[volume_data['code'] == stock]
                stock_volume_data = stock_volume_data[stock_volume_data['volume'] > 0]  # 过滤掉成交量为0的数据
                if len(stock_volume_data) < 10:
                    log.debug(f"股票{stock}有效成交量数据不足({len(stock_volume_data)}天)，保持原位置")
                    continue
                volumes = stock_volume_data['volume'].values
                avg_volume_5d = np.mean(volumes[-5:])# 计算5日平均成交量（最近5天）
                avg_volume_10d = np.mean(volumes[-10:])# 计算10日平均成交量（最近10天）
                
                if avg_volume_10d > 0:
                    volume_ratio = avg_volume_5d / avg_volume_10d# 计算量比
                    if volume_ratio >= threshold:
                        volume_boost_stocks.add(stock)
                        log.info(f"股票{stock}量比={volume_ratio:.2f}，将往前提{g.volume_ratio_boost_positions}位（≥{threshold}）")
                else:
                    log.debug(f"股票{stock}10日均量为0，保持原位置")
            except Exception as e:
                log.error(f"计算股票{stock}的量比失败: {e}，保持原位置")
                continue
        
        # 对原列表进行位置调整：量比>=阈值的股票往前提5位
        result_list = stock_list.copy()
        # 从后往前处理，避免索引变化的影响
        i = len(result_list) - 1
        while i>=0:
            stock = result_list[i]
            if stock in volume_boost_stocks:
                # 计算新位置：往前提升指定位置数，但不能超过索引0
                new_position = max(0, i - g.volume_ratio_boost_positions)
                # 移除股票并插入到新位置
                removed_stock = result_list.pop(i)
                result_list.insert(new_position, removed_stock)
                volume_boost_stocks.remove(stock)
            else:
                i = i-1
        # log.info(f"量比调整：原有{len(stock_list)}只股票，{len(volume_boost_stocks)}只股票量比>={threshold}往前提{g.volume_ratio_boost_positions}位")
        log.info(f"量比调整前股票列表：{stock_list}")
        log.info(f"量比调整后股票列表：{result_list}")
        return result_list
        
    except Exception as e:
        log.error(f"量比排序调整失败: {e}，返回原股票列表")
        return stock_list

##@ 周线MACD因子：筛选周线MACD>0的股票
def filter_by_weekly_macd(context, stock_list):
    """
    根据周线MACD指标过滤股票，筛选出周线MACD>0的股票
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    good_stocks = []
    other_stocks = []
    try:
        # 一次性获取所有股票的周线数据
        weekly_data = get_history(36, '1w', 'close', security_list=stock_list, fq='dypre', include=False, fill='pre')
        if weekly_data.empty:
            log.warning(f"无法获取股票的周线数据: {stock_list}")
            return stock_list
        # 获取最新1分钟数据作为本周当前价格
        current_data = get_history(1, '1m', 'close', security_list=stock_list, fq='dypre', include=True)
        for stock in stock_list:# 对每只股票计算MACD
            try:
                stock_data = weekly_data[weekly_data['code'] == stock]
                close_prices = stock_data['close'].values
                
                current_stock_data = current_data[current_data['code'] == stock]
                if not current_stock_data.empty:
                    current_close = current_stock_data['close'].values[0]
                    close_prices = np.append(close_prices, current_close)
                macdDIF_data, macdDEA_data, macd_data = get_MACD(close_prices, 12, 26, 9)
                latest_macd = macd_data[-1]
                if latest_macd > 0:
                    good_stocks.append(stock)
                    log.info(f"股票{stock}周线MACD={latest_macd:.4f}>0，位置提前")
                else:
                    other_stocks.append(stock)
            except Exception as e:
                log.error(f"计算股票{stock}的MACD失败: {e}")
                other_stocks.append(stock)
                continue
        filtered_stocks = good_stocks + other_stocks
        log.info(f"周线MACD过滤：原有{len(stock_list)}只股票，符合标准的有{len(good_stocks)}只排序提前")
    except Exception as e:
        log.error(f"周线MACD过滤失败: {e}，返回原股票列表")
        return stock_list
    return filtered_stocks
    

#@3、下午交易任务：检查是否有因为涨停破板触发的卖出信号；检查账户中是否需要补仓。
def trade_afternoon(context):
    """
    下午交易任务：
    1. 检查是否有因为涨停破板触发的卖出信号；
    2. 如启用了成交量监控，则检测是否有异常成交量；
    3. 检查账户中是否需要补仓。
    """
    if not g.no_trading_today_signal:
        check_continue_limitup(context)
        if g.HV_control:
            check_high_volume(context)
        rebalance_positions(context)    
##@检查昨日处于涨停状态的股票在今天下午是否继续涨停，如没有继续涨停则卖出该股票
def check_continue_limitup(context):
    """
    检查昨日处于涨停状态的股票在当前是否继续涨停。
    如没有继续涨停，则立即卖出该股票，并记录卖出原因为 "limitup"。
    """
    now_time = context.blotter.current_dt
    if g.yesterday_HL_list:
        for stock in g.yesterday_HL_list:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            if check_limit(stock)[stock] != 1:#gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
                log.critical(f"股票{stock}昨日涨停今日没有继续涨停，触发卖出操作，持仓收益率{price/avg_cost-1:.2%}。")
                close_position(context,stock)
                g.reason_to_sell = 'limitup'
            else:
                log.critical(f"股票{stock}昨日涨停，今日仍维持涨停状态，持仓收益率{price/avg_cost-1:.2%}。")                
##@检查账户中是否因没有继续涨停卖出而需要补仓。
def rebalance_positions(context):
    """
    检查账户资金与持仓数量：
    如果因涨停破板卖出导致持仓不足，则从目标股票中筛选未买入股票，进行补仓操作。
    """
    if g.reason_to_sell == 'limitup':
        g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if len(g.hold_list) < g.stock_num:
            target_list = filter_not_buy_again(g.target_list)
            target_list = target_list[:min(g.stock_num, len(target_list))]
            log.info(f"检测到补仓需求，可用资金 {round(context.portfolio.cash, 2)}，候选补仓股票: {target_list}")
            buy_security(context, target_list)
        g.reason_to_sell = ''
    else:
        log.info("未检测到涨停破板卖出事件，不进行补仓买入。")   
##@过滤在g.not_buy_again中的股票，也就是当天买入后有持仓的股票
def filter_not_buy_again(stock_list):
    """
    过滤掉当日已买入的股票，避免重复下单
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        未买入的股票代码列表
    """
    return [stock for stock in stock_list if stock not in g.not_buy_again]
#@如果当天是空仓日，清仓所有股票
def close_account(context):
    """
    清仓操作：若当天为空仓日，则平仓所有持仓股票
    """
    if g.no_trading_today_signal:
        if g.hold_list:
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                close_position(context,stock)
                log.info(f"股票{stock}清仓，空仓日，持仓收益率{price/avg_cost-1:.2%}。")


# 4、收盘前后维护策略
#@持久化记录count和firstcount
def record_counters(context):
    with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
        pickle.dump(g.count,f,-1)
    with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
        pickle.dump(g.trade_count,f,-1)  
#@如果是周五，打印所有持仓信息
def print_position_info_weekend(context):
    """
    每周五打印当前持仓详细信息，包括股票代码、成本价、现价、涨跌幅、持仓股数和市值
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1
    if weekdays == 5:
        position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        log.info(f"{'='*50}")
        log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 周末持仓总结")
        log.info(f"{'='*50}")
        if len(position_list) == 0:
            log.info(f"                    空")
        else:
            for stock in position_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                ret = 100 * (price / avg_cost - 1)
                value = position.amount
                amount = position.amount * price
                print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
        log.info(f"{'='*50}")


# 5、工具函数
#@判断今天是否是要空仓跳过的月份
def today_is_between(context):
    # 判断当前日期是否为资金再平衡（空仓）日，通常在04月或01月期间执行空仓操作
    today_str = context.blotter.current_dt.strftime('%m-%d')
    if g.pass_april:
        if ('04-01' <= today_str <= '04-30') or ('01-01' <= today_str <= '01-31'):
            return True
        else:
            return False
    else:
        return False    
#@获取市值数据函数
def get_float_value(context,stocks):
    """
    获取总市值、流通市值、总股本
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                last_trade_day = str(get_trading_day(-1))
                last_trade_day = last_trade_day.replace('-','')
                df = get_fundamentals(stocks, 'valuation', fields=['total_value','float_value','total_shares'], date=last_trade_day)
                if not df.empty:
                    log.info("获取流通市值第: %s次, 获取成功" % (count))
                    break 
            except:
                log.info("获取流通市值第: %s次, 获取不成功，正在重新获取" % (count))
                time.sleep(1)
    return df
#@僵尸因子：获取指定日期的总市值
def get_total_value_bydate(context,stocks,query_date):
    """
    获取指定日期的总市值
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                df = get_fundamentals(stocks, 'valuation', fields=['total_value'], date=query_date)
                if not df.empty:
                    break
                    # log.info("获取日期%s的流通市值第: %s次, 获取成功" % (query_date,count)) 
            except:
                log.info("获取日期%s的流通市值第: %s次, 获取不成功，正在重新获取" % (query_date,count))
                time.sleep(1)
    return df

# 6、交易相关底层函数
#@清仓指定股票
def close_position(context,stock):
    """
    指定股票清仓
    """
    last_prices = get_last_price(stock)
    limitprice = round(last_prices*0.985,2)
    if limitprice>0:
        position = get_position(stock)
        vol = position.amount
        if not is_trade():# 回测
            order(stock, -vol)
        else: #实盘
            if (stock.startswith('6') or stock.startswith('5')):#最优五档即时成交剩余转限价
                order_market(stock, -vol, 1, limitprice)
            else:#对手方最优价格
                order_market(stock, -vol, 0,limitprice)# gai:这里类型应该改为限价单，保证成交
    else:
        log.error(f"股票{stock}清仓失败，价格为0。")
#@对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
def buy_security(context, target_list):
    """
    买入操作：对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
    """
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
    position_count = len(position_list)
    target_num = len(target_list)
    log.info(f"目标数 {target_num}，当前持仓数 {position_count}")
    if target_num > position_count:
        try:
            value = g.totalcash / target_num  #每只股票购买资金，策略资金除以策略持仓股票个数
        except ZeroDivisionError as e:
            log.error(f"资金分摊时除零错误: {e}")
            return
        log.info(f"目标股票列表:{target_list}")
        for stock in target_list:
            if stock not in g.zt:#gai:回测g.zt始终为空
                position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
                log.info(f"准备检查股票{stock},当前持仓数{len(position_list)}")
                position = get_position(stock)
                total_amount = position.amount
                log.info(f"股票{stock},当前持仓{total_amount},可用资金{g.totalcash *(1-position_count/ target_num):.2f}，计划买入均摊市值 {value:.2f}")
                if total_amount == 0 and context.portfolio.cash>=value:# 当前持仓为0，且可用资金>=计划买入均摊市值
                    if open_position(context,stock,value):
                        log.info(f"股票{stock}买入，分配资金 {value:.2f}")
                        g.not_buy_again.append(stock)
                        if is_trade():
                            time.sleep(5)
                        if len(position_list) == target_num:
                            break
#@买入指定股票相应数量
def open_position(context,stock,vol):
    '''
    买入stock金额vol
    '''
    last_prices = get_last_price(stock)
    if last_prices<g.up_price and last_prices>3:
        limitprice = round(last_prices*1.005,2)
        if limitprice>0:
            if not is_trade():
                order_target_value(stock, vol)
            else:
                amount = int(vol / last_prices/100)*100
                avaliable_cash = context.portfolio.cash
                amount = int((amount * 0.9)/100)*100#gai:这里待优化
                if avaliable_cash < amount*limitprice*0.9:
                    amount = int(avaliable_cash*0.9/limitprice/100)*100
                if (stock.startswith('6') or stock.startswith('5')):#最优五档即时成交剩余转限价
                    order_market(stock, amount, 1, limitprice)
                else:#对手方最优价格
                    order_market(stock, amount, 0, limitprice)#gai:深市不支持1，只能02345
            return True
    else:
        return False
    return False
#@获取股票的最新价格:回测和实盘方法不同
def get_last_price(stock):
    '''
    获取股票的最新价格
    '''
    last_prices_panle = get_history(1, '1m', 'close', [stock], fq='dypre', include=True)
    last_prices = 0
    if not is_trade():
        last_prices = last_prices_panle.loc[last_prices_panle['code'] == stock, 'close'].values[0]
    else:
        snapshot = get_snapshot(stock)
        last_prices = snapshot[stock]['last_px']
    return last_prices
#@获取股票是否涨跌停：回测和实盘方法不同
def my_check_limit(stock):
    '''
    获取股票是否涨跌停
    2：触板涨停(已经是涨停价格，但还有卖盘)(仅支持交易研究查询当日)；
    1：涨停；
    0：既不涨停也不跌停；
    -1：跌停；
    -2：触板跌停(已经是跌停价格，但还有买盘)(仅支持交易研究查询当日)；
    '''
    if is_trade():#实盘
        return check_limit(stock)[stock]
    else:#回测
        last_price = get_last_price(stock)
        day_info = get_history(1, '1d', ['high_limit','low_limit'], [stock], fq='dypre', include=True)
        high_limit = day_info.iloc[0]['high_limit']
        low_limit = day_info.iloc[0]['low_limit']
        if last_price == 0  or high_limit == 0 or low_limit == 0 or pd.isna(high_limit) or pd.isna(low_limit) or pd.isna(last_price):
            log.error(f'股票{stock}价格异常，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        
        if last_price == high_limit:#涨停
            return 1
        elif last_price == low_limit:#跌停
            return -1
        elif last_price > high_limit or last_price < low_limit:#价格超过涨跌停限制
            log.error(f'股票{stock}价格超过涨跌停限制，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        else:#既不涨停也不跌停
            return 0
                   
# 7、没用到
"""
# 切分list
def split_list(input_list, chunk_size):
    '''
    将一个大列表按指定大小分割成多个小的子列表，用于批量处理数据和规避API调用限制。
    '''
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
def check_high_volume(context):
    '''
    检查持仓股票当日成交量是否异常放量：
    如果当日成交量大于过去 HV_duration 天内最大成交量的 HV_ratio 倍，则视为异常，执行卖出操作。
    '''
    hold_list = [position.sid for position in context.portfolio.positions.values() if position.enable_amount > 0]
    if len(hold_list)>0:
        halt_status = get_stock_status(hold_list, 'HALT')
        for stock in hold_list:
            if halt_status[stock]:#gai0：这里错了，delisting_status改为halt_status
                continue
            if check_limit(stock)[stock] == 1:
                continue
            his1d = get_history(g.HV_duration, '1d', 'volume', security_list=stock, fq='pre')#fq方式不影响成交量
            #获取当天成交量
            today_str = context.blotter.current_dt.strftime('%Y%m%d')+'093000'
            today_str_time = datetime.strptime(today_str, '%Y%m%d%H%M%S')
            diff_minues = int((context.blotter.current_dt-today_str_time).total_seconds() // 60)
            his1m = get_history(diff_minues, '1m', 'volume', security_list=stock, fq='pre')
            #当天的成交量
            cur_volume = sum(list(his1m))
            his_volume_list = list(his1d)
            if cur_volume > g.HV_ratio * his_volume_list.max():
                log.info(f"检测到股票{stock} 出现异常放量，执行卖出操作。")
                close_position(context,stock)
#保存财报到本地
def save_data_local(context):
    '''
    获取、更新和维护股票财务报表的本地缓存数据库
    回测：年份变化才更新一次
    实盘：startyear为启动年份-1，endyear为当前年份，每天更新  #gai：这里改一下更新频率？策略中断启动年份怎么办？是否不要这么频繁更新？
    归属母公司所有者的净利润、净利润、营业收入、公告日期、截止日期、股票简称
    '''
    MKT_index = g.risk_idx #'399101.XBHS'#中小综指
    current_time = context.blotter.current_dt - timedelta(days=1)
    
    cur_formatted_time = current_time.strftime("%Y%m%d")
    
    startyear = "2005"
    isadjust = False
    if not is_trade():
        #if g.get_finiance:
        today = context.blotter.current_dt
        current_date = str(today.strftime("%Y%m%d"))
        startyear = str(today.year-1)
        endyear = str(today.year)
        #endyear = str(current_time.year)
        #g.get_finiance = False
        if endyear != g.end_year:
            isadjust = True
    else:
        if g.get_finiance:
            today = context.blotter.current_dt
            current_date = str(today.strftime("%Y%m%d"))
            startyear = str(today.year-1)
            g.get_finiance = False
        endyear = str(current_time.year)
        isadjust = True
    #财报截止年份更新才会重新获取数据
    if isadjust:
        log.info("开始补充财报数据...") 
        initial_list = get_index_stocks(MKT_index,cur_formatted_time)
        initial_list = filter_stocks(context, initial_list)#gai0：未来函数，名字带退的
        df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
        #每秒不得调用超过100次（单次最大调用量是500条数据）
        #initial_list = initial_list[:5]
        chunked_lists = split_list(initial_list, 400)
        try:
            df_csv = pd.read_csv(NOTEBOOK_PATH+'finance_data.csv')
        except:
            df.to_csv(NOTEBOOK_PATH+'finance_data.csv', index=False)
        df_csv = pd.read_csv(NOTEBOOK_PATH+'finance_data.csv')
        for stocklist in chunked_lists:
            #time.sleep(1)
            print(startyear,endyear)
            df1 = get_fundamentals(stocklist, 'income_statement', fields=['np_parent_company_owners','net_profit','operating_revenue'], start_year=startyear, end_year=endyear)   
            df_single_index = df1.reset_index()
            for index, row in df_single_index.iterrows():
                #print(f"索引: {index}:{row}")
                new_row = {'code':row['secu_code'], 'np_parent_company_owners':row['np_parent_company_owners'], 'net_profit':row['net_profit'], 'operating_revenue':row['operating_revenue'],'publ_date':row['publ_date'],'end_date':row['end_date'],'secu_abbr':row['secu_abbr']}
                df_csv.loc[len(df_csv)] = new_row
        #df.to_csv("ss.csv")
        # 删除重复数据
        df_unique = df_csv.drop_duplicates()
        df_unique = df_unique.sort_values(by=['code', 'end_date'], ascending=[True, True])
        #sorted_df = df_csv.sort_values(by='end_date', ascending=True)
        df_unique.to_csv(NOTEBOOK_PATH+'finance_data.csv', index=False)
        log.info("当前财报表有 %s 条记录" % (len(df_unique))) 
        
    #跟新获取数据起始年份
    g.start_year = startyear
    g.end_year = endyear
    #log.info("当前财报起止年份: %s - %s" % (g.start_year,g.end_year))
#获取营业总收入数据函数
def get_income_by_csv(context,stocks):
    '''
    从本地CSV文件中提取股票的最新财务报表数据，如果最新是一季报直接使用，否则使用相比上一份财报的环比增长
    '''
    today = context.blotter.current_dt
    df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    df_one = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    df_pre = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    #读取本地财报数据
    df_finance = pd.read_csv(NOTEBOOK_PATH+'finance_data.csv')
    #筛选财报
    for stock in stocks:
        df_finance['publ_date'] = pd.to_datetime(df_finance['publ_date'])  # 将日期列转换为日期时间格式
        # 筛选日期早于当前日期的数据
        filtered_df1 = df_finance[df_finance['publ_date'] < today]
        #print("-------1--------")
        #print(filtered_df1)
        filtered_df = filtered_df1.loc[(filtered_df1['code'] == stock)]
        #print("-------2--------")
        #print(filtered_df)
        if len(filtered_df)>1:
            #一季报
            if filtered_df.iloc[-1]['end_date'][5:].replace("-", "") == "0331":
                new_row = {'code': filtered_df.iloc[-1]['code'], 'np_parent_company_owners': filtered_df.iloc[-1]['np_parent_company_owners'], 'net_profit': filtered_df.iloc[-1]['net_profit'], 'operating_revenue': filtered_df.iloc[-1]['operating_revenue'],'publ_date':  filtered_df.iloc[-1]['publ_date'],'end_date':  filtered_df.iloc[-1]['end_date'],'secu_abbr':  filtered_df.iloc[-1]['secu_abbr']}
                df_one.loc[len(df_one)] = new_row
            #其他季报
        else:
                new_row = {'code': filtered_df.iloc[-1]['code'], 'np_parent_company_owners': filtered_df.iloc[-1]['np_parent_company_owners'], 'net_profit': filtered_df.iloc[-1]['net_profit'], 'operating_revenue': filtered_df.iloc[-1]['operating_revenue'],'publ_date':  filtered_df.iloc[-1]['publ_date'],'end_date':  filtered_df.iloc[-1]['end_date'],'secu_abbr':  filtered_df.iloc[-1]['secu_abbr']}
                df.loc[len(df)] = new_row
                new_row = {'code': filtered_df.iloc[-2]['code'], 'np_parent_company_owners': filtered_df.iloc[-2]['np_parent_company_owners'], 'net_profit': filtered_df.iloc[-2]['net_profit'], 'operating_revenue': filtered_df.iloc[-2]['operating_revenue'],'publ_date':  filtered_df.iloc[-2]['publ_date'],'end_date':  filtered_df.iloc[-2]['end_date'],'secu_abbr':  filtered_df.iloc[-2]['secu_abbr']}
                df_pre.loc[len(df_pre)] = new_row
    #处理数据
    df.set_index('code', inplace=True)
    df_pre.set_index('code', inplace=True)
    df_one.set_index('code', inplace=True)
    df.drop('publ_date', axis=1, inplace=True)
    df_pre.drop('publ_date', axis=1, inplace=True)
    df_one.drop('publ_date', axis=1, inplace=True)
    df.drop('end_date', axis=1, inplace=True)
    df_pre.drop('end_date', axis=1, inplace=True)
    df_one.drop('end_date', axis=1, inplace=True)     
    df.drop('secu_abbr', axis=1, inplace=True)
    df_pre.drop('secu_abbr', axis=1, inplace=True)
    df_one.drop('secu_abbr', axis=1, inplace=True)  
    merged_df = None
    if len(df_one)>0:
        merged_df = df_one
    if len(df)>0 and len(df_pre)>0:
        #print('---yy---')
        #print(df - df_pre)
        merged_df = pd.concat([merged_df, df - df_pre], ignore_index=False)
    return merged_df
"""

# 8、实盘增加
# 炸板卖出
'''
def tick_data(context,data):#gai：回测没有运行这个函数
    """
    实盘增加：炸板卖出
    """
    log.info("tick_data")
    hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    if len(hold_list)>0:
        for stock in hold_list:
            position = get_position(stock)
            ava = position.amount
            if ava>0:
                #最新价
                current_price = ast.literal_eval(data[stock]['tick']['bid_grp'][0])[1][0]
                #最高价
                high_price = data[stock]['tick']['high_px'][0]
                #涨停价
                highlimit_price = data[stock]['tick']['up_px'][0]
                #卖一价
                m1_price = ast.literal_eval(data[stock]['tick']['offer_grp'][0])[1][0]
                log.info("%s,卖一价%s" % (stock,m1_price))
                if current_price>=highlimit_price and m1_price == 0:
                    if stock not in g.zt:
                        g.zt[stock]=context.blotter.current_dt
                        log.info("%s监控到已经封板,最新价%s,卖一价%s" % (stock,current_price,m1_price)) 
                if current_price<highlimit_price and stock in g.zt:
                    #炸板卖出
                    close_position(context,stock)
                    log.info("%s炸板卖出,最新价%s" % (stock,current_price)) 
'''
########################################################
#逐鹿，0703改买入委托方式为限价单
#导入函数库 3.11版本  #0406
import numpy as np
import pandas as pd
import time
import pickle
import ast
from datetime import datetime
from datetime import timedelta
import json

NOTEBOOK_PATH=''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

def initialize(context):
    # 设定基准为沪深300指数
    set_benchmark('000300.SS')
    NOTEBOOK_PATH = get_research_path()#+'xsz/'#'/home/fly/notebook/'
    g.risk_idx = "000985.XBHS"         #'000985.XBHS'中证全指、'399101.XBHS'中小综指
    # 策略基础配置和状态变量
    g.no_trading_today_signal = False  # 当天是否执行空仓（资金再平衡）操作
    g.pass_april = True                # 是否在04月或01月期间执行空仓策略
    g.run_stoploss = True              # 是否启用止损策略
    # 持仓和调仓记录
    g.hold_list = []                 # 当前持仓股票代码列表
    g.yesterday_HL_list = []         # 昨日涨停的股票列表（收盘价等于涨停价）
    g.target_list = []               # 本次调仓候选股票列表
    g.not_buy_again = []             # 当天已买入的股票列表，避免重复下单
    # 策略交易及风控的参数
    g.stock_num = 10                  # 每次调仓目标持仓股票数量
    g.up_price = 100.0               # 股票价格上限过滤条件（排除股价超过此值的股票）
    g.reason_to_sell = ''            # 记录卖出原因（例如：'limitup' 涨停破板 或 'stoploss' 止损）
    g.stoploss_strategy = 3          # 止损策略：1-个股止损；2-大盘止损；3-联合止损策略
    g.stoploss_limit = 0.94          # 个股止损阀值（成本价 × 0.92） 0.88
    g.stoploss_market = 0.97         # 大盘止损参数（若整体跌幅过大则触发卖出）

    g.HV_control = False             # 是否启用成交量异常检测
    g.HV_duration = 120              # 检查成交量时参考的历史天数
    g.HV_ratio = 0.9                 # 当天成交量超过历史最高成交量的比例（如0.9即90%）
    
    # 僵尸因子：市值排名rolling过滤参数
    g.enable_rank_filter = False      # 是否启用市值排名rolling过滤
    g.rank_threshold = 2            # 市值排名rolling均值阈值
    g.rank_rolling_days = 30         # rolling窗口天数，只算交易日
    
    # 周线MACD因子
    g.enable_macd_filter = False       # 是否启用周线MACD因子
    
    # 5日/10日量比因子
    g.enable_volume_ratio_filter = True   # 是否启用量比因子
    g.volume_ratio_threshold = 1.0        # 量比阈值
    g.volume_ratio_boost_positions = 8     # 量比优秀股票往前提升的位置数
    
    #代码转换需要加的全局变量
    g.trading_signal = True  # 是否为可交易日
    g.count = 1 #记录交易日
    g.trade_count = 0 #记录交易日
    g.up_tardeday = ''
    
    g.get_finiance = True
    g.start_year = ""
    g.end_year = ""
    
    g.zt = {}
    #清空财务数据表
    #df = pd.DataFrame(columns=['code', 'np_parent_company_owners', 'net_profit', 'operating_revenue','publ_date','end_date','secu_abbr'])
    #df.to_csv('\\finance_data\\output.csv', index=False)
    #持久化，尝试启动pickle文件
    
    if not is_trade():# 如果是回测，则强制初始化count=1和firstcount=0的文件
        with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
            pickle.dump(1,f,-1)
        with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
            pickle.dump(0,f,-1)
    try:# 从文件中读取count和firstcount的值
        with open(NOTEBOOK_PATH+'count.pkl','rb') as f:
            g.count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略当前交易日: %s" % (g.count)) 
        with open(NOTEBOOK_PATH+'firstcount.pkl','rb') as f:
            g.trade_count = pickle.load(f)
            log.info("策略重启初始化,从文件中读取本策略运行第%s个交易日" % (g.trade_count)) 
    except Exception as e:
        log.error("读取count和firstcount文件失败: %s" % (e))
    
    # 设置交易运行时间
    run_daily(context, update_counters, time='9:00')
    run_daily(context, print_position_info, time='9:00')
    # run_daily(context, save_data_local, time='9:00')
    # run_daily(context, prepare, time='9:05')#gai0:这里改到before_trading_start
    
    # 上午交易任务
    run_daily(context, sell_stocks, time='10:00')
    run_daily(context, weekly_adjustment, time='10:30')
    # 下午交易任务
    run_daily(context, trade_afternoon, time='14:30')
    run_daily(context, close_account, time='14:50')
    # 策略维护
    run_daily(context, record_counters, time='14:55')
    # run_daily(context, print_position_info_weekend, time='15:10')
    # if is_trade():#实盘模式增加
    #     run_daily(context, save_data_local, time='15:00')
    if not is_trade():
        set_limit_mode('UNLIMITED')
    
# 1、开盘前准备工作
#@维护周内计数(g.count)和总计数(g.trade_count)
def update_counters(context):
    """
    更新维护周内计数(g.count)和总计数(g.trade_count)
    如果经过假期，或者策略中断，重置g.count为1，否则g.count++
    g.trade_count++
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1 #weekday()返回0-6，所以要+1
    current_date = str(get_trading_day()) #返回格式'2025-06-06'
    date_time = datetime.strptime(current_date, "%Y-%m-%d")
    days = 0
    if g.up_tardeday !='':
        date_time_pre = datetime.strptime(g.up_tardeday, "%Y-%m-%d")
        days = (date_time-date_time_pre).days
    else:#策略首次启动或中断后重启，需要重置count计数
        g.count = 1

    if days >1 or weekdays == 1:#距离上次执行超过1天（说明跨周末或假期），或者今天是周一
        g.count = 1
    else:
        if days != 0:
            g.count += 1
    g.up_tardeday = current_date
    g.trade_count += 1

#@打印每只持仓股票的数据。
def print_position_info(context):
    """
    打印每只持仓股票的数据。
    """
    positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    log.info(f"{'='*50}")
    log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 持仓总结")
    log.info(f"{'='*50}")
    if len(positions)==0:
        log.info(f"                    空")
    else:
        for stock in positions:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            ret = 100 * (price / avg_cost - 1)
            value = position.amount
            amount = position.amount * price
            print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
    log.info(f"{'='*50}")
    return
def before_trading_start(context, data):
    prepare(context)
#@ 初始化g.zt={}, g.hold_list持仓股票列表, g.yesterday_HL_list昨日涨停持仓, g.no_trading_today_signal空仓日
def prepare(context):
    """
    1、初始化涨停板追踪字典g.zt={}
    2、更新持仓列表g.hold_list：刷新当前实际持仓股票清单
    3、识别涨停股票g.yesterday_HL_list：找出昨日收盘时处于涨停状态的持仓股票
    4、判断交易状态g.no_trading_today_signal：确定当日是否为资金再平衡的空仓日
    """
    g.zt = {}
    # 从当前持仓中提取股票代码，更新持仓列表
    g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    if g.hold_list != []:
        # 获取持仓股票昨日数据（包括收盘价、涨停价、跌停价）
        p = get_history(1, frequency="1d", field=['low','open','close','high_limit','volume'], security_list=g.hold_list, fq='dypre', include=False)#gai0：这里pre改成dypre，不影响结果，因为只是判断涨停与否
        up_limit_list = list(p[p['close'] == p['high_limit']]['code'])
        g.yesterday_HL_list = up_limit_list
    else:
        g.yesterday_HL_list = []
    # 根据当前日期判断是否为空仓日（例如04月或01月时资金再平衡）
    g.no_trading_today_signal = today_is_between(context)


# 2、上午交易任务
#@止盈与止损操作
def sell_stocks(context):
    """
    止盈与止损操作：
    根据策略（1: 个股止损；2: 大盘止损；3: 联合策略）判断是否执行卖出操作。
    """
    if g.run_stoploss:
        current_positions = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if g.stoploss_strategy == 1:# 个股止盈或止损判断
            for stock in current_positions:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if price >= avg_cost * 2:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止盈。")
                elif price < avg_cost * g.stoploss_limit and price > 0 :
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，个股止损。")
                    g.reason_to_sell = 'stoploss'
        elif g.stoploss_strategy == 2:# 大盘止损判断，若整体市场跌幅过大则平仓所有股票
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks('399101.XBHS',last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'], count=1)
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    close_position(context,stock)
                    log.info(f"股票{stock}清仓，大盘止损。")
                
        elif g.stoploss_strategy == 3:# 联合止损策略：结合大盘和个股判断
            last_trade_day = str(get_trading_day(-1))
            last_trade_day = last_trade_day.replace('-','')
            stock_df = get_price(security=get_index_stocks('399101.XBHS',last_trade_day)
                        ,end_date=last_trade_day, frequency='daily'
                        ,fields=['close', 'open'],count=1)#gai:fq从None改成dypre，不影响结果
            # #gai：当天跌幅过大就清仓，不要算昨天的。效果有提升，但是回测太慢
            # stock_list = get_index_stocks('399101.XBHS',last_trade_day)
            # stock_df = get_history(1,'1d',['open'],stock_list,include=True)
            # latest_close = get_history(1, '1m', 'close', stock_list, include=True)
            # stock_df = stock_df.merge(latest_close[['code', 'close']], on='code', how='left')
            # 计算成分股平均涨跌，即指数涨跌幅
            down_ratio = (stock_df['close'] / stock_df['open']).mean()
            if down_ratio <= g.stoploss_market:
                g.reason_to_sell = 'stoploss'
                log.info(f"市场风险（平均跌幅 {down_ratio:.2%}），准备清仓...")
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    close_position(context,stock)
                    log.critical(f"股票{stock}清仓，大盘止损，持仓收益率{price/avg_cost-1:.2%}。")
            else:
                for stock in current_positions:
                    position = get_position(stock)
                    price = position.last_sale_price
                    avg_cost = position.cost_basis
                    if price < avg_cost * g.stoploss_limit and price > 0:
                        close_position(context,stock)
                        log.critical(f"股票{stock}清仓，个股止损，持仓收益率{price/avg_cost-1:.2%}。")
                        g.reason_to_sell = 'stoploss'
#@每周调仓策略
def weekly_adjustment(context):
    """
    每周调仓策略：
    如果非空仓日，先选股得到目标股票列表，再卖出当前持仓中不在目标列表且昨日未涨停的股票，
    最后买入目标股票，同时记录当天买入情况避免重复下单。

    时机控制：只在策略启动日或每周第2天执行调仓
    智能卖出：保护昨日涨停股票，避免错失涨停后续收益
    资金管理：先卖后买，确保资金合理分配
    实盘适配：为实盘交易增加延时处理
    """
    if not g.no_trading_today_signal:
        log.info(f"当前第{g.trade_count}个交易日，周{g.count}")
        if g.trade_count == 1 or g.count == 2:#策略首次运行，或者每周第2天
            log.info(f"每周调仓，开始...")
            g.not_buy_again = []  # 重置当天已买入记录
            g.target_list = get_stock_list(context)
            # 取目标持仓数以内的股票作为调仓目标
            target_list = g.target_list[:g.stock_num]
            log.info(f"每周调仓目标股票: {target_list}")
            log.info(f"每周调仓，先卖出不在目标中的股票...")
            # 遍历当前持仓，若股票不在目标列表且非昨日涨停，则执行卖出操作
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                if stock not in target_list and stock not in g.yesterday_HL_list:
                    log.critical(f"股票{stock}不在调仓目标中，清仓，持仓收益率{price/avg_cost-1:.2%}。")
                    close_position(context,stock)
                else:
                    log.info(f"股票{stock}仍在调仓目标中，继续持有，持仓收益率{price/avg_cost-1:.2%}。")
            if is_trade():
                time.sleep(30)
            log.info(f"每周调仓，买入目标中还未持仓的股票...")
            buy_security(context, target_list)# 对目标股票执行买入操作
            if is_trade():
                time.sleep(30)
            # 更新当天已买入记录，防止重复买入
            check_hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
            for stock in check_hold_list:
                if stock not in g.not_buy_again:
                    g.not_buy_again.append(stock)
##@获取市值最小的2*g.stock_num只股票
def get_stock_list(context):
    '''
    股票池：g.risk_idx
    进行过滤
    先选出市值最小的50只股票，再根据市值排名rolling均值进行二次筛选，最后选出市值最小的2 * g.stock_num作为候选池
    '''
    final_list = []
    MKT_index = g.risk_idx #'399101.XBHS'#中小综指
    current_time = context.blotter.current_dt - timedelta(days=1)
    cur_formatted_time = current_time.strftime("%Y%m%d")
    initial_list = filter_stocks(context, get_index_stocks(MKT_index,cur_formatted_time))

    circulating_market_cap_df = get_float_value(context,initial_list)
    if not circulating_market_cap_df.empty:
        sort_df = circulating_market_cap_df.sort_values(by='total_value', ascending=True)#排序
        initial_list = list(sort_df.index)
        final_list = initial_list[:50]  # 限制数据规模，防止一次处理数据过大
        
        # 僵尸因子：按市值排名rolling均值过滤
        if g.enable_rank_filter:
            final_list = filter_by_market_cap_rank_rolling(context, final_list, 
                                                         threshold=g.rank_threshold, 
                                                         rolling_days=g.rank_rolling_days)
        
        # 5日/10日量比因子：筛选量比>=阈值的股票
        if g.enable_volume_ratio_filter:
            final_list = filter_by_volume_ratio(context, final_list, g.volume_ratio_threshold)
        
        # 周线MACD因子：筛选上周MACD>0的股票
        if g.enable_macd_filter:
            final_list = filter_by_weekly_macd(context, final_list)
        
        #hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        # 取前2倍目标持仓股票数作为候选池
        final_list = final_list[:2 * g.stock_num]
        log.info(f"初选候选股票: {final_list}")
    return final_list
##@ 过滤股票
def filter_stocks(context, stock_list):
    """
    过滤以下股票：
    1、过滤停牌、退市、ST等有风险的股票
    2、只保留主板
    3、过滤未持仓的涨跌停股票
    4、过滤上市时间不足375天的次新股
    5、过滤名称中包含退市标识的股票
    """
    today = context.blotter.current_dt
    today_str = str(today.strftime("%Y%m%d"))
    yesterday = context.blotter.current_dt - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y%m%d")
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
    filtered_stocks = []
    halt_status_today = get_stock_status(stock_list, 'HALT',today_str)
    halt_status_yesterday = get_stock_status(stock_list, 'HALT',yesterday_str)
    delisting_status = get_stock_status(stock_list, 'DELISTING',today_str)
    st_status = get_stock_status(stock_list, 'ST',today_str)
    #获取股票信息
    stock_infos = get_stock_info(stock_list, ['stock_name','listed_date','de_listed_date'])
    last_trade_day = get_trading_day(-1)
    for stock in stock_list:
        if is_trade():#gai0：这里改为is_trade()，回测有未来函数
            if '退' in stock_infos[stock]['stock_name'] or 'ST' in stock_infos[stock]['stock_name']: #gai0:这里加上名字st
                continue
        if halt_status_yesterday[stock]:
            continue
        if halt_status_today[stock]:  # 停牌
            continue
        if st_status[stock]:  # ST
            continue
        if delisting_status[stock]:  # 退市
            continue
        # if not (stock.startswith('00') or stock.startswith('60')):  # 非主板
        #     continue
        # if stock.startswith('00') or stock.startswith('60'):  # 主板剔除
        #     continue
        if not (stock in position_list or check_limit(stock)[stock]==0):  # 涨跌停 #gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
            continue
        if 'listed_date' in stock_infos[stock]:# 过滤上市天数少于375天的股票
            listed_date_str = stock_infos[stock]['listed_date']
            listed_date = datetime.strptime(listed_date_str, '%Y-%m-%d')
            if (last_trade_day-listed_date.date()).days<375:
                continue
        else:
            continue
        filtered_stocks.append(stock)
    return filtered_stocks
##@ 僵尸因子：按市值排名rolling均值过滤股票
def filter_by_market_cap_rank_rolling(context, stock_list, threshold, rolling_days):
    """
    根据市值排名rolling均值过滤股票
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 市值排名rolling均值阈值，小于此值的股票将被剔除
        rolling_days: rolling窗口天数，默认20个交易日（约一个月）
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    
    filtered_stocks = []
    
    try:
        trading_days = []
        for i in range(rolling_days, 0, -1):# 获取过去rolling_days个交易日的日期
            trade_day = get_trading_day(-i)
            trading_days.append(str(trade_day).replace('-',''))
        
        # # 获取昨日指数成分股作为排名基准池
        # yesterday = context.blotter.current_dt - timedelta(days=1)
        # yesterday_formatted_time = yesterday.strftime("%Y%m%d")
        # index_stocks = get_index_stocks(MKT_index, yesterday_formatted_time)
        
        # 创建DataFrame存储每只股票每天的排名：行是股票，列是交易日
        stock_rankings_df = pd.DataFrame(index=stock_list)
        
        for trade_day in trading_days:
            try:
                daily_market_cap = get_total_value_bydate(context,stock_list,trade_day)# 获取该日期的市值数据
                if not daily_market_cap.empty:
                    # 直接计算市值排名（市值越小，排名数字越小）
                    daily_market_cap['rank'] = daily_market_cap['total_value'].rank(method='min', na_option='keep')
                    # stock_rankings_df有但daily_market_cap没有的填NaN，反之舍弃
                    stock_rankings_df[trade_day] = daily_market_cap['rank'].reindex(stock_rankings_df.index)
                else:
                    log.error(f"获取{trade_day}日市值数据为空")
            except Exception as e:
                log.error(f"计算{trade_day}日市值排名失败: {e}")
        
        # 检查是否有有效的交易日数据
        total_trading_days = len(stock_rankings_df.columns)
        if total_trading_days == 0:
            log.error("没有获取到任何有效的交易日数据，返回原股票列表")
            return stock_list
            
        valid_days_count = stock_rankings_df.count(axis=1)  # 每行非NaN值的数量
        avg_ranks = stock_rankings_df.mean(axis=1)  # 每行的平均值（自动忽略NaN）
        # 数据充足的股票（有效数据>=一半交易日）
        min_required_days = max(1, total_trading_days // 2)  # 至少需要1天数据
        sufficient_data_mask = valid_days_count >= min_required_days
        sufficient_data_stocks = stock_rankings_df.index[sufficient_data_mask]
        # 在数据充足的股票中，筛选平均排名>=阈值的股票
        qualified_mask = avg_ranks[sufficient_data_mask] >= threshold
        qualified_stocks = sufficient_data_stocks[qualified_mask]
        # 数据不足的股票（保守保留）
        insufficient_data_stocks = stock_rankings_df.index[~sufficient_data_mask]
        # 合并结果
        filtered_stocks = list(qualified_stocks) + list(insufficient_data_stocks)
        
        # 日志输出
        for stock in sufficient_data_stocks:
            avg_rank = avg_ranks[stock]
            log.debug(f"股票{stock}排名: {stock_rankings_df.loc[stock]}")
            if avg_rank >= threshold:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，通过筛选（排名≥{threshold}）")
            else:
                log.info(f"股票{stock}平均排名{avg_rank:.1f}，被剔除（排名<{threshold}，市值排名过于靠前）")
        for stock in insufficient_data_stocks:
            valid_days = valid_days_count[stock]
            log.info(f"股票{stock}数据不足（有效数据{valid_days}天），保留")
        log.info(f"市值排名rolling过滤：原有{len(stock_list)}只股票，过滤后{len(filtered_stocks)}只股票")
    
    except Exception as e:
        log.error(f"市值排名rolling过滤失败: {e}，返回原股票列表")
        return stock_list
    
    return filtered_stocks
##@ 5日/10日量比因子：筛选量比>=阈值的股票
def filter_by_volume_ratio(context, stock_list, threshold):
    """
    根据5日/10日量比调整股票排序，量比>=阈值的股票在原顺序基础上往前提升指定位置
    参数:
        stock_list: 待过滤的股票代码列表
        threshold: 量比阈值，大于等于此值的股票将往前提升位置
    返回:
        调整排序后的股票代码列表
    """
    if not stock_list:
        return stock_list
    volume_boost_stocks = set()# 记录量比>=阈值的股票
    try:
        volume_data = get_history(20, '1d', 'volume', security_list=stock_list, fq='dypre', include=False, fill='pre')
        for stock in stock_list:
            try:
                stock_volume_data = volume_data[volume_data['code'] == stock]
                stock_volume_data = stock_volume_data[stock_volume_data['volume'] > 0]  # 过滤掉成交量为0的数据
                if len(stock_volume_data) < 10:
                    log.debug(f"股票{stock}有效成交量数据不足({len(stock_volume_data)}天)，保持原位置")
                    continue
                volumes = stock_volume_data['volume'].values
                avg_volume_5d = np.mean(volumes[-5:])# 计算5日平均成交量（最近5天）
                avg_volume_10d = np.mean(volumes[-10:])# 计算10日平均成交量（最近10天）
                
                if avg_volume_10d > 0:
                    volume_ratio = avg_volume_5d / avg_volume_10d# 计算量比
                    if volume_ratio >= threshold:
                        volume_boost_stocks.add(stock)
                        log.info(f"股票{stock}量比={volume_ratio:.2f}，将往前提{g.volume_ratio_boost_positions}位（≥{threshold}）")
                else:
                    log.debug(f"股票{stock}10日均量为0，保持原位置")
            except Exception as e:
                log.error(f"计算股票{stock}的量比失败: {e}，保持原位置")
                continue
        
        # 对原列表进行位置调整：量比>=阈值的股票往前提5位
        result_list = stock_list.copy()
        # 从后往前处理，避免索引变化的影响
        i = len(result_list) - 1
        while i>=0:
            stock = result_list[i]
            if stock in volume_boost_stocks:
                # 计算新位置：往前提升指定位置数，但不能超过索引0
                new_position = max(0, i - g.volume_ratio_boost_positions)
                # 移除股票并插入到新位置
                removed_stock = result_list.pop(i)
                result_list.insert(new_position, removed_stock)
                volume_boost_stocks.remove(stock)
            else:
                i = i-1
        # log.info(f"量比调整：原有{len(stock_list)}只股票，{len(volume_boost_stocks)}只股票量比>={threshold}往前提{g.volume_ratio_boost_positions}位")
        log.info(f"量比调整前股票列表：{stock_list}")
        log.info(f"量比调整后股票列表：{result_list}")
        return result_list
        
    except Exception as e:
        log.error(f"量比排序调整失败: {e}，返回原股票列表")
        return stock_list

##@ 周线MACD因子：筛选周线MACD>0的股票
def filter_by_weekly_macd(context, stock_list):
    """
    根据周线MACD指标过滤股票，筛选出周线MACD>0的股票
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        过滤后的股票代码列表
    """
    if not stock_list:
        return stock_list
    good_stocks = []
    other_stocks = []
    try:
        # 一次性获取所有股票的周线数据
        weekly_data = get_history(36, '1w', 'close', security_list=stock_list, fq='dypre', include=False, fill='pre')
        if weekly_data.empty:
            log.warning(f"无法获取股票的周线数据: {stock_list}")
            return stock_list
        # 获取最新1分钟数据作为本周当前价格
        current_data = get_history(1, '1m', 'close', security_list=stock_list, fq='dypre', include=True)
        for stock in stock_list:# 对每只股票计算MACD
            try:
                stock_data = weekly_data[weekly_data['code'] == stock]
                close_prices = stock_data['close'].values
                
                current_stock_data = current_data[current_data['code'] == stock]
                if not current_stock_data.empty:
                    current_close = current_stock_data['close'].values[0]
                    close_prices = np.append(close_prices, current_close)
                macdDIF_data, macdDEA_data, macd_data = get_MACD(close_prices, 12, 26, 9)
                latest_macd = macd_data[-1]
                if latest_macd > 0:
                    good_stocks.append(stock)
                    log.info(f"股票{stock}周线MACD={latest_macd:.4f}>0，位置提前")
                else:
                    other_stocks.append(stock)
            except Exception as e:
                log.error(f"计算股票{stock}的MACD失败: {e}")
                other_stocks.append(stock)
                continue
        filtered_stocks = good_stocks + other_stocks
        log.info(f"周线MACD过滤：原有{len(stock_list)}只股票，符合标准的有{len(good_stocks)}只排序提前")
    except Exception as e:
        log.error(f"周线MACD过滤失败: {e}，返回原股票列表")
        return stock_list
    return filtered_stocks
    

#@3、下午交易任务：检查是否有因为涨停破板触发的卖出信号；检查账户中是否需要补仓。
def trade_afternoon(context):
    """
    下午交易任务：
    1. 检查是否有因为涨停破板触发的卖出信号；
    2. 如启用了成交量监控，则检测是否有异常成交量；
    3. 检查账户中是否需要补仓。
    """
    if not g.no_trading_today_signal:
        check_continue_limitup(context)
        if g.HV_control:
            check_high_volume(context)
        rebalance_positions(context)    
##@检查昨日处于涨停状态的股票在今天下午是否继续涨停，如没有继续涨停则卖出该股票
def check_continue_limitup(context):
    """
    检查昨日处于涨停状态的股票在当前是否继续涨停。
    如没有继续涨停，则立即卖出该股票，并记录卖出原因为 "limitup"。
    """
    now_time = context.blotter.current_dt
    if g.yesterday_HL_list:
        for stock in g.yesterday_HL_list:
            position = get_position(stock)
            price = position.last_sale_price
            avg_cost = position.cost_basis
            if check_limit(stock)[stock] != 1:#gai0：这里看文档，有未来函数，原来是check_limit(stock)[stock]
                log.critical(f"股票{stock}昨日涨停今日没有继续涨停，触发卖出操作，持仓收益率{price/avg_cost-1:.2%}。")
                close_position(context,stock)
                g.reason_to_sell = 'limitup'
            else:
                log.critical(f"股票{stock}昨日涨停，今日仍维持涨停状态，持仓收益率{price/avg_cost-1:.2%}。")                
##@检查账户中是否因没有继续涨停卖出而需要补仓。
def rebalance_positions(context):
    """
    检查账户资金与持仓数量：
    如果因涨停破板卖出导致持仓不足，则从目标股票中筛选未买入股票，进行补仓操作。
    """
    if g.reason_to_sell == 'limitup':
        g.hold_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        if len(g.hold_list) < g.stock_num:
            target_list = filter_not_buy_again(g.target_list)
            target_list = target_list[:min(g.stock_num, len(target_list))]
            log.info(f"检测到补仓需求，可用资金 {round(context.portfolio.cash, 2)}，候选补仓股票: {target_list}")
            buy_security(context, target_list)
        g.reason_to_sell = ''
    else:
        log.info("未检测到涨停破板卖出事件，不进行补仓买入。")   
##@过滤在g.not_buy_again中的股票，也就是当天买入后有持仓的股票
def filter_not_buy_again(stock_list):
    """
    过滤掉当日已买入的股票，避免重复下单
    参数:
        stock_list: 待过滤的股票代码列表
    返回:
        未买入的股票代码列表
    """
    return [stock for stock in stock_list if stock not in g.not_buy_again]
#@如果当天是空仓日，清仓所有股票
def close_account(context):
    """
    清仓操作：若当天为空仓日，则平仓所有持仓股票
    """
    if g.no_trading_today_signal:
        if g.hold_list:
            for stock in g.hold_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                close_position(context,stock)
                log.info(f"股票{stock}清仓，空仓日，持仓收益率{price/avg_cost-1:.2%}。")


# 4、收盘前后维护策略
#@持久化记录count和firstcount
def record_counters(context):
    with open(NOTEBOOK_PATH+'count.pkl','wb') as f:
        pickle.dump(g.count,f,-1)
    with open(NOTEBOOK_PATH+'firstcount.pkl','wb') as f:
        pickle.dump(g.trade_count,f,-1)  
#@如果是周五，打印所有持仓信息
def print_position_info_weekend(context):
    """
    每周五打印当前持仓详细信息，包括股票代码、成本价、现价、涨跌幅、持仓股数和市值
    """
    today = context.blotter.current_dt
    weekdays = today.weekday()+1
    if weekdays == 5:
        position_list = [position.sid for position in context.portfolio.positions.values() if position.amount != 0]
        log.info(f"{'='*50}")
        log.info(f"          {context.blotter.current_dt.strftime('%Y-%m-%d')} 周末持仓总结")
        log.info(f"{'='*50}")
        if len(position_list) == 0:
            log.info(f"                    空")
        else:
            for stock in position_list:
                position = get_position(stock)
                price = position.last_sale_price
                avg_cost = position.cost_basis
                ret = 100 * (price / avg_cost - 1)
                value = position.amount
                amount = position.amount * price
                print(f"股票: {stock} | 成本价: {avg_cost:.2f} | 现价: {price:.2f} | 涨跌幅: {ret:.2f}% | 市值: {amount:.2f} | 持仓数: {value:.0f}")
        log.info(f"{'='*50}")


# 5、工具函数
#@判断今天是否是要空仓跳过的月份
def today_is_between(context):
    # 判断当前日期是否为资金再平衡（空仓）日，通常在04月或01月期间执行空仓操作
    today_str = context.blotter.current_dt.strftime('%m-%d')
    if g.pass_april:
        if ('04-01' <= today_str <= '04-30') or ('01-01' <= today_str <= '01-31'):
            return True
        else:
            return False
    else:
        return False    
#@获取市值数据函数
def get_float_value(context,stocks):
    """
    获取总市值、流通市值、总股本
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                last_trade_day = str(get_trading_day(-1))
                last_trade_day = last_trade_day.replace('-','')
                df = get_fundamentals(stocks, 'valuation', fields=['total_value','float_value','total_shares'], date=last_trade_day)
                if not df.empty:
                    log.info("获取流通市值第: %s次, 获取成功" % (count))
                    break 
            except:
                log.info("获取流通市值第: %s次, 获取不成功，正在重新获取" % (count))
                time.sleep(1)
    return df
#@僵尸因子：获取指定日期的总市值
def get_total_value_bydate(context,stocks,query_date):
    """
    获取指定日期的总市值
    """
    df = pd.DataFrame()
    count = 0
    while count<=10:
        count +=1
        if df.empty:
            try:
                df = get_fundamentals(stocks, 'valuation', fields=['total_value'], date=query_date)
                if not df.empty:
                    break
                    # log.info("获取日期%s的流通市值第: %s次, 获取成功" % (query_date,count)) 
            except:
                log.info("获取日期%s的流通市值第: %s次, 获取不成功，正在重新获取" % (query_date,count))
                time.sleep(1)
    return df

# 6、交易相关底层函数
#@清仓指定股票
def close_position(context,stock):
    """
    指定股票清仓
    """
    last_prices = get_last_price(stock)
    limitprice = round(last_prices*0.985,2)
    if limitprice>0:
        position = get_position(stock)
        vol = position.amount
        if not is_trade():# 回测
            order(stock, -vol)
        else: #实盘
            if (stock.startswith('6') or stock.startswith('5')):#最优五档即时成交剩余转限价
                order_market(stock, -vol, 1, limitprice)
            else:#对手方最优价格
                order_market(stock, -vol, 0,limitprice)# gai:这里类型应该改为限价单，保证成交
    else:
        log.error(f"股票{stock}清仓失败，价格为0。")
#@对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
def buy_security(context, target_list):
    """
    买入操作：对target_list中没有持仓的股票执行买入，下单资金均摊分配到每个未持仓的股票
    """
    position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
    position_count = len(position_list)
    target_num = len(target_list)
    log.info(f"目标数 {target_num}，当前持仓数 {position_count}")
    if target_num > position_count:
        try:
            value = context.portfolio.cash / (target_num - position_count)
        except ZeroDivisionError as e:
            log.error(f"资金分摊时除零错误: {e}")
            return
        log.info(f"目标股票列表:{target_list}")
        for stock in target_list:
            if stock not in g.zt:#gai:回测g.zt始终为空
                position_list = [position.sid for position in context.portfolio.positions.values() if position.amount > 0]
                log.info(f"准备检查股票{stock},当前持仓数{len(position_list)}")
                position = get_position(stock)
                total_amount = position.amount
                log.info(f"股票{stock},当前持仓{total_amount},可用资金{context.portfolio.cash:.2f}，计划买入均摊市值 {value:.2f}")
                if total_amount == 0 and context.portfolio.cash>=value:# 当前持仓为0，且可用资金>=计划买入均摊市值
                    if open_position(context,stock,value):
                        log.info(f"股票{stock}买入，分配资金 {value:.2f}")
                        g.not_buy_again.append(stock)
                        if is_trade():
                            time.sleep(5)
                        if len(position_list) == target_num:
                            break
#@买入指定股票相应数量
def open_position(context,stock,vol):
    '''
    买入stock金额vol
    '''
    last_prices = get_last_price(stock)
    limitprice = round(last_prices*1.015,2)
    if limitprice>0:
     
        order_value(stock, vol)
      
        return True
    return False

#@获取股票的最新价格:回测和实盘方法不同
def get_last_price(stock):
    '''
    获取股票的最新价格
    '''
    last_prices_panle = get_history(1, '1m', 'close', [stock], fq='dypre', include=True)
    last_prices = 0
    if not is_trade():
        last_prices = last_prices_panle.loc[last_prices_panle['code'] == stock, 'close'].values[0]
    else:
        snapshot = get_snapshot(stock)
        last_prices = snapshot[stock]['last_px']
    return last_prices
#@获取股票是否涨跌停：回测和实盘方法不同
def my_check_limit(stock):
    '''
    获取股票是否涨跌停
    2：触板涨停(已经是涨停价格，但还有卖盘)(仅支持交易研究查询当日)；
    1：涨停；
    0：既不涨停也不跌停；
    -1：跌停；
    -2：触板跌停(已经是跌停价格，但还有买盘)(仅支持交易研究查询当日)；
    '''
    if is_trade():#实盘
        return check_limit(stock)[stock]
    else:#回测
        last_price = get_last_price(stock)
        day_info = get_history(1, '1d', ['high_limit','low_limit'], [stock], fq='dypre', include=True)
        high_limit = day_info.iloc[0]['high_limit']
        low_limit = day_info.iloc[0]['low_limit']
        if last_price == 0  or high_limit == 0 or low_limit == 0 or pd.isna(high_limit) or pd.isna(low_limit) or pd.isna(last_price):
            log.error(f'股票{stock}价格异常，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        
        if last_price == high_limit:#涨停
            return 1
        elif last_price == low_limit:#跌停
            return -1
        elif last_price > high_limit or last_price < low_limit:#价格超过涨跌停限制
            log.error(f'股票{stock}价格超过涨跌停限制，无法获取涨跌停状态, last_price:{last_price},high_limit:{high_limit},low_limit:{low_limit}')
            return 0
        else:#既不涨停也不跌停
            return 0
###############################################
'''
索普量化逆回购
作者:索普量化
微信:xms_quants1
时间:20251017
'''
import math
import pandas as pd
def initialize(context):
    # 初始化策略
    #一天期的深圳逆回购标的
    g.stock='131810.SZ'
    #保留的资金，避免新股，可转债等申购
    g.cash=0
    print('开始运行逆回购策略*********************')
    run_daily(context, func=run_reverse_repurchase, time='10:30')
def run_reverse_repurchase(context):
    '''
    逆回购函数
    '''
    current_dt=context.blotter.current_dt
    current_dt=current_dt.strftime('%Y-%m-%d')
    account=get_xg_account(context)
    if account.shape[0]>0:
        cash=account['可用金额'].tolist()[-1]
        print('可以金额****************',cash)
        cash=cash-g.cash
        #逆回购最低1000元10张一手
        if cash>=1000:
            amount = int(cash/1000)*10
            if amount>=10:
                #全部逆回购卖出
                order(g.stock, -1*amount)
                print(current_dt,'逆回购回购成功')
            else:
                print(current_dt,'逆回购回购失败，低于最低数量')
        else:
           print(current_dt,'逆回购回购失败，低于最低金额')
    else:
        print(current_dt,'逆回购回购失败，没有金额')
def get_xg_account(context):
    '''
    获取小果账户数据
    '''
    df=pd.DataFrame()
    df['可用金额']=[context.portfolio.cash]
    df['总资产']=[context.portfolio.portfolio_value]
    df['持仓价值']=[context.portfolio.positions_value]
    df['已使用现金']=[context.portfolio.capital_used]
    df['当前收益比例']=[context.portfolio.returns]
    df['初始账户总资产']=[context.portfolio.pnl]
    df['开始时间']=[context.portfolio.start_date]
    return df
def get_xg_position(context):
    '''
    获取小果持股数据
    '''
    data=pd.DataFrame()
    positions=context.portfolio.positions
    stock_list=list(set(positions.keys()))
    print('持股数量{}'.format(len(stock_list)))
    for stock in stock_list:
        df=pd.DataFrame()
        df['证券代码']=[positions[stock].sid]
        df['可用数量']=[positions[stock].enable_amount]
        df['持有数量']=[positions[stock].amount]
        df['最新价']=[positions[stock].last_sale_price ]
        df['成本价']=[positions[stock].cost_basis ]
        df['今日买入']=[positions[stock].today_amount ]
        df['持股类型']=[positions[stock].business_type  ]
        data=pd.concat([data,df],ignore_index=True)
    '''
    if data.shape[0]>0:
        if g.is_del=='是':
            print('开始策略隔离**********')
            data['隔离']=data['证券代码'].apply(lambda x: '是' if x in g.stock_list else '不是')
            data=data[data['隔离']=='是']
        else:
            print('不开启策略隔离*********')
    '''
    return data
def get_xg_order(context):
    '''
    获取小果委托数据
    '''
    orders=get_orders()
    print("委托数量{}".format(len(orders)))
    data=pd.DataFrame()
    if len(orders)>0:
        for ors in orders:
            df=pd.DataFrame()
            df['订单号']=[ors.id]
            df['订单产生时间']=[ors.dt]
            df['指定价格']=[ors.limit ]
            df['证券代码']=[ors.symbol ]
            df['委托数量']=[ors.amount ]
            df['订单生成时间']=[ors.created ]
            df['成交数量']=[ors.filled ]
            df['委托编号']=[ors.entrust_no]
            df['盘口档位']=[ors.priceGear ]
            df['订单状态']=[ors.status ]
            data=pd.concat([data,df],ignore_index=True)
        
    else:
        data=data
    return data
def get_xg_position_on(context,security=''):
    ''''
    获取单股的持股情况
    '''
    pos=get_positions(security=security)
    df=pd.DataFrame()
    if len(pos)>0:
        df['证券代码']=[pos[security].sid]
        df['可以数量']=[pos[security].enable_amount]
        df['持有数量']=[pos[security].amount]
        df['最新价']=[pos[security].last_sale_price ]
        df['成本价']=[pos[security].cost_basis ]
        df['今日买入']=[pos[security].today_amount ]
        df['持股类型']=[pos[security].business_type  ]
    else:
        df=df
    return df
#########################################
"""
策略名称：
两融双均线策略
运行周期:
日线
==============================================================================
备注：该demo仅支持交易使用
"""
import numpy as np


def initialize(context):
    # 融资融券策略
    # 初始化此策略
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.security = '600570.SS'
    # 默认买入股数
    g.amount = 1000
    if not is_trade():
        log.info('两融demo策略无法在回测场景使用')



def before_trading_start(context, data):
    if not is_trade():
        return
    h = get_history(20, '1d', field=['close', 'volume'], security_list=g.security,
                    fq='dypre', include=False, is_dict=True)
    g.close_data = h[g.security]['close']


def handle_data(context, data):
    if not is_trade():
        return
    security = g.security
    # 获取历史日K线数据
    current_price = data[security].close
    # 合成最新K线序列
    close_data = np.concatenate((g.close_data, np.array(list([current_price]))), axis=0)
    # 获取5日、10日均线
    ma5 = get_ma(close_data, 5)
    ma10 = get_ma(close_data, 10)

    # 如果五日均线大于十日均线，进行买入
    if ma5 > ma10:
        # 获取最大可融资数量
        amount = get_margincash_open_amount(security).get(security)
        log.info('最大可融资买入的数量:%s' % amount)
        # 可融资买入最大股数超过目标买入股数则用融资买入方式买入标的
        if amount >= g.amount:
            margincash_open(security, g.amount)
            log.info('融资买入全部')
        # 可融资买入最大股数小于目标买入股数但大于零则用先用融资买入方式买入部分，剩余部分用担保品交易方式进行买入
        elif g.amount > amount > 0:
            margincash_open(security, amount)
            log.info('融资买入部分')
            margin_trade(security, g.amount - amount)
            log.info('担保品买入部分')
        elif amount == 0:
            margin_trade(security, g.amount)
            log.info('担保品买入全部')
        g.flag = False

    # 如果五日均线小于十日均线，进行卖出
    else:
        hold_amount = get_position(security).enable_amount
        if hold_amount > 0:
            # 获取标的卖券还款最大可卖数量
            amount = get_margincash_close_amount(security).get(security)
            log.info('最大可卖券还款卖出的数量:%s' % amount)
            # 如果卖券还款最大数量不小于持仓数量，则进行卖券还款操作
            if amount >= hold_amount:
                margincash_close(security, -amount)
                log.info('卖券还款卖出全部')
            # 如果卖券还款最大数量小于持仓数量，则先进行部分数量的卖券还款操作，剩余通过担保品交易卖出
            elif hold_amount > amount > 0:
                margincash_close(security, -amount)
                log.info('卖券还款卖出部分')
                margin_trade(security, -(hold_amount - amount))
                log.info('担保品卖出部分')
            # 如果卖券还款最大数量为零，则持仓部分用担保品方式卖出
            elif amount == 0:
                margin_trade(security, -hold_amount)
                log.info('担保品卖出全部')


# 获取MA函数
def get_ma(close_array, num):
    ma = close_array[-num:].mean()
    return round(ma, 2)
######################################
"""
策略名称：
期货日内交易策略
运行周期:
分钟
策略流程：
盘中每隔5分钟进行一次RSI短周期与长周期多空共振的判断，决定做开多头仓还是空头仓；
盘中再按照盈利比例进行头寸平仓或者收盘前清算头寸平仓
==============================================================================
备注：该demo仅支持回测场景使用，如在交易场景使用，需要将主力合约代码，如"IF888.CCFX"
替换为当前交易日正处理上市状态的合约代码
"""
# 导入函数库
import numpy as np


# 初始化此策略
def initialize(context):
    # 设置我们要操作的股票池, 这里我们只操作一支股票
    g.ini_buy_flag = False  # 买底仓开关
    g.amount = 1  # 1份标准交易头寸
    g.rate = 0.5  # 做T涨跌幅，1就是1%
    g.L = 50  # 长周期RSI阈值
    g.S = 80  # 短周期RSI阈值
    g.target = 'IF'  # 设置交易标的
    g.security = g.target + '888.CCFX'  # 设置主力合约
    log.info(g.security)
    if not is_trade():
        set_limit_mode('UNLIMITED')
        set_margin_rate(g.target, 0.15)


# 盘前处理
def before_trading_start(context, data):
    g.count = 0
    g.B_T_flag = False  # 做正T开关（先买后卖）
    g.S_T_flag = False  # 做反T开关（先卖后买）
    g.first_buy_flag = False
    g.second_buy_flag = False
    g.trade_flag = True


# 盘中处理
def handle_data(context, data):
    g.count += 1
    k_num = g.count
    if k_num <= 5:
        return
    # 每个5分钟整点进行做T判断
    if k_num % 1 == 0:
        # 获取5分钟K线数据
        h = get_history(100, '1m', field=['close', 'volume'], security_list=g.security,
                        fq=None, include=True, is_dict=True)
        close_array_m = h[g.security]['close']
        # 获取5分钟K线数据
        h = get_history(100, '5m', field=['close', 'volume'], security_list=g.security,
                        fq=None, include=True, is_dict=True)
        close_array_5m = h[g.security]['close']

        if close_array_m.ndim != 0 and close_array_5m.ndim != 0:
            # 获取5分钟、15分钟RSI
            rsi_m = get_rsi(close_array_m, 11)[-1]
            rsi_5m = get_rsi(close_array_5m, 11)[-1]
            # 做T条件判断
            if rsi_5m > g.L and rsi_m > g.S:
                if get_position(g.security).long_amount == 0 and not g.B_T_flag:
                    order_id = buy_open(g.security, g.amount)
                    if order_id is not None:
                        log.info('日内看多开多头仓')
                        log.info('========================')
                        g.B_T_flag = True
                        g.B_T_cost = data[g.security].price
            if rsi_5m < 100 - g.L and rsi_m < 100 - g.S:
                if get_position(g.security).short_amount == 0 and not g.S_T_flag:
                    order_id = sell_open(g.security, g.amount)
                    if order_id is not None:
                        log.info('日内看空开空头仓')
                        log.info('========================')
                        log.info(get_positions())
                        g.S_T_flag = True
                        g.S_T_cost = data[g.security].price
    if g.B_T_flag:
        if data[g.security].price >= g.B_T_cost * (1 + g.rate / 100):
            order_id = sell_close(g.security, 1)
            if order_id is not None:
                log.info('多头仓做T后多头仓平仓')
                log.info('------------------------')
                g.B_T_flag = False
    if g.S_T_flag:
        if data[g.security].price <= g.S_T_cost * (1 - g.rate / 100):
            order_id = buy_close(g.security, 1)
            if order_id is not None:
                log.info('空头仓做T后空头仓平仓')
                log.info('------------------------')
                g.S_T_flag = False
    # 收盘前多次尝试将持仓恢复到开盘持有量
    if k_num == 238:
        log.info('收盘前尝试将持仓恢复到开盘持有量')
        long_pos = get_long_position_list(context)
        short_pos = get_short_position_list(context)
        if long_pos:
            order_id = sell_close(g.security, 1)
            if order_id is not None:
                log.info('收盘多头仓清算')
        if short_pos:
            order_id = buy_close(g.security, 1)
            if order_id is not None:
                log.info('收盘空头仓清算')


# 获取RSI数据
def get_rsi(array_list, periods=14):
    length = len(array_list)
    rsi_values = [np.nan] * length
    if length <= periods:
        return rsi_values
    up_avg = 0
    down_avg = 0

    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsi_values[periods] = 100 - 100 / (1 + rs)

    for j in range(periods + 1, length):
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        rs = up_avg / down_avg
        rsi_values[j] = 100 - 100 / (1 + rs)
    return rsi_values


# 生成持仓股票列表
def get_long_position_list(context):
    position_list = []
    for code in context.portfolio.positions:
        if context.portfolio.positions[code].long_amount != 0:
            position_list.append(code)
    return position_list


# 生成持仓股票列表
def get_short_position_list(context):
    position_list = []
    for code in context.portfolio.positions:
        if context.portfolio.positions[code].short_amount != 0:
            position_list.append(code)
    return position_list
######################################
"""
策略名称：
期货双均线策略
运行周期:
日线
==============================================================================
备注：该demo仅支持回测场景使用，如在交易场景使用，需要将主力合约代码，如"IF888.CCFX"
替换为当前交易日正处理上市状态的合约代码
"""
import numpy as np


def initialize(context):
    g.target = 'IF'  # 设置交易标的
    # 设置主力合约
    g.security = g.target + '888.CCFX'
    g.amount = 1
    if not is_trade():
        set_limit_mode('UNLIMITED')
        set_margin_rate(g.target, 0.15)


def before_trading_start(context, data):
    h = get_history(20, '1d', field=['close', 'volume'], security_list=g.security,
                    fq='dypre', include=False, is_dict=True)
    g.close_data = h[g.security]['close']


# 当五日均线高于十日均线时开多仓、平空仓，当五日均线低于十日均线时开空仓、平多仓
def handle_data(context, data):
    # 获取历史日K线数据
    current_price = data[g.security].close
    # 合成最新K线序列
    close_data = np.concatenate((g.close_data, np.array(list([current_price]))), axis=0)
    # 获取5日、10日均线
    ma5 = get_ma(close_data, 5)
    ma10 = get_ma(close_data, 10)
    # 五日均线大于十日均线
    if ma5 > ma10:
        if get_position(g.security).long_amount == 0:
            # 开一份多头仓
            order_id = buy_open(g.security, g.amount)
            log.info("开多头仓 %s" % g.security)
        if get_position(g.security).short_amount != 0:
            # 平一份空头仓
            order_id = buy_close(g.security, g.amount)
            log.info("平空头仓 %s" % g.security)

    # 五日均线小于十日均线
    elif ma5 < ma10:
        if get_position(g.security).short_amount == 0:
            # 开一份空头仓
            order_id = sell_open(g.security, g.amount)
            log.info("开空仓 %s" % g.security)
        if get_position(g.security).long_amount != 0:
            # 平一份多头仓
            order_id = sell_close(g.security, g.amount)
            log.info("平多仓 %s" % g.security)


# 获取MA函数
def get_ma(close_array, num):
    ma = close_array[-num:].mean()
    return round(ma, 2)