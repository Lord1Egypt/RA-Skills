# Google 账户分析报告

> 统计区间：`{startDate}` ~ `{endDate}`  
> 账户：`{mediaCustomerId}`

> **用户明确要求 Excel / xlsx**（且非 OKKI / 询盘话术）时：在拉数步骤不变的前提下，**另 Read 全文** `report-templates/google-period-report-excel.md`，并**先读齐**各维度 `*.outline.txt` 再写脚本；禁止加载宿主第三方 xlsx Skill。

---

## 默认报告维度

生成报告时，**默认包含**以下 8 个维度：

| #   | 维度                                                                         | CLI                                                                                           |
| --- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1   | 执行摘要（消耗/展示/点击/转化/CTR/CPC/CPA 本期概览）                         | `google-analysis --sections overview`                                                         |
| 2   | 每日投放趋势（按日消耗/点击/转化曲线；金额/CPA **2 位小数**，转化/点击整数） | `google-analysis --sections daily-metrics`                                                    |
| 3   | 月度汇总（全周期汇总数据）                                                   | `google-analysis --sections dimension-summary`                                                |
| 4   | 广告系列表现（预算/出价策略/各系列消耗与效果）                               | `google-analysis --sections campaigns`                                                        |
| 5   | 设备分布（PC/移动/平板 消耗/点击/转化）                                      | `google-analysis --sections devices`                                                          |
| 6   | 地域分布（国家/地区 消耗占比）                                               | `google-analysis --sections geographic`                                                       |
| 7   | 关键词表现（词/消耗/CTR/CPC 排行）                                           | `google-analysis --sections keywords`（这个命令获取的关键词数据会来自多个系列，不能合并去重） |
| 8   | 优化建议（根据以上数据给出可执行改进建议）                                   | 不额外拉数，基于已有数据撰写                                                                  |

**在执行任何数据拉取之前**，先向用户展示以下可选维度，询问是否需要追加：

---

## 平台支持的全部可选维度

| 维度          | CLI                                             | 备注                                                              |
| ------------- | ----------------------------------------------- | ----------------------------------------------------------------- |
| 系列按小时    | `google-analysis --sections campaign-hour`      | 行在 `items[]`，含 `date`/`hour`/消耗与效果                       |
| 受众分布      | `google-analysis --sections audience`           | 可分 `SystemDefined` / `UserDefined`                              |
| 搜索词报告    | `google-analysis --sections search-terms`       | 高消耗搜索词；`queryTargetingStatusZh` 列（已添加/已排除/都没有） |
| 广告创意表现  | `google-analysis --sections ads`                | 广告标题/类型/到达网址                                            |
| 附加信息      | `google-analysis --sections extensions`         | 附加链接/电话/宣传信息等状态                                      |
| 图片/视频素材 | `google-analysis --sections materials`          | 图片 + 视频合并视图                                               |
| 账户落地页    | `google-analysis --sections final-urls`         | 主投放域名/落地页（不传日期）                                     |
| 黄金账户评分  | `google-analysis --sections gold-account`       | 健康度评分与各项达标状态                                          |
| 广告质量指标  | `google-analysis --sections ads-index`          | 质量得分汇总                                                      |
| 转化动作配置  | `google-analysis --sections conversion-actions` | 已配置的转化目标列表                                              |
| 账户结构统计  | `google-analysis --sections resource-counts`    | 系列/组/广告/词数量                                               |
| 广告系列类型  | `google-analysis --sections campaign-types`     | 系列类型分布（不传日期）                                          |

---

## 拉数顺序（默认 7 个维度）

**首选：用 `google-analysis --sections` 一次拉齐**（单进程复用 keep-alive，比逐个 spawn 快 3-7×；详见 `references/analytics/account-analytics.md` 的 `all` 子命令说明）：

```bash
mkdir -p ./snap-google
siluzan-tso google-analysis -a <id> --start <s> --end <e> --json-out ./snap-google \
  --sections overview,daily-metrics,dimension-summary,campaigns,devices,geographic,keywords
```

如果用户**追加**了维度（按上文「可选追加」表），把它们加入 `--sections` 即可；要全 21 维则省略 `--sections`。

> 仅在调试单个维度或需要传 `all` 暂未透传的特殊参数时，才回落到逐条 `siluzan-tso google-analysis <子命令> -a <id> …` 调用。
