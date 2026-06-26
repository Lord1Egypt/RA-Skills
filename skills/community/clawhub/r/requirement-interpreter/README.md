# 智能需求解读器

## 概述

帮助用户与AI进行高效、准确的沟通。通过多级分类、案例匹配和结构化访谈，显著提升需求理解质量。

## 安装

1. 解压到 `~/.codebuddy/skills/` 或 `.codebuddy/skills/`
2. 重启 CodeBuddy

## 核心功能

### 1. 智能分类
- 6大一级类型：技术开发、内容创作、数据分析、业务流程、问题解决、咨询服务
- 25+二级子类精准识别
- 置信度评估

### 2. 案例匹配
- 基于相似案例推荐最佳实践
- 行业知识库支持

### 3. 结构化访谈
- 个性化问题引导
- 需求完整性验证

## 使用方式

### 自动触发
当需求描述模糊时自动启动

### 手动调用
- "请使用需求解读技能"
- "帮我详细分析这个需求"

## 文件结构

```
requirement-interpreter/
├── SKILL.md              # 技能主文档
├── scripts/
│   ├── main.py           # 入口文件
│   ├── optimized_classifier.py    # 分类引擎
│   ├── optimized_interpreter.py   # 解读器
│   ├── case_library.json          # 案例库
│   └── structured_interview.py   # 访谈框架
├── assets/
│   ├── templates/        # 需求模板
│   └── checklists/       # 检查清单
└── references/
    └── requirement_patterns.md    # 需求模式
```

## 效果指标

- 一级分类准确率: >95%
- 二级分类准确率: >85%
- 案例推荐准确率: >90%
