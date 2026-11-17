#encoding:gbk
'''
2法玛全天候绝对动量无个股风控策略回测
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
'''
import pandas as pd
import numpy as np
import talib
import math
def init(c):
	#账户
	c.account=''
	#账户类型
	c.account_type='STOCK'
	#开始时间
	c.start='20240101 00:00:00'
	#结束时间
	c.end='20500101 00:00:00'
	#测试资金
	c.capital=200000
	#动量天数
	c.n=25
	#买入排行
	c.rank=1
	#最低的动量
	c.min_value=0
	#最大的动量
	c.max_value=30
	#卖出目标仓位
	c.sell_ratio=0
	
	
	#买入目前仓位
	c.buy_ratio=1
	c.stock_list=['518800.SH','513100.SH','159915.SZ']
	c.name_list=['黄金ETF','纳斯达克','创业板']
	c.name_dict=dict(zip(c.stock_list,c.name_list))
	c.set_universe(c.stock_list)  
	#下载数据
	for stock in c.stock_list:
		download_history_data(stock,"1d",c.start,c.end)
def MOM(c,df,etf):
	close_list=df['close'].tolist()[-c.n:]
	last_value =close_list[-1]
	pre_value=close_list[0]
	score=((last_value-pre_value)/pre_value)*100
	return score
def get_rank(c,etf_pool,score_list):
	df = pd.DataFrame(index=etf_pool, data={'score':score_list})
	df = df.sort_values(by='score', ascending=False)
	#total_score = df['score'].sum() 不告诉你这个怎么用
	df = df[(df['score'] > c.min_value) & (df['score'] <= c.max_value)] #安全区间，动量过高过低都不好
	rank_list = list(df.index)
	if len(rank_list) == 0:
		rank_list=[] #如果全部都小于最新动量，那么空仓或者买《国债、银华日历、黄金》避险
	return rank_list
def handlebar(c):
	#索普全天候绝对动量策略回测
	d=c.barpos
	#获取当前K线日期
	#精确到分钟小周期,不然有未来函数
	#date=timetag_to_datetime(c.get_bar_timetag(d),'%Y%m%d%H%M%S')
	#日线
	date=timetag_to_datetime(c.get_bar_timetag(d),'%Y-%m-%d')
	hist=c.get_history_data(c.n,'1d','close')
	score_list=[]
	for stock in c.stock_list:
		df=pd.DataFrame()
		df['close']=hist[stock]
		score=MOM(c,df,stock)
		score_list.append(score)
	data=pd.DataFrame()
	data['证券代码']=c.stock_list
	data['名称']=data['证券代码'].apply(lambda x: c.name_dict.get(x,x))
	data['分数']=score_list
	data['日期']=date
	print(data)
	rank_list=get_rank(c,c.stock_list,score_list)
	position=get_position(c,c.account,c.account_type)
	if position.shape[0]>0:
		position=position[position['持仓量']>=10]
		if position.shape[0]>0:
			hold_list=position['证券代码'].tolist()
		else:
			hold_list=[]
	else:
		hold_list=[]
	#先卖出
	target_list=rank_list[:c.rank]
	for stock in hold_list:
		if stock not in target_list:
			order_target_percent(stock, c.sell_ratio, c, c.account)
			try:
				hold_list.remove(stock)
			except Exception as e:
				print(stock,e,'移除持股有问题')
		else:
			print(date,stock,'在动量排行继续持有')
	#买入
	for stock in target_list:
		if stock not in hold_list:
			order_target_percent(stock, c.buy_ratio, c, c.account)
		else:
			print(date,stock,'在动量排行继续持有')
#获取账户总权益m_dBalance
def get_account(c,accountid,datatype):
	'''
	获取账户数据
	'''
	accounts = get_trade_detail_data(accountid, datatype, 'account')
	result={}
	for dt in accounts:
		result['总资产']=dt.m_dBalance
		result['净资产']=dt.m_dAssureAsset
		result['总市值']=dt.m_dInstrumentValue
		result['总负债']=dt.m_dTotalDebit
		result['可用金额']=dt.m_dAvailable
		result['盈亏']=dt.m_dPositionProfit
	return result
#获取持仓信息{code.market:手数}
def get_position(c,accountid,datatype):
	'''
	获取持股数据
	'''
	positions = get_trade_detail_data(accountid,datatype, 'position')
	data=pd.DataFrame()
	print('持股数量{}'.format(len(positions)))
	if len(positions)>0:
		df=pd.DataFrame()
		try:
			for dt in positions:
				df['股票代码']=[dt.m_strInstrumentID]
				df['市场类型']=[dt.m_strExchangeID]
				df['证券代码']=df['股票代码']+'.'+df['市场类型']
				df['证券名称']=[dt.m_strInstrumentName]
				df['持仓量']=[dt.m_nVolume]
				df['可用数量']=[dt.m_nCanUseVolume]
				df['成本价']=[dt.m_dOpenPrice]
				df['市值']=[dt.m_dInstrumentValue]
				df['持仓成本']=[dt.m_dPositionCost]
				df['盈亏']=[dt.m_dPositionProfit]
				data=pd.concat([data,df],ignore_index=True)
		except Exception as e:
			print('获取持股股票池有问题')
			data=pd.DataFrame()
	else:
		data=pd.DataFrame()
	return data 
def get_order(c,accountid,datatype):
	'''
	获取委托
	'''
	data=pd.DataFrame()
	orders = get_trade_detail_data(accountid,datatype, 'order')
	print('委托数量{}'.format(len(orders)))
	if len(orders)>0:
		df=pd.DataFrame()
		for o in orders:
			df['股票代码']=[o.m_strInstrumentID]
			df['市场类型']=[o.m_strExchangeID]
			df['证券代码']=df['股票代码']+'.'+df['市场类型']
			df['买卖方向']=[o.m_nOffsetFlag]
			df['委托数量']=[o.m_nVolumeTotalOriginal]
			df['成交均价']=[o.m_dTradedPrice]
			df['成交数量']=[o.m_nVolumeTraded]
			df['成交金额']=[o.m_dTradeAmount]
			df['投资备注']=[o.m_strRemark]
			df['委托状态']=[o.m_nOrderStatus]
			df['委托数量']=[o.m_nVolumeTotalOriginal]
			df['委托价格']=[o.m_dLimitPrice]
			df['成交数量']=[o.m_nVolumeTraded]
			df['订单编号']=[o.m_strOrderSysID]
			df['未成交数量']=df['委托数量']-df['成交数量']
			df['未成交金额']=df['未成交数量']*df['委托价格']
			data=pd.concat([data,df],ignore_index=True)
	else:
		data=pd.DataFrame()
	return data
def get_deal(c,accountid,datatype):
	'''
	获取成交
	'''
	data=pd.DataFrame()
	deals = get_trade_detail_data(account, 'stock', 'deal')
	print('成交数量{}'.format(len(deals)))
	if len(deals):
		df=pd.DataFrame()
		for dt in deals:
			df['股票代码']=[dt.m_strInstrumentID]
			df['市场类型']=[dt.m_strExchangeID]
			df['证券代码']=df['股票代码']+'.'+df['市场类型']
			df['证券名称']=[dt.m_strInstrumentName]
			df['买卖方向']=[dt.m_nOffsetFlag]
			df['成交价格']=[dt.m_dPrice]
			df['成交数量']=[dt.m_nVolume]
			df['成交金额']=[dt.m_dTradeAmount]
			data=pd.concat([data,df],ignore_index=True)
	else:
		data=pd.DataFrame()
