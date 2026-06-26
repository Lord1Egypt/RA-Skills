# WT8运行优化函数

## 目录
1. [SIGCHECK](#一sigcheck)
2. [SETSIGPRICETYPE](#二setsigpricetype)
3. [信号复核机制](#三信号复核机制)
4. [注意事项](#四注意事项)

---

## 一、SIGCHECK

### 作用
在K线还没走完但条件已满足时发出交易指令，不需要等K线走完。

### 语法
```mql
SIGCHECK(MODE, TIME)
SIGCHECK_MIN(MODE, TIME)  // 分钟级
```
- MODE：确认模式（'A'/'B'/'C'）
- TIME：秒/分钟数（0-30）

### MODE 参数

| 模式 | 说明 |
|------|------|
| 'A' | K线走完前TIME秒确认信号下单，K线走完复核 |
| 'B' | BK线走完前TIME秒确认信号下单，K线走完复核 |
| 'C' | 最后一根K线走完前TIME秒确认信号下单，K线走完复核 |

### TIME 参数
- 取值范围：0-30
- 含义：
  - 分钟周期：TIME表示分钟数
  - 日线等：TIME表示秒数

### 示例

```mql
// K线走完前15秒下单，K线走完复核
SIGCHECK('B', 15);

// 均线策略
MA5:MA(C,5);
MA10:MA(C,10);
CROSS(MA5,MA10), BK;
CROSSDOWN(MA5,MA10), SP;

AUTOFILTER;
```

### 效果对比

| 方式 | 入场时机 | 成本 |
|------|----------|------|
| 默认 | 下一根K线开盘价 | 较高 |
| SIGCHECK | 条件满足时（更优价格） | 较低 |

---

## 二、SETSIGPRICETYPE

### 作用
设置信号的下单价格方式，提高成交率。

### 语法
```mql
SETSIGPRICETYPE(信号类型, 价格类型)
```

### 信号类型

| 类型 | 说明 |
|------|------|
| BK | 买开 |
| SK | 卖开 |
| BP | 买平 |
| SP | 卖平 |
| ADD_LONG | 多头加仓 |
| LOWER_LONG | 多头减仓 |
| ADD_SHORT | 空头加仓 |
| LOWER_SHORT | 空头减仓 |

### 价格类型

| 类型 | 说明 |
|------|------|
| 0 | 最新价 |
| 1 | 排队价（挂单价） |
| 2 | 对手价 |
| 3 | 超价 |
| 4 | 市价 |
| 5 | 触发价 |

### 示例

```mql
// 设置止损信号立即成交
SETSIGPRICETYPE(SP, 4);   // 止损用市价
SETSIGPRICETYPE(BP, 4);   // 止损用市价

// 设置开仓用对手价
SETSIGPRICETYPE(BK, 2);
SETSIGPRICETYPE(SK, 2);

// 均线策略
MA10:MA(C,10);
CROSS(CLOSE,MA10), BK;
CROSSDOWN(CLOSE,MA10), SK;

// 止损
CLOSE <= BKPRICE-10*MINPRICE, SP;
CLOSE >= SKPRICE+10*MINPRICE, BP;

AUTOFILTER;
```

---

## 三、信号复核机制

### 什么是信号消失（忽闪）
```
K线走完前：条件满足 → 出信号 → K线走完 → 条件不再满足 → 信号消失
```

### 信号复核的作用
- 消失的信号会被恢复持仓
- 保证交易策略完整执行

### 复核处理方式

| 信号消失 | 处理方式 |
|----------|----------|
| BK/SK消失 | 平仓 |
| ADD_LONG/ADD_SHORT消失 | 平仓 |
| BPK/SPK消失 | 平仓+恢复建仓 |
| BP/SP消失 | 恢复建仓 |
| LOWER_LONG/LOWER_SHORT消失 | 恢复建仓 |

### 示例

```mql
// K线走完前出信号就下单，K线走完复核
SIGCHECK('A', 0);

// 策略条件
MA10:MA(C,10);
MA20:MA(C,20);

// 条件严格，可能忽闪
条件A:=CROSS(MA10,MA20) AND VOL>1000;
条件B:=CROSSDOWN(MA10,MA20);

条件A, BK;
条件B, SK;

AUTOFILTER;
```

---

## 四、注意事项

### 适用场景
- 短线策略：需要精确入场点
- 突破策略：需要快速反应

### 不适用场景
- 长线策略：K线走完前出信号意义不大
- 依赖运行优化才能盈利的策略：可能过度优化

### 与页面盒子的关系
| 函数 | 页面盒子支持 |
|------|--------------|
| SIGCHECK | ❌ 不支持 |
| SETSIGPRICETYPE | ❌ 不支持 |

### 回测说明
- 回测报告仍用收盘价计算
- 运行优化收益差单独显示
- 信号明细提供对比参考

### 使用建议

1. **短线策略推荐使用**
   - 入场时机影响大
   - 滑点成本占比高

2. **长线策略谨慎使用**
   - 对结果影响不大
   - 可能干扰策略研究

3. **配合SETSIGPRICETYPE**
   - 止损用市价确保成交
   - 开仓用对手价降低成本

---

## 完整示例

```mql
// ============================================
// 运行优化示例：短线突破策略
// ============================================

// K线走完前15秒确认信号
SIGCHECK('B', 15);

// 设置下单价格
SETSIGPRICETYPE(BK, 2);   // 开仓用对手价
SETSIGPRICETYPE(SP, 4);   // 止损用市价
SETSIGPRICETYPE(SK, 2);
SETSIGPRICETYPE(BP, 4);

// 参数
N:=20;  // 止损跳数
M:=30;  // 止盈跳数

// 突破策略
HH20:=HHV(HIGH,20);
LL20:=LLV(LOW,20);

// 突破20日高点买开
CLOSE>HH20, BK;

// 跌破20日低点卖开
CLOSE<LL20, SK;

// 止损止盈
CLOSE<=BKPRICE-N*MINPRICE, SP;     // 亏损N跳止损
CLOSE>=BKPRICE+M*MINPRICE, SP;     // 盈利M跳止盈
CLOSE>=SKPRICE+N*MINPRICE, BP;
CLOSE<=SKPRICE-M*MINPRICE, BP;

AUTOFILTER;
```
