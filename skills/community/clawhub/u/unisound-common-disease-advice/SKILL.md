---
name: clinic-common-disease-advice
description: 基层常见病诊疗建议。输入患者主诉/症状/体征文本，输出鉴别诊断（概率+依据）、推荐检查、初步处理意见及转诊判断（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏥"
      }
  }
---

# 基层常见病诊疗建议

概述
----
面向**社区诊所/基层卫生机构**医生，给定患者主诉、症状、体征及基本信息，本技能会：

- 给出鉴别诊断（最多3种，按可能性排序，含诊断依据）
- 推荐适合基层开展的检查项目
- 提供初步处理意见（药物建议优先国家基本药物 + 一般处理）
- 识别红旗症状并给出转诊判断

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理生成诊疗建议所必需的患者信息；不要求也不鼓励包含姓名、证件号、手机号、详细地址等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理。仅传递脱敏后的必要信息用于本次 skill 调用。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储。仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能输出为辅助诊疗建议，不构成医疗诊断或治疗决定；请由执业医生复核并承担最终医疗责任。

输入格式
--------
纯文本（UTF-8），包含患者基本信息和临床资料，例如：

```text
主诉：发热3天，咳嗽有黄痰
年龄：35岁，性别：男
既往史：无特殊
体格检查：T 38.5℃，双肺可闻及湿啰音
辅助检查：WBC 12.0×10⁹/L，中性粒细胞85%
```

也支持 JSON 格式（包含 `text`/`content`/`patient_info` 字段的对象，或直接为字符串）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/primary-care-assist/common-disease-advice/scripts/run.py \
  --input data/clinic-common-disease/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/primary-care-assist/common-disease-advice/scripts/run.py \
  --input data/clinic-common-disease/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-common-disease/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。患者信息文件路径（txt 或 json，UTF-8）。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。
- `--output PATH`：输出文件路径（默认：打印到 stdout）。
- `--base URL`：内部大模型 base URL（默认：`https://maas-api.hivoice.cn/v1`）。
- `--model STRING`：模型名称（默认：`u1-insuremed`）。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待（默认：0）。
- `--encoding STRING`：输入文件编码（默认：`utf-8`）。

输出约定
--------
输出分两部分：

**JSON 结构**：

```json
{
  "possible_diagnoses": [
    {
      "diagnosis": "社区获得性肺炎",
      "probability": "高",
      "basis": "发热、黄痰、双肺湿啰音、WBC升高"
    }
  ],
  "recommended_exams": ["胸部X线", "痰培养+药敏"],
  "treatment_advice": {
    "medication": "阿莫西林克拉维酸钾 457mg tid 口服，疗程7天",
    "general": "卧床休息，多饮水，监测体温，退热处理"
  },
  "warnings": ["如72小时内症状无改善或出现呼吸困难，需立即转诊"],
  "referral_needed": false,
  "referral_reason": null
}
```

**自然语言摘要**：以"【摘要】"开头，总结关键诊断和处理要点。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`
  - 方法：POST，OpenAI 兼容格式
  - 需要网络访问内部地址

备注
----
- 药物建议优先选用《国家基本药物目录》品种，并给出具体剂量和用法
- 红旗症状（如胸痛、意识障碍、严重呼吸困难等）触发时，`referral_needed` 自动置为 `true`
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
