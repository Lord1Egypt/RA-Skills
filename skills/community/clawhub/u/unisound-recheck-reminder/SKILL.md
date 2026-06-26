---
name: health-exam-recheck-reminder
description: 复查提醒。从体检报告中提取所有需复查项目，按紧急程度分级（2周/1-3月/3-6月/6-12月），给出复查检查项、就诊科室和准备事项（JSON + 面向受检者的复查提醒）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔔"
      }
  }
---

# 复查提醒

概述
----
面向**体检中心/健康管理机构**，给定受检者体检报告，本技能会：

- 识别所有需要复查的异常项目
- 按紧急程度分级（紧急2周内/短期1-3月/中期3-6月/长期6-12月）
- 为每项指定复查检查项目、就诊科室和建议机构
- 给出复查前注意事项（空腹/停药等）
- 区分"需到医院就诊"、"可在体检机构复查"、"可居家自测"三类
- 生成面向受检者的友好提醒通知

与"检后随访管理"的区别：本技能聚焦**复检闭环**，输出更轻量（以提醒清单为主），适合直接推送给受检者；随访管理则包含健康指导等更宽泛的检后服务。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理生成复查提醒所必需的体检数据；不要求包含直接身份标识。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：复查提醒为健康管理服务，具体复查方案由接诊医生决定。

输入格式
--------
纯文本（UTF-8），可输入完整体检报告，例如：

```text
受检者：女，42岁，体检日期：2026年5月
主要异常发现：
- 宫颈液基细胞学（TCT）：ASCUS（不典型鳞状细胞，意义不明）
- 乳腺超声：右乳3mm低回声结节，BI-RADS 3类
- 甲状腺超声：左叶6mm低回声结节，TI-RADS 3类
- TG：2.3mmol/L（轻度升高）
- 空腹血糖：5.9mmol/L（正常高值）
- 血压：128/82mmHg
- 骨密度：腰椎T值-1.1（骨量减少）
```

也支持 JSON 格式（包含 `text`/`content`/`report` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 health-exam/post-exam-mgmt/recheck-reminder/scripts/run.py \
  --input data/health-exam-recheck/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 health-exam/post-exam-mgmt/recheck-reminder/scripts/run.py \
  --input data/health-exam-recheck/case-001.txt \
  --appkey <your-appkey> \
  --output runs/health-exam-recheck/case-001.json
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
  "recheck_count": 6,
  "has_urgent": false,
  "items": [
    {
      "item": "宫颈TCT（ASCUS）",
      "current_finding": "ASCUS（不典型鳞状细胞，意义不明）",
      "recheck_urgency": "短期（1-3个月）",
      "recheck_exam": "HPV分型检测 + TCT复查",
      "recheck_venue": "二级及以上医院",
      "recheck_department": "妇科",
      "purpose": "明确是否存在高危型HPV感染，判断是否需要阴道镜检查",
      "preparation": ["月经干净后3-5天就诊", "就诊前24小时避免同房和阴道冲洗"],
      "what_to_watch": "如出现同房后出血或异常白带，提前就诊"
    },
    {
      "item": "甲油三酯（TG）轻度升高",
      "current_finding": "TG 2.3mmol/L（轻度升高）",
      "recheck_urgency": "中期（3-6个月）",
      "recheck_exam": "血脂四项复查",
      "recheck_venue": "体检机构",
      "recheck_department": null,
      "purpose": "评估生活方式干预后血脂控制效果",
      "preparation": ["空腹8-12小时", "复查前3天避免高脂饮食"],
      "what_to_watch": null
    }
  ],
  "grouped_by_venue": {
    "urgent_medical_referral": [],
    "followup_at_exam_center": ["血脂四项复查", "血糖复查", "骨密度复查"],
    "self_monitoring": ["每周测量血压1-2次"]
  }
}
```

**复查提醒**：以"【复查提醒】"开头，用清晰友好的语言提醒受检者需要跟进的复查事项。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- TI-RADS/BI-RADS 分类随访时间遵循国际超声学会标准
- has_urgent 为 true 时，输出文字会特别强调紧急就诊的必要性
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
