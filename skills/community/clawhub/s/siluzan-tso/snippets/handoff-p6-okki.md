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
  --sections overview,campaigns,keywords,search-terms,campaign-device,geo-targeted
```

**returnSchema**: 仅回传 exitCode、manifestFile、writtenFiles、outlineFiles、stderrTail、summary（无编造数字）。

## 阶段 B · 写叙事 JSON + okki-render（委派本阶段时使用）

**snapDir**: 同上（拉数已完成）

**forbidden**:

- 禁止在脚本中写死业务数字；数值只来自落盘 JSON
- 禁止跳过 outline；先读 `*.outline.txt` 再读 JSON
- 禁止 Agent 手写 / 脚本写 xlsx；必须走 `google-analysis okki-render`

**任务**:

1. Read `report-templates/okki-weekly-google-client.md` 的 **§对外客户话术**。交回的话术是一个代码块：行首为「您好，同步一下谷歌」、`1、消耗：`、`2、展示点击：`、`3、点击率：`、`4、平均点击单价：`、`5、转化：`、`5.1`、`5.2`、`6、优化建议：`、①②③ 各一行、`7、账户余额：`。主 Agent 若写明用户本轮换了骨架，照那个骨架交回，不要自己再改一版。
2. 按 `assets/okki-weekly-report.schema.json` 写 `okki-weekly-report.json`：只填 `meta` + `narrative.sheetAnalysis`（5 Sheet，各 summary≥1 / suggestions≥1）+ `narrative.review`（固定 5 维：账户/关键词/搜索字词/设备/国家，每维 overview+summary+suggestion）。表为空也须写分析。`campaign-device` 的 `deviceType` 是 `Desktop`/`Mobile`/`Tablet`（不是 `DESKTOP`/`MOBILE`）；设备消耗按 `toLowerCase()` / `includes("desktop")` 分类累加，**禁止** `.get("DESKTOP")`。
3. 执行：
   ```bash
   siluzan-tso google-analysis okki-render \
     --data ./okki-weekly-report.json \
     --snapshot-dir <snapDir> \
     --out ./okki-weekly-report.xlsx
   ```
   失败则按 stderr 补 JSON 后重跑，不得改用手写表。
4. 设备/国家必须来自 `campaign-device` / `geo-targeted`（由 render 校验）。国家不要用 `campaign-geo-matched`，那会把已移除的国家算进来。

**returnSchema**: xlsx 路径 + `okki-render` exitCode + 客户话术代码块（行首见任务 1；用户本轮换过骨架则用用户的）。勿贴 xlsx 二进制，勿另附「结论先行」摘要。
