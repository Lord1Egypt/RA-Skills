---
name: clinic-prescription-assist
description: 基层处方开具辅助。输入诊断、患者基本信息（年龄/肾功/过敏史/合并用药），推荐用药方案，检查药物相互作用与禁忌，给出剂量调整建议（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "💊"
      }
  }
---

# 基层处方开具辅助

概述
----
面向**社区诊所/基层卫生机构**医生，给定患者诊断及个体信息，本技能会：

- 推荐合理用药方案（优先国家基本药物，含剂量/频次/疗程）
- 检查已有合并用药与拟开药之间的相互作用
- 识别禁忌（如过敏史、妊娠、肝肾功能不全等）并给出剂量调整建议
- 给出用药监测建议和患者教育要点

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理开具处方所必需的患者信息；不要求也不鼓励包含姓名、证件号、手机号等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能输出为处方辅助建议，不替代执业药师/医生的审方责任；最终处方须由执业医生签发。

输入格式
--------
纯文本（UTF-8），包含诊断和患者用药相关信息，例如：

```text
诊断：2型糖尿病，高血压病2级
患者信息：年龄65岁，体重70kg，血肌酐120μmol/L，eGFR约46 ml/min/1.73m²
过敏史：磺胺类药物过敏
当前用药：缬沙坦80mg qd，阿司匹林100mg qd
拟新增用药：二甲双胍，格列齐特
```

也支持 JSON 格式（包含 `text`/`content` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/primary-care-assist/prescription-assist/scripts/run.py \
  --input data/clinic-prescription/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/primary-care-assist/prescription-assist/scripts/run.py \
  --input data/clinic-prescription/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-prescription/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。处方信息文件路径（txt 或 json，UTF-8）。
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
  "prescription_check": {
    "status": "需注意",
    "issues": [
      {
        "type": "剂量调整",
        "severity": "moderate",
        "drugs_involved": ["二甲双胍"],
        "description": "eGFR 46 ml/min/1.73m²，二甲双胍需谨慎使用，应减量至500mg bid",
        "recommendation": "建议起始剂量500mg bid，定期复查肾功能；eGFR<45时停用"
      }
    ]
  },
  "recommended_drugs": [
    {
      "drug_name": "二甲双胍",
      "dosage": "500mg",
      "frequency": "bid",
      "route": "口服",
      "duration": "长期，定期评估",
      "notes": "餐中或餐后服用，减少胃肠道反应"
    }
  ],
  "monitoring_required": ["每3个月复查血肌酐/eGFR", "空腹血糖及糖化血红蛋白"],
  "patient_education": ["随餐服药", "出现恶心呕吐时及时就诊"],
  "overall_safety": "需监测"
}
```

**自然语言摘要**：以"【摘要】"开头，总结关键用药建议和注意事项。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- severity 分级：`major`（禁忌/严重，必须干预）、`moderate`（需调整）、`minor`（注意观察）
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
