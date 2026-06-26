# 社保公积金查询助手 🇨🇳

> 🏢 打工人必备工具 —— 一键查询社保公积金，轻松计算五险一金，精准估算退休金

[![ClawHub](https://img.shields.io/badge/ClawHub-social--security--fund-blue)](https://clawhub.ai/testmtcode/social-security-fund)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.ai/testmtcode/social-security-fund)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](https://clawhub.ai/testmtcode/social-security-fund)

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 📋 **社保查询** | 查询缴纳记录、缴费基数、账户余额 |
| 🏦 **公积金查询** | 查询余额、缴存记录、贷款额度估算 |
| 💰 **五险一金计算** | 计算个人/企业缴纳部分、实发工资 |
| 👴 **退休金估算** | 根据缴费年限估算每月养老金 |

---

## 🚀 快速开始

### 安装依赖

```bash
cd skills/social-security-fund
pip3 install -r requirements.txt
```

### 使用示例

```bash
# 五险一金计算（月薪 1 万，北京）
python3 scripts/check_deals.py calculate --salary 10000 --city 北京

# 社保查询指引（上海）
python3 scripts/check_deals.py social-security --city 上海 --guide

# 公积金查询指引（深圳）
python3 scripts/check_deals.py fund --city 深圳 --guide

# 退休金估算（缴费 25 年）
python3 scripts/check_deals.py pension --years 25 --avg-salary 8000
```

---

## 📊 输出示例

### 五险一金计算

```
💰 五险一金计算结果
━━━━━━━━━━━━━━━━
📍 城市：北京
💵 税前工资：¥10,000.00

👤 个人缴纳：¥2,250.00 (22.5%)
🏢 企业缴纳：¥3,970.00 (39.7%)

📋 实发工资：¥7,667.50
🏭 企业成本：¥13,970.00
```

### 退休金估算

```
👴 退休金估算结果
━━━━━━━━━━━━━━━━
📊 缴费年限：25 年
💰 每月养老金：¥4,321.94
📉 替代率：54.0%
```

---

## 🗺️ 支持城市

✅ 北京 · 上海 · 广州 · 深圳 · 杭州 · 成都

> 更多城市持续更新中...

---

## 📋 完整文档

详细使用说明请查看 [SKILL.md](SKILL.md)

---

## ⚠️ 说明

- 🔒 所有计算在本地完成，数据不出设备
- 📊 查询结果为模拟数据，实际数据请通过官方渠道查询
- 📈 费率数据参考 2024 年各地公布标准

---

## 📄 许可证

**MIT-0** - 自由使用、修改、分发，无需署名

---

**🎯 让社保公积金查询更简单！**
