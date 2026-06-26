# 技能设置流程模板

## 使用方法

当用户说"为 {skill-name} 创建设置流程"时，按以下步骤执行：

## 步骤清单

### 1️⃣ 读取技能文档
```
读取 ~/skills/{skill-name}/SKILL.md
读取 ~/skills/{skill-name}/README.md (如有)
```

### 2️⃣ 分析技能类型

**配置型技能** (需要 API 密钥/配置):
- 创建 config.md
- 提供配置模板
- 指导用户配置

**数据型技能** (需要存储数据):
- 创建数据目录
- 创建索引和模板
- 设置自动保存

**行为型技能** (改变 AI 行为):
- 更新 SOUL.md
- 添加触发条件
- 创建行为日志

**工具型技能** (提供新工具/命令):
- 更新 TOOLS.md
- 创建快速参考
- 添加使用示例

### 3️⃣ 创建目录结构

```bash
# 基础目录（如需要）
mkdir -p ~/skills/{skill-name}/config
mkdir -p ~/skills/{skill-name}/data
mkdir -p ~/skills/{skill-name}/templates
```

### 4️⃣ 创建核心文件

根据技能类型创建：

#### memory.md (行为型技能)
```markdown
# {Skill} Memory

## Preferences
- 

## Patterns
- 

## Rules
- 
```

#### config.md (配置型技能)
```markdown
# {Skill} Configuration

## Required
- API_KEY: ""

## Optional
- OPTION_1: "default"
- OPTION_2: "default"
```

#### state.md (数据型技能)
```markdown
# {Skill} State

## Current State
status: initialized
last_run: never

## Statistics
runs: 0
errors: 0
```

#### setup-log.md (所有技能)
```markdown
# {Skill} Setup Log

## Setup Date
{YYYY-MM-DD}

## Version
{version}

## Files Created
- [ ] memory.md
- [ ] config.md
- [ ] state.md

## Core Files Updated
- [ ] SOUL.md
- [ ] AGENTS.md
- [ ] MEMORY.md

## Configuration
- option1: value1

## Tests
- [ ] Basic test passed
- [ ] Integration test passed

## Notes
- 
```

### 5️⃣ 更新核心文件

#### SOUL.md
添加技能特定的行为指导：

```markdown
## {Skill Name}

{技能特定的行为描述}
```

#### AGENTS.md
添加使用说明：

```markdown
## {Skill Name} Integration

{技能的使用说明和命令}
```

#### MEMORY.md
记录设置事件：

```markdown
### {YYYY-MM-DD}: 设置 {Skill Name}
- 技能来源：{source}
- 配置选项：{options}
- 状态：✅ 完成
```

### 6️⃣ 测试技能

运行基本测试：
- 读取配置
- 执行基本功能
- 验证集成

### 7️⃣ 提供快速参考

创建 `quickstart.md`:

```markdown
# {Skill} 快速参考

## 命令
- `命令 1` - 功能 1
- `命令 2` - 功能 2

## 示例
示例 1
示例 2

## 配置
- 配置文件：~/skills/{skill-name}/config.md
- 状态文件：~/skills/{skill-name}/state.md
```

## 完整示例

参考 `examples/self-improving-setup.md` 查看完整示例。

## 自动化脚本

对于常见技能，可以创建自动化脚本：

```bash
# setup-{skill-name}.sh
#!/bin/bash
SKILL_NAME="{skill-name}"
SKILL_PATH="~/skills/$SKILL_NAME"

# 创建目录
mkdir -p "$SKILL_PATH/config"
mkdir -p "$SKILL_PATH/data"

# 创建文件
echo "# Config" > "$SKILL_PATH/config.md"
echo "# State" > "$SKILL_PATH/state.md"
echo "# Log" > "$SKILL_PATH/setup-log.md"

# 更新核心文件
# (使用 edit 工具)

echo "Setup complete!"
```

## 检查清单

设置完成后确认：

- [ ] 目录结构正确
- [ ] 核心文件已创建
- [ ] SOUL.md 已更新
- [ ] AGENTS.md 已更新
- [ ] MEMORY.md 已记录
- [ ] 基本功能测试通过
- [ ] 提供了快速参考
- [ ] 用户知道如何使用

## 故障排除

**问题**: 技能未正确加载
**解决**: 检查 SKILL.md 格式，确保包含正确的触发器

**问题**: 配置文件丢失
**解决**: 重新运行设置流程，使用 setup-log.md 追踪

**问题**: 技能行为异常
**解决**: 检查 memory.md 和 state.md，重置为默认值

---

_使用此模板为任何 OpenClaw 技能创建标准化的设置流程。_
