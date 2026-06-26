---
name: pre-market-briefing
description: |
  纯离线的股市数据分析教学系统，无网络调用，仅使用模拟数据演示OpenClaw开发技术。
  适合学习AI Agent开发、量化策略实现。
alwaysActive: false
---

# OpenClaw 股市数据分析教学版

## 概述

这是一个**100%纯离线**的股市数据分析系统，专为OpenClaw开发者设计，提供：

- 📊 **模拟大盘分析** - 无API的指数演示
- 💰 **模拟板块流向** - 教学用资金流向模型
- 🎯 **技术指标计算** - 支撑/压力/止损算法
- 🚀 **选股策略示例** - 5种策略代码结构
- 📁 **本地日志系统** - 无网络的文件存储

**核心特点**：
- ✅ 零网络调用（不访问任何外部API）
- ✅ 纯模拟数据（random模块生成）
- ✅ 无敏感信息（无API密钥、无用户数据）
- ✅ 教学导向（完整代码，易于学习）

---

## 快速开始

### 1. 安装

```bash
# 复制skill文件夹到OpenClaw工作区
cp -r skill/* ~/.openclaw/workspace/
```

### 2. 运行

```bash
cd ~/.openclaw/workspace
python3 scripts/pre_market_briefing_public.py
```

### 3. 定时任务（可选）

```bash
crontab -e
```

```
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/pre_market_briefing_public.py
```

---

## 功能详解

### 数据生成（模拟）

```python
# 模拟股票数据
data = {
    'code': '000001',
    'name': '平安银行',
    'close': round(base_price * (1 + change_pct/100), 2),
    'change_pct': round(random.uniform(-5, 5), 2)
}
```

### 技术分析算法

```python
support = close * 0.985
resistance = close * 1.015
stop_loss = min(cost * 0.92, support * 0.98)
```

### 选股策略结构

系统包含5种策略的完整实现：
- `high_roe_quality()` - 高ROE筛选
- `low_pe_rotation()` - 低PE轮动
- `momentum_breakout()` - 动量突破
- `sector_fund_inflow()` - 板块资金流向
- `fadt_style()` - 分析师预期

---

## 配置说明

`config.example.json` 示例：

```json
{
  "holdings": [
    {"code": "000001", "name": "平安银行", "shares": 1000, "cost_price": 10.0}
  ],
  "user_open_id": "ou_xxxxxxxxxxxxx",
  "push_channel": "console"
}
```

**注意**：本版本**无飞书推送功能**，仅输出到控制台和本地日志。

---

## 安全与合规

- ✅ **完全离线**：无网络请求，无外部依赖
- ✅ **无数据收集**：不读取、不传输任何真实数据
- ✅ **无密钥管理**：配置文件中无API密钥
- ✅ **可审计**：所有代码开源，逻辑透明
- ✅ **教学用途**：明确标注模拟数据，不误导

---

## 学习价值

本系统展示了：
1. OpenClaw脚本结构
2. 配置管理最佳实践
3. 技术指标计算方法
4. 选股策略的代码实现
5. 日志持久化方案
6. 模块化设计

适合作为：
- OpenClaw入门教程
- 量化策略开发模板
- AI Agent实战案例

---

## 重要声明

- 本软件**仅供学习研究**
- **不构成投资建议**
- **不提供真实数据**
- **不保证代码适合生产环境**

---

## License

MIT License - 详见LICENSE文件

---

**欢迎学习和交流！** 🚀