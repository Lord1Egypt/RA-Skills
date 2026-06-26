---
name: med-patient-medication-reminder
description: 病人端慢病管理用药提醒。参考 MedTimer 的 medication reminder 部分，构建提升慢病依从性的提醒能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "💊"
      }
  }
---

# 用药提醒

概述
----
本 skill 对应：病人端 / 慢病管理 / 用药提醒。

要求：提升慢病依从性。

来源核验
--------
- 匹配来源：MedTimer
- 来源类型：公开开源 Android App
- 来源链接：https://f-droid.org/en/packages/com.futsch1.medtimer/
- 匹配结论：匹配。MedTimer 明确支持 medication and pill reminder、服药确认/忽略、剂量历史、离线隐私等能力。

参考部分
--------
只参考 MedTimer 的 **medication reminder** 部分：
- 用药提醒时间
- 重复规则
- 确认服药
- 延后提醒
- 漏服记录

不参考部分
----------
- 不参考完整 Android 通知实现
- 不参考生物识别锁定
- 不参考库存管理
- 不扩展到药品知识库或处方审核

构建方式
--------
OpenClaw 中应构建为一个独立的提醒型 skill：
- 输入药品名称、剂量、频次、提醒时间
- 生成结构化提醒计划
- 支持输出今日提醒清单
- 支持标记提醒状态

建议输入字段
------------
- `medicine_name`：药品名称
- `dose`：剂量
- `frequency`：频次
- `remind_times`：提醒时间列表
- `start_date`
- `end_date`
- `status`：启用或停用

建议输出字段
------------
- `skill`：`用药提醒`
- `reminder_type`：`medication`
- `medicine_name`
- `dose`
- `schedule`
- `status`
- `today_reminders`

医疗边界
--------
本 skill 只做提醒管理，不判断药物是否适合患者，不调整医嘱。

快速开始
--------
从本 skill 目录执行：

```bash
python3 scripts/run.py --input input.json --date 2026-04-29 --output output.json --appkey YOUR_KEY
```

最小输入示例
------------
```json
{
  "medicine_name": "二甲双胍",
  "dose": "0.5g",
  "frequency": "每日2次",
  "remind_times": ["08:00", "20:00"],
  "start_date": "2026-04-01",
  "end_date": "",
  "status": "active"
}
```

参数说明
--------
- `--input PATH`：输入 JSON。
- `--date YYYY-MM-DD`：生成哪一天的提醒，默认当天。
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
