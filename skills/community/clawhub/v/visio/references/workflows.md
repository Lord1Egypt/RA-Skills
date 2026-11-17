# 场景工作流

> 按用户请求分流到合适的技术路径。原则：能不依赖 Visio 安装就不依赖；需要精修时在 Visio 中完成最后一步。

## 1. 场景分流表

| 用户请求 | 路径 | 工具 |
|---|---|---|
| 「看看/讲讲这个 vsdx 的内容」 | 解析摘要 | inspect_vsdx.py |
| 「把这张图改成 Visio 格式」 | 复杂图：先出 SVG 交付，附 Visio 导入指引；基础框图：build_vsdx.py 直接生成 | build_vsdx.py / Visio |
| 「生成一张可编辑的 Visio 框图/链路图」 | JSON 规格 → .vsdx → COM 导出 SVG 复核 → 交付 | build_vsdx.py + export_via_com.ps1 |
| 「批量把 vsdx 转成 SVG/PDF」 | COM 批量导出 | export_via_com.ps1 |
| 「改已有 vsdx 里的文字/颜色」 | 解包 → 改 pageN.xml → 重新打包 | Python（zipfile + XML） |
| 「要报告/汇报材料」 | 出单文件 HTML（内嵌 SVG），Visio 文件作为附件另给 | HTML + 本 skill |

## 2. 生成可编辑 Visio 图的标准流程

1. 依据需求设计节点与连线清单（节点 id、坐标、文案、颜色语义按 style-mapping.md）。
2. 写 JSON 规格文件（坐标单位英寸，横向 A4：宽 11.69、高 8.27）。
3. 运行 `python scripts/build_vsdx.py spec.json output.vsdx`。
4. 本机有 Visio 时运行 `export_via_com.ps1` 导出 SVG 自检：文字不溢出、箭头方向正确、配色正确。
5. 发现问题优先改 JSON 重新生成；布局微调可交用户在 Visio 内拖动（形状未做胶水连接，移动自由）。

## 3. 修改已有 .vsdx 的注意事项

- 重新打包时保持 `[Content_Types].xml` 与 `_rels` 结构不变，仅替换 visio/pages/pageN.xml。
- 修改形状单元格时保留原有 `Master` 引用，否则模具图元会失去样式。
- 改文本注意 `<Text>` 内的 `cp/pp` 游标引用；简单替换文字优先整体重写 Text 节点并保留 Character/Paragraph Section。
- 操作前先用 inspect_vsdx.py 备份一份结构摘要，便于回滚对照。

## 4. 已知限制

- build_vsdx.py 仅支持矩形/圆角矩形节点与直线连线；泳道、扇形、模具图形需 Visio 内精修或改用 SVG 交付。
- 生成的连线是中心到中心的直线，不做边缘吸附；交付说明中告知用户可在 Visio 中拖动调整。
- COM 导出需要桌面版 Visio；未安装时改为交付 .vsdx + 说明，或用 inspect 摘要代替预览。
- Visio 页面导出 SVG 后嵌入 HTML 报告时，统一用浅色底（用户偏好）。
