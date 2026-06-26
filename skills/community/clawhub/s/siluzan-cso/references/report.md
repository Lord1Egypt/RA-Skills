# report — 运营报表查询

> 查询账号/平台维度的运营核心指标、视频表现、粉丝趋势等数据。
> 需要账号的 `mediaCustomerId`，可通过 `list-accounts --json-out` 落盘获取（参见 `references/list-accounts.md`）。

---

## 常用场景速查

| 用户意图              | 命令                                                                        |
| --------------------- | --------------------------------------------------------------------------- |
| 查某账号近期运营数据  | `siluzan-cso report fetch --media <平台> --maids <账号ID>`                  |
| 查整个平台的汇总数据  | `siluzan-cso report fetch --media <平台>`                                   |
| 近 N 天数据           | `siluzan-cso report fetch --media <平台> --days <N>`                        |
| 哪条视频播放最高      | `siluzan-cso report fetch --media <平台> --include works --order play`      |
| 查粉丝趋势（按天/周） | `siluzan-cso report fetch --media <平台> --include fans-trend --method Day` |

---

## 平台名称对照表

| 用户常说       | `--media` 参数值        |
| -------------- | ----------------------- |
| 抖音           | `Douyin`                |
| TikTok         | `TikTokBusinessAccount` |
| YouTube        | `YouTube`               |
| 微信视频号     | `Wechat`                |
| Instagram / IG | `Instagram`             |
| Facebook / FB  | `Facebook`              |
| Twitter / X    | `Twitter`               |
| Kwai / 快手    | `Kwai`                  |

---

## 示例

```bash
# 默认近 30 天，某账号核心指标 + 视频排行
siluzan-cso report fetch --media TikTokBusinessAccount --maids <账号ID>

# 近 7 天
siluzan-cso report fetch --media TikTokBusinessAccount --maids <id> --days 7

# 自定义日期区间
siluzan-cso report fetch --media YouTube --maids <id> --start 2026-01-01 --end 2026-03-31

# 多账号同时查询（同一平台）
siluzan-cso report fetch --media TikTokBusinessAccount --maids <id1> <id2> <id3>

# 不指定账号，查该平台所有账号的汇总
siluzan-cso report fetch --media YouTube --days 30

# 按播放量排序找最佳视频
siluzan-cso report fetch --media TikTokBusinessAccount --include works --order play

# 按周查近 90 天粉丝趋势
siluzan-cso report fetch --media YouTube --days 90 --method Week --include fans-trend
```

---

## `--include` 可查询模块

不传 `--include` 时默认查所有模块：

| 模块名               | 含义                                   |
| -------------------- | -------------------------------------- |
| `operation`          | 核心运营指标（播放、互动、粉丝增量等） |
| `total-fans`         | 当前总粉丝数                           |
| `fans-analysis`      | 粉丝画像                               |
| `works`              | 视频明细（可按播放/点赞/完播排序）     |
| `fans-trend`         | 粉丝趋势                               |
| `new-fans-trend`     | 新增粉丝趋势                           |
| `comment-trend`      | 评论趋势                               |
| `hot-topic`          | 热门话题                               |
| `hot-comment-word`   | 热门评论词云                           |
| `comment-top10`      | Top10 热门评论                         |
| `video-duration`     | 视频时长分布                           |
| `video-distribution` | 视频流量分布                           |
| `homepage-visit`     | 主页访问数据                           |

**`--order` 可选值**（配合 `--include works`）：`play`（播放）/ `digg`（点赞）/ `fullplay`（完播）

---

## `--method` 聚合维度

| 值            | 含义 | 适用场景             |
| ------------- | ---- | -------------------- |
| `Day`（默认） | 按天 | 近 7~30 天细粒度分析 |
| `Week`        | 按周 | 近 2~3 个月趋势      |
| `Moth`        | 按月 | 年度趋势             |

---

## AI 行为规则

1. 用户没说具体账号/平台时，先用 `list-accounts` 展示总览，让用户决定深入哪个账号。
2. 用户提到具体平台但没有账号 ID 时，先用 `list-accounts --json-out` 落盘获取，再调 `report fetch --maids`。
3. 用户只想横向对比账号，优先用 `list-accounts`（账号 overview 字段即包含粉丝/播放数据），无需调 `report fetch`。
4. 未指定时间范围时，默认 `--days 30` 并告知用户。

---

## 交叉引用

- 获取账号 mediaCustomerId → 参见 `references/list-accounts.md`
