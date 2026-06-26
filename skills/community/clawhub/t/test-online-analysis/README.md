# OpenClaw Skill: Test Online Analysis

**测试专用在线实时数据分析与规则提取技能**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-%3E%3D0.9.0-blue.svg)](https://openclaw.ai)

## 🚀 功能简介

专为测试场景设计的实时数据分析技能，能够自动从日志、数据流中提取业务规则，识别异常模式，生成测试用例，大幅提升测试效率。

## ✨ 核心特性

### 📊 规则自动提取
- 从交易日志、接口返回、业务数据流中自动识别业务规则
- 支持提取字段约束、校验逻辑、金额限制、状态流转等规则
- 自动生成结构化的规则文档，可直接用于测试设计

### 🚨 实时异常检测
- 基于统计模型的实时异常点检测
- 支持严重程度分级（高/中/低）
- 自动生成异常报告，包含预期值、偏差度等信息

### 🎯 测试场景生成
- 基于提取的规则自动生成测试用例建议
- 识别边界条件和边缘场景
- 映射到测试覆盖度要求

## 🛠️ 快速开始

### 安装依赖
```bash
pip install numpy
```

### 基础使用

#### 1. 从日志提取业务规则
```bash
# 分析文本日志
python scripts/rule_extractor.py transaction_logs.txt

# 分析JSON结构数据
python scripts/rule_extractor.py api_responses.json

# 导出规则到Markdown文件
python scripts/rule_extractor.py logs.txt > business_rules.md
```

#### 2. 检测数据异常
```bash
# 分析数值型数据
python scripts/anomaly_detector.py performance_metrics.json

# 生成异常报告
python scripts/anomaly_detector.py metrics.json > anomaly_report.md
```

## 📋 技能触发关键词

当你提到以下内容时，技能会自动激活：
- online分析 / 实时分析
- 规则提取 / 业务规则识别
- 日志分析 / 数据流分析
- 异常检测 / 问题定位
- 测试场景生成 / 用例设计

## 📁 目录结构
```
online-analysis/
├── SKILL.md              # 技能核心定义与详细文档
├── README.md             # 项目说明文档
├── scripts/              # 可执行脚本
│   ├── rule_extractor.py    # 规则提取工具
│   ├── anomaly_detector.py  # 异常检测工具
│   ├── pattern_recognizer.py # 模式识别工具
│   └── test_case_generator.py # 测试用例生成工具
└── references/           # 参考文档
    ├── rule_extraction_standards.md # 规则提取标准
    ├── pattern_catalog.md            # 测试模式目录
    └── anomaly_severity_matrix.md    # 异常严重度矩阵
```

## 🧪 示例输出

### 规则提取报告示例
```markdown
# Extracted Business Rules

Generated at: 2026-03-13 15:00:00

| Rule Type | Condition | Confidence |
|-----------|-----------|------------|
| amount_limit | transaction amount must be less than 10000 | 0.9 |
| field_type | status must be of type string | 1.0 |
| field_enum | status must be one of: pending, success, failed | 0.9 |
```

### 异常检测报告示例
```markdown
# Anomaly Detection Report

Generated at: 2026-03-13 15:00:00
Total data points processed: 200
Total anomalies detected: 2

## Anomalies

| Timestamp | Value | Expected Mean | Z-Score | Severity |
|-----------|-------|---------------|---------|----------|
| 2026-03-13T14:55:00 | 200 | 100.23 | 9.87 | high |
| 2026-03-13T14:56:00 | 50 | 100.23 | 4.92 | medium |
```

## 📝 开发说明

### 扩展功能
- 在 `scripts/` 目录下添加新的分析脚本
- 在 `references/` 目录下添加行业规则库和模式模板
- 支持自定义规则提取正则表达式

### 贡献
欢迎提交 Issue 和 Pull Request 来完善这个技能！

## 📄 许可证

MIT License

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.com)
