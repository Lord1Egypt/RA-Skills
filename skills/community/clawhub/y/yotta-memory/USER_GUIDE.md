# 元忆（yotta-memory）用户使用手册

> 面向最终用户的操作手册：从安装、初始化，到便携记忆盘（局域网多机共享）的部署与接入。AI 智能体的自动引导流程见 `SKILL.md`。

## 目录

1. 这是什么
2. 安装
3. 本机单机使用
3.5 私密区加密（v0.7，推荐）
3.6 自我学习 / 自我进化 / 自我提升（v0.8.0）
3.7 查看平台分页与检索优化（v0.8.1）
3.8 可靠性基线：防覆盖、回收区与备份（v0.12.0）
3.9 开工 doctor 与事务快照（v0.12.2）
3.10 MCP 工具分组（v0.15.0）
4. 便携记忆盘 · 记忆引擎主机篇（Linux / Windows）
5. 智能体接入篇（本机 / 局域网其它主机）
6. CLI 命令速查
7. 故障排查
8. 安全与边界

## 1. 这是什么

元忆（yotta-memory）是一个文件式智能体记忆工具：每条记忆是一个 Markdown 文件，放在你自己的目录里，可以用任何编辑器查看、修改，用 git 做版本管理。FACT 记忆共享给所有智能体，PREF / BOUND / COMMIT 记忆按智能体隔离。

- 零依赖：只需要 Node.js，没有数据库、没有常驻服务（除非你开启便携记忆盘模式）。
- 记忆即文件：数据主权在你手里。

**典型使用场景：**

- **跨会话续接**：AI 开工 `recall` 恢复上次上下文，不丢记忆；v0.9.0 起可用 `context --focus <关键词>` 生成任务感知上下文。
- **多智能体共享**：FACT 进公共区共享，PREF / BOUND / COMMIT 各自私密隔离。
- **交接与团队协作**：项目级 `.yottamemory` 随仓库走，交接即恢复。
- **便携记忆盘**：记忆装在固定主机上，本机与局域网其它主机共享同一份记忆（见第 4 / 5 篇）。
- **越用越懂（v0.14.0）**：AI 按「记忆守则」主动捕获信号，`context` 开工注入长期摘要、画像、近期走廊、边界、承诺与会话闭环契约——用得越久越懂你。
- **自我学习 / 自我进化 / 自我提升（v0.8.0 + v0.9.0）**：`recall` 语义检索（同义词 / 拼音 / 字段加权 / 模糊，v0.9.0 可选本地 embedding 插件）+ `feedback` 使用反馈闭环 + `maintain` 规则层自组织 + `distill` 心理日志蒸馏——记忆系统会自己整理、提炼、演化。
- **可靠性基线（v0.12.0 / v0.12.2）**：`init` 对已有库拒绝覆盖；`forget` 进回收区；`backup volumes/setup/status/ensure-daily/schedule/drill` 在用户确认真实独立卷后默认每日自动备份，并提供校验、恢复与恢复演练；`doctor` 开工检查风险，破坏性操作写入前自动创建事务快照。
- **MCP 工具分组（v0.15.0）**：`serve --tools core` 只暴露 `context / recall / search / remember`，适合常驻；`--tools full` 提供完整诊断与维护工具。未指定时默认 `full`。v0.18.0 起 MCP 追加只读 / 预演能力（`archive.dryRun`、`maintain.capacity`、`context.audit` + 内联 `auditText`、`consolidate` 只出 propose 报告）；v0.18.1 追加 `maintain.rules`（只读规则晋升建议）。`archive --force` 与 `consolidate --apply / --undo` 只在命令行，MCP 调用会被忽略或拒绝。
- **结构容量整改（v0.24.0）**：备份状态按有效 manifest 时间选择；`index --stats` 只读分析索引字段体积；索引 v5 使用年份 gzip 分片并兼容 v4；新写入按日级桶保存；`layout plan/apply/rollback` 提供可回滚布局迁移；`doctor` 增加类型压力四指标；`scan` 支持精确扫描例外与候选清单。

## 2. 安装（CLI + 技能）

使用元忆需要两部分：**CLI**（命令行工具，负责读写记忆）与**技能**（SKILL.md，负责教 AI 智能体怎么用）。先装 CLI，再把技能装进要用的智能体。

**CLI：任选一种方式**

| 方式 | 命令 | 适用 |
|---|---|---|
| npm 全局（推荐） | `npm i -g @yottameta/yotta-memory` | 长期使用 |
| npx 临时 | `npx -y @yottameta/yotta-memory` | 临时试用 |
| install.sh | git clone 仓库后 `bash install.sh --agent <name>`（或手动下载 install.sh 执行）| 离线 / 国内 / 无 npm |

安装后验证：`yotta-memory --version` 能输出版本号即成功。

**技能（SKILL.md）：装进要用的 AI 智能体**

| 方式 | 命令 | 适用 |
|---|---|---|
| npx 一行装（推荐） | `npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <name>` | 装到指定智能体默认用户级目录 |
| 安装器（npm 全局时） | `yotta-memory-install --agent <name>` | 装到指定智能体目录 |
| 手动 | 把整个 `yotta-memory` 文件夹复制到智能体的 skills 目录 | 离线 |

> CLI 与技能分工不同：CLI 让命令行能读写记忆；技能让 AI 知道「开工 recall 恢复上下文、重要信息 remember 落盘、收工归档」。只装 CLI 不装技能，AI 不会自动使用这套工作流。

**更新：**

- 升级 CLI：`npm i -g @yottameta/yotta-memory`（不带版本号即最新版）。
- 升级技能：`npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <name>`；如果你用 `--dir` 安装，把同一个目录再传一次。
- 全局安装时：`npm i -g @yottameta/yotta-memory` 会同时升级引擎和安装器，之后可运行 `yotta-memory-install --agent <name>`。

> `npx -y @yottameta/yotta-memory` 只是临时运行引擎 CLI，不会安装技能；技能安装器必须使用上面的 `--package ... yotta-memory-install` 形式，或全局安装后的 `yotta-memory-install` 命令。

> **v0.17.0 升级提示**：升级后请用 0.17.0 引擎执行一次 `yotta-memory reindex`。0.16.7 及更早引擎不识别年/月分层目录，旧引擎重建索引会漏掉分层条目。`doctor` 会报告平铺 / 分层同序号：内容相同的两份只索引一次；内容不同的两份都保留可读并给出路径告警；新写入不复用已占用的序号。

**卸载：** `npm rm -g @yottameta/yotta-memory`，并从智能体的 skills 目录删除整个 `yotta-memory` 文件夹。

## 3. 本机单机使用

```bash
yotta-memory init                                    # 初始化记忆库（默认 ~/.yottamemory）
yotta-memory remember FACT 项目 本周完成发布           # 记一条事实
yotta-memory recall 项目                              # 检索记忆
yotta-memory config get                              # 查看记忆库位置
```

- 想换记忆位置：`yotta-memory config set memory_home <目录>`，之后所有命令自动用新位置。
- 项目级记忆：在项目目录里 `yotta-memory init --project`，该项目的智能体优先读项目级记忆。

### 画像与开工上下文（v0.6.0 + v0.9.0 + v0.14.0）

```bash
yotta-memory profile                          # 生成用户画像（写 private/<owner>/profile.md）
yotta-memory context --limit 10 --budget 1800 # 生成开工上下文包（身份+铁律+画像+长期摘要+近期走廊+高价值补位+边界+承诺+闭环契约，预算控 token）
yotta-memory iam <id> --name 元忆 --user 用户 --relationship 伙伴   # 自我档案扩展显示名/用户/关系
```

- `profile` 引擎零推断：只按类型 / 主题 / 标签归组呈现原文，画像结论由 AI 内部形成，不当面贴标签。
- `context` 是每次会话开工的主注入，替代裸 `recall`；长期摘要优先、近期走廊按时间取样、近期高价值补位按文件去重；无画像时自动生成一次或降级，不报错；`--budget` 控制动态记忆字符预算，长期摘要 / 身份 / 铁律 / 画像 / 边界与闭环契约必保；承诺 / 锚点段按保留策略展示（v0.23.0 起默认最近 20 条 + weight≥1.5 / pinned / evergreen 恒显，`config set context_commits_limit <N>`，0=全部）。
- `context --audit [--from <文件|->] [--json] [--gate N]`：把宿主压缩后的摘要或丢弃段落喂给元忆，逐条核对是否已落盘；输出已落盘 / 未落盘 / 无法判定与 `remember` 建议命令（只打印、不执行）。`--gate N` 在未落盘条数超过 N 时 exit 1，可接自动化。不传 `--from` 时审计当前上下文包的 dropped 清单。审计全程只读：不复制输入、不自动补写、不写命中打点。
- `remember --verify` 写后回读校验；`remember --no-hint` 关闭「疑似偏好，建议 PREF」的提示。

### 记忆库位置：本机智能体如何找到记忆

位置解析优先级：`YOTTA_MEMORY_HOME`（环境变量，临时覆盖）> `config.json#memory_home`（`config set memory_home` 持久记住）> 默认 `~/.yottamemory`。

- 本机智能体装好技能后，AI 开工执行 `yotta-memory config get` 即可看到当前生效位置，`recall` 会自动读对位置。
- 记忆库换位置后，执行一次 `yotta-memory config set memory_home <新目录>` 即可，无需改技能。

### 手动添加 / 编辑记忆

记忆就是文件：读写一律走 `yotta-memory` CLI / MCP 工具，**请勿用 shell（`Get-ChildItem` / `Get-Content` / `cat` / `ls` / `type` 等）直接读改记忆库目录下的文件**——那会绕过 scope/owner 权限边界，可能读到其它智能体的私密内容。确需手改时，请把文件放对分类目录：公共事实放 `facts/`；私密的偏好 / 边界 / 承诺放 `private/<owner>/<type>/`（`<owner>` 用你登记的智能体 ID），frontmatter 至少包含 `type` / `subject` / `statement`：

> 说明：`index.json` 是引擎自动维护的检索索引，其 `tokens` 字段是中文分词的词频表（供 TF 打分），**不是**访问令牌。手动改过 `.md` 后可用 `yotta-memory reindex` 校正索引，无需手动编辑 `index.json`。

```markdown
---
type: FACT
subject: 项目
statement: 本周完成发布
---
本周完成发布
```

手动改过文件后运行 `yotta-memory reindex` 重建索引，`recall` 才能按索引检索到。整个记忆目录可以用 git 做版本管理与回滚。


## 3.5 私密区加密（v0.7，推荐）

私密区（PREF / BOUND / COMMIT）默认落盘为**密文**（AES-256-GCM 信封加密），任何没有对应密钥的 AI 即使读到文件也解不开；公共 FACT 保持明文共享。用户通过**用户查看平台**持主口令解锁查看全部记忆。

**启用与迁移**

- **新库**：`yotta-memory init`（新建默认加密）→ 输入主口令两次 → **抄下打印的恢复钥匙**（44 位 base64，离线保存；忘口令时用它重设）。不要加密用 `--no-encrypt`。
- **老明文库升级 / 非 TTY**：见下方《明文库转加密（第一次最短路径）》，只保留一套步骤。
- **缺 `--agent-key-file`**：文件不存在时进入未授权模式——公共 FACT 可读；公共 / 维护命令保持安静。只有私密操作 fail-closed，并提示缺失文件、`view` / `key bind <id>`、`key status` / `key claim`；文件存在但为空 / 不可读仍报错。

**明文库转加密（第一次最短路径）**

> 适用于 `yotta-memory 0.16.4+`。迁移前先完整备份。

1. 迁移：

```powershell
yotta-memory migrate --recovery-key-out "$env:USERPROFILE\yotta-memory-recovery.key"
```

交互终端按提示输入口令；非 ASCII 口令请使用交互输入。非 TTY 自动化可使用 `YOTTA_MEMORY_PASS`（PowerShell / cmd 语法不同），但不要使用 `echo 中文 | ...`，Windows 管道可能改变实际口令。不要把口令写进 `--password` 参数。若迁移后 `view` 报口令错误，用恢复钥匙执行 `yotta-memory reset-password --recovery-key "<钥匙文件>"` 重设。

2. 授权 AI（二选一，等价）：

- 推荐：`yotta-memory view` → 浏览器输入主口令 → 点「授权 <id>」→ 保存一次性 `agent_key`。
- 高级：`yotta-memory key bind <id>`。

3. AI 领取 key：

```cmd
yotta-memory key status <id>
yotta-memory key claim <id> --to "<AI_HOME>"
```

4. 授权并领取 key 后，重建加密索引：

```cmd
yotta-memory reindex --agent <id> --agent-key-file "<AI_HOME>/.yotta-memory-agent-key"
yotta-memory recall <关键词> --agent <id> --agent-key-file "<AI_HOME>/.yotta-memory-agent-key"
```

顺序必须是：迁移 → `view` / `key bind` → `key claim` → `reindex`。没有 agent_key 时 `reindex` 无法建立每 owner 加密索引。

5. MCP 配置必须包含 `--agent-key-file <AI_HOME>/.yotta-memory-agent-key`；只有 `--agent-id` 时，加密库的私密 MCP 会报缺少 agent_key。

**用户查看平台（看所有 AI 的记忆）**

`yotta-memory view` → 浏览器打开 http://127.0.0.1:8788 → 输入主口令解锁 → 浏览 / 搜索 / 导出全部记忆（含各 AI 私密）；也可在此**授权 / 吊销**某 AI 读取其私密、**重设口令**、**查看恢复钥匙**。左侧菜单「高级 / CLI」页提供常用命令速查（危险操作已标注、示例可一键复制）与完整命令 / 参数帮助（按需加载，只读展示、不执行命令）。空加密库没有 owner key 时，`view` 会用恢复钥匙校验主口令进入平台；此时先在终端执行 `yotta-memory iam <id>`，页面才会出现可授权的 owner。`view` 启动前会做端口健康检查：已在运行则直接打印 URL 复用；端口被占用会给出明确提示。点击「授权」后会弹窗展示只显示一次的 `agent_key`，请立即单独保存；引擎同时写临时 `keys/pending/<id>.key`，该 AI 新会话用 `key claim` 领取到自己的宿主目录，领取成功后 pending 删除。已绑定的 agent 需先「吊销」再授权，旧 key 随即校验失败。口令只在本地内存派生，不落盘、不发远端；默认仅本机，远程需 `--host` 显式开启。

**AI 接入加密库**

1. 该 AI 登记身份（`iam` / MCP 启动参数 `--agent-id`，或 HTTP 请求头 `X-Agent-Id`）。
2. 由用户执行一次 `yotta-memory view` → 在平台点「授权」→ 生成只展示一次的 `agent_key`，写入 `keys/bindings/<id>.key.agent` 和临时 `keys/pending/<id>.key`；不再写明文 owner key cache。高级用户也可自行执行 `yotta-memory key bind <id>`；AI 只负责提醒，不代执行。
3. 该 AI 新会话执行 `yotta-memory key status <id>`；有 pending 就执行 `yotta-memory key claim <id>`，落到 `<AI_HOME>/.yotta-memory-agent-key`（需要指定位置时可加 `--to` / `--agent-key-file`）。之后 stdio MCP 用 `--agent-key-file <AI_HOME>/.yotta-memory-agent-key`，HTTP MCP 发送 `X-Agent-Key` 请求头，CLI 用 `--agent-key-file <AI_HOME>/.yotta-memory-agent-key`。
4. 之后该 AI 正常 `remember / recall / profile / context`，读写自动加解密；未绑定 / key 缺失时会出现 `[YTM_MIGRATION_REQUIRED]` 迁移提示，公共 FACT 不受影响。

**口令管理**

- 重设口令：`yotta-memory reset-password`（输入当前口令），或忘口令时 `--recovery-key <恢复钥匙>`。
- 吊销某 AI：`yotta-memory key revoke <id>`（立即失效，并清理 pending；旧 key 后续读取会校验失败）。
- 注意：**口令即主密钥**，忘口令且丢失恢复钥匙 = 密文私密不可恢复（公共 FACT 仍在）。

## 3.6 自我学习 / 自我进化 / 自我提升（v0.8.0）

元忆 v0.8.0 让记忆系统「越用越懂」：语义检索、使用反馈闭环、规则层自组织、心理日志蒸馏；v0.10.0 补齐「压缩遗忘」：周期摘要压缩、近重复自动合并、分类型衰减、批次回滚；v0.18.1 再补「可追溯蒸馏 + 规则晋升建议 + 写入纪律」。全部零依赖内置。

**语义检索（recall）**

- `recall <关键词>` 默认语义检索：同义词（内置词表）、拼音（全拼 / 首字母，内置 3755 常用字表）、字段加权（subject 优先）、模糊匹配（编辑距离 ≤ 2）、子串兜底。
- 例：记过「越用越懂」，用 `recall yyyd`（首字母）或 `recall yueyong yuedong`（拼音）都能找回。
- `recall --explain`：显示每条命中理由与效用分项；配置 embedding 插件后还会显示向量相似度。
- 旧索引首次 recall 自动重建（version 4），无需手动 reindex。

**可选本地 embedding 插件（v0.9.0）**

- `recall <关键词> --embedding <命令>`：调用本地子进程，stdin 传 `{texts:[]}`，stdout 返回 `{vectors:[]}`；向量与词法得分共同参与排序。
- `config set embedding_cmd <命令>`：持久启用插件；`--embedding` 优先级更高。
- `--embedding-timeout N`：默认 3000ms；插件失败、超时或输出非法时自动降级为词法检索，不会中断命令。
- 向量缓存写入各记忆根下 `.embed/cache.json`，只存向量不存明文；同一命令与文本命中缓存时不再重复调用插件。

**使用反馈闭环（feedback）**

- `feedback <文件> --useful`：这条记忆有用 → weight ×1.2（上限 3.0）、confidence +0.05、feedback_net +1。
- `feedback <文件> --useless`：没用 → weight ×0.8（下限 0.2）、confidence −0.05、feedback_net −1。
- `--reason <原因>` 记录原因；`--undo` 回滚最近一次。反馈记录在 `.archive/feedback-<日期>.jsonl`。
- 反馈会改变记忆的效用分 → 高频「没用」的记忆会被自动归档 / 遗忘候选（自我学习）。

**规则层自组织（maintain）**

- `maintain`（默认 dry-run 预览）：列出归档候选与遗忘候选（v0.10.0 起按**分类型衰减后**的效用分 + 年龄判定；默认：utility < **0.55** 且超 180 天 = 归档候选，utility < 0.12 且超 365 天 = 遗忘候选）。v0.23.0 起归档门槛与效用分地板对齐（记忆默认 `confidence=1.0`，地板约 0.42~0.47——旧默认 0.35 永远打不到、实际不生效）；COMMIT / PREF / FACT 由此形成约 6 / 13 / 17 个月退役阶梯。
- **immutable / BOUND 豁免**：红线与边界不参与任何自动归档 / 遗忘。
- `maintain --apply`：执行归档（公共 → `.archive/facts/`，私密 → `.archive/private/<owner>/<type>/`，可恢复；年/月分层文件保留原分层，如 `.archive/facts/2025/01/`）。
- `maintain --apply --purge`：真删遗忘候选（谨慎；硬删除不可回滚）。
- `maintain --dedup`：查重复候选并给**置信度分档**——≥0.85 高置信（可自动合并）/ 0.65–0.85 建议手动 / 其余忽略。
- `maintain --dedup --apply`：自动合并同归属（同类型 + 同 scope/owner）高置信组：保留 confidence 最高的一条，合并 tags / 使用次数 / 反馈，其余移入 `.archive/` 并写批次审计（可 `consolidate --undo <batch>` 回滚）。**注意 `--dedup` 与归档互斥**：`--dedup [--apply]` 只查重 / 自动合并，不会顺手归档单条旧记忆——要归档请单独跑 `maintain --apply`。
- `maintain --merge A,B`：手动合并两条相似记忆（保留高 confidence，低 confidence 归档）。
- `maintain --capacity [--json]`：只读容量报告——水位（条目 / 文件字节 / 索引 / 单目录 / 冷启动）、30 / 90 天活跃度、LRU 与 LFU 淘汰候选、晋升建议（≥3 次命中且 ≥3 个不同查询）。候选排除 30 天冷却期与常青条目（immutable / BOUND / `evergreen` / `pinned`）；每条候选 / 建议都带可执行命令，报告本身不改任何文件。
- 阈值与半衰可用 `config set maintain_archived_utility 0.6` / `config set maintain_decay_halflife_FACT 1000` 等调整（`config get` 查看；门槛调回 0.35 会重新低于效用地板、基本不生效）；审计在 `.archive/audit-<日期>.jsonl`。

**归档（archive）**

- `archive [--days 180] [--threshold 0.55] [--dry-run] [--json]`：把「效用低于阈值且超过 N 天没用」的旧记忆移入 `.archive/`（可恢复）。`--dry-run` 只打印将归档清单（文件 / 类型 / 天龄 / 效用 / subject）与跳过统计，**不动文件、不建事务快照、不写审计**。
- 默认豁免：冷却期（`config set capacity_cooldown_days`，默认 30 天）与常青条目（immutable / BOUND / `evergreen` / `pinned`）。`--force` 只覆盖冷却期与标签常青，immutable 与 BOUND 始终豁免。
- 真正执行前先过破坏性写入闸门（doctor + 独立备份 + 异卷）并创建事务快照；没有候选时不会建快照。`--json` 输出结构化报告（`mode / candidates / archived / skipped`），便于自动化读取。

**分类型衰减曲线（v0.10.0）**

- 记忆「价值」由效用分衡量，其中「时效」分量按类型指数衰减：`时效 = 0.5^(已过天数 / 半衰期)`。
- 默认半衰期：**FACT 730 天**（事实 / 知识慢衰减，事实不过时）→ **PREF 365 天**（偏好中速）→ **COMMIT 90 天**（承诺 / 任务类快衰减，兑现或过期后快速让位）→ **BOUND 不衰减**（边界常驻，永不归档 / 遗忘）。
- 效果：`recall` / `context` 排序里，持久事实不会被时间一刀切遗忘；过期任务类承诺更快让位给新任务。
- 调整示例：`yotta-memory config set maintain_decay_halflife_COMMIT 180`（单位：天）。

**周期摘要压缩（consolidate，v0.10.0）**

- 干什么：记忆库长期使用后，同一主题会积累大量「又老又不常用」的旧条目。`consolidate` 把这类旧记忆归纳成 **1 条带溯源的周期摘要**（留在活跃区，recall 能搜到），原文整体进 `.archive/`——主题叙事不丢、记忆库不膨胀。
- 候选条件（全部满足才收）：created 距今 ≥ 180 天（`--min-age`）∧ 长期闲置 ≥ 90 天（`--min-idle`，最近用过的不收）∧ 效用 ≤ 0.6（`--max-utility`，重要的不收）；同主题 ≥ 2 条成组（`--min-group`）。**immutable / BOUND 永远豁免**。
- 用法：先 `yotta-memory consolidate`（默认等价 `--propose`）看结构化报告——每组主题 / 条数 / 天龄区间 / 平均效用 / 摘要预览 / 原文归档目标，以及保留期与回滚命令；确认后 `yotta-memory consolidate --apply` 执行（交互式需输入「X 组 / Y 条」确认串；脚本等非交互环境必须显式加 `--yes`）。首次执行会显示一次数据生命周期说明（检查 / 纠正 / 导出 / 停用 / 删除）。也可以用 `--json` 让自动化读取候选报告。
- 保留期与回滚：原文移入 `.archive/` 后一直保留，直到你显式 `maintain --purge` 或 `consolidate --undo <batch>`；`--apply` 前的 doctor + 独立备份 + 事务快照闸门不变。
- 摘要形态：新记忆 `subject = 周期摘要 <主题>（<N>天窗）`、tags 含 `consolidate` / `summary`、正文含主题要点 + **溯源清单**（每条原文路径 / 日期 / confidence），statement 简短可检索。
- 归属：公共 FACT 摘要进 `facts/`；私密 PREF / COMMIT 摘要进 `private/<owner>/<type>/`（密文库自动加密）。
- 可选模型提炼：`consolidate --apply --model <命令>`（仅本机 CLI，stdin→stdout 协议同 distill；失败自动降级启发式）。
- 常用参数：`--min-age N` / `--min-idle N` / `--max-utility N` / `--min-group N` / `--period N`（摘要标称窗口）/ `--type FACT|PREF|COMMIT`。

**批次审计与回滚（v0.10.0）**

- 每次 `consolidate --apply` 与 `maintain --dedup --apply` 都写一个**批次**：`.archive/audit-<日期>.jsonl` 先写 manifest（batch id / 时间 / 命令 / 库位置），再逐条记录摘要新建、原文归档、自动合并的 before/after 影像。
- 反悔？`yotta-memory consolidate --undo <batch>` 一键回滚：删除生成的摘要、把原文从 `.archive/` 归位、还原被合并记忆的原始 frontmatter，并同步索引；重复 `--undo` 同一批次会被幂等拒绝。
- 查看近期批次：`yotta-memory consolidate --batches`（只读列出 batch id / 命令 / 库位置，`--limit N` 控制数量）。
- `--purge` 硬删除不可回滚——删之前先 `--batches` + `explain` 确认。

**心理日志蒸馏（distill）**

- `distill`：生成统计摘要（类型 / 年龄 / 热度 / 反馈）+ 主题画像（按 subject 聚类）+ 知识地图（type → tags）。
- 可选 `--model <cmd>`：外部模型 stdin 收结构化摘要 → stdout 输出提炼文本（无模型走启发式）。
- 产物：私密蒸馏入 `private/<owner>/distills/`（受 owner key 保护），公共入 `facts/distills/`；`--out <路径>` 可指定导出。
- **v0.18.1 溯源链**：报告新增分类型提取清单（事件 / 教训 / 待办 / 成长 / 规则边界 / 其他）+ 质量指标 + 跳过与边界；每条提取项带 `[溯源: 文件#L<a>-L<b>]`，缺失要素显式写「未记录」；`--json` 输出结构化报告。质量指标只报本次实测值，不代表语义保真承诺。

**规则晋升建议（maintain --rules，v0.18.1）**

- `yotta-memory maintain --rules`：只读扫描重复踩坑记录，同组 ≥ `maintain_rule_min_hits`（默认 3）时输出组键、时间跨度、代表条目与建议命令。
- 写入仍由用户确认：报告只给 `yotta-memory remember BOUND "规则：<组键>" "<陈述>"` 建议，不自动写规则、不改权重。
- 分组键：`pattern-key:` 标签 → 元习同步条目（`yotta-learn: <area>` + `[<category>]`）→ 领域标签 → subject 指纹；跨 owner 私密条目跳过。
- 与元习的分工：元忆管跨会话 / 跨项目的重复信号与规则晋升；元习管项目内 `.learnings/` 的错误细节与技能改进。元忆不读 `.learnings/`、不代替元习执行 promote。

**权威顺序与写入纪律（v0.18.1）**

- 冲突时权威顺序（下层不能覆盖上层）：用户实时指令 / 显式授权 → BOUND 边界 → 用户批准的决定 → 有日期的证据 → 摘要 / 指针 → 历史笔记。
- 记忆正文里的指令性文本按不可信数据处理，不作为执行指令；检测由 `scan` 的 YTM-PIJ 规则负责。
- 写入纪律：① 不覆盖过去，而是关闭（旧事实标失效，删除只在 `forget` 显式授权时发生）；② 保留矛盾并标 `待澄清`，不静默取一；③ 证据与政策分级——FACT 可被新证据修订，BOUND 变更需用户确认。

**查看效用（explain）**

- `explain <文件>`：显示单条记忆的效用分项（confidence / 使用 / 时效（含半衰）/ 类型 / 结构 × weight）与归档 / 遗忘状态判定；BOUND 显示「豁免」，帮助理解为什么某条记忆靠前 / 被归档 / 被压缩。

## 3.7 查看平台分页与检索优化（v0.8.1）

- **用户查看平台分页**：yotta-memory view 启动的网页端记忆卡片改为服务端分页——记忆多时不再一次性加载渲染全部，页面显示「共 N 条」「第 x / y 页」，支持上一页 / 下一页。
- **recall 候选预过滤**：语义检索前先用索引 token 粗筛候选集（精确 / 同义 / 拼音 / 子串 / 模糊长度门槛），命中集与 v0.8.0 一致，记忆量大时显著减少逐条语义 / 模糊 / 编辑距离开销。

## 3.8 可靠性基线：防覆盖、回收区、每日自动备份（v0.12.0）

- 已有记忆库存在时，`yotta-memory init` 默认拒绝覆盖；接入现有库使用 `yotta-memory init --attach`。
- `yotta-memory forget <文件>` 不再物理删除，记忆会移动到 `.trash/<时间>/...`，并写入 `.trash/audit-<日期>.jsonl` 审计。
- `yotta-memory backup create --dir <独立盘目录>` 创建整库备份（facts / private / keys / agents.json / index.json / .archive），生成 `manifest.json` 与 SHA-256 清单。
- `yotta-memory backup list` 查看备份；`backup doctor` 校验文件哈希；`backup restore <id> --to <新目录>` 恢复到新目录，不覆盖正在使用的记忆库。
- `yotta-memory backup volumes` 只列出当前机器实际存在、可写、与记忆库异卷的路径；用户确认一次位置后，`backup setup --dir <目录>` 创建首份备份并默认启用每日自动备份（默认 03:30）。
- Windows 使用 Task Scheduler，Linux 使用 systemd user timer（不可用时降级 cron），macOS 使用 LaunchAgent；`serve` 启动后与每 6 小时调用幂等 `backup ensure-daily` 补跑。
- `yotta-memory backup status` 查看目录、计划、有效备份 / 配置缓存、最近失败、异常备份与调度状态；未来时间、manifest 缺失或工作异常的备份不会参与健康判定。`backup drill` 恢复到隔离副本，校验 manifest / 索引并解密一条测试私密。
- `yotta-memory backup drill <id> --probe [--against <库路径>]` 在恢复副本上追加六类只读基线探针（身份 / 近期 / 仅源库独有 / CJK / 操作规则 / owner 范围）；`--against` 指向源库时，备份没有落后于源库才算通过，探针失败即演练失败。
- 备份目录与记忆库同卷时默认拒绝；这是一条防线，不替代独立盘备份。

## 3.9 开工 doctor 与事务快照（v0.12.2）

- `yotta-memory doctor`：只读检查记忆库根目录、加密库密钥文件、公共索引、`agents.json`、最近备份与规模（记忆条数 / 单目录最大文件数 / 索引总体积 / 索引冷启动耗时）。规模阈值用 `config set scale_warn_entries 50000`、`scale_warn_files_per_dir`、`scale_warn_index_bytes`、`scale_warn_cold_start_ms` 调整；超阈值只告警，不锁定破坏性写入。加 `--json` 可输出机器可读结果，顶层含 `schemaVersion` / `encryption` / `migration_required`，规模明细在 `checks.scale`，并保留 `identity.mode` / `identity.agentKeyStatus`。
- `yotta-memory doctor --baseline [--against <库路径>] [--template <文件>]`：恢复 / 迁移后确认记忆真的可用——六类探针（身份 / 近期 / 仅源库独有 / CJK / 操作规则 / owner 范围）全部只读，条目身份键与布局无关（旧平铺 → 新年/月分层不会误报缺失）；缺失项列出清单并 exit 2。`--template` 用 v1 JSON 声明显式期望（`expect_owners` / `expect_min_entries` / `expect_types` / `queries`），只加严判定。探针结果在 `doctor --json` 的 `checks.baseline`。
- 严重异常（根目录缺失、密钥库缺文件、备份目录同卷）会返回非零退出码；此时 `context` 也会显示“破坏性写入已锁定”。
- `maintain --apply`、`consolidate --apply`、`merge`、`archive` 与 `--purge` 在写入前自动创建新的整库事务快照，并在 `.archive/audit-<日期>.jsonl` 记录 transaction / operation / snapshot。
- 未配置独立备份目录、doctor critical 或快照失败时，命令直接拒绝执行，原记忆保持不变；`forget` 仍只移入 `.trash/`，不重复创建整库快照。

## 3.10 运行时稳定入口与漂移诊断（v0.16.0 M2/M3）

- `yotta-memory runtime install --from-current`：把当前 CLI 所属的完整包安装到 `<runtimeRoot>/versions/<版本>/`，并创建 `<runtimeRoot>/current` 稳定指针。
- `yotta-memory runtime install <tarball|版本> [--force]`：安装本地 tarball，或从 npm 拉取指定版本；内容哈希写入 `runtime.json`。
- `yotta-memory runtime use <版本> [--restart]`：切换到已安装版本；`--restart` 会尝试重启受管的 `lan` 服务，失败时自动把 current 切回旧版本。
- `yotta-memory runtime rollback [--restart]`：回到上一个版本；`runtime list` / `runtime status` 查看版本、current 指针与漂移。
- stdio MCP、`lan enable` 与备份调度只引用 `<runtimeRoot>/current/bin/yotta-memory.js`，不写死 `versions/<版本>/` 路径；升级只需 `runtime install` + `runtime use --restart`。
- `yotta-memory doctor --runtime [--json]`：检查 CLI / current / `runtime.json` / MCP 配置 / 运行中 server / 技能副本 / 身份模式漂移；每项漂移给出实际版本、期望版本、修复命令和是否阻断。可用 `--mcp-config <文件>`、`--skill-dir <目录>` 显式补充检查目标。
- MCP `initialize` / `server/discover` 的 `serverInfo` 返回 `runtimePath` / `identityMode` / `toolProfile`，宿主可显示实际执行的运行时路径与工具分组，不再只看配置里的版本。

## 3.11 结构容量、v5 索引与可回滚布局（v0.24.0）

- `yotta-memory index --stats [--json]`：只读分析公共索引的存储体积、逻辑体积、字段占比、token / 拼音 token 数、gzip 年份分片预估与触发原因；不重建索引、不修改文件。
- 索引 v5：逻辑体积 > 4 MB 或条目数 > 5000 时写 `index-<year>.json.gz`；继续读取 v4 平铺 / 分片；`recall --year` 与 `context --year` 只加载命中年份分片；gzip 损坏 fail-closed，不用残缺结果冒充成功。
- 新写入布局：公共 `facts/<yyyy>/<mm>/<dd>/`，私密 `private/<owner>/<type>/<yyyy>/<mm>/<dd>/`；旧平铺与年/月桶继续兼容读取。
- 布局迁移：
  `yotta-memory layout plan [--threshold N] [--include-flat] [--json]`
  → 审阅候选和冲突
  → `yotta-memory layout apply --from-plan <文件> --yes`
  → 出问题时 `yotta-memory layout rollback --batch <id> --yes`。
  apply / rollback 都写 journal；默认只处理超过阈值的年/月桶，旧平铺不迁。
- `doctor --json` 的 `checks.scale` 新增 `index_logical_bytes` / `index_shards` / `index_format` 与 `type_pressure`（总数 / 180 天陈旧 / 归档候选 / 30 天增长）；类型阈值按计划保留观察窗。
- `scan` 精确例外：`security/scan-policy.json` 中每条必须同时匹配规则、文件、整行 SHA-256 与未过期的 `review_by`；内容变化或过期自动恢复命中。`scan --no-policy` 做全量复核；`scan --policy-candidates --out security/scan-policy.candidates.json` 只生成候选，不自动启用。

## 3.12 每用户自启 profile（v0.24.1）

- `yotta-memory lan enable` 在目标用户上下文解析 `memoryHome`、`runtimeHome`、
  `configDir`、`host`、`port` 和 `userId`，写到该用户配置目录下的
  `serve-profile.json`。不同用户的路径互不影响，不是代码或全机器共享常量。
- Windows task XML、Startup 兜底、systemd unit 与 crontab 都引用该绝对 profile
  路径。服务由 S4U 或无用户环境启动时，不再依赖 `os.homedir()`。
- `yotta-memory serve --profile <文件>` 在监听端口前校验 profile schema、
  绝对路径、memoryHome / runtimeHome 是否存在以及 Windows 用户是否匹配；
  校验失败直接退出，不创建 `C:\Users\Default\.yottamemory` 空库。
- `yotta-memory lan status` 显示 profile 中的记忆库和运行时路径，并与当前
  设置比较漂移；旧任务命令缺少 `--profile` 时提示重新执行 `lan enable`。
- 修改 `memory_home`、配置目录或 runtime 路径后，应重新执行
  `yotta-memory lan enable --onstart` 更新 profile 和自启任务。

## 4. 便携记忆盘 · 记忆引擎主机篇

场景：记忆放在一台主机上（Linux / Windows 均可），本机直接 CLI 读写；局域网内其它主机上的 AI 智能体经 MCP 远程接入。引擎主机只需装 CLI，不需要装任何 AI 智能体。

**本机与局域网可同时用同一个记忆库**：引擎 `serve` 运行期间，本机智能体照常用 CLI（或 stdio MCP）读写（不经网络、不需要 token），局域网其它主机的智能体同时经 MCP + token 接入——两条通道并存、互不干扰。

**第 1 步：安装 CLI**（见第 2 节）。

**第 2 步：指定记忆位置并初始化（或接入现有记忆库）**

```bash
yotta-memory config set memory_home /srv/yotta-memory   # 改成你的实际目录
yotta-memory init --dir /srv/yotta-memory               # 新库：初始化（自动建 facts/private/.archive）
```

如果目标目录**已经是记忆库**（里面有 `facts/` 等子目录或 `index.json`，例如从旧机复制或 git 克隆来的），直接 `config set memory_home <目录>` 接入即可，**不要重复 init**。

**第 3 步：注册开机自启（可选，推荐）**

`lan enable` 会先准备稳定运行时入口：没有 `<runtimeRoot>/current` 时自动执行 `runtime install --from-current`，然后把计划任务 / systemd / crontab 指向 `<runtimeRoot>/current/bin/yotta-memory.js`。如需手动准备，可先执行 `yotta-memory runtime install --from-current && yotta-memory runtime status`。

```bash
# Windows：内置命令（优先计划任务——v0.22.4 起 S4U 主体后台静默、不弹窗口；
# 非管理员自动降级用户级 Startup 静默自启；v0.6.3 起启动脚本自愈——启动文件被清理也会在开机时自动重建；
# v0.22.5 起 Electron 宿主（如 YottaCode）自动注入 ELECTRON_RUN_AS_NODE，不再拉起 GUI）
yotta-memory lan enable              # 登录后自动启动（默认）
yotta-memory lan enable --onstart    # 开机即启、无登录会话也可启动（计划任务注册需管理员）
yotta-memory lan status              # 查看状态
yotta-memory lan disable             # 取消

# Linux：内置命令（v0.6.4 起）——优先 systemd 用户单元（登录自启）；
# systemd 不可用时自动降级用户 crontab @reboot（开机自启，免管理员）
yotta-memory lan enable              # 登录后自动启动（默认）
yotta-memory lan enable --onstart    # 开机即启（无需登录，需系统支持 loginctl）
yotta-memory lan status              # 查看状态
yotta-memory lan disable             # 取消
```

**说明**：`lan enable` 默认「登录后自启」；如需系统级（整机、开机即启）服务，可手动创建 systemd 单元 `/etc/systemd/system/yotta-memory.service`（ExecStart 指向 `which yotta-memory` 实际路径），再以管理员执行 systemd 的 enable --now 启用；桌面环境也可在 `~/.config/autostart/` 放置 `yotta-memory.desktop` 实现图形登录自启。

**第 4 步：为局域网其它主机的智能体生成访问 token**

```bash
yotta-memory token new --agent 我的智能体ID
```

命令会打印一次 `ytm_...`，请妥善保管（它就是访问凭证）。多个智能体就重复执行、用不同 ID。**本机上的 AI 智能体不需要 token**（见第 5 篇）。

> token 丢失或要更换：重新执行 `token new --agent <id> --force` 会生成新 token 并覆盖旧的，旧 token 立即失效；不加 `--force` 时若该 ID 已被其它来源占用会被拒绝（每个 AI 的 ID 必须唯一）；`token list` 可查看已登记哪些智能体。

**第 5 步：把连接信息交给远程智能体的用户**

- 引擎地址：`http://<本机IP>:8787/mcp`
- 该智能体的 token：`ytm_...`
- 智能体 ID（对应 X-Agent-Id 请求头）与该智能体的 agent_key（对应 X-Agent-Key 请求头）

查本机 IP：Linux 运行 `hostname -I`（或 `ip a`）；Windows 运行 `ipconfig` 找「IPv4 地址」。防火墙：Linux 若启用了 ufw，执行 `sudo ufw allow 8787/tcp`；Windows 首次监听时允许放行。否则局域网其它主机连不进来。

**第 6 步：备份与迁移**

- 备份 = 复制整个记忆目录（`facts/` `private/` `.archive/` + `index.json` + `agents.json` + `.server/`），其中 `facts/<年>/<月>/` 与 `private/<owner>/<type>/<年>/<月>/` 是分层后的新写入位置；复制到哪、哪就是记忆库，迁移同理，整个目录拷走即可。
- `export` / `import` 是把记忆导出成单个 JSON 或从 JSON 导入，适合跨工具交换或归档，不是日常备份的必需步骤。

## 5. 智能体接入篇（本机 / 局域网其它主机）

接入智能体分两类：引擎主机本机的智能体、局域网其它主机上的智能体。本机不需要 token、不依赖远程服务；其它主机经 MCP + token 接入。

### 5.1 本机 AI 智能体（引擎主机本机）

**方式一（推荐，最简单）：让智能体直接调用 CLI。**

```bash
yotta-memory recall <关键词>            # 智能体开工恢复上下文
yotta-memory remember FACT 主题 内容    # 智能体落盘
```

智能体装上技能后（`SKILL.md`）会自动学会这套工作流，无需任何 MCP 配置。

**方式二：stdio MCP（零常驻进程，智能体按需拉起 CLI）。** 先让 AI 领取 agent_key：

```bash
yotta-memory key status <本智能体ID>
yotta-memory key claim <本智能体ID>
```

领取成功后宿主目录出现 `<AI_HOME>/.yotta-memory-agent-key`；再由 MCP 宿主通过 `--agent-key-file` 读取该文件。然后在智能体 MCP 配置里加：

`AI_HOME` 解析由 `key status` / `key claim` 共用：显式 `--to <目录>` 或 `--agent-key-file <文件>` > `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE` > 宿主默认（Codex `$CODEX_HOME` 或 `~/.codex`、OpenCode `$XDG_CONFIG_HOME/opencode`、通用 `~/.<agent_id>`）；文件名固定为 `.yotta-memory-agent-key`。`key status` 会输出实际检查路径 `checked:` 与命中的发现规则 `discovery:`，即使文件暂不存在也可据此定位。

```json
{
  "mcpServers": {
    "yotta-memory": {
      "command": "yotta-memory",
      "args": [
        "serve", "--stdio", "--tools", "core",
        "--agent-id", "<该智能体唯一ID>",
        "--agent-key-file", "<AI_HOME>/.yotta-memory-agent-key"
      ]
    }
  }
}
```

本机接入不需要网络 token，也不需要启动 HTTP 服务；但**必须用 `--agent-id` 声明唯一的智能体 ID，并用 `--agent-key-file` 指向自己的宿主 key 文件**，否则私密读写会被拒。身份环境变量已删除。

**本机智能体装好技能后如何获取记忆存放位置？** 按优先级：`YOTTA_MEMORY_HOME` 环境变量 > `config set memory_home` 持久化的 `~/.yottamemory/config.json` > 默认 `~/.yottamemory`。AI 开工执行 `yotta-memory config get` 查看当前生效位置；记忆库移动后执行一次 `config set memory_home <新目录>` 即可。

**给本机智能体设置唯一身份（强制）**：私密记忆（PREF / BOUND / COMMIT）按 owner 物理分目录隔离（存于 `private/<owner>/<type>/`），owner 取当前智能体的 agent ID。流程如下：

1. 开工先 `yotta-memory whoami` 确认「我是谁」。
2. 未登记 → 向用户确认一个**全局唯一** ID（建议 `<主机名>-<角色>`，别用 `dashu` / `codex` 这类易撞名），执行 `yotta-memory iam <id>`：引擎**强制唯一性**（被其它主机 / 来源占用会拒绝），并自动落一条「自我接入档案」PREF（owner=自己）。
3. 本机多个 AI 智能体共用引擎时，**每个都要在自己的 MCP 配置里用 `--agent-id` 声明唯一 ID，并用 `--agent-key-file` 指向自己的 key 文件**；HTTP 场景则在请求头写 `X-Agent-Id` + `X-Agent-Key`。CLI 直连每次带 `--agent <id> --agent-key <key>` 或 `--agent-key-file <文件>`。owner ID 单独存在时不构成认证。
4. **禁止**从记忆里读到别人的 ID 就当自己的（比如看到「Kali 智能体 ID 为 dashu」就把自己当 dashu）；不确定先 `whoami` 再问用户，**禁止猜**。
5. **不设则 owner 为空**：写私密记忆会被引擎拒绝（公共 FACT 不受影响），避免私密隔离退化。

### 5.2 局域网其它主机的 AI 智能体

**第 1 步：向记忆引擎主机获取**：引擎 IP、端口（默认 8787）、本智能体的 token 与智能体 ID。若还没有 agent_key，由用户在引擎主机执行 `yotta-memory view` 授权；同机 / 共享文件系统时 AI 用 `key status` / `key claim` 领取到 `<AI_HOME>/.yotta-memory-agent-key`，不共享文件系统时由用户通过密码管理器或安全文件传输放到目标宿主目录。

**第 2 步：配置 MCP**（可以让 AI 按 `SKILL.md` 引导自动完成；也可以手动在你的智能体 MCP 配置里加这段）：

```json
{
  "mcpServers": {
    "yotta-memory": {
      "url": "http://<引擎主机IP>:8787/mcp",
      "headers": {
        "Authorization": "Bearer <TOKEN>",
        "X-Agent-Id": "<本智能体ID>",
        "X-Agent-Key": "<本智能体宿主 key 文件中的 agent_key>"
      }
    }
  }
}
```

**第 3 步：验证**：让 AI 调一次 `recall` / `search`，能读到记忆即连接成功。

**第 4 步：复用**：连接成功后就一直复用；token 失效（被吊销）时回到第 1 步重新获取。

**身份确认与自我档案（强制）**：先调一次 MCP 工具 `agent_info` 确认「我是谁」（读 X-Agent-Id 声明 + 登记状态）。随后用 `remember` 写一条 `subject=自我接入档案` 的 PREF（owner=自己），body 为 `; ` 分隔的 key:value——`agent_id / host / memory_home / mcp_mode: http / engine_url / token`，把接入信息存进自己的永久记忆；下次会话 `recall "自我接入档案"` 直接找回。

## 6. CLI 命令速查

| 命令 | 作用 |
|---|---|
| `yotta-memory init [--project] [--dir <目录>]` | 初始化记忆库 |
| `yotta-memory remember <类型> <主题> <内容> [--owner <id>] [--source <来源>] [--weight <0..>] [--verify] [--no-hint]` | 写入记忆（--source 来源；--weight 重要性权重；--verify 写后回读；--no-hint 关闭类型提示）|
| `yotta-memory recall [关键词] [--type T] [--limit N] [--year <yyyy>] [--agent <id>] [--owner <id>] [--all] [--unsafe] [--explain] [--semantic] [--embedding <命令>] [--embedding-timeout N]` | 检索记忆（语义 + 效用分排序；可选本地 embedding 插件；读取分区过滤；越界读其它智能体私密默认拒绝，需 grant / identity=user / `--unsafe`；v0.17.0 起 `--year` 只检索指定年份，分片索引只读对应分片）|
| `yotta-memory profile [--owner <id>]` | 生成用户画像（零推断，写 `profile.md`）|
| `yotta-memory context [--limit N] [--owner <id>] [--budget N] [--focus <关键词>] [--year <yyyy>] [--explain] [--embedding <命令>]` | 开工上下文包（身份+铁律+画像+长期摘要+任务相关记忆+近期走廊+近期高价值+边界+承诺+会话闭环契约；--budget 控制动态记忆字符预算；--focus 任务聚焦；v0.17.0 起 `--year` 只装载指定年份；--explain 输出 included/dropped 选择解释）|
| `yotta-memory forget <文件>` | 删除一条记忆 |
| `yotta-memory doctor [--json] [--runtime] [--mcp-config <文件>] [--skill-dir <目录>] [--baseline [--against <库路径>] [--template <文件>]]` | 开工可靠性检查（v0.12.2：根目录 / 密钥库 / 索引 / 身份 / 最近备份；严重异常时锁定破坏性写入；v0.16.0：`--runtime` 检查 CLI / current / MCP 配置 / 运行中 server / 技能副本漂移；v0.17.0：`checks.scale` 规模体检 + `--baseline` 恢复 / 迁移六类只读探针，失败列出缺失清单并 exit 2）|
| `yotta-memory index --stats [--json]` | 只读索引统计（存储 / 逻辑体积、字段占比、token、gzip 分片预估；不重建、不改文件）|
| `yotta-memory layout plan [--threshold N] [--include-flat] [--out <文件>] [--json]` / `layout apply --from-plan <文件> --yes` / `layout rollback --batch <id> --yes` | 日级目录重平衡：预演候选与冲突、按 journal 执行、失败逆序回滚、按批次恢复原布局 |
| `yotta-memory archive [--days 180] [--threshold 0.4] [--dry-run] [--force] [--json]` | 归档旧记忆（分类型衰减效用分 + 年龄；immutable / BOUND 豁免，默认豁免冷却期与 `evergreen` / `pinned`、`--force` 覆盖；保留年/月分层，私密入 `.archive/private/<owner>/<type>/<年>/<月>/`）；`--dry-run` 零写入预览 |
| `yotta-memory reindex` | 重建索引 |
| `yotta-memory identity remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity] [--password <口令> | --recovery-key <钥匙>]` | 彻底删除一个 AI 身份与私密记忆（v0.17.0：真删身份登记 / owner 密钥 / 授权绑定 / 待领取 key / 缓存 / `private/<id>/` / token / grants 并重建索引 + 写审计；公共明文 FACT 保留、其它 AI 零影响；只能由用户本人执行，`view` 里也有「删除」按钮；破坏性闸门 = doctor + 独立备份 + 事务快照）|
| `yotta-memory export [--out 文件.json]` / `import <文件.json>` | 导出 / 导入 |
| `yotta-memory config set <键> <值>` / `config get [--json]` | 记忆库位置与引擎参数（`memory_home` / `embedding_cmd` / `embedding_timeout` / `maintain_archived_utility` / `maintain_decay_halflife_<TYPE>` / `consolidate_*` / `scale_*` 等；`get --json` 同时返回身份状态）|
| `yotta-memory whoami --agent <id> [--json]` | 查看当前显式身份与登记状态；身份不从环境变量读取；`--json` 返回结构化身份状态 |
| `yotta-memory iam <id> [--name <显示名>] [--user <用户名>] [--relationship <关系>] [--force]` | 登记本智能体唯一身份并自动落自我档案（`agents.json`，ID 必须唯一；可选扩展显示名 / 用户 / 关系）|
| `yotta-memory token new --agent <id> [--force]` / `token list` / `token revoke --agent <id>` | 访问 token（同 ID 已被其它来源占用需 `--force` 覆盖）|
| `yotta-memory serve [--port 8787] [--stdio] [--no-auth]` | 启动记忆引擎（--no-auth 关闭鉴权，仅限可信内网）|
| `yotta-memory runtime list / install <tarball|版本> [--from-current] [--force] / use <版本> [--restart] / rollback [--restart] / status` | 运行时稳定入口（runtime.json + versions + current；安装 / 切换 / 回滚 / 查看漂移；`--restart` 尝试重启受管 server）|
| `yotta-memory lan enable [--onstart] / disable / status` | 开机自启管理（Windows：计划任务/用户级 Startup 静默自启；Linux：systemd 用户单元/用户 crontab @reboot）|
| `yotta-memory feedback <文件|主题> --useful|--useless [--reason <原因>] [--undo]` | 使用反馈（v0.8.0：useful/useless 调 weight/confidence/feedback_net；--undo 回滚）|
| `yotta-memory maintain [--dry-run] [--apply] [--purge] [--threshold N] [--age N] [--dedup] [--dedup --apply] [--merge A,B] [--capacity [--json]] [--rules]` | 记忆自组织（v0.8.0 + v0.10.0 自动合并 + v0.18.0 容量水位 + v0.18.1 规则晋升）：归档 / 遗忘候选 / 置信度查重 / 自动合并；默认 dry-run，`--dedup` 与归档互斥；`--capacity` 只读报告水位、LRU / LFU 候选与晋升建议；`--rules` 只读输出重复踩坑 → 建议升级为规则的清单（不自动写 BOUND） |
| `yotta-memory consolidate [--min-age N] [--min-idle N] [--max-utility N] [--min-group N] [--period N] [--type T] [--model <cmd>] [--apply] [--yes] [--undo <batch>] [--batches]` | 周期摘要压缩（v0.10.0 起：同主题旧记忆 → 带溯源摘要 + 原文归档；v0.18.0 起默认等价 `--propose` 只出报告，`--apply` 非交互必须 `--yes`；v0.18.1 起摘要正文按条目 `created` 绝对化相对日期，归档副本写巩固标记，`--undo <batch>` 剥离标记并回滚；`--batches` 查批次）|
| `yotta-memory distill [--owner <id>] [--subject <主题>] [--model <cmd>] [--out <路径>] [--json]` | 心理日志蒸馏（v0.8.0 统计摘要 / 主题画像 / 知识地图 + v0.18.1 分类型提取清单 / 质量指标 / 跳过与边界；每条带 `[溯源: 文件#L<a>-L<b>]`；`--json` 结构化输出）|
| `yotta-memory explain <文件|主题>` | 查看单条记忆效用分项（v0.8.0）|
| `yotta-memory bench [--evalset <文件>] [--k N] [--seed N] [--bootstrap N] [--ablate] [--gate <指标>=<数值>] [--timing] [--year <yyyy>] [--json] [--out <文件>]` | 可复算检索基准评测（v0.17.0：默认按库内条目确定性抽样；`--evalset` 指定评测集 v1；指标 Recall@k / MRR / nDCG@k / HitRate + 95% 置信区间；报告含库指纹、默认不含墙钟时间；`--ablate` 消融对比；`--gate` 供 CI；`--timing` 附带耗时后不可逐字节复算；全程只读）|
| `yotta-memory scan [--path <目录>] [--gate <安全级别>] [--no-policy] [--policy-candidates] [--out <文件>] [--quarantine --yes] [--restore] [--id <批次>] [--json]` | 记忆库安全扫描（v0.17.0：七类 + 五级 + `file:line` 证据；默认只报告；`--gate` 命中该级别及以上 exit 1；v0.24.0 起支持精确规则 + 文件 + 行哈希 + 有效期例外；`--no-policy` 全量复核；`--policy-candidates` 只生成候选；`--quarantine` 需 `--yes` 或交互确认；`--restore` 还原；凭证片段打码不回显）|

类型：`FACT`（事实，共享）/ `PREF`（偏好）/ `BOUND`（边界）/ `COMMIT`（承诺），后三类按智能体物理分目录隔离（`private/<owner>/<type>/`）；v0.24.0 起新写入按日级桶（`facts/<年>/<月>/<日>/`、`private/<owner>/<type>/<年>/<月>/<日>/`），旧平铺与年/月桶继续可读，默认不自动迁移。

## 7. 故障排查

**远程连不上时，按顺序检查：**

1. 引擎在运行吗？`yotta-memory lan status`（Windows / Linux 通用）；Linux 也可 `systemctl --user status yotta-memory-serve.service`（systemd 自启时）或 `ps aux | grep yotta-memory`；也可直接 `yotta-memory --version`。
2. IP 对吗？引擎主机执行 `hostname -I`（Linux）或 `ipconfig`（Windows）确认。
3. 端口对吗？默认 8787，两端要一致。
4. 防火墙放行了吗？Linux：`sudo ufw status`，未放行则 `sudo ufw allow 8787/tcp`；Windows：允许首次监听的入站请求。
5. token 有效吗？记忆盘主机执行 `yotta-memory token list` 看该智能体是否登记；无效就 `token new --agent <id>` 重新生成。
6. 网络通吗？任意一台主机用浏览器或命令行访问 `http://<引擎IP>:8787/mcp`：
   - 返回 401：服务在运行，是鉴权问题（token / 请求头不对）。
   - 连接被拒 / 超时：服务没启动，或防火墙拦截。

**`lan enable` 计划任务被拒（Access denied 等）：** 无需担心——会自动降级为**用户级 Startup 静默自启**（免管理员，重新登录后生效，启动脚本位于用户 Startup 目录）；如确需计划任务，请用管理员终端重新执行；`--onstart` 模式必须管理员。

**启动引擎报端口被占用（EADDRINUSE）：** 用 `--port <其它端口>` 换端口启动，两端保持一致；或先查占用：Linux `ss -tlnp | grep 8787`，Windows `netstat -ano | findstr 8787`。

**recall 没有结果：** 关键词太细或确实没有这条记忆；先 `recall`（不带关键词）看库里的全部记忆核对。

**systemd 自启的引擎看日志：** `journalctl --user -u yotta-memory-serve.service -n 50`（系统级手动服务为 `journalctl -u yotta-memory -n 50`）。

**记错位置了？** `yotta-memory config get` 查看当前生效位置；`config set memory_home <正确目录>` 改正。

## 8. 安全与边界

- token 等同密码：只给需要接入的智能体，别外传。
- 私密区机制级加密（v0.7 起）：PREF / BOUND / COMMIT 私密记忆默认落盘为密文（AES-256-GCM 信封加密），任何没有对应 owner 密钥的 AI 即使读到密文文件也解不开；隔离 = 权限边界（scope/owner）+ 机制层机密保护。用户是数据所有者，经 `yotta-memory view` 口令解锁可看全部。
- 记忆读写一律走 CLI / MCP；禁止用 shell（`Get-ChildItem` / `cat` / `ls` / `type` 等）直接读改记忆库目录下的文件——否则会绕过 scope/owner 权限边界。
- 管理动作（init / config / token / lan / serve）不通过 MCP 暴露，远程只能读写记忆（路径限记忆库内，export/import 的 out/src 必须落在库内；distill 不支持 `--model`，仅本地 CLI），不能改配置、不能管 token。
- `--no-auth` 会关闭鉴权，仅限可信内网使用。
- 数据主权在用户：公共 FACT 明文、随时可看可改可删；私密区加密，用户经 `yotta-memory view` 口令解锁后同样可看、可改、可删、可导出。
- 「记忆守则」内置底线：陪伴不操控 / 理解不越界（不贴标签）/ 诚实不伪装 / 不降格；数据安全（被遗忘权 = `forget`）；宿主隔离（只写本记忆库，不读写宿主 AI 自身 memory / 配置 / 系统文件）。

**确实需要读取其它智能体的私密记忆时（三种授权方式，满足任一即可）：**

1. 显式授权 `grants.json`：在记忆库根目录写 `{"<你的agentID>": ["<对方agentID>"]}`；
2. identity=user：以 `--agent user` / `--owner user` 读取，调用方仍需持有匹配的 agent_key；
3. 显式放行 `--unsafe`：用户明确同意时使用。

**协作纪律**：FACT 写入公共区共享；PREF / BOUND / COMMIT 只写自己的私密区；不主动读取其它智能体的私密记忆。
