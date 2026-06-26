

# skills-pager

**大型 AI Agent Skill 导航索引 — 只加载你需要的部分**

先回答 · 后建索引 · 永久复用



[English](README.md) · [中文](README.zh-CN.md)



---

## 问题背景

大型 AI Agent Skill——工作流 Skill、策略密集型 Skill、多文件 Skill——动辄 200、400 甚至 600+ 行。每次 Agent 只需要其中一个章节，却必须重读整个源文件。这浪费了宝贵的上下文窗口，拖慢了推理速度，也让跨会话的部分重入变得痛苦。

**如果 Agent 只需深度阅读一次大型 Skill，就能构建一个紧凑的导航索引，此后只加载需要的章节呢？**

## 解决方案

**Skills Pager** 是一个标准 Skill，它教会宿主 Agent 为任何超过约 100 行的 Skill 构建并复用一个单文件导航索引（`index.md`）。

> **首次接触** — Agent 直接读取完整源文件并回答用户问题。回答完成后，构建一个紧凑的 `index.md`，记录该 Skill 的主要路由、重要源文件和精确返回点。
>
> **后续每次使用** — Agent 先读索引文件（通常 30-50 行，而非 300-600 行），只加载当前任务需要的源文件章节，以更少的上下文消耗和更快的定位速度完成回答。

源文件始终是权威。索引是导航工具，不是记忆。Agent 自主决定映射什么、何时映射。

## 核心能力

- **节省上下文** — 不再为不需要的章节烧掉数百行上下文。索引精确告诉你当前任务该加载哪些部分。
- **快速部分访问** — 一次读取即可跳转到大型 Skill 的正确章节，无需扫描整个文件。
- **持久重入** — 未来的会话和任务交接从紧凑的工作文件开始，而非盲目重读源文件。
- **先答后建** — 索引永远不会阻塞回答。在任务完成后、理解还新鲜时构建它。
- **一个文件就够** — 每个 Skill 一个 `index.md`。
- **配套脚手架脚本** — `create-skills-pager-map.js` 消除文件系统摩擦，让 Agent 专注于编写有用的路由笔记。

## 安装

将 `skills-pager` 目录复制到工作区的 skills 文件夹：

```bash
cp -r skills-pager /path/to/workspace/skills/skills-pager
```

## 工作原理

### 首次接触

```
用户询问 research-workflow（400 行 Skill）的 Phase 3 细节
  ↓
Agent 读取 skills/research/workflow/SKILL.md → 直接回答问题
  ↓
Agent 识别到：这是一个大型 Skill，尚无索引
  ↓
Agent 运行：node skills/skills-pager/scripts/create-skills-pager-map.js \
              --skill-id research-workflow \
              --source skills/research/workflow/SKILL.md \
              --page phase-architecture \
              --page innovation-mining \
              --page adversarial-review
  ↓
Agent 将脚手架占位符替换为真实的路由笔记
  ↓
.skill-index/skills/research-workflow/index.md 已生成在磁盘上
```

### 后续使用

```
用户询问 research-workflow 的 Phase 6
  ↓
Agent 读取 .skill-index/skills/research-workflow/index.md（40 行）
  ↓
找到路由笔记："adversarial-review" → 指向 SKILL.md 第 280-350 行
  ↓
Agent 只加载该章节 → 以最小上下文成本完成回答
```

## 文件结构

```text
.skill-index/                          # 位于工作区根目录，不在 Skill 源码内
  registry.json                        # 哪些 Skill 已建立索引
  skills/
    research-workflow/
      index.md                         # 导航索引工作文件
      changes.md                       # 可选：记录索引变更原因
    quant-workflow/
      index.md
```

## `index.md` 示例

```markdown
# research-workflow

## What this skill is for
- 多阶段研究工作流，带门控转换和迭代循环

## When to start here
- 任何涉及研究阶段、创新挖掘或对抗性审查的任务

## Main routes
- `phase-architecture`
- `innovation-mining`
- `adversarial-review`

## Important sources
- `skills/research/workflow/SKILL.md`
- `skills/research/workflow/references/phase-order.md`

## Route notes

### phase-architecture
- When to start here: 理解 6 阶段门控结构
- Start source: `SKILL.md` "Phase Architecture" 章节
- What to verify: 阶段间门控条件、Phase 3 内部循环
- Next likely checks: innovation-mining 获取 Phase 3 细节

### adversarial-review
- When to start here: Phase 6 自审或质量检查
- Start source: `SKILL.md` "Adversarial Self-Review" 章节
- What to verify: 回退到 Phase 3 或 4 的条件
- Next likely checks: phase-architecture 查看完整门控流程
```

## 配套脚本

```bash
node skills/skills-pager/scripts/create-skills-pager-map.js \
  --skill-id <目标-skill-id> \
  --source <SKILL.md-路径> \
  --source <参考文件路径（如需要）> \
  --page <路由名称> \
  --page <另一个路由名称> \
  --note "可选的注册表注释"
```

脚本会创建目录结构、`registry.json` 和带占位符路由笔记的 `index.md` 脚手架。替换占位符为真实内容后，索引即可投入复用。

## 设计原则


| 原则             | 含义                                                 |
| -------------- | -------------------------------------------------- |
| **先答后建**       | 索引创建永远不阻塞用户的问题。回答完成后，趁理解还新鲜时构建索引。                  |
| **源文件是权威**     | 索引是导航工具，不替代对关键细节的源文件验证。                            |
| **一次一个 Skill** | 每个索引只覆盖一个目标 Skill。多 Skill 请求按单目标循环逐个处理。            |
| **一个文件就够**     | 一个 `index.md` 胜过七个不完整的文件。深度来自复用，不来自仪式。             |
| **100 行阈值**    | 不足 100 行的 Skill 通常不需要索引。把精力留给部分加载真正能省上下文的大型 Skill。 |


## 项目结构

```text
skills-pager/
  SKILL.md                              # 主 Skill 文件（宿主 Agent 读取）
  scripts/
    create-skills-pager-map.js          # 索引创建脚手架脚本
  references/
    initial-mapping.md                  # 首次索引创建工作流
    mapping-policy.md                   # 何时映射、映射什么
    map-layout.md                       # 索引文件结构与格式
    lookup-patterns.md                  # 日常使用模式与示例
    map-quality.md                      # 索引质量信号
    refresh-policy.md                   # 何时及如何更新过时索引
```

## 开源许可

[MIT](LICENSE)
