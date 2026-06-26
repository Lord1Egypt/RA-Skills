---
name: med-pharma-clinical-trial-statistics
description: 药企药物研发辅助临床试验数据统计。参考 Statistical Analysis skill 的 descriptive statistics 与 group comparison 部分，构建试验分析支持能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊"
      }
  }
---

# 临床试验数据统计

概述
----
本 skill 对应：药企 / 药物研发辅助 / 临床试验数据统计。

要求：试验分析支持。

来源核验
--------
- 匹配来源：Statistical Analysis
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/Jst-Well-Dan/Skill-Box/statistical-analysis
- 匹配结论：匹配。该 skill 明确覆盖统计分析、描述性统计、组间比较和结果报告。

参考部分
--------
只参考 Statistical Analysis skill 的 **descriptive statistics 与 group comparison** 部分：
- 试验数据分组
- 终点变量描述性统计
- 组间均值差异整理
- 样本量计数

不参考部分
----------
- 不参考临床试验方案设计
- 不参考 EDC 或数据库管理
- 不参考医学写作或学术资料生成
- 不扩展到复杂统计建模

构建方式
--------
OpenClaw 中应构建为一个独立的统计型 skill：
- 输入临床试验记录数据
- 按试验组对终点变量做描述性统计
- 输出统计分析支持 JSON

建议输入字段
------------
- `trial_id`：试验编号
- `population`：分析集
- `group_field`：分组字段名，默认 `group`
- `endpoint_fields`：终点字段列表
- `records`：试验记录列表

建议输出字段
------------
- `skill`：`临床试验数据统计`
- `trial_id`
- `population`
- `statistics`
- `analysis_note`

医疗边界
--------
本 skill 只做临床试验数据统计整理，不替代统计分析计划、注册统计师复核或监管申报分析。

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
  "trial_id": "trial-001",
  "population": "FAS",
  "group_field": "group",
  "endpoint_fields": ["change_from_baseline"],
  "records": [
    {"subject_id": "001", "group": "试验组", "change_from_baseline": -2.1},
    {"subject_id": "002", "group": "对照组", "change_from_baseline": -0.8}
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

