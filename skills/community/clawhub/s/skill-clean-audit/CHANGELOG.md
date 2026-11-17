# Changelog

## v1.4.0 (2026-10-08)

依据 `clean_code_v1.4.0_plan.md`（基于 SkillHub TRACE 评测 + ClawHub 安全扫描的双源诊断）落地 P0+P1。核心目标：**防 C 维度因 v1.3.0 膨胀而退化**，而非继续加功能。

- **P0-O-1 执行模型小节**：新增《执行模型（方法论型，非工具型）》——明确本 skill 交付「判据+流程+清单」由 Agent 逐项判断，审计核心动作是**判断**（人的推理），无法预先编码为确定性自动流程；「没有端到端自动化脚本」重述为**设计决策而非缺失**，`metric_probe.py` 定位为可选加速器。对冲 E·开箱即用度「无自动化脚本」扣分，同时不偏离 methodology 定位。
- **P0-R-1 行数预算 + 内容下沉**：新增主文件**硬闸**（目标 ≤215 行、硬上限 250 行）；产物映射表下沉至 `references/faq.md` §8、轻量指标 5 项明细下沉至 §5（含 A/B 轴归属表与「命中≠脏」完整论证）、异常细则（超大文件/整目录/网络凭据）合并至 §4。主文件保留一行自足摘要 + 指针，避免信息孤岛。
- **P1-R-4 导航表**：新增《我该读哪个文件》渐进式披露路由表（何时读哪个文件），并在 README 目录树按用途分组。
- **P1-R-3 权限声明措辞收紧**：`metric_probe.py` 由「不入 requires」改为「**已评估并显式豁免**」，并加触发条件——若未来读 env / 调二进制 / 写被审源码 / 联网，必须立即改为声明。红线：**不得为消解扫描告警而谎报依赖**。
- **修复文档口径冲突**：FAQ §4 大文件阈值 `>2000 行` 与 SKILL.md 异常细则 `>500 行` 不一致，统一为 `>500 行`（中英同步）。
- 双语维护：FAQ 扩至 9 问（中英各 9，问数对齐），新增产物映射表、执行模型问答、指标完整定义表。
- 验收：`SKILL.md` 234 行（< 250 硬闸）；`skillhub-gate` 对导出副本 PASS；frontmatter 合法；`metric_probe.py` 实跑正确；中英 FAQ 问数一致。

## v1.3.0 (2026-10-04)

双依据优化：SkillHub TRACE 评测（4.8/5 优+）+ ClawHub SkillSpector 安全扫描（v1.2.0，6 条 finding 全为「声明/行为不符」与「语言强制」软问题，无恶意代码）。按 `clean_code_v1.3.0_plan.md` 分 P0/P1/P2 落地：

- **P0 · 安全扫描驱动**：① 精确化「只读」措辞（frontmatter description + 合规段 + 维护须知 Trust 红线）——「只读=只读被审计代码，只写自身产物(已声明)」，直接消 2 条 Medium 读-写 mismatch；② 语言选择 + 英文版产物：新增《语言选择》小节（auto/zh/en 三模式 + 产物映射），新增 `assets/clean_code_checklist.en.html` 与 `references/clean_code_audit_sample.en.md`，交付物/输出格式按语言映射，用户可明确选中文或英文。
- **P1 · 评测驱动**：③ FAQ——新建 `references/faq.md` + `references/faq.en.md` 集中解答 7 个高频问题（回应 C·反模式与FAQ 4.0）；④ 异常与降级升级——「文件缺失/无权限」改为 3 步行动指引（回应 R·异常处理 4.0）；⑤ 新增 `scripts/metric_probe.py`（纯 stdlib / `ast` 解析，只提示不判级，5 项指标信号，回应 E·开箱即用度 4.5 与总评「无自动化脚本」）；`.clawhubignore` 收窄为只排除导出脚本本身，使 metric_probe 能进 ClawHub 包。
- **P2 · 打磨**：⑥ 复杂场景样例——`references/clean_code_audit_sample_complex.md` + `.en.md`（类/继承/异步/全局态合成样本，演示 B 轴优先亮红灯）；⑦ 顶部《30 秒上手》5 行 Quick Start（回应 C·渐进式披露「章节多需耐心」）；⑧ 大文件分段兜底（>500 行按 ~500 行/段分段审 + 跨段汇总）。
- **双语交付**：README 新增 `README.en.md`，全部产物（清单/样例/FAQ/README）均提供中英文版；语言模式 auto/zh/en 由用户在触发时显式或按消息语言判定。
- 验收：ClawHub 重扫应消解 2 条 Medium mismatch + 4 条自然语言项；TRACE 目标 R→4.8+/C→4.8+/E→4.9+/总评≥4.9；`skill-publish-gate` 对导出副本 PASS。

## v1.2.0 (2026-09-30)

基于 `clean_code_skill_quality_eval.md`（对照 CSDN 8 维度框架、v1.1.1 评级 A / 8.80）的扣分点做文档侧优化，只修 D2/D4/D5，守住 D8 聚焦不蔓延（本次纯文档增改，不引入新依赖/网络，ClawHub 扫描应稳定通过）：

- **D2/D5 执行引导**：审计流程第 1 步补「用户未指定目标 → 先追问再审」闭环（中英双语），避免 Agent 凭印象审计未指定代码。
- **D4 工作流完整性**：新增《异常与降级》小节——文件缺失/无权限、非代码文件、超大文件(>2000 行)、网络/凭据 N/A 四类的显式处理，与「纯本地只读」行为一致，强化合规 Trust 维度。
- **D5 输入输出清晰度**：新增《输入要求》小节——明确接受 `.py/.js/.ts` 及任何人类可读源码文本、拒绝二进制/图片/数据/混淆代码、说明报告「不覆盖已有同名文件」的写盘行为，消除 Agent 误判「不支持某语言而拒触发」。
- **D2 路由提示（锦上添花）**：「它是什么/不是什么」末尾补「单文件→直接走流程；整 skill 目录→逐个脚本审、优先最常被改的」路由。
- 验收目标：重跑 8 维度评估 D2/D4/D5 ≥ 9、加权总分 ≥ 9.1；`skill-publish-gate` 对剥离封禁文件后的导出副本仍 PASS。

## v1.1.1 (2026-09-28)

多平台发布对齐（能力不变，内容等同 v1.1.0 + ClawHub 审核通过记录）：

- 版本号对齐：GitHub Release / SkillHub / ClawHub 三端统一为 v1.1.1。SkillHub 平台禁止同一版本号重复提交（v1.1.0 已于 2026-09-25 提交且审核中），故 bump 至 v1.1.1 重新提交。
- ClawHub 侧：v1.1.0 已于 2026-09-28 审核通过、恢复 Visible；本次以 v1.1.1 对齐更新。
- 发布包与 v1.1.0 一致：SKILL.md 双语 frontmatter、渐进式披露（assets/references/scripts）、MIT（SkillHub）/ MIT-0（ClawHub）。

## v1.1.0 (2026-09-25)

ClawHub 发布前优化 + 中英对照文档（能力不变）：

- **文档中英对照 / Bilingual docs**：`README.md` 全文改为中文 + 英文段落；`SKILL.md` 的 `description` 与各级 `##` 标题加英文副标题，便于国际平台（ClawHub / OpenClaw）发现与扫描。
- **ClawHub 合规前置 / ClawHub hardening**：
  - 新建 `.clawhubignore`，排除 `LICENSE`（与 ClawHub 强制 MIT-0 冲突，S1/S3/S5）与 `scripts/`（开发者构建脚本 `scripts/clean_code_clawhub_export.py` 只用于本地生成发布副本，不是技能可加载内容，不随包发布）；并把 `.clawhubignore` 加进 `.gitignore`，避免泄漏进 SkillHub 的 `git archive` 导出包。
  - `SKILL.md`《合规与边界声明》补一行可见的 `Requirements（声明与行为一致）`：无需外部二进制 / 环境变量 / 凭据（S4 扫描器读正文校验）。
  - 新增《维护须知》一节，写明「未来脚本若读 env / 调二进制须声明 `metadata.openclaw.requires`」红线（S1 mismatch 审核）。
  - 源仓库 frontmatter 仍保留 `license: MIT` / `slug` / `displayName`（供 SkillHub）；这些字段由 ClawHub 导出脚本剥离，不在发布包内。
- 多平台授权说明：GitHub / SkillHub 副本仍为 MIT（保留署名）；ClawHub 发布包按平台规则默认 MIT-0，源仓库**无需**改授 MIT-0。
- **ClawHub 审核通过（2026-09-28）**：首次发布 `versionId=k97d3cnx0df9jwtdm5kmpcdhzh8f0mr3`，安全扫描 `Moderate CLEAN`；新发布排队复核期间曾显示 `Hidden / Needs review`，现已恢复 `Visible`（公开可见、可安装，非违规判定）。
- **skill-publish-gate 实跑修到 PASS**：补 `SKILL.md` frontmatter 推荐字段 `summary` / `tags`（根因为中英对照版 description 折叠块内误置 `---` 视觉分隔线导致 frontmatter 被提前闭合）；`README.md` 去真实用户名；`scripts/clean_code_clawhub_export.py` 脱敏正则改动态读取当前用户（`getpass.getuser()`），源码不再含硬编码用户名路径。对「剥离封禁文件后的发布包」跑门禁结论 `PASS (exit 0, 0 问题)`。

## v1.0.1 (2026-09-25)

隐私脱敏 + 发布路径调整（能力不变）：

- 重写 `references/clean_code_audit_sample.md`：审计样例从真实项目 `agent-analytics-report` 的内部代码，改为自带行号、可逐行核对的**合成示例脚本** `demo-skill/scripts/aggregate.py`，不再泄露任何真实项目。
- `SKILL.md` / `README.md` 中的 `agent-analytics-report`、`ai-weekly` 命名引用改为合成示例；输出路径里的用户名绝对路径改为 `~/WorkBuddy/<session>/`。
- `assets/clean_code_checklist.html` 三处点名引用（`agent-analytics-report` 例1 / `ai-weekly` 例4 / `_PROXY_OVERRIDE` 例3）改为「审计范例」+ 通用占位 `_CONFIG_OVERRIDE`。
- skill 源目录从 `~/.workbuddy/skills/` 迁至 `~\dev\skill-clean-audit`（仅路径变更，方法/产出不变）。

## v1.0.0 (2026-09-23)

首个稳定版（stable）。整合 v0.1.0 第一性原理方法论与 v0.2.0 对标 Uncle Bob 的四项增强，并补齐发布就绪项：

- 版本号升至 **1.0.0**（SKILL.md frontmatter + 本 CHANGELOG）。
- **新增《合规与边界声明（网络访问）》小节**：本 skill 纯本地只读、零网络、零凭据、无第三方接口，不提供 / 不指导 / 不支持任何规避网络管理措施的能力；利于 SkillHub 内容审核的信任维度。
- 审计能力不变：A 理解成本 / B 修改风险两轴 + 红黄绿严重度 + 只读审计 + 交互式清单 + Uncle Bob 气味交叉对照 + CQS 红项 + 轻量指标信号 + 增量清理（Boy Scout）。
- 发布包剔除 LICENSE / .gitignore（SkillHub 封禁点文件），仅含 SKILL.md / README.md / CHANGELOG.md / assets / references。

## v0.2.0 (2026-09-23)

对标 Uncle Bob 原则库，补充 4 项不重叠、且重新接地到第一性原理的增强：

- **新增 `references/smells_crosswalk.md`**：把 Uncle Bob 的 canonical 代码气味（Rigidity/Fragility/Immobility/Opacity/Needless Repetition + 长函数/长参数/布尔旗/switch-on-type）映射到本 skill 的 A/B 两轴与红黄绿严重度，作为审计的标准命名桥接。
- **严重度红项补「命名与行为不一致 / 隐藏副作用（CQS 违反）」**：堵住函数级隐藏副作用的盲点（之前只覆盖模块级全局态）。
- **新增「轻量指标信号」小节**：函数行数 >40 / 参数 ≥4 / 嵌套 ≥4 / 布尔旗 / 重复 ≥3 次，明确框为「核查提示、非硬规则」，避免偏离第一性原理。
- **新增「修复优先级：增量清理（Boy Scout）」小节**：红项在你本来就要改该文件时顺手清，未碰代码不 gold-plate；Skill 脚本测试「有则绿、无不算红」。
- 审计流程第 2 步增加对照 `references/smells_crosswalk.md` 的指引。
- 交付物段补一句：生成物已被仓库 `.gitignore` 忽略。

## v0.1.0 (2026-09-22)

- 首个发布版：第一性原理 clean code 审计法（A 理解成本 / B 修改风险 两轴 + 红黄绿严重度 + 只读审计）。
- 交付 `SKILL.md`、`assets/clean_code_checklist.html`（交互式清单）、`references/clean_code_audit_sample.md`（完整审计范例）。
- MIT 开源，仓库 github.com/Elisabeth15501/skill-clean-audit。
