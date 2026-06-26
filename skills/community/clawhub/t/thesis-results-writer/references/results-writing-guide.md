# Chinese Results Chapter Writing Guide

This reference is derived and paraphrased from the local source `4result.txt`. Use it to write only the Results/Chapter Four/研究结果 section.

## Table of Contents

1. Core Function of Results Chapter
2. Data Availability Rules
3. Result Type Decision Rules
4. Standard Chapter Structures
5. Chapter Opening
6. Results Writing Style
7. Quantitative Results
8. Qualitative Results
9. Mixed Methods Results
10. Literature Review and Intervention-Scheme Results
11. Tables and Figures
12. Statistical Reporting Templates
13. Additional Analyses
14. Chapter Summary
15. Chinese Templates
16. Revision Checklist

## Core Function of Results Chapter

The results chapter presents and analyzes data clearly and comprehensively. It should report what the data show, not explain why the findings occurred or how they compare with the literature.

Core rules:

- Focus on objective presentation.
- Avoid value judgments, broad generalizations, and recommendations.
- Save interpretation, implications, comparison with prior studies, and limitations for the discussion chapter.
- Do not restate the theoretical framework or methodology in detail.
- Plan tables and figures before writing the narrative.

For qualitative papers, some schools allow combined "results and discussion" chapters. Unless the user asks for that format, keep results separate from discussion.

## Data Availability Rules

Never invent:

- Sample size
- Mean, standard deviation, frequency, percentage
- p value, effect size, confidence interval
- Correlation or regression coefficient
- Theme, code, participant quote, or case detail
- Statistical significance or non-significance

If the user provides no actual results, output:

- A complete results chapter framework
- Table shells
- Placeholder sentences
- A list of exact data needed to complete the chapter

Placeholder examples:

> 表4-1呈现了样本的人口学特征。结果显示，……（此处补充性别、年级、专业等频数和百分比）。

> 对……与……进行Pearson相关分析，结果见表4-3。……（此处补充r值、p值及方向）。

> 通过对访谈资料进行编码分析，本研究形成了……个主题：……（此处补充主题名称和代表性引语）。

## Result Type Decision Rules

Choose the results-chapter pattern from the user's supplied materials:

- Quantitative results: the user provides variables, scales, sample size, descriptive statistics, SPSS/R/Excel output, p values, coefficients, test names, hypotheses, or tables.
- Qualitative results: the user provides interviews, observations, documents, participant IDs, cases, codes, categories, themes, subthemes, representative excerpts, or field notes.
- Mixed methods results: the user provides both numeric analyses and qualitative themes, or the research questions explicitly require quantitative description plus qualitative explanation.
- Literature-review results: the user has no primary data but has literature retrieval records, included studies, coding categories, themes, or evidence tables.
- Intervention-scheme results: the study designs a psychological intervention but does not implement it. Present the designed scheme as an output, not as effectiveness evidence.

When the user's declared method and available data conflict, follow the available evidence and state the assumption. For example, if the user says "问卷研究" but supplies only interview themes, write a qualitative results structure or ask for the missing survey results if necessary.

## Standard Chapter Structures

### Quantitative Results Chapter

```markdown
第四章 研究结果

4.1 本章导言
4.2 样本基本情况
4.3 描述统计与信度分析
4.4 研究问题/研究假设检验
4.4.1 研究问题一/假设一
4.4.2 研究问题二/假设二
4.4.3 研究问题三/假设三
4.5 附加分析
4.6 本章小结
```

### Qualitative Results Chapter

```markdown
第四章 研究结果

4.1 本章导言
4.2 资料整理与主题形成概况
4.3 主题一：……
4.3.1 子主题一
4.3.2 子主题二
4.4 主题二：……
4.5 主题三：……
4.6 典型案例或差异表现
4.7 本章小结
```

Alternative qualitative organizations:

- By themes: best for interview/focus-group studies.
- By participants: useful when each participant or case is central.
- By cases: useful for case study and multiple-case study.
- By phases: useful for process studies or intervention implementation.
- By data sources: useful when documents, observations, and interviews produce distinct findings.

### Mixed Methods Results Chapter

```markdown
第四章 研究结果

4.1 本章导言
4.2 定量研究结果
4.2.1 样本基本情况
4.2.2 描述统计
4.2.3 研究问题/假设检验
4.3 质性研究结果
4.3.1 主题一
4.3.2 主题二
4.3.3 主题三
4.4 定量与质性结果对应关系
4.5 本章小结
```

## Chapter Opening

The opening should be one or two paragraphs and act as an advance organizer.

Quantitative template:

> 本章主要呈现本研究的数据分析结果。根据研究目的和研究问题，本文首先报告样本基本情况和主要变量的描述统计结果，其次依次呈现……、……和……的统计分析结果，最后对附加分析结果进行说明。

Qualitative template:

> 本章主要呈现访谈/观察/文本资料的分析结果。研究者通过对资料进行反复阅读、编码和主题归纳，形成了……个主要主题。以下将围绕各主题及其子主题展开呈现，并结合代表性资料片段说明研究发现。

Mixed template:

> 本章按照混合研究设计的逻辑呈现研究结果。首先报告问卷调查所得的定量结果，其次呈现访谈资料归纳出的质性主题，最后对两类结果之间的对应关系作客观说明。

## Results Writing Style

Results chapters should be plain, consistent, and somewhat repetitive. Similar analyses should use similar sentence structures so readers can scan the chapter easily.

Style rules:

- State the research question or hypothesis before the result.
- Mention the relevant table or figure before displaying it.
- Put statistics near the end of the sentence when doing so improves readability.
- Use the conceptual variable name rather than only the instrument name. For example, write "考试焦虑水平" rather than only "考试焦虑量表得分" when the sentence discusses the construct.
- Report significant and non-significant results with equal clarity.
- Avoid causal wording unless the design truly supports causal inference.
- Avoid phrases such as "证明了", "充分说明", "效果显著提升" unless the design and data justify them.
- Do not compare with previous literature in a separate paragraph; that belongs in the discussion chapter.
- Do not describe every cell in a table. Highlight the values that answer the research question.

Useful neutral verbs:

- "结果显示"
- "表明"
- "呈现出"
- "达到/未达到统计显著水平"
- "支持/未支持该假设"
- "形成了……个主题"
- "主要集中在……方面"

## Quantitative Results

### Descriptive Statistics

Usually report first:

- Sample demographic characteristics: frequency and percentage.
- Main variables: mean, standard deviation, minimum, maximum.
- Reliability if it belongs in results: Cronbach's α.
- Normality or assumptions if required.

Template:

> 表4-1呈现了样本基本情况。由表可见，本研究有效样本共……人，其中……。总体来看，样本在……方面具有……特点。

> 表4-2呈现了主要研究变量的描述统计结果。……的平均分为……，标准差为……；……的平均分为……，标准差为……。

### Reporting by Research Question or Hypothesis

Use this six-step pattern for each quantitative research question/hypothesis:

1. Restate the research question or hypothesis exactly or almost exactly.
2. Refer to the table or figure that contains the relevant statistics.
3. Highlight the key data in the table or figure.
4. State the statistical procedure used.
5. State the result and whether it supports the question/hypothesis.
6. Move to the next question/hypothesis.

Template:

> 研究问题一为：……。为回答该问题，本研究采用……分析，结果见表4-3。结果显示，……。因此，研究问题一的结果表明……。

Hypothesis template:

> 假设一认为……。为检验该假设，本研究采用……分析。结果显示，……，说明……。因此，假设一得到支持/未得到支持。

Repeat this structure for every research question or hypothesis. Do not combine several unrelated hypotheses into one long paragraph unless the school format explicitly requires it.

### Assumption Checks

Discuss assumptions before the relevant inferential test when needed:

- Normality
- Homogeneity of variance
- Interval/continuous data
- Independence
- Expected cell counts for chi-square
- Multicollinearity for regression

Template:

> 在进行……分析前，研究者对数据进行了前提检验。结果显示，……满足/不满足……要求。鉴于……，本研究采用……方法进行后续分析。

### Additional Analyses

Use only for analyses not directly tied to research questions:

- Demographic differences not planned as hypotheses
- Extra correlations among predictors
- Factor analysis of instruments
- Post hoc or sensitivity analyses
- Modified instrument reanalysis

Template:

> 除上述研究问题外，本文进一步对……进行了附加分析。该分析旨在补充说明……，结果见表4-…。结果显示……。

## Qualitative Results

### Theme-Based Reporting

For each theme:

1. Name the theme clearly.
2. Define what the theme means.
3. Present subthemes if any.
4. Support with short anonymized excerpts if supplied.
5. Report differences or exceptions when relevant.
6. Avoid over-interpreting; leave implications for discussion.

Theme template:

> 主题一：……
>
> 该主题主要反映了参与者在……方面的共同经验。资料显示，多数参与者提到……。例如，P3表示："……"。P7也提到："……"。这些资料表明，……是参与者经验中的重要组成部分。

Subtheme template:

> 子主题一：……
>
> 在该子主题中，参与者主要描述了……。这一表现集中体现在……、……和……三个方面。

### Case-Based Reporting

For case studies:

1. Present each case background briefly.
2. Report within-case findings.
3. Compare cases in a cross-case section.
4. Use tables or matrices when helpful.

Template:

> 案例A的资料显示，……。从问题形成过程来看，……；从应对方式来看，……；从支持资源来看，……。

Cross-case template:

> 跨案例比较显示，三个案例在……方面具有共同特征，但在……方面存在差异。具体而言，案例A更突出……，案例B更强调……，案例C则表现为……。

### Qualitative Analysis Process in Results

A brief statement is useful, but do not repeat the whole methodology.

Template:

> 研究者对访谈文本进行编码后，形成……个初始编码，并进一步归纳为……个类别和……个主题。表4-1呈现了主题和子主题结构。

Suggested table:

| 主题 | 子主题 | 代表性编码 | 资料来源 |
|---|---|---|---|

### Theme Formation Process

When the user needs to describe how themes emerged, use a concise results-focused version of the process:

1. Repeatedly read interview transcripts, observation notes, or documents.
2. Write analytic memos or reflective notes.
3. Conduct participant/member checking if the user has done it.
4. Reduce raw data into initial codes.
5. Sort codes into categories and themes.
6. Mark themes, quotes, and speakers consistently.
7. Continue coding across all data sources or participants.
8. Identify subthemes, exceptions, and cross-case similarities.

Results wording:

> 通过对资料的反复阅读和编码，研究者首先形成……个初始编码，随后将意义相近的编码整合为……个类别，并进一步归纳出……个核心主题。主题结构见表4-…。 

If the user has not conducted member checking or cross-checking, do not claim it was done. Use "可在论文中说明研究者通过反复阅读和同伴讨论提高编码稳定性" only when the user has actually done or plans to do that work.

## Mixed Methods Results

Keep quantitative and qualitative results distinguishable unless the user requests integrated reporting.

Sequential explanatory template:

> 定量结果显示……。为进一步理解该结果，研究者对……名参与者进行了访谈。质性资料显示，参与者主要从……、……和……三个方面解释了这一现象。

Joint display table:

| 定量结果 | 质性主题 | 对应说明 |
|---|---|---|

Avoid:

- Discussing implications too deeply.
- Treating interviews as proving causality.
- Repeating all quantitative numbers inside qualitative sections.

## Literature Review and Intervention-Scheme Results

### Literature Review/Systematic Review Results

If the paper itself is a literature review or systematic review, results may include:

- Search and screening results
- Included literature characteristics
- Theme categories
- Evidence patterns
- Research gaps

Template:

> 经检索共获得文献……篇，剔除重复文献……篇，依据纳入与排除标准筛选后，最终纳入……篇文献。纳入文献主要集中在……、……和……三个方面。

### Intervention-Scheme Design Results

If no intervention was implemented, do not write effectiveness results. Write scheme-design output:

```markdown
第四章 干预方案设计结果

4.1 方案设计依据
4.2 干预对象与目标
4.3 干预原则
4.4 总体流程
4.5 分次活动设计
4.6 实施条件与评价设想
4.7 本章小结
```

Mandatory caution:

> 本研究仅呈现干预方案设计结果，未实际实施干预，因此本章不报告干预效果数据。

## Tables and Figures

Table rules:

- Number every table in order.
- Give every table a clear title.
- Mention every table in text before showing it.
- Use headings such as N, M, SD, df, t, F, r, β, p where appropriate.
- Align decimals and usually keep two decimal places unless the school requires otherwise.
- Use notes for abbreviations and probability levels.
- Use Arabic table numbers such as "表4-1".
- The title should identify the variables, groups, or analysis shown in the table.
- Use a dash for unavailable or inapplicable cells rather than leaving them ambiguous.
- Explain uncommon abbreviations in notes.
- Include effect sizes where appropriate, such as Cohen's d, η², R², OR, or Cramer's V.
- Do not place many tables consecutively without explanatory text.

Table components:

- Number
- Title
- Headings
- Body
- Notes

Probability note example:

> 注：* p < .05，** p < .01，*** p < .001。

Common table shells:

Descriptive statistics:

| 变量 | N | M | SD | 最小值 | 最大值 |
|---|---:|---:|---:|---:|---:|
| …… | …… | …… | …… | …… | …… |

Correlation matrix:

| 变量 | 1 | 2 | 3 | M | SD |
|---|---:|---:|---:|---:|---:|
| 1. …… | 1 |  |  | …… | …… |
| 2. …… | …… | 1 |  | …… | …… |
| 3. …… | …… | …… | 1 | …… | …… |

Group comparison:

| 组别 | N | M | SD | t/F | p | 效应量 |
|---|---:|---:|---:|---:|---:|---:|
| …… | …… | …… | …… | …… | …… | …… |

Regression:

| 预测变量 | B | SE | β | t | p |
|---|---:|---:|---:|---:|---:|
| …… | …… | …… | …… | …… | …… |

Qualitative themes:

| 主题 | 子主题 | 代表性资料 | 资料来源 |
|---|---|---|---|
| …… | …… | "……" | P1 |

Figure rules:

- Use figures for trends, scatter plots, moderation effects, cluster analysis, path analysis, structural equation models, or qualitative process models.
- Mention the figure before presenting it.
- Explain what the figure shows without over-interpreting.

## Statistical Reporting Templates

### t Test

> 独立样本t检验结果显示，……组在……上的得分（M = ……, SD = ……）高于/低于……组（M = ……, SD = ……），差异达到/未达到统计显著水平，t(df) = ……, p = ……。

### ANOVA

> 单因素方差分析结果显示，不同……群体在……上的差异达到/未达到统计显著水平，F(df1, df2) = ……, p = ……，η² = ……。进一步事后比较显示，……。

### Chi-Square

> 卡方检验结果显示，……与……之间存在/不存在显著关联，χ²(df, N = ……) = ……, p = ……。Cramer's V = ……，表明关联强度为……。

### Correlation

> Pearson相关分析结果显示，……与……呈显著正相关/负相关，r(df) = ……, p = ……。

If non-significant:

> ……与……之间相关不显著，r(df) = ……, p = ……。

### Regression

> 回归分析结果显示，……能够显著预测……，β = ……, t = ……, p = ……；模型整体达到/未达到统计显著水平，F(df1, df2) = ……, p = ……，R² = ……。

### Reliability

> 信度分析结果显示，……量表的Cronbach's α系数为……，各维度α系数介于……至……之间，说明量表在本研究样本中具有……内部一致性。

## Additional Analyses

Report additional analyses only after planned research-question results.

Appropriate wording:

> 为进一步了解……，本研究进行了附加分析。需要说明的是，该部分分析不属于原研究假设检验，而是对主要结果的补充。

## Chapter Summary

The summary should synthesize findings at a higher level than the preceding table-by-table reporting.

Quantitative template:

> 本章对研究数据进行了呈现与分析。首先，本文报告了样本基本情况和主要变量的描述统计结果；其次，围绕研究问题依次进行了……、……和……分析。结果显示，……。上述结果为下一章进一步讨论研究发现提供了依据。

Qualitative template:

> 本章呈现了质性资料分析结果。通过对访谈/文本资料的编码分析，本文归纳出……个主题，分别为……、……和……。这些主题反映了参与者在……方面的主要经验和差异表现。下一章将结合相关理论和既有研究对上述结果进行进一步讨论。

Mixed template:

> 本章分别呈现了定量和质性研究结果。定量结果显示……；质性结果进一步呈现了……。下一章将对两类结果进行综合解释和讨论。

## Chinese Result Chapter Templates

### Quantitative Full Skeleton

```markdown
第四章 研究结果

4.1 本章导言
本章主要呈现……

4.2 样本基本情况
表4-1呈现……

4.3 主要变量描述统计与信度分析
表4-2呈现……

4.4 研究假设检验
4.4.1 假设一检验
……

4.4.2 假设二检验
……

4.5 附加分析
……

4.6 本章小结
……
```

### Qualitative Full Skeleton

```markdown
第四章 研究结果

4.1 本章导言
……

4.2 主题形成概况
……

4.3 主题一：……
……

4.4 主题二：……
……

4.5 主题三：……
……

4.6 本章小结
……
```

## Revision Checklist

Before finalizing, check:

- Is the chapter limited to results rather than discussion?
- Are all numbers, themes, quotes, and statistical outputs supplied by the user?
- Does the structure match the research type?
- Are descriptive statistics presented before inferential tests?
- Is each research question or hypothesis addressed explicitly?
- Are tables/figures referenced before presentation?
- Are statistical symbols and p values reported consistently?
- Are non-significant results reported clearly?
- Are qualitative themes supported by evidence when available?
- Is additional analysis separated from planned analyses?
- Does the summary synthesize results and lead to the discussion chapter?
