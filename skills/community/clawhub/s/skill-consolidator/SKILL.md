---
name: "skill-consolidator"
version: "2.0.0"
description: "吸星大法 / Skill Consolidator：扫描并整理本地已安装的 AI Agent skills / rules / commands（WorkBuddy、Trae、Cursor、Claude Code、Windsurf、Cline、Continue、Roo Code、GitHub Copilot、OpenAI Codex 等），检测同名冲突、功能重叠、触发词冲突与版本差异，生成整理报告与分类索引。当用户输入 /吸星大法 或 /skill-consolidator、请求整理/清理/查看 skills（如\"帮我整理 skill\"、\"skills 冲突了\"、\"organize my skills\"），或在安装新 skill 之前评估冲突时自动调用。Scans and consolidates installed AI Agent skills, detects conflicts and overlaps, generates cleanup reports and categorized indexes."
agent_created: true
allowed-tools: Bash, Read, Glob, Grep, Write, Edit
metadata:
  openclaw:
    requires:
      anyBins: [node]
    homepage: "https://github.com/alancouny/skill-consolidator"
compatibility:
  agents: ["claude-code", "cursor", "codex", "windsurf", "cline", "continue", "roo-code", "trae", "copilot", "workbuddy"]
---

# 吸星大法 · Skill Consolidator

像《天龙八部》里的吸星大法一样，把散落在各处的 skills 吸纳进来、去芜存菁、融会贯通，解决 skill 过多导致的冲突、重叠与命中率下降。

## 触发条件 Trigger Conditions

满足以下任一条件即调用本 skill：

1. 用户输入 `/吸星大法` 或 `/skill-consolidator`。
2. 用户表达整理意图，例如："帮我整理一下 skill / skills / 插件 / 能力"、"skills 太多了"、"skills 冲突了"、"skill 命中率低"、"skill 重复了"、"我有哪些 skill"、"该用哪个 skill"，或英文 "organize my skills"、"clean up my skills"、"are these skills conflicting"。
3. Agent 准备安装、下载或推荐新的 skill 之前（无论手动还是自动），先评估是否与现有 skill 冲突。
4. 用户询问 skills 是否重复或冲突。

## 工作流 Workflow

### 步骤 1：运行扫描器 Run the scanner（确定性步骤）

不要手工逐个扫描，直接运行随本 skill 附带的扫描脚本（需 Node >= 18）：

```bash
node "<skill-dir>/scripts/scan_skills.mjs" [--output <report.md>] [--json] [--no-write] [--extra <path,...>]
```

脚本会自动完成：扫描所有已知 Agent 的 skills 位置（项目级 + 用户级）→ 解析 frontmatter → 检测同名冲突 / 功能重叠 / 触发词冲突 / 版本差异 → 按类别归档 → 生成 Markdown 报告。报告同时输出到 stdout，并默认写入 `./skill-consolidation-report.md`。

- `--json`：改为输出结构化 JSON（便于进一步分析）。
- `--no-write`：只输出到 stdout，不写文件。
- `--extra <path>`：追加扫描目录（逗号分隔）。

### 步骤 2：解读与汇报 Present findings

阅读脚本输出，按以下结构向用户汇报：

1. **摘要**：共发现 N 个 skill，M 处冲突（同名 / 重叠 / 触发词）。
2. **分类索引**：按类别列出 skills。
3. **冲突详情**：逐个列出冲突与建议动作。
4. **下一步**：给出选项让用户选择。

### 步骤 3：执行整理 Execute cleanup（需用户明确确认）

在用户明确确认前，只生成报告，不得删除或修改任何现有 skill。

用户确认后允许执行：

- 禁用冲突 skill（写入对应工具的配置文件，如 Trae 的 `~/.trae-cn/skill-config.json`）。
- 合并同类 skill：在对应工具的 skills/rules 目录创建主 skill，例如 `MASTER-<category>`（`.claude/skills/MASTER-research/SKILL.md`）。
- 重写 description 以提升区分度；建立"主 skill"映射表。
- 更新本地 skill 目录汇总文件（如 `.trae/skill-registry.md`）。

执行任何写操作前，先向用户列出受影响文件路径并再次确认。

## 扫描范围 Scan Scope

扫描目标表由脚本内置（`scripts/scan_skills.mjs` 顶部的 `TARGETS`），是本 skill 扫描范围的单一事实来源：

- **P0 目录型 SKILL.md**：WorkBuddy、Trae、Cursor、Claude Code、Agents（项目级 + 用户级）。
- **P1 目录型 rules**：Windsurf、Cline、Continue、Roo Code（普通 Markdown，文件名即规则名）。
- **P2 单文件配置**：GitHub Copilot、OpenAI Codex、Aider、Augment。
- **P3 内置 / 插件缓存 skills**（只读参考，默认不修改）。

需要扩展扫描范围时，直接编辑脚本的 `TARGETS` 表，不要改本文档。

## 手工回退 Manual Fallback

当 Node 环境不可用时，按上述扫描范围手工执行：用 Glob 查找各路径的 `SKILL.md` / rules 文件，用 Read 提取 frontmatter 与关键词，按本 skill 定义的冲突类型（同名 / 功能重叠 / 触发词冲突 / 版本差异）检测，手工生成报告。

## 输出示例 Example

**用户：** `/吸星大法`

**助手：** 运行扫描器 → 汇报摘要（"发现 12 个 skill，3 处功能重叠，详见报告"）→ 展示分类索引与冲突详情 → 提出建议（合并 `research-guide` 与 `academic-search` 为 `MASTER-research` 等）→ 询问是否执行整理。
