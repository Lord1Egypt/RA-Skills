---
name: med-followup-record-struct
description: 将中文门诊复诊病历文本结构化为细粒度字段，输出 JSON（如现病史/既往史/诊断/处理意见等）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧩"
      }
  }
---

# 门诊复诊病历结构化

概述
----
给定一份中文门诊 **复诊病历文本**（医生已书写），本技能抽取并规范化为细粒度字段 JSON，例如：

- 现病史.病情概述
- 现病史.药物
- 现病史.其他治疗措施
- 现病史.病情转归
- 现病史.一般情况
- 既往史.疾病
- 既往史.其他信息
- 既往史.手术史
- 既往史.过敏史
- 既往史.输血史
- 婚育史
- 月经史
- 个人史
- 家族史
- 查体
- 辅助检查
- 诊断
- 处理意见.药物
- 处理意见.其他建议

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理结构化抽取所必需的文本内容；不要求也不鼓励包含姓名、证件号、手机号、详细地址等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理（如姓名、证件号、手机号、详细地址、人脸/影像等）。仅传递脱敏后的必要信息用于本次 skill 调用。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储（包含磁盘文件、数据库、日志）。仅在内存中短暂处理；**本次调用结束即销毁**。
- **第三方 API 风险提示**：在功能需要时，可能会调用第三方模型/服务接口；此时仅会发送**脱敏后的必要信息**，并使用加密传输。除完成本次请求外，不用于任何其他用途（如训练、画像、营销）。
- **医疗边界**：本技能输出为文本抽取与结构化结果，不构成医疗诊断或治疗建议；如涉及临床判断请以执业医生意见为准。


输入格式
--------
纯文本病历（UTF-8），可包含如下分段：

主诉：……
现病史：……
既往史：……
婚育史：……
月经史：……
个人史：……
家族史：……
查体：……
辅助检查：……
诊断：……
处理：……

也支持通过统一入口 `scripts/run.py` 直接输入 `pdf/doc/docx/xls/xlsx/csv/txt/json`。
预处理成功后，会先归一化为标准复诊病历文本，再调用本 skill 的原始结构化逻辑。

快速开始
--------

```bash
# JSON 结构化输入
python doctor/emr-gen/followup-record/scripts/run.py \
  --input data/med-followup-record/gen_records.json \
  --appkey <your-appkey>

# 普通病历文件（纯文本）
python doctor/emr-gen/followup-record/scripts/run.py \
  --input data/med-followup-record/record.txt \
  --appkey <your-appkey>
```

参数说明
--------
- `--input PATH`：**必填**。输入 JSON 文件或病历文本文件路径。
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型，默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码，默认 `utf-8`。
- `--base URL`：内部大模型 base URL，默认 `https://maas-api.hivoice.cn/v1`。
- `--model STRING`：模型名称，默认 `u1-insuremed`。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待，默认 `0`。
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key，使用 Bearer 方式认证。
- `--output-json PATH`：可选。保存输出 JSON。
- `--output PATH`：可选：输出病历文本文件路径。
- `--save-prepared`：可选：保存预处理后的文本，便于调试。

输出约定
--------
- 输出为 UTF-8 文本，每行格式：`字段：值`
- 如果某个字段在原文中没有对应内容，返回 `未提及`
- 标准化表达：如无过敏史、无手术史等统一简化为 `无`


依赖
----
### 前置 Skill

`scripts/run.py` 依赖 **`_shared/doc-preprocess`** 提供的公共文件预处理库（`preprocess.py`）。
请确保 `_shared/doc-preprocess/` 位于 `skills/` 根目录下。

### 运行环境

- Python 3.7+

### 外部 API

- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`
  - 方法：POST，OpenAI 兼容格式
  - 需要传入 `--appkey` 参数进行 Bearer 认证

### Python 第三方包（可选，run.py 使用非 txt/json 输入时需要）

| 包名 | 用途 | 必要条件 |
|------|------|---------|
| `openpyxl` | 读取 `.xlsx` 文件 | 输入为 xlsx 时必须 |
| `pypdf` | 提取 PDF 文本 | 输入为 pdf 时必须 |

安装：`pip install openpyxl pypdf`

> 仅使用 TXT/JSON 输入时，无需安装任何额外包。

测试命令
--------
从 `skills` 根目录执行：

```bash
# 离线自测（检查输入和构造请求）
python self_tests/med-followup-record-gen/self_test_followup_record_gen.py

# 在线自测（调用内部接口）
python self_tests/med-followup-record-gen/self_test_followup_record_gen.py --run-network
```
