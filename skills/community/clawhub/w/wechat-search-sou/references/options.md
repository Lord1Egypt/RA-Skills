# 微信搜一搜实时搜索 完整选项参数说明

> 与 `scripts/wechat/*-cli.js`、`assets/*_cli_req.schema.json` 保持一致。非法枚举会直接失败，不会静默改成默认值。

## 微信文章搜索

| 参数            | 缩写 | 作用     | 可选值                                      | 必填 | 默认值 |
| --------------- | ---- | -------- | ------------------------------------------- | ---- | ------ |
| `--keyword`     | `-k` | 搜索关键词 | 2-50 个字符，不能是链接，不含 `< > " ' &` | 是   | 无     |
| `--sort`        | `-s` | 排序     | 0=综合 / 1=最新 / 2=最热                    | 否   | 0      |
| `--publishTime` | `-t` | 发布时间 | 0=不限 / 1=最近1天 / 2=最近7天 / 3=最近半年 | 否   | 0      |
| `--limit`       | `-l` | 返回数量 | 1-10000（**包月 Token 实际最多 20**）       | 否   | 10     |
| `--help`        | `-h` | 帮助     |                                             | 否   |        |

```bash
# 基础语法
node scripts/wechat/article-cli.js --keyword <关键词> --sort <排序> --publishTime <发布时间> --limit <返回数量>

# 搜索"AI"的微信文章
node scripts/wechat/article-cli.js --keyword AI

# 搜索"AI"的热门微信文章
node scripts/wechat/article-cli.js --keyword AI --sort 2

# 搜索"AI"的最近1天发布的微信文章
node scripts/wechat/article-cli.js --keyword AI --publishTime 1
```

## 微信视频搜索

| 参数         | 缩写 | 作用     | 可选值                                           | 必填 | 默认值 |
| ------------ | ---- | -------- | ------------------------------------------------ | ---- | ------ |
| `--keyword`  | `-k` | 搜索关键词 | 2-50 个字符，不能是链接，不含 `< > " ' &`      | 是   | 无     |
| `--sort`     | `-s` | 排序     | 0=综合 / 1=最新 / 2=最热                         | 否   | 0      |
| `--duration` | `-d` | 视频时长 | 0=不限 / 1=5分钟以下 / 2=5-20分钟 / 3=20分钟以上 | 否   | 0      |
| `--limit`    | `-l` | 返回数量 | 1-10000（**包月 Token 实际最多 20**）            | 否   | 10     |
| `--help`     | `-h` | 帮助     |                                                  | 否   |        |

```bash
# 基础语法
node scripts/wechat/video-cli.js --keyword <关键词> --sort <排序> --duration <视频时长> --limit <返回数量>

# 搜索"AI"的微信视频
node scripts/wechat/video-cli.js --keyword AI

# 搜索"AI"的最新微信视频
node scripts/wechat/video-cli.js --keyword AI --sort 1

# 搜索长度在5-20分钟的"AI"的微信视频
node scripts/wechat/video-cli.js --keyword AI --sort 2 --duration 2
```

> **套餐双上限**：技能硬上限 10000（按量）。包月 Token 超限返回 `PLAN_LIMIT`：文章/视频搜索最多 **20** 条。
> **计费错误码**：余额不足 → `INSUFFICIENT_BALANCE`（15）；短时过频 → `RATE_LIMITED`（2）；日消费上限 → `DAILY_LIMIT`（后端 `CheckDayMoney` **18**）。均禁止盲目重试。

> **数量约定**：未指定 `--limit` 时只返回 10 条。用户未要求更多时不要加大。创建后约 9 分钟内同参可复用任务；结果约 15 分钟内可查询。
