---
name: visio
description: "Visio（.vsdx）图表的解析、生成、修改与导出能力。当用户要求读取或总结 .vsdx 文件内容、把架构图/流程图/链路图生成为可编辑的 Visio 文件、批量将 .vsdx 导出为 SVG/PNG/PDF、或按固定视觉规范（蓝"
version: 1.0.0
---
# Visio 图表处理

## 概述

本 skill 提供 .vsdx（Visio 2013+）文件的程序化处理能力，覆盖四类任务：

1. **解析**：不依赖 Visio 安装，直接按 OPC 包解包 XML，输出页/图元/连线/文本的结构化摘要。
2. **生成**：由 JSON 规格确定性生成基础框图（矩形/圆角矩形节点 + 直线连线，可设箭头、虚线、标签），产物可用 Visio 打开继续编辑。
3. **修改**：解包 → 改写 pageN.xml → 重新打包的安全修改路径。
4. **导出**：通过 Visio COM 自动化批量导出 SVG/PNG/PDF（需本机安装桌面版 Visio）。

所有产出的视觉规范遵循用户固定配色与制图约定（见 `references/style-mapping.md`）。

## 工作方式

### 第一步：场景分流

读取 `references/workflows.md` 的场景分流表，确定技术路径：

- 「看看/讲讲这个 vsdx」→ 解析摘要路径。
- 「生成可编辑 Visio 图」→ 生成路径（基础框图用脚本；复杂图形先出 SVG 交付并附 Visio 导入指引）。
- 「批量转 SVG/PDF」→ COM 导出路径。
- 「改 vsdx 里的内容」→ 修改路径。
- 「要报告/汇报材料」→ 单文件 HTML 为主，Visio 文件作附件。

### 第二步：按需加载参考

- 需要理解 .vsdx 内部结构、解析或修改 XML 时，读 `references/vsdx-format.md`。
- 需要确定颜色、字体、图类画法时，读 `references/style-mapping.md`。
- 执行生成/导出/修改的具体步骤与注意事项，读 `references/workflows.md`。

### 第三步：调用脚本

| 任务 | 脚本 | 依赖 |
|---|---|---|
| 解析 .vsdx | `python scripts/inspect_vsdx.py <file.vsdx> [--json]` | Python 3 |
| 生成 .vsdx | `python scripts/build_vsdx.py <spec.json> <output.vsdx>` | Python 3 |
| 导出 SVG/PNG/PDF | `scripts/export_via_com.ps1 -InputFile <vsdx> -OutDir <dir> -Format svg` | 桌面版 Visio |

生成流程要点：

1. 依需求设计节点/连线清单，按 style-mapping.md 定坐标（英寸，横向 A4：11.69×8.27）与颜色语义。
2. 写 JSON 规格（格式见 build_vsdx.py 文件头），运行生成脚本。
3. 本机有 Visio 时导出 SVG 自检（文字溢出、箭头方向、配色），再向用户交付。
4. 说明产物为未胶水连接的自由形状，用户可在 Visio 中拖动微调。

## 已知限制

- 生成脚本仅支持矩形/圆角矩形节点与直线连线；泳道、扇形、模具图形需在 Visio 内精修或改走 SVG 交付。
- COM 导出依赖本机 Visio；未安装时交付 .vsdx 并附结构摘要代替预览。

## 资源文件

- `scripts/inspect_vsdx.py` — .vsdx 结构解析器（页/图元/连线/文本，Markdown 或 JSON 输出）。
- `scripts/build_vsdx.py` — JSON 规格 → .vsdx 生成器（颜色 hex、箭头、虚线、标签、圆角）。
- `scripts/export_via_com.ps1` — Visio COM 批量导出 SVG/PNG/PDF。
- `references/vsdx-format.md` — .vsdx OPC 包结构、page XML 要点、Shapesheet 常用单元格。
- `references/style-mapping.md` — 固定配色/字体/图类到 Visio 的映射规则。
- `references/workflows.md` — 场景分流表、生成标准流程、修改注意事项、已知限制。
