---
name: research-paper-writer
description: Complete research paper generation skill supporting IEEE/ACM/Nature formats. Provides paper structure generation, abstract writing, introduction, methods, results, discussion, and reference management.
license: MIT License
metadata:
    skill-author: academic-assistant
    version: 1.0.0
    created: 2026-03-14
---

# Research Paper Writer

## Overview

完整论文生成技能，支持 IEEE/ACM/Nature 等格式，提供论文结构生成、各部分写作、参考文献管理等功能。

## Supported Templates

### Scientific Data (Nature)

**结构**:
1. Abstract (150-200 字)
2. Background & Summary
3. Methods
4. Data Records
5. Technical Validation
6. Usage Notes
7. Code Availability
8. References

**要求**:
- 总字数：~3000 字
- 图表：5+ 图，2+ 表
- 引用格式：Nature 格式

---

### Nature Communications

**结构**:
1. Abstract (150 字)
2. Introduction
3. Results
4. Discussion
5. Methods
6. Data Availability
7. Code Availability
8. References

**要求**:
- 总字数：~5000 字
- 图表：6+ 图，2+ 表
- 引用格式：Nature 格式

---

### IEEE Conference

**结构**:
1. Abstract (150-200 字)
2. Introduction
3. Related Work
4. Methods
5. Experiments
6. Results & Discussion
7. Conclusion
8. References

**要求**:
- 页数：6-8 页
- 图表：4+ 图
- 引用格式：IEEE 格式

---

### PNAS

**结构**:
1. Abstract (250 字)
2. Significance Statement
3. Introduction
4. Results
5. Discussion
6. Materials & Methods
7. Acknowledgments
8. References

**要求**:
- 总字数：~5000 字
- 图表：5+ 图
- 引用格式：PNAS 格式

---

## Usage

### 基本使用

```bash
# 生成完整论文
python research_paper_writer.py --template scientific_data --output paper.md

# 生成特定部分
python research_paper_writer.py --section introduction --output intro.md

# 生成摘要
python research_paper_writer.py --section abstract --output abstract.md

# 格式检查
python research_paper_writer.py --action check --input paper.md --template scientific_data
```

---

### 高级使用

```bash
# 批量生成
python research_paper_writer.py --template ieee_conference --output-dir papers/

# 润色已有论文
python research_paper_writer.py --action polish --input draft.md --output polished.md

# 生成参考文献
python research_paper_writer.py --action generate_references --input paper.md --style APA
```

---

## Paper Structure

### 摘要 (Abstract)

**写作要点**:
- 背景（1-2 句）
- 方法（1-2 句）
- 结果（2-3 句）
- 结论（1 句）

**字数限制**: 150-250 字

**示例**:
```
摘要：本研究探讨了 AI 辅助在心理学研究中的应用效果。采用随机对照试验设计，N=200 名研究者参与。结果显示，AI 辅助组的研究效率显著提升（d=0.65），论文质量评分更高（p<.01）。结论：AI 辅助能有效提升心理学研究效率和质量。

关键词：AI 辅助；心理学研究；研究效率；随机对照试验
```

---

### 引言 (Introduction)

**写作结构**:
1. 研究背景（宽）
2. 文献综述（窄）
3. 研究空白
4. 研究问题
5. 研究假设
6. 研究意义

**字数限制**: 800-1200 字

**写作技巧**:
- 漏斗式结构（从宽到窄）
- 每段一个主题
- 引用关键文献
- 明确指出研究空白

---

### 方法 (Methods)

**写作内容**:
1. 研究设计
2. 参与者
3. 材料/工具
4. 程序
5. 数据分析

**字数限制**: 1000-1500 字

**写作要点**:
- 详细到可重复
- 使用标准术语
- 包含伦理审批
- 说明统计方法

**示例**:
```
2.1 研究设计

本研究采用 2（AI 辅助：有/无）× 2（任务类型：文献搜索/数据分析）混合实验设计。AI 辅助为被试间变量，任务类型为被试内变量。因变量包括研究效率（完成时间）和研究质量（专家评分）。

2.2 参与者

通过 G*Power 3.1 计算，设定效应量 f=0.25，α=0.05，统计功效 1-β=0.80，计算得所需样本量为 128 人。考虑到 20% 的流失率，实际招募 160 名心理学研究生（M_age=24.5, SD=2.3, 65% 女性）。参与者随机分配到 AI 辅助组（n=80）和对照组（n=80）。
```

---

### 结果 (Results)

**写作内容**:
1. 描述统计
2. 操纵检查
3. 假设检验
4. 补充分析

**字数限制**: 1000-1500 字

**写作要点**:
- 客观描述
- 先文字后图表
- 报告统计值（t, F, p, d/η²）
- 包含效应量

**示例**:
```
3.1 描述统计

表 1 显示了各组的描述统计结果。AI 辅助组的平均完成时间（M=45.2 分钟，SD=8.3）显著短于对照组（M=62.5 分钟，SD=10.2）。

3.2 假设检验

为检验 AI 辅助对研究效率的影响，进行 2×2 混合 ANOVA 分析。结果显示，AI 辅助主效应显著，F(1, 158)=125.6, p<.001, η²=0.44。AI 辅助组的研究效率显著高于对照组（d=0.89, 95% CI [0.65, 1.13]）。
```

---

### 讨论 (Discussion)

**写作结构**:
1. 主要发现总结
2. 与现有研究对比
3. 理论贡献
4. 实践意义
5. 局限性
6. 未来方向

**字数限制**: 1500-2000 字

**写作要点**:
- 回应研究问题
- 客观解释发现
- 承认局限性
- 提出具体建议

---

### 结论 (Conclusion)

**写作内容**:
- 总结主要发现
- 强调贡献
- 提出建议

**字数限制**: 300-500 字

---

## Citation Styles

### APA 第 7 版（心理学）

**文内引用**:
- 单作者：(Smith, 2025)
- 双作者：(Smith & Jones, 2025)
- 三作者+：(Smith et al., 2025)

**参考文献**:
```
Author, A. A. (Year). Title of article. Title of Journal, Volume(Issue), Pages. DOI
```

---

### Nature 格式

**文内引用**:
- 上标数字：研究结果表明¹

**参考文献**:
```
1. Author, A. A. et al. Title of article. Journal Volume, Pages (Year).
```

---

### IEEE 格式

**文内引用**:
- 方括号数字：研究结果表明 [1]

**参考文献**:
```
[1] Author, A. A., "Title of article," Journal, vol. x, no. x, pp. xxx-xxx, Abbrev. Month. Year.
```

---

## Quality Checks

### 结构检查

**检查项目**:
- [ ] IMRAD 结构完整
- [ ] 各部分字数符合要求
- [ ] 图表数量符合要求
- [ ] 参考文献数量充足（30-50 篇）

---

### 内容检查

**检查项目**:
- [ ] 研究问题明确
- [ ] 方法详细可重复
- [ ] 结果客观准确
- [ ] 讨论深入全面
- [ ] 结论简洁有力

---

### 格式检查

**检查项目**:
- [ ] 引用格式正确
- [ ] 参考文献列表完整
- [ ] 图表格式规范
- [ ] 字数符合要求
- [ ] DOI 包含

---

## Best Practices

### 写作建议

1. **先写再改**
   - 初稿不求完美
   - 完成比完美重要
   - 多次修改润色

2. **图表驱动**
   - 先规划图表
   - 图表引导写作
   - 确保质量

3. **文献支撑**
   - 充分文献搜索
   - 引用关键文献
   - 避免过度引用

4. **寻求反馈**
   - 导师审阅
   - 同行评议
   - 多次修改

---

### 避免错误

1. **结构问题**
   - ❌ 缺少关键部分
   - ✅ 遵循 IMRAD 结构

2. **内容问题**
   - ❌ 方法不详细
   - ✅ 详细到可重复

3. **引用问题**
   - ❌ 格式不一致
   - ✅ 使用引用管理工具

4. **语言问题**
   - ❌ 口语化表达
   - ✅ 学术风格

---

## Integration

### 与 scientific-writing 配合

```
research-paper-writer: 负责整体结构和内容生成
scientific-writing: 负责详细写作指导
academic-writing: 负责语言润色
```

### 与 citation-management 配合

```
citation-management: 负责文献搜索和引用生成
research-paper-writer: 负责论文写作和引用插入
```

---

## Examples

### 示例 1: 生成 Scientific Data 论文

```bash
python research_paper_writer.py \
  --template scientific_data \
  --topic "CPWBD-2025: A National Wellbeing Dataset from China" \
  --output paper.md
```

**输出**:
- 完整论文草稿
- 参考文献列表
- 图表清单
- 格式检查报告

---

### 示例 2: 生成摘要

```bash
python research_paper_writer.py \
  --section abstract \
  --topic "AI 辅助心理学研究效率提升" \
  --style APA \
  --output abstract.md
```

**输出**:
```
摘要：本研究探讨了 AI 辅助在心理学研究中的应用效果。采用随机对照试验设计，N=200 名研究者参与。结果显示，AI 辅助组的研究效率显著提升（d=0.65），论文质量评分更高（p<.01）。结论：AI 辅助能有效提升心理学研究效率和质量。

关键词：AI 辅助；心理学研究；研究效率；随机对照试验
```

---

## References

- Scientific Data: https://www.nature.com/sdata/
- Nature Communications: https://www.nature.com/ncomms/
- IEEE: https://ieeeauthorcenter.ieee.org/
- APA Style: https://apastyle.apa.org/

---

**技能版本**: v1.0.0  
**创建时间**: 2026-03-14  
**维护者**: academic-assistant  
**下次更新**: 功能改进时

---

*完整论文生成，从模板开始！*📝✨
