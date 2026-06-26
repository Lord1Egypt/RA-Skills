---
name: med-pharma-target-screening
description: 药企药物研发辅助药物靶点筛选。参考 Open Targets Database skill 的 target-disease association 与 target prioritization 部分，构建药企研发场景下的候选靶点筛选能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯"
      }
  }
---

# 药物靶点筛选

概述
----
本 skill 对应：药企 / 药物研发辅助 / 药物靶点筛选。

要求：药企研发场景。

来源核验
--------
- 匹配来源：Open Targets Database
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/x-cmd/skill/opentargets-database
- 匹配结论：匹配。该 skill 明确覆盖 target-disease association、known drugs、druggability、safety 与 target prioritization。

参考部分
--------
只参考 Open Targets Database skill 的 **target-disease association 与 target prioritization** 部分：
- 疾病/适应症与候选靶点关联
- 证据强度整理
- 可成药性整理
- 安全风险整理
- 候选靶点优先级排序

不参考部分
----------
- 不参考外部数据库实时查询
- 不参考分子生成、化合物设计或合成路线
- 不参考临床试验设计
- 不扩展到医学事务资料生成

构建方式
--------
OpenClaw 中应构建为一个独立的筛选型 skill：
- 输入疾病/适应症和候选靶点列表
- 按证据强度、可成药性、安全风险生成靶点优先级
- 输出候选靶点筛选 JSON

建议输入字段
------------
- `disease`：疾病或适应症
- `targets`：候选靶点列表
  - `target`：靶点名称或基因符号
  - `mechanism`：作用机制
  - `evidence`：证据描述或证据强度
  - `druggability`：可成药性
  - `safety_risk`：安全风险
  - `references`：来源引用

建议输出字段
------------
- `skill`：`药物靶点筛选`
- `disease`
- `ranked_targets`
- `screening_basis`

医疗边界
--------
本 skill 只做药物研发候选靶点筛选整理，不构成临床诊断、治疗建议或药品有效性结论。

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
  "disease": "非小细胞肺癌",
  "targets": [
    {
      "target": "EGFR",
      "mechanism": "抑制肿瘤驱动信号",
      "evidence": "high",
      "druggability": "high",
      "safety_risk": "medium",
      "references": ["example-ref"]
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
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由用户在 OpenClaw 中调用时提供。本 skill 强制通过 API 进行靶点筛选排序，无本地透传模式。

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
