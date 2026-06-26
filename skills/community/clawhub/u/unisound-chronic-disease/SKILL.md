---
name: med-chronic-disease-review
description: 门诊慢病审核（糖尿病/高血压）。输入 OCR 结果数组 JSON，由内部医疗大模型输出审核结论与原因（原始 JSON + 自然语言结论）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺"
      }
  }
---

# 门诊慢病审核

概述
----
给定一份 OCR 结果数组（每项包含 `fileName/page/docType/ocrText`），本技能会：

- 调用内部医疗大模型进行慢病审核推理
- 输出结构化 JSON（含 `final_decision`、`reasoning`）
- 输出自然语言摘要（结论 + 原因）

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理审核所必需的文本内容；不要求也不鼓励提供与审核无关的身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理（如姓名、证件号、手机号、详细地址、人脸/影像等）。仅传递脱敏后的必要信息用于本次 skill 调用。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储（包含磁盘文件、数据库、日志）。仅在内存中短暂处理；**本次调用结束即销毁**。
- **第三方 API 风险提示**：在功能需要时，会调用内部医疗大模型接口；此时仅会发送**脱敏后的必要信息**，并使用加密传输。除完成本次请求外，不用于任何其他用途（如训练、画像、营销）。
- **医疗边界**：本技能输出为审核规则匹配与原因摘要的辅助信息，不构成医疗诊断或治疗建议；如涉及临床判断请以执业医生意见为准。

输入格式
--------
输入必须是 JSON 数组（list），示例：

```json
[
  {"fileName":"xxx.pdf","page":1,"docType":"出院记录","ocrText":"..."},
  {"fileName":"xxx.pdf","page":2,"docType":"检验报告","ocrText":"..."}
]
```

也支持通过统一入口 `scripts/run.py` 直接输入 `pdf/doc/docx/xls/xlsx/csv/txt/json`。
预处理成功后，会先归一化为 `ocr_array.json`（每项含 `fileName/page/docType/ocrText`），再调用医疗大模型审核。

快速开始
--------
从 `skills` 目录执行：

```bash
# 糖尿病
python3 insurance/claims-review/chronic-disease/scripts/run.py \
  --disease-code diabetes \
  --appkey <your-appkey> \
  --input data/med-chronic-disease-review/糖尿病_ocr_task_result.json

# 高血压
python3 insurance/claims-review/chronic-disease/scripts/run.py \
  --disease-code hypertension \
  --appkey <your-appkey> \
  --input data/med-chronic-disease-review/高血压_ocr_task_result.json

# 本地校验（不调模型）
python3 insurance/claims-review/chronic-disease/scripts/run.py \
  --disease-code diabetes \
  --dry-run \
  --input data/med-chronic-disease-review/糖尿病_ocr_task_result.json

# 或继续直接使用原始 OCR 数组入口
python3 insurance/claims-review/chronic-disease/scripts/chronic_disease_review.py \
  --disease-code diabetes \
  --appkey <your-appkey> \
  --input data/med-chronic-disease-review/糖尿病_ocr_task_result.json
```

参数说明
--------
- `--disease-code STRING`：**必填**。糖尿病/高血压（也支持 `diabetes/hypertension/dm/htn` 别名）。本 skill 每次只审核一个病种。
- `--review-type STRING`：可选。默认 `慢病审核`。
- `--appkey STRING`：**必填**（`--dry-run` 时除外）。内部医疗大模型鉴权 key，由平台分配。
- `--input PATH`：OCR 数组 JSON（UTF-8）或经 `run.py` 支持的文档格式。
- `--base URL`：大模型 base（默认：`https://maas-api.hivoice.cn/v1`）。
- `--model STRING`：模型名（默认：`u1-insuremed`）。
- `--timeout SECONDS`：HTTP 超时（默认：120）。
- `--dry-run`：跳过模型调用，输出占位结论（用于联调预处理链路）。
- `--output-json PATH`：保存原始返回 JSON（默认：`../runs/med-chronic-disease-review/{scenario}_resp.json`）。
- `--output-text PATH`：保存自然语言摘要（默认：`../runs/med-chronic-disease-review/{scenario}_resp.txt`）。

统一入口附加参数（`scripts/run.py`）
----------------------------------
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型；默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码（默认：`utf-8`）。
- `--save-prepared`：保存预处理后的 OCR 数组 JSON，便于调试。

输出约定
--------
- 若输出路径父目录不存在，会自动创建。
- 自然语言摘要重点字段：
  - `final_decision`：通过/不通过/待补充
  - `reasoning`：原因（可选）

依赖
----
### 前置 Skill
本 skill 的 `scripts/run.py` 依赖 **`_shared/doc-preprocess`** 提供的公共文件预处理库（`preprocess.py`）。
请确保 `_shared/doc-preprocess/` 位于 `skills/` 根目录下。

### 运行环境
- Python 3.7+

### 模型配置
本 skill 通过内部医疗大模型进行推理（不再依赖商保后端审核 flow API）：

- endpoint：`https://maas-api.hivoice.cn/v1/chat/completions`
- model：`u1-insuremed`
- 协议：OpenAI Chat Completions（兼容标准 `/v1/chat/completions`）
- 鉴权：通过 `--appkey` 参数传入 Bearer token，由用户在 OpenClaw 中调用时提供

> 强制通过 `--appkey` 调用内部医疗大模型；`--dry-run` 仅用于本地链路校验。

### Python 第三方包（可选，按输入格式需要）
| 包名 | 用途 | 必要条件 |
|------|------|---------|
| `openpyxl` | 读取 `.xlsx` 文件 | 输入为 xlsx 时必须 |
| `pypdf` | 提取 PDF 文本 | 输入为 pdf 时必须（或用 pdftotext 替代） |

安装：`pip install openpyxl pypdf`

### 外部工具（可选，按输入格式需要）
| 工具 | 用途 | 必要条件 |
|------|------|---------|
| LibreOffice (`soffice`) | 转换 `.doc` / `.xls` 为文本 | 输入为 doc/xls 时必须 |
| `pdftotext`（poppler-utils） | 提取 PDF 文本 | 输入为 pdf 且未安装 pypdf 时必须 |
| `tesseract`（含 chi_sim+eng 语言包） | 图片 OCR | 输入为 png/jpg/bmp/tif 等图片时必须 |

安装（Ubuntu/Debian）：`sudo apt-get install libreoffice poppler-utils tesseract-ocr tesseract-ocr-chi-sim`

> 仅使用 JSON 输入时，无需安装任何第三方包或外部工具。

备注
----
- **发布约束**：示例输入、运行输出、自测脚本均放在 skill 包外（分别位于 `../data/`、`../runs/`、`../self_tests/`），skill 目录内仅保留可发布的核心文件（`scripts/`、`SKILL.md`、`_meta.json`）。
