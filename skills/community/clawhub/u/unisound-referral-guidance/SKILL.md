---
name: clinic-referral-guidance
description: 基层转诊指导。输入患者病情摘要，判断是否需要转诊、紧急程度、目标科室/医院级别，给出转诊前处置和随附材料清单（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🚑"
      }
  }
---

# 基层转诊指导

概述
----
面向**社区诊所/基层卫生机构**医生，给定患者病情摘要（症状、诊断、处理情况），本技能会：

- 判断是否需要转诊及紧急程度（立即/较急/择期/不需要）
- 推荐目标转诊科室和医院级别
- 列出满足的转诊指征（依据国家分级诊疗政策）
- 给出转诊前必要处置措施
- 列出应随患者携带的材料

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理转诊决策所必需的病情信息；不要求包含身份信息。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能输出为转诊决策辅助，不替代临床判断；紧急情况下请优先处置患者。

输入格式
--------
纯文本（UTF-8），包含患者病情关键信息，例如：

```text
患者：男，72岁
主要诊断：急性胸痛，持续20分钟
心电图：II、III、aVF导联ST段压低0.2mV
当前处理：硝酸甘油舌下含服1片，症状无缓解
血压：90/60 mmHg，心率：108次/分
既往史：高血压、糖尿病
```

也支持 JSON 格式（包含 `text`/`content`/`case_summary` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/primary-care-assist/referral-guidance/scripts/run.py \
  --input data/clinic-referral/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/primary-care-assist/referral-guidance/scripts/run.py \
  --input data/clinic-referral/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-referral/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。患者病情摘要文件路径（txt 或 json，UTF-8）。
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
  "referral_decision": "建议立即转诊",
  "urgency": "紧急（立即）",
  "target_department": "心内科/急诊科",
  "target_hospital_level": "三级医院",
  "referral_reason": "急性下壁心肌缺血，血压低，硝酸甘油无效，疑似急性冠脉综合征",
  "referral_criteria_met": [
    "心电图提示ST段改变",
    "血流动力学不稳定（血压90/60mmHg）",
    "胸痛持续且治疗无效"
  ],
  "pre_transfer_measures": [
    "建立静脉通道",
    "持续心电监护",
    "给予阿司匹林300mg嚼服（若无禁忌）",
    "拨打120急救"
  ],
  "transfer_documents_required": [
    "转诊单",
    "心电图原件/照片",
    "用药记录"
  ],
  "can_manage_locally_if_no_referral": null
}
```

**自然语言摘要**：以"【摘要】"开头，说明转诊建议和关键注意事项。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 转诊标准参考国家分级诊疗相关政策及常见疾病转诊指南
- 紧急情况下，系统会同时在 `pre_transfer_measures` 中列出院前急救措施
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
