# 结果包（ZIP）真实结构

> 本文件内容均来自 **2026-09-01 真实线上调用实测**，非官方文档转述。
> 实测样本：英文单页 PDF、2.2MB/15 页英文论文、自制 5 页中文 PDF。

## 1. 文件命名规则

包内所有文件共享一个 **32 位十六进制任务哈希** 前缀：

```
{hash}_md_full.md
{hash}_xml_full.xml
{hash}_ocr_page0.json
{hash}_ocr_page1.json
...
images/imgParseSvr_img_{imgid}_{index}.png
```

`{hash}` 示例：`37fd7158dab05dcfc99e62d2cc13a345-2f7a4da30bbc456c91dd2f1d2cdb9017`
（实际形如 `<32位hex>-<32位hex>`，两段用 `-` 连接）

**注意**：文件名**不含**原文件名，多次解析同一文件会得到不同 hash。靠 hash 无法回溯源文件，需自行记录映射关系。

## 2. 产出文件与 `--result-type` 的对应关系

`--result-type` 是**选择**而非累加，直接决定产出哪些文件：

| result-type | 产出 |
|------------|------|
| `1`（json） | `_ocr_page{N}.json` |
| `2`（md） | `_md_full.md` |
| `3`（xml） | `_xml_full.xml` |
| `9`（三合一） | md + xml + 全部 ocr_page json |

实测：传 `2` 时 ZIP 内只有 `_md_full.md`（外加图片），**不会**附带 json/xml。

## 3. Markdown（`_md_full.md`）

按页用 HTML 注释分隔，`value` 为 **0-based** 页码：

```markdown
<!-- "type": "page-number", "value": 0 -->
#   第 1 页 · 中文测试

腾讯云文字识别多模态解析接口端到端验证文档。页码标记 PAGE-001


<!-- "type": "page-number", "value": 1 -->
##   第 2 页 · 中文测试

本页用于验证中文段落的识别准确率与版面还原效果。页码标记 PAGE-002
```

要点：

- 标题用 `#` / `##` 表示层级，**标题文本前有 3 个空格**（如 `#   第 1 页`）
- 图片以 `<image>` 标签内联，**图片内的文字会被识别并写入标签体**：
  ```markdown
  <image id="p-45" name="" page-numbers="2" border=""
         src="images/imgParseSvr_img_8c454fcd62cb4be985232d3ae2f8ba65_0.png"
         alt="" media_id="">N×\n\nOutput Probabilities\n\nSoftmax...</image>
  ```
- 公式保留 LaTeX 写法，如 `$N = 6$`、`$d_{\text{model}} = 512$`
- XML 特殊字符已转义（`&amp;`）

## 4. XML（`_xml_full.xml`）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<body>
    <toolId>8</toolId>
    <h1 id="p-0" name="  第 1 页 · 中文测试" page-numbers="0"/>
    <p id="p-1" page-numbers="0">腾讯云文字识别多模态解析接口端到端验证文档。页码标记 PAGE-001</p>
    <p id="p-2" page-numbers="0"></p>
    <h2 id="p-3" name="  第 2 页 · 中文测试" page-numbers="1"/>
    ...
</body>
```

- 根元素 `<body>`，首个子元素 `<toolId>`（实测值为 `8`）
- 段落节点 `<p>`、标题节点 `<h1>`/`<h2>`
- `id` 为 `p-{序号}`，**序号在全文档内连续，不按页重置**
- `page-numbers` 为 **0-based** 页码
- 标题节点的文本在 `name` 属性上，元素本身是自闭合的

## 5. 每页 JSON（`_ocr_page{N}.json`）

每页一个独立文件，`N` 从 **0** 开始。

```json
{
  "height": 1684,
  "width": 1191,
  "org_height": 841,
  "org_width": 595,
  "elements": [
    {
      "polygon": {
        "left_bottom": { "x": 77, "y": 99 },
        "left_top":    { "x": 77, "y": 77 },
        "right_bottom":{ "x": 273, "y": 99 },
        "right_top":   { "x": 273, "y": 77 }
      },
      "type": 9,
      "index": 100,
      "level": 1,
      "text_info": { "content": "#  第 1 页 · 中文测试" }
    },
    {
      "polygon": { "...": "..." },
      "type": 2,
      "index": 101,
      "text_info": { "content": "腾讯云文字识别多模态解析接口端到端验证文档。页码标记 PAGE-001" }
    }
  ],
  "parse_mode": 2
}
```

### 顶层字段

| 字段 | 说明 |
|------|------|
| `width` / `height` | **内部处理坐标系**尺寸 |
| `org_width` / `org_height` | 原始页面尺寸 |
| `elements` | 页面元素数组，按阅读顺序排列 |
| `parse_mode` | 解析模式（实测恒为 `2`） |

### ⚠️ 坐标系缩放（易踩坑）

`polygon` 里的坐标基于 **`width`/`height`**，不是原始尺寸。实测：

| 样本 | 原始尺寸 | 处理坐标系 | 缩放倍数 |
|------|---------|-----------|---------|
| 自制中文 PDF（A4 595×841） | 595 × 841 | 1191 × 1684 | **2×** |
| W3C dummy.pdf（1190×1684） | 1190 × 1684 | 1190 × 1684 | **1×** |

服务端会**自适应**把页面短边归一化到约 1190px。
**要把坐标映射回原图，需除以 `width / org_width` 这个比例，不能直接当原图像素用。**

### elements[].type 枚举（实测观测值）

| type | 含义 | 附加字段 |
|------|------|---------|
| `2` | 正文段落 | — |
| `9` | 标题 | `level`（层级，实测 `1`） |

其他 type 值待补充（本轮样本仅含段落与标题，未覆盖表格、图片、页眉页脚）。

### 其他字段

- `index`：元素序号，**跨页不重置**（实测首页从 `100` 起）
- `level`：仅标题元素携带，表示标题层级
- `text_info.content`：文本内容。标题文本会**带上 Markdown 的 `#` 前缀和多余空格**（如 `"#  第 1 页"`），使用时需清洗
- 空段落元素可能**没有** `text_info` 字段（只有 `polygon` + `type` + `index`），解析时要做容错

## 6. 分页与页码（重点）

`--page-range` 入参是 **1-based**，输出索引是 **0-based**：

| 传入 | 返回 page-number | 返回内容 |
|------|----------------|---------|
| `1-1` | `0` | 第 1 页 |
| `2-3` | `1, 2` | 第 2、3 页 |

**输出索引 = 输入页码 − 1**。

## 7. 中文识别质量实测

对自制中文 PDF 的实测结果：

| 字符类型 | 结果 |
|---------|------|
| 简体汉字 | ✅ 准确 |
| 全角标点（，。；：） | ✅ 准确 |
| 阿拉伯数字 | ✅ 准确 |
| 中文大写金额（壹仟贰佰叁拾肆元整） | ✅ 准确 |
| 中英文混排 | ✅ 准确 |
| **间隔号 `·`（U+00B7）** | ❌ **被替换为 U+FFFD `�`** |

**结论**：中文正文、发票要素、合同主体等场景下识别质量可靠；标题中的装饰性特殊符号存在丢失风险，下游处理建议对 `\ufffd` 做兜底替换。
