---
name: med-diagnosis-review
description: 诊断编码审核。输入结构化病案 record 与待审核诊断列表，输出诊断编码规则命中、病历证据和审核结论。
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺"
      }
  }
---

# 诊断编码审核

概述
----
给定结构化病案 `record` 和待审核诊断列表，本技能从诊断编码审核规则库读取规则，核对病历文书证据，输出诊断编码审核结果。

本技能会：
- 从 `diagnosis_audit_guidelines` 读取诊断编码审核规则。
- 优先按用户提供的 `diagnoses` 候选列表审核；未提供时，默认审核 `record.diagnosis.primaryDiagnosis` 和 `record.diagnosis.otherDiagnoses` 中的全部诊断。
- 调用 skill 内置的 `review_diagnosis_record` function 完成审核。
- 通过 `scripts/run.py` 提供统一 CLI 入口；不转发、不调用当前项目已有 API 服务，也不导入当前项目 `app.*` 模块。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理审核所需的病案文书、诊断编码和诊断名称。
- **严格脱敏**：调用方应在传入前完成姓名、证件号、手机号、详细地址等可识别身份信息的脱敏。
- **不做本地持久化**：本技能不把请求体、中间结果或审核结果写入本地文件或数据库。
- **规则库服务用途**：规则库 API 仅用于读取诊断编码审核规则。
- **模型调用说明**：默认使用内部医疗大模型生成审核说明；鉴权 `appkey` 必须由调用方传入。如需完全离线规则回退，可传 `use_llm=false`。
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
        "docName": "出院记录",
        "fileName": "出院记录",
        "docClassName": "出院记录",
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
- **医学内涵优先**：匹配依据以医学内涵、医保目录归类、编码规则和诊疗目的为准，不能只看字面相似。
- **证据优先**：审核结论必须基于病历文书明确支持的信息；不能把病历中未明确支持的信息当作事实。
- **角色边界**：主诊断优先核对本次住院主要诊疗原因；其他诊断核对是否有明确并存、影响诊疗或资源消耗的依据。
- **父类/子类边界**：编码可按规则库从细到粗检索，但父类规则不能自动证明子类编码成立；细分部位、病因、并发症、分型不明确时应输出 `待人工复核`。
- **同义词/简称边界**：仅当简称、同义词与候选诊断在医学内涵和编码归类上明确一致时可视为匹配。
- **模糊保守**：字面相似但医学内涵不同、疑似/排除诊断、仅有既往史或家族史、缺少直接证据时，不强行通过。
- **DRG/CC 边界**：涉及 DRG 分组或严重合并症/并发症、一般合并症/并发症、无合并症/并发症判断时，必须有病历明确支持；不能用模型常识自动升级。

快速开始
--------

```bash
# JSON 结构化病历；未显式传入候选时审核主诊断和全部其他诊断
python3 doctor/icd-drg/diagnosis-review/scripts/run.py \
  --input doctor/icd-drg/diagnosis-review/example/10109_A5204171_1.json \
  --appkey <your-appkey> \
  --no-llm

# TXT/PDF 等普通病历文件；必须传入待审核诊断，可重复传入主诊断和其他诊断
python3 doctor/icd-drg/diagnosis-review/scripts/run.py \
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
- `--save-prepared`：可选。保存预处理后的病历文本到 `doctor/icd-drg/runs/diagnosis-review/` 或输出文件所在目录；路径提示输出到 stderr。

输出约定
--------
CLI 只输出 JSON，不输出 Markdown、序号或额外提示语。响应结构：

```json
{
  "final_decision": "通过",
  "reasoning": "E11.901 2型糖尿病：通过。病历文书存在可支撑该诊断编码的明确依据。"
}
```

`final_decision` 只能为 `通过`、`不通过`、`待人工复核`。`reasoning` 只写面向用户的简洁依据，不展示内部 chain-of-thought。

示例
----
- 正例：候选 `E11.901 2型糖尿病`，出院记录和检验记录明确记载 2 型糖尿病及相关诊疗依据，可输出 `通过`。
- 正例：候选主诊断与规则库编码精确命中，入院记录、首次病程记录和出院记录均支持本次住院主要诊疗原因，可输出 `通过`。
- 多项审核例：结构化病案包含 `primaryDiagnosis` 和多个 `otherDiagnoses` 时，未传 `--diagnosis` 也会审核主诊断和全部其他诊断；普通文件需用多个 `--diagnosis` 显式列出。
- 边界例：候选为细分子类编码，但文书只支持父类诊断，未明确分型、部位或并发症，应输出 `待人工复核`。
- 不应匹配例：候选名称与文书关键词字面相似，但医学内涵不同，或仅见“排除/疑似/既往史”，不得强行通过，应输出 `不通过` 或 `待人工复核`。

依赖
----
### 运行环境
- Python 3.11+

### 外部服务
- ICD/DRG 规则库 API：读取诊断编码审核规则。
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
- `scripts/run.py` 是唯一对外入口，复用 `scripts/diagnosis_review.py` 的核心审核逻辑。
- LLM 鉴权 `appkey` 由用户在调用时传入，脚本不硬编码。
- 发布目录只保留 `SKILL.md`、`_meta.json`、`scripts/`；示例输入、运行输出、自测脚本放在 skill 包外。
