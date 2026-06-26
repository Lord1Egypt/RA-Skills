---
name: docx
description: 创建或编辑 Word (.docx) 文档。当用户要求生成、导出、下载 Word 文档，或对现有 .docx 编辑时使用本技能。当最终交付物是"文档"且用户未指定格式时（如"生成文档"、"写一份文档"、"帮我做个文档"），默认使用本技能生成 .docx。仅适用于最终交付物，中间生成物的格式不受此约束。
---

# DOCX 文档创建与编辑

## 何时使用

- **最终交付物**为文档且用户未指定格式时，默认生成 `.docx`
- 用户明确要求生成、导出、下载 Word 文档
- 对现有 `.docx` 做文本替换（正文、页眉、页脚）
- 解包查看 Word XML 结构并重新打包

注意：任务过程中的中间生成物（如临时数据文件、处理脚本等）不需要使用本技能，格式自由选择。

## 何时不要使用

- 批注、回复批注
- 接受修订或保留修订
- 大规模样式重构、复杂目录修复、复杂域代码处理

---

## 快速参考

| 任务             | 推荐方式                             |
| ---------------- | ------------------------------------ |
| 创建新 `.docx`   | 写 HTML → `html2docx()` → 见工作流 A |
| 编辑现有 `.docx` | `edit_docx()` → 见工作流 B           |
| 检查 XML 结构    | `unpack_docx()`                      |
| 重新打包         | `pack_docx()`（默认含校验）          |

---

## 工作流 A：创建新文档

流程分三步：根据内容基调设计视觉风格 → 用 `start_write_file` / `end_write_file` 编写语义化 HTML → 通过 `jupyter_cell_exec`工具 执行转换脚本输出 .docx。

### 第 1 步：分析内容基调，推演视觉风格

在编写 HTML 前，先完成意图识别与风格推演，并将结果直接落实到后续 CSS 中：

- **色板**：根据内容基调设定主标题颜色、正文颜色和弱化文本颜色。轻量级高亮可使用浅色背景。公文、法律声明、严肃通知、学术论文等严肃场景禁止使用彩色，仅使用 `#000000` 和 `#333333`
- **字体**：正式报告优先使用衬线体（宋体、仿宋）；现代文档或技术文档优先使用无衬线体（微软雅黑、黑体）；代码部分使用等宽字体（Consolas）；公文场景禁止使用非衬线字体，默认全用宋体或黑体
- **节奏**：设定符合打印和离线阅读的行高（如 `1.5` 到 `1.8`）、统一段落间距（如 `12pt`）及章节留白

### 第 2 步：用 start_write_file / end_write_file 编写 HTML 文件

> **强制规则：必须使用 `start_write_file` + `end_write_file` 写入 HTML 文件。禁止通过 Python 代码生成 HTML 内容。** HTML 内容应由你直接以文本形式输出，以充分发挥 LLM 的长文本生成能力和排版能力。

1. 调用 `start_write_file(path="<OUTPUT_ROOT>/<文档名>.html")` 开启写作模式
2. 直接以 `<!DOCTYPE html>` 开头输出完整 HTML（禁止使用 ` ```html ` 等 markdown 代码围栏包裹，直接输出原始 HTML 内容）
3. 输出完毕后调用 `end_write_file()` 保存文件

生成 HTML 时，提示词正文按以下约束执行：

- **适用范围**：本规范仅适用于经 `html2docx()` 转为 Word 文档的 HTML 源文件，不适用于其他场景的 HTML 写作
- **角色目标**：根据用户输入指令，生成专门用于转换为 `.docx` 文件的单文件 HTML 源文件，要求结构严谨、内容生动、具备专业美感，并适配 Word 离线阅读场景
- **核心目标**：深入理解用户输入内容的意图、受众和情感基调，量身定制符合 Word 渲染逻辑的视觉呈现方案；排版兼顾信息层级秩序与文档正式感，确保转换为 `.docx` 后仍具备良好阅读体验

_Technical Constraints（Word 渲染限制，必须绝对遵守）：_

- 禁用现代布局：绝对不可使用 Flexbox（`display: flex`）、CSS Grid（`display: grid`）、`float`、`position: absolute`、`position: fixed`；若需左右分栏或复杂对齐，必须且只能使用无边框表格：`<table border="0" cellpadding="0" cellspacing="0">`
- 禁用现代 CSS 特性：绝对不可使用 CSS 变量（`var(--xxx)`）、`calc()`、`clamp()`、伪类（如 `:hover`）、`transition`、媒体查询（`@media`）
- 安全单位与颜色：字体大小和行高必须使用 `pt` 或 `px`，缩进和间距可使用 `em`；颜色值必须使用确定的 Hex 值，如 `#000000`，不可使用 `rgba()` 或 `hsla()`
- 字体声明机制：必须使用标准 CSS 的字体回退机制，并严格遵守“先英文字体，后中文字体”的声明顺序，例如 `font-family: Arial, "Microsoft YaHei", SimSun, sans-serif;`

_语义化重组与内容强化：_

- HTML 必须包含完整 `<!DOCTYPE html><html><head><body>` 结构，且头部必须声明 `<meta charset="UTF-8">`
- 严格按信息层级分配 `h1` 到 `h6`，为 Word 自动目录做好结构化准备
- 在不改变核心原意的前提下优化可读性：长段落中的关键结论可独立抽取并使用 `<blockquote>` 包裹，配合左侧粗边框（`border-left`）和极浅背景色强调；公文等严肃文档不宜使用此样式
- 将松散短句归纳为 `<ol>` 或 `<ul>` 列表，并保持列表项间距适中
- 识别专业术语、代码片段、按键，使用 `<code>` 标签包裹，并设置浅灰背景、圆角及等宽字体

_Word 兼容 CSS 构建：_

- CSS 仅允许写在 `<head>` 的 `<style>` 标签内，尽量使用标签选择器或单层类选择器，避免复杂嵌套
- 如内容基调需要传统中文排版，可使用 `text-indent: 2em;` 处理首行缩进
- 如需使用表格，必须通过 CSS 设置 `border-collapse: collapse;`，并为 `th`、`td` 设置明确边框与内边距，例如 `border: 1px solid #dddddd; padding: 8px;`

_Output Constraints：_

- 必须输出单文件 HTML，包含完整 `<!DOCTYPE html>`、`<head>`（含内联 `<style>`）和 `<body>`
- 严肃文档必须基于事实创作，禁止编造数据、KPI、日期、公司名、电话、邮箱、论文引用等
- 文档内容需根据用户需求和上下文灵活调整文体，禁止生搬硬套和假大空
- 用户如明确限制字数、字体、排版、演讲时长等要求，必须严格遵循

### 第 3 步：执行转换脚本（仅用于 HTML → DOCX 转换）

> **`jupyter_cell_exec`工具 仅用于调用 html2docx 转换脚本**，不要用它来生成或写入 HTML 内容。

通过 **`jupyter_cell_exec`工具** 执行以下代码：

```python
import sys, os
sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'docx', 'scripts'))
from html2docx import html2docx

result = html2docx(input_html="<OUTPUT_ROOT>/report.html", output_docx="<OUTPUT_ROOT>/report.docx")  # 此处填写 OUTPUT_ROOT 完整路径
print(result)
```

> **路径规则：**
>
> - `html2docx()` 的两个参数需要填写 OUTPUT_ROOT 前缀的**完整绝对路径**。

**函数签名：**

| 参数          | 类型  | 说明               |
| ------------- | ----- | ------------------ |
| `input_html`  | `str` | 输入 HTML 文件路径 |
| `output_docx` | `str` | 输出 DOCX 文件路径 |

**返回值：** `dict`，必须检查 `result["ok"]` 判断转换是否成功。

```python
# 成功
{"ok": True, "output_path": "...", "message": "转换成功，文件大小 123.4 KB"}
# 失败
{"ok": False, "output_path": "...", "message": "转换失败: ..."}
```

## 纯 Python 实现（BeautifulSoup + python-docx），无需 Selenium 或 Chrome。

## 工作流 B：编辑现有文档

### 1. 基础文本替换

通过 `edit_docx()` 完成，内部流程：解包 → 合并相邻同样式 run → 文本替换 → 重打包 → 校验。通过 **`jupyter_cell_exec`工具** 执行：

```python
import sys, os
sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'docx', 'scripts'))
from edit_docx import edit_docx

result = edit_docx(
    input_docx="<OUTPUT_ROOT>/input.docx",
    output_docx="<OUTPUT_ROOT>/output.docx",
    replacements=[
        {"from": "旧公司名称", "to": "新公司名称"},
        {"from": "2024年", "to": "2025年"},
    ],
)
print(result)
```

**参数：**

| 参数           | 类型                | 默认值      | 说明                                                                                |
| -------------- | ------------------- | ----------- | ----------------------------------------------------------------------------------- |
| `input_docx`   | `str`               | —           | 输入文件完整路径                                                                    |
| `output_docx`  | `str`               | —           | 输出文件完整路径                                                                    |
| `replacements` | `list[dict]`        | —           | 替换规则列表，每项含 `"from"` 和 `"to"`                                             |
| `parts`        | `list[str] \| None` | `None`      | 要处理的 XML 部件（支持 glob），默认 `document.xml` + `header*.xml` + `footer*.xml` |
| `match_mode`   | `str`               | `"literal"` | `"literal"` 精确匹配 或 `"regex"` 正则匹配                                          |
| `ignore_case`  | `bool`              | `False`     | 是否忽略大小写                                                                      |

**返回值结构：**

```python
{
    "ok": True,                         # 校验是否通过
    "input_path": "...",
    "output_path": "...",
    "match_mode": "literal",
    "ignore_case": False,
    "files_modified": ["word/document.xml"],
    "replacements_applied": [           # 每条规则的命中次数
        {"from": "旧公司名称", "to": "新公司名称", "count": 3},
    ],
    "validation": {"ok": True, "errors": [], "warnings": []},
}
```

**正则替换示例：**

```python
import sys, os
sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'docx', 'scripts'))
from edit_docx import edit_docx

result = edit_docx(
    input_docx="<OUTPUT_ROOT>/input.docx",
    output_docx="<OUTPUT_ROOT>/output.docx",
    replacements=[{"from": r"Q([1-4]) 2024", "to": r"Q\1 2025"}],
    match_mode="regex",
    ignore_case=True,
)
print(result)
```

### 2. 低层 XML 编辑

如果 `edit_docx()` 替换命中数为 0，通常是目标文本被 Word 拆成了多个 XML run。可退回低层工具链手动处理：

```python
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.join(os.getenv('skill_path'), 'docx', 'scripts'))
from office.unpack import unpack_docx
from office.pack import pack_docx

source = Path("<OUTPUT_ROOT>/input.docx")
unpacked = Path("<OUTPUT_ROOT>/input_unpacked")
output = Path("<OUTPUT_ROOT>/output.docx")

unpack_docx(source, unpacked)   # 解包并合并相邻同样式 run
# 用 jupyter_cell_exec工具 读取并修改 unpacked/word/*.xml
pack_docx(unpacked, output)     # 重打包（默认含校验，失败会抛 ValueError）
```

重点文件：

- `word/document.xml`：正文
- `word/header*.xml`：页眉
- `word/footer*.xml`：页脚
- `word/styles.xml`：样式

---

## 编辑规则

- `edit_docx()` 是基础文本替换工具，不负责批注、修订和复杂域代码
- 解包时会合并相邻的同样式 run，提高文本替换命中率
- 对于被 Word 拆成复杂片段的文本，退回 `unpack_docx()` 手动处理
- `pack_docx()` 会自动修复常见的 XML 空白属性和 `durableId` 溢出问题

---

## Troubleshooting

| 问题                                       | 处理方式                                                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------- |
| `FileNotFoundError`                        | 检查路径是否使用了 OUTPUT_ROOT 完整前缀                                       |
| `缺少依赖 beautifulsoup4`                  | `pip install beautifulsoup4`                                                  |
| `replacements_applied` 中某项 `count` 为 0 | 先 `unpack_docx()` 检查目标文本是否被拆成多个 XML run                         |
| `DOCX 验证失败`                            | 检查修改过的 XML 文件是否有语法错误                                           |
| flex/grid 布局错位                         | 转换器将 flex/grid 降级为表格，简化布局结构或改用扁平 HTML                    |
| 输出样式丢失                               | 确认 CSS 选择器命中正确；复杂嵌套选择器可能不被支持，改用类选择器或标签选择器 |
| 中文乱码                                   | 确认 HTML 头部有 `<meta charset="UTF-8">`                                     |

---

## 资源

| 文件                                     | 用途                                    |
| ---------------------------------------- | --------------------------------------- |
| `skills/docx/scripts/html2docx.py`       | HTML → DOCX 转换主入口（`html2docx()`） |
| `skills/docx/scripts/edit_docx.py`       | DOCX 文本替换编辑                       |
| `skills/docx/scripts/office/unpack.py`   | 解包 DOCX 为 XML 目录                   |
| `skills/docx/scripts/office/pack.py`     | 重打包 XML 目录为 DOCX                  |
| `skills/docx/scripts/office/validate.py` | DOCX 结构校验                           |
| `skills/docx/scripts/office/_shared.py`  | 底层 XML 读写与命名空间工具             |
