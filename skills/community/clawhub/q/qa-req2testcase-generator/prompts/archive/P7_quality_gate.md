# P7 质量门禁（已归档）

> ⚠️ **此文件已废弃** | V3.3.1 起 P7 改为代码校验（`p7_code_check` action），不再使用此 prompt。
> 此文件仅作历史参考，代码中不再依赖。

## 历史说明

- V3.3.0 及之前：P7 通过此 prompt 调用 Agent 做质量门禁
- V3.3.1 起：P7 改为 `orchestrator --action p7_code_check`，纯代码校验绕过 LLM

## 原文件内容（仅供参考）

P7 质量门禁的核心检查项：
- P0 用例占比 ≤ 40%
- 冒烟用例覆盖率
- 伞形用例检测（C9 规则）
- 字段完整性校验

详见 `tools/truncation_guard.py` L3_SCHEMA 定义。
