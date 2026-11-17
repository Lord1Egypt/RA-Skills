#encoding:gbk
'''
17止盈止损策略
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
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
'''
import pandas as pd
import numpy as np
import talib
import time 
from datetime import datetime
import math
text={
	"自定义交易品种交易":"自定义交易类型比如股票，可转债，etf***********",
	"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
	'策略名称':'止盈止损',
	"账户":"",
	"账户类型":"STOCK",
	
	"买入价格编码":5,
	"卖出价格编码":5,
	"是否隔离策略":"是",
	"买入黑名单":['600031.SH'],
	"卖出黑名单":['600031.SH'],
	"账户个股止盈止损设置":"账户个股止盈止损设置安成本价计算************",
	"账户个股止盈":25,
	"账户个股止损":-8,
	"当日止盈止损设置":"当日止盈止损设置安买入价格计算当日止盈,安自己需要该",
	"当日止盈":15,
	"当日止损":-5,
	"时间设置":"时间设置********",
	"交易时间段":4,
	"交易开始时间":9,
	"交易结束时间":24,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	
}
class A():
	pass
a=A()
#id记录模块，补单
a.log_id=[]
def init(c):
	#账户
	c.account=text['账户']
	#账户类型
	c.account_type=text['账户类型']
	#交易股票池
	c.st_name=text['策略名称']
	
	if c.account_type=='stock' or c.account_type=='STOCK':
		c.buy_code=23
		c.sell_code=24
	else:
		#融资融券
		c.buy_code=33
		c.sell_code=34
	c.buy_price_code=text['买入价格编码']
	c.sell_price_code=text['卖出价格编码']
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	
	#账户个股止盈止损，安成本价计算
	c.run_time("get_account_stock_stop_trader","3nSecond","2024-07-25 13:20:00")
	#当日止盈止损,结合涨跌幅，成本价计算
	c.run_time("get_daily_stock_stop_trader","4nSecond","2024-07-25 13:20:00")
	
	
def handlebar(c):
	
	pass

def trader_info(c):
	if check_is_trader_date_1():
		print('{} 等待程序调仓'.format(datetime.now()))
	else:
		print('{} 不是交易时间等待程序调仓'.format(datetime.now()))
def get_price(c,stock):
	'''
	获取最新价格
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	price=tick['lastPrice']
	return price
def get_zdf(c,stock):
	'''
	获取涨跌幅数据
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	price=tick['lastPrice']
	lastClose=tick['lastClose']
	zdf=((price-lastClose)/lastClose)*100
	return zdf
def get_account_stock_stop_trader(c):
	'''
	账户个股止盈止损，安成本价计算
	'''
	if check_is_trader_date_1():
		x1=text['账户个股止盈']
		x2=text['账户个股止损']
		position=get_position(c,c.account,c.account_type)
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				for stock,cost_price,av_amount,hold_amount in zip(position['证券代码'],position['成本价'],position['可用数量'],position['持仓量']):
					price=get_price(c,stock)
					zdf=((price-cost_price)/cost_price)*100
					if zdf>=x1:
						print('{} 股票{} 账户止盈 最新价{} 成本价{} 目前涨跌幅{} 大于目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
						maker=c.st_name+','+'sell'+','+stock+','+'账户止盈'
						if maker not in a.log_id:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								a.log_id.append(maker)
							else:
								print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
						else:
							print(maker,'在委托记录等待订单检查')
					elif zdf<=x2:
						print('{} 股票{} 账户止损 最新价{} 成本价{} 目前涨跌幅{} 小于目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
						maker=c.st_name+','+'sell'+','+stock+','+'账户止损'
						if maker not in a.log_id:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								a.log_id.append(maker)
							else:
								print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
						else:
							print(maker,'在委托记录等待订单检查')
					else:
						print('{} 股票{} 账户止盈止损继续观察 最新价{} 成本价{} 目前涨跌幅{} 目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
			else:
				print('账户止盈止损没有持股数据1')
		else:
			print('账户止盈止损没有持股数据2')
	else:
		print(datetime.now(),'账户止盈止损不是交易时间')
def get_daily_stock_stop_trader(c):
	'''
	当日止盈止损
	'''
	if check_is_trader_date_1():
		x1=text['当日止盈']
		x2=text['当日止损']
		position=get_position(c,c.account,c.account_type)
		#检查是不是今天建立的全部单子
		trader_log=get_order(c,c.account,c.account_type)
		if trader_log.shape[0]>0:
			try:
				trader_log['交易类型']=trader_log['投资备注'].apply(lambda x:x.split(',')[1] )
				trader_log=trader_log[trader_log['交易类型']=='buy']
			except:
				trader_log=trader_log[trader_log['买卖方向']==48]
			if trader_log.shape[0]>0:
				#成交数量
				trader_amount_dict=dict(zip(trader_log['证券代码'],trader_log['成交数量']))
			else:
				trader_amount_dict={}
		else:
			trader_amount_dict={}
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				for stock,cost_price,hold_amount,av_amount in zip(position['证券代码'],position['成本价'],position['持仓量'],position['可用数量']):
					price=get_price(c,stock)
					#检查是不是今天建立的仓位，今天建立的安成本价计算
					trader_amount=trader_amount_dict.get(stock,0)
					price=get_price(c,stock)
					if hold_amount==trader_amount:
						print(stock ,'当日止盈止损检查是不是今天建立的仓位，今天建立的安成本价计算')
						
						zdf=((price-cost_price)/cost_price)*100
					else:
						zdf=get_zdf(c,stock)
					if zdf>=x1:
						print('{} 股票{} 当日止盈 最新价{} 成本价{} 目前涨跌幅{} 大于目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
						maker=c.st_name+','+'sell'+','+stock+','+'当日止盈'
						if maker not in a.log_id:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								a.log_id.append(maker)
							else:
								print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
						else:
							print(maker,'在委托记录等待订单检查')
					elif zdf<=x2:
						print('{} 股票{} 当日止损 最新价{} 成本价{} 目前涨跌幅{} 小于目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
						maker=c.st_name+','+'sell'+','+stock+','+'当日止损'
						if maker not in a.log_id:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								a.log_id.append(maker)
							else:
								print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
						else:
							print(maker,'在委托记录等待订单检查')
					else:
						print('{} 股票{} 当日止盈止损继续观察 最新价{} 成本价{} 目前涨跌幅{} 目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
			else:
				print('当日止盈止损没有持股数据2')
		else:
			print('当日止盈止损没有持股数据2')
	else:
		print(datetime.now(),'当日止盈止损不是交易时间')
def check_is_sell(c,accountid,datatype,stock='513100.SH',amount=100):
	'''
	检查是否可以卖出
	'''
	position=get_position(c,accountid,datatype)
	if position.shape[0]>0:
		position=position[position['证券代码']==stock]
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				hold_amount=position['持仓量'].tolist()[-1]
				av_amount=position['可用数量'].tolist()[-1]
				if av_amount>=amount and amount>=10:
					return True
				elif av_amount< amount and av_amount>=10:
					return True
			else:
				return False
		else:
			return False
	else:
		return False
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
def adjust_amount(stock='',amount=''):
	'''
	调整数量
	'''           
	if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['11','12']:
		amount=math.floor(amount/10)*10
	else:
		amount=math.floor(amount/100)*100
	return amount

def check_is_down_limit(c,stock):
	'''
	检查是否是跌停
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	askPrice=sum(tick['bidPrice'])
	if askPrice==0:
		return True
	else:
		return False
def check_is_jhjj():
	'''
	检查是否集合竞价
	集合竞价不做撤单
	9点15到9点30不撤单
	14点57到59不撤单
	'''
	loc=time.localtime()
	tm_hour=loc.tm_hour
	tm_min=loc.tm_min
	wo=loc.tm_wday
	#早上集合竞价开始时间
	zs_start_hour=9
	zs_start_mini=15
	#早上集合竞价结束时间
	zs_end_hour=9
	zs_end_mini=30
	#下午时间
	xw_start_hour=14
	xw_start_mini=57
	#下午集合竞价结束时间
	xw_end_hour=14
	xw_end_mini=59
	if tm_hour==zs_start_hour and tm_hour==zs_end_hour and tm_min>=zs_start_mini and tm_min<zs_end_mini:
		print("早上集合竞价时间")
		return True
	elif tm_hour==xw_start_hour and tm_hour==xw_end_hour and tm_min>=xw_start_mini and tm_min<=xw_end_mini:
		print("下午集合竞价时间")
		return True
	else:
		print('非集合竞价时间')
		return False
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
			df['成交数量']=[o.m_nVolumeTraded]
			df['订单编号']=[o.m_strOrderSysID]
			df['未成交数量']=df['委托数量']-df['成交数量']
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
def order_target_amount(c,accountid,datatype,stock,price,target_amount,com_ratio=0.0001):
	'''
	目标交易数量
	'''
	account=get_account(c,accountid,datatype)
	#可以使用的现金
	av_cash=account['可用金额']
	position=get_position(c,accountid,datatype)
	if position.shape[0]>0:
		position[position['持仓量']>=10]
		if position.shape[0]>0:
			hold_amount=position['持仓量'].tolist()[-1]
			av_amount=position['可用数量'].tolist()[-1]
		else:
			hold_amount=0
			av_amount=0
	else:
		hold_amount=0
		av_amount=0
	#可以交易的数量
	av_trader_amount=target_amount-hold_amount
	#存在买入空间
	if av_trader_amount>=10:
		#买入的价值
		value=av_trader_amount*price
		#手续费
		com=value*com_ratio
		if av_cash>=value+com:
			print('{} 目标数量{} 持有数量{} 可用数量{} 买入数量{} 可用资金{} 大于买入资金{} 买入'.format(stock,target_amount,hold_amount,av_amount,av_trader_amount,av_cash,value))
			return 'buy',price,av_trader_amount
		else:
			print('{} 目标数量{} 持有数量{} 可用数量{} 买入数量{} 可用资金{} 小于买入资金{} 不买入'.format(stock,target_amount,hold_amount,av_amount,av_trader_amount,av_cash,value))
			return '',price,av_trader_amount
	elif av_trader_amount<=-10:
		av_trader_amount=abs(av_trader_amount)
		if av_amount>=av_trader_amount:
			print('{} 目标数量{} 持有数量{} 可用数量{}大于 卖出数量{} 卖出'.format(stock,target_amount,hold_amount,av_amount,av_trader_amount))
			return 'sell',price,-av_trader_amount
		else:
			print('{} 目标数量{} 持有数量{} 可用数量{}小于 卖出数量{} 卖出全部'.format(stock,target_amount,hold_amount,av_amount,av_trader_amount))
			return 'sell',price,-av_amount
	else:
		print('{} 目标数量{} 持有数量{}一样不交易'.format(stock,target_amount,hold_amount))
		return '','',''
