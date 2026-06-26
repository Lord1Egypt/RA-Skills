# API 端点详情

后端服务地址：`http://124.221.10.61/api/v1/`

## 全部 MCP 工具列表

| # | 工具 | 免费 | 用途 |
|---|------|:----:|------|
| 1 | `check_environment()` | ✅ | 首次使用先调！检查服务是否运行 |
| 2 | `recommend_templates(task)` | ✅ | 智能推荐模板 |
| 3 | `search_templates(q, category?)` | ✅ | 按关键词精确搜索 |
| 4 | `list_categories()` | ✅ | 获取所有分类 |
| 5 | `get_template_detail(id)` | ✅ | 单个模板详细信息 |
| 6 | `preview_template(id, format?)` | ✅ | 缩略图预览 |
| 7 | **`user_upload_template(file)`** | ✅ **免费3次** | 用户上传自有模板 → 自动分析结构 |
| 8 | **`user_fill_document(session_id, content)`** | ✅ **免费3次** | 填充内容到模板（文本/表格/图片） |
| 9 | `create_api_key(name)` | ✅ | 创建 API Key |
| 10 | `key_balance()` | ✅ | 查余额 + 剩余免费次数 |
| 11 | `generate_document(template_id, content)` | ¥0.99 | 用内置模板+内容一键生成文档/PPT |
| 12 | `download_template(template_id)` | ¥0.99 | 下载内置模板文件 |
| 13 | `pay_for_download(template_id)` | 💵 | 创建 ¥0.99 支付订单 |
| 14 | `test_pay_order(order_id)` | 🎲 | 模拟支付（本地测试用） |

> **¥0.99 一次性买断后，以上所有"付费"工具全部变为免费，不限次数。**

---

## 场景一：自有模板 API

### user_upload_template（上传模板）

- 对应 `POST /api/v1/user/upload`
- HTTP multipart/form-data 上传，字段名 `file`
- 文件格式：.docx（推荐）/ .doc

返回格式说明（**AI 需逐字段解析**）：

```json
{
  "ok": true,
  "data": {
    "session_id": "abc123def456",
    "original_name": "毕业论文模板.docx",
    "file_size": 32000,
    "format": "docx",
    "analysis": {
      "total_paragraphs": 85,
      "sections_count": 12,
      "structure": {
        "type": "document",
        "children": [
          {
            "type": "text",
            "position": "封面",
            "label": "{{封面:姓名}}",
            "hint": "请填写此项?"
          },
          {
            "type": "chapter",
            "label": "{{绪论}}",
            "children": [
              {
                "type": "text",
                "label": "研究背景",
                "hint": "请在此章节下撰写内容"
              },
              {
                "type": "chapter",
                "label": "{{子章节1}}",
                "children": []
              }
            ]
          },
          {
            "type": "reference",
            "position": "末尾",
            "label": "{{参考文献}}",
            "hint": "按学术规范列出参考文献"
          }
        ]
      },
      "preview": ["文档前几行预览..."]
    }
  }
}
```

**解析要点：**
- `session_id` → 后续填充必须使用此 ID，**10 分钟过期**
- `structure.children` → 树形结构，顶级节点为封面字段 / 章节 / 参考文献
- `type = "chapter"` → 有 children 数组，代表子章节
- `type = "text"` → 需要用户填写的内容字段
- `type = "reference"` → 参考文献列表
- `label` 包含 `{{xxx}}` → 模板中标记的占位符字段名，填充时必须用这个完整字符串作为 key
- `label` 不含 `{{}}` → 系统自动分析的普通文本段落

### user_fill_document（填充内容）

对应 `POST /api/v1/user/fill`

```json
{
  "session_id": "abc123def456",
  "content": { ... },
  "filename": "毕业论文_李四",
  "format": "docx",
  "formatting": { ... }
}
```

---

## 场景二：内置模板库 API

### recommend_templates（智能推荐）

调 `recommend_templates(task=用户的需求)` — 传用户原始需求文本。

### search_templates（搜索）

调 `search_templates(q, category?)` — 按关键词精确搜索。

---

## content 数据结构

### 数据类型1：纯文本替换

```json
{
  "{{封面:姓名}}": "李四",
  "{{封面:学号}}": "123456",
  "{{内容:研究背景}}": "随着信息技术的发展..."
}
```

**规则：**
- key 必须与 analysis 中 label 的 `{{}}` 内容完全匹配（包括大小写和空格）
- value 为普通字符串 → 直接替换模板中对应位置
- 如果 label 不含 `{{}}`，可用 label 整体作为 key 进行模糊匹配

### 数据类型2：插入表格

```json
{
  "{{TABLE:实验数据}}": {
    "type": "table",
    "headers": ["年份", "样本量", "有效率"],
    "rows": [
      ["2020", "100", "85%"],
      ["2021", "150", "90%"]
    ],
    "caption": "表1 实验数据统计"
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `type` | string | ✅ | 固定为 `"table"` |
| `headers` | string[] | ✅ | 表头列名数组 |
| `rows` | string[][] | ✅ | 数据行数组，每行长度需与 headers 一致 |
| `caption` | string | 可选 | 表格标题（居中，斜体） |

### 数据类型3：插入图片

```json
{
  "{{IMAGE:实验流程图}}": {
    "type": "image",
    "path": "用户提供的图片本地路径",
    "width": 500,
    "caption": "图1 实验流程图"
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `type` | string | ✅ | 固定为 `"image"` |
| `path` | string | ✅ | 图片的**相对路径**（相对 session 临时目录） |
| `width` | number | 可选 | 图片宽度（像素），默认 400 |
| `caption` | string | 可选 | 图片标题 |

> ⚠️ 安全限制：禁止使用绝对路径，禁止 `..` 路径遍历。

### 混合使用（最常见）

```json
{
  "{{封面:姓名}}": "李四",
  "{{TABLE:实验数据}}": {
    "type": "table",
    "headers": ["年份", "样本量"],
    "rows": [["2020", "100"]],
    "caption": "表1"
  },
  "{{IMAGE:校徽}}": {
    "type": "image",
    "path": "校徽.png",
    "width": 120,
    "caption": ""
  }
}
```

---

## 导出格式控制

| 场景 | format 参数 |
|------|:-----------:|
| 用户没提格式 | 不传 → 默认 .docx |
| 用户要 PDF | `"format": "pdf"` |
| 用户说"打印"/"提交学校" | 先问要不要 PDF |
| 默认电子版 | .docx（Word 可编辑） |

> PDF 导出依赖本机安装的 Word（通过 COM 调用），若无 Word 会回退为 .docx。

---

## 排版格式控制（formatting 参数）

当用户有排版要求时传入：

```json
{
  "formatting": {
    "page_setup": {
      "size": "A4",
      "margin_top": "2.54cm",
      "margin_bottom": "2.54cm",
      "margin_left": "3.17cm",
      "margin_right": "3.17cm"
    },
    "body_text": {
      "font": "宋体",
      "size": "12pt",
      "line_spacing": "1.5",
      "first_line_indent": "2字符",
      "alignment": "justify"
    },
    "headings": {
      "level1": {
        "font": "黑体", "size": "16pt", "bold": true,
        "left_indent": "2字符"
      },
      "level2": {
        "font": "黑体", "size": "14pt", "bold": true
      }
    },
    "page_number": {
      "position": "bottom_center",
      "format": "arabic",
      "start_at": 1
    }
  }
}
```

---

## 缩略图展示规则

1. 调 `preview_template(template_id)` 获取预览图 URL
2. 通过 MEDIA 将图片发到对话框供用户查看
3. 同时提供预览图 URL（用户可以点击查看）

---

## {{}} 占位符全覆盖规则

**填充前必须做到：content 字典的 key 覆盖模板中每一个 `{{}}` 占位符。**

为什么必须全部覆盖：填充接口使用字符串替换，没被替换的 `{{}}` 会原样留在文档中。

**操作步骤：**
1. 解析 analysis 返回的结构树，提取所有的 label（包括 `{{}}` 格式的占位符）
2. 遍历每个占位符，对每个 `{{}}` 生成对应的内容
3. 把所有映射放入 content 字典再调接口

**模板中 `{{子章节X}}` 是通用占位符，按先后顺序分配章节号：**

```
模板中的占位符顺序          预期替换内容
{{子章节1、}}       → "一、绪论"
{{子章节1.}}        → "1.1 研究背景与意义"
{{子章节1.}}        → "1.2 国内外研究现状"  (第2个出现→递增)
{{子章节1.}}        → "1.3 研究内容"
{{子章节2、}}       → "二、相关技术介绍"
{{子章节2.}}        → "2.1 Spring Boot"
...
```

> 填充接口的替换是**逐段精确匹配**的（`if key in p.text`），所以相同的 `{{子章节1.}}` 存在多次也没问题。

**如果 AI 需要自动生成论文全部内容：**
1. 确定用户专业、选题方向
2. 推荐合适的论文结构（6-8章）
3. 针对模板中每一个 `{{}}` 占位符生成对应内容
4. 构建完整的 content 字典
5. 调用 user_fill_document 并验证返回文件中还有没有被替换的 `{{}}`

---

# 本地模板创建（本地 python-docx）

当用户**没有现成模板**但能**描述想要的样式**时，使用此能力从零创建 .docx 文件。

## 创建工具

scripts/create_template.py — 本地 Python 脚本，根据 JSON 参数文件生成 .docx。

## 支持的自定义项

| 项目 | 说明 |
|------|------|
| 纸张大小 | A4 / B5 / 自定义 mm |
| 页边距 | 上下左右精确 cm |
| 页眉文字 | 任意文本，居中 |
| 页脚页码 | 自动页码（- N - 格式） |
| 封面内容 | 图片 + 文本序列，居左/中/右 |
| 图片插入 | 指定路径 + 宽度（cm），等比缩放 |
| 标题字号字体 | 一级黑体16pt、二级黑体14pt 等 |
| 正文样式 | 字体/字号/行距/首行缩进/对齐 |
| 表格 | 空表格框架，留待填充 |
| 目录 | 自动 TOC 域代码 |
| {{}} 占位符 | 可任意插入，后续复用 |
| 多章节结构 | 绪论、正文各章、参考文献 |

## 调用方式

```bash
python scripts/create_template.py params.json output.docx
```

## 参数格式示例

```json
{
  "page": { "size": "A4", "margin_top_cm": 2.54, "margin_left_cm": 3.17 },
  "header": "XX大学毕业论文",
  "cover": [
    {"type": "image", "path": "C:/logo.png", "width_cm": 3, "align": "left"},
    {"type": "text", "content": "毕业论文", "font": "黑体", "size_pt": 22, "bold": true, "align": "center"},
    {"type": "text", "content": "{{论文题目}}", "font": "宋体", "size_pt": 16, "align": "center"}
  ],
  "body": { "font": "宋体", "size_pt": 12, "first_line_indent_cm": 0.74 },
  "headings": [{"level": 1, "font": "黑体", "size_pt": 16, "bold": true}],
  "placeholders": [
    {"text": "{{内容:研究背景}}", "style": "body"},
    {"text": "{{TABLE:实验数据}}", "style": "body"}
  ]
}
```

## 生成后处理

生成的 .docx 包含 {{}} 占位符，可继续通过 user_fill_document() 填充内容（走自有模板场景）。
