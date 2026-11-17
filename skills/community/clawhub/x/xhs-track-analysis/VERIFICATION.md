# 部署后验证包（Verification Package）

> 生成于 2026-08-21（v3.0.0）。有效期至 2026-11-19（T+90d），到期后应重新验证。
> 用法：用下列 prompt 真实触发一次，对比实际路由与 expected_sections；命中率下降即触发改进流程。

## Trigger Prompts（应触发本 skill）

| # | Prompt | 期望路由（应加载的文件） |
|---|--------|------------------------|
| T1 | "做一份小红书赛道分析：熟龄抗老，我们要进这个赛道" | methodology（Step 0-6）→ table-template → data-sources（→ collection-playbook，需采集时） |
| T2 | "分析 XX 品类在小红书的内容生态，看看达人谁在讲、内容是否饱和" | methodology（四分组 + 供给结构 7.2）→ table-template |
| T3 | "帮我采集这个小红书品类的笔记和评论数据，我要做赛道分析" | collection-playbook + collector/collect.py + data-sources |
| T4 | "评估这个护肤赛道在小红书的风险和机会，帮我们做投决" | methodology（风险扫描 7.3 + 决策收敛 7.4）→ table-template → finalize_report.py |

## Anti-Trigger Prompts（不应触发本 skill）

| # | Prompt | 应由其他能力处理 |
|---|--------|----------------|
| A1 | "帮我估算这个品类在小红书的市场规模" | 市场规模建模（本 skill 明确排斥） |
| A2 | "研究一下小红书搜索排序算法是怎么工作的" | 平台算法逆向（本 skill 明确排斥） |
| A3 | "自动帮我生成一份达人投放排期和预算" | 自动生成投放策略（本 skill 明确排斥） |
| A4 | "深度分析这个单一个达人的账号内容，判断合作" | 单达人账号深度分析（kol-account-analysis skill） |

## 路由完整性检查点

1. 是否先写三问（Step 0）再定关键词，还是直接搜完就总结
2. 关键词是否四分组 + 意图标注（发现/了解/比较/决策）
3. 每个关键词是否覆盖 4 种排序角度 + 长尾检查
4. 无数据时是否路由到 collection-playbook / data-sources 取数路径而非编造
5. 报告是否含：达人生态位 + 评论四行为 + 评论者类型/自来水 + 供给结构 + 风险扫描 + 证据边界
6. 是否产出决策结论（GO/NO-GO + 找谁讲 + 讲什么角度 + 进入策略）并运行 finalize_report.py
7. 案例引用是否仅为匿名化演示数据（无真实人名/品牌）

## 稳定性容忍阈值

- 分析/知识类任务：质量偏差容忍 ≤ 5%（关键计数错误、意图标注错列为不可容忍项）
- 路由失败（应触发未触发 / 不应触发而触发）：0 容忍
