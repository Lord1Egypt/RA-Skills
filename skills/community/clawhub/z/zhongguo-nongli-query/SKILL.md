---
name: zhongguo-nongli-query
license: MIT
homepage: https://nongli.skill.4glz.com
repository: https://github.com/Leocdchina/huangli-agent-skills
publisher: Leocdchina
version: 1.0.2
compatibility: Requires Python 3.9+ or bash with curl. Set required HUANGLI_TOKEN env var (Bearer token from https://nongli.skill.4glz.com/dashboard). Optional HUANGLI_BASE env var overrides API base. Needs HTTPS outbound access to api.nongli.skill.4glz.com.
required_env:
  - HUANGLI_TOKEN (required)
  - HUANGLI_BASE (optional)
outbound_hosts:
  - api.nongli.skill.4glz.com
description: |
  中国农历日期换算工具。专注公历转农历、阴历日期换算、农历年月日、生肖、干支查询。适合已明确要做日期换算的场景；若还要查黄历宜忌、吉凶判断、择日，请优先使用 zhongguo-nongli-huangli-jixiong 统一技能。
---

# 中国农历日期换算 / 公历转农历

这是一个 **更窄的日期换算技能**，重点是：

- 公历转农历
- 阴历日期换算
- 农历年月日
- 生肖、干支

它**不是**主要面向黄历宜忌或吉凶择日的统一入口。
如果用户要查：

- 今日黄历
- 黄历宜忌
- 吉凶判断
- 搬家 / 结婚 / 开业 / 开工择日

请优先使用：`zhongguo-nongli-huangli-jixiong`

## 适用问题

- 2027-08-08 对应的农历日期是什么？
- 某个公历日期换算成中国农历是多少？
- 某一天的农历年月日、生肖、干支是什么？

## 使用方式

```bash
# 1）查询单日农历日期换算
python3 toolkit.py by-date 2027-08-08

# 2）批量查询一个时间段内的农历日期
python3 toolkit.py batch 2027-08-01 2027-08-31

# 3）按关键词检索特殊日期
python3 toolkit.py search 甲子日 --year 2027
```

## 触发词建议

- 公历转农历
- 农历日期换算
- 阴历日期换算
- 中国农历日期
- 生肖干支查询

## 环境变量

```bash
export HUANGLI_TOKEN="***"
export HUANGLI_BASE="https://api.nongli.skill.4glz.com"
```

Token 获取地址：

- https://nongli.skill.4glz.com/dashboard
