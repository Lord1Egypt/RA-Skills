---
name: skill-orchestration-core
description: Skill 编排核心 - 上下文管理、流程编排、质量保证（Python 实现）
version: 2.1.0
author: Hermes Agent
tags: [orchestration, workflow, context, quality]
---

# Skill 编排核心

轻量级的 skill 编排系统，专注于上下文管理、流程编排和质量保证。
**v2.1.0**: 新增 4 个实用工作流模板（示例/Web全栈/数据分析/API产品），基于 DESIGN.md 的流程编排，集成 Hermes delegate_task 真正执行 skill。

## 最新功能 (v2.1.0)

- **4 个工作流模板**: 示例项目(4阶段)、Web全栈(5阶段)、数据分析(5阶段)、API产品(4阶段)
  - 复制即用: `cp -r templates/web-fullstack /path/to/my-project`
  - 解析验证: `python3 scripts/workflow_orchestrator.py parse DESIGN.md`
- **输出验证强化**: `validate-all` 全部通过，`auto-fix` 自动补全缺失文件
- **端到端测试**: `python3 scripts/test_e2e.py` 一键验证全部脚本协同工作

## 核心功能

### 1. 上下文管理（context_manager.py）

管理 skill 之间的上下文传递和共享。

#### 上下文结构

```json
{
  "project": {
    "name": "my-project",
    "path": "/path/to/project",
    "description": "项目描述"
  },
  "state": {
    "currentSkill": "test-driven-development",
    "progress": 40.0,
    "completedSkills": ["writing-plans"],
    "startTime": "2026-06-10T20:00:00"
  },
  "data": {
    "plan": "计划内容...",
    "requirements": "需求内容..."
  },
  "config": {
    "contextCompression": true,
    "maxContextSize": 100000
  }
}
```

#### 上下文操作

```python
from context_manager import ContextManager

ctx = ContextManager("/path/to/project")
ctx.load()

# 保存/获取数据
ctx.set("plan", plan_content)
value = ctx.get("plan")

# 传递给下一个 skill
ctx.pass_to("test-driven-development")

# 标记完成
ctx.mark_skill_completed("writing-plans")
print(ctx.is_skill_completed("writing-plans"))  # True

# 压缩/恢复
compressed = ctx.compress()
ctx.restore(compressed)

# 保存到文件
ctx.save()
```

#### 上下文文件

上下文保存在项目目录的 `.orchestration/context.json`，带文件锁防止并发写冲突。

#### CLI 接口

```bash
python scripts/context_manager.py show [project_path]
python scripts/context_manager.py status [project_path]
python scripts/context_manager.py set <key> <value> [project_path]
python scripts/context_manager.py get <key> [project_path]
python scripts/context_manager.py complete <skill_name> [project_path]
python scripts/context_manager.py clear [project_path]
```

### 2. 流程编排（workflow_orchestrator.py）

基于 DESIGN.md 的流程编排，**集成 Hermes delegate_task 真正执行 skill**。

#### DESIGN.md 结构

```yaml
---
name: my-project
description: 项目描述
version: 1.0.0
---

## 工作流程

### 阶段 1: 需求分析
**使用的 Skills**:
- writing-plans
**任务**:
- 分析需求
- 编写用户故事
**输出**:
- requirements.md

### Stage 2: Development
**Skills**:
- test-driven-development
**Tasks**:
- Write tests
- Implement features
**Outputs**:
- src/
- tests/
```

> **中英文兼容**: 阶段标题支持 `### 阶段 N:` 和 `### Stage N:` 两种格式。

#### 编排指令输出

执行工作流时，编排器会为每个阶段生成 `[ORCHESTRATE]` 指令，供 Hermes agent 通过 delegate_task 调度：

```
[ORCHESTRATE] 阶段 1: 需求分析
[ORCHESTRATE]   → 执行 skill: writing-plans
[ORCHESTRATE]     delegate_task goal: "使用 writing-plans skill 完成阶段 1(需求分析)的任务"
[ORCHESTRATE]     delegate_task context: "项目路径=/path/to/project, 任务列表=[...], 期望输出=[...]"
[CONTEXT]   writing-plans 输入: [requirements.md]
[CONTEXT]   writing-plans 输出: [IMPLEMENTATION.md]
[CONTEXT]   writing-plans → test-driven-development
[VALIDATE]  writing-plans 验证规则: {...}
```

Hermes agent 读取这些指令后，调用 delegate_task 真正调度 skill 执行。

#### Python API

```python
from workflow_orchestrator import WorkflowOrchestrator

orch = WorkflowOrchestrator("/path/to/DESIGN.md")
parsed = orch.parse_design()
orch.execute()

# 控制
orch.pause()
orch.resume()
orch.jump_to("开发")

# 检查点
orch.set_checkpoint("checkpoint-需求分析")
orch.restore_checkpoint("checkpoint-需求分析")
```

#### CLI 接口

```bash
python scripts/workflow_orchestrator.py parse <DESIGN.md>
python scripts/workflow_orchestrator.py execute <DESIGN.md>
python scripts/workflow_orchestrator.py status <DESIGN.md>
python scripts/workflow_orchestrator.py checkpoint <DESIGN.md> <name>
python scripts/workflow_orchestrator.py restore <DESIGN.md> <name>
python scripts/workflow_orchestrator.py jump <DESIGN.md> <stage_name>
```

### 3. 输出验证（output_validator.py）

自动验证 skill 输出质量，**真正读取项目文件做验证**。

#### 验证能力

- **必需章节检查**: 支持多语言章节名（中文/英文）
- **格式验证**: markdown / json / yaml
- **长度验证**: 最大/最小长度
- **文件存在性检查**: 验证期望的输出文件是否生成
- **测试覆盖率估算**: 基于 tests/ 和 src/ 文件比例
- **自动修复**: 为缺失章节/文件添加占位符

#### Python API

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

# 报告
report = validator.get_report()
```

#### CLI 接口

```bash
python scripts/output_validator.py validate <skill> [project_path]
python scripts/output_validator.py validate-all [project_path]
python scripts/output_validator.py auto-fix <skill> [project_path]
python scripts/output_validator.py load-design <DESIGN.md>
python scripts/output_validator.py report
```

## DESIGN.md 编写规范

### 上下文传递

```yaml
## 上下文传递

context:
  writing-plans:
    input: [requirements.md]
    output: [IMPLEMENTATION.md]
    pass_to: test-driven-development

  test-driven-development:
    input: IMPLEMENTATION.md
    output: [tests/, src/]
    pass_to: github-code-review
```

> **重要**: 上下文传递的 YAML 内容不要用 ```yaml 代码块包裹，直接写在 `## 上下文传递` 标题下即可。编排器会自动兼容两种格式。

### 质量验证

```yaml
## 质量验证

validation:
  writing-plans:
    required_sections: [overview, implementation, testing]
    format: markdown
    max_length: 10000

  test-driven-development:
    test_coverage: 80
    expected_outputs: [tests/, src/]
```

### 状态管理

```yaml
## 状态管理

state:
  checkpoints:
    - name: requirements_complete
      after: writing-plans
    - name: tests_complete
      after: test-driven-development

  auto_save: true
  save_interval: 300
```

## 项目结构

```
skill-orchestration-core/
├── SKILL.md                            # Skill 文档
├── references/
│   └── workflow-orchestrator-regex-pitfalls.md
├── scripts/
│   ├── context_manager.py              # 上下文管理
│   ├── workflow_orchestrator.py        # 流程编排
│   ├── output_validator.py             # 输出验证
│   └── test_e2e.py                     # 端到端测试
├── templates/
│   ├── README.md                       # 模板说明
│   ├── QUICKSTART.md                   # 快速入门
│   ├── example-project/                # 示例项目模板（4阶段）
│   ├── web-fullstack/                  # Web全栈模板（5阶段）
│   ├── data-analysis/                  # 数据分析模板（5阶段）
│   └── api-product/                    # API产品模板（4阶段）
```

## 最佳实践

### 1. 上下文管理

```python
# 只传递必要的数据
ctx.set("plan", plan_content)        # 好
ctx.set("everything", all_data)      # 不好

# 使用有意义的键名
ctx.set("user_requirements", reqs)   # 好
ctx.set("data", reqs)                # 不好

# 定期清理不需要的数据
ctx.delete("temp_data")
```

### 2. 流程编排

```yaml
# 明确每个阶段的输入输出
### 阶段 1: 需求分析
**使用的 Skills**:
- writing-plans
**任务**:
- 分析需求
**输出**:
- requirements.md
```

### 3. 质量验证

```python
# 设置合理的验证规则
validator.add_rule("writing-plans", {
    "required_sections": ["overview", "implementation"],  # 合理
    "max_length": 10000                                    # 合理
})

# 不要设置过于严格的规则
validator.add_rule("writing-plans", {
    "required_sections": ["overview", "implementation", "testing", "deployment", "maintenance"],  # 过于严格
    "max_length": 100  # 过于严格
})
```

## 工作流模板

提供多种开箱即用的工作流模板，位于 `templates/` 目录：

| 模板 | 路径 | 阶段数 | 适用场景 |
|------|------|--------|----------|
| 示例项目 | `templates/example-project/` | 4 | 学习和测试编排系统 |
| Web 全栈 | `templates/web-fullstack/` | 5 | React + FastAPI 全栈开发 |
| 数据分析 | `templates/data-analysis/` | 5 | 数据采集/清洗/建模/报告 |
| API 产品 | `templates/api-product/` | 4 | 免费 API 组合成商业产品 |

### 使用模板

```bash
# 复制模板到你的项目
cp -r ~/.hermes/skills/devops/skill-orchestration-core/templates/web-fullstack /path/to/my-project

# 修改 DESIGN.md 适配你的项目
cd /path/to/my-project
# 编辑 DESIGN.md ...

# 解析验证
python3 ~/.hermes/skills/devops/skill-orchestration-core/scripts/workflow_orchestrator.py parse DESIGN.md
```

## 常见问题

### Q: 上下文太大怎么办？

A: 使用上下文压缩：

```python
ctx.context["config"]["contextCompression"] = True
ctx.context["config"]["maxContextSize"] = 50000
```

### Q: 如何处理长时间运行的项目？

A: 使用检查点：

```yaml
state:
  checkpoints:
    - name: requirements_complete
      after: writing-plans
  auto_save: true
```

### Q: DESIGN.md 中的 YAML 解析失败？

A: 确保 YAML 内容不以 ```yaml 代码块包裹（编排器已兼容两种格式，但推荐裸写）。
同时注意 YAML 缩进必须一致，使用空格而非 Tab。

### Q: 如何让 Hermes agent 真正执行 skill？

A: 编排器输出 `[ORCHESTRATE]` 指令后，Hermes agent 应读取这些指令，
通过 `delegate_task` 调度子 agent 执行对应的 skill。示例：

```python
# Hermes agent 侧的编排逻辑
orch = WorkflowOrchestrator("DESIGN.md")
parsed = orch.parse_design()

for stage in parsed["workflow"]:
    for skill_name in stage["skills"]:
        # 通过 delegate_task 真正执行 skill
        delegate_task(
            goal=f"使用 {skill_name} skill 完成阶段 {stage['number']}({stage['name']})",
            context=f"项目路径={project_path}, 任务={stage['tasks']}, 输出={stage['outputs']}",
            toolsets=["terminal", "file", "web"]
        )
```

## 陷阱

1. **YAML 缩进**: DESIGN.md 中的 YAML 段落缩进必须一致，不要混用 Tab 和空格
2. **阶段标题格式**: 必须使用 `### 阶段 N:` 或 `### Stage N:`，不支持其他格式
3. **文件锁**: 多进程并发写上下文时会自动加文件锁，但同一进程内不会
4. **PyYAML 可选**: 无 PyYAML 时会使用简单解析器（只支持一级 key:value），建议安装
5. **检查点命名**: 检查点名称不要包含特殊字符，推荐使用 `checkpoint-阶段名` 格式
6. **输出文件路径**: 验证器查找输出文件时基于项目根目录的相对路径
7. **DESIGN.md 加粗标记**: 阶段内的列表标题如果用了 Markdown 加粗（`**使用的 Skills**:`），正则必须用 `\*{0,2}` 包裹关键词，否则匹配失败导致 skills/tasks/outputs 全部为空列表。这是最常见的坑——直觉会写 `(?:使用的\s*)?[Ss]kills?[:：]`，但实际文本是 `**使用的 Skills**:`，星号捷足先登让正则完全失配
8. **阶段标题正则必须分离 name 和 body**: `STAGE_HEADING_REGEX` 必须用 `([^\n]+)` 在同一行捕获阶段名，再用 `(.*?)(?=\n###|\n##|\Z)` 捕获 rest-of-body。如果用 `(.+?)(?=\n###|\n##|\Z)` 把 name 和 body 混在一个组里，`name` 会吃进整个 body 文本直到下一个标题，导致阶段名变成 "需求分析\n\n**使用的 Skills**:..."
9. **端到端验证**: 修改正则或解析逻辑后，务必跑 `scripts/test_e2e.py` 验证三个脚本的协同工作——单脚本能导入不代表 parse 输出的 skills/tasks/outputs 非空
10. **模板验证**: 新增 DESIGN.md 模板后，务必用 `workflow_orchestrator.py parse <DESIGN.md>` 验证解析输出——阶段数、skills、tasks、outputs 必须非空。模板里用了加粗列表标题（`**使用的 Skills**:`）就触发陷阱 #7，不验不知道
11. **跨会话恢复**: 迭代跨多天多 session 时，用 `session_search` 按关键词找到最近 session → 读尾部 TODO → 从最后一个未完成项继续。不要从头重做，也不要跳过验证步骤

## 参考文档

- **[正则排坑记录](references/workflow-orchestrator-regex-pitfalls.md)** — 跨3个session才修好的 STAGE_REGEX 和 `_extract_list` 正则 bug，含根因分析和修复方案
- **[模板编写与跨会话恢复](references/template-authoring-and-recovery.md)** — 新建模板的验证流程、跨 session 恢复迭代工作的方法、模板目录约定

## 端到端测试

修改解析逻辑后，运行验证：

```bash
cd scripts && python3 test_e2e.py
```

验证内容：DESIGN.md 解析 → 上下文操作 → checkpoint/restore → 输出验证 → 状态查询。

## 更新日志

### v2.1.0 (2026-06-13)

- **新增**: 3个实用工作流模板：`web-fullstack`（5阶段全栈开发）、`data-analysis`（5阶段数据分析）、`api-product`（4阶段API产品）
- **新增**: example-project 模板补全所有阶段输出文件（requirements.md、user-stories.md、features.md、IMPLEMENTATION.md、technical-design.md、test-plan.md）
- **修复**: README.md 和 QUICKSTART.md 从旧 Node.js 命令更新为 Python CLI 命令
- **改进**: validate-all 全部通过

### v2.0.1 (2026-06-13)

- **修复**: STAGE_HEADING_REGEX 拆分 name/body 捕获组（name 只取标题行 `[^\n]+`，body 独立捕获）
- **修复**: _extract_list 三行正则加 `\*{0,2}` 支持 `**加粗**:` Markdown 格式
- **新增**: 端到端测试脚本 `scripts/test_e2e.py`
- **新增**: 正则排坑参考文档 `references/workflow-orchestrator-regex-pitfalls.md`

### v2.0.0 (2026-06-10)

- **P0**: 全部脚本从 Node.js 重写为 Python（3.11 兼容）
- **P0**: 集成 Hermes delegate_task，编排器输出可操作的调度指令
- **P0**: OutputValidator._getOutputForSkill() 不再返回空字符串，真正读取项目文件
- **P1**: 清理 SKILL.md 3倍重复的 Dashboard 配置
- **P1**: YAML 解析兼容 ```yaml 代码块包裹和裸写两种格式
- **P1**: 阶段正则支持英文 `Stage N:` 和中文 `阶段 N:`
- **P1**: 删除空壳 dashboard-server.js 和 orchestrator-cli.js
- **P2**: ContextManager 加文件锁（fcntl）防止并发写冲突
- **P2**: autoFix() 真正实现（为缺失章节/文件添加占位符）
- **P2**: 验证规则支持多语言章节名

### v1.0.0 (2026-04-26)

- 初始版本（Node.js）
- 上下文管理
- 流程编排
- 质量保证
