# 协议

ThoughtCodec 建立在两个互补协议之上：解压协议与压缩协议。

## 解压协议

当输入是高密度、抽象、战略性或尚未充分展开的信息，而期望结果是可执行计划或制品时，使用解压协议。

### 输入

```json
{
  "intent_abstract": "高密度目标或想法。",
  "context": "相关背景、约束、用户和环境。",
  "success_criteria": ["可观察结果 1", "可观察结果 2"],
  "constraints": ["边界 1", "边界 2"],
  "preferred_output": "SOP、架构、代码脚手架、清单、图表或文档"
}
```

### 输出

```json
{
  "version": "V1.0.0",
  "logic_core": {
    "workflow_nodes": [
      {
        "step": 1,
        "action": "具体动作",
        "input": "所需输入",
        "output": "预期输出",
        "validation": "该步骤的检查方式"
      }
    ]
  },
  "presentation_layer": {
    "format": "Markdown、Mermaid、JSON、代码目录树或表格",
    "display_rules": "仅包含呈现规则，不包含业务计算"
  }
}
```

## 压缩协议

当输入是嘈杂、重复、纠错性或操作性的材料，而期望结果是可复用规则或 Skill 时，使用压缩协议。

### 输入

```json
{
  "source_material": "对话历史、diff、日志、代码、审阅记录或重复决策。",
  "observed_problem": "反复出错或重复发生的事项。",
  "human_correction": "用户修改或澄清的内容。",
  "reuse_target": "提示词规则、Skill、组件、清单或策略"
}
```

### 输出

```json
{
  "rule_id": "简短稳定的规则 ID",
  "layer": "L1_Presentation | L2_Application | L3_Logic | L4_Base_Protocol",
  "rule": "以指令形式表达的可复用规则。",
  "evidence": ["证据项 1", "证据项 2"],
  "regression_checks": ["防止错误泛化的回归检查"],
  "version_patch": "V1.0.1-draft"
}
```

## 四层自进化模型

| 层级 | 范围 | 示例 |
| --- | --- | --- |
| L1 表现层 | 输出风格与格式 | Markdown 排版、表格形状、语气规则 |
| L2 应用层 | 工具或领域使用方式 | Codex 工作流、Claude 写作、RPA 数据源规则 |
| L3 逻辑层 | 核心决策逻辑 | 计划规则、验证策略、数据流转 |
| L4 底层协议 | 不可轻易改变的系统原则 | 隐私、安全、计算与表现分离 |

新规则应先作为草稿补丁进入系统。L3 与 L4 的变化会影响大量下游任务，因此需要显式审核。

## 智能体闭环

```text
任务输入
  -> 解压
  -> 执行
  -> 结果采集
  -> 压缩门
  -> 回归检查
  -> 合并或回滚
```

这个闭环的作用是避免系统把每一次纠错都直接当作通用真理。修改意见会先变成草稿补丁，经过检查后再沉淀为长期规则。
