"""
topology_extractor.py - 将结构化提取结果转为 Mermaid 拓扑描述
"""


def build_teaser_topology(extraction_result: str, style: str = "academic") -> str:
    """
    生成 teaser（概念图/动机图）的 Mermaid 拓扑
    """
    prompt = f"""你是一个专业的学术图表工程师。根据以下提取的结构化信息，生成一个 Mermaid flowchart 描述。

## 要求
- 输出必须是合法的 Mermaid flowchart LR 或 TB 语法
- 使用简洁的英文节点描述（每个节点文字不超过 10 个词）
- 包含节点之间的箭头连接
- 用 subgraph 分组相关概念
- 不要有任何中文字符

## 风格
- academic: 干净简洁，适合顶会论文
- 先展示痛点（旧方法），再展示本文解决方案（新方法）
- 使用对比色区分旧方法（红色调）和新方法（蓝色调）

## 输出格式
只输出 Mermaid 代码，不要任何解释，格式如下：
```mermaid
flowchart LR
    style old_method fill:#ffcccc
    style new_method fill:#cce5ff
    ...
```

## 提取的信息
{extraction_result}
"""
    return prompt


def build_architecture_topology(extraction_result: str, style: str = "academic") -> str:
    """
    生成 architecture（主框架图）的 Mermaid 拓扑
    这是最核心的模块！
    """
    prompt = f"""你是一个专业的学术图表工程师。根据以下提取的结构化信息，生成一个精确的 Mermaid flowchart LR（从左到右）拓扑描述。

## 严格规则
1. **输出必须是合法的 Mermaid 代码**，直接可以被渲染
2. **所有节点 ID 必须是唯一的英文标识符**（如 enc1, att1, dec1）
3. **所有节点 label 使用方括号** `[label text]`
4. **箭头格式**：`A-->B` 或 `A-->|label|B`
5. **绝对不能有任何中文字符**
6. **节点内文字要简洁**，每个节点不超过 8 个英文单词
7. **用 subgraph 分层**：Input/Encoder/Decoder/Output
8. **数据流向必须清晰**：严格从左到右

## 节点样式建议（通过 Mermaid 语法）
```
classDef encoder fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
classDef decoder fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
classDef attention fill:#FFF8E1,stroke:#F9A825,stroke-width:2px
classDef io fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
classDef fc fill:#FBE9E7,stroke:#BF360C,stroke-width:2px
class A classDef
```

## 提取的结构化信息
{extraction_result}

请直接输出 Mermaid 代码：
"""
    return prompt


def build_flowchart_topology(extraction_result: str, style: str = "academic") -> str:
    """
    生成 flowchart（算法流程图）的 Mermaid 拓扑
    """
    prompt = f"""你是一个专业的学术图表工程师。根据以下提取的算法流程信息，生成一个 Mermaid flowchart TD（从上到下）拓扑描述。

## 严格规则
1. **输出必须是合法的 Mermaid flowchart TD 代码**
2. **使用圆角矩形表示普通步骤**：`[Step description]`
3. **使用菱形表示条件分支**：`{{condition?}}`
4. **使用椭圆形表示开始/结束**：`([Start])` / `([End])`
5. **循环用 subgraph 包裹并加粗边框**
6. **绝对不能有任何中文字符**
7. **每步描述不超过 10 个英文单词**

## 提取的算法步骤
{extraction_result}

请直接输出 Mermaid 代码：
"""
    return prompt


def build_environment_topology(extraction_result: str, style: str = "academic") -> str:
    """
    生成 environment（实验环境图）的 Mermaid 拓扑
    """
    prompt = f"""你是一个专业的学术图表工程师。根据以下提取的实验环境信息，生成一个 Mermaid flowchart LR（从左到右）拓扑描述。

## 严格规则
1. **输出必须是合法的 Mermaid 代码**
2. **展示 Agent-Environment 交互闭环**
3. **用不同颜色区分 Agent 和 Environment**
4. **绝对不能有任何中文字符**
5. **节点标签简洁，每个不超过 8 个英文单词**

## 风格
- Agent 节点用蓝色调
- Environment 节点用绿色调
- 交互箭头加 label 表示交互类型（state/action/reward）

## 提取的环境信息
{extraction_result}

请直接输出 Mermaid 代码：
"""
    return prompt


def convert_to_topology(figure_type: str, extraction_result: str, style: str = "academic") -> str:
    """
    主入口：根据图类型分发到对应的拓扑生成器
    """
    if figure_type == "teaser":
        return build_teaser_topology(extraction_result, style)
    elif figure_type == "architecture":
        return build_architecture_topology(extraction_result, style)
    elif figure_type == "flowchart":
        return build_flowchart_topology(extraction_result, style)
    elif figure_type == "environment":
        return build_environment_topology(extraction_result, style)
    else:
        # 默认用架构图
        return build_architecture_topology(extraction_result, style)
