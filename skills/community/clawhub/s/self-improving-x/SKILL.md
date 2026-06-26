---
name: self-improvement
description: |
  捕获学习成果、错误和纠正，以实现持续改进，当出现以下情况，使用本技能：
  (1) 命令或操作意外失败，
  (2) 用户纠正 '不，那是错的...'，'实际上...'），
  (3) 用户请求不存在的功能，
  (4) 外部 API 或工具失败，
  (5) 意识到其知识已过时或不正确，
  (6) 发现更好的方法处理重复任务。在执行重要任务前也要回顾学习记录。"
metadata:
  version: 0.1.0
---

# 自我改进技能

将学习成果和错误记录到 markdown 文件中以实现持续改进。编码智能体稍后可以将这些处理成修复补丁，重要的学习内容会被提升到项目记忆中。

## 快速参考

### 工作区结构

将这些文件注入每个会话：

```
<workspace-dir>
├── AGENTS.md          # 多智能体工作流，委托模式
├── SOUL.md            # 行为准则，人格，原则
├── TOOLS.md           # 工具能力，集成注意事项
├── MEMORY.md          # 长期记忆（仅主会话）
├── memory/            # 每日记忆文件
│   └── YYYY-MM-DD.md
└── .learnings/        # 此技能的学习记录文件
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

### 创建学习文件

创建目录 `.learnings`，然后从 `assets/` 复制：
- `LEARNINGS.md` — 纠正、知识差距、最佳实践
- `ERRORS.md` — 命令失败、异常
- `FEATURE_REQUESTS.md` — 用户请求的功能


### 自我改进工作流

当发生错误或纠正时：
1. 记录到 `.learnings/ERRORS.md`、`.learnings/LEARNINGS.md` 或 `.learnings/FEATURE_REQUESTS.md`
2. 回顾并将广泛适用的学习内容提升到：
    - `AGENTS.md` - 工作流和自动化

### 场景示例

| 场景 | 操作 |
|-----------|--------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正你 | 记录到 `.learnings/LEARNINGS.md`，类别为 `correction` |
| 用户需要缺失的功能 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到 `.learnings/ERRORS.md`，包含集成详情 |
| 知识已过时 | 记录到 `.learnings/LEARNINGS.md`，类别为 `knowledge_gap` |
| 发现更好的方法 | 记录到 `.learnings/LEARNINGS.md`，类别为 `best_practice` |
| 简化/强化重复模式 | 记录/更新 `.learnings/LEARNINGS.md`，来源 `simplify-and-harden`，带稳定的 `Pattern-Key` |
| 与现有条目相似 | 用 `**See Also**` 链接，考虑提升优先级 |
| 广泛适用的学习内容 | 提升到 `CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md` |
| 工作流改进 | 提升到 `AGENTS.md` |
| 工具陷阱 | 提升到 `TOOLS.md` |
| 行为模式 | 提升到 `SOUL.md` |


---

## 日志格式

### 学习条目

> 完整示例可查看 `./examples/LEARNINGS_example.md`

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] 类别

**记录时间**: ISO-8601 时间戳
**优先级**: low | medium | high | critical
**状态**: pending
**领域**: frontend | backend | infra | tests | docs | config

### 摘要
一句话描述学到的内容

### 详情
完整上下文：发生了什么、哪里错了、正确的是什么

### 建议操作
具体的修复或改进

### 元数据
- 来源: conversation | error | user_feedback
- 相关文件: path/to/file.ext
- 标签: tag1, tag2
- 另请参阅: LRN-20250110-001（如果与现有条目相关）
- Pattern-Key: simplify.dead_code | harden.input_validation（可选，用于重复模式跟踪）
- Recurrence-Count: 1（可选）
- First-Seen: 2025-01-15（可选）
- Last-Seen: 2025-01-15（可选）

---
```

### 错误条目

> 完整示例可查看 `./examples/ERRORS_example.md`

追加到 `.learnings/ERRORS.md`：

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**记录时间**: ISO-8601 时间戳
**优先级**: high
**状态**: pending
**领域**: frontend | backend | infra | tests | docs | config

### 摘要
失败内容的简要描述

### 错误
实际错误消息或输出

### 上下文
- 尝试的命令/操作
- 使用的输入或参数
- 相关环境详情

### 建议修复
如果可以识别，可能解决此问题的方法

### 元数据
- 可复现: yes | no | unknown
- 相关文件: path/to/file.ext
- 另请参阅: ERR-20250110-001（如果重复）

---
```

### 功能请求条目

> 完整示例可查看 `./examples/FEATURE_REQUESTS_example.md`

追加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**记录时间**: ISO-8601 时间戳
**优先级**: medium
**状态**: pending
**领域**: frontend | backend | infra | tests | docs | config

### 请求的功能
用户想要做什么

### 用户上下文
为什么需要它，正在解决什么问题

### 复杂度估计
simple | medium | complex

### 建议实现方式
如何构建，可以扩展什么

### 元数据
- 频率: first_time | recurring
- 相关功能: existing_feature_name

---
```

## ID 生成

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: `LRN`（学习）、`ERR`（错误）、`FEAT`（功能）
- YYYYMMDD: 当前日期
- XXX: 序列号或随机3个字符（例如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 解析条目

当问题被修复时，更新条目：

1. 将 `**状态**: pending` → `**状态**: resolved`
2. 在元数据后添加解析块：

```markdown
### 解析
- **已解决**: 2025-01-16T09:00:00Z
- **提交/PR**: abc123 或 #42
- **备注**: 所做工作的简要描述
```

其他状态值：
- `in_progress` - 正在积极处理
- `wont_fix` - 决定不处理（在解析备注中添加原因）
- `promoted` - 已提升到 CLAUDE.md、AGENTS.md 或 .github/copilot-instructions.md

## 提升到项目记忆

当学习内容具有广泛适用性（不是一次性修复）时，将其提升到永久项目记忆。

### 何时提升

- 学习内容适用于多个文件/功能
- 任何贡献者（人类或 AI）都应该知道的知识
- 防止重复犯错
- 记录项目特定的约定

### 提升目标

| 目标 | 属于那里的内容 |
|--------|-------------------|
| `AGENTS.md` | 智能体特定工作流、工具使用模式、自动化规则 |
| `SOUL.md` | 行为准则、沟通风格、原则 |
| `TOOLS.md` | 工具能力、使用模式、集成注意事项 |

### 如何提升

1. **提炼**学习内容为简洁的规则或事实
2. **添加**到目标文件的适当部分（需要时创建文件）
3. **更新**原始条目：
    - 将 `**状态**: pending` → `**状态**: promoted`
    - 添加 `**已提升**: CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

### 提升示例

**学习**（详细）：
> 项目使用 pnpm workspaces。尝试 `npm install` 但失败了。
> 锁文件是 `pnpm-lock.yaml`。必须使用 `pnpm install`。

**在 CLAUDE.md 中**（简洁）：
```markdown
## 构建和依赖
- 包管理器: pnpm（不是 npm）- 使用 `pnpm install`
```

**学习**（详细）：
> 修改 API 端点时，必须重新生成 TypeScript 客户端。
> 忘记这一点会导致运行时类型不匹配。

**在 AGENTS.md 中**（可操作）：
```markdown
## API 变更后
1. 重新生成客户端: `pnpm run generate:api`
2. 检查类型错误: `pnpm tsc --noEmit`
```

## 重复模式检测

如果记录的内容与现有条目相似：

1. **首先搜索**: `grep -r "keyword" .learnings/`
2. **链接条目**: 在元数据中添加 `**另请参阅**: ERR-20250110-001`
3. **提升优先级** 如果问题持续出现
4. **考虑系统性修复**: 重复问题通常表示：
    - 缺少文档（→ 提升到 CLAUDE.md 或 .github/copilot-instructions.md）
    - 缺少自动化（→ 添加到 AGENTS.md）
    - 架构问题（→ 创建技术债务工单）

## 简化和强化反馈

使用此工作流来吸收来自 `simplify-and-harden` 技能的重复模式，并将它们转化为持久的提示指导。

### 吸收工作流

1. 从任务摘要中读取 `simplify_and_harden.learning_loop.candidates`
2. 对于每个候选，使用 `pattern_key` 作为稳定的去重键
3. 搜索 `.learnings/LEARNINGS.md` 中具有该键的现有条目：
    - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 如果找到：
    - 增加 `Recurrence-Count`
    - 更新 `Last-Seen`
    - 添加 `See Also` 链接到相关条目/任务
5. 如果未找到：
    - 创建新的 `LRN-...` 条目
    - 设置 `来源: simplify-and-harden`
    - 设置 `Pattern-Key`、`Recurrence-Count: 1` 和 `First-Seen`/`Last-Seen`

### 提升规则（系统提示反馈）

当满足以下所有条件时，将重复模式提升到智能体上下文/系统提示文件：

- `Recurrence-Count >= 3`
- 在至少 2 个不同任务中看到
- 在 30 天窗口内发生

提升目标：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md`（适用于 OpenClaw 工作区级指导）

将提升的规则写为简短的预防规则（编码前/编码期间要做什么），
而不是长的事故报告。

## 定期回顾

在自然断点时回顾 `.learnings/`：

### 何时回顾
- 开始新的重要任务前
- 完成功能后
- 在有过去学习内容的领域工作时
- 活跃开发期间每周

### 快速状态检查
```bash
# 统计待处理项目
grep -h "状态**: pending" .learnings/*.md | wc -l

# 列出待处理的高优先级项目
grep -B5 "优先级**: high" .learnings/*.md | grep "^## \["

# 查找特定领域的学习内容
grep -l "领域**: backend" .learnings/*.md
```

### 回顾操作
- 解决已修复的项目
- 提升适用的学习内容
- 链接相关条目
- 升级重复问题

## 检测触发器

当你注意到以下情况时自动记录：

**纠正**（→ 类别为 `correction` 的学习）：
- "不，那是不对的..."
- "实际上，应该是..."
- "你错了..."
- "那已经过时了..."

**功能请求**（→ 功能请求）：
- "你也可以..."
- "我希望你能..."
- "有没有办法..."
- "为什么你不能..."

**知识差距**（→ 类别为 `knowledge_gap` 的学习）：
- 用户提供了你不知道的信息
- 你引用的文档已过时
- API 行为与你的理解不同

**错误**（→ 错误条目）：
- 命令返回非零退出码
- 异常或堆栈跟踪
- 意外输出或行为
- 超时或连接失败

## 优先级指南

| 优先级 | 何时使用 |
|----------|-------------|
| `critical` | 阻止核心功能、数据丢失风险、安全问题 |
| `high` | 重大影响、影响常见工作流、重复问题 |
| `medium` | 中等影响，存在变通方法 |
| `low` | 小麻烦、边缘情况、可有可无 |

## 领域标签

用于按代码库区域过滤学习内容：

| 领域 | 范围 |
|------|-------|
| `frontend` | UI、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | CI/CD、部署、Docker、云 |
| `tests` | 测试文件、测试工具、覆盖率 |
| `docs` | 文档、注释、README |
| `config` | 配置文件、环境、设置 |

## 最佳实践

1. **立即记录** - 上下文在问题发生后最清晰
2. **要具体** - 未来的智能体需要快速理解
3. **包含复现步骤** - 特别是对于错误
4. **链接相关文件** - 使修复更容易
5. **建议具体修复** - 不要只是"调查"
6. **使用一致的类别** - 便于过滤
7. **积极提升** - 如果有疑问，添加到 CLAUDE.md 或 .github/copilot-instructions.md
8. **定期回顾** - 过时的学习内容会失去价值

## Gitignore 选项

**保持学习内容本地化**（每个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要添加到 .gitignore - 学习内容成为共享知识。

**混合**（跟踪模板，忽略条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 自动技能提取

当学习内容有价值到可以成为可重用技能时，使用提供的辅助工具进行提取。

### 技能提取标准

当满足以下任何条件时，学习内容有资格进行技能提取：

| 标准 | 描述 |
|-----------|-------------|
| **重复** | 有到 2+ 类似问题的 `另请参阅` 链接 |
| **已验证** | 状态为 `resolved`，修复有效 |
| **非显而易见** | 需要实际调试/调查才能发现 |
| **广泛适用** | 不是项目特定的；对代码库有用 |
| **用户标记** | 用户说"保存为技能"或类似的话 |

### 提取工作流

1. **识别候选**: 学习内容满足提取标准
2. **创建技能**:
    ```
    .agents/skills/<skill-name>/SKILL.md
    ```
3. **自定义 SKILL.md**: 用学习内容填充模板，模版可查看 `./assets/SKILL-TEMPLATE.md`
4. **更新学习**: 将状态设置为 `promoted_to_skill`，添加 `Skill-Path`
5. **验证**: 在新会话中读取技能以确保它是独立的

### 提取检测触发器

注意以下表示学习内容应该成为技能的信号：

**在对话中：**
- "保存为技能"
- "我一直在遇到这个问题"
- "这对其他项目也有用"
- "记住这个模式"

**在学习条目中：**
- 多个 `另请参阅` 链接（重复问题）
- 高优先级 + 已解决状态
- 类别: `best_practice`，广泛适用
- 用户反馈称赞解决方案

### 技能质量门

提取前，验证：

- [ ] 解决方案已测试并有效
- [ ] 描述清晰，不需要原始上下文
- [ ] 代码示例是独立的
- [ ] 没有项目特定的硬编码值
- [ ] 遵循技能命名约定（小写，连字符）
