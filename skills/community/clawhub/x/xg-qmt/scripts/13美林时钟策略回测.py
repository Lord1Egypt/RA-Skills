#encoding:gbk
'''
13美林时钟策略回测
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
'''

import numpy as np
import pandas as pd
import math

class A():
	pass
a=A()
#初始化函数 
def init(C):
	C.acct = '55003243'
	C.acct_type = 'STOCK'

	C.etf_pool = ['513100.SH','159915.SZ','159937.SZ']
	C.stock = '511130.SH'
	#C.etf_pool = C.get_stock_list_in_sector('上证50')
	#print(C.etf_pool)
	for i in C.etf_pool:
		download_history_data(i,'1d','','')
		download_history_data(C.stock,'1d','','')
	C.m_days = 25 #动量参考天数
	C.Num = 1  #购买股票数量
	#C.run_time('trade','1nDay',"2024-07-25 14:57:00")
	
def handlebar(C):
	#pass
	trade(C) #每天运行确保即时捕捉动量变化
	print('运行中')
    #trade(C) #每天运行确保即时捕捉动量变化

def get_rank(C,etf_pool):
	score_list = []
	px=-1
	start_time = timetag_to_datetime(C.get_bar_timetag(C.barpos-C.m_days),'%Y%m%d')
	end_time = timetag_to_datetime(C.get_bar_timetag(C.barpos),'%Y%m%d')
	for etf in etf_pool: 
		data = C.get_market_data_ex(fields=["close"],stock_code=[etf], period = "1d", start_time = start_time, end_time = end_time,count=C.m_days)
		df = data[etf]
		pre_line2 = np.mean(df.close[-21: -1])
		if df.close[-1]>pre_line2:
			px = 1
		y = df['log'] = np.log(df.close)
		x = df['num'] = np.arange(df.log.size)
		slope, intercept = np.polyfit(x, y, 1)
		annualized_returns = math.pow(math.exp(slope), 250) - 1
		r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
		score = annualized_returns * r_squared * px
		score_list.append(score)
	df = pd.DataFrame(index=etf_pool, data={'score':score_list})
	df = df.sort_values(by='score', ascending=False)
	rank_list = list(df.index)  
	print(df)
	print('最大',df['score'].max())
	if df['score'].max()<0:
		rank_list = ['511130.SH']
		return rank_list
	else:
		return rank_list

		


# 交易
def trade(C):
	get_rank(C,C.etf_pool)
	
	# 获取动量最高的一只ETF
	target_num = C.Num 
	
	target_list = get_rank(C,C.etf_pool)[:target_num]
	#获取持仓信息
	holdings = get_trade_detail_data(C.acct, C.acct_type, 'position')
	#获取股票的代码和持仓数量的字典
	holdings = {i.m_strInstrumentID + '.' + i.m_strExchangeID : i.m_nCanUseVolume for i in holdings}
	# 卖出  
	hold_list = holdings
	for etf in hold_list:
		if etf not in target_list:
			passorder(24, 1101, C.acct, etf, 10, 0, holdings.get(etf,0), '', 1 , '', C)
			print(timetag_to_datetime(C.get_bar_timetag(C.barpos),'%Y%m%d'), '卖出' + str(etf))
		else:
			print( timetag_to_datetime(C.get_bar_timetag(C.barpos),'%Y%m%d'),'继续持有' + str(etf))
	# 买入
	for i in get_trade_detail_data(C.acct,C.acct_type,"account"):
		cash = i.m_dAvailable
	#hold_list = list(context.portfolio.positions)
	if len(hold_list) < target_num:
		value = cash / (target_num - len(hold_list))
		for etf in target_list:
			if holdings.get(etf,0) == 0:
				passorder(23, 1102, C.acct, etf, 0, 0, value, '', 1 , '', C)

