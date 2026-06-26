# Scheme Generation and Design Writing

概念方案生成与设计说明撰写技能

## 简介

这是一个专业的 UI/UX 设计文档自动生成工具，能够：

- 📝 基于历史项目资料智能生成概念方案
- 🎨 根据 Figma 设计稿自动撰写设计说明
- 🔄 支持多风格方案对比
- 📄 输出专业的 Word 文档

将设计文档产出时间从 **3-5 天缩短至 2 分钟**。

## 快速开始

### 1. 配置

编辑 config.json，设置你的项目路径：

`json
{
  "projects_path": "C:\\path\\to\\your\\historical\\projects",
  "output_path": "C:\\path\\to\\output\\directory",
  "max_related_projects": 5,
  "num_proposal_styles": 3,
  "enable_figma": true,
  "enable_image_analysis": true
}
`

### 2. 建立索引

`ash
python scripts/index_projects.py
`

### 3. 开始使用

在 OpenClaw 中输入需求，例如：

`
请基于历史项目生成一个智能家居 APP 的概念方案，要求：
- 行业：IoT / 智能硬件
- 目标用户：25-45岁，中高收入
- 核心功能：设备控制、场景联动、数据可视化
- 设计风格：科技感、简洁、现代
`

## 主要功能

### 概念方案生成

- 自动匹配相关历史项目
- 生成多个风格方向的方案
- 包含完整的项目概述、设计目标、用户画像、信息架构等章节
- 输出专业的 Word 文档

### 设计说明撰写

- 支持图片和 Figma 设计稿分析
- 自动提取布局、色彩、字体、组件信息
- 生成结构化的设计说明文档
- 引用历史项目的设计规范

## 技术特点

- ✅ **极简**: 代码 < 500 行，无复杂依赖
- ✅ **智能**: 充分利用 OpenClaw 的理解能力
- ✅ **灵活**: 支持多种文档和设计稿格式
- ✅ **快速**: 2 分钟生成专业文档
- ✅ **可扩展**: 易于添加新的文档类型

## 依赖

- Python 3.7+
- OpenClaw
- figma skill（可选，用于 Figma 集成）

## 文档

详细使用说明请参考 SKILL.md

## 许可证

MIT License
