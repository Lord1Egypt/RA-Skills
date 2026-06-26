# Sage DNA 互动协议

`~/.sage` 是公司共享事实层，不是某个 Agent 的私有记忆。Sage COO 必须尊重这个边界：身份、语气和 COO 思维模型留在 Skill / workspace 人格档案内；公司事实、通用规则和业务历史写入 `~/.sage`。

## 记忆源契约

- 唯一公司事实真源：`$HOME/.sage/`
- 只读工作区镜像：`sage-mirror/`

## 固定路径

- 默认路径：`$HOME/.sage`
- 初始化模板：`sage-coo/assets/sage-template/`
- 所有 Sage 系列 Skill 共用同一个 `~/.sage`
- 工作区阅读镜像：可用 `scripts/mirror_sage.sh` 复制到当前目录的 `sage-mirror/`
- 工作区人格注入：可用 `scripts/bootstrap_workspace_identity.sh` 检查或创建 OpenClaw 固定文件

## 启动检查

每次开始工作时：

1. 先查看当前 workspace 根目录是否存在 `AGENTS.md`、`CLAUDE.md`、`SOUL.md`、`IDENTITY.md`、`TOOLS.md`、`USER.md`、`HEARTBEAT.md`。
2. 运行当前 Skill 目录下的 `scripts/bootstrap_workspace_identity.sh [workspace_root]`。已有 OpenClaw 文件时只追加或刷新 Sage COO 托管区块；没有时创建最小可用文件。
3. 读取 `references/coo-identity.md`，加载 Sage COO 核心身份与基础思维模型。
4. 检查 `$HOME/.sage` 是否存在。
5. 若不存在，运行当前 Skill 目录下的 `scripts/init_sage.sh`。不要假设当前工作目录正好包含 `sage-coo/`。
6. 若存在，读取：
   - `~/.sage/INDEX.md`
   - `~/.sage/MANIFEST.yaml`
7. 根据用户问题选择具体目录，不全文扫描；经营节奏、OKR、指标、RACI、复盘类问题读取 `references/coo-operating-system.md`；只有具体场景需要时才读取 `references/coo-scenarios.md`。

## OpenClaw / 非 OpenClaw 边界

- OpenClaw / Codex / Claude Code 文件是当前 workspace Agent 的人格与行为入口；`CLAUDE.md` 与 `AGENTS.md` 应保持同源，用来适配 Claude Code。
- `~/.sage` 是跨 workspace、跨 Sage Skill 共享的公司事实真源。
- `sage-mirror/` 是只读镜像，不是写入目标。
- 如果两者冲突：人格、语气、身份以 workspace 文件为准；公司事实以 `~/.sage` 为准。
- 不要把公司事实写进 `SOUL.md` 或 `IDENTITY.md`；也不要把 COO 人格写进 `.sage`。

## 渐进式披露

遵循“入口 -> 目录 -> 具体文件”的顺序：

1. `INDEX.md`：公司摘要、导航、读取规则。
2. 领域目录：如 `team_and_roles/`、`operations_and_workflows/`。
3. 具体文件：如 `roster.csv`、某个 workflow。
4. 历史与洞察：只在需要判断演变过程时读取 `memory_and_insights/`。
5. `inbox/`：只在信息不确定、冲突、或需要寻找未整理材料时读取。

## 写入层级

用户提供的信息分三类：

- **临时信息**：先写入 `inbox/capture.md`。
- **未确认或冲突信息**：写入 `inbox/unresolved.md`。
- **已确认且未来可复用的信息**：写入对应正式文件。

不要把所有对话都写入 `.sage`。只保存能影响未来判断的信息。

本 Skill 或 `write-routing.md` 中出现的相对公司档案路径，例如 `memory_and_insights/open_loops.md`，都表示 `$HOME/.sage/memory_and_insights/open_loops.md`。不要把这些相对路径解析到当前 workspace。

## 初始化后的状态判断

如果 `INDEX.md` 仍大量包含“待填写”，视为 onboarding 未完成。此时不要机械填表，而是像新来的 COO 一样，通过 2 轮自然问答补全公司 DNA。

## 多 Agent 边界

Sage COO 可以更新通用事实：

- 公司基础
- 团队与角色
- 产品服务
- 运营工作流
- 近期决策
- 待跟进事项

Sage COO 不应该写入其他身份专属逻辑，例如 CPO 的产品方法论、CGO 的增长实验框架。其他 Sage Skill 可以扩展目录，但必须在 `MANIFEST.yaml` 或 `INDEX.md` 中保持可发现。

## 更新时的用户体验

不要频繁打断用户说“我要更新记忆”。优先完成对话目标。只有在以下情况主动说明：

- 新信息会改变公司长期档案。
- 信息存在冲突，需要用户确认。
- 你准备把临时想法晋升为正式事实。
- 涉及隐私、联系方式、财务或敏感客户信息。

## 写入后的收尾

当你实际修改了 `~/.sage` 文件后，用一句话说明：

- 更新了哪些文件。
- 为什么这些信息值得长期保存。
- 是否还有信息需要用户确认。

不要把写入日志写得比业务建议还长。

## 工作区镜像

当用户说“让我在当前工作区看 `.sage`”、“复制公司 DNA 到 workspace”、“生成阅读镜像”时：

1. 运行当前 Skill 目录下的 `scripts/mirror_sage.sh`。
2. 默认目标目录是当前工作区的 `sage-mirror/`。
3. 如果目标目录已存在，脚本会先改名备份再复制。
4. 明确告诉用户：镜像只是方便阅读，`~/.sage` 仍是唯一真源，不会自动反向同步。
