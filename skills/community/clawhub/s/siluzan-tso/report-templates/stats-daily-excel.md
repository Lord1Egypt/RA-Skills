# 账户按日投放数据 Excel（stats --by-day）

> 账户级**按日**消耗表 → Excel。≠ P4 / P4-FB / P1。无 CLI excel 子命令。

```bash
siluzan-tso list-accounts -m <媒体> -k <id> --json-out ./snap
siluzan-tso stats -m <媒体> -a <id> --start <S> --end <E> --by-day --json-out ./snap/daily.json
```

脚本读 `items[]`（含 `date`、`spend`、`impressions`、`clicks`、`conversions` 等）写 xlsx。建议 Sheet：每日明细 + 汇总。ID 列文本；CTR/CPA 由脚本派生。

**样式（必须）**：`import` `report-templates/excel-style-kit.mjs`，`createExcelWorkbook({ accent: <按 -m 媒体取值：google/tiktok/yandex/bingv2/facebook(MetaAd)> })` + `titleBar`/`tableHeader`/`dataRow` 组件搭版面，不裸写无样式单元格。规范见 `report-templates/excel-style-guide.md`。
