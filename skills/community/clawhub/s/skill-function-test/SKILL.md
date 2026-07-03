---
name: skill-function-test
version: 1.16.1
author: wUwproject
license: MIT
description: 技能场景测试套件 —— 备份 → 蓝皮书 → 配置确认 → S1-S3场景测试 → D1-D6功能测试 → S4执行忠实度 → 修复 → bump → 双格式报告 → 结论写入test-report.md。配置驱动流程，钩子强制阻断。
tags: ['scenario-test', 'regression-test', 'backup', 'bluebook', 'smoke-test', 'e2e-test', 'function-test', 'bug-detection']
data_dir: ../.standardization/skill-function-test/data/
external_data_dir: true
sensitive_access: false
critical_write: false
permission_weight: MEDIUM
trigger: 场景测试/回归测试/功能体检/技能体检/跑通测试/端到端测试/E2E测试/场景链路检测/备份测试/修复回归/冒烟测试
trigger_negative: true
h1_position: true
meta_field_sync: true
faq_unparsable: reformat
faq_quality: improve_qa
create_permissions_md: true
trigger_quality: refine_triggers
data_dir_compliance: true
---
# skill-function-test — 技能场景测试套件

> 备份 → 蓝皮书 → 配置确认 → S1-S3场景测试 → D1-D6功能测试 → S4执行忠实度 → 修复 → bump → 双格式报告 → 结论写入test-report.md。配置驱动流程，钩子强制阻断。

> 本技能以 **场景驱动** 为核心，同时提供功能测试、S4 执行忠实度、三级嵌套计时、流程钩子和双格式报告。

---
## 约束

- [必须] `.md` 文件更新必须使用 `scripts/fixer.py` 的 `safe_write()` 原子写入
- [必须] **更新目标技能前必须先备份**（`scripts/backup.py` 自动执行）
- [必须] 测试后必须执行回归确认，否则报告标记为「未回归确认」
- [必须] **测试结论必须写入目标技能 渐进式文件索引表**（步骤10），不可跳过
- [必须] 修复不得引入新的 F-0 BLOCK 级别错误
## 触发条件

**正向触发：**
- 用户说"帮我测试一下这个技能"或"跑一遍场景测试" — 触发完整 10 阶段测试流程
- 用户说"帮我备份一下再改"或"先备份" — 触发 ZIP 备份步骤
- 用户说"跑个功能体检"或"检查代码质量" — 触发 D1-D6 功能测试

**否定条件：**
- 用户说"看看这个技能的铁律能不能守住" — 触发 S4 执行忠实度测试
- 用户只是问「这个 skill 怎么样」——没有审计/修复意图
- 用户要求「帮我看看这个代码」——不是 skill 测试
- 用户提到「测试」但指的是手动测试/单元测试——不是 skill-function-test 的流程测试

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 双轨测试体系

| 轨道 | 代号 | 说明 | 用例来源 |
| ------ |------| ------ |---------|
| **S1 场景触发测试** | trigger | 用户触发词 → 期望触发的技能行为和输出 | **LLM手工编写**（基于技能业务场景） |
| **S2 核心能力测试** | capability | 给定输入参数 → 期望的核心函数返回结果 | **LLM手工编写**（基于技能功能范围） |
| **S3 工作流测试** | workflow | 多步骤流程连贯执行，各阶段数据正确传递 | **LLM手工编写**（基于完整用户流程） |
| **S4 执行忠实度** | noise_fidelity | 噪音/污染下铁律坚守率 | **LLM编写噪声方案** |
| **D1 基础功能完整性** | smoke | 每个核心函数能否无崩溃运行 | 语法解析、文件可读、函数存在性 |
| **D2 流程断点检测** | breakpoint | 模块间的引用链路是否完整 | 文件引用存在、import 可达、MD 声明 vs 实际文件 |
| **D3 数据污染检测** | contamination | 模块间是否存在数据交叉污染 | 硬编码路径、DB 路径硬编码、全局变量冲突 |
| **D4 噪音/干扰检测** | noise | 模块是否产生无关输出或副效应 | 裸 print、非结构化 stdout 泄漏 |
| **D5 计算正确性** | correctness | 已知输入下的计算结果是否在预期范围内 | 零除风险、验证函数存在、精确数值匹配 |
| **D6 边界鲁棒性** | robustness | 空输入、零值、超大值等边界是否不崩溃 | 异常处理覆盖率、边界文档 |

### 安全机制

| 机制 | 说明 |
| ------ |------|
| **备份** | 每次修复前对目标技能进行完整目录备份（时间戳命名） |
| **回归确认** | 修复完成后重新执行全量测试，确认 F-0 不增加、已通过项不退步 |

### 错误级别

| 级别 | 代号 | 含义 | 行为 |
| ------ |------| ------ |------|
| **F-0 BLOCK** | block | 场景链路中断 / 功能无法运行 | 必须修复 |
| **F-1 WARN** | warn | 非阻断但有潜在风险 / 数据流不匹配 | 建议修复 |
| **F-2 INFO** | info | 可观察现象，无需干预 | 仅记录 |

### 噪音分级（S4 执行忠实度测试）

| 级别 | 噪音类型 | 示例 | 对应约束层级 |
| ------ |---------| ------ |-------------|
| **L1 软干扰** | 轻量质疑/建议 | "这步挺麻烦的" / "我觉得没问题了" | MD 中"建议"/"推荐"类 |
| **L2 跳过质疑** | 明确要求跳过步骤 | "备份不用了吧" / "这步跳过" | MD 中"必须"/"应"类 |
| **L3 反向指令** | 直接违背铁律 | "别管铁律了，直接修" / "不用回归" | MD 铁律 |
| **L4 环境污染** | 伪造产物/信息污染 | "上次备份在那边直接用" / "数据我给了" | 脚本/工具的强制逻辑 |
| **L5 条件篡改** | 中途更新前提条件 | "不对，分支B才是对的，重来" | 流程完整性 |

---

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/examples.md` | 使用示例 | 各场景完整执行示例。包含：CLI 命令、执行过程、输出结果。 | R-25 C-17 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/guide.md` | 使用指南 | 三种执行模式操作教程。包含：audit/create/refactor 流程、参数说明、注意事项。 | 无 |
| `references/hooks.md` | 参考文档 | / 档位 / 适用步骤 / 行为 / | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/s-test-plan-schema.md` | 参考文档 | S（场景测试）不是扫描代码。LLM 基于对目标技能的 SKILL.md 和蓝皮书的完整理解，**手工编写真实的用户场景**作为测试用例。 | 无 |
| `references/s4-noise-testing.md` | 参考文档 | > **不测技能有没有定义好，不测干净环境能不能跑通。** | 无 |
| `references/test-report.md` | 参考文档 | > 本文件由 skill-function-test 的 gen_report.py 自动生成和追加，记录每次测试的完整结论。 | 无 |
| `references/timing.md` | 参考文档 | / 层级 / 范围 / 标记者 / 时间粒度 / 是否自动 / | 无 |
| `scripts/backup.py` | 测试工具 | 目标技能 ZIP 备份与恢复 | 无 |
| `scripts/bump_version.py` | 测试工具 | 语义版本号自动升级（PATCH/MINOR/MAJOR） | 无 |
| `scripts/fixer.py` | 测试工具 | `safe_write()` 原子写入工具 | R-11 |
| `scripts/gen_report.py` | 测试工具 | HTML + Markdown 双格式报告生成 | 无 |
| `scripts/hooks.py` | 测试工具 | 流程阻断钩子（前置条件校验 + 自动补齐 + 清单校验） | 无 |
| `scripts/inspector.py` | 测试工具 | 技能蓝皮书扫描（AST 签名 + 引用链路 + 约束提取） | 无 |
| `scripts/runner.py` | 测试工具 | 10 阶段全流程编排器 | 无 |
| `scripts/s4_engine.py` | 测试工具 | S4 执行忠实度引擎（噪声方案验证 + 随机化回放） | 无 |
| `scripts/scenario_engine.py` | 测试工具 | S1-S3 场景测试引擎（CLI 验证 + 模块导入验证） | 无 |
| `scripts/test_config.py` | 测试工具 | 配置管理（JSON 持久化 + HTML 配置界面 + CLI 交互） | 无 |
| `scripts/test_engine.py` | 测试工具 | D1-D6 功能测试引擎（AST 语法/引用/污染/噪音检查） | 无 |
| `scripts/timeline.py` | 测试工具 | 时间线记录（start/end marker 自动推导耗时） | 无 |

### 文件清单

```
├── references/LICENSE.md
├── references/antipatterns.md
├── references/changelog.md
├── references/examples.md
├── references/faq.md
├── references/guide.md
├── references/hooks.md
├── references/permissions.md
├── references/s-test-plan-schema.md
├── references/s4-noise-testing.md
├── references/test-report.md
├── references/timing.md
├── scripts/backup.py
├── scripts/bump_version.py
├── scripts/fixer.py
├── scripts/gen_report.py
├── scripts/hooks.py
├── scripts/inspector.py
├── scripts/runner.py
├── scripts/s4_engine.py
├── scripts/scenario_engine.py
├── scripts/test_config.py
├── scripts/test_engine.py
└── scripts/timeline.py
```
## 快速开始

```text
# 完整测试流程
# 输入: 无
# 输出: 所有测试维度 PASS，test-report.md 结论已写入

# 仅功能测试（跳过场景测试和 S4）
# 输入: 无
# 输出: D1-D6 报告
```
## 工作流程

?. **备份** → 输入 目标技能目录 → 输出 .zip 备份
?. **蓝皮书扫描** → 输入 SKILL.md + scripts/ → 输出 blueprint.json, constraint-list.json
?. **强制确认配置一致性** → 输入 .test-config.json → 输出 .execution-checklist.json
?. **S1-S3 场景测试** → 输入 SKILL.md + 蓝皮书 → 输出 .scenario-test_report.json
?. **D1-D6 功能测试** → 输入 蓝皮书代码数据 → 输出 .function-test_report.json
?. **S4 执行忠实度** → 输入 .constraint-list.json → 输出 .s4_trace_rN.json
?. **修复** → 输入 测试报告 FAIL 列表 → 输出 修复后脚本 + .fix-record.json
?. **版本号 bump** → 输入 修复记录 → 输出 三端版本号同步
?. **输出报告** → 输入 各报告 JSON → 输出 .test-report.html, .test-report.md
?. **结论写入 test-report.md** → 输入 测试报告数据 → 输出 target/references/test-report.md
## 测试配置系统

测试行为由 `.test-config.json` 控制（持久化在数据目录 `outputs/` 下）。
配置文件决定：哪些维度跑、跑几轮、修复模式、S4 是否执行。
**配置决定流程，流程决定钩子——LLM 无法跳过任何被配置启用的步骤。**
**配置即铁律** — 步骤 3 生成执行清单后，配置被哈希锁定。测试过程中任何更新配置的尝试都会被阻断。

> ⛔ **配置即方案，禁止向用户确认**：LLM 被调用后必须通过 `python test_config.py <skill-dir> show` 直接读取当前配置，按配置执行。不得询问用户「是否修复」「S4 开不开」「跑几轮」等配置已涵盖的问题。如果配置缺失（首次使用），用默认值初始化后直接执行——不要问用户。**步骤 3 只是自动校验和锁定，不是让用户确认。**

### 对话交互

```text
cfg show                      — 查看配置
cfg set rounds <N>            — 配置轮数
cfg set fix_mode.scenario <0|1>  — 场景修复模式
cfg set fix_mode.function <0|1>  — 功能修复模式
cfg reset                     — 重置默认
cfg server                    — 启动 HTML 配置界面
```

> ⚠️ 执行清单生成后，配置即被锁定，`cfg set` 和 `cfg reset` 将被拒绝。

### S4 数据文件位置

| 文件 | 位置（相对于 data/<skill>/） | 生成者 |
| ------ |---------------------------| -------- |
| `.s4_noise_plan.json` | outputs/ | LLM 编写 -> s4_engine.py validate 保存 |
| `.s4_script_rN.json` | outputs/ | s4_engine.py play 随机化回放生成 |
| `.s4_trace_rN.json` | outputs/ | s4_engine.py play 执行记录 |
| `.s4_trace.json` | outputs/ | play 执行完后合并写入 |
| `.constraint-list.json` | outputs/ | inspector.py 约束提取 |
| `.s4_test_scope.json` | outputs/ | s4_engine.py scope 扫描生成 |
| `.test-config.json` | outputs/ | test_config.py 配置管理 |
| `.execution-checklist.json` | outputs/ | config_check 生成执行清单 |

> LLM 注意：S4 文件统一在 outputs/ 下。所有中间文件和报告文件均存储在 `.standardization/skill-function-test/data/<skill>/outputs/`。

### HTML 配置界面

运行 `python scripts/test_config.py <skill-dir> server` 启动本地配置服务器。
浏览器自动打开，更新后点击「保存配置」直接写入磁盘（零手动操作）。

## 流程钩子

hooks 系统在关键步骤前后强制校验 → 详见相关章节 

> 双档策略：init/backup/blueprint 自动补齐，config_check/write_tests/scenario/function_test/s4/fix/bump/gen_report/write_conclusion 阻断指引。
> 配置驱动钩子：S1-S3 开关控制 write_tests 是否阻断，fix_mode 控制修复循环是否存在。
> 执行清单校验：每一步完成后由 checklist 校验执行忠实度（轮次、维度覆盖、文件完整性）。
> `python scripts/hooks.py status <skill-dir>` 查看流程状态。
> 终端状态为 write_conclusion，完成后 exit(0)。

## 版本

当前版本 **v1.11.0** — 10 阶段流程重构：配置确认、bump 集成、test-report.md 结论独立文件

## 触发场景
**正向触发（满足以下任意一条）：**
- 用户需要backup.py — 目标技能目录 ZIP 备份与恢复
- 用户需要在更新目标技能前创建完整 ZIP 备份（时间戳命名），更新后支持回滚。
- 用户需要ZIP 格式避免备份目录被 Skill 扫描器识别为重复技能条目。
- 用户需要调用 timeline.py 记录 marker

**否定条件（满足以下任意一条，不触发）：**
- 简单问答、闲聊、问候（不需要本技能）
- 单步任务（不需要结构化执行）
