#encoding:gbk
'''
15小果中证1000趋势增强策略代码版
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
风险告知书,代码开源,自己使用风险自担，和作者无关，代码只用于学习研究使用,不做交易参考,运行请仔细研究源代码,模拟盘测试
请在使用前仔细阅读下述内容
1、数据、计算、程序等力求但不保证绝对正确，不排除技术故障，因此带来的风险需自行承担。
2、回测数据仅代表历史，不代表未来收益，仅供参考。
3、请在使用前，充分学习和掌握，操作不当造成的后果需自行承担。
4、提供内容仅作为交流，不代表开通证券账户必然提供该服务。
5、程序化交易不代表一定能赚钱，旨在讨论、交流和学习一种更为科学的交易方式，请做好预期管理。
6、部分内容整理自互联网或得到作者授权转载分享，所述内容不代表个人观点，仅供参考学习。
7、建议投资者务必确认自身风险承受能力及投资目标,不推荐投资目标不相符的投资者参与。
8、智能交易可能因系统、通讯等原因无法正常使用或无法按照您的设置价格发出委托指令及完成成交，最终成交价格及数量以交易所、登记结算机构等记录为准。请密切关注交易回报情况及条件单设置情况。
9、提供内容仅供参考，不构成对委托指令成交的承诺，不构成投资建议，不构成收益或避免损失的承诺。请您务必仔细阅读相关风险提示及协议，了解各类智能交易功能的区别及不同风险，审慎决策是否使用相关功能。
10、所有内容仅供参考学习，均在模拟盘的环境下使用，请充分掌握后使用，实盘使用风险请自行承担。
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
def init(c):
	c.text={
		"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
		'策略名称':'小果中证1000趋势增强策略代码版',
		"账户":"55001947",
		"账户类型":"STOCK",
		"会员账户设置":"账户密码量化网页注册就可以",
		"会员账户":"test",
		"会员密码":"test",
		"会员授权码":"test",
		"授权码":"",
		"调仓时间":["14:35"],
		"股票池路径":'C:/Users/lxg123456/Desktop/ZZ1000.blk',
		"大盘风险控制算法":"大盘风险控制算法，保留的仓位资金大就可用保留，小资金可用直接0清仓",
		"是否开启风控算法":"是",
		'风控标的':"512050.SH",
		"保留仓位比例":0,
		"交易条件设置": "交易条件设置",
		"持股限制": 10,
		"买入前N":10,
		"持有限制":10,
		"交易模式说明":"金额/数量",
		"交易模式":"金额",
		"固定交易金额":10000,
		"固定交易数量":10000,
		"特殊交易标的设置":"特殊交易标的设置",
		"特殊交易标的":['511090.SH','000000.SZ'],
		"特殊交易标的固定交易金额":15000,
		"特殊交易标的固定交易数量":100,
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
		"交易结束时间":14,
		"是否参加集合竞价":"否",
		"开始交易分钟":0,
		"买入因子设置": "买入因子设置******************",
		"剔除的代码开头": [
			"688",
			"300",
			"301",
			"831",
			"832",
			"833",
			"834",
			"835",
			"836",
			"837",
			"838",
			"920",
			"430",
			"830",
			"871",
			"873",
			"600519"
			
		],
		"自定义选股函数": {
			"趋势强度": "mean_line_models_buy(x1=3,x2=5,x3=10,x4=15,x5=20)",
			"站上均线分析": "standing_average_line(n=5)",
			"涨跌幅": "cacal_price_limit()",
			"N日收益":"cacal_n_return(n=5)",
			"前N天收益":"cacal_shift_return(n=-2)",
			"六脉神剑日周期": "cacal_diurnal_cycle()",
			"六脉神剑日周期数量": "cacal_diurnal_cycle_amount(n=3)",
			"连续六脉神剑数量": "cacal_diurnal_cycle_lx(n=5)",
			"波段状态": "cacal_bond_stats()",
			"买波段的数量": "cacal_bond_lx_buy()",
			"卖波段的数量": "cacal_bond_lx_sell()",
			"分数均线":"time_sharing_average()",
		},
		"自定义选股因子选择":{
			"站上均线分析":[
				1
			],
			"分数均线":[
				1
			],
			"趋势强度":[
				75,
				100
			],
			"涨跌幅":[
				0,
				5
			],
			"N日收益":[
				3,
				20
			],
			"前N天收益":[
				0,
				7
			],
			"六脉神剑日周期": [
				4,
				6
			],
			"波段状态": [
				"买"
			]
		},
		"因子排序设置": "因子排序设置",
		"排序因子": [
			"买波段的数量",
			"N日收益",
			"连续六脉神剑数量",
			"趋势强度"
		],
		"排序方式": "降序",
		"卖出因子设置": "卖出因子设置*********",
		"自定义卖出函数": {
			"趋势强度": "mean_line_models_buy(x1=3,x2=5,x3=10,x4=15,x5=20)",
			"站上均线分析": "standing_average_line(n=5)",
			"涨跌幅": "cacal_price_limit()",
			"六脉神剑日周期": "cacal_diurnal_cycle()",
			"六脉神剑日周期数量": "cacal_diurnal_cycle_amount(n=3)",
			"连续六脉神剑数量": "cacal_diurnal_cycle_lx(n=5)",
			"波段状态": "cacal_bond_stats()",
			"买波段的数量": "cacal_bond_lx_buy()",
			"卖波段的数量": "cacal_bond_lx_sell()",
			"跌破均线分析": "tarder_down_mean_line()"
			
			
		},
		"自定义卖出因子选择": {
			"趋势强度": [
				0,
				50
			],
			"跌破均线分析": [
				1
			],
			"六脉神剑日周期": [
				0,
				3
			],
			"波段状态": [
				"卖"
			]
		}
		
	}
	#账户
	c.account=c.text['账户']
	#账户类型
	c.account_type=c.text['账户类型']
	#交易股票池
	hold_limit=c.text['持有限制']
	c.st_name=c.text['策略名称']
	stock_df=get_trader_stock(c)
	if stock_df.shape[0]>0:
		c.trade_code_list=stock_df['证券代码'].tolist()
		c.trade_code_name=stock_df['名称'].tolist()
	else:
		c.trade_code_list=[]
		c.trade_code_name=[]
	if c.account_type=='stock' or c.account_type=='STOCK':
		c.buy_code=23
		c.sell_code=24
	else:
		#融资融券
		c.buy_code=33
		c.sell_code=34
	c.buy_price_code=c.text['买入价格编码']
	c.sell_price_code=c.text['卖出价格编码']
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	c.hy_username=c.text['会员账户']
	c.hy_password=c.text['会员密码']
	c.hy_invite_code=c.text['会员授权码']
	date_list=c.text['调仓时间']
	if (c,c.hy_username,c.hy_password,c.hy_invite_code):
		#定时
		for date in date_list:
			print('策略调仓时间{}等待时间交易**************************'.format(date))
			c.run_time("run_tarder_func","1nDay","2024-07-25 {}:00".format(date))
		
		c.run_time("get_account_stock_stop_trader","3nSecond","2024-07-25 13:20:00")
		#当日止盈止损,结合涨跌幅，成本价计算
		c.run_time("get_daily_stock_stop_trader","4nSecond","2024-07-25 13:20:00")
		#检查开板卖出
		c.run_time("run_check_open_pool_sell_func","3nSecond","2024-07-25 13:20:00")
		#分析一下今天的风控
		print('分析一下今天的风控************************************************')
		run_xg_index_analaysis(c)
		#测试配置
		run_tarder_func(c)
	else:
		pass
def handlebar(c):
	
	pass
def run_xg_index_analaysis(c):
	'''
	指数风险控制
	'''
	stock=c.text['风控标的']
	hist=c.get_market_data_ex([],stock_code=[stock], period = "1d",count =-1,
			start_time='20240101',
			end_time='20500101',
			dividend_type='front')
	hist=hist[stock]
	hist=xg_index_analysis(c,hist)
	stats=hist['stats'].tolist()[-1]
	if stats=='买':
		print('没有触发指数风险控制继续安策略运行*********************')
		return False
	else:
		print('触发指数风险控制降低仓位*************************')
		return True
def adjust_index_trader(c):
	'''
	调整指数风险交易
	'''
	print('调整指数风险交易')
	trader_type=c.text['交易模式']
	fix_value=c.text['固定交易金额']
	fix_amount=c.text['固定交易数量']
	ratio=c.text['保留仓位比例']
	position=get_position(c,c.account,c.account_type)
	if position.shape[0]>0:
		for stock,av_amount,hold_amount in zip(position['证券代码'],position['可用数量'],position['持仓量']):
			try:
				price=get_price(c,stock)
				if trader_type=='金额':
					amount=fix_value/price
				else:
					amount=fix_amount
				amount=amount*ratio
				sell_amount=hold_amount-amount
				sell_amount=adjust_amount(stock,sell_amount)
				if sell_amount>=10 and av_amount>=10:
					if sell_amount>=av_amount:
						sell_amount=sell_amount
					else:
						sell_amount=av_amount
					if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
						print('调整指数风险交易 卖出{} 数量{} 价格{}'.format(stock,sell_amount,price))
						maker='{},{},{}'.format(c.st_name,'调整指数风险交易',stock)
						passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, sell_amount, maker,1,maker,c)
					else:
						print('调整指数风险交易有问题',stock,'不能卖出')
				else:
					print('调整指数风险交易有问题',stock,'不能卖出低于最小卖出单位')
			except Exception as  e:
				print(e,stock,'调整指数风险交易有问题')
	else:
		print('调整指数风险交易没有持股')
		
		
def get_read_tdx_data(c,path):
	'''
	读取通达信数据
	'''
	try:
		stock_list=[]
		with open(r'{}'.format(path)) as p:
			com=p.readlines()
		for stock in com:
			if len(stock)>=6:
				stock=stock.replace("\n", "")
				stock_list.append(stock)
		df=pd.DataFrame()
		df['证券代码']=stock_list
		def select_stock(x):
			'''
			选择股票
			'''
			stock=str(x)
			if stock[0]=='0':
				stock=stock[1:]
				stock=str(stock)+'.SZ'
			elif stock[0]=='1':
				stock=stock[1:]
				stock=str(stock)+'.SH'
			else:
				stock=stock[1:]
				stock=str(stock)+'.SZ'
			return stock
		df['证券代码']=df['证券代码'].apply(lambda x:select_stock(x))
		df['名称']=df['证券代码']
	except Exception as e:
		try:
			print(e,'通达信路径有问题可能不存在',path)
			df=pd.read_excel(r'{}'.format(path))
		except Exception as e:
			print(e)
			try:
				df=pd.read_csv(r'{}'.format(path))
			except Exception as e:
				print(e)
				df=pd.DataFrame()
	return df 
def get_trader_stock(c):
	'''
	读取交易股票池数据
	'''
	path=c.text['股票池路径']
	df=get_read_tdx_data(c,path=r'{}'.format(path))
	if df.shape[0]>0:
		df['投资备注']=c.st_name+','+'buy'+','+df['证券代码']
		df['买入黑名单']=df['证券代码'].apply(lambda x: '是' if x in c.text['买入黑名单'] else '不是')
		df=df[df['买入黑名单']=='不是']
	return df
	
def trader_info(c):
	if check_is_trader_date_1(c):
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
	if check_is_trader_date_1(c):
		x1=c.text['账户个股止盈']
		x2=c.text['账户个股止损']
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
						if True:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								
							else:
								print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
						else:
							print(maker,'在委托记录等待订单检查')
					elif zdf<=x2:
						print('{} 股票{} 账户止损 最新价{} 成本价{} 目前涨跌幅{} 小于目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
						maker=c.st_name+','+'sell'+','+stock+','+'账户止损'
						if True:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								
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
	if check_is_trader_date_1(c):
		x1=c.text['当日止盈']
		x2=c.text['当日止损']
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
						if True:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								
							else:
								print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
						else:
							print(maker,'在委托记录等待订单检查')
					elif zdf<=x2:
						print('{} 股票{} 当日止损 最新价{} 成本价{} 目前涨跌幅{} 小于目前收益{}'.format(datetime.now(),stock,price,cost_price,zdf,x1))
						maker=c.st_name+','+'sell'+','+stock+','+'当日止损'
						if True:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
								print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
								passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
								
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
def check_open_pool_sell_func(c,stock='000680.SZ'):
	'''
	检查开板卖出函数
	'''
	date=''.join(str(datetime.now())[:10].split('-'))
	#观察的tck周期
	n=10
	hist=c.get_market_data_ex([],stock_code=[stock], period = "tick",count =-1,
			start_time=date,
			end_time=date,
			dividend_type='front')
	hist=hist[stock]
	if hist.shape[0]>0:
		hist['date']=hist.index.tolist()
		hist['date']=hist['date'].apply(lambda x: int(str(x).split('.')[0][8:]))
		hist=hist[hist['date']>=92800]
		hist=hist[hist['date']<=145659]
		hist['stats']=hist['askVol'].apply(lambda x:1 if sum(x)==0 else 0)
		hist=hist[-n:]
		stats_list=hist['stats'].tolist()
		last_stats=stats_list[-1]
		cum_stats=sum(stats_list)
		if cum_stats==n:
			print(stock,'涨停没有开板')
			return False
		elif cum_stats !=n and cum_stats>=1 and last_stats==0:
			print(stock,'涨停开板卖出')
			return True
		elif cum_stats !=n and cum_stats>=1 and last_stats==1:
			print(stock,'涨停开板,再次涨停不卖出')
			return False
		else:
			print(stock,'不存在涨停不卖出')
			return False
	else:
		print('开板卖出目前没有数据不交易')
		return False
def run_check_open_pool_sell_func(c):
	'''
	检测持股开板卖出
	'''
	if check_is_trader_date_1(c):
		position=get_position(c,c.account,c.account_type)
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				for stock,cost_price,hold_amount,av_amount in zip(position['证券代码'],position['成本价'],position['持仓量'],position['可用数量']):
					try:
						price=get_price(c,stock)
						stats=check_open_pool_sell_func(c,stock)
						if stats:
							maker=c.st_name+','+'sell'+','+stock+','+'开板卖出'
							if True:
								if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
									print('开板卖出{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
									passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
									
								else:
									print('开板卖出{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
							else:
								print(maker,'在委托记录等待订单检查')
						else:
							pass
					except Exception as e:
						print(e,'开板卖出有问题')
			else:
				print('开板卖出没有持股1')
		else:
			print('开板卖出没有持股2')
	else:
		print(datetime.now(),'开板卖出不是交易时间')
def cacal_select_stock_factor(c):
	'''
	计算选股因子
	'''
	user_factor=c.text['自定义选股函数']
	factor_name=list(user_factor.keys())
	df=get_trader_stock(c)
	try:
		del_list = c.text['剔除的代码开头']
		df['剔除'] = df['证券代码'].apply(lambda x: '是' if any(str(x).startswith(prefix) for prefix in del_list) else '不是')
		df = df[df['剔除'] == '不是']
	except:
		df=df  
	df=df
	if df.shape[0]>0:
		user_factor_list=[]
		stock_list=df['证券代码'].tolist()
		j=0
		for stock  in stock_list:
			try:
			
				hist=c.get_market_data_ex([],stock_code=[stock], period = "1d",count =-1,
				start_time='20210101',
				end_time='20500101',
				dividend_type='front')
				hist=hist[stock]
				tick=c.get_full_tick(stock_code=[stock])
				tick=tick[stock]
				result_list=[]
				#分时tick
				end_time=''.join(str(datetime.now())[:10].split('-'))
				lx_tick=c.get_market_data_ex([],stock_code=[stock], period = "tick",count =-1,
				start_time=end_time,
				end_time=end_time,
				dividend_type='front')
				lx_tick=lx_tick[stock]
				for name in  factor_name:
					models=user_def_factor(stock,hist,tick,lx_tick)
					try:
					
						func=user_factor[name] 
						func='models.{}'.format(func)
						result=func)
						result_list.append(result)
					
					except Exception as e:
						print(e,'函数计算错误')
						result_list.append(None)
					
				user_factor_list.append(result_list)
			
			except Exception as e:
				print(e,stock,'买入因子计算有问题')
				user_factor_list.append([])
			j+=1
			print('买入选股计算，总数{} 已经计算{}'.format(len(stock_list),j))
		if len(user_factor_list[0])<len(factor_name):
			df1=pd.DataFrame()
		else:
			df1=pd.DataFrame(user_factor_list)
			df1.columns=factor_name
			df1['证券代码']=stock_list
			df=pd.merge(df,df1,on=['证券代码'])
	else:
		print('自定义因子计算没有数据')
	print('选股因子计算选股因子计算的结果888888888888')
	print(df)
	return df 
def get_select_buy_stock(c):
	'''
	选股因子计算的结果
	'''
	df=cacal_select_stock_factor(c)
	user_factor=c.text['自定义选股因子选择']
	factor_name=list(user_factor.keys())
	select_select=[]
	if df.shape[0]>0:
		all_columns=df.columns.tolist()
		if len(factor_name)>0:
			for name in factor_name:
				if name  in all_columns:
					try:
						df[name]=pd.to_numeric(df[name])
					except:
						pass
					try:
						min_value=user_factor[name][0]
						max_value=user_factor[name][-1]
						df=df[df[name]>=min_value]
						df=df[df[name]<=max_value]
					except Exception as e:
						print(e)
						try:
							factor_list=user_factor[name]
							df['select']=df[name].apply(lambda x: '是' if x in factor_list else '不是')
							df=df[df['select']=='是']
						except Exception as e:
							factor=user_factor[name]
							try:
								print(e,factor[0],name,'计算有问题#########')
								df=df[df[name]==factor[0]]
							except Exception as e:
								print(e,factor[0],name,'计算有问题#########')
					print('{}因子分析完成'.format(name))
				else:
					print('{}因子不在因子表里面'.format(name))
		else:
			print('没有自定义买入因子')
	else:
		print('没有买入的股票池******')
	
	return df
def get_buy_stock_rank(c):
	'''
	买入股票排序
	'''
	rank_factor=c.text['排序因子']
	rank_type=c.text['排序方式']
	if rank_type=='降序':
		rank=False
	else:
		rank=True
	df=get_select_buy_stock(c)
	if df.shape[0]>0:
		select_factor=[]
		all_factor=df.columns.tolist()
		for factor in rank_factor:
			if factor in all_factor:
				select_factor.append(factor)
			else:
				pass
		if len(select_factor)>0:
			df=df.sort_values(by=select_factor,ascending=rank)
		else:
			df=df
	else:
		df=df
	df=df.drop_duplicates()
	return df
def cacal_sell_stock_factor(c):
	'''
	卖出股票因子计算
	'''
	user_factor=c.text['自定义卖出函数']
	factor_name=list(user_factor.keys())
	hold_stock=get_position(c,c.account,c.account_type)
	df=hold_stock
	#df=pd.DataFrame()
	#df['证券代码']=['513100.SH','600031.SH']
	if df.shape[0]>0:
		df=df[df['持仓量']>=10]
		if df.shape[0]>0:
			df['投资备注']=c.st_name+','+'sell'+','+df['证券代码']
			user_factor_list=[]
			stock_list=df['证券代码'].tolist()
			
			for stock in stock_list:
				try:
					hist=c.get_market_data_ex([],stock_code=[stock], period = "1d",count =-1,
					start_time='20210101',
					end_time='20500101',
					dividend_type='front')
					hist=hist[stock]
					tick=c.get_full_tick(stock_code=[stock])
					tick=tick[stock]
					#分时tick
					end_time=''.join(str(datetime.now())[:10].split('-'))
					lx_tick=c.get_market_data_ex([],stock_code=[stock], period = "tick",count =-1,
					start_time=end_time,
					end_time=end_time,
					dividend_type='front')
					lx_tick=lx_tick[stock]
					result_list=[]
					for name in  factor_name:
						models=user_def_factor(stock,hist,tick,lx_tick)
						try:
							func=user_factor[name] 
							func='models.{}'.format(func)
							result=func)
							result_list.append(result)
						except Exception as e:
							print(e,'函数计算错误')
							result_list.append(None)
					user_factor_list.append(result_list)
				except Exception as e:
					print(e,stock,'卖出因子计算有问题')
					user_factor_list.append([])
			if len(user_factor_list[0])<len(factor_name):
				df1=pd.DataFrame()
				
			else:
				df1=pd.DataFrame(user_factor_list)
				df1.columns=factor_name
				df1['证券代码']=stock_list
				df=pd.merge(df,df1,on=['证券代码'])
		else:
			print('卖出自定义因子计算没有数据没有持股数据1')
	else:
		print('卖出自定义因子计算没有数据没有持股数据2')
	print('卖出因子计算的结果888888888888')
	print(df)
	return df 
def get_select_sell_stock(c):
	'''
	选股因子计算的结果
	'''
	df=cacal_sell_stock_factor(c)
	user_factor=c.text['自定义卖出因子选择']
	factor_name=list(user_factor.keys())
	or_df=pd.DataFrame()
	select_select=[]
	df1=df
	if df.shape[0]>0:
		all_columns=df.columns.tolist()
		if len(factor_name)>0:
			for name in factor_name:
				if name  in all_columns:
					try:
						df[name]=pd.to_numeric(df[name])
					except:
						pass
					try:
						min_value=user_factor[name][0]
						max_value=user_factor[name][-1]
						df2=df1[df1[name]>=min_value]
						df2=df2[df2[name]<=max_value]
						or_df=pd.concat([or_df,df2],ignore_index=True)
					except Exception as e:
						print(e,1,name)
						try:
							df=df1
							factor_list=user_factor[name]
							df['select']=df[name].apply(lambda x: '是' if x in factor_list else '不是')
							df2=df[df['select']=='是']
							or_df=pd.concat([or_df,df2],ignore_index=True)
						except Exception as e:
							print(e,2,name)
							factor=user_factor[name]
							df2=df1[df1[name]==factor]
							or_df=pd.concat([or_df,df2],ignore_index=True)
				else:
					print('{}因子不在因子表里面'.format(name))
			df=or_df
			df=df.drop_duplicates(keep='last')
			
		else:
			print('没有自定义卖出因子选择')
	else:
		print('没有因子数据************')
		df=pd.DataFrame()	
	return df 
def get_buy_sell_stock_data(c):
	'''
	获取买卖数据
	'''
	print('获取买卖数据*********')
	hold_limit=c.text['持股限制']
	hold_stock=get_position(c,c.account,c.account_type)
	print('8888888888888888888888888888888888888888888888')
	if hold_stock.shape[0]>0:
		hold_stock=hold_stock[hold_stock['持仓量']>=10]
		if hold_stock.shape[0]>0:
			hold_stock_list=hold_stock['证券代码'].tolist()
			hold_amount=hold_stock.shape[0]
		else:
			hold_stock_list=[]
			hold_amount=0
	else:
		hold_stock_list=[]
		hold_amount=0
	
	
	buy_df=get_buy_stock_rank(c)
	if buy_df.shape[0]>0:
		buy_df=buy_df.drop_duplicates(subset=['证券代码'], keep='last')
	else:
		buy_df=buy_df
	if buy_df.shape[0]>0:
		buy_df['持股']=buy_df['证券代码'].apply(lambda x: '是' if x in hold_stock_list else '不是')
		buy_df=buy_df[buy_df['持股']=='不是']
	else:
		buy_df=pd.DataFrame()
	sell_df=get_select_sell_stock(c)
	if sell_df.shape[0]>0:
		sell_df=sell_df.drop_duplicates(subset=['证券代码'], keep='last')
	else:
		sell_df=sell_df
	if sell_df.shape[0]>0:
		sell_df['证券代码']=sell_df['证券代码'].apply(lambda x:'0'*(6-len(str(x)))+str(x))
		sell_stock_list=sell_df['证券代码'].tolist()
		sell_amount=len(sell_stock_list)
	else:
		sell_amount=0
	av_buy=(hold_limit-hold_amount)+sell_amount
	if av_buy>=0:
		av_buy=av_buy
	else:
		print('超过持股限制不买入')
		av_buy=0
	buy_df=buy_df[:av_buy]
	print('(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
	print('买入股票数据************************')
	print(buy_df)
	print('卖出股票池***********************')
	print(sell_df)
	return buy_df,sell_df
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
def run_tarder_func(c):
	'''
	运行交易函数
	'''
	if check_is_trader_date_1(c):
		trader_models=c.text['交易模式']
		fix_value=c.text['固定交易金额']
		fix_amount=c.text['固定交易数量']
		sep_fix_value=c.text['特殊交易标的固定交易金额']
		sep_fix_amount=c.text['特殊交易标的固定交易数量']
		sep_stock_list=c.text['特殊交易标的']
		ratio=c.text['保留仓位比例']
		open_models=c.text['是否开启风控算法']
		if open_models=='是':
			print('开启风控算法********************')
			index_stats=run_xg_index_analaysis(c)
			if index_stats==True:
				fix_value=fix_value*ratio
				fix_amount=fix_amount*ratio
				sep_fix_value=sep_fix_value*ratio
				sep_fix_amount=sep_fix_amount*ratio
				#调整仓位
				adjust_index_trader(c)
			else:
				fix_value=fix_value
				fix_amount=fix_amount
				sep_fix_value=sep_fix_value
				sep_fix_amount=sep_fix_amount
		else:
			print('不开启开启风控算法******************')
		trader_log=get_order(c,c.account,c.account_type)
		now_date=str(datetime.now())[:10]
		#不成交代码,注意57这个是策略下的废单，看个人是否需要
		not_list=[49,50,51,52,54]
		if trader_log.shape[0]>0:
			trader_log['不成交']=trader_log['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
			trader_log=trader_log[trader_log['不成交']=='是']
		else:
			trader_log=trader_log
		name_list=[c.st_name]
		try:
			trader_log=trader_log.drop_duplicates(subset=['投资备注'], keep='last')
		except Exception as e:
			trader_log=pd.DataFrame()
			print(e)
		if trader_log.shape[0]>0:
			trader_log['证券代码']=trader_log['证券代码'].apply(lambda x: '0'*(6-len(str(x)))+str(x))
			trader_log['策略']=trader_log['投资备注'].apply(lambda x: str(x).split(',')[0])
			trader_log['本策略']=trader_log['策略'].apply(lambda x: '是' if x in name_list else '不是')
			trader_log=trader_log[trader_log['本策略']=='是']
			trader_maker_list=trader_log['投资备注'].tolist()
		else:
			trader_maker_list=[]
		#先卖在买入
		buy_df,sell_df=get_buy_sell_stock_data(c)
		if sell_df.shape[0]>0:
			for stock,hold_amount,av_amount,maker in zip(sell_df['证券代码'],
					sell_df['持仓量'],sell_df['可用数量'],sell_df['投资备注']):
				if True:
					if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
						print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
						passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
						
					else:
						print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
				else:
					print(maker,'在委托记录等待订单检查')
		else:
			print('没有卖出的数据')
		#买入
		if buy_df.shape[0]>0:
			for stock,maker in zip(buy_df['证券代码'].tolist(),buy_df['投资备注'].tolist()):
				price=get_price(c,stock)
				if trader_models=='数量':
					if stock  in sep_stock_list:
						print('{}在特殊标的里面*********'.format(stock))
						amount=sep_fix_amount
					else:
						amount=fix_amount
				else:
					if stock  in sep_stock_list:
						print('{}在特殊标的里面*********'.format(stock))
						amount=sep_fix_value/price
						amount=adjust_amount(stock,amount)
					else:
						amount=fix_value/price
						amount=adjust_amount(stock,amount)
				if True:
					if check_is_buy(c,c.account,c.account_type,stock=stock ,amount=amount,price=price) and amount>=10:
						passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
						print('{} 最新价格 买入{} '.format(stock,amount))
					else:
						print('{}金额交易{}买入不了,检测账户金额/风险控比例*******'.format(stock,amount))
				else:
					print(maker,'在委托记录等待订单检查')
		else:
			print('没有买入数据')
	else:
		print('{} 目前不是交易时间'.format(datetime.now()))
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
def check_is_trader_date_1(c):
	'''
	检测是不是交易时间
	'''
	trader_time=c.text['交易时间段']
	start_date=c.text['交易开始时间']
	end_date=c.text['交易结束时间']
	start_mi=c.text['开始交易分钟']
	jhjj=c.text['是否参加集合竞价']
	if decode_trader_password(c):
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
	else:
		print('授权码不对联系作者微信；xg_quant')
def (c,
	username='username',
	password='password',
	invite_code='invite_code'):
	'''
	验证用户
	'''
	import requests
	url='http:///?'
	parsms={
		"username":username,
		"password":password,
		"invite_code":invite_code
	}
	res=requests.get(url=url,params=parsms)
	text=res.json()
	status=text['status']
	if status==True or status=='True' or status=='true' or status=='TRUE':
		print('*************用户账户:{},密码:{},授权码:{}正确开启量化交易之路*************'.format(username,password,invite_code))
		print(text)
		return status
	else:
		print('*************用户账户:{},密码:{},授权码:{}不正确退出系统,权限找管理员*********'.format(username,password,invite_code))
		print(text)
		return status
def get_n1_n2_daily(c,start_date='2023-12-14',end_date='2023-12-30'):
	'''
	获取2个时间的天数
	'''
	import datetime
	end_date=end_date.split('-')
	start_date=start_date.split('-')
	d1 =datetime.datetime(int(start_date[0]),int(start_date[1]),int(start_date[2])) 
	d2 = datetime.datetime(int(end_date[0]),int(end_date[1]),int(end_date[2]))   # 第二个日期
	interval = d2 - d1                   # 两日期差距
	days=interval.days  
	return days
def decode_trader_password(c):
	password_str=c.text['授权码']
	text=password_str
	text=str(password_str))
	start_date=str(datetime.now())[:10]
	year=text[100:104]
	moth=text[163:165]
	daily=text[184:186]
	end_date='{}-{}-{}'.format(year,moth,daily)
	daily=get_n1_n2_daily(c,start_date=start_date,end_date=end_date)
	if text[8]=='9' and text[16]=='9' and text[24]=='9' and text[32]=='9' and daily>0:
		print('作者:小果量化,微信:xg_quant************授权码正确,到期日{} 剩余天数{}******************'.format(end_date,daily))
		return True
	else:
		print('授权码不对联系作者:小果量化,微信:xg_quant')

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
			is_del=c.text['是否隔离策略']
			df['证券代码']=df['证券代码'].astype(str)
			df['隔离策略']=df['证券代码'].apply(lambda x: '是' if x in c.trade_code_list else '不是')
			df=df[df['隔离策略']=='是']
			data=df
			data['卖出黑名单']=data['证券代码'].apply(lambda x: '是' if x in c.text['卖出黑名单'] else '不是')
			data=data[data['卖出黑名单']=='不是']
			
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
class user_def_factor:
	'''
	自定义因子框架
	对于真和假的判断用1，0替代
	'''
	def __init__(self,stock,hist,spot,lx_tick):
		self.stock=stock
		self.hist=hist
		self.df=hist
		self.tick=spot
		self.lx_tick=lx_tick
	def time_sharing_average(self):
		'''
		分数均线
		'''
		df=self.lx_tick
		df['select']=df.index
		df['select']=df['select'].apply(lambda x: int(str(x).split('.')[0][-6:-2]))
		df=df[df['select']>=930]
		lastPrice=df['lastPrice'].tolist()[-1]
		df['sharing_average']=df['amount']/df['volume']/100
		sharing_average=df['sharing_average'].tolist()[-1]
		if lastPrice>sharing_average:
			return 1
		else:
			return 0
	def cacal_limit(self):
		'''
		计算涨跌幅
		'''
		try:
			tick=self.tick
			limit=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
			return limit
		except:
			print('{}涨跌幅计算有问题'.format(stock ))
			return -40
	def get_price(self):
		'''
		获取最新价格
		'''
		tick=self.tick
		price=tick['lastPrice']
		return price
	def tarder_up_mean_line(self,line=5):
		'''
		站上交易均线
		'''
		df=self.hist
		price=df['close'].tolist()[-1]
		df['line']=df['close'].rolling(line).mean()
		mean_line=df['line'].tolist()[-1]
		if price>=mean_line:
			return 1
		else:
			return 0
	def tarder_down_mean_line(self,line=5):
		'''
		跌破交易均线
		'''
		df=self.hist
		price=df['close'].tolist()[-1]
		df['line']=df['close'].rolling(line).mean()
		mean_line=df['line'].tolist()[-1]
		if price<mean_line:
			return 1
		else:
			return 0
	def stock_stop_up(self,limit=3):
		'''
		当日止盈
		'''
		df=self.df
		
		df['day_limit']=df['close'].pct_change()*100
		day_limit=df['day_limit'].tolist()[-1]
		if limit>=day_limit:
			return 1 
		else:
			return 0
	def stock_stop_down(self,limit=-6):
		'''
		当日止损
		'''
		df=self.df
		
		df['day_limit']=df['close'].pct_change()*100
		day_limit=df['day_limit'].tolist()[-1]
		if day_limit<=limit:
			return 1 
		else:
			return 0
	def standing_average_line(self,n=5):
		'''
		站上均线分析
		'''
		df=self.df
		df['n']=df['close'].rolling(n).mean()
		line=df['n'].tolist()[-1]
		price=df['close'].tolist()[-1]
		if price>=line:
			return 1
		else:
			return 0
	def cacal_n_return(self,n=5):
		'''
		计算N日收益
		'''
		df=self.df
		df['n']=df['close'].pct_change()
		ratio=sum(df['n'][-n:].tolist())
		return ratio*100
	def cacal_shift_return(self,n=-2):
		'''
		计算前几天收益
		'''
		df=self.df
		df['n']=df['close'].pct_change()
		n_list=df['n'].tolist()
		ratio=n_list[n]
		return ratio*100
		
		
	def down_average_line(self,n=5):
		'''
		跌破均线分析
		'''
		df=self.df
		df['n']=df['close'].rolling(n).mean()
		line=df['n'].tolist()[-1]
		price=df['close'].tolist()[-1]
		if line>=price:
			return 1
		else:
			return 0
	def cacal_price_limit(self):
		'''
		计算涨跌幅
		'''
		try:
			tick=self.tick
			limit=((tick['lastPrice']-tick['lastClose'])/tick['lastClose'])*100
			return limit
		except:
			print('{}涨跌幅计算有问题'.format(stock ))
			return -40
	def cacal_diurnal_cycle(self):
		'''
		计算日周期
		'''
		df=self.df
		df=self.six_pulse_excalibur()
		
		signal=df['signal'].tolist()[-1]
		return signal
	def cacal_diurnal_cycle_amount(self,n=5):
		'''
		计算日周期数量
		'''
		df=self.df
		df=self.six_pulse_excalibur()
		signal=df['signal'].tolist()[-n:]
		return sum(signal)
	def cacal_diurnal_cycle_lx(self,n=5):
		'''
		连续六脉神剑数量
		'''
		df=self.six_pulse_excalibur()[-n:]
		amount=BARSLASTCOUNT(df['signal']>=5)
		return amount.tolist()[-1]
	def cacal_bond_stats(self):
		'''
		波段状态
		'''
		df=self.df
		df=self.small_fruit_band_trading()
		stats=df['stats'].tolist()[-1]
		return stats
	def cacal_bond_lx_buy(self):
		'''
		连续买波段的数量
		'''
		df=self.df
		df=self.small_fruit_band_trading()
		df['stats']=df['stats'].apply(lambda x: 1 if x=='买' else 0)
		stats=df['stats']
		amount=BARSLASTCOUNT(stats>=1)
		return amount.tolist()[-1]
	def cacal_bond_lx_sell(self):
		'''
		连续卖波段的数量
		'''
		df=self.df
		df=self.small_fruit_band_trading()
		df['stats']=df['stats'].apply(lambda x: 1 if x=='买' else 0)
		stats=df['stats']
		amount=BARSLASTCOUNT(stats<=0)
		return amount.tolist()[-1]
	def mean_line_models_buy(self,x1=3,x2=5,x3=10,x4=15,x5=20):
		'''
		均线模型
		趋势模型
		'''
		df=self.df
		df1=pd.DataFrame()
		df1['x1']=df['close'].rolling(window=x1).mean()
		df1['x2']=df['close'].rolling(window=x2).mean()
		df1['x3']=df['close'].rolling(window=x3).mean()
		df1['x4']=df['close'].rolling(window=x4).mean()
		df1['x5']=df['close'].rolling(window=x5).mean()
		score=0
		#加分的情况
		mean_x1=df1['x1'].tolist()[-1]
		mean_x2=df1['x2'].tolist()[-1]
		mean_x3=df1['x3'].tolist()[-1]
		mean_x4=df1['x4'].tolist()[-1]
		mean_x5=df1['x5'].tolist()[-1]
		#相邻2个均线进行比较
		if mean_x1>=mean_x2:
			score+=25
		if mean_x2>=mean_x3:
			score+=25
		if mean_x3>=mean_x4:
			score+=25
		if mean_x4>=mean_x5:
			score+=25
		return score
	def six_pulse_excalibur(self):
		'''
		六脉神剑
		'''
		markers=0
		signal=0
		df=self.hist
		#df=self.data.get_hist_data_em(stock=stock)
		CLOSE=df['close']
		LOW=df['low']
		HIGH=df['high']
		DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
		DEA=EMA(DIFF,5)
		#如果满足DIFF>DEA 在1的位置标记1的图标
		#DRAWICON(DIFF>DEA,1,1);
		markers+=IF(DIFF>DEA,1,0)[-1]
		#如果满足DIFF<DEA 在1的位置标记2的图标
		#DRAWICON(DIFF<DEA,1,2);
		markers+=IF(DIFF<DEA,1,0)[-1]
		#DRAWTEXT(ISLASTBAR=1,1,'. MACD'),COLORFFFFFF;{微信公众号:数据分析与运用}
		ABC1=DIFF>DEA
		signal+=IF(ABC1,1,0)[-1]
		尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
		K=SMA(尊重市场1,3,1)
		D=SMA(K,3,1)
		#如果满足k>d 在2的位置标记1的图标
		markers+=IF(K>D,1,0)[-1]
		#DRAWICON(K>D,2,1);
		markers+=IF(K<D,1,0)[-1]
		#DRAWICON(K<D,2,2);
		#DRAWTEXT(ISLASTBAR=1,2,'. KDJ'),COLORFFFFFF;
		ABC2=K>D
		signal+=IF(ABC2,1,0)[-1]
		指标营地=REF(CLOSE,1)
		RSI1=(SMA(MAX(CLOSE-指标营地,0),5,1))/(SMA(ABS(CLOSE-指标营地),5,1))*100
		RSI2=(SMA(MAX(CLOSE-指标营地,0),13,1))/(SMA(ABS(CLOSE-指标营地),13,1))*100
		markers+=IF(RSI1>RSI2,1,0)[-1]
		#DRAWICON(RSI1>RSI2,3,1);
		markers+=IF(RSI1<RSI2,1,0)[-1]
		#DRAWICON(RSI1<RSI2,3,2);
		#DRAWTEXT(ISLASTBAR=1,3,'. RSI'),COLORFFFFFF;
		ABC3=RSI1>RSI2
		signal+=IF(ABC3,1,0)[-1]
		尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
		LWR1=SMA(尊重市场,3,1)
		LWR2=SMA(LWR1,3,1)
		#DRAWICON(LWR1>LWR2,4,1);
		markers+=IF(LWR1>LWR2,1,0)[-1]
		#DRAWICON(LWR1<LWR2,4,2);
		markers+=IF(LWR1<LWR2,1,0)[-1]
		#DRAWTEXT(ISLASTBAR=1,4,'. LWR'),COLORFFFFFF;
		ABC4=LWR1>LWR2
		signal+=IF(ABC4,1,0)[-1]
		BBI=(MA(CLOSE,3)+MA(CLOSE,5)+MA(CLOSE,8)+MA(CLOSE,13))/4
		#DRAWICON(CLOSE>BBI,5,1);
		markers+=IF(CLOSE>BBI,1,0)[-1]
		#DRAWICON(CLOSE<BBI,5,2);
		markers+=IF(CLOSE<BBI,1,0)[-1]
		#DRAWTEXT(ISLASTBAR=1,5,'. BBI'),COLORFFFFFF;
		ABC10=7
		ABC5=CLOSE>BBI
		signal+=IF(ABC5,1,0)[-1]
		MTM=CLOSE-REF(CLOSE,1)
		MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
		MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
		markers+=IF(MMS>MMM,1,0)[-1]
		#DRAWICON(MMS>MMM,6,1);
		markers+=IF(MMS<MMM,1,0)[-1]
		#DRAWICON(MMS<MMM,6,2);
		#DRAWTEXT(ISLASTBAR=1,6,'. ZLMM'),COLORFFFFFF;
		ABC6=MMS>MMM
		signal+=IF(ABC6,1,0)[-1]
		df['signal']=signal
		return df
	def small_fruit_band_trading(self):
		'''
		小果波段交易
		'''
		df=self.hist
		CLOSE=df['close']
		C=df['close']
		LOW=df['low']
		L=df['low']
		HIGH=df['high']
		H=df['high']
		OPEN=df['open']
		O=df['open']
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
				stats_list.append('买')
			elif sell=='卖':
				stats_list.append('卖')
			else:
				stats_list.append(None)
		df['stats']=stats_list
		df['stats']=df['stats'].fillna(method='ffill')
		return df
def xg_index_analysis(c,hist):
		'''
		小果指数风险控制
		'''
		df=hist
		CLOSE=df['close']
		C=df['close']
		LOW=df['low']
		L=df['low']
		HIGH=df['high']
		H=df['high']
		OPEN=df['open']
		O=df['open']
		N1=18
		N2=14
		N3=10
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
				stats_list.append('买')
			elif sell=='卖':
				stats_list.append('卖')
			else:
				stats_list.append(None)
		df['stats']=stats_list
		df['stats']=df['stats'].fillna(method='ffill')
		return df
def RD(N,D=3):   
	#四舍五入取3位小数 
	return np.round(N,D)        
def RET(S,N=1):  
	#返回序列倒数第N个值,默认返回最后一个
	return np.array(S)[-N]      
def ABS(S):  
	#返回N的绝对值    
	return np.abs(S)
def MAX(S1,S2): 
	#序列max 
	return np.maximum(S1,S2)    
def MIN(S1,S2):  
	 #序列min
	return np.minimum(S1,S2)   
def IF(S,A,B): 
	#序列布尔判断 return=A  if S==True  else  B  
	return np.where(S,A,B)      
def AND(S1,S2):
	#and
	return np.logical_and(S1,S2)
def OR(S1,S2):
	#or
	return np.logical_or(S1,S2)
def RANGE(A,B,C):
	'''
	期间函数
	B<=A<=C
	'''
	df=pd.DataFrame()
	df['select']=A.tolist()
	df['select']=df['select'].apply(lambda x: True if (x>=B and x<=C) else False)
	return df['select']

def REF(S, N=1):          #对序列整体下移动N,返回序列(shift后会产生NAN)    
	return pd.Series(S).shift(N).values  

def DIFF(S, N=1):         #前一个值减后一个值,前面会产生nan 
	return pd.Series(S).diff(N).values     #np.diff(S)直接删除nan，会少一行

def STD(S,N):             #求序列的N日标准差，返回序列    
	return  pd.Series(S).rolling(N).std(ddof=0).values     

def SUM(S, N):            #对序列求N天累计和，返回序列    N=0对序列所有依次求和         
	return pd.Series(S).rolling(N).sum().values if N>0 else pd.Series(S).cumsum().values  

def CONST(S):             #返回序列S最后的值组成常量序列
	return np.full(len(S),S[-1]) 
def HHV(S,N):             #HHV(C, 5) 最近5天收盘最高价        
	return pd.Series(S).rolling(N).max().values     

def LLV(S,N):             #LLV(C, 5) 最近5天收盘最低价     
	return pd.Series(S).rolling(N).min().values    
	
def HHVBARS(S,N):         #求N周期内S最高值到当前周期数, 返回序列
	return pd.Series(S).rolling(N).apply(lambda x: np.argmax(x[::-1]),raw=True).values 

def LLVBARS(S,N):         #求N周期内S最低值到当前周期数, 返回序列
	return pd.Series(S).rolling(N).apply(lambda x: np.argmin(x[::-1]),raw=True).values    
	  
def MA(S,N):              #求序列的N日简单移动平均值，返回序列                    
	return pd.Series(S).rolling(N).mean().values  
	
def EMA(S,N):             #指数移动平均,为了精度 S>4*N  EMA至少需要120周期     alpha=2/(span+1)    
	return pd.Series(S).ewm(span=N, adjust=False).mean().values     

def SMA(S, N, M=1):       #中国式的SMA,至少需要120周期才精确 (雪球180周期)    alpha=1/(1+com)    
	return pd.Series(S).ewm(alpha=M/N,adjust=False).mean().values           #com=N-M/M

def DMA(S, A):            #求S的动态移动平均，A作平滑因子,必须 0<A<1  (此为核心函数，非指标）
	return pd.Series(S).ewm(alpha=A, adjust=True).mean().values

def WMA(S, N):            #通达信S序列的N日加权移动平均 Yn = (1*X1+2*X2+3*X3+...+n*Xn)/(1+2+3+...+Xn)
	return pd.Series(S).rolling(N).apply(lambda x:x[::-1].cumsum().sum()*2/N/(N+1),raw=True).values 
	  
def AVEDEV(S, N):         #平均绝对偏差  (序列与其平均值的绝对差的平均值)   
	return pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values 

def SLOPE(S, N):          #返S序列N周期回线性回归斜率            
	return pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N),x,deg=1)[0],raw=True).values

def FORCAST(S, N):        #返回S序列N周期回线性回归后的预测值， jqz1226改进成序列出    
	return pd.Series(S).rolling(N).apply(lambda x:np.polyval(np.polyfit(range(N),x,deg=1),N-1),raw=True).values  

def LAST(S, A, B):        #从前A日到前B日一直满足S_BOOL条件, 要求A>B & A>0 & B>=0 
	return np.array(pd.Series(S).rolling(A+1).apply(lambda x:np.all(x[::-1][B:]),raw=True),dtype=bool) 
	#------------------   1级：应用层函数(通过0级核心函数实现） ----------------------------------
def COUNT(S, N):                       # COUNT(CLOSE>O, N):  最近N天满足S_BOO的天数  True的天数
	return SUM(S,N)    

def EVERY(S, N):                       # EVERY(CLOSE>O, 5)   最近N天是否都是True
	return  IF(SUM(S,N)==N,True,False)                     
def EXIST(S, N):                       # EXIST(CLOSE>3010, N=5)  n日内是否存在一天大于3000点  
	return IF(SUM(S,N)>0,True,False)

def FILTER(S, N):                      # FILTER函数，S满足条件后，将其后N周期内的数据置为0, FILTER(C==H,5)
	for i in range(len(S)): S[i+1:i+1+N]=0  if S[i] else S[i+1:i+1+N]        
	return S                           # 例：FILTER(C==H,5) 涨停后，后5天不再发出信号 
	  
def BARSLAST(S):                       #上一次条件成立到当前的周期, BARSLAST(C/REF(C,1)>=1.1) 上一次涨停到今天的天数 
	M=np.concatenate(([0],np.where(S,1,0)))  
	for i in range(1, len(M)):  M[i]=0 if M[i] else M[i-1]+1    
	return M[1:]                       

def BARSLASTCOUNT(S):                  # 统计连续满足S条件的周期数        by jqz1226
	rt = np.zeros(len(S)+1)            # BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数
	for i in range(len(S)): rt[i+1]=rt[i]+1  if S[i] else rt[i+1]
	return rt[1:]  
	  
def BARSSINCEN(S, N):                  # N周期内第一次S条件成立到现在的周期数,N为常量  by jqz1226
	return pd.Series(S).rolling(N).apply(lambda x:N-1-np.argmax(x) if np.argmax(x) or x[0] else 0,raw=True).fillna(0).values.astype(int)

	  
def CROSS(S1, S2):                     #判断向上金叉穿越 CROSS(MA(C,5),MA(C,10))  判断向下死叉穿越 CROSS(MA(C,10),MA(C,5))   
	return np.concatenate(([False], np.logical_not((S1>S2)[:-1]) & (S1>S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226
def CROSS_UP(S1, S2):                     #判断向上金叉穿越 CROSS(MA(C,5),MA(C,10))  判断向下死叉穿越 CROSS(MA(C,10),MA(C,5))   
	return np.concatenate(([False], np.logical_not((S1>S2)[:-1]) & (S1>S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226
def CROSS_DOWN(S1, S2):                     
	return np.concatenate(([False], np.logical_not((S1<S2)[:-1]) & (S1<S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226

def LONGCROSS(S1,S2,N):                #两条线维持一定周期后交叉,S1在N周期内都小于S2,本周期从S1下方向上穿过S2时返回1,否则返回0         
	return  np.array(np.logical_and(LAST(S1<S2,N,1),(S1>S2)),dtype=bool)            # N=1时等同于CROSS(S1, S2)
		
def VALUEWHEN(S, X):                   #当S条件成立时,取X的当前值,否则取VALUEWHEN的上个成立时的X值   by jqz1226
	return pd.Series(np.where(S,X,np.nan)).ffill().values  
