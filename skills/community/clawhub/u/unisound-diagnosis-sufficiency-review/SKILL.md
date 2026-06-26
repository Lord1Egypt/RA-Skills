---
name: med-diagnosis-sufficiency-review
description: 诊断依据充分性审核。输入结构化病案 record 与待审核诊断列表，输出诊断依据充分性审核结果。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺"
      }
  }
---

# 诊断依据充分性审核

概述
----
给定结构化病案 `record` 和待审核诊断列表，本技能从诊断依据充分性规则库读取指南，核对病历文书证据，输出诊断依据是否充分。

本技能会：
- 从 `diagnosis_sufficiency_guidelines` 读取诊断依据充分性审核指南。
- 按诊断 `role` 区分主诊断和其他诊断，分别匹配指南适用范围。
- 优先按用户提供的 `diagnoses` 候选列表审核；未提供时，默认审核 `record.diagnosis.primaryDiagnosis` 和 `record.diagnosis.otherDiagnoses` 中的全部诊断。
- 调用 skill 内置的 `review_diagnosis_sufficiency_record` function 完成审核。
- 通过 `scripts/run.py` 提供统一 CLI 入口；不转发、不调用当前项目已有 API 服务，也不导入当前项目 `app.*` 模块。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理审核所需的病案文书、诊断编码和诊断名称。
- **严格脱敏**：调用方应在传入前完成姓名、证件号、手机号、详细地址等可识别身份信息的脱敏。
- **不做本地持久化**：本技能不把请求体、中间结果或审核结果写入本地文件或数据库。
- **规则库服务用途**：规则库 API 仅用于读取诊断依据充分性审核指南。
- **模型调用说明**：默认使用内部医疗大模型生成依据充分性判断；鉴权 `appkey` 必须由调用方传入。如需完全离线规则回退，可传 `use_llm=false`。
- **医疗边界**：输出为医保编码审核辅助信息，不构成医疗诊断或治疗建议。

输入格式
--------
统一入口支持 `pdf/doc/docx/xls/xlsx/csv/txt/json`。JSON 可为结构化病案；其他格式会先预处理为一份完整病历文书。未显式传入 `diagnoses` 时，会自动审核结构化病案中的主诊断和全部其他诊断；普通病历文件需要通过参数传入待审核诊断列表。

```json
{
  "record": {
    "hospitalId": "988",
    "serialNum": "0001092574",
    "docs": [
      {
        "docName": "首次病程记录",
        "fileName": "首次病程记录",
        "docClassName": "首次病程记录",
        "content": "..."
      }
    ],
    "diagnosis": {
      "primaryDiagnosis": {"name": "2型糖尿病", "code": "E11.901"},
      "otherDiagnoses": []
    }
  },
  "diagnoses": [
    {"role": "primary", "code": "E11.901", "name": "2型糖尿病"}
  ],
  "appkey": "由平台分配的鉴权 key",
  "model": "",
  "use_llm": true
}
```

字段说明：
- `record`：**必填**。结构化病案 JSON。
- `diagnoses`：可选。待审核诊断候选数组；每项包含 `role`、`code`、`name`。
- `role`：`primary` 表示主诊断；其他值按其他诊断处理。
- `appkey`：**必填**。内部医疗大模型鉴权 key，由平台分配；调用时使用 Bearer 鉴权。
- `model`：可选。内部医疗大模型名称，默认 `u1-insuremed`。
- `use_llm`：可选，默认 `true`。传 `false` 时不调用模型，仅使用本地回退审核逻辑。

审核规则
--------
- **候选优先**：只审核输入候选或病案首页中已有诊断，不自由生成候选列表外的诊断名称或编码。
- **证据优先**：依据充分必须来自病程、出院记录、检查检验、治疗经过等病历文书明确支持；不能把病案首页诊断列表本身当作充分临床依据。
- **主诊断边界**：主诊断应体现本次住院主要诊疗原因、主要资源消耗或核心治疗目标；仅有既往史、伴随疾病或偶然检出，不能自动视为主诊断依据充分。
- **其他诊断边界**：其他诊断应有明确并存、影响检查治疗、用药、护理、病情评估或资源消耗的证据；仅名称出现时需保守。
- **父类/子类边界**：父类诊断证据不能自动证明子类分型、并发症、部位、病因成立；缺少细分证据时输出 `待人工复核` 或 `依据不充分`。
- **同义词/简称边界**：仅当简称、同义词与候选诊断在医学内涵和编码归类上明确一致时可作为证据。
- **模糊保守**：疑似、待排、排除、术前诊断未证实、既往史、家族史、患者自述未被医生确认等，不应直接判为依据充分。
- **DRG/CC 边界**：严重合并症或并发症、一般合并症或并发症、无合并症或并发症的边界必须由病历明确支持；不能用模型常识或编码父类自动升级。

快速开始
--------

```bash
# JSON 结构化病历；未显式传入候选时审核主诊断和全部其他诊断
python3 doctor/icd-drg/diagnosis-sufficiency-review/scripts/run.py \
  --input doctor/icd-drg/diagnosis-sufficiency-review/example/10109_A5204171_1.json \
  --appkey <your-appkey> \
  --no-llm

# TXT/PDF 等普通病历文件；必须传入待审核诊断，可重复传入主诊断和其他诊断
python3 doctor/icd-drg/diagnosis-sufficiency-review/scripts/run.py \
  --input /path/to/record.txt \
  --appkey <your-appkey> \
  --diagnosis 'primary|E11.901|2型糖尿病' \
  --diagnosis 'other|I10.x00|高血压' \
  --save-prepared
```

参数说明
--------
- `--input PATH`：**必填**。结构化病案 JSON，或包含 `record` 的请求体 JSON。
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型，默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码，默认 `utf-8`。
- `--diagnosis STRING`：待审核诊断，格式 `role|code|name` 或 `code|name`；可重复。
- `--diagnoses-json STRING`：待审核诊断 JSON 字符串或文件路径。
- 普通 `txt/pdf/doc/docx/xls/xlsx/csv` 文件不会自动知道待审核诊断，必须传 `--diagnosis` 或 `--diagnoses-json`。
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由平台分配；调用时使用 Bearer 鉴权。
- `--base URL`：内部大模型 base URL，默认 `https://maas-api.hivoice.cn/v1`。
- `--model STRING`：模型名称，默认 `u1-insuremed`。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待，默认 `0`。
- `--no-llm`：可选。禁用 LLM，仅使用本地回退逻辑。
- `--output-json PATH`：可选。保存响应 JSON；同时传 `--output` 时优先使用该参数。
- `--output PATH`：可选。兼容旧调用方式，等同于 `--output-json`。
- `--save-prepared`：可选。保存预处理后的病历文本到 `doctor/icd-drg/runs/diagnosis-sufficiency-review/` 或输出文件所在目录；路径提示输出到 stderr。

输出约定
--------
CLI 只输出 JSON，不输出 Markdown、序号或额外提示语。响应结构：

```json
{
  "final_decision": "依据充分",
  "reasoning": "E11.901 2型糖尿病：依据充分。病历文书存在可支撑该诊断的明确临床依据。"
}
```

`final_decision` 只能为 `依据充分`、`依据不充分`、`待人工复核`。`reasoning` 只写面向用户的简洁依据，不展示内部 chain-of-thought。

示例
----
- 正例：候选主诊断 `E11.901 2型糖尿病`，病程记录、检验结果和治疗经过均支持本次住院围绕糖尿病诊疗，可输出 `依据充分`。
- 正例：候选其他诊断有明确检查结果、用药或治疗调整，且影响本次诊疗，可输出 `依据充分`。
- 多项审核例：结构化病案包含 `primaryDiagnosis` 和多个 `otherDiagnoses` 时，未传 `--diagnosis` 也会审核主诊断和全部其他诊断；普通文件需用多个 `--diagnosis` 显式列出。
- 边界例：文书只支持糖尿病父类诊断，未明确候选子类所需并发症或分型，应输出 `待人工复核`。
- 不应匹配例：仅病案首页诊断列表出现候选名称，正文无症状、检查、治疗或病程依据，不应直接判为依据充分。

依赖
----
### 运行环境
- Python 3.11+

### 外部服务
- ICD/DRG 规则库 API：读取诊断依据充分性审核指南。
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

测试命令
--------
从 `skills` 根目录执行：

```bash
python3 self_tests/med-icd-drg-review/self_test_icd_drg_review.py
```

备注
----
- 规则库访问必须通过环境变量配置：`GUIDELINE_API_BASE`；如平台启用鉴权，可配置 `GUIDELINE_API_KEY`。
- `scripts/run.py` 是唯一对外入口，复用 `scripts/diagnosis_sufficiency_review.py` 的核心审核逻辑。
- LLM 鉴权 `appkey` 由用户在调用时传入，脚本不硬编码。
- 发布目录只保留 `SKILL.md`、`_meta.json`、`scripts/`；示例输入、运行输出、自测脚本放在 skill 包外。
