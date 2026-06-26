---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: d0687d7718835bad5273d94957cb45ab
    PropagateID: d0687d7718835bad5273d94957cb45ab
    ReservedCode1: 3046022100a91358d8db1901c0f956669d53769a47ae26d72d3fc697668e073b85004f6a3f022100840ae22fb7c9d3084af81b50f218a3576d0614f8c00bf696d01dc7d69659efbe
    ReservedCode2: 304602210093143fc821eb73a3e432b7266a2d9a88bd074ee0f0421a3195e9a1c7a14ebdf2022100c66d747fe49345a76295f0d07c88a03b0aa09634beb3ff8850b035b0c30de595
description: 临床医学顶刊文献检索与分析。当用户要求检索医学文献、查找临床研究论文、搜索特定疾病或治疗方法相关文献、或者需要基于PubMed数据库进行系统文献综述时使用。支持JCR分区筛选、影响因子排序和综合相关性排序。
name: pubmed-literature-search
---

# PubMed临床医学顶刊文献检索与分析系统

## 概述

本技能提供完整的临床医学文献检索服务，基于PubMed数据库，结合JCR期刊分区数据进行智能筛选和排序，帮助用户快速定位高质量医学文献。

## 工作流程

### 第一步：需求分析与检索词拆解

**核心任务**：
- 分析用户提供的临床医学主题或研究问题
- 将复杂主题拆解为精准的PubMed检索词
- 识别关键术语、同义词、医学主题词(MeSH Terms)

**检索词构建原则**：
- 使用MeSH主题词确保检索准确性
- 添加同义词和缩写扩大检索范围
- 使用布尔运算符(AND/OR/NOT)组合检索词
- 包含研究类型限定词如"Randomized Controlled Trial"、"Meta-Analysis"等

**检索示例**：
| 用户主题 | 拆解检索词 |
|---------|-----------|
| 糖尿病心血管并发症 | ("Diabetes Mellitus"[MeSH] OR "Diabetic Cardiomyopathies"[MeSH]) AND ("Cardiovascular Diseases"[MeSH] OR "Myocardial Infarction") |
| PD-1抑制剂治疗肺癌 | ("PD-1" OR "Programmed Cell Death 1 Receptor") AND ("Lung Neoplasms"[MeSH] OR "NSCLC") AND ("Immunotherapy"[MeSH] OR "Immune Checkpoint Inhibitors") |

**时间范围**：
- 用户未指定时，默认检索**近5年**文章
- 用户可指定具体年份范围（如2019-2024）

**用户确认环节**：
- 将拆解后的检索词呈现给用户
- 等待用户确认或修改
- 用户确认后再执行实际检索

---

### 第二步：JCR分区与影响因子匹配

**数据来源**：
- 使用用户提供的JCR Excel文件（2025年最新完整版）
- 提取字段：Journal Name, Abbreviated Journal, JIF Quartile, JIF 2024

**权重赋值规则**：
| JCR分区 | 权重分数 |
|--------|---------|
| Q1 | 40分 |
| Q2 | 30分 |
| Q3 | 20分 |
| Q4 | 10分 |

> ⚠️ **本地规则（用户指定，不可覆盖JCR数据）：**
> - **Int J Surg（International Journal of Surgery）** → 分区修正为 **Q2**（权重30分，而非JCR原始数据中的Q1）

**匹配流程**：
1. 从检索结果中提取发表期刊名称
2. 在JCR数据库中匹配期刊全称或缩写
3. 记录匹配到的分区和影响因子
4. 未匹配期刊标记为"未收录"

---

### 第三步：综合排序与初筛

**排序维度**：
1. **相关性分数**（PubMed Relevance Score）
2. **JCR分区权重**（Q1>Q2>Q3>Q4）
3. **发表年份**（最新优先）

**综合评分公式**：
```
综合分数 = 相关性分数 × 0.4 + 分区权重 × 0.35 + 年份标准化分数 × 0.25
```
- 年份标准化分数：(发表年份 - 最老年份) / (最新年份 - 最老年份) × 100

**初筛规则**：
- 从所有检索结果中选取**综合排序前50篇**
- 优先选择有摘要的文献
- 确保Q1区文章占比不低于60%（若Q1文章不足50篇，则选取所有Q1+按需补充Q2）

---

### 第四步：深度分析与内容提取

**分析对象**：综合排序前50篇文献

**分析内容**：

1. **标题分析**：
   - 提取研究类型（RCT、Meta-Analysis、Review、Cohort Study等）
   - 识别干预措施、暴露因素、结局指标
   - 判断与用户需求的匹配度

2. **摘要分析**：
   - 研究目的与方法概述
   - 样本量与研究设计
   - 主要发现与结论摘要

3. **关键词分析**：
   - 提取高频关键词
   - 识别研究热点主题
   - 统计MeSH主题词分布

**统计输出**：

1. **研究类型分布**：
   | 类型 | 数量 | 占比 |
   |-----|------|-----|
   | Meta-Analysis | X | X% |
   | Randomized Controlled Trial | X | X% |
   | Systematic Review | X | X% |
   | Cohort Study | X | X% |
   | Case-Control Study | X | X% |
   | Other | X | X% |

2. **期刊来源分布**（前10名）

3. **发表年份趋势**

**最终输出：Top 10 文章清单**

| 排名 | 标题 | 期刊 | 年份 | JCR分区 | IF | 简要内容 |
|-----|------|------|------|--------|-----|---------|
| 1 | [文章标题] | [期刊名] | 2024 | Q1 | 45.5 | [2-3句核心内容] |
| ... | ... | ... | ... | ... | ... | ... |

---

### 第五步：范围调整与重新筛选

**可调整参数**：

1. **时间范围扩展**：
   - 扩大至近10年
   - 自定义年份区间

2. **分区筛选**：
   - 仅Q1
   - Q1+Q2
   - 全部分区

3. **研究类型筛选**：
   - 仅Meta-Analysis
   - 仅RCT
   - 仅Review

4. **排序方式调整**：
   - 仅按相关性
   - 仅按JCR分区
   - 仅按年份
   - 自定义权重组合

**执行方式**：
- 用户提出调整需求后，重新执行筛选和排序
- 生成新的Top 50列表和Top 10输出

---

## 技术实现

### PubMed API调用

使用NCBI Entrez API进行文献检索：
- 检索接口：`ESearch`
- 摘要获取：`ESummary` 或 `EFetch`
- 支持批量获取（每次最多1000篇）

### JCR数据处理

使用pandas处理Excel文件：
- 建立期刊名称到JCR分区的快速查询表
- 支持模糊匹配和精确匹配
- 处理期刊重命名和合并情况

### 排序算法

```python
def calculate_composite_score(relevance, jcr_quartile, year, year_range):
    quartile_weight = {'Q1': 40, 'Q2': 30, 'Q3': 20, 'Q4': 10}
    q_score = quartile_weight.get(jcr_quartile, 0)
    year_score = (year - year_range[0]) / (year_range[1] - year_range[0]) * 100 if year_range[1] != year_range[0] else 50
    return relevance * 0.4 + q_score * 0.35 + year_score * 0.25
```

---

## 输出格式

### 完整报告结构

```
## 文献检索报告

**检索主题**：[用户主题]
**检索词**：[确认的检索词]
**时间范围**：[年 - 年]
**检索日期**：[执行日期]

---

### 检索结果概览
- 总检索结果：XXX篇
- 匹配JCR数据：XXX篇
- Q1区文章：XXX篇
- Q2区文章：XXX篇

### Top 10 高质量文献

[详细表格]

### 研究热点分析
[关键词云/词频统计]

### 研究类型分布
[饼图/柱状图]

---
```

---

## 注意事项

1. **检索词准确性**：务必与用户确认检索词后再执行检索
2. **时间范围**：用户未指定时明确告知默认5年设定
3. **JCR数据时效**：使用最新的JCR数据文件
4. **批量限制**：PubMed API有使用限制，大批量检索需分批执行
5. **结果验证**：对关键文献的PMID进行二次验证

---

## 使用场景示例

**场景1：新手研究者**
> 用户："帮我检索一下关于CAR-T细胞治疗淋巴瘤的文献"
> → 自动拆解检索词 → 用户确认 → 执行检索 → 输出Top 10文献

**场景2：系统综述准备**
> 用户："我想做关于二甲双胍在糖尿病中心血管保护作用的Meta-Analysis"
> → 提供系统性检索词 → 侧重筛选Meta-Analysis和Systematic Review → 详细输出研究方法相关文献

**场景3：临床指南更新**
> 用户："查找近3年关于PD-1/PD-L1抑制剂治疗非小细胞肺癌的最新临床试验"
> → 限定时间范围 → 筛选RCT和Phase III研究 → 按年份排序