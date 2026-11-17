'''
2上涨买入
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
'''
#encoding:gbk
'''
上涨买入
先模拟盘测试
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
'''
import pandas as pd
import numpy as np
import talib
import time 
from datetime import datetime
import math
pd.set_option('display.float_format', lambda x: '%.2f' % x)

text={
	"自定义交易品种交易":"自定义交易类型比如股票，可转债，etf***********",
	"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
	"策略名称":"上涨买入",
	"账户类型":"STOCK",
	"账户":"77",
	"账户类型":"STOCK",
	"是否隔离策略":"否",
	"买入价格编码":5,
	"卖出价格编码":5,
	
	"买入金额":5000,
	"每天最多买入":2,
	"上涨买入":5,
	"买入黑名单":['600031.SH'],
	"卖出黑名单":['600031.SH'],
	
	"股票池":['002138.SZ','603520.SH','603936.SH','002326.SZ','002580.SZ',
	'600211.SH','002796.SZ','002632.SZ','600869.SH','600207.SH','002887.SZ',
	'603665.SH','603429.SH','603168.SH','002778.SZ','002077.SZ','603520.SH',
	'603569.SH'],
	"股票池名称":['顺络电子','司太立','博敏电子','永太科技','圣阳股份','西藏药业',
	'世嘉科技',	'道明光学','远东股份','安彩高科','绿茵生态','康隆达','集友股份',
	'莎普爱思','中晟高科','大港股份','长久物流','其他'],
	
	"时间设置":"时间设置********",
	"交易时间段":4,
	"交易开始时间":9,
	"交易结束时间":14,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
}
#记录交易数据
class A:
	pass
a=A()
def init(c):
	#账户
	c.account=text['账户']
	#账户类型
	c.account_type=text['账户类型']
	if c.account_type=='stock' or c.account_type=='STOCK':
		c.buy_code=23
		c.sell_code=24
	else:
		#融资融券
		c.buy_code=33
		c.sell_code=34
	c.buy_price_code=text['买入价格编码']
	c.sell_price_code=text['卖出价格编码']
	a.trade_code_list=text['股票池']
	a.trade_code_name=text['股票池名称']
	c.st_name=text['策略名称']
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	#3秒一次
	c.run_time("run_tarder_func","3nSecond","2024-07-25 13:20:00")
def handlebar(c):
	#run_tarder_func(c)
	pass
def get_trader_stock(c):
	'''
	读取交易股票池数据
	'''
	df=pd.DataFrame()
	df['证券代码']=text['股票池']
	df['名称']=text['股票池名称']
	df['证券代码']=df['证券代码'].apply(lambda x: adjust_stock(x))
	return df
def get_price(c,stock='512480.SH'):
	'''
	获取最新价格
	'''
	tick=c.get_full_tick(stock_code=[stock])
	price=tick[stock]['lastPrice']
	return price
def get_zdf(c,stock='512480.SH'):
	'''
	获取tick数据
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	zdf=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
	return zdf
def adjust_stock(stock='600031.SH'):
	'''
	调整代码
	'''
	if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
		stock=stock.upper()
	else:
		if stock[:3] in ['600','601','603','605','688','689',
			] or stock[:2] in ['11','51','58'] or stock[:1] in ['5']:
			stock=stock+'.SH'
		else:
			stock=stock+'.SZ'
	return stock

def check_buy_order_amount(c):
	'''
	检测买入成功委托数量
	'''
	daily_limit_n=text['每天最多买入']
	trader_log=get_order(c,c.account,c.account_type)
	#委托成功代码
	not_list=[49,50,51,52,53,55,56]
	if trader_log.shape[0]>0:
		trader_log['买入委托成功']=trader_log['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
		trader_log=trader_log[trader_log['买入委托成功']=='是']
		trader_log=trader_log[trader_log['买卖方向']==48]
		amount=trader_log.shape[0]
	else:
		amount=0
	av_amount=daily_limit_n-amount
	if av_amount>=1:
		return True
	else:
		return False
def check_stock_is_order(c,stock='000001.SZ'):
	'''
	检测股票是不是有成功的委托
	'''
	trader_log=get_order(c,c.account,c.account_type)
	#委托成功代码
	not_list=[49,50,51,52,53,55,56]
	if trader_log.shape[0]>0:
		trader_log['买入委托成功']=trader_log['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
		trader_log=trader_log[trader_log['买入委托成功']=='是']
		trader_log=trader_log[trader_log['买卖方向']==48]
		stock_list=trader_log['证券代码'].tolist()
	else:
		
		stock_list=[]
	if stock not in stock_list:
		return True
	else:
		return False
def run_tarder_func(c):
	'''
	运行交易函数
	'''
	if check_is_trader_date_1():
		df=get_trader_stock(c)
		buy_zdf=text['上涨买入']
		daily_limit_n=text['每天最多买入']
		value=text['买入金额']
		if df.shape[0]>0:
			for stock ,name in zip(df['证券代码'].tolist(),df['名称'].tolist()):
				zdf=get_zdf(c,stock)
				price=get_price(c,stock)
				if zdf>=buy_zdf:
					#检测是不是达到今天买入数量限制
					if check_buy_order_amount(c):
						#检测这个标的是不是已经委托成功
						if check_stock_is_order(c,stock):
							amount=value/price
							amount=adjust_amount(c,stock,amount)
							maker='{},上涨买入'.format(stock)
							if check_is_buy(c,c.account,c.account_type,stock=stock ,amount=amount,price=price) and amount>=10:
								passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
								print('{} 最新价格 买入{} '.format(stock,amount))
							else:
								print('{}金额交易买入不了*******'.format(stock))
						else:
							print(stock,'已经有委托等待成交')
					else:
						print(stock,'已经达到今天买入{}次数量限制不买入'.format(daily_limit_n))
				else:
					print('不买入{} 目前涨跌幅{} 小于目标涨跌幅{}'.format(stock,zdf,buy_zdf))
		else:
			print('上涨买入没有股票池')
	else:
		print(datetime.now(),'目前上涨买入不是交易时间')

def check_is_buy(c,accountid,datatype,stock='513100.SH',amount=100,price=1.3):
	'''
	检查是否可以买入
	'''
	account=get_account(c,accountid,datatype)
	#可以使用的现金
	av_cash=account['可用金额']
	value=amount*price
	if av_cash>=value:
		return True
	else:
		return False
def adjust_amount(c,stock='',amount=''):
	'''
	调整数量
	'''           
	if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['11','12']:
		amount=math.floor(amount/10)*10
	else:
		amount=math.floor(amount/100)*100
	return amount
def check_is_trader_date_1():
	'''
	检测是不是交易时间
	'''
	trader_time=text['交易时间段']
	start_date=text['交易开始时间']
	end_date=text['交易结束时间']
	start_mi=text['开始交易分钟']
	jhjj=text['是否参加集合竞价']
	if jhjj=='是':
		jhjj_time=15
	else:
		jhjj_time=30
	loc=time.localtime()
	tm_hour=loc.tm_hour
	tm_min=loc.tm_min
	wo=loc.tm_wday
	if wo<=trader_time:
		if tm_hour>=start_date and tm_hour<=end_date:
			if tm_hour==9 and tm_min<jhjj_time:
				return False
			
			elif tm_min>=start_mi:
				return True
			else:
				return False
		else:
			return False    
	else:
		print('周末')
		return False

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
			df=data
			is_del=text['是否隔离策略']
			if is_del=='是':
				df['证券代码']=df['证券代码'].astype(str)
				df['隔离策略']=df['证券代码'].apply(lambda x: '是' if x in a.trade_code_list else '不是')
				df=df[df['隔离策略']=='是']
				data=df
			else:
				data=data
			
		except Exception as e:
			print('获取持股隔离股票池有问题')
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
