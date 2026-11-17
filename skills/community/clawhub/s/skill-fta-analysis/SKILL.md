---
name: 故障树分析技能
slug: fta-analysis
displayName: 故障树分析技能
description: 故障树分析技能；用于系统可靠性与安全性分析；支持故障树构建、可视化、概率计算、重要性分析、报告生成及数据导入导出；覆盖定性与定量FTA
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 故障树分析（FTA）技能

## 任务目标
- 本技能用于：系统可靠性与安全性分析，支持定性与定量故障树分析
- 能力包含：故障树构建与可视化、顶事件概率计算、基本事件重要性分析、专业报告生成、数据导入导出
- 触发条件：用户需要分析系统故障原因、评估系统可靠性、识别关键故障模式或生成质量分析报告

## 前置准备
- 依赖说明：`graphviz` 用于故障树图形渲染
- 非标准文件准备：故障树数据文件（JSON格式），用户需提供或由智能体根据对话构建

## 操作步骤

### 标准流程

#### 1. 构建故障树数据
根据用户描述的系统结构，构建故障树JSON数据：
```json
{
  "name": "系统名称",
  "top_event": "event_id",
  "nodes": {
    "event_id": {
      "type": "basic|intermediate|and|or",
      "name": "事件名称",
      "probability": 0.01,
      "description": "事件描述"
    }
  },
  "edges": [
    {"from": "parent_id", "to": "child_id"}
  ]
}
```

#### 2. 生成故障树可视化
调用可视化脚本生成图形：
```bash
python scripts/fta_visualizer.py --input fta_data.json --output fault_tree.png
```

#### 3. 执行概率计算
```bash
python scripts/fta_calculator.py --input fta_data.json --output calc_result.json
```

#### 4. 生成分析报告
```bash
python scripts/fta_report.py --input fta_data.json --calc-result calc_result.json --output report.html
```

### 数据导入导出
- 导入：将外部格式转换为标准JSON：
  ```bash
  python scripts/fta_io.py --mode import --input source.yaml --output fta_data.json
  ```
- 导出：将JSON导出为其他格式：
  ```bash
  python scripts/fta_io.py --mode export --input fta_data.json --output export.yaml
  ```

## 使用示例

### 示例1：简单串联系统分析
- 场景/输入：用户描述"电机驱动系统包含电源、控制器、电机三个串联组件，故障率分别为0.01、0.02、0.03"
- 预期产出：故障树图形、顶事件概率（约0.059）、各组件重要性排序
- 关键要点：需将三个basic事件通过OR门连接到顶事件

### 示例2：复杂冗余系统分析
- 场景/输入：用户描述"双冗余系统，两个组件同时故障才导致系统失效"
- 预期产出：故障树图形、顶事件概率（两组件概率乘积）、最小割集分析
- 关键要点：使用AND门表示冗余逻辑

### 示例3：导入已有故障树数据
- 场景/输入：用户提供JSON/YAML格式的故障树数据
- 预期产出：可视化图形、分析报告
- 关键要点：数据需符合标准格式规范

## 资源索引
- 脚本:见 [scripts/fta_visualizer.py](scripts/fta_visualizer.py)(用途：生成故障树可视化图形)
- 脚本:见 [scripts/fta_calculator.py](scripts/fta_calculator.py)(用途：概率计算与重要性分析)
- 脚本:见 [scripts/fta_report.py](scripts/fta_report.py)(用途：生成HTML分析报告)
- 脚本:见 [scripts/fta_io.py](scripts/fta_io.py)(用途：故障树数据导入导出)
- 参考:见 [references/fta_format.md](references/fta_format.md)(何时读取：构建或解析故障树数据时)

## 注意事项
- 概率值应在0-1之间，接近0时可使用近似公式P≈λt（λ为故障率，t为运行时间）
- 重要性分析结果可指导质量改进优先级
- 最小割集越小说明系统越脆弱，需重点关注
- 导入导出支持JSON和YAML两种格式

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 10/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互；已声明安全注意事项 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **48/50** | 通过 |
