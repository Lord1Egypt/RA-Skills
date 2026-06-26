#!/usr/bin/env python3
# i18n.py - Shared internationalization for skill-insight
# All output scripts import translations from here.

LANG_DEFAULT = "en"

TRANSLATIONS = {
    # report.py
    "report_title":         {"en": "Skill Usage Report",            "zh": "技能使用报告"},
    "generated":            {"en": "Generated:",                    "zh": "生成时间:"},
    "beijing_time":         {"en": "Beijing time",                 "zh": "北京时间"},
    "total_calls":          {"en": "Total calls:",                 "zh": "总调用次数:"},
    "active_skills":        {"en": "Active skills:",               "zh": "活跃技能数:"},
    "top_skills":           {"en": "TOP 3 Most Used Skills",       "zh": "TOP 3 最常用技能"},
    "unused_skills":        {"en": "Unused skills",               "zh": "未使用技能"},
    "and_n_others":         {"en": "and {n} others",              "zh": "及其他 {n} 个"},
    "call_unit":            {"en": "x",                           "zh": "次"},

    # analyze.py
    "analysis_title":       {"en": "Skill Usage Analysis Report", "zh": "技能使用分析报告"},
    "analyzed":             {"en": "Analyzed:",                   "zh": "分析时间:"},
    "period":               {"en": "Period:",                     "zh": "统计周期:"},
    "last_n_days":          {"en": "Last {n} days",              "zh": "最近 {n} 天"},
    "total_records":        {"en": "Total records:",              "zh": "总调用记录:"},
    "installed_skills":     {"en": "Installed skills:",            "zh": "已安装技能:"},
    "active":               {"en": "Active:",                     "zh": "活跃技能:"},
    "zero_use":             {"en": "Zero-use:",                   "zh": "零使用技能:"},
    "category":             {"en": "Category:",                   "zh": "分类:"},
    "calls":                {"en": "Calls:",                      "zh": "调用:"},
    "desc":                 {"en": "Desc:",                       "zh": "描述:"},
    "reasons":              {"en": "Reasons:",                    "zh": "原因:"},
    "keep":                 {"en": "Keep",                        "zh": "建议保留"},
    "review":               {"en": "Review",                     "zh": "建议审查"},
    "uninstall":            {"en": "Uninstall",                  "zh": "建议卸载"},
    "summary":              {"en": "Summary:",                    "zh": "总结:"},
    "uninstall_rec":        {"en": "Uninstall recommendations:", "zh": "卸载建议:"},
    "no_description":       {"en": "no description",             "zh": "无描述"},
    "none":                 {"en": "(none)",                     "zh": "(无)"},
    "period_days":          {"en": "Last {n} days",              "zh": "近 {n} 天"},

    # Reason tags
    "reason_core_category":  {"en": "core category({cat})",        "zh": "核心类别({cat})"},
    "reason_recently_used": {"en": "recently used {n}x",          "zh": "近期使用 {n} 次"},
    "reason_has_use_cases": {"en": "has specific use cases",      "zh": "有明确使用场景"},
    "reason_critical":      {"en": "critical infrastructure",    "zh": "关键基础设施技能"},
    "reason_scheduled":     {"en": "scheduled task (low trigger)", "zh": "定时任务技能(预期低对话触发)"},
    "reason_specialized":   {"en": "specialized skill",           "zh": "专业场景技能"},
    "reason_access_tool":   {"en": "access_type=tool (not in conversation logs)",  "zh": "access_type=tool(预期不出现在对话记录)"},
    "reason_access_script": {"en": "access_type=script (not in conversation logs)", "zh": "access_type=script(预期不出现在对话记录)"},
    "reason_zero_but_keep": {"en": "zero-call but may be needed", "zh": "零调用但可能需要保留"},
}

def t(key, lang=None, **kwargs):
    """Translate a key to the given language, falling back to English."""
    if lang is None:
        lang = LANG_DEFAULT
    val = TRANSLATIONS.get(key, {}).get(lang) or TRANSLATIONS.get(key, {}).get("en", key)
    if kwargs:
        val = val.format(**kwargs)
    return val

def detect_lang():
    """Detect language from LANG environment variable."""
    import os
    lang = os.environ.get("LANG") or os.environ.get("LC_ALL", "")
    if "zh" in lang.lower():
        return "zh"
    return "en"
CATEGORIES = {
    "development": {"en": "DEVELOPMENT",   "zh": "开发"},
    "agent":        {"en": "AGENT",          "zh": "智能体"},
    "security":     {"en": "SECURITY",        "zh": "安全"},
    "integration":  {"en": "INTEGRATION",     "zh": "集成"},
    "automation":   {"en": "AUTOMATION",      "zh": "自动化"},
    "utility":      {"en": "UTILITY",         "zh": "工具"},
    "search":       {"en": "SEARCH",          "zh": "搜索"},
    "vcs":          {"en": "VCS",             "zh": "版本控制"},
    "knowledge":     {"en": "KNOWLEDGE",       "zh": "知识"},
    "multimodal":   {"en": "MULTIMODAL",     "zh": "多模态"},
    "system":       {"en": "SYSTEM",          "zh": "系统"},
    "unknown":      {"en": "OTHER",           "zh": "其他"},
}
def cat_name(key, lang=None):
    """Translate a category key."""
    if lang is None:
        lang = LANG_DEFAULT
    return CATEGORIES.get(key, {}).get(lang, CATEGORIES.get(key, {}).get("en", key.upper()))
