# 维普 FAQ 独立资料库

来源入口：<https://vpcs.cqccjy.cn/faq/vip>  
抓取快照：2026-09-27  
覆盖文章：FAQ 2、3、4、5、6、7、8、40、41、42、43、44、45、46、47。

## 读取规则

每篇 FAQ 独立保存，按用户问题读取对应文件，不再依赖合并长文：

| 文件 | 文章 |
|---|---|
| [02-report-overview.md](02-report-overview.md) | 维普论文查重、AIGC 检测与斟知智评报告说明 |
| [03-institution-code.md](03-institution-code.md) | 维普检测报告编码为何不能同步到院校系统 |
| [04-report-verification.md](04-report-verification.md) | 维普论文检测报告如何验真 |
| [05-wechat-download.md](05-wechat-download.md) | 微信中无法下载维普检测报告怎么办 |
| [06-tutorial.md](06-tutorial.md) | 维普论文查重与 AIGC 检测使用教程 |
| [07-refund.md](07-refund.md) | 维普论文检测提交与退款须知 |
| [08-products-pricing.md](08-products-pricing.md) | 维普论文检测产品介绍与计费说明 |
| [40-national-thresholds.md](40-national-thresholds.md) | 2026 全国高校毕业论文查重率标准与 AIGC 红线 |
| [41-wuhan-university.md](41-wuhan-university.md) | 武汉大学毕业论文查重率要求 |
| [42-hust.md](42-hust.md) | 华中科技大学毕业论文查重率标准 |
| [43-sichuan-university.md](43-sichuan-university.md) | 四川大学毕业论文查重与 AIGC 检测 |
| [44-zhengzhou-university.md](44-zhengzhou-university.md) | 郑州大学本硕论文查重率要求 |
| [45-sun-yat-sen-university.md](45-sun-yat-sen-university.md) | 中山大学学位论文查重标准 |
| [46-shandong-university.md](46-shandong-university.md) | 山东大学毕业论文查重率与 AIGC 排查 |
| [47-self-built-database.md](47-self-built-database.md) | 高校自建库与校外自查差异 |

## 如何使用这些 FAQ 才有教学价值

FAQ 文件不是让 agent 背诵网页句子，而是提供可迁移的判断方法。回答用户时优先找下面的“核心能力”：

| 用户问题 | 先读 | 用户最终应该学会什么 |
|---|---|---|
| 字符数、件数、金额为什么不同 | [08-products-pricing.md](08-products-pricing.md) + [character-count.md](../character-count.md) | 区分本地预估、平台解析、计费字段和补差 |
| 查重、AIGC、智评有什么区别 | [02-report-overview.md](02-report-overview.md) | 按“检测目标”选产品，不能用一个百分比代替另一个 |
| 上传后一直处理中 | [06-tutorial.md](06-tutorial.md) + [workflow.md](../workflow.md) | 按状态字段判断是在解析、补差、检测还是失败 |
| 报告是真是假 | [04-report-verification.md](04-report-verification.md) + [verification-logic.md](../verification-logic.md) | 用 `orderNo` 找报告，用报告编码验真，再逐字段比对 |
| 学校系统为什么不认 | [03-institution-code.md](03-institution-code.md) + [47-self-built-database.md](47-self-built-database.md) | 区分公共验真、学校入口和学校私有库 |
| 能不能退款 | [07-refund.md](07-refund.md) | 区分未支付、解析中、检测失败和结果不满意，不能凭感觉承诺 |
| 某学校多少算合格 | 40-46 对应文件 | 只能把文章当参考材料，最终回到本年度校方通知 |

如果一个 FAQ 段落不能改变用户的产品选择、字段判断、下一步操作或风险认识，就只保留为来源摘要，不要把宣传语扩写成“结论”。

## 证据分级

- `/pwp` 页面、`config` 和原订单接口：当前可执行事实。稳定的产品和计费快照已写入 Skill；产品选择直接读取本地目录，当前价格或启用状态以 `/pwp` 页面为准。
- FAQ 2-8：站点发布的操作说明和产品说明。旧文章仍可能使用淘宝订单号，当前脚本以 `orderNo` 为查询键。
- FAQ 40-47：站点高校指南、避坑和导流文章，不是任何学校当年度正式通知。
- 图片：只用来定位字段和理解流程。图片可能展示旧域名、旧淘宝流程或演示订单，不能覆盖 `domains/cqccjy.json` 的固定域名，也不能证明当前价格和结果。

## 图片归档

核心文章中的远程图片已保存到 [../../assets/faq/](../../assets/faq/)：

- FAQ 3：院校自检系统和编码边界示例；
- FAQ 4：报告编码、检测类型和验真结果示例；
- FAQ 6：旧版浏览器、产品选择、上传和提交教程截图；
- FAQ 7：退款规则提示图；
- FAQ 8：AIGC、大学生版、研究生版和斟知智评产品卡片；
- FAQ 2：文章封面图。

图片文件保留文章中的教学信息，但 agent 输出时应遮蔽或不复述示例订单号、报告编码和个人信息。
