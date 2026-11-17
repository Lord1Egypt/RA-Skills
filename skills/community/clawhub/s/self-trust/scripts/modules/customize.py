# -*- coding: utf-8 -*-
"""记账自定义（§5.4 / §7.1 / §9）：逐项增量覆盖修改契约配置区参数。

确定性规则（公正性靠代码不靠 AI）：
- 增量覆盖：只改用户指定的字段，不破坏未填值（deep-merge）；
- §5.4 核心护栏字段（safety_cushion / objectives / fast_track_whitelist /
  optimization_goal / distribution_rules）修改 → 二次确认 + 风险提示 + 落 override_log；
- 非核心字段（monthly_contribution / mode / corpus 等）走普通确认（同一「预览→确认」两步）；
- 单次预览不落盘（needs_confirm）；确认须带预览返回的 token（防漂移 / 手滑）；
- 落盘经 core.contract.write_contract(actor="configurator", confirm=True)，
  三区权限 + §5.4 闸门由底层强制，未知字段 / 审计字段显式 GuardError；
- 变更落 override_log（§5.4 步骤4），与 §10.1 审计一致、仅追加可复盘。

LLM 铁律：禁止心算，风险提示中的数字必须原样引用本模块从契约算出的结果。
"""
from __future__ import annotations

import copy
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import secrets

from core import audit as audit_io
from core import contract as contract_io
from core.contract import _validate_zones
from core.models import (
    CORE_GUARD_FIELDS, living_baseline_value, ObjectiveStatus, ConfigChangeStatus,
)
from core.i18n import CONFIG_CHANGE_STATUS_ZH
from core.util import make_token as _token, contract_sha as _contract_sha
from modules.judge import estimate_mortgage_monthly as _est_mortgage


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _parse_scalar(s: str) -> Any:
    """--set 的值类型解析：null/bool/float/str（按此顺序）。"""
    low = s.strip().lower()
    if low in ("null", "none", ""):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def _set_dotpath(d: dict[str, Any], path: str, value: Any) -> None:
    """在嵌套 dict 上按 dotpath 设置值（就地修改 d）。"""
    parts = path.split(".")
    cur = d
    for p in parts[:-1]:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    cur[parts[-1]] = value


def _parse_objective(spec: str) -> dict[str, Any]:
    """解析 --add-objective "名称:目标额:期限"，补齐 Objective schema 默认。"""
    parts = spec.split(":")
    obj: dict[str, Any] = {
        "name": parts[0], "weight": 1.0, "current_amount": 0.0,
        "start_date": None, "deadline": None, "target_amount": None,
        "lag_streak": 0, "reward_unlocked": False, "reward_quota": 0.0,
        "status": ObjectiveStatus.ACTIVE.value,
    }
    if len(parts) > 1 and parts[1]:
        ta = float(parts[1])
        if ta <= 0:
            raise ValueError(f"目标额须为正数，得到 {parts[1]!r}（目标 {parts[0]}）")
        obj["target_amount"] = ta
    if len(parts) > 2 and parts[2]:
        obj["deadline"] = parts[2]
    return obj


def _top_field(path: str) -> str:
    """dotpath 的顶层字段名（用于 §5.4 护栏归属判定）。"""
    return path.split(".", 1)[0]


def _parse_liability(spec: str) -> dict[str, Any]:
    """解析 --add-liability "名称:余额[:月供[:年利率]]"。"""
    parts = spec.split(":")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("--add-liability 格式应为 名称:余额[:月供[:年利率]]")
    return {
        "name": parts[0],
        "balance": float(parts[1]),
        "monthly_payment": float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
        "annual_rate": float(parts[3]) if len(parts) > 3 and parts[3] else 0.0,
    }


def _parse_rigid(spec: str) -> dict[str, Any]:
    """解析 --add-rigid "名称:金额[:due_month]"。"""
    parts = spec.split(":")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("--add-rigid 格式应为 名称:金额[:due_month]")
    return {
        "name": parts[0],
        "amount": float(parts[1]),
        "due_month": int(parts[2]) if len(parts) > 2 and parts[2] else None,
    }


def _parse_home_purchase(spec: str) -> dict[str, Any]:
    """解析 --record-home-purchase "房价:首付比例[:期限年[:利率]]"。

    首付比例 0~1（如 0.3 = 首付 30%）。返回含计算结果的规范：
    down_payment / financed / mortgage_monthly。
    """
    parts = spec.split(":")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("--record-home-purchase 格式应为 房价:首付比例[:期限年[:利率]]")
    price = float(parts[0])
    down_ratio = float(parts[1])
    if not (0.0 <= down_ratio <= 1.0):
        raise ValueError("首付比例须介于 0~1（如 0.3 表示首付 30%）")
    term = float(parts[2]) if len(parts) > 2 and parts[2] else 30.0
    rate = float(parts[3]) if len(parts) > 3 and parts[3] else 0.04
    down_payment = price * down_ratio              # 首付（打 liquid）
    financed = price * (1.0 - down_ratio)          # 贷款（变负债 + 月供）
    mortgage_monthly = _est_mortgage(financed, term, rate)
    return {
        "price": price, "down_ratio": down_ratio, "term_years": term,
        "rate": rate, "down_payment": down_payment, "financed": financed,
        "mortgage_monthly": mortgage_monthly,
    }


def _risk_warnings(contract: dict[str, Any], changed: dict[str, Any]) -> list[str]:
    """§5.4 步骤1 + 485：核心护栏字段修改须用具体数字与后果提示（不空泛）。"""
    warns: list[str] = []
    lb = living_baseline_value(contract)
    m = float(contract.get("monthly_contribution", 0) or 0)

    if "safety_cushion" in changed:
        old, new = (changed["safety_cushion"]["from"],
                    changed["safety_cushion"]["to"])
        om, nm = old.get("months"), new.get("months")
        if om is not None and nm is not None and nm < om:
            warns.append(
                f"安全垫月数由 {om} 降至 {nm}；按当前生活费基线 {lb}，"
                f"现金缓冲由 {om * lb} 降至 {nm * lb}（抗风险能力↓）")
        if old.get("mode") != new.get("mode"):
            warns.append(
                f"安全垫模式由 {old.get('mode')} 改为 {new.get('mode')}（缓冲口径变化）")

    if "distribution_rules" in changed:
        od = changed["distribution_rules"]["from"].get("invest_ratio")
        nd = changed["distribution_rules"]["to"].get("invest_ratio")
        if od is not None and nd is not None:
            if nd == 0:
                warns.append("投资比例归零，FIRE 将实质性停滞（每月增值投入归零）")
            elif nd < od:
                warns.append(
                    f"投资比例由 {od} 降至 {nd}；按月净流入 {m}，"
                    f"每月增值投入由 {od * m} 降至 {nd * m}（目标推进减速）")
            elif nd > od:
                warns.append(
                    f"投资比例由 {od} 升至 {nd}；按月净流入 {m}，"
                    f"每月增值投入由 {od * m} 升至 {nd * m}（短期可支配收入减少）")

    if "optimization_goal" in changed:
        new = changed["optimization_goal"]["to"]
        if new == "wealth":
            warns.append("切换至激进增值模式：生活费基线压缩、短期可支配收入减少、目标推进加速")
        elif new == "objective":
            warns.append("切换至目标优先模式：非目标支出更受限")
        elif new == "balanced":
            warns.append("切回均衡模式：恢复默认调度")

    if "objectives" in changed:
        olds = {o.get("name") for o in changed["objectives"]["from"]}
        news = changed["objectives"]["to"]
        new_names = {n.get("name") for n in news}
        for o in news:
            if o.get("name") not in olds:
                warns.append(
                    f"新增目标 {o.get('name')}（目标额 {o.get('target_amount')}，"
                    f"期限 {o.get('deadline')}）")
        for o in changed["objectives"]["from"]:
            if o.get("name") not in new_names:
                warns.append(f"移除目标 {o.get('name')}（已删目标不再追踪）")

    if "fast_track_whitelist" in changed:
        olds = {w.get("name") for w in changed["fast_track_whitelist"]["from"]}
        news = changed["fast_track_whitelist"]["to"]
        new_names = {w.get("name") for w in news}
        for n in news:
            if n.get("name") not in olds:
                warns.append(
                    f"新增极速审批类目 {n.get('name')}（单笔上限 {n.get('per_tx_cap')}，"
                    f"年上限 {n.get('annual_cap')}）：免冷静期不豁免安全垫")
        for name in olds - new_names:
            warns.append(f"移除极速审批类目 {name}（该类目恢复走正常冷静期）")
    return warns


def _eff_cushion(sc: dict[str, Any], lb: float, net: float) -> float:
    """按安全垫配置算有效安全垫（与 F.f1_effective_cushion 同口径，避免新增依赖）。"""
    mode = (sc.get("mode", "months") or "").strip().lower()  # L5 大小写不敏感
    if mode == "months":
        return float(lb) * float(sc.get("months", 6))
    if mode == "fixed":
        return float(sc.get("fixed", 0))
    if mode == "ratio":
        return max(float(net), 0.0) * float(sc.get("ratio", 0.2))
    return 0.0


def _is_weakening(changed: dict[str, Any],
                  contract: dict[str, Any] | None = None) -> bool:
    """§5.4 冷却窗：仅「削弱自身」的护栏修改需 1 个自然日冷静窗。

    - safety_cushion.months 下调；
    - safety_cushion.ratio / fixed 下调，或模式切换导致有效安全垫下降（H4 修复）；
    - distribution_rules.invest_ratio 下调。
    其余护栏修改（上调安全垫 / 切 optimization_goal / 增删白名单 / 增删目标）
    不属「削弱自身」，立即生效、不进冷却窗。
    """
    if "safety_cushion" in changed:
        frm = changed["safety_cushion"]["from"]
        to = changed["safety_cushion"]["to"]
        # 简单口径（向后兼容）：月数下调
        om, nm = frm.get("months"), to.get("months")
        if om is not None and nm is not None and nm < om:
            return True
        # 通用口径（H4）：有效安全垫下降即削弱——覆盖 ratio/fixed 下调与模式切换
        if contract is not None:
            lb = living_baseline_value(contract)
            net = float(contract.get("corpus", 0)) - sum(
                float(x.get("balance", 0)) for x in contract.get("liabilities", []))
            if _eff_cushion(to, lb, net) < _eff_cushion(frm, lb, net):
                return True
    if "distribution_rules" in changed:
        od = changed["distribution_rules"]["from"].get("invest_ratio")
        nd = changed["distribution_rules"]["to"].get("invest_ratio")
        if od is not None and nd is not None and nd < od:
            return True
    return False


def _apply_changes(contract: dict[str, Any], changes: dict[str, Any]):
    """将 changes 规范应用到契约深拷贝，返回 (new_contract, touched_top_fields)。"""
    new = copy.deepcopy(contract)
    touched: set[str] = set()

    for op in changes.get("set", []):
        _set_dotpath(new, op["path"], op["value"])
        touched.add(_top_field(op["path"]))

    for spec in changes.get("add_objective", []):
        obj = _parse_objective(spec)
        # H6 修复：拒绝同名重复追加，避免 _objective_impacts 重复计算 / 下游只取首条
        if any(o.get("name") == obj.get("name") for o in new.get("objectives", [])):
            raise ValueError(f"目标已存在: {obj.get('name')}（请用 set 修改）")
        new.setdefault("objectives", []).append(obj)
        touched.add("objectives")

    for w in changes.get("whitelist_add", []):
        # H6 修复：拒绝同名白名单重复追加
        if any(x.get("name") == w["name"]
               for x in new.get("fast_track_whitelist", [])):
            raise ValueError(f"极速审批类目已存在: {w['name']}（请用 set 修改）")
        new.setdefault("fast_track_whitelist", []).append({
            "name": w["name"], "per_tx_cap": w["per_tx_cap"],
            "annual_cap": w["annual_cap"], "used_annual": 0})
        touched.add("fast_track_whitelist")

    for name in changes.get("whitelist_remove", []):
        wl = new.get("fast_track_whitelist", [])
        if not any(w.get("name") == name for w in wl):
            raise ValueError(f"白名单中不存在类目: {name}")
        new["fast_track_whitelist"] = [w for w in wl if w.get("name") != name]
        touched.add("fast_track_whitelist")

    for lb in changes.get("add_liability", []):
        # H6 修复：拒绝同名负债重复追加
        if any(x.get("name") == lb.get("name") for x in new.get("liabilities", [])):
            raise ValueError(f"负债已存在: {lb.get('name')}（请用 set 修改）")
        new.setdefault("liabilities", []).append(lb)
        touched.add("liabilities")

    for name in changes.get("remove_liability", []):
        lst = new.get("liabilities", [])
        if not any(x.get("name") == name for x in lst):
            raise ValueError(f"负债清单中不存在: {name}")
        new["liabilities"] = [x for x in lst if x.get("name") != name]
        touched.add("liabilities")

    for rg in changes.get("add_rigid", []):
        # H6 修复：拒绝同名刚性支出重复追加
        if any(x.get("name") == rg.get("name")
               for x in new.get("rigid_annual_expenses", [])):
            raise ValueError(f"刚性年支出已存在: {rg.get('name')}（请用 set 修改）")
        new.setdefault("rigid_annual_expenses", []).append(rg)
        touched.add("rigid_annual_expenses")

    for name in changes.get("remove_rigid", []):
        lst = new.get("rigid_annual_expenses", [])
        if not any(x.get("name") == name for x in lst):
            raise ValueError(f"刚性年支出清单中不存在: {name}")
        new["rigid_annual_expenses"] = [x for x in lst if x.get("name") != name]
        touched.add("rigid_annual_expenses")

    # —— 支出类目词汇表（allowed_categories，嵌套于 distribution_rules）——
    # 属配置区但非「削弱自身」，走 §5.4 二次确认、立即生效、不进冷却窗。
    for name in changes.get("add_category", []):
        cats = new.setdefault("distribution_rules", {}).setdefault("allowed_categories", [])
        if name not in cats:
            cats.append(name)
        touched.add("distribution_rules")

    for name in changes.get("remove_category", []):
        dr = new.get("distribution_rules", {})
        cats = dr.get("allowed_categories", [])
        if name not in cats:
            raise ValueError(f"支出类目词汇表中不存在: {name}")
        dr["allowed_categories"] = [c for c in cats if c != name]
        touched.add("distribution_rules")

    hp = changes.get("record_home_purchase")
    if hp:
        # M4：首付不得超当前资金池，否则 corpus 变负污染后续所有判定（F0 净资产/
        # F1 安全垫收敛），须在落账前显式拒绝而非静默转负。
        if float(new.get("corpus", 0)) < hp["down_payment"]:
            raise ValueError(
                f"记录购房失败：当前资金池 {new.get('corpus')} 不足以支付首付 "
                f"{hp['down_payment']:.2f}（首付须 ≤ 资金池；缺口请降低首付比例或先攒池）")
        # 首付（打 liquid）→ corpus 减；融资部分 → 变负债（含月供）
        new["corpus"] = float(new.get("corpus", 0)) - hp["down_payment"]
        liabs = new.setdefault("liabilities", [])
        # 修复 H2：已存在「房贷」（手动录入或上次记录）则更新而非追加，避免负债/月供翻倍
        existing = next((x for x in liabs if x.get("name") == "房贷"), None)
        if existing:
            existing["balance"] = hp["financed"]
            existing["monthly_payment"] = hp["mortgage_monthly"]
            existing["annual_rate"] = hp["rate"]
        else:
            liabs.append({
                "name": "房贷", "balance": hp["financed"],
                "monthly_payment": hp["mortgage_monthly"], "annual_rate": hp["rate"],
            })
        touched.add("corpus")
        touched.add("liabilities")

    # 层 A：录入负债/刚性后净口径化 → 标记位解除（两者皆空回 True）。
    # 统一在此重算，覆盖 add/remove（含 record_home_purchase 追加房贷、H6 同名更新）。
    new["monthly_is_gross_estimate"] = not (
        new.get("liabilities") or new.get("rigid_annual_expenses"))

    return new, touched


def _diff(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """顶层字段 before/after 差异（深层比较）。"""
    changed: dict[str, Any] = {}
    for k in set(old) | set(new):
        if old.get(k) != new.get(k):
            changed[k] = {"from": old.get(k), "to": new.get(k)}
    return changed


def _monthly_summary(contract: dict[str, Any]) -> dict[str, float]:
    """净口径化前后对比快照（展示用）：净口径 / 生活费基线 / 有效安全垫。"""
    from core.models import monthly_net_effective, living_baseline_value
    eff = monthly_net_effective(contract)
    lb = living_baseline_value(contract)
    net = float(contract.get("corpus", 0)) - sum(
        float(x.get("balance", 0)) for x in contract.get("liabilities", []))
    cushion = _eff_cushion(contract.get("safety_cushion", {}), lb, net)
    return {
        "monthly_net_effective": eff["net"],
        "living_baseline": lb,
        "effective_cushion": cushion,
    }


def _monthly_consequence(contract: dict[str, Any], new: dict[str, Any],
                         changes: dict[str, Any]) -> dict[str, Any] | None:
    """层 C：补负债/刚性 → 预览额外返回净口径化前后后果行（不落盘预告）。

    仅当变更涉及 add/remove 负债/刚性 或 record_home_purchase 时返回；
    其余变更（set/白名单/目标/类目）与净口径无关，返回 None。
    """
    touches = bool(
        changes.get("add_liability") or changes.get("remove_liability")
        or changes.get("add_rigid") or changes.get("remove_rigid")
        or changes.get("record_home_purchase"))
    if not touches:
        return None
    before = _monthly_summary(contract)
    after = _monthly_summary(new)
    note = (f"净口径 ¥{before['monthly_net_effective']:,.0f} → "
            f"¥{after['monthly_net_effective']:,.0f}；"
            f"安全垫 ¥{before['effective_cushion']:,.0f} → "
            f"¥{after['effective_cushion']:,.0f}；"
            f"生活费基线 ¥{before['living_baseline']:,.0f} → "
            f"¥{after['living_baseline']:,.0f}")
    return {"before": before, "after": after, "note": note}


def build_changes(args) -> dict[str, Any]:
    """从 CLI args 解析出 changes 规范（结构化变更列表）。"""
    changes: dict[str, Any] = {
        "set": [], "add_objective": [],
        "whitelist_add": [], "whitelist_remove": [],
        "add_liability": [], "remove_liability": [],
        "add_rigid": [], "remove_rigid": [],
        "add_category": [], "remove_category": [],
        "record_home_purchase": None,
    }
    for item in (args.set or []):
        if "=" not in item:
            raise ValueError(f"--set 格式应为 DOTPATH=VALUE，得到: {item}")
        path, _, raw = item.partition("=")
        changes["set"].append({"path": path.strip(), "value": _parse_scalar(raw)})
    for spec in (args.add_objective or []):
        changes["add_objective"].append(spec)
    if getattr(args, "whitelist_add", None):
        ptc = args.per_tx_cap
        anc = args.annual_cap
        if ptc is None or anc is None:
            raise ValueError("--whitelist-add 须同时提供 --per-tx-cap 与 --annual-cap")
        changes["whitelist_add"].append(
            {"name": args.whitelist_add, "per_tx_cap": float(ptc),
             "annual_cap": float(anc)})
    if getattr(args, "whitelist_remove", None):
        changes["whitelist_remove"].append(args.whitelist_remove)
    for spec in (getattr(args, "add_liability", None) or []):
        changes["add_liability"].append(_parse_liability(spec))
    for name in (getattr(args, "remove_liability", None) or []):
        changes["remove_liability"].append(name)
    for spec in (getattr(args, "add_rigid", None) or []):
        changes["add_rigid"].append(_parse_rigid(spec))
    for name in (getattr(args, "remove_rigid", None) or []):
        changes["remove_rigid"].append(name)
    for name in (getattr(args, "add_category", None) or []):
        changes["add_category"].append(name)
    for name in (getattr(args, "remove_category", None) or []):
        changes["remove_category"].append(name)
    for spec in (getattr(args, "record_home_purchase", None) or []):
        if changes["record_home_purchase"] is not None:
            raise ValueError("--record-home-purchase 每次只能记录一笔")
        changes["record_home_purchase"] = _parse_home_purchase(spec)
    if not any(changes.values()):
        raise ValueError(
            "未提供任何修改（--set / --add-objective / --whitelist-add / "
            "--whitelist-remove / --add-liability / --remove-liability / "
            "--add-rigid / --remove-rigid / --add-category / --remove-category / "
            "--record-home-purchase 至少一项）")
    return changes


_VALID_CUSHION_MODES = ("months", "fixed", "ratio")


def _check_safety_cushion_mode(new: dict[str, Any]) -> dict[str, Any] | None:
    """边界校验安全垫模式；非法返回错误 dict，否则 None。

    与 formulas.f1_effective_cushion 的兜底 0.0 形成双层防护：边界处直接拒绝
    bogus 模式，避免脏值落盘后再靠兜底掩盖（仍给即时反馈）。
    """
    sc = new.get("safety_cushion") or {}
    mode = (sc.get("mode") or "").strip().lower()
    if mode and mode not in _VALID_CUSHION_MODES:
        return {"ok": False, "error": "invalid_safety_cushion_mode",
                "message": f"安全垫模式 {mode!r} 非法，仅支持 months/fixed/ratio"}
    return None


def preview(data_dir: Path, changes: dict[str, Any]) -> dict[str, Any]:
    """预览修改（不落盘）：before/after + 护栏字段风险提示 + 二次确认 token。"""
    contract = contract_io.read_contract(data_dir)
    new, _ = _apply_changes(contract, changes)
    _mode_err = _check_safety_cushion_mode(new)  # 边界拒绝非法安全垫模式
    if _mode_err:
        return _mode_err
    # 提前校验三区 / §5.4（preview 即暴露 GuardError，避免 confirm 才报错）
    _validate_zones(new, contract, "configurator", confirm=True)

    changed = _diff(contract, new)
    touched_guard = sorted(t for t in changed if t in CORE_GUARD_FIELDS)
    risks = _risk_warnings(new, changed)          # H5 修复：风险提示用修改后契约
    weakening = _is_weakening(changed, contract)  # H4 修复：传入契约算有效安全垫
    tok = _token(changes, _contract_sha(contract))
    consequence = _monthly_consequence(contract, new, changes)  # 层 C 净口径化后果
    return {
        "ok": True, "needs_confirm": True, "preview": True,
        "changed_fields": changed,
        "touched_guard_fields": touched_guard,
        "risk_warnings": risks,
        "cooldown_required": weakening,
        "monthly_consequence": consequence,
        "token": tok,
        "home_purchase": changes.get("record_home_purchase"),
        "message": (
            ("⚠️ 检测到「削弱自身」的护栏修改，确认后将进入 1 个自然日冷静窗"
             "（窗内可无理由撤回，到期前二次提醒并自动生效），不立即落盘。"
             if weakening else
             "以下修改将在确认后落盘（§5.4 二次确认）。核心护栏字段已标注风险提示；")
            + "回复确认修改（带本 token）即生效。")
        if touched_guard else
        ("以下非核心参数修改将在确认后落盘（普通确认）。"
         "回复确认修改（带本 token）即生效。"),
    }


def apply(data_dir: Path, changes: dict[str, Any], *, confirm: bool,
          token: str | None, reason: str) -> dict[str, Any]:
    """应用修改：confirm=False → 返回预览；confirm=True + 正确 token → 落盘 + 写 override_log。

    §5.4 冷却窗：若变更属「削弱自身」（safety_cushion 月数下调 / invest_ratio 下调），
    确认后**不立即落盘**，而是入 `pending_config_changes` 队列、给 1 个自然日冷静窗，
    窗内可无理由撤回（withdraw_config），到期懒惰扫描自动生效（sweep_pending_config）。
    其余变更（含非削弱护栏修改）确认后立即落盘。
    """
    contract = contract_io.read_contract(data_dir)
    expected = _token(changes, _contract_sha(contract))
    if not confirm:
        return preview(data_dir, changes)
    if not secrets.compare_digest(str(token or ""), str(expected)):
        return {
            "ok": False, "error": "stale_token",
            "message": "确认 token 不匹配或契约已变更，请重新预览（customize 不带 --confirm）再确认",
            "expected_token": expected,
        }

    new, _ = _apply_changes(contract, changes)
    _mode_err = _check_safety_cushion_mode(new)  # 边界拒绝非法安全垫模式
    if _mode_err:
        return _mode_err
    changed = _diff(contract, new)
    touched_guard = sorted(t for t in changed if t in CORE_GUARD_FIELDS)
    risks = _risk_warnings(new, changed)          # H5 修复：风险提示用修改后契约

    # —— §5.4 冷却窗：削弱自身 → 进 pending，不落盘配置 ——
    if _is_weakening(changed, contract):          # H4 修复：传入契约算有效安全垫
        now = datetime.now()
        entry = {
            "request_id": secrets.token_hex(6),
            "created_at": now.isoformat(timespec="seconds"),
            "expires_at": (now + timedelta(days=1)).isoformat(timespec="seconds"),
            "changes": changes,
            "preview": {
                "changed_fields": changed,
                "touched_guard_fields": touched_guard,
                "risk_warnings": risks,
            },
            "withdraw_token": secrets.token_hex(8),
            "status": ConfigChangeStatus.PENDING.value,
        }
        contract.setdefault("pending_config_changes", []).append(entry)
        # 仅落盘运行时态（pending 队列），配置区原值未动 → 冷却窗内不生效
        contract_io.write_contract(data_dir, contract, actor="configurator", confirm=True)
        return {
            "ok": True, "applied": False, "pending": True,
            "cooldown_days": 1,
            "request_id": entry["request_id"],
            "withdraw_token": entry["withdraw_token"],
            "expires_at": entry["expires_at"],
            "touched_guard_fields": touched_guard,
            "risk_warnings": risks,
            "note": "削弱自身修改已进入 1 日冷静窗（§5.4）；窗内可无理由撤回，到期自动生效。",
        }

    # —— 其余变更：立即落盘 ——
    contract_io.write_contract(data_dir, new, actor="configurator", confirm=True)
    audit_io.append(data_dir, "override_log", {
        "time": _now(), "event": "contract_customize",
        "changed_fields": changed,
        "touched_guard_fields": touched_guard,
        "risk_warnings": risks,
        "reason": reason or "用户显式自定义（§5.4）",
        "confirm": "已二次确认（token 校验通过）",
    })
    return {
        "ok": True, "applied": True,
        "changed_fields": changed,
        "touched_guard_fields": touched_guard,
        "risk_warnings": risks,
        "monthly_consequence": _monthly_consequence(contract, new, changes),
        "home_purchase": changes.get("record_home_purchase"),
        "note": "配置区增量覆盖完成；审计日志已追加（仅追加，不可改）",
    }


def withdraw_config(data_dir: Path, request_id: str, token: str,
                    *, now: datetime | None = None) -> dict[str, Any]:
    """§5.4 冷却窗内无理由撤回：仅 pending 且未过期可撤；过期则修改已自动生效，不可撤。"""
    contract = contract_io.read_contract(data_dir)
    pcc = contract.get("pending_config_changes", []) or []
    entry = next((e for e in pcc if e["request_id"] == request_id), None)
    if entry is None or entry["status"] != ConfigChangeStatus.PENDING.value:
        return {"ok": False, "error": "not_found",
                "message": f"未找到待撤回的冷却窗修改（request_id={request_id}）"}
    if entry["withdraw_token"] != token:
        return {"ok": False, "error": "bad_token",
                "message": "撤回 token 不匹配（须用确认时返回的 withdraw_token）"}
    now = now or datetime.now()
    if datetime.fromisoformat(entry["expires_at"]) <= now:
        return {"ok": False, "error": "expired",
                "message": "冷却窗已过期，修改已自动生效，不可撤回（详见审计日志）"}
    contract["pending_config_changes"] = [
        e for e in pcc if e["request_id"] != request_id]
    contract_io.write_contract(data_dir, contract, actor="configurator", confirm=True)
    audit_io.append(data_dir, "override_log", {
        "time": _now(), "event": "config_change_withdrawn",
        "request_id": request_id,
        "changed_fields": entry["preview"]["changed_fields"],
        "reason": "冷却窗内无理由撤回（§5.4）",
    })
    return {"ok": True, "withdrawn": True, "request_id": request_id,
            "note": "冷却窗修改已撤回，配置区未变动。"}


def sweep_pending_config(data_dir: Path, *, now: datetime | None = None) -> dict[str, Any]:
    """§5.4 冷却窗懒惰终裁：过期未撤回的 pending 配置修改自动生效（复用 §5.1 范式）。

    返回本次自动生效的 request_id 列表；无过期项则返回空。
    """
    now = now or datetime.now()
    contract = contract_io.read_contract(data_dir)
    # 全程在契约深拷贝上操作，避免 contract 原引用与 work 深拷贝链脱节
    # （旧实现 pcc=contract.get(...) 取原列表，依赖下方重建才侥幸正确）。
    work = copy.deepcopy(contract)
    pcc = work.get("pending_config_changes", []) or []
    expired: list[dict[str, Any]] = []
    for e in pcc:
        if e["status"] == ConfigChangeStatus.PENDING.value and datetime.fromisoformat(e["expires_at"]) <= now:
            expired.append(e)
    if not expired:
        return {"ok": True, "applied": [], "pending_count": len(pcc)}

    failed: list[dict[str, Any]] = []
    for e in expired:
        try:
            work, _ = _apply_changes(work, e["changes"])
            e["status"] = ConfigChangeStatus.APPLIED.value
        except Exception as ex:
            # M3：单条过期修改应用失败（如字段已不存在）→ 标记 failed 不阻塞其余，
            # 不把契约写成脏状态；failed 项保留在 pending_config_changes 供排查，
            # 下次扫描不再误当作 pending 重跑（status≠pending）。
            e["status"] = ConfigChangeStatus.FAILED.value
            e["error"] = str(ex)
            failed.append({"request_id": e["request_id"], "error": str(ex)})
    # M5：到期自动生效的条目（status=applied）从待决队列移除；failed 项保留。
    # pcc 即 work 自身的 pending_config_changes 列表，状态已在上面就地更新。
    work["pending_config_changes"] = [e for e in pcc if e["status"] != ConfigChangeStatus.APPLIED.value]
    contract_io.write_contract(data_dir, work, actor="configurator", confirm=True)
    for e in expired:
        if e["status"] != ConfigChangeStatus.APPLIED.value:
            continue
        audit_io.append(data_dir, "override_log", {
            "time": _now(), "event": "contract_customize_cooled",
            "request_id": e["request_id"],
            "changed_fields": e["preview"]["changed_fields"],
            "touched_guard_fields": e["preview"]["touched_guard_fields"],
            "risk_warnings": e["preview"]["risk_warnings"],
            "reason": "冷却窗到期自动生效（§5.4）",
        })
    return {"ok": True, "applied": [e["request_id"] for e in expired if e["status"] == ConfigChangeStatus.APPLIED.value],
            "failed": failed, "pending_count": len([e for e in pcc if e["status"] == ConfigChangeStatus.PENDING.value])}


def review_config(data_dir: Path, *, now: datetime | None = None) -> dict[str, Any]:
    """§5.4 冷却窗复查：先懒惰扫描过期项自动生效，再列出仍在窗内的待决修改 + 二次提醒。"""
    swept = sweep_pending_config(data_dir, now=now)
    contract = contract_io.read_contract(data_dir)
    now = now or datetime.now()
    pcc = contract.get("pending_config_changes", []) or []
    items: list[dict[str, Any]] = []
    for e in pcc:
        if e["status"] != ConfigChangeStatus.PENDING.value:
            continue
        exp = datetime.fromisoformat(e["expires_at"])
        days_left = (exp.date() - now.date()).days
        items.append({
            "request_id": e["request_id"],
            "expires_at": e["expires_at"],
            "days_left": days_left,
            "kind": "expiring" if days_left <= 1 else "cooling",
            "changed_fields": e["preview"]["changed_fields"],
            "risk_warnings": e["preview"]["risk_warnings"],
        })
    return {
        "ok": True, "swept": swept["applied"], "pending": items,
        "message": ("冷却窗内可无理由撤回（customize --withdraw --request-id X --token T）；"
                    "到期前二次提醒并自动生效（§5.4，复用 §5.1 机制）。"),
    }
