---
name: med-patient-blood-pressure-monitor-record
description: 病人端慢病管理血压监测记录。参考 HealthLog 的 vitals/measurements 部分，构建慢病管理基础记录能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "❤️"
      }
  }
---

# 血压监测记录

概述
----
本 skill 对应：病人端 / 慢病管理 / 血压监测记录。

要求：慢病管理基础记录能力。

来源核验
--------
- 匹配来源：HealthLog
- 来源类型：公开开源自托管健康记录 App
- 来源链接：https://healthlog.dev/
- 匹配结论：匹配。HealthLog 明确支持 blood pressure、heart rate 等 vitals 记录，并提供趋势图、自托管和 Docker 部署方式。

参考部分
--------
只参考 HealthLog 的 **vitals/measurements** 部分：
- 血压记录
- 心率记录
- 测量时间记录
- 历史趋势展示
- JSON/CSV 数据导出思路

不参考部分
----------
- 不参考 HealthLog 的完整账号系统
- 不参考 Withings 同步
- 不参考 AI 健康报告
- 不扩展到体重、睡眠、情绪等非本 skill 能力

构建方式
--------
OpenClaw 中应构建为一个独立的记录型 skill：
- 输入患者本次血压测量信息
- 结构化收缩压、舒张压、心率、测量时间
- 输出标准血压记录 JSON
- 可追加输出简短自然语言确认

建议输入字段
------------
- `systolic`：收缩压
- `diastolic`：舒张压
- `heart_rate`：心率
- `unit`：默认 `mmHg`
- `measured_at`：测量时间
- `note`：备注

建议输出字段
------------
- `skill`：`血压监测记录`
- `record_type`：`blood_pressure`
- `systolic`
- `diastolic`
- `heart_rate`
- `unit`
- `measured_at`
- `note`

医疗边界
--------
本 skill 只做血压记录，不做诊断，不替代医生判断。

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
  "systolic": 128,
  "diastolic": 82,
  "heart_rate": 76,
  "unit": "mmHg",
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
收缩压：130
舒张压：85
心率：72
```

CSV 格式示例
-----------
```
收缩压,舒张压,心率
130,85,72
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
