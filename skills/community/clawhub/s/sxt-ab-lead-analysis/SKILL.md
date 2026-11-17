---
name: sxt-ab-lead-analysis
description: 私信通(私信AI) AB 实验留资效果分析全流程 playbook。从线上埋点表 CSV 出发, 完成「会话重建 → 留资信号标注(A/B/C+宽口径) → 组间对比与置信区间 → 行业 mix 分解/标准化/商家配对 → 漏斗分层 → OR 归因(规则版特征 + LLM 反向提取 rubrics 管道) → 在线报告」。当用户要"分析 AB 实验留资率差异""实验组对照组留资对比""归因哪些 AI 动作影响留资""跑 rubrics OR 归因""复跑留资分析报告"时使用。也适用于其他二值结局(如成单/加微)的会话级 AB 归因分析。
---

# 私信通 AB 留资分析

对照产出物: 在线报告 dashboardId=`74A745162541EB3D096DD9667B4AAADC`; LLM 管道执行记录 REDoc `b61d031b113084e5690ded518dc9369b`; 首次执行(2026-07-24)中间产物在 `~/workspace/temp_files/sxt_ab_lead_analysis/`。

## 核心方法论(先读, 决定报告结论质量)

1. **总率直接对比不可信**——行业 mix 污染是头号陷阱(首次分析中教辅行业两组占比差 2.2 倍, 压低表观差异 2.3pp)。结论必须以「宽口径 + 行业标准化/商家配对」为准。
2. **文本口径系统性漏判组件留资**——只用 A/B/C 文本规则会把"发留资卡组件收资"的形态判成未留资, 且对发卡率高的组偏差更大。宽口径 = A∪B∪C∪企微卡点击∪hasLeadGen。
3. **OR 归因必须控内生性**——AI 动作受用户意图影响, 裸 OR 把用户意图记到动作头上。对策: 剔除 L0(用户未开口)会话、两组分开算 OR、**读因果只读动作全量化的实验组列**(近自然实验), 对照组高 OR 因子(如 emoji/催促)多为"会话活了"的混杂假象。
4. **警惕同义反复与 halo**——与结局定义重叠的 rubric(如"留资后跟进")OR 无意义须剔除; LLM 判定可见留资事件文本会产生 halo, 严格版应把会话截断到首个留资事件前再判定。
5. 先做 turn_trace 硬故障体检排除工程问题解释(首次分析: 硬故障 session ≤3.1%, 影响 <0.5pp, 不解释组间差)。

## 执行流程(七步)

数据 schema、口径正则、分层定义等细节见 [references/data-schema.md](references/data-schema.md)——第 1-4 步开始前先读它。

1. **数据解析与会话重建**: 埋点表 CSV(表头文件+part 文件, BOM 用 utf-8-sig)→ 按 raw_request 的 `session.visitorId × proUserId` 聚合为 session → 产出 all_sessions.jsonl(每行一个 session 含全部消息)。分组: biz_name 含 chat-with-history=exp, rag/ask=ctrl; 同 session 跨两组的"混合会话"单独记 key 列表, 主分析剔除并做含/不含敏感性检验。
2. **留资信号标注**: 逐 session 打 A/B/C/组件/宽口径布尔标 + 行业 + 漏斗分层 L0-L5 → all_flagged.jsonl。
3. **总率对比**: 两组 A/B/C 口径与宽口径留资率, Wilson 或正态近似 95%CI; 差值 CI 跨零与否分开报。
4. **行业 mix 处理**(结论主口径): ①按行业分解贡献(定位 mix 差异大户) ②直接标准化(以合并组行业分布为权重) ③同商家配对对比(两组都有会话的商家内配对)。三个口径互证。
5. **漏斗分层与定性归因**: L0-L5 分布对比 + 负向行业(若有)抽样读会话找机制(路径稀释/口径迁移/场景错配等)。
6. **OR 归因**(可选但强烈建议): 规则版 12 特征全量 + LLM rubrics 管道(归纳→合并→判定→OR+FDR)。完整管道含 prompt 模板、模型参数、质检清单见 [references/or-pipeline.md](references/or-pipeline.md); 18 条 rubrics 起点库直接复用 [references/rubrics_final.json](references/rubrics_final.json)(换 rubric 集只需替换此文件重跑判定+OR 两步); OR/CI/BH-FDR 计算用 `scripts/or_fdr.py`(确定性脚本, 输入 judgments jsonl + flags)。
7. **报告产出**: 结构参照首次报告八节(TL;DR/数据概况/留资率对比/行业 mix+负向深挖/漏斗/turn_trace 体检/OR 归因/建议), html-go-live 部署; 更新已有报告用 `--update 74A745162541EB3D096DD9667B4AAADC --force` 保链接不变。

## 报告写作纪律

- 每个数字带口径标注(A/B/C/宽), 每个组间差带 CI。
- "表观负向/正向"与"标准化后"分开陈述, 不许只报其一。
- OR 表按 exp 列排序解读, ctrl 列仅作交叉验证; 同义反复项与 halo 疑似项在质检小节显式声明。
- 方法论局限(相关非因果/结局泄漏/判定相关性)必须有诚实声明小节。
