#!/usr/bin/env python3
"""Check supplied promotion facts locally; this program makes no external calls."""
import json, sys
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

def money(value):
    result = Decimal(str(value))
    if not result.is_finite(): raise InvalidOperation
    return result
def value_or_none(value):
    try: return money(value)
    except (InvalidOperation, ValueError, TypeError): return None

def has_confirmed_zero_discount(rule):
    """Whether a rule is known to leave balances unchanged.

    Percentage rules require a merchant-confirmed rounding convention even
    when their nominal deduction is zero.  Without it, the rule remains a
    pending calculation and must not be used to prove that allocation or a
    later payable result is unaffected.
    """
    kind = rule.get("type")
    if kind == "fixed": return value_or_none(rule.get("amount")) == Decimal("0")
    if kind == "percent":
        return (value_or_none(rule.get("percent")) == Decimal("100")
                and rule.get("rounding_mode") == "total_half_up_2")
    return False

def display_money(value):
    cents = value.quantize(Decimal("0.01"))
    return f"{value:.2f}" if value == cents else format(value, "f")

def non_negative(value, label):
    parsed = value_or_none(value)
    if parsed is None or parsed < 0:
        raise ValueError(f"{label}必须是非负的有效金额")
    return parsed

def positive_quantity(value):
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("购物行数量必须是正整数")
    if not parsed.is_finite() or parsed <= 0 or parsed != parsed.to_integral_value():
        raise ValueError("购物行数量必须是正整数")
    return int(parsed)

def definitely_unavailable_for_current_cart(rule, current_skus, lines, shipping, now):
    eligible_skus = rule.get("eligible_skus")
    if not isinstance(eligible_skus, list) or not current_skus.intersection(eligible_skus):
        return True
    if rule.get("start") and rule.get("end") and now and rule.get("timezone"):
        try:
            zone = ZoneInfo(rule["timezone"])
            start = datetime.fromisoformat(rule["start"])
            end = datetime.fromisoformat(rule["end"])
            current = datetime.fromisoformat(now)
            if all(value.tzinfo for value in (start, end, current)):
                start, end, current = start.astimezone(zone), end.astimezone(zone), current.astimezone(zone)
                if start <= end and not start <= current <= end:
                    return True
        except (ValueError, TypeError, ZoneInfoNotFoundError):
            pass
    basis, threshold = rule.get("threshold_basis"), value_or_none(rule.get("threshold"))
    includes_shipping = rule.get("threshold_includes_shipping")
    if basis in ("商品额", "优惠前商品额", "优惠后商品额") and threshold is not None and isinstance(includes_shipping, bool) and (not includes_shipping or shipping is not None):
        applicable = sum((line["original"] for line in lines if line["sku"] in eligible_skus), Decimal("0"))
        if includes_shipping:
            applicable += shipping
        if applicable < threshold:
            return True
    return False

def known_discount_for_scope(rule, skus, balance, lines, shipping, now):
    """Return a fully determined discount for an exact SKU scope, else None."""
    eligible_skus = rule.get("eligible_skus")
    if not isinstance(eligible_skus, list) or set(eligible_skus) != set(skus):
        return None
    if rule.get("start") and rule.get("end") and now and rule.get("timezone"):
        try:
            zone = ZoneInfo(rule["timezone"])
            start = datetime.fromisoformat(rule["start"])
            end = datetime.fromisoformat(rule["end"])
            current = datetime.fromisoformat(now)
            if not all(value.tzinfo for value in (start, end, current)):
                return None
            start, end, current = (value.astimezone(zone) for value in (start, end, current))
            if start > end or not start <= current <= end:
                return Decimal("0")
        except (ValueError, TypeError, ZoneInfoNotFoundError):
            return None
    else:
        return None
    basis, threshold = rule.get("threshold_basis"), value_or_none(rule.get("threshold"))
    includes_shipping = rule.get("threshold_includes_shipping")
    if (basis not in ("商品额", "优惠前商品额", "优惠后商品额") or threshold is None
            or not isinstance(includes_shipping, bool) or (includes_shipping and shipping is None)):
        return None
    original = sum((line["original"] for line in lines if line["sku"] in skus), Decimal("0"))
    threshold_base = original if basis in ("商品额", "优惠前商品额") else balance
    if includes_shipping:
        threshold_base += shipping
    if threshold_base < threshold:
        return Decimal("0")
    kind = rule.get("type")
    if kind == "fixed":
        amount = value_or_none(rule.get("amount"))
        return amount if amount is not None and Decimal("0") <= amount <= balance else None
    if kind == "percent":
        percent = value_or_none(rule.get("percent"))
        if percent is None or not Decimal("0") <= percent <= Decimal("100") or rule.get("rounding_mode") != "total_half_up_2":
            return None
        deduction = (balance * (Decimal("100") - percent) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return deduction if deduction <= balance else None
    return None

def later_split_matters(later_rules, current_skus, balance, lines, shipping, now):
    """Check whether a later partial-SKU offer can observe an earlier split.

    A known full-scope offer that consumes the remaining aggregate balance
    makes any earlier line allocation unobservable to still-later offers.
    """
    remaining = balance
    aggregate_known = True
    for later in later_rules:
        if not isinstance(later, dict):
            continue
        eligible = later.get("eligible_skus")
        if not isinstance(eligible, list) or not (current_skus & set(eligible)):
            continue
        if has_confirmed_zero_discount(later):
            continue
        if definitely_unavailable_for_current_cart(later, current_skus, lines, shipping, now):
            continue
        eligible_scope = set(eligible)
        # A later offer that includes every SKU affected by the current split
        # only reads their combined balance. Extra eligible SKUs add known
        # amounts to that aggregate; they do not expose how the earlier
        # discount was divided within current_skus. Only a proper subset of
        # the affected scope can observe that division.
        # Allocation only becomes observable if this later rule *omits* an
        # SKU touched by the earlier discount.  It may cover the same scope
        # or a superset: in either case it reads the invariant combined
        # balance of current_skus, rather than the unknown line split.
        omitted_current_skus = current_skus - eligible_scope
        if omitted_current_skus:
            return True
        if eligible_scope > current_skus:
            if aggregate_known and later_guarantees_clear_scope(later, eligible_scope, current_skus, remaining, lines, shipping, now):
                return False
            # A non-clearing superset offer can change the total amount left
            # on the current SKUs, but without merchant allocation facts we
            # cannot attribute that aggregate back to this subset afterward.
            aggregate_known = False
            continue
        discount = known_discount_for_scope(later, current_skus, remaining, lines, shipping, now)
        if discount is None:
            # The rule still applies to the complete affected SKU scope, so
            # its missing value cannot observe the earlier line allocation.
            # A later proper subset, if any, will still be caught below.
            aggregate_known = False
            continue
        if discount == remaining:
            return False
        if aggregate_known:
            remaining -= discount
    return False

def later_guarantees_clear_scope(rule, eligible_scope, current_skus, current_balance, lines, shipping, now):
    """Whether a full-scope superset offer is certain to zero every balance."""
    if not current_skus.issubset(eligible_scope):
        return False
    # The earlier split changes individual rows, not the aggregate for this
    # complete scope.  Therefore a positive, confirmed threshold can also be
    # proved here when its selected basis is known; limiting this proof to a
    # zero threshold would incorrectly retain an allocation dependency.
    basis, threshold = rule.get("threshold_basis"), value_or_none(rule.get("threshold"))
    includes_shipping = rule.get("threshold_includes_shipping")
    if (basis not in ("商品额", "优惠前商品额", "优惠后商品额")
            or threshold is None or not isinstance(includes_shipping, bool)):
        return False
    if includes_shipping and shipping is None:
        return False
    if not (rule.get("start") and rule.get("end") and now and rule.get("timezone")):
        return False
    try:
        zone = ZoneInfo(rule["timezone"])
        start = datetime.fromisoformat(rule["start"])
        end = datetime.fromisoformat(rule["end"])
        current = datetime.fromisoformat(now)
    except (ValueError, TypeError, ZoneInfoNotFoundError, KeyError):
        return False
    try:
        if not all(value.tzinfo for value in (start, end, current)):
            return False
        start, end, current = start.astimezone(zone), end.astimezone(zone), current.astimezone(zone)
        if start > end or not start <= current <= end:
            return False
    except (ValueError, TypeError, ZoneInfoNotFoundError):
        return False
    extra_balance = sum((line["remaining"] for line in lines if line["sku"] in eligible_scope - current_skus), Decimal("0"))
    total_balance = current_balance + extra_balance
    original_total = sum((line["original"] for line in lines if line["sku"] in eligible_scope), Decimal("0"))
    threshold_base = original_total if basis in ("商品额", "优惠前商品额") else total_balance
    if includes_shipping:
        threshold_base += shipping
    if threshold_base < threshold:
        return False
    if rule.get("type") == "fixed":
        return value_or_none(rule.get("amount")) == total_balance
    if (rule.get("type") == "percent" and value_or_none(rule.get("percent")) == Decimal("0")
            and rule.get("rounding_mode") == "total_half_up_2"):
        deduction = (total_balance * Decimal("100") / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return deduction == total_balance
    return False

def decimal_working_precision(data):
    """Return a context large enough for every supplied decimal calculation.

    JSON numbers have already been parsed as ``Decimal`` before this is called.
    Twice the serialized input size comfortably covers multiplication and
    addition across the documented 20-line cart without falling back to the
    process-wide default precision of 28 significant digits.
    """
    return max(100, len(str(data)) * 2)

def main(data):
    # Keep precision local to this evaluation.  Callers that import ``main``
    # therefore get the same exact-decimal behaviour as the command-line tool.
    with localcontext() as context:
        context.prec = decimal_working_precision(data)
        return _main(data)

def _main(data):
    rules, items = data.get("promotions", []), data.get("cart", [])
    if len(rules) > 10 or len(items) > 20: raise ValueError("最多支持10条优惠规则和20条购物行")
    if not data.get("currency"): raise ValueError("缺少 currency")
    names = [rule.get("name", "未命名优惠") for rule in rules]
    if len(set(names)) != len(names): raise ValueError("优惠名称重复；请提供唯一名称后再核对叠加顺序")
    if not isinstance(items, list) or not isinstance(rules, list): raise ValueError("cart 和 promotions 必须是列表")
    lines = []
    for item_index, item in enumerate(items):
        if not isinstance(item, dict): raise ValueError("购物行必须是对象")
        if not isinstance(item.get("sku"), str) or not item["sku"].strip():
            raise ValueError("购物行缺少可核对的 SKU，不能判断优惠适用范围")
        line_total = non_negative(item.get("unit_price"), "商品单价") * positive_quantity(item.get("quantity"))
        lines.append({"line": item_index + 1, "sku": item.get("sku"), "original": line_total, "remaining": line_total})
    subtotal = sum((line["original"] for line in lines), Decimal("0"))
    shipping = None if data.get("shipping_fee") is None else non_negative(data["shipping_fee"], "运费")
    conditions, calculations = [], []
    now, order = data.get("current_time"), data.get("stacking_order")
    uncertain_skus = set()
    uncertain_all_skus = False
    order_valid = isinstance(order, list) and len(order) == len(rules) and set(order) == set(names)
    if len(rules) > 1 and order_valid:
        by_name = {rule.get("name", "未命名优惠"): rule for rule in rules}
        rules = [by_name[name] for name in order]
    for rule_index, rule in enumerate(rules):
        if not isinstance(rule, dict): raise ValueError("优惠规则必须是对象")
        name = rule.get("name", "未命名优惠")
        checks = []
        reasons = []
        def check(label, state, detail):
            checks.append({"条件": label, "状态": state, "依据": detail})
            if state == "不可用": reasons.append(detail)
        eligible_skus = rule.get("eligible_skus")
        sku_known = isinstance(eligible_skus, list) and bool(eligible_skus) and all(isinstance(sku, str) and sku.strip() for sku in eligible_skus)
        if not sku_known:
            check("适用SKU", "待确认", "未提供适用SKU")
            eligible_skus = []
        else:
            matching_skus = {line["sku"] for line in lines} & set(eligible_skus)
            if matching_skus:
                check("适用SKU", "可用", "适用SKU：" + "、".join(map(str, sorted(matching_skus))))
            else:
                check("适用SKU", "不可用", "购物车不含该优惠适用的SKU")
        eligible = [line for line in lines if line["sku"] in eligible_skus]
        current_skus = {line["sku"] for line in eligible}
        prior_promo_uncertain = uncertain_all_skus or bool(current_skus & uncertain_skus)
        prior_uncertain_skus = current_skus & uncertain_skus
        prior_uncertain_lines = [line for line in eligible if uncertain_all_skus or line["sku"] in uncertain_skus]
        before = sum((line["original"] for line in eligible), Decimal("0"))
        after = sum((line["remaining"] for line in eligible), Decimal("0"))

        if rule.get("start") and rule.get("end") and now and rule.get("timezone"):
            try:
                zone = ZoneInfo(rule["timezone"])
                start = datetime.fromisoformat(rule["start"])
                end = datetime.fromisoformat(rule["end"])
                current = datetime.fromisoformat(now)
                if not all(x.tzinfo for x in (start, end, current)):
                    check("有效期", "待确认", "时间必须包含明确时区偏移")
                elif start.astimezone(zone) > end.astimezone(zone):
                    check("有效期", "待确认", "开始时间晚于结束时间；优惠有效期区间无效，需商家确认")
                else:
                    valid = start.astimezone(zone) <= current.astimezone(zone) <= end.astimezone(zone)
                    check("有效期", "可用" if valid else "不可用", "当前时间在有效期内" if valid else "当前时间不在有效期内")
            except (ValueError, TypeError, ZoneInfoNotFoundError):
                check("有效期", "待确认", "有效期或时区无效，需商家确认")
        else: check("有效期", "待确认", "有效期、当前时间或优惠时区未完整提供")

        basis, threshold = rule.get("threshold_basis"), value_or_none(rule.get("threshold"))
        if threshold is not None and threshold < 0:
            raise ValueError("门槛金额必须是非负的有效金额")
        includes_shipping = rule.get("threshold_includes_shipping")
        if not isinstance(includes_shipping, bool):
            check("门槛运费口径", "待确认", "运费是否计入门槛未明确")
        if basis not in ("商品额", "优惠前商品额", "优惠后商品额"):
            check("门槛", "待确认", "门槛口径未明确")
        elif threshold is None:
            check("门槛", "待确认", "门槛金额未提供")
        elif not isinstance(includes_shipping, bool):
            check("门槛", "待确认", f"门槛金额 {threshold}；运费是否计入未明确")
        elif includes_shipping and shipping is None:
            check("门槛", "待确认", f"门槛金额 {threshold}；计入运费但未提供运费金额")
        elif not sku_known:
            check("门槛", "待确认", f"门槛金额 {threshold}；适用SKU未明确，无法确定适用金额")
        elif basis == "优惠后商品额" and threshold > before + (shipping if includes_shipping else Decimal("0")):
            maximum = before + (shipping if includes_shipping else Decimal("0"))
            check("门槛", "不可用", f"门槛金额 {threshold}；优惠后商品额不可能高于优惠前上限 {maximum}，门槛必不可能达到")
        elif basis == "优惠后商品额" and prior_promo_uncertain:
            # Earlier unresolved offers can only reduce the applicable goods
            # amount; they cannot make it negative.  Therefore confirmed
            # shipping is a deterministic lower bound for a post-discount
            # threshold.  In particular, a zero goods-only threshold is
            # always met, even if the SKU-level allocation is unknown.
            lower_bound = shipping if includes_shipping else Decimal("0")
            if threshold > lower_bound:
                check("门槛", "待确认", f"门槛金额 {threshold}；前序优惠状态待确认，优惠后金额仅可确认不低于 {lower_bound}")
            else:
                check("门槛", "可用", f"门槛金额 {threshold}；前序优惠虽待确认，但已知下界 {lower_bound}（运费{('计入' if includes_shipping else '不计入')}）仍达到门槛")
        else:
            base = before if basis in ("商品额", "优惠前商品额") else after
            if includes_shipping: base += shipping
            meets = base >= threshold
            check("门槛", "可用" if meets else "不可用",
                  f"门槛金额 {threshold}；{basis}适用金额 {base}（运费{('计入' if includes_shipping else '不计入')}）" + ("，达到门槛" if meets else "，门槛不足"))
        if len(rules) > 1:
            check("叠加顺序", "可用" if order_valid else "待确认", "已按明确顺序核对" if order_valid else "叠加顺序未明确")

        kind = rule.get("type")
        amount = value_or_none(rule.get("amount")) if kind == "fixed" else None
        # `percent` is the payable percentage, matching common Chinese
        # promotion wording: 90 means "九折" (pay 90%), not 90% off.
        percent = value_or_none(rule.get("percent")) if kind == "percent" else None
        if amount is not None and amount < 0:
            raise ValueError("固定优惠金额必须是非负的有效金额")
        if percent is not None and not Decimal("0") <= percent <= Decimal("100"):
            raise ValueError("折扣比例必须在 0 至 100 之间")
        if kind == "fixed":
            if amount is None:
                check("优惠值", "待确认", "满减金额未提供")
            elif amount == Decimal("0"):
                # A confirmed zero amount cannot alter any balance, even if a
                # previous rule is still unresolved.
                check("优惠值", "可用", "固定优惠金额 0（不改变商品余额）")
            elif prior_promo_uncertain:
                check("优惠值", "待确认", "同一适用SKU的前序优惠状态待确认；当前可抵扣余额无法确定")
            elif amount > after:
                check("优惠值", "待确认", f"固定优惠金额 {amount} 超过当前适用商品余额 {after}；余额不足时如何处理未提供商家规则")
            else:
                check("优惠值", "可用", f"固定优惠金额 {amount}")
        elif kind == "percent":
            if percent is None:
                check("优惠值", "待确认", "折扣比例未提供")
            elif percent == Decimal("100"):
                check("优惠值", "可用", "折扣比例 100%（应付比例；不改变商品余额）")
            elif prior_promo_uncertain:
                check("优惠值", "待确认", "同一适用SKU的前序优惠状态待确认；当前折扣基数无法确定")
            else:
                check("优惠值", "可用", f"折扣比例 {percent}%（应付比例）")
            rounding_mode = rule.get("rounding_mode")
            check("金额舍入", "可用" if rounding_mode == "total_half_up_2" else "待确认",
                  "已确认：先按适用金额合计计算减免，再以四舍五入保留两位小数" if rounding_mode == "total_half_up_2" else "未提供经商家确认的金额舍入规则")
        else: check("优惠值", "待确认", "优惠类型未明确")

        # Allocation is only material when a later rule selects a proper
        # subset of this rule's affected SKU set. A later rule covering every
        # affected SKU (including the exact same set) sees the same aggregate
        # remaining amount regardless of how the earlier total was split.
        no_discount = has_confirmed_zero_discount(rule)
        preliminary_states = [entry["状态"] for entry in checks]
        preliminary_status = "不可用" if "不可用" in preliminary_states else ("待确认" if "待确认" in preliminary_states else "可用")
        # A percentage rule is allocation-independent whenever the actual
        # rounded discount consumes the whole applicable balance, whatever
        # nominal rate produced it (including sub-cent totals).
        rounded_percent_deduction = (
            (after * (Decimal("100") - percent) / Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP)
            if kind == "percent" and percent is not None
            and rule.get("rounding_mode") == "total_half_up_2" else None
        )
        # Do not infer this from the nominal payable rate.  A non-zero rate
        # can still consume a tiny aggregate balance after the confirmed
        # total-level rounding rule is applied.
        percent_clears_balance = (
            rounded_percent_deduction is not None
            and rounded_percent_deduction == after
        )
        guarantees_zero_balance = (preliminary_status == "可用" and (
            (kind == "fixed" and amount == after) or percent_clears_balance
        ))
        current_discount_preview = (
            amount if kind == "fixed" and amount is not None and amount <= after else
            (after * (Decimal("100") - percent) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if kind == "percent" and percent is not None and rule.get("rounding_mode") == "total_half_up_2" else
            Decimal("0")
        )
        later_splits_current = later_split_matters(
            rules[rule_index + 1:], current_skus, after - current_discount_preview, lines, shipping, now
        # An unavailable current rule cannot affect a later balance, even if
        # some unrelated facts on that rule are absent.  In particular, never
        # request an allocation rule for an expired promotion.
        ) and preliminary_status == "可用" and not no_discount and not guarantees_zero_balance
        multiple_lines = len([line for line in eligible if line["remaining"] > 0]) > 1
        if multiple_lines and later_splits_current and kind in ("fixed", "percent"):
            allocation = rule.get("allocation_rule")
            check("优惠分摊", "可用" if allocation == "cart_order" else "待确认",
                  "已确认按购物车商品行顺序分摊" if allocation == "cart_order" else "后续优惠会覆盖本优惠的部分SKU，未提供商家确认的分摊规则")

        if (kind == "percent" and percent is not None and rule.get("rounding_mode") == "total_half_up_2"
                and not prior_promo_uncertain):
            preview = (after * (Decimal("100") - percent) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if preview > after:
                check("优惠值", "待确认", f"按 total_half_up_2 舍入后的优惠额 {preview} 超过适用商品余额 {after}；余额不足时如何处理未提供商家规则")

        states = [entry["状态"] for entry in checks]
        status = "不可用" if "不可用" in states else ("待确认" if "待确认" in states else "可用")
        discount = Decimal("0")
        raw_discount = None
        rounding_detail = "金额待确认，无法执行舍入"
        deduction_by_line = {}
        if status == "可用":
            discount_rate = Decimal("100") - percent if kind == "percent" else None
            # A fixed amount reaches this branch only after the explicit
            # amount <= applicable-balance check above.  Do not cap it here:
            # silently changing an over-balance amount into the balance would
            # invent a platform rule and produce a misleading payable draft.
            if kind == "fixed":
                discount = amount
                rounding_detail = f"固定减免按确认金额 {display_money(discount)} 计，无额外舍入"
            else:
                raw_discount = after * discount_rate / Decimal("100")
                discount = raw_discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                rounding_detail = (f"原始减免 {display_money(raw_discount)}；"
                                   f"按 total_half_up_2 四舍五入至分为 {display_money(discount)}")
            left = discount
            for line in eligible:
                # Internal row allocation is only used when later scoped
                # rules cannot observe it. Never present that fallback as a
                # merchant-confirmed per-line deduction.
                before_line = line["remaining"]
                line_discount = min(line["remaining"], left)
                line["remaining"] -= line_discount
                if rule.get("allocation_rule") == "cart_order" or len(eligible) == 1:
                    deduction_by_line[line["line"]] = before_line - line["remaining"]
                left -= line_discount
            if left != 0:
                raise ValueError("优惠计算金额超过适用商品余额；未生成应付草稿")
        elif status == "待确认" and not no_discount:
            if current_skus:
                uncertain_skus.update(current_skus)
            else:
                uncertain_all_skus = True
        # Keep the result as a condition table rather than hiding individual
        # findings behind one promotion-level result.  A promotion can be
        # pending for time while its threshold is already known to fail.
        conditions.extend({"优惠": name, **entry} for entry in checks)
        # A zero discount is known not to change any balance.  Missing facts
        # about its eligibility must remain visible in the condition table,
        # but cannot make a later scoped promotion or payable draft unknown.
        uncertain_step = status == "待确认" and not no_discount
        line_deductions = []
        for line in eligible:
            if status == "不可用":
                line_deductions.append({"购物行": line["line"], "SKU": line["sku"], "本步扣减": "0.00", "依据": "本优惠已确定不可用，不改变商品余额"})
            elif line in prior_uncertain_lines:
                line_deductions.append({"购物行": line["line"], "SKU": line["sku"], "本步扣减": "待确认", "依据": "前序优惠影响该SKU余额"})
            elif status == "待确认":
                line_deductions.append({"购物行": line["line"], "SKU": line["sku"], "本步扣减": "待确认", "依据": "本优惠存在待确认条件，不能确定行级扣减"})
            elif status == "可用" and discount and line["line"] not in deduction_by_line:
                line_deductions.append({"购物行": line["line"], "SKU": line["sku"], "本步扣减": "待确认", "依据": "未提供商家确认的行级分摊规则"})
            elif status == "可用" and discount:
                line_deductions.append({"购物行": line["line"], "SKU": line["sku"], "本步扣减": display_money(deduction_by_line.get(line["line"], Decimal("0")))})
            else:
                line_deductions.append({"购物行": line["line"], "SKU": line["sku"], "本步扣减": "0.00"})
        current_balance = "待确认" if prior_promo_uncertain else display_money(after)
        # A rule that has already failed a condition has no applied formula:
        # showing its nominal fixed/percentage expression alongside a zero
        # amount can read as if the discount were still being attempted.
        formula = ("本优惠已确定不可用；实际应用金额 0.00，不改变商品余额"
                   if status == "不可用" else
                   f"固定减免 {display_money(amount)}；适用SKU当前优惠前余额 {current_balance}"
                   if kind == "fixed" and amount is not None else
                   f"{current_balance} × (100% − {percent}%)，总额舍入至分"
                   if kind == "percent" and percent is not None and rule.get("rounding_mode") == "total_half_up_2" else
                   f"待确认：{current_balance} × (100% − {percent}%)；缺少商家确认的金额舍入规则"
                   if kind == "percent" and percent is not None else "金额规则未提供")
        calculation_basis = {"适用SKU": sorted(current_skus), "当前优惠前余额": current_balance,
                             "公式": formula, "行级扣减": line_deductions,
                             "舍入过程": rounding_detail,
                             "前序不确定SKU": sorted(prior_uncertain_skus),
                             "状态说明": "金额待确认" if uncertain_step else "按所列公式计算"}
        total_subtotal_uncertain = uncertain_all_skus or any(line["sku"] in uncertain_skus for line in lines)
        calculations.append({"优惠": name, "优惠额": "待确认" if uncertain_step else display_money(discount),
                             "应付小计": "待确认" if uncertain_step or total_subtotal_uncertain else display_money(sum((line["remaining"] for line in lines), Decimal("0"))),
                             "计算依据": calculation_basis})
    payable = sum((line["remaining"] for line in lines), Decimal("0")) + (shipping if shipping is not None else Decimal("0"))
    payable_uncertain = shipping is None or any(step["优惠额"] == "待确认" for step in calculations)
    calculation = {"商品额": display_money(subtotal), "steps": calculations, "应付草稿": "待确认" if payable_uncertain else display_money(payable)}
    calculation["运费"] = display_money(shipping) if shipping is not None else "待确认"
    return {"currency": data["currency"], "conditions": conditions, "calculation": calculation, "note": "仅按输入核对；不查询价格、领券、下单或认定平台规则。"}

if __name__ == "__main__":
    try:
        raw_input = sys.stdin.read()
        result = main(json.loads(raw_input, parse_float=Decimal))
        print(json.dumps(result, ensure_ascii=False, indent=2, default=lambda value: str(value) if isinstance(value, Decimal) else TypeError()))
    except Exception as e: print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr); sys.exit(1)
