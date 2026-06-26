---
name: med-pharma-literature-analysis
description: 药企医学事务管理研发文献分析。参考 Literature Review skill 的 evidence synthesis 部分，构建文献分析能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📚"
      }
  }
---

# 研发文献分析

概述
----
本 skill 对应：药企 / 医学事务管理 / 研发文献分析。

要求：文献分析能力。

来源核验
--------
- 匹配来源：Literature Review
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/ovachiever/droid-tings/literature-review
- 匹配结论：匹配。该 skill 明确覆盖文献筛选、证据综合、研究问题整理和引用核验。

参考部分
--------
只参考 Literature Review skill 的 **evidence synthesis** 部分：
- 研发主题匹配
- 文献信息结构化
- 关键发现提取
- 证据摘要
- 研究空白整理

不参考部分
----------
- 不参考外部文献库实时检索
- 不参考学术资料生成
- 不参考临床试验数据统计
- 不扩展到个体化医疗建议

构建方式
--------
OpenClaw 中应构建为一个独立的分析型 skill：
- 输入研发主题和文献列表
- 按主题或关键词筛选文献
- 输出文献分析 JSON

建议输入字段
------------
- `topic`：研发主题
- `keywords`：关键词列表
- `literature`：文献列表
  - `title`
  - `year`
  - `journal`
  - `study_type`
  - `abstract`
  - `conclusion`
  - `url`

建议输出字段
------------
- `skill`：`研发文献分析`
- `topic`
- `matched_literature`
- `evidence_summary`
- `research_gaps`

医疗边界
--------
本 skill 只做研发文献分析整理，不构成临床诊疗建议或药品推广结论。

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
  "topic": "EGFR 非小细胞肺癌",
  "keywords": ["EGFR", "NSCLC"],
  "literature": [
    {
      "title": "EGFR targeted therapy in NSCLC",
      "year": 2024,
      "journal": "Example Journal",
      "study_type": "review",
      "abstract": "Review of EGFR targeted therapy.",
      "conclusion": "EGFR remains a key target in selected NSCLC patients.",
      "url": "https://example.org/article"
    }
  ]
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
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由用户在 OpenClaw 中调用时提供。本 skill 强制通过 API 进行语义级文献分析，无本地透传模式。

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
