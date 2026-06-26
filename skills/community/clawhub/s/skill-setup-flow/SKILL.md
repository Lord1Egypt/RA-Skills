# skill-setup-flow

为已安装的 OpenClaw 技能创建标准化的设置流程。

## 用途

当用户说：
- "为 X 技能创建设置流程"
- "初始化 X 技能的配置"
- "设置 X 技能"
- "启用 X 技能"

此技能提供标准化的设置步骤，包括：
1. 读取技能的 SKILL.md 了解需求
2. 创建必要的目录结构
3. 创建配置文件模板
4. 更新 SOUL.md/AGENTS.md 集成说明
5. 记录设置日志

## 使用方法

```bash
# 为已安装的技能创建设置流程
为 self-improving 创建设置流程
初始化 proactive-agent 配置
设置 weather 技能
```

## 设置流程模板

### 步骤 1: 读取技能文档
```
读取 ~/skills/{skill-name}/SKILL.md
```

### 步骤 2: 创建目录结构
```bash
mkdir -p ~/skills/{skill-name}/config
mkdir -p ~/skills/{skill-name}/data
```

### 步骤 3: 创建配置文件
- `config.md` — 配置选项
- `state.md` — 运行时状态
- `memory.md` — 技能特定记忆

### 步骤 4: 集成到核心文件
- 更新 `SOUL.md` 添加技能特定行为
- 更新 `AGENTS.md` 添加使用说明
- 更新 `MEMORY.md` 记录设置事件

### 步骤 5: 记录设置日志
在 `skills/{skill-name}/setup-log.md` 记录：
- 设置日期
- 配置选项
- 创建的文件
- 更新的核心文件

## 示例：Self-Improving Agent 设置

```markdown
# Self-Improving Agent 设置流程

## 1. 读取技能文档
✅ 读取 ~/skills/self-improving/SKILL.md

## 2. 创建目录
✅ ~/self-improving/
   ├── memory.md (HOT tier)
   ├── corrections.md (纠正日志)
   ├── index.md (索引)
   ├── heartbeat-state.md (心跳状态)
   ├── projects/ (项目特定)
   ├── domains/ (领域特定)
   └── archive/ (归档)

## 3. 创建核心文件
✅ memory.md — 初始偏好和规则
✅ corrections.md — 纠正日志模板
✅ index.md — 文件索引
✅ heartbeat-state.md — 心跳跟踪

## 4. 集成到核心文件
✅ SOUL.md — 添加 Self-Improving 章节
✅ AGENTS.md — 添加使用说明和命令

## 5. 设置完成
- 日期：2026-04-04
- 状态：✅ 完成
- 测试：添加首条偏好记录
```

## 通用设置流程

对于任何技能，遵循以下模式：

### A. 配置型技能（需要 API 密钥等）
1. 创建 `config.md` 模板
2. 列出所需配置项
3. 提供配置示例
4. 测试连接

### B. 数据型技能（需要数据存储）
1. 创建数据目录
2. 创建索引文件
3. 创建数据模板
4. 设置自动保存

### C. 行为型技能（改变 AI 行为）
1. 更新 SOUL.md
2. 添加触发条件
3. 创建行为日志
4. 设置反馈循环

### D. 工具型技能（提供新工具）
1. 创建工具配置文件
2. 添加使用示例
3. 更新 TOOLS.md
4. 创建快速参考

## 设置日志模板

```markdown
# {Skill Name} 设置日志

## 设置日期
{YYYY-MM-DD}

## 技能信息
- 来源：{clawhub/github/本地}
- 版本：{version}
- 路径：~/skills/{skill-name}/

## 创建的文件
- [ ] {file1}
- [ ] {file2}

## 更新的核心文件
- [ ] SOUL.md
- [ ] AGENTS.md
- [ ] MEMORY.md
- [ ] TOOLS.md

## 配置选项
- 选项 1: {value}
- 选项 2: {value}

## 测试结果
- [ ] 基本功能测试通过
- [ ] 集成测试通过
- [ ] 心跳测试通过（如适用）

## 下一步
- [ ] 配置心跳（如需要）
- [ ] 添加自定义规则
- [ ] 测试学习流程
```

## 快速命令

创建技能时自动包含：

```markdown
## 🚀 快速启动

1. **基础设置** - `为 {skill} 创建设置流程`
2. **配置** - `配置 {skill} 的 {选项}`
3. **测试** - `测试 {skill} 功能`
4. **查看状态** - `{skill} 状态`
```

## 最佳实践

1. **最小化初始配置** - 只创建必要的文件
2. **提供默认值** - 所有配置都有合理的默认值
3. **记录一切** - 设置日志要详细
4. **可逆操作** - 提供卸载/重置方法
5. **测试导向** - 设置完成后立即测试

## 相关文件

- `~/skills/{skill-name}/SKILL.md` — 技能文档
- `~/skills/{skill-name}/setup-log.md` — 设置日志
- `~/skills/{skill-name}/config.md` — 配置选项
- `~/skills/{skill-name}/state.md` — 运行状态

## 示例调用

```
为 self-improving 创建设置流程
为 proactive-agent 创建设置流程
为 weather 创建设置流程
为 news-summary 创建设置流程
```

---

_此技能提供标准化的技能设置流程，确保每个技能都能正确配置和集成。_
