# Hub（本机单点安装 + 链接分发）

## 它解决什么

多智能体各自维护技能目录时，同一技能会被复制多份，升级后容易版本漂移。Hub 把
技能集中到本机一份真源，再按宿主建立链接（Windows junction / macOS·Linux
symlink），升级只改真源，已链接宿主即时生效。

## 默认位置

- Hub 真源：`~/.yottaskills/hub`
- 技能台账：`<hub>/.yotta-hub.json`
- 链接台账：`<hub>/.yotta-links.json`
- 收敛回收站：`~/.yottaskills/trash/<时间戳>/<宿主>/<技能>/`（保留 7 天，可用 `YOTTA_SKILLS_TRASH` 覆盖）
- 覆盖方式（优先级）：`--hub <dir>` > `YOTTA_SKILLS_HUB` > `config.json`（`hub config set`）> 默认

## Hub 位置持久化（0.29.2 起；0.29.5 迁移向导 / 回滚 / 残留清理）

`hub config` 把 Hub 位置写进用户级配置（与 hosts.json / self.json 同根）：

```bash
npx -y @yottameta/yotta-skills hub config get                # 生效位置 + 来源 + 配置文件
npx -y @yottameta/yotta-skills hub config set --hub "D:\my-hub"        # 只换指针（旧 Hub 保留）
npx -y @yottameta/yotta-skills hub config set --hub "D:\my-hub" --move # 迁移：复制校验 → 重链 → 旧 Hub 入回收站
npx -y @yottameta/yotta-skills hub config rollback           # 回滚预览（上次迁移前的原位置）
npx -y @yottameta/yotta-skills hub config rollback --yes     # 执行回滚（位置回退，用当前内容）
npx -y @yottameta/yotta-skills hub config clear              # 清除覆盖（有技能时默认阻断，确认影响后加 --yes）
```

- 配置文件：`<YOTTA_SKILLS_HOME>/config.json`（默认 `~/.yottaskills/config.json`；schema v1，原子写）。
- 校验（fail-closed）：路径不能是文件、不能与配置根 / 独立安装目录重叠、不能是锁 / 数据桥接目录；路径不存在允许（首次使用时创建）。
- `--move` 语义：旧 Hub 复制到新位置 → 逐技能 treeHash 校验 → 切换配置 → `hub link` 以新 Hub 为源 `--force` 重链 → 旧 Hub 入回收站（保留 7 天）。校验失败不切配置；重链未全部完成时旧 Hub 保留供重试（新旧内容一致，混合链接均可用）。
- 目标目录只含元阁自己的空台账残留（`.yotta-hub.json` / `.yotta-hub-audit.jsonl`）时，`--move` 默认 fail-closed 并提示；确认后加 `--clean-residue`（残留移入回收站）再迁移。
- 迁移记录：`config.json` 的 `lastMigration` 记录时间 / from→to / 校验技能数 / 重链目录数 / 回收站与剩余天数；`hub config get` 展示「最近一次迁移」块与回滚命令。
- 回滚语义：`hub config rollback` 默认预览、`--yes` 执行 = 位置回退（把当前 Hub 内容复制校验回原位置，再重链、当前 Hub 入回收站 7 天）；**不是**恢复旧快照。目标非空 fail-closed（不合并）。
- 仅切换指针（不带 `--move`）时，若旧 Hub 非空会记录「未迁移」并在面板提示「旧 Hub 还有 N 个技能未迁移」+ 一键迁移；执行迁移 / 回滚后该提示自动清除。
- `hub config clear` 影响面防护（0.30.0）：当前配置 Hub 仍有技能时默认阻断（fail-closed），输出影响面（回落默认位置、真源与链接不移动）、替代路径（`hub config set --hub <新路径> --move`）与 `--yes` 指引；确认后加 `--yes` 执行。`hub config get` 若检测到运行中的 `view` 面板仍用旧位置，会提示重启面板生效。
- 面板「Hub 位置」区显示来源 / 配置覆盖 / 重启提示，并提供「设置新位置（迁移向导：迁移 / 仅切换，默认迁移）/ 最近一次迁移 + 一键回滚 / 清除覆盖」（写操作需页面令牌 + `hub-config` 确认串）；已在运行的 `view` 需重启后生效。
- 误用防护：`--hub` 只允许与 `hub` / `view` / `where` 一起使用；其它命令（含裸 `--hub`）fail-closed 报错，不再静默忽略。

## 备份 / 暂存残留清理（0.29.5 起）

`hub link --force` 替换真目录时，旧副本移入回收站（不再原地留 `<name>.yottaskills-backup-*`，宿主不会把备份当技能扫描）。历史残留可用：

```bash
npx -y @yottameta/yotta-skills hub cleanup-backups          # 预览（Hub + 已核实宿主）
npx -y @yottameta/yotta-skills hub cleanup-backups --yes    # 移入回收站（7 天可恢复）
```

- 识别标记：`.yottaskills-backup-*` / `.yottaskills-import-*` / `.yottaskills-rollback-*` / `.yottaskills-staging`。
- `hub doctor` 会只读报告 `backup_residue:*` 警告并给出清理命令；`--dir` / `--agent` 可收窄范围。

## 元技能唯一性收敛（`hub link` 执行时）

元技能（清单 27 + 特殊家族 5：元开 / 元伴 / 元呈 / 元阁本体 / 元信MCP）在
`hub link`（含面板链接动作）执行时收敛唯一性，不做事后全机扫描：

1. 收集宿主目录中的同名真目录与 `yotta-X__*` 重命名副本（frontmatter `name` 相同）；
2. 版本闸门：Hub 版本 ≥ 宿主副本版本才收敛；宿主更高 → 跳过并提示先 `hub update`；
   版本无法解析 → 跳过提示（fail-safe）；
3. 旧副本移入回收站（保留 7 天、输出恢复路径）→ 建立指向 Hub 的链接；
   跨盘（源目录在其它卷，或经 junction / symlink 落在其它卷）时 `rename`
   会报 `EXDEV`，自动回退「复制 → 校验（treeHash + 文件数 + 字节数）→ 删除源」；
   建链失败后的恢复同样支持跨盘回退，校验不通过不会删除源；
4. 先移后链；建链失败自动尝试恢复已移动副本，恢复失败时报出回收站路径；
   目标条目为指向 Hub 之外的链接时默认跳过；显式 `--force` 可替换为 Hub 链接
   （仅移除链接本身，目标目录不动；dry-run 报 `would-replace`）；
5. 外部技能保持原行为：同名冲突默认跳过，不自动删、不自动更新。

落地后跑一次 `hub link --all` 即可完成现存收敛。`hub doctor` 的
`single_source:*` 检查只读报告宿主中的多份副本与版本参差，不自动修改。
Hub 真源对清单声明了 `runtimePayload` 的技能（元忆 / 元阁：`bin`）保留运行时
载荷：链接分发后 OpenCode 等宿主直接获得 `bin/`，无需再单独补投影；普通宿主
安装仍为薄片（顶层 `bin` 默认跳过）。

## 链接范围（0.28.0 起）

`hub hosts` 把发现的目录分为三类，`hub link --all` / `hub unlink --all` 的
**默认范围只含已核实宿主**：

- **已核实（verified）**：映射经公开宿主表（Vercel Labs `skills@1.7.0`）、官方
  文档或本机自证（应用数据 / 配置 / 管理痕迹）核实 —— 默认链接；
- **自动发现（discovered）**：文件系统启发式扫到的目录 —— 默认不链，
  `--include-discovered` 显式纳入；
- **桥接（bridge）**：`XDG_STATE_HOME/skills`（官方 skills CLI 锁目录）与
  `XDG_DATA_HOME/skills`（数据桥接）—— 永不作为链接目标（`hub link --dir`
  指向时会被拒绝）；历史误链用 `hub unlink --dir <目录>` 显式清理（fail-closed，
  仍只删指向 Hub 的链接）。

未核实映射（如无文档 / 无自证的宿主）默认不链，可用 `--dir <目录>` 显式指定。
`hub doctor` 的 `link_scope:*` 检查只读报告「位于默认范围之外」的已建链接，
并给出 `hub unlink --dir <目录>` 的清理提示；`hub hosts` 输出三类的本机计数。

## 宿主状态细分与自定义注册（0.29.0 起）

每条宿主目录带生命周期状态（`hub hosts` / 面板宿主矩阵）：

- **可用**：目录存在 + 实体证据（应用标记 / 用户注册 / 手动标记）—— 默认链接 / 分发；
- **残留**：目录存在 + 无实体证据（卸载残留或 CLI-only 安装）—— 默认保留使用（仍可链接），
  可显式清理；文案统一「实体未确认」，不判定「已卸载」；
- **未创建**：目录不存在且无实体证据 —— 安装宿主后自动出现；
- **仅标记**：已装实体、技能目录未创建 —— `hub link --agent <id>` 会创建目录并链接。
- **隐藏标记**（`ignored`）：只影响列表显示，不拦截任何行为；真正拦截发现 / 显示 / 链接的是「不接管」（`hosts exclude`）。

`hub doctor` 的 `host_state:*` 检查对残留 / 仅标记给 info 提示，不判 fail。
自定义宿主目录可用 `hub hosts add` 注册进发现 / 分发 / 收编范围（只注册，
不创建目录、不改宿主配置；移除注册绝不删目录）：

```bash
# 注册 / 查看 / 移除自定义宿主（realpath 去重；Hub / 桥接目录拒绝注册）
npx -y @yottameta/yotta-skills hub hosts add ~/my-agent/skills --label "我的宿主"
npx -y @yottameta/yotta-skills hub hosts rename ~/my-agent/skills --label "新名字"   # 一步改名（只改显示名）
npx -y @yottameta/yotta-skills hub hosts list
npx -y @yottameta/yotta-skills hub hosts remove ~/my-agent/skills

# 手动标记状态（实体证据不足时）：available / orphan / ignored（隐藏标记，只影响显示）
npx -y @yottameta/yotta-skills hub hosts mark ~/my-agent/skills --state orphan

# 清理残留目录：默认预览；--yes 执行 —— 只删指向 Hub 的链接（含死链），
# 非 Hub 链接 / 非技能内容随目录保留在回收站（7 天，输出恢复路径）
npx -y @yottameta/yotta-skills hub hosts remove ~/my-agent/skills --purge
npx -y @yottameta/yotta-skills hub hosts remove ~/my-agent/skills --purge --yes
```

注册表 = `<root>/hosts.json`（root = `YOTTA_SKILLS_HOME` 或 `~/.yottaskills`，schema v1，
可 diff）；面板「宿主矩阵 → 添加自定义目录」等价可用，写操作需页面令牌与确认串。
移除注册 / 不接管后若该目录仍有 Hub 链接，CLI 会提示剩余条数与 `hub unlink --dir` 清理指引（面板确认框同源显示）。

## 不接管与目录覆盖（0.29.1 起）

**不接管**（excluded）：把某个智能体或目录从发现、显示、链接三层全部跳过
（`--include-discovered` 也不纳入）；已建立的链接不受影响，可用 `hub unlink` 清理：

```bash
npx -y @yottameta/yotta-skills hub hosts exclude box                    # 按 agentId
npx -y @yottameta/yotta-skills hub hosts exclude "D:\my-agent\skills"  # 按目录
npx -y @yottameta/yotta-skills hub hosts include box                    # 恢复接管
```

**目录覆盖**（override）：用户级覆盖某个已收录 agentId 的内置映射目录
（不改宿主配置；被覆盖的旧目录不再进入默认发现 / 链接）：

```bash
npx -y @yottameta/yotta-skills hub hosts set box --dir "D:\box-agent\skills"
npx -y @yottameta/yotta-skills hub hosts set box --clear     # 恢复内置映射
```

面板「宿主矩阵」提供等价动作：行内「不接管 / 编辑目录 / 标记可用 / 隐藏标记 / 重命名（自定义注册）」，
底部「不接管名单」区可「恢复接管」；写操作均写 Hub 审计。

**YottaCode 不纳入接管**：YottaCode 自带三层技能管理（skill-inventory / skill /
user-skills），元阁对其 `.yottacode` 路径与 `YOTTACODE_HOME` 子树在映射、扫描、
注册、标记、链接全部 fail-closed 排除，避免重复管理。

**未核实映射 ≠ 自动发现**：内置映射里尚未逐机核实的条目显示「映射·未核实」；
「自动发现」只用于文件系统扫描结果。`installed` 配对按「用户注册 / 已核实映射 > env >
未核实映射 > 自动发现」确定性优选（同级按技能数 + 路径稳定排序）。

## 命令

```bash
# 发现本机已装智能体与技能目录（文件系统优先；不读元忆 / 注册表）
npx -y @yottameta/yotta-skills hub hosts

# 状态过滤 / 自定义注册 / 残留清理（详见「宿主状态细分与自定义注册」节）
npx -y @yottameta/yotta-skills hub hosts --state orphan
npx -y @yottameta/yotta-skills hub hosts add ~/my-agent/skills --label "我的宿主"

# 安装 / 更新 Hub 真源
# 范围 = 全家清单 27 + 特殊家族 5；特殊家族跟随各自 npm latest
# 非元技能不参与更新（来源无统一安装源，用户自行处理）
npx -y @yottameta/yotta-skills hub install
npx -y @yottameta/yotta-skills hub update

# 接管各宿主现有技能：先只读预演，再复制收编（原目录保留）
# --apply 输出明示范围与目标 Hub；--skip-scan 会显式提示跳过装前扫描
# 非元技能 frontmatter 的严格 YAML 风险只读告警，不影响使用则不处理
npx -y @yottameta/yotta-skills hub adopt --scan
npx -y @yottameta/yotta-skills hub adopt --apply

# 非元阁来源技能没有统一更新源：手动从指定目录刷新
npx -y @yottameta/yotta-skills hub refresh my-skill --from <技能目录>

# 分发到全部已核实宿主（默认范围）：元技能链接时收敛旧副本（回收站 7 天）；
# 外部技能同名真目录默认跳过（--force 才把旧副本移入回收站并替换）
npx -y @yottameta/yotta-skills hub link --all

# 显式把自动发现目录一并纳入（桥接目录永不链接）
npx -y @yottameta/yotta-skills hub link --all --include-discovered

# 只删除链接，不动 Hub 真源；--dir 不带 slug 时以文件系统为真源清理该目录全部 Hub 链接
npx -y @yottameta/yotta-skills hub unlink --all

# 指定智能体分发 / 解除（只影响该宿主；Hub 真源保留）
npx -y @yottameta/yotta-skills hub link yotta-memory --agent codex
npx -y @yottameta/yotta-skills hub unlink yotta-memory --agent codex

# 彻底删除 Hub 技能：全宿主清链接（含死链）+ 目录入回收站 + 清台账 + 审计
npx -y @yottameta/yotta-skills hub remove my-skill --dry-run

# 查看来源、版本、链接宿主与异常
npx -y @yottameta/yotta-skills hub status
npx -y @yottameta/yotta-skills hub doctor
```

## 删除技能（hub remove，0.28.3 起）

`hub remove <slug>` 五阶段 fail-closed：

1. **preflight（只读）**：逐目录分类健康链接 / 死链 / 漂移链接 / 指向 Hub 外链接 /
   真副本 / 不存在；`--dry-run` 到此为止（零写入）。
2. **unlink**：只删指向 Hub 的链接（含死链）；报错即中止，不进入下一步。
3. **trash**：Hub 目录移入 `<hub>/../trash/<stamp>/hub-remove/<slug>`，保留 7 天；
   跨卷自动回退「复制 → 校验 → 删源」。
4. **ledger**：定向删 `.yotta-hub.json` 条目 + 过滤 `.yotta-links.json`
   （不调 `syncHubState`，防止把删除记回 `missing`）。
5. **审计 + 汇总**：写 `remove` 审计；无痕迹时退出码 4。

边界：真副本 / 外部链接一律保留并报告（真副本版本高于 Hub 时逐条提示）；
`--agent` / `--dir` 收窄仅用于「Hub 目标已缺失」的死链清理；恢复路径 =
从回收站取回 + `hub install` 重装 + `hub link` 重建。

## 宿主发现口径

1. 已收录宿主映射（81 条；兼容 Vercel Labs `skills` CLI / SkillCat 的公开宿主表，
   经 0.28.0 逐智能体核实：XDG 解析只覆盖 skills CLI 表确认的 `.config/agents`、
   `.config/devin`、`.config/opencode` 三类 rel，其余 `.config/...` 按字面
   `~/.config` 解析）；
2. 环境变量覆盖（`CODEX_HOME`、`XDG_CONFIG_HOME`、`DSH_HOME`、
   `OPENCLAW_STATE_DIR`、`CLAUDE_CONFIG_DIR` 等）；
3. 常见配置根启发式扫描；
4. `YOTTA_SKILLS_DISCOVERY_ROOTS` 显式补充（自动发现类，需 `--include-discovered`）；
5. `--dir <path>` 精确指定非标准宿主。

自动发现默认排除临时目录、`.bak`、candidate / staging、插件构建目录等噪声。

## 兼容标准

- 技能格式：`agentskills.io` Agent Skills（`SKILL.md` + `name` / `description`）。
- 通用投影：`~/.agents/skills`、`$XDG_CONFIG_HOME/agents/skills`。
- 官方锁文件：只读兼容 Vercel Labs `skills` CLI 的 `.skill-lock.json` v3
  （`$XDG_STATE_HOME/skills/` 或 `~/.agents/`）。

## 本地面板（yotta-skills view）

```bash
npx -y @yottameta/yotta-skills view
npx -y @yottameta/yotta-skills view --port 8790
```

面板只在 `127.0.0.1`（默认 8789）监听，零远程资源、零遥测，只读写 Hub
目录与台账 / 证据文件，不读元忆、不改宿主全局配置。六个视图：概览、宿主矩阵、
收编向导、链接与体检、记录与回滚、路由与编排，另附**全量 CLI 页**（全部命令 /
子命令 + 人话说明 + 可复制示例 + 完整选项，与 `--help` 单一真源）。

动作边界：收编 / 链接 / 解除 / 回滚 / 删除技能可执行（预览 → 确认 → 执行 → 证据；
删除技能需手输 slug 二次确认）；概览 Hub 内容行可过滤后直接删除技能；
install / update / refresh 只在高级 CLI 页给出可复制命令，不在网页执行。
写操作需要页面会话令牌，解除与回滚需要破坏性确认串；收编始终逐项运行元信
扫描，high / critical 阻断。

## 安全边界

- `unlink` 只删除 lstat 确认为链接、且 readlink 目标位于当前 Hub 内的路径；`--dir` 不带 slug 时以文件系统为真源枚举该目录（台账缺失也能清理），指向其它位置的链接 fail-closed 不动并给出错位警告。
- 真目录 / 非 Hub 链接一律拒绝删除；`--force` 对真目录把旧副本移入回收站（7 天）再替换；
  替换失败会把旧副本移回原位（回收站路径随结果输出）。
- `remove` 只删指向 Hub 的链接与 Hub 内目录；链接清理报错即中止、不删 Hub；
  Hub 目录入回收站保留 7 天，可恢复。
- 收敛只动元技能在宿主目录中的旧副本：移入回收站（7 天）而非直删；
  不碰插件与宿主 MCP 配置；外部技能源文件绝不修改。
- Hub 仅本机使用，不对外分发技能内容。
