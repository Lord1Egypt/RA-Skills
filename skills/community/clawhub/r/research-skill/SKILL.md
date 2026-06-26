---
name: write-paper
description: 自动生成学术论文各部分内容。支持摘要、引言、方法、实验、结论等章节的撰写。
---

# 学术论文撰写 Skill

自动生成高质量的学术论文各部分内容，支持多种研究领域和论文格式。

## 任务参数

从用户输入中提取以下参数：

- **项目路径** (project_path): 必需，包含代码和实验结果的项目路径
- **章节** (section): 可选，要生成的章节（abstract/intro/method/related/experiments/conclusion/all）
- **研究领域** (domain): 可选，研究领域（vq/gnn/rec/diffusion）
- **会议格式** (format): 可选，目标会议格式（neurips/icml/iclr/cvpr/acl）
- **输出路径** (output_path): 可选，论文输出路径

## 执行步骤

### 1. 项目信息收集

#### 1.1 代码分析

从项目代码中提取：
- 模型架构
- 算法流程
- 核心创新点

#### 1.2 实验结果收集

- 主实验结果表格
- 消融实验数据
- 可视化图表

#### 1.3 参考文献整理

- 引用的论文列表
- BibTeX条目

### 2. 摘要撰写 (Abstract)

#### 模板结构

```markdown
## Abstract 结构

1. **背景和问题** (1-2句)
   {problem_context}

2. **现有方法局限** (1句)
   {existing_limitations}

3. **我们的方法** (2-3句)
   {our_approach}

4. **主要结果** (1-2句)
   {key_results}

5. **意义** (1句)
   {significance}
```

#### 字数控制

- NeurIPS/ICML: ~150-200词
- CVPR/ICCV: ~150词
- ACL: ~150-200词

### 3. 引言撰写 (Introduction)

#### 标准结构

```markdown
## Introduction 结构

### 第1段: 背景引入
- 研究领域概述
- 核心任务定义
- 重要性说明

### 第2段: 现有方法
- 主流方法分类
- 各类方法的特点
- 研究现状

### 第3段: 问题和挑战
- 现有方法的局限
- 未解决的问题
- 研究动机

### 第4段: 我们的方法
- 核心想法
- 技术创新
- 方法概述

### 第5段: 贡献总结
- 贡献点1
- 贡献点2
- 贡献点3
```

### 4. 相关工作撰写 (Related Work)

#### 组织方式

```markdown
## Related Work 结构

### {研究方向1}
- 代表性工作介绍
- 方法特点分析
- 与本工作的关系

### {研究方向2}
- ...

### {研究方向3}
- ...

### 与本工作的区别
- 总结性对比
```

### 5. 方法撰写 (Methodology)

#### 标准结构

```markdown
## Methodology 结构

### 问题定义 (Problem Formulation)
- 符号定义
- 问题形式化
- 目标函数

### 方法概述 (Method Overview)
- 整体框架图
- 流程描述

### 核心组件1 (Component 1)
- 技术细节
- 数学公式
- 直观解释

### 核心组件2 (Component 2)
- ...

### 训练和推理 (Training and Inference)
- 损失函数
- 优化过程
- 算法伪代码
```

#### 数学公式规范

```latex
% 公式编号
\begin{equation}
    \mathcal{L} = \sum_{i=1}^{N} \ell(f(x_i), y_i)
    \label{eq:loss}
\end{equation}

% 行内公式
... where $f(\cdot)$ denotes the model function ...
```

### 6. 实验撰写 (Experiments)

#### 标准结构

```markdown
## Experiments 结构

### 实验设置 (Experimental Setup)

#### 数据集 (Datasets)
| Dataset | #Samples | #Features | Task |
|---------|----------|-----------|------|
| ... | ... | ... | ... |

#### 基线方法 (Baselines)
- 方法1: 简要描述
- 方法2: 简要描述

#### 评估指标 (Evaluation Metrics)
- 指标1: 定义
- 指标2: 定义

#### 实现细节 (Implementation Details)
- 超参数设置
- 训练配置
- 计算环境

### 主实验结果 (Main Results)

#### 结果表格
| Method | Metric1 | Metric2 | Metric3 |
|--------|---------|---------|---------|
| Baseline1 | ... | ... | ... |
| **Ours** | **...** | **...** | **...** |

#### 结果分析
- 关键观察1
- 关键观察2

### 消融实验 (Ablation Study)
- 组件贡献分析
- 超参数敏感性

### 可视化分析 (Qualitative Analysis)
- 案例分析
- 可视化结果
```

### 7. 结论撰写 (Conclusion)

#### 标准结构

```markdown
## Conclusion 结构

### 第1段: 工作总结
- 研究问题回顾
- 方法概述
- 主要贡献

### 第2段: 实验结论
- 关键实验发现
- 性能提升总结

### 第3段: 局限和未来工作
- 当前局限性
- 未来研究方向
```

### 8. LaTeX生成

#### 文件结构

```
paper/
├── main.tex           # 主文件
├── abstract.tex       # 摘要
├── introduction.tex   # 引言
├── related_work.tex   # 相关工作
├── methodology.tex    # 方法
├── experiments.tex    # 实验
├── conclusion.tex     # 结论
├── appendix.tex       # 附录
├── references.bib     # 参考文献
└── figures/           # 图片目录
```

#### 格式模板

支持的会议格式：
- NeurIPS (neurips_2024.sty)
- ICML (icml2024.sty)
- ICLR (iclr2024_conference.sty)
- CVPR (cvpr.sty)
- ACL (acl.sty)

## 输出格式

```
论文撰写完成

项目: {project_name}
生成章节: {sections}
目标格式: {format}

生成文件:
- 主文件: paper/main.tex
- 摘要: paper/abstract.tex ({word_count} 词)
- 引言: paper/introduction.tex ({word_count} 词)
- 相关工作: paper/related_work.tex ({word_count} 词)
- 方法: paper/methodology.tex ({word_count} 词)
- 实验: paper/experiments.tex ({word_count} 词)
- 结论: paper/conclusion.tex ({word_count} 词)
- 参考文献: paper/references.bib ({num_refs} 条)

编译命令:
cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

待完善:
- [ ] 检查数学符号一致性
- [ ] 添加实验图表
- [ ] 完善参考文献
- [ ] 语言润色
```

## 示例用法

```
/write-paper project/
/write-paper project/ --section=abstract
/write-paper project/ --format=neurips --domain=vq
/write-paper project/ --section=experiments --output-path=paper/
```

## 写作规范

### 学术写作要点

1. **客观性**: 避免主观判断词
2. **精确性**: 使用准确的技术术语
3. **简洁性**: 避免冗余表达
4. **逻辑性**: 段落间有清晰的逻辑联系

### 常见问题

- 避免: "Obviously", "Clearly", "It is well known"
- 使用: "We observe that", "The results show that"
- 避免: 过长的句子
- 使用: 适当的段落划分

## 注意事项

重要提示:

1. 确保所有数字和结果准确
2. 检查公式符号的一致性
3. 引用所有使用的方法和数据集
4. 遵循目标会议的格式要求
5. 预留时间进行语言润色

## 可用工具

使用以下工具完成任务：
- **Read**: 读取项目代码和实验结果
- **Write**: 生成LaTeX文件
- **Bash**: 编译LaTeX文档
- **WebSearch**: 搜索相关论文引用

## 相关 Skills

- `/analyze-experiments` - 分析实验结果
- `/survey-paper` - 调研相关工作
- `/fetch-paper` - 获取参考论文
