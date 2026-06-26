---
name: qmt-dev
description: QMT平台开发专用技能。当用户说"QMT"、"实盘"、"QMT策略"、"QMT回测"、"QMT开发"时自动触发。提供QMT API规范、核心函数机制、止损监控方式、实盘注意事项。适用于使用QMT平台的量化策略开发。
---

# QMT平台开发技能

> 版本：1.0.0
> 适用平台：迅投QMT量化交易平台

---

## 🎯 核心函数机制

### 1. QMT标准函数

| 函数 | 用途 | 触发时机 | 说明 |
|------|------|---------|------|
| `init()` | 初始化 | 策略启动时 | 加载信号、设置参数、设置股票池 |
| `handlebar()` | K线处理 | **每根K线** | 主要逻辑，买入/卖出/止损 |

---

### 2. ⚠️ 重要：is_last_bar() 机制

| 场景 | is_last_bar() 返回值 | 止损检查 |
|------|---------------------|---------|
| **回测** | 每根K线都返回True | ✅ 每天检查 |
| **实盘** | 只在特定时刻返回True | ❌ 盘中可能不检查 |

**关键理解**：
- 回测时，每根K线都是"最后一根"，所以`is_last_bar()`都返回True
- 实盘时，`is_last_bar()`只在特定时刻返回True（可能是收盘时）

**结论**：
- ❌ 不要用`is_last_bar()`控制止损/止盈检查
- ✅ 用时间判断控制检查频率

---

## 📋 止损监控方式

### 方式1：时间判断（推荐）

```python
def handlebar(ContextInfo):
    """每根K线都会触发"""
    
    # 止损监控（每5分钟检查一次）
    now = datetime.now()
    if G.last_check_time:
        elapsed = (now - G.last_check_time).total_seconds() / 60
        if elapsed >= 5:  # 每5分钟检查
            check_stop_loss(ContextInfo)
            G.last_check_time = now
    
    # 买入逻辑（可以保留is_last_bar()限制）
    if not ContextInfo.is_last_bar():
        return
    
    # 买入逻辑...
```

### 方式2：bar_count判断

```python
def handlebar(ContextInfo):
    """每根K线都会触发"""
    
    # 每5根K线检查一次止损
    if ContextInfo.bar_count % 5 == 0:
        check_stop_loss(ContextInfo)
```

---

## 🚀 代码模板

### 完整策略模板

```python
# 全局状态对象
class GlobalState:
    pass
G = GlobalState()

def init(ContextInfo):
    """初始化"""
    # 全局状态
    G.waiting_list = []
    G.sent_orders = set()
    G.buy_prices = {}  # 记录买入价格
    G.last_check_time = None
    
    # 加载信号
    with open('trading_signals/alphagbm_signals_qmt.json') as f:
        data = json.load(f)
    G.signals = [s['code'] for s in data['signals']]
    
    # 设置股票池
    ContextInfo.set_universe(G.signals)

def handlebar(ContextInfo):
    """每根K线触发"""
    
    # 1. 止损监控（每5分钟）
    now = datetime.now()
    if G.last_check_time:
        elapsed = (now - G.last_check_time).total_seconds() / 60
        if elapsed >= 5:
            check_stop_loss(ContextInfo)
            G.last_check_time = now
    
    # 2. 检查waiting_list
    if check_waiting_orders(ContextInfo):
        return
    
    # 3. 买入逻辑（只在最后一根K线）
    if not ContextInfo.is_last_bar():
        return
    
    # 买入...
```

---

## ⚠️ 实盘注意事项

### 1. passorder的prType参数

```python
# ❌ 错误
passorder(23, 1101, accID, code, -1, ...)  # prType=-1（价格不可控）

# ✅ 正确
passorder(23, 1101, accID, code, 14, ...)  # prType=14（对手价）
```

---

### 2. waiting_list防重机制

```python
# 初始化
G.waiting_list = []
G.sent_orders = set()

# 买入时记录
if code not in G.sent_orders:
    passorder(...)
    G.sent_orders.add(code)
    G.waiting_list.append(msg)

# 检查waiting_list
def check_waiting_orders(ContextInfo):
    for msg in G.waiting_list[:]:
        order_result = get_trade_detail_data(...)
        if order_result:
            G.waiting_list.remove(msg)
```

---

### 3. 风控设置

**QMT层面**：
- [ ] 金额合规（限制资金上限）
- [ ] 反向单交易（禁止买入后立即卖出）
- [ ] 对敲单交易（禁止高买低卖）

**代码层面**：
- [ ] 硬编码资金限制
- [ ] 止损止盈逻辑
- [ ] 异常处理

---

## 🚫 禁止事项

1. ❌ 使用`is_last_bar()`控制止损检查
2. ❌ 使用prType=-1
3. ❌ 没有waiting_list防重机制
4. ❌ 没有止损止盈逻辑

---

## 📚 参考文档

- QMT官方示例（双均线实盘、竞价选股、行业轮动、多因子选股）
- QMT API文档
- QMT_STRATEGY_DEVELOPMENT_STANDARDS.md

---

*技能版本：1.0.0*
