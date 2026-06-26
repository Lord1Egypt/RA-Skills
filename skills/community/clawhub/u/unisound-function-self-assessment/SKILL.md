---
name: med-patient-function-self-assessment
description: 病人端术后康复功能自测评估。参考 ResearchKit 的 surveys/questionnaires 部分，构建自评量表能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📝"
      }
  }
---

# 功能自测评估

概述
----
本 skill 对应：病人端 / 术后康复 / 功能自测评估。

要求：自评量表能力。

来源核验
--------
- 匹配来源：ResearchKit
- 来源类型：公开开源研究/问卷框架
- 来源链接：https://github.com/ResearchKit/ResearchKit
- 匹配结论：匹配。ResearchKit 明确提供 surveys 能力，可用于问卷问题、答案格式、表单步骤和结果采集。

参考部分
--------
只参考 ResearchKit 的 **surveys/questionnaires** 部分：
- 问卷步骤
- 问题项
- 答案格式
- 表单式自评
- 结果结构化

不参考部分
----------
- 不参考知情同意流程
- 不参考主动传感器任务
- 不参考研究项目管理
- 不扩展到医学诊断量表判定

构建方式
--------
OpenClaw 中应构建为一个独立的自评型 skill：
- 输入自评量表定义和患者回答
- 结构化保存每个问题的答案
- 计算简单总分或分项得分
- 输出自评结果摘要

建议输入字段
------------
- `assessment_id`
- `questions`
- `answers`
- `assessed_at`

建议输出字段
------------
- `skill`：`功能自测评估`
- `assessment_id`
- `score`
- `answer_summary`
- `assessed_at`

医疗边界
--------
本 skill 只做自评问卷收集和基础计分，不做诊断，不替代专业评估。

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
  "assessment_id": "rehab-self-assessment-001",
  "questions": [
    {"id": "pain", "text": "疼痛评分"},
    {"id": "walk", "text": "行走能力评分"}
  ],
  "answers": {
    "pain": 2,
    "walk": 4
  },
  "assessed_at": "2026-04-29"
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

文本格式示例
-----------
```
评估ID：func-001
评估时间：2026-04-29
```

CSV 格式示例
-----------
```
评估ID,评估时间
func-001,2026-04-29
```

统一入口附加参数
----------------
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型；默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码（默认：`utf-8`）。
- `--save-prepared`：保存预处理后的 JSON，便于调试。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。

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
