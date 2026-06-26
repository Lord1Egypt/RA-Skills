---
name: clinic-vaccination-reminder
description: 预防接种提醒。输入居民年龄/接种史/特殊情况，依据国家免疫规划生成个性化接种提醒清单（JSON + 自然语言摘要）。
metadata:
  {
    "openclaw":
      {
        "emoji": "💉"
      }
  }
---

# 预防接种提醒

概述
----
面向**社区卫生服务机构/乡镇卫生院**公共卫生人员，给定居民年龄、已接种记录和特殊健康情况，本技能会：

- 核查是否有已逾期（漏种）的免疫规划疫苗
- 列出近期应接种的疫苗及建议时间
- 针对特殊人群（老年人、慢性病患者、妊娠等）推荐非免疫规划但有益的疫苗
- 提示禁忌证和接种前注意事项

参考依据：**中国国家免疫规划（2021年版）** 及相关特殊人群接种指南。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理接种提醒所必需的年龄、接种史和健康状况信息；不要求包含直接身份标识。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：接种建议仅供参考，最终接种方案由接种医生根据具体情况决定。

输入格式
--------
纯文本（UTF-8），包含居民基本信息和接种记录，例如：

```text
年龄：2岁3个月，性别：男
已接种记录：
- 乙肝疫苗：已接种3剂
- 卡介苗：已接种
- OPV/IPV：已接种3剂
- 百白破：已接种3剂
- 麻腮风：8月龄已接种1剂
- 甲肝疫苗：未接种
- 流脑疫苗：6月、9月各1剂
特殊情况：无
```

也支持 JSON 格式（包含 `text`/`content`/`vaccination_info` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 clinic/public-health-mgmt/vaccination-reminder/scripts/run.py \
  --input data/clinic-vaccination/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 clinic/public-health-mgmt/vaccination-reminder/scripts/run.py \
  --input data/clinic-vaccination/case-001.txt \
  --appkey <your-appkey> \
  --output runs/clinic-vaccination/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。居民接种信息文件路径（txt 或 json，UTF-8）。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。
- `--output PATH`：输出文件路径（默认：打印到 stdout）。
- `--base URL`：内部大模型 base URL（默认：`https://maas-api.hivoice.cn/v1`）。
- `--model STRING`：模型名称（默认：`u1-insulremed`）。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待（默认：0）。
- `--encoding STRING`：输入文件编码（默认：`utf-8`）。

输出约定
--------
输出分两部分：

**JSON 结构**：

```json
{
  "resident_profile": {
    "age_group": "幼儿1-3岁",
    "special_conditions": []
  },
  "overdue_vaccines": [],
  "due_soon_vaccines": [
    {
      "vaccine_name": "甲肝疫苗（HepA）第1剂",
      "recommended_timing": "18月龄（已到，需尽快补种）",
      "notes": "标准接种时间为18月龄，现已2岁3个月，建议尽快补种"
    },
    {
      "vaccine_name": "麻腮风疫苗（MMR）第2剂",
      "recommended_timing": "18月龄（已到，需补种）",
      "notes": "第2剂标准接种时间为18月龄"
    },
    {
      "vaccine_name": "百白破第4剂（加强）",
      "recommended_timing": "18月龄（已到）",
      "notes": "基础免疫完成后18月龄需加强接种"
    }
  ],
  "recommended_non_mandatory": [
    {
      "vaccine_name": "水痘疫苗",
      "reason": "部分地区已纳入免疫规划，建议接种",
      "notes": "1岁以上可接种第1剂，4岁加强"
    }
  ],
  "contraindications": [],
  "precautions": ["接种前确认无发热、急性疾病", "如有鸡蛋过敏史，告知接种医生"],
  "next_visit_suggestion": "建议本月内到接种门诊补种甲肝、麻腮风第2剂及百白破加强针"
}
```

**自然语言摘要**：以"【摘要】"开头，列出需要补种的疫苗和建议事项。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 接种程序以国家免疫规划为准，不同地区可能有差异
- 特殊人群（免疫缺陷、妊娠等）会有专门的禁忌提示
- 接种记录不完整时，输出中会注明"需核实接种记录"
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
