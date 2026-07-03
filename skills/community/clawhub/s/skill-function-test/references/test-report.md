# 基于 skill-function-test 的测试报告

> 本文件由 skill-function-test 的 gen_report.py 自动生成和追加，记录每次测试的完整结论。

---

## 报告结构

| 段落 | 内容 |
|------|------|
| **元信息** | 目标技能名、版本、测试时间、配置快照 |
| **维度覆盖总览** | S1-S3 / D1-D6 / S4 各维度的 PASS/FAIL/BLOCK 聚合统计 |
| **S1-S3 场景测试详情** | 每条场景用例的触发条件、预期行为、实际结果、断裂位置 |
| **D1-D6 功能测试详情** | 每条功能检查项的扫描结果、文件行号、严重级别 |
| **S4 执行忠实度** | 噪声方案条目数、坚守/失守明细、坚守率矩阵、综合评分 |
| **回归对比** | 修复前 vs 修复后的 BLOCK/PASS 变化对比表 |
| **修复记录摘要** | 自动修复的条目列表（文件、类型、结果） |
| **计时统计** | 各阶段耗时、py_script 耗时、LLM 推理耗时 |

---

## 示例

```markdown
## 基于 skill-function-test 的测试报告

### 元信息
| 字段 | 值 |
|------|----|
| 目标技能 | activity-duration-estimation |
| 版本 | v2.3.0 |
| 测试时间 | 2026-06-18 12:45 |
| 测试轮次 | 3 |
| 修复模式 | 功能修复=1, 场景修复=0 |
| S4 | 开启 (2轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | 失败 | BLOCK | 通过率 |
|------|------|------|------|-------|--------|
| S1 场景触发 | 3 | 3 | 0 | 0 | 100% |
| S2 核心能力 | 4 | 3 | 1 | 0 | 75% |
| S3 工作流 | 2 | 2 | 0 | 0 | 100% |
| D1 基础功能 | 8 | 8 | 0 | 0 | 100% |
| D2 流程断点 | 6 | 5 | 1 | 0 | 83% |
| D3 数据污染 | 4 | 4 | 0 | 0 | 100% |
| D4 噪音检测 | 3 | 3 | 0 | 0 | 100% |
| D5 计算正确性 | 5 | 5 | 0 | 0 | 100% |
| D6 边界鲁棒性 | 4 | 4 | 0 | 0 | 100% |
| **S4 忠实度** | 12 | 11 | 1 | - | 92% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1-01 | BLOCK | 触发词识别 | PASS | 输入"帮我估算工期"→正确触发技能 |
| S2-01 | WARN | 三点估算精度 | FAIL | 输入参数表→结果偏差>5% |

### 修复记录摘要
| 文件 | 类型 | 结果 |
|------|------|------|
| scripts/engine.py:42 | 零除保护 | ✅ 已修复 |
| scripts/utils.py:88 | 裸print→logging | ✅ 已修复 |

### 回归对比
| 指标 | 修复前 | 修复后 | 变化 |
|------|--------|--------|------|
| 场景 BLOCK | 1 | 0 | -1 ✅ |
| 功能通过 | 32 | 34 | +2 ✅ |

### 计时统计
| 阶段 | py_script | LLM | 合计 |
|------|-----------|-----|------|
| 备份 | 0.2s | 0s | 0.2s |
| 蓝皮书 | 0.8s | 0s | 0.8s |
| 场景测试 | 1.2s | 45s | 46.2s |
| 功能测试 | 3.5s | 0s | 3.5s |
| S4 | 0.5s | 60s | 60.5s |
| 报告 | 0.3s | 0s | 0.3s |
| **总计** | **6.5s** | **105s** | **111.5s** |
```

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:15 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:21 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 267 | 158 | 0 | 59% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 57 chars |
| D1 | WARN | 运行时异常: scripts\bump_version.py | FAIL | scripts\bump_version.py:0 | object of type 'NoneType' has no len() |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 328 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 58 chars |
| D1 | WARN | 运行时异常: scripts\inspector.py | FAIL | scripts\inspector.py:0 | object of type 'NoneType' has no len() |
| D1 | WARN | 运行时异常: scripts\runner.py | FAIL | scripts\runner.py:0 | 'NoneType' object has no attribute 'strip' |
| D1 | WARN | 运行时异常: scripts\s4_engine.py | FAIL | scripts\s4_engine.py:0 | object of type 'NoneType' has no len() |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | WARN | 运行时异常: scripts\test_config.py | FAIL | scripts\test_config.py:0 | object of type 'NoneType' has no len() |
| D1 | WARN | 运行时异常: scripts\test_engine.py | FAIL | scripts\test_engine.py:0 | object of type 'NoneType' has no len() |
| D1 | WARN | 运行时异常: scripts\timeline.py | FAIL | scripts\timeline.py:0 | object of type 'NoneType' has no len() |
| D2 | WARN | 引用文件不存在 | FAIL | changelog.md:0 | changelog.md → scripts/permission_checker.py |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config._fix_mode_text_sce |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config._fix_mode_text_fun |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\runner.py → glob |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.list_backups |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_engine | PASS | :0 | scripts\runner.py → test_engine.run_full_test |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\runner.py → fixer |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 6 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:293 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:666 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:667 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:668 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:669 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:670 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:745 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:309 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:320 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:419 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:438 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:449 | print("请指定步骤: init | backup | blueprint | scenario |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:119 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:131 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:139 | print("\n  [S4 阶段A] 生成全量测试范围（蓝皮书+约束+工作流+引用链路）...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:148 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:192 | print(""" |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:261 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:267 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:268 | print(s_text if test_rounds == 1 else f"  场景测试 {te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:316 | print("  [SKIP] 功能测试维度未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:336 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:386 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:397 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:409 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:410 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:411 | print("  ║                                     ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:412 | print("  ║  1. 按以上工作流步骤顺序执行一次     ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:413 | print("  ║  2. 每步完成后记录到                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:414 | print("  ║     .s4_positive.json               ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:415 | print('  ║     格式: [{"step":1,"title":"备份",  ║') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:416 | print('  ║            "completed":true}]        ║' |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:417 | print("  ║                                     ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:418 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:432 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:433 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:507 | print("  无待判断问题，无需过滤") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:545 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:548 | print("  直接修复模式，LLM 执行自动修复...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:565 | print("  询问模式，LLM 逐条展示给用户确认...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:585 | print("  仅报告/询问模式，跳过自动 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:593 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:694 | print(state.regression_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:762 | print("  无待判断问题") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:873 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:937 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:1000 | print("用法: python runner.py <skill-dir> [full|test |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:1001 | print("  fix_mode: 0=仅报告  1=直接修复  2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:791 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:803 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:808 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:812 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:837 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:841 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:845 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:853 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:870 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:874 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:452 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:470 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:245 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:255 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:259 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:267 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:273 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:280 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:290 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:296 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:300 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:345 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:349 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:354 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:777 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:803 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:812 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:813 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:814 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:815 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:816 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:817 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:833 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:853 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:623 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:692 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:708 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 16 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 4 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:299 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:41 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:48 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:63 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:308 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:33 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:40 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:46 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:85 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:88 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:92 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:95 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:98 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:101 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:114 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:119 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:129 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:145 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:190 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:218 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:252 | hook_pre_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:306 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:317 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:328 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:333 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:352 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:369 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:392 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:393 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:394 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:401 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:953 | run_pipeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:238 | _has_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:153 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:161 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:171 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:179 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:215 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:680 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:558 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:106 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:146 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:390 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:226 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:240 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:92 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:109 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:123 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:129 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:748 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:94 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:718 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:616 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:121 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:197 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 1 个 except / 775 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:38 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 294 | 195 | 0 | 66% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 56 chars |
| D1 | INFO | 运行时: scripts\bump_version.py - | PASS | :0 | exit code 0, stdout 22 chars |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 327 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 205 chars |
| D1 | INFO | 运行时: scripts\inspector.py --he | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | WARN | 启动失败: scripts\runner.py | FAIL | scripts\runner.py:0 | exit code 1: n-test\scripts\runner.py", line 92, i |
| D1 | INFO | 运行时: scripts\s4_engine.py --he | PASS | :0 | exit code 0, stdout 594 chars |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\test_config.py -- | PASS | :0 | exit code 0, stdout 475 chars |
| D1 | INFO | 运行时: scripts\test_engine.py -- | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | INFO | 运行时: scripts\timeline.py --hel | PASS | :0 | exit code 0, stdout 396 chars |
| D2 | WARN | 引用文件不存在 | FAIL | changelog.md:0 | changelog.md → scripts/permission_checker.py |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\gen_report.py → fixer.safe_write |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\gen_report.py → hooks._clean_old_test_repo |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\hooks.py → fixer.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_markdown |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_html |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report._write_conclusion |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\runner.py → hooks._generate_execution_chec |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\scenario_engine.py → importlib |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\test_config.py → scripts.test_config.rende |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 5 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:300 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:666 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:667 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:668 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:669 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:670 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:934 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:380 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:586 | print("  [CHKLIST] 配置文件不存在，跳过生成清单") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1200 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1219 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1220 | print("  step: init | backup | blueprint | config_ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1221 | print("        function_test | s4 | fix | bump | g |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1232 | print("请指定步骤: init | backup | blueprint | write_te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:107 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:116 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:124 | print("\n  [S4 阶段A] 生成全量测试范围...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:130 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:163 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:166 | print("=== 当前配置（来自 .test-config.json）===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:170 | print("\n── 配置自检 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:239 | print("\n  ✅ 配置一致性校验通过，所有项自洽") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:289 | print("  [SKIP] 场景维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:301 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:335 | print("  [SKIP] 功能维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:383 | print("  [SKIP] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:402 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:449 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:457 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:468 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:469 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:470 | print("  ║  按工作流步骤顺序执行并记录到       ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:471 | print("  ║  .s4_positive.json                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:472 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:482 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:483 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:512 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:553 | print("  无待判断问题，跳过修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:584 | print("  未开启修复模式，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:589 | print("  无修复记录，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:597 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:676 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:733 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:753 | print("用法: python runner.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:848 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:860 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:865 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:869 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:894 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:898 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:902 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:910 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:936 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:940 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:637 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:655 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:269 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:279 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:283 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:291 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:297 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:304 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:314 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:320 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:324 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:369 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:373 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:378 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:799 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:825 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:834 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:835 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:836 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:837 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:838 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:839 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:855 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:875 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:630 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:699 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:715 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 36 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 7 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:299 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:42 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:49 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:65 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:322 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:757 | _write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:71 | _find_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:34 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:41 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:47 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:86 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:89 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:93 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:96 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:99 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:102 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:115 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:120 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:130 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:146 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:174 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:205 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:274 | hook_post_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:279 | hook_pre_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:292 | hook_pre_final_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:388 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:409 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:419 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:428 | hook_pre_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:441 | hook_post_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:447 | hook_pre_config_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:485 | hook_post_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:490 | hook_pre_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:538 | hook_post_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:562 | _checklist_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:566 | _config_checksum() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:578 | _generate_execution_checklist() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:739 | _validate_checklist_step() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:801 | _chk_count_plan_cases() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:829 | _chk_check_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:875 | _chk_count_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:922 | _chk_check_fix_records() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:934 | _chk_check_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:941 | _chk_check_all_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:960 | _chk_check_conclusion_written() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:971 | _save_checklist_item() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:988 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1005 | _clean_old_test_report_from_permissions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1055 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1062 | _is_step_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1076 | _check_scenario_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1105 | _check_s4_state() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1133 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1149 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1150 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1151 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1158 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:279 | _has_s_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:325 | _has_d_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:157 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:165 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:180 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:188 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:224 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:737 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:498 | generate_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:566 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:118 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:158 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:575 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:238 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:372 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:116 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:133 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:147 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:153 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:767 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:118 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:737 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:623 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:128 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:204 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 2 个 except / 968 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:43 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 294 | 195 | 0 | 66% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 56 chars |
| D1 | INFO | 运行时: scripts\bump_version.py - | PASS | :0 | exit code 0, stdout 22 chars |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 327 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 205 chars |
| D1 | INFO | 运行时: scripts\inspector.py --he | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | WARN | 启动失败: scripts\runner.py | FAIL | scripts\runner.py:0 | exit code 1: n-test\scripts\runner.py", line 92, i |
| D1 | INFO | 运行时: scripts\s4_engine.py --he | PASS | :0 | exit code 0, stdout 594 chars |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\test_config.py -- | PASS | :0 | exit code 0, stdout 475 chars |
| D1 | INFO | 运行时: scripts\test_engine.py -- | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | INFO | 运行时: scripts\timeline.py --hel | PASS | :0 | exit code 0, stdout 396 chars |
| D2 | WARN | 引用文件不存在 | FAIL | changelog.md:0 | changelog.md → scripts/permission_checker.py |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\gen_report.py → fixer.safe_write |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\gen_report.py → hooks._clean_old_test_repo |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\hooks.py → fixer.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_markdown |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_html |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report._write_conclusion |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\runner.py → hooks._generate_execution_chec |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\scenario_engine.py → importlib |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\test_config.py → scripts.test_config.rende |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 5 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:300 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:666 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:667 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:668 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:669 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:670 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:934 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:380 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:586 | print("  [CHKLIST] 配置文件不存在，跳过生成清单") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1200 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1219 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1220 | print("  step: init | backup | blueprint | config_ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1221 | print("        function_test | s4 | fix | bump | g |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1232 | print("请指定步骤: init | backup | blueprint | write_te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:107 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:116 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:124 | print("\n  [S4 阶段A] 生成全量测试范围...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:130 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:163 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:166 | print("=== 当前配置（来自 .test-config.json）===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:170 | print("\n── 配置自检 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:239 | print("\n  ✅ 配置一致性校验通过，所有项自洽") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:289 | print("  [SKIP] 场景维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:301 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:335 | print("  [SKIP] 功能维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:383 | print("  [SKIP] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:402 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:449 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:457 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:468 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:469 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:470 | print("  ║  按工作流步骤顺序执行并记录到       ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:471 | print("  ║  .s4_positive.json                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:472 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:482 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:483 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:512 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:553 | print("  无待判断问题，跳过修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:584 | print("  未开启修复模式，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:589 | print("  无修复记录，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:597 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:676 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:733 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:753 | print("用法: python runner.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:848 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:860 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:865 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:869 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:894 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:898 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:902 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:910 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:936 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:940 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:637 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:655 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:269 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:279 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:283 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:291 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:297 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:304 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:314 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:320 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:324 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:369 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:373 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:378 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:799 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:825 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:834 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:835 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:836 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:837 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:838 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:839 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:855 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:875 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:630 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:699 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:715 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 36 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 7 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:299 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:42 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:49 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:65 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:322 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:757 | _write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:71 | _find_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:34 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:41 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:47 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:86 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:89 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:93 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:96 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:99 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:102 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:115 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:120 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:130 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:146 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:174 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:205 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:274 | hook_post_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:279 | hook_pre_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:292 | hook_pre_final_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:388 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:409 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:419 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:428 | hook_pre_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:441 | hook_post_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:447 | hook_pre_config_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:485 | hook_post_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:490 | hook_pre_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:538 | hook_post_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:562 | _checklist_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:566 | _config_checksum() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:578 | _generate_execution_checklist() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:739 | _validate_checklist_step() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:801 | _chk_count_plan_cases() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:829 | _chk_check_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:875 | _chk_count_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:922 | _chk_check_fix_records() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:934 | _chk_check_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:941 | _chk_check_all_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:960 | _chk_check_conclusion_written() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:971 | _save_checklist_item() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:988 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1005 | _clean_old_test_report_from_permissions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1055 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1062 | _is_step_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1076 | _check_scenario_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1105 | _check_s4_state() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1133 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1149 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1150 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1151 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1158 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:279 | _has_s_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:325 | _has_d_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:157 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:165 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:180 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:188 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:224 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:737 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:498 | generate_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:566 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:118 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:158 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:575 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:238 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:372 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:116 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:133 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:147 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:153 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:767 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:118 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:737 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:623 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:128 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:204 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 2 个 except / 968 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:44 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 294 | 195 | 0 | 66% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 56 chars |
| D1 | INFO | 运行时: scripts\bump_version.py - | PASS | :0 | exit code 0, stdout 22 chars |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 327 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 205 chars |
| D1 | INFO | 运行时: scripts\inspector.py --he | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | WARN | 启动失败: scripts\runner.py | FAIL | scripts\runner.py:0 | exit code 1: n-test\scripts\runner.py", line 92, i |
| D1 | INFO | 运行时: scripts\s4_engine.py --he | PASS | :0 | exit code 0, stdout 594 chars |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\test_config.py -- | PASS | :0 | exit code 0, stdout 475 chars |
| D1 | INFO | 运行时: scripts\test_engine.py -- | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | INFO | 运行时: scripts\timeline.py --hel | PASS | :0 | exit code 0, stdout 396 chars |
| D2 | WARN | 引用文件不存在 | FAIL | changelog.md:0 | changelog.md → scripts/permission_checker.py |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\gen_report.py → fixer.safe_write |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\gen_report.py → hooks._clean_old_test_repo |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\hooks.py → fixer.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_markdown |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_html |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report._write_conclusion |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\runner.py → hooks._generate_execution_chec |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\scenario_engine.py → importlib |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\test_config.py → scripts.test_config.rende |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 5 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:300 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:666 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:667 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:668 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:669 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:670 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:934 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:380 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:586 | print("  [CHKLIST] 配置文件不存在，跳过生成清单") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1200 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1219 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1220 | print("  step: init | backup | blueprint | config_ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1221 | print("        function_test | s4 | fix | bump | g |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1232 | print("请指定步骤: init | backup | blueprint | write_te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:107 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:116 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:124 | print("\n  [S4 阶段A] 生成全量测试范围...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:130 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:163 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:166 | print("=== 当前配置（来自 .test-config.json）===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:170 | print("\n── 配置自检 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:239 | print("\n  ✅ 配置一致性校验通过，所有项自洽") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:289 | print("  [SKIP] 场景维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:301 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:335 | print("  [SKIP] 功能维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:383 | print("  [SKIP] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:402 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:449 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:457 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:468 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:469 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:470 | print("  ║  按工作流步骤顺序执行并记录到       ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:471 | print("  ║  .s4_positive.json                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:472 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:482 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:483 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:512 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:553 | print("  无待判断问题，跳过修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:584 | print("  未开启修复模式，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:589 | print("  无修复记录，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:597 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:676 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:733 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:753 | print("用法: python runner.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:848 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:860 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:865 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:869 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:894 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:898 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:902 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:910 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:936 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:940 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:637 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:655 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:269 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:279 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:283 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:291 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:297 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:304 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:314 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:320 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:324 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:369 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:373 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:378 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:799 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:825 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:834 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:835 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:836 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:837 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:838 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:839 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:855 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:875 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:630 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:699 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:715 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 36 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 7 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:299 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:42 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:49 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:65 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:322 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:757 | _write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:71 | _find_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:34 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:41 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:47 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:86 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:89 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:93 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:96 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:99 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:102 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:115 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:120 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:130 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:146 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:174 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:205 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:274 | hook_post_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:279 | hook_pre_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:292 | hook_pre_final_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:388 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:409 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:419 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:428 | hook_pre_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:441 | hook_post_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:447 | hook_pre_config_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:485 | hook_post_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:490 | hook_pre_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:538 | hook_post_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:562 | _checklist_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:566 | _config_checksum() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:578 | _generate_execution_checklist() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:739 | _validate_checklist_step() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:801 | _chk_count_plan_cases() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:829 | _chk_check_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:875 | _chk_count_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:922 | _chk_check_fix_records() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:934 | _chk_check_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:941 | _chk_check_all_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:960 | _chk_check_conclusion_written() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:971 | _save_checklist_item() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:988 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1005 | _clean_old_test_report_from_permissions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1055 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1062 | _is_step_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1076 | _check_scenario_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1105 | _check_s4_state() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1133 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1149 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1150 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1151 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1158 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:279 | _has_s_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:325 | _has_d_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:157 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:165 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:180 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:188 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:224 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:737 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:498 | generate_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:566 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:118 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:158 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:575 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:238 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:372 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:116 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:133 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:147 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:153 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:767 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:118 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:737 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:623 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:128 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:204 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 2 个 except / 968 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:53 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 294 | 195 | 0 | 66% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 56 chars |
| D1 | INFO | 运行时: scripts\bump_version.py - | PASS | :0 | exit code 0, stdout 22 chars |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 327 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 205 chars |
| D1 | INFO | 运行时: scripts\inspector.py --he | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | WARN | 启动失败: scripts\runner.py | FAIL | scripts\runner.py:0 | exit code 1: n-test\scripts\runner.py", line 92, i |
| D1 | INFO | 运行时: scripts\s4_engine.py --he | PASS | :0 | exit code 0, stdout 594 chars |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\test_config.py -- | PASS | :0 | exit code 0, stdout 475 chars |
| D1 | INFO | 运行时: scripts\test_engine.py -- | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | INFO | 运行时: scripts\timeline.py --hel | PASS | :0 | exit code 0, stdout 396 chars |
| D2 | WARN | 引用文件不存在 | FAIL | changelog.md:0 | changelog.md → scripts/permission_checker.py |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\gen_report.py → fixer.safe_write |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\gen_report.py → hooks._clean_old_test_repo |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\hooks.py → fixer.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_markdown |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_html |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report._write_conclusion |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\runner.py → hooks._generate_execution_chec |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\scenario_engine.py → importlib |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\test_config.py → scripts.test_config.rende |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 5 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:300 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:666 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:667 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:668 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:669 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:670 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:934 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:380 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:586 | print("  [CHKLIST] 配置文件不存在，跳过生成清单") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1200 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1219 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1220 | print("  step: init | backup | blueprint | config_ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1221 | print("        function_test | s4 | fix | bump | g |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1232 | print("请指定步骤: init | backup | blueprint | write_te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:107 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:116 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:124 | print("\n  [S4 阶段A] 生成全量测试范围...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:130 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:163 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:166 | print("=== 当前配置（来自 .test-config.json）===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:170 | print("\n── 配置自检 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:239 | print("\n  ✅ 配置一致性校验通过，所有项自洽") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:289 | print("  [SKIP] 场景维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:301 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:335 | print("  [SKIP] 功能维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:383 | print("  [SKIP] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:402 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:449 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:457 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:468 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:469 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:470 | print("  ║  按工作流步骤顺序执行并记录到       ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:471 | print("  ║  .s4_positive.json                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:472 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:482 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:483 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:512 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:553 | print("  无待判断问题，跳过修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:584 | print("  未开启修复模式，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:589 | print("  无修复记录，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:597 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:676 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:733 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:753 | print("用法: python runner.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:848 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:860 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:865 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:869 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:894 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:898 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:902 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:910 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:936 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:940 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:637 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:655 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:269 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:279 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:283 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:291 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:297 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:304 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:314 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:320 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:324 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:369 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:373 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:378 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:799 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:825 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:834 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:835 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:836 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:837 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:838 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:839 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:855 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:875 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:630 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:699 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:715 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 36 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 7 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:299 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:42 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:49 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:65 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:322 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:757 | _write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:71 | _find_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:34 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:41 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:47 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:86 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:89 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:93 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:96 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:99 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:102 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:115 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:120 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:130 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:146 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:174 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:205 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:274 | hook_post_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:279 | hook_pre_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:292 | hook_pre_final_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:388 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:409 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:419 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:428 | hook_pre_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:441 | hook_post_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:447 | hook_pre_config_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:485 | hook_post_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:490 | hook_pre_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:538 | hook_post_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:562 | _checklist_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:566 | _config_checksum() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:578 | _generate_execution_checklist() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:739 | _validate_checklist_step() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:801 | _chk_count_plan_cases() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:829 | _chk_check_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:875 | _chk_count_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:922 | _chk_check_fix_records() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:934 | _chk_check_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:941 | _chk_check_all_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:960 | _chk_check_conclusion_written() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:971 | _save_checklist_item() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:988 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1005 | _clean_old_test_report_from_permissions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1055 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1062 | _is_step_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1076 | _check_scenario_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1105 | _check_s4_state() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1133 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1149 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1150 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1151 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1158 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:279 | _has_s_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:325 | _has_d_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:157 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:165 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:180 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:188 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:224 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:737 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:498 | generate_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:566 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:118 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:158 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:575 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:238 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:372 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:116 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:133 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:147 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:153 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:767 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:118 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:737 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:623 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:128 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:204 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 2 个 except / 968 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 13:54 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 294 | 195 | 0 | 66% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 56 chars |
| D1 | INFO | 运行时: scripts\bump_version.py - | PASS | :0 | exit code 0, stdout 22 chars |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 327 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 205 chars |
| D1 | INFO | 运行时: scripts\inspector.py --he | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | WARN | 启动失败: scripts\runner.py | FAIL | scripts\runner.py:0 | exit code 1: n-test\scripts\runner.py", line 92, i |
| D1 | INFO | 运行时: scripts\s4_engine.py --he | PASS | :0 | exit code 0, stdout 594 chars |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\test_config.py -- | PASS | :0 | exit code 0, stdout 475 chars |
| D1 | INFO | 运行时: scripts\test_engine.py -- | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | INFO | 运行时: scripts\timeline.py --hel | PASS | :0 | exit code 0, stdout 396 chars |
| D2 | WARN | 引用文件不存在 | FAIL | changelog.md:0 | changelog.md → scripts/permission_checker.py |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\gen_report.py → fixer.safe_write |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\gen_report.py → hooks._clean_old_test_repo |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\hooks.py → fixer.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_markdown |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_html |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report._write_conclusion |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\runner.py → hooks._generate_execution_chec |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\scenario_engine.py → importlib |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\test_config.py → scripts.test_config.rende |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 5 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:300 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:666 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:667 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:668 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:669 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:670 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:934 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:380 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:586 | print("  [CHKLIST] 配置文件不存在，跳过生成清单") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1200 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1219 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1220 | print("  step: init | backup | blueprint | config_ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1221 | print("        function_test | s4 | fix | bump | g |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1232 | print("请指定步骤: init | backup | blueprint | write_te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:107 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:116 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:124 | print("\n  [S4 阶段A] 生成全量测试范围...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:130 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:163 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:166 | print("=== 当前配置（来自 .test-config.json）===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:170 | print("\n── 配置自检 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:239 | print("\n  ✅ 配置一致性校验通过，所有项自洽") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:289 | print("  [SKIP] 场景维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:301 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:335 | print("  [SKIP] 功能维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:383 | print("  [SKIP] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:402 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:449 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:457 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:468 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:469 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:470 | print("  ║  按工作流步骤顺序执行并记录到       ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:471 | print("  ║  .s4_positive.json                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:472 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:482 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:483 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:512 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:553 | print("  无待判断问题，跳过修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:584 | print("  未开启修复模式，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:589 | print("  无修复记录，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:597 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:676 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:733 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:753 | print("用法: python runner.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:848 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:860 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:865 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:869 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:894 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:898 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:902 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:910 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:936 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:940 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:637 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:655 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:269 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:279 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:283 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:291 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:297 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:304 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:314 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:320 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:324 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:369 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:373 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:378 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:799 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:825 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:834 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:835 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:836 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:837 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:838 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:839 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:855 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:875 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:630 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:699 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:715 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 36 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 7 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:299 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:42 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:49 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:65 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:322 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:757 | _write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:71 | _find_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:34 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:41 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:47 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:86 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:89 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:93 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:96 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:99 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:102 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:115 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:120 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:130 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:146 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:174 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:205 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:274 | hook_post_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:279 | hook_pre_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:292 | hook_pre_final_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:388 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:409 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:419 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:428 | hook_pre_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:441 | hook_post_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:447 | hook_pre_config_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:485 | hook_post_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:490 | hook_pre_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:538 | hook_post_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:562 | _checklist_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:566 | _config_checksum() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:578 | _generate_execution_checklist() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:739 | _validate_checklist_step() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:801 | _chk_count_plan_cases() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:829 | _chk_check_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:875 | _chk_count_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:922 | _chk_check_fix_records() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:934 | _chk_check_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:941 | _chk_check_all_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:960 | _chk_check_conclusion_written() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:971 | _save_checklist_item() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:988 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1005 | _clean_old_test_report_from_permissions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1055 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1062 | _is_step_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1076 | _check_scenario_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1105 | _check_s4_state() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1133 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1149 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1150 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1151 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1158 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:279 | _has_s_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:325 | _has_d_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:157 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:165 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:180 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:188 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:224 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:737 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:498 | generate_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:566 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:118 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:158 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:575 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:238 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:372 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:116 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:133 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:147 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:153 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:767 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:118 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:737 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:623 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:128 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:204 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 2 个 except / 968 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-function-test |
| 测试时间 | 2026-06-18 17:42 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 3 | 3 | 0 | 100% |
| D1-D6 功能测试 | 293 | 195 | 0 | 66% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景执行汇总 | PASS | 执行了 3 个 CLI 命令 |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 6 个 CLI 命令 |
| S3 | INFO | 工作流链路 | PASS | 验证了 6 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\backup.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\bump_version.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\fixer.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\gen_report.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\inspector.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\runner.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\s4_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\scenario_engine. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_config.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_engine.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\timeline.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\backup.py --help | PASS | :0 | exit code 0, stdout 56 chars |
| D1 | INFO | 运行时: scripts\bump_version.py - | PASS | :0 | exit code 0, stdout 22 chars |
| D1 | INFO | 运行时: scripts\fixer.py --help | PASS | :0 | exit code 0, stdout 327 chars |
| D1 | WARN | 启动失败: scripts\gen_report.py | FAIL | scripts\gen_report.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\hooks.py --help | PASS | :0 | exit code 0, stdout 205 chars |
| D1 | INFO | 运行时: scripts\inspector.py --he | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | WARN | 启动失败: scripts\runner.py | FAIL | scripts\runner.py:0 | exit code 1: n-test\scripts\runner.py", line 92, i |
| D1 | INFO | 运行时: scripts\s4_engine.py --he | PASS | :0 | exit code 0, stdout 594 chars |
| D1 | WARN | 启动失败: scripts\scenario_engine. | FAIL | scripts\scenario_engine.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\test_config.py -- | PASS | :0 | exit code 0, stdout 475 chars |
| D1 | INFO | 运行时: scripts\test_engine.py -- | PASS | :0 | exit code 0, stdout 17 chars |
| D1 | INFO | 运行时: scripts\timeline.py --hel | PASS | :0 | exit code 0, stdout 396 chars |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\backup.py → io |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\backup.py → zipfile |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\gen_report.py → glob |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\gen_report.py → fixer.safe_write |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\gen_report.py → test_config.load_config |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\gen_report.py → hooks._clean_old_test_repo |
| D2 | INFO | 外部依赖: fixer | PASS | :0 | scripts\hooks.py → fixer.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\inspector.py → ast |
| D2 | INFO | 外部依赖: backup | PASS | :0 | scripts\runner.py → backup.backup_skill |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.scan |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.print_bluebook |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\runner.py → inspector.extract_constraints |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.save_test_scope |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.format_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_s4_rounds |
| D2 | INFO | 外部依赖: scenario_engine | PASS | :0 | scripts\runner.py → scenario_engine.run_scenario_t |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_ma |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_matri |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.extract_workflow_ste |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_workflow_steps |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.generate_fidelity_sc |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_markdown |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report.gen_html |
| D2 | INFO | 外部依赖: gen_report | PASS | :0 | scripts\runner.py → gen_report._write_conclusion |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.load_config |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\runner.py → test_config.get_active_tests |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_constraint_sum |
| D2 | INFO | 外部依赖: hooks | PASS | :0 | scripts\runner.py → hooks._generate_execution_chec |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.NoisePlayer |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.auto_bump |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.get_current_versi |
| D2 | INFO | 外部依赖: bump_version | PASS | :0 | scripts\runner.py → bump_version.detect_bump_type |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.print_fidelity_score |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.s4_scope_repair |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_test_scope |
| D2 | INFO | 外部依赖: s4_engine | PASS | :0 | scripts\runner.py → s4_engine.load_trace |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\scenario_engine.py → ast |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\scenario_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\scenario_engine.py → importlib |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\scenario_engine.py → test_config.load_conf |
| D2 | INFO | 外部依赖: http | PASS | :0 | scripts\test_config.py → http.server |
| D2 | INFO | 外部依赖: threading | PASS | :0 | scripts\test_config.py → threading |
| D2 | INFO | 外部依赖: webbrowser | PASS | :0 | scripts\test_config.py → webbrowser |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_config.py → test_config.render_html |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\test_config.py → scripts.test_config.rende |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\test_engine.py → ast |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\test_engine.py → importlib.util |
| D2 | INFO | 外部依赖: inspect | PASS | :0 | scripts\test_engine.py → inspect |
| D2 | INFO | 外部依赖: inspector | PASS | :0 | scripts\test_engine.py → inspector.scan |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.config_path |
| D2 | INFO | 外部依赖: test_config | PASS | :0 | scripts\test_engine.py → test_config.load_config |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\timeline.py → time |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\backup.py:153 | 5 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\test_engine.py:300 | if ".db" in line and ("sqlite" in line.lower() or  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\backup.py:187 | print("用法: python backup.py backup|list|restore <p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\bump_version.py:201 | print("用法: python bump_version.py <skill-dir> [pat |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:682 | print("用法: python fixer.py <filepath> <fix-type> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:683 | print("  fix-type: add_none_guard | stdout_to_logg |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:684 | print("            exception_guard | shell_cd_guar |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:685 | print("            js_null_guard | js_try_catch |  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\fixer.py:686 | print("            powershell_error_guard | safe_p |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\gen_report.py:955 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:380 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:584 | print("  [CHKLIST] 配置文件不存在，跳过生成清单") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1198 | print("\n  ── 流程状态 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1217 | print("用法: python hooks.py check|done|status <skil |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1218 | print("  step: init | backup | blueprint | config_ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1219 | print("        function_test | s4 | fix | bump | g |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\hooks.py:1230 | print("请指定步骤: init | backup | blueprint | write_te |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:546 | print(print_bluebook(bb)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\inspector.py:569 | print("用法: python inspector.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:107 | print(state.blueprint_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:116 | print("\n  [S4 阶段A] 提取约束...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:124 | print("\n  [S4 阶段A] 生成全量测试范围...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:130 | print(print_constraint_summary(full_scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:163 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:166 | print("=== 当前配置（来自 .test-config.json）===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:170 | print("\n── 配置自检 ──") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:239 | print("\n  ✅ 配置一致性校验通过，所有项自洽") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:289 | print("  [SKIP] 场景维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:301 | print(s_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:335 | print("  [SKIP] 功能维度均未启用") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:383 | print("  [SKIP] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:402 | print("\n  [S4-修复] 检查可修复项...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:449 | print(state.s4_matrix_text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:457 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:468 | print("  [S4-正向] 无正向追踪记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:469 | print("  ╔═══════ 正向测试：LLM 必须执行 ══════╗") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:470 | print("  ║  按工作流步骤顺序执行并记录到       ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:471 | print("  ║  .s4_positive.json                 ║") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:472 | print("  ╚═════════════════════════════════════╝") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:482 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:483 | print(print_fidelity_score(score_result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:512 | print("  仅报告模式，不执行修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:553 | print("  无待判断问题，跳过修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:584 | print("  未开启修复模式，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:589 | print("  无修复记录，跳过 bump") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:597 | print("  [BUMP] 无法读取版本号，跳过") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:676 | print(state.final_report) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:733 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\runner.py:753 | print("用法: python runner.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:848 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:860 | print(print_constraint_summary(constraints)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:865 | print(print_constraint_summary(scope)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:869 | print("缺少方案 JSON 路径") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:894 | print(print_fidelity_matrix(matrix)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:898 | print(print_workflow_steps(steps)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:902 | print("用法: score <positive_rate> <negative_rate> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:910 | print(print_fidelity_score(result)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:936 | print("[S4-修复] 无需要修复的项") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\s4_engine.py:940 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:637 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\scenario_engine.py:655 | print("用法: python scenario_engine.py <skill-dir>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:269 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:279 | print("用法: cfg rounds <1-5>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:283 | print("轮数必须在 1-5 之间") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:291 | print("用法: cfg fix_mode scenario <0|1>   或   cfg f |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:297 | print("场景修复模式: 0=仅报告 1=尝试修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:304 | print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:314 | print("用法: cfg s4 on/off 或 cfg s4 rounds <N>") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:320 | print("[CFG] S4 已开启") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:324 | print("[CFG] S4 已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:369 | print("[CFG] 已重置为默认配置") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:373 | print("[CFG] 启动配置服务器...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:378 | print(INTERACTIVE_HELP) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:799 | print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:825 | print("\n[CFG] 服务器已关闭") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:834 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:835 | print("  python test_config.py <skill-dir> show    |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:836 | print("  python test_config.py <skill-dir> set <pa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:837 | print("  python test_config.py <skill-dir> reset   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:838 | print("  python test_config.py <skill-dir> server  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:839 | print("  python test_config.py <skill-dir> interac |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:855 | print("用法: set <path> <value> 例: set s4.enabled tr |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_config.py:875 | print("配置交互模式（输入 'q' 退出）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:630 | print("  [FT] 扫描蓝皮书...", flush=True) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:699 | print(text) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_engine.py:715 | print("用法: python test_engine.py <skill-dir> [d1_s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:48 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:58 | print(r.stdout) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:351 | print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:456 | print("\n".join(lines)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:501 | print(USAGE) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:513 | print("用法: ... mark <skill-dir> <phase> <label> [e |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\timeline.py:548 | print(USAGE) |
| D5 | INFO | 发现 36 个验证函数 | PASS | :0 | _hook_check, hook_pre_function_test, hook_post_fun |
| D5 | INFO | 发现 7 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\inspector | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\runner | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\scenario_engine | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_config | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_engine | PASS | :0 |  |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:52 | _walk_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:67 | backup_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\backup.py:93 | list_backups() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\bump_version.py:44 | update_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:40 | log_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:66 | _detect_lang() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:91 | safe_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\fixer.py:315 | fix_js_try_catch() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:23 | _hook_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:28 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:42 | _load_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:49 | _load_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:65 | load_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:343 | gen_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:778 | _write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\gen_report.py:71 | _find_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:34 | _data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:41 | _skill_name() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:47 | _block() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:86 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:89 | _bp_json_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:93 | _bp_legacy_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:96 | _scenario_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:99 | _func_report_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:102 | _backup_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:115 | hook_pre_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:120 | hook_pre_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:130 | hook_pre_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:146 | hook_pre_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:174 | hook_pre_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:205 | hook_pre_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:274 | hook_post_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:279 | hook_pre_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:292 | hook_pre_final_regress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:376 | hook_post_scenario() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:388 | hook_post_function_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:409 | hook_post_s4() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:419 | hook_post_gen_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:428 | hook_pre_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:441 | hook_post_write_conclusion() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:447 | hook_pre_config_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:485 | hook_post_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:490 | hook_pre_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:538 | hook_post_write_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:560 | _checklist_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:564 | _config_checksum() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:576 | _generate_execution_checklist() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:737 | _validate_checklist_step() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:799 | _chk_count_plan_cases() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:827 | _chk_check_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:873 | _chk_count_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:920 | _chk_check_fix_records() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:932 | _chk_check_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:939 | _chk_check_all_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:958 | _chk_check_conclusion_written() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:969 | _save_checklist_item() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:986 | _clean_skill_root() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1003 | _clean_old_test_report_from_permissions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1053 | _flow_state_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1060 | _is_step_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1074 | _check_scenario_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1103 | _check_s4_state() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1131 | _mark_done() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1147 | hook_post_init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1148 | hook_post_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1149 | hook_post_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\hooks.py:1156 | cmd_status() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:127 | _classify_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:168 | _scan_python_ast() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:251 | _scan_md_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:320 | extract_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\inspector.py:407 | scan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:279 | _has_s_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\runner.py:325 | _has_d_dim() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:51 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:143 | load_constraints() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:157 | save_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:165 | load_noise_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:180 | save_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:188 | load_trace() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:224 | load_blueprint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:737 | extract_workflow_steps() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:498 | generate_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\s4_engine.py:566 | playback_all_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:118 | parse_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:158 | auto_build_test_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:575 | run_scenario_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:238 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\scenario_engine.py:372 | add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:64 | config_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:72 | load_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:84 | save_config() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:116 | _merge_defaults() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:133 | get_active_tests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:147 | get_s4_rounds() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:153 | set_value() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:767 | start_server() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:118 | _merge() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_config.py:737 | _do_save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:623 | run_full_test() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:128 | add_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\test_engine.py:204 | _find_cli_scripts() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:83 | _data_dir_for() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:90 | _timeline_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:94 | _load_timeline() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:317 | _find_gap_label() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\timeline.py:347 | cmd_report() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\bump_version.py:0 | scripts\bump_version.py: 1 个 except / 202 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\gen_report.py:0 | scripts\gen_report.py: 2 个 except / 989 行 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)
