# x2c-real-dashboard — X2C 个人数据看板

X2C 平台个人中心「总览」页的实时数据查询工具，与前端 `useDashboardData` Hook 数据口径 100% 一致。

## 功能

- 📈 **总览 KPI** — 历史/月/今/昨收入、ROI、挖矿状态、项目数、播放量
- 📊 **收益趋势** — 近 1–90 日按日聚合的 X2C + 法币收入
- 🌍 **平台播放量** — TikTok / YouTube / Instagram / Twitter / Facebook 分平台数据
- 💰 **最近动态** — 财务交易记录（X2C 释放、挖矿、佣金等）
- 🎬 **赚钱作品** — 分页列表，含每项 7 日趋势与各平台播放量

## 安装

```bash
# 安装到共享 skills 目录（所有 agent 可用）
unzip x2c-real-dashboard.skill -d ~/.openclaw/skills/

# 或安装到当前 workspace（仅当前 agent）
unzip x2c-real-dashboard.skill -d ./skills/
```

## 配置 API Key

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "x2c-real-dashboard": {
        "enabled": true,
        "apiKey": "x2c_sk_YOUR_KEY_HERE"
      }
    }
  }
}
```

或通过环境变量：

```bash
export X2C_API_KEY=x2c_sk_YOUR_KEY_HERE
```

## 示例对话

- "今天赚了多少？"
- "最近 14 天的收益趋势"
- "哪个平台播放量最高？"
- "显示最近 10 条交易记录"
- "我有哪些作品在赚钱？"

## Scripts

| 脚本 | 功能 | 参数 |
|---|---|---|
| `scripts/overview.sh` | 总览 KPI | 无 |
| `scripts/trend.sh` | 收益趋势 | `[DAYS]` 1–90，默认 7 |
| `scripts/platform-breakdown.sh` | 平台播放量 | 无 |
| `scripts/recent-activity.sh` | 最近动态 | `[LIMIT]` 1–50，默认 5 |
| `scripts/earning-projects.sh` | 赚钱作品 | `[PAGE] [PAGE_SIZE]` 默认 1 10 |

## 数据说明

- 所有日期边界为 **UTC**，每日 00:10 UTC 出账
- 轮询建议间隔 ≥ 30 秒
- `trend7d` 第一个元素为 6 天前，最后一个为今天
