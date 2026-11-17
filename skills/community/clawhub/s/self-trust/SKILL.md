---
name: self-trust
description: >
  个人自律记账与资金治理的确定性引擎（规则代码，非 AI 推断）：支出审批+冷静期、预算目标与奖励、月报校准、对账、债务/房贷建模、多币种、可选 AES-256-GCM 加密账本。触发：记账/账本/预算/存钱/FIRE/消费审批/对账/债务/房贷/审计。

  Self-trust — a deterministic personal-finance discipline engine (rule code, not AI inference): spending approval + cooldown, budget goals & rewards, monthly calibration, reconciliation, debt/mortgage modeling, multi-currency, optional AES-256-GCM encrypted ledger. Triggers: bookkeeping / ledger / budget / saving / FIRE / spend-approval / reconciliation / debt / mortgage / audit.
---

# self-trust（自律记账引擎）

规则引擎是**确定性 Python 代码**，不是 AI。你（LLM）只做三件事：
1. 解析用户自然语言意图 → **按 `references/interaction.md` 预处理**（类目映射/金额解析/planned 推断/request_id 继承）→ 映射到下方命令；
2. 调 `scripts/cli.py` 对应子命令（**一律输出结构化 JSON**：判定 + 全部中间变量）；
3. 把引擎 JSON 润色成意见书/回执（措辞放开，数字锁死）——**渲染规则见 `references/rendering.md`**（先按 §1.1 选模板、套 §0.5 骨架）；`templates/` 仅字段路径速查，**格式以 `rendering.md` 为准、禁止照抄旧示例、禁止看 JSON 自编文案**。

## 铁律（不可违反）

1. **禁止心算公式**：F0~F8 一律由引擎计算；任何金额、月数、比例、阈值**必须原样引用引擎 JSON 输出**，不得自行推算、四舍五入改数、或"大概估一下"（§8.3 #1：cli.py 输出判定+中间变量，LLM 只润色不心算）。
2. **禁止代替引擎判定**：批准/附条件/驳回只认 `decision.result`；不得因用户恳求而改口（§4.2 长期优先原则）。
3. **禁止写配置区**：契约核心参数（安全垫/目标/invest_ratio 等）修改必须走 §5.4 二次确认闸门；引擎/LLM 均无权静默改（§10.3 三区权限）。
4. **误差披露**：简化口径（F5）数字须用「约/大约/估算」措辞，并附「长期目标以真实口径（F7）为准」（§2.0）。
5. **性质声明**：涉及"信托/资产保护/法律"话题时，明确本工具无法律效力（§0）。
6. **输出前必须按路由表实际打开对应 `references/*.md`**：渲染类必读 `rendering.md` 并套其 §0.5 骨架；预处理类读 `interaction.md`。**禁止凭记忆作答，禁止把为 A 目的读过的文件当成 B 目的的权威源**。
7. **引擎 message/note 串须全中文、禁露字段名/枚举值**：引擎模块产出的所有用户可见字符串（`message`/`note`/`warning`/`summary`）必须为全中文；禁止将字段名（如 `monthly_history`/`invest_ratio`/`override_log`）或枚举常量（如 `imported_pending`/`imported_confirmed`/`manual`）直接暴露给用户——代码内须做中文映射后再拼接（详见 `rendering.md §0.7`）。

## 命令表（§9）

> **交互预处理**（类目映射 / 金额解析 / planned 推断 / request_id 上下文继承 / 多笔拆分 / 引导初始化）见 `references/interaction.md`——调引擎前先按规则消解模糊性。

| 用户说 | 引擎命令（用途 + 最小调用） | 参考 |
|---|---|---|
| 记账初始化 | 懒人一键建契约：`python scripts/cli.py init --corpus 200000 --monthly 8000 --objective "FIRE:3000000:2036-01-01"`（`--objective` 可重复 1~3 个；`--currency USD` 可选默认 CNY；**`--encrypt [--crypto-mode passphrase\|keyfile]`** 可选启用静态加密，默认关） | references/init.md |
| 审查：买X花Y / 记账审批 | §4.4 判定+冷静期入队+F8 快照：`python scripts/cli.py judge --amount 6000 --category 合理享受 [--planned]`（外币消费加 `--currency USD --rate 7.25`） | references/approval.md |
| 记账撤回 | 冷静期撤回+正向激励测算：`python scripts/cli.py judge --action withdraw --request-id <id>` | references/approval.md |
| 记账确认执行 | 到期前确认终裁：`python scripts/cli.py judge --action finalize --request-id <id>` | references/approval.md |
| （调度）到期终裁 | 过期申请按原判定收尾：`python scripts/cli.py judge --action expire [--request-id <id>]`（省略 id 处理全部到期项） | references/approval.md |
| （调度）冷静期提醒 | 双阶段提醒数据：`python scripts/cli.py judge --action reminders` | references/approval.md |
| 融资购房审查 | 大额资产购买拆**首付(打 liquid)+房贷(变负债+月供)**评估：`python scripts/cli.py judge --amount 1000000 --category 投资 --financed-amount 700000 [--financed-term-years 30] [--financed-rate 0.04]`（判定看①首付是否击穿流动安全垫②月供是否≤月度净流入；首付=总额-贷款） | references/approval.md |
| 记账申诉 | 同一逻辑重审+计数：`python scripts/cli.py appeal --request-id <id> --reason "理由"` | references/exceptions.md |
| 记账覆写（满 3 次申诉） | 人工兜底放行：`python scripts/cli.py appeal --request-id <id> --override --confirm` | references/exceptions.md |
| 记账报表 | 双轨进度条+趋势+当月快照：`python scripts/cli.py report` | references/report.md |
| 记账校准 | 月度校准（同月幂等）：`python scripts/cli.py calibrate [--force]` | references/report.md |
| 记账奖励 | 状态：`python scripts/cli.py reward`（默认 `--action status`）；解锁：`--action unlock`；支取：`--action claim --objective FIRE --amount 2000 --purpose "犒劳"` | references/report.md |
| 目标完结/归档 | 用户显式迁移：`python scripts/cli.py objective --name FIRE --to completed\|archived --confirm` | references/report.md |
| 记账对账 | hybrid 用户拍板修正：`python scripts/cli.py reconcile [--corpus 元] [--income 元] [--invest 元] [--living 元] [--impulse 元]`。**审批通过的支出不自动改 corpus（corpus 属配置区、引擎最小权限）；改为记入运行时 `pending_spends` 台账，对账时并入并清空**（返回 `pending_spends_cleared` 笔数/合计），故每月对账即「把已批支出销账 + 重锚真实基数」 | references/data-modes.md |
| 记账重置 | 二次确认整文件重建（audit 保留）：`python scripts/cli.py reset --confirm --corpus 元 --monthly 元 --objective "名:目标额:期限" [--reason "..."]` | references/exceptions.md |
| 记账自定义 | 增量覆盖契约配置区参数（§5.4 二次确认）：`python scripts/cli.py customize --set distribution_rules.invest_ratio=0.3`（预览返回 token）→ 同一变更加 `--confirm --token <token>` 落盘；支持 `--set`（嵌套 DOTPATH，含 `safety_cushion.months` / `optimization_goal` / `mode`）/ `--add-objective "名:额:期限"` / `--whitelist-add 名称 --per-tx-cap 元 --annual-cap 元` / `--whitelist-remove 名称`。**§5.4 冷却窗**：`safety_cushion.months` 下调 / `invest_ratio` 下调等「削弱自身」修改，确认后进入 **1 个自然日**冷静窗（`pending_config_changes`），窗内可无理由撤回、到期自动生效，不立即落盘；其余修改（含上调护栏）立即生效 | references/exceptions.md |
| 记账模式 | 切换全局优化调度（记账自定义子集）：`python scripts/cli.py customize --set optimization_goal wealth\|balanced\|objective`（核心护栏字段，触发 §5.4 风险提示） | references/exceptions.md |
| 记账切模式 | 切换数据存储模式：`python scripts/cli.py customize --set mode ledger\|conversational\|hybrid`（非核心，普通确认） | references/data-modes.md |
| 记账自定义·撤回 | 冷却窗内无理由撤回：`python scripts/cli.py customize --withdraw --request-id <id> --token <撤回token>`（撤回 token 在确认时返回） | references/exceptions.md |
| 记账自定义·复查 | 冷却窗复查（懒惰扫描过期项自动生效 + 列窗内待决 + 二次提醒）：`python scripts/cli.py customize --review` | references/exceptions.md |
| 记账日志 [类型] | 审计只读查询：`python scripts/cli.py log --name approval_log\|appeal_log\|override_log\|reward_log\|monthly_history` | references/report.md |
| 记账演示 | 三场景真实干跑（不落盘不影响真实账户）：`python scripts/cli.py demo`（init 回执也自动附 demo 区块） | references/init.md |
| 记账白名单 加/删 | 极速审批应急类目管理（记账自定义子集）：`python scripts/cli.py customize --whitelist-add 名称 --per-tx-cap 元 --annual-cap 元` / `--whitelist-remove 名称`（核心护栏字段，触发 §5.4 风险提示） | references/exceptions.md |
| 记账负债/刚性支出 增删 | 负债与刚性年支出建账（如实上报，影响净资产口径）：`python scripts/cli.py customize --add-liability "房贷:800000:5000:0.04"` / `--remove-liability 房贷` / `--add-rigid "保费:12000:3"` / `--remove-rigid 保费` | references/exceptions.md |
| 记账记录购房 | 已购房产落账（首付打 liquid + 房贷变负债）：`python scripts/cli.py customize --record-home-purchase "1000000:0.3"`（房价:首付比例[:期限年[:利率]]；确认后 corpus-=首付、liabilities 追加房贷及月供） | references/exceptions.md |
| 记账类目 增删 | 支出类目词汇表（`allowed_categories`，嵌套于 distribution_rules）：`python scripts/cli.py customize --add-category 园艺` / `--remove-category 园艺`（去重追加 / 移除，缺失报错；核心护栏字段，触发 §5.4 二次确认，但因不改 invest_ratio 不进冷却窗）。**标准类目已内置 23 项**（食品/居住/交通/通讯/医疗/教育/服饰/日用/合理享受/娱乐/旅行/社交/宠物/数码家电/保险/房产/车辆/投资/理财/基金/股票/黄金/其他），新增仅需补「标准外」个性化类目；投资理财组仅作资金去向标签、`房产/车辆` 为大额购置（与 `居住`/`交通` 日常支出区分），`invest_ratio` 投资机制不受影响；judge 当前不强制校验 `--category` 是否在其内（自由文本 + 词汇表作推荐）；如需硬约束见 STATUS 待定项 B | references/exceptions.md |
| 第三方导入 [工具名] | CSV/手动拉取资产并**人工核对**后生效（§7.3，数据中立硬约束）：`python scripts/cli.py import-asset --balances <csv> [--flows <csv>] [--source 钱迹]`（暂存→返回 token + 摘要 + 可疑流水）→ 核对修正后 `import-asset --confirm --token <token>` 落盘（corpus_status: imported_pending→imported_confirmed）；放弃 `import-asset --cancel --token <token>`。无 CSV 可手动：`import-asset --corpus 150000 --monthly 8000 --liabilities "房贷:700000:3341.91" --rigid "保费:6000"`。导入待核对（imported_pending）锁定全部审批，跳过核对不得审批。**导入语义**：CSV 须为**完整快照**（资产/负债/刚性全部列齐，确认=全量重基线，缺类不会清空已录入项）；手动 `--corpus/--monthly/--liabilities/--rigid` 为**局部修正**（只覆盖显式传参的分类，其余 live 原值保留）。**同名账户自动去重**：同一 `(账户名, 类型)` 在 CSV 重复列出时按同账户合并——完全重复行静默丢弃，同名异额行求和并告警，不再双倍计入资产/负债（§H1 修复）。**CSV 格式更宽容（M2/M3）**：余额/月供/流水金额支持币种符号（¥ $ ￥）与千分位逗号；流水日期支持 `年-月-日 / 年/月/日 / 年.月.日 / 年-月`；rigid 行可附 `due_month` 列（1–12）标注到期月。**部分负债/刚性修正合并**：确认时若只修正部分条目（按 name），未提及项保留、不整表覆盖（M6 修复） | references/data-modes.md |

**全局参数**（所有子命令通用，只说明这一次）：
- `--data-dir <path>`：数据目录（优先级：命令行 > `SELFTRUST_DATA_DIR` > 默认 `<home>/.claw/self-trust/`）；
- `--today YYYY-MM-DD`：覆盖当前日期（测试/重放用，日常勿传）；
- `--pass <密码>` / `--key-file <路径>`：加密契约密钥（passphrase / key-file 二选一，须置于子命令前）；亦可用环境变量 `SELFTRUST_PASS` / `SELFTRUST_KEY_FILE`；非加密契约无需传；
- 输出恒为 JSON（`--json` 为默认且唯一格式）；失败时 `{"ok": false, "error": ..., "message": ...}` + 非零退出码（2=not_found / 3=guard 权限违规 / 4=invalid 参数 / **5=crypto 加密（缺密钥或密码错误）** / **6=contract_corrupted 契约损坏（拼接/截断 JSON，见 `.bak.corrupt` 恢复，勿重跑）**）。

## 静态加密（密码）用法

opt-in，**默认关**。启用后本地契约（`contract.json`）与审计日志（`audit/*.jsonl`）以 AES-256-GCM 加密落盘；非加密契约行为完全不变，向后兼容。

**两条密钥路线（初始化时一次性决定，之后不可原地切换）**
- `passphrase`（默认）：用户口令，每次命令前传 `--pass <密码>`（或环境变量 `SELFTRUST_PASS`）。密钥由口令经 PBKDF2-HMAC-SHA256（20 万轮）派生，**从不写入磁盘**——无口令即无法解密。
- `key-file`：首次 `init --encrypt --crypto-mode keyfile` 自动生成 `<data-dir>/.self-trust.key`（权限 600），后续命令**自动定位、无需每次传参**；但密钥文件丢失 = 数据永久不可解密，务必单独备份。

**启用（仅初始化时可开）**
```
python scripts/cli.py init --corpus 200000 --monthly 8000 --encrypt --crypto-mode passphrase
python scripts/cli.py init --corpus 200000 --monthly 8000 --encrypt --crypto-mode keyfile
```

**启用后，每次命令都要带密钥**（全局参数，须置于子命令之前）
```
python scripts/cli.py --pass <密码> judge --amount 100 --category 食品
python scripts/cli.py --key-file <路径> report
```
- 缺密钥 / 口令错误 → 退出码 5（`error=crypto`）；引擎返回清晰提示，不会静默用明文读写。
- 切换加密状态（开→关 / 换路线）：需 `reset --confirm` 后重新 `init`，现有契约不原地改密。

详细机制与恢复：references/init.md §4；可选依赖 `cryptography` 见上方「依赖」。

## references 加载路由（按需读，别全读）

| 用户动作 | 读 |
|---|---|
| **用户交互预处理（所有命令）** | **references/interaction.md**（上下文继承 + 类目映射 + 引导初始化 + 金额解析 + planned 推断 + 主动提醒 + 多笔审批） |
| **输出渲染（所有命令）** | **references/rendering.md**（全场景模板选择 + 字段映射 + 省略清单 + 错误渲染） |
| 日常小额审批（最高频） | rendering.md §1 + §11（紧凑卡片 A-1/A-3；有冷静期回退 §1.4 长模板） |
| 审批有分歧/冷静期/白名单 | references/approval.md + rendering.md §1.4（B/C 长模板） |
| 申诉/覆写/护栏修改/重置（低频） | references/exceptions.md + rendering.md §9/§10 |
| 初始化/演示 | references/init.md + rendering.md §3/§4 |
| 报表/校准/奖励/目标生命周期/日志 | references/report.md + rendering.md §5/§6/§7/§8（templates/report.md 仅字段参考） |
| 切模式/切数据源/对账 | references/data-modes.md + rendering.md §10 |
| schema/权限排障 | references/contract-schema.md |

> **渲染优先级**：引擎 JSON → rendering.md 选模板/规则（套 §0.5 骨架）→ 输出用户可见文本；`templates/` 仅字段路径速查，不参与格式。
> rendering.md 是输出格式**唯一权威源**；`templates/` 仅作字段映射速查（字段名→JSON 路径），不得照抄其旧格式示例。
> ⚠️ **硬约束（每次输出前）**：按本表「用户动作 → 读」**重查并实际打开**对应文件，**不依赖记忆、不复用为其他目的读过的文件**；渲染类输出一律走 `rendering.md`（templates/ 仅字段参考），预处理类走 `interaction.md`。

## 模板（仅字段路径速查）
`templates/*.md` 仅字段名→JSON 路径映射；**格式一律以 `references/rendering.md` 为准，禁止照抄其旧示例**。对应章节：opinion→§1/§1.4/§11，report→§5，demo→§4。

## 状态

**已实装能力**：初始化→审批→冷静期→报表→校准→奖励→申诉/覆写→重置→对账 核心闭环；演示干跑；记账自定义（模式/白名单/类目/冷却窗）；负债与房贷建模；第三方导入（CSV/手动，人工核对落盘）；支出类目词汇表；多币种；可选 AES-256-GCM 静态加密。实现进度与测试覆盖见 `STATUS.md`。

## 依赖

- 核心引擎纯标准库，**无第三方依赖**即可运行（init/judge/report/... 全部可用）。
- **静态加密功能（opt-in）需 `cryptography`**：仅当用户启用 `init --encrypt` 时才需要；未安装时引擎返回清晰错误 `加密功能需安装 cryptography：pip install cryptography`。安装：`pip install cryptography`。
