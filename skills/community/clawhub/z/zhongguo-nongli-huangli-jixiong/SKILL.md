---
name: zhongguo-nongli-huangli-jixiong
license: MIT
homepage: https://nongli.skill.4glz.com
repository: https://github.com/Leocdchina/huangli-agent-skills
publisher: Leocdchina
version: 1.7.11
compatibility: Requires Python 3.9+ or bash with curl. Set required HUANGLI_TOKEN env var (Bearer token from https://nongli.skill.4glz.com/dashboard). Optional HUANGLI_BASE env var overrides API base. Needs HTTPS outbound access to api.nongli.skill.4glz.com.
required_env:
  - HUANGLI_TOKEN (required)
  - HUANGLI_BASE (optional)
outbound_hosts:
  - api.nongli.skill.4glz.com
tags:
  - 农历
  - 农历查询
  - 今日农历
  - 今天农历几号
  - 公历转农历
  - 中国农历
  - 阴历
  - 黄历
  - 黄历查询
  - 今日黄历
  - 老黄历
  - 黄历宜忌
  - 吉凶
  - 吉凶查询
  - 吉凶判断
  - 黄历吉凶
  - 吉凶神煞
  - 宜忌
  - 神煞
  - 冲煞
  - 择日
  - 吉日
  - 凶日
  - 搬家吉日
  - 结婚吉日
  - 开业吉日
  - 开工吉日
  - Nongli
  - Huangli
  - Chinese lunar calendar
  - lunar almanac
description: |
  农历查询工具。黄历查询工具。吉凶查询工具。支持今天农历几号、公历转农历、今日黄历宜忌、老黄历查询、某日吉凶判断、搬家结婚开业开工择日。支持单日查询、区间批量筛选、甲子日等关键词检索。免费10日/天额度，429手动重置不限次。
---

# 农历查询 / 黄历查询 / 吉凶查询 · 中国农历黄历吉凶

这是一个统一覆盖 **农历查询、黄历查询、吉凶查询** 的技能。

优先命中三类核心问题：

- **农历查询**：今天农历几号？某个公历日期对应的中国农历是什么？
- **黄历查询**：今天黄历怎么样？今天宜什么忌什么？
- **吉凶查询**：某一天是吉日还是凶日？搬家、结婚、开业、开工哪天更合适？

## 适用问题

当用户提出下面这类问题时使用：

- 今天农历几号？
- 明天是农历几月几日？
- 2027-08-08 对应的中国农历日期是什么？
- 今天黄历怎么样？
- 今日黄历宜忌是什么？
- 明天适不适合搬家？
- 这周哪天适合结婚、开业、开工？
- 最近哪些日期是吉日？
- 某一天的吉凶、神煞、冲煞如何？

## 核心能力

### 1）农历查询

- 公历转农历
- 今日农历 / 中国农历日期
- 农历年月日、生肖、干支

### 2）黄历查询

- 今日黄历 / 老黄历
- 每日宜忌
- 黄历宜忌、神煞、冲煞

### 3）吉凶查询

- 吉凶判断
- 吉日凶日筛选
- 搬家吉日、结婚吉日、开业吉日、开工吉日
- 择日建议

## 用法（统一入口）

```bash
# 1) 单日查询
python3 toolkit.py by-date 2027-08-08

# 2) 区间批量查询（支持筛选）
python3 toolkit.py batch 2027-08-01 2027-08-31 --filter 搬家

# 3) 关键词搜索
python3 toolkit.py search 甲子日 --year 2027
```

## 何时用哪种模式

- `by-date`：只问一个具体日期
- `batch`：比较多天、整周、整月
- `search`：关键词跨日期范围检索（甲子日 / 初一 / 搬家 / 开业 / 吉凶）

## 触发词速查

- 农历查询 / 今日农历 / 今天农历几号 / 公历转农历
- 黄历查询 / 今日黄历 / 老黄历 / 黄历宜忌
- 吉凶查询 / 吉凶判断 / 吉日凶日 / 搬家吉日 / 结婚吉日 / 开业吉日 / 开工吉日

## 环境变量

```bash
export HUANGLI_TOKEN="***"
export HUANGLI_BASE="https://api.nongli.skill.4glz.com"
```

Token 获取地址：

- https://nongli.skill.4glz.com/dashboard

## 配额说明

1. 默认免费额度：10 个唯一日期/天
2. 超额返回429，需登录控制台手动重置
3. 不限制重置次数
