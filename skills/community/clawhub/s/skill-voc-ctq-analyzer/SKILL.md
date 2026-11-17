---
name: CTQ分析技能
slug: voc-ctq-analyzer
displayName: CTQ分析技能
description: 将客户声音(VOC)转化为关键质量特性(CTQ)的分析工具；支持文本分析、需求提取、映射关联、可视化报告生成；当用户需要分析客户反馈、提炼产品需求、确定质量改进优先级时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# VOC-CTQ 分解工具

## 任务目标
- 本 Skill 用于：将客户声音(VOC)分解为关键质量特性(CTQ)，支持需求分析、映射关联、优先级评估和可视化展示
- 能力包含：VOC录入与分析、关键词提取、需求分类、CTQ定义与映射、优先级评分、可视化报告生成
- 触发条件：用户需要分析客户反馈文本、提炼产品/服务质量需求、建立VOC-CTQ映射关系、生成质量改进报告

## 前置准备
- 依赖说明：jieba(中文分词)、pyecharts(可视化)、snownlp(情感分析)
- 非标准文件/文件夹准备：
  - 输入数据：客户反馈文本文件(JSON/CSV/TXT格式)
  - 字典文件(如需要)：用户可提供自定义分词词典 `user_dict.txt`

## 操作步骤

### 标准流程

1. **VOC数据录入**
   - 手动输入：`python scripts/voc_analyzer.py --mode input`
   - 文件导入：`python scripts/voc_analyzer.py --mode import --file <path>`
   - 支持格式：JSON(推荐)、CSV、TXT(每行一条反馈)

2. **文本分析与关键词提取**
   - 命令：`python scripts/voc_analyzer.py --mode analyze --input <data.json> --output <result.json>`
   - 功能：分词、词性标注、关键词提取、情感分析、需求分类
   - 输出：包含分析结果的JSON文件

3. **CTQ候选提取与确认**
   - 命令：`python scripts/voc_analyzer.py --mode extract-ctq --input <analyzed.json> --output <ctq.json>`
   - 功能：基于词频和重要性提取CTQ候选
   - 用户确认：可编辑输出文件调整CTQ

4. **VOC-CTQ映射建立**
   - 命令：`python scripts/voc_analyzer.py --mode map --voc <analyzed.json> --ctq <ctq.json> --output <mapping.json>`
   - 功能：建立VOC与CTQ的对应关系，支持多对多映射

5. **优先级评估**
   - 命令：`python scripts/voc_analyzer.py --mode evaluate --mapping <mapping.json> --output <scored.json>`
   - 算法：综合频率权重(40%)、情感强度(30%)、明确重要性(30%)计算最终优先级

6. **可视化报告生成**
   - 命令：`python scripts/voc_analyzer.py --mode visualize --data <scored.json> --output <report.html>`
   - 内容：桑基图(映射关系)、词云(高频需求)、评分表格(CTQ优先级)

### 快速全流程
```bash
python scripts/voc_analyzer.py --mode full \
    --input customer_feedback.json \
    --ctq-template ctq_template.json \
    --output ./analysis_result/
```
执行完整流程：分析→提取CTQ→映射→评估→可视化

## 使用示例

### 示例1：分析客户投诉文本
- 场景/输入：`customer_complaints.json`包含50条客户投诉文本
- 预期产出：分析报告，包含词频统计、情感评分、问题分类、CTQ候选列表
- 关键要点：确保JSON格式正确，每条反馈包含`text`字段

### 示例2：建立需求映射关系
- 场景/输入：已分析的客户反馈 `analyzed.json`，已定义的CTQ `quality_ctq.json`
- 预期产出：`mapping.json`包含VOC-ID到CTQ-ID的映射关系
- 关键要点：CTQ需先通过 `--mode extract-ctq` 或手动定义

### 示例3：生成优先级报告
- 场景/输入：`mapping.json`包含完整映射关系
- 预期产出：`priority_report.html`交互式页面，包含桑基图和评分表格
- 关键要点：桑基图展示VOC来源→需求类型→CTQ的流向

## 资源索引
- 脚本：见 [scripts/voc_analyzer.py](scripts/voc_analyzer.py)(功能：VOC分析、CTQ提取、映射关联、可视化生成；支持7种模式)
- 参考：见 [references/format_spec.md](references/format_spec.md)(何时读取：准备输入数据或解析输出结果时)

## 注意事项
- 情感分析对讽刺、反话识别有限，重要决策需人工复核
- 自定义词典可通过 `user_dict.txt` 添加专业术语
- 大批量数据(>1000条)建议分批处理
- 输出HTML报告在浏览器中打开可获得最佳交互体验

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
