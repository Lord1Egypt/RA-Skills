<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-skills banner" width="100%" />
</p>

<h1 align="center">yotta-skills · 元阁 (YuanGe)</h1>

<p align="center">YottaMeta 的<b>技能生态编排路由 + 全家一键安装器 + 技能盘点</b>：先按需求路由该组合哪几个技能，再一条 <code>npx</code> 命令把已发布的全部
<code>yotta-*</code> 技能（当前 <b>27</b> 个）装进指定智能体或目录。</p>
<p align="center">看清单、路由组合、装全家、增量更新、<code>--dry-run</code> 预览、<code>--pin</code> 锁版本--
幂等、零依赖（Node.js 18+）、纯 npm 生态。</p>
<p align="center">本包<b>不含任何技能本体</b>——只做「清单 + 下载 + 落位 + 汇总」；每个技能仍走各自 npm 包。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-skills"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-skills" /></a>
  <a href="https://github.com/YottaMeta/yotta-skills"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-skills" /></a>
  <a href="https://github.com/YottaMeta/yotta-skills/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-skills" /></a>
  <a href="https://github.com/YottaMeta/yotta-skills"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

以前装元阁全家要逐个 <code>npx</code> 跑很多次。元阁把它变成一条命令：读内置清单（27 个已发布技能）、
逐个从各自 npm 包下载、落位到目标技能目录、打印汇总（成功 / 跳过 / 失败）。

元阁也是全家的**编排策划层**：接到需求先查「编排策划」组合表——该组合哪几个技能、按什么顺序、各自强在哪——然后给出安装与调用**建议**，由用户确认后执行。决策表随包提供（<code>references/orchestration.md</code>），<code>SKILL.md</code> 中有摘要。

- **看清单**--全家技能一览：slug / 中文名 / 包名 / 版本 / 一句话说明。
- **编排路由**--`--route` 按需求摘要输出候选组合、调用顺序、技能角色、置信度、依据、已装/缺失状态与安装命令；非元阁家族已装技能按 frontmatter description 机械匹配作并列候选（标注来源与未扫描状态，只读不自动调用）；只建议安装，不自动安装。可选本地扩展提供方可在已装白名单内增补 / 重排，并返回 `confidence` / `reasons` / `summary` / `alternatives`（未配置时行为不变），协议见 `references/provider-protocol.md`。
- **M1 记忆裁决**--`decide-memory` 输出技能 `promote / hold / demote` 只读建议、分数与信号明细；评分由用户显式配置的本地 provider（capability `m1.adjudicate`）完成。默认只读，`--promote` 只写本地建议文件，不写元忆、不删除内容。`usage` 默认关闭，显式开启后才记录结构化使用信号（不含需求原文）。
- **安装**——装全家（或指定技能）到智能体默认用户级目录或任意目录。
- **更新**——增量更新：补齐缺失技能、升级版本不一致的技能。
- **更新检查 / 自动更新**——<code>update --check</code> 只读比对已装技能版本与 npm 注册表并报告；<code>update --check --scheduled</code> 是后台周检入口，用本地缓存和随机抖动做到未到期不联网；<code>update --auto</code> 检查后自动把已装元阁家族升到最新（非元阁家族技能绝不自动更新）。
- **自检 / 回滚**——<code>doctor</code> 只读检查技能目录、版本、manifest、注册表和自定义 doctor，`--dir` 可直接指向单个技能包目录；<code>rollback</code> 校验快照后恢复最近一次安装或更新，恢复失败不会覆盖当前目录。
- **运行时 hook 适配层**——技能 manifest 只声明六个生命周期要求；<code>hook capabilities / evaluate / bind / unbind</code> 负责宿主能力探测、确定性决策、结构化证据和降级标注，不把 audit 能力夸大为强制。
- **幂等**——已在清单版本的技能跳过；重复运行安全。
- **装前门禁**——家族安装先读取包内 manifest，元信（yotta-verify）缺失时自动自举，再逐个扫描。`DO NOT INSTALL` 阻断；`CAUTION` / `REVIEW` 继续但显示风险。旧版本会先做快照再替换。
- **无 npm 也能接管**——拉包与解包默认走 Node 内置通道（npm / 系统 tar 仅作回退）；`update --installed-only` 只接管机器内已安装的元技能，不补装、不新增、不报错。
- **盘点 / re-index**--扫描本机各智能体技能目录，维护本地注册表（<code>~/.yottaskills/registry.json</code>）；可用 <code>YOTTA_SKILLS_REGISTRY_FILE</code> 为不同 agent 指定独立注册表；自包含，不需要任何其他技能。新装技能自动被发现：<code>install</code> / <code>update</code> 完成后自动重扫注册表，<code>--reindex</code> 可随时手动重扫（如会话开工）。可选 <code>yotta-skills</code> MCP（按需加载、不常驻）提供 <code>list_installed_skills</code> / <code>describe_skill</code> / <code>reindex</code> / <code>route_request</code> / <code>decide_memory</code> 五工具，配置见 <code>SKILL.md</code>。

边界：只做「下载 + 落位 + 门禁 + 汇总」——**不**开发技能内容、**不**内置任何技能本体、**不**用 <code>-g</code>
全局安装；除目标目录外，会在 <code>~/.yottaskills</code> 下保留注册表、快照、安装证据与更新检查缓存。

## 使用案例

**1. 一次把全家装进一个智能体。** `npx -y @yottameta/yotta-skills install --agent codex` 读清单、用装前门禁逐包扫描、落位每个技能（已最新的自动跳过），完成后自动重扫注册表。

**2. 单点真源 + 全宿主分发。** `hub install` 把全家装进一个本机 Hub 目录，`hub link --all` 再以 junction / symlink 分发到全部已核实宿主；`hub status` / `doctor` 显示每个副本指向哪里、有没有漂移。

**3. 盘点已装了什么、一个任务该用哪几个。** `--inventory` / `--reindex` 扫描本机技能目录写入本地注册表；`--route "<需求摘要>"` 给出候选组合、调用顺序、每个技能的角色、置信度、依据、已装 / 缺失状态与安装命令。路由只建议，不自动安装。

## 快速使用

首选流程（Hub 主路径，安装本体与智能体无关）：

```bash
# 1) 看本机有哪些宿主与技能目录（状态细分：可用 / 残留 / 未创建 / 仅标记）
npx -y @yottameta/yotta-skills hub hosts

# 2) 装进 Hub 真源（默认 ~/.yottaskills/hub；无需指定智能体）
npx -y @yottameta/yotta-skills hub install

# 3) 分发到全部已核实宿主（Windows junction / macOS·Linux symlink）
npx -y @yottameta/yotta-skills hub link --all

# 4) 图形化面板管理（宿主矩阵 / 链接与体检 / 收编 / 回滚）
npx -y @yottameta/yotta-skills view
```

元阁独立安装（把管理引擎装成独立 CLI，不依赖任何智能体）：

```bash
npx -y @yottameta/yotta-skills install-self                    # 默认 ~/.yottaskills/yotta-skills
npx -y @yottameta/yotta-skills install-self --dir ~/tools/yotta-skills
npx -y @yottameta/yotta-skills where                           # 查看运行中 CLI / 独立安装 / Hub 位置
```

指定智能体直装（兼容路径）：

```bash
# 列出全家技能（不联网、不改动）
npx -y @yottameta/yotta-skills --list

# 装全家到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-skills install --agent codex

# 装全家到任意目录（每个技能落在 <dir>/<slug>）
npx -y @yottameta/yotta-skills install --dir ~/my-skills

# 只装个别技能
npx -y @yottameta/yotta-skills install yotta-memory yotta-verify --dir ~/my-skills

# 增量更新已装技能
npx -y @yottameta/yotta-skills update --agent codex

# 只读检查更新（不改动；手动或由 doctor / 发布前检查触发）
npx -y @yottameta/yotta-skills update --check

# 后台周检入口（未到期不联网；到期单次检查并写缓存）
npx -y @yottameta/yotta-skills update --check --scheduled

# 检查后自动更新已装元阁家族（含装前门禁；非元阁家族技能不自动更新）
npx -y @yottameta/yotta-skills update --auto

# 只接管机器内已装的元技能（不补装缺失；清单只作身份 / 版本参照）
npx -y @yottameta/yotta-skills update --installed-only --dir ~/my-skills

# 只读检查已装技能（可加 --slug / --json）
npx -y @yottameta/yotta-skills doctor --dir ~/my-skills --slug yotta-memory

# 查看快照；恢复最近一次安装或更新
npx -y @yottameta/yotta-skills rollback --list --dir ~/my-skills
npx -y @yottameta/yotta-skills rollback --slug yotta-memory --dir ~/my-skills

# 查看宿主 hook 能力并评估一次 manifest 事件
npx -y @yottameta/yotta-skills hook capabilities --host codex --json
npx -y @yottameta/yotta-skills hook evaluate --host codex --event before_send --manifest ./skill-manifest.json --json

# 预览将安装清单（不联网、不改动）
npx -y @yottameta/yotta-skills --dry-run

# 按需求摘要给出组合、顺序与缺失技能安装建议
npx -y @yottameta/yotta-skills --route "检查代码质量，别糊弄"

# 查看 / 开启本地使用记录（默认关闭）
npx -y @yottameta/yotta-skills usage status
npx -y @yottameta/yotta-skills usage enable

# M1 记忆裁决只读建议；--promote 只写本地建议文件
npx -y @yottameta/yotta-skills decide-memory --explain
npx -y @yottameta/yotta-skills decide-memory --promote --json

# 盘点本机已装技能（自包含扫描，不依赖任何元技能）
npx -y @yottameta/yotta-skills --inventory

# 重扫注册表（随时手动运行；install / update 完成后已自动重扫）
npx -y @yottameta/yotta-skills --reindex

# 发现本机已装智能体与技能目录（文件系统优先，不读元忆 / 注册表）
npx -y @yottameta/yotta-skills hub hosts

# 单点装到本机 Hub，再链接分发到全部已核实宿主（默认范围）
npx -y @yottameta/yotta-skills hub install
npx -y @yottameta/yotta-skills hub adopt --scan
npx -y @yottameta/yotta-skills hub adopt --apply
npx -y @yottameta/yotta-skills hub link --all
# 显式把自动发现目录一并纳入（锁 / 数据桥接目录永不链接）
npx -y @yottameta/yotta-skills hub link --all --include-discovered
npx -y @yottameta/yotta-skills hub status
npx -y @yottameta/yotta-skills hub doctor
```

前置：Node.js 18+、npm、系统 tar（Windows 10+ / macOS / 多数 Linux 自带）。

## 命令与选项

| 命令 / 选项 | 作用 |
|---|---|
| `--list`（`-l`） | 列出全家技能 + 版本 + 说明；可加技能名过滤 |
| `install-self [--dir <path>] [--dry-run] [--force]` | 元阁独立安装：把管理引擎装到独立位置（默认 `~/.yottaskills/yotta-skills`）；不写宿主配置、不建全局 shim |
| `where [--json]` | 查看元阁位置：运行中 CLI / 独立安装目录（标记当前运行项）/ Hub 真源 |
| `install --agent <name>` | 装全家到指定智能体默认用户级技能目录（兼容直装路径） |
| `install --dir <path>` | 装全家到指定目录，每个技能落在 `<path>/<slug>` |
| `install <skill>... [--agent <name> \| --dir <path>]` | 只装指定的一个或多个技能 |
| `update [--agent <name> \| --dir <path>]` | 增量更新：补齐缺失、升级版本不一致的技能 |
| `update --check` | 只读更新检查：比对已装版本与 npm 注册表并报告（退出码 0=最新 / 3=有更新 / 1=无法检查；可用 `--registry <url>` 指定镜像）；不改动 |
| `update --check --scheduled` | 后台周检入口：未到期不联网；到期只检查一次并写本地缓存；文本失败静默，`--json` 保留诊断；始终退出 0 |
| `update --auto` | 检查后自动更新已装元阁家族到最新（含装前门禁；非元阁家族技能绝不自动更新） |
| `doctor [--agent <name> \| --dir <path>] [--slug <slug>]` | 只读自检：SKILL / 版本 / manifest / 注册表 / 自定义 doctor；`--dir` 可指向技能集合目录或单个技能包目录；退出码 0=通过 / 4=没有可检查对象 / 1=检查失败 / 6=manifest 身份失败 |
| `rollback [--agent <name> \| --dir <path>] [--slug <slug>]` | 校验并恢复最近一次快照；`--list` 只列快照；`--json` 输出机器可读结果 |
| `hook capabilities --host <name>` | 查看六个统一事件的宿主能力矩阵；未知宿主默认 `unsupported` |
| `hook evaluate --host <name> --event <event> --manifest <file> --context <json>` | 评估 manifest hook 事件，返回 allow / block / warn / unverified，并写结构化证据 |
| `hook bind --host <name> --manifest <file>` / `hook unbind <id>` | 幂等注册或反注册 hook 声明 |
| `--registry <url>` | 检查的 npm registry 地址（默认 https://registry.npmjs.org/；`YOTTA_SKILLS_REGISTRY` 覆盖） |
| `--inventory` | 盘点已装技能：扫描技能目录并更新本地注册表（自包含）；`--json` 输出 JSON、`--project` 附扫项目级目录 |
| `--reindex` | 重扫注册表：扫描技能目录并增量合并变化（install / update 完成后自动重扫，也可随时手动运行；`--rescan` 同义）；`--json` 输出 JSON |
| `hub hosts [--json] [--state <state>]` | 发现宿主与技能目录（文件系统 + 环境变量；不读元忆 / 注册表）；状态细分（可用 / 残留 / 未创建 / 仅标记）；`--state` 过滤；`--json` 输出 JSON |
| `hub hosts add <dir> [--label <名称>] [--id <agentId>]` | 注册自定义宿主目录（只注册，不创建目录、不改宿主配置；Hub / 桥接目录 fail-closed 拒绝） |
| `hub hosts remove <dir \| --id <agentId>> [--purge [--yes]]` | 移除注册（绝不删目录）；`--purge` = 清理残留目录（默认预览，`--yes` 执行；只删指向 Hub 的链接，目录入回收站 7 天） |
| `hub hosts list` / `hub hosts mark <dir> --state <available\|orphan\|ignored>` | 查看注册表 / 手动标记宿主状态（与注册表共用存储） |
| `hub config get \| set --hub <path> [--move] \| clear` | Hub 位置持久化（`config.json`；优先级 `--hub` > `YOTTA_SKILLS_HUB` > config > 默认）；`--move` = 复制校验 → 重链 → 旧 Hub 入回收站（7 天），fail-closed |
| `hub install [skill...]` | 把元技能安装到本机 Hub 真源（默认 `~/.yottaskills/hub`；`--hub` / `YOTTA_SKILLS_HUB` 覆盖） |
| `hub adopt --scan` | 只读预演：扫描各宿主现有技能，输出收编候选、多副本冲突与已在 Hub 状态 |
| `hub adopt --apply [--include <a,b>] [--force] [--in-place]` | 把选中技能收编进 Hub；默认复制保真 + 原目录保留；非元阁来源标注「无更新源」 |
| `hub refresh <slug> --from <path>` | 手动同步非元阁技能（重新收编 + 更新哈希 + 台账） |
| `hub link --all [--include-discovered]` | 把 Hub 技能链接到全部已核实宿主（默认范围；`--include-discovered` 纳入自动发现目录）；指定智能体分发用 `hub link <技能> --agent <id>`；Windows junction / POSIX symlink |
| `hub unlink --all` | 只删除链接，不动 Hub 真源（fail-closed；真目录 / 非 Hub 链接一律拒绝）；指定智能体解除用 `hub unlink <技能> --agent <id>`；清理范围外链接用 `--dir <目录>` 精确指定 |
| `hub remove <slug> [--dry-run] [--include-discovered]` | 删除 Hub 技能：全宿主清链接（含死链）+ Hub 目录入回收站（7 天）+ 清 Hub / 链接台账 + 写审计；fail-closed（真副本 / 外部链接保留并报告；链接报错即中止不删 Hub）；`--agent` / `--dir` 收窄仅用于死链清理 |
| `hub status` | 查看 Hub 技能来源、版本、链接宿主与异常；`--json` 输出 JSON |
| `hub doctor` | 检查断链 / Hub 目标缺失 / slug 不一致 / 链接范围（`link_scope`）/ 目录权限；异常时退出码 1；`--json` 输出 JSON |
| `--route <需求摘要>` | 编排路由：输出组合、调用顺序、技能角色、置信度、依据、已装/缺失状态与安装建议；可选本地扩展提供方在已装白名单内增补 / 重排并返回 `confidence` / `reasons` / `summary` / `alternatives`（未配置时行为不变，协议见 `references/provider-protocol.md`）；`--json` 输出 JSON 与 `dynamic` 状态块、`--project` 附扫项目级目录 |
| `usage status` / `usage enable` / `usage disable` | 查看 / 开启 / 关闭本地结构化使用记录；默认关闭，只记录 slug、时间、信号类型、playbook / confidence 与组合对 |
| `usage mark --skill <slug> --signal used\|named\|accepted` | 记录一次显式使用信号；不要求先 enable |
| `usage reset --yes` | 清空本地使用记录 |
| `decide-memory [--dry-run\|--promote] [--explain]` | M1 记忆裁决只读建议；`--promote` 只写本地建议文件，不写元忆、不删除内容；`--json` 输出稳定 JSON |
| `--no-reindex` | 安装 / 更新后不自动重扫注册表 |
| `--dry-run` | 预览将执行的安装 / 更新清单；不联网、不改动 |
| `--pin` | 锁死清单精确版本（默认） |
| `--range` | 跟随同 major 最新 patch（非默认：显式指定后才浮动跟随） |
| `--force` | 已是最新也重新安装 |
| `--skip-scan` | 人工应急路径：跳过元信门禁并标记 `explicit-unverified`；`update --auto` 不使用该开关 |
| `--npm <path>` | 指定 npm 可执行文件 |
| `--python <path>` | 指定 python 可执行文件（元信 scan 用） |
| `--verify <path>` | 指定 yotta_verify.py 路径 |
| `-h, --help` / `-v, --version` | 帮助 / 版本 |

不带命令直接给技能名时，等价于 `install <skill>`。

支持 17 个智能体键名：`claude` `cursor` `codex` `gemini` `goose` `amp` `opencode` `windsurf`
`workbuddy` `kiro` `trae` `trae-cn` `qwen` `comate` `codebuddy` `kimi` `agents`。
未收录的智能体请用 `--dir` 指到它的技能目录（`.agents/skills` 不是通用目录）。

## 版本策略

- 默认 `pin`：`npm pack <pkg>@<清单精确版本>`——完全可复现，不会静默跟随 npm 上的浮动版本；
- `--range`（可选）：`npm pack <pkg>@<major>.x`——取清单同 major 的最新 patch，仅在你明确要求跟随 patch 时使用；
- 是否「已是最新」由目标 `<dir>/<slug>/SKILL.md` 的 frontmatter `version` 与清单比对，一致即跳过。

## 安装

> **先分清两层**：`yotta-skills`（元阁）是「全家技能安装器」，本身**不含任何技能本体**。它所做的事是把已发布的 27 个 `yotta-*` 技能从各自 npm 包装进目标目录，所以「拿到元阁」不等于「已装齐技能」——拿到后还需运行一次 `install`，才会把全家真正放进目标目录。单个技能（如 `@yottameta/yotta-memory`）是各自独立的 npm 包、装自己即可；元阁是「一次装齐全家」的管理器，安装方式与此不同。

下面四种方式任选，顺序即推荐优先级；本包一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。方式二 / 三只「拿到安装器」；方式四只把「安装器技能」本身装进智能体目录——都仍需再跑一次 `install` 才装齐全家。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-skills install --agent <智能体名称>      # 装全家到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-skills install --dir <你的技能目录>     # 装全家到指定目录（如 ~/.codex/skills）
```

- `npx` 会自动拉取最新版 `yotta-skills`，无需单独安装步骤；这是唯一「拿到安装器 + 装齐全家」一步到位的方式。
- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-skills.git <你的技能目录>/yotta-skills
cd <你的技能目录>/yotta-skills
node bin/yotta-skills.js install --dir <你的技能目录>
```

- 克隆只拿到**安装器**；`--list` 只会打印清单、不安装任何东西。跑 `install` 才会把全家装进目标目录。

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-skills` 点 **Code → Download ZIP**，解压后跑 `node bin/yotta-skills.js install --dir <你的技能目录>` 装齐全家。把 `yotta-skills` 文件夹放进智能体技能目录只让**安装器技能**本身可被调用（它有自己的 `SKILL.md`），并不会把 27 个技能一并带进去——那仍需跑 `install`。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 把「安装器技能」本身装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 把「安装器技能」本身装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

- `install.sh` 把「元阁安装器技能」本身装进智能体 / 目录，让代理能调用元阁；要装齐 27 个技能，再执行 `node bin/yotta-skills.js install --agent <name>`（或 `--dir <path>`）。

### 方式五：OpenClaw（宿主官方命令）

```text
openclaw skills install @yottameta/yotta-skills   # 安装（含 ClawHub 安全审计）
openclaw skills update @yottameta/yotta-skills    # 更新
```

- OpenClaw 使用 `~/.openclaw/skills` 技能目录；元阁的 `--inventory` / `--reindex` 已能识别该目录（含 `OPENCLAW_STATE_DIR` 覆盖）。
- 走宿主官方命令可保留 ClawHub 安全审计卡与更新追踪（`openclaw skills update` 只覆盖 ClawHub 追踪安装的技能）。

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

## 全家技能清单

27 个技能的 slug / 中文名 / 包名 / 版本 / 说明见 `references/skill-list.md`（机器权威源为
`skills.json`）。家族分布：安全与护栏（12）/ 质量与工程（4）/ 记忆与上下文（3）/ 写作与表达（1）/
工作流（1）/ 入口与引导（1）。

## 工作原理

对清单里每个技能：`npm pack <pkg>@<spec>` 到临时目录 → `tar -xzf` 解压 → 读取 manifest →
元信装前门禁 → 快照旧版本并暂存新版本 → 原子替换 `<dest>/<slug>` → setup / doctor → 汇总报告；
任一步失败会恢复旧版本。`rollback` 可校验并恢复已有快照。`install` / `update` 完成后自动重扫本地技能注册表，
新装技能随即出现在 `--inventory` / `--reindex` 里（可用 `--no-reindex` 关闭）。
细节见 `references/install-flow.md`；新手中文教程见 `references/tutorial.md`。

## 开发与校验

```bash
# 在技能目录内跑测试
npm test
```

测试覆盖 `--list`、临时目录安装断言、幂等、`--pin`、`update`、异常路径、manifest 校验、元信自举与装前门禁
（用 fake npm 不联网）。

## 参考文档

- 常见问题：`references/faq.md`
- 复杂场景走查：`references/walkthroughs.md`

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
