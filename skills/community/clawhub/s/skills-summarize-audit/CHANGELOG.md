# Changelog

All notable changes to the skills-summarize-audit skill.

---

## [9.2.2] - 2026-09-20

- 移除未再属于核心能力的生命周期指导模板与配置开关，避免把安装、卸载、迁移、回滚等可写入操作打包进只读审查技能。
- 保留 `actions-schema.md` 的建议交接字段；具体实施继续交给用户明确调用的对应 Agent。

## [9.2.1] - 2026-09-20

- 根据真实全量扫描回修输出：消除 Agent 风险对的误导性零项表述，保留“未验证正常”的事实边界。
- 严格校验 MCP、Skill、Agent 使用信号的计数与覆盖字段；畸形或负数输入转为 `unavailable`。
- 区分 proxy 活跃与可归因 MCP 调用，修复项目画像低适用项统计，并扩展常见缓存目录排除。
- 项目技术版本标记为声明范围；全量验收确认扫描源 SHA256 未变化。
- 发布包仅纳入 `scripts/*.py`，排除 `__pycache__`、`.data` 与测试目录，避免把本地运行产物带入 npm/插件包。

## [9.2.0] - 2026-09-20

- 全量实跑回修：合并重复补证、去除零项任务、明确局部分数/扫描覆盖；临时安装缓存不再误报活动来源冲突。
- 修复 Codex function_call 漏记与跨时间窗长会话漏记；修正上下文多行 description 解析及旧参考文档证据冲突。

- 公开能力统一为翻译精炼、项目画像、技能/插件推荐操作；按需加载内部健康、生态与安全证据。
- 缺失使用、画像、市场数据不补零、不排名，不生成隐藏/卸载建议；配置存在不再等于启动成功。
- 增加完整行动交接、市场与风险证据字段，修复 MCP 调用客户端误归因，报告不输出凭据。
- 增加显式基线、首次全景/后续增量、升级扫描建议、Markdown/JSON 导出与 CI 门禁。
- 增加隔离环境测试依赖、空/部分证据与 SHA256 只读回归；统一报告及 UI 元数据。

## [9.1.0] - 2026-07-25

- 能力架构重构（6→5）：合并「推荐 + 生命周期指导」为能力五，新增能力四「生态综合评估」，覆盖 MCP+Agent+Skill 三层。
- 新增 transcript 提取器（extract_usage_signals.py）提供真实使用证据；跨客户端扫描（zcode/codex/claude）。
- dsh 技能包插件外壳（package.json + cordis.patch.yml + index.js）：支持 `dsh plugin add github:gtbwpkwjnb-alt/skills-summarize-audit-skill`。

## [8.2.4] - 2026-07-25

- 翻译回测支持完整截图、显式 `namespace:id`、`$namespace:id` 和绝对路径证据，禁止用历史集合替代本次输入。
- 补齐系统技能、插件 cache/staging、模板 frontmatter、runtime、manifest、远程目录和安装回执的来源矩阵与字段优先级。
- 增加全量翻译硬性门禁、UTF-8/代码页损坏检查、快照回滚说明和 `display_equivalent_sources` 来源处理。
- 修复系统技能和模板技能只改错 frontmatter、命令栏仍读取英文 `agents/openai.yaml` 的回退问题。

## [8.2.3] - 2026-07-23

- config.yaml 瘦身：trend_tracking（默认关闭、无消费者）与 capacity_analysis（唯一消费者为已归档的 .archived/flow-v7/02-bis-capacity.md）移至 references/config-candidates.md，原位留指针注释；community_feed 与 dev_search_policy 因 security-rules.yaml 现行依赖保留不动。
- config.yaml 与 user-profile.md 行尾统一为 LF（仓库无 .gitattributes，core.autocrlf=true，入库 LF 约定），内容不变。
- SKILL.md 触发节新增与 summarize 技能的分工声明：文本压缩/摘要属 summarize，本技能只做技能库审查、翻译精炼、项目画像与推荐。

## [8.2.2] - 2026-07-23

- config.yaml 顶部注明本文件为 Agent 行为约定配置、无脚本消费，并在 translation_refinement 块补 collect 脚本声明，三个脚本均有 script 声明。
- platforms/workbuddy.yaml 移除与只读底线矛盾的 write 权限；新增 platforms/README.md 说明平台文件仅记录平台特征、无脚本消费。
- 推荐档位术语统一为六档（保留/升级/替换/引入/共存/归档），修正 SKILL.md、config.yaml 注释与 recommendation-framework.md 中的"五档"误述。
- 合并 references/description-refinement.md 的 Forma 维度/权重/阈值至 description-quality.md 并删除原文件，消除双份事实源。
- SKILL.md 输出节与 report-template.md 接入 references/output-contract.md 事实状态契约引用。
- README 新增「脚本参数」一节，文档化三个脚本的 argparse 参数（含 --batch-size/--offset/--fail-on/--profile/--max-files/--max-depth 与各目录参数）。
- agents/openai.yaml 增加顶层 version 字段并纳入 tests/validate.py 版本一致性门禁。
- 修正 SKILL.md frontmatter description 中的右双引号误用为正常引号对。

## [8.2.1] - 2026-07-23

- 归档 v7 阶段式旧流程 references/flow/ 至 references/.archived/flow-v7/，消除与只读底线矛盾的写入流程误导。
- 修复 analyze_project_profile.py PyYAML 硬依赖：缺失时优雅降级输出 unavailable，新增 requirements.txt 与 README 环境依赖说明；相关测试与 validate 画像门禁在缺依赖时跳过。
- 兑现翻译自学习存储段：glossary 增加 learned_phrases/learned_overrides 空段，创建 .data/glossary-learn-log.jsonl。
- 清理根目录误生成的 nul 文件与空目录残留。

## [8.2.0] - 2026-07-23

- 将 `installed`/`visible` 审查绑定到 `config.toml` 插件登记和远程安装回执；缓存、市场目录和未安装残留不再静默视为已安装。
- 增加 `plugin_ref`、`installation_status`、安装证据和缓存残留边界，修正多版本/等价来源处理方案。
- 将翻译质量告警限制在有 UI 可见证据的集合；保留英文 `display_name`/skill ID，只精炼 `short_description`，并强化 `--require-ready` 数量、来源和回读门禁。
- 收紧冲突检测，避免 `summarize` 与 `skills-summarize-audit`、`figma-use` 与其变体因英文 ID 子串误报；互补继续要求具体画像词。
- 项目画像执行 `project-types.yaml` 的文件、目录、依赖和回退规则，输出截断状态，排除快照/归档/记忆目录并合并重复推荐。
- 本版本的提交、打标和远程推送属于本次迭代操作，不是 Audit 日常功能。

## [8.1.0] - 2026-07-23

- 将主审查范围统一为已安装技能与插件的问题、来源、版本、可用性和元数据核验。
- 新增只读问题审计入口，输出严重度、证据、可编辑性和逐项处理方案。
- 新增用户画像匹配、健康评分、技能触发冲突与能力互补关系分析。
- 保留并强化当前 UI 可见技能的说明翻译精炼、数量门禁、来源解析和写后回读。
- 本次版本同步通过严格验证；发布提交和远程推送属于本次迭代操作，不是 Audit 日常功能。

---

## [8.0.1] - 2026-07-20

- 将使用证据从已废弃的 summarize `error-ledger` 迁移到结构化 Codex session/tool-call 事件。
- 无法建立 provenance 时标记 `unavailable`，不再误判为 zombie 或回填质量分。
- 允许用户明确授权后的本地、可回滚修复，并保留外部发布与账号授权边界。

---

## [8.0.0] - 2026-07-19

### Summary
**加强大脑，不动手**：扩充 9 个 references 知识库，把"被动响应、静态规则、四档建议"升级为"主动体检、80+ 指纹、五档推荐、九大生命周期模板"。保持 v7.1.0 只读底线，所有写入操作仍由用户的 Agent 按 Audit 输出的指令模板执行。

### Changed
- **职责重新定位**：从"翻译/画像/推荐器"升级为"AI Agent 技能管家大脑"。仍只读，但输出更密集、更可执行。
- **触发词扩展**：新增 `技能体检`/`skill checkup`/`僵尸技能`/`过期检查`/`触发词冲突`/`指导安装/升级/卸载/迁移` 等定向触发词。
- **推荐输出**：四档（保留/观察/考虑引入/不建议）→ 五档（保留/升级/替换/引入/共存/归档），新增"组合套餐"与"可达性反推"。

### Added（9 个新 references 知识库）
- **`references/tech-fingerprints.yaml`**：80+ 技术指纹（前端/后端/移动/桌面/DB/DevOps/AI/语言/工具/Agent 生态/文档），参考 specfy/stack-analyser 700+ 精选。覆盖 React/Vue/Next.js/Django/FastAPI/PyTorch/Docker/K8s 等。
- **`references/mcp-marketplaces.md`**：MCP 市场目录（Glama/Smithery/官方 Registry/MCP Toplist）+ 六维健康分评估框架 + URL 模板供用户的 Agent 抓取。
- **`references/skill-marketplaces.md`**：技能市场目录（Skills Directory/SkillRegistry/csreg/Skill CLI）+ 七维健康分 + 跨平台一致性检查规则。
- **`references/translation-quality.md`**：TQI 四维评分（术语保护 30% + 触发词命中 30% + 长度合规 20% + 同源一致 20%）+ 自学习规则。
- **`references/conflict-detection.md`**：触发词冲突检测（同义词/包含/范围/格式/过宽五大类型）+ 豁免机制 + 增量检测。
- **`references/health-checklist.md`**：八大健康维度（存在性/元数据/依赖/使用/版本/触发词/安全/跨平台）+ 综合健康分 0–10。
- **`references/recommendation-framework.md`**：五档推荐 + 互补性分析（替代/共存/补充/无关）+ 组合套餐算法（贪心集合覆盖）+ 可达性反推（参考 Safeguard reachability）+ 信心指数六因子。
- **`references/lifecycle-guidance.md`**：九大生命周期模板 A-I（安装/升级/卸载/归档/启用禁用/迁移/重命名/同步/回滚），每个含"前置检查 + 快照 + 主操作 + 验证 + 风险 + 回滚"。

### Research（业界轮子对照）
- **`specfy/stack-analyser` ⭐416**：700+ 技术指纹 → 精选 80+，避免手维护 project-types.yaml
- **`OpenSSF Scorecard`**：18 项检查透明权重 → health-checklist.md 八维
- **`npms.io`**：quality 35% + popularity 25% + maintenance 40% → 健康分公式参考
- **`Skills Directory`**：50+ 安全规则 + A/B/C 评级 → 候选库安全维度
- **`Glama`**：10,000+ maintainer-verified MCP + 质量分 → MCP 市场首选
- **`Safeguard`**：reachability analysis → recommendation-framework.md 可达性反推
- **`Dependabot/Renovate`**：定时扫描 + 自动 PR → health-checklist.md 定时检查
- **`Skill CLI (skillsdir.dev)`**：包管理体验 → lifecycle-guidance.md 模板规范
- **`OpenSSF dependency depth`**：依赖深度惩罚 → 健康分"依赖深度"维度

### Compatibility
- **向下兼容**：v7.1.0 的 collect_codex_display_candidates.py 输出字段保留；translation_quality 字段值映射（ready → TQI ≥ 8）。
- **触发词兼容**：v7.1.0 的所有触发词仍然有效；新增触发词不冲突。
- **配置兼容**：v7.1.0 的 config.yaml 字段全部保留；新增字段默认值不破坏现有行为。

### Boundary
- 仍保持"默认只读"底线；不直接执行写入/安装/卸载。
- 所有候选评估的市场数据抓取由用户的 Agent 按 URL 模板执行。
- 仍要求用户明确授权才进行联网查询。

---

## [7.1.0] - 2026-07-11

### Changed
- **职责收缩**：主技能只保留技能库翻译精炼、项目画像和技能/插件推荐。
- **建议转介**：安装、发布、配置、桌面迁移、历史清理、回滚等仅作为报告中的后续建议，要求用户直接调用对应 Agent。
- **主流程瘦身**：移除容量、评分、活性、CI 与执行编排等主流程依赖，常规使用不再加载这些上下文。

---

## [6.4.8] - 2026-07-11

### Fixed
- **范围输出一致性**：`collect_codex_display_candidates.py --scope installed` 的 Markdown 输出现在只渲染已安装去重项，不再混入 remote catalog。
- **缓存候选去重**：同名条目优先选择非 `plugin-install-*` 临时目录中的较高版本；fixture 覆盖旧版本 cache。
- **自身展示中文化**：Audit 的 `agents/openai.yaml` 改为简体中文命令栏和侧边栏文案。

### Changed
- **输出规范收敛**：移除过时的“30 秒摘要 + 大评分表”示例，常规审计改为引用当前分类决策报告；评分明细仅在 `技能审查 深度` 展开。
- **安装入口修正**：删除不存在的 `references/installation.md` 引用，统一指向 `README.md`。

### Added
- **回归门禁**：严格验证检查 Audit 自身中文 UI 元数据、当前输出结构，以及旧输出/无效引用不再出现。

---

## [6.4.7] - 2026-07-11

### Added
- **展示来源地图**：新增 Codex、ZCode、Claude 与通用 `.agents` 的命令/侧边栏元数据定位表，明确已验证文件层与未验证 UI 层边界。
- **插件卡片解析**：采集器读取安装插件 `.codex-plugin/plugin.json` 的 `interface`，生成独立的 `codex_plugin_manifest` 中文候选。

### Fixed
- **UI 取证边界**：remote catalog 仅作为市场发现元数据；没有客户端 UI 验收时不再声称文件修改必然改变命令栏或侧边栏。

---

## [6.4.6] - 2026-07-11

### Fixed
- **安装边界纠正**：采集器区分已安装项与 remote catalog 市场项；健康度、容量和 P1 翻译积压只计算 `--scope installed` 的去重结果。
- **翻译质量分层**：命令栏名与侧边栏短描述达标即标记 `ready`；长描述单独标记，避免阻塞可见 UI 的中文化。

### Added
- **P1 首批精炼**：为 25 个真实已安装项添加稳定的按 id 中文覆盖，已安装短描述积压从 75 降至 51。

---

## [6.4.5] - 2026-07-11

### Added
- **审计交卷阶段**：新增⑥-e，固定输出带优先级、收益、验证与确认边界的 `🛠 建议执行`；不再只报告发现。
- **深度分析入口**：`技能审查 深度` 逐项检查版本、当前状态、可运行性、联网更新可用性与维护建议。
- **翻译积压治理**：按 UI 可见性、去重和每批 25 项的质量抽样计划精炼，不再把待处理总数直接抛给用户。

### Fixed
- 清理已卸载 `caveman` 的用户画像与本地 registry 引用。

---

## [6.4.4] - 2026-07-11

### Added
- **中文精炼质量门禁**：引入可维护术语/短语库，保护技术术语；精确命中标记 `ready`，不完整候选必须标记 `needs_agent_refinement`。
- **分类决策报告**：常规审计首屏固定输出“对当前用户的作用”和“保留/归档候选/建议安装/建议更新/翻译精炼”清单；评分明细仅按需展开。

### Research
- 评估 GitHub `argosopentech/argos-translate`（MIT、离线语言包）：保留为用户确认后的可选后端，因模型与运行时依赖较重，不随 Audit 捆绑。

---

## [6.4.3] - 2026-07-11

### Added
- **Codex 中文翻译清单**：`技能审查 精炼` 读取全局技能、插件 cache、runtime、`agents/openai.yaml`、manifest 与 remote catalog，固定输出命令栏和侧边栏的简体中文候选。
- **只读解析器与 fixture 门禁**：新增 `collect_codex_display_candidates.py`；采集前后验证扫描源 SHA256 一致，覆盖普通 `SKILL.md`、插件 UI metadata 与 remote catalog `interface`。

### Changed
- **边界收紧**：官方插件、runtime 与 remote catalog 永远只生成候选，不提供 UI/cache 写入命令；系统项保持只读。

---

## [6.4.2] - 2026-07-11

### Fixed
- **Codex 覆盖补齐**：扫描 `~/.codex/skills`、`$CODEX_HOME/skills` 和已启用 runtime 插件；归档与系统目录排除在 editable 扫描之外。
- **插件翻译候选**：Codex runtime 与系统技能现在必须输出中文精炼候选，并标注只读，不修改缓存。

---

## [6.4.1] - 2026-07-11

### Fixed
- **描述精炼接入审计流**：新增⑥-d；每次审计发现 Forma 不合格 description 时，强制输出翻译精炼候选。
- **触发与门禁对齐**：新增 `技能审查 精炼` / `refine` 子命令；候选缺失时报告标记 `partial`，不允许进入执行。
- **只读一致性**：移除“自动修正”表述，description 修改统一要求明确确认。

---

## [6.4.0] - 2026-07-11

### Changed
- **默认只读**：画像、记忆、缓存、日志、趋势、快照和修改全部移至明确确认后。
- **事实契约**：报告统一标注 `observed` / `inferred` / `estimated` / `unavailable`，未知数据不再回填默认高分。
- **证据化输出**：报告模板移除写死的健康度、收益、趋势和推荐，要求结论附来源、公式或限制。

### Fixed
- 快照顺序改为“确认 → 快照 → 执行”，避免未获授权前写入。
- 质量账本缺失时不再使用 8/10 fallback；registry 对齐不再宣称版本新鲜度。

---

## [6.3.0] - 2026-07-10

### Added
- **GitHub 同类横向比较**：候选必须比较能力覆盖、活跃度、许可证、兼容性、安全、成本与可复查 URL；不再只以 stars 决策。
- **安装作用域决策**：每项建议输出 project / global / plugin / defer、目标路径、理由、兼容性与确认门禁。
- **发布契约验证**：新增校验和、无破坏安装器、联网同意、比较协议和作用域输出的自动化检查。

### Changed
- **社区 Feed 默认关闭**：联网 GitHub/网页搜索需要当次用户明确同意。
- **安装器安全更新**：新增 --dry-run / -DryRun；检测本地修改或快进失败时中止且保留原目录。
- **评分与文档对齐**：README、报告和自检清单统一为八维评分。

### Security
- 移除远程脚本管道执行示例与更新失败后的递归删除回退。

---

## [6.1.0] - 2026-07-05

### Added
- **安全合规自检体系**：审计自检(⑥-bis)新增「🧩 安全合规」第7项，按 `references/security-rules.yaml` 8条规则检测
- **发布前门禁**：`publish_xiaping.py --safety-check` 上传前自动扫描技能目录，HIGH 风险阻止上传
- **安全规则文件**：`references/security-rules.yaml` — 8条规则覆盖数据外泄/供应链/提权/凭证/意图声明

### Changed
- **description 精简**：SKILL.md frontmatter description 从 7 行精简为 4 行 120 字，中英分开不混排，帮助 Xiaping LLM 正常解析意图
- **security_scan 默认启用**：config.yaml `security_scan.enabled: true`，审计时自动执行内置安全规则
- **发布脚本升级**：`publish_xiaping.py` 新增 `--safety-check` / `--no-safety-check` / `--safety-fail-on` 参数

### Security
- **analysis_error 修复**：精简 SKILL.md description 避免 Xiaping LLM 解析失败（`实际行为: LLM 分析失败` → 应可正常识别）

### 文件变更
- 新建: references/security-rules.yaml
- 修改: references/flow/06-bis-verify.md, config.yaml, SKILL.md, VERSION, CHANGELOG.md
- 修改: scripts/publish_xiaping.py（新增安全门禁）
- VERSION 6.0.1 → 6.1.0

---

## [6.0.1] - 2026-07-05

### Security
- **数据外泄修复 (HIGH)**：`config.yaml` external_signals_cache 默认关闭（`enabled: false`），需用户知情同意后手动启用；china_sources 补充额外知情同意注释
- **数据外泄修复 (MEDIUM)**：`config.yaml` dev_search_policy 默认关闭（`enabled: false`），需用户知情同意后手动启用
- **供应链风险修复 (HIGH)**：`README.md` 安装章节新增 SHA256 校验和（install.sh / install.ps1）、下载审查流程、安全提醒

---

## [6.0.0] - 2026-07-05

### Added
- **能力维度矩阵**：新增 `references/capability-dimensions.yaml`，定义 12 个能力维度，T0 核心工具手动精标，T1 工具从 tags 自动推断
- **质量信号**：审计时读取 summarize 的 `error-ledger.md`，提取 `TOOL:` 工具级错误记录，低于阈值(6/10)标记为 P1 缺口
- **社区 Feed**：新增步骤⑤-aa `references/flow/05-aa-community-feed.md`，从质量缺口和项目核心活动反推搜索词，用 GitHub MCP 搜索替代工具
- **能力互补性推荐**：重写推荐引擎(⑤b)，从"选 stars 多的"改为"能力矩阵对比"，输出替代/互补/补充/无关四类关系
- **生态雷达**：报告(⑥)新增条件区块，仅在发现质量缺口+社区替代品时输出，附带能力对比证据

### Changed
- **名称统一扫尾**：完成全量文件中的 `skills-audit` → `skills-summarize-audit` 替换（install.sh/install.ps1/SKILL.md/README.md/user-profile.md/06-report.md）
- **02-inventory.md**：新增能力映射步骤，扫描时加载 capability-dimensions.yaml
- **04-scoring.md**：新增质量信号读取规则，评分前先读错误账本
- **config.yaml**：新增 `quality_signals` 和 `community_feed` 配置块
- **execution-flow.md**：流程图新增 ⑤-aa 社区 Feed 步骤

### 文件变更
- 新建: references/capability-dimensions.yaml, flow/05-aa-community-feed.md
- 重写: flow/05-rec-engine.md (能力矩阵推荐)
- 修改: flow/02-inventory.md, flow/04-scoring.md, flow/06-report.md, config.yaml, SKILL.md, VERSION, execution-flow.md
- 名称修复: install.sh, install.ps1, README.md, user-profile.md (旧名→新名)
- VERSION 5.9.3 → 6.0.0

### Changed
- **技能改名**：`skills-audit` → `skills-summarize-audit`（全平台同步）
- **新增触发词**：`技能总结`（联动 summarize 品牌，触发技能审计模式）
- **SKILL.md 联动说明**：触发词章节标注与 summarize 的联动关系
- **When to Use**：增加「run summarize → 发现技能堆积 → 建议 `技能总结`」场景

### 文件变更
- 所有文件中的 `skills-audit` 名称引用更新为 `skills-summarize-audit`
- install.sh/install.ps1 仓库 URL 更新为新仓库
- skill-registry.yaml tag 增加 summarize
- VERSION 5.9.2 → 5.9.3

---

## [5.9.2] - 2026-07-05

### 改进
- **前置条件重构**：去平台约束、去 skillfather/skill-creator 多余依赖，硬/软分离，工具标注安装引导，user-profile.md 改为缺失时自动创建
- **frontmatter 精简**：`requires.configs` 移除 user-profile.md（非硬性依赖，改为自动创建）
- **冗余文件清理**：
  - 删除旧备份 `.SKILL.md.v5.1.bak`、`.VERSION.v5.1.bak`（git 已存历史）
  - 删除意外文件 `nul`（Windows 保留名）
  - 删除历史重定向 `references/workflow-details.md`
  - 删除零引用笔记 `references/learned/skills-audit.md`
  - 删除 `.github/ISSUE_TEMPLATE/`（3 文件）+ 空 `.github/` 目录
- **缓存迁移**：`external-signals-cache.json` 从根目录移至 `.data/`，对齐 config.yaml 路径配置
- **文件结构图更新**：移除 workflow-details.md 行，.data/ 注释补全外部信号缓存

---

## [5.9.1] - 2026-07-05

### P0 - 版本同步与修复
- **版本号统一**：VERSION / SKILL.md / README.md / skill-registry.yaml 同步至 5.9.1
- **7维权重修正**：Novelty 10% → 7%、Contamination 5% → 3%、Fresh 17% → 15%、Community 18% → 15%，权重和恢复 100%
- **平台 YAML 修复**：移除 `platforms/zcode.yaml`、`claude.yaml`、`codex.yaml`、`cursor.yaml` 中未闭合的 `"`
- **config.yaml 缩进修复**：插件技能路径恢复为 `scan_paths` 同级项
- **project-types.yaml 缩进修复**：`requirements.txt` 模式条目结构正确

### P1 - 文档对齐
- **七维评分替换**：移除 `workbuddy.yaml`、`description-quality.md`、`report-template.md`、`recommendation-examples.md` 中残留的"五维"与数值分示例
- **flow/*.md 转义修复**：修正反斜杠丢失、单引号代码块、换行符污染
- **仓库名统一**：`SKILL.md` 与 `install.sh` / `install.ps1` 统一使用 `skills-audit-skill`
- **自检清单更新**：`self-audit-issues.json` 记录本轮修复

### P2 - 运行时治理与测试工程化
- **运行时数据目录 `.data/`**：迁移 `stats.json`、`project-profiles.json`、`activity-log.jsonl` 至 `.data/`，避免与源码混排
- **config.yaml 路径更新**：`data_dir` 指向 `.data/`，所有缓存/统计/日志文件路径统一
- **无用文件清理**：删除 `nul`、`.skill-order.json`
- **旧数据格式重置**：`stats.json` / `project-profiles.json` 从数值分制重置为 S/A/B/C/D 格式
- **自动化验证脚本**：新增 `tests/validate.py`，覆盖 YAML 解析、版本同步、权重和、平台合规、flow 格式、数据目录检查
- **扩展测试用例**：新增 `test-weight-sum.md`、`test-yaml-parse.md`、`test-version-sync.md`、`test-platform-yaml.md`
- **SKILL.md 文件结构**：补全 `tests/`、`references/flow/`、`.data/` 说明

---

## [5.8.0] - 2026-06-28

### P0 - 容量分析引擎
- **容量分析引擎**：新增步骤②-bis，分析当前 agent 环境下每个已安装技能/工具的 token 成本
- **灵活上限计算公式**：`(上下文可用空间 - 固定消耗) / 单 skill 平均注入成本`
- **容量报告输出**：步骤⑥新增 `capacity_analysis` 块（JSON 格式），含 agent 类型、固定消耗明细、容量判定（🟢/🟡/🟠/🔴 + 可再装数量）
- **步骤②扩展**：新增容量采集项（SKILL.md 大小/MCP工具数/描述长度/Agent类型）
- **多 Agent 计算模型**：CodeBuddy(16K硬限制) / Claude Code(listingBudget=1%) / Cursor(动态)

### P0 - CI/CD 无交互模式
- **--ci 模式入口**：触发词 `技能审查 --ci` 或 `skills-audit --ci`
- **CI 模式特征**：无交互、JSON 输出、跳过 ④-bis、max_tokens 预算限制（默认 8000）
- **门禁逻辑**：health=🔴→exit_code=1 / actions>5→exit_code=2 / t3_ratio>0.35→exit_code=3
- **CI 输出 schema**：新增 `references/ci-output-schema.md`
- **GitHub Actions 模板**：新增 `references/ci-github-actions.yml`
- **config.yaml 更新**：新增 `ci` 配置块（max_tokens/skip_steps/gates）

### P1 - Novelty + Contamination 7维评分
- **评分从 5维→7维**：新增 Novelty(10%) + Contamination(5%)
- **权重重分配**：Fit 35%→30%, Fresh 15%→17%, Community 20%→18%, 其余不变
- **Novelty 检测**：WebSearch 竞品对比 + skill-registry.yaml 交叉比对（仅 S/A 档执行）
- **Contamination 检测**：正则语言混合检测 + 触发词矩阵一致性校验（本地计算，零 token 成本）
- **CI 降维**：CI 模式自动降为 5 维（跳过 Novelty + Contamination）

### P2 - SkillSpector 集成 + 生态合作
- **安全扫描配置**：`config.yaml` 新增 `security_scan` 块（skillspector/builtin）
- **安全子项融入 Value 维度**：通过→+0.5档 / Critical→D / High→C
- **actions.json 输出**：新增 `references/actions-schema.md`，对接 Skills Manager
- **WorkBuddy 上架准备**：SKILL.md frontmatter 新增 `category: "开发工具"` + `platforms` 字段

### 文件变更汇总
- SKILL.md: v5.7.0→5.8.0，frontmatter +category/platforms，7维评分表，CI模式入口，容量分析引擎，安全子项
- workflow-details.md: 全量同步所有变更，新增 ②-bis 容量分析章节，7维评分详细标准
- config.yaml: 新增 ci 块 + security_scan 块
- report-template.md: 新增容量分析报告块，评分表头更新为7维
- skill-registry.yaml: 版本 5.7.0→5.8.0
- VERSION: 5.7.0→5.8.0
- 新增: references/ci-output-schema.md, references/ci-github-actions.yml, references/actions-schema.md
- CHANGELOG.md: v5.8.0 条目

---

## [5.7.0] - 2026-06-28

### P0 - 阻塞修复
- **P0-1: 并行依赖修复**：②→⑤a 从并行改为串行（⑤a 依赖②输出的技能名列表）
- **P0-1: Community 离线策略**：网络不可用且无缓存时标注「⏸ 信号待获取」，跳过 Community 维度（4维重算权重），禁止使用伪造默认值25
- ⑤a 增加重试机制：最多2次重试，每次10s超时
- **P0-2: Value 维度重建**：从"项目价值(依赖usage)"改为"预期价值(基于画像推断)"，5档基于命中核心活动数+场景频率
- **P0-2: 痛点推导去usage化**：所有依赖 usage 数据的痛点改为基于画像推断（核心活动覆盖/技能分布/零匹配）
- **P0-2: 健康阈值更新**：`low_usage_warn` → `zero_match_warn`（调用次数=0 → 与画像零匹配）
- **P0-3: 版本自动回写**：④-bis 深度阅读时自动从 SKILL.md 提取 version，回写 `skill-registry.yaml`
- **P0-3: skill-registry.yaml 更新**：skills-audit 版本 5.5.0→5.7.0，注释说明自动回写规则

### P1 - 实用性增强
- **P1-1: 30秒摘要块**：报告最前面增加摘要块（健康度/关键操作/预估收益）
- **P1-2: 趋势对比行**：最近3次审计数据趋势行（均分/活跃/冗余变化）
- **P1-3: ROI 5档精化**：从3档（高/正向/净消耗）→5档连续制（S:>+3000t, A:+1000~3000, B:0~1000, C:-500~0, D:<-500），ROI计算基于加载成本+预期节约
- **P1-4: project-types.yaml 扩展**：新增 DevOps-多服务、CI/CD、游戏-Unity、游戏-Unreal、区块链-Hardhat、区块链-Solana、AI/深度学习、AI-LLM部署 共8种项目类型
- **P1-5: 推荐去重合并**：A/B/C三层推荐后按技能名去重，优先保留A层（内置映射更可靠），C层仅补充未命中技能

### P2 - 普适性/自进化增强
- **P2-1: 多平台配置补全**：新增 `platforms/claude.yaml`、`platforms/codex.yaml`、`platforms/cursor.yaml`
- **P2-2: 复合项目类型识别**：检测多个独立类型时生成复合类型+合并推荐列表
- **P2-3: custom_rules 轻量实现**：支持 add_skill/remove_skill/suggest 三种动作，在B层之后执行
- **P2-4: 缓存GC**：步骤⑧持久化时清理不在当前技能列表中的缓存条目
- **P2-5: 离线降级标注**：references 缺失时标注「⚠️ 离线模式」，禁止伪造默认数据
- **P2-6: 评分自进化基础**：⑥-bis 增加评分-决策一致性追踪，累积 ≥5 次偏差后触发权重微调建议
- **P2-7: user-profile 深度映射**：建立高频技能→Value+1档、工作模式→推荐权重、技术兴趣→搜索关键词等8条显式映射
- **P2-8: 审计反馈收集**：⑦执行后增加1-4分反馈问卷，写入 stats.json 用于长期优化
- **P2-9: ④-bis 分级策略**：S/A全量深读、B轻量检查、C/D跳过，token消耗降低 40-60%
- **P2-10: 描述检查位置调整**：从④步骤移至⑥报告阶段，减少不必要消耗
- **P2-11: 评分快照即时持久化**：报告输出前持久化评分快照，用户中断可增量恢复

### 文件变更汇总
- SKILL.md: 版本5.6.0→5.7.0，并行化修正、Value重建、ROI精化、分级策略、反馈收集等
- workflow-details.md: 全量同步所有19项变更
- config.yaml: low_usage_warn→zero_match_warn，custom_rules轻量实现
- project-types.yaml: +8种项目类型（游戏/区块链/DevOps/AI）
- skill-registry.yaml: 版本更新+自动回写规则注释
- report-template.md: +30秒摘要块+趋势对比行
- platforms/: 新增 claude.yaml/codex.yaml/cursor.yaml
- CHANGELOG.md: 完整19项变更记录

---

## [5.6.0] - 2026-06-28

### Added
- **独立词触发机制**：参考 `summarize` 技能，触发词必须独立发送（可带子命令），句中不触发，避免误触发
- **中英双语触发词矩阵**：22个词条（中文12+英文10），覆盖技能审计/项目审计双模式
- **同义字词自动映射**：审查=审计=检查=诊断、能力=技能=工具、环境=项目
- **语言自适应**：根据用户会话主语言（中/英/混合）自动切换翻译方向和报告语言
- **触发词翻译精炼**升级为核心能力：自动翻译+精炼技能触发词和简介，中英双向互译
- **同义字词映射表**：10个英文关键词→中文主词+2-4个同义扩展
- **子命令支持**：`深度`/`推荐`/`画像`/`健康` 四个子命令，按需执行特定步骤
- `platforms/workbuddy.yaml`：WorkBuddy 技能市场平台配置

### Changed
- **SKILL.md 精简**：从852行精简到176行（-79%），执行流程细节外移到 `references/workflow-details.md`
- frontmatter description 双语化：`技能审查·项目审计 → 画像驱动·五维评分·逐技能优化 | Skill Audit·Project Audit → profile·5dim·deep opt`
- `references/description-quality.md` 升级：新增语言自适应规则、同义字词映射表、翻译精炼示例
- `platforms/zcode.yaml`：触发词从5个扩展到22个
- `user-profile.md`：通用模板化，添加注释引导新用户填写
- `README.md`：更新触发章节、v5.6.0 changelog

---

## [5.5.0] - 2026-06-27

### Added
- **S/A/B/C/D 五档评分**：从连续0-100分改为五档定性制，减少agent间评分不一致
- **强制评分理由**：每个技能必须附带1句理由，无理由=未评分
- **前置目录检查**：步骤⓪新增项目根检测，防止非项目目录运行

### Changed
- 评分规则：逐维判定→定性选档→计算综合→映射最终档位

---

## [5.4.0] - 2026-06-26

### Added
- **画像强制持久化**：画像构建完成后必须写入磁盘，不持久化则阻止后续评分
- **报告输出强制检查**（⑥-c）：防止agent跳过报告直接执行
- **操作清单格式规则**：[!N]/[N]/[AUTO]/[SKIP] 四类标记，减少执行模糊性
- **自检缺陷追踪**：持久化阶段写入 `self-audit-issues.json`，下次审计回测修复情况

### Changed
- 执行前确认模板：展示自动/需确认/依赖暂停三类操作

---

## [5.3.0] - 2026-06-25

### Added
- **MCP跨层扫描**：步骤②新增第二阶段，扫描MCP服务器和工具列表
- **技能-MCP跨层重叠检测**：互补关系判定（方法型+执行型→✅互补）
- `mcp_config` 配置项

### Changed
- 能力来源从"技能"扩展到"技能+MCP"

---

## [5.2.0] - 2026-06-24

### Added
- **五维评分**：Fit/Value/Fresh/Community/ROI，从三维扩展到五维
- **置信推荐**：信心指数(0-10) + ROI + 证据链
- **不推荐清单**：5种数据驱动判定规则
- **并行编排**：6阶段化并行，减少35-40% tool call轮次
- **条件报告**：按需输出，无内容不兜底
- **审计验证**（⑥-bis）：数据一致性检查 + 抽样交叉验证
- When to Use / When NOT to Use 章节

### Changed
- 报告模板外移至 `references/report-template.md`
- 深度分析模板外移至 `references/deep-analysis-template.md`
- 推荐示例外移至 `references/recommendation-examples.md`
- 描述规则外移至 `references/description-quality.md`

---

## [5.0.0] - 2026-06-23

### Added
- **④-bis 逐技能深度阅读与分析**：不读技能正文的审计=盲评
- 六维分析框架：作用·适配·缺口·建议·维护·参考
- 外部参考验证（agent-reach/web_fetch ≥2来源）
- 自指校验

---

## [4.3.0] - 2026-06-22

### Added
- Community回填机制
- Value维度重构
- undo/回滚机制
- 外部信号增量缓存（GitHub⭐缓存7天，npm📥缓存30天）

---

## [4.2.0] - 2026-06-21

### Added
- 触发词优化
- `output_language` 三态（auto/zh/en）
- 自检锚点

---

## [4.0.0] - 2026-06-19

### Added
- 项目角色画像驱动
- 五维评分体系（初版）
- 15+ 项目类型支持
- 三级分层（T1/T2/T3）
- 描述质量检查
- 三层推荐引擎

---

## [3.0.0] - 2026-06-17

### Added
- 项目记忆驱动
- 双模式（技能审计/项目审计）
- 持久化机制

---

## [1.0.0] - 2026-06-15

### Added
- Initial release
- 基础技能扫描
- 简易评分
- 内置推荐映射
