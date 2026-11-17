#encoding:gbk
'''
34高频日内算法交易
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
pd.set_option('display.float_format', lambda x: '%.2f' % x)

text={
	"自定义交易品种交易":"自定义交易类型比如股票，可转债，etf***********",
	"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
	"策略名称":"高频日内算法交易框架5",
	"账户类型":"STOCK",
	"账户":"7705",
	"账户类型":"STOCK",
	"是否时间测试":"否",
	"测试时间":"20250912",
	"买入价格编码":4,
	"卖出价格编码":6,
	"是否隔离策略":"否",
	"交易记录":'C:/Users/lxg123456/Desktop/西蒙斯高频日内算法交易5.xlsx',
	"监测股票池设置":"监测股票池设置 自定义/持股,交易股票池类型'stock','bond','fund'",
	"监测股票池":"自定义",
	"交易股票类型":['stock','bond','fund'],
	'自定义股票池':"自定义股票池设置",
	
	"自定义股票池":[
				"512480.SH",'159509.SZ','159915.SZ',"159937.SZ",
				"510800.SH","512800.SH","513100.SH","510300.SH",
				"159937.SZ",'159857.SZ','159869.SZ',"159655.SZ"],
	"自定义股票池名称":[
				'半导体ETF','纳斯达克ETF','创业板ETF',"黄金ETF",
				"红利ETF",'银行ETF','可转债ETF',"沪深300ETF",
				"A500ETF","光伏ETF",'游戏ETF',"标普ETF"],
	
	"算法模型":{
		"固定高频分时网格":{
			"函数名称":"conditional_single_time_sharing_grid(name='固定高频分时网格',x1=0.8,x2=-1)",
			"是否开启":"是",
			"资金模型":"金额",
			"卖出值":200,
			"买入值":200,
			"持有值":600,
			"保留底仓":0,
			"是否生成买入虚拟单子":"是",
			"是否生成卖出虚拟单子":"否"
			},
		"对称高频分时网格":{
			"函数名称":"symmetric_grid_trading(name='对称高频分时网格',x1=0.8,x2=-1)",
			"是否开启":"否",
			"资金模型":"金额",
			"卖出值":200,
			"买入值":200,
			"持有值":600,
			"保留底仓":0,
			"是否生成买入虚拟单子":"是",
			"是否生成卖出虚拟单子":"否"
			},
		"冲高回落卖出":{
			"函数名称":"sell_on_the_rally(name='冲高回落卖出',x1=3,x2=1)",
				"是否开启":"否",
				"资金模型":"金额",
				"卖出值":200,
				"买入值":200,
				"持有值":600,
				"保留底仓":0,
				"是否生成买入虚拟单子":"是",
				"是否生成卖出虚拟单子":"否",
				}
	},
	
	"时间设置":"时间设置********",
	"交易时间段":8,
	"交易开始时间":9,
	"交易结束时间":24,
	"是否参加集合竞价":"是",
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
	c.path=text['交易记录']
	c.stock_type=text['交易股票类型']
	#交易股票池
	a.trade_code_list=text['自定义股票池']
	a.trade_code_name=text['自定义股票池名称']
	c.stock_name_dict=dict(zip(a.trade_code_list,a.trade_code_name))
	
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	#3秒一次
	c.run_time("run_tarder_func","3nSecond","2024-07-25 13:20:00")
	#建立记录文件
	check_trader_log_file(c)
	
	
	
def handlebar(c):
	#run_tarder_func(c)
	pass
def check_trader_log_file(c):
	'''
	检测交易记录文件是不是存在
	'''
	path=c.path
	try:
		df=pd.read_excel(r'{}'.format(path))
		print('交易记录文件存在')
	except Exception as e:
		print('交易文件不存在建立',e)
		df=pd.DataFrame()
		df.to_excel(r'{}'.format(path))
def select_data_type(stock='600031.SH'):
	'''
	选择数据类型
	'''
	stock=str(stock)
	if stock[:2] in ['11','12'] or stock[:3] in ['123','110','113','123','127','128','118','132','120']:
		return 'bond'
	elif stock[:2] in ['51','15','50','16','18','52']:
		return 'fund'
	else:
		return 'stock'
def get_now_tick_data(c,stock='512480.SH'):
	'''
	获取tick数据当天tick数据
	'''
	test=text['是否时间测试']
	test_date=text['测试时间']
	if test=='是':
		print('开启测试数据*************实盘记得关闭{}'.format(test_date))
		start_time=test_date
		end_time=start_time
	else:
		start_time=''.join(str(datetime.now())[:10].split('-'))
		end_time=start_time
	hist=c.get_market_data_ex(
		fields=[], 
		stock_code=[stock], 
		period='tick', 
		start_time=start_time, 
		end_time=end_time, 
		count=-1, 
		fill_data=True, 
		subscribe=True)
	hist=hist[stock]
	hist['date']=hist.index.tolist()
	hist['date']=hist['date'].astype(str)
	hist['date']=hist['date'].apply(lambda x: int(str(x).split('.')[0][-6:]))
	#剔除集合竞价
	hist['date_1']=hist['date'].astype(int).tolist()
	hist=hist[hist['date_1']>=92700]
	return hist
	#return hist
def get_stock_daily_data(c,stock='513100.SH'):
	'''
	获取股票日线数据
	'''
	test=text['是否时间测试']
	test_date=text['测试时间']
	if test=='是':
		print('开启测试数据*************实盘记得关闭{}'.format(test_date))
		start_time=test_date
		end_time=start_time
	else:
		start_time=''.join(str(datetime.now())[:10].split('-'))
		end_time=start_time
	hist=c.get_market_data_ex(
		fields=[], 
		stock_code=[stock], 
		period='1d', 
		start_time=start_time, 
		end_time=end_time, 
		count=-1, 
		fill_data=True, 
		subscribe=True)
	hist=hist[stock]
	return hist
def get_price(c,stock='512480.SH'):
	'''
	获取最新价格
	'''
	tick=c.get_full_tick(stock_code=[stock])
	price=tick[stock]['lastPrice']
	return price
def get_tick_data(c,stock='512480.SH'):
	'''
	获取tick数据
	'''
	tick=c.get_full_tick(stock_code=[stock])
	price=tick[stock]
	return price
	
def run_tarder_func(c):
	'''
	运行交易函数
	'''
	if check_is_trader_date_1():
		user_def_models=text['算法模型']
		name_list=list(user_def_models.keys())
		trader_stock=text['监测股票池']
		if trader_stock=='自定义':
			df=pd.DataFrame()
			df['证券代码']=text['自定义股票池']
			df['名称']=text['自定义股票池名称']
		else:
			df=get_position(c,c.account,c.account_type)
		if df.shape[0]>0:
			for stock in df['证券代码'].tolist():
				log=pd.read_excel(r'{}'.format(c.path))
				if log.shape[0]>0:
					log=log[['证券代码','模块名称','交易日','触发时间','交易类型','交易数量','触发价格','投资备注','交易状态']]
					trader_date=str(datetime.now())[:10]
					log=log.sort_values(by='触发时间',ascending=True)
					log=log[log['交易日']==trader_date]
					
				else:
					log=pd.DataFrame()
				for name in name_list:
					try:
					#if True:
						params_set=user_def_models[name]
						func=params_set['函数名称']
						is_open=params_set['是否开启']
						trader_type=params_set['资金模型']
						buy_value=params_set['买入值']
						sell_value=params_set['卖出值']
						hold_value=params_set['持有值']
						bl_value=params_set['保留底仓']
						buy_xn=params_set['是否生成买入虚拟单子']
						sell_xn=params_set['是否生成卖出虚拟单子']
						if is_open=='是':
							price=get_price(c,stock)
							if trader_type=='金额':
								buy_amount=buy_value/price
								buy_amount=adjust_amount(c,stock,buy_amount)
								sell_amount=sell_value/price
								sell_amount=adjust_amount(c,stock,sell_amount)
								hold_amount=hold_value/price
								hold_amount=adjust_amount(c,stock,hold_amount)
								bl_amount=bl_value/price
								bl_amount=adjust_amount(c,stock,bl_amount)
							else:
								buy_amount=buy_value
								sell_amount=sell_value
								hold_amount=hold_value
								bl_amount=bl_value
							hist=get_now_tick_data(c,stock=stock)
							tick=get_tick_data(c,stock)
							models=user_def_trader_func(c,stock=stock,tick=tick,hist=hist,other_data='')
							func='models.{}'.format(func)
							stats=func)
							if stats=='buy':
								not_trader_amount,not_trader_value=check_not_trader_data(c,stock=stock)
								limit=hold_amount-not_trader_amount
								if check_hold_limit_amount(c,c.account,c.account_type,stock=stock,limit=limit):
									maker='{},{},{},{},{}'.format(name,stats,stock,buy_amount,price)
									if check_is_buy(c,c.account,c.account_type,stock=stock,amount=buy_amount,price=price):
										passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, buy_amount, maker,1,maker,c)
										print("{} 买入{} 数量{} 价格{}".format(name,stock,buy_amount,price))
										flage='买入成功'
									else:
										if buy_xn=='是':
											flage='虚拟买入,账户资金不足'
											maker=''
											stats='buy'
										else:
											print('{} {} 资金买入不了'.format(name,stock))
											stats=''
								else:
									if buy_xn=='是':
										flage='虚拟买入,达到持股限制'
										maker=''
										stats='buy'
									else:
										print("{} {}达到持有限制不买入".format(name,stock))
										stats=''
							elif stats=='sell':
								sell_amount=sell_amount-bl_amount
								if sell_amount>=10:
									maker='{},{},{},{},{}'.format(name,stats,stock,sell_amount,price)
									if check_is_sell(c,c.account,c.account_type,stock=stock,amount=sell_amount):
										passorder(c.sell_code, 1101, c.account, str(stock), c.sell_price_code, 0, sell_amount, maker,1,maker,c)
										print("{} 卖出{} 数量{} 价格{}".format(name,stock,sell_amount,price))
										flage='卖出成功'
									else:
										if sell_xn=='是':
											flage='虚拟卖出,达到持股限制'
											stats='sell'
											maker=''
										else:
											print('{} {} 不能卖出'.format(name,stock))
											stats=''
								else:
									if sell_xn=='是':
										flage='虚拟卖出,到达保留仓位'
										maker=''
										stats='sell'
									print('{} {} 不能卖出低于保留仓位'.format(name,stock))
									stats=''
							else:
								print('{} {} 不符合交易继续观察'.format(name,stock))
								stats=''
							#
							#['证券代码','模块名称','交易日','触发时间','交易类型',
							#'交易数量','触发价格','投资备注','交易状态']]
							if stats=='buy' or stats=='sell':
								trader_date=str(datetime.now())[:10]
								trader_log=pd.DataFrame()
								trader_log['证券代码']=[stock]
								trader_log['模块名称']=[name]
								trader_log['交易日']=[trader_date]
								trader_log['触发时间']=[datetime.now()]
								trader_log['交易类型']=[stats]
								if stats=='buy':
									amount=buy_amount
								else:
									amount=sell_amount
								trader_log['交易数量']=[amount]
								trader_log['触发价格']=[price]
								trader_log['投资备注']=[maker]
								trader_log['交易状态']=[flage]
								log=pd.concat([log,trader_log],ignore_index=True)
								log=log.sort_values(by='触发时间',ascending=True)
								log.to_excel(r'{}'.format(c.path))
							else:
								pass
						else:
							#print(name,'不开启')
							pass
					except Exception as e:
						print(name,stock,'计算有问题',e)
		else:
			print('高频模块没有股票池')
	else:
		print(datetime.now(),'高频交易模型不是交易时间')
	
def test_analysis_func(c,stock='512480.SH'):
	'''
	测试函数
	'''
	hist=get_now_tick_data(c,stock=stock)
	tick=get_price(c,stock=stock)
	models=user_def_trader_func(c,stock=stock,tick=tick,hist=hist)
	models.conditional_single_time_sharing_grid()

class user_def_trader_func:
	def __init__(self,c,stock='512480.SH',tick='',hist='',other_data=''):
		'''
		自定义交易函数
		'''
		self.tick=tick
		self.hist=hist
		self.other_data=other_data
		self.log=pd.read_excel(r'{}'.format(c.path))
		self.trader_date=str(datetime.now())[:10]
		self.now_date=datetime.now()
		self.stock=stock
		if self.log.shape[0]>0:
			self.log=self.log[['证券代码','模块名称','交易日','触发时间','交易类型','交易数量','触发价格','投资备注','交易状态']]
			self.log=self.log.sort_values(by='触发时间',ascending=True)
			self.log=self.log[self.log['交易日']==self.trader_date]
		else:
			self.log=pd.DataFrame()
		
		self.c=c
	def conditional_single_time_sharing_grid(self,
			name='固定高频分时网格',
			x1=0.8,
			x2=-1):
		tick=self.hist
		stock=self.stock
		base_price=tick['lastClose'].tolist()[-1]
		price=tick['lastPrice'].tolist()[-1]
		close_list=tick['lastPrice'].tolist()
		if self.log.shape[0]>0:
			self.log['证券代码']=self.log['证券代码'].astype(str)
			log=self.log[self.log['模块名称']==name]
			log=log[log['证券代码']==stock]
			if log.shape[0]>0:
				pre_price=log['触发价格'].tolist()[-1]
				zdf=((price-pre_price)/pre_price)*100
			else:
				order_stats,order_price=check_buy_order(self.c,stock=stock)
				if order_stats==True:
					base_price=order_price
				else:
					base_price=base_price
				zdf=((price-base_price)/base_price)*100
		else:
			order_stats,order_price=check_buy_order(self.c,stock=stock)
			if order_stats==True:
				base_price=order_price
			else:
				base_price=base_price
			zdf=((price-base_price)/base_price)*100
		if zdf>=x1:
			print('{} 模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
			return 'sell'
		elif zdf<=x2:
			print('{} 模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x2))
			return 'buy'
		else:
			print('{} 模块{} 不符合交易{}  目前涨跌幅{} 在{}到{}期间 '.format(self.now_date,name,stock,zdf,x2,x1))
			return ''
	def symmetric_grid_trading(self,
			name='对称高频分时网格',
			x1=0.8,
			x2=-1):
		'''
		对称高频分时网格
		'''
		tick=self.hist
		stock=self.stock
		base_price=tick['lastClose'].tolist()[-1]
		price=tick['lastPrice'].tolist()[-1]
		close_list=tick['lastPrice'].tolist()
		if self.log.shape[0]>0:
			self.log['证券代码']=self.log['证券代码'].astype(str)
			log=self.log[self.log['模块名称']==name]
			log=log[log['证券代码']==stock]
			
			if log.shape[0]>0:
				pre_price=log['触发价格'].tolist()[-1]
				zdf=((price-pre_price)/pre_price)*100
				shift_trader_type=log['交易类型'].tolist()[-1]
				
			else:
				order_stats,order_price=check_buy_order(self.c,stock=stock)
				if order_stats==True:
					base_price=order_price
				else:
					base_price=base_price
				zdf=((price-base_price)/base_price)*100
				shift_trader_type=''
				
				
		else:
			order_stats,order_price=check_buy_order(self.c,stock=stock)
			if order_stats==True:
				base_price=order_price
			else:
				base_price=base_price
			zdf=((price-base_price)/base_price)*100
			shift_trader_type=''
			
			
		if zdf>=x1 and shift_trader_type=='buy':
			print('{} 上一笔买入模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
			return 'sell'
		elif zdf<=x2 and shift_trader_type=='sell':
			print('{}上一笔卖出 模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x2))
			return 'buy'
		if zdf>=x1 :
			print('{}上一笔没有买入委托 模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x1))
			return 'sell'
		elif zdf<=x2 :
			print('{} 上一笔没有卖出委托模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} '.format(self.now_date,name,stock,zdf,x2))
			return 'buy'
		
		else:
			print('{} 模块{} 不符合交易{}  目前涨跌幅{} 在{}到{}期间 '.format(self.now_date,name,stock,zdf,x2,x1))
			return ''
		
		

	def sell_on_the_rally(self,
		name='冲高回落卖出',
		x1=3,
		x2=-1):
		'''
		冲高回落卖出
		x1 冲高启动计算最低涨跌幅
		x2 回落涨跌幅
		'''
		stock=self.stock
		tick=self.hist
		base_price=tick['lastClose'].tolist()[-1]
		stock=self.stock
		if self.log.shape[0]>0:
			self.log['证券代码']=self.log['证券代码'].astype(str)
			log=self.log[self.log['模块名称']==name]
			log=log[log['证券代码']==stock]
			if log.shape[0]>0:
				pre_price=log['触发价格'].tolist()[-1]
				#触发时间
				shift_date=log['触发时间'].tolist()[-1]
				shift_date=str(shift_date).split('.')[0].replace('-','').replace(' ','').replace(':','')
				shift_date=int(shift_date)
				tick=tick[tick['date_1']>=shift_date]
				close_list=tick['lastPrice'].tolist()
				price=close_list[-1]
				#最大值
				max_value=max(close_list)
			else:
				close_list=tick['lastPrice'].tolist()
				price=close_list[-1]
				order_stats,order_price=check_buy_order(self.c,stock=stock)
				if order_stats==True:
					base_price=order_price
				else:
					base_price=base_price
				pre_price=base_price
				#最大值
				max_value=max(close_list)
		else:
			close_list=tick['lastPrice'].tolist()
			price=close_list[-1]
			order_stats,order_price=check_buy_order(self.c,stock=stock)
			if order_stats==True:
				base_price=order_price
			else:
				base_price=base_price
			pre_price=base_price
			#最大值
			max_value=max(close_list)
		#最大涨跌幅
		max_zdf=((max_value-pre_price)/pre_price)*100
		#回落的涨跌幅
		last_zdf=((price-max_value)/max_value)*100
		if max_zdf>=x1 and last_zdf<=x2:
			print('{} {} 冲高{} 大于{} 回落{}大于{} 卖出'.format(stock,name,max_zdf,x1,last_zdf,x2))
			return 'sell'
		else:
			print('{} {} 冲高{} {} 回落{} {} 等待卖出'.format(stock,name,max_zdf,x1,last_zdf,x2))
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
			print(position)
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
def check_hold_limit_amount(c,accountid,datatype,stock='513100.SH',limit=1000):
	'''
	检查是否到持股限制数量
	'''
	position=get_position(c,accountid,datatype)
	if position.shape[0]>0:
		position=position[position['证券代码']==stock]
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				hold_amount=position['持仓量'].tolist()[-1]
			else:
				hold_amount=0
		else:
			hold_amount=0
	else:
		hold_amount=0
	av_amount=limit-hold_amount
	if av_amount>=10:
		return True
	else:
		return False
def check_hold_limit_value(c,accountid,datatype,stock='513100.SH',limit=1000,price=1):
	'''
	检查是否到持股限制金额
	'''
	limit=limit/price
	limit=adjust_amount(c,stock,limit)
	position=get_position(c,accountid,datatype)
	if position.shape[0]>0:
		position=position[position['证券代码']==stock]
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				hold_amount=position['持仓量'].tolist()[-1]
			else:
				hold_amount=0
		else:
			hold_amount=0
	else:
		hold_amount=0
	av_amount=limit-hold_amount
	if av_amount>=10:
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
def check_not_trader_data(c,stock='513100.SH'):
	'''
	检测个股没有成交的数据
	主要检测买入的
	'''
	trader_log=get_order(c,c.account,c.account_type)
	now_dat=str(datetime.now())[:10]
	#不成交代码,注e意57这个是策略下的废单，看个人是否需要
	not_list=[49,50,51,52]
	if trader_log.shape[0]>0:
		trader_log['不成交']=trader_log['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
		trader_log=trader_log[trader_log['不成交']=='是']
		trader_log=trader_log[trader_log['买卖方向']==48]
		trader_log=trader_log[trader_log['证券代码']==stock]
		if trader_log.shape[0]>0:
			not_trader_amount=trader_log['未成交数量'].sum()
			not_trader_value=trader_log['未成交金额'].sum()
		else:
			not_trader_amount=0
			not_trader_value=0
	else:
		not_trader_amount=0
		not_trader_value=0
	return not_trader_amount,not_trader_value
def check_buy_order(c,stock='513100.SH'):
	'''
	检测今天是不是有委托
	'''
	trader_log=get_order(c,c.account,c.account_type)
	now_dat=str(datetime.now())[:10]
	#成功下单
	not_list=[49,50,51,52,53,55,56]
	if trader_log.shape[0]>0:
		trader_log['成功下单']=trader_log['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
		trader_log=trader_log[trader_log['成功下单']=='是']
		trader_log=trader_log[trader_log['买卖方向']==48]
		trader_log=trader_log[trader_log['证券代码']==stock]
		if trader_log.shape[0]>0:
			price=trader_log['委托价格'].tolist()[0]
			return True,price
		else:
			return False,''
	else:
		return False,''
	
	
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
			data['股票类型']=data['证券代码'].apply(lambda x: select_data_type(x))
			data['股票类型选择']=data['股票类型'].apply(lambda x: '是' if x in c.stock_type else '不是')
			data=data[data['股票类型选择']=='是']
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
