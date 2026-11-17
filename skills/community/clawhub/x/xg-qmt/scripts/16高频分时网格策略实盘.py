#encoding:gbk
'''
16高频分时网格策略实盘
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
text={
	"自定义交易品种交易":"自定义交易类型比如股票，可转债，etf***********",
	"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
	"账户类型":"STOCK",
	"账户":"770",
	"账户类型":"STOCK",
	"是否测试说明":"实盘改成否",
	"是否测试":"否",
	"是否立马交易交易说明":"利用run_time运行策略第一次循环不会下单，但是会记录交易数据需要清空",
	"是否立马交易交易":"是",
	"买入价格编码":5,
	"卖出价格编码":5,
	"是否隔离策略":"否",
	"固定交易数量":100,
	"持有数量限制":300,
	"卖出单元格":0.2,
	"买入单元格":-0.2,
	"时间设置":"时间设置********",
	"交易时间段":8,
	"交易开始时间":9,
	"交易结束时间":24,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	"监测股票池设置":"监测股票池设置 自定义/持股",
	"监测股票池":"自定义",
	'自定义股票池':"自定义股票池设置",
	"股票池设置":"持有限制10的股票池设置",
	"自定义股票池":['511130.SH','511090.SH'],
	"自定义股票池名称":['30年国债ETF','30年国债ETF'],
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
	is_open=text['是否立马交易交易']
	if is_open=='是':
		a.del_log=True
	else:
		a.del_log=False
	c.buy_price_code=text['买入价格编码']
	c.sell_price_code=text['卖出价格编码']
	#交易股票池
	a.trade_code_list=text['自定义股票池']
	a.trade_code_name=text['自定义股票池名称']
	a.log=get_order_log(c)
	print('开启策略交易）））））））））））））')
	print('读取系统的委托数据记录，继续上一步策略*******************************')
	print(a.log)
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	c.run_time("run_tarder_func","1nDay","2024-07-25 09:145:00")
	c.run_time("run_tarder_func","3nSecond","2024-07-25 13:20:00")
	#passorder(23, 1101, c.account, '513100.SH', 5, 0, 100, '',1,'',c)
	
	#run_tarder_func(c)
def handlebar(c):
	#run_tarder_func(c)
	pass
def get_order_log(c):
	'''
	第一次运行获取全部委托备注，避免程序断开没有记录数据
	'''
	order=get_order(c,c.account,c.account_type)
	if order.shape[0]>0:
		result_list=[]
		order['投资备注']=order['投资备注'].apply(lambda x: str(x).split(','))
		for j  in order['投资备注'].tolist():
			if len(j)==6:
				result_list.append(j)
		if len(result_list)>0:
			log=pd.DataFrame(result_list)
			log.columns=['证券代码','触发时间','交易类型','交易数量','持有限制','触发价格']
		else:
			log=pd.DataFrame()
	else:
		log=pd.DataFrame()
	return log
def conditional_single_time_sharing_grid(c,name='name',stock='511090.SH',x1=0.2,x2=-0.2):
	'''
	条件单分时网格
	stock_type=自定义/持股
	'time'                  #时间戳
	'lastPrice'             #最新价
	'open'                  #开盘价
	'high'                  #最高价
	'low'                   #最低价
	'lastClose'             #前收盘价
	'amount'                #成交总额
	'volume'                #成交总量
	'pvolume'               #原始成交总量
	'stockStatus'           #证券状态
	'openInt'               #持仓量
	'lastSettlementPrice'   #前结算
	'askPrice'              #委卖价
	'bidPrice'              #委买价
	'askVol'                #委卖量
	'bidVol'                #委买量
	'transactionNum'		#成交笔数
	'''
	name='小果高频分时网格策略实盘'
	now_date=datetime.now()
	#'证券代码','触发时间','触发的价格','资金类型','交易类型','交易数量','投资备注'
	trader_date=str(datetime.now())[:10]
	#采用委托查询的方式,避免程序停止信号丢失
	#log=a.log[a.log['交易时间']==trader_date]
	log=a.log
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	base_price=tick['lastClose']
	price=tick['lastPrice']
	if log.shape[0]>0:
		log['触发价格']=pd.to_numeric(log['触发价格'])
		log['触发时间']=pd.to_datetime(log['触发时间'])
		log=log.sort_values(by='触发时间',ascending=True)
		log=log[log['证券代码']==stock]
		if log.shape[0]>0:
			
			pre_price=log['触发价格'].tolist()[-1]
			zdf=((price-pre_price)/pre_price)*100
		else:
			zdf=((price-base_price)/base_price)*100
	else:
		zdf=((price-base_price)/base_price)*100
	if zdf>=x1:
		print('{} 模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} '.format(now_date,name,stock,zdf,x1))
		return 'sell'
	elif zdf<=x2:
		print('{} 模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} '.format(now_date,name,stock,zdf,x1))
		return 'buy'
	else:
		print('{} 模块{} 不符合交易{}  目前涨跌幅{} 目前标涨跌幅{} '.format(now_date,name,stock,zdf,x1))
		return ''
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
def check_hold_limit(c,accountid,datatype,stock='513100.SH',limit=1000):
	'''
	检查是否到持股限制
	'''
	position=get_position(c,accountid,datatype)
	if position.shape[0]>0:
		position=position[position['证券代码']==stock]
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			hold_amount=position['持仓量'].tolist()[-1]
		else:
			hold_amount=0
	else:
		hold_amount=0
	av_amount=limit-hold_amount
	if av_amount>=10:
		return True
	else:
		return False
def run_tarder_func(c):
	'''
	运行交易函数
	'''
	fix_amount=text['固定交易数量']
	hold_amount_limit=text['持有数量限制']
	stock_list_type=text['监测股票池']
	x1=text['卖出单元格']
	x2=text['买入单元格']
	test=text['是否测试']
	name='小果高频分时网格策略实盘'
	if check_is_trader_date_1():
		if test=='是':
			print('开启测试模式实盘记得关闭*（（（（（（（（（（（（（（（（（')
			a.log=pd.DataFrame()
		else:
			pass
		print(a.log)
		now_date=datetime.now()
		if stock_list_type=='自定义':
			df=pd.DataFrame()
			df['证券代码']=text['自定义股票池']
			df['证券名称']=text['自定义股票池名称']
		else:
			df=get_position(c,c.account,c.account_type)
		if df.shape[0]>0:
			for stock in df['证券代码'].tolist():
				try:
				#if True:
					price=get_price(c,stock)
					trader_type=conditional_single_time_sharing_grid(c,stock=stock,name='条件单分时网格',x1=x1,x2=x2)
					if trader_type=='sell':
						if check_is_sell(c,c.account,c.account_type,stock=stock,amount=fix_amount):
							trader_type='sell'
							amount=fix_amount
							price=price
						else:
							print("{} {} 不能卖出".format(datetime.now(),stock))
							trader_type=''
							amount=fix_amount
							price=price
					elif trader_type=='buy':
						#检查是否到达持股限制
						if check_hold_limit(c,c.account,c.account_type,
								stock=stock,limit=hold_amount_limit)==True:
							#检查是否可以买入
							if check_is_buy(c,c.account,c.account_type,stock=stock ,amount=fix_amount,price=price):
								
								trader_type='buy'
								amount=fix_amount
								price=price
							else:
								trader_type=''
								amount=fix_amount
								price=price
								print("{} {} 买入不了".format(datetime.now(),stock))
						else:
							trader_type=''
							amount=fix_amount
							price=price
							print("{} {} 不买入超过持有限制".format(datetime.now(),stock))
					else:
						trader_type=''
						amount=fix_amount
						price=price

					if trader_type=='buy' and amount>=10:
						#'证券代码','触发时间','交易类型','交易数量','持有限制,'触发价格''
						flag="{},{},{},{},{},{}".format(stock,now_date,'买',amount,hold_amount_limit,price)
						passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, flag,1,flag,c)
						print('{} {} 最新价格{} 买入{} 数量***************'.format(now_date,stock,price,amount))
					elif trader_type=='sell' and amount>=10:
						flag="{},{},{},{},{},{}".format(stock,now_date,'卖',amount,hold_amount_limit,price)
						passorder(c.sell_code, 1101,c.account, str(stock), c.sell_price_code, 0, amount, flag,1,flag,c)
						print('{} {} 最新价格{} 卖出{} 数量*******************'.format(now_date,stock,price,amount))
					else:
						print('{} {} 没有触发网格继续观察'.format(now_date,stock))
					if (trader_type=='buy' or trader_type=='sell') and  amount>=10:
						#'证券代码','触发时间','交易类型','交易数量','持有限制'
						df1=pd.DataFrame()
						df1['证券代码']=[stock]
						df1['触发时间']=[now_date]
						df1['交易类型']=[trader_type]
						df1['交易数量']=[amount]
						df1['持有限制']=[hold_amount_limit]
						df1['触发价格']=[price]
						a.log=pd.concat([a.log,df1],ignore_index=True)
					else:
						pass
					#print(a.log)
				
				except Exception as e:
					print(e,stock,'{}运行有问题可能不是交易日期'.format(datetime.now()))
				
			if a.del_log==True:
				print('第一次循环清空交易记录********************************')
				a.log=pd.DataFrame()
				a.del_log=False
			else:
				a.del_log=False
				
		else:
			print('{} 分时网格股票没有数据'.format(now_date))
	else:
		print('{} 分时网格股票不是交易时间'.format(datetime.now()))

	
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
def get_price(c,stock):
	'''
	获取最新价格
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	price=tick['lastPrice']
	return price
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
			return 'sell',price,av_trader_amount
		else:
			print('{} 目标数量{} 持有数量{} 可用数量{}小于 卖出数量{} 卖出全部'.format(stock,target_amount,hold_amount,av_amount,av_trader_amount))
			return 'sell',price,av_amount
	else:
		print('{} 目标数量{} 持有数量{}一样不交易'.format(stock,target_amount,hold_amount))
		return '','',''
