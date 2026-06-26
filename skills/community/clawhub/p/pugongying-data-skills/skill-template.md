# Skill 标准化模板

本模板定义蒲公英数据开发Skill套件中所有Skill的编写规范。

## 必须包含的章节（按顺序）

### 1. YAML Frontmatter（必需）

```yaml
---
name: skill-id
description: |
  Skill 一句话描述。
  当用户需要XXX时触发。
  触发词：关键词1、关键词2、关键词3。
---
```

**要求**:
- `name`: 使用小写字母和连字符，如 `sql-assistant`
- `description`: 必须包含触发词，帮助Claude识别何时使用

### 2. 架构概览

使用统一的简洁风格：

```markdown
## 架构概览

```
输入 → [阶段1: 功能名] → [阶段2: 功能名] → [阶段3: 功能名] → 输出
            │                    │                    │
            ▼                    ▼                    ▼
       Agent:类型          Agent:类型           Agent:类型
```

| 阶段 | 命令 | Agent | 功能 |
|------|------|-------|------|
| 1 | /cmd-1 | general-purpose | 功能描述 |
| 2 | /cmd-2 | Explore | 功能描述 |
| 3 | /cmd-3 | general-purpose | 功能描述 |

**输出标准**: 生成 `{skill_name}_package.yaml` 便于下游 Skill 消费
```

### 3. 参考资料导航

统一格式：

```markdown
## 参考资料导航

| 何时读取 | 文件 | 内容 | 场景 |
|---------|------|------|------|
| 场景A | references/file-a.md | 内容描述 | 何时需要读取 |
| 场景B | references/file-b.md | 内容描述 | 何时需要读取 |
| 查看示例 | examples/ | 典型示例 | 学习使用方法 |
```

### 4. 快速开始

```markdown
## 快速开始

### 方式1：分阶段使用（推荐）

```bash
# 阶段1: XXX
/cmd-1 参数...

# 阶段2: XXX
/cmd-2 参数...

# 阶段3: XXX
/cmd-3 参数...
```

### 方式2：端到端工作流

```bash
# 启动完整工作流
/skill-name 端到端任务描述
```
```

### 5. 核心功能详解

每个功能必须包含：

```markdown
### 功能N: 功能名 (/command)

**Agent类型**: general-purpose|Explore
**工具权限**: Read, Grep, Glob, Edit, Write, Bash (按需)

**使用场景**:
- 场景1
- 场景2

**输入格式**:
```
/command 参数...
```

**输出规范**:
- 输出项1
- 输出项2
```

### 6. 标准输出格式（必需）

定义 `{skill_name}_package.yaml` 格式：

```markdown
## 标准输出格式

每个任务输出标准化的 `{skill_name}_package.yaml`：

```yaml
{skill_name}_package:
  version: "1.0"
  metadata:
    generated_by: "skill-name"
    generated_at: "2024-01-15T10:00:00Z"
    # 其他元数据字段...

  content:
    # 核心内容...

  downstream_specs:
    - target: "下游skill-id"
      input_file: "{skill_name}_package.yaml"
      mapping:
        - "字段A → 下游字段A"
```
```

### 7. 前置检查（如适用）

如果Skill需要特定前置信息：

```markdown
## 前置强制检查

执行 `/cmd` 前，必须完成以下检查：

```markdown
【强制】前置检查清单：
- [ ] **检查项1**
  - 如果未确认 → 必须主动询问
- [ ] **检查项2**

如果任何项未确认，必须先询问用户，禁止假设默认值。
```
```

### 8. 与下游 Skill 的联动（必需）

```markdown
## 与下游 Skill 的联动

本Skill输出后的下一步：

```bash
## 输出后的推荐操作

# 步骤1: 下游Skill调用（推荐）
/downstream-skill 基于以下输入：
- 输入文件: outputs/{skill_name}_package.yaml
- 关键字段: 字段说明
- 其他参数: 参数说明

# 步骤2: 另一个下游Skill调用
/another-skill ...
```
```

### 9. 示例快速索引（推荐）

```markdown
## 示例快速索引

| 需求场景 | 推荐命令 | 详情位置 |
|----------|----------|----------|
| 场景A | `/cmd-a 参数` | [功能1](#功能1) |
| 场景B | `/cmd-b 参数` | [功能2](#功能2) |
```

### 10. 项目初始化（可选）

如有初始化脚本：

```markdown
## 项目初始化

```bash
bash .claude/skills/{skill-name}/scripts/init-project.sh ./project-name "描述"
```

自动生成目录结构：
```
project-name/
├── PROJECT.md
├── outputs/           # 标准包输出目录
│   └── {skill_name}_package.yaml
└── ...
```
```

### 11. 故障排除

```markdown
## 故障排除

### Skill未触发
1. 检查skill文件路径
2. 确认Frontmatter格式正确
3. 重启Claude Code

### 输出不符合预期
1. 检查输入参数是否完整
2. 确认前置检查是否通过
3. 查看 references/ 中的规范
```

### 12. 示例场景

```markdown
## 示例场景

详见 [examples/](examples/) 目录：

| 示例 | 场景 | 流程 |
|------|------|------|
| example-a.md | 场景A | 步骤1 → 步骤2 → 步骤3 |
```

---

## 质量检查清单

发布前检查：

- [ ] 包含YAML Frontmatter（name + description）
- [ ] description包含触发词
- [ ] 定义了标准输出包格式
- [ ] 包含下游Skill联动说明
- [ ] 参考资料导航格式正确
- [ ] 所有Agent类型和权限已标注
- [ ] 包含故障排除章节
- [ ] 无README.md等冗余文件

---

## 与其他Skill的关系

```
requirement-analyst (标杆)
    ↓ requirement_package.yaml
    
sql-assistant
    ↓ sql_package.yaml
    
etl-assistant
    ↓ etl_package.yaml
    
dq-assistant
    ↓ dq_package.yaml
    
test-engineer
```

---

**参考实现**: requirement-analyst/SKILL.md (最成熟的实现)
