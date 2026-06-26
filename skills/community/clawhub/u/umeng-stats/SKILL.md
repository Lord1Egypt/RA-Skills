---
name: umeng-stats
description: >
  Query Umeng (友盟) app statistics including U-APM crash/error data and U-App analytics.
  Covers: crash stats, ANR counts, error trends, affected users, daily active users,
  new users, launches, total users, and all-app summaries.
  Use when the user asks about: 崩溃统计, 友盟数据, U-APM, crash stats, ANR, error rate,
  活跃用户, 新增用户, 启动次数, 累计用户, 友盟统计, app稳定性, or any Umeng analytics question.
  Supports all 20 configured apps (工作台, 微小助, 企业服务, 微信服务, etc.).
---

# Umeng Stats

Query 友盟 U-APM (crash) and U-App (analytics) data via Open API.

## Config

Apps and credentials: `skills/umeng-crash-stats/config.json`
Resolve skill dir relative to `~/.openclaw/workspace`.

## Query Script

```bash
python3 scripts/query_crash.py \
  --app <name_or_key> \
  --type <crash|today|yesterday|allapps> \
  [--date YYYY-MM-DD|today|yesterday] \
  [--crash-type all|java|ios|native|anr|custom|freeze] \
  [--days N] [--json] [--list-apps]
```

Resolve `scripts/` relative to `skills/umeng-crash-stats/`.

### Query Types

| --type | Service | Description |
|--------|---------|-------------|
| `crash` | U-APM | 崩溃/错误统计（按小时） |
| `today` | U-App | 今日实时数据 |
| `yesterday` | U-App | 昨日统计数据 |
| `allapps` | U-App | 全产品汇总 |

### Crash Types (--crash-type, only for type=crash)

| Value | Description |
|-------|-------------|
| all (0) | 全部崩溃 |
| java/ios (1) | Java/iOS 崩溃 |
| native (2) | Native 崩溃 |
| anr (3) | ANR |
| custom (4) | 自定义异常 |
| freeze (5) | 卡顿 |

### Examples

```bash
# 工作台昨天数据（活跃/新增/启动）
python3 scripts/query_crash.py --app 工作台 --type yesterday

# 企业服务昨天崩溃
python3 scripts/query_crash.py --app 企业服务 --type crash

# 微小助今天实时数据
python3 scripts/query_crash.py --app 微小助 --type today

# 全产品汇总
python3 scripts/query_crash.py --type allapps

# 列出所有已配置 app
python3 scripts/query_crash.py --list-apps
```

## Supported Apps (in config.json)

工作台, 微小助, 企业服务, 微信服务, 企微服务, QQ服务, 新QQ服务, 飞书服务, 抖音服务, 小红书服务, WA商业版服务, WA个人版服务, 加微助手, 应用管理, Linkunion, 成长星, 违禁词, 管控助手, 拨号盘, 工作台_ios

## API Details

- Gateway: `https://gateway.open.umeng.com`
- U-APM: `umeng.quickbird.server.getStatTrend` (signed with `com.umeng.uapm`)
- U-App: `getTodayData`, `getYesterdayData`, `getAllAppData` (signed with `com.umeng.uapp`)
- Rate limit: 5 calls/second
- Max date range (crash): 90 days
- Signing: HMAC-SHA1 on `urlPath + sorted_param_kv`, key=`apiSecurity`
