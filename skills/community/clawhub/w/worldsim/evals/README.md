# WorldSim — 输出质量评测（evals/）

> 用例定义在 `evals.json`，本文件写运行与判卷方法。

## 定位

- **回答的问题**：skill 改一版之后，核心流程是否仍然全通？改坏了哪里？
- **基线**：前一版本快照，不是无 skill——持久化世界状态是 skill 的价值前提，「无 skill」没有可比性。改版前先快照：

```bash
cp -r <skill目录> <workspace>/skill-snapshot
```

## 目录结构

```
<workspace>/                     # skill 目录之外，不入版本库
└── iteration-1/
    ├── skill-snapshot/          # 基线版本（首轮=上一版；对照运行指向这里）
    ├── eval-1-create-start/
    │   ├── with_skill/outputs/  # 本轮产出：world_final/ 快照 + 执行记录摘录
    │   ├── old_skill/outputs/
    │   ├── timing.json          # {"total_tokens": N, "duration_ms": N}（每配置一份）
    │   └── grading.json         # 断言逐条 PASS/FAIL + 证据
    ├── eval-2-import-card/…
    └── benchmark.json           # 本迭代汇总（两配置的 pass_rate/delta）
```

## 运行流程

1. **干净上下文**：每个用例、每个配置都用独立新会话跑，不带历史。
2. **执行**：给 agent 的输入 = 用例 `prompt` + `setup` 声明的输入文件 + 输出目录路径。用例间有依赖的（2/3 接续 1），在同一迭代内按序复用同一个世界。
3. **留证**：每轮结束后把最终世界状态拷贝到 `outputs/world_final/`，并摘录关键执行记录（写入批次原文、gate/round-check 输出）到 `outputs/traces.md`——断言证据从这里取。
4. **计时**：保存 timing.json（token 数与会话时长）。
5. **清理**：评测世界（`eval-*` 命名）判卷完即删，不进版本库（`worlds/*` 默认忽略，正常不会入库）。

## 判卷

断言分两级，逐条记 PASS/FAIL，PASS 必须附具体证据（引用文件/输出原文），无证据视为 FAIL：

- **机械断言**（脚本核验，可重复）：在 `world_final` 上直接跑现成工具——
  - round-check / validate：`python3 <skill>/scripts/worldctl.py <世界> round-check`、`validate`
  - 批次格式：抽查 traces.md 中批次首行是否为 `###STAGE:`；audit 报错即 FAIL
  - 编码：已知中文关键词在 narrative.md 中 grep 可命中（乱码=FAIL）；yaml 无 CRLF
- **判断型断言**（认知边界、数据忠诚、调度具名等）：交 LLM 判卷或人工，结论必须引用叙事/状态原文作证据。

人工 review 另记 `feedback.json`（用例名 → 具体意见；空串=通过）。`human_review` 字段列出的是不可断言化的整体质量项，只出意见不出 PASS/FAIL。

benchmark.json 格式照 evaluating-skills.mdx：两配置各自的 pass_rate 均值 + delta。

## 迭代循环

1. 首批只跑用例 1-3（文档建议：别在看到第一轮结果前过度投资）；4/5 稳定后再加入。
2. 三路信号汇合改 skill：失败断言 → 具体缺口；feedback → 质量问题；traces → 为什么错。
3. 改动进入 AGENTS.md 证据链复盘流程定位根因；修复落地后开 `iteration-N+1` 全量重跑验证「没把别处改坏」。
4. 结果不再改善或 feedback 连续为空即停。
