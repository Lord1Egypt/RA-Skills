"""
prompts.py — 一念紫微斗数 结构化AI解盘Prompt体系
四层Prompt：基础→进阶→高阶→专业
适配Claude/GPT（主）+ DeepSeek（备）

Author: 崽儿虾 🦞
"""

# ============================================================
# 系统提示词（各流派）
# ============================================================

SYSTEM_CORE = """你是一位精通紫微斗数的顶尖命理师，擅长「三派合一」综合解读。

【核心能力】
1. 三合派（中州派）：星曜性质 × 亮度 × 三方四正
2. 飞星派（钦天门）：宫干四化脉络 × 自化 × 追禄追忌
3. 占验派（紫云）：太岁入卦 × 特殊格局 × 星曜互涉

【输出铁律】
- 每层用【】标题，清晰分段
- 使用可能性语气，禁止绝对化断言
- 专业术语搭配白话解释
- 每段结尾标注"📜 文化参考，理性看待"
"""

SYSTEM_SANHE = SYSTEM_CORE + """
【三合派专用原则】
- 星曜亮度：庙>旺>得>利>平>陷
- 每宫必看：主星性质 + 三方四正联动 + 空宫借对宫
- 星组判断：紫府相(贵气)、杀破狼(变动)、机月同梁(才艺)
"""

SYSTEM_FEIXING = SYSTEM_CORE + """
【飞星派专用原则】
- 宫干四化：该宫天干向各宫飞化
- 自化：本宫天干四化入本宫
- 来因宫：年干所在宫位定轨迹起点
"""

SYSTEM_ZHANYAN = SYSTEM_CORE + """
【占验派专用原则】
- 太岁入卦：年干定位长期趋势
- 特殊格局：杀破狼格、紫府相格、日月同宫格等
"""

# ============================================================
# 四层Prompt构建器
# ============================================================

from typing import Dict, Any, Optional, List
from zwds_calc import AstrolabeResult, compute_surrounded


def build_basic_prompt(data: Dict[str, Any]) -> str:
    """第一层：基础逐宫解读"""
    lines = []
    lines.append("【第一层：基础宫位解读】")
    lines.append("请对以下命盘逐宫详细解读：")
    lines.append("")

    for p in data["palaces"]:
        ms = " ".join(
            f"{s['name']}({s['brightness']})" + (f"→{s['mutagen']}" if s.get('mutagen') else "")
            for s in p["major_stars"]
        )
        mins = " ".join(s["name"] for s in p["minor_stars"])
        empty = "【空宫（需借对宫星曜论断）】" if p["is_empty"] else ""

        lines.append(f"▪ {p['name_cn']}（{p['heavenly_stem']}{p['earthly_branch']}）")
        if p["major_stars"]:
            lines.append(f"  主星：{ms}")
        else:
            lines.append(f"  {empty}")
        if mins:
            lines.append(f"  辅星：{mins}")

        # 三方四正
        sur = compute_surrounded(p["index"])
        sur_names = [data["palaces"][i]["name_cn"] for i in sur]
        lines.append(f"  三方四正联：{'、'.join(sur_names)}")
        lines.append("")

    lines.append("【解读要求】")
    lines.append("• 每宫：主星性质 → 亮度影响 → 辅星增减 → 三方联动 → 整体判断")
    lines.append("• 空宫：说明借对宫哪颗星，以及借星后的格局")
    lines.append("• 关注星曜组合效应而非孤星论")
    lines.append("")

    return "\n".join(lines)


def build_advanced_prompt(data: Dict[str, Any]) -> str:
    """第二层：四化飞星与格局"""
    lines = []
    lines.append("【第二层：四化飞星与格局】")
    lines.append("")

    # 生年四化
    if data.get("mutagens"):
        lines.append("【生年四化分析】")
        mutagen_meanings = {
            "禄": ("增加·融合·顺遂", "该宫主题和谐顺畅，资源丰沛，为人生福气所在"),
            "权": ("主导·掌控·权威", "该宫主题主控性强，需担当但有压力，为人生发力所在"),
            "科": ("文雅·名声·调和", "该宫主题有文化气息，名声佳，为人缘加分所在"),
            "忌": ("缺失·纠葛·收缩", "该宫主题有缺憾，需格外经营，为人生的课题所在"),
        }
        for m in data["mutagens"]:
            meaning, detail = mutagen_meanings.get(m["mutagen"], ("", ""))
            lines.append(f"  {m['palace']}：{m['star']}化{m['mutagen']} → {meaning}")
            lines.append(f"    {detail}")
        lines.append("")

    # 来因宫
    if data.get("laiyin_palace"):
        lp = data["laiyin_palace"]
        lines.append(f"【来因宫】{lp['palace']}（年干{lp['year_stem']}定位）")
        lines.append(f"  人生轨迹的起点与方向由{lp['palace']}主题统领")
        lines.append("")

    # 格局识别
    if data.get("patterns"):
        lines.append("【特殊格局】")
        for pt in data["patterns"]:
            lines.append(f"  ▪ {pt['name']}：{pt['description']}")
        lines.append("")

    lines.append("【飞星四化脉络】")
    lines.append("  请分析以下四化脉络：")
    lines.append("  1. 禄权科忌在各宫之间的串联轨迹")
    lines.append("  2. 化忌的宫位是人生需要经营的课题")
    lines.append("  3. 化禄的宫位是人生福气与资源的所在")
    lines.append("  4. 四化飞星体现命运走势的强弱转换")
    lines.append("")

    lines.append("【六亲宫联动】")
    if data.get("six_relations"):
        for rel in data["six_relations"]:
            ms = "、".join(rel["major_stars"]) if rel["major_stars"] else "空宫"
            th = "、".join(rel["three_combined"])
            lines.append(f"  ▪ {rel['relation']}（{rel['palace']}）：{ms}  联动：{th}")
    lines.append("")

    return "\n".join(lines)


def build_timing_prompt(data: Dict[str, Any]) -> str:
    """第三层：大限流年"""
    lines = []
    lines.append("【第三层：大限与流年】")
    lines.append("")

    timing = data.get("timing", {})
    d = timing.get("current_decadal")
    if d:
        lines.append(f"【当前大限】{d['palace_name']}（{d['age_start']}-{d['age_end']}岁）")
        dp = timing.get("current_decadal_palace", {})
        if dp:
            ms = "、".join(s["name"] for s in dp.get("major", []))
            if ms:
                lines.append(f"  大限宫主星：{ms}")

            # 大限宫位在命盘上的星曜组合
            lines.append("")
            lines.append("  分析要点：")
            lines.append(f"  · 当前大限在{d['palace_name']}，该宫星曜组合主导未来十年")
            lines.append(f"  · 大限宫的三方四正联动宫位分析")
            lines.append(f"  · 大限四化对该宫位带来的影响")
        lines.append("")

    # 大限表
    if timing.get("decadal_sequence"):
        lines.append("【十年大运表】")
        for item in timing["decadal_sequence"]:
            mk = "👉" if item.get("is_current") else "  "
            lines.append(f"  {mk} {item['age_start']}-{item['age_end']}岁 → {item['palace_name']}")
        lines.append("")

    # 流年
    lines.append(f"【当前流年】{timing.get('current_year', '')}年（地支{timing.get('yearly_branch', '')}）")
    lines.append("  叠宫分析：大限宫位 × 流年地支宫位")
    lines.append("  · 流年地支对应的宫位星曜")
    lines.append("  · 大限与流年叠宫效应")
    lines.append("")

    return "\n".join(lines)


def build_professional_prompt(data: Dict[str, Any]) -> str:
    """第四层：专业深度"""
    lines = []
    lines.append("【第四层：专业深度解析】")
    lines.append("")

    # 体用宫
    ty = data.get("tiyong_palaces", {})
    if ty.get("body"):
        lines.append("【体用宫系统】")
        for b in ty["body"]:
            lines.append(f"  ▪ {b['name']}（{b['role']}）")
        lines.append(f"  分析：{ty.get('usage_analysis', '')}")
        lines.append("")

    # 煞星分布
    if data.get("sha_locations"):
        lines.append("【煞星分布与影响】")
        for si in data["sha_locations"]:
            lines.append(f"  ▪ {si['star']}坐{si['palace']}")
            impact = {
                "擎羊": "刑伤、冲突突破",
                "陀罗": "拖延、纠缠反复",
                "火星": "急躁、爆发式变动",
                "铃星": "暗斗、慢性纠纷",
                "地空": "理想化、空亡感",
                "地劫": "破耗、波折中断",
            }.get(si["star"], "凶星影响")
            lines.append(f"    影响：{impact}")
        lines.append("")

    lines.append("【三派综合论断】")
    lines.append("  请融合三派视角给出综合判断：")
    lines.append("  · 三合派：最重要的星曜组合与格局")
    lines.append("  · 飞星派：关键的四化脉络与自化学")
    lines.append("  · 占验派：时间维度上的引动节点")
    lines.append("")

    return "\n".join(lines)


# ============================================================
# 完整四层解盘Prompt组装
# ============================================================

def build_full_deep_prompt(
    chart_data: Dict[str, Any],
    deep_data: Dict[str, Any],
    target_year: int,
) -> str:
    """组装四层完整AI解盘Prompt"""
    lines = []

    # 命主信息
    fp = chart_data.get("four_pillars", {})
    lines.append(f"📅 命主：{fp.get('year', '')} {fp.get('month', '')} {fp.get('day', '')} {fp.get('hour', '')}")
    lines.append(f"🐉 生肖：{chart_data.get('zodiac', '')}　五行：{chart_data.get('five_elements', '')}")
    lines.append(f"🏠 命宫：{chart_data.get('palaces', [{}])[0].get('name_cn', '')}")
    lines.append("")

    # 整合deep_data中的数据
    basic_data = chart_data
    advanced_data = deep_data.get("advanced", {})
    timing_data = deep_data.get("timing", {})
    professional_data = deep_data.get("professional", {})
    
    # 把prof/adv数据注入
    basic_data["laiyin_palace"] = professional_data.get("laiyin_palace")
    basic_data["patterns"] = advanced_data.get("patterns", [])
    basic_data["six_relations"] = advanced_data.get("six_relations", [])
    basic_data["tiyong_palaces"] = professional_data.get("tiyong_palaces")
    basic_data["sha_locations"] = professional_data.get("star_interactions", [])
    basic_data["timing"] = timing_data

    # 逐层拼接
    sections = [
        ("第一层", build_basic_prompt(basic_data)),
        ("第二层", build_advanced_prompt(basic_data)),
        ("第三层", build_timing_prompt(basic_data)),
        ("第四层", build_professional_prompt(basic_data)),
    ]

    for name, section_text in sections:
        lines.append(section_text)

    # 最终指令
    lines.append("=" * 40)
    lines.append("【最终输出要求】")
    lines.append("请严格按照以下JSON格式输出解盘报告：")
    lines.append("""
{
  "report": {
    "metadata": {
      "four_pillars": "甲子 庚午 丁亥 丙午",
      "zodiac": "鼠",
      "five_elements": "水二局",
      "target_year": 2026,
      "current_decadal": "官禄宫 (42-51岁)"
    },
    "layers": {
      "basic": {
        "summary": "命盘整体格局简要判断",
        "palaces": [
          {
            "name": "命宫",
            "soul_stars": "紫微(平)",
            "interpretation": "紫微帝星独坐命宫，性格稳重有贵气...",
            "key_points": ["稳重有领导风范", "三方联动暗示..."]
          }
        ]
      },
      "advanced": {
        "mutagen_analysis": "生年四化脉络分析...",
        "patterns": ["杀破狼格局"],
        "six_relations": {"父母宫": "...", "夫妻宫": "..."}
      },
      "timing": {
        "current_decadal": "当前大限在官禄宫，星象暗示...",
        "yearly": "今年流年运势..."
      },
      "professional": {
        "laiyin_analysis": "来因宫分析...",
        "tiyong_analysis": "体用宫判断..."
      }
    },
    "conclusion": "综合判断与建议"
  }
}
""")
    lines.append("")
    lines.append("📜 文化参考，理性看待")

    return "\n".join(lines)


# ============================================================
# 模型适配器
# ============================================================

def adapt_prompt_for_model(prompt: str, model_type: str = "claude") -> str:
    """
    根据不同模型调整Prompt格式
    
    Args:
        model_type: "claude" | "gpt" | "deepseek"
    """
    if model_type == "deepseek":
        # DeepSeek对JSON结构更敏感
        prompt = prompt.replace("【", "<").replace("】", ">")
        prompt += "\n\n请确保输出为可直接解析的JSON格式。"
    elif model_type == "gpt":
        # GPT更喜欢结构化Markdown
        pass  # 默认格式就适合
    # Claude默认格式即Markdown最优
    
    return prompt


if __name__ == "__main__":
    # 测试构建prompt
    from deep_reading import full_deep_reading
    from zwds_calc import astrolabe_to_json, generate_astrolabe
    
    astro = generate_astrolabe("1984-6-22", 6, "男")
    deep = full_deep_reading("1984-6-22", 6, "男")
    
    if astro and deep["success"]:
        chart_data = astrolabe_to_json(astro)
        prompt = build_full_deep_prompt(chart_data, deep, 2026)
        print(f"✅ Prompt构建完成（{len(prompt)}字）")
        print(prompt[:1500])
        print(f"\n...（截断，共{len(prompt)}字）")
