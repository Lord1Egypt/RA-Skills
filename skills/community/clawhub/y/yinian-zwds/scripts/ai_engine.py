"""
ai_engine.py — 一念紫微斗数 AI解盘执行引擎
真正的AI模型调用 + 完整解盘输出 + 流年流月运势

Author: 崽儿虾 🦞
"""

from typing import Optional, Dict, Any, List
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_reader_v2 import generate_standard_report
from deep_reading import full_deep_reading
from zwds_calc import generate_astrolabe, astrolabe_to_json, compute_surrounded, BRANCH_TO_INDEX
from decadal import calculate_decadal_sequence


# ============================================================
# AI API 调用器（DeepSeek / OpenAI兼容）
# ============================================================

# API Key优先级：DeepSeek环境变量 > OpenClaw配置DeepSeekKey > OpenAI环境变量
import json

def _resolve_api_key():
    """解析API Key，优先DeepSeek"""
    # 1. DeepSeek环境变量
    ds_env = os.environ.get("DEEPSEEK_API_KEY", "")
    if ds_env:
        return ds_env
    
    # 2. OpenClaw配置中的DeepSeek Key
    _cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(_cfg_path):
        try:
            with open(_cfg_path) as _f:
                _cfg = json.load(_f)
            _providers = _cfg.get("models", {}).get("providers", {})
            _key = _providers.get("deepseek", {}).get("apiKey", "")
            if _key:
                return _key
        except:
            pass
    
    # 3. 降级到OpenAI（但仅当key不是sk-proj-格式时才用）
    oa_env = os.environ.get("OPENAI_API_KEY", "")
    if oa_env and not oa_env.startswith("sk-proj-"):
        return oa_env
    
    return ""

AI_API_KEY = _resolve_api_key()
# DeepSeek API（国内可直连）
AI_BASE_URL = "https://api.deepseek.com/v1"
AI_MODEL = "deepseek-chat"


def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    """
    调用大模型 API 进行AI解盘
    自动检测使用 DeepSeek 或 OpenAI
    """
    import urllib.request
    import urllib.error
    
    api_key = AI_API_KEY
    base_url = AI_BASE_URL
    model = AI_MODEL
    
    if not api_key:
        return "⚠️ 未找到AI API Key，请配置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY"
    
    # DeepSeek对中文格式更友好
    if "deepseek" in model:
        system_prompt = system_prompt.replace("【", "<").replace("】", ">")
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            return content
    except Exception as e:
        return f"⚠️ AI调用失败: {str(e)}"


# ============================================================
# 完整解盘（排盘 → AI解读 → 输出报告）
# ============================================================

def ai_reading(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    target_year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    端到端：出生信息 → 排盘 → 深度数据 → AI解读 → 格式化报告
    
    Returns:
        {
            "success": True/False,
            "chart_json": {...},
            "ai_raw": "AI原始输出文本",
            "ai_report": {...} or parsed dict,
            "telegram_text": "适合Telegram发送的文本",
            "error": "...",
        }
    """
    # 1. 生成Prompt
    result = generate_standard_report(
        date_str, hour, gender, is_lunar, target_year, model_type="deepseek"
    )
    if not result["success"]:
        return {"success": False, "error": result.get("error", "排盘失败")}
    
    # 2. 调用AI
    system_prompt = result["system_prompt"]
    user_prompt = result["ai_prompt"]
    
    ai_raw = call_llm(system_prompt, user_prompt)
    
    # 3. 解析AI输出
    report_parsed = _parse_ai_output(ai_raw)
    
    # 4. 格式化为Telegram文本
    tg_text = _format_reading_for_tg(
        result["chart_json"],
        report_parsed,
        result.get("deep_data", {}),
        ai_raw,
    )
    
    return {
        "success": True,
        "chart_json": result["chart_json"],
        "ai_raw": ai_raw,
        "ai_report": report_parsed,
        "telegram_text": tg_text,
    }


def _parse_ai_output(raw: str) -> Dict[str, Any]:
    """解析AI返回的JSON或文本报告"""
    # 先尝试JSON解析
    text = raw.strip()
    
    # 去除 ```json ``` 包裹
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{") and part.endswith("}"):
                try:
                    return json.loads(part)
                except:
                    continue
    
    # 直接找 JSON 对象
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end+1])
        except:
            pass
    
    # 无法解析，返回原始文本
    return {"raw_text": text}


def _format_reading_for_tg(
    chart_json: Dict,
    ai_report: Dict,
    deep_data: Dict,
    ai_raw: str,
) -> str:
    """格式化为Telegram友好文本（无markdown表格，无headings）"""
    lines = []
    lines.append("🔮 *紫微斗数 · AI深度解盘*")
    lines.append("")
    
    # 命主信息
    fp = chart_json.get("four_pillars", {})
    lines.append(f"📅 四柱：{fp.get('year','')} {fp.get('month','')} {fp.get('day','')} {fp.get('hour','')}")
    lines.append(f"🐉 五行局：{chart_json.get('five_elements','')}  命宫：{chart_json.get('palaces',[{}])[0].get('name_cn','')}")
    
    # 大限信息
    timing = deep_data.get("timing", {})
    d = timing.get("current_decadal")
    if d:
        lines.append(f"📍 当前大限：{d['palace_name']}（{d['age_start']}-{d['age_end']}岁）")
    lines.append("")
    
    # 生年四化
    if chart_json.get("mutagens"):
        m_strs = [f"{m['palace']}: {m['star']}化{m['mutagen']}" for m in chart_json["mutagens"]]
        lines.append(f"✨ 生年四化：{'｜'.join(m_strs)}")
        lines.append("")
    
    lines.append("━━━━━━━━━━━━")
    lines.append("")
    
    # AI解盘正文
    if isinstance(ai_report, dict) and "report" in ai_report:
        r = ai_report["report"]
        layers = r.get("layers", {})
        
        # 基础层
        basic = layers.get("basic", {})
        if isinstance(basic, dict):
            summary = basic.get("summary", "")
            if summary:
                lines.append(f"**命盘格局**")
                lines.append(summary)
                lines.append("")
            
            palaces = basic.get("palaces", [])
            if palaces:
                lines.append("**分宫解读**")
                for p in palaces:
                    name = p.get("name", "")
                    interp = p.get("interpretation", "")
                    if name and interp:
                        lines.append(f"▪ {name}：{_truncate(interp, 200)}")
                lines.append("")
        
        # 进阶层
        adv = layers.get("advanced", {})
        if isinstance(adv, dict):
            ma = adv.get("mutagen_analysis", "")
            pats = adv.get("patterns", [])
            if ma:
                lines.append(f"**四化脉络**")
                lines.append(_truncate(ma, 300))
                lines.append("")
            if pats:
                pstr = "、".join(pats) if isinstance(pats, list) else str(pats)
                lines.append(f"**格局**：{pstr[:200]}")
                lines.append("")
        
        # 高阶层
        tm = layers.get("timing", {})
        if isinstance(tm, dict):
            cd = tm.get("current_decadal", "")
            if cd:
                lines.append(f"**大限流年**")
                lines.append(_truncate(cd, 300))
                lines.append("")
        
        # 专业层
        prof = layers.get("professional", {})
        if isinstance(prof, dict):
            laiyin = prof.get("laiyin_analysis", "")
            tiyong = prof.get("tiyong_analysis", "")
            if laiyin:
                lines.append(f"**来因宫**：{_truncate(laiyin, 200)}")
            if tiyong:
                lines.append(f"**体用宫**：{_truncate(tiyong, 200)}")
            if laiyin or tiyong:
                lines.append("")
        
        # 结论
        conclusion = r.get("conclusion", "")
        if conclusion:
            lines.append(f"**综合判断**")
            lines.append(_truncate(conclusion, 400))
            lines.append("")
    
    else:
        # AI返回自由文本
        text = ai_raw.strip()
        if text:
            # 去除过大篇幅
            if len(text) > 3000:
                text = text[:3000] + "\n\n...（以下省略）"
            lines.append(text)
            lines.append("")
    
    lines.append("━" * 14)
    lines.append("📜 文化参考，理性看待")
    
    return "\n".join(lines)


def _truncate(text: str, max_len: int = 200) -> str:
    """截断文本并添加省略号"""
    if not text:
        return ""
    text = str(text)
    return text[:max_len] + "…" if len(text) > max_len else text


# ============================================================
# 流年/流月运势
# ============================================================

def generate_monthly_reading(
    date_str: str,
    hour: int,
    gender: str,
    target_year: int,
    target_month: int,
) -> Dict[str, Any]:
    """
    流月运势分析
    
    Args:
        target_month: 1-12
    """
    astro = generate_astrolabe(date_str, hour, gender)
    if not astro:
        return {"success": False, "error": "排盘失败"}
    
    deep = full_deep_reading(date_str, hour, gender, target_year=target_year)
    timing = deep.get("timing", {})
    
    # 流月地支
    monthly_branch_map = {
        1: "寅", 2: "卯", 3: "辰", 4: "巳", 5: "午", 6: "未",
        7: "申", 8: "酉", 9: "戌", 10: "亥", 11: "子", 12: "丑",
    }
    month_branch = monthly_branch_map[target_month]
    
    # 流月对应的宫位（命宫为0标准序）
    # 地支→标准宫序映射
    branch_to_std = {"寅": 0, "卯": 1, "辰": 2, "巳": 3, "午": 4, "未": 5,
                     "申": 6, "酉": 7, "戌": 8, "亥": 9, "子": 10, "丑": 11}
    # 需要映射回标准宫序——先看命宫地支
    soul_branch = _branch_value(astro.soul_palace_branch)
    soul_branch_idx = BRANCH_TO_INDEX.get(soul_branch, 0)
    
    # 流月对应标准宫序 = (月地支的iztro索引 - 命宫iztro索引) % 12 再转标准
    month_branch_idx = BRANCH_TO_INDEX.get(month_branch, 0)
    raw_offset = (month_branch_idx - soul_branch_idx) % 12
    palace_idx = raw_offset  # 在标准序中的索引
    
    palace = astro.palaces[palace_idx] if 0 <= palace_idx < len(astro.palaces) else None
    
    if not palace:
        return {"success": False, "error": f"找不到流月对应的宫位"}
    
    # 构建流月分析Prompt
    majors = [f"{s.name}({s.brightness})" + (f"→{s.mutagen}" if s.mutagen else "") for s in palace.major_stars]
    minors = [s.name for s in palace.minor_stars]
    
    mstr = "、".join(majors) if majors else "空宫"
    mistr = "、".join(minors) if minors else "无辅星"
    
    d = timing.get("current_decadal", {})
    decadal_info = f"{d['palace_name']}（{d['age_start']}-{d['age_end']}岁）" if d else "未知"
    
    prompt = f"""你是一位紫微斗数命理师。请简析以下流月运势：

年份：{target_year}年{target_month}月
地支：{month_branch}
当前大限：{decadal_info}

流月宫位：{palace.name_cn}
主星：{mstr}
辅星：{mistr}
空宫：{"是（需借对宫）" if palace.is_empty else "否"}

请给出以下信息（每条50字以内）：
1. 本月运势核心提示
2. 需要注意的领域
3. 有利的发力方向
"""
    
    system = "你是紫微斗数命理师。简短回复，每条不超过50字。使用可能性语气。📜"
    ai_resp = call_llm(system, prompt, temperature=0.5, max_tokens=800)
    
    return {
        "success": True,
        "year": target_year,
        "month": target_month,
        "month_branch": month_branch,
        "palace_name": palace.name_cn,
        "major_stars": mstr,
        "minor_stars": mistr,
        "is_empty": palace.is_empty,
        "analysis": ai_resp,
    }


def _branch_value(branch: str) -> str:
    """获取地支的字符串值，确保兼容各种输入"""
    if not branch:
        return "子"
    return branch


# ============================================================
# 流年详尽运势
# ============================================================

def generate_yearly_reading(
    date_str: str,
    hour: int,
    gender: str,
    target_year: int,
) -> Dict[str, Any]:
    """
    流年详尽运势分析
    """
    astro = generate_astrolabe(date_str, hour, gender)
    if not astro:
        return {"success": False, "error": "排盘失败"}
    
    deep = full_deep_reading(date_str, hour, gender, target_year=target_year)
    timing = deep.get("timing", {})
    
    # 流年地支
    year_offset = (target_year - 1984) % 12
    branch_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    year_branch = branch_list[year_offset]
    
    # 流年所在标准宫序
    soul_branch = _branch_value(astro.soul_palace_branch)
    soul_branch_idx = BRANCH_TO_INDEX.get(soul_branch, 0)
    year_branch_idx = BRANCH_TO_INDEX.get(year_branch, 0)
    raw_offset = (year_branch_idx - soul_branch_idx) % 12
    palace_idx = raw_offset
    
    palace = astro.palaces[palace_idx] if 0 <= palace_idx < len(astro.palaces) else None
    
    d = timing.get("current_decadal", {})
    decadal_info = f"{d['palace_name']}（{d['age_start']}-{d['age_end']}岁）" if d else "未知"
    
    # 叠宫：大限宫位 × 流年宫位
    decadal_pi = d.get("palace_index", 0) if d else 0
    overlay = f"大限{astro.palaces[decadal_pi].name_cn}叠流年{astro.palaces[palace_idx].name_cn}" if palace else "无法计算"
    
    majors_str = ""
    minors_str = ""
    empty_str = ""
    
    if palace:
        majors = [f"{s.name}({s.brightness})" + (f"→{s.mutagen}" if s.mutagen else "") for s in palace.major_stars]
        minors = [s.name for s in palace.minor_stars]
        majors_str = "、".join(majors) if majors else "空宫"
        minors_str = "、".join(minors) if minors else "无辅星"
        empty_str = "【该宫为空宫，需借对宫星曜论断】" if palace.is_empty else ""
    
    prompt = f"""请以紫微斗数流年视角解读以下运势：

基础信息：
- {target_year}年（地支{year_branch}）流年运势
- 当前大限：{decadal_info}
- 叠宫：{overlay}

流年宫位详情：
- 宫位：{palace.name_cn if palace else "未知"}
- 主星：{majors_str}
- 辅星：{minors_str}
- {empty_str}

请从以下五个维度分析（每项60字以内）：
1. 事业：工作发展的机会与挑战
2. 财运：收入波动与投资时机
3. 感情：人际关系与姻缘走向
4. 健康：身体状况注意点
5. 建议：本年行动指南
"""
    
    system = "你是紫微斗数命理师。逐项简短回答。使用可能性语气。📜"
    ai_resp = call_llm(system, prompt, temperature=0.5, max_tokens=1200)
    
    return {
        "success": True,
        "year": target_year,
        "year_branch": year_branch,
        "decadal": decadal_info,
        "overlay": overlay,
        "palace": palace.name_cn if palace else "未知",
        "analysis": ai_resp,
    }


# ============================================================
# 完整AI解盘 + 流年整合
# ============================================================

def full_reading_with_yearly(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    target_year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    完整命盘解盘 + 流年运势（一次生成）
    """
    from datetime import datetime
    if not target_year:
        target_year = datetime.now().year
    
    # 主命盘解盘
    main = ai_reading(date_str, hour, gender, is_lunar, target_year)
    if not main["success"]:
        return main
    
    # 流年运势
    yearly = generate_yearly_reading(date_str, hour, gender, target_year)
    
    # 合并Telegram文本
    tg_text = main.get("telegram_text", "")
    
    if yearly.get("success"):
        tg_text += "\n\n"
        tg_text += f"━━━ 📅 {target_year}年流年运势 ━━━\n\n"
        tg_text += yearly.get("analysis", "")
        tg_text += "\n\n📜 文化参考，理性看待"
    
    # 流月（当前月）
    current_month = datetime.now().month
    monthly = generate_monthly_reading(date_str, hour, gender, target_year, current_month)
    
    if monthly.get("success"):
        tg_text += f"\n\n━━━ 🌙 {target_year}年{current_month}月流月 ━━━\n\n"
        tg_text += f"宫位：{monthly['palace_name']}（地支{monthly['month_branch']}）\n"
        tg_text += f"星曜：{monthly['major_stars']}\n"
        tg_text += monthly.get("analysis", "")
        tg_text += "\n\n📜 文化参考，理性看待"
    
    return {
        "success": True,
        "telegram_text": tg_text,
        "chart_json": main.get("chart_json"),
        "yearly": yearly,
        "monthly": monthly,
    }


if __name__ == "__main__":
    import sys
    
    date = sys.argv[1] if len(sys.argv) > 1 else "1984-6-22"
    hour = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    gender = sys.argv[3] if len(sys.argv) > 3 else "男"
    
    print(f"🔮 南曦命盘完整解盘 + 流年流月")
    print(f"=" * 40)
    
    result = full_reading_with_yearly(date, hour, gender)
    
    if result["success"]:
        print(result["telegram_text"])
    else:
        print(f"❌ {result.get('error')}")
