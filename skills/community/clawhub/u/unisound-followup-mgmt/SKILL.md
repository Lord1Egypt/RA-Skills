---
name: health-exam-followup-mgmt
description: 检后随访管理。根据体检报告，生成结构化随访计划（时间节点/随访内容/健康指导），支撑体检闭环服务（JSON + 面向受检者的随访通知）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📅"
      }
  }
---

# 检后随访管理

概述
----
面向**体检中心/健康管理机构**，给定受检者体检报告，本技能会：

- 生成按时间节点（1个月/3个月/6个月/1年）组织的随访计划
- 明确每个时间点需复查的项目、就诊科室和目标值
- 提供针对性的健康指导要点（饮食/运动/用药依从性等）
- 列出预警条件（出现哪些症状需立即就医）
- 给出下次年度体检的重点关注项目

本技能是体检服务闭环的核心环节，实现"检查—发现—跟踪—改善"全链条管理。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理制定随访计划所必需的体检数据；不要求包含直接身份标识。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：随访计划为健康管理建议，具体就诊方案由接诊医生决定。

输入格式
--------
纯文本（UTF-8），建议提供体检报告原文，例如：

```text
受检者：女，42岁
体检日期：2026年5月
主要发现：
- 血压：135/86mmHg（临界高血压）
- 空腹血糖：6.0mmol/L（临界偏高）
- TG：2.1mmol/L（轻度升高）
- 宫颈液基细胞学：ASCUS（不典型鳞状细胞）
- 乳腺超声：右乳3mm结节，BI-RADS 3类
- 甲状腺超声：TI-RADS 2类
- 骨密度：T值-1.2（骨量减少）
其余各项：正常
```

也支持 JSON 格式（包含 `text`/`content`/`report` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 health-exam/post-exam-mgmt/followup-mgmt/scripts/run.py \
  --input data/health-exam-followup/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 health-exam/post-exam-mgmt/followup-mgmt/scripts/run.py \
  --input data/health-exam-followup/case-001.txt \
  --appkey <your-appkey> \
  --output runs/health-exam-followup/case-001.json
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
  "followup_summary": {
    "total_followup_items": 5,
    "highest_priority": "宫颈ASCUS需6个月内行HPV检测+TCT复查",
    "exam_date": "2026年5月"
  },
  "followup_schedule": [
    {
      "timepoint": "1个月内",
      "items": [
        {
          "issue": "宫颈ASCUS",
          "followup_action": "妇科就诊，行HPV分型检测",
          "target_value": "明确是否高危型HPV阳性",
          "channel": "医院就诊"
        }
      ]
    },
    {
      "timepoint": "6个月后",
      "items": [
        {
          "issue": "右乳结节（BI-RADS 3）",
          "followup_action": "乳腺超声复查",
          "target_value": "结节无增大",
          "channel": "本机构复查或医院超声科"
        }
      ]
    }
  ],
  "health_coaching_points": [
    {
      "topic": "代谢管理",
      "key_messages": ["低盐低糖饮食", "增加有氧运动", "每日监测血压"],
      "materials_to_provide": ["高血压预防手册", "血糖管理指南"]
    }
  ],
  "alert_conditions": ["出现持续头痛、视物模糊或血压≥160/100mmHg时立即就诊"],
  "next_annual_exam_focus": ["血压、血糖、血脂", "妇科（宫颈+乳腺）", "骨密度"]
}
```

**随访通知**：以"【随访通知】"开头，用友好语言向受检者说明需要跟进的事项和时间安排。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- followup_schedule 按紧急程度和时间从近到远排序
- 对于影像学可疑发现（乳腺结节/甲状腺结节等），会给出明确的随访时间窗
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
