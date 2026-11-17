---
name: "zero-cover-mode"
description: "零稀泥模式：bug修复→自动生成测试+跑全量回归+标注根因+周报+重复bug重构警报"
version: "1.0.0"
---

# 零稀泥模式（Zero Cover Mode）

> **⚠️ 重要：路径约定**
> - 本技能脚本位于 `skills/zero-cover-mode/lib/`
> - agent CWD 为 workspace 根目录
> - 执行 CLI 命令时请使用完整路径：`python skills/zero-cover-mode/lib/<module>.py <action> <args>`
> - 也可以先 `cd skills/zero-cover-mode/` 然后使用 `python lib/<module>.py`
> - 详见 `§ 附录C：执行路径指南`

## 概要
每次修复 bug 强制执行的四阶段闭环：**环境检测 → 根因分析 → 测试验证 → 闭环归档 → 上线验证**。
同一类型 bug 重复出现时自动拉重构警报。所有产出以 `bugs/{bug_id}/` 目录隔离，支持多 session 并发安全运行。

---

## 0️⃣ 前置条件（跨会话安全）
> [强制] 每个新会话在修复任何 bug 之前，必须先 **read** 以下文件：
> - `FIX_CLOSURE_LOG.ndjson`
> - `.zero-cover-state.json`
>
> claw-guardian 插件的 read 前置检查是按**会话独立触发**的。
> 即使其他会话读过，本会话没读前依然禁止 edit/write/exec 写入上述文件。
>
> 这是故意的安全设计——防止跨会话覆盖数据而不自知。

---

## 0.5️⃣ 项目环境检测

[强制] 每次修复开始时，必须先完成环境检测。结果写入 `.zero-cover-state.json` 的 `project_env` 字段。

### 检测步骤
```
1. 检测项目类型：
   if exists gateway.py in CWD:
       TEST_CMD = "gateway.py dispatch()"
       PROJECT_TYPE = "gateway_project"
   elif exists pyproject.toml or setup.py or pytest.ini:
       TEST_CMD = "pytest tests/ -v --tb=short"
       PROJECT_TYPE = "python"
   elif exists package.json:
       # 检测 JS 框架
       if "jest" in package.json:
           TEST_CMD = "npx jest"
       elif "vitest" in package.json:
           TEST_CMD = "npx vitest run"
       elif "mocha" in package.json:
           TEST_CMD = "npx mocha"
       PROJECT_TYPE = "node"
   else:
       print WARNING: "未检测到已知测试框架"
       print "请手动输入测试命令，或直接回车跳过："
       TEST_CMD = input("> ") or "skip"
       PROJECT_TYPE = "unknown"

2. 检测 VCS：
   if exists ".git":
       VCS = "git"
   elif exists ".svn":
       VCS = "svn"
   else:
       VCS = "none"

3. 检测并发状态：
   if exists ".zero-cover-state.json":
       读 active_session_ids
       如果当前 session 已在 active_session_ids 中 → 使用现有 bug_id
       否则 → 新 bug_id
   else:
       新建 .zero-cover-state.json
```

### 降级策略
| 检测结果 | 行为 |
|---------|------|
| 无测试框架 | Phase 2 降级为手动验证 + WARNING |
| 无 VCS | 回滚策略降级为"保留文件副本"（见 § 回滚流程） |
| 无 Python | Phase 2 的假数据检测用 JS/TS 版关键词 |

---

## 0.8️⃣ bug_id 自动生成规则

### 生成算法
```
bug_id = f"{mod_prefix}{type_prefix}{timestamp}_{rand_suffix}"

其中:
- mod_prefix: 模块名去除非字母字符，取前4个小写字母
  "algorithmic_novel_writer" → "algo"
  "one_novel_skill" → "onen"
  "claw-guardian" → "claw"
  "zero-cover-mode" → "zero"
- type_prefix: bug_type 取前3个小写字母
  "type_mismatch" → "typ"
  "config_error" → "con"
- timestamp: datetime.now().strftime("%y%m%d%H%M%S")
  "2026-06-28 21:28:30" → "2606282130"
- rand_suffix: 用 secrets.token_hex(2) 生成 4 位 hex
  → "a3f6"

完整示例:
  "algo-typ-2606282130-a3f6"
  "one-con-2606282130-b9e2"
```

### 去重保障
- 写入 `.zero-cover-state.json` 的 `bug_id_registry` 列表
- 生成后检查是否已存在 → 重新生成

---

## 一、触发条件
当以下任一情况发生时，本模式自动激活：
1. 用户要求修复某个 bug（显式或隐式）
2. 执行过程中发现失败的测试或异常
3. 系统日志中出现已知/未知的 error/warning 需要修复

---

## 二、文件隔离与并发安全

### 2.1 目录隔离策略

所有产出按 bug 隔离，存储在 `bugs/` 目录下：

```
workspace/
  bugs/{bug_id}/
    BUG_ROOT_CAUSE.md
    TEST_RESULT.md
    test_[module]_fix_[bug_shortname].py
    regression_output.log
    REVERT_LOG.md（如有回滚）
    evidence/          # 截图、日志等证据
  FIX_CLOSURE_LOG.ndjson       # 中央归档（仅 Phase 3 追加）
  REFACTORING_ALERT.md         # 中央归档（仅触发时追加）
  .zero-cover-state.json       # 全局状态
  tests/regression/            # 测试文件归入此目录
  reports/
    fix_closure_weekly_YYYY-Www.md
```

**好处**：
- 多个 session 并行修复互不覆盖
- 每个 bug 有完整的工作目录
- 取消修复后直接删除 `bugs/{bug_id}` 即可

### 2.2 原子写入规范

所有文件写入遵循以下规则：

| 操作 | 方式 | 说明 |
|------|------|------|
| `bugs/{bug_id}/` 内文件 | `write` 全量覆盖 | 每个 bug 一个实例，无冲突风险 |
| `FIX_CLOSURE_LOG.ndjson` | 原子追加 | 写临时文件 → `os.replace()`（跨平台安全） |
| `REFACTORING_ALERT.md` | 追加写 | Python `open("a")` 模式追加，保留历史 |
| `.zero-cover-state.json` | 读→改→原子写 | 读取全部 → 修改 → 写临时文件 → rename |
| `reports/*.md` | 全量重写 | 每次重新聚合生成 |

### 2.3 并发锁机制

对中央文件（`FIX_CLOSURE_LOG.ndjson`、`.zero-cover-state.json`）使用 `lib/` 模块的原子操作：

```bash
# state_manager: 读/写/注册/注销
python skills/zero-cover-mode/lib/state_manager.py read
python skills/zero-cover-mode/lib/state_manager.py register <session_id> <bug_id>
python skills/zero-cover-mode/lib/state_manager.py unregister <session_id>

# ndjson_schema: 校验/追加
python skills/zero-cover-mode/lib/ndjson_schema.py append <ndjson_path> '<json>'
python skills/zero-cover-mode/lib/ndjson_schema.py validate <ndjson_path>
```

所有 `lib/` 模块的写入操作使用 OS 级原子操作（写临时文件 → `os.replace()`），无需额外文件锁。

手动降级（lib 不可用时）：
```
1. 写临时文件 → os.replace() 覆盖原文
2. .zero-cover-state.json: 读全部 → 修改 → 写临时 → rename
```

### 2.4 Session 注册与注销

使用 `lib/state_manager.py` 管理 session 生命周期：

```bash
# 修复前注册
python skills/zero-cover-mode/lib/state_manager.py register <session_id> <bug_id>
# 修复完成注销
python skills/zero-cover-mode/lib/state_manager.py unregister <session_id>
```

手动降级：
```
1. 在 .zero-cover-state.json 的 sessions 中添加 session 记录
2. 设置 status=in_progress, bug_id, started_at
3. 完成时设置 status=completed, completed_at
4. 从 active_session_ids 中移除
```

---

## 三、四阶段闭环（每轮必执行）

### Phase 0 — 准备阶段
在执行修复前，按 §0.5 完成环境检测，按 §0.8 生成 bug_id，按 §2.4 注册 session。
产出：
- 写入 `.zero-cover-state.json` 注册 session
- 创建 `bugs/{bug_id}/` 目录

### Phase 1 — 根因分析（Root Cause）
1. 修复前，必须先定位根因并写入文件 `bugs/{bug_id}/BUG_ROOT_CAUSE.md`：
   - 标题、发现时间、影响范围
   - **5 Whys 分析法，明确定义每层标准**（见 § 四）
   - 临时缓解方案 vs 永久修复方案
2. 写入后运行深度验证：
   ```bash
   python skills/zero-cover-mode/lib/root_cause_validator.py check bugs/{bug_id}/BUG_ROOT_CAUSE.md
   ```
   如果输出 `blocking: true`（未达到 L3）→ **禁止进入 Phase 2**，补充分析
3. 然后才实施修复代码。

### Phase 2 — 测试验证（Test & Regression）
1. **生成活代码验证**：
   - 生成测试验证脚本时，严禁使用硬编码假数据
   - 通过 §0.5 检测到的 `TEST_CMD` 使用**真实项目数据**和**真实后端**进行验证
   - 测试证据必须来自活执行结果，而非手动伪造的断言预期
   - 验证方式：
     a. 构造真实请求参数（从项目业务数据中提取）
     b. 通过检测到的测试命令实际调用后端逻辑
     c. 捕获返回值、日志、数据库状态变化
     d. 基于实际返回值断言（而非预写假预期）
   - 测试文件命名格式：`test_[module]_fix_[bug_shortname].py`
   - 存放位置：`tests/regression/` 目录 + 复制到 `bugs/{bug_id}/`

2. **全量回归**：
   - 使用 §0.5 检测到的 `TEST_CMD`
   - 回归输出写入 `bugs/{bug_id}/regression_output.log`
   - 若回归失败 → 截图/日志归档，**不允许提交修复代码**
   - **若 TEST_CMD = "skip"（无测试框架）** → 标记 `test_skipped: true`，跳过全量回归，但必须做人工验证

3. **测试结果写入** `bugs/{bug_id}/TEST_RESULT.md`：
   ```markdown
   # 测试验证结果 — {bug_id}

   ## 环境
   - 测试时间: YYYY-MM-DD HH:mm (ISO8601)
   - 执行环境: {操作系统}/{Python 版本}/{Node 版本}
   - VCS: {git/svn/none} {commit hash}
   - 测试命令: {TEST_CMD}
   - 项目类型: {PROJECT_TYPE}

   ## 结果
   | 测试 | 结果 |
   |------|------|
   | 新增测试 | test_[module]_fix_[bug_shortname].py |
   | 是否通过 | PASS/FAIL |
   | 回归总数 | N |
   | 回归通过 | N |
   | 回归失败 | N |
   | blocking | true/false |
   ```
   **注意**：`bugs/{bug_id}/TEST_RESULT.md` 是整个 bug 的执行证据文档。与 `FIX_CLOSURE_LOG.ndjson` 的关系是：`ndjson` 存结构化数据，`TEST_RESULT.md` 存执行证据（日志输出、截图引用）。

### Phase 3 — 闭环归档（Closure）
1. **写入修复日志** `FIX_CLOSURE_LOG.ndjson`（原子追加，schema 见 § ndjson 规范）：
   ```json
   {"timestamp":"2026-06-28T21:30:00+08:00","bug_id":"algo-typ-2606282130-a3f6","module":"zero_cover_mode","bug_type":"config_error","root_cause":"硬编码路径无环境检测层","fix_type":"permanent","test_count":5,"regression_pass":5,"regression_fail":0,"blocking":false,"details":"添加 §0.5 项目环境检测，bug_id 自动生成，文件隔离","vcs_hash":"abc1234","test_skipped":false}
   ```

2. **更新修复事件**：
   - 首选：`events.ndjson.append()`（有 claw-guardian 时）
   - 降级：追加到 `events.ndjson`（标准日志路径）
   - 备用：仅追加 `FIX_CLOSURE_LOG.ndjson`（最小可行）

3. **更新 `.zero-cover-state.json`**：
   ```json
   {
     "total_fixes": 20,
     "bug_type_counter": {"config_error": 7, "logic_error": 6, ...},
     ...
   }
   ```

4. **注销 session**（§2.4）

5. **敏感数据过滤**（§ 安全边界）

### Phase 4 — 上线验证（可选，推荐）
修复上线后增加验证阶段：

1. **记录验证计划**：
   ```bash
   # 在 .zero-cover-state.json 中记录 24h/168h/720h 验证计划
   python skills/zero-cover-mode/lib/state_manager.py schedule-verify <bug_id> 24,168,720
   
   # 列出所有待验证的修复
   python skills/zero-cover-mode/lib/state_manager.py pending-verify
   
   # 验证通过后标记
   python skills/zero-cover-mode/lib/state_manager.py mark-verify <bug_id> 24 "pass"
   ```

2. **设置 cron 任务**（由 agent 执行）：
   ```bash
   python skills/zero-cover-mode/lib/state_manager.py cron-instructions <bug_id> "<TEST_CMD>"
   # 输出格式: cron action=add schedule.kind=every everyMs=<ms> ...
   ```

3. **复查条件**：
   - 24h 后：同根因的模式是否再次出现
   - 168h 后（7天）：同模块是否出现新 bug
   - 720h 后（30天）：所有检查完成 → 标记 `verified`

3. **复发处理**：
   - 如果复发 → 自动触发 Phase 1 重新分析
   - 同时检查是否落入 § 循环检测范围

---

## 四、5-Whys 层标准定义

**明确每一层的边界**，让执行者可以客观判断深度：

| 层级 | 名称 | 询问 | 产出示例 |
|------|------|------|---------|
| L1 | 现象层 | "用户/测试/日志显示什么具体错误？" | `ModuleNotFoundError: No module named 'gateway'` |
| L2 | 直接原因 | "执行了什么代码导致了 L1？覆盖了哪些路径？" | Phase 2 硬编码 `gateway.py dispatch()`，未做检测 |
| L3 | 深层原因 | "为什么 L2 的代码这么写？设计时遗漏了什么？" | 发布通用版前只在一个项目上测试 |
| L4 | 根本原因 | "团队/流程/架构中的哪个系统性问题？" | 技能设计缺少"环境检测层"的通用架构要求 |

**最低要求**：必须写到 L3，尽量写到 L4。如果只到 L2 → 标记为 `shallow_analysis: true`

---

## 五、修复闭环周报

### 触发
- 每周日 23:00 或用户主动 `/weekly-report`
- 周报数据**必须从 `FIX_CLOSURE_LOG.ndjson` 读取并聚合**，不是手写模板

### 聚合逻辑

使用 `lib/weekly_report.py` 从 ndjson 自动聚合：

```bash
# 列出可用周
python skills/zero-cover-mode/lib/weekly_report.py list-weeks FIX_CLOSURE_LOG.ndjson

# 生成周报
python skills/zero-cover-mode/lib/weekly_report.py generate FIX_CLOSURE_LOG.ndjson 2026-W26 reports/fix_closure_weekly_2026-W26.md
```

周报数据**必须从 `FIX_CLOSURE_LOG.ndjson` 读取并聚合**，不是手写模板。

### 内容格式
```
# 修复闭环周报 — 2026-W26 (06/22 - 06/28)

**生成时间**: YYYY-MM-DD HH:mm CST
**数据源**: FIX_CLOSURE_LOG.ndjson（{N} 条记录）

---

## 概览

| 指标 | 数值 |
|------|------|
| 本周修复 | 19 个 bug |
| 新增测试 | 15 个 |
| 回归通过率 | 67/67 (100%) |
| 阻塞修复 | 0 个 |
| 活跃重构警报 | 2 个 |

## 修复明细

| # | Bug ID | 模块 | bug_type | 根因摘要 | 修复类型 | 测试通过 | 日期 |
|---|--------|------|----------|---------|---------|---------|------|
| 1 | algo-typ-2606282100-a3f6 | algorithmic_novel_writer | type_mismatch | key 命名空间不统一 | permanent | 67/67 | 06-28 |

## ⚠️ 重构警报

| Bug 类型 | 出现次数 | 涉及模块 | 建议 |
|----------|---------|---------|------|
| config_error | 6 次 | one_novel_skill, claw-guardian | 建立统一配置层 |

## 趋势

> 本周修复数: 19(↑) | 回归通过率: 100%(→) | 阻塞数: 0(→)

---

*本报告由零稀泥模式从 FIX_CLOSURE_LOG.ndjson 自动聚合生成*
```

### 存储
- `reports/fix_closure_weekly_YYYY-Www.md`

---

## 六、重构警报规则

### 触发条件
同一 `bug_type`（基于根因摘要的语义分类）出现 **≥ 2 次** 时自动触发。
- 跨模块的同 bug_type 合并计数
- 通过 `.zero-cover-state.json` 的 `bug_type_counter` 读取
- 或者实时扫描 `FIX_CLOSURE_LOG.ndjson`

### 输出格式（统一模板）
每次追加到 `REFACTORING_ALERT.md` 必须使用以下模板：

```markdown
## {YYYY-MM-DD} {会话/修复标题}

- **{bug_type}**: {N} 次 — 涉及模块: {module_1}, {module_2}
  - Bug IDs: {id_1}, {id_2}
  - 根因摘要: {一句话}
  - 根源模式: {deliberate|unintentional|documentation|architecture}
  - 建议: {一句话}
```

**根源模式**说明：
- `deliberate`：故意设计如此（缺文档约束）
- `unintentional`：意外遗漏（代码审查未覆盖）
- `documentation`：文档与代码不一致
- `architecture`：架构层面需要调整

### 分类体系
标准类型（可直接使用，无需注册）：
`null_pointer`、`race_condition`、`edge_case`、`config_error`、`type_mismatch`、`resource_leak`、`timeout`、`permission`、`data_corruption`、`logic_error`、`syntax_error`、`performance`、`dead_code`

扩展新类型：
- 直接使用自然语言名称（如 `encoding_error`），不需要预先注册
- 如果新类型出现 ≥ 2 次 → 自动触发警报，同时在报告中标注 `new_type: yes`
- 建议在下一版本将高频新类型加入标准列表

---

## 七、安全边界与防御

### 7.1 假数据检测（增强版）

使用 `lib/fake_data_detector.py` 执行多层级检测：

```bash
# L1 静态扫描：检测 MagicMock/@patch/fake_data 等关键词 + 硬编码断言
python skills/zero-cover-mode/lib/fake_data_detector.py l1 <test_file>

# 全量检测（L1 + L2/L3 桩）
python skills/zero-cover-mode/lib/fake_data_detector.py full <test_file>
```

检测策略：

| 层级 | 方式 | blocking 条件 |
|------|------|--------------|
| L1 静态扫描 | 26 个关键词 + 硬编码断言模式 | 硬编码断言占 assert 总量 ≥ 80% |
| L2 活代码验证 | `--coverage` 覆盖率为 0%（桩） | 覆盖率为 0% → blocking |
| L3 启发式检查 | assert 全是字面量（桩） | 全部为字面量 → WARNING |

**L1 关键词列表**（Python，26 种模式）：
`MagicMock`, `mock.patch`, `@patch`, `AsyncMock`, `mock_open`, `create_autospec`, `PropertyMock`, `patch.object`, `patch.multiple`, `Faker()`, `FactoryBoy`, `sentinel`, `pytest.mocker`, `mocker.patch`, 等等。

**L1 关键词列表**（JS/TS 项目）：
`jest.fn()`, `jest.mock()`, `vi.fn()`, `vi.mock()`, `createMock`, `fakeData`, `MockClass`。

**硬编码断言检测**：`assert result == {literal_dict}` 或 `assert result == [literal_list]`。

**L2 覆盖率为 0% 的处理**：
```
WARNING: 测试覆盖率为 0% — 测试未实际调用任何被测代码
标记 FAKE_DATA_DETECTED = true
建议: 改为真实业务数据调用，或检查测试是否导入了正确模块
```

### 7.2 敏感数据过滤

在 Phase 3 写入前执行敏感数据过滤：

```bash
python skills/zero-cover-mode/lib/sensitive_filter.py check <file_path>   # 扫描
python skills/zero-cover-mode/lib/sensitive_filter.py filter <file_path>  # 过滤（原地替换）
```

`lib/sensitive_filter.py` 支持以下敏感模式：API key/token/password、Windows 用户路径、连接字符串、OpenAI key、JWT、GitHub PAT。

### 7.3 循环检测

在 Phase 3 归档时运行循环检测：

```bash
# 检查特定 bug 是否落入循环
python skills/zero-cover-mode/lib/loop_detector.py check FIX_CLOSURE_LOG.ndjson <bug_type> <root_cause>

# 扫描 ndjson 全量，输出所有循环模式
python skills/zero-cover-mode/lib/loop_detector.py scan FIX_CLOSURE_LOG.ndjson
```

检测触发（同类型 ≥3 次 + 根因相似度 ≥0.8）→ 写入 BUG_ROOT_CAUSE.md 的 WARNING 区，标记 blocking: true。

### 7.4 跳过 Phase 2 机制

允许显式跳过全量回归的场景：

| 场景 | 判定方式 | 操作 |
|------|---------|------|
| 文档修复 | fix_type = "documentation" | 跳过 Phase 2，标记 test_skipped: true |
| 配置 typo | fix_type = "config_typo" | 同上 |
| 纯注释/日志修改 | fix_type = "cosmetic" | 同上 |
| 空指针修复 | 不允许跳过 | 强制测试 |

FIX_CLOSURE_LOG.ndjson 对应字段：
```json
{"test_skipped": true, "skip_reason": "仅文档修复, 无代码逻辑变更"}
```

### 7.5 根因状态路由（合并 §7.5 vs §7.6 规则，按场景路由）

> **注意**: `bug_type="multiple"` 表示**批量提交**（一次修复多个 bug_type），
> 不属于单一 bug_type，不参与重构警报计数（同类型 ≥ 2 次触发），
> 但仍会被计入 `.zero-cover-state.json` 的 `bug_type_counter`。

**核心原则**: 分两种模式，通过 `fallback_mode` 标志路由：

#### 模式 A：严格模式（默认）— 对应旧 §7.6
- Phase 1 必须产出 `BUG_ROOT_CAUSE.md`，深度 ≥ L3
- 文件不存在 → blocking: true
- 文件存在但空内容 → blocking: true
- 文件深度 < L3 且 `fallback_mode=false` → blocking: true
- 此模式下不允许跳过 Phase 1

#### 模式 B：fallback 模式（显式启用）— 对应旧 §7.5
- 启用条件：Phase 1 尽力分析后无法定位根因
- 设置 `fallback_mode: true`，输出 `UNKNOWN_ROOT_CAUSE`
- **不拦截修复**，但标记 `fix_type: "workaround"`、`root_cause: "UNKNOWN"`
- 强制增加 Phase 3 后置任务：48h 内设置 cron 追踪，重新分析根因
- 对话末尾输出：`⚠️ 根因未知（fallback），此修复为 workaround，48h 内需重新分析`

#### 路由选择流程
```
Phase 1 开始
├─ BUG_ROOT_CAUSE.md 已存在吗？
│  ├─ 不存在 → blocking: true（严格模式）
│  └─ 存在 → 深度检查
│      ├─ ≥ L3 → 通过，进入 Phase 2
│      ├─ < L3 
│      │  ├─ fallback_mode=true → 模式 B，不拦截
│      │  └─ fallback_mode=false → blocking: true
└─ 尝试分析后仍然未知
   ├─ 设置 fallback_mode=true → 模式 B
   └─ 输出 UNKNOWN_ROOT_CAUSE
```

---

## 八、ndjson 规范与校验

### 8.1 强制 Schema

`FIX_CLOSURE_LOG.ndjson` 每行必须符合以下 schema：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| timestamp | string(ISO8601) | 是 | 精确到秒，不含微秒。含时区偏移 |
| bug_id | string | 是 | 按 §0.8 生成 |
| module | string | 是 | 模块名（snake_case） |
| bug_type | string | 是 | 单一值（见 §六 分类体系） |
| root_cause | string | 是 | 根因摘要，≤255 字 |
| fix_type | string | 是 | permanent | workaround | reverted |
| test_count | integer | 否（test_skipped=true 时跳过） | ≥ 0 |
| regression_pass | integer | 否 | ≥ 0 |
| regression_fail | integer | 否 | ≥ 0 |
| blocking | boolean | 是 | |
| details | string | 否 | 备注，≤500 字 |
| vcs_hash | string | 否 | git commit hash 或 "none" |
| test_skipped | boolean | 否 | 默认 false |

### 8.2 写入前校验 + 轮转

使用 `lib/ndjson_schema.py`：

```bash
# 追加（自动校验 + 自动轮转）
python skills/zero-cover-mode/lib/ndjson_schema.py append FIX_CLOSURE_LOG.ndjson '<json>'

# 全量验证
python skills/zero-cover-mode/lib/ndjson_schema.py validate FIX_CLOSURE_LOG.ndjson

# 手动轮转
python skills/zero-cover-mode/lib/ndjson_schema.py rotate FIX_CLOSURE_LOG.ndjson
```

轮转阈值：超过 1000 行时自动触发，旧文件命名为 `FIX_CLOSURE_LOG.W{W}.ndjson`。

### 8.3 数据迁移（v1→v2）

```bash
# 将旧格式 ndjson 迁移到 v2 schema
python skills/zero-cover-mode/lib/ndjson_migrate_v1_to_v2.py FIX_CLOSURE_LOG.ndjson --in-place
```

迁移内容：`bug_types`(数组)→`bug_type`(字符串)、缺失字段补充、微秒时间戳截断。

### 8.4 状态格式版本

`.zero-cover-state.json` 包含 `format_version` 字段标记 schema 版本。

---

## 九、持久化状态 (`.zero-cover-state.json`)

```json
{
  "version": "1.0.0",
  "total_fixes": 19,
  "active_session_ids": ["session_abc123"],
  "sessions": {
    "session_abc123": {
      "bug_id": "algo-typ-2606282130-a3f6",
      "started_at": "2026-06-28T21:28:00+08:00",
      "status": "in_progress"
    }
  },
  "bug_id_registry": ["algo-typ-2606282130-a3f6", "one-con-2606282100-b9e2"],
  "bug_type_counter": {
    "logic_error": 6,
    "config_error": 7,
    "type_mismatch": 4
  },
  "fix_history": [
    {"bug_id": "...", "bug_type": "...", "timestamp": "..."}
  ],
  "last_weekly_report": "2026-W26",
  "ndjson_line_count": 19,
  "ndjson_last_rotate": null,
  "project_env": {
    "project_type": "python",
    "test_cmd": "pytest tests/ -v --tb=short",
    "vcs": "git"
  },
  "updated_at": "2026-06-28T21:28:00+08:00"
}
```


  },
  "字段说明": {
    "version": "state schema 版本号",
    "total_fixes": "历史修复总数",
    "active_session_ids": "当前活跃 session 列表",
    "sessions": "session 详情映射",
    "bug_id_registry": "所有已注册 bug_id",
    "bug_type_counter": "bug_type 出现次数统计",
    "fix_history": "历史修复记录（按时间排序）",
    "verifications": "验证计划状态",
    "last_weekly_report": "最近周报",
    "ndjson_line_count": "ndjson 行数",
    "ndjson_last_rotate": "最近轮转时间",
    "project_env": "项目环境配置",
    "projects": "项目级统计",
    "_write_version": "写入版本号（已弃用）",
    "_pipeline_checkpoints": "Pipeline 阶段 checkpoint",
    "_orphan_sessions": "孤儿 session 记录",
    "_verify_needs_cron": "待创建 cron job"
  }
```

### 维护命令

**`compact()`**: 压缩 state 文件，清理过期 session 和已处理的 orphan 记录。
建议每 100 次修复后或每月手动运行一次：
```bash
python -m lib.state_manager compact
```

`compact()` 会:
1. 删除已完成且超过 SESSION_MAX_AGE_HOURS 的 session
2. 清理已处理的 orphan sessions 记录
3. 压缩 ndjson 轮转文件

---

## 十、回滚流程

### 触发条件
Phase 2 回归失败且无法在合理时间（≤15 分钟）内解决。

### 回滚步骤

```
1. 检测 VCS:
   if VCS == "git":
       git diff --stat
       git checkout -- <changed_files>
       记录 git HEAD hash
       echo "已回滚到 {hash}"
   elif VCS == "svn":
       svn revert -R .
   else:
       # 无 VCS：手动保存修改
       cp BUG_ROOT_CAUSE.md bugs/{bug_id}/BUG_ROOT_CAUSE.md     # 根因分析保留
       cp test_*.py bugs/{bug_id}/tests/                         # 测试文件保留
       手动撤销代码修改（需人工确认）
       echo "WARNING: 无 VCS，代码修改需手动撤销"

2. 标记回滚:
   FIX_CLOSURE_LOG.ndjson 追加:
   {"fix_type": "reverted", "reverted_at": "ISO8601", "revert_reason": "..."}

3. 创建 bugs/{bug_id}/REVERT_LOG.md:
   # 修复回滚记录
   - 原始修复: {bug_id}
   - 回滚时间: ISO8601
   - 回滚原因: {回归失败详情}
   - 原始文件: bugs/{bug_id}/
   - 重试计划: {后续计划}
```

---

## 附录A：各阶段产出物对照表

| 阶段 | 产出物 | 位置 | 写入方式 |
|------|--------|------|---------|
| Phase 0 | session 注册 | `.zero-cover-state.json` | 原子写 |
| Phase 1 | BUG_ROOT_CAUSE.md | `bugs/{bug_id}/` | 全量写 |
| Phase 2 | 测试文件 | `tests/regression/` + `bugs/{bug_id}/` | 全量写 |
| Phase 2 | TEST_RESULT.md | `bugs/{bug_id}/` | 全量写 |
| Phase 2 | regression_output.log | `bugs/{bug_id}/` | 追加 |
| Phase 3 | FIX_CLOSURE_LOG.ndjson | 根目录 | 原子追加 |
| Phase 3 | REFACTORING_ALERT.md | 根目录 | 原子追加 |
| Phase 3 | .zero-cover-state.json 更新 | 根目录 | 原子写 |
| Phase 3 | 敏感数据过滤 | 所有文件 | 写入前执行 |
| Phase 4 | 验证检查 | cron 任务 | 临时 |

## 附录B：各阶段快速参考

```
修 bug 前必做：
  1. read FIX_CLOSURE_LOG.ndjson
  2. read .zero-cover-state.json
  3. 检查 active_session_ids

修 bug 流程：
  Phase 0: 检测项目 → 生成 bug_id → 注册 session → 创建 bugs/{bug_id}/
  Phase 1: 写 BUG_ROOT_CAUSE.md（5-Whys ≥ L3）
  Phase 2: 写测试 → 跑回归 → 写 TEST_RESULT.md
  Phase 3: 过滤敏感数据 → 写入 ndjson → events.ndjson.append() → 更新 state
  Phase 4: 设置检查 → 标记 verified
```

---

## 附录C：执行路径指南

> **P1-N3/P1-N4 修复**：所有 `lib/` 脚本路径统一规范

### 路径约定

本技能的 Python 脚本在 `skills/zero-cover-mode/lib/` 目录下。
agent 默认 CWD 是 workspace 根目录（`C:\Users\Administrator\.openclaw\workspace`），
所以 `python lib/xxx.py` 不会找到脚本。

### 推荐用法

从 workspace 根执行时，使用完整相对路径：

```bash
# state_manager
python skills/zero-cover-mode/lib/state_manager.py read
python skills/zero-cover-mode/lib/state_manager.py register <session_id> <bug_id>
python skills/zero-cover-mode/lib/state_manager.py add-fix <bug_id> <bug_type> [project]

# ndjson_schema
python skills/zero-cover-mode/lib/ndjson_schema.py append FIX_CLOSURE_LOG.ndjson '<json>'
python skills/zero-cover-mode/lib/ndjson_schema.py validate FIX_CLOSURE_LOG.ndjson
python skills/zero-cover-mode/lib/ndjson_schema.py rotate FIX_CLOSURE_LOG.ndjson

# 其他 lib 模块同理
python skills/zero-cover-mode/lib/weekly_report.py generate FIX_CLOSURE_LOG.ndjson 2026-W26
python skills/zero-cover-mode/lib/root_cause_validator.py check bugs/{bug_id}/BUG_ROOT_CAUSE.md
python skills/zero-cover-mode/lib/sensitive_filter.py filter <file_path>
python skills/zero-cover-mode/lib/loop_detector.py scan FIX_CLOSURE_LOG.ndjson
python skills/zero-cover-mode/lib/refactoring_alert.py generate FIX_CLOSURE_LOG.ndjson
python skills/zero-cover-mode/lib/fake_data_detector.py l1 <file_path>
```

### 快捷写法

如果觉得路径太长，可以先 cd 到技能目录：

```bash
cd skills/zero-cover-mode
python lib/state_manager.py read
```

### path 参数 vs 文件位置

- `state_manager.py` 的 `locate()` 会自动从脚本路径向上探测 workspace 根，
  所以 `add-fix` 等操作会自动找到 workspace 根的 `.zero-cover-state.json`
- `ndjson_schema.py` 的 `FIX_CLOSURE_LOG.ndjson` 参数需要显式指定路径
- 如果使用 `STATE_PATH` 环境变量，所有 `state_manager.py` 的 `path` 参数都从环境变量读

---

## 附录D：编排器（orchestrator.py）— 推荐入口

> **v1.0.0**。消除对 LLM 手工执行四阶段的依赖，自动串联全部阶段。

### 架构总览

```
config.py  ─── 中央配置（版本/时区/常量）
    │
    ├─ state_manager.py        ─── 状态读写、session 管理
    ├─ ndjson_schema.py         ─── ndjson 校验/追加/轮转
    ├─ root_cause_validator.py  ─── 5-Whys 深度验证
    ├─ fake_data_detector.py    ─── 假数据检测（L1/L2/L3）
    ├─ sensitive_filter.py      ─── 敏感数据脱敏
    ├─ loop_detector.py         ─── 循环检测（Jaccard 相似度）
    ├─ weekly_report.py         ─── 周报聚合
    ├─ refactoring_alert.py     ─── 重构警报 upsert
    ├─ ndjson_migrate_v1_to_v2.py ─── 数据迁移
    └─ orchestrator.py  ⬅       ─── 编排层（推荐入口）
```

### 推荐用法：一键流水线

```bash
cd skills/zero-cover-mode

python -m lib.orchestrator run-pipeline \
    --bug-id "algo-typ-2606282130-a3f6" \
    --bug-type config_error \
    --module algorithmic_novel_writer \
    --fix-type permanent \
    --root-cause-file bugs/algo-typ-2606282130-a3f6/BUG_ROOT_CAUSE.md \
    --test-file tests/regression/test_algo_fix_*.py \
    --test-cmd "python -m pytest tests/ -v --tb=short" \
    --project-type python --vcs git
```

### Python API 调用

```python
from orchestrator import Pipeline, PipelineConfig

cfg = PipelineConfig(
    session_id="session_abc",
    bug_id="algo-typ-2606282130-a3f6",
    bug_type="config_error",
    module="algorithmic_novel_writer",
    test_cmd="pytest tests/ -v --tb=short",
    project_type="python",
    vcs="git",
)

pipe = Pipeline(cfg)
results = pipe.run_full_pipeline(
    root_cause_md=open("BUG_ROOT_CAUSE.md").read(),
    test_code=open("test_fix.py").read(),
    bug_type="config_error",
    fix_type="permanent",
    project_name="zero-cover-mode",
)
```

### Checkpoint 恢复

编排器在每个阶段完成后将 checkpoint 写入 `.zero-cover-state.json` 的 `_pipeline_checkpoints` 字段。
如果流水线中途中断，重新运行时会自动跳过已完成的阶段：

```bash
python -m lib.orchestrator status
# 输出示例:
#   algo-typ-2606282130-a3f6: phase0, phase1
```

### 各阶段产出物

| 阶段 | 方法 | 产出 | blocking 条件 |
|------|------|------|-------------|
| Phase 0 | `phase0_prepare()` | session 注册, bug 目录创建 | — |
| Phase 1 | `phase1_root_cause(md)` | BUG_ROOT_CAUSE.md | 5-Whys < L3 |
| Phase 2 | `phase2_test(code, cmd)` | 测试文件 + TEST_RESULT.md | 假数据检测/回归失败 |
| Phase 3 | `phase3_closure(...)` | ndjson 追加 + 敏感过滤 + 循环检测 | — |
| Phase 4 | `phase4_verify(cmd, hours)` | 验证计划 cron | — |

---

## 附录E：架构变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 初始版本 |
