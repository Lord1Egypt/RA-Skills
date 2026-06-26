---
name: clinic-chronic-screening
description: 慢病筛查辅助。输入居民健康数据（体征/检验/生活方式/家族史），评估高血压、糖尿病、心脑血管疾病等慢性病风险，给出分级和管理建议（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊"
      }
  }
---

# 慢病筛查辅助

概述
----
面向**社区卫生服务机构/乡镇卫生院**公共卫生人员，给定居民健康数据，本技能会：

- 对高血压、糖尿病、心脑血管疾病、COPD、慢性肾脏病等主要慢性病进行风险评估
- 判断筛查状态（已确诊/高风险/中风险/低风险/需进一步检查）
- 对已确诊慢病评估当前控制状况
- 给出分级管理建议（生活方式干预、就诊、检查）
- 建议随访频次

筛查标准参考《国家基本公共卫生服务规范（第三版）》及相关慢病管理指南。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理慢病筛查所必需的健康数据；不要求包含直接身份标识。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：筛查结果仅为辅助判断，不替代临床诊断；慢病的最终诊断须由执业医生确认。

输入格式
--------
纯文本（UTF-8），包含居民健康数据，例如：

```text
居民信息：男，55岁，务农
血压：145/92 mmHg（连续3次测量均超标）
空腹血糖：6.5 mmol/L（糖耐量减低史）
BMI：27.5
吸烟史：吸烟30年，每天约1包，近期有慢性咳嗽
饮酒：每天少量
体力活动：较少
家族史：父亲有高血压、2型糖尿病
```

也支持 JSON 格式（包含 `text`/`content`/`health_data` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/public-health-mgmt/chronic-screening/scripts/run.py \
  --input data/clinic-chronic-screening/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/public-health-mgmt/chronic-screening/scripts/run.py \
  --input data/clinic-chronic-screening/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-chronic-screening/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。居民健康数据文件路径（txt 或 json，UTF-8）。
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
  "screening_results": [
    {
      "disease": "高血压",
      "screening_status": "已确诊",
      "risk_level": "高",
      "risk_basis": ["连续3次血压测量收缩压≥140mmHg", "有家族史"],
      "current_control": "控制不佳",
      "management_recommendations": [
        "加强健康教育，低盐低脂饮食",
        "建议就诊调整降压方案",
        "每月随访测量血压"
      ]
    },
    {
      "disease": "2型糖尿病",
      "screening_status": "高风险",
      "risk_level": "高",
      "risk_basis": ["空腹血糖6.5mmol/L（糖耐量减低）", "超重（BMI 27.5）", "家族史阳性"],
      "current_control": null,
      "management_recommendations": [
        "建议行OGTT明确诊断",
        "减重、增加体力活动",
        "低糖饮食干预"
      ]
    }
  ],
  "priority_action": "尽快完善糖尿病诊断（OGTT），同时调整高血压治疗方案",
  "follow_up_frequency": "每1个月随访1次（高血压），每3个月复查血糖",
  "lifestyle_interventions": ["戒烟", "减盐（<6g/天）", "增加有氧运动（每周≥150分钟）", "控制体重"]
}
```

**自然语言摘要**：以"【摘要】"开头，概括筛查结果和重点管理措施。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 筛查标准参考《国家基本公共卫生服务规范（第三版）》及相关专科指南
- 数据信息越完整（含体征、检验、生活方式），筛查结果越准确
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
