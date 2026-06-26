# T+0 基金 5 分钟实时监控系统

## 快速开始

### 1. 添加基金到监控列表

```bash
# 批量添加（逗号或空格分隔）
~/.openclaw/skills/fund-monitor/tools/monitor.py add 512880,513050,159915

# 单个添加
~/.openclaw/skills/fund-monitor/tools/monitor.py add 512880
```

### 2. 查看监控列表

```bash
~/.openclaw/skills/fund-monitor/tools/monitor.py list
```

### 3. 启动监控

```bash
~/.openclaw/skills/fund-monitor/tools/monitor.py start
```

监控启动后：
- 每 5 分钟自动检查一次
- 只在交易时间运行（9:30-11:30, 13:00-15:00）
- 发现信号时会在终端显示并播放提示音

### 4. 查看最新信号

```bash
~/.openclaw/skills/fund-monitor/tools/monitor.py signals
```

### 5. 停止监控

```bash
# 按 Ctrl+C 停止
```

### 6. 移除基金

```bash
~/.openclaw/skills/fund-monitor/tools/monitor.py remove 512880
```

## 信号策略

### 买入信号（同时满足）
- ✅ MACD 金叉（DIF 上穿 DEA）
- ✅ KDJ < 20（超卖区）
- ✅ 成交量 > 5 日均量 1.5 倍

### 卖出信号（满足任一）
- 🔴 MACD 死叉（DIF 下穿 DEA）
- 🔴 KDJ > 80（超买区）
- 🔴 跌破 5 日均线 2%

## 配置通知（可选）

编辑 `~/.openclaw/skills/fund-monitor/config/default.yaml`：

### 钉钉通知
```yaml
notify:
  dingtalk:
    enabled: true
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
```

### 企业微信通知
```yaml
notify:
  wechat:
    enabled: true
    key: "YOUR_KEY"
```

## 支持的基金类型

| 类型 | 代码前缀 | 示例 |
|------|----------|------|
| 沪市 ETF | 51xxxx | 512880 (证券 ETF) |
| 深市 ETF | 15xxxx | 159915 (创业板 ETF) |
| 跨境 QDII | 513xxx | 513050 (纳指 ETF) |
| 债券 ETF | 511xxx | 511010 (国债 ETF) |

## 注意事项

⚠️ **重要提示**：
- 数据有 1-5 分钟延迟，不适合高频交易
- 信号仅供参考，不构成投资建议
- T+0 基金日内可多次交易，但需注意手续费
- 建议在交易时间前启动监控

## 文件说明

```
~/.openclaw/skills/fund-monitor/
├── tools/
│   ├── monitor.py      # 主程序（CLI 入口）
│   ├── data_fetch.py   # 数据获取
│   ├── indicators.py   # 指标计算
│   ├── signals.py      # 信号生成
│   └── notifier.py     # 通知推送
├── config/
│   └── default.yaml    # 配置文件
├── data/
│   ├── watchlist.json  # 监控列表
│   └── signals.json    # 历史信号
└── logs/
    └── monitor.log     # 运行日志
```

## 常见问题

**Q: 为什么没有信号？**
A: 当前市场可能不符合买入/卖出条件，这是正常的。策略设计为只在高置信度时发出信号。

**Q: 数据获取失败？**
A: 检查网络连接，或基金代码是否正确。

**Q: 如何调整信号阈值？**
A: 编辑 `config/default.yaml` 中的 `signals` 部分。
