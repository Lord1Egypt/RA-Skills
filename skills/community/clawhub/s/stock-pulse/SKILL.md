---
name: stock-pulse
version: 1.2.0
description: "A股智能决策仪表盘：一条命令看今日该买卖什么。输入股票代码，AI分析技术面+筹码，输出买/卖/观望信号和精确点位、单日走势图、月/年价格预测（蒙特卡洛）、综合买入建议。当用户想分析股票、看走势、预测价格、生成选股建议时触发。"
metadata:
  requires:
    bins: ["python3"]
    pip: ["baostock", "pandas", "requests"]
  env:
    - name: LLM_API_KEY
      description: "大模型 API Key（OpenClaw 自动注入）"
      required: true
    - name: LLM_BASE_URL
      description: "大模型 API 地址（OpenClaw 自动注入）"
      required: true
    - name: LLM_MODEL
      description: "大模型名称（OpenClaw 自动注入）"
      required: true
---

# stock-pulse

**一条命令，看懂今天该买什么。**

数据源：[baostock](http://baostock.com/)（免费、稳定）｜AI 分析：由 OpenClaw 注入的大模型

## 快速开始

```bash
cd /path/to/stock-pulse
pip install -r requirements.txt
python handler.py --stocks "600519,300750"
```

> OpenClaw 会自动注入 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，无需手动配置。

## 命令

```bash
# 今日买卖信号（支持多只）
python handler.py --stocks "600519,300750,002594"

# 某天分时走势 + AI 点评
python handler.py --day 600519 --date 2026-04-10

# 月/年价格预测（蒙特卡洛 2000 次模拟）
python handler.py --predict 600519 --horizon month
python handler.py --predict 600519 --horizon year

# 综合买入建议（技术面 + 预测 → 明确结论）
python handler.py --should-buy 600519

# 推送到飞书
python handler.py --stocks "600519" --push feishu
```

## 输出示例

### 今日仪表盘
```
📊 2026-04-11 决策仪表盘

🟢 买入 | 贵州茅台 (600519)
  📌 缩量回踩MA5支撑，乖离率1.2%处于最佳买点
  💰 买入 1800 | 止损 1750 | 目标 1900
  ✅ 多头排列  ✅ 乖离安全  ✅ 量能配合

🟡 观望 | 宁德时代 (300750)
  📌 乖离率7.8%超过5%警戒线，等待回调
  ⚠️ 等待回调至 MA5 附近（约 245 元）
```

### 月度预测
```
🔮 贵州茅台(600519)  1个月价格预测

  当前价格: 1453.96 元
  蒙特卡洛模拟 2000 次（概率分布）:

     悲观(10%)  保守(25%)  中性(50%)  乐观(75%)  极乐(90%)
     1337.13   1394.47   1462.25   1526.29   1589.20
```

### 综合建议
```
🎯 贵州茅台(600519)  该不该买？

  当前价: 1453.96  1个月预期: 1464.54(+0.7%)  1年预期: 1500.94(+3.2%)

  结论: 观望
  买入价区间: 1400-1420元 | 仓位: 10-20% | 止损: 1350元
```

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `LLM_API_KEY` | 大模型 API Key | ✅（OpenClaw 自动注入）|
| `LLM_BASE_URL` | 大模型 API 地址 | ✅（OpenClaw 自动注入）|
| `LLM_MODEL` | 大模型名称 | ✅（OpenClaw 自动注入）|
| `FEISHU_WEBHOOK_URL` | 飞书群机器人 Webhook | 推送用 |
| `WECHAT_WEBHOOK_URL` | 企业微信群机器人 Webhook | 推送用 |

## 交易理念（内置）

- **严禁追高**：乖离率 > 5% 自动标记危险信号
- **趋势优先**：MA5 > MA10 > MA20 多头排列才考虑买入
- **精确点位**：每个信号附带买入价、止损价、目标价
- **量能验证**：放量突破更可信，缩量回踩是买点
