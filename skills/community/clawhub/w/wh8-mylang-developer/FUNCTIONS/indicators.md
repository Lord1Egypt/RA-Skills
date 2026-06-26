# WT8技术指标函数

## 目录
1. [移动平均线](#一移动平均线)
2. [最高最低](#二最高最低)
3. [交叉判断](#三交叉判断)
4. [布林带](#四布林带)
5. [MACD](#五macd)
6. [其他常用](#六其他常用)

---

## 一、移动平均线

### MA - 简单移动平均
```mql
MA(X, N)
```
- X：数据序列
- N：周期数
- 返回：N周期简单平均值

```mql
MA5:MA(C,5);     // 5日均线
MA10:MA(C,10);   // 10日均线
MA20:MA(C,20);   // 20日均线
```

### EMA - 指数移动平均
```mql
EMA(X, N)
```
- X：数据序列
- N：周期数
- 返回：N周期指数加权平均值

```mql
EMA12:EMA(C,12);  // 12日指数均线
EMA26:EMA(C,26);  // 26日指数均线
```

### SMA - 平滑移动平均
```mql
SMA(X, N, M)
```
- X：数据序列
- N：周期
- M：权重
- 返回：(M*X + (N-M)*昨日SMA) / N

---

## 二、最高最低

### HHV - N周期最高值
```mql
HHV(X, N)
```
- X：数据序列
- N：周期数
- 返回：最近N个周期中X的最大值

```mql
HHV10:HHV(HIGH,10);   // 10周期最高价
HHV(HIGH,20), BK;     // 创20周期新高买开
```

### LLV - N周期最低值
```mql
LLV(X, N)
```
- X：数据序列
- N：周期数
- 返回：最近N个周期中X的最小值

```mql
LLV10:LLV(LOW,10);   // 10周期最低价
LLV(LOW,20), SK;      // 创20周期新低卖开
```

### HHVBARS - 距最高价的周期数
```mql
HHVBARS(X, N)
```
- 返回：当前时点距离N周期内最高价的K线根数

```mql
HHVBARS(HIGH,20)=0, SP;  // 创20日新高平多
```

### LLVBARS - 距最低价的周期数
```mql
LLVBARS(X, N)
```
- 返回：当前时点距离N周期内最低价的K线根数

---

## 三、交叉判断

### CROSS - 上穿
```mql
CROSS(X, Y)
```
- X上穿Y：X从下方穿越到Y上方
- 返回：1（成立）或0（不成立）

```mql
CROSS(MA5,MA10), BK;   // 5日均线上穿10日均线买开
```

### CROSSDOWN - 下穿
```mql
CROSSDOWN(X, Y)
```
- X下穿Y：X从上方穿越到Y下方
- 返回：1（成立）或0（不成立）

```mql
CROSSDOWN(MA5,MA10), SP;  // 5日均线下穿10日均线卖平
```

### 示例：双均线策略
```mql
MA5:MA(C,5);
MA10:MA(C,10);

// 金叉买开
CROSS(MA5,MA10), BK;

// 死叉卖平
CROSSDOWN(MA5,MA10), SP;

AUTOFILTER;
```

---

## 四、布林带

### BOLL - 布林带
```mql
MID:MA(CLOSE,26);                    // 中轨
TMP2:=STD(CLOSE,26);                // 标准差
TOP:MID+2*TMP2;                      // 上轨
BOTTOM:MID-2*TMP2;                   // 下轨
```

### STD - 标准差
```mql
STD(X, N)
```
- X：数据序列
- N：周期数
- 返回：N周期标准差

```mql
STD20:STD(CLOSE,20);  // 20周期收盘价标准差
```

### 用法示例
```mql
MID:MA(C,26);
TMP2:=STD(C,26);
TOP:MID+2*TMP2;
BOTTOM:MID-2*TMP2;

// 价格上穿上轨买开
CROSS(CLOSE,TOP), BK;

// 价格下穿下轨卖开
CROSSDOWN(CLOSE,BOTTOM), SK;

// 价格回到中轨平仓
CROSSDOWN(CLOSE,MID), SP;

AUTOFILTER;
```

---

## 五、MACD

### MACD默认公式
```mql
DIF:EMA(CLOSE,12)-EMA(CLOSE,26);  // 快线
DEA:EMA(DIF,9);                     // 慢线
MACD:(DIF-DEA)*2;                   // 柱状图
```

### 金叉死叉
```mql
// MACD金叉（DIF上穿DEA）
CROSS(DIF,DEA), BK;

// MACD死叉（DIF下穿DEA）
CROSSDOWN(DIF,DEA), SP;
```

### 零轴判断
```mql
// DIF在零轴上方
DIF>0, BK;

// DIF在零轴下方
DIF<0, SK;
```

---

## 六、其他常用

### REF - 引用N周期前的值
```mql
REF(X, N)
```
- X：数据序列
- N：周期数
- 返回：N周期前的X值

```mql
REF(CLOSE,1);       // 上一根K线收盘价
REF(HIGH,5)=HHV(HIGH,20);  // 创20日新高
```

### SUM - 求和
```mql
SUM(X, N)
```
- X：数据序列
- N：周期数
- 返回：N周期X的总和

```mql
SUM(VOL,10)/10;     // 10周期平均成交量
SUM(VOL,5)>SUM(VOL,20), BK;  // 5日均量大于20日均量
```

### ABS - 绝对值
```mql
ABS(X)
```
- 返回：X的绝对值

```mql
ABS(CLOSE-BKPRICE);  // 持仓盈亏点数
```

### MAX - 最大值
```mql
MAX(X, Y)
```
- 返回：X和Y中的较大值

### MIN - 最小值
```mql
MIN(X, Y)
```
- 返回：X和Y中的较小值

### IF - 条件取值
```mql
IF(条件, X, Y)
```
- 条件成立返回X，否则返回Y

```mql
IF(CLOSE>MA(C,10), 1, 0);  // 价格在均线上返回1
```

### BETWEEN - 区间判断
```mql
BETWEEN(X, A, B)
```
- X在A和B之间（含）返回1

```mql
BETWEEN(CLOSE, MA(C,10), MA(C,20));  //价格在两条均线之间
```

---

## 指标组合示例

### 趋势跟踪策略
```mql
// 参数
N1:=10;  // 短周期
N2:=20;  // 长周期

// 均线
MA1:MA(C,N1);
MA2:MA(C,N2);

// 趋势判断
多头:=MA1>MA2;
空头:=MA1<MA2;

// 交易
多头 AND CROSS(CLOSE,MA1), BK;      // 多头趋势且价格上穿短均线买开
NOT 多头, SP;                        // 不再是多头就平仓

空头 AND CROSSDOWN(CLOSE,MA1), SK;  // 空头趋势且价格下穿短均线卖开
NOT 空头, BP;                        // 不再是空头就平仓

AUTOFILTER;
```

### 突破策略
```mql
// 20日高低点突破
HH20:HHV(HIGH,20);
LL20:LLV(LOW,20);

// 突破20日高点买开
CLOSE>HH20, BK;

// 跌破20日低点卖开
CLOSE<LL20, SK;

// 止损
CLOSE<BKPRICE-10*MINPRICE, SP;
CLOSE>SKPRICE+10*MINPRICE, BP;

AUTOFILTER;
```
