# 门禁系统

所有规划、执行操作由 **10 座 HARD 门禁** 串行阻断。门禁状态存 `data/gate_state.json`。

```bash
# 查看全部门禁状态
python {SKILL_DIR}/scripts/chain_gate.py status
# 检查单个门禁（失败则 exit(1) + HOOK-BLOCK）
python {SKILL_DIR}/scripts/chain_gate.py check --name chain_connected
# 强制开放（跳过阻断）
python {SKILL_DIR}/scripts/chain_gate.py set --name chain_connected --status open
# 重置全部门禁
python {SKILL_DIR}/scripts/chain_gate.py reset
```

门禁依赖链（不可跳过）：
blueprint_verified → intent_decomposed → steps_searched → steps_selected → llm_chain_verified → milestones_set → io_validated → adhesion_resolved → chain_connected → chain_saved → chain_loaded → execution_planned → execution_completed

