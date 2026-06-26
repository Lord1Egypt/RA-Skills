# WT8头寸管理示例

## 一、按资金比例下单

```mql
// 按资金比例下单
// 每次按理论资金的fPercent比例下单，最大N手
// 适合资金管理严格的组合

SETDEALPERCENT(20, 10);  // 每次按资金的20%下单，最大10手

MA10:MA(C,10);
MA20:MA(C,20);

// 策略
CROSS(MA10,MA20), BK;
CROSSDOWN(MA10,MA20), SK;

// 止损
CLOSE<=BKPRICE*0.98, SP;
CLOSE>=SKPRICE*1.02, BP;

AUTOFILTER;
```

---

## 二、固定手数 + 动态调整

```mql
// 固定手数开仓，亏损后手数增加
// 盈利后恢复默认手数

N:=1;  // 默认开仓手数

// 持续亏损次数
Q:=TNUMSEQLOSS;

// 动态调整手数：亏损+N，盈利恢复默认
T:=IF(LASTOFFSETPROFIT>=0 || (COUNTSIG(BK,BARPOS)+COUNTSIG(SK,BARPOS)=0), N, N+Q);
TC:=MIN(T, 10);  // 最大10手

// 设置开仓手数
T_COMMAND(TC);

MA10:MA(C,10);
MA20:MA(C,20);

// 策略
CROSS(MA10,MA20), BK;
CROSSDOWN(MA10,MA20), SK;

// 止损
CLOSE<=BKPRICE-15*MINPRICE, SP;
CLOSE>=SKPRICE+15*MINPRICE, BP;

AUTOFILTER;
```

---

## 三、权益回撤控制

```mql
// 权益回撤控制
// 权益回撤超过20%时，清仓止损

// 计算权益回撤比
HM:=HHV(MONEYTOT,BARPOS);
QY:=(HM-MONEYTOT)/HM;  // 权益回撤比

// 权益回撤比超过20%止损
QY>0.2, SP;
QY>0.2, BP;

// 均线策略
MA20:MA(C,20);
CLOSE>MA20, BK;
CLOSE<MA20, SP;

AUTOFILTER;
```

---

## 四、资金使用率控制

```mql
// 资金使用率控制
// 通过SETDEALPERCENT控制每笔交易的风险

// 参数设置
资金使用率:=30;  // 每笔交易使用30%资金
最大手数:=5;     // 最多5手

SETDEALPERCENT(资金使用率, 最大手数);

// 均线策略
MA10:MA(C,10);
MA20:MA(C,20);

CROSS(MA10,MA20), BK;
CROSSDOWN(MA10,MA20), SP;

// 止损
CLOSE<=BKPRICE*0.97, SP;
CLOSE>=SKPRICE*1.03, BP;

AUTOFILTER;
```

---

## 五、综合头寸管理

```mql
// 综合头寸管理示例
// 资金使用率 + 权益止损 + 动态手数

// ========== 头寸管理 ==========
// 1. 按资金比例下单
SETDEALPERCENT(25, 8);  // 25%资金，最大8手

// 2. 权益止损
HM:=HHV(MONEYTOT,BARPOS);
QY:=(HM-MONEYTOT)/HM;
QY>0.15, SP;    // 权益回撤15%止损
QY>0.15, BP;

// 3. 最大持仓限制
// 实际通过SETDEALPERCENT的第二个参数控制

// ========== 交易策略 ==========
MA10:MA(C,10);
MA20:MA(C,20);

// 开仓
CROSS(MA10,MA20), BK;
CROSSDOWN(MA10,MA20), SK;

// 止损
CLOSE<=BKPRICE*0.98, SP;
CLOSE>=SKPRICE*1.02, BP;

AUTOFILTER;
```
