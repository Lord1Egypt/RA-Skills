---
slug: "skill-creator-free"
name: "skill-creator-free"
version: 1.0.1
displayName: "AI技能创建指南（免费版）"
summary: "免费版AI Skill创建指南，支持基础SKILL.md结构与Progressive Disclosure设计"
summary_zh: "免费版AI Skill创建指南，支持基础SKILL.md结构与Progressive Disclosure设计"
license: "MIT"
description: "|-. 适用于需要skill creator相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  创建有效AI Skill的基础指南（免费版）.
  覆盖Core Principles、SKILL.md结构设计与Progressive Disclosure基础概念.
  免费版不含完整Bundled Resources规范、Skill Creation Process脚本集成与不应包含内容指南.
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
tags:
  - - bundled
  - skill
  - creator
  - automation
  - productivity
  - resources
  - body
  - progressive
  - disclosure
  - level
category: "Automation"
pricing_tier: free
---
# AI技能创建指南（免费版）

创建有效AI Skill的基础指南，覆盖Core Principles与SKILL.md结构设计.
## 输入输出

**输入**: 用户提供skill创建需求，包括具体的concrete examples（skill应支持的功能描述与触发场景）、预期触发关键词或短语、skill名称建议、所需的bundled resources类型（（请参考skill目录中的脚本文件））、skill的复杂度与自由度偏好（High/Medium/Low freedom）.
**输出**: SKILL.md结构设计指导（含frontmatter中 `name` 与 `description` 字段的编写规范、body内容组织建议）、Progressive Disclosure三级加载系统设计建议（Level 1 Metadata约100 words / Level 2 SKILL.md body <5k words / Level 3 Bundled resources按需加载）、Bundled Resources基础组织方案（（请参考skill目录中的脚本文件））、Core Principles三大原则应用建议。免费版不含 `init_skill.py`/`package_skill.py` 脚本集成与完整规范（付费版专享）.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---|---|----|----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于指令驱动，无需额外API Key

### 可用性分类
- **分类**: MD+EXEC（）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行skill创建任务

## 核心能力

### Core Principles指导

提供skill创建的三大核心原则指导：

- **Concise is Key**：context window是公共资源，skill仅添加Claude不具备的知识。默认假设"Claude already is very smart"，对每段内容质疑"Does Claude really need this explanation?"与"Does this paragraph justify its token cost?"。优先用简洁examples替代冗长explanations.
- **Set Appropriate Degrees of Freedom**：根据任务的fragility和variability匹配specificity级别
  - High freedom（text-based instructions）：多种方法valid、决策依赖context时使用
  - Medium freedom（pseudocode or scripts with parameters）：有preferred pattern但允许variation时使用
  - Low freedom（specific scripts, few parameters）：操作fragile且error-prone、consistency关键时使用
- **Anatomy of a Skill**：每个skill由required的SKILL.md与optional的Bundled Resources组成

### SKILL.md结构设计
提供SKILL.md的标准结构与编写规范：

```text
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

- **Frontmatter（YAML）**：包含`name`和`description`字段。这是Claude读取以判断何时使用skill的唯一依据，必须清晰全面地描述skill是什么以及何时使用。`description`是primary triggering mechanism，应包含skill做什么与具体触发场景.
- **Body（Markdown）**：使用skill的instructions和guidance。仅在skill触发后加载.
### Progressive Disclosure设计
提供三级加载系统的设计原则：

- **Level 1 - Metadata（name + description）**：始终在context中（约100 words）
- **Level 2 - SKILL.md body**：skill触发时加载（<5k words）
- **Level 3 - Bundled resources**：Claude按需加载（Unlimited，因scripts可不读入context即执行）

保持SKILL.md body在essentials以内且<500 lines，接近限制时拆分内容。重要准则：references保持一级深度；长reference文件（>100 lines）顶部包含table of contents.
### Bundled Resources基础组织

提供三类bundled resources的基础说明：

- **Scripts（`scripts/`）**：Executable code用于需要deterministic reliability或反复重写的任务
- **References（`references/`）**：按需加载的文档与参考材料，大文件（>10k words）在SKILL.md中包含grep search patterns
- **Assets（`assets/`）**：用于输出而非加载入context的文件（templates、icons、fonts等）

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. **理解需求**：通过concrete examples明确skill应支持的功能与触发场景
2. **规划资源**：分析examples，列出reusable的scripts、references、assets清单
3. **编辑SKILL.md**：编写frontmatter（name + description）与body
4. **应用Progressive Disclosure**：保持SKILL.md <500 lines，detailed info移至references
5. **迭代优化**：实际使用后识别改进点并更新

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 示例

### 示例1：创建pdf-editor skill基础结构

```
需求: 用户频繁请求"帮我旋转这个PDF"
Step 1 - Understand:
  - 功能: PDF旋转
  - 触发: "rotate this PDF"、"rotate PDF"
Step 2 - Plan:
  - 分析: 旋转PDF每次都需重写相同代码
  - 资源: （请参考skill目录中的脚本文件）
Step 3 - 编写 SKILL.md:
  frontmatter:
    name: pdf-editor
    description: "PDF manipulation toolkit. Use when user needs to rotate, split, merge PDFs..."
  body:
    - 旋转PDF的使用说明
    - 引用 （请参考skill目录中的脚本文件）
Step 4 - Progressive Disclosure 检查:
  - SKILL.md <500 lines ✓
  - description含触发信息 ✓
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:-----|:-----|:-----|
| frontmatter格式错误 | YAML缩进或字段缺失 | 确保`name`和`description`字段存在且格式正确，description不为空 |
| skill未触发 | description缺少触发信息 | 在description中补充"when to use"信息与具体触发场景 |
| context window溢出 | SKILL.md过长或未使用Progressive Disclosure | 将detailed info移至references/，保持SKILL.md <5k words |

## 常见问题

### Q1: 免费版与付费版有何区别？
A: 免费版提供基础Core Principles、SKILL.md结构与Progressive Disclosure设计指导。不含完整Bundled Resources规范、Skill Creation Process（init_skill.py/package_skill.py脚本集成）、三种Progressive Disclosure Patterns详解与不应包含内容指南.
### Q2: description应该包含哪些内容？
A: description是skill的primary triggering mechanism，必须包含skill做什么与具体触发场景（when to use）。不应在body中放"When to Use"sections，因为body仅在触发后加载.
### Q3: Progressive Disclosure的三个层级如何划分？
A: Level 1是Metadata（name + description），始终在context（约100 words）；Level 2是SKILL.md body，skill触发时加载（<5k words）；Level 3是Bundled resources，Claude按需加载（unlimited，因scripts可执行不读入context）.
## 已知限制

- 不含init_skill.py与package_skill.py脚本集成，需手动创建skill目录结构
- 不含三种Progressive Disclosure Patterns（High-level guide、Domain-specific organization、Conditional details）详解
- 不含完整Bundled Resources组织规范与不应包含内容指南
- 依赖用户提供准确的concrete examples以理解skill需求
- SKILL.md的<500 lines限制对于复杂skill可能需要大量内容拆分

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "AI技能创建指南（免费版）处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "skill-creator"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
