# .vsdx 文件格式要点

> .vsdx（Visio 2013+ 默认格式）是基于 OPC（Open Packaging Convention）的 ZIP 包，与 docx/xlsx 同族。理解结构后才能可靠地读、改、生成。

## 1. 包结构

```
diagram.vsdx
├── [Content_Types].xml          # 部件内容类型声明
├── _rels/.rels                  # 包级关系（指向主文档）
├── docProps/
│   ├── core.xml / app.xml
└── visio/
    ├── document.xml             # 文档级设置（FaceNames、样式表、颜色表）
    ├── _rels/document.xml.rels  # → pages.xml、windows.xml
    ├── windows.xml
    └── pages/
        ├── pages.xml            # 页目录（每页一个 <Page> + <Rel>）
        ├── _rels/pages.xml.rels # 页 ID → pageN.xml 部件映射
        └── page1.xml            # 页面内容（Shapes / Connects）
```

关键命名空间：`http://schemas.microsoft.com/office/visio/2012/main`（元素）、`http://schemas.openxmlformats.org/officeDocument/2006/relationships`（关系引用 r:id）。

## 2. 页面内容（pageN.xml）

- 根元素 `<PageContents>`，下含 `<Shapes>` 与可选 `<Connects>`。
- **二维图元**：`<Shape Type="Shape">`，定位单元格 `PinX`/`PinY`（中心点，英寸）、`Width`/`Height`/`LocPinX`/`LocPinY`/`Angle`。
- **一维连线**：同 `<Shape>`，但带 `BeginX`/`BeginY`/`EndX`/`EndY` 属性，几何 Section 用本地坐标（MoveTo 0,0 → LineTo Width,Height）。
- **几何**：`<Section N="Geometry">` 内按 Row（MoveTo/LineTo/RelMoveTo/RelLineTo/EllipticalArcTo…）描述轮廓；`Rel*` 行坐标为 0–1 相对值，随宽高缩放。
- **文本**：`<Text>` 直接子元素；样式由 `<Section N="Character">`（Font/Size/Color，Size 单位为英寸，12pt=0.1667）与 `<Section N="Paragraph">`（HorzAlign：0 左 1 中 2 右）控制。
- **填充/线条**：`FillBkgnd`/`FillForegnd`（颜色公式如 `RGB(24,95,165)`）、`FillPattern`（1=纯色）、`LineColor`/`LineWeight`/`LinePattern`（2=虚线）、`EndArrow`（4=实心箭头）。

## 3. 形状引用与连接

- 从模板拖入的形状带 `Master` 属性（指向 `visio/masters/` 中的模具定义）；程序化生成的简单形状通常 `Master="-1"` 且无 masters 部件。
- 胶水连接记录在 `<Connect FromSheet="连线ID" FromCell="BeginX" ToSheet="图元ID" ToCell="PinX"/>`；`inspect_vsdx.py` 会输出这些关系。
- 解析他人交付的 .vsdx 时，优先看 `Master` 与 `Connects`，可判断图元语义与拓扑。

## 4. 解析要点（供 inspect_vsdx.py 对照）

1. `_rels/.rels` 找到 document.xml → `visio/_rels/document.xml.rels` 找到 pages.xml → `visio/pages/_rels/pages.xml.rels` 把页 ID 映射到 pageN.xml。
2. 每页遍历 `<Shape>`：有 `BeginX` 属性即连线，否则为图元；`<Text>` 用 itertext 拼接。
3. 中文名优先取 `NameU`（通用名），其次 `Name`。

## 5. 生成与修改的可行路径

| 需求 | 路径 | 依赖 |
|---|---|---|
| 程序化新建基础框图 | `scripts/build_vsdx.py`（JSON → .vsdx） | 仅 Python |
| 解析/盘点已有 .vsdx | `scripts/inspect_vsdx.py` | 仅 Python |
| 导出 SVG/PNG/PDF | `scripts/export_via_com.ps1` | 本机安装 Visio |
| 复杂美化、模具形状 | 生成 SVG 后在 Visio 中「插入 SVG」或手工精修 | Visio |
| 批量改形状文本/颜色 | Python 改写 pageN.xml 后重新打包 ZIP | 仅 Python |
