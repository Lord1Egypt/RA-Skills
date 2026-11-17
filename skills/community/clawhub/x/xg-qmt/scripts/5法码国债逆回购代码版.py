#encoding:gbk
'''
5小果国债逆回购代码版
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
'''
import pandas as pd
import numpy as np
import talib
import math 
from datetime import datetime
def init(c):
	c.text={
		"策略名称":"小果国债逆回购代码版",
		"标记":"作者小果量化",
		"账户":"55001947",
		"账户类型":"STOCK",
		"会员账户设置":"账户密码量化网页注册就可以",
		"会员账户":"test",
		"会员密码":"test",
		"会员授权码":"test",
		"授权码":"",
		"购买标的":"131810.SZ",
		"购买比例":1,
		"购买时间":"15:01",
		"卖出价格编码":6,
		"交易时间段":4,
		"交易开始时间":9,
		"交易结束时间":15,
		"是否参加集合竞价":"是",
		"开始交易分钟":0,
	}
	#账户
	c.account=c.text['账户']
	#账户类型
	c.account_type=c.text['账户类型']
	if c.account_type=='stock' or c.account_type=='STOCK':
		c.buy_code=23
		c.sell_code=24
	else:
		#融资融券
		c.buy_code=33
		c.sell_code=34
	c.sell_price_code=c.text['卖出价格编码']
	c.sell_stock=c.text['购买标的']
	c.sell_ratio=c.text['购买比例']
	c.st_name=c.text['策略名称']
	c.date=c.text['购买时间']
	c.hy_username=c.text['会员账户']
	c.hy_password=c.text['会员密码']
	c.hy_invite_code=c.text['会员授权码']
	print(balance(c))
	if (c,
		username=c.hy_username,
		password=c.hy_password,
		invite_code=c.hy_invite_code):
		print('等待逆回购逆回购时间{} 逆回购标的{} 逆回购比例{}******************'.format(c.date,c.sell_stock,c.sell_ratio))	
		c.run_time("reverse_repurchase_of_treasury_bonds_1","1nDay","2024-07-25 {}:00".format(c.date))  
	else:
		pass
def adjust_stock(stock='600031.SH'):
	'''
	调整代码
	'''
	if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
		stock=stock.upper()
	else:
		if stock[:3] in ['600','601','603','688','510','511',
			'512','513','515','113','110','118','501'] or stock[:2] in ['11']:
			stock=stock+'.SH'
		else:
			stock=stock+'.SZ'
		return stock
def adjust_amount(stock='',amount=''):
	'''
	调整数量
	'''           
	if stock[:3] in ['110','113','123','127','128','111'] or stock[:2] in ['11','12']:
		amount=math.floor(amount/10)*10
	else:
		amount=math.floor(amount/100)*100
		return amount
def balance(c):
		'''
		对接同花顺
		'''
		try:
			accounts = get_trade_detail_data(c.account, c.account_type, 'account')
		except:
			accounts=accounts
		df=pd.DataFrame()
		for dt in accounts:
			df['账号类型']=[dt.m_nBrokerType]
			df['资金账户']=[dt.m_strAccountID]
			df['可用金额']=[dt.m_dAvailable]
			#df['冻结金额']=[dt.frozen_cash]
			df['持仓市值']=[dt.m_dInstrumentValue]
			df['总资产']=[dt.m_dBalance]
		return df
def get_spot_data(c,stock='600031.SH'):
	'''
	获取最新价格
	'''
	df=c.get_full_tick([stock])
	price=df[stock]['lastPrice']
	return price
def sell(c,stock='159985.SZ',amount=100,price=2.045):
	'''
	自定义卖出函数
	stock,股票
	amount,数量
	price价格
	'''
	account=c.account
	maker=c.st_name
	passorder(c.sell_code, 1101, c.account, str(stock), c.sell_price_code, 0, amount, maker,1,maker,c)
def reverse_repurchase_of_treasury_bonds_1(c,):
	'''
	国债逆回购
	购买比例buy_ratio
	'''
	if check_is_trader_date_1(c):
		# 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
		account=balance(c)
		av_cash=account['可用金额'].tolist()[-1]
		av_cash=float(av_cash)
		av_cash=av_cash*c.sell_ratio
		#stock_code_sh = '204001.SH'
		#统一用深圳
		stock=c.sell_stock
		price= get_spot_data(c,stock)
		print('逆回购标的',stock,'价格',price)
		#下单的数量要是1000
		amount = int(av_cash/1000)*10
		#sell
		print('开始逆回购***********')
		if amount>0:
			sell(c,stock=stock,amount=amount,price=price)
			text='国债逆回购交易类型 代码{} 价格{} 数量{}'.format(stock,price,amount)
			return '交易成功',text
		else:
			text='国债逆回购卖出 标的{} 价格{} 委托数量{}小于0有问题'.format(stock,price,amount)
			print('账户没有可以的钱@@@@@@@@@@@@@@@@@@@')
			return '交易失败',text
	else:
		print(datetime.now(),'逆回购目前不是交易时间')
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