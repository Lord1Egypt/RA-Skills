---
name: xungu-query
displayName: "☯️ 循古排盘 · 算命 / 八字 / 紫微 / 奇门 / 六爻 / 大六壬"
description: "算命、八字排盘与今日运势查询。想排紫微盘时，按出生时间查看紫微斗数十二宫、命宫与四化；想起奇门局时，按指定时刻查看奇门遁甲九宫、值符与值使。也支持六爻起卦和大六壬起课。Chinese fortune telling and astrology: BaZi, Zi Wei Dou Shu, Qi Men Dun Jia, Liu Yao, Da Liu Ren."
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":"XUNGU_API_TOKEN","envVars":[{"name":"XUNGU_API_TOKEN","required":false,"description":"循古网站用户 API Key。个人盘面和占盘需要有效 Key，匿名八字仅返回鉴权状态。"}]}}
---

# ☯️ 循古排盘 · 算命 / 八字 / 紫微 / 奇门 / 六爻 / 大六壬

用户明确请求算命或排盘时，按下表选择一个命令。查询会将所需的出生资料或起局时刻发送到循古网站。首次查询时说明数据去向，缺少密钥时引导用户在 OpenClaw 环境中设置 XUNGU_API_TOKEN。[我的 API Key](https://www.xungufa.com/apikey/)

运行 `python3 "{baseDir}/scripts/query.py" <命令>`，通过标准输入传入一个 UTF-8 JSON 对象。用户输入通过 JSON 编码传入，不拼进 shell 命令。客户端只访问 www.xungufa.com，输出 API 返回的 JSON。

| 用户要查什么 | 命令与接口 | 输入示例 |
| --- | --- | --- |
| 八字四柱、本命评级、今日运势 | bazi · POST /api/agent/bazi | `{"birth_date":"1990-05-15T10:30","gender":"女","birth_place":"北京","time_method":"现代"}` |
| 紫微斗数、本命十二宫、流年四化 | ziwei · POST /api/agent/ziwei | `{"birth_date":"1990-05-15T10:30","gender":"女","birth_place":"北京","birth_place_id":"11","target_date":"2026-11-20T09:30","layer":"year"}` |
| 奇门遁甲、按时起局、看九宫 | qimen · POST /api/agent/qimen | `{"time":"2026-11-20T09:30","mode":"maoshan","method":"时家"}` |
| 六爻、按时间起卦 | liuyao · POST /api/agent/liuyao | `{}` |
| 大六壬、起课、四课三传 | daliuren · POST /api/agent/daliuren | `{"time":"2026-11-20T09:30","guiren_mode":0}` |

**紫微斗数**　需要性别和出生地当地公历时间，精确到分钟。出生地影响时辰，先确认地点；仅当采用北京时可省略地点。国内可用唯一地名。重名及海外城市用 `locations` 命令传 `{"q":"地点"}`，从候选中确认地点，再把候选的 path 和 id 分别传作 birth_place 和 birth_place_id。默认现代计时，古法用 calculation_method=ancient。school 可选 QS、XD1、ZZ、XD2，默认 QS。layer 对应本命 natal、大限／童限 decadal、小限 small、流年 year、流月 month、流日 day、流时 hour，默认本命。查询特定运限时用 target_date 指定目标公历时刻。先展示 result.chart 的五行局、命主身主及所问宫位，再读 result.selected 的四化。宫支索引 0 至 11 依次为子至亥。

**奇门遁甲**　空对象按当前北京时间起道家阴盘。指定时刻用 time，精确到分钟或秒。道家阴盘用 yinpan，kind 可选时盘、刻盘、心盘、山向、穿壬时家、穿壬刻家、命理；山向 angle 传 0 至 359 的整数字符串。拆补法用 maoshan，method 可选时家、日家、月家、年家。置闰法用 zhirun，支持 1901 至 2051 年，其余两派支持 1900 至 2100 年。展示 cast_time、各盘 boards 的 title、info（如值符和值使）及所问宫位 palaces。多盘结果保留各盘标题。[各流派参数枚举](https://www.xungufa.com/static/openapi/agent-api.json)

**八字**　返回四柱及禄命古法本命、当日评分。读取 natal_fortune.score、daily_fortune.score；收到 UNAUTHENTICATED 时仅展示鉴权提示。若出现 time_method_warning，告知用户古法与现代计时存在差异，用户要求对照时再用古法请求第二次。

**六爻和大六壬**　不需出生档案，空对象按服务器当前时刻起卦或起课。指定时刻传公历 time。需要传统文本盘面时在命令后加 `--chart`，可直接生成六爻盘或大六壬日课。六爻展示 cast_time、本卦与变卦，六爻明细从 result.yao_6 至 yao_1 自上而下排列。大六壬默认展示 courses.ri 的四课三传，询问时课或月课时分别使用 shi、yue。


黄历日期、宜忌及吉时查询请使用独立技能 xungu-huangli。

**档案和错误处理**　原有用户档案位置为 `~/.openclaw/workspace-jarvis/memory/xungu-users.json`，按当前用户标识查找 users 下的本人记录。首次录入可询问是否记住，只有明确同意才写入或更新；用户请求删除时仅删除本人的条目。六爻、奇门时间起局和大六壬可直接查询。密钥仅通过运行环境注入。HTTP 400 时按返回的字段提示更正，401 时提示配置有效 Key，429 时告知配额已用尽。网站用户 Key 日限 20 次、账户合计 30 次；匿名八字另有 IP 限流。仅解读实际返回的数据。
