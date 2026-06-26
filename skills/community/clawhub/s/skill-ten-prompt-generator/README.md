# Skill Ten - Prompt Generator

> 基于 Claude Code Agent Skills 的 AI 提示词工程系统 - 10个场景化专家，自动路由，精准生成优秀提示词

## 项目简介

这是一个基于 Claude Code Agent Skills 技术的智能提示词生成系统。通过自然语言请求，系统会自动路由到对应的专业 Skill，帮助用户写出高质量的 AI 提示词。

### 核心特性

- **自动场景识别**：根据用户输入的关键词，自动匹配最合适的专家 Skill
- **10大场景覆盖**：涵盖视频生成、图像生成、AI编程、数据分析等主流应用场景
- **结构化框架**：每个场景都有经过验证的最佳实践框架和模板
- **双语支持**：完整支持中英文输入和输出

## 系统架构

```
用户请求 → 关键词识别 → 场景路由 → 对应 Skill → 优秀提示词
```

### 技术栈

- **Claude Code** - Anthropic 官方 AI 编程助手
- **Agent Skills** - Claude Code 的模块化功能扩展系统
- **Markdown** - 文档格式
- **YAML** - Skill 配置格式

## 10个专业场景

| 场景 | Skill 名称 | 核心能力 | 触发关键词示例 |
|------|-----------|---------|---------------|
| 视频生成 | `video-prompt-generator` | 7层结构、运镜术语、物理描述、JSON Prompt | Sora, Veo, 视频生成, 运镜 |
| 图像生成 | `image-prompt-generator` | 工单式协议、S-E-L-C框架、风格克隆 | Flux, Midjourney, 生图, 证件照 |
| AI编程 | `coding-prompt-assistant` | .cursorrules、TDD流程、P-R-E模式 | Cursor, .cursorrules, TDD, 重构 |
| 结构化提示词 | `json-prompt-architect` | JSON Schema、模块化模板、负向约束 | JSON, Schema, API对接, 批量生成 |
| 数据分析 | `data-analyst-prompter` | 代码执行、元数据注入、EDA优先 | Python, Pandas, CSV, 数据可视化 |
| 去AI味 | `humanizing-expert` | 负向词表、风格克隆、困惑度注入 | 去AI味, 人性化, 自然化 |
| 创意写作 | `creative-writing-coach` | 语料注射、认知建模、内心独白 | 角色扮演, 模仿风格, 小说, 剧本 |
| 深度调研 | `research-agent` | 递归规划、信源分级、批判性红队 | 调研, 竞品分析, 市场研究 |
| 实时语音 | `voice-conversation-coach` | 极简口语、重以此纠错、压力面试 | 语音对话, 雅思口语, 面试模拟 |
| 长期运行 | `long-running-orchestrator` | 初始化-执行分离、状态序列化 | Agent, 长期运行, 自动化, LangGraph |

## 使用方法

### 前置要求

1. 安装 [Claude Code](https://code.claude.com/)
2. 确保版本支持 Agent Skills (1.0+)
3. 将项目克隆到本地

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/skill-ten-prompt-generator.git
cd skill-ten-prompt-generator

# Skills 会自动被 Claude Code 发现
# 确认安装：在 Claude Code 中询问 "What Skills are available?"
```

### 使用示例

**示例1：生成视频提示词**

```
你: 帮我写一个 Sora 2 的视频提示词，赛博朋克风格的雨夜城市

系统: 自动调用 video-prompt-generator Skill

输出: 7层结构化的视频生成提示词
```

**示例2：创建编程规范**

```
你: 帮我写一个 Next.js 项目的 .cursorrules

系统: 自动调用 coding-prompt-assistant Skill

输出: 完整的 .cursorrules 配置文件
```

**示例3：去除AI痕迹**

```
你: 这段文字太AI了，帮我改得更自然一点

系统: 自动调用 humanizing-expert Skill

输出: 经过负向词表清洗和风格优化的自然文本
```

## 项目结构

```
skill-ten-prompt-generator/
├── .claude/
│   ├── CLAUDE.md              # 项目说明文档
│   ├── SKILL_ROUTING.md       # 场景路由指南
│   └── skills/                # 10个专业 Skills
│       ├── video-prompt-generator/
│       │   └── skill.md       # 视频生成专家
│       ├── image-prompt-generator/
│       │   └── skill.md       # 图像生成专家
│       ├── coding-prompt-assistant/
│       │   └── skill.md       # AI编程专家
│       ├── json-prompt-architect/
│       │   └── skill.md       # 结构化提示词专家
│       ├── data-analyst-prompter/
│       │   └── skill.md       # 数据分析专家
│       ├── humanizing-expert/
│       │   └── skill.md       # 去AI味专家
│       ├── creative-writing-coach/
│       │   └── skill.md       # 创意写作专家
│       ├── research-agent/
│       │   └── skill.md       # 深度调研专家
│       ├── voice-conversation-coach/
│       │   └── skill.md       # 实时语音专家
│       └── long-running-orchestrator/
│           └── skill.md       # 长期运行专家
├── skills.md                  # Agent Skills 技术文档
├── prompt_new.md              # 提示词工程完整指南
└── README.md                  # 本文件
```

## Skill 路由逻辑

系统根据用户输入中的关键词自动选择对应的 Skill：

```
用户输入
    ↓
关键词提取
    ↓
场景匹配
    ↓
┌─────────────────────────────────────────┐
│ Sora / Veo / 视频生成                   │ → video-prompt-generator
│ Flux / Midjourney / 生图                 │ → image-prompt-generator
│ Cursor / .cursorrules / 编程              │ → coding-prompt-assistant
│ JSON / Schema / 结构化                   │ → json-prompt-architect
│ Python / Pandas / 数据分析                │ → data-analyst-prompter
│ 去AI味 / 人性化 / 自然化                  │ → humanizing-expert
│ 角色扮演 / 模仿风格 / 创意写作             │ → creative-writing-coach
│ 调研 / 竞品分析 / 深度研究                │ → research-agent
│ 语音对话 / 雅思口语 / 面试                │ → voice-conversation-coach
│ Agent / 长期运行 / 自动化                 │ → long-running-orchestrator
└─────────────────────────────────────────┘
```

详细的路由逻辑请查看 [`.claude/SKILL_ROUTING.md`](.claude/SKILL_ROUTING.md)

## 贡献指南

欢迎贡献新的 Skill 或改进现有的 Skills！

### 添加新 Skill

1. 在 `.claude/skills/` 下创建新目录
2. 创建 `skill.md` 文件，包含：
   - YAML frontmatter（name, description）
   - Skill 说明文档
3. 更新 `SKILL_ROUTING.md` 添加路由规则
4. 更新 `CLAUDE.md` 和本 README

### Skill 模板

```yaml
---
name: your-skill-name
description: Brief description with trigger keywords
---

# Skill Name

## 核心理解
[说明这个场景的核心问题]

## 技巧1：[技巧名称]
[具体内容和模板]

## 工作流程
[步骤说明]

## 示例对话
[实际使用示例]
```

## 文档资源

- [Claude Code 官方文档](https://code.claude.com/)
- [Agent Skills 指南](skills.md)
- [提示词工程完整指南](prompt_new.md)
- [场景路由指南](.claude/SKILL_ROUTING.md)

## 许可证

MIT License

## 致谢

- Anthropic - Claude Code
- 饼干哥哥 - 提示词工程方法论
- 开源社区的贡献者

---

**让 AI 为你工作，而不是你为 AI 工作。**
