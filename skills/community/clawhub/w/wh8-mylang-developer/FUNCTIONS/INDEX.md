# WT8麦语言函数索引

## 目录

1. [信号和指令 (signals.md)](signals.md) - BK, SK, BP, SP, ADD_LONG, LOWER_LONG 等
2. [技术指标 (indicators.md)](indicators.md) - MA, EMA, MACD,布林带等
3. [持仓资金管理 (position.md)](position.md) - MONEYTOT, BKVOL, SETDEALPERCENT 等
4. [回测函数 (backtest.md)](backtest.md) - AUTOFILTER, 历史回测相关
5. [优化函数 (optimization.md)](optimization.md) - 枚举、遗传、滚动调参
6. [跨周期跨合约 (cross.md)](cross.md) - #IMPORT, #CALL
7. [运行优化 (execution.md)](execution.md) - SIGCHECK, SETSIGPRICETYPE

---

## 按功能分类

### 价格数据变量
| 函数 | 说明 | 语法 |
|------|------|------|
| CLOSE | 当前收盘价 | `CLOSE` |
| OPEN | 当前开盘价 | `OPEN` |
| HIGH | 当前最高价 | `HIGH` |
| LOW | 当前最低价 | `LOW` |
| VOL | 成交量 | `VOL` |
| OI | 持仓量 | `OI` |
| REF(X,N) | N周期前的值 | `REF(CLOSE,5)` |
| MINPRICE | 最小变动价位 | `MINPRICE` |

### 技术指标函数
| 函数 | 说明 | 语法 |
|------|------|------|
| MA(X,N) | 简单移动平均 | `MA(CLOSE,20)` |
| EMA(X,N) | 指数移动平均 | `EMA(CLOSE,12)` |
| HHV(X,N) | N周期最高值 | `HHV(HIGH,10)` |
| LLV(X,N) | N周期最低值 | `LLV(LOW,10)` |
| CROSS(X,Y) | 上穿 | `CROSS(MA5,MA10)` |
| CROSSDOWN(X,Y) | 下穿 | `CROSSDOWN(MA5,MA10)` |

### 交易信号
| 函数 | 说明 | 语法 |
|------|------|------|
| BK | 买开 | `条件, BK;` |
| SK | 卖开 | `条件, SK;` |
| BP | 买平 | `条件, BP;` |
| SP | 卖平 | `条件, SP;` |
| BPK | 反手买 | `条件, BPK;` |
| SPK | 反手卖 | `条件, SPK;` |

### 加减仓指令
| 函数 | 说明 | 语法 |
|------|------|------|
| ADD_LONG(N) | 多头加仓N手 | `条件, ADD_LONG(2);` |
| LOWER_LONG(N) | 多头减仓N手 | `条件, LOWER_LONG(1);` |
| ADD_SHORT(N) | 空头加仓N手 | `条件, ADD_SHORT(2);` |
| LOWER_SHORT(N) | 空头减仓N手 | `条件, LOWER_SHORT(1);` |

### 价格获取
| 函数 | 说明 | 语法 |
|------|------|------|
| BKPRICE | 多头开仓价 | `CLOSE < BKPRICE - 10` |
| SKPRICE | 空头开仓价 | `CLOSE > SKPRICE + 10` |
| BKHIGH | 多头持仓期间最高价 | `CLOSE < BKHIGH - 20` |
| SKLOW | 空头持仓期间最低价 | `CLOSE > SKLOW + 20` |

### 持仓查询
| 函数 | 说明 | 语法 |
|------|------|------|
| BKVOL | 多头持仓手数 | `BKVOL > 0` |
| SKVOL | 空头持仓手数 | `SKVOL > 0` |
| VOL() | 总持仓手数 | `VOL() > 0` |

### 资金查询
| 函数 | 说明 | 语法 |
|------|------|------|
| MONEYTOT | 当前权益 | `MONEYTOT <= INITMONEY*0.9` |
| INITMONEY | 初始资金 | `INITMONEY + 10000` |
| BKVOL | 持仓手数 | `BKVOL > 0` |

### 头寸管理
| 函数 | 说明 | 语法 |
|------|------|------|
| SETDEALPERCENT(f,n) | 按资金比例下单 | `SETDEALPERCENT(20,10);` |
| T_COMMAND(N) | 设置开仓手数 | `T_COMMAND(5);` |
| TRADE_AGAIN(N) | 加减仓可连续N次 | `TRADE_AGAIN(3);` |

### 信号过滤
| 函数 | 说明 | 语法 |
|------|------|------|
| AUTOFILTER | 信号过滤 | `AUTOFILTER;` |

### 运行优化
| 函数 | 说明 | 语法 |
|------|------|------|
| SIGCHECK(M,T) | 信号复核 | `SIGCHECK('B',15);` |
| SIGCHECK_MIN(M,T) | 分钟级复核 | `SIGCHECK_MIN('A',5);` |

### 跨周期跨合约
| 函数 | 说明 | 语法 |
|------|------|------|
| #IMPORT | 跨周期引用 | `#IMPORT[DAY,1,AA]ASVAR1` |
| #CALL | 跨合约引用 | `#CALL["RB",AA]ASVAR` |

### 指定交易合约
| 函数 | 说明 | 语法 |
|------|------|------|
| TRADE_OTHER(X) | 指定交易合约 | `TRADE_OTHER('RB2410');` |
| TRADE_OTHER('ZHULIAN') | 主连自动换月 | `TRADE_OTHER('ZHULIAN');` |

---

## 快速查找

### 想实现这个功能？
| 功能 | 函数 |
|------|------|
| 均线金叉买开 | `CROSS(MA5,MA10), BK;` |
| 均线死叉卖平 | `CROSSDOWN(MA5,MA10), SP;` |
| 亏损N跳止损 | `CLOSE <= BKPRICE-N*MINPRICE, SP;` |
| 盈利M跳止盈 | `CLOSE >= BKPRICE+M*MINPRICE, SP;` |
| 权益回撤10%止损 | `MONEYTOT<=INITMONEY*(1-10/100), SP;` |
| 按资金20%下单 | `SETDEALPERCENT(20,10);` |
| 多头加仓两手 | `条件, ADD_LONG(2);` |
| 动态追踪止损 | `CLOSE <= BKHIGH-N*MINPRICE, SP;` |
| 引用日线数据 | `#IMPORT[DAY,1,AA]ASVAR1` |
| K线走完前15秒下单 | `SIGCHECK('B',15);` |
