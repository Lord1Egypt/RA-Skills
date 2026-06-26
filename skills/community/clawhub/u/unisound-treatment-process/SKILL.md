---
name: med-treatment-process-gen
description: 根据病程记录生成诊疗经过。输入病程记录文本，调用内部医疗大模型，输出结构化诊疗经过文本。
metadata:
  {
    "openclaw":
      {
        "emoji": "📝"
      }
  }
---

# 诊疗经过生成

概述
----
根据患者的**病程记录**文本（包括首次病程、日常病程、查房记录等），本技能调用内部医疗大模型生成一份结构化、连贯的**诊疗经过**文本。

诊疗经过用于病历归档、病历首页填写、病案统计等场景，需要对住院期间的诊疗过程进行系统性总结。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理生成诊疗经过所需的病程记录内容；不要求也不鼓励包含姓名、证件号、手机号、详细地址等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，请确保病程记录已完成脱敏/去标识化处理。
- **不做本地持久化**：不将输入与中间结果写入本地持久化存储；**本次调用结束即销毁**。
- **医疗边界**：本技能用于诊疗经过文本整理与结构化表达的辅助生成，不构成医疗诊断或治疗建议；请由执业医生复核并承担最终医疗责任。

输入格式
--------
统一入口支持 `pdf/doc/docx/xls/xlsx/csv/txt/json`。JSON 可包含病程字段；普通病历文件会先预处理为文本。

### JSON 输入示例

```json
{
  "records": [
    {
      "title": "首次病程记录",
      "time": "2023-3-21 15:01:00",
      "content": "诊疗计划\n1、病情及护理注意事项：清淡软食，避免劳累\n2、检查计划：完善相关检查\n3、治疗计划：暂给予保肝、营养等对症治疗\n4、请上级医师指导诊疗。"
    },
    {
      "title": "日常病程记录",
      "time": "2023-3-22 10:10:00",
      "content": "患者一般情况尚可，无明显不适主诉。\n查体：生命体征平稳，慢性肝病面容，腹平软，无压痛及反跳痛..."
    }
  ]
}
```

也支持直接传入完整 prompt：

```json
{
  "prompt": "根据病历生成诊疗经过\n\n输入：\n[完整病程记录文本]\n\n输出："
}
```

### 普通文本输入

对于 TXT/PDF/DOC 等格式的病程记录文件，文件内容会被预处理为纯文本，然后通过命令行参数传入。

快速开始
--------

```bash
python doctor/emr-gen/treatment-process/scripts/run.py \
  --input data/med-treatment-process/gen_records.json \
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
- `--output PATH`：可选。输出诊疗经过文本文件路径。
- `--save-prepared`：可选。保存预处理后的文本，便于调试。

输出约定
--------
- 输出为 UTF-8 文本，格式示例：

```
患者于 2023-3-21 至 2023-3-31 在我院住院治疗。入院后完善相关检查，网织红细胞 + 全血细胞分析 (含有核红):白细胞计数 3.45×10^9/L，血红蛋白 141g/L，血小板计数 77×10^9/L；凝血项 I:凝血酶原活动度 HSPT% 62.4%↓，纤维蛋白原含量 1.85g/L↓；血氨 60μg/dl↑。

入院后给予异甘草酸酶及水飞蓟宾保肝、营养等对症治疗。住院期间 Fibroscan 示 27kPa，腹水彩超未见腹腔积液。2023-03-29 于病房行放血治疗，全程心电监测、氧气吸入，护士给予肘正中静脉穿刺，全程持续 30 分钟，共放出静脉血 350ml，过程顺利，患者无特殊不适反应。后复查胃镜提示食管静脉显露，腹部增强 CT 提示肝脏、胰腺、脾脏均可见铁沉积。经治疗后患者目前病情平稳，准予出院。
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
python self_tests/med-treatment-process-gen/self_test_treatment_process_gen.py

# 在线自测（调用内部接口）
python self_tests/med-treatment-process-gen/self_test_treatment_process_gen.py --run-network
```

备注
----
- `scripts/run.py` 是唯一对外入口。
- 示例输入放在 `example/gen_records.json`。
