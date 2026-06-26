# Handoff · P7 Google 询盘分析（供 Task / Bash 子会话）

> 主 Agent 已确认 3 个月窗口与 `mediaCustomerId`。询盘数据已在 `./snap-inquiry/inquiries.json`（流程 A/B 完成后）。

## 变体 · 主 snap 拉数（单次）

**snapDir**: `./snap-inquiry`

```bash
siluzan-tso list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-inquiry
siluzan-tso google-analysis -a <mediaCustomerId> \
  --start <S> --end <D> \
  --sections campaigns,keywords,search-terms,campaign-geo \
  --json-out ./snap-inquiry
```

**forbidden**: 禁止编造询盘行；禁止 7 个月窗口。

**returnSchema**: exitCode、writtenFiles、outlineFiles、stderrTail、summary。

---

## 变体 · 月度 m1 / m2 / m3（可并行 3 个子会话）

| 子任务 | snapDir             | 命令                                                                                                             |
| ------ | ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| m1     | `./snap-inquiry/m1` | `google-analysis -a <id> --start <M1S> --end <M1E> --sections campaigns,geographic --json-out ./snap-inquiry/m1` |
| m2     | `./snap-inquiry/m2` | 同上，M2 日期                                                                                                    |
| m3     | `./snap-inquiry/m3` | 同上，M3 日期                                                                                                    |

**forbidden**: 禁止用 `daily-metrics` 填 Sheet 4 上区；禁止主会话 Read 全量 JSON。

**returnSchema**: 各目录 manifest + exitCode。

---

## 变体 · 写 8 Sheet xlsx（单次，主 Agent 或一个 Task）

**snapDir**: `./snap-inquiry`（含 m1/m2/m3 子目录）

**任务**: 读 `report-templates/google-inquiry-analysis.md` 版式；脚本读 JSON + `references/analytics/geo-continents.json`；产出 xlsx。

**returnSchema**: xlsx 路径 + exitCode；勿贴表内全部单元格。
