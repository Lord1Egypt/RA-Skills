---
name: xungu-huangli
displayName: "循古老黄历 · 万年历、农历、每日宜忌与吉时"
description: "查今天或指定公历日期的中国老黄历、万年历，获取农历、干支、宜忌、吉时、冲煞、月相和当日节气。适用于「今天宜做什么」「明天有什么吉时」「这天农历几号」等历法和择日查询。Chinese almanac (Huangli / Tung Shing), lunar calendar and auspicious hours."
metadata: {"openclaw":{"requires":{"env":["HUANGLI_API_TOKEN"],"bins":["python3"]},"primaryEnv":"HUANGLI_API_TOKEN"}}
---

# 循古老黄历

查询指定公历日的历法与宜忌。用户要看个人八字或出生资料对应的今日运势时，使用独立技能 xungu-query。

**调用**　运行 `python3 "{baseDir}/scripts/huangli.py"`。查询今天时省略日期，让服务器选择北京时间当天。指定日期放在命令末尾，如 `2026-11-20`；遇到“明天”“下周三”，先按北京时间换算为公历日期。只传经过校验的 YYYY-MM-DD。

客户端向 `https://www.xungufa.com/huangli/api/calendar` 发起 GET 请求，指定日期用 date 查询参数。仅发送日期和鉴权头，无需出生资料。沿用环境变量 HUANGLI_API_TOKEN，可设置为循古网站生成的用户 API Key；网站用户 Key 与排盘接口共用日配额。请在 OpenClaw 环境中配置密钥。[申请 API Key](https://www.xungufa.com/apikey/)

**结果**　命令输出完整黄历，包括公历、农历、年月日三柱干支、宜、忌、吉时、冲煞、月相、道历和佛历。干支按年、月、日顺序以空格分隔；宜忌和吉时完整列出。有节气时附节气名。查询节日、喜神或财神方位等结构化字段时加 `--json`，分别读取 solar、lunar、buddha 或 huangli。返回的 jieqi 为空表示当日没有交节。

请求返回 400 时核对日期；401 时提示配置有效的 HUANGLI_API_TOKEN；429 时提示配额已用尽。网络失败时报告查询状态。
