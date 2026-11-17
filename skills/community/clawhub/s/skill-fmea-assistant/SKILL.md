---
name: FMEA分析技能
slug: fmea-assistant
displayName: FMEA分析技能
description: 辅助FMEA 2019版分析；帮助用户完成失效模式识别、RPN计算、风险等级评估与预防措施跟踪；支持DFMEA、PFMEA、SFMEA全场景
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# FMEA 分析助手

## 任务目标
- 本 Skill 用于：产品/过程可靠性分析，支持完整FMEA工作流程
- 能力包含：流程指引 | 表格输入 | RPN计算 | 风险评估 | 措施跟踪
- 触发条件：用户需要进行FMEA分析、评估产品风险或跟踪改进措施

## 前置准备
- Python 依赖：openpyxl==3.1.2（用于Excel表格操作）
- 无需额外系统命令
- 输出目录：当前工作目录下的 `fmea_output/`

## 操作步骤

### 完整FMEA分析流程

#### 1. 准备阶段
- 明确分析范围：系统、子系统、组件
- 确定分析边界与假设条件
- 组建跨职能团队
- 收集设计输入、历史数据、类似FMEA参考

#### 2. 功能分析
- 识别每个组件的功能
- 建立功能树/功能框图
- 定义功能参数与性能指标

#### 3. 潜在失效模式识别
- 针对每个功能识别可能的失效模式
- 失效模式回答：什么情况下会失效？
- 常见类型：功能丧失、部分丧失、意外功能

#### 4. 影响分析
- 评估每个失效模式的影响
- 严重度(S)评分：1-10级
- 失效影响的严重程度量化

#### 5. 预防措施制定
- 预防措施：降低发生概率
- 探测措施：提高发现概率
- 严重度由失效后果决定，不可降低

#### 6. RPN计算与风险评估
```bash
python scripts/fmea_calculator.py --action calculate --severity 8 --occurrence 5 --detection 3
```
- 输出：RPN值与风险等级建议

#### 7. FMEA表格管理
```bash
python scripts/fmea_tracker.py --action create --project "项目名称"
python scripts/fmea_tracker.py --action add --project "项目名称" --item "组件A" --function "功能描述" --failure "失效模式" --severity 8 --occurrence 5 --detection 3
python scripts/fmea_tracker.py --action list --project "项目名称"
python scripts/fmea_tracker.py --action recommend --severity 8 --occurrence 5 --detection 3
python scripts/fmea_tracker.py --action export --project "项目名称"
```

## 使用示例

### 示例1：快速RPN计算
- 场景/输入：已知 S=8, O=5, D=3
- 预期产出：RPN=120，风险等级=高
- 关键要点：根据2019版标准评估是否需要优化

### 示例2：完整FMEA项目分析
- 场景/输入：创建新项目，添加多个分析项
- 预期产出：结构化的FMEA表格文件
- 关键要点：按流程逐步完成分析，使用推荐措施

### 示例3：风险优化决策
- 场景/输入：当前RPN偏高，需要识别优先改进项
- 预期产出：按RPN排序的改进优先级清单
- 关键要点：S不可降低，优先优化O和D

## 资源索引
- 脚本:见 [scripts/fmea_calculator.py](scripts/fmea_calculator.py)(用途:RPN计算与风险评估，参数:--action/--severity/--occurrence/--detection)
- 脚本:见 [scripts/fmea_tracker.py](scripts/fmea_tracker.py)(用途:FMEA表格管理与预防措施跟踪，参数:--action/--project及多项分析数据)
- 参考:见 [references/fmea_format.md](references/fmea_format.md)(何时读取:创建FMEA表格前或需要格式规范时)

## 风险等级判定规则

| RPN范围 | 风险等级 | 建议行动 |
|---------|---------|---------|
| 1-20 | 低 | 可接受，无需立即行动 |
| 21-60 | 中 | 建议改善，列入观察 |
| 61-100 | 高 | 需要改善措施 |
| 101-200 | 很高 | 必须采取改善行动 |
| 201-1000 | 极高 | 立即采取行动，考虑重新设计 |

## 2019版FMEA核心变化
- 5步法替代7步法：聚焦于标准化工作流程
- 强调基础分析 vs. 补充分析的分离
- 强调元FMEA（FMEA for FMEA）
- 强调高层审查与签署
- 增加P图（Parameter Diagram）作为功能分析工具

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 10/10 | 有清晰工作流程; 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **48/50** | 通过 |
