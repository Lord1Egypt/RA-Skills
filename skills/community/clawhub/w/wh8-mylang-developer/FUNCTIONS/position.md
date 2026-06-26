# WT8持仓资金管理函数

## 目录
1. [持仓查询](#一持仓查询)
2. [资金查询](#二资金查询)
3. [头寸管理](#三头寸管理)
4. [止损止盈](#四止损止盈)
5. [风控函数](#五风控函数)

---

## 一、持仓查询

### BKVOL - 多头持仓手数
```mql
BKVOL
```
- 返回：当前多头持仓手数
- 示例：
```mql
BKVOL > 0;          // 有多头持仓
BKVOL >= 3;         // 多头持仓至少3手
BKVOL > 0 AND CLOSE < BKPRICE, SP;  // 有多头且亏损就平仓
```

### SKVOL - 空头持仓手数
```mql
SKVOL
```
- 返回：当前空头持仓手数
- 示例：
```mql
SKVOL > 0;          // 有空头持仓
SKVOL < 3;          // 空头持仓少于3手
```

### VOL() - 总持仓手数
```mql
VOL()
```
- 返回：总持仓手数（多头+空头的绝对值）
- 示例：
```mql
VOL() = 0;         // 无持仓
VOL() > 0;         // 有持仓
```

---

## 二、资金查询

### MONEYTOT - 当前权益
```mql
MONEYTOT
```
- 返回：当前总权益（含浮动盈亏）
- 说明：账户可用资金 + 持仓保证金 + 浮动盈亏
- 示例：
```mql
MONEYTOT <= INITMONEY * 0.9;     // 权益回撤10%
MONEYTOT > INITMONEY * 1.1;      // 盈利超过10%
```

### INITMONEY - 初始资金
```mql
INITMONEY
```
- 返回：回测/运行设置的初始资金
- 示例：
```mql
INITMONEY + 10000;               // 在初始资金基础上加1万
MONEYTOT / INITMONEY;            // 计算收益率
```

### 权益计算公式
```
当前权益 = 可用资金 + 持仓保证金 + 浮动盈亏
```

---

## 三、头寸管理

### SETDEALPERCENT - 按资金比例下单
```mql
SETDEALPERCENT(fPercent, N)
```
- fPercent：下单资金占理论资金的比例（%）
- N：最大下单手数
- 作用：每次按当前理论资金的比例下单

```mql
SETDEALPERCENT(20, 10);  // 每次按理论资金的20%下单，最大10手
```

**示例场景**：
```mql
// 初始资金10万，保证金率10%
// 按20%资金使用率下单，螺纹钢10吨/手，假设价格4000
// 下单手数 = 100000 * 20% / (4000 * 10 * 10%) = 5手
```

### T_COMMAND - 设置开仓手数
```mql
T_COMMAND(N)
```
- N：固定开仓手数
- 作用：设置首次建仓的手数

```mql
T_COMMAND(5);  // 每次开仓5手
```

### TRADE_AGAIN - 加减仓可重复次数
```mql
TRADE_AGAIN(N)
```
- N：同一行加减仓指令最多连续出现的次数
- 作用：允许分批加仓/减仓

```mql
TRADE_AGAIN(3);  // 加减仓可连续3次
CLOSE > BKPRICE * 1.02, ADD_LONG(BKVOL/2);  // 每次盈利2%加仓一半
```

---

## 四、止损止盈

### BKPRICE - 多头开仓价
```mql
BKPRICE
```
- 返回：多头开仓的平均价格
- 示例：
```mql
// 固定点差止损：亏损N跳止损
N:=10;
CLOSE <= BKPRICE - N*MINPRICE, SP;

// 固定比例止损：亏损5%止损
CLOSE <= BKPRICE * (1-5/100), SP;
```

### SKPRICE - 空头开仓价
```mql
SKPRICE
```
- 返回：空头开仓的平均价格
- 示例：
```mql
// 固定点差止损
N:=10;
CLOSE >= SKPRICE + N*MINPRICE, BP;
```

### BKHIGH - 多头持仓期间最高价
```mql
BKHIGH
```
- 返回：多头持仓以来的最高价
- 用途：动态追踪止损

```mql
// 动态追踪止损：从最高点回撤N跳止损
N:=20;
CLOSE <= BKHIGH - N*MINPRICE, SP;
```

### SKLOW - 空头持仓期间最低价
```mql
SKLOW
```
- 返回：空头持仓以来的最低价
- 用途：动态追踪止损

```mql
// 动态追踪止损
N:=20;
CLOSE >= SKLOW + N*MINPRICE, BP;
```

### MINPRICE - 最小变动价位
```mql
MINPRICE
```
- 返回：当前合约的最小跳动
- 说明：螺纹钢=1，沪铜=10，股指=0.2

```mql
// 用MINPRICE计算跳数
CLOSE - BKPRICE >= 10*MINPRICE;  // 盈利至少10跳
```

---

## 五、风控函数

### 权益回撤止损
```mql
// 权益回撤超过20%清仓
MONEYTOT <= INITMONEY * (1-20/100), SP;   // 多头清仓
MONEYTOT <= INITMONEY * (1-20/100), BP;   // 空头清仓
```

### 权益回撤比计算
```mql
HM:=HHV(MONEYTOT, BARPOS);  // 历史最高权益
QY:(HM-MONEYTOT)/HM;         // 权益回撤比
QY > 0.2, SP;                 // 回撤超过20%平多
```

### 连续亏损控制
```mql
Q:=TNUMSEQLOSS;  // 持续亏损次数
T:=IF(LASTOFFSETPROFIT>=0, N, N+Q);  // 亏损后手数+N
TC:=MIN(T, 10);   // 最大10手
T_COMMAND(TC);
```

### 保本止损
```mql
// 开多后最高上涨超过N跳，回落到开仓价+M跳保本平多
N:=20;
M:=5;
BKHIGH>BKPRICE+N*MINPRICE && CLOSE<=BKPRICE+M*MINPRICE, SP;
```

---

## 完整示例

### 示例1：带止损的趋势策略
```mql
// 参数
N:=10;  // 止损跳数

MA5:MA(C,5);
MA20:MA(C,20);

// 开仓条件
CROSS(MA5,MA20), BK;
CROSSDOWN(MA5,MA20), SK;

// 止损
CLOSE <= BKPRICE - N*MINPRICE, SP;
CLOSE >= SKPRICE + N*MINPRICE, BP;

AUTOFILTER;
```

### 示例2：动态追踪止损
```mql
// 参数
N:=20;  // 回撤跳数

// 开仓
MA5:MA(C,5);
MA10:MA(C,10);
CROSS(MA5,MA10), BK;
CROSSDOWN(MA5,MA10), SK;

// 动态追踪止损
CLOSE <= BKHIGH - N*MINPRICE, SP;
CLOSE >= SKLOW + N*MINPRICE, BP;

AUTOFILTER;
```

### 示例3：按资金比例下单
```mql
// 每次按资金的20%下单，最大5手
SETDEALPERCENT(20,5);

// 均线策略
MA10:MA(C,10);
MA20:MA(C,20);

CROSS(MA10,MA20), BK;
CROSSDOWN(MA10,MA20), SP;

// 止损
CLOSE <= BKPRICE*0.98, SP;
CLOSE >= SKPRICE*1.02, BP;

AUTOFILTER;
```

### 示例4：权益风控
```mql
// 权益回撤10%止损
HM:=HHV(MONEYTOT,BARPOS);
QY:=(HM-MONEYTOT)/HM;
QY>0.1, SP;
QY>0.1, BP;

// 均线策略
MA20:MA(C,20);
CLOSE>MA20, BK;
CLOSE<MA20, SP;

AUTOFILTER;
```
