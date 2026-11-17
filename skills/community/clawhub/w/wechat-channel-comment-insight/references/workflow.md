# 采集计划与分析

关键词示例，只取第一屏的一个账号作为搜索样本，不表示已经核验为某公司的官方账号：

```json
{"keyword":"家居收纳","maxAccounts":1,"videosPerAccount":10,"videoPagesPerAccount":1,"maxVideos":10,"commentsPerVideo":100,"pagesPerVideo":2,"includeReplies":false}
```

用户给出确定账号时，删掉 keyword，设置 `accounts:[{"accountId":"真实账号ID"}]`。单视频用 `videos:[{"url":"https://weixin.qq.com/sph/真实短码"}]`，也支持 `{"objectId":"原样字符串","objectNonceId":"配套ID"}`。所有身份保留为字符串。

可选回复设置：`includeReplies:true`、`maxReplyParentsPerVideo:5`、`replyPagesPerComment:1`。父评论按采集顺序选取；其中 replyCount=0 的跳过。二级页每次最多请求 100 条，真实数量以返回为准；已内嵌的回复一起去重。

默认上限：1 个搜索候选、每号 1 页作品列表/最多 10 条作品、总计最多 10 条视频、每视频最多 100 条一级评论且最多 2 页。用户要求不同数量时改计划，并重新估算。成本按请求页数而非结果条数计算。

采集产物：report.xlsx、report.md、report.html、evidence.json、analysis-input.json，以及保存请求进度的 job.json。保留整个工作区可恢复；计划改变或用户要求重新采集，使用新工作区。不要把包含用户数据的工作区打包进 Skill。

分析 JSON：

```json
{"factsHash":"从analysis-input.json原样复制","findings":[{"finding":"有证据支持的观察","action":"对应建议","evidenceIds":["作品ID:评论ID"]}]}
```

每个主题说明观察内容、采样限制、代表证据和可做的动作。统计数字从 evidence.json 计算，不让模型估计；不要由昵称、地域或一句评论推断敏感身份、真实购买能力。

`collected_needs_analysis` 只表示采集完成；`analyzed` 才表示导入了证据校验通过的分析。`partial=true` 需向用户说明未获取部分。预算达到上限会保留已完成结果，不能擅自加额重跑。
