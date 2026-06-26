---
name: toxicology-assessment
description: 毒理学评估技能。覆盖TRA/PDE/TTC/QSAR/NAMs/毒理学数据库/SDS/GHS。适用化妆品/食品/药品/医疗器械/化学品安全评估。
---

# 毒理学评估技能

> v1.2.0 | 数据截止：2026年5月 | 适用：化妆品/食品/药品/医疗器械/化学品

---

## 一、核心能力矩阵

| 评估类型 | 适用场景 | 核心方法 |
|---------|---------|---------|
| TRA毒性风险评估 | 产品安全评价 | 四步法 |
| TTC毒理学关注阈值 | 无数据时快速评估 | Cramer分类 |
| PDE每日允许暴露量 | 药品杂质/残留溶剂 | ICH Q3C/Q3D |
| QSAR定量构效关系 | 数据预测 | OECD Toolbox |
| NAMs替代方法 | 减少动物试验 | OECD 471/487 |
| IATA整合测试 | 皮肤致敏/眼刺激 | OECD 497 |

---

## 二、核心术语

TTC：化学物质暴露阈值，低于此值风险极低（µg/person/day）
PDE：人每日允许摄入而不产生毒性的最大剂量（mg/day）
NOAEL：未观察到不良效应的最高剂量（mg/kg bw/day）
LOAEL：首次观察到不良效应的剂量
BMD/BMDL：基准剂量及其置信下限
LD50：引起实验动物50%死亡的剂量
MoS：安全边际 = NOAEL ÷ 暴露量

---

## 三、TRA毒性风险评估（四步法）

四步：危害识别→剂量反应→暴露评估→风险表征

危害识别数据优先级：体内试验 > 体外试验 > QSAR > 类似物 > 文献

不确定因子（UF）：动物→人=10，个体差异=10，LOAEL→NOAEL=3~10，严重毒性=1~2

暴露评估（化妆品经皮）：日暴露量 = 单次用量(g)×浓度(%)×每日次数×皮肤吸收率(%)

MoS判读：≥100可接受，25~99需关注，<25较高风险，<10不可接受

---

## 四、TTC毒理学关注阈值（Cramer分类）

决策树：遗传毒性警示结构？→金属/蛋白质/强酸碱？→Cramer分类

| 类别 | 描述 | TTC值 |
|------|------|-------|
| Class I | 低毒性，简单结构 | 1800 µg/person/day |
| Class II | 中等毒性 | 540 µg/person/day |
| Class III | 高毒性/复杂结构 | 90 µg/person/day |
| 遗传毒性警示 | 非CMR确认 | 0.15 µg/person/day |
| 确认CMR | 致癌/致畸/生殖毒 | 0.0025 µg/person/day |

不适用：金属/无机物、蛋白质、强酸碱（pH<2/>11）、放射性、纳米材料、已知CMR

---

## 五、PDE每日允许暴露量

公式：PDE（mg/day）= PoD × BW ÷ （F1×F2×F3×F4×F5×MF）
BW默认60kg；PoD优先NOAEL

修正因子：F1（小鼠12/大鼠6/仓鼠4/兔3.5/狗2/猫2/灵长类1）；F2=10；F3（≤1月10/1~3月5/>3月2/生殖5/致癌2）；F4（不可逆10/可逆1~5）；F5（有NOAEL=1/LOAEL=10）

示例：NOAEL=50 mg/kg/day（大鼠），F1=6，F2=10，F3=5，F4=1，F5=1 → PDE=10 mg/day；实际暴露5mg/day<PDE→可接受

---

## 六、QSAR软件

| 软件 | 类型 | 主要应用 |
|------|------|---------|
| OECD QSAR Toolbox | 免费 | 数据填补/类似物（OECD/ECHA）|
| TEST（ToxTree）| 免费 | 急性毒性/致突变（US EPA）|
| Derek Nexus | 商业 | 细菌突变/致癌（Lhasa）|
| Sarah Nexus | 商业 | DNA反应性致突变 |
| VEGA | 免费 | 59个模型（意大利ISS）|
| Toxtree | 免费 | 18个模型（保加利亚），含皮肤致敏/遗传毒 |
| pkCSM | 免费Web | 药代动力学ADMET+皮肤致敏Pred-Skin |

QSAR四原则：明确终点+明确算法+适用范围+拟合优度

警示结构：芳香胺、偶氮、硝基芳香烃、亚硝基、多环芳烃

---

## 七、NAMs替代方法（FDA 2026四原则）

FDA 2026 NAMs框架：以人为中心+科学严谨+透明可重复+监管等效

OECD核心测试指南：

| 方法 | OECD | 终点 |
|------|------|------|
| Ames细菌回复突变 | 471 | 遗传毒-基因突变 |
| 体外微核MNvit | 487 | 遗传毒-染色体 |
| BCOP牛角膜浑浊 | 437 | 眼刺激 |
| EpiOcular人造角膜 | 492 | 眼刺激 |
| DPRA直接多肽反应 | 442C | 皮肤致敏KE1 |
| KeratinoSens | 442D | 皮肤致敏KE2 |
| h-CLAT | 442E | 皮肤致敏KE3 |
| 3T3 NRU光毒性 | 432 | 光毒性 |
| 皮肤致敏IATA | 497 | 3选2策略 |

皮肤致敏IATA（OECD 497）：任何两个体外试验阳性→皮肤致敏结论；仅一个→证据不足

AOP框架：分子起始事件（MIE）→KE1→KE2→KE3→有害结局（AO）

---

## 八、体外试验方法库

Ames（OECD 471）：TA1535/TA100/TA1537/TA98±S9；回复突变≥2倍阴性对照

MNvit（OECD 487）：CHO/V79/HL-60±S9；≥1000个双核细胞

BCOP（OECD 437）：牛角膜浑浊度+渗透性；IVIS分类

EpiOcular（OECD 492）：MatTek重组角膜+MTT；ET-50>100s无刺激

细胞毒性：MTT法/ATP发光/LDH释放/alamarBlue/NRU/Calcein-AM/PI

HCA高内涵：微核/线粒体/神经突/钙流（Molecular Devices ImageXpress）

ADME：Franz扩散池（皮肤渗透）/肝微粒体（代谢）/HPLC-MS（代谢物）

---

## 九、监管要求

中国：化妆品安全技术规范（2015版）/安评技术导则（2021版）/中国毒理学会TTC团体标准（2025）

欧盟：EC 1223/2009（禁限用/CPSR/动物试验禁令2023）/SCCS指南/REACH

美国：MoCRA 2022（强制FRAP）/21 CFR 700-800（禁用物质）/加州65号提案（OEHHA）

药品/器械：ICH Q3C残留溶剂/ICH Q3D元素杂质/ICH M7基因毒杂质/ISO 10993-17:2023

---

## 十、毒理学数据库

| 数据库 | 网址 | 内容 |
|--------|------|------|
| BDC | bdc.iss.it | 致癌物IARC分类（意大利ISS）|
| NeurotoxKb | neurotoxkb.eu | 神经毒物知识库 |
| EFSA OpenFoodTox | efsa.europa.eu | EFSA所有化学评估与毒理学信息 |
| COSMOS | cosmosplatform.eu | 化妆品TTC方法数据 |
| 丹麦QSAR | envs.au.dk | 免费QSAR预测结果 |
| IFA | dguv.de/ifa | 职业化学品风险（德国）|
| OEHHA | oehha.ca.gov | 加州65致癌物清单/NSRL/MADL |
| HSDB | pubchem.ncbi.nlm.nih.gov | 5000+化学品毒理数据 |
| Cosmetics Info | cosmeticsinfo.org | PCPC化妆品原料CIR评估 |
| OECD Toolbox | qsartoolbox.org | QSAR工具+数据填补 |

---

## 十一、SDS/GHS安全数据表（16节）

SDS第11节（毒理学信息）：急性毒性/皮肤眼刺激/致敏/突变/致癌/生殖毒性；须注明数据来源（实验研究/文献/历史数据）

SDS编写步骤：收集数据（COA/实验室/文献）→ ISO/IEC 17025验证 → 危险性分类 → 生成SDS/GHS标签 → 电子审批 → 发布 → 保持翻译同步

GHS危险性分类（9类）：爆炸物/易燃/氧化性/压力气体/金属腐蚀/急性毒性/刺激/严重健康危害/环境危害

---

## 十二、TTC阈值对比

| 类别 | SCCS 2021（COSMOS-Munro）| 中国团体标准2025 |
|------|--------------------------|-----------------|
| Class I | 46 µg/kg bw/day | 1800 µg/person/day |
| Class II | 540 µg/person/day | 540 µg/person/day |
| Class III | 2.3 µg/kg bw/day | 90 µg/person/day |
| CMR | 0.0025 µg/person/day | 0.0025 µg/person/day |

建议：出口欧盟→SCCS 2021（更保守）；国内→中国团体标准

---

*数据来源：SGS+Molecular Devices+Labcorp+BrunsLab+无锡药石科技+中国毒理学会+OECD+FDA NAMs 2026+毒理学家说安全*
*版本：v1.2.0 | 2026-05-17*