---
name: health-exam-overall-report
description: 体检报告整体解读。输入完整体检报告文本，输出整体健康评级、主要发现（含严重程度）、优先行动清单和个性化生活方式建议（JSON + 通俗易懂的整体解读）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📄"
      }
  }
---

# 体检报告整体解读

概述
----
面向**体检中心/健康管理机构**，给定受检者完整体检报告，本技能会：

- 综合所有检查结果给出整体健康评级（优秀/良好/需关注/需重视）
- 提取关键异常发现，按重要程度排序并标注严重程度
- 列出最优先需要处理的行动（最多3条）
- 给出个性化生活方式建议
- 建议下次体检时间及重点关注项目
- 生成面向受检者的通俗易懂整体解读文字

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理体检报告解读所必需的检查结果数据；不要求包含姓名、证件号、手机号等直接身份标识。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储。仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能输出为健康管理辅助解读，不构成医疗诊断；如有异常项目，请务必就诊由执业医生进一步评估。

输入格式
--------
纯文本（UTF-8），包含体检报告内容（可粘贴报告原文），例如：

```text
受检者：男，45岁
体检日期：2026年4月

一般检查：身高175cm，体重82kg，BMI 26.8，血压142/90mmHg
血常规：WBC 7.2×10⁹/L，RBC 5.1×10¹²/L，HGB 155g/L（均正常）
生化：ALT 52U/L（↑），AST 38U/L，TG 2.8mmol/L（↑），TC 5.9mmol/L（↑），FBG 6.2mmol/L（↑）
尿常规：尿蛋白(-)，尿糖(-)
心电图：窦性心律，ST段轻度改变
胸部CT：双肺未见明显实质性病变
腹部超声：轻度脂肪肝
```

也支持 JSON 格式（包含 `text`/`content`/`report` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 health-exam/report-interpret/overall-report/scripts/run.py \
  --input data/health-exam-overall/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 health-exam/report-interpret/overall-report/scripts/run.py \
  --input data/health-exam-overall/case-001.txt \
  --appkey <your-appkey> \
  --output runs/health-exam-overall/case-001.json
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
  "overall_grade": "需关注",
  "summary": "本次体检发现代谢相关多项异常，包括血压偏高、血脂升高、血糖偏高及轻度脂肪肝，需积极改善生活方式并尽快就医评估。",
  "key_findings": [
    {
      "category": "心血管/代谢",
      "finding": "血压142/90mmHg，达高血压1级标准；TG、TC均升高；空腹血糖6.2mmol/L（糖耐量减低范围）",
      "severity": "中度异常",
      "action_needed": "就医复诊，评估是否需要药物干预"
    },
    {
      "category": "消化/代谢",
      "finding": "ALT轻度升高，腹部超声提示轻度脂肪肝",
      "severity": "轻度异常",
      "action_needed": "定期监测，控制体重和饮食"
    }
  ],
  "normal_systems": ["血常规正常", "尿常规正常", "胸部CT未见异常"],
  "priority_actions": [
    {"rank": 1, "action": "前往内科/心内科就诊，评估高血压及代谢综合征", "reason": "血压达高血压标准，合并血脂、血糖异常"},
    {"rank": 2, "action": "3个月内复查肝功能、血脂、血糖", "reason": "监测代谢指标变化"}
  ],
  "lifestyle_advice": ["减少高脂高糖饮食", "每周至少150分钟中等强度有氧运动", "减重至正常BMI范围"],
  "next_exam_suggestion": "6个月后复查，重点关注：血压、血糖、血脂、肝功能"
}
```

**整体解读**：以"【整体解读】"开头，用通俗语言面向受检者说明健康状况和建议。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- overall_grade 评定标准：全部正常→优秀；有轻微异常但无需就医→良好；有需就诊异常→需关注；有紧急处理项→需重视
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
