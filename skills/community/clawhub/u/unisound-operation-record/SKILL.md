---
name: med-operation-record-gen
description: 根据手术相关病历素材生成规范的手术记录。输入术前小结、术中记录、术后记录等，调用内部医疗大模型，输出结构化手术记录（含手术日期、时间、地点、医生、手术名称、指征、诊断、经过、异常情况、术后情况、签名等 14 个字段）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔪"
      }
  }
---

# 手术记录生成

概述
----
根据患者的**手术相关病历素材**（包括术前小结、术中记录、术后即刻记录等），本技能调用内部医疗大模型生成一份规范、完整、专业的**手术记录**。

手术记录是手术科室病历的核心组成部分，用于病案归档、医疗纠纷举证、手术质量评价等场景。生成内容需严格遵循临床手术记录书写标准，完全忠于原文。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理生成手术记录所需的手术病历内容；不要求也不鼓励包含姓名、证件号、手机号、详细地址等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，请确保手术病历已完成脱敏/去标识化处理。
- **不做本地持久化**：不将输入与中间结果写入本地持久化存储；**本次调用结束即销毁**。
- **医疗边界**：本技能用于手术记录文本整理与结构化表达的辅助生成，不构成医疗诊断或治疗建议；请由执业医生复核并承担最终医疗责任。

输入格式
--------
统一入口支持 `pdf/doc/docx/xls/xlsx/csv/txt/json`。JSON 可包含结构化手术病历字段；普通病历文件会先预处理为文本。

### JSON 输入示例

```json
{
  "records": [
    {
      "section": "术前小结",
      "content": "患者，男性，62 岁，因'反复右上腹疼痛 1 年，加重 1 周'入院。术前诊断：胆囊结石伴慢性胆囊炎。患者反复右上腹隐痛，进食油腻食物后加重..."
    },
    {
      "section": "术中记录",
      "content": "患者于 2026 年 5 月 10 日 9:00 进入手术室 2 号间，全身麻醉生效后，取仰卧位，常规消毒腹部皮肤，铺无菌巾。在脐上缘做一 1cm 切口..."
    },
    {
      "section": "术后即刻记录",
      "content": "患者手术结束后，麻醉苏醒顺利，生命体征平稳（体温 36.8℃，脉搏 78 次/分，呼吸 18 次/分，血压 135/85mmHg）..."
    }
  ]
}
```

也支持直接传入完整 prompt：

```json
{
  "prompt": "请你作为临床外科病历书写专家，严格依据提供的患者手术相关病历素材，生成一份规范、完整、专业的手术记录...\n\n患者手术相关病历\n#### 术前小结\n...\n"
}
```

### 普通文本输入

对于 TXT/PDF/DOC 等格式的手术病历文件，文件内容会被预处理为纯文本，然后通过命令行参数传入。

快速开始
--------

```bash
python doctor/emr-gen/operation-record/scripts/run.py \
  --input data/med-operation-record/gen_records.json \
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
- `--output PATH`：可选。输出手术记录文本文件路径。
- `--save-prepared`：可选。保存预处理后的文本，便于调试。

输出约定
--------
- 输出为 UTF-8 文本，按顺序包含 14 个标准字段：手术日期、手术时间、手术地点、手术医生、助手、麻醉方式、手术名称、手术指征、术前诊断、术中诊断、手术经过、术中出现的情况及处理、术后情况、手术者签名。
- 格式示例（字段值从输入病历抽取，勿编造）：

```text
# 手术记录
1. 手术日期：…
2. 手术时间：…
…
11. 手术经过：按操作顺序叙述消毒、切口、探查、切除、止血、缝合等关键步骤
…
14. 手术者签名：…
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
python self_tests/med-operation-record-gen/self_test_operation_record_gen.py

# 在线自测（调用内部接口）
python self_tests/med-operation-record-gen/self_test_operation_record_gen.py --run-network
```

备注
----
- `scripts/run.py` 是唯一对外入口。
- 示例输入放在 `example/gen_records.json`。
