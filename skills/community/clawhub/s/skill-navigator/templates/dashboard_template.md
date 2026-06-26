# OpenClaw Skill Dashboard

## 🚀 已安装 Skill 概览

| 图标 | Skill 名称 | 核心能力摘要 | 适用场景 |
| :--- | :--- | :--- | :--- |
| {{icon}} | **{{name}}** | {{description}} | {{use_cases}} |

---

## 📊 能力矩阵 (Capability Map)

> [!TIP]
> 以下雷达图展示了您当前已安装 Skill 的能力覆盖范围。

```mermaid
radar-chart
    title 已安装 Skill 能力分布
    axes
        数据处理: 0-100
        创意写作: 0-100
        技术开发: 0-100
        逻辑推理: 0-100
        沟通协作: 0-100
    dataset
        label: 当前能力
        data: [{{data_score}}, {{creative_score}}, {{tech_score}}, {{logic_score}}, {{comm_score}}]
```

---

## 💡 智能联想提示 (Contextual Prompting)

当您输入以下关键词时，系统将自动联想：

- **数据/报表** → 启用 `{{data_skill}}`
- **设计/视频** → 启用 `{{creative_skill}}`
- **代码/API** → 启用 `{{tech_skill}}`
- **流程/自动化** → 启用 `{{logic_skill}}`
