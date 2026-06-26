# stock-pulse

> A股智能决策仪表盘 — 一条命令，看懂今天该买什么

数据源：[baostock](http://baostock.com/)（免费、稳定）｜AI 分析：由 OpenClaw 注入的大模型

---

## 功能

| 命令 | 说明 |
|------|------|
| `--stocks` | 今日买卖信号 + 精确点位（支持多只） |
| `--day` | 指定日期分时走势图（ASCII K线）+ AI 点评 |
| `--predict` | 月/年价格区间预测（蒙特卡洛 2000 次模拟） |
| `--should-buy` | 综合买入建议：技术面 + 预测 → 明确结论 |

---

## 安装

```bash
cd stock-pulse
pip install -r requirements.txt
```

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `LLM_API_KEY` | 大模型 API Key | ✅（OpenClaw 自动注入）|
| `LLM_BASE_URL` | 大模型 API 地址 | ✅（OpenClaw 自动注入）|
| `LLM_MODEL` | 大模型名称 | ✅（OpenClaw 自动注入）|
| `FEISHU_WEBHOOK_URL` | 飞书群机器人 Webhook | 推送用 |
| `WECHAT_WEBHOOK_URL` | 企业微信群机器人 Webhook | 推送用 |

---

## 使用

### 今日仪表盘

```bash
python handler.py --stocks "600519,300750,002594"
```

```
📊 2026-04-11 决策仪表盘

🟢 买入 | 贵州茅台 (600519)
  📌 缩量回踩MA5支撑，乖离率1.2%处于最佳买点
  💰 买入 1800 | 止损 1750 | 目标 1900
  ✅ 多头排列  ✅ 乖离安全  ✅ 量能配合

🟡 观望 | 宁德时代 (300750)
  📌 乖离率7.8%超过5%警戒线，等待回调
  ⚠️ 等待回调至 MA5 附近（约 245 元）

---
生成时间: 18:03 | 数据: baostock
```

### 单日走势

```bash
python handler.py --day 600519 --date 2026-04-10
```

### 月/年价格预测

```bash
python handler.py --predict 600519 --horizon month
python handler.py --predict 600519 --horizon year
```

```
🔮 贵州茅台(600519)  1个月价格预测

  当前价格: 1453.96 元
  蒙特卡洛模拟 2000 次（概率分布）:

     悲观(10%)  保守(25%)  中性(50%)  乐观(75%)  极乐(90%)
     1337.13   1394.47   1462.25   1526.29   1589.20
```

### 综合买入建议

```bash
python handler.py --should-buy 600519
```

---

## 内置交易理念

- **严禁追高**：乖离率 > 5% 自动标记危险信号
- **趋势优先**：MA5 > MA10 > MA20 多头排列才考虑买入
- **精确点位**：每个信号附带买入价、止损价、目标价

---

## 技术说明

- **数据**：baostock 日K + 5分钟K，免费稳定，覆盖沪深全部A股
- **预测**：对数正态随机游走，年化收益率 + 波动率基于近 250 个交易日
- **AI 分析**：标准 chat completions 接口，结构化 JSON 输出
- **依赖**：`baostock pandas requests`，轻量无外部服务依赖
