# version-decide — 双报告驱动的优化方案（v1.0.0 审计后）

> 输入：ClawHub 安全审计报告（`version-decide-1.0.0-security-audit.zip`，2026-10-14）
> + SkillHub TRACE 评测报告（skillId=275900, versionId=424723）。
> 目标：提升 **① 代码安全性** 与 **② 代码质量**，逐条落到具体文件/函数。
> 全部条目已对现有代码实跑复核（含负向用例），非臆测。

---

## 一、审计结论快照

| 报告 | 结果 | 说明 |
|---|---|---|
| ClawHub aig / clawscan / static-analysis / virustotal | **clean** | 无隐藏执行/外传/持久化/破坏性行为 |
| ClawHub SkillSpector | `suspicious` / 机械式 `DO_NOT_INSTALL` (score 95) | 与 v0.2.0 同型的「顶层 pass vs 底层 CRITICAL」矛盾误报；TP4/AE1/LP1 均已被 clawscan 判定为 **expected/downgraded** |
| SkillHub TRACE | trust=5.0（scan 双实验室无 P0/P1）、effectiveness≈4.8 | **质量短板 = `reliability.errorHandling` 4.5 与 `reliability.stability` 4.5** |

**可执行项（非误报）**：

- **SDI-2**（MEDIUM）：`references/i18n-plan.md` 的 P6/P7 行混入「跑发布门禁 / 打 tag / 推远端 / 建 Release」等**发版管理**能力，超出「版本判定」技能范围。
- **SQP-3**（LOW）：`measure_skill.py` 用户面向 print 仍**纯中文**（L59-90）。
- **TRACE 质量短板**：`errorHandling` 提示「版本格式错误仅给规范条文、未针对具体输入给精准修正建议」「语言检测静默回退、未显式告知」；`stability` 提示「无超时/重试（本地脚本非关键）」。
- **结构提示**：`measure_skill.py`/`test_semver_check.py` 若能在 `_meta.json`/frontmatter 显式声明为「维护工具」更清晰（缓解 TP4 残留误报）。

---

## 二、安全性优化

### S1. 加固 `load_locale()`：把「locale 文件损坏/未知语言」从崩溃降为可回退
- **问题描述**：`load_locale()`（`scripts/semver_check.py` L54-63）只 `except FileNotFoundError`。
  已实跑确认：`en.json` 损坏（`JSONDecodeError`）或走 `xx.json→en.json` 回退路径时**直接崩溃**；
  且当 locale 缺键时 `_()` **静默返回裸 key**（L70-78 无日志）。这是 `reliability.stability` 扣分点
  的实际根因，也属于「输入验证 + 敏感数据（自带数据文件）完整性」缺口。
- **涉及文件/函数**：`scripts/semver_check.py` `load_locale`、`_`。
- **推荐修改**：
  1. `load_locale` 同时捕获 `(FileNotFoundError, json.JSONDecodeError, ValueError)`，
     回退到内嵌的**英文默认串表**（把当前 en.json 关键键固化为代码内兜底常量），保证任何
     locale 损坏都不阻断决策主流程。
  2. `_()` 命中缺键时，除返回 key 外，向 **stderr** 写一条 WARN（`sys.stderr.write`），
     不污染 stdout 的 JSON 输出，便于排障且不破坏机器可读性。
- **优先级**：**P0**（唯一会导致整技能崩溃的路径；本地零网络脚本，崩溃即不可用）。

### S2. 给 CLI 失败路径补充「针对输入」的精准修正建议（防误用）
- **问题描述**：`main()`（L456-541）对 `BadVersion` 只回 `ERR_BAD_VERSION_SYNTAX`（规范条文），
  TRACE 明确指出「未针对具体输入给精准修正建议」。输入校验偏粗——例如 `1.2`（两段）与
  `01.2.3`（前导零）都笼统报同一句，新手看不出**差在哪**。
- **涉及文件/函数**：`scripts/semver_check.py` `Version.parse` / `_PRE_RE` / `main` 的
  `except BadVersion` 分支。
- **推荐修改**：在 `BadVersion` 异常上带一个**子原因标签**（`leading_zero` / `wrong_segment_count`
  / `trailing_hyphen` / `empty` …），`main` 按标签选对应的修正提示 locale 键（如
  `ERR_FIX_LEADING_ZERO`、`ERR_FIX_SEGMENT_COUNT`），实现「针对输入」的精准纠错。
- **优先级**：**P1**（质量/可维护性，直接抬升 `errorHandling`；纯本地、无安全风险）。

### S3. 权限声明一致性（LP1 / SDI-2 残留）
- **问题描述**：扫描器对「`env` 能力未在 allowed-tools 声明」「读 locale 环境变量」反复报 LP1。
  v1.0.0 已加 `metadata.openclaw.requires.envVars: [LC_ALL,LC_MESSAGES,LANG]` 与 Capabilities 小节；
  但 `allowed-tools: …Bash(python*)` 相对 `git tag`/`cat` 等**只读发现**示例仍偏宽（SDI-2, conf 0.80）。
- **涉及文件/函数**：`SKILL.md` frontmatter `allowed-tools`。
- **推荐修改**：把 `Bash(python*)` 收窄注释为「仅用于运行本技能自带 Python 脚本与只读版本发现命令
  （`cat`/`grep`/`git tag`）」，或拆成 `Bash(python*)` 只保留脚本执行、发现命令显式标注只读。
  同时在前置 metadata 补一句「本技能不授予、也不建议授予写/网络/包管理权限」。
- **优先级**：**P2**（权限最小化声明；不影响运行，主要是消除扫描器重复告警 + TRACE trust 加固）。

### S4. 将「发版管理」文档与「版本判定」运行时隔离（SDI-2）
- **问题描述**：`references/i18n-plan.md` P6/P7（L121-122）与 §10 记录「跑门禁/打 tag/推远端/建
  Release」，被扫描器判定为超出技能范围的**发版管理能力**。
- **涉及文件/函数**：`references/i18n-plan.md`（含 §10）。
- **推荐修改**：在该文档顶部加显式声明块——「本文档是**维护者历史/计划记录，非运行期指令**；
  发布、打 tag、推送、建 Release 属人工操作，本技能的 `allowed-tools` 不授予、`semver_check.py`
  从不执行这些动作」。把 release 步骤与「版本判定」核心明确分栏，避免被读成越权指引。
- **优先级**：**P2**（纯文档，消除 MEDIUM 级 SDI-2）。

---

## 三、代码质量优化

### Q1. `measure_skill.py` 双语/可配置输出（SQP-3）
- **问题描述**：`measure_skill.py`（L59-90）print 全中文，`_meta.json` 亦无「这是维护工具」声明。
- **涉及文件/函数**：`scripts/measure_skill.py` `main` 的 print。
- **推荐修改**：输出默认英文（与 SKILL.md English-default 一致），中文保留为注释或 `--zh` 开关；
  并在脚本首行 docstring 已标注 DEV/MAINTENANCE-ONLY 的基础上，补一句「language: en by default」。
- **优先级**：**P3**（LOW，纯可读性）。

### Q2. 语言检测结果显式化（TRACE `errorHandling` 4.5 的第二扣分点）
- **问题描述**：`--lang auto` 静默回退 en，用户无从得知实际用了哪种语言。
- **涉及文件/函数**：`scripts/semver_check.py` `main`（L496-497）。
- **推荐修改**：当走 auto 且命中回退（未检出 zh）时，在 **stderr** 提示一行
  `note: lang=auto → en (no zh* locale detected)`；显式 `--lang` 时不提示。不影响 stdout JSON。
- **优先级**：**P2**（低成本、直接抬升 `errorHandling`）。

### Q3. 缺失项日志统一走 stderr，stdout 保纯 JSON（可维护性/机器可读）
- **问题描述**：当前 `_()` 缺键静默、locale 回退无迹可循；若日后加告警需避免污染 JSON stdout。
- **涉及文件/函数**：`scripts/semver_check.py` `_` / `load_locale` / `main`。
- **推荐修改**：约定「诊断信息一律 stderr、结果一律 stdout」；S1/S2/Q2 的提示都遵守此约定，
  并在模块 docstring 补一行该约定。
- **优先级**：**P2**（与 S1/S2/Q2 联动，一次落地）。

### Q4. 补充针对上述改动的回归测试（可维护性护栏）
- **问题描述**：现有 37 项测试未覆盖「locale 损坏回退」「未知语言回退」「BadVersion 子原因」
  等新行为。
- **涉及文件/函数**：`scripts/test_semver_check.py`。
- **推荐修改**：新增 `TestRobustness`：① 临时写坏 en.json 断言不崩且返回英文默认；② `xx` 语言
  回退 en；③ `01.2.3`/`1.2` 各命中对应子原因标签。保持跨语言「reasons 变、next/level 不变」断言。
- **优先级**：**P1**（保证 S1/S2 改动零回归）。

---

## 四、优先级汇总（建议实施顺序）

| 序 | 条目 | 方向 | 优先级 | 影响 |
|---|---|---|---|---|
| 1 | **S1** locale 损坏/未知语言回退 + 缺键 stderr 告警 | 安全+稳定 | **P0** | 消除唯一崩溃路径 |
| 2 | **Q4** 配套回归测试 | 质量护栏 | **P1** | 保证改动零回归 |
| 3 | **S2** BadVersion 子原因 → 精准修正建议 | 质量/安全 | **P1** | 抬升 errorHandling |
| 4 | **Q2/Q3** 语言检测显式化 + stderr/stdout 分道 | 质量 | **P2** | 抬升 errorHandling |
| 5 | **S3** 权限声明收窄 | 安全 | **P2** | 消 LP1/SDI-2 残留 |
| 6 | **S4** 发版文档与运行时隔离 | 安全 | **P2** | 消 MEDIUM SDI-2 |
| 7 | **Q1** measure_skill 双语输出 | 质量 | **P3** | 消 SQP-3 |

**版本影响**：以上全部为**向后兼容**增强（无 API 破坏、无行为倒退）→ 按本技能自身 0.x 之外
「新功能=minor」语义，落 **v1.1.0**（当前稳定版 1.0.0，非 0.x，故 minor 非破坏边界）。

> **实施状态（2026-10-15 完成）**：S1/S2/Q2/Q3/S3/S4/Q1/Q4 全部落地，46 项回归测试全绿（含新增
> `TestRobustness` 9 项），YAML frontmatter 解析正常，en/zh locale 键集对齐（各 59 键），
> SKILL.md 升至 **1.1.0** 并 `git commit`。locale 键集合一致性由 `test_en_fallback_table_matches_enjson_keys`
> 长期守住（新增 en.json 键必须同步进 `_EN_FALLBACK`，否则测试失败）。

## 五、未证明事项（静态审计边界）
- 未运行任何目标脚本的**联网/写盘**路径——本技能声明零网络，静态未见网络调用；如需 100%
  证明运行时隔离，建议另做**沙箱受控运行**（最小权限、断网）一次验证。
- SkillSpector `DO_NOT_INSTALL` 为机械阈值（与 `decision:pass` 矛盾），不构成实质阻断证据。
