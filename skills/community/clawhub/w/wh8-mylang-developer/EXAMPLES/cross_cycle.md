# WT8跨周期跨合约示例

## 一、引用日线数据

```mql
// ============================================
// 第一步：建立日线指标（保存为 DAY_MA）
// ============================================
DAY_MA
MA5:MA(C,5);
MA30:MA(C,30);
DAYUP:MA5>MA30;  // 日线多头
DAYDN:MA5<MA30;  // 日线空头
```

```mql
// ============================================
// 第二步：在分钟周期引用日线数据
// ============================================

// 引用日线指标
#IMPORT[DAY,1,DAY_MA] AS D

DAYUP:D.DAYUP;
DAYDN:D.DAYDN;

// 分钟周期自己的条件
MA5:MA(C,5);
MA10:MA(C,10);

MINUP:CROSS(MA5,MA10);       // 分钟金叉
MINDN:CROSSDOWN(MA5,MA10);   // 分钟死叉

// 综合判断：日线多头 + 分钟金叉 → 做多
DAYUP && MINUP, BPK;

// 综合判断：日线空头 + 分钟死叉 → 做空
DAYDN && MINDN, SPK;

AUTOFILTER;
```

---

## 二、三周期共振

```mql
// 日线指标（保存为 DAY_IND）
DAY_IND
MA5:MA(C,5);
MA20:MA(C,20);
DAYUP:MA5>MA20;
DAYDN:MA5<MA20;
```

```mql
// 小时指标（保存为 HOUR_IND）
HOUR_IND
MID:MA(CLOSE,26);
TMP2:=STD(CLOSE,26);
TOP:MID+2*TMP2;
BOTTOM:MID-2*TMP2;
HOURUP:C>TOP;
HOURDN:C<BOTTOM;
```

```mql
// ============================================
// 三周期共振策略（加载到分钟周期）
// ============================================

// 引用日线
#IMPORT[DAY,1,DAY_IND] AS D
DAYUP:D.DAYUP;
DAYDN:D.DAYDN;

// 引用小时
#IMPORT[HOUR,1,HOUR_IND] AS H
HOURUP:H.HOURUP;
HOURDN:H.HOURDN;

// 分钟条件
MINUP:CROSS(MA(C,5),MA(C,10));
MINDN:CROSSDOWN(MA(C,5),MA(C,10));

// 三周期共振做多
DAYUP && HOURUP && MINUP, BPK;

// 三周期共振做空
DAYDN && HOURDN && MINDN, SPK;

// 止损
CLOSE<=BKPRICE-15*MINPRICE, SP;
CLOSE>=SKPRICE+15*MINPRICE, BP;

AUTOFILTER;
```

---

## 三、引用板块指数

```mql
// 板块指数指标（保存为 HG_IND）
HG_IND
MA5:MA(C,5);
MA10:MA(C,10);
MA30:MA(C,30);
HGUP:MA5>MA10 && MA10>MA30;  // 板块多头
HGDN:MA5<MA10 && MA10<MA30;  // 板块空头
```

```mql
// ============================================
// 板块对冲策略（加载到螺纹钢）
// ============================================

// 引用黑色系板块（7161）
#CALL[7161,HG_IND] AS VAR

// 螺纹自己的均线
MA5:MA(C,5);
MA30:MA(C,30);
RBUP:MA5>MA30;
RBDN:MA5<MA30;

// 综合判断：板块 + 单合约同向
RBUP && VAR.HGUP, BK;
RBDN && VAR.HGDN, SK;

// 平仓
CLOSE<MA30 && BKVOL>0, SP;
CLOSE>MA30 && SKVOL>0, BP;

AUTOFILTER;
```

---

## 四、跨合约套利

```mql
// 螺纹-热卷价差策略
// 当螺纹比热卷低时，买螺纹卖热卷

// 螺纹指标
MA5:MA(C,5);

// 引用热卷数据
// 假设热卷合约代码为 HC

MA5:MA(C,5);           // 螺纹5日均线
MA20:MA(C,20);         // 螺纹20日均线

// 螺纹与热卷价差
// 使用跨合约引用的方式获取热卷价格

// 简单策略：螺纹与热卷的比值
// 当螺纹相对热卷走强时买螺纹

MA5>MA20, BK;          // 螺纹多头排列买开
MA5<MA20, SK;          // 螺纹空头排列卖开

// 止损
CLOSE<=BKPRICE*0.98, SP;
CLOSE>=SKPRICE*1.02, BP;

AUTOFILTER;
```

---

## 五、综合跨周期跨合约

```mql
// 日线指标（保存为 DAY_IND）
DAY_IND
MA5:MA(C,5);
MA10:MA(C,10);
MA20:MA(C,20);
DAYUP:MA5>MA20;  // 日线多头
DAYDN:MA5<MA20;  // 日线空头
```

```mql
// ============================================
// 综合策略
// 日线趋势 + 板块方向 + 分钟信号
// ============================================

// 引用日线趋势
#IMPORT[DAY,1,DAY_IND] AS D

// 引用板块（黑链7161）
#CALL[7161,HG_IND] AS VAR

// 分钟MACD
DIFF:=EMA(CLOSE,12)-EMA(CLOSE,26);
DEA:=EMA(DIFF,9);
MACDUP:CROSS(DIFF,DEA);        // MACD金叉
MACDDN:CROSSDOWN(DIFF,DEA);    // MACD死叉

// 综合做多：日线多头 + 板块多头 + MACD金叉
D.DAYUP && VAR.HGUP && MACDUP, BPK;

// 综合做空：日线空头 + 板块空头 + MACD死叉
D.DAYDN && VAR.HGDN && MACDDN, SPK;

// 止损
CLOSE<=BKPRICE-20*MINPRICE, SP;
CLOSE>=SKPRICE+20*MINPRICE, BP;

AUTOFILTER;
```
