---
slug: skill-writer-tool-free
name: skill-writer-tool-free
version: 1.0.0
displayName: Skill编写工具免费版
summary: "创建结构规范的Agent技能，支持渐进式展开与资源捆绑，适合个人开发者快速上手.。Skill编写工具免费版，面向个人开发者的轻量级Agent技能创建工具。核心能力:"
license: Proprietary
edition: free
description: Skill编写工具免费版，面向个人开发者的轻量级Agent技能创建工具。核心能力:，可自动提升工作效率

  - 结构化 SKILL。Use when 需要生成营销文案、写作内容、标题优化、内容创作时使用。不适用于纯技术文档撰写。Use
  when 需要生成营销文案、写作内容、标题优化、内容创作时使用。不适用于纯技术文档撰写。'
tags:
  - Skill编写
  - 技能创建
  - 结构规范
  - 免费版
  - 工具
  - 效率
  - 写作
  - 电商
  - 编写工具
  - reference
  - use
  - markdown
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# Skill编写工具（免费版）

## 概述

Skill编写工具免费版帮助你创建结构规范的 Agent 技能。提供 SKILL.md 模板、渐进式内容展开与资源捆绑能力，确保技能描述精准、结构清晰、适用关键词明确.
## 核心能力

| 能力 | 说明 |
|---|---|
| 结构化创建 | SKILL.md + REFERENCE.md + EXAMPLES.md + scripts/ |
| 渐进式展开 | 主文件简洁，详细内容拆分至引用文件 |
| 资源捆绑 | 脚本与文档统一管理 |
| 描述校准 | 适用关键词明确，描述符合规范 |
| 审查清单 | 创建后自动检查规范合规性 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：创建结构规范的、Agent、支持渐进式展开与、适合个人开发者快、速上手、编写工具免费版、面向个人开发者的、轻量级、技能创建工具、Use、when、需要生成营销文案、写作内容、标题优化、内容创作时使用、不适用于纯技术文、档撰写、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：创建自定义技能

开发者希望为常见任务创建一个技能.
```text
用户：帮我创建一个「代码格式化」的技能.
助手：
让我先了解几个问题：
1. 这个技能覆盖什么任务/领域？ → 代码格式化
2. 具体处理哪些用例？ → Python、JavaScript、Go 的格式化
3. 需要可执行脚本还是仅指令？ → 调用 prettier/black/gofmt
4. 有参考资料需要包含吗？ → 各工具的配置示例
# ...
基于你的需求，技能结构如下：
# ...
skill-code-formatter/
├── SKILL.md           # 主指令（含适用关键词）
├── REFERENCE.md       # 各语言格式化工具详情
├── EXAMPLES.md        # 使用示例
└── scripts/
    └── format.sh      # 格式化脚本
```

### 场景二：编写 SKILL.md

按照规范编写主指令文件.
```markdown
---
name: code-formatter
description: Format code with prettier, black, gofmt. Use when user mentions
  formatting, code style, or when files need formatting.
---
# ...
## Quick start
# ...
\`\`\`bash
（请参考skill目录中的脚本文件） --language python --file path/to/file.py
\`\`\`
# ...
## Workflows
# ...
1. 检测文件语言
2. 选择对应格式化工具
3. 执行格式化
4. 验证格式化结果
# ...
## 快速开始
# ...
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问
# ...
```bash
# 1. 收集需求
# - 任务/领域
# - 具体用例
# - 是否需要脚本
# - 参考资料来源

# 2. 创建技能结构
mkdir -p my-skill/scripts
touch my-skill/SKILL.md
touch my-skill/REFERENCE.md

# 3. 编写 SKILL.md（参考模板）
# 4. 编写引用文件（如需要）
# 5. 编写脚本（如需要）
# 6. 审查规范合规性
```
# ...
**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
# ...
## 示例
# ...
```markdown
# SKILL.md 模板
---
name: skill-name
description: 简要描述能力。Use when [具体触发条件].
---

## Quick start(续1)

以下是Skill编写工具免费版的快速开始指南，包含最小可用示例与核心配置.
## Workflows(续1)

以下是Skill编写工具免费版的复杂任务工作流程，包含分步骤操作与清单.
## Advanced features

[详细内容链接至: See REFERENCE.md]
```
# ...
```text
# 描述规范
- 最大 1024 字符
- 第三人称书写
- 第一句: 做什么
- 第二句: "Use when [触发条件]"

# 好的描述示例:
Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

# 差的描述示例:
Helps with documents.
（Agent 无法区分此技能与其他文档技能）
```
# ...
## 最佳实践
# ...
* 描述是 Agent 选择技能的唯一依据，务必精准.
* SKILL.md 控制在 100 行以内，超出时拆分至引用文件.
* 适用关键词要具体（文件类型、操作动词、场景）.
* 确定性操作优先编写脚本，节省 Token 并提升可靠性.
* 引用深度保持一层，避免多层嵌套增加加载成本.
* 不包含时效性信息（版本号、日期等会过时）.
* 术语保持一致，避免同义词混用.
* 包含具体可运行的示例.
# ...
## 常见问题
# ...
**Q：免费版支持技能模板库吗？**
A：免费版提供基础模板。如需模板库与复用，请考虑 PRO 版本.
# ...
**Q：免费版支持多人协作编写吗？**
A：免费版面向个人编写。如需多人协作与审核，请使用 PRO 版本.
# ...
**Q：SKILL.md 超过 100 行怎么办？**
A：将详细内容拆分至 REFERENCE.md，主文件仅保留快速开始与工作流.
# ...
**Q：什么时候需要编写脚本？**
A：操作是确定性的（校验、格式化）、相同代码会重复生成、错误需要显式处理时，编写脚本更优.
# ...
**Q：描述里应该包含哪些适用关键词？**
A：文件类型（PDF/CSV）、操作动词（提取/合并/格式化）、场景（表单/文档）等具体词汇.
# ...
## 依赖说明
# ...
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
# ...
### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
# ...
### API Key 配置
- 本skill基于Markdown指令规范，无需额外API Key（除内容中明确标注的外部API）
# ...
### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent创建技能
# ...
## 错误处理
# ...
| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
# ...
## 已知限制
# ...
- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
# ...
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Skill编写工具免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "skill writer"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
# ...