---
name: med-patient-exercise-guidance
description: 病人端术后康复运动指导。参考 CareKit 的 instructions task view 部分，构建训练动作指导能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏃"
      }
  }
---

# 运动指导

概述
----
本 skill 对应：病人端 / 术后康复 / 运动指导。

要求：训练动作指导。

来源核验
--------
- 匹配来源：CareKit
- 来源类型：公开开源护理计划框架
- 来源链接：https://github.com/carekit-apple/CareKit
- 匹配结论：匹配。CareKit 的 instructions task view 用于展示任务标题、时间和执行说明，适合参考康复动作指导的展示结构。

参考部分
--------
只参考 CareKit 的 **instructions task view** 部分：
- 任务标题
- 执行时间
- 指导说明
- 完成按钮
- 任务卡片结构

不参考部分
----------
- 不参考 iOS 组件代码
- 不参考完整 CareKitUI
- 不扩展到动作识别或视频分析
- 不生成新的康复训练处方

构建方式
--------
OpenClaw 中应构建为一个独立的指导型 skill：
- 输入康复动作条目
- 输出动作名称、执行说明、次数/时长、注意事项
- 支持按今日任务引用动作指导
- 输出结构化指导内容，便于前端渲染

建议输入字段
------------
- `exercise_name`
- `phase`
- `instruction`
- `frequency`
- `duration`
- `precautions`

建议输出字段
------------
- `skill`：`运动指导`
- `exercise_name`
- `instruction`
- `frequency`
- `duration`
- `precautions`

医疗边界
--------
本 skill 只展示既有动作指导，不替代康复师现场评估。

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
  "exercise_name": "踝泵运动",
  "phase": "第1阶段",
  "instruction": "按既有康复计划中的动作说明执行",
  "frequency": "每日3次",
  "duration": "每次5分钟",
  "precautions": ["如出现明显不适，按原计划要求停止并联系医生"]
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
运动名称：踝泵运动
阶段：术后第1周
频次：每日3次
时长：每次10分钟
```

CSV 格式示例
-----------
```
运动名称,阶段,频次,时长
踝泵运动,术后第1周,每日3次,每次10分钟
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
