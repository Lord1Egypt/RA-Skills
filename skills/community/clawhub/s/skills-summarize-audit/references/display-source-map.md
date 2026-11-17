# Agent 展示文案来源地图

当前 v9.2 工作流只生成中文候选，不修改用户技能、系统项、staging、cache 或 runtime。
下文带日期的应用/重建记录是历史取证，不能用作当前修改命令或通用跨客户端结论。
路径先从实际 CODEX_HOME、安装登记与用户输入解析；本机绝对路径仅示例，不硬编码到其他用户环境。

审计“命令栏/输入框”和“侧边栏”时，先区分**展示位置**与**本地元数据来源**。只有标记为 `observed` 的映射才能作为精炼候选来源；客户端 UI 未直接验证时不得声称修改某文件即可改变该 UI。

## Codex（本机已验证）

| 展示对象 | 首选来源 | 回退来源 | 审计分类 | 可写性 |
|---|---|---|---|---|
| 技能命令栏名称 | `<skill>/agents/openai.yaml` → `interface.display_name` | `SKILL.md` frontmatter `name` | `codex_global_skill` / `codex_system_skill` | 用户 skill 根目录（通常 `~/.agents/skills`）可写；`CODEX_HOME/skills/.system` 只读 |
| 技能侧边栏短说明 | `<skill>/agents/openai.yaml` → `interface.short_description` | `SKILL.md` frontmatter `description` | 同上 | 同上；只改 `short_description`，不改 ID/名称 |
| 插件卡片/侧边栏名称与说明 | `<plugin>/.codex-plugin/plugin.json` → `interface.displayName` / `shortDescription` / `longDescription` | manifest `name` / `description` | `codex_plugin_manifest` | 只读 cache |
| 已安装插件技能 | `<plugin>/skills/<skill>/agents/openai.yaml` | 对应 `SKILL.md` | `codex_plugin_cache` / `codex_runtime_plugin` | 只读 cache/runtime |
| 插件暂存技能 | `CODEX_HOME/.tmp/bundled-marketplaces/**/SKILL.md` | 对应 `agents/openai.yaml` | `codex_plugin_staging` | 只读；与 cache 同 ID 时必须报告冲突 |
| 市场可发现技能 | `$CODEX_HOME/cache/remote_plugin_catalog/*.json` → `plugins[].release.skills[].interface` | catalog skill `description` | `remote_plugin_catalog` | 只读；`catalog_only`，不计入已安装统计 |

本机验证样本：`D:\codex\plugins\cache\openai-curated-remote\openai-templates\0.1.0\skills\artifact-template-minimal-letterhead\agents\openai.yaml` 与其上级 `.codex-plugin\plugin.json`。

### Codex 全路径矩阵（翻译与回测入口）

| 来源层 | 必查路径 | 主要字段 | 状态/写入规则 |
|---|---|---|---|
| CODEX_HOME 用户技能 | `D:\codex\skills\<skill>\agents\openai.yaml` | `interface.display_name`, `interface.short_description` | 非 `.system` 通常可写；必须保留 ID/名称 |
| `.agents` 用户技能 | `C:\Users\Administrator\.agents\skills\<skill>\agents\openai.yaml` | 同上 | 用户技能可写；同时回读 `SKILL.md` frontmatter |
| Codex 系统技能 | `D:\codex\skills\.system\<skill>\agents\openai.yaml` | `interface.short_description` | 系统更新可能覆盖；本地修改须标记覆盖风险 |
| 用户/项目 staging | `<project>\.agents\skills\...`、`<project>\.zcode\skills\...` | `SKILL.md` frontmatter | 仅在对应客户端可见证据下处理，不跨客户端推断 |
| bundled cache | `D:\codex\plugins\cache\openai-bundled\<plugin>\<version>\skills\<skill>\` | `agents/openai.yaml` 优先，`SKILL.md` 回退 | cache 只读/可被重建 |
| bundled staging | `D:\codex\.tmp\bundled-marketplaces\openai-bundled\plugins\<plugin>\skills\<skill>\` | 同上 | 本地重建来源；应用中文候选时需与 cache 一起回读 |
| curated remote cache | `D:\codex\plugins\cache\openai-curated-remote\<plugin>\<version>\skills\<skill>\` | `agents/openai.yaml` 优先，`SKILL.md` 回退 | `cache_only` 时提示上游覆盖 |
| curated remote staging | `D:\codex\.tmp\plugins\plugins\<plugin>\skills\<skill>\` | 同上 | 插件更新/刷新可能重新生成 cache |
| 插件级展示 | `D:\codex\plugins\cache\<channel>\<plugin>\<version>\.codex-plugin\plugin.json` | `interface.displayName`, `shortDescription`, `longDescription` | 只读 manifest；不修改功能或 ID |
| runtime 技能 | `C:\Users\Administrator\.cache\codex-runtimes\...\skills\<skill>\` | YAML 优先，frontmatter 回退 | 运行时刷新覆盖；只记录候选 |
| 远程市场目录 | `D:\codex\cache\remote_plugin_catalog\*.json` | `plugins[].release.skills[].interface` | 发现源，不计入已安装，不作为 UI 证据 |
| 安装回执 | `D:\codex\plugins\cache\<channel>\<plugin>\.codex-remote-plugin-install.json` | plugin ID/版本回执 | 用于确认安装状态，不是展示文案来源 |
| 生效配置 | `D:\codex\config.toml`、`codex doctor --json` loaded config path | 插件启用项、真实配置入口 | 先读 `doctor`，不能凭目录存在判断启用 |
| 变更快照 | `D:\codex\backups\audit-translation-*` | 文件副本、SHA256 | 写入前创建；失败按快照人工回滚 |

### 命令栏窗口来源快照（2026-07-25，observed）

本次用户提供的命令栏截图已与本地文件逐项对照。后续同类英文回退问题，先按以下路径回读，不必重复索要截图来定位来源：

| 命令栏项类型 | 当前实际来源 | 回读字段 | 持久化边界 |
|---|---|---|---|
| 用户全局技能 | `D:\codex\skills\<skill>\agents\openai.yaml`；少数技能位于 `C:\Users\Administrator\.agents\skills\<skill>\agents\openai.yaml` | `interface.short_description` / `short_description` | `editable=true`，可在明确授权后修改 |
| 系统技能 | `D:\codex\skills\.system\<skill>\agents\openai.yaml` | `interface.short_description` | 只读，由 Codex 更新覆盖 |
| bundled 插件子技能 | `D:\codex\plugins\cache\openai-bundled\<plugin>\<version>\skills\<skill>\agents\openai.yaml`；不存在时回退同目录 `SKILL.md` frontmatter `description` | `short_description` 或 `description` | `editable=false`，cache/staging 更新会覆盖 |
| curated remote 插件子技能 | `D:\codex\plugins\cache\openai-curated-remote\<plugin>\<version>\skills\<skill>\agents\openai.yaml`；不存在时回退 `SKILL.md` | 同上 | `editable=false`，只能生成候选 |
| 插件级命令/卡片 | `D:\codex\plugins\cache\<channel>\<plugin>\<version>\.codex-plugin\plugin.json` | `interface.shortDescription` / `longDescription` | `editable=false`，上游或插件更新控制 |
| runtime 技能 | `C:\Users\Administrator\.cache\codex-runtimes\...\skills\<skill>\agents\openai.yaml`；不存在时回退 `SKILL.md` | 同上 | `editable=false`，运行时刷新覆盖 |

已核实的英文来源实例：

- `Browser`：`D:\codex\plugins\cache\openai-bundled\browser\26.721.31836\.codex-plugin\plugin.json` 与 `skills\control-in-app-browser\SKILL.md`。
- `Computer Use`：`D:\codex\plugins\cache\openai-bundled\computer-use\26.721.31836\.codex-plugin\plugin.json`。
- `Visualize`：`D:\codex\plugins\cache\openai-bundled\visualize\1.0.15\.codex-plugin\plugin.json`。
- `Figma:*`：`D:\codex\plugins\cache\openai-curated-remote\figma\2.0.16\skills\<skill>\SKILL.md`。
- `GitHub`：`D:\codex\plugins\cache\openai-curated-remote\github\0.1.8-2841cf9749ae\skills\<skill>\agents\openai.yaml` 与对应 `SKILL.md`。
- 模板技能：`D:\codex\plugins\cache\openai-curated-remote\openai-templates\0.1.0\skills\artifact-template-*\agents\openai.yaml`。

处理顺序：先读取当前 config/安装回执确认版本，再按上述路径回读真实字段；只有可见集合变化、来源无法映射或需要最终 UI 验收时，才要求用户补充截图。路径快照是来源线索，不替代 UI 可见性证据。

### 应用模式与英文回退记录（2026-07-25，observed）

- 插件本地 staging 可能位于 `D:\codex\.tmp\plugins\plugins\<plugin>` 或 `D:\codex\.tmp\bundled-marketplaces\openai-bundled\plugins\<plugin>`；应用中文候选后必须清理对应活动 cache，避免旧 metadata 继续显示。
- Figma 曾在清理活动 cache 后由 `D:\codex\.tmp\plugins\plugins\figma` 自动重建到 `D:\codex\plugins\cache\openai-curated-remote\figma\2.0.16`；因此只删除 cache 不能完成卸载或持久翻译。
- `openai-templates` 当前可见模板没有本地 staging 副本，属于 `cache_only`；只能最小更新 cache 并报告上游覆盖风险，不得声称永久生效。
- Windows PowerShell 管道把中文脚本直接传给 Python 可能按系统代码页写成 `?`；应用模式必须使用 UTF-8 文件输入或 ASCII `\\u` 转义，并逐文件检查存在中文字符后才清 cache。

### 显式 ID 集合与系统/模板技能回退（2026-07-25，observed）

- 用户直接提供 `[$namespace:id](absolute-path\SKILL.md)` 时，路径和 ID 一起作为本次可见集合证据；不能因不在旧截图 29 项中而漏检。
- 系统技能命令栏说明来自 `D:\codex\skills\.system\<skill>\agents\openai.yaml` 的 `interface.short_description`；`SKILL.md` frontmatter 只作为回退或其他界面说明。
- `openai-templates` 的部分技能没有 `agents/openai.yaml`，实际说明来自 `SKILL.md` frontmatter `description`；Audit 必须把这类项标为 `cache_only`，不能只检查 `agents/openai.yaml`。
- 上次遗漏原因：翻译流程只使用历史截图集合，并把无 `agents/openai.yaml` 的模板项视为未映射；本次修正为“显式 ID 优先 + agents/openai.yaml/frontmatter 双字段回读”。
- `control-in-app-browser` 曾出现 cache/staging 行为文件指纹不同但展示字段已一致；这类项应标记 `display_equivalent_sources`，只阻止功能文件写入，不阻止已确认的展示文案回读。

## ZCode（本机已验证的发现层）

| 对象 | 本地来源 | 已验证事实 | UI 映射状态 |
|---|---|---|---|
| 用户/项目技能 | `<project>/.zcode/skills`、`<project>/.agents/skills`、`~/.zcode/skills`、`~/.agents/skills` 下 `SKILL.md` frontmatter | `name` / `description` 是发现和触发元数据；路径优先级由 ZCode skill-creator 说明 | 命令栏/侧边栏具体渲染位置 `unavailable` |
| 已启用插件 | `~/.zcode/cli/config.json` → `plugins.enabledPlugins` | 只记录启用状态，不是说明文字来源 | `unavailable` |
| 插件命令 | `<plugin>/commands/*.md` frontmatter `description` | 可作为命令说明候选 | 需实际客户端验收 |

## Claude Code（本机插件示例已验证）

| 展示对象 | 来源 | 已验证事实 |
|---|---|---|
| `/help` 中用户调用技能/命令说明 | `skills/<name>/SKILL.md` 或 legacy `commands/<name>.md` frontmatter `description` | 本机 example-plugin 明确说明该字段显示于 `/help` |
| 插件 UI 标签 | marketplace 或 manifest 的 `displayName` | 本机 marketplace README 说明可用 `displayName` 更新 UI 标签；不修改 immutable slug |

## 通用 `.agents` 技能

`~/.agents/skills/<name>/SKILL.md` 的 `name` 与 `description` 是可审计的技能元数据，但 `.agents` 本身不定义命令栏或侧边栏渲染器。Audit 必须将具体 Agent 标为 `unavailable`，不能擅自映射到 Codex、ZCode 或 Claude UI。

## Audit 操作规则

1. 翻译精炼先取得侧栏和命令栏的可见性证据，再以 `collect_codex_display_candidates.py --scope visible --visible-id <id>` 逐项解析；绝不以 `installed`、`catalog` 或缓存发现结果替代可见性。
2. 支持裸 ID、`namespace:id` 和 `$namespace:id`；输出中必须给出 `input_id`、`normalized_id`、`visibility_evidence`、`source_paths`、`source_type`、`inventory_scope`、`editable` 和 `source_candidates`；未显示项不输出。
3. official plugin cache、runtime、manifest、remote catalog 一律只读，只生成候选；修改后可见 UI 的说法必须由实际客户端验收支持。
4. 只有用户自制且 `editable=true` 的技能才可在确认后修改 frontmatter；修改后重新解析并执行严格验证。
5. 用户声明数量必须与 ID 数量及 `--expect-visible-count` 一致；数量不一致、缺失、歧义或 `source_conflict` 时暂停写入。
6. 若需要证明某客户端的实际命令栏或侧边栏位置，使用客户端自动化或人工截图验收；文件层证据不能替代 UI 验收。客户端自动化不可用时，要求用户提供截图或可复制 ID 列表。
7. 应用中文候选后，必须以同一可见 ID 集合执行 `--require-chinese --expect-visible-count <n> --check-unchanged`；缺少项、仍英文项或未完成两页截图验收时，报告 `partial`。
