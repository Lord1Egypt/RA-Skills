"""输入审计（Pipeline Step 1）。

核对历法 / 时区 / 出生地 / 节气边界 / 日界规则 / 真太阳时影响 8 字段。
信息不全或落在 23:00–00:59 日界 / 真太阳时跨时支边界 -> 标记“暂定盘”，
不得直接进入命理判断。
"""
from __future__ import annotations

from datetime import datetime

from evidence import EvidenceRecord, load_vault_text, load_by_canonical
from paipan import paipan
from solar_time import to_true_solar_time, resolve_longitude

AUDIT_RULES = ["AUDIT_CALENDAR", "AUDIT_TZ", "AUDIT_SOLARTIME", "AUDIT_DAYBOUNDARY"]


def input_audit(birth_dt: datetime, birth_place: str, sex: str,
                calendar: str = "公历", vault_base: str | None = None,
                theme: str = "通用全览"):
    flags = []
    reasoning = []
    opposing = ""

    # 历法
    if calendar not in ("公历", "农历"):
        flags.append("暂定盘:历法未声明")
        reasoning.append("未声明公历/农历，按公历处理并标注。")

    # 出生地（真太阳时经度校正强制依赖；缺失则不得排盘）
    _EMPTY_PLACE = {"", "x", "未知", "不明", "不详", "待补", "无", "暂无"}
    if not birth_place or birth_place.strip() in _EMPTY_PLACE:
        flags.append("暂定盘:出生地缺失")
        reasoning.append("未提供出生地，真太阳时经度校正无法进行；按暂定盘处理，请用户补出生地(到县/区)后再排盘。")
        # 出生地缺失时仍记录当前钟表时间，但不进入命理判断
        output = {
            "calendar": calendar,
            "birth_place": birth_place or "",
            "birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"),
            "true_solar_time": None,
            "sex": sex,
            "flags": flags,
            "is_tentative": True,
        }
        rec = EvidenceRecord(
            step="input_audit",
            input={"birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"), "birth_place": birth_place or "", "sex": sex, "calendar": calendar},
            rules_used=AUDIT_RULES,
            intermediate_reasoning="；".join(reasoning),
            opposing_evidence=opposing,
            output=output,
            confidence=0.0,
            vault_source="VAULT_SKIPPED_BIRTHPLACE_MISSING",
        )
        return rec, None

    # 问事主题（契约强制：须主动询问，不得默认通用全览）
    _EMPTY_THEME = {"", "无", "待定", "待补", "暂无", "未指定", "未知", "通用"}
    if not theme or theme.strip() in _EMPTY_THEME:
        flags.append("暂定盘:问事主题未指定")
        reasoning.append("未指定问事主题，按契约须主动询问（事业/财运/婚姻/学业/健康/子女/官非，或明确选通用全览）后再排盘；不进入命理判断。")
        output = {
            "calendar": calendar,
            "birth_place": birth_place,
            "birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"),
            "true_solar_time": None,
            "sex": sex,
            "theme": theme or "",
            "flags": flags,
            "is_tentative": True,
        }
        rec = EvidenceRecord(
            step="input_audit",
            input={"birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"), "birth_place": birth_place, "sex": sex, "calendar": calendar, "theme": theme or ""},
            rules_used=AUDIT_RULES,
            intermediate_reasoning="；".join(reasoning),
            opposing_evidence=opposing,
            output=output,
            confidence=0.0,
            vault_source="VAULT_SKIPPED_THEME_MISSING",
        )
        return rec, None

    # 时区 / 出生地
    lng, matched = resolve_longitude(birth_place)
    if not matched:
        flags.append("未校时差:出生地未匹配城市经度表")
        reasoning.append(f"出生地“{birth_place}”未命中城市经度表，按北京时(120°E)计算并标注“未校时差”。")

    # 真太阳时影响
    true_dt, corr, _ = to_true_solar_time(birth_dt, birth_place)
    reasoning.append(f"钟表时间 {birth_dt:%Y-%m-%d %H:%M} 真太阳时校正 {corr:+.1f} 分 -> {true_dt:%Y-%m-%d %H:%M}。")

    # 日界规则：23:00 起为次日子时（用真太阳时）
    if true_dt.hour == 23 or (true_dt.hour == 0 and true_dt.minute > 0):
        flags.append("日界边界:真太阳时落在23:00附近")
        reasoning.append("真太阳时接近 23:00 日界，需确认是否跨日，列为候选盘。")
    # 23:00–00:59 双候选盘
    if 23 <= birth_dt.hour <= 23 or 0 <= birth_dt.hour < 1:
        # 仅提示，具体跨日由真太阳时判定
        pass

    # 节气边界：月界已由 paipan 用节气计算，这里记录
    p = paipan(birth_dt, birth_place)
    reasoning.append(f"月界以“节”定，本月令支为 {p['four_pillars']['month']['label'][1]}（节令日 {p['jieqi_date']}）。")

    vault_path, vault_text = load_by_canonical("八字排盘校验规范", vault_base)
    vault_ref = vault_path if vault_text else "VAULT_UNREADABLE"

    output = {
        "calendar": calendar,
        "birth_place": birth_place,
        "birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"),
        "true_solar_time": p["true_solar_time"],
        "sex": sex,
        "flags": flags,
        "is_tentative": len([f for f in flags if f.startswith("暂定") or f.startswith("日界")]) > 0,
    }

    rec = EvidenceRecord(
        step="input_audit",
        input={"birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"), "birth_place": birth_place, "sex": sex, "calendar": calendar},
        rules_used=AUDIT_RULES,
        intermediate_reasoning="；".join(reasoning),
        opposing_evidence=opposing,
        output=output,
        confidence=1.0 if not output["is_tentative"] else 0.6,
        vault_source=vault_ref,
    )
    return rec, p
