#encoding:gbk
'''
3索普量化日线T0交易策略
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
修改账户参数就可以改成自己的
"账户":"222",
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
	"授权码":"",
	"策略名称":"索普量化日线T0交易策略",
	"账户类型":"STOCK",
	"账户":"77",
	"账户类型":"STOCK",
	"是否时间测试":"否",
	"测试时间":"20250912",
	"买入价格编码":4,
	"卖出价格编码":6,
	"是否隔离策略":"否",
	
	"是否建立底仓":"否",
	"底仓金额":200,
	
	"是否尾盘恢复仓位":"否",
	"恢复模式说明":"目标金额/交易差额",
	"恢复模式":"目标金额",
	"尾盘目标仓位金额":200,
	
	"交易记录":'C:/Users/lxg123456/Desktop/索普量化日线T0交策略.xlsx',
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
	
	"起点":-3,
	"ATR周期":14,
	"ATR倍数":0.5,
	"算法模型":{
		"索普ATR日线固定网格":{
			"函数名称":"conditional_single_time_sharing_grid(name='索普ATR日线固定网格')",
			"是否开启":"是",
			"资金模型":"金额",
			"卖出值":400,
			"买入值":400,
			"持有值":1000,
			"保留底仓":0,
			"是否生成买入虚拟单子":"否",
			"是否生成卖出虚拟单子":"否"
			},
		"索普ATR日线对称网格":{
			"函数名称":"symmetric_grid_trading(name='索普ATR日线对称网格')",
			"是否开启":"否",
			"资金模型":"金额",
			"卖出值":200,
			"买入值":200,
			"持有值":600,
			"保留底仓":0,
			"是否生成买入虚拟单子":"是",
			"是否生成卖出虚拟单子":"否"
			}
	},
	
	"时间设置":"时间设置********",
	"交易时间段":8,
	"交易开始时间":9,
	"交易结束时间":24,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	
	
	
}
#记录交易数据
class A:
	pass
a=A()
def init(c):
	c.text=text
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
	c.st_name=text['策略名称']
	c.stock_name_dict=dict(zip(a.trade_code_list,a.trade_code_name))
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	#3秒一次
	c.run_time("run_tarder_func","3nSecond","2024-07-25 13:20:00")
	#点单检查
	c.run_time("run_next_trader_func","30nSecond","2024-07-25 13:20:00")
	#检测文件是不是存在
	check_trader_log_file(c)
	#建立底仓
	c.run_time("creat_base_position","1nDay","2024-07-25 09:45:00")
	#尾盘恢复仓位
	c.run_time("get_recover_position","1nDay","2024-07-25 14:50:00")
	
def handlebar(c):
	#run_tarder_func(c)
	pass
def check_stop_trader(c,stock='002185.SZ'):
	'''
	检查停牌
	'''
	tick=c.get_full_tick(stock_code=[stock])
	tick=tick[stock]
	open=tick['open']
	high=tick['high']
	low=tick['low']
	amount=tick['amount']
	openint=tick['openInt']
	if amount==0 and open==0 and high==0 and openint==1:
		return True
	else:
		return False
def run_next_trader_func(c):
	'''
	检测补单函数
	'''
	if check_is_trader_date_1(c):
		select=['证券代码','模块名称','交易日','触发时间','交易类型','交易数量','触发价格','投资备注','交易状态']
		log=pd.read_excel(r'{}'.format(c.path))
		now_date=str(datetime.now())[:10]
		if log.shape[0]>0:
			log=log[select]
			log['交易日']=pd.to_datetime(log['交易日'])
			now_log=log[log['交易日']==now_date]
			pre_log=log[log['交易日']<now_date]
			if now_log.shape[0]>0:
				trader_log=get_order(c,c.account,c.account_type)
				now_dat=str(datetime.now())[:10]
				if trader_log.shape[0]>0:
					user_def_models=text['算法模型']
					name_list=list(user_def_models.keys())
					trader_log['策略']=trader_log['投资备注'].apply(lambda x: str(x).split(',')[0])
					trader_log['本策略']=trader_log['策略'].apply(lambda x: '是' if x in name_list else '不是')
					trader_log=trader_log[trader_log['本策略']=='是']
					if trader_log.shape[0]>0:
						maker_list=trader_log['投资备注'].tolist()
					else:
						maker_list=[]
				else:
					maker_list=[]
				now_log['下单']=now_log['投资备注'].apply(lambda x: '是' if x in maker_list else '不是')
				not_log=now_log[now_log['下单']=='不是']
				now_log=now_log[now_log['下单']=='是']
				print('订单检查重新下单的数据没有委托***********')
				print(not_log)
				print('单检查已经下单的订单**********************')
				print(now_log)
				if not_log.shape[0]>0:
					for stock,trader_type,amount,maker in zip(not_log['证券代码'],
							not_log['交易类型'],not_log['交易数量'],not_log['投资备注']):
						try:
						
							price=get_price(c,stock)
							amount=int(amount)
							if trader_type=='buy' and amount>=10:
								if check_is_buy(c,c.account,c.account_type,stock=stock,amount=amount,price=price):
									passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
									print("订单检查补单 买入{} 数量{} 价格{}".format(stock,amount,price))
								else:
									print("订单检查补单 买入{} 资金不足".format(stock))
							elif trader_type=='sell' and amount>=10:
								if check_is_sell(c,c.account,c.account_type,stock=stock,amount=amount):
									passorder(c.sell_code, 1101, c.account, str(stock), c.sell_price_code, 0, amount, maker,1,maker,c)
									print("订单检查补单 卖出{} 数量{} 价格{}".format(stock,amount,price))
								else:
									print('订单检查补单{} 不能卖出可能数量不足'.format(stock))
							else:
								print(stock,'不是交易类型')
						except Exception as e:
							print(e,stock,'订单检查补单有问题')
				else:
					print('订单检查补单没有符合需要的数据*************')
			else:
				print('今天没有委托检查数据')
		else:
			print('历史记录为空')
	else:
		print('委托检查目前不是交易时间*****')
	

def creat_base_position(c,):
	'''
	建立底仓
	'''
	if check_is_trader_date_1(c):
		is_open=c.text['是否建立底仓']
		base_value=c.text['底仓金额']
		trader_stock=c.text['监测股票池']
		if is_open=='是':
			if trader_stock=='自定义':
				df=pd.DataFrame()
				df['证券代码']=c.text['自定义股票池']
				df['名称']=c.text['自定义股票池名称']
				position=get_position(c,c.account,c.account_type)
				if position.shape[0]>0:
					hold_amount_dict=dict(zip(position['证券代码'].tolist(),position['持仓量'].tolist()))
				else:
					hold_amount_dict={}
				if df.shape[0]>0:
					df['持仓量']=df['证券代码'].apply(lambda x: hold_amount_dict.get(x,0))
					df['最新价']=df['证券代码'].apply(lambda x: get_price(c,x))
					df['持有市值']=df['持仓量']*df['最新价']
				else:
					df=pd.DataFrame()
			else:
				df=get_position(c,c.account,c.account_type)
				df['最新价']=df['证券代码'].apply(lambda x: get_price(c,x))
				df['持有市值']=df['持仓量']*df['最新价']
			if df.shape[0]>0:
				df['买入市值']=base_value-df['持有市值']
				print('建立底仓分析**************')
				print(df)
				for stock,value in zip(df['证券代码'].tolist(),df['买入市值'].tolist()):
					if value>0:
						price=get_price(c,stock)
						amount=value/price
						amount=adjust_amount(c,stock=stock,amount=amount)
						if amount>=10:
							maker='{},{},{},{}'.format(c.st_name,'建立底仓',stock,amount)
							if check_stop_trader(c,stock):
								print(stock,'停牌不交易')
							else:
								if check_is_buy(c,c.account,c.account_type,stock=stock,amount=amount,price=price):
									passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
									print("建立底仓 买入{} 数量{} 价格{}".format(stock,amount,price))
								else:
									print("建立底仓失败不 买入{} 资金不足".format(stock))
						else:
							print("建立底仓失败不买入{} 低于最低交易单位".format(stock))
					else:
						print("建立底仓失败不买入{} 已经有持股".format(stock))
			else:
				print('建立底仓没有持股')
		else:
			print('不开启建立底仓*********')
	else:
		
		
		print(datetime.now(),'建立底仓目前不是交易时间')
def get_buy_sell_amount(c,stock='513100.SH'):
	'''
	获取当天交易的买卖差额
	'''
	order=get_order(c,c.account,c.account_type)
	#print(order)
	user_def_models=text['算法模型']
	name_list=list(user_def_models.keys())
	if order.shape[0]>0:
		order['本策略']=order['投资备注'].apply(lambda x: str(x).split(',')[0])
		#这里只选择完全成交的部分处理	
		id_list=[56]
		order['成交']=order['委托状态'].apply(lambda x: '是' if x in id_list else '不是')
		order=order[order['本策略']=='是']
		order=order[order['证券代码']==stock]
		order=order[order['成交']=='是']
		if order.shape[0]>0:
			buy_order=order[order['买卖方向']==48]
			sell_order=order[order['买卖方向']==49]
			if buy_order.shape[0]>0:
				buy_amount=buy_order['成交数量'].sum()
			else:
				buy_amount=0
			if sell_order.shape[0]>0:
				sell_amount=sell_order['成交数量'].sum()
			else:
				sell_amount=0
			amount=sell_amount-buy_amount
			amount=adjust_amount(c,stock,amount)
			if amount>=10:
				print('{} 买入{} 今天卖出{} 今天买入{} '.format(stock,amount,sell_amount,buy_amount))
				return amount
			else:
				print('{} 买入低于最低数量'.format(stock))
				return 0
		else:
			print('本策略{} 没有需要补的'.format(stock))
			return 0
	else:
		print('没有委托数据')
		return 0
def get_recover_position(c):
	'''
	尾盘恢复仓位
	'''
	if check_is_trader_date_1(c):
		is_open=c.text['是否尾盘恢复仓位']
		base_value=c.text['尾盘目标仓位金额']
		trader_stock=c.text['监测股票池']
		hf_type=c.text['恢复模式']
		if is_open=='是':
			if trader_stock=='自定义':
				df=pd.DataFrame()
				df['证券代码']=c.text['自定义股票池']
				df['名称']=c.text['自定义股票池名称']
				position=get_position(c,c.account,c.account_type)
				if position.shape[0]>0:
					hold_amount_dict=dict(zip(position['证券代码'].tolist(),position['持仓量'].tolist()))
				else:
					hold_amount_dict={}
				if df.shape[0]>0:
					df['持仓量']=df['证券代码'].apply(lambda x: hold_amount_dict.get(x,0))
					df['最新价']=df['证券代码'].apply(lambda x: get_price(c,x))
					df['持有市值']=df['持仓量']*df['最新价']
				else:
					df=pd.DataFrame()
			else:
				df=get_position(c,c.account,c.account_type)
				df['最新价']=df['证券代码'].apply(lambda x: get_price(c,x))
				df['持有市值']=df['持仓量']*df['最新价']
			if df.shape[0]>0:
				if hf_type=='目标金额':
					df['买入市值']=base_value-df['持有市值']
					print('尾盘恢复仓位分析****************')
					print(df)
					for stock,value in zip(df['证券代码'].tolist(),df['买入市值'].tolist()):
						if value>0:
							price=get_price(c,stock)
							amount=value/price
							amount=adjust_amount(c,stock=stock,amount=amount)
							if amount>=10:
								maker='{},{},{},{}'.format(c.st_name,'尾盘恢复仓位',stock,amount)
								if check_stop_trader(c,stock):
									print(stock,'停牌不交易')
								else:
									if check_is_buy(c,c.account,c.account_type,stock=stock,amount=amount,price=price):
										passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
										print("尾盘恢复仓位 买入{} 数量{} 价格{}".format(stock,amount,price))
									else:
										print("尾盘恢复仓位失败不 买入{} 资金不足".format(stock))
							else:
								print("尾盘恢复仓位不买入{} 低于最低交易单位".format(stock))
						else:
							print("尾盘恢复仓位失败不买入{} 已经有持股".format(stock))
				else:
					#安交易的差额，补今天委托的买卖差额
					print('尾盘恢复仓位分析****************')
					print(df)
					for stock in df['证券代码'].tolist():
						amount=get_buy_sell_amount(c,stock)
						price=get_price(c,stock)
						if amount>=10:
							maker='{},{},{},{}'.format(c.st_name,'尾盘恢复仓位',stock,amount)
							if check_stop_trader(c,stock):
								print(stock,'停牌不交易')
							else:
								if check_is_buy(c,c.account,c.account_type,stock=stock,amount=amount,price=price):
									passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, maker,1,maker,c)
									print("尾盘恢复仓位 买入{} 数量{} 价格{}".format(stock,amount,price))
								else:
									print('尾盘恢复仓位{} 买入不了'.format(stock))
						else:
							print('尾盘恢复仓位{} 没有需要补的'.format(stock))
			else:
				print('尾盘恢复仓位没有持股数据')
		else:
			print('不开启尾盘恢复仓位算法')
	else:
		print(datetime.now(),'尾盘恢复仓位不是交易时间')
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
def get_base_price(c,stock='513100.SH'):
	'''
	获取基础价格
	'''
	n=text['起点']
	start_time='20250101'
	end_time='20500101'
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
	base_price=hist['close'].tolist()[n]
	price=hist['close'].tolist()[-1]
	return base_price 
def cacal_atr(c,stock='513100.SH'):
	'''
	计算atr
	'''
	n=text['ATR倍数']
	N=text['ATR周期']
	start_time='20250101'
	end_time='20500101'
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
	CLOSE=hist['close']
	HIGH=hist['high']
	LOW=hist['low']
	N=N
	mtr,atr=ATR(CLOSE=CLOSE,HIGH=HIGH,LOW=LOW,N=N)
	last_atr=atr[-1]
	last_atr=last_atr*n
	close=CLOSE.tolist()[-1]
	zdf=(last_atr/close)*100
	return last_atr,zdf
	
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
def check_reserve_amount(c, stock='513100.SH', amount=100, bl_amount=100):
	'''
	检查保留的数量
	'''
	
	if amount>=10:
		try:
			position = get_position(c, c.account, c.account_type)
			# 检查持仓是否存在
			if position.empty:
				print('没有持股数据**************')
				return False, 0
			# 过滤指定股票
			stock_position = position[position['证券代码'] == stock]
			if stock_position.empty:
				return False, 0
			# 安全获取持仓数据
			hold_amount = stock_position['持仓量'].iloc[0]
			av_amount = stock_position['可用数量'].iloc[0]
			# 检查保留数量
			if hold_amount <= bl_amount :
				print(f'{stock}不允许卖出,持有数量{hold_amount}小于等于保留数量{bl_amount}')
				return False, 0
			# 计算可卖出数量
			max_sellable = hold_amount - bl_amount  # 最大可卖数量
			actual_sellable = min(max_sellable, av_amount)  # 考虑可用数量
			if actual_sellable < 10:
				print('****************',actual_sellable)
				return False, 0
			# 确定最终卖出数量
			final_amount = min(amount, actual_sellable)
			# 调整数量
			adjusted_amount = adjust_amount(c, stock, final_amount)
			if adjusted_amount >= 10:
				return True, adjusted_amount
			else:
				print('不能保留底仓卖出{}可能单笔金额卖出不了一手 卖出数量{} 小于 保留{}'.format(stock,adjusted_amount,bl_amount))
				return False, 0
		except Exception as e:
			print(f"检查保留数量时发生错误: {e}")
			return False, 0
	else:
		print('@@@@@@不能保留底仓卖出{}可能单笔金额卖出不了一手 '.format(stock))
		return False, 0

def run_tarder_func(c):
	'''
	运行交易函数
	'''
	if check_is_trader_date_1(c):
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
					#log=log[log['交易日']==trader_date]
				else:
					log=pd.DataFrame()
				for name in name_list:
					#try:
					if True:
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
							print('*******************{} {}*****************'.format(stock,name))
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
							daily_df=get_stock_daily_data(c,stock)
							models=user_def_trader_func(c,stock=stock,tick=tick,hist=hist,other_data=daily_df)
							func='models.{}'.format(func)
							stats=func)
							if stats=='buy':
								not_trader_amount,not_trader_value=check_not_trader_data(c,stock=stock)
								limit=hold_amount-not_trader_amount
								if check_hold_limit_amount(c,c.account,c.account_type,stock=stock,limit=limit):
									maker='{},{},{},{},{}'.format(name,stats,stock,buy_amount,str(price).split('.')[0]+'.'+str(price).split('.')[-1][:3])
									if check_stop_trader(c,stock):
										print(stock,'停牌不交易')
										flage='停牌不交易'
										stats=''
									else:
										if check_is_buy(c,c.account,c.account_type,stock=stock,amount=buy_amount,price=price) and buy_amount>=10:
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
								#计算保留仓位
					
								stats1,sell_amount=check_reserve_amount(c, stock=stock, amount=sell_amount, bl_amount=bl_amount)
								if sell_amount>=10 and stats1==True:
									
									maker='{},{},{},{},{}'.format(name,stats,stock,sell_amount,str(price).split('.')[0]+'.'+str(price).split('.')[-1][:3])
									if check_stop_trader(c,stock):
										print(stock,'停牌不交易')
										flage='停牌不交易'
										stats=''
									else:
										if check_is_sell(c,c.account,c.account_type,stock=stock,amount=sell_amount):
											passorder(c.sell_code, 1101, c.account, str(stock), c.sell_price_code, 0, sell_amount, maker,1,maker,c)
											print("{} 卖出{} 数量{} 价格{}".format(name,stock,sell_amount,price))
											flage='卖出成功'
											stats='sell'
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
									else:
										#print('{} {} 不能卖出低于保留仓位'.format(name,stock))
										stats=''
							else:
								#print('{} {} 不符合交易继续观察'.format(name,stock))
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
					#except Exception as e:
						#print(name,stock,'计算有问题',e)
		else:
			print('高频模块没有股票池')
	else:
		print(datetime.now(),'高频交易模型不是交易时间')
	

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
			#self.log=self.log[self.log['交易日']==self.trader_date]
		else:
			self.log=pd.DataFrame()
		
		self.c=c
	def conditional_single_time_sharing_grid(self,
			name='西蒙斯ATR日线固定网格'):
		tick=self.tick
		stock=self.stock
		atr,zdf=cacal_atr(self.c,stock=stock)
		x1=zdf
		x2=-zdf
		base_price=get_base_price(self.c,stock=stock)
		price=tick['lastPrice']
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
			print('{} 模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} atr {}'.format(self.now_date,name,stock,zdf,x1,atr))
			return 'sell'
		elif zdf<=x2:
			print('{} 模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} atr {}'.format(self.now_date,name,stock,zdf,x2,atr))
			return 'buy'
		else:
			print('{} 模块{} 不符合交易{}  目前涨跌幅{} 在{}到{}期间 atr {}'.format(self.now_date,name,stock,zdf,x2,x1,atr))
			return ''
	def symmetric_grid_trading(self,
			name='西蒙斯ATR日线对称网格'):
		'''
		西蒙斯ATR日线对称网格
		'''
		tick=self.tick
		stock=self.stock
		atr,zdf=cacal_atr(self.c,stock=stock)
		x1=zdf
		x2=-zdf
		base_price=get_base_price(self.c,stock=stock)
		price=tick['lastPrice']
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
			print('{} 上一笔买入模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} atr {} '.format(self.now_date,name,stock,zdf,x1,atr))
			return 'sell'
		elif zdf<=x2 and shift_trader_type=='sell':
			print('{}上一笔卖出 模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} atr {}'.format(self.now_date,name,stock,zdf,x2,atr))
			return 'buy'
		if zdf>=x1 :
			print('{}上一笔没有买入委托 模块{} 卖出{}  目前涨跌幅{} 大于目前标涨跌幅{} atr {}'.format(self.now_date,name,stock,zdf,x1,atr))
			return 'sell'
		elif zdf<=x2 :
			print('{} 上一笔没有卖出委托模块{} 买入{}  目前涨跌幅{} 小于目前标涨跌幅{} atr {}'.format(self.now_date,name,stock,zdf,x2,atr))
			return 'buy'
		
		else:
			print('{} 模块{} 不符合交易{}  目前涨跌幅{} 在{}到{}期间 atr {}'.format(self.now_date,name,stock,zdf,x2,x1,atr))
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
	
	
def check_is_trader_date_1(c):
	'''
	检测是不是交易时间
	'''
	trader_time=text['交易时间段']
	start_date=text['交易开始时间']
	end_date=text['交易结束时间']
	start_mi=text['开始交易分钟']
	jhjj=text['是否参加集合竞价']
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
		print('授权码不对')
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
	import datetime
	password_str=c.text['授权码']
	text=password_str
	text=str(password_str))
	start_date=str(datetime.datetime.now())[:10]
	year=text[100:104]
	moth=text[163:165]
	daily=text[184:186]
	end_date='{}-{}-{}'.format(year,moth,daily)
	daily=get_n1_n2_daily(c,start_date=start_date,end_date=end_date)
	if text[8]=='9' and text[16]=='9' and text[24]=='9' and text[32]=='9' and daily>0:
		print('作者:索普量化,微信:xg_quant************授权码正确,到期日{} 剩余天数{}******************'.format(end_date,daily))
		return True
	else:
		print('授权码不对联系作者:索普量化,微信:xg_quant')
def ABS(S):  
	'''
	返回N的绝对值
	'''   
	return np.abs(S)  
def REF(S, N=1):  
	'''        
	对序列整体下移动N,返回序列(shift后会产生NAN)    
	'''
	return pd.Series(S).shift(N).values    
def MA(S,N):    
	'''
	求序列的N日简单移动平均值，返回序列     
	'''                         
	return pd.Series(S).rolling(N).mean().values  
def MAX(S1,S2): 
	'''
	序列max
	'''
	return np.maximum(S1,S2)    
def ATR(CLOSE,HIGH,LOW,N=14):
	'''
	真实波幅
	输出MTR:(最高价-最低价)和1日前的收盘价-最高价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值
	输出真实波幅:MTR的N日简单移动平均
	'''
	MTR=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW))
	ATR=MA(MTR,N)
	return MTR,ATR