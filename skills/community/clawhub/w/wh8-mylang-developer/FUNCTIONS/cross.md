# WT8跨周期跨合约

## 目录
1. [跨周期引用](#一跨周期引用)
2. [跨合约引用](#二跨合约引用)
3. [综合示例](#三综合示例)

---

## 一、跨周期引用

### 语法
```mql
#IMPORT[PERIOD, N, FORMULA] AS VAR
```
- PERIOD：被引用周期（MIN1/DAY/WEEK等）
- N：周期倍数
- FORMULA：被引用指标名称

### 周期参数

| 参数 | 含义 |
|------|------|
| MIN1 | 1分钟 |
| MIN5 | 5分钟 |
| MIN15 | 15分钟 |
| MIN30 | 30分钟 |
| HOUR | 1小时 |
| DAY | 日线 |
| WEEK | 周线 |

### 示例：引用日线数据

```mql
// 第一步：建立日线指标 AA
AA
MA5:MA(C,5);
MA30:MA(C,30);
DAYCON1:MA5>MA30;  // 日线多头
DAYCON2:MA5<MA30;  // 日线空头
```

```mql
// 第二步：在分钟周期引用日线数据
#IMPORT[DAY,1,AA] AS VAR1

DAYCON1:VAR1.DAYCON1;
DAYCON2:VAR1.DAYCON2;

// 分钟周期自己的条件
MINCON1:CROSS(MA(CLOSE,5),MA(CLOSE,10));  // 分钟金叉
MINCON2:CROSSDOWN(MA(CLOSE,5),MA(CLOSE,10));  // 分钟死叉

// 综合判断
DAYCON1 && MINCON1, BPK;  // 日线多头 + 分钟金叉 → 做多
DAYCON2 && MINCON2, SPK;  // 日线空头 + 分钟死叉 → 做空

AUTOFILTER;
```

### 示例：引用多周期

```mql
// 日线指标
#IMPORT[DAY,1,AA] AS VAR1
DAYMA:VAR1.MA5;

// 小时周期指标
#IMPORT[HOUR,2,AA] AS VAR2  
HOURMA:VAR2.MA5;

// 分钟MACD
DIFF:=EMA(CLOSE,12)-EMA(CLOSE,26);
DEA:=EMA(DIFF,9);
MINCON1:CROSS(DIFF,DEA);
MINCON2:CROSSDOWN(DIFF,DEA);

// 三周期共振
VAR1.DAYCON1 && VAR2.HOURCON1 && MINCON1, BPK;
VAR1.DAYCON2 && VAR2.HOURCON2 && MINCON2, SPK;

AUTOFILTER;
```

---

## 二、跨合约引用

### 语法
```mql
#CALL["CODE", FORMULA] AS VAR
```
- CODE：被引用合约代码
- FORMULA：被引用指标名称

### 示例：引用板块指数

```mql
// 第一步：建立黑链指数指标
HG
MA5:MA(C,5);
MA10:MA(C,10);
MA30:MA(C,30);
HGCON1:MA5>MA10 && MA10>MA30;  // 板块多头
HGCON2:MA5<MA10 && MA10<MA30;  // 板块空头
```

```mql
// 第二步：在螺纹合约引用黑链指数
#CALL[7161,HG] AS VAR

HGCON1:VAR.HGCON1;
HGCON2:VAR.HGCON2;

// 螺纹自己的均线
MA5:MA(C,5);
MA30:MA(C,30);
WGCON1:CROSS(MA5,MA30);     // 螺纹金叉
WGCON2:CROSSDOWN(MA5,MA30);  // 螺纹死叉

// 综合判断：板块 + 单合约同向
HGCON1 && WGCON1, BPK;  // 板块多头 + 螺纹多头 → 做多
HGCON2 && WGCON2, SPK;  // 板块空头 + 螺纹空头 → 做空

AUTOFILTER;
```

### 常用板块代码
| 代码 | 品种 |
|------|------|
| 7161 | 黑链指数 |
| 7162 | 有色指数 |
| 7163 | 化工指数 |
| 7164 | 农产品指数 |

---

## 三、综合示例

### 三周期趋势策略

```mql
// ============================================
// 第一部分：建立各周期指标
// ============================================

// 日线指标（保存为 DAY_MA）
DAY_MA
MA5:MA(C,5);
MA10:MA(C,10);
DAYUP:MA5>MA10;        // 日线多头
DAYDN:MA5<MA10;        // 日线空头
```

```mql
// 小时指标（保存为 HOUR_MA）
HOUR_MA
MID:MA(CLOSE,26);
TMP2:=STD(CLOSE,26);
TOP:MID+2*TMP2;        // 布林上轨
BOTTOM:MID-2*TMP2;     // 布林下轨
HOURUP:C>TOP;          // 小时多头（突破上轨）
HOURDN:C<BOTTOM;       // 小时空头（跌破下轨）
```

```mql
// ============================================
// 第二部分：跨周期策略（加载到分钟周期）
// ============================================

// 引用日线
#IMPORT[DAY,1,DAY_MA] AS D
DAYUP:D.DAYUP;
DAYDN:D.DAYDN;

// 引用小时
#IMPORT[HOUR,1,HOUR_MA] AS H
HOURUP:H.HOURUP;
HOURDN:H.HOURDN;

// 分钟条件
MINUP:CROSS(CLOSE,MA(C,5));
MINDN:CROSSDOWN(CLOSE,MA(C,5));

// 三周期共振做多
DAYUP && HOURUP && MINUP, BPK;

// 三周期共振做空
DAYDN && HOURDN && MINDN, SPK;

// 止损
CLOSE<=BKPRICE-15*MINPRICE, SP;
CLOSE>=SKPRICE+15*MINPRICE, BP;

AUTOFILTER;
```

### 板块对冲策略

```mql
// 引用黑色系板块
#CALL[7161,HG] AS VAR

// 螺纹钢
MA5:MA(C,5);
MA30:MA(C,30);
RBUP:MA5>MA30;
RBDN:MA5<MA30;

// 螺纹与板块共振
RBUP && VAR.HGCON1, BK;    // 螺纹多头 + 板块多头
RBDN && VAR.HGCON2, SK;     // 螺纹空头 + 板块空头

// 平仓
CLOSE<MA30 && BKVOL>0, SP;
CLOSE>MA30 && SKVOL>0, BP;

AUTOFILTER;
```

---

## 注意事项

1. **被引用指标需先建立**
   - 先建立被引用指标的公式
   - 保存时记住公式名称
   - 再编写引用该指标的模型

2. **指标不需要加载**
   - 跨周期/跨合约模型加载时
   - 只需要加载主模型
   - 被引用指标不需要加载

3. **变量访问语法**
   - `VAR.变量名` 访问被引用变量
   - 注意大小写一致
