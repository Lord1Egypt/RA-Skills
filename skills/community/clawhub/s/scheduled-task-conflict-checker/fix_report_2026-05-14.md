# scheduled-task-conflict-checker 评测修复记录

## 来源

- 评测报告：`/Users/wangzhilelelelele/Downloads/评测报告_scheduled-task-conflict-checker_2026-5-14.pdf`
- 评测版本：0.3.0
- 评测时间：2026-05-14 16:13:50

## 修复项

1. 修复失败项 `tracker_script`
   - 新增 `scripts/_tracker.py`。
   - 打点只记录脚本事件、决策、是否需要提示和 finding 数量。
   - 不记录用户原始话术、店铺、商品、订单、AK、Token、Cookie 或授权凭证。

2. 修复/降低 `output_contract` 风险
   - `check_scheduled_task_conflicts.py` 新增 `--json` 和 `--markdown` 参数。
   - `SKILL.md` 明确 JSON 输出结构和退出码约定。
   - 非法输入返回 exit code `2`，并向 stderr 输出结构化错误 JSON。

3. 修复/降低 `has_workflow` 风险
   - `SKILL.md` 新增 `Workflow / 执行步骤`。
   - 明确读取输入、标准化、边界检查、重复检查、输出决策、等待用户确认的执行顺序。

4. 修复/降低 `has_guardrails` 与 `error_constraints` 风险
   - `SKILL.md` 新增 `Guardrails / 约束`。
   - 明确“严禁/不得”绕过冲突检测、静默合并高风险任务、暴露敏感凭证、编造上下文。

5. 保持 ISV 文案
   - 用户可见文案继续使用 `ISV 高级版`。
   - 内部兼容字段和 reason code 仍保留 `sv_advanced_permission_missing` 等旧契约，避免破坏调用方。

## 验证

```bash
python3 -m py_compile scripts/check_scheduled_task_conflicts.py scripts/_tracker.py
python3 scripts/check_scheduled_task_conflicts.py benchmarks/lui_conflict_50_cases/fixtures/case_016/input.json --json
python3 benchmarks/lui_conflict_50_cases/tools/run_benchmark.py
```

验证结果：

- 语法检查通过。
- 非法输入返回 exit code `2`。
- 50 组 benchmark：50 通过，0 失败，0 错误。
- `runtime/task_pool.json` 执行后不存在。
