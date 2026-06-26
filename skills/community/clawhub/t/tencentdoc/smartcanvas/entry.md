# 文档（SmartCanvas）工具完整参考文档

腾讯文档（SmartCanvas）提供了一套完整的文档元素操作 API，支持对页面、文本、标题、待办事项等元素进行增删改查操作。

---

## 目录

- [概念说明](#概念说明)
- [创建智能文档 — create_smartcanvas_by_mdx](#创建智能文档--create_smartcanvas_by_mdx)
- [统一编辑工具（推荐）](#统一编辑工具推荐)
  - [smartcanvas.read - 读取页面内容](#smartcanvasread)
  - [smartcanvas.find - 搜索文档内容](#smartcanvasfind)
  - [smartcanvas.edit - 编辑文档内容](#smartcanvasedit)
    - [边界场景处理规范](#边界场景处理规范)
- [典型工作流示例](#典型工作流示例)
  - [工作流一：用户指定了编辑位置（有查询意图）](#工作流一用户指定了编辑位置有查询意图)
  - [工作流二：用户未指定编辑位置（无查询意图）](#工作流二用户未指定编辑位置无查询意图)
  - [工作流三：在「XXX」后插入内容](#工作流三在xxx后插入内容)
  - [工作流四：修改「XXX」为新内容](#工作流四修改xxx为新内容)
  - [工作流五：删除「XXX」](#工作流五删除xxx)
  - [工作流六：直接追加内容到文档末尾](#工作流六直接追加内容到文档末尾)
  - [工作流七：创建分栏布局](#工作流七创建分栏布局)
  - [工作流八：向已有分栏中添加内容](#工作流八向已有分栏中添加内容)
  - [工作流九：修改分栏列数或宽度比例](#工作流九修改分栏列数或宽度比例)

---

## 概念说明

| 概念 | 说明 |
|------|------|
| `file_id` | 文档的唯一标识符，每个文档有唯一的 file_id |
| `page_id` | 页面 ID，Page 是文档的基本容器单元，可通过 `smartcanvas.read` 读取页面内容 |
| `Block ID` | 块 ID，`smartcanvas.read` / `smartcanvas.find` 返回的 MDX 中 `id` 属性值，用于 `smartcanvas.edit` 定位锚点 |

**文档结构**：

```
file_id（文档）
└── Page（页面）
    ├── Heading（标题，level 1-6）
    ├── Paragraph / Text（段落/文本）
    ├── BulletedList / NumberedList（列表）
    ├── Todo（待办事项）
    ├── Table（表格）
    ├── Callout（高亮块）
    ├── ColumnList（分栏布局）
    ├── Image（图片）
    └── ...（更多组件详见 mdx_references.md）
```

> ⚠️ **重要约束**：
> - 所有内容块（Block）必须挂载在 `Page` 下
> - `Page` 可以不指定父节点（挂载到根节点）
> - 完整的组件列表和规范详见 `mdx_references.md`

---

## 创建智能文档 — create_smartcanvas_by_mdx

**【创建文档的首选工具】** 创建排版丰富的在线智能文档。

**【格式选择】** 通过 `content_format` 参数指定内容格式：
- **mdx（默认，强烈推荐）**：支持分栏布局 ColumnList、高亮块 Callout、待办列表 Todo、表格 Table、带样式文本 Mark 等丰富排版组件，适用于需要复杂排版和视觉效果的场景。内容必须严格遵循 `mdx_references.md` 规范，生成后须对照规范逐条自校验，确保合规后再提交。
- **markdown**：仅当用户明确要求时使用，`mdx` 字段传入标准 Markdown 格式内容即可，无需遵循 MDX 组件规范。

**【图片约束（两种格式通用）】** 所有图片禁止直接使用 http/https 外链，必须先调用 `upload_image` 工具上传获取 `image_id`，再填入对应位置：
- **MDX 格式**：封面图 `cover: image_id值`，正文图片 `<Image src='image_id值' alt='描述' />`
- **Markdown 格式**：`![描述](image_id值)`
- 如果图片过大导致上传失败，必须先本地压缩图片再重新上传，严禁回退使用 URL。

**📖 MDX 规范详见：** `mdx_references.md`

### 工作流

```
【MDX 格式（默认，content_format 为空或 "mdx"）】
1. 阅读 mdx_references.md 了解 MDX 组件规范（组件、属性、取值白名单、格式约束）
2. 按规范生成包含 Frontmatter 和 MDX 组件的内容
3. ⚠️【图片前置检查 - 必须执行】检查 MDX 内容中是否包含 <Image> 图片元素或 frontmatter cover 封面图：
   a. 如果包含图片：必须先调用公共工具 upload_image（详见 references/workflows.md）上传每张图片获取 image_id
   b. 将 image_id 填入对应位置：封面图 cover: image_id值，正文图片 <Image src='image_id值' alt='描述' />
   c. 严禁在 src 或 cover 中直接使用 http/https 外部网络链接，系统不支持外部 URL，会导致图片无法显示
   d. 如果图片过大导致 upload_image 上传失败，必须先本地压缩图片，再重新上传，严禁回退使用 URL
4. 对照 mdx_references 逐条自校验，确保格式合规（特别检查 frontmatter cover 和所有 <Image> 的 src 值均为 image_id 而非 URL）
5. 调用 create_smartcanvas_by_mdx 创建文档（传入 title + MDX 内容）
6. 从返回结果中获取 file_id 和 url

【Markdown 格式（content_format 为 "markdown"）】
1. 按标准 Markdown 格式编写内容，无需遵循 MDX 组件规范
2. ⚠️【图片前置检查 - 必须执行】检查 Markdown 内容中是否包含图片：
   a. 如果包含图片：必须先调用公共工具 upload_image（详见 references/workflows.md）上传每张图片获取 image_id
   b. 将 image_id 填入图片语法中：![描述](image_id值)
   c. 严禁直接使用 http/https 外部网络链接
   d. 如果图片过大导致 upload_image 上传失败，必须先本地压缩图片，再重新上传，严禁回退使用 URL
3. 调用 create_smartcanvas_by_mdx 创建文档（传入 title + Markdown 内容 + content_format="markdown"）
4. 从返回结果中获取 file_id 和 url
```

> ⚠️ **图片强制约束（创建场景 & 编辑场景均适用，MDX 和 Markdown 两种格式通用）**：
> - **绝对禁止**直接使用外部网络 URL（如 `https://example.com/image.png`），系统不支持外部链接，图片将无法显示。
> - **所有图片**（无论 MDX 还是 Markdown 格式）**必须**先通过公共工具 `upload_image`（详见 `references/workflows.md`）上传获取 `image_id`，再将 `image_id` 填入对应位置。
> - **MDX 格式写法**：
>   - 正文图片：`<Image src="aGVsbG8gd29ybGQ=" alt="描述" />`（src 值为 upload_image 返回的 image_id）
>   - 封面图：`cover: aGVsbG8gd29ybGQ=`（cover 值为 upload_image 返回的 image_id）
> - **Markdown 格式写法**：
>   - 图片：`![描述](aGVsbG8gd29ybGQ=)`（括号内为 upload_image 返回的 image_id）
> - 错误示例：`<Image src="https://example.com/photo.jpg" alt="描述" />`（❌ 严禁使用 URL）
> - 错误示例：`cover: https://example.com/banner.jpg`（❌ 严禁使用 URL）
> - 错误示例：`![描述](https://example.com/photo.jpg)`（❌ 严禁使用 URL）
> - 图片地址必须使用 `src` 属性（MDX 格式），严禁使用 `imageId`、`image_id` 等非标准属性名。
> - `image_id` 有效期为一天，请在获取后及时使用。
> - **图片过大处理**：如果图片文件过大导致 `upload_image` 上传失败，**必须先在本地压缩图片**（建议压缩到 50KB 以内）再重新上传，**严禁**因上传失败而回退使用 URL。
> - **注意**：由于 `upload_image` 的 `image_base64` 字段可能非常大（图片越大 Base64 字符串越长），建议通过 Python 脚本等方式直接构造 HTTP 请求调用 MCP 接口，避免 AI 模型逐 token 生成 Base64 字符串导致超时或截断。

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文档标题。参数名必须为 `title`，不要使用 `doc_title`、`name`、`file_name` 等其他名称 |
| `mdx` | string | ✅ | 文档正文内容。默认使用 MDX 格式：必须严格符合 `mdx_references` 规范，生成前须阅读 `mdx_references` 了解组件定义和格式约束，生成后须逐条自校验（frontmatter 格式、缩进规则、组件写法、属性语法、颜色 token 等）。当 `content_format` 为 `"markdown"` 时：传入标准 Markdown 格式内容即可，无需遵循 MDX 组件规范。图片约束：无论哪种格式，都必须先通过 `upload_image` 上传获取 `image_id`，MDX 中用 `<Image src='image_id值' />`，Markdown 中用 `![描述](image_id值)`，严禁使用 http/https 外链 |
| `content_format` | string | | 内容格式。可选值：`"mdx"`（默认，推荐）、`"markdown"`。为空时默认 mdx 格式，支持丰富排版组件；仅当不需要高级排版或用户明确要求时才指定为 `"markdown"` |

### 调用示例

```json
{
  "title": "项目需求文档",
  "mdx": "---\ntitle: 项目需求文档\nicon: 📋\n---\n\n# 项目需求\n\n<Callout icon=\"📌\" blockColor=\"light_blue\" borderColor=\"blue\">\n    本项目旨在开发一套智能文档管理系统。\n</Callout>\n\n## 功能需求\n\n<BulletedList>\n    文档创建功能\n</BulletedList>\n<BulletedList>\n    文档编辑功能\n</BulletedList>\n<BulletedList>\n    协作功能\n</BulletedList>"
}
```

### 调用示例（Markdown 格式）

当 `content_format` 为 `"markdown"` 时，`mdx` 字段传入标准 Markdown 格式内容即可，无需遵循 MDX 组件规范：

```json
{
  "title": "项目需求文档",
  "mdx": "# 项目需求\n\n> 本项目旨在开发一套智能文档管理系统。\n\n## 功能需求\n\n- 文档创建功能\n- 文档编辑功能\n- 协作功能\n\n## 时间规划\n\n| 阶段 | 时间 | 负责人 |\n|------|------|--------|\n| 需求分析 | 第1周 | 张三 |\n| 开发 | 第2-4周 | 李四 |",
  "content_format": "markdown"
}
```

### 返回值说明

```json
{
  "file_id": "doc_1234567890",
  "url": "https://docs.qq.com/doc/DV2h5cWJ0R1lQb0lH",
  "error": "",
  "trace_id": "trace_1234567890"
}
```

---

## 统一编辑工具（推荐）

> 💡 **推荐使用统一编辑工具**：`smartcanvas.read` + `smartcanvas.find` + `smartcanvas.edit` 组合，支持 MDX 格式内容、更简洁的 API 设计。

### smartcanvas.read

**功能**：读取智能文档指定页面的完整 MDX 格式内容。一次调用即返回页面全部内容。

**使用场景**：
- 在编辑文档前先阅读全文，了解文档结构和内容
- 获取页面完整内容用于分析、总结或摘要
- `smartcanvas.find` 找不到目标内容时，降级用本工具获取全文查找

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | string | ✅ | 智能文档的唯一标识符 |
| `page_id` | string | | 要读取的页面 ID，为空时自动获取文档的第一个页面 |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `content` | string | 页面完整的 MDX 格式文本内容 |
| `error` | string | 错误信息 |
| `trace_id` | string | 调用链追踪 ID |

**调用示例（读取文档第一个页面）**：

```json
{
  "file_id": "your_file_id"
}
```

**调用示例（读取指定页面）**：

```json
{
  "file_id": "your_file_id",
  "page_id": "page_abc123"
}
```

**返回示例**：

```json
{
  "content": "## 项目背景\n\n本项目旨在提升用户体验...\n\n## 总结\n\n以上是文档的全部内容。"
}
```

---

### smartcanvas.find

**功能**：根据文本搜索智能文档中的 Block，返回匹配 Block 的 ID 和 MDX 格式内容。搜索结果中的 Block ID 可作为锚点，用于 `smartcanvas.edit` 的精准编辑操作。

**使用场景**：
- 定位文档中某段内容的位置，获取 Block ID 作为编辑锚点
- 搜索包含特定关键词的内容块

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | string | ✅ | 智能文档的唯一标识符 |
| `query` | string | ✅ | 搜索文本，系统将在文档所有页面中搜索包含该文本的 Block |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `blocks` | array | 匹配的 Block 列表 |
| `blocks[].id` | string | Block 的唯一标识符（锚点 ID） |
| `blocks[].content` | string | Block 的 MDX 格式内容 |
| `error` | string | 错误信息 |
| `trace_id` | string | 调用链追踪 ID |

**调用示例**：

```json
{
  "file_id": "your_file_id",
  "query": "项目背景"
}
```

**返回示例**：

```json
{
  "blocks": [
    {
      "id": "block_abc123",
      "content": "## 项目背景\n\n本项目旨在提升用户体验..."
    }
  ]
}
```

---

### smartcanvas.edit

**功能**：编辑智能文档，支持 4 种操作类型：在指定位置前/后插入、删除、修改。

**操作类型说明**：

| Action | 说明 | id 参数 | content 参数 |
|--------|------|---------|----------|
| `INSERT_BEFORE` | 在指定 Block 前插入内容 | 锚点 Block ID（必填） | MDX 格式内容（必填） |
| `INSERT_AFTER` | 在指定 Block 后插入内容 | 锚点 Block ID（为空则追加到文档末尾） | MDX 格式内容（必填） |
| `DELETE` | 删除指定 Block | 要删除的 Block ID（必填，⚠️ 必须先通过 find/read 获取） | 不需要 |
| `UPDATE` | 修改指定 Block 的内容 | 要修改的 Block ID（必填，⚠️ 必须先通过 find/read 获取） | 新的 MDX 格式内容（必填） |

> ⚠️ **强制约束**：`UPDATE` 和 `DELETE` 操作的 `id` 参数**必须**来源于 `smartcanvas.find` 或 `smartcanvas.read` 的返回结果，**禁止**在未获取文档数据的情况下直接传入 id 执行 UPDATE 或 DELETE 操作。

> ⚠️ **readonly 约束**：当 `smartcanvas.find` 或 `smartcanvas.read` 返回的 MDX 内容中，某个块级组件（如 `<Table>`）带有 `readonly` 属性时，表示该组件及其所有子元素为只读状态。**禁止**使用只读组件或其内部子元素的 `id` 作为 `smartcanvas.edit` 的锚点（INSERT_BEFORE / INSERT_AFTER / UPDATE / DELETE 均不可用）。如需在只读组件附近操作，应选择只读组件上方或下方的非只读 Block 作为锚点。

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | string | ✅ | 智能文档的唯一标识符 |
| `action` | enum | ✅ | 操作类型：INSERT_BEFORE / INSERT_AFTER / DELETE / UPDATE |
| `id` | string | 条件 | 锚点 Block ID，见上表说明 |
| `content` | string | 条件 | MDX 格式内容，见上表说明 |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | string | 错误信息 |
| `trace_id` | string | 调用链追踪 ID |

**调用示例（在指定 Block 后插入内容）**：

```json
{
  "file_id": "your_file_id",
  "action": "INSERT_AFTER",
  "id": "block_abc123",
  "content": "## 新章节\n\n这是插入的新内容。"
}
```

**调用示例（追加到文档末尾）**：

```json
{
  "file_id": "your_file_id",
  "action": "INSERT_AFTER",
  "content": "追加到文档末尾的内容"
}
```

**调用示例（删除指定 Block）**：

```json
{
  "file_id": "your_file_id",
  "action": "DELETE",
  "id": "block_abc123"
}
```

**调用示例（修改指定 Block）**：

```json
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "block_abc123",
  "content": "## 修改后的标题\n\n这是更新后的内容。"
}
```

---

### 边界场景处理规范

#### 1. `ColumnList` 分栏删除边界场景

- **删除后只剩 1 个 Column**：不允许 `ColumnList` 中只有一个 `Column`，必须将整个 `ColumnList`（包含剩余 `Column` 内的所有内容）用 `UPDATE` 操作替换为普通块内容（将 `Column` 内的子块直接平铺输出，去掉 `ColumnList` / `Column` 容器）。
- **删除后剩余 2 个或更多 Column**：需要用 `UPDATE` 操作更新整个 `ColumnList`，重新均分或合理分配各 `Column` 的 `width`（例如两列各 `50%`，三列各 `33%`）。
- **操作方式**：上述两种情况均不能只 `DELETE` 单个 `Column`，必须对 `ColumnList` 整体执行 `UPDATE`，传入调整后的完整 MDX 内容。

```json
// 删除一列后只剩一列 → 将 ColumnList 整体替换为普通块内容
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "columnlist_id",
  "content": "剩余 Column 内子块平铺后的 MDX 内容"
}
```

```json
// 删除一列后仍剩多列 → 更新整个 ColumnList 并重新分配 width
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "columnlist_id",
  "content": "<ColumnList>\n    <Column width=\"50%\">\n        左列内容\n    </Column>\n    <Column width=\"50%\">\n        右列内容\n    </Column>\n</ColumnList>"
}
```

#### 2. `Callout` 内容清空边界场景

- 当用户要删除 `Callout` 内的全部内容时，`Callout` 本身也应一并删除，不允许保留空的 `Callout` 容器。
- **操作方式**：对 `Callout` 的 `id` 执行 `DELETE` 操作，而非仅删除其内部子块。

```json
{
  "file_id": "your_file_id",
  "action": "DELETE",
  "id": "callout_id"
}
```

#### 3. `BlockQuote` 内容清空边界场景

- 当 `BlockQuote` 内的全部内容被删除时，`BlockQuote` 本身也应一并删除，不允许保留空的 `BlockQuote` 容器。
- **操作方式**：对 `BlockQuote` 的 `id` 执行 `DELETE` 操作，而非仅删除其内部子块。

```json
{
  "file_id": "your_file_id",
  "action": "DELETE",
  "id": "blockquote_id"
}
```

#### 4. 列表（`BulletedList` / `NumberedList` / `Todo`）删除含子项的列表项边界场景

- 当删除某个列表项时，若该列表项下存在子列表项（嵌套的 `BulletedList` / `NumberedList` / `Todo`），子项不能悬空独立存在。
- **操作方式**：对该列表项的 `id` 执行 `DELETE` 操作，系统会连同其所有子项一并删除；若需保留子项内容，应先用 `UPDATE` 将子项内容提升到父级或平铺为独立块，再执行 `DELETE`。

```json
// 直接删除父项（子项一并删除）
{
  "file_id": "your_file_id",
  "action": "DELETE",
  "id": "parent_list_item_id"
}
```

#### 5. `TableRow` / `TableCell` 使用边界场景

- `TableRow` 禁止单独存在，只能作为 `Table` 的直接子元素；`TableCell` 禁止单独存在，只能作为 `TableRow` 的直接子元素。
- **禁止**使用 `TableRow` 或 `TableCell` 的 `id` 作为 `INSERT_BEFORE` / `INSERT_AFTER` 的锚点，向表格内部插入非表格结构的内容。
- **禁止**单独对 `TableRow` 或 `TableCell` 执行 `DELETE` 操作（删除单行/单格），如需修改表格结构，应对整个 `Table` 执行 `UPDATE`，传入调整后的完整表格 MDX 内容。
- **禁止**单独对 `TableCell` 执行 `UPDATE` 操作修改单元格内容，同样应对整个 `Table` 执行 `UPDATE`，传入完整表格 MDX 内容。
- 注意：`Table` 通常带有 `readonly` 属性，此时 `TableRow` / `TableCell` 的 `id` 同样不可用，任何操作均需绕开只读表格，选择其上方或下方的非只读 Block 作为锚点。

```json
// 修改表格内容（如删除某行、修改某单元格）→ 对整个 Table 执行 UPDATE
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "table_id",
  "content": "<Table>\n    <TableRow>\n        <TableCell>\n            列1内容\n        </TableCell>\n        <TableCell>\n            列2内容\n        </TableCell>\n    </TableRow>\n</Table>"
}
```

---

### 图片编辑说明

当 `smartcanvas.edit` 的 `content`（MDX 内容）中包含 `<Image>` 图片元素时，需要遵循以下流程：

**图片处理流程**：

```
步骤 1：上传图片获取 image_id
  → 调用公共工具 upload_image（详见 references/workflows.md）上传图片的 base64 内容
  → 从返回结果中获取 image_id（有效期一天）

步骤 2：将 image_id 设置到 MDX 的 Image 组件 src 属性中
  → <Image src="upload_image返回的image_id" alt="描述" />
```

> ⚠️ **重要**：
> - **编辑场景与创建场景一致**：所有图片（包括 frontmatter cover 和正文 `<Image>`）**必须**先通过公共工具 `upload_image`（详见 `references/workflows.md`）上传获取 `image_id`，再将 `image_id` 设置到对应属性中。
> - 图片地址必须使用 `src` 属性，严禁使用 `imageId`、`image_id` 等非标准属性名。
> - `upload_image` 返回的 `image_id` 值也必须设置到 `src` 属性中（如 `<Image src="image_id值" />`）。
> - `image_id` 有效期为一天，请在获取后及时使用。
> - **图片过大处理**：如果图片文件过大导致 `upload_image` 上传失败，**必须先在本地压缩图片**（建议压缩到 50KB 以内）再重新上传，**严禁**因上传失败而回退使用 URL。
> - **注意**：由于 `upload_image` 的 `image_base64` 字段可能非常大（图片越大 Base64 字符串越长），建议通过 Python 脚本等方式直接构造 HTTP 请求调用 MCP 接口，避免 AI 模型逐 token 生成 Base64 字符串导致超时或截断。

**调用示例（使用 upload_image 上传后插入图片）**：

```json
// 步骤 1：先调用 upload_image 获取 image_id
// 步骤 2：将 image_id 设置到 content 的 Image src 属性中
{
  "file_id": "your_file_id",
  "action": "INSERT_AFTER",
  "id": "block_abc123",
  "content": "<Image src=\"upload_image返回的image_id\" alt=\"示例图片\" />"
}
```

---

## 典型工作流示例

> ⚠️ **编辑位置定位策略（核心原则）**：
> - **有查询意图 / 用户指定了编辑位置关键词**：优先使用 `smartcanvas.find` 搜索定位。找到后展示给用户确认锚点位置，再执行编辑。找不到则降级使用 `smartcanvas.read` 获取全文来猜测位置。
> - **无查询意图 / 用户未指定编辑位置**：直接使用 `smartcanvas.read` 获取全文内容，根据文档结构猜测合适的锚点位置。插入到最前使用 `INSERT_BEFORE`（指定首个 Block ID），插入到最后使用 `INSERT_AFTER`（id 为空）。
> - **⚠️ UPDATE/DELETE 强制前置条件**：执行 `UPDATE` 或 `DELETE` 操作前，**必须**先通过 `smartcanvas.find` 或 `smartcanvas.read` 获取文档数据，从返回结果中选择具体的锚点 Block ID 后才能执行，**禁止跳过此步骤**。

### 工作流一：用户指定了编辑位置（有查询意图）

```
步骤 1：使用 find 搜索目标 Block
  → smartcanvas.find(file_id, query="用户指定的关键词")
  → 检查搜索结果

步骤 2A：find 找到匹配 Block
  → 将 find 返回的 Block 列表展示给用户确认
  → 用户确认锚点位置后，调用 smartcanvas.edit 传入确认的锚点 ID 执行操作

步骤 2B：find 未找到匹配 Block（降级）
  → 调用 smartcanvas.read(file_id) 读取文档全部内容
  → 在返回的 content 中查找目标内容
  → 根据找到的内容分析并猜测合适的锚点位置
  → 调用 smartcanvas.edit 执行编辑操作
```

### 工作流二：用户未指定编辑位置（无查询意图）

```
步骤 1：读取文档全部内容（⚠️ UPDATE/DELETE 操作此步骤为必须）
  → smartcanvas.read(file_id)
  → 返回的 content 即为页面完整 MDX 内容，了解文档结构

步骤 2：根据文档内容和用户意图猜测锚点位置，执行编辑操作
  → 插入到文档最前面：smartcanvas.edit(action=INSERT_BEFORE, id=首个Block ID, content=MDX内容)
  → 插入到文档最后面：smartcanvas.edit(action=INSERT_AFTER, id为空, content=MDX内容)
  → 插入到特定位置：smartcanvas.edit(action=INSERT_BEFORE/INSERT_AFTER, id=猜测的锚点ID, content=MDX内容)
  → 修改特定内容：smartcanvas.edit(action=UPDATE, id=目标Block ID, content=新MDX内容)【id 必须来自 find/read 结果】
  → 删除特定内容：smartcanvas.edit(action=DELETE, id=目标Block ID)【id 必须来自 find/read 结果】
```

### 工作流三：在「XXX」后插入内容

```
步骤 1：搜索定位目标 Block
  → smartcanvas.find(file_id, query="XXX")

步骤 2A：找到匹配 Block
  → 展示 find 结果给用户确认锚点位置
  → 用户确认后，调用 smartcanvas.edit(action=INSERT_AFTER, id=确认的锚点ID, content=MDX内容)

步骤 2B：未找到匹配 Block（降级）
  → smartcanvas.read(file_id) 获取全文
  → 根据全文内容猜测"XXX"附近的锚点位置
  → smartcanvas.edit(action=INSERT_AFTER, id=猜测的锚点ID, content=MDX内容)
```

### 工作流四：修改「XXX」为新内容

```
步骤 1：搜索定位目标 Block
  → smartcanvas.find(file_id, query="XXX")

步骤 2A：找到匹配 Block
  → 展示 find 结果给用户确认目标 Block
  → 用户确认后，调用 smartcanvas.edit(action=UPDATE, id=确认的Block ID, content=新MDX内容)

步骤 2B：未找到匹配 Block（降级）
  → smartcanvas.read(file_id) 获取全文
  → 根据全文内容定位目标位置
  → smartcanvas.edit(action=UPDATE, id=目标Block ID, content=新MDX内容)
```

### 工作流五：删除「XXX」

```
步骤 1：搜索定位目标 Block
  → smartcanvas.find(file_id, query="XXX")

步骤 2A：找到匹配 Block
  → 展示 find 结果给用户确认要删除的 Block
  → 用户确认后，调用 smartcanvas.edit(action=DELETE, id=确认的Block ID)

步骤 2B：未找到匹配 Block（降级）
  → smartcanvas.read(file_id) 获取全文
  → 根据全文内容定位目标位置
  → smartcanvas.edit(action=DELETE, id=目标Block ID)
```

### 工作流六：直接追加内容到文档末尾

```
步骤 1：直接追加到文档末尾（无需定位）
  → smartcanvas.edit(file_id, action=INSERT_AFTER, id为空, content=MDX内容)
```

### 工作流七：创建分栏布局

> 适用场景：用户希望在文档中新增一个左右分栏区域（如「左边放说明，右边放示例」）。

```
步骤 1：确定插入位置
  → 若用户指定了位置关键词：smartcanvas.find(file_id, query="关键词") 获取锚点 Block ID
  → 若用户未指定位置：smartcanvas.read(file_id) 获取全文，根据文档结构选择合适锚点

步骤 2：构造 ColumnList MDX 内容
  → 两列等宽示例（各 50%）：
     <ColumnList>
         <Column width="50%">
             左列内容（可包含 Heading、Paragraph、BulletedList 等任意块）
         </Column>
         <Column width="50%">
             右列内容
         </Column>
     </ColumnList>
  → 三列等宽示例（各 33%）：
     <ColumnList>
         <Column width="33%">
             第一列内容
         </Column>
         <Column width="33%">
             第二列内容
         </Column>
         <Column width="34%">
             第三列内容
         </Column>
     </ColumnList>
  ⚠️ 注意：ColumnList 至少需要 2 个 Column，width 之和应为 100%

步骤 3：调用 smartcanvas.edit 插入分栏
  → smartcanvas.edit(file_id, action=INSERT_AFTER, id=锚点Block ID, content=ColumnList MDX内容)
  → 若插入到文档末尾：id 为空
```

**调用示例**：

```json
// 在 block_abc123 后插入一个两列分栏
{
  "file_id": "your_file_id",
  "action": "INSERT_AFTER",
  "id": "block_abc123",
  "content": "<ColumnList>\n    <Column width=\"50%\">\n        ## 功能说明\n\n        这里描述功能的详细说明。\n    </Column>\n    <Column width=\"50%\">\n        ## 代码示例\n\n        这里放对应的代码示例。\n    </Column>\n</ColumnList>"
}
```

### 工作流八：向已有分栏中添加内容

> 适用场景：用户希望在某个已存在的分栏（ColumnList）的某一列中追加或修改内容。

```
步骤 1：读取文档内容，获取目标 ColumnList 的完整 MDX 结构
  → smartcanvas.find(file_id, query="分栏内已知的关键词")
    或 smartcanvas.read(file_id) 获取全文
  → 找到目标 ColumnList 的 id 及其完整 MDX 内容

步骤 2：在原有 MDX 基础上修改目标列的内容
  → 保持 ColumnList / Column 结构不变
  → 仅在目标 Column 内追加或修改子块内容
  ⚠️ 注意：不能单独对 Column 内的子块执行 INSERT_BEFORE/INSERT_AFTER，
     必须对整个 ColumnList 执行 UPDATE，传入完整的新 MDX 内容

步骤 3：调用 smartcanvas.edit 更新整个 ColumnList
  → smartcanvas.edit(file_id, action=UPDATE, id=ColumnList的Block ID, content=更新后的完整ColumnList MDX)
```

**调用示例**：

```json
// 在右列末尾追加一条说明（对整个 ColumnList 执行 UPDATE）
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "columnlist_block_id",
  "content": "<ColumnList>\n    <Column width=\"50%\">\n        ## 功能说明\n\n        这里描述功能的详细说明。\n    </Column>\n    <Column width=\"50%\">\n        ## 代码示例\n\n        这里放对应的代码示例。\n\n        > 注意：示例仅供参考，请根据实际情况调整。\n    </Column>\n</ColumnList>"
}
```

### 工作流九：修改分栏列数或宽度比例

> 适用场景：用户希望将两列分栏改为三列，或调整各列宽度比例（如从 50/50 改为 30/70）。

```
步骤 1：读取文档内容，获取目标 ColumnList 的完整 MDX 结构
  → smartcanvas.find(file_id, query="分栏内已知的关键词")
    或 smartcanvas.read(file_id) 获取全文
  → 找到目标 ColumnList 的 id 及其完整 MDX 内容

步骤 2：构造调整后的完整 ColumnList MDX
  → 增加列：在原有 Column 基础上新增 Column，重新分配 width（各列 width 之和为 100%）
  → 调整宽度：修改各 Column 的 width 属性值
  → 减少列（删除后剩余 ≥ 2 列）：移除目标 Column，重新均分剩余列的 width
  → 减少列（删除后只剩 1 列）：将 ColumnList 整体替换为普通块内容（参见边界场景处理规范第 1 条）
  ⚠️ 注意：width 之和必须为 100%，且 ColumnList 至少保留 2 个 Column

步骤 3：调用 smartcanvas.edit 更新整个 ColumnList
  → smartcanvas.edit(file_id, action=UPDATE, id=ColumnList的Block ID, content=调整后的完整ColumnList MDX)
```

**调用示例（两列改三列）**：

```json
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "columnlist_block_id",
  "content": "<ColumnList>\n    <Column width=\"33%\">\n        ## 第一列\n\n        第一列内容。\n    </Column>\n    <Column width=\"33%\">\n        ## 第二列\n\n        第二列内容。\n    </Column>\n    <Column width=\"34%\">\n        ## 第三列\n\n        新增的第三列内容。\n    </Column>\n</ColumnList>"
}
```

**调用示例（调整宽度比例为 30/70）**：

```json
{
  "file_id": "your_file_id",
  "action": "UPDATE",
  "id": "columnlist_block_id",
  "content": "<ColumnList>\n    <Column width=\"30%\">\n        ## 侧边说明\n\n        简短的辅助说明内容。\n    </Column>\n    <Column width=\"70%\">\n        ## 主要内容\n\n        详细的主体内容区域。\n    </Column>\n</ColumnList>"
}
```

---

> 📌 **提示**：
> - 所有操作都需要先获取 `file_id`，可通过 `manage.search_file` 搜索文档获取，或在创建文档时从返回结果中获取。
> - **编辑定位优先级**：有查询意图时先 `find` → find 不到则降级 `read` 全文；无查询意图时直接 `read` 全文猜测锚点或使用 `INSERT_BEFORE`（最前）/ `INSERT_AFTER`（id 为空，最后）。
> - **UPDATE/DELETE 强制前置条件**：执行 `UPDATE` 或 `DELETE` 操作前，**必须**先通过 `find` 或 `read` 获取文档数据并从中选择具体锚点 Block ID，禁止跳过此步骤。
> - `find` 返回结果后应展示给用户确认锚点位置，而非直接使用第一个结果。
> - 所有内容块必须挂载在 `Page` 下，完整组件列表详见 `mdx_references.md`。

---
