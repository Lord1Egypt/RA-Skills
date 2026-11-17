---
name: 小果通达信公式转Python量化
description: |
   小果通达信公式转Python量化函数库。提供100+核心函数、30+技术指标、12+完整交易策略，
   支持将通达信指标公式无缝迁移至Python量化环境，实现策略回测、数据分析与实盘交易信号生成。
   触发关键词：通达信、TDX、公式转换、指标迁移、选股公式、技术指标、量化策略、回测、
   买卖信号、金叉死叉、MACD、KDJ、RSI、BOLL、SAR、CCI、OBV、DMI、BIAS、WR、VR、
   PSY、BRAR、CR、MASS、WAD、ASI、EMV、DPO、CHO、WVAD、TRIX、UOS、VTP、BBI、
   EXPMA、ENE、PBX、MIKE、XS、TQN、BBIBOLL、ALLIGAT、GMMA、AMV、CYC、CYS、CYW、
   ZIG、BACKSET、PEAK、TROUGH、波段交易、趋势跟踪、超买超卖、主力控盘、筹码分布、
   量价配合、股票分析、ETF分析、指数分析、量化投资、程序化交易、小果、xg_quant。
version: 2.0.0
author: 小果
contact:
  wechat: xg_quant
metadata:
  openclaw:
    emoji: "📈"
---
概述
本Skill用于将通达信（TDX）指标公式无缝迁移至Python量化环境。提供100+核心函数、30+技术指标、12+完整交易策略，支持策略回测、数据分析与实盘交易信号生成。

⚠️ 核心原则：所有函数基于pandas/numpy实现，输入数据必须为DataFrame格式，包含open、high、low、close、volume列。函数返回numpy数组或pandas Series，策略类返回增强型DataFrame。
'''
required_columns = {
    'open': '开盘价（float）',
    'high': '最高价（float）',
    'low': '最低价（float）',
    'close': '收盘价（float）',
    'volume': '成交量，单位：手（int或float）'
}
optional_columns = {
    'amount': '成交额，单位：元（float）',
    'capital': '流通股本，单位：股（int或float）',
    'hsl': '换手率，单位：%（float）',
    'date': '日期（datetime类型）',
    'indexc': '大盘收盘价（float）',
    'indexh': '大盘最高价（float）',
    'indexl': '大盘最低价（float）',
    'indexo': '大盘开盘价（float）',
    'indexv': '大盘成交量（float）'
}
# 核心工具函数

函数名	通达信对应	功能说明	实现代码
MA(S, N)	MA	N日简单移动平均	pd.Series(S).rolling(N).mean().values
EMA(S, N)	EMA	N日指数移动平均	pd.Series(S).ewm(span=N, adjust=False).mean().values
SMA(S, N, M)	SMA	中国式加权移动平均	pd.Series(S).ewm(alpha=M/N, adjust=False).mean().values
WMA(S, N)	WMA	N日加权移动平均	pd.Series(S).rolling(N).apply(lambda x: x[::-1].cumsum().sum() * 2 / N / (N + 1), raw=True).values
DMA(S, A)	DMA	动态移动平均	pd.Series(S).ewm(alpha=A, adjust=True).mean().values
HHV(S, N)	HHV	N日内最高值	pd.Series(S).rolling(N).max().values
LLV(S, N)	LLV	N日内最低值	pd.Series(S).rolling(N).min().values
SUM(S, N)	SUM	N日累加和	pd.Series(S).rolling(N).sum().values if N>0 else pd.Series(S).cumsum().values
STD(S, N)	STD	N日估算标准差	pd.Series(S).rolling(N).std(ddof=0).values
AVEDEV(S, N)	AVEDEV	N日平均绝对偏差	pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values
SLOPE(S, N)	SLOPE	N日线性回归斜率	pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N), x, deg=1)[0], raw=True).values
FORCAST(S, N)	FORCAST	N日线性回归预测值	pd.Series(S).rolling(N).apply(lambda x: np.polyval(np.polyfit(range(N), x, deg=1), N-1), raw=True).values
MAX(S1, S2)	MAX	两序列取最大值	np.maximum(S1, S2)
MIN(S1, S2)	MIN	两序列取最小值	np.minimum(S1, S2)
ABS(S)	ABS	绝对值	np.abs(S)
RD(N, D=3)	ROUND	四舍五入保留D位小数	np.round(N, D)
📅 引用与时序类函数（8个）
函数名	通达信对应	功能说明	实现代码
REF(S, N)	REF	引用N周期前的值	pd.Series(S).shift(N).values
DIFF(S, N)	DIFF	前N值减后N值	pd.Series(S).diff(N).values
HHVBARS(S, N)	HHVBARS	N日内最高值到当前周期数	pd.Series(S).rolling(N).apply(lambda x: np.argmax(x[::-1]), raw=True).values
LLVBARS(S, N)	LLVBARS	N日内最低值到当前周期数	pd.Series(S).rolling(N).apply(lambda x: np.argmin(x[::-1]), raw=True).values
CONST(S)	CONST	返回序列最后值组成常量序列	np.full(len(S), S[-1])
BARSCOUNT(S)	BARSCOUNT	有效数据到当前的周期数	统计非NaN数据数量
RET(S, N=1)	RET	返回序列倒数第N个值	np.array(S)[-N]
ALIGNRIGHT(X)	ALIGNRIGHT	有效数据右对齐	有效数据向右移动，左边填充NaN
🧠 逻辑与条件类函数（10个）
函数名	通达信对应	功能说明	实现代码
IF(S, A, B)	IF	条件判断	np.where(S, A, B)
AND(S1, S2)	AND	逻辑与运算	np.logical_and(S1, S2)
OR(S1, S2)	OR	逻辑或运算	np.logical_or(S1, S2)
NOT(S)	NOT	逻辑非运算	np.logical_not(S)
RANGE(A, B, C)	RANGE	区间判断：B <= A <= C	pd.DataFrame(A).apply(lambda x: True if (x >= B and x <= C) else False)
CROSS(S1, S2)	CROSS	判断向上金叉穿越	np.concatenate(([False], np.logical_not((S1 > S2)[:-1]) & (S1 > S2)[1:]))
CROSS_UP(S1, S2)	CROSS	向上金叉（同CROSS）	同上
CROSS_DOWN(S1, S2)	CROSS	向下死叉穿越	np.concatenate(([False], np.logical_not((S1 < S2)[:-1]) & (S1 < S2)[1:]))
LONGCROSS(S1, S2, N)	LONGCROSS	N周期内S1<S2后金叉	np.array(np.logical_and(LAST(S1 < S2, N, 1), (S1 > S2)), dtype=bool)
LAST(S, A, B)	LAST	从前A日到前B日一直满足	np.array(pd.Series(S).rolling(A+1).apply(lambda x: np.all(x[::-1][B:]), raw=True), dtype=bool)
📡 信号与状态类函数（8个）
函数名	通达信对应	功能说明	实现代码
COUNT(S, N)	COUNT	N周期内条件成立次数	SUM(S, N)
EVERY(S, N)	EVERY	N周期内是否全部成立	IF(SUM(S, N) == N, True, False)
EXIST(S, N)	EXIST	N周期内是否存在成立	IF(SUM(S, N) > 0, True, False)
FILTER(S, N)	FILTER	信号过滤，N周期内只保留一次	循环遍历，命中后置零后续N周期
BARSLAST(S)	BARSLAST	上次条件成立到当前周期数	从0开始计数，遇True归零
BARSLASTCOUNT(S)	BARSLASTCOUNT	连续满足条件的周期数	累加器实现
BARSSINCEN(S, N)	BARSSINCEN	N周期内第一次成立到当前	pd.Series(S).rolling(N).apply(lambda x: N-1-np.argmax(x) if np.argmax(x) or x[0] else 0, raw=True)
VALUEWHEN(S, X)	VALUEWHEN	条件成立时取X值，否则取上次值	pd.Series(np.where(S, X, np.nan)).ffill().values
⚠️ 未来函数（6个） - 严禁实盘使用
函数名	通达信对应	功能说明	使用警告
BACKSET(X, N)	BACKSET	将当前位置到N周期前设为1	⚠️ 未来函数，使用未来数据，仅复盘分析
ZIG(CLOSE, X)	ZIG	之字转向，X为转向百分比	⚠️ 未来函数，使用未来数据，仅复盘分析
PEAK(S, N, M)	PEAK	前M个波峰值	⚠️ 未来函数，依赖ZIG，仅复盘分析
TROUGH(S, N, M)	TROUGH	前M个波谷值	⚠️ 未来函数，依赖ZIG，仅复盘分析
PEAKBARS(S, N, M)	PEAKBARS	前M个波峰到当前周期数	⚠️ 未来函数，仅复盘分析
TROUGHBARS(S, N, M)	TROUGHBARS	前M个波谷到当前周期数	⚠️ 未来函数，仅复盘分析

'''
# 技术指标库

指标名称	函数名	参数	输出	使用场景
相对强弱指标	RSI(CLOSE, N1=6, N2=12, N3=24)	N1,N2,N3	RSI1, RSI2, RSI3	RSI>70超买，<30超卖
随机指标	KDJ(CLOSE, HIGH, LOW, N=9, M1=3, M2=3)	N,M1,M2	K, D, J	J>100超买，<0超卖
慢速随机	SKDJ(CLOSE, LOW, HIGH, N=9, M=3)	N,M	K, D	比KDJ更平滑
商品路径指标	CCI(CLOSE, HIGH, LOW, N=14)	N	CCI	>100超买，<-100超卖
威廉指标	WR(CLOSE, LOW, HIGH, N=10, N1=6)	N,N1	WR1, WR2	>80超卖，<20超买
乖离率	BIAS(CLOSE, N1=6, N2=12, N3=24)	N1,N2,N3	BIAS1, BIAS2, BIAS3	偏离均线程度
三六乖离	BIAS36(CLOSE, M=6)	M	BIAS36, BIAS612, MABIAS	短期乖离
资金流量指标	MFI(CLOSE, HIGH, LOW, VOL, N=14)	N	MFI	结合成交量的RSI
动量线	MTM(CLOSE, N=12, M=6)	N,M	MTM, MTMMA	价格变化速度
终极指标	UOS(CLOSE, HIGH, LOW, N1=7, N2=14, N3=28, M=6)	N1,N2,N3,M	UOS, MAUOS	多周期综合
引力线	UDL(CLOSE, N1=3, N2=5, N3=10, N4=20, M=6)	N1,N2,N3,N4,M	UDL, MAUDL	多周期均线综合
LWR指标	LWR(CLOSE, LOW, HIGH, N=9, M1=3, M2=3)	N,M1,M2	LWR1, LWR2	威廉指标变异
📉 趋势类指标（11个）
指标名称	函数名	参数	输出	使用场景
平滑异同平均线	MACD(CLOSE, SHORT=12, LONG=26, MID=9)	SHORT,LONG,MID	DIF, DEA, MACD	金叉买入，死叉卖出
量平滑异同平均	VMACD(VOL, SHORT=12, LONG=26, MID=9)	SHORT,LONG,MID	DIF, DEA, MACD	成交量MACD
单线MACD	SMACD(CLOSE, SHORT=12, LONG=26, MID=9)	SHORT,LONG,MID	DEA, MACD	简化MACD
快速异同平均	QACD(CLOSE, N1=12, N2=12, M=9)	N1,N2,M	DIF, MACD, DDIF	快速MACD
趋向指标	DMI(CLOSE, HIGH, LOW, N=14, M=6)	N,M	PDI, MDI, ADX, ADXR	ADX>25趋势明显
三重指数平均	TRIX(CLOSE, N=12, M=9)	N,M	TRIX, MATRIX	消除短期波动
振动升降指标	ASI(OPEN, CLOSE, HIGH, LOW, M1=26, M2=10)	M1,M2	ASI, ASIT	判断突破与背离
简易波动指标	EMV(HIGH, LOW, VOL, N=14, M=9)	N,M	EMV, MAEMV	结合量价判断趋势
区间震荡线	DPO(CLOSE, N=21, M=6)	N,M	DPO, MADPO	去除趋势后震荡
佳庆指标	CHO(CLOSE, OPEN, LOW, HIGH, VOL, N1=10, N2=20, M=6)	N1,N2,M	CHO, MACHO	量价背离判断
威廉变异离散量	WVAD(CLOSE, OPEN, HIGH, LOW, VOL, N=24, M=6)	N,M	WVAD, MAWVAD	主力资金动向
📊 能量类指标（9个）
指标名称	函数名	参数	输出	使用场景
累积能量线	OBV(VOL, CLOSE, M=30)	M	OBV, MAOBV	量价配合关系
成交量变异率	VR(CLOSE, VOL, N=26, M=6)	N,M	VR, MAVR	成交量变化趋势
心理线	PSY(CLOSE, N=12, M=6)	N,M	PSY, PSYMA	投资者心理
情绪指标	BRAR(OPEN, HIGH, LOW, CLOSE, N=26)	N	BR, AR	市场情绪
带状能量线	CR(HIGH, LOW, N=26, M1=10, M2=20, M3=40, M4=60)	N,M1,M2,M3,M4	CR, MA1~MA4	多周期能量
梅斯线	MASS(HIGH, LOW, N1=9, N2=25, M=6)	N1,N2,M	MASS, MAMASS	趋势反转判断
市场强弱	CYR(AMOUNT, VOL, N=13, M=5)	N,M	CYR, MACYR	市场强弱程度
威廉多空力度	WAD(CLOSE, LOW, HIGH, M=30)	M	WAD, MAWAD	多空力量对比
幅度比	PCNT(CLOSE, M=5)	M	PCNT, MAPCNT	价格变化幅度
💹 均线系统（12个）
指标名称	函数名	参数	输出	使用场景
均线	MA_XT(CLOSE, M1=5, M2=10, M3=20, M4=60)	M1,M2,M3,M4	MA1~MA4	基础趋势跟踪
均线2	MA2(CLOSE, M1=5, M2=10, M3=20, M4=60, M5=120, M6=240, M7=360, M8=420, M9=680, M10=720)	M1~M10	MA1~MA10	多周期均线
多空均线	BBI(CLOSE, M1=3, M2=6, M3=12, M4=24)	M1,M2,M3,M4	BBI	四线综合
指数平均线	EXPMA(CLOSE, M1=12, M2=50)	M1,M2	EXP1, EXP2	平滑均线
高价平均线	HMA(HIGH, M1=6, M2=12, M3=30, M4=70, M5=90)	M1~M5	HMA1~HMA5	高价趋势
低价平均线	LMA(LOW, M1=6, M2=12, M3=30, M4=70, M5=90)	M1~M5	LMA1~LMA5	低价趋势
变异平均线	VMA(HIGH, OPEN, LOW, CLOSE, M1=6, M2=12, M3=30, M4=70, M5=90)	M1~M5	VMA1~VMA5	综合价格均线
成本均线	AMV(OPEN, CLOSE, VOL, M1=5, M2=13, M3=34, M4=60)	M1~M4	AMV1~AMV4	考虑成交量
多空布林线	BBIBOLL(CLOSE, N=11, M=6)	N,M	BBIBOLL, UPR, DWN	多空判断
鳄鱼线	ALLIGAT(HIGH, LOW)	-	上唇,牙齿,下颚	趋势方向
顾比均线	GMMA(CLOSE)	-	12条EMA	短期长期均线组
升降线	ACD(CLOSE, HIGH, LOW, M=20)	M	ACD, MAACD	价格升降
🛤️ 路径类指标（8个）
指标名称	函数名	参数	输出	使用场景
布林线	BOLL(CLOSE, M=20)	M	BOLL, UB, LB	价格高低位置
瀑布线	PBX(CLOSE, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)	M1~M6	PBX1~PBX6	多周期趋势
轨道线	ENE(CLOSE, N=25, M1=6, M2=6)	N,M1,M2	UPPER, LOWER, ENE	价格通道
麦克支撑压力	MIKE(HIGH, LOW, CLOSE, N=10)	N	STOR,MIDR,WEKR,WEKS,MIDS,STOS	支撑阻力位
薛斯通道	XS(CLOSE, VOL, N=13)	N	SUP, SDN, LUP, LDN	多重通道
薛斯通道II	XS2(CLOSE, HIGH, LOW, N=102, M=7)	N,M	通道1~4	扩展通道
唐奇安通道	TQN(HIGH, LOW, X1=20, X2=20)	X1,X2	周期高点,周期低点	突破策略
抛物线转向	SAR(HIGH, LOW, M=10, af=2, amax=20)	M,af,amax	SAR	趋势跟踪止损
🐉 神系龙系鬼系及其他特色指标（29个）
指标名称	函数名	输出	使用场景
心电图	SG_XDT(CLOSE, INDEXC)	QR, MQR1, MQR2	相对大盘强弱
脑电波	SG_NDB(CLOSE, HIGH, LOW)	DK, MDK1, MDK2	特殊波动分析
生命线	SG_SMX(CLOSE, HIGH, LOW, INDEXH, INDEXL, INDEXC)	ZY1, ZY2, ZY3	多周期生命线
量比	SG_LB(VOL, INDEXV)	量比, MA5, MA10	成交量相对强弱
强势股评分	SG_PF(CLOSE, INDEXC)	强势股评分	个股强势程度
威力雷达	RAD(OPEN, HIGH, CLOSE, LOW, INDEXO, INDEXH, INDEXL, INDEXC)	RADER1, RADERMA	相对大盘动量
龙系长线	LON(CLOSE, HIGH, LOW, VOL)	LON, LONMA, LONT	长线趋势判断
龙系短线	SHT(CLOSE, VOL)	SHT, SHTMA	短线交易信号
主力进出	ZLJC(CLOSE, LOW, HIGH, VOL)	JCS, JCM, JCL	主力资金动向
主力买卖	ZLMM(CLOSE)	MMS, MMM, MML	主力多空判断
神龙在天	SLZT(CLOSE, LOW, HIGH)	白龙,黄龙,紫龙,青龙,红龙,蓝龙	多空趋势
龙系离散量	ADVOL(CLOSE, HIGH, LOW, VOL)	ADVOL, MA1, MA2	量价离散
成本均线	CYC(CLOSE, AMOUNT, VOL)	CYC1, CYC2, CYC3	市场成本分布
市场盈亏	CYS(CLOSE, AMOUNT, VOL)	CYS	筹码盈亏状态
主力控盘	CYW(CLOSE, HIGH, LOW, VOL)	CYW	主力控盘程度
济安线	JAX(CLOSE, HIGH, LOW, N=30)	J, A, X	动态支撑压力
超级短线	XJDX(CLOSE, HIGH, LOW)	J, D, K	短线交易信号
庄家抬轿	ZJTJ(CLOSE)	无庄控盘,开始控盘,有庄控盘,主力出货	主力行为判断
准备抄底	ZBCD(HIGH, LOW, OPEN, AMOUNT, VOL, CLOSE, N=10)	抄底	底部信号
波段之星	BDZX(HIGH, LOW, CLOSE)	AK, AD1, AJ, AA, BB, CC, 买进,卖出	波段操作
猎狐先觉	LHXJ(HIGH, LOW, CLOSE)	主力弃盘,主力控盘	主力动向
猎鹰歼狐	LYJH(CLOSE, HIGH, LOW, M=80, M1=50)	机构做空能量线,机构做多能量线,LH,LH1	机构行为
飓风智能中线	JFZX(OPEN, CLOSE, VOL, N=30)	多头力量,空头力量,多空平衡	多空力量
财运亨通	CYHT(CLOSE, HIGH, LOW, OPEN)	高抛,SK,SD,低吸,强弱分界,卖出,买进	买卖点判断
买卖区间	BSQJ(CLOSE)	B买,持仓,S卖,空仓	持仓区间判断
逆势操作	CDP_STD(CLOSE, HIGH, LOW)	CDP, AH, NH, NL, AL	关键价位
趋势平衡点	TBP_STD(HIGH, LOW, CLOSE)	TBP,多头获利,多头停损,空头回补,空头停损	趋势平衡
市场趋势	CYE(CLOSE)	CYEL, CYES	市场趋势速度
强弱指标	QR(CLOSE, INDEXC, N=21)	GG, DP, value	个股大盘对比
轨道线	GDX(CLOSE, HIGH, LOW, N=30, M=9)	轨道,压力线,支撑线	轨道判断
3.3 完整交易策略类（12个）
策略名称	类名	方法名	适用场景	输出字段
波段超级买卖	band_supe_buy_sell	band_supe_buy_sell()	中短线波段操作	笑脸、标记文字、趋势、stats
六脉神剑	six_pulse_excalibur_hist	six_pulse_excalibur_hist()	多维度共振判断	买入、持有、共振、signal、markers
麒麟趋势线	the_kirin_trend_line	the_kirin_trend_line()	趋势跟踪，明显趋势行情	红色持股、青色观望、短买、白色离场、量化评分、stats
鼎牛周期共振主图	dingniu_periodic_resonance_master_diagram	dingniu_periodic_resonance_master_diagram()	强势股捕捉，追涨策略	红色柱子、绿色柱子、黄色柱子、涨停牛、共振、条形线
鼎牛周期共振副图	dingniu_periodic_resonance_subdiagram	dingniu_periodic_resonance_subdiagram()	副图辅助判断	柱子、起点、淡红色
主力擒黑马主图	main_approach_to_capture_dark_horse_main_figure	main_approach_to_capture_dark_horse_main_figure()	捕捉底部启动黑马股	黑马、深灰色、黄色、红色、淡红色、青色、绿色
主力擒黑马副图	main_approach_to_capture_the_dark_horse_deputy_map	main_approach_to_capture_the_dark_horse_deputy_map()	副图辅助判断黑马	趋势、买、卖、卖临界、主力吸筹、低点、追
九指共振	nine_finger_resonance	nine_finger_resonance()	多周期多指标共振	综合评分（0-9分）
小果波段交易	small_fruit_band_trading	small_fruit_band_trading()	波段交易，适合震荡市场	柱子、买、卖、stats
小果波段交易指数	small_fruit_band_trading_index	small_fruit_band_trading_index()	指数波段交易	柱子、买、卖、stats
小果波段交易高频T0	small_fruit_band_trading_hist_trader	small_fruit_band_trading_hist_trader()	T0高频交易	MA1、MA2、柱子、买、卖、stats、连续交易
小果波段掘金	small_fruit_band_gold_mining	small_fruit_band_gold_mining()	波段掘金信号	B、S、红色、绿色、黄色、蓝色、星
小果高频量线	small_fruit_high_frequency_measurement_line	small_fruit_high_frequency_measurement_line()	高频交易	超准、股、币、均、买、卖、stats、连续交易
趋势王V02主图	trend_king_v2_master_chart	trend_king_v2_master_chart()	中长线趋势跟踪	趋势、共振、建仓
趋势王V02副图	trend_king_v2_subchart	trend_king_v2_subchart()	副图趋势确认	趋势线、方块
顺势黑马	take_advantage_of_the_trend	take_advantage_of_the_trend()	顺势交易，趋势跟踪	买、强、红色、绿色、hold、sell、buy
四、使用注意事项（必须遵守）
4.1 数据要求
序号	注意事项	详细说明
1	数据长度要求	至少250个交易日（约1年），EMA/SMA至少120周期保证精度
2	数据顺序要求	必须按时间升序排列（从旧到新），否则指标计算完全错误
3	列名必须小写	open、high、low、close、volume，大小写敏感
4	不允许空值	所有NA/NaN需提前清洗，否则函数返回全NaN
5	成交量不能为0	需将0替换为1，避免除零错误
6	价格不能为负	价格序列必须为正数
7	频率必须一致	不能混用日线/周线/月线数据
8	索引不能为日期	建议使用整数索引，日期放在独立列
4.2 性能建议
序号	建议	详细说明
1	使用numpy数组	大数据量（>5000行）建议转为numpy数组计算
2	避免循环遍历	优先使用pandas向量化操作
3	减少rolling apply	使用内置rolling方法（mean、sum、max、min）更快
4	批量计算	多个指标一起计算，减少重复遍历
5	内存管理	及时删除中间变量，释放内存
4.3 未来函数警告（严禁实盘）
函数	危害说明
ZIG	使用未来数据重绘曲线，产生完美买卖点假象
BACKSET	将未来信号前置到历史位置，制造信号命中假象
PEAK/TROUGH	基于ZIG，同样使用未来数据
PEAKBARS/TROUGHBARS	基于ZIG，同样使用未来数据
后果	回测收益虚高，实盘完全失效，造成重大亏损
4.4 常见错误与解决方案
错误现象	可能原因	解决方案
计算结果全是NaN	数据长度不足或存在空值	检查数据长度≥N+1，清洗空值
EMA/SMA精度不够	数据长度<120周期	增加数据长度至120以上
信号明显延迟	使用了未来函数或REF偏移方向错误	检查CROSS和REF的使用
策略类报错KeyError	数据列名不匹配	检查列名必须为小写：open、high、low、close、volume
除零错误	成交量或价格序列含0	将0替换为小正数（如1）
买卖信号过多	FILTER参数设置过小	增大过滤周期N
回测结果与实际不符	可能使用了未来函数	移除BACKSET、ZIG、PEAK、TROUGH等
4.5 导入规范
python
# 正确导入方式
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data

# 策略类导入
from xg_tdx_func.band_supe_buy_sell import band_supe_buy_sell
from xg_tdx_func.six_pulse_excalibur_hist import six_pulse_excalibur_hist
from xg_tdx_func.the_kirin_trend_line import the_kirin_trend_line
from xg_tdx_func.trend_king_v2_master_chart import trend_king_v2_master_chart
from xg_tdx_func.main_approach_to_capture_dark_horse_main_figure import main_approach_to_capture_dark_horse_main_figure
from xg_tdx_func.nine_finger_resonance import nine_finger_resonance
from xg_tdx_func.small_fruit_band_trading import small_fruit_band_trading
from xg_tdx_func.small_fruit_high_frequency_measurement_line import small_fruit_high_frequency_measurement_line
from xg_tdx_func.small_fruit_band_gold_mining import small_fruit_band_gold_mining
from xg_tdx_func.take_advantage_of_the_trend import take_advantage_of_the_trend
五、使用示例
5.1 基础指标计算
python
from xg_tdx_func.xg_tdx_func import *
import pandas as pd

df = pd.read_csv('stock_data.csv')
close = df['close'].values
high = df['high'].values
low = df['low'].values
volume = df['volume'].values

# MACD
dif, dea, macd = MACD(close, SHORT=12, LONG=26, MID=9)

# KDJ
k, d, j = KDJ(close, high, low, N=9, M1=3, M2=3)

# RSI
rsi1, rsi2, rsi3 = RSI(close, 6, 12, 24)

# 金叉检测
golden_cross = CROSS(k, d)

# 超买超卖信号
oversold = rsi1 < 30
overbought = rsi1 > 70

df['MACD'] = macd
df['KDJ_K'] = k
df['KDJ_D'] = d
df['金叉'] = golden_cross
df['超卖'] = oversold
5.2 策略类调用
python
from xg_tdx_func.band_supe_buy_sell import band_supe_buy_sell
from trader_tool.unification_data import unification_data

data = unification_data(trader_tool='ths')
df = data.get_hist_data_em(stock='513100', start_date='20200101')

model = band_supe_buy_sell(df=df)
result = model.band_supe_buy_sell()

buy_signals = result[result['买'] == '买']
sell_signals = result[result['卖'] == '卖']

print(f"买入信号数量: {len(buy_signals)}")
print(f"卖出信号数量: {len(sell_signals)}")

result.to_excel('策略信号结果.xlsx')
5.3 自定义指标组合
python
from xg_tdx_func.xg_tdx_func import *

def my_custom_strategy(close, high, low, volume):
    # 计算均线
    ma5 = MA(close, 5)
    ma20 = MA(close, 20)
    ma60 = MA(close, 60)
    
    # 计算RSI
    rsi = RSI(close, N1=6)[0]
    
    # 计算MACD
    dif, dea, macd = MACD(close)
    
    # 均线多头排列
    bullish = AND(AND(ma5 > ma20, ma20 > ma60), rsi > 50)
    
    # 金叉信号
    golden = CROSS(ma5, ma20)
    
    # 成交量放量
    vol_ma = MA(volume, 10)
    volume_surge = volume > vol_ma * 1.5
    
    # 综合买入信号
    buy_signal = AND(AND(golden, bullish), volume_surge)
    
    return {'ma5': ma5, 'ma20': ma20, 'ma60': ma60, 'rsi': rsi, 'buy': buy_signal}
5.4 完整交易系统示例
python
from xg_tdx_func.xg_tdx_func import *
import pandas as pd
import numpy as np

class MyTradingSystem:
    def __init__(self, df):
        self.df = df.copy()
        self.signals = None
        
    def calculate_signals(self):
        close = self.df['close'].values
        high = self.df['high'].values
        low = self.df['low'].values
        volume = self.df['volume'].values
        
        # 计算指标
        ma10 = MA(close, 10)
        ma30 = MA(close, 30)
        rsi = RSI(close, 6)[0]
        k, d, j = KDJ(close, high, low)
        
        # 生成信号
        buy_condition = AND(CROSS(ma10, ma30), AND(rsi > 40, k > d))
        sell_condition = OR(CROSS(ma30, ma10), j > 100)
        
        # 过滤信号
        buy_signal = FILTER(buy_condition, 5)
        sell_signal = FILTER(sell_condition, 5)
        
        self.df['buy'] = buy_signal
        self.df['sell'] = sell_signal
        self.df['ma10'] = ma10
        self.df['ma30'] = ma30
        self.df['rsi'] = rsi
        
        return self.df
    
    def backtest(self):
        position = 0
        trades = []
        for i in range(len(self.df)):
            if self.df['buy'][i] and position == 0:
                position = 1
                trades.append({'date': self.df.index[i], 'action': 'buy', 'price': self.df['close'][i]})
            elif self.df['sell'][i] and position == 1:
                position = 0
                trades.append({'date': self.df.index[i], 'action': 'sell', 'price': self.df['close'][i]})
        return pd.DataFrame(trades)
六、输出结果说明
6.1 单指标输出
返回numpy数组或pandas Series

开头可能包含NaN（需自行处理）

6.2 策略类输出（DataFrame）
字段类型	字段名	说明
原始数据	open, high, low, close, volume	原始行情数据
指标列	MA5, MA10, 动力线, 趋势线等	各种技术指标值
信号列	买, 卖, stats	买卖标记和连续持仓状态
颜色列	柱子, 红色, 绿色, 黄色等	用于可视化
特殊列	共振, 建仓, 涨停牛等	策略特有信号
# 例子参考
# 基础指标计算
'''
from xg_tdx_func.xg_tdx_func import *
import pandas as pd

df = pd.read_csv('stock_data.csv')
close = df['close'].values
high = df['high'].values
low = df['low'].values
volume = df['volume'].values

# MACD
dif, dea, macd = MACD(close, SHORT=12, LONG=26, MID=9)

# KDJ
k, d, j = KDJ(close, high, low, N=9, M1=3, M2=3)

# RSI
rsi1, rsi2, rsi3 = RSI(close, 6, 12, 24)

# 金叉检测
golden_cross = CROSS(k, d)

# 超买超卖信号
oversold = rsi1 < 30
overbought = rsi1 > 70

df['MACD'] = macd
df['KDJ_K'] = k
df['KDJ_D'] = d
df['金叉'] = golden_cross
df['超卖'] = oversold
'''
# 2自定义参考
'''
from xg_tdx_func.xg_tdx_func import *

def my_custom_strategy(close, high, low, volume):
    # 计算均线
    ma5 = MA(close, 5)
    ma20 = MA(close, 20)
    ma60 = MA(close, 60)
    
    # 计算RSI
    rsi = RSI(close, N1=6)[0]
    
    # 计算MACD
    dif, dea, macd = MACD(close)
    
    # 均线多头排列
    bullish = AND(AND(ma5 > ma20, ma20 > ma60), rsi > 50)
    
    # 金叉信号
    golden = CROSS(ma5, ma20)
    
    # 成交量放量
    vol_ma = MA(volume, 10)
    volume_surge = volume > vol_ma * 1.5
    
    # 综合买入信号
    buy_signal = AND(AND(golden, bullish), volume_surge)
    
    return {'ma5': ma5, 'ma20': ma20, 'ma60': ma60, 'rsi': rsi, 'buy': buy_signal}
'''
# 核心通达信解析函数
'''
小果
微信:xg_quant
'''
import pandas as pd
import numpy as np
#------------------ 0级：核心工具函数 -------------------------------------------
import numpy as np
import pandas as pd

def RD(N, D=3):
    """四舍五入取3位小数"""
    return np.round(N, D)

def RET(S, N=1):
    """返回序列倒数第N个值，默认返回最后一个"""
    return np.array(S)[-N]

def ABS(S):
    """返回N的绝对值"""
    return np.abs(S)

def MAX(S1, S2):
    """序列max"""
    return np.maximum(S1, S2)

def MIN(S1, S2):
    """序列min"""
    return np.minimum(S1, S2)

def IF(S, A, B):
    """序列布尔判断 return=A if S==True else B"""
    return np.where(S, A, B)

def REF(S, N=1):
    """对序列整体下移动N，返回序列(shift后会产生NAN)"""
    return pd.Series(S).shift(N).values

def DIFF(S, N=1):
    """前一个值减后一个值，前面会产生nan；np.diff(S)直接删除nan，会少一行"""
    return pd.Series(S).diff(N).values

def STD(S, N):
    """求序列的N日标准差，返回序列"""
    return pd.Series(S).rolling(N).std(ddof=0).values

def SUM(S, N):
    """对序列求N天累计和，返回序列；N=0对序列所有依次求和"""
    return pd.Series(S).rolling(N).sum().values if N > 0 else pd.Series(S).cumsum().values

def CONST(S):
    """返回序列S最后的值组成常量序列"""
    return np.full(len(S), S[-1])

def AND(S1, S2):
    """逻辑与运算"""
    return np.logical_and(S1, S2)

def OR(S1, S2):
    """逻辑或运算"""
    return np.logical_or(S1, S2)

def NOT(S1):
    """逻辑非运算"""
    return np.logical_not(S1)

def RANGE(A, B, C):
    """期间函数：B <= A <= C"""
    df = pd.DataFrame()
    df['select'] = A.tolist()
    df['select'] = df['select'].apply(lambda x: True if (x >= B and x <= C) else False)
    return df['select']

def HHV(S, N):
    """HHV(C, 5) 最近5天收盘最高价"""
    return pd.Series(S).rolling(N).max().values

def LLV(S, N):
    """LLV(C, 5) 最近5天收盘最低价"""
    return pd.Series(S).rolling(N).min().values

def HHVBARS(S, N):
    """求N周期内S最高值到当前周期数，返回序列"""
    return pd.Series(S).rolling(N).apply(lambda x: np.argmax(x[::-1]), raw=True).values

def LLVBARS(S, N):
    """求N周期内S最低值到当前周期数，返回序列"""
    return pd.Series(S).rolling(N).apply(lambda x: np.argmin(x[::-1]), raw=True).values

def MA(S, N):
    """求序列的N日简单移动平均值，返回序列"""
    return pd.Series(S).rolling(N).mean().values

def EMA(S, N):
    """指数移动平均，为了精度 S>4*N，EMA至少需要120周期；alpha=2/(span+1)"""
    return pd.Series(S).ewm(span=N, adjust=False).mean().values

def SMA(S, N, M=1):
    """中国式的SMA，至少需要120周期才精确(雪球180周期)；alpha=1/(1+com)"""
    return pd.Series(S).ewm(alpha=M/N, adjust=False).mean().values  # com=N-M/M

def DMA(S, A):
    """求S的动态移动平均，A作平滑因子，必须 0<A<1 (此为核心函数，非指标)"""
    return pd.Series(S).ewm(alpha=A, adjust=True).mean().values

def WMA(S, N):
    """通达信S序列的N日加权移动平均 Yn = (1*X1+2*X2+3*X3+...+n*Xn)/(1+2+3+...+Xn)"""
    return pd.Series(S).rolling(N).apply(lambda x: x[::-1].cumsum().sum() * 2 / N / (N + 1), raw=True).values

def AVEDEV(S, N):
    """平均绝对偏差 (序列与其平均值的绝对差的平均值)"""
    return pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values

def SLOPE(S, N):
    """返回S序列N周期回线性回归斜率"""
    return pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N), x, deg=1)[0], raw=True).values

def FORCAST(S, N):
    """返回S序列N周期回线性回归后的预测值"""
    return pd.Series(S).rolling(N).apply(lambda x: np.polyval(np.polyfit(range(N), x, deg=1), N-1), raw=True).values

def LAST(S, A, B):
    """从前A日到前B日一直满足S_BOOL条件，要求A>B & A>0 & B>=0"""
    return np.array(pd.Series(S).rolling(A+1).apply(lambda x: np.all(x[::-1][B:]), raw=True), dtype=bool)


#------------------ 1级：应用层函数(通过0级核心函数实现）--------------------------
def COUNT(S, N):
    """COUNT(CLOSE>O, N): 最近N天满足S_BOO的天数，True的天数"""
    return SUM(S, N)

def EVERY(S, N):
    """EVERY(CLOSE>O, 5) 最近N天是否都是True"""
    return IF(SUM(S, N) == N, True, False)

def EXIST(S, N):
    """EXIST(CLOSE>3010, N=5) n日内是否存在一天大于3000点"""
    return IF(SUM(S, N) > 0, True, False)

def FILTER(S, N):
    """
    FILTER函数，S满足条件后，将其后N周期内的数据置为0
    例：FILTER(C==H,5) 涨停后，后5天不再发出信号
    """
    for i in range(len(S)):
        if S[i]:
            S[i+1:i+1+N] = 0
    return S

def BARSLAST(S):
    """上一次条件成立到当前的周期，BARSLAST(C/REF(C,1)>=1.1) 上一次涨停到今天的天数"""
    M = np.concatenate(([0], np.where(S, 1, 0)))
    for i in range(1, len(M)):
        M[i] = 0 if M[i] else M[i-1] + 1
    return M[1:]

def BARSLASTCOUNT(S):
    """统计连续满足S条件的周期数；BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数"""
    rt = np.zeros(len(S) + 1)
    for i in range(len(S)):
        rt[i+1] = rt[i] + 1 if S[i] else rt[i+1]
    return rt[1:]

def BARSSINCEN(S, N):
    """N周期内第一次S条件成立到现在的周期数，N为常量"""
    return pd.Series(S).rolling(N).apply(
        lambda x: N-1-np.argmax(x) if np.argmax(x) or x[0] else 0,
        raw=True
    ).fillna(0).values.astype(int)

def CROSS(S1, S2):
    """判断向上金叉穿越 CROSS(MA(C,5), MA(C,10))；判断向下死叉穿越 CROSS(MA(C,10), MA(C,5))"""
    return np.concatenate(([False], np.logical_not((S1 > S2)[:-1]) & (S1 > S2)[1:]))

def CROSS_UP(S1, S2):
    """判断向上金叉穿越 CROSS(MA(C,5), MA(C,10))"""
    return np.concatenate(([False], np.logical_not((S1 > S2)[:-1]) & (S1 > S2)[1:]))

def CROSS_DOWN(S1, S2):
    """判断向下死叉穿越 CROSS(MA(C,5), MA(C,10))"""
    return np.concatenate(([False], np.logical_not((S1 < S2)[:-1]) & (S1 < S2)[1:]))

def LONGCROSS(S1, S2, N):
    """两条线维持一定周期后交叉，S1在N周期内都小于S2，本周期从S1下方向上穿过S2时返回1，否则返回0；N=1时等同于CROSS(S1, S2)"""
    return np.array(np.logical_and(LAST(S1 < S2, N, 1), (S1 > S2)), dtype=bool)

def VALUEWHEN(S, X):
    """当S条件成立时，取X的当前值，否则取VALUEWHEN的上个成立时的X值"""
    return pd.Series(np.where(S, X, np.nan)).ffill().values


#------------------ 扩展函数（来自第二个文件）-------------------------------------
def BACKSET(X, N):
    """
    属于未来函数，将当前位置到若干周期前的数据设为1。
    用法：BACKSET(X,N)，若X非0，则将当前位置到N周期前的数值设为1。
    例如：BACKSET(CLOSE>OPEN,2) 若收阳则将该周期及前一周期数值设为1，否则为0
    """
    result = np.zeros_like(X)
    for i in range(len(X)):
        if X[i] != 0:
            start_index = max(0, i - N + 1)
            result[start_index:i+1] = 1
    return result

def ALIGNRIGHT(X):
    """
    有效数据右对齐。
    用法：ALIGNRIGHT(X) 有效数据向右移动，左边空出来的周期填充无效值
    例如：TC:=IF(CURRBARSCOUNT=2 || CURRBARSCOUNT=5, DRAWNULL, C); XC:=ALIGNRIGHT(TC);
         删除了两天的收盘价，并将剩余数据右移
    """
    valid_indices = np.where(X != np.nan)[0]
    invalid_count = len(X) - len(valid_indices)
    result = np.empty_like(X)
    result[:] = np.nan
    result[invalid_count:len(valid_indices)+invalid_count] = X[valid_indices]
    return result

def BARSCOUNT(X):
    """
    有效数据周期数。
    用法：BARSCOUNT(X) 第一个有效数据到当前的间隔周期数
    注意：判断范围为指标或条件选股计算时公式使用的数据，
          如果给画线指标的数据少(比如没有按下箭头取更多K线)或给条件选股给的数据少，这个有效值也可能少
    """
    valid_indices = np.where(~np.isnan(X))[0]
    if len(valid_indices) == 0:
        return 0
    first_valid_index = valid_indices[0]
    current_index = len(X) - 1
    bars_count = current_index - first_valid_index + 1
    return bars_count

def BARSLASTS(X, N):
    """
    倒数第N次成立时距今的周期数。
    用法：BARSLASTS(X,N): X倒数第N满足到现在的周期数，N支持变量
    """
    valid_indices = np.where(~np.isnan(X))[0]
    if len(valid_indices) == 0:
        return -1
    last_n_indices = valid_indices[-N:]
    if len(last_n_indices) < N:
        return -1
    current_index = len(X) - 1
    bars_since_last_n = current_index - last_n_indices[-1] + 1
    return bars_since_last_n

def ZIG(CLOSE, X=0.05):
    """
    未来函数，计算之字转向。
    用法：ZIG(CLOSE, 0.05) 5%之字转向
    """
    ZIG_STATE_START = 0
    ZIG_STATE_RISE = 1
    ZIG_STATE_FALL = 2
    x = X
    k = CLOSE
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        scan_i += 1
        if scan_i == len(k) - 1:
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i] * (1 - x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i] * (1 + x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i + 1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value) / (peer_end_i - peer_start_i)
        for j in range(peer_end_i - peer_start_i + 1):
            z[j + peer_start_i] = start_value + a * j
    return pd.Series(z)
def calculate_zigzag(data, percent):
    """
    计算ZigZag指标。
    
    参数:
    data : pandas.DataFrame
        包含价格数据的DataFrame，必须包含'High'和'Low'列。
    percent : float
        百分比阈值，用于确定局部高点和低点。
        
    返回:
    zigzag : pandas.Series
        ZigZag指标值。
    """
    # 初始化ZigZag序列
    zigzag = pd.Series(index=data.index)
    
    # 初始方向为向上
    direction = 'up'
    
    # 遍历数据
    for i in range(1, len(data)):
        if direction == 'up':
            if data['high'][i] >= data['high'][i-1] * (1 + percent / 100):
                zigzag[i] = data['high'][i]
                direction = 'down'
            elif data['low'][i] <= data['low'][i-1] * (1 - percent / 100):
                zigzag[i] = data['low'][i]
                direction = 'down'
            else:
                zigzag[i] = zigzag[i-1]
        else:
            if data['low'][i] <= data['low'][i-1] * (1 - percent / 100):
                zigzag[i] = data['low'][i]
                direction = 'up'
            elif data['high'][i] >= data['high'][i-1] * (1 + percent / 100):
                zigzag[i] = data['high'][i]
                direction = 'up'
            else:
                zigzag[i] = zigzag[i-1]
    
    return zigzag

def TROUGHBARS(data, K, N, M):
    """
    计算前M个ZIG转向波谷到当前的周期数。
    
    参数:
    data : pandas.DataFrame
        包含价格数据的DataFrame，必须包含'High'和'Low'列。
    K : int
        百分比阈值，用于计算ZigZag指标。
    N : int
        未使用的参数，保留以符合函数签名。
    M : int
        前M个波谷的数量。
        
    返回:
    result : pandas.Series
        每个周期的前M个波谷到当前的周期数。
    """
    # 计算ZigZag指标
    zigzag = calculate_zigzag(data, K)
    
    # 找到波谷的位置
    valleys = zigzag[zigzag.notna() & (zigzag.shift(1) > zigzag)].index
    
    # 计算每个周期的前M个波谷到当前的周期数
    result = pd.Series(index=data.index)
    for i in range(len(data)):
        if i < len(valleys):
            result[i] = np.nan
        else:
            distances = [i - v for v in valleys[-M:]]
            result[i] = min(distances)
    
    return result
#df,DATE,CLOSE,OPEN,LOW,HIGH,VOL,CAPITAL,HSL,AMOUNT=set_start_data()
def params_data(test='test.txt',to_path='result.txt'):
    '''
    解析通达信公式
    test原来通达信公式文件
    to_path结果文件，python可以直接运行的文件
    '''
    test=open(r'{}'.format(test),'r',encoding='utf-8')
    result=test.readlines()
    columns=[]
    #挑选需要返回的数据
    for i in result:
        if ':' in i and ':=' not in i:
            name_list=i.split(':')
            columns.append(name_list[0])
    text=''.join(result)
    text1=text.replace(':=','=')
    text2=text1.replace(':','=')
    text4=text2.replace('&&',' and ')
    text5=text4.replace('||','or')
    text6=text5.replace('AND','and')
    text7=text6.replace('OR','or')
    text8=text7.replace('NOT','not')
    text9=text8.replace('DRAWNULL','None')
    text10=text9.replace(',NODRAW','')
    text11=text10.replace('MF0>MF1 and MF0>MF2','np.logical_and(MF0>MF1,MF0>MF2)')
    text12=text11.replace('MF0<MF1 and MF0<MF2','np.logical_and(MF0<MF1,MF0<MF2)')
    text3=text12.split(';')
    del text3[-1]
    fill=open(r'{}'.format(to_path),'w+',encoding='utf-8')
    fill.truncate()
    for i in text3:
        try:
            m=i.split('=')
            var=m[0]
            result=m[1]
            fill.write(var +'='+result)
        except:
           fill.write(var +'='+result)
    fill.write('\n')
    fill.write('return {}'.format(','.join(columns)))
    fill.close()
    print('公式分析成功')
def data_to_pandas(func=''):
    '''
    将函数的计算结果数据变成pandas数据,需要自动补充列名称
    func计算公式，例子data_to_pandas(CCI(CLOSE,HIGH,LOW)),CCI函数，也可以计算在返回
    print(data_to_pandas(CCI(CLOSE,HIGH,LOW)))
                   0       
    300          NaN       
    301          NaN       
    302          NaN       
    303          NaN       
    304          NaN       
    ...          ...       
    4634   10.314220       
    4635   68.462799       
    4636  106.677513       
    4637  116.201078       
    4638   85.026126  
    '''
    df=pd.DataFrame(func)
    #自己补充列明，列名称就是返回的参数
    columns=[]
    #df.columns=columns
    df1=df.T
    return df1
def CCI(CLOSE,HIGH,LOW,N=14):
    '''
    超卖超买类
    CCI商品路劲指标
    TYP赋值:(最高价+最低价+收盘价)/3
    输出CCI:(TYP-TYP的N日简单移动平均)*1000/(15*TYP的N日平均绝对偏差)
    '''
    TYP=(HIGH+LOW+CLOSE)/3
    result=(TYP-MA(TYP,N))*1000/(15*AVEDEV(TYP,N))
    return result
def KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3):
    '''
    超卖超买类
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出K:RSV的M1日[1日权重]移动平均
    输出D:K的M2日[1日权重]移动平均
    输出J:3*K-2*D
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M2,1)
    J=3*K-2*D
    return K,D,J
def MFI(CLOSE,HIGH,LOW,VOL,N=14):
    '''
    最近流量指标
    超卖超买类
    赋值: (最高价 + 最低价 + 收盘价)/3
    V1赋值:如果TYP>1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和/如果TYP<1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和
    输出资金流量指标:100-(100/(1+V1))
    '''
    TYP = (HIGH + LOW + CLOSE)/3
    V1=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N)  
    return 100-(100/(1+V1))  
def MTM(CLOSE,N=12,M=6):
    '''
    动量线指标
    超卖超买类
    输出动量线:收盘价-收盘价的有效数据周期数和N的较小值日前的收盘价
    输出MTMMA:MTM的M日简单移动平均
    '''
    MTM=CLOSE-REF(CLOSE,N)
    MTMMA=MA(MTM,M)
    return MTM,MTMMA
def EXPMEMA(data,N=20):
    '''
    data pandas.Series数据
    超卖超买类
    指数平滑移动平均
    '''
    result=data.ewm(com=N).mean()
    return result

def BARSCOUNT(CLOSE):
    df=pd.DataFrame()
    df['数据']=range(len(CLOSE))
    return df['数据']

def RSI(CLOSE, N1=6,N2=12,N3=24):
    '''
    相对强弱指标
    LC赋值:1日前的收盘价
    输出RSI1:收盘价-LC和0的较大值的N1日[1日权重]移动平均/收盘价-LC的绝对值的N1日[1日权重]移动平均*100
    输出RSI2:收盘价-LC和0的较大值的N2日[1日权重]移动平均/收盘价-LC的绝对值的N2日[1日权重]移动平均*100
    输出RSI3:收盘价-LC和0的较大值的N3日[1日权重]移动平均/收盘价-LC的绝对值的N3日[1日权重]移动平均*100
    '''
    LC=REF(CLOSE,1)
    RSI1=SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100
    RSI2=SMA(MAX(CLOSE-LC,0),N2,1)/SMA(ABS(CLOSE-LC),N2,1)*100
    RSI3=SMA(MAX(CLOSE-LC,0),N3,1)/SMA(ABS(CLOSE-LC),N3,1)*100
    return RSI1,RSI2,RSI3
def KD(CLOSE,LOW,HIGH,N=9,M1=3,M2=3):
    '''
    相对强弱指标
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出K:RSV的M1日[1日权重]移动平均
    输出D:K的M2日[1日权重]移动平均
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M2,1)
    return K,D
def SKDJ(CLOSE,LOW,HIGH,N=9,M=3):
    '''
    慢速随机指标
    LOWV赋值:N日内最低价的最低值
    HIGHV赋值:N日内最高价的最高值
    RSV赋值:(收盘价-LOWV)/(HIGHV-LOWV)*100的M日指数移动平均
    输出K:RSV的M日指数移动平均
    输出D:K的M日简单移动平均
    '''
    LOWV=LLV(LOW,N)
    HIGHV=HHV(HIGH,N)
    RSV=EMA((CLOSE-LOWV)/(HIGHV-LOWV)*100,M)
    K=EMA(RSV,M)
    D=MA(K,M)
    return K,D
def UDL(CLOSE,N1=3,N2=5,N3=10,N4=20,M=6):
    '''
    引力线
    输出引力线:(收盘价的N1日简单移动平均+收盘价的N2日简单移动平均+收盘价的N3日简单移动平均+收盘价的N4日简单移动平均)/4
    输出MAUDL:UDL的M日简单移动平均
    '''
    UDL=(MA(CLOSE,N1)+MA(CLOSE,N2)+MA(CLOSE,N3)+MA(CLOSE,N4))/4
    MAUDL=MA(UDL,M)
    return UDL,MAUDL
def WR(CLOSE,LOW,HIGH,N=10,N1=6):
    '''
    威廉指标
    输出WR1:100*(N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)
    输出WR2:100*(N1日内最高价的最高值-收盘价)/(N1日内最高价的最高值-N1日内最低价的最低值)
    '''
    WR1=100*(HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))
    WR2=100*(HHV(HIGH,N1)-CLOSE)/(HHV(HIGH,N1)-LLV(LOW,N1))
    return WR1,WR2
def LWR(CLOSE,LOW,HIGH,N=9,M1=3,M2=3):
    '''
    LWR指标
    RSV赋值: (N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)*100
    输出LWR1:RSV的M1日[1日权重]移动平均
    输出LWR2:LWR1的M2日[1日权重]移动平均
    '''
    RSV= (HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))*100
    LWR1=SMA(RSV,M1,1)
    LWR2=SMA(LWR1,M2,1)
    return LWR1,LWR2
def MEMA(S,N,M=1):
    '''
    平滑移动平均
    '''
    return SMA(S,N,M)
def MARSI(CLOSE,M1=10,M2=6):
    '''
    相对强弱平均线
    DIF赋值:收盘价-1日前的收盘价
    VU赋值:如果DIF>=0,返回DIF,否则返回0
    VD赋值:如果DIF<0,返回-DIF,否则返回0
    MAU1赋值:VU的M1日平滑移动平均
    MAD1赋值:VD的M1日平滑移动平均
    MAU2赋值:VU的M2日平滑移动平均
    '''
    DIF=CLOSE-REF(CLOSE,1)
    VU=IF(DIF>=0,DIF,0)
    VD=IF(DIF<0,-DIF,0)
    MAU1=MEMA(VU,M1)
    MAD1=MEMA(VD,M1)
    MAU2=MEMA(VU,M2)
    MAD2=MEMA(VD,M2)
    RSI1=MA(100*MAU1/(MAU1+MAD1),M1)
    RSI2=MA(100*MAU2/(MAU2+MAD2),M2)
    return RSI1,RSI2
def BIAS_QL(CLOSE,N=6,M=6):
    '''
    乖离率-传统版
    输出乖离率 :(收盘价-收盘价的N日简单移动平均)/收盘价的N日简单移动平均*100
    输出BIASMA :乖离率的M日简单移动平均
    '''
    BIAS=(CLOSE-MA(CLOSE,N))/MA(CLOSE,N)*100
    BIASMA=MA(BIAS,M)
    return BIAS,BIASMA
def BIAS(CLOSE,N1=6,N2=12,N3=24):
    '''
    乖离率
    输出BIAS1 :(收盘价-收盘价的N1日简单移动平均)/收盘价的N1日简单移动平均*100
    输出BIAS2 :(收盘价-收盘价的N2日简单移动平均)/收盘价的N2日简单移动平均*100
    输出BIAS3 :(收盘价-收盘价的N3日简单移动平均)/收盘价的N3日简单移动平均*100
    '''
    BIAS1=(CLOSE-MA(CLOSE,N1))/MA(CLOSE,N1)*100
    BIAS2=(CLOSE-MA(CLOSE,N2))/MA(CLOSE,N2)*100
    BIAS3=(CLOSE-MA(CLOSE,N3))/MA(CLOSE,N3)*100
    return BIAS1,BIAS2,BIAS3
def BIAS36(CLOSE,M=6):
    '''
    三六乖离
    输出三六乖离:收盘价的3日简单移动平均-收盘价的6日简单移动平均
    输出BIAS612:收盘价的6日简单移动平均-收盘价的12日简单移动平均
    输出MABIAS:BIAS36的M日简单移动平均
    '''
    BIAS36=MA(CLOSE,3)-MA(CLOSE,6)
    BIAS612=MA(CLOSE,6)-MA(CLOSE,12)
    MABIAS=MA(BIAS36,M)
    return BIAS36,BIAS612,MABIAS
def ACCER(CLOSE,N=8):
    '''
    幅度涨速
    输出幅度涨速:收盘价的N日线性回归斜率/收盘价
    '''
    ACCER=SLOPE(CLOSE,N)/CLOSE
    return ACCER
#需要编写活力函数
def CYD(CLOSE,CAPITAL,N=21):
    '''
    承接因子
    输出CYDS:以收盘价计算的获利盘比例/(成交量(手)/当前流通股本(手))
    输出CYDN:以收盘价计算的获利盘比例/成交量(手)/当前流通股本(手)的N日简单移动平均
    '''
    CYDS=WINNER(CLOSE)/(VOL/CAPITAL)
    CYDN=WINNER(CLOSE)/MA(VOL/CAPITAL,N);   
    return CYDS,CYDN
def CYF(HSL,N=21):
    '''
    市场能量
    输出市场能量:100-100/(1+换手线的N日指数移动平均)
    '''
    CYF=100-100/(1+EMA(HSL,N))
    return CYF
def SFL(CLOSE,VOL):
    '''
    分水岭
    输出SWL:(收盘价的5日指数移动平均*7+收盘价的10日指数移动平均*3)/10
    输出SWS:以1和100*(成交量(手)的5日累和/(3*当前流通股本(手)))的较大值为权重收盘价的12日指数移动平均的动态移动平均
    '''
    SWL=(EMA(CLOSE,5)*7+EMA(CLOSE,10)*3)/10
    IF(100*(SUM(VOL,5)/(3*CAPITAL)>1),100*(SUM(VOL,5)/(3*CAPITAL)),1)
    SWS=DMA(EMA(CLOSE,12),MAX(1,1))
    return SWL,SWS
def ATR(CLOSE,HIGH,LOW,N=14):
    '''
    真实波幅
    输出MTR:(最高价-最低价)和1日前的收盘价-最高价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值
    输出真实波幅:MTR的N日简单移动平均
    '''
    MTR=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW))
    ATR=MA(MTR,N)
    return MTR,ATR
def DKX(CLOSE,LOW,OPEN,HIGH,M=10):
    '''
    多空线
    MID赋值:(3*收盘价+最低价+开盘价+最高价)/6
    输出多空线:(20*MID+19*1日前的MID+18*2日前的MID+17*3日前的MID+16*4日前的MID+15*5日前的MID+14*6日前的MID+13*7日前的MID+12*8日前的MID+11*9日前的MID+10*10日前的MID+9*11日前的MID+8*12日前的MID+7*13日前的MID+6*14日前的MID+5*15日前的MID+4*16日前的MID+3*17日前的MID+2*18日前的MID+20日前的MID)/210
    输出MADKX:DKX的M日简单移动平均
    '''
    MID=(3*CLOSE+LOW+OPEN+HIGH)/6
    DKX=(20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
    16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
    13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
    10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
    7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
    4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210
    MADKX=MA(DKX,M)
    return DKX,MADKX
#*******************************************
#******************************************
#趋势类型
def ASI(OPEN,CLOSE,HIGH,LOW,M1=26,M2=10):   
    '''
    振动升降指标
    '''        
    LC=REF(CLOSE,1)
    AA=ABS(HIGH-LC)   
    BB=ABS(LOW-LC)
    CC=ABS(HIGH-REF(LOW,1))  
    DD=ABS(LC-REF(OPEN,1))
    R=IF( (AA>BB) & (AA>CC),AA+BB/2+DD/4,IF( (BB>CC) & (BB>AA),BB+AA/2+DD/4,CC+DD/4))
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1))
    SI=16*X/R*MAX(AA,BB)
    ASI=SUM(SI,M1)
    ASIT=MA(ASI,M2)
    return ASI,ASIT  
def CHO(CLOSE,OPEN,LOW,HIGH,VOL,N1=10,N2=20,M=6):
    '''
    佳庆指标
    MID赋值:成交量(手)*(2*收盘价-最高价-最低价)/(最高价+最低价)的历史累和
    输出佳庆指标:MID的N1日简单移动平均-MID的N2日简单移动平均
    输出MACHO:CHO的M日简单移动平均
    '''
    MID=SUM(VOL*(2*CLOSE-HIGH-LOW)/(HIGH+LOW),0)
    CHO=MA(MID,N1)-MA(MID,N2)
    MACHO=MA(CHO,M)
    return CHO,MACHO
def DMA_XT(CLOSE,N1=10,N2=50,M=10):
    '''
    平均差
    输出DIF:收盘价的N1日简单移动平均-收盘价的N2日简单移动平均
    输出DIFMA:DIF的M日简单移动平均
    '''
    DIF=MA(CLOSE,N1)-MA(CLOSE,N2)
    DIFMA=MA(DIF,M)
    return DIF,DIFMA
def DMI(CLOSE,HIGH,LOW,N=14,M=6):
    '''
    趋向指标
    MTR赋值:最高价-最低价和最高价-1日前的收盘价的绝对值的较大值和1日前的收盘价-最低价的绝对值的较大值的N日累和
    赋值:最高价-1日前的最高价
    赋值:1日前的最低价-最低价
    DMP赋值:如果HD>0并且HD>LD,返回HD,否则返回0的N日累和
    DMM赋值:如果LD>0并且LD>HD,返回LD,否则返回0的N日累和
    输出PDI: DMP*100/MTR
    输出MDI: DMM*100/MTR
    输出ADX: MDI-PDI的绝对值/(MDI+PDI)*100的M日简单移动平均
    输出ADXR:(ADX+M日前的ADX)/2
    '''
    MTR=SUM(MAX(MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1))),ABS(REF(CLOSE,1)-LOW)),N)
    HD =HIGH-REF(HIGH,1)
    LD =REF(LOW,1)-LOW
    list_A=[]
    list_B=[]
    for m,n in zip(LD>0,LD>HD):
        if m==n and m==True:
            list_A.append(True)
        else:
            list_A.append(False)
    for i,j in zip(LD>0,LD>HD):
        if i==j and i==True:
            list_B.append(True)
        else:
            list_B.append(False)
    DMP=SUM(IF(list_A,HD,0),N)
    DMM=SUM(IF(list_B,LD,0),N)
    PDI= DMP*100/MTR
    MDI=DMM*100/MTR
    ADX=MA(ABS(MDI-PDI)/(MDI+PDI)*100,M)
    ADXR=(ADX+REF(ADX,M))/2
    return PDI,MDI,ADX,ADXR
def DPO(CLOSE,N=21,M=6):
    '''
    区间震荡线
    输出区间震荡线:收盘价-N/2+1日前的收盘价的N日简单移动平均
    输出MADPO:DPO的M日简单移动平均
    '''
    #print(REF(MA(CLOSE,N),N/2))
    DPO=CLOSE-REF(MA(CLOSE,7),6)
    MADPO=MA(DPO,M)
    return DPO,MADPO
def EMV(HIGH,LOW,VOL,N=14,M=9):
    '''
    简易波动指标
    VOLUME赋值:成交量(手)的N日简单移动平均/成交量(手)
    MID赋值:100*(最高价+最低价-1日前的最高价+最低价)/(最高价+最低价)
    输出EMV:MID*VOLUME*(最高价-最低价)/最高价-最低价的N日简单移动平均的N日简单移动平均
    输出MAEMV:EMV的M日简单移动平均
    '''
    VOLUME=MA(VOL,N)/VOL
    MID=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW)
    EMV=MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N)
    MAEMV=MA(EMV,M)
    return EMV,MAEMV
def MACD(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    平滑异同平均线
    输出DIF:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:(DIF-DEA)*2,COLORSTICK
    '''
    DIF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIF,MID)
    MACD=(DIF-DEA)*2
    return DIF,DEA,MACD

def VMACD(VOL,SHORT=12,LONG=26,MID=9):
    '''
    量平滑异同平均线
    输出DIF:成交量(手)的SHORT日指数移动平均-成交量(手)的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:DIF-DEA,COLORSTICK
    '''
    DIF=EMA(VOL,SHORT)-EMA(VOL,LONG)
    DEA=EMA(DIF,MID)
    MACD=DIF-DEA
    return DIF,DEA,MACD
def SMACD(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    单线平滑异同平均线
    DIF赋值:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    输出DEA:DIF的MID日指数移动平均
    输出平滑异同平均线:DIF,COLORSTICK
    '''
    DIF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIF,MID)
    MACD=DIF
    return DEA,MACD
def QACD(CLOSE,N1=12,N2=12,M=9):
    '''
    快速异同平均线
    输出DIF:收盘价的N1日指数移动平均-收盘价的N2日指数移动平均
    输出平滑异同平均线:DIF的M日指数移动平均
    输出DDIF:DIF-MACD
    '''
    DIF=EMA(CLOSE,N1)-EMA(CLOSE,N2)
    MACD=EMA(DIF,M)
    DDIF=DIF-MACD
    return DIF,MACD,DDIF
def TRIX(CLOSE,N=12,M=9):
    '''
    三重指数平均线
    MTR赋值:收盘价的N日指数移动平均的N日指数移动平均的N日指数移动平均
    输出三重指数平均线:(MTR-1日前的MTR)/1日前的MTR*100
    输出MATRIX:TRIX的M日简单移动平均 
    '''
    MTR=EMA(EMA(EMA(CLOSE,N),N),N)
    TRIX=(MTR-REF(MTR,1))/REF(MTR,1)*100
    MATRIX=MA(TRIX,M) 
    return TRIX,MATRIX
def UOS(CLOSE,HIGH,LOW,N1=7,N2=14,N3=28,M=6):
    '''
    终极指标
    TH赋值:最高价和1日前的收盘价的较大值
    TL赋值:最低价和1日前的收盘价的较小值
    ACC1赋值:收盘价-TL的N1日累和/TH-TL的N1日累和
    ACC2赋值:收盘价-TL的N2日累和/TH-TL的N2日累和
    ACC3赋值:收盘价-TL的N3日累和/TH-TL的N3日累和
    输出终极指标:(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3)
    输出MAUOS:UOS的M日指数平滑移动平均
    '''
    TH=MAX(HIGH,REF(CLOSE,1))
    TL=MIN(LOW,REF(CLOSE,1))
    ACC1=SUM(CLOSE-TL,N1)/SUM(TH-TL,N1)
    ACC2=SUM(CLOSE-TL,N2)/SUM(TH-TL,N2)
    ACC3=SUM(CLOSE-TL,N3)/SUM(TH-TL,N3)
    UOS=(ACC1*N2*N3+ACC2*N1*N3+ACC3*N1*N2)*100/(N1*N2+N1*N3+N2*N3)
    MAUOS=EXPMEMA(pd.Series(UOS),M)
    return UOS,np.array(MAUOS)
def VTP(CLOSE,VOL,N=51,M=6):
    '''
    量价曲线
    输出量价曲线:成交量(手)*(收盘价-1日前的收盘价)/1日前的收盘价的N日累和
    输出MAVPT:VPT的M日简单移动平均
    '''
    VPT=SUM(VOL*(CLOSE-REF(CLOSE,1))/REF(CLOSE,1),N)
    MAVP=MA(VPT,M)
    return VPT,MAVP
def WVAD(CLOSE,OPEN,HIGH,LOW,VOL,N=24,M=6):
    '''
    威廉变异离散量
    输出WVAD:(收盘价-开盘价)/(最高价-最低价)*成交量(手)的N日累和/10000
    输出MAWVAD:WVAD的M日简单移动平均
    '''
    WVAD=SUM((CLOSE-OPEN)/(HIGH-LOW)*VOL,N)/10000
    MAWVAD=MA(WVAD,M)
    return WVAD,MAWVAD
def DBQR(CLOSE,INDEXC,N=5,M1=10,M2=20,M3=60):
    '''
    对比强弱(需下载日线)
    输出ZS:(大盘的收盘价-N日前的大盘的收盘价)/N日前的大盘的收盘价
    输出GG:(收盘价-N日前的收盘价)/N日前的收盘价
    输出MADBQR1:GG的M1日简单移动平均
    输出MADBQR2:GG的M2日简单移动平均
    输出MADBQR3:GG的M3日简单移动平均
    '''
    ZS=(INDEXC-REF(INDEXC,N))/REF(INDEXC,N)
    GG=(CLOSE-REF(CLOSE,N))/REF(CLOSE,N)
    MADBQR1=MA(GG,M1)
    MADBQR2=MA(GG,M2)
    MADBQR3=MA(GG,M3)
    return ZS,GG,MADBQR1,MADBQR2,MADBQR3
def JS(CLOSE,N=5,M1=5,M2=10,M3=20):
    '''
    加数线
    输出加速线:100*(收盘价-N日前的收盘价)/(N*N日前的收盘价)
    输出MAJS1:JS的M1日简单移动平均
    输出MAJS2:JS的M2日简单移动平均
    输出MAJS3:JS的M3日简单移动平均
    '''
    JS=100*(CLOSE-REF(CLOSE,N))/(N*REF(CLOSE,N))
    MAJS1=MA(JS,M1)
    MAJS2=MA(JS,M2)
    MAJS3=MA(JS,M3)
    return JS,MAJS1,MAJS2,MAJS3
def CYE(CLOSE):
    '''
    市场趋势
    MAL赋值:收盘价的5日简单移动平均
    MAS赋值:收盘价的20日简单移动平均的5日简单移动平均
    输出CYEL:(MAL-1日前的MAL)/1日前的MAL*100
    输出CYES:(MAS-1日前的MAS)/1日前的MAS*100
    '''
    MAL=MA(CLOSE,5)
    MAS=MA(MA(CLOSE,20),5)
    CYEL=(MAL-REF(MAL,1))/REF(MAL,1)*100
    CYES=(MAS-REF(MAS,1))/REF(MAS,1)*100
    return CYEL,CYES
def QR(CLOSE,INDEXC,N=21):
    '''
    强弱指标(需下载日线)
    NN赋值:收盘价的有效数据周期数和N的较小值
    输出 个股: (收盘价-NN日前的收盘价)/NN日前的收盘价*100
    输出 大盘: (大盘的收盘价-NN日前的大盘的收盘价)/NN日前的大盘的收盘价*100
    输出 强弱值:个股-大盘的2日指数移动平均,COLORSTICK
    '''
    NN=MIN(BARSCOUNT(CLOSE),N)
    GG=(CLOSE-REF(CLOSE,NN))/REF(CLOSE,NN)*100
    DP=(INDEXC-REF(INDEXC,NN))/REF(INDEXC,NN)*100
    value=EMA(GG-DP,2)
    return GG,DP,value
def GDX(CLOSE,HIGH,LOW,N=30,M=9):
    '''
    轨道线
    AA赋值:(2*收盘价+最高价+最低价)/4-收盘价的N日简单移动平均的绝对值/收盘价的N日简单移动平均
    输出 轨道:以AA为权重收盘价的动态移动平均
    输出压力线:(1+M/100)*轨道
    输出 支撑线:(1-M/100)*轨道
    '''
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N)
    轨道 =DMA(AA,0.5)
    压力线=(1+M/100)*轨道 
    支撑线=(1-M/100)*轨道
    return 轨道,压力线,支撑线
def JLHB(CLOSE,LOW,HIGH,N=7,M=5):
    '''
    绝路航标
    VAR1赋值:(收盘价-60日内最低价的最低值)/(60日内最高价的最高值-60日内最低价的最低值)*80
    输出 B:VAR1的N日[1日权重]移动平均
    输出 VAR2:B的M日[1日权重]移动平均
    输出 绝路航标:如果B上穿VAR2ANDB<40,返回50,否则返回0
    '''
    VAR1=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80
    B=SMA(VAR1,N,1)
    VAR2=SMA(B,M,1)
    绝路航标=IF(np.logical_and(B,VAR2),50,0)
    return B,VAR2,绝路航标
#********************************************
#********************************************
#能量类型
def BRAR(OPEN,HIGH,LOW,CLOSE,N=26):
    '''
    情绪指标
    输出BR:0和最高价-1日前的收盘价的较大值的N日累和/0和1日前的收盘价-最低价的较大值的N日累和*100
    输出AR:最高价-开盘价的N日累和/开盘价-最低价的N日累和*100
    '''
    BR=SUM(MAX(0,HIGH-REF(CLOSE,1)),N)/SUM(MAX(0,REF(CLOSE,1)-LOW),N)*100
    AR=SUM(HIGH-OPEN,N)/SUM(OPEN-LOW,N)*100
    return BR,AR
def CR(HIGH,LOW,N=26,M1=10,M2=20,M3=40,M4=60):
    '''
    带状能量线
    MID赋值:1日前的最高价+最低价/2
    输出带状能量线:0和最高价-MID的较大值的N日累和/0和MID-最低价的较大值的N日累和*100
    输出MA1:M1/2.5+1日前的CR的M1日简单移动平均
    输出均线:M2/2.5+1日前的CR的M2日简单移动平均
    输出MA3:M3/2.5+1日前的CR的M3日简单移动平均
    输出MA4:M4/2.5+1日前的CR的M4日简单移动平均
    '''
    MID=REF(HIGH+LOW,1)/2
    CR=SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100
    MA1=pd.DataFrame(CR).shift(11).mean()
    MA2=pd.DataFrame(CR).shift(5).mean()
    MA3=pd.DataFrame(CR).shift(17).mean()
    MA4=pd.DataFrame(CR).shift(25).mean()
    return CR,MA1,MA2,MA3,MA4
def MASS(HIGH,LOW,N1=9,N2=25,M=6):
    '''
    梅斯线
    输出梅斯线:最高价-最低价的N1日简单移动平均/最高价-最低价的N1日简单移动平均的N1日简单移动平均的N2日累和
    输出MAMASS:MASS的M日简单移动平均
    '''
    MASS=SUM(MA(HIGH-LOW,N1)/MA(MA(HIGH-LOW,N1),N1),N2)
    MAMASS=MA(MASS,M)
    return MASS,MAMASS
def PSY(CLOSE,N=12,M=6):
    '''
    心理线
    输出PSY:统计N日中满足收盘价>1日前的收盘价的天数/N*100
    输出PSYMA:PSY的M日简单移动平均
    '''
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return PSY,PSYMA
def VR(CLOSE,VOL,N=26,M=6):
    '''
    成交量变异率
    TH赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回0的N日累和
    TL赋值:如果收盘价<1日前的收盘价,返回成交量(手),否则返回0的N日累和
    TQ赋值:如果收盘价=1日前的收盘价,返回成交量(手),否则返回0的N日累和
    输出VR:100*(TH*2+TQ)/(TL*2+TQ)
    输出MAVR:VR的M日简单移动平均
    '''
    TH=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N)
    TL=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N)
    TQ=SUM(IF(CLOSE==REF(CLOSE,1),VOL,0),N)
    VR=100*(TH*2+TQ)/(TL*2+TQ)
    MAVR=MA(VR,M)
    return VR,MAVR
def WAD(CLOSE,LOW,HIGH,M=30):
    '''
    威廉多空力度线
    MIDA赋值:收盘价-1日前的收盘价和最低价的较小值
    MIDB赋值:如果收盘价<1日前的收盘价,返回收盘价-1日前的收盘价和最高价的较大值,否则返回0
    输出威廉多空力度线:如果收盘价>1日前的收盘价,返回MIDA,否则返回MIDB的历史累和
    输出MAWAD:WAD的M日简单移动平均
    '''
    MIDA=CLOSE-MIN(REF(CLOSE,1),LOW)
    MIDB=IF(CLOSE<REF(CLOSE,1),CLOSE-MAX(REF(CLOSE,1),HIGH),0)
    WAD=SUM(IF(CLOSE>REF(CLOSE,1),MIDA,MIDB),0)
    MAWAD=MA(WAD,M)
    return WAD,MAWAD
def EXPMEMA(CLOSE,M=5):
    '''
    指数平滑
    '''
    return pd.Series(CLOSE).ewm(span=M, adjust=False).mean().values
def PCNT(CLOSE,M=5):
    '''
    输出幅度比:(收盘价-1日前的收盘价)/收盘价*100
    输出MAPCNT:PCNT的M日指数平滑移动平均
    '''
    PCNT=(CLOSE-REF(CLOSE,1))/CLOSE*100
    MAPCNT=EXPMEMA(PCNT,M)
    return PCNT,MAPCNT
def CYR(AMOUNT,VOL,N=13,M=5):
    '''
    市场强弱
    AMOUNT成交量=price*volume
    DIVE赋值:0.01*成交额(元)的N日指数移动平均/成交量(手)的N日指数移动平均
    输出市场强弱:(DIVE/1日前的DIVE-1)*100
    输出MACYR:CYR的M日简单移动平均
    '''
    DIVE=0.01*EMA(AMOUNT,N)/EMA(VOL,N)
    CYR=(DIVE/REF(DIVE,1)-1)*100
    MACYR=MA(CYR,M)
    return CYR,MACYR
#*********************************************
#*********************************************
#能量型
def AMO(AMOUNT,M1=5,M2=10):
    '''
    成交金额
    输出AMOW:成交额(元)/10000.0,VOLSTICK
    输出AMO1:AMOW的M1日简单移动平均
    输出AMO2:AMOW的M2日简单移动平均
    '''
    AMOW=AMOUNT/10000.0
    AMO1=MA(AMOW,M1)
    AMO2=MA(AMOW,M2)
    return AMOW,AMO1,AMO2
def OBV(VOL,CLOSE,M=30):
    '''
    累积能量线
    VA赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回-成交量(手)
    输出OBV:如果收盘价=1日前的收盘价,返回0,否则返回VA的历史累和
    输出MAOBV:OBV的M日简单移动平均
    '''
    VA=IF(CLOSE>REF(CLOSE,1),VOL,-VOL)
    OBV=SUM(IF(CLOSE==REF(CLOSE,1),0,VA),0)
    MAOBV=MA(OBV,M)
    return OBV,MAOBV
def VOL_XT(VOL,M1=5,M2=10):
    '''
    成交量
    输出VOLUME:成交量(手),VOLSTICK
    输出MAVOL1:VOLUME的M1日简单移动平均
    输出MAVOL2:VOLUME的M2日简单移动平均
    '''
    VOLUME=VOL
    MAVOL1=MA(VOLUME,M1)
    MAVOL2=MA(VOLUME,M2)
    return MAVOL1,MAVOL2
def VRSI(VOL,N1=6,N2=12,N3=24):
    '''
    相对强弱量
    LC赋值:1日前的成交量(手)
    输出RSI1:成交量(手)-LC和0的较大值的N1日[1日权重]移动平均/成交量(手)-LC的绝对值的N1日[1日权重]移动平均*100
    输出RSI2:成交量(手)-LC和0的较大值的N2日[1日权重]移动平均/成交量(手)-LC的绝对值的N2日[1日权重]移动平均*100
    输出RSI3:成交量(手)-LC和0的较大值的N3日[1日权重]移动平均/成交量(手)-LC的绝对值的N3日[1日权重]移动平均*100
    '''
    LC=REF(VOL,1)
    RSI1=SMA(MAX(VOL-LC,0),N1,1)/SMA(ABS(VOL-LC),N1,1)*100
    RSI2=SMA(MAX(VOL-LC,0),N2,1)/SMA(ABS(VOL-LC),N2,1)*100
    RSI3=SMA(MAX(VOL-LC,0),N3,1)/SMA(ABS(VOL-LC),N3,1)*100
    return RSI1,RSI2,RSI3
def HSL(HSL,N=5):
    '''
    换手线
    '''
    HSL=HSL
    MAHSL=MA(HSL,N)
    return HSL,MAHSL
#******************************************
#******************************************
#均线系统
def MA_XT(CLOSE,M1=5,M2=10,M3=20,M4=60):
    '''
    均线
    输出MA1:收盘价的M1日简单移动平均
    输出均线:收盘价的M2日简单移动平均
    输出MA3:收盘价的M3日简单移动平均
    输出MA4:收盘价的M4日简单移动平均
    输出MA5:收盘价的M5日简单移动平均
    输出MA6:收盘价的M6日简单移动平均
    输出MA7:收盘价的M7日简单移动平均
    输出MA8:收盘价的M8日简单移动平均
    '''
    MA1=MA(CLOSE,M1)
    MA2=MA(CLOSE,M2)
    MA3=MA(CLOSE,M3)
    MA4=MA(CLOSE,M4)
    return MA1,MA2,MA3,MA4
def MA2(CLOSE,M1=5,M2=10,M3=20,M4=60,M5=120,M6=240,M7=360,M8=420,M9=680,M10=720):
    '''
    均线2
    输出MA1:收盘价的M1日简单移动平均
    输出均线:收盘价的M2日简单移动平均
    输出MA3:收盘价的M3日简单移动平均
    输出MA4:收盘价的M4日简单移动平均
    输出MA5:收盘价的M5日简单移动平均
    输出MA6:收盘价的M6日简单移动平均
    输出MA7:收盘价的M7日简单移动平均
    输出MA8:收盘价的M8日简单移动平均
    输出MA9:收盘价的M9日简单移动平均
    输出MA10:收盘价的M10日简单移动平均
    '''
    MA1=MA(CLOSE,M1)
    MA2=MA(CLOSE,M2)
    MA3=MA(CLOSE,M3)
    MA4=MA(CLOSE,M4)
    MA5=MA(CLOSE,M5)
    MA6=MA(CLOSE,M6)
    MA7=MA(CLOSE,M7)
    MA8=MA(CLOSE,M8)
    MA9=MA(CLOSE,M9)
    MA10=MA(CLOSE,M10)
    return MA1,MA2,MA3,MA4,MA5,MA6,MA7,MA8,MA8,MA9,MA10
def ACD(CLOSE,HIGH,LOW,M=20):
    '''
    升降线
    LC赋值:1日前的收盘价
    DIF赋值:收盘价-如果收盘价>LC,返回最低价和LC的较小值,否则返回最高价和LC的较大值
    输出升降线:如果收盘价=LC,返回0,否则返回DIF的历史累和
    输出MAACD:ACD的M日指数平滑移动平均
    '''
    LC=REF(CLOSE,1)
    DIF=CLOSE-IF(CLOSE>LC,MIN(LOW,LC),MAX(HIGH,LC))
    ACD=SUM(IF(CLOSE==LC,0,DIF),0)
    MAACD=EXPMEMA(ACD,M)
    return ACD,MAACD
def BBI(CLOSE,M1=3,M2=6,M3=12,M4=24):
    '''
    多空均线
    输出多空均线:(收盘价的M1日简单移动平均+收盘价的M2日简单移动平均+收盘价的M3日简单移动平均+收盘价的M4日简单移动平均)/4
    '''
    BBI=(MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4
    return BBI
def EXPMA(CLOSE,M1=12,M2=50):
    '''
    指数平均线
    输出EXP1:收盘价的M1日指数移动平均
    输出EXP2:收盘价的M2日指数移动平均
    '''
    EXP1=EMA(CLOSE,M1)
    EXP2=EMA(CLOSE,M2)
    return EXP1,EXP2
def HMA(HIGH,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    高价平均线
    输出HMA1:最高价的M1日简单移动平均
    输出HMA2:最高价的M2日简单移动平均
    输出HMA3:最高价的M3日简单移动平均
    输出HMA4:最高价的M4日简单移动平均
    输出HMA5:最高价的M5日简单移动平均
    '''
    HMA1=MA(HIGH,M1)
    HMA2=MA(HIGH,M2)
    HMA3=MA(HIGH,M3)
    HMA4=MA(HIGH,M4)
    HMA5=MA(HIGH,M5)
    return HMA1,HMA2,HMA3,HMA4,HMA5
def LMA(LOW,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    低价平均线
    输出LMA1:最低价的M1日简单移动平均
    输出LMA2:最低价的M2日简单移动平均
    输出LMA3:最低价的M3日简单移动平均
    输出LMA4:最低价的M4日简单移动平均
    输出LMA5:最低价的M5日简单移动平均
    '''
    LMA1=MA(LOW,M1)
    LMA2=MA(LOW,M2)
    LMA3=MA(LOW,M3)
    LMA4=MA(LOW,M4)
    LMA5=MA(LOW,M5)
    return LMA1,LMA2,LMA3,LMA4,LMA5
def VMA(HIGH,OPEN,LOW,CLOSE,M1=6,M2=12,M3=30,M4=70,M5=90):
    '''
    变异平均线
    VV赋值:(最高价+开盘价+最低价+收盘价)/4
    输出VMA1:VV的M1日简单移动平均
    输出VMA2:VV的M2日简单移动平均
    输出VMA3:VV的M3日简单移动平均
    输出VMA4:VV的M4日简单移动平均
    输出VMA5:VV的M5日简单移动平均
    '''
    VV=(HIGH+OPEN+LOW+CLOSE)/4
    VMA1=MA(VV,M1)
    VMA2=MA(VV,M2)
    VMA3=MA(VV,M3)
    VMA4=MA(VV,M4)
    VMA5=MA(VV,M5)
    return VMA1,VMA2,VMA3,VMA4,VMA5
def AMV(OPEN,CLOSE,VOL,M1=5,M2=13,M3=34,M4=60):
    '''
    成本均线
    AMOV赋值:成交量(手)*(开盘价+收盘价)/2
    输出AMV1:AMOV的M1日累和/成交量(手)的M1日累和
    输出AMV2:AMOV的M2日累和/成交量(手)的M2日累和
    输出AMV3:AMOV的M3日累和/成交量(手)的M3日累和
    输出AMV4:AMOV的M4日累和/成交量(手)的M4日累和
    '''
    AMOV=VOL*(OPEN+CLOSE)/2
    AMV1=SUM(AMOV,M1)/SUM(VOL,M1)
    AMV2=SUM(AMOV,M2)/SUM(VOL,M2)
    AMV3=SUM(AMOV,M3)/SUM(VOL,M3)
    AMV4=SUM(AMOV,M4)/SUM(VOL,M4)
    return AMV1,AMV2,AMV3,AMV4
def BBIBOLL(CLOSE,N=11,M=6):
    '''
    多空布林线
    CV赋值:收盘价
    输出多空布林线:(CV的3日简单移动平均+CV的6日简单移动平均+CV的12日简单移动平均+CV的24日简单移动平均)/4
    输出UPR:BBIBOLL+M*BBIBOLL的N日估算标准差
    输出DWN:BBIBOLL-M*BBIBOLL的N日估算标准差
    '''
    CV=CLOSE
    BBIBOLL=(MA(CV,3)+MA(CV,6)+MA(CV,12)+MA(CV,24))/4
    UPR=BBIBOLL+M*STD(BBIBOLL,N)
    DWN=BBIBOLL-M*STD(BBIBOLL,N)
    return BBIBOLL,UPR,DWN
def ALLIGAT(HIGH,LOW):
    '''
    鳄鱼线
    NN赋值:(最高价+最低价)/2
    输出上唇:3日前的NN的5日简单移动平均,COLOR40FF40
    输出牙齿:5日前的NN的8日简单移动平均,COLOR0000C0
    输出下颚:8日前的NN的13日简单移动平均,COLORFF4040
    '''
    H=HIGH
    L=LOW
    NN=(H+L)/2
    上唇=REF(MA(NN,5),3)
    牙齿=REF(MA(NN,8),5)
    下颚=REF(MA(NN,13),8)
    return 上唇,牙齿,下颚
def GMMA(CLOSE):
    '''
    顾比均线
    '''
    MA3=EMA(CLOSE,3)
    MA5=EMA(CLOSE,5)
    MA8=EMA(CLOSE,8)
    MA10=EMA(CLOSE,10)
    MA12=EMA(CLOSE,12)
    MA15=EMA(CLOSE,15)
    MA30=EMA(CLOSE,30)
    MA35=EMA(CLOSE,35)
    MA40=EMA(CLOSE,40)
    MA45=EMA(CLOSE,45)
    MA50=EMA(CLOSE,50)
    MA60=EMA(CLOSE,60)
    return MA3,MA5,MA8,MA10,MA12,MA15,MA30,MA35,MA40,MA45,MA50,MA60
#*******************************************
#*******************************************
#路径类
def BOLL(CLOSE,M=20):
    '''
    布林线
    输出BOLL:收盘价的M日简单移动平均
    输出UB:BOLL+2*收盘价的M日估算标准差
    输出LB:BOLL-2*收盘价的M日估算标准差
    '''
    BOLL=MA(CLOSE,M)
    UB=BOLL+2*STD(CLOSE,M)
    LB=BOLL-2*STD(CLOSE,M)
    return BOLL,UB,LB
def PBX(CLOSE,M1=4,M2=6,M3=9,M4=13,M5=18,M6=24):
    '''
    瀑布线
    输出PBX1:(收盘价的M1日指数移动平均+收盘价的M1*2日简单移动平均+收盘价的M1*4日简单移动平均)/3
    输出PBX2:(收盘价的M2日指数移动平均+收盘价的M2*2日简单移动平均+收盘价的M2*4日简单移动平均)/3
    输出PBX3:(收盘价的M3日指数移动平均+收盘价的M3*2日简单移动平均+收盘价的M3*4日简单移动平均)/3
    输出PBX4:(收盘价的M4日指数移动平均+收盘价的M4*2日简单移动平均+收盘价的M4*4日简单移动平均)/3
    输出PBX5:(收盘价的M5日指数移动平均+收盘价的M5*2日简单移动平均+收盘价的M5*4日简单移动平均)/3
    输出PBX6:(收盘价的M6日指数移动平均+收盘价的M6*2日简单移动平均+收盘价的M6*4日简单移动平均)/3
    '''
    PBX1=(EMA(CLOSE,M1)+MA(CLOSE,M1*2)+MA(CLOSE,M1*4))/3
    PBX2=(EMA(CLOSE,M2)+MA(CLOSE,M2*2)+MA(CLOSE,M2*4))/3
    PBX3=(EMA(CLOSE,M3)+MA(CLOSE,M3*2)+MA(CLOSE,M3*4))/3
    PBX4=(EMA(CLOSE,M4)+MA(CLOSE,M4*2)+MA(CLOSE,M4*4))/3
    PBX5=(EMA(CLOSE,M5)+MA(CLOSE,M5*2)+MA(CLOSE,M5*4))/3
    PBX6=(EMA(CLOSE,M6)+MA(CLOSE,M6*2)+MA(CLOSE,M6*4))/3
    return PBX1,PBX2,PBX3,PBX4,PBX5,PBX6
def ENE(CLOSE,N=25,M1=6,M2=6):
    '''
    轨道线
    输出UPPER:(1+M1/100)*收盘价的N日简单移动平均
    输出LOWER:(1-M2/100)*收盘价的N日简单移动平均
    输出轨道线:(UPPER+LOWER)/2
    '''
    UPPER=(1+M1/100)*MA(CLOSE,N)
    LOWER=(1-M2/100)*MA(CLOSE,N)
    ENE=(UPPER+LOWER)/2
    return UPPER,LOWER,ENE
def MIKE(HIGH,LOW,CLOSE,N=10):
    '''
    麦克支撑压力
    HLC赋值:1日前的(最高价+最低价+收盘价)/3的N日简单移动平均
    HV赋值:N日内最高价的最高值的3日指数移动平均
    LV赋值:N日内最低价的最低值的3日指数移动平均
    输出STOR:2*HV-LV的3日指数移动平均
    输出MIDR:HLC+HV-LV的3日指数移动平均
    输出WEKR:HLC*2-LV的3日指数移动平均
    '''
    HLC=REF(MA((HIGH+LOW+CLOSE)/3,N),1)
    HV=EMA(HHV(HIGH,N),3)
    LV=EMA(LLV(LOW,N),3)
    STOR=EMA(2*HV-LV,3)
    MIDR=EMA(HLC+HV-LV,3)
    WEKR=EMA(HLC*2-LV,3)
    WEKS=EMA(HLC*2-HV,3)
    MIDS=EMA(HLC-HV+LV,3)
    STOS=EMA(2*LV-HV,3)
    return STOR,MIDR,WEKR,WEKS,MIDS,STOS
def XS(CLOSE,VOL,N=13):
    '''
    薛斯通道
    VAR2赋值:收盘价*成交量(手)
    VAR3赋值:(VAR2的3日指数移动平均/成交量(手)的3日指数移动平均+VAR2的6日指数移动平均/成交量(手)的6日指数移动平均+VAR2的12日指数移动平均/成交量(手)的12日指数移动平均+VAR2的24日指数移动平均/成交量(手)的24日指数移动平均)/4的N日指数移动平均
    输出SUP:1.06*VAR3
    输出SDN:VAR3*0.94
    VAR4赋值:收盘价的9日指数移动平均
    输出LUP:VAR4*1.14的5日指数移动平均
    输出LDN:VAR4*0.86的5日指数移动平均
    '''
    VAR2=CLOSE*VOL
    VAR3=EMA((EMA(VAR2,3)/EMA(VOL,3)+EMA(VAR2,6)/EMA(VOL,6)+EMA(VAR2,12)/EMA(VOL,12)+EMA(VAR2,24)/EMA(VOL,24))/4,N)
    SUP=1.06*VAR3
    SDN=VAR3*0.94
    VAR4=EMA(CLOSE,9)
    LUP=EMA(VAR4*1.14,5)
    LDN=EMA(VAR4*0.86,5)
    return SUP,SDN,LUP,LDN
def XS2(CLOSE,HIGH,LOW,N=102,M=7):
    '''
    薛斯通道II
    AA赋值:(2*收盘价+最高价+最低价)/4的5日简单移动平均
    输出 通道1:AA*N/100
    输出 通道2:AA*(200-N)/100
    CC赋值:(2*收盘价+最高价+最低价)/4-收盘价的20日简单移动平均的绝对值/收盘价的20日简单移动平均
    DD赋值:以CC为权重收盘价的动态移动平均
    输出 通道3:(1+M/100)*DD
    '''
    AA=MA((2*CLOSE+HIGH+LOW)/4,5)
    通道1=AA*N/100
    通道2=AA*(200-N)/100
    CC=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,20))/MA(CLOSE,20)
    DD=DMA(CLOSE,0.5)
    通道3=(1+M/100)*DD
    通道4=(1-M/100)*DD
    return 通道1,通道2,通道3,通道4
def TQN(HIGH, LOW, X1=20, X2=20):
    '''
    唐奇安通道
    输出周期高点:1日前的X1日内最高价的最高值
    输出周期低点:1日前的X2日内最低价的最低值
    平空开多赋值:最高价>=周期高点
    平多开空赋值:最低价<=周期低点
    先平空仓再开多仓
    先平多仓再开空仓
    自动过滤交易信号
    '''
    # 计算周期高点：X1日内最高价的最高值，然后取1日前的值
    周期高点 = REF(HHV(HIGH, X1), 1)
    
    # 计算周期低点：X2日内最低价的最低值，然后取1日前的值
    周期低点 = REF(LLV(LOW, X2), 1)
    
    # 平空开多信号：最高价 >= 周期高点
    平空开多 = HIGH >= 周期高点
    
    # 平多开空信号：最低价 <= 周期低点
    平多开空 = LOW <= 周期低点
    
    return 周期高点, 周期低点, 平空开多, 平多开空
#*******************************************
#*******************************************
def SAR(HIGH, LOW, M=10, af=2, amax=20):
    '''
    抛物线指标
    '''
    af = af / 100
    amax = amax / 100
    
    # 转换为numpy数组，处理NaN
    high = np.array(HIGH, dtype=float)
    low = np.array(LOW, dtype=float)
    
    # 检查数据有效性
    if len(high) == 0 or np.isnan(high).all() or np.isnan(low).all():
        return pd.Series([np.nan] * len(HIGH))
    
    # 替换NaN为有效值（用前向填充或均值）
    high_clean = pd.Series(high).fillna(method='ffill').fillna(method='bfill').values
    low_clean = pd.Series(low).fillna(method='ffill').fillna(method='bfill').values
    
    n = len(high_clean)
    
    # 初始化结果数组
    sar = np.full(n, np.nan)
    
    # 需要至少 M+1 个数据点
    if n < M + 1:
        return pd.Series(sar, index=HIGH.index if hasattr(HIGH, 'index') else None)
    
    # 计算标准差，处理0值
    hl_std = np.std(high_clean - low_clean)
    if hl_std == 0 or np.isnan(hl_std):
        hl_std = 0.001  # 设置一个极小值避免除零
    
    # 起始值
    sig0 = True
    xpt0 = high_clean[M - 1] if M > 0 else high_clean[0]
    af0 = af
    
    # 第一个SAR值
    sar[0] = low_clean[0] - hl_std
    
    for i in range(1, n):
        sig1 = sig0
        xpt1 = xpt0
        af1 = af0
        
        if i < M:
            # 前M个数据点使用简单方式
            if i > 0:
                sar[i] = sar[i-1] + (xpt1 - sar[i-1]) * af1
            continue
        
        # 获取当前和前一个的高低点
        lmin = min(low_clean[i-1], low_clean[i])
        lmax = max(high_clean[i-1], high_clean[i])
        
        # 判断趋势方向
        if sig1:
            sig0 = low_clean[i] > sar[i-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high_clean[i] >= sar[i-1]
            xpt0 = min(lmin, xpt1)
        
        # 计算SAR值
        if sig0 == sig1:
            sari = sar[i-1] + (xpt1 - sar[i-1]) * af1
            af0 = min(amax, af1 + af)
            
            if sig0:
                af0 = af0 if xpt0 > xpt1 else af1
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 < xpt1 else af1
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0
        
        sar[i] = sari
    
    # 转换为pandas Series，保持索引一致
    if hasattr(HIGH, 'index'):
        return pd.Series(sar, index=HIGH.index)
    else:
        return pd.Series(sar)
#*******************************
#******************************
#交易类型
def MA_交易(CLOSE,SHORT=5,LONG=20):
    '''
    MA_交易
    MA1赋值:收盘价的SHORT日简单移动平均
    MA2赋值:收盘价的LONG日简单移动平均
    平空开多赋值:MA1上穿MA2
    平多开空赋值:MA2上穿MA1
    先平空仓再开多仓
    先平多仓再开空仓
    '''
    MA1=MA(CLOSE,SHORT)
    MA2=MA(CLOSE,LONG)
    平空开多=CROSS(MA1,MA2)
    平多开空=CROSS(MA2,MA1)
    return MA1,MA2,平空开多,平多开空
def MACD_交易(CLOSE,SHORT=12,LONG=26,MID=9):
    '''
    MACD交易
    DIFF赋值:收盘价的SHORT日指数移动平均-收盘价的LONG日指数移动平均
    DEA赋值:DIFF的MID日指数移动平均
    MACD赋值:2*(DIFF-DEA)
    平空开多赋值:MACD上穿0
    平多开空赋值:0上穿MACD
    先平空仓再开多仓
    '''
    DIFF=EMA(CLOSE,SHORT)-EMA(CLOSE,LONG)
    DEA=EMA(DIFF,MID)
    MACD=2*(DIFF-DEA)
    平空开多=CROSS(MACD,0)
    平空开多=CROSS(0,MACD)
    return DIFF,DEA,MACD,平空开多,平空开多
def KDJ_交易(CLOSE,HIGH,LOW,N=9,M1=3):
    '''
    KDJ交易
    RSV赋值:(收盘价-N日内最低价的最低值)/(N日内最高价的最高值-N日内最低价的最低值)*100
    K赋值:RSV的M1日[1日权重]移动平均
    D赋值:K的M1日[1日权重]移动平均
    J赋值:3*K-2*D
    平空开多赋值:J上穿0
    平多开空赋值:100上穿J
    先平空仓再开多仓
    先平多仓再开空仓
    自动过滤交易信号
    '''
    RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100
    K=SMA(RSV,M1,1)
    D=SMA(K,M1,1)
    J=3*K-2*D
    平空开多=CROSS(J,0)
    平多开空=CROSS(100,J)
    return K,D,J,平空开多,平多开空
#*****************************************
#*****************************************
#神系
def SG_XDT(CLOSE,INDEXC,P1=5,P2=10):
    '''
    心电图(需下载日线)
    输出强弱指标(需下载日线):收盘价/大盘的收盘价*1000
    输出MQR1:QR的5日简单移动平均
    输出MQR2:QR的10日简单移动平均
    ''' 
    QR=CLOSE/INDEXC*1000
    MQR1=MA(QR,5)
    MQR2=MA(QR,10)
    return QR,MQR1,MQR2
def SG_NDB(CLOSE,HIGH,LOW,P1=5,P2=10):
    '''
    脑电波(神系)
    HH赋值:如果收盘价/1日前的收盘价>1.093ANDL>1日前的最高价,返回2*收盘价-1日前的收盘价-最高价,否则返回2*收盘价-最高价-最低价
    V1赋值:收盘价的有效数据周期数
    V2赋值:2*V1日前的收盘价-V1日前的最高价-V1日前的最低价
    输出DK:HH的历史累和+V2
    输出MDK1:DK的P1日简单移动平均
    输出MDK2:DK的P2日简单移动平均
    '''
    C=CLOSE
    H=HIGH
    L=LOW
    HH=IF(np.logical_or(C/REF(C,1)>1.093 ,L>REF(H,1)),2*C-REF(C,1)-H,2*C-H-L)
    V1=1
    V2=2*REF(C,V1)-REF(H,V1)-REF(L,V1)
    DK=SUM(HH,0)+V2
    MDK1=MA(DK,P1)
    MDK2=MA(DK,P2)
    return DK,MDK1,MDK2
def SG_SMX(CLOSE,HIGH,LOW,INDEXH,INDEXL,INDEXC,N=50):
    '''
    生命线(需下载日线)
    INDEXH,INDEXL,INDEXC指数的高，低收盘价,可以通过akshare.stock_zh_a_daily(sybol='sh000001')获取
    H1赋值:N日内最高价的最高值
    L1赋值:N日内最低价的最低值
    H2赋值:N日内大盘的最高价的最高值
    L2赋值:N日内大盘的最低价的最低值
    ZY赋值:收盘价/大盘的收盘价*2000
    输出ZY1:ZY的3日指数移动平均
    输出ZY2:ZY的17日指数移动平均
    输出ZY3:ZY的34日指数移动平均
    '''
    H1=HHV(HIGH,N)
    L1=LLV(LOW,N)
    H2=HHV(INDEXH,N)
    L2=LLV(INDEXL,N)
    ZY=CLOSE/INDEXC*2000
    ZY1=EMA(ZY,3)
    ZY2=EMA(ZY,17)
    ZY3=EMA(ZY,34)
    return ZY1,ZY2,ZY3
def SG_LB(VOL,INDEXV):
    '''
    量比(需下载日线)
    VOl个股成交量，INDXEXV大盘成交量，可以通过ak.stock_zh_a_daily()获取
    ZY2赋值:成交量(手)/大盘的成交量*1000
    输出量比:ZY2
    输出MA5:ZY2的5日简单移动平均
    输出MA10:ZY2的10日简单移动平均
    '''
    ZY2=VOL/INDEXV*1000
    量比=ZY2
    MA5=MA(ZY2,5)
    MA10=MA(ZY2,10)
    return 量比,MA5,MA10
def SG_PF(CLOSE,INDEXC):
    '''
    强势股评分(需下载日线)
    ZY1赋值:收盘价/大盘的收盘价*1000
    A1赋值:如果ZY1>3日内ZY1的最高值,返回10,否则返回0
    A2赋值:如果ZY1>5日内ZY1的最高值,返回15,否则返回0
    A3赋值:如果ZY1>10日内ZY1的最高值,返回20,否则返回0
    A4赋值:如果ZY1>2日内ZY1的最高值,返回10,否则返回0
    A5赋值:统计9日中满足ZY1>1日前的ZY1的天数*5
    输出强势股评分:A1+A2+A3+A4+A5
    '''
    ZY1=CLOSE/INDEXC*1000
    A1=IF(ZY1>HHV(ZY1,3),10,0)
    A2=IF(ZY1>HHV(ZY1,5),15,0)
    A3=IF(ZY1>HHV(ZY1,10),20,0)
    A4=IF(ZY1>HHV(ZY1,2),10,0)
    A5=COUNT(ZY1>REF(ZY1,1) ,9)*5
    强势股评分=A1+A2+A3+A4+A5
    return 强势股评分
#*************************************************
#*************************************************
#龙系
def RAD(OPEN,HIGH,CLOSE,LOW,INDEXO,INDEXH,INDEXL,INDEXC,D=3,S=30,M=30):
    '''
    威力雷达(需下载日线)
    OPEN+HIGH+CLOSE+LOW个股
    INDEXO+INDEXH+INDEXL+INDEXC大盘数据，可以通过akshare获取
    SM赋值:(开盘价+最高价+收盘价+最低价)/4
    SMID赋值:SM的D日简单移动平均
    IM赋值:(大盘的开盘价+大盘的最高价+大盘的最低价+大盘的收盘价)/4
    IMID赋值:IM的D日简单移动平均
    SI1赋值:(SMID-1日前的SMID)/SMID
    II赋值:(IMID-1日前的IMID)/IMID
    输出RADER1:(SI1-II)*2的S日累和*1000
    输出RADERMA:RADER1的M日[1日权重]移动平均
    '''
    SM=(OPEN+HIGH+CLOSE+LOW)/4
    SMID=MA(SM,D)
    IM=(INDEXO+INDEXH+INDEXL+INDEXC)/4
    IMID=MA(IM,D)
    SI1=(SMID-REF(SMID,1))/SMID
    II=(IMID-REF(IMID,1))/IMID
    RADER1=SUM((SI1-II)*2,S)*1000
    RADERMA=SMA(RADER1,M,1)
    return RADER1,RADERMA
    return 
def LON(CLOSE,HIGH,LOW,VOL,N=10):
    '''
    龙系长线
    赋值: 1日前的收盘价
    赋值: 成交量(手)的2日累和/(((2日内最高价的最高值-2日内最低价的最低值))*100)
    赋值: (收盘价-LC)*VID
    赋值: RC的历史累和
    赋值: LONG的10日[1日权重]移动平均
    赋值: LONG的20日[1日权重]移动平均
    输出龙系长线 : DIFF-DEA
    输出LONMA : 龙系长线的N日简单移动平均
    输出LONT : 龙系长线, COLORSTICK
    '''
    LC = REF(CLOSE,1)
    VID = SUM(VOL,2)/(((HHV(HIGH,2)-LLV(LOW,2)))*100)
    RC = (CLOSE-LC)*VID
    LONG = SUM(RC,0)
    DIFF = SMA(LONG,10,1)
    DEA = SMA(LONG,20,1)
    LON = DIFF-DEA
    LONMA = MA(LON,N)
    LONT = LON
    return LON,LONMA,LONT
def SHT(CLOSE,VOL,N=5):
    '''
    龙系短线
    VAR1赋值:(成交量(手)-1日前的成交量(手))/1日前的成交量(手)的5日简单移动平均
    VAR2赋值:(收盘价-收盘价的24日简单移动平均)/收盘价的24日简单移动平均*100
    输出MY: VAR2*(1+VAR1)
    输出龙系短线: MY, COLORSTICK
    输出SHTMA: SHT的N日简单移动平均
    '''
    VAR1=MA((VOL-REF(VOL,1))/REF(VOL,1),5)
    VAR2=(CLOSE-MA(CLOSE,24))/MA(CLOSE,24)*100
    MY= VAR2*(1+VAR1)
    SHT= MY#COLORSTICK
    SHTMA= MA(SHT,N)
    return SHT,SHTMA
def ZLJC(CLOSE,LOW,HIGH,VOL):
    '''
    主力进出
    VAR1赋值:(收盘价+最低价+最高价)/3
    VAR2赋值:((VAR1-1日前的最低价)-(最高价-VAR1))*成交量(手)/100000/(最高价-最低价)的历史累和
    VAR3赋值:VAR2的1日指数移动平均
    输出 JCS:VAR3
    输出 JCM:VAR3的12日简单移动平均
    输出 JCL:VAR3的26日简单移动平均
    '''
    VAR1=(CLOSE+LOW+HIGH)/3
    VAR2=SUM(((VAR1-REF(LOW,1))-(HIGH-VAR1))*VOL/100000/(HIGH-LOW),0)
    VAR3=EMA(VAR2,1)
    JCS=VAR3
    JCM=MA(VAR3,12)
    JCL=MA(VAR3,26)
    return JCS,JCM,JCL
def ZLMM(CLOSE):
    '''
    赋值:1日前的收盘价
    RSI2赋值:收盘价-LC和0的较大值的12日[1日权重]移动平均/收盘价-LC的绝对值的12日[1日权重]移动平均*100
    RSI3赋值:收盘价-LC和0的较大值的18日[1日权重]移动平均/收盘价-LC的绝对值的18日[1日权重]移动平均*100
    输出MMS:3*RSI2-2*收盘价-LC和0的较大值的16日[1日权重]移动平均/收盘价-LC的绝对值的16日[1日权重]移动平均*100的3日简单移动平均
    输出MMM:MMS的8日指数移动平均
    输出MML:3*RSI3-2*收盘价-LC和0的较大值的12日[1日权重]移动平均/收盘价-LC的绝对值的12日[1日权重]移动平均*100的5日简单移动平均
    '''
    LC =REF(CLOSE,1)
    RSI2=SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100
    RSI3=SMA(MAX(CLOSE-LC,0),18,1)/SMA(ABS(CLOSE-LC),18,1)*100
    MMS=MA(3*RSI2-2*SMA(MAX(CLOSE-LC,0),16,1)/SMA(ABS(CLOSE-LC),16,1)*100,3)
    MMM=EMA(MMS,8)
    MML=MA(3*RSI3-2*SMA(MAX(CLOSE-LC,0),12,1)/SMA(ABS(CLOSE-LC),12,1)*100,5)
    return MMS,MMM,MML
def SLZT(CLOSE,LOW,HIGH):
    '''
    神龙在天
    输出白龙: 收盘价的125日简单移动平均
    输出黄龙: 白龙+2*收盘价的170日估算标准差
    输出紫龙: 白龙-2*收盘价的145日估算标准差
    输出青龙: 步长为1极限值为7的125日抛物转向, LINESTICK
    VAR2赋值:70日内最高价的最高值
    VAR3赋值:20日内最高价的最高值
    输出红龙: VAR2*0.83
    输出蓝龙: VAR3*0.91
    '''
    白龙=MA(CLOSE,125)
    黄龙=白龙+2*STD(CLOSE,170)
    紫龙=白龙-2*STD(CLOSE,145)
    青龙=SAR(HIGH,LOW,125,1,7)# LINESTICK;
    VAR2=HHV(HIGH,70)
    VAR3=HHV(HIGH,20)
    红龙= VAR2*0.83
    蓝龙=VAR3*0.91
    return 白龙,黄龙,紫龙,青龙,红龙,蓝龙
def ADVOL(CLOSE,HIGH,LOW,VOL):
    '''
    龙系离散量
    A赋值:((收盘价-最低价)-(最高价-收盘价))*成交量(手)/10000/(最高价-最低价)的历史累和
    输出龙系离散量:A
    输出MA1:A的30日简单移动平均
    输出均线:MA1的100日简单移动平均
    '''
    A=SUM(((CLOSE-LOW)-(HIGH-CLOSE))*VOL/10000/(HIGH-LOW),0)
    ADVOL=A
    MA1=MA(A,30)
    MA2=MA(MA1,100)
    return ADVOL,MA1,MA2
#*********************************************
#*********************************************
#鬼系
def CYC(code='sh600031',start_date='20210101',end_date='20221022',P1=5,P2=13,P3=34):
    '''
    成本均线
    JJJ赋值:如果总量>0.01,简单理解流通股,返回0.01*总金额/总量,否则返回昨收盘价
    DDD赋值:(最高价<0.01 或者 最低价<0.01)
    JJJT赋值:如果DDD,返回1,否则返回(JJJ<(最高价+0.01)并且JJJ>(最低价-0.01))
    输出CYC1:如果JJJT,返回0.01*成交额(元)的P1日指数移动平均/成交量(手)的P1日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P1日指数移动平均
    输出CYC2:如果JJJT,返回0.01*成交额(元)的P2日指数移动平均/成交量(手)的P2日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P2日指数移动平均
    输出CYC3:如果JJJT,返回0.01*成交额(元)的P3日指数移动平均/成交量(手)的P3日指数移动平均,否则返回(最高价+最低价+收盘价)/3的P3日指数移动平均
    输出CYC∞:如果JJJT,返回以100*成交量(手)/流通股本(股)为权重成交额(元)/(100*成交量(手))的动态移动平均,否则返回(最高价+最低价+收盘价)/3的120日指数移动平均
    '''
    pass
    def DYNAINFO_10(M=10):
        '''
        总金额=price*volume
        '''
        result=df['close']*df['volume']
        return result
    def DYNAINFO_3(M=3):
        '''
        昨日收盘价
        '''
        return df['close'].shift(1)
    def DYNAINFO_5(M=5):
        '''
        最高价
        '''
        return df['high']
    def DYNAINFO_6(M=6):
        '''
        最低价
        '''
        return df['low']
    AMOUNT=AMOUNT=df['close']*df['volume']
    VOL=df['volume']
    HIGH=df['high']
    LOW=df['low']
    CLOSE=df['close']
    def FINANCE_7(M=7):
        '''
        100*成交量
        '''
        return 100*df['volume']
    JJJ=IF(DYNAINFO_8(8)>0.01,0.01*DYNAINFO_10(10)/DYNAINFO_8(8),DYNAINFO_3(3))
    DDD=np.logical_or(DYNAINFO_5(5)<0.01,DYNAINFO_6(6)<0.01)
    JJJT=IF(DDD,False,np.logical_and(JJJ<(DYNAINFO_5(5)+0.01),JJJ>(DYNAINFO_6(6)-0.01)))
    CYC1=IF(JJJT,0.01*EMA(AMOUNT,P1)/EMA(VOL,P1),EMA((HIGH+LOW+CLOSE)/3,P1))
    CYC2=IF(JJJT,0.01*EMA(AMOUNT,P2)/EMA(VOL,P2),EMA((HIGH+LOW+CLOSE)/3,P2))
    CYC3=IF(JJJT,0.01*EMA(AMOUNT,P3)/EMA(VOL,P3),EMA((HIGH+LOW+CLOSE)/3,P3))
    #CYC_a=IF(JJJT,DMA(AMOUNT/(100*VOL),100*VOL/FINANCE_7(7)),EMA((HIGH+LOW+CLOSE)/3,120))
    return CYC1,CYC2,CYC3
def CYS(CLOSE,AMOUNT,VOL):
    '''
    市场盈亏
    AMOUNT成交额，VOL成交量
    CYC13赋值:0.01*成交额(元)的13日指数移动平均/成交量(手)的13日指数移动平均
    输出市场盈亏:(收盘价-CYC13)/CYC13*100
    '''
    CYC13=0.01*EMA(AMOUNT,13)/EMA(VOL,13)
    CYS=(CLOSE-CYC13)/CYC13*100
    return CYS
def CYQKL(CLOSE,OPEN):
    '''
    博弈K线长度
    输出KL:100*(以收盘价计算的获利盘比例-以开盘价计算的获利盘比例)
    '''
    KL=100*(WINNER(CLOSE)-WINNER(OPEN))
    return KL
def CYW(CLOSE,HIGH,LOW,VOL):
    '''
    主力控盘
    VAR1赋值:收盘价-最低价
    VAR2赋值:最高价-最低价
    VAR3赋值:收盘价-最高价
    VAR4赋值:如果最高价>最低价,返回(VAR1/VAR2+VAR3/VAR2)*成交量(手),否则返回0
    输出主力控盘: VAR4的10日累和/10000, COLORSTICK
    '''
    VAR1=CLOSE-LOW
    VAR2=HIGH-LOW
    VAR3=CLOSE-HIGH
    VAR4=IF(HIGH>LOW,(VAR1/VAR2+VAR3/VAR2)*VOL,0)
    CYW=SUM(VAR4,10)/10000 #COLORSTICK
    return CYW
#***************************************************
#***************************************************
#其他系
def PEAK(CLOSE,N,n=1):
    '''
    计算倾效
    np.polyfit(range(N),x,deg=1)
    '''
    pass
def TROUGH(CLOSE,N,n=1):
    '''
    箱底
    '''
    pass
def XT(CLOSE):
    '''
    箱体
    '''
    箱顶=PEAK(CLOSE,N,1)*0.98
    箱底=TROUGH(CLOSE,N,1)*1.02
    箱高=100*(箱顶-箱底)/箱底,#NODRAW
def  MOD(M,N):
    '''
    计算模
    M/N的余数
    '''
    return M//N
def SQJZ(CLSOE):
    '''
    N赋值:到最后交易的周期
    B赋值:收盘价<4日前的收盘价
    T1赋值: 条件连续成立次数
    A_B1赋值:(T1>9) AND T1关于9的模=1
    A_B2赋值:(T1>9) AND T1关于9的模=2
    A_B8赋值:(T1>9) AND T1关于9的模=8
    A_B9赋值:(T1>9) AND T1关于9的模=0
    B1赋值:(N=6 AND 5日后的(平滑处理)统计6日中满足B的天数=6) OR (N=7 AND 6日后的(平滑处理)统计7日中满足B的天数=7) OR (N=8 AND 7日后的(平滑处理)统计8日中满足B的天数=8) OR (N>=9 AND 8日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B1AND(1日前的B=0ORA_B1)时,在最低价位置书写数字,画洋红色
    B2赋值:(N=5 AND 4日后的(平滑处理)统计6日中满足B的天数=6) OR (N=6 AND 5日后的(平滑处理)统计7日中满足B的天数=7) OR (N=7 AND 6日后的(平滑处理)统计8日中满足B的天数=8) OR (N>=8 AND 7日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B2AND(2日前的B=0ORA_B2)时,在最低价位置书写数字,画洋红色
    B8赋值:(N=1 AND 统计8日中满足B的天数=8) OR (N>=2 AND 1日后的(平滑处理)统计9日中满足B的天数=9)
    当满足条件B8AND(8日前的B=0ORA_B8)时,在最低价位置书写数字,画洋红色
    B9赋值:(N>=1 AND 统计9日中满足B的天数=9)
    当满足条件B9AND(9日前的B=0ORA_B9)时,在最低价位置书写数字,画红色
    S赋值:收盘价>4日前的收盘价
    T2赋值: 条件连续成立次数
    A_S1赋值:(T2>9) AND T2关于9的模=1
    A_S2赋值:(T2>9) AND T2关于9的模=2
    A_S8赋值:(T2>9) AND T2关于9的模=8
    A_S9赋值:(T2>9) AND T2关于9的模=0
    S1赋值:(N=6 AND 5日后的(平滑处理)统计6日中满足S的天数=6) OR (N=7 AND 6日后的(平滑处理)统计7日中满足S的天数=7) OR (N=8 AND 7日后的(平滑处理)统计8日中满足S的天数=8) OR (N>=9 AND 8日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S1AND(1日前的S=0ORA_S1)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S2赋值:(N=5 AND 4日后的(平滑处理)统计6日中满足S的天数=6) OR (N=6 AND 5日后的(平滑处理)统计7日中满足S的天数=7) OR (N=7 AND 6日后的(平滑处理)统计8日中满足S的天数=8) OR (N>=8 AND 7日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S2AND(2日前的S=0ORA_S2)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S8赋值:(N=1 AND 统计8日中满足S的天数=8) OR (N>=2 AND 1日后的(平滑处理)统计9日中满足S的天数=9)
    当满足条件S8AND(8日前的S=0ORA_S8)时,在最高价位置书写数字,画洋红色,显示在位置之上
    S9赋值:(N>=1 AND 统计9日中满足S的天数=9)
    当满足条件S9AND(9日前的S=0ORA_S9)时,在最高价位置书写数字,画绿色,显示在位置之上
    C=CLOSE
    N=CURRBARSCOUNT()
    B=C<REF(C,4)
    T1= BARSLASTCOUNT(B)
    A_B1=IF(T1>=9,1,None)
    A_B2=IF(T1>9,2,None)
    A_B8=IF(T1>9,8,None)
    A_B9=IF(T1>9,0,None)
    B1:=(N=6 AND REFXV(COUNT(B,6),5)=6) OR (N=7 AND REFXV(COUNT(B,7),6)=7) OR (N=8 AND REFXV(COUNT(B,8),7)=8) OR (N>=9 AND REFXV(COUNT(B,9),8)=9);
    DRAWNUMBER(B1 AND (REF(B,1)=0 OR A_B1),L,1),COLORMAGENTA;
    B2:=(N=5 AND REFXV(COUNT(B,6),4)=6) OR (N=6 AND REFXV(COUNT(B,7),5)=7) OR (N=7 AND REFXV(COUNT(B,8),6)=8) OR (N>=8 AND REFXV(COUNT(B,9),7)=9);
    DRAWNUMBER(B2 AND(REF(B,2)=0 OR A_B2),L,2),COLORMAGENTA;
    B8:=(N=1 AND COUNT(B,8)=8) OR (N>=2 AND REFXV(COUNT(B,9),1)=9);
    DRAWNUMBER(B8 AND (REF(B,8)=0 OR A_B8),L,8),COLORMAGENTA;
    B9:=(N>=1 AND COUNT(B,9)=9);
    DRAWNUMBER(B9 AND (REF(B,9)=0 OR A_B9),L,9),COLORRED;
    S:=C>REF(C,4);
    T2:= BARSLASTCOUNT(S);
    A_S1:=(T2>9) AND MOD(T2,9)=1;
    A_S2:=(T2>9) AND MOD(T2,9)=2;
    A_S8:=(T2>9) AND MOD(T2,9)=8;
    A_S9:=(T2>9) AND MOD(T2,9)=0;
    S1:=(N=6 AND REFXV(COUNT(S,6),5)=6) OR (N=7 AND REFXV(COUNT(S,7),6)=7) OR (N=8 AND REFXV(COUNT(S,8),7)=8) OR (N>=9 AND REFXV(COUNT(S,9),8)=9);
    DRAWNUMBER(S1 AND (REF(S,1)=0 OR A_S1),H,1),COLORMAGENTA,DRAWABOVE;
    S2:=(N=5 AND REFXV(COUNT(S,6),4)=6) OR (N=6 AND REFXV(COUNT(S,7),5)=7) OR (N=7 AND REFXV(COUNT(S,8),6)=8) OR (N>=8 AND REFXV(COUNT(S,9),7)=9);
    DRAWNUMBER(S2 AND (REF(S,2)=0 OR A_S2),H,2),COLORMAGENTA,DRAWABOVE;
    S8:=(N=1 AND COUNT(S,8)=8) OR (N>=2 AND REFXV(COUNT(S,9),1)=9);
    DRAWNUMBER(S8 AND (REF(S,8)=0 OR A_S8),H,8),COLORMAGENTA,DRAWABOVE;
    S9:=(N>=1 AND COUNT(S,9)=9);
    DRAWNUMBER(S9 AND (REF(S,9)=0 OR A_S9),H,9),COLORGREEN,DRAWABOVE;
    '''
    pass
def JAX(CLOSE,HIGH,LOW,N=30):
    '''
    济安线
    AA赋值:(2*收盘价+最高价+最低价)/4-收盘价的N日简单移动平均的绝对值/收盘价的N日简单移动平均
    输出济安线:以AA为权重(2*收盘价+最低价+最高价)/4的动态移动平均,线宽为3,画洋红色
    CC赋值:(收盘价/济安线)
    MA1赋值:CC*(2*收盘价+最高价+最低价)/4的3日简单移动平均
    MAAA赋值:((MA1-济安线)/济安线)/3
    TMP赋值:MA1-MAAA*MA1
    输出J:如果TMP<=济安线,返回济安线,否则返回无效数,线宽为3,画青色
    输出A:TMP,线宽为2,画棕色
    输出X:如果TMP<=济安线,返回TMP,否则返回无效数,线宽为2,画绿色
    '''
    AA=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,N))/MA(CLOSE,N)
    data=pd.DataFrame()
    data['数据']=(2*CLOSE+LOW+HIGH)/4
    #alpha中值0.5
    济安线=data['数据'].ewm(alpha=0.5, adjust=True).mean()#LINETHICK3,COLORMAGENTA
    CC=(CLOSE/济安线)
    MA1=MA(CC*(2*CLOSE+HIGH+LOW)/4,3)
    MAAA=((MA1-济安线)/济安线)/3
    TMP=MA1-MAAA*MA1
    J=IF(TMP<=济安线,济安线,None)#LINETHICK3,COLORCYAN
    A=TMP#LINETHICK2,COLORBROWN
    X=IF(TMP<=济安线,TMP,None)#LINETHICK2,COLORGREEN
    return J,A,X
def XJDX(CLOSE,HIGH,LOW):
    '''
    超级短线
    VAR1赋值:(2*收盘价+最高价+最低价)/4
    VAR2赋值:VAR1的4日指数移动平均的4日指数移动平均的4日指数移动平均
    输出J: (VAR2-1日前的VAR2)/1日前的VAR2*100, COLORSTICK
    输出D: J的3日简单移动平均
    输出K: J的1日简单移动平均
    '''
    VAR1=(2*CLOSE+HIGH+LOW)/4
    VAR2=EMA(EMA(EMA(VAR1,4),4),4)
    J=(VAR2-REF(VAR2,1))/REF(VAR2,1)*100# COLORSTICK
    D=MA(J,3)
    K= MA(J,1)
    return J,D,K
def ZJTJ(CLOSE):
    '''
    庄家抬轿
    获利盘，和成本函数需要写
    VAR1赋值:收盘价的9日指数移动平均的9日指数移动平均
    控盘赋值:(VAR1-1日前的VAR1)/1日前的VAR1*1000
    当满足条件控盘<0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,画白色
    A10赋值:控盘上穿0
    输出无庄控盘:如果控盘<0,返回控盘,否则返回0,画白色,NODRAW
    输出开始控盘:如果A10,返回5,否则返回0,线宽为1,画棕色
    当满足条件控盘>1日前的控盘AND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,画红色
    输出有庄控盘:如果控盘>1日前的控盘AND控盘>0,返回控盘,否则返回0,画红色,NODRAW
    VAR2赋值:100*以收盘价*0.95计算的获利盘比例
    当满足条件VAR2>50ANDCOST(85)<CLOSEAND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,COLORFF00FF
    输出高度控盘:如果VAR2>50ANDCOST(85)<CLOSEAND控盘>0,返回控盘,否则返回0,COLORFF00FF,NODRAW
    当满足条件控盘<1日前的控盘AND控盘>0时,在控盘和0位置之间画柱状线,宽度为1,0不为0则画空心柱.,COLOR00FF00
    输出主力出货:如果控盘<1日前的控盘AND控盘>0,返回控盘,否则返回0,COLOR00FF00,NODRAW
    '''
    VAR1=EMA(EMA(CLOSE,9),9)
    控盘=(VAR1-REF(VAR1,1))/REF(VAR1,1)*1000
    #STICKLINE(控盘<0,控盘,0,1,0),COLORWHITE;
    A10=CROSS(控盘,0)
    无庄控盘=IF(控盘<0,控盘,0)#COLORWHITE,NODRAW;
    开始控盘=IF(A10,1,0)#LINETHICK1,COLORBROWN;
    #STICKLINE(控盘>REF(控盘,1) AND 控盘>0,控盘,0,1,0),COLORRED;
    有庄控盘=IF(np.logical_and(控盘>REF(控盘,1),控盘>0),控盘,0)#COLORRED,NODRAW;
    #VAR2=100*WINNER(CLOSE*0.95)
    #STICKLINE(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0,1,0),COLORFF00FF;
    #高度控盘:IF(VAR2>50 AND COST(85)<CLOSE AND 控盘>0,控盘,0),COLORFF00FF,NODRAW;
    #STICKLINE(控盘<REF(控盘,1) AND 控盘>0,控盘,0,1,0),COLOR00FF00;
    主力出货=IF(np.logical_and(控盘<REF(控盘,1),控盘>0),控盘,0)#COLOR00FF00,NODRAW;
    return 无庄控盘,开始控盘,有庄控盘,主力出货
def ZBCD(HIGH,LOW,OPEN,AMOUNT,VOL,CLOSE,N=10):
    '''
    准备抄底
    VAR1赋值:成交额(元)/成交量(手)/7
    VAR2赋值:(3*最高价+最低价+开盘价+2*收盘价)/7
    VAR3赋值:成交额(元)的N日累和/VAR1/7
    VAR4赋值:以成交量(手)/VAR3为权重VAR2的动态移动平均
    输出抄底:(收盘价-VAR4)/VAR4*100,画淡洋红色
    当满足条件-7.0上穿抄底时,在抄底位置画1号图标
    '''
    VAR1=AMOUNT/VOL/7
    VAR2=(3*HIGH+LOW+OPEN+2*CLOSE)/7
    VAR3=SUM(AMOUNT,N)/VAR1/7
    VAR4=DMA(VAR2,VOL/VAR3)
    抄底=(CLOSE-VAR4)/VAR4*100#COLORLIMAGENTA
    #DRAWICON(CROSS(-7.0,抄底),抄底,1)
    return 抄底
def BDZX(HIGH,LOW,CLOSE):
    '''
    波段之星
    VAR2赋值:(最高价+最低价+收盘价*2)/4
    VAR3赋值:VAR2的21日指数移动平均
    VAR4赋值:VAR2的21日估算标准差
    VAR5赋值:((VAR2-VAR3)/VAR4*100+200)/4
    VAR6赋值:(VAR5的5日指数移动平均-25)*1.56
    输出AK: VAR6的2日指数移动平均*1.22
    输出AD1: AK的2日指数移动平均
    输出AJ: 3*AK-2*AD1
    输出AA:100
    输出布林极限:0
    输出CC:80
    输出买进: 如果AK上穿AD1,返回58,否则返回20
    输出卖出: 如果AD1上穿AK,返回58,否则返回20
    '''
    VAR2=(HIGH+LOW+CLOSE*2)/4
    VAR3=EMA(VAR2,21)
    VAR4=STD(VAR2,21)
    VAR5=((VAR2-VAR3)/VAR4*100+200)/4
    VAR6=(EMA(VAR5,5)-25)*1.56
    AK= EMA(VAR6,2)*1.22
    AD1= EMA(AK,2)
    AJ= 3*AK-2*AD1
    AA=100
    BB=0
    CC=80
    买进= IF(CROSS(AK,AD1),58,20)
    卖出= IF(CROSS(AD1,AK),58,20)
    return AK,AD1,AJ,AA,BB,CC,买进,卖出
def LHXJ(HIGH,LOW,CLOSE):
    '''
    猎狐先觉
    VAR1赋值:(收盘价*2+最高价+最低价)/4
    VAR2赋值:VAR1的13日指数移动平均-VAR1的34日指数移动平均
    VAR3赋值:VAR2的5日指数移动平均
    输出主力弃盘: (-2)*(VAR2-VAR3)*3.8
    输出主力控盘: 2*(VAR2-VAR3)*3.8
    '''
    VAR1=(CLOSE*2+HIGH+LOW)/4
    VAR2=EMA(VAR1,13)-EMA(VAR1,34)
    VAR3=EMA(VAR2,5)
    主力弃盘=(-2)*(VAR2-VAR3)*3.8
    主力控盘=2*(VAR2-VAR3)*3.8
    return 主力弃盘,主力控盘
def LYJH(CLOSE,HIGH,LOW,M=80,M1=50):
    '''
    猎鹰歼狐
    VAR1赋值:(36日内最高价的最高值-收盘价)/(36日内最高价的最高值-36日内最低价的最低值)*100
    输出机构做空能量线: VAR1的2日[1日权重]移动平均
    VAR2赋值:(收盘价-9日内最低价的最低值)/(9日内最高价的最高值-9日内最低价的最低值)*100
    输出机构做多能量线: VAR2的5日[1日权重]移动平均-8
    输出LH: M
    输出LH1: M1
    '''
    VAR1=(HHV(HIGH,36)-CLOSE)/(HHV(HIGH,36)-LLV(LOW,36))*100
    机构做空能量线=SMA(VAR1,2,1)
    VAR2=(CLOSE-LLV(LOW,9))/(HHV(HIGH,9)-LLV(LOW,9))*100
    机构做多能量线=SMA(VAR2,5,1)-8
    LH=M
    LH1=M1
    return 机构做空能量线,机构做多能量线,LH,LH1
def JFZX(OPEN,CLOSE,VOL,N=30):
    '''
    飓风智能中线
    VAR2赋值:如果收阳线,返回成交量(手),否则返回0的N日累和/成交量(手)的N日累和*100
    VAR3赋值:100-如果收阳线,返回成交量(手),否则返回0的N日累和/成交量(手)的N日累和*100
    输出多头力量: VAR2
    输出空头力量: VAR3
    输出多空平衡: 50
    '''
    VAR2=SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100
    VAR3=100-SUM(IF(CLOSE>OPEN,VOL,0),N)/SUM(VOL,N)*100
    多头力量= VAR2
    空头力量= VAR3
    多空平衡= 50
    return 多头力量,空头力量,多空平衡
def CYHT(CLOSE,HIGH,LOW,OPEN):
    '''
    财运亨通
    VAR1赋值:(2*收盘价+最高价+最低价+开盘价)/5
    输出高抛: 80
    VAR2赋值:34日内最低价的最低值
    VAR3赋值:34日内最高价的最高值
    输出SK: (VAR1-VAR2)/(VAR3-VAR2)*100的13日指数移动平均
    输出SD: SK的3日指数移动平均
    输出低吸: 20
    输出强弱分界: 50
    VAR4赋值:如果SK上穿SD,返回40,否则返回22
    VAR5赋值:如果SD上穿SK,返回60,否则返回78
    输出卖出: VAR5
    输出买进: VAR4
    '''
    VAR1=(2*CLOSE+HIGH+LOW+OPEN)/5
    高抛= 80
    VAR2=LLV(LOW,34)
    VAR3=HHV(HIGH,34)
    SK= EMA((VAR1-VAR2)/(VAR3-VAR2)*100,13)
    SD= EMA(SK,3)
    低吸= 20
    强弱分界= 50
    VAR4=IF(CROSS(SK,SD),40,22)
    VAR5=IF(CROSS(SD,SK),60,78)
    卖出= VAR5
    买进= VAR4
    return 高抛,SK,SD,低吸,强弱分界,卖出,买进
def BSQJ(CLOSE):
    '''
    买卖区间
    买线赋值:收盘价的2日指数移动平均
    卖线赋值:收盘价的21日线性回归斜率*20+收盘价的42日指数移动平均
    当满足条件买线>=卖线时,在日期日0日内最高价的最高值和日期日0日内最低价的最低值位置之间画柱状线,宽度为6,0不为0则画空心柱.,COLOR001050
    当满足条件买线<卖线时,在日期日0日内最高价的最高值和日期日0日内最低价的最低值位置之间画柱状线,宽度为6,0不为0则画空心柱.,COLOR404050
    K线
    指导赋值:(收盘价的4日指数移动平均+收盘价的6日指数移动平均+收盘价的12日指数移动平均+收盘价的24日指数移动平均)/4的2日指数移动平均
    界赋值:收盘价的27日简单移动平均
    输出B买:如果指导上穿界ORCROSS(买线,卖线),返回收盘价,否则返回无效数,画洋红色,NODRAW
    输出持仓:如果买线>=卖线,返回收盘价,否则返回无效数,画红色,NODRAW
    输出S卖:如果界上穿指导ORCROSS(卖线,买线),返回收盘价,否则返回无效数,画淡灰色,NODRAW
    输出空仓:如果买线<卖线,返回收盘价,否则返回无效数,画绿色,NODRAW
    当满足条件买线上穿卖线时,在最低价位置画1号图标
    当满足条件卖线上穿买线时,在最高价位置画2号图标
    '''
    C=CLOSE
    买线=EMA(C,2)
    卖线=EMA(SLOPE(C,21)*20+C,42)
    #STICKLINE(买线>=卖线,REFDATE(HHV(H,0),DATE),REFDATE(LLV(L,0),DATE),6,0),COLOR001050
    #STICKLINE(买线<卖线,REFDATE(HHV(H,0),DATE),REFDATE(LLV(L,0),DATE),6,0),COLOR404050;
    #DRAWKLINE(H,O,L,C);
    指导=EMA((EMA(CLOSE,4)+EMA(CLOSE,6)+EMA(CLOSE,12)+EMA(CLOSE,24))/4,2)
    界=MA(CLOSE,27)
    B买=IF(np.logical_or(CROSS(指导,界),CROSS(买线,卖线)),C,None)#COLORMAGENTA,NODRAW;
    持仓=IF(买线>=卖线,C,None)#COLORRED,NODRAW
    S卖=IF(np.logical_or(CROSS(界,指导),CROSS(卖线,买线)),C,None)#COLORLIGRAY,NODRAW
    空仓=IF(买线<卖线,C,None)#COLORGREEN,NODRAW
    #DRAWICON(CROSS(买线,卖线),L,1);
    #DRAWICON(CROSS(卖线,买线),H,2);
    return B买,持仓,S卖,空仓
def CDP_STD(CLOSE, HIGH, LOW):
    '''
    逆势操作
    CH赋值:1日前的最高价
    CL赋值:1日前的最低价
    CC赋值:1日前的收盘价
    输出CDP:(CH+CL+CC)/3
    输出AH:2*CDP+CH-2*CL
    输出NH:CDP+CDP-CL
    输出NL:CDP+CDP-CH
    输出AL:2*CDP-2*CH+CL
    '''
    CH = REF(HIGH, 1)
    CL = REF(LOW, 1)
    CC = REF(CLOSE, 1)
    CDP = (CH + CL + CC) / 3
    AH = 2 * CDP + CH - 2 * CL
    NH = CDP + CDP - CL
    NL = CDP + CDP - CH
    AL = 2 * CDP - 2 * CH + CL
    return CDP, AH, NH, NL, AL
def TBP_STD(HIGH,LOW,CLOSE):
    '''
    趋势平衡点
    APX赋值:(最高价+最低价+收盘价)/3
    TR0赋值:最高价-最低价和最高价-1日前的收盘价的绝对值和最低价-1日前的收盘价的绝对值的较大值的较大值
    MF0赋值:收盘价-2日前的收盘价
    MF1赋值:1日前的MF0
    MF2赋值:2日前的MF0
    DIRECT1赋值:上次MF0>MF1ANDMF0>MF2距今天数
    DIRECT2赋值:上次MF0<MF1ANDMF0<MF2距今天数
    DIRECT0赋值:如果DIRECT1<DIRECT2,返回100,否则返回-100
    输出TBP:1日前的1日前的收盘价+如果DIRECT0>50,返回MF0和MF1的较小值,否则返回MF0和MF1的较大值
    输出多头获利:1日前的如果DIRECT0>50,返回APX*2-最低价,否则返回无效数,NODRAW
    输出多头停损:1日前的如果DIRECT0>50,返回APX-TR0,否则返回无效数,NODRAW
    输出空头回补:1日前的如果DIRECT0<-50,返回APX*2-最高价,否则返回无效数,NODRAW
    输出空头停损:1日前的如果DIRECT0<-50,返回APX+TR0,否则返回无效数,NODRAW
    '''
    H=HIGH
    L=LOW
    C=CLOSE
    APX=(H+L+C)/3
    TR0=MAX(H-L,MAX(ABS(H-REF(C,1)),ABS(L-REF(C,1))))
    MF0=C-REF(C,2)
    MF1=REF(MF0,1)
    MF2=REF(MF0,2)
    DIRECT1=BARSLAST(np.logical_and(MF0>MF1,MF0>MF2))
    DIRECT2=BARSLAST(np.logical_and(MF0<MF1,MF0<MF2))
    DIRECT0=IF(DIRECT1<DIRECT2,100,-100)
    TBP=REF(REF(C,1)+IF(DIRECT0>50,MIN(MF0,MF1),MAX(MF0,MF1)),1)
    多头获利=REF(IF(DIRECT0>50,APX*2-L,None),1)
    多头停损=REF(IF(DIRECT0>50,APX-TR0,None),1)
    空头回补=REF(IF(DIRECT0<-50,APX*2-H,None),1)
    空头停损=REF(IF(DIRECT0<-50,APX+TR0,None),1)
    return TBP,多头获利,多头停损,空头回补,空头停损
#***********************************************
#***********************************************
#****************有空写****************************
# 参考解析例子
from xg_tdx_func.xg_tdx_func import *
from qmt_trader.unification_data_qmt import unification_data_qmt
class band_supe_buy_sell:
    def __init__(self,df) -> None:
        self.df=df
    def band_supe_buy_sell(self):
        '''
        波段超级买卖
        尊重市场1赋值:收盘价的6.5日[1日权重]移动平均
        尊重市场2赋值:收盘价的13.5日[1日权重]移动平均
        尊重市场11赋值:收盘价的3日[1日权重]移动平均
        尊重市场21赋值:收盘价的8日[1日权重]移动平均
        当满足条件尊重市场1>尊重市场2时,在尊重市场1和尊重市场2位置之间画柱状线,宽度为2.5,0不为0则画空心柱.,画红色,线宽为2
        当满足条件尊重市场2>尊重市场1时,在尊重市场1和尊重市场2位置之间画柱状线,宽度为2.5,0不为0则画空心柱.,画蓝色,线宽为2
        当满足条件尊重市场1上穿尊重市场2时,在最低价*0.98位置画5号图标
        当满足条件尊重市场21上穿尊重市场11时,在最高价*1.02位置书写文字,画黄色
        BBI赋值:(收盘价的3日简单移动平均+收盘价的6日简单移动平均+收盘价的12日简单移动平均+收盘价的24日简单移动平均)/4
        UPR赋值:BBI+3*BBI的13日估算标准差,线宽为2
        DWN赋值:BBI-3*BBI的13日估算标准差
        安全赋值:收盘价的60日简单移动平均,线宽为2
        LC赋值:1日前的收盘价
        RSI赋值:收盘价-LC和0的较大值的6日[1日权重]移动平均/收盘价-LC的绝对值的6日[1日权重]移动平均*100
        A7赋值:(2*收盘价+最高价+最低价)/4
        输出操作线:A7的5日简单移动平均,线宽为1
        操作线1赋值:A7的5日简单移动平均*1.03,线宽为2
        操作线2赋值:A7的5日简单移动平均*0.97,线宽为2
        输出ABC1:21日内A7的最低值
        输出ABC2:21日内A7的最高值
        SK赋值:(A7-ABC1)/(ABC2-ABC1)*100的7日指数移动平均
        SD赋值:0.667*1日前的SK+0.333*SK的5日指数移动平均
        当满足条件如果统计8日中满足收盘价<1日前的收盘价的天数/8>6/10ANDVOL>=1.5*成交量(手)的5日简单移动平均ANDCOUNT(SK>=SD,3)ANDREF(最低价,1)=120日内最低价的最低值,返回1,否则返回0时,在最低价*0.98位置画9号图标
        当满足条件如果统计13日中满足收盘价<1日前的收盘价的天数/13>6/10ANDCOUNT(SK>SD,6)ANDREF(最低价,5)=120日内最低价的最低值ANDREF(收盘价>=开盘价,4)ANDREF(收阳线,3)ANDREF(收阳线,2)ANDREF(开盘价>CLOS,返回?,否则返回?时,在,1)ANDOPEN>1日前的收盘价,1,0)位置书写文字 ,画黄色
        当满足条件如果统计13日中满足收盘价<1日前的收盘价的天数/13>6/10ANDCOUNT(SK>SD,6)ANDREF(最低价,5)=120日内最低价的最低值ANDREF(收盘价>=开盘价,4)ANDREF(收阳线,3)ANDREF(收阳线,2)ANDREF(开盘价>CLOS,返回?,否则返回?时,在,1)ANDOPEN>1日前的收盘价,1,0)位置画最低价*0.98号图标
        '''
        df=self.df
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
        尊重市场1=SMA(C,6.5,1)
        尊重市场2=SMA(C,13.5,1)
        尊重市场11=SMA(C,3,1)
        尊重市场21=SMA(C,8,1)
        '''
        STICKLINE(尊重市场1>尊重市场2 , 尊重市场1,尊重市场2 ,2.5, 0),COLORRED,LINETHICK2;
        STICKLINE(尊重市场2>尊重市场1,尊重市场1,尊重市场2,2.5,0),COLORBLUE,LINETHICK2;
        '''
        df['柱子']=IF(尊重市场1>尊重市场2,'红色','蓝色')
        #DRAWICON( CROSS(尊重市场1,尊重市场2),L*0.98,5);
        df['笑脸']=CROSS(尊重市场1,尊重市场2)
        #DRAWTEXT(CROSS(尊重市场21,尊重市场11),H*1.02,''),COLORYELLOW;
        df['标记文字']=CROSS(尊重市场21,尊重市场11)
        BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
        UPR=BBI+3*STD(BBI,13)
        DWN=BBI-3*STD(BBI,13)
        安全=MA(CLOSE,60)
        LC=REF(CLOSE,1)
        RSI=SMA(MAX(CLOSE-LC,0),6,1)/SMA(ABS(CLOSE-LC),6,1)*100
        A7=(2*C+H+L)/4
        操作线=MA(A7,5)
        df['操作线']=操作线
        操作线1=MA(A7,5)*1.03
        df['操作线1']=操作线1
        操作线2=MA(A7,5)*0.97
        df['操作线2']=操作线2
        ABC1=LLV(A7,21)
        ABC2=HHV(A7,21)
        SK=EMA((A7-ABC1)/(ABC2-ABC1)*100,7)
        SD=EMA(0.667*REF(SK,1)+0.333*SK,5)
        '''
        DRAWICON(IF(COUNT(CLOSE<REF(CLOSE,1),8)/8>6/10 AND VOL>=1.5*MA(VOL,5) AND
        COUNT(SK>=SD,3) AND REF(LOW,1)=LLV(LOW,120),1,0),L*0.98,9);
        {DRAWTEXT(IF(COUNT(CLOSE<REF(CLOSE,1),8)/8>6/10 AND VOL>=1.5*MA(VOL,5) AND
        COUNT(SK>=SD,3) AND REF(LOW,1)=LLV(LOW,120),1,0),LOW*0.98,'底买') ,COLOR0099FF;}
        DRAWTEXT(IF(COUNT(CLOSE<REF(CLOSE,1),13)/13>6/10 AND
        COUNT(SK>SD,6) AND REF(LOW,5)=LLV(LOW,120) AND REF(CLOSE>=OPEN,4) AND
        REF(CLOSE>OPEN,3) AND REF(CLOSE>OPEN,2) AND REF(OPEN>CLOSE,1) AND
        OPEN>REF(CLOSE,1),1,0),LOW*0.98,'底买') ,COLORYELLOW;
        DRAWICON(IF(COUNT(CLOSE<REF(CLOSE,1),13)/13>6/10 AND
        COUNT(SK>SD,6) AND REF(LOW,5)=LLV(LOW,120) AND REF(CLOSE>=OPEN,4) AND
        REF(CLOSE>OPEN,3) AND REF(CLOSE>OPEN,2) AND REF(OPEN>CLOSE,1) AND
        OPEN>REF(CLOSE,1),1,0),L*0.98,9);
        '''
        趋势=CLOSE>=操作线
        df['趋势']=CLOSE>=操作线
        df['stats']=IF(AND(趋势,尊重市场1>尊重市场2),"B","S")
        return df
if __name__=='__main__':
    data=unification_data_qmt()
    df=data.get_hist_data_em(stock='513100')
    modes=band_supe_buy_sell(df=df)
    result=modes.band_supe_buy_sell()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考2from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class dingniu_periodic_resonance_master_diagram:
    def __init__(self,df) :
        '''
        鼎牛周期共振主图
        '''
        self.df=df
    def dingniu_periodic_resonance_master_diagram(self):
        '''
        ACB1赋值:收盘价的12日指数移动平均-收盘价的26日指数移动平均
        ACB2赋值:ACB1的9日指数移动平均
        ACB3赋值:ACB1>ACB2
        ACB4赋值:(收盘价-12日内最低价的最低值)/(12日内最高价的最高值-12日内最低价的最低值)*100
        ACB5赋值:ACB4的3日[1日权重]移动平均
        ACB6赋值:ACB5的3日[1日权重]移动平均
        ACB7赋值:ACB5>ACB6
        ACB8赋值:1日前的收盘价
        ACB9赋值:收盘价-ACB8和0的较大值的9日[1日权重]移动平均/收盘价-ACB8的绝对值的9日[1日权重]移动平均*100
        ACB10赋值:收盘价-ACB8和0的较大值的26日[1日权重]移动平均/收盘价-ACB8的绝对值的26日[1日权重]移动平均*100
        ACB11赋值:ACB9>ACB10
        ACB12赋值:ACB4的3日[1日权重]移动平均
        ACB13赋值:ACB12的3日[1日权重]移动平均
        ACB14赋值:ACB12>ACB13
        ACB15赋值:(收盘价的3日简单移动平均+收盘价的9日简单移动平均+收盘价的12日简单移动平均+收盘价的26日简单移动平均)/4
        ACB16赋值:收盘价>ACB15
        ACB17赋值:收盘价-1日前的收盘价
        ACB18赋值:100*ACB17的9日指数移动平均的9日指数移动平均/ACB17的绝对值的9日指数移动平均的3日指数移动平均
        ACB19赋值:100*ACB17的26日指数移动平均的12日指数移动平均/ACB17的绝对值的26日指数移动平均的12日指数移动平均
        ACB20赋值:ACB18>ACB19
        ACB21赋值:以0.9为权重(最高价+最低价+收盘价*2)/4的动态移动平均
        ACB22赋值:1日前的ACB21的3日指数移动平均
        ACB23赋值:成交量(手)/((最高价-最低价)*2-收盘价-开盘价的绝对值)
        ACB24赋值:如果收阳线,返回ACB23*(最高价-最低价),否则返回如果收阴线,返回ACB23*(最高价-开盘价+收盘价-最低价),否则返回成交量(手)/2+如果收阳线,返回0-ACB23*(最高价-收盘价+开盘价-最低价),否则返回如果收阴线,返回0-ACB23*(最高价-最低价),否则返回0-成交量(手)/2
        ACB25赋值:ACB24/20/1.15
        ACB26赋值:ACB25*0.55+1日前的ACB25*0.33+2日前的ACB25*0.22
        ACB27赋值:ACB26的8日指数移动平均
        ACB28赋值:ACB26的3日指数移动平均
        ACB29赋值:ACB28
        ACB30赋值:成交量(手)
        ACB31赋值:ACB30的5日简单移动平均
        ACB32赋值:ACB30的10日简单移动平均
        ACB33赋值:ACB31>=ACB32
        ACB34赋值:ACB29>=0
        ACB35赋值:ACB34 AND ACB33
        当满足条件ACB35时,在最低价位置画1号图标
        ACB36赋值:KDJ的K(9,3,3)的5日简单移动平均
        ACB37赋值:收盘价的12/2日指数移动平均-收盘价的26/2日指数移动平均
        ACB38赋值:ACB37的9/2日指数移动平均
        ACB39赋值:ACB36>=1日前的ACB36 AND ACB37>=ACB38
        ABC51赋值:(最高价+最低价+收盘价*2)/4
        ABC52赋值:ABC51的17日指数移动平均
        ABC53赋值:ABC51的17日估算标准差
        ABC54赋值:((ABC51-ABC52)/ABC53*100+200)/4
        ABC55赋值:(ABC54的5日指数移动平均-25)*1.56
        ABC56赋值:ABC55的2日指数移动平均*1.22
        ABC57赋值:ABC56的2日指数移动平均
        当满足条件ABC56-ABC57>0时,在开盘价和收盘价位置之间画柱状线,宽度为3,1不为0则画空心柱.,画红色
        当满足条件ABC56-ABC57<0时,在开盘价和收盘价位置之间画柱状线,宽度为3,0不为0则画空心柱.,画绿色
        当满足条件ABC56-ABC57>0ANDREF(ABC56-ABC57<0,1)时,在开盘价和收盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画黄色
        当满足条件ABC56-ABC57>0ANDABC56-ABC57<1日前的ABC56-ABC57ANDABC57>110时,在开盘价和收盘价位置之间画柱状线,宽度为3,0不为0则画空心柱.,画淡红色
        涨停赋值:如果(收盘价-1日前的收盘价)*100/1日前的收盘价>=9.80,返回1,否则返回0
        涨停牛赋值:最近2日一直存在涨停
        当满足条件涨停牛时,在最低价*1.02位置书写文字,画黄色
        输出操作线:收盘价的5日简单移动平均,COLORFFFFFF,线宽为1
        输出趋势线:收盘价的10日简单移动平均,画红色,线宽为1
        画带状线
        AA赋值:收盘价>收盘价的10日简单移动平均
        MA5赋值:收盘价的5日简单移动平均
        MA10赋值:收盘价的10日简单移动平均
        多头排列赋值:MA5>MA10
        当满足条件ACB35时,在开盘价和收盘价位置之间画柱状线,宽度为2,0不为0则画空心柱.,画洋红色
        当满足条件涨停牛时,在开盘价和收盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画黄色
        共振赋值:条件连续成立次数=1
        当满足条件共振时,在最低价位置书写文字,画黄色
        当满足条件共振时,在最低价位置画9号图标
        '''
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        VOL=df['volume']
        V=df['volume']
        ACB1=EMA(CLOSE,12)-EMA(CLOSE,26)
        ACB2=EMA(ACB1,9)
        ACB3=ACB1>ACB2
        ACB4=(CLOSE-LLV(LOW,12))/(HHV(HIGH,12)-LLV(LOW,12))*100
        ACB5=SMA(ACB4,3,1)
        ACB6=SMA(ACB5,3,1)
        ACB7=ACB5>ACB6
        ACB8=REF(CLOSE,1)
        ACB9=SMA(MAX(CLOSE-ACB8,0),9,1)/SMA(ABS(CLOSE-ACB8),9,1)*100
        ACB10=SMA(MAX(CLOSE-ACB8,0),26,1)/SMA(ABS(CLOSE-ACB8),26,1)*100
        ACB11=ACB9>ACB10
        ACB12=SMA(ACB4,3,1)
        ACB13=SMA(ACB12,3,1)
        ACB14=ACB12>ACB13
        ACB15=(MA(CLOSE,3)+MA(CLOSE,9)+MA(CLOSE,12)+MA(CLOSE,26))/4
        ACB16=CLOSE>ACB15
        ACB17=CLOSE-REF(CLOSE,1)
        ACB18=100*EMA(EMA(ACB17,9),9)/EMA(EMA(ABS(ACB17),9),3)
        ACB19=100*EMA(EMA(ACB17,26),12)/EMA(EMA(ABS(ACB17),26),12)
        ACB20=ACB18>ACB19
        ACB21=DMA((HIGH+LOW+CLOSE*2)/4,0.9)
        ACB22=REF(EMA(ACB21,3),1)
        ACB23=VOL/((HIGH-LOW)*2-ABS(CLOSE-OPEN))
        ACB24=IF(CLOSE>OPEN,ACB23*(HIGH-LOW),IF(CLOSE< OPEN,ACB23*(HIGH-OPEN+CLOSE-LOW),VOL/2))+IF(CLOSE>OPEN,0-ACB23*(HIGH-CLOSE+OPEN-LOW),IF(CLOSE< OPEN,0-ACB23*(HIGH-LOW),0-VOL/2))
        ACB25=ACB24/20/1.15
        ACB26=ACB25*0.55+REF(ACB25,1)*0.33+REF(ACB25,2)*0.22
        ACB27=EMA(ACB26,8)
        ACB28=EMA(ACB26,3)
        ACB29=ACB28
        ACB30=VOL
        ACB31=MA(ACB30,5)
        ACB32=MA(ACB30,10)
        ACB33=ACB31>=ACB32
        ACB34=ACB29>=0
        ACB35=AND(ACB34,ACB33)
        #标记箭头
        #DRAWICON(ACB35,L,1)
        ACB36=MA(KDJ(CLOSE=CLOSE,LOW=LOW,HIGH=HIGH)[0],5)
        ACB37=EMA(CLOSE,12/2)-EMA(CLOSE,26/2)
        ACB38=EMA(ACB37,9/2)
        ACB39=AND(ACB36>=REF(ACB36,1),ACB37>=ACB38)
        ABC51=(HIGH+LOW+CLOSE*2)/4
        ABC52=EMA(ABC51,17)
        ABC53=STD(ABC51,17)
        ABC54=((ABC51-ABC52)/ABC53*100+200)/4
        ABC55=(EMA(ABC54,5)-25)*1.56
        ABC56=EMA(ABC55,2)*1.22
        ABC57=EMA(ABC56,2)
        #STICKLINE(ABC56-ABC57>0,O,C,3,1),COLORRED
        df['红色柱子']=ABC56-ABC57>0
        #STICKLINE(ABC56-ABC57<0,O,C,3,0),COLORGREEN;
        df['绿色柱子']=ABC56-ABC57<0
        #STICKLINE(ABC56-ABC57>0 AND REF(ABC56-ABC57< 0,1),O,C,1,0),COLORYELLOW;
        df['黄色柱子']=AND(ABC56-ABC57>0,REF(ABC56-ABC57< 0,1))
        #STICKLINE(ABC56-ABC57>0 AND ABC56-ABC57< REF(ABC56-ABC57,1) AND ABC57>110,O,C,3,0),COLORLIRED;
        df['淡红色柱子']=AND(ABC56-ABC57>0,AND(ABC56-ABC57< REF(ABC56-ABC57,1),ABC57>110))
        涨停=IF((C-REF(C,1))*100/REF(C,1)>=9.80,1,0)
        df['涨停']=涨停
        涨停牛=EVERY(涨停,2)
        #DRAWTEXT(涨停牛,L*1.02,'↙牛'),COLORYELLOW;
        df['涨停牛']=涨停牛
        操作线=MA(CLOSE,5)
        趋势线=MA(CLOSE,10)
        #DRAWBAND(操作线,RGB(255,50,50),趋势线,RGB(10,204,60));
        df['条形线']=IF(操作线>=趋势线,'红色','绿色')
        AA=C>MA(C,10); 
        MA5=MA(C,5)
        MA10=MA(C,10)
        多头排列=MA5>MA10
        #STICKLINE(ACB35,O,C,2,0),COLORMAGENTA;
        #STICKLINE(涨停牛,OPEN,CLOSE,1,0),COLORYELLOW;
        共振=BARSLASTCOUNT(AND(ABC56-ABC57>0,AND(多头排列,AA)))==1
        df['共振']=共振
        #DRAWTEXT(共振,L,'★共振'),COLORYELLOW;  
        #DRAWICON(共振,L,9);
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='159632',start_date='19990101')
    print(df)
    modes=dingniu_periodic_resonance_master_diagram(df=df)
    result=modes.dingniu_periodic_resonance_master_diagram()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考3
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
A
class dingniu_periodic_resonance_subdiagram:
    def __init__(self,df) :
        '''
        鼎牛共振副图
        '''
        self.df=df
    def dingniu_periodic_resonance_subdiagram(self):
        '''
        ABC51赋值:(最高价+最低价+收盘价*2)/4
        ABC52赋值:ABC51的17日指数移动平均
        ABC53赋值:ABC51的17日估算标准差
        ABC54赋值:((ABC51-ABC52)/ABC53*100+200)/4
        ABC55赋值:(ABC54的5日指数移动平均-25)*1.56
        ABC56赋值:ABC55的2日指数移动平均*1.22
        ABC57赋值:ABC56的2日指数移动平均
        当满足条件ABC56-ABC57>0时,在0.2和0.4位置之间画柱状线,宽度为3,0不为0则画空心柱.,画红色
        当满足条件ABC56-ABC57<0时,在0.2和0.4位置之间画柱状线,宽度为3,0不为0则画空心柱.,画绿色
        当满足条件ABC56-ABC57>0ANDREF(ABC56-ABC57<0,1)时,在0.2和0.4位置之间画柱状线,宽度为3.05,0不为0则画空心柱.,COLOR000099
        当满足条件ABC56-ABC57>0ANDREF(ABC56-ABC57<0,1)时,在0.2和0.4位置之间画柱状线,宽度为2.2,0不为0则画空心柱.,COLOR0000CC
        当满足条件ABC56-ABC57>0ANDREF(ABC56-ABC57<0,1)时,在0.2和0.4位置之间画柱状线,宽度为1.5,0不为0则画空心柱.,画红色
        当满足条件ABC56-ABC57>0ANDREF(ABC56-ABC57<0,1)时,在0.2和0.4位置之间画柱状线,宽度为0.5,0不为0则画空心柱.,画黄色
        当满足条件ABC56-ABC57>0ANDABC56-ABC57<1日前的ABC56-ABC57ANDABC57>110时,在0.2和0.4位置之间画柱状线,宽度为3,0不为0则画空心柱.,画淡红色
        '''
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        VOL=df['volume']
        V=df['volume']
        ABC51=(HIGH+LOW+CLOSE*2)/4
        ABC52=EMA(ABC51,17)
        ABC53=STD(ABC51,17)
        ABC54=((ABC51-ABC52)/ABC53*100+200)/4
        ABC55=(EMA(ABC54,5)-25)*1.56
        ABC56=EMA(ABC55,2)*1.22
        ABC57=EMA(ABC56,2)
        '''
        STICKLINE(ABC56-ABC57>0,0.2,0.4,3,0),COLORRED
        STICKLINE(ABC56-ABC57< 0,0.2,0.4,3,0),COLORGREEN
        '''
        df['柱子']=IF(ABC56-ABC57>0,"红色",'绿色')
        #STICKLINE(ABC56-ABC57>0 AND REF(ABC56-ABC57< 0,1),0.2,0.4,3.05,0),COLOR000099
        #STICKLINE(ABC56-ABC57>0 AND REF(ABC56-ABC57< 0,1),0.2,0.4,2.2,0),COLOR0000CC
        '''
        STICKLINE(ABC56-ABC57>0 AND REF(ABC56-ABC57< 0,1),0.2,0.4,1.5,0),COLORRED
        STICKLINE(ABC56-ABC57>0 AND REF(ABC56-ABC57< 0,1),0.2,0.4,0.5,0),COLORYELLOW
        '''
        df['起点']=AND(ABC56-ABC57>0,REF(ABC56-ABC57< 0,1))
        #STICKLINE(ABC56-ABC57>0 AND ABC56-ABC57< REF(ABC56-ABC57,1) AND ABC57>110,0.2,0.4,3,0),COLORLIRED
        df['淡红色']=AND(ABC56-ABC57>0,AND(ABC56-ABC57< REF(ABC56-ABC57,1),ABC57>110))
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='159619',start_date='19990101')
    print(df)
    modes=dingniu_periodic_resonance_subdiagram(df=df)
    result=modes.dingniu_periodic_resonance_subdiagram()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考4
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class main_approach_to_capture_dark_horse_main_figure:
    def __init__(self,df):
        
        self.df=df
    def main_approach_to_capture_dark_horse_main_figure(self):
        '''
        一、主图：
        1、灰色K线，底部保持关注；
        2、黄色K线，底部酌情买入；
        3、红色K线，强势持仓阶段；
        4、粉红K线，阶段开始减仓；
        5、青色K线，准备清仓卖出；
        6、绿色K线，要大跌，卖出；
        7、“红色圆球”黑马启动信号；
        8、白虚线上持有，线下休息。
        二、副图：
        1、红柱子，主力吸筹；
        2、紫色柱，主力入场；
        3、绿色柱，主力离场；
        4、先吸筹，后入场买；
        5、保留了“买、卖、追涨”等信号参考；
        输出MA5:收盘价的5日简单移动平均DOTLINE 画白色
        N赋值:30
        M赋值:13
        赋值: 1日前的收盘价
        RSI1赋值:收盘价-LC和0的较大值的13日[1日权重]移动平均/收盘价-LC的绝对值的13日[1日权重]移动平均*100
        RSIF赋值:90-RSI1,COLOR33DD33
        A4赋值:((收盘价-33日内最低价的最低值)/(33日内最高价的最高值-33日内最低价的最低值))*67
        AAC22赋值:10日内最低价的最低值
        AAC33赋值:25日内最高价的最高值
        动力线赋值:(收盘价-AAC22)/(AAC33-AAC22)*4的4日指数移动平均
        RSV赋值:(收盘价-9日内最低价的最低值)/(9日内最高价的最高值-9日内最低价的最低值)*100
        ABB1赋值:RSV的3日[1日权重]移动平均
        ABB2赋值:ABB1的3日[1日权重]移动平均
        ABB3赋值:3*ABB1-2*ABB2
        ABC1赋值:(最低价+最高价+收盘价*2)/4
        ABC2赋值: ABC1的4日简单移动平均
        ABC3赋值:10日内ABC2的最高值
        ABC4赋值:ABC3的3日简单移动平均
        ABC5赋值:1.25*ABC4-0.25*ABC3
        XKKJ赋值:如果ABC5>ABC3,返回ABC3,否则返回ABC5
        ACB1赋值:10日内ABC2的最低值
        ACB2赋值:ACB1的3日简单移动平均
        ACB3赋值:1.25*ACB2-0.25*ACB1
        DKKJ赋值:如果ACB3<ACB1,返回ACB1,否则返回ACB3
        MA13赋值:收盘价的13日简单移动平均
        ZDHM赋值:收盘价上穿DKKJ AND 收盘价上穿MA13 AND 收盘价上穿XKKJ
        ZHM赋值:收盘价上穿MA13 AND 收盘价上穿XKKJ
        当满足条件(ZDHMORZHM)时,在最低价位置画13号图标
        当满足条件(ZDHMORZHM)时,在收盘价和开盘价位置之间画柱状线,宽度为2,0不为0则画空心柱.,画洋红色
        当满足条件(ZDHMORZHM)时,在最低价位置书写文字,画黄色

        当满足条件动力线>0AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画深灰色
        当满足条件动力线>=0.2AND动力线<0.5AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画深灰色
        当满足条件动力线>=0.5AND动力线<1.75AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画黄色
        当满足条件动力线>=1.75AND动力线<3.2AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画红色
        当满足条件动力线>=3.2AND动力线<3.45AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画淡红色
        当满足条件动力线>=3.45时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱. AND ABB3<ABB1,画青色
        当满足条件ABB3<ABB1时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画绿色
        '''
        df=self.df
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
        MA5=MA(CLOSE,5)#DOTLINE COLORWHITE;
        N=30
        M=13
        LC = REF(CLOSE,1)
        RSI1=SMA(MAX(CLOSE-LC,0),13,1)/SMA(ABS(CLOSE-LC),13,1)*100
        RSIF=90-RSI1#COLOR33DD33;
        A4=((C-LLV(L,33))/(HHV(H,33)-LLV(L,33)))*67
        AAC22=LLV(LOW,10)
        AAC33=HHV(HIGH,25)
        动力线=EMA((CLOSE-AAC22)/(AAC33-AAC22)*4,4)
        RSV=(C-LLV(L,9))/(HHV(H,9)-LLV(L,9))*100
        ABB1=SMA(RSV,3,1)
        ABB2=SMA(ABB1,3,1)
        ABB3=3*ABB1-2*ABB2
        ABC1=(LOW+HIGH+CLOSE*2)/4
        ABC2= MA(ABC1,4)
        ABC3=HHV(ABC2,10)
        ABC4=MA(ABC3,3)
        ABC5=1.25*ABC4-0.25*ABC3
        XKKJ=IF(ABC5>ABC3,ABC3,ABC5)
        ACB1=LLV(ABC2,10)
        ACB2=MA(ACB1,3)
        ACB3=1.25*ACB2-0.25*ACB1
        DKKJ=IF(ACB3<ACB1,ACB1,ACB3)
        MA13=MA(C,13)
        ZDHM=AND(AND(CROSS(C,DKKJ),CROSS(C,MA13)) ,CROSS(C,XKKJ))
        ZHM=AND(CROSS(C,MA13),CROSS(C,XKKJ))
        #DRAWICON((ZDHM OR ZHM),L,13);
        #STICKLINE((ZDHM OR ZHM),C,O,2,0),COLORMAGENTA;
        #DRAWTEXT((ZDHM OR ZHM),L,' ★黑马'),COLORYELLOW;
        df['黑马']=IF(OR(ZDHM,ZHM),True,False)[1:]
        #当满足条件动力线>0AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画深灰色
        #STICKLINE(动力线>0 AND ((ABB3>ABB1 AND ABB3<REF(ABB3,1)) OR ABB3>ABB1),C,O,1,0),COLORGRAY;
        df['深灰色']=OR(AND(动力线>0,AND(ABB3>ABB1,ABB3<REF(ABB3,1))),ABB3>ABB1)
        #当满足条件动力线>=0.2AND动力线<0.5AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画深灰色
        #STICKLINE(动力线>=0.2 AND 动力线<0.5 AND ((ABB3>ABB1 AND ABB3<REF(ABB3,1)) OR ABB3>ABB1),C,O,1,0),COLORGRAY;
        df['深灰色']=OR(AND(AND(动力线>=0.2,动力线<0.5),AND(ABB3>ABB1 , ABB3<REF(ABB3,1))),ABB3>ABB1)
        #当满足条件动力线>=0.5AND动力线<1.75AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画黄色
        #STICKLINE(动力线>=0.5 AND 动力线<1.75 AND ((ABB3>ABB1 AND ABB3<REF(ABB3,1)) OR ABB3>ABB1),C,O,1,0),COLORYELLOW;
        df['黄色']=OR(AND(AND(动力线>=0.5,动力线<1.75),AND(ABB3>ABB1,ABB3<REF(ABB3,1))),ABB3>ABB1)
        #当满足条件动力线>=1.75AND动力线<3.2AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画红色
        #STICKLINE(动力线>=1.75 AND 动力线<3.2 AND ((ABB3>ABB1 AND ABB3<REF(ABB3,1)) OR ABB3>ABB1),C,O,1,0),COLORRED;
        df['红色']=OR(AND(AND(动力线>=1.75 ,动力线<3.2) ,AND(ABB3>ABB1,ABB3<REF(ABB3,1))), ABB3>ABB1)
        #当满足条件动力线>=3.2AND动力线<3.45AND((ABB3>ABB1ANDABB3<1日前的ABB3)ORABB3>ABB1)时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画淡红色
        #STICKLINE(动力线>=3.2 AND 动力线<3.45 AND ((ABB3>ABB1 AND ABB3<REF(ABB3,1)) OR ABB3>ABB1),C,O,1,0),COLORLIRED;
        df['淡红色']=OR(AND(AND(动力线>=3.2,动力线<3.45),AND(ABB3>ABB1,ABB3<REF(ABB3,1))) , ABB3>ABB1)
        #当满足条件动力线>=3.45时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱. AND ABB3<ABB1,画青色
        #STICKLINE(动力线>=3.45,C,O,1,0) AND ABB3<ABB1,COLORCYAN;
        df['青色']=AND(动力线>=3.45,ABB3<ABB1)
        #当满足条件ABB3<ABB1时,在收盘价和开盘价位置之间画柱状线,宽度为1,0不为0则画空心柱.,画绿色
        #STICKLINE(ABB3<ABB1,C,O,1,0),COLORGREEN;
        df['绿色']=ABB3<ABB1
        return df 
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='513100')
    modes=main_approach_to_capture_dark_horse_main_figure(df=df)
    result=modes.main_approach_to_capture_dark_horse_main_figure()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考5
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class main_approach_to_capture_the_dark_horse_deputy_map:
    def __init__(self,df=''):
        '''
        主力进场擒黑马副图
        '''
        self.df=df
    def main_approach_to_capture_the_dark_horse_deputy_map(self):
        """
        N赋值:30
        M赋值:13
        LC赋值:1日前的收盘价
        RSI1赋值:收盘价-LC和0的较大值的13日[1日权重]移动平均/收盘价-LC的绝对值的13日[1日权重]移动平均*100
        RSIF赋值:90-RSI1,COLOR33DD33
        A4赋值:((收盘价-33日内最低价的最低值)/(33日内最高价的最高值-33日内最低价的最低值))*67
        ABC1赋值:(9日内最高价的最高值-收盘价)/(9日内最高价的最高值-9日内最低价的最低值)*100-70
        ABC2赋值:ABC1的9日[1日权重]移动平均+100
        ABC3赋值:(收盘价-9日内最低价的最低值)/(9日内最高价的最高值-9日内最低价的最低值)*100
        ABC4赋值:ABC3的3日[1日权重]移动平均
        ABC5赋值:ABC4的3日[1日权重]移动平均+100
        ABC6赋值:ABC5-ABC2
        输出趋势:如果ABC6>45,返回ABC6-45,否则返回0
        当满足条件1日前的趋势<趋势时,在趋势和1日前的趋势位置之间画柱状线,宽度为2,0不为0则画空心柱.,画洋红色
        当满足条件1日前的趋势>趋势时,在趋势和1日前的趋势位置之间画柱状线,宽度为2,0不为0则画空心柱.,画绿色
        强弱分界赋值:50,COLORFFFFCC
        底部赋值:0,COLOR00FFFF
        安全赋值:20,COLORFFFF66,线宽为1
        预警赋值:80,COLORFFFF66,线宽为1
        顶部赋值:100,COLORFFFF33
        V1赋值:10日内最低价的最低值
        V2赋值:25日内最高价的最高值
        价位线赋值:(收盘价-V1)/(V2-V1)*4的4日指数移动平均
        当满足条件价位线上穿0.3时,在20+4位置书写文字,画红色
        当满足条件3.5上穿价位线时,在趋势位置书写文字,画白色
        ABC2Q赋值:1日前的最低价
        ABC3Q赋值:最低价-ABC2Q的绝对值的3日[1日权重]移动平均/最低价-ABC2Q和0的较大值的3日[1日权重]移动平均*100
        ABC4Q赋值:如果收盘价*1.3,返回ABC3Q*10,否则返回ABC3Q/10的3日指数移动平均
        ABC5Q赋值:30日内最低价的最低值
        ABC6Q赋值:30日内ABC4Q的最高值
        ABC7Q赋值:如果收盘价的58日简单移动平均,返回1,否则返回0
        ABC8Q赋值:如果最低价<=ABC5Q,返回(ABC4Q+ABC6Q*2)/2,否则返回0的3日指数移动平均/618*ABC7Q
        ABC9Q赋值:如果ABC8Q>100,返回100,否则返回ABC8Q
        ACB3赋值:(21日内最高价的最高值-收盘价)/(21日内最高价的最高值-21日内最低价的最低值)*100-10
        ACB4赋值:(收盘价-21日内最低价的最低值)/(21日内最高价的最高值-21日内最低价的最低值)*100
        ACB5赋值:ACB4的13日[8日权重]移动平均
        走势赋值:ACB5的13日[8日权重]移动平均的向上舍入
        ACB6赋值:ACB3的21日[8日权重]移动平均
        卖临界赋值:当满足条件走势-ACB6>85时,在103和100位置之间画柱状线,宽度为15,1不为0则画空心柱.,画红色,线宽为2
        主力线赋值:3*(收盘价-27日内最低价的最低值)/(27日内最高价的最高值-27日内最低价的最低值)*100的5日[1日权重]移动平均-2*(收盘价-27日内最低价的最低值)/(27日内最高价的最高值-27日内最低价的最低值)*100的5日[1日权重]移动平均的3日[1日权重]移动平均,线宽为2,画蓝色
        超短线赋值:(((主力线-21日内主力线的最低值)/(21日内主力线的最高值-21日内主力线的最低值))*(4))*(25),线宽为2,画蓝色
        ABC11赋值:1日前的(最低价+开盘价+收盘价+最高价)/4
        ABC21赋值:最低价-ABC11的绝对值的13日[1日权重]移动平均/最低价-ABC11和0的较大值的10日[1日权重]移动平均
        ABC31赋值:ABC21的10日指数移动平均
        ABC41赋值:33日内最低价的最低值
        ABC51赋值:如果最低价<=ABC41,返回ABC31,否则返回0的3日指数移动平均
        输出主力吸筹:如果ABC51>1日前的ABC51,返回ABC51,否则返回0,画红色,NODRAW
        当满足条件ABC51>1日前的ABC51时,在0和ABC51位置之间画柱状线,宽度为3,0不为0则画空心柱.,COLOR000055
        当满足条件ABC51>1日前的ABC51时,在0和ABC51位置之间画柱状线,宽度为2.6,0不为0则画空心柱.,COLOR000077
        当满足条件ABC51>1日前的ABC51时,在0和ABC51位置之间画柱状线,宽度为2.1,0不为0则画空心柱.,COLOR000099
        当满足条件ABC51>1日前的ABC51时,在0和ABC51位置之间画柱状线,宽度为1.5,0不为0则画空心柱.,COLOR0000BB
        当满足条件ABC51>1日前的ABC51时,在0和ABC51位置之间画柱状线,宽度为0.9,0不为0则画空心柱.,COLOR0000DD
        当满足条件ABC51>1日前的ABC51时,在0和ABC51位置之间画柱状线,宽度为0.3,0不为0则画空心柱.,COLOR0000FF
        ABC12赋值:3
        ABC28赋值:(3)*(((收盘价-27日内最低价的最低值)/(27日内最高价的最高值-27日内最低价的最低值))*(100)的5日[1日权重]移动平均) - (2)*(((收盘价-27日内最低价的最低值)/(27日内最高价的最高值-27日内最低价的最低值))*(100)的5日[1日权重]移动平均的3日[1日权重]移动平均)
        动态底部赋值:如果最低价<=30日内最低价的最低值,返回最低价-1日前的最低价的绝对值的30日[1日权重]移动平均/最低价-1日前的最低价和0的较大值的99日[1日权重]移动平均,否则返回0*5的3日指数移动平均
        准备买入赋值:收盘价上穿(收盘价,N,1)*1.02
        输出低点:如果动态底部AND准备买入,返回50,否则返回0,画白色,线宽为3
        RSV11赋值:(收盘价-19日内最低价的最低值)/(19日内最高价的最高值-19日内最低价的最低值)*100
        K赋值:RSV11的3日[1日权重]移动平均
        D赋值:K的3日[1日权重]移动平均
        J赋值:3*K-2*D
        短线赋值:J的6日指数移动平均,画红色
        浮筹赋值:短线的28日简单移动平均*1,线宽为2,画绿色
        空方赋值:100*(35日内最高价的最高值-收盘价)/(35日内最高价的最高值-35日内最低价的最低值)的3日简单移动平均,画黄色
        当满足条件短线上穿浮筹AND短线<36时,在20+4位置画9号图标,画蓝色, 线宽为1
        当满足条件浮筹上穿空方时,在浮筹位置书写文字,画白色
        """
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        low=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        V=df['volume']
        N=30
        M=13
        LC=REF(CLOSE,1)
        RSI1=SMA(MAX(CLOSE-LC,0),13,1)/SMA(ABS(CLOSE-LC),13,1)*100
        RSIF=90-RSI1#,COLOR33DD33;
        A4=((C-LLV(L,33))/(HHV(H,33)-LLV(L,33)))*67
        ABC1=(HHV(HIGH,9)-CLOSE)/(HHV(HIGH,9)-LLV(LOW,9))*100-70
        ABC2=SMA(ABC1,9,1)+100
        ABC3=(CLOSE-LLV(LOW,9))/(HHV(HIGH,9)-LLV(LOW,9))*100
        ABC4=SMA(ABC3,3,1)
        ABC5=SMA(ABC4,3,1)+100
        ABC6=ABC5-ABC2
        趋势=IF(ABC6>45,ABC6-45,0)
        '''
        STICKLINE(REF(趋势,1)< 趋势, 趋势,REF(趋势,1),2,0),COLORMAGENTA;

        STICKLINE(REF(趋势,1)> 趋势, 趋势,REF(趋势,1),2,0),COLORGREEN;
        '''
        df['趋势']=IF(REF(趋势,1),"洋红色","绿色")
        强弱分界=50,#COLORFFFFCC;
        底部=0,#COLOR00FFFF;
        安全=20#COLORFFFF66,LINETHICK1;
        预警=80#COLORFFFF66,LINETHICK1;
        顶部=100#,COLORFFFF33;
        V1=LLV(LOW,10)
        V2=HHV(H,25)
        价位线=EMA((C-V1)/(V2-V1)*4,4)
        #DRAWTEXT(CROSS(价位线,0.3),20+4,'●买'),COLORRED;
        df['买']=IF(CROSS(价位线,0.3),"买",None)
        #DRAWTEXT(CROSS(3.5,价位线),趋势,'●卖'),COLORWHITE;
        df['卖']=IF(CROSS(3.5,价位线),"卖",None)
        ABC2Q=REF(LOW,1)
        ABC3Q=SMA(ABS(LOW-ABC2Q),3,1)/SMA(MAX(LOW-ABC2Q,0),3,1)*100
        ABC4Q=EMA(IF(CLOSE*1.3,ABC3Q*10,ABC3Q/10),3)
        ABC5Q=LLV(LOW,30)
        ABC6Q=HHV(ABC4Q,30)
        ABC7Q=IF(MA(CLOSE,58),1,0)
        ABC8Q=EMA(IF(LOW<=ABC5Q,(ABC4Q+ABC6Q*2)/2,0),3)/618*ABC7Q
        ABC9Q=IF(ABC8Q>100,100,ABC8Q)
        ACB3=(HHV(HIGH,21)-CLOSE)/(HHV(HIGH,21)-LLV(LOW,21))*100-10
        ACB4=(CLOSE-LLV(LOW,21))/(HHV(HIGH,21)-LLV(LOW,21))*100
        ACB5=SMA(ACB4,13,8)
        走势=SMA(ACB5,13,8)
        ACB6=SMA(ACB3,21,8)
        df['卖临界']=IF(走势-ACB6>85,'红色柱状',None)
        主力线=3*SMA((CLOSE-LLV(LOW,27))/(HHV(HIGH,27)-LLV(LOW,27))*100,5,1)-2*SMA(SMA((CLOSE-LLV(LOW,27))/(HHV(HIGH,27)-LLV(LOW,27))*100,5,1),3,1)
        超短线=(((主力线-LLV(主力线,21))/(HHV(主力线,21)-LLV(主力线,21)))*(4))*(25)
        ABC11=REF((LOW+OPEN+CLOSE+HIGH)/4,1)
        ABC21=SMA(ABS(LOW-ABC11),13,1)/SMA(MAX(LOW-ABC11,0),10,1)
        ABC31=EMA(ABC21,10)
        ABC41=LLV(LOW,33)
        ABC51=EMA(IF(LOW<=ABC41,ABC31,0),3)
        df['主力吸筹']=IF(ABC51>REF(ABC51,1),ABC51,0)
        '''
        STICKLINE(ABC51>REF(ABC51,1),0,ABC51,3,0 ),COLOR000055;

        STICKLINE(ABC51>REF(ABC51,1),0,ABC51,2.6,0 ),COLOR000077;

        STICKLINE(ABC51>REF(ABC51,1),0,ABC51,2.1,0 ),COLOR000099;

        STICKLINE(ABC51>REF(ABC51,1),0,ABC51,1.5,0 ),COLOR0000BB;

        STICKLINE(ABC51>REF(ABC51,1),0,ABC51,0.9,0 ),COLOR0000DD;

        STICKLINE(ABC51>REF(ABC51,1),0,ABC51,0.3,0 ),COLOR0000FF;
        '''
        ABC12=3
        ABC28=(3)*(SMA(((CLOSE - LLV(LOW,27))/(HHV(HIGH,27) - LLV(LOW,27)))*(100),5,1)) - (2)*(SMA(SMA(((CLOSE - LLV(LOW,27))/(HHV(HIGH,27) - LLV(LOW,27)))*(100),5,1),3,1))
        动态底部=EMA(IF(L<= LLV(L,30),SMA(ABS(L-REF(L,1)),30,1)/SMA(MAX(L-REF(L,1),0),99,1),0)*5,3)
        准备买入=CROSS(C,CLOSE*1.02)
        df['低点']=IF(AND(动态底部, 准备买入[1:]),50,0)
        RSV11=(CLOSE-LLV(LOW,19))/(HHV(HIGH,19)-LLV(LOW,19))*100
        K=SMA(RSV11,3,1)
        D=SMA(K,3,1)
        J=3*K-2*D
        短线=EMA(J,6)
        浮筹=MA(短线,28)*1
        空方=MA(100*(HHV(HIGH,35)-CLOSE)/(HHV(HIGH,35)-LLV(LOW,35)),3)
        #DRAWICON(CROSS(短线,浮筹) AND 短线<36,20+4,9),COLORBLUE, LINETHICK1;
        #DRAWTEXT(CROSS(浮筹,空方),浮筹,' 追')
        df['追']=IF(CROSS(浮筹,空方),"追",None)
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='513100')
    modes=main_approach_to_capture_the_dark_horse_deputy_map(df=df)
    result=modes.main_approach_to_capture_the_dark_horse_deputy_map()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考6
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class nine_finger_resonance:
    def __init__(self,df) :
        '''
        九指共振
        '''
        self.df=df
    def nine_finger_resonance(self):
        '''
        输出DD11:0.95,COLORFF33FF
        输出DD22:2,画绿色
        日K赋值:"KDJ的K"(9,3,3)
        日D赋值:"KDJ的D"(9,3,3)
        当满足条件日K>日D时,在1位置画1号图标
        当满足条件日K<日D时,在1位置画2号图标
        当满足条件是否最后一个周期=1时,在1位置书写文字,COLORFFFFFF
        日DIF赋值:"平滑异同平均线的DIF"(12,26,9)
        日DEA赋值:"平滑异同平均线的DEA"(12,26,9)
        当满足条件日DIF>日DEA时,在1.1位置画1号图标
        当满足条件日DIF<日DEA时,在1.1位置画2号图标
        当满足条件是否最后一个周期=1时,在1.1位置书写文字,COLORFFFFFF
        日RSI赋值:"RSI的RSI1"(9)
        当满足条件日RSI>50时,在1.2位置画1号图标
        当满足条件日RSI<50时,在1.2位置画2号图标
        当满足条件是否最后一个周期=1时,在1.2位置书写文字,COLORFFFFFF
        周K赋值:"KDJ的K"(9,3,3)
        周D赋值:"KDJ的D"(9,3,3)
        当满足条件周K>周D时,在1.3位置画1号图标
        当满足条件周K<周D时,在1.3位置画2号图标
        当满足条件是否最后一个周期=1时,在1.3位置书写文字,COLORFFFFFF
        周DIF赋值:"平滑异同平均线的DIF"(12,26,9)
        周DEA赋值:"平滑异同平均线的DEA"(12,26,9)
        当满足条件周DIF>周DEA时,在1.4位置画1号图标
        当满足条件周DIF<周DEA时,在1.4位置画2号图标
        当满足条件是否最后一个周期=1时,在1.4位置书写文字,COLORFFFFFF
        周RSI赋值:"RSI的RSI1"(9)
        当满足条件周RSI>50时,在1.5位置画1号图标
        当满足条件周RSI<50时,在1.5位置画2号图标
        当满足条件是否最后一个周期=1时,在1.5位置书写文字,COLORFFFFFF
        月K赋值:"KDJ的K"(9,3,3)
        月D赋值:"KDJ的D"(9,3,3)
        当满足条件月K>月D时,在1.6位置画1号图标
        当满足条件月K<月D时,在1.6位置画2号图标
        当满足条件是否最后一个周期=1时,在1.6位置书写文字,COLORFFFFFF
        月DIF赋值:"平滑异同平均线的DIF"(12,26,9)
        月DEA赋值:"平滑异同平均线的DEA"(12,26,9)
        当满足条件月DIF>月DEA时,在1.7位置画1号图标
        当满足条件月DIF<月DEA时,在1.7位置画2号图标
        当满足条件是否最后一个周期=1时,在1.7位置书写文字,COLORFFFFFF
        月RSI赋值:"RSI的RSI1"(9)
        当满足条件月RSI>50时,在1.8位置画1号图标
        当满足条件月RSI<50时,在1.8位置画2号图标
        当满足条件是否最后一个周期=1时,在1.8位置书写文字,COLORFFFFFF
        ABC1赋值:日K>日D
        ABC2赋值:日DIF>日DEA
        ABC3赋值:日RSI>50
        ABC4赋值:周K>周D
        ABC5赋值:周DIF>周DEA
        ABC6赋值:周RSI>50
        ABC7赋值:月K>月D
        ABC8赋值:月DIF>月DEA
        ABC9赋值:月RSI>50
        尊重市场赋值:ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 AND ABC7 AND ABC8 AND ABC9
        共振赋值:条件连续成立次数=1
        当满足条件共振时,在0.95和1.85位置之间画柱状线,宽度为2,0不为0则画空心柱.,画洋红色
        当满足条件共振时,在1.9位置画9号图标
        当满足条件共振时,在1.90位置书写文字,画红色
        '''
        df=self.df
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        weekly_data = df.resample('W').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        })
        weekly_data.dropna(inplace=True)
        monthly_data=df.resample('M').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        })
        amount=0
        DD11=0.95
        DD22=2
        日K = KDJ(CLOSE=df['close'],HIGH=df['high'],LOW=df['low'])[0].tolist()[-1] #"KDJ.K"(9,3,3)
        日D= KDJ(CLOSE=df['close'],HIGH=df['high'],LOW=df['low'])[1].tolist()[-1]#"KDJ.D"(9,3,3);
        ''''
        DRAWICON(日K>日D,1,1);
        DRAWICON(日K<日D,1,2);
        '''
        #DRAWTEXT(ISLASTBAR=1,1,'日K'),COLORFFFFFF;
        日DIF=MACD(CLOSE=df['close'])[0].tolist()[-1] #"MACD.DIF"(12,26,9);
        日DEA=MACD(CLOSE=df['close'])[1].tolist()[-1] #"MACD.DEA"(12,26,9);
        '''
        DRAWICON(日DIF>日DEA,1.1,1);
        DRAWICON(日DIF<日DEA,1.1,2);
        DRAWTEXT(ISLASTBAR=1,1.1,'日M'),COLORFFFFFF;
        '''
        日RSI = RSI(CLOSE=df['close'],N1=9)[0].tolist()[-1]#"RSI.RSI1"(9)
        '''
        DRAWICON(日RSI>50,1.2,1);
        DRAWICON(日RSI<50,1.2,2);
        DRAWTEXT(ISLASTBAR=1,1.2,'日R'),COLORFFFFFF;
        '''
        周K = KDJ(CLOSE=weekly_data['close'],HIGH=weekly_data['high'],LOW=weekly_data['low'])[0].tolist()[-1]#"KDJ.K"(9,3,3);
        周D= KDJ(CLOSE=weekly_data['close'],HIGH=weekly_data['high'],LOW=weekly_data['low'])[1].tolist()[-1]#"KDJ.D"(9,3,3);
        '''
        DRAWICON(周K>周D,1.3,1);
        DRAWICON(周K<周D,1.3,2);
        DRAWTEXT(ISLASTBAR=1,1.3,'周K'),COLORFFFFFF;
        '''
        周DIF=MACD(CLOSE=weekly_data['close'])[0].tolist()[-1] #"MACD.DIF"(12,26,9);
        周DEA=MACD(CLOSE=weekly_data['close'])[1].tolist()[-1]#"MACD.DEA"(12,26,9);
        '''
        DRAWICON(周DIF>周DEA,1.4,1);
        DRAWICON(周DIF<周DEA,1.4,2);
        DRAWTEXT(ISLASTBAR=1,1.4,'周M'),COLORFFFFFF;
        '''
        
        周RSI=RSI(CLOSE=weekly_data['close'])[0].tolist()[-1]#"RSI.RSI1"(9);
        '''
        DRAWICON(周RSI>50,1.5,1);
        DRAWICON(周RSI<50,1.5,2);
        DRAWTEXT(ISLASTBAR=1,1.5,'周R'),COLORFFFFFF;
        '''

        月K=KDJ(CLOSE=monthly_data['close'],HIGH=monthly_data['high'],LOW=monthly_data['low'])[0].tolist()[-1]#"KDJ.K"(9,3,3);
        月D= KDJ(CLOSE=monthly_data['close'],HIGH=monthly_data['high'],LOW=monthly_data['low'])[1].tolist()[-1]# "KDJ.D"(9,3,3);
        '''
        DRAWICON(月K>月D,1.6,1);
        DRAWICON(月K<月D,1.6,2);
        DRAWTEXT(ISLASTBAR=1,1.6,'月K'),COLORFFFFFF;
        '''
        月DIF=MACD(CLOSE=monthly_data['close'])[0].tolist()[-1]#"MACD.DIF"(12,26,9);
        月DEA=MACD(CLOSE=monthly_data['close'])[1].tolist()[-1]#"MACD.DEA"(12,26,9);
        '''
        DRAWICON(月DIF>月DEA,1.7,1);
        DRAWICON(月DIF<月DEA,1.7,2);
        DRAWTEXT(ISLASTBAR=1,1.7,'月M'),COLORFFFFFF;
        '''
        月RSI=RSI(CLOSE=monthly_data['close'])[0].tolist()[-1] #"RSI.RSI1"(9);
        '''
        DRAWICON(月RSI>50,1.8,1);
        DRAWICON(月RSI<50,1.8,2);
        DRAWTEXT(ISLASTBAR=1,1.8,'月R'),COLORFFFFFF;
        '''
        ABC1=日K>日D
        amount+=IF(ABC1,1,0)
        ABC2=日DIF>日DEA
        amount+=IF(ABC2,1,0)
        ABC3=日RSI>50
        amount+=IF(ABC3,1,0)
        ABC4=周K>周D
        amount+=IF(ABC4,1,0)
        ABC5=周DIF>周DEA
        amount+=IF(ABC5,1,0)
        ABC6=周RSI>50
        amount+=IF(ABC6,1,0)
        ABC7=月K>月D
        amount+=IF(ABC7,1,0)
        ABC8=月DIF>月DEA
        amount+=IF(ABC8,1,0)
        ABC9=月RSI>50
        amount+=IF(ABC9,1,0)
        尊重市场=AND(AND(AND(AND(AND(AND(AND(AND(ABC1,ABC2),ABC3) ,ABC4),ABC5) ,ABC6),ABC7) ,ABC8) ,ABC9)
        '''
        STICKLINE(共振,0.95,1.85,2,0),COLORMAGENTA;
        DRAWICON(共振,1.9,9);
        DRAWTEXT(共振,1.90,'★共振'),COLORRED;
        '''
        return amount
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='159920')
    print(df)
    modes=nine_finger_resonance(df=df)
    result=modes.nine_finger_resonance()
    print(result)
# 参考7
from xg_tdx_func.xg_tdx_func import *
from qmt_trader.unification_data_qmt import unification_data_qmt
class run_straight_to_the_top:
    def __init__(self,df):
        '''
        同花顺逃顶王
        '''
        self.df=df
    def run_straight_to_the_top(self):
        '''
        同花顺逃顶王
        指标买卖口诀：红柱出现时买入并持股，绿柱出现时卖
        VAR2赋值:10日内最低价的最低值
        VAR3赋值:25日内最高价的最高值
        输出阶段卖出: 3.2,COLORC6C600
        3.5,COLOR0088FF
        输出清仓卖出: 3.5,COLORFF75FF
        动力线赋值: (收盘价-VAR2)/(VAR3-VAR2)*4的4日指数移动平均
        当满足条件动力线>1日前的动力线时,在动力线和1日前的动力线位置之间画柱状线,宽度为3,1不为0则画空心柱.,画红色
        当满足条件动力线<=1日前的动力线时,在动力线和1日前的动力线位置之间画柱状线,宽度为3,1不为0则画空心柱.,COLOR00FF00
        输出底部:0.2,COLOR70DB93
        输出关注:0.5,画黄色
        当满足条件动力线上穿关注的20日过滤时,在动力线+0.02位置画1号图标
        当满足条件清仓卖出上穿动力线的20日过滤时,在动力线+0.02位置画2号图标
        当满足条件动力线上穿底部的20日过滤时,在动力线+0.02位置画1号图标
        当满足条件阶段卖出上穿动力线的20日过滤时,在动力线+0.02位置画2号图标
        输出强弱分界线:1.75,POINTDOT,线宽为2,COLOR70DB93
        输出数值:动力线,COLORA8A8A8
        '''
        df=self.df
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
        VAR2=LLV(LOW,10)
        VAR3=HHV(HIGH,25)
        阶段卖出= 3.2#COLORC6C600;
        df['阶段卖出']=阶段卖出
        #3.5,COLOR0088FF;
        清仓卖出=3.5#,COLORFF75FF;
        df['清仓卖出']=清仓卖出
        动力线= EMA((CLOSE-VAR2)/(VAR3-VAR2)*4,4)
        df['动力线']=动力线
        #STICKLINE(动力线>REF(动力线,1) ,动力线 ,REF(动力线,1),3 ,1),COLORRED;
        #STICKLINE(动力线<=REF(动力线,1) ,动力线 ,REF(动力线,1),3 ,1),COLOR00FF00;
        df['柱子']=IF(动力线>REF(动力线,1),'红色','绿色')
        底部=0.2#,COLOR70DB93;
        df['底部']=底部
        关注=0.5#,COLORYELLOW;
        df['关注']=关注
        #DRAWICON( FILTER(CROSS(动力线,关注),20),动力线+0.02 ,1);
        #DRAWICON( FILTER(CROSS(清仓卖出,动力线),20),动力线+0.02,2);
        df['关注箭头']=IF(CROSS(动力线,关注),'红色','')
        #DRAWICON( FILTER(CROSS(动力线,底部),20),动力线+0.02 ,1);
        #DRAWICON( FILTER(CROSS(阶段卖出,动力线),20),动力线+0.02,2);
        df['底部箭头']=IF(CROSS(动力线,底部),'红色','')
        强弱分界线=1.75
        df['强弱分界线']=强弱分界线
        数值=动力线
        df['动力线']=数值
        df['MA_3']=MA(数值,3)
        return df
if __name__=='__main__':
    data=unification_data_qmt()
    df=data.get_hist_data_em(stock='159934')
    modes=run_straight_to_the_top(df=df)
    result=modes.run_straight_to_the_top()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考8
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class six_pulse_excalibur_hist:
    def __init__(self,df):
        '''
        六脉神剑
        '''
        self.df=df
    def six_pulse_excalibur_hist(self):
        '''
        六脉神剑
        DIFF赋值:收盘价的8日指数移动平均-收盘价的13日指数移动平均
        DEA赋值:DIFF的5日指数移动平均
        当满足条件DIFF>DEA时,在1位置画1号图标
        当满足条件DIFF<DEA时,在1位置画2号图标
        当满足条件是否最后一个周期=1时,在1位置书写文字,COLORFFFFFF
        ABC1赋值:DIFF>DEA
        尊重市场1赋值:(收盘价-8日内最低价的最低值)/(8日内最高价的最高值-8日内最低价的最低值)*100
        K赋值:尊重市场1的3日[1日权重]移动平均
        D赋值:K的3日[1日权重]移动平均
        当满足条件K>D时,在2位置画1号图标
        当满足条件K<D时,在2位置画2号图标
        当满足条件是否最后一个周期=1时,在2位置书写文字,COLORFFFFFF
        ABC2赋值:K>D
        指标营地赋值:1日前的收盘价
        RSI1赋值:(收盘价-指标营地和0的较大值的5日[1日权重]移动平均)/(收盘价-指标营地的绝对值的5日[1日权重]移动平均)*100
        RSI2赋值:(收盘价-指标营地和0的较大值的13日[1日权重]移动平均)/(收盘价-指标营地的绝对值的13日[1日权重]移动平均)*100
        当满足条件RSI1>RSI2时,在3位置画1号图标
        当满足条件RSI1<RSI2时,在3位置画2号图标
        当满足条件是否最后一个周期=1时,在3位置书写文字,COLORFFFFFF
        ABC3赋值:RSI1>RSI2
        尊重市场赋值:-(13日内最高价的最高值-收盘价)/(13日内最高价的最高值-13日内最低价的最低值)*100
        LWR1赋值:尊重市场的3日[1日权重]移动平均
        LWR2赋值:LWR1的3日[1日权重]移动平均
        当满足条件LWR1>LWR2时,在4位置画1号图标
        当满足条件LWR1<LWR2时,在4位置画2号图标
        当满足条件是否最后一个周期=1时,在4位置书写文字,COLORFFFFFF
        ABC4赋值:LWR1>LWR2
        BBI赋值:(收盘价的3日简单移动平均+收盘价的5日简单移动平均+收盘价的8日简单移动平均+收盘价的13日简单移动平均)/4
        当满足条件收盘价>BBI时,在5位置画1号图标
        当满足条件收盘价<BBI时,在5位置画2号图标
        当满足条件是否最后一个周期=1时,在5位置书写文字,COLORFFFFFF
        ABC10赋值:7
        ABC5赋值:收盘价>BBI
        MTM赋值:收盘价-1日前的收盘价
        MMS赋值:100*MTM的5日指数移动平均的3日指数移动平均/MTM的绝对值的5日指数移动平均的3日指数移动平均
        MMM赋值:100*MTM的13日指数移动平均的8日指数移动平均/MTM的绝对值的13日指数移动平均的8日指数移动平均
        当满足条件MMS>MMM时,在6位置画1号图标
        当满足条件MMS<MMM时,在6位置画2号图标
        当满足条件是否最后一个周期=1时,在6位置书写文字,COLORFFFFFF
        ABC6赋值:MMS>MMM
        输出买入:如果ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6=1ANDREF(ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6,1)=0,返回6,否则返回0,画黄色,线宽为2
        输出持有:如果ABC1ANDABC2ANDABC3ANDABC4ANDABC5ANDABC6,返回6,否则返回0,画洋红色,线宽为2
        共振赋值:ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 
        当满足条件共振时,在0和6位置之间画柱状线,宽度为0.6,1不为0则画空心柱.,画洋红色
        当满足条件买入时,在0和6位置之间画柱状线,宽度为0.6,0不为0则画空心柱.,画黄色
        当满足条件DIFF>DEA时,在1位置画1号图标
        当满足条件DIFF<DEA时,在1位置画2号图标
        当满足条件K>D时,在2位置画1号图标
        当满足条件K<D时,在2位置画2号图标
        当满足条件RSI1>RSI2时,在3位置画1号图标
        当满足条件RSI1<RSI2时,在3位置画2号图标
        当满足条件LWR1>LWR2时,在4位置画1号图标
        当满足条件LWR1<LWR2时,在4位置画2号图标
        当满足条件收盘价>BBI时,在5位置画1号图标
        当满足条件收盘价<BBI时,在5位置画2号图标
        当满足条件MMS>MMM时,在6位置画1号图标
        当满足条件MMS<MMM时,在6位置画2号图标
        当满足条件买入时,在6.6位置画9号图标
        '''
        df=self.df
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
        '''
        买入:IF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6=1  
        AND REF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6,1)=0,6,0),COLORYELLOW,LINETHICK2;
        持有:IF(ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6,6,0),COLORMAGENTA,LINETHICK2;
        共振:=ABC1 AND ABC2 AND ABC3 AND ABC4 AND ABC5 AND ABC6 ;
        STICKLINE(共振,0,6,0.6,1),COLORMAGENTA;
        STICKLINE(买入,0,6,0.6,0),COLORYELLOW;
        DRAWICON(DIFF>DEA,1,1);
        DRAWICON(DIFF<DEA,1,2);
        DRAWICON(K>D,2,1);
        DRAWICON(K<D,2,2);
        DRAWICON(RSI1>RSI2,3,1);
        DRAWICON(RSI1<RSI2,3,2);
        DRAWICON(LWR1>LWR2,4,1);
        DRAWICON(LWR1<LWR2,4,2);
        DRAWICON(CLOSE>BBI,5,1);
        DRAWICON(CLOSE<BBI,5,2);
        DRAWICON(MMS>MMM,6,1);{微信公众号:尊重市场}
        DRAWICON(MMS<MMM,6,2);
        DRAWICON(买入,6.6,9);
        '''
        df['signal']=signal
        df['markers']=markers
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='513100')
    modes=six_pulse_excalibur_hist(df=df)
    result=modes.six_pulse_excalibur_hist()
    print(result)
# 参考9
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class small_fruit_band_analysis:
    def __init__(self,df) :
        '''
        小果波段分析
        '''
        self.df=df
    def small_fruit_band_analysis(self):
        '''
        {作者:小果}
        {微信：15117320079}
        {公众号:数据分析与运用}
        A1赋值:((开盘价+最高价+最低价+收盘价)/4的3日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的6日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的9日指数移动平均)/3
        A2赋值:((开盘价+最高价+最低价+收盘价)/4的5日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的10日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的20日指数移动平均)/3
        A3赋值:((开盘价+最高价+最低价+收盘价)/4的7日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的14日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的28日指数移动平均)/3
        A4赋值:((开盘价+最高价+最低价+收盘价)/4的9日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的18日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的36日指数移动平均)/3
        A5赋值:((开盘价+最高价+最低价+收盘价)/4的11日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的22日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的44日指数移动平均)/3
        A6赋值:((开盘价+最高价+最低价+收盘价)/4的13日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的26日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的52日指数移动平均)/3
        A7赋值:((开盘价+最高价+最低价+收盘价)/4的21日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的34日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的68日指数移动平均)/3
        VAR1赋值:A1的6日线性回归预测值
        VAR2赋值:A2的6日线性回归预测值
        VAR3赋值:A3的6日线性回归预测值
        VAR4赋值:A4的6日线性回归预测值
        VAR5赋值:A5的6日线性回归预测值
        VAR6赋值:A6的6日线性回归预测值
        VAR7赋值:A7的6日线性回归预测值
        如果VAR1>1日前的VAR1,返回VAR1,否则返回无效数,POINTDOT,COLORFF00FF
        如果VAR1<1日前的VAR1,返回VAR1,否则返回无效数,POINTDOT,COLOR00FF00
        如果VAR2>1日前的VAR2,返回VAR2,否则返回无效数,POINTDOT,COLORFF00FF
        如果VAR2<1日前的VAR2,返回VAR2,否则返回无效数,POINTDOT,COLOR00FF00
        如果VAR3>1日前的VAR3,返回VAR3,否则返回无效数,POINTDOT,COLORFF00FF
        如果VAR3<1日前的VAR3,返回VAR3,否则返回无效数,POINTDOT,COLOR00FF00
        如果VAR4>1日前的VAR4,返回VAR4,否则返回无效数,POINTDOT,COLORFF00FF
        如果VAR4<1日前的VAR4,返回VAR4,否则返回无效数,POINTDOT,COLOR00FF00
        如果VAR5>1日前的VAR5,返回VAR5,否则返回无效数,POINTDOT,COLORFF00FF
        如果VAR5<1日前的VAR5,返回VAR5,否则返回无效数,POINTDOT,COLOR00FF00
        如果VAR6>1日前的VAR6,返回VAR6,否则返回无效数,POINTDOT,COLORFF00FF
        如果VAR6<1日前的VAR6,返回VAR6,否则返回无效数,POINTDOT,COLOR00FF00
        如果VAR7>1日前的VAR7,返回VAR7,否则返回无效数,线宽为2,COLORFF00FF
        如果VAR7<1日前的VAR7,返回VAR7,否则返回无效数,线宽为2,COLOR00FF00
        TOWERC赋值:(3*收盘价+2*开盘价+最高价+最低价)/7的3日指数移动平均的6日线性回归预测值
        DIRECTIONMAX赋值:1日前的TOWERC和1日前的TOWERC的较大值
        DIRECTIONMIN赋值:1日前的TOWERC和1日前的TOWERC的较小值
        当满足条件TOWERC>=1日前的TOWERC时,在TOWERC和DIRECTIONMAX位置之间画柱状线,宽度为4,0不为0则画空心柱.,COLOR0000FF
        当满足条件TOWERC<1日前的TOWERC时,在TOWERC和DIRECTIONMIN位置之间画柱状线,宽度为4,0不为0则画空心柱.,COLOR00FF00
        当满足条件TOWERC>=1日前的TOWERCANDREF(TOWERC,1)<2日前的TOWERC时,在TOWERC位置书写文字,画红色
        当满足条件TOWERC<1日前的TOWERCANDREF(TOWERC,1)>2日前的TOWERC时,在TOWERC位置书写文字,画绿色
        '''
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        VOL=df['volume']
        V=df['volume']
        A1=(EMA((OPEN+HIGH+LOW+CLOSE)/4,3)+EMA((OPEN+HIGH+LOW+CLOSE)/4,6)+EMA((OPEN+HIGH+LOW+CLOSE)/4,9))/3
        A2=(EMA((OPEN+HIGH+LOW+CLOSE)/4,5)+EMA((OPEN+HIGH+LOW+CLOSE)/4,10)+EMA((OPEN+HIGH+LOW+CLOSE)/4,20))/3
        A3=(EMA((OPEN+HIGH+LOW+CLOSE)/4,7)+EMA((OPEN+HIGH+LOW+CLOSE)/4,14)+EMA((OPEN+HIGH+LOW+CLOSE)/4,28))/3
        A4=(EMA((OPEN+HIGH+LOW+CLOSE)/4,9)+EMA((OPEN+HIGH+LOW+CLOSE)/4,18)+EMA((OPEN+HIGH+LOW+CLOSE)/4,36))/3
        A5=(EMA((OPEN+HIGH+LOW+CLOSE)/4,11)+EMA((OPEN+HIGH+LOW+CLOSE)/4,22)+EMA((OPEN+HIGH+LOW+CLOSE)/4,44))/3
        A6=(EMA((OPEN+HIGH+LOW+CLOSE)/4,13)+EMA((OPEN+HIGH+LOW+CLOSE)/4,26)+EMA((OPEN+HIGH+LOW+CLOSE)/4,52))/3
        A7=(EMA((OPEN+HIGH+LOW+CLOSE)/4,21)+EMA((OPEN+HIGH+LOW+CLOSE)/4,34)+EMA((OPEN+HIGH+LOW+CLOSE)/4,68))/3
        VAR1=FORCAST(A1,6)
        VAR2=FORCAST(A2,6)
        VAR3=FORCAST(A3,6)
        VAR4=FORCAST(A4,6)
        VAR5=FORCAST(A5,6)
        VAR6=FORCAST(A6,6)
        VAR7=FORCAST(A7,6)
        '''
        IF(VAR1>REF(VAR1,1),VAR1,DRAWNULL),POINTDOT,COLORFF00FF;
        IF(VAR1<REF(VAR1,1),VAR1,DRAWNULL),POINTDOT,COLOR00FF00;
        IF(VAR2>REF(VAR2,1),VAR2,DRAWNULL),POINTDOT,COLORFF00FF;
        IF(VAR2<REF(VAR2,1),VAR2,DRAWNULL),POINTDOT,COLOR00FF00;
        IF(VAR3>REF(VAR3,1),VAR3,DRAWNULL),POINTDOT,COLORFF00FF;
        IF(VAR3<REF(VAR3,1),VAR3,DRAWNULL),POINTDOT,COLOR00FF00;
        IF(VAR4>REF(VAR4,1),VAR4,DRAWNULL),POINTDOT,COLORFF00FF;
        IF(VAR4<REF(VAR4,1),VAR4,DRAWNULL),POINTDOT,COLOR00FF00;
        IF(VAR5>REF(VAR5,1),VAR5,DRAWNULL),POINTDOT,COLORFF00FF;
        IF(VAR5<REF(VAR5,1),VAR5,DRAWNULL),POINTDOT,COLOR00FF00;
        IF(VAR6>REF(VAR6,1),VAR6,DRAWNULL),POINTDOT,COLORFF00FF;
        IF(VAR6<REF(VAR6,1),VAR6,DRAWNULL),POINTDOT,COLOR00FF00;
        '''
        #IF(VAR7>REF(VAR7,1),VAR7,DRAWNULL),LINETHICK2,COLORFF00FF;
        #IF(VAR7<REF(VAR7,1),VAR7,DRAWNULL),LINETHICK2,COLOR00FF00;
        df['趋势线']=IF(VAR7>REF(VAR7,1),'紫色','绿色')
        TOWERC=FORCAST(EMA((3*CLOSE+2*OPEN+HIGH+LOW)/7,3),6)
        DIRECTIONMAX=MAX(REF(TOWERC,1),REF(TOWERC,1))
        DIRECTIONMIN=MIN(REF(TOWERC,1),REF(TOWERC,1))
        #STICKLINE(TOWERC>=REF(TOWERC,1),TOWERC,DIRECTIONMAX,4,0),COLOR0000FF;
        #STICKLINE(TOWERC<REF(TOWERC,1),TOWERC,DIRECTIONMIN,4,0),COLOR00FF00;
        df['方块']=IF(TOWERC>=REF(TOWERC,1),'红色','绿色')
        #DRAWTEXT(TOWERC >= REF(TOWERC,1)  AND  REF(TOWERC,1) < REF(TOWERC,2) ,TOWERC,'买'),COLORRED;
        df['买']=IF(AND(TOWERC >= REF(TOWERC,1), REF(TOWERC,1) < REF(TOWERC,2)),"买",None)
        #DRAWTEXT(TOWERC < REF(TOWERC,1)  AND  REF(TOWERC,1) > REF(TOWERC,2) ,TOWERC,'卖'),COLORGREEN
        df['卖']=IF(AND(TOWERC < REF(TOWERC,1),REF(TOWERC,1) > REF(TOWERC,2)),'卖',None)
        stats_list=[]
        for buy,sell in zip(df['买'].tolist(),df['卖'].tolist()):
            if buy=='买':
                stats_list.append(buy)
            elif sell=='卖':
                stats_list.append(sell)
            else:
                stats_list.append(None)
        df['stats']=stats_list
        df['stats']=df['stats'].fillna(method='ffill')
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='511090')
    print(df)
    modes=small_fruit_band_analysis(df=df)
    result=modes.small_fruit_band_analysis()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考10
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class small_fruit_band_gold_mining:
    def __init__(self,df):
        '''
        小果波段掘金
        '''
        self.df=df
    def small_fruit_band_gold_mining(self):
        '''
        输出MA3:收盘价的3日简单移动平均
        输出MA5:收盘价的5日简单移动平均,画黄色
        输出MA10:收盘价的10日简单移动平均
        输出MA15:收盘价的15日简单移动平均,画白色
        输出MA20:收盘价的20日简单移动平均,画绿色,POINTDOT
        输出MA30:收盘价的30日简单移动平均,画红色,POINTDOT
        A1赋值:如果收盘价>=MA3,返回1,否则返回-1
        A2赋值:如果收盘价>=MA5,返回1,否则返回-1
        A3赋值:如果收盘价>=MA10,返回1,否则返回-1
        A4赋值:如果MA3>=1日前的MA3,返回1,否则返回-1
        A5赋值:如果MA5>=1日前的MA5,返回1,否则返回-1
        A6赋值:如果MA10>=1日前的MA10,返回1,否则返回-1
        QUSHIX赋值:(A1+A2+A3+A4+A5+A6)/6*100,画青色,线宽为3
        X1赋值:(收盘价+最低价+最高价)/3
        X2赋值:X1的3日指数移动平均
        X3赋值:X2的5日指数移动平均
        当满足条件X2上穿X3时,在最低价*0.98位置书写文字
        当满足条件X3上穿X2时,在最高价*1.02位置书写文字
        当满足条件X2>=X3时,在最低价和最高价位置之间画柱状线,宽度为0,0不为0则画空心柱.,画红色
        当满足条件X2<X3时,在最低价和最高价位置之间画柱状线,宽度为0,0不为0则画空心柱.,画绿色
        当满足条件X2上穿X3时,在开盘价和收盘价位置之间画柱状线,宽度为3,0不为0则画空心柱.,画黄色
        当满足条件X3上穿X2时,在开盘价和收盘价位置之间画柱状线,宽度为3,0不为0则画空心柱.,画蓝色
        当满足条件QUSHIX>=100ANDMA3>1日前的MA3AND(收盘价-开盘价)/开盘价*100>5ANDCLOSE>MA3时,在最低价*0.99位置书写文字,画洋红色
        '''
        df=self.df
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
        MA3=MA(C,3)
        MA5=MA(C,5)
        MA10=MA(C,10)
        MA15=MA(C,15)
        MA20=MA(C,20)
        MA30=MA(C,30)
        A1=IF(C>=MA3,1,-1)
        A2=IF(C>=MA5,1,-1)
        A3=IF(C>=MA10,1,-1)
        A4=IF(MA3>=REF(MA3,1),1,-1)
        A5=IF(MA5>=REF(MA5,1),1,-1)
        A6=IF(MA10>=REF(MA10,1),1,-1)
        QUSHIX=(A1+A2+A3+A4+A5+A6)/6*100
        X1=(C+L+H)/3
        X2=EMA(X1,3)
        X3=EMA(X2,5)
        #DRAWTEXT(CROSS(X2,X3),L*0.98,'B');
        df['B']=CROSS(X2,X3)
        #DRAWTEXT(CROSS(X3,X2),H*1.02,'S');
        df['S']=CROSS(X3,X2)
        #STICKLINE(X2>=X3,LOW,HIGH,0,0),COLORRED;
        #STICKLINE(X2>=X3,CLOSE,OPEN,3,1),COLORRED;
        df['红色']=X2>=X3
        #STICKLINE(X2<X3,LOW,HIGH,0,0),COLORGREEN;
        #STICKLINE(X2<X3,CLOSE,OPEN,3,1),COLORGREEN;
        df['绿色']=X2<X3
        #STICKLINE(CROSS(X2,X3),OPEN,CLOSE,3,0),COLORYELLOW;
        df['黄色']=CROSS(X2,X3)
        #STICKLINE(CROSS(X3,X2),OPEN,CLOSE,3,0),COLORBLUE;
        df['蓝色']=CROSS(X3,X2)
        #DRAWTEXT(QUSHIX>=100 AND MA3>REF(MA3,1) AND (CLOSE-OPEN)/OPEN*100>5 AND CLOSE>MA3,L*0.99,'★'),COLORMAGENTA
        df['星']=AND(AND(AND(QUSHIX>=100,MA3>REF(MA3,1)),(CLOSE-OPEN)/OPEN*100>5),CLOSE>MA3)
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='513100')
    modes=small_fruit_band_gold_mining(df=df)
    result=modes.small_fruit_band_gold_mining()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考11
from xg_tdx_func.xg_tdx_func import *
class small_fruit_band_trading_hist_trader:
    '''
    小果波段交易高频T0
    '''
    def __init__(self,df):
        '''
        小果波段交易高频T0
        '''
        self.df=df
    def small_fruit_band_trading_hist_trader(self):
        '''
        N1赋值:5
        N2赋值:5
        N3赋值:3
        MA_1赋值:3
        MA_2赋值:5
        BUY_AMOUNT_N赋值:2
        SELL_AMOUNT_N赋值:3
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
        输出MA1:UP的MA_1日简单移动平均
        输出均线:UP的MA_2日简单移动平均
        BUY_AMOUNT赋值:条件连续成立次数
        SELL_AMOUNT赋值:条件连续成立次数
        当满足条件UP>1日前的UPANDREF(UP,1)<2日前的UPANDSELL_AMOUNT>=SELL_AMOUNT_N时,在UP位置书写文字,画红色
        当满足条件UP<1日前的UPANDREF(UP,1)>2日前的UPANDBUY_AMOUNT>=BUY_AMOUNT_N时,在UP位置书写文字 ,画绿色

        '''
        df=self.df
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
        N1=5
        N2=9
        N3=7
        MA_1=3
        MA_2=5
        BUY_AMOUNT_N=0
        SELL_AMOUNT_N=0
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
        MA1=MA(UP,MA_1)
        MA2=MA(UP,MA_2)
        df['MA1']=MA1
        df['MA2']=MA2
        BUY_AMOUNT=BARSLASTCOUNT( REF(UP,1) > REF(UP,2))
        SELL_AMOUNT=BARSLASTCOUNT( REF(UP,1) < REF(UP,2))
        #DRAWTEXT(UP > REF(UP,1) AND  REF(UP,1) < REF(UP,2) AND SELL_AMOUNT>=SELL_AMOUNT_N,UP,'买'),COLORRED;
        #DRAWTEXT(UP < REF(UP,1)  AND  REF(UP,1) > REF(UP,2)  AND BUY_AMOUNT>=BUY_AMOUNT_N,UP,'卖') ,COLORGREEN;
        df['柱子']=IF(UP > REF(UP,1),'红色','蓝色')
        df['买']=IF(AND(AND(UP > REF(UP,1),REF(UP,1) < REF(UP,2)),SELL_AMOUNT>=SELL_AMOUNT_N),'买',None)
        df['卖']=IF(AND(AND(UP < REF(UP,1),REF(UP,1) > REF(UP,2)),BUY_AMOUNT>=BUY_AMOUNT_N),'卖',None)
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
if __name__=='__main__':
    from trader_tool.unification_data import unification_data
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='511130',data_type='5')
    modes=small_fruit_band_trading_hist_trader(df=df)
    result=modes.small_fruit_band_trading_hist_trader()
    print(result)
    result.to_excel(r'数据.xlsx')

# 参考12
from xg_tdx_func.xg_tdx_func import *
class small_fruit_band_trading_index:
    '''
    小果波段交易指数
    '''
    def __init__(self,df):
        '''
        小果波段交易指数
        '''
        self.df=df
    def small_fruit_band_trading_index(self):
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
        df=self.df
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
if __name__=='__main__':
    from trader_tool.unification_data import unification_data
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='513100')
    modes=small_fruit_band_trading(df=df)
    result=modes.small_fruit_band_trading()
    print(result)
    result.to_excel(r'数据.xlsx')

# 参考13
from xg_tdx_func.xg_tdx_func import *
class small_fruit_band_trading:
    '''
    小果波段交易
    '''
    def __init__(self,df):
        '''
        小果波段交易
        '''
        self.df=df
    def small_fruit_band_trading(self):
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
        df=self.df
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
if __name__=='__main__':
    from trader_tool.unification_data import unification_data
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='513100')
    modes=small_fruit_band_trading(df=df)
    result=modes.small_fruit_band_trading()
    print(result)
    result.to_excel(r'数据.xlsx')

# 参考13
from xg_tdx_func.xg_tdx_func import *
class small_fruit_high_frequency_measurement_line:
    '''
    小果高频量线
    '''
    def __init__(self,df):
        '''
        小果高频量线
        '''
        self.df=df
    def small_fruit_high_frequency_measurement_line(self):
        '''
        超准赋值:收盘价的20日指数移动平均
        输出股:如果收盘价的1日简单移动平均>=超准,返回超准,否则返回无效数,画红色,线宽为4
        输出币:如果收盘价的2日简单移动平均<超准,返回超准,否则返回无效数,画绿色,线宽为2
        输出均:收盘价*成交量(手)的240日累和/成交量(手)的240日累和,画黄色,DOTLINE,线宽为1

        '''
        df=self.df
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
        超准=EMA(C,20)
        df['超准']=超准
        股=IF(MA(C,1)>=超准,超准,0)
        df['股']=股
        币=IF(MA(C,2)<超准,超准,0)
        df['币']=币
        均=SUM(C*V,240)/SUM(V,240)
        df['均']=均
       
        df['买']=IF(AND(REF(股,1)==0,股>0),'买',None)
        df['卖']=IF(AND(REF(股,1)>0,股==0),'卖',None)
        stats_list=[]
        for buy,sell in zip(df['买'].tolist(),df['卖'].tolist()):
            if buy=='买':
                stats_list.append('买')
            elif sell=='卖':
                stats_list.append('卖')
            else:
                stats_list.append(None)
        df['stats']=stats_list
        
        df['连续交易']=df['stats'].fillna(method='ffill')
        return df
if __name__=='__main__':
    from trader_tool.unification_data import unification_data
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='511090',data_type='1')
    modes=small_fruit_high_frequency_measurement_line(df=df)
    result=modes.small_fruit_high_frequency_measurement_line()
    print(result)
    result.to_excel(r'数据.xlsx')

# 参考14
from xg_tdx_func.xg_tdx_func import *
import pandas as pd
class take_advantage_of_the_trend:
    def __init__(self,df) :
        self.df=df
    def take_advantage_of_the_trend(self):
        '''
        【顺势黑马】套装指标简介：
        这是一个依托EXPMA基础上添加五线通道，并实时显示五线通道的价格，来判断K线所在位置的参考。
        1、“黄金金叉“显示阳线为黄，红色做多线持有；
        2、“死叉阴线”为蓝；绿线做空线休息；
        3、出信号放量突破时，均线多头排列可取，空排不取。
        ABC7:=EMA(C,7),COLORYELLOW,LINETHICK2;
        ABC14:=EMA(C,14),COLOR7FF00F,LINETHICK1 DOTLINE;
        ABC25:=EMA(C,25),COLORFF7F00,LINETHICK1 DOTLINE;
        ABCMA45:=EMA(C,45),COLORF00FFF,LINETHICK1 DOTLINE;
        MA5:=MA(C,5);{微信公众号:尊重市场}
        MA10:=MA(C,10);
        MA20:=MA(C,20);
        ABC:=ABC7>ABC14;
        STICKLINE(C/REF(C,1)>1.095,C,O,2,0),COLORYELLOW;
        DRAWTEXT(C/REF(C,1)>1.095,L*0.96,' ★强'),COLORLIRED;
        STICKLINE(HIGH<REF(LOW,0),HIGH,REF(LOW,0),10,0);
        STICKLINE(LOW>REF(HIGH,0) ,LOW,REF(HIGH,0),10,0);
        STICKLINE(C=O,H,L,0,0);
        STICKLINE((C=O)AND(C>REF(C,0)),C,O,8,0);
        STICKLINE((C=O)AND(C<REF(C,0)),C,O,8,0);
        STICKLINE(CROSS(ABC7,ABC14) AND ABC,CLOSE,OPEN,2,0),COLORMAGENTA;
        DRAWICON(CROSS(ABC7,ABC14) AND ABC,L*1.002,9);
        DRAWTEXT(CROSS(ABC7,ABC14) AND{微信公众号:尊重市场}ABC,L*0.98,' ★买'),COLORMAGENTA;
        STICKLINE(CROSS(ABC25,ABC7),CLOSE,OPEN,2,0),COLORBLUE;
        CC:=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,20))/MA(CLOSE,20);
        DD:=DMA(CLOSE,CC);
        上轨:(1+7/100)*DD,DOTLINE,COLORGREEN;
        下轨:(1-7/100)*DD,DOTLINE,COLORGREEN;
        中轨:(上轨+下轨)/2,DOTLINE,COLORGREEN;
        FK:(1+14/100)*DD,DOTLINE,COLORGRAY;
        CD:(1-14/100)*DD,DOTLINE,COLORGRAY;
        DRAWNUMBER(ISLASTBAR,上轨,上轨),COLOR00FFFF;
        DRAWNUMBER(ISLASTBAR,下轨,下轨),COLORFFFF00;
        DRAWNUMBER(ISLASTBAR,中轨,中轨),COLOR00FF00;
        DRAWNUMBER(ISLASTBAR,FK,FK){微信公众号:尊重市场},COLOR0000FF;
        DRAWNUMBER(ISLASTBAR,CD,CD),COLORWHITE;
        上轨绿:IF(上轨>=REF(上轨,1),上轨,DRAWNULL),DOTLINE,COLORGREEN,LINETHICK1;
        上轨红:IF(上轨>=REF(上轨,1),上轨,DRAWNULL),DOTLINE COLORRED,LINETHICK1;
        中轨绿:IF(中轨>=REF(中轨,1), 中轨,DRAWNULL),DOTLINE,COLORGREEN,LINETHICK1;
        中轨红:IF(中轨>=REF(中轨,1), 中轨,DRAWNULL),DOTLINE COLORRED, LINETHICK1;
        下轨绿:IF(下轨>=REF(下轨,1), 下轨,DRAWNULL),DOTLINE,COLORGREEN,LINETHICK1;
        下轨红:IF(下轨>=REF(下轨,1), 下轨,DRAWNULL),DOTLINE COLORRED,LINETHICK1;
        IF(ABC7>REF(ABC7,1),ABC7,DRAWNULL),COLORRED,LINETHICK2;
        IF(ABC7<REF(ABC7,1),ABC7,DRAWNULL),COLORGREEN,LINETHICK2;
        翻译

        '''
        df=self.df
        data=pd.DataFrame()
        data['date']=df['date']
        C=df['close']
        #ABC7赋值:收盘价的7日指数移动平均,画黄色,线宽为2
        ABC7=EMA(C,7)#,COLORYELLOW,LINETHICK2;
        #ABC14赋值:收盘价的14日指数移动平均,COLOR7FF00F,线宽为1 DOTLINE
        ABC14=EMA(C,14)#COLOR7FF00F,LINETHICK1 DOTLINE;
        #ABC25赋值:收盘价的25日指数移动平均,COLORFF7F00,线宽为1 DOTLINE
        ABC25=EMA(C,25)#,COLORFF7F00,LINETHICK1 DOTLINE;
        #ABCMA45赋值:收盘价的45日指数移动平均,COLORF00FFF,线宽为1 DOTLINE
        ABCMA45=EMA(C,45)#,COLORF00FFF,LINETHICK1 DOTLINE;
        MA5=MA(C,5)
        MA10=MA(C,10)
        MA20=MA(C,20)
        ABC=ABC7>ABC14
        #当满足条件收盘价/1日前的收盘价>1.095时,在收盘价和开盘价位置之间画柱状线,宽度为2,0不为0则画空心柱.,画黄色
        #STICKLINE(C/REF(C,1)>1.095,C,O,2,0),COLORYELLOW;
        #当满足条件收盘价/1日前的收盘价>1.095时,在最低价*0.96位置书写文字,画淡红色
        data['强']=C/REF(C,1)>1.09
        #DRAWTEXT(C/REF(C,1)>1.095,L*0.96,' ★强'),COLORLIRED;

        #当满足条件最高价<0日前的最低价时,在最高价和0日前的最低价位置之间画柱状线,宽度为10,0不为0则画空心柱.
        #STICKLINE(HIGH<REF(LOW,0),HIGH,REF(LOW,0),10,0);
        #STICKLINE(LOW>REF(HIGH,0) ,LOW,REF(HIGH,0),10,0);
        ''''
        STICKLINE(C=O,H,L,0,0);
        STICKLINE((C=O)AND(C>REF(C,0)),C,O,8,0);
        STICKLINE((C=O)AND(C<REF(C,0)),C,O,8,0);
        STICKLINE(CROSS(ABC7,ABC14) AND ABC,CLOSE,OPEN,2,0),COLORMAGENTA;
        DRAWICON(CROSS(ABC7,ABC14) AND ABC,L*1.002,9);
        '''
        data['买']=CROSS(ABC7,ABC14)
        #DRAWTEXT(CROSS(ABC7,ABC14) AND{微信公众号:尊重市场}ABC,L*0.98,' ★买'),COLORMAGENTA;
        '''
        STICKLINE(CROSS(ABC25,ABC7),CLOSE,OPEN,2,0),COLORBLUE;
        CC:=ABS((2*CLOSE+HIGH+LOW)/4-MA(CLOSE,20))/MA(CLOSE,20);
        DD:=DMA(CLOSE,CC);
        上轨:(1+7/100)*DD,DOTLINE,COLORGREEN;
        下轨:(1-7/100)*DD,DOTLINE,COLORGREEN;
        中轨:(上轨+下轨)/2,DOTLINE,COLORGREEN;
        FK:(1+14/100)*DD,DOTLINE,COLORGRAY;
        CD:(1-14/100)*DD,DOTLINE,COLORGRAY;
        DRAWNUMBER(ISLASTBAR,上轨,上轨),COLOR00FFFF;
        DRAWNUMBER(ISLASTBAR,下轨,下轨),COLORFFFF00;
        DRAWNUMBER(ISLASTBAR,中轨,中轨),COLOR00FF00;
        DRAWNUMBER(ISLASTBAR,FK,FK){微信公众号:尊重市场},COLOR0000FF;
        DRAWNUMBER(ISLASTBAR,CD,CD),COLORWHITE;
        上轨绿:IF(上轨>=REF(上轨,1),上轨,DRAWNULL),DOTLINE,COLORGREEN,LINETHICK1;
        上轨红:IF(上轨>=REF(上轨,1),上轨,DRAWNULL),DOTLINE COLORRED,LINETHICK1;
        中轨绿:IF(中轨>=REF(中轨,1), 中轨,DRAWNULL),DOTLINE,COLORGREEN,LINETHICK1;
        中轨红:IF(中轨>=REF(中轨,1), 中轨,DRAWNULL),DOTLINE COLORRED, LINETHICK1;
        下轨绿:IF(下轨>=REF(下轨,1), 下轨,DRAWNULL),DOTLINE,COLORGREEN,LINETHICK1;
        下轨红:IF(下轨>=REF(下轨,1), 下轨,DRAWNULL),DOTLINE COLORRED,LINETHICK1;
        '''
        data['红色']=IF(ABC7>REF(ABC7,1),ABC7,None)
        data['绿色']=IF(ABC7<REF(ABC7,1),ABC7,None)
        data['buy']= data['买']
        data['hold']=data['红色']
        data['sell']=data['绿色']
        data['hold']= data['hold'].apply(lambda x : True if x!=None else False)
        data['sell']= data['sell'].apply(lambda x : True if x!=None else False)
        return data
# 参考15
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class the_kirin_trend_line:
    def __init__(self,df) :
        '''
        麒麟趋势线
        '''
        self.df=df
    def the_kirin_trend_line(self):
        '''
        输出SWL:(收盘价的10日指数移动平均*7+收盘价的20日指数移动平均*3)/10
        输出SWS:以1和100*(成交量(手)的5日累和/(3*当前流通股本(手)))的较大值为权重收盘价的20日指数移动平均的动态移动平均,画白色,DOTLINE
        输出MA5:收盘价的5日简单移动平均DOTLINE 画白色
        画带状线
        当满足条件收阳线时,在收盘价和开盘价位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,画红色
        K线
        JRH赋值:2日内收盘价的最高值
        JRL赋值:2日内收盘价的最低值
        MA3赋值:收盘价的3日简单移动平均
        YTSL赋值:(3*收盘价+最低价+开盘价+最高价)/6
        ABC1赋值:(收盘价>1日前的收盘价 AND 收盘价>2日前的收盘价)
        ABC2赋值:(1日前的ABC1 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC3赋值:(1日前的ABC2 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC4赋值:(1日前的ABC3 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC5赋值:(1日前的ABC4 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC6赋值:(1日前的ABC5 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC7赋值:(1日前的ABC6 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC8赋值:(1日前的ABC7 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC9赋值:(1日前的ABC8 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABCA赋值:(1日前的ABC9 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABCB赋值:(1日前的ABCA AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABCC赋值:(1日前的ABCB AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABCD赋值:(收盘价<1日前的收盘价 AND 收盘价<2日前的收盘价)
        ABCE赋值:(1日前的ABCD AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABCF赋值:(1日前的ABCE AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC10赋值:(1日前的ABCF AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC11赋值:(1日前的ABC10 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC12赋值:(1日前的ABC11 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC13赋值:(1日前的ABC12 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC14赋值:(1日前的ABC13 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC15赋值:(1日前的ABC14 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC16赋值:(1日前的ABC15 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC17赋值:(1日前的ABC16 AND 收盘价<=1日前的收盘价 AND 收盘价>=2日前的收盘价)
        ABC18赋值:(1日前的ABC17 AND 收盘价>=1日前的收盘价 AND 收盘价<=2日前的收盘价)
        ABC19赋值:((1日前的ABCDORABCEORABCFORABC10ORABC11ORABC12ORABC13ORABC14ORABC15ORABC16ORABC17ORABC18) AND ABC1)
        ABC1A赋值:((1日前的ABC1ORABC2ORABC3ORABC4ORABC5ORABC6ORABC7ORABC8ORABC9ORABCAORABCBORABCC) AND ABCD)
        输出红色持股:ABC1 OR ABC2 OR ABC3 OR ABC4 OR ABC5 OR ABC6 OR ABC7 OR ABC8 OR ABC9 OR ABCA OR ABCB OR ABCC,COLOR0000FF,NODRAW
        离场赋值:如果红色持股,返回JRL,否则返回无效数
        明离场价赋值:离场,COLORFF99FF,NODRAW
        输出今离场价:1日前的离场COLOR0000FF,NODRAW
        输出青色观望:ABCD OR ABCE OR ABCF OR ABC10 OR ABC11 OR ABC12 OR ABC13 OR ABC14 OR ABC15 OR ABC16 OR ABC17 OR ABC18,COLORFFFF00,NODRAW
        进赋值:如果青色观望,返回JRH,否则返回无效数
        明进场价赋值:进,COLOR33AACC,NODRAW
        输出今进场价:1日前的明进场价,COLORFF0000,NODRAW
        输出短买:ABC19,COLOR33AACC,NODRAW
        输出白色离场:ABC1A,COLORFF99FF,NODRAW
        输出急速超跌:(收盘价-收盘价的34日简单移动平均)/收盘价的34日简单移动平均*100<-14,COLORFFFFFF,NODRAW
        输出上市日期年:收盘价的有效数据周期数-1日前的年份,NODRAW,COLOR0000FF
        输出月:收盘价的有效数据周期数-1日前的月份,NODRAW,COLORFF00FF
        输出日:收盘价的有效数据周期数-1日前的日,NODRAW,COLOR00FFFF
        辰星线赋值:(20*YTSL+19*1日前的YTSL+18*2日前的YTSL+17*3日前的YTSL+16*4日前的YTSL+15*5日前的YTSL+14*6日前的YTSL+13*7日前的YTSL+12*8日前的YTSL+11*9日前的YTSL+10*10日前的YTSL+9*11日前的YTSL+8*12日前的YTSL+7*13日前的YTSL+6*14日前的YTSL+5*15日前的YTSL+4*16日前的YTSL+3*17日前的YTSL+2*18日前的YTSL+20日前的YTSL)/211,COLOR0000FF
        牵牛线赋值:收盘价的26日简单移动平均,COLORFF00FF
        等待赋值:如果MA3>辰星线,返回辰星线,否则返回MA3
        当满足条件ISLASTBARAND(红色持股ORREF(红色持股,1)=1)时,在今离场价和今离场价位置之间画柱状线,宽度为2.8,1不为0则画空心柱.,画红色
        当满足条件收盘价>=开盘价时,在最低价和最高价位置之间画柱状线,宽度为0,0不为0则画空心柱.,画红色
        当满足条件收阴线时,在最低价和最高价位置之间画柱状线,宽度为0,0不为0则画空心柱.,COLOR00BD00
        当满足条件收盘价>=开盘价时,在收盘价和开盘价位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,画红色
        当满足条件红色持股时,在收盘价和开盘价位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,画红色
        当满足条件青色观望时,在收盘价和开盘价位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,画蓝色
        CO赋值:(收盘价-开盘价)
        当满足条件急速超跌时,在开盘价和收盘价-CO/2位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,COLORC0C0C0
        当满足条件短买时,在开盘价和收盘价位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,COLOR00FFFF
        当满足条件白色离场时,在开盘价和收盘价位置之间画柱状线,宽度为2.8,0不为0则画空心柱.,画蓝色
        当满足条件短买时,在最低价-0.04位置画5号图标
        当满足条件白色离场时,在最高价*1.005位置画6号图标
        E赋值:(最高价+最低价+开盘价+2*收盘价)/5
        明日阻力赋值:2*E-最低价
        明日支撑赋值:2*E-最高价
        明日突破赋值:E+(最高价-最低价)
        明日反转赋值:E-(最高价-最低价)
        今日阻力赋值:1日前的明日阻力
        今日支撑赋值:1日前的明日支撑
        当满足条件收盘价不等于0时,在横轴0.90纵轴0.88位置书写文字,画红色
        当满足条件收盘价不等于0时,在横轴0.90纵轴0.96位置书写文字,画黄色
        X1赋值:如果收盘价的5日简单移动平均>收盘价的10日简单移动平均,返回20,否则返回0
        X2赋值:如果收盘价的20日简单移动平均>收盘价的60日简单移动平均,返回10,否则返回0
        X3赋值:如果KDJ的J>KDJ的K,返回10,否则返回0
        X4赋值:如果平滑异同平均线的DIF>平滑异同平均线的DEA,返回10,否则返回0
        X5赋值:如果平滑异同平均线的MACD>0,返回10,否则返回0
        X6赋值:如果成交量(手)>成交量(手)的60日简单移动平均,返回10,否则返回0
        X7赋值:如果以收盘价计算的获利盘比例>0.5,返回10,否则返回0
        X8赋值:如果收盘价/1日前的收盘价>1.03,返回10,否则返回0
        XX赋值:X1+X2+X3+X4+X5+X6+X7+X8
        当满足条件成交量(手)>开盘价时,在横轴0.90纵轴0.80位置书写文字,COLORFFFFFF
        '''
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        VOL=df['volume']
        V=df['volume']
        CAPITAL=(df['volume']/(df['换手率']))*100
        SWL=(EMA(CLOSE,10)*7+EMA(CLOSE,20)*3)/10
        SWS=DMA(EMA(CLOSE,20),1)#COLORWHITE,DOTLINE;
        MA5=MA(CLOSE,5)#DOTLINE COLORWHITE;
        #DRAWBAND(SWL,RGB(255,50,50),SWS,RGB(64,204,208))
        #STICKLINE(C>O,C,O,2.8,0),COLORRED;
        #DRAWKLINE(HIGH,OPEN,LOW,CLOSE);
        JRH=HHV(C,2)
        JRL=LLV(C,2)
        MA3=MA(CLOSE,3)
        YTSL=(3*CLOSE+LOW+OPEN+HIGH)/6
        ABC1=AND(CLOSE>REF(CLOSE,1),CLOSE>REF(CLOSE,2))
        ABC2=AND(REF(ABC1,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC3=AND(REF(ABC2,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC4=AND(REF(ABC3,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC5=AND(REF(ABC4,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC6=AND(REF(ABC5,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC7=AND(REF(ABC6,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC8=AND(REF(ABC7,1) , AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC9=AND(REF(ABC8,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABCA=AND(REF(ABC9,1) , AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABCB=AND(REF(ABCA,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABCC=AND(REF(ABCB,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABCD=AND(CLOSE<REF(CLOSE,1),CLOSE<REF(CLOSE,2))
        ABCE=AND(REF(ABCD,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABCF=AND(REF(ABCE,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC10=AND(REF(ABCF,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC11=AND(REF(ABC10,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC12=AND(REF(ABC11,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC13=AND(REF(ABC12,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC14=AND(REF(ABC13,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC15=AND(REF(ABC14,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC16=AND(REF(ABC15,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC17=AND(REF(ABC16,1),AND(CLOSE<=REF(CLOSE,1),CLOSE>=REF(CLOSE,2)))
        ABC18=AND(REF(ABC17,1),AND(CLOSE>=REF(CLOSE,1),CLOSE<=REF(CLOSE,2)))
        ABC19=AND(REF(OR(ABCD,OR(ABCE,OR(ABCF,OR(ABC10,OR(ABC11,OR(ABC12,OR(ABC13,OR(ABC14,OR(ABC15,OR(ABC16,OR(ABC17,ABC18))))))))))),1),ABC1)
        ABC1A=AND(REF(OR(ABC1,OR(ABC2,OR(ABC3,OR(ABC4,OR(ABC5,OR(ABC6,OR(ABC7,OR(ABC8,OR(ABC9,OR(ABCA,OR(ABCB,ABCC))))))))))),1),ABCD)
        红色持股=OR(ABC1,OR(ABC2,OR(ABC3,OR(ABC4,OR(ABC5,OR(ABC6,OR(ABC7,OR(ABC8,OR(ABC9,OR(ABCA,OR(ABCB,ABCC)))))))))))
        df['红色持股']=红色持股
        离场=IF(红色持股,JRL,None)
        df['离场']=离场
        明离场价=离场
        今离场价=REF(离场,1)
        青色观望=OR(ABCD,OR(ABCE,OR(ABCF,OR(ABC10,OR(ABC11,OR(ABC12,OR(ABC13,OR(ABC14,OR(ABC15,OR(ABC16,OR(ABC17,ABC18)))))))))))
        df['青色观望']=青色观望
        进=IF(青色观望,JRH,None)
        df['进']=进
        明进场价=进
        df['明进场价']=明进场价
        今进场价=REF(明进场价,1)
        df['今进场价']=今进场价
        短买=ABC19
        df['短买']=短买
        白色离场=ABC1A
        df['白色离场']=白色离场
        急速超跌=(CLOSE-MA(CLOSE,34))/MA(CLOSE,34)*100<-14
        df['急速超跌']=急速超跌
        辰星线=(20*YTSL+19*REF(YTSL,1)+18*REF(YTSL,2)+17*REF(YTSL,3)+16*REF(YTSL,4)+15*REF(YTSL,5)+14*REF(YTSL,6)+13*REF(YTSL,7)+12*REF(YTSL,8)+11*REF(YTSL,9)+10*REF(YTSL,10)+9*REF(YTSL,11)+8*REF(YTSL,12)+7*REF(YTSL,13)+6*REF(YTSL,14)+5*REF(YTSL,15)+4*REF(YTSL,16)+3*REF(YTSL,17)+2*REF(YTSL,18)+REF(YTSL,20))/211
        df['辰星线']=辰星线
        牵牛线=MA(CLOSE,26)
        df['牵牛线']=牵牛线
        等待=IF(MA3>辰星线,辰星线,MA3)
        df['等待']=等待
        '''
        STICKLINE(ISLASTBAR AND (红色持股 OR REF(红色持股,1)=1),今离场价,今离场价,2.8,1),COLORRED;
        STICKLINE(C>=O,L,H,0,0),COLORRED;
        STICKLINE(C<O, L,H,0,0),COLOR00BD00;
        STICKLINE(C>=O,C,O,2.8,0),COLORRED;
        STICKLINE(红色持股,C,O,2.8,0),COLORRED;
        STICKLINE(青色观望,C,O,2.8,0),COLORBLUE;
        '''
        CO=(C-O)
        '''
        STICKLINE(急速超跌,O,C-CO/2,2.8,0),COLORC0C0C0;
        STICKLINE(短买,O,C,2.8,0),COLOR00FFFF;
        STICKLINE(白色离场,O,C,2.8,0),COLORBLUE;
        DRAWICON(短买,L-0.04,5);
        DRAWICON(白色离场,H*1.005,6);
        '''
        E=(HIGH+LOW+OPEN+2*CLOSE)/5
        明日阻力=2*E-LOW
        明日支撑=2*E-HIGH
        明日突破=E+(HIGH-LOW)
        明日反转=E-(HIGH-LOW)
        今日阻力=REF(明日阻力 , 1)
        今日支撑=REF(明日支撑 , 1)
        df['明日支撑']=明日支撑
        df['明日突破']=明日突破
        df['明日反转']=明日反转
        df['今日阻力']=今日阻力
        df['今日支撑']=今日支撑
        '''
        DRAWTEXT_FIX(C!=0,0.90,0.88,0,STRCAT('支撑:',STRCAT(CON2STR(明日支撑,2),' 元'))),COLORRED;
        DRAWTEXT_FIX(C!=0,0.90,0.96,0,STRCAT('反转:',STRCAT(CON2STR(明日反转,2),' 元'))),COLORYELLOW;
        '''
        X1=IF(MA(C,5)>MA(C,10),20,0)
        X2=IF(MA(C,20)>MA(C,60),10,0)
        KDJ_J=KDJ(CLOSE=CLOSE,HIGH=HIGH,LOW=LOW)[-1]
        KDJ_K=KDJ(CLOSE=CLOSE,HIGH=HIGH,LOW=LOW)[0]
        X3=IF(KDJ_J>KDJ_K,10,0)
        MACD_DIF=MACD(CLOSE=CLOSE)[0]
        MACD_DEA=MACD(CLOSE=CLOSE)[1]
        MACD_MACD=MACD(CLOSE=CLOSE)[-1]
        X4=IF(MACD_DIF>MACD_DEA,10,0)
        X5=IF(MACD_MACD>0,10,0)
        X6=IF(V>MA(V,60),10,0)
        #X7=IF(xg_tdx_func_dll.WINNER(C)>0.5,10,0)
        X8=IF(C/REF(C,1)>1.03,10,0)
        XX=X1+X2+X3+X4+X5+X6+X8
        xx=(100/90)*XX
        df['量化评分']=xx
        buy_list=[]
        for 红色持股,短买 in zip(df['红色持股'].tolist(),df['短买'].tolist()):
            if 红色持股==True :
                buy_list.append('买')
            else:
                buy_list.append(None)
        sell_list=[]
        for 青色观望 in df['青色观望'].tolist():
            if 青色观望==True:
                sell_list.append('卖')
            else:
                sell_list.append(None)
        df['买']=buy_list
        df['卖']=sell_list
        stats_list=[]
        for buy,sell in zip(buy_list,sell_list):
            if buy=='买':
                stats_list.append(buy)
            elif sell=='卖':
                stats_list.append(sell)
            else:
                stats_list.append(None)
        df['stats']=stats_list
        df['stats']=df['stats'].fillna(method='ffill')
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='511090')
    print(df)
    modes=the_kirin_trend_line(df=df)
    result=modes.the_kirin_trend_line()
    print(result)
    result.to_excel(r'数据.xlsx')
   
# 参考16
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class trend_king_v2_master_chart:
    def __init__(self,df):
        '''
        趋势王V02主图
        '''
        self.df=df
    def trend_king_v2_master_chart(self):
        """
        趋势王V02主图
        输出MA1:收盘价的5日简单移动平均画白色 DOTLINE
        A1赋值:((开盘价+最高价+最低价+收盘价)/4的3日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的6日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的9日指数移动平均)/3
        A2赋值:((开盘价+最高价+最低价+收盘价)/4的5日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的10日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的20日指数移动平均)/3
        A3赋值:((开盘价+最高价+最低价+收盘价)/4的7日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的14日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的28日指数移动平均)/3
        A4赋值:((开盘价+最高价+最低价+收盘价)/4的9日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的18日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的36日指数移动平均)/3
        A5赋值:((开盘价+最高价+最低价+收盘价)/4的11日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的22日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的44日指数移动平均)/3
        A6赋值:((开盘价+最高价+最低价+收盘价)/4的13日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的26日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的52日指数移动平均)/3
        A7赋值:((开盘价+最高价+最低价+收盘价)/4的21日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的34日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的68日指数移动平均)/3
        ABC1赋值:A1的6日线性回归预测值
        ABC2赋值:A2的6日线性回归预测值
        ABC3赋值:A3的6日线性回归预测值
        ABC4赋值:A4的6日线性回归预测值
        ABC5赋值:A5的6日线性回归预测值
        ABC6赋值:A6的6日线性回归预测值
        ABC7赋值:A7的6日线性回归预测值
        输出做多线:如果ABC7>1日前的ABC7,返回ABC7,否则返回无效数,线宽为2,COLORFF00FF
        输出做空线:如果ABC7<1日前的ABC7,返回ABC7,否则返回无效数,线宽为2,COLOR00FF00
        TOWERC赋值:(3*收盘价+2*开盘价+最高价+最低价)/7的3日指数移动平均的6日线性回归预测值
        DIRECTIONMAX赋值:1日前的TOWERC和1日前的TOWERC的较大值
        DIRECTIONMIN赋值:1日前的TOWERC和1日前的TOWERC的较小值
        共振赋值:条件连续成立次数=1
        当满足条件共振时,在最低价位置画9号图标,画黄色
        建仓赋值:条件连续成立次数=1
        当满足条件建仓时,在最低价位置画1号图标

        """
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        low=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        V=df['volume']
        MA1=MA(CLOSE,5)
        A1=(EMA((OPEN+HIGH+LOW+CLOSE)/4,3)+EMA((OPEN+HIGH+LOW+CLOSE)/4,6)+EMA((OPEN+HIGH+LOW+CLOSE)/4,9))/3
        A2=(EMA((OPEN+HIGH+LOW+CLOSE)/4,5)+EMA((OPEN+HIGH+LOW+CLOSE)/4,10)+EMA((OPEN+HIGH+LOW+CLOSE)/4,20))/3
        A3=(EMA((OPEN+HIGH+LOW+CLOSE)/4,7)+EMA((OPEN+HIGH+LOW+CLOSE)/4,14)+EMA((OPEN+HIGH+LOW+CLOSE)/4,28))/3
        A4=(EMA((OPEN+HIGH+LOW+CLOSE)/4,9)+EMA((OPEN+HIGH+LOW+CLOSE)/4,18)+EMA((OPEN+HIGH+LOW+CLOSE)/4,36))/3
        A5=(EMA((OPEN+HIGH+LOW+CLOSE)/4,11)+EMA((OPEN+HIGH+LOW+CLOSE)/4,22)+EMA((OPEN+HIGH+LOW+CLOSE)/4,44))/3
        A6=(EMA((OPEN+HIGH+LOW+CLOSE)/4,13)+EMA((OPEN+HIGH+LOW+CLOSE)/4,26)+EMA((OPEN+HIGH+LOW+CLOSE)/4,52))/3
        A7=(EMA((OPEN+HIGH+LOW+CLOSE)/4,21)+EMA((OPEN+HIGH+LOW+CLOSE)/4,34)+EMA((OPEN+HIGH+LOW+CLOSE)/4,68))/3
        ABC1=FORCAST(A1,6)
        ABC2=FORCAST(A2,6)
        ABC3=FORCAST(A3,6)
        ABC4=FORCAST(A4,6)
        ABC5=FORCAST(A5,6)
        ABC6=FORCAST(A6,6)
        ABC7=FORCAST(A7,6)
        做多线=IF(ABC7>REF(ABC7,1),ABC7,None)#,LINETHICK2,COLORFF00FF;
        做空线=IF(ABC7<REF(ABC7,1),ABC7,None)#,LINETHICK2,COLOR00FF00;
        df['趋势']=IF(ABC7>REF(ABC7,1),'紫色','绿色')
        TOWERC=FORCAST(EMA((3*CLOSE+2*OPEN+HIGH+LOW)/7,3),6)
        DIRECTIONMAX=MAX(REF(TOWERC,1),REF(TOWERC,1))
        DIRECTIONMIN=MIN(REF(TOWERC,1),REF(TOWERC,1))
        共振=BARSLASTCOUNT(AND(做多线,TOWERC>=REF(TOWERC,1)))==1
        df['共振']=共振
        #DRAWICON(共振,LOW,9),COLORYELLOW;{微信公众号:尊重市场}
        建仓=BARSLASTCOUNT(TOWERC>=REF(TOWERC,1))==1
        df['建仓']=建仓
        #DRAWICON(建仓,LOW,1);
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='159920')
    modes=trend_king_v2_master_chart(df=df)
    result=modes.trend_king_v2_master_chart()
    print(result)
    result.to_excel(r'数据.xlsx')
# 参考 17
from xg_tdx_func.xg_tdx_func import *
from trader_tool.unification_data import unification_data
class trend_king_v2_subchart:
    def __init__(self,df=''):
        '''
        趋势王v2副图
        '''
        self.df=df
    def trend_king_v2_subchart(self):
        '''
        A1赋值:((开盘价+最高价+最低价+收盘价)/4的3日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的6日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的9日指数移动平均)/3
        A2赋值:((开盘价+最高价+最低价+收盘价)/4的5日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的10日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的20日指数移动平均)/3
        A3赋值:((开盘价+最高价+最低价+收盘价)/4的7日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的14日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的28日指数移动平均)/3
        A4赋值:((开盘价+最高价+最低价+收盘价)/4的9日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的18日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的36日指数移动平均)/3
        A5赋值:((开盘价+最高价+最低价+收盘价)/4的11日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的22日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的44日指数移动平均)/3
        A6赋值:((开盘价+最高价+最低价+收盘价)/4的13日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的26日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的52日指数移动平均)/3
        A7赋值:((开盘价+最高价+最低价+收盘价)/4的21日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的34日指数移动平均+(开盘价+最高价+最低价+收盘价)/4的68日指数移动平均)/3
        ABC1赋值:A1的6日线性回归预测值
        ABC2赋值:A2的6日线性回归预测值
        ABC3赋值:A3的6日线性回归预测值
        ABC4赋值:A4的6日线性回归预测值
        ABC5赋值:A5的6日线性回归预测值
        ABC6赋值:A6的6日线性回归预测值
        ABC7赋值:A7的6日线性回归预测值
        如果ABC1>1日前的ABC1,返回ABC1,否则返回无效数,POINTDOT,COLORFF00FF
        如果ABC1<1日前的ABC1,返回ABC1,否则返回无效数,POINTDOT,COLOR00FF00
        如果ABC2>1日前的ABC2,返回ABC2,否则返回无效数,POINTDOT,COLORFF00FF
        如果ABC2<1日前的ABC2,返回ABC2,否则返回无效数,POINTDOT,COLOR00FF00
        如果ABC3>1日前的ABC3,返回ABC3,否则返回无效数,POINTDOT,COLORFF00FF
        如果ABC3<1日前的ABC3,返回ABC3,否则返回无效数,POINTDOT,COLOR00FF00
        如果ABC4>1日前的ABC4,返回ABC4,否则返回无效数,POINTDOT,COLORFF00FF
        如果ABC4<1日前的ABC4,返回ABC4,否则返回无效数,POINTDOT,COLOR00FF00
        如果ABC5>1日前的ABC5,返回ABC5,否则返回无效数,POINTDOT,COLORFF00FF
        如果ABC5<1日前的ABC5,返回ABC5,否则返回无效数,POINTDOT,COLOR00FF00
        如果ABC6>1日前的ABC6,返回ABC6,否则返回无效数,POINTDOT,COLORFF00FF
        如果ABC6<1日前的ABC6,返回ABC6,否则返回无效数,POINTDOT,COLOR00FF00
        如果ABC7>1日前的ABC7,返回ABC7,否则返回无效数,线宽为2,画红色
        如果ABC7<1日前的ABC7,返回ABC7,否则返回无效数,线宽为2,COLOR00FF00
        尊重市场赋值:(3*收盘价+2*开盘价+最高价+最低价)/7的3日指数移动平均的6日线性回归预测值
        DIRECTIONMAX赋值:1日前的尊重市场和1日前的尊重市场的较大值
        DIRECTIONMIN赋值:1日前的尊重市场和1日前的尊重市场的较小值
        当满足条件尊重市场>=1日前的尊重市场时,在尊重市场和DIRECTIONMAX位置之间画柱状线,宽度为4,0不为0则画空心柱.,画黄色
        当满足条件尊重市场<1日前的尊重市场时,在尊重市场和DIRECTIONMIN位置之间画柱状线,宽度为4,0不为0则画空心柱.,COLOR00FF00
        '''
        df=self.df
        CLOSE=df['close']
        C=df['close']
        LOW=df['low']
        L=df['low']
        low=df['low']
        HIGH=df['high']
        H=df['high']
        OPEN=df['open']
        O=df['open']
        volume=df['volume']
        V=df['volume']
        A1=(EMA((OPEN+HIGH+LOW+CLOSE)/4,3)+EMA((OPEN+HIGH+LOW+CLOSE)/4,6)+EMA((OPEN+HIGH+LOW+CLOSE)/4,9))/3
        A2=(EMA((OPEN+HIGH+LOW+CLOSE)/4,5)+EMA((OPEN+HIGH+LOW+CLOSE)/4,10)+EMA((OPEN+HIGH+LOW+CLOSE)/4,20))/3
        A3=(EMA((OPEN+HIGH+LOW+CLOSE)/4,7)+EMA((OPEN+HIGH+LOW+CLOSE)/4,14)+EMA((OPEN+HIGH+LOW+CLOSE)/4,28))/3
        A4=(EMA((OPEN+HIGH+LOW+CLOSE)/4,9)+EMA((OPEN+HIGH+LOW+CLOSE)/4,18)+EMA((OPEN+HIGH+LOW+CLOSE)/4,36))/3
        A5=(EMA((OPEN+HIGH+LOW+CLOSE)/4,11)+EMA((OPEN+HIGH+LOW+CLOSE)/4,22)+EMA((OPEN+HIGH+LOW+CLOSE)/4,44))/3
        A6=(EMA((OPEN+HIGH+LOW+CLOSE)/4,13)+EMA((OPEN+HIGH+LOW+CLOSE)/4,26)+EMA((OPEN+HIGH+LOW+CLOSE)/4,52))/3
        A7=(EMA((OPEN+HIGH+LOW+CLOSE)/4,21)+EMA((OPEN+HIGH+LOW+CLOSE)/4,34)+EMA((OPEN+HIGH+LOW+CLOSE)/4,68))/3
        ABC1=FORCAST(A1,6)
        ABC2=FORCAST(A2,6)
        ABC3=FORCAST(A3,6)
        ABC4=FORCAST(A4,6)
        ABC5=FORCAST(A5,6)
        ABC6=FORCAST(A6,6)
        ABC7=FORCAST(A7,6)
        '''
        IF(ABC1>REF(ABC1,1),ABC1,None),POINTDOT,COLORFF00FF;
        IF(ABC1<REF(ABC1,1),ABC1,None),POINTDOT,COLOR00FF00;
        IF(ABC2>REF(ABC2,1),ABC2,None),POINTDOT,COLORFF00FF;
        IF(ABC2<REF(ABC2,1),ABC2,None),POINTDOT,COLOR00FF00;
        IF(ABC3>REF(ABC3,1),ABC3,None),POINTDOT,COLORFF00FF;
        IF(ABC3<REF(ABC3,1),ABC3,None),POINTDOT,COLOR00FF00;
        IF(ABC4>REF(ABC4,1),ABC4,None),POINTDOT,COLORFF00FF;
        IF(ABC4<REF(ABC4,1),ABC4,None),POINTDOT,COLOR00FF00;
        IF(ABC5>REF(ABC5,1),ABC5,None),POINTDOT,COLORFF00FF;
        IF(ABC5<REF(ABC5,1),ABC5,None),POINTDOT,COLOR00FF00;
        IF(ABC6>REF(ABC6,1),ABC6,None),POINTDOT,COLORFF00FF;
        IF(ABC6<REF(ABC6,1),ABC6,None),POINTDOT,COLOR00FF00;
        '''
        '''
        IF(ABC7>REF(ABC7,1),ABC7,None),LINETHICK2,COLORRED;
        IF(ABC7<REF(ABC7,1),ABC7,None),LINETHICK2,COLOR00FF00;
        '''
        df['趋势线']=IF(ABC7>REF(ABC7,1),'红色',"绿色")
        尊重市场=FORCAST(EMA((3*CLOSE+2*OPEN+HIGH+LOW)/7,3),6)
        DIRECTIONMAX=MAX(REF(尊重市场,1),REF(尊重市场,1))
        DIRECTIONMIN=MIN(REF(尊重市场,1),REF(尊重市场,1))
        '''
        STICKLINE(尊重市场>=REF(尊重市场,1),尊重市场,DIRECTIONMAX,4,0),COLORYELLOW;
        STICKLINE(尊重市场<REF(尊重市场,1),尊重市场,DIRECTIONMIN,4,0),COLOR00FF00;
        '''
        df['方块']=IF(尊重市场>=REF(尊重市场,1),"黄色","绿色")
        return df
if __name__=='__main__':
    data=unification_data(trader_tool='ths')
    data=data.get_unification_data()
    df=data.get_hist_data_em(stock='159920')
    modes=trend_king_v2_subchart(df=df)
    result=modes.trend_king_v2_subchart()
    print(result)
    result.to_excel(r'数据.xlsx')
