---
name: med-patient-medication-record-management
description: 病人端通用健康用药记录管理。参考 MedTimer 的 medication list/dose history 部分，构建个人长期用药管理能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📋"
      }
  }
---

# 用药记录管理

概述
----
本 skill 对应：病人端 / 通用健康 / 用药记录管理。

要求：个人长期用药管理。

来源核验
--------
- 匹配来源：MedTimer
- 来源类型：公开开源 Android App
- 来源链接：https://f-droid.org/en/packages/com.futsch1.medtimer/
- 匹配结论：匹配。MedTimer 明确支持 medication list、dose history、CSV 导出、JSON 备份恢复和标签过滤。

参考部分
--------
只参考 MedTimer 的 **medication list/dose history** 部分：
- 药品列表
- 剂量记录
- 服药历史
- CSV 导出
- JSON 备份恢复

不参考部分
----------
- 不参考提醒通知实现
- 不参考库存提醒
- 不参考复杂 Android 本地存储
- 不扩展到处方审核或药物相互作用判断

构建方式
--------
OpenClaw 中应构建为一个独立的管理型 skill：
- 输入长期用药条目
- 支持新增、更新、停用、查询
- 输出个人用药清单和历史摘要
- 与用药提醒 skill 保持数据字段兼容

建议输入字段
------------
- `medicine_name`
- `dose`
- `frequency`
- `start_date`
- `end_date`
- `status`
- `note`

建议输出字段
------------
- `skill`：`用药记录管理`
- `medications`
- `active_medications`
- `stopped_medications`
- `history_summary`

医疗边界
--------
本 skill 只管理个人用药记录，不判断药品适应症，不调整用药方案。

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
  "medications": [
    {
      "medicine_name": "二甲双胍",
      "dose": "0.5g",
      "frequency": "每日2次",
      "start_date": "2026-04-01",
      "end_date": "",
      "status": "active",
      "note": ""
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

文本格式示例
-----------
```
药品名称：二甲双胍
剂量：500mg
频次：每日2次
状态：active
```

CSV 格式示例
-----------
```
药品名称,剂量,频次,状态
二甲双胍,500mg,每日2次,active
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
