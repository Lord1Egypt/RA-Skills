# WorldSim — 命令速查（commands.md）

> **本文件 = 全部命令的唯一速查**（worldctl.py 子命令 / shell 脚本 / 用户命令）。命令不会用时来这里查，不需要逐轮执行。
> 行为指令在 SKILL.md（编排·每轮必读）+ references/phase_*.md（阶段规则·阶段开始前必读）；键表/写语义在 references/keys.md；写入批次格式在 references/write_protocol.md。
> **写入通道：** 下方 heredoc 示例为 bash 语法；无 heredoc 的 shell（如 Windows PowerShell）走 `--file` 通道——规则/落点/命名/清理见 references/write_protocol.md §批次文本双通道（全局唯一权威），本文件不重复。

---

## worldctl.py 子命令

| 子命令 | 用法 | 说明 |
|--------|------|------|
| read（默认·核心集） | `python3 {skill_dir}/scripts/worldctl.py <世界> read` | 加载世界必读：world_state/conflicts/焦点场景 scene_state/焦内 CHAR_state（CHAR 按需补读） |
| read（指定文件） | `python3 {skill_dir}/scripts/worldctl.py <世界> read world_state conflicts` | 位置参数=文件 key 过滤（或 `--files a,b,c`） |
| read（全量） | `python3 {skill_dir}/scripts/worldctl.py <世界> read --all` | 调试用全量（含全部已发现状态文件） |
| write（增量合并） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> write` | YAML diff 递归合并——world_map/结构化短字段通道 |
| write（全量覆写） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> write --full` | 整文件覆写（少用） |
| write-raw（单字段） | `python3 {skill_dir}/scripts/worldctl.py <世界> write-raw <文件key> <YAML键> "内容"` | 仅限短 ASCII 值；**中文/多行一律走 `--batch`**（通道见 references/write_protocol.md §批次文本双通道——CLI 参数传中文随 locale 解码会损坏文件） |
| write-raw（批量·推荐） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> write-raw --batch` | **change set 写入通道**——内置 audit 语义检查（硬性违规单字段顶回·软性警告 validate 汇总）+ 写入后自动轻量校验。**实跑前必先过 `--dry-run`**（见下条） |
| write-raw（批量·预演） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> write-raw --batch --dry-run` | **实跑前的硬性闸·判据=退出码**——解析+audit+段级闸门+op 级形态预检+对比磁盘差异，**不落盘**。`exit 1`=实跑必失败（段级闸门拦截·整段零副作用 或 op 级失败·部分写入）→ **禁提交**；`exit 0`=通过（**必要条件非充分**·不模拟磁盘异常）。重跑批次/脚本改过 change set 后必跑 |
| write-raw（批量·回退） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> write-raw --batch --force` | **显式回退专用**——绕过 audit 轮次单调/轨迹覆盖写（无快照手工重建时用·见 rollback.md）；其余硬性检查照常·非幂等同前·回退后必做残留扫描+validate |
| write-raw（批量·重提） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> write-raw --batch --resume-from <段N>` | **合并批失败后重提**：只执行段 N 及其后（段号按原始批次 1 起始·免重跑已成功段）；须先按 stderr 的 `[BATCH-FAIL]` 报告，把已落盘的 `###STORYLINE/###BEAT` 从重提内容中剔除，再跑一次 `--dry-run` 预演确认无 `[无变化]` 误报 |
| write-raw（批量·维护） | `python3 {skill_dir}/scripts/worldctl.py <世界> write-raw --batch --maintenance --file <临时文件>` | **同轮续批/字段修复/数据归一专用**——豁免段级完整性闸（角色覆盖/ACTION↔decision 共现/必含项/施压方向/轨道/cast），op 级合法性照常（格式/白名单/单写者/结构化 APPEND/轮次单调）。一批只含增量 op（已落盘 KEY 幂等重写、APPEND 靠查重）·不得用于常规六阶段推进 |
| append-raw（单字段追加） | `python3 {skill_dir}/scripts/worldctl.py <世界> append-raw <文件key> <YAML键> "内容"` | 字段末尾追加——仅短 ASCII 值·中文/多行走 `--batch` |
| audit（预检） | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> audit` | 只校验不落盘；通过 → `AUDIT OK`；硬性违规 → 列出全部 exit 1；仅软性警告 → 打印警告 exit 0 |
| validate | `python3 {skill_dir}/scripts/worldctl.py <世界> validate` | YAML 格式报错 + 内容级警告（load 后/跨 Session 恢复后必跑；含同物理地点场景元素继承检查）。**格式错误 → exit 1（硬拦·先修坏文件再继续）；仅内容警告 → exit 0** |
| init-states | `python3 {skill_dir}/scripts/worldctl.py <世界> init-states` | **启动世界动态文件物化（幂等·缺什么补什么·LF）**——conflicts←SEED（物化前净化：剥离 Markdown 标题/引用块/说明段落/HTML 注释/未填占位，只提取顶层 CT-XX 块；净化后仍非法 YAML → exit 1 不落盘·无 CT 则 WARN） / 模板三件 / CHAR_state 骨架（自主性解析自 CHAR_.md·外部者无该行）+ regions/ 自动对账；叙事约定为空时提示 LLM 填写（session_recovery.md 第二章 Step 0 唯一入口） |
| map-sync | `python3 {skill_dir}/scripts/worldctl.py <世界> map-sync` | world_map 镜像层对账（regions/ 目录树→补缺失节点·init-states 自动调用·validate 报缺失时也可单独跑） |
| grep | `python3 {skill_dir}/scripts/worldctl.py <世界> grep <关键词>` | 全仓（含所有场景 scene_state）搜索元素注册原文——**使用已有元素前核对形态/位置/状态/性质的标准工具（W4 前置·防凭印象改写元素）**；无匹配=未注册=使用即幻觉 |
| delete | `python3 {skill_dir}/scripts/worldctl.py <世界> delete <文件key> <键路径>` | 删整条 CT / pending 条目；批量流支持 `###DELETE:`。**删除是失败即失败的操作**——未知文件 key / 键或路径不存在 = 该 op 失败（直调 exit 1·批次内计入失败账·不静默跳过）。删除前自动备份原文件到 `tmp/<文件名>.delete.<时间戳>.bak`（备份失败=不执行删除；误删可从备份恢复） |
| storyline show | `python3 {skill_dir}/scripts/worldctl.py <世界> storyline show [SL-XX]` | 读事件线（全部 / 指定·states/storylines.yaml） |
| storyline add | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> storyline add`（stdin=单条事件线 YAML：名称/类型/状态/拍序） | **storylines 唯一写入入口·②编剧**——建线（ID 自动递增 SL-XX·脚本机械落盘+结构/枚举校验·LLM 不直接改 YAML·**顶点拍须含 `顶点约束`（关系主体≥2/核心张力/变化维度/非玩家爆破≥1·缺则拒绝 exit 1）**）；建线后起点指针由③导演 `beat set 新线 <起点拍>` 落 direction（**同批 add 用「新线」·add 的 SL-XX 由脚本分配不可预知·跨批则 read 后写实际 SL-XX**） |
| storyline rewrite | `cat <<'EOF' \| python3 {skill_dir}/scripts/worldctl.py <世界> storyline rewrite SL-XX`（stdin=新事件线 YAML） | 换线/重规划（现实不承接·前提取翻但问题仍重要·顶点拍同步重填·缺则拒绝） |
| storyline close | `python3 {skill_dir}/scripts/worldctl.py <世界> storyline close SL-XX`（批次中 `###STORYLINE: close SL-XX` 后跟一行 `收束摘要:`） | **收束（进入余波拍·待收束（`direction.当前拍==余波`））**——保留 名称/类型＋状态=已收束＋收束摘要·清拍序；当前线收束须当前拍==余波（非余波/缺摘要 exit 1）；遗留线收束凭收束摘要留档·指针不动；close与add分别触发、可同批可分轮 |
| storyline clear | `python3 {skill_dir}/scripts/worldctl.py <世界> storyline clear SL-XX` | 废弃（不承接·三问全灭——前提崩塌/问题无意义/无承诺待兑现）——整条抹为空锚点·direction 指针自动复位；当前拍=余波时 WARN 提示应走 close 收束留档 |
| beat show | `python3 {skill_dir}/scripts/worldctl.py <世界> beat show` | 读 direction（当前事件线/当前拍/演出状态/guidance） |
| beat set | `python3 {skill_dir}/scripts/worldctl.py <世界> beat set SL-XX 拍名`（同批建线时批次内写 `###BEAT: set 新线 拍名`·脚本替换为 add 实际分配的 SL-XX） | 跨线切换/空指针初始/同拍重锚（建线后③导演设定起点拍·**同批 add 用「新线」否则写实际 SL-XX**·进入顶点时自动记录基准快照·**同线在指且换拍时拒绝·同线换拍用 advance/续演用 deepen**·**进入新拍时时间窗口重置：`预算` 默认←该拍拍序 `预估时长`·`起点`=当前世界时间**） |
| beat deepen | `python3 {skill_dir}/scripts/worldctl.py <世界> beat deepen SL-XX` | 续演当前拍——指针不动，在这一拍里继续演深、演到该爆发的节点（③导演回判确认·无写入·旧名 stay 保留一个版本） |
| beat advance | `python3 {skill_dir}/scripts/worldctl.py <世界> beat advance SL-XX 拍名` | 推进指针（校验拍名在拍序中·**禁回退**·顶点出线=advance SL-XX 余波 受 gate director 收束核验；尚不推进时用 deepen 续演当前拍·**进入新拍时时间窗口重置：`预算` 默认←该拍拍序 `预估时长`（缺则清空待③重估）·`起点`=当前世界时间**） |
| in-track | `python3 {skill_dir}/scripts/worldctl.py <世界> in-track` | 只读查询——按各 CHAR_.md「默认循环时间线」表+world_state 当前时间，输出此刻各循环角色应在哪/做什么（③导演调度单输入之一·循环世界用；无时间线角色报「无可用时间线」·不改任何状态）。**已并入 precheck SNAPSHOT §1b·保留为独立查询手段** |
| **precheck** | `python3 {skill_dir}/scripts/worldctl.py <世界> precheck` | **本轮调度信号导出器（只读·exit 0 恒过·不拦截）**——机械义务前置暴露 ＋ 唤醒判定 ＋ SNAPSHOT 数据快照。**细则见下方「precheck 细则」** |
| **context** | `python3 {skill_dir}/scripts/worldctl.py <世界> context [角色]` | **Runtime Context 机械导出（v0.28·只读）**——direction 拍级字段编译（当前拍戏剧问题/guidance/调度单/时间窗口）+ 推进池CT摘要 + 环境压力项 + 该角色相关事件/可观察行动；④角色子 agent 组装通道优先引用（省重复读多文件 token）；无 context 则按 phase_actor 数据就绪逐项读 |
| round-check | `python3 {skill_dir}/scripts/worldctl.py <世界> round-check` | **⑤场记轮完整性收尾**——direction/世界三件套/场景时间线/区域一致性（POV 位置节点 vs 焦点场景区域节点·空间已变未切即 FAIL·途经节点豁免）/引用对账逐项核对·FAIL exit 1 |
| **cast-baseline** | `python3 {skill_dir}/scripts/worldctl.py <世界> cast-baseline` | **场景 cast 基线查询（只读·exit 0 恒过）**——输出当前焦点场景的基线名单与 scene_card 两栏覆盖/缺失情况（口径与 gate keeper cast 硬拦同源：调度单四层点名无条件入基线·常驻NPC/关联角色按当前时刻时间线命中本场者入基线·子区域位置命中计入本场）；**场景切换时 init_scene 焦点切换后、写 scene_card 前运行一次，基线名单照填「出场角色」/「焦外/在场」两栏**（scene_management §6） |
| **ledger** | `python3 {skill_dir}/scripts/worldctl.py <世界> ledger [轮次]` | **批次账本查询（只读·取证面）**——各阶段段 `阶段/META/op索引`，④角色段额外含 `###MUSE/###ACTION/###SCHEDULE/###META` 原文（脚本在各段落盘成功后自动写 `scenes/{段所属场景}/.ledger_r{轮次}.{阶段}.{时间戳}.yaml`·点前缀不进 discover/read/加载面）；跨场景轮焦点场景未命中时自动回退扫全部场景；缺轮次=列出全部账本。用途=标准模式审计取证与续驱动恢复；**创作路径不读** |
| convert（.md→.yaml） | `python3 {skill_dir}/scripts/worldctl.py <世界> convert` | 旧 .md 状态文件转 .yaml |
| gate | `python3 {skill_dir}/scripts/worldctl.py <世界> gate dramatist\|storyliner\|director\|actor\|keeper\|writer [--check] [--target N] [--style sepia|dialogue|explicit]` | 阶段出口闸门——批次类五阶段的闸门已默认内嵌于 write-raw --batch 逐段执行（`--force` 豁免）；本命令无 `--check` 打印该阶段人工审计清单（gates.md 同源），有 `--check` 用于 writer 叙事核验与单段手动复检——批次类阶段须把该段批次文本（含 `###STAGE` 行）经 stdin/`--file` 重新提交（空输入即拦·不复检已落盘状态），不合格 exit 1；writer 可选 `--target` 大约目标数/`--style` 所用校准工具（sepia\|dialogue\|explicit·缺声明软提醒·不拦截） |
| lint | `python3 {skill_dir}/scripts/worldctl.py <世界> lint` | 全部状态文件 YAML 格式/引用问题只读检查（不落盘） |
| fix | `python3 {skill_dir}/scripts/worldctl.py <世界> fix` | 规范化重写全部 YAML 状态文件（snap 自动备份 + validate） |
| scan | `python3 {skill_dir}/scripts/worldctl.py <世界> scan <关键词> [--live]` | 全仓关键词扫描（worlds/<世界>/ 下 .md/.yaml·排除 narrative 轮转与 archive；`--live` 只扫现行文件）——残留扫描/修复验证用；退出码：0=无匹配（已清除）1=有匹配 2=用法错误 |

### precheck 细则

**作用**：把 gate/round-check 必然强制的**机械义务**前置暴露（顶点拍 / 停滞旗标 / 不承接旗标 / CT待结算 / 空表建线 / 未引用CT建线 / 切场景 / 跨天 / 结构基线），让 LLM 第一射即满足，避免 gate 失败整轮重提。

**输出三段：**
- **唤醒判定（首行）**：①/② 唤醒或未唤醒＋机械原因 · ③④⑤⑥ 恒跑——Step1 编排任务单直接取用；
- **机械义务**：结构基线缺失（最高优先级·必须先行初始化）＋ `escalation_flags.CT待结算`（①必含 CT op）＋ 时间窗口已耗导出。**只覆盖状态可导出的机械义务**——用户指令/重大事件/回判张力等推断类触发仍由 LLM 判定（输出末尾明示）；
- **SNAPSHOT 数据快照**（参考数据·非义务）：§1a 临近互锁事件（LOOPS 跨场景互锁时刻表·与窗口重叠·窗口＝time_window 缺省 30min·③调度单「即将触发事件」预判）· §1b 循环轨道对照（预设 vs 实际·偏离基线·范围＝调度单点名循环角色 ∪ 当前焦点区 REGION 常驻NPC ∪ §1a互锁涉及角色）· §2 元素注册索引（scene_state 元素名·替代⑥多次 grep）· §3 骨架待物化角色（本轮相关）。

**用法**：各阶段取数优先引用快照·上下文已有→跳过重复读/grep；本轮编排前跑。与 `--dry-run`（批内预演）/ `gate --check`（单段复验）互补。

> **批次自动执行（硬性）：** 批次中的 `###STORYLINE:`（②编剧·结构）与 `###BEAT:`（③导演·指针）由 write-raw --batch 自动执行对应子命令落盘（`add`/`rewrite` 后直接跟事件线 YAML 块直到下一个 `###` 行·失败=批次拦截 exit 1）——**LLM 不手动调用 storyline/beat 写命令**；下表命令保留用于查询（show）与维护。
> **每轮触发（硬性·条件跳过）：**
> - **②编剧**：`###STORYLINE: add/rewrite/close/clear`（add 取材按 phase_storyliner D5——扫描冲突池与焦点场景·NPC-NPC 与玩家 CT 同权；进入余波拍·待收束〔`direction.当前拍==余波`〕；顶点拍预填 顶点约束·缺则拒绝）＋ `###KEY: 故事弧线.*`（phase_storyliner D1 弧线定位·本批必含）。
> - **③导演**：每轮回判——
>   - 已兑现 → `###BEAT: advance SL-XX 下一拍`（顶点＝advance 余波·受 gate director 收束核验）；
>   - 未兑现且窗口未耗尽 → `###BEAT: deepen SL-XX` ＋ `节拍决策=继续当前拍`（窗口＝拍发育期；承接判断点名调度单各角色的未完成意图；验收点＝窗口耗尽：已答→advance；未答且意图仍在推进本拍问题→续演并批内重设时间窗口 `{起点=当前世界时间·新拍级预算}`；未答且意图已不再推进→`escalation_flags.停滞`·gate 核验→①次轮加压/兜底）；
>   - 不承接/意外事件 → escalation flag → ②次轮三问定原线去向（保留＋建新线接焦 / rewrite / clear·判据见 phase_storyliner D1）。
> - **查询轮/维护轮豁免。**

## Shell 脚本

| 脚本 | 用法 | 说明 |
|------|------|------|
| write_narrative.py | `cat <<'EOF' \| python3 {skill_dir}/scripts/write_narrative.py <世界> <场景ID> [--scene2 <新场景ID>] [--target N] [--style sepia\|dialogue\|explicit]`（场景ID支持短 ID S05 或完整目录名） | ⚠ 写入磁盘：前置 `gate writer --check` 通过才落盘至焦点场景 narrative.md（未通过不落盘；`--force` 跳检供维护/回退）。**跨场景轮用 `--scene2` 一次落两段**（输入＝合并正文·两段各带场景头行·闸门按合并正文跑一次） |
| snap.py save | `python3 {skill_dir}/scripts/snap.py <世界> save [快照名]` | 缺省名自动生成「场景ID-场景名-时间戳」——⚠ 写入磁盘：复制当前状态至快照目录 |
| snap.py load | `python3 {skill_dir}/scripts/snap.py <世界> load <快照名>` | 破坏性操作（覆盖当前状态·自动备份 _before_）——交互提示确认 / 非交互加 `--force` |
| snap.py list | `python3 {skill_dir}/scripts/snap.py <世界> list` | 列出全部快照 |
| snap.py delete | `python3 {skill_dir}/scripts/snap.py <世界> delete <快照名>` | 破坏性操作（不可恢复）——交互提示确认 / 非交互加 `--force` |
| init_scene.py | `python3 {skill_dir}/scripts/init_scene.py <世界> <场景ID> <场景名> [--from <旧场景ID>] [--type <类型>] [--time <时间>] [--cast <出场角色>]` | `--from`：继承旧场景 scene_state 的物理锚点/道具清单——**同物理地点切换必用**，防止漏继承；`--type/--time/--cast` 自动填充 scene_card 与 INDEX 行，缺省标「待填」 |
| reset_scene.py | `python3 {skill_dir}/scripts/reset_scene.py <世界> [<场景ID>] [--force]` | **重置场景到 start_snapshot 状态**——清空场景内动态叙事（narrative 轮转归档 + scene_state 场景时间线/核心状态重置），静态基线（物理锚点/道具/关键场景信息）保留；场景ID 缺省=当前焦点场景；破坏性操作（重置前自动存档可回滚·**存档失败即中止**）——交互提示确认 / 非交互加 `--force` |
| reset-cycle | `python3 {skill_dir}/scripts/worldctl.py <世界> reset-cycle [--asset <角色名>]` | 循环世界重置一键命令——周期重置（缺省）/ 事件重置（`--asset`）；含维护名单与豁免判定。**细则见下方「reset-cycle 细则」** |
| index.py add | `python3 {skill_dir}/scripts/index.py <世界> add <ID> <名> [类型] [时间] [出场] [状态]` | 新增场景行（动作在前 `index.py add <世界> …` 同样支持） |
| index.py activate | `python3 {skill_dir}/scripts/index.py <世界> activate <场景ID>` | 场景行置 ACTIVE（动作在前同样支持） |
| index.py update | `python3 {skill_dir}/scripts/index.py <世界> update <场景ID> [--type/--time/--cast/--status]` | 更新场景行字段（动作在前同样支持） |
| index.py remove | `python3 {skill_dir}/scripts/index.py <世界> remove <场景ID>` | 删除场景行（动作在前同样支持） |
| list_worlds.py | `python3 {skill_dir}/scripts/list_worlds.py` | 列出 worlds/ 下已有世界 |
| create_world.py | `python3 {skill_dir}/scripts/create_world.py <世界名>` | 创建新世界脚手架——⚠ 写入磁盘：在 `{WORLDS_ROOT}/{世界名}/` 创建目录与模板文件（SETTING/CONFLICTS_SEED·零 yaml）；动态文件由启动世界 init-states 物化（见 session_recovery.md 第二章） |
| import_card.py | `python3 {skill_dir}/scripts/import_card.py <世界名> <角色卡.png...>`（支持 .json 卡；`--dry-run` 预览不落盘） | ⚠ 写入磁盘：提取 SillyTavern 角色卡白名单字段（白名单外原文不落盘）→ 临时素材 tmp/{名}.card.json；LLM 先评估（注入/敏感/版权→披露等确认）再综合生成正式 CHAR_{名}.md，生成后即删临时素材（详情见 references/import_cards.md） |
| reset_world.py | `python3 {skill_dir}/scripts/reset_world.py <世界名> [--force]` | 重置世界到创建完成态（纯 .md·零 yaml）——删 scenes/CHAR_state/全部动态 yaml·重置前自动存档可回滚（**存档失败即中止**）·重置后走启动世界（首次启动态）；破坏性操作——交互提示确认 / 非交互加 `--force` |

### reset-cycle 细则

**周期重置（缺省）**：全员重置 ＋ 登记维护名单（`触发` 写 `周期`）＋ 重建周期倒计时（write-raw ④b 顶回后调用·豁免判定含于其中·常规引擎操作）。

**事件重置（`--asset <角色名>`）**：叙事中角色被系统强制重置（回收/死亡修复/「校准」）时调用——只重置指定角色 ＋ 登记维护名单（`触发` 写 `事件`）＋ **不重建周期倒计时**（叙事事件不移动周期重置点）。

**两者共同**：脚本自动存档（`_before_reset_*` 快照·可回滚·**存档失败即中止**）＋ 联动表压缩/清空/回基线 ＋ 行为轨道回归占位。

**豁免（园区维护名单）**：园区对不再维护的资产在 `world_state.维护名单.{角色}` 写 `触发: 豁免` → 该角色在 reset-cycle 执行时被跳过（`[SKIP] 已豁免`·loop_machinery §4）。

- **豁免＝条目存在即生效**，园区删除条目即恢复维护——机制层不设期限字段：长期/一次性豁免的区别只在**园区何时删条目**（不删＝长期；用完即删＝一次性）。
- 豁免条目**不改写任何字段**（`重置日期`/`轮次` 恒为上次重置的事实）；**豁免条目即名单实体**（`触发: 豁免` 只表达「园区未对其执行维护」·不携带任何已执行维护的事实）。
- audit 重置覆盖判定排除豁免条目（豁免不算全员重置已执行·其他循环角色仍须重置）。

**调用后 LLM**：保留候选微调 / 状态按 CHAR_.md 默认循环时间线补写 / CT 节拍核查 / 重置叙事。幂等（当日已重置则重跑无害）。

## 用户命令（对话内）

| 命令 | 作用 |
|------|------|
| 「创建世界 <名>」 | 走 session_recovery.md 第一章（create_world.py 脚手架 + 创作填充→校验→收尾提示启动世界） |
| 「重置世界」/「/reset」 | reset_world.py——破坏性操作（自动存档可回滚）·重置后走启动世界（首次启动态） |
| 「重置场景」/「/reset-scene [场景ID]」 | reset_scene.py——重置指定场景（缺省=当前焦点场景）到 start_snapshot 状态（自动存档可回滚） |
| 「启动世界 <名>」「继续世界 <名>」「进入世界 <名>」（会话首轮·须带世界名） | 启动世界统一序列（首次启动/跨 Session 恢复）——走 session_recovery.md 第二章：物化→入场物化→分层加载→validate→循环核对→描绘→停住·不推进；用户只说「继续/恢复」而未指名世界 → 列出已有世界请其点名 |
| `/scene <ID>` / `/scene new <名>` | 场景切换 / 新建场景 |
| `/conflicts` | 查看冲突 |
| `/storylines` | 查看故事线 |
| `/status [名]` / `/status --full` | 查看角色状态 / 完整状态 |
| `/sync` / `/update` | 场记记录变化更新状态 |
| `/save [名]` / `/load <名>` | 存档管理（⚠ /load 覆盖当前状态·自动备份 _before_ 可回滚） |
| `/silent` | 切回沉浸式模式（全局默认·沉浸·只推叙事正文）——world_state 写 `输出模式: 沉浸式` |
| `/loud` / 说「调试」「标准模式」 | 切到标准模式（完整回复正文 + 六阶段人工审计·清单见 references/gates.md）——world_state 写 `输出模式: 标准` |
| 「审计」/「/audit」 | **用户觉察不对劲时使用**——六阶段审计流程（机械核验 → 六阶段人工审计 → 知情边界核对 → 伏笔闭环核对）；输出＝逐项 PASS/FAIL ＋ 证据。**细则见下方「/audit 细则」** |

---

### /audit 细则

用户觉察不对劲时使用——六阶段审计流程（人工清单＝references/gates.md·机械项调用现成工具）：

- **① 机械核验**＝worldctl.py `validate` ＋ `audit` ＋ `gate <阶段> --check` ＋ `round-check`；
- **② 六阶段人工审计**＝加载 references/gates.md → D/S/R/A/K/W 清单逐项（默认不通过·找茬制·证据引用）；
- **③ 知情边界核对**＝有 knowledge_index.yaml → 独立审计者视角逐条按 `记录` 指针读状态文件比对 ＋ 清理（已公开/已落定/循环重置失效→删·不确定留）；
- **④ 伏笔闭环核对**＝有 foreshadow.yaml → validate 已机械检查 ＋ 人工核对 `时间` 错位。

**输出**＝逐项 PASS/FAIL ＋ 证据；FAIL → 修复流程（≤2 轮）超限终止报告。

**若审计反复发现同类违规（补丁无效）→ 主动建议用户更换 LLM model**——不无限打补丁·诚实承认模型能力/注意力上限。

## 执行频率分类

- **每轮执行：** write_narrative.py + worldctl.py（write-raw --batch——**change set 原样转交 + 内置 audit + 写入后自动校验**）
- **场景切换时：** init_scene.py + worldctl.py 更新 world_state 顶层字段（**焦点场景** 唯一权威源·必须同步 INDEX ACTIVE 行）
- **存档管理：** snap.py save / snap.py load
- **跨 Session：** worldctl.py read
- **清理：** worldctl.py delete（CT 归档 / pending 条目移除）
