# Skill 编排核心 - 快速开始指南

欢迎使用 Skill 编排核心！5 分钟上手。

## 快速开始

### 步骤 1: 创建项目

```bash
# 创建项目目录
mkdir my-project
cd my-project

# 复制示例 DESIGN.md
cp ~/.hermes/skills/devops/skill-orchestration-core/templates/example-project/DESIGN.md .

# 或使用其他模板
# cp -r ~/.hermes/skills/devops/skill-orchestration-core/templates/web-fullstack .
# cp -r ~/.hermes/skills/devops/skill-orchestration-core/templates/data-analysis .
# cp -r ~/.hermes/skills/devops/skill-orchestration-core/templates/api-product .
```

### 步骤 2: 查看和修改 DESIGN.md

```bash
cat DESIGN.md
# 编辑以适配你的项目...
```

### 步骤 3: 解析流程

```bash
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py parse DESIGN.md
```

### 步骤 4: 初始化上下文

```bash
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py show
```

### 步骤 5: 加载验证规则

```bash
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py load-design DESIGN.md
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py validate-all .
```

## 下一步

### 修改 DESIGN.md

```yaml
---
name: my-project
description: 我的项目描述
version: 1.0.0
---

# 项目设计编排指南

## 工作流程

### 阶段 1: 需求分析

**使用的 Skills**:
- writing-plans

**任务**:
- 分析需求
- 编写用户故事

**输出**:
- requirements.md
- user-stories.md
```

### 使用上下文管理

```bash
# 设置数据
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py set requirements "plan content"

# 获取数据
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py get requirements

# 查看上下文
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py show

# 标记 skill 完成
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py complete writing-plans
```

### 使用流程编排

```bash
# 解析 DESIGN.md
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py parse DESIGN.md

# 查看状态
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py status DESIGN.md

# 设置检查点
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py checkpoint DESIGN.md my-checkpoint

# 恢复检查点
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py restore DESIGN.md my-checkpoint
```

### 使用质量验证

```bash
# 验证所有 skill 输出
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py validate-all .

# 自动修复缺失内容
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py auto-fix writing-plans .

# 获取验证报告
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py report
```

## 工作流模板

| 模板 | 阶段数 | 适用场景 |
|------|--------|----------|
| example-project | 4 | 学习和测试编排系统 |
| web-fullstack | 5 | React + FastAPI 全栈开发 |
| data-analysis | 5 | 数据采集/清洗/建模/报告 |
| api-product | 4 | 免费 API 组合成商业产品 |

## 常用命令速查

### 上下文管理

```bash
python3 scripts/context_manager.py show [project_path]
python3 scripts/context_manager.py status [project_path]
python3 scripts/context_manager.py get <key> [project_path]
python3 scripts/context_manager.py set <key> <value> [project_path]
python3 scripts/context_manager.py complete <skill_name> [project_path]
python3 scripts/context_manager.py clear [project_path]
```

### 流程编排

```bash
python3 scripts/workflow_orchestrator.py parse <DESIGN.md>
python3 scripts/workflow_orchestrator.py execute <DESIGN.md>
python3 scripts/workflow_orchestrator.py status <DESIGN.md>
python3 scripts/workflow_orchestrator.py checkpoint <DESIGN.md> <name>
python3 scripts/workflow_orchestrator.py restore <DESIGN.md> <name>
python3 scripts/workflow_orchestrator.py jump <DESIGN.md> <stage_name>
```

### 输出验证

```bash
python3 scripts/output_validator.py validate <skill> [project_path]
python3 scripts/output_validator.py validate-all [project_path]
python3 scripts/output_validator.py auto-fix <skill> [project_path]
python3 scripts/output_validator.py load-design <DESIGN.md>
python3 scripts/output_validator.py report
```

## 端到端测试

修改解析逻辑后验证：

```bash
cd scripts && python3 test_e2e.py
```

## 更多资源

- [README.md](templates/README.md) — 详细说明
- [SKILL.md](SKILL.md) — 完整 API 文档和陷阱列表
- [example-project/](templates/example-project/) — 完整示例项目

## 许可证

MIT
