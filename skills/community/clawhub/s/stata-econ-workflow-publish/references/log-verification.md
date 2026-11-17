---
paths:
  - "dofiles/**/*.do"
  - "reports/**/*.qmd"
  - "quality_reports/**"
  - "logs/**"
---

# Log Verification Protocol

> 源自 codex-stata-for-economists (陈铸)。本工作流的**基石规则**。

**没有日志，就没有结论。** 每个关于分析的数值声明都必须能追溯到 `logs/*.log` 文件中的一行，
或 `output/tables/*.csv`/`*.tex` 中的一个单元格。

---

## 何时触发

- 总结日志/计划/commit message/报告中的结果时
- 填写复现目标行时
- 回答"模型对X的结果是什么？"时
- 任何包含可归因于回归、模拟或描述统计的数字的句子

---

## 如何遵守

对于每个数值陈述，必须：

1. **标识来源人工产物：**
   - 特定的日志文件（`logs/03_analysis_main_regression.log`）+ 行号/上下文
   - **或** `output/tables/*.csv` 中的特定单元格（行+列）
   - **或** 保存在的估计值（`estimates use ...`）——但优先读取底层日志

2. **引用相关行**（或者用上下文引用该值）首次引入该数字时

3. **使用 `log-validator` agent** 在任何提交前进行校验

4. **如果还没有日志**，拒绝陈述该结果。改说：
   > "我无法陈述该结果。do文件 `dofiles/03_analysis/main_regression.do` 自上次编辑后尚未运行（无新的 `logs/03_analysis_main_regression.log`），因此我没有日志行来支持该声明。您希望我 (a) 运行该do文件，还是 (b) 从报告中移除该数值声明？"

---

## 什么算"日志行"

**可以接受的：**
- `_b[treated]` 被Stata在 `regress` / `reghdfe` / `ivreg2` 后显示的结果
- `esttab` 写入 `.tex` 或 `.csv` 的表格
- `summarize` 表格输出
- `tabulate` 输出
- `display` 命令打印的值（仅当 `display` 明确是do文件的一部分时，非交互式）

**不可以接受的：**
- Claude从其他报告数字中手算的值（除非计算过程显示且很简单）
- 之前Stata会话的日志，不再存在时
- 用户分享的截图或粘贴的输出（视作输入而非项目人工产物——要求重新运行）

---

## log-validator 工作流

输入到agent：
- 声明（例如："主规范的ATT是-1.632 (SE 0.584)"）
- 候选日志文件路径

Agent步骤：
1. 读取日志文件
2. 在合理邻域内搜索声明的系数和标准误（例如 `reghdfe ... cluster(state_id)` 的输出）
3. 如找到，验证与声明是否在容差内匹配（容差参考 `quality-gates.md`）
4. 如未找到，返回 `UNVERIFIED — number does not appear in <logfile>`

Agent输出：
- `VERIFIED — found at <logfile>:<line>`（含匹配摘录），**或**
- `UNVERIFIED — <reason>`

提交前必须 `VERIFIED`。`UNVERIFIED` 阻止提交，直到： (a) do文件被重新运行且产生新日志，或 (b) 声明被移除。

---

## Commit Message 纪律

每个提及数值结果的commit message必须引用日志：

```
Update main regression table with clustered SE

ATT estimate: -1.632 (SE 0.584, clustered at state)
Source: logs/03_analysis_main_regression.log (line 412)
```

`log-validator` agent 在 `/commit` 时会自动被调用。

---

## 不能验证时怎么说

> "我无法陈述该结果。没有日志文件来支持该声明。要 (a) 运行 do 文件来生成日志，还是 (b) 从报告中移除这个数字？"

这个措辞非灵活——宁可多问也不要编造。
