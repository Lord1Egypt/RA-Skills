---
name: med-primary-diagnosis-surgery-selection
description: 主诊断和主手术选择。输入病历摘要、候选诊断和候选手术，调用内部医疗大模型，从候选项中选择本次入院的主诊断和主手术。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺"
      }
  }
---

# 主诊断和主手术选择

概述
----
给定患者本次住院相关病历摘要，以及外部传入的候选诊断和候选手术，本技能直接调用内部医疗大模型，从候选项中分别选择：

- 本次入院的主诊断
- 本次入院的主手术

本技能只做候选选择，不生成候选列表外的新诊断或新手术。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理主诊断/主手术选择所需的病历摘要和候选项。
- **严格脱敏**：调用方应在传入前完成姓名、证件号、手机号、详细地址等可识别身份信息的脱敏。
- **不做本地持久化**：脚本不把请求体、中间结果或审核结果写入本地文件或数据库。
- **模型调用说明**：默认调用内部医疗大模型 `u1-insuremed`；鉴权 `appkey` 必须由调用方传入，调用时使用 Bearer 鉴权。
- **医疗边界**：输出为医保编码/病案首页填写辅助信息，不构成医疗诊断或治疗建议。

输入格式
--------
统一入口支持 `pdf/doc/docx/xls/xlsx/csv/txt/json`。JSON 可包含病历字段和候选项；普通病历文件会先预处理为文本，并通过命令行参数传入候选诊断和候选手术。

JSON 输入示例：

```json
{
  "admission": "入院情况文本",
  "treatment": "诊疗过程文本",
  "pathology": "病理文本，可为空",
  "candidate_diagnoses": ["支气管扩张", "曲霉菌性肺炎"],
  "candidate_surgeries": ["胸腔镜下肺叶切除术", "呼吸机治疗[大于等于96小时]"]
}
```

也支持直接传入完整 prompt：

```json
{
  "prompt": "根据如下患者信息，以及对应的【候选诊断】和【候选手术】..."
}
```

审核规则
--------
- **候选优先**：主诊断和主手术必须从传入候选中选择，不输出候选外答案。
- **本次入院优先**：选择与本次入院目的、主要治疗过程、资源消耗和出院结论最相关的诊断/手术。
- **主诊断边界**：优先选择导致本次住院、消耗主要医疗资源、解释主要治疗目标的诊断。
- **主手术边界**：优先选择与本次住院主要治疗目的和核心资源消耗直接相关的手术/操作。
- **保守处理**：候选中存在辅助操作、并发支持治疗或历史诊断时，不能因字面重要而自动选为主项。

快速开始
--------

```bash
# JSON 结构化输入，候选诊断和候选手术来自 JSON
conda run -n deep-review-ins python doctor/icd-drg/primary-diagnosis-surgery-selection/scripts/run.py \
  --input doctor/icd-drg/primary-diagnosis-surgery-selection/example/sample.json \
  --appkey <your-appkey> \
  --timeout 120

# TXT/PDF 等普通病历文件；必须显式传入候选诊断和候选手术
conda run -n deep-review-ins python doctor/icd-drg/primary-diagnosis-surgery-selection/scripts/run.py \
  --input /path/to/record.txt \
  --appkey <your-appkey> \
  --candidate-diagnosis 支气管扩张 \
  --candidate-diagnosis 曲霉菌性肺炎 \
  --candidate-surgery 胸腔镜下肺叶切除术 \
  --candidate-surgery '呼吸机治疗[大于等于96小时]' \
  --save-prepared \
  --timeout 120
```

参数说明
--------
- `--input PATH`：**必填**。输入 JSON 文件。
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型，默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码，默认 `utf-8`。
- `--candidate-diagnosis STRING`：候选诊断；可重复。
- `--candidate-diagnoses-json STRING`：候选诊断字符串数组 JSON 或文件路径。
- `--candidate-surgery STRING`：候选手术；可重复。
- `--candidate-surgeries-json STRING`：候选手术字符串数组 JSON 或文件路径。
- 普通 `txt/pdf/doc/docx/xls/xlsx/csv` 文件不会自动知道候选诊断和候选手术，必须传候选列表参数。
- `--base URL`：内部大模型 base URL，默认 `https://maas-api.hivoice.cn/v1`。
- `--model STRING`：模型名称，默认 `u1-insuremed`。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待，默认 `0`。
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由平台分配；调用时使用 Bearer 鉴权。
- `--output-json PATH`：可选。保存输出 JSON；同时传 `--output` 时优先使用该参数。
- `--output PATH`：可选。兼容旧调用方式，等同于 `--output-json`。
- `--save-prepared`：可选。保存预处理后的病历文本到 `doctor/icd-drg/runs/primary-diagnosis-surgery-selection/` 或输出文件所在目录；路径提示输出到 stderr。

输出约定
--------
CLI 只输出 JSON，不输出 Markdown、序号或额外提示语。响应结构：

```json
{
  "main_diagnosis": "曲霉菌性肺炎",
  "main_surgery": "胸腔镜下肺叶切除术"
}
```

示例
----
- 正例：候选诊断包含本次住院主要治疗目标，候选手术包含实际核心手术，输出对应主诊断和主手术。
- 正例：病历同时包含支持治疗和核心手术时，应优先选择与本次入院主要治疗目的最相关的候选手术。
- 边界例：候选诊断包含既往史和本次治疗疾病时，不因既往史字面出现频繁而选为主诊断。
- 不应匹配例：候选列表外即使有更合适的诊断或手术，也不得输出候选外答案。

依赖
----
- Python 3.11+
- 仅使用 Python 标准库。
- 需要网络访问内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

测试命令
--------
从 `skills` 根目录执行：

```bash
conda run -n deep-review-ins python doctor/icd-drg/primary-diagnosis-surgery-selection/scripts/run.py \
  --input doctor/icd-drg/primary-diagnosis-surgery-selection/example/sample.json \
  --appkey <your-appkey> \
  --timeout 120
```

备注
----
- `scripts/run.py` 是唯一对外入口。
- 示例输入放在 `example/sample.json`。
