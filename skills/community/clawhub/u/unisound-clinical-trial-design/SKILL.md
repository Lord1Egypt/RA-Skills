---
name: med-pharma-clinical-trial-design
description: 药企药物研发辅助临床试验设计辅助。参考 Clinical Trial Protocol Skill 的 protocol design 部分，构建药研方法设计能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📋"
      }
  }
---

# 临床试验设计辅助

概述
----
本 skill 对应：药企 / 药物研发辅助 / 临床试验设计辅助。

要求：药研方法设计。

来源核验
--------
- 匹配来源：Clinical Trial Protocol Skill
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/anthropics/healthcare/clinical-trial-protocol-skill
- 匹配结论：匹配。该 skill 明确覆盖临床试验 protocol 设计、研究目的、入排标准、终点和访视安排。

参考部分
--------
只参考 Clinical Trial Protocol Skill 的 **protocol design** 部分：
- 研究目的
- 研究分期
- 研究类型
- 入排标准
- 主要/次要终点
- 访视安排

不参考部分
----------
- 不参考临床试验数据统计
- 不参考受试者招募管理
- 不参考监管递交文件生成
- 不扩展到药物靶点筛选或医学事务资料生成

构建方式
--------
OpenClaw 中应构建为一个独立的设计型 skill：
- 输入适应症、干预措施、试验分期和研究目的
- 整理研究设计、入排标准、终点和访视安排
- 输出临床试验设计辅助 JSON

建议输入字段
------------
- `indication`：适应症
- `intervention`：干预措施
- `phase`：试验分期
- `objective`：研究目的
- `population`：目标人群
- `control`：对照方式
- `randomization`：随机化方式
- `blinding`：盲法
- `endpoints`：终点列表
- `visits`：访视安排

建议输出字段
------------
- `skill`：`临床试验设计辅助`
- `indication`
- `intervention`
- `phase`
- `study_design`
- `population`
- `endpoints`
- `visit_schedule`

医疗边界
--------
本 skill 只做临床试验方法设计辅助，不替代伦理审查、法规审查、统计师或临床专家最终确认。

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
  "indication": "非小细胞肺癌",
  "intervention": "研究药物A",
  "phase": "II期",
  "objective": "评价初步有效性和安全性",
  "population": "既往治疗失败患者",
  "control": "标准治疗",
  "randomization": "1:1",
  "blinding": "开放标签",
  "endpoints": ["ORR", "PFS"],
  "visits": ["筛选期", "基线", "每3周一次"]
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
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由用户在 OpenClaw 中调用时提供。本 skill 强制通过 API 提供临床试验设计建议，无本地透传模式。

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
