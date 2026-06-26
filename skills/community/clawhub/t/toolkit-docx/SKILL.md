---
name: istarshine-docx
description: >
  创建、读取、编辑或操作 Word 文档（.docx 文件）。
  支持从零创建专业文档（含目录、标题、页码、信头等格式），
  编辑现有文档（查找替换、插入图片、处理修订和批注），
  以及提取和重组文档内容。
  当用户提到 Word、.docx 或要求生成报告、备忘录、信件等文档时使用。
  不要用于 PDF、电子表格或 Google 文档。
license: "Proprietary. See LICENSE.txt for complete terms."
metadata:
  version: 0.21.4
  author: istarshine
  display_name: "Word 文档处理"
  tags:
    - 工具
---

# DOCX 创建、编辑与分析

## 概述

.docx 文件是一个包含 XML 文件的 ZIP 压缩包。

## 快速参考

| 任务 | 方法 |
|------|----------|
| 读取/分析内容 | 使用 `pandoc` 或解包查看原始 XML |
| 创建新文档 | 使用 `docx-js` - 参见下文的"创建新文档" |
| 编辑现有文档 | 解包 → 编辑 XML → 重新打包 - 参见下文的"编辑现有文档" |

### 将 .doc 转换为 .docx

旧版的 `.doc` 文件必须先进行转换才能进行编辑：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 提取带有修订记录的文本
pandoc --track-changes=all document.docx -o output.md

# 访问原始 XML
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图片

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受修订

生成包含所有已接受修订的干净文档（需要 LibreOffice）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

使用 JavaScript 生成 .docx 文件，然后进行验证。安装：`npm install -g docx`

### 设置
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证
创建文件后，对其进行验证。如果验证失败，进行解包，修复 XML，然后重新打包。
```bash
python scripts/office/validate.py doc.docx
```

### 页面大小

```javascript
// 注意：docx-js 默认页面大小为 A4，而非美式信纸（US Letter）
// 始终明确设置页面大小以获得一致结果
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 英寸（单位：DXA）
        height: 15840   // 11 英寸（单位：DXA）
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 英寸边距
    }
  },
  children: [/* 内容 */]
}]
```

**常见页面大小（单位为 DXA，1440 DXA = 1 英寸）：**

| 纸张 | 宽度 | 高度 | 内容宽度 (1" 边距) |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 (默认) | 11,906 | 16,838 | 9,026 |

**横向（Landscape）排版：** docx-js 在内部交换宽高，因此请传递纵向尺寸并让它处理交换：
```javascript
size: {
  width: 12240,   // 将短边作为宽度传递
  height: 15840,  // 将长边作为高度传递
  orientation: PageOrientation.LANDSCAPE  // docx-js 会在 XML 中交换它们
},
// 内容宽度 = 15840 - 左边距 - 右边距 (使用长边)
```

### 样式（覆盖内置标题）

使用 Arial 作为默认字体（普遍支持）。标题保持黑色以增强可读性。

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt 默认大小
    paragraphStyles: [
      // 关键：使用精确的 ID 以覆盖内置样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // TOC 需要 outlineLevel 属性
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题")] }),
    ]
  }]
});
```

### 列表（切勿使用 Unicode 项目符号）

```javascript
// ❌ 错误做法：切勿手动输入项目符号字符
new Paragraph({ children: [new TextRun("• 项目")] })  // 错误
new Paragraph({ children: [new TextRun("\u2022 项目")] })  // 错误

// ✅ 正确做法：使用带 LevelFormat.BULLET 的 numbering（编号）配置
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("带项目符号的项")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("带编号的项")] }),
    ]
  }]
});

// ⚠️ 每个 reference（引用）都会创建独立的编号：
// 相同引用 = 延续 (1,2,3 接着 4,5,6)
// 不同引用 = 重新开始 (1,2,3 接着 1,2,3)
```

### 表格

**关键点：表格需要双重宽度声明**——既要在表格设置 `columnWidths`（列宽），也需要为每个单元格（cell）设置 `width`（宽）。如果不同时设置，表格在某些平台上可能会渲染错误。

```javascript
// 关键点：始终设置表格宽度以获得一致的渲染
// 关键点：使用 ShadingType.CLEAR（非 SOLID）防止背景变黑
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 务必使用 DXA（百分比在 Google Docs 中会出错）
  columnWidths: [4680, 4680], // 必须其和等于表格宽度（DXA：1440 = 1 英寸）
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 务必在每个单元格上也进行设置
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // 必须使用 CLEAR，不能用 SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 单元格内补白（内部空间，不增加整体宽度）
          children: [new Paragraph({ children: [new TextRun("单元格")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算法：**

始终使用 `WidthType.DXA` — `WidthType.PERCENTAGE` 在 Google Docs 会失效。

```javascript
// 表格宽度 = sum of columnWidths = 内容宽度
// 使用 1" 边距的 US Letter：12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // 求和必须等于表格宽度
```

**宽度规则：**
- **务必使用 `WidthType.DXA`** ——绝不能用 `WidthType.PERCENTAGE`（不兼容 Google Docs）
- 表格宽度（width）必须等于 `columnWidths` 之和
- 单元格 `width` 必须与相应的 `columnWidth` 匹配
- 单元格 `margins` 控制内置补距 - 缩小内容区可用空间，而非增加单元格总宽度
- 全宽表格：使用内容宽度（页面宽度减去左右边距）

### 图片

```javascript
// 关键点：type 参数不可或缺
new Paragraph({
  children: [new ImageRun({
    type: "png", // 必须指定：png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // 这三项都需提供
  })]
})
```

### 分页符（Page Breaks）

```javascript
// 关键点：PageBreak 必须包裹在 Paragraph 内
new Paragraph({ children: [new PageBreak()] })

// 或使用 pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("新页面")] })
```

### 链接

```javascript
// 外部链接
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "点击此处", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// 内部链接 (书签 + 引用)
// 1. 在目标处创建书签
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("第1章")] }),
]})
// 2. 链向该位置
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "参见第1章", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### 脚注（Footnotes）

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("资料来源：2024 年报")] },
    2: { children: [new Paragraph("方法论详见附录")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("使用调整后的指标"),
        new FootnoteReferenceRun(2),
        new TextRun("，收入增长了 15%"),
        new FootnoteReferenceRun(1),
      ],
    })]
  }]
});
```

### 制表符（Tab Stops）

```javascript
// 同一行的右对齐文本（如对面对着标题的日期）
new Paragraph({
  children: [
    new TextRun("公司名称"),
    new TextRun("\t2025年1月"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// 引线（例如目录样式）
new Paragraph({
  children: [
    new TextRun("引言"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### 多栏布局

```javascript
// 等宽分栏
sections: [{
  properties: {
    column: {
      count: 2,          // 栏数
      space: 720,        // 栏与栏间隙（单位：DXA，720 = 0.5英寸）
      equalWidth: true,
      separate: true,    // 分隔线
    },
  },
  children: [/* 内容跨栏自适应流动 */]
}]

// 自定义宽度分栏（此时 equalWidth 必须为 false）
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* 内容 */]
}]
```

如果要强制从新的分栏开始内容，请创建使用 `type: SectionType.NEXT_COLUMN` 的新区域（section）。

### 目录（Table of Contents）

```javascript
// 关键点：只有被标记 HeadingLevel 级别的段落才能被追踪并加入目录 - 请勿使用自定义样式标记标题
new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 英寸
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("页眉")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("第 "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" 页")]
    })] })
  },
  children: [/* 内容 */]
}]
```

### 关于 docx-js 的重要原则

- **显式设置页面大小** - docx-js 默认使用 A4；对于美国文档，请使用 US Letter（12240 x 15840 DXA）。
- **横向排版：传递纵向尺寸** - docx-js 内部自动切换宽高，故传递短边作为 `width`，长边作为 `height`，并将方向设为：`orientation: PageOrientation.LANDSCAPE`。
- **避免使用 `\n`** - 请改用独立的 Paragraph 元素。
- **避免使用 Unicode 圆点** - 结合采用 `LevelFormat.BULLET` 的编号配置。
- **分页符（PageBreak）必须置于 Paragraph 内** - 单独放置会生成无效 XML。
- **ImageRun 亟需带入 `type`** - 切记指定 png/jpg 格式。
- **永远以 DXA 设置表格 `width`** - `WidthType.PERCENTAGE` 会导致在 Google Docs 格式渲染破坏。
- **表格需声明双向宽度** - 既提供 `columnWidths` 数组，也设置逐个单元格的 `width`；必须完美契合。
- **表格宽度 = 列宽的加总** - 为了让表以 DXA 正确展现，这必须严格对等。
- **请务必定义单元格内部间距`margin`** - 使用诸如 `margins: { top: 80, bottom: 80, left: 120, right: 120 }` 让其有充分布白而提高可看性。
- **表格请用 `ShadingType.CLEAR`** - 背景遮罩（shading）切莫用 SOLID。
- **不要用空表去实现装饰线或行间线** - 因为在有的平台上可能会展示出预想之外的最小框或线条。请用特定段落的底边边框（如：`border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }`）。对于拥有多列排列需求的页脚，多用 Tab Stops。
- **目录（TOC）只能读取到具有纯正HeadingLevel级别的标题段** - 在此类标题上不得使用自定义外壳样式。
- **要完全覆盖原有默认预置的样式规则** - 请精准命名 ID: "Heading1", "Heading2"。
- **别忘了赋予 `outlineLevel` 属性** - (如H1对应0, H2对应1)，否则这会导致它不被载入到目录。

---

## 编辑现有文档

**请务必按先后顺序推进以下 3 步操作。**

### 第一步：解包（Unpack）
```bash
python scripts/office/unpack.py document.docx unpacked/
```
解析出内部XML数据，提供结构化易读的排版并且规整相关联的运行文本，还能妥善规避处理单双引智能符号问题将之编码为XML的符号（诸如 `&#x201C;`）规避丢失。如想取消合并文本片断可以加参数 `--merge-runs false`。

### 第二步：编辑XML数据

在子文件夹 `unpacked/word/` 之内处理这些XML代码。具体格式细节看后面的“XML数据规范要点”说明。

**建议指派 "Author" 或相似称谓记录那些批注和修订标记事件的使用者**：除非用户指定要求显示特定称呼。

**直接用编辑器工具替代文本字串，请尽量别用独立的Python代码来解决。**由于编写执行复杂的代码不仅提高处理成本和容错率反而常常画蛇添足。直接可视化替换会精准快捷。

**极为关键：对于新的补充语段请遵循专业的智能圆滑标点（Smart quotes）。** 当增加带撇号甚至单双引的新字段时，请用 XML 字符实体，好呈现考究的特殊符号：
```xml
<!-- 利用以上字符为文档提供更讲究和贴合字型的专业印刷呈现要求 -->
<w:t>看看这段引用：&#x201C;您好。&#x201D;</w:t>
```
| 实体标签 | 对应字符 |
|--------|-----------|
| `&#x2018;` | ‘ (左单引) |
| `&#x2019;` | ’ (右单引 / 省略撇号) |
| `&#x201C;` | “ (左双引号) |
| `&#x201D;` | ” (右双引号) |

**添加注释（批注）：** 多处文件的关联注释结构需要用 `comment.py` 代为搞定繁重连环更新，免生遗漏（参数文本务需遵循XML实体反转义保护模式操作）：
```bash
python scripts/comment.py unpacked/ 0 "带 &amp; 或者 &#x2019; 等符号的评论文"
python scripts/comment.py unpacked/ 1 "针对上文跟帖回复" --parent 0  # 这是针对0号批注的附属答复
python scripts/comment.py unpacked/ 0 "随意填写的留言内容" --author "自定义人名"  # 指定自定义发出人
```
然后在 `document.xml` 具体行添加对应的书签界域指针标识（详情参见之后的 XML 注释范例点拨）。

### 第三步：重新封卷（Pack）
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
过程中自动尝试验证并且自带修复机制然后重新将其压缩回归 DOCX 标准制式输出。不希望校验可以使用参数 `--validate false` 跳跑过。

**自动回正功能可矫正如下：**
- 修改大到溢出 `durableId` >= 0x7FFFFFFF 的标记（生成合法新标识ID）
- 为具备隐藏留白字符的文本 `<w:t>` 补发 `xml:space="preserve"`

**自动功能所没有办法搭救的事项涵盖：**
- 不对的XML架构标签或者严重错位的结构层级嵌套（也就是缺失该存在的包含关系等致命故障）

### 常见缺陷/难点

- **直接整体置换原始的文本片段 `<w:r>` ：** 增加系统级改版修订的时候请注意使用同级替换技巧。就是采用 `<w:del>` 包裹旧的搭配另外加装 `<w:ins>` 塞进去成为一个相连紧挨的平行新骨架。千万不可直接把这些外壳修定符生猛强行塞进现有 `<w:r>` 体内。
- **保留 `<w:rPr>` 修饰特征：** 重置的修订跑段务必承接旧有的段落格式要求模块（也就是需要把那些包含加粗字体甚至预设字号等的 `<w:rPr>` 统统接过来照抄套用上）。

---

## XML 语法要点

### Schema 校验与格式依规

- `<w:pPr>` **元素从上到下的强制顺序为**：`<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`, 最后才是 `<w:rPr>`
- **留白判定（Whitespace）**：如果 `<w:t>` 内容里的前后首尾存在真正的空格，必须要配合打上标记 `xml:space="preserve"`
- **RSIDs**：需要确认为严格 8 位数长度且必须只能处于 Hex 区间（例如：`00AB1234`）

### 修订记录（Tracked Changes）

**新增：**
```xml
<w:ins w:id="1" w:author="Author" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>新增的文本</w:t></w:r>
</w:ins>
```

**删除：**
```xml
<w:del w:id="2" w:author="Author" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>被删去的话语</w:delText></w:r>
</w:del>
```

**处于 `<w:del>` 的下层内部**：需要相应使用 `<w:delText>` 以此替换原本常规的 `<w:t>`。并把 `<w:instrText>` 换做等价撤回命令号的 `<w:delInstrText>`。

**尽量用最小化影响的精改法** - 比如只是改变了些微小变动就不需牵扯到周边文辞：
```xml
<!-- 从 "30 days" 换成 "60 days" -->
<w:r><w:t>对应的工期为 </w:t></w:r>
<w:del w:id="1" w:author="Author" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Author" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> 个工作日。</w:t></w:r>
```

**如果删空或者截除整个段落/或者罗列的系列节点** - 既然要让这一行全部干干净净不留踪迹，那么切记必须要标记其结尾最末端潜藏的段落控制号以让它可以自然与它下一段贴合。需要在最上方标签 `<w:pPr><w:rPr>` 下插入控制子 `<w:del/>`:
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- （假使本来身处带编列序列表范围） -->
    <w:rPr>
      <w:del w:id="1" w:author="Author" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Author" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>被您完全无痕摘除删除的完整全篇幅长篇文字...</w:delText></w:r>
  </w:del>
</w:p>
```
倘若忽略了顶端头部配置所辖的 `<w:pPr><w:rPr>` 里那个隐形子符 `<w:del/>` 取接操作结束后那里最终必然会滞留个完全碍眼的空无一物段落断层空白。

**回绝或拒采非自身的第三方增加字句** - 就是包裹一套将其退撤丢入垃圾堆里的结构法则嵌套：
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Author" w:id="10">
    <w:r><w:delText>他们妄想加入的一些新东西等</w:delText></w:r>
  </w:del>
</w:ins>
```

**将别的作者以前误丢废弃字串拯救归位还原过来** - 用另起增词在它周边去添设同义副本（请忌尝试破坏原人废弃语句原本面貌状态）：
```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>已经被其所删丢词条数据</w:delText></w:r>
</w:del>
<w:ins w:author="Author" w:id="10">
  <w:r><w:t>已经被其所删丢词条数据</w:t></w:r>
</w:ins>
```

### 批注（Comments）

运行了前期步骤中指代的 `comment.py` （参见 第 2 步），那你就开始要为其配置关联对应的 xml 位置起终点包裹挂靠了（document.xml）。 如果属对旧留言做盖楼回帖追评等，可以通过加置使用 `--parent` 标志进而把它囊括到老祖先界限界碑包围领空区域范围内。

**千万注重！： `<w:commentRangeStart>` 跟 `<w:commentRangeEnd>` 必须置为最外围与各个 `<w:r>` 们兄弟相交错排列。别让其陷落在任意 `<w:r>` 圈层内部之下作为次属小部件存活。**

```xml
<!-- 批注标记必须是 w:p 的直接子元素，切勿放在 w:r 内部 -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Author" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>被抹去的</w:delText></w:r>
</w:del>
<w:r><w:t> 残留句子文本等等</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- ID为0的关键主贴。其腹肚里挂有一套与之同源互动 ID是1的一级跟帖套叠串联现象 -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>文本</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 图片（Images）

1. 把真实图片扔进目标子结构夹 `word/media/`
2. 为关联地图增加配置引导联系词 `word/_rels/document.xml.rels`：
```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```
3. 在类型说明中附上该新载入的介质的品种声名：`[Content_Types].xml`：
```xml
<Default Extension="png" ContentType="image/png"/>
```
4. 将该标识正式加入呼叫运用（于 document.xml 文件中）：
```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- 单位为 EMU：914400 即代表 1英寸的长短值 -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

---

## 依赖关系

- **pandoc**: 文本提取转换
- **docx**: `npm install -g docx` (生成新的全新空本文卷必备)
- **LibreOffice**: 担任PDF及部分转换的核心基石（通过 `scripts/office/soffice.py` 将自动调配兼容隔离保护沙箱安全区执行）
- **Poppler**: 通过 `pdftoppm` 命令搞定图档裁切与生成转化
