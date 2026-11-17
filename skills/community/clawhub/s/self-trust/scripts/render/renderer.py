"""renderer — 确定性文本渲染器（替代 LLM 手工排版）

把 CLI 输出的结构化 JSON 渲染成带 §0.5 骨架的人可见格式化回执。
所有命令统一骨架：
    {prefix}{命令标签}·{结果词} 🕐[YYYY-MM-DD HH:MM GMT+8]
    ============================================
    {命令专属正文，逐行}
    ============================================
    {上下文行：按需}

本文件不依赖任何外部库，纯标准库。"""
from __future__ import annotations
# ================================================================
# pylint: disable=too-many-branches,too-many-return-statements

import datetime
from typing import Any

from core.i18n import zh_status

SEP: str = "=" * 44
"""分隔线：44 个等号（仅用于顶部 + 标题下，§0.5）"""
SEP_CTX: str = "-" * 44
"""正文↔上下文分隔线：44 个短横（§0.5 规定，区分「正文块」与「上下文行」，非 =）"""


# ── 工具函数 ────────────────────────────────────────────────────

def _fmt(v: float) -> str:
    """§0.1 金额格式：¥ + 千分位 + 2 位小数"""
    return f"¥{v:,.2f}"


def _now_ts(today: datetime.date | None = None) -> str:
    """生成时间戳 🕐[YYYY-MM-DD HH:MM GMT+8]"""
    base = today or datetime.date.today()
    now = datetime.datetime.now().time()
    dt = datetime.datetime.combine(base, now)
    return dt.strftime("🕐[%Y-%m-%d %H:%M GMT+8]")


def _ts_from(r: dict) -> str:
    """从结果 dict 中提取日期生成时间戳"""
    d = r.get("date")
    if d:
        try:
            return _now_ts(datetime.date.fromisoformat(str(d)[:10]))
        except (ValueError, TypeError):
            pass
    return _now_ts()


# ── 头部生成 ────────────────────────────────────────────────────

_HDR = "{prefix}{label}{ts}"


def _header(prefix: str, label: str, ts: str) -> str:
    return f"{prefix}{label}{ts}"


# ── §1 / §11 审批（judge submit）─────────────────────────────────

def _render_judge_submit(r: dict, ts: str) -> str:
    dec = r.get("decision", {})
    inp = r.get("inputs", {})
    basis = inp.get("monthly_basis")
    imp = r.get("impacted_objectives", [])
    cd = r.get("cooldown", {})
    scene = dec.get("scene", "?")
    result_word = dec.get("result", "?")

    amount = inp.get("amount", 0)
    category = inp.get("category", "")
    cushion = inp.get("effective_cushion", 0)
    corpus = inp.get("corpus", 0)
    remaining = inp.get("remaining_after", 0)
    cooldown_t = cd.get("triggered", False)
    days = cd.get("days", 3)
    request_id = r.get("request_id", "")
    expire_at = r.get("expire_at", "")
    obj_name = imp[0].get("name") if imp else None
    delay_simple = r.get("impact", {}).get("delay_months_simple", 0)
    summary = dec.get("summary", "")

    # 前缀映射
    prefix_map = {"A": "✅", "B": "📋", "C": "📋"}
    prefix = prefix_map.get(scene, "📋")

    if not cooldown_t and scene == "A":
        # A-1 / A-3 紧凑卡片（§11.1）
        lines = [
            _header(prefix, "审批·批准", ts),
            SEP,
        ]
        # 消费行
        lines.append(f"{_fmt(amount)} {category}")
        # 判定行（§11.2：impacted_objectives 空→不受损；非空→显示延迟）
        if imp:
            parts = []
            for o in imp:
                nm = o.get("name", "目标")
                dly = o.get("delay_months_simple", delay_simple)
                parts.append(f"{nm}约{_fmt_months(dly)}个月")
            lines.append(f"安全垫 {_fmt(cushion)} 之上 · {'、'.join(parts)}（简化口径，误差 ±20%~50%）")
        else:
            lines.append(f"安全垫 {_fmt(cushion)} 之上 · 目标不受损")
        # 账本行
        lines.append(f"账本 {_fmt(corpus)} → {_fmt(remaining)}")
        lines.append(SEP)
        return "\n".join(lines)

    # A-2（有冷却）/ B / C → 长模板（§1.4）
    lines = [_header(prefix, f"审批·{result_word}", ts), SEP]

    if scene == "B":
        lines.append(f"契约对照：{summary}")
    elif scene == "C":
        lines.append(f"契约对照：{summary}")
        lines.append(f"目标影响：{obj_name or '目标'} 延后约 {_fmt_months(delay_simple)}（简化口径，误差 ±20%~50%）")
    else:
        # A-2
        lines.append(f"契约对照：{summary}")

    if obj_name and scene != "C":
        lines.append(f"目标影响：{obj_name} 延后约 {_fmt_months(delay_simple)}（简化口径，误差 ±20%~50%）")

    if cooldown_t:
        if expire_at and request_id:
            lines.append(f"冷静期 {days} 天，到期 {expire_at}（编号 {request_id}）")
        else:
            lines.append(f"冷静期 {days} 天，到期终裁（§2.3）")

    # §1.5 毛口径提示行：仅 B/C/冷静期 且 毛口径时追加（小额直批 A 不刷屏）
    if basis == "gross_estimate" and (scene in ("B", "C") or cooldown_t):
        lines.append("⚠️ 月净流入为毛口径估算，安全垫/基线偏高"
                     "（说『记账自定义·补负债』或『补刚性』即净口径化）")

    lines.append(SEP)
    return "\n".join(lines)


# ── §2 冷静期生命周期 ───────────────────────────────────────────

def _render_judge_withdraw(r: dict, ts: str) -> str:
    fb = r.get("feedback", {})
    amount = fb.get("withdrawn_amount", 0)
    rid = r.get("request_id", "")
    obj = fb.get("objective") or "你的长期目标"
    ahead_simple = fb.get("ahead_months_simple", 0)
    ahead_real = fb.get("ahead_months_real")
    note = fb.get("estimation_note", "")

    # 试着从上下文中找 category
    lines = [
        _header("✅", "撤回·已撤回", ts),
        SEP,
        f"申请 {rid}（¥{amount:,.2f}）已撤回",
        f"即时回馈：相当于 {obj} 目标提前约 {_fmt_months(ahead_simple)}",
        "· 估算非承诺：基于简化口径，误差 ±20%~50%",
        f"· {note}",
        "· 钱留在账上，冷静期自动解除",
        SEP,
    ]
    if ahead_real is not None:
        lines.insert(-1, f"· 真实口径约 {_fmt_months(ahead_real)}（含通胀/回撤）")
    return "\n".join(lines)


def _render_judge_finalize(r: dict, ts: str) -> str:
    rid = r.get("request_id", "")
    dec = r.get("decision", {})
    result_word = dec.get("result", "执行")
    summary = dec.get("summary", "")
    lines = [
        _header("✅", "终裁确认·已执行", ts),
        SEP,
        f"申请 {rid} 按「{result_word}」终裁执行",
        summary,
        SEP,
    ]
    return "\n".join(lines)


def _render_judge_expire(r: dict, ts: str) -> str:
    processed = r.get("processed", [])
    lines = [_header("⏰", "到期终裁·已处理", ts), SEP]
    if not processed:
        lines.append("✅ 无到期申请待终裁")
    else:
        for p in processed:
            amt = p.get("amount", 0)
            cat = p.get("category", "")
            final = p.get("final_status", "")
            d = p.get("decision", {})
            dr = d.get("result", "")
            lines.append(f"· {cat} {_fmt(amt)} → {zh_status(final)}（{dr}）")
    lines.append(SEP)
    return "\n".join(lines)


def _render_judge_reminders(r: dict, ts: str) -> str:
    reminders = r.get("reminders", [])
    lines = [_header("⏰", "冷静期提醒·查询", ts), SEP]
    if not reminders:
        lines.append("✅ 无冷静期挂起申请")
    else:
        for rm in reminders:
            kind = rm.get("kind", "cooling")
            cat = rm.get("category", "")
            amt = rm.get("amount", 0)
            days_left = rm.get("days_left", 0)
            expire_at = rm.get("expire_at", "")
            rid = rm.get("request_id", "")
            icon = "⚠️" if kind == "expiring" else "⏳"
            tag = "即将到期" if kind == "expiring" else "冷静中"
            lines.append(f"· {icon} {tag}：{cat} {_fmt(amt)}")
            lines.append(f"  剩余 {days_left} 天（到期 {expire_at}）编号 {rid}")
    lines.append(SEP)
    return "\n".join(lines)


# ── §3 初始化 ────────────────────────────────────────────────────

def _render_init(r: dict, ts: str) -> str:
    corpus = r.get("corpus", 0)
    monthly = r.get("monthly_contribution", 0)
    objs = r.get("objectives", [])
    warnings = r.get("warnings", [])
    currency = r.get("currency", "CNY")
    sym = CURRENCY_SYMBOLS.get(currency, currency)
    basis = r.get("monthly_basis", "gross_estimate")

    lines = [_header("✅", "记账初始化·已生成", ts), SEP]
    obj_strs = []
    for o in objs:
        name = o.get("name", "")
        ta = o.get("target_amount", 0)
        dl = o.get("deadline", "")
        if ta and dl:
            obj_strs.append(f"{name}（{sym}{ta:,.2f}，{dl}）")
        elif ta:
            obj_strs.append(f"{name}（{sym}{ta:,.2f}）")
        else:
            obj_strs.append(name)
    monthly_badge = "〔毛口径·待校准〕" if basis == "gross_estimate" else ""
    lines.append(f"资金池 {sym}{corpus:,.2f}{'' if currency == 'CNY' else ' ' + currency}"
                 f"·月度净流入 {sym}{monthly:,.2f}{monthly_badge}"
                 f"{'' if currency == 'CNY' else ' ' + currency}")
    lines.append(f"目标：{'；'.join(obj_strs)}")
    for w in warnings:
        lines.append(f"⚠️ {w}")
    lines.append(SEP_CTX)
    lines.append("· 已生成默认契约，可随时说『自定义』逐项调")
    return "\n".join(lines)


# ── §4 演示 ──────────────────────────────────────────────────────

def _render_demo(r: dict, ts: str) -> str:
    demo_defaults = r.get("demo_defaults_used", True)
    lines = [
        _header("✅", "演示·已生成", ts),
        SEP,
    ]
    # 警告行：区分合成默认 vs 真实契约参数
    if demo_defaults:
        lines.append("⚠️ 演示数据（场景为合成，基于默认参数），非真实审批")
    else:
        # 真实契约参数：展示资金池/月净流入（原样引用，不心算）
        ep = r.get("engine_params", {})
        corpus = ep.get("corpus")
        monthly = ep.get("monthly_net")
        param_hint = ""
        if corpus is not None and monthly is not None:
            param_hint = f"（基于你真实契约：资金池 {_fmt(corpus)} / 月净流入 {_fmt(monthly)}）"
        lines.append(f"⚠️ 演示数据（场景为合成{param_hint}），非真实审批")

    # 三场景列表（含金额 + 目标影响）
    scenes = r.get("scenarios", [])
    for s in scenes:
        label = s.get("name", "")
        scene = s.get("scene", "")
        days = s.get("cooldown_days", 0)
        amt = s.get("amount")
        amt_str = f" {_fmt(amt)}" if amt is not None else ""
        delay = s.get("delay_months_simple")
        impact_str = ""
        # §0.1：月数 < 0.1 视为无影响（省略行，不展示 0 / 0.0 噪声）
        if delay is not None and round(delay, 1) >= 0.1:
            impact_str = f"  · 目标延后约 {round(delay, 1):.1f} 个月（简化口径）"
        if scene == "A":
            lines.append(f"· {label}{amt_str} → 批准（无冷静期）{impact_str}")
        elif scene == "B":
            lines.append(f"· {label}{amt_str} → 批准（触发 {days} 天冷静期）{impact_str}")
        else:
            lines.append(f"· {label}{amt_str} → 驳回（冷却）{impact_str}")
            alt = r.get("alt_plan_scenario3")
            if alt:
                m = alt.get("months")
                pm = alt.get("per_month")
                if m is not None and pm is not None:
                    lines.append(f"  · 替代方案：{int(m)} 期 / 每期 {_fmt(pm)}（单笔不超冷静期阈值、不击穿安全垫）")

    # 上下文行（--- 分隔线后）
    lines.append("---" + "-" * 41)
    lines.append("这是演示，不影响真实账户（干跑不落账目、不入冷静期队列、不写审计）；")
    lines.append("现在可以说「审查：买X花Y」开始真实审批。")
    return "\n".join(lines)


# ── §5 报表 ──────────────────────────────────────────────────────

def _render_report(r: dict, ts: str) -> str:
    corpus = r.get("corpus", 0)
    net = r.get("net_assets", 0)
    margin = r.get("cushion_margin", 0)
    alert = r.get("cushion_alert", False)
    monthly_net = r.get("monthly_net", 0)
    objs = r.get("objectives", [])
    pc = r.get("pending_cooling", [])
    notes = r.get("notes", [])
    basis = r.get("monthly_basis", "gross_estimate")
    eff = r.get("monthly_net_effective") or {}

    lines = [_header("📊", "报表·已生成", ts), SEP]
    lines.append(f"· 资金池 {_fmt(corpus)}·净资产 {_fmt(net)}")
    lines.append(f"· 安全垫余量 {_fmt(margin)}")
    for o in objs:
        name = o.get("name", "")
        ar = o.get("achieved_ratio", 0)
        color = "✅" if ar >= 100 else ("🟡" if ar >= 50 else "🔴")
        tp = o.get("time_progress", 0)
        lines.append(f"· {name} 达成 {_fmt_pct(ar)}·{color}（时间轴应达 {_fmt_pct(tp)}）")
    monthly_badge = "〔毛口径·待校准〕" if basis == "gross_estimate" else ""
    lines.append(f"· 本月净流入 {_fmt(monthly_net)}{monthly_badge}（进度平稳）")
    if alert:
        lines.append("· 安全垫预警：⚠️ 告警")
    else:
        lines.append("· 安全垫预警：余量充足，无预警")
    if basis == "net" and eff:
        entered = float(eff.get("entered", 0) or 0)
        debt = float(eff.get("debt_monthly", 0) or 0)
        rigid = float(eff.get("rigid_monthly", 0) or 0)
        net_eff = float(eff.get("net", entered - debt - rigid) or 0)
        lines.append(
            f"· 月净流入（净）{_fmt(net_eff)}"
            f"（录入 {_fmt(entered)} − 负债月供 {_fmt(debt)} − 刚性月摊 {_fmt(rigid)}）"
        )
    if pc:
        lines.append(f"· 冷静期挂起（{len(pc)} 笔）：")
    for p in pc:
        cat = p.get("category", "")
        amt = p.get("amount", 0)
        exp = p.get("expire_at", "")
        rid = p.get("request_id", "")
        lines.append(f"  · {cat} {_fmt(amt)} 待决")
        lines.append(f"    到期 {exp}（编号 {rid}）")
    for n in notes:
        lines.append(f"· {n}")
    lines.append(SEP)
    return "\n".join(lines)


# ── §6 校准 ──────────────────────────────────────────────────────

def _render_calibrate(r: dict, ts: str) -> str:
    skipped = r.get("skipped", False)
    changes = r.get("changes", [])
    ro = r.get("rebalance_override")
    lines = [_header("📊", "月度校准·已生效" if not skipped else "月度校准·已跳过", ts), SEP]
    if skipped:
        lines.append("✅ 本月已校准过（同月幂等），--force 可强制重跑")
    else:
        if not changes:
            lines.append("✅ 无需调整，目标进度正常")
        else:
            lines.append("以下调整已生效：")
            for c in changes:
                desc = c.get("note")
                if not desc:
                    t = c.get("type")
                    if t == "reward_unlocked":
                        desc = (f"{c.get('objective')} 达成 "
                                f"{_fmt_pct(c.get('achieve_ratio', 0))} "
                                f"→ 解锁奖励额度 {_fmt(c.get('reward_quota', 0))}")
                    else:
                        desc = f"[{t}] {c.get('objective', '')}".strip()
                lines.append(f"· {desc}")
        if ro:
            lines.append("· 仅本月有效，原始权重不变")
    lines.append(SEP)
    return "\n".join(lines)


# ── §7 奖励 ──────────────────────────────────────────────────────

def _render_reward_status(r: dict, ts: str) -> str:
    objs = r.get("rewards", [])
    lines = [_header("🏆", "奖励状态·查询", ts), SEP]
    for o in objs:
        name = o.get("name", "")
        ar = o.get("achieve_ratio", 0)
        quota = o.get("reward_quota", 0)
        status = zh_status(o.get("reward_status"))
        lines.append(f"· {name}：达成率 {_fmt_pct(ar)} {status}")
        if quota > 0:
            lines.append(f"  可支取 {_fmt(quota)}")
        else:
            lines.append(f"  暂无可支取额度")
    lines.append(SEP)
    return "\n".join(lines)


def _render_reward_unlock(r: dict, ts: str) -> str:
    objs = r.get("unlocked", [])
    lines = [_header("🏆", "奖励解锁·已解锁", ts), SEP]
    new_unlocked = False
    for o in objs:
        name = o.get("name", "")
        ar = o.get("achieve_ratio", 0)
        quota = o.get("reward_quota", 0)
        if ar >= 1.2:
            new_unlocked = True
            lines.append(f"· {name} 达成 {_fmt_pct(ar)}（≥120%）→ 解锁奖励额度 {_fmt(quota)}")
    if not new_unlocked:
        lines.append("✅ 暂无新解锁的奖励（达成率 ≥120% 时自动解锁）")
    lines.append(SEP)
    return "\n".join(lines)


def _render_reward_claim(r: dict, ts: str) -> str:
    obj = r.get("objective", "")
    amount = r.get("amount", 0)
    purpose = r.get("purpose", "")
    remaining = r.get("quota_remaining", 0)
    lines = [
        _header("✅", "奖励支取·已执行", ts),
        SEP,
        f"{obj} {_fmt(amount)}（{purpose}）",
        f"· 剩余额度 {_fmt(remaining)}",
        SEP,
    ]
    return "\n".join(lines)


# ── §8 日志 ──────────────────────────────────────────────────────

def _render_log(r: dict, ts: str) -> str:
    log_name = r.get("log", "?")
    count = r.get("count", 0)
    records = r.get("records", [])
    lines = [_header("📋", f"审计日志·{log_name}", ts), SEP]
    lines.append(f"共 {count} 条，展示最近 {min(10, count)} 条：")
    for rec in records[:10]:
        rt = rec.get("time", "")
        scene = rec.get("scene", rec.get("event", "?"))
        amount = rec.get("amount", 0)
        cat = rec.get("category", "")
        lines.append(f"· [{rt}] {scene} {_fmt(amount)} {cat}")
    lines.append(SEP)
    return "\n".join(lines)


# ── §9 申诉 / 覆写 ──────────────────────────────────────────────

def _render_appeal(r: dict, ts: str) -> str:
    upheld = r.get("upheld", True)
    dec = r.get("decision", {})
    summary = dec.get("summary", "")
    ac = r.get("appeal_count", 0)
    ov = r.get("override_open", False)
    result_word = "维持" if upheld else "改判"
    lines = [
        _header("📋", f"申诉·{result_word}", ts),
        SEP,
        summary,
        f"· 申诉计数 {ac}/3{' → 已开放人工覆写入口' if ov else ''}",
        SEP,
    ]
    return "\n".join(lines)


def _render_override_preview(r: dict, ts: str) -> str:
    ti = r.get("target_impact", {})
    ds = ti.get("delay_months_simple", 0)
    lines = [
        _header("⚠️", "人工覆写·预览", ts),
        SEP,
        f"· 目标影响：延后约 {_fmt_months(ds)}（简化口径，误差 ±20%~50%）",
        "· 确认知悉后回复「确认覆写」执行",
        SEP,
    ]
    return "\n".join(lines)


def _render_override_confirm(r: dict, ts: str) -> str:
    rid = r.get("request_id", "")
    ti = r.get("target_impact", {})
    ds = ti.get("delay_months_simple", 0)
    lines = [
        _header("✅", "人工覆写·已执行", ts),
        SEP,
        f"申请 {rid} 放行",
        f"· 目标延后影响已记录（约 {_fmt_months(ds)} 个月）",
        "· 已记入审计日志",
        SEP,
    ]
    return "\n".join(lines)


# ── §10 自定义 / 对账 / 重置 / 导入 ─────────────────────────────

def _render_customize_preview(r: dict, ts: str) -> str:
    # 引擎三种输出形态：
    #  (a) review_config → {swept, pending:[...], message}
    #  (b) apply 预览/已应用 → {changed_fields, risk_warnings, cooldown_required,
    #                            token, home_purchase, applied?}
    #  (d) apply 削弱自身 → {pending:True, cooldown_days, request_id,
    #                         withdraw_token, expires_at, risk_warnings}
    lines = [_header("📋", "修改预览·待确认", ts), SEP]

    if "swept" in r:  # (a) 冷却窗复查
        swept = r.get("swept") or []
        items = r.get("pending") or []
        if swept:
            lines.append(f"· 冷却窗到期自动生效 {len(swept)} 项")
        if items:
            lines.append(f"· 冷却窗内待决 {len(items)} 项：")
            for it in items:
                lines.append(f"  · 编号 {it.get('request_id', '')} "
                             f"剩余 {it.get('days_left', 0)} 天"
                             f"（到期 {it.get('expires_at', '')}）")
                for w in it.get("risk_warnings", []):
                    lines.append(f"    · {w}")
        else:
            lines.append("· 冷却窗内无待决修改")
        lines.append(SEP)
        return "\n".join(lines)

    if r.get("pending") is True:  # (d) 削弱自身 → 冷却窗
        cd = r.get("cooldown_days", 1)
        rid = r.get("request_id", "")
        wt = r.get("withdraw_token", "")
        exp = r.get("expires_at", "")
        lines.append(f"⚠️ 削弱自身修改已进入 {cd} 天冷静窗（编号 {rid}）")
        lines.append(f"· 到期 {exp} 前可无理由撤回（撤回令牌 {wt}）")
        for w in r.get("risk_warnings", []):
            lines.append(f"· {w}")
        lines.append(SEP)
        return "\n".join(lines)

    # (b)/(c) 预览 / 已应用
    token = r.get("token", "")
    cw = r.get("cooldown_required", False)
    cd = r.get("cooldown_days", 1)
    cf = r.get("changed_fields", {}) or {}
    for field, ch in cf.items():
        fr = ch.get("from")
        to = ch.get("to")
        lines.append(f"· {field}: {fr} → {to}")
    for w in r.get("risk_warnings", []) or []:
        lines.append(f"· {w}")
    cons = r.get("monthly_consequence")
    if cons:
        lines.append(f"· 净口径化后果：{cons.get('note', '')}")
    if token:
        lines.append(f"· 确认令牌 {token}（回复「确认修改」+ 令牌生效）")
    if cw:
        lines.append(f"· ⚠️ 削弱型修改，确认后进入 {cd} 天冷静窗，窗内可无理由撤回")
    if r.get("applied"):
        lines.append("· 已落盘生效")
    lines.append(SEP)
    return "\n".join(lines)


def _render_customize_confirm(r: dict, ts: str) -> str:
    cs = r.get("changes_summary", "")
    cw = r.get("cooldown_window", False)
    cd = r.get("cooldown_days", 1)
    rid = r.get("request_id", "")
    lines = [
        _header("✅", "修改生效·已生效", ts),
        SEP,
        cs,
    ]
    cons = r.get("monthly_consequence")
    if cons:
        lines.append(f"· 净口径化后果：{cons.get('note', '')}")
    if cw:
        lines.append(f"· 进入 {cd} 天冷静窗（编号 {rid}），窗内可「记账自定义·撤回」")
    lines.append(SEP)
    return "\n".join(lines)


def _render_reconcile(r: dict, ts: str) -> str:
    changes = r.get("changes", {})
    psc = r.get("pending_spends_cleared", {})
    last = r.get("last_reconcile", "")
    lines = [_header("📊", "对账·已完成", ts), SEP]
    cc = changes.get("corpus")
    if cc:
        diff = float(cc.get("to", 0) or 0) - float(cc.get("from", 0) or 0)
        lines.append(f"· 资金池 {_fmt(cc['from'])} → {_fmt(cc['to'])}（差额 {_fmt(diff)}）")
    if psc:
        lines.append(f"· 清销已批支出 {psc.get('count', 0)} 笔"
                     f"（合计 {_fmt(psc.get('total_actual_cash_out', 0))}）")
    lines.append(f"· 本次对账：{last}" if last else "· 本次对账已完成")
    lines.append(SEP)
    return "\n".join(lines)


def _render_reset_preview(r: dict, ts: str) -> str:
    sha = r.get("old_contract_sha256", "")
    lines = [
        _header("⚠️", "重置警告·待确认", ts),
        SEP,
        "· 将重建整个契约（审计日志保留）",
        f"· 旧契约 sha256: {sha}",
        "· 确认后须提供新契约参数（资金池/月度流入/目标）",
        SEP,
    ]
    return "\n".join(lines)


def _render_reset_confirm(r: dict, ts: str) -> str:
    sha = r.get("old_contract_sha256", "")
    corpus = r.get("corpus", 0)
    monthly = r.get("monthly_contribution", 0)
    objs = r.get("objectives", [])
    warnings = r.get("warnings", [])
    currency = r.get("currency", "CNY")
    sym = CURRENCY_SYMBOLS.get(currency, currency)
    lines = [
        _header("✅", "重置·已生效", ts),
        SEP,
        f"· 旧契约 sha256: {sha}（已归档）",
        "· 新契约回执：",
        f"  资金池 {sym}{corpus:,.2f}·月度净流入 {sym}{monthly:,.2f}",
    ]
    for o in objs:
        name = o.get("name", "")
        ta = o.get("target_amount")
        dl = o.get("deadline", "")
        if ta and dl:
            lines.append(f"  · {name}（{sym}{ta:,.2f}，{dl}）")
        elif ta:
            lines.append(f"  · {name}（{sym}{ta:,.2f}）")
        else:
            lines.append(f"  · {name}")
    for w in warnings:
        lines.append(f"  · {w}")
    lines.append(SEP)
    return "\n".join(lines)


def _render_import_pending(r: dict, ts: str) -> str:
    summary = r.get("summary", {})
    susp = r.get("suspicious", [])
    token = r.get("token", "")
    total = summary.get("total_assets", 0)
    lc = summary.get("liabilities_count", 0)
    rc = summary.get("rigid_count", 0)
    lines = [
        _header("📋", "资产导入·待核对", ts),
        SEP,
        f"· 总资产 {_fmt(total)}",
        f"· 负债 {lc} 项 / 刚性支出 {rc} 项",
    ]
    if susp:
        lines.append(f"· ⚠️ 可疑流水 {len(susp)} 条，请核对")
    else:
        lines.append("· 无可疑流水")
    lines.append(f"· 导入状态：{zh_status(r.get('import_status'))}（核对前锁定全部审批）")
    lines.append(f"· 确认令牌 {token}")
    lines.append("· 核对后回复「确认导入」+ 令牌生效；或「取消导入」放弃")
    lines.append(SEP)
    return "\n".join(lines)


def _render_import_confirm(r: dict, ts: str) -> str:
    applied = r.get("applied", {})
    lines = [
        _header("✅", "资产导入·已生效", ts),
        SEP,
    ]
    if applied:
        corpus = applied.get("corpus")
        monthly = applied.get("monthly_contribution")
        liabs = applied.get("liabilities") or []
        rigid = applied.get("rigid_annual_expenses") or []
        parts = []
        if corpus is not None:
            parts.append(f"资金池 {_fmt(corpus)}")
        if monthly is not None:
            parts.append(f"月净流入 {_fmt(monthly)}")
        if parts:
            lines.append("· " + "·".join(parts))
        if liabs:
            lines.append(f"· 负债 {len(liabs)} 项已纳入")
        if rigid:
            lines.append(f"· 刚性年支出 {len(rigid)} 项已纳入")
    lines.append(f"· 导入状态：{zh_status(r.get('import_status'))}，审批已解锁")
    lines.append(SEP)
    return "\n".join(lines)


def _render_import_cancel(r: dict, ts: str) -> str:
    status = zh_status(r.get("import_status", "manual"))
    return (
        f"✅资产导入·已取消{_now_ts()}\n"
        f"{SEP}\n"
        f"资产状态已还原为「{status}」（实际资产未改动）\n"
        f"{SEP}\n"
    )


def _render_objective(r: dict, ts: str) -> str:
    name = r.get("name", "")
    ar = r.get("achieved_ratio", 0)
    to = r.get("to", "archived")
    lines = [
        _header("✅", f"目标·已{'归档' if to == 'archived' else '完结'}", ts),
        SEP,
        f"· {name} 已达成 {_fmt_pct(ar)}，归档至历史目标",
        "· 后续资金可重新分配",
        SEP,
    ]
    return "\n".join(lines)


# ── 错误渲染 ────────────────────────────────────────────────────

def _render_error(r: dict, ts: str) -> str:
    err = r.get("error", "unknown")
    msg = r.get("message", "")

    guide_map: dict[str, str] = {
        "not_found": "未找到契约数据，请先初始化（记账初始化）",
        "guard": msg,
        "invalid": f"参数有误：{msg}",
        "import_pending": "资产待核对，禁止审批；请先完成人工核对确认",
        "exists": "契约已存在，不可重复初始化；如需重建请走『记账重置』",
        "invalid_transition": msg,
        "request_not_found": "未找到该申请，可能已终裁或撤回",
        "not_due": f"该申请尚未到期，请到期后再终裁（{msg}）",
        "already_expired": "该申请已过期，请走到期终裁",
        "missing_rate": msg,
        "override_not_open": "尚未达到人工覆写条件（须连续 3 次申诉被驳）",
        "cushion_violation": "奖励支取击穿安全垫，规则引擎拒付",
        "invalid_amount": "申请金额必须为正数",
    }
    hint = guide_map.get(err, msg)
    lines = [
        _header("⚠️", "错误", ts),
        SEP,
        hint,
        SEP,
    ]
    return "\n".join(lines)


# ── 主入口 ──────────────────────────────────────────────────────

CURRENCY_SYMBOLS: dict[str, str] = {
    "CNY": "¥", "USD": "$", "EUR": "€", "GBP": "£",
    "HKD": "HK$", "JPY": "¥", "SGD": "S$", "AUD": "A$", "CAD": "C$",
}


def _fmt_pct(v: float) -> str:
    """百分比，保留 1 位小数"""
    return f"{v:.1f}%"


def _fmt_months(v: float) -> str:
    """月数，保留 1 位小数，0.1 兜底"""
    v = float(v)
    if abs(v) < 0.1:
        return "0.1 个月"
    return f"{v:.1f} 个月"


def _apply_skeleton(text: str) -> str:
    """§0.5 骨架强制（唯一权威入口）：确保顶部 =×44，剔除卡片末行的任何分隔线。

    各渲染函数只负责「标题下分隔线 + 正文（+ 可选上下文）」，统一在此：
      1. 补全顶部 =×44（历史所有函数都漏了顶部分隔线）；
      2. 清除尾部分隔线（= 或 -，长度≥40）——§0.5 规定「卡片最末行之后严禁任何分隔线」。
    正文↔上下文之间的 ---×44 分隔线由各函数自行输出（init/demo 已合规）。
    """
    out = text.split("\n")
    # 末行若是分隔线（纯 = 或纯 -，长度≥40）则剔除
    if out and len(out[-1]) >= 40 and set(out[-1]) <= {"=", "-"}:
        out.pop()
    # 顶部确保有 = ×44
    if not (out and len(out[0]) >= 40 and set(out[0]) <= {"=", "-"}):
        out.insert(0, SEP)
    return "\n".join(out)


def render(result: dict, command: str, subcommand: str | None = None) -> str:
    """渲染引擎主入口。

    Args:
        result: CLI 模块输出的结构化 JSON（含 ok/error 等元字段）。
        command: 命令名（judge / init / report / demo / calibrate / reward /
                  log / appeal / customize / reconcile / reset / import-asset /
                  objective）。
        subcommand: 子命令识别（如 reward 的 status/unlock/claim，
                    customize 的 preview/confirm，appeal 的 override 等）。

    Returns:
        格式化文本，含 §0.5 全局骨架（分隔线 + 时间戳）。
        失败时返回 JSON 的 message。
    """
    ts = _ts_from(result)

    if not result.get("ok", True):
        return _apply_skeleton(_render_error(result, ts))

    text = _render_error(result, ts)  # 兜底（下方分支必覆盖）
    # judge 按 action 分派
    if command == "judge":
        action = subcommand or "submit"
        if action == "submit":
            text = _render_judge_submit(result, ts)
        elif action == "withdraw":
            text = _render_judge_withdraw(result, ts)
        elif action == "finalize":
            text = _render_judge_finalize(result, ts)
        elif action == "expire":
            text = _render_judge_expire(result, ts)
        elif action == "reminders":
            text = _render_judge_reminders(result, ts)
        else:
            text = _render_error({"ok": False, "error": "invalid",
                                  "message": f"未知 judge action: {action}"}, ts)
    elif command == "init":
        text = _render_init(result, ts)
    elif command == "demo":
        text = _render_demo(result, ts)
    elif command == "report":
        text = _render_report(result, ts)
    elif command == "calibrate":
        text = _render_calibrate(result, ts)
    elif command == "reconcile":
        text = _render_reconcile(result, ts)
    elif command == "reward":
        act = subcommand or "status"
        if act == "status":
            text = _render_reward_status(result, ts)
        elif act == "unlock":
            text = _render_reward_unlock(result, ts)
        elif act == "claim":
            text = _render_reward_claim(result, ts)
        else:
            text = _render_error(result, ts)
    elif command == "log":
        text = _render_log(result, ts)
    elif command == "appeal":
        ov = subcommand == "override"
        confirm = subcommand == "override_confirm"
        if confirm:
            text = _render_override_confirm(result, ts)
        elif ov:
            text = _render_override_preview(result, ts)
        else:
            text = _render_appeal(result, ts)
    elif command == "customize":
        if subcommand == "confirm":
            text = _render_customize_confirm(result, ts)
        else:
            text = _render_customize_preview(result, ts)
    elif command == "reset":
        if subcommand == "confirm":
            text = _render_reset_confirm(result, ts)
        else:
            text = _render_reset_preview(result, ts)
    elif command == "import-asset":
        status = subcommand or "pending"
        if status == "pending":
            text = _render_import_pending(result, ts)
        elif status == "confirm":
            text = _render_import_confirm(result, ts)
        elif status == "cancel":
            text = _render_import_cancel(result, ts)
        else:
            text = _render_error(result, ts)
    elif command == "objective":
        text = _render_objective(result, ts)
    else:
        text = _render_error({"ok": False, "error": "invalid",
                              "message": f"未知命令: {command}"}, ts)

    return _apply_skeleton(text)


if __name__ == "__main__":  # pragma: no cover — 快速预览用
    import sys
    import json
    raw = sys.stdin.read()
    data = json.loads(raw)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "?"
    sub = sys.argv[2] if len(sys.argv) > 2 else None
    print(render(data, cmd, sub))
