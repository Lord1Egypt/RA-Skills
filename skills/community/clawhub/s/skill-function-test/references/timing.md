# 测试流程时间线 — 使用说明

## 三级嵌套计时体系

| 层级 | 范围 | 标记者 | 时间粒度 | 是否自动 |
|------|------|--------|---------|---------|
| **L1 技能加载** | 从用户下达测试指令 → skill-function-test 加载完成 | 首个 py_script 开始 | ms 级 | ✅ 自动 |
| **L2 各阶段** | 备份、蓝皮书扫描、写测试案例、场景测试、功能测试、S4、报告等 | 各脚本自动 mark start/end | ms 级 | ✅ 自动 |
| **L3 测试执行** | 每个测试用例、每个 subprocess 调用目标脚本 | 脚本内部 `_tl()` + `_exec()` 自动标记 | us 级 | ✅ 自动 |

## 间隙推导（Gap Deduction）

`timeline.py report --validate` 模式自动执行间隙分析。两个 py_script end → 下一个 py_script start 之间的 gap 归类为 LLM 时段。根据工作流序列自动打标签。

## 验证模式

```
python scripts/timeline.py report <skill-dir> --validate
```

输出阶段覆盖状态和未归属长间隙检测。
