"""Public Finder interaction semantics for the gateway videos/info response.

The legacy gateway calls Finder favCount 'favoriteCount' and keeps likeCount.
Finder fav is the private like (heart); Finder like is public recommendation.
Neither is the separate global collection action. Do not apply this mapping to
comment likes, other platforms, or data explicitly normalized with this version.
"""
from copy import deepcopy
from decimal import Decimal, InvalidOperation

SEMANTICS_VERSION = "wechat-channels-interactions-v2"
INTERACTION_KEYS = (("likeCount", "点赞"), ("shareCount", "转发"),
                    ("commentCount", "评论"), ("recommendCount", "推荐"))
METRIC_NOTE = "点赞与推荐分别统计；本接口未提供独立收藏数，不据此判断收藏或存档需求。"
METHOD_NOTE = ("占比 = 该项 /（点赞+转发+评论+推荐）；相对比值 = 该项 / 点赞。"
               "仅四项均有精确值且点赞大于 0 时计算结构；计数相加不等于去重人数，"
               "无播放量不计算互动率，也不由计数直接判断传播原因、情绪或存档价值。")


def exact_count(value):
    """Preserve integers exactly; unknown/rounded/invalid values are not zero."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None
    if not number.is_finite() or number < 0 or number != number.to_integral_value():
        return None
    return int(number)


def norm_metrics(metrics):
    return {key: exact_count((metrics or {}).get(key)) for key, _ in INTERACTION_KEYS}


def normalize_info(payload):
    """Return a new payload; preserve originals and never remap canonical data."""
    if not payload:
        return payload
    result = deepcopy(payload)
    data = result.setdefault("data", {})
    version = data.get("metricSemanticsVersion")
    if version not in (None, "", SEMANTICS_VERSION):
        raise ValueError("未知视频号指标口径：%s；请核对接口契约后再分析" % version)
    metrics = data.get("metrics") or {}
    details = data.get("metricDetails") or {}
    mapping = {key: key for key, _ in INTERACTION_KEYS}
    if version != SEMANTICS_VERSION:
        mapping.update(likeCount="favoriteCount", recommendCount="likeCount")
    normalized, normalized_details = {}, {}
    for key, source in mapping.items():
        detail = details.get(source) or {}
        raw_value = metrics.get(source)
        value = exact_count(raw_value)
        if detail.get("exact") is False or detail.get("relation") not in (None, "", "exact"):
            value = None
        elif value is None and detail.get("exact") is True:
            value = exact_count(detail.get("value"))
        display = str(detail.get("display") or (raw_value if raw_value is not None else ""))
        normalized[key] = value
        normalized_details[key] = {
            "value": value, "exact": value is not None,
            "display": display or (str(value) if value is not None else ""),
            "relation": "exact" if value is not None else detail.get("relation") or "unknown",
        }
    data["metrics"], data["metricDetails"] = normalized, normalized_details
    data["metricSemanticsVersion"] = SEMANTICS_VERSION
    return result


def interaction_basis(payload, is_local=False):
    data = (normalize_info(payload) or {}).get("data") or {}
    return {
        "semanticsVersion": SEMANTICS_VERSION,
        "isLocal": bool(is_local),
        "metrics": {} if is_local else norm_metrics(data.get("metrics")),
        "metricDetails": {} if is_local else data.get("metricDetails", {}),
    }


def metric_display(data, key):
    value = (data.get("metrics") or {}).get(key)
    if value is not None:
        return format(value, ",")
    display = (data.get("metricDetails") or {}).get(key, {}).get("display")
    return (str(display) + "（非精确值）") if display else "未获取"


def interaction_total(metrics):
    counts = norm_metrics(metrics)
    return sum(counts.values()) if all(v is not None for v in counts.values()) else None


def infer_interaction_profile(metrics):
    """Describe observed structure, without turning likes into collection intent."""
    values = norm_metrics(metrics)
    total = interaction_total(values)
    like = values["likeCount"]
    if total is None or not total or not like:
        return None
    counts = {label: values[key] for key, label in INTERACTION_KEYS}
    shares = {label: round(value * 100 / total, 1) for label, value in counts.items()}
    ratios = {label + "/点赞": round(value * 100 / like, 1)
              for label, value in counts.items() if label != "点赞"}
    dominant = max(counts, key=counts.get)
    signals = [(label, "占比", "%s %s，占四项计数之和 %.1f%%。" %
                (label, format(count, ","), shares[label])) for label, count in counts.items()]
    return {
        "counts": counts, "total": total, "shares": shares, "ratios": ratios,
        "dominant": dominant, "type": dominant + "占比最高",
        "signals": signals,
        "actions": ["结合具体画面和评论内容解释互动表现；没有收藏、触达及转化数据时，不作这些维度的结论。"],
    }


def normalize_gateway_channels(data):
    """Known Finder projections only; comment and non-WeChat metrics are untouched."""
    if not isinstance(data, dict):
        return data
    result = deepcopy(data)
    if isinstance(result.get("metrics"), dict):
        original_metrics, original_details = result["metrics"], result.get("metricDetails") or {}
        result = normalize_info({"data": result})["data"]
        # Playback remains optional and never becomes an invented denominator.
        view = exact_count(original_metrics.get("viewCount"))
        detail = original_details.get("viewCount") or {}
        if view is not None and detail.get("exact") is not False and detail.get("relation") in (None, "", "exact"):
            result["metrics"]["viewCount"] = view
        if detail:
            result["metricDetails"]["viewCount"] = detail
    for name in ("items", "videos"):
        if isinstance(result.get(name), list):
            result[name] = [normalize_gateway_channels(item) for item in result[name]]
    return result
