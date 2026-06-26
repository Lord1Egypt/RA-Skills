---
name: xiaolongxia-workflow
description: 分层任务分解与执行工作流
metadata:
  openclaw:
    emoji: "🦞"
    category: "workflow"
    tags: ["workflow", "task-management", "decomposition", "error-handling", "automation"]
---

---
slug: xiaolongxia-workflow
version: 0.5.0
---

# 小龙虾分层任务工作流

**版本**: 0.5.0 (Release Candidate)
**作者**: OpenClaw 助手
**创建时间**: 2026-03-17
**状态**: 开发中 - 最小可行版本

## 🎯 概述

小龙虾分层任务工作流是一个系统化、工程化的任务处理框架，专为复杂AI代理设计。它将大型任务分解为阶段、步骤、子步骤，直到每个子步骤对模型来说是可执行的，同时提供完整的错误处理、输入输出控制和备份机制。

## 🚀 快速开始

### 安装
```bash
# 从工作空间直接使用（开发中）
cd /root/.openclaw/workspace/skills/xiaolongxia-workflow
```

### 基本使用
```python
from scripts.task_analyzer import TaskAnalyzer
from scripts.project_manager import ProjectManager

# 1. 分析任务
analyzer = TaskAnalyzer()
summary = analyzer.analyze("帮我设计一个完整的电商网站后端系统")

# 2. 创建项目
manager = ProjectManager(summary)
project_path = manager.create_project()

print(f"项目创建在: {project_path}")
```

## 📁 目录结构
```
skills/xiaolongxia-workflow/
├── SKILL.md                    # 本文件
├── config/
│   └── workflow_config.json    # 配置文件
├── scripts/
│   ├── task_analyzer.py        # 任务分析器
│   ├── project_manager.py      # 项目管理器
│   ├── step_decomposer.py      # 步骤分解器
│   ├── step_executor.py        # 步骤执行器
│   ├── robust_executor.py      # 鲁棒执行器 (错误恢复)
│   ├── error_classifier.py     # 错误分类器
│   ├── template_engine.py      # 模板引擎
│   ├── run_workflow.py         # 工作流运行器
│   └── demo_integrated.py      # 集成演示
├── templates/
│   ├── task_summary.md.tpl     # 任务概要模板
│   ├── top_level_plan.md.tpl   # 顶层方案模板
│   └── step_report.md.tpl      # 步骤报告模板
├── tests/
│   ├── test_basic.py           # 基础测试
│   └── (更多测试待添加)
└── references/
    └── workflow_diagram.png    # 工作流程图 (待创建)
```

## 🔧 当前版本功能 (Beta 0.3.0)

### ✅ 已实现
1. **任务分析器** (`task_analyzer.py`)
   - 解析用户输入的任务描述
   - 生成结构化任务概要
   - 评估任务复杂度 (1-10分)
   - 自动判断是否需要分层处理

2. **项目管理器** (`project_manager.py`)
   - 创建标准项目文件夹结构
   - 生成任务概要文档 (`task_summary.md`)
   - 生成顶层方案 (`top_level_plan.md`)
   - 提供完整的项目信息接口

3. **步骤分解器** (`step_decomposer.py`)
   - 递归分解任务为阶段、步骤、子步骤
   - 支持复杂依赖关系管理
   - 生成可执行的叶子步骤
   - 保存分解结果为JSON

4. **步骤执行器** (`step_executor.py`)
   - 执行单个步骤和批量步骤
   - 模拟执行和实际执行模式
   - 执行结果记录和状态更新
   - 生成执行报告

5. **错误分类器** (`error_classifier.py`)
   - 识别常见API错误 (400, 429, 500, 504等)
   - 提供恢复策略 (重试、拆分、降级等)
   - 错误统计和学习功能
   - 策略成功率评估

6. **模板引擎** (`template_engine.py`)
   - 加载和渲染模板文件
   - 支持变量替换、条件判断、循环
   - 内置任务摘要、步骤计划、报告模板
   - 扩展自定义模板

7. **鲁棒执行器** (`robust_executor.py`)
   - 集成错误分类和恢复策略
   - 自动错误检测和恢复
   - 智能重试机制
   - 执行监控和增强报告

8. **工作流运行器** (`run_workflow.py`)
   - 完整的端到端工作流集成
   - 支持交互模式、测试模式、执行模式
   - 命令行界面和API调用

### 🚧 开发中
1. **邮件汇报系统** - 自动发送进度报告
2. **自动备份机制** - 项目状态持久化
3. **可视化进度跟踪** - 实时执行监控
4. **ClawHub集成** - 技能发布和版本管理

### 📅 待实现
- 邮件汇报系统
- 自动备份机制
- 依赖关系管理
- 可视化进度跟踪

## ⚙️ 配置

配置文件: `config/workflow_config.json`
```json
{
  "version": "0.1.0",
  "project_base_dir": "/root/.openclaw/workspace/projects",
  "max_decomposition_depth": 4,
  "default_model": "deepseek-reasoner",
  "max_input_tokens": 1000000,
  "max_output_tokens": 8000,
  "retry_policy": {
    "max_retries": 3,
    "backoff_factor": 2,
    "initial_delay": 1
  }
}
```

## 📋 工作流程

### 1. 任务接收与分析
```python
from scripts.task_analyzer import TaskAnalyzer

task = "帮我设计一个完整的电商网站后端系统"
analyzer = TaskAnalyzer()
summary = analyzer.analyze(task)

# 输出: task_summary.md
print(summary.to_markdown())
```

### 2. 项目创建
```python
from scripts.project_manager import ProjectManager

manager = ProjectManager(summary)
project_path = manager.create_project()
```

### 3. 生成文件夹结构
```
project_20260317_1320/
├── task_summary.md
├── top_level_plan.md
├── steps/
│   └── (后续生成)
└── backup/
```

## 🧪 测试

运行基础测试:
```bash
cd /root/.openclaw/workspace/skills/xiaolongxia-workflow
python3 -m pytest tests/test_basic.py -v
```

## 🔌 集成OpenClaw

### 自动触发规则 (待实现)
在`AGENTS.md`中添加:
```markdown
### 小龙虾工作流自动触发

当任务满足以下条件时自动启用:
- 包含复杂关键词（"系统设计"、"架构迁移"等）
- 估计执行时间 > 2小时
- 用户明确要求
```

### 作为技能调用
```bash
# 使用clawhub安装后
openclaw skill use xiaolongxia-workflow --task "你的大型任务描述"
```

## 🐛 已知问题 (MVP)

1. 步骤分解逻辑尚不完整
2. 错误处理仅为占位实现
3. 邮件汇报功能缺失
4. 备份机制待实现

## 📈 开发路线图

### v0.1.0 (当前) - 基础骨架
- [x] 任务分析器
- [x] 项目模板生成
- [ ] 基础文档生成

### v0.2.0 - 核心分解
- [ ] 步骤分解器
- [ ] 简单执行器
- [ ] 基础错误处理

### v0.3.0 - 执行引擎
- [ ] API调用封装
- [ ] 重试策略
- [ ] 输出验证

### v0.4.0 - 生产就绪
- [ ] 邮件汇报
- [ ] 自动备份
- [ ] 进度持久化

### v1.0.0 - 完整技能
- [ ] 完整测试套件
- [ ] ClawHub发布
- [ ] 文档完善

## 🤝 贡献指南

1. Fork本技能仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

MIT License

## 📞 支持

如有问题，请:
1. 查看`references/`目录中的文档
2. 运行测试检查功能
3. 在OpenClaw社区提问

---

**注意**: 这是最小可行版本，功能有限。建议仅在测试环境中使用。