# 毒理学数据库与QSAR工具参考

> version: 1.0.0（毒理学评估技能附录文件）
> 学习来源：毒理学家说安全（微信专辑）+ 各数据库官网
> 数据截止：2026年5月

---

## 一、毒理学数据库

| 数据库 | 开发者 | 网址 | 主要内容 |
|--------|-------|------|---------|
| BDC | ISS意大利 | bdc.iss.it | 致癌物数据库，含IARC分类及流行病学数据 |
| NeurotoxKb | 荷兰 | neurotoxkb.eu | 神经毒物知识库，神经毒性物质识别 |
| EFSA OpenFoodTox 2.0 | 欧洲食品安全局 | efsa.europa.eu | EFSA所有化学评估与毒理学信息，食品/饲料/农药全覆盖 |
| COSMOS数据库 | 欧洲COSMOS项目 | cosmosplatform.eu | 化妆品原料安全评估数据，基于TTC方法 |
| 丹麦(Q)SAR数据库 | 丹麦环保署 | envs.au.dk | 免费QSAR预测结果与化学品风险数据 |
| IFA数据库 | 德国IFA | dguv.de/ifa | 职业化学品风险评估，WORKPLACELIMITS |
| OEHHA | 加州环保署 | oehha.ca.gov | 加州65号提案致癌物清单，发育/生殖毒物识别 |
| HSDB | NIH/旧金山 | pubchem.ncbi.nlm.nih.gov | 5000+化学品毒理/暴露/急救数据 |
| Cosmetics Info | PCPC | cosmeticsinfo.org | 美国化妆品原料数据库，含CIR评估报告 |
| OECD QSAR Toolbox | OECD/ECHA | qsartoolbox.org | 免费QSAR工具，含类似物查找与数据填补 |

## 二、EFSA OpenFoodTox 2.0

欧洲食品安全局综合毒理学数据库，收录EFSA自创建以来所有化学评估与毒理学信息。
- 查询食品/饲料/农药化学物质的毒理学终点数据（NOAEL/LOAEL/ADI）
- 检索EFSA已发布的科学评估结论
- 用于食品接触材料、农药、添加剂合规评估

## 三、OEHHA 加州65号提案

OEHHA（California Office of Environmental Health Hazard Assessment）维护《加州65号提案》有害物质清单。
- 致癌物质清单查询（Prop 65 List）
- 发育/生殖毒物（DART）识别
- 安全港水平（NSRL）与每日可接受摄入量（MADL）查询
- 每年至少两次更新，出口美国加州市场产品须筛查

## 四、SDS/GHS安全数据表（16节）

SDS（Safety Data Sheet）是GHS体系中传递化学品危险信息的核心文件，16个部分：

| 节号 | 内容 | 节号 | 内容 |
|------|------|------|------|
| 1 | 标识（产品名称/CAS/供应商）| 9 | 物理和化学特性 |
| 2 | 危险识别（GHS象形图/信号词/危害声明）| 10 | 稳定性和反应性 |
| 3 | 成分/配料信息 | 11 | **毒理学信息**（须含急性毒性/皮肤刺激/致敏/突变/致癌/生殖毒性）|
| 4 | 急救措施 | 12 | 生态信息 |
| 5 | 消防措施 | 13 | 处置注意事项 |
| 6 | 意外泄漏措施 | 14 | 运输信息 |
| 7 | 操作处置和储存 | 15 | 监管信息 |
| 8 | 暴露控制/个人防护（OEL/PPE）| 16 | 其他信息（编制日期/版本）|

SDS编写步骤：收集数据（COA/实验室/文献）→ 验证方法（ISO/IEC 17025）→ 危险性分类 → 生成SDS和GHS标签 → 电子审批 → 发布 → 保持翻译同步

## 五、Toxtree 3.1.0（18个模型插件）

Toxtree由IdeaConsult（保加利亚）开发，基于Java的免费QSAR软件，主要根据警示结构对物质进行分类和毒性预测。最新版Toxtree-3.1.0含18个模型插件，安装需要JRE 7以上。

主要模型：CRAMER2（Cramer分类）、SkinSense（皮肤致敏）、DNA alerts（DNA反应性致突变）、Carcinogenicity BGv2（致癌性）、Bacterial Mutagenicity（细菌突变性 Ames模拟）、Acute Toxicity LD50（急性经口毒性）、Developmental toxicity（发育毒性）、Aquatic Toxicity（水生毒理）、皮肤腐蚀性

使用方法：下载安装 → 导入SMILES/SDF结构 → 选择模型插件 → 查看预测结果（含警示结构+分类依据）→ 结合试验数据综合判断

## 六、VEGA QSAR（59个模型）

VEGA由意大利ISS开发，JAVA应用程序，集成59个QSAR模型，可预测理化、毒理、生态毒理、环境行为等终点。安装需要JRE 7以上。

模型分类：理化性质（~10）、健康毒理（~20）、生态毒理（~15）、环境行为（~10）、毒代动力学（~5）

在基因毒性杂质评估中应用：输入SMILES结构 → 运行Ames预测模块 → 查看DNA反应性警示结构（亲电基团）→ 结合TTCi方法（ICH M7）计算可接受摄入量 → 置信度评估

## 七、pkCSM（药代动力学与毒性预测）

pkCSM是预测小分子药代动力学和毒性的免费Web工具（pkcsm.crdd.soton.ac.uk），基于图结构特征进行分子表示。

主要模块：Absorption（Caco-2渗透性/肠道吸收/皮肤渗透）、Distribution（血浆蛋白结合率/P-gp底物/血脑屏障）、Metabolism（CYP450酶抑制 1A2/2C19/2C9/2D6/3A4）、Excretion（肾脏分泌率/Total clearance）、Toxicity（皮肤致敏 Pred-Skin/hERG心脏毒性/Ames/Max tolerated dose）

Pred-Skin：基于109种化合物的人体皮肤致敏数据，可与DPRA/KeratinoSens交叉验证。局限性：不适用于聚合物/无机物/蛋白质。

## 八、TTC阈值对比（SCCS vs 中国团体标准）

| Cramer类别 | SCCS 2021（COSMOS-Munro）| 中国毒理学会团体标准（2025）|
|------------|--------------------------|--------------------------|
| Class I | 46 µg/kg bw/day | 1800 µg/person/day |
| Class II | 540 µg/person/day（约9 µg/kg bw/day）| 540 µg/person/day |
| Class III | 2.3 µg/kg bw/day | 90 µg/person/day |
| 遗传毒性/CMR | 0.0025 µg/person/day | 0.0025 µg/person/day |

选择建议：出口欧盟用SCCS 2021（更保守）；中国国内市场用中国团体标准；遗传毒性/CMR两者一致。

## 九、GHS危险性分类（16类）

| 类别 | 名称 | 类别 | 名称 |
|------|------|------|------|
| GHS01 | 爆炸物 | GHS02 | 易燃气体/气溶胶/固体 |
| GHS03 | 氧化性气体/液体/固体 | GHS04 | 压力气体 |
| GHS05 | 金属腐蚀物 | GHS06 | 急性毒性（1-5类）|
| GHS07 | 皮肤刺激/致敏/急性毒性（4类）| GHS08 | 严重健康危害（致癌/致畸/生殖毒）|
| GHS09 | 环境危害 | | |

---

*版本：v1.0.0 | 2026-05-17 | 毒理学评估技能附录文件*