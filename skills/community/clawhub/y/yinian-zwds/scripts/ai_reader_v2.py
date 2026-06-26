"""
ai_reader_v2.py — 一念紫微斗数 AI解盘引擎 v2
多模型支持（Claude/GPT/DeepSeek），输出标准JSON解盘报告

Author: 崽儿虾 🦞
"""

from typing import Optional, Dict, Any, List, Tuple
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zwds_calc import generate_astrolabe, astrolabe_to_json
from deep_reading import full_deep_reading
from prompts import (
    build_full_deep_prompt,
    adapt_prompt_for_model,
    SYSTEM_SANHE, SYSTEM_FEIXING, SYSTEM_ZHANYAN,
)


# ============================================================
# AI模型调用层（适配OpenClaw框架）
# ============================================================

def call_ai_model(
    system_prompt: str,
    user_prompt: str,
    model_type: str = "auto",
    temperature: float = 0.5,
) -> str:
    """
    调用AI模型进行解盘
    
    在OpenClaw框架内运行时，由框架处理实际API调用。
    此处返回格式化后的prompt供框架读取。
    
    Args:
        model_type: "auto"（框架自动选择）| "claude" | "gpt" | "deepseek"
        temperature: 0.0-1.0，越低越保守
    """
    # 组合成完整请求
    full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
    
    if model_type == "deepseek":
        full_prompt = adapt_prompt_for_model(full_prompt, "deepseek")
    
    return full_prompt


def _clean_json_response(raw: str) -> str:
    """清理模型返回的JSON（去除多余markdown）"""
    raw = raw.strip()
    # 去除 ```json ``` 包裹
    if raw.startswith("```"):
        lines = raw.split("\n")
        content = []
        started = False
        for line in lines:
            if line.strip().startswith("```"):
                started = not started
                continue
            if started:
                content.append(line)
        if content:
            return "\n".join(content)
    return raw


# ============================================================
# 解盘报告解析器
# ============================================================

def parse_reading_report(raw_output: str) -> Dict[str, Any]:
    """解析模型返回的解盘文本为结构化数据"""
    cleaned = _clean_json_response(raw_output)
    
    # 尝试JSON解析
    try:
        report = json.loads(cleaned)
        return report
    except json.JSONDecodeError:
        pass
    
    # 如果不是标准JSON，按文本分段解析
    return _parse_text_report(cleaned)


def _parse_text_report(text: str) -> Dict[str, Any]:
    """解析自由文本格式的解盘报告"""
    sections = {}
    current_section = "intro"
    current_text = []
    
    for line in text.split("\n"):
        # 检测JSON结构
        if '"name"' in line and '"interpretation"' in text:
            # 尝试JSON解析所有{}
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(text[start:end])
            except:
                pass
        
        # 按层解析
        for layer in ["第一层", "第二层", "第三层", "第四层", "basic", "advanced", "timing", "professional", "conclusion"]:
            if layer in line.lower() and ("【" in line or ":" in line or "Layer" in line):
                if current_text:
                    sections[current_section] = "\n".join(current_text)
                current_section = layer
                current_text = []
                break
        else:
            current_text.append(line)
    
    if current_text:
        sections[current_section] = "\n".join(current_text)
    
    return {"report": {"layers": sections}}


# ============================================================
# 标准化解盘报告生成
# ============================================================

def generate_standard_report(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    target_year: Optional[int] = None,
    model_type: str = "auto",
) -> Dict[str, Any]:
    """
    全流程：排盘 → 深度数据 → 构建Prompt → 调用AI → 输出JSON报告
    
    Returns:
        {
            "success": bool,
            "chart_json": {...},           # 命盘JSON
            "ai_prompt": "...",            # 发送给AI的Prompt
            "report": {...},               # AI返回的解盘JSON报告
            "report_text": "...",          # 纯文本版本
            "model_type": "claude",
        }
    """
    from datetime import datetime
    
    if not target_year:
        target_year = datetime.now().year
    
    # 1. 排盘 + 深度数据
    astro = generate_astrolabe(date_str, hour, gender, is_lunar)
    if not astro:
        return {"success": False, "error": "排盘失败"}
    
    deep = full_deep_reading(date_str, hour, gender, is_lunar, target_year)
    if not deep["success"]:
        return {"success": False, "error": "深度分析失败"}
    
    chart_data = astrolabe_to_json(astro)
    
    # 2. 构建Prompt
    school = "综合"
    system_prompt = SYSTEM_CORE
    
    prompt = build_full_deep_prompt(chart_data, deep, target_year)
    full_prompt = call_ai_model(system_prompt, prompt, model_type)
    
    return {
        "success": True,
        "chart_json": chart_data,
        "deep_data": deep,
        "ai_prompt": full_prompt,
        "model_type": model_type,
        "system_prompt": system_prompt,
    }


# ============================================================
# 解盘结果格式化（Telegram友好）
# ============================================================

def format_report_for_tg(report: Dict[str, Any]) -> str:
    """把解盘报告格式化为Telegram可读文本"""
    lines = []
    
    # 元数据
    meta = report.get("report", {}).get("metadata", {})
    if meta:
        lines.append(f"🔮 *一念紫微斗数 · 深度解盘*")
        lines.append(f"📅 四柱：{meta.get('four_pillars', '')}")
        lines.append(f"🐉 大限：{meta.get('current_decadal', '')}")
        lines.append("")
    
    # 各层解读
    layers = report.get("report", {}).get("layers", {})
    
    if "basic" in layers:
        basic = layers["basic"]
        lines.append("*🥇 基础宫位解读*")
        if isinstance(basic, dict):
            lines.append(basic.get("summary", ""))
            for p in basic.get("palaces", []):
                name = p.get("name", "")
                interp = p.get("interpretation", "")
                if name and interp:
                    lines.append(f"▪ {name}：{interp[:200]}")
        elif isinstance(basic, str):
            lines.append(basic[:500])
        lines.append("")
    
    if "advanced" in layers:
        adv = layers["advanced"]
        lines.append("*🥈 四化格局分析*")
        if isinstance(adv, dict):
            lines.append(adv.get("mutagen_analysis", ""))
        elif isinstance(adv, str):
            lines.append(adv[:500])
        lines.append("")
    
    if "timing" in layers:
        timing = layers["timing"]
        lines.append("*🥉 大限流年*")
        if isinstance(timing, dict):
            lines.append(timing.get("current_decadal", ""))
        elif isinstance(timing, str):
            lines.append(timing[:500])
        lines.append("")
    
    if "professional" in layers:
        prof = layers["professional"]
        lines.append("*🏆 专业深度*")
        if isinstance(prof, dict):
            lines.append(prof.get("laiyin_analysis", ""))
        elif isinstance(prof, str):
            lines.append(prof[:500])
        lines.append("")
    
    # 结论
    conclusion = report.get("report", {}).get("conclusion", "")
    if conclusion:
        lines.append("*📝 综合论断*")
        lines.append(conclusion[:300] if len(str(conclusion)) > 300 else str(conclusion))
        lines.append("")
    
    lines.append("━━━━━━━━━━━━━━")
    lines.append("📜 *文化参考，理性看待*")
    
    return "\n".join(lines)


# 系统核心提示词（供外部调用）
SYSTEM_CORE = """你是一位精通紫微斗数的顶尖命理师，擅长三派合一综合解读。

【核心能力】
1. 三合派（中州派）：星曜性质 × 亮度 × 三方四正
2. 飞星派（钦天门）：宫干四化脉络 × 自化 × 追禄追忌
3. 占验派（紫云）：太岁入卦 × 特殊格局 × 星曜互涉

【输出要求】
- 严格按照JSON格式输出报告
- 每层用清晰结构，包含summary和详情
- 专业术语搭配白话解释
- 使用可能性语气，禁止绝对化断言
- 结语标注：📜 文化参考，理性看待"""


if __name__ == "__main__":
    import sys
    
    date = sys.argv[1] if len(sys.argv) > 1 else "1984-6-22"
    hour = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    gender = sys.argv[3] if len(sys.argv) > 3 else "男"
    
    result = generate_standard_report(date, hour, gender)
    
    if result["success"]:
        print(f"✅ 解盘准备就绪")
        print(f"📊 Prompt长度: {len(result['ai_prompt'])} 字")
        print(f"🤖 模型: {result['model_type']}")
        print()
        print("🔮 系统提示词（前300字）:")
        print(result["system_prompt"][:300])
        print()
        print("━" * 30)
        print("📝 用户Prompt（前1000字）:")
        print(result["ai_prompt"][:1000])
    else:
        print(f"❌ {result.get('error')}")
