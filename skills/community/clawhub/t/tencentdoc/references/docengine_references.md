# DOC 编辑引擎 API 参考

本文件包含腾讯文档 DOC 编辑引擎（docengine）的所有工具 API 说明。这些工具专用于 Word 文档的编辑操作，包括文本插入、替换、查找、段落设置、文本属性修改、任务插入、图片插入、分页符和表格插入等。

> ⚠️ **注意**：本文档中的工具仅适用于 **Word 文档（doc_type: word）** 类型，不适用于智能文档（smartcanvas）等其他类型。

---

## 服务信息

| 项目 | 说明 |
|------|------|
| 服务名 | `tencent-docengine` |
| API 地址 | `https://docs.qq.com/api/v6/doc/mcp` |
| 调用方式 | `mcporter call tencent-docengine <工具名>` |
| Token | 与 tencent-docs **共用同一个 Token**，完成 tencent-docs 授权（`auth.md`）后自动配置，无需单独鉴权 |
| 文档类型 | 仅支持 Word 文档类型 |

> ⚠️ **推荐优先使用 `file_url`（文档链接）而非 `file_id` 来标识文档**，用户通常直接提供文档链接，使用更便捷。
>
> 编辑前推荐先调用 `get_outline` 获取文档大纲结构，了解各标题和正文的可操作位置。
>
> 当用户要求「在文档开头插入」时，需向用户确认是在「文档标题之前」（使用 `HEADING_LEVEL_TITLE` 的 `title_start`）还是「正文开头/标题之后」（使用 `HEADING_LEVEL_TITLE` 的 `content_start`）插入，未明确时应主动询问。

---

## 通用说明

### 文档标识

所有 docengine 工具都支持两种文档标识方式（二选一）：
- `file_url` (string): **⭐ 推荐** 腾讯文档的文档链接（如 `https://docs.qq.com/doc/xxxxxxxx`），直接使用用户提供的文档链接即可
- `file_id` (string): 文档唯一标识符

> 💡 **推荐优先使用 `file_url`**：用户通常会直接提供文档链接，使用 `file_url` 无需额外解析 `file_id`，更加便捷。

### 响应结构

编辑类 API 返回：
- `base_version` (int64): 文档的基准版本号
- `new_version` (int64): 编辑后的文档新版本号
- `err_msg` (string): 错误信息（成功时为空）
- `trace_id` (string): 调用链追踪 ID

查询类 API（如 find）返回：
- `read_result.version` (int64): 文档当前版本号
- `read_result.trace_id` (string): 调用链追踪 ID

---

## 工具列表

| 工具名称 | 功能说明 |
|---------|---------|
| find | 查找文本所在位置，返回匹配位置和上下文 |
| insert_text | 在指定位置插入文本 |
| insert_paragraph | 在指定位置插入段落，支持设置标题级别、编号类别和编号级别 |
| replace_text | 替换指定范围内的文本 |
| find_and_replace_text | 查找并替换文档中所有匹配的文本 |
| update_text_property | 更新指定范围内文本的属性（加粗、斜体、下划线、删除线、颜色等） |
| insert_task | 在指定位置插入一个或多个任务，支持设置任务状态和内容文本 |
| insert_image | 在指定位置插入图片 |
| insert_page_break | 在指定位置插入分页符 |
| insert_table | 在指定位置插入表格 |
| insert_comment | 在指定范围插入批注 |
| replace_image | 替换文档中的图片 |
| get_last_operable_pos | 获取文档末尾最后一个可操作位置的索引及前面内容 |
| get_outline | 获取文档大纲结构（标题层级树），包含各标题和正文的可操作起止位置 |
| resolve_document_structure | 获取文档完整结构树，返回所有块级元素（段落、标题、表格、文本框、代码块等）的层级结构和精确位置，可用于定位表格指定行列、文本框内部等复杂位置 |

---

## 工具详细说明

## 1. find

### 功能说明
在 Word 文档中查找指定文本，返回所有匹配位置及其上下文。如果用户需要替换文本，建议先使用 `find` 查找文本所在的各处位置，让用户确认要替换哪个位置后，再调用 `replace_text` 进行精确替换。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "text": "要查找的文本"
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `text` (string, 必填): 要查找的文本内容

### 返回值说明
```json
{
  "text_and_locations": [
    {
      "range": { "begin": 10, "end": 15 },
      "related_text": "...上下文文本..."
    }
  ],
  "read_result": {
    "version": 1,
    "trace_id": "trace_1234567890"
  }
}
```
- `text_and_locations` (array): 匹配到的文本位置列表
  - `range.begin` (uint32): 匹配文本的起始位置
  - `range.end` (uint32): 匹配文本的结束位置
  - `related_text` (string): 匹配位置的上下文文本
- `read_result.version` (int64): 当前文档版本号
- `read_result.trace_id` (string): 调用相关的可追踪链路id

### 推荐使用流程
1. 调用 `find` 查找目标文本，获取所有匹配位置
2. 将匹配结果展示给用户，让用户选择要替换的位置
3. 根据用户选择，调用 `replace_text` 传入对应的 `range` 进行替换

---

## 2. insert_text

### 功能说明
在 Word 文档的指定位置插入文本。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "text": "要插入的文本内容",
  "index": 0
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `text` (string, 必填): 要插入的文本内容
- `index` (integer, 必填): 插入位置的索引，从 0 开始，请确认好索引后再操作

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 3. insert_paragraph

### 功能说明
在 Word 文档的指定位置插入段落。支持设置标题级别、编号类别和编号级别，可用于创建标题、有序/无序列表等。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "idx": 0,
  "level": "1",
  "type": "1",
  "numbering_lvl": "1",
  "space_cnt": 0
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `idx` (integer, 必填): 插入位置的索引，从 0 开始
- `level` (string, 可选): 标题级别，取值：
  - `"0"`: 未指定（保持原样）
  - `"1"` ~ `"9"`: 一级标题 ~ 九级标题
  - `"10"`: 正文（无标题）
  - `"11"`: 标题
  - `"12"`: 副标题
- `type` (string, 可选): 编号类别，取值：
  - `"0"`: 未知/无编号
  - `"1"`: 圆点列表（无序列表）
  - `"2"`: 数字编号列表（有序列表）
- `numbering_lvl` (string, 可选): 编号级别，取值与 `level` 相同（`"1"` ~ `"9"`）
- `space_cnt` (integer, 可选): 空格数量

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 4. replace_text

### 功能说明
替换 Word 文档中指定范围内的文本为新文本。建议先使用 `find` 工具查找文本位置，让用户确认后再调用此工具进行精确替换。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "text": "替换后的文本内容",
  "ranges": [{"start_index": 0, "end_index": 5}]
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `text` (string, 必填): 替换后的文本内容
- `ranges` (array, 必填): 需要替换的文本范围列表，每个范围包含 `start_index` 和 `end_index`

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 5. find_and_replace_text

### 功能说明
在 Word 文档中查找所有匹配的文本并直接替换为新文本。与 `find` + `replace_text` 的组合不同，此工具会直接替换所有匹配项，用户无法选择性地替换某个特定位置。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "old_text": "要查找的文本",
  "new_text": "替换后的文本"
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `old_text` (string, 必填): 要查找的原始文本
- `new_text` (string, 必填): 替换后的新文本

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 6. update_text_property

### 功能说明
更新 Word 文档中指定范围内文本的属性，支持设置加粗、斜体、下划线、删除线、小型大写、字体颜色、背景颜色等。建议先使用 `find` 工具查找文本位置，获取 range 后再调用此工具修改文本属性。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "ranges": [{"begin": 0, "end": 5}],
  "property": {
    "bold": true,
    "color": "#FF0000"
  }
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `ranges` (array, 必填): 需要更新属性的文本范围列表，每个范围包含 `begin` 和 `end`
- `property` (object, 必填): 要设置的文本属性，支持以下字段：
  - `bold` (bool, 可选): 是否加粗
  - `italic` (bool, 可选): 是否斜体
  - `underline` (bool, 可选): 是否下划线
  - `strikethrough` (bool, 可选): 是否删除线
  - `small_caps` (bool, 可选): 是否小型大写
  - `color` (string, 可选): 字体颜色，如 "#FF0000"
  - `background_color` (string, 可选): 背景颜色，如 "#FFFF00"

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 7. insert_task

### 功能说明
在 Word 文档的指定位置插入一个或多个任务（待办事项）。每个任务支持设置任务状态（待办/已完成）和任务内容文本。

### 调用示例

**插入单个任务：**
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "idx": 0,
  "tasks": [
    {
      "state": 1,
      "content": "完成需求文档编写"
    }
  ]
}
```

**插入多个任务：**
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "idx": 5,
  "tasks": [
    {
      "state": 1,
      "content": "完成需求文档编写"
    },
    {
      "state": 2,
      "content": "完成接口设计"
    },
    {
      "state": 1,
      "content": "编写单元测试"
    }
  ]
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `idx` (integer, 必填): 插入位置的索引，从 0 开始
- `tasks` (array, 必填): 任务列表，支持一次插入多个任务，每个任务包含：
  - `state` (integer, 必填): 任务状态枚举值，不允许传递0值，取值：
    - `1`: 待办（未完成）
    - `2`: 已完成
  - `content` (string, 必填): 任务内容文本

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 8. insert_image

### 功能说明
在 Word 文档的指定位置插入图片。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "image_url": "https://example.com/image.png",
  "index": 0,
  "width": 400,
  "height": 300
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `image_url` (string, 必填): 图片的 URL 地址
- `index` (integer, 必填): 插入位置的索引，从 0 开始
- `width` (integer, 可选): 图片宽度（像素）
- `height` (integer, 可选): 图片高度（像素）
- `addon_source` (string, 可选): 插件来源类型
- `addon_id` (string, 可选): 插件 ID
- `anchor_id` (string, 可选): 锚点 ID
- `extra_data` (string, 可选): 额外数据

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 9. insert_page_break

### 功能说明
在 Word 文档的指定位置插入分页符。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "index": 10
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `index` (integer, 必填): 插入位置的索引，从 0 开始

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 10. insert_table

### 功能说明
在 Word 文档的指定位置插入表格。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "index": 0,
  "rows": 3,
  "cols": 4
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `index` (integer, 必填): 插入位置的索引，从 0 开始
- `rows` (integer, 必填): 表格行数
- `cols` (integer, 必填): 表格列数

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 11. insert_comment

### 功能说明
在 Word 文档的指定范围内插入批注（评论）。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "text": "这里需要修改措辞",
  "range": {"begin": 5, "end": 15}
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `text` (string, 必填): 批注内容
- `range` (object, 必填): 批注关联的文本范围，包含 `begin` 和 `end`
- `ref_id` (string, 可选): 评论ID，用于回复已有批注

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 12. replace_image

### 功能说明
替换 Word 文档中的图片。可以通过旧图片的 URL 或 ID 定位要替换的图片，并指定新图片。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx",
  "idx": 0,
  "source": 1,
  "old_url": "https://example.com/old_image.png",
  "new_url": "https://example.com/new_image.png"
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `idx` (integer, 必填): 图片位置索引
- `source` (integer, 必填): 图片来源类型，0-未知，1-链接来源，2-附件来源
- `old_url` (string, 可选): 旧图片的 URL，与 `old_id` 二选一
- `old_id` (string, 可选): 旧图片的 ID，与 `old_url` 二选一
- `new_url` (string, 可选): 新图片的 URL 地址，与 `content` 二选一
- `content` (string, 可选): 新图片的 base64 内容，与 `new_url` 二选一

### 返回值说明
```json
{
  "base_version": 1,
  "new_version": 2,
  "trace_id": "trace_1234567890",
  "err_msg": ""
}
```

---

## 13. get_last_operable_pos

### 功能说明
获取 Word 文档正文（main story）最后一个可操作位置的索引，以及该位置前面最多 10 个字符的内容。在需要向文档末尾追加内容时，可先调用此接口获取末尾可操作位置，再使用 `insert_text`/`insert_image` 等接口在该位置插入内容。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx"
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一

### 返回值说明
```json
{
  "position": 100,
  "preceding_text": "...前面内容...",
  "version": 1
}
```
- `position` (int64): 最后一个可操作位置的索引
- `preceding_text` (string): 该位置前面最多 10 个字符的内容
- `version` (int64): 当前文档版本号

---

## 14. get_outline

### 功能说明
获取 Word 文档的完整大纲结构（树形），返回文档标题、各级标题及其下正文的可操作位置范围。可用于：
- 了解文档整体结构和层级关系
- 获取指定标题或正文区域的精确位置（`title_start`/`title_end`、`content_start`/`content_end`），以便在对应位置插入或替换内容
- 在操作前先掌握文档大纲，避免盲目使用 `find` 查找

> ⚠️ **关于「在文档开头插入」的位置说明**：文档大纲的根节点通常是 `HEADING_LEVEL_TITLE`（文档标题），其 `title_start` 表示文档标题之前的位置，`content_start` 表示标题之后、正文开头的位置。当用户要求"在文档开头插入内容"时，需要向用户确认具体含义：
> - **在文档标题之前插入**：使用 `HEADING_LEVEL_TITLE` 节点的 `title_start`
> - **在正文开头插入（标题之后）**：使用 `HEADING_LEVEL_TITLE` 节点的 `content_start`
> 
> 如果用户未明确说明，应主动询问确认。

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx"
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一

### 返回值说明
```json
{
  "outlines": [
    {
      "title": "文档标题",
      "level": "HEADING_LEVEL_TITLE",
      "title_start": 0,
      "title_end": 5,
      "content_start": 6,
      "content_end": 100,
      "children": [
        {
          "title": "第一章 概述",
          "level": "HEADING_LEVEL_1",
          "title_start": 6,
          "title_end": 12,
          "content_start": 13,
          "content_end": 50,
          "children": [
            {
              "title": "1.1 背景",
              "level": "HEADING_LEVEL_2",
              "title_start": 13,
              "title_end": 18,
              "content_start": 19,
              "content_end": 50,
              "children": []
            }
          ]
        }
      ]
    }
  ],
  "version": 1
}
```

- `outlines` (array): 大纲根节点列表（树形结构），每个节点包含：
  - `title` (string): 标题文本内容
  - `level` (string): 标题级别，取值说明：
    - `HEADING_LEVEL_TITLE` (11): 文档标题
    - `HEADING_LEVEL_1` ~ `HEADING_LEVEL_9` (1~9): 一级标题 ~ 九级标题
    - `HEADING_LEVEL_BODY` (10): 正文（无标题）
  - `title_start` (int64): 标题可操作的起始位置（可在此位置前插入内容）
  - `title_end` (int64): 标题可操作的结束位置
  - `content_start` (int64): 该标题下正文可操作的起始位置（在标题下方插入内容时使用）
  - `content_end` (int64): 该标题下正文可操作的结束位置（在正文末尾追加内容时使用）
  - `children` (array): 子目录项列表（递归结构，构成树形大纲）
- `version` (int64): 当前文档版本号

---

## 15. resolve_document_structure

### 功能说明
获取 Word 文档的完整结构树（DOC），返回 main story 下所有块级元素的层级结构和位置信息。与 `get_outline` 只返回标题层级不同，此接口返回**所有**块级元素，包括：
- **Paragraph**：普通文本段落
- **Heading**：标题段落（含级别）
- **Table**：表格（含每行每列的起止位置）
- **TextBox**：文本框（含内部段落的起止位置）
- **CodeBlock**：代码块（含内部段落的起止位置）

适用场景：
- 需要在**表格指定行列**插入或修改文本（通过 `table_rows[row].cells[col].end_index` 定位单元格末尾）
- 需要在**文本框内部**插入内容（通过 `children` 中的段落位置定位）
- 需要了解文档完整布局后再决定操作位置
- 需要精确获取某个段落、代码块的起止范围

### 调用示例
```json
{
  "file_url": "https://docs.qq.com/doc/xxxxxxxx"
}
```

### 参数说明
- `file_url` (string, 推荐): 腾讯文档的文档链接，与 `file_id` 二选一，**推荐优先使用**
- `file_id` (string, 可选): 文档唯一标识符，与 `file_url` 二选一
- `include_heading` (bool, 可选): 是否将标题也作为独立节点列出，默认 false（标题单独归类为 Heading 类型，不计入普通段落序号）

### 返回值说明
```json
{
  "nodes": [
    {
      "type": "Heading",
      "start_index": 0,
      "end_index": 6,
      "text_preview": "文档标题",
      "heading_level": 1,
      "logical_index": 1,
      "table_rows": [],
      "children": []
    },
    {
      "type": "Paragraph",
      "start_index": 7,
      "end_index": 20,
      "text_preview": "这是第一段正文内容",
      "heading_level": 0,
      "logical_index": 2,
      "table_rows": [],
      "children": []
    },
    {
      "type": "Table",
      "start_index": 21,
      "end_index": 60,
      "text_preview": "",
      "heading_level": 0,
      "logical_index": 3,
      "table_rows": [
        {
          "row": 1,
          "cells": [
            { "row": 1, "col": 1, "start_index": 22, "end_index": 30, "text_preview": "单元格内容" },
            { "row": 1, "col": 2, "start_index": 31, "end_index": 38, "text_preview": "" }
          ]
        },
        {
          "row": 2,
          "cells": [
            { "row": 2, "col": 1, "start_index": 40, "end_index": 48, "text_preview": "" },
            { "row": 2, "col": 2, "start_index": 49, "end_index": 57, "text_preview": "" }
          ]
        }
      ],
      "children": []
    },
    {
      "type": "TextBox",
      "start_index": 61,
      "end_index": 80,
      "text_preview": "文本框内容",
      "heading_level": 0,
      "logical_index": 4,
      "table_rows": [],
      "children": [
        {
          "type": "Paragraph",
          "start_index": 62,
          "end_index": 79,
          "text_preview": "文本框内容",
          "heading_level": 0,
          "logical_index": 1,
          "table_rows": [],
          "children": []
        }
      ]
    },
    {
      "type": "CodeBlock",
      "start_index": 81,
      "end_index": 110,
      "text_preview": "console.log('hello')",
      "heading_level": 0,
      "logical_index": 5,
      "table_rows": [],
      "children": [
        {
          "type": "Paragraph",
          "start_index": 82,
          "end_index": 109,
          "text_preview": "console.log('hello')",
          "heading_level": 0,
          "logical_index": 1,
          "table_rows": [],
          "children": []
        }
      ]
    }
  ],
  "version": 5,
  "total_paragraphs": 3,
  "total_headings": 1,
  "total_tables": 1
}
```

- `nodes` (array): 顶层块级节点列表（main story 直接子节点），按文档顺序排列，每个节点包含：
  - `type` (string): 节点类型，取值：`Paragraph`、`Heading`、`Table`、`TextBox`、`CodeBlock`、`HighlightBlock`
  - `start_index` (uint32): 节点起始位置（inclusive）
  - `end_index` (uint32): 节点结束位置（在此处插入可追加到节点末尾）
  - `text_preview` (string): 文本预览，最多 50 字符，仅 Paragraph/Heading 有值
  - `heading_level` (int32): 标题级别 1-9，仅 Heading 类型有值，其余为 0
  - `logical_index` (int32): 在同级中的逻辑序号（从 1 开始）
  - `table_rows` (array): 仅 Table 类型有值，包含行列结构：
    - `row` (int32): 行号（从 1 开始）
    - `cells` (array): 该行所有单元格：
      - `row` (int32): 行号（从 1 开始）
      - `col` (int32): 列号（从 1 开始）
      - `start_index` (uint32): 单元格起始位置
      - `end_index` (uint32): 单元格结束位置（在此处插入可追加到单元格末尾）
      - `text_preview` (string): 单元格文本预览，最多 30 字符
  - `children` (array): 子节点列表，TextBox/CodeBlock 内部的段落等
- `version` (int64): 当前文档版本号
- `total_paragraphs` (int32): 正文段落总数（不含标题）
- `total_headings` (int32): 标题总数
- `total_tables` (int32): 表格总数

---

## 典型工作流示例

### 编辑已有 Word 文档

```
1. 调用 get_outline 获取文档大纲结构，了解文档的标题层级和各区域的可操作位置
   （如需精确定位表格行列、文本框内部等，改用 resolve_document_structure）
2. 根据大纲定位目标区域，或调用 find 查找具体文本位置
3. 按需调用工具进行编辑：
   - 插入文本：insert_text
   - 插入段落：insert_paragraph
   - 替换文本：replace_text
   - 全文替换：find_and_replace_text
   - 修改文本样式：update_text_property
   - 插入任务：insert_task
   - 插入图片：insert_image
   - 替换图片：replace_image
   - 插入分页符：insert_page_break
   - 插入表格：insert_table
   - 插入批注：insert_comment
   - 获取文档大纲：get_outline
   - 获取完整结构树：resolve_document_structure
```

### 查找并替换文本（精确替换）

```
1. 调用 find 查找目标文本，获取所有匹配位置
2. 将匹配结果展示给用户，让用户选择要替换的位置
3. 调用 replace_text 传入对应的 range 进行精确替换
```

### 查找并替换文本（全部替换）

```
1. 直接调用 find_and_replace_text，一次性替换所有匹配项
```

### 格式化文本

```
1. 调用 find 查找目标文本，获取文本的 range
2. 调用 update_text_property 设置文本属性（加粗、颜色等）
```

### 向文档末尾追加内容

```
1. 调用 get_last_operable_pos 获取文档末尾可操作位置
2. 使用返回的 position 作为 index，调用 insert_text / insert_image / insert_table 等工具追加内容
```

### 在指定标题下插入内容

```
1. 调用 get_outline 获取文档大纲，找到目标标题节点
2. 使用节点的 content_start 作为插入位置（在标题下方开头插入）
   或使用 content_end 作为插入位置（在标题下方正文末尾追加）
3. 调用 insert_text / insert_paragraph / insert_image 等工具在对应位置插入内容
```

### 在文档开头插入内容

```
1. 调用 get_outline 获取文档大纲
2. 明确用户意图——是要在「文档标题前」还是「正文开头」插入：
   - 文档标题前：使用 HEADING_LEVEL_TITLE 节点的 title_start 作为插入位置
   - 正文开头（标题之后）：使用 HEADING_LEVEL_TITLE 节点的 content_start 作为插入位置
3. 如果用户未明确说明，应主动询问用户确认具体插入位置
4. 确认位置后，调用 insert_text / insert_paragraph 等工具在对应位置插入内容
```

### 在表格指定行列插入文本

```
1. 调用 resolve_document_structure 获取文档完整结构树
2. 在返回的 nodes 中找到目标 Table 节点
3. 通过 table_rows[row-1].cells[col-1].end_index 获取目标单元格的末尾位置
4. 调用 insert_text，将 index 设为该 end_index，即可在指定单元格末尾插入文本
```

### 在文本框内部插入内容

```
1. 调用 resolve_document_structure 获取文档完整结构树
2. 在返回的 nodes 中找到目标 TextBox 节点
3. 通过 children 中的段落节点获取内部精确位置
4. 调用 insert_text / insert_paragraph 在对应位置插入内容
```

### 为文本添加批注

```
1. 调用 find 查找目标文本，获取文本的 range（begin/end）
2. 调用 insert_comment 传入 range 和批注内容
```

### 替换文档中的图片

```
1. 调用 replace_image 传入旧图片的 URL 或 ID，以及新图片的 URL 或 base64 内容
```

---

## 注意事项

- 仅支持 Word 文档类型（doc_type: word）
- `index` / `idx` 参数表示插入位置，从 0 开始计数
- 操作前需确保拥有文档的写入权限
- `replace_text` 的 `ranges` 参数中 `start_index` 和 `end_index` 必须在文档有效范围内
- 替换文本的推荐流程：先调用 `find` 查找定位，让用户确认后再用 `replace_text` 精确替换；如果需要全部替换可直接使用 `find_and_replace_text`
- `file_id` 和 `file_url` 二选一，**推荐优先使用 `file_url`**（直接传入文档链接更便捷），两者都传时优先使用 `file_id`
- `get_last_operable_pos` 返回的 `position` 即为文档末尾可安全插入内容的位置
- `get_outline` 返回树形大纲结构，每个节点的 `content_start`/`content_end` 表示该标题下正文区域的可操作范围，可直接用作 `insert_text` 等工具的 `index` 参数
- **「在文档开头插入」需明确位置**：用户要求在文档开头插入内容时，应先通过 `get_outline` 获取大纲，区分「文档标题前」（`HEADING_LEVEL_TITLE` 的 `title_start`）和「正文开头」（`HEADING_LEVEL_TITLE` 的 `content_start`），并向用户确认具体插入位置
- `resolve_document_structure` 返回所有块级元素的完整结构树，`table_rows[row].cells[col].end_index` 即为对应单元格末尾可插入位置；TextBox/CodeBlock 的内部段落通过 `children` 字段获取；`logical_index` 表示节点在同级中的顺序（从 1 开始）
- `insert_comment` 的 `range` 必须在文档有效范围内，建议先用 `find` 获取精确范围
- `replace_image` 需要通过 `old_url` 或 `old_id` 定位旧图片，新图片通过 `new_url` 或 `content`（base64）指定
