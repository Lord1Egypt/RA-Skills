# morning-brief

晨间简报 Skill - 每天早上 8 点自动推送假期倒计时和时间进度提醒。

## 功能

- 📅 显示当前日期、周数、星期
- 🏖️ 距离周末还有几天
- 🎊 距离各法定节假日还有几天（春节、清明、劳动节、端午、中秋、国庆、元旦等）
- 📊 时间进度：本周/本月/本年进度百分比

## 触发方式

Cron 定时任务：每天早上 8:00 自动执行

```json
{
  "trigger": {
    "type": "cron",
    "value": "0 0 8 * * ?"
  }
}
```

## 安装

```bash
clawhub install morning-brief
# 或手动复制到 skills/morning-brief 目录
cd skills/morning-brief
npm install
```

## 依赖

- axios ^1.6.0
- dayjs ^1.11.0

## 数据来源

中国节假日数据来自 [lanceliao/china-holiday-calender](https://github.com/lanceliao/china-holiday-calender)

## 示例输出

```
提醒您：2026 年 03 月 18 日，第 12 周，周三，大家上午好，
工作虽然辛苦，但也不要忘了休息，起来走一走～
距离【周末】还有 3 天
距离【清明节】还有 16 天
距离【劳动节】还有 43 天
距离【端午节】还有 92 天
距离【中秋节】还有 190 天
距离【国庆节】还有 196 天
距离【周一】过去 3 天 (42%)
距离【月初】过去 17 天 (58%)
距离【年初】过去 77 天 (21%)
```

## 作者

Original by GitHub user (morning-skill-github)
Packaged for OpenClaw

## 许可

MIT
