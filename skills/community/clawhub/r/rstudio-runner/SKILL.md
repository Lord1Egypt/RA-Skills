---
name: BioinfoAI-Assistant
version: 4.0.0
description: AI-powered bioinformatics analysis platform with intelligent auto-organization and comprehensive Chinese report generation. Auto-detects sequencing data, generates R scripts, saves all outputs to structured subfolders, and creates detailed analysis reports in Chinese.
icon: 🧬
author: (孟令章 教授) & 赵净洁
institution: 广西壮族自治区人民医院（广西医学科学院）
email: lzmeng@gxams.org.cn, 87611218@qq.com
triggers:
  - file: .R
  - file: .Rmd
  - file: .csv
  - file: .tsv
  - file: .mtx
  - file: .h5
  - file: .h5ad
  - directory: count_matrix
  - directory: raw_data
  - directory: sequencing-data
  - keyword: "analyze sequencing"
  - keyword: "bioinformatics"
  - keyword: "auto-organize"
  - keyword: "run analysis"
  - keyword: "测序数据分析"
  - keyword: "自动分析"
  - keyword: "生成报告"
---

# BioinfoAI-Assistant v4.0.0 🧬
# AI驱动的生物信息学智能分析平台
# AI-Powered Bioinformatics Analysis Platform

## 核心理念 / Core Philosophy
**"一键分析，全程自动，智能整理，中文报告"**

---

## 📥 安装方法 / Installation

### 方法1：通过 ClawHub 安装（推荐）
```bash
clawhub install rstudio-runner
```

### 方法2：通过 OpenClaw CLI 安装
```bash
openclaw skills install rstudio-runner
```

### 方法3：手动安装
1. 下载技能文件夹
2. 复制到 OpenClaw 工作目录的 `skills/` 文件夹下
3. 运行 `openclaw skills check` 验证安装

### 系统要求
- **R**: 版本 ≥ 4.0.0
- **RStudio**: 版本 ≥ 2022.07.1
- **必需R包**: Seurat, DESeq2, clusterProfiler, ggplot2, rmarkdown

---

## 👥 作者信息 / Authors

### 主要作者 / Primary Author
- **姓名**: (孟令章 教授)
- **全称**: Prof. Dr. rer. nat. Lingzhang Meng
- **单位**: 广西壮族自治区人民医院（广西医学科学院）
- **邮箱**: lzmeng@gxams.org.cn

### 合作作者 / Co-Author
- **姓名**: 赵净洁
- **邮箱**: 87611218@qq.com

---

## 🎯 功能概述 / Overview

本技能是一个**AI驱动的生物信息学智能分析平台**，能够：

1. **自动检测**测序数据类型（单细胞、普通转录组等）
2. **智能推荐**生物信息学分析策略
3. **自动生成**R分析脚本
4. **自动整理**所有输出文件到结构化子文件夹
5. **自动生成**详细的中文分析报告

---

## 📁 智能自动整理系统 / Intelligent Auto-Organization

### 自动创建的文件夹结构 / Auto-Created Folder Structure

```
项目名_YYYYMMDD/
│
├── 📂 01_原始数据/                      # 原始输入数据（只读）
│   ├── 表达矩阵/
│   ├── 样本信息/
│   └── 元数据/
│
├── 📂 02_R脚本/                         # 生成的R脚本
│   ├── 01_数据加载.R
│   ├── 02_质控分析.R
│   ├── 03_数据标准化.R
│   ├── 04_细胞聚类.R
│   ├── 05_细胞注释.R
│   ├── 06_差异表达分析.R
│   ├── 07_拟时序分析.R
│   └── 08_细胞通讯分析.R
│
├── 📂 03_结果图片/                      # 所有可视化图片
│   ├── 01_质控图/
│   ├── 02_降维图/
│   ├── 03_聚类图/
│   ├── 04_标记基因图/
│   ├── 05_差异表达图/
│   ├── 06_拟时序图/
│   └── 07_细胞通讯图/
│
├── 📂 04_结果表格/                      # 所有CSV/TXT结果文件
│   ├── 01_质控统计/
│   ├── 02_聚类信息/
│   ├── 03_细胞注释/
│   ├── 04_差异表达结果/
│   ├── 05_通路分析/
│   └── 06_元数据/
│
├── 📂 05_分析报告/                      # 中文分析报告
│   ├── 完整分析报告.html
│   ├── 质控报告.html
│   ├── 聚类分析报告.html
│   └── 方法学说明.pdf
│
├── 📂 06_R对象/                         # 保存的R数据对象
│   ├── seurat_QC后.rds
│   ├── seurat_聚类后.rds
│   └── seurat_注释后.rds
│
├── 📂 07_运行日志/                      # 执行日志
│   └── 执行记录.log
│
└── 📂 08_会话信息/                      # 可重复性信息
    ├── R版本信息.txt
    └── 包版本记录.csv
```

---

## 📊 中文分析报告 / Chinese Analysis Report

### 报告内容 / Report Contents

生成的中文分析报告包含：

#### 1. 分析概述 / Analysis Overview
- 数据类型和基本信息
- 样本数量和细胞数量
- 分析流程概览

#### 2. 质控分析 / Quality Control
- **图片说明**:
  - `nFeature_RNA_violin.png`: 每个细胞的基因数分布，反映细胞质量
  - `nCount_RNA_violin.png`: 每个细胞的UMI数分布，反映测序深度
  - `percent_MT_violin.png`: 线粒体基因比例，高比例可能表示死细胞
  - `QC_correlation.png`: 基因数与UMI数的相关性

- **CSV文件说明**:
  - `cell_QC_stats.csv`: 每个细胞的质控统计信息
  - `gene_QC_stats.csv`: 每个基因的检测频率

#### 3. 降维和聚类 / Dimensionality Reduction & Clustering
- **图片说明**:
  - `ElbowPlot.png`: 肘部图，帮助选择最佳主成分数
  - `PCA_heatmap.png`: 主成分热图，显示主要变异来源
  - `UMAP_res0.8.png`: UMAP降维聚类图，显示细胞群体结构
  - `tSNE_res0.8.png`: tSNE降维聚类图，另一种可视化

- **CSV文件说明**:
  - `cluster_cell_counts.csv`: 每个聚类的细胞数量
  - `cluster_markers_all.csv`: 所有聚类的标记基因

#### 4. 细胞注释 / Cell Annotation
- **图片说明**:
  - `DotPlot_top10.png`: 点图显示各细胞类型的Top10标记基因
  - `Heatmap_all_markers.png`: 热图显示所有标记基因表达

- **CSV文件说明**:
  - `cell_type_predictions.csv`: 每个细胞的类型预测
  - `annotation_confidence.csv`: 注释置信度评分

#### 5. 差异表达分析 / Differential Expression
- **图片说明**:
  - `Volcano_cluster0_vs_others.png`: 火山图显示差异基因
  - `Heatmap_topDEGs.png`: 热图显示Top差异基因

- **CSV文件说明**:
  - `DEG_cluster0_vs_all.csv`: 聚类0与其他聚类的差异基因
  - `DEG_summary_statistics.csv`: 差异表达统计汇总

#### 6. 通路分析 / Pathway Analysis
- **CSV文件说明**:
  - `GO_enrichment_results.csv`: GO富集分析结果
  - `KEGG_enrichment_results.csv`: KEGG通路富集结果

---

## 🤖 AI工作流程 / AI Workflow

### 步骤1: 数据输入 / Data Input
```
用户: "分析我的测序数据 F:\\HCC_Xiuli\\0. Datasets\\GSE242889"

AI: 🔍 正在分析输入数据...
    ✅ 检测到: 10X Genomics单细胞RNA测序
    ✅ 物种: 人类 (Homo sapiens, hg38)
    ✅ 样本数: 6个HCC样本
    ✅ 估计细胞数: ~15,000个
```

### 步骤2: 项目创建 / Project Creation
```
AI: 📁 创建组织化的项目结构...
    ✅ 创建: HCC_scRNAseq_20260329/
    ✅ 子文件夹: 8个主要目录
    ✅ 准备进行分析
```

### 步骤3: 策略选择 / Strategy Selection
```
AI: 🎯 推荐的分析策略:

    [1] 🔬 标准单细胞分析流程
        • 质控 → 过滤 → 标准化 → 聚类 → 注释
        • 输出: ~25个文件
        • 预计时间: 45分钟
        
    [2] 🧬 高级整合分析流程
        • 批次校正 → 整合 → 亚聚类
        • 输出: ~40个文件
        • 预计时间: 90分钟
        
    [3] 📊 差异表达重点分析
        • 质控 → 聚类 → 找标记基因 → 差异分析
        • 输出: ~30个文件
        • 预计时间: 60分钟

请选择策略 (1/2/3): 1
```

### 步骤4: 智能脚本生成 / Intelligent Script Generation
```
AI: ✍️ 编写R脚本并设置自动保存路径...

    ✅ 01_数据加载.R
       → 保存: 06_R对象/01_seurat_raw.rds
       → 保存: 04_结果表格/01_质控统计/细胞统计.csv
       
    ✅ 02_质控分析.R
       → 保存: 03_结果图片/01_质控图/*.png
       → 保存: 04_结果表格/01_质控统计/*.csv
       
    ✅ 03_数据标准化.R
       → 保存: 06_R对象/03_seurat_normalized.rds
       
    ✅ 04_细胞聚类.R
       → 保存: 03_结果图片/03_聚类图/*.png
       → 保存: 04_结果表格/02_聚类信息/*.csv
```

### 步骤5: 自动执行与文件跟踪 / Auto-Execution with File Tracking
```
AI: ▶️ 在RStudio中运行脚本...
    📊 监控文件生成...
    
    [01_数据加载.R] ✅ 完成
    ├── 生成: 01_seurat_raw.rds → 06_R对象/
    ├── 生成: 细胞统计.csv → 04_结果表格/01_质控统计/
    └── 生成: 基因统计.csv → 04_结果表格/01_质控统计/
    
    [02_质控分析.R] ✅ 完成
    ├── 生成: 6张质控图 → 03_结果图片/01_质控图/
    └── 生成: QC汇总.csv → 04_结果表格/01_质控统计/
```

### 步骤6: 生成中文分析报告 / Generate Chinese Report
```
AI: 📝 生成中文分析报告...
    ✅ 完整分析报告.html
       - 包含所有图片的详细中文说明
       - 每个CSV文件的用途解释
       - 分析结果的生物学意义解读
    
    ✅ 方法学说明.pdf
       - 详细的分析方法
       - 参数设置说明
       - 可重复性信息
```

### 步骤7: 最终整理报告 / Final Organization Report
```
AI: 📊 分析完成!

    📁 项目: HCC_scRNAseq_20260329/
    
    📈 生成的文件:
    ├── 02_R脚本/: 8个R脚本
    ├── 03_结果图片/: 47张图（7个子文件夹）
    ├── 04_结果表格/: 23个CSV/TXT文件
    ├── 05_分析报告/: 4个HTML/PDF报告 ⭐
    ├── 06_R对象/: 5个RDS文件
    └── 07_运行日志/: 8个日志文件
    
    📊 总计: 98个文件自动整理!
    📖 中文报告: 已生成详细说明文档
    ✅ 准备发表!
```

---

## 💡 使用示例 / Usage Examples

### 示例1: 全自动分析 / Full Auto Analysis
```
用户: "分析我的测序数据"

AI: [自动检测，推荐策略，生成脚本]
AI: [创建文件夹，运行分析，保存所有输出]
AI: [生成中文报告]
AI: "✅ 完成! 98个文件已整理到8个文件夹，中文报告已生成。"
```

### 示例2: 分步进行 / Step-by-Step
```
用户: "为我的数据创建整理好的项目"
AI: ✅ 已创建: MyProject_20260329/ 含8个子文件夹

用户: "生成质控脚本"
AI: ✅ 已保存: 02_R脚本/02_质控分析.R

用户: "运行并保存结果"
AI: ▶️ 运行中... 保存图片到 03_结果图片/01_质控图/
AI: ✅ 已保存6张质控图 + 2个CSV文件 + 1个RDS对象

用户: "生成中文报告"
AI: ✅ 已生成: 05_分析报告/完整分析报告.html
```

---

## 🐛 问题报告 / Issue Reporting

**联系作者 / Contact Authors:**

**主要联系人 / Primary Contact:**
- **姓名**: (孟令章 教授)
- **邮箱**: lzmeng@gxams.org.cn
- **单位**: 广西壮族自治区人民医院（广西医学科学院）

**合作作者 / Co-Author:**
- **姓名**: 赵净洁
- **邮箱**: 87611218@qq.com

---

## 🔄 版本历史 / Version History

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v4.0.0** | 2026-03-29 | **重大更新**: 添加中文分析报告生成功能 |
| v3.0.0 | 2026-03-29 | 智能自动整理系统 |
| v2.0.0 | 2026-03-29 | AI驱动的生物信息学平台 |
| v1.0.0 | 2026-03-29 | 初始版本 |

---

## 🙏 使命 / Mission

**"一键分析，全程自动，智能整理，中文报告"**

让生物信息学分析变得强大、有序、轻松，通过AI自动化实现。

---

**每个文件都有归属。每个分析都可重复。** 🧬✨
