# WT8麦语言语法格式规范（重要！）

> 📖 **官方文档参考**：
> - 操作符语法：https://www.wenhua.com.cn/guide/views41a.htm
> - 基本语法：https://www.wenhua.com.cn/guide/views41a3.htm

## ⚠️ 格式对比：错误 vs 正确

### ❌ 错误格式（Python/C风格）
```python
# 大括号、IF语句、函数定义
INIT {
    T_COMMAND(2);
    AUTOFILTER;
}

FUNCTION main() {
    IF (CLOSE > MA(C,10)) {
        BK;
    }
}
```

### ✅ 正确格式（麦语言）
```mql
# 无大括号、无IF语句、无函数定义
# 条件, 信号;  写在同一行

T_COMMAND(2);        # 设置开仓手数
AUTOFILTER;          # 必须写最后一行

MA10:=MA(C,10);      # 赋值用 :=

CLOSE>MA10, BK;     # 条件在前，信号在后，逗号分隔
```

---

## 运算符说明（最重要！）

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `:=` | **赋值**（定义变量） | `MA10:=MA(C,10);` |
| `=` | **比较**（等于判断） | `CLOSE=OPEN` |
| `<>` | **不等于** | `CLOSE<>OPEN` |
| `>` | 大于 | `CLOSE>MA10` |
| `<` | 小于 | `CLOSE<MA10` |
| `>=` | 大于等于 | `CLOSE>=MA10` |
| `<=` | 小于等于 | `CLOSE<=MA10` |
| `AND` | 逻辑与 | `CLOSE>MA AND CROSS` |
| `OR` | 逻辑或 | `CLOSE>MA OR CLOSE>MA2` |
| `NOT` | 逻辑非 | `NOT 多头` |

```mql
# ✅ 正确：赋值用 :=
MA10 := MA(C,10);
N := 20;
条件 := CROSS(MA5,MA10);

# ✅ 正确：比较用 =
CLOSE > MA10;         # 大于
CLOSE < MA10;         # 小于
CLOSE >= MA10;        # 大于等于
CLOSE <= MA10;        # 小于等于
CLOSE = OPEN;         # 等于（比较）
CLOSE <> OPEN;        # 不等于

# ✅ 逻辑运算
多头 AND CROSS(MA5,MA10);     # AND
空头 OR CROSS(MA10,MA20);     # OR
NOT 多头;                       # NOT

# ❌ 错误：混淆赋值和比较
MA10 = MA(C,10);      # 错！这是比较，不是赋值
```

---

## 麦语言核心语法

### 1. 指标定义
```mql
# ✅ 正确：变量名 := 指标函数(参数);
MA10 := MA(C,10);
MA20 := MA(C,20);
DIF := EMA(C,12) - EMA(C,26);

# ❌ 错误：使用 = 而不是 :=
MA10 = MA(C,10);    # 这是比较，不是赋值！
N = 20;              # 错！
```

### 2. 条件表达式
```mql
# ✅ 正确：直接写条件（用比较运算符）
CLOSE > MA10              # 价格大于均线
CLOSE < MA10              # 价格小于均线
BKVOL > 0                 # 有多头持仓
MONEYTOT < INITMONEY*0.9  # 权益回撤

# ✅ 多条件组合
多头 := MA5>MA20;
金叉 := CROSS(MA5,MA20);
多头 AND 金叉, BK;         # AND组合
```

### 3. 交易信号（最关键！）
```mql
# ✅ 正确格式：条件, 信号;
# 金叉买开
CROSS(MA5,MA10), BK;

# 死叉卖平
CROSSDOWN(MA5,MA10), SP;

# 止损
CLOSE <= BKPRICE-10*MINPRICE, SP;

# ❌ 错误格式：多种错误
IF (CLOSE > MA10) { BK; }        # 不能用IF
CLOSE > MA10 THEN BK;            # 不能用THEN
```

### 4. 变量引用
```mql
# ✅ 正确（全大写）
CLOSE       # 当前收盘价
OPEN        # 当前开盘价
HIGH        # 当前最高价
LOW         # 当前最低价
MINPRICE    # 最小变动价位
BKVOL       # 多头持仓手数
SKVOL       # 空头持仓手数
MONEYTOT    # 当前权益

# ❌ 错误
c            # 不能用小写
close        # 不能用小写
```

### 5. 函数参数
```mql
# ✅ 正确：MA(数据, 周期)
MA(C,10)           # 收盘价的10日均线
EMA(C,12)          # 12日指数均线
HHV(HIGH,20)       # 20周期最高价
LLV(LOW,20);       # 20周期最低价

# ❌ 错误：参数顺序或数量不对
MA(10,C)           # 参数顺序错误
```

### 6. 加减仓指令
```mql
# ✅ 正确：必须带手数
ADD_LONG(2);        # 加仓2手
LOWER_LONG(1);      # 减仓1手
ADD_SHORT(BKVOL/2); # 加仓一半持仓

# ❌ 错误：不带手数
ADD_LONG;           # 缺少手数！
```

---

## 完整示例对比

### ❌ 错误代码
```python
# 用户提供的错误代码
INIT {
    T_COMMAND(2);
    AUTOFILTER;
}

FUNCTION main() {
    CLOSE_S = MA(CLOSE, MA_SHORT, S);
    HOLONG = BKVOL;
    
    IF (CROSS(CLOSE_SHORT, MA_LONG, S) == 0) {
        BKPRICE;
    }
}
```

### ✅ 正确代码
```mql
# 麦语言正确格式
# 参数
MA_SHORT := 10;     # 赋值用 :=
MA_LONG := 20;
止损 := 15;

# 指标
MA_S := MA(C,MA_SHORT);
MA_L := MA(C,MA_LONG);

# 金叉买开
CROSS(MA_S,MA_L), BK;

# 死叉卖开
CROSSDOWN(MA_S,MA_L), SK;

# 止损
CLOSE <= BKPRICE-止损*MINPRICE, SP;
CLOSE >= SKPRICE+止损*MINPRICE, BP;

# 必须写最后一行
AUTOFILTER;
```

---

## 麦语言 vs 其他语言

| 特性 | 麦语言 | Python/C |
|------|--------|----------|
| 赋值运算符 | `:=` | `=` 或 `let` |
| 比较运算符 | `=` | `==` |
| 不等于 | `<>` | `!=` |
| 逻辑与 | `AND` | `and` 或 `&&` |
| 逻辑或 | `OR` | `or` 或 `\|\|` |
| 条件语句 | 无IF，直接写条件 | `if () {}` |
| 信号语法 | `条件,信号;` | 函数调用 |
| 函数定义 | 无FUNCTION | `def/function` |

---

## 快速检查清单

写完代码后检查：

- [ ] **赋值用 `:=` 而不是 `=`**？ (`N := 10;` 不是 `N = 10;`)
- [ ] **没有** `{}` 大括号？
- [ ] **没有** `IF ()` 语句？
- [ ] **没有** `FUNCTION main()` 定义？
- [ ] 条件都直接写在信号前面？
- [ ] 信号前有逗号？
- [ ] 加减仓带了手数？
- [ ] 写了 `AUTOFILTER;`？

---

## 正确的双均线策略

```mql
# ============================================
# 正确的双均线策略
# ============================================

# 参数（赋值用 :=）
N1 := 10;   # 短周期
N2 := 20;   # 长周期

# 指标计算（赋值用 :=）
MA_S := MA(C,N1);   # 短期均线
MA_L := MA(C,N2);   # 长期均线

# 开仓条件
金叉 := CROSS(MA_S,MA_L);      # 短上穿长
死叉 := CROSSDOWN(MA_S,MA_L);  # 短下穿长

# 交易信号（条件,信号;）
金叉, BK;      # 金叉买开
死叉, SP;      # 死叉卖平（多头持仓时）
金叉, SK;      # 金叉卖开
死叉, BP;      # 死叉买平（空头持仓时）

# 止损（比较用 =）
CLOSE <= BKPRICE-15*MINPRICE, SP;
CLOSE >= SKPRICE+15*MINPRICE, BP;

# 必须写最后一行
AUTOFILTER;
```
