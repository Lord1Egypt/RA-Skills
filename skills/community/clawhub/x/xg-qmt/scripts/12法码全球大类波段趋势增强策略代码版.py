#encoding:gbk
'''
12小果全球大类波段趋势增强策略代码版,策略模板,只做学习研究
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

class A():
	pass
a=A()
def init(c):
	c.text={
		"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
		'策略名称':'小果全球大类波段趋势增强策略代码版',
		"账户":"55001947",
		"账户类型":"STOCK",
		"会员账户设置":"账户密码量化网页注册就可以",
		"会员账户":"test",
		"会员密码":"test",
		"会员授权码":"test",
		"授权码":"",
		"调仓时间":["09:45","14:35"],
		"买入价格编码":4,
		"卖出价格编码":6,
		"是否隔离策略":"是",
		"交易模式说明":"金额/数量",
		"交易模式":"金额",
		"固定交易金额":1000,
		"固定交易数量":100,
		"特殊交易标的设置":"特殊交易标的设置",
		"特殊交易标的":['511360.SH', '159651.SZ', '511580.SH', '511380.SH', '159649', '511270.SH',
		'511030.SH', '511100.SH', '159816.SZ','159651.SZ', '159972.SZ','159651.SZ', '511260.SH', '511010.SH', '511220.SH',
		'511020.SH', '511520.SH', '511060.SH', '511180.SH', '511130.SH', '511090.SH'],
		"特殊交易标的固定交易金额":15000,
		"特殊交易标的固定交易数量":100,
		"买入前N":10,
		"持有限制":10,
		"持股限制":10,
		"时间设置":"时间设置********",
		"交易时间段":4,
		"交易开始时间":9,
		"交易结束时间":24,
		"是否参加集合竞价":"否",
		"开始交易分钟":0,
		'自定义股票池':"自定义股票池设置",
		"股票池设置":"持有限制10的股票池设置",
		"股票池":["513100.SH", "159937.SZ", "159941.SZ", "512890.SH", 
				"159934.SZ", "510300.SH", "159659.SZ", "159915.SZ", 
				"511130.SH", "159680.SZ", "159612.SZ", 
				"159887.SZ", "159351.SZ",'159611.SZ'],
		"股票池名称":["纳斯达克ETF", "黄金ETF", "纳斯达克ETF",
			"红利ETF", "黄金ETF", "沪深300ETF", "纳斯达克ETF", 
			"创业板ETF", "30年债券ETF", "中证1000ETF",
			"标普500ETF", "银行ETF", "A500ETF",'159611.SZ']
	}
	#账户
	c.account=c.text['账户']
	#账户类型
	c.account_type=c.text['账户类型']
	#交易股票池
	hold_limit=c.text['持有限制']
	a.trade_code_list=c.text['股票池']
	a.trade_code_name=c.text['股票池名称']
	c.st_name=c.text['策略名称']
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
			print('策略在{}调仓,等待策略交易****************************************'.format(date))
			c.run_time("run_tarder_func","1nDay","2024-07-25 {}:00".format(date))
		print(run_tarder_func(c))
		#5分钟不成交撤单
		#c.run_time("run_order_trader_func","300nSecond","2024-07-25 13:20:00")
		#30分钟一次
		#c.run_time("run_tarder_func","1800nSecond","2024-07-25 13:20:00")
		c.run_time("trader_info","3nSecond","2024-07-25 13:20:00")
	else:
		pass
		
	
def handlebar(c):
	
	pass
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
def get_trader_stock(c):
	'''
	获取交易股票池
	'''
	df=pd.DataFrame()
	try:
		df['证券代码']=c.text['股票池']
		df['名称']=c.text['股票池名称']
	except Exception as e:
		print(e,'股票池获取有问题')
	return df 
	
def get_select_buy_stock(c):
	'''
	买入股票
	'''
	hold_stock=get_position(c,c.account,c.account_type)
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
	df=get_trader_stock(c)
	if df.shape[0]>0:
		df['持股检查']=df['证券代码'].apply(lambda x: '是' if x in hold_stock_list else '不是')
		df=df[df['持股检查']=='不是']
	else:
		df
	if df.shape[0]>0:
		stats_list=[]
		stats_count_list=[]
		stock_list=df['证券代码'].tolist()
		for stock in stock_list:
			try:
				hist=c.get_market_data_ex([],stock_code=[stock], period = "1d",count =-1,
				start_time='20210101',
				end_time='20500101',
				dividend_type='front')
				hist=hist[stock]
				func=small_fruit_band_trading(c,hist)
				stats=func['stats'].tolist()[-1]
				stats_count=BARSLASTCOUNT(func['stats']=='买')
				stats_list.append(stats)
				stats_count_list.append(stats_count.tolist()[-1])
			except Exception as e:
				print(e,stock,'买入分析计算有问题**********')
				stats_list.append(None)
				stats_count_list.append(None)
		df['stats']=stats_list
		df['连续波段数量']=stats_count_list
		print(df)
		df['投资备注']=c.st_name+','+'buy'+','+df['证券代码']
		df=df[df['stats']=='买']
		if df.shape[0]>0:
			df=df.sort_values(by='连续波段数量',ascending=False)
			df=df.drop_duplicates(subset=['证券代码'])
		else:
			df=df
		print('买入分析数据**********************')
		print(df)
			
	else:
		df=pd.DataFrame()
	return df
def get_select_sell_stock(c):
	'''
	获取卖出股票
	'''
	hold_stock=get_position(c,c.account,c.account_type)
	if hold_stock.shape[0]>0:
		hold_stock=hold_stock[hold_stock['持仓量']>=10]
		if hold_stock.shape[0]>0:
			stats_list=[]
			for stock in hold_stock['证券代码'].tolist():
				try:
					hist=c.get_market_data_ex([],stock_code=[stock], period = "1d",count =-1,
					start_time='20210101',
					end_time='20500101',
					dividend_type='front')
					hist=hist[stock]
					func=small_fruit_band_trading(c,hist)
					stats=func['stats'].tolist()[-1]
					stats_list.append(stats)
				except Exception as e:
					print(e,stock,'卖出分析计算有问题**********')
					stats_list.append(None)
			hold_stock['stats']=stats_list
		hold_stock['投资备注']=c.st_name+','+'sell'+','+hold_stock['证券代码']
		print('卖出股票分析数据*********************')
		print(hold_stock)
		hold_stock=hold_stock[hold_stock['stats']=='卖']
		print('卖出股票数据***********************')
		print(hold_stock)
	else:
		hold_stock=pd.DataFrame()
	return hold_stock
def get_buy_sell_stock_data(c):
	'''
	获取买卖数据
	'''
	print('获取买卖数据*********')
	hold_limit=c.text['持股限制']
	hold_stock=get_position(c,c.account,c.account_type)
	if hold_stock.shape[0]>0:
		hold_stock=hold_stock[hold_stock['持仓量']>=10]
		if hold_stock.shape[0]>0:
			hold_stock_list=hold_stock['证券代码'].tolist()
			hold_amount_dict=dict(zip(hold_stock['证券代码'].tolist(),hold_stock['持仓量'].tolist()))
			av_amount_dict=dict(zip(hold_stock['证券代码'].tolist(),hold_stock['可用数量'].tolist()))
			hold_amount=hold_stock.shape[0]
			
		else:
			hold_stock_list=[]
			hold_amount_dict={}
			av_amount_dict={}
			hold_amount=0
	else:
		hold_amount_dict={}
		av_amount_dict={}
		hold_stock_list=[]
		hold_amount=0
	buy_df=get_select_buy_stock(c)
	print(buy_df)
	if buy_df.shape[0]>0:
		def select_data(stock):
			if str(stock) in hold_stock_list:
				return '持股超过限制'
			else:
				return '没有持股'
		buy_df['持股检查']=buy_df['证券代码'].apply(select_data)
		buy_df=buy_df[buy_df['持股检查']=='没有持股']
	sell_df=get_select_sell_stock(c)
	if sell_df.shape[0]>0:
		sell_df['证券代码']=sell_df['证券代码'].apply(lambda x:'0'*(6-len(str(x)))+str(x))
		sell_df['持仓量']=sell_df['证券代码'].apply(lambda x: hold_amount_dict.get(x))
		sell_df['可用数量']=sell_df['证券代码'].apply(lambda x: av_amount_dict.get(x))
		sell_stock_list=sell_df['证券代码'].tolist()
		sell_amount=len(sell_stock_list)
	else:
		sell_amount=0
	av_buy=(hold_limit-hold_amount)+sell_amount
	if av_buy<0:
		av_buy=0
		print('达到持股限制不买入')
	else:
		av_buy=av_buy
	buy_df=buy_df[:av_buy]
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
	trader_models=c.text['交易模式']
	fix_value=c.text['固定交易金额']
	fix_amount=c.text['固定交易金额']
	sep_fix_value=c.text['特殊交易标的固定交易金额']
	sep_fix_amount=c.text['特殊交易标的固定交易数量']
	sep_stock_list=c.text['特殊交易标的']
	if check_is_trader_date_1(c):
		#先卖在买入
		buy_df,sell_df=get_buy_sell_stock_data(c)
		if sell_df.shape[0]>0:
			for stock,hold_amount,av_amount,maker in zip(sell_df['证券代码'],
					sell_df['持仓量'],sell_df['可用数量'],sell_df['投资备注']):
				if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount) and av_amount>=10:
					print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
					passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
				else:
					print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
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
				if check_is_buy(c,c.account,c.account_type,stock=stock ,amount=amount,price=price) and amount>=10:
					passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
					print('{} 最新价格 买入{} '.format(stock,amount))
				else:
					print('{}金额交易买入不了*******'.format(stock))
		else:
			print('没有买入数据')
	else:
		print('{} 目前不少交易时间'.format(datetime.now()))
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
def small_fruit_band_trading(c,hist):
	'''
	小果波段交易
	N1赋值:7
	N2赋值:5
	N3赋值:3
	ABC1赋值:(((最高价 + 最低价)+(收盘价*2)) / 4)
	ABC3赋值:ABC1的N1日指数移动平均
	ABC4赋值:ABC1的N1日估算标准差
	ABC5赋值:((ABC1 - ABC3)*100) / ABC4
	ABC6赋值:ABC5的N2日指数移动平均
	RK7赋值:ABC6的N1日指数移动平均
	UP赋值:(ABC6的10日指数移动平均+(100 / 2)) - 5,画红色
	DOWN赋值:UP的N3日指数移动平均
	ACB1赋值:DOWN的N3日指数移动平均
	ACB2赋值:ACB1的N3日指数移动平均,画绿色
	ACB3赋值:ACB2的N3日指数移动平均
	ACB4赋值:ACB3的N3日指数移动平均
	当满足条件UP<1日前的UP时,在UP和UP的3日简单移动平均位置之间画柱状线,宽度为5,0不为0则画空心柱.,画蓝色
	当满足条件UP>1日前的UP时,在UP和UP的3日指数移动平均位置之间画柱状线,宽度为5,0不为0则画空心柱.,画洋红色
	当满足条件UP>1日前的UPANDREF(UP,1)<2日前的UP时,在UP位置书写文字,画红色
	当满足条件UP<1日前的UPANDREF(UP,1)>2日前的UP时,在UP位置书写文字,画绿色
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
	volume=df['volume']
	V=df['volume']
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
			df['隔离策略']=df['证券代码'].apply(lambda x: '是' if x in a.trade_code_list else '不是')
			df=df[df['隔离策略']=='是']
			data=df
			
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

def RD(N,D=3):   
	#四舍五入取3位小数 
	return np.round(N,D)        
def RET(S,N=1):  
	#返回序列倒数第N个值,默认返回最后一个
	return np.array(S)[-N]      
def ABS(S
):  
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