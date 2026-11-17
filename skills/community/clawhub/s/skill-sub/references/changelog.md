## [1.38.1] - 2026-07-10

### 修复
- **SKILL.md 标题断裂**：3 处 `##` 标题前缺少空行导致拼接失效
- **changelog.md 格式**：`---## [1.31.0]` 缺少分隔线换行
- **permissions.md 重复**：删除新旧两版权限扫描结果合并的旧版冗余内容

## [1.38.0] - 2026-07-03

### 新增
- **流程钩子系统（chain_hook.py）**：在里程碑步骤和末尾步骤上挂载 `hook.expects` 检查前置产出物
  - 新增 `chain_hook.py`：钩子检查引擎，支持 check/check_chain/CLI
  - `chain_executor.py plan` 输出显示钩子信息，`--force-hooks` 跳过
  - `chain_executor.py validate` 输出钩子验证结果
  - Step schema 新增 `hook` 字段，文档见 chain_schema.md

## [1.37.3] - 2026-07-03

### 修复
- 修正渐进式文件索引表：移除 scripts/ 条目（索引表应仅含 references/*.md）

## [1.37.2] - 2026-07-03

### 修复
- 修正 displayName 为 skill-sub（原错误设为 Skill Sub - 调用链编排）

## [1.37.1] - 2026-07-03

### 修复
- 修正 1.37.0 更新日志：删除不相关的 skill-standardization 工具修复条目，仅保留 skill-sub 自身的更新

## [1.37.0] - 2026-07-03

### 修复
- SKILL.md 文档结构标准化：触发条件章节优化（触发词改为具体操作描述，删除危险表述），工作流程格式化（列表+输入输出标注），配置表补齐，约束章节合并
- 技能子命令间增加有效分隔，提升指令执行清晰度

## [1.36.0] - 2026-07-03

### 修复
- **SKILL.md 标准化审计修复**（skill-standardization refactor）
  - R-17：SKILL.md 从 377 行裁剪至 160 行
  - R-20：changelog 术语统一
  - R-21：渐进式加载模板句恢复
  - R-23：文档-代码一致性误报分类
  - C-07：14 个代码块补充语言标识
  - C-11/C-12/C-13/C-17/C-18：章节格式、索引表、示例、边界量化修复
- 扩展 step_indexer search 过期检测覆盖 chain_planner 内部搜索（--ignore-stale 兜底）

---

## [1.35.1] - 2026-07-03

### 修复
- **SKILL.md 文档脱钩修复**：
  - 核心能力表：新增门禁系统、蓝皮书过期检测、链私有蓝皮书基线校验、自增强闭环
  - 工作流程：更新为 0-9 步串行门禁阻断表
  - 新增门禁系统文档（chain_gate CLI + 依赖链）
  - 新增链私有蓝皮书文档（基线保护 + 执行前自动校验）
  - 新增 LLM 参数文档（--llm-chain-check / --milestones / --adhesion）
  - 新增自增强闭环文档（chain_manager search）
  - 渐进式加载约束从 ≤230 行更新为 ~380 行
  - 快速开始示例补全 check-health / search / gate status 等新命令

---

## [1.35.0] - 2026-07-03

### 新增
- **链执行前蓝皮书健康检查**（chain_executor.py load_chain）
  每次加载链执行时自动比 blueprints.json 中的 _skill_md5s vs 当前 SKILL.md
  发现基线偏移 → HOOK-BLOCK [HARD] 阻断，输出修复命令
  跳过：`--force-health`

### 更新
- chain_executor.py plan 新增 `--force-health` 参数
- chain_executor.validate 也受健康检查影响（共用 load_chain）

---

## [1.34.0] - 2026-07-03

### 新增
- **LLM 参数门禁**（chain_gate.py/chain_planner.py）：三座新增 HARD 门禁
  - `llm_chain_verified`：接收 `--llm-chain-check` JSON，passed=false 阻断
  - `milestones_set`：接收 `--milestones`（逗号分隔序号），缺值阻断
  - `adhesion_resolved`：接收 `--adhesion` JSON，resolved=false 阻断
- **自增强模板缓存**（chain_cache.py）：参考 semantic-split 的闭环设计
  - `save_template()`：链规划成功时自动保存到 templates/
  - `scan_templates()`：n-gram 匹配（复用 step_indexer 同源算法）
  - `hit_template()`：相似意图命中后直接复用里程碑/步骤组合
  - CLI：`python chain_cache.py [list|clear|scan <intent>]`
- **chain_planner plan** 新增参数：--llm-chain-check, --milestones, --adhesion

### 更新
- chain_planner cmd_plan 管线新增门禁步：steps_selected → llm_chain_verified → milestones_set → io_validated → ... → adhesion_resolved → chain_connected → chain_saved

---

## [1.33.0] - 2026-07-03

### 新增
- **门禁系统**（chain_gate.py）：10 个 HARD 门禁，参考 novel-weaver pipeline_gate 架构
  GATE_REGISTRY 含依赖链：blueprint_verified → intent_decomposed → steps_searched → steps_selected → io_validated → chain_connected → chain_saved → chain_loaded → execution_planned → execution_completed
  API: check()/set_gate()/block()/reset(), 不通过则 exit(1) + HOOK-BLOCK 输出
- **chain_planner 门禁集成**：cmd_plan 每步前后注入 gate.check/set/block
  - 第1步搜索 → set steps_searched
  - 第2步 LLM 选 → set steps_selected（无输入则 blocked）
  - 第4步校验 → set io_validated（gap 数过大则 blocked）
  - 第4b步 DAG → set chain_connected（不连通则 blocked）
  - 第5步保存 → set chain_saved（失败则 blocked）
  阻断格式：HOOK-BLOCK [HARD] + 原因 + 修复命令

### 更新
- chain_planner.py：无 --steps 返回时 set steps_selected=blocked（标记问题，非静默退出）
- chain_planner.py：搜索无结果时 gate.block 替代 print+return

---

### 新增
- **search 过期硬检测**：搜索前自动比对所有技能的 SKILL.md 指纹与蓝皮书记录
  指纹不一致 → 直接拒绝搜索，提示先更新蓝皮书
  跳过检测：`--ignore-stale`

### 更新
- **工作流文档**：SKILL.md 明确标注蓝皮书校验为前置硬约束（第0步）
  链规划串行流程：校验→理解→规划→缺口→搜索→校验→生成→调度→健康检查

---

## [1.32.2] - 2026-07-03

### 新增
- **LLM 步骤蓝皮书提取路径**：prepare-llm-input (输出 SKILL.md 供 LLM 读)
- **apply-blueprint 命令**：接收+校验+保存 LLM 提取结果，含指纹记录
- **validate_llm_output() 校验器**：LLM 输出结构化校验 (step_name/consumes/produces 字段)
- **scan --check-fingerprint**：仅输出指纹更新列表，零更新
- **文档/help 顺序**：LLM 优先，regex 兜底

### 修复
- **I/O 文本清洗** (skill_extractor.py)：`_clean_io_text()` 删除 `|` `**` `` ` `` 代码块碎片，80字截断
- **description 清洗**：`_clean_io_text` 处理后 120字截断，替换 raw 200字
- **表格行过滤**：含 `|` 或 `` ` `` 的编号步骤跳过（748→672步）
- **无 ### 的 SKILL.md**：通过 LLM 提取路径覆盖（regex 无法提取的 ## / 列表格式）

---

## [1.32.1] - 2026-07-02

### 修复
- **意图分解器 Bugfix**：SEQ2 正则尾部 `.+?` 改为 `.+`（非贪婪只吞1字符导致"分析数据后做 PPT"拆成["分析数据","做"]后被长度过滤掉）
- **递归拆解**：支持"分析数据后做 PPT 然后发邮件"→3步拆解（右侧递归）
- **最左标记优先**：改用 `sep_pos`（分隔符位置）替代 `match.start()` 比较，避免多标记同起点时选错
- **「最后」避险**：`(?<!最)[后後]` 负向后顾，防止"最后"被误切

---

---

### 修复
- `--fixed-rules` 修复参数解析（逗号分词 bug）
- 修复循环顺序：fixed-rules 过滤移到 break 之前
- cmd_bump 新增 --fixed-rules 支持

---

## [1.31.0] - 2026-06-16

### 修复
- v1.29.1: 步骤蓝图索引、链文件夹结构、链规划器

---

## [1.30.0] - 2026-06-16

### 修复
- v1.29.1: 步骤蓝图索引、链文件夹结构、链规划器

---

## [1.29.0] - 2026-06-16

### 新增
- extract_step_semantics: 步骤语义提取，从 SKILL.md 自动提取 I/O 线索
- step_indexer.py: 步骤蓝图索引器，支持 scan/search/info/status/rebuild
- step_link_validator.py: 步骤衔接校验器，自动检测 I/O 缺口并生成粘连点建议
- chain_planner.py: 链规划流水线，统一"搜索→校验→创建"全流程
- 链文件夹结构：每条链私有目录 chains/{name}/chain.json + blueprints.json + backups/
- check-health: 链健康检查命令，md5 快速校验 SKILL.md 变化

### 改进
- 同义词字典 + n-gram 匹配，提升意图搜索精度
- I/O 提取 fallback：正则取不到时从步骤名推断
- 链蓝皮书私有化：独立于全局索引，链自包含
- classify_milestones 统一为 7 条规则
- PathManager 统一路径逻辑

### 修复
- 删除死代码 loop_branch_renderer.py
- 修复三处脚本中重复的 DEFAULT_DATA_DIR_RAW/SKILL_DIR/DATA_DIR 行
- 技能能力扫描钩子集成 step_link_validator 自动化校验

---

## [1.28.1] - 2026-06-16

## 1.28.0 (2026-06-16)

### 标准化改造（skill-standardization refactor）

- 修复 R-11：产出物路径违规（将 settings.py 路径引用置入代码块）
- 修复 R-17：SKILL.md 超 230 行限制（循环与分支编排拆分至 references/loop_branch.md，原 242 行 → 现 188 行）
- 修复 R-07：触发条件章节补充否定条件内容
- 修复 R-15：permissions.md 补充 skill-standardization 权限说明头部
- 自动修复 R-25：章节顺序调整、空行精简、表格格式规范化、触发条件格式修正
- 渐进式文件索引表补充：LICENSE.md、loop_branch.md
- 术语统一与写作规范修复（writing_standards 自动修正）
- 新增 references/loop_branch.md 渐进式加载拆分文件

## 1.27.1 (2026-06-05)

### 修复
- 全流程钩子加固: cmd_create 缺口分析提示+创建后自动校验(结构+流程)+调度注册 exit(1)截断

---

## 1.27.0 (2026-06-02)

### 新增

- **调度强制注册机制**：创建含 schedule 的链后**立即**输出强制注册提醒（不等执行日）；新增 register-schedule CLI 子命令将 registered 标记置为 true
- **执行计划注册提醒**：chain_executor.py 检测未注册调度并输出强制提醒

### 更新

- **chain_manager.py**：新增 register-schedule CLI 子命令；创建成功后含 schedule 时立即输出强制注册提醒
- **chain_executor.py**：新增 unregistered_schedule 检测，计划输出顶部含强制注册提醒
- **chain_schema.md**：schedule 定义新增 registered 字段，含注册流程说明
- **SKILL.md**：工作流程步骤 5 改为「立即注册调度」，明确不等手动执行

---

## 1.26.0 (2026-06-02)

### 新增

- **粘连点（Adhesion Point）系统**：新增第四种步骤类型 `type: "adhesion"`，标记调用链中无法由 skill 自动化的缺口，提供三种解决方案（manual/auto/hybrid）保证链不断
- **链自愈机制**：新增 `check-gaps` 命令，扫描所有调用链的粘连点，自动检测是否有新 skill 可填补并升级为 skill 步骤；`user_specified: true` 的链跳过自愈
- **执行计划渲染**：`chain_executor.py` 在计划中渲染粘连点步骤，展示原因和 3 种方案
- **流程缺口分析**：创建调用链时新增流程缺口分析，按语义/流程/决策三类真实缺口判断是否打粘连点；明确禁止过度粘连
- **算法组件**：新增 `chain_flow_validator.py`（步骤连续性/依赖链/孤立步骤/粘连点比例≤30%/禁止连续粘连点）和 `chain_structure_checker.py`（JSON 结构/类型枚举/必填字段/依赖闭环——最后一道关，不合格拒保存）
- **skill_extractor suggest**：新增 `suggest` 子命令，根据用户意图关键词匹配 skill 并排序候选，检测未匹配缺口（Python 扫描+LLM 选最终集合的混合模式）
- **能力边界文档**：SKILL.md 新增「能力边界与限制」章节，含适宜/不适宜场景表、硬限制表、常见创建错误速查
- **FAQ 错误场景**：faq.md 新增 E1~E4 四个常见错误场景（粘连点连续、skill 不存在、步骤失败、校验器阻断），每条报错附原因和解决方法
- **调度配置系统**：新增 `schedule` 元数据字段（type/expression/description/registered），任何平台可据此创建定时任务；新增 `chain_manager.py schedule` 子命令；创建链时描述含定时关键词（每天/每周/自动等）强制要求 `--schedule` 参数，否则阻断
- **auto_safe 自动化检测**：`chain_flow_validator` 自动计算链是否可全自动执行（无 manual 粘连点且无 ask 模式），输出 `auto_safe` 布尔字段供平台使用
- **调度强制注册机制**：创建含 `schedule` 的链后**立即**输出强制注册提醒（不等执行日）；新增 `register-schedule` CLI 子命令将 `registered` 标记置为 `true`；`chain_executor.py` 执行计划检测未注册调度并输出强制提醒

### 更新

- **`chain_manager.py`**：`validate_chain` 适配 adhesion 类型；新增 `check-gaps` / `schedule` / `register-schedule` CLI 子命令；`create_chain` 和 `update` 自动调用 `flow_validator` + `structure_checker` 校验；新增 `user_specified`、`schedule` 字段和对应 CLI 参数；新增定时关键词强制检测逻辑；创建成功后含 schedule 时立即输出强制注册提醒
- **`chain_schema.md`**：新增类型 D 粘连点步骤、`user_specified` 字段、`auto_safe` 字段、`schedule` 字段（含 `registered`）及 Schedule 定义章节
- **`chain_executor.py`**：新增 `unregistered_schedule` 检测，计划输出顶部含强制注册提醒（`registered=false` 时）
- **`workflow.md`**：创建流程从 7 步扩展为 8 步，新增步骤 6 流程+结构双重校验
- **`adhesion.md`**：补充缺口分析规则、禁止行为清单、连续粘连点合并规则、判定示例
- **`SKILL.md`**：核心能力新增第 7 项粘连点支持；工作流程新增步骤 3 流程缺口分析；快速开始重写为「三步上手」含完整 JSON 示例；新增「能力边界与限制」章节
- **`faq.md`**：新增 E1~E4 常见错误场景
- **`chain_executor.py`**：新增 `unregistered_schedule` 检测，计划输出顶部含强制注册提醒

---

## 1.24.10 (2026-06-01)

### 修复
- 清除H1后冗余反模式引用

---

## 1.24.9 (2026-06-01)

### 修复
- 清除H1后冗余反模式引用

---

## 1.24.8 (2026-06-01)

### 修复
- 标准化改造最终版

---

## 1.24.7 (2026-06-01)

### 修复
- 版本追平仓库

---

## 1.24.6 (2026-06-01)

### 修复
- 标准化改造完成(非标章节处理+description 同步)

---

## 1.24.5 (2026-06-01)

### 修复
- audit --fix 自动修正: meta_field_sync, writing_standards

---

## 1.24.4 (2026-06-01)

### 修复
- 标准化改造完成

---

## 1.24.3 (2026-06-01)

### 修复
- 版本追平 changelog

---

## 1.24.2 (2026-06-01)

### 修复
- 标准化改造：章节重排+索引表+非标章节处理

---

## 1.24.7 (2026-06-01)

### 修复
- C-13索引表补全

---

## 1.24.6 (2026-06-01)

### 修复
- 从1.24.1恢复，仅添加索引表+顺序修正+R-10/R-20同步

---

## 1.24.5 (2026-06-01)

### 修复
- 版本追平

---

## 1.24.4 (2026-06-01)

### 修复
- 恢复原始版本后仅保留索引表+description 同步

---

## 1.24.3 (2026-06-01)

### 修复
- 标准化修复：渐进式索引表 + 章节顺序修正

---

## 1.24.1 (2026-05-31)

### 修复
- 补回缺失的 H1 标题（）
- R-25 C-07: 3 个代码块补充语言标识
- R-25 C-10: 精简 frontmatter 后多余空行

---
## 1.24.0 (2026-05-31)

### Changed（skill-standardization 规范化改造）
- **SKILL.md 全面重构** — frontmatter 补充 trigger/trigger_negative 字段；description 删除版本号（R-04 修复）；删除 H1 版本号（R-06 修复）；清理冗余空白行和历史性内容
- **_meta.json 同步修复** — 补全 data_dir 字段（同步 SKILL.md frontmatter）；tags 与 SKILL.md 同步；补全 triggers 字段；R-12 合规
- **references/changelog.md** — 版本号去除 v 前缀，使用纯数字 SemVer 格式（R-10 修复）
- **references/faq.md** — 删除与 antipatterns.md 重复的反模式内容，专注 FAQ + 使用技巧；修正文档描述
- **references/reference.md** — CLI 命令补全 `{SKILL_DIR}/scripts/` 路径前缀，确保从任意目录可执行
- **references/workflow.md** — 修正配置路径错误（`scripts/default_config.json` → `config.json`）
- **scripts/ 目录清理** — 删除 13 个 .bak 备份文件和 9 个历史 patch/fix 脚本，仅保留 7 个活动文件

---

## 1.23.4 (2026-05-30)

### 修复
- audit --fix 自动修正

---

## 1.23.3 (2026-05-30) — R-12 合规完善

### Changed
- 所有脚本补充 DEFAULT_DATA_DIR_RAW + DATA_DIR R-12 定义
- _meta.json 补充 data_dir 字段
- 运行 fix_missing_data_dir 一键修复，R-12 审计通过


## 1.23.0 (2026-05-27)

### 修复（R-11 路径规范）
- **assets/ 目录迁移** — `assets/` 目录下的 `default_config.json` 和 `settings.html` 迁移到 `scripts/`
- **路径引用修正** — `chain_manager.py`、`chain_executor.py`、`settings.py` 中的 `assets/` 路径统一改为 `scripts/`
- **assets/ 目录删除** — 符合 R-11 规则（产出物必须在 `scripts/` 或根目录）

---
## 1.22.0 (2026-05-26)

### 面向对象（OO）改造
- **chain_executor.py** — 全面 OO 改造，拆分为 7 个类：
  - `Config` — 配置管理（加载默认配置 + 用户配置合并）
  - `PathManager` — 路径管理（技能目录、调用链目录、技能查找）
  - `Validator` — 验证器（里程碑判断、retry_policy/failure_mode 验证）
  - `TopoSorter` — 拓扑排序器（子步骤依赖排序、递归处理 loop/branch）
  - `ExecutionPlanBuilder` — 执行计划构建器（构建执行计划、收集技能名称、生成 AI 指令）
  - `InstructionGenerator` — AI 指令生成器（独立类，处理 loop/branch 步骤的指令渲染）
  - `CLIHandler` — CLI 处理器（plan/quick/validate 命令处理）
- **chain_manager.py** — 全面 OO 改造，拆分为 7 个类：
  - `ConfigManager` — 配置管理器（加载/保存用户配置）
  - `PathManager` — 路径管理器（调用链目录、索引文件、技能目录、状态/日志目录）
  - `ChainValidator` — 调用链验证器（里程碑判断、调用链数据验证）
  - `BackupManager` — 备份管理器（自动备份、备份列表、备份恢复）
  - `ChainManager` — 调用链管理器（加载/保存索引、加载/保存/删除调用链、列表）
  - `ChainEditor` — 调用链编辑器（创建/更新/删除调用链、添加/删除步骤）
  - `CLIHandler` — CLI 命令处理器（init/create/list/show 命令处理）
- **可维护性提升** — 原 1000+ 行函数式代码拆分为职责单一的类方法，便于单元测试和后续扩展
- **SKILL.md 更新** — 修正快速开始代码块中的文件名引用（`chain_manager_oo.py` → `chain_manager.py`、`chain_executor_oo.py` → `chain_executor.py`）

---

## 1.21.0 (2026-05-26)

### 新增功能（build_execution_plan 子步骤处理）
- **子步骤拓扑排序** — `_topo_sort_substeps(steps)` 递归对 loop/branch 内的子步骤按 depends_on 依赖关系进行拓扑排序，替代原来的数组顺序执行
- **递归步骤计数** — `_count_all_steps(steps)` 递归统计所有步骤数（含 loop 子步骤 for_each 迭代次数、while 预估、branch 最大分支），total_steps 计算现在准确
- **build_execution_plan() 接入** — 在生成执行计划时自动对 loop/branch 子步骤进行拓扑排序，并调用 _count_all_steps() 计算准确的 total_steps

---

### 修复

---

# skill-sub 更新日志
## 1.20.0 (2026-05-26)

### 新增功能（高级编排）
- **循环步骤（Loop Step）** — `type: "loop"` 支持 `for_each` / `while` 两种模式，可嵌套子步骤
- **分支步骤（Branch Step）** — `type: "branch"` 支持 `if_steps` / `else_steps` 条件分支，可嵌套子步骤
- **递归渲染引擎** — `loop_branch_renderer.py` 独立模块，支持 `skill` / `loop` / `branch` 步骤的递归 AI 指令渲染
- **`chain_schema.md` 扩展** — 新增 `type` 字段定义，支持三种步骤类型及其子结构（`loop.*` / `branch.*`）
- **`chain_executor.py` 接入** — `generate_ai_instructions()` 改为调用 `render_plan_with_loop_branch()`，完整支持循环/分支渲染

---

### 修复
- `calc_intent_similarity()` 分词 bug：`chain_words` 未做 `re.findall` 分词导致永远匹配不上；加入 `user_intent` 字段参与相似度计算
- `cmd_error_stats()` 日志目录路径错误：`log_dir` 手工拼路径改为使用 `LOGS_DIR`；文件读取改 `with open()` 上下文管理器

---

## 1.19.1 (2026-05-25)

### 修复（v1.19.0 虚假 DONE 项实际实现）
- 里程碑影响分析（milestones）— 真正实现并注册到 parser
- 动态里程碑（--dynamic）— 真正实现并注册到 parser
- 里程碑统计（milestone-stats）— 真正实现并注册到 parser
- 标签系统增强（list-tags）— 真正实现并注册到 parser
- v1.19.0 仅标记 DONE 但未实现上述四项，v1.19.1 修复

---

## 1.19.0 (2026-05-24)

### 新增功能
- 链标签系统增强（Chain Tag System Enhancement）— `list-tags`
- 链导入/导出（Chain Import/Export）— `import` / `export`
- 步骤摘取器：参数提取（Parameter Extraction）
- 步骤摘取器：兼容性检查（Compatibility Check）
- 执行计划生成器：资源分析（Resource Analysis）
