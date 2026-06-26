---
name: waquanquaner
display-name: "挖券券儿"
version: 1.0.3
description: "外卖红包优惠券领券神器，一个链接领美团/饿了么/京东外卖全部隐藏优惠，无需注册无需API Key"
author: WaQuanquaner
homepage: https://waquanquaner.cn
argument-hint: "[平台(美团/饿了么/京东)]"
allowed-tools: Bash(curl https://waquanquaner.cn/*) PowerShell(Invoke-WebRequest https://waquanquaner.cn/*) Node(node scripts/query.js)
emoji: 🧧
category: 生活工具
tags: [外卖, 红包, 优惠券, 领券, 省钱, 美团, 饿了么, 京东, 外卖红包, 外卖优惠券, 满减, 折扣, 挖券券儿]
---

# 🧧 挖券券儿 — 一个链接挖取当日所有隐藏外卖红包

实时挖掘美团、饿了么、京东三大外卖平台的隐藏红包和优惠券活动。**一个链接搞定，无需注册、无需 API Key、装完即用。**

## 适用场景

- 每天点外卖前想找红包省钱
- 想知道今天哪个平台有隐藏大额红包
- 朋友问"今天吃什么"时顺便领个券
- 想一次性领取所有平台优惠，不想逐个 App 翻找
- 想领外卖优惠券、满减红包、首单优惠
- 找美团外卖红包、饿了么红包、京东外卖优惠券

## 使用

**方式一：curl 直接查询**（推荐，所有平台通用）
```bash
curl -s "https://waquanquaner.cn/api/v1/activities/channel/skill_compact"
```

**方式二：Node.js 格式化输出**
```bash
node scripts/query.js
```

**方式三：指定渲染格式**
```bash
node scripts/query.js --feishu   # 飞书消息卡片
node scripts/query.js --text     # 纯文本
```

## 输出示例

```
🧧 今日外卖隐藏红包已挖出！（4月10日）

🔗 一键领全部红包：
   https://waquanquaner.cn/go

👆 一个链接，挖取当日所有隐藏活动

💡 今日必领：
   🔵 饿了么·红包节天天领（今日主角）
      → 周末大餐红包提前抢，晚上就能用
   🔵 饿了么·大额红包限时领（热门推荐）
      → 领券下单立减，无门槛叠加用

💬 听说今天有人用红包点了一顿霸王餐

复制到微信打开 → 一个个领 → 再点餐
```

## 触发关键词

外卖红包、外卖优惠券、外卖优惠、饿了么红包、美团红包、点外卖省钱、外卖券、领券、领红包、今天吃什么、点外卖、美团外卖、饿了么外卖、京东外卖、外卖神券、满减红包、首单优惠、外卖折扣、挖券券、挖券券儿

## 特性

- **零门槛**：无需 API Key、无需注册、装完即用
- **一个链接搞定**：不用逐个找，打开就能全部领
- **三大平台全覆盖**：美团、饿了么、京东外卖
- **隐藏红包挖掘**：限时活动 App 里找不到的，这里有
- **多格式输出**：微信文本 / 飞书消息卡片 / 纯文本
- **隐私安全**：不收集个人信息，无密钥存储

## 更新说明

- v1.0.3: 优化显示名称为中文"挖券券儿"，规范 SKILL.md 格式
- v1.0.2: 极简聚焦模式，一个链接挖取当日所有隐藏活动
- v1.0.1: 首次发布