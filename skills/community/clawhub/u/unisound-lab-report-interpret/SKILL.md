---
name: clinic-lab-report-interpret
description: 基础检查辅助解读。输入血常规/生化/尿常规/心电图等检查报告文本，识别异常指标，给出临床意义和随访建议（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬"
      }
  }
---

# 基础检查辅助解读

概述
----
面向**社区诊所/基层卫生机构**医生，给定检查报告文本，本技能会：

- 识别所有异常指标（含偏高/偏低及程度）
- 结合参考范围给出每项异常的临床意义
- 标注需紧急关注的危急值
- 给出综合解读和随访/进一步检查建议

支持的检查类型（不限于）：
- 血常规（CBC）
- 生化全套（肝功、肾功、血糖、血脂、电解质等）
- 尿常规
- 凝血功能
- 甲状腺功能
- 心电图（文字描述）

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理解读所必需的检查结果；不要求包含患者姓名等身份信息。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能输出为检查结果辅助解读，不替代临床判断；最终诊断须由执业医生确定。

输入格式
--------
纯文本（UTF-8），包含检查报告内容，例如：

```text
患者：男，55岁，高血压病史8年
检查类型：血常规 + 生化

血常规：
WBC 12.5×10⁹/L（↑，参考：4.0-10.0）
RBC 4.2×10¹²/L（正常）
HGB 130g/L（正常）
PLT 280×10⁹/L（正常）

生化：
ALT 65U/L（↑，参考：0-40）
AST 45U/L（↑，参考：0-35）
Cr 115μmol/L（正常）
GLU 6.8mmol/L（↑，参考：3.9-6.1）
```

也支持 JSON 格式（包含 `text`/`content`/`lab_report` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/primary-care-assist/lab-report-interpret/scripts/run.py \
  --input data/clinic-lab-report/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/primary-care-assist/lab-report-interpret/scripts/run.py \
  --input data/clinic-lab-report/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-lab-report/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。检查报告文件路径（txt 或 json，UTF-8）。
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
  "exam_type": "血常规 + 生化",
  "overall_status": "轻度异常",
  "abnormal_items": [
    {
      "item_name": "WBC（白细胞）",
      "value": "12.5×10⁹/L",
      "reference_range": "4.0-10.0×10⁹/L",
      "status": "偏高",
      "clinical_significance": "白细胞升高，提示可能存在感染或炎症反应",
      "urgency": "需关注",
      "suggestions": "结合临床症状，建议复查或行CRP、PCT等炎症指标"
    }
  ],
  "normal_items_summary": "RBC、HGB、PLT均在正常范围",
  "overall_interpretation": "WBC轻度升高，合并ALT、AST轻度升高，提示可能存在感染伴肝功能轻度受损，血糖略高于正常上限。建议进一步评估感染原因，注意肝功能动态变化。",
  "follow_up_suggestions": [
    "1周后复查肝功能、血常规",
    "监测血糖，必要时行OGTT"
  ],
  "urgent_attention_needed": false
}
```

**自然语言摘要**：以"【摘要】"开头，总结关键异常和临床建议。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 危急值（如严重低钠、极低血小板等）会触发 `urgent_attention_needed: true`，需立即处置
- 若输入包含患者年龄、性别、临床背景，解读将更精准
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
