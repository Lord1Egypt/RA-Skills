# 命令速查表

## 基本格式

```bash
python stock_monitor.py <command> [args]
```

工作目录：`C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts`

---

## 行情查询

### 查询股票行情
```bash
python stock_monitor.py quote <code>
```
**示例：**
```bash
python stock_monitor.py quote 600900    # A股
python stock_monitor.py quote 00992      # 港股
```

### 查询大盘指数
```bash
python stock_monitor.py index
```

---

## 技术分析

### 分析股票技术指标
```bash
python stock_monitor.py analyze <code>
```
**示例：**
```bash
python stock_monitor.py analyze 600900
python stock_monitor.py analyze 00992
```

返回：MA、MACD、KDJ、RSI、BOLL、OBV、DMI、WR、支撑阻力、趋势强度

---

## 监控池管理

### 添加股票到监控池
```bash
python stock_monitor.py add <code>
```
**示例：**
```bash
python stock_monitor.py add 600900
```

### 从监控池移除
```bash
python stock_monitor.py remove <code>
```
**示例：**
```bash
python stock_monitor.py remove 600900
```

### 查看监控池列表
```bash
python stock_monitor.py list
```

### 监控所有股票（含技术指标）
```bash
python stock_monitor.py monitor
```

### 仅监控A股
```bash
python stock_monitor.py monitor-a
```

### 仅监控港股
```bash
python stock_monitor.py monitor-hk
```

---

## 综合报告

### 生成综合分析报告
```bash
python stock_monitor.py report [标签]
```
**示例：**
```bash
python stock_monitor.py report           # 生成完整报告
python stock_monitor.py report mytag     # 带标签
```

**报告内容：**
- 大盘指数概览（上证、深证、创业板、沪深300等）
- 市场情绪（资讯积极/消极评分）
- 持仓股详细分析（支撑阻力+趋势+指标+资讯+建议）
- 关注股分析
- 综合评级排序

### 仅生成A股报告
```bash
python stock_monitor.py report-a [标签]
```

### 仅生成港股报告
```bash
python stock_monitor.py report-hk [标签]
```

---

## 持仓管理

### 查看持仓列表
```bash
python stock_monitor.py position list
```

### 添加持仓
```bash
python stock_monitor.py position add <code> <quantity> <cost_price>
```
**示例：**
```bash
python stock_monitor.py position add 600900 6000 28.69
# 格式：position add 股票代码 数量 成本价
```

### 清除持仓
```bash
python stock_monitor.py position remove <code>
```
**示例：**
```bash
python stock_monitor.py position remove 600900
```

### 分析单只持仓
```bash
python stock_monitor.py position <code>
```
**示例：**
```bash
python stock_monitor.py position 600900
```

---

## 交易记录

### 记录买入
```bash
python stock_monitor.py trade buy <code> <quantity> <price>
```
**示例：**
```bash
python stock_monitor.py trade buy 600900 1000 28.50
# 格式：trade buy 股票代码 数量 价格
```

### 记录卖出
```bash
python stock_monitor.py trade sell <code> <quantity> <price>
```
**示例：**
```bash
python stock_monitor.py trade sell 600900 500 30.00
```

### 查看交易记录
```bash
python stock_monitor.py trades [code]
```
**示例：**
```bash
python stock_monitor.py trades              # 查看全部交易记录
python stock_monitor.py trades 600900        # 查看特定股票交易记录
```

---

## 资金流向

### 查看资金流向
```bash
python stock_capital.py <code>
```
**示例：**
```bash
python stock_capital.py 600900
```

**返回数据：**
- 主力净流入/净流出
- 超大单净流入/净流出
- 大单净流入/净流出
- 中单净流入/净流出
- 小单净流入/净流出

---

## 常用场景

### 场景1：每日开盘前检查
```bash
python stock_monitor.py index              # 查看大盘
python stock_monitor.py report             # 生成完整持仓报告
```

### 场景2：盘中监控
```bash
python stock_monitor.py monitor            # 监控所有股票
```

### 场景3：收盘后分析
```bash
python stock_monitor.py report             # 生成综合报告
```

### 场景4：新买入股票后记录
```bash
python stock_monitor.py position add <code> <quantity> <cost_price>
python stock_monitor.py add <code>          # 添加到监控池
```
