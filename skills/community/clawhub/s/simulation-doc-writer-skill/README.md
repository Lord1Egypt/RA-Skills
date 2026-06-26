# simulation-doc-writer

`simulation-doc-writer` 是一个用于编写、审阅和完善中文通信仿真程序说明文档的 Agent Skill。生成的程序说明文档默认是 Markdown 文件，扩展名为 `.md`。它特别适合论文复现实验、研究生论文仿真代码说明、MATLAB 通信仿真程序整理、以及论文算法与代码实现的逐项对照。

## 功能描述

该 skill 会指导 AI 工具完成以下工作：

- 编写中文通信仿真程序说明文档，输出格式为 Markdown `.md` 文件。
- 对比论文与仿真程序，建立“论文算法/模型/仿真图”到代码文件和函数的映射关系。
- 逐一解释目标文件夹中的每个 `.m` 文件。
- 逐一解释每个 `.m` 文件中定义的每个函数，包括 local function/subfunction。
- 明确指出仿真环境对应的代码文件，例如主入口、参数设置、信道生成、码本生成、随机种子、Monte Carlo 次数、绘图和数据加载路径。
- 说明仿真目标、系统模型、信道模型、输入输出、关键参数、运行流程、结果指标、复现实验步骤和常见问题。
- 默认将生成的 Markdown 说明文档和配套输出文件放在用户提供论文所在的文件夹中；如果无法确定论文路径或文件夹不存在，会先询问保存位置。

## 适用场景

使用该 skill 的典型请求包括：

```text
使用 simulation-doc-writer 将论文 xxx.pdf 与文件夹下的仿真程序生成一个程序说明文档。
```

```text
帮我把这个 MATLAB 通信仿真代码整理成中文程序说明文档，并说明每个 .m 文件的作用。
```

```text
对比论文中的算法和代码实现，指出每个算法对应哪个函数。
```

## 目录结构

```text
simulation-doc-writer/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── references/
    └── communication-simulation-doc-template.md
```

其中：

- `SKILL.md`：skill 的核心触发描述和执行规则。
- `references/communication-simulation-doc-template.md`：中文通信仿真程序说明文档模板。
- `agents/openai.yaml`：Codex/OpenAI 相关的 UI 元数据。
- `README.md`：面向用户的安装和使用说明。

## 安装到 Codex

Codex 会从用户级 skill 目录中发现 skill。当前推荐放置路径为：

```text
~/.codex/skills/simulation-doc-writer/
```

在 Windows PowerShell 中，从当前本地目录复制到 Codex：

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force "C:\Users\zhangxiuyu\.codex\skills\simulation-doc-writer" "$HOME\.codex\skills\simulation-doc-writer"
```

如果你是从 Git 仓库下载：

```powershell
git clone <your-repo-url> skills-repo
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills-repo\simulation-doc-writer" "$HOME\.codex\skills\simulation-doc-writer"
```

安装后重启 Codex 或开启新会话，然后用类似下面的方式触发：

```text
使用 simulation-doc-writer 为这篇论文和仿真代码生成中文程序说明文档。
```

## 安装到 Claude Code

Claude Code 的自定义 skills 是文件系统目录。常用位置包括：

- 用户级：`~/.claude/skills/<skill-name>/SKILL.md`
- 项目级：`<project>/.claude/skills/<skill-name>/SKILL.md`

Windows PowerShell 用户级安装：

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force "C:\Users\zhangxiuyu\.codex\skills\simulation-doc-writer" "$HOME\.claude\skills\simulation-doc-writer"
```

macOS/Linux 用户级安装：

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/simulation-doc-writer ~/.claude/skills/simulation-doc-writer
```

项目级安装：

```bash
mkdir -p .claude/skills
cp -R /path/to/simulation-doc-writer .claude/skills/simulation-doc-writer
```

如果是在 Claude Code 会话启动后才创建新的顶层 skills 目录，建议重启 Claude Code 或开启新会话，以确保目录被发现。

## 安装到 OpenCode

OpenCode 支持 Agent Skills，并会读取以下位置：

- 项目级 OpenCode 路径：`.opencode/skill/<name>/SKILL.md`
- 用户级 OpenCode 路径：`~/.config/opencode/skill/<name>/SKILL.md`
- 项目级 Claude 兼容路径：`.claude/skills/<name>/SKILL.md`
- 用户级 Claude 兼容路径：`~/.claude/skills/<name>/SKILL.md`

macOS/Linux 用户级安装：

```bash
mkdir -p ~/.config/opencode/skill
cp -R /path/to/simulation-doc-writer ~/.config/opencode/skill/simulation-doc-writer
```

Windows PowerShell 用户级安装：

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode\skill" | Out-Null
Copy-Item -Recurse -Force "C:\Users\zhangxiuyu\.codex\skills\simulation-doc-writer" "$HOME\.config\opencode\skill\simulation-doc-writer"
```

项目级安装：

```bash
mkdir -p .opencode/skill
cp -R /path/to/simulation-doc-writer .opencode/skill/simulation-doc-writer
```

安装后，OpenCode 通常会根据请求上下文自动选择 skill；也可以在提示词中显式写：

```text
Use simulation-doc-writer to generate a Chinese simulation program manual.
```

## 使用通用 Agent Skills CLI

部分工具链支持通过 `npx skills` 安装跨工具 Agent Skills。若你已经将该 skill 发布到 GitHub 或兼容的 skill registry，可尝试：

```bash
npx skills install <repo-or-skill-url>
```

或：

```bash
npx skills i <repo-or-skill-url>
```

这种方式适合一次性安装到多个支持 Agent Skills 的工具中；若安装失败，优先使用上面的“复制 skill 文件夹到目标目录”方式。

## 使用示例

```text
使用 simulation-doc-writer 将论文 "F:\文献\研究生毕业论文\仿真结果\仿真代码\URA.pdf" 与文件夹下的仿真程序 "F:\文献\研究生毕业论文\仿真结果\仿真代码\URA" 生成一个程序说明文档。
```

期望输出包括：

- 文档概述。
- 论文算法/模型到代码映射表。
- 仿真环境对应代码文件。
- MATLAB 文件与函数说明表。
- 系统模型、信道模型和程序流程。
- 关键算法说明。
- 参数表、输入输出说明、结果指标说明。
- 复现实验步骤、常见问题和限制。

## 更新 skill

如果你修改了 `SKILL.md` 或 `references/communication-simulation-doc-template.md`，建议：

1. 保持 `SKILL.md` 的 YAML frontmatter 中至少包含 `name` 和 `description`。
2. 避免把大量细节都放在 `SKILL.md`，较长模板和参考资料放入 `references/`。
3. 修改后重启或刷新对应 AI 工具会话。
4. 用一个真实任务测试 skill 是否会按预期触发和输出。

## 注意事项

- 该 skill 会要求 AI 工具读取论文、代码、配置、日志和结果文件后再写文档，避免凭空编造。
- 如果论文路径存在，生成的说明文档默认以 `.md` 格式保存到论文所在文件夹。
- 如果某个论文算法没有找到明确代码实现，文档中应标注“未找到明确对应实现”。
- 如果代码中存在多个候选实现，文档应列出候选文件，并说明推荐哪个脚本用于复现实验。
- 第三方 skill 应在安装前人工检查内容，尤其是其中的脚本、命令和外部依赖。

## 参考资料

- Claude Code skills 文档：<https://docs.claude.com/en/docs/claude-code/skills>
- Claude Code Agent SDK skills 文档：<https://code.claude.com/docs/en/agent-sdk/skills>
- OpenCode Agent Skills 文档：<https://opencode.ubitools.com/skills/>
- OpenAI skills catalog：<https://github.com/openai/skills>
