# traffic-query

A practical OpenClaw skill for querying **China domestic flights and trains** and turning messy result pages into clean, chat-friendly summaries.

## What it does

`traffic-query` helps an agent:
- query flight information
- query high-speed rail / train information
- normalize schedules, prices, duration, stops, and seat/cabin details
- distinguish full results vs partial results
- summarize the best options for chat

## Best use cases

Use it for requests like:
- 查明天北京大兴飞深圳所有航班
- 查北京到深圳的高铁和动车
- 查下午三点后直飞深圳的班次
- 查最便宜的 3 个方案
- 总结携程 / 12306 / OTA 结果页

## Output style

The skill prefers compact lines like:

- 南航 CZ3190｜20:00-23:30｜直飞｜¥829起
- G303｜10:00-17:50｜7时50分｜二等座 ¥1107.5

## Included files

- `SKILL.md` — workflow and usage rules
- `references/sources.md` — source notes, route/station caveats, extraction checklist

## Notes

- Browser Relay is preferred when the user already has a filtered result page open.
- Public scraping can be incomplete on dynamic or anti-bot-heavy sites.
- The skill favors honesty over fake precision.

## Version

Current version: **1.0.1**
