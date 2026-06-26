---
name: rili
description: "Calendar and Chinese lunar date lookups via a bundled local Node script. Use when the user asks about dates, weekdays, month views, lunar calendar dates, traditional lunar festivals, or Gregorian↔lunar conversion. Triggers on 日历, 月历, 农历, 公历, 初几, 星期几, 黄历日期, 春节, 元宵, 端午, 中秋, 重阳. NOT for calendar event CRUD, reminders, or shared calendar integrations."
metadata: { "openclaw": { "emoji": "📅", "requires": { "bins": ["node"] } } }
---

# Rili Skill

面向中文日期查询的本地日历技能，覆盖公历、星期、月历、农历、常见农历节日日期查询。

默认用中文回答，优先给出：

- 公历日期
- 星期
- 农历年月日
- 生肖
- 常见农历节日

## 适用场景

- “今天农历几月几号？”
- “2026-03-14 是星期几？”
- “看一下 2026 年 9 月月历”
- “2026 年中秋节是几号？”
- “农历 2025 年闰六月初一对应哪天？”
- “今年春节是哪天？”

## 不适用场景

- 创建、修改、删除日历事件
- 查询共享日程、会议邀请、提醒事项
- 天文级精度的节气、朔望月、黄历宜忌
- 地区差异明显的民俗日期（例如“小年”）

## 命令

### 今天 / 指定日期

```bash
node {baseDir}/scripts/rili.js today
node {baseDir}/scripts/rili.js date 2026-03-14
node {baseDir}/scripts/rili.js date tomorrow --tz Asia/Shanghai
node {baseDir}/scripts/rili.js date 2026-02-17 --json
```

### 月历

```bash
node {baseDir}/scripts/rili.js month 2026-03
node {baseDir}/scripts/rili.js month today --tz Asia/Shanghai
node {baseDir}/scripts/rili.js month 2026-09 --json
```

说明：

- 月历文本视图按周一到周日排列。
- 文本输出下方会补充农历月初和常见节日节点。

### 农历转公历

```bash
node {baseDir}/scripts/rili.js find-lunar 2026 8 15
node {baseDir}/scripts/rili.js find-lunar 2025 6 1
node {baseDir}/scripts/rili.js find-lunar 2025 6 1 --leap
node {baseDir}/scripts/rili.js find-lunar 2025 6 1 --json
```

说明：

- `find-lunar <lunarYear> <month> <day>` 里的年份是**农历年**，不是公历年。
- 不带 `--leap` 时，如果该农历年存在同月闰月，会返回普通月和闰月两个结果。
- 带 `--leap` 时只返回闰月结果。

### 常见农历节日

```bash
node {baseDir}/scripts/rili.js festival 2026 中秋
node {baseDir}/scripts/rili.js festival 2026 春节 --json
node {baseDir}/scripts/rili.js festival list
```

当前支持：

- 春节
- 元宵
- 龙抬头
- 上巳
- 端午
- 七夕
- 中元
- 中秋
- 重阳
- 腊八
- 除夕

## 回复习惯

- 用户问“今天农历几号”，直接给公历 + 星期 + 农历。
- 用户问“某天是星期几”，补充农历会更有用。
- 用户问“今年中秋/春节是哪天”，优先返回精确公历日期，并标明对应农历。
- 用户问“某月月历”，给出月历文本；若还关心农历细节，再用 `--json` 或逐日查询。
- 结果里若出现闰月，要明确写成“闰六月”等，不要省略。

## 注意事项

- 这是本地计算，不依赖外部 API。
- 农历换算依赖 Node 的 `Intl` 中文历法支持，适合常见问答场景。
- 不要把这个技能用于“帮我加一个日历事件”；那是日程/日历集成问题，不是日期查询。
