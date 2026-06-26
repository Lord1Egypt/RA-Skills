---
name: med-patient-followup-reminder
description: 病人端慢病管理随访复诊提醒。参考 Simple 的 appointments/overdue patients 部分，构建管理连续性能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📅"
      }
  }
---

# 随访复诊提醒

概述
----
本 skill 对应：病人端 / 慢病管理 / 随访复诊提醒。

要求：管理连续性能力。

来源核验
--------
- 匹配来源：Simple
- 来源类型：公开开源慢病管理系统
- 来源链接：https://docs.simple.org/readme/simple-app-features
- 匹配结论：匹配。Simple 明确使用 appointment 作为 return-to-care 提醒，并有 overdue patients、SMS reminder、默认复诊周期等机制。

参考部分
--------
只参考 Simple 的 **appointments/overdue patients** 部分：
- 复诊日期
- 默认复诊周期
- 逾期识别
- 回访提醒
- 回访状态记录

不参考部分
----------
- 不参考医疗机构端完整工作流
- 不参考患者搜索、BP Passport、Secure Calling
- 不参考 Simple Dashboard
- 不扩展到医生排班系统

构建方式
--------
OpenClaw 中应构建为一个独立的提醒型 skill：
- 输入上次就诊日期、复诊周期或医嘱复诊日期
- 生成复诊提醒
- 判断是否逾期
- 输出提醒状态和建议下一步动作

建议输入字段
------------
- `last_visit_date`：上次就诊日期
- `followup_date`：复诊日期（与 followup_interval_days 二选一）
- `followup_interval_days`：复诊周期天数（与 followup_date 二选一）
- `disease_type`：疾病类型
- `note`：备注

建议输出字段
------------
- `skill`：`随访复诊提醒`
- `followup_date`
- `is_overdue`
- `days_overdue`
- `reminder_status`
- `suggested_action`

医疗边界
--------
本 skill 只做随访复诊提醒，不判断是否必须就诊，不替代医生安排。

快速开始
--------
从本 skill 目录执行：

```bash
python3 scripts/run.py --input input.json --today 2026-04-29 --output output.json --appkey YOUR_KEY
```

最小输入示例
------------
```json
{
  "disease_type": "高血压",
  "last_visit_date": "2026-04-01",
  "followup_interval_days": 28,
  "note": ""
}
```

参数说明
--------
- `--input PATH`：输入 JSON。
- `--today YYYY-MM-DD`：用于判断是否逾期，默认当天。
- `--output PATH`：输出 JSON；不传则输出到 stdout。

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
上次就诊：2026-04-01
间隔天数：28
疾病类型：糖尿病
```

CSV 格式示例
-----------
```
上次就诊,间隔天数,疾病类型
2026-04-01,28,糖尿病
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
