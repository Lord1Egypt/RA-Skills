# Changelog

## v0.30.14 (2026-11-14)

- **元忆联动**：`skills.json` 的 `yotta-memory` pin 更新到 **0.24.3**，同步 `references/skill-list.md`。
- **扫描例外重绑**：按元忆 0.24.3 的干净 LF 候选 tarball 重建 `scan-policy.json`。
- **发布期修复**：处理 Linux CI 上命中打点 mtime 断言的 Node 原生亚微秒精度差异。

## v0.30.13 (2026-11-14)

- **元忆联动**：`skills.json` 的 `yotta-memory` pin 更新到 **0.24.2**，同步 `references/skill-list.md`。
- **扫描例外重绑**：按元忆 0.24.2 的干净 LF 候选 tarball 重建 `scan-policy.json`。
- **发布期修复**：元忆 0.24.1 的 CI 在 Linux 上暴露 Windows profile 路径解析缺陷；本版随元忆 0.24.2 重新签发。

## v0.30.12 (2026-11-14)

- **清单联动**：`skills.json` 的 `yotta-memory` pin 更新到 **0.24.1**，同步 `references/skill-list.md`。
- **扫描例外重绑**：按元忆 0.24.1 的干净候选 tarball 重建 `scan-policy.json`；旧版本例外自动失效。
- 兼容性：元阁命令、参数、安装流程与清单结构不变；本版仅清单 pin、扫描例外和版本同步。

## v0.30.11 (2026-11-12)

- **清单联动**：`skills.json` 的 `yotta-memory` pin 从 0.23.3 更新到 **0.24.0**，同步 `references/skill-list.md`。
- **扫描例外重绑**：按元忆 0.24.0 候选 tarball 的 treeHash 重建 `scan-policy.json`；检测规则、路径与例外策略不变，旧版本例外自动失效。
- 兼容性：元阁命令、参数、安装流程与清单结构不变；本版仅清单 pin、扫描例外和版本同步。

## v0.30.10 (2026-11-06)

- 最终修正 Linux `spawnSync` 对超大 stdout 的截断差异：内部最多捕获 1 MiB，再按 256 KiB 业务上限统一返回 `error`。
- 技能与插件同步到 0.30.10；0.30.9 的插件已发布但缺少本项最终修复，不回写旧版本。

## v0.30.9 (2026-11-06)

- provider stdout 超限改为在 Windows / Linux 一致返回 `error`，不再因 Node 平台差异落到 `invalid_output`。
- 发布测试改为干净 checkout 自包含：pilot hook manifest、scan-policy 路径、跨仓覆盖检查与 Hub adopt 环境隔离不再依赖本机兄弟仓或真实宿主。

## v0.30.8 (2026-11-05)

- scan-policy 补测试夹具例外；测试字面量去自命中；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。
- S6 候选收口：scan-policy 改为从 LF 干净候选 tarball 重绑，修正 7 个技能在 CRLF 工作树口径下的 treeHash 漂移。

## v0.30.7 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.30.6 (2026-10-25)

- **ClawHub 英文门面（无引擎变更）**：发布副本改为英文优先的双语 `summary` / `description`（英文在前、中文关键词保留在后）并补英文 tags，上线后 ClawHub 技能卡摘要由超长中文变为英文优先；同时以更高版本覆盖此前在该市场提交后未转公开的两版。
- **README 使用案例**：英文 / 中文 README 首屏新增「使用案例」三条（一条命令装全家 / Hub 单点真源 + 全宿主分发 / 盘点与路由建议）。
- **清单联动（发布期）**：`skills.json` pin `yotta-memory` 0.23.0 → **0.23.1**；`references/skill-list.md` 同步；安装扫描例外表按 npm 真包口径重绑（`yotta-memory` 0.23.1 / treeHash `578570c2…` / 18 文件 / 1,367,666 B；9 技能 / 37 例外）。
- 兼容性：命令、参数、清单结构与安装行为全部不变；本次仅门面文案、发布副本与清单版本。

## v0.30.5 (2026-10-25)

- **清单联动（发布期）**：`skills.json` pin `yotta-humanize` 0.2.2 → **0.2.3**（去 AI 味即时入口包装：展示名 / 摘要 / 描述 + README 首屏 + 2 条真实 before/after 案例；检测与改写引擎逻辑不变）；`references/skill-list.md` 同步；`scan-policy.json` 无需重绑（元真不在扫描例外表内）。

## v0.30.4 (2026-10-20)

- **清单联动（发布期）**：`skills.json` pin `yotta-memory` 0.22.9 → **0.23.0**（上下文包 COMMIT 段保留策略 + 归档门槛 0.35→0.55 + 规模体检补强 + 用法引导）；`references/skill-list.md` 同步；`scan-policy.json` 按 npm 真包口径重绑（yotta-memory 0.23.0 / treeHash `d18537c9…` / 18 文件 / 1,364,905 B；9 技能 / 37 例外）。

## v0.30.3 (2026-10-13)

- **清单联动（发布期）**：`skills.json` pin `yotta-learn` 0.6.0 → **0.6.4**（含面板弹窗 / 写库门槛 / 端口 fail-fast / 排空超时四项修复）；`references/skill-list.md` 同步；`scan-policy.json` 无需重绑（元习不在扫描例外表内）。

## v0.30.2 (2026-10-12)

- **清单联动（发布期）**：`skills.json` pin `yotta-learn` 0.5.1 → **0.6.0**（desc 同步为知识库口径：跨智能体知识库 + 归位决策树 + 首次激活引导）；`references/skill-list.md` 同步；`scan-policy.json` 无需重绑（元习不在扫描例外表内）。

## v0.30.1 (2026-10-11)

- **面板「高级 CLI」速查说明修复（UX-10）**：速查行此前只按命令后第一段匹配（`hub hosts add` / `hub hosts list` 等全部落回父级 `hub hosts` 条目），导致说明整列重复、`hub config get` 等行说明为空；现在按**最深前缀**解析（容忍旗标 / 参数尾段），每行显示自己条目的说明。
- **解析单一真源化**：新增 `resolveHelpEntry()` + `quickWithMeta()`（`lib/cli-help.js`），`/api/help` 随载荷下发每行的 `meta`，面板直接渲染（移除前端本地解析，终端 / 面板同源）。
- **旗标变体行 per-row note**：`hub hosts` / `hub link` / `hub unlink` / `hub adopt` / `update` / `install` / `view` 等同一命令的多个速查行补齐区分说明，不再出现两行一模一样的解释。
- **门禁**：`test/cli-help-coverage.test.js` 新增「最深条目 + 同组说明不重复 + 服务端 meta 一致性」回归；`tools/check_hub_view.js` 面板走查新增代表性行断言（`hub hosts add` 不得回退到父级说明、`hub config get` 说明非空、`hub hosts` 旗标变体行必须不同）。
- **清单联动（发布期）**：`skills.json` pin `yotta-memory` 0.22.8 → **0.22.9**、`yotta-learn` 0.5.0 → **0.5.1**；`references/skill-list.md` 同步；`scan-policy.json` 按 npm 真包口径重绑（yotta-memory 0.22.9）。

## v0.30.0 (2026-10-11)

- **Hub 清理与配置防呆（UX-02 / UX-04 / OPT-01 / OPT-02）**：`hub unlink` 无 slug 时以文件系统为真源扫描目标目录（台账缺失也能清理指向当前 Hub 的链接；指向其它位置的链接 fail-closed 不动，并给出错位警告 + `hub config get` 自查提示）；dry-run / 执行均输出汇总；空结果不再静默。`hub config clear` 当前配置 Hub 有技能时默认阻断（输出影响面 + 默认位置 + `--move` 替代路径 + `--yes` 显式确认）。
- **一致性检查与列语义（UX-03 / OPT-03）**：`hub doctor` 新增 `hub_mismatch` 检查（宿主链接指向其它 Hub 时告警 + 修复指引）；面板「宿主矩阵 / 链接与体检」把「指向当前 Hub」改为文件系统真源口径，其它 Hub 链接单独计数并警告色标注（配置错位预警）。
- **宿主管理（UX-06 / UX-08 / UX-09）**：新增 `hub hosts rename <目录> --label <名称>` 一步改名（只改显示名，保留目录 / 手动状态 / 覆盖；CLI + 面板 + 审计）；「忽略」统一改名「隐藏标记」（ignored 只影响显示，不拦截行为）；移除注册 / 不接管后提示目录剩余 Hub 链接与 `hub unlink --dir` 清理指引。
- **帮助与提示（UX-05 / UX-07 / OPT-04 / OPT-05）**：面板宿主矩阵新增「术语速查」折叠块 + 关键动作 tooltip；高危命令（unlink / remove / config clear / config rollback / hosts remove / hosts exclude）在 `--help` 与面板高级 CLI 页统一补「影响面 / 替代路径」两行；`hub config get` 检测到运行中 view 面板仍用旧位置时提示重启（view 运行标记 + PID 存活校验）；`hub refresh` 被 scanPolicy 拦截时输出「当前命中 + 与上一已审版本新增 / 消失规则」差异摘要 + `--allow-unverified` 复核指引。
- 面板：清除覆盖确认框显示影响面（技能数 / 原 Hub / 回落默认位置），当前 Hub 有技能时要求输入 `clear` 二次确认。
- 测试：新增 `hub-ux-030`（7 项）与 `hub-view-ux-030`（2 项）；全量 458/458。
- **清单联动（发布期）**：`skills.json` pin `yotta-memory` 0.22.7 → **0.22.8**、`yotta-learn` 0.4.0 → **0.5.0**；`references/skill-list.md` 同步；`scan-policy.json` 按 npm 真包口径重绑。

## v0.29.10 (2026-10-09)

- **清单联动**：`skills.json` pin `yotta-memory` 0.22.6 → **0.22.7**（配置键人话说明：管理台「高级 / CLI」页与官网 /product/ 的 39 个配置键逐键补全说明 + 覆盖回归；无其他行为变更）；`references/skill-list.md` 同步。
- **scan-policy 重绑 yotta-memory 0.22.7（npm 真包口径）**：treeHash 由 `python tools/build_scan_policy.py` 从 npm 发布包重算（非本地候选），与 2026-10-09 行尾口径红线一致。

## v0.29.9 (2026-10-09)

- **scan-policy 重绑 yotta-memory 0.22.6（npm 真包口径）**：treeHash `sha256:efa988a0…`（18 文件 / 1,334,872 B），与 npm 发布包逐字节一致；修复候选与发布包行尾差异导致的哈希绑定不一致。

## v0.29.8 (2026-10-09)

- **图形化面板 CLI 补全**：高级 CLI 页现在渲染全部子命令选项（此前 74 个子命令级选项完全未渲染），选项计数改为完整口径（命令级 + 子命令级 + 全局 = 187），与 `--help` 同源、不漂移。
- 新增 `test/hub-view-cli.test.js` 子命令选项渲染与计数回归。

## v0.29.7 (2026-10-07)

- 清单联动：`skills.json` pin `yotta-memory` 0.22.4 → **0.22.5**（Electron 宿主自启修复：任务 / 兜底 / 定时配置自动注入 ELECTRON_RUN_AS_NODE，不再拉起 GUI）；`references/skill-list.md` 同步；包内 `scan-policy.json` 重绑元忆 0.22.5（treeHash 随候选包重算）。
- 无行为变更（本版仅 pin 与扫描例外表联动）。

## v0.29.6 (2026-10-07)

- 清单联动：`skills.json` 的 yotta-learn pin 0.3.0 → 0.4.0（元习 0.4.0：存储独立与迁移 / MCP stdio / 本地管理台 / 升库路径；legacy 回退写操作 fail-closed）；yotta-memory pin 0.22.3 → 0.22.4（元忆 Windows 自启修复：S4U 主体 + 任务 XML + 去电池 / 72h 限制 + Startup 兜底）；`references/skill-list.md` 同步；包内 `scan-policy.json` 重绑元忆 0.22.4（treeHash 随候选包重算）；无其他行为变更。

## v0.29.5 (2026-10-06)

- **面板迁移向导（S1，缺陷修复）**：面板「设置 Hub 位置」不再只写指针 + 报「已写入配置」；升级为向导 —— 「迁移到新位置」（默认推荐，复用 CLI `--move` 同一内核：复制 → 逐技能校验 → 切配置 → 全宿主重链 → 旧 Hub 入回收站 7 天）/「仅切换位置（保留旧内容）」，迁移中 loading 态、结果真实回显（技能数 / 重链目录数 / 回收站路径；部分失败保留旧 Hub + 重试指引，不报成功）；目标为「空 Hub 台账残留」时提供「清理残留并迁移」；仅切换且旧 Hub 非空 → 二次确认 + 概览横幅「旧 Hub 还有 N 个技能未迁移」+ 一键迁移。
- **最近迁移 + 一键回滚（S2，面板 + CLI 双端）**：`config.json` 新增 `lastMigration`（时间 / from→to / 校验技能数 / 重链目录数 / 回收站与剩余天数）；`hub config get` 展示「最近一次迁移」块与回滚命令；新增 `hub config rollback`（默认预览，`--yes` 执行；反向迁移同内核，`--json`）；面板新增「最近一次迁移」卡片 + 一键回滚。回滚语义 = **位置回退（用当前内容）**，不是恢复旧快照；目标非空 fail-closed 不合并。
- **备份自动清理（S3）**：`hub link --force` / `hub adopt` 替换真目录时，旧副本不再原地留 `<name>.yottaskills-backup-*`（宿主会把备份当技能扫描），统一移入回收站（7 天可恢复）；替换失败自动把旧副本移回原位；`hub link` 输出「替换了 N 份真目录旧副本 + 回收站去向」；`hub doctor` 只读报告 `backup_residue` 警告；新增 `hub cleanup-backups [--yes] [--include-discovered]`（默认预览，清理 `.yottaskills-backup-*` / `.yottaskills-import-*` / `.yottaskills-rollback-*` / `.yottaskills-staging`）。
- **`--dir` 模式修复（S4）**：① 元信自举落点改为运行时缓存（`<记录根>/runtime/verifier`，默认 `~/.yottaskills/runtime/verifier`），不再把 `yotta-verify` + `.yottaskills-staging` 写进目标目录（yottacode skill-inventory 污染修复）；受信记录仍按路径 + SHA-256 校验，目标目录未受信副本一律不用（反劫持模型不变）。② `.yottaskills-staging` 结束（含失败）强制清理 + 启动时清理超过 1 小时的陈旧暂存；扫描 / 注册忽略点目录（不把暂存目录当 slug）。③ `--dir` 托管目录更新保持既有运行时载荷（目标已带 `bin/` 等 → 继续携带，防更新后引擎缺 bin）；新装 / 普通技能目录仍只落本体（§6.3 口径不变）。④ npm / npx 子进程显式继承调用方环境（`YOTTA_SKILLS_REGISTRY_FILE` / `YOTTA_SKILLS_MANIFEST` 等）。
- **面板数据源**：`GET /api/hub/config`（位置 + 最近迁移 + 回滚预览）；概览新增迁移块与未迁移提示；`from` 迁移仅接受面板记录的「未迁移旧 Hub」（不接受任意目录）。
- **修复（自用走查发现）**：回收站目录命名加「目录短哈希」——多个同 basename 的宿主目录（如 `.../skills`）在同一次清理 / 收敛中不再互相撞车（Windows rename EPERM）；回归覆盖收敛与清理两条路径。
- **修复（自用走查发现·二）**：面板「仅切换位置」的结果不再按迁移渲染（此前误显示「校验 0 个技能」）；改为明示「已切换（只改指针，未移动文件）」+ 旧 Hub 未迁移技能数提示。
- 测试：新增 / 扩展 18 项（hub-config 5 + hub-converge 4 + hub-view-config 3 + install-pipeline 3 + self-bootstrap-cache 2 + skills-scan 1）+ 既有自举断言改口径；全量 `npm test` 448/448 连续复跑。

## v0.29.4 (2026-10-05)

- **清单同步**：`skills.json` pin 元习 `0.2.2 → 0.3.0`（元习 0.3.0 知识库批次）；`references/skill-list.md` 同步版本与说明。
- **修复（npm test flake 根因）**：`hub adopt --scan` 对不可读候选目录（坏链 / 扫描途中被删除）不再整体失败 —— 新增 `safeHashTree` 守卫，跳过该候选并在输出中列出「跳过」清单；回归覆盖坏链候选与有效候选共存场景。
- **测试隔离**：测试进程 preload `test/setup-env.js`，清除指向真实宿主根的环境变量（DSH / Codex / XDG / OpenClaw / Claude 等）—— 此前 `hub config --move` 与 host-scope 类用例会把 junction 写进真实宿主技能目录、用例清理后留下坏链（flake 根因）。

## v0.29.3 (2026-10-05)

- **修复（发布缺陷）**：0.29.2 的 npm / GitHub 包内 `scan-policy.json` 未随本批重绑（仍绑元忆 0.22.2，treeHash `7b2cd7a2…`），导致安装元忆 0.22.3 时 scanPolicy 复核 `version-mismatch` → DO NOT INSTALL（可 `--skip-scan` 临时绕过）。本版将包内 policy 重绑为元忆 0.22.3（treeHash `4f499e0d…`）；其余功能与 0.29.2 一致。
- **修复（同类第二处）**：`install-self` 运行件载荷补上 `scan-policy.json`（此前独立安装的引擎缺该文件 → scanPolicy 复核 `policy-unavailable` → 安装元忆等自指技能被误阻断）；`test/self-install.test.js` 补断言。
- **护栏（防复发）**：`tools/pack_candidate.py` 打包 yotta-skills 候选时自动校验包内 `package/scan-policy.json`（version vs skills.json pins + 例外 vs SCAN_SPECS + treeHash vs handoff lock），不一致即 FAIL（exit 4）；新增 `tools/check_scan_policy.py --policy/--tarball` 与回归 `tools/test_check_scan_policy.py`；发布规范 §19.4 增补红线。

## v0.29.2 (2026-10-05)

- **U4 Hub 位置持久化**：新增 `<YOTTA_SKILLS_HOME>/config.json`（schema v1，原子写）与 `hub config get / set --hub <path> [--move] / clear`；解析优先级 `--hub` > `YOTTA_SKILLS_HUB` > config > 默认 `~/.yottaskills/hub`；`where` 与面板「Hub 位置」显示来源与配置覆盖。
- **`--move` 迁移（fail-closed）**：复制旧 Hub → 逐技能 treeHash 校验 → 切换配置 → `hub link` 以新 Hub 为源 `--force` 重链 → 旧 Hub 入回收站（7 天）；校验失败不切配置、不删旧 Hub；重链未完成保留旧 Hub 供重试。
- **误用防护**：`--hub` 只允许与 `hub` / `view` / `where` 一起使用；裸 `yotta-skills --hub X` 或 `install --hub` 现在 fail-closed（此前会落入 install 并静默忽略 `--hub`）。
- **`hub refresh` scanPolicy 复核**：refresh / adopt 复用安装管线同款 scanPolicy 例外复核（version + treeHash 绑定，fail-closed）；元忆自指扫描不再需要 `--skip-scan` 绕过。
- **面板**：概览「Hub 位置」区新增来源 / 配置覆盖 / 重启提示与「设置新位置 / 清除覆盖」（页面令牌 + `hub-config` 确认串；不热切换，重启 `view` 生效）。
- 测试：新增 hub-config 6 + hub-migrate 3 + refresh scanPolicy 2 + 面板 2。

## v0.29.1 (2026-10-05)

- **update「只升不降」**（U1）：`update` / `update --check` / `update --auto` / `hub update` 四路径统一语义 —— 本地版本高于目标（清单 pin / npm latest）时保留不降级：`update` / `hub update` 跳过并标注「本地领先」，`--check` 单列 `localAhead` 且不计更新（退出码 0），`--auto` 不动作；`--force` / `rollback` 保留显式降级通道；`latest` / range 模式在解析出精确版本后、任何写入之前复判。
- **宿主矩阵与范围修正**（U2）：已安装标记区只显示未配对标记（CLI / 面板单一真源）；`installed` 配对确定性优选（用户注册 / 已核实映射 > env > 未核实映射 > 自动发现，消除 last-write-wins）；未核实映射显示「映射·未核实」而非「自动发现」；新增「不接管」开关（`hub hosts exclude/include`，发现 / 显示 / 链接三层跳过，含 `--include-discovered`）；新增目录覆盖（`hub hosts set <agentId> --dir` / `--clear`）；面板新增「不接管 / 恢复接管 / 编辑目录 / 标记可用 / 忽略」动作；**YottaCode 不纳入接管**（映射 / `YOTTACODE_HOME` / 扫描 / 注册 / 标记全部排除）。
- **Hub 审计补全**（U3）：`hub install` / `hub update` 成功、失败各写一条 Hub 审计（slug / 版本 / 来源 / verdict / via / ok；skip 与 dry-run 不写），面板「最近动作」可见。
- **元忆联动**：清单 pin 元忆 0.22.2（插件载荷修复同步升版）；scanPolicy 按新 treeHash 重绑。

## v0.29.0 (2026-10-04)

- **D1 修复：`hub install / update --dry-run` 真正只读**。此前该命令会真实联网安装特殊家族并写 Hub 台账；现 dryRun 透传到安装管线 —— 预览不发网络请求、不写任何文件（含台账），`--json` 输出机器可读 plan（install / update / skip + installedVersion + latest 标记「预览不解析」）；隔离回归证明 treeHash / mtime / 台账逐字节不变、npm 零调用。
- **F1 安装面：`install-self` + `where`**。保留 `install --agent/--dir` 兼容直装；新增元阁独立安装（默认 `~/.yottaskills/yotta-skills`，`--dir` 指定，`YOTTA_SKILLS_HOME` 覆盖根；写 `self.json` 登记；不写宿主配置、不建全局 shim；fail-closed：Hub 真源重叠 / 桥接目录 / 非空陌生目录拒绝，`--force` 才覆盖同名运行件）；新增 `where` 查看运行中 CLI / 独立安装目录（标记当前运行项）/ Hub 真源；README / SKILL / CLI help 首选流程统一为 Hub 四步（hosts → install → link → view）。
- **F2 自定义宿主注册**：`hub hosts add/remove/list/mark` —— 注册进发现 / 分发 / 收编范围（`hosts.json` schema v1，realpath 去重；只注册不建目录、移除注册不删目录）；Hub / 桥接 / 不存在 / 重复 / 非法 label fail-closed；Hub 审计 hosts.add / hosts.remove / hosts.mark；面板「宿主矩阵 → 添加自定义目录 / 移除注册」。
- **F3 宿主状态细分与残留清理**：目录证据与实体证据分开（应用标记 / 用户注册 / 手动标记），状态 = 可用 / 残留（实体未确认）/ 未创建 / 仅标记（+ 手动 ignored）；`hub hosts --state` 过滤、`hub doctor` 新增 `host_state` 只读检查；`hub hosts remove <dir> --purge` 清理残留（默认预览，`--yes` 执行；只删指向 Hub 的链接，非 Hub 链接 / 非技能内容随目录保留在回收站 7 天）；面板宿主矩阵统计 / 筛选 / 状态徽章 / 清理与移除动作（手输确认串 + 页面令牌）。
- **面板 API**：`/api/hosts` 增加状态计数；新增 `/api/hosts/add`、`/api/hosts/remove`、`/api/hosts/purge` 与只读 `/api/hosts/purge-plan`。
- **测试**：新增 dry-run 4 + 安装管线 2 + install-self 5 + host-state 3 + 注册表 5 + 残留清理 3 + 面板 2；provider 测试夹具并发加固；全量测试 385/385（原 361）。

## v0.28.3 (2026-10-03)

- **新增 `hub remove <slug>`**：一条命令完成「全宿主清链接（含死链）→ Hub 目录入回收站（保留 7 天，跨卷复制 + 校验）→ 清 Hub / 链接台账（不调 `syncHubState`，防记回 missing）→ 写审计」；fail-closed：只删指向 Hub 的链接与 Hub 内目录，真副本 / 外部链接保留并报告；链接清理报错即中止、不删 Hub；默认范围 = 已核实宿主 ∪ 本技能链接台账；`--agent/--dir` 收窄仅用于死链清理；退出码 0 / 1 / 2 / 4。
- **面板新增「删除技能」动作**：概览 Hub 内容行 → 影响预览（将清理 / 保留逐条列出）→ 手输 slug 二次确认 → 与 CLI 同内核、同台账、同审计；面板写 token 与串行写队列不变。
- **全量 CLI 单一真源**：新增 `lib/cli-help.js`（35 个命令 / 子命令 + 46 个选项，全部人话）；面板「高级 CLI」页改为 `/api/help` 渲染（全量速查 + 完整参数），`--help` 由同一模型渲染；`tools/export_cli_help.js` 提供结构化导出与 `--check` 覆盖门禁。
- **指定智能体分发**：`hub link <slug> --agent <id>` / `hub unlink <slug> --agent <id>` 纳入全量 CLI 页与单测（只影响该宿主，Hub 真源保留）。
- **清单联动**：`yotta-memory` pin 0.22.0 → 0.22.1（管理台 CLI 页速查层全量 33 命令 / 31 子命令）；scanPolicy 按 0.22.1 候选重绑 treeHash。
- 测试：`npm test`（新增 hub-remove 14 项 + CLI 覆盖 4 项 + 面板帮助 / 删除 2 项）；面板 `tools/check_hub_view.js` 1440 / 390 两档（含全量 CLI 与删除预览）。

## v0.28.2 (2026-10-03)

- **面板加载态**：技能枢纽面板（`yotta-skills view`）切视图 / 点刷新时显示「正在加载 <视图>…」提示（带转圈动画，刷新按钮同步禁用），数据到达后自动消失；修复宿主矩阵 / 收编向导等慢视图先显示空表、无加载提示的体感问题。
- **清单 pin 更新**：`yotta-memory` 0.21.1 → 0.22.0（记忆管理台新增「高级 / CLI」页：高频命令速查 + 只读完整帮助，`HELP_MODEL` 单一真源）。
- **scanPolicy 重绑**：`yotta-memory` 例外表按 0.22.0 候选 tarball 重算 treeHash（fail-closed 语义不变：版本或内容变化即旧例外失效）。

## v0.28.1 (2026-10-03)

- **修复：桥接目录的 `unlink` 清理被误拦**。0.28.0 的 `--dir` 桥接守卫同时拦住了 `hub unlink --dir`，导致历史误链（如 `XDG_STATE_HOME/skills` 的 145 条）无法用 CLI 清理；现仅 `hub link --dir` 拒绝桥接目录（永不作为链接目标），`hub unlink --dir <目录>` 恢复为显式清理路径（fail-closed：仍只删指向 Hub 的链接）。
- **修复：Hub 真源保留运行时载荷（OpenCode 契约）**。特殊家族收敛为 Hub 链接后，OpenCode 的 `yotta-skills` 缺 `bin/`（安装管线顶层跳过），违反 handoff `keepExtra` 硬约束；现在 Hub 安装 / 更新（`hubScope`）按清单声明的 `runtimePayload` 保留顶层载荷（元忆 `bin`、元阁 `bin`），链接宿主直接获得，`sync_opencode_runtime --check` 通过；普通宿主安装仍为薄片（跳过 bin）。
- **回归测试**：新增「桥接目录 `unlink --dir` 允许清理」+「hubScope 安装保留 runtimePayload」用例；全量测试 341/341。

## v0.28.0 (2026-10-03)

- **宿主目录核实与链接范围收口**：`hub hosts` 把发现的目录分为三类 —— **已核实（verified）/ 自动发现（discovered）/ 桥接（bridge）**；`hub link --all` / `hub unlink --all` 默认范围只含已核实宿主，自动发现目录需 `--include-discovered` 显式纳入；`XDG_STATE_HOME/skills`（官方 skills CLI 锁目录）与 `XDG_DATA_HOME/skills`（数据桥接）永不作为链接目标（`--dir` 指向也会被拒绝，面板同样 fail-closed）。
- **映射修正（逐智能体核实）**：新增 `replit`（公开宿主表 `configHome/agents/skills`）与 `mimocode`（官方 MiMoCode 布局 + 本机自证）；`universal` 补 XDG 变体；`goose` 由 XDG 解析修正为本机真实目录字面 `~/.config/goose`；`crush` / `kimchi` 由 XDG 误解析改回公开宿主表字面 `~/.config`；XDG 解析收敛为显式集合（仅 `.config/agents`、`.config/devin`、`.config/opencode` 三类 rel）；`yottacode` / `box` 标记未核实、默认不链。
- **realpath 去重**：`hub link` / `unlink` 的目标目录按 realpath 去重，junction / symlink 双路径不再重复建链；`hub hosts` 停止扫描 `XDG_STATE_HOME` / `XDG_DATA_HOME` 根。
- **doctor 链接范围检查（只读）**：新增 `link_scope:*`，报告位于默认范围之外的已建链接并给出 `hub unlink --dir <目录>` 清理提示。
- **面板**：宿主矩阵新增「范围」列（已核实 / 自动发现 / 桥接·不链），链接与体检页对桥接目录隐藏链接入口、对自动发现目录显示范围徽章；CLI 速查补 `--include-discovered`。
- **文档**：`references/hub.md` 补「链接范围（0.28.0 起）」与发现口径；`SKILL.md` / help 同步。
- **测试**：新增 `test/agent-dirs-scope.test.js`（5 项）+ `test/hub-scope.test.js`（4 项）；全量 339/339。

## v0.27.1 (2026-10-03)

- **跨卷收敛修复**：`hub link` 收敛旧副本时，`rename` 在跨盘场景（源目录位于其它卷，或经 junction / symlink 落在其它卷）会报 `EXDEV: cross-device link not permitted`；现回退为「复制到回收站 → 校验（treeHash + 文件数 + 字节数）→ 删除源目录」，任一步失败都保持失败自动恢复语义（源完整则回滚副本；源已不完整则保留完整副本并输出路径）；链接条目按「重建链接 → 校验目标 → 删除原链接」处理；链接输出对跨卷复制的份数给出说明。
- **家族分支 `--force` 生效（WorkBuddy 验收 D1）**：家族技能的目标条目为指向 Hub 之外的链接时，显式 `--force` 现在会替换为 Hub 链接（仅移除链接本身、不碰目标目录；dry-run 报 `would-replace`）；无 `--force` 仍默认跳过；`--force` 不越过版本闸门等既有 fail-safe。
- **回归测试**：新增 EXDEV 注入回归（跨卷收敛成功 / 建链失败后跨卷恢复 / 非 EXDEV 错误不回退）+ `--force` 家族替换回归（force 替换 / 无 force 保持跳过 / force 收敛 + 替换 / force 不越版本闸门），全量测试 330/330。

## v0.27.0 (2026-10-03)

- **元技能唯一性收敛（hub link 执行时）**：家族技能在链接时收集宿主中的同名真目录与 `yotta-X__*` 重命名副本（frontmatter `name` 相同），版本闸门 Hub ≥ 宿主后把旧副本移入 `~/.yottaskills/trash/<时间戳>/<宿主>/<技能>/`（保留 7 天、输出恢复路径）再建立指向 Hub 的链接；宿主版本高于 Hub / 版本无法解析时跳过并提示；先移后链，建链失败自动尝试恢复；外部技能同名冲突仍默认跳过，不自动删、不自动更新。
- **Hub 家族范围扩到 32**：特殊家族 5 个（元开 `yotta-dev-mcp` / 元伴 `yotta-partner` / 元呈 `yotta-present` / 元阁本体 `yotta-skills` / 元信MCP `yotta-verify-mcp`）纳入 Hub 安装 / 更新 / 收敛 / 体检范围，版本跟随各自 npm `latest`（内置拉包通道支持 `dist-tags.latest` 解析）；一次性安装清单 27 语义不变。
- **非元技能口径**：更新只管元技能；外部技能来源多样（不一定从 npm 安装），不参与 `hub update`、不改源文件，用户自行处理（`hub refresh --from` 仍为显式手动路径）。
- **doctor 单一真源检查（只读）**：新增 `single_source:*` 检查，报告宿主中的同名多份副本与版本参差（高于 Hub 提示先更新 Hub、低于 Hub 提示链接时收敛）；只报告不修改，错误级语义不变。
- **面板与输出**：`view` 链接预览新增「将收敛」区块（数量 + 明细 + 回收站说明），执行链接按同一收敛语义落盘并在 toast 显示收敛数量；`hub adopt --apply` 输出明示范围与目标 Hub，`--skip-scan` 显式提示；非元技能 adopt 扫描对严格 YAML 风险（前导逗号 / 未加引号的 `: ` 值）做只读告警，不影响使用不处理。
- **文档**：`references/hub.md` 补收敛语义 / 回收站 / 非元技能更新口径 / adopt 范围警示；`SKILL.md` 与 help 同步。
- **测试**：新增 `test/hub-converge.test.js` 11 项（收敛 / 版本闸门 / dry-run / 已链接副本收敛 / 失败恢复 / 回收站清理 / 家族范围 / latest 解析 / doctor 单一真源 / 严格 YAML 告警 / adopt 告警）；全量 323/323。

## v0.26.0 (2026-10-02)

- 新增本机技能枢纽面板 `yotta-skills view`（默认 `127.0.0.1:8789`，`--port` 可改，仅本机监听）：六视图（概览 / 宿主矩阵 / 收编向导 / 链接与体检 / 记录与回滚 / 路由与编排）+ 高级 CLI 页；全部包装既有 Hub / 快照 / 证据 / 路由 lib，不建平行状态。
- 面板动作边界：收编 / 链接 / 解除 / 回滚可执行（预览 → 确认 → 执行 → 证据）；install / update / refresh 只给复制命令；收编逐项运行元信扫描，high / critical 阻断，面板不提供跳过 / 降级（`--skip-scan` / `--allow-unverified` 仍只在 CLI 显式使用）。
- 安全壳：Host / Origin / Sec-Fetch-Site 校验、严格 CSP / no-store / noindex、写操作会话令牌、256KB 请求体上限、写操作串行、破坏性确认串；零远程资源、零遥测，不读元忆、不改宿主配置。
- 新增 `lib/hub-view-server.js`（HTTP 服务与 API）与 `lib/hub-scan.js`（CLI / 面板共用元信扫描发现；CLI 同名逻辑改为委托，行为不变）；`assets/view.html` 为前端单一真源，`tools/sync_hub_view_html.py` 嵌入 CLI 并提供 `--check` 漂移门禁（已接入 `preflight-publish.py`）；`tools/check_hub_view.js` 做 1440 / 390 浏览器验收。
- 快照回读增强（additive）：`validateSnapshot` / `listSnapshots` 输出 `source` / `createdAt`，供面板回滚定位来源目录；CLI 原字段不变。
- 断链修复：Hub 真源删除后遗留的 junction / symlink 现在会被识别为 `broken`（读取链接值判定是否指向 Hub），`hub unlink` 可 fail-closed 清理；此前面向断链的 `unlink` 会因目标不可解析被误拒。
- 测试：`test/hub-view-server.test.js` 17/17、`test/hub-view-cli.test.js` 2/2、`test/hub-view-embedding.test.js` 3/3；全量 312/312。

## v0.25.1 (2026-10-02)

- 家族清单同步：元质 `yotta-code-quality` 0.4.3（分发副本 frontmatter `description` 单引号标量修复，严格 YAML 解析器不再跳过）。

## v0.25.0 (2026-10-02)

- 新增本机技能 Hub（标准 `yotta-skills-hub/v1`）：`hub hosts` 只读发现本机宿主与技能目录（文件系统优先，不读元忆 / 注册表）；`hub install` / `hub update` 把技能装到 `~/.yottaskills/hub` 单点真源；`hub adopt --scan|--apply` 收编各宿主现有技能（默认复制保真 + 原目录保留）；`hub refresh <slug> --from <path>` 手动同步非元阁来源技能；`hub link --all` 用 Windows junction / POSIX symlink 分发到全部已发现宿主；`hub unlink` fail-closed 只删链接；`hub status` 显示来源、版本、链接与异常；`hub doctor` 检查断链 / 目标缺失 / slug 不一致 / 目录权限。
- 宿主发现复用公开宿主表（兼容 Vercel Labs `skills` CLI / SkillCat 的目录映射，当前 79 条），支持 `CODEX_HOME` / `XDG_CONFIG_HOME` / `DSH_HOME` / `OPENCLAW_STATE_DIR` / `CLAUDE_CONFIG_DIR` 等环境变量覆盖，并过滤临时目录、`.bak`、candidate / staging、插件构建目录等噪声。
- 只读桥接 Vercel Labs `skills` CLI 的 `.skill-lock.json` v3（`$XDG_STATE_HOME/skills/` 或 `~/.agents/`）；元阁不重写官方锁文件，只在 Hub 台账中合并来源信息。
- 兼容矩阵实测：官方 `skills@1.7.0` 在临时假 home 中 8/8 宿主透过 Windows junction 读取同一技能；元阁 `hub hosts` 本机识别 31 个技能目录 / 44 个已装应用标记。证据：`docs\元阁-Hub-宿主兼容矩阵-2026-10-02.md`。
- WorkBuddy 复验修复：`hub doctor` 对「Hub 目录存在但零技能」判为 error 并提示先 `hub install` / `hub adopt --apply`；`hub link` / `hub unlink` 补齐 `--json` 结构化输出，不再静默退化为文本。
- 新增 `lib/agent-dirs.js` / `lib/agent-discovery.js` / `lib/hub.js` / `lib/hub-adopt.js` / `lib/skills-cli-lock.js` 与 `test/hub.test.js`；全量测试 289/289。

## v0.24.2 (2026-10-02)

- 家族清单同步：元忆 `0.21.1`（管理台归属 AI 平铺选择 + 记忆详情抽屉遮罩层级修复）。
- scanPolicy 重绑：元忆 0.21.1 的已审查例外按新 treeHash 绑定。

## v0.24.1 (2026-10-02)

- 家族清单同步：元忆 `0.21.0`（记忆管理台 M1：真实读写 / 权限矩阵 / 归档与回收区撤销）。
- scanPolicy 重绑：元忆 0.21.0 的已审查例外按新 treeHash 绑定（skill + version + treeHash + 规则 + 路径，fail-closed）。

## v0.24.0 (2026-10-02)

- 接管能力补缺口（A 无 npm 拉包 / B 依赖人话提示 / C 范围控制 / D 行为回归）：
- A 内置拉包 / 解包：新增 `lib/registry-fetch.js`（Node 内置 https 直连 registry：abbreviated packument + 版本解析 + tarball 下载 + `integrity`(sha512) / `shasum`(sha1) fail-closed 校验 + `HTTPS_PROXY` / `HTTP_PROXY` CONNECT 隧道）与 `lib/untar.js`（zlib + ustar / pax / GNU 长名解析；路径越界与链接条目 fail-closed）；默认内置为主，npm 与系统 tar 仅作回退通道，`YOTTA_SKILLS_FETCH` / `YOTTA_SKILLS_EXTRACT` 可强制单通道；安装证据新增 `fetch_channel` / `extract_channel`。
- B 依赖统一提示：新增 `lib/deps.js` 人话模板（需要什么 / 为什么 / 一条修复命令 / 不影响使用），接入拉包失败、缺 Python、双通道解包失败与 Node 版本检查；`doctor` 新增 `dependencies` 自检块（text + `--json`，只告警不失败）；顺手修 `--python` 旗标在扫描路径被忽略。
- C 范围控制：`skills.json` 每条技能新增 `domain`（对齐家族索引 9 类），`references/skill-list.md` 同步补列；新增 `--only` / `--domain` 与 `update --installed-only`。接管语义：只维护目标目录已安装的家族技能，`skills.json` 只作身份 / 版本参照；未装不动作、不新增、不报错；已管理且已最新跳过（退出码 0）；无旗标时 install / update 语义不变。
- D 回归与文档：新增 `test/update-scope.test.js` / `domain-filter.test.js` / `fetch-builtin.test.js` / `deps-message.test.js` / `python-flag.test.js`（含 PATH 隔离的 Node-only 端到端）；`references/install-flow.md` 补双通道流程、依赖矩阵与范围语义矩阵；`SKILL.md` / README 中英同步。

## v0.23.3 (2026-10-01)

- 安装器卫生批次：`install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单）；`skills.json` 清单 pin 同步 27 项。

## v0.23.2 (2026-10-01)

- 修复家族安装管线嵌套载荷丢失：复制原语的顶层跳过名单（`package.json` / `bin` / `node_modules` / `.git`）此前按条目名逐层生效，会把技能包内嵌套的同名载荷（如元造 `template/package.json`、`template/bin/install.js`）一并跳过——家族安装 / 更新元造后，其脚手架自检会失败（缺必需文件）。现改为仅顶层生效，与元造 0.1.3 的安装器修复对齐。
- 新增 `lib/copy-tree.js`（单一复制原语）与回归测试：顶层同名跳过、嵌套同名保留、缓存类（`__pycache__` / `.pytest_cache` / `.mypy_cache` / `*.pyc` / `*.pyo`）任意层级清理；家族管线集成回归同步补齐。
- 清单同步：`skills.json` / `references/skill-list.md` 更新元造 0.1.4、元案 0.1.1。

## v0.23.1 (2026-10-01)

- 文档：环境变量表补齐 `YOTTA_SKILLS_REGISTRY_FILE` / `YOTTA_SKILLS_USAGE_FILE` / `YOTTA_PROVIDER_HOME` 三项，并新增「隔离环境：三个状态文件成组导出」小节（bash / PowerShell 示例）——测试、CI 与多 agent 场景需三件成组导出，避免读写宿主真实状态。
- 行为零变更：安装 / 更新 / 路由 / hook / MCP 契约不变。

## v0.23.0 (2026-10-01)

- O1 动态路由 MVP：`--route` / MCP `route_request` 在静态 playbook 之上，可选调用本地 provider（capability `o1.route`）做确定性组合排序；新增 `confidence` / `reasons` / `summary` / `alternatives` 输出。
- 开源侧新增 `lib/route-features.js`（请求特征 + 已装技能元数据 + 聚合使用信号 + 公开 playbook 元数据）与 `lib/route-dynamic.js`（白名单 / 枚举 / 限长校验）；静态技能始终保留，provider 不能删除静态技能或改变 `missing_skills` 语义。
- `usage` 默认关闭；仅显式启用后向本地 provider 发送聚合计数（used / named / accepted / route_hits / distinct_pairs / last_signal_at），不发送需求原文、记忆正文、路径或身份信息；provider 审计仍只记元数据。
- 非元阁家族技能仍只作候选并标注 `scan_required`；不自动安装、不自动调用。
- 评分算法位于本地私有目录 `license/o1/`，不进任何发布件；未配置 / 未授权 / 超时 / 非法输出时回落静态路由，退出码保持 0。
- 元忆 0.20.0 不变；安装 / 更新 / hook / scanPolicy 契约零变更。

## v0.22.2 (2026-09-30)

- 修复 `doctor --dir` 指向单个技能包目录时的 UX：现在会按 `SKILL.md` / `skill-manifest.json` / 目录名自动识别技能身份，不再误报「目标目录下没有可检查的元阁家族技能」。
- 修复 doctor 退出码语义：没有可检查对象返回 `4`，检查失败仍返回 `1`，manifest / 身份校验失败仍返回 `6`，便于只读调用方区分「没目标」与「检查失败」。
- 新增单技能目录、显式 `--slug` 单技能目录、空目录退出码三组 CLI 回归。

## v0.22.1 (2026-09-30)

- 清单同步：元忆 pin 0.19.0 → 0.20.0，承接上下文分页 (`context.paging`) 与 `memory.hook` PREF 驱逐修复。
- scanPolicy 随元忆 0.20.0 treeHash 重绑；其余安装 / 路由 / hook / DSH 适配行为不变。

## v0.22.0 (2026-09-30)
- 关联 Agent Plugin 包新增 DeepSeek Harness（DSH）profile bundle 适配层：插件仓根 `package.json` 增加 `dsh.bundle.patch`，并由构建器生成 `cordis.patch.yml`。
- DSH 安装后同时注册包内 `yotta-skills` 技能与 `mcp__yotta-skills__*` 工具；复用包内 stdio MCP server，不新增运行时依赖。
- Agent Plugins 1.0 安装方式与 CLI / MCP 工具行为保持不变；本版为插件分发形态升级。

## v0.21.0 (2026-09-30)
- 新增 M1 记忆裁决器开源调用口：`yotta-skills decide-memory` 与 MCP `decide_memory`，调用本地扩展提供方 `m1.adjudicate`，输出每个技能的 `promote / hold / demote` 只读建议、分数与信号明细。
- 新增本地使用记录：`usage status|enable|disable|mark|reset`；默认关闭，`usage enable` 后 `--route` 才记录结构化 route_hits 与组合对，显式 `usage mark` 记录 used / named / accepted。记录只含 slug、时间、信号类型、playbook / confidence 与组合对，不含需求原文、记忆正文、路径或身份信息。
- `decide-memory` 默认只读；`--dry-run` 显式只读；`--promote` 只写 `~/.yottaskills/memory-adjudication.json` 建议文件，生成私密 `PREF` 记忆候选，不自动写元忆、不删除任何内容。`--explain` 输出每个信号的得分明细。
- provider 子进程环境透传授权库相关变量（`YOTTA_LICENSE_HOME` / `YOTTA_LICENSE_KEYS_DIR` / `YOTTA_LICENSE_BASE_URL` / `YOTTA_LICENSE_SERVER_ID`），私有 M1 provider 可用 `LicenseGate.assertCan('m1.adjudicate')` 做授权门；未授权 / 超时 / 非法输出一律 fail-open，退出码保持 0。
- 评分算法位于本地私有目录 `license/m1/`，不进任何发布件；开源侧只做特征快照、白名单校验与展示。协议见 `references/provider-protocol.md`。
- 元忆 0.19.0 不变；静态 playbook / 安装 / hook / scanPolicy 契约零变更。

## v0.20.2 (2026-09-29)
- 家族安装的 npm 拉包新增镜像回退：默认源返回 404（国内镜像未同步该版本 tarball）时自动改用官方源 `https://registry.npmjs.org/` 重试一次；安装输出显示回退行，安装证据新增 `npm_registry_fallback` 字段。
- 两次都失败时给出可直接复制的修复提示（`npm_config_registry` / `YOTTA_SKILLS_NPM_FLAGS`）；已显式指定 registry 或设置 `YOTTA_SKILLS_NO_FALLBACK=1` 时不回退。
- 非 404 错误（网络超时等）不触发回退，保持原失败信息。
- 静态 playbook / 路由 / hook / scanPolicy 契约零变更。

## v0.20.1 (2026-09-29)
- 家族安装接入 scanPolicy 例外复核：元信判 `DO NOT INSTALL` 时，按包内 `scan-policy.json` 的已审查例外（逐条绑定技能 + 版本 + treeHash + 规则 + 路径）复核，豁免检测规则表 / 攻防样例 / 文档说明类命中；复核后无阻断级发现则继续安装。
- 修复元忆 / 元察 / 元鉴从元阁安装时被元信自指误报阻断的问题（检测类技能自带规则表字面量）；例外表与 handoff / OpenCode 的 scanPolicy 同源，由 `tools/build_scan_policy.py` 生成。
- 技能升版或内容变化后旧例外自动失效（treeHash 绑定，fail-closed），安装回到元信原始判定。
- 安装日志新增 `scan_policy` 字段（是否应用 / 豁免条数 / version / treeHash）。
- 元信扫描输出解析失败（空输出 / 截断 / 子进程抖动）自动重试一次；仍失败时报错带退出码与 stderr 摘要。
- 静态 playbook / 路由 / hook 契约零变更。

## v0.20.0 (2026-09-28)
- 新增 `o1.route` 动态扩展口：`--route` / MCP `route_request` 可选调用用户配置的本地扩展提供方（provider），在已装注册表白名单内增补 / 重排路由结果。
- 静态 playbook 结果先算必算；未配置或未授权 / 超时 / 非法输出时一律回落静态结果，文本输出与历史一致，`--json` 增加 `dynamic` 状态块。
- 清单同步：元忆 pin 0.19.0。
- 协议与配置见 `references/provider-protocol.md`。

## v0.19.28 (2026-09-28)

清单同步元盾 `0.1.7`（代码围栏占位符修复 20 处 / 非法转义告警与致命异常退出码 fail-open 修复 / 彩色输出路径在真人终端崩溃修复 / 新增宿主接入说明）。
版本五件对齐 0.19.28；安装器 / 路由 / hook 契约零变更。

## v0.19.27 (2026-09-27)

清单同步元安 `0.3.0`（新增教育版学生数据隐私扫描：`--target edu` + 15 条规则 + 固定脱敏报告）。
版本五件对齐 0.19.27；安装器 / 路由 / hook 契约零变更。

## v0.19.26 (2026-09-27)

清单同步元忆 `0.18.1`（蒸馏分类型提取 + 行号溯源 + 实测质量指标；`consolidate` 相对日期绝对化 + 归档巩固标记；`maintain --rules` 只读规则晋升建议；记忆守则新增权威顺序与写入纪律）。
版本五件对齐 0.19.26；安装器 / 路由 / hook 契约零变更。

## v0.19.25 (2026-09-26)

清单同步元忆 `0.18.0`（命中打点与容量水位 / `consolidate` 提案闸门 / `doctor` 规模分级 / `context --audit` 上下文压缩审计；`archive --dry-run` 真只读 + MCP 只读面）。
版本五件对齐 0.19.25；安装器 / 路由 / hook 契约零变更。

## v0.19.24 (2026-09-26)

清单同步元忆 `0.17.4`（新增 `rename` 改名命令，用于消除平铺 / 分层同序号冲突）。
版本五件对齐 0.19.24；安装器 / 路由 / hook 契约零变更。

## v0.19.23 (2026-09-26)

清单同步元忆 `0.17.3`（顶层帮助去掉逐项重复的「做什么：」前缀，仅文案变化）。
版本五件对齐 0.19.23；安装器 / 路由 / hook 契约零变更。

## v0.19.22 (2026-09-25)

口径修正：安装 / 更新权限边界写清楚（ClawHub LLM 复核）。

- SKILL.md 新增权限边界：`install` / `update` 属有副作用操作，执行前先用 `--dry-run` 展示目标目录与技能清单、由用户确认；批量安装不是一次性授权，新增目标目录要重新确认；不静默写宿主配置、不自动安装缺失技能、不 `-g` 污染全局。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除；批量安装（`-g`）必须显式加 `--yes`。
- 元忆清单一并同步 0.17.2。

**清单同步：元忆 0.17.1**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.17.0 → 0.17.1，承接「view 删除 AI 身份时输入错误 ID 无提示」修复。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / 引擎 VERSION / MCP VERSION / CHANGELOG = 0.19.21。

## v0.19.21 (2026-09-25)

## v0.19.20 (2026-09-25)

**清单同步：元忆 0.17.0 + 信任层四件 + 元公 0.1.2**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.16.7 → 0.17.0；清单更新日期 → 2026-09-25。
- 补记信任层四件（元规 0.1.0 / 元镜 0.1.0 / 元案 0.1.0 / 元题 0.1.0）与元公 0.1.2，人工可读清单从 22 技能补齐到 27 技能，并补「合规与信任」「教育与学习」两个家族分区。
- 修正 `skill-list.md` 与 `skills.json` 的技能集合 / 版本一致性回归；`--list`、install、install 幂等、update 的测试计数改为读取清单长度，后续新增技能不再硬编码数量。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / 引擎 VERSION / MCP VERSION / CHANGELOG = 0.19.20。

## v0.19.19 (2026-09-23)

**清单同步：元忆 0.16.7（迁移口令安全 + view 根指纹）**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.16.6 → 0.16.7。
- 同步元忆迁移文档的编码安全修正，以及 `view` 端口复用前的 memory_home 指纹校验。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / 引擎 VERSION / CHANGELOG = 0.19.19。

## v0.19.18 (2026-09-23)

**插件载荷完整性修复：lib/ + skills.json**

- `tools/build_standalone_plugins.py` 的 `PAYLOAD_DIRS` 补 `lib`，插件载荷含元阁 12 个运行时模块；新增 `PAYLOAD_EXTRA_FILES` 把 `skills.json` 带入载荷。
- 修复插件内 `reindex` / `route_request` 报 `Cannot find module '../lib/install-evidence'` 与清单读取失败。
- 新增回归 `tools/test_plugin_payload_runtime.py`：构建后插件载荷必须跑通 reindex + route_request。
- 清单同步元忆 0.16.6；版本对齐 package.json / SKILL.md frontmatter / skill-manifest.json / 引擎 VERSION / CHANGELOG = 0.19.18。

## v0.19.17 (2026-09-22)

**清单同步：元忆 0.16.5（doctor JSON 稳定契约）**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.16.4 → 0.16.5。
- 同步 `doctor --json` 顶层 `schemaVersion` / `encryption` / `migration_required` 契约，确保全家安装取得正确版本。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / 引擎 VERSION / CHANGELOG = 0.19.17。

## v0.19.16 (2026-09-22)

**清单同步：元忆 0.16.4（agent-key 提示范围修复）**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.16.3 → 0.16.4，清单更新日期 → 2026-09-22。
- 同步元忆缺 `--agent-key-file` 的提示范围修复，确保全家安装按清单取得正确版本。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / 引擎 VERSION / CHANGELOG = 0.19.16。

## v0.19.15 (2026-09-22)

**清单同步：元忆 0.16.3（迁移授权最短路径）**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.16.2 → 0.16.3，`updated` → 2026-09-22。
- 同步内容：明文库迁移最短命令、`view` / `key bind` 授权等价口径、CLI 帮助与技能文档统一。
- 安装器 / 路由 / hook 契约零变更；本版仅为清单与版本同步。

## v0.19.14 (2026-09-21)

**清单同步：元忆 0.16.2（首启修复）**

- `skills.json` / `references/skill-list.md` 的 yotta-memory 版本 0.16.1 → 0.16.2，`updated` → 2026-09-21。
- 同步内容：元忆 0.16.2 首启修复——空加密库 `view` 恢复钥匙解锁、非 TTY `--password-stdin`、`--recovery-key-out`、缺 `agent-key` 降级未授权、空明文 `migrate`、doctor 分档与 `view` 端口健康检查。
- 安装器 / 路由 / hook 契约零变更；本版仅为清单与版本同步。

## v0.19.13 (2026-09-19)

**安全修复：校验器（元信）发现改为「受信安装记录 + 身份 + 摘要」三重绑定。**

- 背景（平台扫描发现，T07 工具劫持）：旧实现通过本地技能注册表里 `slug=yotta-verify` 的
  `source_dirs` 发现扫描引擎，而注册表身份来自被扫描技能自己 `SKILL.md` frontmatter 的 `name`。
  任意目录只要自称 `yotta-verify` 并提供 `scripts/yotta_verify.py`，就会被当作引擎执行——
  既可直接执行任意代码，也能伪造 `SAFE TO INSTALL` 放行后续安装。
- 修复：
  - 新增 `lib/trusted-verifier.js`：受信记录 `~/.yottaskills/trusted-verifier.json`
    （与注册表同目录，支持 `YOTTA_SKILLS_REGISTRY_FILE` 多 agent 隔离），只在安装管线
    校验通过、元信安装 / 更新成功后写入。
  - `findVerifier` 只认两类来源：用户显式指定（`--verify` / `YOTTA_SKILLS_VERIFY`）与
    受信记录；候选须通过「路径 realpath 无符号链接跳转 + 包身份（slug / package / trust /
    SKILL.md 与 manifest 版本一致）+ 引擎 SHA-256 与记录一致」。
  - 任一环节不满足即 fail-closed：不再回退到注册表 / 目标目录里的同名引擎，改走自举安装
    （从 npm 重装一份干净的元信，装完立即写记录）。
  - 自举安装后新增身份 / 摘要复核，未通过不返回引擎。
- 测试：新增 `test/trusted-verifier.test.js` 8 项（含 T07 回归、摘要不符、身份不符、版本不符、
  裸引擎不被采用、记录读写往返）；测试夹具 `test/helpers/fake-npm.js` 按真实元信包形态
  生成 manifest；`node --test "test/*.test.js"` 180/180。
- 清单同步：`skills.json` 元信 0.3.1 → 0.3.2（`references/skill-list.md` 同步）。

## v0.19.12 (2026-09-19)

同步家族维护批次清单版本：元安全 0.2.6 / 元盾 0.1.4 / 元察 0.2.9 / 元析 0.1.7 / 元安 0.2.4 / 元审 0.2.5。

## v0.19.11 (2026-09-19)

**OpenClaw / QClaw 目录识别 + 清单同步**

- `--inventory` / `--reindex` 等盘点能力新增识别 OpenClaw / QClaw 技能目录（`~/.openclaw/skills`，支持 `OPENCLAW_STATE_DIR` 覆盖）——QClaw 基于 OpenClaw，同一目录下的技能现在可被盘点、去重与路由覆盖；新增 `test/skills-scan.test.js` 用例。
- 清单同步：`skills.json` 与 `references/skill-list.md` 更新元真 `0.2.1`（位置参数修复）与元忆 `0.16.1`（维护性重发）。

## v0.19.10 (2026-09-19)

**台账口径维护**

- `references/skill-list.md` 元忆行由 `0.15.0` 更正为 `0.16.0`，清单更新日期改为 `2026-09-19`；`skills.json` 为机器权威源，`test/skill-list.test.js` 强制两者一致。
- 更正 v0.19.7 条目表述：元伴 `yotta-partner` 不在全家清单内（`skills.json` 与 `skill-list.md` 均未收录该技能，元伴通过自带安装器单独安装）。
- 本次只维护清单口径与文档表述，不改变安装器、路由、hook 契约与清单技能集合（仍为 22 项）。

## v0.19.9 (2026-09-18)

- 同步元链 `0.1.4` 到 skills.json / skill-list：新增 `scannedFiles` 扫描输入证据，统一 stdout / stderr UTF-8。
- 不改变安装器、路由与 hook 契约。

## v0.19.8 (2026-09-17)

- 同步 O6 候选清单：元链 0.1.3 / 元守 0.4.2 / 元引 0.2.2 / 元习 0.2.1 / 元测 0.3.1 / 元鉴 0.1.3。
- 不改变安装器、路由与 hook 契约；版本四件与 OpenCode 锁文件统一更新。

## v0.19.7 (2026-09-17)

**MCP registry 按 agent 隔离**

- 新增 `YOTTA_SKILLS_REGISTRY_FILE`：CLI 与 MCP 统一读取该环境变量，允许为不同 agent 指定独立 `registry.json`；未设置时保持 `~/.yottaskills/registry.json`。
- MCP `list_installed_skills` / `reindex` 返回实际注册表路径，便于宿主核对隔离位置。
- OpenCode 锁文件将配置 `<dataDir>/yottaskills/<agentId>/registry.json`，避免多 agent 共用同一注册表。
- `install.sh --dir` 改为只安装技能本体与 MCP / 清单资产，清理旧的 `.github`、`bin`、`lib`、`test`、`package.json` 等开发文件；新增自用安装回归。
- 同步清单中的元质 `0.4.1`、元伴 `0.2.1`、元引 `0.2.1` 与元忆 `0.15.0` 候选版本。
- 本里程碑只隔离 registry；安装快照、安装证据、更新缓存和 hook 绑定仍保持现有用户级位置。

## v0.19.6 (2026-09-16)

- 清单同步：yotta-memory 0.13.2（调用者认证 / agent_key 绑定安全修复）。
- 更新 `skills.json` / `references/skill-list.md` 的元忆版本与 updated 日期。
- 安装器版本四件对齐 0.19.6；本次不改变安装 / 路由算法。

## v0.19.5 (2026-09-15)

**多源技能盘点版本修复**：

- 同名技能多副本扫描新增 `variants` 明细，代表版本取合法版本中的最高 semver；版本差异持久化为 `conflicts`，不再由首个来源副本决定显示版本。
- `--inventory` / `--route` 显示代表版本与多副本摘要；`doctor` 优先按目标目录匹配精确副本版本，旧注册表缺少 `variants` 时回退聚合版本。
- 回归覆盖多副本 semver 选择、注册表幂等、CLI 文本/JSON 与 doctor 精确匹配；`npm test` 168/168。

## v0.19.4 (2026-09-14)

**元造 0.1.2 清单同步**：

- `skills.json` / `references/skill-list.md` 将 `yotta-skill-creator` 版本
  从 0.1.1 同步到 0.1.2，清单更新日期同步为 2026-09-14。
- 本次为清单同步版本，安装器、路由与 hook 逻辑无行为变更。

## v0.19.3 (2026-09-13)

**自装契约修复 + 扫描误报消除**：

- `skill-manifest.json` 的 `before_install` 声明由 `install_gate` 改为 `scan_skill`，与安装管线实际提供的检查项对齐；此前自装会被自己的 hook 判为 missing → block（只能 `--skip-scan` 绕过）。
- `permissions.note` 调整措辞，避免同时出现「下载 / 执行」触发元信 PIJ-020 误报（high）。
- 新增 `test/self-install-contract.test.js`：锁定「声明 = 管线检查项」「扫描通过放行 / 失败阻断」「note 不触发 PIJ-020」三条契约。

## v0.19.2 (2026-09-13)

**授权边界整改（平台安全评估反馈）**：

- SKILL.md「使用须知」由「首次使用必须写入宿主全局记忆」改为**可选步骤 + 显式确认**：写入前展示目标文件、完整文本与后果，用户拒绝则不写任何文件并保持 CLI 用法。
- 删除常驻授权表述：可选注入文本不再要求每个会话无条件重扫或代用户安装、调用其他技能；组合建议统一改为「先建议、经用户确认后安装与调用」。
- MCP 配置写入改为显式确认后落盘；用户拒绝或无法改配置时继续 CLI 降级。
- 安装版本策略默认改为 `--pin`（清单精确版本，可复现）；`--range` 为显式可选项，不再默认跟随浮动 patch。
- 同步 SKILL.md / README 中英 / FAQ / 教程 / 编排表 / install-flow / MCP server 说明；新增文档授权边界回归测试。

## v0.19.1 (2026-09-13)

- 文档去本机硬编码：Codex 永久记忆写入位置从本机绝对路径改为 `$CODEX_HOME/AGENTS.md`（未设置时 `~/.codex/AGENTS.md`）。
- 清理测试夹具中的本机路径；新增发布前机器路径硬编码扫描闸门后，此类问题不允许再进入发布件。

## v0.19.0 (2026-09-13)

**元守家族分类假阳性修复**：

- 元守 0.4.1 内置分类副本补入 `yotta-skills` 非安全家族排除，消除元阁 Defense Triple 假阳性。
- `skills.json` / `references/skill-list.md` 同步 yotta-publish-guard 0.4.1。

## v0.18.0 (2026-09-13)

**Advisory 仓库文档 hygiene 清理**：

- 元察 0.2.8 / 元析 0.1.6 / 元安 0.2.3 / 元造 0.1.1 / 元鉴 0.1.2 清理历史公开文档中的内部表述。
- 五个技能 preflight、validate、测试与 pack 全部通过。
- `skills.json` / `references/skill-list.md` 同步五个版本。

## v0.17.0 (2026-09-13)

**P0-6 全家族铺开覆盖验收**：

- 新增 26 技能 manifest 覆盖测试：全部技能必须能解析包内 manifest 或家族默认契约。
- 强制 8 技能必须提供包内 manifest 和 hook 声明；补齐 `yotta-verify-mcp` 与 `yotta-skills` 两个缺口。
- 版本与发布件同步 0.17.0。

## v0.16.0 (2026-09-13)

**P0-4.6 元忆 after_milestone 试点**：

- 元忆 manifest 声明 `after_milestone` / `remember_commit` / `fallback: explicit-unverified`。
- 元阁真实 manifest 回归验证：有记忆文件证据时 allow/verified；缺证据或写入失败时 `explicit-unverified` + 一次纠偏。
- `skills.json` / `references/skill-list.md` 同步 yotta-memory 0.13.0。

## v0.15.0 (2026-09-13)

**P0-4.5 元守 before_publish 试点**：

- 元守 manifest 声明 `before_publish` / `publish_gate` / `fallback: wrapper`。
- 元阁真实 manifest 回归验证：wrapper 已注册且门禁失败时 block；wrapper 未注册时 `explicit-unverified`。
- `skills.json` / `references/skill-list.md` 同步 yotta-publish-guard 0.4.0。

## v0.14.0 (2026-09-13)

**P0-4.4 元序 before_start / after_milestone 试点**：

- 元序 manifest 声明 `before_start` / `read_state` 与 `after_milestone` / `write_state`。
- 元阁真实 manifest 回归验证：有状态文件证据时 allow；缺证据或落盘失败时 `explicit-unverified` + 一次纠偏。
- `skills.json` / `references/skill-list.md` 同步 yotta-workflow 0.4.1。

## v0.13.0 (2026-09-13)

**P0-4.3 元盾 before_tool 试点**：

- 元盾 manifest 声明 `before_tool` / `guard_check` / `fallback: explicit-unverified`。
- 元阁真实 manifest 回归验证 Codex `native-audit` 只输出纠偏与 `unverified`，不宣称动作前硬拦截。
- `skills.json` / `references/skill-list.md` 同步 yotta-guardian 0.1.3。

## v0.12.0 (2026-09-13)

**P0-4.1 元信 before_install 试点**：

- 安装管线接入统一 hook 适配器：包内 `before_install` 声明在落位前评估，manifest 声明 `on_fail: block` 时扫描失败会阻断并保留旧版本。
- 适配器证据写入 `~/.yottaskills/hook-log.jsonl`；`--skip-scan` 仍走人工应急路径，标记 `explicit-unverified`，不会被误报为已验证。
- `skills.json` / `references/skill-list.md` 同步 yotta-verify 0.3.0。
- 新增安装管线 hook 阻断回归；真实 yotta-verify manifest 随 0.3.0 发布。

## v0.11.0 (2026-09-13)

**P0-3 运行时 hook 适配层**：

- 新增 `lib/hook-adapter.js`：六个统一事件、Codex 四档能力矩阵、manifest hook 声明校验、四档决策聚合和 `explicit-unverified` 降级。
- 新增 `hook capabilities / evaluate / bind / unbind` CLI：可查看宿主能力、评估事件、写入结构化证据、幂等注册与反注册声明。
- 证据写入 `~/.yottaskills/hook-log.jsonl`；绑定注册表写入 `~/.yottaskills/hook-bindings.json`，不直接改写宿主配置。
- `native-audit` 不宣称强制；失败时输出 `explicit-unverified` 与纠偏信号。未核验宿主一律 `unsupported`。
- 新增 `test/hook-adapter.test.js` 与 `test/hook-cli.test.js`；全量测试 131/131。
- 本版只交付适配器内核，具体技能接入留待 P0-4 试点。

## v0.10.0 (2026-09-13)

**更新检查缓存与后台周检**：

- 新增 `update --check --scheduled`：默认 7 天加 0 到 24 小时随机抖动，未到期不联网；到期只检查一次并把结果写入 `~/.yottaskills/update-check.json`。
- 后台周检网络失败时文本模式静默、退出码 0；`--json` 保留 `error` / `cache` 诊断字段，不把后台调度失败变成用户噪音。
- 手动 `update --check` 保持每次联网和 0 / 3 / 1 退出码；检查结果同样写入本地缓存，避免手动检查后立即重复周检。
- `update --auto` 继续复用完整安装管线，`--skip-scan` 不能绕过元信门禁；`DO NOT INSTALL` 阻断、保留旧版本并写入证据。
- SKILL / README / FAQ / 教程 / 走查同步：移除“会话开工默认联网检查”，明确手动检查与后台周检边界。
- 新增 `lib/update-check.js`、`test/update-check-state.test.js`，并扩展 scheduled / auto 门禁回归。

## v0.9.0 (2026-09-13)

**doctor / rollback 与自定义生命周期**：

- 新增 `doctor`：只读检查技能目录、`SKILL.md`、版本、manifest 身份、注册表一致性和自定义 doctor 脚本；支持 `--json`。
- 新增 `rollback`：列出并校验快照，恢复最近一次安装或更新；恢复前后都保留快照与安装证据。
- 安装管线接入包内 `setup` / `doctor` / `rollback` 生命周期脚本；setup 或 doctor 失败时自动恢复旧版本，脚本路径只能指向包内相对路径。
- 新快照写入 SHA-256 元数据；旧快照仍可按结构校验和恢复。
- `--slug` 用于 doctor / rollback 定向处理单个技能。
- 新增生命周期、doctor、快照完整性与 CLI 回归测试。

## v0.8.0 (2026-09-12)

**P0-2.1 安装编排与元信自举**：

- 安装链路读取包内 `skill-manifest.json`，缺失时使用 `skills.json` 家族默认契约。
- 元信缺失时自动自举，随后对所有家族包执行装前扫描。
- `DO NOT INSTALL` 和扫描失败阻断安装；`CAUTION` / `REVIEW` 继续但显示风险。
- 安装改为快照、暂存、原子切换，失败不删除旧版本。
- 新增 `~/.yottaskills/install-log.jsonl` 安装证据。
- `--skip-scan` 仅保留为人工应急路径，并记录 `explicit-unverified`。

## v0.7.2 (2026-09-10)

skills.json 清单同步（元序路径模型澄清升版后，元阁安装清单随包更新）：

- yotta-workflow 0.3.0 → 0.4.0。
- skills.json 与 references/skill-list.md 同步，updated → 2026-09-10。
- 版本四件对齐 0.7.2；无功能代码变更。

## v0.7.1 (2026-09-09)

skills.json 清单同步（评测批 2 六技能升版后，元阁安装清单随包更新）：

- yotta-learn 0.1.4 → 0.2.0；yotta-humanize 0.1.3 → 0.2.0；
  yotta-security-testing 0.2.4 → 0.3.0；yotta-publish-guard 0.2.1 → 0.3.0；
  yotta-intel 0.1.1 → 0.2.0；yotta-secret 0.1.2 → 0.2.0。
- skills.json 与 references/skill-list.md 全量同步，updated → 2026-09-09。
- 版本四件对齐 0.7.1；无功能代码变更。

## v0.7.0 (2026-09-08)

**评测驱动完善**：新增 FAQ 与复杂场景走查；同步 22 技能清单并新增清单一致性测试，防止人工文档版本漂移；CLI 增加统一异常提示。

- 新增 references/faq.md 与 references/walkthroughs.md。
- skills.json 与 references/skill-list.md 全量同步，新增 test/skill-list.test.js 强制版本一致。
- CLI 增加顶层异常提示与修复建议。

## v0.6.2 (2026-09-06)

**更新检查 / 自动更新（`update --check` / `update --auto`）**：元阁 CLI 新增联网只读检查本地已装技能是否有更新（对 npm `dist-tags.latest`，版本源唯一），
按本地 `SKILL.md` 版本对比，无论技能源自哪个安装渠道（npm / git clone / 本地拷贝等）都兼容。`--check` 只读列清单，退出码 0=全部最新 / 3=有更新 / 1=查失败；
`--auto` 检测到家族（`yotta-*` / 清单内）可更新时走安装管线（含元信装前安全扫描）自动更新，非元阁家族（非 yotta-*）技能绝不自动更新。
新增 `--registry <url>` 自定义版本源；网络异常优雅降级（不阻塞会话）。SKILL.md「使用须知」注入文本同步加入「会话开工跑 `update --check`」规则。（v0.19.2 起：该规则已从注入文本移除，改为用户确认后的可选说明。）
测试：新增 update-check / update-auto 本地 HTTP registry 离线用例，npm test 47/47。
## v0.6.1 (2026-09-06)

**skills.json 全量清单对齐（22 技能 vs npm latest 全一致）**：yotta-memory 0.10.1 → 0.11.0（MCP 协议对齐批次发布后同步，元阁 install 按清单版本拉包，不同步会装到旧版）；源清单 + 构建副本双份同步；其余 21 技能核对无滞后。无功能代码变更。

## v0.6.0 (2026-09-06)

**MCP 协议对齐最新版 2026-07-28（无状态时代）**：yotta-skills MCP 升级 dual-era——modern 直连（server/discover 免握手、逐请求 _meta 版本声明、resultType、-32022）服务新客户端；legacy（initialize 握手，protocolVersion 2025-11-25）兼容旧客户端，旧形状响应零惊扰。SKILL 标注「基于 MCP 最新协议 2026-07-28（向后兼容 2025-11-25 及更早握手）」。npm test 42/42（含 modern MCP e2e）。

## v0.5.1 (2026-09-06)

skills.json 三处滞后同步修复（yotta-skills 0.5.0→0.5.1）：元真 0.1.2→0.1.3 / 元忆 0.8.5→0.10.1 / 元守 0.1.1→0.2.1 + updated 改期 2026-09-06 + yotta-skills 四件对齐 0.5.1 + 技能分发清单副本 + 插件同步。

## v0.5.0 (2026-08-31)

方案 A（其他已装技能候选编排）：路由输出从「只编排元阁组合」扩展为「组合 + 并列候选提示」。

- 新增 `--route` / `route_request` 输出「其他已装技能候选」：注册表中非元阁家族的已装技能，按 frontmatter `description` 与需求文本做本地机械匹配（英文词项 + 中文二字组交集），Top N（默认 3）并列展示，标注来源、得分、命中词项与扫描状态。
- 安全边界：只读 frontmatter `description` 做机械匹配，不读取全文指令、不做语义推理、不自动调用；候选默认标注「未扫描」，使用/安装前需先做装前安全扫描；数据不出本机。
- 确定性：同输入同输出，无状态、无个人数据；候选不参与组合融合排序，7 个静态组合输出保持不变。
- CLI 文本输出追加「其他已装技能候选」段；`--json` 追加 `other_skill_candidates` / `other_skills_note` 字段；MCP `route_request` 同步。
- 测试：路由核心新增候选匹配 / 元技能排除 / Top N 与排序 / 确定性 / 空结果；CLI JSON 与文本输出用例。
- 版本升至 0.5.0。

## v0.4.0 (2026-08-31)

阶段 C（O1 静态编排 playbook + 路由指引）：从「知道装了什么」升级为「给出该用哪几个、什么顺序」。

- 新增静态编排 playbook（7 个场景组合）：输出呈现、长生命周期、交付质量门、装前安全门、造技能发版、安全事件响应、入口安装。
- 新增 CLI `--route "<需求摘要>"`：先更新本地注册表，再输出候选组合、调用顺序、技能角色、置信度、命中依据、已装/缺失状态、安装命令与应用模式提醒；支持 `--json`。
- 新增 MCP `route_request` 工具，与 CLI 复用同一套路由核心；MCP 工具扩展为四个。
- 缺失技能只建议安装，不自动安装；安装命令需用户确认并先执行装前安全扫描。应用模式默认显式调用，切换为按场景自动调用需用户确认。
- 文档：SKILL.md / README 中英 / orchestration.md / tutorial.md 同步「编排路由」层与边界；banner 同步升级为编排层定位。
- 测试：新增路由核心（playbook 完整性 / 命中顺序 / 缺失建议 / 无匹配兜底 / 应用模式）、CLI JSON 与文本输出、MCP e2e 用例。
- 版本升至 0.4.0。

## v0.3.0 (2026-08-31)

阶段 B（D2 re-index 自动钩子）：新装技能自动被发现。

- 新增 CLI `--reindex`：重扫所有技能目录并增量合并注册表，变化聚焦输出（文本 / `--json` 机器可读），供钩子与手动调用；`--rescan` 为同义别名。
- 装技能后自动 re-index：`install` / `update` 完成后自动重扫注册表，把本次落位结果反映进 `~/.yottaskills/registry.json`（新增 / 更新 / 消失随输出列出）；`--no-reindex` 可关闭。
- 会话开工 re-scan：SKILL.md「使用须知」护栏补「会话开工先跑一次 `yotta-skills --reindex`」；注册表 `note` 口径同步 `--inventory / --reindex`。（v0.19.2 起：该常驻要求已移除，改为可选提示。）
- MCP `reindex` 工具改走 `--reindex --json`（同一套扫描核心）；CLI 等价命令注明。
- 文档：SKILL.md / README 中英 / references/install-flow.md / tutorial.md 同步 re-index 用法。
- 测试：新增 `--reindex`（含幂等）与装后自动 re-index（含 `--no-reindex` 关闭）用例；全量用例全绿。
- 版本升至 0.3.0。

## v0.2.1 (2026-08-31)

MCP 配置说明补全（按需加载口径）。

- SKILL.md「技能盘点」节补「MCP：按需加载（可选）」：明确本技能与 MCP 均为按需触发、不走常驻；mcpServers 配置 JSON 示例、配置步骤（用后可移除）、重启/重载提示、未加载降级 CLI 兜底；frontmatter description 同步按需加载口径。（v0.19.2 起：写入客户端配置前必须先获得用户明确同意。）
- 测试：mcp-e2e serverInfo.version 断言改为动态读 package.json；python 探测加候选兜底（YOTTA_TEST_PYTHON / python / python3 / Scoop python38），Windows 无需手动设环境变量。
- 版本升至 0.2.1。

## v0.2.0 (2026-08-31)

技能生态盘点层（阶段 A）：元阁从「编排策划 + 安装器」升级为「编排策划 + 安装器 + 技能盘点」。

- 新增 lib/skills-scan.js：技能扫描核心（零依赖 Node.js 18+）——frontmatter 解析（含 YAML block scalar）、多根目录扫描、同名技能去重合并来源、注册表增量合并（新增/更新/消失，幂等）、原子写 ~/.yottaskills/registry.json。
- 新增 CLI --inventory：盘点本机已装技能（文本表格 / --json 机器可读；--dir 追加目录；--project 附扫项目级目录），自包含输出不依赖任何元技能。
- 新增 MCP scripts/yotta-skills-mcp.py：stdio JSON-RPC（零依赖），list_installed_skills / describe_skill / reindex 三工具，按需加载。
- SKILL.md / README 中英同步「技能盘点」层与用法；frontmatter 触发语加「盘点技能 / 查看已装技能」。
- 测试：skills-scan 7 + cli-inventory 2 + mcp-e2e 2（共 23 用例全绿）。
- 版本升至 0.2.0。

## v0.1.3 (2026-08-31)

编排策划层升级：元阁从「一键安装器」升级为「总编排策划 + 一键安装器」两层。

- SKILL.md 重写：新增「使用须知」节——提供「元阁编排策划」护栏文本，供用户确认后写入客户端全局记忆；新增「编排策划」节（7 组组合矩阵 + 场景映射 + 组合建议规则）；frontmatter description 同步「总编排策划 + 一键安装器」定位与触发语。（v0.19.2 起：写入改为可选步骤 + 显式确认，并移除常驻授权表述。）
- 新增 references/orchestration.md：编排策划决策表（技能家族全景 / 组合矩阵 / 场景映射 / 自动安装规则）。
- skills.json 清单版本同步（2026-08-30：yotta-memory 0.8.5 / yotta-security-audit 0.2.2 / yotta-vetter 0.2.3 / yotta-security-testing 0.2.4 等六处）。
- README 中英版定位同步「编排策划 + 一键安装」两层。
- 测试：pin 断言同步至 yotta-memory 0.8.5。
- 版本同步升至 0.1.3。

## v0.1.2 (2026-08-29)

安装方法清晰化：install.sh 用途与 README 中英「安装」章节对齐。

- 修正 install.sh 头部注释：明确其只把「元阁安装器技能」本身装进智能体/目录（自带 SKILL.md，
  让代理能调用元阁），并提示装齐 22 个 yotta-* 技能需再跑 `node bin/yotta-skills.js install`；
  避免用户误以为 `bash install.sh` 一次就装齐全家。
- 版本同步升至 0.1.2。

## v0.1.1 (2026-08-29)

文档修正：明确「元阁是全家安装器、与单个技能安装不同」。

- 更正 README 中英版「安装」章节：先分清「拿到安装器」与「装齐全家」两层（元阁本身不内置 22 个技能本体）；方式二 git clone / 方式三 Download ZIP 示例由 `--list` 改为 `install --dir <目标目录>`；方式四 install.sh 说明「只把安装器技能本身装进智能体目录」，装齐 22 个技能仍需再跑一次 `install`。
- 澄清：`--list` 只查看清单、不安装；克隆 / 解压只拿到安装器，不含任何技能本体。
- SKILL.md 增补「与单个技能安装不同」说明；版本同步升至 0.1.1。


## v0.1.0 (2026-08-29)

初始发布：

- 定位：元阁 —— 全家技能一键安装 CLI（「分发与安装」家族，市场主线 M2「全渠道分发」第一步，
  降低「n 个技能逐个装」门槛）。
- CLI（bin/yotta-skills.js，零依赖 Node.js 18+）：
  - `--list` 列出全家技能 + 版本 + 说明（可按技能名过滤）；
  - `install --agent <name>` / `install --dir <path>` 装全家或指定技能；
  - `update` 增量更新（补齐缺失 / 升级版本不一致）；
  - `--dry-run` 预览不联网不改动；`--pin` 锁死清单精确版本；
  - `--force` / `--skip-scan` / `--npm` / `--python` / `--verify` 等选项。
- 清单：skills.json 收录 22 个已发布技能（登记表为权威源，2026-08-29 校准；
  元安全 / 元测 / 元造 / 元守 / 元察 / 元情 / 元钥 / 元链 / 元鉴 等补入）。
- 机制：逐技能 `npm pack` → 系统 tar 解压 → 元信装前摘要（若可用，仅提示不拦截）→
  落位 `<dest>/<slug>` → 汇总报告（✔ 成功 / - 跳过 / ✘ 失败，有失败项退出码 1）。
- 幂等：目标 `<slug>/SKILL.md` frontmatter version 与清单一致即跳过；`update` 只补缺失 /
  版本不一致。
- 版本策略：默认 range（`major.x` 取同 major 最新 patch）；`--pin` 锁死可复现。
- 支持智能体：内置 17 个键名（claude / cursor / codex / gemini / goose / amp / opencode /
  windsurf / workbuddy / kiro / trae / trae-cn / qwen / comate / codebuddy / kimi / agents）；
  未收录用 `--dir` 指目录。
- Windows npm 解析：定位 npm.cmd 同目录 npm-cli.js 用 node 直跑（规避 EINVAL / cmd 引号坑）。
- 测试：12 用例全绿（--list / 临时目录安装断言 / 幂等 / --pin / update / 异常路径 /
  元信 scan 集成）+ 全家族联网实测 22/22 安装成功、版本全对齐、幂等复跑 22 跳过。
- 文档：SKILL.md（中立版）+ references 三件（skill-list 全家清单 / install-flow 内部机制 /
  tutorial 中文教程）+ README 中英双版。
- 发布件：LICENSE（MIT）/ NOTICE / banner（1280×640）/ install.sh。
