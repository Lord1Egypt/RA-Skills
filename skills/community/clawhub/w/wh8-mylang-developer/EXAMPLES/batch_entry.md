# WT8分批进出示例

## 一、分批建仓

```mql
// 分批建仓示例
// 先开6手，盈利后加仓

// 每次固定开仓6手
T_COMMAND(6);

// 允许加减仓指令连续出现3次
TRADE_AGAIN(3);

MA1:MA(CLOSE,30);

// 开仓
CROSS(CLOSE,MA1), BK;

// 盈利2%时，加仓一半
CLOSE>BKPRICE*(1+2/100), ADD_LONG(BKVOL/2);

// 价格下穿均线，全平
CROSSDOWN(CLOSE,MA1), SP;

AUTOFILTER;
```

---

## 二、盈利加仓

```mql
// 盈利加仓示例
// 开仓后，盈利逐步加仓
// 亏损减仓

M:=0.02;  // 加仓盈利比例2%
N:=0.01;  // 减仓亏损比例1%

// 每次固定开仓4手
T_COMMAND(4);

// 允许加减仓连续3次
TRADE_AGAIN(3);

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;

// 盈利2%时，加仓一半持仓
CLOSE>BKPRICE*(1+M), ADD_LONG(BKVOL/2);

// 亏损1%时，减仓一半持仓
CLOSE<BKPRICE*(1-N), LOWER_LONG(BKVOL/2);

// 平仓
CLOSE<MA20, SP;

AUTOFILTER;
```

---

## 三、分批出场

```mql
// 分批出场示例
// 盈利后分批平仓

M:=0.03;  // 第一批止盈3%

T_COMMAND(6);  // 开仓6手
TRADE_AGAIN(3);  // 允许加减仓3次

MA20:MA(C,20);

// 开仓
CLOSE>MA20, BK;

// 第一批止盈：盈利3%平一半
CLOSE>=BKPRICE*(1+M), LOWER_LONG(3);

// 第二批止盈：盈利6%再平一半
CLOSE>=BKPRICE*(1+M*2), LOWER_LONG(3);

// 第三批止盈：盈利10%全部平
CLOSE>=BKPRICE*(1+0.1), SP;

// 止损
CLOSE<BKPRICE*(1-0.02), SP;

AUTOFILTER;
```

---

## 四、金字塔加仓

```mql
// 金字塔加仓示例
// 越涨越买，但每次加仓数量递减

MA10:MA(C,10);
MA20:MA(C,20);

// 初始开仓10手
T_COMMAND(10);
TRADE_AGAIN(5);  // 允许加仓5次

// 开仓条件
CROSS(MA10,MA20), BK;

// 金字塔加仓
// 盈利2%加仓4手
CLOSE>BKPRICE*(1+0.02), ADD_LONG(4);

// 盈利4%再加仓2手
CLOSE>BKPRICE*(1+0.04), ADD_LONG(2);

// 盈利6%再加仓1手
CLOSE>BKPRICE*(1+0.06), ADD_LONG(1);

// 平仓
CROSSDOWN(MA10,MA20), SP;

// 止损
CLOSE<BKPRICE*(1-0.03), SP;

AUTOFILTER;
```

---

## 五、完整分批策略

```mql
// ============================================
// 完整分批进出示例
// 开仓 → 加仓 → 减仓 → 分批平仓
// ============================================

// 参数
开仓手数:=5;
加仓盈利比例:=0.02;   // 盈利2%加仓
减仓亏损比例:=0.01;   // 亏损1%减仓
止盈比例:=0.08;       // 总体止盈8%

// 头寸管理
T_COMMAND(开仓手数);
TRADE_AGAIN(3);

// 均线
MA20:MA(C,20);
MA60:MA(C,60);

// ========== 开仓 ==========
CLOSE>MA20 && CLOSE>MA60, BK;    // 价格在长短均线上方买开

// ========== 加减仓 ==========
// 盈利2%且持仓不足15手时，加仓2手
CLOSE>BKPRICE*(1+加仓盈利比例) && BKVOL<15, ADD_LONG(2);

// 亏损1%且持仓大于5手时，减仓2手
CLOSE<BKPRICE*(1-减仓亏损比例) && BKVOL>5, LOWER_LONG(2);

// ========== 分批平仓 ==========
// 盈利5%平1/3
CLOSE>BKPRICE*(1+0.05), LOWER_LONG(开仓手数);

// 盈利8%平剩余全部
CLOSE>BKPRICE*(1+止盈比例), SP;

// ========== 止损 ==========
CLOSE<BKPRICE*(1-0.03), SP;

// ========== 均线平仓 ==========
CROSSDOWN(CLOSE,MA20), SP;

AUTOFILTER;
```
