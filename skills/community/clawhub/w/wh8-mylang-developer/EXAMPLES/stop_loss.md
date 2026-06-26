# WT8止损止盈示例

## 一、固定点差止损

```mql
// 固定点差止损
// 亏损N跳止损

N:=10;  // 止损跳数

MA10:MA(C,10);

// 金叉买开
CROSS(CLOSE,MA10), BK;

// 死叉卖开
CROSSDOWN(CLOSE,MA10), SK;

// 固定点差止损
CLOSE<=BKPRICE-N*MINPRICE, SP;    // 多头亏损N跳止损
CLOSE>=SKPRICE+N*MINPRICE, BP;   // 空头亏损N跳止损

AUTOFILTER;
```

---

## 二、固定比例止损

```mql
// 固定比例止损
// 亏损5%止损

止损比例:=5;  // 5%

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;
CLOSE<MA20, SK;

// 固定比例止损
CLOSE<=BKPRICE*(1-止损比例/100), SP;
CLOSE>=SKPRICE*(1+止损比例/100), BP;

AUTOFILTER;
```

---

## 三、动态追踪止损

```mql
// 动态追踪止损
// 从持仓期间最高/最低点回撤N跳止损
// 优点：让利润奔跑

N:=20;  // 回撤跳数

MA10:MA(C,10);

// 开仓
CROSS(CLOSE,MA10), BK;
CROSSDOWN(CLOSE,MA10), SK;

// 动态追踪止损
// 多头：从持仓期间最高价回撤N跳止损
CLOSE<=BKHIGH-N*MINPRICE, SP;

// 空头：从持仓期间最低价上涨N跳止损
CLOSE>=SKLOW+N*MINPRICE, BP;

AUTOFILTER;
```

---

## 四、固定点差止盈

```mql
// 固定点差止盈
// 盈利M跳止盈

M:=30;  // 止盈跳数

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;
CLOSE<MA20, SK;

// 止盈
CLOSE>=BKPRICE+M*MINPRICE, SP;    // 多头盈利M跳止盈
CLOSE<=SKPRICE-M*MINPRICE, BP;   // 空头盈利M跳止盈

AUTOFILTER;
```

---

## 五、保本止损

```mql
// 保本止损
// 盈利超过N跳后，跌破开仓价+M跳时保本平仓
// 适合趋势策略

N:=20;  // 保本开启参数（盈利超过N跳后启用）
M:=5;   // 保本参数（回落到开仓价+M跳保本）

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;
CLOSE<MA20, SK;

// 保本止损
// 多头：盈利超过N跳后，回落到开仓价+M跳保本平
BKHIGH>BKPRICE+N*MINPRICE && CLOSE<=BKPRICE+M*MINPRICE, SP;

// 空头：盈利超过N跳后，反弹到开仓价-M跳保本平
SKLOW<SKPRICE-N*MINPRICE && CLOSE>=SKPRICE-M*MINPRICE, BP;

AUTOFILTER;
```

---

## 六、综合止损止盈

```mql
// 综合止损止盈示例
// 止损 + 止盈 + 保本 + 追踪

止损N:=15;   // 固定止损跳数
止盈M:=40;   // 固定止盈跳数
保本N2:=20;  // 保本开启跳数
保本M2:=5;   // 保本回撤跳数
追踪N3:=25;  // 追踪止损跳数

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;
CLOSE<MA20, SK;

// 1. 固定止损
CLOSE<=BKPRICE-止损N*MINPRICE, SP;
CLOSE>=SKPRICE+止损N*MINPRICE, BP;

// 2. 固定止盈
CLOSE>=BKPRICE+止盈M*MINPRICE, SP;
CLOSE<=SKPRICE-止盈M*MINPRICE, BP;

// 3. 保本止损（盈利后启用）
BKHIGH>BKPRICE+保本N2*MINPRICE && CLOSE<=BKPRICE+保本M2*MINPRICE, SP;
SKLOW<SKPRICE-保本N2*MINPRICE && CLOSE>=SKPRICE-保本M2*MINPRICE, BP;

// 4. 追踪止损（最后防线）
CLOSE<=BKHIGH-追踪N3*MINPRICE, SP;
CLOSE>=SKLOW+追踪N3*MINPRICE, BP;

AUTOFILTER;
```

---

## 七、权益止损

```mql
// 权益止损
// 权益回撤超过一定比例时止损
// 适合组合风控

回撤比例:=10;  // 权益回撤10%

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;
CLOSE<MA20, SK;

// 权益止损：权益回撤超过X%清仓
MONEYTOT<=INITMONEY*(1-回撤比例/100), SP;
MONEYTOT<=INITMONEY*(1-回撤比例/100), BP;

AUTOFILTER;
```

---

## 八、权益回撤比止损

```mql
// 权益回撤比止损
// 从历史最高点回撤超过X%止损
// 更精确的风控

回撤比:=20;  // 回撤20%

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;
CLOSE<MA20, SK;

// 计算权益回撤比
HM:=HHV(MONEYTOT,BARPOS);  // 历史最高权益
QY:=(HM-MONEYTOT)/HM*100;  // 权益回撤比(%)

// 权益回撤比止损
QY>回撤比, SP;
QY>回撤比, BP;

AUTOFILTER;
```
