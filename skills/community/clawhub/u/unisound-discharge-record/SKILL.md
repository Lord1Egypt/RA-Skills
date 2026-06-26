---
name: med-discharge-record-gen
description: 根据住院病历生成标准出院记录。输入入院记录、病程记录等，调用内部医疗大模型，输出结构化出院记录（含主诉、入院情况、入院诊断、诊疗经过、出院诊断、出院情况、出院医嘱七个字段）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📝"
      }
  }
---

# 出院记录生成

概述
----
根据患者的完整**住院病历**（包括入院记录、首次病程、日常病程、末次病程等），本技能调用内部医疗大模型生成一份标准化的**出院记录**。

出院记录是病历首页的重要组成，用于病案归档、医保结算、转诊交接等场景。生成内容需严格遵循 7 个字段规范，完全忠于原文。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理生成出院记录所需的病历内容；不要求也不鼓励包含姓名、证件号、手机号、详细地址等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，请确保病历已完成脱敏/去标识化处理。
- **不做本地持久化**：不将输入与中间结果写入本地持久化存储；**本次调用结束即销毁**。
- **医疗边界**：本技能用于出院记录文本整理与结构化表达的辅助生成，不构成医疗诊断或治疗建议；请由执业医生复核并承担最终医疗责任。

输入格式
--------
统一入口支持 `pdf/doc/docx/xls/xlsx/csv/txt/json`。JSON 可包含结构化病历字段；普通病历文件会先预处理为文本。

### JSON 输入示例

```json
{
  "records": [
    {
      "section": "入院记录",
      "title": "主诉",
      "content": "反复咳嗽咳痰 5 年，加重伴胸闷气喘 3 天。"
    },
    {
      "section": "入院记录",
      "title": "既往史",
      "content": "有高血压病史 8 年，最高血压 165/95mmHg，长期口服降压药；否认糖尿病、冠心病史。"
    },
    {
      "section": "首次病程记录",
      "title": "病例特点",
      "content": "老年男性，5 年反复咳嗽咳痰病史，3 天前受凉后症状加重..."
    },
    {
      "section": "日常病程记录",
      "title": "",
      "content": "入院后予吸氧、抗感染、止咳化痰、控制血压对症支持治疗..."
    },
    {
      "section": "末次病程记录",
      "title": "",
      "content": "患者目前无明显胸闷气喘，偶有轻微咳嗽咳痰..."
    }
  ]
}
```

也支持直接传入完整病历文本：

```json
{
  "prompt": "你作为专业医疗病历整理专家，严格依据给定住院病历原文，按照固定规则生成标准出院记录...\n\n### 患者原始病历文本\n#### 入院记录\n...\n",
}
```

### 普通文本输入

对于 TXT/PDF/DOC 等格式的完整病历文件，文件内容会被预处理为纯文本，然后通过命令行参数传入。

快速开始
--------

```bash
# JSON 结构化输入
python doctor/emr-gen/discharge-record/scripts/run.py \
  --input data/med-discharge-record/gen_records.json \
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
- `--output PATH`：可选。输出出院记录文本文件路径。
- `--save-prepared`：可选。保存预处理后的文本，便于调试。

输出约定
--------
- 输出为 UTF-8 文本，包含以下 7 个标准字段：

```
# 出院记录
### 1. 主诉
反复咳嗽咳痰 5 年，加重伴胸闷气喘 3 天。

### 2. 入院情况
患者老年男性，有 5 年反复咳嗽咳痰病史，本次因受凉后症状加重，伴胸闷、活动后气喘入院。既往有高血压病史 8 年，最高血压 165/95mmHg，长期口服降压药物，否认糖尿病、冠心病史，无家族遗传病史。查体示双肺呼吸音粗，可闻及散在湿性啰音，心律齐，腹部查体无异常阳性体征。

### 3. 入院诊断
慢性阻塞性肺疾病急性加重；高血压病 2 级（很高危）。

### 4. 诊疗经过
患者入院后予以吸氧、抗感染、止咳化痰、控制血压等对症支持治疗。住院期间完善相关检查，血常规及胸部 CT 提示肺部炎症明显；入院第 3 天患者咳嗽咳痰症状较前减轻，胸闷气喘症状明显缓解，病情逐渐平稳，继续维持原治疗方案巩固治疗。住院期间无手术及特殊介入检查操作。

### 5. 出院诊断
慢性阻塞性肺疾病急性加重；高血压病 2 级（很高危）。

### 6. 出院情况
患者出院时无明显胸闷气喘，仅偶有轻微咳嗽咳痰，生命体征平稳，双肺湿性啰音较入院时明显减少，整体病情控制稳定，达到出院标准。

### 7. 出院医嘱
1. 出院后规律服用降压药物及止咳化痰药物；
2. 1 周后至呼吸内科门诊复查血常规、胸部 CT；
3. 日常生活保持低盐低脂饮食，避免受凉、过度劳累；
4. 居家适当进行呼吸功能康复锻炼；
5. 若出现胸闷气喘加重、发热等不适症状，及时前往医院就诊。
```

- 若输出路径父目录不存在，会自动创建。

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
python self_tests/med-discharge-record-gen/self_test_discharge_record_gen.py

# 在线自测（调用内部接口）
python self_tests/med-discharge-record-gen/self_test_discharge_record_gen.py --run-network
```

备注
----
- `scripts/run.py` 是唯一对外入口。
- 示例输入放在 `example/gen_records.json`。
