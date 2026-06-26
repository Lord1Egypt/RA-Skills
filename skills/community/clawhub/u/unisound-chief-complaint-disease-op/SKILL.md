---
name: med-emr-qc-chief-complaint-disease-op
description: 门诊病历内涵质控：主诉不应使用疾病和操作。给定门诊病历文本，调用内部医疗大模型，输出无缺陷或有缺陷及原因。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍"
      }
  }
---

# 主诉不应使用疾病和操作

概述
----
本 skill 仅针对**「主诉不应使用疾病和操作」**这一条内涵质控规则。将字段解析、多步 LLM 推理与条件分支实现在本目录 `scripts/emr_qc_impl.py` 中；`scripts/emr_qc.py`、`scripts/run.py` 为入口，本 skill 可单独打包发布。调用 **HiVoice MaaS** 医疗大模型（OpenAI 兼容 `chat/completions`），输出 `无缺陷` 或 `有缺陷` + 原因。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理质控所必需的病历文本内容；不要求提供姓名、证件号等身份信息。
- **严格脱敏**：在发送至任何接口前，请确保病历文本已完成脱敏/去标识化处理。
- **不做本地持久化**：不将输入与中间结果写入本地持久化存储；**本次调用结束即销毁**。
- **医疗边界**：本技能为辅助质控工具，不构成医疗诊断或治疗建议；最终结论请由执业医生审核。

输入格式
--------
纯文本门诊病历（UTF-8），各字段用中文标签开头，例如：

```
主诉:发热3天
现病史:患者3天前无明显诱因出现发热，体温最高38.5℃...
既往史:高血压病史5年，规律服用氨氯地平，血压控制可...
体格检查:T 38.2℃，BP 150/90mmHg，双肺呼吸音清...
初步诊断:上呼吸道感染
处理意见:对症治疗
```

支持的字段标签：`主诉`、`现病史`、`既往史`、`体格检查`、`辅助检查`、`初步诊断`/`诊断`、`处理意见`/`处理`（中英文冒号均可）。

也支持通过 `scripts/run.py` 直接输入 `pdf/doc/docx/xls/xlsx/csv/txt/json`。

快速开始
--------

```bash
# 文本入口（在仓库 skills 根目录运行）
python3 doctor/emr-qc/chief-complaint-disease-op/scripts/emr_qc.py \
  --input data/med-emr-qc/record.txt \
  --appkey <your-appkey>

# 多格式入口
python3 doctor/emr-qc/chief-complaint-disease-op/scripts/run.py \
  --input data/med-emr-qc/record.xlsx \
  --appkey <your-appkey>
```

参数说明
--------

`scripts/emr_qc.py`：

- `--input PATH`：**必填**。门诊病历文本文件路径（UTF-8）。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配；**不得写入仓库**。
- `--base URL`：大模型 base URL（默认：`https://maas-api.hivoice.cn/v1`）。
- `--model STRING`：模型名称（默认：`u1-insuremed`）。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待（默认：0）。
- `--output PATH`：输出文件路径（默认：`../runs/med-emr-qc/chief-complaint-disease-op.txt`）。

`scripts/run.py` 附加参数：

- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型；默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码（默认：`utf-8`）。
- `--save-prepared`：保存预处理后的文本，便于调试。

输出约定
--------
- 输出为 UTF-8 文本：
  - 无缺陷：输出 `无缺陷`
  - 有缺陷：输出 `有缺陷` + 换行 + 原因说明

依赖
----

### 自包含实现
质控与 LLM 调用逻辑均在 `scripts/emr_qc_impl.py`（与同 skill 一并发布）。

### 预处理（仅 `run.py`）
`scripts/run.py` 依赖 **`_shared/doc-preprocess`**（`preprocess.py`），须位于仓库 `skills/` 根下。

### 运行环境
- Python 3.7+
- 无需第三方包（仅标准库；多格式输入时可选 `openpyxl`、`pypdf`）

### 外部 API
- 医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`（POST，OpenAI 兼容格式）
