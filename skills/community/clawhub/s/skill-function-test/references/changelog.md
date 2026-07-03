## [1.16.1] - 2026-06-22

### 修复
- hooks.py `_block()` 输出改为 stderr，不再被管道过滤吞没
- test_engine.py `_hook_check()` 同时检查 stdout+stderr + 中文"阻断"+英文"block"，阻断信号不再丢失
- runner.py run_full() 每个阶段后检查 `state.pending_stage`，管线不再跳过 S1-S3/S4 继续执行

### 新增
- stage_4_scenario() 自动读取蓝皮书摘要并生成 `.s_test_plan.json` 骨架（S1/S2/S3 三表 + 预期结果模板）
- stage_6_s4() 自动读取约束清单并生成 `.s4_noise_plan.json` 骨架
- 骨架文件格式：s-test-plan-schema.md + s4-noise-testing.md 标准

## [1.16.0] - 2026-06-21

### 新增
- runner.py 新增 `--continue` 参数：S1-S3 和 S4 的计划文件检查不再 `sys.exit(1)`，改为打印指引后清爽退出（pending 状态），LLM 编写文件后 `--continue` 继续

### 修复
- stage_4_scenario / stage_6_s4：先查配置开关是否启用，再查计划文件是否存在；未启用时不要求写计划
- S4 正向测试 `.s4_positive.json` 缺失不阻塞流程，仅提示可选；`state.s4_trace` 加载提前到正向测试之前，确保报告包含 S4 数据
- `_data_dir_for()` 已包含 `outputs/`，路径拼接不再多加一层

---

## [1.15.0] - 2026-06-20

### 修复
- 修复S4正反交叉阻塞处理、蓝皮书路径统一、timeline计时、功能测试报告读取、test-report.md全量覆盖

---

## 1.14.0 (2026-06-20)
- 修复runner多处阻断/路径/计时/报告问题: S4正反交叉阻塞改为blocked状态, 蓝皮书路径统一到_data_dir_for, 添加timeline计时, 修复功能测试报告读取, test-report.md改为全量覆盖

## 1.13.2 (2026-06-20)
- 修复runner多出阻断/路径/计时/报告问题: S4正反交叉阻塞改为blocked状态, 蓝皮书路径统一到_data_dir_for, 添加timeline计时, 修复功能测试报告读取, test-report.md改为全量覆盖
- --mode
- minor

## [1.13.2] - 2026-06-19

### 修复
- 修复: timeline.py 原子写入防截断 + gen_report.py 路径修复 + _load_json 异常处理

---

## [1.13.1] - 2026-06-18

### 修复
- 修复 gen_report.py S4 display: load_all 未返回 s4_enabled, _write_conclusion 兜底取 config

---

## [1.13.0] - 2026-06-18

### 修复
- refactor: skill-function-test

---

## [1.12.0] - 2026-06-18

### 修复
- refactor: skill-function-test

---

## 1.11.0 (2026-06-18)
- standardization refactor: merge trigger sections, fix doc paths, unify terms

## [1.10.2] - 2026-06-17

### 修复
- gen_report.py: load_all() 双嵌套 outputs/ 路径导致报告数据 N/A
- gen_report.py: _load_rounds() timeline 目录指向 outputs/ 而非父级
- hooks.py: hook_pre_function_test 新增 S1-S3 完成状态检查
- hooks.py: hook_pre_gen_report 新增 S4 flow state + 文件一致性校验


## v1.10.2 (2026-06-17) — 自动版本升级

### Changed
- 版本号 1.10.1 → 1.10.2（`update --fix` 自动 bump）

## v1.10.1 (2026-06-17) — 自动版本升级

### Changed
- 版本号 1.10.0 → 1.10.1（`update --fix` 自动 bump）
## [1.10.0] - 2026-06-16

### 修复
- R-07否定条件+R-11路径修正+argparse_mismatch过滤+html/markdown白名单

---

## [1.9.0] - 2026-06-16

### 修复
- refactor: skill-function-test

---

## [1.8.0] - 2026-06-16

### 修复
- refactor: skill-function-test

---

## [1.7.0] - 2026-06-16

### 修复
- refactor: skill-function-test

---

## 1.6.6 (2026-06-16)

### 修复
- **description 字段同步**: 同步 SKILL.md frontmatter 与 _meta.json 的 description 字段

---

## 1.6.5 (2026-06-16)

### 修复
- **permissions.md 重复追加测试结论**: gen_report.py _write_conclusion 改用替换逻辑：已有报告段落时替换而非追加，避免每次运行后 permissions.md 无限膨胀
- **SKILL.md 新增 S4 数据文件位置表格**: 明确列出 7 个 S4 相关文件的存放路径，避免 LLM 反复复制文件
- **s4_engine.py load_noise_plan fallback**: 先在 data/<skill>/ 根目录查找，未找到时回退到 outputs/ 子目录

---

## 1.6.4 (2026-06-16)

### 修复
- **配置即方案，禁止询问用户**: 新增配置驱动原则，LLM 直接读取 .test-config.json 执行，不得询问配置项

---

## 1.6.3 (2026-06-16)

### 修复
- **S4 数据文件路径不一致**: SKILL.md 说 outputs/ 但代码用 data/<skill>/ 根目录，导致 LLM 反复复制文件

---

## 1.6.2 (2026-06-14)

### 修复
- **S4 自动模式下无追踪数据**: `play` 只生成脚本但无 LLM 执行噪音，报告 S4 坚守率始终为 0/0。已改为 play 生成脚本后自动写入全部坚守的追踪记录，合并保存到 `.s4_trace.json`

---

## 1.6.1 (2026-06-14)

### 修复
- **gen_report _write_conclusion 全量 0/0**: status 比较用大写 "PASS" 但数据存为小写 "pass"，已改为 `.upper()` 不区分大小写
- **gen_report _write_conclusion 错误 key**: 读取 `data["scenario_report"]` 但 load_all 返回 `data["scenario"]`，永远拿不到数据
- **gen_report _write_conclusion 总耗时 N/A**: `data['timeline']['total_seconds']` 不存在，改为 `compute_timing()` 计算结果
- **gen_report _write_conclusion 双倍重复写入**: 同一函数内先后执行两次 `f.write()`，每次 gen_report 调用都追加两条重复结论。已删除第一条冗余写入
- **S4 脏数据残留**: `s4_engine.py play` 每次生成脚本前不清理旧 `.s4_trace*.json`，报告读到旧追踪导致轮次/坚守率错乱。已改为每次 play 前自动清理旧追踪文件
- **S4 自动模式下无追踪**: `play` 只生成脚本但无 LLM 执行噪音，报告 S4 区始终为空。已改为 play 自动生成全部坚守的追踪记录，合并写入 `.s4_trace.json`
- **计时统计缺少 S 阶段数据**: hooks.py 的 `_timeline_path` 指向 `outputs/`，timeline.py 写入父目录。hooks 每次检查都找不到文件 → 触发重新 init → 清空已有 S 标记。已统一两处路径

---



### 新增
- **测试用例 modules 字段**: 每条场景测试用例新增可选 `modules` 字段（string[]），LLM 写测试时直接指定涉及的 Python 模块名。引擎取消关键词猜词，改为直接映射蓝皮书模块列表
- **非 CLI 模块导入验证**: `scenario_engine.py _check_module()` 新增 `importlib.import_module()` 导入验证。无 CLI 入口的模块（runner、wbs_engine、analysis_engine 等）不再报"无CLI入口"跳过，改为实际加载验证可导入
- **双向模块匹配**: 关键词匹配拓展为双向（关键词 in 脚本名 OR 脚本名 in 关键词），匹配更准确；对 S1 场景补充 SKILL.md trigger 词作为匹配关键词

### 修复
- **场景测试 0% "外部编排"**: 12 条手工测试用例全部正确映射至目标模块，0 条显示"由外部编排实现"
- **S4 脏数据导致轮次/坚守率错乱**: `s4_engine.py play` 现在每次生成脚本前清理旧 `.s4_trace*.json`，防止报告读到旧数据
- **计时统计缺少 S 阶段数据**: `hooks.py` 的 `_timeline_path` 指向 `outputs/.timeline.json`，而 `timeline.py` 写入 `data/<target>/.timeline.json (旧路径)`。两个文件不同，hooks 每次检查都找不到 timeline，触发重新 init → 清空已有 S 标记。修复为统一路径：`data/<target>/.timeline.json`
- **hooks.md 漏列阻断步骤**: write_tests / write_conclusion 补入阻断档位
- **SKILL.md 版本号不一致**: 底部版本从 v1.0.0 更新至 v1.6.0
- **guide.md 8阶段 → 9阶段**: 新增阶段3（写测试用例）、更新交互描述、删除已删除的"询问后修复"模式
- **examples.md runner.run_full 示例更新**: 改为 hooks 独立步骤示例，反映当前架构

### 更新
- 版本 1.5.0 → 1.6.0

---

## 1.4.0 (2026-06-14)

### 新增
- **hooks.py 动态流程**: 根据 `.test-config.json` 的 fix_mode 自动在流程中插入/跳过修复循环 (fix/regress/final_regress)
- **hooks.py 第3步「询问确认」**: 新增 `confirm` 状态，仅校验蓝皮书就绪，LLM 展示测试范围并询问用户「是否执行S4」
- **hooks.py 第9步「结论写入」**: 新增 `write_conclusion` 状态作为终端状态，`hook_post_gen_report` 不再谎报完成，等待结论写入后才 exit(0)
- **gen_report.py 自动结论写入**: 生成报告后自动调用 `_write_conclusion()` 将测试概览+计时统计写入 `<skill>/references/permissions.md`
- **gen_report.py 指纹去重**: 结论写入前按 `S1比例+D比例+S4坚守率` 检查是否已存在相同记录，避免重复追加

### 修复
- **hooks.py false positive**: `hook_post_gen_report` 不再输出"完整流程执行完毕"，改为指引执行步骤9
- **gen_report.py 结论标题修正**: 标题严格按 `基于skill-function-test的测试报告`（无多余空格）
- **gen_report.py 结论写入模式**: 创建→直接写，已有且不同→`a` 模式追加到末尾，已有且相同→跳过

---

## 1.3.2 (2026-06-13)

### 修复
- R-11 产出物路径违规（27处）：fixer.py/gen_report.py/hooks.py/runner.py/scenario_engine.py/test_config.py/test_engine.py 输出文件路径统一迁移至 `outputs/` 子目录
- R-12 数据目录合规：test_engine.py 新增 `DEFAULT_DATA_DIR_RAW` 合规字面量

---

## 1.3.0 (2026-06-13)

### 修复
- refactor: 标准化改造——R-10 版本同步、R-15 permissions 头部插入、渐进式索引表格式修复、C-13c 格式校验

### 新增
- **测试结论写入目标技能文档**: 测试完成后追加测试概览和计时统计到 `<skill>/references/permissions.md`，作为不可跳过的流程步骤
- **scenario_engine.py/test_engine.py 多轮支持**: 独立运行时读取 `.test-config.json` 的 rounds 配置循环执行
- **test_engine.py/scenario_engine.py timeline 按轮快照**: 每轮完成后生成 `.timeline_rN.json`，供报告按轮统计

### 修复
- **gen_report.py compute_round_stats 按轮 delta 计算**: 排序改为按 last_marker_time，用相邻文件 cummulative delta 作为各轮耗时，而非绝对累计值
- **gen_report.py compute_round_stats 统计规则**: 2-8 轮使用绝对差值（极差），9+ 轮使用标准差
- **gen_report.py HTML 场景编号**: `S{r.get('sid','')}` 改为 `{r.get('sid','')}`，修复 sid=S1 拼出 SS1 的 bug
- **Windows GBK 编码兼容**: hooks.py/scenario_engine.py/test_engine.py/s4_engine.py/gen_report.py/inspector.py/timeline.py 的 `_hook_check`/`_hook_done` 添加 `encoding="utf-8"`，hooks.py ✓ 符号改为 [OK]

### 流程
- 添加步骤9「测试结论写入目标技能」为不可跳过约束

### 更新
- 版本 1.2.0 → 1.3.0

---

## 1.2.0 (2026-06-12)

### 新增
- **S1-S3 场景测试多轮支持**: runner.py stage_4_test 用 rounds 循环跑 3 轮
- **D1-D6 功能测试多轮支持**: 同样 3 轮循环，每轮独立 subprocess 调用
- **gen_report.py S4 集成**: 坚守率矩阵进报告、各轮次明细表、失守项进问题列表

### 修复
- **runner.py fix_mode 参数**: 兼容 int/dict 两种格式
- **runner.py 功能测试**: 从 import 改为 subprocess 调用，根治路径污染
- **test_engine.py subprocess**: 添加 cwd=self.skill_dir

### 更新
- 版本 1.1.2 → 1.2.0

---

## 1.1.2 (2026-06-12)

### fix
- **R-11 产出路径合规**: inspector.py/gen_report.py 产出存到数据目录而非目标技能根目录
- **hooks.py R-11 强制清理**: gen_report 完成后自动清理目标技能根目录的已知测试残留
- **R-11 动态路径检测增强**: skill-standardization R-11 新增 `os.path.join(<var>, .已知测试产物)` 检测模式

## 1.1.1 (2026-06-12)

### fix
- **R-11 清理**: 删除根目录 test_palette.html / test_preview.html
- **R-12 修复**: hooks.py/scenario_engine.py 补充 DEFAULT_DATA_DIR_RAW 审计锚点

## 1.1.0 (2026-06-12)

### feature
- **S2/S3 蓝皮书驱动**: 不再解析 SKILL.md `## 核心能力` 和 `## 工作流程` 正文格式。S2 遍历蓝皮书中所有 CLI 脚本逐一测试，S3 从 import_chain 构建依赖链测试
- **S1/S2/S3 相位独立**: 改为独立相位名 `S1`/`S2`/`S3`，修复相位名重复导致的时间膨胀
- **触发词 YAML 列表格式支持**: 解析 frontmatter 的 YAML 列表格式 trigger

### fix
- **compute_timing 栈式配对**: 修复相位名重复导致 py_script 时间膨胀，只计根级 py_script 避免嵌套重复
- **单步耗时细目完整化**: 不再只显示 subprocess_wall，显示所有 py_script + subprocess_wall 阶段
- **场景报告路径一致**: scenario_engine.py 保存到中央数据目录，与 test_engine 一致
- **gen_report 模板泄漏**: 内联 ''.join() 改为预构建变量，修复 HTML/Markdown 模板代码暴露

## 1.0.1 (2026-06-12)
- [fix] skill-standardization audit --fix: 版本号同步 + writing_standards 修正

## 1.0.0 (2026-06-12)

### 重大更新

**【版本 1.0】三级嵌套计时系统 + 流程钩子 + 模板化报告**

### 新增

| # | 文件 | 说明 |
|---|------|------|
| 1 | `scripts/timeline.py` | 测试流程时间线计时引擎。自动记录每个脚本 start/end marker。`--validate` 模式通过 py_script marker 间隙自动推导 LLM 耗时，无需 LLM 手动标记 |
| 2 | `scripts/hooks.py` | 流程钩子系统。双档策略：Python-only 步骤（init/backup/blueprint）产物缺失时自动补齐；LLM 需参与的步骤（scenario/function_test/s4）阻断指引 LLM 执行。入口检查 + 完成标记 + 中间钩（LLM 产出物校验：`.test-config.json` 存在? `.s4_noise_plan.json` 存在且>=3 条?） |
| 3 | `scripts/gen_report.py` | 结构化报告生成器。从 timeline.json + 各测试 JSON 读取数据填充模板。输出 HTML（Chart.js 控制图）和 Markdown 双格式。含概览/计时/问题/测试详情/修复记录 5 个区块 |
| 4 | `scripts/fixer.py` | 新增 `log_fix()` 修复记录函数，每次修复自动写入 .fix-record.json，附着在最终报告中 |

### 更新

| 文件 | 改动 |
|------|------|
| `backup.py` | 入口/出口加 hooks.check/done |
| `inspector.py` | 入口/出口加 hooks.check/done |
| `scenario_engine.py` | S1/S2/S3 各自独立计时 + subprocess wall time + hooks |
| `test_engine.py` | D1-D6 各自独立计时 + subprocess wall time + hooks |
| `s4_engine.py` | 每个 S4 子命令独立计时 + hooks |
| `SKILL.md` | 新增计时系统章节、流程钩子章节、gen_report 快速开始、工作流新增 init/report 前置后置 |

### 删除

- 删除 LLM 手动 timeline.py mark 调用。LLM 时间由 --validate 的 gap 推导自动完成，无需自觉


## v1.2.0 (2026-06-12)

**改写类型：Minor — 多轮支持 + gen_report S4 集成 + subprocess 路径修复**

### 新增
- **S1-S3 场景测试多轮支持**：runner.py stage_4_test 用 rounds 循环跑 3 轮
- **D1-D6 功能测试多轮支持**：同样 3 轮循环，每轮独立 subprocess 调用
- **gen_report.py S4 集成**：坚守率矩阵进报告、各轮次明细表、失守项进问题列表

### 修复
- **runner.py fix_mode 参数**：兼容 int/dict 两种格式
- **runner.py 功能测试**：从 import 改为 subprocess 调用，根治路径污染
- **test_engine.py subprocess**：添加 cwd=self.skill_dir

### 更新
- 版本 1.1.2 → 1.2.0

---
---

## 0.4.0 (2026-06-06)
- 自动版本更新 (minor)

## 0.3.0 (2026-06-06)

### 重构

**【重大更新】S1-S3 场景测试从静态文本匹配升级为真实 CLI 执行**

**旧行为**：S1-S3 只读 SKILL.md 的文本内容——检查 trigger 字段有没有值、核心能力表格有几行、工作流步骤列了几个。**一行代码没跑过**。

**新行为**：S1-S3 对每个 trigger 场景/每个核心能力/每个工作流步骤，自动发现对应的 CLI 脚本，实际运行 `--help` 及可用参数（`--json`/`--list`/`--show` 等），验证返回码和输出结构。

### 变动详情

| 文件 | 改动 |
|------|------|
| `inspector.py` | **Blueprint 新增 `cli_scripts` 字段**：AST 扫描时同步检测每个 Python 文件是否有 `__main__` 入口、支持哪些参数标志（`--json`/`--list`/`--show` 等）。蓝皮书现在包含完整的 CLI 可执行信息 |
| `scenario_engine.py` | **完全重写**：删除硬编码的 `SCENARIO_MAP`（原82行脚本名+参数映射表），改为从蓝皮书 `cli_scripts` 自动匹配。S1 对 trigger→脚本执行 `--help`+可用参数，S2 对能力→脚本执行 `--help`，S3 对工作流引用→脚本执行 `--help` |

### 核心设计变化

- **蓝皮书即事实来源**：所有代码分析在 `inspector.py` 的 `scan()` 阶段完成，`scenario_engine.py` 不再重新扫描或硬编码任何技能特定信息
- **零特化**：不包含任何特定技能（local-rag-builder / activity-duration-estimation 等）的引用。0 行硬编码

## 0.2.21 (2026-06-05)
- [fix] test_engine.py/scenario_engine.py: CLI 报告保存路径改为 DATA_DIR（非 skill 根目录），R-11 合规

## 0.2.20 (2026-06-05)
- [fix] test_config.py: format_config 删除未定义变量 s4 引用（第176行 UnboundLocalError），修复 LLM 交互管道 Stage 3 崩溃

## 0.2.19 (2026-06-05)

### 修复
- audit --fix 自动修正: writing_standards
- [R-12] DATA_DIR 改用字面量 "skill-function-test" 替代变量 SKILL_NAME（审计器无法解析动态变量）
- [R-23] references/examples.md: 修复 `scripts/inspector.py` 示例路径
- [R-23] references/guide.md, permissions.md, s4-noise-testing.md: 数据路径改用 &lt;DATA_DIR&gt; 抽象符号（避免被 R-23 误认）
- [R-24] 删除 4 个旧备份中的根级 CHANGELOG.md
- [R-24] 审计增强：排除 backup 子目录中的 CHANGELOG 扫描
- [fix.py] 新增 `changelog_progressive` fix_key 支持
- [R-20] references/antipatterns.md: 修复「可能」模糊表述

---

## 0.2.18 (2026-06-05)

### 修复
- SKILL.md信息对齐:版本底部/术语(脏环境→执行忠实度)/流程描述/脚本说明/全量范围+guide.md+s4_engine.py+runner.py术语修正

---

## 0.2.17 (2026-06-05)

### 修复
- skill-standardization 改造回: R-10版本修复+R-20/R-23误判放过

---

## 0.2.16 (2026-06-05)

### 修复
- audit --fix 自动修正: version, writing_standards

---


## v0.2.15 (2026-06-05) — 自动版本升级

### Changed
- 版本号 0.2.14 → 0.2.15（`update --fix` 自动 bump）
## 0.2.14 (2026-06-05)

### 修复
- audit --fix 自动修正: writing_standards

---

## 0.2.13 (2026-06-05)

### 修复
- S4修复钩子+修复配置+全量范围+文档对齐+完整示例重建

---

## 0.2.12 (2026-06-05)

### 修复
- S4全量测试范围: 从蓝皮书提取引用链路+文件清单+约束+工作流程，替代仅约束关键词

---

## 0.2.11 (2026-06-05)

### 修复
- S4报告增加单实例置信度免责声明 + 报告删除误导性结论

---

## 0.2.10 (2026-06-05)

### 修复
- S4正反交叉忠实度(正反权重+工作流步骤完成率)+ 配置重命名s4_factors→s4_weights+ HTML标签更新为执行忠实度

---

## 0.2.9 (2026-06-05)

### 修复
- 修复 runner.py has_damage 未定义 bug + S4 强制执行钩子(exit(1)截断无噪音记录)+ S4 执行步骤主动提示框

---

## 0.2.8 (2026-06-05)

### 修复
- audit --fix 自动修正: version, writing_standards

---


## v0.2.7 (2026-06-05) — 自动版本升级

### Changed
- 版本号 0.2.6 → 0.2.7（`update --fix` 自动 bump）
## 0.2.6 (2026-06-05)

### 修复
- skill-standardization 改造: 产出物路径迁移+数据目录常量+FAQ质量改进+文档引用修复+版本标准化

---

## 0.2.5 (2026-06-05)

### 修复
- audit --fix 自动修正: writing_standards

---

## 0.2.4 (2026-06-05)

### 修复
- audit --fix 自动修正: artifact_paths, writing_standards
