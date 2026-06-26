"""
Feedback Learning System - 收集用户反馈并与 WHOOP 数据对比学习

学习机制：
1. 睡眠质量：用户主观反馈 vs WHOOP 睡眠效率/深睡眠时长 对比
2. 训练感受：用户主观反馈 vs 实际训练强度（strain/心率）对标
3. 恢复感知：用户感知 vs WHOOP 恢复评分/HRV 对标
4. 有效性追踪：建议被采纳的比例

数据保存在 data/processed/feedback_learn.json
"""

import os
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.environ.get(
    "OPENCLAW_WORKSPACE",
    os.path.dirname(SKILL_DIR)
)
PROCESSED_DIR = os.environ.get(
    "WHOOP_DATA_DIR",
    os.path.join(WORKSPACE_DIR, "data", "processed")
)
FEEDBACK_FILE = os.path.join(PROCESSED_DIR, 'feedback_learn.json')


# ============================================================
# 基础存储
# ============================================================

def _load() -> Dict:
    try:
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return _default()


def _save(data: Dict) -> None:
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _default() -> Dict:
    return {
        "version": 2,
        "feedback": [],          # 所有反馈记录
        "sleep_quality_map": {},   # 用户感知 → WHOOP数据映射（睡眠）
        "training_intensity_map": {},  # 用户感受词 → strain区间
        "recovery_map": {},      # 用户感知 → WHOOP恢复区间
        "adjustments": [],       # 系统调整记录
        "stats": {
            "total_feedbacks": 0,
            "sleep_correlation": 0.0,   # 睡眠反馈与WHOOP数据相关性
            "training_correlation": 0.0, # 训练反馈相关性
        }
    }


# ============================================================
# 反馈录入（与 WHOOP 数据对比）
# ============================================================

FEEDBACK_CATEGORIES = ["sleep", "training", "recovery", "general"]

SLEEP_QUALITY_KEYWORDS = {
    "很好": ["好", "不错", "棒", "充足", "精力充沛"],
    "一般": ["普通", "还行", "一般", "有点累"],
    "差": ["差", "糟糕", "不足", "困", "累", "没睡好"],
}

TRAINING_FEEL_KEYWORDS = {
    "轻松": ["轻松", "easy", "毫不费力", "恢复跑"],
    "正常": ["正常", "不错", "还好", "良好", "良好"],
    "吃力": ["吃力", "累", "喘", "费劲", "强度大"],
    "过度": ["过度", "透支", "太累了", "崩溃", "受伤"],
}

RECOVERY_KEYWORDS = {
    "完全恢复": ["完全恢复", "精力充沛", "满血", "状态好"],
    "部分恢复": ["还行", "一般", "普通", "正常"],
    "未恢复": ["累", "疲惫", "没恢复", "还很累", "透支"],
}


def _classify_sleep(feedback_text: str) -> Optional[str]:
    """从反馈文字推断睡眠质量等级"""
    text = feedback_text.lower()
    for quality, keywords in SLEEP_QUALITY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return quality
    return None


def _classify_training_feel(feedback_text: str) -> Optional[str]:
    """从反馈文字推断训练感受"""
    text = feedback_text.lower()
    for feel, keywords in TRAINING_FEEL_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return feel
    return None


def _classify_recovery(feedback_text: str) -> Optional[str]:
    """从反馈文字推断恢复程度"""
    text = feedback_text.lower()
    for level, keywords in RECOVERY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return level
    return None


def add_feedback(
    category: str,
    feedback_text: str,
    whoop_baseline: Optional[Dict] = None,
    notes: str = ""
) -> Dict:
    """
    记录用户反馈，同时存储 WHOOP 基线数据用于学习

    Args:
        category: sleep | training | recovery | general
        feedback_text: 用户反馈的文字内容
        whoop_baseline: WHOOP 实际数据（如 {'sleep_efficiency': 95, 'strain': 16.0}）
        notes: 额外备注
    """
    data = _load()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "feedback_text": feedback_text,
        "notes": notes,
    }

    # 推断主观等级
    inferred = None
    if category == "sleep":
        inferred = _classify_sleep(feedback_text)
        entry["inferred_sleep"] = inferred
    elif category == "training":
        inferred = _classify_training_feel(feedback_text)
        entry["inferred_training"] = inferred
    elif category == "recovery":
        inferred = _classify_recovery(feedback_text)
        entry["inferred_recovery"] = inferred

    # 存储 WHOOP 基线数据
    if whoop_baseline:
        entry["whoop_baseline"] = whoop_baseline

        # 更新映射表（用户词 → WHOOP数据）
        _update_baseline_map(data, category, entry, whoop_baseline)

    data["feedback"].append(entry)
    data["stats"]["total_feedbacks"] += 1

    _save(data)
    return _get_recent_summary(data)


def _update_baseline_map(
    data: Dict,
    category: str,
    entry: Dict,
    baseline: Dict
) -> None:
    """更新用户词 → WHOOP数据 的映射表"""

    inferred = entry.get(f"inferred_{category}", None) if category in [
        "sleep", "training", "recovery"
    ] else None

    if not inferred:
        return

    if category == "sleep":
        key = "sleep_quality_map"
        if key not in data:
            data[key] = {}
        if inferred not in data[key]:
            data[key][inferred] = {"samples": [], "avg_efficiency": 0, "avg_deep_sleep": 0}

        sample = {
            "sleep_efficiency": baseline.get("sleep_efficiency", 0),
            "deep_sleep_min": baseline.get("deep_sleep_min", 0),
            "sleep_performance": baseline.get("sleep_performance", 0),
            "disturbances": baseline.get("disturbance_count", 0),
        }
        data[key][inferred]["samples"].append(sample)

        # 更新平均值
        samples = data[key][inferred]["samples"]
        n = len(samples)
        data[key][inferred]["avg_efficiency"] = round(
            sum(s["sleep_efficiency"] for s in samples) / n, 1
        )
        data[key][inferred]["avg_deep_sleep"] = round(
            sum(s["deep_sleep_min"] for s in samples) / n, 1
        )

    elif category == "training":
        key = "training_intensity_map"
        if key not in data:
            data[key] = {}
        if inferred not in data[key]:
            data[key][inferred] = {"samples": [], "avg_strain": 0, "avg_hr": 0}

        sample = {
            "strain": baseline.get("strain", 0),
            "avg_hr": baseline.get("avg_hr", 0),
        }
        data[key][inferred]["samples"].append(sample)

        samples = data[key][inferred]["samples"]
        n = len(samples)
        data[key][inferred]["avg_strain"] = round(
            sum(s["strain"] for s in samples) / n, 1
        )
        data[key][inferred]["avg_hr"] = round(
            sum(s["avg_hr"] for s in samples) / n, 1
        )

    elif category == "recovery":
        key = "recovery_map"
        if key not in data:
            data[key] = {}
        if inferred not in data[key]:
            data[key][inferred] = {"samples": [], "avg_recovery": 0, "avg_hrv": 0}

        sample = {
            "recovery_score": baseline.get("recovery_score", 0),
            "hrv": baseline.get("hrv", 0),
            "rhr": baseline.get("rhr", 0),
        }
        data[key][inferred]["samples"].append(sample)

        samples = data[key][inferred]["samples"]
        n = len(samples)
        data[key][inferred]["avg_recovery"] = round(
            sum(s["recovery_score"] for s in samples) / n, 1
        )
        data[key][inferred]["avg_hrv"] = round(
            sum(s["hrv"] for s in samples) / n, 1
        )


# ============================================================
# 学习成果查询
# ============================================================

def get_sleep_quality_baseline(feedback_quality: str) -> Optional[Dict]:
    """
    查询用户说"很好/一般/差"时，对应的 WHOOP 数据基线
    用于理解用户的个人标准
    """
    data = _load()
    sq_map = data.get("sleep_quality_map", {})
    return sq_map.get(feedback_quality)


def get_training_feel_baseline(feel: str) -> Optional[Dict]:
    """查询用户说"轻松/正常/吃力"时，对应的训练数据基线"""
    data = _load()
    ti_map = data.get("training_intensity_map", {})
    return ti_map.get(feel)


def get_recovery_baseline(level: str) -> Optional[Dict]:
    """查询用户说"完全恢复/部分恢复/未恢复"时，对应的恢复数据基线"""
    data = _load()
    rc_map = data.get("recovery_map", {})
    return rc_map.get(level)


def get_recent_summary(data: Dict = None) -> Dict:
    """获取最近的学习摘要"""
    if data is None:
        data = _load()

    feedbacks = data.get("feedback", [])
    recent = feedbacks[-10:] if len(feedbacks) > 10 else feedbacks

    return {
        "total": data["stats"]["total_feedbacks"],
        "recent": recent[::-1],  # 最新的在前
        "sleep_map": data.get("sleep_quality_map", {}),
        "training_map": data.get("training_intensity_map", {}),
        "recovery_map": data.get("recovery_map", {}),
    }


def _get_recent_summary(data: Dict) -> Dict:
    return get_recent_summary(data)


# ============================================================
# 调整建议生成
# ============================================================

def should_adjust_recommendation(
    category: str,
    inferred_level: str,
    current_whoop: Dict
) -> Tuple[bool, str]:
    """
    判断是否需要调整建议

    Returns:
        (should_adjust: bool, reason: str)
    """
    data = _load()

    if category == "sleep":
        baseline = get_sleep_quality_baseline(inferred_level)
        if not baseline or baseline["samples"] < 3:
            return False, ""

        # 用户说睡眠"差"，但 WHOOP 效率>90% → 可能需要提醒用户注意入睡时机
        current_eff = current_whoop.get("sleep_efficiency", 0)
        if inferred_level == "差" and current_eff > 90:
            return True, "用户感知睡眠差，但WHOOP效率正常偏高，可能存在主观入睡困难"
        # 用户说睡眠"好"，但实际效率<85% → 建议改善睡眠卫生
        if inferred_level == "很好" and current_eff < 85:
            return True, "用户感知睡眠好，但WHOOP效率偏低，可能存在测量误差或习惯性低估"

    elif category == "training":
        baseline = get_training_feel_baseline(inferred_level)
        if not baseline or baseline["samples"] < 3:
            return False, ""

        current_strain = current_whoop.get("strain", 0)
        avg_strain = baseline["avg_strain"]
        if inferred_level == "正常" and abs(current_strain - avg_strain) > 3:
            if current_strain > avg_strain + 3:
                return True, f"训练强度({current_strain})明显高于用户正常水平({avg_strain})，建议加强恢复"
            if current_strain < avg_strain - 3:
                return True, f"训练强度({current_strain})明显低于用户正常水平({avg_strain})，可能是休息日"

    elif category == "recovery":
        baseline = get_recovery_baseline(inferred_level)
        if not baseline or baseline["samples"] < 3:
            return False, ""

        current_rec = current_whoop.get("recovery_score", 0)
        avg_rec = baseline["avg_recovery"]
        if inferred_level == "完全恢复" and current_rec < 60:
            return True, "用户感知完全恢复，但WHOOP恢复评分偏低，建议保持当前节奏"
        if inferred_level == "未恢复" and current_rec > 70:
            return True, "用户感知未恢复，但WHOOP恢复评分良好，可能需要关注心理状态"

    return False, ""


# ============================================================
# 打印学习统计（CLI工具）
# ============================================================

def print_learning_stats() -> None:
    """打印学习统计"""
    data = _load()
    total = data["stats"]["total_feedbacks"]

    print("📊 反馈学习统计")
    print("-" * 50)
    print(f"总反馈数：{total}")
    print()

    sq = data.get("sleep_quality_map", {})
    if sq:
        print("😴 睡眠感知基线（用户词 → WHOOP数据）：")
        for quality, info in sq.items():
            n = len(info["samples"])
            print(f"  「{quality}」（{n}次样本）")
            print(f"    平均睡眠效率：{info['avg_efficiency']:.1f}%")
            print(f"    平均深睡眠：{info['avg_deep_sleep']:.0f}min")
        print()

    ti = data.get("training_intensity_map", {})
    if ti:
        print("🏃 训练感受基线（用户词 → 训练数据）：")
        for feel, info in ti.items():
            n = len(info["samples"])
            print(f"  「{feel}」（{n}次样本）")
            print(f"    平均strain：{info['avg_strain']:.1f}")
            print(f"    平均心率：{info['avg_hr']:.0f}bpm")
        print()

    rc = data.get("recovery_map", {})
    if rc:
        print("💪 恢复感知基线（用户词 → 恢复数据）：")
        for level, info in rc.items():
            n = len(info["samples"])
            print(f"  「{level}」（{n}次样本）")
            print(f"    平均恢复评分：{info['avg_recovery']:.1f}%")
            print(f"    平均HRV：{info['avg_hrv']:.1f}ms")
        print()

    if total == 0:
        print("暂无反馈数据，开始打卡后将自动积累。")


# CLI
if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print_learning_stats()
    elif sys.argv[1] == "add":
        # add <category> <feedback_text> [notes]
        cat = sys.argv[2] if len(sys.argv) > 2 else "general"
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        result = add_feedback(cat, text, notes=notes)
        print(f"✅ 反馈已记录")
    elif sys.argv[1] == "stats":
        print_learning_stats()
