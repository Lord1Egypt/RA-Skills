# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-21

### ✨ Features

- **analyze_skill.py** - 分析单个技能，生成完整报告
  - 支持 text/markdown/json 三种输出格式
  - 提取基本信息、功能、示例、配置、注意事项
  
- **creative_usage.py** - 生成技能的创意用法建议
  - 为常用技能预设创意用法
  - 为其他技能自动生成智能建议
  - 提供具体的实施步骤和价值说明

- **find_combinations.py** - 发现可组合使用的技能
  - 预定义常见技能组合模式
  - 基于描述分析潜在组合
  - 显示已安装和未安装的技能

- **recommend_skill.py** - 根据任务描述推荐技能
  - 关键词匹配推荐
  - 生成工作流程建议
  - 提供安装命令

- **compare_matrix.py** - 对比多个相似技能
  - 生成对比矩阵表格
  - 分析优缺点
  - 给出选择建议

- **analyze_all.py** - 批量分析所有已安装技能
  - 生成技能索引
  - 按类别分组
  - 支持 markdown/json 输出

### 📝 Documentation

- 完整的 SKILL.md 文档
- README.md 使用指南
- 每个脚本的详细注释

### 🔧 Technical

- 纯 Python 3 实现
- 无外部依赖（仅使用标准库）
- 兼容 OpenClaw 环境

## [0.1.0] - 2026-03-20

### 🎉 Initial Release

- 基础功能实现
- 支持基本的技能分析
