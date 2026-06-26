---
name: med-patient-health-record-management
description: 病人端通用健康健康档案管理。参考 GitEHR 的 patient-owned health record 部分，构建病史、过敏史等信息管理能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "🗃️"
      }
  }
---

# 健康档案管理

概述
----
本 skill 对应：病人端 / 通用健康 / 健康档案管理。

要求：病史、过敏史等信息管理。

来源核验
--------
- 匹配来源：GitEHR
- 来源类型：公开开源健康档案平台
- 来源链接：https://gitehr.org/
- 匹配结论：匹配。GitEHR 明确强调 patient-owned、portable、offline-first、auditable health records，适合参考患者端健康档案结构。

参考部分
--------
只参考 GitEHR 的 **patient-owned health record** 部分：
- 患者持有健康档案
- 可移植文件化记录
- 追加式历史
- 离线优先
- 审计追踪思路

不参考部分
----------
- 不参考 Git 加密链实现
- 不参考机构协同同步
- 不参考完整 HL7/FHIR 适配器
- 不扩展到医院 EHR 系统

构建方式
--------
OpenClaw 中应构建为一个独立的档案型 skill：
- 输入患者健康档案条目
- 按基础信息、病史、过敏史、手术史、家族史、用药史组织
- 支持新增、更新和查询
- 输出结构化健康档案摘要

建议输入字段
------------
- `profile`
- `medical_history`
- `allergy_history`
- `surgery_history`
- `family_history`
- `medication_history`
- `updated_at`

建议输出字段
------------
- `skill`：`健康档案管理`
- `profile`
- `medical_history`
- `allergy_history`
- `surgery_history`
- `family_history`
- `medication_history`

医疗边界
--------
本 skill 只做健康档案管理，不判断病史风险，不生成诊断或治疗建议。

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
  "profile": {"gender": "女", "birth_year": 1968},
  "medical_history": ["高血压"],
  "allergy_history": ["青霉素"],
  "surgery_history": [],
  "family_history": [],
  "medication_history": ["长期服用降压药"],
  "updated_at": "2026-04-29"
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
基本信息：张三,65岁,男
既往史：高血压
```

CSV 格式示例
-----------
```
基本信息,既往史
张三,高血压
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
