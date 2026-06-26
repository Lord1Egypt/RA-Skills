# Handoff · P6 OKKI 周报（供 Task / Bash 子会话）

> 主 Agent 派发前已确认 `mediaCustomerId`、`--start`、`--end`。将下列占位符替换为实值。

## 角色

你是 siluzan-tso **拉数**子任务（或 **写 xlsx** 子任务，见阶段）。只执行指定命令或脚本，不向用户对话。

## 阶段 A · 拉数（委派本阶段时使用）

**snapDir**: `./snap-okki`（或主 Agent 指定路径）

**forbidden**:

- 禁止在回复中粘贴完整 JSON 内容
- 禁止编造 mediaCustomerId
- 禁止写 xlsx、禁止写操作类 CLI

**commands**（在同一 snapDir 依次执行）:

```bash
mkdir -p ./snap-okki

siluzan-tso list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-okki

siluzan-tso stats -m Google -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-okki

siluzan-tso balance -m Google -a <mediaCustomerId> --json-out ./snap-okki

siluzan-tso google-analysis -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-okki \
  --sections overview,campaigns,keywords,search-terms,campaign-device,campaign-geo-matched
```

**returnSchema**: 仅回传 exitCode、manifestFile、writtenFiles、outlineFiles、stderrTail、summary（无编造数字）。

## 阶段 B · 写 xlsx（委派本阶段时使用）

**snapDir**: 同上（拉数已完成）

**forbidden**:

- 禁止在脚本中写死业务数字；数值只来自落盘 JSON
- 禁止跳过 outline；先读 `*.outline.txt` 再读 JSON

**任务**:

1. Read `report-templates/okki-weekly-google-client.md` 中 xlsx 版式（若子会话可 Read skill 内路径）。
2. 编写并执行 Node/Python 脚本，产出 `.xlsx` + 客户话术。
3. 设备/国家 Sheet 必须用 `campaign-device` / `campaign-geo-matched` 落盘文件。

**returnSchema**: 产出文件路径列表 + 脚本 exitCode；勿贴 xlsx 二进制内容。
