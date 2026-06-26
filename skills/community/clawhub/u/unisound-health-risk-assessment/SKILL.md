---
name: health-exam-health-risk-assessment
description: 体检健康风险评估。基于体检报告对心脑血管、糖代谢、肿瘤、代谢综合征等多维度健康风险进行分级，生成含时间节点的个性化健康管理方案（JSON + 健康风险报告）。
metadata:
  {
    "openclaw":
      {
        "emoji": "⚠️"
      }
  }
---

# 健康风险评估

概述
----
面向**体检中心/健康管理机构**，给定受检者体检报告，本技能会：

- 对7大健康风险维度进行分级评估：
  - 心脑血管风险
  - 糖代谢风险
  - 代谢综合征
  - 肿瘤风险（基于标志物和影像发现）
  - 肝脏健康
  - 肾脏健康
  - 甲状腺健康
- 给出整体风险级别（低/中/高/极高）
- 生成含立即行动、3个月目标、1年目标的健康管理计划
- 提供个性化的饮食、运动、睡眠建议
- 给出专科转诊建议

与"体检报告整体解读"的区别：本技能重点在**风险前瞻性评估**和**管理计划制定**，适合作为检后健康管理服务的入口。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理风险评估所必需的检查数据；不要求包含直接身份标识。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能输出为风险评估参考，不替代专科诊断；高风险人群请务必就医。

输入格式
--------
纯文本（UTF-8），建议提供完整体检报告，信息越全评估越精准，例如：

```text
受检者：男，50岁，公司管理层，吸烟史20年（每天约1包），偶尔饮酒
BMI：27.8，腰围93cm
血压：148/94mmHg
血糖：空腹6.8mmol/L，HbA1c 6.4%
血脂：TC 6.2mmol/L，LDL 4.0mmol/L，HDL 0.9mmol/L，TG 3.1mmol/L
肝功：ALT 68U/L，AST 52U/L，GGT 78U/L
肾功：肌酐88μmol/L，尿酸480μmol/L
肿瘤标志物：CEA 5.8ng/mL（↑，参考<5），AFP正常，PSA正常
心电图：窦性心律，左室高电压
超声：中度脂肪肝，甲状腺右叶3mm低回声结节（TI-RADS 3类）
```

也支持 JSON 格式（包含 `text`/`content`/`report` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 health-exam/report-interpret/health-risk-assessment/scripts/run.py \
  --input data/health-exam-risk/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 health-exam/report-interpret/health-risk-assessment/scripts/run.py \
  --input data/health-exam-risk/case-001.txt \
  --appkey <your-appkey> \
  --output runs/health-exam-risk/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。体检报告文件路径（txt 或 json，UTF-8）。
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
  "risk_profile": {
    "age": "50岁",
    "gender": "男",
    "overall_risk_level": "高风险"
  },
  "risk_dimensions": [
    {
      "dimension": "心脑血管风险",
      "risk_level": "高",
      "risk_factors": ["高血压（148/94mmHg）", "高LDL（4.0mmol/L）", "低HDL（0.9mmol/L）", "吸烟20年", "超重"],
      "protective_factors": [],
      "10_year_risk_estimate": "较高（Framingham评分估算>20%）",
      "priority_interventions": ["戒烟", "就医评估降脂降压治疗", "增加有氧运动"]
    }
  ],
  "health_management_plan": {
    "immediate_actions": [
      {"action": "前往内科/心内科就诊", "reason": "多重心血管危险因素叠加", "target": "血压<130/80mmHg，LDL<2.6mmol/L"}
    ],
    "3_month_goals": ["戒烟或显著减量", "血压达标", "体重减少3-5kg"],
    "1_year_goals": ["血脂达标", "血糖控制在正常范围", "完成甲状腺结节随访"],
    "long_term_monitoring": ["每3个月查血压、血糖、血脂", "每年体检含肿瘤标志物"]
  },
  "personalized_advice": {
    "diet": ["地中海饮食模式", "减少红肉和加工肉类", "增加深海鱼类（每周2次）"],
    "exercise": "每周5次中等强度有氧运动（快步走/游泳），每次30-45分钟",
    "sleep_stress": "保证7-8小时睡眠，学习压力管理技巧",
    "smoking_alcohol": "强烈建议戒烟（最重要的单一干预），限酒至每周<2标准饮"
  },
  "specialist_referrals": [
    {"specialty": "心内科/内分泌科", "reason": "高血压合并多重代谢异常", "urgency": "尽快"},
    {"specialty": "超声科/甲状腺外科", "reason": "甲状腺结节TI-RADS 3类随访", "urgency": "择期（3-6个月）"}
  ]
}
```

**健康风险报告**：以"【健康风险报告】"开头，用友好通俗的语言告知受检者主要风险和行动建议。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 体检信息越完整（含生活方式、家族史、既往病史），风险评估越精准
- overall_risk_level 综合所有维度：有任一维度"极高"→整体极高风险
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
