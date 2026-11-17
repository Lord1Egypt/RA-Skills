#encoding:gbk
'''
11可转债5因子轮动策略
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
import talib
import time 
from datetime import datetime
import math
import json
import requests
import numpy as np
import json
text={
	
	"账户":"770",
	"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
	"账户类型":"STOCK",
	"策略名字":"可转债5因子轮动策略高速服务器3",
	"买入价格编码":5,
	"卖出价格编码":5,
	"是否测试":"否",
	"测试时间":'20250303',
	"黑名单":['600031.SH'],
	"是否隔离策略":"是",
	"交易模式说明":"金额/数量",
	"交易模式":"金额",
	"固定交易金额":2000,
	"固定交易数量":100,
	"账户个股止盈止损设置":"账户个股止盈止损设置安成本价计算************",
	"账户个股止盈":25,
	"账户个股止损":-8,
	"当日止盈止损设置":"当日止盈止损设置安买入价格计算当日止盈,安自己需要该",
	"当日止盈":5,
	"当日止损":-3,
	"时间设置":"时间设置********",
	"交易时间段":4,
	"交易开始时间":9,
	"交易结束时间":14,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	
	"因子设置说明": "全部因子看策略下面的全部数据，注意因子的大小，因子名称,全部的因子更多因子在合成",
	"服务器数据源设置": "服务器数据源设置********",
	"服务器": "http://124.220.32.224",
	"端口": "8023",
	"实时交易系统网页": "http:///xms_quants_bond_cov_trader_data.html",
	"数据表类型": "实时数据/全部默认因子/合成因子",
	"数据表": "实时数据",
	"是否测试": "否",
	"测试时间": "20250218",
	"可转债自定义因子计算": "可转债自定义因子计算************,基于默认因子表计算,df是因子表名称",
	"是否开启默认因子计算": "是",
	"默认因子计算": {
	"三要素评分": "df['转股溢价率']*100+df['剩余年限']-df['到期收益率(税前)']*100"
	},
	"强制赎回设置": "************************",
	"是否剔除强制赎回": "是",
	"满足强制赎回天数": 10,
	"排除上市天数": 3,
	"是否排除ST": "是",
	"排除市场": [],
	"行业说明": "查询行业表**********,混合排除不区分一二三级行业",
	"排除行业": [],
	"排除企业类型": [],
	"排除地域": [],
	"排除外部评级": [],
	"排除三方评级": [],
	"添加排除因子": "排除因子设置************************",
	"因子计算符号说明": "大于,小于,大于排名%,小于排名%,空值,排除是相反的,大于是小于",
	"排除因子": [
		"双低",
		"双低",
		"剩余市值(亿)",
		"剩余市值(亿)",
		"剩余年限",
		"转股溢价率",
		"转股溢价率",
		"最新价",
		"最新价",
		"正股年化波动率",
		"涨跌幅",
		"换手率"
	 ],
	"因子计算符号": [
		"大于",
		"小于",
		"大于",
		"小于",
		"小于",
		"大于",
		"小于",
		"大于",
		"小于",
		"小于",
		"小于",
		"小于"
	 ],
	"因子值": [
		170,
		100,
		8,
		1,
		1,
		70,
		-1,
		150,
		100,
		60,
		0,
		5
		],
	"打分因子设置": "*************************************************",
	"打分因子说明": "正相关：因子值越大得分越高；负相关：因子值越大得分越低,",
	"打分因子": [
		"溢价率"
		],
	"因子相关性": [
		"负相关"
	],
	"因子权重": [
		1
	],
	"持有限制": 10,
	"持股限制": 10,
	"策略轮动设置": "策略轮动设置************************,轮动都按排名来",
	"轮动方式说明": "每天/每周/每月/特别时间",
	"轮动方式": "每天",
	"说明": "每天按自定义函数运行",
	"每周轮动是说明": "每周比如0是星期一,4是星期五**********",
	"每周轮动时间": 0,
	"每月轮动是说明": "必须是交易日,需要自己每个月自动输入**********",
	"每月轮动时间": [
		"2024-02-29",
		"2024-02-29"
	],
	"特定时间说明": "特别的应该交易日",
	"特定时间": [
		"2024-02-23",
		"2024-02-24"
	],
	"轮动规则设置": "轮动规则设置88888888**********排名",
	"持有排名前N": 10
}
class A():
	pass
a=A()
a.log_id=[]
def init(c):
	#账户
	c.account=text['账户']
	#账户类型
	c.account_type=text['账户类型']
	#交易股票池
	hold_limit=text['持有限制']
	if c.account_type=='stock' or c.account_type=='STOCK':
		c.buy_code=23
		c.sell_code=24
	else:
		#融资融券
		c.buy_code=33
		c.sell_code=34
	c.buy_price_code=text['买入价格编码']
	c.sell_price_code=text['卖出价格编码']
	c.st_name=text['策略名字']
	c.del_trader_list=text['黑名单']
	#强制赎回
	c.redeem=''
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	#可以考虑一天轮动2次
	c.run_time("run_tarder_func","1nDay","2024-07-25 09:40:00")
	c.run_time("run_tarder_func","1nDay","2024-07-25 14:20:00")
	#300秒检查一下是不是下单成功
	c.run_time("run_check_trader_func","300nSecond","2024-07-25 13:20:00")
	#5分钟不成交撤单了在下
	#c.run_time("run_order_trader_func","300nSecond","2024-07-25 13:20:00")
	c.run_time("trader_info","3nSecond","2024-07-25 13:20:00")
	#账户个股止盈止损，安成本价计算
	c.run_time("get_account_stock_stop_trader","3nSecond","2024-07-25 13:20:00")
	#当日止盈止损,结合涨跌幅，成本价计算
	c.run_time("get_daily_stock_stop_trader","4nSecond","2024-07-25 13:20:00")
	run_tarder_func(c)
def handlebar(c):
	#run_tarder_func(c)
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
def get_price(c,stock):
	'''
	获取最新价格
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	price=tick['lastPrice']
	return price
def get_trader_data(c):
	'''
	获取因子数据
	'''
	url=text['服务器']
	port=text['端口']
	table=text['数据表']
	test=text['是否测试']
	test_date=text['测试时间']
	if test=='是':
		print('开启测试模式实盘记得关闭********************')
		date=test_date
	else:
		date=''.join(str(datetime.now())[:10].split('-'))
	#date='20250229'
	models=xms_quant_bond_user_factor_trader(
		data_type=table,
		url=url,
		port=port,
		text=text,
		date=date)
	stats,df,redeem=models.get_select_result()
	if stats==True:
		print('可转债数据获取成功，开始轮动分析')
		print('选股结果*********************')
		print(df)
		df['更新时间']=datetime.now()
		hold_limit=text['持股限制']
		buy_rank=text['持有排名前N']
		hold_stock=get_position(c,c.account,c.account_type)
		if hold_stock.shape[0]>0:
			hold_stock=hold_stock[hold_stock['持仓量']>=10]
			if hold_stock.shape[0]>0:
				hold_stock['证券代码']=hold_stock['证券代码'].astype(str)
				hold_stock_list=hold_stock['证券代码'].tolist()
				hold_amount=hold_stock.shape[0]
			else:
				hold_stock_list=[]
				hold_amount=0
		else:
			hold_stock_list=[]
			hold_amount=0
		df=df
		if df.shape[0]>0:
			df['可转债代码']=df['转债代码'].astype(str)
			df['可转债代码']=df['转债代码'].apply(lambda x:adjust_stock(x))
			all_stock_list=df['可转债代码'].tolist()
			buy_stock_list=df['可转债代码'].tolist()[:buy_rank]
		else:
			all_stock_list=[]
			buy_stock_list=[]
			#轮动卖出
		sell_stock_list=[]
		for stock  in hold_stock_list:
			if stock not in buy_stock_list:
				print('卖出 {} 不在买入前{} 排名{}'.format(stock,buy_rank,buy_stock_list))
				sell_stock_list.append(str(stock))
			else:
				print('持有 {} 在买入前{} 排名{}'.format(stock,buy_rank,buy_stock_list.index(stock)))
		#剔除强制赎回
		if redeem.shape[0]>0:
			redeem['转债代码']=redeem['转债代码'].apply(lambda x:adjust_stock(x))
			redeem_list=redeem['转债代码'].tolist()
			print('强制赎回数据**************************')
			print(redeem_list)
		else:
			redeem_list=[]
		for stock in hold_stock_list:
			if stock in redeem_list:
				print(stock,'在强制赎回里面卖出*****************')
				sell_stock_list.append(stock)
			else:
				print(stock,'不在强制赎回里面不卖出*****************')
		sell_stock_list=list(set(sell_stock_list))
		#轮动买入
		buy_stock_list_1=[]
		for stock in buy_stock_list:
			if stock in hold_stock_list:
				print('已经持有 {} 在买入前{} 排名{}'.format(stock,buy_rank,buy_stock_list.index(stock)))
			else:
				print('买入 {} 在买入前{} 排名{}'.format(stock,buy_rank,buy_stock_list.index(stock)))
				buy_stock_list_1.append(stock)
		
		sell_df=pd.DataFrame()
		sell_df['证券代码']=sell_stock_list
		sell_df['交易状态']='卖'
		sell_amount=sell_df.shape[0]
		av_buy=(hold_limit-hold_amount)+sell_amount
		if av_buy>=hold_limit:
			av_buy=hold_limit
		else:
			av_buy=av_buy
		buy_df=pd.DataFrame()
		buy_df['证券代码']=buy_stock_list_1[:av_buy]
		buy_df['交易状态']='买'
		if sell_df.shape[0]>0:
			sell_df['名称']=sell_df['证券代码']
		else:
			sell_df['名称']=None
		if buy_df.shape[0]>0:
			buy_df['证券代码']=buy_df['证券代码'].astype(str)
			buy_df['名称']=buy_df['证券代码']
		else:
			buy_df['名称']=None
		buy_df['交易时间']=datetime.now()
		if buy_df.shape[0]>0:
			buy_df['投资备注']=c.st_name+','+buy_df['证券代码']+','+'buy'
		else:
			buy_df=buy_df
		print('买入股票****************')
		print(buy_df)
		print('卖出股票*****************')
		if sell_df.shape[0]>0:
			sell_df['投资备注']=c.st_name+','+sell_df['证券代码']+','+'sell'
		else:
			sell_df=sell_df
		print(sell_df)
		if hold_stock.shape[0]>0:
			hold_stock=hold_stock[hold_stock['持仓量']>=10]
			if hold_stock.shape[0]>0:
				hold_stock['证券代码']=hold_stock['证券代码'].astype(str)
				hold_stock['卖出']=hold_stock['证券代码'].apply(lambda x: '是' if x in sell_stock_list else '不是')
				sell_df=hold_stock[hold_stock['卖出']=='是']
			else:
				sell_df=pd.DataFrame()
		else:
			sell_df=pd.DataFrame()
			
		return buy_df,sell_df
	else:
		print('可转债数据获取失败，等待服务器更新')
		buy_df=pd.DataFrame()
		sell_df=pd.DataFrame()
		return buy_df,sell_df
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
def check_is_sell(c,accountid,datatype,stock='',amount=''):
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
					print('{} 不能卖出可以数量{} 小于卖出数量{}'.format(stock,av_amount,amount))
					return False
					
			else:
				print('{} 不能卖出可以数量没有持股'.format(stock))
				return False
		else:
			print('{} 不能卖出可以数量没有持股'.format(stock))
			return False
	else:
		print('{} 不能卖出可以数量没有持股'.format(stock))
		return False
def check_is_hold_stock_limit(c,accountid,datatype,stock='600031.SH',limit_amount=100):
	'''
	检查是否到持股限制
	'''
	position=get_position(c,accountid,datatype)
	if position.shape[0]>0:
		position=position[position['证券代码']==stock]
		if position.shape[0]>0:
			hold_amount=position['持仓量'].tolist()[-1]
			if hold_amount>=limit_amount and limit_amount>=10:
				print('{} 持有数量{} 大于持股限制{} 不允许买入'.format(stock,hold_amount,limit_amount))
				return True
			else:
				print('{} 持有数量{} 小于持股限制{} 允许买入'.format(stock,hold_amount,limit_amount))
				return False
		else:
			print('{} 持有数量{} 小于持股限制{} 允许买入'.format(stock,0,limit_amount))
			return False
	else:
		print('{} 持有数量{} 小于持股限制{} 允许买入'.format(stock,0,limit_amount))
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
	trader_models=text['交易模式']
	fix_value=text['固定交易金额']
	fix_amount=text['固定交易数量']
	if check_is_trader_date_1():
		#先卖在买入
		buy_df,sell_df=get_trader_data(c)
		if sell_df.shape[0]>0:
			for stock,hold_amount,av_amount,maker in zip(sell_df['证券代码'],sell_df['持仓量'],sell_df['可用数量'],sell_df['投资备注'].tolist()):
				try:
					if maker not in a.log_id:
						price=get_price(c,stock)
						if check_is_sell(c,c.account,c.account_type,stock=stock,amount=av_amount):
							print('{} 持有数量{} 可以数量{}大于0 卖出数量{} '.format(stock,hold_amount,av_amount,av_amount,))
							passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, maker,1,maker,c)
							a.log_id.append(maker)
						else:
							print('{} 持有数量{} 可以数量{}大于0 不卖出卖出数量{} '.format(stock,hold_amount,av_amount,av_amount))
					else:
						print(maker,'在卖出id记录等待订单检查**************')
				except:
					print('{}卖出有问题'.format(maker))
		else:
			print('没有卖出的数据')
		#买入
		if buy_df.shape[0]>0:
			for stock,maker in zip(buy_df['证券代码'].tolist(),buy_df['投资备注'].tolist()):
				price=get_price(c,stock)
				if trader_models=='数量':
					amount=fix_amount
				else:
					amount=fix_value/price
					amount=adjust_amount(stock,amount)
				if maker not in a.log_id:
					if check_is_buy(c,c.account,c.account_type,stock=stock,amount=amount,price=price) and amount>=10:
						passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
						print('{} 最新价格 买入{} id{}'.format(stock,amount,maker))
						a.log_id.append(maker)
					else:
						print('{} 账户资金无法买入'.format(maker))
				else:
					print(maker,'在买入id记录等待订单检查************')
		else:
			print('没有买入数据')
	else:
		print('{} 目前不少交易时间'.format(datetime.now()))
def run_check_trader_func(c):
	'''
	检查交易下单情况，没有下单的就补单
	'''
	trader_log=get_order(c,c.account,c.account_type)
	now_date=str(datetime.now())[:10]
	#剔除撤单废单
	#这里注意看个人要不要加57废单的编号,加了废单有可能会继续下废单，检查好自己的代码在加
	not_list=[49,50,51,52]
	if trader_log.shape[0]>0:
		trader_log['撤单']=trader_log['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
		trader_log=trader_log[trader_log['撤单']=='不是']
	else:
		trader_log=trader_log
	name_list=[c.st_name]
	if trader_log.shape[0]>0:
		trader_log['策略']=trader_log['投资备注'].apply(lambda x: str(x).split(',')[0])
		trader_log['本策略']=trader_log['策略'].apply(lambda x: '是' if x in name_list else '不是')
		trader_log=trader_log[trader_log['本策略']=='是']
		if trader_log.shape[0]>0:
			maker_list=trader_log['投资备注'].tolist()
		else:
			maker_list=[]
	else:
		maker_list=[]
	#交易id记录a
	if check_is_jhjj()==False:
		if len(a.log_id)>0:
			for maker in a.log_id:
				if maker not in maker_list:
					a.log_id.remove(maker)
					print('{} id记录没有委托重新委托*******************************'.format(maker))
				else:
					print('{} id记录已经委托不委托*******************************'.format(maker))
		else:
			print('交易检查没有id记录数据*******************************')
	else:
		print('交易检查没有id记录数据 集合竞价时间不分析')
def run_order_trader_func(c):
	'''
	下单不成交撤单在下单
	'''
	if check_is_trader_date_1():
		print('********************下单不成交撤单在下单******************')
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
			
			if trader_log.shape[0]>0:
				for stock,amount,trader_type,maker,oder_id,name in zip(trader_log['证券代码'].tolist(),trader_log['未成交数量'].tolist(),
						trader_log['买卖方向'].tolist(),trader_log['投资备注'].tolist(),trader_log['订单编号'].tolist(),trader_log['策略'].tolist()):
					price=get_price(c,stock)
					#未成交卖出
					print('证券代码：{} 未成交数量{}交易类型{} 投资备注{} 订单id{}'.format(stock,amount,trader_type,maker,oder_id))
					if trader_type==49:
						cancel(oder_id, c.account, c.account_type, c)
						#先检查是否撤单成功
						check_trader=get_order(c,c.account,c.account_type)
						
						#撤单代码
						not_list=[54]
						#成交代码
						order_list=[55,56]
						if check_trader.shape[0]>0:
							check_trader['撤单']=check_trader['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
							check_trader['成交']=check_trader['委托状态'].apply(lambda x: '是' if x in order_list else '不是')
							cacal_df=check_trader[check_trader['撤单']=='是']
							trader_df=check_trader[check_trader['成交']=='是']
							
							if cacal_df.shape[0]>0:
								cacal_maker_list=cacal_df['投资备注'].tolist()
							else:
								cacal_maker_list=[]
							if trader_df.shape[0]>0:
								trader_maker_list=trader_df['投资备注'].tolist()
							else:
								trader_maker_list=[]
						else:
							cacal_maker_list=[]
							trader_maker_list=[]
						if maker in cacal_maker_list and maker not in trader_maker_list:
							if check_is_sell(c,c.account,c.account_type,stock=stock,amount=amount):
								passorder(c.sell_code, 1101, c.account, str(stock), c.sell_price_code, 0, int(amount), str(maker),1,str(maker),c)
								print('组合{} 撤单重新卖出标的{} 数量{} 价格{}'.format(name,stock,amount,price))
							else:
								print('组合{} 撤单不能卖出标的{} 数量{} 价格{}'.format(name,stock,amount,price))
						else:
							print(maker,'没有撤单成功不委托/已经成交')
					elif trader_type==48:
						cancel(oder_id, c.account, c.account_type, c)
						#先检查是否撤单成功
						check_trader=get_order(c,c.account,c.account_type)
						#撤单代码
						not_list=[54]
						#成交代码
						order_list=[55,56]
						if check_trader.shape[0]>0:
							check_trader['撤单']=check_trader['委托状态'].apply(lambda x: '是' if x in not_list else '不是')
							check_trader['成交']=check_trader['委托状态'].apply(lambda x: '是' if x in order_list else '不是')
							cacal_df=check_trader[check_trader['撤单']=='是']
							trader_df=check_trader[check_trader['成交']=='是']
							
							if cacal_df.shape[0]>0:
								cacal_maker_list=cacal_df['投资备注'].tolist()
							else:
								cacal_maker_list=[]
							if trader_df.shape[0]>0:
								trader_maker_list=trader_df['投资备注'].tolist()
							else:
								trader_maker_list=[]
						else:
							cacal_maker_list=[]
							trader_maker_list=[]
						if maker in cacal_maker_list and maker not in trader_maker_list:
							if check_is_buy(c,c.account,c.account_type,stock=stock ,
									amount=amount,price=price):
								
								passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, int(amount), str(maker),1,str(maker),c)
								print('组合{} 撤单重新买入标的{} 数量{} 价格{}'.format(name,stock,amount,price))
							else:
								print('组合{} 撤单重新买入标的{} 数量{} 价格{} 不能买入资金不足'.format(name,stock,amount,price))
						else:
							print(maker,'没有撤单成功不委托/已经成交')
					else:
						print('组合{} 撤单重新交易未知的交易类型'.format(name))
			else:
				print('撤单了在下单组合没有委托数据')
		else:
			print('撤单了重新下单没有委托数据')
	else:
		print(datetime.now(),'下单不成交撤单在下单不是交易时间')
def check_is_up_limit(c,stock):
	'''
	检查是否是涨停
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	askPrice=sum(tick['askPrice'])
	if askPrice==0:
		return True
	else:
		return False
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
			data['股票类型']=data['证券代码'].apply(lambda x:select_data_type(x))
			print('持股只选择可转债交易**********')
			data=data[data['股票类型']=='bond']
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
def select_data_type(stock):
	'''
	选择数据类型
	'''
	stock=str(stock)[:6]
	if stock[:3] in ['110','113','128','127','123','117'] or stock[:2] in ['11','12']:
		return 'bond'
	elif stock[:3] in ['502','501'] or stock[:2] in ['16','15','51','50','56','58'] or stock[:1] in ['5']:
		return 'fund'
	else:
		return 'stock'
def adjust_stock(stock='600031.SH'):
	'''
	调整代码
	'''
	if stock[-2:]=='SH' or stock[-2:]=='SZ' or stock[-2:]=='sh' or stock[-2:]=='sz':
		stock=stock.upper()
	else:
		if stock[:3] in ['600','601','603','605','688','689',
			 ] or stock[:2] in ['11','51','58']:
			stock=stock+'.SH'
		else:
			stock=stock+'.SZ'
	return stock
class xms_quant_bond_user_factor_trader:
    def __init__(self,
                data_type='实时数据',
                url='http://124.220.32.224/',
                port='8023',
                text={},
                date='20250114'
                ):
        '''
        西蒙斯可转债量化交易系统3.0
        作者:西蒙斯量化
        微信:xg_quant
        '''
        print('西蒙斯可转债量化交易系统3.0')
        print('作者:西蒙斯量化,微信:xg_quant')
        self.data_type=data_type
        self.url=url
        self.port=port
        self.text=text
        self.date=date
        self.stats=False
        self.redeem=pd.DataFrame()
    def get_spot_data(self,date='20250711'):
        '''
        获取实时数据表
        '''
        try:
            url='{}:{}/data/实时数据/{}.json?t=1752251108452'.format(self.url,self.port,date)
            res=requests.get(url=url)
            res=res.json()
            df=pd.DataFrame(res)
        except Exception as e:
            print(e,'获取实时数据表有问题')
            df=pd.DataFrame()
        return df
    def get_all_mr_factor_data(self,date='20250711'):
        '''
        获取全部默认因子表
        '''
        try:
            url='{}:{}/data/全部默认因子/{}.json?t=1752251108452'.format(self.url,self.port,date)
            res=requests.get(url=url)
            res=res.json()
            df=pd.DataFrame(res)
        except Exception as e:
            print(e,'全部默认因子有问题')
            df=pd.DataFrame()
        return df
    def get_all_connect_factor_data(self,date='20250711'):
        '''
        获取合成因子表
        '''
        try:
            url='{}:{}/data/合成因子/{}.json?t=1752251108452'.format(self.url,self.port,date)
            res=requests.get(url=url)
            res=res.json()
            df=pd.DataFrame(res)
        except Exception as e:
            print(e,'合成因子有问题')
            df=pd.DataFrame()
        return df
    def select_bond_cov(self,x):
        '''
        选择证券代码
        '''
        if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
            return '是'
        else:
            return '不是'
    def get_shift_data(self,n=1):
        '''
        获取前n天的日期
        '''
        date_str =self.date
        date_obj = pd.to_datetime(date_str, format="%Y%m%d")  # 转换为 pandas Timestamp
        new_date_obj = date_obj - pd.Timedelta(days=n)        # 减少一天
        new_date_str = new_date_obj.strftime("%Y%m%d")        # 转换回字符串
        return new_date_str
    def get_all_factor_data(self):
        '''
        获取可转债全部数据
        '''
        print("获取可转债全部数据************")
        text=self.text
        now_date=self.date
        if self.data_type=='实时数据':
            df=self.get_spot_data(date=now_date)
        elif self.data_type=='全部默认因子':
            df=self.get_all_mr_factor_data(date=now_date)
        elif self.data_type=='合成因子':
            df=self.get_all_connect_factor_data(date=now_date)
        else:
            df=self.get_spot_data(date=now_date)
        if df.shape[0]<=0:
            print(now_date,'获取数据有问题获取前一个交易日数据')
            now_date=self.get_shift_data(n=1)
            print(now_date)
            if self.data_type=='实时数据':
                df=self.get_spot_data(date=now_date)
            elif self.data_type=='全部默认因子':
                df=self.get_all_mr_factor_data(date=now_date)
            elif self.data_type=='合成因子':
                df=self.get_all_connect_factor_data(date=now_date)
            else:
                df=self.get_spot_data(date=now_date)
        else:
            df=df
        if df.shape[0]>0:
            self.stats=True
        else:
            df=pd.DataFrame()
            self.stats=False
        return df
    def get_cacal_factor_base_table(self):
        '''
        计算默认因子
        '''
        print('计算默认因子***********************')
        text=self.text
        is_open=text['是否开启默认因子计算']
        df=self.get_all_factor_data()
        if df.shape[0]>0:
            factor=text['默认因子计算']
            if is_open=='是':
                print('开启计算默认因子***********************')
                factor_name=list(factor.keys())
                if len(factor_name)>0:
                    for name in factor_name:
                        try:
                            print(name,'因子计算完成')
                            func=factor[name]
                            df[name]=func)
                        except Exception as e:
                            print(e,name,'因子计算有问题')
                else:
                    print('没有默认因子需要计算')
            else:
                print('不开启计算默认因子***********************')
        else:
            df=pd.DataFrame()
        return df
    def get_del_qzsh_data(self):
        '''
        剔除强制赎回
        '''
        print('剔除强制赎回')
        text=self.text
        del_select=text['是否剔除强制赎回']
        n=text['满足强制赎回天数']
        df=self.get_cacal_factor_base_table()
        select_list=['强赎登记日','已公告要强赎']
        try:
            if df.shape[0]>0:
                df['强赎']=df['转债提示'].apply(lambda x: '是' if '强赎登记日' in str(x) or '已公告要强赎' in str(x) else '不是')
                df1=df[df['强赎']=='是']
                df2=df[df['强赎']=='不是']
            else:
                df1=pd.DataFrame()
                df=pd.DataFrame()
        except Exception as e:
            print(e,'剔除强制赎回')
            df1=pd.DataFrame()
            df2=df
        self.redeem=df1
        return df2
    def get_n1_n2_daily(self,start_date: str = '2023-12-14') -> int:

        """计算两个日期之间的天数差"""
        end_date=str(datetime.now())[:10]
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return (end - start).days
    def days_excluded_from_market(self):
        '''
        排除上市天数
        '''
        print('排除上市天数')
        text=self.text
        df=self.get_del_qzsh_data()
        try:
            if df.shape[0]>0:
                n=text['排除上市天数']
                df['上市日期']=pd.to_datetime(df['上市日期'],unit='ms')
                df['上市日期']=df['上市日期'].astype(str)
                df['上市天数']=df['上市日期'].apply(lambda x: self.get_n1_n2_daily(str(x)))
                df=df[df['上市天数']>=n]
            else:
                df=df
    
        except Exception as e:
            print(e,'排除上市天数')
            df=df
        return df
    def st_exclusion(self):
        '''
        排除st
        '''
        print('排除st')
        text=self.text
        is_del=text['是否排除ST']
        df=self.days_excluded_from_market()
        try:
            if df.shape[0]>0:
                if is_del=='是':
                    def_list=['ST','st','*ST','*st']
                    df['ST']=df['正股名称'].apply(lambda x: '是' if 'st' in x or 'ST' in x or '*st' in x or '*ST' in x else '不是' )
                    df=df[df['ST']=='不是']
                else:
                    df=df
        except Exception as e:
            print(e,'排除st')
            df=df
        
        return df
    def exclusion_of_market(self):
        '''
        排除市场
        '''
        print("排除市场")
        text=self.text
        exclusion_market_list = []
        del_stock_list=text['排除市场']
        for exclusion_market in del_stock_list:
            if exclusion_market == '沪市主板':
                exclusion_market_list.append(['110','113'])
            elif exclusion_market == '深市主板':
                exclusion_market_list.append(['127','128'])
            elif exclusion_market == '创业板':
                exclusion_market_list.append('123')
            elif exclusion_market == '科创板':
                exclusion_market_list.append('118')
            else:
                pass
        df=self.st_exclusion()
        try:
            if df.shape[0]>0:
                df['market'] = df['转债代码'].apply(lambda x: '排除' if str(x)[:3] in exclusion_market_list  else '不排除')
                df = df[df['market'] == '不排除']
            else:
                df=df
        except Exception as e:
            print(e,'排除市场') 
            df=df
        return df
    def excluded_industry(self):
        '''
        排除行业
        '''
        print('排除行业')
        text=self.text
        del_list=text['排除行业']
        df=self.exclusion_of_market()
        try:
            if df.shape[0]>0:
                industry_list=[]
                data=pd.DataFrame()
                industry_1=df['一级行业'].tolist()
                for i in industry_1:
                    industry_list.append(i)
                industry_2=df['二级行业'].tolist()
                for i in industry_2:
                    industry_list.append(i)
                industry_3=df['三级行业'].tolist()
                for i in industry_3:
                    industry_list.append(i)
                industry_list=list(set(industry_list))
                data['可转债行业']=industry_list
                industry_name=['一级行业','二级行业','三级行业']
                for name in industry_name:
                    df['行业排除']=df[name].apply(lambda x: '是' if x in del_list else '不是')
                    df=df[df['行业排除']=='不是']
            else:
                df=df
        except Exception as e:
            print(e,'排除行业')
            df=df
        
        return df
    def exclusion_of_enterprise(self):
        '''
        排除企业
        '''
        print('排除企业')
        text=self.text
        df=self.excluded_industry()
        return df
    def exclusion_area(self):
        '''
        排除地域
        '''
        print('排除地域')
        text=self.text
        df=self.exclusion_of_enterprise()
        try:
            if df.shape[0]>0:
                del_list=text['排除地域']
                df['排除地域']=df['地域'].apply(lambda x:'是' if str(x) in del_list else '不是')
                df=df[df['排除地域']=='不是']
            else:
                df=df
        except Exception as e :
            print(e,'排除地域')
            df=df
        return df
    def exclusion_of_external_rating(self):
        '''
        排除外部评级
        '''
        print('排除外部评级')
        text=self.text
        df=self.exclusion_area()
        try:
            if df.shape[0]>0:
                del_list=text['排除外部评级']
                df['排除外部评级']=df['主体评级'].apply(lambda x:'是' if str(x) in del_list else '不是')
                df=df[df['排除外部评级']=='不是']
            else:
                df=df
        except Exception as e:
            print(e,'排除外部评级')
        return df
    def tripartite_exclusion(self):
        '''
        排除三方评级
        '''
        print('排除三方评级')
        text=self.text
        df=self.exclusion_of_external_rating()
        try:
            if df.shape[0]>0:
                del_list=text['排除三方评级']
                df['排除三方评级']=df['主体评级'].apply(lambda x:'是' if str(x) in del_list else '不是')
                df=df[df['排除三方评级']=='不是']
            else:
                df=df
        except Exception as e:
            print(e,'排除三方评级')
            df=df
        return df
    def cacal_exclusion_factor(self):
        '''
        计算排除因子
        '''
        print('计算排除因子')
        text=self.text
        df=self.tripartite_exclusion()
        df.to_excel(r'数据.xlsx')
        if df.shape[0]>0:
            factor_list=text['排除因子']
            factor_func_list=text['因子计算符号']
            factor_value_list=text['因子值']
            all_factor_list=df.columns.tolist()
            for factor,func,value in zip(factor_list,factor_func_list,factor_value_list):
                try:
                    if factor in all_factor_list:
                        df[factor]=pd.to_numeric(df[factor])
                        if func=='大于':
                            df=df[df[factor]<=value]
                        elif func=='小于':
                            df=df[df[factor]>=value]
                        elif func=='大于排名%':
                            df=df.sort_values(by=factor,ascending=True)[value:]
                        elif func=='小于排名%':
                            df=df.sort_values(by=factor,ascending=True)[:value]
                        elif func=='空值':
                            df=df
                        else:
                            print('{}未知的计算方式'.format(func))
                       
                    else:
                        print('{}排除因子不在全部的因子表里面全部因子表{}'.format(factor,all_factor_list))
                except Exception as e:
                    print(factor,e,'排除因子计算有问题')
        else:
            df=pd.DataFrame()
        return df
    def cacal_score_factor(self):
        '''
        计算打分因子
        升序从小到大
        降序从大到小
        '''
        print("计算打分因子")
        text=self.text
        df=self.cacal_exclusion_factor()
        if df.shape[0]>0:
            factor_list=text['打分因子']
            factor_cov_list=text['因子相关性']
            factor_weight_list=text['因子权重']
            all_factor_list=df.columns.tolist()
            score_list=[]
            for factor,cov,weight in zip(factor_list,factor_cov_list,factor_weight_list):
                try:
                    if factor in all_factor_list:
                        if cov=='正相关':
                            df[factor]=df[factor]*1
                        elif cov=='负相关':
                            df[factor]=df[factor]*-1
                        else:
                            print('{}未知的相关性'.format(cov))
                        df['{}_得分'.format(factor)]=df[factor].rank(ascending=False)*weight
                        score_list.append('{}_得分'.format(factor))
                    else:
                        print('{}打分因子不在全部的因子表里面全部因子表{}'.format(factor,all_factor_list))
                except Exception as e:
                    print(factor,e,'排除因子打分有问题')
            df['总分']=df[score_list].sum(axis=1).tolist()
            df['排名']=df['总分'].rank( ascending=True)
            df=df.sort_values(by='总分',ascending=True)
        else:
            df=pd.DataFrame()
        return df
    def get_time_rotation(self):
        '''
        轮动方式
        '''
        text=self.text
        now_date=''.join(str(datetime.now())[:10].split('-'))
        now_time=time.localtime()                               
        trader_type=text['轮动方式']                               
        trader_wday=text['每周轮动时间']                               
        moth_trader_time=text['每月轮动时间']
        specific_time=text['特定时间']
        year=now_time.tm_year
        moth=now_time.tm_mon
        wday=now_time.tm_wday
        daily=now_time.tm_mday
        if trader_type=='每天':
            print('轮动方式每天********************************')
            return True
        elif trader_type=='每周':
            if trader_wday==wday:
                return True
            elif trader_wday<wday:
                print('安周轮动 目前星期{} 轮动时间星期{} 目前时间大于轮动时间不轮动'.format(wday+1,trader_wday+1))
                return False
            else:
                print('安周轮动 目前星期{} 轮动时间星期{} 目前时间小于轮动时间不轮动'.format(wday+1,trader_wday+1))
                return False
        elif trader_type=='每月轮动时间':
            stats=''
            for date in moth_trader_time:
                data=''.join(data.split('-'))
                if int(moth_trader_time)==int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间等于轮动时间轮动'.format(now_date,date))
                    stats=True
                    break
                elif int(moth_trader_time)<int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间小于轮动时间轮动'.format(now_date,date))
                    stats=False
                else:
                    print('安月轮动 目前{} 轮动时间{} 目前时间大于轮动时间轮动'.format(now_date,date))
                    stats=False
            return stats
        else:
            #特别时间
            stats=''
            for date in specific_time:
                data=''.join(data.split('-'))
                if int(specific_time)==int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间等于轮动时间轮动'.format(now_date,date))
                    stats=True
                    break
                elif int(specific_time)<int(date):
                    print('安月轮动 目前{} 轮动时间{} 目前时间小于轮动时间轮动'.format(now_date,date))
                    stats=False
                else:
                    print('安月轮动 目前{} 轮动时间{} 目前时间大于轮动时间轮动'.format(now_date,date))
                    stats=False
            return stats  
    def get_select_result(self):
        '''
        获取选股结果
        '''
        if self.get_time_rotation():
            text=self.text
            select_columns=['转债名称',"转债代码"]
            del_factor=list(set(text['排除因子']))
            score_factor=text['打分因子']
            score_type=text['因子相关性']
            for fcator in del_factor:
                select_columns.append(fcator)
            for fcator in score_factor:
                select_columns.append(fcator)  
            df=self.cacal_score_factor()
            all_columns=df.columns.tolist()
            select_facto=[]
            for columns in select_columns:
                if columns in all_columns:
                    select_facto.append(columns)
            select_facto.append('总分')
            select_facto.append('排名')
            if df.shape[0]>0:
                df=df[select_facto]
                all_columns=df.columns.tolist()
                for factor,cacal_type in zip(score_factor,score_type):
                    if factor in all_columns:
                        if cacal_type=='负相关':
                            df[factor]=df[factor]*-1
                        else:
                            pass
                    else:
                        pass
                df.index=range(0,df.shape[0])
                df=df.drop_duplicates(subset=['转债代码'],keep='last')
            else:
                df=pd.DataFrame()
            stats=self.stats
        else:
            self.stats=False
            df=pd.DataFrame()
        return stats,df,self.redeem
    