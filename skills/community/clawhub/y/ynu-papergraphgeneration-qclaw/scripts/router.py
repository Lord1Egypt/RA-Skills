"""
router.py - 论文可视化路由判断
判断用户想要哪种类型的图，并从论文中提取对应章节的内容
"""

# 图类型常量
TYPE_TEASER = "teaser"          # 概念图/动机图 - Abstract/Introduction
TYPE_ARCHITECTURE = "architecture"  # 主框架图/架构图 - Methodology
TYPE_FLOWCHART = "flowchart"    # 算法流程图 - Methodology (伪代码)
TYPE_ENVIRONMENT = "environment" # 实验环境图 - Experimental Setup
TYPE_RESULTS = "results"        # 结果对比图 - Results (不用生图，用 Matplotlib)


def classify_figure_type(llm_call_fn, user_intent: str, paper_content: str) -> str:
    """
    根据用户意图 + 论文内容判断生成哪种图
    """
    prompt = f"""你是一个学术论文图表分类专家。根据用户的描述和论文内容，判断用户想要生成哪种类型的学术插图。

请从以下 5 种类型中选择最合适的一个（只输出类型名称，不要任何解释）：

1. **teaser** - 概念图/动机图：展示研究动机、痛点对比、应用场景
   关键词：动机、痛点、对比、概念、应用场景、头图、宣传图

2. **architecture** - 主框架图/系统架构图：展示模型整体结构、模块组成、数据流向
   关键词：架构、框架、模型结构、模块、pipeline、系统图

3. **flowchart** - 算法流程图：展示算法的执行步骤、条件分支、循环逻辑
   关键词：算法、流程、步骤、伪代码、loop、if-else、循环

4. **environment** - 实验环境图：展示智能体与环境的交互、状态空间、任务定义
   关键词：环境、交互、智能体、任务、setup、强化学习、游戏

5. **results** - 结果对比图：展示实验数据、柱状图、折线图、性能对比
   关键词：结果、对比、实验、图表、柱状图、折线图、ablation、metric

用户意图：{user_intent}

论文摘要（前 1500 字）：
{paper_content[:1500]}

请只输出一个词：teaser / architecture / flowchart / environment / results"""

    try:
        result = llm_call_fn(prompt).strip().lower()
        valid_types = {TYPE_TEASER, TYPE_ARCHITECTURE, TYPE_FLOWCHART, TYPE_ENVIRONMENT, TYPE_RESULTS}
        # 提取：LLM 可能返回 "architecture" 或 "1. architecture" 等
        for t in valid_types:
            if t in result:
                return t
        return TYPE_ARCHITECTURE  # 最常见的默认
    except Exception:
        return TYPE_ARCHITECTURE  # fallback


def extract_section(user_intent: str, paper_content: str, figure_type: str) -> dict:
    """
    根据图类型，从论文中提取对应章节的结构化内容
    """
    extract_prompt = f"""你是一个学术论文结构化信息提取专家。请从以下论文内容中提取生成【{{figure_type_label}}】所需的关键信息。

## 任务
根据图类型「{{figure_type_label}}」，重点阅读以下对应章节：
{{target_sections}}

## 论文内容
{{paper_content}}

## 输出要求
请以 JSON 格式输出，字段如下（根据图类型选择相关字段）：

### 如果是 teaser（概念图/动机图）：
{{
  "pain_point": "现有方法的痛点/缺陷",
  "proposed_solution": "本文提出的核心解决方案",
  "input_output": {{"input": "系统输入", "output": "系统输出"}},
  "application_scenario": "应用场景",
  "highlight": "最核心的创新点一句话"
}}

### 如果是 architecture（主框架图）：
{{
  "title": "图表标题（如：Model Overview）",
  "modules": [
    {{"name": "模块名称", "type": "encoder|decoder|attention|fc|embedding|normalization|other", "sub_modules": ["子模块列表"]}}
  ],
  "data_flow": [
    {{"from": "模块A", "to": "模块B", "label": "数据/特征"}}
  ],
  "stacks": {{"encoder_layers": N, "decoder_layers": N, "heads": N}},
  "key_components": ["关键组件列表，用于标注"]
}}

### 如果是 flowchart（算法流程图）：
{{
  "title": "图表标题（如：Training Procedure）",
  "steps": [
    {{"id": 1, "text": "步骤描述", "condition": null, "loop": null, "next": 2}},
    {{"id": 2, "text": "if [条件]", "condition": "条件分支", "next_true": 3, "next_false": 4}}
  ],
  "start": "开始节点",
  "end": "结束节点"
}}

### 如果是 environment（实验环境图）：
{{
  "task_name": "任务名称",
  "agent_description": "智能体描述",
  "state_space": "状态空间",
  "action_space": "动作空间",
  "interaction_loop": ["交互步骤序列"],
  "reward_signal": "奖励信号描述"
}}

### 如果是 results（结果对比图）：
{{
  "datasets": ["数据集列表"],
  "metrics": ["评价指标列表，如：Accuracy, F1, BLEU"],
  "baselines": ["基线模型列表"],
  "proposed_method": "本文方法名",
  "key_results": {{"数据集名": {{"metric": value}}}},
  "highlight": "最突出的结果亮点"
}}

请只输出 JSON，不要任何额外文字：
"""

    section_map = {
        TYPE_TEASER: "摘要 (Abstract) 和 引言 (Introduction)",
        TYPE_ARCHITECTURE: "方法论 (Methodology / Proposed Method) 的整体概述段落",
        TYPE_FLOWCHART: "方法论 (Methodology) 中的算法伪代码部分",
        TYPE_ENVIRONMENT: "实验设置 (Experimental Setup / Task Definition)",
        TYPE_RESULTS: "实验结果 (Results / Experiments) 章节",
    }

    figure_label_map = {
        TYPE_TEASER: "概念图/动机图 (Teaser Figure)",
        TYPE_ARCHITECTURE: "主框架图/系统架构图 (Architecture Diagram)",
        TYPE_FLOWCHART: "算法流程图 (Flowchart)",
        TYPE_ENVIRONMENT: "实验环境图 (Environment Diagram)",
        TYPE_RESULTS: "结果对比图 (Results Chart)",
    }

    target_sections = section_map.get(figure_type, "")
    figure_label = figure_label_map.get(figure_type, figure_type)

    formatted_prompt = extract_prompt.format(
        figure_type_label=figure_label,
        target_sections=target_sections,
        paper_content=paper_content[:8000]  # 限制字数避免 token 爆炸
    )

    return {
        "figure_type": figure_type,
        "figure_label": figure_label,
        "target_sections": target_sections,
        "extract_prompt": formatted_prompt
    }


def route(llm_call_fn, user_intent: str, paper_content: str) -> dict:
    """
    主路由函数：判断图类型 + 提取对应内容
    返回路由结果供后续模块使用
    """
    # 判断图类型
    figure_type = classify_figure_type(llm_call_fn, user_intent, paper_content)

    # 提取对应章节内容
    extraction = extract_section(user_intent, paper_content, figure_type)

    return {
        "figure_type": figure_type,
        "figure_label": extraction["figure_label"],
        "target_sections": extraction["target_sections"],
        "extract_prompt": extraction["extract_prompt"],
        "user_intent": user_intent
    }
