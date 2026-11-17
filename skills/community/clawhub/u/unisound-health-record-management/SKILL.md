---
name: clinic-health-record
description: 居民健康档案管理。从非结构化就诊记录/体检报告/问卷文本中抽取结构化居民健康档案，符合《国家基本公共卫生服务规范（第三版）》（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📋"
      }
  }
---

# 居民健康档案管理

概述
----
面向**社区卫生服务机构/乡镇卫生院**公共卫生人员，给定居民就诊记录、体检报告或健康问卷文本，本技能会：

- 提取基本信息（性别、年龄、职业等）
- 结构化现病史、慢性病史、家族史
- 提取生活方式信息（吸烟、饮酒、运动、饮食）
- 整理体格检查和实验室检查结果
- 汇总当前用药情况
- 识别健康风险因素并给出随访计划建议

档案结构参考《国家基本公共卫生服务规范（第三版）》。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理健康档案建立所必需的信息；**不处理姓名、身份证号、手机号、家庭住址等直接身份标识**，建议在传入前完成脱敏。
- **严格脱敏**：发送前对可识别身份信息进行脱敏/去标识化处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **公共卫生用途声明**：本技能输出的档案信息仅用于基层居民健康管理，须由公卫人员复核后录入正式档案系统。

输入格式
--------
纯文本（UTF-8），包含居民健康相关信息，例如：

```text
男，52岁，务农，小学文化。
2018年诊断为2型糖尿病，规律口服二甲双胍500mg tid。
2021年诊断为高血压病，服用氨氯地平5mg qd。
父亲有高血压和冠心病。
吸烟30年，每天约1包；偶尔饮酒。
体检：身高168cm，体重78kg，BP 148/92mmHg，空腹血糖7.8mmol/L，HbA1c 7.9%。
```

也支持 JSON 格式（包含 `text`/`content`/`health_info` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/public-health-mgmt/health-record/scripts/run.py \
  --input data/clinic-health-record/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/public-health-mgmt/health-record/scripts/run.py \
  --input data/clinic-health-record/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-health-record/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。居民健康信息文件路径（txt 或 json，UTF-8）。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。
- `--output PATH`：输出文件路径（默认：打印到 stdout）。
- `--base URL`：内部大模型 base URL（默认：`https://maas-api.hivoice.cn/v1`）。
- `--model STRING`：模型名称（默认：`u2-med`）。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待（默认：0）。
- `--encoding STRING`：输入文件编码（默认：`utf-8`）。

输出约定
--------
输出分两部分：

**JSON 结构**（参考国家公卫规范字段）：

```json
{
  "basic_info": { "gender": "男", "age": 52, "occupation": "务农", "education": "小学" },
  "health_status": {
    "chronic_diseases": ["2型糖尿病（2018年）", "高血压病（2021年）"]
  },
  "lifestyle": {
    "smoking": "现在吸烟",
    "smoking_amount": "20支/天",
    "drinking": "偶尔"
  },
  "physical_exam": {
    "height_cm": 168, "weight_kg": 78, "bmi": 27.6,
    "blood_pressure": "148/92 mmHg"
  },
  "lab_results": {
    "blood_glucose_fasting": "7.8 mmol/L",
    "hba1c": "7.9%"
  },
  "current_medications": [
    { "drug_name": "二甲双胍", "dosage": "500mg tid", "indication": "2型糖尿病" },
    { "drug_name": "氨氯地平", "dosage": "5mg qd", "indication": "高血压" }
  ],
  "health_assessment": {
    "risk_factors": ["吸烟", "超重（BMI 27.6）", "血糖控制不佳", "血压未达标"],
    "health_guidance_needed": ["戒烟干预", "糖尿病自我管理教育", "高血压生活方式指导"]
  },
  "follow_up_plan": {
    "frequency": "每3个月随访1次",
    "items_to_monitor": ["血压", "血糖", "HbA1c", "体重"]
  }
}
```

**自然语言摘要**：以"【摘要】"开头，概括主要健康问题和管理要点。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 未在输入中明确提及的字段输出 `null`，不捏造信息
- BMI 如有身高体重数据会自动计算
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
