# 维普 FAQ 快速路由

详细内容已经按文章拆分在 [faq/README.md](faq/README.md) 和同目录的独立 Markdown 文件中。这里保留一个短路由，方便 agent 快速定位，不再复制整篇文章。

| 用户问题 | 读取文件 | 主要动作 |
|---|---|---|
| 查重、AIGC、智评有什么区别，旧教程怎么操作 | [02-report-overview.md](faq/02-report-overview.md) | 区分指标和旧淘宝流程与当前 `/pwp` |
| 字符数、计费件数、金额或补差为什么不同 | [character-count.md](character-count.md) | 区分本地预估、平台解析、计费字段和补差状态 |
| 为什么学校系统不认维普报告编码 | [03-institution-code.md](faq/03-institution-code.md) | 解释院校自检链接和私有系统边界 |
| 报告怎么验真 | [04-report-verification.md](faq/04-report-verification.md) + [verification-logic.md](verification-logic.md) | 用订单找报告、报告编码验真、逐字段比对 |
| 微信打不开或不能下载报告 | [05-wechat-download.md](faq/05-wechat-download.md) | 换普通浏览器、`/reports`、解压 |
| 怎么进入维普、上传、付款、提交和下载 | [06-tutorial.md](faq/06-tutorial.md) | 按页面和当前 API 状态机操作 |
| 能不能退款 | [07-refund.md](faq/07-refund.md) | 只把系统明确“检测失败”作为咨询入口 |
| 产品、版本、价格、计费和上限 | [08-products-pricing.md](faq/08-products-pricing.md) | 先按场景选型，再以 `/pwp` 页面或实时配置确认 |
| 全国高校文章中的查重率/AIGC 红线 | [40-national-thresholds.md](faq/40-national-thresholds.md) | 只作背景，必须回到校方通知 |
| 武汉大学 | [41-wuhan-university.md](faq/41-wuhan-university.md) | 先确认学部、年份和指定系统 |
| 华中科技大学 | [42-hust.md](faq/42-hust.md) | 关注代码、实验方案和医学综述风险 |
| 四川大学 | [43-sichuan-university.md](faq/43-sichuan-university.md) | 不采信跨平台 AIGC 百分比换算 |
| 郑州大学 | [44-zhengzhou-university.md](faq/44-zhengzhou-university.md) | 核对院系和送审要求 |
| 中山大学 | [45-sun-yat-sen-university.md](faq/45-sun-yat-sen-university.md) | 外文项目先确认是否需要国际系统 |
| 山东大学 | [46-shandong-university.md](faq/46-shandong-university.md) | 注意一校三区和学院差异 |
| 高校自建库、自查与校查差异 | [47-self-built-database.md](faq/47-self-built-database.md) | 解释公开库、私有库、解析和统计差异 |

动态价格、启用状态、支付渠道、字符上限、订单状态和报告地址不从 FAQ 文章推断，分别以 `/pwp` 实时配置、原订单 `status` 和官方验真页面为准。
