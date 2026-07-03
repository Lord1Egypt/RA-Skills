import pandas as pd
import numpy as np
from collections import defaultdict

A2_TABLE = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308,
            11: 0.285, 12: 0.266, 13: 0.249, 14: 0.235, 15: 0.223, 16: 0.212, 17: 0.203, 18: 0.194,
            19: 0.187, 20: 0.180, 21: 0.173, 22: 0.167, 23: 0.162, 24: 0.157, 25: 0.153}
D3_TABLE = {2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223,
            11: 0.256, 12: 0.284, 13: 0.308, 14: 0.329, 15: 0.348, 16: 0.364, 17: 0.379, 18: 0.392,
            19: 0.404, 20: 0.414, 21: 0.425, 22: 0.434, 23: 0.443, 24: 0.452, 25: 0.459}
D4_TABLE = {2: 3.267, 3: 2.575, 4: 2.282, 5: 2.115, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777,
            11: 1.744, 12: 1.716, 13: 1.692, 14: 1.671, 15: 1.652, 16: 1.636, 17: 1.621, 18: 1.608,
            19: 1.597, 20: 1.586, 21: 1.577, 22: 1.568, 23: 1.560, 24: 1.553, 25: 1.547}
D2_TABLE = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078,
            11: 3.173, 12: 3.258, 13: 3.336, 14: 3.407, 15: 3.472, 16: 3.532, 17: 3.588, 18: 3.640,
            19: 3.689, 20: 3.735, 21: 3.778, 22: 3.819, 23: 3.858, 24: 3.895, 25: 3.931}


def _get_control_chart_constants(n: int) -> dict:
    if n < 2:
        return {"A2": 2.66, "D3": 0.0, "D4": 3.267, "d2": 1.128}
    if n > 25:
        return {"A2": 3.0 / np.sqrt(n), "D3": max(0.0, 1 - 3 * np.sqrt(2 / n)), "D4": 1 + 3 * np.sqrt(2 / n), "d2": 4 * (n - 0.5) / (4 * n - 3)}
    return {"A2": A2_TABLE[n], "D3": D3_TABLE[n], "D4": D4_TABLE[n], "d2": D2_TABLE[n]}


def _imr_chart(measurements: np.ndarray) -> dict:
    x_bar = float(np.mean(measurements))
    mr = np.abs(np.diff(measurements))
    mr_bar = float(np.mean(mr))
    const = _get_control_chart_constants(2)
    ucl_x = x_bar + const["A2"] * mr_bar
    lcl_x = x_bar - const["A2"] * mr_bar
    ucl_mr = const["D4"] * mr_bar
    lcl_mr = const["D3"] * mr_bar

    return {
        "chart_type": "I-MR",
        "statistics": {
            "x_bar": round(x_bar, 6), "mr_bar": round(mr_bar, 6),
            "ucl_x": round(ucl_x, 6), "lcl_x": round(lcl_x, 6), "cl_x": round(x_bar, 6),
            "ucl_mr": round(ucl_mr, 6), "lcl_mr": round(lcl_mr, 6), "cl_mr": round(mr_bar, 6),
        },
        "subgroup_means": [float(v) for v in measurements],
        "subgroup_ranges": [float(v) for v in mr],
        "subgroup_size": 1,
    }


def _xbar_r_chart(subgroups: list, subgroup_size: int) -> dict:
    means = [float(np.mean(sg)) for sg in subgroups]
    ranges = [float(np.max(sg) - np.min(sg)) if len(sg) > 1 else 0.0 for sg in subgroups]
    xbar_bar = float(np.mean(means))
    r_bar = float(np.mean(ranges))
    const = _get_control_chart_constants(subgroup_size)

    ucl_x = xbar_bar + const["A2"] * r_bar
    lcl_x = xbar_bar - const["A2"] * r_bar
    ucl_r = const["D4"] * r_bar
    lcl_r = const["D3"] * r_bar

    return {
        "chart_type": "Xbar-R",
        "statistics": {
            "xbar_bar": round(xbar_bar, 6), "r_bar": round(r_bar, 6),
            "ucl_xbar": round(ucl_x, 6), "lcl_xbar": round(lcl_x, 6), "cl_xbar": round(xbar_bar, 6),
            "ucl_r": round(ucl_r, 6), "lcl_r": round(lcl_r, 6), "cl_r": round(r_bar, 6),
            "a2": const["A2"], "d3": const["D3"], "d4": const["D4"], "subgroup_size": subgroup_size,
        },
        "subgroup_means": means,
        "subgroup_ranges": ranges,
        "subgroup_size": subgroup_size,
    }


def _compute_capability_imr(measurements: np.ndarray, mr_bar: float, usl: float = None, lsl: float = None) -> dict:
    n = len(measurements)
    sigma_within = mr_bar / _get_control_chart_constants(2)["d2"]
    sigma_overall = float(np.std(measurements, ddof=1))
    mu = float(np.mean(measurements))

    result = {"capability_available": False}
    if usl is not None and lsl is not None and lsl < usl:
        cp = (usl - lsl) / (6.0 * sigma_within) if sigma_within > 0 else None
        cpk = min(usl - mu, mu - lsl) / (3.0 * sigma_within) if sigma_within > 0 else None
        pp = (usl - lsl) / (6.0 * sigma_overall) if sigma_overall > 0 else None
        ppk = min(usl - mu, mu - lsl) / (3.0 * sigma_overall) if sigma_overall > 0 else None
        sigma_level = 3.0 * cpk if cpk is not None else None
        result = {"capability_available": True,
                  "cp": round(cp, 4) if cp else None, "cpk": round(cpk, 4) if cpk else None,
                  "pp": round(pp, 4) if pp else None, "ppk": round(ppk, 4) if ppk else None,
                  "sigma_level": round(sigma_level, 4) if sigma_level else None,
                  "sigma_within": round(sigma_within, 6), "sigma_overall": round(sigma_overall, 6),
                  "usl": usl, "lsl": lsl, "mean": round(mu, 6)}
    return result


def _compute_capability_xbar(subgroups: list, r_bar: float, subgroup_size: int, usl: float = None, lsl: float = None) -> dict:
    all_values = np.concatenate([np.array(sg) for sg in subgroups]) if subgroups else np.array([])
    sigma_within = r_bar / _get_control_chart_constants(subgroup_size)["d2"]
    sigma_overall = float(np.std(all_values, ddof=1))
    mu = float(np.mean(all_values))

    result = {"capability_available": False}
    if usl is not None and lsl is not None and lsl < usl:
        cp = (usl - lsl) / (6.0 * sigma_within) if sigma_within > 0 else None
        cpk = min(usl - mu, mu - lsl) / (3.0 * sigma_within) if sigma_within > 0 else None
        pp = (usl - lsl) / (6.0 * sigma_overall) if sigma_overall > 0 else None
        ppk = min(usl - mu, mu - lsl) / (3.0 * sigma_overall) if sigma_overall > 0 else None
        sigma_level = 3.0 * cpk if cpk is not None else None
        result = {"capability_available": True,
                  "cp": round(cp, 4) if cp else None, "cpk": round(cpk, 4) if cpk else None,
                  "pp": round(pp, 4) if pp else None, "ppk": round(ppk, 4) if ppk else None,
                  "sigma_level": round(sigma_level, 4) if sigma_level else None,
                  "sigma_within": round(sigma_within, 6), "sigma_overall": round(sigma_overall, 6),
                  "usl": usl, "lsl": lsl, "mean": round(mu, 6)}
    return result


def _detect_alarms_xbar(means: list, cl: float, ucl: float, lcl: float, sigma: float) -> list:
    alarms = []
    n = len(means)
    if n < 2:
        return alarms

    z_scores = [(means[i] - cl) / sigma if sigma > 0 else 0.0 for i in range(n)]

    # Rule 1: 1 point beyond 3-sigma
    for i, z in enumerate(z_scores):
        if abs(z) > 3.0:
            alarms.append({"rule": "Rule 1: 单点超出3σ控制限", "points": [i + 1], "severity": "critical"})

    # Rule 2: 9 consecutive points on same side of center line
    side = [1 if z > 0 else (-1 if z < 0 else 0) for z in z_scores]
    streak, start = 0, 0
    for i, s in enumerate(side):
        if s == 0:
            streak, start = 0, i + 1
            continue
        if streak == 0 or side[i - 1] == s:
            if streak == 0:
                start = i
            streak += 1
        else:
            streak, start = 1, i
        if streak >= 9:
            alarms.append({"rule": "Rule 2: 连续9点中心线同侧", "points": list(range(start + 1, i + 2)), "severity": "warning"})

    # Rule 3: 6 consecutive points trending up or down
    streak, start, direction = 0, 0, None
    for i in range(1, n):
        if z_scores[i] > z_scores[i - 1]:
            d = 1
        elif z_scores[i] < z_scores[i - 1]:
            d = -1
        else:
            d = 0
        if d != 0 and d == direction:
            streak += 1
            if streak >= 5:
                alarms.append({"rule": "Rule 3: 连续6点递增或递减", "points": list(range(start + 1, i + 2)), "severity": "warning"})
        else:
            streak, start, direction = 1, i - 1, d

    # Rule 4: 14 consecutive points alternating up and down
    streak, start = 0, 0
    for i in range(2, n):
        d1 = 1 if z_scores[i - 1] > z_scores[i - 2] else (-1 if z_scores[i - 1] < z_scores[i - 2] else 0)
        d2 = 1 if z_scores[i] > z_scores[i - 1] else (-1 if z_scores[i] < z_scores[i - 1] else 0)
        if d1 != 0 and d2 == -d1:
            if streak == 0:
                start = i - 2
            streak += 1
            if streak >= 13:
                alarms.append({"rule": "Rule 4: 连续14点交替上下", "points": list(range(start + 1, i + 2)), "severity": "warning"})
        else:
            streak = 0

    # Rule 5: 3 consecutive points with 2 beyond 2-sigma (same side)
    for i in range(2, n):
        window = z_scores[i - 2:i + 1]
        pos_count = sum(1 for z in window if z > 2.0)
        neg_count = sum(1 for z in window if z < -2.0)
        if pos_count >= 2:
            alarms.append({"rule": "Rule 5: 连续3点有2点超出+2σ（同侧）", "points": list(range(i - 1, i + 2)), "severity": "warning"})
        if neg_count >= 2:
            alarms.append({"rule": "Rule 5: 连续3点有2点超出-2σ（同侧）", "points": list(range(i - 1, i + 2)), "severity": "warning"})

    # Rule 6: 5 consecutive points with 4 beyond 1-sigma (same side)
    for i in range(4, n):
        window = z_scores[i - 4:i + 1]
        pos_count = sum(1 for z in window if z > 1.0)
        neg_count = sum(1 for z in window if z < -1.0)
        if pos_count >= 4:
            alarms.append({"rule": "Rule 6: 连续5点有4点超出+1σ（同侧）", "points": list(range(i - 3, i + 2)), "severity": "warning"})
        if neg_count >= 4:
            alarms.append({"rule": "Rule 6: 连续5点有4点超出-1σ（同侧）", "points": list(range(i - 3, i + 2)), "severity": "warning"})

    # Rule 7: 15 consecutive points inside ±1 sigma
    streak, start = 0, 0
    for i, z in enumerate(z_scores):
        if abs(z) < 1.0:
            if streak == 0:
                start = i
            streak += 1
            if streak >= 15:
                alarms.append({"rule": "Rule 7: 连续15点在±1σ内", "points": list(range(start + 1, i + 2)), "severity": "warning"})
        else:
            streak = 0

    # Rule 8: 8 consecutive points all outside ±1 sigma (both sides)
    streak, start = 0, 0
    for i, z in enumerate(z_scores):
        if abs(z) > 1.0:
            if streak == 0:
                start = i
            streak += 1
            if streak >= 8:
                alarms.append({"rule": "Rule 8: 连续8点全部在±1σ外", "points": list(range(start + 1, i + 2)), "severity": "warning"})
        else:
            streak = 0

    seen = set()
    unique = []
    for a in alarms:
        key = (a["rule"], tuple(a["points"]))
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


def _detect_alarms_r(ranges: list, cl: float, ucl: float, lcl: float) -> list:
    alarms = []
    for i, r in enumerate(ranges):
        if r > ucl:
            alarms.append({"rule": "Rule 1: 极差超出上控制限", "points": [i + 1], "severity": "critical"})
    return alarms


def _detect_alarms_imr(measurements: np.ndarray, mr: np.ndarray, cl_x: float, ucl_x: float, lcl_x: float,
                       cl_mr: float, ucl_mr: float, lcl_mr: float) -> list:
    sigma = abs(ucl_x - cl_x) / 3.0 if abs(ucl_x - cl_x) > 0 else 0.001
    alarms = _detect_alarms_xbar(list(measurements), cl_x, ucl_x, lcl_x, sigma)
    for i, r in enumerate(mr):
        if r > ucl_mr:
            alarms.append({"rule": "Rule 1: MR超出上控制限", "points": [i + 2], "severity": "critical"})
    seen = set()
    unique = []
    for a in alarms:
        key = (a["rule"], tuple(a["points"]))
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


def qc_spc_analyze(data_schema: dict, column: str, subgroup_size: int = None, chart_type: str = "auto") -> dict:
    columns_info = data_schema.get("columns", [])
    suggestions = data_schema.get("suggestions", {})
    file_name = data_schema.get("file", "")

    measurement_cols = [c["name"] for c in columns_info if c["type"] == "measurement"]
    batch_cols = [c["name"] for c in columns_info if c["type"] == "batch"]

    if column not in measurement_cols and column not in [c["name"] for c in columns_info]:
        available = [c["name"] for c in columns_info if c["type"] == "measurement"]
        if available:
            column = available[0]

    if subgroup_size is None:
        subgroup_size = suggestions.get("subgroup_size")
    if chart_type == "auto":
        chart_type = suggestions.get("control_chart", "I-MR")

    file_path = data_schema.get("_file_path")
    if file_path:
        df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
    else:
        return {"error": "Cannot access original data file. Provide _file_path in data_schema."}

    values = pd.to_numeric(df[column], errors="coerce").dropna().values

    usl = suggestions.get("usl")
    lsl = suggestions.get("lsl")

    if batch_cols and chart_type in ("Xbar-R", "Xbar-S", "auto"):
        groups = df.groupby(batch_cols[0])[column].apply(list)
        subgroups = [g for g in groups if len(g) >= 2]
        if not subgroups:
            # fall back to I-MR
            result = _imr_chart(values)
            cap = _compute_capability_imr(values, result["statistics"]["mr_bar"], usl, lsl)
            sigma_for_alarms = abs(result["statistics"]["ucl_x"] - result["statistics"]["cl_x"]) / 3.0 if abs(result["statistics"]["ucl_x"] - result["statistics"]["cl_x"]) > 0 else 0.001
            alarms = _detect_alarms_imr(values, np.array(result.get("subgroup_ranges", [])),
                                        result["statistics"]["cl_x"], result["statistics"]["ucl_x"],
                                        result["statistics"]["lcl_x"],
                                        result["statistics"]["cl_mr"], result["statistics"]["ucl_mr"],
                                        result["statistics"]["lcl_mr"])
            return {
                "chart_type": "I-MR",
                "statistics": {**result["statistics"], **cap},
                "alarms": alarms,
                "chart_data": {
                    "subgroups": list(range(1, len(values) + 1)),
                    "xbar_values": result["subgroup_means"],
                    "r_values": result.get("subgroup_ranges", []),
                    "ucl_x_line": result["statistics"]["ucl_x"],
                    "lcl_x_line": result["statistics"]["lcl_x"],
                    "cl_x_line": result["statistics"]["cl_x"],
                    "ucl_r_line": result["statistics"]["ucl_mr"],
                    "lcl_r_line": result["statistics"]["lcl_mr"],
                    "cl_r_line": result["statistics"]["cl_mr"],
                    "usl": usl, "lsl": lsl,
                },
            }

        actual_size = len(subgroups[0]) if subgroups else 1
        result = _xbar_r_chart(subgroups, actual_size)
        cap = _compute_capability_xbar(subgroups, result["statistics"]["r_bar"], actual_size, usl, lsl)
        sigma_for_alarms = abs(result["statistics"]["ucl_xbar"] - result["statistics"]["cl_xbar"]) / 3.0 if abs(result["statistics"]["ucl_xbar"] - result["statistics"]["cl_xbar"]) > 0 else 0.001
        alarms_x = _detect_alarms_xbar(result["subgroup_means"], result["statistics"]["cl_xbar"],
                                       result["statistics"]["ucl_xbar"], result["statistics"]["lcl_xbar"],
                                       sigma_for_alarms)
        alarms_r = _detect_alarms_r(result["subgroup_ranges"], result["statistics"]["cl_r"],
                                    result["statistics"]["ucl_r"], result["statistics"]["lcl_r"])
        alarms = alarms_x + alarms_r

        return {
            "chart_type": "Xbar-R",
            "statistics": {**result["statistics"], **cap},
            "alarms": alarms,
            "chart_data": {
                "subgroups": list(range(1, len(subgroups) + 1)),
                "xbar_values": result["subgroup_means"],
                "r_values": result["subgroup_ranges"],
                "ucl_xbar_line": result["statistics"]["ucl_xbar"],
                "lcl_xbar_line": result["statistics"]["lcl_xbar"],
                "cl_xbar_line": result["statistics"]["cl_xbar"],
                "ucl_r_line": result["statistics"]["ucl_r"],
                "lcl_r_line": result["statistics"]["lcl_r"],
                "cl_r_line": result["statistics"]["cl_r"],
                "usl": usl, "lsl": lsl,
            },
        }

    result = _imr_chart(values)
    cap = _compute_capability_imr(values, result["statistics"]["mr_bar"], usl, lsl)
    alarms = _detect_alarms_imr(values, np.array(result.get("subgroup_ranges", [])),
                                result["statistics"]["cl_x"], result["statistics"]["ucl_x"],
                                result["statistics"]["lcl_x"],
                                result["statistics"]["cl_mr"], result["statistics"]["ucl_mr"],
                                result["statistics"]["lcl_mr"])

    return {
        "chart_type": "I-MR",
        "statistics": {**result["statistics"], **cap},
        "alarms": alarms,
        "chart_data": {
            "subgroups": list(range(1, len(values) + 1)),
            "xbar_values": result["subgroup_means"],
            "r_values": result.get("subgroup_ranges", []),
            "ucl_x_line": result["statistics"]["ucl_x"],
            "lcl_x_line": result["statistics"]["lcl_x"],
            "cl_x_line": result["statistics"]["cl_x"],
            "ucl_r_line": result["statistics"]["ucl_mr"],
            "lcl_r_line": result["statistics"]["lcl_mr"],
            "cl_r_line": result["statistics"]["cl_mr"],
            "usl": usl, "lsl": lsl,
        },
    }
