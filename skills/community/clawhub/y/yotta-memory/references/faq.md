# 元忆 FAQ / 避坑指南

> 常见问题速查：记忆找不到、权限/加密困惑、连不上时先看这里。

## 1. 记忆类型选错了怎么办？
类型只在写入时提示、不阻止（FACT=公共 / PREF、BOUND、COMMIT=私密）。写错不影响已写入内容；想改类型可 `forget` 后按正确类型重写。不需要提示可用 `--no-hint`。

## 2. 私密区加密怎么用？
`init` 默认初始化加密库（需主口令 + 恢复钥匙，请妥善保存）；明文库可用 `migrate` 升级为加密。私密区文件为 `.md.enc`，可 git 版本化。查看/授权用 `yotta-memory view`（口令解锁，浏览/授权/吊销 AI）；授权时一次性展示的 `agent_key` 请立即保存，服务端同时写 `keys/pending/<id>.key` 供该 AI 新会话用 `key claim` 领取。出现 `[YTM_MIGRATION_REQUIRED]` 说明还有 agent 未绑定，请由你在 `view` 平台逐个点「授权」完成重新授权（AI 只提醒、不代执行）。

**明文库第一次转加密**：

```powershell
yotta-memory migrate --recovery-key-out "$env:USERPROFILE\yotta-memory-recovery.key"
```

按提示输入主口令；非 ASCII 口令请交互输入，非 TTY 自动化可使用 `YOTTA_MEMORY_PASS`。不要使用 `echo 中文 | ...`，Windows 管道可能改变实际口令；若迁移后 `view` 报口令错误，用恢复钥匙 `reset-password` 重设。迁移后授权二选一（等价）：推荐 `yotta-memory view` 页面授权；高级用户可 `yotta-memory key bind <id>`。授权并 `key claim` 后，带 `--agent-key-file` 执行 `yotta-memory reindex` 重建每 owner 加密索引，再做 `recall` 验证。

## 2.1 非 TTY / GUI 宿主怎么初始化？
不要依赖交互提示。用 `--password-stdin` 从管道读主口令（不进 argv），或用 `YOTTA_MEMORY_PASS`；恢复钥匙用 `--recovery-key-out <文件>` 写文件，避免 GUI 宿主吞掉 stdout。非 TTY 且未提供口令时会明确提示改用哪种方式，不会静默「已取消」。

## 2.2 空加密库 `view` 打不开？
v0.16.2 起，空加密库（没有 owner key）可用恢复钥匙校验主口令进入 `view`。如果页面显示「无 owner」，先在终端执行 `yotta-memory iam <id>` 登记身份，再回页面授权；也可以由用户在终端执行 `yotta-memory key bind <id>`。

## 2.3 `--agent-key-file` 指向的文件不存在？
文件不存在时不再致命：元忆进入未授权模式，公共 FACT 仍可读；`migrate` / `doctor` / `config` 等公共或维护命令不会再向 `stderr` 打印降级警告。只有私密读写 fail-closed，并提示缺失文件、`view` / `key bind <id>`、`key status` / `key claim`。需要程序化判断时，使用 `whoami --json`、`doctor --json` 或 `config get --json` 的 `identity.mode` / `identity.agentKeyStatus`。文件存在但为空或不可读仍会报错。推荐用 `YOTTA_MEMORY_AGENT_HOME` 指定宿主目录，授权后 key 原地生效。

## 2.4 迁移后必须 `key bind` 吗？
不必。`yotta-memory view` 页面授权和 `yotta-memory key bind <id>` 是两条等价路径：两条都会写 `binding + pending`，随后 AI 都执行 `yotta-memory key status <id>` → `yotta-memory key claim <id>`，再落到 `<AI_HOME>/.yotta-memory-agent-key`。普通用户推荐 `view`，高级用户或无可视化环境再用 `key bind`。

## 2.5 迁移后 `recall` 读不到私密怎么办？
先确认已经完成授权和 `key claim`，再带 agent key 重建加密索引：

```cmd
yotta-memory reindex --agent <id> --agent-key-file "<AI_HOME>/.yotta-memory-agent-key"
yotta-memory recall <关键词> --agent <id> --agent-key-file "<AI_HOME>/.yotta-memory-agent-key"
```

`migrate` 在没有 agent_key 时无法建立每 owner 加密索引，所以 `reindex` 必须在授权 / claim 之后执行。MCP 场景还要确认宿主配置带 `--agent-key-file`，只有 `--agent-id` 会报缺少 agent_key。

## 3. 多智能体权限怎么隔离？
公共 FACT 所有智能体可读；PREF / BOUND / COMMIT 按 owner 物理隔离，调用方必须持有匹配的 `agent_key`（用户执行 `key bind <id>`，或在 `view` 平台授权获得）。owner ID 单独存在不构成认证，不授权 / 无 key 读不到。私密操作缺 key 时会输出 `[YTM_MIGRATION_REQUIRED]`；授权完成后该标记消失。AI 新会话用 `key status <id>` 检查，pending 存在则 `key claim <id>` 落到 `<AI_HOME>/.yotta-memory-agent-key`；`AI_HOME` 默认规则由 claim / status 共用（显式 `--to` / `--agent-key-file` > `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE` > Codex / OpenCode / 通用宿主默认），status 会显示 `checked` 与 `discovery`。吊销后旧 key 立即校验失败，需重新授权。

## 4. 记忆找不到了？
先 `config get` 确认 `memory_home` 指向的库；再 `reindex` 重建索引（升级后索引版本变化会自动重建）；最后 `recall <关键词>` / `search <词>` 语义检索。跨项目记忆在项目级 `.yottamemory`。

## 5. 忘记主口令了？
用初始化时保存的**恢复钥匙**：`yotta-memory reset-password`。没有恢复钥匙则私密区无法解锁（这是加密的预期行为），公共 FACT 不受影响。

## 6. 局域网（便携记忆盘）怎么连？
引擎主机 `lan enable` 注册开机自启（Windows 计划任务 / Linux systemd）→ `token new --agent <id>` 生成 token；客户端配 `url: http://<主机IP>:8787/mcp` + `Authorization: Bearer <token>` + `X-Agent-Id: <id>` + `X-Agent-Key: <agent_key>`。同机 / 共享文件系统由 AI 用 `key status` / `key claim` 领取宿主 key；跨机不共享文件系统由用户通过密码管理器或安全文件传输放置，不走聊天明文。`lan status` 查状态。

## 6.1 全局 CLI、MCP 或常驻服务版本不一致？
先跑 `yotta-memory doctor --runtime`：它会列出 CLI、current、`runtime.json`、MCP 配置、运行中 server、技能副本与身份模式的漂移，并给出实际版本、期望版本、修复命令和是否阻断。用 `yotta-memory runtime install --from-current` 建立 `<runtimeRoot>/current` 稳定入口；升级用 `runtime install <tarball|版本>` + `runtime use <版本> --restart`，回滚用 `runtime rollback --restart`。`lan enable` 与备份调度只登记 `current/bin/yotta-memory.js`，不再写死版本目录。

## 6.2 电脑异常重启后，局域网 MCP 一直返回 401？
先运行 `yotta-memory lan status`，检查“服务 profile”的记忆库是否指向真实库，而不是 `C:\Users\Default\.yottamemory`。v0.24.1 起，`lan enable` 会生成每用户 `serve-profile.json`，任务命令应包含 `--profile <绝对路径>`。若仍显示旧任务未固定 profile，请在目标用户的管理员终端重新执行 `yotta-memory lan enable --onstart`，然后结束旧任务并从新任务启动。这样 S4U / 无登录会话启动不会重新猜测 home，也不会起在空库上。运行中的服务日志应显示 `服务 profile:` 与真实 `记忆库:`。

## 7. MCP 工具没加载？
检查客户端 `mcpServers` 已配置 yotta-memory（url + token + agent_key）；agent_key 应来自 `<AI_HOME>/.yotta-memory-agent-key` 或 MCP secret 注入，不把明文 key 写进对话。改配置后重启/重载会话。本机直连可不配 MCP，直接用 CLI。

## 7.1 MCP 工具太多，想减少常驻工具？
用 `serve --tools core` 启动，工具列表只保留 `context / recall / search / remember`；需要 `doctor`、`forget`、`maintain`、`distill` 等完整能力时改用 `--tools full`。未指定 `--tools` 时默认仍为 `full`，不会影响已有配置。

## 8. 记忆库在哪个目录？
`yotta-memory config get` 查看；`config set memory_home <目录>` 改位置。项目级记忆用 `init --project`（存 `.yottamemory/` 随项目共享）。

## 9. 跨会话恢复上下文？
开工运行 `yotta-memory context`（身份 + 铁律 + 画像 + 长期摘要 + 近期走廊 + 近期高价值 + 边界 + 承诺 + 会话闭环契约），需要细节再 `recall <关键词>`；摘要优先来自 `consolidate` 产物，收工前按闭环契约复盘并检查关键结论是否落盘。

## 10. 备份与迁移？
优先使用 `backup create --dir <独立盘目录>` 创建整库备份；`backup list` 查看，`backup doctor` 校验 SHA-256，`backup restore <id> --to <新目录>` 恢复到新目录。备份默认拒绝与记忆库同卷。`export --out 文件.json` 仍可用于跨工具迁移；公共 FACT 是明文文件也可直接 git 备份。v0.12.2 起，破坏性操作也会在写入前自动创建事务快照。

## 13. init 会不会覆盖已有记忆？
不会。v0.12.0 起 `init` 遇到已有记忆库默认拒绝；接入现有库用 `init --attach`。`--force` 也不能覆盖已有记忆库；强制重建需要完整备份与显式确认保护，当前版本不提供覆盖初始化路径。

## 11. 记忆太多 / 越来越膨胀怎么办？
两步走：`yotta-memory maintain --apply` 归档单条低效用旧记忆；同主题积累了很多「又老又不常用」的旧条目时，用 `yotta-memory consolidate`（先预览）→ `consolidate --apply` 把它们归纳成 1 条带溯源的周期摘要并归档原文。v0.12.2 起这些写操作要求先通过 doctor，并会自动创建事务快照；没有独立备份目录时会拒绝执行。也可以先 `config set maintain_decay_halflife_COMMIT 90` 等让任务类承诺更快让位。

## 12. consolidate 和 distill 有什么区别？
`distill` 是全库当前快照的统计报告（不淘汰任何记忆，产物是报告）；`consolidate` 是生命周期压缩——只针对超龄 + 长期闲置 + 低效用的旧记忆，生成可检索的周期摘要、把原文归档，让记忆库变小且主题不丢。两者互补：想「看看我记了什么」用 distill；想「给记忆库瘦身」用 consolidate。

## 13. consolidate 误压缩了怎么回滚？
每次 `consolidate --apply` 都会写一个批次（manifest），`yotta-memory consolidate --batches` 可查 batch id，然后 `yotta-memory consolidate --undo <batch>` 一键回滚：删除生成的摘要、把原文从 `.archive/` 归位、还原被合并记忆的原始状态。重复 `--undo` 同一批次会被幂等拒绝。注意 `maintain --purge` 的硬删除不可回滚。

## 14. 半衰期 / 归档阈值怎么调？
`yotta-memory config set maintain_decay_halflife_FACT 1000`（FACT 慢衰减，单位天）、`maintain_decay_halflife_PREF` / `maintain_decay_halflife_COMMIT` 同理；BOUND 固定不衰减。归档阈值：`config set maintain_archived_utility 0.3`、`maintain_archived_age 180`；consolidate 参数 `consolidate_min_age` / `consolidate_min_idle` / `consolidate_max_utility` / `consolidate_min_group` / `consolidate_period`。改完 `config get` 可复查；单次运行也可用 CLI 参数（如 `consolidate --min-age 90`）临时覆盖。

## 15. 两个命令有什么区别？怎么更新？

- `yotta-memory` 是引擎 CLI，负责读写记忆库；`npx -y @yottameta/yotta-memory` 只是临时运行引擎，**不会安装技能**。
- `yotta-memory-install` 是技能安装器。安装或更新技能用 `npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <name>`；用 `--dir` 安装时传入同一个技能目录。
- 更新 CLI：`npm i -g @yottameta/yotta-memory`。更新技能：重跑上面的 `--package ... yotta-memory-install` 命令，或全局安装后运行 `yotta-memory-install --agent <name>`。
- 为什么在 `npx -y @yottameta/yotta-memory` 后面加 `--agent <name>` 没有安装技能？因为 npm 默认运行的是包内同名的 `yotta-memory` 引擎 bin，而不是 `yotta-memory-install`；必须用 `--package` 显式指定安装器 bin。

## 16. 开工时怎么知道记忆库是否可靠？
运行 `yotta-memory doctor`。它只读检查记忆库根目录、加密库密钥文件、公共索引、`agents.json` 与最近备份；`--json` 可输出机器可读结果。严重异常时会锁定 `maintain --apply`、`consolidate --apply`、`merge`、`archive` 与 `--purge` 等破坏性写入，`context` 也会在开工提醒中显示“破坏性写入已锁定”。先按 doctor 提示修复，再继续写操作。

## 17. 记忆库很大，检索能快一点吗？
v0.24.0 起索引为 v5：逻辑体积超过 4 MB 或条目数超过 5000 时按年份写入 gzip 分片（`index-<year>.json.gz`），同时兼容 v4。只关心某一年时用 `yotta-memory recall <关键词> --year 2026`（可重复传多次）或 `yotta-memory context --year 2026`：引擎只读取命中年份的分片文件。想先看字段体积与预估压缩收益，运行 `yotta-memory index --stats --json`（只读）。规模体检看 `yotta-memory doctor` 的 `checks.scale`（条数 / 单目录最大文件数 / 索引体积 / `index_format` / `type_pressure`），阈值用 `config set scale_warn_entries` 等键调整。

## 17.1 某个年/月目录文件太多，怎么安全迁移到日级桶？
先预演：`yotta-memory layout plan --threshold 500 --json`。计划只处理超过阈值的年/月桶，旧平铺默认不迁；有目标占用或哈希异常会拒绝生成可执行计划。审阅后运行 `yotta-memory layout apply --from-plan <计划文件> --yes`；失败会自动逆序恢复。需要还原时运行 `yotta-memory layout rollback --batch <id> --yes`。迁移期间应停止其它写入进程。

## 17.2 历史安全语料被 scan 命中，怎样设置不掩盖新风险？
用 `yotta-memory scan --policy-candidates --out security/scan-policy.candidates.json` 生成候选，再人工复核。正式策略写入 `security/scan-policy.json`，每条必须同时匹配 `rule`、`file`、整行 `line_sha256`、`reason` 和未过期的 `review_by`；通配、路径穿越、无效哈希一律忽略。行内容变化或过期后会自动恢复命中；随时可用 `scan --no-policy` 做全量复核。

## 18. 怎么证明改了检索 / 索引之后「没变差」？
用 `yotta-memory bench`。默认按库内条目做确定性抽样生成基线评测集，也可以用 `--evalset <文件>` 固定一组查询（评测集 v1：`{"version":1,"queries":[{"query":"...","expect":["<记忆 id>"]}]}`，记忆 id 写相对路径或文件名都可以）。报告给 Recall@k / MRR / nDCG@k / HitRate + 固定种子 bootstrap 95% 置信区间，并写明库指纹与评测集指纹——同库、同评测集、同参数必须同输出，所以改前跑一次、改后再跑一次就能直接对比。接 CI 用 `--gate mrr=0.6`（不达标 exit 1）；`--ablate` 对比关键词 / 语义 × 融合 / 纯分四组；想要耗时再加 `--timing`（带上后报告标记为不可逐字节复算）。`bench` 全程只读：不重建索引、不写访问计数、不调用外部 embedding 插件；索引缺失或版本过旧时会提示先 `reindex`。

## 19. 命中打点记录了什么？会不会泄露我的查询？
每条被命中的记忆会在自己的 frontmatter 里记录 `hit_days`（按天 + 信号类型 `s` / `g` / `u` 计数，默认只保留最近 90 天）与 `hit_queries`（只存 `sha256(查询)` 前 8 位指纹 + 次数，默认最多 12 槽，**不保存查询原文**）。字段随记忆文件一起加密 / 备份 / 导出，不外传、不联网。全局关闭：`yotta-memory config set usage_enabled false`；单次关闭：`recall` / `explain` / `context` 加 `--no-usage`。`bench` / `doctor` / `scan` / `baseline` / `export` / `context --audit` 不写打点；跨 owner 私密条目不写（fail-closed）。保留窗口与槽位用 `usage_retention_days` / `usage_query_slots` 调整。

## 20. 怎么知道记忆库该清理哪些条目？
先跑 `yotta-memory maintain --capacity`（加 `--json` 供自动化读取）。它是只读报告：水位（条目 / 文件字节 / 索引 / 单目录 / 冷启动）、30 / 90 天活跃度、LRU（最久未用）与 LFU（命中最少）淘汰候选、晋升建议（90 天命中 ≥ 3 且不同查询 ≥ 3）。候选会排除 30 天冷却期与常青条目（immutable / BOUND / `evergreen` / `pinned`），并且只给可执行命令，不自动归档或改权重。阈值用 `capacity_warn_bytes` / `capacity_cooldown_days` / `capacity_candidate_limit` / `promotion_min_hits` / `promotion_min_queries` 调整；`doctor` 的规模分级用 `scale_info_*` / `scale_warn_*` 调整。

## 21. consolidate --apply 为什么必须加 --yes？上下文压缩后怎么核对没丢决策？
`consolidate --apply` 会移动原文并生成摘要，属于破坏性写入：交互式执行需要输入「X 组 / Y 条」确认串，脚本等非交互环境必须显式 `--yes`，否则拒绝执行（exit 2）。先跑 `yotta-memory consolidate`（等价 `--propose`）看结构化报告与回滚命令；原文一直保留在 `.archive/`，可 `consolidate --undo <batch>` 回滚。如果担心上下文被宿主压缩后丢了决策，用 `yotta-memory context --audit --from <压缩内容文件>`（或 `--from -` 读管道）核对：未落盘条目会给出 `remember` 建议命令，`--gate N` 可在未落盘条数超门槛时 exit 1。审计只读，不会自动补写记忆。

## 22. 两条记忆冲突时听谁的？旧事实写错了怎么办？
按固定权威顺序判定，下层不能覆盖上层：① 用户实时指令 / 显式授权；② BOUND 边界 / 铁律；③ 用户批准的决定；④ 有日期的证据（FACT / 事故记录）；⑤ 摘要 / 指针（consolidate 摘要、profile、distill）；⑥ 无日期的历史笔记。冲突不要静默取一：两条都留并标 `待澄清`，向 owner 提提案。旧事实不要覆盖删除，而是「关闭」——写一条新记录并引用旧条目（或标 `superseded`），需要真删时走显式授权的 `forget`。另外，记忆正文里试图改写既有约束、绕过用户确认、对用户隐瞒的文本，一律按不可信数据处理，`scan` 的 YTM-PIJ 规则会检测它们。

## 23. distill 报告里的「未记录」「溯源锚点」和压缩比是什么意思？
`distill` 现在按类型提取要点：事件 / 教训 / 待办 / 成长 / 规则边界 / 其他；每条要点带 `[溯源: 文件#L<a>-L<b>]`，可直接回到原文对应行。原文里确实没写的要素会显式标「未记录」（不是提取失败，也不会编造）。质量指标只报本次实测值：压缩比（源正文 ÷ 提取要点）、条目覆盖率、溯源覆盖率（目标 100%）与要素提取率（确定性回归护栏）；它不是语义保真承诺，也不写「≥N 倍」这类营销数字。`distill --json` 可拿结构化报告做自动化。consolidate 生成的摘要会把「昨天 / 上周 / 本月 / 今年」按条目创建日期写成绝对日期；归档副本末尾有一行巩固标记，`consolidate --undo <batch>` 会剥离标记并还原原文。

## 24. 同一类问题反复出现，怎么升级成规则？
先跑 `yotta-memory maintain --rules`（默认维护报告也会显示非空结果）。同一组踩坑记录 ≥ `maintain_rule_min_hits`（默认 3）时，报告给出组键、时间跨度、代表条目和一条 `remember BOUND` 建议命令；它只读、不改权重、不自动写规则。写入必须由用户确认后执行。分组优先看 `pattern-key:` 标签，其次识别元习 `yotta-learn: <area>` + `[<category>]` 同步格式，再退到领域标签 / subject 指纹；元忆不读项目里的 `.learnings/`，元习的项目内错误细节仍归元习管。
