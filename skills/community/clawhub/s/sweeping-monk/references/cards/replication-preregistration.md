# 复现与预注册卡（replication & preregistration）

> 招式定位：设计/创制 / 批判/评价。学科轴：全学科（医学/社科/心理最紧迫）。
> 与 `research-playbook.md` §十七（开放科学）、`sources/B4`（假发现）、`sources/B5`（可复现宣言）互补：本卡给"取卡即用的复现闸门清单"。

## 适用场景
- 要做高风险/不可逆研究（大样本实验、毁样、政策试点）→ **先预注册再动手**。
- 读文献/评审时，第一道闸门先问"这结论复现过吗？数据公开吗？"
- 想投 Registered Report（方法先接收，不看出结果正负）。

## 核心操作
1. **预注册（preregistration）**：收数据前，把假设、设计、主要/次要结局、分析计划（含缺失处理、outlier、协变量）登记到 OSF / AsPredicted / 领域注册库（临床用 ClinicalTrials.gov），取得注册 ID/DOI。
2. **注册报告（Registered Reports）**：方法部分先投期刊送审，接收后再执行；无论结果正负都发——从源头消除"结果决定发表"。
3. **复现设计**：直接复现（同方案重跑）、概念复现（不同样本/范式验同一假设）、多实验室协作（Many Labs 模式）。
4. **复现度判读**：用效应量 + CI 而非只看 p；报告原始研究是否与复现结果相容（兼容性区间）。
5. **材料全公开**：预注册分析计划 + 数据（FAIR）+ 代码/刺激/问卷，四样齐才"可复现"。

## 前提
- 研究问题在预注册时已成形（不能边做边改核心假设）。
- 团队接受"先规划后执行"的纪律。

## 常见坑
- **预注册变"空注册"**：只登标题不登分析计划，等于没注册；评审判的是计划细不细。
- **HARKing**：先有结果再编假设；预注册正是为堵这个。
- **p-hacking 换皮**：预注册后偷偷把 exploratory 分析当 confirmatory 报——明确标注 exploratory。
- **选择性复现**：只挑"能复现的"报，仍是偏。

## 何时换招
- 要"怎么统合已有证据" → `cards/systematic-review.md`（meta 含复现度评估）。
- 要"多重比较/功效"实操 → `research-playbook.md` §十一 / §十六。
- 要"开放科学具体做法" → `research-playbook.md` §十七。

## 经典出处
- Nosek et al. 2018. *The Preregistration Revolution*. PNAS 115(11):2600–2606. DOI 10.1073/pnas.1708274114
- Open Science Collaboration. 2015. *Estimating the reproducibility of psychological science*. Science 349(6251):aac4716. DOI 10.1126/science.aac4716
- Munafò et al. 2017（见 `sources/B5-manifesto-reproducible.md`）：可复现危机需方法+报告+复现+评价+激励五维协同。
