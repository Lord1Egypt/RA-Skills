# Handoff · P5 多账户 batch（供 Task / Bash 子会话）

## 阶段 A · batch 执行（通常由主会话或单次 Bash 完成，非 per-account）

主 Agent **应**在主会话或**一次** Bash 子会话执行，不要用多个子会话替代 CLI 并发：

```bash
# 全量：省略 -a
siluzan-tso google-analysis-batch run \
  --start <S> --end <D> \
  --sections campaigns,geographic,keywords \
  --account-concurrency 4 --section-concurrency 6 \
  --min-spend 1 --keyword-limit 1000 \
  --json-out ./snap-p5

# 中断后续跑（禁止重新 run）
siluzan-tso google-analysis-batch resume --json-out ./snap-p5 --run-id <runId>
```

**forbidden**: 先 `list-accounts` 再拼全量 ID 到 `-a`；禁止子会话对每个账户单独 `google-analysis`。

**returnSchema**: stdout 单行 JSON 摘要、`runId`、exitCode；勿贴 `results/` 下全文 JSON。

---

## 阶段 B · 按账户聚合（可选，可并行多个 Task）

**前提**: batch 已成功或部分成功（exitCode 0 或 2），路径已知：

`snapDir`: `./snap-p5`  
`runId`: `<runId>`  
`accountId`: `<单个 mediaCustomerId>`

**forbidden**:

- 禁止 `google-analysis-batch run` 重新跑
- 禁止 Read 整文件 JSON 进回复；脚本读盘

**任务**:

1. 只处理 `{snapDir}/{runId}/results/{accountId}/` 下文件。
2. 先读各 `*.outline.txt`，再脚本读 `*.json` 聚合。
3. 产出该账户报告片段或中间 CSV/JSON（路径回传）。

**returnSchema**: 产出路径 + 该账户汇总摘要（数字须可追溯至 JSON 路径）。
