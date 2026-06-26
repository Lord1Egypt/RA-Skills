---
name: health-exam-abnormal-items
description: 体检异常指标专项解读。针对体检报告中的每项异常，逐一说明"是什么/为何异常/有何影响/如何干预"，并分析多指标关联，语言通俗易懂（JSON + 专项解读文字）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍"
      }
  }
---

# 异常指标专项解读

概述
----
面向**体检中心/健康管理机构**，对体检报告中出现的每一项异常指标进行深度专项解读，本技能会：

- 用通俗语言解释每个指标的含义
- 分析可能的异常原因（结合受检者个人背景）
- 说明对健康的潜在影响
- 给出生活方式干预建议和就医建议
- 分析多个异常指标之间的内在关联（如代谢综合征）
- 标注紧急程度

与"体检报告整体解读"的区别：本技能聚焦**逐项深度解读**，面向用户感知强的异常项，内容更详尽；整体解读侧重全局评级和优先行动。

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理指标解读所必需的检查数据；不要求包含直接身份标识。
- **严格脱敏**：发送前对可识别身份信息进行脱敏处理。
- **不做本地持久化**：仅在内存中短暂处理；**本次调用结束即销毁**。
- **医疗边界**：本技能解读为健康教育参考，不替代医生诊断；存在异常时请就医确认。

输入格式
--------
纯文本（UTF-8），可输入完整体检报告（会自动提取异常项），也可只输入异常指标列表，例如：

```text
受检者：男，45岁，轻体力劳动，BMI 26.8
异常指标：
- 甘油三酯（TG）：2.8mmol/L（↑，参考：<1.7mmol/L）
- 总胆固醇（TC）：5.9mmol/L（↑，参考：<5.2mmol/L）
- 空腹血糖（FBG）：6.2mmol/L（↑，参考：3.9-6.1mmol/L）
- 谷丙转氨酶（ALT）：52U/L（↑，参考：0-40U/L）
- 血压：142/90mmHg（↑，参考：<130/80mmHg）
超声提示：轻度脂肪肝
```

也支持 JSON 格式（包含 `text`/`content`/`report` 字段的对象）。

快速开始
--------

```bash
# 从 skills 目录运行
python3 health-exam/report-interpret/abnormal-items/scripts/run.py \
  --input data/health-exam-abnormal/case-001.txt \
  --appkey <your-appkey>

# 保存输出到文件
python3 health-exam/report-interpret/abnormal-items/scripts/run.py \
  --input data/health-exam-abnormal/case-001.txt \
  --appkey <your-appkey> \
  --output runs/health-exam-abnormal/case-001.json
```

参数说明
--------
- `--input PATH`：**必填**。体检报告或异常指标文件路径（txt 或 json，UTF-8）。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。
- `--output PATH`：输出文件路径（默认：打印到 stdout）。
- `--base URL`：内部大模型 base URL（默认：`https://maas-api.hivoice.cn/v1`）。
- `--model STRING`：模型名称（默认：`u1-insuremed`）。
- `--timeout SECONDS`：HTTP 超时秒数；`0` 表示一直等待（默认：0）。
- `--encoding STRING`：输入文件编码（默认：`utf-8`）。

输出约定
--------
输出分两部分：

**JSON 结构**（每个异常指标一条详细解读）：

```json
{
  "abnormal_count": 5,
  "items": [
    {
      "item_name": "甘油三酯 TG",
      "value": "2.8mmol/L",
      "reference_range": "<1.7mmol/L",
      "deviation": "偏高",
      "deviation_degree": "轻度",
      "plain_explanation": "甘油三酯是血液中一种脂肪，主要来自饮食中的油脂和糖分转化",
      "possible_causes": ["饮食油腻或高糖", "运动量不足", "超重"],
      "health_impact": "长期偏高增加动脉硬化、心脑血管疾病和胰腺炎风险",
      "intervention": {
        "lifestyle": ["减少油炸食品和含糖饮料", "增加有氧运动", "控制体重"],
        "medical": "定期监测，3个月后复查血脂"
      },
      "urgency": "定期复查"
    }
  ],
  "correlations": [
    "血脂升高（TG、TC）+ 血糖偏高 + 超重 + 脂肪肝，提示代谢综合征风险，是心脑血管疾病的重要危险因素组合，建议系统评估和干预"
  ]
}
```

**专项解读文字**：以"【专项解读】"开头，用通俗语言逐项向受检者解释异常指标。

依赖
----
### 运行环境
- Python 3.7+（仅使用标准库，无需额外安装）

### 外部 API
- 内部医疗大模型：`https://maas-api.hivoice.cn/v1/chat/completions`

备注
----
- 输入可以是完整报告（技能会自动提取异常项），也可以只粘贴异常指标列表
- 若受检者有已知慢性病史，在输入中注明可获得更精准的解读
- **发布约束**：示例输入、运行输出均放在 skill 包外（`data/`、`runs/`），skill 目录内仅保留可发布的核心文件
