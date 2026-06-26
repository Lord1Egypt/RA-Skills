---
name: data-analysis
description: 数据分析项目 - 数据采集 + 清洗 + 分析 + 可视化报告
version: 1.0.0
---

# 数据分析项目设计编排指南

## 概述

数据分析项目工作流：数据采集、清洗、探索性分析、建模到报告生成。
适合使用 Python + pandas + matplotlib/jupyter 的项目。

## 工作流程

### 阶段 1: 需求定义

**使用的 Skills**:
- writing-plans

**任务**:
- 定义分析目标和业务问题
- 确定数据源和采集方式
- 制定分析框架

**输出**:
- requirements.md
- docs/data-sources.md

### 阶段 2: 技术方案

**使用的 Skills**:
- writing-plans

**任务**:
- 编写实现计划
- 确定技术栈（pandas/scikit-learn/jupyter）
- 定义数据处理管道

**输出**:
- IMPLEMENTATION.md
- docs/technical-design.md

### 阶段 3: 数据开发

**使用的 Skills**:
- test-driven-development
- subagent-driven-development

**任务**:
- 数据采集脚本
- 数据清洗和预处理
- 探索性数据分析（EDA）
- 特征工程

**输出**:
- src/data_collection/
- src/data_cleaning/
- src/features/
- notebooks/01_eda.ipynb
- tests/

### 阶段 4: 建模与分析

**使用的 Skills**:
- test-driven-development
- subagent-driven-development

**任务**:
- 模型选择和训练
- 模型评估
- 结果可视化

**输出**:
- src/models/
- notebooks/02_modeling.ipynb
- notebooks/03_visualization.ipynb
- tests/

### 阶段 5: 报告与验证

**使用的 Skills**:
- requesting-code-review

**任务**:
- 代码审查
- 生成分析报告
- 数据质量检查

**输出**:
- docs/code-review.md
- docs/analysis-report.md
- notebooks/04_final_report.ipynb

## 上下文传递

context:
  writing-plans:
    input: [requirements.md]
    output: [IMPLEMENTATION.md, docs/data-sources.md]
    pass_to: test-driven-development

  test-driven-development:
    input: [IMPLEMENTATION.md]
    output: [src/, notebooks/, tests/]
    pass_to: requesting-code-review

  requesting-code-review:
    input: [src/, notebooks/, tests/]
    output: [docs/code-review.md, docs/analysis-report.md]

## 质量验证

validation:
  writing-plans:
    required_sections: [overview, implementation, testing]
    format: markdown
    max_length: 12000

  test-driven-development:
    test_coverage: 60
    expected_outputs: [src/, tests/]

  requesting-code-review:
    check_severity: medium
    expected_outputs: [docs/code-review.md, docs/analysis-report.md]

## 状态管理

state:
  checkpoints:
    - name: requirements_complete
      after: writing-plans
    - name: data_pipeline_complete
      after: test-driven-development
    - name: modeling_complete
      after: test-driven-development
    - name: code_reviewed
      after: requesting-code-review

  auto_save: true
  save_interval: 300
