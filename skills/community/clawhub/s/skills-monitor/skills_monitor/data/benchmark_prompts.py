"""
分类基准评测 Prompt 模板 v0.5.0
================================
为 ClawHub 15 个分类定义标准化评测 Prompt。
每个 Prompt 模板接受 {task} 占位符，由具体 Skill 的 benchmark_task 填入。

使用:
    from skills_monitor.data.benchmark_prompts import get_benchmark_prompt
    prompt = get_benchmark_prompt("data_processing", "分析销售数据...")
"""

from typing import Dict, Optional

# ──────── task_type → Prompt 模板 ────────

BENCHMARK_PROMPT_TEMPLATES: Dict[str, str] = {

    "search_and_summarize": (
        "你是一个专业的信息检索与摘要助手。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 返回结构化 JSON 结果\n"
        "2. 每条结果包含: title, url, summary (50 字以内), relevance_score (0-1)\n"
        "3. 按相关度降序排列\n"
        "4. 附带一段 100 字以内的综合摘要\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "results": [...], "summary": "..." }}\n'
        "```"
    ),

    "translation": (
        "你是一个专业的多语言翻译助手，精通中英日韩等主流语言。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 翻译准确、自然，符合目标语言表达习惯\n"
        "2. 保留专业术语，必要时附注原文\n"
        "3. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "original": "...", "translations": {{ "en": "...", "ja": "...", "ko": "..." }} }}\n'
        "```"
    ),

    "file_operation": (
        "你是一个文件系统操作专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 给出具体的命令或脚本\n"
        "2. 处理异常情况（权限不足、文件不存在等）\n"
        "3. 返回结构化 JSON 结果\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "commands": [...], "expected_output": {{ ... }}, "error_handling": "..." }}\n'
        "```"
    ),

    "code_analysis": (
        "你是一个资深软件工程师，擅长代码审查和性能分析。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 系统性分析，覆盖正确性、性能、安全性、可维护性\n"
        "2. 每个问题给出严重程度（critical/warning/info）\n"
        "3. 提供具体的修复代码\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "issues": [{{ "severity": "...", "description": "...", "fix": "..." }}], '
        '"overall_score": 0-100, "summary": "..." }}\n'
        "```"
    ),

    "api_query": (
        "你是一个 API 数据查询专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 返回结构化数据\n"
        "2. 数据字段完整，格式统一\n"
        "3. 标注数据来源和时间\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "data": [...], "source": "...", "queried_at": "..." }}\n'
        "```"
    ),

    "data_processing": (
        "你是一个数据分析专家，精通统计分析和数据可视化。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 给出完整的分析步骤\n"
        "2. 计算结果精确到小数点后 2 位\n"
        "3. 提供数据解读和建议\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "analysis": {{ ... }}, "metrics": {{ ... }}, "insights": [...], "recommendations": [...] }}\n'
        "```"
    ),

    "document_processing": (
        "你是一个文档处理专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 保持文档结构的完整性\n"
        "2. 正确处理各种格式元素\n"
        "3. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "content": {{ ... }}, "metadata": {{ ... }}, "summary": "..." }}\n'
        "```"
    ),

    "text_formatting": (
        "你是一个 Markdown 排版专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 符合 CommonMark 规范\n"
        "2. 结构清晰，格式正确\n"
        "3. 返回纯 Markdown 文本\n\n"
        "## 输出\n直接返回格式化后的 Markdown 文本。"
    ),

    "text_generation": (
        "你是一个专业的文案写作助手。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 内容准确、逻辑清晰\n"
        "2. 语言得体，符合场景要求\n"
        "3. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "content": "...", "word_count": 0, "key_points": [...] }}\n'
        "```"
    ),

    "code_generation": (
        "你是一个全栈开发工程师。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 代码可直接运行\n"
        "2. 包含必要注释\n"
        "3. 覆盖边界情况\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "code": "...", "language": "...", "test_cases": [...], "explanation": "..." }}\n'
        "```"
    ),

    "config_generation": (
        "你是一个 DevOps / 基础设施配置专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 配置可直接使用\n"
        "2. 遵循最佳实践\n"
        "3. 包含注释说明\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "config": "...", "format": "...", "notes": [...] }}\n'
        "```"
    ),

    "sql_generation": (
        "你是一个数据库专家，精通 SQL 和 NoSQL 查询优化。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. SQL 语法正确，兼容主流数据库\n"
        "2. 考虑性能（索引、执行计划）\n"
        "3. 附带解释说明\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "query": "...", "explanation": "...", "optimization_notes": [...] }}\n'
        "```"
    ),

    "financial_analysis": (
        "你是一个专业的金融量化分析师。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 分析逻辑严谨，数据来源可追溯\n"
        "2. 风险提示明确\n"
        "3. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "analysis": {{ ... }}, "recommendations": [...], "risk_warning": "..." }}\n'
        "```"
    ),

    "workflow_design": (
        "你是一个系统架构师，擅长工作流设计和自动化方案。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 流程步骤清晰，有明确的输入输出\n"
        "2. 考虑异常处理和重试机制\n"
        "3. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "steps": [{{ "name": "...", "input": "...", "output": "...", "error_handling": "..." }}], '
        '"estimated_time": "...", "dependencies": [...] }}\n'
        "```"
    ),

    "media_processing": (
        "你是一个多媒体处理专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 给出完整的处理流程\n"
        "2. 推荐最优的工具/库\n"
        "3. 考虑性能和质量平衡\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "pipeline": [...], "tools": [...], "quality_settings": {{ ... }} }}\n'
        "```"
    ),

    "nlp_analysis": (
        "你是一个 NLP / AI 工程师。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 分析方法论清晰\n"
        "2. 结果可量化\n"
        "3. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "results": [...], "method": "...", "confidence": 0.0 }}\n'
        "```"
    ),

    "security_task": (
        "你是一个网络安全专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 分析全面，不遗漏关键风险点\n"
        "2. 严重程度分级（critical/high/medium/low）\n"
        "3. 给出具体修复方案\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "findings": [{{ "severity": "...", "description": "...", "fix": "..." }}], '
        '"overall_risk": "...", "score": 0-100 }}\n'
        "```"
    ),

    "api_testing": (
        "你是一个 API 测试工程师。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 测试用例完整，覆盖正常和异常场景\n"
        "2. 请求格式规范（含 headers、body、params）\n"
        "3. 预期响应明确\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "test_cases": [{{ "method": "...", "url": "...", "headers": {{ }}, '
        '"body": {{ }}, "expected_status": 200, "expected_response": {{ }} }}] }}\n'
        "```"
    ),

    "calculation": (
        "你是一个数学求解专家。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 给出详细的解题步骤\n"
        "2. 最终答案明确\n"
        "3. 附带验证过程\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "solution": {{ "steps": [...], "answer": "...", "verification": "..." }} }}\n'
        "```"
    ),

    "troubleshooting": (
        "你是一个高级运维工程师。\n\n"
        "## 任务\n{task}\n\n"
        "## 要求\n"
        "1. 排查步骤系统化\n"
        "2. 覆盖常见原因\n"
        "3. 给出具体解决命令/操作\n"
        "4. 返回结构化 JSON\n\n"
        "## 输出格式\n"
        "```json\n"
        '{{ "diagnosis": {{ "symptoms": [...], "possible_causes": [...], '
        '"troubleshooting_steps": [...], "solution": "..." }} }}\n'
        "```"
    ),
}


def get_benchmark_prompt(task_type: str, task: str) -> str:
    """
    获取评测 Prompt

    Args:
        task_type: 任务类型 (对应 top50 dataset 中的 task_type)
        task: 具体任务描述 (对应 benchmark_task)

    Returns:
        完整的评测 Prompt 文本
    """
    template = BENCHMARK_PROMPT_TEMPLATES.get(
        task_type,
        BENCHMARK_PROMPT_TEMPLATES.get("text_generation")  # 默认降级
    )
    return template.format(task=task)


def get_available_task_types() -> list:
    """获取所有可用的任务类型"""
    return sorted(BENCHMARK_PROMPT_TEMPLATES.keys())
