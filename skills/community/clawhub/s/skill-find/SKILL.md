---
name: skill-find
description: "Search and discover OpenClaw skills from various sources. Use when: user wants to find available skills, search for specific functionality, or discover new skills to install."
homepage: https://clawhub.ai
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": [] } } }
---

# Find Skills 技能

搜索、发现和安装开放代理技能生态中的各项专门技能。

## 何时使用此技能 (When to Use)

✅ **推荐使用场景：**

- 当用户询问“如何做 X”，而 X 可能是一个常用且已有相关技能的任务。
- 当用户表示寻求针对特定任务的技能：“找一个处理 X 的技能”或“有没有具备某能力的技能？”。
- 当用户想要扩展代理的能力、搜索工具、模板或专门的工作流时。
- 用户需要完成一个功能或者目标，但不确定是否已有技能可以直接使用。

❌ **不推荐使用场景：**

- **管理已安装技能** → 请使用 `openclaw skills list`
- **创建全新技能** → 请使用 `skill-creator` 技能或运行 `npx skills init`

## 技能定位与推荐流程

### 第 1 步：定位需求分析 (Understand What They Need)

明确用户所需处理任务的具体领域（如：React、测试、DevOps、设计、部署等），判断该任务是否为常用需求，是否有现成技能可直接处理。

### 第 2 步：检索所需技能 (Search for Skills)

使用相应的命令行搜索寻找适用技能：

```bash
# 1. 使用 ClawHub (官方推荐)
npx clawhub search "关键字"

# 2. 或者使用 Skills CLI 搜索
npx skills find [查询关键字]
```

> **💡 搜索策略与技巧：**
>
> - **使用精准关键词**：如查询 "react testing" 而非单单寻找 "testing"。
> - **更换同义词**：如 "deploy" 无结果此换用 "deployment" 或 "ci-cd"。
> - **按热度排序**：`npx clawhub search --sort installs` 或 `--sort stars`。

### 第 3 步：展示选项反馈用户 (Present Options)

找到包含相关能力的技能后，应直观地向用户展示：

- 技能名称及其具体功能用途。
- 获取或安装的相应命令行提示。
- 提供对应了解详情的网址（如 `skills.sh` 等）。

### 第 4 步：执行技能安装 (Installation)

引导或直接帮助用户安装所需的库，并在执行前叮嘱：

1. 阅读 `SKILL.md` 的说明规范。
2. 验证前置依赖。
3. 尽量在隔离环境中先行测试再做生产环境部署。

```bash
# 原生 OpenClaw 安装方式
openclaw skills install <skill-slug>

# 或者使用 npx skills 工具进行全局静默安装
npx skills add <owner/repo@skill> -g -y
```

## 如果未找到合适的技能...

如果没有检索到任何可供依赖的外部技能：

1. 告知用户当前生态中虽不包括针对性的第三方技能包。
2. 提出利用自身的原生功能，直接协助用户完成这部分操作需求。
3. **鼓励自主创建**：指导用户使用 `npx skills init [新建技能名称]` 开发定制的技能工具以供后续复用。

## 各领域常见技能检索分类

- **前端与 Web 开发**：`react`, `nextjs`, `typescript`, `tailwind`
- **测试与可靠性验证**：`testing`, `jest`, `playwright`, `healthcheck`, `e2e`
- **DevOps 持续集成与分发**：`deploy`, `docker`, `kubernetes`, `ci-cd`
- **代码规范、文档与设计**：`review`, `lint`, `readme`, `ui`, `accessibility`
- **通用代理化插件**：`github`, `feishu`, `notion`, `tavily-search`, `proactive-agent`

## 其他扩充技能资源库

除了常规 CLI 拉取外，还可以从以下资源集市主动检索第三方功能模块：

1. **[ClawHub](https://clawhub.ai)**：首选技能检索门户。
2. **OpenClaw Directory**：分类与热度浏览导视页 (https://www.openclawdirectory.dev/skills)。
3. **[LobeHub](https://lobehub.com/skills)**：丰富的社区生态驱动合集。
4. **GitHub 开源搜索**：特定仓库通过关键字 `openclaw skill`、`agent-skill` 搜索检索，尤其重点查阅 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills` 等集合下的 `SKILL.md`。
5. 当你遇到 `clawhub` 查询 **API 限流请求超时**，请等待 1 小时，或建议通过上述网页直接执行手工搜索。
