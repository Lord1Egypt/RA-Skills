'''
1ETF美中日债金轮动策略实盘
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
'''
#encoding:gbk
'''
ETF美中日债金轮动策略实盘
'''
import pandas as pd
import numpy as np
import talib
import time 
from datetime import datetime
import math
text={
	"自定义交易品种交易":"自定义交易类型比如股票，可转债，etf***********",
	"账户":"770",
	"账户类型":"STOCK",
	"是否隔离策略":"是",
	"交易模式说明":"金额/数量",
	"交易模式":"金额",
	"交易数据周期":"1d",
	"固定交易金额":1000,
	"固定交易数量":100,
	"交易参数设置":"交易参数设置****************",
	"动量天数":25,
	"买入排名":1,
	
	"特殊交易标的设置":"特殊交易标的设置",
	"特殊交易标的":['511360.SH', '159651.SZ', '511580.SH', '511380.SH', '159649', '511270.SH',
	'511030.SH', '511100.SH', '159816.SZ','159651.SZ', '159972.SZ','159651.SZ', '511260.SH', '511010.SH', '511220.SH',
	'511020.SH', '511520.SH', '511060.SH', '511180.SH', '511130.SH', '511090.SH'],
	"特殊交易标的固定交易金额":15000,
	"特殊交易标的固定交易数量":100,
	"时间设置":"时间设置********",
	"交易时间段":8,
	"交易开始时间":0,
	"交易结束时间":24,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	'自定义股票池':"自定义股票池设置",
	"股票池设置":"持有限制10的股票池设置",
	"股票池":["513100.SH","159915.SZ","513520.SH","511010.SH","518880.SH"],
	"股票池名称":["纳斯达克ETF","创业板ETF","日经ETF","30年国债ETF","黄金ETF"]
	}
class A():
	pass
a=A()
def init(c):
	#账户
	c.account=text['账户']
	#账户类型
	c.account_type=text['账户类型']
	#交易股票池
	a.trade_code_list=text['股票池']
	a.trade_code_name=text['股票池名称']
	c.name_dict=dict(zip(a.trade_code_list,a.trade_code_name))
	c.period_1=text['交易数据周期']
	#动量参考基础天数
	c.m_days = text['动量天数']
	c.target_num=text['买入排名']
	#卖出股票池
	c.sells = []
	c.run_time("run_tarder_func","1nDay","2024-07-25 09:35:00")
	c.run_time("run_tarder_func","1nDay","2024-07-25 14:35:00")
	#60分钟一次
	#c.run_time("run_tarder_func","3600nSecond","2024-07-25 13:20:00")
	c.run_time("trader_info","3nSecond","2024-07-25 13:20:00")
	print(get_account(c,c.account,c.account_type))
	print(get_position(c,c.account,c.account_type))
	print(run_tarder_func(c))
	
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
def get_trader_stock(c):
	'''
	获取交易股票池
	'''
	df=pd.DataFrame()
	try:
		df['证券代码']=text['股票池']
		df['名称']=text['股票池名称']
	except Exception as e:
		print(e,'股票池获取有问题')
	return df 
def polynomial(x):
	'''
	计算趋势强度
	'''
	# Define x values and corresponding f(x) values based on your specifications
	x_points = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99])
	y_points = np.array([50, 2, 0.1,  0,  0,  0, 0, 0, -0.1, -2, -50])
	# Fit a polynomial to these points, degree can be adjusted as necessary
	coefficients = np.polyfit(x_points, y_points, deg=5)
	polynomial_f = np.poly1d(coefficients)
	return(polynomial_f(x))
def attribute_history(c,stock='513100.SH',count=25,period='1d'):
	'''
	读取行情数据
	'''
	hist=c.get_market_data_ex(
		fields=[], 
		stock_code=[stock], 
		period=period, 
		start_time='20210101', 
		end_time='20500101', 
		count=-1, 
		fill_data=True, 
		subscribe=True)
	hist=hist[stock]
	hist=hist[-count:]
	return hist
def get_rank(c,etf_pool=["513100.SH","159915.SZ","513520.SH","511010.SH","518880.SH"],
			name_list=["纳斯达克ETF","创业板ETF","日经ETF","30年国债ETF","黄金ETF"]):
	'''
	计算选股评分
	'''
	score_list = []
	score_slope = []
	score_slope2 = []
	score_curve2 = []
	score_curve2_smooth = []
	score_RSI = []
	for etf in etf_pool:
		df = attribute_history(c,etf, c.m_days, c.period_1)
		y = np.log(df['close'])
		x = np.arange(len(y))
		# Create weights for the regression that increase exponentially for more recent data
		weights = np.exp(np.linspace(-1, 0, num=len(y)))  # Adjust the range and steepness as needed        
		coeffs = np.polyfit(x[-25:], y[-25:], 1)
		slope, intercept = coeffs
		coeffs_s = np.polyfit(x[-15:], y[-15:], 1)
		slope_s, intercept_s = coeffs_s
		#coeffs_l = np.polyfit(x[-10:], y[-10:], 1)
		#slope_l, intercept_l = coeffs_l
		coeffs2 = np.polyfit(x[-25:], y[-25:], 2, w=weights[-25:])
		curve2, slope2, intercept2 = coeffs2
		#coeffs3 = np.polyfit(x[:-1], y[:-1], 2, w=weights[:-1])
		#curve3, slope3, intercept3 = coeffs3

		# Smooth the curve2 to avoid noise
		y_smooth = np.convolve(y[-25:], np.ones(5)/5, mode='valid')
		x_smooth = np.arange(len(y_smooth))
		coeffs2_smooth = np.polyfit(x_smooth, y_smooth, 2, w=weights[-23:-2])
		curve2_smooth, slope2_smooth, intercept2_smooth = coeffs2_smooth
			
		# Moving average for trend confirmation
		moving_average = df['close'].rolling(window=20).mean()
		recent_close = df['close'].iloc[-1]
		recent_ma = moving_average.iloc[-1]
		#''' Calculate Relative Strength Index (RSI)
		changes = np.diff(y[-10:])
		gains = changes[changes > 0].sum()
		losses = -changes[changes < 0].sum()
		average_gain = gains
		average_loss = losses
		RS = average_gain / average_loss
		RSI = 100 - (100 / (1 + RS))
		#'''
		# Stability check by ensuring the trend has been consistent
		if ((recent_close > recent_ma) and ((curve2_smooth < -0.0003) or (curve2 < -0.0006))):
			slope_adjust = 0
		elif ((recent_close < recent_ma) and ((curve2_smooth > 0.0003) or (curve2 > 0.0006))):
			slope_adjust = slope + 0.005
		else:
			slope_adjust = slope
		annualized_returns = math.pow(math.exp(slope_adjust), 250) - 1
		annualized_returns_s = math.pow(math.exp(slope_s), 250) - 1
		#annualized_returns_l = math.pow(math.exp(slope_l), 250) - 1
		y_fit = np.polyval(coeffs, x[-25: ])
		ss_res = np.sum((y[-25:] - y_fit) ** 2)
		ss_tot = np.sum((y[-25:] - np.mean(y[-25:])) ** 2)
		r_squared = 1 - (ss_res / ss_tot)
		y_fit_s = np.polyval(coeffs_s, x[-15:])
		ss_res_s = np.sum((y[-15:] - y_fit_s) ** 2)
		ss_tot_s = np.sum((y[-15:] - np.mean(y[-15:])) ** 2)
		r_squared_s = 1 - (ss_res_s / ss_tot_s)
		#y_fit_l = np.polyval(coeffs_l, x[-10:])
		#ss_res_l = np.sum((y[-10:] - y_fit_l) ** 2)
		#ss_tot_l = np.sum((y[-10:] - np.mean(y[-10:])) ** 2)
		#r_squared_l = 1 - (ss_res_l / ss_tot_l)
		combined_score = annualized_returns * r_squared 
		combined_score_s = annualized_returns_s * r_squared_s 
		
			#combined_score_l = annualized_returns_l * r_squared_l 
		if (r_squared_s >= 0.80) and (combined_score_s > combined_score):
			combined_score = combined_score_s
		#if (r_squared_l >= 0.95) and (combined_score_l > combined_score):
		#    combined_score = combined_score_l
		#'''
		if RSI > 95:
			combined_score = 0 #combined_score + polynomial(RSI)/5
		if RSI < 10:
			combined_score = combined_score + polynomial(RSI)/5
		if etf in c.sells[-2:]:
			combined_score = 0
		#'''
		score_list.append(round(combined_score,2))
		score_slope.append(round(slope*10000,2))
		score_slope2.append(round(slope2*10000,2))
		score_curve2.append(round(curve2*10000,2))
		score_curve2_smooth.append(round(curve2_smooth*10000,2))
		score_RSI.append(round(RSI,2))
	df = pd.DataFrame(data={'score': score_list, \
					'sl':   score_slope, \
					'sl2':  score_slope2, \
					'c2':   score_curve2, \
					'c2_s': score_curve2_smooth, \
					'RSI':  score_RSI, \
					}, index=etf_pool)
	df.sort_values(by='score', ascending=False, inplace=True)
	df['证券代码']=df.index.tolist()
	df['名称']=df['证券代码'].apply(lambda x:c.name_dict.get(x,x))
	print('计算的数据结果************88888888888888888888888888888*****************************')
	print(df)
	if df['score'].max() < 0.01:
			#return []
		df=pd.DataFrame()
	else:
		df=df
	return df
def trade(c):
	'''
	获取交易股票池数据
	'''
	# select top one ETF
	#买入的股票前N
	target_num =c.target_num  
	df=get_trader_stock(c)
	print('交易股票池**************')
	print(df)
	print('买入股票池前{}*******'.format(target_num))
	etf_pool=df['证券代码'].tolist()
	name_list=df['名称'].tolist()
	df=get_rank(c,etf_pool,name_list)
	print('股票池评分*******************************************************************')
	print(df)
	if df.shape[0]>0:
		target_list = df['证券代码'].tolist()[:target_num]
	else:
		target_list=[]
	hold_stock=get_position(c,c.account,c.account_type)
	account=get_account(c,c.account,c.account_type)
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
	hold_list=hold_stock_list
	sell_stock_list=[]
	for etf in hold_list:
		if etf not in target_list:
			print(etf,'持股不在买入排名股票池卖出')
			sell_stock_list.append(etf)
		else:
			print(etf,'持股在买入排名股票池继续持有*************')
	#买入
	buy_stock_list=[]
	#if len(hold_list) < target_num:
	print('排序股票池****************************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*')
	print(target_list)
	if True:
		for etf in target_list:
			if etf not in hold_list:
				print(etf,'买入排名没有在持股买入')
				buy_stock_list.append(etf)
			else:
				print(etf,'买入排名在持股不买入****************')
	else:
		print('持有数量大于买入股票池数量不买入')
	buy_df=pd.DataFrame()
	buy_df['证券代码']=buy_stock_list
	if len(hold_stock_list)>0:
		hold_stock['卖出']=hold_stock['证券代码'].apply(lambda x: '是' if x in sell_stock_list else '不是')
		sell_df=hold_stock[hold_stock['卖出']=='是']
	else:
		sell_df=pd.DataFrame()
	print('买入股票池*********')
	print(buy_df)
	print(sell_stock_list)
	print('卖出股票池*********')
	print(sell_df)
	return buy_df,sell_df
def run_tarder_func(c):
	'''
	运行交易函数
	'''
	trader_models=text['交易模式']
	fix_value=text['固定交易金额']
	fix_amount=text['固定交易金额']
	sep_fix_value=text['特殊交易标的固定交易金额']
	sep_fix_amount=text['特殊交易标的固定交易数量']
	sep_stock_list=text['特殊交易标的']
	if check_is_trader_date_1():
		#先卖在买入
		buy_df,sell_df=trade(c)
		if sell_df.shape[0]>0:
			for stock,hold_amount,av_amount in zip(sell_df['证券代码'],sell_df['持仓量'],sell_df['可用数量']):
				try:
					if av_amount>=10:
						print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
						passorder(24, 1101,c.account, stock, 5, 0, av_amount, '',1,'',c)
					else:
						print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
				except:
					print('{}卖出有问题'.format(stock))
		else:
			print('没有卖出的数据')
		#买入
		if buy_df.shape[0]>0:
			for stock in buy_df['证券代码'].tolist():
				if stock  in sep_stock_list:
					print('{}在特殊标的里面*********'.format(stock))
					fix_value=sep_fix_value
					volume=sep_fix_amount
				else:
					fix_value=text['固定交易金额']
					volume=fix_amount
				print(stock,fix_value)
				if trader_models=='金额':
					print('{}金额交易模式*******'.format(stock))
					tader_type,amount,price=order_stock_value(c,c.account,c.account_type,stock,fix_value,'buy')
					print(tader_type,amount,price)
					if tader_type=='buy' and amount>=10 :
						passorder(23, 1101, c.account, str(stock), 5, 0, amount, '',1,'',c)
						#passorder(23, 1101, c.account, str('513100.SH'), 5, 0, 100, '',1,'',c)
						print('{} 最新价格 买入{} 元'.format(stock,fix_value))
					else:
						print('{}金额交易模式买入不了*******'.format(stock))
				else:
					print('{}数量交易模式*******'.format(stock))
					passorder(23, 1101, c.account, str(stock), 5, 0, volume, '',1,'',c)
					print('{} 最新价格 买入{} 数量'.format(stock,volume))
						
		else:
			print('没有买入数据')
	else:
		print('{} 目前不少交易时间'.format(datetime.now()))

def mean_line_models(c,close_list=[],x1=3,x2=5,x3=10,x4=15,x5=20):
	'''
	均线模型
	趋势模型
	5，10，20，30，60
	'''
	df=pd.DataFrame()
	df['close']=close_list
	#df=self.bond_cov_data.get_cov_bond_hist_data(stock=stock,start=start_date,end=end_date,limit=1000000000)
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
def six_pulse_excalibur_hist(c,df):
	
	markers=0
	signal=0
	#df=self.data.get_hist_data_em(stock=stock)
	CLOSE=df['close']
	LOW=df['low']
	HIGH=df['high']
	DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
	DEA=EMA(DIFF,5)
	#如果满足DIFF>DEA 在1的位置标记1的图标
	#DRAWICON(DIFF>DEA,1,1);
	markers+=IF(DIFF>DEA,1,0)
	#如果满足DIFF<DEA 在1的位置标记2的图标
	#DRAWICON(DIFF<DEA,1,2);
	markers+=IF(DIFF<DEA,1,0)
	#DRAWTEXT(ISLASTBAR=1,1,'. MACD'),COLORFFFFFF;{微信公众号:尊重市场}
	ABC1=DIFF>DEA
	signal+=IF(ABC1,1,0)
	尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
	K=SMA(尊重市场1,3,1)
	D=SMA(K,3,1)
	#如果满足k>d 在2的位置标记1的图标
	markers+=IF(K>D,1,0)
	#DRAWICON(K>D,2,1);
	markers+=IF(K<D,1,0)
	#DRAWICON(K<D,2,2);
	#DRAWTEXT(ISLASTBAR=1,2,'. KDJ'),COLORFFFFFF;
	ABC2=K>D
	signal+=IF(ABC2,1,0)
	指标营地=REF(CLOSE,1)
	RSI1=(SMA(MAX(CLOSE-指标营地,0),5,1))/(SMA(ABS(CLOSE-指标营地),5,1))*100
	RSI2=(SMA(MAX(CLOSE-指标营地,0),13,1))/(SMA(ABS(CLOSE-指标营地),13,1))*100
	markers+=IF(RSI1>RSI2,1,0)
	#DRAWICON(RSI1>RSI2,3,1);
	markers+=IF(RSI1<RSI2,1,0)
	#DRAWICON(RSI1<RSI2,3,2);
	#DRAWTEXT(ISLASTBAR=1,3,'. RSI'),COLORFFFFFF;
	ABC3=RSI1>RSI2
	signal+=IF(ABC3,1,0)
	尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
	LWR1=SMA(尊重市场,3,1)
	LWR2=SMA(LWR1,3,1)
	#DRAWICON(LWR1>LWR2,4,1);
	markers+=IF(LWR1>LWR2,1,0)
	#DRAWICON(LWR1<LWR2,4,2);
	markers+=IF(LWR1<LWR2,1,0)
	#DRAWTEXT(ISLASTBAR=1,4,'. LWR'),COLORFFFFFF;
	ABC4=LWR1>LWR2
	signal+=IF(ABC4,1,0)
	BBI=(MA(CLOSE,3)+MA(CLOSE,5)+MA(CLOSE,8)+MA(CLOSE,13))/4
	#DRAWICON(CLOSE>BBI,5,1);
	markers+=IF(CLOSE>BBI,1,0)
	#DRAWICON(CLOSE<BBI,5,2);
	markers+=IF(CLOSE<BBI,1,0)
	#DRAWTEXT(ISLASTBAR=1,5,'. BBI'),COLORFFFFFF;
	ABC10=7
	ABC5=CLOSE>BBI
	signal+=IF(ABC5,1,0)
	MTM=CLOSE-REF(CLOSE,1)
	MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
	MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
	markers+=IF(MMS>MMM,1,0)
	#DRAWICON(MMS>MMM,6,1);
	markers+=IF(MMS<MMM,1,0)
	#DRAWICON(MMS<MMM,6,2);
	#DRAWTEXT(ISLASTBAR=1,6,'. ZLMM'),COLORFFFFFF;
	ABC6=MMS>MMM
	signal+=IF(ABC6,1,0)
	df['signal']=signal
	df['markers']=markers
	return df
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


def order_stock_value(c,accountid,datatype,stock,value,trader_type):
	'''
	价值下单函数
	'''
	price=get_price(c,stock)
	hold_stock=get_position(c,accountid,datatype)
	if hold_stock.shape[0]>0:
		hold_stock=hold_stock[hold_stock['持仓量']>=10]
		if hold_stock.shape[0]>0:
			hold_df=hold_stock[hold_stock['证券代码']==stock]
			if hold_df.shape[0]>0:
				hold_amount=hold_df['持仓量'].tolist()[-1]
				av_amount=hold_df['可用数量'].tolist()[-1]
			else:
				hold_amount=0
				av_amount=0
		else:
			hold_amount=0
			av_amount=0
	else:
		hold_amount=0
		av_amount=0
	account=get_account(c,accountid,datatype)
	av_cash=account['可用金额']
	amount=value/price
	if str(stock)[:2] in ['11','12']:
		amount=int(amount/10)*10
	else:
		amount=int(amount/100)*100
	if trader_type=='buy':
		if av_cash>=value and amount>=10:
			print('金额下单可以资金{}大于买入金额{} 买入{} 价格{} 数量{}'.format(av_cash,value,stock,price,amount))
			return 'buy',amount,price
		else:
			print('金额下单可以资金{}小于买入金额{} 不买入{} 价格{} 数量{}'.format(av_cash,value,stock,price,amount))
			return '','',price 
	elif trader_type=='sell':
		if av_amount>=amount and amount>=10:
			print('金额下单 持有数量{} 可用数量{} 大于卖出数量{} 卖出{} 价格{} 数量{}'.format(hold_amount,av_amount,amount,stock,price,amount))
			return 'sell',amount,price
		elif av_amount<amount and av_amount>=10:
			print('金额下单 持有数量{} 可用数量{} 小于卖出数量{}，可以数量大于10 卖出{} 价格{} 数量{}'.format(hold_amount,av_amount,amount,stock,price,amount))
			return 'sell',amount,price
		else:
			print('金额下单 持有数量{} 可用数量{} 小于卖出数量{}，不卖出{} 价格{} 数量{}'.format(hold_amount,av_amount,amount,stock,price,amount))
			return 'sell',amount,price
	else:
		print('金额下单未知的交易类型{}'.format(stock))
		return '',amount,price
	


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
			data=pd.concat([data,df],ignore_index=True)
	else:
		data=pd.DataFrame()
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
