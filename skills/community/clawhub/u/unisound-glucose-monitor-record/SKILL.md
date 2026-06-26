---
name: med-patient-glucose-monitor-record
description: 病人端慢病管理血糖监测记录。参考 Glucosio 的 blood glucose logging 部分，构建慢病管理基础记录能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩸"
      }
  }
---

# 血糖监测记录

概述
----
本 skill 对应：病人端 / 慢病管理 / 血糖监测记录。

要求：慢病管理基础记录能力。

来源核验
--------
- 匹配来源：Glucosio
- 来源类型：公开开源 Android App
- 来源链接：https://f-droid.org/packages/org.glucosio.android/
- 匹配结论：匹配。Glucosio 明确面向糖尿病管理，包含 blood glucose 记录、HbA1c、目标范围、提醒、图表、CSV 导入导出等能力。

参考部分
--------
只参考 Glucosio 的 **blood glucose logging** 部分：
- 血糖值记录
- 血糖测量类型区分
- 血糖目标范围
- 历史记录与趋势展示
- CSV 导入导出思路

不参考部分
----------
- 不参考 Glucosio 的完整 Android App 架构
- 不参考 Google Drive 备份
- 不参考研究数据上报
- 不扩展到血压、胆固醇、体重等非本 skill 能力

构建方式
--------
OpenClaw 中应构建为一个独立的记录型 skill：
- 输入患者本次血糖记录信息
- 识别并结构化血糖值、单位、测量时间、测量类型
- 输出标准血糖记录 JSON
- 可追加输出简短自然语言确认

建议输入字段
------------
- `value`：血糖值
- `unit`：单位，如 `mmol/L` 或 `mg/dL`
- `measure_type`：测量类型，如空腹、餐后、随机
- `measured_at`：测量时间
- `note`：备注

建议输出字段
------------
- `skill`：`血糖监测记录`
- `record_type`：`blood_glucose`
- `value`
- `unit`
- `measure_type`
- `measured_at`
- `note`

医疗边界
--------
本 skill 只做血糖记录，不做诊断，不替代医生判断。

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
  "value": 6.8,
  "unit": "mmol/L",
  "measure_type": "空腹",
  "measured_at": "2026-04-29 08:00",
  "note": ""
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
血糖值：6.8
单位：mmol/L
测量类型：空腹
```

CSV 格式示例
-----------
```
血糖值,单位,测量类型
6.8,mmol/L,空腹
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
