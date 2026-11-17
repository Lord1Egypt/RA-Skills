---
name: yotta-skills
slug: yotta-skills
version: 0.30.14
displayName: 元阁 yotta-skills
summary: YuanGe (yotta-skills) is the YottaMeta skill family orchestration router, inventory and one-command installer: route which skills to combine for a task, then install the published yotta-* skills into any agent or directory with a single npx line.
description: 'YuanGe (yotta-skills) is the orchestration and installation layer for the YottaMeta skill family - a router, an inventory and a one-command installer. Given a task summary, `--route` suggests which skills to combine, in what order and why; `install` / `update` place the published yotta-* skills into any agent or directory (idempotent, `--dry-run`, `--pin`); `hub` keeps one local source of truth and links it into every verified host; `--inventory` / `--reindex` scan what is installed; `doctor` / `rollback` keep it healthy. Zero dependencies, Node.js 18+. This package contains no skill bodies - only a manifest, a downloader, a placer and a summary. 中文：元阁 / 技能编排 / 路由建议 / 一键安装 / 技能盘点 / 技能 Hub / 装前门禁。'
tags: [skill orchestration, skill router, one-command install, skill inventory, skill hub, agent skills, orchestration, install, 技能编排, 一键安装, 技能盘点]
category: ai-agent
license: MIT
homepage: https://github.com/YottaMeta/yotta-skills
metadata:
  zh_name: 元阁
---
## 使用须知（先做这一步）

本技能为**按需触发**技能，本身不常驻。「元阁总编排策划」这套组合决策如果想在**每个会话都可用**，
可以由用户把它写进客户端的全局记忆文件（Codex 的 `AGENTS.md`、Claude Code 的 `CLAUDE.md`、
其它智能体的全局/永久记忆），使下个会话自动注入。

**这是可选步骤，且必须先获得用户明确同意。AI 不得静默写入，也不得把写入当作使用本技能的前提。**

写入前按四步执行：

1. **展示**：把**目标文件路径**（如 Codex 的 `$CODEX_HOME/AGENTS.md`）、
   准备写入的**完整文本**、以及写入后的效果（下个会话会自动注入这段说明）一并展示给用户；
2. **确认**：只有用户明确同意后才写入；**未获同意前不写任何文件**；
3. **回读校验**：写入后回读确认；目标文件中已有同段内容 → 跳过，不重复堆叠；
4. **拒绝不影响功能**：用户拒绝或文件不可写时，只说明「未写入全局记忆」，照常使用 CLI
   （`--route` / `install` / `--inventory`），功能不受影响。

**可选写入文本（逐字，需用户确认后写入）**：

> **元阁编排**：单技能是零件，组合才是系统。接到需求先查「元阁编排策划」命中哪个组合
> （输出呈现标准 / 长生命周期 / 交付质量门 / 装前安全门 / 造技能发版 / 安全事件响应 / 入口安装），
> 由 AI 给出**建议**，**经用户确认后**再安装对应技能并调用。本技能不自动安装、不自动调用其他技能，
> 安装与调用决定权始终在用户。需要时可运行 `yotta-skills --reindex` 重扫本机技能注册表（本地扫描），
> `yotta-skills update --check` 做只读版本检查，或后台周检 `yotta-skills update --check --scheduled`
> （未到期不联网，到期单次检查并写缓存）。完整决策表见技能 `yotta-skills/references/orchestration.md`。

**写入位置**：客户端全局记忆文件（Codex = `$CODEX_HOME/AGENTS.md`，未设置时回退 `~/.codex/AGENTS.md` 的「通用方法论」节）。
**写入时机**：仅当用户明确要求「让元阁编排在每个会话自动可用」时，按上面四步执行；否则只提供文本供用户自行粘贴。

---

# 元阁（yotta-skills）

**元阁全家的总编排策划 + 编排路由 + 一键安装 + 技能盘点**，一句话四层：

- **路由层（该用哪几个）**：`--route "<需求摘要>"` / MCP `route_request` 查本地注册表与静态编排 playbook，输出候选组合、调用顺序、每个技能角色、置信度、依据、已装/缺失状态与安装命令；非元阁家族已装技能按 frontmatter description 机械匹配作并列候选（标注来源与未扫描状态，只读不自动调用）；只建议安装，不自动安装。
- **O1 动态路由层（v0.23.0，capability `o1.route`）**：可选调用用户显式配置的本地扩展提供方（provider），在已装注册表白名单内对路由结果增补 / 重排，并返回 `confidence` / `reasons` / `summary` / `alternatives`；静态 playbook 结果先算必算、永不缺席，未配置或调用失败时文本输出与历史一致，`--json` 仅多一个 `dynamic` 状态块。协议与配置见 `references/provider-protocol.md`。
- **M1 记忆裁决层（哪些值得长期记住）**：`decide-memory` / MCP `decide_memory` 调用可选本地 provider（capability `m1.adjudicate`），输出 `promote / hold / demote` 只读建议、分数与信号明细；默认不写元忆、不删除技能。`usage` 默认关闭，用户显式开启后才记录结构化使用信号。协议与边界见 `references/provider-protocol.md`。
- **策划层（怎么用）**：接到需求，先按「编排策划」定位命中哪个组合——哪些元技能搭配起来最强、适合什么场景、AI 该给出什么安装与调用建议（**安装与调用均由用户确认后执行**）。
- **安装层（怎么装）**：一条 `npx -y @yottameta/yotta-skills` 把组合/全家装进指定智能体或目录——`--list` 看清单、`install` 装、`update` 增量更新、`doctor` 只读自检、`rollback` 恢复快照、`--dry-run` 预览、`--pin` 锁版本。

> **权限边界**：`install` / `update` 会写入目标技能目录，属于有副作用操作——执行前先用 `--dry-run`
> 展示将写入的目录与技能清单，由用户确认后再执行；批量安装（多技能 / 多目录 / 装全家）不是一次性授权，
> 新增目标目录要重新确认。不静默写宿主配置、不自动安装缺失技能、不 `-g` 污染全局；
> 安装器拒绝对符号链接目标写入，批量安装需显式 `--yes`。

- **盘点层（已装了什么）**：`--inventory` / `--reindex` 扫描本机各智能体技能目录，生成/更新本地注册表；装技能后自动 re-index，新装技能自动被发现——自包含扫描，不依赖任何元技能。

每个技能仍走各自独立的 npm 包（版本源唯一）；本包只做「清单 + 下载 + 落位 + 汇总」，**不内置任何技能本体**。
> **本包不含技能本体**：拿到它只代表有了「编排策划 + 安装工具」；真正装齐需运行 `install`。

---

## 编排策划（先看这个）

**单技能是零件，组合才是系统。** 元阁的价值不只是「装齐全家」，更是告诉你**什么时候该用哪几个、为什么、怎么组合使用**。完整决策表见 `references/orchestration.md`。

### 组合矩阵（哪些和哪些，强在哪）

| 组合 | 成员（slug） | 一起用强在哪 | 单用缺什么 |
|---|---|---|---|
| **① 输出呈现标准** | yotta-present + yotta-humanize | 先判型渲染成规范可复制输出，再祛 AI 味，交付统一且读感自然 | 只规范化不祛 AI 味；只祛 AI 味不规整 |
| **② 长生命周期智能体** | yotta-workflow + yotta-memory + yotta-learn + yotta-logs | 开工恢复、权限记忆、沉淀学习、检索历史，越用越懂你 | 状态无处放；记忆无边界；错不沉淀；历史查不到 |
| **③ 交付质量门** | yotta-anti-shallow + yotta-code-quality + yotta-publish-guard | 防敷衍、结对评审、发布守门，交付前多层把关 | 容易停留表面；代码无人审；发版无守门 |
| **④ 装前安全门** | yotta-verify（或元信MCP）+ yotta-vetter + yotta-security-audit | 确定性扫描 + 协议审查 + 深检，装其他来源技能前可信判定 | 无确定性扫描；无协议审查；无深检 |
| **⑤ 造技能 / 发版** | yotta-skill-creator + yotta-publish-guard | 脚手架生成合规技能 + 发布守门 | 造技能无模板；造完不知能否发 |
| **⑥ 安全事件响应** | yotta-logwatch + yotta-intel + yotta-triage + yotta-secret + yotta-chain + yotta-recon | 日志攻击链 + IOC + 样本初筛 + 密钥 + 供应链 + 侦察，看全链路 | 每项只管一环，单用看不到全貌 |
| **⑦ 入口 + 安装** | yotta-prompt + yotta-skills | 元引澄清需求串联，元阁按场景把组合装好 | 需求模糊不知用哪个；要一个个装 |

### 场景 → 组合映射（接到需求查表）

| 用户场景 | 该组合 | 建议动作（经用户确认后执行） |
|---|---|---|
| 「让 AI 长期帮我做项目 / 别忘了我 / 跨会话」 | ② 长生命周期 | 装 yotta-workflow yotta-memory yotta-learn yotta-logs；开工恢复上下文、状态就近存、会话结束留记录 |
| 「帮我写/润色，输出规范、别 AI 味」 | ① 输出呈现标准 | 装 yotta-present yotta-humanize；默认先判型渲染，检测 AI 味再改写 |
| 「检查代码/报告质量，别糊弄」 | ③ 交付质量门 | 装 yotta-anti-shallow yotta-code-quality yotta-publish-guard；按对应协议执行 |
| 「我要装其他来源技能/插件/MCP」 | ④ 装前安全门 | 装 yotta-verify(+MCP) yotta-vetter yotta-security-audit；装前必扫 |
| 「我要造新 skill 并发布」 | ⑤ 造技能/发版 | 装 yotta-skill-creator yotta-publish-guard；生成 + 守门 |
| 「我怀疑日志/资产有问题」 | ⑥ 安全事件响应 | 装 yotta-logwatch yotta-intel yotta-triage yotta-secret yotta-chain yotta-recon；按需调用 |
| 「不知道怎么说 / 一堆技能该用哪个」 | ⑦ 入口+安装 | 装 yotta-prompt yotta-skills；元引澄清→串联→按组合装 |

### AI 建议安装与组合规则

1. **查表**：接到需求，先在「场景 → 组合映射」定位命中组合。
2. **查已装**：检查当前智能体技能目录是否存在对应 `<slug>/SKILL.md`；存在即已装，缺失即待装。
3. **建议装**：只列组合所需技能（不装全家）与安装命令
   `npx -y @yottameta/yotta-skills install <slug>... [--agent <name> | --dir <path>]`（默认 `--pin` 锁死清单精确版本），
   **先给出清单与命令，等用户确认后再执行**；用户未确认 → 不安装。
4. **建议用**：说明命中组合的推荐动作（如输出按元呈判型渲染、开工恢复上下文 + 读状态文件），
   **由用户确认后生效**。跨会话的默认行为需要写进客户端全局记忆，写入本身同样需要用户明确同意（见「使用须知」）；
   **不得**把「无需提醒」「默认全走」当作常驻授权。
5. **用户触发（高风险）**：命中「④ ⑥ ⑤」等高风险或目的不明时，AI 给出技能清单 + 执行方案，**先征询用户确认**再执行；拿不准就当未装，只给安装命令。
6. **判断标准**：技能目录有对应 `SKILL.md` 即视为已装；拿不准 → 视为未装并给提示。

---

## 快速使用（安装层）

**首选流程（Hub 主路径，安装本体与智能体无关）**：

```bash
# 1) 看本机有哪些宿主与技能目录（状态细分：可用 / 残留 / 未创建 / 仅标记）
npx -y @yottameta/yotta-skills hub hosts

# 2) 装进 Hub 真源（默认 ~/.yottaskills/hub；无需指定智能体）
npx -y @yottameta/yotta-skills hub install

# 3) 分发到全部已核实宿主（Windows junction / macOS·Linux symlink）
npx -y @yottameta/yotta-skills hub link --all

# 4) 图形化面板管理（宿主矩阵 / 链接与体检 / 收编 / 迁移向导 / 回滚）
npx -y @yottameta/yotta-skills view
```

**换 Hub 存储位置（持久化；`--move` 迁移已有技能并重链）**：

```bash
# 持久化配置（写入 ~/.yottaskills/config.json；优先级 --hub > YOTTA_SKILLS_HUB > config > 默认）
npx -y @yottameta/yotta-skills hub config set --hub "D:\my-hub" --move
npx -y @yottameta/yotta-skills hub config get   # 查看生效位置与来源
npx -y @yottameta/yotta-skills hub config rollback        # 回滚预览（位置回退，用当前内容）
npx -y @yottameta/yotta-skills hub config rollback --yes  # 执行回滚（反向迁移同内核）
npx -y @yottameta/yotta-skills hub config clear # 清除覆盖（有技能时默认阻断，确认影响后加 --yes）
npx -y @yottameta/yotta-skills hub cleanup-backups --yes  # 清理历史备份 / 暂存残留（回收站 7 天）
```

**元阁独立安装（把管理引擎装成独立 CLI，不依赖任何智能体）**：

```bash
# 默认装到 ~/.yottaskills/yotta-skills；--dir 指定位置
npx -y @yottameta/yotta-skills install-self
npx -y @yottameta/yotta-skills install-self --dir ~/tools/yotta-skills

# 查看元阁位置（运行中 CLI / 独立安装目录 / Hub 真源）
npx -y @yottameta/yotta-skills where
```

**指定智能体直装（兼容路径）**：

```bash
# 列出全家技能 + 版本 + 说明
npx -y @yottameta/yotta-skills --list

# 装全家到指定智能体默认用户级目录
npx -y @yottameta/yotta-skills install --agent codex

# 装全家到任意目录（每个技能落在 <dir>/<slug>）
npx -y @yottameta/yotta-skills install --dir ~/my-skills

# 只装单个 / 多个技能（按编排策划选组合时常用）
npx -y @yottameta/yotta-skills install yotta-memory yotta-verify --dir ~/my-skills

# 增量更新已装技能（补齐缺失 + 升级；只升不降：本地更高保留不降级，--force 才显式降级）
npx -y @yottameta/yotta-skills update --agent codex

# 只读检查有没有更新（联网对 npm 最新，不改动；0=全部最新 / 3=有更新 / 1=查失败）
npx -y @yottameta/yotta-skills update --check --agent codex

# 后台周检入口（未到期不联网；到期只检查一次并写 ~/.yottaskills/update-check.json）
npx -y @yottameta/yotta-skills update --check --scheduled --agent codex

# 检查到家族更新后自动更新（仅 yotta-* 自家家族，含装前安全扫描）
npx -y @yottameta/yotta-skills update --auto --agent codex

# 只读检查已装技能（不修改目录；可加 --json 输出机器可读结果）
npx -y @yottameta/yotta-skills doctor --agent codex

# 查看可用快照 / 回滚最近一次安装或更新
npx -y @yottameta/yotta-skills rollback --list --agent codex
npx -y @yottameta/yotta-skills rollback --slug yotta-memory --agent codex

# 预览将安装清单（不联网、不改动）
npx -y @yottameta/yotta-skills --dry-run

# 盘点本机已装技能（自包含扫描，不依赖任何元技能）
npx -y @yottameta/yotta-skills --inventory

# 重扫注册表（会话开工 / 新装技能后，增量合并变化）
npx -y @yottameta/yotta-skills --reindex

# OpenClaw：走宿主官方技能命令，保留安全审计与更新追踪
openclaw skills install @yottameta/yotta-skills
openclaw skills update @yottameta/yotta-skills
```

> **OpenClaw 用户**：技能安装与更新走宿主官方命令 `openclaw skills install|update @yottameta/<slug>`，
> 以保留宿主的 ClawHub 安全审计卡与更新追踪；元阁的 `--inventory` / `--reindex` 已能识别 `~/.openclaw/skills`（含 `OPENCLAW_STATE_DIR` 覆盖）。

## 技能 Hub（单点安装 + 链接分发）

Hub 把「每个宿主装一份」改成「本机一份真源，按宿主链接分发」。默认真源
`~/.yottaskills/hub`，可用 `--hub <dir>` 或 `YOTTA_SKILLS_HUB` 覆盖。

元技能（清单 27 + 特殊家族 5：元开 / 元伴 / 元呈 / 元阁本体 / 元信MCP）
在 `hub link` 执行时收敛唯一性：宿主里的同名真目录 / `yotta-X__*`
重命名副本会先移入回收站（`~/.yottaskills/trash/<时间戳>/`，保留 7 天、
输出恢复路径；跨卷场景自动回退「复制 → 校验 → 删除源」），再建立指向
Hub 的链接；宿主版本高于 Hub 时跳过并提示先
`hub update`；目标条目为指向 Hub 之外的链接时默认跳过，显式 `--force`
可替换（仅移除链接本身）；外部技能同名冲突仍默认跳过、不自动删、不自动更新。

```bash
# 1) 只读发现本机已装智能体与技能目录（文件系统 + 环境变量；不读元忆 / 注册表）
npx -y @yottameta/yotta-skills hub hosts

# 2) 把元技能装进 Hub 真源（复用安装管线 + 元信装前扫描）
npx -y @yottameta/yotta-skills hub install

# 3) 接管各宿主现有技能：先只读预演，再复制收编（原目录保留）
npx -y @yottameta/yotta-skills hub adopt --scan
npx -y @yottameta/yotta-skills hub adopt --apply

# 4) 链接分发到全部已核实宿主（默认范围；Windows junction / macOS·Linux symlink）
npx -y @yottameta/yotta-skills hub link --all

# 4b) 显式把自动发现目录一并纳入（默认不链；锁 / 数据桥接目录永不链接）
npx -y @yottameta/yotta-skills hub link --all --include-discovered

# 5) 查看来源、版本、链接宿主与异常
npx -y @yottameta/yotta-skills hub status
npx -y @yottameta/yotta-skills hub doctor

# 5b) 自定义宿主注册（只注册，不创建目录、不改宿主配置；移除注册不删目录；改名一步到位、只改显示名）
npx -y @yottameta/yotta-skills hub hosts add ~/my-agent/skills --label "我的宿主"
npx -y @yottameta/yotta-skills hub hosts rename ~/my-agent/skills --label "新名字"
npx -y @yottameta/yotta-skills hub hosts list
npx -y @yottameta/yotta-skills hub hosts remove ~/my-agent/skills

# 5c) 手动标记状态 / 清理残留（清理默认预览；只删指向 Hub 的链接，目录入回收站 7 天）
npx -y @yottameta/yotta-skills hub hosts mark ~/my-agent/skills --state orphan
npx -y @yottameta/yotta-skills hub hosts mark ~/my-agent/skills --state ignored  # 隐藏标记（只影响显示）
npx -y @yottameta/yotta-skills hub hosts remove ~/my-agent/skills --purge
npx -y @yottameta/yotta-skills hub hosts remove ~/my-agent/skills --purge --yes

# 5d) 不接管 / 目录覆盖（发现 / 显示 / 链接三层跳过；恢复用 include；set 覆盖内置映射）
npx -y @yottameta/yotta-skills hub hosts exclude box
npx -y @yottameta/yotta-skills hub hosts include box
npx -y @yottameta/yotta-skills hub hosts set box --dir "D:\box-agent\skills"
npx -y @yottameta/yotta-skills hub hosts set box --clear

# 6) 本地面板：预览、确认、执行、留证（仅 127.0.0.1:8789）
npx -y @yottameta/yotta-skills view

# 只删链接，不动 Hub 真源（真目录 / 外部链接一律拒绝）
npx -y @yottameta/yotta-skills hub unlink --all

# 指定智能体分发 / 解除（只影响该宿主；Hub 真源保留）
npx -y @yottameta/yotta-skills hub link yotta-memory --agent codex
npx -y @yottameta/yotta-skills hub unlink yotta-memory --agent codex

# 彻底删除 Hub 技能：全宿主清链接（含死链）+ 目录入回收站 + 清台账 + 审计
npx -y @yottameta/yotta-skills hub remove my-skill --dry-run
```

链接范围（0.28.0 起）：`hub hosts` 把目录分为已核实 / 自动发现 / 桥接三类 ——
**默认范围只含已核实宿主**（映射经公开宿主表 / 官方文档 / 本机自证核实）；自动发现
目录需 `--include-discovered` 显式纳入；`XDG_STATE_HOME/skills`（skills CLI
锁目录）与 `XDG_DATA_HOME/skills` 是锁 / 数据桥接，永不作为链接目标。
`hub doctor` 的 `link_scope` 检查只读报告范围外链接。逐智能体核实表见
发布方内部核实记录；本机可随时用 `hub hosts` 复算分类与范围。

状态细分（0.29.0 起）：每条宿主目录带生命周期状态 —— **可用**（实体已确认：应用标记 /
用户注册 / 手动标记）、**残留**（实体未确认；可手动确认后清理）、**未创建**、
**仅标记**（已装实体、技能目录未创建）、**隐藏标记**（`ignored`，只影响列表显示、
不拦截行为；行为拦截用「不接管」）；`hub doctor` 的 `host_state` 检查只读提示，
不判 fail。残留清理 = `hub hosts remove <目录> --purge`（默认预览，`--yes` 执行；
只删指向 Hub 的链接，非 Hub 链接 / 非技能内容随目录保留在回收站 7 天）。
移除注册 / 不接管后若目录仍有 Hub 链接，会提示剩余条数与 `hub unlink --dir` 清理指引。

不接管与目录覆盖（0.29.1 起）：`hub hosts exclude <agentId|目录>` 把目标从发现、
显示、链接三层全部跳过（`--include-discovered` 也不纳入；已建链接不受影响，可
`hub unlink` 清理），`hub hosts include` 恢复接管；`hub hosts set <agentId> --dir <目录>`
用户级覆盖内置映射（被覆盖旧目录不再进入默认发现 / 链接），`--clear` 恢复默认。
面板「宿主矩阵」提供等价动作（不接管 / 恢复接管 / 编辑目录 / 标记可用 / 隐藏标记 / 重命名（自定义注册）），
写操作均写 Hub 审计。**YottaCode 不纳入接管**（自带三层技能管理；`.yottacode` 与
`YOTTACODE_HOME` 在映射 / 扫描 / 注册 / 标记 / 链接全部排除）。未核实映射显示
「映射·未核实」，「自动发现」只用于文件系统扫描结果。

宿主发现兼容 `agentskills.io` 技能格式与 Vercel Labs `skills` CLI 的
`.agents/skills` 通用目录；已收录 81 条宿主映射，并只读兼容
`.skill-lock.json` v3（`$XDG_STATE_HOME/skills/` 或 `~/.agents/`）。
不读元忆，不重写官方锁文件，不静默降级为复制。

删除技能（0.28.3 起）：`hub remove <slug>` 一条命令完成「全宿主清链接（含死链）→
Hub 目录入回收站（保留 7 天）→ 清 Hub / 链接台账 → 写审计」，fail-closed：只删指向
Hub 的链接与 Hub 内目录，真副本 / 外部链接一律保留并报告；链接清理报错即中止、不删
Hub。默认范围为已核实宿主 ∪ 本技能链接台账；`--agent` / `--dir` 收窄仅用于 Hub 目标
已缺失的死链清理（防止只清一个宿主导致其他宿主变死链）。指定智能体分发 / 解除用
`hub link|unlink <slug> --agent <id>`。

## 命令与选项

| 命令 / 选项 | 作用 |
|---|---|
| `--list`（`-l`） | 列出全家技能 + 版本 + 说明；可加技能名过滤 |
| `install --agent <name>` | 装全家到指定智能体默认用户级目录（推荐） |
| `install --dir <path>` | 装全家到指定目录，每个技能落在 `<path>/<slug>` |
| `install <skill>... [--agent <name> \| --dir <path>]` | 只装指定的一个或多个技能 |
| `update [--agent <name> \| --dir <path>]` | 增量更新：补齐缺失技能、升级版本不一致的技能 |
| `update --installed-only [--agent <name> \| --dir <path>]` | 只维护目标目录**已安装**的家族技能（不补装缺失；无匹配时退出码 0）——接管现有元技能的标准配方 |
| `update --check [--agent <name> \| --dir <path>]` | 只读检查更新：联网对 npm 最新，不改动；退出码 0=全部最新 / 3=有更新 / 1=查失败 |
| `update --check --scheduled [--agent <name> \| --dir <path>]` | 后台周检入口：未到期不联网；到期只检查一次并写本地缓存；文本失败静默，`--json` 保留诊断；始终退出 0 |
| `update --auto [--agent <name> \| --dir <path>]` | 检查到家族更新后自动更新（仅 yotta-* 自家家族，含装前安全扫描） |
| `doctor [--agent <name> \| --dir <path>] [--slug <slug>]` | 只读自检：SKILL / 版本 / manifest / 注册表 / 自定义 doctor；`--dir` 可指向技能集合目录或单个技能包目录；退出码 0=通过 / 4=没有可检查对象 / 1=检查失败 / 6=manifest 身份失败 |
| `rollback [--agent <name> \| --dir <path>] [--slug <slug>]` | 校验并恢复最近一次快照；`--list` 只列快照；`--json` 输出机器可读结果 |
| `hook capabilities --host <name>` | 查看宿主六个统一事件的能力等级；未知宿主默认 `unsupported` |
| `hook evaluate --host <name> --event <event> --manifest <file> --context <json>` | 评估 manifest hook 声明，输出 allow / block / warn / unverified，并写结构化证据 |
| `hook bind --host <name> --manifest <file>` | 幂等注册 hook 声明；`hook unbind <id>` 反注册 |
| `--inventory` | 盘点本机已装技能：扫描技能目录生成/更新注册表（自包含，不依赖元技能）；`--json` 输出 JSON、`--project` 附扫项目级目录 |
| `--reindex` | 重扫注册表：扫描技能目录并增量合并变化（install / update 完成后 CLI 自动重扫；也可在会话开工等时机手动运行）；`--json` 输出 JSON、`--project` 附扫项目级目录；`--rescan` 同义 |
| `hub hosts` | 发现本机已装智能体与技能目录（文件系统 + 环境变量；不读元忆 / 注册表）；按已核实 / 自动发现 / 桥接分类；`--json` 输出 JSON |
| `hub config get \| set --hub <path> [--move [--clean-residue]] \| rollback [--yes] \| clear` | Hub 位置持久化（`config.json`；优先级 `--hub` > `YOTTA_SKILLS_HUB` > config > 默认）；`--move` = 复制校验 → 重链 → 旧 Hub 入回收站（7 天），fail-closed；`lastMigration` 记录最近迁移，`rollback` = 位置回退（用当前内容，非快照恢复）；仅切换指针且旧 Hub 非空时记录「未迁移」供面板一键迁移；`where` / 面板「Hub 位置 + 最近一次迁移」显示来源与回滚入口 |
| `hub cleanup-backups [--yes] [--include-discovered]` | 清理宿主 / Hub 里的 `.yottaskills-backup-*` / `.yottaskills-staging` 等历史残留（默认预览；`--yes` 移入回收站保留 7 天）；`hub doctor` 只读报告 `backup_residue` 警告 |
| `hub install [skill...]` | 把元技能安装到 Hub 真源（清单 27 + 特殊家族 5；特殊家族跟随各自 npm latest；默认 `~/.yottaskills/hub`；`--hub` / `YOTTA_SKILLS_HUB` 覆盖） |
| `hub update` | 更新 Hub 内的元技能；非元技能不参与（来源无统一安装源，用户自行处理） |
| `hub adopt --scan` | 只读预演：扫描各宿主现有技能，输出收编候选、多副本冲突、已在 Hub 状态 |
| `hub adopt --apply [--include <a,b>] [--force] [--in-place]` | 把选中技能收编进 Hub；输出明示范围与目标 Hub；默认复制保真 + 原目录保留；非元阁来源标注「无更新源」并对严格 YAML 风险只读告警；`--skip-scan` 显式提示跳过装前扫描 |
| `hub refresh <slug> --from <path>` | 手动同步非元阁技能（重新收编 + 更新哈希 + 台账） |
| `hub link --agent <id> \| --dir <dir> \| --all [--include-discovered]` | 把 Hub 技能链接到指定宿主 / 目录 / 全部已核实宿主（默认范围）；`--include-discovered` 显式纳入自动发现目录；元技能链接时收敛旧副本（回收站 7 天）；`--dry-run` 只预览（含将收敛明细）；`--force` 可替换指向 Hub 之外的链接（仅移除链接本身） |
| `hub unlink --agent <id> \| --dir <dir> \| --all [--include-discovered]` | 只删除链接；lstat + readlink 校验目标在当前 Hub 内，fail-closed；`--dir` 不带 slug 时以文件系统为真源清理该目录全部 Hub 链接（台账缺失也能清理），指向其它位置的链接不动并给出错位警告；dry-run / 执行均输出汇总 |
| `hub remove <slug> [--dry-run] [--include-discovered]` | 删除 Hub 技能：全宿主清链接（含死链）+ Hub 目录入回收站（7 天）+ 清 Hub / 链接台账 + 写审计；fail-closed（真副本 / 外部链接保留并报告；链接报错即中止不删 Hub）；`--agent` / `--dir` 收窄仅用于死链清理 |
| `hub status [--json]` | 查看 Hub 技能来源、版本、链接宿主、异常链接与宿主发现摘要 |
| `hub doctor [--json]` | 检查断链 / Hub 目标缺失 / slug 不一致 / 单一真源（只读报告多份副本与版本参差）/ 链接范围（`link_scope` 只读报告范围外链接）/ 目录权限；异常时退出码 1 |
| `view [--port <n>]` | 启动本机技能枢纽面板（默认 `127.0.0.1:8789`，仅本机监听）：六视图（概览 / 宿主矩阵 / 收编向导 / 链接与体检 / 记录与回滚 / 路由与编排）+ **全量 CLI 页**（全部命令 / 子命令 + 人话说明 + 可复制示例 + 完整选项，与 `--help` 单一真源）；可执行收编 / 链接 / 解除 / 回滚 / 删除技能（影响预览 + 手输 slug 二次确认），写操作需页面会话令牌，install / update / refresh 只给命令 |
| `--route <需求摘要>` | 编排路由：输出组合、调用顺序、技能角色、置信度、依据、已装/缺失状态与安装建议；可选本地 provider 增补 / 重排并返回 `confidence` / `reasons` / `summary` / `alternatives`；`--json` 输出 JSON、`--project` 附扫项目级目录 |
| `usage status` | 查看本地使用记录开关与计数；默认关闭，不创建文件 |
| `usage enable` / `usage disable` | 开启 / 关闭 `--route` 的结构化使用记录；不记录需求原文 |
| `usage mark --skill <slug> --signal used\|named\|accepted` | 记录一次显式使用信号；不要求先 enable |
| `usage reset --yes` | 清空本地使用记录 |
| `decide-memory [--dry-run\|--promote] [--explain] [--json]` | M1 记忆裁决只读建议；`--promote` 只写本地建议文件，不写元忆、不删除内容 |
| `--no-reindex` | 安装 / 更新后不自动重扫注册表 |
| `--dry-run` | 预览将执行的安装 / 更新清单；不联网、不改动 |
| `--pin` | 锁死清单精确版本（默认 range：跟随同 major 最新 patch） |
| `--force` | 已是最新也重新安装 |
| `--skip-scan` | 人工应急路径：跳过元信门禁并标记 `explicit-unverified`；不得用于 `update --auto` |
| `--only <a,b>` | install / update 只处理指定技能（与位置参数技能列表合并去重） |
| `--domain <name>` | install / update 只处理指定家族（security / quality / memory / writing / workflow / entry / compliance / education / distribution） |
| `--installed-only` | update 只维护目标目录已安装的技能（不补装缺失；无匹配时退出码 0） |
| `--npm <path>` | 指定 npm 可执行文件 |
| `--python <path>` | 指定 python 可执行文件（元信 scan 用） |
| `--verify <path>` | 指定 yotta_verify.py 路径 |
| `--slug <slug>` | doctor / rollback 时只处理指定技能 |
| `-h, --help` / `-v, --version` | 帮助 / 版本 |

不带命令直接给技能名时，等价于 `install <skill>`。

### 范围控制（接多少管多少）

| 用法 | 范围 |
|---|---|
| `install` / `update`（无旗标） | 全量清单：install 安装全部；update 补齐缺失 + 升级已装（现状语义不变） |
| `update --installed-only` | 只维护目标目录已安装的家族技能（不补装缺失；`skills.json` 只作身份 / 版本参照） |
| `--only <a,b>` / `--domain <name>` | 只处理指定技能 / 家族（可与 `--installed-only` 取交集） |
| `update --check` / `--auto` | 只检查 / 维护已装技能，不补装缺失 |

已管理且已最新 → 跳过（退出码 0）；清单内但机器未装 → 不动作、不新增、不报错；
非家族 / 未收录目录 → 忽略不报错。标准接管配方：

```bash
npx -y @yottameta/yotta-skills update --installed-only --dir <技能目录>
```

## 运行时 hook 适配层

技能 manifest 只声明六个统一事件的要求，元阁负责能力探测、确定性评估、证据留痕和降级标注：

```bash
npx -y @yottameta/yotta-skills hook capabilities --host codex
npx -y @yottameta/yotta-skills hook evaluate --host codex --event before_send --manifest ./skill-manifest.json --context '{"checks":{}}'
npx -y @yottameta/yotta-skills hook bind --host codex --manifest ./skill-manifest.json
npx -y @yottameta/yotta-skills hook unbind <binding-id>
```

证据写入 `~/.yottaskills/hook-log.jsonl`，绑定注册表写入
`~/.yottaskills/hook-bindings.json`。`native-audit` 只表示可审计和一次纠偏，不表示动作前强制；
`unsupported` 必须显示 `explicit-unverified`。本层只做本地确定性判断，不联网、不执行下载。

## 技能盘点（--inventory）

元阁自带技能扫描核心（零依赖，不依赖任何元技能）：扫描各智能体技能目录，解析
`SKILL.md` frontmatter，生成/更新本地注册表 `~/.yottaskills/registry.json`，数据不出本机。
多 agent 宿主可用 `YOTTA_SKILLS_REGISTRY_FILE` 为每个 agent 指定独立注册表文件。
适合「装了哪些技能、各干嘛、从哪来」的快速盘点。

```bash
# 盘点本机已装技能（文本表格）
npx -y @yottameta/yotta-skills --inventory

# 机器可读（JSON）
npx -y @yottameta/yotta-skills --inventory --json

# 追加扫描任意目录 / 当前项目级目录
npx -y @yottameta/yotta-skills --inventory --dir ~/my-skills --project
```

注册表增量合并：新增（added）/ 更新（updated）/ 消失（gone）随输出列出；同名技能来自多个目录时合并来源，版本不一致记录冲突。

### re-index：新装技能自动被发现

- **装技能后自动**：`install` / `update` 完成后自动重扫注册表，把本次落位结果反映进
  `~/.yottaskills/registry.json`（新增 / 更新 / 消失随输出列出）；`--no-reindex` 可关闭。
- **会话开工**：建议每会话开工先跑一次 `yotta-skills --reindex`（快速增量，只合并变化），
  让新装 / 更新的技能自动进入注册表。
- **手动**：`yotta-skills --reindex`（`--rescan` 同义）；`--json` 机器可读、`--project` 附扫项目级目录。

### update 增量更新与检查（--check / --auto）

增量更新遍历清单，补齐缺失、升级版本不一致，默认跳过已最新。`--check` 只读联网
（对 npm `dist-tags.latest`），按本地 `SKILL.md` 版本对比——无论技能源自哪个安装渠道
（npm / git clone / 本地拷贝等）都兼容；`--auto` 检测到家族（`yotta-*` / 清单内）可更新时，走安装管线
（含元信装前安全扫描）自动更新。**非元阁家族（非 yotta-*）技能绝不自动更新**（默认保守：`--check` 列清单，
用户确认后再 `update`）。

`--check --scheduled` 是后台周检入口：默认 7 天加 0 到 24 小时随机抖动，未到期不联网；
到期只检查一次并把结果写入 `~/.yottaskills/update-check.json`。文本模式网络失败静默，
`--json` 可读取 `error` / `cache` 诊断字段。它不作为会话开工默认动作。

```bash
# 只读检查（0=全部最新 / 3=有更新 / 1=查失败）
npx -y @yottameta/yotta-skills update --check --agent codex

# 后台周检入口（未到期不联网；到期单次检查并写缓存）
npx -y @yottameta/yotta-skills update --check --scheduled --agent codex

# 检查到家族更新后自动更新（仅自家家族）
npx -y @yottameta/yotta-skills update --auto --agent codex
```

## doctor 与 rollback

`doctor` 是只读自检，不会修改技能目录或注册表。它检查目标技能目录、`SKILL.md`、
frontmatter 版本、manifest 身份、本地注册表记录，以及包内声明的自定义 doctor 脚本。
`--dir` 既可指向包含多个 `yotta-*` 子目录的技能集合目录，也可直接指向单个技能包目录；
后者会按 `SKILL.md` / `skill-manifest.json` 自动识别技能身份。`--json` 返回稳定字段，
适合脚本和智能体消费。退出码：`0` 通过，`4` 没有可检查对象，`1` 检查失败，`6` manifest 身份失败。

```bash
npx -y @yottameta/yotta-skills doctor --agent codex --slug yotta-memory
npx -y @yottameta/yotta-skills doctor --dir ~/my-skills --json
```

`rollback` 只恢复已经存在的本机快照。恢复前会校验快照（新快照校验 SHA-256 元数据，
旧快照按结构校验）；恢复过程中先在同盘暂存，再替换目标，失败时保留当前目录。
快照默认保留，不会被回滚操作删除。

```bash
# 查看当前有哪些快照（--slug 可只看一个技能）
npx -y @yottameta/yotta-skills rollback --list --agent codex

# 回滚最近一次安装或更新；也可用 --slug 指定技能
npx -y @yottameta/yotta-skills rollback --slug yotta-memory --agent codex
```

包内 manifest 可声明 `install.setup`、`install.doctor`、`install.rollback`，
值必须是包内相对路径。安装时先执行 setup，再执行内置 doctor 和自定义 doctor；
任一步失败都会恢复旧版本并留下安装证据。元阁只执行元阁家族包内的生命周期脚本，
不使用 shell，也不接受绝对路径或 `..` 路径。

## 编排路由（--route）

把需求摘要交给静态编排 playbook 和本地注册表，得到一组可执行建议：

```bash
# 文本输出：组合、调用顺序、角色、置信度、依据、缺失技能安装命令
npx -y @yottameta/yotta-skills --route "帮我润色输出，要规范可复制，别有 AI 味"

# 机器可读（JSON）
npx -y @yottameta/yotta-skills --route "检查代码质量，别糊弄" --json
```

- **输出**：候选组合、调用顺序、每个技能的角色、置信度、命中依据、已装/缺失状态、安装命令与应用模式提醒。
- **缺失技能**：只给安装命令，不自动安装；安装前应先做装前安全扫描，决定权在用户。
- **应用模式**：默认用户显式调用；切换为「按场景自动调用」需要用户确认。
- **无明确匹配**：低置信度回退到「入口 + 安装」组合，先澄清需求再继续。
- **边界**：路由是建议，不保证完全正确；关键动作由用户确认，数据不出本机。

## M1 记忆裁决与使用记录

`decide-memory` 判断哪些已装技能值得进入长期记忆，输出 `promote / hold / demote` 建议、分数与信号明细。
评分由用户显式配置的本地 provider（capability `m1.adjudicate`）完成；未配置 / 未授权 / 超时 / 非法输出时
只返回状态，不阻断其他能力，退出码保持 0。

```bash
# 默认只读：只看建议，不写任何文件
npx -y @yottameta/yotta-skills decide-memory

# 显式只读 + 信号明细
npx -y @yottameta/yotta-skills decide-memory --dry-run --explain

# 只写本地建议文件（不写元忆、不删除内容）
npx -y @yottameta/yotta-skills decide-memory --promote --json
```

使用记录默认关闭：

```bash
npx -y @yottameta/yotta-skills usage status
npx -y @yottameta/yotta-skills usage enable
npx -y @yottameta/yotta-skills usage mark --skill yotta-memory --signal used
npx -y @yottameta/yotta-skills usage disable
npx -y @yottameta/yotta-skills usage reset --yes
```

边界：记录只含技能 slug、时间、信号类型、playbook / confidence 与组合对；不含需求原文、记忆正文、路径或身份信息。
`--promote` 只写 `~/.yottaskills/memory-adjudication.json`，生成私密 `PREF` 记忆候选，由用户或 AI 再显式调用元忆写入。

### MCP：按需加载（可选）

本技能自带一个 MCP server：`yotta-skills`（`scripts/yotta-skills-mcp.py`，零依赖、数据不出本机），
基于 MCP 最新协议 2026-07-28（无状态时代；向后兼容 2025-11-25 及更早握手客户端）。
提供 `list_installed_skills`（盘点）/ `describe_skill`（单技能详情）/ `reindex`（强制重扫）/ `route_request`（编排路由，静态基线 + 可选本地动态扩展）/ `decide_memory`（M1 记忆裁决只读建议）五个工具。

**按需加载，不走常驻**：本技能与 MCP 均为按需触发。默认以 CLI 为主
（`npx -y @yottameta/yotta-skills --inventory`）；需要让 AI 通过工具直接调用时，再按下面配置启用。
**写客户端配置前必须先获得用户明确同意**：先展示目标配置文件路径、将写入的完整配置与影响（客户端需重启 / 重载一次），
用户确认后才写入；用户拒绝 → 不写配置，保持 CLI 用法，功能不受影响。

1. **检查当前客户端的 `mcpServers`** 是否已有 `yotta-skills` 条目；已有 → 直接使用。
2. **没有 → 先征得用户同意，再写入**下面这一条 server 配置（用后可移除，不要求常驻）：
   ```json
   {
     "mcpServers": {
       "yotta-skills": {
         "command": "python",
         "args": ["<技能目录>/scripts/yotta-skills-mcp.py"],
         "env": {
           "YOTTA_SKILLS_REGISTRY_FILE": "<配置目录>/yottaskills/<agentId>/registry.json"
         }
       }
     }
   }
   ```
   > `<技能目录>` = 本技能实际安装目录，**不要写死盘符路径**；Windows 用 `python`，Linux/macOS 用 `python3`。
   > 单 agent 环境可不设 `YOTTA_SKILLS_REGISTRY_FILE`；同一宿主内多 agent 共用 MCP 时，应分别配置独立路径，避免注册表状态互相覆盖。
3. **提醒用户**：改 `mcpServers` 后多数客户端需**重启 / 重载一次** MCP server 才生效；加载后应看到
   `list_installed_skills` / `describe_skill` / `reindex` / `route_request` / `decide_memory` 五个工具。
4. **降级兜底（重要）**：若客户端未暴露 MCP 工具 / 用户拒绝改配置 / 无法改配置 / server 未加载，**自动降级 CLI**
   （同一套扫描、路由与 M1 核心、结果一致）：`npx -y @yottameta/yotta-skills --inventory / --reindex / --route ... / decide-memory ...`。

## 版本策略

- 默认 **`pin`**：`npm pack` 使用清单中的精确版本（如 `@yottameta/yotta-present@0.6.2`），结果完全可复现，
  不会静默跟随 npm 上的浮动版本；
- `--range`（可选）：按清单 `major.x` 取 npm 最新 patch（如 `0.x`），仅在用户明确要求跟随 patch 时使用；
- 是否「已是最新」由目标目录 `<slug>/SKILL.md` 的 frontmatter `version` 与清单比对，
  一致即跳过（幂等）。

## 元信装前门禁

家族安装默认执行装前扫描。若本机没有元信（yotta-verify），元阁先按 `skills.json`
安装元信自身，再扫描待装技能。安装前会先读取包内 manifest、校验身份，再进入元信门禁：

- `SAFE TO INSTALL`：继续安装；
- `INSTALL WITH CAUTION` / `REVIEW REQUIRED`：继续安装，但显示风险并写入证据；
- `DO NOT INSTALL` 或扫描失败：阻断，不替换旧版本。

扫描后元阁会用包内 `scan-policy.json`（已审查例外表）复核：每条例外绑定「技能 + 版本 +
内容 treeHash + 规则 + 路径」，只豁免检测规则表、攻防样例与文档说明这类已审查命中。
技能升版或内容有任何变化，旧例外自动失效（fail-closed），安装回到元信原始判定。
命中例外的安装会显示 `↳ scanPolicy 复核：豁免 N 条已审查发现` 并写入安装证据；
未命中例外的 `DO NOT INSTALL` 照常阻断。

引擎查找顺序（v0.19.13 收紧）：`--verify` 指定路径 → 环境变量 `YOTTA_SKILLS_VERIFY` →
**受信安装记录**（`~/.yottaskills/trusted-verifier.json`，由安装管线在元信安装 / 更新成功后写入，
记录包身份 + 引擎路径 + SHA-256）。候选引擎必须同时满足：路径不经符号链接跳转、
包内 `SKILL.md` 与 `skill-manifest.json` 身份一致（slug / package / trust / 版本）、
引擎摘要与记录一致；任一不满足即 fail-closed，改走自举安装。
不再按本地注册表里 `name: yotta-verify` 的目录发现引擎。
`--skip-scan` 只保留为人工应急路径，使用时输出 `explicit-unverified` 并写入
`~/.yottaskills/install-log.jsonl`；`update --auto` 不会使用该开关。

## 支持智能体

17 个内置键名：`claude` `cursor` `codex` `gemini` `goose` `amp` `opencode` `windsurf`
`workbuddy` `kiro` `trae` `trae-cn` `qwen` `comate` `codebuddy` `kimi` `agents`。
未收录的智能体请用 `--dir` 指定其技能目录（`.agents/skills` 不是通用目录）。

## 依赖与回退链

| 依赖 | 角色 | 缺失时 |
|---|---|---|
| Node.js 18+ | 必需（CLI 本体） | 明确提示 + 按平台给安装命令 |
| npm | 拉包**回退通道** | 不影响：内置拉包为主 |
| 系统 tar | 解包**回退通道** | 不影响：内置解包为主 |
| Python 3.8+ | 元信装前扫描 | 门禁阻断；优先用 `--python` / `YOTTA_SKILLS_PYTHON` 指向宿主自带 Python（如 YottaCode），确实没有时用 `--skip-scan` 应急（`explicit-unverified`） |

缺依赖时按需给出「需要什么 / 为什么 / 一条修复命令 / 不影响使用」人话提示，不常驻提醒；
`doctor` 的依赖自检块只告警不失败。

## 环境变量

| 变量 | 作用 |
|---|---|
| `YOTTA_SKILLS_NPM` | 指定 npm 可执行文件（同 `--npm`） |
| `YOTTA_SKILLS_NPM_FLAGS` | 追加传给 `npm pack` 的参数（按空白拆分，如 `--registry=...`） |
| `YOTTA_SKILLS_NO_FALLBACK` | 设为 `1` 时禁用「默认源 404 → 官方源重试」的自动回退 |
| `YOTTA_SKILLS_FETCH` | 拉包通道：`builtin`（仅内置）/ `npm`（仅 npm）；缺省内置为主、失败回退 npm |
| `YOTTA_SKILLS_EXTRACT` | 解包通道：`builtin`（仅内置）/ `tar`（仅系统 tar）；缺省内置为主、失败回退系统 tar |
| `YOTTA_SKILLS_REGISTRY` | registry 地址（默认 `https://registry.npmjs.org/`；内置拉包与更新检查共用；支持 `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY`） |
| `YOTTA_SKILLS_PYTHON` | 指定 python 可执行文件（元信 scan 用，同 `--python`） |
| `YOTTA_SKILLS_VERIFY` | 指定 yotta_verify.py 路径（同 `--verify`） |
| `YOTTA_SKILLS_MANIFEST` | 指定技能清单 JSON 路径（默认随包 skills.json） |
| `YOTTA_SKILLS_REGISTRY_FILE` | 技能注册表文件路径（多 agent / 隔离环境用；默认 `~/.yottaskills/registry.json`） |
| `YOTTA_SKILLS_USAGE_FILE` | 使用记录文件路径（`usage` 记录落点；默认 `~/.yottaskills/usage.json`） |
| `YOTTA_PROVIDER_HOME` | provider 配置根目录（M1 裁决 / O1 动态路由；默认 `~/.yottameta/`，协议见 `references/provider-protocol.md`） |

### 隔离环境：三个状态文件成组导出

测试、CI 与多 agent 共存场景建议把下面三个状态文件变量**成组**导出，避免读写宿主真实状态；
只导出其中一个时，其余状态仍会落到用户目录（例如漏掉 `YOTTA_SKILLS_USAGE_FILE` 时，
`usage` 记录仍会写入 `~/.yottaskills/usage.json`）。

```bash
# bash（Linux / macOS / Git Bash）
export YOTTA_SKILLS_REGISTRY_FILE="${TMPDIR:-/tmp}/registry.json"
export YOTTA_SKILLS_USAGE_FILE="${TMPDIR:-/tmp}/usage.json"
export YOTTA_PROVIDER_HOME="${TMPDIR:-/tmp}/provider"
```

```powershell
# PowerShell（Windows）
$env:YOTTA_SKILLS_REGISTRY_FILE = "$env:TEMP\registry.json"
$env:YOTTA_SKILLS_USAGE_FILE = "$env:TEMP\usage.json"
$env:YOTTA_PROVIDER_HOME = "$env:TEMP\provider"
```

## 常见问题

- **npmmirror 全新包 404**：默认源返回 404 时安装器会**自动**改用官方源
  `https://registry.npmjs.org/` 重试一次（输出显示回退行，安装证据记 `npm_registry_fallback`）；
  若已显式指定 registry 或设置 `YOTTA_SKILLS_NO_FALLBACK=1`，则保持在指定源上，失败时给出可复制的修复提示。
- **未收录智能体**：`--agent <name>` 报未收录时，改用 `--dir` 指到它的技能目录。
- **Windows 下 npm 报错**：CLI 已内置 npm-cli.js 解析，无需额外处理；如需覆盖用 `--npm`。
- **某技能安装失败**：汇总报告会列出失败原因，可单装该技能排查。

## 参考

- **编排策划（组合决策表，先看这个）**：`references/orchestration.md`。
- 全家技能清单（人工可读版）：`references/skill-list.md`（机器权威源为 `skills.json`）。
- 内部机制：`references/install-flow.md`。
- 新手中文教程：`references/tutorial.md`。
- 常见问题：`references/faq.md`。
- 复杂场景走查：`references/walkthroughs.md`。
