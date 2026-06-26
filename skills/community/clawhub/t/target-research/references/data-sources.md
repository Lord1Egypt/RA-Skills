# 数据源与采集规范

> 数据采集核心原则：每类数据必须从指定来源获取，禁止凭记忆填写结构、临床、专利数据。

---

## 数据源 A — 靶点基础信息（最高优先级）

**主力来源（按优先级）：**

来源 1（UniProt，必查）：
- URL：`https://www.uniprot.org/uniprot/?query={基因符号}+organism_id:9606&format=json`
- 备选手动页：`https://www.uniprot.org/uniprotkb?query={基因符号}+organism_id:9606`
- 提取：UniProt ID、蛋白全称、分子量、功能摘要、亚细胞定位、跨膜区、PTM、同源蛋白

来源 2（NCBI Gene）：
- URL：`https://www.ncbi.nlm.nih.gov/gene/?term={基因符号}+AND+Homo+sapiens`
- 提取：基因ID、基因组位置、功能描述、疾病关联、通路链接

来源 3（搜索补充）：
- 搜索词：`"{靶点名称} {基因符号} protein function signaling pathway review"`

**提取字段：**

| 字段 | 说明 |
|------|------|
| UniProt ID | 主 accession |
| 蛋白全称 | Full protein name |
| 分子量 | kDa |
| 功能摘要 | 2-3句核心功能 |
| 亚细胞定位 | 膜/胞浆/核 |
| 跨膜次数 | 如适用 |
| 同源家族成员 | 列出主要同源物 |
| 关键PTM | 磷酸化/泛素化/乙酰化位点 |

---

## 数据源 B — 蛋白结构信息 + CRO Assay 可及性

**主力来源：**

来源 1（RCSB PDB）：
- 搜索页：`https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22value%22%3A%22{基因符号}%22%2C%22attribute%22%3A%22rcsb_entry_container_identifiers.gene_names%22%7D%7D%7D`
- 简化搜索：`https://www.rcsb.org/search?q={基因符号}`
- 提取：PDB ID列表、分辨率、配体类型、是否有小分子共晶

来源 2（AlphaFold DB）：
- URL：`https://alphafold.ebi.ac.uk/search/text/{基因符号}`
- 提取：预测结构可用性、pLDDT评分

来源 3（搜索补充）：
- 搜索词：`"{靶点名称} crystal structure PDB X-ray"`
- 搜索词：`"{靶点名称} allosteric site pocket structure"`

**提取字段：**

| 字段 | 说明 |
|------|------|
| PDB条目总数 | 截至查询日 |
| 代表性PDB ID | 最高分辨率+共晶 |
| 最高分辨率 | Å |
| 是否有小分子共晶 | 是/否，列出配体名 |
| 是否有别构位点结构 | 是/否 |
| AlphaFold预测可用 | 是/否 + pLDDT |
| 结合口袋特征 | 深度/体积/亲疏水性描述 |

**成药性评估搜索：**

```
搜索词："{靶点名称} druggability assessment pocket"
搜索词："{靶点名称} TID score CanSAR"
搜索词："{靶点名称} DrugEBIlity"
```

**CRO Assay 可及性搜索：**

```
搜索词："{靶点名称} {基因符号} assay biochemical binding enzymatic"
搜索词："{靶点名称} {基因符号} cell-based assay reporter luciferase"
搜索词："{靶点名称} inhibitor screening assay Eurofins DiscoverX Reaction Biology"
搜索词："{靶点名称} {基因符号} ADME assay panel CRO service"
```

**CRO panel 检查（直接访问）：**
- Eurofins SafetyScreen / Lead Profiling：`https://www.eurofinsdiscovery.com/`
- DiscoverX KINOMEscan / GPCR scan：`https://www.discoverx.com/`
- Reaction Biology：`https://www.reactionbiology.com/`

提取 CRO Assay 字段：

| 字段 | 说明 |
|------|------|
| 生化 assay 类型 | 酶活/结合/荧光偏振/SPR等 |
| 细胞 assay 类型 | 报告基因/表型/二聚化/Ca²⁺流等 |
| CRO 现成 panel | 是否有现成服务 |
| 定制开发需求 | 需新开发的 assay |
| 定制难度评级 | 低/中/高 |
| Assay 丰富度评级 | 🟢/🟡/🔴 |
| 对项目启动影响 | 时间线/预算影响 |

---

## 数据源 C — 功能与信号通路

**主力来源：**

来源 1（KEGG Pathway）：
- 搜索：`https://www.kegg.jp/search/pathway?query={基因符号}`
- 提取：参与的通路列表、通路中的上下游关系

来源 2（Reactome）：
- 搜索：`https://reactome.org/content/query?q={基因符号}&species=Homo+sapiens`
- 提取：反应、通路层级

来源 3（搜索补充）：
- 搜索词：`"{靶点名称} {基因符号} signaling pathway review 2024 2025"`
- 搜索词：`"{靶点名称} tissue expression expression profile"`
- 搜索词：`"{靶点名称} disease association GWAS OMIM"`

**提取字段：**

| 字段 | 说明 |
|------|------|
| 主要功能 | 1-2句 |
| 关键通路 | 列出3-5条核心通路 |
| 上游调控 | 激活/抑制该靶点的分子 |
| 下游效应 | 该靶点调控的分子/通路 |
| 组织表达谱 | 高表达组织/器官 |
| 疾病关联 | GWAS/OMIM/文献支持 |

---

## 数据源 D — 竞争格局：在研药物与管线

**主力来源：**

来源 1（ClinicalTrials.gov）：
- 搜索：`https://clinicaltrials.gov/search?cond=&term={靶点名称}+OR+{基因符号}&intr=`
- 提取：在研临床试验数量、阶段分布、适应症、申办方

来源 2（Cortellis / DrugBank 搜索）：
- 搜索词：`"{靶点名称} {基因符号} inhibitor drug pipeline clinical trial"`
- 搜索词：`"{靶点名称} {基因符号} small molecule drug development pipeline 2024 2025"`

来源 3（按公司深入）：
- 搜索词：`"{靶点名称} {公司名} pipeline phase"`
- 搜索词：`"{靶点名称} lead compound candidate IND"`

来源 3（差异化策略搜索）：
- 搜索词：`"{靶点名称} {基因符号} allosteric modulator biased signaling differentiation strategy"`
- 搜索词：`"{靶点名称} {基因符号} isoform selectivity specificity challenge opportunity"`
- 搜索词：`"{靶点名称} {基因符号} orphan drug rare disease opportunity"`
- 搜索词：`"{靶点名称} {基因符号} combination therapy biomarker precision medicine"`

来源 4（竞争者差异化分析搜索）：
- 搜索词：`"{靶点名称} inhibitor competitor differentiation mechanism clinical strategy"`
- 搜索词：`"{靶点名称} {竞争者药物名} vs {另一竞争者药物名} comparison"`

**提取字段（每个竞争对手药物）：**

| 字段 | 说明 |
|------|------|
| 药物名称 | 通用名/代号 |
| 研发公司 | |
| 分子类型 | 小分子/抗体/其他 |
| 最高阶段 | 临床I/II/III/上市 |
| 适应症 | |
| 作用机制 | 正构/别构/不可逆等 |
| 关键临床数据 | 疗效/安全性亮点 |
| 特征点评 | 差异化/局限性 |

**竞争对手公司汇总：**

对每个主要竞争公司，输出：
1. 核心管线及阶段
2. 技术特征与差异化
3. 竞争力评价

---

## 数据源 E — 适应症与疾病关联

**主力来源：**

来源 1（Open Targets）：
- URL：`https://platform.opentargets.org/target/{UniProt ID}/associations`
- 提取：疾病关联评分、遗传证据、文献证据

来源 2（搜索）：
- 搜索词：`"{靶点名称} {基因符号} indication disease therapeutic area"`
- 搜索词：`"{靶点名称} {基因符号} rare disease orphan"`
- 搜索词：`"{靶点名称} biomarker companion diagnostic"`

**提取字段：**

| 字段 | 说明 |
|------|------|
| 主要适应症 | 3-5个核心领域 |
| 拓展适应症 | 潜在扩展方向 |
| 罕见病关联 | 如有 |
| 证据强度 | 遗传/功能/临床级别 |
| 生物标志物 | 伴随诊断可能性 |

---

## 数据源 F — 专利态势

**主力来源：**

来源 1（Google Patents）：
- 搜索：`https://patents.google.com/?q={靶点名称}+{基因符号}+inhibitor&sort=new`
- 提取：专利数量趋势、主要申请人、关键专利族

来源 2（搜索补充）：
- 搜索词：`"{靶点名称} {基因符号} patent landscape inhibitor 2024 2025"`
- 搜索词：`"{靶点名称} {基因符号} intellectual property freedom to operate"`

**提取字段：**

| 字段 | 说明 |
|------|------|
| 专利族总数 | 近5年 |
| 申请趋势 | 逐年/上升/平稳/下降 |
| 关键专利持有人 | Top 5 |
| 核心专利覆盖 | 骨架/用途/晶型/制剂 |
| 专利到期窗口 | 关键专利到期时间 |
| 自由实施空间 | 宽松/一般/受限 |

**专利拥挤度评分标准（1-10）：**
```
1-2: 蓝海，极少量专利
3-4: 较宽松，有空间
5-6: 一般，需规避设计
7-8: 拥挤，规避难度大
9-10: 极度拥挤，FTO风险高
```

---

## 数据源 G — 同源/家族靶点

**主力来源：**

来源 1（UniProt 相似蛋白）：
- 从 UniProt 页面"Similar proteins"获取

来源 2（搜索）：
- 搜索词：`"{靶点名称} {基因符号} homolog family paralog isoform selectivity"`
- 搜索词：`"{靶点名称} isoform selectivity challenge drug discovery"`

**提取字段：**

| 字段 | 说明 |
|------|------|
| 同源家族 | 所属家族名称 |
| 主要同源物 | 列出 + UniProt链接 |
| 同源性 | 序列相似度% |
| 选择性挑战 | 哪些同源物需要区分 |
| 已有的选择性方案 | 文献/专利中的策略 |

---

## 数据源 H — 安全性/毒性风险

**主力来源：**

来源 1（搜索 - On-target）：
- 搜索词：`"{靶点名称} {基因符号} knockout mouse phenotype"`
- 搜索词：`"{靶点名称} {基因符号} safety toxicity on-target adverse effect"`
- 搜索词：`"{靶点名称} {基因符号} essential gene CRISPR knockout"`

来源 2（搜索 - Off-target）：
- 搜索词：`"{靶点名称} {基因符号} off-target toxicity selectivity profile"`
- 搜索词：`"{靶点名称} inhibitor adverse event clinical trial safety"`

来源 3（数据库）：
- Open Targets Safety：`https://platform.opentargets.org/target/{UniProt ID}/safety`
- IUPHAR/BPS Guide to Pharmacology：`https://www.guidetopharmacology.org/GRAC/Search?search={基因符号}`

**提取字段：**

| 字段 | 说明 |
|------|------|
| On-target毒性 | 靶点抑制/激活的直接毒性 |
| 基因敲除表型 | 致死/亚致死/可耐受 |
| Off-target风险 | 已知脱靶及相关毒性 |
| 临床已观测AE | 临床试验中的不良反应 |
| 安全性窗口 | 预期治疗指数 |
| 需监测指标 | 临床前/临床需关注的biomarker |
| 黑框警告风险 | 预测是否可能触发 |

---

## 数据源 I — 前沿动态与综述 + 高引文献

**主力来源：**

搜索词：
- `"{靶点名称} {基因符号} review 2024 2025 drug discovery"`
- `"{靶点名称} {基因符号} breakthrough Nature Science Cell 2024 2025"`
- `"{靶点名称} {基因符号} resistance mechanism biomarker"`
- `"{靶点名称} {基因符号} PROTAC degrader molecular glue"`

**高引文献搜索：**

```
搜索词："{靶点名称} {基因符号} highly cited seminal paper Nature Science Cell"
搜索词："{靶点名称} {基因符号} drug discovery review chemical biology"
搜索词："{靶点名称} {基因符号} crystal structure inhibitor co-crystal landmark"
Google Scholar："{靶点名称} {基因符号}" 按引用数排序
PubMed："{靶点名称} {基因符号}" 筛选 Review + 高影响因子
```

**高引文献提取字段：**

| 字段 | 说明 |
|------|------|
| 标题 | 完整标题 |
| 作者 | 第一/通讯作者 |
| 期刊·年份 | 期刊名+发表年 |
| 引用数 | Google Scholar/Published 日期快照 |
| 核心贡献 | 一句话概括 |
| 推荐理由 | 为什么必读 |
| 主题分类 | 机制/结构/药化/临床/综述 |

**原有提取字段：**

| 字段 | 说明 |
|------|------|
| 近期重大进展 | 2024-2025关键发现 |
| 耐药机制 | 已知的获得性耐药 |
| 新技术方向 | PROTAC/分子胶/别构等 |
| 关键综述 | 2-3篇推荐阅读 |

---

## 采集优先级与并发策略

| 优先级 | 数据源 | 可并发 |
|--------|--------|--------|
| P0（必须） | A 基础信息 + B 结构信息 | A+B |
| P0（必须） | C 通路 + D 管线 | C+D |
| P1（重要） | E 适应症 + F 专利 | E+F |
| P1（重要） | G 同源靶点 + H 安全性 | G+H |
| P2（补充） | I 前沿动态 | 单独 |

> 每个数据源至少获取到核心字段才算完成，缺失字段标注"数据未获取"而非留空。