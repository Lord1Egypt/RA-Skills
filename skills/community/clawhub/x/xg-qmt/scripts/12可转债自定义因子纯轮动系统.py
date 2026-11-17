#encoding:gbk
'''
12可转债自定义因子纯轮动系统
我是小果大QMT交易智能体AI，专注于大QMT量化交易框架的深度训练与智能支持。我能够提供精准的代码提示、输出优化以及策略修改服务，帮助你高效开发和迭代量化交易策略。我的创造者是我爸爸小果量化，如有任何需求或合作意向，欢迎联系微信：xg_quant。代码全部由AI生成整理，只做学习使用，不做投资参考，注意风险
下单的价格编码
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
text={
	
	"账户":"7705",
	"账户支持融资融券":"账户支持融资融券,账户类型STOCK/CREDIT",
	"账户类型":"STOCK",
	
	
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
	"特殊交易标的设置":"特殊交易标的设置",
	"特殊交易标的":[],
	"特殊交易标的固定交易金额":15000,
	"特殊交易标的固定交易数量":100,
	"小果可转债自定义因子轮动策略": "小果可转债服务器提供实时因子数据支持",
	"服务器数据源设置": "服务器数据源设置********",
	"服务器": "",
	"端口": "8023",
	"授权码": "123456",
	"时间设置":"时间设置********",
	"交易时间段":8,
	"交易开始时间":9,
	"交易结束时间":24,
	"是否参加集合竞价":"否",
	"开始交易分钟":0,
	"可转债自定义因子计算": "可转债自定义因子计算************,基于默认因子表计算,df是因子表名称",
	"是否开启默认因子计算": "是",
	"默认因子计算": {
		"三要素评分": "df['溢价率']*100+df['剩余年限']-df['到期税前收益']*100"
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
		"剩余规模(亿)",
		"剩余规模(亿)",
		"剩余年限",
		"溢价率",
		"溢价率",
		"价格",
		"价格",
		"正股年化波动率",
		"涨幅",
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
		"5日斜率",
		"正股年化波动率"
	],
	"因子相关性": [
		"正相关",
		"正相关"
	],
	"因子权重": [
		1
	],
	"持有限制": 10,
	"持股限制": 10,
	"轮动规则设置": "轮动规则设置88888888**********排名",
	"买入排名前N": 10,
	"持有排名前N": 10,
	"跌出排名卖出N": 10,
	"买入前N": 10,
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
	c.del_trader_list=text['黑名单']
	#可以考虑一天轮动2次
	#c.run_time("run_tarder_func","1nDay","2024-07-25 09:50:00")
	c.run_time("run_tarder_func","1nDay","2024-07-25 14:20:00")
	#30分钟一次
	#c.run_time("run_tarder_func","1800nSecond","2024-07-25 13:20:00")
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
def get_trader_data(c):
	'''
	小果可转债5因子轮动策略
	'''
	url=text['服务器']
	port=text['端口']
	password=text['授权码']
	test=text['是否测试']
	test_date=text['测试时间']
	if test=='是':
		print('开启测试模式实盘记得关闭********************')
		date=test_date
	else:
		date=''.join(str(datetime.now())[:10].split('-'))
	#date='20250229'
	print('小果服务器提供数据支持***************************')
	print('服务器{} 端口{} 授权码{}'.format(url,port,password))
	models=small_fruit_custom_factor_selection_system(url=url,
		port=port,
		password=password,
		text=text,
		date=date,
		limit=30)
	stats,df=models.get_select_result()
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
			df['可转债代码']=df['可转债代码'].astype(str)
			df['可转债代码']=df['可转债代码'].apply(lambda x:adjust_stock(x))
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
		print('买入股票****************')
		print(buy_df)
		print('卖出股票*****************')
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
		buy_df,sell_df=get_trader_data(c)
		if sell_df.shape[0]>0:
			for stock,hold_amount,av_amount in zip(sell_df['证券代码'],sell_df['持仓量'],sell_df['可用数量']):
				if stock not in c.del_trader_list:
					print('{} 标的不在黑名单卖出'.format(stock))
					try:
						if av_amount>=10:
							print('{} 持有数量{} 可以数量{}大于0 卖出数量{}'.format(stock,hold_amount,av_amount,av_amount))
							passorder(c.sell_code, 1101,c.account, stock, c.sell_price_code, 0, av_amount, '',1,'',c)
						else:
							print('{} 持有数量{} 可以数量{}等于0 卖出数量{} 不交易'.format(stock,hold_amount,av_amount,av_amount))
					except:
						print('{}卖出有问题'.format(stock))
				else:
					print('{} 标的在黑名单不卖出'.format(stock))
		else:
			print('没有卖出的数据')
		#买入
		if buy_df.shape[0]>0:
			for stock in buy_df['证券代码'].tolist():
				if stock not in c.del_trader_list:
					print('{} 标的不在黑名单买入'.format(stock))
					try:
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
								passorder(c.buy_code, 1101, c.account, str(stock), c.buy_price_code, 0, amount, '',1,'',c)
								#passorder(23, 1101, c.account, str('513100.SH'), 5, 0, 100, '',1,'',c)
								print('{} 最新价格 买入{} 元'.format(stock,fix_value))
							else:
								print('{}金额交易模式买入不了*******'.format(stock))
						else:
							print('{}数量交易模式*******'.format(stock))
							passorder(23, 1101, c.account, str(stock), 5, 0, volume, '',1,'',c)
							print('{} 最新价格 买入{} 数量'.format(stock,volume))
					except Exception as e:
						print(e,'{}买入有问题'.format(stock))
				else:
					print('{} 标的在黑名单不买入'.format(stock))
						
		else:
			print('没有买入数据')
	else:
		print('{} 目前不少交易时间'.format(datetime.now()))
class xg_bond_factor_data:
	'''
	小果可转债因子数据库
	http:///
	'''
	def __init__(self,url='http://124.220.32.224',port='8023',password='123456'):
		'''
		小果可转债因子数据库
		url服务器网页
		port端口
		password授权码
		'''
		self.url=url
		self.port=port
		self.password=password
	def xg_bond_factor_data(self,date_type='实时数据',date='2024-09-09'):
		'''
		小果可转债因子数据库
		date_type=实时数据/全部默认因子/合成因子
		'''
		url='{}:{}/_dash-update-component'.format(self.url,self.port)
		headers={'Content-Type':'application/json'}
		data={
			"output":"xg_bond_data_maker_table.data@5071dc6e12cd478aa2ab511bbb96abce1f6c0a05a17df9112582acfb29cc3216",
			"outputs":{"id":"xg_bond_data_maker_table","property":"data@5071dc6e12cd478aa2ab511bbb96abce1f6c0a05a17df9112582acfb29cc3216"},
			"inputs":[{"id":"password","property":"value","value":self.password},
				{"id":"xg_bond_data_data_type","property":"value","value":date_type},
				{"id":"xg_bond_data_end_date","property":"date","value":date},
				{"id":"xg_bond_data_run","property":"value","value":"运行"},
				{"id":"xg_bond_data_down_data","property":"value","value":"不下载数据"}],
				"changedPropIds":["xg_bond_data_run.value"],
				"parsedChangedPropsIds":["xg_bond_data_run.value"]}
		res=requests.post(url=url,data=json.dumps(data),headers=headers)
		text=res.json()
		df=pd.DataFrame(text['response']['xg_bond_data_maker_table']['data'])
		return df
class small_fruit_custom_factor_selection_system:
	def __init__(self,url='http://124.220.32.224',
		port='8023',
		password='xg123456',
		text={},
		date='20250114',
		limit=30):
		print('小果可转债自定义因子选择系统        ')
		print('作者:小果')
		print('作者微信:15117320079,开实盘qmt可以联系我,开户也可以')
		print('作者微信公众号:数据分析与运用')
		print('公众号链接:https://mp.weixin.qq.com/s/rxGJpZYxdUIHitjvI-US1A')
		print("作者知识星球:金融量化交易研究院  https://t.zsxq.com/19VzjjXNi")
		self.url=url
		self.port=port
		self.password=password
		self.text=text
		self.xg_data=xg_bond_factor_data(url=self.url,port=self.port,password=self.password)
		self.date=date
		self.limit=limit
		self.stats=False
	def select_bond_cov(self,x):
		'''
		选择证券代码
		'''
		if x[:3] in ['110','113','123','127','128','111'] or x[:2] in ['11','12']:
			return '是'
		else:
			return '不是'
	def get_all_factor_data(self):
		'''
		获取可转债全部数据
		'''
		print("获取可转债全部数据************")
		text=self.text
		now_date=self.date
		df=self.xg_data.xg_bond_factor_data(date_type='合成因子',date=now_date)
		stats=df['数据状态'].tolist()[-1]
		try:
			if stats==True or stats=='True' or stats=='true':
				df=df
				print('可转债获取成功***********')
				self.stats=True
			else:
				print(df)
				df=pd.DataFrame()
				self.stats=False
		except Exception as e:
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
		if df.shape[0]>0:
			select_list=['公告要强赎','已公告']
			df['强赎']=df['强赎天计数'].apply(lambda x : '是' if '公告要强赎' in x or '已公告' in x else '不是')
			df1=df[df['强赎']=='是']
			df2=df[df['强赎']=='不是']
			df2['强赎天计数']=df2['强赎天计数'].apply(lambda x: '0/15 | 30' if str(x)[:4]=='暂不强赎' or '不强赎' in x else x)
			df2['强赎天数']=df2['强赎天计数'].apply(lambda x: int(str(x).split('/')[0]))
			df2=df2[df2['强赎天数']<=n]
		else:
			df2=pd.DataFrame()
		return df2
	def days_excluded_from_market(self):
		'''
		排除上市天数
		'''
		print('排除上市天数')
		text=self.text
		df=self.get_del_qzsh_data()
		if  df.shape[0]>0:
			n=text['排除上市天数']
			try:
				df['上市天数']=df['上市天数'].apply(lambda x: float(str(x).split('days')[0]))
				df=df[df['上市天数']>=n]
			except:
				df=df
		else:
			df=pd.DataFrame()
			
		return df
	def st_exclusion(self):
		'''
		排除st
		'''
		print('排除st')
		text=self.text
		is_del=text['是否排除ST']
		df=self.days_excluded_from_market()
		if  df.shape[0]>0:
			if is_del=='是':
				def_list=['ST','st','*ST','*st']
				df['ST']=df['正股名称'].apply(lambda x: '是' if 'st' in x or 'ST' in x or '*st' in x or '*ST' in x else '不是' )
				df=df[df['ST']=='不是']
			else:
				df=df
		else:
			df=pd.DataFrame()
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
		if df.shape[0]>0:
			df['market'] = df['转债代码'].apply(lambda x: '排除' if str(x)[:3] in exclusion_market_list  else '不排除')
			df = df[df['market'] == '不排除']
		else:
			df=pd.DataFrame()
		return df
	def excluded_industry(self):
		'''
		排除行业
		'''
		print('排除行业')
		text=self.text
		del_list=text['排除行业']
		df=self.exclusion_of_market()
		if  df.shape[0]>0:
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
			df=pd.DataFrame()
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
		if df.shape[0]>0:
			del_list=text['排除地域']
			df['排除地域']=df['地域'].apply(lambda x:'是' if str(x) in del_list else '不是')
			df=df[df['排除地域']=='不是']
		else:
			df=pd.DataFrame()
		return df
	def exclusion_of_external_rating(self):
		'''
		排除外部评级
		'''
		print('排除外部评级')
		text=self.text
		df=self.exclusion_area()
		if df.shape[0]>0:
			del_list=text['排除外部评级']
			df['排除外部评级']=df['主体评级'].apply(lambda x:'是' if str(x) in del_list else '不是')
			df=df[df['排除外部评级']=='不是']
		else:
			df=pd.DataFrame()
		return df
	def tripartite_exclusion(self):
		'''
		排除三方评级
		'''
		print('排除三方评级')
		text=self.text
		df=self.exclusion_of_external_rating()
		if df.shape[0]>0:
			del_list=text['排除三方评级']
			df['排除三方评级']=df['主体评级'].apply(lambda x:'是' if str(x) in del_list else '不是')
			df=df[df['排除三方评级']=='不是']
		else:
			df=pd.DataFrame()
		return df
	def cacal_user_def_factor(self):
		'''
		计算自定义因子
		'''
		df=self.tripartite_exclusion()
		return df
	def cacal_exclusion_factor(self):
		'''
		计算排除因子
		'''
		print('计算排除因子')
		text=self.text
		df=self.cacal_user_def_factor()
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
	def get_select_result(self):
		'''
		获取选股结果
		'''
		text=self.text
		select_columns=['可转债名称',"可转债代码"]
		del_factor=list(set(text['排除因子']))
		score_factor=text['打分因子']
		score_type=text['因子相关性']
		for fcator in del_factor:
			select_columns.append(fcator)
		for fcator in score_factor:
			select_columns.append(fcator)   
		select_columns.append('总分')
		df=self.cacal_score_factor()
		if df.shape[0]>0:
			df=df[select_columns]
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
			df=df[:self.limit]
		else:
			df=pd.DataFrame()
		stats=self.stats
		
		return stats,df
	
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
			if is_del=='是':
				df['证券代码']=df['证券代码'].astype(str)
				df['隔离策略']=df['证券代码'].apply(lambda x:select_data_type(x))
				df=df[df['隔离策略']=='bond']
				data=df
			else:
				data=data
		except Exception as e:
			print(e,'隔离策略有问题')
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