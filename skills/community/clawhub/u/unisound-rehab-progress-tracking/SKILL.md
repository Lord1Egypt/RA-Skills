---
name: med-patient-rehab-progress-tracking
description: 病人端术后康复进度追踪。参考 rehabilitation-analyzer 的 progress analysis 部分，构建康复效果可视化能力。
metadata:
  {
    "openclaw":
      {
        "emoji": "📈"
      }
  }
---

# 康复进度追踪

概述
----
本 skill 对应：病人端 / 术后康复 / 康复进度追踪。

要求：康复效果可视化。

来源核验
--------
- 匹配来源：rehabilitation-analyzer
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/huifer/WellAlly-health/rehabilitation-analyzer
- 匹配结论：匹配。该 skill 明确包含康复进展分析、功能改善曲线、疼痛模式识别、目标达成率、阶段分析和训练依从性评估。

参考部分
--------
只参考 rehabilitation-analyzer 的 **progress analysis** 部分：
- 康复进展分析
- 功能改善趋势
- 疼痛趋势
- 训练依从性
- 目标达成情况
- 阶段进展

不参考部分
----------
- 不参考完整报告长模板
- 不参考个性化康复建议生成
- 不扩展到康复处方调整
- 不处理急性疼痛或并发症判断

构建方式
--------
OpenClaw 中应构建为一个独立的分析型 skill：
- 输入康复任务完成记录、疼痛评分、功能自测结果
- 计算完成率和趋势
- 输出阶段进度、可视化指标和待关注事项
- 为患者端展示提供结构化摘要

建议输入字段
------------
- `plan_id`
- `task_records`
- `pain_scores`
- `functional_assessments`
- `phase`
- `date_range`

建议输出字段
------------
- `skill`：`康复进度追踪`
- `completion_rate`
- `pain_trend`
- `function_trend`
- `phase_progress`
- `attention_items`

医疗边界
--------
本 skill 只做康复记录汇总与趋势展示，不判断治疗效果，不替代康复师评估。

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
  "plan_id": "rehab-plan-001",
  "phase": "第1阶段",
  "task_records": [
    {"name": "踝泵运动", "status": "completed"},
    {"name": "伤口观察", "status": "pending"}
  ],
  "pain_scores": [{"score": 3}, {"score": 2}],
  "functional_assessments": [{"score": 60}, {"score": 65}],
  "phase_progress": "进行中"
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
计划ID：rehab-001
阶段：术后第2周
```

CSV 格式示例
-----------
```
计划ID,阶段
rehab-001,术后第2周
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
