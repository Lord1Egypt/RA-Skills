---
name: questionnaire-quality-checker
version: 1.0.0
description: 对心理学问卷数据进行可复现的数据质量筛查，检查缺失比例、非法或超范围值、量表内直线作答和极端作答模式，并生成逐样本标记报告。当用户说“检查问卷数据质量”“筛查无效问卷”“检查直线作答”“检查异常作答”“questionnaire quality check”“screen invalid responses”或要求对多个不同计分范围的量表进行基础质量控制时使用。适用于 CSV 格式的心理学问卷数据。
---

# Questionnaire Quality Checker

对心理学问卷数据进行基础、透明、可复现的数据质量筛查。

本 Skill 的目标是**标记需要人工复核的样本**，而不是根据单一指标自动删除被试。

## 适用场景

适用于包含一个或多个 Likert 量表的 CSV 数据，例如：

- A 量表：1–5 分
- B 量表：1–7 分
- C 量表：0–3 分

不同量表可以设置不同的合法取值范围。

## 工作流程

1. **确认数据与配置**
   - 数据文件应为 CSV。
   - 使用 JSON 配置文件指定：
     - 被试 ID 列
     - 每个量表包含的题目
     - 每个量表的最小值和最大值
     - 缺失率、直线作答和极端作答阈值
   - 不根据变量名猜测量表范围。

2. **运行筛查脚本**

```bash
python scripts/questionnaire_quality_checker.py <数据.csv> --config <配置.json>
```

如需保存完整 JSON 报告：

```bash
python scripts/questionnaire_quality_checker.py <数据.csv> --config <配置.json> --output report.json
```

3. **检查以下质量指标**

### A. 非法或超范围值

逐题检查：

- 非数字且未被定义为缺失值的内容
- 小于该量表最小值的数值
- 大于该量表最大值的数值

任何异常值都应报告具体变量和值。

### B. 高缺失比例

计算每位被试在所有已配置题目中的缺失比例。

默认规则：

- 缺失比例 `> 20%`：标记为 `high_missingness`

该阈值可以在配置文件中修改。

### C. 量表内直线作答

如果某个量表达到最少有效答题数后，所有有效回答完全相同，则标记：

`straightlining:<scale_name>`

默认要求至少有 4 个有效回答后才判断直线作答。

### D. 极端作答模式

在单个量表内，计算有效回答中选择该量表理论最小值或最大值的比例。

如果：

`极端值比例 >= 配置阈值`

则标记：

`extreme_response:<scale_name>`

默认阈值为 90%。

极端作答本身不能证明样本无效，只表示需要结合研究情境进一步核查。

4. **整理结果**

脚本输出 JSON，包括：

- 总样本数
- 配置题目数
- 被标记样本数
- 各筛查指标命中次数
- 每个被试的具体 flags 和 details

Agent 应将结果整理为简洁报告，例如：

```markdown
# Questionnaire Quality Report

## Overall
- Total respondents: 200
- Flagged respondents: 18
- Flagged rate: 9.0%

## Flag summary
| Criterion | N |
| --- | ---: |
| high_missingness | 5 |
| out_of_range | 2 |
| straightlining:Scale_A | 8 |
| extreme_response:Scale_B | 6 |

## Respondents requiring review
| ID | Flags | Details |
| --- | --- | --- |
| P013 | straightlining:Scale_A | all valid answers = 4 |
| P087 | out_of_range | B3 = 8, legal range 1–7 |

## Interpretation
这些标记用于数据质量复核，不应直接等同于“无效问卷”。
```

## 配置文件格式

示例：

```json
{
  "id_column": "id",
  "missing_tokens": ["", "NA", "N/A", "null", "."],
  "criteria": {
    "max_missing_prop": 0.2,
    "straightline_min_answered": 4,
    "extreme_prop_threshold": 0.9
  },
  "scales": [
    {
      "name": "Scale_A",
      "items": ["A1", "A2", "A3", "A4", "A5"],
      "min": 1,
      "max": 5
    },
    {
      "name": "Scale_B",
      "items": ["B1", "B2", "B3", "B4"],
      "min": 1,
      "max": 7
    }
  ]
}
```

## 解释原则

- **标记不等于删除。** 单一筛查指标通常不足以证明某份问卷无效。
- 所有排除规则应尽可能在分析前确定，并在论文中透明报告。
- 不应因为被试大量选择最低分或最高分就自动删除；真实的极端心理特征也可能产生极端回答。
- 直线作答只是一种潜在低努力作答指标，需要结合答题时长、注意力检测题、开放题质量或其他信息判断。
- 不同量表取值范围不同时，必须按量表分别检查，禁止用一个统一范围检查全部变量。
- 不对未配置变量进行范围推断。
- 如果配置中指定的题目在数据中不存在，应停止分析并报告缺失列，而不是静默跳过。
- 若用户需要形成正式论文中的样本排除标准，应报告每条规则、阈值、命中人数及规则重叠情况。
