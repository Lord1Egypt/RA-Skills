# Changelog

## 0.1.0 — 2026-10-03

首个公开版本。命令：`run`（从 DWG/DXF 找设计方自带的钢筋/材料工程数量表、还原成结构化表格、做 R001–R006 确定性算术核对，输出 `evidence.json` / `钢筋数量表.xlsx` / `report.md`）和 `doctor`（报告运行环境与转换器探测结果）。

镜像（负比例）块参照内的文字与多段线按 WCS 取坐标（修正此前 x 取反）。

验证范围（请按此预期使用）：

- 只在 1 份真实隧道结构图上做过端到端验收：13 条疑点与人工独立核对一致；ODA File Converter 与 GNU LibreDWG 两条 DWG 转换链的结果一致。
- 其它设计院的版式、字体、符号编码尚未验证；遇到对不上的情况，以 `evidence.json` 里的图元 handle 回原图核实。
- DWG 转换器（ODA File Converter / GNU LibreDWG）不随包分发，需用户自行安装；`.dxf` 输入不需要。
