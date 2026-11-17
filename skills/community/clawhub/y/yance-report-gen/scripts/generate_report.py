#!/usr/bin/env python3
"""
研策 · 综合投研报告生成器 v2
由5个角色的分析JSON（研木/研林/研技/研声/研盾）真实驱动生成综合投研报告。
输入缺失或字段不全时，相应板块明确标注「未提供数据（教学演示）」，不冒充真实分析。
"""
import json, sys, argparse, os
from datetime import datetime

ROLES = {
    "yanmu":    ("研木", "基本面深度分析", "基本面"),
    "yanlin":   ("研林", "产业与宏观背景", "产业策略"),
    "yanji":    ("研技", "技术面研判", "技术面"),
    "yansheng": ("研声", "舆情与市场情绪", "舆情"),
    "yandun":   ("研盾", "风险评估与仓位建议", "风控"),
}

def safe_load(path):
    """宽容加载JSON文件：不存在/解析失败返回None"""
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def deep_get(obj, *keys, default=None):
    """多路径取值：依次尝试每个键路径"""
    for kpath in keys:
        cur = obj
        ok = True
        for k in kpath.split("."):
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                ok = False
                break
        if ok and cur is not None:
            return cur
    return default

def extract_role_info(role, data):
    """从角色JSON中宽容提取：方向/置信度/摘要/详情，返回结构化信息"""
    if not isinstance(data, dict):
        return None
    info = {"provided": True, "direction": None, "confidence": None,
            "summary": None, "details": None, "rating": None}

    # 1) 统一格式: conclusion{direction,confidence,summary,time_horizon}
    direction = deep_get(data, "conclusion.direction", "overall_signal.direction",
                         "direction", default=None)
    confidence = deep_get(data, "conclusion.confidence", "overall_signal.confidence",
                          "confidence", default=None)
    summary = deep_get(data, "conclusion.summary", "overall_signal.description",
                       "summary", "description", default=None)
    details = deep_get(data, "details", default=None)
    # 2) 风控角色特殊结构: assessments.<code>.overall_risk / overall_score
    risk_level = None
    risk_score = None
    assessments = data.get("assessments")
    if isinstance(assessments, dict):
        for code, item in assessments.items():
            if isinstance(item, dict):
                risk_level = item.get("overall_risk") or risk_level
                risk_score = item.get("overall_score") if risk_score is None else risk_score
    if risk_level is None:
        risk_level = deep_get(data, "overall_risk", default=None)
    if risk_score is None:
        risk_score = deep_get(data, "overall_score", default=None)
    if risk_level:
        info["rating"] = f"风险等级 {risk_level}" + (f"（评分{risk_score}）" if risk_score is not None else "")
        # 风控方向映射：高/中高→negative，中→neutral，低→positive
        lv = str(risk_level)
        if "高" in lv:
            direction = "negative"
        elif "低" in lv:
            direction = "positive"
        else:
            direction = "neutral"
    # 3) 技术面角色: overall_technical_signal
    tech_signal = deep_get(data, "overall_technical_signal", default=None)
    if tech_signal and not direction:
        direction = "positive" if "多" in str(tech_signal) or "强" in str(tech_signal) else "neutral"
    # 4) 舆情角色: sentiment.sentiment_label / sentiment_score
    senti_label = deep_get(data, "sentiment.sentiment_label", default=None)
    if senti_label and not direction:
        direction = {"偏积极": "positive", "积极": "positive"}.get(str(senti_label), "neutral")
    # 5) 资金流角色: market_mood
    mood = deep_get(data, "market_mood", default=None)
    if mood and not direction:
        direction = {"偏暖": "positive", "暖": "positive", "偏冷": "negative", "冷": "negative"}.get(str(mood), "neutral")
    # 6) 通用字段: overall / verdict / signal
    for f in ("overall", "verdict", "signal", "conclusion_text"):
        v = deep_get(data, f, default=None)
        if v and not summary:
            summary = str(v)

    info["direction"] = direction
    info["confidence"] = confidence
    info["summary"] = str(summary)[:300] if summary else None
    info["details"] = str(details)[:500] if details else None
    return info

def direction_label(d):
    return {"positive": "看多", "neutral": "中性", "negative": "看空"}.get(d, "未评估")

def direction_score(d):
    return {"positive": 1, "neutral": 0, "negative": -1}.get(d, 0)

def star_rating(score):
    if score >= 0.6: return "★★★★★ 强烈推荐"
    if score >= 0.3: return "★★★★☆ 推荐"
    if score >= 0:   return "★★★☆☆ 中性观望"
    if score >= -0.3: return "★★☆☆☆ 谨慎回避"
    return "★☆☆☆☆ 明确回避"

def render_section(lines, title, info, stocks, extra_note=""):
    lines.append(f"## {title}")
    if info is None or not info.get("provided"):
        lines.append(f"> ⚠️ 未提供该角色分析数据（教学演示占位）。{extra_note}".rstrip(" "))
        lines.append("")
        return
    if info.get("summary"):
        lines.append(f"- 结论方向：**{direction_label(info['direction'])}**"
                     + (f" ｜ 置信度：{info['confidence']}" if info.get("confidence") is not None else ""))
        lines.append(f"- 核心观点：{info['summary']}")
    elif info.get("direction"):
        # 有方向但无摘要：如实输出方向结论
        lines.append(f"- 结论方向：**{direction_label(info['direction'])}**"
                     + (f" ｜ 置信度：{info['confidence']}" if info.get("confidence") is not None else "")
                     + "（该角色未提供详细摘要）")
    if info.get("details"):
        lines.append(f"- 详细分析：{info['details']}")
    if info.get("rating"):
        lines.append(f"- {info['rating']}")
    lines.append("")

def generate_report(report_files, stocks, output_dir):
    stocks_list = [s.strip() for s in stocks.split(",") if s.strip()] or ["（未指定标的）"]
    report_date = datetime.now().strftime("%Y-%m-%d")

    # 加载各角色数据
    data = {role: safe_load(report_files.get(role, "")) for role in ROLES}
    infos = {role: extract_role_info(role, d) for role, d in data.items()}

    # 综合评分（方向×置信度加权，风控否决）
    scores = {}
    for role in ROLES:
        info = infos[role]
        if info and info.get("direction"):
            base = direction_score(info["direction"])
            conf = info.get("confidence")
            bonus = 0.2 if (isinstance(conf, (int, float)) and conf >= 0.7) else (0 if isinstance(conf, (int, float)) else 0)
            scores[role] = base + bonus
    weights = {"yanmu": 0.30, "yanlin": 0.25, "yanji": 0.20, "yansheng": 0.15, "yandun": 0.10}
    total = sum(scores.get(r, 0) * weights[r] for r in ROLES)
    # 风控否决：risk为高时整体保守
    yandun_info = infos.get("yandun")
    veto = False
    if yandun_info and yandun_info.get("rating") and "高" in str(yandun_info.get("rating")):
        veto = True
        total = min(total, -0.5)

    lines = []
    lines.append(f"# 研家团自选股投研报告 ({report_date})")
    lines.append("")
    lines.append("> 由研家团 · 研策综合投顾合成输出")
    lines.append("> 数据来源：研木（基本面）+ 研林（产业策略）+ 研技（技术面）+ 研声（舆情）+ 研盾（风控）")
    lines.append("> 本报告由各角色分析JSON驱动生成；标注「教学演示占位」的板块表示对应输入缺失。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 一、综述
    lines.append("## 一、投研观点综述")
    for s in stocks_list:
        lines.append(f"- **{s}**：综合评级 **{star_rating(total)}**"
                     + ("（⚠️ 研盾风控否决生效：整体结论保守）" if veto else ""))
    lines.append("")

    # 二~六、各板块
    render_section(lines, "二、基本面深度分析（研木）", infos["yanmu"], stocks_list)
    render_section(lines, "三、产业与宏观背景（研林）", infos["yanlin"], stocks_list)
    render_section(lines, "四、技术面研判（研技）", infos["yanji"], stocks_list)
    render_section(lines, "五、舆情与市场情绪（研声）", infos["yansheng"], stocks_list)
    render_section(lines, "六、风险评估与仓位建议（研盾）", infos["yandun"], stocks_list)

    # 七、综合评级表
    lines.append("## 七、综合评级与操作建议（研策）")
    lines.append("| 标的 | 综合评分 | 综合评级 | 风控否决 |")
    lines.append("|------|---------|---------|---------|")
    for s in stocks_list:
        lines.append(f"| {s} | {total:+.2f} | {star_rating(total)} | {'是' if veto else '否'} |")
    lines.append("")
    lines.append("> ⚠️ 免责声明：本报告由课程教学智能体生成，仅供教学演示，不构成任何投资建议。")

    report = "\n".join(lines)
    filename = f"研家团投研报告_{report_date}.md"
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已生成: {filepath}")
    else:
        print(report)
    return {"filename": filename, "content": report, "date": report_date, "score": total}

def main():
    parser = argparse.ArgumentParser(description="研策·综合投研报告生成器（由各角色JSON驱动）")
    for role in ROLES:
        parser.add_argument(f"--{role}-report", default="", help=f"{role}分析结果JSON文件路径")
    parser.add_argument("--output", default=".", help="输出目录")
    parser.add_argument("--stocks", default="", help="标的列表（逗号分隔）")
    args = parser.parse_args()

    report_files = {role: getattr(args, f"{role}_report") for role in ROLES}
    result = generate_report(report_files, args.stocks, args.output)
    if args.output != ".":
        print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
