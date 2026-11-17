#encoding:gbk
'''
6法玛趋势回归动量策略代码版,策略改写来自聚宽,策略模板,只做学习研究
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
	'策略名称':'法玛趋势回归动量策略代码版',
	"会员账户设置":"账户密码量化网页注册就可以",
	"账户":"",
	"密码":"",
	"授权码":"",
	"授权码":"",
	"账户":"55001947",
	"账户类型":"STOCK",
	"是否开启策略隔离":"是",
	"调仓时间":"09:31",
	"买入价格编码":4,
	"卖出价格编码":6,
	"动量天数":25,
	"买入数量":1,
	"风险控制线":10,
	"交易模式说明":"金额/数量/百分比",
	"交易模式":"金额",
	"下单值":1000,
	"交易时间段":4,
	"交易开始时间":9,
	"交易结束时间":14,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	"股票池":"518880.SH,513100.SH,159915.SZ,510180.SH",
	"股票池名称":"黄金ETF,纳指100,创业板100,上证180",
}
	#账户
	c.account=c.text['账户']
	#账户类型
	c.account_type=c.text['账户类型']
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
	#定时
	if (c,c.hy_username,c.hy_password,c.hy_invite_code):
		#定时
		trader_date=c.text['调仓时间'].split(',')
		for date in trader_date:
			c.run_time("trade","1nDay","2024-07-25 {}:00".format(date))
			print('开始运行策略每天的{}调仓*******************'.format(date))
		c.run_time("run_log","3nSecond","2024-07-25 13:20:00")
		trade(c)
	else:
		pass
def handlebar(c):
	pass
def run_log(c):
	if check_is_trader_date_1(c):
		print('等待策略调仓每天的9点31调仓*******')
		
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
		df['证券代码']=c.text['股票池'].split(',')
		df['名称']=c.text['股票池名称'].split(',')
	except Exception as e:
		print(e,'股票池获取有问题')
	return df 
def MOM(c,etf='513100.SH'):
	'''
	计算动量
	'''
	n=c.text['动量天数']
	r_line=c.text['风险控制线']
	stock=etf
	df=c.get_market_data_ex([],stock_code=[stock], period = "1d",count =-1,
		start_time='20210101',
		end_time='20500101',
		dividend_type='front')
	df=df[stock]
	df['line']=df['close'].rolling(r_line).mean()
	df=df[-n:]
	y = np.log(df['close'].values)
	n = len(y)  
	x = np.arange(n)
	weights = np.linspace(1,2, n)  # 线性增加权重
	slope, intercept = np.polyfit(x, y, 1, w=weights)
	annualized_returns = math.pow(math.exp(slope), 250) - 1
	residuals = y - (slope * x + intercept)
	weighted_residuals = weights * residuals**2
	r_squared = 1 - (np.sum(weighted_residuals) / np.sum(weights * (y - np.mean(y))**2))
	last_price=df['close'].tolist()[-1]
	last_line=df['line'].tolist()[-1]
	if last_price<last_line:
		score=-100
	else:
		score = annualized_returns * r_squared
	return score
# 基于年化收益和判定系数打分的动量因子轮动 https://www.joinquant.com/post/26142
def get_rank(c,etf_pool=["518880.SH","513100.SH",
	"159915.SZ","510180.SH"]):
	score_list = []
	for etf in etf_pool:
		score = MOM(c,etf)
		score_list.append(score)
	df = pd.DataFrame(index=etf_pool, data={'score':score_list})
	df = df.sort_values(by='score', ascending=False)
	df['证券代码']=df.index.tolist()
	name_dict=dict(zip(c.text['股票池'].split(','),c.text['股票池名称'].split(',')))
	df['名称']=df['证券代码'].apply(lambda x: name_dict.get(x,x))
	df=df[['证券代码','名称','score']]
	print('今日动量计算排行***************')
	print(df)
	#total_score = df['score'].sum() 不告诉你这个怎么用
	df = df[(df['score'] > 0) & (df['score'] <= 5)] #安全区间，动量过高过低都不好
	rank_list = list(df.index)
	if len(rank_list) == 0:
		rank_list=[] #如果全部都小于0，那么空仓或者买《国债、银华日历、黄金》避险
	return rank_list
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
# 交易
def trade(c):
	if check_is_trader_date_1(c):
		#获取动量最高的N个ETF
		target_num =c.text['买入数量']
		trader_type=c.text['交易模式']
		value=c.text['下单值']
		etf_pool=c.text['股票池'].split(',')
		target_list = get_rank(c,etf_pool)[:target_num]
		# 卖出    
		position=get_position(c,c.account,c.account_type)
		account=get_account(c,c.account,c.account_type)
		if position.shape[0]>0:
			position=position[position['持仓量']>=10]
			if position.shape[0]>0:
				hold_list=position['证券代码'].tolist()
				av_amount_dict=dict(zip(position['证券代码'],position['可用数量']))
			else:
				hold_list=[]
				av_amount_dict={}
		else:
			hold_list=[]
			av_amount_dict={}
		for stock in hold_list:
			price=get_price(c,stock)
			if stock not in target_list:
				if trader_type=='数量':
					amount=value
				elif trader_type=='金额':
					amount=value/price
					amount=adjust_amount(stock,amount)
				elif trader_type=='百分比':
					total=account['总资产']
					value=total*value
					amount=value/price
					amount=adjust_amount(stock,amount)
				else:
					amount=0
				av_amount=av_amount_dict.get(stock,0)
				if av_amount>=10:
					if av_amount>=amount:
						amount=amount
					else:
						amount=av_amount
				else:
					amount=0
				if check_is_sell(c,c.account,c.account_type,stock=stock,amount=amount) and amount>=10:
					maker='{},{},{},{},{}'.format(c.st_name,stock,'sell',amount,price)
					passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, amount, maker,1,maker,c)
					print(maker)
					#注意这个卖出了要移除持股,不然无法买入
					try:
						hold_list.remove(stock)
					except Exception as e:
						print(e,stock,'移除持股有问题******')
					#卖出等待30秒充分的等待卖单成交
					time.sleep(30)
				else:
					print(stock,'卖出不了')
			else:
				print(stock,'在动量排名继续持有')
		# 买入
		for stock in target_list:
			if stock not in hold_list:
				price=get_price(c,stock)
				if trader_type=='数量':
					amount=value
				elif trader_type=='金额':
					amount=value/price
					amount=adjust_amount(stock,amount)
				elif trader_type=='百分比':
					total=account['总资产']
					value=total*value
					amount=value/price
					amount=adjust_amount(stock,amount)
				else:
					amount=0
				if check_is_buy(c,c.account,c.account_type,stock=stock,amount=amount,price=price) and amount>=10:
					maker='{},{},{},{},{}'.format(c.st_name,stock,'buy',amount,price)
					passorder(c.buy_code, 1101,c.account, stock, c.buy_price_code, 0, amount, maker,1,maker,c)
					print(maker)
				else:
					print(stock,'买入不了')
			else:
				print(stock,'在动量排名继续持有')
	else:
		print('{} 目前不是交易时间'.format(datetime.now()))

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
	stock_list=c.text['股票池'].split(',')
	is_open=c.text['是否开启策略隔离']
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
			if is_open=='是':
				print('开启策略隔离')
				data['隔离']=data['证券代码'].apply(lambda x: '是' if x in stock_list else '不是')
				data=data[data['隔离']=='是']
			else:
				print('不开启策略隔离谨慎使用***************')
			
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
