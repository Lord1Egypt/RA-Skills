---
name: med-surgery-review
description: 手术/操作编码审核。输入结构化病案 record 与待审核手术/操作列表，输出编码规则命中、病历证据和审核结论。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏥"
      }
  }
---

# 手术/操作编码审核

概述
----
给定结构化病案 `record` 和待审核手术/操作列表，本技能从手术编码审核规则库读取规则，核对病历文书证据，输出手术/操作编码审核结果。

本技能会：
- 从 `surgery_audit_guidelines` 读取手术/操作编码审核规则。
- 优先按用户提供的 `surgeries` 候选列表审核；未提供时，默认审核 `record.surgery.primarySurgery` 和 `record.surgery.otherSurgeries` 中的全部手术/操作。
- 调用 skill 内置的 `review_surgery_record` function 完成审核。
- 通过 `scripts/run.py` 提供统一 CLI 入口；不转发、不调用当前项目已有 API 服务，也不导入当前项目 `app.*` 模块。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理审核所需的病案文书、手术/操作编码和名称。
- **严格脱敏**：调用方应在传入前完成姓名、证件号、手机号、详细地址等可识别身份信息的脱敏。
- **不做本地持久化**：本技能不把请求体、中间结果或审核结果写入本地文件或数据库。
- **规则库服务用途**：规则库 API 仅用于读取手术/操作编码审核规则。
- **模型调用说明**：默认使用内部医疗大模型生成审核说明；鉴权 `appkey` 必须由调用方传入。如需完全离线规则回退，可传 `use_llm=false`。
- **医疗边界**：输出为医保编码审核辅助信息，不构成医疗诊断或治疗建议。

输入格式
--------
统一入口支持 `pdf/doc/docx/xls/xlsx/csv/txt/json`。JSON 可为结构化病案；其他格式会先预处理为一份完整病历文书。未显式传入 `surgeries` 时，会自动审核结构化病案中的主手术/操作和全部其他手术/操作；普通病历文件需要通过参数传入待审核手术/操作列表。

```json
{
  "record": {
    "hospitalId": "988",
    "serialNum": "0001861856",
    "docs": [
      {
        "docName": "手术记录",
        "fileName": "手术记录",
        "docClassName": "手术记录",
        "content": "..."
      }
    ],
    "surgery": {
      "primarySurgery": {"name": "阑尾切除术", "code": "47.0101"},
      "otherSurgeries": []
    }
  },
  "surgeries": [
    {"role": "primary", "code": "47.0101", "name": "阑尾切除术"}
  ],
  "appkey": "由平台分配的鉴权 key",
  "model": "",
  "use_llm": true
}
```

字段说明：
- `record`：**必填**。结构化病案 JSON。
- `surgeries`：可选。待审核手术/操作候选数组；每项包含 `role`、`code`、`name`。
- `role`：`primary` 表示主要手术/操作；其他值按其他手术/操作处理。
- `appkey`：**必填**。内部医疗大模型鉴权 key，由平台分配；调用时使用 Bearer 鉴权。
- `model`：可选。内部医疗大模型名称，默认 `u1-insuremed`。
- `use_llm`：可选，默认 `true`。传 `false` 时不调用模型，仅使用本地回退审核逻辑。

审核规则
--------
- **候选优先**：只审核输入候选或病案首页中已有手术/操作，不自由生成候选列表外的名称或编码。
- **核心用途优先**：匹配依据以手术/操作的医学内涵、医保目录归类、编码规则、诊疗目的、服务/耗材核心用途为准，不能只看字面相似。
- **证据优先**：审核结论必须基于手术记录、术后首次病程记录、出院记录等文书明确支持的信息。
- **角色边界**：主要手术/操作优先核对与本次住院主要治疗目的、资源消耗和病案首页主要手术选择一致性；其他手术/操作核对是否有明确实施证据。
- **父类/子类边界**：编码可按规则库从细到粗检索，但父类规则不能自动证明子类编码成立；入路、部位、器械、范围、术式细节不明确时应输出 `待人工复核`。
- **组套项目边界**：组套名称不能自动拆成多个操作；一项操作也不能自动扩展为组套，除非文书逐项明确记录。
- **一对一/一对多边界**：候选只支持一个明确操作时，不推断相关附加操作；多个候选共享同一证据时，应分别核对是否均有实施记录。
- **模糊保守**：字面相似但核心用途不同、仅有术前计划、拟行操作、取消操作或缺少实施记录时，不强行通过。
- **DRG 边界**：涉及 DRG 分组或手术级别影响时，必须有病历明确支持；不能用模型常识自动升级主要手术。

快速开始
--------

```bash
# JSON 结构化病历；未显式传入候选时审核主手术和全部其他手术
python3 doctor/icd-drg/surgery-review/scripts/run.py \
  --input doctor/icd-drg/surgery-review/example/10110_48738508.json \
  --appkey <your-appkey> \
  --no-llm

# TXT/PDF 等普通病历文件；必须传入待审核手术/操作，可重复传入主手术和其他手术
python3 doctor/icd-drg/surgery-review/scripts/run.py \
  --input /path/to/record.txt \
  --appkey <your-appkey> \
  --surgery 'primary|32.4100x002|胸腔镜下肺叶切除术' \
  --surgery 'other|34.5100x001|胸腔镜下胸腔粘连松解术' \
  --save-prepared
```

参数说明
--------
- `--input PATH`：**必填**。结构化病案 JSON，或包含 `record` 的请求体 JSON。
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型，默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码，默认 `utf-8`。
- `--surgery STRING`：待审核手术/操作，格式 `role|code|name` 或 `code|name`；可重复。
- `--surgeries-json STRING`：待审核手术/操作 JSON 字符串或文件路径。
- 普通 `txt/pdf/doc/docx/xls/xlsx/csv` 文件不会自动知道待审核手术/操作，必须传 `--surgery` 或 `--surgeries-json`。
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，由平台分配；调用时使用 Bearer 鉴权。
- `--base URL`：内部大模型 base URL，默认 `https://maas-api.hivoice.cn/v1`。
- `--model STRING`：模型名称，默认 `u1-insuremed`。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待，默认 `0`。
- `--no-llm`：可选。禁用 LLM，仅使用本地回退逻辑。
- `--output-json PATH`：可选。保存响应 JSON；同时传 `--output` 时优先使用该参数。
- `--output PATH`：可选。兼容旧调用方式，等同于 `--output-json`。
- `--save-prepared`：可选。保存预处理后的病历文本到 `doctor/icd-drg/runs/surgery-review/` 或输出文件所在目录；路径提示输出到 stderr。

输出约定
--------
CLI 只输出 JSON，不输出 Markdown、序号或额外提示语。响应结构：

```json
{
  "final_decision": "通过",
  "reasoning": "47.0101 阑尾切除术：通过。病历文书存在可支撑该手术/操作编码的明确依据。"
}
```

`final_decision` 只能为 `通过`、`不通过`、`待人工复核`。`reasoning` 只写面向用户的简洁依据，不展示内部 chain-of-thought。

示例
----
- 正例：候选 `47.0101 阑尾切除术`，手术记录明确记载已实施阑尾切除术，可输出 `通过`。
- 正例：候选主要手术与规则库编码精确命中，手术记录和出院记录均支持本次住院主要治疗操作，可输出 `通过`。
- 多项审核例：结构化病案包含 `primarySurgery` 和多个 `otherSurgeries` 时，未传 `--surgery` 也会审核主手术和全部其他手术；普通文件需用多个 `--surgery` 显式列出。
- 边界例：候选为更细子类编码，但文书只记载父类术式，未明确入路、部位、器械或范围，应输出 `待人工复核`。
- 不应匹配例：候选名称与文书操作字面相似，但服务/耗材核心用途不同，或仅见“拟行/计划/取消”，不得强行通过。

依赖
----
### 运行环境
- Python 3.11+

### 外部服务
- ICD/DRG 规则库 API：读取手术/操作编码审核规则。
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
- `scripts/run.py` 是唯一对外入口，复用 `scripts/surgery_review.py` 的核心审核逻辑。
- LLM 鉴权 `appkey` 由用户在调用时传入，脚本不硬编码。
- 发布目录只保留 `SKILL.md`、`_meta.json`、`scripts/`；示例输入、运行输出、自测脚本放在 skill 包外。
