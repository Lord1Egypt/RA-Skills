# skill-function-test 完整使用指南

> **场景测试（Scenario Testing）** — 不以函数为单位，以 **场景链路** 为单位。
> 备份 → 蓝皮书 → 配置确认 → S1-S3场景测试 → D1-D6功能测试 → S4执行忠实度 → 修复 → bump → 双格式报告 → 结论写入test-report.md。

## 核心原则

1. **场景驱动** — LLM 基于目标技能的 SKILL.md 和蓝皮书手工编写场景测试用例，每条用例代表一条真实用户场景
2. **测试用例自带 modules 字段** — LLM 写测试时直接指定涉及的 Python 模块名，引擎直接用蓝皮书映射，不再猜词
3. **无 CLI 入口的模块也测试** — 引擎用 `importlib.import_module()` 验证模块可加载，确保无语法/依赖问题
4. **功能测试做底座** — D1-D6 功能测试定位到具体断点行号，场景测试定位到链路断裂位置
5. **S4 全量范围扫描** — 从蓝皮书提取约束、引用链路、工作流程、文件清单作为测试范围，噪音下测铁律坚守率
6. **不允许修复导致功能失效** — 修复后必须回归确认，与备份前基线对比
7. **配置即铁律** — 配置一致性确认后生成执行清单，锁死配置，后续步骤严格按清单执行

**场景测试 vs 功能测试 vs S4：**

| | 场景测试 | 功能测试 | S4 执行忠实度 |
|--|---------|---------|----------|
| 输入 | 手工编写的场景测试用例 + modules 字段 | 蓝皮书的代码分析 | 技能的铁律/约束 |
| 输出 | "模块 runner 导入成功 / economic_analysis_engine --help rc=0" | "calc_cpm 语法正确" | "C-07 备份铁律在L4下坚守率100%" |
| 测试方式 | CLI 脚本 subprocess + 非 CLI 模块 importlib | AST 扫描 + 代码检查 | 噪音方案回放 |
| 覆盖 | 用户声称的业务场景 | 代码里的全部函数 | 技能定义的行为约束 |

---

## 完整工作流程（10 阶段）

### 阶段 1：备份

hooks 自动补齐，无需手动操作。

```bash
python scripts/hooks.py check /path/to/target-skill backup
```

### 阶段 2：蓝皮书扫描 + 约束提取

hooks 自动补齐（依赖备份已完成）。

```bash
python scripts/hooks.py check /path/to/target-skill blueprint
```

### 阶段 3：强制确认配置一致性

自动校验 `.test-config.json` 配置项（轮数、维度开关、修复模式、S4 权重），发现不一致自动修正。同时生成 `.execution-checklist.json` 执行清单。

```bash
python scripts/hooks.py check /path/to/target-skill config_check
```

> ⛔ 执行清单一旦生成，配置即被锁定。后续步骤禁止更新配置，即使更新也会被 config_hash 校验阻断。

### 阶段 4：S1-S3 场景测试

LLM 基于目标技能的 SKILL.md 和蓝皮书，手工编写 `.s_test_plan.json`。

hooks 阻断检查：文件存在且各维度（S1/S2/S3）均≥1 条才放行。

```bash
python scripts/hooks.py check /path/to/target-skill write_tests   # LLM 编写测试用例
python scripts/scenario_engine.py /path/to/target-skill            # 按配置轮次执行
```

对每条测试用例：
- 指定了有 CLI 入口的模块 → 执行 `python xxx.py --help` 验证返回值
- 指定了无 CLI 入口的模块 → `importlib.import_module()` 验证模块可加载

格式见 `references/s-test-plan-schema.md`。

### 阶段 5：D1-D6 功能测试

AST 级代码扫描，自动执行，无需 LLM 手工写用例。

```bash
python scripts/test_engine.py /path/to/target-skill
```

### 阶段 6：S4 执行忠实度（可选）

LLM 基于约束清单编写噪声方案 → validate 校验 → play 随机化回放。

```bash
# 全量范围扫描
python scripts/s4_engine.py /path/to/target-skill scope

# LLM 编写噪声方案（写入 .s4_noise_plan.json）→ 校验 → 回放
python scripts/s4_engine.py /path/to/target-skill validate /path/to/.s4_noise_plan.json
python scripts/s4_engine.py /path/to/target-skill play
```

S4 执行忠实度测试流程：
1. **阶段A：全量测试范围生成** — 从蓝皮书提取约束+引用链路+工作流程+文件清单
2. **阶段B：LLM推理层** — 读取全量范围 → 设计噪音方案 → schema 校验
3. **阶段C：噪音执行** — 逐条执行噪音方案 → 记录坚守/失守
4. **阶段D：复盘归因** — 归因分析 → 坚守率矩阵

### 阶段 7：修复（可选）

仅当 fix_mode 开启时执行。LLM 逐条判断问题为 FP（误报）或真问题，然后执行自动修复。

| 模式 | 行为 |
|------|------|
| **0 仅报告** | 输出完整报告，不执行任何修复 |
| **1 直接修复** | 对 F-0 BLOCK 和 F-1 WARN 级问题执行自动修复 |

修复后自动执行回归确认：
- 重新执行全量场景+功能测试
- 对比修复前的 BLOCK 数量
- F-0 未减少 → 回滚
- 出现新 F-0 → 标记回归损伤，回滚

### 阶段 8：版本号 bump

修复有更新时自动执行 PATCH bump，三端同步（SKILL.md / _meta.json / CHANGELOG.md）。

### 阶段 9：输出报告

```bash
python scripts/gen_report.py /path/to/target-skill   # HTML + Markdown
```

生成 HTML + Markdown 双格式报告 + S4 坚守率矩阵。gen_report 入口会先校验执行清单全部前置步骤是否通过，未通过则阻断并列出未完成的步骤。

### 阶段 10：结论写入 test-report.md

gen_report 自动执行，将完整测试结论追加到 `<skill>/references/test-report.md`（相同时间戳跳过）。

---

## 修复规则

| 问题类型 | 是否会修复 | 修复方法 |
|---------|-----------|---------|
| F-0 导入错误/语法错误 | ✅ 自动修复 | `fixer.safe_patch()` 修正错误行 |
| F-1 零除风险 | ✅ 自动修复 | `fixer.fix_add_none_guard()` |
| F-1 裸 print | ✅ 自动修复 | `fixer.fix_stdout_to_logging()` |
| F-1 硬编码路径 | ✅ 自动修复 | `fixer.fix_hardcoded_path()` |
| F-1 异常裸奔 | ✅ 自动修复 | `fixer.fix_exception_guard()` |
| F-1 引用断链 | ❌ 不修复 | 输出建议，由人决定 |
| F-2 缺少文档 | ❌ 不修复 | 仅记录 |
| 场景层面的设计缺失 | ❌ 不修复 | 仅报告（越界不修复） |

---

## 输出规范

每条测试结果必须：
1. **场景/维度标识**（S1-S3 / D1-D6）
2. **测试名称**（一句话描述）
3. **严重级别**（F-0 BLOCK / F-1 WARN / F-2 INFO）
4. **状态**（pass / fail / skip）
5. **问题描述**（精确到场景链路或文件行）
6. **精确位置**（文件:行号）
7. **场景级修复建议**（针对场景链路断裂，非泛泛而谈）

禁止产出模糊描述。场景链路报告必须说清：输入是什么、断在哪一步、预期是什么、实际是什么。
