---
name: med-pharma-academic-material-generation
description: 药企医学事务管理学术资料生成。参考 Scientific Writing skill 的 scientific draft generation 部分，构建医学事务输出能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📝"
      }
  }
---

# 学术资料生成

概述
----
本 skill 对应：药企 / 医学事务管理 / 学术资料生成。

要求：医学事务输出能力。

来源核验
--------
- 匹配来源：Scientific Writing
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/ovachiever/droid-tings/scientific-writing
- 匹配结论：匹配。该 skill 明确覆盖科学写作、摘要、正文结构和引用组织。

参考部分
--------
只参考 Scientific Writing skill 的 **scientific draft generation** 部分：
- 学术主题整理
- 受众定位
- 关键信息组织
- 正文初稿生成
- 引用列表整理

不参考部分
----------
- 不参考文献检索或文献分析
- 不参考临床试验数据统计
- 不参考市场推广文案生成
- 不扩展到图表绘制或幻灯片制作

构建方式
--------
OpenClaw 中应构建为一个独立的生成型 skill：
- 输入资料类型、主题、受众和关键信息
- 生成医学事务学术资料初稿
- 输出学术资料 JSON

建议输入字段
------------
- `material_type`：资料类型
- `topic`：主题
- `audience`：目标受众
- `key_messages`：关键信息列表
- `evidence_points`：证据要点列表
- `references`：引用列表

建议输出字段
------------
- `skill`：`学术资料生成`
- `material_type`
- `topic`
- `audience`
- `draft`
- `references`

医疗边界
--------
本 skill 只生成医学事务学术资料初稿，不构成药品推广承诺、临床治疗建议或监管申报材料。

快速开始
--------
从本 skill 目录执行：

```bash
python3 scripts/run.py --input input.json --output output.json --appkey YOUR_KEY
```

最小输入示例
------------
```json
{
  "material_type": "学术摘要",
  "topic": "EGFR 靶向治疗进展",
  "audience": "肿瘤领域医生",
  "key_messages": ["EGFR 是重要治疗靶点"],
  "evidence_points": ["相关研究显示特定人群可获益"],
  "references": ["example-ref"]
}
```

输出约定
--------
输出 UTF-8 JSON，采用统一格式：

```json
{
  "skill": "技能名称",
  "status": "ok",
  "data": { /* 结构化数据 */ },
  "text": "API 生成的 Markdown/自然语言内容，OpenClaw 直接渲染给用户"
}
```

- `data`：本地预处理得到的结构化数据
- `text`：内部医疗大模型生成的自然语言解读/分析/提醒，Markdown 格式

支持的输入格式
--------------
除 JSON 外，还支持以下格式（通过 `--input-type` 自动检测或手动指定）：

| 格式 | 说明 |
|------|------|
| JSON | 默认，直接读取结构化输入 |
| CSV / XLSX / XLS | 表格数据，按列头自动映射字段 |
| TXT / MD | key:value 文本格式（支持中文/英文字段名） |
| PDF / DOC / DOCX | 文档，提取文本后解析 |
| PNG / JPG 等图片 | OCR 提取文本后解析 |

统一入口附加参数
----------------
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型；默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码（默认：`utf-8`）。
- `--save-prepared`：保存预处理后的 JSON，便于调试。
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由用户在 OpenClaw 中调用时提供。本 skill 强制通过 API 生成学术资料初稿，无本地透传模式。

依赖
----
### 运行环境
- Python 3.7+

### Python 第三方包（可选，按输入格式需要）
| 包名 | 用途 | 必要条件 |
|------|------|---------|
| `openpyxl` | 读取 `.xlsx` 文件 | 输入为 xlsx 时必须 |
| `pypdf` | 提取 PDF 文本 | 输入为 pdf 时必须 |

### 外部工具（可选，按输入格式需要）
| 工具 | 用途 | 必要条件 |
|------|------|---------|
| LibreOffice (`soffice`) | 转换 `.doc` / `.xls` | 输入为 doc/xls 时必须 |
| `pdftotext`（poppler-utils） | 提取 PDF 文本 | 输入为 pdf 且未安装 pypdf 时 |
| `tesseract`（含 chi_sim+eng） | 图片 OCR | 输入为图片时必须 |

> 仅使用 JSON 输入时，无需安装任何第三方包或外部工具。

模型配置
--------
本 skill 执行时通过内部医疗大模型进行推理：

- endpoint：`https://maas-api.hivoice.cn/v1/chat/completions`
- model：`u1-insuremed`
- 协议：OpenAI Chat Completions（兼容标准 /v1/chat/completions）
- 鉴权：通过 `--appkey` 参数传入 Bearer token，由用户在 OpenClaw 中调用时提供

> 本 skill 强制走 API 推理，无本地透传模式。

> 强制通过 `--appkey` 调用内部医疗大模型进行推理，无本地兜底模式。
