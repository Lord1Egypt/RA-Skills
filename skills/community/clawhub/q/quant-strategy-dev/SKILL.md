---
name: quant-strategy-dev
description: 量化策略开发主技能。当用户说"开发量化策略"、"设计量化策略"、"写策略代码"、"量化策略开发"时自动触发。提供标准开发流程、代码规范、检查清单、代码模板。适用于量化策略项目的开发阶段。
---

# 量化策略开发技能

> 版本：1.0.0
> 适用项目：量化策略项目（A股、美股）

---

## 🎯 核心原则

### 原则1：回测引擎 = 实盘策略

**必须使用相同的代码逻辑！**

- ✅ 买入条件完全一致
- ✅ 卖出条件完全一致
- ✅ 价格假设完全一致
- ✅ 持仓管理完全一致

### 原则2：先验证，后实盘

**验证流程**：
```
策略开发 → QMT回测 → 小额实盘 → 正式运行
```

### 原则3：小步快跑

- 小资金测试（1-5万）
- 短时间观察（1-2周）
- 快速迭代修复

---

## 📋 标准开发流程

### 阶段1：策略设计

**输出**：
- [ ] 策略逻辑文档
- [ ] 买入条件（明确、可量化）
- [ ] 卖出条件（必须完整）
- [ ] 资金管理规则
- [ ] 风控规则

**检查清单**：
- [ ] 买入条件是否明确？
- [ ] 卖出条件是否完整？（信号过期、止损、止盈、趋势反转）
- [ ] 资金管理是否合理？（单只仓位、总仓位、资金限制）
- [ ] 风控是否完善？（止损、止盈、最大回撤）

---

### 阶段2：代码开发

**关键要求**：

#### 2.1 代码模板

```python
# 1. 全局状态对象
class GlobalState:
    pass
G = GlobalState()

# 2. 初始化
def init(ContextInfo):
    # 初始化全局状态
    G.waiting_list = []
    G.sent_orders = set()
    G.buy_prices = {}  # 记录买入价格
    
    # 设置股票池
    ContextInfo.set_universe(stock_list)

# 3. 买入逻辑
def handlebar(ContextInfo):
    # 检查waiting_list
    if check_waiting_orders(ContextInfo):
        return
    
    # 买入条件判断
    for stock in signals:
        if 买入条件:
            # ⚠️ 关键：passorder的prType参数
            passorder(23, 1101, accID, code, 14, -1, volume, ...)  # prType=14（对手价）
            
            # 记录已发送委托
            G.sent_orders.add(code)
            G.waiting_list.append(msg)

# 4. 卖出逻辑（完整）
def check_and_sell_positions(ContextInfo, ...):
    for stock in positions:
        # 1. 检查止损
        pnl_ratio = (current_price - buy_price) / buy_price
        if pnl_ratio <= -STOP_LOSS:
            卖出(f"stop_loss ({pnl_ratio*100:.2f}%)")
        
        # 2. 检查止盈
        elif pnl_ratio >= TAKE_PROFIT:
            卖出(f"take_profit ({pnl_ratio*100:.2f}%)")
        
        # 3. 检查信号过期
        elif stock_code not in signals:
            卖出("signal_expired")
        
        # 4. 趋势反转（可选）
        elif 趋势反转条件:
            卖出("trend_reversal")
```

**检查清单**：
- [ ] 是否有全局状态对象？
- [ ] 是否有waiting_list防重机制？
- [ ] passorder的prType参数是否正确？（14=对手价）
- [ ] 卖出条件是否完整？（止损+止盈+信号过期+趋势反转）
- [ ] 是否记录买入价格？

---

### 阶段3：代码测试（必须）

> ⚠️ **强制要求**：代码变更后，必须通过测试才能进入下一阶段

#### 3.1 测试用例模板

```python
# tests/test_xxx.py

import sys
sys.path.insert(0, '/path/to/project')

from module import function_to_test

print("=" * 60)
print("模块名称测试")
print("=" * 60)

# 测试1：正常流程
print("\n[测试1] 正常流程")
result = function_to_test(normal_input)
assert result == expected_output, "正常流程失败"
print("  ✅ 通过")

# 测试2：边界条件
print("\n[测试2] 边界条件")
result = function_to_test(edge_case_input)
assert result == edge_case_output, "边界条件失败"
print("  ✅ 通过")

# 测试3：异常情况
print("\n[测试3] 异常情况")
try:
    function_to_test(invalid_input)
    assert False, "应抛出异常"
except ValueError:
    print("  ✅ 通过")

print("\n" + "=" * 60)
print("✅ 所有测试通过！")
print("=" * 60)
```

#### 3.2 测试检查清单

| 测试类型 | 检查项 | 状态 |
|---------|--------|------|
| **功能测试** | 核心功能正常 | [ ] |
| **边界测试** | 空输入、满输入、临界值 | [ ] |
| **异常测试** | 错误输入、网络异常、数据缺失 | [ ] |
| **回归测试** | 历史功能未破坏 | [ ] |

**强制要求**：
- [ ] 每个核心模块有对应测试文件
- [ ] 所有测试通过才能提交代码

---

### 阶段4：回测验证

#### 4.1 回测参数设置

**必须和实盘一致**：
- [ ] 初始资金
- [ ] 单只仓位
- [ ] 最大持仓数
- [ ] 止损比例
- [ ] 止盈比例
- [ ] 手续费率
- [ ] 滑点设置

#### 4.2 回测检查清单

- [ ] 买入股票数量是否合理？
- [ ] 买入价格是否接近实际价格？
- [ ] 是否有异常买卖？（买入后立即卖出）
- [ ] 持仓时间是否合理？
- [ ] 收益表现是否符合预期？

---

### 阶段5：实盘准备

#### 5.1 代码审查关键点

```python
# 检查项1：买入和卖出的信号范围是否一致
# ❌ 错误
if stock_code not in signals[:10]:  # 卖出：检查前10只
    卖出
for stock in filtered_signals:  # 买入：从过滤后的信号买
    买入

# ✅ 正确
if stock_code not in signals:  # 卖出：检查整个信号列表
    卖出
for stock in filtered_signals:  # 买入：从过滤后的信号买
    买入

# 检查项2：passorder的prType参数
# ❌ 错误
passorder(23, 1101, accID, code, -1, ...)  # prType=-1（使用默认，偏高）

# ✅ 正确
passorder(23, 1101, accID, code, 14, ...)  # prType=14（对手价，滑点可控）
```

#### 5.2 风控设置

**必须设置**：
- [ ] 金额合规（限制资金上限）
- [ ] 反向单交易（禁止买入后立即卖出）
- [ ] 对敲单交易（禁止高买低卖）

#### 5.3 资金安全

**必须确认**：
- [ ] 代码硬编码资金限制
- [ ] QMT风控限制
- [ ] 双重保护

---

### 阶段6：小资金实盘

#### 6.1 资金规模

**建议**：**5000-10000元**

#### 6.2 监控要点

**开盘后前1分钟**：
- [ ] 策略启动正常
- [ ] 信号加载正常
- [ ] 数据获取正常
- [ ] 买入触发正常
- [ ] 委托确认正常
- [ ] 持仓更新正常

**观察期**：**1-2周**

---

## ⚠️ 关键教训

### 教训1：止损止盈逻辑缺失

**问题**：策略定义了止损止盈参数，但卖出逻辑中没有实现

**正确做法**：
```python
# ✅ 完整的卖出逻辑
def check_and_sell_positions(ContextInfo, ...):
    # 1. 检查止损
    pnl_ratio = (current_price - buy_price) / buy_price
    if pnl_ratio <= -STOP_LOSS:
        卖出(f"stop_loss")
    
    # 2. 检查止盈
    elif pnl_ratio >= TAKE_PROFIT:
        卖出(f"take_profit")
    
    # 3. 检查信号过期
    elif stock_code not in signals:
        卖出("signal_expired")
```

**教训**：
1. 定义的参数必须在代码中实现
2. 卖出条件必须完整：信号过期 + 止损 + 止盈
3. 必须记录买入价格

---

### 教训2：买入和卖出信号范围不一致

**问题**：卖出检查前10只，买入从过滤后的信号买

**正确做法**：
- 买入和卖出的信号范围必须一致
- 都检查整个信号列表

---

### 教训3：passorder的prType参数错误

**问题**：使用prType=-1，导致价格不可控

**正确做法**：
- 使用prType=14（对手价）
- 滑点可控

---

## 🚫 禁止事项

1. ❌ 回测引擎和实盘策略使用不同的代码逻辑
2. ❌ 买入和卖出的信号范围不一致
3. ❌ 使用prType=-1（价格不可控）
4. ❌ 没有waiting_list防重机制
5. ❌ 没有小资金测试直接大资金实盘
6. ❌ 没有止损止盈逻辑

---

## 📚 参考文档

- QMT官方示例（双均线实盘、竞价选股、行业轮动、多因子选股）
- QMT API文档
- QMT_STRATEGY_DEVELOPMENT_STANDARDS.md

---

## 🎯 成功标准

| 指标 | 标准 |
|------|------|
| 策略设计 | 买入/卖出条件明确完整 |
| 代码质量 | 有防重机制、止损止盈完整 |
| 测试通过 | 所有测试用例通过 |
| 回测验证 | 表现符合预期 |
| 实盘准备 | 风控设置完整 |

---

*技能版本：1.0.0*
*基于：QUANT_STRATEGY_DEVELOPMENT_STANDARD_PROCESS.md*
