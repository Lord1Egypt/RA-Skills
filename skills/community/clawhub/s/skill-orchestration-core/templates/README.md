# Skill 编排核心

轻量级的 skill 编排系统，专注于上下文管理、流程编排和质量保证。

## 快速开始

### 1. 创建项目

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

### 2. 修改 DESIGN.md

根据你的项目需求修改 DESIGN.md 文件。

### 3. 执行流程

```bash
# 使用上下文管理器
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py show

# 使用流程编排器
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py parse DESIGN.md

# 使用输出验证器
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py validate-all .
```

## 核心功能

### 1. 上下文管理

管理 skill 之间的上下文传递和共享。

```python
from context_manager import ContextManager

ctx = ContextManager("/path/to/project")
ctx.load()

# 保存数据
ctx.set("plan", plan_content)

# 获取数据
plan = ctx.get("plan")

# 传递给下一个 skill
ctx.pass_to("test-driven-development")

# 标记完成
ctx.mark_skill_completed("writing-plans")

# 保存到文件
ctx.save()
```

### 2. 流程编排

基于 DESIGN.md 的流程编排，**集成 Hermes delegate_task 真正执行 skill**。

```python
from workflow_orchestrator import WorkflowOrchestrator

orch = WorkflowOrchestrator("/path/to/DESIGN.md")
parsed = orch.parse_design()

# 执行流程
orch.execute()

# 控制
orch.pause()
orch.resume()
orch.jump_to("开发")

# 检查点
orch.set_checkpoint("checkpoint-需求分析")
orch.restore_checkpoint("checkpoint-需求分析")
```

### 3. 质量保证

自动验证 skill 输出质量，**真正读取项目文件做验证**。

```python
from output_validator import OutputValidator

validator = OutputValidator("/path/to/project")

# 从 DESIGN.md 加载规则
validator.load_from_design("/path/to/DESIGN.md")

# 验证单个 skill
result = validator.validate("writing-plans")
# result: {"valid": True/False, "errors": [...], "warnings": [...], "fixable": True/False}

# 验证所有
results = validator.validate_all()

# 自动修复
validator.auto_fix("writing-plans")

# 获取报告
report = validator.get_report()
```

## CLI 接口

### 上下文管理器

```bash
python3 scripts/context_manager.py show [project_path]
python3 scripts/context_manager.py status [project_path]
python3 scripts/context_manager.py set <key> <value> [project_path]
python3 scripts/context_manager.py get <key> [project_path]
python3 scripts/context_manager.py complete <skill_name> [project_path]
python3 scripts/context_manager.py clear [project_path]
```

### 流程编排器

```bash
python3 scripts/workflow_orchestrator.py parse <DESIGN.md>
python3 scripts/workflow_orchestrator.py execute <DESIGN.md>
python3 scripts/workflow_orchestrator.py status <DESIGN.md>
python3 scripts/workflow_orchestrator.py checkpoint <DESIGN.md> <name>
python3 scripts/workflow_orchestrator.py restore <DESIGN.md> <name>
python3 scripts/workflow_orchestrator.py jump <DESIGN.md> <stage_name>
```

### 输出验证器

```bash
python3 scripts/output_validator.py validate <skill> [project_path]
python3 scripts/output_validator.py validate-all [project_path]
python3 scripts/output_validator.py auto-fix <skill> [project_path]
python3 scripts/output_validator.py load-design <DESIGN.md>
python3 scripts/output_validator.py report
```

## 工作流模板

| 模板 | 路径 | 阶段数 | 适用场景 |
|------|------|--------|----------|
| 示例项目 | `templates/example-project/` | 4 | 学习和测试编排系统 |
| Web 全栈 | `templates/web-fullstack/` | 5 | React + FastAPI 全栈开发 |
| 数据分析 | `templates/data-analysis/` | 5 | 数据采集/清洗/建模/报告 |
| API 产品 | `templates/api-product/` | 4 | 免费 API 组合成商业产品 |

## 项目结构

```
project/
├── DESIGN.md           # 设计编排指南
├── .orchestration/     # 编排系统目录
│   ├── context.json    # 上下文文件
│   ├── state.json      # 状态文件
│   ├── .context.lock   # 上下文文件锁
│   ├── .state.lock     # 状态文件锁
│   └── checkpoints/    # 检查点
│       ├── checkpoint-需求分析.json
│       └── checkpoint-开发.json
├── requirements.md     # 需求文档
├── IMPLEMENTATION.md   # 实现计划
├── src/                # 源代码
├── tests/              # 测试
└── docs/               # 文档
```

## 使用示例

### 示例 1: 简单项目

```bash
# 创建项目
mkdir simple-project
cd simple-project

# 创建 DESIGN.md
cat > DESIGN.md << 'EOF'
---
name: simple-project
description: 简单项目示例
version: 1.0.0
---

# 项目设计编排指南

## 工作流程

### 阶段 1: 计划

**使用的 Skills**:
- writing-plans

**任务**:
- 编写实现计划

**输出**:
- IMPLEMENTATION.md
EOF

# 解析 DESIGN.md
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py parse DESIGN.md
```

### 示例 2: 上下文管理

```bash
# 查看上下文
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py show

# 设置数据
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py set plan "plan content"

# 获取数据
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py get plan

# 标记 skill 完成
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/context_manager.py complete writing-plans
```

### 示例 3: 质量验证

```bash
# 从 DESIGN.md 加载验证规则
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py load-design DESIGN.md

# 验证所有 skill 输出
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py validate-all .

# 获取验证报告
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/output_validator.py report
```

## 最佳实践

### 1. 上下文管理

- 只传递必要的数据
- 使用有意义的键名
- 定期清理不需要的数据

### 2. 流程编排

- 明确每个阶段的输入输出
- 合理设置检查点
- 使用自动保存

### 3. 质量验证

- 设置合理的验证规则
- 不要过于严格
- 利用自动修复功能

## 常见问题

### Q: 上下文太大怎么办？

A: 使用上下文压缩：

```python
ctx.context["config"]["contextCompression"] = True
ctx.context["config"]["maxContextSize"] = 50000
ctx.save()
```

### Q: 如何处理长时间运行的项目？

A: 使用检查点：

```yaml
state:
  checkpoints:
    - name: requirements_complete
      after: writing-plans
  auto_save: true
  save_interval: 300
```

### Q: 如何验证输出质量？

A: 使用质量验证：

```python
validator = OutputValidator("/path/to/project")
validator.load_from_design("DESIGN.md")
results = validator.validate_all()
for skill, result in results.items():
    print(f"{skill}: {'PASS' if result['valid'] else 'FAIL'}")
```

### Q: DESIGN.md 中的 YAML 解析失败？

A: 确保 YAML 内容不以 ```yaml 代码块包裹（编排器已兼容两种格式，但推荐裸写）。
同时注意 YAML 缩进必须一致，使用空格而非 Tab。

## 贡献

欢迎贡献改进建议和最佳实践！

## 许可证

MIT
