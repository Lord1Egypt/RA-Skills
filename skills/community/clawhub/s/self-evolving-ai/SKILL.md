---
slug: self-evolving-ai
name: self-evolving-ai
version: "1.0.0"
displayName: 自我进化AI
summary: 自动捕获经验与错误,智能分层记忆,模式复发追踪,按需加载降本增效。
license: MIT
description: |-
  自我进化AI是一个让智能体从每次交互中持续学习并自主改进的记忆与进化系统。针对传统自改进代理"记不住、用不上、成本高"三大痛点,构建了智能分层记忆、自动痛点检测、模式复发追踪和按需加载四大核心能力。

  核心能力包括:经验/错误/特性请求三类结构化记忆;基于语义的自动分类与优先级评估;跨会话模式复发检测与晋升机制;分层文档加载策略(快速入门→标准用法→高级配置);一键晋升到项目记忆与可复用技能。

  适用场景:长期运行的AI代理项目、多人协作的代码仓库、需要积累领域知识的研发团队、希望减少重复犯错的独立开发者、需要将隐性经验转化为显性规则的技术团队。

  差异化亮点:相比原始版本,新增智能痛点检测触发器(自动识别纠正/知识缺口/最佳实践)、模式复发追踪(Recurrence-Count跨任务统计+30天窗口晋升规则)、按需加载机制(主文档<150行,详情分层引用)、token成本预估与优化建议、故障排查决策树、分层评审清单。

  触发关键词:自我进化、经验捕获、错误学习、模式追踪、记忆晋升、持续改进、self-evolving、learnings、corrections、pattern-detection
tags:
- 智能代理
- 记忆管理
- 持续改进
- 自主学习
tools:
- read
- exec
---

# 自我进化AI

让智能体从每次交互中持续学习,自动捕获经验、错误与纠正,并通过模式复发追踪将高频问题晋升为项目级规则。

## 快速开始(3步启用)

1. **初始化记忆目录**
```bash
mkdir -p .learnings
```

2. **识别情境并记录**(参见下方决策表)

3. **定期评审与晋升**(参见晋升机制)

## 情境决策表

| 情境 | 动作 | 目标文件 |
|------|------|----------|
| 任务执行中主动修复失败 | 使用自愈流程,记录到 HEALS.md | `.learnings/HEALS.md` |
| 过去命令/操作失败(非自愈中) | 记录错误条目 | `.learnings/ERRORS.md` |
| 用户纠正你的回答 | 记录学习条目,类别=correction | `.learnings/LEARNINGS.md` |
| 用户提出缺失功能 | 记录特性请求 | `.learnings/FEATURE_REQUESTS.md` |
| 外部API/工具调用失败 | 记录错误条目,含集成详情 | `.learnings/ERRORS.md` |
| 自愈规则满足晋升条件 | 晋升为项目规则 | `CLAUDE.md`/`AGENTS.md` |
| 发现知识已过时 | 记录学习条目,类别=knowledge_gap | `.learnings/LEARNINGS.md` |
| 发现更优方案 | 记录学习条目,类别=best_practice | `.learnings/LEARNINGS.md` |
| 重复出现的模式 | 更新条目,递增Recurrence-Count | `.learnings/LEARNINGS.md` |
| 与已有条目相似 | 添加See Also链接,考虑提升优先级 | 对应条目 |
| 广泛适用的学习 | 晋升到项目记忆 | `CLAUDE.md`/`AGENTS.md` |

## 记录格式

### 学习条目

追加到 `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601时间戳
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述学到了什么

### Details
完整上下文:发生了什么、哪里错了、正确做法是什么

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001(关联已有条目)
- Pattern-Key: simplify.dead_code | harden.input_validation(可选,用于复发模式追踪)
- Recurrence-Count: 1(可选)
- First-Seen: 2025-01-15(可选)
- Last-Seen: 2025-01-15(可选)

---
```

### 错误条目

追加到 `.learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601时间戳
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
简要描述什么失败了

### Error
```
实际错误消息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 相关环境详情

### Suggested Fix
如果能识别,什么可能解决这个问题

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001(如复发)

---
```

### 特性请求条目

追加到 `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601时间戳
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要做什么

### User Context
为什么需要,在解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何构建,可能扩展什么

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID生成规则

格式: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN`(学习)、`ERR`(错误)、`FEAT`(特性)
- YYYYMMDD: 当前日期
- XXX: 顺序号或随机3字符(如 `001`、`A7B`)

示例: `LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 条目状态流转

```
pending → in_progress → resolved
                     ↘ wont_fix(附原因)
                     ↘ promoted(晋升到项目记忆)
                     ↘ promoted_to_skill(提取为可复用技能)
```

修复问题后更新条目:

1. 将 `**Status**: pending` 改为 `**Status**: resolved`
2. 在Metadata后添加解决块:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 或 #42
- **Notes**: 简要描述做了什么
```

## 晋升到项目记忆

当学习具有广泛适用性(非一次性修复)时,晋升为永久项目记忆。

### 晋升时机

- 学习适用于多个文件/功能
- 任何贡献者(人或AI)都应知道的知识
- 防止重复犯错
- 记录项目特定约定

### 晋升目标

| 目标 | 适合内容 |
|------|----------|
| `CLAUDE.md` | 项目事实、约定、注意事项 |
| `AGENTS.md` | 代理特定工作流、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot的项目上下文与约定 |

### 晋升步骤

1. **提炼**学习为简洁规则或事实
2. **添加**到目标文件的适当章节(必要时创建文件)
3. **更新**原始条目:
   - `**Status**: pending` → `**Status**: promoted`
   - 添加 `**Promoted**: CLAUDE.md`

### 晋升示例

**学习条目**(冗长):
> 项目使用 pnpm workspaces。尝试 `npm install` 但失败。
> Lock file 是 `pnpm-lock.yaml`。必须用 `pnpm install`。

**CLAUDE.md中**(简洁):
```markdown
## 构建与依赖
- 包管理器: pnpm(非npm) - 使用 `pnpm install`
```

## 模式复发追踪(差异化核心)

### 复发检测工作流

记录与已有条目相似的内容时:

1. **先搜索**: `grep -r "keyword" .learnings/`
2. **链接条目**: 在Metadata添加 `**See Also**: ERR-20250110-001`
3. **递增计数**: 如有Pattern-Key,递增 `Recurrence-Count`
4. **提升优先级**: 如问题持续复发,提升优先级
5. **考虑系统性修复**: 复发问题通常表明:
   - 文档缺失(→ 晋升到 CLAUDE.md)
   - 自动化缺失(→ 添加到 AGENTS.md)
   - 架构问题(→ 创建技术债工单)

### 晋升规则(系统提示反馈)

当以下条件**全部满足**时,将复发模式晋升到代理上下文/系统提示文件:

- `Recurrence-Count >= 3`
- 跨至少2个不同任务出现
- 在30天窗口内发生

晋升目标:
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

将晋升规则写成简短的预防规则(编码前/中做什么),而非冗长的事故报告。

### 简化与加固馈送

从简化与加固工作流摄入复发模式:

1. 读取任务摘要中的候选模式
2. 对每个候选,使用 `pattern_key` 作为稳定去重键
3. 搜索 `.learnings/LEARNINGS.md` 中已有该键的条目:
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 找到则:递增Recurrence-Count、更新Last-Seen、添加See Also链接
5. 未找到则:创建新 `LRN-...` 条目,设 `Source: simplify-and-harden`,设Pattern-Key、Recurrence-Count: 1、First-Seen/Last-Seen

## 自动检测触发器

自动在以下情况记录:

### 纠正(→ learning,类别=correction)
- "不对,那不是..."
- "实际上应该是..."
- "你错了关于..."
- "那个过时了..."

### 特性请求(→ feature request)
- "你能不能也..."
- "我希望你能..."
- "有没有办法..."
- "为什么不能..."

### 知识缺口(→ learning,类别=knowledge_gap)
- 用户提供了你不知道的信息
- 你引用的文档已过时
- API行为与你的理解不同

### 错误(→ error entry)
- 命令返回非零退出码
- 异常或堆栈跟踪
- 意外输出或行为
- 超时或连接失败

## 优先级指南

| 优先级 | 使用场景 |
|--------|----------|
| `critical` | 阻塞核心功能、数据丢失风险、安全问题 |
| `high` | 重大影响、影响常用工作流、复发问题 |
| `medium` | 中等影响、有变通方案 |
| `low` | 轻微不便、边缘情况、可有可无 |

## 区域标签

用于按代码区域过滤学习:

| 区域 | 范围 |
|------|------|
| `frontend` | UI、组件、客户端代码 |
| `backend` | API、服务、服务端代码 |
| `infra` | CI/CD、部署、Docker、云 |
| `tests` | 测试文件、测试工具、覆盖率 |
| `docs` | 文档、注释、README |
| `config` | 配置文件、环境、设置 |

## 定期评审

### 评审时机
- 开始新主要任务前
- 完成功能后
- 在有历史学习的区域工作时
- 活跃开发期间每周

### 快速状态检查
```bash
grep -h "Status**: pending" .learnings/*.md | wc -l
grep -B5 "Priority**: high" .learnings/*.md | grep "^## ["
grep -l "Area**: backend" .learnings/*.md
```

### 评审动作
- 解决已修复项
- 晋升适用学习
- 链接相关条目
- 升级复发问题

## 自动技能提取

当学习足够有价值可成为可复用技能时,使用提供的助手提取。

### 提取标准(满足任一即可)

| 标准 | 描述 |
|------|------|
| 复发 | 有2+个相似问题的See Also链接 |
| 已验证 | 状态为resolved且有有效修复 |
| 非显而易见 | 需要实际调试/调查才发现 |
| 广泛适用 | 非项目特定,跨代码库有用 |
| 用户标记 | 用户说"把这个保存为技能" |

### 提取工作流

1. **识别候选**: 学习满足提取标准
2. **运行助手**(或手动创建):
   ```bash
   ./skills/self-evolving-ai/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-evolving-ai/scripts/extract-skill.sh skill-name
   ```
3. **定制SKILL.md**: 用学习内容填充模板
4. **更新学习**: 设状态为 `promoted_to_skill`,添加 `Skill-Path`
5. **验证**: 在新会话中读取技能确保自包含

### 技能质量门禁

提取前验证:
- [ ] 解决方案已测试且有效
- [ ] 描述清晰无需原始上下文
- [ ] 代码示例自包含
- [ ] 无项目特定硬编码值
- [ ] 遵循技能命名约定(小写、连字符)

## 多代理支持

本技能跨不同AI编码代理工作,具有代理特定激活。

### Claude Code
- **激活**: 钩子(UserPromptSubmit、PostToolUse)
- **设置**: `.claude/settings.json` 配置钩子
- **检测**: 通过钩子脚本自动

### Codex CLI
- **激活**: 钩子(`UserPromptSubmit`、`PostToolUse`) — 实验性,需在config.toml启用 `codex_hooks = true`
- **设置**: `<repo>/.codex/hooks.json` 或 `~/.codex/hooks.json`
- **检测**: 通过钩子脚本自动
- **回退**: 如钩子不可用,将自改进指导添加到 `AGENTS.md`

### GitHub Copilot
- **激活**: 指令文件(Copilot钩子可记录日志但不能注入上下文)
- **设置**: 添加到 `.github/copilot-instructions.md`:

```markdown
## 自我进化

解决非显而易见的问题后,考虑记录到 `.learnings/`:
1. 使用自我进化AI技能格式
2. 用See Also链接相关条目
3. 将高价值学习晋升为技能

在聊天中询问:"应该把这个记录为学习吗?"
```

### 钩子快速设置(Claude Code)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/skills/self-evolving-ai/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/skills/self-evolving-ai/scripts/error-detector.sh"
      }]
    }]
  }
}
```

钩子接收事件payload为stdin的JSON。错误检测器从JSON解析 `tool_response` 并返回提醒作为 `additionalContext` JSON输出。

## 最佳实践

1. **立即记录** - 问题发生后上下文最鲜活
2. **具体明确** - 未来代理需要快速理解
3. **包含复现步骤** - 特别是错误
4. **链接相关文件** - 使修复更容易
5. **建议具体修复** - 而非仅"调查"
6. **使用一致类别** - 启用过滤
7. **积极晋升** - 如有疑问,添加到CLAUDE.md
8. **定期评审** - 过时的学习失去价值

## Gitignore选项

**保持学习本地**(每开发者):
```gitignore
.learnings/
```

**在仓库中追踪**(团队共享): 不添加到.gitignore,学习成为共享知识。

**混合**(追踪模板,忽略条目):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 常见问题FAQ

**Q: 学习条目太多导致上下文膨胀怎么办?**
A: 使用按需加载机制。主文档只保留快速参考表,详细条目通过grep按需检索。定期将高价值学习晋升到CLAUDE.md后,可在.learnings/中标记为promoted,减少重复加载。

**Q: 如何判断学习是否应该晋升?**
A: 满足以下任一条件即考虑晋升:跨2+任务复发(Recurrence-Count>=3)、适用于多个文件/功能、任何贡献者都应知道、防止重复犯错。

**Q: 不同代理平台如何兼容?**
A: 核心记忆格式(LEARNINGS.md/ERRORS.md/FEATURE_REQUESTS.md)跨平台通用。平台差异仅在激活方式:Claude Code用钩子、Codex用hooks.json、Copilot用指令文件。

**Q: 模式复发追踪如何避免误报?**
A: 使用Pattern-Key作为稳定去重键,要求Recurrence-Count>=3且跨2个不同任务且30天窗口内才晋升。单一任务内的重复不计入。

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 钩子未触发提醒 | 脚本路径错误 | 检查`${CLAUDE_PROJECT_DIR}/.claude/skills/self-evolving-ai/scripts/`路径是否存在 |
| grep搜索无结果 | 条目ID格式不匹配 | 确认ID格式为`TYPE-YYYYMMDD-XXX` |
| 晋升后CLAUDE.md重复 | 未更新原条目状态 | 将原条目Status改为promoted并添加Promoted字段 |
| Recurrence-Count未递增 | Pattern-Key不一致 | 确保相同模式使用相同的Pattern-Key字符串 |
| 记忆目录被git追踪但不想提交 | 未配置gitignore | 添加`.learnings/`到.gitignore |
| PostToolUse钩子无输出 | 未返回additionalContext | 确保脚本输出JSON格式的additionalContext |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Shell**: bash(钩子脚本需要)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| bash | 运行时 | 可选(钩子功能需要) | 系统自带或安装Git Bash |
| grep | 工具 | 可选(搜索功能需要) | 系统自带 |

### API Key 配置
- 本技能基于Markdown指令,无需额外API Key

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务。核心记忆功能仅需Markdown,钩子与脚本功能需要exec能力。
